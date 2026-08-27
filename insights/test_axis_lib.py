import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import axis_lib as al  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CARD = {
    'section': ('seoul', 'x', '서울'),
    'topic': ('t', '재건축'),
    'title': '강남 재건축은 왜 안 되나',
    'oneliner': '조합이 갈라졌다',
    'gain': '분담금 계산이 바뀐 대목',
    'points': ('용적률이 올랐다', '분담금은 그대로다'),
    'quote': ('현장 말', ),
    'note': '2026년 기준',
    'clash': (),
    'stats': (('분담금', '3억'), ),
    'links': (('원문', 'content/estate/a.md'), ),
}


def test_card_modules_finds_real_generators():
    got = al.card_modules(ROOT)
    names = [m for m, _ in got]
    assert 'gen_realestate_dashboard' in names
    assert 'gen_epoch_dashboard' in names
    assert names == sorted(names)


def test_card_modules_returns_existing_paths():
    for _, path in al.card_modules(ROOT):
        assert os.path.isfile(path)


def test_load_cards_reads_real_dashboard():
    cards = al.load_cards(ROOT, 'gen_epoch_dashboard')
    assert len(cards) == 10
    assert all('title' in c for c in cards)


def test_card_text_includes_prose_fields():
    t = al.card_text(CARD)
    assert '강남 재건축' in t
    assert '조합이 갈라졌다' in t
    assert '분담금 계산이 바뀐 대목' in t
    assert '용적률이 올랐다' in t
    assert '현장 말' in t
    assert '2026년 기준' in t


def test_card_text_excludes_numbers_and_links():
    t = al.card_text(CARD)
    assert 'content/estate' not in t
    assert '3억' not in t


def test_card_text_is_lowercased():
    assert al.card_text({'title': 'HBM Supply'}) == 'hbm supply'


def test_card_text_survives_missing_fields():
    assert al.card_text({'title': '제목뿐'}) == '제목뿐'


def test_card_id_is_the_title():
    assert al.card_id(CARD) == '강남 재건축은 왜 안 되나'


def test_parse_axis_fills_defaults():
    a = al.parse_axis({'name': '지역', 'cells': [{'id': '서울', 'words': ['강남']}]})
    assert a['name'] == '지역'
    assert a['cells'][0]['id'] == '서울'
    assert a['cells'][0]['words'] == ['서울', '강남']


def test_parse_axis_adds_id_to_words_when_absent():
    a = al.parse_axis({'name': '지역', 'cells': [{'id': '인천'}]})
    assert '인천' in a['cells'][0]['words']


def test_parse_axis_lowercases_words():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': 'HBM', 'words': ['HBM3E']}]})
    assert a['cells'][0]['words'] == ['hbm', 'hbm3e']


def test_parse_axis_overwrites_human_written_shape():
    a = al.parse_axis({'name': 'x', 'shape': '수식',
                       'cells': [{'id': 'a'}, {'id': 'b'}]})
    assert a['shape'] == '목록'


def test_shape_list_when_no_relations():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': 'a'}, {'id': 'b'}]})
    assert al.shape_of(a) == '목록'


def test_shape_line_when_every_cell_has_order():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': 'a', 'order': 1},
                                              {'id': 'b', 'order': 2}]})
    assert al.shape_of(a) == '선'


def test_shape_list_when_order_is_partial():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': 'a', 'order': 1},
                                              {'id': 'b'}]})
    assert al.shape_of(a) == '목록'


def test_shape_tree_when_a_cell_has_parent():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': '수도권'},
                                              {'id': '서울', 'parent': '수도권'}]})
    assert al.shape_of(a) == '나무'


def test_shape_chain_when_cells_feed_forward():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': '매물', 'feeds': '계약'},
                                              {'id': '계약', 'feeds': '등기'},
                                              {'id': '등기'}]})
    assert al.shape_of(a) == '사슬'


def test_shape_loop_when_last_feeds_first():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': '조달', 'feeds': '칩'},
                                              {'id': '칩', 'feeds': '매출'},
                                              {'id': '매출', 'feeds': '조달'}]})
    assert al.shape_of(a) == '고리'


def test_shape_formula_when_a_cell_has_op():
    a = al.parse_axis({'name': 'x', 'cells': [{'id': '매출', 'op': '×'},
                                              {'id': '단가'}, {'id': '수량'}]})
    assert al.shape_of(a) == '수식'


REGION = {'name': '지역', 'cells': [
    {'id': '서울', 'words': ['서울', '강남']},
    {'id': '경기', 'words': ['경기', '분당']},
    {'id': '인천', 'words': ['인천']},
]}


def _card(title, body=''):
    return {'title': title, 'oneliner': body, 'section': ('s', 'x', 'S')}


