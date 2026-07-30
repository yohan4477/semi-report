# 원자 뷰 페이지 생성 — atoms + synth + views/process.json → 자기완결 HTML
# 스택 8노드와 프로세스 7단계를 한 화면에 두고, 칸을 누르면 그 칸의 인사이트와 원자를
# line_text와 함께 펼친다. 원자가 0인 노드는 감추지 않고 "근거 없음"으로 드러낸다.
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca

ROOT = ca.ROOT
OUT = os.path.join(ROOT, '대시보드', '원자 뷰.html')

STACK = ca.STACK
STACK_ROWS = [['전자·공정', '칩'], ['메모리', '열'], ['랙', '데이터센터'], ['전력망', '연료·지정학']]


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

    ins_html = []
    for ins in insights:
        coord = ('노드 ' + ' · '.join(ins['nodes'])) if ins['view'] == 'stack' else ('단계 ' + ' → '.join(ins['stages']))
        secs = []
        for name, lines in ins['sections']:
            items = ''.join('<li>%s</li>' % md_inline(re.sub(r'^-\s*', '', l)) for l in lines)
            secs.append('<h4>%s</h4><ul>%s</ul>' % (esc(name), items))
        ins_html.append(
            '<details class="ins" data-view="%s" data-coord="%s" data-atoms="%s">'
            '<summary><span class="cid">%s</span><span class="asof">as_of %s</span>'
            '<h2>%s</h2><p class="sub">%s · 원자 %d개%s</p></summary>'
            '<div class="body">%s</div></details>'
            % (esc(ins['view']), esc(coord), esc(','.join(ins['atoms'])),
               esc(ins['view'].upper()), esc(ins['as_of']), md_inline(ins['claim']),
               esc(coord), len(ins['atoms']),
               (' · 무관 %d개' % len(ins['dismissed'])) if ins['dismissed'] else '',
               ''.join(secs)))

    payload = json.dumps({'atoms': adata, 'insights': [
        {'file': i['file'], 'view': i['view'], 'nodes': i['nodes'], 'stages': i['stages'],
         'atoms': i['atoms'], 'claim': i['claim'], 'as_of': i['as_of']} for i in insights]},
        ensure_ascii=False)

    docs = len({a['doc'] for a in adata})
    html = (TMPL
            .replace('__CHAIN__', chain_html)
            .replace('__BAND__', band_html)
            .replace('__INSIGHTS__', ''.join(ins_html))
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
<title>원자 뷰 — 근거의 좌표</title>
<style>
  :root{--bg:#f7f8fa;--card:#fff;--ink:#1a2233;--sub:#5b6577;--faint:#8892a3;--line:#e3e7ee;--accent:#2563eb;--accent2:#1e40af;--soft:#eaf1fe;--sunk:#eef1f5;--shadow:0 1px 2px rgba(26,34,51,.05)}
  @media (prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#7e8798;--line:#2a3140;--accent:#7aa5f8;--accent2:#9ab8fa;--soft:#1e2a44;--sunk:#242b38;--shadow:none}}
  *{box-sizing:border-box}
  body{background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.64;margin:0;padding:0 20px 80px}
  .wrap{max-width:900px;margin:0 auto}
  header{padding:52px 0 6px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
  h1{font-size:clamp(28px,6vw,44px);font-weight:850;letter-spacing:-.035em;margin:0}
  h1::after{content:"";display:block;width:52px;height:3px;background:var(--accent);margin-top:14px;border-radius:2px}
  .lede{color:var(--sub);font-size:15px;margin:16px 0 0;max-width:64ch}
  .meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:12.5px;color:var(--faint)}
  h3.sec{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:38px 0 4px}
  .axnote{font-size:13px;color:var(--sub);margin:0 0 14px;max-width:64ch}
  .chain .row{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;position:relative}
  .band{display:grid;grid-template-columns:repeat(auto-fit,minmax(118px,1fr));gap:8px}
  .cell{text-align:left;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:11px;
        padding:12px 13px;cursor:pointer;font:inherit;color:inherit;display:block;box-shadow:var(--shadow);transition:transform .12s,border-color .12s}
  .cell:hover{transform:translateY(-1px);border-color:var(--accent)}
  .cell.empty{border-left-color:var(--line);background:var(--sunk);opacity:.85}
  .cell.on{border-color:var(--accent);background:var(--soft)}
  .cell .ord{display:block;font-size:10px;font-weight:800;color:var(--faint);letter-spacing:.08em}
  .cell .nm{display:block;font-size:14.5px;font-weight:800;letter-spacing:-.01em}
  .cell .ct{display:block;font-size:11.5px;color:var(--faint);font-variant-numeric:tabular-nums;margin-top:2px}
  .cell.empty .ct{color:#b0463f}
  @media (prefers-color-scheme:dark){.cell.empty .ct{color:#e08a8a}}
  .flow{font-size:11px;color:var(--faint);letter-spacing:.04em;margin:6px 0 0}
  .panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-top:18px;box-shadow:var(--shadow)}
  .panel .ph{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);margin:0 0 4px}
  .panel h2{font-size:20px;font-weight:850;letter-spacing:-.02em;margin:0 0 10px}
  .hint{font-size:13px;color:var(--faint);margin:0}
  .lnk{display:block;font-size:13px;color:var(--ink);text-decoration:none;padding:7px 0;border-bottom:1px solid var(--line)}
  .lnk:last-child{border-bottom:0}
  .lnk b{color:var(--accent2)}
  .atom{border-top:1px solid var(--line);padding:11px 0}
  .atom:first-of-type{border-top:0}
  .aid{font-size:10.5px;font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums}
  .atag{font-size:10px;font-weight:800;padding:1px 7px;border-radius:999px;margin-left:6px;background:var(--sunk);color:var(--faint)}
  .aclaim{font-size:13.5px;color:var(--ink);margin:3px 0 4px}
  .kv{font-size:12px;color:var(--sub);margin:0 0 3px}
  .kv span{color:var(--faint)}
  .src{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;color:var(--sub);background:var(--sunk);
       border-left:2px solid var(--line);border-radius:0 6px 6px 0;padding:7px 9px;margin:5px 0 0;white-space:pre-wrap;word-break:break-word}
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:16px 20px;margin-top:12px;box-shadow:var(--shadow)}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:26px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;color:var(--faint);transition:transform .2s}
  .ins[open]>summary::after{transform:rotate(180deg)}
  .cid{font-size:10.5px;font-weight:800;letter-spacing:.1em;color:var(--accent)}
  .asof{float:right;font-size:11px;color:var(--faint);font-variant-numeric:tabular-nums}
  .ins h2{font-size:18.5px;font-weight:850;letter-spacing:-.02em;margin:6px 0 2px}
  .ins .sub{font-size:12.5px;color:var(--faint);margin:0}
  .body h4{font-size:12px;font-weight:800;color:var(--accent2);margin:14px 0 5px;text-transform:uppercase;letter-spacing:.04em}
  .body ul{margin:0 0 6px;padding-left:17px}
  .body li{font-size:13px;color:var(--sub);line-height:1.58;margin-bottom:4px}
  .body b{color:var(--ink)}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em;background:var(--sunk);padding:1px 4px;border-radius:4px}
  footer{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);font-size:12px;color:var(--faint)}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">Atoms &amp; Views</p>
  <h1>원자 뷰 — 근거의 좌표</h1>
  <p class="lede">문서 원문의 <b>한 줄</b>에서 조건이 붙은 사실 하나(원자)를 뽑고, 두 축의 좌표에 매답니다.
     칸을 누르면 그 칸의 인사이트와 원자가 <b>원문 그 줄</b>과 함께 펼쳐집니다 — 주장이 원문과 어긋나는지 여기서 바로 보입니다.</p>
  <div class="meta">
    <span>원자 __NA__개</span><span>문서 __ND__편</span><span>인사이트 __NI__건</span>
    <span>미배정 __NU__개</span><span>빈 노드: __EMPTY__</span>
  </div>
