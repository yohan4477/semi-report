# -*- coding: utf-8 -*-
"""체인 대시보드 — 밸류체인 정본 하나가 카드 한 장.

씨모어가 「밸류체인을 싹 까 본다」고 한 자리를 원문 117편에서 전수로 뽑아(insights/chains/
extract) 산업별 사슬로 합친 것(insights/chains/canon)이 재료다. 카드 목록은 이 파일에
없다 — 정본 파일 하나가 카드 한 장이고 섹션·제목·한 줄까지 그 json 에 있다.

  카드 = 사슬 하나. 마디 하나가 아니다. 마디로 쪼개면 목록이 이백 줄이 되고 첫 화면에서
  사슬이 안 보인다. 마디는 카드 안에서 번호 매긴 줄로 선다.

  도해가 글보다 앞이다(확정 규칙). 사슬 판은 `chain_figs.chain_svg` 가 굽는다.

  하위 사슬은 부모 카드에서 링크로 간다. 부모의 어느 마디를 확대한 것인지 카드 머리에 적는다.

  파이프라인
    insights/check_chain.py            추출층 — 줄 주소가 실재하나
    insights/check_chain.py --canon    정본층 — refs 가 sources 안에서 실재하나
    scratchpad/gen_chain_dashboard.py  이 화면

  PYTHONIOENCODING=utf-8 python scratchpad/gen_chain_dashboard.py
"""
import glob
import html as _html
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc  # noqa: E402
import chain_figs  # noqa: E402

sys.path.insert(0, os.path.join(dc.ROOT, 'insights', 'chains'))
from sections import SECTIONS  # noqa: E402

CANON = os.path.join(dc.ROOT, 'insights', 'chains', 'canon', '*.json')
RAW = 'content/understanding/채널 씨모어/raw/%s.md'
OUT = os.path.join(dc.ROOT, '대시보드', '체인 대시보드.html')

# 섹션 설명 — 섹션 코드마다 한 줄. sections.py 는 코드와 이름만 쥔다(추출도 그 파일을 읽어서
# 설명까지 넣으면 검사기가 화면 문구를 물게 된다)
SEC_DESC = {
    'nuclear': '우라늄이 연료가 되어 발전하고 남는 데까지, 농축 권한이 갈리는 자리',
    'pharma': '후보물질에서 유통까지 — 어느 마디에 돈이 남는지 진행자가 판단을 바꾼 자리',
    'pharmadist': '약이 가는 길과 돈이 가는 길이 다르다. PBM 이 어디서 끼어들었나',
    'space': '컨텐츠·플랫폼·네트워크·터미널 — 우주 산업을 네 마디로 자른 틀과 그 아래',
    'aiinfra': 'GPU 한 칩에서 데이터센터 건설까지, 사슬이 해마다 길어진 자취',
    'physicalai': '센서에서 액추에이터까지 — 자율주행이 걸린 자리는 어디인가',
    'findata': '데이터가 만들어져 팔리기까지, 그리고 청산소가 낀 뒤 무엇이 바뀌었나',
    'finance': '돈이 누구를 거쳐 어디로 가나 — 주문·대출채권·물량 배정',
    'energy': '캐낸 것이 쓸 것이 되기까지, 웨이퍼·알루미나·원유가 지나는 자리',
    'realestate': '땅에서 분양대금까지, 그리고 건물이 다시 금융상품이 되는 길',
    'ship': '철강과 전자장비가 배가 되어 발주처에 가기까지',
    'hotel': '건물 주인과 브랜드와 운영이 갈라진 뒤 돈이 도는 순서',
    'sports': '리그의 데이터 사용권이 북메이커와 미디어에 닿기까지',
    'platform': '콘텐츠·플랫폼·네트워크·터미널 — 광고비와 매출이 갈리는 자리',
    'health': '진료가 청구가 되어 보험사 승인까지 가는 길',
}

SEC = {}
for i, (code, name, _inds) in enumerate(SECTIONS, 1):
    SEC[code] = ('sec-%s' % code, '%02d' % i, name, SEC_DESC.get(code, ''))

NUM = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮'


def esc(s):
    return _html.escape(s or '', quote=False)


def num(i):
    return NUM[i - 1] if 1 <= i <= len(NUM) else '(%d)' % i


def co_line(stage):
    """마디에 선 회사를 한 줄로. 원문이 댄 역할이 있으면 괄호로 붙인다."""
    out = []
    for c in stage.get('companies') or []:
        nm = esc(c.get('name'))
        role = esc(c.get('role'))
        out.append('<b>%s</b>%s' % (nm, ' — %s' % role if role else ''))
    return ' · '.join(out)


def points_of(d):
    """마디마다 한 줄. 번호는 ①②③ — 카드 안 나열이라 「1. 2.」가 아니다(글 규칙)."""
    pts = []
    for s in d.get('stages') or []:
        head = '<b>%s %s.</b>' % (num(s.get('order', 0)), esc(s.get('name')))
        body = esc(s.get('desc'))
        if s.get('bottleneck') == 'high':
            body += ' <b>여기가 병목이다</b> — %s' % esc(s.get('bottleneck_why'))
        co = co_line(s)
        if co:
            body += '<br><span class="ch-co">선 회사 — %s</span>' % co
        pts.append('%s %s' % (head, body))
    return pts


def clash_of(d):
    """진행자 판단. 회차마다 갈린 자리가 이 장에서 가장 값어치 있는 대목이라 따로 세운다."""
    out = []
    for s in d.get('stages') or []:
        j = (s.get('judgment') or '').strip()
        if j:
            out.append((esc(s.get('name')), esc(j)))
    return out


