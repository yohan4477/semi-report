# -*- coding: utf-8 -*-
"""Gemini 에 각도 하나를 물어 답을 파일로 받는다. CDP 크롬에 붙어 쓴다.

크롬 확장(claude-in-chrome)으로는 gemini.google.com 을 못 읽는다 — 스트리밍 연결을
계속 열어 두는 페이지라 확장이 기다리는 document_idle 이 안 온다. 2026-08-31 에 대기를
3·6·8·10초로 늘리고 탭을 새로 만들어도 같았다. playwright 로 CDP(9222)에 붙으면 된다.

받은 답은 재료가 아니라 프레임 후보다 — insights/frames/ 에 두고 check_frame 으로
원문과 대조한 뒤에 카드로 옮긴다.

  python gem_ask.py <프롬프트파일> <저장경로>

새 대화로 물어야 각도가 안 섞인다 — 매번 /app 을 새로 열고 **임시 채팅**을 켠다.
새 대화만으로는 저장된 정보(기억)가 따라와 앞 회차 틀이 다음 답에 섞인다.
"""
import io
import re
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
    key = want.split()[-1]              # 「3.1 Pro」 -> 「Pro」
    before = (btn.inner_text() or '').strip()
    if key in before:
        # 이미 걸려 있다. 메뉴를 안 연다. 이름은 고른 이름으로 적는다 —
        # 버튼 라벨은 「Gemini Pro」처럼 판 이름을 흘려 어느 판인지 안 남는다
        return 'Gemini ' + want
    btn.click()
    pg.wait_for_timeout(1200)
    items = pg.locator('[role="menuitemradio"], [role="menuitem"], button[role="option"]')
    for i in range(items.count()):
        it = items.nth(i)
        # 임시 채팅에서는 못 고르는 항목이 회색으로 남아 있다. 눌러도 안 걸리고 30초를
        # 기다리다 죽는다 — 막힌 것은 건너뛴다
        if (it.get_attribute('aria-disabled') or '') == 'true':
            continue
        if want in (it.inner_text() or ''):
            it.click()
            pg.wait_for_timeout(2000)
            after = ' '.join((pg.locator('button:has-text("Flash"), button:has-text("Pro")')
                              .first.inner_text() or '').split())
            # 라벨은 줄이 갈려 온다(Gemini / Pro). 그대로 적으면 머리말에
            # 「Gemini」만 남아 어느 모델이 썼는지 못 읽는다 — 고른 이름으로 적는다
            return ('Gemini ' + want) if key in after else None
    pg.keyboard.press('Escape')
    return None


def temp_chat(pg):
    """물을 때마다 「임시 채팅」을 켠다. 켜졌는지 화면 안내로 확인한다.

    새 대화를 열어도 저장된 정보(기억)는 그대로 따라온다 — 앞 회차에서 받은 틀이 다음
    회차 답에 섞이고, 그게 섞였는지 우리 쪽에서 알 길이 없다. 임시 채팅은 기억을 쓰지도
    남기지도 않는다. 못 켜면 그대로 진행하지 않는다 — 섞인 답은 대조로도 안 걸린다.
    """
    btn = pg.locator('button[aria-label*="임시 채팅"], button[aria-label*="Temporary"]').first
    assert btn.count(), '임시 채팅 단추를 못 찾았다'
    btn.click()
    pg.wait_for_timeout(3000)
    # 단추는 눌린 상태를 안 알린다(aria-pressed 없음) — 켜지면 뜨는 안내로 확인한다.
    # 「72시간 동안 저장됩니다」·「잠깐 들르신 건가요?」가 임시 채팅 화면의 글이다
    body = pg.locator('body').inner_text()
    on = any(t in body for t in ('72시간', '잠깐 들르신', 'Temporary chat', '72 hours'))
    assert on, '임시 채팅이 안 켜졌다 — 안내 문구가 없다'
    return True


def current_model(pg):
    """지금 걸려 있는 모델 이름. 모드 단추의 aria-label 이 말해 준다.

    「모드 선택 도구 열기, 현재 Gemini Flash-Lite 모드 사용 중」에서 가운데만 뽑는다.
    받은 글이 어느 모델 것인지는 프레임 머리말에 그대로 적어야 한다 — 카드에 그 이름이
    뜨고, 나중에 무엇을 다시 받을지 그것으로 고른다.
    """
    for sel in ('button[aria-label*="모드 선택"]', 'button[aria-label*="mode"]'):
        b = pg.locator(sel).first
        if not b.count():
            continue
        lab = b.get_attribute('aria-label') or ''
        m = re.search(r'현재\s+(.+?)\s+모드', lab)
        if m:
            return m.group(1).strip()
        t = (b.inner_text() or '').replace(chr(10), ' ').strip()
        if t:
            return t
    return '모델 미상'


def ask(prompt, dest, timeout=600, allow_lower=False):
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
        pg = b.contexts[0].new_page()
        pg.goto('https://gemini.google.com/app', wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(5000)
        temp_chat(pg)
        got = pick_model(pg)
        # 못 걸면 멈춘다. 조용히 기본값으로 받으면 어느 모델이 쓴 글인지 모른 채 프레임
        # 파일에 「3.1 Pro」라고 적힌다. 2026-08-31 에 한도가 차서 3.1 Pro·3.7 Flash 가
        # 회색이었고 여섯 편이 Flash-Lite 로 왔다.
        # allow_lower 를 켜면 낮은 모델로도 받는다 — 대신 실제로 걸린 이름을 돌려주고,
        # 그 이름이 프레임 머리말과 카드에 그대로 선다
        if not got:
            assert allow_lower, ('원하는 모델(%s)이 안 걸렸다. 메뉴에서 회색이면 한도가 '
                                 '찬 것이다 — 풀린 뒤에 다시 묻거나 allow_lower 로 낮은 '
                                 '모델을 받는다' % MODEL)
            got = current_model(pg)
        print('모델:', got, file=OUT)
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
        return got


if __name__ == '__main__':
    ask(io.open(sys.argv[1], encoding='utf-8').read(), sys.argv[2])
