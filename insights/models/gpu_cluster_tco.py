"""GPU 클러스터 TCO 모델 — SemiAnalysis 계산기 재현.

원문: input/clippings/How Much Do GPU Clusters Really Cost.md
표 그림: input/clip-images/How Much Do GPU Clusters Really Cost/
  016 = TCO 계산기 (3티어, GB300 NVL72 5184장)
  019 = Goodput 계산기 시나리오 1 (대규모 학습)
  022 = Goodput 계산기 시나리오 2 (소규모 학습)
  025 = Goodput 계산기 시나리오 3 (추론)

원문이 공표한 수식만 쓴다. 값을 맞추려고 계수를 손대지 않는다.
안 맞는 자리는 안 맞는 대로 표에 남긴다 — 그 자리가 이 작업의 산출물이다.

    PYTHONIOENCODING=utf-8 python insights/models/gpu_cluster_tco.py
"""
from dataclasses import dataclass, field

HOURS_PER_MONTH = 720          # 원문이 못 박은 값. 30일 x 24시간
MONTHS_PER_YEAR = 12
GIB_PER_TIB = 1024
GIB_PER_PIB = 1024 * 1024


# ── Goodput 모델 ────────────────────────────────────────────────────────
# 원문 수식 (시간 단위는 모두 hr):
#   G_chkpt_cold = [(t_id + t_chkpt/2) + t_init + t_repair] * j_size * n_fail * $GPU-hr
#   G_chkpt_hot  = {[(t_id + t_chkpt/2) + t_init] * j_size + t_repair * b_radius} * n_fail * $GPU-hr
#   G_tolerant   = [(t_id + t_failover) * j_size + t_repair * b_radius] * n_fail * $GPU-hr

@dataclass
class GoodputInputs:
    """계산기 019·022·025 의 입력 칸 그대로."""
    cluster_size: int          # GPU 장수
    j_size: int                # 평균 작업 크기 (GPU)
    b_radius: int              # 폭발 반경 (GPU) — HGX 8, NVL72 64
    t_chkpt_min: float         # 체크포인트 주기
    t_failover_min: float      # 핫스페어 전환 시간
    gpu_mtbf_hr: float         # GPU 한 장의 평균 무고장 시간
    mode: str                  # "tolerant" | "chkpt_hot" | "chkpt_cold"
    t_id_min: float            # 고장 인지 시간
    t_repair_hr: float         # 수리·교체 시간 (MTTR)
    t_init_min: float          # 작업 초기화 시간
    idle_spare_gpus: int = 0   # 놀리는 예비 GPU
    perf_overhead_pct: float = 0.0   # 망·메모리 오버헤드

    @property
    def cluster_mtbf_hr(self) -> float:
        """클러스터가 커질수록 고장 사이 시간이 짧아진다."""
        return self.gpu_mtbf_hr / self.cluster_size

    @property
    def failures_per_month(self) -> float:
        return HOURS_PER_MONTH / self.cluster_mtbf_hr


def goodput_lost_gpu_hours(g: GoodputInputs) -> float:
    """한 달에 날리는 GPU-시간. 원문 수식 셋 중 하나를 그대로 쓴다."""
    t_id = g.t_id_min / 60
    t_chkpt = g.t_chkpt_min / 60
    t_init = g.t_init_min / 60
    t_failover = g.t_failover_min / 60
    t_repair = g.t_repair_hr
    n = g.failures_per_month

    if g.mode == "tolerant":
        per_failure = (t_id + t_failover) * g.j_size + t_repair * g.b_radius
    elif g.mode == "chkpt_hot":
        per_failure = (t_id + t_chkpt / 2 + t_init) * g.j_size + t_repair * g.b_radius
    elif g.mode == "chkpt_cold":
        per_failure = (t_id + t_chkpt / 2 + t_init + t_repair) * g.j_size
    else:
        raise ValueError(f"모르는 복원 방식: {g.mode}")

    return per_failure * n


