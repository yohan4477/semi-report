# -*- coding: utf-8 -*-
"""보고서 ⑥ CPO 층의 도해 여덟. 색은 회색만(확정 규칙 S2) — 강조는 짙은 테두리 하나.

값은 전부 원문에 있는 것만 그린다. 상자 개수가 우리 묶음이면 캡션에 그렇게 적는다.
좌표는 _row 가 계산하고 손으로 찍지 않는다(insight-figure 규칙 2).
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _fill(x, y, w, h, st=INK3, sw=1.5):
    """옅은 회색 채움 상자 — 이 글이 고른 자리 한 곳에만 쓴다."""
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="var(--sunk)" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, st, sw))


# ── 도해 0. 세 층 지도 — 값 없음 ────────────────────────────────────
# 스케일업·스케일아웃·스케일어크로스 세 층을 같은 꼴 모듈 셋으로. 구리·광 경계만 보인다.
_L = _row(3, 40, 118, 196, gap=16)
FIG_MAP = _svg(W, 176, '데이터센터 연결 세 층과 구리·광의 경계', ''.join([
    _lt(_L[0][0], 26, '랙 안', 't-sm', True),
    _lt(_L[1][0], 26, '랙과 랙 사이', 't-sm', True),
    _lt(_L[2][0], 26, '건물·캠퍼스 사이', 't-sm', True),
    _fill(*_L[0], st=INK, sw=2.0),
    _t(_L[0][0] + 98, 72, '스케일업', 't-lab'),
    _t(_L[0][0] + 98, 96, 'GPU끼리 직접 연결'),
    _t(_L[0][0] + 98, 114, '구리 백플레인'),
    _t(_L[0][0] + 98, 132, '빛은 아직 못 들어옴'),
    _box(*_L[1], lines=['스케일아웃', '스위치로 묶는다', '플러거블 트랜시버', 'CPO 스위치 첫 실물 2025']),
    _box(*_L[2], lines=['스케일어크로스', '20~50마일', '코히런트 광 · WDM', '빛만 가능']),
    _a(_L[0][0] + _L[0][2], 99, _L[1][0], 99),
    _a(_L[1][0] + _L[1][2], 99, _L[2][0], 99),
]))


# ── 도해 1. 구리가 닿는 거리 — 세대마다 반 ───────────────────────────
# 값 셋은 SD-0807 L36-38(Barber). 막대 길이는 거리에 비례한다 — 2m 를 380px 로.
_BX0, _BW = 150, 380


def _bar(i, lab, m, txt):
    y = 40 + i * 54
    w = int(_BW * m / 2.0)
    return ''.join([
        _lt(18, y + 24, lab, 't-lab'),
        '<rect x="%d" y="%d" width="%d" height="30" rx="6" fill="var(--sunk)" stroke="%s" stroke-width="1.5"/>'
        % (_BX0, y + 4, w, INK3),
        _lt(_BX0 + w + 10, y + 24, txt, 't-sm', True),
    ])


FIG_REACH = _svg(W, 230, '신호 증폭 없는 직결 구리가 닿는 거리', ''.join([
    _bar(0, '100G/레인', 2.0, '약 2m · 랙 높이'),
    _bar(1, '200G/레인', 1.0, '약 1m · 스위치를 랙 가운데로'),
    _bar(2, '400G/레인', 0.5, '약 0.5m · 랙 안에서도 안 닿는다'),
    '<line x1="%d" y1="34" x2="%d" y2="206" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>'
    % (_BX0 + _BW, _BX0 + _BW, INK3),
    _lt(_BX0 + _BW - 60, 222, '랙 높이 2m', 't-sm', False),
]))


# ── 도해 2. 플러거블 → NPO → CPO — 광엔진이 칩에 가까워진다 ─────────
# 같은 꼴 셋. 값은 SD-0807 L43-46(손실 dB · 비트당 pJ). 칩 상자와 광엔진 상자 사이 거리가
# 전기 경로 길이다 — 셋 다 같은 판 폭 안에서 광엔진만 왼쪽으로 온다.
def _ladder(i, name, gap, loss, pj, accent=False):
    y = 34 + i * 92
    chip = (20, y, 96, 56)
    oe = (20 + 96 + gap, y, 96, 56)
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    return ''.join([
        _lt(20, y - 8, name, 't-sm', True),
        _box(*chip, lines=['스위치 칩']),
        _a(chip[0] + chip[2], y + 28, oe[0], y + 28),
        (_fill(*oe, st=st, sw=sw) if accent else _box(*oe, lines=[])),
        _t(oe[0] + 48, y + 24, '광엔진', 't-lab'),
        _t(oe[0] + 48, y + 44, '빛으로'),
        _lt(470, y + 22, loss, 't-sm', True),
        _lt(470, y + 42, pj, 't-sm', False),
    ])


FIG_LADDER = _svg(W, 296, '플러거블에서 CPO까지 — 전기 경로가 짧아질수록 손실과 전력이 준다', ''.join([
    _ladder(0, '플러거블 트랜시버 (앞판 케이지까지 PCB 배선)', 240, '손실 약 35dB', '20~25pJ/bit'),
    _ladder(1, 'NPO (칩 옆 기판, 소켓)', 110, '손실 약 15~20dB', '약 10pJ/bit'),
    _ladder(2, 'CPO (한 패키지 안)', 14, '손실 약 6dB', '5pJ/bit 미만', accent=True),
]))


# ── 도해 3. 트랜시버 한 개 — 누가 무엇을 맡나 ──────────────────────
# 같은 모듈을 줄마다 한 번씩 그리고 그 줄의 주체가 맡는 부품만 짙게(확정 규칙 「누가 무엇을 맡나」).
_PARTS = [('DSP · 드라이버', 'TIA'), ('레이저', 'InP'), ('광섬유', '연결부'), ('조립', '케이블')]


def _module(i, who, dark):
    y = 36 + i * 84
    cells = _row(4, y, 52, 118, gap=8)
    out = [_lt(18, y - 8, who, 't-sm', True)]
    for k, (c, lab) in enumerate(zip(cells, _PARTS)):
        if k == dark:
            out.append(_fill(*c, st=INK, sw=2.0))
        else:
            out.append(_box(*c, lines=[]))
        out.append(_t(c[0] + c[2] // 2, c[1] + 22, lab[0], 't-sm'))
        out.append(_t(c[0] + c[2] // 2, c[1] + 40, lab[1], 't-sm'))
    return ''.join(out)


FIG_MODULE = _svg(W, 272, '광 트랜시버 한 개를 세 주체가 나눠 만든다', ''.join([
    _module(0, '반도체 — 브로드컴 · 마벨 (미국)', 0),
    _module(1, '레이저 — 루멘텀 · 코히어런트 (미국 공장)', 1),
    _module(2, '조립 — 이노라이트 · 이옵토링크 (중국 · 태국)', 3),
]))


# ── 도해 4. 전력 — 800G 한 개에서 트랜시버와 CPO ───────────────────
# 값은 CPO북 L152. 막대 높이는 값에 비례(17W = 136px). 범위는 위 끝.
def _vbar(x, base, h, lab1, lab2, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    return ''.join([
        '<rect x="%d" y="%d" width="88" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="%s"/>'
        % (x, base - h, h, 'var(--sunk)' if accent else 'none', st, sw),
        _t(x + 44, base - h - 8, lab1, 't-sm'),
        _t(x + 44, base + 20, lab2, 't-sm'),
    ])


_BASE = 190
FIG_POWER = _svg(W, 232, '800G 한 개 — 트랜시버와 CPO 광엔진의 전력', ''.join([
    _lt(18, 18, '800G 한 개 (와트)', 't-sm', True),
    _vbar(196, _BASE, 136, '16~17W', 'DSP 트랜시버'),
    _vbar(356, _BASE, 40, '4~5W', 'CPO 광엔진+레이저', accent=True),
]))


# ── 도해 4a. 비중 — 클러스터에서 모듈까지, 광 부품이 차지하는 것 ─────────
# 막대 하나가 100% 이고 짙은 조각이 그 줄의 대상이다. 값은 CPO북 L112·L151·L154·L366.
# 안에 든 조각(트랜시버)은 원문이 「네트워킹의 60%」로 준 것이라 네트워킹 조각 안에서 60% 로 그린다 —
# 클러스터 대비 몇 % 인지는 원문에 없으니 적지 않는다.
_SX, _SW, _SH = 176, 440, 38


def _sbar(i, name, outer, outer_lab, inner=None, inner_lab='', inner_of_outer=True):
    y = 40 + i * 64
    out = [_lt(18, y + 24, name, 't-sm', True),
           '<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" stroke="%s" stroke-width="1.5"/>'
           % (_SX, y, _SW, _SH, INK3)]
    ow = int(_SW * outer / 100.0)
    out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="var(--sunk)" stroke="%s" stroke-width="2"/>'
               % (_SX, y, ow, _SH, INK))
    if inner is not None:
        iw = int((ow if inner_of_outer else _SW) * inner / 100.0)
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" fill-opacity="0.35" stroke="none"/>'
                   % (_SX, y, iw, _SH, INK3))
        out.append(_lt(_SX + ow + 10, y + 15, outer_lab, 't-sm', True))
        out.append(_lt(_SX + ow + 10, y + 31, inner_lab, 't-sm', False))
    else:
        out.append(_lt(_SX + ow + 10, y + 24, outer_lab, 't-sm', True))
    return ''.join(out)


FIG_SHARE = _svg(W, 310, '광 부품이 차지하는 비중 — 클러스터에서 모듈까지', ''.join([
    _lt(_SX, 26, '막대 하나 = 100%', 't-sm', False),
    _sbar(0, '클러스터 총비용', 15, '네트워킹 15%', 60, '그중 트랜시버 60% (짙은 조각)'),
    _sbar(1, '클러스터 총전력', 9, '네트워킹 9%', 17 / 435 * 100, '그중 광트랜시버 17MW / 435MW', inner_of_outer=False),
    _sbar(2, '트랜시버 한 개 전력', 50, 'DSP 약 50%'),
    _sbar(3, '트랜시버 자재비', 30, 'DSP 20~30% (위 끝)'),
]))


# ── 도해 5. 엔비디아 로드맵 — 랙 안은 구리, 랙 사이만 빛 ────────────
# 같은 크기 상자 셋. 값은 GTC26 L423-424 · LI-2607 L553. 점선 = 아직 없는 것.
_RM = _row(3, 44, 108, 196, gap=16)


def _rack(c, head, l1, l2, l3, dash=False, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    extra = ' stroke-dasharray="6 4"' if dash else ''
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" stroke-width="%s"%s/>'
        % (c[0], c[1], c[2], c[3], st, sw, extra),
        _t(c[0] + 98, c[1] + 26, head, 't-lab'),
        _t(c[0] + 98, c[1] + 50, l1),
        _t(c[0] + 98, c[1] + 70, l2),
        _t(c[0] + 98, c[1] + 90, l3),
    ])


FIG_ROADMAP = _svg(W, 190, '엔비디아 스케일업 — 어디까지 구리인가', ''.join([
    _lt(_RM[0][0], 28, '루빈 (2026~)', 't-sm', True),
    _lt(_RM[1][0], 28, '루빈 울트라', 't-sm', True),
    _lt(_RM[2][0], 28, '파인만', 't-sm', True),
    _rack(_RM[0], 'NVL72', '랙 하나', '전부 구리', '양방향 SerDes 448G'),
    _rack(_RM[1], 'NVL576', '오베론 랙 8개', '랙 안 구리', '랙 사이 CPO 소량', accent=True),
    _rack(_RM[2], 'NVL1152', '카이버 랙 8개', '랙 안 ?', '랙 사이 CPO', dash=True),
    _a(_RM[0][0] + _RM[0][2], 98, _RM[1][0], 98),
    _a(_RM[1][0] + _RM[1][2], 98, _RM[2][0], 98),
    _lt(18, 176, '점선 = 로드맵만 있는 것', 't-sm', False),
]))


# ── 도해 6. 랙을 넘는 세 방식 — 엔비디아 · 화웨이 · 구글 ─────────────
# 같은 꼴 셋. 값은 화웨이 L84·L112·L140, TPU L292·L317, GTC26 L423.
_S3 = _row(3, 44, 130, 196, gap=16)


def _way(c, head, lines, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    out = [('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" stroke-width="%s"/>'
            % (c[0], c[1], c[2], c[3], st, sw)),
           _t(c[0] + 98, c[1] + 26, head, 't-lab')]
    for k, s in enumerate(lines):
        out.append(_t(c[0] + 98, c[1] + 50 + k * 20, s))
    return ''.join(out)


FIG_THREE = _svg(W, 188, '랙 하나를 넘는 스케일업 — 세 회사의 세 답', ''.join([
    _lt(_S3[0][0], 28, '엔비디아 GB200', 't-sm', True),
    _lt(_S3[1][0], 28, '화웨이 CloudMatrix 384', 't-sm', True),
    _lt(_S3[2][0], 28, '구글 TPUv7', 't-sm', True),
    _way(_S3[0], 'NVL72 · 랙 하나', ['직결 구리 백플레인', '스케일업 트랜시버 0', '약 145kW']),
    _way(_S3[1], '랙 16개 · 칩 384', ['400G 트랜시버 6,912개', 'GPU당 7개 물량 투입', '약 600kW']),
    _way(_S3[2], '큐브 64 × OCS', ['큐브 안 구리 · 경계 광', 'TPU당 트랜시버 1.5개', '최대 9,216개'], accent=True),
]))


# ── 도해 7. 엔비디아 CPO 공급망 — 끝에서 끝까지 ─────────────────────
# 다섯 단계는 CPO북 L952-955. 상자 크기는 전부 같다(사슬은 한 크기).
_CH = _row(5, 44, 108, 116, gap=8)
_CH_TXT = [('레이저 · ELS', '루멘텀', '코히어런트', ''),
           ('FAU', 'TFC Optical', 'Senko', 'FOCI'),
           ('셔플박스', 'MPO 커넥터', 'T&S · 코닝', 'US Conec'),
           ('광엔진 패키징', 'TSMC COUPE', 'ASE · 패브리넷', 'Shunsin'),
           ('E/O 시험', '키사이트', 'Ficontec', '테라다인')]
FIG_CHAIN = _svg(W, 166, '엔비디아 CPO 공급망 다섯 단계 — 단계마다 이미 소수다', ''.join(
    [_lt(18, 28, '원문이 세운 다섯 단계 (2026-01)', 't-sm', True)]
    + [''.join([
        (_fill(*c, st=INK, sw=2.0) if i == 1 else _box(*c, lines=[])),
        _t(c[0] + 58, c[1] + 26, h, 't-lab'),
        _t(c[0] + 58, c[1] + 50, l1),
        _t(c[0] + 58, c[1] + 70, l2),
        _t(c[0] + 58, c[1] + 90, l3),
    ]) for i, (c, (h, l1, l2, l3)) in enumerate(zip(_CH, _CH_TXT))]
    + [_a(_CH[i][0] + _CH[i][2], 98, _CH[i + 1][0], 98) for i in range(4)]
    + []
))


# ── 도해 4b. 돈 — 스위치 한 대의 광 부품값과 클러스터 총비용 ────────────
# 값은 CPO북 L190-192. 왼쪽 세 막대는 Q3450 급 스위치 한 대의 광 부품값(천 달러), 오른쪽 둘은
# 클러스터 총비용 절감(%). 범위 값은 위 끝으로 그리고 캡션에 그렇게 적는다.
_CB = 190


def _cbar(x, h, lab1, lab2, accent=False, dash=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    extra = ' stroke-dasharray="6 4"' if dash else ''
    return ''.join([
        '<rect x="%d" y="%d" width="88" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="%s"%s/>'
        % (x, _CB - h, h, 'var(--sunk)' if accent else 'none', st, sw, extra),
        _t(x + 44, _CB - h - 8, lab1, 't-sm'),
        _t(x + 44, _CB + 20, lab2, 't-sm'),
    ])


# 왼쪽 눈금: 9만 달러 = 136px. 오른쪽 눈금: 10% = 136px.
def _kd(v):
    return int(136 * v / 90.0)


def _pc(v):
    return int(136 * v / 10.0)


FIG_COST = _svg(W, 232, '광 부품값은 절반인데 클러스터 총비용은 3~7%만 준다', ''.join([
    _lt(18, 18, '스위치 한 대의 광 부품값 (천 달러)', 't-sm', True),
    _cbar(24, _kd(72), '72', '트랜시버'),
    _cbar(136, _kd(40), '35~40', 'CPO 원가', accent=True),
    _cbar(248, _kd(90), '80~90', '마진 얹은 CPO', dash=True),
    '<line x1="352" y1="10" x2="352" y2="220" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' % INK3,
    _lt(372, 18, '클러스터 총비용 절감', 't-sm', True),
    _cbar(384, _pc(3), '3%', '3층망 그대로'),
    _cbar(504, _pc(7), '7%', '2층으로 평탄화', accent=True),
]))
