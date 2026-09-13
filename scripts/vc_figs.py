# -*- coding: utf-8 -*-
u"""밸류체인 그림 장의 데이터 절 — TSMC 장(2~8절, 사용자가 준 그림)의 꼴을 다른 사슬에도 맞춘다(2026-09-13).

TSMC 2~8절은 조사 보고서에서 손으로 그린 그림(드라이버 트리·단위경제·마진 풀·히트맵·토네이도·시간축·지분
지도)이다. 다른 사슬에는 그 보고서가 없으니 같은 꼴(번호 절·짧은 설명·그림 하나)을 사슬 데이터
(classifications·relationships·observations·claims)로만 세운다. 원문에 없는 값은 안 그린다 — 단위경제·마진
풀·시나리오처럼 데이터에 없는 절은 세우지 않는다.

  2 매출 트리      매출 → 갈래(비중) → 그 갈래의 고객          classifications.revenue_types + DOWNSTREAM 관계
  3 공급원 트리    앞단 → 갈래(비중) → 공급사                  classifications.supply_sources + 공급 관계
  4 병목 히트맵    공급 여력·경제 중요도·근거 등급              relationships.capacity_criticality
  5 고객 집중도    고객별 매출 비중 막대                        observations.customer_revenue_share
  6 시간축         해마다 회사·앞단·뒷단 줄                     claims.period
  7 지분·소유      회사를 가운데 둔 지분 지도                   CORPORATE 관계 + observations.equity_stake
"""
import re

INK, MUTE, LINE = '#1C2733', '#6B7785', '#C9D1DA'
TG, TG_SOFT = '#0E6B66', '#D6ECEA'
KR, KR_SOFT = '#B4620A', '#F6E3C8'
JP, JP_SOFT = '#9B1C3A', '#F3D5DC'
CUST, CUST_SOFT = '#31507A', '#D9E2EF'
SUP = '#8A96A3'


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fmt(v):
    if v is None:
        return ''
    return ('%g' % v) if isinstance(v, (int, float)) else str(v)


def cut(s, n):
    s = s or ''
    return s if len(s) <= n else s[:n - 1] + u'…'


def share_txt(sh):
    u"""비중 글자 — percent 면 %, 아니면 값과 단위 그대로(엔비디아 매출 갈래는 USD M 로 적혀 있다)."""
    if not sh:
        return ''
    v = sh.get('value')
    unit = sh.get('unit') or 'percent'
    if unit in ('percent', '%'):
        if v is None:
            return u'%s~%s%%' % (fmt(sh.get('value_low')), fmt(sh.get('value_high')))
        return u'%s%%' % fmt(v)
    if v is None:
        v = sh.get('value_high')
    if isinstance(v, (int, float)):
        return u'{:,.0f} {}'.format(v, unit) if v >= 100 else u'%s %s' % (fmt(v), unit)
    return u'%s %s' % (fmt(v), unit)


def share_pct(sh):
    u"""막대 길이로 쓸 수 있는 값(percent 만). 아니면 None."""
    if not sh or (sh.get('unit') or 'percent') not in ('percent', '%'):
        return None
    v = sh.get('value')
    if v is None:
        v = sh.get('value_high')
    return v


def latest_share(x):
    best = None
    for sh in x.get('shares') or []:
        if sh.get('value') is None and sh.get('value_low') is None:
            continue
        k = (sh.get('period_end') or sh.get('as_of_date') or '', )
        if best is None or k > (best.get('period_end') or best.get('as_of_date') or '',):
            best = sh
    return best


def _box(x, y, w, h, fill, stroke, lines, dash=False):
    u"""상자 하나 — lines 는 [(글, 색, 굵기)]. 첫 줄은 이름, 둘째 줄은 잿빛 보조 설명."""
    out = [u'<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>'
           % (x, y, w, h, fill, stroke, ' stroke-dasharray="4 3"' if dash else '')]
    ty = y + 17
    for txt, col, wt in lines:
        out.append(u'<text x="%d" y="%d" fill="%s"%s>%s</text>'
                   % (x + 10, ty, col, ' font-weight="500"' if wt else '', esc(txt)))
        ty += 16
    return u''.join(out)


