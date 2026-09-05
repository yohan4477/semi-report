# -*- coding: utf-8 -*-
"""FRED 시계열을 받아 data/fred/ 에 둔다. 도해에 바깥 데이터를 쓰는 유일한 통로다.

    PYTHONIOENCODING=utf-8 python scripts/fetch_fred.py
    PYTHONIOENCODING=utf-8 python scripts/fetch_fred.py DGS10 DGS30

왜 있나 — 이 저장소는 원문에 없는 값을 안 그린다(insight-figure 규칙 1). 그런데 금리는
값이 날마다 움직이는 것이 내용이라, 원문이 짚은 몇 점만으로는 움직임이 안 보인다. 그래서
FRED 를 **정식 재료로 등록해** 들여온다. 워치 장이 부동산 데이터를 어댑터로 들여오는 것과
같은 자리다.

지키는 것 넷
    출처를 남긴다      파일 머리에 시리즈 id · 받은 날 · 내려받은 주소를 적는다
    가공하지 않는다    받은 값을 그대로 둔다. 채우기·보간·반올림 없음
    선과 점을 가른다   도해에서 FRED 는 선, 원문이 적은 값은 점이다. 캡션이 그렇게 밝힌다
    갈리면 드러낸다    원문 값이 시리즈와 다르면 맞추지 말고 둘 다 보인다

메르가 독자에게 직접 FRED 를 열어 보라고 짚은 시리즈가 T10Y2Y 다(메르-역전).
"""
import io
import os
import sys
import time

try:
    from urllib.request import urlopen
except ImportError:                                    # py2 는 안 쓴다
    urlopen = None

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'fred')
URL = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s'

# 이 저장소가 쓰는 시리즈. 새로 늘릴 때는 무엇에 쓰는지 한 줄로 적는다
SERIES = {
    'DGS10': '미국 국채 10년물 · 일별',
    'DGS30': '미국 국채 30년물 · 일별',
    'T10Y2Y': '10년물 빼기 2년물 · 장단기 금리차. 메르가 독자에게 직접 열어 보라고 짚은 시리즈',
    'DFF': '연방기금 실효금리 · 일별',
}


def fetch(sid):
    raw = urlopen(URL % sid, timeout=40).read().decode('utf-8')
    rows = [r for r in raw.strip().split('\n') if r.strip()]
    head, body = rows[0], rows[1:]
    got = time.strftime('%Y-%m-%d')
    last = body[-1].split(',')[0] if body else '?'
    txt = ('# series: %s\n# what: %s\n# fetched: %s\n# source: %s\n# rows: %d · last: %s\n%s\n'
           % (sid, SERIES.get(sid, ''), got, URL % sid, len(body), last, '\n'.join([head] + body)))
    path = os.path.join(OUT, sid + '.csv')
    io.open(path, 'w', encoding='utf-8', newline='\n').write(txt)
    return len(body), last


def load(sid):
    """받아 둔 시리즈를 {날짜: 값} 으로. 값이 없는 날(. 로 표시)은 건너뛴다."""
    path = os.path.join(OUT, sid + '.csv')
    if not os.path.exists(path):
        return {}
    out = {}
    for line in io.open(path, encoding='utf-8'):
        if line.startswith('#') or line.startswith('observation_date'):
            continue
        p = line.strip().split(',')
        if len(p) == 2 and p[1] not in ('.', ''):
            try:
                out[p[0]] = float(p[1])
            except ValueError:
                pass
    return out


def main():
    if urlopen is None:
        print('urllib 을 못 쓴다')
        return 1
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    want = sys.argv[1:] or sorted(SERIES)
    for sid in want:
        try:
            n, last = fetch(sid)
            print('%-8s %5d행 · 마지막 %s · %s' % (sid, n, last, SERIES.get(sid, '')))
        except Exception as e:                          # 네트워크가 막힌 자리에서도 죽지 않는다
            print('%-8s 못 받음 — %s' % (sid, e))
    return 0


if __name__ == '__main__':
    sys.exit(main())
