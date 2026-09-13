# -*- coding: utf-8 -*-
u"""밸류체인 보고서 장 — 사슬마다 한 장. 대시보드/<회사> 밸류체인.html

2026-09-13 사용자가 준 TSMC 그림 장(보고서 꼴: 제목·절·짧은 설명·그림)을 틀로 삼는다. 전체 지도
절에는 밸류체인 탐색기(?focal=…&open=*)를 끼우고, 나머지 절은 그 사슬의 데이터(claims·
classifications·relationships·observations·sources)에서 세운다. TSMC 는 1절 전체 지도를 손으로 그린 SVG 대신
탐색기로 이식하고(상자·선은 chains/tsmc 데이터), 2~8절은 받은 그림 그대로, 뒤에 데이터 절을 붙인다.

절(데이터가 없으면 그 절은 안 세운다). TSMC 가 아닌 사슬은 TSMC 2~8절과 같은 꼴(번호 절·짧은 설명·
그림 하나)을 데이터로만 세운다 — vc_figs.py(2026-09-13, 「TSMC 처럼 다른 회사도 포맷을 맞춘다」):
  1 전체 지도(탐색기)  2 매출 트리  3 공급원 트리  4 병목 히트맵  5 고객 집중도  6 시간축
  7 지분·소유(지도)  8 핵심 수치(주장)  9 출처
TSMC 는 1 지도, 2~8 받은 그림, 9 부터 데이터 절(핵심 수치·매출원·공급원·병목·고객·지분·출처).

  PYTHONIOENCODING=utf-8 python scripts/gen_vcreport.py
"""
import glob
import io
import json
import os
import re
import sys

import mistune  # 0.8 — 조사 보고서 마크다운을 장으로

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUTDIR = os.path.join(ROOT, u'대시보드')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_tsmc_page  # noqa: E402  TSMC 2~8절 원문 그림
import vc_figs  # noqa: E402  다른 사슬의 2~7절 — 데이터로 세운 그림

EV_KO = {'CONFIRMED': u'공시로 확인', 'ESTIMATED': u'추정', 'INFERRED': u'정황 추론',
         'UNDISCLOSED': u'비공개', 'HISTORICAL_CURRENT_UNKNOWN': u'과거 관측·현재 미상'}
CRIT_KO = {'VERY_HIGH': (u'매우 높음', 'h1'), 'HIGH': (u'높음', 'h3'), 'MEDIUM': (u'중간', 'h5')}
REL_KO = {'INVESTS_IN': u'지분 투자', 'SUBSIDIARY_OF': u'자회사', 'OPERATES_THROUGH': u'운영 자회사',
          'CORPORATE_CONTROL': u'지배', 'EXECUTES_THROUGH_SUBSIDIARY': u'실행 자회사',
          'HOLDS_PROJECT': u'프로젝트 보유', 'FINANCES': u'금융', 'JV_ASSEMBLY': u'합작',
          'INTERNAL_MATERIAL_SUPPLY': u'내부 소재 공급', 'INTRAGROUP_SUPPLY': u'그룹 내 공급',
          'MANUFACTURES': u'제조', 'PROCESSING': u'가공', 'SUPPLIES': u'공급',
          'EQUIPMENT_SUPPLY': u'장비 공급', 'OPERATES_AT_SITE': u'부지 운영', 'OWNS_SITE': u'부지 소유',
          'DEVELOPS': u'개발', 'INVESTS': u'투자'}


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def fmt(v):
    if v is None:
        return ''
    return ('%g' % v) if isinstance(v, (int, float)) else str(v)


