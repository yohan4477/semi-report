"""자본에서 웨이퍼까지 — 사슬 네 마디를 잇는 모델.

원문: input/clippings/To Boldly Go The Case for Space Datacenters.md

앞 층들이 돈을 메가와트로 옮겼다. 이 모델은 그 메가와트를 웨이퍼로 옮긴다. 계수는
원문이 준 것이다 — 배치된 컴퓨트 1기가와트가 로직·메모리·패키징을 합쳐 웨이퍼
투입 35만 4,000장이고, 그 가운데 메모리가 60퍼센트를 넘으며, 기가와트당 웨이퍼
가치가 30억 달러쯤이다 (우주영문 L348).

    웨이퍼 투입 = 기가와트 × 354,000
    월 투입 = 연 투입 ÷ 12
    파운드리에서 차지하는 몫 = 월 투입 ÷ 세계 300밀리 용량

사슬은 이렇게 선다.

    자본지출 → 메가와트 → 칩 → 메모리 → 웨이퍼

앞 세 마디는 앞 층들이 갖고 있고, 이 모델은 마지막 마디를 붙인다.
"""

MONTHS = 12


def wafers_from_gw(gw, wafers_per_gw):
    """기가와트를 연 웨이퍼 투입 장수로. 로직·메모리·패키징을 합친 값이다."""
    return gw * wafers_per_gw


def wspm(annual_wafers):
    """연 투입을 월 투입으로. 파운드리 용량은 월 단위로 말한다."""
    return annual_wafers / MONTHS


def share_of_global(monthly_wafers, global_wspm):
    """세계 300밀리 파운드리 용량에서 차지하는 몫."""
    return monthly_wafers / global_wspm * 100


def wafer_value(gw, value_per_gw_bn):
    """기가와트당 웨이퍼 가치를 곱한다. 십억 달러로 낸다."""
    return gw * value_per_gw_bn


def value_share(wafer_value_bn, capex_bn):
    """웨이퍼 가치가 자본지출에서 차지하는 몫."""
    return wafer_value_bn / capex_bn * 100


def memory_wafers(annual_wafers, memory_share_pct):
    """그 가운데 메모리 몫."""
    return annual_wafers * memory_share_pct / 100.0


def implied_tsmc(annual_wafers_1tw, multiple):
    """「1테라와트가 TSMC 전체 출력의 몇 배」에서 그 출력을 거꾸로 푼다."""
    return annual_wafers_1tw / multiple


def implied_global(entry_wspm, entry_share_pct):
    """「10만 장이 세계의 2.5퍼센트」에서 세계 용량을 거꾸로 푼다."""
    return entry_wspm / (entry_share_pct / 100.0)


def hbm_bit_penalty(commodity_wafers, multiple):
    """같은 비트를 HBM 으로 만들 때 드는 웨이퍼. 원문은 세 배로 적었다."""
    return commodity_wafers * multiple
