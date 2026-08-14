# -*- coding: utf-8 -*-
"""통합 인사이트 — 주제 대시보드에 흩어진 카드를 한 장에 모은다.

카드를 다시 쓰지 않는다. 이미 만들어진 대시보드 HTML에서 `.ucard` 블록을 그대로
떼어와 소스 표시(`data-src`)만 붙이고 주제 축으로 다시 묶는다. 그래서 각 대시보드에서
카드를 고치면 그 생성기를 돌린 뒤 이 파일만 다시 돌리면 반영된다.

  py -3.13 scripts/gen_unified.py

미국주식 사관학교가 섞여 있으므로 이 페이지는 공개하지 않는다
(functions/_middleware.js 의 PROTECTED, scripts/gen_site.py 의 locked=True).
"""
import io
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scratchpad'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import dash_common as dc  # noqa: E402

DASH = os.path.join(ROOT, '대시보드')
OUT = os.path.join(DASH, '통합 인사이트.html')

# 소스: 파일명 -> (id, 배지 라벨, 짧은 이름)
SOURCES = [
    ('언더스탠딩 대시보드.html', ('energy', '⚡ AI · 인프라 · 에너지', '에너지')),
    ('부동산 대시보드.html', ('estate', '🏠 부동산', '부동산')),
    ('금융 대시보드.html', ('finance', '💵 금융', '금융')),
    ('미국주식 사관학교 대시보드.html', ('usa', '🎓 미국주식 사관학교', '미주사')),
]

# 통합 주제 축: (id, 번호, 제목, 한 줄) — 원래 섹션 제목을 이쪽으로 옮긴다
AXES = [
    ('u-ai', '01', 'AI · 반도체 · 데이터센터',
     'AI에 들어간 돈이 어디로 가고 무엇이 병목인가. 메모리·광통신·전력망까지'),
    ('u-energy', '02', '에너지 · 전력 · 원자재',
     '전기와 기름이 어디서 모자라고 값이 어떻게 정해지나. 원전과 재생에너지, 중동까지'),
    ('u-macro', '03', '거시 · 금리 · 환율',
     '금리와 환율, 물가·고용 지표에서 무엇이 일회성이고 무엇이 구조인가'),
    ('u-market', '04', '시장 국면 · 투자 방법론',
     '누가 무엇을 보고 사고파는지, 그리고 공개 자료로 남의 판단을 읽는 법'),
    ('u-estate', '05', '부동산 · 주거',
     '집이 얼마나 나오고 세금이 어떻게 매겨지나. 전세·재개발·건설 원가까지'),
]

# 원래 섹션 제목 -> 통합 축. 새 섹션이 생기면 여기에 한 줄 추가한다
AXIS_OF = {
    'AI · 데이터센터 전력': 'u-ai',
    '반도체 · 메모리': 'u-ai',
    '반도체 · 전력 · 광통신': 'u-ai',
    'AI 자본 사이클 · 리스크': 'u-ai',
    '재생에너지 · 원전 · 소재': 'u-energy',
    '전력요금 · 시장 메커니즘': 'u-energy',
    '원유 수급 · 정유': 'u-energy',
    '중동 전쟁 · 지정학': 'u-energy',
    '거시 · 금리 · 환율': 'u-macro',
    '금리 · 국채': 'u-macro',
    '환율 · 달러': 'u-macro',
    '환율 · 지표 · 연준': 'u-macro',
    '시장 국면 · 수급': 'u-market',
    '고르는 틀 · 방법론': 'u-market',
}
ESTATE_DEFAULT = 'u-estate'   # 부동산 대시보드의 섹션은 전부 부동산 축으로 간다


def blocks(html, cls):
    """<div class="cls ...">…</div> 를 중첩 깊이를 세어 통째로 떼어낸다"""
    out = []
    for m in re.finditer(r'<div class="%s\b' % cls, html):
        i, depth = m.start(), 0
        for t in re.finditer(r'<div\b|</div>', html[i:]):
            depth += 1 if t.group(0) != '</div>' else -1
            if depth == 0:
                out.append(html[i:i + t.end()])
                break
    return out


def harvest():
    """각 대시보드에서 (축, 소스, 원래 섹션 제목, 카드 HTML) 을 모은다"""
    cards = []
    for fname, (sid, badge, short) in SOURCES:
        html = io.open(os.path.join(DASH, fname), encoding='utf-8').read()
        # 페이지마다 줄바꿈·들여쓰기가 달라서(에너지 페이지는 생성기가 없다) 느슨하게 잡는다
        for sec in re.finditer(
                r'<section id="[^"]+">\s*<div class="sec-head">\s*'
                r'<span class="sec-num">\d+</span>\s*<h2 class="sec-title">(.*?)</h2>\s*</div>',
                html):
            title = sec.group(1)
            body = html[sec.end():html.index('</section>', sec.end())]
            axis = AXIS_OF.get(title, ESTATE_DEFAULT if sid == 'estate' else None)
            if axis is None:
                print('  ! 축을 못 정한 섹션: %s (%s)' % (title, short))
                axis = 'u-market'
            for card in blocks(body, 'ucard'):
                cards.append((axis, sid, badge, short, title, card))
    return cards