CSS = u'''
  :root{--paper:#EEF1F4;--ink:#1C2733;--mute:#6B7785;--line:#C9D1DA;--tsmc:#0E6B66;--tsmc-soft:#D6ECEA;
    --kr:#B4620A;--kr-soft:#F6E3C8;--jp:#9B1C3A;--jp-soft:#F3D5DC;--cust:#31507A;--cust-soft:#D9E2EF;--sup:#8A96A3}
  *{box-sizing:border-box}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:"IBM Plex Sans KR",-apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;font-size:15px;line-height:1.55}
  main{max-width:960px;margin:0 auto;padding:28px 18px 64px}
  h1{font-size:26px;font-weight:600;margin:0 0 4px;letter-spacing:-0.01em}
  .sub{color:var(--mute);margin:0 0 18px;font-size:14px}
  .sub a,.note a,td a{color:var(--tsmc)}
  nav.chains{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 28px}
  nav.chains a{font-size:13px;padding:4px 10px;border:1px solid var(--line);border-radius:14px;color:var(--ink);text-decoration:none;background:#fff}
  nav.chains a.on{background:var(--tsmc);border-color:var(--tsmc);color:#fff}
  section{margin:0 0 44px;padding-top:18px;border-top:2px solid var(--ink)}
  h2{font-size:18px;font-weight:600;margin:0 0 4px}
  h2 small{font-weight:400;color:var(--mute);font-size:13px;margin-left:8px}
  p.note{margin:0 0 14px;color:var(--mute);font-size:13.5px;max-width:70ch}
  svg{width:100%;height:auto;display:block;font-family:inherit}
  .frame{border:1px solid var(--line);border-radius:4px;overflow:hidden;background:#fff;height:640px}
  .frame iframe{width:100%;height:100%;border:0;display:block}
  .legend{display:flex;flex-wrap:wrap;gap:14px;margin:10px 0 0;font-size:13px;color:var(--mute)}
  .legend span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}
  .l-tsmc::before{background:var(--tsmc)} .l-kr::before{background:var(--kr)} .l-jp::before{background:var(--jp)} .l-cust::before{background:var(--cust)} .l-sup::before{background:#8A96A3}
  table{border-collapse:collapse;width:100%;font-size:13.5px;margin-top:8px}
  th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
  th{font-weight:500;color:var(--mute)}
  td.nw{white-space:nowrap}
  .heat td.c{width:76px;text-align:center;color:#fff;font-weight:500;border-radius:3px}
  .heat th{white-space:nowrap}
  .h1{background:#7F1D1D}.h2{background:#B91C1C}.h3{background:#D97706}.h4{background:#5B8C5A}.h5{background:#2F6F4E}
  .ev{display:inline-block;font-size:11.5px;padding:1px 6px;border:1px solid var(--line);border-radius:3px;color:var(--mute);white-space:nowrap}
  .ev.c{border-color:var(--tsmc);color:var(--tsmc)}
  .bars{margin-top:6px}
  .bar{display:grid;grid-template-columns:200px 1fr 120px;gap:10px;align-items:center;font-size:13.5px;padding:4px 0}
  .bar .lab{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .bar .tr{height:16px;background:#fff;border:1px solid var(--line);border-radius:3px;overflow:hidden}
  .bar .fill{height:100%;background:var(--tsmc)}
  .bar.sup .fill{background:var(--sup)}
  .bar .val{color:var(--mute);white-space:nowrap}
  .tl{position:relative;padding-left:22px}
  .tl::before{content:"";position:absolute;left:6px;top:4px;bottom:4px;width:2px;background:var(--line)}
  .tl .yr{position:relative;margin:0 0 18px}
  .tl .yr::before{content:"";position:absolute;left:-21px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--tsmc)}
  .tl b{display:block;font-weight:600;margin-bottom:2px}
  .tl .row{display:grid;grid-template-columns:64px 1fr;gap:6px 10px;font-size:13.5px}
  .tl .row span:first-child{color:var(--mute)}
  .tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .sv{overflow-x:auto;-webkit-overflow-scrolling:touch}
  /* 핵심 수치 — 표가 아니라 줄 목록. 좁은 화면에서 네 칸 표는 출처 칸이 잘려 나갔다 */
  .claims{margin-top:6px}
  .cl{display:grid;grid-template-columns:110px 1fr;gap:4px 14px;padding:9px 0;border-bottom:1px solid var(--line);font-size:13.5px}
  .cl .per{color:var(--mute);white-space:nowrap}
  .cl .st{margin:0}
  .cl .src{grid-column:2;font-size:12px;color:var(--mute)}
  .cl .src a{color:var(--tsmc)}
  @media (max-width:640px){
    h1{font-size:22px} .frame{height:520px} .bar{grid-template-columns:120px 1fr 90px}
    nav.chains{flex-wrap:nowrap;overflow-x:auto;padding-bottom:4px;margin-bottom:20px}
    nav.chains a{white-space:nowrap;flex:none}
    /* 그림·표는 되도록 한 화면 폭에 — 옆으로 밀지 않는다(2026-09-13). 글자는 셀 안에서 줄바꿈 */
    .cl{grid-template-columns:1fr}
    .cl .src{grid-column:1}
    table{font-size:11.5px} th,td{padding:5px 4px;overflow-wrap:anywhere}
    td.nw{white-space:normal}
    .tw table{min-width:0}
    .tw table.fit{min-width:0;font-size:11.5px;table-layout:fixed;width:100%}
    .heat.fit th,.heat.fit td{padding:6px 3px;overflow-wrap:anywhere}
    .heat.fit th{font-size:10px;line-height:1.2;white-space:normal}
    .heat.fit th:nth-child(1),.heat.fit td:nth-child(1){width:28%}
    .heat.fit th:nth-child(2),.heat.fit td:nth-child(2){width:30%}
    .heat.fit td.c{width:auto;padding:6px 0}
    .bar{grid-template-columns:100px 1fr 96px} .bar .val{white-space:normal;font-size:12px;line-height:1.25}
  }
  /* 조사 보고서(마크다운) */
  .md h2{margin-top:28px;padding-top:18px;border-top:2px solid var(--ink)}
  .md h3{font-size:15.5px;margin:22px 0 6px}
  .md p{max-width:80ch}
  .md ul,.md ol{padding-left:22px}
  .md li{margin:3px 0}
  .md blockquote{margin:10px 0;padding:6px 12px;border-left:3px solid var(--line);color:var(--mute)}
  .md pre{background:#fff;border:1px solid var(--line);border-radius:4px;padding:10px 12px;overflow-x:auto;font-size:12.5px;line-height:1.45}
  .md code{font-size:13px}
  .md .tw{overflow-x:auto}
  .md table{font-size:13px}
  .md hr{border:0;border-top:1px solid var(--line);margin:22px 0}
'''


