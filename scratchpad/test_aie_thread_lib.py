# -*- coding: utf-8 -*-
"""aie_thread_lib 규약 검사. PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib

fails = []

def eq(name, got, want):
    if got != want:
        fails.append('%s: got %r want %r' % (name, got, want))

# 1. 씨앗 재료가 규약을 통과한다
rows = lib.load()
eq('씨앗이 셋 이상', len(rows) >= 3, True)
eq('씨앗 규약 통과', lib.validate(rows), [])

# 2. 날짜순으로 온다
eq('날짜 오름차순', [r['date'] for r in rows], sorted(r['date'] for r in rows))

# 3. rel.to 가 뒤 날짜를 가리키면 잡는다
bad = [dict(rows[0], rel=[{'to': rows[-1]['id'], 'kind': '엇갈림'}])] + rows[1:]
eq('앞 날짜만 가리킨다', any('앞선 날짜' in m for m in lib.validate(bad)), True)

# 4. 없는 id 를 가리키면 잡는다
bad = [dict(rows[-1], rel=[{'to': '없는-id', 'kind': '동조'}])]
eq('없는 id', any('없는 id' in m for m in lib.validate(rows[:-1] + bad)), True)

# 5. 관계 이름이 둘 밖이면 잡는다 — 「반박」은 쓰지 않는다
bad = [dict(rows[-1], rel=[{'to': rows[0]['id'], 'kind': '반박'}])]
eq('관계 이름', any('관계 이름' in m for m in lib.validate(rows[:-1] + bad)), True)

# 6. id 가 겹치면 잡는다
eq('id 중복', any('id 중복' in m for m in lib.validate(rows + rows[:1])), True)

# 7. talk 이 실재하는 파일이어야 한다
bad = [dict(rows[0], talk='없는-발표')] + rows[1:]
eq('원문 없음', any('원문 없음' in m for m in lib.validate(bad)), True)

print('FAIL %d' % len(fails))
for f in fails:
    print(' ', f)
sys.exit(1 if fails else 0)
