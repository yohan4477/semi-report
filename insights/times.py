# -*- coding: utf-8 -*-
"""줄 하나가 가리키는 때. 파일도 코퍼스도 모른다 — 문자열과 쓴 날만 받는다.

셋으로 푼다.
  명시  「1965년」          정규식으로 그대로 읽는다. 색인 줄 1,643개가 그렇다
  계산  「작년」「3년 전」    쓴 날에서 빼고 더한다. 판단이 필요 없다
  없음  아무 표지도 없으면 None 을 낸다. 상속은 여기서 안 한다 —
        조회할 때 쓴 날로 채우고, 그래야 「이건 상속이다」가 저절로 구분된다

한 줄에 연도가 둘 이상이면 t 는 가장 늦은 연도다. 색인 줄 1,643개 중 442개가
그렇다. 늦은 쪽을 잡는 이유는 시제가 낡음 판정을 가르기 때문이다 —
「2018년부터 2028년까지」를 회고로 두면 앞날 주장이 신선도 검사를 빠져나간다.
대신 최소 연도가 다르면 span 에 함께 적어 연표가 구간으로 그릴 수 있게 한다.

「지금·현재·최근·앞으로·향후」는 여기서 안 다룬다. 연도로 안 풀리기 때문이다.
그런 줄은 표지가 없는 줄과 똑같이 상속으로 떨어진다.
"""
import re

YEAR = re.compile(r'(?<![0-9])((?:19|20)\d{2})\s*년')
OFFSET = re.compile(r'(?<![0-9])(\d{1,2})\s*년\s*(전|뒤|후)')

# 긴 말을 먼저 걷어낸다 — 「작년」이 「재작년」 안에 들어 있다
LONG_WORDS = (('재작년', -2), ('내후년', 2))
WORDS = (('작년', -1), ('지난해', -1), ('올해', 0), ('금년', 0), ('내년', 1))

LOW = 1850          # 이보다 이르면 정규식이 헛것을 잡은 것이다
AHEAD = 50          # 쓴 날 연도 + 이만큼까지 앞날 주장으로 성립한다고 본다


def explicit(line):
    return sorted({int(y) for y in YEAR.findall(line)})


def computed(line, utter_year):
    out = set()
    rest = line
    for word, delta in LONG_WORDS:
        if word in rest:
            out.add(utter_year + delta)
            rest = rest.replace(word, ' ')
    for word, delta in WORDS:
        if word in rest:
            out.add(utter_year + delta)
    for n, direction in OFFSET.findall(line):
        n = int(n)
        out.add(utter_year - n if direction == '전' else utter_year + n)
    return sorted(out)


def tense_of(t, utter_year):
    if t < utter_year:
        return '회고'
    if t > utter_year:
        return '전망'
    return '현재'


def find(line, utter_date):
    if not utter_date or len(utter_date) < 4 or not utter_date[:4].isdigit():
        return None
    uy = int(utter_date[:4])
    years = explicit(line)
    how = '명시'
    if not years:
        years = computed(line, uy)
        how = '계산'
    years = [y for y in years if LOW <= y <= uy + AHEAD]
    if not years:
        return None
    t = max(years)
    out = {'t': '%d' % t, 'how': how, 'tense': tense_of(t, uy)}
    if min(years) != t:
        out['span'] = ['%d' % min(years), '%d' % t]
    return out
