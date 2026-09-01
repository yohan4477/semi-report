# -*- coding: utf-8 -*-
"""실험: mermaid flowchart 표기를 읽어 fig_layout.Plate 로 굽는다.

`scripts/frame_view.py` 의 격자 그래프 파서(아스키 상자·선을 문자 단위로 추적)를
대신할 수 있는지 시험한다. 문법이 고정된 mermaid 를 받으면 파서가 정규식 몇 줄로
끝난다는 것이 이 실험의 가설이다 — 아스키 쪽은 화살촉·테두리 문자 꼴이 매번
달라져 규칙이 계속 늘어난다(2026-08-31 하루에 다섯 겹).

읽는 것은 셋뿐이다.

  ```mermaid ... ```           안의 `flowchart LR|TD|TB|BT|RL` 블록
  노드 선언   A[이름] · A(이름) · A{이름}
  이음        A --> B · A -->|라벨| B · A --- B
  묶음        subgraph 이름 … end  — 제목이 판의 열 이름(축)이 된다

`subgraph` 줄은 노드·이음 파서에서는 그대로 건너뛴다(그 줄에 뜬 id 는 노드가
아니다). 대신 딴 판에서 한 번 더 훑어 묶음을 읽는다 — 묶음이 곧은 사슬이면
열 하나로 세우고 제목을 열 이름으로 얹는다(`_column_plate`). 대비 판의 축이
그 자리다. 묶음 안이 갈라지면 이 길을 포기하고 원래 길로 돌아간다.

style·classDef·class·click·linkStyle·%% 주석은 그 줄만 건너뛴다 — 그
안에 든 노드·이음 줄은 그대로 읽는다(노드 이름을 잃지 않는다).

이 파일은 실험 산출물이다. `scripts/fig_layout.py` 를 그대로 쓰되 그 모듈 상수는
고치지 않는다 — 필요한 값은 `Plate(...)` 인자로만 넘긴다.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
import fig_layout  # noqa: E402


# ── 마크다운에서 ```mermaid 덩어리를 뽑는다 ─────────────────────────────
_FENCE = re.compile(r'```mermaid\s*\n(.*?)```', re.S)

# 제어 줄 — 이 줄 자체는 건너뛰지만, 그 안에 든 노드·이음 줄은 딴 줄에서
# 그대로 읽힌다(이 정규식은 그 줄 하나만 걸러 낸다)
_SKIP_LINE = re.compile(
    r'^\s*(flowchart\b|graph\b|subgraph\b|end\s*$|style\b|classDef\b|class\b|'
    r'click\b|linkStyle\b|%%)', re.I)

_ID = r'[A-Za-z0-9_]+'
_BR = r'(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\})'
# 노드 선언 하나 — 대괄호·소괄호·중괄호 중 하나로 이름을 감싼다
_DECL = re.compile(r'^\s*(%s)\s*%s\s*$' % (_ID, _BR))
# 이음 한 줄 — 양끝 노드는 선언을 겸할 수 있다(대괄호가 있으면 그 자리에서
# 이름이 정해진다). 화살표는 --> 와 --- 만 본다. 라벨은 --> 뒤 |...| 로만 온다
_EDGE = re.compile(
    r'^\s*(%s)\s*%s?\s*(-->|---)\s*(?:\|([^|]+)\|\s*)?(%s)\s*%s?' % (_ID, _BR, _ID, _BR))


def _bracket_text(s):
    """`[이름]`·`(이름)`·`{이름}` 에서 안쪽 글자만 뽑는다."""
    if not s:
        return None
    return s[1:-1].strip()


class Graph(object):
    """mermaid flowchart 하나에서 읽은 노드·이음."""

    def __init__(self):
        self.names = {}     # id -> 이름(대괄호가 없으면 id 그대로)
        self.order = []     # 처음 나온 차례
        self.edges = []     # (src_id, dst_id, label)

    def _register(self, nid, disp):
        if nid not in self.names:
            self.names[nid] = disp or nid
            self.order.append(nid)
        elif disp and self.names[nid] == nid:
            self.names[nid] = disp   # 맨몸으로 먼저 나온 id 에 뒤늦게 이름이 붙었다


def parse(block):
    """```mermaid ... ``` 안쪽 글 하나를 Graph 로 읽는다."""
    g = Graph()
    for ln in block.split(chr(10)):
        if not ln.strip():
            continue
        if _SKIP_LINE.match(ln):
            continue
        m = _EDGE.match(ln)
        if m:
            sid, sbr, arrow, label, tid, tbr = m.groups()
            g._register(sid, _bracket_text(sbr))
            g._register(tid, _bracket_text(tbr))
            g.edges.append((sid, tid, (label or '').strip()))
            continue
        m2 = _DECL.match(ln)
        if m2:
            nid, br = m2.group(1), m2.group(2)
            g._register(nid, _bracket_text(br))
            continue
        # 그 밖(주석 안 걸린 산문, subgraph 이름 줄 등)은 노드도 이음도 아니다
    return g


_SUBGRAPH = re.compile(
    r'^\s*subgraph\s+(?:%s\s*)?(\[[^\]]+\]|"[^"]+"|\S.*?)\s*$' % _ID, re.I)
_END = re.compile(r'^\s*end\s*$', re.I)


def parse_groups(block, g):
    """`subgraph … end` 를 (제목, [노드 id]) 로 읽는다. 없으면 빈 목록.

    노드·이음은 `parse()` 가 이미 읽었다 — 여기서는 어느 노드가 어느 묶음에
    드는지만 본다. 중첩 subgraph 는 안쪽부터 닫히는 대로 담는다.
    """
    groups, stack = [], []
    for ln in block.split(chr(10)):
        ms = _SUBGRAPH.match(ln)
        if ms:
            t = ms.group(1).strip()
            for _ in (0, 1):
                if len(t) > 1 and (t[0], t[-1]) in (('[', ']'), ('"', '"')):
                    t = t[1:-1].strip()
            stack.append([t, []])
            continue
        if _END.match(ln):
            if stack:
                groups.append(tuple(stack.pop()))
            continue
        if not stack:
            continue
        for m in _ANY_DECL.finditer(ln):
            nid = m.group(1)
            if nid in g.names and nid not in stack[-1][1]:
                stack[-1][1].append(nid)
    return groups


def _column_plate(g, groups, width):
    """묶음 하나를 열 하나로 세운 판. 제목이 열 이름(축)이다. 못 세우면 None.

    대비 판이 이 길로 온다 — 갈래가 나란한 사슬로 서는 꼴. 묶음 안에서 갈라지거나
    합류하면(한 파도에 형제가 여럿) 열 하나에 못 담으니 None 을 물려 원래 길
    (`_component_plate`)로 돌아간다. 묶음 밖에 남은 노드가 있어도 마찬가지다.
    """
    if len(groups) < 2:
        return None
    inside = set()
    for _, ids in groups:
        inside.update(ids)
    if inside != set(g.order):
        return None
    cols = []
    for title, ids in groups:
        if not title:
            return None
        edges = [e for e in g.edges if e[0] in ids and e[1] in ids]
        rows = _rows_of(ids, edges)
        if not rows or any(len(r) != 1 for r in rows):
            return None
        cols.append((title, [r[0] for r in rows]))
    depth = max(len(c[1]) for c in cols)
    p = fig_layout.Plate(width=width, subout=False, top=2.0, gap_y=10.0,
                         pad_y=8.0, bottom=4.0, fs=13.4, fs_s=12.0,
                         wrap_label=True)
    p.head(*[c[0] for c in cols])
    slot = {}
    for r in range(depth):
        cells, ids = [], []
        for _, chain in cols:
            nid = chain[r] if r < len(chain) else None
            cells.append(g.names[nid] if nid else None)
            ids.append(nid)
        p.row(*cells)
        for ci, nid in enumerate(ids):
            if nid:
                slot[nid] = (r, ci)
    for sid, tid, label in g.edges:
        if sid in slot and tid in slot and sid != tid:
            try:
                p.connect(p.at(*slot[sid]), p.at(*slot[tid]), label)
            except Exception:
                pass
    try:
        return p.render('묶음을 열로 세운 판')
    except AssertionError:
        return None


def mermaid_blocks(md):
    """마크다운 전체에서 ```mermaid 덩어리를 원문 그대로 리스트로."""
    return [m.group(1) for m in _FENCE.finditer(md)]


# ── 그래프를 판으로 ──────────────────────────────────────────────────────

def _topo_levels(order, edges):
    """소스가 먼저인 파도(레벨)로 나눈다. 한 파도 안 순서는 원문 등장 차례.

    frame_view._topo_order 와 같은 셈이지만, 여기서는 파도 자체를 남겨 둔다 —
    한 파도가 셋을 넘으면 그 파도만 여러 줄로 접어야 하기 때문이다.
    """
    indeg = {n: 0 for n in order}
    out = {n: [] for n in order}
    for a, b, _ in edges:
        if a in indeg and b in indeg:
            indeg[b] += 1
            out[a].append(b)
    seen = set()
    levels = []
    frontier = [n for n in order if indeg[n] == 0]
    while frontier:
        levels.append(frontier)
        seen.update(frontier)
        for n in frontier:
            for m in out[n]:
                indeg[m] -= 1
        frontier = [n for n in order if n not in seen and indeg[n] == 0]
    remaining = [n for n in order if n not in seen]
    if remaining:            # 고리 등 위상 정렬로 못 다룬 것은 안전망으로 맨 끝에
        levels.append(remaining)
    return levels


def _rows_of(order, edges):
    """파도(레벨) 하나가 곧 행 하나다.

    예전에는 파도를 `per_row`(3→2→1)로 접어 칸 수를 줄였다 — 그런데 한 파도가
    이미 형제 상자(같은 부모에서 갈렸거나 같은 자식으로 모인 것)를 담고 있으면,
    그 파도를 여러 줄로 쪼개는 순간 형제가 서로 다른 행에 갈려 「갈래」가
    「사슬」로 보인다(2026-09-01, 「폐쇄형/개방형 전략」이 세로로 이어진 사고).
    파도를 쪼개지 않는다 — 이름이 길어 폭을 못 채우면 `_build` 가
    `wrap_label` 로 상자를 늘려 접는다. 그래도 안 되면(파도 자체가 너무
    넓다) 판을 포기한다.
    """
    return _topo_levels(order, edges)


def _weak_groups(order, edges):
    """이음으로 이어진 상자만 한 덩이로 묶는다(약한 연결 성분).

    mermaid `subgraph` 는 안 읽는다(스펙대로 그 줄은 건너뛴다) — 그런데 받은
    도식 하나에 서로 안 이어진 사슬 둘이 들어오는 일이 있다(「기존 방식」
    사슬과 「OpenAI 혁신 방식」사슬처럼). 한 판에 같이 앉히면 위상 정렬이
    둘을 섞어 마치 하나의 순서인 것처럼 보인다 — A1→A2→B1→B2→… 로 읽혀
    실제로는 없는 인과가 생긴다. `frame_view._weak_groups` 와 같은 값으로,
    이어진 상자끼리만 묶어 따로따로 판을 짠다.
    """
    idx = {n: i for i, n in enumerate(order)}
    uf = list(range(len(order)))

    def find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x

    def union(x, y):
        x, y = find(x), find(y)
        if x != y:
            uf[y] = x

    for a, b, _ in edges:
        if a in idx and b in idx:
            union(idx[a], idx[b])
    groups = {}
    for n in order:
        groups.setdefault(find(idx[n]), []).append(n)
    return sorted(groups.values(), key=lambda g: idx[g[0]])


def _build(names, rows, edges, width, wrap_label=False):
    """자리(rows, 행마다 id 리스트)가 정해진 상자들을 판 하나로 굽는다. 실패하면 None.

    `wrap_label` 이면 이름이 칸 폭을 넘을 때 옆 칸을 잡아먹거나 잘리는 대신
    상자 안에서 여러 줄로 접는다(`fig_layout.wrap`) — 형제 상자를 같은 행에
    나란히 세운 채로 긴 mermaid 이름을 담을 수 있다.
    """
    p = fig_layout.Plate(width=width, subout=False, top=2.0, gap_y=10.0,
                         pad_y=8.0, bottom=4.0, fs=13.4, fs_s=12.0,
                         wrap_label=wrap_label)
    slot = {}
    for r, row_ids in enumerate(rows):
        cells = [names.get(nid, nid) for nid in row_ids]
        p.row(*cells)
        for c, nid in enumerate(row_ids):
            slot[nid] = (r, c)
    for sid, tid, label in edges:
        if sid not in slot or tid not in slot or sid == tid:
            continue
        ra, ca = slot[sid]
        rb, cb = slot[tid]
        try:
            p.connect(p.at(ra, ca), p.at(rb, cb), label)
        except Exception:
            pass
    try:
        return p.render('받은 글의 mermaid 도식')
    except AssertionError:
        return None


def _component_plate(names, order, edges, width):
    """한 덩이(서로 이어진 상자들)를 판 하나로.

    파도(레벨)가 행이다 — 파도 하나에 형제 상자가 여럿이면(분기·합류) 그
    행에 나란히 선다. **파도를 쪼개지 않는다**: 예전에는 폭을 넘기면 한
    행에 담는 칸 수를 3→2→1로 줄여 다시 짰는데, 1까지 줄면 형제도 한 칸씩
    떨어져 사슬처럼 보였다(2026-09-01). 이제는 이름이 길어 폭을 넘기면
    칸 수가 아니라 **상자 안 줄 수**를 늘린다(`wrap_label`) — 그래도
    못 들어가면(파도 하나가 낱말 하나로도 폭을 넘길 만큼 넓다) 판을
    포기하고 이전 길(줄 단위 판·표·글)로 물러난다.
    """
    rows = _rows_of(order, edges)
    if not rows:
        return None
    for wrap_label in (False, True):
        svg = _build(names, rows, edges, width, wrap_label=wrap_label)
        if svg:
            return svg
    return None


def to_plate(g, width=520.0, groups=None):
    """그래프 하나를 fig_layout.Plate SVG 로. 못 그리면 None.

    상자 배치는 `scripts/frame_view.py` 의 `_grid_plate_build` 가 쓰는 값을
    그대로 따른다 — 넓은 판 520 · 좁은 판 340 · fs=13.4 · fs_s=12.0 ·
    top=2 · gap_y=10 · pad_y=8 · bottom=4. 서로 안 이어진 덩이는 `_weak_groups`
    로 갈라 따로 판을 짜고 이어 붙인다 — 하나라도 못 앉히면 전부 실패로 되돌린다.
    """
    if groups:
        svg = _column_plate(g, groups, width)
        if svg:
            return svg
    groups = _weak_groups(g.order, g.edges)
    if not groups:
        return None
    svgs = []
    for grp in groups:
        gset = set(grp)
        gedges = [e for e in g.edges if e[0] in gset and e[1] in gset]
        svg = _component_plate(g.names, grp, gedges, width)
        if not svg:
            return None
        svgs.append(svg)
    return ''.join(svgs)


def block_html(block, width=520.0):
    """```mermaid 덩어리 하나를 판(HTML/SVG)으로. 노드가 둘 미만이면 None."""
    g = parse(block)
    if len(g.order) < 2:
        return None
    return to_plate(g, width=width, groups=parse_groups(block, g))


# ── 독립 검산 — 우리 파서와 다른 경로로 노드·이음 수를 다시 센다 ──────────
# `parse()` 자체가 틀렸으면 이 셈도 같이 틀릴 수 있으니 완전한 증명은 아니다.
# 그래도 정규식 하나(도식 문법)로 세는 값과, 좀 더 단순한 잣대(줄에 뜬 화살표
# 개수·대괄호류로 감싼 토큰 개수)로 센 값이 갈리면 파서가 뭔가를 잃었다는
# 신호는 된다.
_ARROW_COUNT = re.compile(r'-->|---')
_ANY_DECL = re.compile(r'(%s)\s*%s' % (_ID, _BR))


def naive_counts(block):
    """제어 줄을 뺀 나머지에서 화살표 수·선언된 id 집합을 단순하게 센다."""
    ids = set()
    arrows = 0
    for ln in block.split(chr(10)):
        if not ln.strip() or _SKIP_LINE.match(ln):
            continue
        arrows += len(_ARROW_COUNT.findall(ln))
        for m in _ANY_DECL.finditer(ln):
            ids.add(m.group(1))
        # 대괄호 없이 화살표에 바로 붙은 맨몸 id 도 노드다
        for tok in re.split(r'-->|---|\|[^|]*\|', ln):
            tm = re.match(r'^\s*(%s)\b' % _ID, tok)
            if tm:
                ids.add(tm.group(1))
    return len(ids), arrows


def verify(block):
    """parse() 결과가 naive_counts() 와 맞아떨어지는지."""
    g = parse(block)
    n_ids, n_arrows = naive_counts(block)
    return {
        'parsed_nodes': len(g.order), 'naive_nodes': n_ids,
        'parsed_edges': len(g.edges), 'naive_edges': n_arrows,
        'nodes_match': len(g.order) == n_ids,
        'edges_match': len(g.edges) == n_arrows,
    }


if __name__ == '__main__':
    md = io.open(sys.argv[1], encoding='utf-8').read()
    for i, block in enumerate(mermaid_blocks(md)):
        g = parse(block)
        print('--- 도식 %d: 노드 %d · 이음 %d ---' % (i + 1, len(g.order), len(g.edges)))
        print('검산:', verify(block))
        svg = to_plate(g, groups=parse_groups(block, g))
        print('판 굽기:', 'OK (%d자)' % len(svg) if svg else '실패')
