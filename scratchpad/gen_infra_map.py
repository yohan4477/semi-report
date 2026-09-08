# -*- coding: utf-8 -*-
# AI 인프라 지도 — 공정 한 장을 마인드맵으로 세운다. 공정마다 페이지 하나다.
# 재료는 공정 모듈(map_litho.py·map_packaging.py)이 원문 코퍼스에서 센 빈도.
# 손으로 값을 적지 않는다. 새 공정은 모듈 하나를 더 쓰고 PROCESSES 에 이름만 넣는다.
# 쓰기: python gen_infra_map.py [litho|packaging|…]  (없으면 전부)
import io, os, re, sys, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_litho
import map_etch
import map_packaging
import map_memory

# 공정 순서대로. 메모리는 공정이 아니라 제품 축이라 뒤에 둔다 —
# 새 장은 모듈을 쓰고 이 줄에 넣는다
PROCESSES = [map_litho, map_etch, map_packaging, map_memory]

W_ROOT, W_BR, W_MID, W_LEAF = 96, 128, 250, 230
X_ROOT, X_BR, X_MID, X_LEAF = 8, 132, 292, 558
ROW, GAP = 30, 22          # 잎 한 줄 높이, 가지 사이 여백
PAD_TOP = 16


def layout(branches):
    """가지·마디·잎의 y 좌표를 잡는다. 자식을 거느린 마디는 자식들 한가운데 선다."""
    y = PAD_TOP
    rows = []
    for b in branches:
        y0 = y
        mids = []
        for nd in b['nodes']:
            kids = nd.get('kids') or []
            if kids:
                ky0 = y
                kid_rows = []
                for kd in kids:
                    kid_rows.append((kd, y + ROW / 2))
                    y += ROW
                mids.append({'node': nd, 'cy': (ky0 + y) / 2, 'kids': kid_rows})
            else:
                mids.append({'node': nd, 'cy': y + ROW / 2, 'kids': []})
                y += ROW
        rows.append({'name': b['name'], 'mids': mids, 'cy': (y0 + y) / 2})
        y += GAP
    return rows, y + PAD_TOP


def curve(x1, y1, x2, y2, dim=''):
    return ('<path d="M%.1f %.1f C%.1f %.1f, %.1f %.1f, %.1f %.1f" class="link%s"/>'
            % (x1, y1, x1 + 16, y1, x2 - 16, y2, x2, y2, dim))


def leaf_box(nd, x, y, w):
    """잎 상자 하나 — 이름 왼쪽, 횟수 오른쪽."""
    dim = ' dim' if nd['n'] == 0 else ''
    cnt = ('%d회 · %d편' % (nd['n'], nd['ndoc'])) if nd['n'] else '원문 없음'
    return ('<g class="leaf%s" data-node="%s" tabindex="0" role="button">'
            '<rect x="%d" y="%.1f" width="%d" height="24" rx="6" class="n-leaf"/>'
            '<text x="%d" y="%.1f" class="t-leaf">%s</text>'
            '<text x="%d" y="%.1f" class="t-cnt">%s</text></g>'
            % (dim, html.escape(nd['name'], quote=True),
               x, y - 12, w,
               x + 10, y + 4.5, html.escape(nd['name']),
               x + w - 10, y + 4.5, cnt))


