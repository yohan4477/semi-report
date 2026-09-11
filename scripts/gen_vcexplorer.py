# -*- coding: utf-8 -*-
"""밸류체인 탐색기 — data/valuechain 을 읽어 한 장짜리 HTML 로 굽는다.

원본은 JSON 이다. HTML 은 생성물이니 손으로 고치지 않는다.
  entities.json / sources.json / methods.json        전역
  chains/<사슬>/relationships.json                    지속적인 관계. 숫자를 박지 않는다
  chains/<사슬>/observations.json                     시점별 값. 분모·기준일·근거등급이 붙는다
  chains/<사슬>/claims.json · hypotheses.json
  chains/<사슬>/bom/*.json · financials/*.json

어느 회사도 코드에 박지 않는다. 시작 회사는 관계가 가장 많은 엔티티에서 고른다.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')

# 화면에 싣는 사슬. 구조는 여러 사슬을 받지만 지금 내보내는 것은 이 하나다
SHIP = ['bloom-energy']

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
:root{--paper:#fff;--ink1:#151b28;--ink2:#39415a;--ink3:#6b7488;--ink4:#9aa2b1;
--line:#c6ccd8;--line2:#e5e8ee;--bg:#e8ebf0;--hi:#dde6f4;--warm:#8a6a3d}
*{box-sizing:border-box}
html,body,#root{height:100%;margin:0}
body{background:var(--bg);color:var(--ink1);overflow:hidden;
font:13.5px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",sans-serif;
font-variant-numeric:tabular-nums}
.app{display:flex;flex-direction:column;height:100%}
.top{display:flex;align-items:center;gap:12px;padding:9px 14px;background:var(--paper);
border-bottom:1px solid var(--line);position:relative;z-index:40;flex-wrap:wrap}
.brand{font-size:14.5px;font-weight:700;letter-spacing:-.2px;white-space:nowrap}
.brand small{display:block;font-size:11px;font-weight:400;color:var(--ink3)}
.search{position:relative;flex:1;min-width:150px;max-width:330px}
.search input{width:100%;padding:7px 10px;border:1px solid var(--line);border-radius:5px;
font:inherit;font-size:13px;background:var(--paper);color:var(--ink1)}
.search input:focus{outline:none;border-color:var(--ink3)}
.sug{position:absolute;top:36px;left:0;right:0;background:var(--paper);
border:1px solid var(--line);border-radius:5px;max-height:320px;overflow:auto;z-index:60;
box-shadow:0 8px 24px rgba(20,26,40,.1)}
.sug div{padding:7px 10px;cursor:pointer;font-size:12.5px;border-bottom:1px solid var(--line2)}
.sug div:hover{background:var(--hi)}
.sug .k{color:var(--ink3);font-size:11px;margin-left:6px}
.modes{display:flex;border:1px solid var(--line);border-radius:5px;overflow:hidden}
.modes button{border:0;background:var(--paper);color:var(--ink2);padding:6px 11px;
font:inherit;font-size:12.5px;cursor:pointer;border-right:1px solid var(--line)}
.modes button:last-child{border-right:0}
.modes button.on{background:var(--ink1);color:#fff}
.spacer{flex:1}
.btn{border:1px solid var(--line);background:var(--paper);color:var(--ink2);
padding:6px 10px;border-radius:5px;font:inherit;font-size:12.5px;cursor:pointer}
.btn.on{background:var(--ink1);color:#fff;border-color:var(--ink1)}
.crumb{display:flex;align-items:center;gap:6px;padding:6px 14px;background:var(--paper);
border-bottom:1px solid var(--line);font-size:12px;color:var(--ink3);overflow-x:auto;
white-space:nowrap}
.crumb b{color:var(--ink1);font-weight:600}
.crumb span{cursor:pointer}
.crumb span:hover{text-decoration:underline}
.scrub{display:flex;align-items:center;gap:0;padding:7px 14px;background:var(--paper);
border-bottom:1px solid var(--line);overflow-x:auto;user-select:none;cursor:ew-resize;
touch-action:pan-y}
.scrub:focus{outline:none;box-shadow:inset 0 0 0 1px var(--line)}
.scrub .yr{position:relative;padding:4px 16px;font-size:12.5px;color:var(--ink3);
cursor:pointer;white-space:nowrap;border-bottom:2px solid transparent}
.scrub .yr.on{color:var(--ink1);font-weight:700;border-bottom-color:var(--ink1)}
.scrub .rail{flex:1;height:1px;background:var(--line);min-width:10px}
.main{flex:1;display:flex;min-height:0;position:relative}
.canvas{flex:1;min-width:0;position:relative}
.drw{width:30%;min-width:280px;max-width:420px;flex:0 0 auto;background:var(--paper);
border-left:1px solid var(--line);overflow:auto;padding:14px 16px 40px}
.drw h3{margin:0 0 2px;font-size:15px}
.drw .role{color:var(--ink3);font-size:12px;margin-bottom:12px}
.drw section{border-top:1px solid var(--line2);padding:10px 0}
.drw .k{color:var(--ink3);font-size:11.5px}
.drw .v{font-size:13px;margin-bottom:7px}
.drw a{color:var(--ink2)}
.rowk{display:grid;grid-template-columns:92px 1fr;gap:4px 10px;font-size:12.5px}
.rowk div:nth-child(odd){color:var(--ink3)}
.badge{display:inline-block;padding:1px 6px;border:1px solid var(--line);border-radius:3px;
font-size:11px;color:var(--ink2);margin-right:4px;background:var(--paper)}
.badge.est{border-color:var(--warm);color:var(--warm)}
.badge.new{border-color:var(--ink1);color:#fff;background:var(--ink1)}
.steps{border:1px solid var(--line2);border-radius:5px;padding:8px 10px;background:var(--bg)}
.steps div{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;
padding:2px 0;border-bottom:1px dashed var(--line2)}
.steps div:last-child{border-bottom:0;font-weight:600}
table.t{border-collapse:collapse;width:100%;font-size:12.5px}
table.t th,table.t td{border-bottom:1px solid var(--line2);padding:5px 6px;text-align:left;
vertical-align:top}
table.t th{color:var(--ink3);font-weight:500;font-size:11.5px}
.pane{flex:1;overflow:auto;padding:16px 20px 60px;background:var(--paper)}
.steps{background:#f4f6fa}
.pane h2{font-size:15px;margin:0 0 4px}
.pane p.note{color:var(--ink3);font-size:12px;margin:0 0 14px}
.sw{border-collapse:collapse;width:100%;font-size:12.5px}
.sw th{font-weight:500;color:var(--ink3);font-size:11.5px;padding:4px 8px;text-align:center;
border-bottom:1px solid var(--line)}
.sw th:first-child{text-align:left;width:230px}
.sw td{padding:5px 8px;text-align:center;border-bottom:1px solid var(--line2)}
.sw td:first-child{text-align:left;color:var(--ink1)}
.sw td small{color:var(--ink3)}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--ink2)}
.dot.o{display:inline-block;width:9px;height:9px;border-radius:50%;background:transparent;
border:1px solid var(--ink4)}
.bom{display:flex;height:34px;border:1px solid var(--line);border-radius:4px;overflow:hidden;
margin:10px 0 6px}
.bom div{border-right:1px solid var(--paper);cursor:pointer}
.bom div:last-child{border-right:0}
.bomleg{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--ink2)}
.bomleg span.it{display:flex;align-items:center;gap:5px;cursor:pointer}
.sq{width:10px;height:10px;border-radius:2px;display:inline-block}
.nd{background:var(--paper);border:1px solid #aab2c2;border-radius:6px;padding:7px 10px;
min-width:118px;max-width:196px;box-shadow:0 1px 3px rgba(20,26,40,.14);cursor:pointer}
.nd .nm{font-size:12.5px;font-weight:600;line-height:1.35}
.nd .sub{font-size:11px;color:var(--ink3);margin-top:2px}
.nd.focal{border-color:var(--ink1);border-width:1.8px;background:#fff;
box-shadow:0 2px 8px rgba(20,26,40,.2)}
.nd.grp{background:#f4f6fa;border-style:dashed;border-color:#9aa3b5}
.nd.dim{opacity:.28}
.nd.gone{opacity:.32;border-style:dotted}
.legend{display:flex;flex-wrap:wrap;align-items:center;gap:4px 16px;padding:6px 14px;
background:var(--paper);border-top:1px solid var(--line);font-size:11.5px;color:var(--ink3)}
.legend b{font-size:11px;color:var(--ink4);font-weight:500}
.legend i{font-style:normal;white-space:nowrap}
@media (max-width:720px){
  .main{flex-direction:column}
  .canvas{flex:1 1 auto;min-height:44vh}
  .drw{width:100%;max-width:none;min-width:0;flex:0 0 52%;border-left:0;
       border-top:1px solid var(--line);box-shadow:0 -6px 18px rgba(20,26,40,.1);
       padding:10px 14px 28px}
  .drw h3{font-size:14.5px}
  .legend{display:none}
  .scrub{padding:7px 10px}
  .sw th:first-child{width:auto}
  .top{gap:8px;padding:8px 10px}
  .brand small{display:none}
}
'''

APP = u'''
(function(){
var h = React.createElement;
var RFlib = window.ReactFlow;
var RF = RFlib.default || RFlib.ReactFlow;
var Background = RFlib.Background, Controls = RFlib.Controls;
var Handle = RFlib.Handle, Position = RFlib.Position, MarkerType = RFlib.MarkerType;
var useState = React.useState, useMemo = React.useMemo, useEffect = React.useEffect;

var DB = window.__VC__;
var ENT = DB.entities, SRC = DB.sources, METH = DB.methods, CHAINS = DB.chains;

// ── 색인 ────────────────────────────────────────────────────────────
var REL = {}, OBS_BY_REL = {}, REL_BY_ENT = {}, CHAIN_OF = {};
Object.keys(CHAINS).forEach(function(ck){
  var c = CHAINS[ck];
  c.relationships.forEach(function(r){
    REL[r.id] = r; CHAIN_OF[r.id] = ck;
    (REL_BY_ENT[r.source_entity] = REL_BY_ENT[r.source_entity] || []).push(r.id);
    (REL_BY_ENT[r.target_entity] = REL_BY_ENT[r.target_entity] || []).push(r.id);
  });
  (c.observations || []).forEach(function(o){
    (OBS_BY_REL[o.relationship_id] = OBS_BY_REL[o.relationship_id] || []).push(o);
  });
});
function relsOf(id){
  var seen = {}, out = [];
  (REL_BY_ENT[id] || []).forEach(function(rid){
    if (seen[rid]) return; seen[rid] = 1; out.push(REL[rid]);
  });
  return out;
}
function nm(id){ var e = ENT[id]; return e ? (e.name_ko || e.name) : id; }

var YEARS = (function(){
  var s = {};
  Object.keys(CHAINS).forEach(function(ck){
    // 값을 「알게 된 시점」으로 축을 세운다. 계약 종료일이 미래라고 그 해가 생기지 않는다
    (CHAINS[ck].observations || []).forEach(function(o){
      var d = o.as_of_date || o.period_end || '';
      if (d) s[d.slice(0, 4)] = 1;
    });
  });
  return Object.keys(s).sort();
})();
var NOW = YEARS[YEARS.length - 1];

var HOME = (function(){
  var best = null, n = -1;
  Object.keys(REL_BY_ENT).forEach(function(id){
    if (REL_BY_ENT[id].length > n) { n = REL_BY_ENT[id].length; best = id; }
  });
  return best;
})();

var EV_KO = { CONFIRMED:'공시로 확인', ESTIMATED:'추정', INFERRED:'정황 추론',
  UNDISCLOSED:'비공개', HISTORICAL_CURRENT_UNKNOWN:'과거 관측·현재 미상' };
var EV_STYLE = {
  CONFIRMED: { stroke:'#5b6377', strokeWidth:1.8 },
  ESTIMATED: { stroke:'#8a6a3d', strokeWidth:1.5 },
  INFERRED:  { stroke:'#8b93a5', strokeWidth:1.4, strokeDasharray:'6 4' },
  UNDISCLOSED:{ stroke:'#b6bcc7', strokeWidth:1.2, strokeDasharray:'2 4' },
  HISTORICAL_CURRENT_UNKNOWN:{ stroke:'#c2c7d1', strokeWidth:1.2, strokeDasharray:'1 5' }
};
function evStyle(k){ return EV_STYLE[k] || EV_STYLE.INFERRED; }
var SUB_KO = { 'Raw material':'원재료', 'Operational input':'운영 투입',
  'Cell':'셀·세라믹', 'Other ceramic':'기타 세라믹', 'Thermal':'열·단열',
  'Interconnect':'인터커넥트', 'Hotbox':'핫박스', 'Power electronics':'전력 전자',
  'Mechanical':'기계·모듈', 'Instrumentation':'계측',
  'Manufacturing equipment':'제조 장비', 'Site electrical BoP':'부지 전기',
  'Financing':'금융', 'EPC / Distribution':'EPC·유통', 'Utility':'유틸리티',
  'Data center':'데이터센터', 'C&I':'산업·상업 고객', 'Project':'프로젝트',
  'Undisclosed customer':'미상 고객', 'Assembly':'조립', 'Integrator':'통합' };
function subKo(k){ return SUB_KO[k] || k; }
var TIER_KO = { CONTRACTUAL_CUSTOMER:'계약 상대', INTERMEDIARY:'중개',
  PROJECT:'프로젝트·부지', END_USER:'최종 사용자',
  REVENUE_TYPE:'매출원', RAW_MATERIAL:'원재료', MATERIAL_PROCESSING:'소재·가공',
  COMPONENT_SUPPLIER:'부품 공급', SUBSYSTEM_MODULE:'계통·모듈' };
function tierOf(r, up){ return up ? r.source_tier : r.target_tier; }
// 05 §4 — 첫 화면은 제품 BOM 계통 다섯을 앞에 세우고 다른 lane 은 뒤로 뺀다
var CAT_ORDER = ['Cell', 'Interconnect', 'Hotbox', 'Power electronics', 'Mechanical',
  'Other ceramic', 'Thermal', 'Instrumentation', 'Raw material', 'Material processing',
  'Manufacturing equipment', 'Site electrical BoP', 'Operational input'];
var DOWN_ORDER = ['Financing', 'EPC / Distribution', 'Utility', 'Data center', 'C&I',
  'Project', 'Undisclosed customer', 'Assembly'];
function ordOf(g){
  var a = (g.up ? CAT_ORDER : DOWN_ORDER).indexOf(g.key);
  return (a < 0 ? 90 : a) + (g.up ? 0 : 0);
}
var LANE_KO = { MANUFACTURING_BOM:'제품 BOM', MANUFACTURING_EQUIPMENT:'제조 장비',
  SITE_ELECTRICAL_BOP:'부지 전기', OPERATIONAL_INPUT:'운영 투입',
  DOWNSTREAM:'다운스트림', CORPORATE:'기업 구조' };
var MET_KO = { sourcing_share:'조달 점유율', sourcing_volume_share:'물량 점유율',
  capacity_volume_share:'설비 기준 점유율', customer_revenue_share:'고객 매출 비중',
  contract_value:'계약 금액', cumulative_orders:'누적 수주', content_per_mw:'1MW 당 값',
  supplier_capacity:'공급사 생산 능력', agreement_capacity_max:'계약 상한',
  initial_order_capacity:'초기 주문', contracted_capacity:'계약·배치 용량',
  relationship_capacity:'관계 용량', planned_capacity:'계획 용량',
  project_capacity:'프로젝트 용량', financing_framework:'금융 프레임워크',
  revenue_share:'매출 비중', receivables_share:'매출채권 비중',
  supplier_purchase_share:'매입액 비중', supply_share:'공급 점유',
  commitment_value:'약정 총액', guarantee_cap:'보증 상한', investment_value:'투자 금액' };
function metKo(k){ return MET_KO[k] || k; }
var PCT = { 'percent':1, '%':1 };

function y4(d){ return d ? parseInt(d.slice(0, 4), 10) : null; }
function activeIn(r, yr){
  var y = parseInt(yr, 10), f = y4(r.valid_from), t = y4(r.valid_to);
  if (r.status === 'ENDED' && !t) return false;   // 끝난 관계인데 언제 끝났는지 모른다
  if (f && y < f) return false;
  if (t && y > t) return false;
  return true;
}
function endedOpen(r){ return r.status === 'ENDED' && !y4(r.valid_to); }
function firstYear(r){ var f = y4(r.valid_from); return f ? String(f) : null; }
function obsIn(rid, yr){
  var y = parseInt(yr, 10);
  return (OBS_BY_REL[rid] || []).filter(function(o){
    var a = y4(o.period_start) || y4(o.as_of_date), b = y4(o.period_end) || y4(o.as_of_date);
    return a <= y && y <= b;
  });
}
function onEdge(o){ return (o.denominator_scope || 'EDGE') === 'EDGE'; }
function shareIn(rid, yr){
  var os = obsIn(rid, yr).filter(function(o){ return PCT[o.unit] && onEdge(o); });
  return os.length ? os[0] : null;
}
function hasShareEver(rid){
  return (OBS_BY_REL[rid] || []).some(function(o){ return PCT[o.unit] && onEdge(o); });
}
function fmt(v){
  if (v === null || v === undefined) return '?';
  return (Math.round(v * 1000) / 1000).toLocaleString('en-US');
}
function shareLabel(rid, yr){
  var o = shareIn(rid, yr);
  if (!o) return hasShareEver(rid) ? '?' : null;
  if (o.value === null || o.value === undefined) return '?';
  if (o.value_low !== null && o.value_low !== undefined)
    return o.value_low + '~' + o.value_high + '%';
  return fmt(o.value) + '%';
}

// ── 노드 ────────────────────────────────────────────────────────────
function Nd(p){
  var d = p.data;
  var cls = 'nd' + (d.kind === 'grp' ? ' grp' : '') + (d.focal ? ' focal' : '')
          + (d.dim ? ' dim' : '') + (d.gone ? ' gone' : '');
  return h('div', { className: cls }, [
    h(Handle, { key:'t', type:'target', position:Position.Left, style:{opacity:0} }),
    h('div', { key:'n', className:'nm' }, d.title),
    (d.sub || d.isNew) ? h('div', { key:'s', className:'sub' }, [
      d.sub ? h('span', { key:'t2' }, d.sub) : null,
      d.isNew ? h('span', { key:'b', className:'badge new',
        style:{ marginLeft: d.sub ? '5px' : 0 } }, 'NEW') : null
    ]) : null,
    h(Handle, { key:'s2', type:'source', position:Position.Right, style:{opacity:0} })
  ]);
}
var NODE_TYPES = { nd: Nd };

function place(nodes, edges){
  var g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir:'LR', nodesep:22, ranksep:96, marginx:24, marginy:24 });
  g.setDefaultEdgeLabel(function(){ return {}; });
  nodes.forEach(function(n){
    var d = n.data;
    // 제목 줄수(한 줄 15자 남짓) + 부제 한 줄 + 테두리·여백
    var lines = Math.ceil((d.title || '').length / 14) || 1;
    var hgt = 16 + lines * 18 + ((d.sub || d.isNew) ? 17 : 0);
    g.setNode(n.id, { width:176, height:hgt });
  });
  edges.forEach(function(e){ g.setEdge(e.source, e.target); });
  dagre.layout(g);
  return nodes.map(function(n){
    var p = g.node(n.id);
    return Object.assign({}, n, { position:{ x:p.x - 88, y:p.y - 19 } });
  });
}

function readUrl(first){
  var q = new URLSearchParams(location.search);
  // 처음 열 때는 늘 가장 최신 해다. 주소에 옛 해가 남아 있어도 최신으로 연다.
  // 앱 안에서 오간 뒤(뒤로 가기)에는 그때 보던 해를 지킨다
  var y = q.get('year');
  if (first && !history.state) y = NOW;
  if (YEARS.indexOf(y) < 0) y = NOW;
  return { focal: q.get('focal') || HOME, year: y,
           mode: q.get('mode') || 'current',
           open: (q.get('open') || '').split(',').filter(Boolean),
           sel: q.get('sel') || '' };
}
function writeUrl(s, push){
  var q = new URLSearchParams();
  q.set('focal', s.focal); q.set('year', s.year);
  if (s.mode && s.mode !== 'current') q.set('mode', s.mode);
  if (s.open && s.open.length) q.set('open', s.open.join(','));
  if (s.sel) q.set('sel', s.sel);
  var u = location.pathname + '?' + q.toString();
  if (push) history.pushState(s, '', u); else history.replaceState(s, '', u);
}

// ── 그래프 ──────────────────────────────────────────────────────────
// 모든 해를 합쳐 자리를 잡고, 그 해에 없는 것은 흐리게 둔다. 연도를 옮겨도 자리가 안 튄다
// 상대 노드 하나와 그 관계선. host 쪽이 중심에 가까운 칸이다.
// 같은 회사가 사슬 여러 갈래에 나오면 노드를 하나로 합치고 선만 더한다.
// 반환값은 그 회사가 앉은 노드 id 다
function addRelNode(ctx, r, nid, host, up, year){
  var eid = up ? r.source_entity : r.target_entity;
  var have = ctx.byEnt[eid];
  if (!have) {
    var on0 = activeIn(r, year), fy0 = firstYear(r);
    ctx.nodes.push({ id: nid, type:'nd', data:{ title: nm(eid), kind:'ent',
      sub: TIER_KO[tierOf(r, up)] || r.component || null, gone: !on0,
      isNew: on0 && fy0 === year && fy0 !== YEARS[0],
      ref:{ kind:'rel', id:r.id, entity: eid } } });
    ctx.byEnt[eid] = nid;
    have = nid;
  }
  var eidge = 'e-' + r.id + '-' + host;
  if (ctx.edges.some(function(x){ return x.id === eidge; })) return have;
  var on = activeIn(r, year);
  ctx.edges.push({ id: eidge, source: up ? have : host, target: up ? host : have,
    label: shareLabel(r.id, year), labelStyle:{ fontSize:10.5 },
    labelBgStyle:{ fill:'#fff' }, labelBgPadding:[3,1],
    style: Object.assign({}, evStyle(r.evidence_level), on ? {} : { opacity:.35 }),
    markerEnd:{ type: MarkerType.ArrowClosed, width:13, height:13,
                color: evStyle(r.evidence_level).stroke },
    type:'smoothstep' });
  return have;
}

// 판매 사슬은 층이 있다 — 계약 상대 → 중개 → 프로젝트 → 최종 사용자.
// 층 수를 미리 정하지 않고 데이터에 있는 만큼만 따라간다
function chainDown(ctx, eid, host, year, depth, seen){
  if (depth > 2 || seen[eid]) return;
  seen[eid] = 1;
  relsOf(eid).forEach(function(r){
    if (r.source_entity !== eid || r.lane !== 'DOWNSTREAM') return;
    var nid = addRelNode(ctx, r, 'x|' + r.target_entity, host, false, year);
    chainDown(ctx, r.target_entity, nid, year, depth + 1, seen);
  });
}

// 05 §16 — 공급사를 전부 중심에 바로 붙이지 않는다. 확인된 만큼만 위로 올라간다
function chainUp(ctx, eid, host, year, depth, seen){
  if (depth > 2 || seen[eid]) return;
  seen[eid] = 1;
  relsOf(eid).forEach(function(r){
    if (r.target_entity !== eid || r.lane !== 'MANUFACTURING_BOM') return;
    var nid = addRelNode(ctx, r, 'x|' + r.source_entity, host, true, year);
    chainUp(ctx, r.source_entity, nid, year, depth + 1, seen);
  });
}

function buildGraph(focal, year, open, expanded, focusOn){
  var groups = {}, nodes = [], edges = [];
  var ctx = { nodes: nodes, edges: edges, byEnt: {} };
  ctx.byEnt[focal] = focal;
  var revRels = relsOf(focal).filter(function(r){
    return r.source_entity === focal && r.target_tier === 'REVENUE_TYPE';
  });
  relsOf(focal).forEach(function(r){
    if (r.target_tier === 'REVENUE_TYPE' && r.source_entity === focal) return;
    var up = r.target_entity === focal;
    var key = (up ? 'u:' : 'd:') + (r.subsystem || LANE_KO[r.lane] || '기타');
    (groups[key] = groups[key] || { up: up, key: r.subsystem || '기타',
                                    label: subKo(r.subsystem) || LANE_KO[r.lane] || '기타',
                                    lane: r.lane, rels: [] }).rels.push(r);
  });
  nodes.push({ id: focal, type:'nd', data:{ title: nm(focal), kind:'ent', focal:true,
    sub: (ENT[focal] && ENT[focal].country) || null, ref:{ kind:'ent', id:focal } } });
  // 매출원 — 눌러야 그 매출원에 근거가 붙는 고객이 열린다 (05 §28)
  revRels.forEach(function(r){
    var rt = r.target_entity, nid = 'rev|' + rt;
    var o = shareIn(r.id, year);
    var pct = o && o.value !== null && o.value !== undefined ? fmt(o.value) + '%' : '?';
    ctx.nodes.push({ id: nid, type:'nd', data:{ title: nm(rt), kind:'grp',
      sub: pct + ' · 총매출 대비', gone: !o,
      ref:{ kind:'rel', id:r.id, entity: rt, revtype:true } } });
    ctx.byEnt[rt] = nid;
    ctx.edges.push({ id:'rev-' + r.id, source: focal, target: nid,
      style:{ stroke:'#9aa3b5', strokeWidth:1.3 }, type:'smoothstep' });
    if (open.indexOf(nid) < 0) return;
    relsOf(rt).forEach(function(c){
      if (c.source_entity !== rt) return;
      var cid = addRelNode(ctx, c, 'rc|' + c.target_entity, nid, false, year);
      chainDown(ctx, c.target_entity, cid, year, 1, {});
    });
  });
  Object.keys(groups).sort(function(a, b){
    return ordOf(groups[a]) - ordOf(groups[b]);
  }).forEach(function(gk){
    var g = groups[gk];
    var act = g.rels.filter(function(r){ return activeIn(r, year); });
    nodes.push({ id: gk, type:'nd', data:{ title: g.label, kind:'grp',
      sub: act.length + '곳 · ' + (g.lane === 'MANUFACTURING_BOM'
        ? (g.up ? '들어온다' : '나간다') : LANE_KO[g.lane]), gone: !act.length,
      ref:{ kind:'grp', id: gk, label:g.label, lane:g.lane, up:g.up,
            rels: g.rels.map(function(r){ return r.id; }) } } });
    edges.push({ id:'g-' + gk, source: g.up ? gk : focal, target: g.up ? focal : gk,
      style:{ stroke:'#c2c7d1', strokeWidth:1.2 }, type:'smoothstep' });
    if (open.indexOf(gk) < 0) return;
    g.rels.forEach(function(r){
      var other = g.up ? r.source_entity : r.target_entity;
      var nid = addRelNode(ctx, r, gk + '|' + other, gk, g.up, year);
      if (g.up) chainUp(ctx, other, nid, year, 1, {});
      else chainDown(ctx, other, nid, year, 1, {});
    });
  });
  // 누른 회사에서 한 홉만 더. 저절로 번지지 않는다
  Object.keys(expanded).forEach(function(k){
    var sp = k.split('@'), eid = sp[0], dir = sp[1];
    var host = null;
    nodes.forEach(function(n){
      if (host) return;
      if (n.id === eid || n.id.split('|').pop() === eid) host = n.id;
    });
    if (!host) return;
    relsOf(eid).forEach(function(r){
      var up = r.target_entity === eid;
      if (dir === 'up' && !up) return;
      if (dir === 'down' && up) return;
      var other = up ? r.source_entity : r.target_entity;
      if (other === focal) return;
      addRelNode(ctx, r, 'x|' + other, host, up, year);
    });
  });
  if (focusOn) {
    var adj = {}, keep = {};
    keep[focal] = 1;
    edges.forEach(function(e){
      (adj[e.source] = adj[e.source] || []).push(e.target);
      (adj[e.target] = adj[e.target] || []).push(e.source);
    });
    var front = [focal], d = 0;
    while (d < 2) {
      var nx = [];
      front.forEach(function(n){
        (adj[n] || []).forEach(function(m){ if (!keep[m]) { keep[m] = 1; nx.push(m); } });
      });
      front = nx; d++;
    }
    nodes = nodes.map(function(n){
      return keep[n.id] ? n
        : Object.assign({}, n, { data: Object.assign({}, n.data, { dim:true }) });
    });
  }
  return { nodes: place(nodes, edges), edges: edges };
}

// ── 서랍 ────────────────────────────────────────────────────────────
function srcLine(sid){
  var s = SRC[sid];
  if (!s) return sid;
  var t = (s.publisher ? s.publisher + ' · ' : '') + s.title
        + (s.published_date ? ' (' + s.published_date + ')' : '');
  return s.url ? h('a', { href:s.url, target:'_blank', rel:'noopener' }, t) : t;
}
function Method(p){
  var m = METH[p.id];
  if (!m) return null;
  var rows = (m.steps || []).filter(function(s){
    return s.value !== null && s.value !== undefined;
  }).map(function(s, i){
    return h('div', { key:i }, [ h('span', { key:'a' }, s.label),
      h('span', { key:'b' }, (s.value === null || s.value === undefined ? '' : fmt(s.value))
        + (s.unit ? ' ' + s.unit : '')) ]);
  });
  return h('div', null, [
    rows.length ? h('div', { key:'s', className:'steps' }, rows) : null,
    m.note ? h('div', { key:'n', className:'v',
      style:{ color:'#6b7488', marginTop:'5px' } }, m.note) : null
  ]);
}
function ObsRow(o){
  var val = (o.value === null || o.value === undefined)
    ? ((o.value_low !== null && o.value_low !== undefined)
        ? fmt(o.value_low) + '~' + fmt(o.value_high) + ' ' + (o.unit || '') : '미상')
    : ((o.value_low !== null && o.value_low !== undefined)
        ? o.value_low + '~' + o.value_high + (PCT[o.unit] ? '%' : ' ' + o.unit)
        : fmt(o.value) + (PCT[o.unit] ? '%' : ' ' + (o.unit || '')));
  return h('div', { key:o.id, style:{ marginBottom:'12px' } }, [
    h('div', { key:'h', style:{ fontSize:'13px', fontWeight:600 } },
      metKo(o.metric) + ' — ' + val),
    h('div', { key:'r', className:'rowk' }, [
      h('div', { key:'a' }, '언제 것'),
      h('div', { key:'b' }, o.period + ' · 기준일 ' + o.as_of_date),
      h('div', { key:'c' }, '분모'), h('div', { key:'d' }, o.denominator || '—'),
      h('div', { key:'e' }, '근거'), h('div', { key:'f' }, [
        h('span', { key:'x',
          className:'badge' + (o.evidence_level === 'CONFIRMED' ? '' : ' est') },
          EV_KO[o.evidence_level] || o.evidence_level),
        h('span', { key:'y', className:'badge' },
          o.status === 'CURRENT' ? '현재' : o.status === 'HISTORICAL' ? '과거'
          : o.status === 'NOT_YET_ACTIVE' ? '진입 전' : '현재 미상'),
        o.confidence ? h('span', { key:'z', className:'badge' },
          '확신 ' + Math.round(o.confidence * 100) + '%') : null,
        (o.denominator_scope === 'FOCAL_TOTAL_REVENUE')
          ? h('span', { key:'w', className:'badge est' }, '총매출 기준 · 이 선의 몫 아님')
          : null ])
    ]),
    o.method_id ? h('div', { key:'m', style:{ marginTop:'6px' } },
      h(Method, { id:o.method_id })) : null,
    o.method_note ? h('div', { key:'n', className:'v',
      style:{ color:'#6b7488', marginTop:'5px' } }, o.method_note) : null,
    (o.source_ids || []).length ? h('div', { key:'s', className:'v' },
      o.source_ids.map(function(sid, i){ return h('div', { key:i }, srcLine(sid)); })) : null
  ]);
}
function Drawer(p){
  var ref = p.sel, year = p.year;
  if (!ref) return null;
  if (ref.kind === 'grp') {
    var rels = ref.rels.map(function(id){ return REL[id]; });
    return h('div', { className:'drw' }, [
      h('button', { key:'x', className:'btn', style:{ float:'right' },
        onClick: p.onClose }, '닫기'),
      h('h3', { key:'t' }, ref.label),
      h('div', { key:'r', className:'role' },
        LANE_KO[ref.lane] + ' · ' + rels.length + '곳 · '
        + (ref.up ? '이 회사로 들어온다' : '이 회사에서 나간다')),
      h('table', { key:'x', className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '회사'),
          h('th', { key:2 }, '부품·역무'), h('th', { key:3 }, year + ' 비중'),
          h('th', { key:5 }, '층'), h('th', { key:4 }, '근거') ])),
        h('tbody', { key:'b' }, rels.map(function(r){
          var other = ref.up ? r.source_entity : r.target_entity;
          return h('tr', { key:r.id, style:{ cursor:'pointer' },
            onClick: function(){ p.onSel({ kind:'rel', id:r.id, entity:other }); } }, [
            h('td', { key:1 }, nm(other)),
            h('td', { key:2 }, r.component || '—'),
            h('td', { key:3 }, shareLabel(r.id, year) || '—'),
            h('td', { key:5 }, TIER_KO[r.source_tier || r.target_tier] || '—'),
            h('td', { key:4 }, h('span', {
              className:'badge' + (r.evidence_level === 'CONFIRMED' ? '' : ' est') },
              EV_KO[r.evidence_level])) ]);
        }))
      ])
    ]);
  }
  var r = ref.kind === 'rel' ? REL[ref.id] : null;
  var eid = ref.kind === 'ent' ? ref.id : ref.entity;
  var e = ENT[eid] || {};
  var obs = r ? (OBS_BY_REL[r.id] || []) : [];
  var claims = [], hyps = [];
  Object.keys(CHAINS).forEach(function(k){
    (CHAINS[k].claims || []).forEach(function(c){
      if (c.subject === eid || c.object === eid) claims.push(c); });
    (CHAINS[k].hypotheses || []).forEach(function(x){
      if (x.anon_company_id === eid || x.candidate_company_id === eid) hyps.push(x); });
  });
  return h('div', { className:'drw' }, [
    h('button', { key:'x', className:'btn', style:{ float:'right' },
      onClick: p.onClose }, '닫기'),
    h('h3', { key:'t' }, nm(eid)),
    h('div', { key:'r', className:'role' },
      [e.entity_type, e.country,
       (e.categories || []).map(subKo).join(' · ')].filter(Boolean).join(' · ')),
    e.desc ? h('div', { key:'d', className:'v' }, e.desc) : null,
    h('div', { key:'btns',
      style:{ display:'flex', gap:'6px', flexWrap:'wrap', margin:'8px 0' } }, [
      h('button', { key:'u', className:'btn',
        onClick: function(){ p.onExpand(eid, 'up'); } }, '업스트림 한 홉'),
      h('button', { key:'d', className:'btn',
        onClick: function(){ p.onExpand(eid, 'down'); } }, '다운스트림 한 홉'),
      h('button', { key:'f', className:'btn',
        onClick: function(){ p.onFocus(eid); } }, '이 회사 중심으로'),
      h('button', { key:'t2', className:'btn',
        onClick: function(){ p.onTimeline(eid); } }, '시점별로 보기')
    ]),
    r ? h('section', { key:'rel' }, [
      h('div', { key:'k', className:'k' }, '관계'),
      h('div', { key:'v', className:'v' }, nm(r.source_entity) + ' → ' + nm(r.target_entity)),
      h('div', { key:'rk', className:'rowk' }, [
        h('div', { key:1 }, '부품·역무'), h('div', { key:2 }, r.component || '—'),
        h('div', { key:3 }, '계통'),
        h('div', { key:4 }, subKo(r.subsystem || '—') + ' · ' + LANE_KO[r.lane]),
        h('div', { key:5 }, '역할'),
        h('div', { key:6 }, (r.source_role || '—') + ' → ' + (r.target_role || '—')),
        h('div', { key:'t1' }, '사슬 층'),
        h('div', { key:'t2' }, TIER_KO[r.source_tier || r.target_tier] || '—'),
        h('div', { key:7 }, '기간'),
        h('div', { key:8 }, (r.valid_from || '?') + ' ~ ' + (r.valid_to || '현재')),
        h('div', { key:9 }, '근거'), h('div', { key:10 }, [
          h('span', { key:'a',
            className:'badge' + (r.evidence_level === 'CONFIRMED' ? '' : ' est') },
            EV_KO[r.evidence_level]),
          r.economic_importance ? h('span', { key:'b', className:'badge' },
            '원가 비중 ' + r.economic_importance) : null,
          r.capacity_criticality ? h('span', { key:'c', className:'badge' },
            '증설 병목 ' + r.capacity_criticality) : null,
          r.integration_criticality ? h('span', { key:'d', className:'badge' },
            '통합 난이도 ' + r.integration_criticality) : null ])
      ]),
      r.notes ? h('div', { key:'n', className:'v',
        style:{ color:'#6b7488', marginTop:'6px' } }, r.notes) : null
    ]) : null,
    obs.length ? h('section', { key:'obs' }, [
      h('div', { key:'k', className:'k', style:{ marginBottom:'8px' } }, '시점별 값'),
      obs.slice().sort(function(a, b){ return a.as_of_date < b.as_of_date ? 1 : -1; })
         .map(function(o){ return ObsRow(o); })
    ]) : null,
    claims.length ? h('section', { key:'clm' }, [
      h('div', { key:'k', className:'k', style:{ marginBottom:'6px' } }, '주장'),
      claims.map(function(c){
        return h('div', { key:c.id, style:{ marginBottom:'9px' } }, [
          h('div', { key:'s', className:'v' }, c.statement),
          h('div', { key:'m' }, [
            h('span', { key:'a',
              className:'badge' + (c.evidence_level === 'CONFIRMED' ? '' : ' est') },
              EV_KO[c.evidence_level]),
            h('span', { key:'b', className:'badge' }, c.period) ]),
          h('div', { key:'src', className:'v' }, (c.source_ids || []).map(function(sid, i){
            return h('div', { key:i }, srcLine(sid)); }))
        ]);
      })
    ]) : null,
    hyps.length ? h('section', { key:'hyp' }, [
      h('div', { key:'k', className:'k', style:{ marginBottom:'6px' } }, '실명 후보'),
      hyps.map(function(x){
        return h('div', { key:x.id, style:{ marginBottom:'9px' } }, [
          h('div', { key:'a', className:'v' },
            nm(x.anon_company_id) + ' = ' + nm(x.candidate_company_id) + ' ?'),
          h('div', { key:'b', className:'v', style:{ color:'#6b7488' } }, x.method),
          h('div', { key:'c' },
            h('span', { className:'badge est' }, '가능성 ' + x.likelihood + '/5')) ]);
      })
    ]) : null,
    r && (r.source_ids || []).length ? h('section', { key:'src' }, [
      h('div', { key:'k', className:'k', style:{ marginBottom:'6px' } }, '출처'),
      r.source_ids.map(function(sid, i){
        return h('div', { key:i, className:'v' }, srcLine(sid)); })
    ]) : null
  ]);
}

// ── 스윔레인 ────────────────────────────────────────────────────────
function Swim(p){
  var focal = p.focal;
  var rows = relsOf(focal).map(function(r){
    var up = r.target_entity === focal;
    return { r:r, other: up ? r.source_entity : r.target_entity, up:up };
  });
  rows.sort(function(a, b){
    if (a.up !== b.up) return a.up ? -1 : 1;
    return (a.r.subsystem || '') < (b.r.subsystem || '') ? -1 : 1;
  });
  return h('div', { className:'pane' }, [
    h('h2', { key:'t' }, nm(focal) + ' — 시점별 관계'),
    h('p', { key:'n', className:'note' },
      '값이 있는 해만 숫자를 적는다. 물음표는 관계는 이어지는데 그 해 수치가 공개되지 않았다는 뜻이다. '
      + '빈 동그라미는 그 해에 관계가 없었다는 뜻이다.'),
    h('table', { key:'x', className:'sw' }, [
      h('thead', { key:'h' }, h('tr', null, [ h('th', { key:'n' }, '상대') ].concat(
        YEARS.map(function(y){ return h('th', { key:y }, y === NOW ? y + ' 현재' : y); })))),
      h('tbody', { key:'b' }, rows.map(function(row){
        return h('tr', { key:row.r.id, style:{ cursor:'pointer' },
          onClick: function(){ p.onSel({ kind:'rel', id:row.r.id, entity:row.other }); } },
          [ h('td', { key:'n' }, [ h('span', { key:'a' }, nm(row.other)),
              h('small', { key:'b' }, ' · ' + subKo(row.r.subsystem || LANE_KO[row.r.lane])) ]) ]
          .concat(YEARS.map(function(y){
            var on = activeIn(row.r, y), lbl = on ? shareLabel(row.r.id, y) : null;
            var isNew = firstYear(row.r) === y && y !== YEARS[0];
            if (endedOpen(row.r))
              return h('td', { key:y }, y === YEARS[0]
                ? h('span', { className:'badge' }, '과거') : h('span', { className:'dot o' }));
            return h('td', { key:y }, on
              ? (lbl ? h('span', null, [ h('span', { key:'v' }, lbl),
                        isNew ? h('span', { key:'n', className:'badge new',
                          style:{ marginLeft:'4px' } }, 'NEW') : null ])
                     : (isNew ? h('span', { className:'badge new' }, 'NEW')
                              : h('span', { className:'dot' })))
              : h('span', { className:'dot o' }));
          })));
      }))
    ])
  ]);
}

// ── 근거 ────────────────────────────────────────────────────────────
function Evidence(){
  var rows = [];
  Object.keys(CHAINS).forEach(function(k){
    (CHAINS[k].claims || []).forEach(function(c){ rows.push(c); });
  });
  return h('div', { className:'pane' }, [
    h('h2', { key:'t' }, '주장과 출처'),
    h('p', { key:'n', className:'note' },
      '공시 그대로인 것과 우리가 계산한 것을 갈라 둔다. 추정에는 분모와 방법이 붙는다.'),
    h('table', { key:'x', className:'t' }, [
      h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '주장'),
        h('th', { key:2 }, '언제 것'), h('th', { key:3 }, '근거'),
        h('th', { key:4 }, '출처') ])),
      h('tbody', { key:'b' }, rows.map(function(c){
        return h('tr', { key:c.id }, [
          h('td', { key:1 }, c.statement),
          h('td', { key:2 }, c.period),
          h('td', { key:3 }, h('span', {
            className:'badge' + (c.evidence_level === 'CONFIRMED' ? '' : ' est') },
            EV_KO[c.evidence_level])),
          h('td', { key:4 }, (c.source_ids || []).map(function(sid, i){
            return h('div', { key:i }, srcLine(sid)); }))
        ]);
      }))
    ])
  ]);
}

// ── 원가 ────────────────────────────────────────────────────────────
var TONE = ['#3d4557','#575f73','#6f7688','#888e9d','#a0a6b3','#b8bcc6','#cfd2d9'];
function Bom(p){
  var ch = CHAINS[p.chain] || {};
  var keys = Object.keys(ch.bom || {});
  var fin = ch.financials || {};
  if (!keys.length && !Object.keys(fin).length)
    return h('div', { className:'pane' }, '이 회사에는 원가 자료가 없다.');
  var b = keys.length ? ch.bom[keys[keys.length - 1]] : null;
  var sum = b ? b.components.reduce(function(a, c){ return a + c.central; }, 0) : 0;
  return h('div', { className:'pane' }, [
    b ? h('h2', { key:'t' }, nm(p.focal) + ' — 제품 원가 구성 (' + b.period + ')') : null,
    b ? h('p', { key:'n', className:'note' }, [
      h('span', { key:'a', className:'badge est' }, '전부 추정'),
      h('span', { key:'b' }, ' ' + b.note + ' 분모는 ' + b.denominator + '.') ]) : null,
    b ? h('div', { key:'bar', className:'bom' }, b.components.map(function(c, i){
      return h('div', { key:c.id, title:c.label,
        onClick: function(){ if (c.subsystem) p.onDrill(c.subsystem); },
        style:{ width:(c.central / sum * 100) + '%', background:TONE[i % TONE.length] } });
    })) : null,
    b ? h('div', { key:'leg', className:'bomleg' }, b.components.map(function(c, i){
      return h('span', { key:c.id, className:'it',
        onClick: function(){ if (c.subsystem) p.onDrill(c.subsystem); } }, [
        h('i', { key:'s', className:'sq', style:{ background:TONE[i % TONE.length] } }),
        h('span', { key:'l' }, c.label + ' ' + c.share_pct + '%') ]);
    })) : null,
    b ? h('table', { key:'t2', className:'t', style:{ marginTop:'16px' } }, [
      h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '구성'),
        h('th', { key:2 }, '중앙값'), h('th', { key:3 }, '범위'), h('th', { key:4 }, '비중'),
        h('th', { key:5 }, '근거'), h('th', { key:6 }, '공급사') ])),
      h('tbody', { key:'b' }, b.components.map(function(c){
        var sup = c.subsystem ? relsOf(p.focal).filter(function(r){
          return r.subsystem === c.subsystem && r.target_entity === p.focal;
        }).map(function(r){ return nm(r.source_entity); }) : [];
        return h('tr', { key:c.id,
          style:{ cursor: c.subsystem ? 'pointer' : 'default' },
          onClick: function(){ if (c.subsystem) p.onDrill(c.subsystem); } }, [
          h('td', { key:1 }, c.label),
          h('td', { key:2 }, c.central + ' ' + b.unit),
          h('td', { key:3 }, c.low ? (c.low + '~' + c.high) : '—'),
          h('td', { key:4 }, c.share_pct + '%'),
          h('td', { key:5 }, h('span', { className:'badge est' }, EV_KO[c.evidence_level])),
          h('td', { key:6 }, sup.join(' · ') || '—')
        ]);
      }))
    ]) : null,
    Object.keys(fin).length ? h('div', { key:'fin' }, [
      h('h2', { key:'t', style:{ marginTop:'20px' } }, '재무 앵커'),
      h('p', { key:'n', className:'note' },
        '매출 환산 MW 는 출하 공시가 아니라 ASP 앵커로 나눈 값이다. 원가를 나눌 분모로만 쓴다.'),
      h('table', { key:'x', className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '기간'),
          h('th', { key:2 }, '총매출'), h('th', { key:3 }, '제품 매출'),
          h('th', { key:4 }, '제품 원가'), h('th', { key:5 }, '매출 환산 MW'),
          h('th', { key:6 }, 'MW 당 원가') ])),
        h('tbody', { key:'b' }, Object.keys(fin).sort(function(a, b){
          return fin[a].as_of_date < fin[b].as_of_date ? -1 : 1;
        }).map(function(k){
          var f = fin[k];
          return h('tr', { key:k }, [
            h('td', { key:1 }, f.period),
            h('td', { key:2 }, fmt(f.total_revenue_usd_m) + ' M'),
            h('td', { key:3 }, fmt(f.product_revenue_usd_m) + ' M'),
            h('td', { key:4 }, fmt(f.product_cogs_usd_m) + ' M'),
            h('td', { key:5 }, [ h('span', { key:'v' },
              fmt(f.revenue_equivalent_mw.value) + ' MW '),
              h('span', { key:'b', className:'badge est' }, '추정') ]),
            h('td', { key:6 },
              f.cogs_per_equivalent_mw.value + ' ' + f.cogs_per_equivalent_mw.unit)
          ]);
        }))
      ])
    ]) : null
  ]);
}

// ── 앱 ──────────────────────────────────────────────────────────────
function App(){
  var u0 = readUrl(true);
  var a = useState(u0.focal), focal = a[0], setFocal = a[1];
  var b = useState(u0.year), year = b[0], setYear = b[1];
  var c = useState(u0.mode), mode = c[0], setMode = c[1];
  var d = useState(u0.open), open = d[0], setOpen = d[1];
  var e = useState({}), expanded = e[0], setExpanded = e[1];
  var f = useState({ kind:'ent', id: u0.sel || u0.focal }), sel = f[0], setSel = f[1];
  var g = useState(''), q = g[0], setQ = g[1];
  var i2 = useState(false), focusOn = i2[0], setFocusOn = i2[1];
  var j = useState([u0.focal]), path = j[0], setPath = j[1];
  var k2 = useState(true), leg = k2[0], setLeg = k2[1];
  // 좁은 화면에서는 서랍을 닫고 시작한다. 열면 그래프를 덮기 때문이다
  var l2 = useState(window.innerWidth >= 980), drw = l2[0], setDrw = l2[1];
  var m2 = useState(null), rf = m2[0], setRf = m2[1];
  useEffect(function(){
    if (!rf) return;
    var t = setTimeout(function(){ rf.fitView({ padding:0.12, duration:220 }); }, 80);
    return function(){ clearTimeout(t); };
  }, [rf, drw, open, focal, year, mode, expanded]);

  useEffect(function(){
    writeUrl({ focal:focal, year:year, mode:mode, open:open,
               sel: sel ? (sel.entity || sel.id) : '' }, false);
  }, [focal, year, mode, open, sel]);
  useEffect(function(){
    function pop(){
      var s = readUrl();
      setFocal(s.focal); setYear(s.year); setMode(s.mode); setOpen(s.open);
      setSel({ kind:'ent', id: s.sel || s.focal });
    }
    window.addEventListener('popstate', pop);
    return function(){ window.removeEventListener('popstate', pop); };
  }, []);

  var chainOfFocal = useMemo(function(){
    var best = null;
    Object.keys(CHAINS).forEach(function(k){
      if (best) return;
      if (CHAINS[k].relationships.some(function(r){
        return r.source_entity === focal || r.target_entity === focal; })) best = k;
    });
    return best;
  }, [focal]);

  var gr = useMemo(function(){
    return buildGraph(focal, year, open, expanded, focusOn);
  }, [focal, year, open, expanded, focusOn]);

  function goFocal(id){
    setFocal(id); setOpen([]); setExpanded({}); setSel({ kind:'ent', id:id });
    setPath(function(p){
      return p.indexOf(id) >= 0 ? p.slice(0, p.indexOf(id) + 1) : p.concat([id]);
    });
    writeUrl({ focal:id, year:year, mode:mode, open:[], sel:id }, true);
  }
  function toggleGroup(gk){
    setOpen(function(o){
      return o.indexOf(gk) >= 0 ? o.filter(function(x){ return x !== gk; }) : o.concat([gk]);
    });
  }
  function onNodeClick(_, node){
    var ref = node.data.ref;
    if (ref.kind === 'grp') toggleGroup(ref.id);
    else if (ref.revtype) toggleGroup('rev|' + ref.entity);
    setSel(ref); setDrw(true);
  }
  function drill(subsystem){
    var rels = relsOf(focal).filter(function(r){
      return r.subsystem === subsystem && r.target_entity === focal;
    });
    if (!rels.length) return;
    var gk = 'u:' + subsystem;
    setMode('current');
    setOpen(function(o){ return o.indexOf(gk) >= 0 ? o : o.concat([gk]); });
    setSel({ kind:'grp', id:gk, label:subsystem, lane:rels[0].lane, up:true,
             rels: rels.map(function(r){ return r.id; }) });
  }

  var hits = q ? Object.keys(ENT).filter(function(id){
      var x = ENT[id];
      var s = (x.name + ' ' + (x.name_ko || '') + ' ' + id).toLowerCase();
      return REL_BY_ENT[id] && s.indexOf(q.toLowerCase()) >= 0;
    }).slice(0, 14) : [];

  var top = h('div', { key:'top', className:'top' }, [
    h('div', { key:'b', className:'brand' }, [ '밸류체인 탐색기',
      h('small', { key:'s' }, '회사를 고르고 눌러 넓히고 시점을 옮긴다') ]),
    h('div', { key:'s', className:'search' }, [
      h('input', { key:'i', value:q, placeholder:'회사 이름으로 찾기',
        onChange: function(ev){ setQ(ev.target.value); } }),
      hits.length ? h('div', { key:'g', className:'sug' }, hits.map(function(id){
        return h('div', { key:id, onClick: function(){ setQ(''); goFocal(id); } }, [
          h('span', { key:'a' }, nm(id)),
          h('span', { key:'b', className:'k' },
            (ENT[id].categories || []).map(subKo).join(' · ')) ]);
      })) : null
    ]),
    h('div', { key:'m', className:'modes' }, [
      ['current', '현재'], ['timeline', '시점'], ['bom', '원가'], ['evidence', '근거']
    ].map(function(x){
      return h('button', { key:x[0], className: mode === x[0] ? 'on' : '',
        onClick: function(){ setMode(x[0]); } }, x[1]);
    })),
    h('div', { key:'sp', className:'spacer' }),
    h('button', { key:'f', className:'btn' + (focusOn ? ' on' : ''),
      onClick: function(){ setFocusOn(!focusOn); } }, '포커스'),
    mode === 'current' ? h('button', { key:'dw', className:'btn' + (drw ? ' on' : ''),
      onClick: function(){ setDrw(!drw); } }, '근거 서랍') : null
  ]);

  var crumb = h('div', { key:'c', className:'crumb' }, path.map(function(id, i){
    return h('span', { key:id, onClick: function(){ goFocal(id); } },
      [ i ? ' › ' : '', i === path.length - 1 ? h('b', { key:'b' }, nm(id)) : nm(id) ]);
  }));

  // 연도는 굴리거나 끌어서 옮긴다. 화살표 키도 듣는다
  function stepYear(d){
    var i = YEARS.indexOf(year) + d;
    if (i < 0) i = 0;
    if (i > YEARS.length - 1) i = YEARS.length - 1;
    if (YEARS[i] !== year) setYear(YEARS[i]);
  }
  function yearAtX(ev){
    var b = ev.currentTarget.getBoundingClientRect();
    var f = (ev.clientX - b.left) / Math.max(1, b.width);
    var i = Math.round(f * (YEARS.length - 1));
    if (i < 0) i = 0;
    if (i > YEARS.length - 1) i = YEARS.length - 1;
    if (YEARS[i] !== year) setYear(YEARS[i]);
  }
  var scrub = h('div', { key:'s', className:'scrub', tabIndex:0,
    title:'굴리거나 끌어서 연도를 옮긴다',
    onWheel: function(ev){ stepYear((ev.deltaY || ev.deltaX) > 0 ? 1 : -1); },
    onMouseDown: function(ev){ yearAtX(ev); },
    onMouseMove: function(ev){ if (ev.buttons === 1) yearAtX(ev); },
    onKeyDown: function(ev){
      if (ev.key === 'ArrowRight' || ev.key === 'ArrowUp') stepYear(1);
      if (ev.key === 'ArrowLeft' || ev.key === 'ArrowDown') stepYear(-1);
    } }, YEARS.reduce(function(acc, y, i){
    if (i) acc.push(h('div', { key:'r' + i, className:'rail' }));
    acc.push(h('div', { key:y, className:'yr' + (y === year ? ' on' : ''),
      onClick: function(){ setYear(y); } }, y === NOW ? y + ' 현재' : y));
    return acc;
  }, []));

  var body;
  if (mode === 'timeline') body = h(Swim, { focal:focal, onSel:setSel });
  else if (mode === 'evidence') body = h(Evidence, null);
  else if (mode === 'bom') body = h(Bom, { chain:chainOfFocal, focal:focal, onDrill:drill });
  else body = h('div', { key:'cv', className:'canvas' }, [
    h(RF, { key:'rf', nodes:gr.nodes, edges:gr.edges, nodeTypes:NODE_TYPES,
      onNodeClick:onNodeClick, onInit:setRf, fitView:true, maxZoom:1.6,
      // 좁은 화면에서는 글자가 안 보일 만큼 줄이지 않는다. 대신 끌어서 본다
      minZoom: window.innerWidth < 720 ? .42 : .2,
      onPaneClick: function(){ if (window.innerWidth < 720) setDrw(false); },
      nodesDraggable:false, proOptions:{ hideAttribution:true } }, [
      h(Background, { key:'bg', gap:22, size:1, color:'#c9cfdb' }),
      h(Controls, { key:'ct', showInteractive:false })
    ])
  ]);

  var legend = h('div', { key:'lg', className:'legend' }, [
    h('b', { key:'b' }, '선'),
    h('i', { key:1 }, '굵은 실선 공시로 확인'),
    h('i', { key:2 }, '갈색 실선 추정 (분모 있음)'),
    h('i', { key:3 }, '파선 정황 추론'),
    h('i', { key:4 }, '점선 비공개·과거 관측'),
    h('i', { key:5 }, '? 그 해 값 없음'),
    h('b', { key:'c' }, '가로'),
    h('i', { key:6 }, '왼쪽 원재료 → 소재·가공 → 부품 → 계통'),
    h('i', { key:7 }, '오른쪽 계약 상대 → 중개 → 프로젝트 → 최종 사용자')
  ]);

  return h('div', { className:'app' }, [ top, crumb,
    (mode === 'current' || mode === 'timeline') ? scrub : null,
    h('div', { key:'m', className:'main' }, [
      body,
      (mode === 'current' && drw) ? h(Drawer, { key:'d', sel:sel, year:year, onSel:setSel,
        onClose: function(){ setDrw(false); },
        onFocus: goFocal,
        onTimeline: function(id){ goFocal(id); setMode('timeline'); },
        onExpand: function(id, dir){
          setExpanded(function(x){
            var y = Object.assign({}, x); y[id + '@' + dir] = 1; return y;
          });
        } }) : null
    ]),
    mode === 'current' ? legend : null
  ]);
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();
'''


def load(*parts):
    p = os.path.join(DATA, *parts)
    if not os.path.exists(p):
        return None
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def by_id(rows):
    return dict((r['id'], r) for r in (rows or []))


def read_dir(base, sub):
    d = os.path.join(base, sub)
    out = {}
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith('.json'):
                with io.open(os.path.join(d, fn), encoding='utf-8') as f:
                    out[fn[:-5]] = json.load(f)
    return out


def build():
    db = {'entities': by_id(load('entities.json')),
          'sources': by_id(load('sources.json')),
          'methods': by_id(load('methods.json')),
          'chains': {}}
    cdir = os.path.join(DATA, 'chains')
    for ck in sorted(os.listdir(cdir)):
        base = os.path.join(cdir, ck)
        if not os.path.isdir(base) or ck not in SHIP:
            continue
        db['chains'][ck] = {
            'relationships': load('chains', ck, 'relationships.json') or [],
            'observations': load('chains', ck, 'observations.json') or [],
            'claims': load('chains', ck, 'claims.json') or [],
            'hypotheses': load('chains', ck, 'hypotheses.json') or [],
            'bom': read_dir(base, 'bom'),
            'financials': read_dir(base, 'financials'),
        }
    # 실은 사슬이 쓰는 엔티티만 내보낸다
    used = set()
    for c in db['chains'].values():
        for r in c['relationships']:
            used.add(r['source_entity'])
            used.add(r['target_entity'])
        for x in c['hypotheses']:
            used.add(x['anon_company_id'])
            used.add(x['candidate_company_id'])
    db['entities'] = dict((k, v) for k, v in db['entities'].items() if k in used)

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
    n = sum(len(c['relationships']) for c in db['chains'].values())
    print('%s\n사슬 %d · 엔티티 %d · 관계 %d · 출처 %d'
          % (p, len(db['chains']), len(db['entities']), n, len(db['sources'])))
