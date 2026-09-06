# -*- coding: utf-8 -*-
"""보고서 ⑨ — 트럼프 총정리. 본문은 insights/reports/trump-2026-09-06.md 에서 읽는다.

금리·물가 층(_rate_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고 여기서 HTML 로
바꾼다. 차례와 절 번호는 _rep_toc 가 붙인다 — 층마다 복사하지 않는다.

이 층만 다른 것 하나 — 재료가 한 사람의 블로그 마흔일곱 편뿐이다. 주체를 축으로 삼으면
절이 관세·연준·중동·자원으로 흩어져 나열이 되므로, 수(手)의 순서를 축으로 잡았다.
그래서 값마다 공표인지 저자 추정인지를 본문에서 가려 적었다.
"""
import io
import os
import re

import _rep_toc as rt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'trump-2026-09-06.md')

HEAD_TRUMP = (
    '<div class="rep-head"><span class="rn">보고서 ⑨</span>'
    '<h2 id="rep-trump">트럼프 총정리 — 무엇을 걸어 무엇을 받아냈고, 한국은 그 순서 어디에서 '
    '값을 치렀나</h2>'
    '<p class="rm">바탕 <b>메르 47편</b> · 원문 기간 <b>2025-04 ~ 2026-09</b><br>'
    '재료가 한 사람의 블로그입니다. 다른 매체나 1차 문서로 교차 확인하지 않았으므로, 이 층의 값은 '
    '「원문에 그렇게 적혀 있다」까지만 보증합니다. 저자가 스스로 추정이라고 밝힌 값은 본문에서 '
    '추정이라고 적었습니다. 분량 제한 없이 썼습니다.</p></div>')

GROUPS = [('수를 어떻게 읽나', 1, 2),
          ('위협에서 청구까지', 3, 9),
          ('안에서 벌어진 일', 10, 11),
          ('한국과 남은 물음', 12, 14)]

LEAD = ('이 층은 수(手)의 순서를 축으로 따라갑니다 — 위협하고, 날짜를 박고, 미루고, '
        '거래하고, 요금을 붙입니다. 그 순서 어디에서 한국이 값을 냈는지가 물음입니다.')

# 도해는 아직 없다. 붙일 때 _trump_fig 를 만들고 여기에 캡션을 적는다 —
# gen_report_dashboard 의 REPORT_FIGS 가 이 사전을 걷어 check_fig 로 넘긴다
CAPTION = {}

_CITE = re.compile(r'\s*\(([^()]*?\b(?:[LT]\d|[a-z]\d)[^()]*)\)')


def _strip(s):
    """(라벨 T12) 를 걷고 마크다운 굵게를 <b> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
         '<thead><tr>' + ''.join('<th>%s</th>' % _strip(c) for c in head) + '</tr></thead><tbody>']
    for r in body:
        h.append('<tr>' + ''.join('<td>%s</td>' % _strip(c) for c in r) + '</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def load():
    txt = io.open(SRC, encoding='utf-8').read()
    if txt.startswith('---'):
        txt = txt.split('---', 2)[2]
    out, para, tbl = [], [], []

    def flush():
        if para:
            out.append(('p', ' '.join(para)))
            para.clear()
        if tbl:
            out.append(('table', list(tbl)))
            tbl.clear()

    for line in txt.split('\n'):
        s = line.rstrip()
        if s.startswith('## '):
            flush()
            out.append(('sec', re.sub(r'^\d+\.\s*', '', s[3:]).strip()))
        elif s.startswith('[[fig:'):
            flush()
            out.append(('fig', s[6:].rstrip(']').strip()))
        elif s.startswith('|'):
            if para:
                flush()
            tbl.append(s)
        elif not s:
            flush()
        elif s.startswith('#'):
            continue
        else:
            para.append(s.strip())
    flush()
    return out


def toc_html(titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다(2026-09-05)."""
    return rt.toc_html('trump', LEAD, GROUPS, titles)


def report_trump(sec, p, fig):
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig') and not toc_done:
            p(toc_html(titles))
            toc_done = True
        if k == 'sec':
            sec(rt.sec_title(titles.index(v) + 1, v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'table':
            p(_table(v))
    return titles