def tree_svg(root, branches, aria):
    u"""왼쪽 뿌리 → 가운데 갈래 → 오른쪽 잎. TSMC 2절 드라이버 트리와 같은 꼴.

    root = (큰 글, 작은 글); branches = [(이름, 보조, [(잎 이름, 잎 보조, style)])], style 은
    'tg'|'kr'|'jp'|'cust'|'sup'|'dash'. 잎이 없는 갈래는 갈래 상자만 선다."""
    RX, RW, RH = 10, 150, 70
    BX, BW, BH = 240, 200, 50
    LX, LW, LH = 520, 250, 34
    GAP_B, GAP_L = 14, 8
    rows = []
    y = 20
    for name, sub, leaves in branches:
        n = max(1, len(leaves))
        hgt = max(BH, n * LH + (n - 1) * GAP_L)
        rows.append((y, hgt, name, sub, leaves))
        y += hgt + GAP_B
    H = y + 10
    W = 960
    out = [u'<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, H, esc(aria))]
    # 선
    ry = H / 2.0
    paths = []
    for y0, hgt, name, sub, leaves in rows:
        by = y0 + hgt / 2.0
        paths.append(u'M%d %.0fH%dV%.0fH%d' % (RX + RW, ry, BX - 25, by, BX))
        for i, lf in enumerate(leaves):
            ly = y0 + i * (LH + GAP_L) + LH / 2.0
            paths.append(u'M%d %.0fH%dV%.0fH%d' % (BX + BW, by, LX - 25, ly, LX))
    out.append(u'<g stroke="%s" stroke-width="1.5" fill="none"><path d="%s"/></g>' % (LINE, u''.join(paths)))
    out.append(u'<g font-size="12">')
    # 뿌리
    out.append(u'<rect x="%d" y="%.0f" width="%d" height="%d" rx="4" fill="%s"/>' % (RX, ry - RH / 2.0, RW, RH, TG))
    out.append(u'<text x="%d" y="%.0f" text-anchor="middle" fill="#fff" font-size="14" font-weight="600">%s</text>'
               % (RX + RW / 2, ry - 6, esc(cut(root[0], 14))))
    out.append(u'<text x="%d" y="%.0f" text-anchor="middle" fill="#fff">%s</text>'
               % (RX + RW / 2, ry + 14, esc(cut(root[1], 16))))
    STY = {'tg': ('#fff', TG), 'kr': (KR_SOFT, KR), 'jp': (JP_SOFT, JP), 'cust': (CUST_SOFT, CUST),
           'sup': ('#fff', SUP), 'dash': ('#fff', SUP)}
    for y0, hgt, name, sub, leaves in rows:
        by = y0 + hgt / 2.0 - BH / 2.0
        out.append(_box(BX, by, BW, BH, TG_SOFT, TG, [(cut(name, 16), INK, True), (cut(sub, 20), MUTE, False)]))
        for i, (ln, ls, st) in enumerate(leaves):
            ly = y0 + i * (LH + GAP_L)
            fill, stroke = STY.get(st, STY['sup'])
            out.append(u'<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>'
                       % (LX, ly, LW, LH, fill, stroke, ' stroke-dasharray="4 3"' if st == 'dash' else ''))
            out.append(u'<text x="%d" y="%d" fill="%s">%s</text>' % (LX + 10, ly + 15, INK, esc(cut(ln, 19))))
            if ls:
                out.append(u'<text x="%d" y="%d" fill="%s" font-size="11">%s</text>' % (LX + 10, ly + 29, MUTE, esc(cut(ls, 22))))
    out.append(u'</g></svg>')
    return u''.join(out)


def _crit_style(c, r):
    if r.get('capacity_criticality') in ('HIGH', 'VERY_HIGH'):
        return 'jp'
    if (c.ents.get(r['source_entity']) or {}).get('country') == u'한국':
        return 'kr'
    if r.get('source_tier') == 'INTERMEDIARY':
        return 'dash'
    return 'sup'


def _obs_by_rel(c, metric):
    out = {}
    for o in c.obs:
        if o.get('metric') != metric or o.get('value') is None:
            continue
        k = o.get('relationship_id')
        if k not in out or (o.get('period_end') or '') > (out[k].get('period_end') or ''):
            out[k] = o
    return out


def sec_revtree(c, n):
    kinds = [x for x in (c.cls.get('revenue_types') or []) if not x.get('unallocated')]
    items = []
    cust_share = _obs_by_rel(c, 'customer_revenue_share')
    for x in kinds:
        sh = latest_share(x)
        rels = [r for r in c.rels if r.get('lane') == 'DOWNSTREAM' and r.get('source_entity') == c.focal
                and x['id'] in (r.get('revenue_type_ids') or [])]
        if not sh and not rels:
            continue
        leaves = []
        for r in rels[:3]:
            o = cust_share.get(r['id'])
            sub = (u'%s · %s' % (share_txt(o), o.get('period') or '')) if o else (r.get('target_role') or '')
            leaves.append((c.nm(r['target_entity']), sub, 'cust'))
        if len(rels) > 3:
            leaves.append((u'그 밖 %d곳' % (len(rels) - 3), u'', 'dash'))
        w = share_pct(sh)
        items.append((w if w is not None else -1, x.get('label'),
                      (u'%s · %s' % (share_txt(sh), sh.get('period') or '')) if sh else u'비중 미공시', leaves, sh))
    if not items:
        return ''
    items.sort(key=lambda t: -t[0])
    items = items[:7]
    dens = [t[4].get('denominator') for t in items if t[4] and t[4].get('denominator')]
    pers = sorted(set(t[4].get('period') for t in items if t[4] and t[4].get('period')))
    root = (c.nm(c.focal), u'매출')
    svg = tree_svg(root, [(t[1], t[2], t[3]) for t in items], u'%s 매출 트리' % c.label)
    unit_note = u'' if all(share_pct(t[4]) is not None for t in items if t[4]) else u' 비중이 아니라 금액으로 적힌 갈래는 단위를 그대로 둔다.'
    return u'''  <section>
    <h2>%d. 매출 트리<small>%s</small></h2>
    <p class="note">왼쪽 매출에서 오른쪽 갈래와 그 갈래를 사는 고객으로. 갈래 상자의 값은 그 갈래가 분모(%s)에서 차지하는 비중이고 갈래마다 가장 최근 값이다. 고객 상자의 값은 고객별 매출 비중 관측. 남색은 고객, 점선은 이름을 안 밝힌 나머지.%s</p>
    <div class="sv">%s</div>
  </section>
''' % (n, esc(u', '.join(pers) or u'시점 갈래마다'), esc(u' / '.join(sorted(set(dens))) or u'미상'), unit_note, svg)


def sec_suptree(c, n):
    kinds = [x for x in (c.cls.get('supply_sources') or []) if not x.get('unallocated')]
    items = []
    for x in kinds:
        sh = latest_share(x)
        rels = [r for r in c.rels if x['id'] in (r.get('supply_source_ids') or []) and r.get('source_entity') != c.focal]
        if not sh and not rels:
            continue
        # 병목·한국 회사가 앞에 오도록
        order = {'jp': 0, 'kr': 1, 'sup': 2, 'dash': 3}
        rels.sort(key=lambda r: (order[_crit_style(c, r)], c.nm(r['source_entity'])))
        seen, leaves = set(), []
        for r in rels:
            nm = c.nm(r['source_entity'])
            if nm in seen:
                continue
            seen.add(nm)
            if len(leaves) >= 3:
                continue
            sub = r.get('component') or r.get('source_role') or ''
            leaves.append((nm, sub, _crit_style(c, r)))
        if len(seen) > 3:
            leaves.append((u'그 밖 %d곳' % (len(seen) - 3), u'', 'dash'))
        items.append((len(seen), x.get('label'),
                      (u'%s · %s' % (share_txt(sh), sh.get('period') or '')) if sh else (u'공급사 %d곳' % len(seen)), leaves, sh))
    if not items:
        return ''
    items.sort(key=lambda t: -t[0])
    items = items[:7]
    dens = sorted(set(t[4].get('denominator') for t in items if t[4] and t[4].get('denominator')))
    svg = tree_svg((c.nm(c.focal), u'앞단'), [(t[1], t[2], t[3]) for t in items], u'%s 공급원 트리' % c.label)
    dn = (u' 갈래 상자의 값은 분모(%s)에서의 비중.' % esc(u' / '.join(dens))) if dens else u''
    return u'''  <section>
    <h2>%d. 공급원 트리<small>갈래마다 공급사</small></h2>
    <p class="note">왼쪽 회사에서 오른쪽 공급 갈래와 그 갈래를 대는 공급사로. 진홍은 공급 여력 등급이 HIGH 이상인 병목, 주황은 한국 회사, 점선은 중개·유통과 이름을 안 밝힌 나머지.%s 관계에 갈래가 안 적힌 공급사는 1절 지도에만 선다.</p>
    <div class="sv">%s</div>
  </section>
''' % (n, dn, svg)


CRIT_KO = {'VERY_HIGH': (u'매우 높음', 'h1'), 'HIGH': (u'높음', 'h3'), 'MEDIUM': (u'중간', 'h5')}
IMP_KO = {'HIGH': (u'높음', 'h2'), 'MEDIUM': (u'중간', 'h3'), 'LOW': (u'낮음', 'h5')}
EV_KO = {'CONFIRMED': u'공시로 확인', 'ESTIMATED': u'추정', 'INFERRED': u'정황 추론',
         'UNDISCLOSED': u'비공개', 'HISTORICAL_CURRENT_UNKNOWN': u'과거 관측·현재 미상'}


def sec_heat(c, n):
    rows = [r for r in c.rels if r.get('capacity_criticality') in CRIT_KO]
    if not rows:
        return ''
    order = {'VERY_HIGH': 0, 'HIGH': 1, 'MEDIUM': 2}
    rows.sort(key=lambda r: (order[r['capacity_criticality']], c.nm(r['source_entity'])))
    ss = dict((x['id'], x.get('label')) for x in c.cls.get('supply_sources') or [])
    tr = []
    for r in rows:
        ko, hcls = CRIT_KO[r['capacity_criticality']]
        imp = IMP_KO.get(r.get('economic_importance'))
        item = u'·'.join(ss.get(i, i) for i in (r.get('supply_source_ids') or [])) or (r.get('component') or '')
        tr.append(u'<tr><td class="nw">%s</td><td>%s</td><td>%s</td><td class="c %s">%s</td><td class="c %s">%s</td><td><span class="ev%s">%s</span></td></tr>' % (
            esc(c.nm(r['source_entity'])), esc(c.nm(r['target_entity'])), esc(item), hcls, ko,
            imp[1] if imp else '', imp[0] if imp else u'—',
            ' c' if r.get('evidence_level') == 'CONFIRMED' else '', esc(EV_KO.get(r.get('evidence_level'), ''))))
    return u'''  <section>
    <h2>%d. 병목 히트맵<small>공급 여력 등급이 적힌 줄</small></h2>
    <p class="note">관계 데이터에 공급 여력 등급(capacity_criticality)이 적힌 공급 줄 %d개. 등급이 높을수록 짙다. 경제 중요도는 적힌 줄에만 칠하고, 1절 지도의 진홍 상자와 같은 줄이다.</p>
    <div class="tw"><table class="heat"><tr><th>공급사</th><th>받는 쪽</th><th>품목</th><th>공급 여력</th><th>경제 중요도</th><th>근거</th></tr>%s</table></div>
  </section>
''' % (n, len(rows), u''.join(tr))


def sec_custbars(c, n):
    rid = dict((r['id'], r) for r in c.rels)
    best = {}
    for o in c.obs:
        r = rid.get(o.get('relationship_id'))
        if not r or r.get('lane') != 'DOWNSTREAM' or r.get('source_entity') != c.focal:
            continue
        if not re.search(r'share$', o.get('metric') or '') or o.get('unit') not in ('percent', '%'):
            continue
        if o.get('value') is None and o.get('value_high') is None:
            continue
        k = r['target_entity']
        if k not in best or (o.get('period_end') or '') > (best[k].get('period_end') or ''):
            best[k] = o
    if not best:
        return ''
    items = []
    for k, o in best.items():
        v = o.get('value')
        w = v if v is not None else o.get('value_high')
        items.append((w, c.nm(k), share_txt(o), o.get('period') or '', o.get('denominator') or ''))
    items.sort(key=lambda t: -(t[0] or 0))
    items = items[:12]
    dens = sorted(set(t[4] for t in items if t[4]))
    W, LW, RH, PAD = 960, 260, 30, 10
    H = PAD * 2 + RH * len(items)
    scale = (W - LW - 120) / 100.0
    out = [u'<svg viewBox="0 0 %d %d" role="img" aria-label="%s 고객 집중도">' % (W, H, esc(c.label)), u'<g font-size="12">']
    for i, (v, nm, txt, per, den) in enumerate(items):
        y = PAD + i * RH
        bw = max(1.0, min(100.0, v or 0) * scale)
        out.append(u'<text x="%d" y="%d" text-anchor="end" fill="%s">%s</text>' % (LW - 10, y + 19, INK, esc(cut(nm, 22))))
        out.append(u'<rect x="%d" y="%d" width="%.1f" height="18" rx="2" fill="%s"/>' % (LW, y + 6, bw, CUST))
        out.append(u'<text x="%.1f" y="%d" fill="%s">%s · %s</text>' % (LW + bw + 8, y + 19, MUTE, esc(txt), esc(per)))
    out.append(u'</g></svg>')
    return u'''  <section>
    <h2>%d. 고객 집중도<small>고객마다 가장 최근 비중</small></h2>
    <p class="note">회사에서 나가는 줄에 붙은 매출 비중 관측 가운데 고객마다 가장 최근 값. 분모: %s. 익명 고객은 공시가 이름을 안 밝힌 자리이고, 전방시장 갈래가 섞여 있으면 한 줄에서 더하지 않는다.</p>
    <div class="sv">%s</div>
  </section>
''' % (n, esc(u' / '.join(dens) or u'미상'), u''.join(out))


def _year(p):
    m = re.search(r'(20\d{2})', p or '')
    return int(m.group(1)) if m else None


def sec_timeline(c, n):
    up = set(r['source_entity'] for r in c.rels if r.get('lane') not in ('DOWNSTREAM', 'CORPORATE') and r.get('target_entity') == c.focal)
    up |= set(r['source_entity'] for r in c.rels if r.get('lane') not in ('DOWNSTREAM', 'CORPORATE'))
    down = set(r['target_entity'] for r in c.rels if r.get('lane') == 'DOWNSTREAM')
    years = {}
    for x in c.claims:
        y = _year(x.get('period'))
        if not y or not x.get('statement'):
            continue
        s = x.get('subject')
        grp = u'회사' if s == c.focal else (u'뒷단' if s in down else (u'앞단' if s in up else u'그 밖'))
        years.setdefault(y, {}).setdefault(grp, []).append(x)
    if not years:
        return ''
    ys = [y for y in sorted(years) if y >= 2023] or sorted(years)[-3:]
    blocks = []
    for y in ys:
        rows = []
        for grp in (u'회사', u'앞단', u'뒷단', u'그 밖'):
            xs = years[y].get(grp) or []
            if not xs:
                continue
            xs.sort(key=lambda x: (x.get('period') or ''), reverse=True)
            def line(x):
                per = x.get('period') or ''
                if per and x['statement'].startswith(per):
                    return esc(x['statement'])  # 주장이 기간으로 시작하면 두 번 안 적는다
                return u'%s %s' % (esc(per), esc(x['statement']))
            txt = u' '.join(line(x) for x in xs[:2])
            if len(xs) > 2:
                txt += u' <span style="color:%s">외 %d건</span>' % (MUTE, len(xs) - 2)
            rows.append(u'<span>%s</span><span>%s</span>' % (grp, txt))
        blocks.append(u'<div class="yr"><b>%d</b><div class="row">%s</div></div>' % (y, u''.join(rows)))
    return u'''  <section>
    <h2>%d. 시간축 %d~%d</h2>
    <p class="note">주장 데이터의 기간을 해로 묶었다(2023년 이후만). 회사 줄은 회사가 주어인 주장, 앞단은 공급 쪽, 뒷단은 고객 쪽. 해마다 최근 두 건만 적고 나머지는 건수로 센다. 전망(가이던스)은 그 해에 선다.</p>
    <div class="tl">%s</div>
  </section>
''' % (n, ys[0], ys[-1], u''.join(blocks))


REL_KO = {'INVESTS_IN': u'지분 투자', 'SUBSIDIARY_OF': u'자회사', 'OPERATES_THROUGH': u'운영 자회사',
          'CORPORATE_CONTROL': u'지배', 'EXECUTES_THROUGH_SUBSIDIARY': u'실행 자회사',
          'HOLDS_PROJECT': u'프로젝트 보유', 'FINANCES': u'금융', 'JV_ASSEMBLY': u'합작',
          'INTERNAL_MATERIAL_SUPPLY': u'내부 소재 공급', 'INTRAGROUP_SUPPLY': u'그룹 내 공급',
          'MANUFACTURES': u'제조 자회사', 'PROCESSING': u'가공 자회사', 'SUPPLIES': u'공급',
          'STRATEGIC_PARTNERSHIP': u'전략 협력', 'INVESTS': u'투자'}


def sec_equity_map(c, n):
    rows = [r for r in c.rels if r.get('lane') == 'CORPORATE']
    if not rows:
        return ''
    stake = _obs_by_rel(c, 'equity_stake')
    left, right, other = [], [], []
    for r in rows:
        o = stake.get(r['id'])
        pct = (u' %s' % share_txt(o)) if o else u''
        rel = REL_KO.get(r.get('relationship_type'), r.get('relationship_type') or '')
        note = (r.get('notes') or '').split(u'(')[0].split(u'. ')[0]
        if r['source_entity'] == c.focal:
            left.append((c.nm(r['target_entity']) + pct, u'%s · %s' % (rel, note) if note else rel, r))
        elif r['target_entity'] == c.focal:
            right.append((c.nm(r['source_entity']) + pct, u'%s · %s' % (rel, note) if note else rel, r))
        else:
            other.append((u'%s → %s' % (c.nm(r['source_entity']), c.nm(r['target_entity'])), rel + (u' · ' + note if note else u''), r))
    L, R, O = left[:5], right[:5], other[:3]
    rows_n = max(len(L), len(R), 1)
    BW, BH, GAP = 250, 42, 14
    top = 30
    H = top + rows_n * (BH + GAP) + (60 if O else 0) + (30 if len(left) > 5 or len(right) > 5 or len(other) > 3 else 10)
    cy = top + (rows_n * (BH + GAP) - GAP) / 2.0
    out = [u'<svg viewBox="0 0 960 %d" role="img" aria-label="%s 지분 지도">' % (H, esc(c.label)), u'<g font-size="12" fill="%s">' % INK]
    out.append(u'<rect x="400" y="%.0f" width="160" height="70" rx="4" fill="%s"/><text x="480" y="%.0f" text-anchor="middle" fill="#fff" font-size="16" font-weight="600">%s</text>'
               % (cy - 35, TG, cy + 6, esc(cut(c.nm(c.focal), 10))))
    paths = []
    for i in range(len(L)):
        y = top + i * (BH + GAP) + BH / 2.0
        paths.append(u'M400 %.0fC330 %.0f 330 %.0f %d %.0f' % (cy, cy, y, 60 + BW, y))
    for i in range(len(R)):
        y = top + i * (BH + GAP) + BH / 2.0
        paths.append(u'M560 %.0fC630 %.0f 630 %.0f 700 %.0f' % (cy, cy, y, y))
    out.append(u'<g stroke="%s" stroke-width="1.5" fill="none"><path d="%s"/></g>' % (TG, u''.join(paths)))

    def style(r, ent):
        e = c.ents.get(ent) or {}
        if r.get('capacity_criticality') in ('HIGH', 'VERY_HIGH'):
            return JP_SOFT, JP
        if e.get('country') == u'한국':
            return KR_SOFT, KR
        return TG_SOFT, TG
    for i, (nm, sub, r) in enumerate(L):
        y = top + i * (BH + GAP)
        f, s = style(r, r['target_entity'])
        out.append(_box(60, y, BW, BH, f, s, [(cut(nm, 19), INK, False), (cut(sub, 22), MUTE, False)]))
    for i, (nm, sub, r) in enumerate(R):
        y = top + i * (BH + GAP)
        f, s = style(r, r['source_entity'])
        out.append(_box(700, y, BW, BH, f, s, [(cut(nm, 19), INK, False), (cut(sub, 22), MUTE, False)]))
    if O:
        oy = top + rows_n * (BH + GAP) + 6
        for i, (nm, sub, r) in enumerate(O):
            out.append(_box(60 + i * 300, oy, 280, BH, '#fff', SUP, [(cut(nm, 22), INK, False), (cut(sub, 25), MUTE, False)]))
    more = []
    if len(left) > 5:
        more.append(u'회사가 쥔 지분 %d건 더' % (len(left) - 5))
    if len(right) > 5:
        more.append(u'회사를 쥔 쪽 %d건 더' % (len(right) - 5))
    if len(other) > 3:
        more.append(u'그 밖의 구조 선 %d건 더' % (len(other) - 3))
    out.append(u'<text x="480" y="%d" text-anchor="middle" fill="%s" font-size="11">왼쪽은 회사가 쥔 지분·자회사, 오른쪽은 회사에 들어온 투자·모회사·협력. 아래는 사슬 안 다른 회사끼리의 구조 선.%s</text>'
               % (H - 8, MUTE, (u' ' + u' · '.join(more)) if more else u''))
    out.append(u'</g></svg>')
    return u'''  <section>
    <h2>%d. 지분·소유<small>지분·자회사·협력 선</small></h2>
    <p class="note">기업 구조 선 %d개. 지분율은 관측이 붙은 줄에만 적고, 없는 줄은 관계 이름만 남긴다. 주황은 한국 회사. 탐색기는 이 선을 따라가지 않고 서랍에만 보인다.</p>
    <div class="sv">%s</div>
  </section>
''' % (n, len(rows), u''.join(out))


SECTIONS = (sec_revtree, sec_suptree, sec_heat, sec_custbars, sec_timeline, sec_equity_map)


# ── 2026-09-13 통일 골격 — 여섯 장이 같은 열한 절 ───────────────────────────────
# 1 전체 지도  2 매출 드라이버 트리  3 단위경제  4 마진 풀  5 병목 리스크 히트맵  6 시나리오 민감도
# 7 시간축  8 거래 위에 소유를 겹치기  9 고객 집중도  10 핵심 수치  11 출처
# 3·4·6 은 조사 보고서 값(chains/<id>/report_figs.json)에서, 없으면 자리만 지킨다(데이터 없음 한 줄).
import io as _io
import json as _json
import os as _os


def load_figs(c):
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'data', 'valuechain', 'chains', c.id, 'report_figs.json')
    if not _os.path.exists(p):
        return {}
    with _io.open(p, encoding='utf-8') as f:
        return _json.load(f) or {}


