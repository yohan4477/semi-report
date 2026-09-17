"""지분 그래프 검사 — FAIL 이면 gen_ownership 이 굽지 않는다.

O1 선 값이 0~100 밖이거나 비었다
O2 한 회사의 보통주 주주 합(동일인측+그 밖)이 100.05 를 넘는다 — 파싱이 줄을 두 번 셌다
O3 부모가 없는 국내 계열사가 있다 — 동일인측 주주를 못 읽었다
O4 부모 사슬에 고리가 남았다
O5 출처(접수번호·기준)가 비었다
O6 국내 계열사 수가 공시 줄의 회사 수와 다르다
O7 일가 누적 지분(계산값)이 0~100 밖이거나, 산식 항의 합이 값과 다르다
--selftest 는 결함을 넣어 각 규칙이 무는지 본다.
"""
import copy, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate(d):
    fails = []
    for e in d['edges']:
        if e['pct'] is None or not (0 < e['pct'] <= 100):
            fails.append(f"O1 {e['from']}→{e['to']} 값 {e['pct']}")
    for n in d['nodes']:
        if n['kind'] != 'corp' or n.get('foreign'):
            continue
        s = sum((r['common_pct'] or 0) for r in n['holders'] + n['side'])
        if s > 100.05:
            fails.append(f"O2 {n['name']} 보통주 주주 합 {s:.2f}")
        if not n.get('parent'):
            fails.append(f"O3 {n['name']} 부모 없음")
        cfv = n.get('cf')
        if cfv is None or not (0 <= cfv <= 100.05) or abs(sum(t['v'] for t in n.get('cf_terms', [])) - cfv) > 0.01:
            fails.append(f"O7 {n['name']} 누적 지분 {cfv}")
    if d.get('cycles'):
        fails.append(f"O4 고리 {d['cycles']}")
    src = d.get('source') or {}
    if not src.get('url') or not src.get('basis'):
        fails.append('O5 출처 비었음')
    dom = sum(1 for n in d['nodes'] if n['kind'] == 'corp' and not n.get('foreign'))
    if dom != d.get('company_count', dom):
        fails.append(f"O6 국내 계열사 {dom} ≠ 공시 {d['company_count']}")
    return fails


def selftest(d):
    cases = []
    x = copy.deepcopy(d); x['edges'][0]['pct'] = 120; cases.append(('O1', x))
    x = copy.deepcopy(d); n = next(n for n in x['nodes'] if n['kind'] == 'corp' and n['holders'])
    n['holders'].append(dict(n['holders'][0], common_pct=99)); cases.append(('O2', x))
    x = copy.deepcopy(d); n = next(n for n in x['nodes'] if n.get('parent')); n['parent'] = None; cases.append(('O3', x))
    x = copy.deepcopy(d); x['cycles'] = [['a', 'b']]; cases.append(('O4', x))
    x = copy.deepcopy(d); x['source'] = {}; cases.append(('O5', x))
    x = copy.deepcopy(d); x['company_count'] = 1; cases.append(('O6', x))
    x = copy.deepcopy(d); n = next(n for n in x['nodes'] if n.get('cf')); n['cf'] += 5; cases.append(('O7', x))
    ok = True
    for rule, broken in cases:
        hit = any(f.startswith(rule) for f in validate(broken))
        print(('물었다 ' if hit else '놓쳤다 ') + rule)
        ok &= hit
    return ok


def main():
    d = json.loads((ROOT / 'data' / 'ownership' / 'hanwha.json').read_text(encoding='utf-8'))
    if '--selftest' in sys.argv:
        sys.exit(0 if selftest(d) else 1)
    fails = validate(d)
    for f in fails:
        print('FAIL', f)
    print(f'check_own: FAIL {len(fails)}')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
