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
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fig_layout  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAMES = os.path.join(ROOT, 'insights', 'frames')


# 아스키 도식을 상자로 굽는다. 그대로 두면 폭이 넘치고 글꼴이 바뀌면 선이 어긋난다 —
# 상자는 판 폭에 맞춰 서고 다크모드 색도 따라온다. 못 읽는 꼴이면 아스키 그대로 둔다.
_BOX = re.compile(r'\[([^\]\[]+)\]')
_ARROW = re.compile(r'(-->|→|▶|=>|=+>)')


_BAR = '│║'


def _bracketize(block):
    """선 그림(│ 이름 │)을 [ 이름 ] 꼴로 바꾼다.

    받는 쪽이 아스키 선으로 그려 오는 일이 잦은데, 상자 뽑는 자리는 대괄호만 안다.
    선 그림의 세로선 사이 글자가 곧 상자 이름이라 그대로 옮길 수 있다.
    """
    out = []
    for ln in block.split(chr(10)):
        if any(c in ln for c in _BAR) and not _BOX.search(ln):
            cells = [c.strip(' ─═-') for c in re.split('[%s]' % _BAR, ln)]
            cells = [c for c in cells if len(re.findall(r'[가-힣A-Za-z0-9]', c)) >= 2]
            if cells:
                ln = ' '.join('[%s]' % c for c in cells)
        out.append(ln)
    return chr(10).join(out)


def _rows_of(block):
    """줄마다 [ ... ] 를 뽑아 상자 줄로 만든다. 못 뽑으면 None."""
    rows, notes = [], []
    for ln in _bracketize(block).split(chr(10)):
        toks = _BOX.findall(ln)
        if toks:
            parts = _BOX.split(ln)
            cells = []
            for i, t in enumerate(toks):
                tail = parts[2 * i + 2] if 2 * i + 2 < len(parts) else ''
                tail = _ARROW.sub(' ', tail).strip(' |/\_·—-+')
                cells.append((t.strip(), tail[:34]))
            rows.append(cells)
        else:
            t = _ARROW.sub('', ln).strip(' |/\_+—-=<>←↑↓▲▼')
            if len(re.findall(r'[가-힣A-Za-z]', t)) >= 4:
                notes.append(t[:60])
    if not rows or sum(len(r) for r in rows) < 2:
        return None
    return rows, notes[:3]


def boxes(block):
    """도식 한 덩어리를 판 하나로. 못 읽으면 None."""
    got = _rows_of(block)
    if not got:
        return None
    rows, notes = got
    ncol = max(len(r) for r in rows)
    if ncol > 3:
        return None                 # 한 줄에 넷을 넘으면 판에 안 들어간다
    # 이름이 길면 판을 넘는다. 한 번 줄여 다시 굽고, 그래도 넘치면 아스키로 둔다 —
    # 상자 안에서 글자를 자르는 것보다 원본을 그대로 보이는 편이 낫다
    for cut in (None, 14):
        try:
            return _plate(rows, notes, ncol, cut)
        except AssertionError:
            continue
    return None


def _plate(rows, notes, ncol, cut=None):
    def fit(name, sub):
        if cut and len(name) > cut:
            sub = (name[cut:] + ' ' + sub).strip()[:30]
            name = name[:cut]
        return name, sub
    p = fig_layout.Plate()
    for r in rows:
        p.row(*([fit(n, sub) for n, sub in r] + [None] * (ncol - len(r))))
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
            try:
                svg = boxes(block)
            except Exception:
                svg = None
            out.append(svg if svg else '<pre class="fv-pre">%s</pre>'
                       % block.replace('&', '&amp;').replace('<', '&lt;'))
            i = j + 1
            continue
        j = _dia_span(lines, i)
        if j > i:
            block = chr(10).join(lines[i:j])
            try:
                svg = boxes(block)
            except Exception:
                svg = None
            out.append(svg if svg else '<pre class="fv-pre">%s</pre>'
                       % block.replace('&', '&amp;').replace('<', '&lt;'))
            i = j
            continue
        if ln.lstrip().startswith('|') and '|' in ln[1:]:
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            if len(rows) >= 3:
                out.append(_table(rows))
            continue
        m = re.match(r'\s*(#{1,6})\s+(.*)', ln)
        if m:
            out.append('<p class="fv-h">%s</p>' % _inline(m.group(2)))
            i += 1
            continue
        if re.match(r'\s*[\*\-]\s+', ln):
            items = []
            while i < len(lines) and re.match(r'\s*[\*\-]\s+', lines[i]):
                items.append(_inline(re.sub(r'\s*[\*\-]\s+', '', lines[i])))
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


CSS = '''
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
.uc-rep .fv-pre { margin:10px 0; padding:10px 12px; border:1px solid var(--line);
  border-radius:6px; background:var(--sunk); overflow-x:auto;
  font:400 .72rem/1.7 ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--ink-2); }
'''