def tag(card, sid, badge, sec_title):
    """카드에 소스 표시와 배지를 박는다. 접힌 상태에서도 어디서 온 편인지 보이게"""
    card = card.replace('<div class="ucard', '<div data-src="%s" class="ucard' % sid, 1)
    chip = ('<span class="usrc">%s</span>' % badge)
    # 주제칩 앞에 소스 배지를 세운다(주제칩은 원래 대시보드의 분류라 그대로 둔다)
    card = re.sub(r'(<div class="uc-head"[^>]*>)', r'\1' + chip, card, count=1)
    # 원래 섹션 제목은 접힌 카드에서 빠지므로 메타에 남긴다
    return card.replace('<div class="uc-meta">', '<div class="uc-meta"><span>%s</span>' % sec_title, 1)


EXTRA = """
<style>
  /* unified:start — 통합 인사이트에서만 쓰는 규칙 */
  .usrc{display:inline-block; margin:0 8px 6px 0; padding:2px 9px; border-radius:999px;
    font-size:.68rem; font-weight:800; letter-spacing:.02em;
    color:var(--ink-2, var(--sub)); background:var(--chip, var(--accent-soft)); white-space:nowrap;}
  .srctabs{display:flex; flex-wrap:wrap; gap:6px; margin:0 0 16px;}
  .srctabs button{font:inherit; font-size:.78rem; font-weight:700; padding:6px 12px;
    border:1px solid var(--line); border-radius:999px; background:transparent;
    color:var(--ink-2, var(--sub)); cursor:pointer;}
  .srctabs button[aria-pressed="true"]{border-color:var(--accent); color:var(--accent);}
  .srctabs .cnt{margin-left:6px; font-variant-numeric:tabular-nums; opacity:.7;}
  .ujump{display:flex; flex-wrap:wrap; gap:8px 14px; margin:0 0 22px; font-size:.78rem;}
  .ujump a{color:var(--ink-3, var(--sub)); text-decoration:none; font-weight:700;}
  .ujump a:hover{color:var(--accent);}
  /* unified:end */
</style>"""

SRC_JS = """<script>
(function(){
  var tabs=document.querySelector('.srctabs'); if(!tabs) return;
  var pick='all';
  function apply(){
    document.querySelectorAll('.ucard[data-src]').forEach(function(c){
      c.hidden = !(pick==='all' || c.dataset.src===pick);
    });
    document.querySelectorAll('section[id]').forEach(function(s){
      var live=s.querySelectorAll('.ucard:not([hidden])').length;
      s.hidden = live===0;
      var jump=document.querySelector('.ujump a[href="#'+s.id+'"]');
      if(jump){ jump.hidden = live===0; jump.querySelector('.jn').textContent=live; }
    });
    tabs.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.src===pick));
    });
  }
  tabs.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    pick=b.dataset.src; apply();
    window.scrollTo({top:0, behavior:'smooth'});
  });
  apply();
})();
</script>"""


def main():
    cards = harvest()
    by_axis = {}
    for axis, sid, badge, short, sec_title, card in cards:
        by_axis.setdefault(axis, []).append(tag(card, sid, badge, sec_title))
    per_src = {}
    for _a, sid, _b, short, _t, _c in cards:
        per_src[sid] = per_src.get(sid, 0) + 1

    tabs = ['<button data-src="all" aria-pressed="true">전체 <span class="cnt">%d</span></button>' % len(cards)]
    tabs += ['<button data-src="%s" aria-pressed="false">%s <span class="cnt">%d</span></button>'
             % (sid, badge, per_src.get(sid, 0)) for _f, (sid, badge, _s) in SOURCES]

    jump, body = [], []
    for aid, num, title, sub in AXES:
        cs = by_axis.get(aid, [])
        if not cs:
            continue
        jump.append('<a href="#%s">%s <span class="jn">%d</span></a>' % (aid, title, len(cs)))
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2></div>%s</section>'
                    % (aid, num, title, ''.join(cs)))

    header = '''  <header>
    <p class="eyebrow">주제 대시보드 넷을 한 장으로</p>
    <h1>통합 인사이트</h1>
    <p class="lede">에너지·부동산·금융·미국 증시 대시보드에 올라간 카드를 주제 축으로 다시 묶었습니다.
       카드 내용은 각 대시보드와 같고, 여기서는 <b>어디서 온 편인지</b>와 <b>무엇과 같은 줄에 서는지</b>를 봅니다.</p>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d건</b></span>
      <span>소스 <b>%d곳</b></span>
    </div>
  </header>''' % (date.today().isoformat(), len(cards), len(SOURCES))

    footer = ('카드 원본은 각 주제 대시보드에 있습니다. 이 페이지는 '
              '<code>scripts/gen_unified.py</code> 가 그 HTML에서 카드를 떼어와 다시 묶습니다.<br>'
              '  주제 대시보드를 다시 만든 뒤 이 파일을 돌려야 최신 상태가 됩니다.')

    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>통합 인사이트</title>\n' + dc.css() + EXTRA
            + '\n<div class="wrap">\n' + header
            + '\n\n  <div class="srctabs">' + ''.join(tabs) + '</div>'
            + '\n\n  <div class="ujump">' + ''.join(jump) + '</div>\n\n  '
            + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n' + dc.FOLD_JS + SRC_JS + '\n')
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 축 %d개 -> %s' % (len(cards), len(by_axis), OUT))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
    for _f, (sid, _b, short) in SOURCES:
        print('  %-8s %d' % (short, per_src.get(sid, 0)))


if __name__ == '__main__':
    main()
