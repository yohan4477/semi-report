# -*- coding: utf-8 -*-
"""엔비디아 DCF 를 Bear/Base/Bull 셋으로 돌린다. 검토용 계산이라 scratchpad 에 둔다.

알파벳 편(googl_cases.py)과 경로 만드는 법이 다르다. 알파벳은 성장률을 선형으로
내리는 H-모델이면 됐지만 엔비디아는 룰북 R15 가 걸린다 — 사이클 산업은 한 사이클을
통째로 명시적 기간에 담아야 한다. 오르는 구간만 담고 끝내면 호황기 마진이 영구가치로
그대로 넘어간다.

그래서 성장률과 마진을 해마다 손으로 적는다. 선형 감소로는 「몇 해 뒤에 한 번 꺾이고
다시 오른다」를 못 그린다. 엔비디아 실적에 그 꺾임이 두 번 찍혀 있다 — 회계연도
2020년 매출 -7%, 2023년 0%, 그때 영업이익률이 37.3%에서 15.7%로 내려갔다.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'insights'))
import dcf

B = 1e9
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(root, 'insights/valuation/NVDA/facts.json'), encoding='utf-8'))
c = d['sec']['concepts']
t = d['sec']['ttm']

REV0 = t['revenue']['val'] / B
FCF0 = (t['ocf']['val'] - t['capex']['val']) / B
MARGIN0 = FCF0 / REV0
EBIT0 = t['ebit']['val'] / B
TAXR = t['tax_expense']['val'] / t['pretax_income']['val']
NOPAT0 = EBIT0 * (1 - TAXR)
NWC0 = (t['receivables']['val'] + t['inventory']['val'] - t['payables']['val']) / B
NWC_PREV = (c['receivables']['2026']['val'] + c['inventory']['2026']['val']
            - c['payables']['2026']['val']) / B
NET_DEBT = (t['lt_debt']['val'] + t['st_debt']['val']
            - t['cash']['val'] - t['st_investments']['val']) / B
SHARES = d['sec']['shares_outstanding']['val'] / B
SHARES_DIL = d['sec']['shares_diluted']['val'] / B
PRICE = d['market']['price']
PRICE_DAY = d['market']['as_of'][:10]
MCAP = d['market']['market_cap'] / B
TTM_END = t['revenue']['end']

RF = d['risk_free']['rate']
BETA = d['beta']['beta']
MRP = 0.046
KD_PRE = 0.045
KE = RF + BETA * MRP
DEBT = (t['lt_debt']['val'] + t['st_debt']['val']) / B
DEBT_W = DEBT / (DEBT + MCAP)
WACC = KE * (1 - DEBT_W) + KD_PRE * (1 - TAXR) * DEBT_W

# 케이스마다 할인율을 다르게 준다. 회계사 판의 필자가 리노공업 편(2026-03-08)에서
# 쓴 방식이다 — 보수 9.5% · 기준 8.5% · 공격 7.5% 로 구간화하고, 근거를 순현금 ·
# 고마진 · 높은 자본수익률로 적었다. 현재가를 정당화하는 6%대 후반은 「역산 수준」
# 이라 배제했다.
#
# 우리는 그 폭을 비율로 옮긴다. 자본자산가격결정모형이 낸 값을 보수 자리에 두고,
# 기준은 그 89%, 공격은 79% 다. 룰북이 비워 둔 칸(W3)을 채우는 것이라 「필자 룰
# 아님」으로 표시한다 — 산식이 아니라 실례에서 옮긴 값이다.
BAND = {'Bear': 1.0, 'Base': 8.5 / 9.5, 'Bull': 7.5 / 9.5}


def wacc_of(name):
    """케이스 이름에 맞는 할인율. 모르는 이름은 기준 자리로 본다."""
    return WACC * BAND.get(name, BAND['Base'])


WACC_BASE = WACC * BAND['Base']     # 기준 경로 할인율. 본문이 가장 자주 부른다

def band_is_circular(name):
    """그 케이스의 할인율이 「역산 수준」에 닿았나.

    필자가 리노공업 편에서 세운 가드다. 현재 주가를 정당화하는 할인율(6%대 후반)을
    「역산 수준」이라 부르고 시나리오에서 배제했다. 우리 구간이 그 선을 넘으면 값이
    스스로 서는 것이 아니라 주가가 자기를 정당화하는 것이므로 본문이 그렇게 밝힌다.
    """
    ir = dcf.implied_discount_rate([r[3] for r in path(CASES[name])],
                                   CASES[name]['g'], MCAP, NET_DEBT)
    return bool(ir) and wacc_of(name) <= ir



YEAR0 = 2027   # 표의 첫 열. 최근 12개월(2026-07 종료)에서 한 해 뒤 12개월이다

# 해마다 (매출 성장률, 잉여현금흐름 마진). 열 해가 한 사이클이다 —
# 상승 · 조정 · 회복 · 성숙 순서로 읽는다.
# 1년차는 우리가 고르지 않는다. 회사가 낸 3분기 가이던스 1,080억 달러(중국 제외)를
# 기준점으로 쓴다. 그 뒤 세 분기를 제자리로 두면 다음 12개월 매출이 4,320억이고
# 최근 12개월 대비 +43% 다. 처음에는 +25% 로 적었는데, 그 값은 이미 발표된 분기와
# 가이던스에 어긋나는 숫자였다. Bear 는 가이던스만 채우고 그 뒤 바로 식는 경우,
# Bull 은 분기마다 5%씩 더 나가는 경우다.
GUIDE_Q3 = 108.0        # 회계연도 2027년 3분기 가이던스(중국 제외)
GUIDE_Q2 = 96.22        # 회계연도 2027년 2분기 실적

CASES = {
    'Bear': dict(g=0.0225,
                 rows=[(0.35, 0.38), (0.04, 0.34), (-0.25, 0.24), (-0.10, 0.21),
                       (0.06, 0.24), (0.07, 0.26), (0.05, 0.27), (0.04, 0.27),
                       (0.03, 0.27), (0.03, 0.27)],
                 why='가이던스까지는 채우고 그 뒤 바로 식는다. 자체 칩이 하이퍼스케일러 '
                     '물량을 크게 떼어 가고 조정이 두 해 깊게 온다'),
    'Base': dict(g=0.0275,
                 rows=[(0.43, 0.40), (0.18, 0.39), (0.08, 0.37), (-0.10, 0.29),
                       (-0.04, 0.27), (0.12, 0.31), (0.09, 0.32), (0.07, 0.32),
                       (0.06, 0.32), (0.05, 0.32)],
                 why='3분기 가이던스 뒤 세 분기가 제자리이고, 상승이 두 해 더 이어진 뒤 '
                     '소화 국면을 한 번 지나 가속기 시장 성장률로 내려앉는다'),
    'Bull': dict(g=0.0325,
                 rows=[(0.54, 0.42), (0.26, 0.42), (0.16, 0.41), (0.08, 0.40),
                       (-0.02, 0.35), (0.14, 0.38), (0.11, 0.38), (0.09, 0.38),
                       (0.07, 0.38), (0.06, 0.38)],
                 why='가이던스 뒤로도 분기마다 5%씩 더 나가고, 추론 수요가 학습 수요를 '
                     '이어받아 상승이 네 해로 늘며 조정이 한 해로 그친다'),
}
ORDER = ('Bear', 'Base', 'Bull')

# ── 넷째 경로 — 컨센서스 ────────────────────────────────────────────
# 「우리 가정이 보수적이라 값이 낮게 나오는가」를 독자가 직접 가르게 하는 자리다.
# 야후가 주는 애널리스트 추정치는 회계연도 둘까지다(0y·+1y). 우리 표는 최근
# 12개월에서 한 해씩 굴린 창이라 회계연도와 반년 어긋나므로, 이웃한 두 회계연도를
# 평균해 우리 창에 맞춘다. 그 뒤로는 컨센서스가 없으므로 Base 경로를 그대로 잇는다.
# 마진도 Base 와 같게 둔다 — 이 케이스가 묻는 것은 매출 하나다.
CONS = d.get('consensus')


def _cons_fy():
    """컨센서스 회계연도 매출 둘. (이번 회계연도, 다음 회계연도) 단위는 10억 달러."""
    if not CONS:
        return None
    got = {p['period']: p for p in CONS['periods']}
    if '0y' not in got or '+1y' not in got:
        return None
    return got['0y']['revenue'] / B, got['+1y']['revenue'] / B


def _cons_rows():
    """컨센서스 케이스의 연도별 (성장률, 마진). 못 받으면 None."""
    fy = _cons_fy()
    if not fy:
        return None
    y1 = (fy[0] + fy[1]) / 2          # 우리 1년차 창이 두 회계연도에 걸친다
    base = CASES['Base']['rows']
    rows = [((y1 / REV0) - 1, base[0][1]),
            (CONS_Y2, base[1][1])] + list(base[2:])
    return rows


# 2년차는 컨센서스가 안 준다. 다음 회계연도 성장률 45.0% 에서 우리가 내린 값이고,
# 이 한 칸만 우리 가정이다. 본문이 그렇게 밝힌다.
CONS_Y2 = 0.30
CONS_NAME = '컨센서스'


def cons_case():
    rows = _cons_rows()
    if not rows:
        return None
    return dict(g=CASES['Base']['g'], rows=rows,
                why='애널리스트 평균 추정치를 1년차에 그대로 넣고, 그 뒤는 Base 경로를 잇는다')

# 감도표 축. 할인율은 우리 값을 가운데 두고 ±2%포인트를 1%포인트씩 흔든다.
SENS_R = [round(WACC_BASE + x, 6) for x in (-0.02, -0.01, 0.0, 0.01, 0.02)]
SENS_G = [0.0175, 0.0225, 0.0275, 0.0325, 0.0375]

# 필자 엘곰이 옮긴 SimplyWall.st 2단계 FCFE 모형(2025-03-07 편).
# 값은 그 글에 있는 것을 그대로 옮긴다 — 우리가 고치지 않는다.
EL = dict(rate=0.0848, g=0.0275, shares=24.4, per_share=127.19, price_then=117.30,
          years=[(2025, 64.585), (2026, 98.643), (2027, 127.386), (2028, 144.661),
                 (2029, 163.448), (2030, 193.089), (2031, 213.243), (2032, 230.582),
                 (2033, 245.609), (2034, 258.840)],
          pv_explicit=1048.332, pv_tv=2055.053, equity=3103.385)
EL_REST = [v for y, v in EL['years'] if y >= 2028]


def tv_multiple(g, r=None):
    """영구가치가 마지막 해 잉여현금흐름의 몇 배인가. (1+g)/(r-g).

    본문이 이 배수를 드러내는 이유는 여기서 시장과 갈리기 때문이다. 우리 잣대는
    마지막 해 현금흐름의 열 배 아래로 그 뒤 영원을 사는 셈인데, 시장은 지금 잉여
    현금흐름의 마흔 배를 낸다. 할인율과 영구성장률을 따로 말하면 이 사실이 안 보인다.
    """
    r = WACC_BASE if r is None else r
    return (1 + g) / (r - g)


def price_multiple():
    """시장이 지금 내는 배수. 시가총액을 최근 12개월 잉여현금흐름으로 나눈다."""
    return MCAP / FCF0


def path(case):
    """연도별 (연도, 매출, 마진, 잉여현금흐름)."""
    rows, rev = [], REV0
    for i, (g, m) in enumerate(case['rows']):
        rev *= 1 + g
        rows.append((YEAR0 + i, rev, m, rev * m))
    return rows


def value(name):
    case = CASES[name] if name in CASES else cons_case()
    return dcf.value([r[3] for r in path(case)], wacc_of(name), case['g'], NET_DEBT, SHARES)


def implied_r(name):
    case = CASES[name] if name in CASES else cons_case()
    return dcf.implied_discount_rate([r[3] for r in path(case)], case['g'], MCAP, NET_DEBT)


def report():
    """콘솔로 결과를 찍는다. import 하는 쪽이 값만 쓰도록 함수에 넣었다."""
    print('기준 (최근 12개월 %s) 매출 %.1fB · 잉여현금흐름 %.1fB · 마진 %.1f%%'
          % (TTM_END, REV0, FCF0, MARGIN0 * 100))
    print('영업이익 %.1fB (%.1f%%) · 실효세율 %.1f%% · 세후영업이익 %.1fB'
          % (EBIT0, EBIT0 / REV0 * 100, TAXR * 100, NOPAT0))
    print('순운전자본 %.1fB (직전 회계연도말 %.1fB, %+.1fB)' % (NWC0, NWC_PREV, NWC0 - NWC_PREV))
    print('주가 $%.2f (%s) · 시총 %.0fB · 순현금 %.1fB · 주식수 %.3fB'
          % (PRICE, PRICE_DAY, MCAP, -NET_DEBT, SHARES))
    print('Ke %.2f%% (Rf %.2f%% + 베타 %.3f x MRP %.1f%%) · 부채비중 %.2f%% · WACC %.2f%%\n'
          % (KE * 100, RF * 100, BETA, MRP * 100, DEBT_W * 100, WACC * 100))
    print('케이스별 할인율 ' + ' · '.join('%s %.2f%%' % (n, wacc_of(n) * 100) for n in ORDER))

    print('%-6s %9s %8s %8s %9s %8s %7s' % ('케이스', '주당가치', '괴리', 'TV비중',
                                            '10년매출', '10년FCF', '내재r'))
    for name in ORDER:
        v = value(name)
        rows = path(CASES[name])
        print('%-6s %8.0f$ %7.0f%% %7.0f%% %9.0f %8.0f %6.2f%%'
              % (name, v['per_share'], (v['per_share'] / PRICE - 1) * 100,
                 v['tv_share'] * 100, rows[-1][1], rows[-1][3], (implied_r(name) or 0) * 100))

    print('\nBase 연도별 경로')
    print('%6s %9s %8s %8s' % ('연도', '매출B', '마진', 'FCF B'))
    for y, rev, m, f in path(CASES['Base']):
        print('%6d %9.0f %7.1f%% %8.0f' % (y, rev, m * 100, f))

    print('\n역산 — 시장가를 정답으로 놓으면')
    for r in (WACC_BASE, 0.12, 0.10):
        g10 = dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT)
        print('  할인율 %.2f%% -> 10년 균등 성장률 %.2f%% · 10년 뒤 잉여현금흐름 %.0fB (지금의 %.1f배)'
              % (r * 100, g10 * 100, FCF0 * (1 + g10) ** 10, (1 + g10) ** 10))

    print('\n민감도 (Base 경로, 할인율 x 영구성장률) — 주당 $')
    fcfs = [r[3] for r in path(CASES['Base'])]
    grid = dcf.sensitivity(fcfs, SENS_R, SENS_G, NET_DEBT, SHARES)
    print('%8s' % 'r/g' + ''.join('%8.2f%%' % (g * 100) for g in SENS_G))
    for r in SENS_R:
        print('%7.2f%%' % (r * 100) + ''.join('%9.0f' % grid[(r, g)] for g in SENS_G))


def _googl_tv():
    """알파벳 편의 영구가치 배수. 그쪽 할인율이 움직이면 여기도 따라온다 —
    두 편이 같은 화면에 서므로 한쪽만 옛 값을 들고 있으면 비교가 어긋난다."""
    import googl_cases as gcs
    return (1 + gcs.CASES['Base']['g']) / (gcs.WACC - gcs.CASES['Base']['g'])


PAIR_R = None   # 표에 세울 할인율 축. 아래에서 채운다


def rate_growth_pairs():
    """같은 주가를 만드는 (할인율, 10년 균등 성장률) 짝.

    역산에는 미지수가 둘인데 방정식이 하나다. 주가 하나로는 「할인율이 낮다」와
    「성장 기대가 크다」를 못 가른다. 값 하나를 골라 「시장이 틀렸다」고 쓰는 대신
    선을 통째로 싣는다 — 독자가 자기 할인율을 골라 읽는다.
    """
    ir = implied_r('Base') or 0.06
    out = []
    for r in sorted({round(ir, 4), 0.08, 0.10, 0.12, round(WACC_BASE, 4), round(WACC, 4)}):
        g = dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT)
        if g is None:
            continue
        out.append((r, g, FCF0 * (1 + g) ** 10))
    return out


def terminal_uplift(name='Base'):
    """역산 셋째 방식 — 영구 현금흐름을 얼마나 올려야 지금 주가가 나오나.

    필자가 리노공업 편에서 쓴 셋째 축이다. 할인율만 조정하는 방식과 성장만 조정하는
    방식에 더해, 명시적 기간은 그대로 두고 마지막 해 현금흐름만 올려 본다.

    돌려주는 것은 (필요한 마지막 해 잉여현금흐름, 우리 경로 대비 배수).
    """
    rows = path(CASES[name])
    r, g = wacc_of(name), CASES[name]['g']
    fcfs = [x[3] for x in rows]
    n = len(fcfs)
    pv_exp = dcf.pv_explicit(fcfs, r)
    target_ev = MCAP + NET_DEBT
    need_pv_tv = target_ev - pv_exp
    if need_pv_tv <= 0:
        return None
    need_tv = need_pv_tv * (1 + r) ** n
    need_last = need_tv * (r - g) / (1 + g)
    return need_last, need_last / fcfs[-1]


def multiples():
    """상대가치 재료. scripts/fetch_multiples.py 가 떠 둔 파일을 읽는다."""
    fp = os.path.join(root, 'insights/valuation/_multiples.json')
    if not os.path.exists(fp):
        return None
    return json.load(open(fp, encoding='utf-8'))


def multiple_rows():
    """(티커, 이름, 선행 주가수익비율, 회계연도말, 애널리스트 수). 배수 없는 곳은 뺀다."""
    m = multiples()
    if not m:
        return []
    out = []
    for t, name in m['names'].items():
        r = m['rows'].get(t, {})
        ny = r.get('next_year') or {}
        if ny.get('fwd_per'):
            out.append((t, name, ny['fwd_per'], ny['end'], ny['analysts']))
    return sorted(out, key=lambda x: -x[2])


def implied_by_multiple():
    """비교 회사 배수를 엔비디아 추정 주당순이익에 대면 주가가 얼마인가.

    필자가 리노공업 편에서 한 것과 같다 — 비교 대상을 어떻게 고르느냐가 결론을
    가른다는 것을 보이려고 묶음별로 낸다.
    """
    m = multiples()
    if not m:
        return None
    eps = ((m['rows'].get('NVDA') or {}).get('next_year') or {}).get('eps')
    if not eps:
        return None
    per = {t: v for t, _n, v, _e, _a in multiple_rows()}
    # 라벨은 짧게 둔다. 도해 왼쪽 자리가 좁아 길면 판 밖으로 나간다 —
    # 어느 회사가 든 묶음인지는 본문이 적는다.
    groups = [('AMD 하나', ['AMD']),
              ('브로드컴·TSMC', ['AVGO', 'TSM']),
              ('성장 비교군 셋', ['AMD', 'AVGO', 'TSM']),
              ('메모리까지 넷', ['AMD', 'AVGO', 'TSM', 'MU']),
              ('인텔까지 다섯', ['AMD', 'AVGO', 'TSM', 'MU', 'INTC'])]
    out = []
    for lab, ts in groups:
        vs = [per[t] for t in ts if t in per]
        if not vs:
            continue
        avg = sum(vs) / len(vs)
        out.append((lab, avg, avg * eps))
    return eps, per.get('NVDA'), out


def beta_grid_rows():
    """베타 격자를 (창, 간격, 베타, 관측수) 로 편다. 없으면 빈 목록."""
    g = d.get('beta_grid') or {}
    rows = []
    for w in ('52주', '2년', '5년'):
        for i in ('일간', '주간', '월간'):
            k = '%s %s' % (w, i)
            if k in g:
                rows.append((w, i, g[k]['beta'], g[k]['n']))
    return rows


def _two(v):
    """10억 달러 값을 두 표기로 낸다. 본문이 「억 달러」로 쓰므로 둘 다 적어야 대조된다."""
    e = v * 10
    return '%.1f (%s억 · %s억)' % (v, format(e, ',.1f'), format(int(round(e)), ','))


def write_facts():
    """check_report 가 대조할 사실표. 손으로 옮기지 않고 계산에서 바로 만든다."""
    L = ['# 엔비디아 밸류에이션 사실표 — 기계 대조용', '',
         '자동 생성이다. `python scratchpad/nvda_cases.py` 가 다시 쓴다. 손으로 고치지 않는다.',
         '', '## SEC 제출서류에서 받은 값', '']
    for k, name in (('revenue', '매출'), ('ebit', '영업이익'), ('ocf', '영업현금흐름'),
                    ('capex', '설비투자'), ('dna', '감가상각비'), ('net_income', '순이익'),
                    ('pretax_income', '세전이익'), ('tax_expense', '세금비용'),
                    ('nonoperating', '영업 밖 손익'), ('receivables', '매출채권'),
                    ('inventory', '재고자산'), ('payables', '매입채무')):
        for fy in ('2024', '2025', '2026'):
            if k in c and fy in c[k]:
                L.append('- FY%s %s %s' % (fy, name, _two(c[k][fy]['val'] / B)))
        if k in t:
            L.append('- 최근 12개월 %s %s' % (name, _two(t[k]['val'] / B)))
    L += ['- 최근 12개월 잉여현금흐름 %s' % _two(FCF0),
          '- 최근 12개월 잉여현금흐름 마진 %.1f%%' % (MARGIN0 * 100),
          '- 최근 12개월 영업이익률 %.1f%%' % (EBIT0 / REV0 * 100),
          '- 최근 12개월 실효세율 %.1f%%' % (TAXR * 100),
          '- 최근 12개월 세후영업이익 %s' % _two(NOPAT0),
          '- 세후영업이익이 매출에서 차지하는 몫 %.1f%%' % (NOPAT0 / REV0 * 100),
          '- 세후영업이익과 잉여현금흐름의 차이 %s' % _two(NOPAT0 - FCF0),
          # 기준 기간을 만드는 계산이 한 번 틀렸다. 본문 절 3이 그 값을 적으므로
          # 대조할 자리를 여기 남긴다 — 고치기 전 값이지 실적이 아니다.
          '- 고치기 전 최근 12개월 매출 %s' % _two(217.53),
          '- 순운전자본 %s' % _two(NWC0),
          '- 직전 회계연도말 순운전자본 %s' % _two(NWC_PREV),
          '- 반년 사이 순운전자본 증가 %s' % _two(NWC0 - NWC_PREV),
          '- 장기차입금 %s' % _two(t['lt_debt']['val'] / B),
          '- 직전 회계연도말 장기차입금 %s' % _two(c['lt_debt']['2026']['val'] / B),
          '- 반년 사이 장기차입금 증가 %s' % _two(t['lt_debt']['val'] / B - c['lt_debt']['2026']['val'] / B),
          '- 순현금 %s' % _two(-NET_DEBT),
          '- 설비투자 대비 감가상각 배수 %.2f' % (t['capex']['val'] / t['dna']['val']),
          '- 설비투자가 매출에서 차지하는 몫 %.1f%%' % (t['capex']['val'] / t['revenue']['val'] * 100),
          '- 주가 %.2f' % PRICE,
          '- 시가총액 %s' % _two(MCAP),
          '- 발행주식수 %.3f' % SHARES,
          '- 희석주식수 %.3f' % SHARES_DIL,
          '- 무위험수익률 %.2f%%' % (RF * 100),
          '- 베타 %.3f' % BETA,
          '- 베타 관측일수 %d' % d['beta']['n_days'],
          '- 기준기간 종료일 %s' % TTM_END,
          '- 주가 기준일 %s' % PRICE_DAY]
    for fy in ('2020', '2022', '2023', '2024', '2025', '2026'):
        if fy in c['revenue']:
            prev = c['revenue'].get(str(int(fy) - 1))
            L.append('- FY%s 매출 %s · 영업이익률 %.1f%%%s'
                     % (fy, _two(c['revenue'][fy]['val'] / B),
                        c['ebit'][fy]['val'] / c['revenue'][fy]['val'] * 100,
                        (' · 매출 성장률 %.0f%%' % ((c['revenue'][fy]['val'] / prev['val'] - 1) * 100))
                        if prev else ''))
    L += ['', '## 우리가 돌린 계산', '',
          '- 자기자본비용 %.2f%%' % (KE * 100),
          '- 시장위험프리미엄 %.1f%%' % (MRP * 100),
          '- 세전 타인자본비용 %.1f%%' % (KD_PRE * 100),
          '- 부채 비중 %.2f%%' % (DEBT_W * 100),
          '- 자본자산가격결정모형이 낸 할인율 %.2f%%' % (WACC * 100),
          '- 케이스별 할인율 보수 %.2f%% · 기준 %.2f%% · 공격 %.2f%%'
          % tuple(wacc_of(n) * 100 for n in ORDER),
          '- 할인율 %.2f%%' % (WACC_BASE * 100),
          '- 기준 자리가 자본자산가격결정모형 값의 %.0f%%' % (BAND['Base'] * 100),
          '- 공격 자리가 그 값의 %.0f%%' % (BAND['Bull'] * 100),
          '- 명시적 기간 10년',
          '- 민감도 할인율 축 %s' % ' '.join('%.2f%%' % (r * 100) for r in SENS_R),
          '- 민감도 영구성장률 축 %s' % ' '.join('%.2f%%' % (g * 100) for g in SENS_G)]
    for name in ORDER:
        v = value(name)
        rows = path(CASES[name])
        L.append('- %s 주당가치 %.0f · 현재가 대비 %.0f%% · 영구가치비중 %.0f%% · '
                 '영구성장률 %.2f%% · 10년째 매출 %s · 10년째 잉여현금흐름 %s · '
                 '매출 연평균 성장률 %.1f%% · 내재 할인율 %.2f%%'
                 % (name, v['per_share'], (v['per_share'] / PRICE - 1) * 100,
                    v['tv_share'] * 100, CASES[name]['g'] * 100,
                    _two(rows[-1][1]), _two(rows[-1][3]),
                    ((rows[-1][1] / REV0) ** 0.1 - 1) * 100, (implied_r(name) or 0) * 100))
    base = path(CASES['Base'])
    disc = [1 / (1 + WACC_BASE) ** i for i in range(1, len(base) + 1)]
    for (y, rev, m, f), ds in zip(base, disc):
        L.append('- %d 표기값 매출 %.0f · 잉여현금흐름 %.0f · 할인계수 %.4f · 현재가치 %.0f'
                 % (y, rev, f, ds, f * ds))
    for y, rev, m, f in base:
        L.append('- %d 매출 %s · 잉여현금흐름 마진 %.1f%% · 잉여현금흐름 %s'
                 % (y, _two(rev), m * 100, _two(f)))
    _prev = REV0
    for y, rev, m, f in base:
        L.append('- %d 매출 성장률 %.1f%%' % (y, (rev / _prev - 1) * 100))
        _prev = rev
    L.append('- Base 명시적 기간 현재가치 합 %s'
             % _two(sum(f * ds for (_y, _r, _m, f), ds in zip(base, disc))))
    grid = dcf.sensitivity([r[3] for r in base], SENS_R, SENS_G, NET_DEBT, SHARES)
    L.append('- 민감도 최고 %.0f · 최저 %.0f' % (max(grid.values()), min(grid.values())))
    L += ['- 영구가치 배수 Bear %.1f배 · Base %.1f배 · Bull %.1f배'
          % tuple(tv_multiple(CASES[n]['g']) for n in ORDER),
          '- 시장이 내는 배수 %.1f배' % price_multiple(),
          '- 영구가치 배수의 분모 %.2f%%포인트' % ((WACC_BASE - CASES['Base']['g']) * 100),
          '- 우리가 요구하는 무위험수익률 위 위험 대가 %.2f%%포인트' % ((WACC_BASE - RF) * 100),
          '- 알파벳 편 영구가치 배수 %.1f배' % _googl_tv(),
          '- 할인율 10%% 자리의 영구가치 배수 %.1f배' % (1.0275 / (0.10 - 0.0275)),
          '- 회계연도 2027년 2분기 실적 매출 %s' % _two(GUIDE_Q2),
          '- 회계연도 2027년 3분기 가이던스 %s' % _two(GUIDE_Q3),
          '- 3분기 가이던스를 네 배로 늘린 값 %s' % _two(GUIDE_Q3 * 4),
          '- 그 값이 최근 12개월 대비 %.0f%%' % ((GUIDE_Q3 * 4 / REV0 - 1) * 100)]

    if cons_case():
        _cc = cons_case()
        _cv = value(CONS_NAME)
        _fy = _cons_fy()
        L += ['', '## 애널리스트 컨센서스 (야후, %s 조회)' % CONS['fetched_at'][:10], '']
        for q in CONS['periods']:
            L.append('- %s %s 매출 %s · 애널리스트 %d명%s'
                     % (q['period'], q['end'][:10], _two(q['revenue'] / B), q['analysts'],
                        (' · 성장률 %.1f%%' % (q['growth'] * 100)) if q.get('growth') else ''))
        L += ['- 이번 회계연도와 다음 회계연도 평균 %s' % _two(sum(_fy) / 2),
              '- 그 값이 최근 12개월 대비 %.1f%%' % ((sum(_fy) / 2 / REV0 - 1) * 100),
              '- 우리 Base 1년차 매출 %s' % _two(path(CASES['Base'])[0][1]),
              '- 컨센서스가 우리 Base 1년차보다 %s 많다'
              % _two(sum(_fy) / 2 - path(CASES['Base'])[0][1]),
              '- 컨센서스 2년차 성장률 %.0f%%' % (CONS_Y2 * 100),
              '- 컨센서스 케이스 주당가치 %.0f · 현재가 대비 %.0f%% · 영구가치비중 %.0f%% · '
              '내재 할인율 %.2f%%'
              % (_cv['per_share'], (_cv['per_share'] / PRICE - 1) * 100,
                 _cv['tv_share'] * 100, (implied_r(CONS_NAME) or 0) * 100),
              '- 컨센서스 케이스가 Base 보다 주당 %.0f달러 높다'
              % (_cv['per_share'] - value('Base')['per_share']),
              '- 컨센서스 10년째 매출 %s · 잉여현금흐름 %s'
              % (_two(path(_cc)[-1][1]), _two(path(_cc)[-1][3]))]
        for y, rev, m, f in path(_cc)[:3]:
            L.append('- 컨센서스 %d 매출 %s · 잉여현금흐름 %s' % (y, _two(rev), _two(f)))

    _tu = terminal_uplift()
    if _tu:
        L += ['', '## 역산 셋째 — 영구 현금흐름을 얼마나 올려야 하나', '',
              '- 마지막 해 잉여현금흐름이 %s 여야 한다' % _two(_tu[0]),
              '- 우리 Base 경로 마지막 해의 %.2f배' % _tu[1]]
    _im = implied_by_multiple()
    if _im:
        _eps, _own, _gr = _im
        L += ['', '## 상대가치 축 — 비교 회사 선행 배수', '']
        # 반복 변수를 t 로 두면 모듈 전역 t(최근 12개월 표)를 가려 함수가 통째로
        # 깨진다. 파이썬이 함수 안 대입을 보고 그 이름을 지역으로 잡기 때문이다.
        for tk, name, per, end, na in multiple_rows():
            L.append('- %s(%s) 선행 주가수익비율 %.1f배 · 회계연도말 %s · 애널리스트 %d명'
                     % (name, tk, per, end, na))
        L.append('- 엔비디아 차기 추정 주당순이익 %.2f달러' % _eps)
        for lab, avg, px in _gr:
            L.append('- %s 평균 배수 %.1f배 · 함의 주가 %.0f달러 · 현재가 대비 %.0f%%'
                     % (lab, avg, px, (px / PRICE - 1) * 100))

    L += ['', '## 할인율 축 — 같은 주가를 만드는 짝', '']
    for r, g, f in rate_growth_pairs():
        L.append('- 할인율 %.2f%% 이면 10년 균등 성장률 %.2f%% · 10년 뒤 잉여현금흐름 %s'
                 % (r * 100, g * 100, _two(f)))
    if beta_grid_rows():
        L += ['', '## 베타 격자 — 창과 간격을 바꾸면', '']
        for w, i, bt, n in beta_grid_rows():
            L.append('- %s %s 베타 %.3f · 관측 %d개 · 그 베타로 낸 자기자본비용 %.2f%%'
                     % (w, i, bt, n, (RF + bt * MRP) * 100))
        _bs = [x[2] for x in beta_grid_rows()]
        L += ['- 격자 최저 %.3f · 최고 %.3f' % (min(_bs), max(_bs)),
              '- 우리가 쓰는 값 %.3f' % BETA,
              '- 격자에서 우리 값보다 낮은 칸 %d개 · 높은 칸 %d개'
              % (sum(1 for x in _bs if x < BETA), sum(1 for x in _bs if x > BETA))]

    L += ['', '## 역산 — 시장가를 정답으로 놓으면', '']
    for r in (WACC_BASE, 0.12, 0.10):
        g10 = dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT)
        f10 = FCF0 * (1 + g10) ** 10
        L.append('- 할인율 %.2f%% 이면 10년 균등 성장률 %.2f%% · 10년 뒤 잉여현금흐름 %s · '
                 '지금의 %.1f배' % (r * 100, g10 * 100, _two(f10), f10 / FCF0))
    g10 = dcf.implied_growth(FCF0, WACC_BASE, 0.0275, 10, MCAP, NET_DEBT)
    f10 = FCF0 * (1 + g10) ** 10
    rev10 = base[-1][1]
    L.append('- 요구 잉여현금흐름을 우리 Base 10년째 매출로 나눈 마진 %.1f%%' % (f10 / rev10 * 100))
    for m in (0.32, 0.35, 0.40, 0.42):
        need = f10 / m
        L.append('- 잉여현금흐름 마진 %.0f%% 이면 10년째 매출 %s 필요 · 우리 Base 경로의 %.1f배 · '
                 '매출 연평균 성장률 %.1f%%'
                 % (m * 100, _two(need), need / rev10, ((need / REV0) ** 0.1 - 1) * 100))
    for name in ORDER:
        ir = implied_r(name)
        if ir:
            L.append('- %s 경로 내재 할인율 %.2f%% · 우리 할인율보다 %.2f%%포인트 낮다 · '
                     '그 할인율이 나오려면 베타가 %.3f 여야 한다'
                     % (name, ir * 100, (wacc_of(name) - ir) * 100, (ir - RF) / MRP))
    L += ['', '## 필자 엘곰이 엔비디아에 쓴 값 (2025-03-07 편)', '',
          '- 방법 2단계 FCFE',
          '- 할인율 %.2f%%' % (EL['rate'] * 100),
          '- 영구성장률 %.2f%%' % (EL['g'] * 100),
          '- 발행주식수 %s백만' % format(int(EL['shares'] * 1000), ','),
          '- 명시적 기간 현재가치 합 %s' % _two(EL['pv_explicit']),
          '- 영구가치 현재가치 %s' % _two(EL['pv_tv']),
          '- 자기자본가치 %s' % _two(EL['equity']),
          '- 주당 내재가치 %.2f' % EL['per_share'],
          '- 당시 시장가 %.2f' % EL['price_then'],
          '- 당시 할인율 7.8%',
          '- 오늘 주가가 그 값보다 %.0f%% 높다' % ((PRICE / EL['per_share'] - 1) * 100)]
    for y, v in EL['years']:
        L.append('- 엘곰 %d 잉여현금흐름 %s' % (y, _two(v)))
    L.append('- 엘곰 2027 칸 %s · 우리 최근 12개월 실적 %s · 차이 %s'
             % (_two(127.386), _two(FCF0), _two(abs(FCF0 - 127.386))))
    L.append('- 엘곰 2026 칸 %s · 실제 FY2026 잉여현금흐름 %s'
             % (_two(98.643), _two(c['ocf']['2026']['val'] / B - c['capex']['2026']['val'] / B)))
    for r in (EL['rate'], WACC_BASE):
        v = dcf.value(EL_REST, r, EL['g'], 0.0, EL['shares'])
        L.append('- 엘곰 남은 경로(2028~2034)를 할인율 %.2f%% 로 재면 주당 %.0f · 현재가 대비 %.0f%%'
                 % (r * 100, v['per_share'], (v['per_share'] / PRICE - 1) * 100))
    ir = dcf.implied_discount_rate(EL_REST, EL['g'], MCAP, 0.0)
    L.append('- 엘곰 남은 경로가 지금 시총을 받치려면 할인율 %.2f%%' % ((ir or 0) * 100))
    L += ['', '## 회계사 판이 실적 전후로 짚은 것 (260826 · 260827 편)', '',
          '- 회계연도 2027년 2분기 매출 962억 2천만 달러 · 예상 921억 7천만 달러',
          '- 3분기 매출 가이던스 약 1,080억 달러 · 예상 1,042억 달러',
          '- 가이던스는 중국 매출을 빼고 나온 숫자',
          '- AWS GPU 200만 개 구매 계약',
          '- 정규장 -1.59% · 시간외 +5.19% · +1.45% · +2.73%',
          '- 애널리스트들이 보는 조정 총마진 약 75%',
          '- 서버 가격 인상설 15% 수준',
          '- 보유 유동성 약 2,500억 달러',
          '- 고객사 파이낸싱과 전력 생산 지원까지 포함하면 약 5,000억 달러',
          '- 미국 6대 금융기관과 주선한 고객 자금조달 5,000억 달러',
          '- 오픈AI 오하이오 데이터센터 20년 임대 보증 최대 1,050억 달러',
          '- 뱅크오브아메리카 목표주가 350달러 · 동종업계 대비 최대 50% 저평가',
          '']
    p = os.path.join(root, 'scratchpad', 'nvda_facts.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p


if __name__ == '__main__':
    report()
    print('\n사실표 ->', write_facts())
