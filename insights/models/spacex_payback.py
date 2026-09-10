"""컴퓨트 자본 회수 모델 — 기가와트당 500억 달러를 무엇으로 갚나.

원문: input/clippings/SpaceX 10GW in 2027 ... .md

원문은 기가와트당 자본지출을 500억 달러로 잡고, 그 용량을 파는 값을 네 자리로
적었다 — 지금 오픈AI 에 임대되는 MW당 연 1,400만 달러, 리드타임을 무기로 매길 수
있다는 3,000만~5,000만, API 추론으로 팔 때의 1억. 그리고 기가와트당 연 비용을
120억 달러로 잡았다.

원문은 「1년 안에 자본을 회수한다」고 적었다. 이 모델은 그 문장이 어느 셈에서
나오는지를 본다. 매출로 나누면 회수이고 현금흐름으로 나누면 다른 값이 된다.

    매출 기준 회수 = MW당 자본 ÷ MW당 연 매출
    현금 기준 회수 = MW당 자본 ÷ (MW당 연 매출 − MW당 연 비용)
"""

MW_PER_GW = 1000


def per_mw(value_per_gw):
    """기가와트당 값을 MW당으로. 십억 달러/GW 는 백만 달러/MW 와 같은 수다."""
    return value_per_gw


def payback_on_revenue(capex_per_mw, rev_per_mw_year):
    """매출로 자본을 다 갚는 데 걸리는 햇수. 비용을 안 뺀 값이다."""
    return capex_per_mw / rev_per_mw_year


def payback_on_cash(capex_per_mw, rev_per_mw_year, cost_per_mw_year):
    """비용을 빼고 남는 돈으로 갚는 햇수. 비용이 매출보다 크면 못 갚는다."""
    net = rev_per_mw_year - cost_per_mw_year
    if net <= 0:
        return None
    return capex_per_mw / net


def gross_margin(rev_per_mw_year, cost_per_mw_year):
    """매출에서 비용을 빼고 남는 몫."""
    return (rev_per_mw_year - cost_per_mw_year) / rev_per_mw_year * 100


def arr_from_capacity(gw, monetize_pct, rev_per_mw_year):
    """수익화하는 용량만 매출로 센다. 나머지는 자기가 쓴다는 가정이다."""
    return gw * MW_PER_GW * (monetize_pct / 100.0) * rev_per_mw_year


def implied_price(arr_target_bn, gw, monetize_pct):
    """발표된 연간반복매출 목표가 전제하는 MW당 매출을 거꾸로 푼다."""
    mw = gw * MW_PER_GW * (monetize_pct / 100.0)
    return arr_target_bn * 1000.0 / mw


def contract_value_per_gw(value_bn, gw):
    """계약 총액을 용량으로 나눈다. 몇 해치인지는 따로 봐야 한다."""
    return value_bn / gw


def years_implied(value_per_gw_bn, rev_per_mw_year):
    """계약 총액이 MW당 연 매출로 몇 해치인지."""
    return value_per_gw_bn * 1000.0 / (rev_per_mw_year * MW_PER_GW)
