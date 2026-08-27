# -*- coding: utf-8 -*-
"""엔비디아 밸류에이션 리포트 도해 넷.

값은 전부 근거가 있다 — 재무 숫자는 SEC 10-K·10-Q(insights/valuation/NVDA/facts.json),
경로와 역산 결과는 우리가 돌린 계산(scratchpad/nvda_cases.py)이다. 후자는 우리 값이라
캡션에 그렇게 적는다(insight-figure 규칙 1).

막대 높이와 길이도 값이다. 넷 다 실제 수치에 비례하고 눈금은 아래 함수가 계산한다 —
손으로 찍지 않는다(규칙 2). 판 위에는 막대만 두고 숫자는 막대 밖에 세운다(규칙 3).
"""
import gen_sudoremove_dashboard as sudo
import nvda_cases as nc

_svg, _lt, _t, _r = sudo._svg, sudo._lt, sudo._t, sudo._r

W = 640


# ── 도해 ① 영업이익률이 두 번 무너졌다 ──────────────────────────
# 시계열 막대. 사이클을 명시적 기간에 통째로 담아야 하는 근거가 여기 있다 —
# 회계연도 2020년과 2023년에 이익률이 반 토막 아래로 내려갔다.

_YEARS = [str(y) for y in range(2016, 2027)]
_MARG = [(y, nc.c['ebit'][y]['val'] / nc.c['revenue'][y]['val'] * 100)
         for y in _YEARS if y in nc.c['ebit'] and y in nc.c['revenue']]
_MARG.append(('TTM', nc.EBIT0 / nc.REV0 * 100))

_M_MAX = 70.0        # 눈금 상한(%). 최근 12개월 65.2% 가 들어가야 한다
_M_H = 108           # 상한에 해당하는 픽셀 높이
_M_BASE = 168        # 막대가 서는 바닥 y
_M_X0 = 44
_M_W = 36
_M_GAP = 13
# 이익률이 직전 해보다 15%포인트 넘게 내려간 해를 강조한다. 눈으로 고르지 않는다.
_DROP = {_MARG[i][0] for i in range(1, len(_MARG)) if _MARG[i][1] - _MARG[i - 1][1] < -15}


