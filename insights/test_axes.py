# -*- coding: utf-8 -*-
import io
import os
import notes_lib as nl
import paths

LI = 'content/linkedin/[2608] 링크드인 게시물.md'


def _abs(rel):
    return os.path.join(paths.ROOT, rel.replace('/', os.sep))


def test_li_basis_reads_the_block_the_line_belongs_to():
    text = io.open(_abs(LI), encoding='utf-8').read().split('\n')
    # 「기준일」 줄을 하나 찾고, 그보다 아래 줄의 기준일이 같은 값이어야 한다
    idx = next(i for i, l in enumerate(text) if l.startswith('- 기준일 '))
    want = text[idx].split('기준일 ')[1].split()[0]
    assert nl.li_basis(LI, idx + 3) == want


def test_li_basis_returns_none_for_non_linkedin():
    assert nl.li_basis('content/newsletter/ai_infra/x.md', 10) is None


def test_loop_path_is_under_insights():
    assert paths.LOOP == os.path.join(paths.ROOT, 'insights', 'loop')
    assert os.path.isdir(paths.LOOP)


import axes


def test_money_axis_has_six_loop_cells_and_two_outside():
    rows = axes.cells('money')
    loop = [r for r in rows if r[3] == 'loop']
    out = [r for r in rows if r[3] == 'outside']
    assert [r[0] for r in loop] == ['capital', 'chip', 'power', 'run', 'sell', 'back']
    assert [r[0] for r in out] == ['money_cost', 'estate']


def test_cell_of_returns_name_and_gloss():
    name, gloss = axes.cell_of('money', 'capital')
    assert name == '조달'
    assert gloss


def test_cell_of_unknown_is_none():
    assert axes.cell_of('money', 'nope') is None


# shape 없는 기존 축은 loop로 읽힌다
def test_money_shape_defaults_to_loop():
    assert axes.shape_of('money') == 'loop'


def test_measure_shape_defaults_to_loop():
    assert axes.shape_of('measure') == 'loop'


def test_edges_of_and_flow_of_empty_for_axes_without_them():
    assert axes.edges_of('money') == []
    assert axes.flow_of('money') == []


# 가짜 merge 축 — rates 축 자료는 별도 커밋에서 들어온다. 자료구조만 여기서 시험한다.
_FAKE_MERGE = {
    'id': 'zz_fake_merge',
    'shape': 'merge',
    'title': '가짜 합류 축',
    'lede': '시험용',
    'outer': [('a1', '바깥1', '바깥1 설명'), ('a2', '바깥2', '바깥2 설명')],
    'price': [('p1', '값1', '값1 설명')],
    'merge': ('m1', '합류', '합류 설명'),
    'edges': [('a1', 'p1', '+', '근거 한 줄', '가짜노트.md', 3)],
    'flow': [('01-01', '첫 정거장', '가짜노트.md')],
}


def _with_fake_axis():
    axes.AXES.append(_FAKE_MERGE)
    axes.BY_ID['zz_fake_merge'] = _FAKE_MERGE


def _without_fake_axis():
    if _FAKE_MERGE in axes.AXES:
        axes.AXES.remove(_FAKE_MERGE)
    axes.BY_ID.pop('zz_fake_merge', None)


def test_merge_axis_cells_has_outer_price_merge_columns():
    _with_fake_axis()
    try:
        rows = axes.cells('zz_fake_merge')
        cols = [r[3] for r in rows]
        assert cols == ['outer', 'outer', 'price', 'merge']
        ids = [r[0] for r in rows]
        assert ids == ['a1', 'a2', 'p1', 'm1']
    finally:
        _without_fake_axis()


def test_merge_axis_cell_of_and_all_cell_ids():
    _with_fake_axis()
    try:
        name, gloss = axes.cell_of('zz_fake_merge', 'm1')
        assert name == '합류'
        assert gloss
        assert ('zz_fake_merge', 'm1') in axes.all_cell_ids()
        assert ('zz_fake_merge', 'a1') in axes.all_cell_ids()
    finally:
        _without_fake_axis()


def test_merge_axis_shape_edges_flow_helpers():
    _with_fake_axis()
    try:
        assert axes.shape_of('zz_fake_merge') == 'merge'
        assert axes.edges_of('zz_fake_merge') == [
            ('a1', 'p1', '+', '근거 한 줄', '가짜노트.md', 3)]
        assert axes.flow_of('zz_fake_merge') == [('01-01', '첫 정거장', '가짜노트.md')]
    finally:
        _without_fake_axis()


def test_shape_of_unknown_axis_defaults_to_loop():
    assert axes.shape_of('nope-no-such-axis') == 'loop'