class Chain(object):
    def __init__(self, ck, ents, srcs):
        b = os.path.join(DATA, 'chains', ck)
        self.id = ck
        self.meta = rd(os.path.join(b, 'chain.json'))
        self.focal = self.meta['focal_entity']
        self.label = self.meta.get('label') or self.focal
        self.rels = rd(os.path.join(b, 'relationships.json'))
        self.cls = rd(os.path.join(b, 'classifications.json'))
        self.claims = rd(os.path.join(b, 'claims.json')) if os.path.exists(os.path.join(b, 'claims.json')) else []
        self.obs = rd(os.path.join(b, 'observations.json')) if os.path.exists(os.path.join(b, 'observations.json')) else []
        self.ents, self.srcs = ents, srcs

    def nm(self, i):
        e = self.ents.get(i) or {}
        return e.get('name_ko') or e.get('display_name') or e.get('name') or i

    def src_html(self, ids):
        out = []
        for s in ids or []:
            x = self.srcs.get(s)
            if not x:
                continue
            t = esc(x.get('title') or s)
            d = x.get('published_date')
            lab = t + ((u' (%s)' % d) if d else '')
            out.append((u'<a href="%s">%s</a>' % (esc(x['url']), lab)) if x.get('url') else lab)
        return u' · '.join(out)


def period_key(p):
    u"""기간 문자열을 대충 시간순으로 — FY2027 Q1 > 2026 Q2 > 2026 > FY2026 > 2025."""
    p = p or ''
    m = re.search(r'(\d{4})', p)
    y = int(m.group(1)) if m else 0
    q = re.search(r'Q(\d)', p)
    h = re.search(r'H(\d)', p)
    sub = (int(q.group(1)) * 2 if q else (int(h.group(1)) * 4 if h else 9))
    return (y, sub, p)


