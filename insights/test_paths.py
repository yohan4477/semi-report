import os
import paths


def test_root_is_repo_root():
    assert os.path.isdir(os.path.join(paths.ROOT, 'insights'))
    assert os.path.isdir(os.path.join(paths.ROOT, 'content'))


def test_manifest_path_exists():
    assert os.path.isfile(paths.MAN)


def test_notes_dir_under_insights():
    assert paths.NOTES == os.path.join(paths.ROOT, 'insights', 'notes')


def test_cites_path_under_insights():
    assert paths.CITES == os.path.join(paths.ROOT, 'insights', 'cites.json')
