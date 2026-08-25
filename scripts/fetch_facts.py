# -*- coding: utf-8 -*-
"""SEC XBRL · 야후 주가 · FRED 국채금리에서 밸류에이션 입력값을 떠서
insights/valuation/<티커>/facts.json 에 조회 시각과 함께 떨어뜨린다.

왜 파일로 떨어뜨리나: 렌더 시점에 API를 때리면 페이지를 다시 만들 때마다 숫자가
조용히 바뀐다. 어제 읽은 글과 오늘 읽은 글이 달라지면 인용이 무의미해진다.

설계는 docs/superpowers/specs/2026-08-26-미국-빅테크-밸류에이션-design.md.
베타는 야후가 주는 값을 받지 않고 주가 시계열을 ^GSPC에 회귀해 직접 낸다 —
산출 구간·주기가 안 밝혀진 값은 감사가 안 된다.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

UA = 'insight-dashboard yohan4477@gmail.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'insights', 'valuation')

# 회사 → CIK. SEC는 10자리 0채움을 요구한다.
CIKS = {
    'GOOGL': '0001652044',
    'MSFT': '0000789019',
    'NVDA': '0001045810',
    'AMZN': '0001018724',
    'META': '0001326801',
    'AAPL': '0000320193',
}

# 뽑을 XBRL 태그. 한 개념에 태그가 여럿인 회사가 있어 후보를 순서대로 시도한다.
CONCEPTS = {
    'revenue': ['RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenues'],
    'ebit': ['OperatingIncomeLoss'],
    'net_income': ['NetIncomeLoss'],
    'tax_expense': ['IncomeTaxExpenseBenefit'],
    'pretax_income': ['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'],
    # 알파벳은 DepreciationDepletionAndAmortization을 안 쓰고 Depreciation으로 낸다.
    # 리스자산 상각은 별개 태그라 따로 받는다 — 합칠지는 회사마다 판단이 갈린다.
    'dna': ['DepreciationDepletionAndAmortization', 'DepreciationAmortizationAndAccretionNet',
            'Depreciation'],
    'lease_amortization': ['FinanceLeaseRightOfUseAssetAmortization'],
    'capex': ['PaymentsToAcquirePropertyPlantAndEquipment'],
    'ocf': ['NetCashProvidedByUsedInOperatingActivities'],
    'cash': ['CashAndCashEquivalentsAtCarryingValue'],
    'st_investments': ['ShortTermInvestments', 'MarketableSecuritiesCurrent'],
    'lt_debt': ['LongTermDebtNoncurrent', 'LongTermDebt'],
    'st_debt': ['LongTermDebtCurrent'],
    # 운전자본 (R7)
    'receivables': ['AccountsReceivableNetCurrent'],
    'inventory': ['InventoryNet'],
    'payables': ['AccountsPayableCurrent'],
}


def get(url, headers=None, tries=3):
    req = urllib.request.Request(url, headers=headers or {'User-Agent': UA})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and i < tries - 1:
                time.sleep(2 ** i)
                continue
            raise
    raise RuntimeError('unreachable')


def annuals(facts, tags, ns='us-gaap', unit='USD'):
    """companyfacts에서 연간(10-K, FY) 값만 골라 회계연도 → 값으로 돌린다.

    같은 연도가 여러 번 보고된다(원래 10-K + 다음 해 비교표시). 가장 나중에
    제출된 것이 정정 반영본이라 그것을 남긴다.

    **후보 태그를 합친다 — 첫 매치에서 끊지 않는다.** 회사가 도중에 태그를 갈아타면
    연도가 두 태그에 갈린다. 알파벳은 FY2022~2024 매출이
    RevenueFromContractWithCustomerExcludingAssessedTax에, FY2025가 Revenues에 있다.
    첫 매치에서 끊으면 가장 중요한 최근 연도가 통째로 빈다 — 2026-08-26에 실제로 그랬다.
    앞선 태그가 이긴다(더 좁게 정의된 태그를 우선 후보로 둔다).
    """
    out = {}
    for tag in tags:
        node = facts.get('facts', {}).get(ns, {}).get(tag)
        if not node:
            continue
        vals = node.get('units', {}).get(unit)
        if not vals:
            continue
        for x in vals:
            if x.get('form') != '10-K' or x.get('fp') != 'FY':
                continue
            fy = x.get('fy')
            if fy is None:
                continue
            # 손익·현금흐름은 기간 값이라 start가 있고, 재무상태표는 시점 값이라 없다.
            if 'start' in x:
                days = (datetime.strptime(x['end'], '%Y-%m-%d')
                        - datetime.strptime(x['start'], '%Y-%m-%d')).days
                if days < 300:  # 분기·반기 값은 버린다
                    continue
            prev = out.get(fy)
            if prev is None:
                out[fy] = dict(end=x['end'], val=x['val'], filed=x.get('filed', ''), tag=tag)
            elif prev['tag'] == tag and x.get('filed', '') >= prev['filed']:
                out[fy] = dict(end=x['end'], val=x['val'], filed=x.get('filed', ''), tag=tag)
    return out


def sec_facts(ticker):
    cik = CIKS[ticker]
    raw = get('https://data.sec.gov/api/xbrl/companyfacts/CIK%s.json' % cik)
    facts = json.loads(raw)
    out = {'entity': facts.get('entityName'), 'cik': cik, 'concepts': {}}
    for name, tags in CONCEPTS.items():
        got = annuals(facts, tags)
        if got:
            out['concepts'][name] = {str(k): v for k, v in sorted(got.items())}
    # 주식수. dei의 EntityCommonStockSharesOutstanding을 먼저 보되, 없는 회사가 있다 —
    # 알파벳의 dei에는 EntityPublicFloat 하나뿐이다. 그때는 us-gaap 쪽으로 내려간다.
    #
    # 발행주식수와 희석 가중평균 둘 다 남긴다. 시총은 발행주식수로 곱하고(어느 시점의
    # 실제 주식 수), 주당가치는 희석 기준으로 낼지 판단이 갈리기 때문이다. 하나만
    # 남기면 나중에 어느 것을 썼는지가 안 남는다.
    for key, ns, tags in (
            ('shares_outstanding', 'dei', ['EntityCommonStockSharesOutstanding']),
            ('shares_outstanding', 'us-gaap', ['CommonStockSharesOutstanding']),
            ('shares_diluted', 'us-gaap', ['WeightedAverageNumberOfDilutedSharesOutstanding']),
            ('shares_basic', 'us-gaap', ['WeightedAverageNumberOfSharesOutstandingBasic']),
    ):
        if out.get(key):
            continue
        got = annuals(facts, tags, ns=ns, unit='shares')
        if got:
            fy = max(got)
            out[key] = dict(val=got[fy]['val'], end=got[fy]['end'],
                            tag=got[fy]['tag'], ns=ns)
    return out


def price(ticker, rng='2y'):
    """야후 chart에서 현재가와 종가 시계열을 받는다."""
    url = ('https://query1.finance.yahoo.com/v8/finance/chart/%s'
           '?range=%s&interval=1d' % (ticker, rng))
    d = json.loads(get(url, headers={'User-Agent': 'Mozilla/5.0'}))
    res = d['chart']['result'][0]
    closes = res['indicators']['quote'][0]['close']
    ts = res['timestamp']
    series = [(t, c) for t, c in zip(ts, closes) if c is not None]
    return dict(
        price=res['meta']['regularMarketPrice'],
        currency=res['meta']['currency'],
        market_time=datetime.fromtimestamp(
            res['meta']['regularMarketTime'], timezone.utc).isoformat(),
        series=series,
    )


def beta(stock_series, index_series):
    """일간 수익률을 지수에 회귀한 기울기. 공분산/분산으로 낸다.

    날짜(초 단위 타임스탬프)가 맞는 날만 짝지어 쓴다 — 휴장일이 어긋나면
    수익률이 한 칸씩 밀려 베타가 엉뚱하게 나온다.
    """
    a = dict(stock_series)
    b = dict(index_series)
    days = sorted(set(a) & set(b))
    if len(days) < 60:
        return None
    rs, ri = [], []
    for prev, cur in zip(days, days[1:]):
        rs.append(a[cur] / a[prev] - 1)
        ri.append(b[cur] / b[prev] - 1)
    n = len(rs)
    ms, mi = sum(rs) / n, sum(ri) / n
    cov = sum((x - ms) * (y - mi) for x, y in zip(rs, ri)) / (n - 1)
    var = sum((y - mi) ** 2 for y in ri) / (n - 1)
    return dict(beta=cov / var, n_days=n,
                start=datetime.fromtimestamp(days[0], timezone.utc).date().isoformat(),
                end=datetime.fromtimestamp(days[-1], timezone.utc).date().isoformat(),
                index='^GSPC', freq='daily')


def rf():
    """FRED 10년 국채. 마지막 유효값(휴장일은 '.'으로 온다)."""
    txt = get('https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10').decode()
    for line in reversed(txt.strip().splitlines()):
        date, val = line.split(',')
        if val not in ('.', 'value'):
            return dict(rate=float(val) / 100, date=date, series='DGS10 (US 10Y)')
    return None


def build(ticker):
    now = datetime.now(timezone.utc).isoformat()
    px = price(ticker)
    idx = price('%5EGSPC')
    sec = sec_facts(ticker)
    shares = (sec.get('shares_outstanding') or {}).get('val')
    doc = {
        'ticker': ticker,
        'fetched_at': now,
        'sec': sec,
        'market': {
            'price': px['price'], 'currency': px['currency'],
            'as_of': px['market_time'],
            'market_cap': (px['price'] * shares) if shares else None,
            'market_cap_note': '주가 × SEC 보고 주식수. 야후 시총을 받지 않는다',
            'source': 'query1.finance.yahoo.com/v8/finance/chart',
        },
        'beta': beta(px['series'], idx['series']),
        'risk_free': rf(),
    }
    d = os.path.join(OUT, ticker)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'facts.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    return p, doc


if __name__ == '__main__':
    for t in (sys.argv[1:] or ['GOOGL']):
        p, doc = build(t.upper())
        m, b = doc['market'], doc['beta']
        print('%s  %s' % (t.upper(), doc['sec']['entity']))
        print('  주가 %s %.2f (%s)' % (m['currency'], m['price'], m['as_of'][:10]))
        if m['market_cap']:
            print('  시총 %.1fB' % (m['market_cap'] / 1e9))
        if b:
            print('  베타 %.3f (%s~%s, %d일)' % (b['beta'], b['start'], b['end'], b['n_days']))
        print('  Rf   %.2f%% (%s)' % (doc['risk_free']['rate'] * 100, doc['risk_free']['date']))
        print('  개념 %d종 -> %s' % (len(doc['sec']['concepts']), p))
