# -*- coding: utf-8 -*-
"""미주사 09-18~09-27 편 도해 열 장 (회색만, 판 위는 이름과 값과 번호, 캡션은 번호 풀이).

  0918 FIG_BANK      예금·대출 고리와 그 바깥에 서는 세 회사
  0920 FIG_CONNECT   전력망과 만나는 접점이 몇 곳인가 (초대형 한 곳 대 모듈 수십 곳)
       FIG_COVER     이튼과 버티브가 강한 자리 (UPS가 겹친다)
  0921 FIG_FIVE      현금 문턱 위에 선 다섯 질문과 원문이 든 사례
  0923 FIG_DIESEL    경유 재고가 줄어드는 연쇄와 여유 없는 세 곳
       FIG_TOLL      정유사 열과 파이프라인 열
  0925 FIG_PAYMENT   같은 대출, 금리별 월 원리금
       FIG_BUILDERS  세 건설사를 같은 꼴로 견준다
  0927 FIG_KR_NOW    2023년과 2026년의 한국 사정
       FIG_KR_DELINQ 평균 연체율과 취약 차주 연체율

규칙(yohan-figure):
  - 원문에 없는 값은 안 그린다. FIG_PAYMENT 막대 높이는 원문의 월 원리금 셋(1,686·2,147·2,661달러)에
    비례한다. FIG_KR_NOW 의 성장률 막대는 1.4%와 3.3%, FIG_KR_DELINQ 막대는 연체율 네 개에 비례한다.
    그 밖의 도형 개수는 값을 뜻하지 않게 했다(FIG_CONNECT 의 작은 상자 셋은 「수십 곳」을 줄임표로 끊는다).
  - FIG_COVER 는 원문이 두 회사의 위치를 「위쪽에서 시작」「랙 바로 옆」으로만 말하므로 장비 사이 순서를
    그리지 않고 세 칸(이튼만·겹침·버티브만)으로 둔다.
  - 판 위는 이름과 값과 번호뿐이고 판단은 본문이 한다. 붓은 _figs_0825 의 t-* 클래스를 쓰고
    상자 색은 인라인 회색 두 가지(옅은 채움·짙은 채움)만 쓴다.
"""

BOX = 'fill:rgba(127,127,127,.07);stroke:var(--line);stroke-width:1.2'
STRONG = 'fill:rgba(127,127,127,.22);stroke:var(--ink-3);stroke-width:1.4'
BAR = 'fill:rgba(127,127,127,.30);stroke:var(--ink-3);stroke-width:1.2'
LINE = 'stroke:var(--ink-3);stroke-width:1.5;fill:none'


def _svg(w, h, label, body):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>'
            % (w, h, label, ''.join(body)))


def _t(x, y, s, cls='t-sub', anchor='middle'):
    return '<text x="%d" y="%d" class="%s" text-anchor="%s">%s</text>' % (x, y, cls, anchor, s)


def _r(x, y, w, h, style=BOX, rx=8):
    return '<rect x="%d" y="%d" width="%d" height="%d" rx="%d" style="%s"/>' % (x, y, w, h, rx, style)


def _l(x1, y1, x2, y2):
    return '<line x1="%d" y1="%d" x2="%d" y2="%d" style="%s"/>' % (x1, y1, x2, y2, LINE)


def _a(x1, y1, x2, y2):
    return '<line class="flow" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x1, y1, x2, y2)


# ── 0918 ① 예금·대출 고리, 그 바깥 ───────────────────────────────────────
_LOOP = [('연준 인상', '25bp'), ('예금금리 상승', 'deposit beta'), ('대출 수요', '둔화'),
         ('차주 이자부담', '증가'), ('연체·대손', '비용 상승')]
_OUT = [('①', '스테이트 스트리트', 'STT · 수탁은행'),
        ('②', '골드만삭스', 'GS · 거래와 기업금융'),
        ('③', '블랙록', 'BLK · 자산운용')]


