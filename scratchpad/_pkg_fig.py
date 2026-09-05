# -*- coding: utf-8 -*-
"""보고서 ⑦ 선단 패키징 층의 도해 열하나. 색은 회색만(확정 규칙 S2) — 강조는 짙은 테두리 하나.

값은 전부 원문에 있는 것만 그린다. 도형 개수도 값이라, 다이 개수·접합 횟수처럼 셀 수 있는
것은 원문이 센 수와 같게 그리고 아니면 캡션에 그렇게 적는다(insight-figure 규칙 1).
좌표는 _row 와 아래 눈금 함수가 계산하고 손으로 찍지 않는다(규칙 2).
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
_elbow = bf._elbow
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _fill(x, y, w, h, st=INK3, sw=1.5, rx=8):
    """옅은 회색 채움 상자 — 그 그림이 고른 자리 한 곳에만 쓴다."""
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="var(--sunk)" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, st, sw))


def _plain(x, y, w, h, st=INK3, sw=1.5, rx=4, dash=False):
    extra = ' stroke-dasharray="5 4"' if dash else ''
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, st, sw, extra))


# ── 도해 1. 레티클 한 장과 그 위에 놓이는 다이 수 ──────────────────────
# 값은 SD-0619 L25(26mm×33mm·858제곱밀리미터)·L27(다이 둘·넷)·L25(H100 이 한계에 닿음).
# 다이 개수 1·2·4 는 원문이 센 수다. 다이 상자는 26:33 비율을 지킨다.
_DW, _DH = 34, 43          # 레티클 한 장(26mm×33mm)을 그린 크기
_RC = _row(3, 46, 122, 196, gap=16)


def _pkg(c, head, n, note, accent=False):
    x, y, w, h = c
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    gx = 8
    tw = n * _DW + (n - 1) * gx
    x0, y0 = x + (w - tw) // 2, y + 38
    out = [_plain(x, y, w, h, st, sw, rx=8), _t(x + w // 2, y + 22, head, 't-lab')]
    for i in range(n):
        out.append(_fill(x0 + i * (_DW + gx), y0, _DW, _DH, INK, 1.6, rx=3))
    out.append(_t(x + w // 2, y + h - 10, note))
    return ''.join(out)


FIG_RETICLE = _svg(W, 214, '레티클 한 장이 다이의 최대 크기이고, 패키지는 그보다 커야 한다', ''.join([
    _lt(18, 22, '작은 사각형 하나 = 레티클 한 장 = 26mm × 33mm = 858제곱밀리미터', 't-sm', True),
    _lt(18, 40, '큰 테두리 = 패키지', 't-sm', False),
    _pkg(_RC[0], 'H100', 1, '다이 하나가 이미 한계'),
    _pkg(_RC[1], '그레이스 블랙웰', 2, '둘을 하나처럼'),
    _pkg(_RC[2], '루빈', 4, '넷을 붙이기로', accent=True),
    _a(_RC[0][0] + _RC[0][2], 107, _RC[1][0], 107),
    _a(_RC[1][0] + _RC[1][2], 107, _RC[2][0], 107),
    _lt(18, 206, '패키지 테두리 크기는 실제 배수에 비례하지 않는다', 't-sm', False),
]))


# ── 도해 2. CoWoS 세 갈래와 EMIB — 가운데 층을 무엇으로 두나 ────────────
# 같은 꼴 넷을 같은 자리에 그리고 가운데 층만 다르게(확정 규칙 「견줄 때는 같은 꼴」).
# 값은 SD-0619 L35·L37·L45. 층 이름은 원문 그대로.
_BC = _row(4, 60, 132, 142, gap=10)
_LH = 26                    # 층 하나의 높이


def _stack(c, head, mid_kind, note):
    """아래부터 기판·(인터포저)·칩. mid_kind ∈ si·rdl·bridge·none."""
    x, y, w, h = c
    cx = x + w // 2
    out = [_t(cx, y - 8, head, 't-lab')]
    chip_y = y + 8
    mid_y = chip_y + _LH + 6
    sub_y = mid_y + _LH + 6
    # 칩 둘 — 어느 갈래에서나 같은 자리
    cw = (w - 32) // 2
    out.append(_fill(x + 12, chip_y, cw, _LH, INK, 1.6, rx=3))
    out.append(_t(x + 12 + cw // 2, chip_y + 17, '칩', 't-sm'))
    out.append(_fill(x + 20 + cw, chip_y, cw, _LH, INK, 1.6, rx=3))
    out.append(_t(x + 20 + cw + cw // 2, chip_y + 17, '칩', 't-sm'))
    if mid_kind == 'none':
        out.append(_plain(x + 8, mid_y, w - 16, _LH, INK3, 1.2, rx=3, dash=True))
        out.append(_t(cx, mid_y + 17, '없음', 't-sm'))
    elif mid_kind == 'bridge':
        out.append(_plain(x + 8, mid_y, w - 16, _LH, INK3, 1.5, rx=3))
        out.append(_fill(cx - 26, mid_y + 5, 52, _LH - 10, INK, 1.8, rx=2))
        out.append(_t(cx, mid_y + 17, '브리지', 't-sm'))
    elif mid_kind == 'si':
        out.append(_fill(x + 8, mid_y, w - 16, _LH, INK, 1.8, rx=3))
        out.append(_t(cx, mid_y + 17, '실리콘', 't-sm'))
    else:
        out.append(_plain(x + 8, mid_y, w - 16, _LH, INK3, 1.5, rx=3))
        out.append(_t(cx, mid_y + 17, '유기 RDL', 't-sm'))
    # 기판 — EMIB 는 여기에 브리지가 박힌다
    out.append(_plain(x + 4, sub_y, w - 8, _LH, INK3, 1.5, rx=3))
    if mid_kind == 'none':
        out.append(_fill(cx - 26, sub_y + 5, 52, _LH - 10, INK, 1.8, rx=2))
        out.append(_t(cx, sub_y + 17, '브리지', 't-sm'))
    else:
        out.append(_t(cx, sub_y + 17, '기판', 't-sm'))
    out.append(_t(cx, sub_y + _LH + 20, note))
    return ''.join(out)


FIG_BRANCH = _svg(W, 226, 'CoWoS 세 갈래와 EMIB — 가운데 층을 무엇으로 두나', ''.join([
    _lt(18, 22, '아래부터 기판 · 가운데 층 · 칩. 짙은 칸이 실리콘이다', 't-sm', True),
    _stack(_BC[0], 'CoWoS-S', 'si', '가늘지만 비싸고'),
    _stack(_BC[1], 'CoWoS-R', 'rdl', '싸지만 열·습기에'),
    _stack(_BC[2], 'CoWoS-L', 'bridge', '필요한 데만 실리콘'),
    _stack(_BC[3], 'EMIB', 'none', '가운데 층을 뺀다'),
]))


# ── 도해 3. 원형 웨이퍼와 사각 패널 — 어디서 만드나 ─────────────────
# 값은 SD-0619 L47(500mm×500mm·300mm 웨이퍼), ECTC L597(320×320·600×600·300×300),
# ECTC L674·L722(510×515). 한 변 길이에 비례해 그리고 캡션에 그렇게 적는다.
_MM = 0.36                  # 1mm 를 몇 px 로 그릴지. 600mm 가 216px.
_PB = 268                   # 도형들이 서는 바닥선
_PX0 = 200                  # 패널 셋이 함께 쓰는 왼쪽 아래 모서리


def _panel(mm_w, mm_h, lab, who, accent=False):
    """왼쪽 아래 모서리를 맞춰 겹쳐 그린 사각 패널 하나. 크기 견줌은 겹쳐야 보인다."""
    w, h = int(mm_w * _MM), int(mm_h * _MM)
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    top = _PB - h
    return ''.join([
        _plain(_PX0, top, w, h, st, sw, rx=4),
        '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
        % (_PX0 + w, top, 438, top, INK3),
        _lt(444, top + 5, lab, 't-sm', accent),
        _lt(444, top + 21, who, 't-sm', False),
    ])


_PR = int(300 * _MM) // 2
FIG_PANEL = _svg(W, 340, '원형 웨이퍼에서 사각 패널로', ''.join([
    _lt(18, 22, '한 변 길이에 비례해 그렸고, 패널 셋은 왼쪽 아래 모서리를 맞춰 겹쳤다', 't-sm', True),
    '<circle cx="90" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.5"/>'
    % (_PB - _PR, _PR, INK3),
    _t(90, _PB + 22, '300mm 웨이퍼', 't-lab'),
    _t(90, _PB + 40, '원 안에서 사각형을'),
    _t(90, _PB + 56, '잘라 낸다'),
    _panel(600, 600, '600 × 600mm', 'ASE, 넷으로 나눠 조립', accent=True),
    _panel(510, 515, '510 × 515mm', '인텔 유리 패널'),
    _panel(320, 320, '320 × 320mm', 'Resonac 패널'),
]))


# ── 도해 4. 접합 피치 — 마이크로범프에서 하이브리드 본딩까지 ────────────
# 값은 ECTC L105-107(45·36/35·25µm), ISSCC L636(9µm), ECTC L559(450nm).
# 사다리는 순서만 보이고 간격에 비례하지 않는다 — 세 자릿수 차이라 비례로는 못 그린다.
def _rung(i, pitch, who, accent=False):
    y = 44 + i * 40
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    return ''.join([
        (_fill(150, y, 118, 28, st, sw, rx=5) if accent else _plain(150, y, 118, 28, st, sw, rx=5)),
        _t(209, y + 19, pitch, 't-lab'),
        _lt(284, y + 19, who, 't-sm', False),
    ])


FIG_PITCH = _svg(W, 262, '접합점 간격이 좁아지면서 붙이는 방법이 바뀐다', ''.join([
    _lt(18, 26, '마이크로범프', 't-sm', True),
    _rung(0, '45µm', '그래나이트 래피즈 EMIB'),
    _rung(1, '36 / 35µm', 'EMIB-T, 범프 밀도 +65%'),
    _rung(2, '25µm', 'EMIB-T 다음 목표. 여기부터 솔더 부피가 모자란다'),
    _lt(18, 186, '하이브리드 본딩', 't-sm', True),
    _rung(3, '9µm', '포베로스 다이렉트 M3DProc'),
    _rung(4, '450nm', '웨이퍼 대 웨이퍼, 연결 2,000만 개에 수율 98%', accent=True),
    _lt(18, 254, '위아래 간격은 순서만 보인다', 't-sm', False),
]))


# ── 도해 5. 층을 쌓으면 접합이 쌓인다 ─────────────────────────────
# 값은 HBM북 L279·L283-284(8층 7회 92% · 12층 11회 87%). 접합 표시 개수가 원문이 센 횟수다.
def _joins(y, layers, joins, pct):
    out = [_lt(18, y + 20, '%d층' % layers, 't-sm', True),
           _lt(72, y + 20, '접합 %d회' % joins, 't-sm', False)]
    for k in range(joins):
        out.append(_plain(160 + k * 26, y + 4, 18, 22, INK3, 1.5, rx=3))
    out.append(_lt(160 + joins * 26 + 14, y + 20, '스택 수율 약 %d%%' % pct, 't-sm', True))
    return ''.join(out)


FIG_YIELD = _svg(W, 176, '층당 99%가 쌓이면 스택 수율이 이렇게 내려간다', ''.join([
    _lt(18, 26, '네모 하나가 접합 한 번. 층 하나를 붙이는 수율을 99%로 잡았을 때다', 't-sm', True),
    _joins(46, 8, 7, 92),
    _joins(96, 12, 11, 87),
    _lt(18, 166, '실제로는 결함이 쌓여 이 계산보다 나쁘다', 't-sm', False),
]))


# ── 도해 6. TSMC 패키징 매출 — 애플이 만든 것을 엔비디아가 넘어섰다 ────────
# 값은 애플TSMC L790·L798-801(2018년 InFO 6억·CoWoS 1.18억, 2025년 CoWoS 96억),
# L298(2025년 InFO 84억)·L790(38억). 두 값이 원문 안에서 갈려 점선으로 함께 그린다.
_MB = 214                   # 막대 바닥선


def _mk(v):
    """억 달러 값이 놓이는 막대 높이. 96억 = 150px. 글자는 원문 표기 그대로 쓴다."""
    return int(150 * v / 96.0)


def _mbar(x, v, lab, name, accent=False, dash=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    extra = ' stroke-dasharray="6 4"' if dash else ''
    h = max(_mk(v), 2)
    return ''.join([
        '<rect x="%d" y="%d" width="76" height="%d" rx="5" fill="%s" stroke="%s" '
        'stroke-width="%s"%s/>' % (x, _MB - h, h, 'var(--sunk)' if accent else 'none', st, sw, extra),
        _t(x + 38, _MB - h - 8, lab, 't-sm'),
        _t(x + 38, _MB + 20, name, 't-sm'),
    ])


FIG_MONEY = _svg(W, 278, 'InFO 를 CoWoS 가 넘어섰다', ''.join([
    _lt(18, 22, '2018년', 't-sm', True),
    _mbar(56, 6, '6억', 'InFO'),
    _mbar(150, 1.18, '1억 1,800만', 'CoWoS'),
    '<line x1="272" y1="30" x2="272" y2="238" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' % INK3,
    _lt(292, 22, '2025년', 't-sm', True),
    _mbar(310, 38, '38억', 'InFO'),
    _mbar(404, 84, '84억', '같은 편 다른 대목', dash=True),
    _mbar(526, 96, '96억', 'CoWoS', accent=True),
    _lt(18, 270, '점선 = 같은 원문이 다른 곳에 적은 값', 't-sm', False),
]))


# ── 도해 7. EMIB 와 EMIB-T — 전력이 가는 길이 바뀐다 ──────────────────
# 값은 ECTC L144-146. 같은 꼴 둘, 화살표만 다르다(확정 규칙 「전후 변화」·「인과」).
_EC = _row(2, 52, 150, 268, gap=28)


def _emib(c, head, tsv, note):
    x, y, w, h = c
    cx = x + w // 2
    chip_y, sub_y = y + 26, y + 92
    out = [_t(cx, y + 16, head, 't-lab'),
           _fill(x + 20, chip_y, 90, 30, INK, 1.6, rx=3), _t(x + 65, chip_y + 20, '칩', 't-sm'),
           _fill(x + w - 110, chip_y, 90, 30, INK, 1.6, rx=3), _t(x + w - 65, chip_y + 20, '칩', 't-sm'),
           _plain(x + 8, sub_y, w - 16, 34, INK3, 1.5, rx=4),
           _lt(x + 16, sub_y + 21, '기판', 't-sm', False),
           _plain(cx - 40, sub_y + 6, 80, 22, INK, 1.8, rx=2), _t(cx, sub_y + 21, '브리지', 't-sm')]
    c1, c2 = x + 65, x + w - 65
    if tsv:
        # 브리지에서 곧장 올라가 칩 밑으로 꺾는다. 비스듬한 선은 검사기가 무는 자리다
        out.append(_elbow(cx - 20, sub_y + 6, c1, chip_y + 30))
        out.append(_elbow(cx + 20, sub_y + 6, c2, chip_y + 30))
    else:
        out.append(_a(c1, sub_y, c1, chip_y + 30))
        out.append(_a(c2, sub_y, c2, chip_y + 30))
    out.append(_t(cx, y + h + 4, note))
    return ''.join(out)


FIG_EMIBT = _svg(W, 240, '브리지에 구멍을 뚫자 전력이 곧장 올라간다', ''.join([
    _lt(18, 26, '화살표가 전력이 가는 길이다', 't-sm', True),
    _emib(_EC[0], 'EMIB', False, '브리지 옆으로 우회'),
    _emib(_EC[1], 'EMIB-T', True, '브리지에 TSV'),
]))


# ── 도해 8. 레티클 배수 — 두 방식이 어디까지 가나 ────────────────────
# 값은 SD-0619 L73. System on Wafer 40배는 시점이 확실치 않아 막대로 안 그리고 캡션에 적는다.
_MULB = 206


def _mux(v):
    """레티클 배수가 놓이는 막대 높이. 12배 = 150px."""
    return int(150 * v / 12.0)


def _mxbar(x, v, lab, name, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    h = _mux(v)
    return ''.join([
        '<rect x="%d" y="%d" width="70" height="%d" rx="5" fill="%s" stroke="%s" stroke-width="%s"/>'
        % (x, _MULB - h, h, 'var(--sunk)' if accent else 'none', st, sw),
        _t(x + 35, _MULB - h - 8, lab, 't-sm'),
        _t(x + 35, _MULB + 20, name, 't-sm'),
    ])


FIG_MULT = _svg(W, 250, '패키지가 레티클의 몇 배까지 가나', ''.join([
    _lt(18, 22, 'TSMC CoWoS', 't-sm', True),
    _mxbar(44, 3.3, '3.3배', '1세대'),
    _mxbar(130, 5.5, '5.5배', '루빈 세대'),
    _mxbar(216, 9.5, '9.5배', '다음 계획'),
    '<line x1="322" y1="30" x2="322" y2="230" stroke="%s" stroke-width="1" stroke-dasharray="4 4"/>' % INK3,
    _lt(342, 22, '인텔 EMIB-T', 't-sm', True),
    _mxbar(376, 8, '8배', '지금'),
    _mxbar(486, 12, '12배', '2028년', accent=True),
    _lt(18, 242, '그다음으로 거론되는 System on Wafer 40배는 시점이 확실치 않아 안 그렸다', 't-sm', False),
]))


# ── 도해 9. HBM4 베이스 다이 — 세 회사가 다른 공정을 골랐다 ──────────────
# 같은 모듈을 줄마다 한 번씩 그리고 그 회사가 바꾼 칸만 짙게(확정 규칙 「누가 무엇을 맡나」).
# 값은 ISSCC L96-98.
def _hbm(i, who, proc, note):
    y = 46 + i * 62
    x0 = 168
    out = [_lt(18, y + 32, who, 't-sm', True)]
    for k in range(4):                       # D램 코어 다이 넉 장 — 층수가 아니라 코어 다이 표시다
        out.append(_plain(x0, y + k * 9, 150, 8, INK3, 1.2, rx=2))
    out.append(_lt(x0 + 160, y + 16, 'D램 코어', 't-sm', False))
    out.append(_fill(x0, y + 38, 150, 20, INK, 2.0, rx=3))
    out.append(_t(x0 + 75, y + 52, proc, 't-sm'))
    out.append(_lt(x0 + 160, y + 52, note, 't-sm', False))
    return ''.join(out)


FIG_BASE = _svg(W, 250, 'HBM4 베이스 다이 — 짙은 칸을 누구 공정으로 굽나', ''.join([
    _lt(18, 26, '위가 D램 코어 다이, 아래 짙은 칸이 베이스 다이다', 't-sm', True),
    _hbm(0, '삼성', 'SF4', '자사 공정. 가장 앞서고 가장 비싸다'),
    _hbm(1, 'SK하이닉스', 'TSMC N12', '남의 저비용 로직 공정'),
    _hbm(2, '마이크론', '자체 CMOS', '가장 싸게'),
    _lt(18, 242, '코어 다이를 넉 장으로 그린 것은 표시용이고 실제 층수가 아니다', 't-sm', False),
]))


# ── 도해 10. 냉각 — 열계면 소재를 건너뛰면 어디까지 뽑나 ────────────────
# 값은 ECTC L387·L398-400·L407-409. 범위는 위 끝으로 그리고 캡션에 그렇게 적는다.
_CB = 200


def _kw(v):
    """kW 값이 놓이는 막대 높이. 5.3kW = 150px."""
    return int(150 * v / 5.3)


def _cbar(x, v, lab, n1, n2, accent=False):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    h = _kw(v)
    return ''.join([
        '<rect x="%d" y="%d" width="88" height="%d" rx="5" fill="%s" stroke="%s" stroke-width="%s"/>'
        % (x, _CB - h, h, 'var(--sunk)' if accent else 'none', st, sw),
        _t(x + 44, _CB - h - 8, lab, 't-sm'),
        _t(x + 44, _CB + 20, n1, 't-sm'),
        _t(x + 44, _CB + 36, n2, 't-sm'),
    ])


FIG_COOL = _svg(W, 258, '같은 시험차량에서 뽑아낸 열 (kW)', ''.join([
    _lt(18, 22, 'TSMC CoWoS-R 시험차량, SoC 다이 넷과 HBM 여덟', 't-sm', True),
    _cbar(120, 2.3, '1.9~2.3', '뚜껑형 냉각판', '분당 1~2리터'),
    _cbar(276, 3.0, '2.5~3.0', '뚜껑 없는 냉각판', '분당 4리터에서 포화'),
    _cbar(432, 5.3, '5.3', '실리콘에 새긴 미세기둥', '분당 8리터', accent=True),
    _lt(18, 250, '범위 값은 위 끝 높이로 그렸다', 't-sm', False),
]))


# ── 도해 11. HBM4 를 만드는 사슬 넷 ─────────────────────────────────
# 값은 HBM북 L885·L899-902. 상자 크기는 전부 같다(사슬은 한 크기).
_CH = _row(4, 52, 112, 140, gap=18)
_CH_TXT = [('베이스 다이 설계', '엔비디아 등', '가속기 회사가', '직접 그린다'),
           ('파운드리', 'TSMC N12', '삼성 SF4', '마이크론 자체'),
           ('D램 적층', 'SK하이닉스', '마이크론', '삼성'),
           ('패키지 조립', 'TSMC CoWoS', '인텔 EMIB', 'ASE · SPIL · 앰코')]
FIG_CHAIN = _svg(W, 194, 'HBM4 한 덩어리가 손을 네 번 바꾼다', ''.join(
    [_lt(18, 26, '설계와 굽기와 쌓기와 붙이기가 다 다른 회사다', 't-sm', True)]
    + [''.join([
        (_fill(*c, st=INK, sw=2.0) if i == 3 else _plain(*c, st=INK3, sw=1.5, rx=8)),
        _t(c[0] + c[2] // 2, c[1] + 26, h, 't-lab'),
        _t(c[0] + c[2] // 2, c[1] + 52, l1),
        _t(c[0] + c[2] // 2, c[1] + 72, l2),
        _t(c[0] + c[2] // 2, c[1] + 92, l3),
    ]) for i, (c, (h, l1, l2, l3)) in enumerate(zip(_CH, _CH_TXT))]
    + [_a(_CH[i][0] + _CH[i][2], 108, _CH[i + 1][0], 108) for i in range(3)]
    + [_lt(18, 186, '메모리 3사의 TSV 구조가 서로 달라 한 베이스 다이는 다른 회사 HBM 에 안 맞는다',
           't-sm', False)]
))
