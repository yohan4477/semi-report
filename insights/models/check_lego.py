"""모듈러 자본지출 모델을 원문 발표치와 대조한다.

발표치는 `insights/models/raw/capex.json` 이 정본이고 전부 원문 본문에 글로
적힌 값이다. 값을 맞추려고 가정을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_lego.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                  # noqa: E402
from lego_capex import (content_share, delta_pct, early_revenue,    # noqa: E402
                        explained_share, labor_saving, months_cut)

RAW = load_raw('capex')
C = table(RAW, 'lego-cost')
L = table(RAW, 'lego-labor')
S = table(RAW, 'lego-schedule')
P = table(RAW, 'lego-power-only')
G = table(RAW, 'ground-assump')


def c(k):
    return C['rows'][k][1]


def lb(k):
    return L['rows'][k][1]


def po(k):
    return P['rows'][k][1]


def main():
    fails = 0

    print('── 발표된 차이를 다시 낸다 ' + '─' * 38)
    got = delta_pct(c('stick_all_in'), c('modular_all_in'))
    want = c('stated_pct')
    ok = abs(got - want) <= 0.5
    fails += not ok
    print('  현장시공 %.1f 백만 달러/MW · 모듈러 %.1f — 차이 %.1f, %.2f%%'
          % (c('stick_all_in'), c('modular_all_in'),
             c('stick_all_in') - c('modular_all_in'), got))
    print('  원문이 적은 값 %g%% %s' % (want, '' if ok else ' FAIL'))

    add = c('svc_saving') + c('install_saving')
    ok2 = abs(add - c('stated_delta')) <= 0.01
    fails += not ok2
    print('  절감 항목 둘을 더하면 %.1f 이고 발표된 차이는 %.1f 다%s'
          % (add, c('stated_delta'), '' if ok2 else '  FAIL'))

    print()
    print('── 원문에 없는 값 ① 그 차이 가운데 인건비는 얼마인가 ' + '─' * 12)
    s = labor_saving(lb('hours_field'), lb('hours_after'),
                     lb('wage_field_eff'), lb('wage_factory'))
    print('  현장 인시 %s 시간에 실질 임금 %g달러를 곱하면 MW당 %s 달러다.'
          % (format(lb('hours_field'), ','), lb('wage_field_eff'),
             format(int(s['before']), ',')))
    print('  옮긴 뒤는 남은 %s 시간 × %g달러 + 옮긴 %s 시간 × 공장 %g달러 = %s 달러다.'
          % (format(lb('hours_after'), ','), lb('wage_field_eff'),
             format(s['moved_hours'], ','), lb('wage_factory'),
             format(int(s['after']), ',')))
    share = explained_share(s['saving'], c('stated_delta'))
    print('  아끼는 인건비는 MW당 %s 달러이고, 발표된 차이 %s 달러의 %.0f%% 다.'
          % (format(int(s['saving']), ','),
             format(int(c('stated_delta') * 1e6), ','), share))
    rest = c('stated_delta') * 1e6 - s['saving']
    print('  나머지는 MW당 %s 달러, %.0f%% 다 — 인건비가 아니다. 원문은 공기가 짧아져'
          % (format(int(rest), ','), 100 - share))
    print('  에스컬레이션과 컨틴전시와 현장관리비가 준다고 적었다(레고영문 L563).')

    print()
    print('── 원문에 없는 값 ② 시간이 준 만큼 값이 주나 ' + '─' * 20)
    hour_cut = (lb('hours_field') - lb('hours_after')) / lb('hours_field') * 100
    print('  현장 시간은 %.0f%% 줄고(원문 %g%%), 원가는 %.1f%% 준다.'
          % (hour_cut, lb('cut_pct'), got))
    print('  시간이 준 폭이 원가가 준 폭의 %.1f 배다 — 옮긴 시간이 공장 임금으로'
          % (hour_cut / got))
    print('  다시 붙고, 인건비가 총원가에서 차지하는 몫이 작기 때문이다.')

    print()
    print('── 공기 ' + '─' * 56)
    print('%-14s %10s %10s %12s' % ('방식', '공사(하한)', '공사(상한)', '허가 포함'))
    for k, v in S['rows'].items():
        name, lo, hi, alo, ahi, _cite = v
        span = '%g~%g개월' % (alo, ahi) if alo else '—'
        print('%-14s %8g개월 %8g개월 %12s' % (name, lo, hi, span))
    cut_lo = months_cut(S['rows']['stick'][1], S['rows']['modular'][1])
    cut_hi = months_cut(S['rows']['stick'][2], S['rows']['modular'][2])
    print('  공사만 보면 %.0f~%.0f%% 짧다. 원문은 36%% 라고 적었다(레고영문 L44).'
          % (cut_hi, cut_lo))

    got_po = months_cut(po('months_stick'), po('months_modular'))
    ok3 = abs(got_po - po('cut_pct')) <= 1.0
    fails += not ok3
    print('  전력 스코프만 옮기면 %.1f개월에서 %g개월로 %.0f%% 짧다 — 원문 %g%%%s'
          % (po('months_stick'), po('months_modular'), got_po, po('cut_pct'),
             '' if ok3 else '  FAIL'))

    print()
    print('── 원문에 없는 값 ③ 앞당긴 달이 버는 매출 ' + '─' * 22)
    print('  MW당 매출은 이 원문에 없다. 지상 데이터센터 층의 값을 빌린다(우주영문 L288).')
    for months in (7, 9):
        for rev in (G['rows']['rev_lo'][1], G['rows']['rev_hi'][1]):
            v = early_revenue(months, 1, rev)
            print('    %d개월 일찍 켜면 MW당 %.1f 백만 달러를 먼저 받는다 (연 %g 기준)'
                  % (months, v, rev))
    save = c('stated_delta')
    lo = early_revenue(7, 1, G['rows']['rev_lo'][1])
    print('  가장 낮게 잡아도 %.1f 이고, 아끼는 자본 %.1f 의 %.1f 배다.'
          % (lo, save, lo / save))
    print('  매출이지 이익이 아니다 — 그 매출에서 전기와 인건비와 GPU 값이 나간다.')

    print()
    print('── 원문에 없는 값 ④ 벤더 하나가 MW당 총원가에서 가져가는 몫 ' + '─' * 4)
    a = content_share(c('vertiv_discrete'), c('stick_all_in'))
    b = content_share(c('vertiv_fullstack'), c('modular_all_in'))
    print('  낱개 장비 %.1f 를 현장시공 총원가 %.1f 로 나누면 %.0f%% 다.'
          % (c('vertiv_discrete'), c('stick_all_in'), a))
    print('  풀스택 %.1f 를 모듈러 총원가 %.1f 로 나누면 %.0f%% 다.'
          % (c('vertiv_fullstack'), c('modular_all_in'), b))
    print('  총원가는 %.1f%% 줄었는데 한 벤더의 몫은 %.0f%%p 늘었다.' % (got, b - a))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
