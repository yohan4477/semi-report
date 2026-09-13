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
    <h2>%d. 지분·소유<small>거래 위에 소유를 겹치기</small></h2>
    <p class="note">기업 구조 선 %d개. 지분율은 관측이 붙은 줄에만 적고, 없는 줄은 관계 이름만 남긴다. 주황은 한국 회사. 탐색기는 이 선을 따라가지 않고 서랍에만 보인다.</p>
    <div class="sv">%s</div>
  </section>
''' % (n, len(rows), u''.join(out))


SECTIONS = (sec_revtree, sec_suptree, sec_heat, sec_custbars, sec_timeline, sec_equity_map)
