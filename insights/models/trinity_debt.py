"""GPU 금융 모델 — 담보가 없으면 이익이 어디로 가나.

원문: input/clippings/Nvidia GPU Debt Backstop Unleashes the AI Project Trinity ... .md

원문은 네오클라우드가 GPU 를 사는 돈을 어떻게 빌리는지를 다룬다. 값이 세 무리다.
① 엔비디아가 깔아 주는 바닥값(백스톱)과 그 위에서 나누는 몫, ② 은행이 요구하는
담보인정비율과 부채상환비율, ③ 담보가 붙느냐 아니냐로 갈리는 조달 금리와 이익률.

이 모델은 그 셋을 잇는다.

    실현 단가 = 백스톱 바닥값 + (청구가 − 바닥값) × 네오클라우드 몫
    테이크레이트 = 엔비디아 몫 ÷ 청구가
    부채 여력 = 프로젝트 현금 ÷ 부채상환비율
    이익률이 깎이는 폭 = 금리 차 × 부채 ÷ 매출

원문이 값 몇 개를 흩어 적었을 뿐 이 셈을 이어서 보여 주지는 않는다.
"""

HOURS_PER_YEAR = 8760


def implied_floor(total_usd, gpus, years, hours_per_year=HOURS_PER_YEAR):
    """공시된 백스톱 총액에서 GPU 시간당 바닥값을 거꾸로 푼다."""
    return total_usd / (gpus * years * hours_per_year)


def split(floor, charge, nvda_share_pct):
    """바닥값 위 초과분을 엔비디아와 네오클라우드가 나눈다."""
    excess = charge - floor
    nvda = excess * nvda_share_pct / 100.0
    return {'excess': excess, 'nvda': nvda, 'neo': excess - nvda,
            'neo_total': floor + excess - nvda}


def take_rate(nvda_hourly, charge_hourly):
    """엔비디아가 청구가에서 가져가는 몫."""
    return nvda_hourly / charge_hourly * 100


def gpus_behind(guarantee_usd, floor_hourly, years, hours_per_year=HOURS_PER_YEAR):
    """우발채무 금액과 바닥값에서 그 뒤에 선 GPU 장수를 푼다."""
    return guarantee_usd / (floor_hourly * years * hours_per_year)


def kw_per_gpu(gpus, mw):
    """장수와 용량에서 GPU 한 장이 끌어가는 전력. 부대설비까지 포함된 값이다."""
    return mw * 1000.0 / gpus


def margin_drop(rate_lo_pct, rate_hi_pct, debt_to_revenue):
    """금리가 오를 때 세전이익률이 깎이는 폭. 부채는 매출 대비 배수로 받는다."""
    return (rate_hi_pct - rate_lo_pct) * debt_to_revenue


def implied_debt_to_revenue(rate_lo_pct, rate_hi_pct, pbt_lo_pct, pbt_hi_pct):
    """발표된 이익률 두 값에서 부채가 매출의 몇 배인지를 거꾸로 푼다.

    금리가 그만큼 올랐을 때 이익률이 그만큼 깎였다면, 그 사이를 잇는 것은
    부채 규모뿐이다. 원문은 부채 규모를 안 적었다.
    """
    return (pbt_hi_pct - pbt_lo_pct) / (rate_hi_pct - rate_lo_pct)


def implied_yield_on_cost(debt_to_revenue, ltv_pct):
    """부채 배수와 담보인정비율에서 원가수익률을 푼다.

    원가수익률은 연 매출 ÷ 프로젝트 비용이다. 부채가 매출의 몇 배이고
    그 부채가 비용의 몇 할이면 비용이 풀린다.
    """
    project_cost = debt_to_revenue / (ltv_pct / 100.0)
    return 1.0 / project_cost * 100


def max_debt_service(cash_flow, dscr):
    """부채상환비율을 지키면서 낼 수 있는 최대 원리금."""
    return cash_flow / dscr
