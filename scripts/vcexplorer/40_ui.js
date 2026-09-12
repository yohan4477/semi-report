// 40_ui.js
// 화면 — 서랍·띠·회사 목록·앱
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
  // 비중 없는 칩이 많은 줄은 접는다 — 블룸 공급원 21개 중 비중 있는 것은 5개뿐인데
  // 두 줄로 펼치면 띠가 판을 밀어낸다. 「+N」을 누르면 편다
  var m2 = useState({}), more = m2[0], setMore = m2[1];
  var FOLD_OVER = 8, FOLD_MIN = 3;
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
    var foldable = list.filter(function(x){
      var sh = pick(kind, x);
      return !(sh && den && sh.denominator === den) && !x.unallocated
             && p.axis !== kind + ':' + x.id; });
    var fold = list.length > FOLD_OVER && foldable.length >= FOLD_MIN;
    var folded = fold && !more[kind];
    var prev = null;
    var items = list.reduce(function(acc, x){
      var key = kind + ':' + x.id, on = p.axis === key, sh = pick(kind, x);
      var show = sh && den && sh.denominator === den;
      if (folded && foldable.indexOf(x) >= 0) return acc;
      // 분류 체계(무리)가 바뀌는 자리에 이름표 하나 — 두 체계의 비중을 한 줄로 더하지 않게
      if (x.group_label && (!prev || prev.group_label !== x.group_label))
        acc.push(h('span', { key:'g' + x.id, className:'axgroup' }, x.group_label));
      prev = x;
      acc.push(h('button', { key:x.id, title: tip(x),
        className: 'axchip' + (on ? ' on' : '') + (x.unallocated ? ' un' : ''),
        onClick: function(){ p.onPick(on ? null : key); } }, [
        x.label, show ? h('i', { key:'s' },
          sh.value + '%' + (sh.stale ? ' ' + (sh.period || '') : '')) : null ]));
      return acc;
    }, []);
    if (fold) items.push(h('button', { key:'*more', className:'axchip fold',
      title: folded ? '비중이 안 적힌 분류 ' + foldable.length + '개를 편다' : '비중 없는 분류를 접는다',
      onClick: function(){ var n = {}; n[kind] = folded; setMore(Object.assign({}, more, n)); } },
      folded ? '+' + foldable.length + ' 비중 없음' : '접기'));
    return h('div', { key:kind, className:'axrow' }, [
      h('b', { key:'b' }, label),
      h('div', { key:'c', className:'axchips' }, [all].concat(items))
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

// ── 표 ──────────────────────────────────────────────────────────────
// 판의 관계 전부를 한 장으로. 머리를 누르면 그 열로 정렬한다. 비중은 그 해 값이고
// 분모가 서로 다를 수 있어 숫자 옆에 분모를 적는다 — 한 열에서 더하지 않게
function Table(p){
  var st = useState({ key:'share', dir:-1 }), sort = st[0], setSort = st[1];
  var qq = useState(''), q = qq[0], setQ = qq[1];
  var rels = p.chain ? CHAINS[p.chain].relationships : relsOf(p.focal);
  var m = clsOf(p.chain);
  rels = rels.filter(function(r){ return activeIn(r, p.year); });
  var rows = rels.map(function(r){
    var up = r.target_entity === p.focal;
    var other = up ? r.source_entity : (r.source_entity === p.focal ? r.target_entity : null);
    var sh = shareIn(r.id, p.year);
    var cls = (r.supply_source_ids || []).map(function(i){ return (m.ss[i] || {}).label || i; })
      .concat((r.revenue_type_ids || []).map(function(i){ return (m.rt[i] || {}).label || i; }));
    return { r:r, up:up, other:other,
      from: nm(r.source_entity), to: nm(r.target_entity),
      rel: relKo(r.relationship_type), lane: LANE_KO[r.lane] || r.lane,
      cls: cls.join(' · '),
      share: sh ? (sh.value !== null && sh.value !== undefined ? sh.value
              : (sh.value_high !== null && sh.value_high !== undefined ? sh.value_high : null)) : null,
      shareTxt: sh ? ((sh.value_low !== null && sh.value_low !== undefined)
                      ? sh.value_low + '~' + sh.value_high + '%' : fmt(sh.value) + '%') : '',
      den: sh ? (sh.denominator || '') : '',
      ev: r.evidence_level, evKo: EV_KO[r.evidence_level] || r.evidence_level,
      from_y: r.valid_from || '', srcN: (r.source_ids || []).length };
  });
  var EVR = { CONFIRMED:0, ESTIMATED:1, INFERRED:2, UNDISCLOSED:3, HISTORICAL_CURRENT_UNKNOWN:4 };
  function keyOf(x){
    switch (sort.key){
      case 'share': return x.share === null ? -1 : x.share;
      case 'ev': return -(EVR[x.ev] === undefined ? 9 : EVR[x.ev]);
      case 'from_y': return x.from_y;
      case 'from': return x.from;
      case 'to': return x.to;
      case 'rel': return x.rel;
      case 'cls': return x.cls;
      default: return 0;
    }
  }
  rows.sort(function(a, b){
    var ka = keyOf(a), kb = keyOf(b);
    var c = ka < kb ? -1 : ka > kb ? 1 : 0;
    return c * sort.dir || (a.from < b.from ? -1 : 1);
  });
  if (q) {
    var ql = q.toLowerCase();
    rows = rows.filter(function(x){
      return (x.from + ' ' + x.to + ' ' + x.rel + ' ' + x.cls).toLowerCase().indexOf(ql) >= 0; });
  }
  function th(key, label){
    var on = sort.key === key;
    return h('th', { key:key, style:{ cursor:'pointer', whiteSpace:'nowrap' },
      onClick: function(){ setSort({ key:key, dir: on ? -sort.dir : (key === 'share' || key === 'ev' ? -1 : 1) }); } },
      label + (on ? (sort.dir > 0 ? ' \u2191' : ' \u2193') : ''));
  }
  return h('div', { className:'pane' }, [
    h('h2', { key:'t' }, nm(p.focal) + ' — ' + p.year + ' 관계 ' + rows.length + '줄'),
    h('p', { key:'n', className:'note' }, [
      h('span', { key:'a' }, '머리를 누르면 그 열로 정렬한다. 비중은 그 해 값이고 분모가 줄마다 다를 수 있다 — 한 열에서 더하지 않는다. '),
      h('input', { key:'q', value:q, placeholder:'이름·관계·분류로 거르기',
        onChange: function(ev){ setQ(ev.target.value); },
        style:{ font:'inherit', fontSize:'12.5px', padding:'3px 8px', border:'1px solid var(--line)',
                borderRadius:'5px', marginLeft:'6px', minWidth:'180px' } }) ]),
    h('div', { key:'w', style:{ overflowX:'auto' } },
      h('table', { className:'t' }, [
        h('thead', { key:'h' }, h('tr', null, [ th('from', '어디서'), th('to', '어디로'),
          th('rel', '관계'), th('cls', '공급원·매출원'), th('share', p.year + ' 비중'),
          h('th', { key:'den' }, '분모'), th('ev', '근거'), th('from_y', '언제부터'),
          h('th', { key:'src' }, '출처') ])),
        h('tbody', { key:'b' }, rows.map(function(x){
          return h('tr', { key:x.r.id, className:'pick',
            onClick: function(){ if (x.other) p.onPick(x.other); } }, [
            h('td', { key:1, className:'nw' }, withFlag(x.r.source_entity, 'a')),
            h('td', { key:2, className:'nw' }, withFlag(x.r.target_entity, 'b')),
            h('td', { key:3 }, x.rel + ' · ' + x.lane),
            h('td', { key:4 }, x.cls || '—'),
            h('td', { key:5, className:'nw', style:{ fontWeight:600 } }, x.shareTxt || '—'),
            h('td', { key:6, style:{ color:'var(--ink3)', fontSize:'11.5px' } }, x.den || '—'),
            h('td', { key:7 }, h('span', { className:'badge' + (x.ev === 'CONFIRMED' ? '' : ' est') }, x.evKo)),
            h('td', { key:8, className:'nw' }, x.from_y || '—'),
            h('td', { key:9 }, x.srcN ? x.srcN + '건' : '—') ]);
        }))
      ]))
  ]);
}

// ── 앱 ──────────────────────────────────────────────────────────────
function prefAll(){
  try { return localStorage.getItem('vc_openall') === '1'; } catch (e) { return false; }
}

function App(){
  var u0 = readUrl(true);
  var a = useState(u0.focal), focal = a[0], setFocal = a[1];
  var b = useState(u0.year), year = b[0], setYear = b[1];
  var c = useState(u0.mode), mode = c[0], setMode = c[1];
  // 「전부 펴기」는 기억한다 — 한 번 누르면 다음 회사·다음 방문에도 클릭 없이 펴진 채로
  // 열린다. 「접기」가 기억을 지운다. 주소에 open= 이 있으면 그쪽이 먼저다
  var d = useState(u0.open.length ? u0.open : (prefAll() ? ['*'] : [])),
      open = d[0], setOpen = d[1];   // 펼친 상자 id. '*' 는 전부
  function setAll(on){
    try { if (on) localStorage.setItem('vc_openall', '1'); else localStorage.removeItem('vc_openall'); }
    catch (e) {}
    setOpen(on ? ['*'] : []);
  }
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
  var l2 = useState(false), lgOpen = l2[0], setLgOpen = l2[1];
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
    setFocal(id); setOpen(prefAll() ? ['*'] : []); setSel({ kind:'ent', id:id }); setAxis(null);
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
    if (node.data.kind === 'cluster') { toggleOpen(node.id); setPanTo(node.id); return; }
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
      onClick: function(){ setMode('current'); setMenu(false); } }, nm(focal)),
    // 표 — 이 판의 관계를 비중·근거·기간 순으로 정렬해 한 장으로(SPLC Key Metrics 꼴)
    h('button', { key:'tab', className: (mode === 'table' && !menu) ? 'on' : '',
      onClick: function(){ setMode('table'); setMenu(false); } }, '표')
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
          onClick: function(){ setAll(!allOpen); } }, allOpen ? '접기' : '전부 펴기') : null,
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
  else if (mode === 'table')
    body = h(Table, { focal:focal, chain:gr.chain, year:year,
      onPick: function(id){ setMode('current'); goFocal(id); } });
  else if (mode === 'bom') body = h(Bom, { focal:focal, onDrill:drill });
  else body = h('div', { key:'cv', className:'canvas' + (busy ? ' loading' : '') }, [
    busy ? null : h(HdrBar, { key:'hb', nodes: gr.nodes, vp: vp }),
    // 좁은 화면 — 조작은 엄지 자리(아래)에. 오른쪽은 전부 펴기·서랍, 왼쪽은 뒤로 한 단
    narrow ? h('div', { key:'fab', className:'fab' }, [
      h('button', { key:'all', className:'iconbtn' + (allOpen ? ' on' : ''),
        title: allOpen ? '접기' : '전부 펴기', 'aria-label':'전부 펴기',
        onClick: function(){ setAll(!allOpen); } }, ICON_ALL),
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
      (!narrow && allOpen && !drw && window.innerWidth >= 1200 && MiniMap) ? h(MiniMap, { key:'mm', pannable:true, zoomable:true,
        nodeStrokeWidth:0, maskColor:'rgba(232,235,240,.6)',
        nodeColor:function(n){ return n.type === 'hdr' ? 'transparent'
          : (n.data && n.data.focal ? '#0E6B66' : (n.data && n.data.kind === 'lane' ? '#c6ccd8'
             : (n.data && n.data.bott ? '#9B1C3A' : (n.data && n.data.kr ? '#B4620A'
             : (n.data && n.data.side === 'cust' ? '#31507A' : '#9aa3b5'))))); },
        style:{ width:180, height:120 } }) : null
    ])
  ]);

  // 범례는 세 줄 글 벽이라 접어 두고 「범례」를 누르면 편다
  var legend = h('div', { key:'lg', className:'legend' + (lgOpen ? ' open' : '') }, [
    h('button', { key:'tg', className:'lgbtn', onClick: function(){ setLgOpen(!lgOpen); } },
      lgOpen ? '범례 접기' : '범례'),
    h('b', { key:'k' }, '색'),
    h('i', { key:'k1', className:'lsw tsmc' }, '타겟'),
    h('i', { key:'k2', className:'lsw kr' }, '한국 회사'),
    h('i', { key:'k3', className:'lsw jp' }, '병목 — 공급 여력 HIGH 이상'),
    h('i', { key:'k4', className:'lsw cust' }, '고객'),
    h('i', { key:'k5', className:'lsw sup' }, '그 밖의 공급사'),
    h('i', { key:'k6', className:'lsw mid' }, '점선 테두리 중개·유통'),
    h('b', { key:'b' }, '선'),
    h('i', { key:1 }, '실선 공시로 확인 — 공급 쪽 회색, 고객 쪽 남색'),
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
    (mode === 'current' || mode === 'timeline' || mode === 'table') ? scrub : null,
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
