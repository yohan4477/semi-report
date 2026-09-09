# -*- coding: utf-8 -*-
"""메르 흐름 장의 도해 셋. 색은 회색만 — 강조는 짙은 테두리 하나.

값은 전부 원문에 있는 것만 쓴다(yohan-figure 규칙 1). 막대 개수도 값이다 —
유류세 일곱 칸은 원문이 센 여섯 번의 변경에 처음 값을 더한 수이고, 환매 세 건은
원문이 든 펀드 수다. 없는 칸을 채우지 않는다.

자리는 눈금 함수 _x·_h 가 계산한다. 손으로 찍지 않는다(규칙 2).
"""
import _biz_fig as bf

_svg, _box, _a, _lt = bf._svg, bf._box, bf._a, bf._lt
_t, _r = bf.sudo._t, bf.sudo._r
W = 640
INK, INK3, ACC = 'var(--ink)', 'var(--ink-3)', 'var(--accent)'


# ── 1절. 한도와 실제가 벌어진 자리 ────────────────────────────────
_X0, _XMAX, _XW = 118, 32.0, 452        # 눈금 왼쪽 끝 · 상한(%) · 폭


def _x(v):
    """비중 v(%)가 놓이는 x 좌표. 막대 끝도 한도선도 전부 이 함수만 쓴다."""
    return _X0 + _XW * v / _XMAX


def _cap_row(y, when, cap, cap_lab):
    """실제 보유 29.7% 막대 하나와 그 위에 선 한도선."""
    return ''.join([
        _lt(14, y + 20, when, bold=False),
        '<rect x="%d" y="%d" width="%.1f" height="26" rx="3" fill="var(--sunk)" '
        'stroke="%s" stroke-width="1.5"/>' % (_X0, y, _x(29.7) - _X0, INK3),
        '<path d="M%.1f %d V%d" stroke="%s" stroke-width="2.2"/>'
        % (_x(cap), y - 8, y + 34, ACC),
        _t(int(_x(cap)), y - 14, cap_lab, 't-sm'),
    ])


FIG_CAP = _svg(W, 200, '허용 상한이 실제 보유를 못 따라가자 상한을 옮겼다', ''.join([
    _lt(14, 26, '국민연금 국내 주식 비중'),
    _cap_row(62, '2026년 5월', 19.9, '허용 19.9%'),
    _lt(int(_x(29.7)) + 8, 82, '실제 29.7%', bold=False),
    _cap_row(140, '목표를 고친 뒤', 28.8, '허용 28.8%'),
    _lt(int(_x(29.7)) + 8, 160, '실제 29.7%', bold=False),
    _lt(14, 192, '막대 길이는 보유 비중에 비례한다. 두 줄의 막대는 같은 값이고 한도선만 옮겼다',
        bold=False),
]))


# ── 2절. 깎아 주던 폭이 계단으로 줄었다 ──────────────────────────
_FUEL = [('37%', 37, ''), ('25%', 25, '24-06'), ('20%', 20, '24-10'),
         ('15%', 15, '25-04'), ('10%', 10, '25-10'), ('7%', 7, '25-11'),
         ('0%', 0, '25-12')]
_FB, _FMAX, _FH = 150, 37.0, 96         # 바닥 y · 상한(%) · 최대 높이


def _fh(v):
    return _FH * v / _FMAX


def _fuel_bar(i, lab, v, when):
    cells = bf._row(len(_FUEL), 0, 0, 62, gap=12)
    x = cells[i][0]
    y = _FB - _fh(v)
    out = [_t(x + 31, 168, when, 't-sm')] if when else []
    if v:
        out.append('<rect x="%d" y="%.1f" width="62" height="%.1f" rx="3" fill="var(--sunk)" '
                   'stroke="%s" stroke-width="%s"/>'
                   % (x, y, _fh(v), ACC if i == 0 else INK3, 1.8 if i == 0 else 1.5))
        out.append(_t(x + 31, y - 8, lab, 't-sm'))
    else:
        out.append('<path d="M%d %d H%d" stroke="%s" stroke-width="1.5" '
                   'stroke-dasharray="4 4"/>' % (x, _FB, x + 62, INK3))
        out.append(_t(x + 31, _FB - 8, lab, 't-sm'))
    return ''.join(out)


FIG_FUEL = _svg(W, 196, '유류세 깎아 주던 폭이 여섯 번에 걸쳐 0이 됐다', ''.join(
    [_lt(14, 26, '유류세 인하율')]
    + [_fuel_bar(i, lab, v, when) for i, (lab, v, when) in enumerate(_FUEL)]
    + ['<path d="M%d %d H%d" stroke="%s" stroke-width="1.2"/>' % (60, _FB, 600, INK3),
       _lt(14, 190, '맨 왼쪽이 줄이기 전이고 날짜가 없다. 마지막 칸은 인하가 끝난 자리다',
           bold=False)]))


# ── 5절. 계약 한도와 실제 요청 ───────────────────────────────────
_RQ = [('블랙록', 9.3), ('클리프워터', 14.0), ('블랙스톤', 7.9)]
_RB, _RMAX, _RH = 148, 14.0, 92


def _rh(v):
    return _RH * v / _RMAX


def _req_bar(i, name, v):
    cells = bf._row(len(_RQ), 0, 0, 96, gap=28)
    x = cells[i][0]
    y = _RB - _rh(v)
    return ''.join([
        '<rect x="%d" y="%.1f" width="96" height="%.1f" rx="3" fill="var(--sunk)" '
        'stroke="%s" stroke-width="1.5"/>' % (x, y, _rh(v), INK3),
        _t(x + 48, y - 8, '%s%%' % ('%g' % v), 't-sm'),
        _t(x + 48, 166, name, 't-sm'),
    ])


FIG_REDEEM = _svg(W, 196, '계약은 5%인데 요청이 그 선을 넘었다', ''.join(
    [_lt(14, 26, '2026년 3월 사모대출 환매 요청')]
    + [_req_bar(i, n, v) for i, (n, v) in enumerate(_RQ)]
    + ['<path d="M%d %.1f H%d" stroke="%s" stroke-width="2.2" stroke-dasharray="6 4"/>'
       % (60, _RB - _rh(5.0), 600, ACC),
       # 라벨은 첫 막대 왼쪽 빈자리에 둔다. 오른쪽에 두면 셋째 막대에 깔린다
       _lt(62, int(_RB - _rh(5.0)) - 6, '계약 한도 5%', bold=False),
       '<path d="M%d %d H%d" stroke="%s" stroke-width="1.2"/>' % (60, _RB, 600, INK3),
       _lt(14, 190, '막대 높이는 요청 비율에 비례한다. 클리프워터는 7%만 돌려줬고 블랙스톤은 '
           '한도를 7%로 늘렸다', bold=False)]))
