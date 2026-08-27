import io
import os

import gen_index as gi


ROWS = [
    {'canonical': '램리서치', 'type': '회사',
     'ko': ['램리서치'], 'en': ['Lam Research'], 'deny': []},
    {'canonical': '엔비디아', 'type': '회사',
     'ko': ['엔비디아'], 'en': ['NVIDIA'], 'deny': []},
]


def _mkcorpus(tmp_path):
    d = tmp_path / 'content' / 'sub'
    d.mkdir(parents=True)
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(
        '첫 줄이다.\n엔비디아가 샀다.\n램리서치와 엔비디아.\n')
    io.open(str(d / 'b.md'), 'w', encoding='utf-8').write(
        'Lam Research holds share.\n')
    io.open(str(d / 'c.txt'), 'w', encoding='utf-8').write('엔비디아\n')
    return str(tmp_path)


def test_corpus_files_takes_only_md_under_content(tmp_path):
    root = _mkcorpus(tmp_path)
    got = gi.corpus_files(root)
    assert got == ['content/sub/a.md', 'content/sub/b.md']


def test_corpus_files_uses_forward_slashes(tmp_path):
    for p in gi.corpus_files(_mkcorpus(tmp_path)):
        assert '\\' not in p


def test_build_records_line_addresses(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert idx['엔비디아'] == ['content/sub/a.md#L2', 'content/sub/a.md#L3']
    assert idx['램리서치'] == ['content/sub/a.md#L3', 'content/sub/b.md#L1']


def test_build_omits_entities_with_no_hit(tmp_path):
    root = _mkcorpus(tmp_path)
    rows = ROWS + [{'canonical': '마이크론', 'type': '회사',
                    'ko': ['마이크론'], 'en': [], 'deny': []}]
    idx = gi.build(root, rows, gi.corpus_files(root))
    assert '마이크론' not in idx


def test_build_meta_counts_files_and_lines(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert idx['_meta']['files'] == 2
    assert idx['_meta']['lines'] == 4


def test_build_is_deterministic(tmp_path):
    root = _mkcorpus(tmp_path)
    files = gi.corpus_files(root)
    a = gi.build(root, ROWS, files)
    b = gi.build(root, ROWS, files)
    assert a == b


def test_fingerprint_changes_when_a_file_changes(tmp_path):
    root = _mkcorpus(tmp_path)
    files = gi.corpus_files(root)
    before = gi.fingerprint(root, files)
    io.open(os.path.join(root, 'content', 'sub', 'a.md'), 'a',
            encoding='utf-8').write('엔비디아 또.\n')
    assert gi.fingerprint(root, files) != before


def test_fingerprint_changes_when_a_file_is_added(tmp_path):
    root = _mkcorpus(tmp_path)
    before = gi.fingerprint(root, gi.corpus_files(root))
    io.open(os.path.join(root, 'content', 'sub', 'd.md'), 'w',
            encoding='utf-8').write('엔비디아.\n')
    assert gi.fingerprint(root, gi.corpus_files(root)) != before


def test_index_holds_addresses_not_text(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    for addr in idx['엔비디아']:
        assert '#L' in addr
        assert '샀다' not in addr
