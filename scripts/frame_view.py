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
_ARROW = re.compile(r'(<[─—=-]+>|-->|→|▶|►|=>|=+>|[─—-]+>|<[─—-]+|[↔⇒])')


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
    # ► (U+25BA, 다른 모델이 ──►로 자주 그려 보낸다)도 ▶ 와 같은 화살촉이다.
    # 여기 없으면 이 화살촉이 낀 선은 방향이 없는 문자로 취급돼 이음이 안 잡힌다
    '►': 'LR',
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
        # 판에서 사라진다 — 2026-08-31 밸류체인 그림이 그랬다. **화살촉 하나만
        # 있어도**(「├─ 후회 계수 높다 ──► Gen 1 …」처럼 사슬 한 토막뿐인 줄) 잇는다
        # — 화살촉 자체가 「여기서 갈린다」는 표시라 두 개를 요구할 이유가 없다.
        # 화살촉이 아예 없이 대시만 두 칸 이상 이어진 줄(「랩 ──── 안 판다」)도
        # 잇는다 — 2026-08-31 「경쟁 관계 세기별 판로」가 그런 화살촉 없는 대조였다
        if not taken and _EDGE.search(ln):
            pos = 0
            for piece in re.split(_EDGE_CAP, ln):
                if not piece or _EDGE.fullmatch(piece):
                    pos += len(piece or '')
                    continue
                # 이름표는 앞뒤 선 부스러기(├─ 의 ├─ 등)와 빈칸을 뗀다 — 실제
                # 이음은 격자 문자 그대로 `_wire_cells` 가 따로 다시 읽으니
                # 이름표에는 안 남겨도 된다. 하지만 **칸(c0·c1)은 조각 원래
                # 자리 그대로** 쓴다 — 이름만 잘라 칸까지 줄이면 「몫  ──」처럼
                # 이름과 선 사이에 빈칸이 둘 이상 낀 줄에서 상자 오른쪽 끝이
                # 선보다 두 칸 넘게 떨어져 `_touches`(빈칸 한 칸까지만 허용)가
                # 못 잇는다(2026-08-31 「OpenAI 전력 예산」 다지관이 그랬다)
                name = piece.strip(_WIRE_CH + ' \t')
                if len(re.findall(r'[가-힣A-Za-z0-9]', name)) >= 2:
                    s0, e0 = pos, pos + len(piece)
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
                    taken.append((s, e))
        # 선 문자가 아예 하나도 없는 줄 통째(「기능 목록(다 넣고 싶다)」 같은
        # 뿌리 제목, 「(A) NVL72 랙 1대 …」 같은 갈래 이름)도 상자 후보로 둔다 —
        # 위아래 줄의 세로선이 이 칸 범위에 닿으면 `_touches` 가 마디로 이어
        # 준다. 안 닿으면(진짜 산문이면) `_graph_plate` 가 손대지 않은 상자를
        # 각주로 내리는 안전망을 이미 갖고 있어 그림이 지어지지 않는다.
        # 폭이 넓은 줄(24 칸 넘음)은 뺀다 — 두 갈래 제목을 한 줄에 큰 공백으로
        # 나란히 적은 줄(「과거 …    현재 및 미래 …」)까지 상자 하나로 삼으면
        # 그 상자가 열 폭을 통째로 먹어 진짜 마디들의 자리를 밀어낸다
        # (2026-08-31 Grok bot 밸류체인이 그렇게 깨졌다). 「text」(울타리 언어
        # 표시)는 상자가 아니다. 낱말다운 이어진 글자가 있어야 한다 — 「v … v」
        # 처럼 화살촉 대용 낱글자만 흩어진 줄(우리 격자가 모르는 ASCII 표시)을
        # 상자로 세우면 안 된다
        if not taken and not (set(ln) & _WIRE):
            text = ln.strip()
            if (text and text != 'text'
                    and re.search(r'[가-힣]{2,}|[A-Za-z]{3,}|[0-9]{2,}', text)):
                s = len(ln) - len(ln.lstrip())
                e = s + len(text)
                c0, c1 = col_of(s), _end_col(e, cells)
                if c1 - c0 <= 24:
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


_ARROWHEAD = frozenset('▲▼◀▶►→←↑↓<>')

