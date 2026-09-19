# -*- coding: utf-8 -*-
"""어텐션 애니메이션 — 스텝 일곱을 실제로 눌러 보고 배치를 잰다.

눈으로 보고 「안 겹친다」고 보고하지 않는다(CLAUDE.md). 스텝마다 화면을 찍고 판 SVG 를
check_fig 에 먹인다. 모바일 폭에서 가로로 넘치는지도 같은 자리에서 본다.
"""
import io, os, sys
sys.path.insert(0, 'scratchpad')
import check_fig
from playwright.sync_api import sync_playwright

PAGE = os.path.abspath(os.path.join('대시보드', '애니메이션 — 어텐션.html'))
OUT = os.path.join('scratchpad', 'anim_shots')
N_STEPS = 7


def main():
    os.makedirs(OUT, exist_ok=True)
    fails = []
    url = 'file:///' + PAGE.replace(os.sep, '/')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1100, 'height': 780})
        pg.goto(url)
        pg.evaluate("document.getElementById('btn-pause').click()")
        pg.evaluate("document.getElementById('btn-reset').click()")
        for i in range(N_STEPS):
            if i:
                pg.evaluate("document.getElementById('btn-next').click()")
            pg.wait_for_timeout(3600 if i == 3 else 700)
            pg.screenshot(path=os.path.join(OUT, 'step%d.png' % i))
            shown = pg.eval_on_selector_all(
                '.stepdesc',
                'els=>els.filter(e=>getComputedStyle(e).display!=="none").length')
            bars = pg.eval_on_selector_all(
                '.bar', 'els=>els.filter(x=>+x.getAttribute("height")>0).length')
            step = pg.get_attribute('#stage', 'data-step')
            print('step%d  설명줄 %d · 선 막대 %d · data-step %s' % (i, shown, bars, step))
            if shown != 1:
                fails.append('스텝 %d: 보이는 설명 줄이 %d개다' % (i, shown))
            if step != str(i):
                fails.append('스텝 %d: data-step 이 %s 다' % (i, step))
        over = pg.evaluate('document.documentElement.scrollWidth - '
                           'document.documentElement.clientWidth')
        if over > 0:
            fails.append('폭 1100: 가로로 %dpx 넘친다' % over)
        pg.set_viewport_size({'width': 360, 'height': 780})
        pg.wait_for_timeout(400)
        over_m = pg.evaluate('document.documentElement.scrollWidth - '
                             'document.documentElement.clientWidth')
        pg.screenshot(path=os.path.join(OUT, 'mobile.png'))
        if over_m > 0:
            fails.append('폭 360: 가로로 %dpx 넘친다' % over_m)
        print('가로 넘침 — 1100: %d · 360: %d' % (over, over_m))
        b.close()
    page = io.open(PAGE, encoding='utf-8').read()
    svg = page[page.find('<svg'):page.find('</svg>') + 6]
    for h in (check_fig.hits(svg) or []):
        fails.append('배치: ' + h)
    for f in fails:
        print('FAIL', f)
    print('요약: 스텝 %d개 · 화면 2벌 / FAIL %d' % (N_STEPS, len(fails)))
    return len(fails)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.exit(1 if main() else 0)
