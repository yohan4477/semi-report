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
}

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
            if r.get('contractual_customer'):
                continue
            t = r.get('relationship_type')
            if t in CONTRACTUAL:
                v = CONTRACTUAL[t]
            elif r.get('target_tier') == 'CONTRACTUAL_CUSTOMER':
                v = 'CONFIRMED'
            else:
                v = 'UNVERIFIED'
            r['contractual_customer'] = v
            n += 1
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
        print(u'%s — 계약 고객 근거 %d줄 적음, 프로젝트 %d' % (
            ck, n, len(PROJECTS.get(ck, []))))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