def fig_bank():
    h = [_t(24, 22, '예금을 받아 대출하는 고리와, 그 바깥에 서는 세 회사', 't-head', 'start')]
    for i, (a, b) in enumerate(_LOOP):
        x = 23 + i * 110
        h.append(_r(x, 40, 94, 54))
        h.append(_t(x + 47, 64, a, 't-step'))
        h.append(_t(x + 47, 82, b, 't-sub'))
        if i < len(_LOOP) - 1:
            h.append(_a(x + 95, 67, x + 109, 67))
    h.append(_l(23, 104, 557, 104))
    h.append(_l(23, 104, 23, 110))
    h.append(_l(557, 104, 557, 110))
    h.append(_t(24, 128, '고리 안 · JPM · BAC · C · WFC', 't-head', 'start'))
    h.append(_t(24, 170, '고리 밖 · 서는 법 세 가지', 't-head', 'start'))
    for i, (n, name, sub) in enumerate(_OUT):
        x = 23 + i * 182
        h.append(_r(x, 182, 170, 70, STRONG))
        h.append(_t(x + 12, 202, n, 't-head', 'start'))
        h.append(_t(x + 85, 222, name, 't-step'))
        h.append(_t(x + 85, 240, sub, 't-sub'))
    return _svg(580, 266, '대형 은행이 갇힌 예금과 대출의 고리, 그 바깥에 서는 수탁은행·거래중개·자산운용', h)


FIG_BANK = (
    1, '금리 인상의 부담이 은행에 닿는 고리, 그 바깥에 서는 세 회사',
    fig_bank(),
    '① 고객이 돈을 빌리러 오는 곳이 아니라 자산을 맡기러 오는 수탁은행<br>'
    '② 채권·외환·원자재·주식 거래와 기업금융 중심<br>'
    '③ 예금에서 빠진 자금이 닿는 ETF·펀드 운용사')


# ── 0920 ② 접점 수 ──────────────────────────────────────────────────────
def fig_connect():
    h = [_t(24, 22, '전력망과 만나는 지점이 몇 곳인가', 't-head', 'start')]
    h.append(_t(24, 52, '초대형 한 곳', 't-head', 'start'))
    h.append(_t(300, 52, '모듈형 수십 곳', 't-head', 'start'))
    h.append(_r(24, 64, 210, 68, STRONG))
    h.append(_t(129, 92, '초대형 데이터센터', 't-step'))
    h.append(_t(129, 112, '1GW급', 't-sub'))
    for i in range(3):
        x = 300 + i * 80
        h.append(_r(x, 64, 70, 68, BOX))
        h.append(_t(x + 35, 92, '모듈', 't-step'))
        h.append(_t(x + 35, 112, '10MW급', 't-sub'))
        h.append(_l(x + 35, 132, x + 35, 196))
    h.append(_t(544, 104, '…', 't-step'))
    h.append(_l(129, 132, 129, 196))
    h.append(_r(24, 196, 532, 34, BOX))
    h.append(_t(290, 218, '전력망', 't-step'))
    h.append(_t(142, 168, '①', 't-head', 'start'))
    h.append(_t(346, 168, '②', 't-head', 'start'))
    return _svg(580, 246, '초대형 데이터센터 한 곳과 모듈형 수십 곳이 전력망에 연결되는 접점 수 비교', h)


FIG_CONNECT = (
    2, '데이터센터가 흩어지면 전력망과의 접점이 늘어난다',
    fig_connect(),
    '① 한 곳이면 접점도 한 곳<br>'
    '② 사이트마다 새로 연결되어 변압기·스위치기어·차단기·배전설비가 다시 필요한 접점. '
    '작은 상자 셋과 줄임표는 「수십 곳」을 끊어 그린 것이고 곳 수는 원문에 없다')


