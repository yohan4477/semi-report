# -*- coding: utf-8 -*-
"""새로고침하면 맨 위에서 시작하는가 — 대시보드 전부(하위 글 페이지 포함).

브라우저는 기본으로 새로고침 때 스크롤 자리를 되살린다. 첫 화면이 최신순 목록이 되면서
페이지가 길어졌고, 그래서 새로고침하면 목록 한가운데가 나왔다(2026-09-08 지적).
`scripts/ui_bits.py` 의 OPEN_AT_TOP 이 그것을 끄고, 여기서는 그 조각이 모든 페이지에
실렸는지만 센다 — 글자 검사라 빠르고 빠짐이 없다. 실제로 어디서 시작하는지는
브라우저로 재는 편이 확실하지만(scratchpad/probe 계열), 매번 돌리기에는 느리다.

  PYTHONIOENCODING=utf-8 python scratchpad/check_scrolltop.py
"""
import glob
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = os.path.join(ROOT, '대시보드')
MARK = 'scrollRestoration'


def main():
    files = sorted(glob.glob(os.path.join(DASH, '**', '*.html'), recursive=True))
    bad = []
    skipped = 0
    for p in files:
        s = io.open(p, encoding='utf-8').read()
        # 넘김 페이지(묶음 글로 곧바로 보내는 줄)는 머무는 화면이 아니다 — 잴 것이 없다
        if 'http-equiv="refresh"' in s:
            skipped += 1
            continue
        if MARK not in s:
            bad.append(os.path.relpath(p, ROOT))
    for b in bad[:20]:
        print('FAIL 새로고침이 중간에서 시작한다 — %s' % b)
    if len(bad) > 20:
        print('  … 외 %d장' % (len(bad) - 20))
    print('\n요약: 페이지 %d장(넘김 %d장은 건너뜀) / FAIL %d'
          % (len(files), skipped, len(bad)))
    return 1 if bad else 0


sys.exit(main())
