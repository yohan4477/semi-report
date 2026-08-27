import io
import json

import source_lines as sl


def _md(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'a.md'), 'w', encoding='utf-8').write(
        '첫 줄.\n둘째 줄.\n셋째 줄.\n')
    return str(tmp_path)


def _json(tmp_path, text='가.\n나.\n다.\n라.'):
    d = tmp_path / 'input' / 'clippings' / 'mer'
    d.mkdir(parents=True)
    io.open(str(d / '1.json'), 'w', encoding='utf-8').write(json.dumps(
        {'no': '1', 'title': '제목', 'date': '2024-04-03', 'text': text,
         'imgs': [], 'url': 'u', 'cat': '1', 'catname': '잡', 'comments': '0'},
        ensure_ascii=False))
    return str(tmp_path)


def test_markdown_lines_are_physical_lines(tmp_path):
    assert sl.lines(_md(tmp_path), 'content/a.md') == ['첫 줄.', '둘째 줄.', '셋째 줄.']


def test_markdown_line_endings_are_stripped(tmp_path):
    for line in sl.lines(_md(tmp_path), 'content/a.md'):
        assert not line.endswith('\n')


def test_json_lines_come_from_the_text_field(tmp_path):
    got = sl.lines(_json(tmp_path), 'input/clippings/mer/1.json')
    assert got == ['가.', '나.', '다.', '라.']


def test_json_ignores_the_other_keys(tmp_path):
    got = sl.lines(_json(tmp_path), 'input/clippings/mer/1.json')
    assert '제목' not in got
    assert '2024-04-03' not in got


def test_json_with_no_text_field_gives_nothing(tmp_path):
    d = tmp_path / 'input' / 'clippings' / 'mer'
    d.mkdir(parents=True)
    io.open(str(d / '2.json'), 'w', encoding='utf-8').write('{"no": "2"}')
    assert sl.lines(str(tmp_path), 'input/clippings/mer/2.json') == []


def test_broken_json_gives_nothing_instead_of_raising(tmp_path):
    d = tmp_path / 'input' / 'clippings' / 'mer'
    d.mkdir(parents=True)
    io.open(str(d / '3.json'), 'w', encoding='utf-8').write('{ not json')
    assert sl.lines(str(tmp_path), 'input/clippings/mer/3.json') == []


def test_missing_file_gives_nothing(tmp_path):
    assert sl.lines(str(tmp_path), 'content/없다.md') == []


def test_count_matches_the_line_list(tmp_path):
    root = _md(tmp_path)
    assert sl.count(root, 'content/a.md') == 3


def test_count_of_a_json_uses_the_text_field(tmp_path):
    assert sl.count(_json(tmp_path), 'input/clippings/mer/1.json') == 4


def test_line_at_counts_from_one(tmp_path):
    root = _md(tmp_path)
    assert sl.line_at(root, 'content/a.md', 1) == '첫 줄.'
    assert sl.line_at(root, 'content/a.md', 3) == '셋째 줄.'


def test_line_at_is_empty_outside_the_range(tmp_path):
    root = _md(tmp_path)
    assert sl.line_at(root, 'content/a.md', 0) == ''
    assert sl.line_at(root, 'content/a.md', 4) == ''


def test_line_at_strips_surrounding_space(tmp_path):
    d = tmp_path / 'content'
    d.mkdir()
    io.open(str(d / 'b.md'), 'w', encoding='utf-8').write('   가운데   \n')
    assert sl.line_at(str(tmp_path), 'content/b.md', 1) == '가운데'


def test_known_accepts_the_two_kinds_we_index():
    assert sl.known('content/a.md') is True
    assert sl.known('input/clippings/mer/1.json') is True


def test_known_rejects_anything_else():
    assert sl.known('content/a.txt') is False
    assert sl.known('content/a.html') is False
