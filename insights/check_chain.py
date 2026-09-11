# -*- coding: utf-8 -*-
"""밸류체인 데이터 무결성 — data/valuechain 전부를 본다.

FAIL 0 이어야 푸시한다. 규칙은 docs/superpowers/specs/2026-09-11-밸류체인-인텔리전스-design.md §2.
  C1 참조가 실재하나 (엔티티·관계·출처·방법)
  C2 percent 에 분모가 붙었나
  C3 관측에 기간과 기준일이 있나
  C4 열거값이 정해진 것인가
  C5 과거 비중이 CURRENT 로 올라왔나 (분모가 같은 시계열 안에서)
  C6 BOM 구성 합이 총액 범위 안인가
  C7 수량 없는 계약에서 단가를 뽑았나
  C8 주장에 주어·근거등급·출처가 붙었나
  C9 다운스트림 관계에 층이 붙었나
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')

ENTITY_TYPE = set(['company', 'jv', 'project_spv', 'fund_jv', 'financial_institution',
                   'utility', 'end_user', 'material'])
LANE = set(['MANUFACTURING_BOM', 'MANUFACTURING_EQUIPMENT', 'SITE_ELECTRICAL_BOP',
            'OPERATIONAL_INPUT', 'DOWNSTREAM', 'CORPORATE'])
EV_LEVEL = set(['CONFIRMED', 'ESTIMATED', 'INFERRED', 'UNDISCLOSED',
                'HISTORICAL_CURRENT_UNKNOWN'])
OBS_STATUS = set(['CURRENT', 'HISTORICAL', 'HISTORICAL_CURRENT_UNKNOWN',
                  'NOT_YET_ACTIVE', 'UNKNOWN'])
REL_STATUS = set(['ACTIVE', 'ENDED', 'PLANNED', 'UNKNOWN'])
TIER = set(['CONTRACTUAL_CUSTOMER', 'INTERMEDIARY', 'PROJECT', 'END_USER'])
PCT = set(['%', 'percent'])

fails = []
warns = []


def fail(where, msg):
    fails.append(u'FAIL %s — %s' % (where, msg))


def warn(where, msg):
    warns.append(u'WARN %s — %s' % (where, msg))


def load(path, default=None):
    if not os.path.exists(path):
        return default
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


def chains():
    d = os.path.join(DATA, 'chains')
    if not os.path.isdir(d):
        return []
    return sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)))


def main():
    ents = load(os.path.join(DATA, 'entities.json'), []) or []
    srcs = load(os.path.join(DATA, 'sources.json'), []) or []
    meths = load(os.path.join(DATA, 'methods.json'), []) or []
    E = {}
    for e in ents:
        if e['id'] in E:
            fail('entities', u'%s 가 두 번 있다' % e['id'])
        E[e['id']] = e
        if e.get('entity_type') not in ENTITY_TYPE:
            fail('entities/' + e['id'], u'entity_type 이 %r' % e.get('entity_type'))
    S = {}
    for s in srcs:
        S[s['id']] = s
        if not s.get('url'):
            warn('sources/' + s['id'], u'url 이 없다')
    M = dict((m['id'], m) for m in meths)
    for m in meths:
        if not m.get('steps'):
            fail('methods/' + m['id'], u'steps 가 비었다')
        for sid in m.get('source_ids') or []:
            if sid not in S:
                fail('methods/' + m['id'], u'없는 출처 %s' % sid)

    for ch in chains():
        base = os.path.join(DATA, 'chains', ch)
        rels = load(os.path.join(base, 'relationships.json'), []) or []
        obss = load(os.path.join(base, 'observations.json'), []) or []
        evs = load(os.path.join(base, 'evidence.json'), []) or []
        hyps = load(os.path.join(base, 'hypotheses.json'), []) or []
        R = {}
        for r in rels:
            w = ch + '/' + r['id']
            if r['id'] in R:
                fail(w, u'관계 id 가 두 번 있다')
            R[r['id']] = r
            for k in ('source_entity', 'target_entity'):
                if r.get(k) not in E:
                    fail(w, u'%s 가 엔티티에 없다: %r' % (k, r.get(k)))
            if r.get('lane') not in LANE:
                fail(w, u'lane 이 %r' % r.get('lane'))
            if r.get('evidence_level') not in EV_LEVEL:
                fail(w, u'evidence_level 이 %r' % r.get('evidence_level'))
            if r.get('status') not in REL_STATUS:
                fail(w, u'status 가 %r' % r.get('status'))
            # C9 — 다운스트림은 층이 있어야 한다. 없으면 전부 한 홉으로 납작해진다
            if r.get('lane') == 'DOWNSTREAM' and r.get('target_tier') not in TIER:
                fail(w, u'다운스트림인데 target_tier 가 %r' % r.get('target_tier'))
            if r.get('lane') != 'DOWNSTREAM' and r.get('target_tier'):
                fail(w, u'다운스트림이 아닌데 target_tier 가 붙었다')

        O = {}
        latest = {}
        for o in obss:
            w = ch + '/' + o['id']
            O[o['id']] = o
            if o.get('relationship_id') not in R:
                fail(w, u'관계 %r 가 없다' % o.get('relationship_id'))
            if not o.get('period'):
                fail(w, u'period 가 없다')
            if not o.get('as_of_date'):
                fail(w, u'as_of_date 가 없다')
            if o.get('unit') in PCT and not o.get('denominator'):
                fail(w, u'%s 에 분모가 없다' % o.get('metric'))
            if o.get('status') not in OBS_STATUS:
                fail(w, u'status 가 %r' % o.get('status'))
            if o.get('evidence_level') not in EV_LEVEL:
                fail(w, u'evidence_level 이 %r' % o.get('evidence_level'))
            if o.get('method_id') and o['method_id'] not in M:
                fail(w, u'없는 방법 %s' % o['method_id'])
            for sid in o.get('source_ids') or []:
                if sid not in S:
                    fail(w, u'없는 출처 %s' % sid)
            # 비중만 시계열로 본다. 계약·용량은 같은 시점에 여러 건이 설 수 있다
            if o.get('unit') in PCT:
                key = (o.get('relationship_id'), o.get('metric'), o.get('denominator'))
                end = o.get('period_end') or o.get('as_of_date') or ''
                if end > latest.get(key, ''):
                    latest[key] = end
        for o in obss:
            if o.get('unit') not in PCT:
                continue
            key = (o.get('relationship_id'), o.get('metric'), o.get('denominator'))
            end = o.get('period_end') or o.get('as_of_date') or ''
            if o.get('status') == 'CURRENT' and end < latest.get(key, ''):
                fail(ch + '/' + o['id'],
                     u'더 늦은 관측이 있는데 CURRENT 다 (%s < %s)' % (end, latest[key]))

        H = dict((x['id'], x) for x in hyps)
        for e in evs:
            w = ch + '/' + e['id']
            if e.get('source_id') not in S:
                fail(w, u'없는 출처 %r' % e.get('source_id'))
            if e.get('metric_id') and e['metric_id'] not in O:
                fail(w, u'없는 관측 %s' % e['metric_id'])
            if e.get('hypothesis_id') and e['hypothesis_id'] not in H:
                fail(w, u'없는 가설 %s' % e['hypothesis_id'])
            if (not e.get('metric_id') and not e.get('hypothesis_id')
                    and e.get('relationship_id') not in R):
                fail(w, u'없는 관계 %r' % e.get('relationship_id'))
        for x in hyps:
            w = ch + '/' + x['id']
            if x.get('anon_company_id') not in E:
                fail(w, u'익명 엔티티 %r 가 없다' % x.get('anon_company_id'))
            if x.get('candidate_company_id') not in E:
                fail(w, u'후보 엔티티 %r 가 없다' % x.get('candidate_company_id'))

        for c in load(os.path.join(base, 'claims.json'), []) or []:
            w = ch + '/' + c['id']
            if not c.get('statement'):
                fail(w, u'주장 문장이 비었다')
            if c.get('subject') not in E:
                fail(w, u'주어 %r 가 엔티티에 없다' % c.get('subject'))
            if c.get('object') and c['object'] not in E:
                fail(w, u'목적어 %r 가 엔티티에 없다' % c['object'])
            if c.get('evidence_level') not in EV_LEVEL:
                fail(w, u'evidence_level 이 %r' % c.get('evidence_level'))
            if not c.get('source_ids'):
                fail(w, u'출처가 없다')
            for sid in c.get('source_ids') or []:
                if sid not in S:
                    fail(w, u'없는 출처 %s' % sid)

        bdir = os.path.join(base, 'bom')
        if os.path.isdir(bdir):
            for fn in sorted(os.listdir(bdir)):
                b = load(os.path.join(bdir, fn))
                w = ch + '/bom/' + fn
                tot = b.get('total')
                if not tot or 'low' not in tot or 'high' not in tot:
                    fail(w, u'total 범위가 없다')
                    continue
                s = sum(c.get('central', 0) for c in b.get('components') or [])
                if not (tot['low'] * 0.9 <= s <= tot['high'] * 1.1):
                    fail(w, u'구성 합 %.3f 가 총액 범위 %.2f~%.2f 밖이다'
                         % (s, tot['low'], tot['high']))
                for c in b.get('components') or []:
                    if c.get('evidence_level') not in EV_LEVEL:
                        fail(w, u'%s 의 evidence_level 이 %r'
                             % (c.get('id'), c.get('evidence_level')))
                    if c.get('denominator') is None:
                        fail(w, u'%s 에 분모가 없다' % c.get('id'))

        for o in obss:
            if o.get('unit') in ('USD/MW', 'USD per MW') and not o.get('method_id'):
                fail(ch + '/' + o['id'], u'$/MW 인데 방법이 없다')

    for w in warns:
        print(w)
    for f in fails:
        print(f)
    print(u'FAIL %d / WARN %d' % (len(fails), len(warns)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
