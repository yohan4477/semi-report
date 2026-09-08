# -*- coding: utf-8 -*-
# AI 인프라 지도 — 공정 가지 하나(리소그래피)를 마인드맵으로 세운다.
# 재료는 scratchpad/litho_scan.py 가 원문 코퍼스에서 센 빈도. 손으로 값을 적지 않는다.
# 산출: 대시보드/AI 인프라 지도.html
import io, os, sys, json, html, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litho_scan

OUT = os.path.join(ROOT, '대시보드', 'AI 인프라 지도.html')

# 가지마다 한 줄 설명 — 그 가지가 무엇을 묶는지. 값이 아니라 이름이다.
BRANCH_NOTE = {
    '빛으로 새긴다': '파장이 짧을수록 가는 선을 새긴다 — 마디 안에 그 갈래가 든다',
    '해상도를 늘린다': '같은 빛으로 더 가늘게 — 여러 번 나눠 찍는다',
    '빛을 안 쓴다': '빛 대신 틀을 찍어 누른다',
    '장비': '노광기를 파는 곳이 마디, 그 기계 안에 든 것이 잎',
    '소재': '웨이퍼에 바르고 깎이는 것',
    '마스크·펠리클': '새길 무늬를 담은 원판과 그 덮개',
    '계측·수율·통제': '얼마나 맞았나, 몇 장 나왔나, 누가 못 사나',
}

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


def svg(data):
    rows, H = layout(data['branches'])
    W = X_LEAF + W_LEAF + 8
    root_y = H / 2
    out = ['<svg class="map" viewBox="0 0 %d %d" width="%d" height="%d" '
           'xmlns="http://www.w3.org/2000/svg" role="img" '
           'aria-label="리소그래피 마인드맵">' % (W, H, W, H)]
    # 루트
    out.append('<rect x="%d" y="%.1f" width="%d" height="34" rx="8" class="n-root"/>'
               % (X_ROOT, root_y - 17, W_ROOT))
    out.append('<text x="%.1f" y="%.1f" class="t-root">리소그래피</text>'
               % (X_ROOT + W_ROOT / 2, root_y + 5))
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
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}
.chip{font:inherit;font-size:.78rem;cursor:pointer;border:1px solid var(--line);background:var(--card);
 color:var(--sub);border-radius:999px;padding:4px 11px}
