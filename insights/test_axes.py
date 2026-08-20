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
