# -*- coding: utf-8 -*-
"""프레임 답을 카드에 **받은 그대로** 싣는다.

`insights/frames/*.md` 는 다른 모델에게 물어 받은 뷰다. 지금까지는 그 글을 재료로만 쓰고
문장은 우리가 다시 썼는데(겹침 1~4%), 받은 글 자체를 보여 달라는 자리도 있다. 이 모듈은
그 마크다운을 카드 마크업으로 옮긴다 — 요약하지 않고, 문장을 고치지 않는다.

옮기는 것은 넷이다.

  ## 제목        -> <p class="fv-h">
  | 표 |         -> <table>
  ``` 도식 ```   -> <pre class="fv-pre">
  * 목록 · 문단  -> <ul> · <p>

**미검증 원본이라는 표시를 상자 머리에 박는다.** 값이 원문에 있는지는 `check_frame` 이
따로 세고, 그 결과(원문 밖 몇 개)를 상자 머리에 같이 적는다.
"""
import io
import os
import unicodedata
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_layout  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(ROOT, 'insights', 'frames')


# 아스키 도식을 상자로 굽는다. 그대로 두면 폭이 넘치고 글꼴이 바뀌면 선이 어긋난다 —
# 상자는 판 폭에 맞춰 서고 다크모드 색도 따라온다. 못 읽는 꼴이면 아스키 그대로 둔다.
_BOX = re.compile(r'\[([^\]\[]+)\]')
# 「──>」처럼 선을 길게 끌고 온 화살표도 잡는다 — 안 잡으면 「>」가 상자 밑에
# 딸린 라벨로 남는다. ➡⬅⬆⬇ 는 여기서 안 잡는다 — `_denorm_emoji` 가 도식
# 덩어리 맨 앞에서 이미 →←↑↓ 로 바꿔 놓는다(방침: 화면에 이모지를 안 남긴다).
# ↔·⇒ 는 그 방침에서도 그대로 두는 문자라 여기 남는다
_ARROW = re.compile(r'(<[─—=-]+>|-->|→|▶|=>|=+>|[─—-]+>|<[─—-]+|[↔⇒])')


# 세로선은 전각만 오지 않는다. 아스키 표 꼴(+---+ 와 | 이름 |)로 그려 오는 판이 있어
# ASCII 막대도 본다 — 도식 덩어리 안에서만 도는 함수라 마크다운 표와 안 부딪친다
_BAR = '│║|'


def _bracketize(block):
    """선 그림(│ 이름 │)을 [ 이름 ] 꼴로 바꾼다.

    받는 쪽이 아스키 선으로 그려 오는 일이 잦은데, 상자 뽑는 자리는 대괄호만 안다.
    선 그림의 세로선 사이 글자가 곧 상자 이름이라 그대로 옮길 수 있다.
    """
    out = []
    for ln in block.split(chr(10)):
        # 막대가 둘 이상이라야 상자 줄이다. 하나뿐이면 「│ (작업 지시 …)」처럼
        # 이음 선 옆에 붙은 라벨이라 상자로 세우면 없던 칸이 하나 생긴다
        if sum(ln.count(c) for c in _BAR) >= 2 and not _BOX.search(ln):
            cells = [c.strip(' ─═-+') for c in re.split(r'[%s]' % re.escape(_BAR), ln)]
            cells = [c for c in cells if len(re.findall(r'[가-힣A-Za-z0-9]', c)) >= 2]
            if cells:
                ln = ' '.join('[%s]' % c for c in cells)
        out.append(ln)
    return chr(10).join(out)


_TOP = re.compile(r'^\s*[┌╔+][─═\-]{2,}')
_BOT = re.compile(r'^\s*[└╚+][─═\-]{2,}')


def _unframe(block):
    """여러 줄로 그린 상자(┌ │ └)를 한 줄짜리 [ 이름 — 설명 ] 로 접는다.

    상자 하나가 세 줄이면 우리 파서는 그 줄들을 따로 센다 — 상자 안 설명이 저마다
    상자가 되어 한 줄에 칸이 여섯이 되고, 폭이 넘쳐 판이 세로 사슬로 떨어진다.
    2026-08-31 그록 경영전략 뷰가 그랬다. 테두리 줄 사이를 열별로 이어 붙인다.
    """
    lines = block.split(chr(10))
    out, i = [], 0
    while i < len(lines):
        if not _TOP.match(lines[i]):
            out.append(lines[i])
            i += 1
            continue
        j = i + 1
        body = []
        while j < len(lines) and not _BOT.match(lines[j]):
            body.append(lines[j])
            j += 1
        if j >= len(lines) or not body:
            out.append(lines[i])
            i += 1
            continue
        # 열 슬롯별로 글을 모은다. 세로선 사이가 한 칸이다
        cols = []
        for ln in body:
            parts = [p.strip(' -─═') for p in re.split(r'[│║|]', ln)]
            parts = [p for p in parts if len(re.findall(r'[가-힣A-Za-z0-9]', p)) >= 2]
            for k, p in enumerate(parts):
                while len(cols) <= k:
                    cols.append([])
                cols[k].append(p)
        cells = []
        for c in cols:
            if not c:
                continue
            name, sub = c[0], ' '.join(c[1:])
            cells.append('[ %s ]%s' % (name, (' — ' + sub) if sub else ''))
        out.append('  '.join(cells) if cells else lines[i])
        i = j + 1
    return chr(10).join(out)


def _cells(ln):
    """줄 하나를 (글자, 시작 칸, 끝 칸) 으로. 한글은 두 칸을 먹는다.

    글자 수로 칸을 세면 한글 줄과 라틴 줄의 칸이 어긋나 좌우 두 판을 못 가른다 —
    「[ 기존 구조: 공유형 HBM ]」은 글자 17 개인데 화면에서는 27 칸이다.
    """
    out, col = [], 0
    for ch in ln:
        w = 2 if unicodedata.east_asian_width(ch) in 'WF' else 1
        out.append((ch, col, col + w))
        col += w
    return out


# ── 격자 그래프 파서 ─────────────────────────────────────────────────────
# 줄 순서로 상자를 이어 붙이지 않는다. 문자 격자에서 상자를 찾고, 상자 밖의
# 선 문자를 따라가 실제로 어느 상자와 어느 상자가 닿았는지를 읽은 뒤, 그
# 그래프(상자 + 이음) 그대로 판을 짠다. 「연산기 A·B·C 가 한 풀에 붙는다」처럼
# 갈래·모임이 있는 그림은 줄 단위 사슬(옛 길)로는 못 그린다 — 세 상자가
# 세로로 쌓인 것과 셋이 한 곳에 모이는 것이 같은 그림으로 나온다.
# 글자마다 어느 쪽(위·아래·왼·오)으로 이어지는지를 정해 둔다. '◀' 같은 화살촉은
# 좌우로만 잇는다 — 방향을 안 가리면 화살촉이 우연히 같은 칸에 세로로 쌓였을 때
# (독립된 가로선 셋이 왼쪽 끝만 나란한 경우) 하나의 세로선으로 잘못 묶인다.
# 2026-08-31 「전용 저지연 버스」 세 줄이 그렇게 하나로 뭉쳤다.
_DIRS = {
    '─': 'LR', '-': 'LR', '═': 'LR', '~': 'LR', '=': 'LR',
    '│': 'UD', '|': 'UD', '║': 'UD',
    '┌': 'DR', '╔': 'DR', '╭': 'DR',
    '┐': 'DL', '╗': 'DL', '╮': 'DL',
    '└': 'UR', '╚': 'UR', '╰': 'UR',
    '┘': 'UL', '╝': 'UL', '╯': 'UL',
    '├': 'UDR', '┤': 'UDL', '┬': 'DLR', '┴': 'ULR', '┼': 'UDLR',
    '+': 'UDLR',
    '▲': 'UD', '▼': 'UD', '↑': 'UD', '↓': 'UD',
    '◀': 'LR', '▶': 'LR', '←': 'LR', '→': 'LR', '<': 'LR', '>': 'LR',
    # ➡⬅⬆⬇ 는 여기 없다 — `_denorm_emoji` 가 도식 맨 앞에서 이미 →←↑↓ 로
    # 바꿔 놓는다(화면에 이모지를 안 남기는 방침). ↔·⇒ 는 그대로 남는 문자라
    # 방향을 정해 둔다 — 안 넣으면 「TSMC ↔ 엔비디아」 같은 줄이 이음이 안 잡힌다
    '↔': 'LR', '⇒': 'LR',
}
_WIRE_CH = ''.join(_DIRS.keys())
_WIRE = frozenset(_DIRS.keys())
# 줄 머리에서 대괄호 없이 선에 바로 붙은 낱말(「사용자 프롬프트 ──>」의
# 「사용자 프롬프트」)도 상자로 본다 — 안 그러면 그 낱말이 각주로 떨어져
# 그래프에서 시작점이 사라진다
_BARE_HEAD = re.compile(r'^([가-힣A-Za-z0-9][가-힣A-Za-z0-9 /]{0,18}[가-힣A-Za-z0-9])'
                        r'\s*(?=[%s])' % re.escape(_WIRE_CH))


class _GBox(object):
    """격자에서 읽은 상자 하나. (줄, 칸) 이 곧 원래 그림에서의 자리다."""
    __slots__ = ('name', 'sub', 'row', 'c0', 'c1', 'bare')

    def __init__(self, name, sub, row, c0, c1, bare=False):
        self.name, self.sub, self.row, self.c0, self.c1 = name, sub, row, c0, c1
        self.bare = bare             # 대괄호 없이 맨몸으로 선에 붙은 낱말인가