def goodput_breakdown(g: GoodputInputs) -> dict:
    """계산기 RESULTS 칸을 재현한다. 백분율 분모는 클러스터 GPU-시간."""
    capacity = g.cluster_size * HOURS_PER_MONTH
    downtime = goodput_lost_gpu_hours(g) / capacity * 100
    idle = g.idle_spare_gpus / g.cluster_size * 100
    return {
        "cluster_mtbf_hr": g.cluster_mtbf_hr,
        "failures_per_month": g.failures_per_month,
        "downtime_pct": downtime,
        "idle_spare_pct": idle,
        "perf_overhead_pct": g.perf_overhead_pct,
        "total_pct": downtime + idle + g.perf_overhead_pct,
    }


# ── TCO 모델 ───────────────────────────────────────────────────────────
# TCO/월 = GPU + 저장 + 네트워크 + 컨트롤플레인 + 지원 + Goodput + 설치 + 디버깅

@dataclass
class TcoInputs:
    """계산기 016 의 입력 칸 그대로."""
    gpu_count: int
    gpu_price_hr: float
    hot_storage_tib: float
    hot_storage_gib_mo: float
    cold_storage_pib: float
    cold_storage_gib_mo: float
    network_items: list = field(default_factory=list)   # (수량, 단가)
    ctrl_plane_vms: int = 0
    ctrl_plane_vm_hr: float = 0.0
    support_uplift_pct: float = 0.0
    goodput_pct: float = 0.0
    setup_eng_months: float = 0.0
    poc_weeks: float = 0.0
    debug_eng_months: float = 0.0        # 매달
    debug_cluster_pct: float = 0.0       # 매달, GPU 비용 대비
    eng_cost_year: float = 200_000.0
    contract_months: int = 36

    def gpu_cost(self) -> float:
        return self.gpu_count * self.gpu_price_hr * HOURS_PER_MONTH

    def storage_cost(self) -> float:
        hot = self.hot_storage_tib * GIB_PER_TIB * self.hot_storage_gib_mo
        cold = self.cold_storage_pib * GIB_PER_PIB * self.cold_storage_gib_mo
        return hot + cold

    def network_cost(self) -> float:
        return sum(qty * price for qty, price in self.network_items)

    def ctrl_plane_cost(self) -> float:
        return self.ctrl_plane_vms * self.ctrl_plane_vm_hr * HOURS_PER_MONTH

    def support_cost(self) -> float:
        """지원은 하드웨어·저장·망·컨트롤플레인 합에 붙는 비율이다."""
        base = self.gpu_cost() + self.storage_cost() + self.network_cost() + self.ctrl_plane_cost()
        return base * self.support_uplift_pct / 100

    def goodput_cost(self) -> float:
        """Goodput 손실은 GPU 비용에만 붙는다."""
        return self.gpu_cost() * self.goodput_pct / 100

    def setup_cost_onetime(self) -> float:
        """엔지니어 인건비 + POC 기간 동안 놀린 클러스터 값.

        POC 주수는 4주를 한 달로 세어 GPU 비용에 곱한다 (016 재현).
        """
        eng = self.setup_eng_months * self.eng_cost_year / MONTHS_PER_YEAR
        poc = self.poc_weeks / 4 * self.gpu_cost()
        return eng + poc

    def debugging_cost(self) -> float:
        eng = self.debug_eng_months * self.eng_cost_year / MONTHS_PER_YEAR
        return eng + self.gpu_cost() * self.debug_cluster_pct / 100

    def monthly_amortized(self) -> float:
        return (
            self.gpu_cost()
            + self.storage_cost()
            + self.network_cost()
            + self.ctrl_plane_cost()
            + self.support_cost()
            + self.goodput_cost()
            + self.setup_cost_onetime() / self.contract_months
            + self.debugging_cost()
        )

    def contract_total(self) -> float:
        return self.monthly_amortized() * self.contract_months
