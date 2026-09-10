# -*- coding: utf-8 -*-
"""밸류체인 탐색기 — data/valuechain/*.json 을 읽어 한 장짜리 HTML 로 굽는다.

원본은 JSON 두 장이다. HTML 은 생성물이니 손으로 고치지 않는다.
  data/valuechain/companies.json      회사
  data/valuechain/relationships.json  관계 (source 가 target 에게 준다)
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')

CDN = 'https://cdn.jsdelivr.net/npm'
LIBS = [
    CDN + '/react@18.3.1/umd/react.production.min.js',
    CDN + '/react-dom@18.3.1/umd/react-dom.production.min.js',
    CDN + '/reactflow@11.11.4/dist/umd/index.js',
    CDN + '/@dagrejs/dagre@1.1.4/dist/dagre.min.js',
]
RF_CSS = CDN + '/reactflow@11.11.4/dist/style.css'

TEMPLATE = u'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>밸류체인 탐색기</title>
<link rel="stylesheet" href="__RFCSS__">
<style>__CSS__</style>
</head><body>
<div id="root"></div>
__SCRIPTS__
<script>window.__VC__ = __DATA__;</script>
<script>__APP__</script>
</body></html>
'''

CSS = u'''
:root{--paper:#fff;--ink1:#1a2233;--ink2:#39415a;--ink3:#6b7488;--ink4:#98a0b0;
--line:#d6dae2;--bg:#f7f8fa;--hi:#e8eef7;--hiline:#39415a}
*{box-sizing:border-box}
html,body,#root{height:100%;margin:0}
body{background:var(--bg);color:var(--ink1);
font:14px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",sans-serif}
.app{display:flex;flex-direction:column;height:100%}
.top{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 16px;
background:var(--paper);border-bottom:1px solid var(--line)}
.brand{font-size:15px;font-weight:700;letter-spacing:-.2px;margin-right:4px}
.brand small{display:block;font-size:11.5px;font-weight:400;color:var(--ink3)}
.search{position:relative}
.search input{width:230px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;
font:inherit;font-size:13px;background:var(--paper);color:var(--ink1)}
.sug{position:absolute;z-index:30;top:36px;left:0;width:300px;max-height:280px;overflow:auto;
background:var(--paper);border:1px solid var(--line);border-radius:6px;
box-shadow:0 6px 20px rgba(26,34,51,.10)}
.sug div{padding:7px 10px;cursor:pointer;font-size:13px;border-bottom:1px solid #f0f2f6}
.sug div:hover{background:var(--hi)}
.sug em{font-style:normal;color:var(--ink3);font-size:11.5px;margin-left:6px}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{padding:5px 10px;border:1px solid var(--line);border-radius:14px;background:var(--paper);
font:inherit;font-size:12.5px;color:var(--ink2);cursor:pointer}
.chip:hover{background:var(--hi)}
.chip.on{background:var(--hiline);border-color:var(--hiline);color:#fff}
.grp{display:flex;align-items:center;gap:6px}
.grp b{font-size:11.5px;color:var(--ink3);font-weight:600}
.main{flex:1;display:flex;min-height:0}
.canvas{flex:1;min-width:0;position:relative}
.side{width:330px;flex:none;background:var(--paper);border-left:1px solid var(--line);
overflow:auto;padding:16px 16px 40px}
.side h2{font-size:17px;margin:0 0 2px;letter-spacing:-.2px}
.side .tk{font-size:12px;color:var(--ink3);margin-bottom:10px}
.side p{margin:0 0 12px;font-size:13px;color:var(--ink2)}
.side .rev{font-size:13px;font-weight:600;color:var(--ink1);margin-bottom:10px}
.side h3{font-size:12px;color:var(--ink3);margin:18px 0 6px;letter-spacing:.3px}
.rel{border:1px solid var(--line);border-radius:6px;padding:8px 10px;margin-bottom:6px;
cursor:pointer;font-size:12.5px}
.rel:hover{background:var(--hi)}
.rel b{display:block;font-size:13px;margin-bottom:2px}
.rel span{color:var(--ink3)}
.rel .src{display:block;color:var(--ink4);font-size:11px;margin-top:4px}
.btns{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 4px}
.btn{padding:6px 11px;border:1px solid var(--line);border-radius:6px;background:var(--paper);
font:inherit;font-size:12.5px;color:var(--ink2);cursor:pointer}
.btn:hover{background:var(--hi)}
.btn.pri{background:var(--hiline);border-color:var(--hiline);color:#fff}
.empty{color:var(--ink3);font-size:13px}
/* 노드 */
.co{width:210px;background:var(--paper);border:1px solid var(--line);border-radius:7px;
padding:8px 10px;position:relative;cursor:pointer}
.co:hover{border-color:var(--ink4)}
.co.center{background:var(--hi);border-color:var(--hiline);border-width:1.6px}
.co.anon{background:#f4eef4;border-style:dashed}
.co .nm{font-size:12.5px;font-weight:600;line-height:1.35;padding-right:22px}
.co .ind{font-size:10.5px;color:var(--ink3);margin-top:2px}
.co .sh{font-size:10.5px;color:var(--ink2);margin-top:3px}
.co .ex{position:absolute;top:6px;right:6px;width:18px;height:18px;line-height:16px;
text-align:center;border:1px solid var(--line);border-radius:4px;background:var(--paper);
font-size:12px;color:var(--ink3)}
.co .ex:hover{background:var(--hiline);color:#fff;border-color:var(--hiline)}
.react-flow__handle{opacity:0;width:1px;height:1px;min-width:0;min-height:0;border:0}
.lgd{position:absolute;left:12px;top:12px;z-index:5;background:rgba(255,255,255,.94);
border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-size:11.5px;color:var(--ink2)}
.lgd div{display:flex;align-items:center;gap:7px;margin-top:3px}
.lgd div:first-child{margin-top:0}
.lgd b{font-weight:600;color:var(--ink3);font-size:11px}
@media (max-width:860px){.main{flex-direction:column}.side{width:auto;border-left:0;
border-top:1px solid var(--line);max-height:44%}.search input{width:150px}}
'''

APP = u'''
(function(){
var h = React.createElement;
var RFlib = window.ReactFlow;
var RF = RFlib.default || RFlib.ReactFlow;
var Background = RFlib.Background, Controls = RFlib.Controls, MiniMap = RFlib.MiniMap;
var Handle = RFlib.Handle, Position = RFlib.Position, MarkerType = RFlib.MarkerType;
var useState = React.useState, useMemo = React.useMemo, useCallback = React.useCallback;

var DATA = window.__VC__;
var CO = {};
DATA.companies.forEach(function(c){ CO[c.id] = c; });
var RELS = DATA.relationships;

var PERIODS = (function(){
  var s = {}; RELS.forEach(function(r){ s[r.period] = 1; });
  return Object.keys(s).sort();
})();

var CONF_LABEL = { high: '공시로 확인', medium: '한쪽만 공시', low: '추정' };
var CONF_STYLE = {
  high:   { stroke: '#6b7488', strokeWidth: 1.7 },
  medium: { stroke: '#8b93a5', strokeWidth: 1.4, strokeDasharray: '6 4' },
  low:    { stroke: '#b0b6c2', strokeWidth: 1.3, strokeDasharray: '2 4' }
};

function label(c){ return c.name_ko || c.name; }
function up(id, f){ return RELS.filter(function(r){ return r.target === id && f(r); }); }
function down(id, f){ return RELS.filter(function(r){ return r.source === id && f(r); }); }

// ── 노드 ──────────────────────────────────────────────────────────
function CoNode(p){
  var d = p.data, c = d.co;
  var cls = 'co' + (d.isCenter ? ' center' : '') + (c.anon ? ' anon' : '');
  var kids = [
    h(Handle, { key:'t', type:'target', position: Position.Left }),
    h(Handle, { key:'s', type:'source', position: Position.Right }),
    h('div', { key:'n', className:'nm' }, label(c)),
    h('div', { key:'i', className:'ind' }, c.industry + (c.country ? ' · ' + c.country : ''))
  ];
  if (d.share) kids.push(h('div', { key:'sh', className:'sh' }, d.share));
  if (d.hidden > 0) kids.push(h('div', {
    key:'x', className:'ex', title: '이웃 ' + d.hidden + '곳 더 펼치기',
    onClick: function(e){ e.stopPropagation(); d.onExpand(c.id); }
  }, '+'));
  return h('div', { className: cls, onClick: function(){ d.onOpen(c.id); } }, kids);
}
var NODE_TYPES = { co: CoNode };

// ── 배치 ──────────────────────────────────────────────────────────
function place(nodes, edges){
  var g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(function(){ return {}; });
  g.setGraph({ rankdir:'LR', nodesep:16, ranksep:120, marginx:24, marginy:24 });
  nodes.forEach(function(n){ g.setNode(n.id, { width:210, height:n.__h }); });
  edges.forEach(function(e){ g.setEdge(e.source, e.target); });
  dagre.layout(g);
  return nodes.map(function(n){
    var p = g.node(n.id);
    return Object.assign({}, n, { position: { x: p.x - 105, y: p.y - n.__h / 2 } });
  });
}

// ── 앱 ────────────────────────────────────────────────────────────
function App(){
  var s0 = useState('nvidia'), center = s0[0], setCenter = s0[1];
  var s1 = useState({}), open = s1[0], setOpen = s1[1];          // 펼친 회사
  var s2 = useState('nvidia'), sel = s2[0], setSel = s2[1];      // 옆판에 띄운 회사
  var s3 = useState(''), q = s3[0], setQ = s3[1];
  var s4 = useState(PERIODS.slice()), per = s4[0], setPer = s4[1];
  var s5 = useState(['high','medium','low']), conf = s5[0], setConf = s5[1];

  var pass = useCallback(function(r){
    return per.indexOf(r.period) >= 0 && conf.indexOf(r.confidence) >= 0;
  }, [per, conf]);

  var graph = useMemo(function(){
    var keep = {}; keep[center] = 1;
    var roots = [center].concat(Object.keys(open));
    roots.forEach(function(id){
      up(id, pass).forEach(function(r){ keep[r.source] = 1; });
      down(id, pass).forEach(function(r){ keep[r.target] = 1; });
    });
    var ids = Object.keys(keep).filter(function(id){ return CO[id]; });
    var eds = RELS.filter(function(r){
      return pass(r) && keep[r.source] && keep[r.target];
    }).map(function(r, i){
      return {
        id: 'e' + i + r.source + r.target, source: r.source, target: r.target,
        type: 'smoothstep', style: CONF_STYLE[r.confidence],
        markerEnd: { type: MarkerType.ArrowClosed, width: 13, height: 13,
                     color: CONF_STYLE[r.confidence].stroke },
        data: r
      };
    });
    var nds = ids.map(function(id){
      var c = CO[id];
      var shown = 0, total = 0;
      up(id, pass).forEach(function(r){ total++; if (keep[r.source]) shown++; });
      down(id, pass).forEach(function(r){ total++; if (keep[r.target]) shown++; });
      var sh = null;
      var inbound = RELS.filter(function(r){ return pass(r) && r.target === id && r.share; });
      if (inbound.length) sh = inbound[0].share;
      var lines = 2 + (sh ? 1 : 0);
      var nameLen = label(c).length;
      var nameRows = nameLen > 14 ? 2 : 1;
      var hgt = 16 + nameRows * 17 + (lines - 1) * 15;
      return {
        id: id, type: 'co', position: { x:0, y:0 }, __h: hgt,
        data: { co: c, isCenter: id === center, share: sh,
                hidden: total - shown,
                onOpen: function(x){ setSel(x); },
                onExpand: function(x){ setOpen(function(o){
                  var n = Object.assign({}, o); n[x] = 1; return n; }); } }
      };
    });
    return { nodes: place(nds, eds), edges: eds };
  }, [center, open, pass]);

  function focus(id){
    setCenter(id); setOpen({}); setSel(id); setQ('');
  }

  var hits = q.trim() ? DATA.companies.filter(function(c){
    var t = (c.name + ' ' + (c.name_ko||'') + ' ' + (c.ticker||'') + ' ' + c.industry).toLowerCase();
    return t.indexOf(q.trim().toLowerCase()) >= 0;
  }).slice(0, 12) : [];

  function toggle(arr, v, set){
    set(arr.indexOf(v) >= 0 ? arr.filter(function(x){ return x !== v; }) : arr.concat([v]));
  }

  // ── 옆판 ──
  var c = CO[sel];
  var ups = up(sel, pass), dws = down(sel, pass);
  function relRow(r, other, dir){
    return h('div', { key: dir + other + r.product, className:'rel',
                      onClick: function(){ setSel(other); } }, [
      h('b', { key:'b' }, label(CO[other])),
      h('span', { key:'p' }, r.product + (r.share ? ' · ' + r.share : '')),
      h('span', { key:'c' }, ' · ' + CONF_LABEL[r.confidence]),
      h('span', { key:'s', className:'src' }, r.sources.join(' / '))
    ]);
  }

  var side = h('div', { className:'side' }, [
    h('h2', { key:'h' }, label(c)),
    h('div', { key:'t', className:'tk' },
      [c.ticker, c.industry, c.country].filter(Boolean).join(' · ')),
    c.revenue ? h('div', { key:'r', className:'rev' }, c.revenue) : null,
    h('p', { key:'d' }, c.desc),
    h('div', { key:'bt', className:'btns' }, [
      h('button', { key:'1', className:'btn pri', onClick: function(){ focus(sel); } }, '중심으로'),
      h('button', { key:'2', className:'btn', onClick: function(){
        setOpen(function(o){ var n = Object.assign({}, o); n[sel] = 1; return n; }); } },
        '이웃 펼치기')
    ]),
    h('h3', { key:'hu' }, '공급받는 곳 ' + ups.length),
    ups.length ? ups.map(function(r){ return relRow(r, r.source, 'u'); })
               : h('div', { key:'eu', className:'empty' }, '데이터에 없다'),
    h('h3', { key:'hd' }, '공급하는 곳 ' + dws.length),
    dws.length ? dws.map(function(r){ return relRow(r, r.target, 'd'); })
               : h('div', { key:'ed', className:'empty' }, '데이터에 없다')
  ]);

  var legend = h('div', { className:'lgd' }, [
    h('b', { key:'b' }, '선'),
    h('div', { key:'1' }, [svgLine('high'), '공시가 양쪽을 잇는다']),
    h('div', { key:'2' }, [svgLine('medium'), '한쪽 공시만 있거나 익명이다']),
    h('div', { key:'3' }, [svgLine('low'), '추정이다'])
  ]);
  function svgLine(k){
    var st = CONF_STYLE[k];
    return h('svg', { key:'s'+k, width:30, height:8 },
      h('line', { x1:0, y1:4, x2:30, y2:4, stroke:st.stroke,
                  strokeWidth:st.strokeWidth, strokeDasharray:st.strokeDasharray }));
  }

  return h('div', { className:'app' }, [
    h('div', { key:'top', className:'top' }, [
      h('div', { key:'br', className:'brand' }, ['밸류체인 탐색기',
        h('small', { key:'s' }, '회사를 눌러 상류와 하류를 펼친다')]),
      h('div', { key:'se', className:'search' }, [
        h('input', { key:'i', value:q, placeholder:'회사 이름·티커로 찾기',
                     onChange: function(e){ setQ(e.target.value); } }),
        hits.length ? h('div', { key:'g', className:'sug' }, hits.map(function(x){
          return h('div', { key:x.id, onClick: function(){ focus(x.id); } },
            [label(x), h('em', { key:'e' }, x.industry)]);
        })) : null
      ]),
      h('div', { key:'ch', className:'chips' }, ['nvidia','amd','tsmc','asml'].map(function(id){
        return h('button', { key:id, className:'chip' + (center === id ? ' on' : ''),
                             onClick: function(){ focus(id); } }, label(CO[id]));
      })),
      h('div', { key:'pf', className:'grp' }, [h('b', { key:'b' }, '기간')].concat(
        PERIODS.map(function(p){
          return h('button', { key:p, className:'chip' + (per.indexOf(p) >= 0 ? ' on' : ''),
                               onClick: function(){ toggle(per, p, setPer); } }, p);
        }))),
      h('div', { key:'cf', className:'grp' }, [h('b', { key:'b' }, '근거')].concat(
        ['high','medium','low'].map(function(k){
          return h('button', { key:k, className:'chip' + (conf.indexOf(k) >= 0 ? ' on' : ''),
                               onClick: function(){ toggle(conf, k, setConf); } },
                   CONF_LABEL[k]);
        })))
    ]),
    h('div', { key:'main', className:'main' }, [
      h('div', { key:'cv', className:'canvas' }, [
        h(RF, { key:'rf', nodes: graph.nodes, edges: graph.edges, nodeTypes: NODE_TYPES,
                fitView: true, fitViewOptions: { padding: 0.18 },
                minZoom: 0.2, maxZoom: 1.8, proOptions: { hideAttribution: false },
                nodesDraggable: true, nodesConnectable: false, elementsSelectable: true }, [
          h(Background, { key:'bg', gap: 22, size: 1, color: '#dfe3ea' }),
          h(Controls, { key:'ct', showInteractive: false }),
          h(MiniMap, { key:'mm', pannable: true, zoomable: true,
                       nodeColor: function(n){ return n.data.isCenter ? '#39415a' : '#c9cfda'; } })
        ]),
        legend
      ]),
      side
    ])
  ]);
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();
'''


def build():
    companies = json.load(io.open(os.path.join(DATA, 'companies.json'), encoding='utf-8'))
    rels = json.load(io.open(os.path.join(DATA, 'relationships.json'), encoding='utf-8'))

    ids = set(c['id'] for c in companies)
    bad = [r for r in rels if r['source'] not in ids or r['target'] not in ids]
    if bad:
        raise SystemExit('회사 목록에 없는 관계가 있다: %s' % bad[:3])

    payload = json.dumps({'companies': companies, 'relationships': rels},
                         ensure_ascii=False, separators=(',', ':'))
    scripts = '\n'.join('<script src="%s"></script>' % u for u in LIBS)
    html = (TEMPLATE
            .replace('__RFCSS__', RF_CSS)
            .replace('__CSS__', CSS)
            .replace('__SCRIPTS__', scripts)
            .replace('__DATA__', payload)
            .replace('__APP__', APP))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    return OUT, len(companies), len(rels)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p, nc, nr = build()
    print('%s — 회사 %d · 관계 %d' % (p, nc, nr))
