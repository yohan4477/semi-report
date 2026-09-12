# -*- coding: utf-8 -*-
u"""엔비디아 사슬을 실을 수 있게 빚을 갚는다. 멱등.

nvidia 사슬은 v1 여섯 장에서 migrate_vc.py 로 옮겨 온 것이라 빌더가 없다. 이 스크립트가
그 위에 얹는 유일한 손질이다. 관계를 지어내지 않는다 — 출처가 있는 것은 출처를 잇고,
없는 것은 등급을 INFERRED 로 내리고 귀속을 미상으로 닫는다(프레임워크 §3-H·§23).

  r202 nvidia → coreweave   코어위브 10-K 가 「쓰는 GPU 는 전부 NVIDIA」라고 적었다 → sec_crwv_10k_fy2025
  r207 nvidia → nebius      네비우스·NVIDIA 제휴 발표 → ne_nvidia
  r206 nvidia → lambda_labs 보도자료를 적었으나 원장에 출처가 없다 → INFERRED
  r107 quanta → nvidia      실적발표의 AI 서버 서술로 이은 것 → INFERRED, 공급원 미상
  r108 wiwynn → nvidia      같다
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAIN = os.path.join(ROOT, 'data', 'valuechain', 'chains', 'nvidia')
UNALLOC_SS = 'ss-unallocated'


def rd(p):
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def wr(p, o):
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(o, f, ensure_ascii=False, indent=1)
        f.write('\n')


def main():
    rp = os.path.join(CHAIN, 'relationships.json')
    rels = rd(rp)
    by = dict((r['id'], r) for r in rels)

    def add_src(rid, sid):
        r = by[rid]
        r['source_ids'] = sorted(set((r.get('source_ids') or []) + [sid]))

    add_src('r202', 'sec_crwv_10k_fy2025')
    add_src('r207', 'ne_nvidia')
    by['r206']['evidence_level'] = 'INFERRED'
    by['r206']['confidence_band'] = 'low'
    by['r206']['notes'] = (u'보도자료가 클라우드 파트너로 이름을 적었다고 조사에 적혔으나 원장에 '
                          u'출처가 없어 추론으로 둔다. 매입 규모는 없다')
    for rid in ('r107', 'r108'):
        r = by[rid]
        r['evidence_level'] = 'INFERRED'
        r['confidence_band'] = 'low'
        r['supply_source_ids'] = [UNALLOC_SS]
        r['notes'] = ((r.get('notes') or u'') + u' 서로를 공시에 적지 않아 후공정 귀속 근거가 없다. '
                      u'공급원 미상으로 닫는다').strip()
    wr(rp, rels)

    cp = os.path.join(CHAIN, 'classifications.json')
    cls = rd(cp)
    if not any(x['id'] == UNALLOC_SS for x in cls['supply_sources']):
        cls['supply_sources'].append({
            'id': UNALLOC_SS, 'kind': 'SUPPLY_SOURCE', 'label': u'공급원 미상',
            'label_en': 'Unallocated', 'level': 'UNALLOCATED', 'unallocated': True,
            'note': u'공급사인 것은 맞는데 무엇을 대는지 근거가 없다', 'shares': [],
            'source_ids': []})
        cls['supply_sources'].sort(key=lambda x: x['id'])
    wr(cp, cls)

    mp = os.path.join(CHAIN, 'chain.json')
    if not os.path.exists(mp):
        wr(mp, {'id': 'nvidia', 'focal_entity': 'nvidia', 'label': u'엔비디아',
                'note': u'AI 가속기 회사 한 곳을 중심으로 세운 사슬. FY2026 10-K 가 앵커다'})
    print(u'nvidia — 출처 2줄, 추론으로 내림 3줄, chain.json %s' % ('있음' if os.path.exists(mp) else '없음'))


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
