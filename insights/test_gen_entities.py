import io
import os

import entities_lib as el
import gen_entities as ge


NOTE_A = '''---
source: "content/x.md"
actors: [엔비디아, 램리서치]
topics: [HBM]
---

본문.
'''

NOTE_B = '''---
source: "content/y.md"
actors: [엔비디아]
---

본문.
'''


def _write_notes(tmp_path):
    d = tmp_path / 'notes'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(NOTE_A)
    io.open(str(d / 'b.md'), 'w', encoding='utf-8').write(NOTE_B)
    return str(d)


def test_actors_from_notes_counts_occurrences(tmp_path):
    got = ge.actors_from_notes(_write_notes(tmp_path))
    assert got == {'엔비디아': 2, '램리서치': 1}


def test_actors_from_notes_ignores_missing_key(tmp_path):
    d = tmp_path / 'notes'
    d.mkdir()
    io.open(str(d / 'c.md'), 'w', encoding='utf-8').write('---\nsource: "x"\n---\n\n본문.\n')
    assert ge.actors_from_notes(str(d)) == {}


def test_seed_folds_alias_into_canonical_row():
    rows = ge.seed({'엔비디아': 2}, {'NVIDIA': '엔비디아', 'Lam': '램리서치'})
    assert len(rows) == 1
    r = rows[0]
    assert r['canonical'] == '엔비디아'
    assert '엔비디아' in r['ko']
    assert 'NVIDIA' in r['en']


def test_seed_drops_case_variant_of_an_alias_it_already_has():
    # 영문 별칭 매칭이 대소문자를 무시한다. 변형을 다 담으면 사람이 읽는 사전만 붇는다
    rows = ge.seed({'엔비디아': 2}, {'NVIDIA': '엔비디아', 'Nvidia': '엔비디아'})
    assert rows[0]['en'] == ['NVIDIA']


def test_seed_splits_latin_aliases_into_en():
    rows = ge.seed({'앤트로픽': 1}, {'Anthropic': '앤트로픽', '앤스로픽': '앤트로픽'})
    r = rows[0]
    assert 'Anthropic' in r['en']
    assert '앤스로픽' in r['ko']


def test_seed_keeps_latin_canonical_in_both_lists():
    rows = ge.seed({'TSMC': 3}, {})
    r = rows[0]
    assert r['canonical'] == 'TSMC'
    assert 'TSMC' in r['ko']
    assert 'TSMC' in r['en']


def test_seed_marks_type_undecided():
    rows = ge.seed({'엔비디아': 2}, {})
    assert rows[0]['type'] == '미정'


def test_seed_output_passes_validate():
    rows = ge.seed({'엔비디아': 2, 'TSMC': 1}, {'NVIDIA': '엔비디아'})
    assert el.validate(rows) == []


def test_seed_drops_aliases_pointing_at_unknown_canonical():
    rows = ge.seed({'엔비디아': 1}, {'Lam Research': '램리서치'})
    assert [r['canonical'] for r in rows] == ['엔비디아']
