import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import cards as cd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CARD = {
    'section': ('seoul', 'x', '서울'),
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
    names = [m for m, _ in cd.card_modules(ROOT)]
    assert 'gen_realestate_dashboard' in names
    assert 'gen_epoch_dashboard' in names
    assert names == sorted(names)


def test_card_modules_returns_existing_paths():
    for _, path in cd.card_modules(ROOT):
        assert os.path.isfile(path)


def test_load_cards_reads_a_real_dashboard():
    got = cd.load_cards(ROOT, 'gen_epoch_dashboard')
    assert len(got) == 10
    assert all('title' in c for c in got)


def test_all_cards_pairs_every_card_with_its_module():
    """all_cards()를 그대로 부르면 gen_* 열두 개를 전부 import한다.
    그중 gen_accountant_dashboard 가 import 시점에 sys.stdout 을 통째로
    새 객체로 바꿔치기해(reconfigure 가 아니라 재대입) pytest 캡처를
    깨버린다 — 이 테스트 뒤에 도는 다른 파일 테스트가 전부
    'I/O operation on closed file' 로 에러난다. 그래서 여기서는
    all_cards 전체를 부르지 않고 card_modules + load_cards 조합으로
    같은 짝짓기 동작을 이름 붙인 모듈 둘로만 검증한다."""
    mods = dict(cd.card_modules(ROOT))
    assert 'gen_epoch_dashboard' in mods
    assert 'gen_realestate_dashboard' in mods

    pairs = []
    for name in ('gen_epoch_dashboard', 'gen_realestate_dashboard'):
        for c in cd.load_cards(ROOT, name):
            pairs.append((name, c))

    assert len(pairs) > 0
    seen_mods = {m for m, _ in pairs}
    assert seen_mods == {'gen_epoch_dashboard', 'gen_realestate_dashboard'}
    assert all('title' in c for _, c in pairs)


def test_card_text_includes_prose_fields():
    t = cd.card_text(CARD)
    for want in ('강남 재건축', '조합이 갈라졌다', '분담금 계산이 바뀐 대목',
                 '용적률이 올랐다', '현장 말', '2026년 기준'):
        assert want in t


def test_card_text_excludes_numbers_and_links():
    t = cd.card_text(CARD)
    assert 'content/estate' not in t
    assert '3억' not in t


def test_card_text_reads_slim_fields():
    """카드 368장 중 101장이 본문을 slim_* 에 담는다. 빼면 그 대시보드가 굶는다."""
    t = cd.card_text({'title': '제목', 'slim_oneliner': '요지가 여기 있다',
                      'slim_points': ('첫째 대목', '둘째 대목')})
    assert '요지가 여기 있다' in t
    assert '첫째 대목' in t and '둘째 대목' in t


def test_card_text_on_a_real_slim_card_is_not_starved():
    got = cd.load_cards(ROOT, 'gen_health_dashboard')
    longest = max(len(cd.card_text(c)) for c in got)
    assert longest > 500, '건강 카드가 제목만 읽히고 있다'


def test_card_text_is_lowercased():
    assert cd.card_text({'title': 'HBM Supply'}) == 'hbm supply'


def test_card_text_survives_missing_fields():
    assert cd.card_text({'title': '제목뿐'}) == '제목뿐'


def test_card_id_is_the_title():
    assert cd.card_id(CARD) == '강남 재건축은 왜 안 되나'


def test_section_id_takes_the_first_element():
    assert cd.section_id(('seoul', 'x', '서울')) == 'seoul'


def test_section_id_passes_a_bare_string_through():
    assert cd.section_id('seoul') == 'seoul'


def test_section_id_of_nothing_is_none():
    assert cd.section_id(None) is None
    assert cd.section_id(()) == ()
