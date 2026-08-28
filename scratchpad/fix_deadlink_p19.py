# -*- coding: utf-8 -*-
"""P19 기계 치환이 깬 파일명 참조를 되돌린다.

생성기 안에는 원문 파일명이 문자열로 박혀 있는데, 경로는 상수로 앞에 붙고
따옴표 안에는 파일명만 있는 경우가 많다. 그래서 경로로 못 찾고 파일명으로 찾는다.

원문 제목은 필자가 쓴 것이라 고칠 대상이 아니다 — 참조를 되돌리고, 그 제목은
검사기에서 인용으로 떼어 낸다. 되돌린 제목을 마지막에 출력한다.
"""
import glob
import io
import os
import re

BACK = [('나누는', '가르는'), ('나눈다', '가른다'), ('나눈', '가른'),
        ('나눴', '갈랐'), ('나누고', '가르고'), ('나누며', '가르며'),
        ('구분', '가름')]
NAMES = {}
for pat in ('content/**/*.md', 'input/**/*.md', 'content/**/*.json',
            'input/**/*.json'):
    for p in glob.glob(pat, recursive=True):
        NAMES[os.path.basename(p)] = p

STR = re.compile(r"""['"]([^'"\n]*\.(?:md|json))['"]""")
titles = set()

TARGETS = (glob.glob('scratchpad/*.py') + glob.glob('insights/*.py')
           + glob.glob('scripts/*.py')
           # 노트·인사이트의 frontmatter source: 경로도 같은 사고를 맞았다
           + glob.glob('insights/**/*.md', recursive=True))

for f in sorted(TARGETS):
    s = io.open(f, encoding='utf-8').read()
    out, hit = s, 0
    for ref in set(STR.findall(s)):
        base = os.path.basename(ref)
        if base in NAMES:
            continue
        for a, b in BACK:
            if a not in base:
                continue
            cand = base.replace(a, b)
            if cand in NAMES:
                out = out.replace(base, cand)
                hit += 1
                stem = re.sub(r'^\[\d{6}\]\s*', '', cand.rsplit(' - ', 1)[0])
                titles.add(stem.replace('.md', ''))
                break
    if hit:
        io.open(f, 'w', encoding='utf-8', newline='\n').write(out)
        print('%2d %s' % (hit, f.replace(os.sep, '/')))

print('--- 되돌린 원제 %d개 ---' % len(titles))
for t in sorted(titles):
    print('   ', t)
