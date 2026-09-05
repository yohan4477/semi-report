# -*- coding: utf-8 -*-
"""보고서 ⑧ — 금리·물가 총정리. 본문은 insights/reports/rate-2026-09-05.md 에서 읽는다.

CPO(_cpo_part1)·선단 패키징(_pkg_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고
여기서 HTML 로 바꾼다. 차례와 절 번호는 _rep_toc 가 붙인다 — 층마다 복사하지 않는다.

이 층만 다른 것 하나 — 재료가 SemiAnalysis 가 아니라 해설과 블로그다. 그래서 절마다
같은 사실을 놓고 갈리는 말을 함께 싣고, 마지막 표를 화자 배치로 세웠다.
"""
import io
import os
import re

import _rate_fig as rf
import _rep_toc as rt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'rate-2026-09-05.md')

HEAD_RATE = (
    '<div class="rep-head"><span class="rn">보고서 ⑧</span>'
    '<h2 id="rep-rate">금리·물가 총정리 — 연준이 내렸는데 왜 장기금리는 올랐고, 누가 그것을 '
    '다르게 읽나</h2>'
    '<p class="rm">바탕 <b>메르 24편 · 해설 17편 · 사슬 2건 · 쟁점 1건</b> · '
    '원문 기간 <b>2025-05 ~ 2026-09</b><br>'
    '이 층은 앞의 일곱 층과 재료 계보가 다릅니다. SemiAnalysis 가 아니라 블로그와 해설이 '
    '바탕이라 화자가 여럿이고 자주 어긋납니다. 그래서 절마다 같은 사실을 놓고 갈리는 말을 '
    '함께 실었습니다. 분량 제한 없이 썼습니다.</p></div>')

GROUPS = [('금리가 어떻게 움직이나', 1, 6),
          ('2026년 7~9월에 무슨 일이 있었나', 7, 12),
          ('누가 어디 서 있나', 13, 14)]

LEAD = ('이 층은 물음 하나를 세 묶음으로 따라갑니다 — 금리가 어떻게 움직이나, '
        '2026년 7~9월에 무슨 일이 있었나, 누가 어디 서 있나.')

