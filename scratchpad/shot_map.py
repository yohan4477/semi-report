# -*- coding: utf-8 -*-
"""AI 인프라 지도 한 장을 브라우저로 열어 화면을 본다.

    py -3.13 scratchpad/shot_map.py

check_ui 는 만들어진 글자를 본다. 여기서는 브라우저가 그린 화면을 본다 —
한눈이 먼저 보이는가, 공정 칸을 누르면 그 공정만 서는가, 잎을 누르면 패널이 차는가.
"""
import asyncio
import io
import os
import sys

from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, '대시보드', 'AI 인프라 지도.html')
SHOT = os.path.join(ROOT, 'scratchpad', '_shot_map')


async def main():
    bad = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={'width': 1100, 'height': 900})
        await pg.goto('file:///' + PAGE.replace('\\', '/'))
        await pg.wait_for_timeout(400)

        # 한눈이 먼저 선다
        panes = await pg.eval_on_selector_all(
            '.pane:not(.off)', 'els => els.map(e => e.dataset.proc)')
        if panes != ['all']:
            bad.append('첫 화면이 %r — 한눈 하나여야 한다' % panes)
        boxes = await pg.locator('.ovbox').count()
        if boxes != 5:
            bad.append('한눈 상자가 %d개 — 공정 다섯이어야 한다' % boxes)
        await pg.screenshot(path=SHOT + '_1_overview.png', full_page=False)

        # 공정 칸을 누르면 그 공정만 선다
        await pg.click('.pchip[data-proc="litho"]')
        await pg.wait_for_timeout(300)
        panes = await pg.eval_on_selector_all(
            '.pane:not(.off)', 'els => els.map(e => e.dataset.proc)')
        if panes != ['litho']:
            bad.append('공정을 골랐는데 선 화면이 %r' % panes)
        vis = await pg.eval_on_selector_all(
            '.pane:not(.off) .mapwrap:not(.off)', 'els => els.map(e => e.dataset.proc + "/" + e.dataset.view)')
        if vis != ['litho/func']:
            bad.append('보이는 지도가 %r — litho/func 하나여야 한다' % vis)
        await pg.screenshot(path=SHOT + '_2_litho.png', full_page=False)

        # 잎을 누르면 패널이 찬다
        await pg.click('.pane:not(.off) .leaf:not(.dim)')
        await pg.wait_for_timeout(300)
        txt = await pg.inner_text('#panel')
        if '회' not in txt or len(txt) < 60:
            bad.append('잎을 눌렀는데 패널이 안 찼다: %r' % txt[:80])
        await pg.screenshot(path=SHOT + '_3_panel.png', full_page=False)

        # 뷰 칩이 그 공정 안에서만 바뀐다
        await pg.click('.chip[data-proc="litho"][data-view="supply"]')
        await pg.wait_for_timeout(300)
        vis = await pg.eval_on_selector_all(
            '.pane:not(.off) .mapwrap:not(.off)', 'els => els.map(e => e.dataset.proc + "/" + e.dataset.view)')
        if vis != ['litho/supply']:
            bad.append('뷰를 바꿨더니 보이는 지도가 %r' % vis)

        # 좁은 화면에서는 목록이 대신 선다
        await pg.set_viewport_size({'width': 420, 'height': 900})
        await pg.wait_for_timeout(300)
        wide = await pg.locator('.wide').first.is_visible()
        narrow = await pg.locator('.narrow').first.is_visible()
        if wide or not narrow:
            bad.append('좁은 화면에서 지도 %s · 목록 %s' % (wide, narrow))
        await pg.screenshot(path=SHOT + '_4_narrow.png', full_page=False)

        # 가로 스크롤이 몸통에 생기면 안 된다
        over = await pg.evaluate(
            'document.documentElement.scrollWidth > document.documentElement.clientWidth')
        if over:
            bad.append('좁은 화면에서 몸통이 가로로 넘친다')
        await b.close()
    for x in bad:
        print('FAIL ' + x)
    print('요약: 화면 검사 FAIL %d — 그림 %s_*.png' % (len(bad), SHOT))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.exit(asyncio.run(main()))
