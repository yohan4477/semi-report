# -*- coding: utf-8 -*-
"""조회 — 색인에서 주소를 받고 그 줄만 읽는다. 아무것도 쓰지 않는다.

답에 영수증을 붙인다. 색인을 언제 어느 지문으로 만들었는지, 몇 줄을 봤는지,
그리고 상한에 걸려 몇 줄을 안 봤는지. 마지막 것이 없으면 잘린 답과 다 본 답이
화면에서 똑같아 보인다.

  py -3.13 scripts/q.py 램리서치
  py -3.13 scripts/q.py 램리서치 --cap 100
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import paths  # noqa: E402

CAP = 40


def read_line(root, rel, num):
    full = os.path.join(root, rel.replace('/', os.sep))
    if not os.path.isfile(full):
        return ''
    with io.open(full, encoding='utf-8', errors='replace') as f:
        for n, line in enumerate(f, 1):
            if n == num:
                return line.strip()
    return ''


def lookup(root, idx, name, cap=CAP):
    addrs = idx.get(name) or []
    meta = idx.get('_meta') or {}
    shown = addrs[:cap]
    rows = []
    for addr in shown:
        rel, _, num = addr.rpartition('#L')
        rows.append({'addr': addr,
                     'text': read_line(root, rel, int(num)) if num.isdigit() else ''})
    return {
        'name': name,
        'total': len(addrs),
        'shown': len(shown),
        'cut': len(addrs) - len(shown),
        'files': len({a.rpartition('#L')[0] for a in addrs}),
        'built': meta.get('built', ''),
        'fingerprint': meta.get('fingerprint', ''),
        'rows': rows,
    }


def render(r):
    out = ['%s · 원문 %d편 · %d줄' % (r['name'], r['files'], r['total'])]
    for i, row in enumerate(r['rows'], 1):
        out.append('  [%d] %s' % (i, row['addr']))
        if row['text']:
            out.append('      %s' % row['text'][:120])
    out.append('  — 영수증 — 색인 %s (%s) · 본 줄 %d · 잘림 %d'
               % (r['built'], r['fingerprint'][:8], r['shown'], r['cut']))
    return '\n'.join(out)


def main(argv):
    if len(argv) < 2:
        print('쓰기: py -3.13 scripts/q.py <개체 이름> [--cap N]')
        return 1
    name = argv[1]
    cap = CAP
    if '--cap' in argv:
        cap = int(argv[argv.index('--cap') + 1])
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    print(render(lookup(ROOT, idx, name, cap)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