def stats_of(d):
    """센 것만 — 마디 수·병목 수·원문 편수. 죄다 이 카드가 실제로 쥔 수다."""
    st = d.get('stages') or []
    n_bn = sum(1 for s in st if s.get('bottleneck') == 'high')
    n_co = sum(len(s.get('companies') or []) for s in st)
    out = [('%d' % len(st), '마디'), ('%d' % n_co, '원문이 댄 회사')]
    if n_bn:
        out.append(('%d' % n_bn, '원문이 병목이라 한 마디'))
    return out


def note_of(d, kids):
    """무엇을 재료로 삼았나, 아래로 어디가 이어지나. 영수증은 카드 밖에 두지 않는다."""
    src = ' · '.join('<a href="%s">%s</a>' % (dc.blob(RAW % s['src']), esc(s.get('date') or s['src']))
                     for s in d.get('sources') or [])
    h = ['<b>재료</b> — 씨모어 전사 %d편: %s' % (len(d.get('sources') or []), src)]
    if (d.get('notes') or '').strip():
        h.append(esc(d['notes']))
    if kids:
        h.append('<b>이 사슬에서 갈라지는 것</b> — %s'
                 % ' · '.join('<a href="#%s">%s</a>' % (dc.card_id(k['chain_name']), esc(k['chain_name']))
                              if hasattr(dc, 'card_id') else esc(k['chain_name']) for k in kids))
    return '<br>'.join(h)


# `fig_layout` 의 CSS 는 이 장이 직접 실어야 한다. 안 실으면 `.fl-b{fill:var(--surface)}`
# 규칙 자체가 없어 상자가 새까맣게 칠해진다 — 다크모드 문제가 아니라 규칙 누락이다
CSS = chain_figs.fl.CSS + chain_figs.CSS + '''
  .ch-co{font-size:13px;color:var(--ink-3)}
  .ch-parent{font-size:12.5px;color:var(--ink-3);margin:0 0 6px}
'''


def load():
    ds = [json.load(io.open(p, encoding='utf-8')) for p in sorted(glob.glob(CANON))]
    by_slug = {d['canon_slug']: d for d in ds}
    kids = {}
    for d in ds:
        if d.get('parent'):
            kids.setdefault(d['parent'], []).append(d)
    cards = []
    for d in ds:
        code = d['section']
        if code not in SEC:
            raise SystemExit('%s: 모르는 섹션 %s' % (d['canon_slug'], code))
        svg, _ = chain_figs.chain_svg(d)
        cap = '마디 %d개. 회사는 원문이 이름을 댄 것만 넣었다' % len(d.get('stages') or [])
        # 카드 날짜는 그 사슬을 판 원문 가운데 가장 나중 것이다 — 최신순 목록이 「언제 판
        # 이야기인가」로 서야 한다
        dates = sorted(s.get('date', '') for s in d.get('sources') or [])
        lead = ''
        if d.get('parent') and d['parent'] in by_slug:
            lead = ('<p class="ch-parent">「%s」의 <b>%s</b> 마디를 확대한 사슬이다</p>'
                    % (esc(by_slug[d['parent']]['chain_name']), esc(d.get('parent_stage'))))
        cards.append({
            'section': SEC[code],
            'topic': ('market', SEC[code][2]),
            'title': esc(d['chain_name']),
            'gain': esc(d['one_line']),
            'meta': ['채널 씨모어', '원문 %d편' % len(d.get('sources') or []),
                     '%s ~ %s' % (dates[0], dates[-1]) if dates else ''],
            'oneliner': lead,
            'points': points_of(d),
            'figs': [(0, d['chain_name'], svg, cap)],
            'stats': stats_of(d),
            'clash': clash_of(d),
            'note': note_of(d, kids.get(d['canon_slug'], [])),
            'links': [],
            'date': dates[-1] if dates else '',
            '_file': d['canon_slug'],
        })
    return cards


HEADER = '''  <header>
    <p class="eyebrow">채널 씨모어 전사 117편에서 뽑은 밸류체인</p>
    <h1>체인 인사이트</h1>
  </header>'''

if __name__ == '__main__':
    cards = load()
    n_sec = len({c['section'][0] for c in cards})
    n_st = sum(len(c['points']) for c in cards)
    dates = sorted(c['date'] for c in cards if c['date'])
    FOOTER = ('<p class="lede">한 카드가 밸류체인 하나입니다. 마디마다 원문이 이름을 댄 회사와, '
              '원문이 진입장벽·문지기라고 지목한 자리만 실었습니다. 진행자가 회차를 거치며 판단을 '
              '바꾼 자리는 덮지 않고 날짜와 함께 둘 다 남겼습니다.</p>'
              '<div class="meta-row"><span>사슬 <b>%d</b></span><span>마디 <b>%d</b></span>'
              '<span>섹션 <b>%d</b></span><span>원문 <b>117편 전수</b></span></div>'
              '\n제3자 해설 요약 아카이브 · 원문은 싣지 않습니다. 투자 추천이 아닙니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_chain_dashboard.py</code>'
              % (len(cards), n_st, n_sec))
    dc.render(cards, '체인 인사이트', HEADER, FOOTER, OUT,
              page_slug='chain',
              search_ph='산업·회사·마디로 찾기', extra_css=CSS,
              newest_first=True)
    print('사슬 %d · 마디 %d · 섹션 %d · %s ~ %s'
          % (len(cards), n_st, n_sec, dates[0], dates[-1]))
    print(OUT)
