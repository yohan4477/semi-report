"""GPU 클러스터 TCO 모델을 원문 발표 숫자와 대조한다.

발표 숫자는 표 그림 016·019·022·025 에서 읽은 것이다. 모델이 그 값을
다시 내면 재현 성공, 못 내면 어긋난 자리를 표에 남긴다. 값을 맞추려고
수식을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_gpu_tco.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_raw, table                                       # noqa: E402
from gpu_cluster_tco import GoodputInputs, TcoInputs, goodput_breakdown  # noqa: E402

TOL_PCT = 0.01   # 발표치가 소수 둘째 자리까지라 그 폭 안이면 일치로 본다


# ── Goodput 시나리오 셋 (그림 019·022·025) ──────────────────────────────
# 값은 (입력, 발표된 결과) 짝. 발표치는 그림에서 읽은 그대로 적는다.

# 발표치는 코드에 안 적는다. 그림에서 읽은 값은 `insights/models/raw/tables.json`
# 이 정본이다 — 두 곳에 적으면 갈린다(check_model M3).
_RAW = load_raw('tables')
_TIER = ['Gold', 'Hyperscaler', 'Silver']
_SCEN = [('대규모 학습', 'goodput-large-training'),
         ('소규모 학습', 'goodput-small-training'),
         ('추론', 'goodput-inference')]
# 굿풋 표에서 대조에 쓸 열. 원자료에 없는 줄은 건너뛴다
_WANT = ('cluster_mtbf_hr', 'failures_per_month', 'downtime_pct',
         'idle_spare_pct', 'total_pct')


def _scenarios():
    """원자료의 굿풋 표 셋을 (이름, 입력, 발표치) 목록으로 편다."""
    out = []
    for label, tid in _SCEN:
        t = table(_RAW, tid)
        sh, rows = t['shared_inputs'], t['rows']
        for i, tier in enumerate(_TIER):
            if 'total_pct' not in rows:
                continue
            g = GoodputInputs(
                cluster_size=sh['cluster_size'], j_size=sh['j_size'],
                b_radius=sh['b_radius'], t_chkpt_min=sh['t_chkpt_min'],
                t_failover_min=sh['t_failover_min'],
                gpu_mtbf_hr=rows['gpu_mtbf_hr'][i], mode=rows['mode'][i],
                t_id_min=rows['t_id_min'][i], t_repair_hr=rows['t_repair_hr'][i],
                t_init_min=rows['t_init_min'][i],
                idle_spare_gpus=rows.get('idle_spare_gpus', [0, 0, 0])[i],
                perf_overhead_pct=rows.get('perf_overhead_pct', [0, 0, 0])[i])
            want = {k: rows[k][i] for k in _WANT if k in rows}
            out.append(('%s / %s' % (label, tier), g, want))
    return out


SCENARIOS = _scenarios()


def _tiers():
    """TCO 표를 (이름, 입력, 발표치) 셋으로 편다."""
    t = table(_RAW, 'cluster-tco')
    sh, r = t['shared_inputs'], t['rows']
    net = [(100, 0.09), (100, 0.045), (500, 0.01)]
    out = []
    for i, name in enumerate(t['columns']):
        inp = TcoInputs(
            gpu_count=sh['gpu_count'], gpu_price_hr=sh['gpu_price_hr'],
            hot_storage_tib=sh['hot_storage_tib'],
            hot_storage_gib_mo=r['hot_storage_gib_mo'][i],
            cold_storage_pib=sh['cold_storage_pib'],
            cold_storage_gib_mo=r['cold_storage_gib_mo'][i],
            network_items=net if r['network_cost'][i] else [],
            ctrl_plane_vms=sh['ctrl_plane_vms'] if r['ctrl_plane_cost'][i] else 0,
            ctrl_plane_vm_hr=sh['ctrl_plane_vm_hr'],
            support_uplift_pct=r['support_uplift_pct'][i],
            goodput_pct=r['goodput_pct'][i],
            setup_eng_months=r['setup_eng_months'][i],
            poc_weeks=r['poc_weeks'][i],
            debug_eng_months=r['debug_eng_months'][i],
            debug_cluster_pct=r['debug_cluster_pct'][i] and 0.8333,
            eng_cost_year=sh['engineer_cost_year'],
            contract_months=sh['contract_months'])
        want = {'storage': r['storage_cost'][i], 'support': r['support_cost'][i],
                'goodput': r['goodput_cost'][i], 'setup': r['setup_onetime'][i],
                'debugging': r['debugging_cost'][i],
                'monthly': r['monthly_amortized'][i],
                'total36': r['total_36mo'][i],
                'relative': r['relative_to_gold'][i]}
        out.append((name, inp, want))
    return out


TIERS = _tiers()


def near(got: float, want: float, tol: float) -> bool:
    return abs(got - want) <= tol


def money_near(got: float, want: float) -> bool:
    """돈은 발표치가 달러 단위 반올림이라 0.01% 안이면 일치로 본다."""
    if want == 0:
        return abs(got) < 1
    return abs(got - want) / abs(want) < 0.0001


def main() -> int:
    fails = 0

    print("── Goodput 계산기 재현 (그림 019·022·025) " + "─" * 26)
    print(f"{'시나리오':28} {'항목':12} {'모델':>10} {'발표':>10} {'차이':>9}")
    for name, g, want in SCENARIOS:
        got = goodput_breakdown(g)
        for key, tol in (("cluster_mtbf_hr", 0.05), ("failures_per_month", 0.1),
                         ("downtime_pct", TOL_PCT), ("idle_spare_pct", TOL_PCT),
                         ("total_pct", TOL_PCT)):
            if key not in want:
                continue
            ok = near(got[key], want[key], tol)
            if not ok:
                fails += 1
                print(f"{name:28} {key:12} {got[key]:10.3f} {want[key]:10.3f} "
                      f"{got[key] - want[key]:+9.3f}  FAIL")
    print(f"  Goodput 어긋난 칸: {fails}")

    print()
    print("── TCO 계산기 재현 (그림 016) " + "─" * 38)
    tco_fails = 0
    for name, t, want in TIERS:
        got = {
            "storage": t.storage_cost(),
            "support": t.support_cost(),
            "goodput": t.goodput_cost(),
            "setup": t.setup_cost_onetime(),
            "debugging": t.debugging_cost(),
            "monthly": t.monthly_amortized(),
            "total36": t.contract_total(),
        }
        for key, val in got.items():
            # goodput 은 발표 비율이 소수 둘째 자리까지라, 그 반올림 폭(±0.005%)
            # 이 GPU 비용에 곱해져 ±746달러까지 벌어진다. 그 안은 일치로 본다.
            if key == "goodput" and abs(val - want[key]) <= t.gpu_cost() * 0.00005:
                continue
            if not money_near(val, want[key]):
                tco_fails += 1
                print(f"{name:14} {key:10} 모델 {val:>16,.0f}  발표 {want[key]:>16,.0f}"
                      f"  차이 {val - want[key]:+,.0f}  FAIL")
        print(f"{name:14} 월 {got['monthly']:>14,.0f}   36개월 {got['total36']:>16,.0f}")

    base = TIERS[0][1].contract_total()
    print()
    for name, t, want in TIERS:
        rel = t.contract_total() / base
        mark = "" if near(rel, want["relative"], 0.005) else "  FAIL"
        print(f"{name:14} Gold 대비 {rel:.2f}x  (발표 {want['relative']:.2f}x){mark}")
        if mark:
            tco_fails += 1

    print(f"\n  TCO 어긋난 칸: {tco_fails}")

    print()
    print("── 수식을 그대로 쓰면 3년 값이 얼마나 달라지나 " + "─" * 22)
    print("발표된 goodput 비율 대신, 원문 수식이 내는 비율을 TCO 에 물린다.")
    print(f"{'티어':14} {'goodput 발표':>13} {'goodput 수식':>13} "
          f"{'36개월 발표':>16} {'36개월 수식':>16} {'차이':>15}")
    model_pct = {n.split(" / ")[1]: goodput_breakdown(g)["total_pct"]
                 for n, g, _ in SCENARIOS if n.startswith("대규모 학습")}
    base_pub = base_mod = None
    for name, t, want in TIERS:
        key = {"Gold-tier": "Gold", "Hyperscaler": "Hyperscaler",
               "Silver-tier": "Silver"}[name]
        published = t.contract_total()
        pub_pct = t.goodput_pct
        t.goodput_pct = model_pct[key]
        modeled = t.contract_total()
        t.goodput_pct = pub_pct
        if base_pub is None:
            base_pub, base_mod = published, modeled
        print(f"{name:14} {pub_pct:12.2f}% {model_pct[key]:12.2f}% "
              f"{published:16,.0f} {modeled:16,.0f} {modeled - published:+15,.0f}")

    print()
    print("Gold 대비 배수 — 발표 / 수식")
    for name, t, want in TIERS:
        key = {"Gold-tier": "Gold", "Hyperscaler": "Hyperscaler",
               "Silver-tier": "Silver"}[name]
        published = t.contract_total()
        pub_pct = t.goodput_pct
        t.goodput_pct = model_pct[key]
        modeled = t.contract_total()
        t.goodput_pct = pub_pct
        print(f"{name:14} {published / base_pub:.2f}x  /  {modeled / base_mod:.2f}x")

    print(f"\n총 FAIL {fails + tco_fails}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
