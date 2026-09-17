/* 지분 대시보드 — 두 가지로 본다.
   회사 중심  고른 회사 위로 일가까지 올라가는 사슬 한 줄, 아래로 그 회사가 최대 동일인측 주주인 계열사.
              세로로만 읽혀 좁은 화면에서도 옆으로 밀 일이 없다(Orbis 의 주주·피출자 나눔 꼴).
   전체 나무  부모 선으로 왼쪽에서 오른쪽으로. 그 밖의 동일인측 선은 상자를 고르면 점선으로 겹친다.
   두 보기 모두 아래 회사가 없는 비상장 자회사(4곳 이상)는 한 칸으로 묶는다. */
(function () {
  'use strict';
  var D = window.OWN;
  var BOX_W = 168, BOX_H = 26, COL_GAP = 74, ROW = 34, PAD = 18, SEC_MIN = 1, GROUP_MIN = 4;
  var NS = 'http://www.w3.org/2000/svg';
  var byId = {}, kids = {}, inEdges = {}, outEdges = {};
  D.nodes.forEach(function (n) { byId[n.id] = n; kids[n.id] = []; inEdges[n.id] = []; outEdges[n.id] = []; });
  D.nodes.forEach(function (n) { if (n.parent) kids[n.parent].push(n.id); });
  D.edges.forEach(function (e) { inEdges[e.to].push(e); outEdges[e.from].push(e); });

  function nm(id) { return byId[id].label || byId[id].name; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fmt(p) { return (p === null || p === undefined) ? '–' : (Math.round(p * 100) / 100) + '%'; }
  function parentEdge(id) { return inEdges[id].filter(function (x) { return x.parent; })[0]; }
  function parentPct(id) { var e = parentEdge(id); return e ? e.pct : 0; }
  function listedCount(id) {
    return kids[id].reduce(function (s, k) { return s + listedCount(k); }, byId[id].stock ? 1 : 0);
  }
  function kidOrder(id) {  // 아래 상장사가 많은 곳 먼저, 그다음 지분 큰 순
    return kids[id].slice().sort(function (a, b) {
      var la = listedCount(a), lb = listedCount(b);
      if (la !== lb) return lb - la;
      return parentPct(b) - parentPct(a) || nm(a).localeCompare(nm(b), 'ko');
    });
  }
  function isLeaf(id) { var n = byId[id]; return !kids[id].length && !n.stock && !n.foreign; }
  function split(id) {  // [묶지 않는 자식, 묶는 자식]
    var ks = kidOrder(id), leaves = ks.filter(isLeaf);
    // 묶을 것이 적거나, 자식이 전부 비상장 자회사라 묶어도 한 칸만 남으면(12곳 이하) 그대로 보인다
    if (leaves.length < GROUP_MIN || (leaves.length === ks.length && ks.length <= 12)) return [ks, []];
    return [ks.filter(function (k) { return !isLeaf(k); }), leaves];
  }
  function chain(id) { var c = []; while (id) { c.unshift(id); id = byId[id].parent; } return c; }
  function tagOf(n) {
    return n.kind === 'person' ? (n.rel === '동일인' ? '동일인' : '친족') : n.stock ? '상장' : n.foreign ? '국외' : '';
  }
  function range(ids) {
    var ps = ids.map(parentPct), lo = Math.min.apply(null, ps), hi = Math.max.apply(null, ps);
    return lo === hi ? fmt(lo) : fmt(lo) + '~' + fmt(hi);
  }

  var mode = 'focus', sel = null, open = {}, gOpen = {};
  var view = document.getElementById('view'), panelEl = document.getElementById('panel');

  /* ---------- 회사 중심 ---------- */
  function renderFocus() {
    var id = sel, n = byId[id], c = chain(id), h = '';
    h += '<p class="chainline">' + c.map(function (x, i) {
      var p = i ? ' <span class="pp">' + fmt(parentPct(x)) + '</span>' : '';
      return (i ? '<span class="ar">→</span>' : '') + (x === id ? '<b>' + esc(nm(x)) + '</b>' + p :
        '<a href="#' + encodeURIComponent(x) + '" data-go="' + esc(x) + '">' + esc(nm(x)) + '</a>' + p);
    }).join(' ') + '</p>';
    h += '<div class="fx">';
    c.slice(0, -1).forEach(function (x, i) {
      h += card(x, 'anc') + '<div class="vlink"><span>' + fmt(parentPct(c[i + 1])) + '</span></div>';
    });
    var co = inEdges[id].filter(function (e) { return !e.parent && e.pct >= SEC_MIN; })
      .sort(function (a, b) { return b.pct - a.pct; });
    h += '<div class="me">';
    h += '<div class="me-h"><b>' + esc(nm(id)) + '</b><span class="tg">' + esc(tagOf(n)) + '</span></div>';
    var facts = [];
    if (n.cf !== undefined) facts.push('일가 누적 지분 <b>' + fmt(n.cf) + '</b> <span class="calc">계산값</span>');
    if (kids[id].length) facts.push('최대주주로 거느린 계열사 <b>' + kids[id].length + '곳</b>');
    if (facts.length) h += '<div class="me-f">' + facts.join('<br>') + '</div>';
    if (co.length) {
      h += '<div class="me-co">함께 가진 동일인측 ' + co.map(function (e) {
        return '<a href="#' + encodeURIComponent(e.from) + '" data-go="' + esc(e.from) + '">' + esc(nm(e.from)) + ' ' + fmt(e.pct) + '</a>';
      }).join(' · ') + '</div>';
    }
    h += '</div>';
    var sp = split(id);
    if (sp[0].length || sp[1].length) {
      h += '<div class="vlink short"></div><div class="grid">' + sp[0].map(function (k) { return card(k, 'kid'); }).join('');
      if (sp[1].length) {
        h += '<button type="button" class="card grp" data-grp="' + esc(id) + '"><span class="cn">비상장 자회사 ' +
          sp[1].length + '곳</span><span class="cp">' + range(sp[1]) + '</span><span class="cs">' +
          (gOpen[id] ? '접기' : '펼치기') + '</span></button>';
      }
      h += '</div>';
      if (sp[1].length && gOpen[id]) h += '<div class="grid sub">' + sp[1].map(function (k) { return card(k, 'kid'); }).join('') + '</div>';
    }
    var minor = outEdges[id].filter(function (e) { return !e.parent && e.pct >= SEC_MIN; });
    if (minor.length) {
      h += '<p class="minor">최대주주는 아닌 지분 ' + minor.map(function (e) {
        return '<a href="#' + encodeURIComponent(e.to) + '" data-go="' + esc(e.to) + '">' + esc(nm(e.to)) + ' ' + fmt(e.pct) + '</a>';
      }).join(' · ') + '</p>';
    }
    h += '</div>';
    view.innerHTML = h;
  }
  function card(id, cls) {
    var n = byId[id], sub = [];
    if (cls === 'kid') sub.push(fmt(parentPct(id)));
    if (kids[id].length) sub.push('아래 ' + kids[id].length + '곳');
    return '<button type="button" class="card ' + cls + (n.stock ? ' listed' : '') + (n.kind === 'person' ? ' person' : '') +
      '" data-go="' + esc(id) + '"><span class="cn">' + esc(nm(id)) + '</span><span class="tg">' + esc(tagOf(n)) +
      '</span>' + (sub.length ? '<span class="cs">' + esc(sub.join(' · ')) + '</span>' : '') + '</button>';
  }

  /* ---------- 전체 나무 ---------- */
  function resetOpen(all) {
    open = {}; gOpen = {};
    D.nodes.forEach(function (n) {
      if (kids[n.id].length && (all || listedCount(n.id) > (n.stock ? 1 : 0) || n.kind === 'person')) open[n.id] = true;
      if (all) gOpen[n.id] = true;
    });
  }
  var roots = D.nodes.filter(function (n) { return !n.parent; }).map(function (n) { return n.id; })
    .sort(function (a, b) {
      // 사람이 위 — 동일인, 나무 없는 친족, 나무 있는 친족, 그다음 국외 계열사
      var rank = function (id) { var n = byId[id]; return n.kind !== 'person' ? 3 : n.rel === '동일인' ? 0 : kids[id].length ? 2 : 1; };
      return rank(a) - rank(b) || kids[b].length - kids[a].length || nm(a).localeCompare(nm(b), 'ko');
    });

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function width(p) { return p >= 50 ? 2.6 : p >= 30 ? 1.8 : 1.1; }
  function X(c) { return PAD + c * (BOX_W + COL_GAP); }
  function Y(r) { return PAD + r * ROW + ROW / 2; }

  function renderTree() {
    var pos = {}, links = [], slot = 0;
    function place(id, depth) {
      var y = null;
      if (open[id]) {
        var sp = split(id);
        sp[0].forEach(function (k) { var p = place(k, depth + 1); if (y === null) y = p; links.push([id, k]); });
        if (sp[1].length) {
          var g = 'grp:' + id, gy = null;
          if (gOpen[id]) sp[1].forEach(function (k) { var p = place(k, depth + 2); if (gy === null) gy = p; links.push([g, k]); });
          else gy = slot++;
          pos[g] = { x: depth + 1, y: gy, grp: id, n: sp[1].length };
          links.push([id, g]);
          if (y === null) y = gy;
        }
      }
      if (y === null) y = slot++;  // 부모는 첫 자식 줄에 선다
      pos[id] = { x: depth, y: y };
      return y;
    }
    roots.forEach(function (r) { place(r, 0); slot += 0.5; });
    var cols = 0;
    Object.keys(pos).forEach(function (k) { cols = Math.max(cols, pos[k].x); });
    var W = X(cols) + BOX_W + PAD, H = PAD * 2 + slot * ROW;
    view.innerHTML = '<div class="board" id="board"></div>';
    var board = document.getElementById('board');
    var svg = el('svg', { width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': D.group + ' 지분 나무' }, board);
    var gE = el('g', {}, svg), gL = el('g', {}, svg), gN = el('g', {}, svg);
    var focus = {};
    if (sel) chain(sel).forEach(function (x) { focus[x] = true; });

    function label(x, y, txt, anchor, dim) {
      var t = el('text', { x: x, y: y, 'text-anchor': anchor, class: 'pl' + (dim ? ' dim' : '') }, gL);
      t.textContent = txt;
    }
    links.forEach(function (l) {
      var a = pos[l[0]], b = pos[l[1]];
      var x1 = X(a.x) + BOX_W, y1 = Y(a.y), x2 = X(b.x), y2 = Y(b.y);
      var real = byId[l[1]], pct = real ? parentPct(l[1]) : 0;
      var on = sel && focus[l[1]] && (focus[l[0]] || String(l[0]).indexOf('grp:') === 0);
      el('path', { d: 'M' + x1 + ' ' + y1 + 'H' + (x2 - COL_GAP / 2) + 'V' + y2 + 'H' + x2,
        class: 'ed' + (on ? ' on' : sel ? ' dim' : ''), 'stroke-width': real ? width(pct) : 1.1 }, gE);
      if (real) label(x2 - 6, y2 - 5, fmt(pct), 'end', sel && !on);
    });
    if (sel && pos[sel]) {  // 고른 상자에 닿는 그 밖의 동일인측 선
      var fan = { i: 0, o: 0 };
      D.edges.forEach(function (e) {
        if (e.parent || e.pct < SEC_MIN || (e.to !== sel && e.from !== sel)) return;
        var a = pos[e.from], b = pos[e.to];
        if (!a || !b) return;
        var k = e.to === sel ? ++fan.i : ++fan.o;
        var x1 = X(a.x) + BOX_W, y1 = Y(a.y), x2 = X(b.x), y2 = Y(b.y), lane = y2 - ROW / 2;
        el('path', { d: 'M' + x1 + ' ' + y1 + 'H' + (x1 + 8 + 5 * k) + 'V' + lane + 'H' + (x2 - COL_GAP / 2 + 6 + 4 * k) + 'V' + y2 + 'H' + x2,
          class: 'ed sec on', 'stroke-width': width(e.pct) }, gE);
        // 고른 회사로 들어오는 선은 숫자를 주주 쪽 끝에 — 들어오는 끝에 모으면 겹친다
        if (e.to === sel) label(x1 + 4, y1 - 5, fmt(e.pct), 'start', false);
        else label(x2 - 6, y2 + 11, fmt(e.pct), 'end', false);
      });
    }
    Object.keys(pos).forEach(function (id) {
      var p = pos[id], gx = X(p.x), gy = Y(p.y) - BOX_H / 2;
      if (p.grp) {
        var gg = el('g', { class: 'nd grp' + (sel && !focus[p.grp] ? ' dim' : ''), transform: 'translate(' + gx + ',' + gy + ')', 'data-tog-grp': p.grp }, gN);
        el('rect', { width: BOX_W, height: BOX_H, rx: 4, class: 'bx' }, gg);
        var gt = el('text', { x: 9, y: BOX_H / 2 + 1, class: 'nm' }, gg);
        gt.textContent = '비상장 자회사 ' + p.n + '곳';
        var gs = el('text', { x: BOX_W - 8, y: BOX_H / 2 + 1, 'text-anchor': 'end', class: 'tag' }, gg);
        gs.textContent = gOpen[p.grp] ? '접기' : '펼치기';
        return;
      }
      var n = byId[id], linked = sel && (inEdges[sel].some(function (e) { return e.from === id; }) || outEdges[sel].some(function (e) { return e.to === id; }));
      var g = el('g', { class: 'nd ' + n.kind + (n.stock ? ' listed' : '') + (n.foreign ? ' foreign' : '') + (id === sel ? ' sel' : '') +
        (sel && !focus[id] && !linked ? ' dim' : ''), transform: 'translate(' + gx + ',' + gy + ')', tabindex: 0, 'data-id': id }, gN);
      el('rect', { width: BOX_W, height: BOX_H, rx: n.kind === 'person' ? 13 : 4, class: 'bx' }, g);
      var s = nm(id), t = el('text', { x: 9, y: BOX_H / 2 + 1, class: 'nm' }, g);
      t.textContent = s.length > 13 ? s.slice(0, 12) + '…' : s;
      el('title', {}, g).textContent = s;
      if (tagOf(n)) el('text', { x: BOX_W - (kids[id].length ? 30 : 8), y: BOX_H / 2 + 1, 'text-anchor': 'end', class: 'tag' }, g).textContent = tagOf(n);
      if (kids[id].length) {
        var mg = el('g', { 'data-tog': id }, g);
        el('rect', { x: BOX_W - 24, y: 5, width: 18, height: BOX_H - 10, rx: 3, class: 'more' }, mg);
        el('text', { x: BOX_W - 15, y: BOX_H / 2 + 1, class: 'more-t' }, mg).textContent = open[id] ? '−' : kids[id].length;
      }
    });
    if (sel && pos[sel]) {
      board.scrollLeft = Math.max(0, X(pos[sel].x) - board.clientWidth / 3);
      board.scrollTop = Math.max(0, Y(pos[sel].y) - board.clientHeight / 2);
    }
  }

  /* ---------- 영수증 칸 ---------- */
  function row(name, sub, pct, total, later) {
    var mv = later && later.moved ? '<span class="c moved">' + esc(later.asof) + ' 정기보고서 ' + fmt(later.pct) + '</span>' : '';
    var tot = (total !== null && total !== undefined && Math.abs(total - (pct || 0)) > 0.005) ? '<span class="c">우선주 포함 ' + fmt(total) + '</span>' : '';
    return '<tr><td>' + esc(name) + (sub ? '<span class="c">' + esc(sub) + '</span>' : '') + '</td><td class="n">' +
      fmt(pct) + tot + mv + '</td></tr>';
  }
  function panel(id) {
    var n = byId[id], h = '<h2>' + esc(nm(id)) + '</h2>', bits = [];
    if (n.kind === 'person') bits.push(n.rel === '동일인' ? '동일인' : '동일인의 ' + n.rel);
    else {
      bits.push(n.stock ? '상장 ' + n.stock : n.foreign ? '국외 계열사' : '비상장');
      if (kids[id].length) bits.push('최대주주로 거느린 계열사 ' + kids[id].length + '곳');
    }
    h += '<p class="sub">' + esc(bits.join(' · ')) + '</p>';
    if (n.kind !== 'person' && !n.foreign) {
      h += '<h3>동일인측 주주 (보통주)</h3>';
      var hs = n.holders.slice().sort(function (a, b) { return (b.common_pct || 0) - (a.common_pct || 0); });
      h += hs.length ? '<table>' + hs.map(function (r) {
        return row(r.label || r.name, r.cat === '계열회사' ? '계열사' : r.cat, r.common_pct, r.total_pct, r.later);
      }).join('') + '</table>' : '<p class="empty">없음</p>';
      var officers = n.side.filter(function (r) { return r.cat === '등기된 임원'; });
      var rows = n.side.filter(function (r) { return r.cat !== '등기된 임원'; }).map(function (r) {
        var self = r.cat === '자기주식';
        return row(self ? '자기주식' : (r.label || r.name), self ? '' : r.cat, r.common_pct, r.total_pct, r.later);
      });
      if (officers.length) {
        var sum = function (k) { return officers.reduce(function (a, r) { return a + (r[k] || 0); }, 0); };
        rows.push(row('등기 임원 ' + officers.length + '명', '합계', sum('common_pct'), sum('total_pct'), null));
      }
      if (rows.length) h += '<h3>그 밖의 주주</h3><table>' + rows.join('') + '</table>';
      if (n.cf !== undefined) {
        h += '<h3>일가 누적 지분 ' + fmt(n.cf) + ' <span class="calc">계산값</span></h3><table>' +
          n.cf_terms.filter(function (t) { return t.v >= 0.005 || t.unknown; }).map(function (t) {
            var who = byId[t.from].kind === 'person' ? esc(nm(t.from)) + ' 직접' :
              esc(nm(t.from)) + ' ' + fmt(t.pct) + ' × ' + (t.unknown ? '주주 모름' : fmt(t.up));
            return '<tr><td>' + who + '</td><td class="n">' + fmt(t.v) + '</td></tr>';
          }).join('') + '</table><p class="note">주주 지분율 × 그 주주에 대한 일가 누적 지분을 더했다. 공시에 없는 값이다.</p>';
      }
    }
    var outs = outEdges[id].slice().sort(function (a, b) { return b.pct - a.pct; });
    if (outs.length) {
      h += '<h3>가진 계열사 지분 (보통주)</h3><table>' + outs.map(function (e) {
        return row(nm(e.to), e.parent ? '최대 동일인측 주주' : '', e.pct, e.total_pct, e.later);
      }).join('') + '</table>';
    }
    h += '<p class="src">출처: <a href="' + esc(D.source.url) + '" target="_blank" rel="noopener">' + esc(D.source.label) + '</a> (' +
      esc(D.source.basis) + ', ' + esc(D.source.rcept_dt.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3')) + ' 접수)';
    var laters = [];
    n.holders.concat(n.side).forEach(function (r) { if (r.later && laters.indexOf(r.later.url) < 0) laters.push(r.later.url); });
    laters.forEach(function (u) { h += '<br>뒤값: <a href="' + esc(u) + '" target="_blank" rel="noopener">DART 정기보고서</a>'; });
    panelEl.innerHTML = h + '</p>';
  }

  /* ---------- 조작 ---------- */
  function render() {
    document.body.setAttribute('data-mode', mode);
    ['m-focus', 'm-tree'].forEach(function (b) { document.getElementById(b).setAttribute('aria-pressed', b === 'm-' + mode); });
    if (mode === 'focus') renderFocus(); else renderTree();
    panel(sel);
  }
  function go(id, keepMode) {
    if (!byId[id]) return;
    sel = id;
    var up = byId[id].parent;
    while (up) { open[up] = true; up = byId[up].parent; }
    if (byId[id].parent && isLeaf(id)) gOpen[byId[id].parent] = true;
    render();
    if (history.replaceState) history.replaceState(null, '', '#' + encodeURIComponent(id));
    if (mode === 'focus' && !keepMode) view.scrollIntoView({ block: 'nearest' });
  }
  view.addEventListener('click', function (ev) {
    var t = ev.target.closest('[data-tog]');
    if (t) { var id = t.getAttribute('data-tog'); open[id] = !open[id]; render(); return; }
    var g = ev.target.closest('[data-tog-grp]');
    if (g) { var gid = g.getAttribute('data-tog-grp'); gOpen[gid] = !gOpen[gid]; render(); return; }
    var gb = ev.target.closest('[data-grp]');
    if (gb) { var bid = gb.getAttribute('data-grp'); gOpen[bid] = !gOpen[bid]; render(); return; }
    var a = ev.target.closest('[data-go],[data-id]');
    if (a) { ev.preventDefault(); go(a.getAttribute('data-go') || a.getAttribute('data-id')); }
  });
  view.addEventListener('keydown', function (ev) {
    var nd = ev.target.closest('[data-id]');
    if (nd && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); go(nd.getAttribute('data-id')); }
  });
  panelEl.addEventListener('click', function (ev) {
    var a = ev.target.closest('[data-go]');
    if (a) { ev.preventDefault(); go(a.getAttribute('data-go')); }
  });
  document.getElementById('m-focus').onclick = function () { mode = 'focus'; render(); };
  document.getElementById('m-tree').onclick = function () { mode = 'tree'; render(); };
  document.getElementById('b-listed').onclick = function () { resetOpen(false); render(); };
  document.getElementById('b-all').onclick = function () { resetOpen(true); render(); };
  var q = document.getElementById('q');
  q.addEventListener('change', function () {
    var v = q.value.replace(/\s/g, '');
    if (!v) return;
    var hit = D.nodes.filter(function (n) { return n.name.replace(/\s/g, '') === v; })[0] ||
      D.nodes.filter(function (n) { return n.name.replace(/\s/g, '').indexOf(v) >= 0; })[0];
    if (hit) go(hit.id);
  });

  window.addEventListener('hashchange', function () {
    var h = decodeURIComponent(location.hash.slice(1));
    if (byId[h] && h !== sel) go(h);
  });
  resetOpen(false);
  var start = decodeURIComponent(location.hash.slice(1));
  sel = byId[start] ? start : D.start;
  go(sel, true);
})();
