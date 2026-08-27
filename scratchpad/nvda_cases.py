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

YEAR0 = 2027   # 표의 첫 열. 최근 12개월(2026-07 종료)에서 한 해 뒤 12개월이다

# 해마다 (매출 성장률, 잉여현금흐름 마진). 열 해가 한 사이클이다 —
# 상승 · 조정 · 회복 · 성숙 순서로 읽는다.
CASES = {
    'Bear': dict(g=0.0225,
                 rows=[(0.16, 0.38), (0.05, 0.34), (-0.25, 0.24), (-0.10, 0.21),
                       (0.06, 0.24), (0.07, 0.26), (0.05, 0.27), (0.04, 0.27),
                       (0.03, 0.27), (0.03, 0.27)],
                 why='자체 칩이 하이퍼스케일러 물량을 크게 떼어 가고 조정이 두 해 깊게 온다'),
    'Base': dict(g=0.0275,
                 rows=[(0.25, 0.40), (0.18, 0.39), (0.10, 0.37), (-0.08, 0.29),
                       (-0.03, 0.27), (0.14, 0.31), (0.10, 0.32), (0.08, 0.32),
                       (0.06, 0.32), (0.05, 0.32)],
                 why='지금 분기 속도가 두 해 더 이어지고, 소화 국면을 한 번 지난 뒤 '
                     '가속기 시장 성장률로 내려앉는다'),
    'Bull': dict(g=0.0325,
                 rows=[(0.32, 0.42), (0.26, 0.42), (0.18, 0.41), (0.10, 0.40),
                       (-0.02, 0.35), (0.16, 0.38), (0.12, 0.38), (0.10, 0.38),
                       (0.08, 0.38), (0.06, 0.38)],
                 why='추론 수요가 학습 수요를 이어받아 상승 국면이 네 해로 늘고 '
                     '조정이 한 해로 그친다'),
}
ORDER = ('Bear', 'Base', 'Bull')

# 감도표 축. 할인율은 우리 값을 가운데 두고 ±2%포인트를 1%포인트씩 흔든다.
SENS_R = [round(WACC + x, 6) for x in (-0.02, -0.01, 0.0, 0.01, 0.02)]
SENS_G = [0.0175, 0.0225, 0.0275, 0.0325, 0.0375]

# 필자 엘곰이 옮긴 SimplyWall.st 2단계 FCFE 모형(2025-03-07 편).
# 값은 그 글에 있는 것을 그대로 옮긴다 — 우리가 고치지 않는다.
EL = dict(rate=0.0848, g=0.0275, shares=24.4, per_share=127.19, price_then=117.30,
          years=[(2025, 64.585), (2026, 98.643), (2027, 127.386), (2028, 144.661),
                 (2029, 163.448), (2030, 193.089), (2031, 213.243), (2032, 230.582),
                 (2033, 245.609), (2034, 258.840)],
          pv_explicit=1048.332, pv_tv=2055.053, equity=3103.385)
EL_REST = [v for y, v in EL['years'] if y >= 2028]


def path(case):
    """연도별 (연도, 매출, 마진, 잉여현금흐름)."""
    rows, rev = [], REV0
    for i, (g, m) in enumerate(case['rows']):
        rev *= 1 + g
        rows.append((YEAR0 + i, rev, m, rev * m))
    return rows


def value(name):
    case = CASES[name]
    return dcf.value([r[3] for r in path(case)], WACC, case['g'], NET_DEBT, SHARES)


def implied_r(name):
    case = CASES[name]
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
    for r in (WACC, 0.12, 0.10):
        g10 = dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT)
        print('  할인율 %.2f%% -> 10년 균등 성장률 %.2f%% · 10년 뒤 잉여현금흐름 %.0fB (지금의 %.1f배)'
              % (r * 100, g10 * 100, FCF0 * (1 + g10) ** 10, (1 + g10) ** 10))

    print('\n민감도 (Base 경로, 할인율 x 영구성장률) — 주당 $')
    fcfs = [r[3] for r in path(CASES['Base'])]
    grid = dcf.sensitivity(fcfs, SENS_R, SENS_G, NET_DEBT, SHARES)
    print('%8s' % 'r/g' + ''.join('%8.2f%%' % (g * 100) for g in SENS_G))
    for r in SENS_R:
        print('%7.2f%%' % (r * 100) + ''.join('%9.0f' % grid[(r, g)] for g in SENS_G))


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
          '- 할인율 %.2f%%' % (WACC * 100),
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
    disc = [1 / (1 + WACC) ** i for i in range(1, len(base) + 1)]
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
    L += ['', '## 역산 — 시장가를 정답으로 놓으면', '']
    for r in (WACC, 0.12, 0.10):
        g10 = dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT)
        f10 = FCF0 * (1 + g10) ** 10
        L.append('- 할인율 %.2f%% 이면 10년 균등 성장률 %.2f%% · 10년 뒤 잉여현금흐름 %s · '
                 '지금의 %.1f배' % (r * 100, g10 * 100, _two(f10), f10 / FCF0))
    g10 = dcf.implied_growth(FCF0, WACC, 0.0275, 10, MCAP, NET_DEBT)
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
                     % (name, ir * 100, (WACC - ir) * 100, (ir - RF) / MRP))
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
    for r in (EL['rate'], WACC):
        v = dcf.value(EL_REST, r, EL['g'], 0.0, EL['shares'])
        L.append('- 엘곰 남은 경로(2028~2034)를 할인율 %.2f%% 로 재면 주당 %.0f · 현재가 대비 %.0f%%'
                 % (r * 100, v['per_share'], (v['per_share'] / PRICE - 1) * 100))
    ir = dcf.implied_discount_rate(EL_REST, EL['g'], MCAP, 0.0)
    L.append('- 엘곰 남은 경로가 지금 시총을 받치려면 할인율 %.2f%%' % ((ir or 0) * 100))
    p = os.path.join(root, 'scratchpad', 'nvda_facts.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p


if __name__ == '__main__':
    report()
    print('\n사실표 ->', write_facts())
