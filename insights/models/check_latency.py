"""지연 모델을 원문 값과 대조하고, 원문이 안 낸 값을 낸다.

원문이 낸 것은 식 하나와 처리량 다섯 개뿐이다. 식은 항등식이라 대조할 발표치가
없으므로, 원문 값이 이 식 안에서 서로 어긋나지 않는지를 본다. 그다음 리틀의 법칙과
TCO 모델을 물려 원문이 안 낸 값을 낸다.

    PYTHONIOENCODING=utf-8 python insights/models/check_latency.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                   # noqa: E402
from latency_model import (concurrency_per_gpu, cost_per_million_tokens,  # noqa: E402
                           e2e_latency_s, interactivity, tbot_from_e2e)
import check_inference_tco as I                                      # noqa: E402

RAW = load_raw('tables')
ANCHOR = table(RAW, 'amd-throughput-anchors')
COLS = ANCHOR['columns']
OUT_TOKENS = {'1k/1k': 1000, '1k/4k': 4000, '4k/1k': 1000}


def rows():
    for key, v in ANCHOR['rows'].items():
        yield key, dict(zip(COLS, v))


def hourly(sku):
    """그 SKU 의 자기 TCO 시간당 원가. 추론 원가 모델에서 온다."""
    for s in I.SKUS:
        if s.name == sku:
            from inference_tco import Capex, Sku
            fixed = Sku(s.name, Capex(s.capex.server_cost, s.capex.other_cluster_cost,
                                      wacc=0.1325), s.opex)
            return fixed.tco_hourly_per_gpu()
    raise KeyError(sku)


def main():
    print('── 원문이 낸 것 — 식 하나와 처리량 다섯 ' + '─' * 24)
    print('E2E 지연 = 첫 토큰까지 시간 + 출력 토큰 수 × 토큰 사이 시간 (AMD영문 L98)')
    print('%-16s %-7s %-14s %-9s %10s %9s  %s'
          % ('모델', '길이', '엔진', 'SKU', '토큰/초/GPU', '지연(초)', '인용'))
    for _k, r in rows():
        print('%-16s %-7s %-14s %-9s %10s %9s  %s'
              % (r['model'], r['seq'], r['engine'], r['sku'],
                 format(r['tokens_per_s_per_gpu'], ','),
                 '—' if r['latency_s'] is None else r['latency_s'], r['cite']))

    print()
    print('── 식이 서로 어긋나지 않나 ' + '─' * 36)
    print('항등식이라 대조할 발표치가 없다. 원문 값을 넣어 되돌아오는지만 본다.')
    fails = 0
    for _k, r in rows():
        if r['latency_s'] is None:
            continue
        osl = OUT_TOKENS[r['seq']]
        tbot = tbot_from_e2e(r['latency_s'], osl, 0.0)
        back = e2e_latency_s(0.0, osl, tbot)
        ok = abs(back - r['latency_s']) < 1e-9
        fails += not ok
        print('  %-9s 지연 %ds · 출력 %d토큰 → 토큰 사이 %.1fms → 되돌리면 %.1fs%s'
              % (r['sku'], r['latency_s'], osl, tbot * 1000, back,
                 '' if ok else '  FAIL'))

    print()
    print('── 원문이 안 낸 값 ① 그 운영점의 대화 속도 ' + '─' * 20)
    print('첫 토큰까지 시간을 0 으로 놓은 값이다 — 원문이 그 값을 안 밝혔다.')
    print('실제 첫 토큰 시간이 있으면 대화 속도는 이보다 조금 빨라진다.')
    print('%-9s %-7s %12s %14s %18s' % ('SKU', '길이', '지연(초)', '토큰 사이(ms)',
                                        '대화 속도(토큰/초)'))
    for _k, r in rows():
        if r['latency_s'] is None:
            continue
        osl = OUT_TOKENS[r['seq']]
        tbot = tbot_from_e2e(r['latency_s'], osl, 0.0)
        print('%-9s %-7s %12d %14.1f %18.1f'
              % (r['sku'], r['seq'], r['latency_s'], tbot * 1000, interactivity(tbot)))

    print()
    print('── 원문이 안 낸 값 ② GPU 한 장이 붙들고 있는 요청 수 ' + '─' * 12)
    print('리틀의 법칙 — 처리량 ÷ 요청당 출력 토큰 × 지연.')
    print('%-9s %-14s %12s %16s' % ('SKU', '엔진', '토큰/초/GPU', '동시 요청/GPU'))
    for _k, r in rows():
        if r['latency_s'] is None:
            continue
        osl = OUT_TOKENS[r['seq']]
        c = concurrency_per_gpu(r['tokens_per_s_per_gpu'], osl, r['latency_s'])
        print('%-9s %-14s %12s %16.0f'
              % (r['sku'], r['engine'], format(r['tokens_per_s_per_gpu'], ','), c))

    print()
    print('── 원문이 안 낸 값 ③ 그 운영점의 백만 토큰당 원가 ' + '─' * 14)
    print('시간당 원가는 추론 원가 모델에서 온다(자기 TCO, WACC 13.25%).')
    print('%-9s %-14s %12s %12s %14s' % ('SKU', '엔진', '토큰/초/GPU', '$/GPU-시간',
                                         '$/백만 토큰'))
    costs = []
    for _k, r in rows():
        try:
            h = hourly(r['sku'])
        except KeyError:
            continue
        c = cost_per_million_tokens(h, r['tokens_per_s_per_gpu'])
        costs.append((r, h, c))
        print('%-9s %-14s %12s %12.2f %14.3f'
              % (r['sku'], r['engine'], format(r['tokens_per_s_per_gpu'], ','), h, c))

    print()
    print('── 같은 워크로드 안에서 견준다 ' + '─' * 32)
    print('Llama3 405B FP8 · 1k/1k · 지연 150초 — 원문이 두 값을 한 자리에서 말했다.')
    pair = {r['sku'] + '·' + r['engine']: (r, h, c) for r, h, c in costs
            if r['latency_s'] == 150}
    if len(pair) == 2:
        (n1, (r1, h1, c1)), (n2, (r2, h2, c2)) = sorted(pair.items(), key=lambda x: x[1][2])
        print('  %s 가 %s 보다 토큰당 %.2f 배 싸다 (%.3f 대 %.3f 달러)'
              % (n1, n2, c2 / c1, c1, c2))
        print('  처리량은 %.2f 배인데 시간당 원가는 %.2f 배라 그렇다.'
              % (r1['tokens_per_s_per_gpu'] / r2['tokens_per_s_per_gpu'], h1 / h2))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