def _end_col(idx, cells):
    """문자 인덱스 [.., idx) 범위 — 곧 마지막 글자(인덱스 idx-1)의 끝 칸.

    끝 칸을 「시작 칸 + 1」로 어림하면 한글처럼 두 칸 먹는 글자로 끝나는
    이름에서 한 칸이 모자란다 — 「엔비디아」 뒤 화살표가 상자 바로 옆이 아니라
    한 칸 건너에 있는 것으로 읽혀 이음이 안 잡힌다(2026-08-27 밸류체인 그림).
    `_cells` 가 이미 (글자, 시작, 끝) 을 주므로 끝 칸을 그대로 쓴다.
    """
    j = idx - 1
    if 0 <= j < len(cells):
        return cells[j][2]
    return cells[-1][2] if cells else 0


def _graph_boxes(block):
    """대괄호 상자와 맨몸 낱말을 줄·칸 위치와 함께 뽑는다.

    여러 줄 테두리(┌│└)는 호출하는 쪽에서 미리 `_unframe` 으로 접어 한 줄로
    만들어 둔다 — 상자 찾기는 대괄호 정규식 하나로 충분해진다.
    """
    out = []
    for i, ln in enumerate(block.split(chr(10))):
        cells = _cells(ln)
        idx2col = [a for ch, a, b in cells]

        def col_of(idx):
            return idx2col[idx] if idx < len(idx2col) else (
                idx2col[-1] + 1 if idx2col else 0)
        taken = []           # 이 줄에서 이미 상자로 먹은 문자 구간(시작,끝)
        for m in _BOX.finditer(ln):
            name = m.group(1).strip()
            if len(re.findall(r'[가-힣A-Za-z0-9]', name)) < 2:
                continue
            s, e = m.start(), m.end()
            c0, c1 = col_of(s), col_of(e - 1) + (cells[e - 1][2] - cells[e - 1][1]
                                                 if e - 1 < len(cells) else 1)
            tail = ln[e:]
            tm = re.match(r'\s*[:\-–—]\s*(.+)', tail)
            sub = ''
            if tm and not (set(tm.group(1)) & _WIRE) and '[' not in tm.group(1):
                sub = tm.group(1).strip()
            out.append(_GBox(name, sub, i, c0, c1))
            taken.append((s, e))
        # 화살표로 이어 놓은 낱말 사슬(「TSMC(제조) ➡ 엔비디아 ➡ 클라우드 ➡ …」)도
        # 상자로 읽는다. 대괄호가 없다고 각주로 내리면 그 줄이 그림의 알맹이인데
        # 판에서 사라진다 — 2026-08-31 밸류체인 그림이 그랬다
        if not taken and len(_ARROW.findall(ln)) >= 2:
            pos = 0
            for piece in _ARROW.split(ln):
                if not piece or _ARROW.fullmatch(piece):
                    pos += len(piece or '')
                    continue
                name = piece.strip()
                if len(re.findall(r'[가-힣A-Za-z0-9]', name)) >= 2:
                    s0 = pos + (len(piece) - len(piece.lstrip()))
                    e0 = s0 + len(name)
                    out.append(_GBox(name, '', i, col_of(s0), _end_col(e0, cells)))
                    taken.append((s0, e0))
                pos += len(piece)
        bm = _BARE_HEAD.match(ln.lstrip())
        if bm:
            lead = len(ln) - len(ln.lstrip())
            s, e = lead, lead + bm.end(1)
            if not any(s < te and s2 < e for s2, te in taken):
                text = bm.group(1).strip()
                if len(re.findall(r'[가-힣A-Za-z0-9]', text)) >= 2:
                    c0 = col_of(s)
                    c1 = _end_col(e, cells) if e else c0
                    out.append(_GBox(text, '', i, c0, c1, bare=True))
    return out


def _wire_cells(block, boxes):
    """상자 칸을 뺀 나머지에서 선 문자만 (줄,칸) -> 글자 로 모은다."""
    covered = set()
    for b in boxes:
        for c in range(b.c0, b.c1):
            covered.add((b.row, c))
    cells = {}
    for i, ln in enumerate(block.split(chr(10))):
        for ch, a, b in _cells(ln):
            if ch == ' ' or (i, a) in covered:
                continue
            if ch in _WIRE:
                cells[(i, a)] = ch
    return cells


_ARROWHEAD = frozenset('▲▼◀▶→←↑↓<>')


def _components(cells):
    """선 칸을 이웃으로 묶어 이음 성분을 만든다.

    글자의 방향(`_DIRS`)이 맞는 이웃만 잇는다 — 아무 선 칸이나 붙어 있다고
    이으면 '◀' 셋이 왼쪽 끝만 나란한 우연을 세로선 하나로 읽는다. 나가는 쪽은
    엄격히 본다. 다만 **받는 쪽이 화살촉이면 방향을 안 가린다** — 손으로 그린
    그림은 화살촉이 꺾이는 자리에서 한 칸씩 어긋나는 일이 흔하다(「▼」가 코너
    「┘」보다 한 칸 왼쪽에 서는 식). 화살촉은 그 자체가 「여기서 선이 끝난다」는
    표시라 어느 쪽에서 와도 받는다.
    """
    seen, comps = set(), []
    for pos in cells:
        if pos in seen:
            continue
        stack, comp = [pos], []
        seen.add(pos)
        while stack:
            p = stack.pop()
            comp.append(p)
            r, c = p
            dp = _DIRS.get(cells[p], '')
            for dr, dc, out, back in ((0, 1, 'R', 'L'), (0, -1, 'L', 'R'),
                                      (1, 0, 'D', 'U'), (-1, 0, 'U', 'D')):
                if out not in dp:
                    continue
                q = (r + dr, c + dc)
                if q not in cells or q in seen:
                    continue
                qc = cells[q]
                if back in _DIRS.get(qc, '') or qc in _ARROWHEAD or cells[p] in _ARROWHEAD:
                    seen.add(q)
                    stack.append(q)
        comps.append(comp)
    return comps


class _UF(object):
    """이음 성분을 라벨 다리로 합칠 때 쓰는 합집합-찾기."""

    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            self.p[y] = x


def _bridge(block, comps, boxes):
    """같은 줄에서 글 하나(라벨)를 사이에 두고 끊긴 이음 성분을 하나로 잇는다.

    「─┼─ (트래픽 경합/지연) ─▶」처럼 선 가운데 글이 끼면 그 자리의 선 문자가
    없어 두 성분으로 갈린다. 사이에 상자가 없고 글이 짧으면(60 칸 이내) 원래
    한 선이었던 것으로 보고 합치고, 그 글을 이음의 이름으로 얹는다.
    """
    comp_id = {}
    for i, comp in enumerate(comps):
        for p in comp:
            comp_id[p] = i
    uf = _UF(len(comps))
    box_spans = {}
    for b in boxes:
        box_spans.setdefault(b.row, []).append((b.c0, b.c1))
    labels = {}
    lines = block.split(chr(10))
    for row_i, ln in enumerate(lines):
        cells = _cells(ln)
        cols = sorted(c for (r, c) in comp_id if r == row_i)
        runs = []                    # (시작칸, 끝칸, 성분id) — 이 줄 안에서 이어진 구간
        cur = None
        for c in cols:
            cid = comp_id[(row_i, c)]
            if cur and cur[2] == cid and c == cur[1] + 1:
                cur = (cur[0], c, cid)
            else:
                if cur:
                    runs.append(cur)
                cur = (c, c, cid)
        if cur:
            runs.append(cur)
        for k in range(len(runs) - 1):
            s0, e0, id0 = runs[k]
            s1, e1, id1 = runs[k + 1]
            if uf.find(id0) == uf.find(id1):
                continue
            g0, g1 = e0 + 1, s1 - 1
            if g1 < g0 or g1 - g0 > 60:
                continue
            if any(bc0 < g1 + 1 and bc1 > g0 for bc0, bc1 in box_spans.get(row_i, [])):
                continue            # 사이에 상자가 있으면 상자를 건너 잇지 않는다
            text = ''.join(ch for ch, a, bb in cells if g0 <= a <= g1).strip(' ─═-·')
            if len(re.findall(r'[가-힣A-Za-z0-9]', text)) < 1:
                continue
            uf.union(id0, id1)
            root = uf.find(id0)
            if text and root not in labels:
                labels[root] = text
    groups = {}
    for i, comp in enumerate(comps):
        groups.setdefault(uf.find(i), []).extend(comp)
    out_cells, out_labels = [], []
    for root, cells_ in groups.items():
        out_cells.append(cells_)
        out_labels.append(labels.get(root, ''))
    return out_cells, out_labels


def _horiz_seeded(comps, boxes):
    """가로로(대괄호 바로 옆) 선이 닿은 적이 있는 상자 id 집합.

    넓은 상자(제목 줄)는 세로 붙음을 안 본다 — 아래 세로선의 칸이 넓은 폭
    안에 우연히 들 수 있다. 하지만 그 상자가 다른 자리에서 이미 가로로
    선을 문 적이 있으면(진짜 마디라는 증거) 넓어도 세로 붙음을 마저 본다.
    """
    allcells = set()
    for c in comps:
        allcells.update(c)
    seeded = set()
    for b in boxes:
        if any((b.row, c) in allcells for c in (b.c1, b.c1 + 1, b.c0 - 1, b.c0 - 2)):
            seeded.add(id(b))
    return seeded


# 화살촉이 가리키는 쪽. 닿은 자리의 글자가 이 사전에 있으면 기본 방향을 뒤집을
# 수도 있다 — 「[상자] <── …」처럼 화살촉이 상자 쪽을 보면 그 상자는 나가는
# 쪽이 아니라 받는 쪽이다
_ARROW_DIR = {'<': 'L', '◀': 'L', '>': 'R', '▶': 'R', '←': 'L', '→': 'R',
             '▲': 'U', '▼': 'D', '↑': 'U', '↓': 'D'}
_OPPOSITE = {'R': 'L', 'L': 'R', 'U': 'D', 'D': 'U'}


