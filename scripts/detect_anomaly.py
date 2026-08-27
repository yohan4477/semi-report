# -*- coding: utf-8 -*-
"""공시에서 「숨은 항목」 후보를 기계로 찾는다.

**왜 만드나.** 2026-08-27까지 우리가 찾은 회계 항목은 전부 SemiAnalysis 가 먼저 짚은
자리였다. 원문이 가리킨 데만 본 것이라 원문이 안 본 것은 우리도 못 본다. 방향을
뒤집는다 — **공시에서 먼저 찾고, 그다음 원문이 그걸 봤는지 본다.**

**채점이 되는 설계다.** 코퍼스 훑기가 낸 관찰 열일곱 건 중 우리 여섯 회사에 닿는
넷이 정답지다. 이 탐지기가 그 넷을 스스로 집어내면 그 밖에 집은 것도 믿을 만하고,
못 집으면 탐지기가 약한 것이다. `--benchmark` 로 그 채점을 돌린다.

**문서를 안 읽고 XBRL 만으로 잡는 신호 셋.**

    신규   없던 태그가 최근에 생겼다. 회사가 없던 줄을 새로 만들면 그게 사건이다
    단절   쓰던 태그가 끊겼다. 표시나 처리가 바뀐 신호이고, 우리 파이프라인이
           조용히 옛 값을 물고 있을 수 있다
    급변   같은 태그가 전기 대비 몇 배로 뛰었다

셋 다 **매출 대비 크기**로 거른다. 안 그러면 태그 육백 개에서 잡동사니가 쏟아진다.

찾은 것은 후보이지 결론이 아니다. 무엇을 뜻하는지는 주석을 읽어야 알고, 그건 사람
몫이다. 이 파일은 **어디를 읽어야 하는지**까지만 낸다.

    PYTHONIOENCODING=utf-8 python scripts/detect_anomaly.py
    PYTHONIOENCODING=utf-8 python scripts/detect_anomaly.py --benchmark
"""
import io
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_facts as ff                                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = 1e9

# 매출 대비 이 비율을 넘는 것만 낸다. 낮추면 잡동사니가, 높이면 놓친 것이 늘어난다.
MATERIAL = 0.01
# 「최근」의 길이. 분기 여섯이면 회계연도가 다른 회사도 두 해가 덮인다.
NEW_DAYS = 560
# 마지막 관측이 이보다 오래됐으면 끊긴 것으로 본다. 연간만 내는 항목이 있어 넉넉히 준다.
DROP_DAYS = 400
# 급변으로 볼 배수.
JUMP = 5.0
# 「지금 이야기」의 길이. 이보다 오래된 뜀·단절은 안 낸다 — 십수 년 전 것이 크기 순으로
# 위에 올라와 최근 것을 덮는다.
RECENT_DAYS = 760

# 정답지. 코퍼스 훑기(2026-08-27)가 낸 관찰 중 우리 여섯 회사의 연결 입력에 닿는 넷과,
# 우리가 파이프라인을 고치며 겪은 태그 사고 둘이다. 탐지기가 이것들을 집어내야 한다.
BENCH = {
    'NVDA': [('GuaranteeObligationsMaximumExposure', '백스톱이 대차대조표에 나타났다'),
             ('MarketableSecuritiesCurrent', '시장성증권 태그가 끊겨 잔액이 한 해 낡았다')],
    'GOOGL': [('RevenueFromContractWithCustomerExcludingAssessedTax',
               '매출 태그를 갈아탔다'),
              ('LongTermPurchaseCommitmentAmount', '구매약정을 새로 내기 시작했다')],
}


def _pts(facts, tag):
    u = facts['facts']['us-gaap'].get(tag, {}).get('units', {}).get('USD', [])
    out = []
    for x in u:
        if not x.get('end'):
            continue
        out.append(dict(end=x['end'], start=x.get('start'), val=x['val'],
                        form=x.get('form'), filed=x.get('filed')))
    out.sort(key=lambda r: (r['end'], r['val']))
    return out


