# -*- coding: utf-8 -*-
"""생성기가 없는 대시보드에 표준 카드를 한 장 끼워 넣는다.

부동산·금융·미국주식 사관학교는 생성기의 CARDS 목록에 카드를 추가하고 페이지를
통째로 다시 만든다. 그 경로가 있는 대시보드에는 이 스크립트를 쓰지 않는다.

AI · 인프라 · 에너지(언더스탠딩 대시보드.html)만 예외다. 옛 형식 카드 26장이
생성기 없이 쌓여 있어 통째로 다시 만들 수 없고, 소급 변환도 아직 안 한다.
그래서 새 카드만 표준 형식으로 이 페이지에 끼워 넣는다 — 한동안 두 형식이 섞인다.

쓰는 법: 카드 dict를 담은 파이썬 파일을 만들고
    python scripts/add_card.py <카드파일.py> --section sec-ai
카드 dict의 필수·선택 키는 scripts/card_lib.py 머리말에 적혀 있다.
"""
from __future__ import annotations

import argparse
import io
import re
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import card_lib  # noqa: E402

PAGE = ROOT / '대시보드' / '언더스탠딩 대시보드.html'
SCOPE_LABEL = {'kr': '국내', 'intl': '해외'}


def ensure_css(html: str) -> str:
    """표준 카드가 쓰는 규칙(uc-gain·clash·표·접기)이 없으면 한 번만 넣는다."""
    if '.uc-gain{' in html:
        return html
    end = html.find('</style>')
    if end < 0:
        raise SystemExit('style 블록을 못 찾았다')
    print('  · 표준 카드 CSS를 이 페이지에 처음 넣는다')
    return html[:end] + card_lib.EXTRA_CSS + html[end + len('</style>'):]


def section_span(html: str, sec_id: str) -> tuple:
    m = re.search(r'<section id="%s"[^>]*>' % re.escape(sec_id), html)
    if not m:
        have = re.findall(r'<section id="([^"]+)"', html)
        raise SystemExit('섹션 %s 이 없다. 있는 섹션: %s' % (sec_id, ', '.join(have)))
    end = html.find('</section>', m.end())
    return m.end(), end


def insert(html: str, sec_id: str, card_html: str) -> str:
    """섹션 머리 바로 뒤에 넣는다 — 섹션 안은 최신 편이 위다."""
    start, end = section_span(html, sec_id)
    body = html[start:end]
    head = re.match(r'\s*<div class="sec-head">.*?</div>', body, re.S)
    at = start + (head.end() if head else 0)
    return html[:at] + '\n' + card_html + html[at:]


def recount(html: str) -> str:
    """카드를 센 결과로 머리글·섹션 목록·범위 탭 숫자를 다시 쓴다."""
    cards = re.findall(r'<div class="ucard[^"]*"([^>]*)>', html)
    total = len(cards)
    scopes = {'kr': 0, 'intl': 0}
    for attrs in cards:
        m = re.search(r'data-scope="(\w+)"', attrs)
        if m and m.group(1) in scopes:
            scopes[m.group(1)] += 1

    # 머리글: 수록 <b>26편</b>(국내 11·해외 15)
    def head_repl(m):
        tail = ''
        if scopes['kr'] or scopes['intl']:
            tail = '(국내 %d·해외 %d)' % (scopes['kr'], scopes['intl'])
        return '수록 <b>%d편</b>%s' % (total, tail)

    html = re.sub(r'수록 <b>\d+편</b>(?:\([^)]*\))?', head_repl, html, count=1)

    # 섹션별 개수
    for sec_id in re.findall(r'<section id="([^"]+)"', html):
        start, end = section_span(html, sec_id)
        n = html.count('<div class="ucard', start, end)
        html = re.sub(
            r'(<button data-sec="%s">[^<]*<span class="cnt">)\d+(</span>)' % re.escape(sec_id),
            lambda m: m.group(1) + str(n) + m.group(2), html)

    # 전체 보기 / 범위 탭
    html = re.sub(r'(<button data-sec="">전체 보기<span class="cnt">)\d+(</span>)',
                  lambda m: m.group(1) + str(total) + m.group(2), html)
    for key in ('kr', 'intl'):
        html = re.sub(r'(data-pick="%s"[^>]*>[^<]*<span class="cnt">)\d+(</span>)' % key,
                      lambda m, k=key: m.group(1) + str(scopes[k]) + m.group(2), html)
    html = re.sub(r'(data-pick="all"[^>]*>[^<]*<span class="cnt">)\d+(</span>)',
                  lambda m: m.group(1) + str(total) + m.group(2), html)
    return html, total, scopes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('card_file', help='CARD dict를 담은 파이썬 파일')
    ap.add_argument('--section', required=True, help='넣을 섹션 id (예: sec-ai)')
    ap.add_argument('--page', default=str(PAGE))
    args = ap.parse_args()

    card = runpy.run_path(args.card_file).get('CARD')
    if not isinstance(card, dict):
        raise SystemExit('%s 안에 CARD dict가 없다' % args.card_file)
    missing = [k for k in ('topic', 'title', 'gain', 'meta', 'oneliner',
                           'points', 'stats', 'quote', 'clash', 'note', 'links')
               if not card.get(k)]
    if missing:
        raise SystemExit('표준 카드에 빠진 키: %s (scripts/card_lib.py 머리말 참조)' % ', '.join(missing))

    page = Path(args.page)
    html = page.read_text(encoding='utf-8')
    anchor = card_lib.slug(card['title'])
    if 'id="%s"' % anchor in html:
        raise SystemExit('같은 제목의 카드가 이미 있다: %s' % anchor)

    html = ensure_css(html)
    html = insert(html, args.section, card_lib.card_html(card))
    html, total, scopes = recount(html)
    page.write_text(html, encoding='utf-8')
    print('  · %s 에 넣었다 (#%s)' % (args.section, anchor))
    print('OK: 수록 %d편 (국내 %d·해외 %d) -> %s' % (total, scopes['kr'], scopes['intl'], page))
    print('\n다음: 리포트 갱신(data/rollup_notes*.json) → scripts/update_card_ledger.py → scripts/gen_site.py')


if __name__ == '__main__':
    main()