def _side_role(touch_dir, ch, default):
    """상자에서 touch_dir 쪽으로 닿은 자리의 글자 ch 를 보고 나가는지·받는지 정한다.

    화살촉이 상자를 향하면(닿은 방향의 반대쪽을 가리키면) 받는 쪽이고, 상자에서
    멀어지는 쪽을 가리키면 나가는 쪽이다. 화살촉이 없으면 `default`(기본값)다.
    """
    d = _ARROW_DIR.get(ch)
    if d is None:
        return default
    return 'dst' if d == _OPPOSITE[touch_dir] else 'src'


def _touches(cellset, cellchars, boxes, seeded, ignore_arrows=False):
    """이 이음 성분이 닿은 상자를 나가는 쪽(src)·들어오는 쪽(dst) 으로 가른다.

    오른쪽·아래로 나는 선은 나가는 쪽, 왼쪽·위에서 오는 선은 들어오는 쪽으로
    본다 — 화살촉이 없을 때의 기본 방향이다. 닿은 자리에 화살촉이 있으면
    `_side_role` 이 그 방향을 따라 뒤집는다(`ignore_arrows` 면 안 뒤집는다 —
    「◀── … ──▶」처럼 양끝에 화살촉이 서로를 보면 둘 다 받는 쪽이 되어 이음이
    아예 안 잡힌다. 그때는 화살촉을 무시하고 기본값으로 되돌린다). 가로 붙음
    (같은 줄, 대괄호 바로 옆)을 먼저 보고, 그것이 없을 때만 세로 붙음(윗줄·
    아랫줄)을 본다. 세로 붙음은 좁은 상자(24 칸 이하)이거나 `seeded`(다른
    곳에서 이미 가로로 닿은 적이 있는) 상자만 본다.
    """
    src, dst = [], []
    for b in boxes:
        narrow = b.c1 - b.c0 <= 24 or id(b) in seeded
        # 대괄호와 선 사이에 빈칸이 하나 끼는 꼴(「] ─┐」)까지 허용한다
        right = next((c for c in (b.c1, b.c1 + 1) if (b.row, c) in cellset), None)
        left = next((c for c in (b.c0 - 1, b.c0 - 2) if (b.row, c) in cellset), None)
        below = next((c for c in range(b.c0, b.c1) if (b.row + 1, c) in cellset), None)
        above = next((c for c in range(b.c0, b.c1) if (b.row - 1, c) in cellset), None)
        if right is not None:
            ch = '' if ignore_arrows else cellchars.get((b.row, right), '')
            role = _side_role('R', ch, 'src')
        elif left is not None:
            ch = '' if ignore_arrows else cellchars.get((b.row, left), '')
            role = _side_role('L', ch, 'dst')
        elif narrow and below is not None:
            ch = '' if ignore_arrows else cellchars.get((b.row + 1, below), '')
            role = _side_role('D', ch, 'src')
        elif narrow and above is not None:
            ch = '' if ignore_arrows else cellchars.get((b.row - 1, above), '')
            role = _side_role('U', ch, 'dst')
        else:
            continue
        (src if role == 'src' else dst).append(b)
    return src, dst


def _graph_edges(block, boxes):
    """상자 목록에서 실제 선으로 닿은 쌍만 이음으로 만든다. 없는 이음은 안 만든다."""
    wcells = _wire_cells(block, boxes)
    comps = _components(wcells)
    if not comps:
        return []
    seeded = _horiz_seeded(comps, boxes)
    groups, labels = _bridge(block, comps, boxes)
    edges = []
    for cells, label in zip(groups, labels):
        cellset = set(cells)
        src, dst = _touches(cellset, wcells, boxes, seeded)
        if not src or not dst:
            # 화살촉 방향이 양끝에서 서로를 가리키면(「◀──…──▶」) 둘 다 받는
            # 쪽이 되어 여기 걸린다 — 화살촉을 무시하고 기본 방향으로 다시 본다
            src, dst = _touches(cellset, wcells, boxes, seeded, ignore_arrows=True)
        if not src or not dst:
            continue                # 상자를 못 찾은 선은 이음이 아니다(꾸밈 화살표 등)
        first = True
        for s in src:
            for t in dst:
                if s is t:
                    continue
                edges.append((s, t, label if first else ''))
                first = False
    return edges


_WIRE_STRIP = re.compile('[%s]' % re.escape(_WIRE_CH))


def _mask_boxes(ln, row, boxes):
    """이 줄에서 상자가 차지한 칸을 빈칸으로 지운다.

    대괄호 상자는 `_BOX.sub` 로 이미 지워지지만, 화살표 사슬의 맨몸 상자
    (「TSMC(제조) → 엔비디아」의 「TSMC(제조)」)는 대괄호가 없어 그대로 남는다 —
    각주 추출이 사슬 줄 자체를 다시 각주 글로 읽어 버린다(2026-08-27
    밸류체인 그림). 칸 위치로 상자 몫을 지운다.
    """
    row_boxes = [b for b in boxes if b.row == row]
    if not row_boxes:
        return ln
    out = list(ln)
    for i, (ch, a, bnd) in enumerate(_cells(ln)):
        if any(b.c0 <= a < b.c1 for b in row_boxes):
            out[i] = ' '
    return ''.join(out)


def _graph_notes(block, used, skip_rows=frozenset(), boxes=()):
    """상자에도 이음에도 못 붙는 글을 각주로 남긴다.

    `used` 는 이미 쓴 글(이음 이름), `skip_rows` 는 `_below_labels` 가 이미
    이음 이름으로 다 건져 간 줄이다 — 안 빼면 「(마진 흡수) · (마진 흡수) ·
    (비용 압박)」이 각주로 한 번 더 나온다. `boxes` 는 대괄호 없는 사슬 상자를
    빼려고 받는다(`_mask_boxes`).
    """
    notes = []
    for r, ln in enumerate(block.split(chr(10))):
        if r in skip_rows:
            continue
        t = _mask_boxes(ln, r, boxes)
        t = _BOX.sub(' ', t)
        t = _ARROW.sub(' ', t)
        t = _WIRE_STRIP.sub(' ', t)
        t = re.sub(r'\s{2,}', ' · ', t).strip(' ·')
        if len(re.findall(r'[가-힣A-Za-z0-9]', t)) >= 4 and t not in used:
            notes.append(t)
    return notes


_PAREN = re.compile(r'\(([^()]+)\)')


def _below_labels(block, boxes, edges):
    """사슬 아래 줄에 괄호로 붙은 라벨을 칸 위치로 가장 가까운 이음에 붙인다.

    「TSMC → 엔비디아 → 클라우드」사슬 밑에 「(마진 흡수)   (마진 흡수)」식으로
    라벨이 화살표가 아니라 **한 줄 아래**에 따로 앉는 꼴이 있다. 그 줄은 상자도
    이음도 아니라 격자 추적(`_graph_edges`)으로는 안 잡힌다 — 괄호 조각의 칸
    중심과, 그 위 줄에서 라벨 없는 이음마다의 자리(두 상자 사이 빈 칸의 가운데)
    를 견줘 가장 가까운 이음에 이름으로 얹는다. 반환은 (새 이음 목록, 라벨
    줄로 다 쓴 줄 번호 집합) — 뒤엣것은 `_graph_notes` 가 그 줄을 다시 각주로
    안 내리게 뺄 때 쓴다.
    """
    box_rows = set(b.row for b in boxes)
    lines = block.split(chr(10))
    used_rows = set()
    out = list(edges)
    for r, ln in enumerate(lines):
        if r in box_rows or r - 1 not in box_rows:
            continue
        pieces = [(m.start(), m.end(), m.group(1)) for m in _PAREN.finditer(ln)]
        if not pieces:
            continue
        # 괄호 밖에 다른 글이 있으면 라벨 줄이 아니라 그냥 설명 문단이다
        if _PAREN.sub('', ln).strip():
            continue
        row_edges = [i for i, (a, b, lab) in enumerate(out)
                    if a.row == b.row == r - 1 and not lab]
        if not row_edges:
            continue
        cells = _cells(ln)
        for s, e, text in pieces:
            c0 = cells[s][1] if s < len(cells) else 0
            c1 = cells[e - 1][2] if e - 1 < len(cells) else c0
            center = (c0 + c1) / 2.0

            def dist(i):
                a, b, _ = out[i]
                return abs((a.c1 + b.c0) / 2.0 - center)
            best = min(row_edges, key=dist)
            a, b, _ = out[best]
            out[best] = (a, b, text.strip())
            row_edges.remove(best)      # 라벨 하나가 이음 둘을 먹지 않는다
        used_rows.add(r)
    return out, used_rows


def _col_bands(boxes, gap=6):
    """상자의 왼쪽 칸을 왼→오 묶음(열)으로 가른다. 틈이 좁으면 같은 열이다."""
    xs = sorted(set(b.c0 for b in boxes))
    bands = []
    for x in xs:
        if bands and x - bands[-1][-1] <= gap:
            bands[-1].append(x)
        else:
            bands.append([x])
    band_of = {}
    for i, grp in enumerate(bands):
        for x in grp:
            band_of[x] = i
    return band_of, len(bands)


def _graph_of(block):
    """도식 한 덩어리를 (상자, 이음, 각주) 그래프로. 그래프로 못 읽으면 None.

    이음이 하나도 안 잡히면 그래프로 다룰 뜻이 없다 — 사슬 하나짜리 그림은
    옛 길(줄 단위)에 맡긴다. 그 길도 같은 안전망(`_kept`)을 탄다.
    """
    block = _unframe(block)
    boxes = _graph_boxes(block)
    if len(boxes) < 2:
        return None
    edges = _graph_edges(block, boxes)
    if not edges:
        return None
    edges, label_rows = _below_labels(block, boxes, edges)
    used = set(e[2] for e in edges if e[2])
    notes = _graph_notes(block, used, label_rows, boxes)
    return boxes, edges, notes


