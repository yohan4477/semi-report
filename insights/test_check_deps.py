import io
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import check_deps as cd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _tree(tmp_path, files):
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        io.open(str(p), 'w', encoding='utf-8').write(text)
    return str(tmp_path)


def test_imports_of_finds_both_forms(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'import foo\nfrom bar import x\n'})
    assert set(cd.imports_of(root, 'scripts/a.py')) == {'foo', 'bar'}


def test_imports_of_ignores_indented_and_commented(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': '# import foo\nx = 1  # from bar import y\n'})
    assert cd.imports_of(root, 'scripts/a.py') == []


def test_imports_of_reads_indented_import_inside_a_function(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'def f():\n    import foo\n'})
    assert cd.imports_of(root, 'scripts/a.py') == ['foo']


def test_where_resolves_a_module_in_the_repo(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': '', 'scratchpad/b.py': ''})
    assert cd.where(root, 'b') == os.path.join('scratchpad', 'b.py')


def test_where_returns_none_for_a_library(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': ''})
    assert cd.where(root, 'json') is None


def test_clean_repo_reports_nothing(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'import b\n', 'scripts/b.py': ''})
    tracked = {os.path.join('scripts', 'a.py'), os.path.join('scripts', 'b.py')}
    assert cd.untracked_deps(root, tracked) == {}


def test_untracked_dependency_is_reported_with_its_caller(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'import b\n', 'scratchpad/b.py': ''})
    tracked = {os.path.join('scripts', 'a.py')}
    got = cd.untracked_deps(root, tracked)
    assert list(got) == [os.path.join('scratchpad', 'b.py')]
    assert got[os.path.join('scratchpad', 'b.py')] == [os.path.join('scripts', 'a.py')]


def test_closure_follows_an_untracked_chain(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'import b\n',
                            'scratchpad/b.py': 'import c\n',
                            'scratchpad/c.py': ''})
    got = cd.untracked_deps(root, {os.path.join('scripts', 'a.py')})
    assert set(got) == {os.path.join('scratchpad', 'b.py'),
                        os.path.join('scratchpad', 'c.py')}


def test_untracked_file_that_nobody_tracked_calls_is_ignored(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': '', 'scratchpad/junk.py': 'import os\n'})
    assert cd.untracked_deps(root, {os.path.join('scripts', 'a.py')}) == {}


def test_a_module_importing_itself_does_not_hang(tmp_path):
    root = _tree(tmp_path, {'scripts/a.py': 'import b\n', 'scratchpad/b.py': 'import b\n'})
    got = cd.untracked_deps(root, {os.path.join('scripts', 'a.py')})
    assert list(got) == [os.path.join('scratchpad', 'b.py')]


def test_callers_are_sorted_and_unique(tmp_path):
    root = _tree(tmp_path, {'scripts/z.py': 'import b\n',
                            'scripts/a.py': 'import b\nimport b\n',
                            'scratchpad/b.py': ''})
    tracked = {os.path.join('scripts', 'a.py'), os.path.join('scripts', 'z.py')}
    got = cd.untracked_deps(root, tracked)
    assert got[os.path.join('scratchpad', 'b.py')] == [
        os.path.join('scripts', 'a.py'), os.path.join('scripts', 'z.py')]


def test_the_real_repo_has_no_untracked_dependency():
    """036ef2b 에서 다섯을 추적에 넣었다. 다시 새면 여기서 걸린다."""
    assert cd.untracked_deps(ROOT, cd.tracked(ROOT)) == {}