# ── 절 ─────────────────────────────────────────────────────────────────
def sec_map(c, n, title=u'전체 지도'):
    q = 'focal=%s&amp;open=*' % c.focal
    return u'''  <section>
    <h2>%d. %s<small>앞단 → %s → 뒷단</small></h2>
    <p class="note">밸류체인 탐색기로 그린다. 상자와 선은 데이터에서 나오고 상자를 누르면 근거가 열린다. 색은 소속: 청록 타겟, 주황 한국 회사, 진홍 병목(공급 여력 HIGH 이상), 남색 고객. 중개·유통은 점선 테두리. 선 굵기에는 뜻이 없다. <a href="밸류체인 탐색기.html?%s">새 창에서 크게 보기</a></p>
    <div class="frame"><iframe src="밸류체인 탐색기.html?%s" title="%s 밸류체인 탐색기" loading="lazy"></iframe></div>
    <div class="legend"><span class="l-tsmc">타겟</span><span class="l-kr">한국 회사</span><span class="l-jp">병목</span><span class="l-cust">고객</span><span class="l-sup">그 밖의 공급사</span></div>
  </section>
''' % (n, esc(title), esc(c.label), q, q, esc(c.label))


def sec_claims(c, n):
    rows = [x for x in c.claims if x.get('subject') == c.focal]
    if not rows:
        return ''
    rows.sort(key=lambda x: period_key(x.get('period')), reverse=True)
    tr = []
    for x in rows[:16]:
        ev = x.get('evidence_level') or ''
        tr.append(u'<div class="cl"><div class="per">%s<br><span class="ev%s">%s</span></div><p class="st">%s</p><div class="src">%s</div></div>' % (
            esc(x.get('period') or u'시점 미상'), ' c' if ev == 'CONFIRMED' else '', esc(EV_KO.get(ev, ev)),
            esc(x.get('statement')), c.src_html(x.get('source_ids'))))
    return u'''  <section>
    <h2>%d. 핵심 수치<small>최신 공시부터</small></h2>
    <p class="note">회사를 주어로 한 주장 %d건 가운데 최근 %d건. 근거 등급은 공시로 확인, 추정, 정황 추론 순으로 약하다.</p>
    <div class="claims">%s</div>
  </section>
''' % (n, len(rows), min(16, len(rows)), u''.join(tr))


def latest_share(x):
    best = None
    for sh in x.get('shares') or []:
        if sh.get('value') is None and sh.get('value_low') is None:
            continue
        k = (sh.get('period_end') or sh.get('as_of_date') or '', )
        if best is None or k > (best.get('period_end') or best.get('as_of_date') or '',):
            best = sh
    return best


def sec_shares(c, n, kind, title, note, cls):
    items = []
    for x in c.cls.get(kind) or []:
        sh = latest_share(x)
        if not sh:
            continue
        txt = vc_figs.share_txt(sh)
        w = vc_figs.share_pct(sh) or 0  # 막대는 percent 만. 금액으로 적힌 갈래는 글자만 남긴다
        items.append((w, x.get('label'), txt, sh.get('period'), sh.get('denominator')))
    if not items:
        return ''
    items.sort(key=lambda t: -(t[0] or 0))
    dens = sorted(set((t[4] or u'분모 미상') for t in items))
    bars = u''.join(u'<div class="bar%s"><span class="lab" title="%s">%s</span><div class="tr"><div class="fill" style="width:%s%%"></div></div><span class="val">%s · %s</span></div>' % (
        cls, esc(t[4] or ''), esc(t[1]), min(100, max(0, t[0] or 0)), esc(t[2]), esc(t[3] or '')) for t in items)
    return u'''  <section>
    <h2>%d. %s<small>분류마다 가장 최근 값</small></h2>
    <p class="note">%s 분모: %s. 분모가 다른 값은 한 줄에서 더하지 않는다.</p>
    <div class="bars">%s</div>
  </section>
''' % (n, title, note, esc(u' / '.join(dens)), bars)


