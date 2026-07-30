# 언더스탠딩 대시보드 카드를 산업별로 재편 + 각 그룹 최신순 정렬
import re, io

F = r"C:\Users\y\semianalysis\대시보드\언더스탠딩 대시보드.html"
html = io.open(F, encoding="utf-8").read()

# 통합 인사이트 섹션·칩은 gen_insights.py 소관 — regroup 영역에서 제외(gen_insights가 나중에 재생성)
html = re.sub(r'<!-- INSIGHTS:START -->.*?<!-- INSIGHTS:END -->\n*', '', html, flags=re.DOTALL)
html = re.sub(r'[ \t]*<a href="#sec-insights">.*?</a>\n', '', html)

# 카드 영역 = 첫 <section> ~ footer 직전 </section>
m_start = html.index("  <section")
m_foot = html.index("  <footer>")
# footer 앞의 마지막 </section>
sec_close = html.rindex("</section>", 0, m_foot)
region = html[m_start:sec_close + len("</section>")]
before = html[:m_start]
after = html[sec_close + len("</section>"):]
# 기존 점프 내비 제거(재실행 멱등성)
before = re.sub(r'  <nav class="sec-nav">.*?</nav>\n\n', '', before, flags=re.DOTALL)

# 카드 추출: <div class="ucard"> ~ 4-space </div>
cards = re.findall(r'    <div class="ucard">.*?\n    </div>', region, re.DOTALL)
assert len(cards) == 25, f"카드 수 이상: {len(cards)}"

def date_of(card):
    return re.search(r'(\d{4}-\d{2}-\d{2})', card).group(1)

def title_of(card):
    return re.search(r'<h2[^>]*>(.*?)(?:<span|</h2>)', card, re.DOTALL).group(1)

# 산업 버킷 배정 (제목 부분일치, 위에서부터 우선)
BUCKETS = [
    ("ai",       ["미국 데이터센터 전력난", "지금 에너지 투자"]),
    ("renew",    ["삼성까지 뛰어들었다", "싼 전기 시대", "독일 신재생", "은 가격 급등"]),
    ("pmarket",  ["태양광 세배", "원전만으로는", "서울-지방"]),
    ("semi",     ["반도체 룰이 바뀌었다", "호남 반도체"]),
    ("war",      ["이란 전쟁 오늘", "석유 치킨게임", "하르그섬", "미군은 이란", "베네수엘라"]),
    ("macro",    ["경제 교과서 틀렸다", "환율 오른다고"]),
    ("oilsupply",["호르무즈 막히는 것보다", "중동산 기름", "대만 LNG", "15억 인구", "호르무즈 막히자 10조", "전쟁 끝나도 계속 간다"]),
]
def bucket(card):
    t = title_of(card)
    for key, kws in BUCKETS:
        if any(k in t for k in kws): return key
    raise SystemExit(f"미분류 카드: {t}")

buckets = {k: [] for k, _ in BUCKETS}
for c in cards:
    buckets[bucket(c)].append(c)
for k in buckets:
    buckets[k].sort(key=date_of, reverse=True)

SECTIONS = [
    ("01", "AI · 데이터센터 전력", "AI 데이터센터 전력난 · 에너지 인프라 투자 — 권효재", "ai", "AI·DC전력"),
    ("02", "재생에너지 · 원전 · 소재", "재생/원전 정책 · 에너지 전환 소재(은) — 국내외", "renew", "재생·원전"),
    ("03", "전력요금 · 시장 메커니즘", "SMP · 지역 차등요금 · 태양광 시스템 비용 — 백브리핑", "pmarket", "전력요금·시장"),
    ("04", "원유 수급 · 정유", "호르무즈·홍해 항로 · 원유 다변화 · LNG·자원 확보", "oilsupply", "원유수급"),
    ("05", "중동 전쟁 · 지정학", "이란 전쟁 · 셧인·하르그 · 미사일 소모전 · 베네수엘라", "war", "중동전쟁"),
    ("06", "반도체 · 메모리", "메모리 리레이팅 · 호남 반도체 산단 전력 해법 — 이선엽", "semi", "반도체"),
    ("07", "거시 · 금리 · 환율", "국채·물가가 지배하는 금리 · 달러가 끌고 가는 환율 — 류상철", "macro", "거시·금리"),
]

# 섹션 점프 내비
nav = ['  <nav class="sec-nav">']
for num, title, sub, key, chip in SECTIONS:
    nav.append(f'    <a href="#sec-{key}">{chip} <b>{len(buckets[key])}</b></a>')
nav.append("  </nav>\n")

out = ["\n".join(nav)]
for num, title, sub, key, chip in SECTIONS:
    out.append(f'  <section id="sec-{key}">')
    out.append(f'    <div class="sec-head"><span class="sec-num">{num}</span><h2 class="sec-title">{title}</h2></div>')
    out.append(f'    <p class="sec-sub">{sub}</p>\n')
    out.append("\n".join(buckets[key]))
    out.append("  </section>\n")
new_region = "\n".join(out).rstrip("\n") + "\n"

io.open(F, "w", encoding="utf-8").write(before + new_region + after)
print("OK: " + " ".join("%s=%d" % (k, len(v)) for k, v in buckets.items()))
