import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import kin_lib as kl  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _card(title, body, sec='a', related=None):
    c = {'title': title, 'oneliner': body, 'section': (sec, 'x', sec)}
    if related:
        c['related'] = [(t, 'card-%s' % t) for t in related]
    return c


# ── 조각 내기 ──────────────────────────────────────────────────

def test_grams_stay_inside_a_token():
    got = kl.grams('가나 다라')
    assert '가나' in got
    assert '다라' in got
    assert '나다' not in got          # 낱말 경계를 넘으면 안 된다


def test_grams_give_both_two_and_three():
    got = kl.grams('가나다')
    assert '가나' in got and '나다' in got and '가나다' in got


def test_grams_keep_short_token_whole():
    assert '가나' in kl.grams('가나')


def test_grams_drop_one_letter_token():
    assert kl.grams('가') == set()


def test_grams_ignore_punctuation():
    assert kl.grams('가나, 가나!') == kl.grams('가나 가나')


# ── 가중치 ────────────────────────────────────────────────────

def test_idf_weighs_rare_gram_above_common_one():
    prof = {'a': {'흔함', '드묾'}, 'b': {'흔함'}, 'c': {'흔함'}}
    w = kl.idf(prof)
    assert w['드묾'] > w['흔함']


def test_idf_gives_zero_to_a_gram_in_every_card():
    prof = {'a': {'전부'}, 'b': {'전부'}}
    assert kl.idf(prof)['전부'] == 0.0


# ── 닮음 ──────────────────────────────────────────────────────

def test_similarity_of_a_set_with_itself_is_one():
    w = {'가나': 1.0, '나다': 2.0}
    s = kl.similarity({'가나', '나다'}, {'가나', '나다'}, w)
    assert abs(s - 1.0) < 1e-9


def test_similarity_of_disjoint_sets_is_zero():
    assert kl.similarity({'가나'}, {'다라'}, {'가나': 1.0, '다라': 1.0}) == 0.0


def test_similarity_is_symmetric():
    w = {'가나': 1.0, '나다': 2.0, '다라': 3.0}
    a, b = {'가나', '나다'}, {'나다', '다라'}
    assert kl.similarity(a, b, w) == kl.similarity(b, a, w)


def test_similarity_of_empty_set_is_zero():
    assert kl.similarity(set(), {'가나'}, {'가나': 1.0}) == 0.0


def test_similarity_ignores_zero_weight_grams():
    w = {'전부': 0.0, '드묾': 1.0}
    assert kl.similarity({'전부'}, {'전부'}, w) == 0.0


# ── 이웃 ──────────────────────────────────────────────────────

CARDS = [
    _card('재건축 분담금', '재건축 분담금이 올랐다 조합이 갈라졌다', 'seoul',
          related=['용적률 완화']),
    _card('용적률 완화', '재건축 분담금과 용적률을 같이 본다', 'seoul'),
    # 원본과 「조합」 하나만 겹친다 — 걸리되 아래쪽에 서야 한다
    _card('전세 계약', '전세 보증금과 조합 규약을 같이 본다', 'lease'),
    _card('먼 이야기', 'zzz qqq', 'other'),
]


def test_neighbors_on_unknown_title_is_empty():
    assert kl.neighbors(CARDS, '없는 제목')['rows'] == []


def test_neighbors_never_include_the_card_itself():
    got = kl.neighbors(CARDS, '재건축 분담금')
    assert '재건축 분담금' not in [r['title'] for r in got['rows']]


def test_neighbors_rank_the_more_alike_card_first():
    rows = kl.neighbors(CARDS, '재건축 분담금')['rows']
    assert rows[0]['title'] == '용적률 완화'


def test_neighbors_drop_cards_that_share_nothing():
    rows = kl.neighbors(CARDS, '재건축 분담금')['rows']
    assert '먼 이야기' not in [r['title'] for r in rows]


def test_neighbors_mark_same_section():
    rows = kl.neighbors(CARDS, '재건축 분담금')['rows']
    by = {r['title']: r for r in rows}
    assert by['용적률 완화']['same_section'] is True
    assert by['전세 계약']['same_section'] is False


def test_neighbors_mark_what_is_already_in_related():
    rows = kl.neighbors(CARDS, '재건축 분담금')['rows']
    by = {r['title']: r for r in rows}
    assert by['용적률 완화']['in_related'] is True
    assert by['전세 계약']['in_related'] is False


def test_neighbors_report_declared_count():
    got = kl.neighbors(CARDS, '재건축 분담금')
    assert got['declared'] == 1
    assert got['declared_in_top'] == 1
    assert got['declared_missing'] == []


def test_neighbors_report_declared_the_score_did_not_find():
    cards = CARDS + [_card('혼자 있는 글', 'aaa bbb', 'far')]
    cards[0] = _card('재건축 분담금', '재건축 분담금이 올랐다 조합이 갈라졌다', 'seoul',
                     related=['용적률 완화', '혼자 있는 글'])
    got = kl.neighbors(cards, '재건축 분담금')
    assert got['declared'] == 2
    assert got['declared_missing'] == ['혼자 있는 글']


def test_neighbors_respect_the_top_cap():
    got = kl.neighbors(CARDS, '재건축 분담금', top=1)
    assert len(got['rows']) == 1
    assert got['shown'] == 1


def test_neighbors_carry_the_source_section():
    assert kl.neighbors(CARDS, '재건축 분담금')['section'] == 'seoul'


def test_neighbors_are_deterministic():
    a = kl.neighbors(CARDS, '재건축 분담금')
    b = kl.neighbors(CARDS, '재건축 분담금')
    assert a == b


def test_neighbors_break_score_ties_by_title():
    # 넷째 카드가 있어야 앞 셋이 나눠 가진 조각의 idf 가 0 을 벗어난다
    same = [_card('가', '똑같은 본문이다', 'x'),
            _card('나', '똑같은 본문이다', 'x'),
            _card('다', '똑같은 본문이다', 'x'),
            _card('라', '전혀 다른 이야기', 'x')]
    rows = kl.neighbors(same, '가')['rows']
    assert [r['title'] for r in rows] == ['나', '다']


def test_neighbors_find_nothing_when_every_card_says_the_same():
    """모든 카드가 같은 말을 쓰면 그 말로는 아무것도 구별 못 한다 — idf 가 0 이다."""
    same = [_card('가', '똑같은 본문이다', 'x'),
            _card('나', '똑같은 본문이다', 'x')]
    assert kl.neighbors(same, '가')['rows'] == []


# ── 실제 자료 ─────────────────────────────────────────────────

def test_neighbors_work_on_a_real_dashboard():
    import cards as cd
    cards = cd.load_cards(ROOT, 'gen_health_dashboard')
    got = kl.neighbors(cards, cd.card_id(cards[0]))
    assert got['rows'], '실제 카드에서 이웃이 하나도 안 나온다'
    assert all(0.0 < r['score'] <= 1.0 for r in got['rows'])
