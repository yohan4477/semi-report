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
