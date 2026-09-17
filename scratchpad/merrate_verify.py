# -*- coding: utf-8 -*-
"""merrate_facts_*.md 의 원문 구절이 그 글 본문에 글자 그대로 있나."""
import io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
bad = n = 0
for k in 'ABCD':
    for l in io.open('scratchpad/merrate_facts_%s.md' % k, encoding='utf-8'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 6 or not re.match(r'\d{4}-\d\d-\d\d', c[0]):
            continue
        n += 1
        q = c[5].strip('「」"\'“”')
        try:
            t = json.load(io.open('input/clippings/mer/%s.json' % c[1], encoding='utf-8'))['text']
        except Exception:
            print('NOFILE', k, c[0], c[1]); bad += 1; continue
        norm = lambda s: re.sub(r'\s+', '', s)
        if norm(q) not in norm(t):
            bad += 1
            print('MISS', k, c[0], c[1], q[:50])
print('줄 %d · 불일치 %d' % (n, bad))
