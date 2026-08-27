import io
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import bench_index as bi  # noqa: E402


def _mkroot(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(
        '램리서치가 왔다.\nLam Research shipped.\n무관한 줄.\n')
    return str(tmp_path)


IDX = {
    '_meta': {'built': '2026-08-27', 'files': 1, 'lines': 3,
              'fingerprint': 'abc'},
    '램리서치': ['content/a.md#L1', 'content/a.md#L2'],
}


def test_grep_hits_finds_only_the_literal(tmp_path):
    got = bi.grep_hits(_mkroot(tmp_path), ['램리서치'])
    assert got == ['content/a.md#L1']


def test_compare_reports_index_superset(tmp_path):
    r = bi.compare(_mkroot(tmp_path), IDX,
                   {'entity': '램리서치', 'needles': ['램리서치']})
    assert r['grep'] == 1
    assert r['index'] == 2
    assert r['index_only'] == ['content/a.md#L2']
    assert r['grep_only'] == []
    assert r['covers'] is True


def test_compare_flags_when_index_misses_a_grep_hit(tmp_path):
    idx = dict(IDX)
    idx['램리서치'] = ['content/a.md#L2']
    r = bi.compare(_mkroot(tmp_path), idx,
                   {'entity': '램리서치', 'needles': ['램리서치']})
    assert r['grep_only'] == ['content/a.md#L1']
    assert r['covers'] is False
