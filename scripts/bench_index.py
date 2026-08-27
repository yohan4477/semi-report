# -*- coding: utf-8 -*-
"""판정 — 색인이 그냥 문자열 훑기보다 나은가.

사람이 손으로 찾을 때 떠올리는 표기는 보통 하나다. 색인은 별칭 전부를 안다.
그 차이가 실제로 줄 수로 나타나는지를 본다. 안 나타나면 색인을 만들 이유가 없다.

  py -3.13 scripts/bench_index.py
"""
import glob
import io
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import paths  # noqa: E402
import q  # noqa: E402

CASES = [
    {'entity': '램리서치', 'needles': ['램리서치']},
    {'entity': '도쿄일렉트론', 'needles': ['도쿄일렉트론']},
    {'entity': '엔비디아', 'needles': ['엔비디아']},
    {'entity': '앤트로픽', 'needles': ['앤트로픽']},
    {'entity': 'TSMC', 'needles': ['TSMC']},
]

SEP = chr(92)


def corpus_files(root):
    pat = os.path.join(root, 'content', '**', '*.md')
    return sorted(os.path.relpath(p, root).replace(SEP, '/')
                  for p in glob.glob(pat, recursive=True))


def grep_hits(root, needles):
    out = []
    for rel in corpus_files(root):
        with io.open(os.path.join(root, rel), encoding='utf-8',
                     errors='replace') as f:
            for n, line in enumerate(f, 1):
                if any(x in line for x in needles):
                    out.append('%s#L%d' % (rel, n))
    return out


def compare(root, idx, case):
    g = set(grep_hits(root, case['needles']))
    i = set(idx.get(case['entity']) or [])
    return {
        'entity': case['entity'],
        'grep': len(g),
        'index': len(i),
        'index_only': sorted(i - g),
        'grep_only': sorted(g - i),
        'covers': not (g - i),
    }


def main():
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    t0 = time.time()
    rows = [compare(ROOT, idx, c) for c in CASES]
    grep_secs = time.time() - t0

    t1 = time.time()
    for c in CASES:
        q.lookup(ROOT, idx, c['entity'], cap=40)
    idx_secs = time.time() - t1

    print('%-14s %8s %8s %10s %9s' % ('개체', 'grep', '색인', '색인만', '놓친 것'))
    for r in rows:
        print('%-14s %8d %8d %10d %9d'
              % (r['entity'], r['grep'], r['index'],
                 len(r['index_only']), len(r['grep_only'])))
    print()
    print('전수 훑기 %.2fs · 색인 조회 %.3fs' % (grep_secs, idx_secs))
    bad = [r['entity'] for r in rows if not r['covers']]
    if bad:
        print('놓친 것이 있다: %s' % ', '.join(bad))
    print()
    print('표본 검토용 — 색인만 잡은 줄 다섯')
    for r in rows:
        for addr in r['index_only'][:5]:
            rel, _, num = addr.rpartition('#L')
            print('  %-10s %s  %s'
                  % (r['entity'], addr, q.read_line(ROOT, rel, int(num))[:80]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
