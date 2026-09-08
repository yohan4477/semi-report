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

# 본문이 통째로 인용이라 인용 대조가 유일한 바닥이다. 어긋난 재료를 먹이면 멈춰야 한다.
import copy
bent = copy.deepcopy(rows)
bent[0]['claim'] = '원문 어느 줄에도 없는 문장을 여기 박아 둔다'
ck('인용 그물이 문다', gen.check_ui(html, bent) != [])

# 걸림마다 대상 줄로 갈 앵커가 문서에 실재하나
missing = [r['id'] for r in rows for rel in r['rel']
           if 'id="%s"' % rel['to'] not in html]
ck('걸림의 대상 앵커가 다 있다 (%s)' % missing[:3], not missing)
ck('앵커 그물이 문다', gen.check_ui(html.replace('id="', 'x="'), rows) != [])

print('FAIL %d' % len(fails))
for f in fails:
    print(' ', f)
sys.exit(1 if fails else 0)
