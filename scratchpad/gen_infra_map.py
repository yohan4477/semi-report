# -*- coding: utf-8 -*-
# AI 인프라 지도 — 공정 다섯을 한 장으로 세운다(2026-09-09. 그 전에는 공정마다 한 장씩
# 다섯 장이었다). 재료는 공정 모듈(map_litho.py·map_packaging.py)이 원문 코퍼스에서 센 빈도이고,
# 이름마다 붙는 판단 한 줄은 insights/maps/takes/<공정>.json 에서 온다 — 빈도만 세우면
# 읽는 사람이 얻는 게 「무엇이 몇 번 나왔나」뿐이라 색인이지 지도가 아니다.
# 손으로 값을 적지 않는다. 새 공정은 모듈 하나를 더 쓰고 PROCESSES 에 이름만 넣는다.
# 쓰기: python gen_infra_map.py [--selftest]
import io, os, re, sys, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import map_litho
import map_etch
import map_packaging
import map_memory
import map_network

# 공정 순서대로. 메모리와 네트워킹은 공정이 아니라 제품 축이라 뒤에 둔다 —
# 새 장은 모듈을 쓰고 이 줄에 넣는다
PROCESSES = [map_litho, map_etch, map_packaging, map_memory, map_network]
OUT_NAME = 'AI 인프라 지도.html'

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
  .ovmap{min-width:610px;height:445px}
  .ovnode{width:155px;padding:8px 10px}.ovnode.litho{left:1%}.ovnode.etch{left:0}.ovnode.packaging{left:1%}
  .ovnode.memory{right:1%}.ovnode.network{right:1%}
}
.pchips{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 14px}
.pchip{font:inherit;font-size:.84rem;font-weight:600;cursor:pointer;border:1px solid var(--line);
 background:var(--card);color:var(--sub);border-radius:999px;padding:5px 13px}
