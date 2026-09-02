# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — 목록 한 장과 회차마다 글 한 장.

카드가 없다. 접힘도 타일도 없다. 회차 목록에서 줄을 눌러 글로 들어가고,
글 페이지에는 그 회차에 대해 선 판만 실린다.

  판   전략(⚖) 전략 컨설턴트 출신 애널리스트의 해설   ·   기술(🔧) 주제 + 순서·층위
       판은 주제가 서는 회차에만 생긴다. 둘 다 안 서면 그 줄은 링크가 안 걸린다.

  재료 content/understanding/Semi Doped/*.md   회차 메타와 한 줄
       insights/semidoped/<slug>-{strategy,tech}.md   받은 글 원본

  이 화면   py -3.13 scratchpad/gen_semidoped.py

규약은 이 파일 check_ui() 가 검사한다 — 접는 것 없음 · 판 없는 줄은 링크가
안 걸림 · 메타에 「언제 것」 · 타일 없음.
"""
import io
import os
import re
import sys
import html as _html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semidoped_figs  # noqa: E402
import check_fig  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'understanding', 'Semi Doped')
LANE_DIR = os.path.join(ROOT, 'insights', 'semidoped')
OUT = os.path.join(ROOT, '대시보드', 'Semi Doped 대시보드.html')
POST_DIR = os.path.join(ROOT, '대시보드', 'semidoped')
BLOB = 'https://github.com/johnn8n/semianalysis/blob/main/'

LANES = [('strategy', '⚖', '전략', '전략 컨설턴트 출신 애널리스트의 해설'),
         ('tech', '🔧', '기술', '주제 아래 순서와 층위')]

# 섹션 — 회차 frontmatter section 코드에 이름을 얹는다. 순서가 곧 화면 순서(2026-09-02).
# 글이 있는 회차가 하나도 없는 섹션은 안 보인다 — 「0편」 머리줄은 「글 없음」과 같다
SECTIONS = [('compute', '추론 칩'), ('link', '칩끼리 잇는 길'), ('power', '전력'), ('mem', '메모리'),
            ('fab', '공정·패키징·리소'), ('news', '시황·규제·자금')]

# 회차가 아니라 모음인 글. 목록에 줄은 서되 판을 세우지 않는다
NOT_EPISODE = {'daily-2026-04-08': '월별 회차 목록',
               'til-14': '역사 토막 모음'}


def esc(s):
    return _html.escape(s, quote=False)


def blob(p):
    return BLOB + p.replace(' ', '%20')


def front(md):
    """frontmatter 를 얕게 읽는다. 값에 콜론이 들어와도 첫 콜론에서만 가른다."""
    if not md.startswith('---'):
        return {}, md
    end = md.find('\n---', 3)
    if end < 0:
        return {}, md
    meta = {}
    for ln in md[3:end].splitlines():
        if ':' in ln:
            k, v = ln.split(':', 1)
            meta[k.strip()] = v.strip()
    return meta, md[end + 4:]


def one_line(body):
    """요약본의 「## 한 줄」 절 첫 문단. 없으면 gain 으로 갈음한다."""
    m = re.search(r'^## 한 줄\s*\n+(.+?)(?:\n\s*\n|\n## )', body, re.S | re.M)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


# ── 받은 글을 화면으로 ────────────────────────────────────────────────
# 표·문단·목록·굵게만 옮긴다. 도해는 받은 글에 없다 — 우리가 그려 semidoped_figs 에
# 두고, 절 제목 바로 아래(본문보다 앞)에 세운다. 그림을 보고 그 아래 글을 읽는 순서다.

# 전사 줄 번호 (L97)·(L45·L47)·(Vik이 전함, L177) 은 대조용 장치다. 원본 파일에는 남기고
# 화면에서만 걷는다 — 독자는 뉴스를 따라가는 사람이고 줄 번호는 그에게 소음이다(2026-09-02)
LREF_ALONE = re.compile(r'\s*\(\s*L\d+(?:\s*[·,\-–~]\s*L?\d+)*\s*\)')
LREF_TAIL = re.compile(r',\s*L\d+(?:\s*[·\-–~]\s*L?\d+)*(?=\))')
# 영어 인용은 옅게 — 앞뒤 한국어 문장이 뜻을 말하고 인용은 근거다
ENG_QUOTE = re.compile(r'"([A-Za-z][^"<>]{3,}?)"')


def strip_lrefs(s):
    return LREF_TAIL.sub('', LREF_ALONE.sub('', s))


# 진행자는 여는 문단에서 풀네임으로 한 번만 부르고 뒤에서는 진행자A·진행자V 다(2026-09-02).
# 원본 파일에는 이름이 남는다(전사 대조용). 풀네임(Austin Lyons·Vik Sekar)과 Vik's 는 건드리지 않는다.
PN_RE = re.compile(r'\[\[([^\]]+)\]\]')   # 화자 줄의 [[이름]]
HOST = {'Austin': '진행자A', 'Vik': '진행자V'}
HOST_RE = re.compile(r"\b(Austin|Vik)(?! Lyons| Sekar|['’]s)\s?(이|가|은|는|을|를|과|와)?(?=[^A-Za-z]|$)")
PART = {'이': '가', '은': '는', '을': '를', '과': '와'}
NAMES = []   # 화자 줄의 [[이름]] 중 진행자가 아닌 사람 — 본문에서 사람마다 다른 색. post_html 이 회차마다 채운다
HOSTS = []   # 진행자 이름 — 둘이 한 색(pn). 본문의 진행자A·진행자V 도 같은 색(2026-09-02)
PN_COLORS = 4


def pn_cls(n):
    return 'pn' if n in HOSTS or n not in NAMES else 'pn g%d' % (NAMES.index(n) % PN_COLORS)



def host_sub(s):
    return HOST_RE.sub(lambda m: HOST[m.group(1)] + (PART.get(m.group(2), m.group(2)) if m.group(2) else ''), s)


def _pn_sub(s, t, cls):
    # 앞뒤 경계는 영문·숫자·태그 꺾쇠만 본다 — 한글 조사가 바로 붙는 자리(진행자A가·Barber의)도 칠해야 한다
    return re.sub(r'(?<![A-Za-z0-9>])' + re.escape(t) + r'(?![A-Za-z0-9<])', '<span class="%s">%s</span>' % (cls, t), s)


def name_spans(s):
    """본문 이름 색 — 진행자 둘(과 풀네임)은 한 색, 게스트·발표자는 사람마다 다른 색.
    성만 쓴 자리(Barber·Yuen)도 칠한다(2026-09-02)."""
    for n in ['진행자A', '진행자V'] + HOSTS:
        s = _pn_sub(s, n, 'pn')
    for n in NAMES:
        toks = [n] + ([n.split()[-1]] if ' ' in n and len(n.split()[-1]) >= 3 else [])
        for t in toks:
            s = _pn_sub(s, t, pn_cls(n))
    return s


def inline(s):
    s = esc(host_sub(strip_lrefs(s)))
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = ENG_QUOTE.sub(r'<span class="q">"\1"</span>', s)
    return name_spans(s)


def fig_block(f):
    key, title, svg, cap = f
    return semidoped_figs.fig_html((key, title, svg, name_spans(host_sub(strip_lrefs(cap)))))


def table_html(rows):
    """칸마다 열 이름을 data-label 로 붙인다 — 640px 아래에서 표를 행 블록으로 세울 때
    CSS 가 그 이름을 칸 앞에 쓴다. 안 붙이면 모바일에서 5열 표가 한 글자씩 세로로 늘어진다."""
    head, body = rows[0], rows[2:]
    out = ['<table><thead><tr>']
    out += ['<th>%s</th>' % inline(c) for c in head]
    out.append('</tr></thead><tbody>')
    for r in body:
        out.append('<tr>' + ''.join(
            '<td data-label="%s">%s</td>' % (esc(head[k]) if k < len(head) else '', inline(c))
            for k, c in enumerate(r)) + '</tr>')
    out.append('</tbody></table>')
    return ''.join(out)


# ── 절 머리·방법 칩·트리 ─────────────────────────────────────────────
# 받은 글의 절 제목은 「N. (방법) 물음」이다. 방법은 제목·목차에서 걷고 부록 트리에만 칩으로
# 남긴다 — 쓰는 쪽 규율(한 노드 한 방법)이지 독자가 읽을 말이 아니다(2026-09-02).

METHODS = ['부분 나눔', '인과 사슬', '조건 갈림', '이해관계자', '밸류체인', '프로세스',
           '시간 흐름', '행위자', '층위', '대비', '수식']
METHOD_RE = re.compile(r'\((%s)(?::\s*([^)]*))?\)' % '|'.join(METHODS))
HEAD_RE = re.compile(r'^(\d+(?:-\d+)?)\.?\s+(?:\((%s)(?::[^)]*)?\)\s*)?(.*)$' % '|'.join(METHODS))
TREE_TOP = re.compile(r'^[├└]─\s*([A-Z])\.\s*(.+?)\s*[—-]\s*(.+?)\s*\(([^)]*)\)\s*$')


def chip(method, value=''):
    h = '<span class="chip">%s</span>' % esc(method)
    if value:
        h += '<span class="mv">%s</span>' % esc(value)
    return h


def parse_head(title):
    """「2-1 (부분 나눔) 잰 것」 → ('2-1', '부분 나눔', '잰 것'). 번호가 없으면 None."""
    m = HEAD_RE.match(title)
    if not m:
        return None
    return m.group(1), m.group(2) or '', m.group(3).strip()


def heading_html(tag, title, anchor=''):
    p = parse_head(title)
    idattr = ' id="%s"' % anchor if anchor else ''
    if not p:
        return '<%s%s>%s</%s>' % (tag, idattr, inline(title), tag)
    num, _method, q = p
    # 방법(부분 나눔·대비…)은 쓰는 쪽 규율이라 제목에서 걷는다 — 독자에게는 소음이다(2026-09-02)
    return '<%s%s><span class="num">%s</span> %s</%s>' % (tag, idattr, esc(num), inline(q), tag)


def tree_html(code):
    """트리 코드 블록을 들여쓴 줄로 낸다. 고정폭 30줄은 모바일에서 옆으로 밀어야 했다.
    선 글자(│├└─)는 걷고 깊이만 들여쓰기로 남긴다. 방법은 칩, [L줄] 은 옅게."""
    out = ['<div class="tree">']
    for ln in code:
        if not ln.strip() or set(ln.strip()) <= set('│ '):
            continue
        m = re.match(r'^((?:[│ ] {3})*)\s*([├└]─\s*)?(.*)$', ln)
        prefix, branch, text = m.groups()
        depth = len(prefix) // 4 + (1 if branch else 0)
        t = esc(text.strip())
        t = METHOD_RE.sub(lambda mm: chip(mm.group(1), mm.group(2) or ''), t)
        t = re.sub(r'\[(L[^\]]*)\]', r'<span class="lref">\1</span>', t)
        out.append('<div class="tn d%d">%s</div>' % (min(depth, 6), t))
    out.append('</div>')
    return ''.join(out)


def cells(ln):
    return [c.strip() for c in ln.strip().strip('|').split('|')]


def body_html(md, figs=()):
    """figs = [(절 제목 머리, 제목, svg, 캡션)]. 머리가 h2 제목의 앞부분과 같으면 그 제목
    바로 아래에 그림을 세운다. 안 걸린 그림은 오류다 — 절 번호가 바뀌면 그림이 소리 없이
    사라지는 일을 막는다."""
    lines = md.split('\n')
    out, i, para, items = [], 0, [], []
    pending = list(figs)

    def figs_under(title):
        hit = [f for f in pending if '|' not in f[0] and title.startswith(f[0])]
        for f in hit:
            pending.remove(f)
            out.append(fig_block(f))

    def figs_before_para(text):
        # 열쇠에 「|」가 있으면 뒤가 문단 머리다 — 그 문단 앞에 그림을 세운다. 절 하나에
        # 그림 여럿을 두되 절 머리에 쌓지 않으려는 것이다(2026-09-02)
        hit = [f for f in pending if '|' in f[0] and text.startswith(f[0].split('|', 1)[1])]
        for f in hit:
            pending.remove(f)
            out.append(fig_block(f))

    def flush():
        if para:
            text = ' '.join(para)
            figs_before_para(text)
            m = re.match(r'^\*\*so-what\*\*\s*[—-]?\s*(.*)$', text, re.S)
            if m:
                # 절의 값이 여기 있다. 본문과 같은 모양이면 지나친다
                out.append('<div class="sowhat"><span class="sw">so-what</span>%s</div>' % inline(m.group(1)))
            else:
                out.append('<p>%s</p>' % inline(text))
            del para[:]
        if items:
            out.append('<ul>%s</ul>' %
                       ''.join('<li>%s</li>' % inline(x) for x in items))
            del items[:]

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            # 펜스 블록 — 구조 절의 트리가 여기로 온다. 줄바꿈과 들여쓰기가 뜻이라
            # 문단으로 합치면 안 된다. 2026-09-02 에 이걸 안 잡아 트리가 인라인 코드
            # 한 문단으로 나갔다
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(lines[i])
                i += 1
            out.append(tree_html(code))
            i += 1
            continue
        if ln.strip().startswith('|') and i + 1 < len(lines) and \
                set(lines[i + 1].replace('|', '').strip()) <= set('-: '):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i]))
                i += 1
            out.append('<div class="tw">%s</div>' % table_html(rows))
            continue
        if ln.startswith('## '):
            flush()
            out.append('<h2>%s</h2>' % inline(ln[3:].strip()))
            figs_under(ln[3:].strip())
        elif ln.startswith('### '):
            flush()
            out.append(heading_html('h3', ln[4:].strip()))
            figs_under(ln[4:].strip())
        elif re.match(r'^\s*[-*] ', ln):
            if para:
                out.append('<p>%s</p>' % inline(' '.join(para)))
                del para[:]
            items.append(re.sub(r'^\s*[-*] ', '', ln).strip())
        elif not ln.strip():
            flush()
        else:
            if items:
                out.append('<ul>%s</ul>' %
                           ''.join('<li>%s</li>' % inline(x) for x in items))
                del items[:]
            para.append(ln.strip())
        i += 1
    flush()
    if pending:
        raise SystemExit('도해가 설 절이 없다: %s' % ', '.join(f[0] for f in pending))
    return '\n'.join(out)


# ── 판 한 장을 읽는 순서로 다시 세운다 ─────────────────────────────────
# 받은 글의 순서는 쓴 사람의 순서다 — 앞머리 · 남는 것 · 구조 · 1~N · 한계. 독자의 순서는
# 앞머리 · 목차 · 남는 것 · 1~N · 지켜볼 것 · 한계 · 구조(부록)다. 방법론은 애널리스트
# 보고서처럼 뒤에 둔다. 글 파일은 안 고치고 화면만 다시 배치한다(2026-09-02).

def split_sections(md):
    """앞머리 줄들과 [(제목, 줄들)] — h2 단위."""
    lead, secs, cur = [], [], None
    for ln in md.split('\n'):
        if ln.startswith('## '):
            cur = [ln[3:].strip(), []]
            secs.append(cur)
        elif cur is None:
            lead.append(ln)
        else:
            cur[1].append(ln)
    return lead, secs


def lead_html(lead):
    """「**물음** — …」 세 줄을 표 셋 줄로. 한 문단에 붙어 있으면 셋이 구분이 안 된다."""
    rows = []
    for ln in lead:
        m = re.match(r'^\*\*(물음|바탕|축)\*\*\s*[—-]\s*(.*)$', ln.strip())
        if m:
            rows.append((m.group(1), m.group(2)))
    if not rows:
        return body_html('\n'.join(lead))
    return '<div class="lead">%s</div>' % ''.join(
        '<div class="lk">%s</div><div class="lv">%s</div>' % (k, inline(v)) for k, v in rows)


def subjects_from_tree(secs):
    """부록 트리의 레벨 1 줄 「├─ A. 원인 — 왜 … (방법)」에서 다루는 것을 뽑는다. A→1, B→2 …"""
    subj = {}
    for title, lines in secs:
        if not title.startswith('구조'):
            continue
        for ln in lines:
            m = TREE_TOP.match(ln.strip())
            if m:
                subj[str(ord(m.group(1)) - ord('A') + 1)] = m.group(2)
    return subj


def toc_html(secs):
    """두 칸 — 다루는 것 · 묻는 것. 왼쪽은 트리의 레벨 1 이름, 오른쪽은 절 물음과 소절 물음."""
    subj = subjects_from_tree(secs)
    rows = []
    for title, lines in secs:
        p = parse_head(title)
        if not p or '-' in p[0]:
            continue
        num, method, q = p
        left = subj.get(num) or (q.split(' — ', 1)[1] if ' — ' in q else q)
        subs = [parse_head(l[4:].strip()) for l in lines if l.startswith('### ')]
        subs = ['<span class="tq">%s</span>' % esc(s[2]) for s in subs if s]
        right = '<a href="#s%s">%s</a>' % (num, esc(q.split(' — ', 1)[0]))
        if subs:
            right += '<div class="tsub">%s</div>' % ' '.join(
                '%s %s' % ('①②③④⑤⑥⑦⑧⑨'[k] if k < 9 else '', s) for k, s in enumerate(subs))
        if subj:
            rows.append('<div class="tl"><span class="num">%s</span> %s</div><div class="tr">%s</div>'
                        % (esc(num), esc(left), right))
        else:
            # 트리(부록)가 없는 글은 한 칸 — 절 제목만 앵커로 늘어선다
            rows.append('<div class="tr one"><span class="num">%s</span> %s</div>' % (esc(num), right))
    for title, _lines in secs:
        if title.startswith('한계'):
            rows.append('<div class="tl">한계</div><div class="tr"><a href="#limits">이 회차가 안 말한 것</a></div>')
    heads = ('<div class="th">다루는 것</div><div class="th">묻는 것</div>' if subj
             else '<div class="th">차례</div>')
    cls = 'toc' if subj else 'toc one'
    return '<nav class="%s">%s%s</nav>' % (cls, heads, ''.join(rows))


def insights_html(lines):
    """「이 회차에서 남는 것」 — ①②③ 문단을 카드로. 주장은 굵게, 「→ 3-1. …」 이후는 출처 줄."""
    out = []
    for para in re.split(r'\n\s*\n', '\n'.join(lines).strip()):
        t = ' '.join(para.split())
        if not t:
            continue
        m = re.match(r'^([①②③④⑤⑥])\s*(.*?)\s*(→\s*.*)?$', t, re.S)
        if not m:
            out.append('<p>%s</p>' % inline(t))
            continue
        mark, claim, meta = m.groups()
        h = '<div class="ins"><div class="ins-c"><span class="ins-n">%s</span>%s</div>' % (mark, inline(claim))
        if meta:
            h += '<div class="ins-m">%s</div>' % inline(meta)
        out.append(h + '</div>')
    return '<div class="insights">%s</div>' % ''.join(out)


def lane_html(body, figs):
    lead, secs = split_sections(body)
    numbered = [(t, l) for t, l in secs if parse_head(t) and '-' not in parse_head(t)[0]]
    insights = [(t, l) for t, l in secs if t.startswith('이 회차에서 남는 것')]
    limits = [(t, l) for t, l in secs if t.startswith('한계')]
    appendix = [(t, l) for t, l in secs if t.startswith('구조')]
    rest = [(t, l) for t, l in secs if not (
        parse_head(t) or t.startswith('이 회차에서 남는 것') or t.startswith('한계') or t.startswith('구조'))]
    out = [lead_html(lead), toc_html(secs)]
    for t, l in insights:
        out.append('<h2 id="insights">%s</h2>' % inline(t))
        out.append(insights_html(l))
    used = set()
    for t, l in numbered:
        out.append(heading_html('h2', t, 's%s' % parse_head(t)[0]))
        # 절 머리에 걸린 도해는 여기서 바로 세운다 — 제목 줄을 본문에서 뺐으므로 body_html 은
        # ### 아래에 걸린 것만 잡는다
        top = [f for f in figs if '|' not in f[0] and t.startswith(f[0])]
        out += [fig_block(f) for f in top]
        sub = [f for f in figs if f not in top and (
            ('|' in f[0] and t.startswith(f[0].split('|', 1)[0])) or
            any(x.startswith('### ') and x[4:].strip().startswith(f[0]) for x in l))]
        used.update(f[0] for f in top + sub)
        out.append(body_html('\n'.join(l), sub))
    for t, l in rest:
        out.append('<h2>%s</h2>' % inline(t))
        out.append(body_html('\n'.join(l)))
    for t, l in limits:
        out.append('<h2 id="limits">%s</h2>' % inline(t))
        out.append(body_html('\n'.join(l)))
    for t, l in appendix:
        out.append('<h2 id="appendix" class="apx">부록 — %s</h2>' % inline(t.split('—', 1)[-1].strip() if '—' in t else t))
        out.append(body_html('\n'.join(l)))
    missing = [f[0] for f in figs if f[0] not in used]
    if missing:
        raise SystemExit('도해가 설 절이 없다: %s' % ', '.join(missing))
    return '\n'.join(out)


# ── 재료 읽기 ────────────────────────────────────────────────────────

def episodes():
    eps = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith('.md'):
            continue
        slug = name[:-3]
        meta, body = front(io.open(os.path.join(SRC, name), encoding='utf-8').read())
        lanes = []
        for key, emo, label, sub in LANES:
            path = os.path.join(LANE_DIR, '%s-%s.md' % (slug, key))
            if os.path.exists(path):
                lmeta, lbody = front(io.open(path, encoding='utf-8').read())
                lanes.append({'key': key, 'emo': emo, 'label': label, 'sub': sub,
                              'meta': lmeta, 'body': lbody,
                              'src': 'insights/semidoped/%s-%s.md' % (slug, key)})
        eps.append({'slug': slug, 'meta': meta, 'lanes': lanes,
                    'one': one_line(body),
                    'note': NOT_EPISODE.get(slug, ''),
                    'raw': 'content/understanding/Semi Doped/%s.md' % slug})
    eps.sort(key=lambda e: e['meta'].get('date', ''), reverse=True)
    return eps


CSS = '''
*{box-sizing:border-box}
body{margin:0;background:#f6f7f9;color:#1b1f27;
 font:15px/1.8 -apple-system,"Segoe UI","Malgun Gothic",sans-serif}
a{color:inherit}
.wrap{max-width:720px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:26px;margin:0 0 6px}
.sub{color:#66707f;font-size:13px;margin:0 0 28px;line-height:1.7}
.secnav{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
.secnav a{text-decoration:none;font-size:13px;padding:5px 12px;border:1px solid #d5dae2;border-radius:16px;background:#fff;color:#3a4150}
.secnav a:hover{background:#eef1f6}
.secnav a small{color:#8a93a1;margin-left:4px}
.sec{display:flex;align-items:baseline;gap:10px;margin:34px 0 6px;font-size:17px;scroll-margin-top:16px}
.sec small{font-size:12px;color:#8a93a1;font-weight:400}
.rows{border-top:1px solid #e2e5ea}
.row{display:block;padding:16px 4px;border-bottom:1px solid #e2e5ea;
 text-decoration:none;color:inherit}
a.row:hover{background:#eef1f6}
.rmeta{font-size:12px;color:#8a93a1;display:flex;gap:10px;flex-wrap:wrap}
.rtitle{font-size:16px;font-weight:600;margin:3px 0 4px;line-height:1.5}
.rone{font-size:13px;color:#5b6472;line-height:1.7}
.tags{display:flex;gap:5px;margin-top:7px;flex-wrap:wrap}
.tag{font-size:11px;padding:2px 8px;border-radius:11px;background:#e7ebf1;color:#4c5563}
.tag.on{background:#1b1f27;color:#fff}
.row.dead{opacity:.62}
.why{font-size:12px;color:#8a93a1;margin-top:6px}
.back{display:inline-block;font-size:13px;color:#66707f;margin-bottom:18px;
 text-decoration:none}
.whobox{margin:12px 0 4px;padding:10px 14px;background:#fff;border:1px solid #e2e5ea;border-radius:8px}
.who{font-size:13px;color:#4c5563;line-height:1.8}
.who b{color:#1b1f27;margin-right:6px}
.pn{color:#2b5d8a;font-weight:600}
.pn.g0{color:#7a4a1e}.pn.g1{color:#3d6b3a}.pn.g2{color:#6a3d7a}.pn.g3{color:#8a3a3a}
.pmeta{font-size:12px;color:#8a93a1;line-height:1.9;margin:0 0 26px;
 padding-bottom:18px;border-bottom:1px solid #e2e5ea}
.lane{margin:0 0 44px}
.lhead{display:flex;align-items:baseline;gap:9px;margin:0 0 4px}
.lhead b{font-size:19px;white-space:nowrap}
.lhead span{font-size:12px;color:#8a93a1}
.ltitle{font-size:15px;font-weight:600;line-height:1.6;margin:10px 0 20px;
 padding:12px 14px;background:#fff;border-left:3px solid #1b1f27;border-radius:0 6px 6px 0}
.lane h2{font-size:20px;margin:44px 0 12px;line-height:1.45;padding-top:18px;border-top:1px solid #e2e5ea;scroll-margin-top:22px}
.lane h2.apx{color:#66707f}
.lane h3{font-size:16px;margin:26px 0 8px;line-height:1.5}
.lane p{margin:0 0 20px}
.lane ul{margin:0 0 14px;padding-left:20px}
.lane li{margin:0 0 6px}
.q{color:#5b6472}
.num{display:inline-block;min-width:22px;padding:0 6px;margin-right:4px;border-radius:5px;
 background:#e7ebf1;color:#3a4150;font-size:12px;font-weight:700;line-height:20px;text-align:center;vertical-align:2px}
h3 .num{background:#e7ebf1;color:#3a4150}
.chip{display:inline-block;padding:0 7px;margin-left:2px;border-radius:10px;background:#eef1f6;color:#3a4150;
 font-size:11px;font-weight:700;line-height:18px;vertical-align:2px;white-space:nowrap}
.mv{font-size:12px;color:#66707f;margin-left:4px}
.lead{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:0 0 22px;padding:12px 14px;
 background:#fff;border:1px solid #e2e5ea;border-radius:8px;font-size:14px;line-height:1.7}
.lk{font-weight:700;color:#66707f;white-space:nowrap}
.toc{display:grid;grid-template-columns:auto 1fr;gap:8px 18px;margin:0 0 30px;padding:14px 16px;
 background:#fff;border:1px solid #e2e5ea;border-radius:8px;font-size:14px;line-height:1.6}
.toc.one{grid-template-columns:1fr;gap:6px}
.toc .th{font-size:11px;font-weight:700;color:#8a93a1;letter-spacing:.04em}
.toc .tl{white-space:nowrap}
.toc .tr a{text-decoration:none;font-weight:600;border-bottom:1px solid #c9ced6}
.toc .tsub{font-size:13px;color:#66707f;margin-top:2px}
.toc .tq{margin-right:8px}
.insights{display:grid;gap:10px;margin:0 0 10px}
.ins{padding:12px 14px;background:#fff;border:1px solid #e2e5ea;border-left:4px solid #9aa3b2;border-radius:0 8px 8px 0}
.ins-c{font-weight:700;line-height:1.65}
.ins-n{color:#3a4150;margin-right:6px}
.ins-m{font-size:13px;color:#66707f;margin-top:6px;line-height:1.65}
.sowhat{margin:4px 0 18px;padding:10px 14px;background:#fff;border-left:3px solid #1b1f27;border-radius:0 6px 6px 0;line-height:1.7}
.sw{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.06em;color:#66707f;margin-right:8px;vertical-align:1px}
code{background:#e9edf2;padding:1px 5px;border-radius:4px;font-size:.9em}
.tree{margin:0 0 18px;padding:12px 14px;background:#fff;border:1px solid #dfe3e9;border-radius:8px;font-size:13.5px;line-height:1.6}
.tn{padding:3px 0 3px 0;border-left:2px solid #e2e5ea}
.tn.d0{border:0;font-weight:700;font-size:14px;margin-bottom:6px}
.tn.d1{margin-left:0;padding-left:10px;font-weight:600;margin-top:8px}
.tn.d2{margin-left:14px;padding-left:10px}
.tn.d3{margin-left:28px;padding-left:10px;color:#3a4150}
.tn.d4{margin-left:42px;padding-left:10px;color:#3a4150}
.tn.d5,.tn.d6{margin-left:56px;padding-left:10px;color:#3a4150}
.lref{font-size:11px;color:#8a93a1;margin-left:4px}
.tw{overflow-x:auto;margin:0 0 18px}
table{border-collapse:collapse;font-size:13px;background:#fff;min-width:100%}
th,td{border:1px solid #dfe3e9;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#eef1f6;font-weight:600;white-space:nowrap}
@media (max-width:640px){
 .tw table,.tw thead,.tw tbody,.tw tr,.tw td{display:block;min-width:0;width:auto}
 .tw thead{display:none}
 .tw tr{border:1px solid #dfe3e9;border-radius:8px;margin:0 0 10px;background:#fff}
 .tw td{border:0;border-top:1px solid #eef1f6;padding:6px 10px}
 .tw td:first-child{border-top:0;font-weight:600}
 .tw td::before{content:attr(data-label);display:block;font-size:11px;color:#8a93a1;margin-bottom:1px}
 .toc{grid-template-columns:1fr}
 .toc .th:nth-child(2){display:none}
 .toc .tl{white-space:normal}
}
.foot{margin-top:40px;font-size:12px;color:#8a93a1;line-height:1.9}
''' + semidoped_figs.CSS

HEAD = ('<!doctype html><html lang="ko"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>%s</title><style>%s</style><div class="wrap">')


def row_html(ep):
    m = ep['meta']
    tags = []
    # 판이 선 것만 표시한다 — 회색 「🔧 기술」 꼬리표는 「없음」을 말하는 것이라 걷었다(2026-09-02)
    for key, emo, label, _sub in LANES:
        if any(l['key'] == key for l in ep['lanes']):
            tags.append('<span class="tag on">%s %s</span>' % (emo, label))
    # 날짜 옆에는 진행자 말고 다른 참가자(게스트·발표자)만 — 이름과 짧은 소개(2026-09-02).
    # 진행자 둘뿐인 회차는 날짜만 선다
    others = [x.strip() for x in m.get('people', '').split(' / ') if x.strip() and not x.strip().startswith('진행')]
    onames = [n for x in others for n in PN_RE.findall(x)]
    who = ' · '.join(PN_RE.sub(lambda mm: '<span class="pn g%d">%s</span>' % (onames.index(mm.group(1)) % PN_COLORS, mm.group(1)), esc(x))
                    for x in others)
    inner = ('<div class="rmeta"><span>%s</span>%s</div>'
             '<div class="rtitle">%s</div>'
             % (esc(m.get('date', '')), ('<span>%s</span>' % who) if who else '',
                esc(m.get('title', ep['slug']))))
    if ep['one']:
        inner += '<div class="rone">%s</div>' % esc(ep['one'])
    inner += '<div class="tags">%s</div>' % ''.join(tags)
    if ep['lanes']:
        return '<a class="row" href="semidoped/%s.html">%s</a>' % (ep['slug'], inner)
    why = ep['note'] or '아직 판이 안 섰다'
    inner += '<div class="why">글 없음 — %s</div>' % esc(why)
    return '<div class="row dead">%s</div>' % inner


def post_html(ep):
    m = ep['meta']
    out = [HEAD % (esc(m.get('title', ep['slug'])) + ' — Semi Doped', CSS)]
    out.append('<a class="back" href="../Semi Doped 대시보드.html">← 회차 목록</a>')
    out.append('<h1>%s</h1>' % esc(m.get('title', ep['slug'])))
    # 화자 — 팟캐스트라 누가 말하는 사람인지가 먼저다. 요약본 frontmatter people 에
    # 「진행 … / 발표 …」로 적고, 없으면 speaker 만 낸다. 전사에 없는 소속·직함은 안 적는다
    people = m.get('people', '')
    HOSTS[:] = [n for x in people.split(' / ') if x.strip().startswith('진행') for n in PN_RE.findall(x)]
    NAMES[:] = [n for x in people.split(' / ') if not x.strip().startswith('진행') for n in PN_RE.findall(x)]

    def who_line(x):
        k, v = x.strip().split(' ', 1)
        v = PN_RE.sub(lambda mm: '<span class="%s">%s</span>' % (pn_cls(mm.group(1)), mm.group(1)), esc(v))
        return '<div class="who"><b>%s</b> %s</div>' % (esc(k), v)
    who = ('<div class="whobox">%s</div>' % ''.join(who_line(x) for x in people.split(' / ') if ' ' in x.strip())) if people else ''
    out.append('<div class="pmeta">%s · %s<br>원문 <a href="%s">%s</a> · '
               '요약본 <a href="%s">저장소</a>%s</div>'
               % (esc(m.get('date', '')), esc(m.get('speaker', '')),
                  esc(m.get('source', '')), esc(m.get('source', '')),
                  blob(ep['raw']), who))
    for lane in ep['lanes']:
        lm = lane['meta']
        out.append('<div class="lane">')
        out.append('<div class="lhead"><b>%s %s 판</b><span>%s · %s 가 씀</span></div>'
                   % (lane['emo'], lane['label'], esc(lane['sub']),
                      esc(lm.get('model', ''))))
        if lm.get('title'):
            out.append('<div class="ltitle">%s</div>' % esc(lm['title']))
        out.append(lane_html(lane['body'],
                             semidoped_figs.figs_for(ep['slug'], lane['key'])))
        out.append('<div class="foot">받은 글을 문장 그대로 싣는다. '
                   '원본 <a href="%s">%s</a> · 페르소나 %s</div>'
                   % (blob(lane['src']), esc(lane['src']),
                      esc(lm.get('persona', ''))))
        out.append('</div>')
    out.append('</div>')
    return ''.join(out)


def index_html(eps):
    live = sum(1 for e in eps if e['lanes'])
    out = [HEAD % ('Semi Doped 대시보드', CSS)]
    out.append('<h1>🎙️ Semi Doped</h1>')
    out.append('<div class="sub">칩을 만드는 사람이 나와 앉아 설계를 말하는 팟캐스트. '
               '회차마다 두 판이 따로 읽는다 — ⚖ 전략은 전략 컨설턴트 출신 애널리스트의 해설로, '
               '🔧 기술은 주제 아래 순서와 층위로.<br>'
               '글이 있는 회차만 싣는다 — 회차 %d편 중 %d편.</div>' % (len(eps), live))
    # 글 없는 회차는 목록에 안 싣는다 — 「글 없음」 줄이 열여덟 개 서 있으면 목록이 아니라 빈칸이다(2026-09-02)
    # 섹션 머리줄로 갈라 세운다. 머리에 「글 m편 / 회차 n편」
    groups = []
    for code, name in SECTIONS:
        allc = [e for e in eps if e['meta'].get('section', '') == code and not e['note']]
        withl = [e for e in allc if e['lanes']]
        if withl:
            groups.append((code, name, allc, withl))
    # 섹션 선택 줄 — 맨 위에서 누르면 그 섹션으로 간다. 접지 않는다(2026-09-02)
    out.append('<nav class="secnav">%s</nav>' % ''.join(
        '<a href="#sec-%s">%s <small>%d</small></a>' % (code, esc(name), len(withl)) for code, name, _a, withl in groups))
    for code, name, allc, withl in groups:
        out.append('<h2 class="sec" id="sec-%s"><span>%s</span><small>글 %d편 / 회차 %d편</small></h2>' % (code, esc(name), len(withl), len(allc)))
        out.append('<div class="rows">%s</div>' % ''.join(row_html(e) for e in withl))
    stray = [e for e in eps if e['lanes'] and e['meta'].get('section', '') not in dict(SECTIONS)]
    if stray:
        raise SystemExit('섹션 코드가 없는 회차: ' + ', '.join(e['slug'] for e in stray))
    out.append('<div class="foot">글은 원문 전사를 통째로 읽힌 뒤 받은 것이고 '
               '문장을 고치지 않는다. 값이 원문에 있는지는 사람이 대조한다.</div>')
    out.append('</div>')
    return ''.join(out)


def check_ui(index, posts):
    """이 장의 규약. 워치 장처럼 아카이브 부품을 안 쓰므로 여기서 직접 본다."""
    bad = []
    if '<details' in index or any('<details' in p for p in posts):
        bad.append('접는 것이 있다 — 이 장은 목록과 글뿐이다')
    if 'class="sec"' not in index:
        bad.append('목록에 섹션 머리줄이 없다')
    if 'class="secnav"' not in index:
        bad.append('목록 위에 섹션 선택 줄이 없다')
    if 'class="tile' in index:
        bad.append('타일이 있다 — 첫 화면은 회차 줄이다')
    for p in posts:
        if 'class="pmeta"' not in p:
            bad.append('글 페이지에 회차 메타(언제 것·누가)가 없다')
        if '<code>```' in p or '├─' in p:
            bad.append('트리 선 글자가 화면에 남았다 — 펜스가 문단으로 뭉개졌거나 tree_html 을 안 거쳤다')
        if '<nav class="toc' not in p:
            bad.append('글 페이지에 목차(다루는 것 · 묻는 것)가 없다')
        if 'id="appendix"' in p and 'id="limits"' in p and p.index('id="appendix"') < p.index('id="limits"'):
            bad.append('구조(부록)가 한계보다 앞에 섰다 — 방법론은 뒤에 둔다')
        if 'id="insights"' in p and 'id="s1"' in p and p.index('id="insights"') > p.index('id="s1"'):
            bad.append('「이 회차에서 남는 것」이 본문 뒤에 섰다')
        if '회차 목록' not in p:
            bad.append('글 페이지에서 목록으로 돌아갈 길이 없다')
    dead = re.findall(r'<div class="row dead">(.*?)</div>\s*(?=<a class="row"|'
                      r'<div class="row|</div>)', index, re.S)
    for d in dead:
        if '글 없음' not in d:
            bad.append('판이 없는 줄에 이유가 안 적혔다')
    if re.search(r'<a class="row"[^>]*>(?:(?!</a>).)*글 없음', index, re.S):
        bad.append('판이 없는 줄에 링크가 걸렸다')
    return bad


def check_figs():
    """도해 규칙 둘을 생성 때 기계로 본다 — 글자에 든 값이 전사에 있나, 배치가 겹치나.
    도형 개수가 값인지는 사람이 본다."""
    bad = []
    for (slug, lane), figs in semidoped_figs.FIGS.items():
        for key, title, svg, _cap in figs:
            miss = semidoped_figs.missing_values(slug, svg)
            if miss:
                bad.append('%s/%s %s — 전사에 없는 값 %s' % (slug, lane, title, miss))
            # 엄격 모드로 본다(줄임말·비스듬한 선까지). 화살촉 마커는 <defs> 안 path 라
            # 비스듬한 선으로 읽히므로 defs 만 걷고 잰다
            bare = re.sub(r'<defs>.*?</defs>', '', svg, flags=re.S)
            for h in check_fig.hits(bare, strict=True):
                bad.append('%s/%s %s — %s' % (slug, lane, title, h))
    return bad


def main():
    eps = episodes()
    bad = check_figs()
    if bad:
        raise SystemExit('도해 규칙 위반\n  ' + '\n  '.join(bad))
    if not os.path.isdir(POST_DIR):
        os.makedirs(POST_DIR)
    posts = []
    for ep in eps:
        if not ep['lanes']:
            continue
        h = post_html(ep)
        posts.append(h)
        io.open(os.path.join(POST_DIR, ep['slug'] + '.html'), 'w',
                encoding='utf-8', newline='').write(h)
    idx = index_html(eps)
    bad = check_ui(idx, posts)
    if bad:
        raise SystemExit('규약 위반\n  ' + '\n  '.join(bad))
    io.open(OUT, 'w', encoding='utf-8', newline='').write(idx)
    # 모바일 폭에서 옆으로 밀리나 — 브라우저로만 잴 수 있어 Playwright 를 부른다.
    # 없으면 넘어가지 않고 멈춘다. 이 규약은 눈으로 본 결함에서 나왔다
    import subprocess
    targets = [OUT] + [os.path.join(POST_DIR, ep['slug'] + '.html') for ep in eps if ep['lanes']]
    r = subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_scroll.js')]
                       + targets, capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        raise SystemExit('모바일 가로 스크롤\n' + (r.stdout or '') + (r.stderr or ''))
    live = sum(1 for e in eps if e['lanes'])
    lanes = sum(len(e['lanes']) for e in eps)
    print('Semi Doped — 회차 %d줄 · 글 %d장 · 판 %d개  ->  %s'
          % (len(eps), live, lanes, os.path.basename(OUT)))


if __name__ == '__main__':
    main()
