"""컴퓨트 자본 회수 모델을 원문 발표치와 대조한다.

발표치는 `insights/models/raw/capex.json` 이 정본이고 전부 원문 본문에 글로 적힌
값이다. 값을 맞추려고 가정을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_spacex.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                    # noqa: E402
from spacex_payback import (arr_from_capacity, contract_value_per_gw,  # noqa: E402
                            gross_margin, implied_price, payback_on_cash,
                            payback_on_revenue, years_implied)

RAW = load_raw('capex')
S = table(RAW, 'spacex-econ')


def s(k):
    return S['rows'][k][1]


def scenarios():
    return (('지금 임대되는 값', s('rev_ms_current')),
            ('리드타임 프리미엄 하한', s('rev_premium_lo')),
            ('리드타임 프리미엄 상한', s('rev_premium_hi')),
            ('API 추론으로 팔 때', s('rev_api')))


def main():
    fails = 0

    print('── 발표된 총 자본지출을 다시 낸다 ' + '─' * 32)
    lo = s('gw_lo') * s('capex_per_gw')
    hi = s('gw_hi') * s('capex_per_gw')
    ok = abs(lo - s('capex_total_lo')) <= 1
    fails += not ok
    print('  %g~%g GW × %g십억 달러/GW = %g~%g십억 달러다.'
          % (s('gw_lo'), s('gw_hi'), s('capex_per_gw'), lo, hi))
    print('  원문이 적은 폭은 %g~%g십억 달러다 — 아래쪽은 맞고 위쪽은 %g 만큼 넘는다.%s'
          % (s('capex_total_lo'), s('capex_total_hi'),
             s('capex_total_hi') - hi, '' if ok else '  FAIL'))
    need = s('capex_total_hi') / s('capex_per_gw')
    print('  위쪽 %g십억 달러가 나오려면 %g GW 가 필요하다. 원문이 같은 문장에서'
          % (s('capex_total_hi'), need))
    print('  「10기가와트를 훨씬 넘길 수도 있다」고 적은 그 폭이다(스페이스X영문 L14).')
    print('  기가와트당 %g십억 달러는 MW당 %g백만 달러와 같은 수다.'
          % (s('capex_per_gw'), s('capex_per_gw')))

    print()
    print('── 원문에 없는 값 ① 회수는 몇 해 걸리나 ' + '─' * 24)
    print('  MW당 자본 %g백만 달러, MW당 연 비용 %g백만 달러(GPU 시간당 %g달러 가정).'
          % (s('capex_per_gw'), s('cost_per_gw_yr'), s('rent_assumption')))
    print('%-22s %10s %12s %12s %10s'
          % ('파는 값', 'MW당 연 매출', '매출 기준', '현금 기준', '매출총이익률'))
    for label, rev in scenarios():
        pr = payback_on_revenue(s('capex_per_gw'), rev)
        pc = payback_on_cash(s('capex_per_gw'), rev, s('cost_per_gw_yr'))
        m = gross_margin(rev, s('cost_per_gw_yr'))
        print('%-22s %8g M %10.2f년 %10s %9.0f%%'
              % (label, rev, pr,
                 '못 갚는다' if pc is None else '%.2f년' % pc, m))
    print('  원문은 「1년 안에 자본을 회수한다」고 적었다(스페이스X영문 L53).')
    print('  그 문장이 맞는 자리는 매출 기준 5,000만 달러 하나뿐이고, 거기서도 딱 1.00년이다.')
    print('  비용을 빼면 같은 자리가 %.2f년이다.'
          % payback_on_cash(s('capex_per_gw'), s('rev_premium_hi'), s('cost_per_gw_yr')))

    print()
    print('── 원문에 없는 값 ② 매출 목표가 전제하는 값 ' + '─' * 22)
    p_lo = implied_price(s('arr_target'), s('gw_hi'), s('monetize_share'))
    p_hi = implied_price(s('arr_target'), s('gw_lo'), s('monetize_share'))
    print('  %g십억 달러를 %g~%g GW 의 %g%% 로 나누면 MW당 연 %.0f~%.0f 백만 달러다.'
          % (s('arr_target'), s('gw_lo'), s('gw_hi'), s('monetize_share'), p_lo, p_hi))
    print('  프리미엄 상한 %g 과 API 값 %g 사이다 — 목표가 그 둘 사이를 전제한다.'
          % (s('rev_premium_hi'), s('rev_api')))
    for label, rev in scenarios():
        v = arr_from_capacity(s('gw_hi'), s('monetize_share'), rev) / 1000.0
        print('    %s 기준으로 %g GW 의 절반을 팔면 %.0f십억 달러가 나온다.'
              % (label, s('gw_hi'), v))

    print()
    print('── 원문에 없는 값 ③ 묶인 계약은 몇 해치인가 ' + '─' * 22)
    for label, value, gw in (('마이크로소프트가 올해 묶은 것',
                              s('ms_contract_value'), s('ms_contract_gw')),
                             ('2025년 10월 오픈AI 계약',
                              s('openai_deal_value'), s('openai_deal_gw'))):
        v = contract_value_per_gw(value, gw)
        y = years_implied(v, s('rev_ms_current'))
        print('  %s — %g십억 ÷ %g GW = GW당 %.1f십억 달러'
              % (label, value, gw, v))
        print('    지금 임대가 %g백만 달러/MW·년 로 세면 %.1f년치다.'
              % (s('rev_ms_current'), y))
    print('  계약 총액에는 GPU 값이 안 들어 있다(스페이스X영문 L42).')
    print('  그래서 이 햇수는 계약 기간이 아니라 「임대가로 환산한 두께」다.')

    print()
    print('── 원문에 없는 값 ④ 파는 층에 따라 값이 일곱 배 벌어진다 ' + '─' * 14)
    print('  지금 %g 에서 API %g 까지 %.1f 배다. 같은 전력, 같은 GPU 인데'
          % (s('rev_ms_current'), s('rev_api'), s('rev_api') / s('rev_ms_current')))
    print('  파는 층이 달라서 벌어진다 — 상면을 빌려주느냐, 토큰을 파느냐.')
    print('  원문이 마이크로소프트를 최대 고객으로 본 이유가 이 배수다.')

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