CAPTION = {
    'SERIES': ('2026년 6월부터 9월까지 미국 국채금리', rf.FIG_SERIES,
               '선은 FRED 일별 종가이고, 동그라미는 원문이 짚은 날에 찍었습니다. 값이 아니라 날에 '
               '찍습니다 — 원문 값은 장중 고점일 때가 있어 종가 선에서 떠 버리기 때문입니다. '
               '세로 점선은 7월 29일 FOMC 와 8월 19일 바이백 발표입니다. 두 달 반 동안 30년물이 '
               '4.9%대에서 5.3%대로 올라섰습니다. 값이 갈리는 자리도 밝힙니다 — 엘곰이 화요일 '
               '5.34%라고 적은 날 FRED 종가는 5.28%이고, 맞추지 않고 둘 다 뒀습니다.'),
    'DIVERGE': ('연준이 내리기 시작한 뒤 장기금리는 거꾸로 갔다', rf.FIG_DIVERGE,
                '선은 FRED 일별입니다. 2024년 9월 18일 첫 인하부터 지금까지 기준금리는 1.7%포인트 '
                '내려왔는데 30년물은 1.2%포인트 올라갔습니다. 회계사 채널이 2026년 8월에 「1.75%포인트 '
                '인하하는 동안 10년물 약 1%포인트, 30년물 1.3%포인트 상승」이라고 적은 것과 같은 '
                '움직임입니다. 이 어긋남이 이 글 전체가 설명하려는 것이라 여는 자리에 둡니다.'),
    'INVERT': ('10년물에서 2년물을 뺀 값 — 0 아래가 역전이다', rf.FIG_INVERT,
               '메르가 독자에게 직접 열어 보라고 짚은 FRED 시리즈(T10Y2Y)를 그대로 그렸습니다. '
               '2022년 4월에 뒤집혀 2024년 9월 5일에 풀렸고, 가장 깊었던 자리가 2023년 7월 3일 '
               '-1.08%포인트입니다. 메르가 「40년 만의 107bp」라고 적은 그 값입니다. 메르는 역전이 '
               '풀리고 평균 열두 달쯤 뒤에 일이 생겼다고 했는데, 그 열두 달은 2025년 9월에 지났습니다.'),
    'ZOOM': ('재무부 바이백 발표 전후 30년물', rf.FIG_ZOOM,
             '앞의 넓은 그림에서는 안 보이는 사흘을 확대했습니다. 세로 점선이 8월 19일 발표이고 '
             '동그라미는 원문이 짚은 세 값입니다. 발표에 9bp 내렸다가 이튿날 되올라 그 주 안에 발표 '
             '이전을 넘어섰습니다. 미국주식 사관학교가 「하루 만에 되돌아왔다」고 쓴 것이 선에서 '
             '그대로 보입니다.'),
    'TIPS': ('유가가 올랐는데 튄 것은 기대인플레이션이 아니라 실질금리였다', rf.FIG_TIPS,
             '메르가 2026년 7월에 잰 값입니다. 물가연동국채로 30년물을 실질금리와 기대인플레이션으로 '
             '쪼개 보니 실질금리만 2.987%로 2008년 금융위기 이후 최고였고 기대인플레이션은 2.3%대에 '
             '머물렀습니다. 교과서대로라면 유가 충격은 오른쪽 막대에 얹혀야 합니다. 명목금리 총합은 '
             '원문에 없어 그리지 않았습니다.'),
    'GAUGE': ('잣대를 바꾸면 같은 물가가 낮아 보인다', rf.FIG_GAUGE,
              '메르의 사슬이 인과로 이어 놓은 네 걸음입니다. 번즈가 근원 CPI 를 만들고, 그린스펀의 '
              '증언이 위원회의 1.1%포인트 결론으로 이어지고, 그것이 명분이 되어 핵심 지표가 PCE 로 '
              '바뀌고, 워시가 절사평균을 선호합니다. 짙은 칸이 지금 자리입니다. 메르는 이 계보를 '
              '숫자 마사지라 불렀는데, 사슬은 잭슨홀 선언을 그 가설이 깨지는 자리로 함께 표시해 '
              '두었습니다(10절).'),
    'DISCOUNT': ('먼 미래일수록 같은 1%포인트가 크게 깎는다', rf.FIG_DISCOUNT,
                 '메르가 예금으로 푼 계산입니다. 금리가 4%에서 5%로 오르면 1년 뒤 1,000만원의 오늘 '
                 '값은 961만원에서 952만원으로 9만원 깎이는데, 10년 뒤 1,000만원은 676만원에서 '
                 '614만원으로 62만원 깎입니다. 이자에 이자가 붙기 때문입니다. 먼 이익을 약속하는 '
                 '기술주가 금리에 더 민감한 이유가 여기 있습니다. 막대 높이는 값에 비례합니다.'),
    'VIGILANTE': ('채권 자경단이 나타난 네 번 — 매번 정책이 물러섰다', rf.FIG_VIGILANTE,
                  '메르가 든 사례 넷입니다. 왼쪽이 방아쇠이고 오른쪽이 물러선 결과입니다. 사례 개수 '
                  '넷은 원문이 센 수입니다. 메르는 채권 자경단이 실체가 있는 집단이 아니라 위험을 '
                  '피하려고 집단으로 움직이는 현상이라고 못 박았고, 재정적자 확대와 물가 우려와 '
                  '중앙은행 독립성 훼손 셋이 겹칠 때 나타난다고 조건을 달았습니다.'),
    'BUYBACK': ('같은 바이백을 두 사람이 다르게 셌다', rf.FIG_BUYBACK,
                '2026년 8월 19일 재무부가 한 회 바이백 한도를 20억에서 40억 달러로 늘린 같은 조치를 '
                '두 화자가 다르게 셌습니다. 메르는 증액 대상이 두 구간이고 각각 분기에 네 번이니 '
                '분기 여덟 번으로 세고, 미국주식 사관학교는 구간별 월 한 번을 가정해 두 달에 네 번으로 '
                '셉니다. 그래서 나오는 숫자가 다릅니다. 미주사 본인이 이것이 자기 가정이라고 밝혀 '
                '두었고, 32조 달러 국채시장 앞에서는 어느 셈으로도 작다는 판단은 둘이 같습니다.'),
    'WHO': ('30년물이 19년 만의 고점을 찍은 한 달, 원인 진단이 넷으로 갈렸다', rf.FIG_WHO,
            '같은 값을 놓고 네 화자가 다른 원인을 듭니다. 상자 개수는 이 글이 그 물음에 답을 실은 '
            '화자 수이고 값은 없습니다. 넷은 서로를 지우지 않습니다. 그리고 원인 진단이 갈려도 '
            '처방은 오히려 모입니다 — 장기채를 지금 담지 말라는 데 메르와 미국주식 사관학교가 같은 '
            '자리에 섭니다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\b(?:[LT]\d|[a-z]\d)[^()]*)\)')


def _strip(s):
    """(라벨 L12) 와 (사슬-CPI b4) 를 걷고 마크다운 굵게를 <b> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
         '<caption>같은 물음에 화자마다 다르게 답한 것을 나란히 놓았습니다. 빈칸은 그 화자가 그 물음을 '
         '다루지 않은 자리입니다. 「언제 것 · 성격」은 그 말이 언제 나왔고 저자 주장인지 인용인지를 '
         '가릅니다.</caption>',
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
    return rt.toc_html('rate', LEAD, GROUPS, titles)


def report_rate(sec, p, fig):
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
