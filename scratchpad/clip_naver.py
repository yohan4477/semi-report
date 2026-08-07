# naver 프리미엄(언더스탠딩 백브리핑) 클리퍼 — CDP 크롬에서 전문 추출 → 로컬 옵시디언 볼트에만 저장
# 유료 구독 콘텐츠라 공개 repo엔 커밋 금지. 원문은 semi_docs 볼트에만.
# 사용: python scratchpad/clip_naver.py <URL>
import json, time, re, sys, os, datetime, urllib.request
from websocket import create_connection

VAULT = r"C:\Users\y\semi_docs\Clippings\언더스탠딩 백브리핑"

def get_tab():
    return [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:9222/json")) if t["type"] == "page"][0]

class CDP:
    def __init__(self, tab):
        self.ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=30); self.mid = 0
    def call(self, m, p=None):
        self.mid += 1; self.ws.send(json.dumps({"id": self.mid, "method": m, "params": p or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.mid: return r
    def js(self, e):
        return self.call("Runtime.evaluate", {"expression": e, "returnByValue": True, "awaitPromise": True})["result"]["result"].get("value")

EXTRACT = r"""
(()=>{
  const meta=(p)=>{const m=document.querySelector(`meta[property='${p}'],meta[name='${p}']`);return m?m.content:null};
  const body=document.querySelector('.se-main-container')||document.querySelector('#_SE_VIEWER_CONTENT');
  const paywalled=!!document.querySelector('.viewer_paywall:not(.viewer_paywall_none)')||/프리미엄 구독|로그인이 필요/.test(document.body.innerText.slice(0,3000));
  const bym=document.body.innerText.match(/by\s*([가-힣]{2,4})\s*기자/);
  return JSON.stringify({
    og_title:meta('og:title')||document.title,
    published:meta('article:published_time')||'',
    author:(bym?bym[1]:'')||meta('og:author')||meta('author')||'',
    text_len:body?body.innerText.length:0,
    paywalled,
    text:body?body.innerText:''
  });
})()
"""

def sanitize(n):
    return re.sub(r'[\\/:*?"<>|]', "", n).strip()[:150]

def pub_from_url(url):
    m = re.search(r'/contents/(\d{6})', url)  # yymmdd 접두
    if m:
        d = m.group(1)
        return f"20{d[0:2]}-{d[2:4]}-{d[4:6]}"
    return ""

def main():
    url = sys.argv[1]
    cdp = CDP(get_tab())
    cdp.call("Page.navigate", {"url": url})
    time.sleep(8)
    d = json.loads(cdp.js(EXTRACT))
    cdp.ws.close()
    if d["paywalled"] or d["text_len"] < 1500:
        print(f"PAYWALL/SHORT (len={d['text_len']}) — 로그인 세션 확인 필요"); return
    os.makedirs(VAULT, exist_ok=True)
    pub = d["published"][:10] or pub_from_url(url)
    reporter = d.get("author") or "언더스탠딩"
    fm = ["---",
          f'title: "{d["og_title"]}"',
          f'source: "{url}"',
          'author:', f'  - "[[{reporter}]]"', '  - "[[언더스탠딩]]"',
          f'published: {pub}',
          f'created: {datetime.date.today().isoformat()}',
          'tags:', '  - "clippings"', '  - "understanding"', "---", ""]
    out = "\n".join(fm) + d["og_title"] + "\n\n" + d["text"]
    fname = os.path.join(VAULT, sanitize(d["og_title"]) + ".md")
    open(fname, "w", encoding="utf-8").write(out)
    print(f"OK ({d['text_len']} chars) -> {fname}")

if __name__ == "__main__":
    main()
