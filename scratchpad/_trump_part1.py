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
import _trump_fig as tf

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

CAPTION = {
    'SWAP': ('상호관세가 위헌이 된 뒤에도 세율은 남았다', tf.FIG_SWAP,
             '근거가 바뀐 걸음 넷입니다. 대법원이 2026년 2월 21일 6대 3으로 상호관세를 위헌으로 '
             '판단했지만 소급 취소는 판단하지 않고 하급심으로 돌려보냈고, 백악관은 판결 직후 '
             '무역법 122조로 갈아타 10%를 하루 만에 15%로 올렸습니다. 122조는 150일 한도라 '
             '7월 24일에 끝날 조항이었습니다. 점선 상자는 저자가 다음 카드로 지목했을 뿐 아직 '
             '발동되지 않은 관세법 338조입니다. 저자가 든 Plan B 다섯 장 가운데 실제로 근거가 '
             '바뀐 걸음만 그렸습니다 — 안 쓰인 232조·301조·201조는 그리지 않았습니다.'),
    'DELAY': ('시한은 다섯 번 박혔고 다섯 번 미뤄졌다', tf.FIG_DELAY,
              '다섯이라는 수는 원문이 센 것이 아니라 원문에 박힌 날짜를 이 글이 센 것입니다. '
              '2026년 3월 27일 글은 공격 시간이 48시간에서 5일이 되었다가 다시 열흘로 연장됐다고 '
              '적었고, 여기에 4월 8일 2주 휴전과 5월 18일 공격 보류를 이어 다섯으로 세었습니다. '
              '오른쪽 칸이 빈 두 줄은 그때 무엇을 받았는지가 원문에 안 적힌 자리입니다. '
              '유조선 10척은 파키스탄 선적 여덟 척을 포함한 수입니다.'),
    'BILL': ('같은 청구서인데 조건이 셋 다 다르다', tf.FIG_BILL,
             '2025년 10월부터 11월 사이에 나온 세 나라 조건입니다. 총액은 한국이 스위스의 '
             '2.5배이지만, 이익을 어떻게 나누는지와 거절하면 어떻게 되는지가 적힌 것은 일본 '
             '조건뿐입니다. 「이익 배분 조항 없음」은 그 조항이 유리하다는 뜻이 아니라 그 '
             '팩트시트에 안 나온다는 뜻입니다. 한국도 일본과 비슷할 것이라는 저자의 추정이 '
             '있으나 근거를 대지 않았으므로 그리지 않았습니다.'),
}

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
