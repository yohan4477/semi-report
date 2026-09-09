# -*- coding: utf-8 -*-
"""카드 한 장을 세로로 이어 찍는다. 표와 수식은 도해와 달리 흐름으로 봐야 한다.

    PYTHONIOENCODING=utf-8 python scratchpad/_shot_card.py 모델-총정리 [선택자]
"""
import glob
import os
import sys

import playwright.sync_api as pw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scratchpad', '_shot_card')


def main():
    frag = sys.argv[1] if len(sys.argv) > 1 else '모델-총정리'
    sel = sys.argv[2] if len(sys.argv) > 2 else '.xls, .eqbox'
    hits = [p for p in glob.glob(os.path.join(ROOT, '대시보드', 'report', '*.html'))
            if frag in os.path.basename(p)]
    if not hits:
        print('그런 카드가 없다:', frag)
        return 1
    os.makedirs(OUT, exist_ok=True)
    url = 'file:///' + hits[0].replace(os.sep, '/')
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width': 900, 'height': 1200})
        page.goto(url)
        page.wait_for_timeout(600)
        page.evaluate("document.querySelectorAll('[hidden]')"
                      ".forEach(e => e.removeAttribute('hidden'))")
        page.wait_for_timeout(300)
        els = page.query_selector_all(sel)
        print('조각 개수:', len(els))
        for i, e in enumerate(els):
            try:
                e.scroll_into_view_if_needed(timeout=3000)
                page.wait_for_timeout(80)
                e.screenshot(path=os.path.join(OUT, 'p%02d.png' % i))
            except Exception as exc:  # noqa: BLE001
                print(i, '건너뜀', type(exc).__name__)
        b.close()
    print('저장:', OUT)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