def _weak_groups(boxes, edges):
    """이음으로 이어진 상자만 한 덩이로 묶는다(약한 연결 성분).

    받은 그림 한 덩어리 안에 서로 안 이어진 미니 도식이 여럿 들어오는 일이
    있다(「과거」 사슬과 「현재」 다이아몬드가 빈 줄로만 나뉜 채 한 울타리
    안에 있는 경우). 그 둘을 한 판의 같은 열로 묶으면 서로 무관한 상자의
    가로 자리가 우연히 겹쳐 열이 쓸데없이 늘고 판 폭을 넘는다 — 이음이 실제로
    있는 상자끼리만 한 판으로 묶고, 나머지는 따로 판을 짠다.
    """
    idx = {id(b): i for i, b in enumerate(boxes)}
    uf = _UF(len(boxes))
    for a, b, _ in edges:
        uf.union(idx[id(a)], idx[id(b)])
    groups = {}
    for b in boxes:
        groups.setdefault(uf.find(idx[id(b)]), []).append(b)
    # 원래 그림에서 먼저 나온 덩이가 앞서게, 맨 위 줄 번호로 정렬한다
    return sorted(groups.values(), key=lambda g: min(b.row for b in g))


def _grid_plate_build(boxes, edges, row_of, col_of, ncol, width):
    """자리(row_of·col_of, 상자 id 로 찾는다)가 이미 정해진 상자들을 판 하나로 굽는다.

    좁은 판(열을 줄이거나 한 칸으로 쌓은 것)과 넓은 판이 이 함수 하나를 같이
    쓴다 — 자리를 어떻게 셈했든 판을 짜고 이음을 거는 마지막 손은 하나여야
    한다. 자리가 겹치거나 폭을 넘으면 None.
    """
    grid = {}
    for b in boxes:
        key = (row_of[id(b)], col_of[id(b)])
        if key in grid:
            return None           # 자리가 겹치면 읽은 자리를 못 믿는 것이니 되돌린다
        grid[key] = b
    nrow = len(set(row_of.values()))
    p = fig_layout.Plate(width=width, subout=False, top=2.0, gap_y=10.0,
                         pad_y=8.0, bottom=4.0, fs=13.4, fs_s=12.0)
    slot = {}
    for r in range(nrow):
        cells = []
        for c in range(ncol):
            b = grid.get((r, c))
            cells.append((b.name, b.sub) if b else None)
        p.row(*cells)
        for c in range(ncol):
            b = grid.get((r, c))
            if b:
                slot[id(b)] = (r, c)
    try:
        for a, b, label in edges:
            ra, ca = slot[id(a)]
            rb, cb = slot[id(b)]
            # 한 칸으로 쌓은 판(ncol=1)에서 상자를 하나 이상 건너뛰는 이음은
            # 가운데로 그으면 사이 상자를 정통으로 뚫고 지나가 다른(인접) 이음과
            # 겹쳐 안 보인다 — 가장자리로 붙여 「이 상자를 지나쳐 간다」를 보이게 한다
            at = 0.82 if ncol == 1 and abs(ra - rb) > 1 else 0.5
            p.connect(p.at(ra, ca), p.at(rb, cb), label, at=at)
        return p.render('받은 글의 도식')
    except AssertionError:
        return None


def _topo_order(boxes, edges):
    """소스(들어오는 이음이 없는 상자)가 먼저, 싱크(나가는 이음이 없는 상자)가
    나중에 오는 순서로 상자를 늘어놓는다.

    좁은 판이 한 칸으로 쌓아야 할 때 원문 줄 순서를 그대로 쓰면 갈래·모임이
    사슬로 보인다 — 「연산기 A·B·C 가 다 풀로 모인다」인데 줄 순서로 쌓으면
    B 가 A 와 C 사이에 끼어 「A→B→C→풀」사슬처럼 읽힌다. 이음을 따라 위상
    정렬해 소스를 앞으로, 싱크를 뒤로 모은다. 같은 단계에 선 상자끼리는 원문
    줄 순서를 지킨다 — 안 그러면 매번 다른 순서가 나와 재현이 안 된다.
    """
    ids = [id(b) for b in boxes]
    by_id = {id(b): b for b in boxes}
    indeg = {i: 0 for i in ids}
    out = {i: [] for i in ids}
    for a, b, _ in edges:
        if id(a) in indeg and id(b) in indeg:
            indeg[id(b)] += 1
            out[id(a)].append(id(b))
    order, seen = [], set()
    frontier = [i for i in ids if indeg[i] == 0]
    while frontier:
        frontier.sort(key=lambda i: by_id[i].row)
        nxt = []
        for i in frontier:
            if i in seen:
                continue
            seen.add(i)
            order.append(by_id[i])
            for j in out[i]:
                indeg[j] -= 1
                if indeg[j] == 0:
                    nxt.append(j)
        frontier = nxt
    order += [b for b in boxes if id(b) not in seen]   # 고리 등 못 다룬 것은 안전망으로
    return order


def _group_plate(boxes, edges, width):
    """상자·이음 한 덩이(서로 이어진 것들)를 판 하나로. 자리가 안 맞으면 셋을
    차례로 시도한다. 넓은 판(520)·좁은 판(340) 둘 다 이 하나를 쓴다.

    ① 원래 자리(행·열) 그대로 앉혀 본다 — 칸이 넷 이하고 이름이 짧으면
       이걸로 된다.
    ② 안 되면 왼쪽 첫 열만 남기고 나머지 열을 하나로 합친다 — 칸 수를
       줄이지만 이음은 그대로다.
    ③ 그래도 안 되면(칸이 넷을 넘거나 ②도 자리가 겹치면) 한 칸으로 쌓되,
       원문 줄 순서가 아니라 `_topo_order`(소스 먼저, 싱크 나중)로 쌓는다.
       이음은 여전히 실제 이음 그대로 건다 — 옛 길처럼 「위아래로 이웃한
       줄은 다 잇는다」로 되돌아가지 않는다. 한 줄에 상자 다섯이 나란히
       서는 사슬(「TSMC → 엔비디아 → … → 최종 사용자」)이 여기로 온다 —
       520 폭에 다섯 칸을 나란히 못 놓으니 위상 정렬 사슬로 세로로 세운다.
    """
    if len(boxes) < 2:
        return None
    rows_sorted = sorted(set(b.row for b in boxes))
    row_idx = {r: i for i, r in enumerate(rows_sorted)}
    row_of = {id(b): row_idx[b.row] for b in boxes}
    band_of, ncol = _col_bands(boxes)
    col_of = {id(b): band_of[b.c0] for b in boxes}
    if 1 <= ncol <= 4:
        svg = _grid_plate_build(boxes, edges, row_of, col_of, ncol, width)
        if svg:
            return svg
    if ncol > 2:
        col_of2 = {i: (0 if c == 0 else 1) for i, c in col_of.items()}
        svg = _grid_plate_build(boxes, edges, row_of, col_of2, 2, width)
        if svg:
            return svg
    order = _topo_order(boxes, edges)
    row_of1 = {id(b): i for i, b in enumerate(order)}
    col_of1 = {id(b): 0 for b in boxes}
    return _grid_plate_build(boxes, edges, row_of1, col_of1, 1, width)


def _graph_plate(block, width=520.0, narrow=False):
    """그래프를 판으로. 자리가 겹치거나 칸이 넷을 넘으면 못 읽은 것으로 되돌린다.

    서로 안 이어진 미니 도식이 한 덩어리에 여럿 있으면(`_weak_groups`) 판을
    여럿 짜서 위아래로 잇는다 — 하나라도 못 앉히면 전부 되돌려 옛 길에 맡긴다.
    한 덩이씩 `_group_plate`(자리가 안 맞으면 열을 줄이거나 위상 정렬로
    쌓는다)를 쓴다 — `narrow` 는 그 판의 폭만 바꾼다. 넓은 판과 좁은 판이
    **같은 그래프**(상자·이음)를 쓰되 자리만 화면 폭에 맞춰 다시 잡는다.
    화면 폭이 바뀐다고 그림의 뜻(누가 누구에게 붙는가)이 바뀌면 안 된다.
    """
    g = _graph_of(block)
    if not g:
        return None
    boxes, edges, notes = g
    # 이음이 하나도 안 닿은 상자는 그래프의 마디가 아니라 소제목·구분줄이다
    # (「기존 방식: 통합 메모리 풀」처럼). 칸에 넣으면 그 넓은 글이 열 폭을
    # 잡아먹어 진짜 마디들이 밀려나거나 판 자체가 폭을 넘는다 — 각주로 내린다
    touched = set()
    for a, b, _ in edges:
        touched.add(id(a))
        touched.add(id(b))
    heads = [b for b in boxes if id(b) not in touched]
    boxes = [b for b in boxes if id(b) in touched]
    if len(boxes) < 2:
        return None
    notes = [h.name + (' — ' + h.sub if h.sub else '') for h in heads] + notes
    # 이음 이름이 길면 같은 줄 이음의 틈(`_need_gap_x`)이 그 글자 폭만큼 벌어져
    # 판 폭을 넘긴다 — 긴 이름은 선 위에 못 얹고 판 아래 각주로 내린다. 좁은
    # 판은 틈이 더 좁으니 문턱도 더 낮춘다
    limit = 55 if narrow else 90
    fixed_edges = []
    for a, b, label in edges:
        if label and fig_layout.text_w(label, fig_layout.FS_S) > limit:
            notes.append(label)
            label = ''
        fixed_edges.append((a, b, label))
    edges = fixed_edges
    groups = _weak_groups(boxes, edges)
    svgs = []
    for grp in groups:
        gset = set(id(b) for b in grp)
        gedges = [e for e in edges if id(e[0]) in gset and id(e[1]) in gset]
        svg = _group_plate(grp, gedges, width)
        if not svg:
            return None            # 한 덩이라도 못 앉히면 전부 옛 길로 되돌린다
        svgs.append(svg)
    # 각주는 빈 판에 못 싣는다(줄이 없으면 `_layout` 이 못 짠다) — 문단으로
    # 마지막 판 뒤에 붙인다. svg 안 각주(`p.note()`)와 달리 판 높이에 안 갇히는
    # <p> 라 개수를 억지로 줄이지 않는다 — 줄이면 `_kept` 가 낱말 빠짐으로 막는다
    seen, uniq = set(), []
    for n in notes:
        if n and n not in seen:
            seen.add(n)
            uniq.append(n)
    if uniq:
        notes_html = ''.join('<p class="fig-note">%s</p>' % _inline(n) for n in uniq)
        return ''.join(svgs) + notes_html
    return ''.join(svgs)


