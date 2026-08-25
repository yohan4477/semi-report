# -*- coding: utf-8 -*-
"""알파벳 밸류에이션 리포트 도해 셋.

값은 전부 근거가 있다 — 재무 숫자는 SEC 10-K·10-Q(insights/valuation/GOOGL/facts.json),
케이스 결과는 우리가 돌린 계산(scratchpad/googl_cases.py)이다. 후자는 우리 값이라
캡션에 그렇게 적는다(insight-figure 규칙 1).

막대 높이·길이도 값이다. 셋 다 실제 수치에 비례하고, 눈금은 아래 _px 가 계산한다 —
손으로 찍지 않는다(규칙 2). 판 위에는 막대만 두고 숫자는 막대 밖에 세운다(규칙 3).
"""
import gen_sudoremove_dashboard as sudo

_svg, _box, _a, _lt, _t, _r = (sudo._svg, sudo._box, sudo._a,
                               sudo._lt, sudo._t, sudo._r)

W = 640


# ── 도해 ① 기준연도를 언제로 잡느냐 ─────────────────────────────
# 좌우 대비다. 매출과 영업이익률은 올랐는데 잉여현금흐름은 줄었다 —
# 「조건은 좋아졌는데 결과가 뒤집혔다」를 보이는 자리라 같은 눈금 막대 둘씩을 세운다.

_B_MAX = 140.0      # 막대 눈금 상한(10억 달러). CapEx TTM 132.4 가 들어가야 한다
_B_H = 104          # 상한에 해당하는 픽셀 높이
_B_BASE = 178       # 막대가 서는 바닥 y


def _px(v):
    """10억 달러 값을 막대 높이(픽셀)로. 눈금은 두 패널이 공유한다."""
    return int(round(v / _B_MAX * _B_H))


def _bar(x, w, v, label, accent=False):
    """바닥에서 위로 자란 막대 하나 + 값(막대 위) + 이름(막대 아래)."""
    h = _px(v)
    y = _B_BASE - h
    col = 'var(--accent)' if accent else 'var(--ink-3)'
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"/>'
        % (x, y, w, h, col, 0.85 if accent else 0.42),
        _t(x + w // 2, y - 7, '%.1f' % v),
        _t(x + w // 2, _B_BASE + 16, label, 't-sm'),
    ])


def _panel(x0, title, sub, capex, fcf, mark_fcf):
    """패널 하나 — 제목 두 줄과 막대 둘(CapEx·FCF)."""
    return ''.join([
        _lt(x0, 40, title),
        _lt(x0, 57, sub, bold=False),
        _bar(x0 + 12, 62, capex, 'CapEx'),
        _bar(x0 + 100, 62, fcf, 'FCF', accent=mark_fcf),
    ])


FIG_BASE = _svg(W, 232, '기준연도를 어디로 잡느냐가 잉여현금흐름을 뒤집는다', ''.join([
    _panel(30, 'FY2025', '2025-12-31 종료', 91.4, 73.3, False),
    _panel(360, 'TTM', '2026-06-30 기준', 132.4, 53.3, True),
    # 두 패널을 가르는 선. 판 위에 글자를 얹지 않으려고 선만 둔다
    '<path d="M320 34 V196" stroke="var(--line)" stroke-width="1.5" fill="none"/>',
    _r(30, _B_BASE, 580, 1, 'var(--ink-3)', 1),
    _lt(30, 216, '매출 402.8 → 445.9 · 영업이익률 32.0% → 33.1% · 단위 10억 달러', bold=False),
]))


# ── 도해 ② 순이익을 왜 못 쓰나 ──────────────────────────────────
# 구성 막대 하나. 세전이익을 둘로 가르면 영업 밖이 절반을 넘는다.

_S_X, _S_W, _S_Y, _S_H = 40, 560, 74, 46
_S_TOTAL = 299.3


def _seg(x0, v, lines, accent=False):
    w = int(round(v / _S_TOTAL * _S_W))
    col = 'var(--accent)' if accent else 'var(--ink-3)'
    out = ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"/>'
           % (x0, _S_Y, w, _S_H, col, 0.8 if accent else 0.4)]
    for i, s in enumerate(lines):
        out.append(_t(x0 + w // 2, _S_Y + _S_H + 22 + i * 16, s, 't-lab' if i == 0 else 't-sm'))
    return ''.join(out), x0 + w


_seg1, _x1 = _seg(_S_X, 147.6, ['영업이익 147.6', '장사로 번 것'])
_seg2, _x2 = _seg(_x1, 151.6, ['영업 밖 151.6', '그중 지분 평가이익 149.0'], accent=True)

FIG_NI = _svg(W, 216, '세전이익의 절반이 장사 밖에서 왔다', ''.join([
    _lt(40, 46, '세전이익 299.3 (최근 12개월, 10억 달러)'),
    _seg1, _seg2,
    _lt(40, 200, '지분 평가이익은 보유 주식을 다시 매긴 금액이라 현금이 들어오지 않는다', bold=False),
]))


# ── 도해 ③ 케이스 셋과 현재가 ───────────────────────────────────
# 순위 막대. 우리가 돌린 세 경로와 시장가를 같은 눈금에 둔다.

_C_X, _C_MAXV, _C_MAXW = 96, 360.0, 468


def _cbar(y, name, v, note, accent=False):
    w = int(round(v / _C_MAXV * _C_MAXW))
    col = 'var(--accent)' if accent else 'var(--ink-3)'
    return ''.join([
        '<text x="%d" y="%d" text-anchor="end" class="t-lab">%s</text>' % (_C_X - 12, y + 17, name),
        '<rect x="%d" y="%d" width="%d" height="22" fill="%s" opacity="%.2f"/>'
        % (_C_X, y, w, col, 0.85 if accent else 0.4),
        '<text x="%d" y="%d" class="t-sm">%s</text>' % (_C_X + w + 8, y + 17, note),
    ])


_PRICE_X = _C_X + int(round(346.96 / _C_MAXV * _C_MAXW))

FIG_CASE = _svg(W, 216, '케이스 셋이 모두 현재가 아래에 선다', ''.join([
    _lt(40, 34, '주당가치 (달러) — 우리가 돌린 세 경로'),
    _cbar(52, 'Bear', 131, '131'),
    _cbar(84, 'Base', 185, '185'),
    _cbar(116, 'Bull', 261, '261', accent=True),
    # 현재가 세로선. 막대와 같은 눈금이라 자리를 계산해서 건다
    '<path d="M%d 44 V148" stroke="var(--accent)" stroke-width="2" '
    'stroke-dasharray="5 4" fill="none"/>' % _PRICE_X,
    _lt(40, 176, '점선은 2026-08-25 종가 346.96달러다', bold=False),
    _lt(40, 196, '가장 후한 Bull 도 25% 아래에 선다', bold=False),
]))
