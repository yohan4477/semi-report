# -*- coding: utf-8 -*-
"""frontmatter 의 각도 이름과 절 제목이 어긋난 자리를 센다 — 띄어쓰기 하나로 안 붙는다."""
import glob, io, os, re, sys
sys.path.insert(0, 'insights')
import paths

for p in sorted(glob.glob(os.path.join(paths.ANGLES, '*.md'))):
    if os.path.basename(p).startswith('_'):
        continue
    t = io.open(p, encoding='utf-8').read()
    m = re.search(r'^angles: \[(.+?)\]', t, re.M)
    if not m:
        continue
    fm = [x.strip() for x in m.group(1).split(',')]
    heads = [h.strip() for h in re.findall(r'^## (.+)$', t, re.M)]
    heads = [h for h in heads if h not in ('시계열', '잔여', '다음 글이 채울 자리')]
    flat = {x.replace(' ', ''): x for x in fm}
    for h in heads:
        k = h.replace(' ', '')
        if h not in fm and k in flat:
            print('%s  절 「%s」 ≠ frontmatter 「%s」' % (os.path.basename(p)[:6], h, flat[k]))
        elif k not in flat:
            print('%s  절 「%s」 가 frontmatter 에 없다' % (os.path.basename(p)[:6], h))