def sec_bottleneck(c, n):
    rows = [r for r in c.rels if r.get('capacity_criticality') in CRIT_KO]
    if not rows:
        return ''
    order = {'VERY_HIGH': 0, 'HIGH': 1, 'MEDIUM': 2}
    rows.sort(key=lambda r: (order[r['capacity_criticality']], c.nm(r['source_entity'])))
    ss = dict((x['id'], x.get('label')) for x in c.cls.get('supply_sources') or [])
    tr = []
    for r in rows:
        ko, hcls = CRIT_KO[r['capacity_criticality']]
        item = u'·'.join(ss.get(i, i) for i in (r.get('supply_source_ids') or [])) or (r.get('component') or '')
        tr.append(u'<tr><td class="nw">%s</td><td>%s</td><td>%s</td><td class="c %s">%s</td><td><span class="ev%s">%s</span></td><td>%s</td></tr>' % (
            esc(c.nm(r['source_entity'])), esc(c.nm(r['target_entity'])), esc(item), hcls, ko,
            ' c' if r.get('evidence_level') == 'CONFIRMED' else '', esc(EV_KO.get(r.get('evidence_level'), '')),
            esc((r.get('notes') or '')[:120])))
    return u'''  <section>
    <h2>%d. 병목<small>공급 여력 등급이 적힌 줄</small></h2>
    <p class="note">관계 데이터의 공급 여력 등급(capacity_criticality)이 중간 이상인 공급 줄 %d개. 탐색기에서 진홍으로 칠한 상자와 같다.</p>
    <div class="tw"><table class="heat"><tr><th>공급사</th><th>받는 쪽</th><th>품목</th><th>등급</th><th>근거</th><th>비고</th></tr>%s</table></div>
  </section>
''' % (n, len(rows), u''.join(tr))


def sec_customers(c, n):
    rid = dict((r['id'], r) for r in c.rels)
    rows = []
    for o in c.obs:
        r = rid.get(o.get('relationship_id'))
        if not r or r.get('lane') != 'DOWNSTREAM' or r.get('source_entity') != c.focal:
            continue
        if not re.search(r'share$', o.get('metric') or '') or o.get('unit') not in ('percent', '%'):
            continue
        v = o.get('value')
        txt = (u'%s~%s%%' % (fmt(o.get('value_low')), fmt(o.get('value_high')))) if v is None else (u'%s%%' % fmt(v))
        rows.append((period_key(o.get('period')), c.nm(r['target_entity']), o.get('period'), txt,
                     o.get('denominator') or '', o.get('evidence_level'), o.get('source_ids')))
    if not rows:
        return ''
    rows.sort(key=lambda t: (t[0], t[1]), reverse=True)
    tr = u''.join(u'<tr><td class="nw">%s</td><td class="nw">%s</td><td class="nw">%s</td><td>%s</td><td><span class="ev%s">%s</span></td><td>%s</td></tr>' % (
        esc(t[1]), esc(t[2] or ''), esc(t[3]), esc(t[4]), ' c' if t[5] == 'CONFIRMED' else '', esc(EV_KO.get(t[5], '')), c.src_html(t[6])) for t in rows[:20])
    return u'''  <section>
    <h2>%d. 고객·전방시장 비중<small>타겟에서 나가는 줄의 비중 관측</small></h2>
    <p class="note">타겟에서 나가는 줄에 붙은 비중 관측 %d건. 고객 실명이 아니라 전방시장 갈래일 수도 있고, 익명 고객은 공시가 이름을 안 밝힌 자리다.</p>
    <div class="tw"><table><tr><th>고객·전방</th><th>시점</th><th>비중</th><th>분모</th><th>근거</th><th>출처</th></tr>%s</table></div>
  </section>
''' % (n, len(rows), tr)