def svg(data, label):
    rows, H = layout(data['branches'])
    W = X_LEAF + W_LEAF + 8
    root_y = H / 2
    out = ['<svg class="map" viewBox="0 0 %d %d" width="%d" height="%d" '
           'xmlns="http://www.w3.org/2000/svg" role="img" '
           'aria-label="%s 마인드맵">' % (W, H, W, H, label)]
    # 루트
    out.append('<rect x="%d" y="%.1f" width="%d" height="34" rx="8" class="n-root"/>'
               % (X_ROOT, root_y - 17, W_ROOT))
    out.append('<text x="%.1f" y="%.1f" class="t-root">%s</text>'
               % (X_ROOT + W_ROOT / 2, root_y + 5, html.escape(label)))
    for r in rows:
        # 루트 -> 가지
        out.append(curve(X_ROOT + W_ROOT, root_y, X_BR, r['cy']))
        out.append('<rect x="%d" y="%.1f" width="%d" height="30" rx="7" class="n-br"/>'
                   % (X_BR, r['cy'] - 15, W_BR))
        out.append('<text x="%.1f" y="%.1f" class="t-br">%s</text>'
                   % (X_BR + W_BR / 2, r['cy'] + 4.5, html.escape(r['name'])))
        for m in r['mids']:
            nd, cy = m['node'], m['cy']
            # 열이 층을 뜻한다 — 마디는 자식이 있든 없든 마디 칸에 선다
            out.append(curve(X_BR + W_BR, r['cy'], X_MID, cy,
                             ' dim' if nd['n'] == 0 else ''))
            out.append(leaf_box(nd, X_MID, cy, W_MID))
            for kd, ky in m['kids']:
                out.append(curve(X_MID + W_MID, cy, X_LEAF, ky,
                                 ' dim' if kd['n'] == 0 else ''))
                out.append(leaf_box(kd, X_LEAF, ky, W_LEAF))
    out.append('</svg>')
    return '\n'.join(out)


CSS = """
:root{--bg:#f7f8fa;--card:#fff;--ink:#1a2233;--sub:#5b6577;--line:#e3e7ee;--accent:#2563eb;--accent-soft:#eaf1fe;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--line:#2a3140;--accent:#7aa5f8;--accent-soft:#1e2a44;}}
:root[data-theme="dark"]{--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--line:#2a3140;--accent:#7aa5f8;--accent-soft:#1e2a44;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);margin:0;padding:16px;font-size:15px;line-height:1.6;
 font-family:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,sans-serif}
main{max-width:900px;margin:0 auto}
.back{display:inline-block;color:var(--sub);font-size:.8rem;text-decoration:none;margin-bottom:12px}
h1{font-size:1.35rem;margin:0 0 6px;letter-spacing:-.01em}
.lead{color:var(--sub);font-size:.86rem;margin:0 0 14px}
.box{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin-bottom:14px}
.scroll{overflow-x:auto}
svg.map{display:block;min-width:520px}
.link{fill:none;stroke:var(--line);stroke-width:1.4}
.link.dim{stroke-dasharray:3 3}
.n-root{fill:#6b7280;stroke:none}
.t-root{fill:#fff;font-size:13px;font-weight:700;text-anchor:middle}
.n-br{fill:var(--accent-soft);stroke:var(--line)}
.t-br{fill:var(--ink);font-size:12px;font-weight:700;text-anchor:middle}
.n-leaf{fill:var(--card);stroke:var(--line)}
.t-leaf{fill:var(--ink);font-size:12px}
.t-cnt{fill:var(--sub);font-size:10.5px;text-anchor:end}
.leaf{cursor:pointer}
.leaf:hover .n-leaf,.leaf:focus .n-leaf{stroke:var(--accent);fill:var(--accent-soft)}
.leaf.dim{cursor:default;opacity:.45}
.leaf.on .n-leaf{stroke:var(--accent);stroke-width:1.8;fill:var(--accent-soft)}
.panel h2{font-size:.95rem;margin:0 0 4px}
.panel .hint{color:var(--sub);font-size:.82rem;margin:0}
.panel ul{margin:8px 0 0;padding-left:18px}
.panel li{font-size:.82rem;color:var(--sub);word-break:break-all}
.panel li b{color:var(--ink);font-weight:600}
.panel li .where{opacity:.7;font-size:.75rem;margin-left:6px}
.panel li{margin-bottom:9px}
.panel .q{margin:4px 0 0;padding:5px 8px;border-left:2px solid var(--line);
 background:var(--bg);border-radius:0 6px 6px 0;font-size:.78rem;color:var(--ink);line-height:1.5}
.panel .q .ln{display:block;color:var(--sub);font-size:.68rem;margin-bottom:2px;word-break:break-all}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}
.chip{font:inherit;font-size:.78rem;cursor:pointer;border:1px solid var(--line);background:var(--card);
 color:var(--sub);border-radius:999px;padding:4px 11px}
.chip .cnt{opacity:.6;font-size:.72rem;margin-left:3px}
.chip:hover{border-color:var(--accent);color:var(--ink)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.chip.on .cnt{opacity:.85}
.mapwrap.off, .listwrap.off, .nview.off{display:none}
.narrow{display:none}
.tb{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:8px;overflow:hidden}
.tb-head{display:flex;align-items:center;gap:8px;width:100%;font:inherit;font-size:.92rem;font-weight:700;
 color:var(--ink);background:none;border:0;padding:11px 13px;cursor:pointer;text-align:left}
.tb-name{flex:1}
.tb-n{font-size:.72rem;font-weight:600;color:var(--sub);background:var(--accent-soft);border-radius:999px;padding:1px 8px}
.tb-caret{color:var(--sub);font-size:.7rem;transition:transform .15s}
.tb.fold .tb-caret{transform:rotate(-90deg)}
.tb.fold .tb-body{display:none}
.tb-body{padding:0 13px 10px}
.tb-note{font-size:.78rem;color:var(--sub);margin:0 0 8px}
.tl{display:flex;align-items:center;gap:10px;width:100%;font:inherit;font-size:.86rem;color:var(--ink);
 background:none;border:0;border-top:1px solid var(--line);padding:10px 2px;cursor:pointer;text-align:left}
.tl-name{flex:1}
.tl-n{font-size:.74rem;color:var(--sub);white-space:nowrap}
.tl.sub{padding-left:16px;font-size:.82rem}
.tl.sub .tl-name::before{content:"└ ";color:var(--sub)}
.tl.dim{opacity:.45;cursor:default}
.tl.on{color:var(--accent);font-weight:700}
.notes{font-size:.8rem;color:var(--sub)}
.notes b{color:var(--ink)}
@media (max-width: 640px){
  body{padding:12px}
  .wide{display:none}
  .narrow{display:block}
  /* 가지 설명이 목록 안에 이미 붙어 있어 아래 상자는 겹친다 */
  .notes{display:none}
  h1{font-size:1.2rem}
  .panel li{word-break:normal}
  .panel li .where{display:block;margin-left:0}
}
"""