# ── 0920 ③ 이튼과 버티브의 자리 ─────────────────────────────────────────
def fig_cover():
    h = [_t(24, 22, '두 회사가 강한 자리가 겹치는 곳은 UPS 하나다', 't-head', 'start')]
    h.append(_t(24, 44, '① 이튼 ETN', 't-head', 'start'))
    h.append(_t(556, 44, '② 버티브 VRT', 't-head', 'end'))
    h.append(_l(24, 52, 375, 52))
    h.append(_l(24, 52, 24, 58))
    h.append(_l(375, 52, 375, 58))
    h.append(_l(205, 64, 556, 64))
    h.append(_l(205, 64, 205, 70))
    h.append(_l(556, 64, 556, 70))
    cols = [(24, BOX, ['변압기', '스위치기어', '차단기', '배전반']),
            (205, STRONG, ['UPS']),
            (387, BOX, ['전력분배장치', '냉각장비', '액체냉각', '랙'])]
    for x, st, items in cols:
        h.append(_r(x, 80, 170, 100, st))
        if len(items) == 1:
            h.append(_t(x + 85, 135, items[0], 't-step'))
        else:
            for j, s in enumerate(items):
                h.append(_t(x + 85, 102 + j * 22, s, 't-msg'))
    h.append(_t(24, 212, '전력망 쪽', 't-head', 'start'))
    h.append(_a(100, 208, 480, 208))
    h.append(_t(556, 212, '서버랙 쪽', 't-head', 'end'))
    return _svg(580, 226, '이튼은 전기가 들어오는 길 전체, 버티브는 서버랙 옆 장비에 강하고 UPS에서 겹친다', h)


FIG_COVER = (
    3, '이튼은 전력망 쪽, 버티브는 서버랙 쪽, UPS는 둘 다 판다',
    fig_cover(),
    '① 변압기부터 UPS까지 전기가 들어오는 길 전체<br>'
    '② UPS부터 랙까지 서버랙 바로 옆 장비. 원문은 장비 사이의 순서를 말하지 않아 칸 안의 위아래를 순서로 읽지 않는다')


# ── 0921 ④ 다섯 질문 ────────────────────────────────────────────────────
_FIVE = [('① 가격 결정력', '은행 BK·USB 정리 → 손해보험 처브 확대'),
         ('② 고객 통로', '파라마운트 2024년 전량 매도 · 알파벳 매수'),
         ('③ 통제 밖 위험', 'TSMC 2022년 3분기 매수 → 2023년 1분기 매도'),
         ('④ 불황 체력', '항공사 · 주택 산업 (델타항공 2026년 재진입)'),
         ('⑤ 기존 현금흐름', '알파벳 · 검색과 유튜브')]


def fig_five():
    h = [_t(24, 22, '현금이 연 4% 안팎을 버는 문턱 위에서 고르는 다섯 질문', 't-head', 'start')]
    h.append(_r(24, 34, 532, 40, STRONG))
    h.append(_t(290, 59, '2025년 말 현금과 단기국채 약 3,700억 달러', 't-step'))
    h.append(_t(24, 104, '질문', 't-head', 'start'))
    h.append(_t(214, 104, '원문이 든 사례', 't-head', 'start'))
    for i, (q, c) in enumerate(_FIVE):
        y = 114 + i * 44
        h.append(_r(24, y, 170, 36, BOX))
        h.append(_t(36, y + 23, q, 't-step', 'start'))
        h.append(_r(204, y, 352, 36, BOX))
        h.append(_t(216, y + 23, c, 't-msg', 'start'))
    return _svg(580, 340, '버크셔의 현금 문턱과 다섯 질문, 질문마다 원문이 든 사례', h)


FIG_FIVE = (
    2, '이 현금을 포기하고 살 만큼 좋은가, 다섯 질문과 사례',
    fig_five(),
    '① 원가가 10% 오르면 1년 안에 가격을 얼마나 올릴 수 있나<br>'
    '② 회사와 돈을 내는 고객 사이에 플랫폼·유통업체·앱스토어 같은 누가 끼어 있나<br>'
    '③ 경영진이 풀 수 없는 전쟁·규제·수출통제·단일 공장 같은 위험이 무엇인가<br>'
    '④ 불황에 버티기만 하나, 경쟁자 점유율까지 가져가나<br>'
    '⑤ 테마가 틀려도 다른 사업에서 현금이 들어오나')


# ── 0923 ⑤ 경유 연쇄와 여유 없는 세 곳 ─────────────────────────────────
_CHAIN = [('러시아·중동', '경유 공급 감소'), ('미국산 경유', '수출 증가'),
          ('미국 경유', '재고 감소'), ('미국 경유 가격', '갤런당 6.529달러')]
