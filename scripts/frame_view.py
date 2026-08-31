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
# 딸린 라벨로 남는다
_ARROW = re.compile(r'(<[─—=-]+>|-->|→|▶|=>|=+>|[─—-]+>|<[─—-]+)')


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
    """좁은 화면용 판. 칸을 한 줄로 쌓는다.

    넓은 판은 폭 520 을 채우고 글자가 줄어 든다 — 휴대폰에서 상자 이름이 깨알이 된다.
    같은 내용을 한 칸으로 다시 구워 CSS 로 갈아 끼운다.
    """
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
        a, b = (_one_plate(_unframe(x)) for x in two)
        if a and b:
            return '<div class="fv-two">%s%s</div>' % (a, b)
        return None
    return _one_plate(block)


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
    if not _TITLE_ONLY.match(t):
        return '', block
    rest = chr(10).join(lines[:i] + lines[i + 1:])
    if not _BOX.search(rest):
        return '', block
    return t.strip('[]').strip(), rest


def _block_html(block):
    """도식 덩어리 하나를 판·글·아스키 중 하나로.

    들여쓴 목록은 그냥 글이다 — 판으로 구우면 딱지가 주인공이 되고(「한계」·「장점」),
    아스키로 두면 읽기 어려운 고정폭 덩어리가 된다. 목록 표시를 불릿으로 바꿔 글로 낸다.
    """
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
    return ('<pre class="fv-pre">%s</pre>'
            % block.replace('&', '&amp;').replace('<', '&lt;'))


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
