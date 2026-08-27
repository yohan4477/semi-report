import io
import json
import os

import paths
import utterance as ut


def test_paths_points_under_insights():
    assert paths.TIMES == os.path.join(paths.HERE, 'times.json')


def test_name_date_reads_six_digit_bracket():
    assert ut.name_date('content/epoch/[260520] 프런티어 랩.md') == '2026-05-20'


def test_name_date_reads_iso_in_filename():
    assert ut.name_date(
        'content/understanding/2026-08-24-물가-신호.md') == '2026-08-24'


def test_name_date_reads_four_digit_bracket_as_month_start():
    assert ut.name_date('content/linkedin/[2604] 링크드인 게시물.md') == '2026-04-01'


def test_name_date_is_empty_when_nothing_matches():
    assert ut.name_date('content/understanding/권효재 대표/대만 LNG 초비상.md') == ''


def test_name_date_ignores_directory_part():
    assert ut.name_date('content/[250101] 폴더/무제.md') == ''


def test_section_for_maps_known_categories():
    assert ut.section_for(['ai-infra/compute']) == 'chip'
    assert ut.section_for(['회계사']) == 'biz'
    assert ut.section_for(['ai-infra/power']) == 'power'
    assert ut.section_for(['AI Engineer']) == 'model'


def test_section_for_is_empty_on_unknown():
    assert ut.section_for(['root']) == ''
    assert ut.section_for(None) == ''


def _mkmanifest(tmp_path):
    p = str(tmp_path / 'manifest.json')
    io.open(p, 'w', encoding='utf-8').write(json.dumps({
        'generated': '2026-08-28',
        'sources': [
            {'path': 'content/a/[260520] 가.md', 'date': '2026-05-20',
             'categories': ['ai-infra/compute']},
            {'path': 'content/a/[260601] 나.md', 'date': '',
             'categories': ['회계사']},
            {'path': 'content/a/무제.md', 'date': '', 'categories': []},
        ],
    }, ensure_ascii=False))
    return p


def test_load_takes_date_from_manifest(tmp_path):
    meta = ut.load('.', _mkmanifest(tmp_path))
    assert meta['content/a/[260520] 가.md']['date'] == '2026-05-20'
    assert meta['content/a/[260520] 가.md']['section'] == 'chip'


def test_load_falls_back_to_filename_when_manifest_date_is_blank(tmp_path):
    meta = ut.load('.', _mkmanifest(tmp_path))
    assert meta['content/a/[260601] 나.md']['date'] == '2026-06-01'


def test_load_leaves_date_empty_when_neither_source_has_one(tmp_path):
    meta = ut.load('.', _mkmanifest(tmp_path))
    assert meta['content/a/무제.md']['date'] == ''


def test_date_of_falls_back_for_a_file_absent_from_manifest(tmp_path):
    meta = ut.load('.', _mkmanifest(tmp_path))
    assert ut.date_of(meta, 'content/b/[251231] 다.md') == '2025-12-31'
    assert ut.date_of(meta, 'content/b/무제.md') == ''


def test_section_of_is_empty_for_unknown_file(tmp_path):
    meta = ut.load('.', _mkmanifest(tmp_path))
    assert ut.section_of(meta, 'content/b/없다.md') == ''


import json as _json


def _mkclips(tmp_path):
    d = tmp_path / 'input' / 'clippings'
    d.mkdir(parents=True)
    io.open(str(d / 'Deep Dive.md'), 'w', encoding='utf-8').write(
        '---\ntitle: "Deep Dive"\nsource: "https://x"\n'
        'published: 2026-08-16\ncreated: 2026-08-17\n---\n본문.\n')
    io.open(str(d / 'No Published.md'), 'w', encoding='utf-8').write(
        '---\ntitle: "No Published"\ncreated: 2026-08-17\n---\n본문.\n')
    io.open(str(d / 'Bare.md'), 'w', encoding='utf-8').write('머리말 없다.\n')
    m = d / 'mer'
    m.mkdir()
    io.open(str(m / '111.json'), 'w', encoding='utf-8').write(_json.dumps(
        {'no': '111', 'date': '2024-04-03', 'text': '본문.'},
        ensure_ascii=False))
    io.open(str(m / '222.json'), 'w', encoding='utf-8').write(
        _json.dumps({'no': '222', 'text': '본문.'}, ensure_ascii=False))
    io.open(str(tmp_path / 'insights_manifest.json'), 'w',
            encoding='utf-8').write(_json.dumps(
                {'generated': '2026-08-28', 'sources': []}))
    return str(tmp_path), str(tmp_path / 'insights_manifest.json')


def test_clipping_date_prefers_published(tmp_path):
    root, _ = _mkclips(tmp_path)
    assert ut.clipping_date(root, 'input/clippings/Deep Dive.md') == '2026-08-16'


def test_clipping_date_falls_back_to_created(tmp_path):
    root, _ = _mkclips(tmp_path)
    assert ut.clipping_date(
        root, 'input/clippings/No Published.md') == '2026-08-17'


def test_clipping_date_is_empty_without_frontmatter(tmp_path):
    root, _ = _mkclips(tmp_path)
    assert ut.clipping_date(root, 'input/clippings/Bare.md') == ''


def test_clipping_date_reads_the_json_date(tmp_path):
    root, _ = _mkclips(tmp_path)
    assert ut.clipping_date(
        root, 'input/clippings/mer/111.json') == '2024-04-03'


def test_clipping_date_is_empty_when_the_json_has_none(tmp_path):
    root, _ = _mkclips(tmp_path)
    assert ut.clipping_date(root, 'input/clippings/mer/222.json') == ''


def test_load_fills_clipping_dates(tmp_path):
    root, man = _mkclips(tmp_path)
    meta = ut.load(root, man)
    assert meta['input/clippings/Deep Dive.md']['date'] == '2026-08-16'
    assert meta['input/clippings/mer/111.json']['date'] == '2024-04-03'


def test_clippings_have_no_freshness_section(tmp_path):
    root, man = _mkclips(tmp_path)
    meta = ut.load(root, man)
    assert meta['input/clippings/Deep Dive.md']['section'] == ''
