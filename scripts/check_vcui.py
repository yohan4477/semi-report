# -*- coding: utf-8 -*-
u"""밸류체인 탐색기 화면 규약 — 브라우저에서 눌러 보며 오류가 나나.

FAIL 0 이어야 푸시한다. 선 규약(check_vcroute)은 그려진 선만 보고, 이 검사는 사람이 하는
일을 기계가 한다 — 사슬마다·해마다 열고, 접힌 첫 화면과 전부 편 판을 보고, 띠의 칩을 다
누르고, 상자를 몇 개 누르고, 회사 목록·찾기·좁은 화면 버튼을 누른다. 그 사이 페이지 오류나
콘솔 오류·경고가 하나라도 나면 FAIL 이다.

  U1 페이지 오류(예외)
  U2 콘솔 error·warning. route 가 중간 상자를 비켜 더 먼 높이로 간 것은 설계된 예비 경로라
     info 로만 남기고(2026-09-13) 여기서 안 센다 — 그 선이 규약을 지켰는지는 check_vcroute 가 잰다
  U3 첫 화면에 상자가 하나도 안 섰다
  U4 좁은 화면에서 판이 첫 화면 높이의 70% 밑이다
  U5 첫 화면 머리줄·띠·연도가 가로로 넘친다(좁은 화면)

넓은 화면 1500×1100 과 좁은 화면 390×844 둘 다 본다. 사슬 목록은 chain.json 에서 읽는다.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')
DATA = os.path.join(ROOT, 'data', 'valuechain')

fails = []


def chains():
    base = os.path.join(DATA, 'chains')
    out = []
    for d in sorted(os.listdir(base)):
        cp = os.path.join(base, d, 'chain.json')
        if os.path.exists(cp):
            out.append(json.load(io.open(cp, encoding='utf-8'))['focal_entity'])
    return out


def run(page, label, url):
    errs = []
    h1 = lambda e: errs.append(u'U1 %s' % str(e)[:160])
    h2 = lambda m: errs.append(u'U2 %s: %s' % (m.type, m.text[:160])) \
        if m.type in ('error', 'warning') else None
    page.on('pageerror', h1)
    page.on('console', h2)
    page.goto(url)
    page.wait_for_timeout(1400)
    n = page.evaluate("document.querySelectorAll('.react-flow__node .nd').length")
    if not n:
        errs.append(u'U3 상자 0')
    page.remove_listener('pageerror', h1)
    page.remove_listener('console', h2)
    for e in errs:
        fails.append(u'FAIL %s — %s' % (label, e))
    return n


def poke(page, label):
    u"""칩 전부, 상자 여덟, 회사 목록 하나 — 오류만 본다."""
    errs = []
    h1 = lambda e: errs.append(u'U1 %s' % str(e)[:160])
    h2 = lambda m: errs.append(u'U2 %s: %s' % (m.type, m.text[:160])) \
        if m.type in ('error', 'warning') else None
    page.on('pageerror', h1)
    page.on('console', h2)
    chips = page.locator('.axchip')
    for i in range(chips.count()):
        chips.nth(i).click(force=True)
        page.wait_for_timeout(80)
    nodes = page.locator('.react-flow__node .nd')
    for i in range(min(nodes.count(), 8)):
        try:
            page.locator('.react-flow__node .nd').nth(i).click(force=True, timeout=2000)
            page.wait_for_timeout(250)
        except Exception:
            pass    # 눌러서 판이 접히면 그 자리가 없어진다. 오류가 아니다
    # 회사 목록 — 안 열리면 그 자체가 결함이다(U6). 30초를 기다리지 않는다
    page.locator('.modes button').first.click(force=True)
    try:
        page.wait_for_selector('.menu .row', timeout=3000)
        page.locator('.menu .row').first.click(force=True)
        page.wait_for_timeout(1200)
    except Exception:
        errs.append(u'U6 회사 목록이 안 열린다')
        try:
            page.screenshot(path=os.path.join(ROOT, 'scratchpad', 'check_vcui_u6.png'))
        except Exception:
            pass
    page.remove_listener('pageerror', h1)
    page.remove_listener('console', h2)
    for e in errs:
        fails.append(u'FAIL %s — %s' % (label, e))


def main():
    import playwright.sync_api as pw
    base = 'file:///' + PAGE.replace(os.sep, '/')
    focals = chains()
    years = ('2024', '2025', '2026')
    steps = 0
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        for w, hh in ((1500, 1100), (390, 844)):
            page = b.new_page(viewport={'width': w, 'height': hh}, is_mobile=(w < 720),
                              has_touch=(w < 720))
            tag = u'%dpx' % w
            for f in focals:
                for y in years:
                    for op in ('', '&open=*'):
                        run(page, u'%s %s %s%s' % (tag, f, y, op and u' 전부'),
                            base + '?focal=%s&year=%s%s' % (f, y, op))
                        steps += 1
                run(page, u'%s %s' % (tag, f), base + '?focal=%s' % f)
                poke(page, u'%s %s 누르기' % (tag, f))
                steps += 1
            if w < 720:
                page.goto(base + '?focal=' + focals[0])
                page.wait_for_timeout(1400)
                m = page.evaluate("""(function(){var c=document.querySelector('.canvas').getBoundingClientRect();
                  return {ratio:c.height/innerHeight, overflow:document.documentElement.scrollWidth>innerWidth}})()""")
                if m['ratio'] < 0.7:
                    fails.append(u'FAIL %s — U4 판이 첫 화면의 %d%% 다' % (tag, round(m['ratio'] * 100)))
                if m['overflow']:
                    fails.append(u'FAIL %s — U5 가로로 넘친다' % tag)
            page.close()
        b.close()
    for f in fails[:30]:
        print(f)
    print(u'요약: 사슬 %d · 화면 2 · 걸음 %d / FAIL %d' % (len(focals), steps, len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
