# -*- coding: utf-8 -*-
# 카드 형식 비교용 미리보기. 같은 편(마곡 토지임대부)을 두 형식으로 나란히 놓는다.
#   왼쪽  = 지금 부동산 형식(gain·표·반론·메모 포함, 접힘)
#   오른쪽 = AI · 인프라 · 에너지 형식(한 줄짜리 포인트 6개 + 숫자 4개 + 인용, 항상 펼침)
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import gen_realestate_dashboard as g

NEW = [c for c in g.CARDS if c['title'] == '3억 4천만 원짜리 마곡 아파트'][0]

# 옛 형식으로 다시 쓴 같은 편 — 포인트는 한 줄, 숫자는 넷, 인용 한 줄
OLD = '''<div class="ucard">
  <span class="uc-topic market">토지임대부 · 공공분양</span>
  <h2>3억 4천만 원짜리 마곡 아파트</h2>
  <div class="uc-meta">
    <span>백종훈 <b>언더스탠딩 기자</b></span>
    <span>2026-03-23</span>
    <span>42분</span>
    <span>언더스탠딩</span>
  </div>
  <p class="uc-oneliner">땅은 SH가 갖고 건물만 파는 토지임대부 아파트가 서울에 14년 만에 나왔다. 전용 59㎡가 3억 4천만 원에 월 토지임대료 66만 원, 옆 단지 같은 면적은 16억 원대다.</p>

  <p class="uc-label">핵심 포인트</p>
  <ul class="uc-points">
    <li><b>전세 보증금보다 싸다.</b> 분양가 3억 4천만 원, 인근 전세 보증금 6억 원. 대신 땅은 끝까지 공공 소유다.</li>
    <li><b>14년 만의 재등장.</b> 로또 논란으로 접었던 방식인데 LH·SH가 택지를 팔지 말고 직접 지으라는 주문으로 되살아났다.</li>
    <li><b>10년 뒤엔 팔 수 있다.</b> 5년 실거주·10년 전매제한만 지키면 매매와 증여가 자유롭다. 2012년 강남브리즈힐은 2억대에서 12억대가 됐다.</li>
    <li><b>40년 뒤가 진짜 쟁점.</b> 재건축 때 토지 소유자는 정당한 이유 없이 거부할 수 없고, 합의하면 매각으로 전환할 길도 열려 있다.</li>
    <li><b>공공에는 남는 게 없다.</b> 토지임대료를 공공성 때문에 낮게 설계해 땅만 쥐고 현금흐름이 안 생긴다. LH 부채는 160조 원.</li>
    <li><b>물량이 문제다.</b> 381가구에 경쟁률 100대 1. 시세를 누르는 효과가 아니라 당첨된 소수의 혜택에 가깝다.</li>
  </ul>

  <p class="uc-label">주요 숫자</p>
  <div class="stat-grid">
    <div class="stat"><div class="s-val">3억 4천만 원 + 월 66만 원</div><div class="s-label">전용 59㎡ 분양가와 토지임대료(인근 매매 16억 원대)</div></div>
    <div class="stat"><div class="s-val">5년 · 10년 · 40년</div><div class="s-label">실거주 의무 · 전매제한 · 토지 임대 기간</div></div>
    <div class="stat"><div class="s-val">2억 → 12억 원</div><div class="s-label">2012년 강남브리즈힐 분양가와 현재 시세</div></div>
    <div class="stat"><div class="s-val">160조 원</div><div class="s-label">LH 부채. 토지주택은행 신설안이 거론된다</div></div>
  </div>

  <p class="uc-quote">"토지 소유자는 정당한 이유 없이 거부할 수 없다." 40년 뒤 재건축 규정이다. "저 빚이나 이 빚이나 전부 다 정부이긴 하다." 토지주택은행 안에 대한 평가다.</p>

  <div class="uc-links">
    <a href="https://youtu.be/Vfpfkvvmy9U" target="_blank" rel="noopener">▶ 유튜브 원본</a>
  </div>
</div>'''

CSS = '''
<style>
  .cmp{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
  @media (max-width:900px){.cmp{grid-template-columns:1fr}}
  .cmp h3{font-size:13px;letter-spacing:.04em;color:var(--ink-3);margin:0 0 10px;font-weight:800}
  .cmp .tag{display:inline-block;padding:3px 9px;border-radius:999px;background:var(--sunk);
            color:var(--ink-2);font-size:11px;font-weight:700;margin-left:6px}
</style>'''

HTML = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>카드 형식 비교</title>\n' + dc.css() + CSS + '''
<div class="wrap">
  <header>
    <p class="eyebrow">형식 비교</p>
    <h1>같은 편, 두 형식</h1>
    <p class="lede">마곡 토지임대부 편 하나를 지금 부동산 형식과 AI · 인프라 · 에너지 형식으로 각각 써 봤습니다.
       왼쪽은 접힌 채로 고르는 구조라 정보가 많고, 오른쪽은 한 화면에서 다 읽히게 짧습니다.</p>
  </header>

  <div class="cmp">
    <div>
      <h3>지금 부동산 형식 <span class="tag">gain · 표 · 반론 · 메모</span></h3>
      ''' + dc.card_html(NEW).replace('ucard is-fold', 'ucard') + '''
    </div>
    <div>
      <h3>AI · 인프라 · 에너지 형식 <span class="tag">포인트 6 · 숫자 4 · 인용</span></h3>
      ''' + OLD + '''
    </div>
  </div>
</div>
''' + dc.FOLD_JS + '\n')

OUT = os.path.join(dc.ROOT, 'scratchpad', 'preview_fmt.html')
io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK ->', OUT, len(HTML))