</header>

<h3 class="sec">스택 뷰 — 물리 의존</h3>
<p class="axnote">위가 상류입니다. 원자가 0인 노드는 감추지 않았습니다 — 사슬이 어디서 끊겼는지가 그 자체로 정보입니다.</p>
__CHAIN__
<p class="flow">전자·공정 → 칩 → 메모리 / 열 → 랙 → 데이터센터 → 전력망 → 연료·지정학</p>

<h3 class="sec">프로세스 뷰 — 결정 순서</h3>
<p class="axnote">같은 층 이름을 쓰지만 다른 축입니다. 어느 결정이 어느 결정보다 먼저 고정되는가 — 스택이 "무엇이 상류인가"를 말하고 이쪽이 "그래서 무엇이 밀리나"를 말합니다.</p>
__BAND__

<div class="panel" id="panel">
  <p class="ph">선택한 칸</p>
  <h2 id="ptitle">칸을 누르세요</h2>
  <p class="hint">스택 노드 또는 프로세스 단계를 누르면 그 칸에 속한 원자와, 그 칸을 근거로 쓴 인사이트가 나옵니다.</p>
</div>

<h3 class="sec">인사이트</h3>
<p class="axnote">원자 3개 이상·문서 2편 이상이어야 쓸 수 있습니다. 조건이 다른 같은 단위의 수치를 나란히 쓰면 검사기가 「조건 충돌」 절을 강제합니다.</p>
__INSIGHTS__

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
document.querySelectorAll('.ins').forEach(function(d, i){
  const t = d.querySelector('h2'); if(t) d.id = D.insights[i] ? D.insights[i].file : ('ins'+i);
});
</script>
'''

if __name__ == '__main__':
    build()
