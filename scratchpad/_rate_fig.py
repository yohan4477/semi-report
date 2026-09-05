# -*- coding: utf-8 -*-
"""보고서 ⑧ 금리·물가 층의 도해 일곱. 색은 회색만(확정 규칙 S2) — 강조는 짙은 테두리 하나.

값은 전부 원문에 있는 것만 그린다. 도형 개수도 값이라, 셀 수 있는 것은 원문이 센 수와 같게
그리고 아니면 캡션에 그렇게 적는다(insight-figure 규칙 1). 좌표는 헬퍼가 계산한다(규칙 2).
"""
import datetime as _dt
import os as _os
import sys as _sys

import _biz_fig as bf

_sys.path.insert(0, _os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'scripts'))
from fetch_fred import load as _fred        # noqa: E402  도해의 선은 이 값이다

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
_elbow = bf._elbow
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'
# 확정 규칙 S2 는 회색만이다. 시계열에서 선이 셋을 넘으면 회색만으로는 안 갈려서
# **기준금리 한 줄에만** 예외를 뒀다(2026-09-06). 이미 있는 --fig-amber 를 쓴다
AMBER = 'var(--rate-amber)'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _fill(x, y, w, h, st=INK3, sw=1.5, rx=8):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="var(--sunk)" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, st, sw))


def _plain(x, y, w, h, st=INK3, sw=1.5, rx=4, dash=False):
    extra = ' stroke-dasharray="5 4"' if dash else ''
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, st, sw, extra))


# 도해 1(화살표로 그린 변화폭)은 걷었다 — FRED 선을 들여오면서 FIG_DIVERGE 가 같은 말을
# 더 정확히 한다. 안 실리는 도해를 파일에 두면 목록이 거짓말을 한다(2026-09-06).

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


# ── 도해 8. 2026년 여름 — 원문이 짚은 날에 점을 찍는다 ────────────────
# 선은 FRED, 점은 원문이 짚은 **날**이다. 값이 아니라 날에 찍는다 — 원문 값에 찍으면
# 선에서 떠서 잘못 그린 것처럼 보인다(2026-09-06 지적). 값이 갈리는 자리는 캡션이 말한다.
# 점 출처: 미주사-0608 · 엘곰-0724 · 엘곰-0801 · 엘곰-0802 · 엘곰-0818 · 엘곰-0819 ·
#          엘곰-0822 · 쟁점-0828 · 언보-0824


