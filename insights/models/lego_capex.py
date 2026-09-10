"""모듈러 데이터센터 자본지출 모델 — 8퍼센트가 어디서 나오나.

원문: input/clippings/The Wild Wild West Of LEGO Datacenters.md

원문은 50MW 액체냉각 홀 하나를 두 가지로 지어 견줬다. 현장에서 다 짓는 방식이
MW당 1,460만 달러, 전기·기계를 공장에서 만들어 실어 오는 방식이 1,350만 달러다.
차이가 110만 달러이고 원문은 이것을 「8퍼센트쯤 싸다」고 적었다.

이 모델이 묻는 것은 그 110만 달러가 어느 항에서 나오나다. 원문이 절감 항목을
둘로 적었다 — 건설서비스 60만 달러와 설치비 50만 달러. 합이 정확히 110만이다.
그러면 그 항들이 인건비인가. 원문이 인시와 임금을 따로 적어 두었으므로 곱해 보면
안다. 곱해 보면 안 맞는다. 그 어긋난 몫이 이 모델의 답이다.

    현장 인건비 = 인시 × 임금
    옮긴 뒤 = 남은 현장 인시 × 현장 임금 + 옮긴 인시 × 공장 임금
    인건비로 설명되는 몫 = (현장 − 옮긴 뒤) ÷ 발표된 차이
"""

HOURS_PER_MONTH = 730


def labor_cost(hours_per_mw, wage):
    """MW당 인시에 임금을 곱한다. 시간과 임금 둘 다 원문 값이다."""
    return hours_per_mw * wage


def labor_saving(hours_before, hours_after, wage_field, wage_factory):
    """공장으로 옮겨 아끼는 MW당 인건비.

    옮긴 시간이 사라지는 것이 아니라 공장 임금으로 다시 붙는다. 원문이
    현장 임금과 공장 임금을 따로 적은 이유가 이 자리다.
    """
    moved = hours_before - hours_after
    before = labor_cost(hours_before, wage_field)
    after = labor_cost(hours_after, wage_field) + labor_cost(moved, wage_factory)
    return {'moved_hours': moved, 'before': before, 'after': after,
            'saving': before - after}


def explained_share(saving_usd, stated_delta_musd):
    """인건비로 설명되는 몫. 발표된 차이는 백만 달러 단위로 받는다."""
    return saving_usd / (stated_delta_musd * 1e6) * 100


def delta_pct(stick, modular):
    """비싼 쪽을 기준으로 몇 퍼센트 싼가. 원문이 8퍼센트라고 적은 자리다."""
    return (stick - modular) / stick * 100


def months_cut(before, after):
    """공기 단축률. 하한과 상한이 따로 있으면 각각 부른다."""
    return (before - after) / before * 100


def early_revenue(months, mw, rev_per_mw_year):
    """공기를 앞당겨 먼저 받는 매출. 이익이 아니라 매출이다.

    레고 원문에는 MW당 매출이 없다. 이 함수가 받는 값은 지상 데이터센터 층에서
    오고(우주영문 L288), 그래서 부르는 자리에서 출처를 밝힌다.
    """
    return mw * rev_per_mw_year * (months / 12.0)


def content_share(content_per_mw, all_in_per_mw):
    """벤더 하나가 MW당 총원가에서 가져가는 몫."""
    return content_per_mw / all_in_per_mw * 100
