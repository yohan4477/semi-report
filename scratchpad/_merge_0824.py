# -*- coding: utf-8 -*-
# _newcards_0824.py 의 NEW_CARDS 본문을 gen_accountant_dashboard.py 의 CARDS 끝에 끼운다.
# 섹션 상수는 새 파일에서 이름 문자열로 두었으므로, 본문 텍스트를 그대로 옮기면
# 생성기 안의 진짜 SEC_* 객체를 가리키게 된다. 한 번만 돌린다(표시로 막는다).
import io, re, sys

GEN = 'scratchpad/gen_accountant_dashboard.py'
NEW = 'scratchpad/_newcards_0824.py'
MARK = '# ---- 2026-08-24 새 카드 ----'

src = io.open(NEW, encoding='utf-8').read()
i = src.index('NEW_CARDS = [')
body = src[i + len('NEW_CARDS = ['):]
body = body[:body.rindex(']')].strip()
assert body.startswith('{') and body.endswith('}'), body[:40]

gen = io.open(GEN, encoding='utf-8').read()
if MARK in gen:
    sys.exit('이미 병합돼 있다')
tail = '\n}]\n'
assert gen.count(tail) == 1, gen.count(tail)
gen = gen.replace(tail, '\n}, ' + MARK + '\n' + body + ']\n')
io.open(GEN, 'w', encoding='utf-8').write(gen)
print('병합했다')
