"""루프라인 모델을 원문 발표 숫자와 대조한다.

발표치는 원문 본문에 글로 적힌 값이고 `insights/models/raw/tables.json` 이 정본이다.
대조가 끝나면 원문이 안 낸 값을 낸다 — 공표된 능선이 함의하는 SRAM 대역폭,
그리고 그 능선에서 정사각 행렬이 언제 연산에 막히기 시작하나.

    PYTHONIOENCODING=utf-8 python insights/models/check_roofline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_raw, table                                   # noqa: E402
from roofline import (achieved_flops, area_mm2, arithmetic_intensity,  # noqa: E402
                      bound_by, implied_bandwidth, power_density,
                      ridge_point, shoreline_density, square_intensity)

RAW = load_raw('tables')
S = table(RAW, 'wse3-spec')
PF = 1e15
GB = 1e9
TB = 1e12


def v(key):
    return S['rows'][key][1]


def main():
    fails = 0

    def cmp(label, got, want, tol, unit=''):
        nonlocal fails
        ok = abs(got - want) <= tol
        fails += not ok
        print('  %-30s 모델 %12.4f  발표 %12.4f %s%s'
              % (label, got, want, unit, '' if ok else '  FAIL'))

    print('── 원문 값이 서로 어긋나지 않나 ' + '─' * 32)
    cmp('웨이퍼 면적 (mm²)', area_mm2(v('side_mm')), v('area_mm2'), 1)
    cmp('제곱센티미터당 전력 (W/cm²)',
        power_density(v('power_kw') * 1000, v('side_mm')), v('power_density'), 5)
    cmp('가장자리 밀도 (GB/s/mm)',
        shoreline_density(v('io_gbs'), v('side_mm')), v('io_per_mm'), 0.005)
    cmp('희소 대 조밀 배수', v('flops_sparse_pf') / v('flops_dense_pf'), 8, 0.01, '배')

    print()
    print('── 정사각 행렬의 산술 강도 — 원문 축약형이 맞나 ' + '─' * 16)
    print('  원문: 정사각이면 AI = (2/3)·(n/b), FP8(b=1) 이면 약 0.67n')
    for n in (64, 512, 4096):
        full = arithmetic_intensity(n, n, n, 1)
        short = square_intensity(n, 1)
        ok = abs(full - short) < 1e-9
        fails += not ok
        print('  n=%-6d 전체식 %10.2f  축약형 %10.2f  0.67n %10.2f%s'
              % (n, full, short, 0.67 * n, '' if ok else '  FAIL'))

    print()
    print('── 원문에 없는 값 ① 공표된 능선이 함의하는 SRAM 대역폭 ' + '─' * 10)
    print('능선 = 최대 연산량 ÷ 대역폭. 능선과 연산량을 알면 대역폭이 나온다.')
    bw = implied_bandwidth(v('flops_dense_pf') * PF, v('ridge'))
    print('  조밀 %g PFLOPS ÷ 능선 %g → SRAM 대역폭 %.1f PB/s (%.0f TB/s)'
          % (v('flops_dense_pf'), v('ridge'), bw / 1e15, bw / TB))
    print('  웨이퍼 밖 대역폭 %g GB/s 의 %.0f만 배다 — 안과 밖의 격차가 이만큼이다.'
          % (v('io_gbs'), bw / (v('io_gbs') * GB) / 10000))

    print()
    print('── 원문에 없는 값 ② 정사각 행렬은 언제 연산에 막히나 ' + '─' * 12)
    print('산술 강도가 능선을 넘는 크기를 푼다. AI = (2/3)(n/b) = 능선.')
    for b, name in ((1, 'FP8'), (2, 'FP16')):
        n_star = v('ridge') * 1.5 * b
        print('  %-5s 원소당 %d바이트 → n = %.2f 를 넘으면 연산에 막힌다' % (name, b, n_star))
    print('  즉 쓸 만한 크기의 정사각 행렬은 전부 연산에 막힌다.')
    print('  이 칩이 겨냥한 자리는 그 반대편, 배치가 아주 작은 디코드다.')

    print()
    print('── 원문에 없는 값 ③ 그 능선에서 디코드 커널은 어떻게 도나 ' + '─' * 8)
    print('원문이 든 예 — 배치 1, 산술 강도 2 인 디코드 커널.')
    peak = v('flops_dense_pf') * PF
    for ai in (0.5, 0.74, 2.0, 10.0):
        got = achieved_flops(peak, bw, ai)
        print('  AI %5.2f → %s에 막힘, 실현 %6.2f PFLOPS (최대의 %5.1f%%)'
              % (ai, bound_by(peak, bw, ai), got / PF, got / peak * 100))

    print()
    print('── 원문에 없는 값 ④ 가장자리 밀도를 거꾸로 풀면 ' + '─' * 16)
    nv = shoreline_density(v('io_gbs'), v('side_mm')) * v('nvidia_denser')
    print('  엔비디아가 %g배 촘촘하다면 그쪽은 mm당 %.1f GB/s 다.'
          % (v('nvidia_denser'), nv))
    print('  NVLink5 가 GPU 한 장에 %g GB/s 이므로, 그 칩의 유효 변 길이는 %.0f mm 다.'
          % (v('nvlink5_gbs'), v('nvlink5_gbs') / (4 * nv)))
    print('  웨이퍼는 변이 %g mm 인데 나르는 양은 그 %.2f 배뿐이다.'
          % (v('side_mm'), v('io_gbs') / v('nvlink5_gbs')))

    print('\n총 FAIL %d' % fails)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
