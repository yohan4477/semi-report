"""백스톱 용량 모델을 원문 발표치와 대조한다.

발표치는 `insights/models/raw/capex.json` 이 정본이고 전부 원문 본문에 글로 적힌
값이다. 앞 두 글의 값(GPU 한 장의 전력, 메가와트당 자본)은 그 글의 표에서 다시 낸다.
값을 맞추려고 가정을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_backstop.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                     # noqa: E402
from backstop_capacity import (HOURS_PER_YEAR, capex_behind, coverage,  # noqa: E402
                               discount, floor_from_per_gw, gpus_behind,
                               gw_enabled, implied_capex_per_mw,
                               kw_per_gpu, per_gw, ratio, residual, share)
from bridge_capex import all_in_per_mw, gpu_capex, it_capex_per_mw     # noqa: E402
import trinity_debt as TD                                              # noqa: E402

CAPEX = load_raw('capex')
TBL = load_raw('tables')
S = table(CAPEX, 'backstop-sheet')
C = table(CAPEX, 'backstop-capacity')
A = table(CAPEX, 'backstop-aicp')
R = table(CAPEX, 'backstop-rvg')
B = table(CAPEX, 'trinity-backstop')
LY = table(CAPEX, 'ground-layers')
F = table(CAPEX, 'frame-capex')
SH = table(CAPEX, 'frame-sheet')
AMD = table(TBL, 'amd-capex')

GPUS_PER_SERVER = 8


def s(k):
    return S['rows'][k][1]


def c(k):
    return C['rows'][k][1]


def a(k):
    return A['rows'][k][1]


def r(k):
    return R['rows'][k][1]


def b(k):
    return B['rows'][k][1]


def sku(name, row):
    i = AMD['columns'].index(name)
    return AMD['rows'][row][i]


def bridge_span():
    """다리 층이 세운 메가와트당 자본의 폭. 그 층의 검사기와 같은 길로 낸다."""
    n = TD.gpus_behind(b('guarantee_per_100mw') * 1e9, b('curve_avg'), b('backstop_years'))
    kw = TD.kw_per_gpu(n, 100)
    per_gpu = gpu_capex(sku('B200', 'server_cost'), sku('B200', 'other_cluster_cost'),
                        GPUS_PER_SERVER)
    it = it_capex_per_mw(kw, per_gpu)
    los = [v[1] for v in LY['rows'].values()]
    his = [v[2] if v[2] is not None else v[1] for v in LY['rows'].values()]
    return kw, all_in_per_mw(min(los), it), all_in_per_mw(max(his), it)


def main():
    fails = 0

    print('── 여섯 항목 가운데 넷을 더하면 ' + '─' * 34)
    named = [s('supply_now'), s('lps_now'), s('aicp_now'), s('lease_now')]
    rest = residual(s('off_total'), named)
    rest_prev = residual(s('off_prev'), [s('supply_prev'), s('lps_prev')])
    print('  공급 %g · 보증 %g · AI 클라우드 %g · 리스 %g = %g (십억 달러)'
          % (named[0], named[1], named[2], named[3], sum(named)))
    print('  총액 %g 에서 빼면 이름 없는 두 항목이 %g 다. 전 분기는 %g 였다.'
          % (s('off_total'), rest, rest_prev))
    print('  원문이 항목 넷만 적었으므로 이 둘은 원문에 없는 값이다.')
    ok = rest > 0
    fails += not ok
    print('  나머지가 양수%s' % ('' if ok else '  FAIL'))

    print()
    print('── 1기가와트당 부담을 계약에서 다시 낸다 ' + '─' * 26)
    firmus = per_gw(a('firmus_total'), a('firmus_mw') / 1000.0)
    ports = per_gw(s('lps_now'), c('ports_gw'))
    for label, got, want, tol in (('AICP (Firmus)', firmus, c('per_gw_aicp'), 1.0),
                                  ('PORTS-Pike', ports, c('per_gw_ports'), 1.0)):
        okk = abs(got - want) <= tol
        fails += not okk
        print('  %-14s 모델 %.1f · 발표 %g 십억/GW%s' % (label, got, want, '' if okk else '  FAIL'))
    print('  Firmus 21.1십억을 0.36GW 로, 보증 108.5십억을 4.25GW 로 나눈 값이다.')

    print()
    print('── 원문에 없는 값 ① Firmus 뒤에 선 GPU 와 전력 ' + '─' * 18)
    n = gpus_behind(a('firmus_total') * 1e9, a('floor'), a('years'), HOURS_PER_YEAR)
    kw = kw_per_gpu(n, a('firmus_mw'))
    kw_trn, span_lo, span_hi = bridge_span()
    print('  %g십억을 바닥값 %g달러 × %g년으로 나누면 %s 장이다.'
          % (a('firmus_total'), a('floor'), a('years'), format(int(n), ',')))
    print('  360MW 를 그 장수로 나누면 한 장에 %.2fkW 다.' % kw)
    print('  GPU 금융 층이 7월 글에서 되짚은 값은 %.2fkW 였다 — 다른 계약, 다른 글에서 같은 자리에 선다.'
          % kw_trn)
    okk = abs(kw - kw_trn) <= 0.05
    fails += not okk
    print('  두 값의 차이 %.2fkW%s' % (abs(kw - kw_trn), '' if okk else '  FAIL'))

    print()
    print('── 원문에 없는 값 ② 59십억/GW 를 바닥값으로 되돌리면 ' + '─' * 12)
    fl = floor_from_per_gw(c('per_gw_aicp'), kw_trn, a('years'), HOURS_PER_YEAR)
    print('  1GW 에 %.2fkW 짜리 GPU %s 장. %g십억을 6년 시간으로 나누면 %.3f달러다.'
          % (kw_trn, format(int(1e6 / kw_trn), ','), c('per_gw_aicp'), fl))
    okk = abs(fl - a('floor')) <= 0.05
    fails += not okk
    print('  원문 바닥값 %g달러와 %s' % (a('floor'), '같은 자리다' if okk else '어긋난다  FAIL'))
    print('  시장 5년 계약가 %g~%g달러보다 %.0f~%.0f%% 낮다.'
          % (a('market_lo'), a('market_hi'),
             discount(a('floor'), a('market_lo')), discount(a('floor'), a('market_hi'))))

    print()
    print('── 원문에 없는 값 ③ 잔존가치보증이 전제하는 자본 ' + '─' * 14)
    impl = implied_capex_per_mw(c('per_gw_rvg'), r('guarantee_cap'))
    print('  1GW당 %g십억이 거래액의 %g%% 라면 거래액은 1GW당 %.1f십억 — 메가와트당 %.1f백만 달러다.'
          % (c('per_gw_rvg'), r('guarantee_cap'), impl, impl))
    okk = span_lo <= impl <= span_hi
    fails += not okk
    print('  다리 층이 세운 메가와트당 자본 %.1f~%.1f백만 안에 %s'
          % (span_lo, span_hi, '든다' if okk else '안 든다  FAIL'))

    print()
    print('── 부담이 자본을 몇 배 덮나 ' + '─' * 38)
    print('%-16s %12s %12s' % ('구조', '1GW당 부담', '자본 대비'))
    for label, v in (('AICP', c('per_gw_aicp')), ('PORTS-Pike', c('per_gw_ports')),
                     ('잔존가치보증', c('per_gw_rvg'))):
        print('%-16s %9g 십억 %9.2f 배' % (label, v, coverage(v, impl)))
    print('  자본은 위 ③의 %.1f백만/MW 로 셌다. AICP 만 자본보다 부담이 크다 —' % impl)
    print('  6년 임대료를 다 받쳐 주면 GPU 값을 넘는다는 뜻이다.')

    print()
    print('── 부담 총액이 받치는 용량 ' + '─' * 40)
    for label, v in (('AICP 공시 잔액', a('total')), ('저자의 F1/27 말 추정', a('total_f127'))):
        print('  %-20s %g십억 ÷ %g = %.2f GW' % (label, v, c('per_gw_aicp'),
                                               gw_enabled(v, c('per_gw_aicp'))))
    cb = capex_behind(c('nvda_gw'), impl)
    print('  원문이 센 받쳐 준 용량 %gGW 에 %.1f백만/MW 를 곱하면 자본지출 %.0f십억 달러다.'
          % (c('nvda_gw'), impl, cb))
    print('  프레임의 빅4 2026년 자본지출 %g십억의 %.0f%% 다.'
          % (F['rows']['total_stated'][1], share(cb, F['rows']['total_stated'][1])))

    print()
    print('── 암묵적 백스톱과 명시적 백스톱 ' + '─' * 34)
    for label, gw in (('엔비디아(명시)', c('nvda_gw')),
                      ('빅4 제3자 리스 2026', c('giga_gw_2026')),
                      ('같은 리스 2028 하한', c('giga_gw_2028'))):
        print('  %-20s %5g GW  자본 %6.0f십억  엔비디아 대비 %.1f배'
              % (label, gw, capex_behind(gw, impl), ratio(gw, c('nvda_gw'))))
    print('  리스는 %g~%g년이고 개발자가 그것을 담보로 투자등급 값에 빌린다(백스톱영문 L56).'
          % (c('lease_years_lo'), c('lease_years_hi')))

    print()
    print('── 대차대조표 안팎 ' + '─' * 48)
    print('  오프밸런스 %g 은 온밸런스 부채 %g 의 %.1f배, 차입금 %g 의 %.1f배다.'
          % (s('off_total'), s('on_liab'), ratio(s('off_total'), s('on_liab')),
             s('debt'), ratio(s('off_total'), s('debt'))))
    print('  F1/28 EBITDA 컨센서스 %g 으로 나누면 %.2f년치다.'
          % (s('ebitda_f128'), ratio(s('off_total'), s('ebitda_f128'))))
    print('  전 분기 %g 에서 이번 분기 %g 로 %.1f배 — 한 분기에 %g십억이 늘었다.'
          % (s('off_prev'), s('off_total'), ratio(s('off_total'), s('off_prev')),
             s('off_total') - s('off_prev')))
    rv = share(r('obl_f131'), r('assumed_funding'))
    print('  잔존가치보증 F1/31 부담 %g 은 가정한 조달 %g 의 %.1f%% — 상한 %g%% 아래다.'
          % (r('obl_f131'), r('assumed_funding'), rv, r('guarantee_cap')))
    okk = rv <= r('guarantee_cap')
    fails += not okk

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
