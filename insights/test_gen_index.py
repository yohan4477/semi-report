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


def _read(root, rel):
    return io.open(os.path.join(root, rel.replace('/', os.sep)),
                   encoding='utf-8').read()


def _write(root, rel, text):
    io.open(os.path.join(root, rel.replace('/', os.sep)), 'w',
            encoding='utf-8').write(text)


def test_file_hashes_gives_one_digest_per_file(tmp_path):
    root = _mkcorpus(tmp_path)
    got = gi.file_hashes(root, gi.corpus_files(root))
    assert sorted(got) == ['content/sub/a.md', 'content/sub/b.md']
    assert got['content/sub/a.md'] != got['content/sub/b.md']


def test_file_hashes_change_only_for_the_touched_file(tmp_path):
    root = _mkcorpus(tmp_path)
    files = gi.corpus_files(root)
    before = gi.file_hashes(root, files)
    _write(root, 'content/sub/a.md', _read(root, 'content/sub/a.md') + '또.\n')
    after = gi.file_hashes(root, files)
    assert after['content/sub/a.md'] != before['content/sub/a.md']
    assert after['content/sub/b.md'] == before['content/sub/b.md']


def test_fingerprint_is_derived_from_the_per_file_hashes(tmp_path):
    root = _mkcorpus(tmp_path)
    files = gi.corpus_files(root)
    assert gi.fingerprint(root, files) == gi.fingerprint_of(
        gi.file_hashes(root, files))


def test_entities_hash_tracks_the_dictionary(tmp_path):
    other = ROWS + [{'canonical': '마이크론', 'type': '회사',
                     'ko': ['마이크론'], 'en': [], 'deny': []}]
    assert gi.entities_hash(ROWS) == gi.entities_hash(list(ROWS))
    assert gi.entities_hash(ROWS) != gi.entities_hash(other)


def test_build_records_what_it_needs_to_go_incremental(tmp_path):
    root = _mkcorpus(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    stat = idx['_meta']['files_stat']
    assert sorted(stat) == ['content/sub/a.md', 'content/sub/b.md']
    assert stat['content/sub/a.md'][1] == 3          # 줄 수
    assert idx['_meta']['entities_hash'] == gi.entities_hash(ROWS)


def test_incremental_matches_a_full_rebuild_after_an_edit(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    _write(root, 'content/sub/b.md',
           'Lam Research holds share.\n엔비디아도 왔다.\n')
    files = gi.corpus_files(root)
    assert gi.build(root, ROWS, files, old) == gi.build(root, ROWS, files)


def test_incremental_matches_a_full_rebuild_after_a_new_file(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    _write(root, 'content/sub/d.md', '엔비디아가 또 샀다.\n')
    files = gi.corpus_files(root)
    assert gi.build(root, ROWS, files, old) == gi.build(root, ROWS, files)


def test_incremental_matches_a_full_rebuild_after_a_deletion(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    os.remove(os.path.join(root, 'content', 'sub', 'b.md'))
    files = gi.corpus_files(root)
    assert gi.build(root, ROWS, files, old) == gi.build(root, ROWS, files)


def test_incremental_reads_only_the_changed_file(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    _write(root, 'content/sub/b.md', 'Lam Research holds share.\n엔비디아.\n')
    seen = []
    real = gi.scan

    def spy(r, rows, files):
        seen.extend(files)
        return real(r, rows, files)

    gi.scan = spy
    try:
        gi.build(root, ROWS, gi.corpus_files(root), old)
    finally:
        gi.scan = real
    assert seen == ['content/sub/b.md']


def test_a_changed_dictionary_forces_a_full_rebuild(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    rows = ROWS + [{'canonical': '마이크론', 'type': '회사',
                    'ko': ['첫 줄'], 'en': [], 'deny': []}]
    seen = []
    real = gi.scan

    def spy(r, r2, files):
        seen.extend(files)
        return real(r, r2, files)

    gi.scan = spy
    try:
        idx = gi.build(root, rows, gi.corpus_files(root), old)
    finally:
        gi.scan = real
    assert seen == ['content/sub/a.md', 'content/sub/b.md']
    assert idx['마이크론'] == ['content/sub/a.md#L1']


def test_incremental_drops_a_hit_that_the_edit_removed(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    assert '램리서치' in old
    _write(root, 'content/sub/a.md', '첫 줄이다.\n엔비디아가 샀다.\n엔비디아.\n')
    _write(root, 'content/sub/b.md', '아무 회사도 없다.\n')
    idx = gi.build(root, ROWS, gi.corpus_files(root), old)
    assert '램리서치' not in idx
    assert idx['엔비디아'] == ['content/sub/a.md#L2', 'content/sub/a.md#L3']


def test_incremental_keeps_line_count_in_sync(tmp_path):
    root = _mkcorpus(tmp_path)
    old = gi.build(root, ROWS, gi.corpus_files(root))
    _write(root, 'content/sub/b.md', 'Lam Research.\n또.\n또.\n')
    idx = gi.build(root, ROWS, gi.corpus_files(root), old)
    assert idx['_meta']['lines'] == 6


def _mkwide(tmp_path):
    import json as _json
    c = tmp_path / 'content' / 'sub'
    c.mkdir(parents=True)
    io.open(str(c / 'a.md'), 'w', encoding='utf-8').write('엔비디아가 샀다.\n')
    e = tmp_path / 'input' / 'clippings'
    e.mkdir(parents=True)
    io.open(str(e / 'Deep Dive.md'), 'w', encoding='utf-8').write(
        'NVIDIA ships Blackwell.\n램리서치도 나온다.\n')
    m = e / 'mer'
    m.mkdir()
    io.open(str(m / '111.json'), 'w', encoding='utf-8').write(_json.dumps(
        {'no': '111', 'date': '2024-04-03',
         'text': '머리말.\n엔비디아 이야기.\n끝.'}, ensure_ascii=False))
    io.open(str(e / '메모.txt'), 'w', encoding='utf-8').write('엔비디아\n')
    return str(tmp_path)


def test_corpus_takes_all_three_kinds(tmp_path):
    got = gi.corpus_files(_mkwide(tmp_path))
    assert got == ['content/sub/a.md',
                   'input/clippings/Deep Dive.md',
                   'input/clippings/mer/111.json']


def test_corpus_leaves_out_kinds_we_cannot_read(tmp_path):
    for p in gi.corpus_files(_mkwide(tmp_path)):
        assert not p.endswith('.txt')


def test_corpus_does_not_take_clipping_md_as_a_mer_file(tmp_path):
    got = gi.corpus_files(_mkwide(tmp_path))
    assert got.count('input/clippings/Deep Dive.md') == 1


def test_build_indexes_a_clipping_json_by_its_text_lines(tmp_path):
    root = _mkwide(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    # 영문 클리핑 1줄의 NVIDIA 도 같은 정본에 걸린다
    assert idx['엔비디아'] == ['content/sub/a.md#L1',
                            'input/clippings/Deep Dive.md#L1',
                            'input/clippings/mer/111.json#L2']


def test_build_indexes_an_english_clipping(tmp_path):
    root = _mkwide(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert 'input/clippings/Deep Dive.md#L1' in idx['엔비디아']
    assert idx['램리서치'] == ['input/clippings/Deep Dive.md#L2']


def test_meta_line_count_uses_body_lines_not_physical_lines(tmp_path):
    root = _mkwide(tmp_path)
    idx = gi.build(root, ROWS, gi.corpus_files(root))
    assert idx['_meta']['lines'] == 6
