# -*- coding: utf-8 -*-
"""회계사 대시보드에 선 회사들의 지금 시세를 받아 insights/prices.json에 적는다.

왜 따로 두나 — 대시보드의 괴리 값은 필자가 낸 것이고 그가 견준 주가도 그 글의 시점이다.
「지금 주가로는 얼마인가」는 우리가 새로 계산하는 값이라 원천도 시점도 갈라 두어야 한다.
그래서 시세는 이 파일이 받아 적고, 화면에서는 필자 값과 다른 자리에 다른 이름으로 선다.

쓰는 법
    PYTHONIOENCODING=utf-8 python scratchpad/fetch_prices.py            # 시세만 갱신
    PYTHONIOENCODING=utf-8 python scratchpad/fetch_prices.py --resolve  # 코드부터 찾아 채운다

종목코드는 insights/tickers.json에 둔다. 원문에 코드가 없는 회사가 많은데, 코드는 값이
아니라 이름표라 원문 밖에서 채워도 「원문에 있는 값만」 규칙에 걸리지 않는다. 대신 이름이
맞는지 받아 온 이름과 대조해 적어 둔다.
"""
import json, time, sys, io, os, re, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from clip_naver import CDP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TICKERS = os.path.join(ROOT, 'insights', 'tickers.json')
PRICES = os.path.join(ROOT, 'insights', 'prices.json')

# 섹션 id → 찾을 이름. 코드가 원문에 있던 회사는 코드를 바로 적었다.
WANT = [
    ('sec-samsung', '삼성전자', '005930'),
    ('sec-hynix', 'SK하이닉스', '000660'),
    ('sec-cosmax', '코스맥스', '192820'),
    ('sec-silicon2', '실리콘투', '257720'),
    ('sec-orion', '오리온', '271560'),
    ('sec-hugel', '휴젤', '145020'),
    ('sec-jusung', '주성엔지니어링', '036930'),
    ('sec-sds', '삼성에스디에스', '018260'),
    ('sec-lselectric', 'LS ELECTRIC', '010120'),
    ('sec-apr', '에이피알', '278470'),
    ('sec-shinhan', '신한지주', '055550'),
    ('sec-hdel', 'HD현대일렉트릭', '267260'),
    ('sec-semco', '삼성전기', '009150'),
    ('sec-kolmar', '한국콜마', '161890'),
    ('sec-hdhi', 'HD현대중공업', '329180'),
    ('sec-hws', '한화시스템', '272210'),
    ('sec-isu', '이수페타시스', '007660'),
    ('sec-naver', 'NAVER', '035420'),
    ('sec-jeju', '제주반도체', '080220'),
    ('sec-ecopro', '에코프로비엠', '247540'),
    ('sec-wontech', '원텍', '336570'),
    ('sec-hyosung', '효성중공업', '298040'),
    ('sec-lge', 'LG전자', '066570'),
    ('sec-skt', 'SK텔레콤', '017670'),
    ('sec-kia', '기아', '000270'),
    ('sec-kzinc', '고려아연', '010130'),
    # 아래는 원문에 코드가 없어 이름으로 찾는다
    ('sec-lgcns', 'LG CNS', None),
    ('sec-scnt', '삼성물산', None),
    ('sec-hmc', '현대차', None),
    ('sec-mobis', '현대모비스', None),
    ('sec-bobcat', '두산밥캣', None),
    ('sec-sdi', '삼성SDI', None),
    ('sec-sbl', '삼성바이오로직스', None),
    ('sec-lnf', '엘앤에프', None),
    ('sec-hanmi', '한미반도체', None),
]
# 국내 시세만 받는다. 해외 상장사는 이 경로로 안 받아 값을 비운다.
# 검색 주소가 죽어 코드를 후보로 넣고 확인한다. 값이 아니라 이름표라 원문 밖에서 채워도
# 되지만, 잘못 넣으면 남의 회사 시세를 붙이게 되므로 돌아온 이름과 대조해 통과한 것만 쓴다.
CANDIDATE = {
    'sec-lgcns': '064400', 'sec-scnt': '028260', 'sec-hmc': '005380',
    'sec-mobis': '012330', 'sec-bobcat': '241560', 'sec-sdi': '006400',
    'sec-sbl': '207940', 'sec-lnf': '066970', 'sec-hanmi': '042700',
}
# 네이버 표기가 우리 이름과 다른 곳. 대조는 이 표기로 한다 — 이름이 안 맞으면 남의 회사
# 시세를 붙이게 되므로 대조 자체를 없애지 않고 별칭만 더한다.
ALIAS = {'sec-lgcns': 'LG씨엔에스'}
SKIP = {'sec-sandisk': '샌디스크(미국 상장)', 'sec-googl': '알파벳(미국 상장)'}