def walk(view):
    """가지의 마디와 자식을 한 줄로 편다 — 세거나 목록으로 낼 때 쓴다."""
    for b in view['branches']:
        for nd in b['nodes']:
            yield nd
            for kd in nd.get('kids', []):
                yield kd


def tree_list(view):
    """좁은 화면용 그릇 — 같은 나무를 접이식 목록으로. 첫 가지만 펴고 연다."""
    out = []
    for i, b in enumerate(view['branches']):
        out.append('<div class="tb%s">' % ('' if i == 0 else ' fold'))
        out.append('<button class="tb-head" aria-expanded="%s"><span class="tb-name">%s</span>'
                   '<span class="tb-n">%d</span><span class="tb-caret">▾</span></button>'
                   % ('true' if i == 0 else 'false',
                      html.escape(b['name']),
                      sum(1 + len(nd.get('kids', [])) for nd in b['nodes'])))
        out.append('<div class="tb-body">')
        out.append('<div class="tb-note">%s</div>' % html.escape(b['note']))

        def row(nd, depth):
            cnt = ('%d회 · %d편' % (nd['n'], nd['ndoc'])) if nd['n'] else '원문 없음'
            return ('<button class="tl%s%s" data-node="%s"%s>'
                    '<span class="tl-name">%s</span><span class="tl-n">%s</span></button>'
                    % (' dim' if not nd['n'] else '',
                       ' sub' if depth else '',
                       html.escape(nd['name'], quote=True),
                       ' disabled' if not nd['n'] else '',
                       html.escape(nd['name']), cnt))

        for nd in b['nodes']:
            out.append(row(nd, 0))
            for kd in nd.get('kids', []):
                out.append(row(kd, 1))
        out.append('</div></div>')
    return '\n'.join(out)


