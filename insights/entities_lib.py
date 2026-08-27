# -*- coding: utf-8 -*-
"""개체 사전 하나만 다룬다 — 읽고 쓰고 검증하고 별칭을 정본으로 푼다.
코퍼스는 안 읽는다. 파일을 훑는 일은 gen_index.py 가 한다.

사전은 생성물이 아니라 사람이 검토해 커밋하는 자료다. 그래서 정렬해서 쓰고
아스키 이스케이프를 안 쓴다 — 손으로 고칠 수 있어야 하고 diff 가 읽혀야 한다.
"""
import io
import json

import paths

TYPES = ('회사', '기술', '제품', '지표', '사람', '미정')


def norm(s):
    return s.strip().lower()


def load(path=None):
    with io.open(path or paths.ENTITIES, encoding='utf-8') as f:
        return json.load(f)


def save(rows, path=None):
    rows = sorted(rows, key=lambda r: r['canonical'])
    with io.open(path or paths.ENTITIES, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(rows, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')


def aliases_of(row):
    return list(row.get('ko') or []) + list(row.get('en') or [])


def alias_index(rows):
    out = {}
    for r in rows:
        for a in aliases_of(r):
            out[norm(a)] = r['canonical']
    return out


def validate(rows):
    msgs = []
    owner = {}
    seen = set()
    for r in rows:
        c = r.get('canonical')
        if not c:
            msgs.append('canonical 이 빈 항목이 있다')
            continue
        if c in seen:
            msgs.append('정본이 두 번 나온다: %s' % c)
        seen.add(c)
        if r.get('type') not in TYPES:
            msgs.append('%s 의 type 이 %s 다 — %s 중 하나여야 한다'
                        % (c, r.get('type'), '·'.join(TYPES)))
        if norm(c) not in [norm(a) for a in (r.get('ko') or [])]:
            msgs.append('%s 가 자기 ko 목록에 없다' % c)
        for a in aliases_of(r):
            k = norm(a)
            if k in owner and owner[k] != c:
                msgs.append('별칭 %s 가 %s 와 %s 둘에 걸려 있다' % (a, owner[k], c))
            owner[k] = c
    return msgs
