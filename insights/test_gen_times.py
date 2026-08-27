import io
import os

import gen_times as gt


def _mkroot(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / '[240927] 칠광구.md'), 'w', encoding='utf-8').write(
        '머리말.\n1965년 한일협정으로 시작됐다.\n2028년에 만료된다.\n'
        '작년보다 나빠졌다.\n점유율은 90%다.\n')
    io.open(str(d / '무제.md'), 'w', encoding='utf-8').write(
        '1999년에 있었다.\n')
    return str(tmp_path)


IDX = {
    '_meta': {'built': '2026-08-28', 'files': 2, 'lines': 6,
              'fingerprint': 'abc123'},
    '칠광구': ['content/[240927] 칠광구.md#L2', 'content/[240927] 칠광구.md#L3',
             'content/[240927] 칠광구.md#L4', 'content/[240927] 칠광구.md#L5',
             'content/무제.md#L1'],
}
META = {}


def test_indexed_lines_groups_by_file():
    got = gt.indexed_lines(IDX)
    assert got['content/무제.md'] == {1}
    assert got['content/[240927] 칠광구.md'] == {2, 3, 4, 5}


def test_indexed_lines_skips_meta():
    assert '_meta' not in gt.indexed_lines(IDX)


def test_build_marks_explicit_retrospect(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert out['content/[240927] 칠광구.md#L2'] == {
        't': '1965', 'how': '명시', 'tense': '회고'}


def test_build_marks_explicit_forecast(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert out['content/[240927] 칠광구.md#L3']['tense'] == '전망'


def test_build_marks_computed_line(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert out['content/[240927] 칠광구.md#L4'] == {
        't': '2023', 'how': '계산', 'tense': '회고'}


def test_build_omits_lines_without_a_marker(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert 'content/[240927] 칠광구.md#L5' not in out


def test_build_omits_files_with_no_utterance_date(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert 'content/무제.md#L1' not in out


def test_build_carries_the_index_fingerprint(tmp_path):
    out = gt.build(_mkroot(tmp_path), IDX, META)
    assert out['_meta']['index_fingerprint'] == 'abc123'
    assert out['_meta']['lines'] == 3


def test_build_is_deterministic(tmp_path):
    root = _mkroot(tmp_path)
    assert gt.build(root, IDX, META) == gt.build(root, IDX, META)


def test_build_prefers_manifest_date_over_the_filename(tmp_path):
    root = _mkroot(tmp_path)
    meta = {'content/[240927] 칠광구.md':
            {'date': '2030-01-01', 'section': 'biz'}}
    out = gt.build(root, IDX, meta)
    assert out['content/[240927] 칠광구.md#L3']['tense'] == '회고'


def test_build_skips_an_address_whose_file_is_gone(tmp_path):
    root = _mkroot(tmp_path)
    idx = dict(IDX)
    idx['칠광구'] = list(IDX['칠광구']) + ['content/없다.md#L1']
    out = gt.build(root, idx, META)
    assert 'content/없다.md#L1' not in out
