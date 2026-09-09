"""GPU 클러스터 TCO 모델을 원문 발표 숫자와 대조한다.

발표 숫자는 표 그림 016·019·022·025 에서 읽은 것이다. 모델이 그 값을
다시 내면 재현 성공, 못 내면 어긋난 자리를 표에 남긴다. 값을 맞추려고
수식을 손대지 않는다.

    PYTHONIOENCODING=utf-8 python insights/models/check_gpu_tco.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gpu_cluster_tco import GoodputInputs, TcoInputs, goodput_breakdown  # noqa: E402

TOL_PCT = 0.01   # 발표치가 소수 둘째 자리까지라 그 폭 안이면 일치로 본다


# ── Goodput 시나리오 셋 (그림 019·022·025) ──────────────────────────────
# 값은 (입력, 발표된 결과) 짝. 발표치는 그림에서 읽은 그대로 적는다.

SCENARIOS = [
    # ── 019: 대규모 학습. 5184장 클러스터에 4096장짜리 작업 하나
    ("대규모 학습 / Gold", GoodputInputs(
        cluster_size=5184, j_size=4096, b_radius=64, t_chkpt_min=60,
        t_failover_min=5, gpu_mtbf_hr=25000, mode="tolerant",
        t_id_min=15, t_repair_hr=0.25, t_init_min=10, idle_spare_gpus=32,
    ), {"cluster_mtbf_hr": 4.8, "failures_per_month": 149.3,
        "downtime_pct": 5.53, "idle_spare_pct": 0.62, "total_pct": 6.14}),

    ("대규모 학습 / Hyperscaler", GoodputInputs(
        cluster_size=5184, j_size=4096, b_radius=64, t_chkpt_min=60,
        t_failover_min=5, gpu_mtbf_hr=25000, mode="tolerant",
        t_id_min=15, t_repair_hr=0.25, t_init_min=10, perf_overhead_pct=5.0,
    ), {"cluster_mtbf_hr": 4.8, "failures_per_month": 149.3,
        "downtime_pct": 5.53, "idle_spare_pct": 0.0, "total_pct": 10.53}),

    ("대규모 학습 / Silver", GoodputInputs(
        cluster_size=5184, j_size=4096, b_radius=64, t_chkpt_min=60,
        t_failover_min=5, gpu_mtbf_hr=15000, mode="chkpt_hot",
        t_id_min=60, t_repair_hr=1, t_init_min=15,
    ), {"cluster_mtbf_hr": 2.9, "failures_per_month": 248.8,
        "downtime_pct": 20.91, "idle_spare_pct": 0.0, "total_pct": 20.91}),

    # ── 022: 소규모 학습. 2048장 클러스터에 64장짜리 작업들
    ("소규모 학습 / Gold", GoodputInputs(
        cluster_size=2048, j_size=64, b_radius=8, t_chkpt_min=60,
        t_failover_min=5, gpu_mtbf_hr=25000, mode="chkpt_cold",
        t_id_min=15, t_repair_hr=0.25, t_init_min=10,
    ), {"cluster_mtbf_hr": 12.2, "failures_per_month": 59.0,
        "downtime_pct": 0.23, "idle_spare_pct": 0.0, "total_pct": 0.23}),

    ("소규모 학습 / Silver", GoodputInputs(
        cluster_size=2048, j_size=64, b_radius=8, t_chkpt_min=60,
        t_failover_min=5, gpu_mtbf_hr=15000, mode="chkpt_cold",
        t_id_min=60, t_repair_hr=1, t_init_min=15,
    ), {"cluster_mtbf_hr": 7.3, "failures_per_month": 98.3,
        "downtime_pct": 0.96, "idle_spare_pct": 0.0, "total_pct": 0.96}),

    # ── 025: 추론. 512장 클러스터에 8장짜리 작업들
    ("추론 / Gold", GoodputInputs(
        cluster_size=512, j_size=8, b_radius=8, t_chkpt_min=60,
        t_failover_min=7.5, gpu_mtbf_hr=25000, mode="tolerant",
        t_id_min=15, t_repair_hr=0.25, t_init_min=15,
    ), {"cluster_mtbf_hr": 48.8, "failures_per_month": 14.7,
        "downtime_pct": 0.02, "idle_spare_pct": 0.0, "total_pct": 0.02}),

    ("추론 / Silver", GoodputInputs(
        cluster_size=512, j_size=8, b_radius=8, t_chkpt_min=60,
        t_failover_min=7.5, gpu_mtbf_hr=15000, mode="tolerant",
        t_id_min=60, t_repair_hr=8, t_init_min=15,
    ), {"cluster_mtbf_hr": 29.3, "failures_per_month": 24.6,
        "downtime_pct": 0.49, "idle_spare_pct": 0.0, "total_pct": 0.49}),
]


# ── TCO 세 티어 (그림 016) ──────────────────────────────────────────────

NETWORK_HYPERSCALER = [(100, 0.09), (100, 0.045), (500, 0.01)]

TIERS = [
    ("Gold-tier", TcoInputs(
        gpu_count=5184, gpu_price_hr=4.0,
        hot_storage_tib=500, hot_storage_gib_mo=0.035,
        cold_storage_pib=10, cold_storage_gib_mo=0.01,
        goodput_pct=6.14,
    ), {"storage": 122_778, "support": 0, "goodput": 917_088,
        "setup": 0, "debugging": 0,
        "monthly": 15_969_785, "total36": 574_912_276, "relative": 1.00}),

    ("Hyperscaler", TcoInputs(
        gpu_count=5184, gpu_price_hr=4.0,
        hot_storage_tib=500, hot_storage_gib_mo=0.0725,
        cold_storage_pib=10, cold_storage_gib_mo=0.02,
        network_items=NETWORK_HYPERSCALER,
        ctrl_plane_vms=3, ctrl_plane_vm_hr=1.536,
        support_uplift_pct=3.0, goodput_pct=10.53,
        setup_eng_months=4, poc_weeks=4, debug_eng_months=0.5,
    ), {"storage": 246_835, "support": 455_403, "goodput": 1_571_424,
        "setup": 14_996_587, "debugging": 8_333,
        "monthly": 17_631_823, "total36": 634_745_636, "relative": 1.10}),

    ("Silver-tier", TcoInputs(
        gpu_count=5184, gpu_price_hr=4.0,
        hot_storage_tib=500, hot_storage_gib_mo=0.055,
        cold_storage_pib=10, cold_storage_gib_mo=0.015,
        goodput_pct=20.91,
        setup_eng_months=2, debug_eng_months=0.25, debug_cluster_pct=0.8333,
    ), {"storage": 185_446, "support": 0, "goodput": 3_121_349,
        "setup": 33_333, "debugging": 128_583,
        "monthly": 18_366_224, "total36": 661_184_050, "relative": 1.15}),
]


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