def check_ui(doc, data, parts, proc):
    """이 장의 규약을 기계가 보는 자리. 어기면 파일을 쓰지 않는다.

    다음 공정 가지(증착·식각·패키징)를 붙일 때 조용히 깨지는 자리들이다.
    """
    bad = []
    views = data['views']
    keys = [v['key'] for v in views]

    # U1 뷰는 둘 이상이고, 처음 것 하나만 켜진 채로 연다
    if len(views) < 2:
        bad.append('U1 뷰가 %d개다 — 뷰가 하나뿐이면 뷰로 가를 까닭이 없다' % len(views))
    on = re.findall(r'<div class="mapwrap" data-view="([^"]+)"', doc)
    if on != keys[:1]:
        bad.append('U1 처음에 켜진 지도가 %r — 첫 뷰 하나여야 한다' % (on,))

    # U2 빈 가지·빈 마디 금지
    for v in views:
        if not v['branches']:
            bad.append('U2 뷰 「%s」에 가지가 없다' % v['label'])
        for b in v['branches']:
            if not b['nodes']:
                bad.append('U2 「%s」의 가지 「%s」가 비었다' % (v['label'], b['name']))
            if not b['note']:
                bad.append('U2 가지 「%s」에 한 줄 설명이 없다' % b['name'])

    # U3 나무에 쓴 이름은 전부 사전에 있다 — 사전에 없는 말은 만들지 않는다
    for v in views:
        for nd in walk(v):
            if nd['name'] not in proc.NAMES:
                bad.append('U3 「%s」가 NAMES 사전에 없다' % nd['name'])

    # U4 뷰마다 지도·목록·설명이 한 벌씩 — 좁은 화면에서 뷰가 사라지지 않게
    for k in keys:
        for cls in ('mapwrap', 'listwrap', 'nview'):
            if doc.count('class="%s" data-view="%s"' % (cls, k)) + \
               doc.count('class="%s off" data-view="%s"' % (cls, k)) != 1:
                bad.append('U4 뷰 %s 의 %s 가 한 벌이 아니다' % (k, cls))
    if len(re.findall(r'class="chip[^"]*" data-view=', doc)) != len(keys):
        bad.append('U4 칩 수와 뷰 수가 다르다')

    # U5 넓은 그릇과 좁은 그릇이 같은 이름을 담는다
    for v in views:
        names = {nd['name'] for nd in walk(v)}
        for tag, frag in (('지도', parts['map'][v['key']]),
                          ('목록', parts['list'][v['key']])):
            got = set(html.unescape(x)
                      for x in re.findall(r'data-node="([^"]+)"', frag))
            if got != names:
                bad.append('U5 뷰 %s 의 %s 가 담은 이름이 다르다: %s'
                           % (v['key'], tag, sorted(names ^ got)))

    # U6 원문에 없는 이름은 흐리고 누를 수 없다 — 없는 값을 그리지 않는다
    for v in views:
        for nd in walk(v):
            if nd['n'] == 0:
                esc = html.escape(nd['name'], quote=True)
                if ('class="leaf dim" data-node="%s"' % esc) not in doc:
                    bad.append('U6 0회인 「%s」가 지도에서 안 흐리다' % nd['name'])
                if ('data-node="%s" disabled' % esc) not in doc:
                    bad.append('U6 0회인 「%s」가 목록에서 눌린다' % nd['name'])

    # U7 자리가 어긋나지 않았나 — 인자 순서가 밀리면 <title> 이 CSS 를 먹고 스타일이
    # 통째로 사라진다. 눈으로만 보면 「검게 칠해진 상자」로 나타나 원인을 찾기 어렵다.
    head = doc[doc.find('<title>'):doc.find('</title>')]
    if proc.LABEL not in head or '{' in head:
        bad.append('U7 <title> 이 「%s」가 아니다 — 인자 순서가 밀렸다' % proc.LABEL)
    style = doc[doc.find('<style>'):doc.find('</style>')]
    for rule in ('.narrow{display:none}', '.mapwrap.off', 'svg.map'):
        if rule not in style:
            bad.append('U7 <style> 안에 %s 규칙이 없다 — CSS 가 안 들어갔다' % rule)

    if bad:
        raise SystemExit('check_ui 규약 위반 %d건\n  ' % len(bad) + '\n  '.join(bad))


