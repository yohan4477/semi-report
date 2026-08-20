# -*- coding: utf-8 -*-
"""축 검사 — 사슬이 실제 글과 맞나, 그리고 못 쓸 근거를 인용했나.

  A1  글이 밝힌 axis/cell 이 축에 없다
  A2  한 축 안에서 같은 글이 두 칸에 섰다
  A3  옛 글 41장이 여덟 편에 정확히 한 번씩 안 들어갔다 (이행 중에는 WARN)
  S1  충돌을 다루는 절이 있는데 「누가 더 가까이서 봤나」가 없다 (당분간 WARN)
  L1  배제된 링크드인 게시물의 줄을 인용했다
  L2  링크드인 인용의 기준일을 못 읽는다

  py -3.13 insights/check_axes.py
"""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import axes
import notes_lib as nl
import paths

FINDINGS = []
NEAR = '누가 더 가까이서 봤나'
CLASH = re.compile(r'^##\s*(조건 충돌|어긋나는 자리|갈리는 자리)', re.M)
LI_DIR = 'content/linkedin/'


def add(level, rule, where, msg):
    FINDINGS.append((level, rule, where, msg))


def li_excluded():
    """배제된 게시물의 기준일 집합. li_signal 이 usable=False 로 표시한 것."""
    p = os.path.join(paths.HERE, 'views', 'li_signals.json')
    if not os.path.isfile(p):
        return set()
    d = json.load(io.open(p, encoding='utf-8'))
    return set((s.get('basis_date'), s.get('id')) for s in d.get('signals', [])
               if not s.get('usable'))


def li_usable_dates():
    p = os.path.join(paths.HERE, 'views', 'li_signals.json')
    if not os.path.isfile(p):
        return set()
    d = json.load(io.open(p, encoding='utf-8'))
    return set(s.get('basis_date') for s in d.get('signals', []) if s.get('usable'))


def loop_files():
    return sorted(glob.glob(os.path.join(paths.LOOP, '*.md')))


def old_files():
    return sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md')) +
                  glob.glob(os.path.join(paths.SYNTH, '*.md')))


def main():
    known = axes.all_cell_ids()
    ok_dates = li_usable_dates()
    seen_cell = {}
    merged = []

    for f in loop_files():
        where = os.path.basename(f)
        raw = io.open(f, encoding='utf-8').read()
        meta, body = nl.parse_front(raw)
        aid, cid = meta.get('axis', ''), meta.get('cell', '')
        if (aid, cid) not in known:
            add('FAIL', 'A1', where, '축에 없는 자리다: axis=%r cell=%r' % (aid, cid))
        key = (aid, cid)
        if key in seen_cell:
            add('FAIL', 'A2', where, '%s 와 같은 칸에 두 편이 섰다' % seen_cell[key])
        seen_cell[key] = where

        merged += re.findall(r'^\s*-\s*"(.+?)"\s*$',
                             meta.get('_head', '').split('merged:')[-1].split('sources:')[0], re.M)

        if CLASH.search(body) and NEAR not in body:
            add('WARN', 'S1', where, '충돌 절이 있는데 「%s」가 없다' % NEAR)

        src = nl.sources_of(meta)
        for ref in nl.cite_refs(body, src):
            f2 = (ref.get('file') or '').replace('\\', '/')
            if not f2.startswith(LI_DIR) or not ref.get('lines'):
                continue
            b = nl.li_basis(f2, ref['lines'][0])
            if not b:
                add('FAIL', 'L2', where, '링크드인 인용의 기준일을 못 읽는다: L%d'
                    % ref['lines'][0])
            elif b not in ok_dates:
                add('FAIL', 'L1', where,
                    '배제된 링크드인 게시물을 인용했다: %s L%d' % (b, ref['lines'][0]))

    # A3 — 옛 글이 정확히 한 번씩 흡수됐나
    old = []
    for f in old_files():
        meta, _b = nl.parse_front(io.open(f, encoding='utf-8').read())
        old.append(meta.get('headline') or os.path.basename(f)[:-3])
    dup = sorted(h for h in set(merged) if merged.count(h) > 1)
    ghost = sorted(h for h in merged if h not in old)
    left = sorted(h for h in old if h not in merged)
    for h in dup:
        add('FAIL', 'A3', '-', '두 편이 같은 글을 흡수했다: %r' % h)
    for h in ghost:
        add('FAIL', 'A3', '-', '흡수했다는 글이 없다: %r' % h)
    if left:
        add('WARN', 'A3', '-', '아직 안 흡수된 옛 글 %d장' % len(left))

    for level, rule, where, msg in FINDINGS:
        print('%s %s  %s  %s' % (level, rule, where, msg))
    fails = sum(1 for f in FINDINGS if f[0] == 'FAIL')
    warns = len(FINDINGS) - fails
    print('요약: 축 %d개 / 고리 글 %d편 / 남은 옛 글 %d장 / FAIL %d / WARN %d'
          % (len(axes.AXES), len(loop_files()), len(left), fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
