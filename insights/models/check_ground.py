"""지상 데이터센터 자본 모델을 원문 발표치와 대조한다.

발표치는 `insights/models/raw/capex.json` 이 정본이고 전부 원문 본문에 글로 적힌
값이다. 값을 맞추려고 가정을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_ground.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                    # noqa: E402
from ground_capex import (annual_capital, annual_mwh, implied_margin,  # noqa: E402
                          power_cost_per_mw_year, price_from_mwh,
                          pulled_forward_revenue, recovery_factor,
                          revenue_share, wacc)

RAW = load_raw('capex')
LY = table(RAW, 'ground-layers')
G = table(RAW, 'ground-assump')


def g(k):
    return G['rows'][k][1]


def layers():
    return list(LY['rows'].values())


def main():
    fails = 0

    print('── 발표된 자본비용을 다시 낸다 ' + '─' * 34)
    got = wacc(g('debt_cost'), g('equity_cost'), g('debt_share'))
    want = g('wacc')
    # 0.06 까지 봐준다 — 10.25 를 10.3 으로 적은 반올림이다. 가정을 손댄 것이 아니다
    ok = abs(got - want) <= 0.06
    fails += not ok
    print('  부채 %g%% × %g%% + 자기자본 %g%% × %g%% = %.2f%% — 원문 %g%%%s'
          % (g('debt_cost'), g('debt_share'), g('equity_cost'),
             100 - g('debt_share'), got, want, '' if ok else '  FAIL'))
    print('  0.05%포인트 차이는 반올림이다. 원문이 10.25 를 10.3 으로 적었다.')

    crf = recovery_factor(g('wacc'), g('life_dc'))
    print('  자본회수계수는 %.4f 다. 수명 %g년으로 그냥 나눈 %.4f 의 %.2f 배다.'
          % (crf, g('life_dc'), 1.0 / g('life_dc'), crf * g('life_dc')))

    print()
    print('── 원문에 없는 값 ① 층마다 자본이 매출을 얼마나 먹나 ' + '─' * 12)
    print('  연 자본비 = MW당 자본 × %.4f. 매출은 MW당 연 %g~%g 백만 달러다.'
          % (crf, g('rev_lo'), g('rev_hi')))
    print('%-14s %12s %14s %16s' % ('층', 'MW당 자본', '연 자본비', '매출에서 먹는 몫'))
    for name, lo, hi, _why, _cite in layers():
        hi_v = hi if hi is not None else lo
        alo = annual_capital(lo, g('wacc'), g('life_dc'))
        ahi = annual_capital(hi_v, g('wacc'), g('life_dc'))
        slo = revenue_share(lo, g('rev_hi'), g('wacc'), g('life_dc'))
        shi = revenue_share(hi_v, g('rev_lo'), g('wacc'), g('life_dc'))
        span = '%g~%g' % (lo, hi) if hi is not None else '%g 이상' % lo
        print('%-14s %10s M %6.2f~%.2f M %11.1f~%.1f%%'
              % (name, span, alo, ahi, slo, shi))
    print('  1층에서 4층으로 가면 그 몫이 %.1f%% 에서 %.1f%% 로 간다.'
          % (revenue_share(layers()[0][1], g('rev_hi'), g('wacc'), g('life_dc')),
             revenue_share(layers()[3][1], g('rev_lo'), g('wacc'), g('life_dc'))))
    print('  나머지로 GPU 값과 전기값과 사람 값을 다 대야 한다.')

    print()
    print('── 원문에 없는 값 ② 조기 가동의 값이 전제하는 마진 ' + '─' * 14)
    rev = pulled_forward_revenue(g('early_mw'), g('early_months'),
                                 (g('rev_lo') + g('rev_hi')) / 2)
    print('  %g MW 를 %g개월 일찍 켜면 매출 %.0f 백만 달러를 먼저 받는다.'
          % (g('early_mw'), g('early_months'), rev))
    for npv in (g('npv_lo'), g('npv_hi')):
        m = implied_margin(npv, g('early_mw'), g('early_months'),
                           (g('rev_lo') + g('rev_hi')) / 2)
        print('    발표된 %g 백만 달러는 그 매출의 %.0f%% 다.' % (npv, m))
    print('  원문은 이 값을 순현재가치라고만 적고 어떤 마진을 썼는지는 안 밝혔다.')

    print()
    print('── 원문에 없는 값 ③ 같은 글의 전기 단가가 서로 안 맞는다 ' + '─' * 8)
    mwh = annual_mwh(g('pue'), g('util'))
    cost = power_cost_per_mw_year(g('power_price'), g('pue'), g('util'))
    print('  IT 부하 1MW 는 PUE %g 와 가동률 %g%% 로 한 해 %s MWh 를 쓴다.'
          % (g('pue'), g('util'), format(int(mwh), ',')))
    print('  모델이 쓴 단가 %g달러/kWh 는 MWh 당 %g달러이고, MW당 연 %s 달러다.'
          % (g('power_price'), g('power_price') * 1000, format(int(cost), ',')))
    for label, p in (('배후 자체발전 하한', g('btm_lo')),
                     ('배후 자체발전 상한', g('btm_hi')),
                     ('주요 시장 계통가', g('grid_price'))):
        c2 = power_cost_per_mw_year(price_from_mwh(p), g('pue'), g('util'))
        print('    %s %g달러/MWh 로 세면 MW당 연 %s 달러 — 모델 단가의 %.2f 배'
              % (label, p, format(int(c2), ','), c2 / cost))
    print('  같은 글이 한쪽에서 87달러로 세고 다른 쪽에서 시장가를 150달러라고 적는다.')

    print()
    print('── 원문에 없는 값 ④ 전기가 매출에서 먹는 몫 ' + '─' * 22)
    for label, p in (('모델 단가', g('power_price') * 1000),
                     ('계통 시장가', g('grid_price'))):
        c2 = power_cost_per_mw_year(price_from_mwh(p), g('pue'), g('util')) / 1e6
        print('    %s %g달러/MWh — MW당 연 %.2f 백만 달러, 매출의 %.1f~%.1f%%'
              % (label, p, c2, c2 / g('rev_hi') * 100, c2 / g('rev_lo') * 100))

    print()
    print('── 원문에 없는 값 ⑤ 자본과 전기를 함께 세면 ' + '─' * 22)
    for name, lo, hi, _why, _cite in layers():
        hi_v = hi if hi is not None else lo
        cap = annual_capital(hi_v, g('wacc'), g('life_dc'))
        pw = power_cost_per_mw_year(price_from_mwh(g('grid_price')),
                                    g('pue'), g('util')) / 1e6
        print('    %-12s 자본 %.2f + 전기 %.2f = %.2f 백만 달러, 매출 %g 의 %.0f%%'
              % (name, cap, pw, cap + pw, g('rev_lo'),
                 (cap + pw) / g('rev_lo') * 100))
    print('  GPU 값은 여기 안 들어 있다 — 이 둘만으로 매출의 이만큼이 나간다.')

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
