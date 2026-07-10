# SemiAnalysis 클리핑 파서 — CDP 제어 크롬에서 기사 추출 → 옵시디안 클리퍼 형식 md 저장
# 사용: python scratchpad/clip_articles.py [시작인덱스] [개수]
import json, time, re, sys, os, random, datetime
from websocket import create_connection
import urllib.request
import html2text

GAP_FILE = "scratchpad/clipping_gap.md"
OUT_DIR = "input/clippings"
STATE = "scratchpad/clip_state.json"
BASE = "https://newsletter.semianalysis.com/p/"

def slugs():
    out = []
    for line in open(GAP_FILE, encoding="utf-8"):
        m = re.match(r"^\d+\.\s+([a-z0-9-]+)\s*$", line.strip())
        if m: out.append(m.group(1))
    return out

def load_state():
    return json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}

def save_state(s):
    json.dump(s, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def get_tab():
    tabs = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9222/json")) if t["type"] == "page"]
    return tabs[0]

class CDP:
    def __init__(self, tab):
        self.ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=30)
        self.mid = 0
    def call(self, method, params=None):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.mid: return r
    def js(self, expr):
        r = self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        return r["result"]["result"].get("value")

EXTRACT = r"""
(()=>{
  const q=(s)=>document.querySelector(s);
  const meta=(p)=>{const m=document.querySelector(`meta[property='${p}'],meta[name='${p}']`);return m?m.content:null};
  const body=q('.available-content')||q('.body.markup');
  if(!body) return JSON.stringify({error:'NO_BODY'});
  const clone=body.cloneNode(true);
  clone.querySelectorAll('.paywall,.subscription-widget-wrap,[class*=subscribe-widget],.institutional-embed').forEach(e=>e.remove());
  const authors=Array.from(document.querySelectorAll("a[href*='semianalysis.com/@'], .post-header a[href*='/@']")).map(a=>a.innerText.trim()).filter(x=>x);
  return JSON.stringify({
    title:(q('h1.post-title')||q('h1'))?.innerText.trim(),
    subtitle:q('h3.subtitle')?.innerText.trim()||meta('description')||'',
    published:(meta('article:published_time')||q('time[datetime]')?.getAttribute('datetime')||(()=>{try{const ld=Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s=>JSON.parse(s.textContent)).find(j=>j.datePublished);return ld?ld.datePublished:''}catch(e){return ''}})()||'').slice(0,10),
    authors:Array.from(new Set(authors)).slice(0,6),
    text_len:body.innerText.length,
    paywalled:/This post is for paid subscribers|Subscribe to keep reading/i.test(document.body.innerText),
    html:clone.innerHTML
  });
})()
"""

def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()[:150]

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    os.makedirs(OUT_DIR, exist_ok=True)
    state = load_state()
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_images = False
    h.wrap_links = False

    cdp = CDP(get_tab())
    todo = slugs()[start:start+count]
    for slug in todo:
        if state.get(slug, {}).get("ok"):
            print(f"SKIP {slug} (done)")
            continue
        cdp.call("Page.navigate", {"url": BASE + slug})
        time.sleep(6 + random.uniform(0, 2))
        raw = cdp.js(EXTRACT)
        try:
            d = json.loads(raw)
        except Exception:
            print(f"FAIL {slug}: bad extract"); state[slug] = {"ok": False, "err": "extract"}; save_state(state); continue
        if d.get("error") or not d.get("title"):
            print(f"FAIL {slug}: {d.get('error','no title')}"); state[slug] = {"ok": False, "err": d.get("error", "no title")}; save_state(state); continue
        md = h.handle(d["html"])
        authors = d["authors"] or ["SemiAnalysis"]
        fm = ["---",
              f'title: "{d["title"]}"',
              f'source: "{BASE}{slug}"',
              "author:"] + [f'  - "[[{a}]]"' for a in authors] + [
              f'published: {d["published"]}',
              f'created: {datetime.date.today().isoformat()}',
              f'description: "{d["subtitle"][:300].replace(chr(34), chr(39))}"',
              "tags:", '  - "clippings"', "---", ""]
        out = "\n".join(fm) + md
        fname = os.path.join(OUT_DIR, sanitize(d["title"]) + ".md")
        open(fname, "w", encoding="utf-8").write(out)
        flag = "PAYWALL_PARTIAL" if (d["paywalled"] and d["text_len"] < 6000) else "OK"
        state[slug] = {"ok": flag == "OK", "file": fname, "chars": d["text_len"], "flag": flag}
        save_state(state)
        print(f"{flag} {slug} -> {os.path.basename(fname)} ({d['text_len']} chars)")
    cdp.ws.close()

if __name__ == "__main__":
    main()
