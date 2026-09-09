"""추론 원가 모델 — 자본지출·운영비에서 GPU 시간당 원가와 백만 토큰당 원가까지.

원문: input/clippings/AMD vs NVIDIA Inference Benchmark Who Wins - Performance & Cost Per Million Tokens.md
표 그림: input/clip-images/AMD vs NVIDIA Inference Benchmark .../
  049 = AI Cloud Capital Cost of Ownership (자본지출)
  050 = AI Cloud Operating Cost of Ownership (운영비)
  016 = AI Cloud Total Cost of Ownership (합계)

사슬은 이렇다.

  서버 값 + 망·저장·소프트웨어  →  선불 자본지출
  선불 자본지출 × 감가상각(WACC, 내용연수)  →  월 자본비
  전기 + 코로케이션 + 상면 인건비 + 회선  →  월 운영비
  (월 자본비 + 월 운영비) / (GPU 수 × 월 시간)  →  시간당 GPU 원가
  시간당 GPU 원가 / 시간당 토큰 수  →  백만 토큰당 원가

원문이 밝힌 값과 가정만 쓴다. 가려진 칸(GPU 원가 등)은 안 채운다.
"""
from dataclasses import dataclass

HOURS_PER_MONTH = 730          # 이 원문이 쓰는 값. 클러스터 TCO 글의 720 과 다르다
MONTHS_PER_YEAR = 12
GPUS_PER_SERVER = 8


def levelized_monthly(principal: float, wacc_annual: float, years: int) -> float:
    """선불 자본지출을 내용연수에 걸쳐 매달 같은 금액으로 편다.

    자본비용이 붙는 원리금 균등 상환이다. 단순 나눗셈이 아니라서
    WACC 13.3%, 4년이면 원금의 약 1.29배를 갚는다.
    """
    r = wacc_annual / MONTHS_PER_YEAR
    n = years * MONTHS_PER_YEAR
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def implied_wacc(principal: float, monthly_payment: float, years: int,
                 lo: float = 0.0, hi: float = 1.0) -> float:
    """발표된 월 자본비에서 실제 쓰인 WACC 를 역산한다.

    표에 찍힌 13.3% 는 소수 한 자리로 반올림된 표시값이다. 그 값을 그대로
    넣으면 월 자본비가 일제히 0.09% 씩 높게 나온다 — 방향과 비율이 모든
    SKU 에서 같다는 것이 반올림의 지문이다.
    """
    for _ in range(200):
        mid = (lo + hi) / 2
        if levelized_monthly(principal, mid, years) < monthly_payment:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


@dataclass
class Capex:
    """그림 049 의 칸. 가려진 세 줄(GPU 원가·보증·기타)은 안 쓴다."""
    server_cost: float                 # 서버 한 대 값
    other_cluster_cost: float          # 서비스·망·저장·소프트웨어 등
    wacc: float = 0.133
    useful_life_years: int = 4
    gpus_per_server: int = GPUS_PER_SERVER

    def upfront_per_server(self) -> float:
        return self.server_cost + self.other_cluster_cost

    def upfront_per_gpu(self) -> float:
        return self.upfront_per_server() / self.gpus_per_server

    def monthly_per_server(self) -> float:
        return levelized_monthly(self.upfront_per_server(), self.wacc,
                                 self.useful_life_years)

    def hourly_per_gpu(self) -> float:
        return self.monthly_per_server() / self.gpus_per_server / HOURS_PER_MONTH


@dataclass
class Opex:
    """그림 050 의 칸."""
    power_kw: float                    # 서버 한 대의 critical IT 전력
    electricity_kwh: float = 0.0870
    utilization: float = 0.80
    pue: float = 1.35
    colocation_kw_month: float = 130.0
    remote_hands_month: float = 131.0  # 서버 한 대 몫
    internet_month: float = 39.0
    gpus_per_server: int = GPUS_PER_SERVER

    def electricity_per_kw_month(self) -> float:
        """전기는 정격이 아니라 실제 쓴 만큼 낸다. 가동률과 PUE 가 여기 붙는다."""
        return (self.electricity_kwh * HOURS_PER_MONTH
                * self.utilization * self.pue)

    def hosting_per_kw_month(self) -> float:
        return self.electricity_per_kw_month() + self.colocation_kw_month

    def hosting_per_server_month(self) -> float:
        return self.hosting_per_kw_month() * self.power_kw

    def monthly_per_server(self) -> float:
        return (self.hosting_per_server_month()
                + self.remote_hands_month + self.internet_month)

    def monthly_per_gpu(self) -> float:
        return self.monthly_per_server() / self.gpus_per_server

    def hourly_per_gpu(self) -> float:
        return self.monthly_per_gpu() / HOURS_PER_MONTH


@dataclass
class Sku:
    name: str
    capex: Capex
    opex: Opex

    def tco_hourly_per_gpu(self) -> float:
        return self.capex.hourly_per_gpu() + self.opex.hourly_per_gpu()

    def capital_share(self) -> float:
        return self.capex.hourly_per_gpu() / self.tco_hourly_per_gpu() * 100


def cost_per_million_tokens(hourly_per_gpu: float, tokens_per_sec_per_gpu: float) -> float:
    """시간당 원가를 토큰 처리량으로 나눈다. 낮을수록 좋다."""
    tokens_per_hour = tokens_per_sec_per_gpu * 3600
    return hourly_per_gpu / tokens_per_hour * 1_000_000


def breakeven_hourly(reference_hourly: float, throughput_ratio: float) -> float:
    """상대 처리량이 주어졌을 때, 기준 SKU 와 토큰당 원가가 같아지는 시간당 값.

    처리량이 기준의 76% 뿐이면 시간당 값도 76% 여야 본전이다.
    """
    return reference_hourly * throughput_ratio


def implied_throughput_ratio(reference_hourly: float, breakeven_price: float) -> float:
    """거꾸로 — 발표된 손익분기 임대료가 함의하는 상대 처리량."""
    return breakeven_price / reference_hourly