def sec_empty(n, title, small, why):
    return (u'  <section>\n    <h2>%d. %s<small>%s</small></h2>\n    <p class="note">%s</p>\n  </section>\n'
            % (n, esc(title), esc(small), esc(why)))


def _retitle(html, old, new):
    u"""이미 세운 절의 제목만 TSMC 장의 이름으로 바꾼다."""
    return html.replace(u'. %s<small>' % old, u'. %s<small>' % new, 1) if html else html


def _sec(n, title, small, note, body):
    return (u'  <section>\n    <h2>%d. %s<small>%s</small></h2>\n    <p class="note">%s</p>\n    %s\n  </section>\n'
            % (n, esc(title), esc(small), note, body))


# ── 1 전체 지도 — TSMC 손 그림과 같은 다섯 칸(Tier 2 · Tier 1 · 회사 · 고객 · 최종 수요) ────
COLS = {'t2': (10, 180), 't1': (235, 190), 'me': (470, 110), 'cust': (620, 150), 'fin': (800, 150)}
BH_MAP, PITCH = 34, 44


def _style_of(c, ents_ids, rels):
    if any(r.get('capacity_criticality') in ('HIGH', 'VERY_HIGH') for r in rels):
        return JP_SOFT, JP, False
    if any((c.ents.get(e) or {}).get('country') == u'한국' for e in ents_ids):
        return KR_SOFT, KR, False
    if rels and all(r.get('source_tier') == 'INTERMEDIARY' for r in rels):
        return '#fff', SUP, True
    return '#fff', LINE, False


