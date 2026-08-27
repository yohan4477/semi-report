# -*- coding: utf-8 -*-
"""각도 파일을 대상으로 묶어 여러 편에 걸친 것만 낸다 — 글이 될 재료가 있나."""
import glob, io, os, re, sys, collections
sys.path.insert(0, 'insights')
import paths

SEP = re.compile(r'^\|[\s:|-]+\|$')
TAG = re.compile(r'\[([^\[\]\n]*?·[^\[\]\n]*?)\]')

rows = []
for p in sorted(glob.glob(os.path.join(paths.ANGLES, '*.md'))):
    if os.path.basename(p).startswith('_'):
        continue
    doc = os.path.basename(p)[:6]
    angle = ''
    for line in io.open(p, encoding='utf-8').read().split('\n'):
        if line.startswith('## '):
            # 붙일 때는 공백을 지우고 견준다 — 「경쟁사 행동」과 「경쟁사행동」은 같은 각도다
            angle = line[3:].strip().replace(' ', '')
        if line.startswith('|') and not SEP.match(line):
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            if len(c) == 6 and c[0] != '대상':
                rows.append((doc, angle, c[0], c[1], c[2], c[3], c[5]))
            continue
        for body in TAG.findall(line):
            f = [x.strip() for x in body.split(' · ')]
            if len(f) == 4:
                txt = TAG.sub('', line).strip()
                rows.append((doc, angle, f[0], txt[:70], '', f[1], f[3]))

by = collections.defaultdict(list)
for r in rows:
    by[r[2]].append(r)
multi = {k: v for k, v in by.items() if len(set(x[0] for x in v)) > 1}
print('항목 %d · 대상 %d종 · 여러 편에 걸친 대상 %d종\n' % (len(rows), len(by), len(multi)))
for k, v in sorted(multi.items(), key=lambda x: -len(x[1])):
    docs = sorted(set(x[0] for x in v))
    angles = sorted(set(x[1] for x in v))
    print('%-16s 편 %s · 항목 %2d · 각도 %s' % (k, ','.join(docs), len(v), ' / '.join(angles)))
