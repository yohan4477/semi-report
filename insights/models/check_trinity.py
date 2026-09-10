"""GPU 금융 모델을 원문 발표치와 대조한다.

발표치는 `insights/models/raw/capex.json` 이 정본이고 전부 원문 본문에 글로 적힌
값이다. 값을 맞추려고 가정을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_trinity.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                     # noqa: E402
from trinity_debt import (gpus_behind, implied_debt_to_revenue,        # noqa: E402
                          implied_floor, implied_yield_on_cost,
                          kw_per_gpu, margin_drop, split, take_rate)

RAW = load_raw('capex')
B = table(RAW, 'trinity-backstop')
D = table(RAW, 'trinity-debt')


def b(k):
    return B['rows'][k][1]


def d(k):
    return D['rows'][k][1]


def main():
    fails = 0

    print('── 공시된 백스톱 총액에서 바닥값을 다시 낸다 ' + '─' * 22)
    got = implied_floor(b('sharon_total') * 1e9, b('sharon_gpus'), b('sharon_years'))
    want = b('sharon_floor')
    ok = abs(got - want) <= 0.02
    fails += not ok
    print('  %g십억 달러 ÷ (%s장 × %g년 × 8,760시간) = %.3f달러 — 원문 %g달러%s'
          % (b('sharon_total'), format(b('sharon_gpus'), ','), b('sharon_years'),
             got, want, '' if ok else '  FAIL'))

    print()
    print('── 1년차 분배를 다시 낸다 ' + '─' * 38)
    s = split(b('y1_floor'), b('y1_charge'), b('nvda_share'))
    for label, gotv, wantv, tol in (('초과분', s['excess'],
                                     b('y1_charge') - b('y1_floor'), 0.001),
                                    ('엔비디아 몫', s['nvda'], b('y1_nvda'), 0.01),
                                    ('네오클라우드 몫', s['neo'], b('y1_neo'), 0.01),
                                    ('네오클라우드 합계', s['neo_total'],
                                     b('y1_total'), 0.01)):
        okk = abs(gotv - wantv) <= tol
        fails += not okk
        print('  %-16s 모델 %.2f · 발표 %.2f%s'
              % (label, gotv, wantv, '' if okk else '  FAIL'))

    print()
    print('── 원문에 없는 값 ① 1년차 테이크레이트 ' + '─' * 26)
    t = take_rate(s['nvda'], b('y1_charge'))
    print('  엔비디아 몫 %.2f 를 청구가 %.2f 로 나누면 %.1f%% 다.'
          % (s['nvda'], b('y1_charge'), t))
    print('  원문이 적은 6년 평균은 %g%% 다 — 1년차 한 해가 평균과 거의 같다.'
          % b('take_rate'))
    print('  바닥값이 해마다 내려가고 청구가도 내려가서, 몫이 그 자리에 머문다.')

    print()
    print('── 원문에 없는 값 ② 100MW 뒤에 선 GPU 장수 ' + '─' * 22)
    n = gpus_behind(b('guarantee_per_100mw') * 1e9, b('curve_avg'), b('backstop_years'))
    print('  우발채무 %g십억 달러를 평균 바닥값 %g달러로 풀면 %s 장이다.'
          % (b('guarantee_per_100mw'), b('curve_avg'), format(int(n), ',')))
    print('  100MW 를 그 장수로 나누면 한 장에 %.2f kW 다 — 부대설비까지 포함한 값이다.'
          % kw_per_gpu(n, 100))
    print('  이 값이 그럴듯해야 우발채무 수치와 바닥값 수치가 같은 계약을 말한 것이다.')

    print()
    print('── 원문에 없는 값 ③ 담보가 없어지면 부채가 얼마나 있다는 뜻인가 ' + '─' * 2)
    ratio = implied_debt_to_revenue(d('rate_secured'), d('rate_unsecured'),
                                    d('pbt_unsecured'), d('pbt_secured'))
    print('  금리가 %g%% 에서 %g%% 로 %.2f%%포인트 오를 때 세전이익률이 %g%% 에서'
          % (d('rate_secured'), d('rate_unsecured'),
             d('rate_unsecured') - d('rate_secured'), d('pbt_secured')))
    print('  %g%% 로 %.1f%%포인트 깎인다. 그 둘을 잇는 것은 부채 규모뿐이다.'
          % (d('pbt_unsecured'), d('pbt_secured') - d('pbt_unsecured')))
    print('  부채가 연 매출의 %.2f 배여야 이 산수가 맞는다. 원문에 없는 값이다.' % ratio)
    chk = margin_drop(d('rate_secured'), d('rate_unsecured'), ratio)
    print('  되짚으면 %.2f%%포인트다 — 발표된 폭과 같다.' % chk)

    print()
    print('── 원문에 없는 값 ④ 그 부채가 전제하는 원가수익률 ' + '─' * 14)
    print('%-16s %14s %16s' % ('담보인정비율', '프로젝트 비용', '원가수익률'))
    for ltv in (d('ltv_lo'), d('ltv_hi')):
        y = implied_yield_on_cost(ratio, ltv)
        print('%-16s %10.2f 배 매출 %13.1f%%' % ('%g%%' % ltv, ratio / (ltv / 100.0), y))
    print('  원가수익률은 연 매출 ÷ 프로젝트 비용이다(트리니티영문 L251).')
    print('  원문은 네오클라우드가 하이퍼스케일러보다 %g~%g%%포인트 높다고만 적었다.'
          % (d('yoc_gap_lo'), d('yoc_gap_hi')))

    print()
    print('── 원문에 없는 값 ⑤ 백스톱이 금리에서 깎아 주는 폭 ' + '─' * 12)
    gap = d('cw_unsecured') - d('cw_backstopped')
    print('  코어위브 무담보 %g%% 와 메타가 받쳐 준 대출 %g%% 의 차이가 %.1f%%포인트다.'
          % (d('cw_unsecured'), d('cw_backstopped'), gap))
    print('  받쳐 준 쪽은 메타 자기 채권 %g%% 보다 %.1f%%포인트 높을 뿐이다.'
          % (d('meta_bond'), d('cw_backstopped') - d('meta_bond')))
    print('  빌리는 회사가 아니라 받쳐 주는 회사의 신용으로 값이 매겨진다는 뜻이다.')
    drop = margin_drop(d('cw_backstopped'), d('cw_unsecured'), ratio)
    print('  그 %.1f%%포인트를 위 부채 배수에 물리면 이익률 %.1f%%포인트다.' % (gap, drop))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