_THREE = [('정유능력', '가동률 90%대 후반'), ('위치', '걸프 코스트에 몰림'),
          ('재고', '1982년 이후 최저')]


def fig_diesel():
    h = [_t(24, 22, '경유 공급이 모자란 연쇄와, 미국 안에서 여유가 없는 세 곳', 't-head', 'start')]
    for i, (a, b) in enumerate(_CHAIN):
        x = 26 + i * 138
        h.append(_r(x, 40, 114, 60, STRONG if i == 3 else BOX))
        h.append(_t(x + 57, 66, a, 't-step'))
        h.append(_t(x + 57, 86, b, 't-sub'))
        if i < 3:
            h.append(_a(x + 115, 74, x + 137, 74))
            h.append(_t(x + 126, 62, '①②③'[i], 't-head'))
    h.append(_t(24, 136, '여유가 없는 곳', 't-head', 'start'))
    for i, (a, b) in enumerate(_THREE):
        x = 24 + i * 182
        h.append(_r(x, 148, 170, 62, BOX))
        h.append(_t(x + 85, 174, a, 't-step'))
        h.append(_t(x + 85, 194, b, 't-sub'))
    return _svg(580, 226, '러시아·중동 공급 감소가 미국 경유 재고와 가격에 닿는 연쇄와 미국 안의 세 병목', h)


FIG_DIESEL = (
    1, '경유 가격이 오른 연쇄와 미국에 여유가 없는 세 곳',
    fig_diesel(),
    '① 우크라이나 공격으로 러시아 정유시설 피해, 이란 전쟁 관련 중동 차질<br>'
    '② 유럽·중남미가 높은 가격을 부르면 미국 정유사는 내수보다 수출<br>'
    '③ 재고가 얇은 상태에서 수요는 늘고 공급은 모자란다. 화물트럭과 농기계는 사용을 줄이기 어렵다')


_TOLL = [('버는 방식', '가격 급등을 번다', '병목 통과 수수료'),
         ('중요한 것', '크랙스프레드 수준(사이클)', '물량이 계속 움직이는지'),
         ('원문의 수치', 'PSX 2분기 가동률 96%|회사 전체 순이익 38억 달러',
          'OKE 2026년 이익의 약 90%|수수료 기반 예상')]


