# -*- coding: utf-8 -*-
"""합류도 검사 — 지도가 가리키는 글이 실제로 있나.

지도는 카드를 headline 문자열로만 가리킨다(insights/merges.py). 글 제목이 바뀌면
지도가 조용히 빈 칸이 된다. 그 조용함을 막는 검사다.

  M1  칸이 가리키는 headline 이 실제 글에 없다
  M2  한 지도 안에서 같은 글이 두 칸에 배정됐다
  M3  merge 칸이 비었다
  M4  outer·price 칸이 하나도 없다

한 글이 **여러 지도**에 서는 것은 막지 않는다 — 「메모리」 지도와 「자본조달」 지도가
같은 카드를 공유하는 것이 자연스럽다. 겹침은 같은 지도 안에서만 잡는다.

  py -3.13 insights/check_merge.py
"""
import glob
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merges
import notes_lib as nl
import paths

FAILS = []


def add(rule, where, msg):
    FAILS.append((rule, where, msg))


def headlines():
    out = set()
    for d in (paths.BRIEFS, paths.SYNTH, paths.THESES):
        for f in sorted(glob.glob(os.path.join(d, '*.md'))):
            meta, _b = nl.parse_front(io.open(f, encoding='utf-8').read())
            h = meta.get('headline') or os.path.basename(f)[:-3]
            out.add(h)
    return out


def main():
    have = headlines()
    n_cell = 0
    for m in merges.MERGES:
        where = m['id']
        rows = merges.cells(m)
        n_cell += len(rows)
        seen = {}
        for cid, col, label, heads in rows:
            for h in heads:
                if h not in have:
                    add('M1', cid, '이 headline 을 가진 글이 없다: %r' % h)
                if h in seen:
                    add('M2', cid, '같은 지도의 %s 칸과 겹친다: %r' % (seen[h], h))
                seen[h] = label
        if not m['merge'][1]:
            add('M3', where, 'merge 칸에 배정된 글이 없다')
        if not (m['outer'] and m['price']):
            add('M4', where, 'outer 또는 price 칸이 비었다')

    for rule, where, msg in FAILS:
        print('FAIL %s  %s  %s' % (rule, where, msg))
    print('요약: 지도 %d장 / 칸 %d개 / 글 %d편 / FAIL %d'
          % (len(merges.MERGES), n_cell, len(have), len(FAILS)))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