def _split_cols(block):
    """나란히 선 두 판을 가른다. 못 가르면 None.

    받은 도식은 「기존 구조」와 「새 구조」를 좌우로 붙여 그려 오는 일이 잦다. 줄 단위로
    상자를 세면 왼쪽 첫 상자와 오른쪽 첫 상자가 한 줄에 서고, 줄 사이를 잇는 선이
    엉뚱한 상자끼리 대각선으로 그어진다 — 2026-08-31 화면이 그랬다.
    모든 줄에서 빈 칸이 넷 이상 이어지면 그 자리를 두 판의 경계로 본다.
    """
    lines = [ln.rstrip() for ln in block.split(chr(10)) if ln.strip()]
    if len(lines) < 2:
        return None
    grid = [_cells(ln) for ln in lines]
    width = max((c[-1][2] if c else 0) for c in grid)
    used = set()
    for cs in grid:
        for ch, a, b in cs:
            if ch != ' ':
                used.update(range(a, b))
    runs, start, prev = [], None, None
    for c in range(width):
        if c in used:
            if start is not None:
                runs.append((start, prev))
                start = None
            continue
        if start is None:
            start = c
        prev = c
    if start is not None:
        runs.append((start, prev))
    # 세 칸이면 가른다. 모든 줄에서 비어 있어야 하는 조건이 세서 헛나누지 않는다 —
    # 넷으로 잡았더니 틈이 세 칸인 판(할라페뇨 기술 뷰)이 통째로 아스키로 떨어졌다
    cand = [(a, b) for a, b in runs if b - a + 1 >= 3 and a > 6 and b < width - 6]
    if not cand:
        return None
    a, b = max(cand, key=lambda r: r[1] - r[0])
    left = chr(10).join(''.join(ch for ch, s, e in cs if e <= a + 1) for cs in grid)
    right = chr(10).join(''.join(ch for ch, s, e in cs if s > b) for cs in grid)
    if _BOX.search(left) and _BOX.search(right):
        return left, right
    return None


def _rows_of(block):
    """줄마다 [ ... ] 를 뽑아 상자 줄로 만든다. 못 뽑으면 None."""
    rows, notes = [], []
    for ln in _bracketize(block).split(chr(10)):
        toks = _BOX.findall(ln)
        if toks:
            parts = _BOX.split(ln)
            cells = []
            head = _ARROW.sub(' ', parts[0]).strip(' |/·+<>')
            head = head.strip(' \_—-─═│').strip()
            if len(re.findall(r'[가-힣A-Za-z0-9]', head)) >= 2:
                cells.append((head[:20], ''))     # 「Core 1 ── [ … ]」의 왼쪽
            for i, t in enumerate(toks):
                tail = parts[2 * i + 2] if 2 * i + 2 < len(parts) else ''
                tail = _ARROW.sub(' ', tail)
                # 상자 사이를 잇던 선 조각이 설명에 붙어 온다 —
                # 「┼── (트래픽 경합)」처럼 판에 그대로 섰다
                tail = re.sub(r'[─-╿]+', ' ', tail)
                tail = tail.strip(' |/·+<>←↑→↓▲▼').strip()
                cells.append((t.strip(), tail))
            rows.append(cells)
        else:
            # 「- 역할: …」처럼 대시로 시작하는 줄은 바로 앞 상자가 하는 말이다. 각주로
            # 내리면 판 아래에 몰리고 상한(여섯)에 걸려 잘린다 — 그 상자 안에 넣는다
            dash = re.match(r'\s*[-•]\s*(.+)', ln)
            if dash and rows and rows[-1]:
                n, sub = rows[-1][-1]
                add = dash.group(1).strip()
                rows[-1][-1] = (n, (sub + ' · ' + add).strip(' ·') if sub else add)
                continue
            t = _ARROW.sub('', ln).strip(' |/+<>←↑↓▲▼').strip(' \_—-─═│')
            if len(re.findall(r'[가-힣A-Za-z]', t)) >= 4:
                # 한 줄에 캡션 셋을 나란히 쓴 것이 온다 — 넓은 공백을 가운뎃점으로
                # 자르지 않는다. 자른 자리에서 뒷말이 사라진다 — 판 폭에
                # 맞춰 나누는 일은 fig_layout 이 한다
                notes.append(re.sub(r'\s{2,}', ' · ', t))
    if not rows or sum(len(r) for r in rows) < 2:
        return None
    return rows, notes[:6]


def _is_list(block):
    """상자 그림이 아니라 들여쓴 목록인가.

    「Phase 1: …」 아래 「└─ [한계] …」가 붙는 꼴이 온다. 대괄호가 줄머리가 아니라 문장
    속 딱지라, 그대로 구우면 「한계」·「장점」이 주인공 상자가 되고 정작 단계 이름이
    각주로 밀린다 — 2026-08-31 에 Phase 3 이 통째로 판에서 빠졌다. 목록은 안 굽는다.
    """
    head, bullet = 0, 0
    for ln in block.split(chr(10)):
        t = ln.strip()
        if t.startswith('['):
            head += 1
        if t.startswith(('└', '├', '- ', '* ')):
            bullet += 1
    return head == 0 and bullet >= 2


def _narrow_plate(block):
    """좁은 화면용 판.

    넓은 판은 폭 520 을 채우고 글자가 줄어 든다 — 휴대폰에서 상자 이름이 깨알이 된다.
    그래프 길을 먼저 시도한다 — 넓은 판과 같은 상자·이음을 쓰되 폭 340 에
    맞게 자리만 다시 잡는다(`_graph_plate` 의 `narrow` 갈래). 화면이 좁다고
    「연산기 A → B → 풀」처럼 갈래·모임이 사슬로 뒤바뀌면 안 된다 — 그래프가
    안 잡히는 그림만 옛 줄 단위 길(칸을 한 줄로 쌓기)로 내려간다.
    """
    g = _graph_plate(block, width=340.0, narrow=True)
    if g:
        return g
    got = _rows_of(block)
    if not got:
        return None
    rows, notes = got

    def _keep(t):
        return len(re.findall(r'[가-힣A-Za-z0-9]', t)) >= 2
    rows = [[(n, sub if _keep(sub) else '') for n, sub in r if _keep(n)] for r in rows]
    cells = [c for r in rows for c in r]
    if len(cells) < 2:
        return None
    for kw in ({'subout': True}, {}):
        try:
            return _plate([[c] for c in cells], notes, 1, width=340.0, **kw)
        except AssertionError:
            continue
    return None


def _plate_for(block):
    """도식 한 덩어리(가른 뒤의 한쪽도 포함)를 판으로. 그래프 길을 먼저 시도한다.

    격자에서 상자·이음을 읽어 그린 판이 사슬이 아니라 실제 그래프(갈래·모임)를
    담는다 — 되면 그 판을 쓰고, 이음이 안 잡히거나 자리가 겹치면(4-1 칸 넘음 등)
    옛 줄 단위 길로 넘긴다. 옛 길도 같은 낱말 안전망(`_kept`)을 탄다.
    """
    g = _graph_plate(block)
    if g:
        return g
    return _one_plate(block)


def boxes(block):
    """도식 한 덩어리를 판으로. 좌우로 붙여 온 것은 판 둘로 가른다. 못 읽으면 None."""
    # 좌우 가르기가 먼저다. 상자 접기를 먼저 하면 열 정렬이 깨져 나란한 두 판이 한 줄에
    # 쌓인다 — 2026-08-31 에 Traditional 대 Jalapeño 여덟 칸이 세로 사슬로 나갔다
    two = _split_cols(block)
    if not two:
        block = _unframe(block)
        two = _split_cols(block)
    if _is_list(block):
        return None                 # 목록은 받은 꼴 그대로 둔다
    if two:
        a, b = (_plate_for(_unframe(x)) for x in two)
        if a and b:
            return '<div class="fv-two">%s%s</div>' % (a, b)
        return None
    return _plate_for(block)


def _one_plate(block):
    """판 하나. 못 읽으면 None."""
    got = _rows_of(block)
    if not got:
        return None
    rows, notes = got
    # 글자 한둘짜리 칸(「>」·「|」)은 상자가 아니다. 판에 세우면 빈 상자가 하나 선다
    def _keep(t):
        return len(re.findall(r'[가-힣A-Za-z0-9]', t)) >= 2
    rows = [[(n, sub if _keep(sub) else '') for n, sub in r if _keep(n)]
            for r in rows]
    rows = [r for r in rows if r]
    if not rows or sum(len(r) for r in rows) < 2:
        return None
    ncol = max(len(r) for r in rows)
    if ncol > 3:
        return None                 # 한 줄에 넷을 넘으면 판에 안 들어간다
    try:
        return _plate(rows, notes, ncol)
    except AssertionError:
        pass
    # 폭이 모자라면 딸린 설명을 상자 밖 아래에 깔고 다시 굽는다. 설명을 지우지 않는다 —
    # 2026-08-31 에 지웠다가 받은 글의 네 줄이 판에서 사라졌다
    try:
        return _plate(rows, notes, ncol, subout=True)
    except AssertionError:
        pass
    # 폭이 모자라면 세로로 쌓아 다시 굽는다. 이름을 자르지 않는다 — 2026-08-31 에
    # 열넷에서 자르다 「Accelerator Co」와 「re」로 갈린 상자가 그대로 나갔다
    stacked = [[c] for r in rows for c in r]
    try:
        return _plate(stacked, notes, 1)
    except AssertionError:
        return None