def _scale(facts):
    """크기를 재는 잣대. 가장 최근 연간 매출을 쓴다.

    **태그 순서로 고르지 않는다.** 후보를 순서대로 보다 처음 데이터가 있는 것에서
    멈추면, 그 태그가 옛날에 끊긴 회사는 몇 해 전 매출을 잣대로 쓰게 된다 — 엔비디아가
    2022-01-30 뒤로 첫 태그를 안 써서 269억 달러(실제 3,030억)로 나왔다. 후보를 전부
    훑어 **가장 최근 것**을 쓴다.
    """
    best = None
    for tag in ('RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenues'):
        for x in _pts(facts, tag):
            if not x['start']:
                continue
            d = (datetime.strptime(x['end'], '%Y-%m-%d')
                 - datetime.strptime(x['start'], '%Y-%m-%d')).days
            if 350 <= d <= 380 and (best is None or x['end'] > best['end']):
                best = x
    return best['val'] if best else None


def scan(ticker):
    facts = json.loads(ff.get('https://data.sec.gov/api/xbrl/companyfacts/CIK%s.json'
                              % ff.CIKS[ticker]))
    rev = _scale(facts)
    if not rev:
        return dict(ticker=ticker, error='연간 매출을 못 찾아 크기를 못 잰다')
    tags = facts['facts']['us-gaap']
    # 기준일은 그 회사가 낸 가장 최근 관측이다. 오늘 날짜를 쓰면 회계연도가 다른 회사가
    # 실제보다 뒤처져 보인다.
    last_all = max((p['end'] for t in tags for p in _pts(facts, t)), default=None)
    base = datetime.strptime(last_all, '%Y-%m-%d')
    hits = []
    for tag in tags:
        pts = _pts(facts, tag)
        if not pts:
            continue
        first, last = pts[0], pts[-1]
        size = abs(last['val']) / rev
        if size < MATERIAL:
            continue
        age_first = (base - datetime.strptime(first['end'], '%Y-%m-%d')).days
        age_last = (base - datetime.strptime(last['end'], '%Y-%m-%d')).days
        if age_first <= NEW_DAYS:
            hits.append(dict(kind='신규', tag=tag, val=last['val'], size=size,
                             end=last['end'], first=first['end'], n=len(pts),
                             why='%s 에 처음 나왔다' % first['end']))
        # 단절은 **그 태그 자신의 보고 주기**로 잰다. 400일 고정으로 두면 분기마다 내던
        # 항목이 두세 분기 비어도 안 걸린다 — 엔비디아 시장성증권이 그렇게 새어 나갔고,
        # 그때 순현금이 한 해 낡은 값으로 계산됐다.
        gaps = [(datetime.strptime(b['end'], '%Y-%m-%d')
                 - datetime.strptime(a['end'], '%Y-%m-%d')).days
                for a, b in zip(pts, pts[1:])
                if b['end'] != a['end']]
        gaps = [g for g in gaps if g > 0]
        cadence = sorted(gaps)[len(gaps) // 2] if gaps else None
        # 주기의 두 배를 넘게 비면 끊긴 것으로 본다. 주기를 모르면 옛 기준을 쓴다.
        drop_at = max(int(cadence * 2.2), 150) if cadence else DROP_DAYS
        if len(pts) >= 4 and drop_at <= age_last <= RECENT_DAYS + DROP_DAYS:
            hits.append(dict(kind='단절', tag=tag, val=last['val'],
                             size=abs(last['val']) / rev, end=last['end'],
                             first=first['end'], n=len(pts),
                             why='%s 뒤로 안 나온다(%d일 · 이 태그는 보통 %s일마다 냈다)'
                                 % (last['end'], age_last,
                                    cadence if cadence else '?')))
        # 급변은 **기간 길이가 같은 것끼리만** 견준다. 시점 값이냐 기간 값이냐로만 가르면
        # 모자란다 — 10-Q 는 그 분기(약 90일)와 회계연도 누적(180·270일)을 같은 날짜로
        # 함께 내므로, 둘이 짝지어지면 「같은 날 26억에서 409억으로 15배」가 나온다.
        # 아마존 현금흐름 급변이 전부 이 오탐이었다.
        def _bucket(x):
            if not x['start']:
                return 'I'
            d = (datetime.strptime(x['end'], '%Y-%m-%d')
                 - datetime.strptime(x['start'], '%Y-%m-%d')).days
            return 'Q' if d <= 100 else ('H' if d <= 200 else
                                         ('3Q' if d <= 290 else 'Y'))
        for kind in ('I', 'Q', 'H', '3Q', 'Y'):
            seq = [p for p in pts if _bucket(p) == kind]
            for a, b in zip(seq, seq[1:]):
                if not a['val'] or abs(a['val']) < rev * MATERIAL:
                    continue
                # 최근 창 밖의 뜀은 지금 읽을 이야기가 아니다. 2011년 옵션 내재가치가
                # 뛴 것이 상위에 올라오던 자리다.
                if (base - datetime.strptime(b['end'], '%Y-%m-%d')).days > RECENT_DAYS:
                    continue
                r = b['val'] / a['val']
                if r >= JUMP and abs(b['val']) / rev >= MATERIAL:
                    hits.append(dict(kind='급변', tag=tag, val=b['val'],
                                     size=abs(b['val']) / rev, end=b['end'],
                                     first=a['end'], n=len(pts),
                                     why='%s %.0f억에서 %s %.0f억으로 %.1f배'
                                         % (a['end'], a['val'] / 1e8,
                                            b['end'], b['val'] / 1e8, r)))
    # 같은 태그가 여러 신호에 걸리면 큰 쪽부터 본다
    hits.sort(key=lambda h: -h['size'])
    return dict(ticker=ticker, revenue=rev, hits=hits, as_of=last_all)


def benchmark(results):
    """정답지를 스스로 집었나. 탐지기를 믿을지 정하는 자리다."""
    print('\n== 채점 — 원문이 짚은 것을 탐지기가 집었나')
    ok = tot = 0
    for tk, want in BENCH.items():
        got = {h['tag'] for h in (results.get(tk) or {}).get('hits', [])}
        for tag, what in want:
            tot += 1
            hit = tag in got
            ok += hit
            print('  %s %-8s %-58s %s' % ('O' if hit else 'X', tk, tag[:58], what))
    print('  집은 것 %d/%d' % (ok, tot))
    return ok, tot


def write(res):
    L = ['# 공시에서 찾은 숨은 항목 후보', '',
         '자동 생성이다. `python scripts/detect_anomaly.py` 가 다시 쓴다.', '',
         '- 매출 대비 %.0f%% 넘는 것만 낸다' % (MATERIAL * 100),
         '- 신규: 최근 %d일 안에 처음 나온 태그' % NEW_DAYS,
         '- 단절: %d일 넘게 안 나오는 태그' % DROP_DAYS,
         '- 급변: 같은 성격끼리 %.0f배 넘게 뛴 것' % JUMP, '',
         '**후보이지 결론이 아니다.** 무엇을 뜻하는지는 주석을 읽어야 안다.', '']
    for tk, r in res.items():
        if r.get('error'):
            L += ['## %s' % tk, '', '- %s' % r['error'], '']
            continue
        L += ['## %s (기준 %s · 연간 매출 %.0f억 달러)'
              % (tk, r['as_of'], r['revenue'] / 1e8), '']
        if not r['hits']:
            L += ['- 걸린 것 없음', '']
            continue
        for h in r['hits']:
            L.append('- **%s** `%s` %.0f억 달러 (매출의 %.1f%%) — %s'
                     % (h['kind'], h['tag'], h['val'] / 1e8, h['size'] * 100, h['why']))
        L.append('')
    p = os.path.join(ROOT, 'scratchpad', 'anomaly.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p


if __name__ == '__main__':
    tickers = [a.upper() for a in sys.argv[1:] if not a.startswith('--')]
    res = {}
    for t in (tickers or list(ff.CIKS)):
        res[t] = scan(t)
        r = res[t]
        print('%-6s %s' % (t, r.get('error') or '후보 %d건' % len(r['hits'])))
    print('->', write(res))
    if '--benchmark' in sys.argv:
        benchmark(res)
