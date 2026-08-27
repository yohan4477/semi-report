# -*- coding: utf-8 -*-
"""SEC XBRL · 야후 주가 · FRED 국채금리에서 밸류에이션 입력값을 떠서
insights/valuation/<티커>/facts.json 에 조회 시각과 함께 떨어뜨린다.

왜 파일로 떨어뜨리나: 렌더 시점에 API를 때리면 페이지를 다시 만들 때마다 숫자가
조용히 바뀐다. 어제 읽은 글과 오늘 읽은 글이 달라지면 인용이 무의미해진다.

설계는 docs/superpowers/specs/2026-08-26-미국-빅테크-밸류에이션-design.md.
베타는 야후가 주는 값을 받지 않고 주가 시계열을 ^GSPC에 회귀해 직접 낸다 —
산출 구간·주기가 안 밝혀진 값은 감사가 안 된다.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
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
    # 회사마다 태그가 다르다. 엔비디아와 아마존은 최근 연도를
    # PaymentsToAcquireProductiveAssets 로 내고 옛 연도만 PP&E 로 낸다 —
    # 후보를 합치지 않으면 최근 설비투자가 통째로 비고, 아마존은 설비투자가
    # 감가상각의 0.10배라는 말이 안 되는 값이 나온다.
    'capex': ['PaymentsToAcquirePropertyPlantAndEquipment',
              'PaymentsToAcquireProductiveAssets',
              'PaymentsToAcquireOtherPropertyPlantAndEquipment'],
    'ocf': ['NetCashProvidedByUsedInOperatingActivities'],
    # 영업 밖 손익. R3이 EBIT을 쓰기 전에 걷어내라는 자리다.
    # 알파벳은 보유 지분(앤트로픽·스페이스X 등)을 공정가치로 다시 재 순이익에 태운다 —
    # 2026년 2분기 한 분기에 990억 달러가 들어왔다. 현금이 아니라 평가액이다.
    # 이걸 안 빼면 실효세율도 순이익도 DCF에 못 쓴다.
    'nonoperating': ['NonoperatingIncomeExpense'],
    'equity_fv_gain': ['EquitySecuritiesFvNiGainLoss'],
    'cash_taxes_paid': ['IncomeTaxesPaidNet', 'IncomeTaxesPaid'],
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
            rec = dict(end=x['end'], val=x['val'], filed=x.get('filed', ''), tag=tag,
                       start=x.get('start'))
            prev = out.get(fy)
            if prev is None:
                out[fy] = rec
            elif prev['tag'] == tag and x.get('filed', '') >= prev['filed']:
                out[fy] = rec
    return out


# 기간 값(손익계산서·현금흐름표)과 시점 값(재무상태표)을 가른다.
#
# 기간 값만 TTM이 뜻을 갖는다. 재무상태표 항목은 어느 시점의 잔액이라 열두 달을
# 더하면 안 된다 — 현금 잔액 넷을 더한 값은 아무것도 아니다. 시점 값은 가장 최근
# 것 하나를 그대로 쓴다.
#
# 10-Q는 손익도 현금흐름도 **회계연도 시작부터 누적**을 함께 낸다. 4분기는 10-Q가
# 아예 없어(10-K가 연간으로만 낸다) 분기 넷을 이어 붙이는 방법이 막힌다 —
# 2026-08-26에 손익 TTM이 통째로 빈 원인이 이것이었다. 그래서 기간 값은 전부
# 「직전 연간 + 올해 누적 − 작년 같은 기간 누적」으로 만든다.
FLOW = ('revenue', 'ebit', 'net_income', 'tax_expense', 'pretax_income',
        'dna', 'lease_amortization', 'capex', 'ocf',
        'nonoperating', 'equity_fv_gain', 'cash_taxes_paid')


def quarters(facts, tags, kind):
    """10-Q에서 분기 값을 뽑는다. kind로 기간 성격을 가른다.

    **손익계산서와 현금흐름표는 10-Q에서 기간 잡는 법이 다르다.** 손익은 그 분기만
    담고(약 90일), 현금흐름은 회계연도 시작부터 누적이다(1분기 90일 · 2분기 180일 ·
    3분기 270일). 둘을 같은 방식으로 더하면 현금흐름이 배로 잡힌다.

      kind='flow'  분기 값(80~100일)만 받는다 — 손익계산서용
      kind='cum'   누적 값을 그대로 받는다 — 현금흐름표용. 기간 일수를 함께 남긴다
    """
    out = {}
    for tag in tags:
        node = facts.get('facts', {}).get('us-gaap', {}).get(tag)
        if not node:
            continue
        for x in node.get('units', {}).get('USD', []):
            if x.get('form') != '10-Q' or 'start' not in x:
                continue
            days = (datetime.strptime(x['end'], '%Y-%m-%d')
                    - datetime.strptime(x['start'], '%Y-%m-%d')).days
            if kind == 'flow' and not (80 <= days <= 100):
                continue
            if kind == 'cum' and days < 80:
                continue
            key = (x['start'], x['end'])
            prev = out.get(key)
            if prev is None or x.get('filed', '') >= prev['filed']:
                out[key] = dict(start=x['start'], end=x['end'], val=x['val'],
                                days=days, filed=x.get('filed', ''), tag=tag)
    return out


def ttm(facts, name, tags, annual):
    """최근 12개월 값. 기준연도가 낡는 것을 막는다.

    왜 필요한가: 10-K는 회계연도가 끝나야 나온다. 알파벳 FY2025는 2025-12-31에
    끝났는데 주가는 2026-08-25다 — 237일 사이에 두 분기가 지났다. 그 사이 영업이익률이
    32.0%에서 34.1%로 올랐다. FY2025로 DCF를 돌리면 이미 지난 이야기를 할인하게 된다.

    손익은 최근 네 분기를 더한다. 현금흐름은 누적 보고라 더할 수 없어
    「직전 회계연도 + 올해 누적 − 작년 같은 기간 누적」으로 만든다.
    """
    if name in FLOW:
        cum = quarters(facts, tags, 'cum')
        if not cum:
            return None
        # 누적 구간은 **회계연도 첫날에서 시작한 것만** 받는다.
        #
        # 어떤 회사는 10-Q에 최근 12개월 구간을 따로 싣는다. 그것을 「올해 누적」으로
        # 잡으면 연간에 더하고 엉뚱한 구간을 빼게 되어 값이 통째로 틀어진다 —
        # 아마존이 2026-08-26에 잉여현금흐름 -14B 라는 계산 착오를 냈다.
        # 회계연도 첫날은 직전 연간 기록의 시작일에서 가져온다.
        # 월·일을 정확히 맞추지 않는다. 엔비디아와 애플은 52/53주 회계연도라 시작일이
        # 해마다 하루이틀 움직인다 — 정확히 맞추면 그 회사만 분기가 통째로 걸러진다.
        # 대신 「직전 회계연도가 끝난 직후에 시작하는가」로 본다.
        ends = sorted(r['end'] for r in annual.get(name, {}).values())
        if ends:
            def _fresh(v):
                st = datetime.strptime(v['start'], '%Y-%m-%d')
                for e in ends:
                    gap = (st - datetime.strptime(e, '%Y-%m-%d')).days
                    if 0 <= gap <= 10:
                        return True
                return False
            cum = {k: v for k, v in cum.items() if _fresh(v)}
            if not cum:
                return None
        cur = max(cum.values(), key=lambda x: x['end'])
        # 최근 분기가 직전 회계연도보다 뒤인지 본다. 어떤 태그는 옛날에만 10-Q로
        # 나오고 요즘은 10-K에만 실린다 — IncomeTaxesPaid가 그렇다. 그때 여기서
        # 막지 않으면 2016년 분기를 붙잡아 TTM이라 부르게 된다(2026-08-26에 납부세금이
        # 실제로 그렇게 계산돼 실효세율이 1.2%로 나왔다).
        newest_annual = max(annual.get(name, {}), default=None)
        if newest_annual and cur['end'] <= annual[name][newest_annual]['end']:
            return None
        # 더할 연간은 **누적 구간이 시작되기 직전에 끝난 회계연도**다. 연도 이름에서
        # 1을 빼면 안 된다 — 엔비디아는 회계연도가 1월에 끝나서 2026-01-25 에 끝난
        # 연간이 '2026'으로 들어가는데, 2026-07-26 누적에서 1을 빼면 한 해 낡은
        # 2025-01-26 연간을 더하게 된다. 2026-08-27에 엔비디아 최근 12개월 매출이
        # 3,030억이 아니라 2,175억으로 나온 원인이 이것이다.
        cur_start = datetime.strptime(cur['start'], '%Y-%m-%d')
        base = [(k, v) for k, v in annual.get(name, {}).items()
                if 0 <= (cur_start - datetime.strptime(v['end'], '%Y-%m-%d')).days <= 10]
        if not base:
            return None
        fy, last_fy = max(base, key=lambda kv: kv[1]['end'])
        # 작년 같은 기간(일수가 같고 한 해 전에 끝난 누적 구간)을 찾는다. 여기서도
        # 연도 이름을 쓰지 않고 끝난 날의 간격으로 고른다.
        cur_end = datetime.strptime(cur['end'], '%Y-%m-%d')
        prior = [x for x in cum.values()
                 if abs(x['days'] - cur['days']) <= 10
                 and 330 <= (cur_end - datetime.strptime(x['end'], '%Y-%m-%d')).days <= 400]
        if not prior:
            return None
        p = max(prior, key=lambda x: x['end'])
        return dict(val=last_fy['val'] + cur['val'] - p['val'],
                    window='%s 연간 + %s~%s − %s~%s' % (
                        fy, cur['start'], cur['end'], p['start'], p['end']),
                    end=cur['end'], method='누적 보고라 직전 연간에 올해 누적을 더하고 작년 같은 기간을 뺀다')
    # 시점 값(재무상태표). 가장 최근 잔액 하나를 그대로 쓴다 — 더하지 않는다.
    latest = None
    for tag in tags:
        node = facts.get('facts', {}).get('us-gaap', {}).get(tag)
        if not node:
            continue
        for x in node.get('units', {}).get('USD', []):
            if 'start' in x or x.get('form') not in ('10-Q', '10-K'):
                continue
            if latest is None or (x['end'], x.get('filed', '')) > (latest['end'], latest['filed']):
                latest = dict(end=x['end'], val=x['val'], filed=x.get('filed', ''), tag=tag)
    if latest is None:
        return None
    return dict(val=latest['val'], window=latest['end'], end=latest['end'],
                method='시점 값이라 최근 잔액 하나를 쓴다')


def sec_facts(ticker):
    cik = CIKS[ticker]
    raw = get('https://data.sec.gov/api/xbrl/companyfacts/CIK%s.json' % cik)
    facts = json.loads(raw)
    out = {'entity': facts.get('entityName'), 'cik': cik, 'concepts': {}, 'ttm': {}}
    for name, tags in CONCEPTS.items():
        got = annuals(facts, tags)
        if got:
            out['concepts'][name] = {str(k): v for k, v in sorted(got.items())}
    # 최근 12개월. 10-K가 나온 뒤 지난 분기를 담아 기준연도가 낡는 것을 막는다.
    #
    # 회계연도 말이 최근인 회사(마이크로소프트는 6월 말)는 10-K 자체가 이미 최근
    # 12개월이라 더할 분기가 없다. 그때 TTM 을 비우면 그 회사만 기준연도가 통째로
    # 사라지므로 직전 연간을 그대로 쓰고 창에 그 사실을 적는다.
    for name, tags in CONCEPTS.items():
        got = ttm(facts, name, tags, out['concepts'])
        if not got and name in FLOW:
            ann = out['concepts'].get(name, {})
            if ann:
                fy = max(ann)
                got = dict(val=ann[fy]['val'], window='%s 회계연도 (뒤에 분기 보고 없음)' % fy,
                           end=ann[fy]['end'], method='회계연도 말이 최근이라 연간이 곧 최근 12개월')
        if got:
            out['ttm'][name] = got
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


def beta(stock_series, index_series, window=None):
    """일간 수익률을 지수에 회귀한 기울기. 공분산/분산으로 낸다.

    날짜(초 단위 타임스탬프)가 맞는 날만 짝지어 쓴다 — 휴장일이 어긋나면
    수익률이 한 칸씩 밀려 베타가 엉뚱하게 나온다.

    window 는 쓸 거래일 수다. 룰북 R17 이 삼성전자에 52주 베타를 썼으므로
    기본값을 252일로 두고 부른다. 2년치로 재면 엔비디아 베타가 1.96 인데
    52주로 재면 다른 값이 나온다 — 어느 구간으로 쟀는지가 할인율을 통째로
    움직이므로 창을 값과 함께 남긴다.
    """
    a = dict(stock_series)
    b = dict(index_series)
    days = sorted(set(a) & set(b))
    if window:
        days = days[-(window + 1):]
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
    return dict(beta=cov / var, n_days=n, window='52주' if window else '2년',
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


def consensus(ticker):
    """야후에서 애널리스트 매출·주당순이익 추정치를 받는다. basis 는 consensus 다.

    이 장의 basis 넷(sec·semi·mkt·ours)에 다섯째를 더하는 값이다. 우리 가정이
    보수적이라 값이 낮게 나오는지, 아니면 시장 기대 자체가 우리보다 훨씬 높은지를
    독자가 직접 가르려면 「남들은 얼마로 보나」가 같은 화면에 있어야 한다.

    이 엔드포인트는 쿠키와 crumb 을 요구한다. 못 받으면 None 을 돌려주고 값을
    비운다 — 컨센서스가 없다고 나머지 계산이 멈추면 안 된다.

    받는 구간은 넷이다. 이번 분기(0q) · 다음 분기(+1q) · 이번 회계연도(0y) ·
    다음 회계연도(+1y). 그 뒤는 야후가 안 준다. 두 해까지만 앵커로 쓰고 그 뒤는
    우리가 내린다.
    """
    import http.cookiejar
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
    cj = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    def _g(u):
        return op.open(urllib.request.Request(u, headers=ua), timeout=40).read().decode('utf-8', 'replace')

    try:
        try:
            _g('https://fc.yahoo.com')          # 쿠키만 받는다. 404 여도 쿠키는 남는다
        except urllib.error.HTTPError:
            pass
        crumb = _g('https://query1.finance.yahoo.com/v1/test/getcrumb').strip()
        if not crumb:
            return None
        raw = _g('https://query2.finance.yahoo.com/v10/finance/quoteSummary/%s'
                 '?modules=earningsTrend&crumb=%s' % (ticker, urllib.parse.quote(crumb)))
        trend = json.loads(raw)['quoteSummary']['result'][0]['earningsTrend']['trend']
    except Exception:
        return None

    out = []
    for t in trend:
        rev = t.get('revenueEstimate') or {}
        eps = t.get('earningsEstimate') or {}
        if rev.get('avg', {}).get('raw') is None:
            continue
        out.append(dict(
            period=t.get('period'), end=t.get('endDate'),
            revenue=rev['avg']['raw'],
            revenue_low=rev.get('low', {}).get('raw'),
            revenue_high=rev.get('high', {}).get('raw'),
            analysts=rev.get('numberOfAnalysts', {}).get('raw'),
            eps=eps.get('avg', {}).get('raw'),
            growth=t.get('growth', {}).get('raw')))
    if not out:
        return None
    return dict(periods=out, fetched_at=datetime.now(timezone.utc).isoformat(),
                source='query2.finance.yahoo.com/v10/finance/quoteSummary earningsTrend',
                note='애널리스트 평균 추정치. 0q 이번 분기 · +1q 다음 분기 · '
                     '0y 이번 회계연도 · +1y 다음 회계연도. 그 뒤는 안 준다')


def build(ticker):
    now = datetime.now(timezone.utc).isoformat()
    px = price(ticker)
    idx = price('%5EGSPC')
    sec = sec_facts(ticker)
    # 메타는 us-gaap 에도 dei 에도 발행주식수가 없다(EntityPublicFloat 하나뿐).
    # 그때는 희석 가중평균으로 시총을 내고 어느 것을 썼는지 적는다 — 안 그러면
    # 그 회사만 시가총액이 통째로 빈다.
    _sh = sec.get('shares_outstanding') or sec.get('shares_diluted') or {}
    shares = _sh.get('val')
    shares_basis = ('발행주식수' if sec.get('shares_outstanding') else
                    '희석 가중평균(발행주식수가 공시에 없다)')
    doc = {
        'ticker': ticker,
        'fetched_at': now,
        'sec': sec,
        'market': {
            'price': px['price'], 'currency': px['currency'],
            'as_of': px['market_time'],
            'market_cap': (px['price'] * shares) if shares else None,
            'market_cap_note': '주가 × %s. 야후 시총을 받지 않는다' % shares_basis,
            'shares_basis': shares_basis,
            'source': 'query1.finance.yahoo.com/v8/finance/chart',
        },
        # 룰북 R17 이 쓴 창은 52주다. 2년치도 함께 남겨 어느 창이 얼마나
        # 다른 값을 내는지 감사할 수 있게 한다.
        'beta': beta(px['series'], idx['series'], window=252),
        'beta_2y': beta(px['series'], idx['series']),
        'risk_free': rf(),
        # 애널리스트 추정치. 못 받으면 None 이고 그때는 컨센서스 케이스를 안 세운다.
        'consensus': consensus(ticker),
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
