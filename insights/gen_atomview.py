# 인사이트와 근거 페이지 생성 — atoms + synth + views/process.json → 자기완결 HTML
# 판단이 주인이고 원자는 근거다. 인사이트를 먼저 놓고 각 인사이트 안에서 인용 원자를
# line_text(원문 그 줄)와 함께 펼친다. 두 축 다이어그램은 그 아래 "근거 지도"로 —
# 어느 칸이 두텁고 어디가 비었나, 각 원자가 제 칸에 들어갔나를 보는 검토면이다.
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca
import style

ROOT = ca.ROOT
OUT = os.path.join(ROOT, '대시보드', '인사이트와 근거.html')
VERIFY = os.path.join(ROOT, 'insights', 'verify.json')
STCLS = {'열림': 'open', '적중': 'hit', '빗나감': 'miss', '무효': 'void'}

STACK = ca.STACK
# 화면은 큰 것부터 — 연료·지정학에서 전자·공정으로 내려간다.
# ca.STACK(정본)은 EDGES 연결성 판정에 쓰이므로 뒤집지 않는다
DISP = list(reversed(STACK))
STACK_ROWS = [DISP[i:i + 2] for i in range(0, len(DISP), 2)]

# 노드 이름만으로는 그 칸이 무엇을 담는지 모른다. 설계 문서
# docs/superpowers/specs/2026-07-30-원자-뷰-인사이트-design.md의 「담는 것」 표를 줄인 것
NODE_NOTE = {
    '연료·지정학': 'LNG·원유, 해협·항로, 수출 통제',
    '전력망': '예비율, 접속 대기, 변압기·송전, 발전원',
    '데이터센터': '부지, 건설 일정, 시설 전력·용수, 인허가',
    '랙': '랙 전력 밀도, 배전(800VDC), 스케일업 링크',
    '열': '열저항, 냉각판, TIM, 마이크로플루이딕, 칠러',
    'HBM': '적층·본딩·수율, 대역폭, 가속기 탑재량',
    '일반 D램': 'DDR·LPDDR·GDDR, 커먼디티 수급, 계약가',
    '낸드·스토리지': '단수·덱 구조, 비트 밀도, 대용량 저장',
    '칩': '다이 구성, 패키징(CoWoS·EMIB), 본딩, 연산 성능',
    '전자·공정': '노드 세대, 가동률, 수율, CFET',
}


# 스택을 글자 칩으로만 늘어놓으면 열 칸이 그냥 목록으로 보인다. 실제 관계는
# ① 바깥 넷은 안쪽을 담는 포함 관계이고 ② 랙 안의 다섯은 옆으로 이어진 사슬이며
# ③ 인사이트는 EDGES 위에서 이어진 칸끼리만 묶을 수 있다(check_atoms C6).
# 그림은 그 세 가지를 한 번에 보여 준다 — 문장으로는 세 번 말해야 한다.
NEST = ['연료·지정학', '전력망', '데이터센터', '랙']   # 바깥 → 안, 서로를 담는다
CHAIN = ['열', '칩', 'HBM', '일반 D램', '낸드·스토리지']  # 랙 안, 옆으로 이어진다
#  CHAIN의 이웃은 전부 EDGES에 있는 실제 연결이다(열–칩, 칩–HBM, HBM–일반 D램, 일반 D램–낸드).
#  순서를 바꾸면 그림이 없는 연결을 있는 것처럼 보이게 하므로 EDGES를 먼저 확인할 것


def stack_svg(ncount):
    """포함 관계를 중첩 사각형으로, 랙 안의 사슬을 가로 배치로 그린다.
    색·글자는 currentColor라 라이트·다크 어느 쪽에서도 읽힌다."""
    W, H = 720, 400
    p = ['<svg viewBox="0 0 %d %d" role="img" width="100%%" '
         'style="max-width:100%%;height:auto;color:inherit" '
         'aria-label="%s">'
         % (W, H, esc('연료·지정학이 전력망을, 전력망이 데이터센터를, 데이터센터가 랙을 담고, '
                      '랙 안에 열·칩·HBM·일반 D램·낸드가 옆으로 이어져 있다. '
                      '전자·공정은 칩을 만든다'))]
    p.append('<defs><marker id="stkar" viewBox="0 0 10 10" refX="9" refY="5" '
             'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
             '<path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>')

    def label(x, y, txt, size=12, weight=800, anchor='start', op=1.0):
        p.append('<text x="%g" y="%g" font-size="%g" font-weight="%d" '
                 'text-anchor="%s" fill="currentColor" fill-opacity="%.2f">%s</text>'
                 % (x, y, size, weight, anchor, op, esc(txt)))

    # ── 바깥 넷 — 담는 관계는 중첩으로 말한다. 화살표를 쓰면 흐름으로 읽힌다
    for i, name in enumerate(NEST):
        x, y = 6 + i * 18, 6 + i * 34
        w, h = W - 2 * x, H - y - (6 + i * 12)
        p.append('<rect x="%g" y="%g" width="%g" height="%g" rx="14" '
                 'fill="none" stroke="currentColor" stroke-opacity="%.2f"/>'
                 % (x, y, w, h, 0.32 + i * 0.14))
        label(x + 13, y + 21, name)
        label(x + 15 + len(name) * 12.2, y + 21, '원자 %d개' % ncount.get(name, 0),
              size=10.5, weight=700, op=.55)

    # ── 랙 안의 다섯 — 옆으로 이어진 사슬. 이웃끼리만 실제로 연결돼 있다
    bx, by, bw, bh, gap = 72, 150, 107, 72, 10
    for i, name in enumerate(CHAIN):
        x = bx + i * (bw + gap)
        empty = not ncount.get(name)
        p.append('<rect x="%g" y="%g" width="%g" height="%g" rx="10" fill="none" '
                 'stroke="currentColor" stroke-opacity="%.2f"%s/>'
                 % (x, by, bw, bh, .28 if empty else .7,
                    ' stroke-dasharray="4 3"' if empty else ''))
        label(x + bw / 2, by + 30, name, size=12.5, anchor='middle')
        label(x + bw / 2, by + 50, '원자 %d개' % ncount.get(name, 0),
              size=10.5, weight=700, anchor='middle', op=.55)
        if i:  # 이웃 사이의 짧은 연결선 — 이 선이 있어야 한 인사이트로 묶인다
            p.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="currentColor" '
                     'stroke-width="2" stroke-opacity=".55"/>'
                     % (x - gap, by + bh / 2, x, by + bh / 2))
    label(bx + (bw * 5 + gap * 4) / 2, by - 12,
          '이어진 이웃끼리만 한 인사이트로 묶는다', size=11, weight=700,
          anchor='middle', op=.6)

    # ── 전자·공정은 담기는 게 아니라 칩을 만든다. 그래서 혼자 화살표를 갖는다
    cx = bx + 1 * (bw + gap) + bw / 2          # 칩 칸 중앙
    p.append('<rect x="%g" y="264" width="%g" height="54" rx="10" fill="none" '
             'stroke="currentColor" stroke-opacity=".7"/>' % (cx - bw / 2, bw))
    label(cx, 288, '전자·공정', size=12.5, anchor='middle')
    label(cx, 306, '원자 %d개' % ncount.get('전자·공정', 0),
          size=10.5, weight=700, anchor='middle', op=.55)
    p.append('<line x1="%g" y1="264" x2="%g" y2="%g" stroke="currentColor" '
             'stroke-width="2" marker-end="url(#stkar)"/>' % (cx, cx, by + bh + 4))
    label(cx + 12, 252, '칩을 만든다', size=11, weight=700, op=.75)
    p.append('</svg>')
    return ('<figure class="stkfig">%s<figcaption>바깥 넷은 서로를 담고, 랙 안의 다섯은 '
            '옆으로 이어져 있습니다. 인사이트는 이 그림에서 <b>선으로 이어진 칸끼리만</b> '
            '묶을 수 있습니다 — 칩과 랙, 칩과 일반 D램처럼 그림에 안 그린 연결도 몇 개 더 '
            '있습니다. 점선 칸은 아직 원자가 없는 칸입니다.</figcaption></figure>'
            % ''.join(p))