QUOTE_JS = r"""(function(){
  function t(sel){ var e=document.querySelector(sel); return e ? (e.innerText||'').replace(/\s+/g,' ').trim() : null; }
  // 코스피 화면은 .no_today .blind에 값이 통째로 있는데 코스닥 화면은 그 자리가 비고
  // 숫자가 글자 단위로 쪼개져 있다. 그래서 .no_today 글자에서 숫자만 훑어 쓴다.
  return JSON.stringify({name: t('.wrap_company h2'), code: t('.description .code'),
                         price: t('.no_today'), basis: t('.description .date')});
})()"""

SEARCH_JS = r"""(function(){
  var a=document.querySelector('.tbl_search tbody tr td.tit a');
  if(!a) return 'null';
  var m=(a.getAttribute('href')||'').match(/code=(\d{6})/);
  return JSON.stringify({code: m?m[1]:null, name:(a.innerText||'').trim()});
})()"""


def _num(s):
    return int(re.sub(r'[^\d]', '', s)) if s else None


def main():
    resolve = '--resolve' in sys.argv
    req = urllib.request.Request('http://127.0.0.1:9222/json/new?about:blank', method='PUT')
    c = CDP(json.loads(urllib.request.urlopen(req).read()))

    codes = {}
    if os.path.isfile(TICKERS):
        codes = json.load(io.open(TICKERS, encoding='utf-8'))

    for sid, name, code in WANT:
        if code:
            codes.setdefault(sid, {'code': code, 'name': name})
            continue
        if sid in codes and not resolve:
            continue
        cand = CANDIDATE.get(sid)
        if not cand:
            print('후보 코드 없음: %s (%s)' % (name, sid))
            continue
        c.call('Page.navigate', {'url':
               'https://finance.naver.com/item/main.naver?code=' + cand})
        time.sleep(2.2)
        q = json.loads(c.js(QUOTE_JS) or '{}')
        got = (q.get('name') or '').replace(' ', '')
        want = ALIAS.get(sid, name).replace(' ', '')
        if got.replace('주식회사', '') != want:
            print('이름이 안 맞아 버린다: %s 후보 %s -> 「%s」' % (name, cand, q.get('name')))
            continue
        codes[sid] = {'code': cand, 'name': q.get('name'), 'checked_by': '이름 대조'}
        print('코드 확인: %-16s %s' % (q.get('name'), cand))

    io.open(TICKERS, 'w', encoding='utf-8').write(
        json.dumps(codes, ensure_ascii=False, indent=1, sort_keys=True))

    out, asof = {}, None
    for sid, meta in sorted(codes.items()):
        c.call('Page.navigate', {'url':
               'https://finance.naver.com/item/main.naver?code=' + meta['code']})
        time.sleep(2.0)
        q = json.loads(c.js(QUOTE_JS) or '{}')
        price = _num(q.get('price'))
        if not price:
            print('시세 못 읽음: %s %s' % (sid, meta['code']))
            continue
        asof = asof or q.get('basis')
        out[sid] = {'code': meta['code'], 'name': q.get('name'), 'price': price,
                    'basis': q.get('basis')}
        print('%-14s %-8s %10s  %s' % (q.get('name'), meta['code'],
                                       format(price, ','), q.get('basis')))
    c.ws.close()

    io.open(PRICES, 'w', encoding='utf-8').write(json.dumps(
        {'as_of': asof, 'source': '네이버 금융', 'skipped': SKIP, 'items': out},
        ensure_ascii=False, indent=1, sort_keys=True))
    print('\n%d곳 -> %s' % (len(out), PRICES))


if __name__ == '__main__':
    import urllib.parse
    main()
