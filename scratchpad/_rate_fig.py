# -*- coding: utf-8 -*-
"""보고서 ⑧ 금리·물가 층의 도해 일곱. 색은 회색만(확정 규칙 S2) — 강조는 짙은 테두리 하나.

값은 전부 원문에 있는 것만 그린다. 도형 개수도 값이라, 셀 수 있는 것은 원문이 센 수와 같게
그리고 아니면 캡션에 그렇게 적는다(insight-figure 규칙 1). 좌표는 헬퍼가 계산한다(규칙 2).
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
_elbow = bf._elbow
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _fill(x, y, w, h, st=INK3, sw=1.5, rx=8):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="var(--sunk)" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, st, sw))


def _plain(x, y, w, h, st=INK3, sw=1.5, rx=4, dash=False):
    extra = ' stroke-dasharray="5 4"' if dash else ''
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, st, sw, extra))


# ── 도해 1. 연준은 내렸는데 장기금리는 올랐다 ────────────────────────
# 값은 엘곰-0819 L23(2024-09-18 이후 인하 1.75%p · 10년물 +1%p · 30년물 +1.3%p).
# 화살표 길이가 변화폭에 비례한다. 1%p = 46px.
_GB = 150                    # 화살표가 서는 기준선(변화 0)


def _mv(v):
    return int(46 * abs(v))


def _arrow(x, v, lab, who, accent=False):
    st = INK if accent else INK3
    sw = 2.0 if accent else 1.5
    h = _mv(v)
    y0, y1 = (_GB, _GB - h) if v > 0 else (_GB, _GB + h)
    return ''.join([
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"/>' % (x, y0, x, y1, st, sw),
        '<path d="M%d %d l-5 %d h10 z" fill="%s"/>' % (x, y1, 8 if v > 0 else -8, st),
        _t(x, y1 - 10 if v > 0 else y1 + 20, lab, 't-lab'),
        _t(x, _GB + 26 if v > 0 else _GB - 14, who),
    ])


FIG_GAP = _svg(W, 288, '연준은 내렸는데 장기금리는 올랐다 (2024-09-18 이후 변화, %포인트)', ''.join([
    _lt(18, 24, '2024년 9월 18일부터 2026년 8월까지의 변화폭', 't-sm', True),
    '<line x1="40" y1="%d" x2="600" y2="%d" stroke="%s" stroke-width="1"/>' % (_GB, _GB, INK3),
    _lt(18, _GB + 4, '0', 't-sm', False),
    _arrow(160, -1.75, '1.75 내림', '연준 기준금리'),
    _arrow(340, 1.0, '1.0 오름', '10년물'),
    _arrow(500, 1.3, '1.3 오름', '30년물', accent=True),
    _lt(18, 280, '화살표 길이는 변화폭에 비례한다', 't-sm', False),
]))


# ── 도해 2. 명목금리를 셋으로 쪼개면 어디가 튀었나 ──────────────────
# 값은 메르-유가 T57·T99·T101. 30년물 실질금리 2.987%, BEI 2.3%대.
# 막대 높이는 값에 비례(3% = 132px). 명목금리 총합은 원문에 없어 안 그린다.
_TB = 200


def _tk(v):
    return int(132 * v / 3.0)


def _tbar(x, v, lab, name, note, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    h = _tk(v)
    return ''.join([
        '<rect x="%d" y="%d" width="94" height="%d" rx="5" fill="%s" stroke="%s" stroke-width="%s"/>'
        % (x, _TB - h, h, 'var(--sunk)' if accent else 'none', st, sw),
        _t(x + 47, _TB - h - 8, lab, 't-sm'),
        _t(x + 47, _TB + 20, name, 't-sm'),
        _t(x + 47, _TB + 36, note, 't-sm'),
    ])


FIG_TIPS = _svg(W, 262, '유가가 올랐는데 튄 것은 기대인플레이션이 아니라 실질금리였다', ''.join([
    _lt(18, 22, '30년물을 두 조각으로 (%)', 't-sm', True),
    _tbar(150, 2.987, '2.987', '실질금리', '2008년 이후 최고', accent=True),
    _tbar(340, 2.3, '2.3대', '기대인플레이션', '별로 안 튀었다'),
    _lt(18, 254, '교과서대로라면 유가 충격은 오른쪽에 얹혀야 한다', 't-sm', False),
]))


# ── 도해 3. 물가 잣대를 바꿔 온 계보 ────────────────────────────────
# 값은 사슬-CPI b2·d1·d3·d5·b3·b4. 사슬이 이어 놓은 순서를 그대로 그린다.
_GG = _row(4, 56, 96, 134, gap=22)
_GG_TXT = [('1970년대', '아서 번즈', '근원 CPI 를 만든다', '에너지·곡물을 뺀다'),
           ('1995~96년', '그린스펀', 'CPI 가 과대계상', '위원회가 1.1%p 결론'),
           ('2000년 2월', '연준', '핵심 지표를 PCE 로', '0.4%p 낮게 보인다'),
           ('2026년 6월', '케빈 워시', '절사평균을 선호', '3.8 을 2.3 으로')]
FIG_GAUGE = _svg(W, 214, '잣대를 바꾸면 같은 물가가 낮아 보인다', ''.join(
    [_lt(18, 26, '사슬이 이어 놓은 네 걸음', 't-sm', True)]
    + [''.join([
        (_fill(*c, st=INK, sw=2.0) if i == 3 else _plain(*c, st=INK3, sw=1.5, rx=8)),
        _t(c[0] + 67, c[1] + 22, h, 't-lab'),
        _t(c[0] + 67, c[1] + 44, l1),
        _t(c[0] + 67, c[1] + 62, l2),
        _t(c[0] + 67, c[1] + 80, l3),
    ]) for i, (c, (h, l1, l2, l3)) in enumerate(zip(_GG, _GG_TXT))]
    + [_a(_GG[i][0] + _GG[i][2], 104, _GG[i + 1][0], 104) for i in range(3)]
    + [_lt(18, 206, '메르는 이것을 숫자 마사지라 불렀고, 잭슨홀 선언을 그 가설이 깨지는 자리로 표시했다',
           't-sm', False)]
))


# ── 도해 4. 할인율 — 금리가 1%포인트 오르면 오늘 값이 얼마나 깎이나 ────
# 값은 메르-AI주가 T45-T47·T51-T57·T61. 1년 뒤 1천만원, 10년 뒤 1천만원의 오늘 값.
# 막대 높이는 값에 비례(1,000만원 = 132px).
_DB = 200


def _dk(v):
    return int(132 * v / 1000.0)


def _dbar(x, v, lab, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    h = _dk(v)
    return ''.join([
        '<rect x="%d" y="%d" width="70" height="%d" rx="5" fill="%s" stroke="%s" stroke-width="%s"/>'
        % (x, _DB - h, h, 'var(--sunk)' if accent else 'none', st, sw),
        _t(x + 35, _DB - h - 8, lab, 't-sm'),
    ])


FIG_DISCOUNT = _svg(W, 268, '먼 미래일수록 같은 1%포인트가 크게 깎는다 (만원)', ''.join([
    _lt(18, 22, '1년 뒤 1,000만원의 오늘 값', 't-sm', True),
    _dbar(60, 961, '961'),
    _dbar(150, 952, '952', accent=True),
    _t(95, 222, '금리 4%', 't-sm'), _t(185, 222, '금리 5%', 't-sm'),
    _t(140, 244, '9만원 깎인다', 't-sm'),
    '<line x1="270" y1="30" x2="270" y2="252" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' % INK3,
    _lt(292, 22, '10년 뒤 1,000만원의 오늘 값', 't-sm', True),
    _dbar(340, 676, '676'),
    _dbar(430, 614, '614', accent=True),
    _t(375, 222, '금리 4%', 't-sm'), _t(465, 222, '금리 5%', 't-sm'),
    _t(420, 244, '62만원 깎인다', 't-sm'),
]))


# ── 도해 5. 채권 자경단이 나타난 네 번 ──────────────────────────────
# 값은 메르-자경단2 T61·T67·T80-T82·T90-T96. 사례 개수 넷이 원문이 센 수다.
def _case(i, when, where, what, done):
    y = 46 + i * 46
    return ''.join([
        _lt(18, y + 20, when, 't-sm', True),
        _lt(96, y + 20, where, 't-sm', True),
        _plain(160, y, 290, 30, INK3, 1.5, rx=5),
        _t(305, y + 20, what, 't-sm'),
        _a(450, y + 15, 470, y + 15),
        _lt(476, y + 20, done, 't-sm', False),
    ])


FIG_VIGILANTE = _svg(W, 258, '채권 자경단이 나타난 네 번 — 매번 정책이 물러섰다', ''.join([
    _lt(18, 26, '재정적자 확대 · 물가 우려 · 중앙은행 독립성 훼손 셋이 겹칠 때 나타난다', 't-sm', True),
    _case(0, '1993', '미국', '10년물 5.2% → 8%', '클린턴이 지출 취소'),
    _case(1, '2022', '영국', '트러스 감세안', '49일 만에 사퇴'),
    _case(2, '2025-04', '미국', '상호관세 발표', '9일 만에 90일 유예'),
    _case(3, '2026-01', '일본', '40년물 4% 돌파', '다카이치가 발행 축소'),
    _lt(18, 250, '왼쪽은 방아쇠, 오른쪽은 물러선 결과다', 't-sm', False),
]))


# ── 도해 6. 바이백을 두 사람이 다르게 셌다 ──────────────────────────
# 값은 메르-바이백 T44·T46·T48, 미주사-0821 L34-35. 셈이 갈리는 것 자체가 이 그림의 내용이다.
_BC = _row(2, 54, 128, 250, gap=30)


def _count(c, who, l1, l2, l3, l4):
    x, y, w, h = c
    return ''.join([
        _plain(x, y, w, h, INK3, 1.5, rx=8),
        _t(x + w // 2, y + 24, who, 't-lab'),
        _t(x + w // 2, y + 48, l1),
        _t(x + w // 2, y + 68, l2),
        _t(x + w // 2, y + 88, l3),
        _t(x + w // 2, y + 110, l4, 't-lab'),
    ])


FIG_BUYBACK = _svg(W, 226, '같은 바이백을 두 사람이 다르게 셌다', ''.join([
    _lt(18, 26, '재무부가 한 회 한도를 20억에서 40억 달러로 늘린 조치 (2026-08-19)', 't-sm', True),
    _count(_BC[0], '메르', '증액 대상은 두 구간', '각 구간을 분기에 네 번', '분기 여덟 번으로 센다',
           '전에는 분기 160억 달러'),
    _count(_BC[1], '미국주식 사관학교', '구간별로 월 한 번으로 가정', '두 달에 네 번', '',
           '두 달에 100~200억 달러'),
    _lt(18, 218, '미주사는 이것이 자기 가정이라고 밝혀 두었다. 32조 달러 시장 앞이라는 판단은 같다',
        't-sm', False),
]))


# ── 도해 7. 같은 값을 놓고 원인을 다르게 든다 ────────────────────────
# 값 없음. 화자 배치만 보인다 — 상자 개수는 이 글이 다룬 화자 수다.
_WC = _row(4, 100, 92, 146, gap=8)
_WHO = [('메르', '실질금리가', '2008년 이후 최고'),
        ('엘곰', '정책 신뢰가', '흔들렸다'),
        ('미국주식 사관학교', '매수자가', '교체됐다'),
        ('김상훈', '일본이', '팔아야 했다')]
FIG_WHO = _svg(W, 248, '30년물이 19년 만의 고점을 찍은 한 달, 원인 진단이 넷으로 갈렸다', ''.join(
    [_fill(196, 22, 248, 44, INK, 2.0),
     _t(320, 50, '30년물 5.31% · 2026년 8월', 't-lab')]
    + [''.join([
        _plain(*c, st=INK3, sw=1.5, rx=8),
        _t(c[0] + 73, c[1] + 26, w, 't-lab'),
        _t(c[0] + 73, c[1] + 50, l1),
        _t(c[0] + 73, c[1] + 70, l2),
    ]) for c, (w, l1, l2) in zip(_WC, _WHO)]
    # 머리에서 내려와 가로로 흐르다 상자마다 내려꽂는 버스. _elbow 로 그리면 가로선이
    # 상자 윗변과 겹쳐 안 보인다(2026-09-05 스크린샷에서 잡았다)
    + ['<line x1="320" y1="66" x2="320" y2="84" stroke="%s" stroke-width="1.5"/>' % INK3,
       '<line x1="%d" y1="84" x2="%d" y2="84" stroke="%s" stroke-width="1.5"/>'
       % (_WC[0][0] + 73, _WC[3][0] + 73, INK3)]
    + ['<line x1="%d" y1="84" x2="%d" y2="100" stroke="%s" stroke-width="1.5"/>'
       % (c[0] + 73, c[0] + 73, INK3) for c in _WC]
    + [_lt(18, 226, '넷은 서로를 지우지 않는다. 처방은 오히려 모인다 — 장기채를 지금 담지 말라는 데',
           't-sm', True),
       _lt(18, 242, '메르와 미국주식 사관학교가 같은 자리에 선다', 't-sm', False)]
))


# ── 도해 8. 값이 날짜로 어떻게 움직였나 ─────────────────────────────
# 점은 전부 원문에 날짜와 함께 적힌 값이고, 점 사이 선은 이어 본 것이다(캡션에 밝힌다).
# 코퍼스에 있는 값만 쓴다 — FRED 같은 바깥 시계열을 끌어오지 않았다.
# 값 출처: 미주사-0608 L16-17 · 엘곰-0724 L13 · 엘곰-0801 L38 · 엘곰-0802 L6 ·
#          엘곰-0818 L21 · 엘곰-0819 L7 · 엘곰-0822 L19 · 쟁점-0828 L31 · 언보-0824 L97
_SX0, _SX1 = 92, 596          # 가로 눈금 왼쪽·오른쪽 끝
_SY0, _SY1 = 46, 214          # 세로 눈금 위(5.4%)·아래(4.4%)
_SHI, _SLO = 5.4, 4.4         # 세로 눈금 상·하한


def _sx(d):
    """6월 5일을 0, 8월 24일을 1 로 둔 자리. 날짜는 그 사이 일수로 잰다."""
    return _SX0 + int((_SX1 - _SX0) * d)


def _sy(v):
    return _SY1 - int((_SY1 - _SY0) * (v - _SLO) / (_SHI - _SLO))


# (이름 없는 날짜, 값) — 6/5 를 0일로 두고 8/24 까지 80일
def _dd(day):
    return day / 80.0


_T30 = [(56, 5.09, '7월 말 5.09'), (58, 5.27, '8/2 5.27'), (74, 5.31, '8/18 5.31'),
        (74, 5.34, '5.34'), (75, 5.19, '8/19 5.19'), (76, 5.25, '8/20 5.25')]
_T10 = [(0, 4.55, '6/5 4.55'), (49, 4.71, '7/24 4.71'), (57, 4.71, '8/1 4.71'),
        (74, 4.72, '8/18 4.72'), (76, 4.70, '8/20 4.70'), (80, 4.75, '8/24 4.75')]


def _line(pts, accent):
    st = INK if accent else INK3
    sw = 2.0 if accent else 1.5
    xy = [(_sx(_dd(d)), _sy(v)) for d, v, _l in pts]
    out = ['<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"/>'
           % (' '.join('%d,%d' % p for p in xy), st, sw)]
    for (x, y) in xy:
        out.append('<circle cx="%d" cy="%d" r="3.5" fill="var(--paper)" stroke="%s" '
                   'stroke-width="2"/>' % (x, y, st))
    return ''.join(out)


FIG_SERIES = _svg(W, 292, '2026년 6월부터 8월까지 미국 국채금리가 어떻게 움직였나 (%)', ''.join(
    [_lt(18, 24, '점은 원문에 날짜와 함께 적힌 값이다. 점 사이 선은 이어 본 것이다', 't-sm', True)]
    # 세로 눈금 — 원문에 나온 구간만 긋는다
    + ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" '
       'stroke-dasharray="3 4"/>' % (_SX0, _sy(v), _SX1, _sy(v), INK3) for v in (4.5, 5.0)]
    + [_lt(52, _sy(4.5) + 4, '4.5', 't-sm', False), _lt(52, _sy(5.0) + 4, '5.0', 't-sm', False)]
    + [_line(_T10, False), _line(_T30, True)]
    + [_lt(_SX0, 238, '6/5', 't-sm', False), _lt(_sx(_dd(49)) - 10, 238, '7/24', 't-sm', False),
       _lt(_sx(_dd(74)) - 14, 238, '8/18', 't-sm', False)]
    + [_lt(_sx(_dd(0)) + 8, _sy(4.55) + 18, '10년물', 't-lab', True),
       _lt(_sx(_dd(56)) - 46, _sy(5.09) - 10, '30년물', 't-lab', True)]
    + [_lt(18, 262, '8월 18일에 30년물을 두 편이 5.31%와 5.34%로 다르게 적었다. 둘 다 찍었다',
           't-sm', False),
       _lt(18, 280, '기준금리는 이 구간 내내 3.50~3.75% 동결이다', 't-sm', False)]
))
