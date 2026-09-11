# -*- coding: utf-8 -*-
u"""밸류체인 데이터 규약 — 공급원·매출원이 분석축으로 서 있나, 사슬이 닫혔나.

통합 밸류체인 분석 프레임워크 §22·§23(2026-09-11)을 기계가 보는 자리다.
FAIL 0 이어야 푸시한다. 생성기(gen_vcexplorer.py)도 이 검사를 먼저 돌리고 FAIL 이면
굽지 않는다 — 발행을 막는 검사다.

  V1  공급 품목·제품군·계통이 상자로 남았나 (분류여야 한다)
  V2  관계가 없는 상자를 가리키나
  V3  supply_source_ids·revenue_type_ids 가 레지스트리에 실재하나
  V4  공급 관계에 공급원이 비었나 (미상으로도 안 닫혔나)
  V5  거래 관계에 매출원이 비었나 (배분 미상으로도 안 닫혔나)
  V6  기타와 미상을 한 칸에 합쳤나
  V7  비중에 metric·value·unit·period·denominator·근거 등급·출처가 다 붙었나
  V8  중개 뒤에 간접 고객(실명 또는 「간접 고객 미상」)까지 사슬이 닫혔나 —
      중개는 데이터가 준 노릇(tier INTERMEDIARY), 닫힘은 타겟에서 앞으로 이어진 꼴로 잰다
  V9  같은 회사가 분류마다 복제됐나
  V10 프로젝트 — 식구 목록이 명시돼 있나, 타겟이 식구로 들었나, 프로젝트 id 가 관계의
      끝점이 됐나, 식구가 실재하는 상자인가. SPV·부지는 상자로 남는다
  V11 확인·추정이라 적힌 관계에 출처가 붙었나
  V12 공급원·매출원 개별 귀속(미상 아닌 것)에 근거가 붙었나 — 전체 mix 로 배정하면 FAIL
  V13 타겟에서 나가는 거래에 contractual_customer 근거 칸이 있나, 값이 셋 중 하나인가
  V14 귀속별 등급(revenue_type_map)이 ids 안의 분류만 가리키고 등급·출처가 붙었나

실리는 사슬(chain.json 이 있는 디렉터리)은 게이트, 아직 안 실린 사슬은 빚 한 줄로 센다.
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
CONTRACTUAL = {'CONFIRMED', 'NOT_CONTRACTUAL', 'UNVERIFIED'}
SHARE_FIELDS = ('metric', 'value', 'unit', 'period', 'denominator', 'evidence_level',
                'source_ids')
# 간접 고객 자리를 닫는 자리표. 실명이 없으면 이것으로 닫고 회사를 지어내지 않는다
UNDISCLOSED_REL = 'INDIRECT_CUSTOMER_UNDISCLOSED'


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def shipped_chains():
    u"""실리는 사슬 — chain.json 이 있는 디렉터리 전부. 이름을 코드에 박지 않는다."""
    base = os.path.join(DATA, 'chains')
    return sorted(d for d in os.listdir(base)
                  if os.path.exists(os.path.join(base, d, 'chain.json')))


def check_shares(fail, where, rows):
    for s in rows:
        if s.get('value') is None and s.get('value_low') is None:
            continue
        for k in SHARE_FIELDS:
            v = s.get(k)
            if k == 'value' and v is None and s.get('value_low') is not None:
                continue
            if v is None or v == '' or v == []:
                fail('V7', u'%s 의 비중(%s %s)에 %s 가 없다'
                     % (where, s.get('metric'), s.get('value'), k))


def validate():
    u"""(fails, debt, stats). fails 는 문자열 목록, debt 는 사슬별 빚 수."""
    fails = []
    debt = {}

    def fail(code, msg):
        fails.append(u'FAIL %s — %s' % (code, msg))

    ents = dict((e['id'], e) for e in rd(os.path.join(DATA, 'entities.json')))
    for e in ents.values():
        if e.get('entity_type') in CLASS_TYPES:
            fail('V1', u'%s 가 아직 상자다. 공급원·매출원은 분류다' % e['id'])

    base = os.path.join(DATA, 'chains')
    chains = sorted(d for d in os.listdir(base)
                    if os.path.exists(os.path.join(base, d, 'relationships.json')))
    strict = set(shipped_chains())
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
        unalloc = set(k for k, x in list(ss.items()) + list(rt.items()) if x.get('unallocated'))

        def soft(code, msg):
            if cid in strict:
                fail(code, msg)
            else:
                debt[cid] = debt.get(cid, 0) + 1

        for reg in (ss, rt):
            for x in reg.values():
                lab = x.get('label') or ''
                if x.get('unallocated') and (u'기타' in lab or 'other' in lab.lower()):
                    fail('V6', u'%s 의 %s 가 기타와 미상을 한 칸에 담았다' % (cid, x['id']))
                check_shares(fail, u'%s·%s' % (cid, x['id']), x.get('shares') or [])

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
            has_src = bool(r.get('source_ids') or []) or r['id'] in evid
            if r.get('evidence_level') in ('CONFIRMED', 'ESTIMATED') and not has_src:
                soft('V11', u'%s 의 %s 가 출처 없이 %s 라고 적혔다'
                     % (cid, r['id'], r['evidence_level']))
            # V12 — 미상이 아닌 분류에 귀속했으면 그 줄에 근거가 있어야 한다
            mapped = set(r.get('supply_source_ids') or []) \
                | set(r.get('revenue_type_ids') or [])
            if (mapped - unalloc) and not has_src:
                soft('V12', u'%s 의 %s 가 근거 없이 %s 에 귀속됐다. 미상으로 두거나 출처를 단다'
                     % (cid, r['id'], ', '.join(sorted(mapped - unalloc))))
            # V13 — 타겟에서 나가는 다운스트림 줄에는 계약 고객 근거 칸이 선다
            if r.get('lane') == 'DOWNSTREAM' and r['source_entity'] == focal:
                v = r.get('contractual_customer')
                if v not in CONTRACTUAL:
                    soft('V13', u'%s 의 %s 에 contractual_customer 가 %s 다 (%s 중 하나)'
                         % (cid, r['id'], v, '·'.join(sorted(CONTRACTUAL))))
            # V14 — 귀속별 등급(revenue_type_map·supply_source_map)은 ids 안의 분류만
            # 가리키고, 등급·출처가 있어야 한다. 배분 %는 비공개면 비워 둔다
            for mk, ik in (('revenue_type_map', 'revenue_type_ids'),
                           ('supply_source_map', 'supply_source_ids')):
                for mp in r.get(mk) or []:
                    if mp.get('id') not in (r.get(ik) or []):
                        fail('V14', u'%s 의 %s 가 %s 밖의 %s 에 귀속 등급을 적었다'
                             % (cid, r['id'], ik, mp.get('id')))
                    if mp.get('status') not in ('CONFIRMED', 'ESTIMATED', 'INFERRED',
                                                'UNDISCLOSED'):
                        fail('V14', u'%s 의 %s 귀속 %s 에 등급이 없다' % (cid, r['id'], mp.get('id')))
                    if not mp.get('source_ids'):
                        fail('V14', u'%s 의 %s 귀속 %s 에 출처가 없다' % (cid, r['id'], mp.get('id')))
            for k in ('source_entity', 'target_entity'):
                t = r.get('source_tier' if k == 'source_entity' else 'target_tier')
                if (ents.get(r[k], {}).get('entity_type') == 'project_spv'
                        and t in STAGE_TIERS):
                    fail('V10', u'%s 의 %s 가 프로젝트 법인에 사슬 층 %s 를 줬다. '
                                u'칸은 이어진 꼴이 정한다' % (cid, r['id'], t))

        # V8 — 중개는 데이터가 준 노릇, 닫힘은 타겟에서 앞으로 이어진 꼴로 잰다.
        # 타겟에서 다운스트림으로 닿는 중개마다 뒤에 상자가 하나는 있어야 한다.
        # 실명이 없으면 INDIRECT_CUSTOMER_UNDISCLOSED 로 「간접 고객 미상」에 닫는다
        fwd = {}
        for r in rels:
            if r.get('lane') == 'DOWNSTREAM':
                fwd.setdefault(r['source_entity'], []).append(r)
        mid = set()
        for r in rels:
            if r.get('target_tier') == 'INTERMEDIARY':
                mid.add(r['target_entity'])
            if r.get('source_tier') == 'INTERMEDIARY':
                mid.add(r['source_entity'])
        reached, q = {focal}, [focal]
        while q:
            cur = q.pop(0)
            for r in fwd.get(cur, []):
                if r['target_entity'] not in reached:
                    reached.add(r['target_entity'])
                    q.append(r['target_entity'])
        for m in sorted(mid & reached):
            if m == focal:
                continue
            outs = [r for r in fwd.get(m, []) if r['target_entity'] != focal]
            if not outs:
                fail('V8', u'%s 의 중개 %s 뒤에 간접 고객이 없다. 실명이 없으면 '
                           u'INDIRECT_CUSTOMER_UNDISCLOSED 로 「간접 고객 미상」에 닫는다'
                     % (cid, m))
            for r in outs:
                if r['relationship_type'] == UNDISCLOSED_REL \
                        and not ents.get(r['target_entity'], {}).get('anon'):
                    fail('V8', u'%s 의 %s 가 미상 자리표에 실명 상자 %s 를 앉혔다'
                         % (cid, r['id'], r['target_entity']))

        # V10 — 프로젝트는 별도 맥락 파일. 식구는 명시하고, 타겟은 식구가 아니며,
        # 프로젝트 id 는 관계의 끝점이 아니다
        ppath = os.path.join(cdir, 'projects.json')
        projs = rd(ppath) if os.path.exists(ppath) else []
        endpoints = set()
        for r in rels:
            endpoints.add(r['source_entity'])
            endpoints.add(r['target_entity'])
        seen_pid = set()
        for p in projs:
            pid = p.get('id')
            if not pid or pid in seen_pid:
                fail('V10', u'%s 의 프로젝트 id 가 비었거나 겹친다 (%s)' % (cid, pid))
            seen_pid.add(pid)
            if pid in ents or pid in endpoints:
                fail('V10', u'%s 의 프로젝트 %s 가 상자 id 와 겹치거나 관계의 끝점이다'
                     % (cid, pid))
            mem = p.get('members') or []
            if not mem:
                fail('V10', u'%s 의 프로젝트 %s 에 식구가 없다' % (cid, pid))
            if focal in mem:
                fail('V10', u'%s 의 프로젝트 %s 가 타겟을 식구로 넣었다' % (cid, pid))
            for m in mem:
                if m not in ents:
                    fail('V10', u'%s 의 프로젝트 %s 식구 %s 가 없는 상자다' % (cid, pid, m))
                elif m not in endpoints:
                    fail('V10', u'%s 의 프로젝트 %s 식구 %s 가 이 사슬의 관계에 없다'
                         % (cid, pid, m))
        # 프로젝트 법인이 관계에 있는데 어느 테두리에도 안 들었으면 맥락이 빠진 것이다
        for eid in sorted(endpoints):
            if ents.get(eid, {}).get('entity_type') != 'project_spv':
                continue
            if not any(eid in (p.get('members') or []) for p in projs):
                soft('V10', u'%s 의 프로젝트 법인 %s 가 projects.json 의 어느 식구도 아니다'
                     % (cid, eid))

        # V9 — 같은 회사가 분류마다 복제됐나
        names = {}
        for i in endpoints:
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

    return fails, debt, {'chains': len(chains), 'rels': nrel}


def main():
    fails, debt, st = validate()
    for f in fails[:40]:
        print(f)
    for cid in sorted(debt):
        print(u'빚 %s — 안 실린 사슬의 어긋남 %d건' % (cid, debt[cid]))
    print(u'요약: 사슬 %d · 관계 %d / FAIL %d' % (st['chains'], st['rels'], len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
