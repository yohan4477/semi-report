# -*- coding: utf-8 -*-
"""P19 가 걸리는 자리를 원본 파일에서 찾는다 — 대시보드는 생성물이라 고칠 곳이 아니다."""
import glob
import io
import os
import re

RX = re.compile(r'가른|가르는|가르고|가르며|가르지|가름|갈랐|값[을이] 매[기겨]')
PATS = ('insights/synth/*.md', 'insights/briefs/*.md', 'insights/loop/*.md',
        'insights/debate/*.md', 'insights/angles/*.md', 'insights/*.py',
        'insights/valuation/*.py', 'scratchpad/*.py', 'scripts/*.py')

tot = {}
for pat in PATS:
    for f in glob.glob(pat):
        n = len(RX.findall(io.open(f, encoding='utf-8', errors='ignore').read()))
        if n:
            tot[f.replace(os.sep, '/')] = n
print('원본 %d개 · %d곳' % (len(tot), sum(tot.values())))
for f, n in sorted(tot.items(), key=lambda x: -x[1])[:16]:
    print('  %3d %s' % (n, f))
