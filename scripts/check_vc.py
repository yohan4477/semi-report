# -*- coding: utf-8 -*-
u"""밸류체인 데이터 규약 — 공급원·매출원이 분석축으로 서 있나.

통합 밸류체인 분석 프레임워크 §22·§23(2026-09-11)을 기계가 보는 자리다.
FAIL 0 이어야 푸시한다.

  V1  공급 품목·제품군·계통이 상자로 남았나 (분류여야 한다)
  V2  관계가 없는 상자를 가리키나
  V3  supply_source_ids·revenue_type_ids 가 레지스트리에 실재하나
  V4  공급 관계에 공급원이 비었나 (미상으로도 안 닫혔나)
  V5  거래 관계에 매출원이 비었나 (배분 미상으로도 안 닫혔나)
  V6  기타와 미상을 한 칸에 합쳤나
  V7  비중에 분모와 기간이 붙었나
  V8  중개 뒤에 간접 고객까지 사슬이 닫혔나
  V9  같은 회사가 분류마다 복제됐나
  V10 프로젝트가 사슬의 한 칸을 차지했나, 타겟이 프로젝트 식구로 들었나
  V11 확인·추정이라 적힌 관계에 출처가 붙었나
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')

CLASS_TYPES = {'material', 'component', 'subsystem', 'revenue_type'}
STAGE_TIERS = {'RAW_MATERIAL', 'MATERIAL_PROCESSING', 'COMPONENT_SUPPLIER',
               'SUBSYSTEM_MODULE', 'SUBSYSTEM', 'CONTRACTUAL_CUSTOMER',
               'INTERMEDIARY', 'END_USER', 'END_MARKET'}
SUPPLY_REL = {'SUPPLIES', 'MANUFACTURES', 'PROCESSING', 'PROCESSED_INTO', 'INPUT_TO',
              'INTEGRATED_INTO', 'SUBSYSTEM_SUPPLY', 'SUBSYSTEM_INTEGRATION',
              'SURFACE_TREATMENT', 'EMS_ASSEMBLY', 'COATING', 'FUELS',
              'EQUIPMENT_SUPPLY', 'ELECTRICAL_BOP_SUPPLY', 'INTERNAL_MATERIAL_SUPPLY',
              'INTRAGROUP_SUPPLY', 'JV_ASSEMBLY', 'CONTRACT_MANUFACTURES'}
TRADE = {'SELLS_TO', 'DIRECT_CUSTOMER', 'END_CUSTOMER_SUPPLY_CHAIN',
         'DISTRIBUTION_PARTNERSHIP', 'CONTRACTUAL_CUSTOMER'}
PCT = {'percent', '%'}
# 탐색기에 실리는 사슬은 게이트, 아직 안 실린 사슬은 빚 한 줄로 센다 —
# 옛 사슬의 출처 빈칸 때문에 오늘 만지는 장이 못 나가면 검사기를 끄게 된다
STRICT = {'bloom-energy', 'kr-substrate', 'taiyo-yuden'}

fails = []
debt = {}


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def fail(code, msg):
    fails.append(u'FAIL %s — %s' % (code, msg))


def check_shares(where, rows):
    for s in rows:
        if s.get('unit') not in PCT:
            continue
        if not s.get('denominator'):
            fail('V7', u'%s 의 %s%% 에 분모가 없다' % (where, s.get('value')))
        if not (s.get('period') or s.get('period_start')):
            fail('V7', u'%s 의 %s%% 에 기간이 없다' % (where, s.get('value')))


def main():
    ents = dict((e['id'], e) for e in rd(os.path.join(DATA, 'entities.json')))
    for e in ents.values():
        if e.get('entity_type') in CLASS_TYPES:
            fail('V1', u'%s 가 아직 상자다. 공급원·매출원은 분류다' % e['id'])

    base = os.path.join(DATA, 'chains')
    chains = sorted(d for d in os.listdir(base)
                    if os.path.exists(os.path.join(base, d, 'relationships.json')))
    nrel = 0
    for cid in chains:
        cdir = os.path.join(base, cid)
        rels = rd(os.path.join(cdir, 'relationships.json'))
        nrel += len(rels)
        cpath = os.path.join(cdir, 'classifications.json')
        if not os.path.exists(cpath):
            fail('V3', u'%s 에 분류 파일이 없다' % cid)
            continue
        cls = rd(cpath)
        # 출처를 관계에 안 달고 근거 원장에 따로 적는 사슬이 있다. 둘 다 출처로 센다
        epath = os.path.join(cdir, 'evidence.json')
        evid = set()
        if os.path.exists(epath):
            evid = set(x.get('relationship_id') for x in rd(epath)
                       if x.get('source_id'))
        focal = cls.get('focal_entity')
        ss = dict((x['id'], x) for x in cls['supply_sources'])
        rt = dict((x['id'], x) for x in cls['revenue_types'])

        for reg in (ss, rt):
            for x in reg.values():
                lab = x.get('label') or ''
                if x.get('unallocated') and (u'기타' in lab or 'other' in lab.lower()):
                    fail('V6', u'%s 의 %s 가 기타와 미상을 한 칸에 담았다' % (cid, x['id']))
                check_shares(u'%s·%s' % (cid, x['id']), x.get('shares') or [])

        for r in rels:
            for k in ('source_entity', 'target_entity'):
                if r[k] not in ents:
                    fail('V2', u'%s 의 %s 가 없는 상자 %s 를 가리킨다'
                         % (cid, r['id'], r[k]))
                elif ents[r[k]].get('entity_type') in CLASS_TYPES:
                    fail('V1', u'%s 의 %s 가 분류를 상자 자리에 뒀다' % (cid, r['id']))
            for x in r.get('supply_source_ids') or []:
                if x not in ss:
                    fail('V3', u'%s 의 %s 가 없는 공급원 %s 를 가리킨다'
                         % (cid, r['id'], x))
            for x in r.get('revenue_type_ids') or []:
                if x not in rt:
                    fail('V3', u'%s 의 %s 가 없는 매출원 %s 를 가리킨다'
                         % (cid, r['id'], x))
            if (r.get('lane') != 'DOWNSTREAM' and r['relationship_type'] in SUPPLY_REL
                    and not (r.get('supply_source_ids') or [])):
                fail('V4', u'%s 의 %s 에 공급원이 비었다. 미상으로라도 닫는다'
                     % (cid, r['id']))
            if (r.get('lane') == 'DOWNSTREAM' and r['relationship_type'] in TRADE
                    and not (r.get('revenue_type_ids') or [])):
                fail('V5', u'%s 의 %s 에 매출원이 비었다. 배분 미상으로라도 닫는다'
                     % (cid, r['id']))
            if r.get('evidence_level') in ('CONFIRMED', 'ESTIMATED') \
                    and not (r.get('source_ids') or []) and r['id'] not in evid:
                if cid in STRICT:
                    fail('V11', u'%s 의 %s 가 출처 없이 %s 라고 적혔다'
                         % (cid, r['id'], r['evidence_level']))
                else:
                    debt[cid] = debt.get(cid, 0) + 1
            for k in ('source_entity', 'target_entity'):
                t = r.get('source_tier' if k == 'source_entity' else 'target_tier')
                if (ents.get(r[k], {}).get('entity_type') == 'project_spv'
                        and t in STAGE_TIERS):
                    fail('V10', u'%s 의 %s 가 프로젝트에 사슬 층 %s 를 줬다'
                         % (cid, r['id'], t))

        # V8 — 중개 뒤는 간접 고객까지 닫는다
        mids = set(r['target_entity'] for r in rels
                   if r.get('lane') == 'DOWNSTREAM'
                   and r.get('target_tier') == 'INTERMEDIARY'
                   and r['target_entity'] != focal)
        closed = set(r['source_entity'] for r in rels
                     if r.get('target_tier') in ('END_USER', 'END_MARKET'))
        for m in sorted(mids - closed):
            fail('V8', u'%s 의 중개 %s 뒤에 간접 고객이 없다' % (cid, m))

        # V10 — 타겟은 어떤 프로젝트의 식구도 아니다
        for r in rels:
            if ents.get(r['target_entity'], {}).get('entity_type') != 'project_spv':
                continue
            if r['source_entity'] == focal and r.get('lane') == 'DOWNSTREAM' \
                    and r['relationship_type'] not in ('SUPPLIES', 'DEPLOYS_AT_SITE',
                                                       'PROJECT_SUPPLY'):
                fail('V10', u'%s 에서 타겟이 프로젝트 %s 의 식구로 들었다'
                     % (cid, r['target_entity']))

        # V9 — 같은 회사가 분류마다 복제됐나
        names = {}
        used = set()
        for r in rels:
            used.add(r['source_entity'])
            used.add(r['target_entity'])
        for i in used:
            e = ents.get(i)
            if not e or e.get('anon'):
                continue
            key = (e.get('name_ko') or e.get('name') or '').strip()
            if key:
                names.setdefault(key, []).append(i)
        for key, ids in sorted(names.items()):
            if len(ids) > 1:
                fail('V9', u'%s 에서 「%s」가 상자 %s 로 나뉘었다'
                     % (cid, key, ', '.join(sorted(ids))))

        opath = os.path.join(cdir, 'observations.json')
        if os.path.exists(opath):
            for o in rd(opath):
                if o.get('unit') in PCT:
                    if not o.get('denominator'):
                        fail('V7', u'%s 의 관측 %s 에 분모가 없다' % (cid, o['id']))
                    if not (o.get('period') or o.get('period_start')):
                        fail('V7', u'%s 의 관측 %s 에 기간이 없다' % (cid, o['id']))

    for f in fails[:40]:
        print(f)
    for cid in sorted(debt):
        print(u'빚 %s — 출처 없는 확인·추정 관계 %d건' % (cid, debt[cid]))
    print(u'요약: 사슬 %d · 관계 %d / FAIL %d' % (len(chains), nrel, len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
