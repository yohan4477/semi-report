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



def clipboard():
    """윈도 클립보드를 읽는다. 표준 라이브러리로만 — tkinter 가 들고 있다."""
    import tkinter
    r = tkinter.Tk()
    r.withdraw()
    try:
        return r.clipboard_get()
    finally:
        r.destroy()


def copy_via_button(pg):
    """답 밑의 「복사」 버튼을 눌러 마크다운 그대로 가져온다.

    화면 글자를 긁으면(inner_text) 표가 줄바꿈으로 뭉개지고 제목 층위가 사라진다.
    버튼이 넣어 주는 것은 마크다운이라 표와 목록이 그대로 남는다.
    """
    for sel in ('button[aria-label*="복사"]', 'button[data-test-id="copy-button"]',
                'copy-button button', 'button[aria-label*="Copy"]'):
        try:
            btn = pg.locator(sel).last
            if btn.count() and btn.is_visible():
                btn.click()
                pg.wait_for_timeout(900)
                t = clipboard()
                if t and len(t) > 80:
                    return t
        except Exception:
            continue
    return None


MODEL = '3.1 Pro'        # 판단이 섞이는 물음이라 고급 추론 쪽으로. 「확장된 사고 모델」은
                          # 골라도 단추 라벨이 안 바뀌어 실제로 걸렸는지 확인할 길이 없었다


def pick_model(pg, want=MODEL):
    """새 대화마다 모델을 고르고 **바뀌었는지 라벨로 확인한다**.

    안 고르면 기본값(Flash)으로 답한다. 고른 뒤 단추 글자가 안 바뀌면 안 걸린 것이다 —
    2026-08-31 에 「확장된 사고 모델」을 골랐더니 클릭은 되는데 라벨이 그대로였고, 답도
    Flash 라고 말했다. 확인되는 것만 쓴다."""
    btn = pg.locator('button:has-text("Flash"), button:has-text("Pro")').first
    if not btn.count():
        return None
    before = (btn.inner_text() or '').strip()
    btn.click()
    pg.wait_for_timeout(1200)
    items = pg.locator('[role="menuitemradio"], [role="menuitem"], button[role="option"]')
    for i in range(items.count()):
        if want in (items.nth(i).inner_text() or ''):
            items.nth(i).click()
            pg.wait_for_timeout(2000)
            after = (pg.locator('button:has-text("Flash"), button:has-text("Pro")')
                     .first.inner_text() or '').strip()
            key = want.split()[-1]          # 「3.1 Pro」 -> 「Pro」
            return after if key in after else None
    pg.keyboard.press('Escape')
    return None


def ask(prompt, dest, timeout=600):
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
        pg = b.contexts[0].new_page()
        pg.goto('https://gemini.google.com/app', wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(5000)
        got = pick_model(pg)
        print('모델:', got or '기본값 그대로', file=OUT)
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
        text = copy_via_button(pg) or last
        io.open(dest, 'w', encoding='utf-8').write(text)
        print('받은 글자 %d · %s' % (len(text), dest), file=OUT)
        pg.close()


if __name__ == '__main__':
    ask(io.open(sys.argv[1], encoding='utf-8').read(), sys.argv[2])
