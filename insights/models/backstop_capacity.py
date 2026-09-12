"""백스톱 용량 모델 — 우발채무 5,300억 달러가 몇 기가와트를 받치나.

원문: input/clippings/Nvidias Backstop Universe - Heads I Win, Tails Who Loses.md

원문은 엔비디아 10-Q 의 오프밸런스 보증 여섯 항목을 늘어놓고, 구조 셋(AICP ·
PORTS-Pike · 잔존가치보증)이 1기가와트마다 얼마의 부담을 만드는지 적었다. 값은
세 무리다. ① 대차대조표 안팎의 금액, ② 받쳐 주는 용량(기가와트), ③ 1기가와트당
부담. 원문은 ①과 ③을 따로 적고 잇지 않았다.

이 모델은 그 셋을 앞 두 글의 단가와 잇는다 — GPU 금융 층이 되짚은 GPU 한 장의
전력, 다리 층이 세운 메가와트당 자본.

    1GW당 부담 = 계약 총액 ÷ 계약 용량
    받쳐 준 GPU 장수 = 부담 총액 ÷ (바닥값 × 년 × 연 시간)
    부담이 자본을 덮는 배수 = 1GW당 부담 ÷ 1GW당 자본지출
    잔존가치보증이 전제하는 자본 = 1GW당 부담 ÷ 보증 상한

메가와트당 백만 달러와 기가와트당 십억 달러는 같은 수다. 그래서 단가끼리 그대로
나눈다.
"""

HOURS_PER_YEAR = 8760
KW_PER_MW = 1000


def per_gw(total_bn, gw):
    """계약 총액을 용량으로 나눠 1기가와트당 부담을 낸다. 십억 달러 단위."""
    return total_bn / gw


def gw_enabled(total_bn, per_gw_bn):
    """부담 총액을 1기가와트당 부담으로 나눠 그 뒤에 선 용량을 센다."""
    return total_bn / per_gw_bn


def gpus_behind(total_usd, floor_hourly, years, hours_per_year):
    """부담 총액과 바닥값에서 받쳐 준 GPU 장수를 푼다. 시간은 인자로 받는다."""
    return total_usd / (floor_hourly * years * hours_per_year)


def kw_per_gpu(gpus, mw):
    """장수와 용량에서 GPU 한 장이 끄는 전력. 부대설비까지 포함한 값이다."""
    return mw * KW_PER_MW / gpus


def floor_from_per_gw(per_gw_bn, kw_each, years, hours_per_year):
    """1기가와트당 부담을 GPU 시간당 바닥값으로 되돌린다."""
    gpus = KW_PER_MW * KW_PER_MW / kw_each          # 1GW 에 드는 장수
    return per_gw_bn * 1e9 / (gpus * years * hours_per_year)


def coverage(obl_per_gw_bn, capex_per_mw_musd):
    """1기가와트당 부담이 그 기가와트를 짓는 자본의 몇 배인가."""
    return obl_per_gw_bn / capex_per_mw_musd


def implied_capex_per_mw(rvg_per_gw_bn, guarantee_cap_pct):
    """잔존가치보증의 1기가와트당 부담과 보증 상한에서 거래액을 되짚는다.

    보증이 거래액의 25퍼센트까지라면 1기가와트당 9.4십억은 거래액 37.6십억을
    뜻한다. 메가와트당 백만 달러로 읽으면 37.6이다.
    """
    return rvg_per_gw_bn / (guarantee_cap_pct / 100.0)


def capex_behind(gw, capex_per_mw_musd):
    """받쳐 준 용량에 메가와트당 자본을 곱해 그 뒤의 자본지출을 센다. 십억 달러."""
    return gw * capex_per_mw_musd


def discount(floor, market):
    """바닥값이 시장가보다 몇 퍼센트 낮은가."""
    return (1.0 - floor / market) * 100


def residual(total, parts):
    """총액에서 이름이 적힌 항목을 빼 이름이 안 적힌 나머지를 낸다."""
    return total - sum(parts)


def ratio(a, b):
    """두 값의 배수."""
    return a / b


def share(part_bn, whole_bn):
    """전체에서 차지하는 몫. 퍼센트."""
    return part_bn / whole_bn * 100