# 19건이 한 줄로 죽 늘어서면 어디부터 읽을지가 안 보인다. 읽는 사람이 실제로 쓰는 단위는
# 스택 좌표가 아니라 주제다 — 전기, 열, 메모리, 칩. 좌표는 근거를 매다는 축이고,
# 주제는 글을 찾는 문이다. 둘을 같은 화면에서 겸하게 하면 둘 다 흐려진다.
THEMES = [
    ('power', '전기를 어떻게 끌어오나',
     '발전소를 직접 짓는 쪽으로 기울었고, 그 전기를 랙까지 어떤 형태로 나르느냐가 갈렸다.'),
    ('cool', '열을 어디서 빼나',
     '막히는 지점이 건물에서 칩 안으로 내려왔다. 누가 액체로 가고 누가 공기로 남나.'),
    ('mem', '메모리는 왜 모자라나',
     '수요가 아니라 만드는 쪽 사정이다 — 미세화 정체, HBM으로 빠지는 웨이퍼, 중국의 진입.'),
    ('chip', '칩은 무엇으로 갈리나',
     '성능이 아니라 몇 장 받느냐다. 미세화가 되돌아간 자리에서 이득은 다른 층으로 옮겨 갔다.'),
    ('rack', '랙에서 무엇이 바뀌나',
     '칩이 세진 값을 기판과 연결이 대신 치른다. 랙 안과 밖은 역할이 갈렸다.'),
    ('order', '무엇이 먼저 고정되나',
     '되돌릴 수 없는 순서다 — 착공과 웨이퍼 배정이 뒤의 선택지를 미리 지운다.'),
]
THEME_IDX = {k: i for i, (k, _, _) in enumerate(THEMES)}

# 자동 규칙이 못 맞히는 세 건 — 좌표는 A인데 글이 실제로 다루는 것은 B다.
# 규칙을 억지로 늘리는 대신 여기 세 줄로 적는다
THEME_FIX = {
    'stack-랙-데이터센터-02.md': 'power',            # 800V 배전 — 좌표엔 전력망이 없다
    'stack-전자공정-01.md': 'mem',                   # 미세화 정체가 만든 메모리 부족
    'stack-전자공정-칩-메모리-랙-01.md': 'chip',      # 자체 칩 이야기 — 메모리는 배경
    'stack-칩-랙-01.md': 'rack',                     # 값이 옮겨 간 곳이 기판이다 — 칩이 아니라
}


def theme_of(ins):
    if ins['file'] in THEME_FIX:
        return THEME_FIX[ins['file']]
    if ins['view'] == 'process':
        return 'order'
    n = set(ins['nodes'])
    if n & {'HBM', '일반 D램', '낸드·스토리지'}:
        return 'mem'
    if '열' in n:
        return 'cool'
    if n & {'연료·지정학', '전력망'}:
        return 'power'
    if n & {'전자·공정', '칩'}:
        return 'chip'
    return 'rack'


def payoff_line(ins):
    """접힌 카드에서도 「그래서 무엇이 달라지나」 첫 줄이 보이게 — 열지 않고 값을 판단한다"""
    for name, lines in ins['sections']:
        if name == '그래서 무엇이 달라지나' and lines:
            s = re.sub(r'^-\s*', '', lines[0]).strip()
            s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
            s = re.sub(r'`(.+?)`', r'\1', s)
            s = re.sub(r'\(A-\d{6}-\d{2}(?:,\s*A-\d{6}-\d{2})*\)', '', s).replace(' .', '.')
            # 상자가 잘라 「...」로 끝나면 문장이 끊긴 자리가 남는다 — 문장 경계에서 우리가 끊는다
            sents = re.findall(r'[^.]*\.', s)
            out = ''
            for t in sents:
                if out and len(out) + len(t) > 75:
                    break
                out += t
            return (out or s).strip()
    return ''


def esc(s):
    return (str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def load_insights(atoms):
    out = []
    for p in sorted(glob.glob(os.path.join(ca.SYNTH, '*.md'))):
        meta, body = ca.parse_synth(io.open(p, encoding='utf-8').read())
        if not meta:
            continue
        sec = ca.sections(body)
        claim = ' '.join(sec.get('주장') or [])
        claim = re.sub(r'\*\*(.+?)\*\*', r'\1', claim).strip()
        out.append({
            'file': os.path.basename(p),
            'view': meta.get('view') or 'stack',
            'nodes': meta.get('nodes') or ([meta['node']] if meta.get('node') else []),
            'stages': meta.get('stages') or [],
            'atoms': meta.get('atoms') or [],
            'dismissed': meta.get('dismissed') or [],
            'as_of': meta.get('as_of') or '',
            'claim': claim,
            'subhead': meta.get('subhead') or '',
            'headline': meta.get('headline') or re.split(r'(?<=다)\.', claim)[0].strip('* '),
            'sections': [(k, v) for k, v in sec.items() if k != '주장'],
        })
    return out


def md_inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s



def load_theses():
    """종합 판단 — 문서 여럿을 겹쳐 세운 판단. 인사이트보다 위에 놓는다"""
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'insights', 'theses', '*.md'))):
        t = io.open(p, encoding='utf-8').read()
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
        if not m:
            continue
        fm, body = m.group(1), m.group(2)
        def f(k, d=''):
            r = re.search(r'^%s: (.*)$' % k, fm, re.M)
            return r.group(1).strip() if r else d
        out.append({
            'id': f('id'), 'title': f('title'), 'question': f('question'),
            'span': f('doc_span'), 'as_of': f('as_of'), 'review_by': f('review_by'),
            'atoms': re.findall(r'A-\d{6}-\d{2}', f('atoms')),
            'lis': re.findall(r'L-\d{8}-\d{4}', f('li_signals')),
            'docs': len([x for x in f('docs').strip('[]').split(',') if x.strip()]),
            'body': body,
        })
    return out


def md_block(s):
    """판단 본문 — 표·굵은 글씨·목록만 쓰는 좁은 마크다운이라 이 정도로 충분하다"""
    html, rows, para = [], [], []
    def flush_rows():
        if not rows:
            return
        body = [r for r in rows if not re.match(r'^\|[\s\-|]+\|$', r)]
        cells = [[c.strip() for c in r.strip('|').split('|')] for r in body]
        head, rest = cells[0], cells[1:]
        html.append('<div class="tw"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                    % (''.join('<th>%s</th>' % md_inline(c) for c in head),
                       ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % md_inline(c) for c in r) for r in rest)))
        rows.clear()
    def flush_para():
        if para:
            html.append('<p>%s</p>' % md_inline(' '.join(para)))
            para.clear()
    for line in s.splitlines():
        ln = line.rstrip()
        if ln.startswith('|'):
            flush_para(); rows.append(ln); continue
        flush_rows()
        if not ln.strip():
            flush_para(); continue
        if ln.startswith('## '):
            flush_para(); html.append('<h4>%s</h4>' % md_inline(ln[3:])); continue
        if ln.startswith('- '):
            flush_para(); html.append('<li>%s</li>' % md_inline(ln[2:])); continue
        para.append(ln.strip())
    flush_rows(); flush_para()
    # 목록은 여닫이를 상태로 처리한다 — 정규식으로 감싸면 표 안의 문자열까지 건드린다
    out, inlist = [], False
    for h in html:
        if h.startswith('<li>') and not inlist:
            out.append('<ul>'); inlist = True
        elif not h.startswith('<li>') and inlist:
            out.append('</ul>'); inlist = False
        out.append(h)
    if inlist:
        out.append('</ul>')
    return ''.join(out)