def test_place_puts_card_in_matching_cell():
    axis = al.parse_axis(REGION)
    got = al.place([_card('강남 재건축')], axis)
    assert got['강남 재건축'] == ['서울']


def test_place_matches_on_body_not_just_title():
    axis = al.parse_axis(REGION)
    got = al.place([_card('무제', '분당 이야기다')], axis)
    assert got['무제'] == ['경기']


def test_place_returns_empty_list_for_unmatched_card():
    axis = al.parse_axis(REGION)
    assert al.place([_card('아무 데도 안 걸림')], axis)['아무 데도 안 걸림'] == []


def test_place_records_two_cells_when_card_matches_both():
    axis = al.parse_axis(REGION)
    got = al.place([_card('강남과 분당 비교')], axis)
    assert got['강남과 분당 비교'] == ['경기', '서울']


def test_review_counts_cells():
    axis = al.parse_axis(REGION)
    r = al.review([_card('강남 것'), _card('서울 것'), _card('분당 것')], axis)
    assert r['cards'] == 3
    assert {c['id']: c['n'] for c in r['cells']} == {'서울': 2, '경기': 1, '인천': 0}


def test_review_reports_empty_cell():
    axis = al.parse_axis(REGION)
    # 카드 하나가 서울에만 걸리니 경기와 인천이 빈다. 빈칸은 축에 적힌 차례로 나온다
    assert al.review([_card('강남 것')], axis)['empty'] == ['경기', '인천']


def test_review_reports_overlap():
    axis = al.parse_axis(REGION)
    r = al.review([_card('강남과 분당')], axis)
    assert r['overlap'] == [{'card': '강남과 분당', 'cells': ['경기', '서울']}]


def test_review_does_not_count_also_as_overlap():
    axis = al.parse_axis(REGION)
    c = _card('강남 것')
    c['also'] = [('경기', 'x', '경기')]
    assert al.review([c], axis)['overlap'] == []


def test_review_reports_residual_and_pct():
    axis = al.parse_axis(REGION)
    r = al.review([_card('강남 것'), _card('무관한 것')], axis)
    assert r['residual'] == ['무관한 것']
    assert r['residual_pct'] == 50


def test_review_reports_skew_ignoring_empty_cells():
    axis = al.parse_axis(REGION)
    cards = [_card('강남 %d' % i) for i in range(4)] + [_card('분당 하나')]
    assert al.review(cards, axis)['skew'] == 4.0


def test_review_skew_is_zero_when_nothing_placed():
    axis = al.parse_axis(REGION)
    assert al.review([_card('무관')], axis)['skew'] == 0


def test_review_carries_shape_and_full_placement():
    axis = al.parse_axis(REGION)
    r = al.review([_card('강남 것'), _card('무관')], axis)
    assert r['shape'] == '목록'
    assert r['placement'] == {'강남 것': ['서울'], '무관': []}


def test_review_never_raises_on_bad_axis():
    r = al.review([_card('아무거나')], al.parse_axis({'name': '빈 축', 'cells': []}))
    assert r['cells'] == []
    assert r['residual_pct'] == 100


def _sc(title, sec, also=None):
    c = {'title': title, 'section': (sec, 'x', sec)}
    if also:
        c['also'] = [(a, 'x', a) for a in also]
    return c


def test_declared_axis_builds_cells_from_sections():
    cards = [_sc('가', '서울'), _sc('나', '경기'), _sc('다', '서울')]
    a = al.declared_axis(cards)
    assert [c['id'] for c in a['cells']] == ['서울', '경기']
    assert a['name'] == '섹션'


def test_declared_axis_includes_also_sections():
    a = al.declared_axis([_sc('가', '서울', also=['경기'])])
    assert [c['id'] for c in a['cells']] == ['서울', '경기']


def test_declared_place_reads_section_not_words():
    got = al.declared_place([_sc('강남 이야기', '지방')])
    assert got['강남 이야기'] == ['지방']


def test_declared_place_includes_also():
    got = al.declared_place([_sc('가', '서울', also=['경기'])])
    assert got['가'] == ['경기', '서울']


def test_declared_review_has_no_residual():
    r = al.declared_review([_sc('가', '서울'), _sc('나', '경기')])
    assert r['residual'] == []
    assert r['residual_pct'] == 0


def test_declared_review_names_overlap_as_declared():
    r = al.declared_review([_sc('가', '서울', also=['경기'])])
    assert r['overlap_declared'] == [{'card': '가', 'cells': ['경기', '서울']}]
    assert r['overlap'] == []


def test_declared_review_on_real_dashboard():
    cards = al.load_cards(ROOT, 'gen_epoch_dashboard')
    r = al.declared_review(cards)
    assert r['cards'] == 10
    assert r['residual'] == []
    assert sum(c['n'] for c in r['cells']) >= 10