def sec_equity(c, n):
    rows = [r for r in c.rels if r.get('lane') == 'CORPORATE']
    if not rows:
        return ''
    tr = u''.join(u'<tr><td class="nw">%s</td><td class="nw">%s</td><td class="nw">%s</td><td class="nw">%s</td><td>%s</td></tr>' % (
        esc(c.nm(r['source_entity'])), esc(REL_KO.get(r.get('relationship_type'), r.get('relationship_type'))),
        esc(c.nm(r['target_entity'])), esc(r.get('valid_from') or ''), esc((r.get('notes') or '')[:140])) for r in rows)
    return u'''  <section>
    <h2>%d. 지분·소유<small>거래 위에 소유를 겹치기</small></h2>
    <p class="note">기업 구조 선 %d개. 탐색기는 이 선을 따라가지 않고 서랍에만 보인다.</p>
    <div class="tw"><table><tr><th>주체</th><th>관계</th><th>대상</th><th>부터</th><th>비고</th></tr>%s</table></div>
  </section>
''' % (n, len(rows), tr)


def sec_sources(c, n):
    used = set()
    for r in c.rels:
        used.update(r.get('source_ids') or [])
    for x in c.claims + c.obs:
        used.update(x.get('source_ids') or [])
    rows = [c.srcs[s] for s in used if s in c.srcs]
    if not rows:
        return ''
    rows.sort(key=lambda s: (s.get('published_date') or ''), reverse=True)
    tr = u''.join(u'<tr><td class="nw">%s</td><td>%s</td><td>%s</td></tr>' % (
        esc(s.get('published_date') or ''), esc(s.get('publisher') or ''),
        (u'<a href="%s">%s</a>' % (esc(s['url']), esc(s.get('title') or s['id']))) if s.get('url') else esc(s.get('title') or s['id'])) for s in rows)
    return u'''  <section>
    <h2>%d. 출처<small>%d건</small></h2>
    <div class="tw"><table><tr><th>날짜</th><th>발행</th><th>문서</th></tr>%s</table></div>
  </section>
''' % (n, len(rows), tr)


# ── 장 ─────────────────────────────────────────────────────────────────
def page(c, chains):
    nav = u'<a href="기업분석 대시보드.html">← 기업분석</a>'
    nav += u''.join(u'<a href="%s"%s>%s</a>' % (esc(fname(x)), ' class="on"' if x.id == c.id else '', esc(x.label)) for x in chains)
    if report_path(c):
        nav += u'<a href="%s">%s 조사 보고서</a>' % (esc(rname(c)), esc(c.label))
    nav += u'<a href="밸류체인 탐색기.html">탐색기</a>'
    parts, n = [], 1
    # 1절 전체 지도는 탐색기다 — TSMC 는 손으로 그린 SVG 를 탐색기로 이식했다(2026-09-13).
    # 그 지도의 상자·선은 chains/tsmc 데이터로 옮겨져 탐색기가 그린다
    parts.append(sec_map(c, n)); n += 1
    if c.id == 'tsmc':
        # 2~8절은 받은 그림 그대로. 번호도 원문과 같다
        raw = gen_tsmc_page.SECTIONS_2_8.replace('</main>\n</body>\n</html>\n', '')
        raw = raw.replace('<svg ', '<div class="sv"><svg ').replace('</svg>', '</svg></div>')
        # 병목 히트맵은 점수 칸이 좁아 폰 화면에도 한눈에 든다 — 옆으로 밀지 않고 맞춘다(fit)
        raw = raw.replace('<table class="heat">', '<div class="tw"><table class="heat fit">').replace('</table>', '</table></div>')
        parts.append(raw)
        n = 9
        fns = (sec_claims,
               lambda cc, k: sec_shares(cc, k, 'revenue_types', u'매출원 구성', u'매출 갈래마다 가장 최근 비중.', ''),
               lambda cc, k: sec_shares(cc, k, 'supply_sources', u'공급원 구성', u'공급 갈래마다 가장 최근 비중.', ' sup'),
               sec_bottleneck, sec_customers, sec_equity, sec_sources)
    else:
        # 다른 사슬 — TSMC 2~8절과 같은 꼴을 데이터로 세운다. 트리가 비중을 보여 주니 막대 절은 안 겹친다
        fns = vc_figs.SECTIONS + (sec_claims, sec_sources)
    for fn in fns:
        h = fn(c, n)
        if h:
            parts.append(h); n += 1
    sub = (u'보고서 <a href="%s">「TSMC 밸류체인 조사」</a>의 시각 요약. 수치는 2025년 공시 기준, 추정치는 ~로 표시. 1절 전체 지도는 손으로 그린 지도를 탐색기로 이식한 것이고 9절부터는 데이터(chains/tsmc)에서 세운 절이다.' % esc(rname(c))) \
        if c.id == 'tsmc' else esc(c.meta.get('note') or '') + u' 그림은 전부 데이터(data/valuechain/chains/%s)에서 세웠고 값마다 출처가 붙는다. 데이터에 없는 값(단위경제·마진 풀·시나리오)은 그리지 않는다.' % c.id
    return u'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s 밸류체인 — 그림으로 보기</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">
