# -*- coding: utf-8 -*-
"""밸류체인 엔티티가 SEC 에 등록한 업종(SIC)을 받아 둔다.

SEC 에 제출하는 회사만 값이 찬다 — 미국 등록법인과 20-F 를 내는 외국 법인이다.
한국·일본 상장사와 비상장·익명 상대는 SEC 에 없으니 빈칸으로 남는다.
받은 것은 data/valuechain/sec_sector.json 에 적어 두고, 탐색기는 그 파일만 읽는다.
"""
import json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENT = os.path.join(ROOT, 'data', 'valuechain', 'entities.json')
OUT = os.path.join(ROOT, 'data', 'valuechain', 'sec_sector.json')
UA = {'User-Agent': 'semianalysis-research yohan4477@gmail.com'}

# SEC 제출인 이름이 우리 표기와 다른 곳은 손으로 이어 준다
ALIAS = {
    'tsmc': 'TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD',
    'asml': 'ASML HOLDING NV',
    'amd': 'ADVANCED MICRO DEVICES INC',
    'foxconn': None,
}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()

def norm(s):
    s = (s or '').lower()
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\b(inc|corp|corporation|co|ltd|limited|plc|nv|sa|ag|holdings?|group|the)\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def main():
    ents = json.load(open(ENT, encoding='utf-8'))
    tick = json.loads(get('https://www.sec.gov/files/company_tickers.json').decode())
    by_ticker, by_name = {}, {}
    for r in tick.values():
        by_ticker[r['ticker'].upper()] = r
        by_name.setdefault(norm(r['title']), r)
    hit, miss = {}, []
    for e in ents:
        r = None
        # 익명 상대는 이름이 「ASML 최대 고객」 꼴이라 한글을 걷어내면 남의 이름이 된다
        if e.get('anon'):
            miss.append((e['id'], e.get('name')))
            continue
        t = (e.get('ticker') or '').upper()
        if t and t in by_ticker:
            r = by_ticker[t]
        if r is None:
            alias = ALIAS.get(e['id'])
            key = norm(alias) if alias else norm(e.get('legal_name') or e.get('name'))
            if len(key) >= 4:
                r = by_name.get(key)
        if r is None:
            miss.append((e['id'], e.get('name')))
            continue
        hit[e['id']] = {'cik': r['cik_str'], 'name': r['title']}
    print('이름을 이은 곳 %d · 못 이은 곳 %d' % (len(hit), len(miss)))
    out = {}
    for eid, v in sorted(hit.items()):
        sub = json.loads(get('https://data.sec.gov/submissions/CIK%010d.json' % v['cik']).decode())
        out[eid] = {'cik': '%010d' % v['cik'], 'entity_name': sub.get('name'),
                    'sic': sub.get('sic'), 'sic_desc': sub.get('sicDescription'),
                    'forms': sorted({f for f in (sub.get('filings', {}).get('recent', {})
                                                 .get('form') or []) if f in
                                     ('10-K', '20-F', '40-F', 'S-1')})}
        # 업종 코드가 안 붙은 곳은 SEC 가 업종을 등록해 두지 않은 것이다
        if not out[eid]['sic_desc']:
            del out[eid]
            print('  %-26s 업종 없음' % eid)
            time.sleep(0.15)
            continue
        print('  %-26s %-6s %s' % (eid, out[eid]['sic'], out[eid]['sic_desc']))
        time.sleep(0.15)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    print('적었다 —', OUT)
    if '--miss' in sys.argv:
        for m in miss: print('   못 이음', m[0], m[1])

main()
