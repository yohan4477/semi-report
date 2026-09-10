# -*- coding: utf-8 -*-
"""math tree(수식을 항으로 쪼갠 나무). 색은 회색만(확정 규칙 S2).

식을 줄로 늘어놓으면 어느 항이 어느 항을 낳는지가 안 보인다. 왼쪽에 결과를
두고 오른쪽으로 갈수록 잘게 쪼갠 상자로 세우면, 한 칸이 어긋났을 때 그 위로
무엇이 흔들리는지가 눈에 든다.

수식 블록이나 표가 바로 아래에 붙는 자리면 판에는 이름만 둔다. 그것이 없는
자리에서는 상자 둘째 줄에 값을 적는다 — 그때는 판 말고 값을 낼 데가 없다.
좌표는 `_place` 가 계산한다. 손으로 찍지 않는다(yohan-figure 규칙 2).
"""
import _biz_fig as bf

_svg, _r, _t, _lt = bf._svg, bf.sudo._r, bf.sudo._t, bf._lt
W = 640
TOP = 26            # 첫 잎 상자의 위 여백
BH = 34             # 한 줄짜리 상자 높이
LINE = 15           # 상자 안 줄 간격
VGAP = 14           # 잎 상자와 잎 상자 사이. 두 줄 상자도 이만큼은 떨어진다
GAP = 34            # 열과 열 사이. 연산자 동그라미가 이 사이에 선다
MARK_IN = 12        # 번호가 상자 안에서 왼쪽·위 테두리에서 떨어지는 거리


def _node(label, op=None, kids=()):
    return {'l': label, 'op': op, 'k': list(kids)}


def _h(node):
    """상자 높이. 두 줄짜리는 그만큼 키운다 — 높이를 한 값으로 박아 두면
    둘째 줄이 아래 테두리에 붙어 위아래 상자가 맞닿은 것처럼 보인다."""
    return BH + (len(node['l']) - 1) * LINE


def _depth(n):
    return 1 + max([_depth(k) for k in n['k']] or [0])


def _place(node, cols, depth=0, cur=None):
    """잎을 위에서부터 제 높이만큼 쌓고, 어미는 자식들의 한가운데에 놓는다."""
    if cur is None:
        cur = [TOP]
    x, w = cols[depth]
    if not node['k']:
        h = _h(node)
        y = cur[0] + h // 2
        cur[0] += h + VGAP
    else:
        for k in node['k']:
            _place(k, cols, depth + 1, cur)
        y = (node['k'][0]['y'] + node['k'][-1]['y']) // 2
    node['x'], node['y'], node['w'] = x, y, w
    node['bot'] = cur[0]
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
    h = _h(node)
    out.append(_r(x, y - h // 2, w, h))
    for i, s in enumerate(node['l']):
        out.append(_t(x + w // 2, y - h // 2 + (h - (len(node['l']) - 1) * LINE) // 2
                      + i * LINE + 5, s, 't-lab' if i == 0 else 't-sm'))
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

    번호는 상자 위 테두리에 걸친다. 상자 밖 왼쪽에 두면 잇는 선과 겹치고, 상자
    안으로 들이면 이름과 부딪친다. 테두리 위에 얹으면 글자 줄 위를 지나므로 둘 다
    피한다.
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
        # 상자 안 왼쪽 위 구석에 붙인다. 테두리를 물지 않을 만큼만 들인다
        # 번호를 상자 밖으로 옮겨 봤다가 되돌렸다(2026-09-10). 왼쪽 밖은 어미의
        # 연산자 동그라미와, 위쪽 밖은 윗줄 상자와 부딪친다. 이름이 긴 상자에는
        # 번호를 안 다는 쪽으로 푼다 — 다는 자리는 부르는 쪽이 고른다
        out.append(bf._mark(n['x'] + MARK_IN, n['y'] - _h(n) // 2 + MARK_IN, num))
    return _svg(W, root['bot'] - VGAP + TOP, label, ''.join(out))


