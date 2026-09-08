# -*- coding: utf-8 -*-
"""주장 흐름의 재료를 읽고 규약을 문다 — 생성기와 검사기가 같이 쓴다.

한쪽에만 두면 다른 쪽이 낡는다. 규약은 설계
docs/superpowers/specs/2026-09-08-AI-Engineer-주장-흐름-design.md §3·§6 이다.

관계는 동조·엇갈림 둘뿐이다. 「반박」은 발표자들이 서로 이름을 대고 받아친 적이
거의 없는데 그 자리에 없던 의도를 붙이는 이름이라 안 쓴다.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, 'insights', 'views', 'aie_thread.json')
AIE_DIR = os.path.join(ROOT, 'content', 'aie')

REL_KINDS = ('동조', '엇갈림')
FIELDS = ('id', 'talk', 'date', 'org', 'speaker', 'claim', 'line', 'rel')


def load(path=None):
    """재료를 읽어 날짜순(같으면 id순)으로 돌려준다."""
    rows = json.load(io.open(path or JSON_PATH, encoding='utf-8'))
    rows.sort(key=lambda r: (r.get('date', ''), r.get('id', '')))
    return rows


def md_lines(talk):
    """그 발표 변환본의 줄 목록. 없으면 None."""
    p = os.path.join(AIE_DIR, '%s.md' % talk)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n')


def validate(rows):
    """규약 위반 메시지 목록. 빈 목록이면 통과."""
    out = []
    seen = {}
    for r in rows:
        rid = r.get('id', '(id 없음)')
        for f in FIELDS:
            if f not in r:
                out.append('%s: 빠진 자리 %s' % (rid, f))
        if rid in seen:
            out.append('%s: id 중복' % rid)
        seen[rid] = r
        if md_lines(r.get('talk', '')) is None:
            out.append('%s: 원문 없음 content/aie/%s.md' % (rid, r.get('talk', '')))
    for r in rows:
        rid = r.get('id', '')
        for rel in r.get('rel') or ():
            to = rel.get('to')
            if rel.get('kind') not in REL_KINDS:
                out.append('%s: 관계 이름이 동조·엇갈림 밖이다 — %r' % (rid, rel.get('kind')))
            if to not in seen:
                out.append('%s: 없는 id 를 가리킨다 — %s' % (rid, to))
            elif seen[to].get('date', '') >= r.get('date', ''):
                out.append('%s: 앞선 날짜만 가리킬 수 있다 — %s' % (rid, to))
    return out


def orphan_ratio(rows):
    """아무 데도 안 걸린 주장의 비율. 걸림은 나가는 rel 이든 들어오는 rel 이든 센다."""
    if not rows:
        return 0.0
    tied = set()
    for r in rows:
        for rel in r.get('rel') or ():
            tied.add(r['id'])
            tied.add(rel.get('to'))
    return 1.0 - len(tied & {r['id'] for r in rows}) / float(len(rows))
