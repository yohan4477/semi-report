# -*- coding: utf-8 -*-
"""부동산 어댑터 — 한국부동산원 R-ONE.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 넷.

1. **평균을 내지 않는다.** 「강남 3구」는 구 셋이지만 셋을 평균하면 그 수는 공표치가 아니라
   우리가 만든 값이 된다(가중치도 없다). 구마다 값을 따로 준다.
2. **지수를 가격으로 읽지 않는다.** 지수는 기준시점 100 인 상대값이다. 전세지수를
   매매지수로 나눈 것은 전세가율이 아니다 — 전세가율은 별도 통계표(A_2024_00073)다.
3. **표마다 지역 단위가 다르다.** 지수·전세가율은 구까지 오는데, 수급은 권역까지,
   중위가격은 시도까지다. 없는 단위를 만들지 않고 온 단위를 그대로 이름에 적는다 —
   서울 중위가를 강남 3구 값인 것처럼 두면 카드가 거짓말을 한다.
4. **같은 지역의 코드가 표마다 다르다.** 「서울」이 중위가격 표에서는 500004,
   수급 표에서는 500008 이다. 그래서 코드를 지역이 아니라 (지역, 표) 쌍으로 둔다.
"""
import os, json, datetime, urllib.request, urllib.parse

BASE = 'https://www.reb.or.kr/r-one/openapi/SttsApiTblData.do'
KEY_ENV = 'REB_API_KEY'
ITM_DEFAULT = '100001'

# level 은 이 표가 실제로 주는 가장 작은 지역 단위다. 확인해서 적은 것이지 짐작이 아니다.
TBL = {
    'sale_idx':      dict(id='A_2024_00045', level='gu',
                          unit='지수(기준시점=100)', label='매매가격지수(아파트)'),
    'jeonse_idx':    dict(id='A_2024_00050', level='gu',
                          unit='지수(기준시점=100)', label='전세가격지수(아파트)'),
    'jeonse_ratio':  dict(id='A_2024_00073', level='gu',
                          unit='%', label='중위 매매가격 대비 전세가격(아파트)'),
    'supply_demand': dict(id='A_2024_00076', level='zone',
                          unit='지수(100=균형)', label='매매수급동향(아파트)'),
    'median_sale':   dict(id='A_2024_00189', level='sido',
                          unit='만원/㎡', label='지역별 매매 중위가격(아파트)'),
    'median_jeonse': dict(id='A_2024_00193', level='sido',
                          unit='만원/㎡', label='지역별 전세 중위가격(아파트)'),
}


class AdapterError(Exception):
    """응답이 기대한 모양이 아니다. R-ONE 은 키 오류·쿼터 초과·표 폐기를 HTTP 200 에
    다른 모양의 JSON 으로 준다 — 조용히 빈 결과를 주면 화면의 값이 통째로 사라지는데
    아무 데서도 FAIL 이 안 난다."""


def _rows(params):
    u = BASE + '?' + urllib.parse.urlencode(params)
    with urllib.request.urlopen(u, timeout=45) as r:
        d = json.loads(r.read().decode('utf-8'))
    blocks = d.get('SttsApiTblData')
    if not isinstance(blocks, list):
        raise AdapterError('응답에 SttsApiTblData 가 없다: %s' % str(d)[:200])
    total, rows, code = None, [], None
    for b in blocks:
        if isinstance(b, dict) and 'head' in b:
            for h in b['head']:
                if 'list_total_count' in h:
                    total = h['list_total_count']
                if isinstance(h.get('RESULT'), dict):
                    code = h['RESULT'].get('CODE')
        if isinstance(b, dict) and 'row' in b:
            rows = b['row']
    if code is not None and not str(code).startswith('INFO-0'):
        raise AdapterError('R-ONE 이 정상이 아니라고 답했다: %s' % code)
    return total, rows


def series(statbl_id, cls_id, start, end):
    """[(YYYY-MM, 값)] 과 「다 받았나」. 키가 없으면 앞 몇 건만 온다."""
    p = {'STATBL_ID': statbl_id, 'DTACYCLE_CD': 'MM', 'CLS_ID': cls_id,
         'ITM_ID': ITM_DEFAULT, 'START_WRTTIME': start, 'END_WRTTIME': end,
         'Type': 'json', 'pSize': 1000}
    key = os.environ.get(KEY_ENV)
    if key:
        p['KEY'] = key
    total, rows = _rows(p)
    out, dropped = [], 0
    for r in rows:
        t, v = str(r.get('WRTTIME_IDTFR_ID') or ''), r.get('DTA_VAL')
        if len(t) != 6:
            continue
        try:
            out.append(('%s-%s' % (t[:4], t[4:]), round(float(v), 2)))
        except (TypeError, ValueError):
            # 비공표 구간에 '-'·''·'X' 가 온다. 그 점만 버리고 나머지는 살린다
            dropped += 1
    out.sort()
    # B3 — total 을 못 읽으면 「일부」가 아니라 「모름」이다. 파싱 실패가 성격을
    #      통째로 강등시키던 자리다
    if total is None:
        full = None
    else:
        full = len(out) + dropped >= total > 0
    return out, full, dropped


def _targets(area, spec):
    """이 표를 무슨 지역으로 부를지. [(붙일 이름, CLS_ID)].

    구는 여럿이라 이름을 열쇠에 박고, 권역·시도는 하나라 이름을 값 쪽 라벨로만 쓴다."""
    lv = spec['level']
    if lv == 'gu':
        return [(gu, code) for gu, code in (area.get('codes') or {}).items()], ''
    blk = area.get(lv) or {}
    code = (blk.get('codes') or {}).get(spec['id'])
    if not code:
        return [], ''
    return [('', code)], blk.get('이름', '')


def fetch(target, area, start='202401', end=None):
    """워치 대상 하나의 metric 전부. area 는 watch/_areas.json 의 그 항목이다.

    end 를 박아 두면 그 뒤 자료가 **오류 없이** 안 온다 — 시계열이 거기서 멈추고
    화면은 그걸 「지금 값」이라 부른다. 안 주면 오늘 기준으로 넉넉히 잡는다."""
    if end is None:
        t = datetime.date.today()
        end = '%04d%02d' % (t.year + 1, t.month)
    out = {}
    for base, spec in TBL.items():
        pairs, wide = _targets(area, spec)
        for name, cls_id in pairs:
            s, full, dropped = series(spec['id'], cls_id, start, end)
            if not s:
                continue
            key = '%s_%s' % (base, name) if name else base
            src = '한국부동산원 R-ONE %s · %s' % (spec['id'], spec['label'])
            if wide:
                # 대상보다 넓은 단위로 온 값이다. 그 사실을 출처에 박는다 —
                # 표에서 구별 값과 나란히 서면 같은 단위로 읽힌다
                src += ' · %s 단위(대상보다 넓다)' % wide
            out[key] = {
                'value': s[-1][1], 'as_of': s[-1][0],
                'kind': {True: '공표', False: '공표(일부)', None: '확인 못 함'}[full],
                'unit': spec['unit'], 'src': src,
                'area': name or wide, 'level': spec['level'],
                'series': [list(x) for x in s], 'partial': full is not True,
                'dropped': dropped,
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
        print('%-24s %-8s %9s %-14s 점 %-3d %s'
              % (k, v['as_of'], v['value'], v['unit'], len(v['series']), v['kind']))
