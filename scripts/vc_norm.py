# -*- coding: utf-8 -*-
u"""밸류체인 데이터를 v2 꼴로 옮긴다 — 공급원·매출원은 상자가 아니라 분석축이다.

통합 밸류체인 분석 프레임워크 §22·§23(2026-09-11)이 정본이다.

  · 실제 회사·법인·공장·프로젝트만 entity 다. 공급 품목·제품군·계통은 분류다.
  · 분류는 chains/<사슬>/classifications.json 에 따로 서고, 관계는
    supply_source_ids[] · revenue_type_ids[] 로 N:M 으로 가리킨다.
  · 같은 공급사·고객을 분류마다 복제하지 않는다. 상자는 하나뿐이다.
  · 귀속 근거가 없으면 공급원 미상·배분 미상으로 닫는다. 임의 배분은 금지다.
  · 중개가 있으면 그 뒤에 간접 고객(실명 또는 미상)까지 사슬을 닫는다.

옮기는 일은 되풀이해도 같은 결과가 나온다(멱등). 분류 상자가 이미 걷힌 사슬은
관계에 빠진 매핑만 채우고 지나간다.
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')

# 분류로 옮겨 갈 상자 갈래 — 소재·부품·계통은 공급원, 매출 갈래는 매출원이다
SUPPLY_ENT = {'material': 'MATERIAL', 'component': 'COMPONENT', 'subsystem': 'SUBSYSTEM'}
REVENUE_ENT = {'revenue_type': 1}
# 거래 관계 — 매출원 귀속을 따질 자리다. 노출·인증·전방시장은 거래가 아니다
TRADE = {'SELLS_TO', 'DIRECT_CUSTOMER', 'END_CUSTOMER_SUPPLY_CHAIN',
         'DISTRIBUTION_PARTNERSHIP', 'CONTRACTUAL_CUSTOMER'}
# 공급 관계 — 공급원 귀속을 따질 자리다
SUPPLY_REL = {'SUPPLIES', 'MANUFACTURES', 'PROCESSING', 'PROCESSED_INTO', 'INPUT_TO',
              'INTEGRATED_INTO', 'SUBSYSTEM_SUPPLY', 'SUBSYSTEM_INTEGRATION',
              'SURFACE_TREATMENT', 'EMS_ASSEMBLY', 'COATING', 'FUELS',
              'EQUIPMENT_SUPPLY', 'ELECTRICAL_BOP_SUPPLY', 'INTERNAL_MATERIAL_SUPPLY',
              'INTRAGROUP_SUPPLY', 'JV_ASSEMBLY', 'CONTRACT_MANUFACTURES'}
DOWN = 'DOWNSTREAM'
UNALLOC_SS = 'ss-unallocated'
UNALLOC_RT = 'rt-unallocated'

SUB_LEVEL = {'Raw material': 'MATERIAL', 'Material': 'MATERIAL',
             'Material processing': 'MATERIAL', 'Operational input': 'OPERATIONAL',
             'Manufacturing equipment': 'EQUIPMENT', 'Site electrical BoP': 'INFRA'}
# 공급원 이름은 한국말로 세운다. 화면에 그대로 나가는 자리다
SUB_KO = {
    'Raw material': u'원재료', 'Operational input': u'운영 투입', 'Cell': u'셀·세라믹',
    'Other ceramic': u'기타 세라믹', 'Thermal': u'열·단열',
    'Interconnect': u'인터커넥트', 'Hotbox': u'핫박스',
    'Power electronics': u'전력 전자', 'Mechanical': u'기계·모듈',
    'Instrumentation': u'계측', 'Manufacturing equipment': u'제조 장비',
    'Site electrical BoP': u'부지 전기', 'Material': u'소재',
    'Material processing': u'소재·가공', 'Substrate': u'기판', 'Equipment': u'장비',
    'Assembly': u'조립', 'Integrator': u'통합', 'Foundry': u'파운드리',
    'Ceramic powder': u'세라믹 분말', 'Inductor material': u'인덕터 소재',
    'Plating': u'도금', 'MLCC manufacturing': u'MLCC 생산',
    'Memory': u'메모리', 'Networking': u'네트워킹', 'Packaging': u'패키징',
    'Power': u'전력', 'Interconnect fabric': u'인터커넥트 패브릭',
    'Optics': u'광 모듈', 'Cooling': u'냉각', 'Board': u'기판·보드',
    'System assembly': u'시스템 조립', 'Chassis': u'섀시',
    'Assembly & Test': u'후공정(조립·시험)', 'Cloud capacity': u'클라우드 용량',
    'Deposition & etch': u'증착·식각', 'Light source': u'광원',
    'Lithography': u'노광', 'Metrology': u'계측 장비',
    'Precision modules': u'정밀 모듈', 'Silicon wafer': u'실리콘 웨이퍼',
}


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def wr(p, rows):
    with io.open(p, 'w', encoding='utf-8') as f:
        f.write(json.dumps(rows, ensure_ascii=False, indent=1))
        f.write(u'\n')


def slug(s):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', (s or '').strip().lower()).strip('-')
    return s or 'x'


def chain_ids():
    base = os.path.join(DATA, 'chains')
    return sorted(d for d in os.listdir(base)
                  if os.path.isdir(os.path.join(base, d)))


# ── 분류 레지스트리 ──────────────────────────────────────────────────
def ss_entry(eid, ent):
    return {'id': 'ss-' + eid, 'kind': 'SUPPLY_SOURCE',
            'label': ent.get('name_ko') or ent.get('name') or eid,
            'label_en': ent.get('name') or None,
            'level': SUPPLY_ENT.get(ent.get('entity_type'), 'MATERIAL'),
            'note': ent.get('desc') or None,
            'unallocated': False, 'shares': [], 'source_ids': []}


def rt_entry(eid, ent):
    return {'id': 'rt-' + eid, 'kind': 'REVENUE_TYPE',
            'label': ent.get('name_ko') or ent.get('name') or eid,
            'label_en': ent.get('name') or None,
            'note': ent.get('desc') or None,
            'unallocated': eid.endswith('unallocated'),
            'shares': [], 'source_ids': []}


def obs_to_share(o):
    u"""관측 한 줄을 분류의 비중 한 줄로 옮긴다. 분모·기간은 그대로 들고 간다."""
    return {'metric': o.get('metric'), 'value': o.get('value'),
            'value_low': o.get('value_low'), 'value_high': o.get('value_high'),
            'unit': o.get('unit'), 'period': o.get('period'),
            'period_start': o.get('period_start'), 'period_end': o.get('period_end'),
            'as_of_date': o.get('as_of_date'), 'denominator': o.get('denominator'),
            'evidence_level': o.get('evidence_level'), 'confidence': o.get('confidence'),
            'method_note': o.get('method_note'), 'source_ids': o.get('source_ids') or []}


def normalize_chain(cid, ents):
    u"""사슬 하나를 v2 로 옮긴다. 쓰인 분류 상자 id 를 돌려준다."""
    cdir = os.path.join(DATA, 'chains', cid)
    rels = rd(os.path.join(cdir, 'relationships.json'))
    opath = os.path.join(cdir, 'observations.json')
    obs = rd(opath) if os.path.exists(opath) else []
    meta_p = os.path.join(cdir, 'chain.json')
    meta = rd(meta_p) if os.path.exists(meta_p) else {}
    focal = meta.get('focal_entity') or cid

    is_ss = lambda i: ents.get(i, {}).get('entity_type') in SUPPLY_ENT
    is_rt = lambda i: ents.get(i, {}).get('entity_type') in REVENUE_ENT

    # 한 번 옮긴 사슬을 다시 옮겨도 같은 결과가 나오게, 이미 선 분류는 들고 시작한다
    ss_reg, rt_reg = {}, {}
    cpath = os.path.join(cdir, 'classifications.json')
    if os.path.exists(cpath):
        old = rd(cpath)
        ss_reg = dict((x['id'], x) for x in old.get('supply_sources', []))
        rt_reg = dict((x['id'], x) for x in old.get('revenue_types', []))
    for r in rels:
        for i in (r['source_entity'], r['target_entity']):
            if is_ss(i) and 'ss-' + i not in ss_reg:
                ss_reg['ss-' + i] = ss_entry(i, ents[i])
            if is_rt(i) and 'rt-' + i not in rt_reg:
                rt_reg['rt-' + i] = rt_entry(i, ents[i])

    # ① 분류 상자를 지나가는 사슬을 실제 상자끼리 잇는 한 줄로 접는다.
    #    지나온 품목은 그 줄의 공급원으로 붙는다 — 단계를 지우는 것이 아니라
    #    품목 이름을 상자에서 떼어 분석축으로 옮기는 것이다
    out_of = {}
    for r in rels:
        out_of.setdefault(r['source_entity'], []).append(r)

    def walk(item, seen):
        u"""분류 상자에서 나가 처음 만나는 실제 상자들을 찾는다."""
        got = []
        for r in out_of.get(item, []):
            t = r['target_entity']
            if t in seen:
                continue
            if is_ss(t) or is_rt(t):
                got += [(dst, ['ss-' + t] + path, srcs + (r.get('source_ids') or []))
                        for dst, path, srcs in walk(t, seen | {t})]
            else:
                got.append((t, [], r.get('source_ids') or []))
        return got

    new, drop_ids, remap = [], set(), {}
    for r in rels:
        s, t = r['source_entity'], r['target_entity']
        if is_ss(s) or is_rt(s):
            drop_ids.add(r['id'])          # 분류에서 나가는 줄은 접힌 줄이 대신한다
            continue
        if is_rt(t):
            drop_ids.add(r['id'])          # 타겟→매출원 줄은 분류의 비중으로 간다
            continue
        if not is_ss(t):
            new.append(dict(r))
            continue
        hops = walk(t, {t})
        if not hops:
            drop_ids.add(r['id'])
            continue
        for k, (dst, path, srcs) in enumerate(hops):
            n = dict(r)
            n['id'] = r['id'] if k == 0 else '%s-%d' % (r['id'], k + 1)
            if k == 0:
                remap[r['id']] = n['id']
            n['target_entity'] = dst
            n['supply_source_ids'] = ['ss-' + t] + path
            n['source_ids'] = sorted(set((r.get('source_ids') or []) + srcs))
            n['target_tier'] = None
            new.append(n)

    # ② 매출원을 거치던 판매 줄은 타겟에서 고객으로 바로 잇고, 매출원은 분류로 붙인다
    for r in rels:
        s = r['source_entity']
        if not is_rt(s):
            continue
        n = dict(r)
        n['source_entity'] = focal
        n['revenue_type_ids'] = ['rt-' + s]
        n['source_tier'] = None
        new.append(n)

    # ③ 공급사가 안 밝혀진 품목은 「공급사 미상」에서 온 줄로 닫는다.
    #    품목 이름을 상자로 세우지 않으면서도 그 투입이 판에서 사라지지 않게 한다
    fed = set()
    for n in new:
        for x in n.get('supply_source_ids') or []:
            fed.add(x)
    orphan = []
    for r in rels:
        s, t = r['source_entity'], r['target_entity']
        if not is_ss(s) or is_ss(t) or is_rt(t):
            continue
        if ('ss-' + s) in fed:
            continue
        orphan.append((r, s, t))
    if orphan:
        ph = cid + '-supplier-undisclosed'
        ents.setdefault(ph, {
            'id': ph, 'name': 'Undisclosed supplier', 'name_ko': u'공급사 미상',
            'entity_type': 'company', 'anon': True, 'country': None,
            'legal_name': u'공급사 미상(비공개)', 'display_name': u'공급사 미상',
            'desc': u'그 품목을 누가 대는지 원문이 밝히지 않았다', 'categories': [],
            'primary_role': u'미상', 'other_roles': [], 'parent_entity_id': None})
        ents[ph].setdefault('legal_name', u'공급사 미상(비공개)')
        ents[ph]['legal_name'] = ents[ph]['legal_name'] or u'공급사 미상(비공개)'
        ents[ph]['display_name'] = ents[ph].get('display_name') or u'공급사 미상'
        for r, s, t in orphan:
            n = dict(r)
            n['id'] = r['id'] + '-src'
            n['source_entity'] = ph
            n['supply_source_ids'] = ['ss-' + s]
            n['evidence_level'] = 'UNDISCLOSED'
            n['source_tier'] = 'RAW_MATERIAL'
            n['notes'] = (r.get('notes') or '') or None
            new.append(n)

    # ④ 남은 줄에 공급원·매출원을 붙인다. 근거가 없으면 미상으로 닫는다.
    #    미상 칸이 사슬에 이미 서 있으면 그 칸을 쓴다 — 미상이 둘이면 같은 뜻의
    #    칸이 화면에 두 번 선다
    unalloc_ss = next((k for k, v in sorted(ss_reg.items()) if v.get('unallocated')),
                      UNALLOC_SS)
    unalloc_rt = next((k for k, v in sorted(rt_reg.items()) if v.get('unallocated')),
                      UNALLOC_RT)
    for n in new:
        n.setdefault('supply_source_ids', [])
        n.setdefault('revenue_type_ids', [])
        sub = n.get('subsystem')
        # 품목이 이미 붙은 줄에 계통 이름을 겹쳐 달지 않는다. 굵기가 다른 두 축을
        # 한 목록에 섞으면 같은 공급사가 두 번 걸린다
        if (n.get('lane') != DOWN and sub and not n['supply_source_ids']
                and n['relationship_type'] in SUPPLY_REL):
            sid = 'ss-' + slug(sub)
            if sid not in ss_reg:
                ss_reg[sid] = {'id': sid, 'kind': 'SUPPLY_SOURCE',
                               'label': SUB_KO.get(sub, sub), 'label_en': sub,
                               'level': SUB_LEVEL.get(sub, 'SUBSYSTEM'),
                               'note': None, 'unallocated': False, 'shares': [],
                               'source_ids': []}
            n['supply_source_ids'].append(sid)
        if (n.get('lane') != DOWN and not n['supply_source_ids']
                and n['relationship_type'] in SUPPLY_REL):
            n['supply_source_ids'] = [unalloc_ss]
        if (n.get('lane') == DOWN and not n['revenue_type_ids']
                and n['relationship_type'] in TRADE):
            n['revenue_type_ids'] = [unalloc_rt]
        if ents.get(n['target_entity'], {}).get('entity_type') == 'application':
            n['target_tier'] = 'END_MARKET'
        # 프로젝트는 사슬의 한 칸이 아니라 식구를 두르는 테두리다. 층을 주지 않는다
        for k, tk in (('source_entity', 'source_tier'), ('target_entity', 'target_tier')):
            if ents.get(n[k], {}).get('entity_type') == 'project_spv':
                n[tk] = None
        # 층은 타겟이 아닌 쪽을 가리키는 이름이다. 타겟으로 들어오는 줄에 붙은 층은
        # 보내는 쪽 것이다 — 안 옮기면 타겟이 제 사슬의 중개로 읽힌다
        if n['target_entity'] == focal and n.get('target_tier'):
            n['source_tier'] = n.get('source_tier') or n['target_tier']
            n['target_tier'] = None

    if any(unalloc_ss in n['supply_source_ids'] for n in new) and unalloc_ss == UNALLOC_SS:
        ss_reg[UNALLOC_SS] = {'id': UNALLOC_SS, 'kind': 'SUPPLY_SOURCE',
                              'label': u'공급원 미상', 'label_en': 'Unallocated',
                              'level': 'UNALLOCATED', 'unallocated': True,
                              'note': u'공급사인 것은 맞는데 무엇을 대는지 근거가 없다',
                              'shares': [], 'source_ids': []}
    if any(unalloc_rt in n['revenue_type_ids'] for n in new) and unalloc_rt == UNALLOC_RT:
        rt_reg[UNALLOC_RT] = {'id': UNALLOC_RT, 'kind': 'REVENUE_TYPE',
                              'label': u'배분 미상', 'label_en': 'Unallocated',
                              'unallocated': True,
                              'note': u'고객인 것은 맞는데 어느 매출에 드는지 근거가 없다',
                              'shares': [], 'source_ids': []}

    # ⑤ 중개 뒤는 간접 고객까지 닫는다. 실명이 없으면 「간접 고객 미상」이다
    mids = set(n['target_entity'] for n in new
               if n.get('lane') == DOWN and n.get('target_tier') == 'INTERMEDIARY'
               and n['target_entity'] != focal)
    closed = set(n['source_entity'] for n in new
                 if n.get('target_tier') in ('END_USER', 'END_MARKET'))
    openm = sorted(m for m in mids if m not in closed)
    if openm:
        ph = cid + '-indirect-undisclosed'
        ents.setdefault(ph, {
            'id': ph, 'name': 'Undisclosed indirect customer',
            'name_ko': u'간접 고객 미상', 'entity_type': 'end_user', 'anon': True,
            'country': None, 'legal_name': None, 'display_name': u'간접 고객 미상',
            'desc': u'중개 뒤에 누가 쓰는지 원문이 밝히지 않았다', 'categories': [],
            'primary_role': u'미상', 'other_roles': [], 'parent_entity_id': None})
        ents[ph]['legal_name'] = ents[ph].get('legal_name') or u'간접 고객 미상(비공개)'
        ents[ph]['display_name'] = ents[ph].get('display_name') or u'간접 고객 미상'
        for m in openm:
            new.append({'id': 'close-%s' % m, 'source_entity': m, 'target_entity': ph,
                        'relationship_type': 'INDIRECT_CUSTOMER_UNDISCLOSED',
                        'lane': DOWN, 'subsystem': None, 'component': None,
                        'source_role': u'중개', 'target_role': u'간접 고객',
                        'valid_from': None, 'valid_to': None, 'status': 'ACTIVE',
                        'evidence_level': 'UNDISCLOSED', 'source_tier': 'INTERMEDIARY',
                        'target_tier': 'END_USER', 'confidence_band': 'low',
                        'flows': [], 'source_ids': [],
                        'supply_source_ids': [], 'revenue_type_ids': [],
                        'notes': u'중개 뒤 실수요처를 원문이 밝히지 않았다. 사슬을 미상으로 닫는다'})

    # ⑥ 관측 — 매출원·공급원 비중은 분류로 옮기고, 접힌 줄의 관측은 새 줄로 잇는다
    keep_ids = set(n['id'] for n in new)
    nobs = []
    for o in obs:
        rid = o.get('relationship_id')
        src = next((r for r in rels if r['id'] == rid), None)
        if src and is_rt(src['target_entity']):
            key = 'rt-' + src['target_entity']
            if key in rt_reg:
                sh = obs_to_share(o)
                if sh not in rt_reg[key]['shares']:
                    rt_reg[key]['shares'].append(sh)
                rt_reg[key]['source_ids'] = sorted(
                    set(rt_reg[key]['source_ids']) | set(o.get('source_ids') or []))
            continue
        if rid in remap:
            o = dict(o)
            o['relationship_id'] = remap[rid]
        if o.get('relationship_id') and o['relationship_id'] not in keep_ids:
            continue
        nobs.append(o)

    for k, reg in (('rt-', rt_reg), ('ss-', ss_reg)):
        for e in reg.values():
            eid = e['id'][3:]
            src = ents.get(eid)
            if src and src.get('source_ids'):
                e['source_ids'] = sorted(set(e['source_ids']) | set(src['source_ids']))

    # 아무 줄도 안 가리키고 비중도 없는 분류는 걷는다. 빈 칸이 filter 에 서면
    # 눌러도 아무것도 안 걸린다
    ref_ss, ref_rt = set(), set()
    for n in new:
        ref_ss |= set(n.get('supply_source_ids') or [])
        ref_rt |= set(n.get('revenue_type_ids') or [])
    ss_reg = dict((k, v) for k, v in ss_reg.items()
                  if k in ref_ss or v.get('shares'))
    rt_reg = dict((k, v) for k, v in rt_reg.items()
                  if k in ref_rt or v.get('shares'))

    # ⑦ 근거 원장 — 접힌 줄은 새 줄로, 분류로 간 줄은 분류 id 로 다시 잇는다
    to_cls = {}
    for r in rels:
        if is_rt(r['target_entity']):
            to_cls[r['id']] = 'rt-' + r['target_entity']
        elif is_ss(r['source_entity']) or is_rt(r['source_entity']):
            to_cls.setdefault(r['id'], None)
    moved_obs = {}
    for o in obs:
        rid = o.get('relationship_id')
        if rid in to_cls and to_cls[rid]:
            moved_obs[o['id']] = to_cls[rid]
    epath = os.path.join(cdir, 'evidence.json')
    if os.path.exists(epath):
        evs = rd(epath)
        for e in evs:
            mid = e.get('metric_id')
            if mid and mid in moved_obs:
                e['metric_id'] = None
                e['classification_id'] = moved_obs[mid]
            rid = e.get('relationship_id')
            if rid in remap:
                e['relationship_id'] = remap[rid]
            elif rid and rid not in keep_ids:
                e['classification_id'] = e.get('classification_id') or to_cls.get(rid)
                e['relationship_id'] = None
            e.setdefault('classification_id', None)
        wr(epath, evs)
    # ⑧ 주장 — 품목을 가리키던 주어·목적어는 분류를 가리킨다
    kpath = os.path.join(cdir, 'claims.json')
    if os.path.exists(kpath):
        cls_rows = rd(kpath)
        for c in cls_rows:
            for k in ('subject', 'object'):
                v = c.get(k)
                if v and (is_ss(v) or is_rt(v)):
                    c[k] = None
                    c[k + '_classification'] = ('ss-' if is_ss(v) else 'rt-') + v
            c.setdefault('subject_classification', None)
            c.setdefault('object_classification', None)
        wr(kpath, cls_rows)

    cls = {'chain': cid, 'focal_entity': focal,
           'supply_sources': [ss_reg[k] for k in sorted(ss_reg)],
           'revenue_types': [rt_reg[k] for k in sorted(rt_reg)]}
    wr(os.path.join(cdir, 'classifications.json'), cls)
    wr(os.path.join(cdir, 'relationships.json'), new)
    if os.path.exists(opath):
        wr(opath, nobs)
    used = set(i for i in ents if is_ss(i) or is_rt(i))
    return used, len(new), len(ss_reg), len(rt_reg)


def main():
    ents = dict((e['id'], e) for e in rd(os.path.join(DATA, 'entities.json')))
    gone = set()
    for cid in chain_ids():
        if not os.path.exists(os.path.join(DATA, 'chains', cid, 'relationships.json')):
            continue
        used, nr, ns, nt = normalize_chain(cid, ents)
        gone |= used
        print(u'%-14s 관계 %3d · 공급원 %2d · 매출원 %2d' % (cid, nr, ns, nt))
    # 분류로 옮긴 상자는 전역 레지스트리에서도 걷는다
    left = [e for e in ents.values() if e['id'] not in gone]
    order = [e['id'] for e in rd(os.path.join(DATA, 'entities.json'))]
    rank = dict((i, k) for k, i in enumerate(order))
    left.sort(key=lambda e: rank.get(e['id'], 10 ** 6))
    wr(os.path.join(DATA, 'entities.json'), left)
    print(u'상자 %d개 남기고 분류 %d개를 걷었다' % (len(left), len(gone)))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
