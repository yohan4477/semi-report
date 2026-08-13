import check_notes as cn

GOOD = '''---
source: "insights/world_path.txt"
date: 2026-08-07
---

## 이 문서가 주장하는 것

무언가를 주장한다.

## 수치

- 2GW · 2026년 말 기준 · 업체 발표 (world_path L1)
'''

BAD_SRC = GOOD.replace('insights/world_path.txt', 'insights/없는파일.txt')
BAD_LABEL = GOOD.replace('(world_path L1)', '(엉뚱한이름 L1)')
BAD_LINE = GOOD.replace('(world_path L1)', '(world_path L9999999)')
NO_CITE = GOOD.replace(' (world_path L1)', '')


def _rules(text, path='insights/notes/x.md'):
    return {f[2] for f in cn.check_file(path, text, {})}


def test_good_note_has_no_findings():
    assert _rules(GOOD) == set()


def test_missing_source_file_fails():
    assert 'N1' in _rules(BAD_SRC)


def test_unresolved_label_fails():
    assert 'N2' in _rules(BAD_LABEL)


def test_line_past_eof_fails():
    assert 'N3' in _rules(BAD_LINE)


def test_hash_mismatch_warns():
    lock = {'insights/world_path.txt#L1': {'sha1': 'deadbeefdead'}}
    rules = {f[2] for f in cn.check_file('insights/notes/x.md', GOOD, lock)}
    assert 'N4' in rules


def test_oversize_note_warns():
    big = GOOD + ('가' * 3200)
    assert 'N5' in _rules(big)


def test_oversize_track_is_allowed():
    # 3KB 상한은 노트에만. 추적·인사이트 서술은 원래 길다
    big = GOOD + ('가' * 3200)
    assert 'N5' not in _rules(big, 'insights/tracks/musk.md')


def test_numbers_row_without_cite_fails():
    assert 'N6' in _rules(NO_CITE)


def test_levels_are_correct():
    lv = {f[2]: f[0] for f in cn.check_file('insights/notes/x.md', BAD_SRC, {})}
    assert lv['N1'] == 'FAIL'