def fig_toll():
    h = [_t(24, 22, '같은 병목을 보는 두 가지 방식', 't-head', 'start')]
    h.append(_r(150, 34, 194, 36, STRONG))
    h.append(_t(247, 57, '① 정유사 VLO · PSX', 't-step'))
    h.append(_r(358, 34, 198, 36, STRONG))
    h.append(_t(457, 57, '② 파이프라인 OKE · KMI', 't-step'))
    for i, (lab, l, r) in enumerate(_TOLL):
        y = 82 + i * 56
        h.append(_t(24, y + 29, lab, 't-head', 'start'))
        for x, w, s in ((150, 194, l), (358, 198, r)):
            h.append(_r(x, y, w, 48, BOX))
            lines = s.split('|')
            if len(lines) == 1:
                h.append(_t(x + w // 2, y + 29, lines[0], 't-msg'))
            else:
                h.append(_t(x + w // 2, y + 20, lines[0], 't-msg'))
                h.append(_t(x + w // 2, y + 38, lines[1], 't-sub'))
    return _svg(580, 254, '정유사는 가격 급등을, 파이프라인 회사는 병목을 지나는 물량의 수수료를 번다', h)


FIG_TOLL = (
    3, '정유사는 가격 급등을, 파이프라인은 병목 통과 수수료를 번다',
    fig_toll(),
    '① 크랙스프레드(원유와 제품 가격 차이)가 높을 때 크게 번다. 수치는 PSX 2026년 2분기<br>'
    '② 정제제품 물류망을 지나는 물량에서 받는다. 수치는 OKE의 2026년 예상')


# ── 0925 ⑥ 같은 대출, 금리별 월 원리금 ─────────────────────────────────
_PAY = [(70, 1686, '금리 3%', '①'), (230, 2147, '금리 5%', '②'), (390, 2661, '금리 7%', '③')]


def fig_payment():
    h = [_t(24, 22, '40만 달러를 30년 고정금리로 빌릴 때 월 원리금', 't-head', 'start')]
    base, top = 214, 150.0
    h.append(_l(50, base, 530, base))
    for x, v, lab, n in _PAY:
        hh = int(round(v * top / 2661))
        h.append(_r(x, base - hh, 120, hh, STRONG if v == 2661 else BAR, 4))
        h.append(_t(x + 60, base - hh - 10, '{:,}달러'.format(v), 't-val'))
        h.append(_t(x + 60, base - 12, n, 't-head'))
        h.append(_t(x + 60, base + 22, lab, 't-step'))
    return _svg(580, 246, '같은 40만 달러 대출의 월 원리금은 금리 3%에서 1,686달러, 5%에서 2,147달러, 7%에서 2,661달러', h)


FIG_PAYMENT = (
    3, '같은 대출도 금리에 따라 월 납입액이 달라진다',
    fig_payment(),
    '① 몇 년 전 받아 둔 모기지. 이사하면 이 금리를 잃는다<br>'
    '② 건설사 바이다운 뒤 구매자 금리 수준. DHI Mortgage 계약 고객 평균은 6월 말 약 4.9%<br>'
    '③ 지금 시장금리(전날 기준 7.03%)')


_BLD = [('①', 'D.R. Horton', 'DHI · 회계 3분기', '20.7%', '인도 23,983채',
         ['자체 모기지', '금리 바이다운']),
        ('②', 'PulteGroup', 'PHM · 2분기', '25.0%', '신규 주문 7,536채',
         ['첫 구매자부터', '은퇴 수요까지']),
        ('③', 'NVR', 'NVR · 2분기', '21.5% → 19.2%', '신규 주문 +9%',
         ['토지 옵션 계약(LPA)', 'Lot 약 18만4,400개'])]


def fig_builders():
    h = [_t(24, 22, '세 건설사를 같은 항목으로 견준다', 't-head', 'start')]
    for i, (n, name, sub, gm, sale, how) in enumerate(_BLD):
        x = 24 + i * 182
        h.append(_r(x, 34, 170, 52, STRONG))
        h.append(_t(x + 12, 54, n, 't-head', 'start'))
        h.append(_t(x + 85, 60, name, 't-step'))
        h.append(_t(x + 85, 77, sub, 't-sub'))
        h.append(_r(x, 96, 170, 54, BOX))
        h.append(_t(x + 85, 114, '주택판매 gross margin', 't-sub'))
        h.append(_t(x + 85, 138, gm, 't-val'))
        h.append(_r(x, 160, 170, 54, BOX))
        h.append(_t(x + 85, 178, '판매', 't-sub'))
        h.append(_t(x + 85, 202, sale, 't-val'))
        h.append(_r(x, 224, 170, 62, BOX))
        h.append(_t(x + 85, 242, '버티는 수단', 't-sub'))
        h.append(_t(x + 85, 262, how[0], 't-msg'))
        h.append(_t(x + 85, 278, how[1], 't-msg'))
    return _svg(580, 302, '대형 건설사 셋의 마진, 판매, 버티는 수단', h)


FIG_BUILDERS = (
    3, '마진과 판매와 버티는 수단, 세 건설사의 같은 항목',
    fig_builders(),
    '① 마진 일부를 내주고 판매량과 점유율을 지킨 회사(필자 평가)<br>'
    '② 판매와 마진의 균형이 가장 좋은 회사(필자 평가)<br>'
    '③ 지금 실적보다 토지를 안 쌓은 구조로 보는 회사(필자 평가). 기준 분기가 회사마다 다르다')


# ── 0927 ⑦ 2023년과 2026년 ──────────────────────────────────────────────
def fig_kr_now():
    h = [_t(24, 22, '한국은행이 멈춘 2023년과 지금의 한국', 't-head', 'start')]
    h.append(_r(128, 34, 200, 34, STRONG))
    h.append(_t(228, 56, '① 2023년', 't-step'))
    h.append(_r(340, 34, 216, 34, STRONG))
    h.append(_t(448, 56, '② 2026년', 't-step'))
    rows = [('성장률', None), ('기준금리', ('0.5% → 3.5%, 300bp 인상 뒤', '2.50% → 3% (7·8월 연속 인상)')),
            ('금융시장', ('부동산 PF · 회사채시장 불안', '반도체 수출 · 설비투자 강세')),
            ('주택 규제', ('기준금리가 유일한 수단', None))]
    for i, (lab, cells) in enumerate(rows):
        y = 78 + i * 52
        h.append(_t(24, y + 27, lab, 't-head', 'start'))
        h.append(_r(128, y, 200, 44, BOX))
        h.append(_r(340, y, 216, 44, BOX))
        if lab == '성장률':
            h.append(_r(140, y + 8, 42, 14, BAR, 3))
            h.append(_t(190, y + 21, '1.4%', 't-val', 'start'))
            h.append(_r(352, y + 8, 99, 14, BAR, 3))
            h.append(_t(459, y + 21, '3.3%', 't-val', 'start'))
            h.append(_t(352, y + 38, '한국은행 올해 전망', 't-sub', 'start'))
        elif lab == '주택 규제':
            h.append(_t(140, y + 27, cells[0], 't-msg', 'start'))
            h.append(_t(352, y + 18, '규제지역 LTV 40%', 't-sub', 'start'))
            h.append(_t(352, y + 35, 'DSR 40% · 수도권 주담대 한도', 't-sub', 'start'))
        else:
            h.append(_t(140, y + 27, cells[0], 't-msg', 'start'))
            h.append(_t(352, y + 27, cells[1], 't-msg', 'start'))
    return _svg(580, 290, '2023년과 2026년의 성장률, 기준금리, 금융시장, 주택 규제 비교', h)


FIG_KR_NOW = (
    3, '2023년에는 멈춘 한국은행이 지금은 선택지가 다르다',
    fig_kr_now(),
    '① 한국은행이 미국보다 먼저 인상을 멈춘 해<br>'
    '② 7월과 8월 연속 인상으로 3%가 된 지금. 성장률 막대는 1.4%와 3.3%에 비례한다')


def fig_kr_delinq():
    h = [_t(24, 22, '가계대출 연체율', 't-head', 'start')]
    sc = 22.0
    groups = [(36, [('전체', 0.98, False), ('① 취약차주', 10.39, True)]),
              (112, [('전체', 1.99, False), ('② 취약 자영업자', 12.71, True)])]
    for gi, (gy, bars) in enumerate(groups):
        if gi == 1:
            h.append(_t(24, gy - 14, '자영업자 대출 연체율', 't-head', 'start'))
        for bi, (lab, v, strong) in enumerate(bars):
            y = gy + bi * 30
            w = int(round(v * sc))
            h.append(_t(24, y + 16, lab, 't-sub', 'start'))
            h.append(_r(130, y, w, 22, STRONG if strong else BAR, 3))
            h.append(_t(130 + w + 8, y + 17, '{}%'.format(v), 't-val', 'start'))
    h.append(_t(24, 206, '한번 연체에 빠진 취약 자영업자가 다음 분기에도 연체: 82.3%', 't-msg', 'start'))
    return _svg(580, 226, '전체 가계대출 연체율 0.98%와 취약차주 10.39%, 전체 자영업자 1.99%와 취약 자영업자 12.71%', h)


FIG_KR_DELINQ = (
    4, '취약 차주와 취약 자영업자의 연체율은 평균과 크게 벌어져 있다',
    fig_kr_delinq(),
    '① 저소득·저신용 다중채무자<br>'
    '② 취약 자영업자. 막대 길이는 연체율에 비례한다. 한국은행 수치를 필자가 신문 기사로 인용했다')


ALL = [FIG_BANK, FIG_CONNECT, FIG_COVER, FIG_FIVE, FIG_DIESEL, FIG_TOLL,
       FIG_PAYMENT, FIG_BUILDERS, FIG_KR_NOW, FIG_KR_DELINQ]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
