# -*- coding: utf-8 -*-
"""부동산 어댑터 — 한국부동산원 R-ONE 에서 가격지수를 받는다.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 셋.

1. **평균을 내지 않는다.** 「강남 3구」는 구 셋이지만 셋을 평균하면 그 수는 공표치가 아니라
   우리가 만든 값이 된다(가중치도 없다). 구마다 선을 따로 준다 — 성격이 공표치로 남는다.
2. **지수를 가격으로 읽지 않는다.** DTA_VAL 은 기준시점 100 인 지수다. 전세지수를
   매매지수로 나눈 것은 전세가율이 아니다 — 지수끼리의 비라 값에 뜻이 없다.
   전세가율은 별도 통계이고 아직 안 뚫었다.
3. **키가 없으면 조용히 반쪽을 주지 않는다.** R-ONE 은 키 없이도 앞 5건만 주는데
   그걸 시계열로 쓰면 「최근 자료가 없다」가 아니라 「값이 안 움직였다」로 읽힌다.
   키가 없으면 partial 표시를 붙인다.
"""
import os, json, urllib.request, urllib.parse

BASE = 'https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do'
KEY_ENV = 'REB_API_KEY'

# 통계표. 아파트 기준이다 — 「주택종합」은 단독·연립이 섞여 권역 비교가 흐려진다.
TBL = {
    'sale_idx':   ('A_2024_00045', '매매가격지수(아파트)'),
    'jeonse_idx': ('A_2024_00050', '전세가격지수(아파트)'),
}
ITM_INDEX = '100001'      # 항목 「지수」


def _get(params):
    u = BASE + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(u, timeout=30) as r:
        d = json.loads(r.read().decode('utf-8'))
    blocks = d.get('SttsApiTblData') or []
    total, rows = 0, []
    for b in blocks:
        if isinstance(b, dict) and 'head' in b:
            for h in b['head']:
                if 'list_total_count' in h:
                    total = h['list_total_count']
        if isinstance(b, dict) and 'row' in b:
            rows = b['row']
    return total, rows


def series(statbl_id, cls_id, start, end):
    """[(YYYY-MM, 값)] 과 「다 받았나」. 키가 없으면 앞 몇 건만 온다."""
    p = {'STATBL_ID': statbl_id, 'DTACYCLE_CD': 'MM', 'CLS_ID': cls_id,
         'ITM_ID': ITM_INDEX, 'START_WRTTIME': start, 'END_WRTTIME': end,
         'Type': 'json', 'pSize': 1000}
    key = os.environ.get(KEY_ENV)
    if key:
        p['KEY'] = key
    total, rows = _get(p)
    out = []
    for r in rows:
        t = str(r.get('WRTTIME_IDTFR_ID') or '')
        v = r.get('DTA_VAL')
        if len(t) == 6 and v is not None:
            out.append(('%s-%s' % (t[:4], t[4:]), round(float(v), 2)))
    out.sort()
    return out, (len(out) >= total > 0)


def fetch(target, areas, start='202401', end='202612'):
    """워치 대상 하나의 metric 들. areas 는 watch/_areas.json 의 그 대상 항목이다.

    구마다 metric 이 따로 선다 — sale_idx_강남구 처럼. 평균을 안 내는 대신
    이름에 구를 박아 무엇을 재는 값인지가 열쇠에 남는다."""
    out = {}
    for gu, cls_id in areas.get('codes', {}).items():
        for base, (tbl, label) in TBL.items():
            s, full = series(tbl, cls_id, start, end)
            if not s:
                continue
            out['%s_%s' % (base, gu)] = {
                'value': s[-1][1], 'as_of': s[-1][0],
                'kind': '공표' if full else '공표(일부)',
                'unit': '지수(기준시점=100)',
                'src': '한국부동산원 R-ONE %s · %s' % (tbl, label),
                'series': [list(x) for x in s],
                'partial': not full,
            }
    return out


if __name__ == '__main__':
    import sys, io
    sys.stdout.reconfigure(encoding='utf-8')
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    areas = json.load(io.open(os.path.join(root, '_areas.json'), encoding='utf-8'))
    tgt = sys.argv[1] if len(sys.argv) > 1 else '강남 3구'
    got = fetch(tgt, areas[tgt])
    print('열쇠', '있음' if os.environ.get(KEY_ENV) else '없음 — 앞 몇 건만 온다')
    for k, v in sorted(got.items()):
        print('%-22s %-8s %s  점 %d  %s'
              % (k, v['as_of'], v['value'], len(v['series']), v['kind']))
