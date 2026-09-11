# -*- coding: utf-8 -*-
"""구 data/valuechain/*.json 여섯 장을 새 체계로 옮긴다. 한 번만 돌린다.

  companies.json            → entities.json                 (전역)
  sources.json              → sources.json                   (전역)
  relationships.json        → chains/nvidia/relationships.json
  relationship_metrics.json → chains/nvidia/observations.json
  evidence.json             → chains/nvidia/evidence.json
  identity_hypotheses.json  → chains/nvidia/hypotheses.json
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'nvidia')

REL_TYPE = {
    'supplier': 'SUPPLIES', 'contract_manufacturer': 'CONTRACT_MANUFACTURES',
    'customer': 'SELLS_TO', 'end_market': 'SERVES_END_MARKET',
    'subsidiary': 'SUBSIDIARY_OF', 'credit_support': 'CREDIT_SUPPORT',
    'end_user': 'SERVES_END_USER', 'strategic_investment': 'INVESTS_IN',
}
LANE = {
    'SUPPLIES': 'MANUFACTURING_BOM', 'CONTRACT_MANUFACTURES': 'MANUFACTURING_BOM',
    'SELLS_TO': 'DOWNSTREAM', 'SERVES_END_MARKET': 'DOWNSTREAM',
    'SERVES_END_USER': 'DOWNSTREAM', 'CREDIT_SUPPORT': 'DOWNSTREAM',
    'INVESTS_IN': 'DOWNSTREAM', 'SUBSIDIARY_OF': 'CORPORATE',
}
# 관계의 근거 등급. 확정치가 아니라 그 관계를 어디까지 확인했는지다
EV_FROM_CONF = {'high': 'CONFIRMED', 'medium': 'ESTIMATED', 'low': 'INFERRED'}
# 다운스트림 층. 판매 사슬이 한 홉으로 납작해지지 않게 관계 종류에서 뽑는다
TIER = {'SELLS_TO': 'CONTRACTUAL_CUSTOMER', 'SERVES_END_MARKET': 'END_USER',
        'SERVES_END_USER': 'END_USER', 'CREDIT_SUPPORT': 'INTERMEDIARY',
        'INVESTS_IN': 'INTERMEDIARY'}
# 관측의 근거 등급
EV_FROM_EST = {'disclosed': 'CONFIRMED', 'derived': 'ESTIMATED',
               'analyst_estimate': 'ESTIMATED', 'industry_knowledge': 'INFERRED'}
PCT = set(['%', 'percent'])


def load(name):
    with io.open(os.path.join(DATA, name + '.json'), encoding='utf-8') as f:
        return json.load(f)


def dump(path, obj):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))
        f.write(u'\n')


def main():
    cos = load('companies')
    rels = load('relationships')
    mets = load('relationship_metrics')
    ents = []
    for c in cos:
        e = dict(c)
        e['entity_type'] = 'company'
        e['categories'] = []
        ents.append(e)
    # 카테고리는 관계의 subsystem 에서 모은다
    bycat = {}
    for r in rels:
        bycat.setdefault(r['source_company_id'], set()).add(r['category'])
    for e in ents:
        e['categories'] = sorted(bycat.get(e['id'], []))

    # 기간 중 가장 최근 것만 CURRENT, 나머지는 HISTORICAL
    last = max(m['period_end'] for m in mets)

    out_rel = []
    for r in rels:
        t = REL_TYPE[r['relationship_type']]
        out_rel.append({
            'id': r['id'],
            'source_entity': r['source_company_id'],
            'target_entity': r['target_company_id'],
            'relationship_type': t,
            'lane': LANE[t],
            'subsystem': r['category'],
            'component': r['product'],
            'source_role': None,
            'target_role': None,
            'flows': r.get('flows') or [],
            'valid_from': None,
            'valid_to': None,
            'status': 'ACTIVE',
            'target_tier': (TIER.get(t, 'CONTRACTUAL_CUSTOMER')
                            if LANE[t] == 'DOWNSTREAM' else None),
            'source_tier': ('COMPONENT_SUPPLIER'
                            if LANE[t] == 'MANUFACTURING_BOM' else None),
            'evidence_level': EV_FROM_CONF[r['confidence']],
            'confidence_band': r['confidence'],
            'notes': r.get('notes'),
        })

    out_obs = []
    for m in mets:
        unit = m.get('unit')
        out_obs.append({
            'id': m['id'],
            'relationship_id': m['relationship_id'],
            'metric': m['metric'],
            'value': m['value'],
            'unit': unit,
            'period': m['period'],
            'period_start': m['period_start'],
            'period_end': m['period_end'],
            'as_of_date': m['period_end'],
            'denominator': m.get('basis') if unit in PCT else m.get('basis'),
            'status': 'CURRENT' if m['period_end'] == last else 'HISTORICAL',
            'evidence_level': EV_FROM_EST[m['estimate_type']],
            'confidence': None,
            'method_id': None,
            'method_note': m.get('method'),
            'source_ids': [],
        })
    # 근거에 달린 출처를 관측에 끌어올린다
    evs = load('evidence')
    by_met = {}
    for e in evs:
        if e.get('metric_id'):
            by_met.setdefault(e['metric_id'], []).append(e['source_id'])
    for o in out_obs:
        o['source_ids'] = sorted(set(by_met.get(o['id'], [])))

    dump(os.path.join(DATA, 'entities.json'), ents)
    dump(os.path.join(DATA, 'sources.json'), load('sources'))
    dump(os.path.join(DATA, 'methods.json'), [])
    dump(os.path.join(CHAIN, 'relationships.json'), out_rel)
    dump(os.path.join(CHAIN, 'observations.json'), out_obs)
    dump(os.path.join(CHAIN, 'evidence.json'), evs)
    dump(os.path.join(CHAIN, 'hypotheses.json'), load('identity_hypotheses'))
    print('entities %d / relationships %d / observations %d / evidence %d'
          % (len(ents), len(out_rel), len(out_obs), len(evs)))


if __name__ == '__main__':
    main()
