# -*- coding: utf-8 -*-
u"""v2 → v2.1 이행. 멱등이라 여러 번 돌려도 같다.

① 다운스트림 관계에 contractual_customer 를 적는다 — 계약상 구매 주체인지는 화면의 칸이
   아니라 근거 칸이다(프레임워크 §22-B). 칸(직접·중개·간접)은 타겟에서 이어진 꼴이 정한다.
     CONFIRMED        계약상 구매 주체라는 근거가 있다 (옛 target_tier CONTRACTUAL_CUSTOMER)
     NOT_CONTRACTUAL  구매 주체가 아니라고 원문이 말한다 (SEC 의 customer's customer)
     UNVERIFIED       설치처·수요 노출·인증·공급망 목록 — 계약상 구매 주체라는 근거가 없다
② 프로젝트를 별도 맥락 파일 chains/<사슬>/projects.json 으로 뺀다. SPV·부지는 실제 법인이라
   상자로 남고, 프로젝트는 명시한 식구를 두르는 테두리다. 관계의 끝점이 되지 않는다.
   식구 목록은 손으로 정한다 — 관계로 추론하지 않는다. 여기서는 블룸 사슬만 세운다.
③ 계약 상대가 미확인(UNVERIFIED)인 부지·SPV(project_spv)는 직접 고객 칸에 세우지 않는다.
   설치 부지는 물건이 놓이는 자리지 돈을 내는 상대가 아니다. 타겟 → 「계약 상대 미상」
   자리표 → 부지로 옮겨, 자리표가 직접 고객 칸에 서고 부지는 그 다음 칸으로 간다.
   간접 고객 미상(vc_norm ⑤)과 같은 꼴이다. check_vc V15 가 문다.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')

# 타겟에서 나가는 다운스트림 관계의 종류마다 계약 고객 근거 상태
CONTRACTUAL = {
    'CUSTOMERS_CUSTOMER': 'NOT_CONTRACTUAL',
    'END_CUSTOMER_SUPPLY_CHAIN': 'UNVERIFIED',
    # 제휴와 실증은 물건을 판 자리가 아니다. 원문이 계약 고객이라 적지 말라고 못박았다
    'SYSTEM_INTEGRATION_PARTNERSHIP': 'NOT_CONTRACTUAL',
    'DEMONSTRATION_DEPLOYMENT': 'NOT_CONTRACTUAL',
    # 자사 설비 배치(네비우스가 제 데이터센터에 GPU 를 놓는다) — 고객이 아니다
    'DEPLOYS_AT': 'NOT_CONTRACTUAL',
}

CONTRACT_PH_REL = 'CONTRACT_PARTY_UNDISCLOSED'

PROJECTS = {
    'bloom-energy': [
        {'id': 'proj-jupiter', 'name': 'Project Jupiter', 'name_ko': '프로젝트 주피터',
         'site': 'project-jupiter', 'developer': 'borderplex',
         'ultimate_end_user': 'oracle',
         'members': ['project-jupiter', 'borderplex', 'oracle'],
         'note': 'LS일렉트릭은 부지 전기 공급사라 타겟 왼쪽에 서므로 식구에 넣지 않는다. '
                 '선은 그대로 닿는다',
         'from_relationships': ['bloom-jupiter', 'borderplex-jupiter', 'jupiter-oracle',
                                'lselectric-jupiter']},
        {'id': 'proj-sk-eternix-80mw', 'name': 'SK Eternix 80MW Korea project',
         'name_ko': '충주·대소원 80MW', 'site': 'sk-eternix-80mw', 'developer': 'sk-eternix',
         'members': ['sk-eternix-80mw', 'sk-eternix'],
         'from_relationships': ['eternix-80mw-spv', 'bloom-eternix']},
        {'id': 'proj-aep-ohio', 'name': 'AEP Ohio onsite projects',
         'name_ko': 'AEP 오하이오 온사이트', 'developer': 'aep-ohio',
         'members': ['aep-ohio', 'aws', 'cologix'],
         'note': 'AEP 오하이오가 설치를 맡고 AWS·콜로직스가 장기 계약으로 비용을 댄다. '
                 '부지별 용량은 따로 공개되지 않았다',
         'from_relationships': ['aep-aepohio', 'aepohio-aws', 'aepohio-cologix']},
        {'id': 'proj-omika', 'name': 'Hitachi Omika Works pilot',
         'name_ko': '오미카 실증', 'site': 'hitachi-omika-works', 'developer': 'hitachi',
         'members': ['hitachi-omika-works', 'hitachi'],
         'note': '블룸 연료전지에 히타치 제어를 붙인 실증. 용량은 비공개다',
         'from_relationships': ['bloom-omika', 'hitachi-omika']},
        {'id': 'proj-bfjv-spv', 'name': 'Brookfield Fund JV project SPV',
         'name_ko': '펀드 JV 프로젝트 법인', 'site': 'bfjv-spv-unknown',
         'financier': 'brookfield-fund-jvs',
         'members': ['bfjv-spv-unknown', 'brookfield-fund-jvs'],
         'from_relationships': ['fundjv-spv', 'bloom-fundjv-sales']},
        {'id': 'proj-volo', 'name': 'Volo, Illinois Data Center', 'name_ko': '볼로 데이터센터',
         'site': 'volo-datacenter', 'members': ['volo-datacenter', 'chirisa', 'coreweave'],
         'from_relationships': ['chirisa-volo', 'coreweave-volo', 'bloom-volo']},
        {'id': 'proj-mitac', 'name': 'MiTAC manufacturing sites (Fremont, San Jose)',
         'name_ko': 'MiTAC 제조 부지(프리몬트·산호세)',
         'members': ['mitac-fremont', 'mitac-sanjose', 'mitac-computing'],
         'note': '부지 둘을 한 회사가 굴린다. 따로 두르면 테두리 둘이 같은 상자에 겹친다',
         'from_relationships': ['mitac-fremont-site', 'mitac-sanjose-site',
                                'bloom-mitac-fremont', 'bloom-mitac-sanjose']},
    ],
}


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def wr(p, obj):
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write('\n')


def main():
    base = os.path.join(DATA, 'chains')
    ep = os.path.join(DATA, 'entities.json')
    ent_list = rd(ep)
    ents = dict((e['id'], e) for e in ent_list)
    for ck in sorted(os.listdir(base)):
        cdir = os.path.join(base, ck)
        rp = os.path.join(cdir, 'relationships.json')
        if not os.path.exists(rp):
            continue
        meta = rd(os.path.join(cdir, 'chain.json')) if os.path.exists(
            os.path.join(cdir, 'chain.json')) else {}
        focal = meta.get('focal_entity')
        if not focal:
            cls = rd(os.path.join(cdir, 'classifications.json'))
            focal = cls.get('focal_entity')
        rels = rd(rp)
        n = 0
        for r in rels:
            if r.get('lane') != 'DOWNSTREAM' or r.get('source_entity') != focal:
                continue
            t = r.get('relationship_type')
            # 종류가 표에 있으면 표가 이긴다(자사 설비를 미확인 고객으로 적었던 값을 바로잡는다)
            if r.get('contractual_customer') and t not in CONTRACTUAL:
                continue
            if t in CONTRACTUAL:
                v = CONTRACTUAL[t]
            elif r.get('target_tier') == 'CONTRACTUAL_CUSTOMER':
                v = 'CONFIRMED'
            else:
                v = 'UNVERIFIED'
            if r.get('contractual_customer') != v:
                r['contractual_customer'] = v
                n += 1
        rels, moved = contract_placeholder(ck, focal, rels, ents, ent_list)
        wr(rp, rels)
        pp = os.path.join(cdir, 'projects.json')
        if ck in PROJECTS:
            # 출처는 식구를 잇는 관계에서 모은다. 새로 지어내지 않는다
            by_id = dict((r['id'], r) for r in rels)
            rows = []
            for p in PROJECTS[ck]:
                q = dict(p)
                src = []
                for rid in q.pop('from_relationships', []):
                    for s in (by_id.get(rid, {}).get('source_ids') or []):
                        if s not in src:
                            src.append(s)
                q['source_ids'] = src
                rows.append(q)
            wr(pp, rows)
        elif not os.path.exists(pp):
            wr(pp, [])
        print(u'%s — 계약 고객 근거 %d줄 적음, 프로젝트 %d, 계약 상대 미상 뒤 부지 %d' % (
            ck, n, len(PROJECTS.get(ck, [])), moved))
    wr(ep, ent_list)


def contract_placeholder(ck, focal, rels, ents, ent_list):
    u"""③. 멱등 — 자리표 관계는 매번 다시 세우고, 이미 옮긴 줄은 그대로 둔다."""
    ph = ck + '-contract-undisclosed'
    open_id = ph + '-open'
    rels = [r for r in rels if r['id'] != open_id]
    moved = [r for r in rels if r.get('lane') == 'DOWNSTREAM'
             and r.get('contractual_customer') == 'UNVERIFIED'
             and r.get('source_entity') in (focal, ph)
             and (ents.get(r['target_entity']) or {}).get('entity_type') == 'project_spv']
    if not moved:
        return rels, 0
    if ph not in ents:
        e = {'id': ph, 'name': 'Undisclosed contract party', 'name_ko': u'계약 상대 미상',
             'entity_type': 'company', 'anon': True, 'country': None,
             'legal_name': u'계약 상대 미상(비공개)', 'display_name': u'계약 상대 미상',
             'desc': u'설비가 이 부지에 놓인 것은 확인되나 누구와 계약했는지 원문이 밝히지 않았다',
             'categories': [], 'primary_role': u'미상', 'other_roles': [],
             'parent_entity_id': None, 'region': None}
        ents[ph] = e
        ent_list.append(e)
    src, rt, vf = [], [], []
    for r in moved:
        r['source_entity'] = ph
        r['source_role'] = u'계약 상대 미상'
        for s in r.get('source_ids') or []:
            if s not in src:
                src.append(s)
        for s in r.get('revenue_type_ids') or []:
            if s not in rt:
                rt.append(s)
        vf.append(r.get('valid_from'))
    rels.append({
        'id': open_id, 'source_entity': focal, 'target_entity': ph,
        'relationship_type': CONTRACT_PH_REL, 'lane': 'DOWNSTREAM',
        'subsystem': None, 'component': None,
        'source_role': u'제조사', 'target_role': u'계약 상대',
        # 옮긴 줄 가운데 하나라도 시작이 비면 자리표도 비운다 — 어느 해에도 선다
        'valid_from': min(vf) if all(vf) else None, 'valid_to': None,
        'status': 'ACTIVE', 'evidence_level': 'UNDISCLOSED',
        'source_tier': None, 'target_tier': 'CONTRACTUAL_CUSTOMER',
        'confidence_band': 'low', 'flows': [], 'source_ids': src,
        'supply_source_ids': [], 'revenue_type_ids': rt,
        'contractual_customer': 'UNVERIFIED',
        'notes': u'부지 %d곳에 설비가 놓였는데 계약 상대를 원문이 밝히지 않았다. 자리표로 잇는다'
                 % len(moved)})
    return rels, len(moved)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