def build(proc):
    data = proc.scan()
    views = data['views']
    idx = {}
    for v in views:
        for nd in walk(v):
            idx[nd['name']] = {'n': nd['n'], 'ndoc': nd['ndoc'], 'top': nd['top']}
    chips = '\n'.join(
        '<button class="chip%s" data-view="%s">%s <span class="cnt">%s</span></button>'
        % (' on' if i == 0 else '', v['key'], html.escape(v['label']),
           html.escape(v['hint']))
        for i, v in enumerate(views))
    map_frag = {v['key']: svg(v, proc.LABEL) for v in views}
    list_frag = {v['key']: tree_list(v) for v in views}
    maps = '\n'.join(
        '<div class="mapwrap%s" data-view="%s">%s</div>'
        % ('' if i == 0 else ' off', v['key'], map_frag[v['key']])
        for i, v in enumerate(views))
    lists = '\n'.join(
        '<div class="listwrap%s" data-view="%s">%s</div>'
        % ('' if i == 0 else ' off', v['key'], list_frag[v['key']])
        for i, v in enumerate(views))
    notes = '\n'.join(
        '<div class="nview%s" data-view="%s">%s</div>'
        % ('' if i == 0 else ' off', v['key'],
           '\n'.join('<div><b>%s</b> — %s</div>'
                     % (html.escape(b['name']), html.escape(b['note']))
                     for b in v['branches']))
        for i, v in enumerate(views))
    doc = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 인프라 지도 — %s</title>
