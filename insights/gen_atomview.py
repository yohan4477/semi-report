# 인사이트와 근거 페이지 생성 — atoms + synth + views/process.json → 자기완결 HTML
# 판단이 주인이고 원자는 근거다. 인사이트를 먼저 놓고 각 인사이트 안에서 인용 원자를
# line_text(원문 그 줄)와 함께 펼친다. 두 축 다이어그램은 그 아래 "근거 지도"로 —
# 어느 칸이 두텁고 어디가 비었나, 각 원자가 제 칸에 들어갔나를 보는 검토면이다.
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca

ROOT = ca.ROOT
OUT = os.path.join(ROOT, '대시보드', '인사이트와 근거.html')

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
    '메모리': 'HBM·DRAM·NAND, 대역폭, 캐파 배분',
    '칩': '다이 구성, 패키징(CoWoS·EMIB), 본딩, 연산 성능',
    '전자·공정': '노드 세대, 가동률, 수율, CFET',
}


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


def build():
    atoms = ca.load_atoms()
    pr = json.load(io.open(ca.PROCESS, encoding='utf-8'))
    stages, assign = pr['stages'], pr.get('assign') or {}
    # 단계 설명은 process.json이 정본이다. 첫 문장만 잘라 레일에 싣는다
    stage_note = {k: v.split('. ')[0].rstrip('.')
                  for k, v in (pr.get('stage_note') or {}).items()}
    man = {s['id']: s for s in json.load(io.open(ca.MAN, encoding='utf-8'))['sources']}
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
    insights.sort(key=ins_rank)

    ins_html = []
    prev_view = None
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
        chips = ('<span class="axmini" aria-hidden="true">%s</span>'
                 '<span class="cspan">%s</span>' % (bar, esc(label)))
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
        if ins['view'] != prev_view:
            prev_view = ins['view']
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
                ('</section>' if ins_html else '')
                + '<section class="viewsec">'
                '<p class="viewsep">%s</p>'
                '<details class="rail"><summary>'
                '<span class="rstrip"><span class="rk">%s %d칸</span>%s</span>'
                '<span class="rmore">담는 것</span></summary>'
                '<div class="railkey">%s</div></details>'
                % (('스택 뷰 — 큰 것에서 작은 것으로'
                    if ins['view'] == 'stack'
                    else '프로세스 뷰 — 결정 순서를 따라 앞 단계에서 뒤 단계로'),
                   '스택' if ins['view'] == 'stack' else '프로세스',
                   len(full), strip, keys))
        ins_html.append(
            '<details class="ins" id="%s">'
            '<summary><span class="cid">%s</span><span class="asof">as_of %s</span>'
            '<p class="coord">%s<span class="cnt">원자 %d개%s</span></p><h2>%s</h2><p class="sub">%s</p></summary>'
            '<div class="body"><p class="claimfull">%s</p>%s%s</div></details>'
            % (esc(ins['file']),
               '스택 뷰' if ins['view'] == 'stack' else '프로세스 뷰',
               esc(ins['as_of']), chips, len(ins['atoms']),
               (' · 무관 %d개' % len(ins['dismissed'])) if ins['dismissed'] else '',
               esc(ins['headline']), esc(ins['subhead']),
               md_inline(ins['claim']),
               ''.join(secs), ev))
    if ins_html:
        ins_html.append('</section>')

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
    html = (TMPL
            .replace('__CHAIN__', chain_html)
            .replace('__BAND__', band_html)
            .replace('__INSIGHTS__', ''.join(ins_html))
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
<style>
  :root{--bg:#f7f8fa;--card:#fff;--ink:#1a2233;--sub:#5b6577;--faint:#8892a3;--line:#e3e7ee;--accent:#2563eb;--accent2:#1e40af;--soft:#eaf1fe;--sunk:#eef1f5;--shadow:0 1px 2px rgba(26,34,51,.05);
        /* 글자·간격은 여기서만 정한다. 모바일은 이 값만 바꾼다 — 규칙을 두 벌 두면 어긋난다 */
        --t-lbl:10.5px;--t-meta:12px;--t-body:13.5px;--t-lead:14.5px;--t-h2:19px;
        --r:12px;--pad:16px 20px;--gap:12px}
  @media (prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#7e8798;--line:#2a3140;--accent:#7aa5f8;--accent2:#9ab8fa;--soft:#1e2a44;--sunk:#242b38;--shadow:none}}
  *{box-sizing:border-box}
  html{font-size:100%}
  body{font-size:1rem;background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.64;margin:0;padding:0 20px 80px}
  .wrap{max-width:900px;margin:0 auto}
  header{padding:52px 0 6px}
  .eyebrow{font-size:var(--t-meta);font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
  h1{font-size:clamp(28px,6vw,44px);font-weight:850;letter-spacing:-.035em;margin:0}
  h1::after{content:"";display:block;width:52px;height:3px;background:var(--accent);margin-top:14px;border-radius:2px}
  .lede{color:var(--sub);font-size:var(--t-lead);margin:16px 0 0;max-width:64ch}
  .meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:var(--t-meta);color:var(--faint)}
  h3.sec{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:48px 0 4px;padding-top:24px;border-top:1px solid var(--line)}
  h4.sub2{font-size:var(--t-body);font-weight:800;color:var(--sub);margin:22px 0 8px}
  .ev{border:1px solid var(--line);border-radius:var(--r);background:var(--sunk);margin:14px 0 0}
  .ev>summary{cursor:pointer;padding:10px 13px;font-size:var(--t-meta);color:var(--sub);list-style:none}
  .ev>summary::-webkit-details-marker{display:none}
  .ev>summary::before{content:"▸ ";color:var(--faint)}
  .ev[open]>summary::before{content:"▾ "}
  .ev>summary b{color:var(--ink)}
  .ev .atom{padding:11px 13px;border-top:1px solid var(--line)}
  .axnote{font-size:var(--t-body);color:var(--sub);margin:0 0 14px;max-width:64ch}
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
  .atom{border-top:1px solid var(--line);padding:11px 0}
  .atom:first-of-type{border-top:0}
  .aid{font-size:var(--t-lbl);font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums}
  .atag{font-size:var(--t-lbl);font-weight:800;padding:1px 7px;border-radius:999px;margin-left:6px;background:var(--sunk);color:var(--faint)}
  .aclaim{font-size:var(--t-body);color:var(--ink);margin:3px 0 4px}
  .kv{font-size:var(--t-meta);color:var(--sub);margin:0 0 3px}
  .kv span{color:var(--faint)}
  .src{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:var(--t-meta);color:var(--sub);background:var(--sunk);
       border-left:2px solid var(--line);border-radius:0 6px 6px 0;padding:7px 9px;margin:5px 0 0;white-space:pre-wrap;word-break:break-word}
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:var(--r);padding:var(--pad);margin-top:12px;box-shadow:var(--shadow)}
  .viewsep{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;text-transform:uppercase;
            color:var(--accent);margin:30px 0 8px;padding-top:14px;border-top:1px solid var(--line)}
  .hintline{font-size:var(--t-meta);color:var(--faint);margin:26px 0 10px;padding-left:12px;border-left:2px solid var(--line)}
  .ins>summary:hover h2{color:var(--accent)}
  .ins:not([open])>summary{padding-bottom:0}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:26px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;color:var(--faint);transition:transform .2s}
  .ins[open]>summary::after{transform:rotate(180deg)}
  .cid{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;color:var(--accent)}
  .asof{float:right;font-size:var(--t-meta);color:var(--faint);font-variant-numeric:tabular-nums}
  .ins h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;line-height:1.36;margin:8px 0 2px}
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
  .railkey .no{width:16px;height:16px;font-size:10px}
  .railkey .no{grid-row:1/3}
  .rail b{font-size:var(--t-meta);font-weight:800;color:var(--ink);letter-spacing:-.01em;
          overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .rail em{font-size:var(--t-lbl);font-style:normal;color:var(--faint);line-height:1.45}
  .rail[open]>.railkey{animation:reveal .3s cubic-bezier(.32,.72,0,1) both}
  @media (prefers-reduced-transparency:reduce){.rail{background:var(--sunk);backdrop-filter:none}}
  .coord{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin:7px 0 0}
  .axmini{display:inline-flex;align-items:center;gap:2px;flex:0 0 auto}
  .axmini i{display:block;width:9px;height:3px;border-radius:2px;background:var(--line)}
  .axmini i.on{background:var(--accent)}
  .cspan{font-size:var(--t-meta);font-weight:750;color:var(--accent2);letter-spacing:-.01em}
  .coord .cnt{font-size:var(--t-meta);color:var(--faint);margin-left:auto;font-variant-numeric:tabular-nums}
  .ins .sub{font-size:var(--t-body);color:var(--faint);margin:3px 0 0;line-height:1.5}
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
  code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;background:var(--sunk);padding:1px 4px;border-radius:4px}

  footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);font-size:var(--t-meta);color:var(--faint)}
  /* ── 모바일 — 값이 아니라 토큰만 바꾼다. 규칙을 두 벌 두면 반드시 어긋난다 ── */
  @media (max-width:640px){
    :root{--t-lbl:11.5px;--t-meta:12.5px;--t-body:14px;--t-lead:14.5px;--t-h2:17.5px;--pad:16px 15px}
    body{padding:0 14px 64px;line-height:1.66}
    .wrap{max-width:100%}
    header{padding:34px 0 4px}
    h1{font-size:clamp(26px,7.5vw,34px);letter-spacing:-.03em}
    .meta{gap:5px 14px}
    .ins>summary{padding:6px 30px 6px 0;min-height:44px}       /* 손가락 타깃 */
    .ins>summary::after{right:0;top:2px;font-size:24px}
    .ins h2{line-height:1.38}
    .coord .cnt{margin-left:0}
    .ev>summary,.ev .atom{padding:13px 14px;min-height:44px}
    .chain .row{grid-template-columns:1fr;gap:8px;margin-bottom:8px}
    .band{grid-template-columns:1fr 1fr;gap:8px}
    .cell{min-height:56px}
    .rail>summary{padding:0 9px 0 11px}
    .claimfull{padding:10px 12px}
    .atag{padding:2px 8px}
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
  <p class="lede">판단이 주인이고, 원자는 그 밑을 받치는 근거입니다. 각 인사이트의 「근거 원자」를 펼치면
     인용한 원자가 <b>문서 원문의 그 줄</b>과 함께 나옵니다 — 주장이 원문과 어긋나는지 여기서 바로 확인됩니다.</p>
  <div class="meta">
    <span>인사이트 __NI__건</span><span>원자 __NA__개</span><span>문서 __ND__편</span>
    <span>미배정 __NU__개</span><span>구조 __NS__개 · 묶음 __NG__</span><span>빈 노드: __EMPTY__</span>
  </div>
</header>

<p class="hintline">카드를 누르면 그 판단의 <b>그래서 무엇이 달라지나</b>부터 근거·조건 충돌·미지까지 펼쳐집니다. 「근거 원자」를 한 번 더 누르면 인용 원자가 <b>문서 원문의 그 줄</b>과 함께 나옵니다.</p>
__INSIGHTS__

<h3 class="sec">근거 지도 — 어디에 근거가 있고 어디가 비었나</h3>
<p class="axnote">원자는 두 축의 좌표에 매달립니다. 아래는 인사이트를 읽는 화면이 아니라 <b>근거의 분포를 보는 화면</b>입니다 —
   어느 칸이 두텁고 어느 칸이 비었는지, 그리고 각 원자가 제 칸에 제대로 들어갔는지를 봅니다.</p>

<h4 class="sub2">스택 — 큰 것에서 작은 것으로 (아래가 상류)</h4>
__CHAIN__
<p class="flow">연료·지정학 → 전력망 → 데이터센터 → 랙 → 열 / 메모리 → 칩 → 전자·공정</p>

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