# ── 시계열 부품 — 구간과 눈금만 갈아 끼워 여러 절에 쓴다 ─────────────
# 선은 FRED, 점은 원문(fetch_fred.py 규약). 절마다 필요한 구간이 달라 한 장으로는 안 된다.
def _chart(d0, d1, lo, hi, lines, dots=(), marks=(), top=68, bot=196,
           x0=88, x1=604, ticks=(), ylab=()):
    """d0~d1 구간을 그린다.

    lines  [(id, 이름, 짙게?)] · [(id, 이름, 짙게?, 점선?)] · [(id, 이름, 짙게?, 점선?, 색)]
    dots   [(날짜, 시리즈 id, 짙게?)]  원문이 짚은 **날**. 값은 그날 FRED 값에 찍는다
    marks  [(날짜, 글자)]             그 날에 세로 점선과 글자
    ticks  [(날짜, 글자)]             가로 눈금
    ylab   [값]                       세로 눈금
    """
    dt = _dt
    D0 = dt.date(*map(int, d0.split('-')))
    D1 = dt.date(*map(int, d1.split('-')))
    span = max(1, (D1 - D0).days)

    def X(d):
        return x0 + int((x1 - x0) * (d - D0).days / float(span))

    def Y(v):
        return bot - int((bot - top) * (v - lo) / float(hi - lo))

    out, legend = [], []
    for v in ylab:
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1" '
                   'stroke-dasharray="3 4"/>' % (x0, Y(v), x1, Y(v), INK3))
        out.append(_lt(x0 - 38, Y(v) + 4, ('%g' % v), 't-sm', False))
    for ymd, lab in marks:
        d = dt.date(*map(int, ymd.split('-')))
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2" '
                   'stroke-dasharray="5 4"/>' % (X(d), top, X(d), bot, INK3))
        out.append(_t(X(d), bot + 38, lab, 't-sm'))
    for spec in lines:
        sid, name, accent = spec[0], spec[1], spec[2]
        dash = spec[3] if len(spec) > 3 else False
        col = spec[4] if len(spec) > 4 else None
        pts = []
        for k, v in sorted(_fred(sid).items()):
            dd = dt.date(*map(int, k.split('-')))
            if D0 <= dd <= D1 and lo <= v <= hi:
                pts.append((X(dd), Y(v)))
        if not pts:
            continue
        st, sw = (INK, 2.0) if accent else (INK3, 1.4)
        if col:
            st, sw = col, 2.0
        dd = ' stroke-dasharray="6 3"' if dash else ''
        out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s/>'
                   % (' '.join('%d,%d' % p for p in pts), st, sw, dd))
        legend.append((name, accent, dash, col))
    # 점은 **그날 FRED 값**에 찍는다. 원문 값에 찍으면 선에서 떠서 잘못 그린 것처럼 보인다
    # (2026-09-06 지적). 원문이 짚은 것은 「그 날」이고, 값이 갈리는 자리는 캡션이 말한다
    for ymd, sid, accent in dots:
        d = dt.date(*map(int, ymd.split('-')))
        v = _fred(sid).get(ymd)
        if v is None or not (lo <= v <= hi):
            continue
        out.append('<circle cx="%d" cy="%d" r="3.4" fill="var(--paper)" stroke="%s" '
                   'stroke-width="2.2"/>' % (X(d), Y(v), INK if accent else INK3))
    for ymd, lab in ticks:
        d = dt.date(*map(int, ymd.split('-')))
        out.append(_t(X(d), bot + 20, lab, 't-sm'))
    # 범례 — 판 위 오른쪽 끝에 이름을 붙이면 넘친다. 머리글 아래 한 줄로 둔다
    lx = x0
    for name, accent, dash, col in legend:
        out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%s"%s/>'
                   % (lx, top - 14, lx + 18, top - 14,
                      col or (INK if accent else INK3), 2.0 if accent else 1.4,
                      ' stroke-dasharray="6 3"' if dash else ''))
        out.append(_lt(lx + 24, top - 10, name, 't-sm', accent))
        lx += 30 + len(name) * 9
    return ''.join(out)


# ── 도해 1a. 연준은 내리는데 장기금리는 올라갔다 — 두 해를 이어서 ────────
# 엘곰-0819 L23 의 주장을 시계열로. 값은 FRED, 점은 원문이 짚은 두 자리.
FIG_DIVERGE = _svg(W, 300, '연준이 내리기 시작한 뒤 장기금리는 거꾸로 갔다 (%)', ''.join([
    _lt(18, 22, '2024년 9월 18일 첫 인하부터 지금까지. 선은 FRED 일별', 't-sm', True),
    _chart('2024-09-01', '2026-09-04', 2.8, 5.6,
           [('DFF', '기준금리', False, False, AMBER), ('DGS10', '10년물', False),
            ('DGS30', '30년물', True)],
           marks=[('2024-09-18', '첫 인하')],
           ticks=[('2024-10-01', '2024-10'), ('2025-05-01', '2025-05'),
                  ('2025-12-01', '2025-12'), ('2026-07-01', '2026-07')],
           ylab=[3.0, 4.0, 5.0]),
    _lt(18, 262, '기준금리는 1.7%p 내려왔는데 30년물은 1.2%p 올라갔다', 't-sm', True),
    _lt(18, 280, '둘이 반대로 간 것이 이 글이 설명하려는 어긋남이다', 't-sm', False),
]))