def sec_map_data(c, n):
    me = c.nm(c.focal)
    # 앞단 — 공급 줄. 그룹 안 공장·가공 자회사(태양유전)는 CORPORATE 선이지만 물건이 들어오는 줄이라 앞단에 세운다
    IN_TYPES = ('INTERNAL_MATERIAL_SUPPLY', 'PROCESSING', 'MANUFACTURES', 'INTRAGROUP_SUPPLY', 'JV_ASSEMBLY', 'CONTRACT_MANUFACTURES')
    up = [r for r in c.rels if r.get('target_entity') == c.focal and (r.get('lane') not in ('DOWNSTREAM', 'CORPORATE')
          or (r.get('lane') == 'CORPORATE' and r.get('relationship_type') in IN_TYPES))]
    ss = dict((x['id'], x.get('label')) for x in c.cls.get('supply_sources') or [])
    groups = {}
    for r in up:
        k = ss.get((r.get('supply_source_ids') or [None])[0]) or r.get('subsystem') or r.get('component') or u'그 밖'
        groups.setdefault(k, []).append(r)
    t1_boxes = []
    for k, rs in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:10]:
        ents = []
        for r in rs:
            if r['source_entity'] not in ents:
                ents.append(r['source_entity'])
        t1_boxes.append(([c.nm(e) for e in ents], k, ents, rs))
    t1_of = {}
    for i, b in enumerate(t1_boxes):
        for e in b[2]:
            t1_of.setdefault(e, i)
    t2 = {}
    for r in c.rels:
        if r.get('target_entity') in t1_of and r.get('source_entity') != c.focal and r.get('lane') not in ('DOWNSTREAM', 'CORPORATE'):
            t2.setdefault(r['target_entity'], []).append(r)
    t2_boxes = []
    for tgt, rs in sorted(t2.items(), key=lambda kv: -len(kv[1]))[:6]:
        ents = []
        for r in rs:
            if r['source_entity'] not in ents:
                ents.append(r['source_entity'])
        t2_boxes.append(([c.nm(e) for e in ents], u'→ %s' % c.nm(tgt), ents, rs, t1_of[tgt]))
    share = _obs_by_rel(c, 'customer_revenue_share')
    seen = {}
    for r in c.rels:
        if r.get('lane') != 'DOWNSTREAM' or r.get('source_entity') != c.focal:
            continue
        e = r['target_entity']
        o = share.get(r['id'])
        v = o.get('value') if o else None
        if e not in seen or (v is not None and (seen[e][1] is None or v > seen[e][1])):
            seen[e] = (r, v, o)
    # 고객 줄이 없으면(엔비디아) 회사가 맺은 협력·투자·플랫폼 노출 선을 뒷단 자리에 세운다 — 관계 이름을 보조 줄에 적는다
    OUT_TYPES = {'STRATEGIC_PARTNERSHIP': u'전략 협력', 'PLATFORM_EXPOSURE': u'플랫폼 노출', 'INVESTS_IN': u'지분 투자'}
    for r in c.rels:
        if r.get('lane') == 'CORPORATE' and r.get('source_entity') == c.focal and r.get('relationship_type') in OUT_TYPES and r['target_entity'] not in seen:
            seen[r['target_entity']] = (dict(r, target_role=OUT_TYPES[r['relationship_type']]), None, None)
    cust = sorted(seen.values(), key=lambda t: -(t[1] if t[1] is not None else -1))[:7]
    cust_idx = dict((t[0]['target_entity'], i) for i, t in enumerate(cust))
    fin, fseen = [], set()
    for r in c.rels:
        if r.get('lane') == 'DOWNSTREAM' and r.get('source_entity') in cust_idx and r.get('target_entity') != c.focal:
            e = r['target_entity']
            if e in fseen or e in cust_idx:
                continue
            fseen.add(e)
            fin.append((e, cust_idx[r['source_entity']]))
    fin = fin[:6]
    if not (t1_boxes or cust):
        return sec_empty(n, u'전체 지도', u'앞단 → %s → 뒷단' % me, u'이 사슬에는 회사로 들어오거나 나가는 관계 줄이 없다.')
    rows = max(len(t1_boxes), len(t2_boxes), len(cust), len(fin), 5)
    H = 40 + rows * PITCH + 40
    out = [u'<svg viewBox="0 0 960 %d" role="img" aria-label="%s 밸류체인 지도">' % (H, esc(me))]
    out.append(u'<defs><marker id="m-%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="%s"/></marker></defs>' % (c.id, SUP))
    out.append(u'<g font-size="13" fill="%s"><text x="10" y="22">Tier 2 원료·부품</text><text x="235" y="22">Tier 1 소재·장비·유통</text><text x="620" y="22">고객</text><text x="800" y="22">최종 수요</text></g>' % MUTE)

    def box(col, i, fill, stroke, dashed, l1, l2):
        x, w = COLS[col]
        y = 40 + i * PITCH
        h = 40 if l2 else BH_MAP
        s = [u'<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>' % (x, y, w, h, fill, stroke, ' stroke-dasharray="4 3"' if dashed else '')]
        if l2:
            s.append(u'<text x="%d" y="%d" font-size="12" fill="%s">%s</text><text x="%d" y="%d" font-size="11" fill="%s">%s</text>' % (x + 10, y + 16, INK, esc(l1), x + 10, y + 31, MUTE, esc(l2)))
        else:
            s.append(u'<text x="%d" y="%d" font-size="12" fill="%s">%s</text>' % (x + 10, y + 22, INK, esc(l1)))
        return u''.join(s), (x, y, w, h)
    geo = {}
    for i, (names, lab, ents, rs) in enumerate(t1_boxes):
        f, s, d = _style_of(c, ents, rs)
        h, g = box('t1', i, f, s, d, cut(u' · '.join(names), 17), cut(lab, 20))
        out.append(h)
        geo[('t1', i)] = g
    for i, (names, lab, ents, rs, ti) in enumerate(t2_boxes):
        f, s, d = _style_of(c, ents, rs)
        h, g = box('t2', i, f, s, d, cut(u' · '.join(names), 16), cut(lab, 18))
        out.append(h)
        geo[('t2', i)] = g
    for i, (r, v, o) in enumerate(cust):
        sub = (u'%s · %s' % (share_txt(o), o.get('period') or '')) if o else (r.get('target_role') or '')
        h, g = box('cust', i, CUST_SOFT if v is not None else '#fff', CUST, False, cut(c.nm(r['target_entity']), 13), cut(sub, 16))
        out.append(h)
        geo[('cust', i)] = g
    for i, (e, ci) in enumerate(fin):
        h, g = box('fin', i, '#fff', LINE, False, cut(c.nm(e), 13), cut(u'← %s' % c.nm(cust[ci][0]['target_entity']), 16))
        out.append(h)
        geo[('fin', i)] = g
    mx, mw = COLS['me']
    mh = max(200, min(H - 80, rows * PITCH - 10))
    my = 40 + (rows * PITCH - 10 - mh) / 2.0
    out.append(u'<rect x="%d" y="%.0f" width="%d" height="%d" rx="4" fill="%s"/>' % (mx, my, mw, mh, TG))
    lines = [(cut(me, 8), 20, True)]
    rev = (c.ents.get(c.focal) or {}).get('revenue') or ''
    if rev:
        lines.append((cut(rev.split(u' 매출 ')[-1] if u' 매출 ' in rev else rev, 12), 12, False))
    kinds = [(share_pct(latest_share(x)), x.get('label'), latest_share(x)) for x in (c.cls.get('revenue_types') or []) if not x.get('unallocated')]
    kinds = [k for k in kinds if k[0] is not None]
    if kinds:
        k = max(kinds, key=lambda t: t[0])
        lines.append((cut(u'%s %s' % (k[1].replace(u' 매출', u''), share_txt(k[2])), 12), 11, False))
    lines.append((u'관계 %d줄' % len(c.rels), 11, False))
    ty = my + mh / 2.0 - 8 * len(lines)
    for txt, fs, bold in lines:
        out.append(u'<text x="%d" y="%.0f" text-anchor="middle" fill="#fff" font-size="%d"%s>%s</text>' % (mx + mw / 2, ty, fs, ' font-weight="600"' if bold else ' opacity=".9"', esc(txt)))
        ty += fs + 8
    paths = []

    def bez(x0, y0, x1, y1):
        mid = (x0 + x1) / 2.0
        paths.append(u'M%.0f %.0fC%.0f %.0f %.0f %.0f %.0f %.0f' % (x0, y0, mid, y0, mid, y1, x1, y1))
    for i, b in enumerate(t2_boxes):
        a, t = geo[('t2', i)], geo[('t1', b[4])]
        bez(a[0] + a[2], a[1] + a[3] / 2.0, t[0], t[1] + t[3] / 2.0)
    for i in range(len(t1_boxes)):
        g = geo[('t1', i)]
        bez(g[0] + g[2], g[1] + g[3] / 2.0, mx, my + 20 + (mh - 40) * (i + 0.5) / max(1, len(t1_boxes)))
    for i in range(len(cust)):
        g = geo[('cust', i)]
        bez(mx + mw, my + 20 + (mh - 40) * (i + 0.5) / max(1, len(cust)), g[0], g[1] + g[3] / 2.0)
    for i, (e, ci) in enumerate(fin):
        a, t = geo[('cust', ci)], geo[('fin', i)]
        bez(a[0] + a[2], a[1] + a[3] / 2.0, t[0], t[1] + t[3] / 2.0)
    out.append(u'<g stroke="%s" stroke-width="1.3" fill="none" marker-end="url(#m-%s)"><path d="%s"/></g>' % (SUP, c.id, u''.join(paths)))
    out.append(u'<text x="10" y="%d" font-size="11" fill="%s">선 굵기에는 뜻이 없다(금액 관측이 없다). 점선 상자 = 중개·유통. 상자 안 값은 관측이 붙은 줄만.</text></svg>' % (H - 12, MUTE))
    legend = (u'<div class="legend"><span class="l-tsmc">%s</span><span class="l-kr">한국 회사</span><span class="l-jp">병목(공급 여력 HIGH 이상)</span>'
              u'<span class="l-cust">고객</span><span class="l-sup">그 밖의 공급사</span></div>' % esc(me))
    note = (u'관계 데이터의 줄을 다섯 칸에 세웠다. Tier 1 은 회사에 바로 대는 공급사(갈래로 묶음), Tier 2 는 그 공급사에 대는 곳, '
            u'고객은 회사에서 나가는 줄, 최종 수요는 고객의 고객. 색은 소속: 청록 회사, 주황 한국, 진홍 병목, 남색 고객.')
    return _sec(n, u'전체 지도', u'앞단 → %s → 뒷단' % me, note, u'<div class="sv">%s</div>\n    %s' % (u''.join(out), legend))


