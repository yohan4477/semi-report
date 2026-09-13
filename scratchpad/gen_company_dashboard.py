# -*- coding: utf-8 -*-
u"""기업분석 대시보드 — 회사 하나가 카드 하나. 대시보드/기업분석 대시보드.html

밸류체인 데이터(data/valuechain)에서 사슬마다 카드를 세운다. 카드에는 그 회사의 최근 주장(핵심
수치)·매출원 구성 막대(가장 최근 비중, 값은 전부 classifications 의 shares)·병목 수·그림 장과
조사 보고서 링크가 든다. 맨 위 고정 층은 밸류체인 탐색기(iframe)다 — 「기업분석 안에 밸류체인
대시보드를 넣는다」(2026-09-13). 첫 화면은 규약대로 최신순 이름 목록이다(dash_common.render).

  PYTHONIOENCODING=utf-8 python scratchpad/gen_company_dashboard.py
"""
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scripts'))
import dash_common as dc  # noqa: E402
import gen_vcreport as vr  # noqa: E402  사슬 로더·기간 정렬·보고서 파일 찾기

ROOT = dc.ROOT
DATA = os.path.join(ROOT, 'data', 'valuechain')
OUT = os.path.join(ROOT, '대시보드', '기업분석 대시보드.html')

# 섹션 = 업종. 카드가 서는 태그다
SEC_OF = {
    'tsmc': ('sec-foundry', '01', '반도체 파운드리', '웨이퍼를 받아 칩을 찍는 회사와 그 앞뒤'),
    'nvidia': ('sec-aichip', '02', 'AI 반도체', 'GPU·가속기를 설계해 파운드리에 맡기는 회사'),
    'taiyo-yuden': ('sec-passive', '03', '전자부품', 'MLCC·인덕터처럼 기판에 오르는 수동 부품'),
    'kr-substrate': ('sec-substrate', '04', '반도체 기판', '칩과 보드 사이 패키지 기판'),
    'bloom-energy': ('sec-fuelcell', '05', '연료전지·전력', '데이터센터에 전기를 대는 발전 설비'),
    'nebius': ('sec-aicloud', '06', 'AI 클라우드', 'GPU 를 사서 시간 단위로 파는 회사'),
}
TOPIC_OF = {'sec-foundry': 'market', 'sec-aichip': 'market', 'sec-passive': 'market',
            'sec-substrate': 'market', 'sec-fuelcell': 'market', 'sec-aicloud': 'market'}

esc = vr.esc


def latest_period(c):
    ps = [x.get('period') for x in c.claims if x.get('subject') == c.focal and x.get('period')]
    return max(ps, key=vr.period_key) if ps else ''


def date_of(c):
    u"""카드 날짜 — 그 사슬 출처 가운데 가장 늦은 발행일. 최신순 목록이 이 값으로 선다."""
    used = set()
    for r in c.rels:
        used.update(r.get('source_ids') or [])
    for x in c.claims + c.obs:
        used.update(x.get('source_ids') or [])
    ds = [c.srcs[s].get('published_date') for s in used if s in c.srcs and c.srcs[s].get('published_date')]
    ds = [d for d in ds if re.match(r'\d{4}-\d{2}', d or '')]
    return max(ds) if ds else ''


def share_fig(c):
    u"""매출원 구성 — 가로 순위 막대. 값은 classifications 의 가장 최근 비중이라 원문(공시)에 있다."""
    items = []
    for x in c.cls.get('revenue_types') or []:
        sh = vr.latest_share(x)
        if not sh:
            continue
        v = sh.get('value')
        if v is None:
            v = sh.get('value_high') or 0
        items.append((float(v), x.get('label'), sh.get('period') or '', sh.get('denominator') or ''))
    if not items:
        return None
    items.sort(key=lambda t: -t[0])
    items = items[:8]
    W, LW, RH, PAD = 640, 250, 26, 8
    H = PAD * 2 + RH * len(items)
    scale = (W - LW - 70) / max(100.0, max(t[0] for t in items))
    out = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s 매출원 구성">' % (W, H, esc(c.label))]
    for i, (v, lab, per, den) in enumerate(items):
        y = PAD + i * RH
        out.append('<text x="%d" y="%d" font-size="12" text-anchor="end" class="fig-ink">%s</text>'
                   % (LW - 8, y + 17, esc(lab)))
        out.append('<rect x="%d" y="%d" width="%.1f" height="16" rx="2" class="fig-bar"/>'
                   % (LW, y + 5, max(1.0, v * scale)))
        out.append('<text x="%.1f" y="%d" font-size="12" class="fig-ink">%s%%</text>'
                   % (LW + max(1.0, v * scale) + 6, y + 17, ('%g' % v)))
    out.append('</svg>')
    dens = sorted(set(t[3] for t in items if t[3]))
    pers = sorted(set(t[2] for t in items if t[2]))
    cap = ('① 막대 길이는 그 갈래가 분모(%s)에서 차지하는 비중 ② 시점은 %s, 갈래마다 가장 최근 값'
           % (esc(' / '.join(dens) or '미상'), esc(', '.join(pers) or '미상')))
    return ('매출원 구성', ''.join(out), cap)


