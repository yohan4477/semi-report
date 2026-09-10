"""지상 데이터센터 자본지출 모델 — MW당 자본이 매출에서 얼마를 먹나.

원문: input/clippings/To Boldly Go The Case for Space Datacenters.md

원문은 우주 데이터센터를 따지려고 지상 데이터센터를 먼저 세웠다. 그 지상 쪽 값이
이 모델의 재료다 — 전력을 어디서 끌어오느냐로 MW당 자본이 네 층으로 갈리고,
계약 IT 부하 MW당 연 매출이 1,200만에서 1,300만 달러이며, 가중평균자본비용이
10.3퍼센트에 데이터센터 자산 수명이 15년이다.

선불로 낸 자본은 그대로 비용이 아니다. 자본비용과 수명에 걸쳐 매년 얼마씩으로
펴야 매출과 견줄 수 있다. 그 계수가 자본회수계수다.

    자본회수계수 = r ÷ (1 − (1+r)^−n)
    연 자본비 = MW당 자본 × 자본회수계수
    매출에서 먹는 몫 = 연 자본비 ÷ MW당 연 매출

층이 올라갈수록 이 몫이 어디까지 가나가 물음이다.
"""

HOURS_PER_YEAR = 8760
KW_PER_MW = 1000


def recovery_factor(rate_pct, years):
    """자본회수계수. 선불액을 수명에 걸쳐 매년 같은 금액으로 편다.

    단순히 수명으로 나누는 것이 아니다 — 10.3퍼센트에 15년이면 계수가
    0.133 이라 15로 나눈 0.067 의 두 배다.
    """
    r = rate_pct / 100.0
    if r == 0:
        return 1.0 / years
    return r / (1 - (1 + r) ** -years)


def annual_capital(capex_per_mw, rate_pct, years):
    """MW당 자본을 연 자본비로 편다. 단위는 받은 그대로 나간다."""
    return capex_per_mw * recovery_factor(rate_pct, years)


def revenue_share(capex_per_mw, rev_per_mw_year, rate_pct, years):
    """연 자본비가 MW당 연 매출에서 차지하는 몫."""
    return annual_capital(capex_per_mw, rate_pct, years) / rev_per_mw_year * 100


def wacc(debt_cost_pct, equity_cost_pct, debt_share_pct):
    """부채와 자기자본을 비중으로 섞는다. 세금은 안 넣는다 — 원문도 세전이다."""
    d = debt_share_pct / 100.0
    return debt_cost_pct * d + equity_cost_pct * (1 - d)


def pulled_forward_revenue(mw, months, rev_per_mw_year):
    """일찍 켜서 먼저 받는 매출. 할인은 안 한다 — 반 년이라 차이가 작다."""
    return mw * rev_per_mw_year * (months / 12.0)


def implied_margin(npv, mw, months, rev_per_mw_year):
    """발표된 순현재가치가 그 매출의 몇 퍼센트인가.

    원문은 200MW 를 여섯 달 일찍 켜면 4~5억 달러라고만 적었다. 그 값이
    매출의 몇 할인지를 보면 어떤 마진을 전제했는지가 드러난다.
    """
    rev = pulled_forward_revenue(mw, months, rev_per_mw_year)
    return npv / rev * 100


def annual_mwh(pue, util_pct):
    """IT 부하 1MW 가 한 해에 쓰는 전력량. 냉각과 손실이 PUE 로 붙는다."""
    return KW_PER_MW * pue * HOURS_PER_YEAR * (util_pct / 100.0) / 1000


def power_cost_per_mw_year(price_per_kwh, pue, util_pct):
    """MW당 연 전기값. 정격이 아니라 가동률과 PUE 를 거친 값이다."""
    return annual_mwh(pue, util_pct) * 1000 * price_per_kwh


def price_from_mwh(price_per_mwh):
    """MWh 당 가격을 kWh 당으로. 같은 글이 두 단위를 섞어 쓴다."""
    return price_per_mwh / 1000.0
