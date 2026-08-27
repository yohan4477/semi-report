# -*- coding: utf-8 -*-
"""색인 — 코퍼스를 줄 단위로 훑어 개체마다 줄 주소를 적는다.

본문은 안 담는다. 주소만 담는다. cites.json 이 해시만 갖는 것과 같은 이유로,
본문을 넣으면 파일이 세 배로 붇고 원문이 바뀌었을 때 두 곳이 어긋난다.

  py -3.13 insights/gen_index.py
"""
import datetime
import glob
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entities_lib as el  # noqa: E402
import matcher as mt  # noqa: E402
import paths  # noqa: E402


def corpus_files(root):
    pat = os.path.join(root, 'content', '**', '*.md')
    out = [os.path.relpath(p, root).replace('\\', '/')
           for p in glob.glob(pat, recursive=True)]
    return sorted(out)


def fingerprint(root, files):
    h = hashlib.sha1()
    for rel in files:
        h.update(rel.encode('utf-8'))
        with io.open(os.path.join(root, rel), 'rb') as f:
            h.update(hashlib.sha1(f.read()).hexdigest().encode('ascii'))
    return h.hexdigest()


def build(root, rows, files):
    rules = mt.compile_rules(rows)
    hits = {}
    lines = 0
    for rel in files:
        with io.open(os.path.join(root, rel), encoding='utf-8',
                     errors='replace') as f:
            for n, line in enumerate(f, 1):
                lines += 1
                for c in mt.find(line, rules):
                    hits.setdefault(c, []).append('%s#L%d' % (rel, n))
    out = {'_meta': {
        'built': datetime.date.today().isoformat(),
        'files': len(files),
        'lines': lines,
        'fingerprint': fingerprint(root, files),
    }}
    for c in sorted(hits):
        out[c] = hits[c]
    return out


def main():
    rows = el.load()
    files = corpus_files(paths.ROOT)
    idx = build(paths.ROOT, rows, files)
    with io.open(paths.INDEX, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(idx, f, ensure_ascii=False, indent=0, sort_keys=True)
        f.write('\n')
    m = idx['_meta']
    total = sum(len(v) for k, v in idx.items() if k != '_meta')
    print('파일 %d · 줄 %d · 개체 %d · hit %d'
          % (m['files'], m['lines'], len(idx) - 1, total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
