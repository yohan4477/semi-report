// 30_graph.js
// 주소 상태와 그래프 세우기(topology·buildGraph) — 칸 매기기·펼침·강조
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
  EMS_ASSEMBLY:'후공정 외주',
  PROJECT_FINANCE:'프로젝트 금융', CREDIT_SUPPORT:'신용 보강', INVESTS_IN:'투자',
  OPERATES_THROUGH:'운영 자회사', EXECUTES_THROUGH:'실행 법인',
  END_CUSTOMER_SUPPLY_CHAIN:'공급망 목록', DISTRIBUTION_PARTNERSHIP:'유통 제휴',
  INDIRECT_CUSTOMER_UNDISCLOSED:'고객 · 비공개', CONTRACT_PARTY_UNDISCLOSED:'계약 상대 · 비공개' };
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
    // 무리(분류 체계, group_rank)가 먼저 갈린다 — 엔비디아처럼 옛 분류와 새 분류가 한 줄에
    // 서면 비중 합이 100 을 넘는 것처럼 읽힌다. 무리 안에서는 비중 순, 미상은 맨 뒤
    function key(x){
      var g = x.unallocated ? 99 : (x.group_rank || 0);
      if (x.unallocated) return [g, 3, 0];
      var sh = pickShare(kind, x, year);
      if (!sh) return [g, 2, 0];
      return [g, den && sh.denominator === den ? 0 : 1, -(sh.value || 0)];
    }
    var ka = key(a), kb = key(b);
    return (ka[0] - kb[0]) || (ka[1] - kb[1]) || (ka[2] - kb[2]) || (a.label < b.label ? -1 : 1);
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
    // 부지·SPV 는 고객이 아니라 물건이 놓이는 자리다 — 「간접 고객」이라 안 적는다
    sub[id] = (r.relationship_type === 'INDIRECT_CUSTOMER_UNDISCLOSED' || e.anon)
      ? '간접 고객 · 비공개'
      : e.entity_type === 'project_spv'
        ? (r.relationship_type === 'DEPLOYS_AT_SITE' || r.relationship_type === 'DEPLOYS_AT'
           ? '설치 부지' : '프로젝트')
        : '간접 고객';
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
    // 색은 소속이다(TSMC 그림 규약) — 타겟 청록, 한국 회사 주황, 고객 남색, 나머지 공급사 회색.
    // 병목은 진홍: 공급 여력 HIGH 이상이라 적힌 줄의 출발 상자. 중개·유통은 점선 테두리
    var kr = (ENT[id] || {}).country === '한국';
    var side = isFocal ? 'focal' : (tp.col[id] >= COL_OF.CONTRACTUAL_CUSTOMER ? 'cust' : 'sup');
    nodes.push({ id: id, type:'nd', data:{
      title: nm(id), flag: flagOf(id), ico: iconOf(id),
      kind: KIND_OF[(ENT[id] || {}).entity_type] || 'ent',
      focal: isFocal, col: tp.col[id], kr: kr, side: side,
      mid: !isFocal && (tp.sub[id] === '중개' || tp.col[id] === COL_OF.INTERMEDIARY
                        || (iconOf(id) === 'distributor')),
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
          // 밑줄은 옆 숫자의 분모다. 잔여(배분 미상)는 서랍에 적는다 — 알약에 「잔여」를
          // 달면 옆의 비중이 잔여 비중처럼 읽힌다
          sub: x.group_label || ((sh && den && sh.denominator === den) ? den : null),
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
  // 확인된 선은 쪽으로 색을 나눈다 — 공급 쪽 회색, 고객 쪽 남색(TSMC 그림 규약).
  // 추정·추론·비공개는 근거 등급 색·파선을 그대로 둔다
  function sideTint(st, r, lvl){
    if (lvl !== 'CONFIRMED') return st;
    return Object.assign({}, st, { stroke: r.lane === 'DOWNSTREAM' ? SIDE_INK.cust : SIDE_INK.sup });
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
    // 병목 — 공급 여력이 HIGH 이상이라 적힌 줄의 출발 상자를 진홍으로
    if (BOTT[r.capacity_criticality]) {
      var bn = nodes.filter(function(n){ return n.id === r.source_entity; })[0];
      if (bn && !bn.data.focal) bn.data.bott = true;
    }
    var band = bandOf(r);
    if (!band) {
      st = sideTint(st, r, r.evidence_level);
      edges.push({ id:'e-' + r.id, source: r.source_entity, target: r.target_entity,
        style: st, data:{ rel: r.id, on: on },
        markerEnd: marker(st.stroke), type:'smoothstep' });
    } else {
      var ids = band === 'ss' ? r.supply_source_ids : r.revenue_type_ids;
      ids.forEach(function(cid){
        var lid = laneId(band, cid);
        if (!laneOf[lid]) return;
        laneOf[lid].rels.push(r.id);
        var key = band + ':' + cid;
        // 귀속마다 근거 등급이 다르다 — Apple 은 커패시터에는 확인, 인덕터에는 추론
        var mp = mapOf(r, band, cid), lvl = mp ? mp.status : r.evidence_level;
        var st2 = sideTint(Object.assign({}, evStyle(lvl)), r, lvl);
        if (!on) st2.opacity = 0.28;
        edges.push({ id:'e-' + r.id + '|' + cid,
          source: band === 'ss' ? r.source_entity : lid,
          target: band === 'ss' ? lid : r.target_entity,
          style: st2, data:{ rel: r.id, on: on, cls: key, map: mp || null },
          markerEnd: marker(st2.stroke), type:'smoothstep' });
        // 갈림목과 타겟 사이 줄기는 갈림목마다 하나다. 그 갈림목을 지나는 선이 하나라도
        // 그 해에 살아 있으면 진하다
        var tk = trunk[lid];
        if (!tk) {
          var tst = Object.assign({}, EV_STYLE.CONFIRMED,
            { stroke: band === 'ss' ? SIDE_INK.sup : SIDE_INK.cust });
          tk = trunk[lid] = { id:'e-trunk|' + lid,
            source: band === 'ss' ? lid : focal, target: band === 'ss' ? focal : lid,
            style: tst,
            data:{ rel: null, cls: key, on: false, rels: [] },
            markerEnd: marker(tst.stroke), type:'smoothstep' };
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

  // 군집 접기 — 다운스트림 한 칸에 같은 노릇(설치·배치, 직접 고객…)의 회사가 여섯을 넘으면
  // 「설치·배치 11곳」 한 상자로 접는다. 누르면 편다(open 에 grp|칸|노릇). 전부 펴기(*)면 안 접는다.
  // 블룸의 직접 고객 열여덟처럼 긴 칸에서만 일어난다
  var CLUSTER_MIN = 6;
  if (!all) {
    var groups = {};
    nodes.forEach(function(n){
      var d = n.data;
      if (n.type !== 'nd' || d.kind !== 'ent' || d.focal || d.col === undefined) return;
      if (d.col < COL_OF.CONTRACTUAL_CUSTOMER || d.col >= COL_OF.END_MARKET) return;
      var key = 'grp|' + d.col + '|' + (d.sub || '');
      (groups[key] = groups[key] || []).push(n.id);
    });
    var into = {};
    Object.keys(groups).forEach(function(key){
      var mem = groups[key];
      if (mem.length < CLUSTER_MIN || open.indexOf(key) >= 0) return;
      mem.forEach(function(id){ into[id] = key; });
      var col = parseInt(key.split('|')[1], 10), sub = key.split('|')[2];
      nodes.push({ id: key, type:'nd', data:{
        title: (sub || '상자') + ' ' + mem.length + '곳', kind:'cluster', col: col,
        sub: '누르면 펼친다', mem: mem, more: null,
        ref:{ kind:'ent', id: focal, entity: focal } } });
    });
    if (Object.keys(into).length) {
      nodes = nodes.filter(function(n){ return !into[n.id]; });
      var seenE = {};
      edges = edges.map(function(e){
        var s2 = into[e.source] || e.source, t2 = into[e.target] || e.target;
        if (s2 === e.source && t2 === e.target) return e;
        return Object.assign({}, e, { source: s2, target: t2, id: e.id + '|c' });
      }).filter(function(e){
        if (e.source === e.target) return false;
        var k = e.source + '>' + e.target + '>' + ((e.data && e.data.cls) || '');
        if (seenE[k]) return false;
        seenE[k] = 1; return true;
      });
    }
  }

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

