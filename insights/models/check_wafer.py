"""웨이퍼 사슬 모델을 원문 발표치와 대조한다.

계수는 우주영문 본문 값이고, 여기에 들어가는 기가와트는 앞 층들이 낸 값이다.
프레임 값(빅4 자본지출)은 우리 코퍼스 대조를 안 거쳤으므로 그렇게 표시한다.

    PYTHONIOENCODING=utf-8 python insights/models/check_wafer.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                    # noqa: E402
from wafer_chain import (hbm_bit_penalty, implied_global,             # noqa: E402
                         implied_tsmc, memory_wafers, share_of_global,
                         value_share, wafer_value, wafers_from_gw, wspm)
from bridge_capex import implied_gw                                   # noqa: E402

RAW = load_raw('capex')
W = table(RAW, 'wafer-coef')
S = table(RAW, 'frame-sheet')
SC = table(RAW, 'frame-scn')
X = table(RAW, 'spacex-econ')


def w(k):
    return W['rows'][k][1]


def main():
    fails = 0

    print('── 원문이 흘려 적은 값 둘로 TSMC 출력을 되짚는다 ' + '─' * 14)
    a = implied_tsmc(w('tw_wafers') * 1e6, w('tw_multiple')) / 12 / 1e6
    b = w('terafab_full') * 1e6 / (w('terafab_tsmc_share') / 100.0) / 1e6
    ok = abs(a - b) / b <= 0.05
    fails += not ok
    print('  1테라와트 = 연 %g백만 장 = TSMC 출력의 %g배 → TSMC 월 %.2f백만 장'
          % (w('tw_wafers'), w('tw_multiple'), a))
    print('  테라팹 월 %g백만 장 = TSMC 하나의 %g%% → TSMC 월 %.2f백만 장'
          % (w('terafab_full'), w('terafab_tsmc_share'), b))
    print('  서로 다른 문단의 두 값이 %.1f%% 안에서 만난다%s'
          % (abs(a - b) / b * 100, '' if ok else '  FAIL'))

    g = implied_global(w('terafab_entry') * 1000, w('terafab_entry_share')) / 1e6
    ok2 = abs(g - w('global_wspm')) <= 0.1
    fails += not ok2
    print('  테라팹 초기 %g천 장이 세계의 %g%% → 세계 월 %.1f백만 장, 원문 %g%s'
          % (w('terafab_entry'), w('terafab_entry_share'), g, w('global_wspm'),
             '' if ok2 else '  FAIL'))

    print()
    print('── 사슬 — 자본지출이 웨이퍼가 되기까지 ' + '─' * 26)
    capex = S['rows']['total_2026'][1]
    per_mw = X['rows']['capex_per_gw'][1]
    gw = implied_gw(capex, per_mw)
    ann = wafers_from_gw(gw, w('wafers_per_gw'))
    mo = wspm(ann)
    print('  빅4 2026년 자본지출 %g십억 달러(프레임 값)를 MW당 %g백만 달러로 나누면'
          % (capex, per_mw))
    print('  %.1f기가와트다. 거기에 기가와트당 %s장을 곱하면 연 %.2f백만 장이고'
          % (gw, format(w('wafers_per_gw'), ','), ann / 1e6))
    print('  월 %.0f천 장이다. 세계 300밀리 용량 %g백만 장의 %.1f%% 다.'
          % (mo / 1000, w('global_wspm'), share_of_global(mo, w('global_wspm') * 1e6)))

    print()
    print('── 웨이퍼 가치는 자본지출의 몇 할인가 ' + '─' * 28)
    val = wafer_value(gw, w('value_per_gw'))
    print('  기가와트당 %g십억 달러를 곱하면 %.1f십억 달러다.' % (w('value_per_gw'), val))
    print('  빅4 자본지출의 %.1f%%, 서버·칩 %g십억의 %.1f%% 다.'
          % (value_share(val, capex), S['rows']['server_2026'][1],
             value_share(val, S['rows']['server_2026'][1])))

    print()
    print('── 메모리가 그 가운데 얼마인가 ' + '─' * 34)
    mem = memory_wafers(ann, w('memory_share'))
    mem_val = val * w('memory_share') / 100.0
    print('  메모리가 %g%% 를 넘으므로 연 %.2f백만 장, 값으로 %.1f십억 달러 위다.'
          % (w('memory_share'), mem / 1e6, mem_val))
    hbm = S['rows']['hbm_value'][1]
    print('  프레임 엑셀이 낸 2026년 HBM 금액은 %g십억 달러다.' % hbm)
    print('  두 값의 차이가 %.1f%% 다 — 서로 다른 재료에서 온 값이 같은 자리에 선다.'
          % (abs(mem_val - hbm) / hbm * 100))
    print('  같다고는 못 한다. 메모리 웨이퍼에는 범용 D램도 들어 있고, HBM 금액에는')
    print('  웨이퍼 밖의 조립과 시험이 들어 있다.')

    print()
    print('── HBM 은 같은 비트에 웨이퍼를 세 배 먹는다 ' + '─' * 22)
    print('  범용 D램 100장어치 비트를 HBM 으로 만들면 %g장이 든다(우주영문 L316).'
          % hbm_bit_penalty(100, w('hbm_bit_multiple')))
    print('  그래서 메모리가 웨이퍼의 절반을 넘는다 — 값이 아니라 장수로 세는 자리다.')
    print('  AI 수요가 TSMC N3 출력에서 차지하는 몫은 2026년 %g%% 미만, 2027년 %g%% 다.'
          % (w('n3_2026'), w('n3_2027')))

    print()
    print('── 케이스 셋을 웨이퍼로 옮기면 ' + '─' * 34)
    print('%-8s %12s %12s %14s %12s'
          % ('케이스', '2030년 자본', '기가와트', '연 웨이퍼', '세계 몫'))
    for k in ('capex_bear', 'capex_base', 'capex_bull'):
        r = SC['rows'][k]
        v = r[5]
        g2 = implied_gw(v, per_mw)
        a2 = wafers_from_gw(g2, w('wafers_per_gw'))
        print('%-8s %10g십억 %9.1f GW %11.2f백만 %10.1f%%'
              % (r[0], v, g2, a2 / 1e6,
                 share_of_global(wspm(a2), w('global_wspm') * 1e6)))
    print('  세계 용량이 2025년 그대로라고 놓은 값이다. 실제로는 늘어난다.')

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