def build():
    atoms = ca.load_atoms()
    pr = json.load(io.open(ca.PROCESS, encoding='utf-8'))
    stages, assign = pr['stages'], pr.get('assign') or {}
    # 단계 설명은 process.json이 정본이다. 첫 문장만 잘라 레일에 싣는다
    stage_note = {k: v.split('. ')[0].rstrip('.')
                  for k, v in (pr.get('stage_note') or {}).items()}
    man = {s['id']: s for s in json.load(io.open(ca.MAN, encoding='utf-8'))['sources']}
    # 검증 대장 — 이 판단이 무엇으로 무너지는지. 판정은 원자로만 하고 C21이 사후 편입을 막는다
    vdata = json.load(io.open(VERIFY, encoding='utf-8')) if os.path.exists(VERIFY) else {'checks': []}
    vchecks = {}
    for c in vdata.get('checks') or []:
        vchecks.setdefault(c['insight'], []).append(c)
    insights = load_insights(atoms)

    adata = []
    for a in atoms:
        src = man.get(a['_source_id'], {})
        adata.append({
            'id': a['id'], 'claim': a.get('claim'), 'value': a.get('value'),
            'cond': a.get('condition'), 'attr': a.get('attributed_to'),
            'line': a.get('line'), 'text': a.get('line_text'),
            'stack': a['view']['stack'], 'stage': assign.get(a['id']),
            'actor': a['view'].get('actor') or [], 'time': a['view']['time'],
            'doc': os.path.basename(src.get('path', a['_path'])),
            'corpus': ca.corpus_of(a['_source_id']),
        })

    ncount = {n: 0 for n in STACK}
    for a in adata:
        ncount[a['stack']] = ncount.get(a['stack'], 0) + 1
    scount = {s: 0 for s in stages}
    for a in adata:
        if a['stage'] in scount:
            scount[a['stage']] += 1
    unassigned = [a for a in adata if not a['stage']]

    # 스택 사슬 — 노드 카드. 원자 0인 노드는 빈 칸으로 남겨 사슬이 어디서 끊겼는지 보이게 한다
    chain = []
    for row in STACK_ROWS:
        cells = []
        for n in row:
            c = ncount.get(n, 0)
            cls = 'cell' + ('' if c else ' empty')
            cells.append('<button class="%s" data-axis="stack" data-key="%s">'
                         '<span class="nm">%s</span><span class="ct">%s</span></button>'
                         % (cls, esc(n), esc(n), ('원자 %d' % c) if c else '원자 0 · 근거 없음'))
        chain.append('<div class="row">%s</div>' % ''.join(cells))
    chain_html = '<div class="chain">%s</div>' % ''.join(chain)

    band = []
    for i, s in enumerate(stages):
        c = scount.get(s, 0)
        band.append('<button class="cell%s" data-axis="process" data-key="%s">'
                    '<span class="ord">%d</span><span class="nm">%s</span><span class="ct">원자 %d</span></button>'
                    % ('' if c else ' empty', esc(s), i + 1, esc(s), c))
    band_html = '<div class="band">%s</div>' % ''.join(band)

    by_id = {a['id']: a for a in adata}

    def atom_card(a, other_axis):
        h = ['<div class="atom"><span class="aid">%s</span>' % esc(a['id'])]
        h.append('<span class="atag">%s</span>' % esc(a[other_axis] or '미배정'))
        h.append('<span class="atag">%s</span>' % esc(a['corpus']))
        h.append('<p class="aclaim">%s</p>' % esc(a['claim']))
        if a['value']:
            h.append('<p class="kv"><span>값</span> %s</p>' % esc(a['value']))
        h.append('<p class="kv"><span>조건</span> %s</p>' % esc(a['cond']))
        h.append('<p class="kv"><span>귀속</span> %s · <span>출처</span> %s %s행 · %s</p>'
                 % (esc(a['attr']), esc(a['doc']), esc(a['line']), esc(a['time'])))
        h.append('<div class="src">%s</div></div>' % esc(a['text']))
        return ''.join(h)

    # 인사이트가 주인이고 원자는 그 밑을 받치는 근거다 — 인사이트 안에서 원문까지 내려간다
    # 순서는 사슬을 따라간다 — 스택은 상류에서 하류로, 프로세스는 앞 단계에서 뒤 단계로.
    # 파일명 알파벳순은 읽는 사람에게 아무 뜻이 없다
    def ins_rank(i):
        if i['view'] == 'stack':
            return (0, min(DISP.index(n) for n in i['nodes'] if n in DISP))
        return (1, min(stages.index(s) for s in i['stages'] if s in stages))
    # 묶음이 먼저고 그 안에서 사슬 순서다. 파일명 알파벳순은 읽는 사람에게 아무 뜻이 없다
    for i in insights:
        i['theme'] = theme_of(i)
    insights.sort(key=lambda i: (THEME_IDX[i['theme']], ins_rank(i)))

    tcount = {}
    for i in insights:
        tcount[i['theme']] = tcount.get(i['theme'], 0) + 1
    # 맨 위 한 줄로 전체 지형을 먼저 준다 — 19건을 훑기 전에 어디로 갈지 고르게
    nav_html = '<nav class="tnav">%s</nav>' % ''.join(
        '<a href="#th-%s">%s<b>%d</b></a>' % (k, esc(lab), tcount[k])
        for k, lab, _ in THEMES if tcount.get(k))

    ins_html = []
    tseen, tmore = 0, False
    FOLD = 3
    prev_view = None
    prev_theme = None
    for ins in insights:
        # 사슬 전체를 보여주고 이 글이 다루는 칸만 강조한다 — 어디쯤 이야기인지 알아야
        # 판단이 놓인다. 나머지는 회색으로 남겨 위치만 표시
        if ins['view'] == 'stack':
            full, on = DISP, set(ins['nodes'])
            kind_label = '스택'
        else:
            full, on = stages, set(ins['stages'])
            kind_label = '프로세스'
        path = [x for x in full if x in on]
        # 축 이름은 글 위 레일에 한 번만 적는다. 카드에는 그 축 위 어디인지만 —
        # 같은 축을 쓰는 글끼리 눈으로 바로 겹쳐 보이게
        bar = ''.join('<i%s></i>' % (' class="on"' if x in on else '') for x in full)
        # 구분자는 언제나 화살표 하나로 — 어떤 카드는 점, 어떤 카드는 화살표면 규칙이 없어 보인다.
        # 중간에 건너뛴 칸이 있으면 막대의 빈 칸이 그것을 말한다
        label = path[0] if len(path) == 1 else '%s → %s' % (path[0], path[-1])
        # 좌표는 헤드라인을 읽은 뒤에 확인하는 값이다 — 이름을 먼저 두고 막대는 그 보조로 붙인다
        chips = ('<span class="cspan">%s</span>'
                 '<span class="axmini" aria-hidden="true">%s</span>' % (esc(label), bar))
        # 「그래서 무엇이 달라지나」가 이 글의 값이다 — 주장 바로 뒤로 끌어올린다.
        # 근거·조건 충돌은 그 판단을 받치는 장치이므로 뒤로 간다
        ORDER = ['그래서 무엇이 달라지나', '되돌릴 수 없는 지점', '근거', '조건 충돌',
                 '아직 모르는 것', '검토 후 무관']
        def rank(name):
            return ORDER.index(name) if name in ORDER else len(ORDER)
        secs = []
        for name, lines in sorted(ins['sections'], key=lambda kv: rank(kv[0])):
            items = ''.join('<li>%s</li>' % md_inline(re.sub(r'^-\s*', '', l)) for l in lines)
            cls = ' class="payoff"' if name == '그래서 무엇이 달라지나' else ''
            secs.append('<h4%s>%s</h4><ul%s>%s</ul>' % (cls, esc(name), cls, items))
        oax = 'stage' if ins['view'] == 'stack' else 'stack'
        cards = [atom_card(by_id[aid], oax) for aid in ins['atoms'] if aid in by_id]
        dis = [atom_card(by_id[aid], oax) for aid in ins['dismissed'] if aid in by_id]
        ev = ('<details class="ev"><summary>근거 원자 <b>%d개</b> — 각 원자의 원문 줄까지</summary>%s</details>'
              % (len(cards), ''.join(cards)))
        if dis:
            ev += ('<details class="ev"><summary>검토 후 무관 <b>%d개</b> — 같은 칸이지만 이 주장과 안 맞물린다</summary>%s</details>'
                   % (len(dis), ''.join(dis)))
        # 이 판단이 무엇으로 무너지는지를 글 안에 박아 둔다. 나중에 만든 질문은 검증이 아니므로
        # 언제 열었는지(opened_on)를 같이 적는다
        mine = vchecks.get(ins['file']) or []
        vh = ''
        if mine:
            items = ''.join(
                '<li><b>%s</b> <span class="vst %s">%s</span>'
                '<br><span class="vw">볼 것</span> %s'
                '<br><span class="vw">정해지는 것</span> %s'
                '<br><span class="vm">%s 기록 · 기한 %s</span></li>'
                % (esc(c['question']), STCLS.get(c['status'], ''), esc(c['status']),
                   esc(c['watch']), esc(c['settles']), esc(c['opened_on']), esc(c['due']))
                for c in mine)
            vh = '<h4 class="falsify">무엇으로 무너지나</h4><ul class="falsify">%s</ul>' % items
        if ins['view'] != prev_view:
            prev_view = ins['view']
            prev_theme = None  # 구역이 새로 열렸으니 그 안의 격자도 아직 안 열렸다
            # 이름만으로는 그 칸이 뭘로 이뤄졌는지 모른다. 번호로 순서를 박고 설명을 붙인다.
            # 번호가 있으면 줄바꿈이 일어나도 순서를 잃지 않는다
            notes = NODE_NOTE if ins['view'] == 'stack' else stage_note
            strip = ''.join('<span class="rs"><i class="no">%d</i>%s</span>' % (k + 1, esc(x))
                            for k, x in enumerate(full))
            keys = ''.join(
                '<span class="rl"><i class="no">%d</i><b>%s</b><em>%s</em></span>'
                % (k + 1, esc(x), esc(notes.get(x, '')))
                for k, x in enumerate(full))
            ins_html.append(
                # 뷰마다 제 구역을 갖는다 — 고정된 레일은 그 구역이 끝나면 같이 물러난다.
                # 한 컨테이너에 두 레일을 두면 둘 다 화면 위에 겹친다
                ((('</div></details></section>' if tmore else '</div></section>')
                  if ins_html else ''))
                + '<section class="viewsec">'
                '<p class="viewsep">%s</p>'
                '<details class="rail"><summary>'
                '<span class="rstrip"><span class="rk">%s %d칸</span>%s</span>'
                '<span class="rmore">담는 것</span></summary>'
                # 그림은 레일 밖에 둔다 — 레일은 sticky라, 안에 넣으면 펼치는 순간
                # 그림이 화면 위에 눌러앉는다. 접어 두면 아예 안 보이고
                '<div class="railkey">%s</div></details>%s'
                % (('스택 뷰 — 큰 것에서 작은 것으로'
                    if ins['view'] == 'stack'
                    else '프로세스 뷰 — 결정 순서를 따라 앞 단계에서 뒤 단계로'),
                   '스택' if ins['view'] == 'stack' else '프로세스',
                   len(full), strip, keys,
                   stack_svg(ncount) if ins['view'] == 'stack' else ''))
        # 묶음 머리 — 이름만 두면 또 다른 나열이다. 무엇이 이것들을 한데 묶는지 한 줄로 적는다
        if ins['theme'] != prev_theme:
            lab, lead = next((l, d) for k, l, d in THEMES if k == ins['theme'])
            ins_html.append(
                (('</div>' if not tmore else '</div></details>') if prev_theme is not None else '')
                + '<div class="thead" id="th-%s"><h3>%s<span class="tn">%d건</span></h3>'
                  '<p>%s</p></div><div class="tgrid">'
                % (ins['theme'], esc(lab), tcount[ins['theme']], esc(lead)))
            prev_theme, tseen, tmore = ins['theme'], 0, False
        # 처음 세 건만 깔고 나머지는 「N건 더」 뒤로 — 훑는 길이를 화면 하나로 묶는다
        tseen += 1
        if tseen == FOLD + 1 and tcount[ins['theme']] > FOLD:
            ins_html.append('</div><details class="tmore"><summary>%s 나머지 %d건</summary><div class="tgrid">'
                            % (esc(lab), tcount[ins['theme']] - FOLD))
            tmore = True
        ins_html.append(
            '<details class="ins" id="%s">'
            '<summary><h2>%s</h2><p class="sub">%s</p>%s'
            '<p class="coord"><span class="cid">%s</span>%s'
            '<span class="cnt">원자 %d개%s%s · %s</span></p></summary>'
            '<div class="body"><p class="claimfull">%s</p>%s%s%s</div></details>'
            % (esc(ins['file']),
               esc(ins['headline']), esc(ins['subhead']),
               ('<p class="peek"><span class="pk"><i>그래서</i>%s</span></p>' % esc(payoff_line(ins))) if payoff_line(ins) else '',
               '스택 뷰' if ins['view'] == 'stack' else '프로세스 뷰',
               chips, len(ins['atoms']),
               (' · 무관 %d개' % len(ins['dismissed'])) if ins['dismissed'] else '',
               (' · 검증 %d건' % len(mine)) if mine else '',
               esc(ins['as_of']),
               md_inline(ins['claim']),
               ''.join(secs), vh, ev))
    if ins_html:
        ins_html.append('</div></details></section>' if tmore else '</div></section>')
        ins_html.insert(0, nav_html)

    # 종합 판단 — 문서 여럿을 겹쳐 세운 판단. 인사이트 위에 놓는다
    theses = load_theses()
    tcards = []
    for th in theses:
        one = ''
        m1 = re.search(r'^## 한 줄\n+(.*?)(?=\n## )', th['body'], re.S | re.M)
        if m1:
            one = re.sub(r'\*\*(.+?)\*\*', r'\1', m1.group(1)).strip()
        tickers = []
        # 티커는 「종목 노출」 표에서만 뽑는다 — 다른 표의 약어가 섞이면 칩이 거짓말을 한다
        tsec = re.search(r'^## 종목 노출.*?$(.*?)(?=^## )', th['body'], re.S | re.M)
        for row in re.findall(r'^\|(.+)\|$', tsec.group(1) if tsec else '', re.M):
            cells = [c.strip() for c in row.split('|')]
            if len(cells) < 2:
                continue
            for tk in re.split(r'[,/·]', cells[1]):
                tk = tk.strip()
                if re.fullmatch(r'[A-Z]{2,5}|\d{4}|\d{6}|\d{3}[A-Z]', tk):
                    tickers.append(tk)
        chips = ''.join('<span class="tk">%s</span>' % esc(x) for x in dict.fromkeys(tickers))
        tcards.append(
            '<details class="th"><summary>'
            '<span class="thid">%s</span><h3>%s</h3><p class="thone">%s</p>'
            '<p class="thmeta">문서 %d편 · %s · 원자 %d개 · 신호 %d건 · 다시 볼 날 %s</p>'
            '<p class="thtk">%s</p></summary><div class="thbody">%s</div></details>'
            % (esc(th['id']), esc(th['title']), esc(one), th['docs'], esc(th['span']),
               len(th['atoms']), len(th['lis']), esc(th['review_by']), chips, md_block(th['body'])))
    th_html = ''.join(tcards)

    # 문서가 자기 본문에 갖고 있는 구조 — 전역 좌표가 못 담는 층이다
    STRUCT = os.path.join(ROOT, 'insights', 'views', 'structures.json')
    GROUPS = os.path.join(ROOT, 'insights', 'views', 'structure_groups.json')
    st_html, n_struct, n_group = '', 0, 0
    if os.path.exists(STRUCT):
        sdata = json.load(io.open(STRUCT, encoding='utf-8'))
        gdata = json.load(io.open(GROUPS, encoding='utf-8')) if os.path.exists(GROUPS) else {'groups': []}
        n_struct = sum(len(d['structures']) for d in sdata['docs'])
        n_group = len(gdata['groups'])
        rows = []
        for g in gdata['groups']:
            mem = ''.join('<li>%s <span class="gd">%s</span></li>'
                          % (esc(m['name']), esc(m['source_id'].split(':')[-1][:34]))
                          for m in g['members'])
            flag = ('<span class="gp yes">승격 후보</span>' if g.get('promote')
                    else '<span class="gp no">보류</span>')
            rows.append(
                '<div class="grp"><p class="gh">%s %s <span class="gk">%s · 문서 %d편</span></p>'
                '<p class="gn">%s</p><ul class="gm">%s</ul>'
                '<p class="gn2">%s</p></div>'
                % (esc(g['name']), flag, esc(g['kind']), g.get('docs', len(g['members'])),
                   esc(g['note']), mem, esc(g.get('promote_note', ''))))
        docs = []
        for d in sorted(sdata['docs'], key=lambda x: -len(x['structures'])):
            if not d['structures']:
                docs.append('<li><b>%s</b> — 구조 없음%s</li>'
                            % (esc(d['source_id'].split(':')[-1][:40]),
                               ' · 논증 문서' if d.get('kind_of_doc') == 'argument' else ''))
                continue
            items = ''.join('<li><b>%s</b> <span class="gd">%s</span> %s</li>'
                            % (esc(s['name']), esc(s['kind']),
                               esc(' → '.join(s.get('steps') or s.get('levels'))))
                            for s in d['structures'])
            docs.append('<li><b>%s</b> (%d)<ul class="gm">%s</ul></li>'
                        % (esc(d['source_id'].split(':')[-1][:40]), len(d['structures']), items))
        st_html = (''.join(rows) +
                   '<details class="ev"><summary>문서별 구조 <b>%d개</b> — 묶이지 않은 것 포함</summary>'
                   '<ul class="gm">%s</ul></details>' % (n_struct, ''.join(docs)))

    payload = json.dumps({'atoms': adata, 'insights': [
        {'file': i['file'], 'view': i['view'], 'nodes': i['nodes'], 'stages': i['stages'],
         'atoms': i['atoms'], 'claim': i['claim'], 'as_of': i['as_of']} for i in insights]},
        ensure_ascii=False)

    docs = len({a['doc'] for a in adata})
    # 검증 대장 — 판정 0건이면 적중률을 계산하지 않는다. 없는 비율을 만들면 그게 제일 나쁘다
    allv = vdata.get('checks') or []
    st = {}
    for c in allv:
        st[c['status']] = st.get(c['status'], 0) + 1
    done = st.get('적중', 0) + st.get('빗나감', 0)
    vsum = ''.join('<span>%s <b>%d건</b></span>' % (esc(k), v) for k, v in sorted(st.items()))
    vsum += ('<span>적중률 <b>%.0f%%</b> (판정 %d건)</span>' % (100.0 * st.get('적중', 0) / done, done)
             if done else '<span>판정 <b>0건</b> — 적중률은 아직 계산할 수 없다</span>')
    hmap = {i['file']: i['headline'] for i in insights}
    vrows = ''.join(
        '<div class="vrow"><span class="vst %s">%s</span>'
        '<span class="vq">%s</span><span class="vm">기한 %s</span>'
        '<span class="vsrc">%s 기록 · <a href="#%s">%s</a></span></div>'
        % (STCLS.get(c['status'], ''), esc(c['status']), esc(c['question']), esc(c['due']),
           esc(c['opened_on']), esc(c['insight']), esc(hmap.get(c['insight'], c['insight'])))
        for c in sorted(allv, key=lambda x: (x['due'], x['id'])))

    html = (TMPL
            .replace('__CSS__', style.BASE)
            .replace('__VNOTE__', esc(vdata.get('note') or ''))
            .replace('__VSUM__', vsum)
            .replace('__VROWS__', vrows)
            .replace('__CHAIN__', chain_html)
            .replace('__BAND__', band_html)
            .replace('__INSIGHTS__', ''.join(ins_html))
            .replace('__THESES__', th_html)
            .replace('__NT__', str(len(theses)))
            .replace('__STRUCT__', st_html)
            .replace('__NS__', str(n_struct))
            .replace('__NG__', str(n_group))
            .replace('__DATA__', payload)
            .replace('__NA__', str(len(adata)))
            .replace('__ND__', str(docs))
            .replace('__NI__', str(len(insights)))
            .replace('__NU__', str(len(unassigned)))
            .replace('__EMPTY__', ', '.join(n for n in STACK if not ncount.get(n)) or '없음'))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: 원자 %d개 / 문서 %d편 / 인사이트 %d건 -> %s' % (len(adata), docs, len(insights), OUT))


