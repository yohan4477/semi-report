# -*- coding: utf-8 -*-
"""알파벳 3구간 DCF를 Bear/Base/Bull 셋으로 돌린다. 검토용 계산이라 scratchpad에 둔다.

경로는 매출 × FCF마진으로 만든다. FCF를 바로 성장시키지 않는 이유는 지금 알파벳의
FCF가 CapEx로 눌린 값이라(TTM 마진 11.9%) 그 눌린 값에 성장률을 곱하면 압축이 영구히
이어지는 모형이 되기 때문이다. 매출과 마진을 따로 움직여야 R9(정상화 FCF)를 지킨다.

마진은 구간 안에서 선형으로 옮긴다. R12가 성장률을 한 해에 안 꺾는 것과 같은 이유다.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'insights'))
import dcf

B = 1e9
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(root, 'insights/valuation/GOOGL/facts.json'), encoding='utf-8'))
t = d['sec']['ttm']
REV0 = t['revenue']['val'] / B
FCF0 = (t['ocf']['val'] - t['capex']['val']) / B
MARGIN0 = FCF0 / REV0
NET_DEBT = (t['lt_debt']['val'] + t['st_debt']['val']
            - t['cash']['val'] - t['st_investments']['val']) / B
# 주식수도 10억 주 단위로 맞춘다. equity가 10억 달러 단위라 실주식수로 나누면
# 주당가치가 0에 붙는다 — 2026-08-26에 케이스 셋이 전부 $0으로 나온 원인이다.
SHARES = d['sec']['shares_outstanding']['val'] / B
SHARES_DIL = d['sec']['shares_diluted']['val'] / B
PRICE = d['market']['price']
MCAP = d['market']['market_cap'] / B

P1_YEARS = 3   # 2026~2028
P2_YEARS = 7   # 2029~2035

CASES = {
    # 이름: (P1 성장, P1 끝 마진, P2 끝 성장, P3 마진, 영구성장)
    'Bear': dict(g1=0.14, m1=0.09, g2=0.040, m3=0.15, g=0.0225,
                 why='총액 인식·순환 거래를 크게 깎고, 감가상각 수렴이 마진을 15%까지만 되돌린다'),
    'Base': dict(g1=0.175, m1=0.11, g2=0.050, m3=0.17, g=0.0275,
                 why='세미 GCP 전망을 전사 기준으로 환산하고 순환 거래분을 덜어낸 값'),
    'Bull': dict(g1=0.21, m1=0.13, g2=0.060, m3=0.19, g=0.0325,
                 why='TPU 시스템 판매가 수주 잔고대로 실현되고 CapEx 압축이 2028년에 풀린다'),
}
WACC = 0.10


def lerp(a, b, i, n):
    """구간 안에서 a에서 b로 선형 이동. i는 1부터 n까지."""
    return a + (b - a) * i / n


def path(c):
    """연도별 (매출, 마진, FCF)를 만든다."""
    rows, rev = [], REV0
    for i in range(1, P1_YEARS + 1):
        rev *= 1 + c['g1']
        m = lerp(MARGIN0, c['m1'], i, P1_YEARS)
        rows.append((2025 + i, rev, m, rev * m))
    for i in range(1, P2_YEARS + 1):
        g = lerp(c['g1'], c['g2'], i, P2_YEARS)   # H-모델 선형 감소
        rev *= 1 + g
        m = lerp(c['m1'], c['m3'], i, P2_YEARS)
        rows.append((2025 + P1_YEARS + i, rev, m, rev * m))
    return rows


print('기준 (TTM %s) 매출 %.1fB · FCF %.1fB · 마진 %.1f%% · 순현금 %.1fB'
      % (t['revenue']['end'], REV0, FCF0, MARGIN0 * 100, -NET_DEBT))
print('주가 $%.2f · 시총 %.0fB · 주식수 %.3fB · WACC %.0f%%\n' % (PRICE, MCAP, SHARES, WACC * 100))

print('%-6s %7s %7s %7s %8s %9s %8s %7s' % ('케이스', 'P1성장', 'P1마진', 'P3마진', '영구g', '주당가치', '괴리', 'TV비중'))
out = {}
for name, c in CASES.items():
    rows = path(c)
    fcfs = [r[3] for r in rows]
    v = dcf.value(fcfs, WACC, c['g'], NET_DEBT, SHARES)
    ps = v['per_share']
    tv_share = v['tv_share']
    out[name] = (v, rows)
    print('%-6s %6.1f%% %6.1f%% %6.1f%% %7.2f%% %8.0f%s %7.0f%% %6.0f%%'
          % (name, c['g1'] * 100, c['m1'] * 100, c['m3'] * 100, c['g'] * 100,
             ps, '$', (ps / PRICE - 1) * 100, tv_share * 100))

v = out['Base'][0]
print('\nBase 희석주식 기준 주당 $%.0f' % (v['equity'] / SHARES_DIL))
print('\nBase 연도별 경로')
print('%6s %9s %7s %8s' % ('연도', '매출B', '마진', 'FCF B'))
for y, rev, m, f in out['Base'][1]:
    print('%6d %9.0f %6.1f%% %8.0f' % (y, rev, m * 100, f))

print('\n민감도 (Base 경로, WACC × 영구성장률) — 주당 $')
fcfs = [r[3] for r in out['Base'][1]]
rs = [0.09, 0.095, 0.10, 0.105, 0.11]
gs = [0.0175, 0.0225, 0.0275, 0.0325, 0.0375]
print('%8s' % 'WACC\g' + ''.join('%8.2f%%' % (g * 100) for g in gs))
grid = dcf.sensitivity(fcfs, rs, gs, NET_DEBT, SHARES)   # {(r, g): per_share}
for r in rs:
    print('%7.1f%%' % (r * 100) + ''.join('%9.0f' % grid[(r, g)] for g in gs))
