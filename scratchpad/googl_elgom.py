# -*- coding: utf-8 -*-
"""필자 엘곰이 알파벳(260516)에 세운 가정을 그대로 넣어 돌린다.

그는 3구간 가정까지만 내고 현재가치 합산을 하지 않았다. 그 마지막 칸을 우리 계산기로
채운다 — 산식은 그가 삼성전자에 쓴 것과 같은 insights/dcf.py 다.

기준연도도 그가 쓴 FY2025 로 맞춘다. 우리 보고서는 TTM 을 쓰지만 여기서는 「그의
가정 그대로」가 목적이라 출발점을 바꾸지 않는다.

가정 출처: content/understanding/회계사/[260516] ... 엘곰.md
  Phase 1 (2026~2028)  매출 20~22%  · FCF마진 3~8%
  Phase 2 (2029~2031)  매출 15~18%  · FCF마진 12~18%
  Phase 3 (2032~2035)  매출 10~13%  · FCF마진 20~25%
  WACC 8.5(Bull)/9.5(Base)/10.5(Bear)% · 영구성장률 3~4%

콘솔 출력은 report() 안에 둔다 — 보고서 생성기가 이 모듈을 import 해 값만 쓴다.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'insights'))
import dcf  # noqa: E402

B = 1e9
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(_root, 'insights/valuation/GOOGL/facts.json'),
                   encoding='utf-8'))
c = d['sec']['concepts']

REV0 = c['revenue']['2025']['val'] / B
NET_DEBT = (c['lt_debt']['2025']['val'] + c['st_debt']['2025']['val']
            - c['cash']['2025']['val'] - c['st_investments']['2025']['val']) / B
SHARES = d['sec']['shares_outstanding']['val'] / B
PRICE = d['market']['price']

# (구간 연수, 매출 성장, FCF마진) — 낮은쪽 / 가운데 / 높은쪽
PHASES = [(3, (0.20, 0.21, 0.22), (0.03, 0.055, 0.08)),
          (3, (0.15, 0.165, 0.18), (0.12, 0.15, 0.18)),
          (4, (0.10, 0.115, 0.13), (0.20, 0.225, 0.25))]

# 이름: (레인지에서 고를 자리, WACC, 영구성장률)
CASES = {'Bear': (0, 0.105, 0.030),
         'Base': (1, 0.095, 0.0375),
         'Bull': (2, 0.085, 0.040)}
ORDER = ('Bear', 'Base', 'Bull')


def path(k):
    """연도별 (연도, 매출, FCF마진, FCF). k 는 레인지에서 고를 자리."""
    rows, rev, y = [], REV0, 2025
    for years, g, m in PHASES:
        for _ in range(years):
            y += 1
            rev *= 1 + g[k]
            rows.append((y, rev, m[k], rev * m[k]))
    return rows


def value(name):
    """케이스 하나의 평가 결과."""
    k, r, g = CASES[name]
    return dcf.value([x[3] for x in path(k)], r, g, NET_DEBT, SHARES)


def report():
    print('기준 FY2025 매출 %.1fB · 순현금 %.1fB · 주식수 %.3fB · 주가 %.2f\n'
          % (REV0, -NET_DEBT, SHARES, PRICE))
    print('%-6s %7s %7s %9s %10s %9s %8s'
          % ('케이스', 'WACC', '영구g', '2035 FCF', '주당가치', '현재가대비', 'TV비중'))
    for name in ORDER:
        k, r, g = CASES[name]
        rows = path(k)
        v = value(name)
        print('%-6s %6.1f%% %6.2f%% %8.0fB %9.0f$ %8.0f%% %7.0f%%'
              % (name, r * 100, g * 100, rows[-1][3], v['per_share'],
                 (v['per_share'] / PRICE - 1) * 100, v['tv_share'] * 100))
    print('\nBase 연도별')
    print('%6s %9s %7s %9s' % ('연도', '매출B', '마진', 'FCF B'))
    for y, rev, m, f in path(1):
        print('%6d %9.0f %6.1f%% %9.0f' % (y, rev, m * 100, f))


if __name__ == '__main__':
    report()
