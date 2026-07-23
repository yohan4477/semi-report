#!/usr/bin/env python
# 개념 지도 "코퍼스 인덱스" 자동 생성 — content/newsletter 변환본을 개념별로 매핑.
# 파일명 [YYMMDD] + 제목 + categories 프론트매터로 각 개념에 매칭 → 개념 지도 HTML의
# <!--CONCEPTDOCS_START--> ~ <!--CONCEPTDOCS_END--> 구간을 재생성.
# 사용: python scripts/gen_conceptmap_docs.py
import io, sys, os, re, glob, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
NLDIR = "content/newsletter"
PAGE = r"대시보드\개념 지도 — LLM 계층·병렬화.html"
GH = "https://github.com/yohan4477/semi-report/blob/main/"

# 개념(개념 지도 파트 순서와 대응) → (categories 조각, 제목/카테고리 키워드)
CONCEPTS = [
 ("학습 · RL",              ["/rl"],          ["강화학습", "사전학습", "world record", "trainium", "학습"]),
 ("추론 · Prefill/Decode",  ["/agents"],      ["추론", "inference", "cpx", "토큰", "코딩 어시스턴트", "claude code", "inferencemax", "inferencex"]),
 ("어텐션 · MoE",           [],               ["deepseek", "moe", "advancing ai", "어텐션", "mixture"]),
 ("병렬 · NVL72 · 벤치",     [],               ["nvl72", "gb200", "gb300", "h100", "베라 루빈", "vera rubin", "벤치마크"]),
 ("GPU 구조 · 정밀도",       [],               ["텐서 코어", "blackwell", "코디자인", "tpuv7", "inferencex", "inferencemax", "정밀도", "nvfp4"]),
 ("네트워크 · 스케일업/아웃", ["/networking"],  ["nvlink", "인터커넥트", "네트워크", "800vdc"]),
 ("물리 · 랙 · 전력 · 냉각",  ["/power", "/cooling"], ["데이터센터 해부", "800vdc", "전력", "냉각", "가스", "발전", "그리드"]),
 ("메모리 · HBM",           ["/memory"],      ["hbm", "메모리", "ectc", "isscc", "cxmt", "낸드", "dram"]),
]
CAP = 8  # 개념당 최대 문서 수

def scan():
    posts = []
    for path in glob.glob(NLDIR + "/**/*.md", recursive=True):
        fn = os.path.basename(path)
        m = re.match(r"\[(\d{6})\]\s+(.+)\.md$", fn)
        if not m: continue
        rel = path.replace("\\", "/")
        txt = open(path, encoding="utf-8").read(2500)
        cm = re.search(r"categories:\s*\[([^\]]+)\]", txt)
        posts.append({
            "date": m.group(1), "title": m.group(2), "rel": rel,
            "cats": (cm.group(1) if cm else "").lower(),
            "hay": (m.group(2) + " " + (cm.group(1) if cm else "")).lower(),
        })
    return posts

def match(concept_cats, concept_kw, p):
    if any(c in p["cats"] for c in concept_cats): return True
    if any(k.lower() in p["hay"] for k in concept_kw): return True
    return False

def blob(rel): return GH + urllib.parse.quote(rel)

def render(posts):
    out = []
    for name, cats, kw in CONCEPTS:
        hits = [p for p in posts if match(cats, kw, p)]
        hits.sort(key=lambda x: x["date"], reverse=True)
        hits = hits[:CAP]
        if not hits: continue
        links = " · ".join('<a href="' + blob(p["rel"]) + '" target="_blank" rel="noopener">' + p["title"] + "</a>" for p in hits)
        out.append('    <div class="ir"><span class="c">' + name + '</span><div>' + links + " <span class=\"date\">" + str(len(hits)) + "편</span></div></div>")
    return "\n".join(out)

posts = scan()
block = render(posts)
html = open(PAGE, encoding="utf-8").read()
new = re.sub(r"<!--CONCEPTDOCS_START-->.*?<!--CONCEPTDOCS_END-->",
             "<!--CONCEPTDOCS_START-->\n" + block + "\n    <!--CONCEPTDOCS_END-->",
             html, flags=re.S)
assert new != html and "CONCEPTDOCS_START" in new, "marker not found"
open(PAGE, "w", encoding="utf-8").write(new)
print("posts:", len(posts), "| concept rows:", block.count('class="ir"'))
