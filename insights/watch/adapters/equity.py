# -*- coding: utf-8 -*-
"""종목 어댑터 — 이미 있는 밸류에이션 자료를 그대로 쓴다. 새로 받아 오지 않는다.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 넷.

1. **원천이 둘이고 꼴이 다르다.** 미국 6종목은 `facts.json`(연 단위 SEC 개념 + 시장가),
   삼성전자는 `fundamentals.json`·`price.json`(분기 단위, 억원)이다. 억지로 한 꼴로
   합치지 않는다 — 합치는 순간 어느 쪽 기준인지가 값에서 사라진다.
2. **추정치를 공표치와 섞지 않는다.** 삼성 분기에는 `consensus: true` 인 칸이 있다.
   시계열에서 빼고, 뺐다는 것을 남긴다.
3. **주가 이력은 없다.** 두 원천 다 그 시점 스냅숏이라 값 하나뿐이다. series 를
   지어내지 않는다 — 없으면 도해도 안 서고 W8 도 재지 않는다.
4. **밸류에이션을 다시 하지 않는다.** 적정가를 재는 자리는 `insights/valuation/` 이고
   여기는 「무엇이 일어나면 그 계산을 다시 하나」만 센다.
"""
import io, os, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
VAL = os.path.join(ROOT, 'insights', 'valuation')


class AdapterError(Exception):
    pass


def _folder(ticker):
    p = os.path.join(VAL, ticker)
    if os.path.isdir(p):
        return p
    hit = [d for d in glob.glob(os.path.join(VAL, ticker + '-*')) if os.path.isdir(d)]
    return hit[0] if hit else None


def _load(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def _m(value, as_of, kind, unit, src, series=(), note=''):
    return {'value': value, 'as_of': as_of, 'kind': kind, 'unit': unit, 'src': src,
            'area': '', 'level': 'ticker', 'series': [list(x) for x in series],
            'partial': False, 'note': note}


def _from_facts(folder, ticker):
    """미국 6종목 — facts.json. SEC 개념은 회계연도 열쇠라 연 단위 시계열이 된다."""
    d = _load(os.path.join(folder, 'facts.json'))
    src = 'insights/valuation/%s/facts.json (SEC 공시 · %s 기준)' % (
        os.path.basename(folder), (d.get('fetched_at') or '')[:10])
    out = {}
    con = (d.get('sec') or {}).get('concepts') or {}

    def annual(key):
        got = con.get(key) or {}
        s = []
        for y in sorted(got):
            v = (got[y] or {}).get('val')
            if v is not None:
                s.append((y, v))
        return s

    rev, cost = annual('revenue'), dict(annual('cost_of_revenue'))
    if rev:
        # 백만 단위로 줄인다. 원값은 자리수가 커서 판 위에서 안 읽힌다
        s = [(y, round(v / 1e6, 1)) for y, v in rev]
        out['revenue'] = _m(s[-1][1], s[-1][0], '공표', '백만 달러', src, s)
        yoy = [(rev[i][0], round((rev[i][1] / rev[i - 1][1] - 1) * 100, 2))
               for i in range(1, len(rev)) if rev[i - 1][1]]
        if yoy:
            out['revenue_yoy'] = _m(yoy[-1][1], yoy[-1][0], '공표', '%', src, yoy)
        gm = [(y, round((1 - cost[y] / v) * 100, 2)) for y, v in rev
              if y in cost and v]
        if gm:
            out['gross_margin'] = _m(gm[-1][1], gm[-1][0], '공표', '%', src, gm)

    mk = d.get('market') or {}
    if mk.get('price') is not None:
        out['price'] = _m(mk['price'], (mk.get('as_of') or '')[:10], '공표',
                          mk.get('currency') or '', src,
                          note='그 시점 스냅숏이다 — 주가 이력이 이 파일에 없다')

    mp = os.path.join(VAL, '_multiples.json')
    if os.path.exists(mp):
        m = _load(mp)
        row = (m.get('rows') or {}).get(ticker)
        if row and (row.get('next_year') or {}).get('fwd_per') is not None:
            out['fwd_pe'] = _m(round(row['next_year']['fwd_per'], 2),
                               (row.get('as_of') or '')[:10], '추정', '배',
                               'insights/valuation/_multiples.json · ' + str(m.get('note') or ''),
                               note='다음 회계연도 추정 주당순이익 기준이라 성격이 추정치다')
    return out


def _from_naver(folder):
    """삼성전자 — 분기 자료다. consensus 칸은 추정치라 시계열에서 뺀다."""
    fu = _load(os.path.join(folder, 'fundamentals.json'))
    src = 'insights/valuation/%s/fundamentals.json (%s)' % (
        os.path.basename(folder), ' · '.join(fu.get('sources') or [])[:80])
    qs = [q for q in (fu.get('quarters') or []) if not q.get('consensus')]
    dropped = len(fu.get('quarters') or []) - len(qs)
    out = {}

    def ser(key):
        s = []
        for q in qs:
            v = q.get(key)
            k = str(q.get('key') or '')
            if v is not None and len(k) == 6:
                s.append(('%s-%s' % (k[:4], k[4:]), v))
        s.sort()
        return s

    note = ('추정치 %d분기를 뺐다 — 공표치와 한 선에 서면 어디부터 추정인지가 사라진다'
            % dropped) if dropped else ''
    rev = ser('revenue_100m')
    if rev:
        out['revenue'] = _m(rev[-1][1], rev[-1][0], '공표', '억원', src, rev, note)
        op = dict(ser('operating_profit_100m'))
        om = [(t, round(op[t] / v * 100, 2)) for t, v in rev if t in op and v]
        if om:
            out['op_margin'] = _m(om[-1][1], om[-1][0], '공표', '%', src, om, note)
    ni = ser('net_income_100m')
    if ni:
        out['net_income'] = _m(ni[-1][1], ni[-1][0], '공표', '억원', src, ni, note)

    pp = os.path.join(folder, 'price.json')
    if os.path.exists(pp):
        pr = _load(pp)
        if pr.get('close') is not None:
            out['price'] = _m(pr['close'], (pr.get('as_of') or '')[:10], '공표', '원',
                              'insights/valuation/%s/price.json' % os.path.basename(folder),
                              note='그 시점 스냅숏이다 — 주가 이력이 이 파일에 없다')
    return out


def fetch(target, area=None, **_kw):
    """area 는 안 쓴다 — 종목에는 지역이 없다. 계약을 맞추려고 자리만 둔다.

    target 은 워치 줄의 ticker 다(watch_fetch 가 넘긴다)."""
    folder = _folder(target)
    if folder is None:
        raise AdapterError('insights/valuation/ 에 %s 폴더가 없다' % target)
    if os.path.exists(os.path.join(folder, 'facts.json')):
        return _from_facts(folder, target)
    if os.path.exists(os.path.join(folder, 'fundamentals.json')):
        return _from_naver(folder)
    raise AdapterError('%s 에 facts.json 도 fundamentals.json 도 없다' % folder)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for t in (sys.argv[1:] or ['NVDA', '005930']):
        print('##', t)
        try:
            for k, v in sorted(fetch(t).items()):
                print('   %-14s %-12s %12s %-12s 점 %-3d %s'
                      % (k, v['as_of'], v['value'], v['unit'], len(v['series']), v['kind']))
        except AdapterError as e:
            print('   실패:', e)
