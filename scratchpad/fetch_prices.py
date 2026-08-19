# -*- coding: utf-8 -*-
"""회계사 대시보드에 선 회사들의 지금 시세를 받아 insights/prices.json에 적는다.

왜 따로 두나 — 대시보드의 괴리 값은 필자가 낸 것이고 그가 견준 주가도 그 글의 시점이다.
「지금 주가로는 얼마인가」는 우리가 새로 계산하는 값이라 원천도 시점도 갈라 두어야 한다.
그래서 시세는 이 파일이 받아 적고, 화면에서는 필자 값과 다른 자리에 다른 이름으로 선다.

브라우저도 모델도 안 쓴다. 페이지가 서버에서 완성돼 오므로 HTTP로 받아 정규식으로 읽는다 —
그래야 GitHub Actions처럼 화면 없는 곳에서도 돈다.

    PYTHONIOENCODING=utf-8 python scratchpad/fetch_prices.py

종목코드는 insights/tickers.json에 있다. 코드는 값이 아니라 이름표라 원문 밖에서 채워도
「원문에 있는 값만」 규칙에 안 걸리지만, 잘못 넣으면 남의 회사 시세를 붙이게 되므로
받아 온 회사 이름과 대조해 안 맞으면 버린다.
"""
import io, json, os, re, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TICKERS = os.path.join(ROOT, 'insights', 'tickers.json')
PRICES = os.path.join(ROOT, 'insights', 'prices.json')
URL = 'https://finance.naver.com/item/main.naver?code=%s'
UA = {'User-Agent': 'Mozilla/5.0 (compatible; semi-report price sync)'}

# 국내 시세만 받는다. 해외 상장사는 이 경로로 안 받아 값을 비운다.
SKIP = {'sec-sandisk': '샌디스크(미국 상장)', 'sec-googl': '알파벳(미국 상장)'}
# 네이버 표기가 우리 이름과 다른 곳
ALIAS = {'sec-lgcns': 'LG씨엔에스'}


def _txt(m):
    return re.sub(r'<[^>]+>', ' ', m.group(1)).strip() if m else None


def quote(code):
    """한 종목의 이름·현재가·기준일시를 낸다."""
    body = urllib.request.urlopen(
        urllib.request.Request(URL % code, headers=UA), timeout=20
    ).read().decode('utf-8', 'replace')
    name = _txt(re.search(r'<div class="wrap_company">\s*<h2>\s*<a[^>]*>(.*?)</a>', body, re.S))
    # no_today 안에는 눈에 보이는 값과 화면낭독용 값이 같이 들어 있다. 화면낭독용은 장중
    # 한때의 낡은 숫자일 수 있어(삼성전자에서 260,000 대 실제 247,500) 앞의 것만 쓴다.
    blk = re.search(r'<p class="no_today">(.*?)</p>', body, re.S)
    price = None
    if blk:
        nums = re.findall(r'[\d,]{2,}', re.sub(r'<[^>]+>', ' ', blk.group(1)))
        if nums:
            price = int(nums[0].replace(',', ''))
    basis = re.sub(r'\s+', ' ',
                   _txt(re.search(r'<em class="date">(.*?)</em>', body, re.S)) or '')
    return name, price, basis


def main():
    codes = json.load(io.open(TICKERS, encoding='utf-8'))
    out, asof, bad = {}, None, []
    for sid, meta in sorted(codes.items()):
        try:
            name, price, basis = quote(meta['code'])
        except Exception as e:
            bad.append('%s %s: %s' % (sid, meta['code'], type(e).__name__))
            continue
        want = ALIAS.get(sid, meta.get('name') or '').replace(' ', '')
        got = (name or '').replace(' ', '')
        if want and got and got != want:
            bad.append('%s 이름이 안 맞는다: 「%s」 대 「%s」' % (sid, got, want))
            continue
        if not price:
            bad.append('%s %s: 값을 못 읽었다' % (sid, meta['code']))
            continue
        asof = asof or basis
        out[sid] = {'code': meta['code'], 'name': name, 'price': price, 'basis': basis}
        print('%-16s %-8s %12s  %s' % (name, meta['code'], format(price, ','), basis))
        time.sleep(0.35)          # 한 번에 몰아 치지 않는다

    for b in bad:
        print('건너뜀 —', b)

    old = {}
    if os.path.isfile(PRICES):
        old = json.load(io.open(PRICES, encoding='utf-8'))
    new = {'as_of': asof, 'source': '네이버 금융', 'skipped': SKIP, 'items': out}
    if old.get('items') == out and old.get('as_of') == asof:
        print('\n바뀐 값이 없다 — 파일을 안 고친다.')
        return 0
    io.open(PRICES, 'w', encoding='utf-8').write(
        json.dumps(new, ensure_ascii=False, indent=1, sort_keys=True))
    print('\n%d곳 -> %s' % (len(out), PRICES))
    return 0


if __name__ == '__main__':
    sys.exit(main())