# ── 3 단위경제 워터폴 · 4 마진 풀 · 5 점수 히트맵 · 6 토네이도 · 7 시간축 — 보고서 값 ─────
def _money(v):
    return u'{:,.0f}'.format(v) if abs(v) >= 100 else (u'%g' % v)


def _split_small(small, note):
    u"""h2 의 <small> 은 한 토막만. 긴 가정 문장은 폰에서 세 줄로 접혀 제목처럼 읽혀서 note 앞으로 내린다.
    토막은 「, 」(쉼표+공백)로 가른다 — 2,250 같은 숫자 안 쉼표는 안 가른다. 단위 토막이 보통 맨 뒤라 뒤에서부터 고른다."""
    small = (small or '').strip()
    if len(small) <= 24:
        return small, note
    segs = [t.strip() for t in re.split(r',\s+', small) if t.strip()]
    head = u''
    for t in reversed(segs):
        if len(t) <= 24:
            head = t
            break
    rest = u', '.join(t for t in segs if t != head)
    return head, ((rest + u'. ') if rest else u'') + (note or '')

def sec_unit(c, n, fg):
    u = fg.get('unit')
    if not u or not u.get('steps'):
        return sec_empty(n, u'단위경제', u'조사 보고서 없음', u'단위 하나의 판매가와 원가 항목은 조사 보고서가 있어야 선다. 이 회사 보고서에는 아직 그 값이 없다.')
    st, steps, en = u['start'], u['steps'][:7], u['end']
    scale = 180.0 / (float(st['value']) or 1.0)
    cols = 2 + len(steps)
    cw = min(90, int(860 / cols) - 30)
    gap = int((860 - cw * cols) / (cols - 1))
    lim = 13 if cols <= 7 else 11
    out = [u'<svg viewBox="0 0 960 280" role="img" aria-label="%s"><g font-size="12" fill="%s">' % (esc(u.get('title') or ''), INK)]

    def lab(x, i, txt, bold=False):
        # 이웃 라벨과 안 겹치게 두 줄을 번갈아 쓴다
        return u'<text x="%d" y="%d" text-anchor="middle" font-size="11"%s>%s</text>' % (x + cw / 2, 12 if i % 2 == 0 else 28, ' font-weight="600"' if bold else '', esc(cut(txt, lim)))
    x = 40
    out.append(u'<rect x="%d" y="40" width="%d" height="180" fill="%s"/>' % (x, cw, TG) + lab(x, 0, st['label'], True))
    top = 40.0
    for i, s in enumerate(steps, 1):
        x += cw + gap
        h = max(1.0, float(s['value']) * scale)
        out.append(u'<rect x="%d" y="%.0f" width="%d" height="%.0f" fill="%s"/>' % (x, top, cw, h, SUP) + lab(x, i, s['label'])
                   + u'<text x="%d" y="%.0f" text-anchor="middle" fill="%s" font-size="11">−%s</text>' % (x + cw / 2, top + h + 13, MUTE, _money(float(s['value']))))
        top += h
    x += cw + gap
    out.append(u'<rect x="%d" y="%.0f" width="%d" height="%.0f" fill="%s"/>' % (x, top, cw, max(1.0, 220 - top), TG) + lab(x, len(steps) + 1, en['label'], True))
    if en.get('sub'):
        out.append(u'<text x="%d" y="240" text-anchor="middle" fill="%s" font-weight="500">%s</text>' % (x + cw / 2, TG, esc(en['sub'])))
    out.append(u'<line x1="40" y1="220" x2="%d" y2="220" stroke="%s"/>' % (x + cw, LINE))
    if u.get('foot'):
        out.append(u'<text x="40" y="268" fill="%s" font-size="11">%s</text>' % (MUTE, esc(cut(u['foot'], 90))))
    out.append(u'</g></svg>')
    sm, nt = _split_small(u.get('small'), u.get('note'))
    return _sec(n, u.get('title') or u'단위경제', sm, esc(nt), u'<div class="sv">%s</div>' % u''.join(out))


