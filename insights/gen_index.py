# -*- coding: utf-8 -*-
"""색인 — 코퍼스를 줄 단위로 훑어 개체마다 줄 주소를 적는다.

본문은 안 담는다. 주소만 담는다. cites.json 이 해시만 갖는 것과 같은 이유로,
본문을 넣으면 파일이 세 배로 붇고 원문이 바뀌었을 때 두 곳이 어긋난다.

증분으로 만든다. _meta.files_stat 에 파일별 [해시, 줄 수] 를 적어 두고, 다음
번에는 해시가 바뀐 파일만 다시 훑어 그 파일 주소만 갈아끼운다. 478편 전수가
41초인데 새 글 한 편은 그중 한 편만 읽으면 된다.

전수로 되돌아가는 경우가 하나 있다 — 사전(entities.json)이 바뀌었을 때다.
별칭 하나가 늘면 모든 줄의 판정이 달라지므로 옛 주소를 하나도 못 믿는다.
그래서 _meta.entities_hash 를 같이 적고 다르면 전부 다시 훑는다.

  py -3.13 insights/gen_index.py
  py -3.13 insights/gen_index.py --full     증분을 건너뛰고 전수로 만든다
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
    out = [os.path.relpath(p, root).replace(os.sep, '/')
           for p in glob.glob(pat, recursive=True)]
    return sorted(out)


def file_hashes(root, files):
    out = {}
    for rel in files:
        with io.open(os.path.join(root, rel.replace('/', os.sep)), 'rb') as f:
            out[rel] = hashlib.sha1(f.read()).hexdigest()
    return out


def fingerprint_of(hashes):
    h = hashlib.sha1()
    for rel in sorted(hashes):
        h.update(rel.encode('utf-8'))
        h.update(hashes[rel].encode('ascii'))
    return h.hexdigest()


def fingerprint(root, files):
    return fingerprint_of(file_hashes(root, files))


def entities_hash(rows):
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(payload.encode('utf-8')).hexdigest()


def _addr_key(addr):
    rel, _, num = addr.rpartition('#L')
    return (rel, int(num) if num.isdigit() else 0)


def scan(root, rows, files):
    """그 파일들만 훑는다. -> (개체 -> 주소 목록, 파일 -> 줄 수)"""
    rules = mt.compile_rules(rows)
    hits = {}
    lines = {}
    for rel in files:
        n = 0
        with io.open(os.path.join(root, rel.replace('/', os.sep)),
                     encoding='utf-8', errors='replace') as f:
            for n, line in enumerate(f, 1):
                for c in mt.find(line, rules):
                    hits.setdefault(c, []).append('%s#L%d' % (rel, n))
        lines[rel] = n
    return hits, lines


def _reusable(old, ehash):
    """옛 색인을 믿어도 되나. 사전이 그대로여야 하고 파일별 자료가 있어야 한다."""
    if not old:
        return False
    meta = old.get('_meta') or {}
    return bool(meta.get('files_stat')) and meta.get('entities_hash') == ehash


def build(root, rows, files, old=None):
    ehash = entities_hash(rows)
    hashes = file_hashes(root, files)

    if _reusable(old, ehash):
        stat = old['_meta']['files_stat']
        fresh = [rel for rel in files if (stat.get(rel) or [None])[0] != hashes[rel]]
        drop = set(fresh) | (set(stat) - set(files))
        hits = {}
        for name, addrs in old.items():
            if name == '_meta':
                continue
            keep = [a for a in addrs if a.rpartition('#L')[0] not in drop]
            if keep:
                hits[name] = keep
        lines = {rel: stat[rel][1] for rel in files if rel not in fresh}
    else:
        fresh = list(files)
        hits = {}
        lines = {}

    got, got_lines = scan(root, rows, fresh)
    for name, addrs in got.items():
        hits.setdefault(name, []).extend(addrs)
    lines.update(got_lines)

    out = {'_meta': {
        'built': datetime.date.today().isoformat(),
        'files': len(files),
        'lines': sum(lines[rel] for rel in files),
        'fingerprint': fingerprint_of(hashes),
        'entities_hash': ehash,
        'files_stat': {rel: [hashes[rel], lines[rel]] for rel in files},
    }}
    for c in sorted(hits):
        out[c] = sorted(hits[c], key=_addr_key)
    return out


def main():
    rows = el.load()
    files = corpus_files(paths.ROOT)
    old = None
    if '--full' not in sys.argv and os.path.exists(paths.INDEX):
        with io.open(paths.INDEX, encoding='utf-8') as f:
            old = json.load(f)
    idx = build(paths.ROOT, rows, files, old)
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
