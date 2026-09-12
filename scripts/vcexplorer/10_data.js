// 10_data.js
// 색인·사전·비중 고르기 — 데이터를 읽어 찾기 쉽게 만든다
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
// 쪽 색 — 공급 쪽 회색, 고객 쪽 남색. 상자 테두리와 확인된 선이 같은 색을 쓴다
var SIDE_INK = { sup:'#8A96A3', cust:'#31507A' };
// 병목 — 공급 여력이 이 등급이면 진홍 상자
var BOTT = { HIGH:1, VERY_HIGH:1 };
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
  DEPLOYS_AT:'설치 부지', CONTRACT_PARTY_UNDISCLOSED:'계약 상대 미상', SUBSIDIARY_OF:'자회사', CONTRACT_MANUFACTURES:'수탁 제조',
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

