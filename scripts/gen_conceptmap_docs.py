#!/usr/bin/env python
# 개념 지도 각 모듈 패널의 "관련 문서" 슬롯 자동 생성.
# content/newsletter 변환본을 categories·제목 키워드로 6개 모듈(패널)에 매핑 →
# 개념 지도 HTML의 <!--DOCS:key--> ~ <!--/DOCS:key--> 구간을 재생성.
# 사용: python scripts/gen_conceptmap_docs.py
import io, sys, os, re, glob, urllib.parse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
NLDIR = "content/newsletter"
PAGE = r"대시보드\개념 지도 — LLM 계층·병렬화.html"
GH = "https://github.com/yohan4477/semi-report/blob/main/"

# 모듈 key → (categories 조각, 제목/카테고리 키워드)
PANELS = [
 ("jang", ["/rl", "/agents"], ["추론", "inference", "학습", "강화학습", "사전학습", "cpx", "토큰", "코딩 어시스턴트", "claude code", "trainium", "inferencemax", "inferencex"]),
 ("attn", [],                 ["deepseek", "어텐션", "attention", "kimi", "kv"]),
 ("mlp",  [],                 ["moe", "deepseek", "advancing ai", "mixture"]),
 ("par",  [],                 ["nvl72", "gb200", "gb300", "h100", "베라 루빈", "vera rubin", "벤치마크"]),
 ("phys", ["/power", "/cooling", "/networking", "/memory"], ["데이터센터 해부", "800vdc", "전력", "냉각", "nvlink", "인터커넥트", "hbm", "메모리", "ectc", "isscc", "cxmt"]),
 ("prec", [],                 ["blackwell", "텐서 코어", "코디자인", "tpuv7", "inferencex", "inferencemax", "정밀도", "nvfp4", "루빈 cpx"]),
]
CAP = 6  # 모듈당 최대 문서 수

def scan():
    posts = []
    for path in glob.glob(NLDIR + "/**/*.md", recursive=True):
        fn = os.path.basename(path)
        m = re.match(r"\[(\d{6})\]\s+(.+)\.md$", fn)
        if not m: continue
        rel = path.replace("\\", "/")
        txt = open(path, encoding="utf-8").read(2500)
        cm = re.search(r"categories:\s*\[([^\]]+)\]", txt)
        cats = (cm.group(1) if cm else "").lower()
        posts.append({"date": m.group(1), "title": m.group(2), "rel": rel,
                      "cats": cats, "hay": (m.group(2) + " " + cats).lower()})
    return posts

def match(cats, kw, p):
    return any(c in p["cats"] for c in cats) or any(k.lower() in p["hay"] for k in kw)

def blob(rel): return GH + urllib.parse.quote(rel)

posts = scan()
html = open(PAGE, encoding="utf-8").read()
total = 0
for key, cats, kw in PANELS:
    hits = sorted([p for p in posts if match(cats, kw, p)], key=lambda x: x["date"], reverse=True)[:CAP]
    if hits:
        links = " · ".join('<a href="' + blob(p["rel"]) + '" target="_blank" rel="noopener">' + p["title"] + "</a>" for p in hits)
    else:
        links = '<span class="empty">해당 변환본 없음</span>'
    total += len(hits)
    html = re.sub(r"<!--DOCS:" + key + r"-->.*?<!--/DOCS:" + key + r"-->",
                  "<!--DOCS:" + key + "-->" + links + "<!--/DOCS:" + key + "-->",
                  html, flags=re.S)

open(PAGE, "w", encoding="utf-8").write(html)
print("posts:", len(posts), "| doc links injected:", total, "| panels:", len(PANELS))