TMPL = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>인사이트와 그 근거</title>
<style>__CSS__

  .chain .row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;position:relative}
  .band{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px}
  .cell{text-align:left;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);
        padding:13px 14px;cursor:pointer;font:inherit;color:inherit;display:block;box-shadow:var(--shadow);transition:transform .12s,border-color .12s}
  .cell:hover{transform:translateY(-1px);border-color:var(--accent)}
  .cell.empty{border-left-color:var(--line);background:var(--sunk);opacity:.85}
  .cell.on{border-color:var(--accent);background:var(--soft)}
  .cell .ord{display:block;font-size:var(--t-lbl);font-weight:800;color:var(--faint);letter-spacing:.08em}
  .cell .nm{display:block;font-size:var(--t-lead);font-weight:800;letter-spacing:-.01em}
  .cell .ct{display:block;font-size:var(--t-meta);color:var(--faint);font-variant-numeric:tabular-nums;margin-top:2px}
  .cell.empty .ct{color:#b0463f}
  @media (prefers-color-scheme:dark){.cell.empty .ct{color:#e08a8a}}
  .flow{font-size:var(--t-lbl);color:var(--faint);letter-spacing:.04em;margin:6px 0 0}
  .panel{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:var(--pad);margin-top:18px;box-shadow:var(--shadow)}
  .panel .ph{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 4px}
  .panel h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:0 0 10px}
  .hint{font-size:var(--t-body);color:var(--faint);margin:0}
  .lnk{display:block;font-size:var(--t-body);color:var(--ink);text-decoration:none;padding:7px 0;border-bottom:1px solid var(--line)}
  .lnk:last-child{border-bottom:0}
  .lnk b{color:var(--accent2)}
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);padding:var(--pad);margin-top:12px;box-shadow:var(--shadow)}
  /* ── 묶음 ── 19건을 한 줄로 세우면 어디부터 읽을지가 안 보인다. 주제로 묶고,
     접힌 카드는 두 칸씩 깔아 훑게 하고, 펼친 카드만 한 줄을 다 쓴다 */
  .tnav{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 4px}
  .tnav a{display:inline-flex;align-items:center;gap:6px;font-size:var(--t-meta);font-weight:700;
          color:var(--sub);background:var(--card);border:1px solid var(--line);border-radius:999px;
          padding:7px 13px;text-decoration:none;min-height:34px;transition:color .15s,border-color .15s}
  .tnav a:hover{color:var(--accent);border-color:var(--accent)}
  .tnav a b{font-size:var(--t-lbl);font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums}
  .thead{margin:34px 0 2px;scroll-margin-top:56px}
  .thead h3{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:0;display:flex;align-items:baseline;gap:9px}
  .thead .tn{font-size:var(--t-lbl);font-weight:800;color:var(--faint);font-variant-numeric:tabular-nums}
  .thead p{font-size:var(--t-body);color:var(--sub);margin:5px 0 0;max-width:62ch}
  .tgrid{display:grid;grid-template-columns:1fr;gap:12px;margin-top:12px;align-items:start}
  /* 한 묶음에서 처음 세 건만 깔고 나머지는 뒤로 — 목록이 끝없이 이어지면 고르는 일이 못 된다 */
  .tmore{margin-top:12px}
  .tmore>summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:center;
                 gap:7px;min-height:44px;padding:0 16px;border:1px solid var(--line);border-radius:999px;
                 background:var(--card);color:var(--sub);font-size:var(--t-meta);font-weight:750;
                 -webkit-tap-highlight-color:transparent;transition:color .15s,border-color .15s}
  .tmore>summary::-webkit-details-marker{display:none}
  .tmore>summary::after{content:'▾';font-size:10px;color:var(--faint)}
  .tmore[open]>summary{color:var(--accent);border-color:var(--accent)}
  .tmore[open]>summary::after{content:'▴'}
  .tmore>summary:hover{color:var(--accent);border-color:var(--accent)}
  .tgrid>.ins{margin-top:0}
  @media (min-width:820px){
    .tgrid{grid-template-columns:1fr 1fr}
    /* 펼치면 읽는 화면이 된다 — 좁은 칸에 원문 줄을 밀어 넣지 않는다 */
    .tgrid>.ins[open]{grid-column:1/-1}
  }
  /* 접힌 채로도 이 글의 값이 보여야 한다 — 부제는 무엇을 다루나, 이 줄은 그래서 무엇이 달라지나 */
  /* 자르는 상자와 여백을 주는 상자를 나눈다 — 한 상자에 겸하면 잘린 셋째 줄이 아래 여백으로 비친다 */
  .peek{font-size:var(--t-meta);color:var(--sub);margin:9px 0 0;padding:9px 11px;background:var(--sunk);
        border-radius:8px;overflow:hidden}
  .peek .pk{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .peek i{font-style:normal;font-size:var(--t-lbl);font-weight:800;color:var(--accent);letter-spacing:.06em;margin-right:7px}
  .ins[open] .peek{display:none}
  .viewsep{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;
            color:var(--accent);margin:30px 0 8px;padding-top:14px;border-top:1px solid var(--line)}
  /* 근거 지도는 읽는 화면이 아니라 검토 화면이다 — 기본은 접어 두고 필요할 때 편다 */
  .mapsec{margin:34px 0 0;border-top:1px solid var(--line);padding-top:16px}
  .mapsec>summary{cursor:pointer;list-style:none;display:flex;align-items:baseline;flex-wrap:wrap;gap:6px 10px;
                  padding:6px 0;min-height:40px;-webkit-tap-highlight-color:transparent}
  .mapsec>summary::-webkit-details-marker{display:none}
  .mapsec>summary .mh{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em}
  .mapsec>summary .mn{font-size:var(--t-meta);color:var(--faint);font-variant-numeric:tabular-nums}
  .mapsec>summary::after{content:'▾';margin-left:auto;color:var(--faint);font-size:11px}
  .mapsec[open]>summary::after{content:'▴'}
  /* 종합 판단 — 이 페이지의 주인. 인사이트 카드보다 무겁게 둔다 */
  .thsec{font-size:var(--t-h1);font-weight:880;letter-spacing:-.025em;margin:34px 0 6px}
  .thnote{font-size:var(--t-meta);color:var(--faint);margin:0 0 14px;max-width:66ch;line-height:1.6}
  .th{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent2);
      border-radius:var(--r);padding:var(--pad);margin-bottom:12px;box-shadow:var(--shadow)}
  .th>summary{cursor:pointer;list-style:none;-webkit-tap-highlight-color:transparent}
  .th>summary::-webkit-details-marker{display:none}
  .thid{font-size:var(--t-lbl);font-weight:850;letter-spacing:.08em;color:var(--accent2)}
  .th h3{font-size:var(--t-h2);font-weight:860;letter-spacing:-.02em;line-height:1.34;margin:4px 0 6px}
  .thone{font-size:var(--t-body);color:var(--sub);line-height:1.62;margin:0 0 8px}
  .thmeta{font-size:var(--t-meta);color:var(--faint);margin:0;font-variant-numeric:tabular-nums}
  .thtk{display:flex;flex-wrap:wrap;gap:5px;margin:9px 0 0}
  .tk{font-size:var(--t-lbl);font-weight:800;color:var(--accent);background:var(--soft);
      border-radius:5px;padding:3px 7px;font-variant-numeric:tabular-nums}
  .th[open]>summary{border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:4px}
  .thbody{font-size:var(--t-body);line-height:1.72}
  .thbody h4{font-size:var(--t-lead);font-weight:820;margin:18px 0 6px;letter-spacing:-.01em}
  .thbody p{margin:8px 0}
  .thbody ul{margin:6px 0;padding-left:18px}
  .thbody li{margin:5px 0}
  .thbody .tw{overflow-x:auto;margin:10px 0}
  .thbody table{border-collapse:collapse;width:100%;font-size:var(--t-meta)}
  .thbody th{text-align:left;font-weight:800;color:var(--sub);border-bottom:1px solid var(--line);padding:7px 9px;white-space:nowrap}
  .thbody td{border-bottom:1px solid var(--line);padding:7px 9px;vertical-align:top}
  .hintbox{margin:20px 0 4px;font-size:var(--t-meta);color:var(--faint)}
  .hintbox>summary{cursor:pointer;list-style:none;display:inline-flex;align-items:center;gap:6px;
                   font-weight:750;color:var(--sub);padding:6px 0;min-height:32px}
  .hintbox>summary::-webkit-details-marker{display:none}
  .hintbox>summary::after{content:'▾';font-size:10px;color:var(--faint)}
  .hintbox[open]>summary::after{content:'▴'}
  .hintbox>p{margin:2px 0 0;padding-left:12px;border-left:2px solid var(--line);line-height:1.6}
  .ins>summary:hover h2{color:var(--accent)}
  .ins:not([open])>summary{padding-bottom:0}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:26px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;color:var(--faint);transition:transform .2s}
  .ins[open]>summary::after{transform:rotate(180deg)}
  /* 뷰 이름은 헤드라인을 가릴 만큼 크면 안 된다 — 좌표 줄 맨 앞의 작은 표식으로 둔다 */
  .cid{font-size:var(--t-lbl);font-weight:800;letter-spacing:.06em;color:var(--faint);
       border:1px solid var(--line);border-radius:5px;padding:2px 6px;flex:0 0 auto}
  .ins h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;line-height:1.36;margin:0 0 2px}
  /* apple-design: 응답은 누르는 순간(포인터 다운), 열림은 임계감쇠(damping 1.0·response 0.35s).
     제스처가 아니라 클릭이라 오버슈트를 넣지 않는다. transform·opacity만 움직여 합성기에 맡긴다 */
  .ins>summary{-webkit-tap-highlight-color:transparent}
  .ins>summary:active{transform:scale(.994);transition:transform 100ms ease-out}
  .ins>summary::after{transition:transform .35s cubic-bezier(.32,.72,0,1)}
  .ins[open]>.body{animation:reveal .35s cubic-bezier(.32,.72,0,1) both}
  .ev[open]>.atom:first-of-type,.ev[open]>div:first-of-type{animation:reveal .3s cubic-bezier(.32,.72,0,1) both}
  @keyframes reveal{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
  .axmini i{transition:background-color .2s ease}
  .cell,.ins,.grp{will-change:auto}
  @media (prefers-reduced-motion:reduce){
    .ins[open]>.body,.ev[open]>.atom:first-of-type,.ev[open]>div:first-of-type{animation:fadein .18s ease both}
    .ins>summary:active{transform:none}
    .cell:hover{transform:none}
    .uc-links a:active{transform:none}
    @keyframes fadein{from{opacity:0}to{opacity:1}}
  }
  @media (prefers-contrast:more){
    .axmini i{outline:1px solid var(--accent2)}
    .ins,.grp,.panel{border:1px solid var(--ink)}
  }
  .claimfull{font-size:var(--t-lead);line-height:1.62;color:var(--ink);margin:0 0 4px;
              padding:11px 14px;background:var(--sunk);border-radius:8px}
  /* 축은 글 위 레일에 한 번. 카드는 그 축 위 자기 자리만 — 같은 축의 글끼리 겹쳐 보인다 */
  /* 축은 스크롤해도 화면에 남는다 — 카드의 막대가 무엇 위에 그려졌는지 계속 보여야 한다.
     이름 줄은 항상 붙어 있고, 각 칸이 뭘 담는지는 눌러서 접었다 편다(JS 없이 details로).
     apple-design: 떠 있는 층은 반투명·블러 */
  .rail{position:sticky;top:0;z-index:6;margin:0 0 12px;border-radius:var(--r);
        border:1px solid var(--line);background:color-mix(in srgb,var(--sunk) 90%,transparent);
        backdrop-filter:blur(14px) saturate(150%)}
  .rail>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;
                padding:0 11px 0 13px;position:relative;min-height:42px;
                -webkit-tap-highlight-color:transparent}
  /* 축은 언제나 한 줄이다 — 고정된 줄이 두세 줄이면 화면을 먹는다. 넘치면 옆으로 민다 */
  .rstrip{display:flex;align-items:center;gap:4px 5px;flex:1 1 auto;min-width:0;
          overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;
          padding:10px 0;mask-image:linear-gradient(90deg,#000 calc(100% - 18px),transparent)}
  .rstrip::-webkit-scrollbar{display:none}
  .rail>summary:active{background:color-mix(in srgb,var(--line) 35%,transparent)}
  .rail>summary::-webkit-details-marker{display:none}
  .rail .rmore{margin-left:auto;font-size:var(--t-lbl);font-weight:800;color:var(--accent);white-space:nowrap}
  .rail .rmore::after{content:" ⌄";display:inline-block;transition:transform .3s cubic-bezier(.32,.72,0,1)}
  .rail[open] .rmore::after{transform:rotate(180deg)}
  .rail .rk{font-size:var(--t-lbl);font-weight:800;letter-spacing:.08em;color:var(--accent);
            text-transform:uppercase;margin-right:2px;flex:0 0 auto;white-space:nowrap}
  .rail .rs{display:inline-flex;align-items:center;gap:3px;font-size:var(--t-lbl);
            font-weight:750;color:var(--ink);white-space:nowrap;flex:0 0 auto}
  .railkey{display:grid;gap:7px 10px;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));
           padding:2px 13px 11px;border-top:1px solid var(--line);margin-top:-1px;padding-top:11px}
  .rail .rl{display:grid;grid-template-columns:auto 1fr;gap:0 6px;align-items:baseline;min-width:0}
  .rail .no{align-self:center;display:flex;align-items:center;justify-content:center;
            width:15px;height:15px;border-radius:50%;background:var(--card);border:1px solid var(--line);
            font-size:9.5px;font-weight:800;color:var(--faint);font-style:normal;flex:0 0 auto}
  /* 계층 그림 — 열 칸이 목록이 아니라 포함 관계라는 것을 글 읽기 전에 한 번 보여 준다 */
  .stkfig{margin:0 0 18px;padding:14px 16px 12px;background:var(--card);
          border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
  .stkfig svg{display:block;width:100%;height:auto}
  .stkfig figcaption{font-size:var(--t-meta);color:var(--faint);line-height:1.55;
                     margin-top:10px;max-width:70ch}
  .stkfig figcaption b{color:var(--sub)}
  @media (max-width:640px){.stkfig{padding:11px 12px 10px;margin-bottom:14px}}
  .railkey .no{width:16px;height:16px;font-size:10px}
  .railkey .no{grid-row:1/3}
  .rail b{font-size:var(--t-meta);font-weight:800;color:var(--ink);letter-spacing:-.01em;
          overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .rail em{font-size:var(--t-lbl);font-style:normal;color:var(--faint);line-height:1.45}
  .rail[open]>.railkey{animation:reveal .3s cubic-bezier(.32,.72,0,1) both}
  @media (prefers-reduced-transparency:reduce){.rail{background:var(--sunk);backdrop-filter:none}}
  @media (max-width:820px){
    .rstrip{-webkit-mask-image:linear-gradient(to right,#000 calc(100% - 26px),transparent);
            mask-image:linear-gradient(to right,#000 calc(100% - 26px),transparent)}
  }
  /* 좌표·개수는 판단을 받치는 값이라 헤드라인 아래로 내린다 — 위에 쌓이면 제목이 넷째 줄이 된다 */
  .coord{display:flex;flex-wrap:wrap;align-items:center;gap:5px 8px;margin:10px 0 0;
         padding-top:9px;border-top:1px solid var(--line)}
  .axmini{display:inline-flex;align-items:center;gap:2px;flex:0 0 auto}
  .axmini i{display:block;width:9px;height:3px;border-radius:2px;background:var(--line)}
  .axmini i.on{background:var(--accent)}
  .cspan{font-size:var(--t-meta);font-weight:750;color:var(--accent2);letter-spacing:-.01em}
  .coord .cnt{font-size:var(--t-meta);color:var(--faint);margin-left:auto;font-variant-numeric:tabular-nums}
  /* 두 칸으로 깔리면 카드 폭이 좁아진다 — 개수는 제 줄을 갖는다. 카드마다 줄이 다르게 접히면
     같은 줄에 있어야 할 것들이 어긋나 보인다 */
  @media (min-width:820px){.tgrid .coord .cnt{flex:1 0 100%;margin-left:0}}
  .ins .sub{font-size:var(--t-body);color:var(--faint);margin:3px 0 0;line-height:1.5;
            display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .ins[open] .sub{-webkit-line-clamp:unset;overflow:visible}
  .body h4{font-size:var(--t-meta);font-weight:800;color:var(--accent2);margin:14px 0 5px;text-transform:uppercase;letter-spacing:.04em}
  .grp{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);padding:var(--pad);margin-bottom:10px;box-shadow:var(--shadow)}
  .gh{font-size:var(--t-lead);font-weight:800;margin:0 0 4px;letter-spacing:-.01em}
  .gk{font-size:var(--t-meta);font-weight:700;color:var(--faint);margin-left:6px}
  .gp{font-size:var(--t-lbl);font-weight:800;padding:2px 8px;border-radius:999px;margin-left:6px}
  .gp.yes{background:#e8f6ec;color:#1d6e45}
  .gp.no{background:var(--sunk);color:var(--faint)}
  @media (prefers-color-scheme:dark){.gp.yes{background:#173323;color:#63c08c}}
  .gn{font-size:var(--t-body);color:var(--sub);margin:0 0 7px;line-height:1.55}
  .gn2{font-size:var(--t-meta);color:var(--faint);margin:7px 0 0;line-height:1.5}
  .gm{margin:0;padding-left:16px;list-style:none}
  .gm li{font-size:var(--t-body);color:var(--sub);line-height:1.55;margin-bottom:3px;position:relative}
  .gm li::before{content:"";position:absolute;left:-12px;top:9px;width:6px;height:1.5px;background:var(--accent)}
  .gm li b{color:var(--ink)}
  .gd{font-size:var(--t-lbl);color:var(--faint)}
  .body h4.payoff{color:var(--accent);margin-top:4px}
  .body ul.payoff{background:var(--soft);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;
                  margin:0 0 14px;padding:11px 16px 11px 30px}
  .body ul.payoff li{color:var(--ink);font-size:var(--t-body)}
  .body ul{margin:0 0 6px;padding-left:17px}
  .body li{font-size:var(--t-body);color:var(--sub);line-height:1.58;margin-bottom:4px}
  .body b{color:var(--ink)}

  /* 무엇으로 무너지나 — 판단 옆에 반증 조건을 둔다. 지금은 전부 열림이라 적중률이 없다 */
  .body h4.falsify{color:var(--accent2);margin-top:14px}
  .body ul.falsify{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:8px}
  .body ul.falsify li{background:var(--sunk);border-radius:10px;padding:10px 13px;
                      font-size:var(--t-body);color:var(--sub);line-height:1.55;margin:0}
  .body ul.falsify li b{color:var(--ink)}
  .vst{font-size:var(--t-lbl);font-weight:800;padding:2px 8px;border-radius:999px;margin-left:6px;
       white-space:nowrap;background:var(--sunk);color:var(--faint);border:1px solid var(--line)}
  .vst.open{background:var(--soft);color:var(--accent2);border-color:transparent}
  .vst.hit{background:#e8f6ec;color:#1d6e45;border-color:transparent}
  .vst.miss{background:#fbe9e7;color:#a3372f;border-color:transparent}
  @media (prefers-color-scheme:dark){.vst.hit{background:#173323;color:#63c08c}.vst.miss{background:#331a17;color:#e08a8a}}
  .vw{font-size:var(--t-lbl);font-weight:800;color:var(--faint);letter-spacing:.04em}
  .vm{font-size:var(--t-lbl);color:var(--faint);font-variant-numeric:tabular-nums}
  .vrow{display:grid;grid-template-columns:auto 1fr auto;gap:4px 10px;align-items:baseline;
        padding:11px 0;border-top:1px solid var(--line)}
  .vrow:first-of-type{border-top:0}
  .vrow .vq{font-size:var(--t-body);color:var(--ink);min-width:0}
  .vrow .vsrc{grid-column:2/4;font-size:var(--t-lbl);color:var(--faint)}
  .vrow .vsrc a{color:var(--accent);text-decoration:none}
  .vsum{display:flex;flex-wrap:wrap;gap:6px 14px;margin:0 0 12px;font-size:var(--t-meta);color:var(--faint)}
  .vsum b{color:var(--ink)}
  /* ── 모바일 — 값이 아니라 토큰만 바꾼다. 규칙을 두 벌 두면 반드시 어긋난다 ── */
  @media (max-width:640px){
    .ins>summary{padding:6px 30px 6px 0;min-height:44px}       /* 손가락 타깃 */
    .ins>summary::after{right:0;top:2px;font-size:24px}
    .ins h2{line-height:1.38}
    .coord .cnt{margin-left:0}
    .chain .row{grid-template-columns:1fr;gap:8px;margin-bottom:8px}
    .band{grid-template-columns:1fr 1fr;gap:8px}
    .cell{min-height:56px}
    .rail>summary{padding:0 9px 0 11px}
    .claimfull{padding:10px 12px}
  }
  @media (max-width:380px){
    .band{grid-template-columns:1fr}
    .railkey{grid-template-columns:1fr 1fr;padding-left:11px;padding-right:11px}
  }

</style>
<div class="wrap">
<header>
  <p class="eyebrow">Insights &amp; Evidence</p>
  <h1>인사이트와 그 근거</h1>
  <p class="lede">판단이 주인이고 원자는 그 밑을 받치는 근거입니다. 카드를 펼치면
     인용 원자가 <b>문서 원문의 그 줄</b>과 함께 나옵니다.</p>
  <div class="meta">
    <span>인사이트 __NI__건</span><span>원자 __NA__개</span><span>문서 __ND__편</span>
    <span>미배정 __NU__개</span><span>구조 __NS__개 · 묶음 __NG__</span><span>빈 노드: __EMPTY__</span>
    <a class="maplink" href="제약과 회사.html">제약과 회사 →</a>
  </div>
</header>

<h2 class="thsec">종합 판단 __NT__건 — 문서 여럿을 겹쳐 세운 것</h2>
<p class="thnote">한 문서로는 안 나오는 결론만 여기 둡니다. 각 판단은 근거 문서 3편 이상,
   한 문서가 근거의 절반을 넘지 않고, 시간표와 폐기 조건을 갖습니다. 가격·밸류에이션은 없습니다 —
   제약이 매출에 닿는 경로이지 매수·매도 판단이 아닙니다.</p>
__THESES__

<h2 class="thsec">근거가 되는 판단 __NI__건 — 좌표 한 칸씩</h2>
<details class="hintbox"><summary>이 페이지 읽는 법</summary>
<p>글은 <b>주제 6묶음</b>으로 나뉘어 있습니다. 접힌 카드에도 「그래서 무엇이 달라지나」 첫 줄이 붙어 있어 열지 않고 고를 수 있고, 카드를 누르면 근거·조건 충돌·미지까지 펼쳐집니다. 「근거 원자」를 한 번 더 누르면 인용 원자가 <b>문서 원문의 그 줄</b>과 함께 나옵니다.</p></details>
__INSIGHTS__

<details class="mapsec"><summary><span class="mh">근거 지도 — 어디에 근거가 있고 어디가 비었나</span><span class="mn">원자 __NA__개 · 검토용</span></summary>
<p class="axnote">원자는 두 축의 좌표에 매달립니다. 아래는 인사이트를 읽는 화면이 아니라 <b>근거의 분포를 보는 화면</b>입니다 —
   어느 칸이 두텁고 어느 칸이 비었는지, 그리고 각 원자가 제 칸에 제대로 들어갔는지를 봅니다.</p>

<h4 class="sub2">스택 — 큰 것에서 작은 것으로 (아래가 상류)</h4>
__CHAIN__
<p class="flow">연료·지정학 → 전력망 → 데이터센터 → 랙 → 열 / HBM · 일반 D램 · 낸드·스토리지 → 칩 → 전자·공정</p>

<h4 class="sub2">프로세스 — 결정 순서 (어느 결정이 먼저 고정되나)</h4>
__BAND__

<h3 class="sec">문서가 가진 구조 — 좌표가 못 담는 층</h3>
<p class="axnote">전역 좌표(스택 8노드·프로세스 7단계)는 문서 고유의 계층·순서를 담지 못해 한 칸으로 접힌다.
   그래서 문서마다 있는 그대로 기록하고, <b>2편 이상이 같은 것을 말할 때만</b> 좌표 승격 후보로 올린다.
   라벨만으로는 하나도 안 겹쳤다(겹침 0쌍) — 리포트마다 자기 어휘로 틀을 만들기 때문이다.</p>
__STRUCT__

<div class="panel" id="panel">
  <p class="ph">선택한 칸</p>
  <h2 id="ptitle">칸을 누르세요</h2>
  <p class="hint">스택 노드 또는 프로세스 단계를 누르면 그 칸의 원자와, 그 칸을 근거로 쓴 인사이트가 나옵니다.
     원자가 0인 칸은 감추지 않았습니다 — 사슬이 어디서 끊겼는지가 그 자체로 정보입니다.</p>
</div>

</details>

<h3 class="sec">검증 대장 — 무엇이 확인되면 판단이 바뀌나</h3>
<p class="axnote">__VNOTE__</p>
<div class="vsum">__VSUM__</div>
<div class="panel">__VROWS__</div>

<footer>insights/ 산출물 — atoms(원자)·synth(인사이트)·views/process.json(단계 배정)에서 <code>gen_atomview.py</code>로 생성.
검사기 <code>check_atoms.py</code>가 줄 번호·수치·원문 hash·원문 병치를 대조합니다. 주장의 진위는 기계가 판정하지 않습니다 — 원문을 옆에 두는 것이 그 대비입니다.</footer>
</div>
<script>
const D = __DATA__;
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function render(axis, key){
  document.querySelectorAll('.cell').forEach(function(b){
    b.classList.toggle('on', b.dataset.axis===axis && b.dataset.key===key);
  });
  const as = D.atoms.filter(function(a){return axis==='stack' ? a.stack===key : a.stage===key;});
  const ins = D.insights.filter(function(i){
    return axis==='stack' ? (i.view==='stack' && i.nodes.indexOf(key)>=0)
                          : (i.view==='process' && i.stages.indexOf(key)>=0);
  });
  let h = '<p class="ph">'+(axis==='stack'?'스택 노드':'프로세스 단계')+'</p><h2>'+esc(key)+'</h2>';
  if(!as.length){
    h += '<p class="hint">이 칸에는 원자가 없습니다. 근거가 없으므로 이 칸을 쓰는 인사이트도 쓸 수 없습니다.</p>';
  } else {
    h += '<p class="hint">원자 '+as.length+'개 · 이 칸을 쓰는 인사이트 '+ins.length+'건</p>';
    if(ins.length){
      h += '<div style="margin:10px 0 4px">';
      ins.forEach(function(i){
        h += '<a class="lnk" href="#'+esc(i.file)+'"><b>'+esc(i.claim.slice(0,90))+'</b><br><span style="color:var(--faint);font-size:11.5px">'+esc(i.file)+' · as_of '+esc(i.as_of)+'</span></a>';
      });
      h += '</div>';
    }
    as.forEach(function(a){
      h += '<div class="atom"><span class="aid">'+esc(a.id)+'</span>'
        + (axis==='stack' && a.stage ? '<span class="atag">'+esc(a.stage)+'</span>' : '')
        + (axis==='process' ? '<span class="atag">'+esc(a.stack)+'</span>' : '')
        + '<span class="atag">'+esc(a.corpus)+'</span>'
        + '<p class="aclaim">'+esc(a.claim)+'</p>';
      if(a.value) h += '<p class="kv"><span>값</span> '+esc(a.value)+'</p>';
      h += '<p class="kv"><span>조건</span> '+esc(a.cond)+'</p>';
      h += '<p class="kv"><span>귀속</span> '+esc(a.attr)+' · <span>출처</span> '+esc(a.doc)+' '+esc(a.line)+'행 · '+esc(a.time)+'</p>';
      h += '<div class="src">'+esc(a.text)+'</div></div>';
    });
  }
  document.getElementById('panel').innerHTML = h;
  document.getElementById('panel').scrollIntoView({behavior:'smooth', block:'nearest'});
}
document.querySelectorAll('.cell').forEach(function(b){
  b.addEventListener('click', function(){ render(b.dataset.axis, b.dataset.key); });
});
</script>
'''

if __name__ == '__main__':
    build()
