# -*- coding: utf-8 -*-
"""모델 층 도해를 낱장으로 찍는다. 눈으로 봐야 잡히는 결함이 있다.

    PYTHONIOENCODING=utf-8 python scratchpad/_shot_model.py [카드파일조각]
"""
import glob
import os
import sys

import playwright.sync_api as pw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scratchpad', '_shot_model')


def main():
    frag = sys.argv[1] if len(sys.argv) > 1 else '모델-총정리'
    hits = [p for p in glob.glob(os.path.join(ROOT, '대시보드', 'report', '*.html'))
            if frag in os.path.basename(p)]
    if not hits:
        print('그런 카드가 없다:', frag)
        return 1
    card = hits[0]
    os.makedirs(OUT, exist_ok=True)
    url = 'file:///' + card.replace(os.sep, '/')
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width': 900, 'height': 1400})
        page.goto(url)
        page.wait_for_timeout(600)
        page.evaluate("document.querySelectorAll('[hidden]')"
                      ".forEach(e => e.removeAttribute('hidden'))")
        page.wait_for_timeout(300)
        svgs = page.query_selector_all('svg')
        print('svg 개수:', len(svgs))
        for i, s in enumerate(svgs):
            try:
                s.scroll_into_view_if_needed(timeout=3000)
                page.wait_for_timeout(80)
                s.screenshot(path=os.path.join(OUT, 'fig%02d.png' % i))
            except Exception as exc:  # noqa: BLE001
                print(i, '건너뜀', type(exc).__name__)
        b.close()
    print('저장:', OUT)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
