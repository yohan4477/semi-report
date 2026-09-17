"""공시 줄 → data/ownership/hanwha.json(그래프). 판단은 여기서만 한다.

정본   hanwha.ftc.json — 공정위 대규모기업집단현황공시(대표회사용) 3.(1) 소유지분현황.
       계열사 전부가 같은 기준일(금년도 지정일)이다. 선의 값은 보통주 지분율(의결권), 합계 지분율은 곁에.
뒤값   hanwha.raw.json — DART 정기보고서 최대주주현황(2026 반기, 06-30). 같은 선이 있으면 later 로
       붙이고 0.1%p 넘게 달라졌으면 moved. 정본을 덮어쓰지 않는다 — 기준일이 섞이면 합이 안 맞는다.
부모   회사마다 동일인측 주주(일가·계열사) 중 보통주 지분이 가장 큰 하나. 도해의 나무는 부모 선,
       나머지 동일인측 선은 보조선. 임원·자기주식·그룹 밖 주주는 영수증 칸에만.
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from collect import norm, BY_NAME  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'data' / 'ownership'
DART = 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo='
FAMILY_CATS = {'동일인', '배우자/혈족1촌', '혈족2~4촌', '인척 3촌 이내', '기타 친족'}
MOVED = 0.1


def label(raw):
    """화면에 쓰는 이름 — 법인 표기만 떼고 띄어쓰기는 남긴다(해외 법인명)."""
    return re.sub(r'\s+', ' ', re.sub(r'\(주\)|㈜|주식회사', '', raw)).strip()


def code_for(name, filer_codes):
    cands = BY_NAME.get(norm(name), [])
    hit = [c for c in cands if c[0] in filer_codes] or [c for c in cands if c[2]] or (cands if len(cands) == 1 else [])
    return hit[0][0] if hit else None


def main():
    ftc = json.loads((D / 'hanwha.ftc.json').read_text(encoding='utf-8'))
    raw = json.loads((D / 'hanwha.raw.json').read_text(encoding='utf-8'))
    filers = raw['corps']
    src_ftc = {'label': ftc['report_nm'], 'url': ftc['url'], 'basis': ftc['basis'], 'rcept_dt': ftc['rcept_dt']}

    # DART 반기 최대주주현황 — (주주, 회사) → 값
    later = {}
    for h in raw['holdings']:
        if h['kind'] == 'hyslr' and h['pct'] is not None:
            key = (norm(h['holder']), norm(filers[h['target']]['name']))
            if key not in later or later[key]['asof'] < h['asof']:
                later[key] = {'pct': h['pct'], 'asof': h['asof'], 'url': DART + h['rcept_no'],
                              'label': f"{filers[h['target']]['name']} 정기보고서 최대주주현황"}

    companies = sorted({norm(o['company']) for o in ftc['owners']})
    nodes = {}
    for c in companies:
        code = code_for(c, filers)
        nodes[c] = {'id': c, 'name': c, 'kind': 'corp', 'corp_code': code,
                    'stock': next((s for cc, _, s in BY_NAME.get(c, []) if cc == code), ''),
                    'holders': [], 'side': []}

    edges = []
    for o in ftc['owners']:
        co, nm, cat = norm(o['company']), norm(o['name']), o['cat'] or ''
        row = {'name': nm, 'label': label(o['name']), 'cat': cat, 'common_pct': o['common_pct'], 'total_pct': o['total_pct'],
               'pref_pct': o['pref_pct'], 'common': o['common']}
        lt = later.get((nm, co))
        if lt and o['common_pct'] is not None:
            row['later'] = dict(lt, moved=abs(lt['pct'] - o['common_pct']) > MOVED)
        if cat in FAMILY_CATS or cat == '계열회사':
            kind = 'person' if cat in FAMILY_CATS else 'corp'
            if kind == 'person' and nm not in nodes:
                nodes[nm] = {'id': nm, 'name': nm, 'kind': 'person', 'rel': cat, 'holders': [], 'side': []}
            if kind == 'corp' and nm not in nodes:  # 국내 소속회사 목록에 없는 계열사 주주 = 국외 계열사
                nodes[nm] = {'id': nm, 'name': nm, 'label': label(o['name']), 'kind': 'corp', 'foreign': True, 'corp_code': None,
                             'stock': '', 'holders': [], 'side': []}
            if o['common_pct']:
                edges.append({'from': nm, 'to': co, 'pct': o['common_pct'], 'total_pct': o['total_pct'],
                              'later': row.get('later')})
            nodes[co]['holders'].append(row)
        else:
            nodes[co]['side'].append(row)  # 비영리법인·임원·자기주식·그룹 밖 최다주주·기타

    # 부모 — 동일인측 보통주 최대
    parent = {}
    for c in companies:
        ins = [e for e in edges if e['to'] == c]
        if ins:
            parent[c] = max(ins, key=lambda e: e['pct'])['from']
    cycles = []
    for c in list(parent):
        seen, cur = [], c
        while cur in parent and cur not in seen:
            seen.append(cur)
            cur = parent[cur]
        if cur in seen:
            cycles.append(seen[seen.index(cur):])
            del parent[seen[-1]]
    for e in edges:
        e['parent'] = parent.get(e['to']) == e['from']

    def depth(n):
        d = 0
        while n in parent:
            n, d = parent[n], d + 1
        return d

    family = sorted(n for n, v in nodes.items() if v['kind'] == 'person')
    orphans = [c for c in companies if c not in parent]
    out_nodes = []
    for n in sorted(nodes, key=lambda x: (depth(x), x)):
        v = nodes[n]
        v['depth'], v['parent'] = depth(n), parent.get(n)
        v['children'] = sum(1 for p in parent.values() if p == n)
        out_nodes.append(v)
    data = {'group': '한화', 'source': src_ftc, 'family': family, 'orphans': orphans, 'cycles': cycles,
            'company_count': len(companies),
            'nodes': out_nodes, 'edges': sorted(edges, key=lambda e: -e['pct'])}
    (D / 'hanwha.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"회사 {len(companies)} 사람 {len(family)} 선 {len(edges)} 부모없음 {orphans} 고리 {cycles} "
          f"뒤값이동 {sum(1 for e in edges if e['later'] and e['later']['moved'])}")


if __name__ == '__main__':
    main()