<style>%s</style>
</head>
<body>
<main>
  <h1>%s 밸류체인 — 그림으로 보기</h1>
  <p class="sub">%s</p>
  <nav class="chains">%s</nav>
%s</main>
</body>
</html>
''' % (esc(c.label), CSS, esc(c.label), sub, nav, u''.join(parts))


def fname(c):
    return u'%s 밸류체인.html' % c.label


def rname(c):
    return u'%s 밸류체인 조사.html' % c.label


def report_path(c):
    hits = sorted(glob.glob(os.path.join(DATA, 'reports', c.id + '-*.md')))
    return hits[-1] if hits else None


def report_page(c, chains):
    u"""조사 보고서(마크다운)를 같은 꼴의 장으로. 표는 가로로 넘치면 그 표만 스크롤한다."""
    rp = report_path(c)
    if not rp:
        return None
    md = io.open(rp, encoding='utf-8').read()
    body = mistune.markdown(md, escape=False)
    body = body.replace('<table>', '<div class="tw"><table>').replace('</table>', '</table></div>')
    # 첫 h1 은 장 제목으로 쓰니 본문에서 뺀다
    m = re.match(r'\s*<h1>(.*?)</h1>', body, re.S)
    title = re.sub(r'<.*?>', '', m.group(1)) if m else (u'%s 밸류체인 조사' % c.label)
    if m:
        body = body[m.end():]
    nav = u'<a href="기업분석 대시보드.html">← 기업분석</a>'
    nav += u''.join(u'<a href="%s">%s</a>' % (esc(fname(x)), esc(x.label)) for x in chains)
    nav += u'<a href="%s" class="on">%s 조사 보고서</a><a href="밸류체인 탐색기.html">탐색기</a>' % (esc(rname(c)), esc(c.label))
    return u'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">
<style>%s</style>
</head>
<body>
<main>
  <h1>%s</h1>
  <p class="sub">조사 보고서 원문 그대로. 그림은 <a href="%s">%s 밸류체인 그림 장</a>, 상자·선은 <a href="밸류체인 탐색기.html?focal=%s&amp;open=*">탐색기</a>. 원문 파일 <code>%s</code>.</p>
  <nav class="chains">%s</nav>
  <div class="md">%s</div>
</main>
</body>
</html>
''' % (esc(title), CSS, esc(title), esc(fname(c)), esc(c.label), c.focal,
       esc(os.path.relpath(rp, ROOT).replace(os.sep, '/')), nav, body)


def build():
    ents = dict((e['id'], e) for e in rd(os.path.join(DATA, 'entities.json')))
    srcs = dict((s['id'], s) for s in rd(os.path.join(DATA, 'sources.json')))
    base = os.path.join(DATA, 'chains')
    chains = [Chain(d, ents, srcs) for d in sorted(os.listdir(base))
              if os.path.exists(os.path.join(base, d, 'chain.json'))]
    for c in chains:
        html = page(c, chains)
        out = os.path.join(OUTDIR, fname(c))
        with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print(u'%s · %d KB' % (os.path.relpath(out, ROOT), len(html.encode('utf-8')) // 1024))
        rhtml = report_page(c, chains)
        if rhtml:
            rout = os.path.join(OUTDIR, rname(c))
            with io.open(rout, 'w', encoding='utf-8', newline='\n') as f:
                f.write(rhtml)
            print(u'%s · %d KB' % (os.path.relpath(rout, ROOT), len(rhtml.encode('utf-8')) // 1024))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
