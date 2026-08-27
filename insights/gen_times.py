# -*- coding: utf-8 -*-
"""times.json — 색인이 가리키는 줄만 훑어 가리키는 때를 적는다.

희소하게 둔다. 명시되거나 계산된 줄만 적고 상속은 안 적는다. 상속은 조회할 때
쓴 날로 채운다. 없는 것을 안 적어야 파일이 작고 「이건 상속이다」가 구분된다.

코퍼스 88,900줄을 다 훑지 않고 색인이 가리키는 11,910줄만 본다. 개체가 안 나온
줄은 조회에 안 실리므로 때를 매길 이유가 없다.

  py -3.13 insights/gen_times.py
"""
import collections
import datetime
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402
import source_lines as sl  # noqa: E402
import times  # noqa: E402
import utterance as ut  # noqa: E402


def indexed_lines(idx):
    by = collections.defaultdict(set)
    for name, addrs in idx.items():
        if name == '_meta':
            continue
        for a in addrs:
            rel, _, num = a.rpartition('#L')
            if num.isdigit():
                by[rel].add(int(num))
    return by


def build(root, idx, meta):
    by = indexed_lines(idx)
    hits = {}
    for rel in sorted(by):
        utter = ut.date_of(meta, rel)
        if not utter:
            continue
        nums = by[rel]
        for n, line in enumerate(sl.lines(root, rel), 1):
            if n not in nums:
                continue
            got = times.find(line, utter)
            if got:
                hits['%s#L%d' % (rel, n)] = got
    out = {'_meta': {
        'built': datetime.date.today().isoformat(),
        'index_fingerprint': (idx.get('_meta') or {}).get('fingerprint', ''),
        'lines': len(hits),
    }}
    for k in sorted(hits):
        out[k] = hits[k]
    return out


def main():
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    meta = ut.load(paths.ROOT)
    out = build(paths.ROOT, idx, meta)
    with io.open(paths.TIMES, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=0, sort_keys=True)
        f.write('\n')
    how = collections.Counter()
    tense = collections.Counter()
    for k, v in out.items():
        if k == '_meta':
            continue
        how[v['how']] += 1
        tense[v['tense']] += 1
    print('때를 매긴 줄 %d — %s'
          % (out['_meta']['lines'],
             ' · '.join('%s %d' % (k, how[k]) for k in sorted(how))))
    print('시제 — %s' % ' · '.join('%s %d' % (k, tense[k]) for k in sorted(tense)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
