// 20_layout.js
// 상자·선 그리기와 자리 잡기(place·route) — 칸·통로·꺾임 규약
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
          + (d.kind === 'cluster' ? ' cluster' : '')
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
var PROJ_PAD_X = 18, PROJ_PAD_Y = 58;

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
    // 곧은 선(straight)은 안 쓴다 — 상자 가운데 높이가 같아도 포트 자리가 몇 px 달라 선이
    // 기운다. 통로에서 작은 턱 하나로 옮기면 가로로 곧게 읽힌다
    var dir = b.col > a.col ? 1 : -1, mids = [];
    for (var c = a.col + dir; c !== b.col; c += dir) mids.push(c);
    var hit = blockersAt(mids, y1);
    var clearY = y1;
    // 첫 통로의 길(닿을 높이)이 막혔으면 마지막 통로(출발 높이로 곧게 가서 닿을 상자
    // 앞에서 한 번 꺾기)를 본다. 세로 구간은 그대로 하나, 꺾임도 둘이다
    if (hit.length && mids.length && !blockersAt(mids, y0).length) {
      e.type = 'gut';
      e.data = Object.assign({}, e.data,
        { gx: gutterX(bs[bs.length - 1], lane[e.id + '@' + bs[bs.length - 1]] || 0), gy: null,
          late: true });
      return;
    }
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
      var list = byCol[c];
      if (i === fcol) {
        // 타겟 칸 — 타겟은 맨 위에 못박고 빈 자리들만 닿을 높이 순으로. 안 맞추면 빈 자리
        // 둘이 서로 밀어내며 판이 끝없이 자란다
        var head = list.filter(function(it){ return !it.dummy; });
        var ds = list.filter(function(it){ return it.dummy; });
        ds.sort(function(a, b){ return ((a.want || 0) - (b.want || 0)) || (a.ord - b.ord); });
        byCol[c] = head.concat(ds);
        byCol[c].forEach(function(it, k){ it.ord = k; });
        return;
      }
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
  var prevSig = null, deep0 = null;
  for (var pass = 0; pass < 40; pass++){
    var moved = false;
    // 안 맞은 빈 자리의 어긋남이 지난 번과 똑같으면 되풀이해도 안 바뀐다 — 서로 밀어내는
    // 고리다. 거기서 멈춘다. 남은 어긋남은 route 가 한 번에 더 멀리 옮겨 비킨다
    var sig = Object.keys(span).map(function(eid){
      var t = spot[eById[eid].target];
      if (!t || t.top === undefined) return '';
      return span[eid].map(function(did){
        return spot[did] ? Math.round(cyOf(spot[did]) - cyOf(t)) : 0; }).join('/');
    }).join(' ');
    if (sig === prevSig) break;
    prevSig = sig;
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
    if (window.__VCDBG) console.info('vc place pass ' + pass + ' deep ' + Math.round(deep) + ' '
      + Object.keys(span).map(function(eid){
          var t = spot[eById[eid].target];
          return eid + ':' + span[eid].map(function(did){
            return spot[did] ? Math.round(cyOf(spot[did]) - cyOf(t)) : '?'; }).join('/');
        }).filter(function(x){ return !/:(0\/?)+$/.test(x); }).join(' '));
    // 맞아 드는 판은 첫 번 높이에서 몇 % 안에서 멈춘다. 첫 번의 1.6배를 넘으면 서로
    // 밀어내는 고리다 — 거기서 끊는다. 남은 어긋남은 route 가 한 번에 더 멀리 옮겨 비킨다
    if (deep0 === null) deep0 = deep;
    if (deep > span0 * 3 || deep > deep0 * 1.6) {
      // 경고가 아니라 알림이다 — 끊어도 선 규약(check_vcroute)이 그 뒤를 잰다. 남은 어긋남은
      // route 가 마지막 통로나 더 먼 높이로 비킨다
      if (window.console) console.info('vc place: 빈 자리 맞추기가 ' + pass + ' 번에 안 멈춰 끊는다');
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

  // 프로젝트 이름표는 맨 위 식구 상자 위 PROJ_PAD_Y 에 붙는다. 그 식구가 첫 줄이면 이름표가
  // 칸 머리글(고정 띠) 밑으로 들어간다 — 그만큼 판 전체를 내린다
  var topOf = {};
  Object.keys(byCol).forEach(function(c){
    byCol[c].forEach(function(it){ topOf[it.id] = it.top; });
  });
  var extra = 0;
  projs.forEach(function(pn){
    var t = null;
    (pn.data.mem || []).forEach(function(id){
      if (topOf[id] !== undefined && (t === null || topOf[id] < t)) t = topOf[id];
    });
    if (t === null) return;
    var labelTop = t - lo + HDR_H + HDR_GAP - PROJ_PAD_Y;
    if (labelTop < HDR_H + 8) extra = Math.max(extra, HDR_H + 8 - labelTop);
  });

  var out = [], geo = {};
  used.forEach(function(c, i){
    var x = i * (COL_W + COL_GAP);
    byCol[c].forEach(function(it){
      var y = it.top - mid + (hi - lo) / 2 + HDR_H + HDR_GAP + extra;
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

