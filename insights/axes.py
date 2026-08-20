# -*- coding: utf-8 -*-
"""축 — 글 여럿이 하나의 사슬 위 어디에 서는가.

섹션 타일은 글을 주제별로 **나눈다.** 축은 반대로 주제를 **가로질러** 사슬 하나로
꿴다. 설계는 docs/superpowers/specs/2026-08-20-돈-고리-design.md.

**축은 칸만 갖는다.** 어느 글이 어느 칸에 서는지는 글이 자기 frontmatter 의
cell: 로 밝힌다 — 목록을 양쪽에 두면 진실의 출처가 둘이 된다.

축은 여럿일 수 있다. 41장을 다시 읽으면 최소 셋이 보인다(돈 고리 · 세는 기준 ·
병목의 이동). 지금 세우는 것은 돈 고리 하나이고 나머지는 자료구조만 열어 둔다.
같은 글이 여러 축에 서는 것은 허용한다 — 한 축 안에서 두 칸에 서는 것만 막는다.
"""

AXES = [{
    'id': 'money',
    'title': '자금이 도는 고리',
    'lede': '조달한 돈이 설비와 컴퓨트를 거쳐 매출이 되고, 그 매출이 다시 조달을 '
            '정당화하는지까지를 한 바퀴로 따라간다',
    'loop': [
        ('capital', '조달', '돈이 어디서 오나'),
        ('chip', '칩', '그 돈이 무엇으로 바뀌나'),
        ('power', '전기', '꽂을 데가 있나'),
        ('run', '가동', '산 것이 일하나'),
        ('sell', '판매', '얼마 남나'),
        ('back', '되돌아옴', '그래서 조달이 정당한가'),
    ],
    'outside': [
        ('money_cost', '돈값', '고리 전체가 서 있는 바깥 조건 — 금리와 환율'),
        ('estate', '부동산', '따로 서 있는 묶음 — 짓고 사고 파는 쪽'),
    ],
}]

BY_ID = dict((a['id'], a) for a in AXES)


def cells(axis_id):
    """(칸 id, 이름, 설명, 열) — 그리는 쪽과 검사하는 쪽이 같은 순서를 본다."""
    a = BY_ID.get(axis_id)
    if not a:
        return []
    out = [(c, n, g, 'loop') for c, n, g in a['loop']]
    out += [(c, n, g, 'outside') for c, n, g in a['outside']]
    return out


def cell_of(axis_id, cell_id):
    for c, n, g, _col in cells(axis_id):
        if c == cell_id:
            return (n, g)
    return None


def all_cell_ids():
    out = set()
    for a in AXES:
        for c, _n, _g, _col in cells(a['id']):
            out.add((a['id'], c))
    return out
