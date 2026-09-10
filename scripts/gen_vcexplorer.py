# -*- coding: utf-8 -*-
"""밸류체인 탐색기 — data/valuechain/*.json 다섯 장을 읽어 한 장짜리 HTML 로 굽는다.

원본은 JSON 다섯 장이다. HTML 은 생성물이니 손으로 고치지 않는다.
  companies.json             회사
  relationships.json         관계 (source 가 target 에게 준다). 숫자를 박지 않는다
  relationship_metrics.json  시점별 비중. 같은 관계에 기간을 계속 덧붙인다
  sources.json               원문 메타데이터와 등급
  evidence.json              관계와 지표 각각에 붙는 근거
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')
TABLES = ['companies', 'relationships', 'relationship_metrics', 'sources', 'evidence']

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
.brand a{color:var(--ink3);text-decoration:none;border-bottom:1px solid var(--line)}
.search{position:relative}
.search input{width:220px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;
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
.side{width:360px;flex:none;background:var(--paper);border-left:1px solid var(--line);
overflow:auto;padding:16px 16px 40px}
.side h2{font-size:17px;margin:0 0 2px;letter-spacing:-.2px}
.side .tk{font-size:12px;color:var(--ink3);margin-bottom:10px}
.side p{margin:0 0 12px;font-size:13px;color:var(--ink2)}
.side .rev{font-size:13px;font-weight:600;color:var(--ink1);margin-bottom:10px}
.side h3{font-size:12px;color:var(--ink3);margin:18px 0 6px;letter-spacing:.3px}
.side a{color:var(--ink2)}
.rel{border:1px solid var(--line);border-radius:6px;padding:8px 10px;margin-bottom:6px;
cursor:pointer;font-size:12.5px}
.rel:hover{background:var(--hi)}
.rel b{display:block;font-size:13px;margin-bottom:2px}
.rel span{color:var(--ink3)}
.btns{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 4px}
.btn{padding:6px 11px;border:1px solid var(--line);border-radius:6px;background:var(--paper);
font:inherit;font-size:12.5px;color:var(--ink2);cursor:pointer}
.btn:hover{background:var(--hi)}
.btn.pri{background:var(--hiline);border-color:var(--hiline);color:#fff}
.empty{color:var(--ink3);font-size:13px}
.flow{font-size:13.5px;font-weight:600;margin-bottom:2px}
.flow span{color:var(--ink3);font-weight:400}
.dots{font-size:11.5px;color:var(--ink3);margin-bottom:10px}
table.m{border-collapse:collapse;width:100%;font-size:12px;margin:4px 0 10px}
table.m th,table.m td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:left;
vertical-align:top;color:var(--ink2)}
table.m th{color:var(--ink3);font-weight:600;font-size:11px;white-space:nowrap}
table.m td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap;
font-weight:600;color:var(--ink1)}
.ev{border-left:2px solid var(--line);padding:2px 0 2px 9px;margin:0 0 9px}
.ev .q{font-size:12px;color:var(--ink2)}
.ev .m{font-size:11px;color:var(--ink4);margin-top:3px}
.badge{display:inline-block;border:1px solid var(--line);border-radius:3px;padding:0 4px;
font-size:10.5px;color:var(--ink3);margin-right:4px}
.meth{font-size:11.5px;color:var(--ink3);background:#f4f6f9;border-radius:5px;
padding:7px 9px;margin:0 0 10px}
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
.react-flow__edge{cursor:pointer}
.lgd{position:absolute;left:12px;top:12px;z-index:5;background:rgba(255,255,255,.94);
border:1px solid var(--line);border-radius:7px;padding:9px 11px;font-size:11.5px;color:var(--ink2)}
.lgd div{display:flex;align-items:center;gap:7px;margin-top:3px}
.lgd div:first-child{margin-top:0}
.lgd b{font-weight:600;color:var(--ink3);font-size:11px}
@media (max-width:860px){.main{flex-direction:column}.side{width:auto;border-left:0;
border-top:1px solid var(--line);max-height:46%}.search input{width:150px}}
'''

APP = u'''
(function(){
var h = React.createElement;
var RFlib = window.ReactFlow;
var RF = RFlib.default || RFlib.ReactFlow;
var Background = RFlib.Background, Controls = RFlib.Controls, MiniMap = RFlib.MiniMap;
var Handle = RFlib.Handle, Position = RFlib.Position, MarkerType = RFlib.MarkerType;
var useState = React.useState, useMemo = React.useMemo, useCallback = React.useCallback;

var DB = window.__VC__;
var CO = {}, SRC = {}, REL = {};
DB.companies.forEach(function(c){ CO[c.id] = c; });
DB.sources.forEach(function(s){ SRC[s.id] = s; });
DB.relationships.forEach(function(r){ REL[r.id] = r; });

// 관계마다 지표와 근거를 미리 묶어 둔다
var MET_BY_REL = {}, EV_BY_REL = {}, EV_BY_MET = {};
DB.relationship_metrics.forEach(function(m){
  (MET_BY_REL[m.relationship_id] = MET_BY_REL[m.relationship_id] || []).push(m);
});
DB.evidence.forEach(function(e){
  if (e.metric_id) (EV_BY_MET[e.metric_id] = EV_BY_MET[e.metric_id] || []).push(e);
  else (EV_BY_REL[e.relationship_id] = EV_BY_REL[e.relationship_id] || []).push(e);
});
var PERIODS = (function(){
  var s = {}; DB.relationship_metrics.forEach(function(m){ s[m.period] = 1; });
  return Object.keys(s).sort();
})();

var CONF_LABEL = { high: '공시로 확인', medium: '한쪽만 공시', low: '추정' };
var CONF_DOTS = { high: '●●●', medium: '●●○', low: '●○○' };
var CONF_STYLE = {
  high:   { stroke: '#6b7488', strokeWidth: 1.7 },
  medium: { stroke: '#8b93a5', strokeWidth: 1.4, strokeDasharray: '6 4' },
  low:    { stroke: '#b0b6c2', strokeWidth: 1.3, strokeDasharray: '2 4' }
};
var SRC_GRADE = { primary_official: '공식 공시', primary_company: '회사 발표',
  industry_research: '업계 조사', reputable_media: '언론', analyst_estimate: '애널리스트 추정',
  our_estimate: '우리 추정' };
var OFFICIAL = { primary_official: 1, primary_company: 1 };
var EV_LABEL = { direct: '직접 서술', indirect: '간접 근거', estimate_input: '추정 입력값',
  absent: '공시에 없음' };
var MET_LABEL = { customer_revenue_share: '고객 매출 비중',
  receivables_share: '매출채권 비중', supply_share: '공급 점유' };
var EST_LABEL = { disclosed: '공시 그대로', derived: '공시에서 계산',
  analyst_estimate: '애널리스트 추정', industry_knowledge: '업계 통설' };

function label(c){ return c.name_ko || c.name; }
function metsOf(rid, per){
  return (MET_BY_REL[rid] || []).filter(function(m){ return per.indexOf(m.period) >= 0; });
}
function latest(rid, per){
  var ms = metsOf(rid, per).slice().sort(function(a, b){
    return a.period_end < b.period_end ? 1 : -1; });
  return ms[0] || null;
}
function isOfficial(rid){
  var evs = (EV_BY_REL[rid] || []).concat(
    (MET_BY_REL[rid] || []).reduce(function(a, m){
      return a.concat(EV_BY_MET[m.id] || []); }, []));
  return evs.some(function(e){
    var s = SRC[e.source_id];
    return s && OFFICIAL[s.source_type] && e.evidence_type !== 'absent';
  });
}

// ── 노드 ──────────────────────────────────────────────────────────
function CoNode(p){
  var d = p.data, c = d.co;
  var cls = 'co' + (d.isCenter ? ' center' : '') + (c.anon ? ' anon' : '');
  var kids = [
    h(Handle, { key:'t', type:'target', position: Position.Left }),
    h(Handle, { key:'s', type:'source', position: Position.Right }),
    h('div', { key:'n', className:'nm' }, label(c)),
    h('div', { key:'i', className:'ind' },
      [c.company_type, c.country].filter(Boolean).join(' · '))
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
  g.setGraph({ rankdir:'LR', nodesep:16, ranksep:130, marginx:24, marginy:24 });
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
  var s1 = useState({}), open = s1[0], setOpen = s1[1];
  var s2 = useState({ kind:'co', id:'nvidia' }), sel = s2[0], setSel = s2[1];
  var s3 = useState(''), q = s3[0], setQ = s3[1];
  var s4 = useState(PERIODS.slice()), per = s4[0], setPer = s4[1];
  var s5 = useState(['high','medium','low']), conf = s5[0], setConf = s5[1];
  var s6 = useState(false), onlyOfficial = s6[0], setOnlyOfficial = s6[1];

  var pass = useCallback(function(r){
    if (conf.indexOf(r.confidence) < 0) return false;
    if (onlyOfficial && !isOfficial(r.id)) return false;
    return true;
  }, [conf, onlyOfficial]);

  var rels = useMemo(function(){ return DB.relationships.filter(pass); }, [pass]);
  function up(id){ return rels.filter(function(r){ return r.target_company_id === id; }); }
  function down(id){ return rels.filter(function(r){ return r.source_company_id === id; }); }

  var graph = useMemo(function(){
    var keep = {}; keep[center] = 1;
    [center].concat(Object.keys(open)).forEach(function(id){
      up(id).forEach(function(r){ keep[r.source_company_id] = 1; });
      down(id).forEach(function(r){ keep[r.target_company_id] = 1; });
    });
    var eds = rels.filter(function(r){
      return keep[r.source_company_id] && keep[r.target_company_id];
    }).map(function(r){
      var m = latest(r.id, per);
      return {
        id: r.id, source: r.source_company_id, target: r.target_company_id,
        type: 'smoothstep', style: CONF_STYLE[r.confidence],
        label: m ? (m.value + m.unit) : undefined,
        labelStyle: { fontSize: 10, fill: '#39415a' },
        labelBgStyle: { fill: '#fff', fillOpacity: .85 },
        labelBgPadding: [3, 1],
        markerEnd: { type: MarkerType.ArrowClosed, width: 13, height: 13,
                     color: CONF_STYLE[r.confidence].stroke }
      };
    });
    var nds = Object.keys(keep).filter(function(id){ return CO[id]; }).map(function(id){
      var c = CO[id];
      var shown = 0, total = 0, sh = null;
      up(id).forEach(function(r){
        total++; if (keep[r.source_company_id]) shown++;
        var m = latest(r.id, per);
        if (m && !sh) sh = m.value + m.unit + ' · ' + MET_LABEL[m.metric];
      });
      down(id).forEach(function(r){ total++; if (keep[r.target_company_id]) shown++; });
      var rows = 2 + (sh ? 1 : 0) + (label(c).length > 14 ? 1 : 0);
      return {
        id: id, type: 'co', position: { x:0, y:0 }, __h: 16 + 17 + (rows - 1) * 15,
        data: { co: c, isCenter: id === center, share: sh, hidden: total - shown,
                onOpen: function(x){ setSel({ kind:'co', id:x }); },
                onExpand: function(x){ setOpen(function(o){
                  var n = Object.assign({}, o); n[x] = 1; return n; }); } }
      };
    });
    return { nodes: place(nds, eds), edges: eds };
  }, [center, open, rels, per]);

  function focus(id){ setCenter(id); setOpen({}); setSel({ kind:'co', id:id }); setQ(''); }

  var hits = q.trim() ? DB.companies.filter(function(c){
    var t = (c.name + ' ' + (c.name_ko||'') + ' ' + (c.ticker||'') + ' ' +
             (c.company_type||'') + ' ' + c.industry).toLowerCase();
    return t.indexOf(q.trim().toLowerCase()) >= 0;
  }).slice(0, 12) : [];

  function toggle(arr, v, set){
    set(arr.indexOf(v) >= 0 ? arr.filter(function(x){ return x !== v; }) : arr.concat([v]));
  }

  // ── 근거 한 줄 ──
  function evRow(e, i){
    var s = SRC[e.source_id];
    return h('div', { key: e.id || i, className:'ev' }, [
      h('div', { key:'q', className:'q' }, '「' + e.evidence + '」'),
      h('div', { key:'m', className:'m' }, [
        h('span', { key:'b', className:'badge' }, SRC_GRADE[s.source_type]),
        h('span', { key:'t', className:'badge' }, EV_LABEL[e.evidence_type]),
        s.publisher + ' · ',
        h('a', { key:'a', href: s.url, target:'_blank', rel:'noreferrer' }, s.title),
        ' · ' + s.published_date
      ])
    ]);
  }

  // ── 옆판: 관계 ──
  function edgePanel(r){
    var a = CO[r.source_company_id], b = CO[r.target_company_id];
    var ms = metsOf(r.id, per).slice().sort(function(x, y){
      return x.period_end < y.period_end ? 1 : -1; });
    var kids = [
      h('div', { key:'f', className:'flow' },
        [label(a), h('span', { key:'s' }, ' 에서 '), label(b), h('span', { key:'e' }, ' 로')]),
      h('div', { key:'t', className:'tk' }, r.category + ' · ' + r.product),
      h('div', { key:'d', className:'dots' },
        CONF_DOTS[r.confidence] + '  ' + CONF_LABEL[r.confidence]),
      h('div', { key:'bt', className:'btns' }, [
        h('button', { key:'1', className:'btn', onClick: function(){ focus(a.id); } },
          label(a) + ' 중심으로'),
        h('button', { key:'2', className:'btn', onClick: function(){ focus(b.id); } },
          label(b) + ' 중심으로')
      ])
    ];
    if (r.notes) kids.push(h('div', { key:'n', className:'meth' }, r.notes));
    kids.push(h('h3', { key:'hm' }, '시점별 지표 ' + ms.length));
    if (ms.length) {
      kids.push(h('table', { key:'tb', className:'m' }, [
        h('thead', { key:'h' }, h('tr', null, [
          h('th', { key:'1' }, '기간'), h('th', { key:'2' }, '지표'),
          h('th', { key:'3' }, '값'), h('th', { key:'4' }, '무엇의 비중인가'),
          h('th', { key:'5' }, '어떻게 얻었나')])),
        h('tbody', { key:'b' }, ms.map(function(m){
          return h('tr', { key:m.id }, [
            h('td', { key:'1' }, m.period),
            h('td', { key:'2' }, MET_LABEL[m.metric] || m.metric),
            h('td', { key:'3', className:'n' }, m.value + m.unit),
            h('td', { key:'4' }, m.basis),
            h('td', { key:'5' }, EST_LABEL[m.estimate_type] || m.estimate_type)]);
        }))]));
      ms.forEach(function(m){
        if (m.method) kids.push(h('div', { key:'me'+m.id, className:'meth' },
          m.period + ' 계산 — ' + m.method));
        var evs = EV_BY_MET[m.id] || [];
        if (evs.length) {
          kids.push(h('h3', { key:'he'+m.id }, m.period + ' 지표의 근거 ' + evs.length));
          evs.forEach(function(e, i){ kids.push(evRow(e, m.id + i)); });
        }
      });
    } else {
      kids.push(h('div', { key:'em', className:'empty' }, '이 기간에 잡힌 숫자가 없다'));
    }
    var re = EV_BY_REL[r.id] || [];
    kids.push(h('h3', { key:'hr' }, '관계 자체의 근거 ' + re.length));
    if (re.length) re.forEach(function(e, i){ kids.push(evRow(e, i)); });
    else kids.push(h('div', { key:'er', className:'empty' }, '근거가 아직 없다'));
    return kids;
  }

  // ── 옆판: 회사 ──
  function coPanel(c){
    var ups = up(c.id), dws = down(c.id);
    function row(r, other, dir){
      var m = latest(r.id, per);
      return h('div', { key: dir + r.id, className:'rel',
                        onClick: function(){ setSel({ kind:'rel', id:r.id }); } }, [
        h('b', { key:'b' }, label(CO[other])),
        h('span', { key:'p' }, r.category + ' · ' + r.product),
        m ? h('span', { key:'m' }, ' · ' + m.value + m.unit + ' (' + m.period + ')') : null,
        h('span', { key:'c' }, ' · ' + CONF_LABEL[r.confidence])
      ]);
    }
    var kids = [
      h('h2', { key:'h' }, label(c)),
      h('div', { key:'t', className:'tk' },
        [c.ticker, c.company_type, c.country].filter(Boolean).join(' · ')),
      c.revenue ? h('div', { key:'r', className:'rev' }, c.revenue) : null,
      h('p', { key:'d' }, c.desc),
      h('div', { key:'bt', className:'btns' }, [
        h('button', { key:'1', className:'btn pri',
                      onClick: function(){ focus(c.id); } }, '중심으로'),
        h('button', { key:'2', className:'btn', onClick: function(){
          setOpen(function(o){ var n = Object.assign({}, o); n[c.id] = 1; return n; }); } },
          '이웃 펼치기'),
        c.website ? h('a', { key:'3', className:'btn', href:c.website,
                             target:'_blank', rel:'noreferrer' }, '회사 사이트') : null
      ]),
      h('h3', { key:'hu' }, '공급받는 곳 ' + ups.length),
      ups.length ? ups.map(function(r){ return row(r, r.source_company_id, 'u'); })
                 : h('div', { key:'eu', className:'empty' }, '데이터에 없다'),
      h('h3', { key:'hd' }, '공급하는 곳 ' + dws.length),
      dws.length ? dws.map(function(r){ return row(r, r.target_company_id, 'd'); })
                 : h('div', { key:'ed', className:'empty' }, '데이터에 없다')
    ];
    return kids;
  }

  var body = sel.kind === 'rel' && REL[sel.id]
    ? edgePanel(REL[sel.id]) : coPanel(CO[sel.id] || CO[center]);

  function svgLine(k){
    var st = CONF_STYLE[k];
    return h('svg', { key:'s'+k, width:30, height:8 },
      h('line', { x1:0, y1:4, x2:30, y2:4, stroke:st.stroke,
                  strokeWidth:st.strokeWidth, strokeDasharray:st.strokeDasharray }));
  }
  var legend = h('div', { className:'lgd' }, [
    h('b', { key:'b' }, '선을 누르면 근거가 열린다'),
    h('div', { key:'1' }, [svgLine('high'), '공시가 양쪽을 잇는다']),
    h('div', { key:'2' }, [svgLine('medium'), '한쪽 공시만 있거나 고객이 익명이다']),
    h('div', { key:'3' }, [svgLine('low'), '추정이다'])
  ]);

  return h('div', { className:'app' }, [
    h('div', { key:'top', className:'top' }, [
      h('div', { key:'br', className:'brand' }, ['밸류체인 탐색기',
        h('small', { key:'s' }, ['회사와 선을 눌러 펼친다 · ',
          h('a', { key:'a', href:'valuechain/네 회사를 한 장씩.html' }, '정적 판')])]),
      h('div', { key:'se', className:'search' }, [
        h('input', { key:'i', value:q, placeholder:'회사 이름·티커로 찾기',
                     onChange: function(e){ setQ(e.target.value); } }),
        hits.length ? h('div', { key:'g', className:'sug' }, hits.map(function(x){
          return h('div', { key:x.id, onClick: function(){ focus(x.id); } },
            [label(x), h('em', { key:'e' }, x.company_type || x.industry)]);
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
        })).concat([
          h('button', { key:'of', className:'chip' + (onlyOfficial ? ' on' : ''),
                        onClick: function(){ setOnlyOfficial(!onlyOfficial); } },
            '공식 출처만')]))
    ]),
    h('div', { key:'main', className:'main' }, [
      h('div', { key:'cv', className:'canvas' }, [
        h(RF, { key:'rf', nodes: graph.nodes, edges: graph.edges, nodeTypes: NODE_TYPES,
                fitView: true, fitViewOptions: { padding: 0.18 },
                minZoom: 0.2, maxZoom: 1.8,
                onEdgeClick: function(ev, e){ setSel({ kind:'rel', id: e.id }); },
                nodesDraggable: true, nodesConnectable: false }, [
          h(Background, { key:'bg', gap: 22, size: 1, color: '#dfe3ea' }),
          h(Controls, { key:'ct', showInteractive: false, position:'bottom-left' }),
          h(MiniMap, { key:'mm', pannable: true, zoomable: true,
                       nodeColor: function(n){ return n.data.isCenter ? '#39415a' : '#c9cfda'; } })
        ]),
        legend
      ]),
      h('div', { key:'sd', className:'side' }, body)
    ])
  ]);
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();
'''


def build():
    db = {}
    for t in TABLES:
        db[t] = json.load(io.open(os.path.join(DATA, t + '.json'), encoding='utf-8'))

    cids = set(c['id'] for c in db['companies'])
    rids = set(r['id'] for r in db['relationships'])
    sids = set(s['id'] for s in db['sources'])
    mids = set(m['id'] for m in db['relationship_metrics'])
    for r in db['relationships']:
        assert r['source_company_id'] in cids and r['target_company_id'] in cids, r['id']
    for m in db['relationship_metrics']:
        assert m['relationship_id'] in rids, m['id']
    for e in db['evidence']:
        assert e['relationship_id'] in rids and e['source_id'] in sids, e['id']
        assert e['metric_id'] is None or e['metric_id'] in mids, e['id']

    payload = json.dumps(db, ensure_ascii=False, separators=(',', ':'))
    scripts = '\n'.join('<script src="%s"></script>' % u for u in LIBS)
    html = (TEMPLATE
            .replace('__RFCSS__', RF_CSS)
            .replace('__CSS__', CSS)
            .replace('__SCRIPTS__', scripts)
            .replace('__DATA__', payload)
            .replace('__APP__', APP))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    return OUT, db


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p, db = build()
    print('%s\n회사 %d · 관계 %d · 지표 %d · 출처 %d · 근거 %d'
          % (p, len(db['companies']), len(db['relationships']),
             len(db['relationship_metrics']), len(db['sources']), len(db['evidence'])))
