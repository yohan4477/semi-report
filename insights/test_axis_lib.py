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