def _plate(rows, notes, ncol, subout=False, width=520.0):
    # 판 위아래 여백을 좁힌다. 받은 도식은 카드 본문 사이에 끼는 그림이라 판 자체가
    # 여백을 크게 물면 글과 그림 사이가 벌어져 한 덩어리로 안 읽힌다.
    # 글자 크기도 기본값(15.2/13.5, 다른 장과 공용)이 아니라 카드 본문 크기(13.4/12)로
    # 준다 — 이 판은 카드 글 사이에 끼는 그림이라 본문보다 커 보이면 그림만 튄다
    p = fig_layout.Plate(width=width, subout=subout, top=2.0, gap_y=10.0,
                         pad_y=8.0, bottom=4.0, fs=13.4, fs_s=12.0)
    for r in rows:
        p.row(*(list(r) + [None] * (ncol - len(r))))
    for i in range(len(rows) - 1):
        p.connect(p.at(i, 0), p.at(i + 1, 0))
    for ri, r in enumerate(rows):
        for c in range(1, len(r)):
            p.connect(p.at(ri, c - 1), p.at(ri, c))
    for n in notes:
        p.note(n)
    return p.render('받은 글의 도식')


# 도식이 울타리(```) 없이 그냥 본문에 오는 일이 잦다. 요청하지 않아도 오면 상자로
# 굽는다 — 판 위 글자가 아니라 상자라야 폭에 맞고 다크모드 색이 따라온다.
_DRAW = set('─│┌┐└┘├┤┬┴┼╔╗╚╝═║╭╮╰╯→←↑↓▶◀')
_SKIP = ('#', '>', '|')


def _is_dia(ln):
    """이 한 줄이 도식의 일부인가. 제목·목록·표는 아니다."""
    t = ln.strip()
    if not t or t.startswith(_SKIP):
        return False
    draw = bool(set(t) & _DRAW)
    nbox = len(_BOX.findall(t))
    if t.startswith(('*', '-')) and not draw:
        return False               # 그냥 목록
    if nbox >= 2:
        return True                # [A] → [B] 는 한 줄이어도 도식
    if draw and (nbox or sum(c in _DRAW or c in ' +-' for c in t) >= len(t) * 0.4):
        return True
    return False


def _dia_span(lines, i):
    """i 줄부터 이어지는 도식 덩어리의 끝. 도식이 아니면 i."""
    j = i
    while j < len(lines) and _is_dia(lines[j]):
        j += 1
    # 한 줄짜리는 상자가 둘 이상일 때만 도식으로 본다 (제목 속 대괄호 제외)
    if j - i == 1 and len(_BOX.findall(lines[i])) < 2:
        return i
    return j


def _inline(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s


def _table(rows):
    head, body = rows[0], rows[2:]
    h = ''.join('<th scope="col">%s</th>' % _inline(c) for c in head)
    b = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % _inline(c) for c in r) for r in body)
    return '<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (h, b)


def _groups(block):
    """목록을 (머리, [딸린 줄]) 묶음으로. 머리는 불릿이 아닌 줄이다."""
    out, cur = [], None
    for ln in block.split(chr(10)):
        t = ln.strip()
        if not t or t == 'text':
            continue
        m = re.match(r'[└├]─\s*(.*)', t) or re.match(r'[-*]\s+(.*)', t)
        if m:
            if cur is None:
                cur = ('', [])
                out.append(cur)
            cur[1].append(m.group(1).strip())
        else:
            cur = (t, [])
            out.append(cur)
    return [(h, its) for h, its in out if h]


def _compare_pair(block):
    """대괄호 머리 둘에 각각 글줄이 붙은 대조인가. 맞으면 [(머리, [줄]), …].

    「[전통적 칩 디자인 (2~3년 이상)]」 다음 줄에 그 흐름, 「[OpenAI 할라피뇨 방식(9개월)]」
    다음 줄에 그 흐름이 오는 꼴이다. 차례가 아니라 견줌이라 화살표로 이으면 안 된다 —
    2026-08-31 에 앞뒤를 화살표로 잇고 세로로 쌓아 「전통 → 할라피뇨」로 읽혔다.
    """
    groups, cur = [], None
    for ln in block.split(chr(10)):
        t = ln.strip()
        if not t or t == 'text':
            continue
        if t.startswith('[') and t.endswith(']'):
            cur = (t.strip('[]').strip(), [])
            groups.append(cur)
        elif cur is None or '[' in t:
            return None
        elif _is_dia(t) or set(t) & _DRAW or '+--' in t or '===' in t:
            # 딸린 줄이 그림이면 대조가 아니라 도식이다. 그대로 이으면 그림 한 판이
            # 상자 하나의 설명으로 뭉개져 판 밖으로 넘친다(2026-08-31)
            return None
        else:
            cur[1].append(t)
    if len(groups) == 2 and all(g[1] for g in groups):
        return groups
    return None


def _kept(block, html):
    """구운 판에 원문 낱말이 다 들어갔나. 하나라도 빠지면 판을 못 쓴다.

    파서가 어떤 꼴에서 무엇을 흘리는지는 미리 다 알 수 없다 — 그림 한 줄을 각주로
    내렸다가 상한에 걸려 잘리거나, 한 줄에 칸이 넷이면 판을 포기하는 식이다. 낱말이
    빠진 판은 남의 글을 지운 판이라, 그런 판은 안 쓰고 받은 꼴을 그대로 보인다.
    """
    seen = re.sub(r'\s+', '', re.sub('<[^>]+>', ' ', html))
    for ln in block.split(chr(10)):
        bare = re.sub(r'[│║|┌┐└┘─═+<>▼▲←→↓↑·\[\]\-=*★•]', ' ', ln)
        for w in re.split(r'\s+', bare):
            w = w.strip()
            if len(re.findall(r'[가-힣A-Za-z0-9]', w)) >= 3 and w != 'text':
                if re.sub(r'\s+', '', w) not in seen:
                    return False
    return True


_TITLE_ONLY = re.compile(r'^\[[^\[\]]+\]$')


def _split_title(block):
    """맨 앞줄이 대괄호 하나뿐이면 그 글을 판 제목으로 뗀다. (제목, 나머지).

    「[다이어그램 3: 할라페뇨 스케일 업 네트워크 구조]」처럼 도식 첫 줄에 제목만
    얹어 오는 판이 있다. 그대로 두면 상자를 짤 때 그 줄이 칸 하나로 구워져 안 쓰는
    자리가 하나 생긴다 — 상자에서 빼 판 위에 한 줄로 세운다. 여러 줄 틀(┌│└)에
    제목만 든 판도 같은 꼴이라 먼저 풀어서 본다. 뒤에 다른 상자가 없으면 이 한 줄이
    도식의 전부인 것이니 제목이 아니라 그대로 남긴다.
    """
    body = _unframe(block)
    lines = body.split(chr(10))
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return '', block
    t = lines[i].strip()
    # ┌─┐ 테두리 하나짜리 제목은 `_unframe` 을 지나면 안에 있던 [ … ] 를 다시
    # 대괄호로 감싸 [ [ … ] ] 꼴(겹)이 된다 — `_TITLE_ONLY` 는 홑겹만 알아서
    # 겉 한 겹을 먼저 벗긴다. 안 벗기면 이 줄이 상자로 판에 그대로 섞여 든다
    # (2026-08-27 밸류체인 그림)
    m2 = re.match(r'^\[\s*(\[[^\[\]]+\])\s*\]$', t)
    if m2:
        t = m2.group(1)
    if not _TITLE_ONLY.match(t):
        return '', block
    rest = chr(10).join(lines[:i] + lines[i + 1:])
    if not _BOX.search(rest):
        return '', block
    return t.strip('[]').strip(), rest


# ── 도식 안 이모지를 지운다 ──────────────────────────────────────────────
# 방침: 화면에 이모지를 안 남긴다. 받는 글에는 「이모지는 쓰지 않는다」를 이미
# 프롬프트에 박아 뒀지만, 이미 실린 넉 편에는 남아 있어 파서가 대신 지운다.
# 화살표류는 우리 격자 파서가 이미 아는 문자(→←↑↓)로 바꿔야 이음이 잡히고,
# 채운·빈·꺼진 칸은 뜻이 사는 기호(■·□·▨)로 바꿔야 막대 그림이 살아남는다.
# 그 밖의 그림 이모지는 낱말이 아니라 `_kept`에 안 걸리니 그냥 걷는다.
# 산문에는 안 쓴다 — 도식 덩어리(`_block_html`)에 들어온 글만 여기를 거친다.
_EMOJI_MAP = {
    '➡': '→', '⬅': '←', '⬆': '↑', '⬇': '↓', '↔': '↔', '⇒': '⇒',
    '🟩': '■', '🟢': '■', '🟥': '■', '🔴': '■', '🟦': '■', '🔵': '■',
    '⬜': '□', '⚪': '□',
    '⬛': '▨',
}
# VS16(️)·그 밖의 그림 이모지(이모지·딩뱃·기타 화살표 판)를 마저 지운다.
# 위에서 이미 뜻 있는 문자로 바꾼 것들은 이 대역 밖(→←↑↓·■□▨)이라 안 걸린다
_EMOJI_STRIP = re.compile(
    '[\U0001F300-\U0001FAFF⬀-⯿☀-➿️]')


