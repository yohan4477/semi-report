"""공정위 대규모기업집단현황공시(대표회사용) 한 편에서 그룹 전체 지분표를 뽑는다.

대표회사(㈜한화)가 DART 에 내는 [연1회공시및1/4분기용(대표회사)] 문서 안에
  3.(1) 소유지분현황             회사마다 주주 전원 — 동일인·친족·비영리법인·임원·자기주식·계열회사·기타
  3.(2) 국내 계열회사간 주식소유현황  행렬 — 열이 출자회사, 행이 피출자회사
가 계열사 전부에 대해 들어 있다. 기준은 문서가 밝힌 「금년도 지정일」 하나다.
산출: data/ownership/hanwha.ftc.json — 공시 줄 그대로, 판단 없음.
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dart

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data' / 'ownership' / 'hanwha.ftc.json'
REP_CORP = '00160588'  # ㈜한화 — 한화 기업집단 대표회사
REPORT_NM = '대규모기업집단현황공시[연1회공시및1/4분기용(대표회사)]'

CATS = ['동일인', '배우자/혈족1촌', '혈족2~4촌', '인척 3촌 이내', '기타 친족', '비영리법인', '등기된 임원',
        '자기주식', '계열회사', '기타 동일인관련자', '동일인측이 아닌 최다주주', '기타']
SKIP_NAMES = {'-', 'X', ''}


def clean(x):
    x = re.sub(r'<[^>]+>', '', x)
    x = x.replace('&amp;', '&').replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', x).strip()


def company(x):
    return re.sub(r'\s*주\s*\d+\)\s*$', '', x).strip()  # 「한화시스템(주) 주1)」 각주 떼기


def num(x):
    x = x.replace(',', '').strip()
    try:
        return float(x)
    except ValueError:
        return None


def rows_of(seg):
    out = []
    for r in re.findall(r'<TR[^>]*>(.*?)</TR>', seg, re.S):
        out.append([clean(c) for c in re.findall(r'<T[DHEU][^>]*>(.*?)</T[DHEU]>', r, re.S)])
    return out


def latest_filing():
    d = dart.get('list', corp_code=REP_CORP, bgn_de='20260101', end_de='20261231', page_count='100')
    hits = [x for x in d.get('list', []) if REPORT_NM in x['report_nm'].replace(' ', '')]
    if not hits:
        sys.exit('대표회사 공시를 못 찾았다')
    return max(hits, key=lambda x: x['rcept_no'])  # 정정이 있으면 가장 늦은 접수


def canon(h):
    """분류 칸 이름 → 정해진 분류. 공시마다 「계열회사(국내+국외)」「계열회사(국내+해외)」처럼 갈린다."""
    k = h.replace(' ', '')
    if k.startswith('계열회사'):
        return '계열회사'
    for cat in CATS:
        if k == cat.replace(' ', ''):
            return cat
    return None


def co_raw(c):
    return c[c.index('동일인측') - 1] if '동일인측' in c else None


def parse_owners(seg):
    """3.(1) — [{company, cat, name, common, common_pct, pref, pref_pct, total, total_pct}]"""
    out, co, cat = [], None, None
    for c in rows_of(seg):
        if len(c) < 7:
            continue
        if '동일인측' in c:
            co = company(c[c.index('동일인측') - 1])
        nums, name, head = c[-6:], c[-7], c[:-7]
        for h in reversed(head):
            k = canon(h)
            if k:
                cat = k
                break
            if h not in ('동일인측', '친족', '기타주주', co_raw(c)) and not ('합계' in h or h.replace(' ', '') == '총계'):
                sys.exit(f'모르는 분류 칸 「{h}」 — CATS 에 넣거나 규칙을 고친다: {c}')
        if canon(name):  # 성명 칸 자리에 분류가 온 줄
            cat, name = canon(name), '-'
        if co is None or name in SKIP_NAMES or '합계' in name or '총 계' in ''.join(c) and name in SKIP_NAMES:
            continue
        if any('합계' in h or '총 계' in h for h in head[-1:]):
            continue
        out.append({'company': co, 'cat': cat, 'name': company(name),
                    'common': num(nums[0]), 'common_pct': num(nums[1]),
                    'pref': num(nums[2]), 'pref_pct': num(nums[3]),
                    'total': num(nums[4]), 'total_pct': num(nums[5])})
    return out


def parse_matrix(seg):
    """3.(2) — [{investor, investee, common_pct, pref_pct, total_pct, book}] 칸이 '-' 인 곳은 뺀다."""
    out = []
    for tb in re.findall(r'<TABLE[^>]*>(.*?)</TABLE>', seg, re.S):
        rows = rows_of(tb)
        cols, investee, book = None, None, None
        for c in rows:
            if c and c[0].startswith('출자회사'):
                cols = None
                continue
            if cols is None and c and all(x not in ('주식수', '지분율') for x in c) and '장부가액' not in c and len(c) >= 1 \
                    and not any(x in ('보통주', '우선주', '합계') for x in c):
                if any('(주)' in x or '㈜' in x for x in c):
                    cols = [company(x) for x in c]
                continue
            if cols is None:
                continue
            if '장부가액' in c:
                i = c.index('장부가액')
                investee = company(c[i - 1]) if i >= 1 else None
                book = c[i + 1:]
                cur = {}
                continue
            if investee and c and c[0] in ('보통주', '우선주', '합계'):
                vals = c[1:]
                for k, co in enumerate(cols):
                    if 2 * k + 1 >= len(vals):
                        break
                    p = num(vals[2 * k + 1])
                    if p is None:
                        continue
                    key = (co, investee)
                    cur.setdefault(key, {'investor': co, 'investee': investee,
                                         'book': num(book[k]) if k < len(book) else None})
                    cur[key][{'보통주': 'common_pct', '우선주': 'pref_pct', '합계': 'total_pct'}[c[0]]] = p
                if c[0] == '합계':
                    out.extend(v for v in cur.values() if '소계' not in investee and '합계' not in investee)
                    cur = {}
    return out


def main():
    f = latest_filing()
    path = dart.document(f['rcept_no'])[0]
    t = path.read_text(encoding='utf-8')
    a = t.index('(1) 소유지분현황')
    b = t.index('(2) 국내 계열회사간 주식소유현황', a)
    c = t.index('4. 순환출자 현황', b)
    basis = re.search(r'\((금년도 지정일 기준)', t[a:b])
    owners = parse_owners(t[a:b])
    matrix = parse_matrix(t[b:c])
    data = {'rcept_no': f['rcept_no'], 'report_nm': f['report_nm'].strip(), 'rcept_dt': f['rcept_dt'],
            'basis': basis.group(1) if basis else None,
            'url': 'https://dart.fss.or.kr/dsaf001/main.do?rcpNo=' + f['rcept_no'],
            'owners': owners, 'matrix': matrix}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    cos = sorted({o['company'] for o in owners})
    print(f"{f['rcept_no']} {data['basis']}: 회사 {len(cos)}, 주주 줄 {len(owners)}, 행렬 칸 {len(matrix)}")


if __name__ == '__main__':
    main()
