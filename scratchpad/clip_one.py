import json, time, sys, os, datetime, html2text
sys.path.insert(0, "scratchpad")
from clip_articles import CDP, get_tab, EXTRACT, sanitize, BASE, OUT_DIR, load_state, save_state

slug = sys.argv[1]
cdp = CDP(get_tab())
cdp.call("Page.navigate", {"url": BASE + slug})
time.sleep(9)
d = json.loads(cdp.js(EXTRACT))
print("title:", d.get("title"), "| paywalled:", d.get("paywalled"), "| len:", d.get("text_len"), "| pub:", d.get("published"))
assert not d["paywalled"] and d["text_len"] > 6000, "subscriber session expired"
h = html2text.HTML2Text(); h.body_width = 0; h.ignore_images = False; h.wrap_links = False
md = h.handle(d["html"])
authors = d["authors"] or ["SemiAnalysis"]
fm = ["---", f'title: "{d["title"]}"', f'source: "{BASE}{slug}"', "author:"] + \
     [f'  - "[[{a}]]"' for a in authors] + \
     [f'published: {d["published"]}', f'created: {datetime.date.today().isoformat()}',
      f'description: "{d["subtitle"][:300].replace(chr(34), chr(39))}"', "tags:", '  - "clippings"', "---", ""]
fname = os.path.join(OUT_DIR, sanitize(d["title"]) + ".md")
open(fname, "w", encoding="utf-8").write("\n".join(fm) + md)
st = load_state(); st[slug] = {"ok": True, "file": fname, "chars": d["text_len"], "flag": "OK"}; save_state(st)
print("SAVED", fname)
cdp.ws.close()
