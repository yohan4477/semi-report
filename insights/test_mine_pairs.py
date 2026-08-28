import io
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import mine_pairs as mp  # noqa: E402


def test_pairs_in_reads_a_gloss():
    assert mp.pairs_in('도쿄일렉트론(TEL)이 앞선다') == [('도쿄일렉트론', 'TEL')]


def test_pairs_in_allows_spaces_around_the_bracket():
    assert mp.pairs_in('딥마인드 ( Google DeepMind ) 는') == [
        ('딥마인드', 'Google DeepMind')]


def test_pairs_in_reads_more_than_one_on_a_line():
    got = mp.pairs_in('시놉시스(Synopsys)와 케이던스(Cadence)')
    assert got == [('시놉시스', 'Synopsys'), ('케이던스', 'Cadence')]


def test_pairs_in_drops_a_gloss_carrying_a_year():
    # 「인텔(ISSCC 2026)」 은 이름이 아니라 학회 이름과 해다
    assert mp.pairs_in('인텔(ISSCC 2026)에서 밝혔다') == []


def test_pairs_in_ignores_a_korean_gloss():
    assert mp.pairs_in('고대역폭메모리(고대역폭 메모리)') == []


def test_pairs_in_ignores_a_bare_number_gloss():
    assert mp.pairs_in('영업이익(2,530억 달러)') == []


def test_pairs_in_finds_nothing_without_a_bracket():
    assert mp.pairs_in('도쿄일렉트론이 앞선다') == []


def _mkroot(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(
        '도쿄일렉트론(TEL)이 앞선다.\n도쿄일렉트론(TEL)은 또.\n'
        '엔비디아(NVIDIA)는 이미 사전에 있다.\n')
    return str(tmp_path)


def test_mine_counts_repeats(tmp_path):
    got = mp.mine(_mkroot(tmp_path), ['content/a.md'], {'도쿄일렉트론'})
    assert got[('도쿄일렉트론', 'TEL')] == 2


def test_mine_skips_entities_that_already_have_english(tmp_path):
    got = mp.mine(_mkroot(tmp_path), ['content/a.md'], {'도쿄일렉트론'})
    assert not [k for k in got if k[0] == '엔비디아']


def test_mine_skips_korean_words_that_are_not_entities(tmp_path):
    got = mp.mine(_mkroot(tmp_path), ['content/a.md'], set())
    assert got == {}
