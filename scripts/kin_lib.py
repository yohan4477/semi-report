# -*- coding: utf-8 -*-
"""닮은 카드 찾기 — 「이것과 관련된 게 또 뭐가 있나」에 후보군과 분모를 준다.

지금 카드끼리 잇는 길은 attach_related 하나뿐이고 그건 전부 손이다. 연결할 제목을
사람이 적어야 하니 368장 중 19장만 related 를 갖고, 그나마 대부분 두 장이다.
그래서 「관련 셋만 나온다」가 된다 — 적어 둔 만큼만 나오기 때문이다.

여기서는 카드 본문끼리 닮은 정도를 재서 후보를 낸다. 손으로 적은 것을 덮어쓰지
않는다. related 에 이미 있는지를 칸으로 보여줄 뿐이다 — 「이 글 다음에 저 글을
읽어야 한다」는 순서는 사람이 아는 것이고 점수가 알 수 있는 것이 아니다.

닮음은 글자 n-gram 으로 잰다. 한국어는 조사가 붙어서 「분담금이」와 「분담금은」이
공백 토큰으로는 서로 다른 말이 된다. 두세 글자로 쪼개면 겹친다. 형태소 분석기를
안 쓰는 이유는 의존성 하나가 이 저장소의 결정성을 깨기 때문이다.

읽기 전용이다. 아무것도 쓰지 않는다.

성능은 한 곳에서만 쟀고 그 사실이 중요하다. related 를 가진 카드 19장이 전부 회계사
대시보드에 있어서 정답 40 짝도 전부 거기 것이다. 다른 대시보드에는 비교할 정답이 없다.
그러니 아래 숫자는 이 도구의 성능이 아니라 「회계사에서의 성능」이다.

  상위 12 적중 35% · 순위 중앙값 350장 중 21위 · 아예 못 찾는 짝 0

그리고 회계사는 이 방식에 가장 불리한 곳이다. 카드 120장이 전부 밸류에이션 어휘를
쓰는 탓에 카드끼리 평균 닮음이 0.042 로 고르게 낮다. 어휘로는 아무것도 안 갈린다.
실제로 사람이 이은 짝은 「실적이 좋은데 왜 주가가 안 따라오나」 같은 물음으로 묶였는데
점수가 고른 것은 「같은 회사의 밸류에이션」이었다. 사람은 논리로 잇고 점수는 화제로 잇는다.

그래서 이 도구는 순위가 아니라 분모로 쓴다 — 「후보 열둘인데 둘만 적혀 있다」가 값이고,
상위 몇 장이 사람 판단을 대신하지는 못한다.

조각을 idf 높은 것만 남겨 깎아 보았고 더 나빠졌다. K=400 에서 25%, 150 에서 20%,
80 에서 12% 로 떨어지고 못 찾는 짝이 0 → 14 → 34 로 는다. K=80 의 순위 중앙값이 3 위로
좋아 보이는데, 40 짝 중 34 짝을 못 찾아 살아남은 여섯으로만 낸 값이라 읽으면 안 된다.
깎으면 신호가 모이는 게 아니라 없어진다. 다시 시도하지 않는다.
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cards as cd  # noqa: E402

# 한글·라틴·숫자만 남긴다. 문장부호는 조각 경계일 뿐 내용이 아니다
TOKEN = re.compile(r'[0-9a-z가-힣]+')
SIZES = (2, 3)


def grams(text, sizes=SIZES):
    """토큰 안에서만 n-gram 을 뽑는다.

    낱말 경계를 넘으면 「조합이 갈라졌다」에서 「이갈」 같은 조각이 생겨
    아무 글이나 닮아 보이게 된다. 한 글자 토큰은 버린다 — 어디에나 있다.
    """
    out = set()
    for tok in TOKEN.findall(text.lower()):
        if len(tok) < 2:
            continue
        if len(tok) < min(sizes):
            out.add(tok)
            continue
        for n in sizes:
            for i in range(len(tok) - n + 1):
                out.add(tok[i:i + n])
    return out


def idf(profiles):
    """조각 → log(N/df). 모든 카드에 있는 조각은 0 이 되어 닮음에 기여하지 않는다."""
    n = len(profiles)
    df = {}
    for gs in profiles.values():
        for g in gs:
            df[g] = df.get(g, 0) + 1
    return {g: math.log(n / d) for g, d in df.items()}


def similarity(a, b, weight):
    """idf 를 실은 코사인. 두 카드가 드문 조각을 나눠 가질수록 크다."""
    if not a or not b:
        return 0.0
    na = math.sqrt(sum(weight.get(g, 0.0) ** 2 for g in a))
    nb = math.sqrt(sum(weight.get(g, 0.0) ** 2 for g in b))
    if not na or not nb:
        return 0.0
    dot = sum(weight.get(g, 0.0) ** 2 for g in (a & b))
    return dot / (na * nb)


def profiles_of(cards):
    return {cd.card_id(c): grams(cd.card_text(c)) for c in cards}


def related_titles(card):
    """related 는 (제목, 앵커) 목록이다. 제목만 뽑는다."""
    out = []
    for r in card.get('related') or ():
        out.append(r[0] if isinstance(r, (list, tuple)) else r)
    return out


def neighbors(cards, title, top=12):
    """제목 하나에 닮은 카드를 점수순으로 낸다.

    declared_missing 이 있는 쪽도 값어치가 있다 — 사람이 이어 뒀는데 점수가 못 찾은
    것이라, 글끼리의 관계가 낱말이 아니라 논리에 있다는 뜻이다.
    """
    by_title = {cd.card_id(c): c for c in cards}
    src = by_title.get(title)
    empty = {'title': title, 'section': None, 'shown': 0,
             'declared': 0, 'declared_in_top': 0, 'declared_missing': [],
             'rows': []}
    if src is None:
        return empty

    prof = profiles_of(cards)
    weight = idf(prof)
    mine = prof.get(title, set())
    declared = related_titles(src)
    kin = set(declared)
    sec = cd.section_id(src.get('section'))

    rows = []
    for t, gs in prof.items():
        if t == title:
            continue
        score = similarity(mine, gs, weight)
        if score <= 0:
            continue
        rows.append({
            'title': t,
            'score': round(score, 3),
            'same_section': cd.section_id(by_title[t].get('section')) == sec,
            'in_related': t in kin,
        })
    rows.sort(key=lambda r: (-r['score'], r['title']))
    rows = rows[:top]

    shown_titles = {r['title'] for r in rows}
    return {
        'title': title,
        'section': sec,
        'shown': len(rows),
        'declared': len(declared),
        'declared_in_top': sum(1 for t in declared if t in shown_titles),
        'declared_missing': sorted(t for t in declared if t not in shown_titles),
        'rows': rows,
    }
