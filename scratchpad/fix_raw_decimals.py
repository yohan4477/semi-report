# -*- coding: utf-8 -*-
"""문장 넷씩 묶는 과정에서 「18.4 billion」이 「18. 4 billion」으로 갈린 자리를 되붙인다.

줄 안에서만 고치므로 줄 번호는 그대로다 — 이미 붙인 (L줄) 인용이 안 깨진다.
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'content', 'semi_doped', 'raw')
PAT = re.compile(r'(?<=\d)\.\s+(?=\d)')

targets = sys.argv[1:] or [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(RAW, '*.md'))]
for slug in targets:
    path = os.path.join(RAW, slug + '.md')
    s = io.open(path, encoding='utf-8').read()
    n = len(PAT.findall(s))
    if not n:
        continue
    io.open(path, 'w', encoding='utf-8', newline='\n').write(PAT.sub('.', s))
    print('%s — 되붙인 자리 %d' % (slug, n))
