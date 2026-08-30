# -*- coding: utf-8 -*-
"""Gemini 에 각도 하나를 물어 답을 파일로 받는다. CDP 크롬에 붙어 쓴다.

크롬 확장(claude-in-chrome)으로는 gemini.google.com 을 못 읽는다 — 스트리밍 연결을
계속 열어 두는 페이지라 확장이 기다리는 document_idle 이 안 온다. 2026-08-31 에 대기를
3·6·8·10초로 늘리고 탭을 새로 만들어도 같았다. playwright 로 CDP(9222)에 붙으면 된다.

받은 답은 재료가 아니라 프레임 후보다 — insights/frames/ 에 두고 check_frame 으로
원문과 대조한 뒤에 카드로 옮긴다.

  python gem_ask.py <프롬프트파일> <저장경로>

새 대화로 물어야 각도가 안 섞인다 — 매번 /app 을 새로 연다.
"""
import io
import sys
import time
from playwright.sync_api import sync_playwright

OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8')


def ask(prompt, dest, timeout=300):
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
        pg = b.contexts[0].new_page()
        pg.goto('https://gemini.google.com/app', wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(5000)
        box = pg.locator('div[contenteditable="true"]').first
        box.click()
        # 줄바꿈이 전송으로 잡히지 않게 한 덩어리로 넣는다
        pg.evaluate("""(t) => {
            const el = document.querySelector('div[contenteditable="true"]');
            el.focus();
            document.execCommand('insertText', false, t);
        }""", prompt)
        pg.wait_for_timeout(1200)
        pg.keyboard.press('Enter')
        # 답이 멈출 때까지 — 길이가 여덟 번 연속 그대로면 끝난 것으로 본다
        last, still, t0 = '', 0, time.time()
        while time.time() - t0 < timeout:
            pg.wait_for_timeout(2500)
            try:
                cur = pg.locator('model-response').last.inner_text()
            except Exception:
                cur = ''
            if cur and cur == last:
                still += 1
                if still >= 8:
                    break
            else:
                still = 0
            last = cur
        io.open(dest, 'w', encoding='utf-8').write(last)
        print('받은 글자 %d · %s' % (len(last), dest), file=OUT)
        pg.close()


if __name__ == '__main__':
    ask(io.open(sys.argv[1], encoding='utf-8').read(), sys.argv[2])