def sec_pool(c, n, fg):
    p = fg.get('pool')
    if not p or not p.get('cost') or not p.get('price'):
        return sec_empty(n, u'마진 풀', u'조사 보고서 없음', u'제품 하나를 따라가며 원가를 쌓고 판매가와 견주는 그림은 조사 보고서가 있어야 선다.')
    scale = 795.0 / (float(p['price']['value']) or 1.0)
    COL = {'self': TG, 'kr': KR, 'jp': JP, 'sup': SUP}
    out = [u'<svg viewBox="0 0 960 190" role="img" aria-label="%s"><g font-size="12">' % esc(p.get('title') or '')]
    out.append(u'<text x="10" y="30" fill="%s">원가 적층 %s</text>' % (MUTE, esc(_money(sum(float(s['value']) for s in p['cost'])))))
    x = 150.0
    last = [0.0, 0.0, 0.0]  # 줄마다 마지막 라벨의 오른끝 — 좁은 칸이 이어져도 라벨이 안 겹친다
    for i, s in enumerate(p['cost'][:7]):
        w = max(1.0, float(s['value']) * scale)
        col = COL.get(s.get('who'), SUP)
        out.append(u'<rect x="%.0f" y="14" width="%.0f" height="24" fill="%s"/>' % (x, w, col))
        txt = cut(s['label'], 16)
        tw = len(txt) * 7.0
        row = i % 3
        cx = max(x + w / 2, last[row] + 8 + tw / 2)
        last[row] = cx + tw / 2
        out.append(u'<text x="%.0f" y="%d" text-anchor="middle" fill="%s" font-size="11">%s</text>' % (cx, (55, 71, 87)[row], col if col != SUP else MUTE, esc(txt)))
        x += w
    cost_w = x - 150.0
    out.append(u'<text x="10" y="120" fill="%s">%s</text>' % (MUTE, esc(p['price']['label'])))
    out.append(u'<rect x="150" y="104" width="%.0f" height="24" fill="%s"/><rect x="%.0f" y="104" width="%.0f" height="24" fill="%s"/>' % (cost_w, LINE, 150 + cost_w, max(1.0, 795 - cost_w), CUST))
    out.append(u'<text x="%.0f" y="146" text-anchor="middle" fill="%s">원가 %s</text>' % (150 + cost_w / 2, MUTE, esc(_money(cost_w / scale))))
    if p.get('owner'):
        ow = 795 - cost_w
        if ow >= 260:
            out.append(u'<text x="%.0f" y="146" text-anchor="middle" fill="%s" font-weight="500">%s</text>' % (150 + cost_w + ow / 2, CUST, esc(cut(p['owner'].get('label') or '', 40))))
        else:
            out.append(u'<text x="945" y="146" text-anchor="end" fill="%s" font-weight="500">%s</text>' % (CUST, esc(cut(p['owner'].get('label') or '', 40))))
    if p.get('foot'):
        out.append(u'<text x="10" y="180" fill="%s" font-size="11">%s</text>' % (MUTE, esc(cut(p['foot'], 100))))
    out.append(u'</g></svg>')
    sm, nt = _split_small(p.get('small'), p.get('note'))
    return _sec(n, p.get('title') or u'마진 풀', sm, esc(nt), u'<div class="sv">%s</div>' % u''.join(out))