.pchip:hover{border-color:var(--accent);color:var(--ink)}
.pchip.on{background:var(--accent);border-color:var(--accent);color:#fff}
.pane.off{display:none}
.pane-h{font-size:1.05rem;margin:0 0 10px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.pane-n{font-size:.74rem;font-weight:500;color:var(--sub)}
.ov-lead{color:var(--sub);font-size:.84rem;margin:0 0 12px}
.ovmap{position:relative;min-width:760px;height:470px;margin:0 0 18px}
.ovmap svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.ovmap path{fill:none;stroke:var(--line);stroke-width:2}
.ovcore,.ovnode{position:absolute;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer;
 font:inherit;text-align:left;box-shadow:0 5px 18px rgba(20,32,51,.05)}
.ovcore{left:calc(50% - 90px);top:calc(50% - 35px);width:180px;min-height:70px;border-radius:16px;
 background:var(--accent);border-color:var(--accent);color:#fff;text-align:center;font-weight:750;font-size:1.05rem;padding:12px}
.ovcore span{display:block;font-size:.7rem;font-weight:500;opacity:.85;margin-top:2px}
.ovnode{width:190px;min-height:70px;border-radius:12px;padding:10px 12px}
.ovnode strong{display:block;font-size:.92rem}.ovnode span{display:block;color:var(--sub);font-size:.7rem;margin-top:2px}
.ovnode:hover,.ovnode:focus{border-color:var(--accent);background:var(--accent-soft);outline:none;transform:translateY(-2px)}
.ovnode.litho{left:4%;top:6%}.ovnode.etch{left:1%;top:43%}.ovnode.packaging{left:4%;bottom:6%}
.ovnode.memory{right:4%;top:15%}.ovnode.network{right:4%;bottom:15%}
.ovgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.ovbox{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px}
.ov-go{font:inherit;font-size:.98rem;font-weight:700;color:var(--ink);background:none;border:0;
 padding:0;cursor:pointer;text-align:left}
.ov-go:hover{color:var(--accent)}
.ov-n{font-size:.72rem;color:var(--sub);margin:3px 0 8px}
.ov-takes{margin:0;padding-left:16px}
.ov-takes li{font-size:.82rem;margin-bottom:6px}
.ov-none{font-size:.8rem;color:var(--sub);margin:0}
.takes h3{font-size:.82rem;margin:0 0 5px;color:var(--sub)}
.takes .tkbr{margin-bottom:11px}
.takes ul{margin:0;padding-left:16px}
.takes li{font-size:.85rem;margin-bottom:6px;cursor:pointer}
.takes li:hover{color:var(--accent)}
.takes li b{margin-right:5px}
.tk-none{font-size:.8rem;color:var(--sub);margin:0}
.asof{color:var(--sub);font-size:.7rem;margin-left:6px;white-space:nowrap}
.panel .p-take{font-size:.9rem;margin:0 0 6px;padding:7px 9px;border-radius:8px;
 background:var(--accent-soft);color:var(--ink)}
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


def takes_of(proc):
    """이름별 판단 한 줄. insights/maps/takes/<공정>.json — 없으면 빈 사전."""
    path = os.path.join(ROOT, 'insights', 'maps', 'takes', '%s.json' % proc.KEY)
    if not os.path.isfile(path):
        return {}
    return json.loads(io.open(path, encoding='utf-8').read())


def take_list(view, takes):
    """가지마다 그 가지에 달린 판단을 모아 세운다 — 지도 아래 읽는 자리."""
    out = []
    for b in view['branches']:
        rows = []
        for nd in b['nodes']:
            for x in [nd] + list(nd.get('kids', [])):
                t = takes.get(x['name'])
                if not t or not t.get('take'):
                    continue
                rows.append('<li data-take="%s"><b>%s</b> %s<span class="asof">%s</span></li>'
                            % (html.escape(x['name'], quote=True),
                               html.escape(x['name']), html.escape(t['take']),
                               html.escape(t.get('asof', ''))))
        if not rows:
            continue
        out.append('<div class="tkbr"><h3>%s</h3><ul>%s</ul></div>'
                   % (html.escape(b['name']), '\n'.join(rows)))
    if not out:
        return ('<p class="tk-none">이 뷰에는 아직 판단이 없다 — 이름과 횟수만 서 있다.</p>')
    return '\n'.join(out)


def check_ui(doc, panes, procs, takes):
    """이 장의 규약을 기계가 보는 자리. 어기면 파일을 쓰지 않는다.

    공정 다섯을 한 장으로 몬 뒤(2026-09-09)로는 조용히 깨지는 자리가 늘었다 —
    공정 하나를 더 붙일 때 화면이 겹치거나 사라지는 곳들이다.
    """
    bad = []

    # U0 공정 칸은 「한눈」 하나에 공정 수를 더한 만큼, 처음 켜진 것은 한눈뿐이다
    procchips = re.findall(r'<button class="pchip[^"]*" data-proc="([^"]+)"', doc)
    want = ['all'] + [p.KEY for p in procs]
    if procchips != want:
        bad.append('U0 공정 칸이 %r — %r 여야 한다' % (procchips, want))
    on = re.findall(r'<section class="pane" data-proc="([^"]+)"', doc)
    if on != ['all']:
        bad.append('U0 처음에 켜진 화면이 %r — 한눈 하나여야 한다' % (on,))

    for proc in procs:
        pane = panes[proc.KEY]
        data = pane['data']
        views = data['views']
        keys = [v['key'] for v in views]

        # U1 뷰는 둘 이상이고, 처음 것 하나만 켜진 채로 연다
        if len(views) < 2:
            bad.append('U1 %s 뷰가 %d개다 — 뷰가 하나뿐이면 뷰로 가를 까닭이 없다'
                       % (proc.KEY, len(views)))
        first = re.findall(
            r'<div class="mapwrap" data-proc="%s" data-view="([^"]+)"' % proc.KEY, doc)
        if first != keys[:1]:
            bad.append('U1 %s 처음에 켜진 지도가 %r — 첫 뷰 하나여야 한다'
                       % (proc.KEY, first))

        # U2 빈 가지·빈 마디 금지
        for v in views:
            if not v['branches']:
                bad.append('U2 %s 뷰 「%s」에 가지가 없다' % (proc.KEY, v['label']))
            for b in v['branches']:
                if not b['nodes']:
                    bad.append('U2 %s 「%s」의 가지 「%s」가 비었다'
                               % (proc.KEY, v['label'], b['name']))
                if not b['note']:
                    bad.append('U2 %s 가지 「%s」에 한 줄 설명이 없다'
                               % (proc.KEY, b['name']))

        # U3 나무에 쓴 이름은 전부 사전에 있다 — 사전에 없는 말은 만들지 않는다
        for v in views:
            for nd in walk(v):
                if nd['name'] not in proc.NAMES:
                    bad.append('U3 %s 「%s」가 NAMES 사전에 없다' % (proc.KEY, nd['name']))

        # U4 뷰마다 지도·목록·설명·판단이 한 벌씩 — 좁은 화면에서 뷰가 사라지지 않게
        for k in keys:
            for cls in ('mapwrap', 'listwrap', 'nview', 'takewrap'):
                one = 'class="%s" data-proc="%s" data-view="%s"' % (cls, proc.KEY, k)
                off = 'class="%s off" data-proc="%s" data-view="%s"' % (cls, proc.KEY, k)
                if doc.count(one) + doc.count(off) != 1:
                    bad.append('U4 %s 뷰 %s 의 %s 가 한 벌이 아니다' % (proc.KEY, k, cls))
        chips = re.findall(r'class="chip[^"]*" data-proc="%s" data-view=' % proc.KEY, doc)
        if len(chips) != len(keys):
            bad.append('U4 %s 칩 수와 뷰 수가 다르다' % proc.KEY)

        # U5 넓은 그릇과 좁은 그릇이 같은 이름을 담는다
        for v in views:
            names = {nd['name'] for nd in walk(v)}
            for tag, frag in (('지도', pane['map'][v['key']]),
                              ('목록', pane['list'][v['key']])):
                got = set(html.unescape(x)
                          for x in re.findall(r'data-node="([^"]+)"', frag))
                if got != names:
                    bad.append('U5 %s 뷰 %s 의 %s 가 담은 이름이 다르다: %s'
                               % (proc.KEY, v['key'], tag, sorted(names ^ got)))

        # U6 원문에 없는 이름은 흐리고 누를 수 없다 — 없는 값을 그리지 않는다
        for v in views:
            for nd in walk(v):
                if nd['n'] == 0:
                    esc = html.escape(nd['name'], quote=True)
                    if ('class="leaf dim" data-node="%s"' % esc) not in doc:
                        bad.append('U6 %s 0회인 「%s」가 지도에서 안 흐리다'
                                   % (proc.KEY, nd['name']))
                    if ('data-node="%s" disabled' % esc) not in doc:
                        bad.append('U6 %s 0회인 「%s」가 목록에서 눌린다'
                                   % (proc.KEY, nd['name']))

        # U8 판단은 그 공정 화면 안에 서 있다 — 한눈에 셋만 세우고 마는 것을 막는다.
        # 파일에만 있고 공정 화면에 없으면 「썼는데 아무도 못 읽는」 자리가 된다
        shelf = chr(10).join(pane['take'].values())
        for name, t in (takes.get(proc.KEY) or {}).items():
            if not t.get('take'):
                continue
            if html.escape(t['take']) not in shelf:
                bad.append('U8 %s 「%s」의 판단이 공정 화면에 없다' % (proc.KEY, name))

    # U7 자리가 어긋나지 않았나 — 인자 순서가 밀리면 <title> 이 CSS 를 먹고 스타일이
    # 통째로 사라진다. 눈으로만 보면 「검게 칠해진 상자」로 나타나 원인을 찾기 어렵다.
    head = doc[doc.find('<title>'):doc.find('</title>')]
    if 'AI 인프라 지도' not in head or '{' in head:
        bad.append('U7 <title> 이 「AI 인프라 지도」가 아니다 — 인자 순서가 밀렸다')
    style = doc[doc.find('<style>'):doc.find('</style>')]
    for rule in ('.narrow{display:none}', '.mapwrap.off', 'svg.map', '.pane.off'):
        if rule not in style:
            bad.append('U7 <style> 안에 %s 규칙이 없다 — CSS 가 안 들어갔다' % rule)

    if bad:
        raise SystemExit('check_ui 규약 위반 %d건\n  ' % len(bad) + '\n  '.join(bad))


def pane_of(proc):
    """공정 하나치 그릇 — 지도·목록·판단·설명을 뷰마다 한 벌씩."""
    data = proc.scan()
    takes = takes_of(proc)
    views = data['views']
    idx = {}
    for v in views:
        for nd in walk(v):
            idx[nd['name']] = {'n': nd['n'], 'ndoc': nd['ndoc'], 'top': nd['top']}
    return {'proc': proc, 'data': data, 'takes': takes, 'idx': idx,
            'map': {v['key']: svg(v, proc.LABEL) for v in views},
            'list': {v['key']: tree_list(v) for v in views},
            'take': {v['key']: take_list(v, takes) for v in views}}


def pane_html(pane):
    proc, data, views = pane['proc'], pane['data'], pane['data']['views']
    k = proc.KEY
    chips = '\n'.join(
        '<button class="chip%s" data-proc="%s" data-view="%s">%s '
        '<span class="cnt">%s</span></button>'
        % (' on' if i == 0 else '', k, v['key'], html.escape(v['label']),
           html.escape(v['hint']))
        for i, v in enumerate(views))
    def wrap(cls, frag_by_view, inner=lambda s: s):
        return '\n'.join(
            '<div class="%s%s" data-proc="%s" data-view="%s">%s</div>'
            % (cls, '' if i == 0 else ' off', k, v['key'], inner(frag_by_view[v['key']]))
            for i, v in enumerate(views))
    notes = wrap('nview', {v['key']: '\n'.join(
        '<div><b>%s</b> — %s</div>' % (html.escape(b['name']), html.escape(b['note']))
        for b in v['branches']) for v in views})
    n_take = sum(1 for t in pane['takes'].values() if t.get('take'))
    n_live = sum(1 for nd_name, d in pane['idx'].items() if d['n'])
    return ("""<section class="pane off" data-proc="%s">
<h2 class="pane-h">%s <span class="pane-n">이름 %d · 판단 %d · 원문 %d편</span></h2>
<div class="chips" role="group" aria-label="뷰 고르기">%s</div>
<div class="box scroll wide">%s</div>
<div class="narrow">%s</div>
<div class="box takes">%s</div>
<div class="box notes">%s</div>
</section>""" % (k, html.escape(proc.LABEL), n_live, n_take, data['nlitho'],
                 chips,
                 wrap('mapwrap', pane['map']),
                 wrap('listwrap', pane['list']),
                 wrap('takewrap', pane['take']),
                 notes))


def overview(panes, procs):
    """한눈 — 공정마다 상자 하나. 판단이 있으면 앞의 셋을 여기 세운다."""
    out = []
    for proc in procs:
        p = panes[proc.KEY]
        rows = [t for t in p['takes'].values() if t.get('take')]
        n_live = sum(1 for d in p['idx'].values() if d['n'])
        li = ''.join('<li>%s<span class="asof">%s</span></li>'
                     % (html.escape(t['take']), html.escape(t.get('asof', '')))
                     for t in rows[:3])
        body = ('<ul class="ov-takes">%s</ul>' % li if li else
                '<p class="ov-none">아직 판단이 없다 — 이름과 횟수만 서 있다.</p>')
        out.append('<div class="ovbox"><button class="ov-go" data-proc="%s">%s</button>'
                   '<div class="ov-n">이름 %d · 판단 %d · 원문 %d편</div>%s</div>'
                   % (proc.KEY, html.escape(proc.LABEL), n_live,
                      sum(1 for t in p['takes'].values() if t.get('take')),
                      p['data']['nlitho'], body))
    return '\n'.join(out)


def overview_mindmap(panes, procs):
    """첫 화면도 색인 카드가 아니라 공정 다섯이 뻗는 마인드맵으로 세운다."""
    nodes = []
    for proc in procs:
        p = panes[proc.KEY]
        n_live = sum(1 for d in p['idx'].values() if d['n'])
        n_take = sum(1 for t in p['takes'].values() if t.get('take'))
        nodes.append(
            '<button class="ovnode %s ov-go" data-proc="%s"><strong>%s</strong>'
            '<span>이름 %d · 판단 %d · 원문 %d편</span></button>'
            % (proc.KEY, proc.KEY, html.escape(proc.LABEL), n_live, n_take,
               p['data']['nlitho']))
    lines = ('<svg viewBox="0 0 1000 500" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M500 250 C420 250 355 120 235 75"/><path d="M500 250 C410 250 330 250 220 250"/>'
             '<path d="M500 250 C420 250 355 380 235 425"/><path d="M500 250 C580 250 645 155 765 125"/>'
             '<path d="M500 250 C580 250 645 345 765 375"/></svg>')
    return ('<div class="box scroll"><div class="ovmap">%s'
            '<div class="ovcore">AI 인프라<span>공정 다섯의 연결 지도</span></div>%s</div></div>'
            % (lines, '\n'.join(nodes)))


def build():
    procs = PROCESSES
    panes = {p.KEY: pane_of(p) for p in procs}
    takes = {p.KEY: panes[p.KEY]['takes'] for p in procs}
    idx = {p.KEY: panes[p.KEY]['idx'] for p in procs}
    tk = {p.KEY: {n: t for n, t in panes[p.KEY]['takes'].items() if t.get('take')}
          for p in procs}
    nall = panes[procs[0].KEY]['data']['nall']
    pchips = '\n'.join(
        '<button class="pchip%s" data-proc="%s">%s</button>'
        % (' on' if i == 0 else '', key, html.escape(label))
        for i, (key, label) in enumerate(
            [('all', '한눈')] + [(p.KEY, p.LABEL) for p in procs]))
    doc = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI 인프라 지도</title>
<style>%s</style>
</head>
<body>
<main>
<a class="back" href="SemiAnalysis 대시보드.html">← 대시보드</a>
<h1>AI 인프라 지도</h1>
<p class="lead">원문 %d편에서 공정 다섯(리소그래피·증착식각·패키징·메모리·네트워킹)의 이름을 세어 세운 지도다.
공정마다 같은 이름을 네 축(기능·부품·공급·지표)으로 다시 세운다. 이름 옆 숫자는 우리 코퍼스에 몇 번 나왔는지이지
업계 비중이 아니고, 흐린 잎은 아직 우리 원문에 없는 이름이다.
지도 아래 「판단」은 그 이름에 대해 원문이 말한 것을 한 줄로 줄인 것이며, 잎을 누르면 근거 문장이 줄 번호와 함께 아래에 선다.</p>
<div class="pchips" role="group" aria-label="공정 고르기">%s</div>
<section class="pane" data-proc="all">
<p class="ov-lead">가지를 누르면 해당 공정의 기능·부품·공급·지표 마인드맵으로 이어집니다.</p>
%s
<div class="ovgrid">%s</div>
</section>
%s
<div class="box panel" id="panel"><h2>잎을 고르세요</h2><p class="hint">이름 하나를 누르면 그 이름이 나온 원문 목록이 여기 뜬다.</p></div>
</main>
<script>
var IDX = %s;
var TAKE = %s;
var CUR = 'all';
var panel = document.getElementById('panel');
function esc(s){
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function show(name){
  var d = (IDX[CUR] || {})[name];
  var t = (TAKE[CUR] || {})[name];
  document.querySelectorAll('.leaf, .tl').forEach(function(g){
    g.classList.toggle('on', g.getAttribute('data-node') === name);
  });
  var head = '<h2>' + esc(name) + '</h2>';
  if (t) head += '<p class="p-take">' + esc(t.take) +
    (t.asof ? '<span class="asof">' + esc(t.asof) + '</span>' : '') + '</p>';
  if (!d || !d.n){
    panel.innerHTML = head + '<p class="hint">우리 원문에 아직 없는 이름이다.</p>';
    return;
  }
  var li = d.top.map(function(x){
    var parts = x[0].split('/');
    var title = parts[parts.length - 1].replace(/\\.md$/, '');
    var where = parts.slice(0, -1).join(' / ');
    var sents = (x[2] || []).map(function(s){
      return '<div class="q"><span class="ln">' + x[0] + ':' + s[0] + '</span>' +
             esc(s[1]) + '</div>';
    }).join('');
    return '<li><b>' + esc(title) + '</b> — ' + x[1] + '회<span class="where">' + esc(where) +
           '</span>' + sents + '</li>';
  }).join('');
  panel.innerHTML = head + '<p class="hint">이 공정을 말하는 원문 ' +
    d.ndoc + '편에 ' + d.n + '회. 많이 나온 순으로, 줄마다 그 이름이 실제로 든 문장이다:</p><ul>' +
    li + '</ul>';
}
function goProc(k){
  CUR = k;
  document.querySelectorAll('.pchip').forEach(function(c){
    c.classList.toggle('on', c.getAttribute('data-proc') === k);
  });
  document.querySelectorAll('.pane').forEach(function(s){
    s.classList.toggle('off', s.getAttribute('data-proc') !== k);
  });
  panel.hidden = (k === 'all');
  window.scrollTo({top: 0});
}
document.querySelectorAll('.pchip').forEach(function(c){
  c.addEventListener('click', function(){ goProc(c.getAttribute('data-proc')); });
});
document.querySelectorAll('.ov-go').forEach(function(b){
  b.addEventListener('click', function(){ goProc(b.getAttribute('data-proc')); });
});
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
document.querySelectorAll('.takes li[data-take]').forEach(function(li){
  li.addEventListener('click', function(){
    show(li.getAttribute('data-take'));
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
    var k = c.getAttribute('data-view'), p = c.getAttribute('data-proc');
    document.querySelectorAll('.chip[data-proc="' + p + '"]').forEach(function(x){
      x.classList.toggle('on', x === c);
    });
    document.querySelectorAll('[data-proc="' + p + '"].mapwrap, [data-proc="' + p +
      '"].listwrap, [data-proc="' + p + '"].nview, [data-proc="' + p + '"].takewrap')
      .forEach(function(w){ w.classList.toggle('off', w.getAttribute('data-view') !== k); });
  });
});
panel.hidden = true;
</script>
</body>
</html>
""" % (CSS, nall, pchips, overview_mindmap(panes, procs), overview(panes, procs),
       '\n'.join(pane_html(panes[p.KEY]) for p in procs),
       json.dumps(idx, ensure_ascii=False), json.dumps(tk, ensure_ascii=False))
    check_ui(doc, panes, procs, takes)
    out = os.path.join(ROOT, '대시보드', OUT_NAME)
    io.open(out, 'w', encoding='utf-8').write(doc)
    print('wrote %s %.0fKB — 공정 %d · 판단 %d줄'
          % (out, len(doc) / 1024, len(procs),
             sum(len(v) for v in tk.values())))


def selftest():
    """규칙이 결함을 실제로 무는지 본다 — 규칙을 세울 때 먼저 보는 자리."""
    def bites(label, fix):
        try:
            build()
            print('MISS  %s — 검사기가 안 물었다' % label)
            return False
        except SystemExit as e:
            print('BITE  %-24s %s' % (label, str(e).split('\n')[1].strip()))
            return True
        finally:
            fix()

    ok = []
    V = map_litho.VIEWS
    V[0]['branches'][0][2].append('사전에 없는 이름')
    ok.append(bites('U3 사전에 없는 이름', lambda: V[0]['branches'][0][2].pop()))

    V[-1]['branches'].append(('빈 가지', '설명', []))
    ok.append(bites('U2 빈 가지', lambda: V[-1]['branches'].pop()))

    b = V[1]['branches'][0]
    V[1]['branches'][0] = (b[0], '', b[2])
    ok.append(bites('U2 설명 없는 가지',
                    lambda: V[1].__setitem__('branches', [b] + V[1]['branches'][1:])))

    real_list = globals()['tree_list']
    globals()['tree_list'] = lambda v: real_list({'branches': v['branches'][:1]})
    ok.append(bites('U5 목록이 잎을 빠뜨림',
                    lambda: globals().__setitem__('tree_list', real_list)))

    real_css = globals()['CSS']
    globals()['CSS'] = ''
    ok.append(bites('U7 CSS 가 안 들어감',
                    lambda: globals().__setitem__('CSS', real_css)))

    real_procs = globals()['PROCESSES']
    globals()['PROCESSES'] = real_procs[:2]
    globals()['PROCESSES'] = real_procs
    real_pane = globals()['pane_html']
    globals()['pane_html'] = lambda pane: real_pane(pane).replace('class="takewrap"', 'class="takewrap x"', 1)
    ok.append(bites('U4 판단 그릇이 사라짐',
                    lambda: globals().__setitem__('pane_html', real_pane)))

    real_take = globals()['take_list']
    globals()['take_list'] = lambda v, t: ''
    if any(t.get('take') for p in PROCESSES for t in takes_of(p).values()):
        ok.append(bites('U8 판단이 화면에서 빠짐',
                        lambda: globals().__setitem__('take_list', real_take)))
    else:
        globals()['take_list'] = real_take
        print('SKIP  U8 판단이 화면에서 빠짐 — 아직 판단이 한 줄도 없다')

    if any(nd['n'] == 0 for p in PROCESSES for v in p.scan()['views'] for nd in walk(v)):
        real_leaf = globals()['leaf_box']
        globals()['leaf_box'] = lambda nd, x, y, w: real_leaf(
            dict(nd, n=max(nd['n'], 1)), x, y, w)
        ok.append(bites('U6 0회인데 안 흐림',
                        lambda: globals().__setitem__('leaf_box', real_leaf)))
    else:
        print('SKIP  U6 0회인데 안 흐림 — 0회인 이름이 없다')

    build()
    print('요약: 결함 %d개 중 %d개를 물었다' % (len(ok), sum(ok)))
    if not all(ok):
        raise SystemExit('selftest 실패 — 안 무는 규칙이 있다')


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest()
    else:
        build()