# ── 도해 1b. 장단기 역전과 그 해소 — 메르가 직접 짚은 시리즈 ──────────
# 메르-역전 T40-T47 이 독자에게 FRED 의 T10Y2Y 를 열어 보라고 한다. 그 화면을 그린다.
FIG_INVERT = _svg(W, 300, '10년물에서 2년물을 뺀 값 — 0 아래가 역전이다 (%포인트)', ''.join([
    _lt(18, 22, '메르가 독자에게 직접 열어 보라고 짚은 FRED 시리즈다 (T10Y2Y)', 't-sm', True),
    _chart('2021-01-01', '2026-09-04', -1.2, 1.0,
           [('T10Y2Y', '10년-2년', True)],
           marks=[('2023-07-03', '최저'), ('2024-09-05', '역전 해소')],
           ticks=[('2021-06-01', '2021'), ('2023-01-01', '2023'),
                  ('2024-09-01', '2024'), ('2026-06-01', '2026')],
           ylab=[-1.0, 0.0, 1.0]),
    _lt(18, 262, '2022년 4월에 뒤집혀 541거래일 만인 2024년 9월 5일에 풀렸다', 't-sm', True),
    _lt(18, 280, '가장 깊었던 자리가 2023년 7월 3일 -1.08%p — 메르가 40년 만이라 한 107bp 다',
        't-sm', False),
]))


# ── 도해 9a. 바이백 사흘 — 발표에 하루 내리고 이튿날 되올라왔다 ──────────
# 절 9 의 사흘을 확대한다. 넓은 구간에서는 이 움직임이 안 보인다.
FIG_ZOOM = _svg(W, 282, '재무부 바이백 발표 전후 30년물 (%)', ''.join([
    _lt(18, 22, '8월 10일부터 9월 4일까지. 넓게 보면 안 보이는 사흘이다', 't-sm', True),
    _chart('2026-08-10', '2026-09-04', 5.10, 5.36,
           [('DGS30', '30년물', True)],
           dots=[('2026-08-17', 'DGS30', True), ('2026-08-19', 'DGS30', True),
                 ('2026-08-20', 'DGS30', True)],
           marks=[('2026-08-19', '바이백 발표')],
           ticks=[('2026-08-10', '8/10'), ('2026-08-19', '8/19'),
                  ('2026-08-27', '8/27'), ('2026-09-03', '9/3')],
           ylab=[5.2, 5.3]),
    _lt(18, 262, '발표에 9bp 내렸다가 이튿날 되올라 그 주 안에 발표 이전을 넘어섰다', 't-sm', True),
]))


FIG_SERIES = _svg(W, 300, '2026년 6월부터 9월까지 미국 국채금리 (%)', ''.join([
    _lt(18, 22, '선은 FRED 일별 종가, 동그라미는 원문이 짚은 날', 't-sm', True),
    _chart('2026-06-01', '2026-09-04', 4.4, 5.4,
           [('DGS10', '10년물', False), ('DGS30', '30년물', True)],
           dots=[('2026-07-28', 'DGS30', True), ('2026-08-03', 'DGS30', True),
                 ('2026-08-17', 'DGS30', True), ('2026-08-19', 'DGS30', True),
                 ('2026-08-20', 'DGS30', True),
                 ('2026-06-05', 'DGS10', False), ('2026-07-24', 'DGS10', False),
                 ('2026-08-03', 'DGS10', False), ('2026-08-18', 'DGS10', False),
                 ('2026-08-20', 'DGS10', False)],
           marks=[('2026-07-29', 'FOMC'), ('2026-08-19', '바이백')],
           ticks=[('2026-06-05', '6/5'), ('2026-07-10', '7/10'),
                  ('2026-08-14', '8/14'), ('2026-09-03', '9/3')],
           ylab=[4.5, 5.0]),
    _lt(18, 262, '두 달 반 동안 30년물이 4.9%대에서 5.3%대로 올라섰다', 't-sm', True),
    _lt(18, 280, '엘곰이 「화요일 5.34%」라 적은 날 FRED 종가는 5.28% 다 — 장중 고점으로 보인다',
        't-sm', False),
]))