def _hc(v):
    return {1: 'h1', 2: 'h2', 3: 'h3', 4: 'h4'}.get(int(v), 'h5')


def _hsum(v):
    return 'h1' if v <= 4 else ('h2' if v == 5 else ('h3' if v <= 7 else ('h4' if v <= 9 else 'h5')))


def sec_heat_report(c, n, fg):
    h = fg.get('heat')
    if not h or not h.get('rows'):
        return None
    tr = []
    for r in h['rows'][:12]:
        s = int(r['sub']) + int(r['lead']) + int(r['geo'])
        tr.append(u'<tr><td>%s</td><td>%s</td><td class="c %s">%d</td><td class="c %s">%d</td><td class="c %s">%d</td><td class="c %s">%d</td></tr>' % (
            esc(r['item']), esc(r.get('company') or ''), _hc(r['sub']), int(r['sub']), _hc(r['lead']), int(r['lead']), _hc(r['geo']), int(r['geo']), _hsum(s), s))
    body = u'<div class="tw"><table class="heat fit"><tr><th>병목</th><th>지배 회사</th><th>대체</th><th>리드타임</th><th>지정학</th><th>합계</th></tr>%s</table></div>' % u''.join(tr)
    return _sec(n, u'병목 리스크 히트맵', u'합계 낮을수록 위험', u'대체 가능성·리드타임·지정학 각 1~5점. ' + esc(h.get('note') or ''), body)


def _report_md(c):
    import glob as _glob
    base = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'data', 'valuechain', 'reports')
    hits = sorted(_glob.glob(_os.path.join(base, c.id + '-*.md')))
    return hits[-1] if hits else None


def _strip_md(t):
    return re.sub(r'\*\*(.*?)\*\*', r'\1', (t or '')).strip()