.chip .cnt{opacity:.6;font-size:.72rem;margin-left:3px}
.chip:hover{border-color:var(--accent);color:var(--ink)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.chip.on .cnt{opacity:.85}
.mapwrap.off{display:none}
.listwrap.off{display:none}
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


def filtered(data, kind):
    """갈래 하나만 남긴 가지 묶음. 잎이 없어진 가지는 통째로 뺀다."""
    if kind == 'all':
        return data
    out = {'nfile': data['nfile'], 'branches': []}
    for b in data['branches']:
        nodes = []
        for nd in b['nodes']:
            kids = [kd for kd in nd.get('kids', []) if kd['kind'] == kind]
            if nd['kind'] == kind or kids:
                cp = dict(nd)
                cp['kids'] = kids
                nodes.append(cp)
        if nodes:
            out['branches'].append({'name': b['name'], 'nodes': nodes})
    return out


def walk(data):
    """가지의 마디와 자식을 한 줄로 편다 — 세거나 목록으로 낼 때 쓴다."""
    for b in data['branches']:
        for nd in b['nodes']:
            yield nd
            for kd in nd.get('kids', []):
                yield kd


CHIPS = [('all', '전체'), ('tech', '기술'), ('co', '회사'), ('idx', '지표·제도')]


def tree_list(data):
    """좁은 화면용 그릇 — 같은 데이터를 접이식 목록으로. 첫 가지만 펴고 연다."""
    out = []
    for i, b in enumerate(data['branches']):
        out.append('<div class="tb%s">' % ('' if i == 0 else ' fold'))
        out.append('<button class="tb-head" aria-expanded="%s"><span class="tb-name">%s</span>'
                   '<span class="tb-n">%d</span><span class="tb-caret">▾</span></button>'
                   % ('true' if i == 0 else 'false',
                      html.escape(b['name']),
                      sum(1 + len(nd.get('kids', [])) for nd in b['nodes'])))
        out.append('<div class="tb-body">')
        out.append('<div class="tb-note">%s</div>'
                   % html.escape(BRANCH_NOTE.get(b['name'], '')))

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


def build():
    data = litho_scan.scan()
    idx = {}
    for nd in walk(data):
        idx[nd['name']] = {'n': nd['n'], 'ndoc': nd['ndoc'], 'top': nd['top']}
    counts = collections.Counter(nd['kind'] for nd in walk(data))
    chips = '\n'.join(
        '<button class="chip%s" data-kind="%s">%s <span class="cnt">%d</span></button>'
        % (' on' if k == 'all' else '', k, html.escape(lab),
           sum(counts.values()) if k == 'all' else counts.get(k, 0))
        for k, lab in CHIPS)
    maps = '\n'.join(
        '<div class="mapwrap%s" data-kind="%s">%s</div>'
        % ('' if k == 'all' else ' off', k, svg(filtered(data, k)))
        for k, _lab in CHIPS)
    lists = '\n'.join(
        '<div class="listwrap%s" data-kind="%s">%s</div>'
        % ('' if k == 'all' else ' off', k, tree_list(filtered(data, k)))
        for k, _lab in CHIPS)
    notes = '\n'.join(
        '<div data-branch="%s" data-kinds="%s"><b>%s</b> — %s</div>'
        % (html.escape(b['name'], quote=True),
           ' '.join(sorted({nd['kind'] for nd in b['nodes']}
                           | {kd['kind'] for nd in b['nodes']
                              for kd in nd.get('kids', [])})),
           html.escape(b['name']), html.escape(BRANCH_NOTE.get(b['name'], '')))
        for b in data['branches'])
    doc = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 인프라 지도 — 리소그래피</title>
<style>%s</style>
</head>
<body>
<main>
<a class="back" href="SemiAnalysis 대시보드.html">← 대시보드</a>
<h1>AI 인프라 지도 — 리소그래피</h1>
<p class="lead">원문 %d편에서 이름을 세어 세운 가지다. 잎을 누르면 그 이름이 가장 많이 나온 원문이 아래에 선다.
숫자는 우리 코퍼스에 몇 번, 몇 편에 나왔는지이지 업계 비중이 아니다. 흐린 잎은 아직 우리 원문에 없는 이름이다.</p>
<div class="chips" role="group" aria-label="갈래 고르기">%s</div>
<div class="box scroll wide">%s</div>
<div class="narrow">%s</div>
<div class="box panel" id="panel"><h2>잎을 고르세요</h2><p class="hint">이름 하나를 누르면 그 이름이 나온 원문 목록이 여기 뜬다.</p></div>
<div class="box notes">%s</div>
</main>
<script>
var IDX = %s;
var panel = document.getElementById('panel');
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
    return '<li><b>' + title + '</b> — ' + t[1] + '회<span class="where">' + where + '</span></li>';
  }).join('');
  panel.innerHTML = '<h2>' + name + '</h2><p class="hint">원문 ' + d.ndoc + '편에 ' + d.n +
    '회. 많이 나온 순으로:</p><ul>' + li + '</ul>';
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
    var k = c.getAttribute('data-kind');
    document.querySelectorAll('.chip').forEach(function(x){ x.classList.toggle('on', x === c); });
    document.querySelectorAll('.mapwrap, .listwrap').forEach(function(w){
      w.classList.toggle('off', w.getAttribute('data-kind') !== k);
    });
    document.querySelectorAll('.notes [data-branch]').forEach(function(d){
      var ks = d.getAttribute('data-kinds').split(' ');
      d.hidden = (k !== 'all' && ks.indexOf(k) < 0);
    });
  });
});
</script>
</body>
</html>
""" % (CSS, data['nfile'], chips, maps, lists, notes,
       json.dumps(idx, ensure_ascii=False))
    io.open(OUT, 'w', encoding='utf-8').write(doc)
    print('wrote', OUT, len(doc), 'bytes')


if __name__ == '__main__':
    build()
