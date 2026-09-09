# -*- coding: utf-8 -*-
"""수식을 분해 트리로 그린다. 색은 회색만(확정 규칙 S2).

식을 줄로 늘어놓으면 어느 항이 어느 항을 낳는지가 안 보인다. 왼쪽에 결과를
두고 오른쪽으로 갈수록 잘게 쪼갠 상자로 세우면, 한 칸이 어긋났을 때 그 위로
무엇이 흔들리는지가 눈에 든다.

판에는 이름만 둔다 — 값은 바로 아래 수식 블록과 표가 낸다. 좌표는 `_place`
가 계산한다. 손으로 찍지 않는다(yohan-figure 규칙 2).
"""
import _biz_fig as bf

_svg, _r, _t, _lt = bf._svg, bf.sudo._r, bf.sudo._t, bf._lt
W = 640
PITCH = 46          # 잎 상자 한 칸의 세로 간격
TOP = 44            # 첫 잎의 위 여백
BH = 34             # 상자 높이
GAP = 34            # 열과 열 사이. 연산자 동그라미가 이 사이에 선다


def _node(label, op=None, kids=()):
    return {'l': label, 'op': op, 'k': list(kids)}


def _depth(n):
    return 1 + max([_depth(k) for k in n['k']] or [0])


def _place(node, cols, depth=0, slot=[0]):
    """잎에 차례로 자리를 주고, 어미는 자식들의 한가운데에 놓는다."""
    x, w = cols[depth]
    if not node['k']:
        y = TOP + slot[0] * PITCH
        slot[0] += 1
    else:
        for k in node['k']:
            _place(k, cols, depth + 1, slot)
        y = (node['k'][0]['y'] + node['k'][-1]['y']) // 2
    node['x'], node['y'], node['w'] = x, y, w
    return node


def _cols(widths):
    """열마다 (왼쪽 x, 폭). 전체를 판 가운데에 맞춘다."""
    total = sum(widths) + GAP * (len(widths) - 1)
    x0 = (W - total) // 2
    out, x = [], x0
    for w in widths:
        out.append((x, w))
        x += w + GAP
    return out


def _draw(node, out):
    """상자와 잇는 선. 연산자는 자식들을 묶는 세로선 위에 동그라미로 얹는다."""
    x, y, w = node['x'], node['y'], node['w']
    out.append(_r(x, y - BH // 2, w, BH))
    for i, s in enumerate(node['l']):
        out.append(_t(x + w // 2, y - BH // 2 + (BH - (len(node['l']) - 1) * 15) // 2
                      + i * 15 + 5, s, 't-lab' if i == 0 else 't-sm'))
    if not node['k']:
        return
    bx = x + w + GAP // 2
    top, bot = node['k'][0]['y'], node['k'][-1]['y']
    out.append('<path d="M%d %d H%d" stroke="var(--ink-3)" stroke-width="1.5" '
               'fill="none"/>' % (x + w, y, bx))
    out.append('<path d="M%d %d V%d" stroke="var(--ink-3)" stroke-width="1.5" '
               'fill="none"/>' % (bx, top, bot))
    for k in node['k']:
        out.append('<path d="M%d %d H%d" stroke="var(--ink-3)" stroke-width="1.5" '
                   'fill="none"/>' % (bx, k['y'], k['x']))
    if node['op']:
        out.append('<circle cx="%d" cy="%d" r="12" fill="var(--paper)" '
                   'stroke="var(--ink-3)" stroke-width="1.5"/>' % (bx, y))
        out.append(_t(bx, y + 5, node['op'], 't-lab'))
    for k in node['k']:
        _draw(k, out)


def tree_svg(label, widths, root, marks=()):
    """분해 트리 하나. marks 는 (상자 라벨 첫 줄, 번호) — 캡션이 그 번호를 푼다.

    번호는 상자 왼쪽 위 모서리에 걸친다. 상자 밖 왼쪽에 두면 잇는 선과 겹치고,
    어느 상자를 가리키는지가 한 칸 떨어져 흐려진다.
    """
    cols = _cols(widths)
    _place(root, cols, 0, [0])
    out = []
    _draw(root, out)
    seen = {}

    def _walk(n):
        seen[n['l'][0]] = n
        for k in n['k']:
            _walk(k)
    _walk(root)
    for lab, num in marks:
        n = seen[lab]
        out.append(bf._mark(n['x'], n['y'] - BH // 2, num))
    leaves = [0]

    def _cnt(n):
        if not n['k']:
            leaves[0] += 1
        for k in n['k']:
            _cnt(k)
    _cnt(root)
    h = TOP + (leaves[0] - 1) * PITCH + BH // 2 + 16
    return _svg(W, h, label, ''.join(out))


# ── 서버 값이 GPU 시간당 단가가 되는 식. _model_eq 의 'INF' 를 그림으로 ──────
FIG_EQ_INF = tree_svg(
    'GPU 시간당 단가는 어떤 항들로 쪼개지나',
    [116, 128, 128, 154],
    _node(['$', 'GPU·시간'], '÷', [
        _node(['월 총비용', '서버 한 대'], '+', [
            _node(['월 자본비'], '×', [
                _node(['선불 자본지출']),
                _node(['원리금 균등', '상환 계수']),
            ]),
            _node(['월 운영비'], '+', [
                _node(['월 호스팅']),
                _node(['상면 인건비']),
                _node(['회선']),
            ]),
        ]),
        _node(['GPU·시간', '서버 한 대·월'], '×', [
            _node(['서버당 GPU 장수']),
            _node(['한 달 시간']),
        ]),
    ]),
    marks=[('월 자본비', 1), ('월 호스팅', 2), ('한 달 시간', 3)])


# ── 클러스터 월 총비용. _model_eq 의 'TCO' 를 그림으로 ──────────────────────
FIG_EQ_TCO = tree_svg(
    '월 총비용은 여덟 항의 합으로 갈라진다',
    [140, 150, 162],
    _node(['TCO', '클러스터·월'], '+', [
        _node(['GPU'], '×', [
            _node(['$', 'GPU·시간']),
            _node(['GPU 장수']),
            _node(['한 달 시간']),
        ]),
        _node(['저장'], '×', [
            _node(['$', 'GiB·월']),
            _node(['GiB']),
        ]),
        _node(['네트워크']),
        _node(['컨트롤플레인'], '×', [
            _node(['$', 'VM·시간']),
            _node(['VM 수']),
            _node(['한 달 시간']),
        ]),
        _node(['지원'], '×', [
            _node(['할증률']),
            _node(['앞 네 항의 합']),
        ]),
        _node(['굿풋 손실']),
        _node(['설치']),
        _node(['디버깅']),
    ]),
    marks=[('지원', 1), ('굿풋 손실', 2), ('설치', 3)])