def claim_date(c, x):
    u"""주장의 출처 가운데 가장 늦은 발행일 — 「최근 공시」 차례는 기간(전망은 먼 해)이 아니라 이것이다."""
    ds = [c.srcs[s].get('published_date') or '' for s in (x.get('source_ids') or []) if s in c.srcs]
    return max(ds) if ds else ''


def recent_claims(c):
    rows = [x for x in c.claims if x.get('subject') == c.focal and x.get('period')]
    rows.sort(key=lambda x: (claim_date(c, x), vr.period_key(x.get('period'))), reverse=True)
    return rows


def points_of(c):
    rows = recent_claims(c)
    pts = []
    for x in rows[:5]:
        pts.append('<b>%s.</b> %s' % (esc(x['period']), esc(x['statement'])))
    n_bott = sum(1 for r in c.rels if r.get('capacity_criticality') in ('HIGH', 'VERY_HIGH'))
    n_kr = len(set(r['source_entity'] for r in c.rels
                   if (c.ents.get(r['source_entity']) or {}).get('country') == '한국'))
    pts.append('<b>사슬.</b> 관계 %d줄, 공급 여력 등급이 HIGH 이상인 병목 줄 %d개, 한국 공급사 %d곳'
               % (len(c.rels), n_bott, n_kr))
    return pts


def links_of(c):
    fig = vr.fname(c)
    h = ['<a href="%s">%s 밸류체인 그림 장</a>' % (esc(fig), esc(c.label))]
    if vr.report_path(c):
        h.append('<a href="%s">조사 보고서 원문</a>' % esc(vr.rname(c)))
    h.append('<a href="밸류체인 탐색기.html?focal=%s&amp;open=*">탐색기에서 열기</a>' % c.focal)
    return ' · '.join(h)


def card_of(c):
    sec = SEC_OF[c.id]
    fig = share_fig(c)
    d = date_of(c)
    per = latest_period(c)
    lead = ''
    rows = recent_claims(c)
    if rows:
        lead = esc(rows[0]['statement'])
    n_src = len(set(s for r in c.rels for s in (r.get('source_ids') or [])))
    return {
        'section': sec,
        'topic': (TOPIC_OF[sec[0]], sec[2]),
        'title': esc(c.label),
        'gain': lead,
        'meta': ['밸류체인 사슬', '최근 공시 %s' % (d or per), '관계 %d줄' % len(c.rels), '출처 %d건' % n_src],
        'oneliner': esc(c.meta.get('note') or ''),
        'points': points_of(c),
        'figs': [(1, fig[0], fig[1], fig[2])] if fig else [],
        'note': '<b>보기</b> — %s' % links_of(c),
        # 목록에서 회사 이름을 누르면 그 회사의 그림 장(보고서 꼴)으로 간다 — 카드를 펴지 않는다
        '_href': vr.fname(c),
    }


CSS = '''
.fig-bar{fill:#0E6B66}
.fig-ink{fill:currentColor}
.vc-frame{border:1px solid var(--line,#C9D1DA);border-radius:6px;overflow:hidden;background:#fff;height:640px;margin:8px 0}
.vc-frame iframe{width:100%;height:100%;border:0;display:block}
.vc-links{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;margin:8px 0 0}
'''

HEADER = '''  <header>
    <p class="eyebrow">회사 하나를 밸류체인·핵심 수치·병목으로</p>
    <h1>기업분석</h1>
  </header>'''


def top_layer(chains):
    links = ' '.join('<a href="%s">%s</a>' % (esc(vr.fname(x)), esc(x.label)) for x in chains)
    return ('<p>회사를 고르고 눌러 넓히면 공급원·매출원·고객이 선다. 색은 소속(청록 타겟·주황 한국 회사·진홍 병목·남색 고객). '
            '<a href="밸류체인 탐색기.html">새 창에서 크게 보기</a></p>'
            '<div class="vc-frame"><iframe src="밸류체인 탐색기.html" title="밸류체인 탐색기" loading="lazy"></iframe></div>'
            '<div class="vc-links">그림 장: %s</div>' % links)


def main():
    ents = dict((e['id'], e) for e in vr.rd(os.path.join(DATA, 'entities.json')))
    srcs = dict((s['id'], s) for s in vr.rd(os.path.join(DATA, 'sources.json')))
    base = os.path.join(DATA, 'chains')
    chains = [vr.Chain(d, ents, srcs) for d in sorted(os.listdir(base))
              if os.path.exists(os.path.join(base, d, 'chain.json'))]
    chains = [c for c in chains if c.id in SEC_OF]
    cards = [card_of(c) for c in chains]
    footer = ('<p>값은 전부 data/valuechain 의 공시·조사 데이터에서 나오고 카드마다 출처가 붙는다. 투자 추천이 아니다.</p>'
              '<div class="meta-row"><span>회사 <b>%d</b></span><span>관계 <b>%d</b></span></div>'
              '\n  페이지 생성은 <code>scratchpad/gen_company_dashboard.py</code>'
              % (len(cards), sum(len(c.rels) for c in chains)))
    dc.render(cards, '기업분석', HEADER, footer, OUT,
              top=top_layer(chains), top_title='밸류체인 탐색기', top_id='sec-explorer',
              top_sub='회사 여섯의 공급·매출·고객 사슬을 한 판에서 오간다', top_n=len(chains),
              search_ph='회사 이름으로 찾기', extra_css=CSS, newest_first=True)
    print('회사 %d · %s' % (len(cards), OUT))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
