# 네이버 프리미엄 busymoon/kicpakpmg(회계사 채널) 클리퍼 — CDP 크롬에서 전문 추출.
# 유료 구독 콘텐츠라 공개 repo엔 커밋 금지. 원문은 로컬 볼트에만 둔다.
# 사용: python scratchpad/clip_kicpa.py <URL> [<URL> ...]
import json, time, re, sys, os, datetime, urllib.request
from websocket import create_connection

VAULT = r"C:\Users\y\semi_docs\Clippings\회계사"


def get_tab():
    tabs = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json"))
    return [t for t in tabs if t["type"] == "page"][0]


class CDP:
    def __init__(self, tab):
        self.ws = create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=30)
        self.mid = 0

    def call(self, m, p=None):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": m, "params": p or {}}))
        while True:
            r = json.loads(self.ws.recv())
            if r.get("id") == self.mid:
                return r

    def js(self, e):
        r = self.call("Runtime.evaluate", {"expression": e, "returnByValue": True, "awaitPromise": True})
        return r["result"]["result"].get("value")


EXTRACT = r"""
(()=>{
  const meta=(p)=>{const m=document.querySelector(`meta[property='${p}'],meta[name='${p}']`);return m?m.content:null};
  const body=document.querySelector('.se-main-container')||document.querySelector('#_SE_VIEWER_CONTENT');
  const paywalled=!!document.querySelector('.viewer_paywall:not(.viewer_paywall_none)');
  // og:author 가 비어 있다. 채널 필명은 본문 밖 "by ○○" 로만 나온다.
  const bym=document.body.innerText.match(/by\s*([가-힣A-Za-z]{2,10})/);
  return JSON.stringify({
    og_title:meta('og:title')||document.title,
    published:meta('article:published_time')||'',
    author:meta('og:author')||meta('author')||(bym?bym[1]:''),
    channel:meta('og:site_name')||'',
    text_len:body?body.innerText.length:0,
    paywalled,
    text:body?body.innerText:''
  });
})()
"""


def sanitize(n):
    return re.sub(r'[\\/:*?"<>|]', "", n).strip()[:150]


def pub_from_url(url):
    m = re.search(r"/contents/(\d{6})", url)
    if m:
        d = m.group(1)
        return f"20{d[0:2]}-{d[2:4]}-{d[4:6]}"
    return ""


def clip(cdp, url):
    cdp.call("Page.navigate", {"url": url})
    time.sleep(8)
    d = json.loads(cdp.js(EXTRACT))
    # 짧은 글이 있다. 실적공시 코멘트 같은 건 700자대다 — 1500자 문턱에 튕겼다.
    # 페이월 판정은 클래스로 하고 길이는 명백한 프리뷰만 걸러내는 선까지 낮춘다.
    if d["paywalled"] or d["text_len"] < 400:
        return f"SKIP paywall/short (len={d['text_len']}) {url}"
    os.makedirs(VAULT, exist_ok=True)
    pub = (d["published"] or "")[:10] or pub_from_url(url)
    author = d.get("author") or "회계사"
    fm = ["---",
          f'title: "{d["og_title"]}"',
          f'source: "{url}"',
          "author:", f'  - "[[{author}]]"',
          f'published: {pub}',
          f'created: {datetime.date.today().isoformat()}',
          "tags:", '  - "clippings"', '  - "valuation"', "---", ""]
    out = "\n".join(fm) + d["og_title"] + "\n\n" + d["text"]
    fname = os.path.join(VAULT, f"[{pub}] " + sanitize(d["og_title"]) + ".md")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(out)
    return f"OK {d['text_len']:>6} chars  ch={d['channel']!r} au={author!r} -> {os.path.basename(fname)}"


def main():
    cdp = CDP(get_tab())
    for url in sys.argv[1:]:
        print(clip(cdp, url), flush=True)
    cdp.ws.close()


if __name__ == "__main__":
    main()
