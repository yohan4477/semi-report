# -*- coding: utf-8 -*-
"""Semi Doped 회차 전문을 긁어 둔다. CDP 크롬에 붙어 쓴다.

  py -3.13 scripts/semidoped_clip.py <회차 링크> <저장 경로>

우리가 옮긴 요약본은 사실을 골라 담은 중간물이라, 다른 모델에게 「이 회차를 설명해
달라」고 할 때 주면 그 선택까지 같이 넘어간다. 전문을 주면 고르는 일을 그쪽이 한다.

이 매체는 전편을 무료로 푼다 — 유료 원문을 밖으로 안 보낸다는 규칙에 안 걸린다.
"""
import io
import os
import re
import sys

from playwright.sync_api import sync_playwright

OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8')


def trim(text):
    """재생 막대·다음 글 목록 같은 페이지 껍데기를 뗀다. 본문만 넘긴다."""
    lines = text.split(chr(10))
    start = 0
    for i, ln in enumerate(lines[:40]):
        if re.match(r'^\s*(SEMI DOPED|🎙)', ln) or 'Open in app' in ln:
            start = i + 1
    for i, ln in enumerate(lines):
        if ln.strip() in ('Recent Posts', 'Discussion about this episode'):
            lines = lines[:i]
            break
    return chr(10).join(lines[start:]).strip()


def clip(url, dest):
    with sync_playwright() as pw:
        b = pw.chromium.connect_over_cdp('http://127.0.0.1:9222')
        pg = b.contexts[0].new_page()
        pg.goto(url, wait_until='domcontentloaded', timeout=60000)
        pg.wait_for_timeout(4000)
        for sel in ('article', 'div.available-content', 'main', 'body'):
            loc = pg.locator(sel)
            if loc.count():
                text = loc.first.inner_text()
                if len(text) > 2000:
                    break
        else:
            text = pg.locator('body').inner_text()
        title = (pg.title() or '').strip()
        pg.close()
    text = trim(text)
    head = '---\nsource: %s\ntitle: %s\nkind: transcript\n---\n\n' % (url, title)
    io.open(dest, 'w', encoding='utf-8').write(head + text.strip() + '\n')
    print('전문 %d자 -> %s' % (len(text), dest), file=OUT)
    return len(text)


if __name__ == '__main__':
    clip(sys.argv[1], sys.argv[2])
