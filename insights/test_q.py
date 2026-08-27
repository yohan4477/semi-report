import io
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import q  # noqa: E402


def _mkroot(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(
        '머리말.\n램리서치는 점유율 90% 이상이다.\n셋째 줄.\n')
    return str(tmp_path)


IDX = {
    '_meta': {'built': '2026-08-27', 'files': 1, 'lines': 3,
              'fingerprint': 'abc123'},
    '램리서치': ['content/a.md#L2'],
}


def test_lookup_reads_the_cited_line(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치')
    assert r['rows'][0]['addr'] == 'content/a.md#L2'
    assert '점유율 90%' in r['rows'][0]['text']


def test_lookup_counts_files(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치')
    assert r['files'] == 1
    assert r['total'] == 1


def test_lookup_carries_index_receipt(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치')
    assert r['built'] == '2026-08-27'
    assert r['fingerprint'] == 'abc123'


def test_lookup_reports_cut_when_over_cap(tmp_path):
    root = _mkroot(tmp_path)
    idx = dict(IDX)
    idx['램리서치'] = ['content/a.md#L2'] * 5
    r = q.lookup(root, idx, '램리서치', cap=2)
    assert r['total'] == 5
    assert r['shown'] == 2
    assert r['cut'] == 3


def test_lookup_reports_no_cut_when_under_cap(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치', cap=40)
    assert r['cut'] == 0


def test_lookup_on_unknown_name_is_empty_not_error(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '없는회사')
    assert r['total'] == 0
    assert r['rows'] == []


def test_render_shows_cut_count(tmp_path):
    root = _mkroot(tmp_path)
    idx = dict(IDX)
    idx['램리서치'] = ['content/a.md#L2'] * 5
    text = q.render(q.lookup(root, idx, '램리서치', cap=2))
    assert '3' in text
    assert '잘림' in text


def test_render_shows_index_date(tmp_path):
    text = q.render(q.lookup(_mkroot(tmp_path), IDX, '램리서치'))
    assert '2026-08-27' in text


TMAP = {
    '_meta': {'built': '2026-08-28', 'index_fingerprint': 'abc123', 'lines': 1},
    'content/a.md#L2': {'t': '1965', 'how': '명시', 'tense': '회고'},
}
META = {'content/a.md': {'date': '2024-09-27', 'section': 'biz'}}
TODAY = '2026-08-28'


def test_stale_limit_uses_the_shared_table():
    assert q.stale_limit('biz') == 120
    assert q.stale_limit('power') == 365
    assert q.stale_limit('') == 180


def test_lookup_attaches_the_recorded_time(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap=TMAP, meta=META, today=TODAY)
    row = r['rows'][0]
    assert row['tense'] == '회고'
    assert row['t'] == '1965'
    assert row['how'] == '명시'
    assert row['utter'] == '2024-09-27'


def test_lookup_inherits_the_utterance_date_when_no_time_recorded(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap={'_meta': {}}, meta=META, today=TODAY)
    row = r['rows'][0]
    assert row['how'] == '상속'
    assert row['t'] == '2024'
    assert row['tense'] == '현재'


def test_lookup_never_marks_a_retrospect_line_stale(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap=TMAP, meta=META, today=TODAY)
    assert r['rows'][0]['stale'] is False


def test_lookup_marks_an_old_present_line_stale(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap={'_meta': {}}, meta=META, today=TODAY)
    assert r['rows'][0]['stale'] is True


def test_lookup_keeps_a_recent_present_line_fresh(tmp_path):
    meta = {'content/a.md': {'date': '2026-08-01', 'section': 'biz'}}
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap={'_meta': {}}, meta=meta, today=TODAY)
    assert r['rows'][0]['stale'] is False


def test_lookup_counts_tenses_in_the_receipt(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                 tmap=TMAP, meta=META, today=TODAY)
    assert r['tense_counts'] == {'회고': 1}


def test_lookup_without_times_behaves_as_before(tmp_path):
    r = q.lookup(_mkroot(tmp_path), IDX, '램리서치')
    assert r['rows'][0]['addr'] == 'content/a.md#L2'
    assert r['total'] == 1


def test_render_shows_tense_and_year(tmp_path):
    text = q.render(q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                             tmap=TMAP, meta=META, today=TODAY))
    assert '회고' in text
    assert '1965' in text
    assert '명시' in text


def test_render_marks_a_stale_line(tmp_path):
    text = q.render(q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                             tmap={'_meta': {}}, meta=META, today=TODAY))
    assert '낡음' in text


def test_render_receipt_reports_tense_counts(tmp_path):
    text = q.render(q.lookup(_mkroot(tmp_path), IDX, '램리서치',
                             tmap=TMAP, meta=META, today=TODAY))
    assert '회고 1' in text
