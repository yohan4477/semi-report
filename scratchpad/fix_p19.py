# -*- coding: utf-8 -*-
"""P19 번역투 치환 (docs/superpowers 는 설계 이력이라 제외) — 「가르다」 능동형만 바꾼다. 「갈린다」는 정상이라 안 건드린다.

검사기 자신(check_prose.py)과 규칙을 설명하는 문서는 뺀다 — 거기서는 그 말이
금지 대상으로 인용돼 있어야 한다.
"""
import glob, io, os, re, sys

MAP = [('가른다', '나눈다'), ('가르는', '나누는'), ('가르고', '나누고'),
       ('가르며', '나누며'), ('갈랐', '나눴'), ('가름', '구분')]
SKIP = {'insights/check_prose.py', 'scratchpad/fix_p19.py'}
PATS = ('insights/**/*.md', 'insights/*.py', 'scratchpad/*.py', 'scripts/*.py',
        '.claude/skills/**/*.md', 'plugins/**/*.md')

dry = '--write' not in sys.argv
total = 0
for pat in PATS:
    for f in glob.glob(pat, recursive=True):
        key = f.replace(os.sep, '/')
        if key in SKIP:
            continue
        s = io.open(f, encoding='utf-8', errors='ignore').read()
        n = sum(s.count(a) for a, _ in MAP)
        if not n:
            continue
        total += n
        if not dry:
            for a, b in MAP:
                s = s.replace(a, b)
            io.open(f, 'w', encoding='utf-8', newline='\n').write(s)
        print('%3d %s' % (n, key))
print(('[미리보기] ' if dry else '[적용] ') + '합계 %d' % total)
