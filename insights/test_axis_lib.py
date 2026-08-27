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
