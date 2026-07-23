#!/usr/bin/env python
# 인텔리전스 대시보드 ① 소셜 신호 = 소셜 신호 히스토리의 최근분 미러(B안).
# 히스토리 최근 N일 day-group을 자동 파싱 → ① 재생성(LI/YT/뉴스레터 3소스 + NVIDIA 1차 인터리브 + 클러스터 관련 펼침).
# 사용: python scripts/gen_bmirror.py [일수(기본 14)]
# linkedin-update로 히스토리 갱신 후 이 스크립트를 돌리면 ①이 자동 동기됨.
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HIST = r"대시보드\소셜 신호 히스토리.html"
DASH = r"대시보드\인텔리전스 대시보드.html"
DAYS_WINDOW = int(sys.argv[1]) if len(sys.argv) > 1 else 14

hs = open(HIST, encoding="utf-8").read()

def all_days():
    return [m.group(1) for m in re.finditer(r'<h3>(2026-\d\d-\d\d)</h3>', hs)]

def extract(d):
    m = re.search(r'<h3>' + d + r'</h3>(.*?)(?=<div class="day"><h3>|\Z)', hs, re.S)
    block = m.group(1) if m else ""
    rows = []
    for rm in re.finditer(r'<div class="row"><a class="rowmain" href="([^"]+)"[^>]*>.*?<span class="sn">(.*?)</span></a>(.*?)</div>', block, re.S):
        href, sn, tail = rm.group(1), re.sub(r"\s+", " ", rm.group(2)).strip(), rm.group(3)
        typ = "yt" if ("youtube" in href or "youtu.be" in href) else "li"
        art = re.search(r'<a class="art" href="([^"]+)"', tail)
        arturl = art.group(1) if art else None
        artkind = ("yt" if arturl and ("youtube" in arturl or "youtu.be" in arturl) else ("nl" if arturl and "newsletter" in arturl else None))
        rows.append({"typ": typ, "href": href, "sn": sn, "art": arturl, "artkind": artkind})
    return rows

def nv(url, sn, ext=True, brief=False):
    return {"typ": "nv", "href": url, "sn": sn, "art": None, "artkind": None, "ext": ext, "brief": brief}
def L(a): return "https://www.linkedin.com/feed/update/urn:li:activity:" + a + "/"

# NVIDIA 1차(블로그·ai-infra) 오버레이 — 날짜별. 새로 생기면 여기에 추가.
NVROWS = {
 "2026-07-22": [
   nv(L("7485709351870107649"), "CoreWeave, Vera Rubin NVL72 배치 — 랙당 1.64Pb/s Spectrum-X 결합, Rubin 첫 대규모 클라우드 배치 (nvidia-ai-infra)"),
   nv(L("7485496316068802560"), "Wistron 포트워스 신공장 — GB300·Vera Rubin 미국 생산, AI 서버 공급망 이전 (nvidia-ai-infra)"),
 ],
 "2026-07-21": [
   nv("https://developer.nvidia.com/blog/setting-a-world-record-for-moe-pre-training-on-nvidia-gb300-nvl72/", "MoE 사전학습 세계기록 — GB300 NVL72, 프론티어 학습 성능 입증 (NVIDIA 블로그)"),
   nv("기술 브리핑 — NVIDIA Rubin.html", "Rubin GPU·Vera CPU 아키텍처 공개 — HBM4 288GB·Vera 88코어 커스텀 CPU·LPDDR5X (임원 브리핑)", ext=False, brief=True),
 ],
 "2026-07-20": [
   nv("https://developer.nvidia.com/blog/nvidia-nvlink-the-scale-up-network-for-ai-factories/", "NVLink — AI 팩토리용 스케일업 네트워크, Rubin NVLink 6(3.6TB/s) 맥락 (NVIDIA 블로그)"),
 ],
 "2026-07-16": [
   nv("https://developer.nvidia.com/blog/scaling-agentic-ai-factories-through-extreme-co-design-with-nvidia-bluefield/", "BlueField 코디자인으로 에이전틱 인프라 확장 — DPU 극단 코디자인 (NVIDIA 블로그)"),
 ],
}
BRIEF = "기술 브리핑 — NVIDIA Rubin.html"
NEWS = "https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference"
# 클러스터 관련(직접참조 위에 얹는 테마 연결) — href 키.
REL = {
 BRIEF: [(L("7485709351870107649"), "배치", "CoreWeave 첫 대규모 배치 1.64Pb/s"), (NEWS, "TCO", "뉴스레터: VR NVL72 vs GB200 perf/MW 5.4배"), (L("7485016913086095360"), "압축", "Rubin LUT-B 압축 벤치=Kimi K3 2.8T")],
 L("7485771399756673024"): [(L("7483981685408165888"), "모델", "Kimi K3 코딩 프론티어 추월(07-18)"), (L("7483732333850935296"), "HW", "Kimi K3 2.8T FP4 단일 B200 불가(07-17)"), (BRIEF, "Rubin", "Rubin LUT-B 압축이 Kimi로 벤치→브리핑")],
 L("7485709351870107649"): [(BRIEF, "Rubin", "Vera Rubin NVL72 스펙→임원 브리핑"), (NEWS, "검증", "SemiAnalysis가 이 벤치 재검증(뉴스레터)")],
}

