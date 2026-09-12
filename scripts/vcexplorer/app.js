
(function(){
var h = React.createElement;
var RFlib = window.ReactFlow;
var RF = RFlib.default || RFlib.ReactFlow;
var Background = RFlib.Background, Controls = RFlib.Controls, MiniMap = RFlib.MiniMap;
var Handle = RFlib.Handle, Position = RFlib.Position, MarkerType = RFlib.MarkerType;
var getSmoothStepPath = RFlib.getSmoothStepPath;
var EdgeLabelRenderer = RFlib.EdgeLabelRenderer;
var useState = React.useState, useMemo = React.useMemo, useEffect = React.useEffect;

var DB = window.__VC__;
var ENT = DB.entities, SRC = DB.sources, METH = DB.methods, CHAINS = DB.chains;
// SEC 에 등록한 업종. 미국 등록법인과 20-F 를 내는 곳만 있다
var SEC = DB.sec || {};
function secSector(id){ var v = SEC[id]; return v && v.sic_desc ? v.sic_desc : ''; }

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
// 공급원·매출원은 상자가 아니라 분석축이다. 관계가 N:M 으로 가리킨다
var CLS = {};
Object.keys(CHAINS).forEach(function(ck){
  var c = CHAINS[ck].classifications || { supply_sources:[], revenue_types:[] };
  var m = CLS[ck] = { ss:{}, rt:{}, ssList:c.supply_sources || [],
                      rtList:c.revenue_types || [] };
  m.ssList.forEach(function(x){ m.ss[x.id] = x; });
  m.rtList.forEach(function(x){ m.rt[x.id] = x; });
});
function clsOf(ck){ return CLS[ck] || { ss:{}, rt:{}, ssList:[], rtList:[] }; }
function axisHit(r, axis){
  if (!axis) return true;
  var ids = (axis.slice(0, 2) === 'ss' ? r.supply_source_ids : r.revenue_type_ids) || [];
  return ids.indexOf(axis.slice(3)) >= 0;
}
// 원가·재무는 사슬이 아니라 자료에 적힌 주인(company)으로 찾는다.
// 한 회사가 사슬 둘에 걸쳐도 제 것만 본다
var BOM_BY_CO = {}, FIN_BY_CO = {};
Object.keys(CHAINS).forEach(function(ck){
  var c = CHAINS[ck];
  Object.keys(c.bom || {}).forEach(function(k){
    var b = c.bom[k];
    if (b && b.company) (BOM_BY_CO[b.company] = BOM_BY_CO[b.company] || []).push(b);
  });
  Object.keys(c.financials || {}).forEach(function(k){
    var f = c.financials[k];
    if (f && f.company) (FIN_BY_CO[f.company] = FIN_BY_CO[f.company] || []).push(f);
  });
});
Object.keys(BOM_BY_CO).forEach(function(k){
  BOM_BY_CO[k].sort(function(a, b){ return a.as_of_date < b.as_of_date ? -1 : 1; });
});
Object.keys(FIN_BY_CO).forEach(function(k){
  FIN_BY_CO[k].sort(function(a, b){ return a.as_of_date < b.as_of_date ? -1 : 1; });
});

function relsOf(id){
  var seen = {}, out = [];
  (REL_BY_ENT[id] || []).forEach(function(rid){
    if (seen[rid]) return; seen[rid] = 1; out.push(REL[rid]);
  });
  return out;
}
function nm(id){ var e = ENT[id]; return e ? (e.name_ko || e.name) : id; }

// 나라 이름 하나에 깃발 하나. 여러 나라면 여럿을 단다. 모르면 안 단다
var FLAG = { '미국':'US', '한국':'KR', '중국':'CN', '대만':'TW', '일본':'JP', '인도':'IN',
  '캐나다':'CA', '베트남':'VN', '이탈리아':'IT', '네덜란드':'NL' };
var GLOBE = '🌐';
var NO_CC = '?';
var NO_COUNTRY_TYPE = { application:1 };
function iso(cc){
  return cc.replace(/./g, function(c){
    return String.fromCodePoint(0x1F1E6 + c.charCodeAt(0) - 65); });
}
// 소재·매출원은 나라가 없다. 글로벌은 지구본, 원문이 안 밝힌 회사는 물음표
function flagOf(id){
  var e = ENT[id];
  if (!e) return '';
  if (!e.country) return NO_COUNTRY_TYPE[e.entity_type] ? '' : NO_CC;
  var out = [];
  e.country.split('·').forEach(function(part){
    var k = FLAG[part.trim()];
    if (k) out.push(iso(k));
    else if (part.trim() === '글로벌') out.push(GLOBE);
  });
  return out.join(' ');
}
function flagCls(f){ return 'flag' + (f === NO_CC ? ' na' : ''); }
function flagTitle(f){ return f === NO_CC ? '원문이 나라를 밝히지 않았다' : null; }
function withFlag(id, key){
  var f = flagOf(id);
  return f ? [h('span', { key:'f' + (key || ''), className: flagCls(f), title: flagTitle(f) }, f),
              h('span', { key:'n' + (key || '') }, nm(id))] : nm(id);
}

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

// 시작 회사는 사슬의 타겟 가운데 관계가 가장 많은 회사다. 공급사가 관계를 더 많이 가져도
// 첫 화면이 남의 중심으로 다시 세운 판이 되면 안 된다
var HOME = (function(){
  var best = null, n = -1;
  Object.keys(CHAINS).forEach(function(ck){
    var f = (CHAINS[ck].meta || {}).focal_entity;
    if (f && (REL_BY_ENT[f] || []).length > n) { n = REL_BY_ENT[f].length; best = f; }
  });
  if (best) return best;
  Object.keys(REL_BY_ENT).forEach(function(id){
    if (REL_BY_ENT[id].length > n) { n = REL_BY_ENT[id].length; best = id; }
  });
  return best;
})();

var EV_KO = { CONFIRMED:'공시로 확인', ESTIMATED:'추정', INFERRED:'정황 추론',
  UNDISCLOSED:'비공개', HISTORICAL_CURRENT_UNKNOWN:'과거 관측·현재 미상' };
var EV_STYLE = {
  CONFIRMED: { stroke:'#5c6577', strokeWidth:1.7 },
  ESTIMATED: { stroke:'#9a7a4a', strokeWidth:1.6 },
  INFERRED:  { stroke:'#8b93a5', strokeWidth:1.5, strokeDasharray:'7 4' },
  UNDISCLOSED:{ stroke:'#a9b0bf', strokeWidth:1.4, strokeDasharray:'2 4' },
  HISTORICAL_CURRENT_UNKNOWN:{ stroke:'#b8bec9', strokeWidth:1.3, strokeDasharray:'1 5' }
};
function evStyle(k){ return EV_STYLE[k] || EV_STYLE.INFERRED; }
var SUB_KO = { 'Raw material':'원재료', 'Operational input':'운영 투입',
  'Cell':'셀·세라믹', 'Other ceramic':'기타 세라믹', 'Thermal':'열·단열',
  'Interconnect':'인터커넥트', 'Hotbox':'핫박스', 'Power electronics':'전력 전자',
  'Mechanical':'기계·모듈', 'Instrumentation':'계측',
  'Manufacturing equipment':'제조 장비', 'Site electrical BoP':'부지 전기',
  'Financing':'금융', 'EPC / Distribution':'EPC·유통', 'Utility':'유틸리티',
  'Data center':'데이터센터', 'C&I':'산업·상업 고객', 'Project':'프로젝트',
  'Undisclosed customer':'미상 고객', 'Assembly':'조립', 'Integrator':'통합',
  'Material':'소재', 'Material processing':'소재·가공', 'Substrate':'기판',
  'Equipment':'장비',
  'Revenue type':'매출원', 'Chip maker':'칩 회사', 'Automotive':'자동차',
  'Integrator':'통합', 'OSAT':'후공정(OSAT)' };
function subKo(k){ return SUB_KO[k] || k; }
var TIER_KO = { CONTRACTUAL_CUSTOMER:'직접 고객', INTERMEDIARY:'중개',
  PROJECT:'프로젝트', END_USER:'간접 고객', END_MARKET:'전방시장',
  RAW_MATERIAL:'원재료', MATERIAL_PROCESSING:'소재·가공',
  COMPONENT_SUPPLIER:'부품 공급', SUBSYSTEM_MODULE:'계통·모듈' };
function tierOf(r, up){ return up ? r.source_tier : r.target_tier; }
// 상자 꼴 — 회사·법인은 실선, 전방시장처럼 회사가 아닌 축은 파선.
// 소재·부품·계통·매출 갈래는 더 이상 상자가 아니다. 위쪽 공급원·매출원 띠로 간다
var KIND_OF = { application:'grp' };
// 세로 한 줄에는 같은 단계만 선다. 왼쪽부터 오른쪽으로 사슬 순서다.
// note 는 그 칸이 무엇을 세는 자리인지 — 매출원·최종 사용자 칸에는 사슬의 다음 단계가
// 아니라 같은 매출을 다른 축으로 쪼갠 상자가 서기 때문에, 밝히지 않으면 옆 칸과
// 이어진 단계로 읽힌다
var COLS = [
  { key:'RAW_MATERIAL', label:'원재료', note:'사슬 단계' },
  { key:'MATERIAL_PROCESSING', label:'소재·가공', note:'사슬 단계' },
  { key:'COMPONENT_SUPPLIER', label:'부품 공급', note:'사슬 단계' },
  { key:'SUBSYSTEM', label:'계통·모듈', note:'사슬 단계' },
  { key:'SUPPLY_AXIS', label:'공급원', note:'분석축 · 갈림목' },
  { key:'FOCAL', label:'타겟', note:'중심 회사' },
  { key:'REVENUE_AXIS', label:'매출원', note:'분석축 · 갈림목' },
  { key:'CONTRACTUAL_CUSTOMER', label:'직접 고객', note:'사슬 단계' },
  { key:'INTERMEDIARY', label:'중개', note:'사슬 단계' },
  { key:'END_USER', label:'간접 고객', note:'중개 뒤' },
  // 사슬 깊이는 데이터가 정한다(프레임워크 §2 Step 4). 간접 고객 뒤에 또 고객이 있으면
  // 한 칸씩 더 선다 — 한 칸에 몰아넣으면 같은 칸 안에서 가리키는 선이 생긴다
  { key:'END_USER_2', label:'간접 고객', note:'한 단 더' },
  { key:'END_USER_3', label:'간접 고객', note:'두 단 더' },
  { key:'END_USER_4', label:'간접 고객', note:'세 단 더' },
  { key:'END_MARKET', label:'전방시장', note:'다른 축' }
];
var COL_OF = {};
COLS.forEach(function(c, i){ COL_OF[c.key] = i; });
// 검사기가 쓰는 이름과 칸 이름이 한 글자씩 다르다. 같은 자리로 읽는다
var TIER_ALIAS = { COMPONENT:'COMPONENT_SUPPLIER', SUBSYSTEM_MODULE:'SUBSYSTEM' };
// 다른 회사를 중심에 놓을 때 왼쪽 칸 — 사슬 층 대신 그 회사에서 몇 단 앞인가
var HOP_LABEL = { SUBSYSTEM:'1단 앞', COMPONENT_SUPPLIER:'2단 앞',
  MATERIAL_PROCESSING:'3단 앞', RAW_MATERIAL:'4단 이상 앞' };
var HOP_COL = [COL_OF.SUBSYSTEM, COL_OF.COMPONENT_SUPPLIER, COL_OF.MATERIAL_PROCESSING,
  COL_OF.RAW_MATERIAL];
function colOfRel(r, up){
  var t = tierOf(r, up);
  if (TIER_ALIAS[t]) t = TIER_ALIAS[t];
  if (t && COL_OF[t] !== undefined) return COL_OF[t];
  if (up) return COL_OF.MATERIAL_PROCESSING;
  // 층이 안 적힌 상대는 갈래를 보고 자리를 준다. BOM 은 타겟 왼쪽에 놓일
  // 중간재이고, 고객 칸으로 보내면 소재가 고객 자리에 앉는다
  return r.lane === 'DOWNSTREAM' ? COL_OF.CONTRACTUAL_CUSTOMER
                                 : COL_OF.MATERIAL_PROCESSING;
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
var REL_KO = { SUPPLIES:'공급', PROCESSED_INTO:'가공', INPUT_TO:'투입', FEEDS:'넘김',
  FUELS:'연료', EQUIPMENT_SUPPLY:'장비 공급', ELECTRICAL_BOP_SUPPLY:'부지 전기 공급',
  PROJECT_SUPPLY:'프로젝트 공급', JV_ASSEMBLY:'합작 조립', OPERATES_THROUGH:'운영 자회사',
  DEVELOPS:'개발', FINANCES:'금융', HOLDS_PROJECT:'프로젝트 보유',
  PROJECT_FINANCE:'프로젝트 금융', DISTRIBUTION_PARTNERSHIP:'유통·EPC 제휴',
  EXECUTES_THROUGH:'실행 법인', EXECUTES_THROUGH_SUBSIDIARY:'실행 자회사',
  SYSTEM_INTEGRATION_PARTNERSHIP:'시스템 통합 제휴', DEMONSTRATION_DEPLOYMENT:'실증 설치',
  OPERATES_AT_SITE:'부지 운영·통합', SELLS_TO:'판매', REVENUE_FROM:'매출원',
  UTILITY_SERVES:'전력 공급', DIRECT_CUSTOMER:'직접 고객',
  CUSTOMERS_CUSTOMER:'고객의 고객', END_USER_DEPLOYMENT:'설치·배치',
  DEPLOYS_AT:'설치 부지', SUBSIDIARY_OF:'자회사', CONTRACT_MANUFACTURES:'수탁 제조',
  SERVES_END_MARKET:'최종 시장', SERVES_END_USER:'최종 사용자',
  CREDIT_SUPPORT:'신용 보강', INVESTS_IN:'투자' };
function relKo(k){ return REL_KO[k] || k; }
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
var HANDLE_N = 7;
// 유형 아이콘 — 상자 종류를 글자 대신 한 획으로. 회사·공장·유통·플랫폼·부지·금융·전력
var ICON_PATH = {
  company:'M4 21V7l8-4 8 4v14M9 21v-6h6v6M8 11h.01M12 11h.01M16 11h.01',
  factory:'M3 21V10l6 4V10l6 4V4h6v17M7 17h.01M11 17h.01M15 17h.01',
  distributor:'M3 7h11v9H3zM14 10h4l3 3v3h-7M6 19a2 2 0 1 0 0-.1M17 19a2 2 0 1 0 0-.1',
  platform:'M7 18a4 4 0 0 1-.6-8A6 6 0 0 1 18 9a4 4 0 0 1 0 9z',
  site:'M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11zM12 10h.01',
  finance:'M3 10l9-6 9 6M5 10v9M9 10v9M15 10v9M19 10v9M3 21h18',
  utility:'M13 2L4 14h6l-1 8 9-12h-6z',
  market:'M3 12h4l3-8 4 16 3-8h4'
};
function iconOf(id){
  var e = ENT[id] || {}, t = e.entity_type, cats = (e.categories || []).join(' ').toLowerCase();
  if (t === 'application') return 'market';
  if (t === 'project_spv') return 'site';
  if (t === 'utility') return 'utility';
  if (t === 'financial_institution' || t === 'fund_jv') return 'finance';
  if (/distribut/.test(cats)) return 'distributor';
  if (/platform|cloud/.test(cats) && t !== 'company') return 'platform';
  if (/plant|manufactur|ceramic|plating|inductor|assembly|foundry|component/.test(cats)
      && e.entity_type === 'company' && /plant|공장|manufactur/i.test((e.name || '') + cats))
    return 'factory';
  return t === 'end_user' ? 'platform' : 'company';
}
// 포트는 네 갈래 — 왼쪽으로 드는 t, 오른쪽으로 나가는 s, 그리고 왼쪽으로 가는 선을 위한
// sl(왼쪽 변에서 나감)·tr(오른쪽 변으로 듦). 거꾸로 가는 선이 제 상자를 가로지르지 않게
var PORT_SIDE = { t:[ 'target', Position.Left ], s:[ 'source', Position.Right ],
                  sl:[ 'source', Position.Left ], tr:[ 'target', Position.Right ] };
function ports(kind){
  var out = [];
  for (var i = 0; i < HANDLE_N; i++){
    out.push(h(Handle, { key: kind + i, id: kind + i,
      type: PORT_SIDE[kind][0],
      position: PORT_SIDE[kind][1],
      isConnectable: false,
      style:{ opacity:0, width:1, height:1, minWidth:1, minHeight:1, border:0,
              top: Math.round((i + 1) * 100 / (HANDLE_N + 1)) + '%' } }));
  }
  return out;
}
function Nd(p){
  var d = p.data;
  var cls = 'nd' + (d.kind === 'grp' ? ' grp' : '') + (d.kind === 'lane' ? ' lane' : '')
          + (d.un ? ' un' : '') + (d.focal ? ' focal' : '') + (d.sel ? ' sel' : '')
          + (d.dim ? ' dim' : '') + (d.gone ? ' gone' : '');
  var mid = [
    h('div', { key:'n', className:'nm' }, [
      d.ico ? h('svg', { key:'i', className:'ico', viewBox:'0 0 24 24' },
        h('path', { d: ICON_PATH[d.ico] })) : null,
      d.flag ? h('span', { key:'f', className: flagCls(d.flag), title: flagTitle(d.flag) },
        d.flag) : null,
      h('span', { key:'t' }, d.title) ]),
    (d.sub || d.isNew || (d.share && d.kind === 'lane'))
      ? h('div', { key:'s', className:'sub' }, [
      d.sub ? h('span', { key:'t2' }, d.sub) : null,
      (d.share && d.kind === 'lane') ? h('span', { key:'v', className:'shr' }, d.share) : null,
      d.isNew ? h('span', { key:'b', className:'badge new',
        style:{ marginLeft: d.sub ? '5px' : 0 } }, 'NEW') : null,
    ]) : null,
    (d.share && d.kind !== 'lane') ? h('span', { key:'shr', className:'shr',
      title: d.share === '?' ? ('이 해 값 없음 · 값 있는 해 ' + ((d.shareYears || []).join(', ') || '—'))
                             : null }, d.share) : null
  ];
  if (d.more) mid.push(h('span', { key:'more',
    className:'more' + (d.col !== undefined && d.col < COL_OF.FOCAL ? ' l' : ''),
    title:'누르면 ' + d.more + '곳을 편다' }, '+' + d.more));
  return h('div', { className: cls },
    ports('t').concat(ports('sl')).concat(mid).concat(ports('s')).concat(ports('tr')));
}
// 판 안의 머리글 자리는 비워 둔다(fitView 가 그 여백을 세게). 글자는 HdrBar 가 판 위에
// 겹쳐 그린다 — 아래로 끌어도 머리글이 화면 위에 그대로 남아 어느 칸인지 잃지 않는다
function Hdr(p){
  return h('div', { className:'hdr', style:{ visibility:'hidden' } }, [
    h('div', { key:'l', className:'hl' }, p.data.label) ]);
}
function HdrBar(p){
  var z = p.vp.zoom, hs = p.nodes.filter(function(n){ return n.type === 'hdr'; });
  var fz = Math.max(.72, Math.min(1, z));
  return h('div', { className:'hdrbar' }, hs.map(function(n){
    return h('div', { key:n.id, className:'hdr',
      style:{ position:'absolute', top:'6px', left:(n.position.x * z + p.vp.x) + 'px',
              width:(COL_W * z) + 'px', transform:'none', fontSize:(fz * 100) + '%' } }, [
      h('div', { key:'l', className:'hl' }, n.data.label),
      n.data.note ? h('div', { key:'n', className:'hn' }, n.data.note) : null ]);
  }));
}
// 꺾어지는 자리마다 모서리를 둥글린 직교 경로를 만든다
function orth(pts, r){
  var d = 'M ' + pts[0].x + ' ' + pts[0].y;
  for (var i = 1; i < pts.length - 1; i++){
    var a = pts[i - 1], b = pts[i], c = pts[i + 1];
    var d1 = Math.hypot(b.x - a.x, b.y - a.y), d2 = Math.hypot(c.x - b.x, c.y - b.y);
    var rr = Math.max(0, Math.min(r, d1 / 2, d2 / 2));
    if (!rr) continue;
    var p1 = { x: b.x + (a.x - b.x) / d1 * rr, y: b.y + (a.y - b.y) / d1 * rr };
    var p2 = { x: b.x + (c.x - b.x) / d2 * rr, y: b.y + (c.y - b.y) / d2 * rr };
    d += ' L ' + p1.x + ' ' + p1.y + ' Q ' + b.x + ' ' + b.y + ' ' + p2.x + ' ' + p2.y;
  }
  var last = pts[pts.length - 1];
  return d + ' L ' + last.x + ' ' + last.y;
}
// 선은 하나뿐인 문법으로 그린다 — 상자에서 수평으로 나가고, 출발 칸 바로 옆 통로에서
// 한 번만 위아래로 움직이고, 그 높이로 닿을 상자까지 곧게 간다. 꺾임은 둘을 넘지 않는다.
// gx 는 통로 자리(route 가 정한다), gy 는 그 통로에서 옮겨 갈 높이다. gy 가 비면 닿을
// 상자의 높이다. gy 가 그 높이와 다르면(중간 상자를 비키느라 더 멀리 옮긴 선) 그 높이로
// 곧게 가서 끝난다 — 상자 앞에서 다시 꺾지 않는다
function GutEdge(p){
  var d = p.data || {};
  var gx = d.gx, gy = (d.gy === null || d.gy === undefined) ? p.targetY : d.gy;
  var path = [{ x:p.sourceX, y:p.sourceY }];
  if (gx !== null && gx !== undefined) {
    path.push({ x:gx, y:p.sourceY });
    path.push({ x:gx, y:gy });
  }
  path.push({ x:p.targetX, y:gy });
  // 같은 자리에 겹쳐 찍힌 점은 걷는다. 안 걷으면 모서리 반지름이 0 이 된다
  var pts = path.filter(function(q, i){
    return i === 0 || Math.abs(q.x - path[i-1].x) > 0.5 || Math.abs(q.y - path[i-1].y) > 0.5;
  });
  var mid = pts[(pts.length / 2) | 0];
  return h(React.Fragment, null, [
    h('path', { key:'p', id:p.id, d:orth(pts, 8), fill:'none',
      className:'react-flow__edge-path', style:p.style, markerEnd:p.markerEnd }),
    p.label ? h(EdgeLabelRenderer, { key:'l' },
      h('div', { style:{ position:'absolute', pointerEvents:'none',
        transform:'translate(-50%,-50%) translate(' + mid.x + 'px,' + mid.y + 'px)',
        background:'#fff', padding:'0 3px', fontSize:'10.5px', lineHeight:1.3,
        color:'#39415a' } }, p.label)) : null
  ]);
}
var EDGE_TYPES = { gut: GutEdge };
// 프로젝트는 사슬의 한 단계가 아니라 여러 상자를 묶는 테두리다. 상자는 제 자리에
// 그대로 서고, 테두리는 그 뒤에 깔려 누가 한 프로젝트에 얽혔는지만 보여 준다.
// 테두리에는 포트가 없다 — 선은 언제나 상자(SPV·부지·회사)에 닿지 테두리에 닿지 않는다.
// 식구는 projects.json 이 명시한 것뿐이고 관계로 추론하지 않는다
function Proj(p){
  var d = p.data;
  return h('div', { className:'proj', style:{ width:d.w + 'px', height:d.h + 'px' } },
    (d.segs || []).map(function(sg, i){
      return h('div', { key:'sg' + i, className:'pseg',
        style:{ left:sg.x + 'px', top:sg.y + 'px', width:sg.w + 'px', height:sg.h + 'px' } });
    }).concat([
    h('div', { key:'l', className:'plab', style:{ left:(d.lx || 0) + 4 + 'px', right:'auto',
        width: COL_W + 'px' } }, [
      h('div', { key:'a' }, '프로젝트'),
      h('div', { key:'b', className:'pn' }, d.title) ])
  ]));
}
var NODE_TYPES = { nd: Nd, hdr: Hdr, proj: Proj };
// 위 여백은 「프로젝트」 + 이름 두 줄이 들어갈 만큼. 34 로는 이름이 첫 식구 상자와 겹쳤다
var PROJ_PAD_X = 18, PROJ_PAD_Y = 52;

// 칸을 건너뛰는 선이 지나갈 빈 자리는 상자와 같은 높이로 잡는다. 10px 만 비우면
// 그 띠가 상자 높이를 못 덮어 선이 중간 칸 상자를 가로지른다
// 상자 156×64, 칸 사이 56. 읽히는 크기가 먼저다 — 판 전체를 한 화면에 넣지 않는다
var COL_W = 156, COL_GAP = 56, ROW_GAP = 16, HDR_H = 40, DUMMY_H = 64;
// 칸 사이 빈 띠 한가운데가 통로다. 세로 이동은 오직 여기서만 한다 — 상자가 선 칸
// 안에서 세로로 움직이면 선이 상자 옆구리를 스쳐 그 상자에서 나가는 것처럼 읽힌다
function gutterX(bd, lane){
  return bd * (COL_W + COL_GAP) + COL_W + COL_GAP / 2 + (lane || 0);
}
// 칸 머리글과 첫 상자 사이 숨통. HDR_H 는 머리글 상자 높이와 같아서
// 그것만 쓰면 둘이 맞닿는다
var HDR_GAP = 34;

// 상자는 갈래를 가리지 않고 한 크기다. 높이가 갈리면 같은 줄에 선 것들이
// 층이 어긋나 보이고 선도 같은 눈금에 못 선다
var BOX_H = 64, LANE_H = 64;
function boxH(d){
  return d.kind === 'lane' ? LANE_H : BOX_H;
}

// 칸 사이 빈 띠를 레인으로 쪼개고, 노드 변에는 포트를 나눠 꽂는다.
// fcol 은 타겟이 선 칸 번호(geo 의 col 눈금) — 꺾는 쪽을 가르는 기준이다
function route(edges, geo, fcol){
  function cy(id){ var g = geo[id]; return g ? g.y + g.h / 2 : 0; }

  var outg = {}, inn = {};
  edges.forEach(function(e){
    if (!geo[e.source] || !geo[e.target]) return;
    (outg[e.source] = outg[e.source] || []).push(e);
    (inn[e.target] = inn[e.target] || []).push(e);
  });
  function slot(i, n){
    if (n <= 1) return (HANDLE_N - 1) / 2 | 0;
    // 둘·셋·넷이면 한 칸씩 띄워 꽂는다. 붙여 꽂으면 두 줄이 한 줄처럼 보인다
    if (n * 2 - 1 <= HANDLE_N) return ((HANDLE_N - (n * 2 - 1)) / 2 | 0) + i * 2;
    if (n <= HANDLE_N) return ((HANDLE_N - n) / 2 | 0) + i;
    return Math.round(i * (HANDLE_N - 1) / (n - 1));
  }
  // 왼쪽으로 가는 선(닿을 상자가 출발 상자보다 왼쪽)은 왼쪽 변에서 나가 오른쪽 변으로 든다
  function leftward(e){ return geo[e.target].col < geo[e.source].col; }
  function hs(e){ return leftward(e) ? 'sl' : 's'; }
  function ht(e){ return leftward(e) ? 'tr' : 't'; }
  Object.keys(outg).forEach(function(id){
    var a = outg[id].sort(function(p, q){ return cy(p.target) - cy(q.target); });
    a.forEach(function(e, i){ e.sourceHandle = hs(e) + slot(i, a.length); });
  });
  Object.keys(inn).forEach(function(id){
    var a = inn[id].sort(function(p, q){ return cy(p.source) - cy(q.source); });
    a.forEach(function(e, i){ e.targetHandle = ht(e) + slot(i, a.length); });
  });

  // ② 통로 — 세로 이동은 칸 사이 빈 띠 한가운데의 통로에서만 일어난다. 같은 상자에서
  // 갈라지는 선(또는 한 상자로 모이는 선)은 그 통로를 같이 쓰고, 통로가 여럿 겹칠 때만
  // 가운데에서 ±6px 씩, 최대 ±10px 까지 비켜 앉는다. 빈 띠 전체에 퍼뜨리지 않는다
  var MID = (HANDLE_N - 1) / 2 | 0;
  var LANE_STEP = 6, LANE_MAX = 10;
  function bounds(e){
    var a = geo[e.source], b = geo[e.target];
    if (!a || !b || a.col === b.col) return null;
    var list = [];
    if (a.col < b.col) { for (var i = a.col; i < b.col; i++) list.push(i); }
    else { for (var j = a.col - 1; j >= b.col; j--) list.push(j); }
    return list;
  }
  var cross = {}, lane = {};
  edges.forEach(function(e){
    var bs = bounds(e);
    if (!bs) return;
    bs.forEach(function(bd){ (cross[bd] = cross[bd] || []).push(e); });
  });
  Object.keys(cross).forEach(function(bk){
    var list = cross[bk], outd = {}, ind = {};
    list.forEach(function(e){
      outd[e.source] = (outd[e.source] || 0) + 1;
      ind[e.target] = (ind[e.target] || 0) + 1;
    });
    var groups = {}, order = [];
    list.forEach(function(e){
      var key = outd[e.source] > 1 ? 'S|' + e.source
              : (ind[e.target] > 1 ? 'T|' + e.target : 'E|' + e.id);
      if (!groups[key]) { groups[key] = []; order.push(key); }
      groups[key].push(e);
    });
    order.sort(function(p, q){
      return cy(p.slice(2) in geo ? p.slice(2) : groups[p][0].source)
           - cy(q.slice(2) in geo ? q.slice(2) : groups[q][0].source);
    });
    var n = order.length;
    order.forEach(function(key, i){
      var off = n <= 1 ? 0
        : Math.max(-LANE_MAX, Math.min(LANE_MAX, (i - (n - 1) / 2) * LANE_STEP));
      groups[key].forEach(function(e){ lane[e.id + '@' + bk] = off; });
      // 한 상자에서 갈라지거나 한 상자로 모이는 선은 그 상자 쪽 포트를 하나로 모은다
      if (groups[key].length > 1) {
        groups[key].forEach(function(e){
          if (key.charAt(0) === 'S') e.sourceHandle = hs(e) + MID;
          else if (key.charAt(0) === 'T') e.targetHandle = ht(e) + MID;
        });
      }
    });
  });

  // ③ 선마다 통로 자리 하나와 거기서 옮겨 갈 높이 하나를 적는다. 통로는 출발 칸 바로
  // 옆 하나뿐이다 — 그 앞은 출발 높이, 그 뒤는 닿을 높이로 곧게 간다(꺾임 최대 둘).
  // 중간 칸의 상자는 place 가 빈 자리를 잡아 두어 닿을 높이에서 비켜 있다. 그래도
  // 걸리면 더 멀리 한 번에 옮긴다 — 타겟 오른쪽은 아래로(걸린 상자 바닥 아래), 왼쪽은
  // 위로(걸린 상자 머리 위). 상자 앞에서 다시 꺾어 지그재그를 만들지 않는다.
  // 통로를 여럿 밟던 옛 gx[]/gy[] 는 걷었다 — 직접 선이 여러 번 꺾이는 원인이었다
  var boxes = {};
  Object.keys(geo).forEach(function(id){
    var g = geo[id];
    if (!g || g.proj || id.charAt(0) === '~') return;
    g.id = id;
    (boxes[g.col] = boxes[g.col] || []).push(g);
  });
  var CLR = 7;
  function blockersAt(cols, y){
    var out = [];
    cols.forEach(function(c){
      (boxes[c] || []).forEach(function(g){
        if (y > g.y - CLR && y < g.y + g.h + CLR) out.push(g);
      });
    });
    return out;
  }
  edges.forEach(function(e){
    var a = geo[e.source], b = geo[e.target];
    if (!a || !b) return;
    if (a.col === b.col) { e.type = 'default'; return; }
    var bs = bounds(e);
    var y0 = cy(e.source), y1 = cy(e.target);
    if (bs.length === 1 && Math.abs(y0 - y1) <= 8) {
      e.type = 'straight';
      e.data = Object.assign({}, e.data, { gx:null, gy:null });
      return;
    }
    var dir = b.col > a.col ? 1 : -1, mids = [];
    for (var c = a.col + dir; c !== b.col; c += dir) mids.push(c);
    var hit = blockersAt(mids, y1);
    var clearY = y1;
    if (hit.length) {
      // 오른쪽(타겟 칸에서 나가는 쪽)은 아래로만, 왼쪽(타겟 칸으로 드는 쪽)은 위로만
      var rightSide = fcol === undefined ? dir > 0 : Math.min(a.col, b.col) >= fcol;
      hit.forEach(function(g){
        clearY = rightSide ? Math.max(clearY, g.y + g.h + CLR)
                           : Math.min(clearY, g.y - CLR);
      });
      if (window.console) console.warn('vc route: ' + e.id + ' 가 중간 상자('
        + hit.map(function(g){ return g.id + '@' + g.col + ':' + Math.round(g.y) + '~'
                                    + Math.round(g.y + g.h); }).join(',')
        + ')에 걸려 ' + Math.round(y1) + ' 대신 ' + Math.round(clearY)
        + ' 로 옮긴다. place 가 빈 자리를 못 잡았다');
    }
    e.type = 'gut';
    e.data = Object.assign({}, e.data,
      { gx: gutterX(bs[0], lane[e.id + '@' + bs[0]] || 0),
        gy: clearY === y1 ? null : clearY });
  });
}

function place(nodes, edges, opts){
  opts = opts || {};
  // 가로는 단계 칸에 못박는다. dagre 는 부르지 않는다
  var colOf = {}, byCol = {};
  // 프로젝트 테두리는 칸에 안 든다. 식구를 다 앉힌 뒤 그 둘레로 잡는다
  var projs = nodes.filter(function(n){ return n.type === 'proj'; });
  nodes = nodes.filter(function(n){ return n.type !== 'proj'; });
  nodes.forEach(function(n){
    var c = n.data.col === undefined ? COL_OF.FOCAL : n.data.col;
    colOf[n.id] = c;
    (byCol[c] = byCol[c] || []).push(
      { id:n.id, n:n, h: boxH(n.data), dummy:false });
  });
  var used = Object.keys(byCol).map(Number).sort(function(a, b){ return a - b; });
  var at = {};
  used.forEach(function(c, i){ at[c] = i; });

  var nbr = {}, span = {};
  function link(a, b){
    (nbr[a] = nbr[a] || []).push(b);
    (nbr[b] = nbr[b] || []).push(a);
  }
  // 칸을 건너뛰는 선에는 중간 칸마다 보이지 않는 자리를 잡아 둔다. 같은 상자로 모이는
  // 선들은 그 칸에서 자리 하나를 같이 쓴다 — 닿을 높이가 같은데 자리를 둘 잡으면 둘 다
  // 그 높이에 앉을 수 없어 서로 밀어내며 끝없이 내려간다(N:1 은 통로를 함께 쓴다)
  var dummyOf = {};
  edges.forEach(function(e){
    var a = at[colOf[e.source]], b = at[colOf[e.target]];
    if (a === undefined || b === undefined) return;
    if (Math.abs(b - a) <= 1) { link(e.source, e.target); return; }
    var step = b > a ? 1 : -1, prev = e.source;
    var mine = span[e.id] = [];
    for (var i = a + step; i !== b; i += step){
      var did = '~' + e.target + '@' + i;
      if (!dummyOf[did]) {
        dummyOf[did] = { id:did, n:null, h:DUMMY_H, dummy:true };
        byCol[used[i]].push(dummyOf[did]);
      }
      mine.push(did);
      link(prev, did);
      prev = did;
    }
    link(prev, e.target);
  });

  // 빈 자리의 차례 — 타겟으로 드는 선의 빈 자리 0, 상자 1, 지나쳐 가는 선의 빈 자리 2
  var focalId = null;
  nodes.forEach(function(n){ if (n.data && n.data.focal) focalId = n.id; });
  function dummyRank(it){
    if (!it.dummy) return 1;
    var t = it.id.slice(1, it.id.lastIndexOf('@'));
    return t === focalId ? 0 : 2;
  }
  // 세로 차례 — 앞뒤로 여러 번 쓸어야 교차가 준다
  used.forEach(function(c){ byCol[c].forEach(function(it, i){ it.ord = i; }); });
  function sweep(dir){
    var seq = dir > 0 ? used.slice(1) : used.slice(0, -1).reverse();
    seq.forEach(function(c){
      var refCol = byCol[used[at[c] - dir]], ref = {};
      refCol.forEach(function(it, k){ ref[it.id] = k; });
      var span = Math.max(1, refCol.length - 1);
      var list = byCol[c];
      var nFix = list.filter(function(it){
        return it.n && it.n.data && it.n.data.fixOrd !== undefined; }).length;
      list.forEach(function(it){
        // 알약(공급원·매출원)은 정한 차례(비중 순)로 선다. 이웃 무게중심을 안 본다
        if (it.n && it.n.data && it.n.data.fixOrd !== undefined) {
          it.bary = it.n.data.fixOrd / Math.max(1, nFix - 1);
          return;
        }
        var ks = (nbr[it.id] || []).filter(function(x){ return ref[x] !== undefined; });
        // 0~1 로 맞춘다. 참조 칸에 더미가 몇 개 끼든 눈금이 안 흔들린다
        it.bary = ks.length
          ? ks.reduce(function(a, x){ return a + ref[x]; }, 0) / ks.length / span
          : null;
      });
      // 이웃이 없는 상자는 위아래로 가장 가까운 상자 사이에 고르게 끼운다
      var prev = 0;
      for (var i = 0; i < list.length; i++){
        if (list[i].bary !== null) { prev = list[i].bary; continue; }
        var j = i;
        while (j < list.length && list[j].bary === null) j++;
        var next = j < list.length ? list[j].bary : 1;
        var n = j - i + 1;
        for (var k = i; k < j; k++)
          list[k].bary = prev + (next - prev) * (k - i + 1) / n;
        i = j - 1;
      }
      // 무게중심이 같으면 타겟으로 드는 선의 빈 자리만 먼저다(타겟 높이가 비어 있어야
      // 한다). 그 밖의 빈 자리(전방시장처럼 칸을 지나쳐 가는 선)는 상자 뒤로 보낸다 —
      // 앞에 두면 그 통로들이 칸 위쪽을 차지해 알약·상자가 한참 아래로 밀린다
      list.sort(function(a, b){
        return (a.bary - b.bary) || (dummyRank(a) - dummyRank(b)) || (a.ord - b.ord);
      });
      list.forEach(function(it, k){ it.ord = k; });
    });
  }
  for (var s = 0; s < 4; s++){ sweep(1); sweep(-1); }

  // 한 프로젝트의 식구는 붙여 앉힌다. 사이에 남이 끼면 테두리가 그 남까지 두른다
  var ofProj = {};
  projs.forEach(function(pn){
    (pn.data.mem || []).forEach(function(m){ ofProj[m] = pn.id; });
  });
  // 프로젝트의 높이는 칸마다 따로 정하지 않고 판 전체에서 하나로 잡는다(띠). 칸마다
  // 따로 재면 같은 프로젝트의 식구가 칸마다 다른 높이에 앉아 테두리끼리 가로질러 겹친다
  var gsum = {}, gcnt = {};
  used.forEach(function(c){
    var list = byCol[c], span = Math.max(1, list.length - 1);
    list.forEach(function(it){
      var pj = ofProj[it.id];
      if (!pj) return;
      gsum[pj] = (gsum[pj] || 0) + it.ord / span;
      gcnt[pj] = (gcnt[pj] || 0) + 1;
    });
  });
  var grank = {};
  Object.keys(gsum).forEach(function(pj){ grank[pj] = gsum[pj] / gcnt[pj]; });
  used.forEach(function(c){
    var list = byCol[c], key = {}, mean = {}, span = Math.max(1, list.length - 1);
    list.forEach(function(it){
      var k = ofProj[it.id] || ('~' + it.id);
      key[it.id] = k;
      mean[k] = ofProj[it.id] ? grank[ofProj[it.id]] : it.ord / span;
    });
    list.sort(function(a, b){
      var ka = key[a.id], kb = key[b.id];
      // 무게중심이 같으면 같은 프로젝트끼리 먼저 묶는다. 차례로만 가르면 남이 사이에
      // 낀 채로 남는다
      return (mean[ka] - mean[kb]) || (ka < kb ? -1 : ka > kb ? 1 : 0)
          || (a.ord - b.ord);
    });
    list.forEach(function(it, k){ it.ord = k; });
  });

  // 타겟은 제 칸 맨 위에 앉는다. 그래야 왼쪽은 전부 타겟보다 아래에 서고(선이 위로만
  // 꺾인다), 오른쪽도 전부 아래에 서서(선이 아래로만 꺾인다) 흐름이 한 방향으로 읽힌다
  used.forEach(function(c){
    var list = byCol[c], fi = -1;
    for (var i = 0; i < list.length; i++)
      if (list[i].n && list[i].n.data && list[i].n.data.focal) { fi = i; break; }
    if (fi > 0) list.unshift(list.splice(fi, 1)[0]);
  });

  // 자리는 타겟 칸에서 바깥으로 한 칸씩 나가며 잡는다. 칸 안에서는 차례대로 위에서
  // 아래로 붙여 앉히되, 한 상자는 타겟 쪽 이웃보다 위로 올라가지 못한다(바닥값). 그래야
  // 왼쪽 선은 위로만, 오른쪽 선은 아래로만 꺾인다 — 방향은 꺾는 쪽이 아니라 앉히는
  // 쪽이 보장한다. 차례는 위에서 정한 것을 그대로 쓴다
  var where = {};
  used.forEach(function(c, i){
    byCol[c].forEach(function(it){ where[it.id] = i; });
  });
  function cyOf(it){ return it.top + it.h / 2; }
  // 빈 자리가 닿을 상자보다 아래로 밀려났을 때 그 상자를 내리는 바닥값. 아래로만 민다
  var push = {};
  function packCol(i, toward){
    var y = 0, prevProj = null;
    byCol[used[i]].forEach(function(it, k){
      it.ord = k;
      // 프로젝트 테두리가 바뀌는 자리에는 이름이 들어갈 여백을 둔다 — 안 두면 아래
      // 테두리의 이름이 위 테두리의 마지막 식구 상자를 덮는다
      var pj = it.dummy ? null : (ofProj[it.id] || null);
      if (k > 0 && pj !== prevProj) {
        if (prevProj) y += PROJ_PAD_X;
        if (pj) y += PROJ_PAD_Y;
      }
      prevProj = pj;
      var floor = push[it.id] || 0;
      (nbr[it.id] || []).forEach(function(x){
        if (where[x] !== toward) return;
        var nb = byCol[used[toward]].filter(function(q){ return q.id === x; })[0];
        if (nb && nb.top !== undefined) floor = Math.max(floor, cyOf(nb) - it.h / 2);
      });
      // 칸을 건너뛰는 선이 잡아 둔 빈 자리는 그 선이 닿을 상자와 같은 높이로 내린다.
      // 그래야 선이 첫 통로에서 한 번 꺾고 그 높이로 곧게 지나간다 — 중간 칸마다
      // 다시 꺾지 않는다
      if (it.want !== undefined && it.want !== null)
        floor = Math.max(floor, it.want - it.h / 2);
      it.top = Math.max(y, floor);
      y = it.top + it.h + ROW_GAP;
    });
  }
  var fcol = 0;
  used.forEach(function(c, i){
    byCol[c].forEach(function(it){
      if (it.n && it.n.data && it.n.data.focal) fcol = i;
    });
  });
  // 타겟 칸 — 타겟은 맨 위에 못박고, 칸을 건너뛰는 선의 빈 자리는 제 높이(want)에 앉는다
  function packFocal(){
    var y = 0;
    byCol[used[fcol]].forEach(function(it, k){
      it.ord = k;
      var floor = (it.want !== undefined && it.want !== null) ? it.want - it.h / 2 : 0;
      it.top = Math.max(y, floor);
      y = it.top + it.h + ROW_GAP;
    });
  }
  // 칸 안 차례를 지금 높이로 다시 맞춘다. 빈 자리는 닿을 상자 높이(want)로 센다 —
  // 빈 자리 차례와 닿을 상자 차례가 어긋나면 서로 밀어내며 끝없이 내려간다
  function resort(){
    used.forEach(function(c, i){
      if (i === fcol) return;
      var list = byCol[c];
      list.forEach(function(it, k){
        it.key = (it.dummy && it.want !== undefined && it.want !== null) ? it.want
               : (it.top === undefined ? k * 1e6 : cyOf(it));
      });
      list.sort(function(a, b){
        return (a.key - b.key) || (dummyRank(a) - dummyRank(b)) || (a.ord - b.ord);
      });
      list.forEach(function(it, k){ it.ord = k; });
    });
  }
  function packAll(){
    packFocal();
    for (var li = fcol - 1; li >= 0; li--) packCol(li, li + 1);
    for (var ri = fcol + 1; ri < used.length; ri++) packCol(ri, ri - 1);
  }
  packAll();
  // 빈 자리 높이를 닿을 상자에 맞출 때까지 쓴다. 빈 자리는 닿을 상자 높이를 바닥값으로
  // 받고, 그래도 위 상자에 밀려 더 내려갔으면 닿을 상자를 그 높이로 내린다(왼쪽 —
  // 오른쪽은 바닥값이 이미 민다). 자리는 아래로만 움직이므로 되풀이하면 제자리에 선다.
  // 이것이 「중간 상자를 피하려고 다시 꺾지 않는다」를 route 가 아니라 place 가 지키는
  // 자리다 — 선이 닿을 높이에서 중간 칸이 비어 있게 만든다. 타겟은 밀지 않는다
  var spot = {}, eById = {};
  used.forEach(function(c){ byCol[c].forEach(function(it){ spot[it.id] = it; }); });
  edges.forEach(function(x){ eById[x.id] = x; });
  var span0 = 0;
  used.forEach(function(c){ byCol[c].forEach(function(it){ span0 += it.h + ROW_GAP; }); });
  for (var pass = 0; pass < 40; pass++){
    var moved = false;
    Object.keys(span).forEach(function(eid){
      var e = eById[eid];
      if (!e) return;
      var t = spot[e.target];
      if (!t || t.top === undefined) return;
      var ty = cyOf(t);
      span[eid].forEach(function(did){
        var d = spot[did];
        if (!d) return;
        if (d.want !== ty) { d.want = ty; moved = true; }
        var dy = cyOf(d) - ty;
        if (dy > 1 && !(t.n && t.n.data && t.n.data.focal)) {
          var need = t.top + dy;
          if ((push[t.id] || 0) < need - 0.5) { push[t.id] = need; moved = true; }
        }
      });
    });
    if (!moved) break;
    resort();
    packAll();
    // 판이 상자 높이 합의 세 배를 넘게 자라면 서로 밀어내는 고리다. 멈추고 route 가 비킨다
    var deep = 0;
    used.forEach(function(c){ byCol[c].forEach(function(it){
      if (it.top + it.h > deep) deep = it.top + it.h; }); });
    if (deep > span0 * 3) {
      if (window.console) console.warn('vc place: 빈 자리 맞추기가 ' + pass + ' 번에 안 멈춰 끊는다');
      break;
    }
  }

  // 칸마다 위아래 여백을 없애고 전체를 가운데로 모은다
  var lo = 1e9, hi = -1e9;
  used.forEach(function(c){
    byCol[c].forEach(function(it){
      if (it.top < lo) lo = it.top;
      if (it.top + it.h > hi) hi = it.top + it.h;
    });
  });
  var mid = (lo + hi) / 2;

  var out = [], geo = {};
  used.forEach(function(c, i){
    var x = i * (COL_W + COL_GAP);
    byCol[c].forEach(function(it){
      var y = it.top - mid + (hi - lo) / 2 + HDR_H + HDR_GAP;
      geo[it.id] = { x:x, y:y, h:it.h, col:i };
      if (!it.dummy) out.push(Object.assign({}, it.n, { position:{ x:x, y:y } }));
    });
    if (COLS[c]) {
      // 다른 회사를 중심에 놓으면 왼쪽 칸은 사슬 층이 아니라 그 회사에서 몇 단 앞인가다.
      // 사슬의 층(원재료·소재…)은 사슬의 타겟 기준이라 다른 타겟에 못 쓴다
      var hl = COLS[c].label, hn = COLS[c].note || null;
      if (COLS[c].key === 'REVENUE_AXIS' && opts.revenueLabel) hl = opts.revenueLabel;
      if (opts.rooted && HOP_LABEL[COLS[c].key]) {
        hl = HOP_LABEL[COLS[c].key]; hn = '이어진 단 수';
      }
      out.push({ id:'hdr|' + c, type:'hdr', draggable:false, selectable:false,
        connectable:false, position:{ x:x, y:0 }, data:{ label: hl, note: hn } });
    }
  });

  // 프로젝트 테두리 — 식구 상자의 둘레에 여백을 둘러 잡는다(상자를 다 앉힌 뒤
  // 식구 bounding box + 여백). 식구는 projects.json 이 명시한 것뿐이고 타겟은 늘 밖이다
  projs.forEach(function(pn){
    var ids = (pn.data.mem || []).filter(function(id){ return geo[id]; });
    if (!ids.length) return;
    var x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9, col = 99;
    ids.forEach(function(id){
      var g = geo[id];
      x1 = Math.min(x1, g.x); x2 = Math.max(x2, g.x + COL_W);
      y1 = Math.min(y1, g.y); y2 = Math.max(y2, g.y + g.h);
      col = Math.min(col, g.col);
    });
    var px = x1 - PROJ_PAD_X, py = y1 - PROJ_PAD_Y;
    var pw = (x2 - x1) + PROJ_PAD_X * 2, ph = (y2 - y1) + PROJ_PAD_Y + PROJ_PAD_X;
    // 이름은 맨 위 식구 상자 바로 위에 둔다. 그 자리는 packCol 이 비워 둔 띠라 다른
    // 상자가 못 선다. 테두리 왼쪽 위에 두면 다른 칸의 남의 상자와 겹친다
    var topId = ids.slice().sort(function(p, q){ return geo[p].y - geo[q].y; })[0];
    var lx = geo[topId].x - px;
    // 테두리는 칸마다 한 조각이다. 칸을 가로지르는 한 상자로 두르면 사이에 선 남의 상자와
    // 다른 프로젝트 띠까지 삼킨다. 조각은 그 칸의 식구만 두른다
    var byc = {};
    ids.forEach(function(id){ var g = geo[id]; (byc[g.col] = byc[g.col] || []).push(g); });
    var segs = Object.keys(byc).map(function(c){
      var gs = byc[c], sy1 = 1e9, sy2 = -1e9;
      gs.forEach(function(g){ sy1 = Math.min(sy1, g.y); sy2 = Math.max(sy2, g.y + g.h); });
      return { x: gs[0].x - PROJ_PAD_X - px, y: sy1 - PROJ_PAD_Y - py,
               w: COL_W + PROJ_PAD_X * 2, h: (sy2 - sy1) + PROJ_PAD_Y + PROJ_PAD_X };
    });
    geo[pn.id] = { x:px, y:py, h:ph, col:col, proj:true };
    out.push(Object.assign({}, pn, { position:{ x:px, y:py }, zIndex:-1,
      draggable:false, selectable:false,
      data: Object.assign({}, pn.data, { w:pw, h:ph, lx:lx, segs:segs }) }));
  });

  route(edges, geo, fcol);
  return out;
}

function readUrl(first){
  var q = new URLSearchParams(location.search);
  // 처음 열 때는 늘 가장 최신 해다. 주소에 옛 해가 남아 있어도 최신으로 연다.
  // 앱 안에서 오간 뒤(뒤로 가기)에는 그때 보던 해를 지킨다
  // 주소에 아무것도 안 달린 채로 들어오면 「맨 처음」이다.
  // history.state 는 새로고침해도 남아서 기준으로 못 쓴다
  var fresh = first && !location.search;
  var y = q.get('year');
  if (fresh) y = NOW;
  if (YEARS.indexOf(y) < 0) y = NOW;
  // 장을 열면 늘 회사 목록부터다. 주소에 탭이 적혀 있을 때만 그 탭으로 연다
  // (새로고침·북마크로 들어와도 같다 — 주소에 남은 focal·year 는 그대로 지킨다)
  var md = q.get('mode') || 'current';
  var sel = q.get('sel') || '';
  if (sel.slice(0, 5) === 'lane|') sel = '';   // 알약은 새로 열 때 고른 것으로 안 친다
  return { focal: q.get('focal') || HOME, year: y,
           mode: md, chain: q.get('chain') || null,
           open: (q.get('open') || '').split(',').filter(Boolean),
           sel: sel };
}
function writeUrl(s, push){
  var q = new URLSearchParams();
  q.set('focal', s.focal); q.set('year', s.year);
  if (s.chain) q.set('chain', s.chain);
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

// 판매 사슬은 층이 있다 — 직접 고객 → 중개 → 간접 고객. 프로젝트는 층이 아니라 테두리다.
// 층 수를 미리 정하지 않고 데이터에 있는 만큼만 따라간다
// 한 상자를 누르면 그 상자의 다음 한 칸만 열린다. 저절로 번지지 않는다

// 05 §16 — 공급사를 전부 중심에 바로 붙이지 않는다. 확인된 만큼만 위로 올라간다

// 사슬 하나를 통째로 세운다. 연도가 무엇이 보일지 정하고, 고른 상자가 무엇이 진할지 정한다.
// 눌러야 노드가 생기는 방식은 걷었다
function inChain(ck, id){
  return !!CHAINS[ck] && CHAINS[ck].relationships.some(function(r){
    return r.source_entity === id || r.target_entity === id; });
}
function chainOf(focal, hint){
  if (hint && inChain(hint, focal)) return hint;
  var best = null;
  Object.keys(CHAINS).forEach(function(ck){
    if (best) return;
    var m = CHAINS[ck].meta || {};
    if (m.focal_entity === focal) best = ck;
  });
  if (best) return best;
  Object.keys(CHAINS).forEach(function(ck){
    if (best) return;
    if (CHAINS[ck].relationships.some(function(r){
      return r.source_entity === focal || r.target_entity === focal; })) best = ck;
  });
  return best;
}

// 거래가 아닌 관계로 붙은 상자에는 고객이라는 이름을 안 쓴다. 무슨 사이인지 적는다
var ROLE_KO = { PLATFORM_EXPOSURE:'수요 노출', QUALIFICATION:'인증',
  ULTIMATE_COMMERCIAL_USER:'최종 수요처', SERVES_END_USER:'최종 수요처',
  UTILITY_SERVES:'전력 공급', CUSTOMERS_CUSTOMER:'고객의 고객',
  END_USER_DEPLOYMENT:'설치·배치', SERVES_END_MARKET:'전방시장',
  DEVELOPS:'개발', HOLDS_PROJECT:'보유', OWNS_SITE:'부지 소유',
  OPERATES_SITE:'부지 운영', USES_SITE:'부지 이용', PROJECT_SUPPLY:'프로젝트 납품',
  DEPLOYS_AT_SITE:'설치 부지', SUPPLIES:'공급', FINANCES:'금융',
  PROJECT_FINANCE:'프로젝트 금융', CREDIT_SUPPORT:'신용 보강', INVESTS_IN:'투자',
  OPERATES_THROUGH:'운영 자회사', EXECUTES_THROUGH:'실행 법인',
  END_CUSTOMER_SUPPLY_CHAIN:'공급망 목록', DISTRIBUTION_PARTNERSHIP:'유통 제휴',
  INDIRECT_CUSTOMER_UNDISCLOSED:'고객 · 비공개' };
var CONTRACT_KO = { CONFIRMED:'계약 고객 확인', NOT_CONTRACTUAL:'계약 고객 아님',
  UNVERIFIED:'계약 고객 미확인' };
var CONTRACT_NOTE = { CONFIRMED:'계약상 구매 주체라는 근거가 있다',
  NOT_CONTRACTUAL:'원문이 구매 주체가 아니라고 한다(고객의 고객)',
  UNVERIFIED:'설치처·수요 노출·인증·공급망 목록 — 계약상 구매 주체라는 근거가 없다' };

// 띠와 갈림목에 적는 값은 한 갈래뿐이다 — 매출원은 총매출 대비 비중, 공급원은 조달 비중.
// 가동률·전방 구성처럼 다른 것을 세는 값은 숫자를 안 적고 손 얹었을 때만 보여 준다
var SHARE_METRIC = { rt:/revenue.*share$/,
                     ss:/(sourcing|purchase|supply|bom|cost).*share$/ };
function isShare(kind, sh){
  return PCT[sh.unit] && SHARE_METRIC[kind].test(sh.metric || '');
}
// 고른 해를 덮는 비중이 있으면 그것, 없으면 그 해 이전의 가장 최근 값을 기간표를 달아
// 돌려준다(stale). 대덕전자 매입 비중은 FY2025 공시가 최신이라 2026 화면에서 숨기면
// 있는 값이 없는 것처럼 보인다 — 값은 보이되 언제 것인지 칩에 적는다
function pickShare(kind, x, year){
  var y = parseInt(year, 10), cover = null, prev = null, prevY = -1;
  (x.shares || []).forEach(function(sh){
    if (!isShare(kind, sh) || sh.value === null || sh.value === undefined) return;
    var a = y4(sh.period_start) || y4(sh.as_of_date);
    var b = y4(sh.period_end) || y4(sh.as_of_date) || a;
    if (!a) return;
    if (a <= y && y <= b) { if (!cover || b > (y4(cover.period_end) || 0)) cover = sh; }
    else if (b < y && b > prevY) { prevY = b; prev = sh; }
  });
  if (cover) return cover;
  return prev ? Object.assign({}, prev, { stale: true }) : null;
}
// 한 줄의 분모는 하나다. 그 줄에서 가장 많이 쓰인 분모의 값만 적고, 분모가 다른
// 값(가동률·전방 구성)은 손 얹었을 때만 분모와 함께 보여 준다 — 나란히 찍으면 더한다
function rowDen(kind, list, year){
  var cnt = {}, best = null;
  list.forEach(function(x){
    var sh = pickShare(kind, x, year);
    if (!sh || !sh.denominator) return;
    cnt[sh.denominator] = (cnt[sh.denominator] || 0) + 1;
    if (best === null || cnt[sh.denominator] > cnt[best]) best = sh.denominator;
  });
  return best;
}

// 공급원·매출원 차례 — 비중 높은 것이 위. 같은 분모 값이 먼저, 다른 분모 값이 그 다음,
// 값 없는 것, 미상 순. 띠의 칩과 판의 알약이 같은 차례를 쓴다
function orderCls(kind, list, year){
  var den = rowDen(kind, list, year);
  return list.slice().sort(function(a, b){
    function key(x){
      if (x.unallocated) return [3, 0];
      var sh = pickShare(kind, x, year);
      if (!sh) return [2, 0];
      return [den && sh.denominator === den ? 0 : 1, -(sh.value || 0)];
    }
    var ka = key(a), kb = key(b);
    return (ka[0] - kb[0]) || (ka[1] - kb[1]) || (a.label < b.label ? -1 : 1);
  });
}

// ── 자리 매기기 — 타겟에서 실제로 이어진 꼴로 ──────────────────────
// 다운스트림 칸은 관계 종류가 아니라 타겟에서 몇 홉 떨어졌나와 사이에 중개가 끼었나로
// 정한다(프레임워크 §22-B). 1홉이면 직접 고객, 2홉부터는 간접 고객, 중개 노릇(데이터가
// 준 tier INTERMEDIARY)이면 중개. 계약상 구매 주체인지는 칸이 아니라 서랍의 근거 칸
// (contractual_customer)이다. 전방시장은 사슬의 다음 단계가 아니라 다른 축이다.
// 타겟에서 앞으로 안 닿는데 앞쪽 상자에 선을 대는 상자(개발사·부지 소유·금융)는 그
// 상자 뒤 칸에 노릇 이름으로 선다 — 타겟과 바로 거래하지 않는 쪽이다.
// 왼쪽(공급)은 사슬의 타겟이면 데이터의 층(tier)으로, 다른 회사를 중심에 놓으면 그
// 회사에서 몇 단 앞인가로 센다 — 층은 사슬의 타겟 기준이라 남의 중심에 그대로 못 쓴다.
// 반환: { col, sub, via, rooted }. col 이 없는 상자는 이 중심의 사슬 밖이다
function topology(focal, rels, rooted){
  var mid = {};
  rels.forEach(function(r){
    if (r.target_tier === 'INTERMEDIARY') mid[r.target_entity] = 1;
    if (r.source_tier === 'INTERMEDIARY') mid[r.source_entity] = 1;
  });
  var fwd = {}, back = {};
  rels.forEach(function(r){
    (fwd[r.source_entity] = fwd[r.source_entity] || []).push(r);
    (back[r.target_entity] = back[r.target_entity] || []).push(r);
  });
  var col = {}, sub = {}, via = {}, depth = {};
  col[focal] = COL_OF.FOCAL; depth[focal] = 0;
  // ① 앞으로 — 사슬의 타겟은 다운스트림 갈래만, 다른 중심은 선이 가는 쪽을 따른다
  //    (기업 구조 선은 흐름이 아니라 소유라 안 따른다)
  var q = [focal];
  while (q.length){
    var cur = q.shift();
    (fwd[cur] || []).forEach(function(r){
      if (rooted ? r.lane === 'CORPORATE' : r.lane !== 'DOWNSTREAM') return;
      var t = r.target_entity;
      if (depth[t] !== undefined) return;
      depth[t] = depth[cur] + 1; via[t] = r; q.push(t);
    });
  }
  // 칸은 가장 짧은 홉이 아니라 가장 긴 홉이다 — 어떤 상자를 가리키는 상자보다 한 칸은
  // 오른쪽에 선다. 짧은 홉으로 세우면 오라클→프로젝트 주피터처럼 같은 칸 안에서 가리키는
  // 선이 생긴다. 고리가 있으면 여섯에서 멈춘다
  for (var pass = 0; pass < 8; pass++){
    var changed = false;
    Object.keys(depth).forEach(function(u){
      (fwd[u] || []).forEach(function(r){
        if (r.lane === 'CORPORATE') return;
        var t = r.target_entity;
        if (t === focal || depth[t] === undefined) return;
        var d = Math.min(6, depth[u] + 1);
        if (d > depth[t]) { depth[t] = d; changed = true; }
      });
    });
    if (!changed) break;
  }
  Object.keys(depth).forEach(function(id){
    if (id === focal) return;
    var e = ENT[id] || {}, r = via[id];
    if (e.entity_type === 'application') {
      col[id] = COL_OF.END_MARKET; sub[id] = '전방시장'; return;
    }
    if (mid[id]) { col[id] = COL_OF.INTERMEDIARY; sub[id] = '중개'; return; }
    if (depth[id] === 1) {
      col[id] = COL_OF.CONTRACTUAL_CUSTOMER;
      sub[id] = r.contractual_customer === 'CONFIRMED' ? '직접 고객'
              : (ROLE_KO[r.relationship_type] || relKo(r.relationship_type));
      return;
    }
    col[id] = depth[id] >= 5 ? COL_OF.END_USER_4 : depth[id] === 4 ? COL_OF.END_USER_3
            : (depth[id] === 3 ? COL_OF.END_USER_2 : COL_OF.END_USER);
    sub[id] = (r.relationship_type === 'INDIRECT_CUSTOMER_UNDISCLOSED' || e.anon)
      ? '간접 고객 · 비공개' : '간접 고객';
  });
  // ② 뒤로 — 공급. 사슬의 타겟은 층으로, 다른 중심은 홉으로
  var hop = {};
  q = [focal]; hop[focal] = 0;
  while (q.length){
    var cur2 = q.shift();
    (back[cur2] || []).forEach(function(r){
      if (rooted ? r.lane === 'CORPORATE' : r.lane === 'DOWNSTREAM') return;
      var s = r.source_entity;
      if (hop[s] !== undefined || col[s] !== undefined) return;
      hop[s] = hop[cur2] + 1; via[s] = r; q.push(s);
    });
  }
  function tierCol(id){
    // 층이 적힌 선이 자리를 정한다. 어느 선에도 층이 없으면 처음 닿은 선의 갈래로 앉힌다
    var hit = null;
    (fwd[id] || []).forEach(function(r){
      if (hit) return;
      var t = TIER_ALIAS[r.source_tier] || r.source_tier;
      if (t && COL_OF[t] !== undefined) hit = { col: COL_OF[t], tier: t };
    });
    if (hit) return hit;
    return { col: colOfRel(via[id], true), tier: null };
  }
  Object.keys(hop).forEach(function(id){
    if (id === focal) return;
    if (rooted) {
      col[id] = HOP_COL[Math.min(hop[id], HOP_COL.length) - 1];
      sub[id] = hop[id] === 1 ? '바로 앞' : hop[id] + '단 앞';
      return;
    }
    var tc = tierCol(id);
    col[id] = tc.col;
    sub[id] = TIER_KO[tc.tier] || via[id].component || null;
  });
  // ③ 타겟에서 안 닿지만 앉힌 상자에 선을 대는 상자 — 개발사·부지 소유·금융·운영 법인.
  //    사슬의 타겟일 때만이다. 다른 회사를 중심에 놓으면 그 회사에서 이어진 것만 그린다
  //    (미상 자리표를 같이 쓰는 남의 중개까지 딸려 들어온다)
  var again = !rooted;
  while (again){
    again = false;
    rels.forEach(function(r){
      var s = r.source_entity, t = r.target_entity;
      if (col[s] !== undefined || col[t] === undefined) return;
      if (col[t] < COL_OF.FOCAL) return;
      if (ENT[t] && ENT[t].entity_type === 'application') return;
      col[s] = mid[s] ? COL_OF.INTERMEDIARY
             : (t === focal ? COL_OF.CONTRACTUAL_CUSTOMER
                : Math.min(Math.max(col[t] + 1, COL_OF.END_USER), COL_OF.END_USER_4));
      sub[s] = mid[s] ? '중개' : (ROLE_KO[r.relationship_type] || relKo(r.relationship_type));
      via[s] = r; again = true;
    });
  }
  // ④ 그래도 자리가 없는 상자 — 사슬의 타겟이면 옛 갈래 규칙으로 앉히고, 다른 중심이면
  //    이 중심의 사슬 밖이라 그리지 않는다
  if (!rooted) {
    rels.forEach(function(r){
      if (col[r.source_entity] === undefined) {
        col[r.source_entity] = colOfRel(r, true); via[r.source_entity] = r;
        sub[r.source_entity] = TIER_KO[r.source_tier] || r.component || null;
      }
      if (col[r.target_entity] === undefined) {
        col[r.target_entity] = colOfRel(r, false); via[r.target_entity] = r;
        sub[r.target_entity] = TIER_KO[r.target_tier] || r.component || null;
      }
    });
  }
  return { col: col, sub: sub, via: via, rooted: rooted };
}

function buildGraph(focal, year, sel, axis, hint, open){
  var ck = chainOf(focal, hint);
  var rels = ck ? CHAINS[ck].relationships : relsOf(focal);
  // 사슬의 타겟이 아닌 회사를 중심에 놓으면 판을 그 회사 기준으로 다시 세운다(re-root).
  // 층(tier)을 그대로 쓰지 않는다
  var rooted = !ck || ((CHAINS[ck].meta || {}).focal_entity !== focal);
  // 그 해에 살아 있는 관계만 판에 있다(프레임워크 §19). 2025 판에서는 2026 에 생긴 것이
  // 아무리 눌러도 안 나오고, 2026 판에서는 그 전에 끝난 것이 안 나온다. 흐리게 두던
  // 옛 방식은 걷었다 — 흐린 상자도 누르면 펴졌다
  rels = rels.filter(function(r){ return activeIn(r, year); });
  var tp = topology(focal, rels, rooted);
  var nodes = [], edges = [], seen = {};
  var selId = sel ? (sel.entity || sel.id) : null;

  function addNode(id){
    if (seen[id] || tp.col[id] === undefined) return;
    seen[id] = 1;
    var isFocal = id === focal, r = tp.via[id];
    nodes.push({ id: id, type:'nd', data:{
      title: nm(id), flag: flagOf(id), ico: iconOf(id),
      kind: KIND_OF[(ENT[id] || {}).entity_type] || 'ent',
      focal: isFocal, col: tp.col[id],
      sub: isFocal ? ((ENT[focal] || {}).country || null) : (tp.sub[id] || null),
      ref:{ kind: r ? 'rel' : 'ent', id: r ? r.id : id, entity: id,
            up: r ? r.source_entity === id : false } } });
  }
  addNode(focal);
  rels.forEach(function(r){ addNode(r.source_entity); addNode(r.target_entity); });

  // 공급원·매출원은 선이 지나는 갈림목이다. 소재·가공에서 타겟으로 드는 선은 공급원을,
  // 타겟에서 직접 고객으로 나가는 선은 매출원을 거친다 — 타겟에서 고객으로 바로 가지
  // 않는다. 갈림목은 회사가 아니라 분류라 회사 상자는 복제되지 않고, 한 회사가 두 분류에
  // 들면 갈림목 둘에서 선이 온다(N:M). 귀속 근거가 없으면 「미상」 갈림목을 지난다.
  // 사슬의 타겟일 때만 선다 — 분류가 그 타겟 기준이라 다른 회사 중심에는 못 쓴다
  var m = clsOf(ck), laneOf = {}, trunk = {};
  function laneId(kind, id){ return 'lane|' + kind + '|' + id; }
  if (!rooted) {
    [['ss', m.ssList, COL_OF.SUPPLY_AXIS], ['rt', m.rtList, COL_OF.REVENUE_AXIS]]
    .forEach(function(row){
      var kind = row[0], list = orderCls(kind, row[1], year), den = rowDen(kind, list, year);
      list.forEach(function(x, xi){
        var sh = pickShare(kind, x, year), lid = laneId(kind, x.id);
        var rl = [];
        laneOf[lid] = { kind: kind, cls: x, rels: rl };
        seen[lid] = 1;
        nodes.push({ id: lid, type:'nd', data:{
          title: x.label, kind:'lane', col: row[2], un: !!x.unallocated, fixOrd: xi,
          // 실명 매핑 밖의 잔여가 비공개인 매출원은 알약에 그 뜻을 단다(잔여 칸은 상자가 아니다)
          sub: x.residual ? x.residual.label : null,
          share: (sh && den && sh.denominator === den)
            ? sh.value + '%' + (sh.stale ? ' ' + (sh.period || '') : '') : null,
          ref:{ kind:'grp', id: lid, label: x.label, rels: rl, up: kind === 'ss',
                lane: kind === 'ss' ? 'MANUFACTURING_BOM' : 'DOWNSTREAM',
                cls: kind + ':' + x.id, chain: ck } } });
      });
    });
  }
  function bandOf(r){
    if (rooted) return null;
    if (r.target_entity === focal && r.lane !== 'DOWNSTREAM'
        && (r.supply_source_ids || []).length) return 'ss';
    if (r.source_entity === focal && r.lane === 'DOWNSTREAM'
        && (r.revenue_type_ids || []).length) return 'rt';
    return null;
  }
  function mapOf(r, band, cid){
    var list = (band === 'ss' ? r.supply_source_map : r.revenue_type_map) || [];
    return list.filter(function(m){ return m.id === cid; })[0] || null;
  }
  // 화살촉은 선 굵기를 따라 커지지 않는다(markerUnits) — 굵은 비중선의 촉이 상자만 해졌다
  function marker(color){
    return { type: MarkerType.ArrowClosed, width:11, height:11, color: color,
             markerUnits:'userSpaceOnUse', strokeWidth:0 };
  }

  rels.forEach(function(r){
    if (!seen[r.source_entity] || !seen[r.target_entity]) return;
    var on = activeIn(r, year), fy = firstYear(r);
    var st = Object.assign({}, evStyle(r.evidence_level));
    if (!on) st.opacity = 0.28;
    var lbl = shareLabel(r.id, year);
    // 선 굵기는 근거 등급만 말한다. 비중을 굵기로 옮겨 봤으나(2026-09-12) 비중이 붙은
    // 선이 몇 안 되어 굵은 선 하나가 잘못 그린 것처럼 보였다. 비중은 상자의 숫자가 말한다
    if (lbl) {
      // 값은 focal 이 아닌 쪽 상자에 붙인다. 선 위에 얹으면 선을 가린다
      var holder = r.target_entity === focal ? r.source_entity : r.target_entity;
      var hn = nodes.filter(function(n){ return n.id === holder; })[0];
      if (hn && !hn.data.share) {
        hn.data.share = lbl;
        if (lbl === '?') {
          var ys = {};
          (OBS_BY_REL[r.id] || []).forEach(function(o){
            if (!PCT[o.unit] || !onEdge(o) || o.value === null && o.value_low === null) return;
            var yy = y4(o.period_end) || y4(o.as_of_date);
            if (yy) ys[yy] = 1;
          });
          hn.data.shareYears = Object.keys(ys).sort();
        }
      }
    }
    var band = bandOf(r);
    if (!band) {
      edges.push({ id:'e-' + r.id, source: r.source_entity, target: r.target_entity,
        style: st, data:{ rel: r.id, on: on },
        markerEnd: marker(evStyle(r.evidence_level).stroke), type:'smoothstep' });
    } else {
      var ids = band === 'ss' ? r.supply_source_ids : r.revenue_type_ids;
      ids.forEach(function(cid){
        var lid = laneId(band, cid);
        if (!laneOf[lid]) return;
        laneOf[lid].rels.push(r.id);
        var key = band + ':' + cid;
        // 귀속마다 근거 등급이 다르다 — Apple 은 커패시터에는 확인, 인덕터에는 추론
        var mp = mapOf(r, band, cid), lvl = mp ? mp.status : r.evidence_level;
        var st2 = Object.assign({}, evStyle(lvl));
        if (!on) st2.opacity = 0.28;
        edges.push({ id:'e-' + r.id + '|' + cid,
          source: band === 'ss' ? r.source_entity : lid,
          target: band === 'ss' ? lid : r.target_entity,
          style: st2, data:{ rel: r.id, on: on, cls: key, map: mp || null },
          markerEnd: marker(evStyle(lvl).stroke), type:'smoothstep' });
        // 갈림목과 타겟 사이 줄기는 갈림목마다 하나다. 그 갈림목을 지나는 선이 하나라도
        // 그 해에 살아 있으면 진하다
        var tk = trunk[lid];
        if (!tk) {
          tk = trunk[lid] = { id:'e-trunk|' + lid,
            source: band === 'ss' ? lid : focal, target: band === 'ss' ? focal : lid,
            style: Object.assign({}, EV_STYLE.CONFIRMED),
            data:{ rel: null, cls: key, on: false, rels: [] },
            markerEnd: marker(EV_STYLE.CONFIRMED.stroke), type:'smoothstep' };
          edges.push(tk);
        }
        tk.data.rels.push(r.id);
        if (on) tk.data.on = true;
      });
    }
    var t = nodes.filter(function(n){ return n.id === r.target_entity; })[0];
    if (t && on && fy === year && fy !== YEARS[0]) t.data.isNew = true;
  });
  Object.keys(trunk).forEach(function(k){
    if (!trunk[k].data.on) trunk[k].style.opacity = 0.28;
  });

  // 필요한 것만 먼저 보인다 — 타겟과 공급원·매출원 갈림목. 갈림목이나 상자를 누르면 그것에
  // 닿은 다음 홉만 편다(open). '*' 는 전부. 안 보이는 이웃 수는 +N 배지로 상자에 단다.
  // 판 전체를 한 번에 그리면 블룸은 상자 100개라 무엇을 봐야 할지 잃는다
  open = open || [];
  var all = open.indexOf('*') >= 0 || rooted;
  var vis = {};
  vis[focal] = 1;
  nodes.forEach(function(n){ if (n.data.kind === 'lane') vis[n.id] = 1; });
  var adj = {};
  edges.forEach(function(e){
    (adj[e.source] = adj[e.source] || []).push(e.target);
    (adj[e.target] = adj[e.target] || []).push(e.source);
  });
  if (all) nodes.forEach(function(n){ vis[n.id] = 1; });
  else open.forEach(function(o){ (adj[o] || []).forEach(function(x){ vis[x] = 1; }); });
  nodes.forEach(function(n){
    if (!vis[n.id]) return;
    var hid = 0;
    (adj[n.id] || []).forEach(function(x){ if (!vis[x] && x !== focal) hid++; });
    // 같은 이웃이 여러 선으로 닿으면 한 번만 센다
    var uniq = {};
    (adj[n.id] || []).forEach(function(x){ if (!vis[x] && x !== focal) uniq[x] = 1; });
    n.data.more = Object.keys(uniq).length || null;
    n.data.opened = open.indexOf(n.id) >= 0;
  });
  nodes = nodes.filter(function(n){ return vis[n.id]; });
  edges = edges.filter(function(e){ return vis[e.source] && vis[e.target]; });

  // 프로젝트는 칸도 상자도 아니다. projects.json 이 명시한 식구를 두르는 테두리다.
  // SPV·부지는 실제 법인이라 상자로 선다. 타겟은 늘 테두리 밖이고 선은 테두리에 안 닿는다
  ((ck && CHAINS[ck].projects) || []).forEach(function(p){
    var mem = (p.members || []).filter(function(m){ return m !== focal && seen[m] && vis[m]; });
    if (!mem.length) return;
    nodes.push({ id:'proj|' + p.id, type:'proj',
      data:{ title: p.name_ko || p.name, mem: mem, pid: p.id } });
  });

  // 그 해에 걸린 선이 하나도 없는 상자는 흐리게 둔다
  var live = {};
  edges.forEach(function(e){
    if (e.data && e.data.on) { live[e.source] = 1; live[e.target] = 1; }
  });
  nodes.forEach(function(n){
    if (n.id !== focal && !live[n.id]) n.data.gone = true;
  });

  // 고른 상자와 거기 바로 닿는 것만 진하게
  if (selId && seen[selId]) {
    // 고른 상자를 지나는 줄 전체를 진하게 — 앞으로는 닿는 곳까지, 뒤로는 오는 곳까지
    // (원재료 → … → 간접 고객). 바로 옆 한 홉만 진하면 사슬이 안 보인다
    var near = {};
    near[selId] = 1;
    var fwdE = {}, bakE = {};
    edges.forEach(function(e){
      (fwdE[e.source] = fwdE[e.source] || []).push(e.target);
      (bakE[e.target] = bakE[e.target] || []).push(e.source);
    });
    // 타겟에서는 더 안 나간다 — 타겟을 지나면 반대쪽 판 전체가 켜진다
    [fwdE, bakE].forEach(function(g){
      var q = [selId];
      while (q.length){
        var c = q.shift();
        if (c === focal && c !== selId) continue;
        (g[c] || []).forEach(function(x){ if (!near[x]) { near[x] = 1; q.push(x); } });
      }
    });
    nodes = nodes.map(function(n){
      if (n.id === selId)
        return Object.assign({}, n, { data: Object.assign({}, n.data, { sel:true }) });
      return near[n.id] ? n
        : Object.assign({}, n, { data: Object.assign({}, n.data, { dim:true }) });
    });
    edges = edges.map(function(e){
      var hit = near[e.source] && near[e.target];
      return Object.assign({}, e, { style: Object.assign({}, e.style,
        { opacity: hit ? 1 : 0.35 }) });
    });
  }
  // 공급원·매출원 띠에서 하나를 고르면 그 분류에 걸린 줄만 진하게 남는다.
  // 상자를 숨기지는 않는다 — 연도가 무엇이 서 있나를 정하고, 고르는 일은 강조만 바꾼다
  if (axis) {
    var keep = {};
    keep[focal] = 1;
    keep['lane|' + axis.slice(0, 2) + '|' + axis.slice(3)] = 1;
    rels.forEach(function(r){
      if (!axisHit(r, axis)) return;
      keep[r.source_entity] = 1; keep[r.target_entity] = 1;
    });
    edges = edges.map(function(e){
      var r = e.data.rel ? REL[e.data.rel] : null;
      var on = e.data.cls ? e.data.cls === axis : (r && axisHit(r, axis));
      // 고른 상자 강조가 이미 흐려 놓은 선은 더 진해지지 않는다. 둘 다 만족해야 진하다
      return Object.assign({}, e, { style: Object.assign({}, e.style,
        { opacity: on ? (e.style.opacity === undefined ? 1 : e.style.opacity) : 0.3 }) });
    });
    var axLane = 'lane|' + axis.slice(0, 2) + '|' + axis.slice(3);
    nodes = nodes.map(function(n){
      if (n.id === axLane)
        return Object.assign({}, n, { data: Object.assign({}, n.data, { sel:true }) });
      return keep[n.id] ? n
        : Object.assign({}, n, { data: Object.assign({}, n.data, { dim:true }) });
    });
  }


  var meta = (ck && CHAINS[ck].meta) || {};
  return { nodes: place(nodes, edges, { rooted: rooted,
                                        revenueLabel: meta.revenue_axis_label || null }),
           edges: edges,
           rooted: rooted, chain: ck };
}

// ── 서랍 ────────────────────────────────────────────────────────────
// 한 줄이 어느 공급원·매출원에 드는지 적는다. 미상이면 왜 미상인지도 같이 적는다
function clsNames(r, kind){
  var m = clsOf(CHAIN_OF[r.id]);
  var ids = (kind === 'ss' ? r.supply_source_ids : r.revenue_type_ids) || [];
  var maps = (kind === 'ss' ? r.supply_source_map : r.revenue_type_map) || [];
  if (!ids.length) return '—';
  return ids.map(function(id){
    var o = (kind === 'ss' ? m.ss : m.rt)[id];
    if (!o) return id;
    var mp = maps.filter(function(x){ return x.id === id; })[0];
    // 귀속마다 등급이 다르면 그 등급을 붙인다. 배분 %는 비공개라 안 적는다
    return o.label + (o.unallocated ? ' (귀속 근거 없음)' : '')
         + (mp ? ' (' + (EV_KO[mp.status] || mp.status) + ')' : '');
  }).join(' · ');
}
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
      h('div', { key:'b' }, o.period + ' · 기준일 ' + o.as_of_date
        + (o.source_date ? ' · 출처 ' + o.source_date : '')),
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
        + (ref.up ? '타겟으로 들어온다' : '타겟에서 나간다')
        + (ref.bom ? ' · 제품 원가의 ' + ref.bom.pct + '% (추정, ' + ref.bom.period + ')'
                   : '')),
      h('table', { key:'x', className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '회사'),
          h('th', { key:2 }, '부품·역무'), h('th', { key:3 }, year + ' 비중'),
          h('th', { key:5 }, '층'), h('th', { key:4 }, '근거') ])),
        h('tbody', { key:'b' }, rels.map(function(r){
          var other = ref.up ? r.source_entity : r.target_entity;
          return h('tr', { key:r.id, style:{ cursor:'pointer' },
            onClick: function(){ p.onSel({ kind:'rel', id:r.id, entity:other }); } }, [
            h('td', { key:1 }, withFlag(other)),
            h('td', { key:2 }, r.component || '—'),
            h('td', { key:3 }, shareLabel(r.id, year) || '—'),
            h('td', { key:5 },
              TIER_KO[ref.up ? r.source_tier : r.target_tier] || '—'),
            h('td', { key:4 }, (function(){
              var maps = (ref.cls && ref.cls.slice(0, 2) === 'ss'
                          ? r.supply_source_map : r.revenue_type_map) || [];
              var mp = ref.cls ? maps.filter(function(x){
                return x.id === ref.cls.slice(3); })[0] : null;
              var lvl = mp ? mp.status : r.evidence_level;
              return h('span', { className:'badge' + (lvl === 'CONFIRMED' ? '' : ' est'),
                title: mp ? mp.note : null }, EV_KO[lvl] || lvl);
            })()) ]);
        }))
      ]),
      (function(){
        var m = clsOf(ref.chain || (ref.rels[0] && CHAIN_OF[ref.rels[0]]) || HOME);
        var o = ref.cls ? (ref.cls.slice(0, 2) === 'ss' ? m.ss : m.rt)[ref.cls.slice(3)] : null;
        return o && o.residual ? h('div', { key:'res', className:'v',
          style:{ color:'#6b7488', marginTop:'8px' } },
          '잔여 — ' + (o.residual.note || o.residual.label)) : null;
      })()
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
    h('h3', { key:'t' }, withFlag(eid)),
    h('div', { key:'r', className:'role' },
      [e.entity_type, e.country,
       (e.categories || []).map(subKo).join(' · ')].filter(Boolean).join(' · ')),
    e.parent_entity_id ? h('div', { key:'p', className:'v', style:{ color:'#6b7488' } },
      '모회사 ' + nm(e.parent_entity_id)) : null,
    e.desc ? h('div', { key:'d', className:'v' }, e.desc) : null,
    h('div', { key:'btns',
      style:{ display:'flex', gap:'6px', flexWrap:'wrap', margin:'8px 0' } }, [
      h('button', { key:'f', className:'btn',
        onClick: function(){ p.onFocus(eid); } }, '이 회사 중심으로')
    ]),
    r ? h('section', { key:'rel' }, [
      h('div', { key:'k', className:'k' }, '관계 · ' + relKo(r.relationship_type)),
      h('div', { key:'v', className:'v' }, nm(r.source_entity) + ' → ' + nm(r.target_entity)),
      h('div', { key:'rk', className:'rowk' }, [
        h('div', { key:1 }, '부품·역무'), h('div', { key:2 }, r.component || '—'),
        h('div', { key:3 }, '계통'),
        h('div', { key:4 }, subKo(r.subsystem || '—') + ' · ' + LANE_KO[r.lane]),
        h('div', { key:'c1' }, '공급원'),
        h('div', { key:'c2' }, clsNames(r, 'ss')),
        h('div', { key:'c3' }, '매출원'),
        h('div', { key:'c4' }, clsNames(r, 'rt')),
        h('div', { key:5 }, '역할'),
        h('div', { key:6 }, (r.source_role || '—') + ' → ' + (r.target_role || '—')),
        h('div', { key:'t1' }, '사슬 층'),
        h('div', { key:'t2' },
          TIER_KO[eid === r.source_entity ? r.source_tier : r.target_tier] || '—'),
        r.contractual_customer ? h('div', { key:'k1' }, '계약 고객 여부') : null,
        r.contractual_customer ? h('div', { key:'k2' }, [
          h('span', { key:'a', className:'badge'
            + (r.contractual_customer === 'CONFIRMED' ? '' : ' est') },
            CONTRACT_KO[r.contractual_customer] || r.contractual_customer),
          h('span', { key:'b', style:{ color:'#6b7488', fontSize:'11.5px' } },
            CONTRACT_NOTE[r.contractual_customer] || '') ]) : null,
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
// 사슬 이름은 chain.json 의 label 이다. 코드에 회사 이름을 박지 않는다
function chainKo(k){
  var c = CHAINS[k];
  return (c && c.meta && c.meta.label) || k;
}

// ── 회사 목록 ───────────────────────────────────────────────────────
// 기본은 사슬의 중심 회사만. 「전부 보기」를 누르면 판에 선 이름을 다 편다
function Roster(p){
  // 누른 줄을 먼저 진하게 보여 주고 잠깐 뒤에 판으로 넘어간다. 바로 넘어가면 눌린 티가
  // 안 나서 두 번 누르게 된다
  var ps = useState(null), pressed = ps[0], setPressed = ps[1];
  function pick(id){
    setPressed(id);
    setTimeout(function(){ p.onPick(id); }, 140);
  }
  var anchors = {};
  Object.keys(CHAINS).forEach(function(ck){
    var m = CHAINS[ck].meta || {};
    if (m.focal_entity) anchors[m.focal_entity] = ck;
  });
  var rows = [];
  Object.keys(ENT).forEach(function(id){
    var rs = relsOf(id);
    if (!rs.length) return;
    if (!p.all && !anchors[id]) return;
    var e = ENT[id];
    var chains = {};
    rs.forEach(function(r){ chains[CHAIN_OF[r.id]] = 1; });
    rows.push({ id:id, e:e, deg: rs.length, sec: secSector(id),
                chain: Object.keys(chains).map(chainKo).join('·') });
  });
  // SEC 가 업종을 매긴 곳부터, 같은 업종끼리 붙인다. 안 매긴 곳은 뒤에 선 수 순으로
  rows.sort(function(a, b){
    if (!a.sec !== !b.sec) return a.sec ? -1 : 1;
    if (a.sec !== b.sec) return a.sec < b.sec ? -1 : 1;
    return b.deg - a.deg;
  });
  var q = (p.q || '').toLowerCase();
  var view = q ? rows.filter(function(r){
    return (r.e.name + ' ' + (r.e.name_ko || '') + ' ' + r.id).toLowerCase().indexOf(q) >= 0;
  }) : rows;
  return h('div', { className:'pane' }, [
    h('h2', { key:'t' }, p.all ? '이 판에 선 이름 ' + rows.length + '개'
                               : '분석한 회사 ' + rows.length + '곳'),
    h('p', { key:'n', className:'note' }, [
      h('span', { key:'a' }, p.all
        ? '줄을 누르면 그 회사를 중심으로 판이 다시 선다. 섹터는 SEC 에 등록된 업종이라 '
          + '미국에 공시하지 않는 곳은 빈칸이다. '
        : '줄을 누르면 그 회사의 밸류체인이 열린다. '),
      h('button', { key:'b', className:'btn', onClick: p.onToggleAll },
        p.all ? '중심 회사만' : '판에 선 이름 전부 보기')
    ]),
    h('div', { key:'w', style:{ overflowX:'auto' } },
      h('table', { className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [
          h('th', { key:1, className:'nw' }, '나라'),
          h('th', { key:2, className:'nw' }, '이름'),
          h('th', { key:3 }, '섹터') ])),
        h('tbody', { key:'b' }, view.map(function(r){
          return h('tr', { key:r.id, className:'pick' + (pressed === r.id ? ' on' : ''),
            onClick: function(){ pick(r.id); } }, [
            h('td', { key:1, className:'nw' }, (function(){
              var f = flagOf(r.id);
              // 나라를 모르면 물음표 하나로 끝낸다. 뒤에 줄표까지 달면 두 번 말한다
              if (!f) return r.e.country || '—';
              return [h('span', { key:'f', className: flagCls(f),
                                  title: flagTitle(f) }, f),
                      r.e.country ? h('span', { key:'c' }, r.e.country) : null];
            })()),
            h('td', { key:2, className:'nw' }, nm(r.id)),
            // SEC 에 등록된 업종 그대로. 등록을 안 한 곳은 빈칸이다
            h('td', { key:3 }, r.sec || '—')
          ]);
        }))
      ]))
  ]);
}

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
  // 사슬을 보지 않는다. 이 회사 이름이 박힌 자료만 쓴다
  var boms = BOM_BY_CO[p.focal] || [];
  var fins = FIN_BY_CO[p.focal] || [];
  if (!boms.length && !fins.length)
    return h('div', { className:'pane' }, [
      h('h2', { key:'t' }, nm(p.focal) + ' — 원가 자료가 없다'),
      h('p', { key:'n', className:'note' },
        '이 회사 이름으로 된 BOM 이나 재무 앵커가 아직 없다. 다른 회사 것을 대신 보여 주지 않는다.')
    ]);
  var b = boms.length ? boms[boms.length - 1] : null;
  var sum = b ? b.components.reduce(function(a, c){ return a + c.central; }, 0) : 0;
  return h('div', { className:'pane' }, [
    b ? h('h2', { key:'t' }, nm(p.focal) + ' — 제품 원가 구성 (' + b.period + ')') : null,
    b ? h('p', { key:'n', className:'note' }, [
      h('span', { key:'a', className:'badge est' }, '전부 추정'),
      h('span', { key:'b' }, ' ' + b.note + ' 아래 비중의 분모는 ' + b.denominator
        + ' 전체(약 ' + b.total.central + ' ' + b.unit + ')이고 매출이 아니다.') ]) : null,
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
    fins.length ? h('div', { key:'fin' }, [
      h('h2', { key:'t', style:{ marginTop:'20px' } }, '재무 앵커'),
      h('p', { key:'n', className:'note' },
        '원가율은 제품 원가를 제품 매출로 나눈 값이다. 두 숫자 모두 공시다. '
        + '매출 환산 MW 는 출하 공시가 아니라 ASP 앵커로 나눈 값이라 원가를 나눌 분모로만 쓴다.'),
      h('table', { key:'x', className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [ h('th', { key:1 }, '기간'),
          h('th', { key:2 }, '총매출'), h('th', { key:3 }, '제품 매출'),
          h('th', { key:4 }, '제품 원가'), h('th', { key:'r' }, '원가율'),
          h('th', { key:5 }, '매출 환산 MW'), h('th', { key:6 }, 'MW 당 원가') ])),
        h('tbody', { key:'b' }, fins.map(function(f, k){
          return h('tr', { key:k }, [
            h('td', { key:1 }, f.period),
            h('td', { key:2 }, fmt(f.total_revenue_usd_m) + ' M'),
            h('td', { key:3 }, fmt(f.product_revenue_usd_m) + ' M'),
            h('td', { key:4 }, fmt(f.product_cogs_usd_m) + ' M'),
            h('td', { key:'r' }, (f.product_revenue_usd_m
              ? (Math.round(f.product_cogs_usd_m / f.product_revenue_usd_m * 1000) / 10) + '%'
              : '—')),
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

// ── 공급원·매출원 띠 ────────────────────────────────────────────────
// 공급원은 소재·가공과 타겟 사이, 매출원은 타겟과 직접 고객 사이의 분석축이다.
// 상자가 아니라 띠인 이유는 한 공급사가 여러 공급원에, 한 고객이 여러 매출원에
// 걸리기 때문이다. 상자로 세우면 같은 회사가 분류마다 복제된다
function Axis(p){
  var m = clsOf(p.chain);
  // 분모가 다른 %를 한 줄에 나란히 찍지 않는다. 가동률과 매출 비중을 같은 꼴로 적으면
  // 읽는 사람이 둘을 더한다. 그 줄에서 가장 많이 쓰인 분모의 값만 띠에 적고,
  // 나머지는 손 얹었을 때만 분모와 함께 보여 준다
  // 띠에 적는 값은 한 갈래뿐이다 — 매출원은 총매출 대비 비중, 공급원은 조달 비중.
  // 가동률·전방 구성처럼 다른 것을 세는 값은 숫자를 안 적고 손 얹었을 때만 보여 준다
  function pick(kind, x){ return pickShare(kind, x, p.year); }
  function tip(x){
    var t = x.note ? [x.note] : [];
    (x.shares || []).forEach(function(sh){
      if (sh.value === null || sh.value === undefined) return;
      t.push((sh.metric || '') + ' ' + sh.value + '% · ' + (sh.period || '시점 미상')
             + ' · 분모 '
             + (sh.denominator || '미상'));
    });
    return t.join('\n') || null;
  }
  function chips(kind, list, label){
    if (!list.length) return null;
    list = orderCls(kind, list, p.year);
    var den = rowDen(kind, list, p.year);
    var mine = p.axis && p.axis.slice(0, 2) === kind;
    // 「전체」는 고른 것이 없다는 뜻을 칩으로 명시한다. 이 줄의 선택이 없으면 전체가 켜진다
    var all = h('button', { key:'*all', className:'axchip' + (mine ? '' : ' on'),
      title: '이 줄의 분류를 고르지 않는다 — 모든 상자·선이 제 농도로 선다',
      onClick: function(){ if (mine) p.onPick(null); } }, '전체');
    return h('div', { key:kind, className:'axrow' }, [
      h('b', { key:'b' }, label),
      h('div', { key:'c', className:'axchips' }, [all].concat(list.map(function(x){
        var key = kind + ':' + x.id, on = p.axis === key, sh = pick(kind, x);
        var show = sh && den && sh.denominator === den;
        return h('button', { key:x.id, title: tip(x),
          className: 'axchip' + (on ? ' on' : '') + (x.unallocated ? ' un' : ''),
          onClick: function(){ p.onPick(on ? null : key); } }, [
          x.label, show ? h('i', { key:'s' },
            sh.value + '%' + (sh.stale ? ' ' + (sh.period || '') : '')) : null ]);
      })))
    ]);
  }
  var rows = [chips('ss', m.ssList, '공급원'), chips('rt', m.rtList, '매출원')]
    .filter(function(x){ return x; });
  if (!rows.length) return null;
  // 고른 분류에 걸린 줄이 하나도 없으면 화면이 통째로 흐려진다. 왜 그런지 적는다 —
  // 공시가 제품별 매출만 밝히고 고객별 귀속은 안 밝힌 자리다
  var empty = null;
  if (p.axis) {
    var key = p.axis.slice(3), kind = p.axis.slice(0, 2);
    var hit = (CHAINS[p.chain] ? CHAINS[p.chain].relationships : []).some(function(r){
      return ((kind === 'ss' ? r.supply_source_ids : r.revenue_type_ids) || [])
        .indexOf(key) >= 0;
    });
    if (!hit) {
      var o = (kind === 'ss' ? m.ss : m.rt)[key] || {};
      empty = h('div', { key:'e', className:'axnote' },
        '「' + (o.label || key) + '」에 귀속 근거가 붙은 거래가 없다. 회사 전체 비중만 '
        + '공개됐고 개별 ' + (kind === 'ss' ? '공급사' : '고객') + '의 귀속은 '
        + (kind === 'ss' ? '공급원 미상' : '배분 미상') + '으로 남았다');
    }
  }
  return h('div', { className:'axis' }, rows.concat([ empty ]));
}

// ── 앱 ──────────────────────────────────────────────────────────────
function App(){
  var u0 = readUrl(true);
  var a = useState(u0.focal), focal = a[0], setFocal = a[1];
  var b = useState(u0.year), year = b[0], setYear = b[1];
  var c = useState(u0.mode), mode = c[0], setMode = c[1];
  var d = useState(u0.open), open = d[0], setOpen = d[1];   // 펼친 상자 id. '*' 는 전부
  function toggleOpen(id){
    setOpen(function(o){
      var base = o.filter(function(x){ return x !== '*'; });
      return base.indexOf(id) >= 0 ? base.filter(function(x){ return x !== id; })
                                   : base.concat([id]);
    });
  }
  var f = useState({ kind:'ent', id: u0.sel || u0.focal }), sel = f[0], setSel = f[1];
  // 보던 사슬. 그 사슬에 있는 회사로 중심을 옮기면 사슬을 지킨다
  var f2 = useState(u0.chain), chainHint = f2[0], setChainHint = f2[1];
  var g = useState(''), q = g[0], setQ = g[1];
  var j = useState([u0.focal]), path = j[0], setPath = j[1];
  var k2 = useState(true), leg = k2[0], setLeg = k2[1];
  // 좁은 화면에서는 서랍을 닫고 시작한다. 열면 그래프를 덮기 때문이다
  var l2 = useState(window.innerWidth >= 980), drw = l2[0], setDrw = l2[1];
  var m2 = useState(null), rf = m2[0], setRf = m2[1];
  var n2 = useState(false), allNames = n2[0], setAllNames = n2[1];
  var o2 = useState(null), axis = o2[0], setAxis = o2[1];
  // 좁은 화면인가. 돌리거나 창을 줄이면 따라간다
  var q2 = useState(window.innerWidth < 720), narrow = q2[0], setNarrow = q2[1];
  var r2 = useState(false), sopen = r2[0], setSopen = r2[1];
  var u2 = useState(false), menu = u2[0], setMenu = u2[1];
  // 회사 목록에서 고른 뒤 판이 설 때까지. 자리 잡기가 끝나면 fit 효과가 내린다
  // 처음 열 때도 「세우는 중」이다. 자리 잡기 전의 판(머리글만 선 빈 판)을 보이지 않는다
  var s2 = useState(u0.focal), busy = s2[0], setBusy = s2[1];
  // 판의 이동·확대 — 머리글 띠가 가로로 따라가게 한다
  var v2 = useState({ x:0, y:0, zoom:1 }), vp = v2[0], setVp = v2[1];
  // 시야를 옮길 상자. 판이 다시 선 뒤 그 상자를 가운데에 둔다
  var w2 = useState(null), panTo = w2[0], setPanTo = w2[1];
  // 판 상자(.react-flow)는 스크롤 상자가 아니다. 포커스·찾기·자동 스크롤로 안이 밀리면
  // 머리글 띠·미니맵과 상자가 어긋난다. 밀릴 때마다 0 으로 되돌린다
  useEffect(function(){
    var el = document.querySelector('.react-flow');
    if (!el) return;
    function fix(){ if (el.scrollTop || el.scrollLeft) { el.scrollTop = 0; el.scrollLeft = 0; } }
    el.addEventListener('scroll', fix);
    return function(){ el.removeEventListener('scroll', fix); };
  }, [rf, mode]);
  useEffect(function(){
    if (!panTo || !rf || !rf.setCenter) return;
    var t = setTimeout(function(){
      var n = null;
      gr.nodes.forEach(function(x){ if (x.id === panTo) n = x; });
      if (n) {
        // 가운데가 아니라 위에서 1/4 자리에 둔다. 펴진 이웃은 대개 아래로 자라난다
        var z = rf.getZoom ? rf.getZoom() : 1;
        var cv = document.querySelector('.canvas');
        var lift = cv ? (cv.clientHeight / z) * 0.25 : 0;
        rf.setCenter(n.position.x + COL_W / 2, n.position.y + BOX_H / 2 + lift,
                     { zoom: z, duration: 420 });
      }
      setPanTo(null);
    }, 80);
    return function(){ clearTimeout(t); };
  }, [panTo, gr, rf]);
  useEffect(function(){
    if (!busy) return;
    var t = setTimeout(function(){ setBusy(null); }, 3000);
    return function(){ clearTimeout(t); };
  }, [busy]);
  useEffect(function(){
    function onR(){ setNarrow(window.innerWidth < 720); }
    window.addEventListener('resize', onR);
    return function(){ window.removeEventListener('resize', onR); };
  }, []);
  useEffect(function(){
    if (!rf) return;
    var t = setTimeout(function(){
      if (rf.getNodes && rf.setViewport) {
        // 첫 화면 — 판 전체를 한 화면에 욱여넣지 않는다(블룸은 상자 100개라 글자가 안
        // 읽힌다). 칸 머리글을 맨 위에 붙이고 타겟 칸을 가운데 두어 좁은 화면은 양옆
        // 한 칸씩, 넓은 화면은 두 칸씩을 읽히는 크기로 보인다. 나머지는 끌어서 본다
        var me0 = null;
        rf.getNodes().forEach(function(n){ if (n.id === focal) me0 = n; });
        var cv = document.querySelector('.canvas');
        if (me0 && cv) {
          var vw = cv.clientWidth || window.innerWidth;
          var ncol = window.innerWidth < 720 ? 3 : 5;
          var z = Math.min(1, Math.max(.55, (vw - 16) / (ncol * COL_W + (ncol - 1) * COL_GAP)));
          rf.setViewport({ x: vw / 2 - (me0.position.x + COL_W / 2) * z, y: 6, zoom: z },
                         { duration:240 });
          return;
        }
      }
      if (window.innerWidth < 720 && rf.getNodes) {
        // 중심과 바로 옆 칸까지를 한 화면에 담는다. 나머지는 끌어서 본다
        var all = rf.getNodes(), me = null;
        all.forEach(function(n){ if (n.id === focal) me = n; });
        if (me) {
          var myCol = me.data.col, box = null;
          all.forEach(function(n){
            if (n.type === 'hdr' || n.data.col === undefined) return;
            if (Math.abs(n.data.col - myCol) > 1) return;
            var w = n.width || 128, hh = n.height || 44;
            var b = { x:n.position.x, y:n.position.y, x2:n.position.x + w,
                      y2:n.position.y + hh };
            if (!box) box = b;
            else {
              box.x = Math.min(box.x, b.x); box.y = Math.min(box.y, b.y);
              box.x2 = Math.max(box.x2, b.x2); box.y2 = Math.max(box.y2, b.y2);
            }
          });
          if (box) {
            rf.fitBounds({ x:box.x, y:box.y, width:box.x2 - box.x, height:box.y2 - box.y },
                         { padding:0.08, duration:240 });
            return;
          }
        }
      }
      rf.fitView({ padding:0.12, duration:220 });
    }, 90);
    var t2 = setTimeout(function(){ setBusy(null); }, 380);
    return function(){ clearTimeout(t); clearTimeout(t2); };
  // 중심을 바꾸거나 화면을 갈아탈 때만 자리를 다시 잡는다.
  // 상자를 누를 때마다 원점으로 돌아가면 보던 자리를 잃는다
  }, [rf, focal, mode]);

  useEffect(function(){
    var sid = sel ? (sel.entity || sel.id) : '';
    writeUrl({ focal:focal, year:year, mode:mode, open:open, chain: chainHint,
               sel: (sid || '').slice(0, 5) === 'lane|' ? '' : sid }, false);
  }, [focal, year, mode, open, sel, chainHint]);
  useEffect(function(){
    function pop(){
      var s = readUrl();
      setFocal(s.focal); setYear(s.year); setMode(s.mode); setOpen(s.open);
      setChainHint(s.chain);
      setSel({ kind:'ent', id: s.sel || s.focal });
    }
    window.addEventListener('popstate', pop);
    return function(){ window.removeEventListener('popstate', pop); };
  }, []);

  var gr = useMemo(function(){
    return buildGraph(focal, year, sel, axis, chainHint, open);
  }, [focal, year, sel, axis, chainHint, open]);

  // 칸 머리(원재료·소재·가공…) 위로는 못 올라가게 막는다. 아래·좌우는 넉넉히 둔다
  var extent = useMemo(function(){
    var x0 = 1e9, x1 = -1e9, y1 = -1e9;
    gr.nodes.forEach(function(n){
      var w = n.type === 'hdr' ? COL_W : COL_W;
      if (n.position.x < x0) x0 = n.position.x;
      if (n.position.x + w > x1) x1 = n.position.x + w;
      if (n.position.y > y1) y1 = n.position.y;
    });
    if (x0 > x1) return undefined;
    return [[x0 - 420, -12], [x1 + 420, y1 + 600]];
  }, [gr]);

  function goFocal(id){
    var ck = chainOf(id, chainHint || chainOf(focal));
    setChainHint(ck);
    setFocal(id); setOpen([]); setSel({ kind:'ent', id:id }); setAxis(null);
    setPath(function(p){
      return p.indexOf(id) >= 0 ? p.slice(0, p.indexOf(id) + 1) : p.concat([id]);
    });
    writeUrl({ focal:id, year:year, mode:mode, open:[], sel:id, chain: ck }, true);
  }
  // 띠의 칩을 고르면 판이 그 갈림목으로 옮겨 가고 그 갈림목이 펴진다. 고르기만 하고
  // 시야가 그대로면 무엇이 바뀌었는지 안 보인다
  function pickAxis(key){
    setAxis(key);
    if (!key) return;
    var lid = 'lane|' + key.slice(0, 2) + '|' + key.slice(3);
    setOpen(function(o){ return o.indexOf(lid) >= 0 || o.indexOf('*') >= 0 ? o : o.concat([lid]); });
    setPanTo(lid);
  }
  function onNodeClick(_, node){
    var rfEl = document.querySelector('.react-flow');
    if (rfEl) { rfEl.scrollTop = 0; rfEl.scrollLeft = 0; }
    // 누른 상자를 가운데에 둔다. 펴진 이웃이 어느 쪽에 나타났는지 보이게
    setPanTo(node.id);
    // 누르면 그 상자와 바로 닿는 것만 진해진다. 새 상자를 만들지 않는다.
    // 공급원·매출원 알약은 상자가 아니라 분류라 띠의 칩과 같은 일을 한다 — 그 분류에
    // 걸린 줄만 남기고 칩이 켜진다. 다시 누르면 푼다
    if (node.data.kind === 'lane') {
      var key = node.data.ref && node.data.ref.cls;
      var off = axis === key;
      setAxis(off ? null : key);
      setSel(off ? { kind:'ent', id: focal } : node.data.ref);
      if (node.data.more || node.data.opened) toggleOpen(node.id);
      setDrw(!narrow);
      return;
    }
    if (node.data.more || node.data.opened) toggleOpen(node.id);
    setSel(node.data.ref); setDrw(!narrow);
  }
  function drill(subsystem){
    // 그 계통에 속한 상자 하나를 골라 판에서 진하게 보여 준다
    var rels = relsOf(focal).filter(function(r){
      return r.subsystem === subsystem && r.target_entity === focal;
    });
    if (!rels.length) return;
    setMode('current');
    setSel({ kind:'rel', id: rels[0].id, entity: rels[0].source_entity, up:true });
  }

  var hits = q ? Object.keys(ENT).filter(function(id){
      var x = ENT[id];
      var s = (x.name + ' ' + (x.name_ko || '') + ' ' + id).toLowerCase();
      return REL_BY_ENT[id] && s.indexOf(q.toLowerCase()) >= 0;
    }).slice(0, 14) : [];

  var searchBox = h('div', { key:'s', className:'search' }, [
    h('input', { key:'i', value:q, placeholder:'회사 이름으로 찾기', autoFocus: narrow,
      onChange: function(ev){ setQ(ev.target.value); } }),
    hits.length ? h('div', { key:'g', className:'sug' }, hits.map(function(id){
      return h('div', { key:id, onClick: function(){
        setQ(''); setSopen(false); goFocal(id); } }, [
        h('span', { key:'a' }, withFlag(id)),
        h('span', { key:'b', className:'k' },
          (ENT[id].categories || []).map(subKo).join(' · ')) ]);
    })) : null
  ]);
  // 탭은 회사·현재 둘뿐이다. 시점·원가·근거 화면은 코드에 남아 주소(mode=)로는 열리지만
  // 탭에서 뺐다(2026-09-11) — 첫 화면에서 고를 것이 셋이나 더 있으면 판이 뒤로 밀린다
  // 왼쪽은 「회사」(누르면 아래로 목록이 펼쳐진다), 오른쪽은 지금 보는 회사 이름(판 탭)
  var modes = h('div', { key:'m', className:'modes' }, [
    h('button', { key:'co', className: menu ? 'on' : '',
      onClick: function(){ setMenu(!menu); setSopen(false); } },
      [ '회사', h('span', { key:'c', className:'car' }, menu ? '▲' : '▼') ]),
    h('button', { key:'cur', className: (mode === 'current' && !menu) ? 'on' : '',
      onClick: function(){ setMode('current'); setMenu(false); } }, nm(focal))
  ]);
  // 사슬의 타겟 회사들. 많아지면 목록 안에서 민다
  var anchors = [];
  Object.keys(CHAINS).forEach(function(ck){
    var m = CHAINS[ck].meta || {};
    if (m.focal_entity && ENT[m.focal_entity]) anchors.push({ id: m.focal_entity, chain: ck });
  });
  anchors.sort(function(a, b){ return nm(a.id) < nm(b.id) ? -1 : 1; });
  var menuBox = menu ? h('div', { key:'menu', className:'menu' }, [
    h('div', { key:'h', className:'hd' }, '분석한 회사 ' + anchors.length + '곳') ].concat(
    anchors.map(function(a){
      return h('div', { key:a.id, className:'row' + (a.id === focal ? ' cur' : ''),
        onClick: function(){ setMenu(false); setBusy(a.id); setMode('current'); goFocal(a.id); } },
        // 오른쪽에는 SEC 에 등록된 업종. 미국에 공시하지 않는 곳은 빈칸이다
        [ h('span', { key:'n' }, withFlag(a.id, 'm')),
          h('span', { key:'k', className:'k' }, secSector(a.id) || '—') ]);
    }))) : null;
  var ICON_SEARCH = h('svg', { viewBox:'0 0 24 24' }, [
    h('circle', { key:'c', cx:11, cy:11, r:7 }), h('path', { key:'l', d:'M20 20l-3.5-3.5' }) ]);
  var ICON_DRAWER = h('svg', { viewBox:'0 0 24 24' }, [
    h('rect', { key:'r', x:3, y:4, width:18, height:16, rx:2 }),
    h('path', { key:'l', d:'M15 4v16M17.5 9h1M17.5 12h1' }) ]);
  var canDrw = mode === 'current' || mode === 'timeline';
  var allOpen = open.indexOf('*') >= 0;
  var ICON_ALL = h('svg', { viewBox:'0 0 24 24' }, [
    h('path', { key:'a', d:'M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5' }) ]);
  // 좁은 화면 머리줄은 한 줄이다 — 검색은 아이콘으로 접고 서랍도 아이콘, 탭은 분절 컨트롤
  var top = narrow
    ? h('div', { key:'top', className:'top' }, [
        h('div', { key:'b', className:'brand' }, '밸류체인'),
        modes,
        h('button', { key:'sb', className:'iconbtn' + (sopen ? ' on' : ''), title:'회사 찾기',
          'aria-label':'회사 찾기',
          onClick: function(){ setSopen(!sopen); if (sopen) setQ(''); } }, ICON_SEARCH),
        sopen ? h('div', { key:'sp', className:'searchpop' }, searchBox) : null,
        menuBox
      ])
    : h('div', { key:'top', className:'top' }, [
        h('div', { key:'b', className:'brand' }, [ '밸류체인 탐색기',
          h('small', { key:'s' }, '회사를 고르고 눌러 넓히고 시점을 옮긴다') ]),
        searchBox,
        modes,
        h('div', { key:'sp', className:'spacer' }),
        mode === 'current' ? h('button', { key:'all', className:'btn' + (allOpen ? ' on' : ''),
          title:'판 전체를 펴거나 접는다',
          onClick: function(){ setOpen(allOpen ? [] : ['*']); } }, allOpen ? '접기' : '전부 펴기') : null,
        canDrw ? h('button', { key:'dw', className:'btn' + (drw ? ' on' : ''),
          onClick: function(){ setDrw(!drw); } }, '근거 서랍') : null,
        menuBox
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
  // 좁은 화면 연도는 ‹ 2026 현재 › 한 줄이다. 굴림·끌기 대신 누른다
  var yi = YEARS.indexOf(year);
  var yearbar = h('div', { key:'s', className:'yearbar' }, [
    h('button', { key:'l', disabled: yi <= 0, 'aria-label':'이전 해',
      onClick: function(){ stepYear(-1); } }, '‹'),
    h('span', { key:'v', className:'yv' }, year === NOW ? year + ' 현재' : year),
    h('button', { key:'r', disabled: yi >= YEARS.length - 1, 'aria-label':'다음 해',
      onClick: function(){ stepYear(1); } }, '›')
  ]);
  var scrub = narrow ? yearbar : h('div', { key:'s', className:'scrub', tabIndex:0,
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
  if (mode === 'roster') body = h(Roster, { q:q, all:allNames,
    onToggleAll: function(){ setAllNames(!allNames); },
    onPick: function(id){ setQ(''); setBusy(id); setMode('current'); goFocal(id); } });
  else if (mode === 'timeline')
    body = h(Swim, { focal:focal,
      onSel: function(ref){ setSel(ref); setDrw(true); } });
  else if (mode === 'evidence') body = h(Evidence, null);
  else if (mode === 'bom') body = h(Bom, { focal:focal, onDrill:drill });
  else body = h('div', { key:'cv', className:'canvas' + (busy ? ' loading' : '') }, [
    busy ? null : h(HdrBar, { key:'hb', nodes: gr.nodes, vp: vp }),
    // 좁은 화면 — 조작은 엄지 자리(아래)에. 오른쪽은 전부 펴기·서랍, 왼쪽은 뒤로 한 단
    narrow ? h('div', { key:'fab', className:'fab' }, [
      h('button', { key:'all', className:'iconbtn' + (allOpen ? ' on' : ''),
        title: allOpen ? '접기' : '전부 펴기', 'aria-label':'전부 펴기',
        onClick: function(){ setOpen(allOpen ? [] : ['*']); } }, ICON_ALL),
      h('button', { key:'dw', className:'iconbtn' + (drw ? ' on' : ''),
        title:'근거 서랍', 'aria-label':'근거 서랍',
        onClick: function(){ setDrw(!drw); setSopen(false); } }, ICON_DRAWER) ]) : null,
    (narrow && path.length > 1) ? h('button', { key:'back', className:'backbtn',
      onClick: function(){ goFocal(path[path.length - 2]); } },
      [ h('span', { key:'a' }, '←'), h('span', { key:'b' }, nm(path[path.length - 2])) ]) : null,
    busy ? h('div', { key:'busy', className:'busy' }, [ h('i', { key:'i' }),
      h('span', { key:'t' }, nm(busy) + ' 판을 세우는 중') ]) : null,
    h(RF, { key:'rf', nodes:gr.nodes, edges:gr.edges, nodeTypes:NODE_TYPES,
      edgeTypes:EDGE_TYPES,
      onNodeClick:onNodeClick, onInit:function(inst){ setRf(inst);
        if (inst.getViewport) setVp(inst.getViewport()); },
      onMove:function(_, v){ setVp(v); }, fitView:true, maxZoom:1.6,
      // 상자에 포커스가 가면 브라우저가 판 자체를 스크롤해 상자를 보이게 한다 — 판이
      // 통째로 밀리고 미니맵이 엉뚱한 자리에 선다. 포커스는 안 준다
      nodesFocusable:false, edgesFocusable:false,
      // 좁은 화면에서는 글자가 안 보일 만큼 줄이지 않는다. 대신 끌어서 본다
      minZoom: window.innerWidth < 720 ? .28 : .25,
      translateExtent: extent,
      onPaneClick: function(){ if (window.innerWidth < 720) setDrw(false); },
      nodesDraggable:false, proOptions:{ hideAttribution:true } }, [
      h(Background, { key:'bg', gap:22, size:1, color:'#c9cfdb' }),
      h(Controls, { key:'ct', showInteractive:false }),
      // 전부 편 판에서만 — 어디를 보고 있는지. 좁은 화면은 자리가 없다
      (!narrow && allOpen && MiniMap) ? h(MiniMap, { key:'mm', pannable:true, zoomable:true,
        nodeStrokeWidth:0, maskColor:'rgba(232,235,240,.6)',
        nodeColor:function(n){ return n.type === 'hdr' ? 'transparent'
          : (n.data && n.data.focal ? '#151b28' : (n.data && n.data.kind === 'lane' ? '#c6ccd8' : '#9aa3b5')); },
        style:{ width:180, height:120 } }) : null
    ])
  ]);

  var legend = h('div', { key:'lg', className:'legend' }, [
    h('b', { key:'b' }, '선'),
    h('i', { key:1 }, '굵은 실선 공시로 확인'),
    h('i', { key:2 }, '갈색 실선 추정 (분모 있음)'),
    h('i', { key:3 }, '파선 정황 추론'),
    h('i', { key:4 }, '점선 비공개·과거 관측'),
    h('i', { key:5 }, '? 그 해 값 없음'),
    h('i', { key:'q' }, '이름 앞 ? 원문이 나라를 안 밝힘'),
    h('i', { key:'p' }, '상자를 누르면 그 줄기만 진해짐'),
    h('b', { key:'c' }, '가로'),
    h('i', { key:6 }, '왼쪽 원재료 → 소재·가공 → 부품 → 계통 → 공급원 → 타겟'),
    h('i', { key:7 }, '오른쪽 타겟 → 매출원 → 직접 고객 → 중개 → 간접 고객, 프로젝트는 테두리'),
    h('i', { key:'ln' }, '공급원·매출원 알약은 회사가 아니라 갈림목. 한 회사가 두 분류에 들면 선이 둘'),
    h('b', { key:'x' }, '띠'),
    h('i', { key:8 }, '공급원 타겟에 들어가는 품목'),
    h('i', { key:9 }, '매출원 타겟에서 나가는 매출 갈래'),
    h('i', { key:10 }, '고르면 그 분류에 걸린 줄만 진해짐. 상자는 안 사라짐'),
    h('i', { key:11 }, '미상 귀속 근거가 없어 못 나눈 자리')
  ]);

  return h('div', { className:'app' }, [ top,
    mode === 'roster' ? null : crumb,
    (mode === 'current' || mode === 'timeline') ? scrub : null,
    // 공급원·매출원 띠는 사슬의 타겟 기준 분류라 다른 회사를 중심에 놓으면 접는다
    (mode === 'current' && !gr.rooted)
      ? h(Axis, { key:'ax', chain: gr.chain, axis: axis, year: year,
          onPick: pickAxis }) : null,
    (mode === 'current' && gr.rooted)
      ? h('div', { key:'rt', className:'axnote', style:{ padding:'6px 14px',
          background:'var(--paper)', borderBottom:'1px solid var(--line)' } },
          nm(focal) + ' 을(를) 중심으로 다시 세운 판이다. 왼쪽 칸은 사슬 층이 아니라 이 '
          + '회사에서 몇 단 앞인가이고, 공급원·매출원 띠는 사슬의 타겟('
          + (gr.chain ? nm((CHAINS[gr.chain].meta || {}).focal_entity) : '—')
          + ') 기준이라 접었다') : null,
    h('div', { key:'m', className:'main' }, [
      body,
      ((mode === 'current' || mode === 'timeline') && drw)
        ? h(Drawer, { key:'d', sel:sel, year:year, onSel:setSel,
        onClose: function(){ setDrw(false); },
        onFocus: goFocal,
        onTimeline: function(id){ goFocal(id); setMode('timeline'); } }) : null
    ]),
    mode === 'current' ? legend : null
  ]);
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
})();
