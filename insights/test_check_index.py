import io

import check_index as ci
import gen_index as gi


ROWS = [{'canonical': '엔비디아', 'type': '회사',
         'ko': ['엔비디아'], 'en': ['NVIDIA'], 'deny': []}]


def _mkcorpus(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write('엔비디아.\n둘째 줄.\n')
    return str(tmp_path)


def _rules(out):
    return {r for _, r, _ in out}


def test_clean_index_has_no_findings(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert ci.check(root, ROWS, idx, {'엔비디아'}) == []


def test_x1_fires_when_corpus_changed_after_build(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    io.open(str(tmp_path / 'content' / 'b.md'), 'w',
            encoding='utf-8').write('엔비디아 또.\n')
    out = ci.check(root, ROWS, idx, {'엔비디아'})
    assert 'X1' in _rules(out)
    assert all(lvl == 'FAIL' for lvl, r, _ in out if r == 'X1')


def test_x2_fires_on_bad_dictionary(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    bad = [{'canonical': '엔비디아', 'type': '반도체회사',
            'ko': ['엔비디아'], 'en': [], 'deny': []}]
    assert 'X2' in _rules(ci.check(root, bad, idx, {'엔비디아'}))


def test_x3_fires_on_missing_file(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    idx['엔비디아'].append('content/없는파일.md#L1')
    assert 'X3' in _rules(ci.check(root, ROWS, idx, {'엔비디아'}))


def test_x4_fires_on_line_past_eof(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    idx['엔비디아'].append('content/a.md#L999')
    assert 'X4' in _rules(ci.check(root, ROWS, idx, {'엔비디아'}))


def test_x5_warns_on_actor_missing_from_dictionary(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    out = ci.check(root, ROWS, idx, {'엔비디아', '마이크론'})
    assert 'X5' in _rules(out)
    assert all(lvl == 'WARN' for lvl, r, _ in out if r == 'X5')


META1 = {'content/a.md': {'date': '2026-01-01', 'section': ''}}


def _mktimes(fp):
    """fp 는 색인의 진짜 지문이어야 한다 — 아니면 X8 이 같이 운다."""
    return {
        '_meta': {'built': '2026-08-28', 'index_fingerprint': fp, 'lines': 1},
        'content/a.md#L1': {'t': '2020', 'how': '명시', 'tense': '회고'},
    }


def _idx_and_times(tmp_path):
    """지문을 손대지 않는다. X1 은 진짜 코퍼스와 대조하므로 덮어쓰면 같이 운다."""
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    return root, idx, _mktimes(idx['_meta']['fingerprint'])


def test_time_checks_are_skipped_when_no_times_given(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert ci.check(root, ROWS, idx, {'엔비디아'}) == []


def test_clean_times_have_no_findings(tmp_path):
    root, idx, tmap = _idx_and_times(tmp_path)
    assert ci.check(root, ROWS, idx, {'엔비디아'}, tmap, META1) == []


def test_x6_fires_on_an_impossible_year(tmp_path):
    root, idx, tmap = _idx_and_times(tmp_path)
    tmap['content/a.md#L1']['t'] = '1200'
    out = ci.check(root, ROWS, idx, {'엔비디아'}, tmap, META1)
    assert 'X6' in _rules(out)
    assert 'X1' not in _rules(out)


def test_x6_fires_on_a_year_too_far_ahead(tmp_path):
    root, idx, tmap = _idx_and_times(tmp_path)
    tmap['content/a.md#L1']['t'] = '2400'
    assert 'X6' in _rules(ci.check(root, ROWS, idx, {'엔비디아'}, tmap, META1))


def test_x7_fires_on_an_address_absent_from_the_index(tmp_path):
    root, idx, tmap = _idx_and_times(tmp_path)
    tmap['content/a.md#L2'] = {'t': '2020', 'how': '명시', 'tense': '회고'}
    assert 'X7' in _rules(ci.check(root, ROWS, idx, {'엔비디아'}, tmap, META1))


def test_x8_fires_when_times_is_older_than_the_index(tmp_path):
    root, idx, _ = _idx_and_times(tmp_path)
    stale = _mktimes('deadbeef')
    out = ci.check(root, ROWS, idx, {'엔비디아'}, stale, META1)
    assert 'X8' in _rules(out)
    assert all(lvl == 'FAIL' for lvl, r, _ in out if r == 'X8')