<style>%s</style>
</head>
<body>
<main>
<a class="back" href="SemiAnalysis 대시보드.html">← 대시보드</a>
<h1>AI 인프라 지도 — %s</h1>
<p class="lead">원문 %d편 가운데 %s를 말하는 %d편에서만 이름을 세어 세운 지도다 — 흔한 말이 딴 문맥에서 부풀지 않게
걸렀고, 그 문서 안에서도 앞뒤 두 줄에 그 공정의 신호가 있는 줄만 셌다. 같은 이름을 어느 축으로 놓느냐에 따라 나무가 달라져
뷰를 넷으로 나눴다 — 기능·부품·공급·지표.
잎을 누르면 그 이름이 실제로 든 문장이 파일과 줄 번호와 함께 아래에 선다. 숫자는 우리 코퍼스에 몇 번 나왔는지이지 업계 비중이
아니다. 흐린 잎은 아직 우리 원문에 없는 이름이다.</p>
<div class="chips" role="group" aria-label="뷰 고르기">%s</div>
<div class="box scroll wide">%s</div>
<div class="narrow">%s</div>
<div class="box panel" id="panel"><h2>잎을 고르세요</h2><p class="hint">이름 하나를 누르면 그 이름이 나온 원문 목록이 여기 뜬다.</p></div>
<div class="box notes">%s</div>
</main>
<script>
var IDX = %s;
var panel = document.getElementById('panel');
function esc(s){
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function show(name){
  var d = IDX[name];
  document.querySelectorAll('.leaf, .tl').forEach(function(g){
    g.classList.toggle('on', g.getAttribute('data-node') === name);
  });
  if (!d || !d.n){
    panel.innerHTML = '<h2>' + name + '</h2><p class="hint">우리 원문에 아직 없는 이름이다.</p>';
    return;
  }
  var li = d.top.map(function(t){
    var parts = t[0].split('/');
    var title = parts[parts.length - 1].replace(/\.md$/, '');
    var where = parts.slice(0, -1).join(' / ');
    var sents = (t[2] || []).map(function(s){
      return '<div class="q"><span class="ln">' + t[0] + ':' + s[0] + '</span>' +
             esc(s[1]) + '</div>';
    }).join('');
    return '<li><b>' + title + '</b> — ' + t[1] + '회<span class="where">' + where +
           '</span>' + sents + '</li>';
  }).join('');
  panel.innerHTML = '<h2>' + name + '</h2><p class="hint">이 장을 말하는 원문 ' +
    d.ndoc + '편에 ' + d.n + '회. 많이 나온 순으로, 줄마다 그 이름이 실제로 든 문장이다:</p><ul>' +
    li + '</ul>';
}
document.querySelectorAll('.leaf').forEach(function(g){
  if (g.classList.contains('dim')) return;
  g.addEventListener('click', function(){ show(g.getAttribute('data-node')); });
  g.addEventListener('keydown', function(e){
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); show(g.getAttribute('data-node')); }
  });
});
document.querySelectorAll('.tl').forEach(function(t){
  if (t.classList.contains('dim')) return;
  t.addEventListener('click', function(){
    show(t.getAttribute('data-node'));
    panel.scrollIntoView({block: 'nearest', behavior: 'smooth'});
  });
});
document.querySelectorAll('.tb-head').forEach(function(h){
  h.addEventListener('click', function(){
    var box = h.parentNode;
    var fold = box.classList.toggle('fold');
    h.setAttribute('aria-expanded', fold ? 'false' : 'true');
  });
});
document.querySelectorAll('.chip').forEach(function(c){
  c.addEventListener('click', function(){
    var k = c.getAttribute('data-view');
    document.querySelectorAll('.chip').forEach(function(x){ x.classList.toggle('on', x === c); });
    document.querySelectorAll('.mapwrap, .listwrap, .nview').forEach(function(w){
      w.classList.toggle('off', w.getAttribute('data-view') !== k);
    });
  });
});
</script>
</body>
</html>
""" % (proc.LABEL, CSS, proc.LABEL, data['nall'], proc.LABEL, data['nlitho'],
       chips, maps, lists, notes, json.dumps(idx, ensure_ascii=False))
    check_ui(doc, data, {'map': map_frag, 'list': list_frag}, proc)
    out = os.path.join(ROOT, '대시보드', proc.OUT_NAME)
    io.open(out, 'w', encoding='utf-8').write(doc)
    print('wrote', out, len(doc), 'bytes')


def selftest(proc):
    """규칙이 결함을 실제로 무는지 본다 — 규칙을 세울 때 먼저 보는 자리.

    통과했다는 말이 「검사기가 아무것도 못 잡는다」와 같은 뜻이 되는 것을 막는다.
    """
    def bites(label, fix):
        try:
            build(proc)
            print('MISS  %s — 검사기가 안 물었다' % label)
            return False
        except SystemExit as e:
            print('BITE  %-22s %s' % (label, str(e).split('\n')[1].strip()))
            return True
        finally:
            fix()

    ok = []
    V = proc.VIEWS

    V[0]['branches'][0][2].append('사전에 없는 이름')
    ok.append(bites('U3 사전에 없는 이름', lambda: V[0]['branches'][0][2].pop()))

    V[-1]['branches'].append(('빈 가지', '설명', []))
    ok.append(bites('U2 빈 가지', lambda: V[-1]['branches'].pop()))

    b = V[1]['branches'][0]
    V[1]['branches'][0] = (b[0], '', b[2])
    ok.append(bites('U2 설명 없는 가지',
                    lambda: V[1].__setitem__('branches',
                                             [b] + V[1]['branches'][1:])))

    real_list = globals()['tree_list']
    globals()['tree_list'] = lambda v: real_list({'branches': v['branches'][:1]})
    ok.append(bites('U5 목록이 잎을 빠뜨림',
                    lambda: globals().__setitem__('tree_list', real_list)))

    real_css = globals()['CSS']
    globals()['CSS'] = ''
    ok.append(bites('U7 CSS 가 안 들어감',
                    lambda: globals().__setitem__('CSS', real_css)))

    # U6 은 0회인 이름이 있는 장에서만 시험할 수 있다. 없는 장은 SKIP —
    # 「안 물었다」와 「물 것이 없다」는 다르다.
    if any(nd['n'] == 0 for v in proc.scan()['views'] for nd in walk(v)):
        real_leaf = globals()['leaf_box']
        globals()['leaf_box'] = lambda nd, x, y, w: real_leaf(
            dict(nd, n=max(nd['n'], 1)), x, y, w)
        ok.append(bites('U6 0회인데 안 흐림',
                        lambda: globals().__setitem__('leaf_box', real_leaf)))
    else:
        print('SKIP  U6 0회인데 안 흐림 — 이 장에는 0회인 이름이 없다')

    build(proc)
    print('요약: %s — 결함 %d개 중 %d개를 물었다' % (proc.LABEL, len(ok), sum(ok)))
    if not all(ok):
        raise SystemExit('selftest 실패 — 안 무는 규칙이 있다')


if __name__ == '__main__':
    argv = [a for a in sys.argv[1:] if not a.startswith('-')]
    todo = [p for p in PROCESSES if not argv or p.KEY in argv]
    if not todo:
        raise SystemExit('모르는 공정이다: %s (있는 것: %s)'
                         % (argv, [p.KEY for p in PROCESSES]))
    for proc in todo:
        if '--selftest' in sys.argv:
            selftest(proc)
        else:
            build(proc)
