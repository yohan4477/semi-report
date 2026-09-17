"""한화 지분 사슬 수집 — DART 최대주주현황(hyslrSttus)·타법인출자현황(otrCprInvstmntSttus).

㈜한화·한화에너지에서 출발해, 20% 이상 출자한 국내 회사 중 DART 정기보고서를 내는 곳으로
넓혀 간다. 보고서는 2026 반기(기준일 06-30)를 먼저, 없으면 2025 사업보고서.
산출: data/ownership/hanwha.raw.json — 판단 없이 공시 줄만. 거르기와 층 계산은 build.py.
"""
import json, re, sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dart

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data' / 'ownership' / 'hanwha.raw.json'
PERIODS = [('2026', '11012'), ('2025', '11011')]
SEEDS = ['00646495', '00160588']  # 한화에너지, ㈜한화
# 공시상 이름과 DART 고유번호 목록 이름이 다른 곳
ALIAS = {'한화생명보험': '한화생명', '한화호텔앤드리조트': '한화호텔앤드리조트'}
EXPAND_MIN = 20.0


def norm(name):
    s = re.sub(r'\s+', '', name or '')
    s = re.sub(r'^(주식회사|\(주\)|㈜)|(주식회사|\(주\)|㈜)$', '', s)
    s = s.replace('(주)', '').replace('㈜', '')
    return ALIAS.get(s, s)


def pct(s):
    try:
        return float(str(s).replace(',', '').strip())
    except ValueError:
        return None


CODES = dart.corp_codes()
BY_NAME = {}
for code, name, stock in CODES:
    BY_NAME.setdefault(norm(name), []).append((code, name, stock))


def report(code, ep):
    for yr, rc in PERIODS:
        d = dart.get(ep, corp_code=code, bsns_year=yr, reprt_code=rc)
        if d.get('status') == '000' and d.get('list'):
            return d['list']
    return []


def resolve(name):
    """이름 → (corp_code, 정기보고서 제출 여부). 같은 이름이 여럿이면 보고서 낸 쪽, 상장사 우선.
    보고서를 안 내는 비상장사도 고유번호는 돌려준다 — 노드 이름을 고정하려고."""
    cands = sorted(BY_NAME.get(norm(name), []), key=lambda c: not c[2])
    for code, _, _ in cands:
        if report(code, 'hyslrSttus'):
            return code, True
    return (cands[0][0], False) if len(cands) == 1 else (None, False)


def main():
    corps, holdings = {}, []
    # 상장 계열사는 주주 쪽에서도 찾는다 — 보고서 없는 비상장 중간지주(한화임팩트 등) 아래가 끊기지 않게
    listed = [c for c, n, st in CODES if st and (n.startswith('한화') or n in ('쎄트렉아이',)) and '기업인수목적' not in n and '스팩' not in n]
    seeds = SEEDS + [c for c in listed if c not in SEEDS]
    queue, seen = deque(seeds), set(seeds)
    while queue:
        code = queue.popleft()
        sh = report(code, 'hyslrSttus')
        inv = report(code, 'otrCprInvstmntSttus')
        if not sh:
            continue
        head = sh[0]
        corps[code] = {'name': head['corp_name'], 'cls': head['corp_cls'],
                       'stock': next((c[2] for c in CODES if c[0] == code), ''),
                       'rcept_no': head['rcept_no'], 'asof': head['stlm_dt']}
        for x in sh:
            if not re.search(r'보통주|의결권\s*있는', x.get('stock_knd', '')) or norm(x['nm']) in ('계', '합계', '소계'):
                continue
            holdings.append({'holder': x['nm'].strip(), 'relate': x.get('relate', ''), 'target': code,
                             'pct': pct(x['trmend_posesn_stock_qota_rt']), 'shares': x['trmend_posesn_stock_co'],
                             'kind': 'hyslr', 'rcept_no': x['rcept_no'], 'asof': x['stlm_dt'], 'rm': x.get('rm', '')})
        for x in inv:
            nm = x['inv_prm'].replace('\n', '').strip()
            if norm(nm) in ('계', '합계', '소계'):
                continue
            p = pct(x.get('trmend_blce_qota_rt'))
            tcode, filer = resolve(nm) if (p or 0) >= EXPAND_MIN else (None, False)
            holdings.append({'holder_code': code, 'target_name': nm, 'target': tcode, 'target_filer': filer, 'pct': p,
                             'purpose': re.sub(r'\s+', '', x.get('invstmnt_purps', '')),
                             'book': x.get('trmend_blce_acntbk_amount'), 'kind': 'invest',
                             'rcept_no': x['rcept_no'], 'asof': head['stlm_dt']})
            if tcode and filer and tcode not in seen:
                seen.add(tcode)
                queue.append(tcode)
        print(f"{corps[code]['name']:<20} 주주 {len(sh):>3}  출자 {len(inv):>3}  대기 {len(queue)}", flush=True)
    OUT.write_text(json.dumps({'corps': corps, 'holdings': holdings}, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(corps), 'corps', len(holdings), 'rows →', OUT.relative_to(ROOT))


if __name__ == '__main__':
    main()
