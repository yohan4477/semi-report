import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import evidence as ev  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ── 한 줄에서 낱말 찾기 ────────────────────────────────────────

def test_korean_term_matches_with_a_particle_attached():
    assert ev.line_hits('리스 계약이 늘었다', '리스', ())


def test_korean_term_is_blocked_by_deny():
    assert not ev.line_hits('애널리스트가 말했다', '리스', ('애널리스트', ))


def test_deny_blocks_only_the_denied_place():
    assert ev.line_hits('애널리스트와 리스 계약', '리스', ('애널리스트', ))


def test_deny_takes_more_than_one_word():
    assert not ev.line_hits('리스크가 크다', '리스', ('애널리스트', '리스크'))


def test_latin_term_needs_a_word_boundary():
    assert not ev.line_hits('SPVX 라는 것', 'SPV', ())
    assert ev.line_hits('SPV 를 세웠다', 'SPV', ())


def test_latin_term_ignores_case():
    assert ev.line_hits('spv 를 세웠다', 'SPV', ())


def test_latin_term_matches_next_to_punctuation():
    assert ev.line_hits('(SPV) 구조', 'SPV', ())


def test_empty_line_hits_nothing():
    assert not ev.line_hits('', '리스', ())


# ── 문서 빈도와 무게 ──────────────────────────────────────────

DOCS = [
    ('a.md', '리스 계약을 맺었다\nSPV 를 세웠다'),
    ('b.md', '리스 계약이 또 있다'),
    ('c.md', '애널리스트가 말했다'),
    ('d.md', '아무 상관 없는 글'),
]


def test_doc_freq_counts_documents_not_lines():
    """a.md 는 「리스」가 한 줄에만 있고 SPV 가 다른 줄에 있다. 문서로 한 편이다."""
    assert ev.doc_freq(DOCS, 'SPV', ()) == 1


def test_doc_freq_without_deny_lets_the_false_match_in():
    # c.md 의 「애널리스트」가 「리스」로 잡힌다 — deny 가 필요한 이유
    assert ev.doc_freq(DOCS, '리스', ()) == 3


def test_doc_freq_respects_deny():
    assert ev.doc_freq(DOCS, '리스', ('애널리스트', )) == 2


def test_doc_freq_of_a_word_nobody_uses_is_zero():
    assert ev.doc_freq(DOCS, '없는말', ()) == 0


def test_idf_of_a_rare_word_beats_a_common_one():
    assert ev.idf(len(DOCS), 1) > ev.idf(len(DOCS), 3)


def test_idf_of_a_word_in_every_document_is_zero():
    assert ev.idf(4, 4) == 0.0


def test_idf_of_a_word_in_no_document_is_zero():
    assert ev.idf(4, 0) == 0.0


# ── 가지에 붙이기 ────────────────────────────────────────────

BRANCH = {'label': '자금 조달', 'terms': ['리스', 'SPV'],
          'deny': ['애널리스트', '리스크']}


def test_weigh_reports_documents():
    got = ev.weigh(DOCS, BRANCH)
    assert got['label'] == '자금 조달'
    assert got['docs'] == 2


def test_weigh_gives_no_single_ranking_number():
    """무게를 내면 「이 순으로 파라」로 읽힌다. 그러면 맹점이 꼴찌로 간다."""
    got = ev.weigh(DOCS, BRANCH)
    assert 'weight' not in got
    assert 'score' not in got


def test_weigh_shows_how_much_one_term_carried_the_branch():
    got = ev.weigh(DOCS, BRANCH)
    assert got['widest'] == '리스'
    assert got['widest_share'] == 1.0        # 2편 중 2편이 「리스」로 걸렸다
    # 「리스」는 4편 중 2편 → idf = log(2) ≈ 0.693. 흔할수록 0 에 가깝다
    assert abs(got['widest_idf'] - 0.693) < 0.01


def test_weigh_shows_each_term_separately():
    got = ev.weigh(DOCS, BRANCH)
    per = {t['term']: t for t in got['terms']}
    assert per['리스']['docs'] == 2
    assert per['SPV']['docs'] == 1
    assert per['SPV']['idf'] > per['리스']['idf']


def test_weigh_names_the_term_that_carried_the_branch():
    """253편이 「리스」 하나로 부푼 것을 이 줄이 드러낸다."""
    got = ev.weigh(DOCS, BRANCH)
    assert got['widest'] == '리스'


def test_weigh_without_deny_lets_the_false_match_in():
    loose = {'label': 'x', 'terms': ['리스'], 'deny': []}
    assert ev.weigh(DOCS, loose)['docs'] == 3


def test_weigh_with_deny_keeps_the_false_match_out():
    tight = {'label': 'x', 'terms': ['리스'], 'deny': ['애널리스트']}
    assert ev.weigh(DOCS, tight)['docs'] == 2


def test_weigh_carries_addresses_so_the_claim_can_be_checked():
    got = ev.weigh(DOCS, BRANCH)
    assert 'a.md#L2' in got['hits']


def test_weigh_of_a_branch_nothing_supports_is_empty_not_an_error():
    got = ev.weigh(DOCS, {'label': '빈 가지', 'terms': ['없는말'], 'deny': []})
    assert got['docs'] == 0
    assert got['hits'] == []
    assert got['widest'] is None
    assert got['widest_share'] == 0.0


def test_weigh_is_deterministic():
    assert ev.weigh(DOCS, BRANCH) == ev.weigh(DOCS, BRANCH)


# ── 실제 코퍼스 ───────────────────────────────────────────────

def test_deny_actually_shrinks_the_funding_branch_on_the_real_corpus():
    """실측: 「리스」가 애널리스트·리스크에 걸려 문서 수를 부풀렸다."""
    docs = ev.corpus(ROOT)
    loose = ev.weigh(docs, {'label': 'x', 'terms': ['리스'], 'deny': []})
    tight = ev.weigh(docs, {'label': 'x', 'terms': ['리스'],
                            'deny': ['애널리스트', '리스크', '릴리스']})
    assert tight['docs'] < loose['docs'], '실제 코퍼스에서 deny 가 아무것도 안 걸렀다'


def test_corpus_reads_the_real_files():
    docs = ev.corpus(ROOT)
    assert len(docs) > 400
    assert all(isinstance(t, str) for _, t in docs)
