import re, pathlib, collections
d = pathlib.Path("insights/angles")
c = collections.Counter()
per = {}
for f in sorted(d.glob("*.md")):
    if f.name.startswith("_"): continue
    t = f.read_text(encoding="utf-8")
    m = re.search(r"^angles: \[(.+?)\]", t, re.M)
    if not m: continue
    names = [x.strip() for x in m.group(1).split(",")]
    per[f.name] = names
    c.update(names)
print("files", len(per), "angle-tokens", sum(len(v) for v in per.values()), "unique", len(c))
for k,v in c.most_common():
    if v>1: print(v, k)
print("---items---")
tot=0
for f in sorted(d.glob("*.md")):
    if f.name.startswith("_"): continue
    t=f.read_text(encoding="utf-8")
    rows=len(re.findall(r"^\|(?! *[-:]).+\|$", t, re.M))-2*len(re.findall(r"^\| 대상 \|", t, re.M))
    tags=len(re.findall(r"\[[^\[\]]+ · [^\[\]]+ · §[^\[\]]+ · [^\[\]]+\]", t))
    print(f.name, "표행", rows, "꼬리표", tags)
    tot+=rows+tags
print("합계 항목", tot)
