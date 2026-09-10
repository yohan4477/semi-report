# -*- coding: utf-8 -*-
"""밸류체인 탐색기 — data/valuechain/*.json 다섯 장을 읽어 한 장짜리 HTML 로 굽는다.

원본은 JSON 다섯 장이다. HTML 은 생성물이니 손으로 고치지 않는다.
  companies.json             회사
  relationships.json         관계 (source 가 target 에게 준다). 숫자를 박지 않는다
  relationship_metrics.json  시점별 비중. 같은 관계에 기간을 계속 덧붙인다
  identity_hypotheses.json   익명 고객에 붙는 실명 후보. 확정치와 섞지 않는다
  sources.json               원문 메타데이터와 등급
  evidence.json              관계와 지표 각각에 붙는 근거
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')
TABLES = ['companies', 'relationships', 'relationship_metrics', 'sources', 'evidence',
          'identity_hypotheses']

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
body{background:var(--bg);color:var(--ink1);overflow:hidden;
font:14px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",sans-serif}
.app{display:flex;flex-direction:column;height:100%}
.top{display:flex;align-items:center;gap:10px;padding:8px 14px;position:relative;z-index:40;
background:var(--paper);border-bottom:1px solid var(--line)}
.brand{font-size:15px;font-weight:700;letter-spacing:-.2px;white-space:nowrap}
.brand small{display:block;font-size:11.5px;font-weight:400;color:var(--ink3)}
.brand a{color:var(--ink3);text-decoration:none;border-bottom:1px solid var(--line)}
.search{position:relative;flex:1;min-width:90px;max-width:320px}
.top .chips.wide-only{flex:1;overflow:hidden}
.wide-only{display:flex}
.narrow-only{display:none}
@media (max-width:1000px){.wide-only{display:none!important}.narrow-only{display:block}}
.search input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:6px;
font:inherit;font-size:13px;background:var(--paper);color:var(--ink1)}
.sug{position:absolute;z-index:30;top:38px;left:0;width:100%;min-width:230px;max-height:300px;
overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:6px}
.sug div{padding:8px 10px;cursor:pointer;font-size:13px;border-bottom:1px solid #f0f2f6}
.sug div:hover{background:var(--hi)}
.sug em{font-style:normal;color:var(--ink3);font-size:11.5px;margin-left:6px}
.sel{flex:none;max-width:132px;padding:8px 8px;border:1px solid var(--line);border-radius:6px;
background:var(--paper);font:inherit;font-size:12.5px;color:var(--ink2);cursor:pointer}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{padding:5px 10px;border:1px solid var(--line);border-radius:14px;background:var(--paper);
font:inherit;font-size:12.5px;color:var(--ink2);cursor:pointer;white-space:nowrap}
.chip:hover{background:var(--hi)}
.chip.on{background:var(--hiline);border-color:var(--hiline);color:#fff}
/* 필터 서랍 */
.drw{position:absolute;top:calc(100% + 6px);right:10px;z-index:45;padding:12px 14px 14px;
width:min(420px,calc(100vw - 20px));background:var(--paper);border:1px solid var(--line);
border-radius:8px}
.drw h4{margin:0 0 6px;font-size:11.5px;font-weight:600;color:var(--ink3);letter-spacing:.3px}
.drw .row{margin-bottom:12px}
.drw .row:last-child{margin-bottom:0}
.drwx{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.drwx b{font-size:13px}
.main{flex:1;display:flex;min-height:0;position:relative}
.canvas{flex:1;min-width:0;position:relative}
.side{width:380px;flex:none;background:var(--paper);border-left:1px solid var(--line);
overflow:auto;padding:16px 16px 40px}
.shx{display:none}
.side h2{font-size:17px;margin:0 0 2px;letter-spacing:-.2px}
.side .tk{font-size:12px;color:var(--ink3);margin-bottom:10px}
.side p{margin:0 0 12px;font-size:13px;color:var(--ink2)}
.side .rev{font-size:13px;font-weight:600;color:var(--ink1);margin-bottom:10px}
.side h3{font-size:12px;color:var(--ink3);margin:18px 0 6px;letter-spacing:.3px}
.side a{color:var(--ink2)}
.hint{font-size:11.5px;color:var(--ink3);margin:0 0 8px}
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
.tw{overflow-x:auto;margin:4px 0 10px}
table.m{border-collapse:collapse;width:100%;font-size:12.5px}
table.m th,table.m td{border-bottom:1px solid var(--line);padding:6px 6px;text-align:left;
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
.co{width:236px;background:var(--paper);border:1px solid var(--line);border-radius:7px;
padding:9px 11px;position:relative;cursor:pointer}
.co:hover{border-color:var(--ink4)}
.co.center{background:var(--hi);border-color:var(--hiline);border-width:1.6px}
.co.anon{background:#f4eef4;border-style:dashed}
.co .nm{font-size:13.5px;font-weight:600;line-height:1.4;padding-right:30px}
.co .ind{font-size:11px;color:var(--ink3);margin-top:3px;line-height:1.6}
.co .sh{display:inline-block;margin-top:6px;padding:1px 7px;border:1px solid var(--line);
border-radius:10px;background:var(--bg);font-size:11px;line-height:1.6;color:var(--ink2)}
.co .ex{position:absolute;top:7px;right:7px;min-width:22px;height:20px;padding:0 5px;
line-height:18px;text-align:center;border:1px solid var(--line);border-radius:5px;
background:var(--paper);font-size:11px;color:var(--ink3)}
.co .ex:hover{background:var(--hiline);color:#fff;border-color:var(--hiline)}
.react-flow__handle{opacity:0;width:1px;height:1px;min-width:0;min-height:0;border:0}
.react-flow__edge{cursor:pointer}
.react-flow__edge:hover .react-flow__edge-path{stroke:var(--hiline)!important}
.react-flow__edge.pick .react-flow__edge-path{stroke:var(--hiline)!important;
stroke-width:2.6!important}
.react-flow__controls{box-shadow:none;border:1px solid var(--line);border-radius:6px}
.react-flow__controls button{width:24px;height:24px}
.react-flow__attribution{font-size:9px;opacity:.5}
/* 범례 — 화면 세로를 먹지 않게 판 위에 얹는다 */
.lgd{position:absolute;z-index:6;right:8px;bottom:8px;max-width:calc(100% - 16px);
display:flex;align-items:center;gap:6px 14px;flex-wrap:wrap;padding:6px 10px;
background:rgba(255,255,255,.93);border:1px solid var(--line);border-radius:7px;
font-size:11.5px;color:var(--ink2)}
.lgd span{display:inline-flex;align-items:center;gap:6px}
.lgd b{font-weight:600;color:var(--ink1);font-size:11.5px}
.only-narrow{display:none}
@media (max-width:720px){.lgd{left:8px;right:8px;bottom:56px;justify-content:flex-start;font-size:11px;padding:5px 8px}}
@media (max-width:860px){
.main{display:block}
.canvas{position:absolute;top:0;left:0;right:0;bottom:0}
/* 옆판을 바닥 시트로 — 접으면 손잡이만 남고 판이 화면을 다 쓴다 */
.side{position:absolute;left:0;right:0;bottom:0;width:auto;height:46vh;
border-left:0;border-top:1px solid var(--line);padding:0 14px 30px;
transform:translateY(calc(100% - 43px));transition:transform .18s ease}
.side.up{transform:translateY(0)}
.shx{display:flex;position:sticky;top:0;z-index:2;width:100%;gap:10px;align-items:center;
justify-content:space-between;padding:11px 0;background:var(--paper);border:0;
border-bottom:1px solid var(--line);font:inherit;font-size:13px;font-weight:600;
color:var(--ink1);text-align:left;cursor:pointer}
.shx em{font-style:normal;font-weight:400;font-size:12px;color:var(--ink3);white-space:nowrap}
.side h2{font-size:16px}
.only-narrow{display:inline-block}
}
@media (max-width:720px){
.top{gap:8px;padding:7px 10px}
.brand{font-size:14px}
.brand small{display:none}
.chip{padding:5px 9px;font-size:12px}
.sel{max-width:104px;padding:8px 4px}
.drw{right:6px;left:6px;width:auto}
}
@media (max-width:420px){.brand{font-size:0}.brand:before{content:"밸류체인";font-size:14px}}
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
  if (e.hypothesis_id) return;
  if (e.metric_id) (EV_BY_MET[e.metric_id] = EV_BY_MET[e.metric_id] || []).push(e);
  else (EV_BY_REL[e.relationship_id] = EV_BY_REL[e.relationship_id] || []).push(e);
});
var HYP_BY_ANON = {}, EV_BY_HYP = {};
(DB.identity_hypotheses || []).forEach(function(x){
  (HYP_BY_ANON[x.anon_company_id] = HYP_BY_ANON[x.anon_company_id] || []).push(x);
});
DB.evidence.forEach(function(e){
  if (e.hypothesis_id) (EV_BY_HYP[e.hypothesis_id] = EV_BY_HYP[e.hypothesis_id] || []).push(e);
});

// 바로 가기 — 이름을 박지 않고 관계가 많은 회사 넷을 데이터에서 고른다
var QUICK = (function(){
  var deg = {};
  DB.relationships.forEach(function(r){
    deg[r.source_company_id] = (deg[r.source_company_id] || 0) + 1;
    deg[r.target_company_id] = (deg[r.target_company_id] || 0) + 1;
  });
  var rest = Object.keys(deg).filter(function(id){
    return CO[id] && !CO[id].anon && id !== 'nvidia';
  }).sort(function(a, b){ return deg[b] - deg[a]; });
  return (CO['nvidia'] ? ['nvidia'] : []).concat(rest).slice(0, 4);
})();

var PERIODS = (function(){
  var e = {}, st = {};
  DB.relationship_metrics.forEach(function(m){
    if (!e[m.period] || m.period_end > e[m.period]) e[m.period] = m.period_end;
    if (!st[m.period] || m.period_start < st[m.period]) st[m.period] = m.period_start;
  });
  return Object.keys(e).sort(function(a, b){
    if (e[a] !== e[b]) return e[a] < e[b] ? -1 : 1;
    return st[a] > st[b] ? -1 : 1;   // 같은 날 끝나면 긴 쪽을 뒤에
  });
})();
var LATEST = PERIODS[PERIODS.length - 1];

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
  receivables_share: '매출채권 비중', supply_share: '공급 점유',
  revenue_share: '매출 비중', commitment_value: '약정 총액',
  guarantee_cap: '보증 상한', supplier_purchase_share: '매입액 비중',
  investment_value: '투자 금액', contract_value: '계약 금액' };
function metName(k){ return MET_LABEL[k] || k; }
var HYP_STATUS = { estimated: '추정', confirmed: '확인됨', rejected: '기각' };
function stars(v){
  var n = Math.round((v || 0) * 2) / 2, out = '';
  for (var i = 1; i <= 5; i++) out += (n >= i ? '★' : (n >= i - 0.5 ? '☆' : '·'));
  return out;
}
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
  }, '+' + d.hidden));
  return h('div', { className: cls, onClick: function(){ d.onOpen(c.id); } }, kids);
}
var NODE_TYPES = { co: CoNode };

// ── 배치 ──────────────────────────────────────────────────────────
var NODE_W = 236;
function place(nodes, edges){
  var g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(function(){ return {}; });
  g.setGraph({ rankdir:'LR', nodesep:18, ranksep:112, marginx:20, marginy:20 });
  nodes.forEach(function(n){ g.setNode(n.id, { width:NODE_W, height:n.__h }); });
  edges.forEach(function(e){ g.setEdge(e.source, e.target); });
  dagre.layout(g);
  return nodes.map(function(n){
    var p = g.node(n.id);
    return Object.assign({}, n, { position: { x: p.x - NODE_W / 2, y: p.y - n.__h / 2 } });
  });
}

// ── 앱 ────────────────────────────────────────────────────────────
function App(){
  var HOME = CO['nvidia'] ? 'nvidia' : QUICK[0];
  var s0 = useState(HOME), center = s0[0], setCenter = s0[1];
  var s1 = useState({}), open = s1[0], setOpen = s1[1];
  var s2 = useState({ kind:'co', id: HOME }), sel = s2[0], setSelRaw = s2[1];
  var s3 = useState(''), q = s3[0], setQ = s3[1];
  var s4 = useState(LATEST), perOne = s4[0], setPerOne = s4[1];
  var s5 = useState(['high','medium','low']), conf = s5[0], setConf = s5[1];
  var s6 = useState(false), onlyOfficial = s6[0], setOnlyOfficial = s6[1];
  var s7 = useState(false), drawer = s7[0], setDrawer = s7[1];
  var s8 = useState(false), sheet = s8[0], setSheet = s8[1];

  var per = perOne ? [perOne] : PERIODS;
  // 좁은 화면에서는 무엇을 눌렀든 바닥 시트가 따라 올라온다
  function setSel(v){ setSelRaw(v); setSheet(true); }

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
        type: 'smoothstep', style: CONF_STYLE[r.confidence], interactionWidth: 26,
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
        if (m && !sh && m.unit === '%') sh = m.value + '% · ' + metName(m.metric);
      });
      down(id).forEach(function(r){ total++; if (keep[r.target_company_id]) shown++; });
      var lines = label(c).length > 13 ? 2 : 1;
      return {
        id: id, type: 'co', position: { x:0, y:0 },
        __h: 18 + lines * 19 + 21 + (sh ? 28 : 0),
        data: { co: c, isCenter: id === center, share: sh, hidden: total - shown,
                onOpen: function(x){ setSel({ kind:'co', id:x }); },
                onExpand: function(x){ setOpen(function(o){
                  var n = Object.assign({}, o); n[x] = 1; return n; }); } }
      };
    });
    return { nodes: place(nds, eds), edges: eds };
  }, [center, open, rels, perOne]);

  // 고른 선은 굵게 — 옆판이 어느 선을 풀고 있는지 보이게 한다
  var edges = useMemo(function(){
    return graph.edges.map(function(e){
      return (sel.kind === 'rel' && sel.id === e.id)
        ? Object.assign({}, e, { className:'pick' }) : e;
    });
  }, [graph, sel]);

  function focus(id){
    setCenter(id); setOpen({}); setSel({ kind:'co', id:id }); setQ(''); setDrawer(false);
  }

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
      // 좁은 판에서 글자가 뭉개지지 않게 표는 세 칸만 쓰고
      // 나머지(무엇의 비중인가·어떻게 얻었나)는 기간별 설명 줄로 내린다
      kids.push(h('div', { key:'tw', className:'tw' },
        h('table', { className:'m' }, [
        h('thead', { key:'h' }, h('tr', null, [
          h('th', { key:'1' }, '기간'), h('th', { key:'2' }, '지표'),
          h('th', { key:'3' }, '값')])),
        h('tbody', { key:'b' }, ms.map(function(m){
          return h('tr', { key:m.id }, [
            h('td', { key:'1' }, m.period),
            h('td', { key:'2' }, metName(m.metric)),
            h('td', { key:'3', className:'n' }, m.value + m.unit)]);
        }))])));
      ms.forEach(function(m){
        kids.push(h('div', { key:'bs'+m.id, className:'meth' },
          m.period + ' — ' + m.basis + ' 에 대한 비중, ' +
          (EST_LABEL[m.estimate_type] || m.estimate_type) +
          (m.method ? '. 계산은 ' + m.method : '')));
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
      c.anon ? h('h3', { key:'hy' }, '실명 후보 ' + (HYP_BY_ANON[c.id] || []).length) : null,
      (c.anon && (HYP_BY_ANON[c.id] || []).length)
        ? (HYP_BY_ANON[c.id] || []).slice().sort(function(a, b){
            return (b.likelihood || 0) - (a.likelihood || 0); }).map(function(x){
            var cand = CO[x.candidate_company_id];
            var kids2 = [
              h('b', { key:'b' }, label(cand)),
              h('span', { key:'s' }, stars(x.likelihood) + ' · ' +
                (HYP_STATUS[x.status] || x.status) + ' · ' + x.period)
            ];
            if (x.method) kids2.push(h('span', { key:'m', style:{ display:'block' } }, x.method));
            return h('div', { key:x.id, className:'rel',
                              onClick: function(){ setSel({ kind:'co', id:cand.id }); } }, kids2);
          })
        : (c.anon ? h('div', { key:'ey', className:'empty' }, '아직 후보를 세우지 않았다') : null),
      h('h3', { key:'hu' }, '공급받는 곳 ' + ups.length),
      (ups.length || dws.length)
        ? h('div', { key:'ht', className:'hint' }, '한 줄을 누르면 그 관계의 숫자와 근거가 열린다')
        : null,
      ups.length ? ups.map(function(r){ return row(r, r.source_company_id, 'u'); })
                 : h('div', { key:'eu', className:'empty' }, '데이터에 없다'),
      h('h3', { key:'hd' }, '공급하는 곳 ' + dws.length),
      dws.length ? dws.map(function(r){ return row(r, r.target_company_id, 'd'); })
                 : h('div', { key:'ed', className:'empty' }, '데이터에 없다')
    ];
    return kids;
  }

  var selRel = sel.kind === 'rel' && REL[sel.id] ? REL[sel.id] : null;
  var selCo = selRel ? null : (CO[sel.id] || CO[center]);
  var body = selRel ? edgePanel(selRel) : coPanel(selCo);
  var sheetTitle = selRel
    ? (label(CO[selRel.source_company_id]) + ' → ' + label(CO[selRel.target_company_id]))
    : label(selCo);

  function svgLine(k){
    var st = CONF_STYLE[k];
    return h('svg', { key:'s'+k, width:30, height:8 },
      h('line', { x1:0, y1:4, x2:30, y2:4, stroke:st.stroke,
                  strokeWidth:st.strokeWidth, strokeDasharray:st.strokeDasharray }));
  }
  var legend = h('div', { key:'lg', className:'lgd' }, [
    h('b', { key:'b' }, '선을 누르면 근거가 열린다'),
    h('span', { key:'1' }, [svgLine('high'), '공시가 양쪽을 잇는다']),
    h('span', { key:'2' }, [svgLine('medium'), '한쪽 공시만 있거나 고객이 익명이다']),
    h('span', { key:'3' }, [svgLine('low'), '추정이다'])
  ]);

  // 걸어 둔 필터 수 — 서랍을 닫아 두어도 무엇이 켜졌는지 보이게 한다
  var nFilter = (conf.length < 3 ? 1 : 0) + (onlyOfficial ? 1 : 0);
  var drawer_ = drawer ? h('div', { key:'dw', className:'drw' }, [
    h('div', { key:'x', className:'drwx' }, [
      h('b', { key:'t' }, '무엇을 보여줄까'),
      h('button', { key:'c', className:'chip',
                    onClick: function(){ setDrawer(false); } }, '닫기')
    ]),
    h('div', { key:'j', className:'row narrow-only' }, [
      h('h4', { key:'h' }, '바로 가기'),
      h('div', { key:'c', className:'chips' }, QUICK.map(function(id){
        return h('button', { key:id, className:'chip' + (center === id ? ' on' : ''),
                             onClick: function(){ focus(id); } }, label(CO[id]));
      }))
    ]),
    h('div', { key:'g', className:'row' }, [
      h('h4', { key:'h' }, '근거의 세기'),
      h('div', { key:'c', className:'chips' },
        ['high','medium','low'].map(function(k){
          return h('button', { key:k, className:'chip' + (conf.indexOf(k) >= 0 ? ' on' : ''),
                               onClick: function(){ toggle(conf, k, setConf); } },
                   CONF_LABEL[k]);
        }).concat([
          h('button', { key:'of', className:'chip' + (onlyOfficial ? ' on' : ''),
                        onClick: function(){ setOnlyOfficial(!onlyOfficial); } },
            '공식 출처만')]))
    ])
  ]) : null;

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
      h('div', { key:'qk', className:'chips wide-only' }, QUICK.map(function(id){
        return h('button', { key:id, className:'chip' + (center === id ? ' on' : ''),
                             onClick: function(){ focus(id); } }, label(CO[id]));
      })),
      h('select', { key:'pd', className:'sel', value:perOne, title:'어느 시점의 숫자를 볼까',
                    onChange: function(e){ setPerOne(e.target.value); } },
        [h('option', { key:'all', value:'' }, '기간 전체')].concat(
        PERIODS.slice().reverse().map(function(p){
          return h('option', { key:p, value:p }, p);
        }))),
      h('button', { key:'ft', className:'chip' + (drawer || nFilter ? ' on' : ''),
                    onClick: function(){ setDrawer(!drawer); } },
        nFilter ? '필터 ' + nFilter : '필터'),
      drawer_
    ]),
    h('div', { key:'main', className:'main',
               onClick: function(){ if (drawer) setDrawer(false); } }, [
      h('div', { key:'cv', className:'canvas' }, [
        h(RF, { key:'rf', nodes: graph.nodes, edges: edges, nodeTypes: NODE_TYPES,
                // 다 담으려다 글자가 뭉개진다. 읽히는 배율을 바닥으로 두고
                // 나머지는 밀어서 본다 — 전체는 아래 맞춤 단추로 돌아온다
                fitView: true,
                fitViewOptions: { padding: 0.12, minZoom: 0.5, maxZoom: 1 },
                minZoom: 0.2, maxZoom: 2.2,
                onEdgeClick: function(ev, e){ setSel({ kind:'rel', id: e.id }); },
                onInit: function(inst){
                  // 좁은 화면에서는 중심 회사를 왼쪽으로 밀어 고객 쪽을 먼저 보여준다
                  if (window.innerWidth > 720) return;
                  var n = graph.nodes.filter(function(x){ return x.id === center; })[0];
                  if (!n) return;
                  var z = 0.62;
                  inst.setCenter(n.position.x + NODE_W / 2 + window.innerWidth * 0.2 / z,
                                 n.position.y + n.__h / 2, { zoom: z });
                },
                nodesDraggable: true, nodesConnectable: false }, [
          h(Background, { key:'bg', gap: 22, size: 1, color: '#dfe3ea' }),
          h(Controls, { key:'ct', showInteractive: false, position:'bottom-right' }),
          null
        ]),
        legend
      ]),
      h('div', { key:'sd', className:'side' + (sheet ? ' up' : '') }, [
        h('button', { key:'hd', className:'shx',
                      onClick: function(e){ e.stopPropagation(); setSheet(!sheet); } }, [
          h('span', { key:'t' }, sheetTitle),
          h('em', { key:'e' }, sheet ? '내리기' : '자세히 보기')
        ])
      ].concat(body))
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
    hids = set(x['id'] for x in db['identity_hypotheses'])
    for x in db['identity_hypotheses']:
        assert x['anon_company_id'] in cids and x['candidate_company_id'] in cids, x['id']
    for e in db['evidence']:
        # 가설에만 붙는 근거는 관계를 갖지 않는다
        assert e['relationship_id'] is None or e['relationship_id'] in rids, e['id']
        assert e['source_id'] in sids, e['id']
        assert e['relationship_id'] or e.get('hypothesis_id'), e['id']
        assert e['metric_id'] is None or e['metric_id'] in mids, e['id']
        assert e.get('hypothesis_id') is None or e['hypothesis_id'] in hids, e['id']

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
