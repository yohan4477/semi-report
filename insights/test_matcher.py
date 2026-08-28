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
    # 원문이 NVIDIA·Nvidia 를 섞어 쓴다. 가리면 Nvidia 표기를 통째로 잃는다
    assert mt.find('nvidia bought HBM', RULES) == ['엔비디아']
    assert mt.find('Nvidia bought HBM', RULES) == ['엔비디아']


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


# 짧은 한글 이름이 흔한 서술어와 겹치는 자리. deny 에 개체 이름만 넣으면 못 막지만
# 앞말을 붙인 구를 넣으면 _denied 가 그 자리를 걸러 낸다 — 새 장치가 필요 없다.
CURSOR = [
    {'canonical': '커서', 'type': '제품',
     'ko': ['커서'], 'en': ['Cursor'],
     'deny': ['워낙 커서', '너무 커서', '훨씬 커서', '매우 커서', '더 커서',
              '보다 커서', '배 커서', '배나 커서', '만큼 커서',
              '가 커서 ', '이 커서 ']},
]
CURSOR_RULES = mt.compile_rules(CURSOR)


def test_deny_with_a_leading_word_blocks_the_predicate():
    assert mt.find('차이가 커서 순환기내과에서는', CURSOR_RULES) == []
    assert mt.find('분자량이 커서 맛이 없다', CURSOR_RULES) == []
    assert mt.find('아마존보다 커서 외부 고객에게', CURSOR_RULES) == []
    assert mt.find('20배나 커서 전력 낭비', CURSOR_RULES) == []
    assert mt.find('워낙 커서, 오픈AI와', CURSOR_RULES) == []


def test_deny_with_a_leading_word_keeps_the_real_mention():
    assert mt.find('커서가 이 표현을 쓰기 시작했다', CURSOR_RULES) == ['커서']
    assert mt.find('스페이스X의 커서(Cursor) 인수', CURSOR_RULES) == ['커서']
    assert mt.find('딥시크, 커서', CURSOR_RULES) == ['커서']


def test_deny_keeps_a_mention_right_after_a_subject_particle():
    # 「…가 커서」를 통째로 막으면 이 줄이 사라진다. 뒤 공백까지 넣어 가른다 —
    # 서술어(크다)는 뒤에 절이 이어져 공백이 오고, 진짜 언급은 조사나 괄호가 온다.
    assert mt.find('SpaceXAI가 커서(Cursor) 인수 이후', CURSOR_RULES) == ['커서']
    assert mt.find('사용자가 커서를 업데이트하지 않아도', CURSOR_RULES) == ['커서']


def test_deny_still_blocks_the_predicate_after_a_subject_particle():
    assert mt.find('CRAH 보다 용량이 커서 표준이 됐다', CURSOR_RULES) == []
    assert mt.find('차이가 커서 순환기내과에서는', CURSOR_RULES) == []


# 짧은 영문 별칭은 대소문자를 가린다. 종목 기호와 약칭은 대문자로 쓰이는데
# 소문자까지 받으면 Fed 가 「keep them fed with data」의 fed 에 걸린다.
SHORTCASE = [
    {'canonical': '도쿄일렉트론', 'type': '회사', 'ko': ['도쿄일렉트론'],
     'en': ['Tokyo Electron', 'TEL'], 'deny': []},
]
SHORTCASE_RULES = mt.compile_rules(SHORTCASE)


def test_a_short_alias_that_is_a_common_word_belongs_out_of_the_dictionary():
    # Fed 를 별칭으로 두면 「keep them fed with data」가 연준으로 잡힌다.
    # 규칙으로 못 가른다 — 사전에서 빼는 것이 답이다.
    with_fed = mt.compile_rules(
        [{'canonical': '연준', 'type': '회사', 'ko': ['연준'],
          'en': ['Fed'], 'deny': []}])
    assert mt.find('keep them fed with data', with_fed) == ['연준']
    without = mt.compile_rules(
        [{'canonical': '연준', 'type': '회사', 'ko': ['연준'],
          'en': [], 'deny': []}])
    assert mt.find('keep them fed with data', without) == []


def test_english_alias_matches_either_case():
    assert mt.find('tokyo electron ships', SHORTCASE_RULES) == ['도쿄일렉트론']
    assert mt.find('Tokyo Electron ships', SHORTCASE_RULES) == ['도쿄일렉트론']