def _denorm_emoji(block):
    """도식 덩어리의 이모지를 우리 파서가 아는 문자나 칸 기호로 바꾸거나 지운다."""
    for k, v in _EMOJI_MAP.items():
        block = block.replace(k, v)
    return _EMOJI_STRIP.sub('', block)


# 판을 못 짜서 아스키로 남는 도식이 카드 폭을 넘으면 가로 스크롤이 생기는데,
# 스크롤바가 눈에 안 띄어 그냥 잘린 것처럼 읽힌다(2026-08-27). 글자를 지우거나
# 줄을 접지 않고 — 모노스페이스 글꼴 그대로 크기만 줄여 판 폭에 맞춘다. 모노스페이스
# 한 칸의 폭은 글자 크기의 대략 0.6배다(라틴 1칸·한글 2칸이라는 `_cells` 셈과 맞물려,
# 한글도 라틴의 두 배 폭이라 이 비율이 그대로 적용된다)
_MONO_COL_EM = 0.6
_ASCII_SEQ = [0]         # 도식마다 다른 class 이름을 붙이는 데만 쓴다


def _ascii_pre(block):
    """아스키로 남은 도식을 <pre> 로. 가장 긴 줄이 판 폭(520·340)을 넘으면
    그 폭에 맞는 글자 크기를 그 도식만의 class 로 박아 넣는다.
    """
    esc = block.replace('&', '&amp;').replace('<', '&lt;')
    max_cols = 0
    for ln in block.split(chr(10)):
        cells = _cells(ln)
        if cells:
            max_cols = max(max_cols, cells[-1][2])
    if max_cols == 0:
        return '<pre class="fv-pre">%s</pre>' % esc
    # 기본 크기(넓은 화면 .72rem·좁은 화면 .62rem)를 지금 CSS 에서 그대로 가져온다.
    # 이미 다 들어가면(계산값이 기본보다 크면) 손 안 대고 기본 CSS 그대로 쓴다
    base_wide, base_narrow = 0.72 * 16.0, 0.62 * 16.0
    fs_wide = min(base_wide, (520.0 - 24.0) / (max_cols * _MONO_COL_EM))
    fs_narrow = min(base_narrow, (340.0 - 24.0) / (max_cols * _MONO_COL_EM))
    # 9px 아래로는 안 내린다 — 이 장이 이미 쓰는 가장 작은 글자(.62rem≈9.92px)
    # 언저리다. 그 밑으로 줄이면 글자를 지운 것과 다를 바 없이 안 읽힌다.
    # 그래도 다 안 들어가는 줄은 `.fv-pre` 의 overflow-x:auto 로 마저 스크롤한다
    fs_wide, fs_narrow = max(fs_wide, 9.0), max(fs_narrow, 9.0)
    if fs_wide >= base_wide - 0.05 and fs_narrow >= base_narrow - 0.05:
        return '<pre class="fv-pre">%s</pre>' % esc
    _ASCII_SEQ[0] += 1
    cls = 'fv-pre-%d' % _ASCII_SEQ[0]
    # 셀렉터 앞에 .uc-rep 을 또 붙인다 — 전역 CSS 의 `.uc-rep .fv-pre` 와
    # 우선순위가 같으면 뒤에 실린 것이 이기지만, 그 순서에 기대지 않고 확실히
    # 이기도록 특정도를 하나 더 높여 둔다
    style = ('<style>.uc-rep .fv-pre.%s{font-size:%.2fpx}'
             '@media (max-width:640px){.uc-rep .fv-pre.%s{font-size:%.2fpx}}'
             '</style>' % (cls, fs_wide, cls, fs_narrow))
    return style + '<pre class="fv-pre %s">%s</pre>' % (cls, esc)


def _block_html(block):
    """도식 덩어리 하나를 판·글·아스키 중 하나로.

    들여쓴 목록은 그냥 글이다 — 판으로 구우면 딱지가 주인공이 되고(「한계」·「장점」),
    아스키로 두면 읽기 어려운 고정폭 덩어리가 된다. 목록 표시를 불릿으로 바꿔 글로 낸다.
    """
    # 이모지는 여기 하나뿐인 문턱에서 지운다 — 판·아스키 어느 길로 가든,
    # 이 함수를 지난 뒤로는 이모지가 없다고 믿을 수 있다
    block = _denorm_emoji(block)
    if _is_list(block):
        groups = _groups(block)
        # 머리가 둘 이상이면 단계다 — 머리마다 상자 하나를 치고 딸린 줄을 그 안에 넣는다.
        # 단계는 차례가 있으니 상자끼리 이어진다
        # 머리가 대괄호면 나란한 대조다 — 차례가 아니라 견줌이라 화살표로 잇지 않는다.
        # 「[전통적 칩 디자인 (2~3년 이상)]」과 「[OpenAI 할라피뇨 방식 (9개월)]」이 그렇다
        if len(groups) == 2 and all(g[1] and g[0].startswith('[') for g in groups):
            plates = []
            for h, its in groups:
                try:
                    plates.append(_plate([[(h.strip('[]').strip(), ' · '.join(its))]],
                                         [], 1, subout=True))
                except AssertionError:
                    plates = []
                    break
            if len(plates) == 2:
                two = '<div class="fv-two">%s%s</div>' % tuple(plates)
                if _kept(block, two):
                    return two
        if len(groups) >= 2 and all(g[1] for g in groups):
            try:
                plate = _plate([[(h, ' · '.join(its))] for h, its in groups], [], 1,
                               subout=True)
            except AssertionError:
                plate = None
            if plate and _kept(block, plate):
                return plate
        out, items = [], []
        for ln in block.split(chr(10)):
            t = ln.strip()
            if not t or t == 'text':
                continue
            m = re.match(r'[└├]─\s*(.*)', t) or re.match(r'[-*]\s+(.*)', t)
            if m:
                items.append(_inline(m.group(1)))
                continue
            if items:
                out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in items))
                items = []
            out.append('<p>%s</p>' % _inline(t))
        if items:
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % x for x in items))
        return ''.join(out)
    pair = _compare_pair(block)
    if pair:
        plates = []
        for h, its in pair:
            try:
                plates.append(_plate([[(h, ' · '.join(its))]], [], 1, subout=True))
            except AssertionError:
                plates = []
                break
        if len(plates) == 2:
            two = '<div class="fv-two">%s%s</div>' % tuple(plates)
            if _kept(block, two):
                return two
    # 원래 글 그대로 먼저 구워 본다. 여기서 실패하면 아스키로 남을 덩어리다 —
    # 제목을 떼는 손질이 실패작을 판으로 되살리면 안 된다(아스키로 남은 넷은
    # 그대로 둔다는 규칙). 성공했을 때만 제목 줄을 상자에서 빼는 손질을 시도한다
    try:
        svg = boxes(block)
    except Exception:
        svg = None
    if svg and not _kept(block, svg):
        svg = None                  # 낱말을 흘린 판은 안 쓴다
    title = ''
    if svg:
        # 첫 줄이 「[다이어그램 N: …]」 같은 제목 한 줄이면 상자에서 떼고 판 위에
        # 세운다. 뗀 채로 못 구우면(폭 계산이 그 줄에 기대는 판도 있다) 방금 구운
        # 판을 그대로 쓴다 — 제목이 상자 하나로 남는 채가 안전한 대안이다
        t, body = _split_title(block)
        if t:
            try:
                svg2 = boxes(body)
            except Exception:
                svg2 = None
            # 뗀 제목은 판 밖 <p> 로 나가니, 낱말 검사는 그 문단까지 합쳐서 본다 —
            # svg2 만 보면 제목 낱말이 거기 없다는 이유로 늘 걸린다
            head2 = '<p class="fig-title">%s</p>' % _inline(t)
            if svg2 and _kept(block, head2 + svg2):
                svg, title = svg2, t
    if svg:
        head = '<p class="fig-title">%s</p>' % _inline(title) if title else ''
        # 넓은 화면과 좁은 화면에 다른 판을 낸다. 같은 판을 줄이면 글자가 깨알이 된다.
        # 제목을 뗀 판이면 낱말 검사도 head 를 합쳐서 본다 — head 를 빼면 제목
        # 낱말이 small 어디에도 없다는 이유로 늘 걸려 좁은 화면 판을 못 쓴다
        try:
            small = _narrow_plate(body if title else block)
        except Exception:
            small = None
        if small and small != svg and _kept(block, head + small):
            return (head + '<div class="fig-pc">%s</div><div class="fig-mo">%s</div>'
                    % (svg, small))
        return head + svg
    return _ascii_pre(block)


def _place(out, html):
    """판(또는 표)이면 바로 앞 문단 한 개와 자리를 바꾼다.

    받은 글은 설명 문단 다음에 도식이 오는 순서로 온다 — 규칙은 그림을 먼저 보고
    그 아래 설명을 읽는 순서다. 판이나 표를 만들었을 때만 바꾼다. 제목 문단(fv-h)은
    그 판의 이름표라 판보다 앞자리를 지킨다 — `<p>`(class 없는)만 문단으로 본다.
    아스키·목록으로 남은 도식은 순서를 그대로 둔다 — 글로 나온 것이라 원래 자리가 맞다.
    """
    is_fig = html.startswith('<table') or '<svg' in html
    if is_fig and out and re.match(r'^<p>.*</p>$', out[-1], re.S):
        out[-1], para = html, out[-1]
        out.append(para)
        return
    out.append(html)


