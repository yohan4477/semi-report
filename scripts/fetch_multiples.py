# -*- coding: utf-8 -*-
"""상대가치 축 재료. 비교 회사의 주가와 애널리스트 주당순이익 추정치를 받는다.

왜 따로 두나: `fetch_facts.py` 는 SEC 제출서류를 통째로 받아 현금흐름 할인법에 쓰는
재료를 만든다. 비교 회사는 그 깊이가 필요 없다 — 주가와 선행 주당순이익 둘이면
배수가 나온다. 여섯 회사에 쓰는 파이프라인에 비교 회사 열몇을 얹으면 SEC 호출만
늘고 쓰이지 않는다.

왜 필요한가: 회계사 판의 필자는 리노공업 편(2026-03-08)에서 현금흐름 할인법과
주가수익비율 상대가치법을 같은 무게로 냈다. 그리고 **비교 대상을 어떻게 고르느냐가
결론을 가른다**는 것을 전면에 놓았다. 소부장 평균으로 재면 현재가가 30% 비싸고,
직접 경쟁사 하나로 좁히면 거의 같아진다. 우리 장에는 그 축이 없었다.

선행 주가수익비율은 다음 회계연도 추정치로 낸다. 회사마다 회계연도 끝이 달라
같은 달을 재는 것이 아니므로, 결과에 각 회사의 회계연도 종료일을 함께 적는다.
"""
import io
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_facts as ff

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'insights', 'valuation', '_multiples.json')

# 비교 대상. 엔비디아와 같은 판에서 값이 매겨지는 회사들이다.
#   AMD    가속기에서 직접 겨룬다
#   AVGO   맞춤형 가속기와 네트워킹. 하이퍼스케일러 자체 칩의 설계 파트너다
#   TSM    엔비디아 칩을 찍는 곳. 같은 수요를 다른 층에서 받는다
#   MU     고대역폭메모리. 엔비디아 원가에 들어간다
#   INTC   같은 이름의 시장에 있으나 자리가 다르다. 아래쪽 대조군이다
PEERS = {
    'NVDA': '엔비디아',
    'AMD': 'AMD',
    'AVGO': '브로드컴',
    'TSM': 'TSMC',
    'MU': '마이크론',
    'INTC': '인텔',
}


def one(ticker):
    px = ff.price(ticker, rng='1y')
    con = ff.consensus(ticker)
    row = dict(ticker=ticker, price=px['price'], as_of=px['market_time'])
    if not con:
        return row
    got = {p['period']: p for p in con['periods']}
    for key, per in (('this_year', '0y'), ('next_year', '+1y')):
        q = got.get(per)
        if not q or q.get('eps') is None:
            continue
        row[key] = dict(end=q['end'], eps=q['eps'], analysts=q['analysts'],
                        revenue=q['revenue'], growth=q.get('growth'))
        # 주가를 추정 주당순이익으로 나눈 값. 음수 이익이면 배수가 뜻을 잃으므로 비운다.
        if q['eps'] > 0:
            row[key]['fwd_per'] = px['price'] / q['eps']
    return row


def build():
    rows = {}
    for t in PEERS:
        try:
            rows[t] = one(t)
        except Exception as e:                      # 한 종목이 막혀도 나머지는 낸다
            rows[t] = dict(ticker=t, error='%s: %s' % (type(e).__name__, e))
    doc = dict(fetched_at=datetime.now(timezone.utc).isoformat(),
               names=PEERS, rows=rows,
               source='query1.finance.yahoo.com chart + quoteSummary earningsTrend',
               note='선행 주가수익비율은 다음 회계연도 추정 주당순이익 기준이다. '
                    '회사마다 회계연도 끝이 달라 같은 달을 재지 않는다')
    io.open(OUT, 'w', encoding='utf-8').write(
        json.dumps(doc, ensure_ascii=False, indent=1))
    return doc


if __name__ == '__main__':
    d = build()
    print('%-6s %-8s %9s %9s %9s  %s' % ('티커', '이름', '주가', '차기EPS', '선행PER', '회계연도'))
    for t, name in PEERS.items():
        r = d['rows'].get(t, {})
        ny = r.get('next_year') or {}
        print('%-6s %-8s %9.2f %9s %9s  %s'
              % (t, name, r.get('price', 0),
                 ('%.2f' % ny['eps']) if ny.get('eps') is not None else '—',
                 ('%.1f배' % ny['fwd_per']) if ny.get('fwd_per') else '—',
                 ny.get('end', '—')))
    print('->', OUT)
