import io
import json
import os

import entities_lib as el
import paths


ROWS = [
    {'canonical': '램리서치', 'type': '회사',
     'ko': ['램리서치', '램리써치'], 'en': ['Lam Research', 'Lam'], 'deny': []},
    {'canonical': '메타', 'type': '회사',
     'ko': ['메타'], 'en': ['Meta'], 'deny': ['메타버스', '메타인지']},
]


def test_paths_point_under_insights():
    assert paths.ENTITIES == os.path.join(paths.HERE, 'entities.json')
    assert paths.INDEX == os.path.join(paths.HERE, 'index.json')


def test_norm_lowercases_and_strips():
    assert el.norm('  Lam Research ') == 'lam research'
    assert el.norm('램리서치') == '램리서치'


def test_alias_index_maps_every_alias_to_canonical():
    idx = el.alias_index(ROWS)
    assert idx['램리서치'] == '램리서치'
    assert idx['램리써치'] == '램리서치'
    assert idx['lam research'] == '램리서치'
    assert idx['lam'] == '램리서치'
    assert idx['meta'] == '메타'


def test_validate_passes_clean_rows():
    assert el.validate(ROWS) == []


def test_validate_catches_alias_on_two_canonicals():
    rows = ROWS + [{'canonical': '마이크론', 'type': '회사',
                    'ko': ['램리서치'], 'en': [], 'deny': []}]
    msgs = el.validate(rows)
    assert any('램리서치' in m for m in msgs)


def test_validate_catches_bad_type():
    rows = [{'canonical': '엔비디아', 'type': '반도체회사',
             'ko': ['엔비디아'], 'en': [], 'deny': []}]
    msgs = el.validate(rows)
    assert any('반도체회사' in m for m in msgs)


def test_validate_catches_canonical_missing_from_ko():
    rows = [{'canonical': '엔비디아', 'type': '회사',
             'ko': ['엔비디아코리아'], 'en': [], 'deny': []}]
    msgs = el.validate(rows)
    assert any('엔비디아' in m for m in msgs)


def test_save_sorts_by_canonical_and_load_round_trips(tmp_path):
    p = str(tmp_path / 'e.json')
    el.save(list(reversed(ROWS)), p)
    back = el.load(p)
    assert [r['canonical'] for r in back] == ['램리서치', '메타']
    assert back == el.load(p)


def test_save_writes_utf8_without_ascii_escapes(tmp_path):
    p = str(tmp_path / 'e.json')
    el.save(ROWS, p)
    text = io.open(p, encoding='utf-8').read()
    assert '램리서치' in text
    assert '\\u' not in text
