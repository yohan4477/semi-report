# -*- coding: utf-8 -*-
"""반도체 기판 사슬 — 대덕전자를 중심으로.

블룸 사슬과 섞지 않는다. 두 사슬은 겹치는 회사가 없다.
근거는 저장소에 이미 있는 원문 둘뿐이다. 그 밖의 관계는 만들지 않는다.

  content/semi_doped/clips/daily/2026-05-22--daily-update-may-22nd-2026.md
  content/understanding/한주성/2026-05-18 모래가 반도체 칩이 되기까지 2편 '후공정' [2592].md
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'kr-substrate')

SOURCES = [
 ('semidoped_2026_05_22', 'Semi Doped', 'Daily update — 2026-05-22', 'reputable_media',
  '2026-05-22', 'https://www.thelec.net/news/articleView.html?idxno=10639',
  '대덕전자가 FC-CSP·FC-BGA·AI 기판 생산능력을 함께 늘리는 데 8,000억 원 넘게 쓴다. '
  '저장소 클립이 The Elec 기사를 인용한다'),
 ('semianalysis_li_2026_08_27', 'SemiAnalysis (링크드인)', '기판에 여유가 없다 — ABF 공급망',
  'industry_research', '2026-08-27',
  'https://www.linkedin.com/feed/update/urn:li:activity:7498545703879835648/',
  '2026 물량이 전부 예약됐고 공급사 여섯 곳 리드타임이 12~14개월. 재료도 빡빡하다 — '
  'T-glass 공급이 닛토보 한 곳에서 다섯 곳 이상으로 늘고, 기판용 CCL 은 거의 레조낙 '
  '한 곳에서만 나온다'),
 ('hanjuseong_backend_2026_05_18', '한주성', '모래가 반도체 칩이 되기까지 2편 후공정',
  'reputable_media', '2026-05-18', None,
  '삼성전기·대덕전자·심텍이 기판을 만들고 하나마이크론·네패스 같은 OSAT 가 패키징을 맡는다. '
  '다이싱은 이오테크닉스, 본딩 장비는 한미반도체'),
]

ENTITIES = [
 ('daeduck-electronics', 'Daeduck Electronics', '대덕전자', 'company', '한국', ['Substrate'],
  'FC-CSP·FC-BGA·AI 기판. 2026년 증설에 8,000억 원 넘게 쓴다'),
 ('samsung-electro-mechanics', 'Samsung Electro-Mechanics', '삼성전기', 'company', '한국',
  ['Substrate'], '패키지 기판'),
 ('simmtech', 'Simmtech', '심텍', 'company', '한국', ['Substrate'], '패키지 기판'),
 ('ccl-substrate', 'Substrate CCL', '기판용 CCL', 'material', None, ['Material'],
  '기판의 바탕이 되는 동박적층판. 거의 한 곳에서만 나오는 병목'),
 ('t-glass', 'T-glass', 'T-글라스', 'material', None, ['Material'],
  'ABF 기판의 두꺼운 제품과 BT 기판의 얇은 제품에 함께 쓰인다'),
 ('resonac', 'Resonac', '레조낙', 'company', '일본', ['Material'],
  '기판용 CCL 을 사실상 혼자 댄다'),
 ('nittobo', 'Nittobo', '닛토보', 'company', '일본', ['Material'],
  'T-글라스. 공급이 이 한 곳에서 다섯 곳 이상으로 늘고 있다'),
 ('hana-micron', 'Hana Micron', '하나마이크론', 'company', '한국', ['OSAT'],
  '외주 패키징·테스트'),
 ('nepes', 'Nepes', '네패스', 'company', '한국', ['OSAT'], '외주 패키징·테스트'),
 ('eo-technics', 'EO Technics', '이오테크닉스', 'company', '한국', ['Equipment'],
  '레이저 그루빙·스텔스 다이싱 장비. 일본 디스코 독점을 깼다'),
 ('hanmi-semiconductor', 'Hanmi Semiconductor', '한미반도체', 'company', '한국', ['Equipment'],
  'TC 본더. HBM 핵심 장비 점유율 1위'),
]

# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence_level, src_tier, tgt_tier, sources, notes)
R = [
 # ── 업스트림: 소재 ────────────────────────────────────────────────
 ('resonac-ccl', 'resonac', 'ccl-substrate', 'SUPPLIES', 'MANUFACTURING_BOM', 'Material',
  '기판용 동박적층판', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['semianalysis_li_2026_08_27'],
  '거의 이 한 곳에서만 나온다. EMC 가 2026년 4분기 출하를 준비한다'),
 ('nittobo-tglass', 'nittobo', 't-glass', 'SUPPLIES', 'MANUFACTURING_BOM', 'Material',
  'T-글라스 원사', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['semianalysis_li_2026_08_27'],
  '공급이 한 곳에서 다섯 곳 이상으로 늘고 있다. 중국 업체가 들어왔다'),
 ('ccl-daeduck', 'ccl-substrate', 'daeduck-electronics', 'INPUT_TO', 'MANUFACTURING_BOM',
  'Material', '기판용 CCL', '소재', '기판 제조', None, None, 'ACTIVE', 'INFERRED',
  'MATERIAL_PROCESSING', None, ['semianalysis_li_2026_08_27'],
  '원문은 ABF 기판 공급망 전체를 말한다. 이 회사가 어디서 받는지는 밝히지 않는다'),
 ('tglass-daeduck', 't-glass', 'daeduck-electronics', 'INPUT_TO', 'MANUFACTURING_BOM',
  'Material', 'T-글라스', '소재', '기판 제조', None, None, 'ACTIVE', 'INFERRED',
  'MATERIAL_PROCESSING', None, ['semianalysis_li_2026_08_27'], None),
 ('ccl-samsungem', 'ccl-substrate', 'samsung-electro-mechanics', 'INPUT_TO',
  'MANUFACTURING_BOM', 'Material', '기판용 CCL', '소재', '기판 제조', None, None, 'ACTIVE',
  'INFERRED', 'MATERIAL_PROCESSING', None, ['semianalysis_li_2026_08_27'], None),
 ('ccl-simmtech', 'ccl-substrate', 'simmtech', 'INPUT_TO', 'MANUFACTURING_BOM', 'Material',
  '기판용 CCL', '소재', '기판 제조', None, None, 'ACTIVE', 'INFERRED',
  'MATERIAL_PROCESSING', None, ['semianalysis_li_2026_08_27'], None),
 # ── 다운스트림 ───────────────────────────────────────────────────
 ('daeduck-hanamicron', 'daeduck-electronics', 'hana-micron', 'SUPPLIES', 'DOWNSTREAM',
  'OSAT', '패키지 기판', '기판 제조', '패키징', None, None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['hanjuseong_backend_2026_05_18'],
  '원문은 기판 회사와 OSAT 가 다이 어태치 단계를 나눠 맡는다고만 적는다. '
  '두 회사를 잇는 계약 문장은 없다'),
 ('daeduck-nepes', 'daeduck-electronics', 'nepes', 'SUPPLIES', 'DOWNSTREAM', 'OSAT',
  '패키지 기판', '기판 제조', '패키징', None, None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['hanjuseong_backend_2026_05_18'], None),
 ('samsungem-hanamicron', 'samsung-electro-mechanics', 'hana-micron', 'SUPPLIES',
  'DOWNSTREAM', 'OSAT', '패키지 기판', '기판 제조', '패키징', None, None, 'ACTIVE',
  'INFERRED', None, 'CONTRACTUAL_CUSTOMER', ['hanjuseong_backend_2026_05_18'],
  '같은 단계에 선 기판 회사다. 대덕전자와 나란히 둔다'),
 ('simmtech-hanamicron', 'simmtech', 'hana-micron', 'SUPPLIES', 'DOWNSTREAM', 'OSAT',
  '패키지 기판', '기판 제조', '패키징', None, None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['hanjuseong_backend_2026_05_18'], None),
 ('eotechnics-hanamicron', 'eo-technics', 'hana-micron', 'EQUIPMENT_SUPPLY',
  'MANUFACTURING_EQUIPMENT', 'Equipment', '레이저 그루빙·스텔스 다이싱 장비', '장비 공급',
  '패키징', None, None, 'ACTIVE', 'CONFIRMED', None, None,
  ['hanjuseong_backend_2026_05_18'], '다이싱 단계 국산화'),
 ('hanmi-hanamicron', 'hanmi-semiconductor', 'hana-micron', 'EQUIPMENT_SUPPLY',
  'MANUFACTURING_EQUIPMENT', 'Equipment', 'TC 본더', '장비 공급', '패키징', None, None,
  'ACTIVE', 'CONFIRMED', None, None, ['hanjuseong_backend_2026_05_18'],
  'HBM 본딩 장비 점유율 1위'),
]

O = [
 ('o-daeduck-capex-2026', 'daeduck-hanamicron', 'capex_investment', 800, None, None, 'KRW B',
  '2026', '2026-01-01', '2026-12-31', '2026-05-22', '대덕전자 기판 증설 투자액', 'CURRENT',
  'CONFIRMED', 0.9, None, ['semidoped_2026_05_22'],
  'FC-CSP·FC-BGA·AI 기판을 함께 늘린다. 어느 고객향인지는 밝혀지지 않았다'),
]

CLAIMS = [
 ('clm-daeduck-capex', '대덕전자는 FC-CSP·FC-BGA·AI 기판 증설에 8,000억 원 넘게 쓴다.',
  'daeduck-electronics', None, '2026', 'CONFIRMED', 0.9, ['semidoped_2026_05_22'], None),
 ('clm-ccl-bottleneck',
  '기판용 CCL 은 거의 레조낙 한 곳에서만 나와 공급망의 또 하나의 병목이다.',
  'resonac', 'daeduck-electronics', '2026-08', 'CONFIRMED', 0.8,
  ['semianalysis_li_2026_08_27'], 'EMC 가 2026년 4분기 출하를 준비하고 2027년 캐파를 두 배로 늘린다'),
 ('clm-tglass-widening',
  'T-글라스 공급이 닛토보 한 곳에서 다섯 곳 이상으로 늘고 있다.',
  'nittobo', 'daeduck-electronics', '2026-08', 'CONFIRMED', 0.8,
  ['semianalysis_li_2026_08_27'], '중국 업체가 공격적으로 들어왔다'),
 ('clm-substrate-leadtime',
  'ABF 기판은 2026년 물량이 전부 예약됐고 공급사 여섯 곳의 리드타임이 12~14개월이다.',
  'daeduck-electronics', None, '2026-08', 'CONFIRMED', 0.8,
  ['semianalysis_li_2026_08_27'], '층수가 20~24층까지 커져 한 장이 라인을 오래 문다'),
 ('clm-substrate-osat-split',
  '기판은 삼성전기·대덕전자·심텍이 만들고 패키징은 하나마이크론·네패스 같은 OSAT 가 맡는다.',
  'daeduck-electronics', 'hana-micron', '2026-05', 'INFERRED', 0.6,
  ['hanjuseong_backend_2026_05_18'], '단계를 나눠 맡는다는 서술이고 거래 관계 서술은 아니다'),
]


def ent(t):
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3], 'country': t[4],
            'categories': t[5], 'desc': t[6], 'anon': False}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-11', 'note': t[6]}


def rel(t):
    return {'id': t[0], 'source_entity': t[1], 'target_entity': t[2],
            'relationship_type': t[3], 'lane': t[4], 'subsystem': t[5], 'component': t[6],
            'source_role': t[7], 'target_role': t[8], 'valid_from': t[9], 'valid_to': t[10],
            'status': t[11], 'evidence_level': t[12],
            'source_tier': t[13], 'target_tier': t[14],
            'economic_importance': None, 'capacity_criticality': None,
            'integration_criticality': None,
            'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium'}.get(t[12], 'low'),
            'flows': [], 'source_ids': t[15], 'notes': t[16]}


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': t[15], 'source_ids': t[16],
            'method_note': t[17], 'denominator_scope': 'EDGE'}


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


def dump(path, o):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(o, ensure_ascii=False, indent=1))
        f.write(u'\n')


def merge(name, rows, key='id'):
    p = os.path.join(DATA, name)
    cur = json.load(io.open(p, encoding='utf-8'))
    have = set(x[key] for x in cur)
    for r in rows:
        if r[key] not in have:
            cur.append(r)
    dump(p, cur)
    return len(cur)


def evidence():
    out, n = [], 0
    for t in R:
        for sid in t[15]:
            n += 1
            out.append({'id': 'kr-e%03d' % n, 'relationship_id': t[0], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if t[12] == 'CONFIRMED' else 'indirect',
                        'evidence': t[16] or '', 'hypothesis_id': None})
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'kr-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid, 'evidence_type': 'direct',
                        'evidence': t[17] or '', 'hypothesis_id': None})
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'hypotheses.json'), [])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print('전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d'
          % (ne, ns, len(R), len(O)))
