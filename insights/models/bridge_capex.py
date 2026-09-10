"""하향 총액과 상향 단가를 잇는 모델 — 7,300억 달러가 몇 기가와트인가.

재료가 둘이다. 하나는 다른 대화에서 받은 하향 틀(`insights/frames/2026-09-10-dc-capex-
topdown.md`)로, 회사별 2026년 자본지출을 더해 빅4 합산 7,300억 달러를 낸다. 다른 하나는
이 층의 앞 네 글이 원문에서 뽑은 메가와트당·GPU당 단가다.

하향 틀의 핵심 식이 이것이다.

    자본지출 = 신규 GW × MW당 백만 달러
    AI IT = MW당 GPU 장수 × GPU당 단가

두 항 다 그 틀에서는 손으로 넣는 가정이다. 우리 원문이 그 자리에 넣을 값을 갖고 있다 —
메가와트당 자본은 지상 층이, GPU 한 장이 끄는 전력은 GPU 금융 층이, GPU 한 장의 값은
추론 원가 모델의 서버 값이 준다. 그 값을 넣으면 총액이 몇 기가와트를 뜻하는지가 풀린다.

이 모델은 단가를 예측하지 않는다. 남이 낸 총액을 우리 단가로 나눠 볼 뿐이다.
"""

KW_PER_MW = 1000


def gpus_per_mw(kw_per_gpu):
    """메가와트당 GPU 장수. 부대설비까지 포함한 전력으로 나눈다."""
    return KW_PER_MW / kw_per_gpu


def gpu_capex(server_cost, other_cluster_cost, gpus_per_server):
    """GPU 한 장에 붙는 선불 자본. 서버 값에 망·저장·소프트웨어를 더해 나눈다."""
    return (server_cost + other_cluster_cost) / gpus_per_server


def it_capex_per_mw(kw_per_gpu, per_gpu_usd):
    """메가와트당 IT 자본지출. 백만 달러 단위로 낸다."""
    return gpus_per_mw(kw_per_gpu) * per_gpu_usd / 1e6


def all_in_per_mw(facility_musd, it_musd):
    """시설·전력과 IT 를 더한 메가와트당 자본."""
    return facility_musd + it_musd


def implied_gw(total_bn, per_mw_musd):
    """총액이 몇 기가와트를 뜻하나. 십억 달러 ÷ (백만 달러/MW) 는 기가와트다."""
    return total_bn / per_mw_musd


def server_share(it_musd, facility_musd):
    """자본지출에서 IT 가 차지하는 몫. 하향 틀의 서버 대 데이터센터 비중과 견줄 자리."""
    return it_musd / (it_musd + facility_musd) * 100


def recovery_factor(rate_pct, years):
    """자본회수계수. 지상 층과 같은 식이다 — 수명이 바뀌면 얼마나 움직이는지 본다."""
    r = rate_pct / 100.0
    if r == 0:
        return 1.0 / years
    return r / (1 - (1 + r) ** -years)


def life_change(rate_pct, old_years, new_years):
    """내용연수를 늘리면 연 자본비가 얼마나 줄어 보이나."""
    a = recovery_factor(rate_pct, old_years)
    b = recovery_factor(rate_pct, new_years)
    return {'old': a, 'new': b, 'drop_pct': (a - b) / a * 100}


def total_range(values):
    """회사별 값을 더한다. 구간으로 적힌 회사는 하한끼리·상한끼리 더한다."""
    lo = sum(v[0] for v in values)
    hi = sum(v[1] for v in values)
    return lo, hi


def blended_asp(accel_capex_bn, units_m):
    """가속기 자본지출을 대수로 나눈 칩 한 개 값. 천 달러 단위로 낸다."""
    return accel_capex_bn * 1e9 / (units_m * 1e6) / 1000


def gw_from_chips(units_m, kw_per_chip):
    """칩 수와 칩당 전력으로 용량을 센다. 기가와트로 낸다."""
    return units_m * 1e6 * kw_per_chip / 1e6


def chips_from_capex(capex_bn, per_chip_usd):
    """자본지출을 칩 한 개 값으로 나눠 대수를 센다. 백만 개로 낸다."""
    return capex_bn * 1e9 / per_chip_usd / 1e6


def hbm_per_mw(gb_per_chip, chips_per_mw):
    """메가와트당 HBM 용량. 테라바이트로 낸다."""
    return gb_per_chip * chips_per_mw / 1000.0


def hbm_cost_per_mw(gb_per_chip, chips_per_mw, usd_per_gb):
    """메가와트당 HBM 값. 백만 달러로 낸다."""
    return gb_per_chip * chips_per_mw * usd_per_gb / 1e6


def cumulative(values):
    """연도별 값을 더한다. 시나리오 스냅샷은 다섯 해다."""
    return sum(values)


def gw_series(values, per_mw_musd):
    """연도별 자본지출을 우리 단가로 나눠 해마다 몇 기가와트인지 낸다."""
    return [implied_gw(v, per_mw_musd) for v in values]