LI_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M7.1 9.2H4.7V19h2.4zM5.9 4.8a1.45 1.45 0 100 2.9 1.45 1.45 0 000-2.9zM19.3 13.4c0-2.9-1.6-4.4-3.7-4.4-1.7 0-2.4 1-2.8 1.6V9.2h-2.4V19h2.4v-5.2c0-1.4.6-2.2 1.8-2.2 1.1 0 1.6.8 1.6 2.2V19h2.4z"/></svg>'
YT_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#c00"/><path fill="#fff" d="M10 8.5l6 3.5-6 3.5z"/></svg>'
NV_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="4" fill="#76b900"/><text x="12" y="15.5" font-size="8.5" font-weight="700" fill="#fff" text-anchor="middle" font-family="Arial,sans-serif">NV</text></svg>'
def icon(t): return {"li": LI_SVG, "yt": YT_SVG, "nv": NV_SVG}[t]
def cat_for(sn):
    if any(k in sn for k in ["프라임파워", "왕복엔진", "전력", "허가", "그리드", "Bloom", "스타게이트"]): return "power"
    if any(k in sn for k in ["HBM", "메모리", "DRAM", "LPDDR", "낸드", "NAND"]): return "memory"
    if any(k in sn for k in ["Kimi", "Nemotron", "Fable", "Claude", "Groq", "Llama", "모델"]): return "model"
    return "compute"

def render_row(r):
    sn = r["sn"]
    if " — " in sn: title, desc = sn.split(" — ", 1)
    elif "—" in sn: title, desc = sn.split("—", 1)
    else: title, desc = sn, ""
    title, desc = title.strip(), desc.strip()
    href = r["href"]; ext = r.get("ext", True); typ = r["typ"]
    at = ' target="_blank" rel="noopener"' if (ext and href.startswith("http")) else ""
    brief_badge = ' <span class="delta new">브리핑</span>' if r.get("brief") else ""
    artb = ""
    if r.get("art"):
        k = r["artkind"]; lbl = "▶ YouTube" if k == "yt" else "▤ 뉴스레터 원문"
        cls = "ybadge" if k == "yt" else "nbadge"
        artb = '<a class="' + cls + '" href="' + r["art"] + '" target="_blank" rel="noopener">' + lbl + "</a>"
    rel = REL.get(href); relb = ""
    if rel:
        links = "".join('<a href="' + u + ('" target="_blank" rel="noopener"' if u.startswith("http") else '"') + '><span class="rk">' + rk + "</span>" + why + "</a>" for u, rk, why in rel)
        relb = '<button class="relb" aria-expanded="false"><span class="car">▸</span> 관련 ' + str(len(rel)) + '</button><div class="rell">' + links + "</div>"
    dline = ('<div class="d">' + desc + "</div>") if desc else ""
    cat = cat_for(sn)
    return ('<div class="sig" data-c="' + cat + '"><span class="srci">' + icon(typ) + "</span>"
            '<div><div class="t"><a href="' + href + '"' + at + ">" + title + "</a>" + brief_badge + "</div>" + dline + artb + relb + "</div></div>")

days = all_days()[:DAYS_WINDOW]
out = ""
for d in days:
    rows = extract(d) + NVROWS.get(d, [])
    if not rows: continue
    out += '    <div class="day">\n      <h3>' + d[5:] + '</h3>\n      ' + "\n      ".join(render_row(r) for r in rows) + "\n    </div>\n"

ds = open(DASH, encoding="utf-8").read()
start = ds.find('    <div class="day">\n      <h3>')
note_i = ds.find('    <div class="note" data-c="compute memory power model">', start)
assert start != -1 and note_i != -1, (start, note_i)
note_end = ds.find("</div>", note_i) + len("</div>")
newnote = '    <div class="note" data-c="compute memory power model">히스토리 미러(최근 ' + str(len(days)) + '일) · LinkedIn·YouTube·뉴스레터 + NVIDIA 1차 — 전체는 위 "전체 보기"</div>'
ds = ds[:start] + out + newnote + ds[note_end:]
open(DASH, "w", encoding="utf-8").write(ds)
print("days:", len(days), "| sig rows:", out.count('class="sig"'), "| div", ds.count("<div"), ds.count("</div>"), "| newsletter badges:", out.count("nbadge"))
