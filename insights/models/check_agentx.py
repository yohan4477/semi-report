"""AgentX 프런티어 모델을 루빈 원문 발표치와 대조한다.

발표치·칩 상수·매출 가정은 `insights/models/raw/inferencex_dsv4_agentx.json` 이 정본이다.
값을 맞추려고 가정을 손대지 않는다. 맞는 칸은 허용 오차를 넘으면 FAIL, 어긋난 칸은
모델 값과 차이를 찍고 넘어간다 — 어긋남으로 적어 둔 칸이 맞아 버려도 FAIL 이다.
본문이 「어긋난다」고 적은 채로 남으면 안 되기 때문이다.

    PYTHONIOENCODING=utf-8 python insights/models/check_agentx.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                        # noqa: E402
import agentx_frontier as AX                                             # noqa: E402

RAW = load_raw('inferencex_dsv4_agentx')
HW = table(RAW, 'agentx-hw')
PR = table(RAW, 'agentx-pricing')
SER = table(RAW, 'agentx-series')
PUB = table(RAW, 'agentx-published')

TOL = 0.01          # 맞는 칸의 상대 오차 — 원문이 두세 자리로 반올림해 적었다


def hw(k, col):
    return HW['rows'][k][HW['columns'].index(col)]


def pr(k):
    return PR['rows'][k][0]


def pub(k):
    return PUB['rows'][k][0]


def line(k):
    return PUB['rows'][k][1]


def series(key):
    h, fw, _ = SER['rows'][key]
    rows = [e for e in RAW['rows'] if e['hardware'] == h and e['framework'] == fw]
    return h, AX.frontier(rows)


S = {k: series(k) for k in SER['rows']}


def label(k):
    return SER['rows'][k][2]


def tput(k, s):
    return AX.at(S[k][1], s)


def permw(k, s):
    t = tput(k, s)
    return None if t is None else AX.tok_per_s_per_mw(t, hw(S[k][0], 'power_kw')) / 1e6


def perdollar(k, s, col):
    t = tput(k, s)
    return None if t is None else AX.tok_per_dollar(t, hw(S[k][0], col))


def own(a, b, s):
    return perdollar(a, s, 'costh') / perdollar(b, s, 'costh')


def rent(a, b, s):
    return perdollar(a, s, 'costr') / perdollar(b, s, 'costr')


def gw(k, s):
    h = S[k][0]
    price = {n: pr(n) for n in ('input_per_m', 'cached_input_per_m', 'output_per_m')}
    return AX.per_gw_year(S[k][1], h, s, hw(h, 'power_kw'), hw(h, 'costh'), price,
                          pr('utilization'), pr('hours_per_year'))


def daily_revenue(g, kw, gpus, avail):
    """기가와트당 연 매출을 GPU 한 시간 매출로 되돌려 함대 하루 매출로 곱한다."""
    per_gpu_hour = g['revenue'] / AX.gpu_hours_per_gw_year(kw, pr('hours_per_year'))
    return per_gpu_hour * gpus * 24 * avail


def best(fn, lo, hi):
    """lo~hi TPS 를 0.1 간격으로 훑어 가장 큰 배수와 그 속도."""
    return max((fn(x / 10), x / 10) for x in range(int(lo * 10), int(hi * 10) + 1))


class Tally:
    def __init__(self):
        self.fails = 0
        self.gaps = 0

    def match(self, name, got, key, fmt='%.3g', pp=False):
        """pp=True 면 퍼센트 칸이라 상대 오차 대신 1퍼센트포인트 안을 본다."""
        want = pub(key)
        ok = got is not None and (abs(got - want) <= 1 if pp else abs(got / want - 1) <= TOL)
        self.fails += not ok
        print('  %-30s 모델 %s · 발표 %s (L%d)%s'
              % (name, 'N/A' if got is None else fmt % got, fmt % want, line(key),
                 '' if ok else '  FAIL'))

    def gap(self, name, got, key, why, fmt='%.3g'):
        want = pub(key)
        if got is not None and abs(got / want - 1) <= TOL:
            self.fails += 1
            print('  %-30s 모델 %s · 발표 %s (L%d)  어긋남으로 적은 칸이 맞았다 — 본문을 고칠 것  FAIL'
                  % (name, fmt % got, fmt % want, line(key)))
            return
        self.gaps += 1
        diff = '' if got is None else ' %+.1f%%' % ((got / want - 1) * 100)
        print('  %-30s 모델 %s · 발표 %s (L%d)  어긋남%s — %s'
              % (name, 'N/A' if got is None else fmt % got, fmt % want, line(key), diff, why))


def main():
    t = Tally()

    print('── 100 TPS 에서 1메가와트당 토큰 (백만 tok/s) ' + '─' * 22)
    for key in ('vr', 'gb300_sgl', 'gb300_trt', 'mi355x', 'b200', 'b300', 'h200'):
        t.match(label(key), permw(key, 100), 'permw100_' + key)
    t.match('루빈 ÷ GB300 SGLang', permw('vr', 100) / permw('gb300_sgl', 100), 'x100_vr_sgl')
    t.match('루빈 ÷ MI355X', permw('vr', 100) / permw('mi355x', 100), 'x100_vr_mi')

    print()
    print('── 다른 속도에서 1메가와트당 토큰 ' + '─' * 34)
    t.match('150 TPS 루빈', permw('vr', 150), 'permw150_vr')
    t.match('170 TPS 루빈 ÷ GB300 TRT', permw('vr', 170) / permw('gb300_trt', 170),
            'x170_vr_trt_mw')
    why = 'GB300 SGLang 곡선은 09-11·13·14·17 스냅숏에서 같다'
    for s, key in ((150, 'x150_vr_sgl'), (170, 'x170_vr_sgl_mw'), (200, 'x200_vr_sgl')):
        t.gap('%d TPS 루빈 ÷ GB300 SGLang' % s, permw('vr', s) / permw('gb300_sgl', s), key, why)

    print()
    print('── 곡선의 끝 ' + '─' * 55)
    t.match('루빈 최고 P90 속도', max(AX._x(e) for e in S['vr'][1]), 'maxint_vr', '%.2f')
    t.match('GB300 TRT 최고 P90 속도', max(AX._x(e) for e in S['gb300_trt'][1]),
            'maxint_gb300_trt', '%.2f')

    print()
    print('── 1달러당 토큰 — 사서 운영할 때 ' + '─' * 34)
    t.gap('170 TPS 루빈 ÷ GB300 TRT', own('vr', 'gb300_trt', 170), 'x170_vr_trt_own',
          '곡선 끝 171.53 바로 앞이라 속도 1 에 배수가 3 넘게 움직인다')
    for s in (169, 170, 171, 171.4):
        print('    %6.1f TPS  %.1f배' % (s, own('vr', 'gb300_trt', s)))
    lo, hi = own('vr', 'gb300_trt', 75), own('vr', 'gb300_trt', 100)
    ok = pub('own_range_lo') <= lo * 1.01 and hi <= pub('own_range_hi')
    t.fails += not ok
    print('  %-30s 모델 %.2f~%.2f · 발표 %g~%g (L%d)%s'
          % ('75~100 TPS 루빈 ÷ GB300 TRT', lo, hi, pub('own_range_lo'), pub('own_range_hi'),
             line('own_range_lo'), '' if ok else '  FAIL'))
    print('    루빈 곡선이 74 TPS 에서 끝나 원문의 60 TPS 쪽은 잴 수 없다.')
    t.gap('80 TPS 루빈 ÷ B300 vLLM', own('vr', 'b300', 80), 'own80_vr_b300',
          '원문이 「B300」 이라고만 적었다')

    print()
    print('── 1달러당 토큰 — 3년 약정으로 빌릴 때 ' + '─' * 28)
    t.gap('80 TPS 루빈 ÷ GB300 SGLang (%)', (rent('vr', 'gb300_sgl', 80) - 1) * 100,
          'rent80_more_pct', '원문이 엔진을 안 적었다. TRT 대비는 %.0f%%'
          % ((rent('vr', 'gb300_trt', 80) - 1) * 100), '%.0f')
    b_trt = best(lambda s: rent('vr', 'gb300_trt', s), 75, 171.5)
    b_sgl = best(lambda s: rent('vr', 'gb300_sgl', s), 75, 276.2)
    t.gap('최대 배수 (SGLang 대비)', b_sgl[0], 'rent_hi_max',
          '%.1f TPS 에서. TRT 대비 최대는 %.0f배(%.1f TPS)' % (b_sgl[1], b_trt[0], b_trt[1]))

    print()
    print('── 75 TPS · 가동률 60% 에서 기가와트당 연 매출·이익 (십억 달러) ' + '─' * 6)
    g_vr, g_sgl, g_trt = gw('vr', 75), gw('gb300_sgl', 75), gw('gb300_trt', 75)
    for name, g in (('루빈', g_vr), ('GB300 SGLang', g_sgl), ('GB300 TRT', g_trt)):
        print('    %-12s 처리량 %6.0f · 캐시 적중 %.3f · 입력 몫 %.4f · 섞은 단가 $%.4f/M'
              % (name, g['tput'], g['hit'], g['share'], g['price']))
    t.match('루빈 매출', g_vr['revenue'] / 1e9, 'rev_vr', '%.4g')
    t.match('루빈 이익', g_vr['profit'] / 1e9, 'profit_vr', '%.4g')
    t.match('GB300 SGLang 매출', g_sgl['revenue'] / 1e9, 'rev_gb300_sgl', '%.4g')
    t.match('GB300 SGLang 이익', g_sgl['profit'] / 1e9, 'profit_gb300_sgl', '%.4g')
    t.match('GB300 TRT 매출', g_trt['revenue'] / 1e9, 'fleet_gwyr_trt', '%.5g')
    t.match('이익 차이', (g_vr['profit'] - g_sgl['profit']) / 1e9, 'profit_gap')
    t.match('매출 더 (%)', (g_vr['revenue'] / g_sgl['revenue'] - 1) * 100, 'rev_more_pct', '%.2g', pp=True)
    t.match('이익 더 (%)', (g_vr['profit'] / g_sgl['profit'] - 1) * 100, 'profit_more_pct', '%.2g', pp=True)
    t.match('값을 내릴 여력 (%)', (1 - g_sgl['revenue'] / g_vr['revenue']) * 100,
            'price_cut_pct', '%.2g', pp=True)

    print()
    print('── 10메가와트 함대 ' + '─' * 49)
    av = AX.availability(pr('mtbi_days'), pr('recovery_hours'))
    kw_trt, kw_vr = hw('gb300', 'power_kw'), hw('vr200', 'power_kw')
    n_trt, n_vr = AX.fleet_gpus(10, kw_trt), AX.fleet_gpus(10, kw_vr)
    d_trt = daily_revenue(g_trt, kw_trt, n_trt, av) / 1e6
    d_vr = daily_revenue(g_vr, kw_vr, n_vr, av) / 1e6
    print('    가용률 %.4f (고장 간격 %g일 · 복구 %g시간) · 루빈 %d장'
          % (av, pr('mtbi_days'), pr('recovery_hours'), n_vr))
    t.match('GB300 장수', n_trt, 'fleet_gpus', '%d')
    t.match('GB300 칩당 전력 (kW)', kw_trt, 'fleet_kw', '%.2f')
    t.match('GB300 TRT 하루 매출 ($M)', d_trt, 'fleet_daily_trt')
    t.match('루빈 하루 매출 ($M)', d_vr, 'fleet_daily_vr', '%.2g')
    t.match('루빈 ÷ GB300 TRT', d_vr / d_trt, 'fleet_ratio', '%.2g')

    print('\n맞는 칸 FAIL %d · 적어 둔 어긋남 %d' % (t.fails, t.gaps))
    print('총 FAIL %d' % t.fails)
    return 1 if t.fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