def to_html(md):
    """마크다운 한 편을 카드 안에 들어갈 조각으로."""
    out, i = [], 0
    lines = md.split('\n')
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].strip().startswith('```'):
                buf.append(lines[j])
                j += 1
            block = '\n'.join(buf)
            _place(out, _block_html(block))
            i = j + 1
            continue
        j = _dia_span(lines, i)
        if j > i:
            block = chr(10).join(lines[i:j])
            _place(out, _block_html(block))
            i = j
            continue
        if ln.lstrip().startswith('|') and '|' in ln[1:]:
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            if len(rows) >= 3:
                _place(out, _table(rows))
            continue
        m = re.match(r'\s*(#{1,6})\s+(.*)', ln)
        if m:
            out.append('<p class="fv-h">%s</p>' % _inline(m.group(2)))
            i += 1
            continue
        if re.match(r'\s*[\*\-]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'\s*[\*\-]\s+', lines[i]):
                # 줄머리 불릿 하나만 걷는다. 앵커 없이 sub 하면 문장 속 굵은 글씨의
                # 별표까지 먹어 「**핵심 평가지표 변경:*'최초」로 짝이 깨진다
                items.append(_inline(re.sub(r'^\s*[\*\-]\s+', '', lines[i])))
                i += 1
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % t for t in items))
            continue
        if ln.strip() in ('', '---'):
            i += 1
            continue
        out.append('<p>%s</p>' % _inline(ln.strip()))
        i += 1
    return ''.join(out)


def body_of(path):
    """머리말(frontmatter)과 우리가 붙인 안내를 뺀 답 본문."""
    s = io.open(path, encoding='utf-8').read()
    if s.startswith('---'):
        s = s[s.index('---', 3) + 3:]
    s = re.sub(r'이 파일은 \*\*미검증 원본\*\*이다\..*?옮긴다\.\n', '', s, flags=re.S)
    return s.strip()



def lead_of(md):
    """답의 첫 문단. 카드 앞면에 세울 글도 받은 글에서만 뽑는다 — 우리가 쓰지 않는다."""
    for ln in md.split(chr(10)):
        t = ln.strip()
        if not t or t.startswith(('#', '|', '```', '*', '-', '>')):
            continue
        t = re.sub(r'\*\*(.+?)\*\*', r'', t)
        t = re.sub(r'`(.+?)`', r'', t)
        if len(re.findall(r'[가-힣]', t)) >= 10:
            return t
    return ''


def view(slug, kind, title, note=''):
    """카드에 끼울 접히는 상자 하나. 받은 글을 그대로 담는다."""
    md = body_of(os.path.join(FRAMES, '%s-%s.md' % (slug, kind)))
    return ('<details class="fv"><summary>%s<span>받은 그대로 · 미검증%s</span></summary>'
            '<div class="fv-b">%s</div></details>' % (title, (' · ' + note) if note else '',
                                                      to_html(md)))


# 받은 아스키를 상자로 구우면 fig_layout 의 판이 나온다. 그 판의 CSS 를 같이 실어야
# 한다 — 안 실으면 상자가 까맣게 칠해지고 글자가 안 보인다(fill 이 var(--surface) 인데
# 그 규칙이 없으면 SVG 기본값인 검정으로 칠한다). 2026-08-31 에 그대로 나갔다
CSS = fig_layout.CSS + '''
/* 좌우로 붙여 온 도식 — 판 둘을 나란히. 좁은 화면에서는 위아래로 */
.uc-rep .fv-two { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin:10px 0; }
@media (max-width:640px) { .uc-rep .fv-two { grid-template-columns:1fr; } }
/* 받은 뷰를 그대로 싣는 상자 */
.uc-rep details.fv { margin:14px 0; border:1px solid var(--line); border-radius:8px;
  background:var(--surface); }
.uc-rep details.fv > summary { cursor:pointer; padding:11px 14px; font-size:.86rem;
  font-weight:800; color:var(--ink); list-style:none; }
.uc-rep details.fv > summary::-webkit-details-marker { display:none; }
.uc-rep details.fv > summary::before { content:"▸ "; color:var(--ink-3); }
.uc-rep details.fv[open] > summary::before { content:"▾ "; }
.uc-rep details.fv > summary span { display:block; margin-top:2px; font-weight:400;
  font-size:.72rem; color:var(--ink-3); }
.uc-rep .fv-b { padding:4px 14px 14px; }
.uc-rep .fv-b p { margin:8px 0; font-size:.84rem; line-height:1.75; color:var(--ink-2); }
.uc-rep .fv-b p.fv-h { margin:14px 0 6px; font-weight:800; color:var(--ink); }
/* 격자 그래프 판이 상자에도 이음에도 못 붙인 글 — 판 아래 각주로 낸다.
   fig_layout.Plate.note() 가 svg 안에 그리는 각주와 같은 자리 뜻이라 비슷하게
   가운데 정렬한 작은 글자로 둔다 */
.uc-rep .fv-b p.fig-note { text-align:center; font-size:.76rem; color:var(--ink-3);
  margin:2px 0 10px; }
.uc-rep .fv-b ul { margin:6px 0; padding-left:18px; }
.uc-rep .fv-b li { font-size:.84rem; line-height:1.75; color:var(--ink-2); margin:0 0 4px; }
.uc-rep .fv-b table { width:100%; border-collapse:collapse; margin:10px 0; font-size:.78rem; }
.uc-rep .fv-b th, .uc-rep .fv-b td { border:1px solid var(--line); padding:6px 8px;
  text-align:left; vertical-align:top; color:var(--ink-2); }
.uc-rep .fv-b th { background:var(--sunk); color:var(--ink); font-weight:800; }
.uc-rep svg[data-fig-layout] { max-width:520px; margin:10px auto; display:block; }
.uc-rep .fig-mo svg[data-fig-layout] { max-width:340px; }
.uc-rep .fig-mo { display:none; }
@media (max-width:640px) {
  .uc-rep .fig-pc { display:none; }
  .uc-rep .fig-mo { display:block; }
  /* 아스키로 남은 도식은 좁은 화면에서 글자를 줄여 가로 스크롤을 줄인다 */
  .uc-rep .fv-pre { font-size:.62rem; line-height:1.5; }
}
.uc-rep .fv-pre { margin:10px 0; padding:10px 12px; border:1px solid var(--line);
  border-radius:6px; background:var(--sunk); overflow-x:auto;
  font:400 .72rem/1.7 ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--ink-2); }
'''


# ── 받은 글을 카드 자리에 맞게 가른다 ───────────────────────────────────────
# 앞머리(회차가 무엇을 다루나)는 포스트 맨 위로 올리고, 꼬리에 붙은 요약·제언은
# 뷰 카드 맨 위로 올린다. 받은 문장은 고치지 않는다 — 자리만 옮긴다.

_HEAD = re.compile(r'\s*#{1,6}\s+(.*)')
# 「요약 및 컨설턴트 제언」처럼 제목 대신 굵은 글씨 한 줄로 오는 일이 잦다
_BOLDLINE = re.compile(r'^\*\*\[?(.+?)\]?\*\*\s*$')
_SUMWORD = re.compile(r'(요약|제언|결론|종합|맺음)')


def _blocks(md):
    """제목 줄을 경계로 덩어리 목록을 만든다. [(머리글 또는 '', 줄 목록)]"""
    out, cur = [], ('', [])
    for ln in md.split(chr(10)):
        m = _HEAD.match(ln)
        b = _BOLDLINE.match(ln.strip())
        if m or (b and _SUMWORD.search(b.group(1))):
            out.append(cur)
            cur = (m.group(1) if m else b.group(1), [ln])
        else:
            cur[1].append(ln)
    out.append(cur)
    return [(h, ls) for h, ls in out if h or ''.join(ls).strip()]


def intro_of(md):
    """첫 제목 앞에 선 앞머리. 이 회차가 무엇을 다루는지를 말하는 자리다."""
    bs = _blocks(md)
    if not bs or bs[0][0]:
        return ''
    return chr(10).join(bs[0][1]).strip()


def split_summary(md):
    """(요약·제언 덩어리, 나머지). 꼬리에 그런 덩어리가 없으면 ('', md).

    꼬리만 본다 — 「전략적 시사점」처럼 가운데 서는 제목까지 걷으면 글 순서가 무너진다.
    """
    bs = _blocks(md)
    if not bs:
        return '', md
    h, ls = bs[-1]
    if h and _SUMWORD.search(h):
        return chr(10).join(ls).strip(), chr(10).join(
            chr(10).join(l) for _, l in ((x[0], x[1]) for x in bs[:-1])).strip()
    # 제목 없이 「**요약하자면,**」로 시작하는 마지막 문단
    body = chr(10).join(ls).rstrip()
    para = body.split(chr(10) * 2)[-1].strip()
    if _SUMWORD.match(re.sub(r'^\*+', '', para)[:4]) or para.startswith('**요약'):
        rest = body[:len(body) - len(para)].rstrip()
        head = chr(10).join(chr(10).join(l) for _, l in bs[:-1])
        return para, (head + chr(10) + rest).strip()
    return '', md

def front_of(path):
    """머리말(frontmatter)을 사전으로. 어느 모델이 쓴 글인지가 여기 있다."""
    s = io.open(path, encoding='utf-8').read()
    if not s.startswith('---'):
        return {}
    head = s[3:s.index('---', 3)]
    out = {}
    for ln in head.split(chr(10)):
        if ':' in ln:
            k, v = ln.split(':', 1)
            out[k.strip()] = v.strip()
    return out


def model_of(path):
    """그 뷰를 쓴 모델 이름. 괄호 안(어떻게 받았나)은 뗀다.

    카드마다 적어 둔다 — 한도가 차면 조용히 낮은 모델로 답이 오는 일이 있어서, 나중에
    어느 카드를 다시 받아야 하는지 화면에서 바로 보여야 한다.
    """
    m = front_of(path).get('model', '')
    return m.split('(')[0].strip() or '모델 미상'