def _mbar(i, label, v):
    x = _M_X0 + i * (_M_W + _M_GAP)
    h = int(round(v / _M_MAX * _M_H))
    y = _M_BASE - h
    hot = label in _DROP or label == 'TTM'
    col = 'var(--accent)' if hot else 'var(--ink-3)'
    out = ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"/>'
           % (x, y, _M_W, h, col, 0.85 if hot else 0.38)]
    if hot:
        out.append(_t(x + _M_W // 2, y - 8, '%.1f' % v, 't-sm'))
    out.append(_t(x + _M_W // 2, _M_BASE + 17, label[-2:] if label != 'TTM' else 'TTM', 't-sm'))
    return ''.join(out)


FIG_CYCLE = _svg(W, 236, '영업이익률이 두 번 무너졌다', ''.join(
    [_lt(_M_X0, 34, '영업이익률 (%) — 회계연도별, 맨 오른쪽은 최근 12개월')]
    + [_mbar(i, lab, v) for i, (lab, v) in enumerate(_MARG)]
    + [_r(_M_X0, _M_BASE, (_M_W + _M_GAP) * len(_MARG) - _M_GAP, 1, 'var(--ink-3)', 1),
       _lt(_M_X0, _M_BASE + 44, '강조한 해는 직전 해보다 이익률이 15%포인트 넘게 내려간 해다',
           bold=False),
       _lt(_M_X0, _M_BASE + 63, '회계연도 2020년 매출은 7% 줄었고 2023년은 제자리였다',
           bold=False)]))


# ── 도해 ② 매출에서 현금까지 네 단계 ────────────────────────────
# 순위 막대. 세후영업이익과 잉여현금흐름 사이가 벌어지는 자리를 보인다.

_F_X, _F_W = 168, 400
_F_MAX = nc.REV0
_F_ROWS = [('매출', nc.REV0, ''),
           ('영업이익', nc.EBIT0, '매출의 %.1f%%' % (nc.EBIT0 / nc.REV0 * 100)),
           ('세후영업이익', nc.NOPAT0, '실효세율 %.1f%%' % (nc.TAXR * 100)),
           ('잉여현금흐름', nc.FCF0, '매출의 %.1f%%' % (nc.MARGIN0 * 100))]


def _fbar(i, name, v, note):
    y = 54 + i * 34
    w = int(round(v / _F_MAX * _F_W))
    hot = i == 3
    col = 'var(--accent)' if hot else 'var(--ink-3)'
    return ''.join([
        '<text x="%d" y="%d" text-anchor="end" class="t-lab">%s</text>' % (_F_X - 12, y + 16, name),
        '<rect x="%d" y="%d" width="%d" height="21" fill="%s" opacity="%.2f"/>'
        % (_F_X, y, w, col, 0.85 if hot else 0.38),
        '<text x="%d" y="%d" class="t-sm">%.0f%s</text>'
        % (_F_X + w + 8, y + 16, v, ('  ' + note) if note else ''),
    ])


FIG_FUNNEL = _svg(W, 232, '세후영업이익과 잉여현금흐름 사이가 벌어진다', ''.join(
    [_lt(40, 34, '최근 12개월 (10억 달러) — %s 종료' % nc.TTM_END)]
    + [_fbar(i, n, v, note) for i, (n, v, note) in enumerate(_F_ROWS)]
    + [_lt(40, 208, '차이 %.0f억 달러는 설비투자 %.0f억과 운전자본에 묶인 돈이다 — '
                    '매출채권과 재고가 반년 사이 %.0f억 늘었다'
           % ((nc.NOPAT0 - nc.FCF0) * 10, nc.t['capex']['val'] / nc.B * 10,
              (nc.NWC0 - nc.NWC_PREV) * 10), bold=False)]))


# ── 도해 ③ 케이스 셋과 현재가 ───────────────────────────────────

_C_X, _C_MAXW = 96, 452
_CV = {n: nc.value(n)['per_share'] for n in nc.ORDER}
if nc.cons_case():
    _CV[nc.CONS_NAME] = nc.value(nc.CONS_NAME)['per_share']
_C_MAXV = 240.0


def _cbar(y, name, v, accent=False):
    w = int(round(v / _C_MAXV * _C_MAXW))
    col = 'var(--accent)' if accent else 'var(--ink-3)'
    return ''.join([
        '<text x="%d" y="%d" text-anchor="end" class="t-lab">%s</text>' % (_C_X - 12, y + 17, name),
        '<rect x="%d" y="%d" width="%d" height="22" fill="%s" opacity="%.2f"/>'
        % (_C_X, y, w, col, 0.85 if accent else 0.4),
        '<text x="%d" y="%d" class="t-sm">%.0f</text>' % (_C_X + w + 8, y + 17, v),
    ])


_PRICE_X = _C_X + int(round(nc.PRICE / _C_MAXV * _C_MAXW))

_C_ROWS = [('Bear', False), ('Base', False), ('Bull', True)] + (
    [(nc.CONS_NAME, False)] if nc.cons_case() else [])
_C_BOT = 52 + 32 * len(_C_ROWS)

FIG_CASE = _svg(W, _C_BOT + 100, '경로 넷이 모두 현재가 아래에 선다', ''.join(
    [_lt(40, 34, '주당가치 (달러) — 우리 세 경로와 애널리스트 컨센서스')]
    + [_cbar(52 + 32 * i, n, _CV[n], accent=hot) for i, (n, hot) in enumerate(_C_ROWS)]
    + ['<path d="M%d 44 V%d" stroke="var(--accent)" stroke-width="2" '
       'stroke-dasharray="5 4" fill="none"/>' % (_PRICE_X, _C_BOT),
       _lt(40, _C_BOT + 28, '점선은 %s 종가 %.2f달러다' % (nc.PRICE_DAY, nc.PRICE), bold=False),
       _lt(40, _C_BOT + 48, '컨센서스 막대는 애널리스트 %d명·%d명의 회계연도 매출 추정치를 '
           '1년차에 넣은 것이다'
           % (nc._cons_fy() and [q['analysts'] for q in nc.CONS['periods'] if q['period'] == '0y'][0],
              [q['analysts'] for q in nc.CONS['periods'] if q['period'] == '+1y'][0]), bold=False),
       _lt(40, _C_BOT + 68, '가장 후한 Bull 도 %.0f%% 아래에 선다'
           % abs((_CV['Bull'] / nc.PRICE - 1) * 100), bold=False)]))


# ── 도해 ④ 시장가가 요구하는 현금 ───────────────────────────────
# 순위 막대 셋. 지금 · 우리 Base 10년째 · 시장가를 받치는 데 필요한 금액.

_G10 = nc.dcf.implied_growth(nc.FCF0, nc.WACC_BASE, 0.0275, 10, nc.MCAP, nc.NET_DEBT)
_NEED = nc.FCF0 * (1 + _G10) ** 10
_BASE10 = nc.path(nc.CASES['Base'])[-1][3]

_N_X, _N_W = 190, 296
_N_ROWS = [('지금 (최근 12개월)', nc.FCF0, False),
           ('우리 Base 10년째', _BASE10, False),
           ('시장가가 요구하는 값', _NEED, True)]


def _nbar(i, name, v, hot):
    y = 56 + i * 38
    w = int(round(v / _NEED * _N_W))
    col = 'var(--accent)' if hot else 'var(--ink-3)'
    return ''.join([
        '<text x="%d" y="%d" text-anchor="end" class="t-lab">%s</text>' % (_N_X - 12, y + 17, name),
        '<rect x="%d" y="%d" width="%d" height="22" fill="%s" opacity="%.2f"/>'
        % (_N_X, y, w, col, 0.85 if hot else 0.38),
        '<text x="%d" y="%d" class="t-sm">%s억 달러</text>'
        % (_N_X + w + 8, y + 17, format(int(round(v * 10)), ',')),
    ])


FIG_NEED = _svg(W, 226, '시장가는 10년 뒤 현금을 여덟 배로 요구한다', ''.join(
    [_lt(40, 34, '10년 뒤 잉여현금흐름 — 할인율 %.2f%%, 영구성장률 2.75%% 기준'
         % (nc.WACC_BASE * 100))]
    + [_nbar(i, n, v, hot) for i, (n, v, hot) in enumerate(_N_ROWS)]
    + [_lt(40, 190, '맨 아래는 %s 시가총액을 정당화하려면 얼마가 필요한지를 되돌린 값이다 — '
                    '해마다 %.1f%%씩 열 해다' % (nc.PRICE_DAY, _G10 * 100), bold=False),
       _lt(40, 210, '지금의 %.1f배이고 우리 Base 경로 마지막 해의 %.1f배다'
           % (_NEED / nc.FCF0, _NEED / _BASE10), bold=False)]))


# ── 도해 ⑤ 상대가치 축 ──────────────────────────────────────────
# 순위 막대. 비교 회사 묶음을 어떻게 고르느냐에 따라 함의 주가가 어디까지 벌어지는지를
# 보인다. 회계사 판의 필자가 리노공업 편에서 세운 축이고, 값은 우리가 뜬 컨센서스다.

_IM = nc.implied_by_multiple()

if _IM:
    _M_EPS, _M_OWN, _M_GR = _IM
    _MX, _MW = 176, 268
    _MMAX = max(px for _l, _a, px in _M_GR)

    def _mbar2(i, lab, avg, px):
        y = 56 + i * 34
        w = int(round(px / _MMAX * _MW))
        return ''.join([
            '<text x="%d" y="%d" text-anchor="end" class="t-sm">%s</text>'
            % (_MX - 12, y + 16, lab),
            '<rect x="%d" y="%d" width="%d" height="21" fill="var(--ink-3)" opacity="0.42"/>'
            % (_MX, y, w),
            '<text x="%d" y="%d" class="t-sm">%.0f달러 · %.1f배</text>'
            % (_MX + w + 8, y + 16, px, avg),
        ])

    _M_PX = _MX + int(round(nc.PRICE / _MMAX * _MW))
    _M_BOT = 56 + 34 * len(_M_GR)

    FIG_MULT = _svg(W, _M_BOT + 82, '비교 대상을 어떻게 고르느냐가 결론을 가른다', ''.join(
        [_lt(40, 34, '엔비디아 차기 추정 주당순이익 %.2f달러에 비교 회사 배수를 댄 값'
             % _M_EPS)]
        + [_mbar2(i, lab, avg, px) for i, (lab, avg, px) in enumerate(_M_GR)]
        + ['<path d="M%d 48 V%d" stroke="var(--accent)" stroke-width="2" '
           'stroke-dasharray="5 4" fill="none"/>' % (_M_PX, _M_BOT),
           _lt(40, _M_BOT + 26, '점선은 %s 종가 %.2f달러다. 엔비디아 자신의 선행 배수는 '
               '%.1f배다' % (nc.PRICE_DAY, nc.PRICE, _M_OWN), bold=False),
           _lt(40, _M_BOT + 46, '회계연도 끝이 회사마다 달라 같은 달을 재는 것이 아니다',
               bold=False)]))
else:
    FIG_MULT = None
