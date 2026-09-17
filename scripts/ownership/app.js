/* 지분 사슬 — 부모 선으로 왼쪽에서 오른쪽으로 나무를 세우고, 그 밖의 동일인측 선은 점선으로 겹친다.
   점선은 칸 사이 통로(세로)와 줄 사이 통로(가로)로만 지나가 상자를 가로지르지 않는다. */
(function () {
  'use strict';
  var D = window.OWN;
  var BOX_W = 168, BOX_H = 26, COL_GAP = 74, ROW = 34, PAD = 18, SEC_MIN = 1;
  var NS = 'http://www.w3.org/2000/svg';
  var byId = {}, kids = {}, inEdges = {}, outEdges = {};
  D.nodes.forEach(function (n) { byId[n.id] = n; kids[n.id] = []; inEdges[n.id] = []; outEdges[n.id] = []; });
  D.nodes.forEach(function (n) { if (n.parent) kids[n.parent].push(n.id); });
  D.edges.forEach(function (e) { inEdges[e.to].push(e); outEdges[e.from].push(e); });

  function listedBelow(id) {
    return kids[id].some(function (k) { return byId[k].stock || listedBelow(k); });
  }
  function listedCount(id) {
    return kids[id].reduce(function (s, k) { return s + (byId[k].stock ? 1 : 0) + listedCount(k); }, byId[id].stock ? 1 : 0);
  }
  function kidOrder(id) {  // 아래 상장사가 많은 곳 먼저, 그다음 지분 큰 순
    return kids[id].slice().sort(function (a, b) {
      var A = byId[a], B = byId[b], la = listedCount(a), lb = listedCount(b);
      if (la !== lb) return lb - la;
      return parentPct(b) - parentPct(a) || A.name.localeCompare(B.name, 'ko');
    });
  }
  function parentPct(id) {
    var e = inEdges[id].filter(function (x) { return x.parent; })[0];
    return e ? e.pct : 0;
  }

  var open = {};
  function resetOpen(mode) {
    open = {};
    D.nodes.forEach(function (n) {
      if (!kids[n.id].length) return;
      if (mode === 'all') open[n.id] = true;
      else if (listedBelow(n.id) || n.kind === 'person') open[n.id] = true;
    });
  }
  resetOpen('listed');

  var roots = D.nodes.filter(function (n) { return !n.parent; }).map(function (n) { return n.id; })
    .sort(function (a, b) {
      var A = byId[a], B = byId[b];
      // 사람이 위 — 동일인, 나무 없는 친족, 나무 있는 친족, 그다음 국외 계열사
      var rank = function (n, id) { return n.kind !== 'person' ? 3 : n.rel === '동일인' ? 0 : kids[id].length ? 2 : 1; };
      var ra = rank(A, a), rb = rank(B, b);
      if (ra !== rb) return ra - rb;
      return kids[b].length - kids[a].length || A.name.localeCompare(B.name, 'ko');
    });

  var pos, sel = null;
  function layout() {
    pos = {};
    var slot = 0;
    function place(id, depth) {
      var ks = open[id] ? kidOrder(id) : [];
      var y;
      if (ks.length) {
        var first = null;  // 부모는 첫 자식 줄에 선다 — 가운데에 세우면 일가가 판 한복판으로 내려간다
        ks.forEach(function (k) { var p = place(k, depth + 1); if (first === null) first = p; });
        y = first;
      } else {
        y = slot++;
      }
      pos[id] = { x: depth, y: y };
      return y;
    }
    roots.forEach(function (r) { place(r, 0); slot += 0.5; });
    return slot;
  }
  function X(c) { return PAD + c * (BOX_W + COL_GAP); }
  function Y(r) { return PAD + r * ROW + ROW / 2; }
  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function width(p) { return p >= 50 ? 2.6 : p >= 30 ? 1.8 : 1.1; }
  function fmt(p) { return (p === null || p === undefined) ? '–' : (Math.round(p * 100) / 100) + '%'; }

  function chainUp(id) {
    var s = {};
    while (id) { s[id] = true; id = byId[id].parent; }
    return s;
  }

  var svg, board = document.getElementById('board');
  function render() {
    var rows = layout();
    var cols = 0;
    Object.keys(pos).forEach(function (k) { cols = Math.max(cols, pos[k].x); });
    var W = X(cols) + BOX_W + PAD, H = PAD * 2 + rows * ROW;
    board.innerHTML = '';
    svg = el('svg', { width: W, height: H, viewBox: '0 0 ' + W + ' ' + H, role: 'img',
      'aria-label': D.group + ' 지분 사슬' }, board);
    var gE = el('g', {}, svg), gL = el('g', {}, svg), gN = el('g', {}, svg);
    var focus = sel ? chainUp(sel) : null, fan = {};

    D.edges.forEach(function (e) {
      var a = pos[e.from], b = pos[e.to];
      if (!a || !b) return;
      // 보조선은 고른 상자에 닿는 것만 — 늘 그리면 판이 점선으로 덮인다
      // 보조선은 고른 상자에 닿는 것만. 일가 직접 지분은 판 위 표가 맡는다
      if (!e.parent && (e.pct < SEC_MIN || !sel || (e.to !== sel && e.from !== sel))) return;
      var x1 = X(a.x) + BOX_W, y1 = Y(a.y), x2 = X(b.x), y2 = Y(b.y), d;
      if (e.parent) {
        var mx = x2 - COL_GAP / 2;
        d = 'M' + x1 + ' ' + y1 + 'H' + mx + 'V' + y2 + 'H' + x2;
      } else {
        var k = (fan[e.to === sel ? 'in' : 'out'] = (fan[e.to === sel ? 'in' : 'out'] || 0) + 1);
        var gx1 = x1 + 8 + 5 * k, gx2 = x2 - COL_GAP / 2 + 6 + 4 * k, lane = Y(b.y) - ROW / 2;
        d = 'M' + x1 + ' ' + y1 + 'H' + gx1 + 'V' + lane + 'H' + gx2 + 'V' + y2 + 'H' + x2;
      }
      var on = sel && (e.to === sel || e.from === sel || (e.parent && focus[e.to] && focus[e.from]));
      el('path', { d: d, class: 'ed' + (e.parent ? '' : ' sec') + (on ? ' on' : (sel ? ' dim' : '')),
        'stroke-width': width(e.pct) }, gE);
      var lx = x2 - 6, ly = y2 - 5, anchor = 'end';
      // 고른 회사로 들어오는 보조선은 숫자를 주주 쪽 끝에 — 들어오는 끝에 모으면 겹친다
      if (!e.parent && e.to === sel) { lx = x1 + 4; ly = y1 - 5; anchor = 'start'; }
      var t = el('text', { x: lx, y: ly, 'text-anchor': anchor, class: 'pl' + (sel && !on ? ' dim' : '') }, gL);
      t.textContent = fmt(e.pct);
    });

    Object.keys(pos).forEach(function (id) {
      var n = byId[id], p = pos[id];
      var cls = 'nd ' + n.kind + (n.stock ? ' listed' : '') + (n.foreign ? ' foreign' : '') +
        (id === sel ? ' sel' : '') + (sel && !focus[id] && id !== sel && !linked(id) ? ' dim' : '');
      var g = el('g', { class: cls, transform: 'translate(' + X(p.x) + ',' + (Y(p.y) - BOX_H / 2) + ')',
        tabindex: 0, 'data-id': id }, gN);
      el('rect', { width: BOX_W, height: BOX_H, rx: n.kind === 'person' ? 13 : 4, class: 'bx' }, g);
      var nm = n.label || n.name, label = nm.length > 13 ? nm.slice(0, 12) + '…' : nm;
      var t = el('text', { x: 9, y: BOX_H / 2 + 1, class: 'nm' }, g);
      t.textContent = label;
      var tt = el('title', {}, g); tt.textContent = nm;
      var tag = n.kind === 'person' ? (n.rel === '동일인' ? '동일인' : '친족') : n.stock ? '상장' : n.foreign ? '국외' : '';
      if (tag) {
        var tg = el('text', { x: BOX_W - (kids[id].length ? 30 : 8), y: BOX_H / 2 + 1, 'text-anchor': 'end', class: 'tag' }, g);
        tg.textContent = tag;
      }
      if (kids[id].length) {
        var mg = el('g', { class: 'tog', 'data-tog': id }, g);
        el('rect', { x: BOX_W - 24, y: 5, width: 18, height: BOX_H - 10, rx: 3, class: 'more' }, mg);
        var mt = el('text', { x: BOX_W - 15, y: BOX_H / 2 + 1, class: 'more-t' }, mg);
        mt.textContent = open[id] ? '−' : kids[id].length;
      }
    });
  }
  function linked(id) {
    if (!sel) return false;
    return inEdges[sel].some(function (e) { return e.from === id; }) || outEdges[sel].some(function (e) { return e.to === id; });
  }

  board.addEventListener('click', function (ev) {
    var tog = ev.target.closest('[data-tog]');
    if (tog) { var id = tog.getAttribute('data-tog'); open[id] = !open[id]; render(); return; }
    var nd = ev.target.closest('[data-id]');
    if (nd) { select(nd.getAttribute('data-id')); }
  });
  board.addEventListener('keydown', function (ev) {
    var nd = ev.target.closest('[data-id]');
    if (nd && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); select(nd.getAttribute('data-id')); }
  });

  function select(id) {
    sel = id;
    var up = byId[id].parent;
    while (up) { open[up] = true; up = byId[up].parent; }
    render();
    panel(id);
    var p = pos[id];
    if (p) {
      var bx = X(p.x) - board.clientWidth / 3, by = Y(p.y) - board.clientHeight / 2;
      board.scrollTo({ left: Math.max(0, bx), top: Math.max(0, by), behavior: 'smooth' });
    }
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function row(name, sub, pct, total, later) {
    var mv = later && later.moved ? '<span class="c moved">' + esc(later.asof) + ' 정기보고서 ' + fmt(later.pct) + '</span>' : '';
    var tot = (total !== null && total !== undefined && Math.abs(total - (pct || 0)) > 0.005) ? '<span class="c">우선주 포함 ' + fmt(total) + '</span>' : '';
    return '<tr><td>' + esc(name) + (sub ? '<span class="c">' + esc(sub) + '</span>' : '') + '</td><td class="n">' +
      fmt(pct) + tot + mv + '</td></tr>';
  }
  var panelEl = document.getElementById('panel');
  function panel(id) {
    var n = byId[id], h = '';
    h += '<h2>' + esc(n.label || n.name) + '</h2>';
    var bits = [];
    if (n.kind === 'person') bits.push(n.rel === '동일인' ? '동일인' : '동일인의 ' + n.rel);
    else {
      bits.push(n.stock ? '상장 ' + n.stock : n.foreign ? '국외 계열사' : '비상장');
      if (kids[id].length) bits.push('지배하는 계열사 ' + kids[id].length + '곳');
    }
    h += '<p class="sub">' + esc(bits.join(' · ')) + '</p>';
    if (n.kind !== 'person' && !n.foreign) {
      h += '<h3>동일인측 주주 (보통주)</h3>';
      var hs = n.holders.slice().sort(function (a, b) { return (b.common_pct || 0) - (a.common_pct || 0); });
      h += hs.length ? '<table>' + hs.map(function (r) {
        return row(r.label || r.name, r.cat === '계열회사' ? '계열사' : r.cat, r.common_pct, r.total_pct, r.later);
      }).join('') + '</table>' : '<p class="empty">없음</p>';
      var officers = n.side.filter(function (r) { return r.cat === '등기된 임원'; });
      var side = n.side.filter(function (r) { return r.cat !== '등기된 임원'; });
      var rows = side.map(function (r) {
        var self = r.cat === '자기주식';
        return row(self ? '자기주식' : r.name, self ? '' : r.cat, r.common_pct, r.total_pct, r.later);
      });
      if (officers.length) {
        var sum = function (k) { return officers.reduce(function (a, r) { return a + (r[k] || 0); }, 0); };
        rows.push(row('등기 임원 ' + officers.length + '명', '합계', sum('common_pct'), sum('total_pct'), null));
      }
      if (rows.length) h += '<h3>그 밖의 주주</h3><table>' + rows.join('') + '</table>';
    }
    var outs = outEdges[id].slice().sort(function (a, b) { return b.pct - a.pct; });
    if (outs.length) {
      h += '<h3>가진 계열사 지분 (보통주)</h3><table>' + outs.map(function (e) {
        return row(byId[e.to].label || byId[e.to].name, e.parent ? '최대 동일인측 주주' : '', e.pct, e.total_pct, e.later);
      }).join('') + '</table>';
    }
    h += '<p class="src">출처: <a href="' + esc(D.source.url) + '" target="_blank" rel="noopener">' +
      esc(D.source.label) + '</a> (' + esc(D.source.basis) + ', ' + esc(D.source.rcept_dt.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3')) + ' 접수)';
    var laters = [];
    n.holders.concat(n.side).forEach(function (r) { if (r.later && laters.indexOf(r.later.url) < 0) laters.push(r.later.url); });
    laters.forEach(function (u) { h += '<br>뒤값: <a href="' + esc(u) + '" target="_blank" rel="noopener">DART 정기보고서</a>'; });
    h += '</p>';
    panelEl.innerHTML = h;
  }

  document.getElementById('b-listed').onclick = function () { resetOpen('listed'); render(); };
  document.getElementById('b-all').onclick = function () { resetOpen('all'); render(); };
  var q = document.getElementById('q');
  q.addEventListener('change', function () {
    var v = q.value.replace(/\s/g, '');
    if (!v) return;
    var hit = D.nodes.filter(function (n) { return n.name.replace(/\s/g, '') === v; })[0] ||
      D.nodes.filter(function (n) { return n.name.replace(/\s/g, '').indexOf(v) >= 0; })[0];
    if (hit) select(hit.id);
  });

  render();
  panel(D.nodes.filter(function (n) { return n.name === D.start; })[0].id);  // 첫 화면은 흐리지 않는다
})();