def parse_scenarios(path):
    u"""조사 보고서의 시나리오 절 표를 읽는다 — (기준선·가정 줄들, [{name, path, profit, spread}]).
    열 이름은 사슬마다 조금씩 다르다(영업이익 / 영업이익 변화 / 영업손익 변화). 시나리오·충격 경로·
    영업…·전파 네 열만 이름으로 집는다."""
    txt = _io.open(path, encoding='utf-8').read()
    m = re.search(r'^## [^\n]*시나리오[^\n]*\n(.*?)(?=^## |\Z)', txt, re.S | re.M)
    if not m:
        return [], []
    body = m.group(1)
    lead, rows, head = [], [], None
    for line in body.split('\n'):
        st = line.strip()
        if not st:
            continue
        if st.startswith('|'):
            cells = [_strip_md(x) for x in st.strip('|').split('|')]
            if head is None:
                head = cells
                continue
            if set(st.replace('|', '').strip()) <= set('-: '):
                continue
            if len(cells) < 3:
                continue
            def col(pred):
                for i, hname in enumerate(head):
                    if pred(hname) and i < len(cells):
                        return cells[i]
                return ''
            rows.append({'name': cells[0], 'path': col(lambda h: u'충격' in h),
                         'profit': col(lambda h: u'영업' in h), 'spread': col(lambda h: u'전파' in h)})
        elif head is None and not st.startswith('#'):
            lead.append(_strip_md(st).lstrip('- '))
        elif head is not None and st.startswith('**') or st.startswith(u'**핵심'):
            break
    return lead, rows


def _num_sign(t):
    u"""영업이익 칸에서 첫 숫자와 부호 — 막대 길이용. 「−$65억 (−10%)」「(603억, −50%)」「+2,250만 달러」."""
    t = t or ''
    m = re.search(r'([−\-+(]?)\s*\$?\s*([\d][\d,]*\.?\d*)', t)
    if not m:
        return 0.0
    v = float(m.group(2).replace(',', '') or 0)
    neg = m.group(1) in (u'−', '-', '(') or t.strip().startswith('(')
    return -v if neg else v


def sec_scenario(c, n, fg):
    u"""6절 시나리오 — 시나리오마다 「왜 이만큼(충격 경로) · 이익이 얼마나(막대) · 어디로 번지나(전파)」.
    토네이도 막대 하나로는 무엇을 가정한 시나리오인지 안 읽혔다(2026-09-13 「시나리오가 뭘 설명하던가」)."""
    rp = _report_md(c)
    lead, rows = parse_scenarios(rp) if rp else ([], [])
    if not rows:
        return sec_empty(n, u'시나리오', u'조사 보고서 없음', u'기준선과 충격별 변화는 조사 보고서의 시나리오 표가 있어야 선다.')
    mags = [abs(_num_sign(r['profit'])) for r in rows]
    mx = max(mags) or 1.0
    items = []
    for r, mag in zip(rows, mags):
        v = _num_sign(r['profit'])
        cls = 'neg' if v < 0 else 'pos'
        items.append(u'<div class="sc"><div class="sc-h"><b>%s</b><span class="sc-v %s">%s</span></div>'
                     u'<div class="sc-bar"><div class="sc-fill %s" style="width:%d%%"></div></div>'
                     u'<p class="sc-p"><b>왜 이만큼.</b> %s</p><p class="sc-p"><b>어디로 번지나.</b> %s</p></div>'
                     % (esc(r['name']), cls, esc(r['profit'] or u'변화 미상'), cls, int(round(100.0 * mag / mx)),
                        esc(r['path'] or u'—'), esc(r['spread'] or u'—')))
    # 머리글은 기준선 한 줄뿐 — 가정·풀이는 조사 보고서 몫이다(「이렇게 주저리 써야 하냐」)
    sents = [x.strip() for x in re.split(r'(?<=\.)\s+', lead[0] if lead else u'') if x.strip()]
    # 숫자가 든 첫 문장 — 「기준선은 5-3절 워터폴의 오른쪽 칸이다」 같은 자리 안내는 건너뛴다
    base = next((x for x in sents if re.search(r'\d', x)), sents[0] if sents else u'').rstrip('.')
    base = re.sub(r'^\s*기준선\s*[:：]\s*', u'기준선 ', base)
    if not base.startswith(u'기준선'):
        base = u'기준선 ' + base
    base = base[:96]
    return _sec(n, u'시나리오 민감도', u'하나만 바뀌면 영업이익이 얼마나', esc(base) or u'기준선은 조사 보고서 시나리오 절.',
                u'<div class="scn">%s</div>' % u''.join(items))


def sec_timeline_report(c, n, fg):
    t = fg.get('timeline')
    if not t or not t.get('years'):
        return None
    blocks = []
    for yb in t['years']:
        rows = u''.join(u'<span>%s</span><span>%s</span>' % (esc(a), esc(b)) for a, b in (yb.get('rows') or []))
        blocks.append(u'<div class="yr"><b>%s</b><div class="row">%s</div></div>' % (esc(str(yb.get('y'))), rows))
    ys = [str(y.get('y')) for y in t['years']]
    last = ys[-1].split(u'~')[-1]
    last = last if len(last) == 4 else ys[-1][:2] + last
    title = u'시간축 %s~%s' % (ys[0][:4], last)
    return (u'  <section>\n    <h2>%d. %s</h2>\n    <p class="note">%s</p>\n    <div class="tl">%s</div>\n  </section>\n'
            % (n, esc(title), esc(t.get('note') or ''), u''.join(blocks)))


def skeleton(c):
    u"""TSMC 가 아닌 사슬의 1~8절 — 항상 여덟 조각, 없는 절은 자리만."""
    fg = load_figs(c)
    me = c.nm(c.focal)
    parts = [sec_map_data(c, 1)]
    h = sec_revtree(c, 2)
    parts.append(_retitle(h, u'매출 트리', u'매출 드라이버 트리') if h else sec_empty(2, u'매출 드라이버 트리', u'데이터 없음', u'매출 갈래 비중이 데이터에 없다.'))
    parts.append(sec_unit(c, 3, fg))
    parts.append(sec_pool(c, 4, fg))
    h = sec_heat_report(c, 5, fg) or sec_heat(c, 5)
    parts.append(_retitle(h, u'병목 히트맵', u'병목 리스크 히트맵') if h else sec_empty(5, u'병목 리스크 히트맵', u'데이터 없음', u'관계 데이터에 공급 여력 등급이 적힌 줄이 없고 조사 보고서 점수도 없다.'))
    parts.append(sec_scenario(c, 6, fg))
    h = sec_timeline_report(c, 7, fg) or sec_timeline(c, 7)
    parts.append(h or sec_empty(7, u'시간축', u'데이터 없음', u'기간이 적힌 주장이 없다.'))
    h = sec_equity_map(c, 8)
    parts.append(_retitle(h, u'지분·소유', u'거래 위에 소유를 겹치기') if h else sec_empty(8, u'거래 위에 소유를 겹치기', u'구조 선 없음', u'이 사슬의 관계 데이터에 지분·자회사·합작 줄이 없다. %s의 지분 구조는 조사 보고서 10절에 적는다.' % me))
    return parts
