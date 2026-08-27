import times as tm


def test_explicit_reads_a_plain_year():
    assert tm.explicit('1965년 한일협정으로 시작됐다') == [1965]


def test_explicit_allows_a_space_before_the_marker():
    assert tm.explicit('2028 년에 만료된다') == [2028]


def test_explicit_sorts_and_dedupes():
    assert tm.explicit('2020년과 2018년, 다시 2020년') == [2018, 2020]


def test_explicit_ignores_a_bare_number():
    assert tm.explicit('매출이 2024 억이다') == []


def test_explicit_ignores_a_year_glued_to_more_digits():
    assert tm.explicit('일련번호 20260101년') == []


def test_explicit_reads_a_decade_as_its_first_year():
    assert tm.explicit('1990년대 일본은') == [1990]


def test_computed_resolves_last_year():
    assert tm.computed('작년에 샀다', 2026) == [2025]


def test_computed_resolves_the_year_before_last_without_double_counting():
    assert tm.computed('재작년에 샀다', 2026) == [2024]


def test_computed_resolves_this_year_and_next():
    assert tm.computed('올해와 내년에 걸쳐', 2026) == [2026, 2027]


def test_computed_resolves_numeric_offsets():
    assert tm.computed('3년 전에는', 2026) == [2023]
    assert tm.computed('5년 후에는', 2026) == [2031]
    assert tm.computed('2년 뒤에는', 2026) == [2028]


def test_computed_ignores_elapsed_time_phrasing():
    assert tm.computed('3년 만에 처음이다', 2026) == []


def test_computed_does_not_read_digits_of_a_year_as_an_offset():
    assert tm.computed('1965년 전후로', 2026) == []


def test_computed_finds_nothing_without_a_marker():
    assert tm.computed('점유율이 90%다', 2026) == []


def test_tense_splits_three_ways():
    assert tm.tense_of(1965, 2026) == '회고'
    assert tm.tense_of(2026, 2026) == '현재'
    assert tm.tense_of(2028, 2026) == '전망'


def test_find_marks_explicit_retrospect():
    got = tm.find('1965년 한일협정', '2024-09-27')
    assert got == {'t': '1965', 'how': '명시', 'tense': '회고'}


def test_find_marks_explicit_forecast():
    got = tm.find('2028년에 협정이 만료된다', '2024-09-27')
    assert got['t'] == '2028'
    assert got['tense'] == '전망'


def test_find_takes_the_latest_year_and_records_the_span():
    got = tm.find('2018년부터 2028년까지', '2024-09-27')
    assert got['t'] == '2028'
    assert got['tense'] == '전망'
    assert got['span'] == ['2018', '2028']


def test_find_omits_span_when_one_year():
    assert 'span' not in tm.find('2028년', '2024-09-27')


def test_find_prefers_explicit_over_computed():
    got = tm.find('2020년 실적은 작년보다 좋았다', '2026-01-01')
    assert got['how'] == '명시'
    assert got['t'] == '2020'


def test_find_falls_back_to_computed():
    got = tm.find('작년보다 좋았다', '2026-01-01')
    assert got == {'t': '2025', 'how': '계산', 'tense': '회고'}


def test_find_returns_none_without_any_marker():
    assert tm.find('점유율이 90%다', '2026-01-01') is None


def test_find_returns_none_without_an_utterance_date():
    assert tm.find('작년보다 좋았다', '') is None


def test_find_drops_years_outside_the_plausible_range():
    assert tm.find('서기 1200년에는', '2026-01-01') is None
    assert tm.find('2999년에는', '2026-01-01') is None


def test_find_keeps_a_far_but_plausible_year():
    assert tm.find('1900년 이후 106개 구간', '2026-08-20')['t'] == '1900'
    assert tm.find('2050년까지', '2026-04-20')['t'] == '2050'


def test_find_is_deterministic():
    line = '2018년과 2028년, 그리고 작년'
    assert tm.find(line, '2024-09-27') == tm.find(line, '2024-09-27')


def test_computed_ignores_a_duration_that_runs_into_another_word():
    # 「20년 전력공급 계약」은 20년짜리 계약이지 20년 전이 아니다
    assert tm.computed('MS 와 20년 전력공급 계약을 맺었다', 2026) == []
    # 「10~20년 뒤처짐」도 뒤가 아니라 뒤처지다이다
    assert tm.computed('IT 인프라가 10~20년 뒤처짐', 2026) == []


def test_computed_still_reads_offsets_followed_by_a_particle():
    assert tm.computed('3년 전에는', 2026) == [2023]
    assert tm.computed('3년 전이다', 2026) == [2023]
    assert tm.computed('10년 뒤면', 2026) == [2036]
    assert tm.computed('5년 후까지', 2026) == [2031]
    assert tm.computed('3년 전보다', 2026) == [2023]


def test_computed_still_reads_an_offset_followed_by_a_space():
    assert tm.computed('10~20년 뒤 서서히 사라진다', 2026) == [2046]
