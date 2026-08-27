import matcher as mt


ROWS = [
    {'canonical': '램리서치', 'type': '회사',
     'ko': ['램리서치'], 'en': ['Lam Research', 'Lam'], 'deny': []},
    {'canonical': '메타', 'type': '회사',
     'ko': ['메타'], 'en': ['Meta'], 'deny': ['메타버스', '메타인지']},
    {'canonical': '엔비디아', 'type': '회사',
     'ko': ['엔비디아'], 'en': ['NVIDIA'], 'deny': []},
]
RULES = mt.compile_rules(ROWS)


def test_finds_korean_alias_with_particle():
    assert mt.find('엔비디아가 HBM 을 샀다', RULES) == ['엔비디아']


def test_finds_english_alias_case_insensitively():
    assert mt.find('nvidia bought HBM', RULES) == ['엔비디아']


def test_english_alias_needs_word_boundary():
    assert mt.find('Lamborghini 는 차다', RULES) == []


def test_english_alias_matches_standalone_word():
    assert mt.find('Lam shipped the tool', RULES) == ['램리서치']


def test_english_alias_matches_with_punctuation_around():
    assert mt.find('(Lam) 과 TEL', RULES) == ['램리서치']


def test_multiword_english_alias_matches():
    assert mt.find('Lam Research holds the share', RULES) == ['램리서치']


def test_deny_blocks_substring_false_positive():
    assert mt.find('메타버스 시장이 컸다', RULES) == []


def test_deny_does_not_block_real_mention():
    assert mt.find('메타가 칩을 샀다', RULES) == ['메타']


def test_deny_blocks_only_the_denied_span():
    assert mt.find('메타버스 얘기 끝에 메타가 나왔다', RULES) == ['메타']


def test_returns_sorted_unique_canonicals():
    got = mt.find('엔비디아와 메타, 그리고 엔비디아', RULES)
    assert got == ['메타', '엔비디아']


def test_empty_line_finds_nothing():
    assert mt.find('', RULES) == []


def test_result_is_deterministic():
    line = 'NVIDIA 와 Lam Research 가 메타를 만났다'
    assert mt.find(line, RULES) == mt.find(line, RULES)
    assert mt.find(line, RULES) == ['램리서치', '메타', '엔비디아']
