# -*- coding: utf-8 -*-
"""주장 흐름 화면 규약. PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_ui.py"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib
import gen_aie_thread as gen

fails = []
rows = lib.load()
html = gen.build()

def ck(name, cond):
    if not cond:
        fails.append(name)

ck('규약 통과', gen.check_ui(html, rows) == [])
ck('줄이 다 났다', html.count('class="claim"') == len(rows))
ck('거르개 둘', '신규만' in html and '엇갈림만' in html)
ck('색을 안 쓴다', gen.check_ui(html.replace('#555', '#c00'), rows) != [])
ck('반박이라는 말이 없다', '반박' not in html)
ck('카드로 가는 주소', 'ai-engineer/' in html)
ck('별표가 안 남았다', '**' not in html)
# 그물이 실제로 무는지 — 별표를 넣은 판이 통과하면 그물이 아니라 장식이다
ck('별표 그물이 문다', gen.check_ui(html.replace('</h1>', '</h1>**굵게**', 1), rows) != [])

print('FAIL %d' % len(fails))
for f in fails:
    print(' ', f)
sys.exit(1 if fails else 0)
