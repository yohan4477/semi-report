"""추론 원가 모델을 원문 발표 숫자와 대조한다.

발표 숫자는 표 그림 049·050·016 에서 읽은 것이다. 값을 맞추려고 가정을
손대지 않는다. 뒤이어 원문이 안 낸 두 가지를 모델로 낸다 — 발표된 손익
분기 임대료가 함의하는 상대 처리량, 그리고 사서 쓸 때의 처리량 문턱.

    PYTHONIOENCODING=utf-8 python insights/models/check_inference_tco.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_raw, table                                    # noqa: E402
from inference_tco import (Capex, Opex, Sku, implied_throughput_ratio,  # noqa: E402
                           implied_wacc)

# 발표치는 코드에 안 적는다. 그림에서 읽은 값은 `insights/models/raw/tables.json`
# 이 정본이고 여기서는 그것을 읽는다 — 두 곳에 적으면 갈린다(check_model M3).
_RAW = load_raw('tables')
_CAPEX = table(_RAW, 'amd-capex')
_OPEX = table(_RAW, 'amd-opex')
_TCO = table(_RAW, 'amd-tco')
NAMES = _CAPEX['columns']


def _v(t, row):
    """표 한 줄을 SKU 차례대로. 원자료의 열 차례가 곧 이 목록의 차례다."""
    return t['rows'][row]


SKUS = [Sku(n,
            Capex(_v(_CAPEX, 'server_cost')[i], _v(_CAPEX, 'other_cluster_cost')[i]),
            Opex(_v(_OPEX, 'power_kw')[i]))
        for i, n in enumerate(NAMES)]

# (선불/서버, 선불/GPU, 월자본, 자본$/hr, 호스팅/월, 운영/월, 운영/GPU,
#  운영$/hr, TCO$/hr, 자본비중) — 전부 그림에서 읽어 원자료에 옮긴 값이다
PUBLISHED = {
    n: (_v(_CAPEX, 'upfront_per_server')[i], _v(_CAPEX, 'upfront_per_gpu')[i],
        _v(_CAPEX, 'monthly_capital')[i], _v(_CAPEX, 'hourly_per_gpu')[i],
        _v(_OPEX, 'hosting_per_server_month')[i], _v(_OPEX, 'monthly_per_server')[i],
        _v(_OPEX, 'monthly_per_gpu')[i], _v(_OPEX, 'hourly_per_gpu')[i],
        _v(_TCO, 'total_hourly_per_gpu')[i], _v(_TCO, 'capital_share_pct')[i])
    for i, n in enumerate(NAMES)
}

FIELDS = [
    ("선불/서버", lambda s: s.capex.upfront_per_server(), 1.0),
    ("선불/GPU", lambda s: s.capex.upfront_per_gpu(), 1.0),
    ("월자본/서버", lambda s: s.capex.monthly_per_server(), 5.0),
    ("자본$/hr", lambda s: s.capex.hourly_per_gpu(), 0.005),
    ("호스팅/월", lambda s: s.opex.hosting_per_server_month(), 1.0),
    ("운영/월", lambda s: s.opex.monthly_per_server(), 1.0),
    ("운영/GPU", lambda s: s.opex.monthly_per_gpu(), 0.5),
    ("운영$/hr", lambda s: s.opex.hourly_per_gpu(), 0.005),
    ("TCO$/hr", lambda s: s.tco_hourly_per_gpu(), 0.005),
    ("자본비중%", lambda s: s.capital_share(), 0.05),
]

# 원문이 글로 밝힌 손익분기 임대료. 이것도 원자료가 정본이다
_RENT = table(_RAW, 'amd-rental-breakeven')
H200_RENTAL = _RENT['reference']['rental_hr']
BREAKEVEN = [(work, sku, lo, hi)
             for work, per in _RENT['rows'].items()
             for sku, (lo, hi) in sorted(
                 (k, v) for k, v in per.items() if isinstance(v, list))]


def main() -> int:
    fails = 0
    print("── 자본지출·운영비 재현 (그림 049·050·016) " + "─" * 24)
    print(f"{'SKU':10}", "  ".join(f"{n:>11}" for n, _, _ in FIELDS))
    for sku in SKUS:
        want = PUBLISHED[sku.name]
        cells = []
        for i, (label, fn, tol) in enumerate(FIELDS):
            got = fn(sku)
            ok = abs(got - want[i]) <= tol
            if not ok:
                fails += 1
            cells.append(f"{got:>11,.2f}{'' if ok else '!'}")
        print(f"{sku.name:10}", "  ".join(cells))
    print(f"  어긋난 칸: {fails}  (전부 월 자본비 계열. 아래에서 원인을 캔다)")

    print()
    print("── 어긋남의 원인 — 표에 찍힌 13.3% 는 반올림값이다 " + "─" * 16)
    print(f"{'SKU':10} {'발표 월자본':>12} {'13.3% 로 계산':>14} {'차이비율':>10} {'역산 WACC':>11}")
    rates = []
    for sku in SKUS:
        want = PUBLISHED[sku.name][2]
        got = sku.capex.monthly_per_server()
        r = implied_wacc(sku.capex.upfront_per_server(), want,
                         sku.capex.useful_life_years)
        rates.append(r)
        print(f"{sku.name:10} {want:>12,.0f} {got:>14,.2f} "
              f"{want / got - 1:>9.4%} {r:>10.4%}")
    print(f"  역산값 범위 {min(rates):.4%} ~ {max(rates):.4%}"
          f" — 여섯 SKU 가 한 값으로 모인다. 실제 WACC 는 13.25% 다.")

    print()
    print("── 13.25% 를 넣고 다시 대조한다 " + "─" * 32)
    refit = [Sku(s.name, Capex(s.capex.server_cost, s.capex.other_cluster_cost,
                               wacc=0.1325), s.opex) for s in SKUS]
    refails = 0
    for sku in refit:
        want = PUBLISHED[sku.name]
        bad = [label for i, (label, fn, tol) in enumerate(FIELDS)
               if abs(fn(sku) - want[i]) > tol]
        refails += len(bad)
        if bad:
            print(f"  {sku.name:10} 남은 칸: {', '.join(bad)}")
    print(f"  어긋난 칸: {fails} → {refails}")

    by = {s.name: s for s in refit}
    h200 = by["H200 SXM"]

    print()
    print("── 발표된 손익분기 임대료가 함의하는 상대 처리량 " + "─" * 18)
    print("H200 1개월 임대 $2.5/hr/GPU 기준. 임대료 비율이 곧 처리량 비율이다.")
    print(f"{'작업 성격':16} {'SKU':8} {'손익분기 임대료':>16} {'함의 처리량(H200=1)':>20}")
    for workload, name, lo, hi in BREAKEVEN:
        r_lo = implied_throughput_ratio(H200_RENTAL, lo)
        r_hi = implied_throughput_ratio(H200_RENTAL, hi)
        price = f"${lo:.2f}" if lo == hi else f"${lo:.2f}~${hi:.2f}"
        ratio = f"{r_lo:.2f}" if lo == hi else f"{r_lo:.2f}~{r_hi:.2f}"
        print(f"{workload:16} {name:8} {price:>16} {ratio:>20}")

    print()
    print("── 사서 쓰면 문턱이 어디로 옮겨지나 " + "─" * 28)
    print("빌리는 값이 아니라 자기 TCO 로 견주면, 토큰당 원가가 같아지는")
    print("처리량 비율이 달라진다. 이 문턱을 넘으면 AMD 가 싸다.")
    print(f"{'SKU':10} {'TCO $/hr':>10} {'H200 대비 문턱':>16}")
    for name in ("MI300X", "MI325X", "MI355X", "H100 SXM", "B200"):
        s = by[name]
        thr = s.tco_hourly_per_gpu() / h200.tco_hourly_per_gpu()
        print(f"{name:10} {s.tco_hourly_per_gpu():>10.2f} {thr:>16.2f}")

    print()
    print("── 두 문턱을 견준다 " + "─" * 40)
    own_threshold = by["MI300X"].tco_hourly_per_gpu() / h200.tco_hourly_per_gpu()
    print(f"MI300X 를 사서 쓸 때 넘어야 할 처리량 비율: {own_threshold:.2f}")
    for workload, name, lo, hi in BREAKEVEN:
        if name != "MI300X":
            continue
        r_lo = implied_throughput_ratio(H200_RENTAL, lo)
        r_hi = implied_throughput_ratio(H200_RENTAL, hi)
        if r_hi < own_threshold:
            verdict = "빌려도 사도 H200 이 싸다"
        elif r_lo > own_threshold:
            verdict = "사서 쓰면 MI300X 가 싸다"
        else:
            verdict = "문턱을 걸친다 — 작업 조건이 가른다"
        print(f"  {workload:16} 실측 처리량 {r_lo:.2f}~{r_hi:.2f}  →  {verdict}")

    print(f"\n총 FAIL {fails}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
