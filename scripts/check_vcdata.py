# -*- coding: utf-8 -*-
u"""밸류체인 데이터 뜻 검사 — 꼴은 맞는데 뜻이 어긋난 자리.

check_vc 가 분류·닫힘·근거 칸 같은 규약을 재고, 이 검사는 그 밑을 본다. FAIL 은 고쳐야
푸시하고, WARN 은 빚으로 센다(조사 단계에서 채울 것).

FAIL
  D2  없는 출처 id 를 가리킨다
  D6  자기 자신을 가리키는 관계
  D7  같은 관계가 두 번(같은 출발·도착·종류·분류) — 분류가 다르면 한 회사가 두 품목을 대는 것이라 둔다
  D8  관측이 없는 관계를 가리킨다
  D9  % 값이 0~100 밖
  D11 기간이 뒤집혔다(시작 > 끝)
  D14 근거 원장이 없는 관계를 가리킨다
  D23 같은 이름의 상자가 둘 이상(다른 id) — 같은 법인이면 하나로 합친다
WARN
  D3  날짜 꼴이 YYYY-MM-DD 가 아니다(달 단위 출처 날짜는 정직한 값이라 경고만)
  D4  확인(CONFIRMED)인데 메모가 추정·추론·가능성·보도를 말한다
  D5  끝난(ENDED) 관계에 끝난 때가 없다 — 어느 해에도 안 보인다
  D10 기준일이 오늘보다 뒤
  D12 확인·추정 관측/주장에 출처가 없다
  D13 주장에 기간이 없다
  D15 같은 분모·기간의 비중 합이 100 을 넘는다
  D17 어느 사슬에도 안 쓰인 상자
  D18 나라 없는 회사(익명·전방시장 제외)
  D20 어디서도 안 쓰인 출처
  D21 주소 없는 출처(추정·원장 제외)
  D22 발행일 없는 출처
"""
import collections
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
PCT = {'percent', '%'}
DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
YEARISH = re.compile(r'^\d{4}(-\d{2}(-\d{2})?)?$')
HEDGE = re.compile(u'추정|추론|가능성|보도|후보|미확인|정황')


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def validate(today=None):
    today = today or datetime.date.today()
    fails, warns = [], []
    F = lambda c, m: fails.append(u'FAIL %s — %s' % (c, m))
    W = lambda c, m: warns.append(u'WARN %s — %s' % (c, m))
    ents = dict((e['id'], e) for e in rd(os.path.join(DATA, 'entities.json')))
    srcs = dict((s['id'], s) for s in rd(os.path.join(DATA, 'sources.json')))
    base = os.path.join(DATA, 'chains')
    chains = sorted(d for d in os.listdir(base)
                    if os.path.exists(os.path.join(base, d, 'chain.json')))
    used_ent, used_src = collections.Counter(), collections.Counter()
    for ck in chains:
        b = os.path.join(base, ck)
        rels = rd(os.path.join(b, 'relationships.json'))
        obs = rd(os.path.join(b, 'observations.json')) if os.path.exists(
            os.path.join(b, 'observations.json')) else []
        cls = rd(os.path.join(b, 'classifications.json'))
        claims = rd(os.path.join(b, 'claims.json')) if os.path.exists(
            os.path.join(b, 'claims.json')) else []
        evs = rd(os.path.join(b, 'evidence.json')) if os.path.exists(
            os.path.join(b, 'evidence.json')) else []
        relids = set(r['id'] for r in rels)
        pair = collections.Counter()
        for r in rels:
            for k in ('source_entity', 'target_entity'):
                used_ent[r[k]] += 1
            for s in r.get('source_ids') or []:
                used_src[s] += 1
                if s not in srcs:
                    F('D2', u'%s %s → 출처 %s 없음' % (ck, r['id'], s))
            if r['source_entity'] == r['target_entity']:
                F('D6', u'%s %s' % (ck, r['id']))
            key = (r['source_entity'], r['target_entity'], r['relationship_type'],
                   tuple(sorted(r.get('supply_source_ids') or [])),
                   tuple(sorted(r.get('revenue_type_ids') or [])))
            pair[key] += 1
            for k in ('valid_from', 'valid_to'):
                v = r.get(k)
                if v and not YEARISH.match(str(v)):
                    W('D3', u'%s %s %s=%s' % (ck, r['id'], k, v))
            if r.get('evidence_level') == 'CONFIRMED' and HEDGE.search(r.get('notes') or ''):
                W('D4', u'%s %s: %s' % (ck, r['id'], (r.get('notes') or '')[:50]))
            if r.get('status') == 'ENDED' and not r.get('valid_to'):
                W('D5', u'%s %s' % (ck, r['id']))
        for k, n in pair.items():
            if n > 1:
                F('D7', u'%s %s→%s %s ×%d' % (ck, k[0], k[1], k[2], n))
        for o in obs:
            rid = o.get('relationship_id')
            if rid and rid not in relids:
                F('D8', u'%s %s → 관계 %s 없음' % (ck, o['id'], rid))
            if o.get('unit') in PCT:
                for k in ('value', 'value_low', 'value_high'):
                    v = o.get(k)
                    if v is not None and not (0 <= v <= 100):
                        F('D9', u'%s %s %s=%s' % (ck, o['id'], k, v))
            for k in ('as_of_date', 'source_date', 'period_start', 'period_end'):
                v = o.get(k)
                if v and not DATE.match(str(v)):
                    W('D3', u'%s 관측 %s %s=%s' % (ck, o['id'], k, v))
            ps, pe = o.get('period_start'), o.get('period_end')
            if ps and pe and DATE.match(ps) and DATE.match(pe) and ps > pe:
                F('D11', u'%s %s %s > %s' % (ck, o['id'], ps, pe))
            a = o.get('as_of_date')
            if a and DATE.match(a) and datetime.date.fromisoformat(a) > today:
                W('D10', u'%s %s %s' % (ck, o['id'], a))
            for s in o.get('source_ids') or []:
                used_src[s] += 1
                if s not in srcs:
                    F('D2', u'%s 관측 %s → 출처 %s 없음' % (ck, o['id'], s))
            if not (o.get('source_ids') or []) and o.get('evidence_level') in ('CONFIRMED', 'ESTIMATED'):
                W('D12', u'%s 관측 %s (%s)' % (ck, o['id'], o.get('evidence_level')))
        for c in claims:
            for s in c.get('source_ids') or []:
                used_src[s] += 1
                if s not in srcs:
                    F('D2', u'%s 주장 %s → 출처 %s 없음' % (ck, c['id'], s))
            if not c.get('period'):
                W('D13', u'%s %s' % (ck, c['id']))
            if not (c.get('source_ids') or []) and c.get('evidence_level') in ('CONFIRMED', 'ESTIMATED'):
                W('D12', u'%s 주장 %s' % (ck, c['id']))
        for e in evs:
            rid = e.get('relationship_id')
            if rid and rid not in relids:
                F('D14', u'%s %s → 관계 %s 없음' % (ck, e['id'], rid))
            if e.get('source_id'):
                used_src[e['source_id']] += 1
                if e['source_id'] not in srcs:
                    F('D2', u'%s 근거 %s → 출처 %s 없음' % (ck, e['id'], e['source_id']))
        for kind in ('supply_sources', 'revenue_types'):
            tot = collections.defaultdict(float)
            for x in cls[kind]:
                for s in x.get('shares') or []:
                    if s.get('unit') in PCT and s.get('value') is not None \
                            and re.search(r'share$', s.get('metric') or ''):
                        tot[(s.get('denominator'), s.get('period'))] += s['value']
            for k, v in tot.items():
                if v > 100.5:
                    W('D15', u'%s %s %s = %.1f' % (ck, kind, k, v))
    for eid, e in ents.items():
        if used_ent[eid] == 0:
            W('D17', eid)
        if not e.get('anon') and not e.get('country') and e.get('entity_type') != 'application':
            W('D18', u'%s (%s)' % (eid, e.get('entity_type')))
    for sid, s in srcs.items():
        if used_src[sid] == 0:
            W('D20', sid)
        if not s.get('url') and s.get('source_type') not in ('analyst_estimate', 'research_ledger'):
            W('D21', u'%s (%s)' % (sid, s.get('source_type')))
        if not s.get('published_date'):
            W('D22', sid)
    names = collections.defaultdict(list)
    for eid, e in ents.items():
        if e.get('anon'):
            continue
        n = (e.get('name_ko') or e.get('name') or '').strip().lower()
        if n and used_ent[eid]:
            names[n].append(eid)
    for n, ids in sorted(names.items()):
        if len(ids) > 1:
            F('D23', u'「%s」 %s' % (n, ', '.join(sorted(ids))))
    return fails, warns, len(chains)


def main():
    fails, warns, n = validate()
    for f in fails[:40]:
        print(f)
    cnt = collections.Counter(w.split(u' — ')[0] for w in warns)
    for k in sorted(cnt):
        print(u'빚 %s %d건' % (k, cnt[k]))
    print(u'요약: 사슬 %d / FAIL %d / WARN %d' % (n, len(fails), len(warns)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