# 대괄호 없는 줄 안에서 낱말 사슬을 가르는 자리(`_graph_boxes` 가 쓴다).
# 화살촉 문자는 하나만 있어도 이음이다 — 그 자체가 「여기서 갈린다」는
# 표시라 두 개를 요구할 이유가 없다(「├─ 후회 계수 높다 ──► Gen 1 …」처럼
# 사슬 한 토막뿐인 줄도 있다). 화살촉이 없으면 선 문자가 두 칸 이상 이어질
# 때만 이음으로 본다 — 「Gen 1 = Jalapeño」의 「=」 하나, 「23~24 Gb/s」의
# 「~」 하나처럼 낱말 속에 낀 문자 하나까지 자르면 안 된다(화살촉 없는
# 대시 대조 「랩 ──── 안 판다」는 두 칸짜리 대시 이음으로 잡힌다)
_EDGE = re.compile(r'[%s]|[%s]{2,}' % (re.escape(''.join(_ARROWHEAD)), re.escape(_WIRE_CH)))
_EDGE_CAP = re.compile('(%s)' % _EDGE.pattern)


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
_ARROW_DIR = {'<': 'L', '◀': 'L', '>': 'R', '▶': 'R', '►': 'R', '←': 'L', '→': 'R',
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


def _grid_plate_build(boxes, edges, row_of, col_of, ncol, width, wrap_label=False):
    """자리(row_of·col_of, 상자 id 로 찾는다)가 이미 정해진 상자들을 판 하나로 굽는다.

    좁은 판(열을 줄이거나 한 칸으로 쌓은 것)과 넓은 판이 이 함수 하나를 같이
    쓴다 — 자리를 어떻게 셈했든 판을 짜고 이음을 거는 마지막 손은 하나여야
    한다. 자리가 겹치거나 폭을 넘으면 None.

    `wrap_label` 이면 상자 이름이 칸 폭을 넘을 때 칸 수를 줄이는 대신 상자
    안에서 이름을 여러 줄로 접는다(`fig_layout.wrap`) — 형제 상자(분기·합류)를
    같은 행에 세운 채로 긴 이름을 담을 때 쓴다.
    """
    grid = {}
    for b in boxes:
        key = (row_of[id(b)], col_of[id(b)])
        if key in grid:
            return None           # 자리가 겹치면 읽은 자리를 못 믿는 것이니 되돌린다
        grid[key] = b
    nrow = len(set(row_of.values()))
    p = fig_layout.Plate(width=width, subout=False, top=2.0, gap_y=10.0,
                         pad_y=8.0, bottom=4.0, fs=13.4, fs_s=12.0,
                         wrap_label=wrap_label)
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


def _topo_levels(boxes, edges):
    """소스가 먼저인 파도(레벨)로 나눈다. 한 파도 안 순서는 원문 줄 순서.

    `_topo_order` 와 같은 위상 정렬(Kahn)이지만, 한 파도(같은 깊이)를 낱개로
    펴지 않고 그대로 둔다 — 한 상자에서 갈린 형제(같은 부모에서 나간 자식,
    또는 같은 자식으로 모이는 부모)는 부모의 깊이 하나만큼만 떨어져 있으므로
    이 셈으로 **저절로 같은 파도**에 들어온다. 파도를 낱개로 펴서 한 칸으로
    쌓으면(옛 `_topo_order` 를 그대로 한 줄씩 쓰던 방식) 그 형제가 서로 다른
    줄에 갈려 갈래가 사슬로 보인다 — 2026-09-01, 「폐쇄형/개방형 전략」이
    세로로 이어진 사고가 이렇게 났다.
    """
    ids = [id(b) for b in boxes]
    by_id = {id(b): b for b in boxes}
    indeg = {i: 0 for i in ids}
    out = {i: [] for i in ids}
    for a, b, _ in edges:
        if id(a) in indeg and id(b) in indeg:
            indeg[id(b)] += 1
            out[id(a)].append(id(b))
    seen = set()
    levels = []
    frontier = [i for i in ids if indeg[i] == 0]
    while frontier:
        frontier.sort(key=lambda i: (by_id[i].row, by_id[i].c0))
        levels.append([by_id[i] for i in frontier])
        seen.update(frontier)
        for i in frontier:
            for j in out[i]:
                indeg[j] -= 1
        frontier = [i for i in ids if i not in seen and indeg[i] == 0]
    remaining = [by_id[i] for i in ids if i not in seen]
    if remaining:            # 고리 등 위상 정렬로 못 다룬 것은 안전망으로 맨 끝에
        levels.append(remaining)
    return levels


def _group_plate(boxes, edges, width):
    """상자·이음 한 덩이(서로 이어진 것들)를 판 하나로. 자리가 안 맞으면 셋을
    차례로 시도한다. 넓은 판(520)·좁은 판(340) 둘 다 이 하나를 쓴다.

    ① 원래 자리(행·열) 그대로 앉혀 본다 — 칸이 넷 이하고 이름이 짧으면
       이걸로 된다.
    ② 안 되면 왼쪽 첫 열만 남기고 나머지 열을 하나로 합친다 — 칸 수를
       줄이지만 이음은 그대로다.
    ③ 그래도 안 되면(칸이 넷을 넘거나 ②도 자리가 겹치면) `_topo_levels`(소스
       먼저, 싱크 나중인 파도)로 자리를 다시 잡는다. **파도가 곧 행이고, 한
       파도 안 형제는 늘 같은 행에 나란히 선다** — 파도를 쪼개 한 칸씩
       쌓지 않는다. 이름이 길어 그 행이 폭을 넘으면 칸 수를 줄이는 대신
       상자 안에서 이름을 접는다(`wrap_label`). 그래도 안 되면(파도 하나가
       낱말 하나로도 폭을 넘길 만큼 넓다) 판을 포기한다 — 갈래를 사슬로
       바꾸는 대신 이전 길(줄 단위 판·글)로 물러난다. 한 줄에 상자 다섯이
       나란히 서는 사슬(「TSMC → 엔비디아 → … → 최종 사용자」)처럼 파도마다
       상자가 하나뿐인 도식은 이 계산이 옛 `_topo_order`와 같은 결과를 낸다
       — 사슬은 그대로 사슬로, 갈래만 갈래로 남는다.
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
    levels = _topo_levels(boxes, edges)
    row_of3, col_of3, ncol3 = {}, {}, 1
    for ri, lv in enumerate(levels):
        ncol3 = max(ncol3, len(lv))
        for ci, b in enumerate(lv):
            row_of3[id(b)] = ri
            col_of3[id(b)] = ci
    for wrap_label in (False, True):
        svg = _grid_plate_build(boxes, edges, row_of3, col_of3, ncol3, width,
                                wrap_label=wrap_label)
        if svg:
            return svg
    return None


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
    # 이은 상자보다 못 이은 상자(각주로 내려간 것)가 더 많으면 그래프로 읽은
    # 것 자체를 못 믿는다 — 진짜 그래프라면 마디 대부분이 이어져 있어야 한다.
    # 헐거운 이음 한둘만 건지고 나머지를 각주 더미로 흘리면(`_one_plate`가
    # 이미 온전히 읽는 표를 그래프가 어설프게 가로챈 꼴) 되돌려서 줄 단위 표
    # (`_one_plate`)로 넘긴다 — 2026-08-31 Grok bot 밸류체인이 그렇게 상자
    # 열 개 중 여덟이 각주로 흩어질 뻔했다
    if len(heads) > len(boxes):
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
    if cand:
        a, b = max(cand, key=lambda r: r[1] - r[0])
        left = chr(10).join(''.join(ch for ch, s, e in cs if e <= a + 1) for cs in grid)
        right = chr(10).join(''.join(ch for ch, s, e in cs if s > b) for cs in grid)
        if _BOX.search(left) and _BOX.search(right):
            return left, right
    # 밑줄 행이 경계를 대놓고 알려 주는 판이 있다 — 「────────    ────────」처럼
    # 두 덩이로 갈린 줄이다. 그 아래 단에서 한쪽 열만 남아 두 열 구조가 깨져도
    # (2026-08-31 「표준 칩 개발 대 Jalapeño」) 이 줄 하나면 어디서 갈렸는지 안다
    for cs in grid:
        segs, run = [], None
        for ch, a, b in cs:
            if ch in '─═-_':
                run = a if run is None else run
            else:
                if run is not None and a - run >= 6:
                    segs.append((run, a))
                run = None
        if run is not None and cs and cs[-1][2] - run >= 6:
            segs.append((run, cs[-1][2]))
        if len(segs) >= 2:
            edge = (segs[0][1] + segs[1][0]) / 2.0

            def _cut_at(c):
                """그 줄에서 경계에 가장 가까운 빈 자리. 낱말 가운데는 안 자른다.

                왼쪽 열 내용이 제 밑줄보다 넓게 삐져나오는 판이 있다(2026-08-31
                「표준 칩 개발 대 Jalapeño」). 경계 칸으로 곧장 자르면 「테이프아 / 웃」
                처럼 낱말이 갈린다 — 그 줄이 만든 공백에서 자른다.
                """
                gaps, run = [], None
                for ch, a, _b in c:
                    if ch == ' ':
                        run = a if run is None else run
                    else:
                        if run is not None and a - run >= 2:
                            gaps.append((run + a) / 2.0)
                        run = None
                if not gaps:
                    # 빈 자리가 없는 줄은 통째로 한쪽에 둔다. 시작 칸으로 어느 쪽인지 정한다
                    return 0.0 if (c and c[0][1] >= edge) else 10 ** 6
                return min(gaps, key=lambda g: abs(g - edge))

            cuts = [_cut_at(c) for c in grid]
            left = chr(10).join(''.join(ch for ch, s2, e in c if s2 < cut)
                                for c, cut in zip(grid, cuts))
            right = chr(10).join(''.join(ch for ch, s2, e in c if s2 >= cut)
                                 for c, cut in zip(grid, cuts))
            if len(re.findall(r'[가-힣A-Za-z0-9]', left)) >= 6                     and len(re.findall(r'[가-힣A-Za-z0-9]', right)) >= 6:
                return left, right

    # 모든 줄에서 똑같이 비어 있는 자리가 없는 판이다 — 아래 단(사람이 사는
    # 낱말을 넣은 줄, 「하이퍼스케일러 · AI 랩  ← 이 사람이」)이 위 단(머리
    # 줄)보다 넓어 경계 자리를 침범하면 전 줄에서 안 비니 위 방법이 못 가른다
    # (2026-08-27 「판매사 모델 대 수직 통합 모델」). 머리 줄의 대괄호 둘 사이
    # 가운데를 기준 칸으로 잡고, 줄마다 그 칸에 가장 가까운 큰 공백에서 가른다
    # — 표 한 줄을 자르는 것과 같은 이치다(`_row_cut`)
    # 이 블록 전체의 대괄호가 정확히 두 무리(왼쪽 열·오른쪽 열)로 뭉치는지부터
    # 본다 — 안 그러면 「대괄호 둘 있는 줄 아무거나」에 걸려, 한 사슬 안에서
    # 상자 둘이 이웃한 줄(「A ──> [B] ──> [C]」)까지 좌우 두 판으로 잘못 가른다.
    # 2026-08-24 그록봇 다이아몬드 그림이 그렇게 낱말 한가운데서 갈렸다
    # (「AI 워크로드 (Grok bo | t 아키텍처 적용)]」)
    all_cols = []
    for ln in lines:
        cs = _cells(ln)
        for m in _BOX.finditer(ln):
            if m.start() < len(cs):
                all_cols.append(cs[m.start()][1])
    if len(all_cols) < 2:
        return None
    bands = []
    for x in sorted(set(all_cols)):
        if bands and x - bands[-1][-1] <= 8:
            bands[-1].append(x)
        else:
            bands.append([x])
    if len(bands) != 2:
        return None
    c0, c1 = bands[0][0], bands[1][0]
    if c1 - c0 < 6:
        return None
    # 두 무리 사이 틈에 선 문자가 양쪽 다 걸치는 줄이 있으면 좌우가 진짜로
    # 이어진 그림이다 — 나란한 두 판이 아니라 한 판 안에서 상자 둘이 선으로
    # 붙은 것(팬인 등)이다. 그런 줄이 있으면 안 가른다(2026-08-27 「연산기
    # A·B·C → 공유 풀」이 이 틈에 걸친 선 때문에 대괄호가 두 무리로 보였다)
    wire = set('─│┌┐└┘├┤┬┴┼→←↑↓▲▼◀▶═║')
    mid = (c0 + c1) // 2
    for ln in lines:
        cs = _cells(ln)
        left_hit = any(c0 <= a < mid and ch in wire for ch, a, _e in cs)
        right_hit = any(mid <= a < c1 and ch in wire for ch, a, _e in cs)
        if left_hit and right_hit:
            return None
    target = (c0 + c1) // 2
    left_lines, right_lines = [], []
    for cs in grid:
        if not cs:
            left_lines.append('')
            right_lines.append('')
            continue
        gaps = _gaps(cs)
        cut = min(gaps, key=lambda g: abs(g - target)) if gaps else target
        left_lines.append(''.join(ch for ch, s, e in cs if e <= cut))
        right_lines.append(''.join(ch for ch, s, e in cs if s >= cut))
    left = chr(10).join(left_lines)
    right = chr(10).join(right_lines)
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
            # 「- 역할: …」·「└─ 대역폭: …」처럼 대시나 └─·├─ 로 시작하는 줄은
            # 바로 앞 상자가 하는 말이다. 각주로 내리면 판 아래에 몰리고 상한
            # (여섯)에 걸려 잘린다 — 그 상자 안에 넣는다. 나무 꼴 줄머리(└├)를
            # 안 받으면 「[Tier 2: …]」 다음 줄 「└─ 대역폭: …」이 상자에 안
            # 붙고 각주로 떨어져, 정작 있어야 할 Tier 2 → Tier 1 사슬이
            # 상자 둘만 남은 반쪽 사슬로 준다(2026-08-31 스케일업 네트워크)
            dash = re.match(r'\s*[-•]\s*(.+)', ln) or re.match(r'\s*[└├]─\s*(.+)', ln)
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
    if two:
        a, b = (_plate_for(_unframe(x)) for x in two)
        if a and b:
            return '<div class="fv-two">%s%s</div>' % (a, b)
        return None
    # 목록 판정보다 판 시도가 먼저다. 줄머리가 ├─·└─ 라도(`_is_list` 가 보는
    # 표시) 실은 상자 그림인 일이 잦다 — 2026-08-31 「기능 목록」이 그래프로는
    # 다 읽히는데 목록 판정에 먼저 걸려 「│」한 줄이 빈 불릿으로 섰다. 그래프도
    # 줄 단위 판(`_one_plate`)도 다 못 읽어야(`_plate_for` 가 None) 그때
    # `_block_html` 이 목록·글로 내려간다 — 자체 안전망(`_kept`)이 낱말을
    # 흘린 판은 이미 걸러 준다
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
    # 표 한 칸에 여러 줄을 담을 길은 마크다운에 `<br>` 뿐이다. 받은 답이 목차 칸에
    # 절을 여러 줄로 넣을 때 그걸 쓴다 — 통째로 escape 하면 화면에 「<br>」이 글자로
    # 찍힌다(2026-09-01, 제미나이 그록봇 목차). 이 한 태그만 되돌린다
    s = re.sub(r'&lt;br\s*/?&gt;', '<br>', s, flags=re.I)
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
        # mermaid 노드 꼴(원·마름모)이 쓰는 ()·{} 도 지운다 — 안 지우면 「E{정확도」처럼
        # 물음표 노드의 여는 중괄호가 낱말에 눌어붙어, 판이 이름을 제대로 실었어도
        # 이 안전망이 헛걸린다(2026-09-01). 따옴표도 같다 — 이름에 빈칸이 들면
        # mermaid 가 `A["구매 부서"]` 로 한 겹 더 감싸는데, 그 따옴표를 표기로 안 보면
        # 판이 이름을 제대로 실어도 「"구매」가 빠진 낱말로 잡혀 판이 통째로 버려진다
        # 밑줄도 표기다 — mermaid id 를 「작업별_랙_분리」로 쓰면 판에는 「작업별 랙
        # 분리」로 서는데, 밑줄째 한 낱말로 세면 빠진 낱말로 잡혀 판이 통째로 버려진다
        # (2026-09-01, 영문 병기를 막자 받은 답이 id 를 한글로 쓰기 시작했다)
        bare = re.sub(r'[│║|┌┐└┘─═+<>▼▲←→↓↑·\[\]\-=*★•━┼┴┬├┤►(){}"\'_]', ' ', ln)
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
    # 울타리 언어 표시(```text)가 도식 첫 줄로 그대로 들어오는 일이 있다 —
    # 빈 줄과 똑같이 건너뛴다. 안 건너뛰면 「text」자체가 「제목 아님」으로
    # 읽혀 진짜 제목 줄(「[다이어그램 3: …]」)을 못 찾는다(2026-08-31)
    while i < len(lines) and (not lines[i].strip() or lines[i].strip() == 'text'):
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


# ── mermaid flowchart 표기 ───────────────────────────────────────────────
# 아스키 격자 파서(위)는 화살촉·테두리 문자 꼴이 매번 달라져 규칙이 계속
# 늘었다. mermaid flowchart 는 문법이 고정돼 있어 정규식 몇 줄로 노드·이음을
# 읽는다. 시험판과 그 근거는 `insights/frames/exp/mermaid_plate.py` ·
# `insights/frames/exp/2026-08-27-openai-jalapeno-strategy-mermaid.md` — 이
# 아래는 그 시험을 운영으로 그대로 옮긴 것이다. 자리 배치 상수도 같다: 넓은
# 판 520 · 좁은 판 340 · fs=13.4, fs_s=12.0 · top=2, gap_y=10, pad_y=8,
# bottom=4 · 분기는 나란히(`_mm_topo_levels`) · 폭 모자라면 wrap_label.
# `fig_layout` 모듈 상수는 고치지 않는다 — 필요한 값은 `Plate(...)` 인자로만.
#
# 읽는 것은 셋뿐이다 — ```mermaid 안의 flowchart 줄, 노드 선언(`A[이름]` ·
# `A(이름)` · `A{이름}`), 이음(`A --> B` · `A -->|라벨| B` · `A --- B`).
# subgraph·style·classDef·class·click·linkStyle·%% 주석은 그 줄만 건너뛴다.
_MM_HEAD = re.compile(r'^\s*(flowchart|graph)\s+(LR|TD|TB|BT|RL)\s*$', re.I | re.M)
_MM_SKIP_LINE = re.compile(
    r'^\s*(flowchart\b|graph\b|subgraph\b|end\s*$|direction\b|style\b|classDef\b|'
    r'class\b|click\b|linkStyle\b|%%)', re.I)
# id 에 한글이 온다. mermaid 는 허용하고, 받은 답이 실제로 그렇게 쓴다 —
# 「작업별_랙_분리[작업별 랙 분리]」(2026-09-01, 영문 병기를 막자 id 까지 한글로 왔다).
# 영숫자만 보면 그 줄의 이음이 통째로 안 읽혀 판이 버려진다
_MM_ID = r'[A-Za-z0-9_가-힣]+'
_MM_BR = r'(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\})'
_MM_DECL = re.compile(r'^\s*(%s)\s*%s\s*$' % (_MM_ID, _MM_BR))
_MM_EDGE = re.compile(
    r'^\s*(%s)\s*%s?\s*(-->|---)\s*(?:\|([^|]+)\|\s*)?(%s)\s*%s?'
    % (_MM_ID, _MM_BR, _MM_ID, _MM_BR))
# 독립 검산(`mermaid_verify`)에 쓰는 단순 잣대 — 문법 파서와 다른 경로로
# 화살표 수·선언 id 집합을 다시 센다
_MM_ARROW_COUNT = re.compile(r'-->|---')
_MM_ANY_DECL = re.compile(r'(%s)\s*%s' % (_MM_ID, _MM_BR))

# mermaid 화살표 표기는 셋을 넘게 섞여 온다 — 실선(`-->`)뿐 아니라 양방향
# (`<-->`)·대시 사이에 낀 라벨(`--라벨-->`, 파이프 없이)까지 원문이 쓴다
# (2026-09-01, 그록봇 기술 뷰의 「과거: 단순 추론 파이프라인」 도식이 그랬다).
# 파서에 넣기 전에 이 둘을 우리가 아는 꼴로 정규화한다 — 양방향은 방향을
# 무시하고 보통 이음으로, 대시-라벨-대시는 파이프 라벨(`-->|라벨|`)로 바꾼다
_MM_BIDIR = re.compile(r'<-->')
_MM_INLINE_LABEL = re.compile(r'--([^->][^-]*?)-->')
# 점선 이음. 받은 답이 「안 일어나는 쪽」을 점선으로 그린다 — `A -. "라벨" .-> B` 와
# `A -.-> B` 둘 다 온다(2026-09-01, 다크 실리콘 판). 우리는 선 꼴을 안 가리므로
# 보통 이음으로 바꾼다. 라벨은 파이프 꼴로 옮겨 낱말을 안 잃는다
_MM_DOT_LABEL = re.compile(r'-\.\s*"?([^"\n]*?)"?\s*\.->')
_MM_DOT = re.compile(r'-\.->')
# 겹괄호(원 노드) `A(("이름"))` 는 홑괄호와 같은 자리다. 안쪽만 남긴다
_MM_DBL_PAREN = re.compile(r'\(\((.*?)\)\)')
# `--> |라벨|` 처럼 화살표와 파이프 사이에 빈칸이 끼어 온다. 붙여 놓는다
_MM_PIPE_GAP = re.compile(r'(-->|---)\s+\|')


# 이음을 한 줄에 이어 쓴 꼴(`A --> B --> C`)을 낱개 줄로 편다. 우리 이음 규칙은
# 줄 하나에 이음 하나라, 안 펴면 첫 이음만 읽히고 뒤 상자가 통째로 사라진다 —
# 그러면 낱말 검사(`_kept`)가 판을 버리고 글로도 못 풀어 원본이 목록으로 찍힌다
# (2026-09-01, 제미나이 그록봇 「하드웨어 구매 → 소프트웨어 설치 → 직접 유지보수」)
_MM_ARROW_SPLIT = re.compile(r'(-->\|[^|]*\||-->|---)')


def _mm_chain(ln):
    """`A --> B --> C` 를 `A --> B` · `B --> C` 두 줄로. 이음이 하나면 그대로."""
    parts = _MM_ARROW_SPLIT.split(ln)
    if len(parts) < 5:                      # 노드·이음·노드 = 셋이면 이음 하나뿐이다
        return [ln]
    head = parts[0][:len(parts[0]) - len(parts[0].lstrip())]
    nodes = [parts[i].strip() for i in range(0, len(parts), 2)]
    ops = [parts[i] for i in range(1, len(parts), 2)]
    if not all(nodes):                      # 빈 자리가 있으면 손대지 않는다
        return [ln]
    return [head + nodes[i] + ' ' + ops[i] + ' ' + nodes[i + 1]
            for i in range(len(ops))]


def _mm_normalize(block):
    """줄마다 우리 파서가 모르는 표기를 아는 꼴로 바꾼다.

    받는 쪽이 mermaid 표기를 골고루 쓴다 — 양방향·점선·겹괄호·대시 사이 라벨·화살표와
    파이프 사이 빈칸까지. 못 읽는 표기가 하나 오면 그 줄의 이음이 통째로 사라지고,
    낱말 검사가 판을 버려 원본이 목록으로 찍힌다. 선 꼴(실선·점선)은 우리가 안 가리므로
    전부 보통 이음으로 모은다 — 잃는 것은 선 모양이고 지키는 것은 낱말이다.
    """
    out = []
    for ln in block.split(chr(10)):
        ln = _MM_DOT_LABEL.sub(lambda m: '-->|%s|' % m.group(1).strip(), ln)
        ln = _MM_DOT.sub('-->', ln)
        ln = _MM_DBL_PAREN.sub(lambda m: '(%s)' % m.group(1), ln)
        ln = _MM_PIPE_GAP.sub(lambda m: m.group(1) + '|', ln)
        ln = _MM_BIDIR.sub('-->', ln)
        ln = _MM_INLINE_LABEL.sub(lambda m: '-->|%s|' % m.group(1).strip(), ln)
        out.extend(_mm_chain(ln))
    return chr(10).join(out)


def _mm_fanout(ln):
    """`A & B & C --> D`(여러 시작점이 이음 하나를 공유)를 낱개 이음 줄로 편다.

    안 펴면 그 줄 전체가 우리 이음 규칙(시작 하나 · 끝 하나)에 안 맞아
    통째로 버려지고, 그 이음에 달린 라벨(「결과 취합」 같은)까지 함께
    사라진다. 여러 줄로 펴면 형제 상자 하나하나에 같은 라벨이 달리지만
    — 뜻은 그대로고 낱말은 하나도 안 잃는다.
    """
    if '&' not in ln:
        return [ln]
    m = _MM_ARROW_COUNT.search(ln)
    if not m:
        return [ln]
    left = ln[:m.start()]
    if '&' not in left:
        return [ln]           # & 가 화살표 오른쪽(받는 쪽)에 있으면 손 안 댄다
    rest = ln[m.start():]
    srcs = [s.strip() for s in left.split('&') if s.strip()]
    if len(srcs) < 2:
        return [ln]
    return [s + ' ' + rest for s in srcs]


def _is_mermaid_block(block):
    """```mermaid 안쪽 글인가 — 첫 줄이 flowchart 방향 선언이면 그렇다."""
    return bool(_MM_HEAD.search(block))


def _mm_unquote(t):
    """이름을 감싼 따옴표를 벗긴다.

    mermaid 는 이름에 빈칸이나 문장부호가 들면 `A["이름"]` 처럼 따옴표로 한 겹 더
    감싼다. 그 따옴표는 표기이지 이름이 아니다 — 안 벗기면 구운 판에 `"구매 부서"`
    로 찍힌다(2026-09-01, 판 열일곱이 다 그랬다).
    """
    while len(t) > 1 and t[0] == t[-1] and t[0] in (chr(34), chr(39)):
        t = t[1:-1].strip()
    return t


def _mm_bracket_text(s):
    """`[이름]`·`(이름)`·`{이름}` 에서 안쪽 글자만 뽑는다.

    이름 안에 줄바꿈 표기(역슬래시 n)가 글자로 들어오는 일이 있다 —
    `GPU\\n추론 및 의사결정`(2026-09-01). 그대로 두면 한 줄로 붙어 상자가 지나치게
    넓어지고, 그 넓은 상자를 선이 지나간다. 빈칸으로 바꾸면 `wrap_label` 이 알아서
    접는다 — 어차피 우리가 상자 폭에 맞춰 다시 나눈다
    """
    if not s:
        return None
    t = _mm_unquote(s[1:-1].strip())
    return re.sub(r'\\+n', ' ', t).strip()


# subgraph 줄은 `subgraph 제목` 으로도 오고 `subgraph V["제목"]` 으로도 온다.
# id 와 괄호는 표기이지 제목이 아니다 — 통째로 받으면 캡션에 `V["설계 주체 —
# 칩 벤더"]` 가 그대로 찍힌다(2026-09-01)
# subgraph 는 두 꼴로 온다 — `subgraph id ["제목"]` 과 `subgraph 제목`.
# 한 정규식에 담고 id 를 선택으로 두면, id 에 한글이 허용된 뒤로 제목 없는 꼴의
# **첫 낱말을 id 로 먹는다**(2026-09-01, 「메모리 접근 — NUMA」가 「접근 — NUMA」로
# 잘렸다). 괄호가 붙은 꼴을 먼저 보고, 안 맞으면 뒤를 통째로 제목으로 받는다
_MM_SUBGRAPH_ID = re.compile(
    r'^\s*subgraph\s+(?:%s\s+)?(\[[^\]]+\]|"[^"]+")\s*$' % _MM_ID, re.I)
_MM_SUBGRAPH = re.compile(r'^\s*subgraph\s+(.+?)\s*$', re.I)
_MM_END = re.compile(r'^\s*end\s*$', re.I)


class _MGraph(object):
    """mermaid flowchart 하나에서 읽은 노드·이음."""

    def __init__(self):
        self.names = {}     # id -> 이름(대괄호가 없으면 id 그대로)
        self.order = []     # 처음 나온 차례
        self.edges = []     # (src_id, dst_id, label)
        self.title_of = {}  # id -> 그 노드가 든 subgraph 제목(있으면)
        self.direction = 'TD'   # flowchart 머리에 적힌 방향. LR 이면 파도를 열로 세운다

    def _register(self, nid, disp, title=None):
        if nid not in self.names:
            # 이름을 따로 안 붙이고 id 를 이름처럼 쓰는 판이 온다 —
            # 「사전채우기_전용랙 --> 작업량_변동1」. 뜻은 다 있고 밑줄만 mermaid 표기다.
            # 그대로 세우면 화면에 밑줄이 찍히니 빈칸으로 편다(2026-09-01)
            self.names[nid] = disp or (nid.replace('_', ' ') if '_' in nid else nid)
            self.order.append(nid)
        elif disp and self.names[nid] == nid:
            self.names[nid] = disp   # 맨몸으로 먼저 나온 id 에 뒤늦게 이름이 붙었다
        if title and nid not in self.title_of:
            self.title_of[nid] = title


def _mm_parse(block):
    """```mermaid ... ``` 안쪽 글 하나를 _MGraph 로 읽는다.

    `subgraph 제목 ... end` 는 그 줄 자체(제어 줄)는 안 읽지만, **제목은
    그 안에 든 노드에 매달아 둔다** — 「과거: 로컬 구축형」·「현재: 클라우드
    구독형」처럼 두 덩이를 가르는 이름이 통째로 사라지면 안 된다. 판을 짤 때
    한 덩이(약한 연결 성분)의 노드가 모두 같은 제목을 달고 있으면 그 제목을
    판 위 캡션으로 올린다(`_mm_to_plate`).
    """
    g = _MGraph()
    mh = _MM_HEAD.search(block)
    if mh:
        g.direction = mh.group(2).upper()
    stack = []
    for raw_ln in _mm_normalize(block).split(chr(10)):
        if not raw_ln.strip():
            continue
        # subgraph·end 는 펴기 전(원래 한 줄)에 먼저 본다 — 펴는 대상은
        # 이음 줄뿐이라 제어 줄에는 `&` 가 없다
        sm = _MM_SUBGRAPH_ID.match(raw_ln) or _MM_SUBGRAPH.match(raw_ln)
        if sm:
            t = sm.group(1).strip()
            if len(t) > 1 and t[0] == '[' and t[-1] == ']':
                t = t[1:-1].strip()
            stack.append(_mm_unquote(t))
            continue
        if _MM_END.match(raw_ln):
            if stack:
                stack.pop()
            continue
        if _MM_SKIP_LINE.match(raw_ln):
            continue
        title = stack[-1] if stack else None
        for ln in _mm_fanout(raw_ln):
            m = _MM_EDGE.match(ln)
            if m:
                sid, sbr, arrow, label, tid, tbr = m.groups()
                g._register(sid, _mm_bracket_text(sbr), title)
                g._register(tid, _mm_bracket_text(tbr), title)
                g.edges.append((sid, tid, (label or '').strip()))
                continue
            m2 = _MM_DECL.match(ln)
            if m2:
                nid, br = m2.group(1), m2.group(2)
                g._register(nid, _mm_bracket_text(br), title)
                continue
            # 그 밖(주석 안 걸린 산문 등)은 노드도 이음도 아니다
    return g


def _mm_topo_levels(order, edges):
    """소스가 먼저인 파도(레벨)로 나눈다. 한 파도 안 순서는 원문 등장 차례.

    파도를 낱개로 펴서 한 칸에 쌓지 않는다 — 한 상자에서 갈린 형제(같은
    부모의 자식, 같은 자식으로 모이는 부모)가 같은 파도에 남아야 갈래가
    사슬로 안 보인다(2026-09-01, 「폐쇄형/개방형 전략」 사고 참고).
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


def _mm_levels_sink(order, edges):
    """끝에서 재서 파도를 나눈다 — 받는 쪽에 붙여 세운다.

    뿌리에서 세면(`_mm_topo_levels`) 들어오는 이음이 없는 상자가 전부 첫 파도에 몰린다.
    그런데 그중에는 끝까지 두 칸인 것과 한 칸인 것이 섞여 있다 — 한 칸짜리가 첫 파도에
    서면 그 선이 사이 열을 가로질러 남의 상자를 뚫는다(2026-09-01, 할라페뇨 밸류체인에서
    네트워크·메모리·CPU 셋이 파운드리를 건너뛰어 조립으로 갔다).

    끝까지의 가장 긴 거리를 재고 그만큼 뒤에서 당겨 세우면, 한 칸짜리는 받는 상자
    바로 앞 파도에 선다. 층 나누기의 표준 방식이다.
    """
    nxt = {}
    for a, b, _ in edges:
        nxt.setdefault(a, []).append(b)
    memo, busy = {}, set()

    def depth(n):
        """n 에서 끝까지의 가장 긴 걸음 수."""
        if n in memo:
            return memo[n]
        if n in busy:                    # 고리는 여기서 끊는다
            return 0
        busy.add(n)
        d = 0
        for m in nxt.get(n, ()):
            if m in idx:
                d = max(d, depth(m) + 1)
        busy.discard(n)
        memo[n] = d
        return d

    idx = {n: i for i, n in enumerate(order)}
    far = max((depth(n) for n in order), default=0)
    rows = {}
    for n in order:
        rows.setdefault(far - depth(n), []).append(n)
    return [rows[k] for k in sorted(rows)]


def _mm_weak_groups(order, edges):
    """이음으로 이어진 상자만 한 덩이로 묶는다(약한 연결 성분).

    받은 도식 하나에 서로 안 이어진 사슬 둘이 들어오는 일이 있다 — 한 판에
    같이 앉히면 위상 정렬이 둘을 섞어 없던 인과가 생긴다. 이어진 상자끼리만
    묶어 따로따로 판을 짠다.
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
    return sorted(groups.values(), key=lambda gr: idx[gr[0]])


def _mm_build(names, rows, edges, width, wrap_label=False):
    """자리(rows, 파도마다 id 리스트)가 정해진 상자들을 판 하나로 굽는다. 실패하면 None."""
    # 파도 사이 틈 — 화살촉이 8px 라 10 을 주면 막대가 2px 만 남아 촉만 보인다
    # (2026-09-01). 20 이면 막대 12px + 촉 8px 로 이음이 선으로 읽힌다
    p = fig_layout.Plate(width=width, subout=False, top=2.0, gap_y=34.0,
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


def _mm_back_edges(order, edges):
    """DFS 로 고리를 만드는 이음(뒤로 가는 이음)의 자리(edges 안 인덱스)를 찾는다.

    agentic 루프처럼 결과가 앞 상자로 되돌아가는 그림은 진짜 고리(사이클)다 —
    Kahn 위상 정렬은 고리를 못 풀어 남은 상자를 전부 한 파도에 몰아넣는다
    (2026-09-01, 그록봇 기술 뷰 「에이전틱 CPU 풀」이 여덟 상자 중 여섯을 한
    행에 몰아넣어 판 폭을 넘겼다). 표준 DFS 뒤 이음 찾기로 고리를 여는 이음만
    골라 **파도 계산에서만** 뺀다 — 그림에는 그대로 그린다(되돌아가는 화살표
    자체가 뜻이다).
    """
    adj = {}
    for i, (a, b, _) in enumerate(edges):
        adj.setdefault(a, []).append((b, i))
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in order}
    back = set()

    def dfs(u):
        color[u] = GRAY
        for v, ei in adj.get(u, ()):
            if color.get(v, WHITE) == WHITE:
                dfs(v)
            elif color.get(v) == GRAY:
                back.add(ei)          # v 가 지금 스택에 있다 — u->v 는 뒤로 가는 이음
        color[u] = BLACK

    for n in order:
        if color.get(n) == WHITE:
            dfs(n)
    return back


def _mm_transpose(waves):
    """파도를 행이 아니라 **열**로 세운다 — `flowchart LR` 을 위한 자리 잡기.

    파도 하나가 열 하나가 되고, 그 안 형제는 위아래로 쌓인다. 행 수는 가장 긴
    파도만큼이고 빈 자리는 None 이다(`Plate.row` 가 빈 칸으로 받는다).
    """
    depth = max(len(w) for w in waves)
    return [[w[r] if r < len(w) else None for w in waves] for r in range(depth)]


def _mm_component_plate(names, order, edges, width, horizontal=False):
    """한 덩이(서로 이어진 상자들)를 판 하나로. 이름이 길어 폭을 넘기면
    칸 수를 줄이는 대신 상자 안 줄 수를 늘린다(wrap_label). 그래도 안 되면
    판을 포기한다."""
    back = _mm_back_edges(order, edges)
    fwd = [e for i, e in enumerate(edges) if i not in back]
    rows = _mm_levels_sink(order, fwd or edges)
    if not rows:
        return None
    # 한 파도에 형제가 넷을 넘으면 폭 520 에 못 앉는다. 예전에는 판을 통째로 포기하고
    # 프롬프트로 「형제는 셋까지」를 시켰는데, 그건 우리 판이 좁아서 생긴 사정이지
    # 그림의 규칙이 아니다 — 받는 쪽에 시킬 일이 아니라 여기서 감당한다.
    # 넘치는 파도는 셋씩 끊어 잇달아 놓는다(2026-09-01)
    wide = []
    for lv in rows:
        if len(lv) <= 3:
            wide.append(lv)
            continue
        # 고르게 나눈다. 셋씩 끊으면 넷이 3+1 이 되어 마지막 하나가 혼자 한 줄을
        # 차지하고, 칸을 판 끝까지 늘리는 규칙 때문에 그 상자가 폭 전체를 막는다 —
        # 위에서 아래로 가는 선이 그 줄을 지날 데가 없어진다(2026-09-01)
        n = (len(lv) + 2) // 3
        size = (len(lv) + n - 1) // n
        for k in range(0, len(lv), size):
            wide.append(lv[k:k + size])
    rows = wide
    # 가로로 그리라고 적혀 왔으면 파도를 열로 세워 **먼저 시켜 본다**. 파도 수로
    # 미리 자르지 않는다 — 「넷이면 폭을 못 댄다」를 재 보지 않고 규칙으로 박았더니
    # LR 로 온 판 넷 중 둘이 세로로 떨어졌다(2026-09-01). 짧은 이름이면 넷도 앉는다.
    # 굽기가 실제로 실패할 때만 세로로 물러난다
    plans = []
    if horizontal:
        plans.append(_mm_transpose(rows))
    plans.append(rows)
    for plan in plans:
        for wrap_label in (False, True):
            # 파도(행) 자리는 앞으로 가는 이음만으로 잡되, 그리는 이음은 전부
            # (되돌아가는 것 포함) 넘긴다 — 자리와 그림은 다른 일이다
            svg = _mm_build(names, plan, edges, width, wrap_label=wrap_label)
            if svg:
                return svg
    return None


def _mm_to_plate(g, width=520.0):
    """그래프 하나를 fig_layout.Plate SVG 로. 못 그리면 None. 서로 안 이어진
    덩이는 `_mm_weak_groups` 로 갈라 따로 판을 짜고 이어 붙인다 — 하나라도
    못 앉히면 전부 실패로 되돌린다."""
    groups = _mm_weak_groups(g.order, g.edges)
    if not groups:
        return None
    svgs = []
    for grp in groups:
        gset = set(grp)
        gedges = [e for e in g.edges if e[0] in gset and e[1] in gset]
        svg = _mm_component_plate(g.names, grp, gedges, width,
                                  horizontal=g.direction in ('LR', 'RL'))
        if not svg:
            return None
        # 이 덩이(약한 연결 성분)의 노드가 모두 같은 subgraph 제목을 달고
        # 있으면 그 제목을 판 위 캡션으로 올린다 — 「과거: 로컬 구축형」처럼
        # 두 덩이를 가르는 이름을 잃지 않는다
        titles = set(g.title_of.get(nid) for nid in grp)
        titles.discard(None)
        if len(titles) == 1:
            svg = '<p class="fig-title">%s</p>%s' % (_inline(next(iter(titles))), svg)
        svgs.append(svg)
    return ''.join(svgs)


def _mm_prose(g):
    """판을 못 지었을 때의 마지막 수단 — 노드·이음을 글로 푼다. 낱말을 하나도
    안 지운다(이음마다 「A → B(라벨)」, 이음 없는 노드는 이름 그대로)."""
    items, shown = [], set()
    for a, b, label in g.edges:
        na, nb = g.names.get(a, a), g.names.get(b, b)
        shown.add(a)
        shown.add(b)
        items.append('%s → %s%s' % (na, nb, ('(%s)' % label) if label else ''))
    for nid in g.order:
        if nid not in shown:
            items.append(g.names.get(nid, nid))
    if len(items) < 2:
        return None
    return '<ul>%s</ul>' % ''.join('<li>%s</li>' % _inline(x) for x in items)


def mermaid_verify(block):
    """`_mm_parse` 가 읽은 값이 문법과 무관한 단순 셈(화살표 개수 · 선언된
    id 집합)과 맞아떨어지는지 — 파서 자체가 틀렸으면 이 셈도 같이 틀릴 수
    있어 완전한 증명은 아니지만, 둘이 갈리면 파서가 뭔가를 잃었다는 신호는
    된다."""
    g = _mm_parse(block)
    ids = set()
    arrows = 0
    for ln in block.split(chr(10)):
        if not ln.strip() or _MM_SKIP_LINE.match(ln):
            continue
        n = len(_MM_ARROW_COUNT.findall(ln))
        # `A & B & C --> D` 는 한 줄에 화살표가 하나뿐이라도 실제로는 이음이
        # 셋이다 — 시작점 수만큼 센다. 안 그러면 우리 파서가 펴서 읽은 값
        # (`_mm_fanout`)과 이 단순 셈이 갈려, 제대로 읽었는데도 「어긋난다」로
        # 잘못 걸린다
        am = _MM_ARROW_COUNT.search(ln)
        if n and am and '&' in ln[:am.start()]:
            n *= len([s for s in ln[:am.start()].split('&') if s.strip()])
        arrows += n
        for m in _MM_ANY_DECL.finditer(ln):
            ids.add(m.group(1))
        for tok in re.split(r'-->|---|\|[^|]*\|', ln):
            tm = re.match(r'^\s*(%s)\b' % _MM_ID, tok)
            if tm:
                ids.add(tm.group(1))
    return {
        'parsed_nodes': len(g.order), 'naive_nodes': len(ids),
        'parsed_edges': len(g.edges), 'naive_edges': arrows,
        'nodes_match': len(g.order) == len(ids),
        'edges_match': len(g.edges) == arrows,
    }


def _mm_content_only(block):
    """제어 줄(flowchart·subgraph·end·style 등)을 뺀 나머지 — mermaid 문법
    낱말 자체는 화면에 실을 뜻이 없으니 `_kept` 검사에서 요구하지 않는다.

    노드 id 도 표기다. `host_cpu[호스트 CPU]` 에서 화면에 서는 것은 대괄호 안이고
    `host_cpu` 는 어디에도 안 나온다 — 그걸 낱말로 세면 판이 낱말을 흘린 것으로 잡혀
    통째로 버려진다(2026-09-01, 받은 답이 id 를 길게 쓰면서 판 셋이 그렇게 죽었다).
    이름이 붙은 노드는 id 를 떼고 이름만 남긴다. 이름 없이 맨몸으로 선 id 는 그
    글자가 그대로 화면에 서므로 남긴다.
    """
    # 이름이 붙은 id 를 먼저 모은다. 그 id 는 뒤 줄에 맨몸으로 다시 나와도 표기다 —
    # `host_cpu[호스트 CPU]` 로 한 번 이름이 붙으면 그다음 `host_cpu` 도 화면에는
    # 「호스트 CPU」로 선다
    labeled = set(m.group(1) for m in _MM_ANY_DECL.finditer(block))
    bare = [re.compile(r'(?<![A-Za-z0-9_가-힣])%s(?![A-Za-z0-9_가-힣])' % re.escape(i))
            for i in labeled]
    lines = []
    for ln in block.split(chr(10)):
        if _MM_SKIP_LINE.match(ln):
            continue
        ln = _MM_ANY_DECL.sub(lambda m: m.group(0)[len(m.group(1)):], ln)
        for rx in bare:
            ln = rx.sub(' ', ln)
        lines.append(ln)
    return chr(10).join(lines)


_SVG_RECT = re.compile(r'<rect[^>]*x="([-\d.]+)"[^>]*y="([-\d.]+)"'
                       r'[^>]*width="([-\d.]+)"[^>]*height="([-\d.]+)"')
_SVG_LINE = re.compile(r'<path d="([^"]+)" class="fl')


def _mm_crossings(svg):
    """구운 판에서 선이 남의 상자 안을 지나는 자리 수.

    선 끝이 상자에 붙었나는 `check_fig` F5 가 보는데, 선이 **지나가는** 자리는 아무도
    안 봤다 — 2026-09-01 에 화면에서 그걸 짚어 받고서야 알았다. 토막 가운데가 상자
    안이면 뚫은 것으로 센다(끝점은 원래 변에 닿으므로 가운데로 본다).
    """
    boxes = []
    for m in _SVG_RECT.finditer(svg or ''):
        x, y, w, h = [float(v) for v in m.groups()]
        boxes.append((x, y, x + w, y + h))
    n = 0
    for m in _SVG_LINE.finditer(svg or ''):
        pts = [float(v) for v in re.findall(r'[-\d.]+', m.group(1))]
        for k in range(0, len(pts) - 3, 2):
            mx = (pts[k] + pts[k + 2]) / 2.0
            my = (pts[k + 1] + pts[k + 3]) / 2.0
            for (bx0, by0, bx1, by1) in boxes:
                if bx0 + 1 < mx < bx1 - 1 and by0 + 1 < my < by1 - 1:
                    n += 1
                    break
    return n


def _mermaid_block_html(block):
    """mermaid 도식 한 덩어리를 판(또는 글)으로. 노드가 둘 미만이면 None."""
    g = _mm_parse(block)
    if len(g.order) < 2:
        return None
    content = _mm_content_only(block)
    svg = _mm_to_plate(g, width=520.0)
    if svg and not _kept(content, svg):
        svg = None                  # 낱말을 흘린 판은 안 쓴다
    if not svg:
        prose = _mm_prose(g)
        if prose and _kept(content, prose):
            return prose
        return None
    small = _mm_to_plate(g, width=340.0)
    # 좁은 판은 칸이 좁아 선이 남의 상자를 지나는 일이 있다 — 넓은 판은 멀쩡한데
    # 모바일에서만 겹친다(2026-09-01, 할라페뇨 경영 판2). 그런 좁은 판은 안 쓴다.
    # 넓은 판은 width:100% 라 좁은 화면에서도 줄어들 뿐 겹치지는 않는다
    if small and small != svg and _kept(content, small) and not _mm_crossings(small):
        return ('<div class="fig-pc">%s</div><div class="fig-mo">%s</div>'
                % (svg, small))
    return svg


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
    # 10.5px 아래로는 안 내린다. 9px 로 두었더니 화면에서 못 읽었다 — 폭에 맞추려고
    # 글자를 줄이는 일과 글자를 지우는 일이 그 크기에서 갈리지 않는다(2026-08-31 실험).
    # 넓은 화면 기본이 11.52px 이라 바닥을 그보다 높이 잡으면 줄이는 장치가 통째로
    # 무력해진다. 다 안 들어가는 줄은 `.fv-pre` 의 overflow-x:auto 로 마저 스크롤한다
    fs_wide, fs_narrow = max(fs_wide, 10.5), max(fs_narrow, 10.5)
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


# 판도 표도 못 되는 도식의 마지막 수단(글로 풀기)이 걷어 내는 순수 장식 문자.
# 실제 낱말이 하나도 안 섞인 토큰(공백으로 둘러싸인)만 지운다 — 「24~36개월」의
# '~'는 숫자에 붙어 있어 안 걸린다(토큰 경계 조건)
_DECOR_TOK = re.compile(
    r'(?<!\S)[│║|\-─═<>\^v\+~▲▼◀▶→←↑↓┌┐└┘├┤┬┴┼•·*]+(?!\S)')


def _prose_list(block):
    """표도 판도 못 되는 도식(축·눈금 있는 산점도, 문단 딸린 나무 가지 등)을
    불릿 글로 푼다. 새 구조(이음·칸·차례)를 짓지 않는다 — 순수 장식 줄·토큰만
    걷고, 남는 줄을 받은 순서 그대로 한 줄에 한 항목씩 옮길 뿐이다.
    """
    items = []
    for ln in block.split(chr(10)):
        t = ln.strip()
        if not t or t == 'text':
            continue
        t = _DECOR_TOK.sub(' ', t)
        t = re.sub(r'\s{2,}', ' — ', t).strip(' —')
        # 「[제목]」처럼 조각 전체가 대괄호 한 겹으로 싸였으면 벗긴다 — 불릿
        # 글머리에 마크다운 대괄호가 그대로 남으면 제목이 아니라 코드처럼 읽힌다
        t = ' — '.join(seg[1:-1].strip() if re.match(r'^\[[^\[\]]+\]$', seg) else seg
                       for seg in t.split(' — '))
        if len(re.findall(r'[가-힣A-Za-z0-9]', t)) >= 2:
            items.append(t)
    if len(items) < 2:
        return None
    return '<ul>%s</ul>' % ''.join('<li>%s</li>' % _inline(x) for x in items)


_GAP2 = re.compile(r'( {2,})')
# 표 줄 사이에 낀 순수 장식 줄 — 칸을 가르는 대시 한 줄(구분선)이거나, 그림
# 문자(세로줄·화살표)만 있고 실제 글자는 없는 줄(흐름도의 「|」·「v」 같은 이음
# 표시). 표에서는 낱말이 없으니 칸으로 못 자르고, 억지로 넣으면 화살표 조각이
# 옆 칸에 섞여 든다(2026-08-27 「상용 실리콘 업체 대 모델 랩」이 그렇게 깨졌다)
_SEP_LINE = re.compile(r'^[─═\-│║|<>\^v\+=~▲▼◀▶→←↑↓┌┐└┘├┤┬┴┼\s]+$')


def _segs(ln):
    """줄을 큰 공백(두 칸 이상)으로 가른 조각들. [(글, 시작 칸)].

    표 머리를 대괄호가 아니라 큰 공백만으로 가르는 판이 있다(「가진 정보
    쓸 수 있는 수」). `_cells` 로 칸을 재 문자 인덱스를 표시 칸으로 옮긴다.
    """
    cells = _cells(ln)
    idx2col = [a for ch, a, b in cells]
    out, pos = [], 0
    for piece in _GAP2.split(ln):
        if piece and not piece.isspace():
            s = pos + (len(piece) - len(piece.lstrip()))
            col = idx2col[s] if s < len(idx2col) else (idx2col[-1] + 1 if idx2col else 0)
            out.append((piece.strip(), col))
        pos += len(piece)
    return out


def _gaps(cells):
    """그 줄에서 공백이 두 칸 이상 이어지는 자리(시작 칸) 목록."""
    out, run = [], None
    for ch, a, _b in cells:
        if ch == ' ':
            run = a if run is None else run
        else:
            if run is not None and a - run >= 2:
                out.append(run)
            run = None
    return out


def _header_cols(ln):
    """이 줄이 표 머리인가. (이름 목록, 그 이름이 시작하는 칸 목록) 또는 None.

    대괄호가 **정확히 둘**이면 그 자리로(옛 길 — 셋 이상은 상자 여럿이 한 줄에
    선 그래프 줄이지 표 머리가 아니다. 「[가속기] [가속기] [가속기] [가속기]」를
    표로 읽으면 상자 그림이 깨진다). 대괄호가 없어도 큰 공백으로 2~3 조각으로
    갈리고 각 조각이 짧으면(문장이 아니라 이름이면), 그리고 그 줄에 그림
    문자(│┌┐└┘├┤┬┴┼▲▼◀▶→←↑↓)가 없으면 머리로 본다 — 있으면 표가 아니라
    상자·화살표 그림이다.
    """
    boxes = _BOX.findall(ln)
    if len(boxes) == 2:
        cells = _cells(ln)
        cuts = [cells[m.start()][1] for m in _BOX.finditer(ln) if m.start() < len(cells)]
        return [t.strip() for t in boxes], cuts
    if len(boxes) > 2 or (set(ln) & (_DRAW | set('▲▼|^*+'))):
        return None
    segs = _segs(ln)
    if 2 <= len(segs) <= 3 and all(
            len(re.findall(r'[가-힣A-Za-z0-9]', s[0])) <= 26 for s in segs):
        return [s[0] for s in segs], [s[1] for s in segs]
    return None


def _row_cut(ln, bounds):
    """줄을 bounds(오름차순 칸 목록) 자리 가까이서 len(bounds)+1 칸으로 자른다.

    칸 위치로 곧장 자르면 값이 머리보다 넓을 때 낱말이 두 칸에 걸쳐 갈린다
    (「오직 자사 내부 모델 인프라로만 / 활용   엔터프라이즈…」). 값의 경계는
    값이 만든 공백에 있다 — 두 칸 공백 중 그 자리에 가장 가까운 곳에서 자르고,
    없으면 한 칸 공백, 그마저 없으면 최후 수단으로 칸 위치 그대로 쓴다.
    자리를 못 찾아 뒤로 갈수록 앞으로 가면(겹치면) None(이 줄은 못 갈랐다).
    """
    c = _cells(ln)
    if not c:
        return None
    line_max = c[-1][2]
    # 줄 맨 앞 들여쓰기(2 칸 이상)도 `_gaps` 에는 틈으로 잡힌다 — 진짜 칸
    # 경계가 아니니 뺀다
    gs = [g for g in _gaps(c) if g > 1]
    singles = [a for ch, a, _b in c if ch == ' ']
    TOL = 6   # 이 칸 안에 공백 후보가 없으면 안 믿는다 — 엉뚱하게 가까운
              # 딴 낱말 사이 틈을 이 자리의 경계로 삼지 않는다
    picked, prev = [], None
    if len(gs) == len(bounds):
        # 이 줄에 진짜 이음매(두 칸 공백)가 필요한 수만큼 정확히 있다 — 머리
        # 칸 자리에 가장 가까운 것을 고르지 않고 왼→오 차례 그대로 쓴다.
        # 「가장 가까운 자리」로 고르면 이름 길이가 짧은 줄에서 전체가 왼쪽으로
        # 밀려 뒤 칸의 틈이 앞 칸 경계보다 머리 칸에 더 가까워지는 일이 있다
        # (2026-08-27 「문제·선택·근거」 표의 「어떻게 보고하나」 행이 그렇게
        # 둘째 틈을 첫 경계로 잘못 골라 통째로 깨졌다)
        picked = list(gs)
    else:
        for i, target in enumerate(bounds):
            # 이 줄의 글이 애초에 그 칸 근처까지도 안 뻗는다 — 남는 자리를
            # 억지로 채우면 엉뚱하게 가까운 공백(딴 낱말 사이 틈)을 경계로
            # 집어 온다. 줄 끝 바로 뒤에 경계를 둬 이 칸엔 아무것도 안 떨어지게
            # 한다(2026-08-27 「(토큰 사용 통계 없음)」이 엉뚱한 칸으로 갔다)
            if target >= line_max - TOL:
                b = line_max + 1
            else:
                lo = 1 if prev is None else prev + 1
                cand = [g for g in gs if g >= lo]
                b = min(cand, key=lambda g: abs(g - target)) if cand else None
                if b is not None and abs(b - target) > TOL:
                    b = None
                if b is None:
                    far = [a for a in singles if a >= lo and a > 1]
                    b1 = min(far, key=lambda g: abs(g - target)) if far else None
                    b = b1 if (b1 is not None and abs(b1 - target) <= TOL) else target
            if prev is not None and b <= prev:
                return None
            picked.append(b)
            prev = b
    out = [''] * (len(bounds) + 1)
    for ch, a, _b in c:
        idx = 0
        for b in picked:
            if a >= b:
                idx += 1
            else:
                break
        out[idx] += ch
    return [x.strip() for x in out]


def _gap_table(block):
    """대괄호 표든 대괄호 없는 표든 — 큰 공백으로 칸이 갈리는 표를 <table> 로.

    「[ 폐쇄형 ] ◀━▶ [ 개방형 ]」처럼 대괄호 머리도, 「가진 정보    쓸 수 있는
    수」처럼 대괄호 없이 큰 공백으로만 갈린 머리도 받는다. 머리 이름 수와 몸
    첫 줄의 조각 수를 견줘 **줄 이름 칸이 따로 있는지**를 정한다 — 있으면(줄
    이름 + 값들) 머리 칸 그대로 자르고, 없으면(칸마다 이름이 다 있음) 첫 칸을
    빼고 자른다. 한 항목이 줄을 여러 줄 쓰면(다음 줄이 같은 항목의 이어지는
    값이면, 빈 줄로 갈린 한 덩이) 그 조각들을 합친다. 표가 아니면 None.
    """
    lines = [ln.rstrip() for ln in block.split(chr(10)) if ln.strip() != 'text']
    if len(lines) < 4:
        return None
    # 아스키 테두리 상자(+---+ 틀)가 있으면 표가 아니라 상자 그림이다 —
    # `_unframe`+그래프 길이 이미 그 꼴을 다룬다. 여기서 「| 글 |」 줄을 표
    # 칸으로 읽으면 테두리 파이프가 값에 섞여 든다(2026-08-24 「에이전트 AI
    # 패러다임」 조직도가 그렇게 깨졌다) — 그 길에 맡기고 물러선다
    if any(re.match(r'^\s*\+[-+]+\+\s*$', ln) for ln in lines):
        return None
    for top, head in enumerate(lines):
        if not head.strip() or _SEP_LINE.match(head):
            continue
        hc = _header_cols(head)
        if not hc:
            continue
        names, cuts = hc
        body = lines[top + 1:]
        first_data = next((ln for ln in body if ln.strip() and not _SEP_LINE.match(ln)), '')
        first_n = len(_segs(first_data))
        if first_n == len(names) + 1 and cuts[0] >= 2:
            bounds, ncol, has_label = cuts, len(names) + 1, True
        elif first_n >= len(names) and len(cuts) >= 2:
            bounds, ncol, has_label = cuts[1:], len(names), False
        else:
            continue

        def merge(grp):
            merged = [''] * ncol
            hit = False
            for gln in grp:
                cs = _row_cut(gln, bounds)
                if cs is None:
                    continue
                hit = True
                for i, v in enumerate(cs):
                    if v:
                        merged[i] = (merged[i] + ' ' + v).strip() if merged[i] else v
            need = ncol - 1 if has_label else ncol
            if hit and sum(bool(x) for x in merged) >= need and merged[-1]:
                return merged
            return None

        def flush_group(grp):
            """모인 줄들을 행 목록으로. 촘촘한 표(줄마다 한 행, 사이에 빈 줄이
            없는 「타겟 고객 …」류)와 값이 줄을 걸쳐 이어지는 표(「Nvidia …」
            류)를 가른다.

            그룹 첫 줄보다 훨씬 더 들여쓴 줄이 섞여 있으면(「OpenAI …」 다음에
            훨씬 안으로 들어간 「워크로드 분포 …」가 오는 꼴) 그 줄은 새 행이
            아니라 이어지는 값이다 — 줄마다 따로 갈라도 우연히 칸 수가 맞아
            떨어져 각자 완성된 행처럼 보일 수 있다(2026-08-27 「가진 정보」
            표에서 「워크로드 분포」가 그렇게 독립된 행으로 떨어졌다). 그런
            줄이 하나도 없을 때만 줄마다 따로 갈라 본다 — 다들 온전하면 그
            수만큼 행으로 내고, 아니면 그룹 전체를 합쳐 한 행으로 낸다.
            """
            if len(grp) > 1:
                base = len(grp[0]) - len(grp[0].lstrip())
                if any(len(g) - len(g.lstrip()) > base + 2 for g in grp[1:]):
                    m = merge(grp)
                    return [m] if m else []
            per_line = [merge([g]) for g in grp]
            if per_line and all(per_line):
                return per_line
            m = merge(grp)
            return [m] if m else []

        rows, tail, group, stop = [], [], [], False
        for ln in body:
            if stop:
                if ln.strip():
                    tail.append(ln.strip())
                continue
            # 세로 이음 문자(│▲▼◀▶ 등, 흐름도의 「다음 단계로」 표시)가 낀 줄은
            # 글이 섞여 있어도(「TCO」·「고객이므로」) 표 칸이 아니다 — 두 갈래가
            # 나란히 선 흐름도지 표가 아니다(`_split_cols`/그래프 길이 맡을 자리).
            # 여기서 억지로 칸에 넣으면 이음 문자가 값에 섞여 든다(2026-08-27
            # 「판매사 모델 대 수직 통합 모델」이 그렇게 깨졌다) — 이 줄은 버리고
            # 낱말 안전망(`_kept`)이 이 표 자체를 통째로 되돌리게 둔다
            # ◀▶ 는 여기서 뺀다 — 「▶ 시사점: …」처럼 결론 문단을 여는 표시로
            # 이미 쓰는 문자다(꼬리 문단 판정, 아래에서 본다). 여기 넣으면 그
            # 문단이 꼬리로 못 가고 통째로 사라진다(2026-08-27 「예상되는 다음
            # 수」가 그렇게 없어졌다)
            if set(ln) & set('│║┌┐└┘├┤┬┴┼▲▼'):
                if group:
                    rs = flush_group(group)
                    if rs:
                        rows.extend(rs)
                    elif rows:
                        stop = True
                    group = []
                continue
            if not ln.strip() or _SEP_LINE.match(ln):
                # 빈 줄과 장식 줄(구분선)은 똑같이 「이 행은 여기까지」다 —
                # 장식 줄만 건너뛰고 다음 글줄을 같은 행에 이어 붙이면 흐름도의
                # 다음 단계가 이전 단계와 한 칸에 뭉친다
                if group:
                    rs = flush_group(group)
                    if rs:
                        rows.extend(rs)
                    elif rows:
                        stop = True
                    group = []
                continue
            if rows and (_BOX.search(ln) or ln.strip()[:1] in ('▶', '*', '·')):
                stop = True
                tail.append(ln.strip())
                continue
            # 새 줄(=이 이음의 첫 줄)에 큰 공백 자리가 하나도 없으면 표 칸이
            # 아니라 그냥 딸린 산문이다 — 억지로 자르면 (「같은 팀 구성인데
            # 도구만 없던 경우」처럼) 한 문장이 두 칸에 걸쳐 갈리거나, 관계
            # 없는 문단이 표의 한 행처럼 서게 된다(2026-08-27)
            if not group and rows and not _gaps(_cells(ln)):
                stop = True
                tail.append(ln.strip())
                continue
            group.append(ln)
        if not stop and group:
            rows.extend(flush_group(group))
        if len(rows) < 2:
            continue
        title = [re.sub(r'[┌┐└┘│─]', ' ', ln).strip() for ln in lines[:top]]
        title = [t for t in title if len(re.findall(r'[가-힣A-Za-z0-9]', t)) >= 3]
        head_cells = ([''] + names) if has_label else names
        h = '<tr>' + ''.join(
            '<th scope="col">%s</th>' % _inline(n.strip('[]').strip()) if n else '<th></th>'
            for n in head_cells) + '</tr>'
        b = ''.join('<tr>' + ''.join(
            ('<th scope="row">%s</th>' % _inline(v)) if (has_label and i == 0)
            else ('<td>%s</td>' % _inline(v)) for i, v in enumerate(r)) + '</tr>'
            for r in rows)
        cap = ''.join('<p class="fig-title">%s</p>' % _inline(t.strip('[]').strip())
                      for t in title)
        note = ('<p>%s</p>' % _inline(' '.join(tail))) if tail else ''
        return '%s<table>%s<tbody>%s</tbody></table>%s' % (
            cap, '<thead>%s</thead>' % h, b, note)
    return None


def _block_html(block):
    """도식 덩어리 하나를 판·글·아스키 중 하나로.

    들여쓴 목록은 그냥 글이다 — 판으로 구우면 딱지가 주인공이 되고(「한계」·「장점」),
    아스키로 두면 읽기 어려운 고정폭 덩어리가 된다. 목록 표시를 불릿으로 바꿔 글로 낸다.
    """
    # 이모지는 여기 하나뿐인 문턱에서 지운다 — 판·아스키 어느 길로 가든,
    # 이 함수를 지난 뒤로는 이모지가 없다고 믿을 수 있다
    block = _denorm_emoji(block)
    # mermaid flowchart 표기는 문법이 고정돼 있어 정규식 파서(위 `_mm_*`)가
    # 먼저 읽는다. 거기서 판도 글도 못 지었을 때만(정상적으로는 안 일어난다)
    # 옛 아스키 격자 길로 내려간다 — mermaid 의 `A[이름]` 노드 선언도 옛
    # `_BOX` 규칙(대괄호)과 형태가 같아 안전망으로 통한다
    if _is_mermaid_block(block):
        mm = _mermaid_block_html(block)
        if mm:
            return mm
    # 두 갈래를 견주는 표는 판이 아니라 표다 — 좌우로 갈라 나란히 보여야 뜻이 산다
    tbl = _gap_table(block)
    if tbl and _kept(block, tbl):
        return tbl
    # 상자 그래프를 목록·대조 판정보다 먼저 시도한다. 줄머리가 ├─·└─ 라도
    # (`_is_list` 가 목록으로 보는 표시) 실은 상자 그림인 일이 잦다 —
    # 2026-08-31 「기능 목록」이 그래프로는 다 읽히는데 목록 판정에 먼저 걸려
    # 「│」한 줄이 빈 불릿으로 섰다. 여기서 실패하면 아스키로 남을 덩어리다 —
    # 제목을 떼는 손질이 실패작을 판으로 되살리면 안 된다(아스키로 남은 넷은
    # 그대로 둔다는 규칙). 성공했을 때만 제목 줄을 상자에서 빼는 손질을 시도한다
    try:
        svg = boxes(block)
    except Exception:
        svg = None
    if svg and not _kept(block, svg):
        svg = None                  # 낱말을 흘린 판은 안 쓴다
    title = ''
    # 첫 줄이 「[다이어그램 N: …]」 같은 제목 한 줄이면 상자에서 떼고 판 위에
    # 세운다. 뗀 채로 못 구우면(폭 계산이 그 줄에 기대는 판도 있다) 방금 구운
    # 판을 그대로 쓴다 — 제목이 상자 하나로 남는 채가 안전한 대안이다. 첫
    # 시도(svg)가 아예 실패했을 때도 시도한다 — 제목 글이 길면 그 자체로
    # 판 폭을 넘겨 몸통까지 통째로 못 짜이는 일이 있다(2026-08-31 스케일업
    # 네트워크 그림이 그랬다) — 뗀 뒤에야 몸통이 폭 안에 들어온다
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
    # 판으로 못 읽었을 때만 목록으로 본다.
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
    # 표도 판도 못 되는 도식(축·눈금이 있는 산점도, 문단 딸린 나무 가지 등)의
    # 마지막 수단 — 불릿 글로 푼다. 새 이음·칸·차례를 짓지 않는다: 장식 문자만
    # 걷고 남은 줄을 받은 순서 그대로 한 줄에 한 항목씩 옮길 뿐이다
    prose = _prose_list(block)
    if prose and _kept(block, prose):
        return prose
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
            # 표 한 줄이 `|` 로 안 닫히면 그 칸이 다음 줄로 이어진다 — 받은 답이 목차
            # 칸에 절을 여러 줄로 넣을 때 그 꼴로 온다(2026-09-01, 제미나이 그록봇).
            # 이어지는 줄을 안 물면 표가 첫 줄에서 끊기고 나머지가 문단으로 새며
            # 남은 `|` 가 글자로 찍힌다. 이어붙일 줄은 좁게 본다 — 빈 줄이거나
            # `<br>` 이 들었거나 `|` 로 닫는 줄만. 그래야 뒤 문단을 안 삼킨다
            rows, open_row = [], False
            while i < len(lines):
                t = lines[i].strip()
                if t.startswith('|'):
                    rows.append([c.strip() for c in t.strip('|').split('|')])
                    open_row = not t.endswith('|')
                    i += 1
                    continue
                if open_row and (not t or '<br>' in t.lower() or t.endswith('|')):
                    if t:
                        rows[-1][-1] = (rows[-1][-1] + ' ' + t.rstrip('|').strip()).strip()
                        if t.endswith('|'):
                            open_row = False
                    i += 1
                    continue
                break
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
