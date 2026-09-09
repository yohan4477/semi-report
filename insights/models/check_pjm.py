"""PJM 원가 모델을 원문 발표 숫자와 대조한다.

발표치는 원문 본문에 글로 적힌 값이고 `insights/models/raw/tables.json` 이 정본이다.
값을 맞추려고 가정을 손대지 않는다. 안 맞는 자리는 안 맞는 대로 표에 남긴다.

    PYTHONIOENCODING=utf-8 python insights/models/check_pjm.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                              # noqa: E402
from pjm_capacity import (auction_cost, implied_capacity, overlap,  # noqa: E402
                          per_person, price_sensitivity, saving, split_saving)

RAW = load_raw('tables')
A = table(RAW, 'pjm-auctions')
C = table(RAW, 'pjm-context')
BN = 1e9


def auctions():
    cols = A['columns']
    return [dict(zip(cols, v)) for v in A['rows'].values()]


def ctx(key):
    return C['rows'][key][1]


def main():
    fails = 0

    print('── 원문이 낸 절감액을 다시 낸다 ' + '─' * 32)
    print('경매 비용 = 낙찰 용량 × 낙찰 가격 × 365일. 그 차이가 절감액이다.')
    print('%-9s %12s %12s %12s %12s %10s'
          % ('시즌', '실제 비용', '반사실 비용', '모델 절감', '발표 절감', '차이'))
    for r in auctions():
        if r['cf_price'] is None:
            continue
        real = auction_cost(r['cleared_gw'], r['price_usd_mw_day'])
        cf = auction_cost(r['cf_cleared_gw'], r['cf_price'])
        got = saving(r['cleared_gw'], r['price_usd_mw_day'],
                     r['cf_cleared_gw'], r['cf_price']) / BN
        want = r['stated_saving_bn']
        ok = abs(got - want) <= 0.05
        fails += not ok
        print('%-9s %11.2fB %11.2fB %11.2fB %11.2fB %9.2fB%s'
              % (r['season'], real / BN, cf / BN, got, want, got - want,
                 '' if ok else '  FAIL'))

    tot = sum(saving(r['cleared_gw'], r['price_usd_mw_day'],
                     r['cf_cleared_gw'], r['cf_price'])
              for r in auctions() if r['cf_price'] is not None) / BN
    want_tot = ctx('total_waste')
    print('  합계 모델 %.2fB · 발표 %gB — 원문이 「약 120억」이라고 반올림해 적었다'
          % (tot, want_tot))

    print()
    print('── 절감액은 가격에서 오나 용량에서 오나 ' + '─' * 26)
    print('가격 몫은 산 용량 전부에 걸리고, 용량 몫은 줄어든 만큼에만 걸린다.')
    print('%-9s %12s %12s %10s %10s'
          % ('시즌', '가격 몫', '용량 몫', '가격 비중', '줄어든 용량'))
    for r in auctions():
        if r['cf_price'] is None:
            continue
        s = split_saving(r['cleared_gw'], r['price_usd_mw_day'],
                         r['cf_cleared_gw'], r['cf_price'])
        print('%-9s %11.2fB %11.2fB %9.1f%% %9.2fGW'
              % (r['season'], s['price'] / BN, s['volume'] / BN,
                 s['price'] / s['total'] * 100,
                 r['cleared_gw'] - r['cf_cleared_gw']))

    print()
    print('── 원문에 없는 값 ① 기가와트당 가격 지렛대 ' + '─' * 20)
    print('수요곡선을 1기가와트 왼쪽으로 밀면 낙찰 가격이 얼마나 내려가나.')
    print('%-9s %10s %14s %16s' % ('시즌', '민 폭', '내려간 가격', 'GW당 가격'))
    for r in auctions():
        if r['cf_price'] is None:
            continue
        drop = r['price_usd_mw_day'] - r['cf_price']
        print('%-9s %8.1fGW %13d$ %14.0f$'
              % (r['season'], r['shift_gw'], drop,
                 price_sensitivity(r['shift_gw'], drop)))
    print('  상수가 아니다. 공급곡선이 오른쪽 끝에서 수직이라 절벽의 높이가 다르다.')

    print()
    print('── 원문에 없는 값 ② 개선 둘이 겹치는 몫 ' + '─' * 22)
    o = overlap(ctx('cold_air_gw'), ctx('weatherize_gw'), ctx('combined_gw'))
    print('  찬 공기 %.1fGW + 내한 보강 %.1fGW = %.1fGW 인데 함께 세면 %.1fGW 다.'
          % (ctx('cold_air_gw'), ctx('weatherize_gw'), o['sum'], o['combined']))
    print('  겹치는 몫 %.1fGW, 합의 %.0f%% 다 — 둘이 같은 시간대를 고치기 때문이다.'
          % (o['overlap'], o['overlap_pct']))

    print()
    print('── 원문에 없는 값 ③ 주민 한 사람 몫 ' + '─' * 26)
    print('  낭비 %gB 를 주민 %g백만 명으로 나누면 한 사람에 %.0f달러다.'
          % (want_tot, ctx('residents'), per_person(want_tot * BN, ctx('residents'))))
    print('  모델이 낸 %.2fB 로 세면 %.0f달러다.'
          % (tot, per_person(tot * BN, ctx('residents'))))

    print()
    print('── 발표 합계가 어떤 용량을 전제하나 ' + '─' * 26)
    print('네 경매 합계와 지연 전 비용은 우리 식으로 안 맞는다. 거꾸로 풀어 본다.')
    pre = implied_capacity(ctx('pre_delay_cost') * BN, ctx('pre_delay_price'))
    print('  지연 전 %gB 를 %g달러로 나누면 용량이 %.0fGW 다 — 권역 설비보다 크다.'
          % (ctx('pre_delay_cost'), ctx('pre_delay_price'), pre))
    known = sum(auction_cost(r['cleared_gw'], r['price_usd_mw_day'])
                for r in auctions() if r['cleared_gw'] is not None) / BN
    print('  용량이 적힌 두 경매만 더하면 %.1fB 다. 발표 네 경매 합계는 %gB 다.'
          % (known, ctx('four_auction_total')))
    print('  나머지 두 경매의 용량이 안 적혀 있어 이 둘은 대조를 못 한다.')

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
