"""PJM 용량 경매 원가 모델 — 모델링 가정이 요금으로 바뀌는 길.

원문: input/clippings/$12B of US ratepayers' money wasted on a modeling mistake ... .md

원문은 PJM 의 신뢰도 계획 모형을 공개 자료로 되짜서, 겨울철 발전 성능을 제대로
반영했다면 사야 할 용량이 얼마나 줄었을지를 냈다. 그 결과가 요금으로 얼마인지가
이 모델이 다루는 자리다.

사슬은 짧다.

    경매 비용 = 낙찰 용량 × 낙찰 가격 × 365일

낙찰 가격은 수요곡선과 공급곡선이 만나는 자리에서 정해진다. 그런데 PJM 의 공급
곡선은 오른쪽 끝에서 수직으로 선다 — 2025/26 경매에서 입찰의 79%가 2~5달러였고
마지막 1%가 352달러까지 올라갔다. 그래서 수요곡선이 조금만 왼쪽으로 밀려도 가격이
절벽에서 내려온다. 용량은 거의 안 줄고 가격만 반토막이 난다.

이 모델은 그 지렛대를 숫자로 잰다. 기가와트당 가격이 얼마나 떨어지나.
"""

DAYS_PER_YEAR = 365
MW_PER_GW = 1000


def auction_cost(cleared_gw, price_usd_mw_day, days=DAYS_PER_YEAR):
    """경매 하나가 한 해에 물리는 돈. 용량은 기가와트, 가격은 메가와트·일당 달러."""
    return cleared_gw * MW_PER_GW * price_usd_mw_day * days


def saving(cleared_gw, price, cf_cleared_gw, cf_price, days=DAYS_PER_YEAR):
    """실제와 반사실의 차이. 용량이 줄어드는 몫과 가격이 내려가는 몫이 섞인다."""
    return (auction_cost(cleared_gw, price, days)
            - auction_cost(cf_cleared_gw, cf_price, days))


def split_saving(cleared_gw, price, cf_cleared_gw, cf_price, days=DAYS_PER_YEAR):
    """절감액을 둘로 가른다 — 가격이 내려간 몫과 용량이 줄어든 몫.

    가격 몫은 실제 산 용량 전부에 걸리고, 용량 몫은 줄어든 만큼에만 걸린다.
    원문이 「135달러 할인이 135.7기가와트 전부에 곱해진다」고 적은 자리다.
    """
    price_part = (price - cf_price) * cleared_gw * MW_PER_GW * days
    volume_part = (cleared_gw - cf_cleared_gw) * MW_PER_GW * cf_price * days
    return {'price': price_part, 'volume': volume_part,
            'total': price_part + volume_part}


def price_sensitivity(shift_gw, price_drop_usd_mw_day):
    """수요곡선을 1기가와트 왼쪽으로 밀면 가격이 얼마나 내려가나.

    공급곡선이 오른쪽 끝에서 수직이라 이 값은 상수가 아니다. 절벽의 어느 높이에
    걸려 있느냐로 달라진다 — 그래서 해마다 다시 잰다.
    """
    return price_drop_usd_mw_day / shift_gw


def overlap(a_gw, b_gw, combined_gw):
    """따로 세면 a+b 인데 같이 세면 combined 다. 겹치는 몫과 비율.

    두 개선이 같은 시간대를 고치기 때문이다 — 요구 용량을 정하는 것은 한 해에
    몇 시간뿐인 깊은 추위이고, 둘 다 그 시간을 손본다.
    """
    lost = a_gw + b_gw - combined_gw
    return {'sum': a_gw + b_gw, 'combined': combined_gw, 'overlap': lost,
            'overlap_pct': lost / (a_gw + b_gw) * 100}


def per_person(total_usd, residents_millions):
    """권역 주민 한 사람 몫."""
    return total_usd / (residents_millions * 1_000_000)


def implied_capacity(cost_usd, price_usd_mw_day, days=DAYS_PER_YEAR):
    """비용과 가격에서 용량을 거꾸로 푼다. 발표된 합계가 어떤 용량을 전제하는지 본다."""
    return cost_usd / (price_usd_mw_day * days) / MW_PER_GW
