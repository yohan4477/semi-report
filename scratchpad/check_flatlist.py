# -*- coding: utf-8 -*-
"""첫 화면 규약을 실제 브라우저에서 확인한다 — 대시보드 스무 장.

dash_common.check_ui() 는 만들어진 글자를 본다. 여기서는 브라우저가 그린 화면을 본다:
목록이 보이는가, 태그를 누르면 줄이 걸러지는가, 본문 섹션이 접힌 채로 있는가,
줄이 가리키는 글 페이지가 실제로 있는가.

  py -3.13 scratchpad/check_flatlist.py

2026-09-08 에 check_twoscreen.py(타일 ↔ 카드 두 화면 검사)를 대신해 들어왔다. 화면이
하나가 됐으므로 두 화면을 재던 검사는 잴 것이 없다.
"""
import asyncio
import io
import os
import sys

from playwright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = os.path.join(ROOT, '대시보드')

# dash_common.render() 로 조립하는 장 전부. 워치·씨모어·Semi Doped 는 제 규약이 따로 있다.
PAGES = ['AI Engineer 대시보드.html', 'Epoch AI 대시보드.html', 'M&A 대시보드.html',
         '건강 대시보드.html', '기타 대시보드.html', '링크드인 흐름.html',
         '메르 대시보드.html', '메르 흐름.html', '모델 가이드.html',
         '미국주식 사관학교 대시보드.html', '부동산 대시보드.html', '산업시장 대시보드.html',
         '수도리무브 대시보드.html', '알고리즘 계보.html', '언더스탠딩 보고서 대시보드.html',
         '언더스탠딩 프리미엄 대시보드.html', '용어사전.html', '이선엽 시황 대시보드.html',
         '통합 보고서.html', '회계사 대시보드.html']


async def check(pg, name):
    bad = []
    path = os.path.join(DASH, name)
    if not os.path.exists(path):
        return ['파일이 없다']
    await pg.goto('file:///' + path.replace(os.sep, '/'))
    await pg.wait_for_timeout(300)
    if not await pg.eval_on_selector_all('.tagnav', 'e=>e.length'):
        bad.append('태그 줄이 없다')
    if await pg.eval_on_selector_all('.stile, .sec-pick', 'e=>e.length'):
        bad.append('섹션 타일이 남아 있다')
    rows = await pg.eval_on_selector_all('.rows .row:not([hidden])', 'e=>e.length')
    # 본문 섹션은 접혀 있어야 한다. 카드가 없는 장(흐름)은 고정 층이 유일한 본문이라 편다.
    shown = await pg.eval_on_selector_all(
        'section[id]:not([data-fixed])', 'e=>e.filter(s=>s.offsetHeight>0).length')
    if shown:
        bad.append('펴진 채로 서 있는 본문 섹션 %d개' % shown)
    if rows:
        # 태그 하나를 눌러 줄이 줄어드는지. **눈에 보이는 줄**로 센다 — hidden 속성만 보면
        # display:block 이 [hidden] 을 이겨 화면에는 그대로 서 있는 것을 놓친다(2026-09-08)
        seen = 'e=>e.filter(function(r){return r.offsetHeight>0}).length'
        shown = await pg.eval_on_selector_all('.rows .row', seen)
        tags = await pg.eval_on_selector_all('.tagnav button:not([hidden])', 'e=>e.length')
        # 태그가 「전체」와 갈래 하나뿐이면 눌러도 같은 목록이다 — 걸러짐을 잴 수 없다
        if tags > 2:
            # 목록 한가운데서 눌러도 되어야 한다 — 태그 줄이 스크롤을 따라오는지 같이 본다
            await pg.evaluate('window.scrollTo(0, 2000)')
            await pg.wait_for_timeout(120)
            h = await pg.evaluate('window.innerHeight')
            top = await pg.eval_on_selector('.tagbar, .tagnav', 'e=>e.getBoundingClientRect().top')
            if not (0 <= top < h):
                bad.append('스크롤을 내리면 태그 줄이 화면에서 사라진다(top=%d)' % top)
            await pg.click('.tagnav button:nth-child(2)')
            await pg.wait_for_timeout(700)
            got = await pg.eval_on_selector_all('.rows .row', seen)
            if got == 0 or got >= shown:
                bad.append('태그를 눌렀는데 화면의 줄이 안 걸러진다(%d → %d)' % (shown, got))
            first = await pg.eval_on_selector(
                '.rows .row:not([hidden])', 'e=>Math.round(e.getBoundingClientRect().top)')
            if not (-10 <= first < 420):
                bad.append('태그를 눌러도 그 목록 첫 줄로 안 데려간다(첫 줄 y=%d)' % first)
            await pg.click('.tagnav button:nth-child(1)')
        # 줄이 가리키는 글 페이지가 실제로 있는지 — 처음 다섯 줄만 본다
        hrefs = await pg.eval_on_selector_all(
            '.rows .row', 'e=>e.slice(0,5).map(a=>a.getAttribute("href"))')
        for h in hrefs:
            if h.startswith('#'):
                continue
            from urllib.parse import unquote
            if not os.path.exists(os.path.join(DASH, unquote(h).replace('/', os.sep))):
                bad.append('줄이 없는 글 페이지를 가리킨다: %s' % h)
    return bad


async def main():
    fail = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 430, 'height': 900})
        for name in PAGES:
            bad = await check(pg, name)
            fail += len(bad)
            print(('FAIL ' if bad else 'OK   ') + name + (' — ' + ' · '.join(bad) if bad else ''))
        await b.close()
    print('\n요약: 장 %d개 / FAIL %d' % (len(PAGES), fail))
    return 1 if fail else 0


sys.exit(asyncio.run(main()))
