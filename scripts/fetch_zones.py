# -*- coding: utf-8 -*-
"""서울 25구 + 성남 3구의 지정 현황(토지거래허가구역·조정대상지역·투기과열지구) —
insights/watch/_zones.json.

포트폴리오 워치 지도는 구마다 "지금 무엇이 걸려 있나"를 보여준다. 값은 오늘 실제로
연 공식 페이지에서만 채운다 — 지어내면 지도 전체가 무너진다(저장소 규칙, CLAUDE.md).

## 토지거래허가구역 — 서울은 살아 있는 JSON API, 성남은 상수
서울부동산정보광장 페이지(appointStatusSeoul.do)는 화면은 JS로 그리지만 표 데이터
자체는 POST /land/other/searchAppointStatusList.do 가 순수 JSON으로 낸다(로그인·세션
불필요, 2026-09-03 확인). 그래서 이 스크립트는 그 API를 그대로 다시 부른다 — 화면을
읽는 게 아니라 표를 채우는 원 데이터를 읽는다. 표에는 지정구분마다 지정권자·최초
지정일·면적(㎢ 또는 "區 전체"/"市 전체")·비고가 있을 뿐 구 이름을 직접 나열하지
않는 행이 많다("신속통합기획 160개소" 등) — 그런 행은 어느 구인지 특정 못하니
가공 안 하고 note에만 남긴다. 구 이름이 직접 들리는 행(강남·서초·송파·용산,
압구정=강남·여의도=영등포·목동=양천·성수=성동)과 "市 전체"(전 25구) 행만 구별로
옮긴다. **이 API는 서울시 것이다** — "市 전체"("서울시 25개 區 전체") 행을 성남
3구에까지 적용하면 안 된다. 성남은 경기부동산포털에 같은 JSON API가 없어(2026-09-04
확인, gris.gg.go.kr 은 화면만 있다) 조정대상지역·투기과열지구와 같은 방식(사람이
WebSearch/WebFetch로 확인해 상수로 박는다)으로 채운다.

## 조정대상지역·투기과열지구·성남 토지거래허가구역 — 공식 API가 없다
국토교통부는 규제지역 지정을 관보 고시(PDF)로만 낸다. molit.go.kr에 표 형태 API가
없어 이 스크립트는 실행할 때마다 사람이 WebSearch/WebFetch로 다시 확인해 아래 상수를
갱신해야 한다("다시 돌릴 수 있게"의 의미가 여기서는 "같은 절차를 다시 밟게" 쪽이다).
2026-09-03에 확인한 사실 — 정책브리핑(korea.kr, 국무조정실 공동 발표)과
국토교통부공고 두 건(조정대상지역 제2025-1223호, 투기과열지구 제2025-1225호,
2025-10-16 시행)이 서울 25개구 전체를 조정대상지역·투기과열지구로 지정했다고 밝힌다.
기존 4구(강남·서초·송파·용산)는 2023-01-05 규제지역 재편 때부터 계속 지정 상태였고
(그때 다른 21구는 해제됐다), 나머지 21구가 2025-10-16 신규로 다시 묶였다. 두 정부
발표를 부동산위키(교차 확인용, 같은 25구 표를 보여준다)로 한 번 더 대조했다.
이 셋의 지정 여부는 현재 25구 전부 동일(true)하므로 "일부"가 없다 — 그래서 gu 값이
전부 true인 게 이상한 게 아니라 실제로 그렇다.

2026-09-04에 성남 3구를 더하며 같은 정책브리핑(newsId=148950973)을 다시 읽었다 —
그 발표문이 "경기도 12개 지역"으로 과천시·광명시·성남시 분당·수정·중원구·수원시
영통·장안·팔달구·안양시 동안구·용인시 수지구·의왕시·하남시를 원문 그대로 나열하고,
이 12곳이 조정대상지역·투기과열지구·토지거래허가구역 셋 다에 든다고 밝힌다(원문:
"그 외 서울 21개 자치구 전체와 경기도 12개 지역은 새로 지정한다"). 토지거래허가구역의
효력발생일은 발표문에 "지정 공고한 날부터 5일 후인 10월20일부터 발생한다"고 못박혀
있다 — 서울 25개구와 같은 날(2025-10-20)이다. 조정대상지역·투기과열지구의 시행일은
발표문에 따로 안 나와 서울과 같은 국토교통부공고 시행일(2025-10-16)을 그대로 쓴다 —
서울 21개구와 경기 12곳이 "그 외"로 한 문장에 같이 묶여 지정됐으므로 같은 고시로
봐도 된다. 성남 3구는 이 2025-10-16/10-20 지정 이전에는(2023-01-05 규제지역 재편 때)
전국 대부분 지역과 함께 해제돼 있었다 — 그때도 유지된 건 서울 4구(강남·서초·송파·
용산)뿐이라 성남도 서울 21구와 같은 "신규 지정" 문구를 쓴다.

## 분양가상한제 — 성남은 지정된 적이 없다
2020년 민간택지 분양가상한제 지정(국토교통부공고 제2020-1244호류)은 서울 18개구만
묶었다 — 성남을 포함한 경기 지역은 그 목록에 없었다(2026-09-04, 국가법령정보센터
DRF admrul 검색·언론 보도로 교차 확인). 2025-10-15 대책 발표문(newsId=148950973)에도
분양가상한제 지정 문구가 없다. 그래서 성남 3구는 지정된 적이 없는 구(서울의
강북·관악구 등과 같은 부류)로 다룬다.

    python scripts/fetch_zones.py
"""
import io
import json
import os
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GU_SRC = os.path.join(ROOT, 'insights', 'watch', '_seoul_gu.json')
OUT = os.path.join(ROOT, 'insights', 'watch', '_zones.json')

LAND_PAGE = 'https://land.seoul.go.kr/land/other/appointStatusSeoul.do'
LAND_API = 'https://land.seoul.go.kr/land/other/searchAppointStatusList.do'

# 지정구분 문자열에 등장하는 지명 조각 -> 정식 구 이름. 이 표에 없는 조각(신속통합기획
# 등 위치가 특정 안 된 사업 유형)은 구별로 못 옮기고 note로만 남긴다.
NAME_ALIAS = {
    '강남': '강남구', '서초': '서초구', '송파': '송파구', '용산': '용산구',
    '압구정': '강남구', '여의도': '영등포구', '목동': '양천구', '성수': '성동구',
    '잠실': '송파구', '삼성': '강남구', '대치': '강남구', '청담': '강남구',
}

# 성남 3구 — 경기도 12개 지역 중 성남시 몫. 근거는 위 모듈 머리 「조정대상지역·
# 투기과열지구·성남 토지거래허가구역」 절.
_GG_SEONGNAM_SRC = ('https://www.korea.kr/news/policyNewsView.do?newsId=148950973 '
                    '(서울 전역·경기 12곳 투기과열지구·토지거래허가구역 지정, '
                    '2025-10-15 관계부처 합동 발표 — "과천시, 광명시, 성남시 '
                    '분당·수정·중원구, 수원시 영통·장안·팔달구, 안양시 동안구, '
                    '용인시 수지구, 의왕시, 하남시")')


def load_gu_names():
    d = json.load(io.open(GU_SRC, encoding='utf-8'))
    return sorted(d['gu'].keys())


def load_gu_sido():
    """구 이름 -> sido('서울'|'경기'). _seoul_gu.json(지도 정본)에서 읽는다 —
    서울 API 결과를 성남에 잘못 씌우지 않으려면 어느 구가 서울인지를 알아야 한다."""
    d = json.load(io.open(GU_SRC, encoding='utf-8'))
    return dict((name, e.get('sido', '서울')) for name, e in d['gu'].items())


def fetch_land_rows():
    """서울부동산정보광장 API를 그대로 불러 원 레코드 리스트를 돌려준다."""
    body = urllib.parse.urlencode({}).encode()
    req = urllib.request.Request(LAND_API, data=body, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': LAND_PAGE,
        'X-Requested-With': 'XMLHttpRequest',
    })
    with urllib.request.urlopen(req, timeout=20) as f:
        data = json.loads(f.read().decode('utf-8'))
    return data['result']


def fetch_land_asof():
    """페이지 정적 HTML에 박힌 '기준 일자'를 그대로 읽는다(JS 렌더 없이도 있다)."""
    req = urllib.request.Request(LAND_PAGE, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as f:
        html = f.read().decode('utf-8', 'replace')
    import re
    m = re.search(r'기준\s*일자[^0-9]*([0-9]{4}[.\s]*[0-9]{1,2}[.\s]*[0-9]{1,2})', html)
    if not m:
        return None
    y, mo, da = re.findall(r'[0-9]+', m.group(1))
    return '%s-%02d-%02d' % (y, int(mo), int(da))


def matched_gu(text):
    """지정구분 문자열에서 NAME_ALIAS 조각을 찾아 매치된 구 이름 집합을 돌려준다."""
    hit = set()
    for frag, gu in NAME_ALIAS.items():
        if frag in text:
            hit.add(gu)
    return hit


def build_land_zone(all_gu, sido_of):
    """토지거래허가구역. all_gu 는 서울 25구 + 성남 3구다 — 서울부동산정보광장
    API 는 서울시 것이라 sido_of 로 걸러 서울 구에만 적용하고, 성남 3구는 이 API
    안 쓰고 _GG_SEONGNAM 상수로 채운다(위 모듈 머리 참고)."""
    rows = fetch_land_rows()
    as_of = fetch_land_asof() or '확인 못함'

    blanket = []          # areaCn == '市 전체' 인 행 — 서울 25구 전부에 적용
    partial_by_gu = {}    # 구 이름 -> [문구, ...]
    unresolved = []       # 위치가 특정 안 된 행(신속통합기획 등)

    for r in rows:
        typ, first, area, note = r['dsgnTypeNm'], r['frstDsgnYmd'], r['areaCn'], r['rmrkCn']
        authr = r['dsgnAuthrNm']
        label = '%s(%s, %s 지정, %s)' % (typ, first, authr, note)
        if area in ('市 전체',):
            blanket.append(label)
            continue
        hit = matched_gu(typ)
        if hit:
            for gu in hit:
                partial_by_gu.setdefault(gu, []).append(
                    '%s(%s, %s 지정, 면적 %s, %s)' % (typ, first, authr, area, note))
        else:
            unresolved.append('%s(%s, %s, 면적 %s, %s)' % (typ, first, authr, area, note))

    gg_detail = ('토지거래허가구역(2025-10-20 시행, %s)' % _GG_SEONGNAM_SRC)
    gu_out = {}
    for gu in all_gu:
        if sido_of.get(gu) != '서울':
            # 성남 3구 — 서울시 API 밖. "市 전체"(서울 전역) 문구를 그대로 물려주면
            # 근거 없는 값이 된다
            gu_out[gu] = {'value': '전부', 'detail': gg_detail}
            continue
        parts = list(blanket) + partial_by_gu.get(gu, [])
        gu_out[gu] = {'value': '전부' if blanket else ('일부' if parts else '없음'),
                       'detail': ' / '.join(parts) if parts else '해당 지정 없음'}

    note = ('서울부동산정보광장 API(searchAppointStatusList.do) 레코드 %d건 중 '
            '위치가 특정 안 된 사업형 지정 %d건은 구별로 못 옮겨 여기 남긴다: %s'
            ' · 성남 3구는 이 API 밖이라 별도 조사(정책브리핑 2025-10-15 발표문)로 채운다'
            % (len(rows), len(unresolved), '; '.join(unresolved)))
    return {
        'src': LAND_PAGE + ' (표 데이터는 ' + LAND_API + ') · 성남 3구는 ' + _GG_SEONGNAM_SRC,
        'as_of': as_of,
        'note': note,
        'gu': gu_out,
    }


# --- 조정대상지역 · 투기과열지구: 공식 API가 없어 조사 결과를 상수로 박는다 -------
# 확인한 자료(2026-09-03 조사):
#   - korea.kr 정책브리핑 "서울 전역·경기 12곳 투기과열지구·토지거래허가구역 지정"
#     (newsId=148950973, 관계부처 합동 2025-10-15 발표) — 기존 4구(강남·서초·송파·
#     용산) 외 서울 21개구 전체 신규 지정, 5일 뒤(10-20) 토지거래허가 발효.
#   - 국토교통부공고 제2025-1223호(조정대상지역 지정) — 2025-10-16 시행.
#   - 국토교통부공고 제2025-1225호(투기과열지구 지정) — 2025-10-16 시행.
#   - 기존 4구는 2023-01-05 규제지역 재편(그 외 지역 전부 해제) 때부터 계속 지정.
#   - 부동산위키 "투기과열지구 및 조정대상지역 현황"(2025-10-15 기준 표)으로 교차
#     확인 — 서울 25개구 전부 두 항목 모두 지정.
_ADJUST_SRC = ('https://www.korea.kr/news/policyNewsView.do?newsId=148950973 ; '
               '국토교통부공고 제2025-1223호(조정대상지역, 2025-10-16 시행) ; '
               '교차확인 https://xn--989a00af8jnslv3dba.com/wiki/'
               '투기과열지구_및_조정대상지역_현황')
_OVERHEAT_SRC = ('https://www.korea.kr/news/policyNewsView.do?newsId=148950973 ; '
                  '국토교통부공고 제2025-1225호(투기과열지구, 2025-10-16 시행) ; '
                  '교차확인 https://xn--989a00af8jnslv3dba.com/wiki/'
                  '투기과열지구_및_조정대상지역_현황')
_OLD4 = {'강남구', '서초구', '송파구', '용산구'}


# --- 분양가상한제(민간택지): 규제지역과 별개의 지정이라 층을 따로 둔다 ------------
# 규제지역 셋과 달리 이 층은 서울에서 값이 갈린다(4구만 true) — 그래서 지도에서
# 「투기과열지구라 다 같다」로 읽히던 자리가 여기서 처음 나뉜다.
#
# 2026-09-03에 확인한 것:
#   - 국가법령정보센터 DRF admrul 검색('분양가상한제')에서 현행 공고는 하나뿐이다 —
#     「분양가상한제 적용지역 지정 해제」(국토교통부공고 제2023-3호, 2023-01-05 발령·
#     시행, 행정규칙일련번호 2100000221718). 그 뒤로 새 지정·해제 공고가 이 DB에
#     안 잡힌다. 2025-10-15 대책(투기과열지구·조정대상지역 서울 전역 확대)도
#     korea.kr 발표문에 분양가상한제 지정 문구가 없다.
#   - 그 공고의 제·개정이유에 해제 지역이 적혀 있다. 서울에서 통째로 풀린 구는
#     강동·영등포·마포·성동·동작·양천·중·광진·서대문 아홉이고, 강서·노원·동대문·
#     성북·은평은 동 이름을 나열해 풀었다.
#   - 해제 전 지정 범위는 2020년 공고의 서울 18개구 309개동이었다(강남·서초·송파·
#     강동·영등포·마포·성동·동작·양천·용산·서대문·중·광진·강서·노원·동대문·성북·
#     은평). 18개구에서 위 아홉과 동 단위로 푼 다섯을 빼면 강남·서초·송파·용산 넷이
#     남는다 — 2023-01-03 국토교통부 발표를 옮긴 언론 보도 여럿과 같은 결과다.
#
# 못 확인한 것 둘(detail 에 그대로 적는다):
#   1. 남은 네 구가 구 전역인지 동 단위인지. 원 지정 공고가 동 단위였는데 그 동
#      목록을 오늘 못 열었다(molit 고시 페이지는 리다이렉트 루프, 첨부는 PDF·HWP).
#   2. 동 단위로 푼 다섯 구에 안 풀린 동이 남았는지. 해제 공고가 그 구의 지정 동을
#      전부 나열했는지 확인 못 했다 — 언론이 「4구만 남았다」로 쓴 것을 근거로 삼는다.
_CEIL_SRC = ('https://www.law.go.kr/LSW//admRulLsInfoP.do?admRulId=69616&efYd=0 '
             '(국토교통부공고 제2023-3호 「분양가상한제 적용지역 지정 해제」, '
             '2023-01-05 발령·시행 ; DRF admrul 조회로 현행 확인) ; '
             '교차확인 https://www.korea.kr/news/policyNewsView.do?newsId=148950973 '
             '(2025-10-15 대책 — 분양가상한제 지정 문구 없음)')
_CEIL_ON = {'강남구', '서초구', '송파구', '용산구'}
# 2023-01-05 공고가 구 전체를 푼 구
_CEIL_OFF_WHOLE = {'강동구', '영등포구', '마포구', '성동구', '동작구',
                   '양천구', '중구', '광진구', '서대문구'}
# 같은 공고가 동 이름을 나열해 푼 구
_CEIL_OFF_DONG = {'강서구', '노원구', '동대문구', '성북구', '은평구'}


def build_ceiling_zone(all_gu):
    gu_out = {}
    for gu in all_gu:
        if gu in _CEIL_ON:
            gu_out[gu] = {'value': True, 'detail': (
                '2023-01-05 해제 공고의 해제 목록에 없다 — 2020년 지정 18개구 가운데 '
                '남은 넷. 다만 원 지정이 동 단위였고 그 동 목록을 오늘 못 열어 '
                '구 전역인지 일부 동인지는 확인 못 함')}
        elif gu in _CEIL_OFF_WHOLE:
            gu_out[gu] = {'value': False, 'detail':
                          '국토교통부공고 제2023-3호(2023-01-05)가 구 전체를 해제'}
        elif gu in _CEIL_OFF_DONG:
            gu_out[gu] = {'value': False, 'detail': (
                '국토교통부공고 제2023-3호(2023-01-05)가 이 구의 동 이름을 나열해 해제 — '
                '지정돼 있던 동을 전부 나열했는지는 확인 못 함')}
        else:
            gu_out[gu] = {'value': False, 'detail':
                          '2020년 지정 18개구에 안 들어간 구 — 지정된 적이 없다'}
    return {
        'src': _CEIL_SRC,
        'as_of': '2023-01-05',
        'note': ('민간택지 분양가상한제다. 공공택지는 지역 지정과 무관하게 「주택법」 제57조로 '
                 '적용되므로 이 표로 판단하지 않는다. 규제지역(투기과열지구·조정대상지역)과 '
                 '별개의 지정이라 층을 따로 뒀다 — 서울이 전역 투기과열지구가 된 뒤에도 '
                 '이 층은 넷과 스물하나로 갈린다. 지정·해제가 공고(PDF)로만 나와 자동으로 '
                 '못 받는다. 규정이 바뀌면 사람이 이 파일의 상수를 갱신한다.'),
        'gu': gu_out,
    }


def build_regulation_zone(all_gu, src, label):
    gu_out = {}
    for gu in all_gu:
        if gu in _OLD4:
            detail = '2023-01-05 규제지역 재편 때 유지 지정, 2025-10-16 %s 고시로 서울 21개구와 함께 재확인' % label
        else:
            detail = '2025-10-16 국토교통부 고시로 신규 지정(그 전 2023-01-05 재편 때는 해제됐던 구)'
        gu_out[gu] = {'value': True, 'detail': detail}
    return {
        'src': src,
        'as_of': '2025-10-16',
        'note': ('공식 표/JSON API가 없어(고시 PDF만 발행) 사람이 WebSearch/WebFetch로 '
                 '확인한 결과를 상수로 박았다 — 재실행해도 이 스크립트가 자동으로 다시 '
                 '확인하지 않는다. 규정이 바뀌면 이 파일의 상수를 사람이 갱신해야 한다.'),
        'gu': gu_out,
    }


def main():
    all_gu = load_gu_names()
    sido_of = load_gu_sido()
    out = {
        'fetched': '2026-09-04',
        '토지거래허가구역': build_land_zone(all_gu, sido_of),
        '조정대상지역': build_regulation_zone(all_gu, _ADJUST_SRC, '조정대상지역'),
        '투기과열지구': build_regulation_zone(all_gu, _OVERHEAT_SRC, '투기과열지구'),
        '분양가상한제': build_ceiling_zone(all_gu),
    }
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    print('gu=%d (서울 %d · 경기 %d) -> %s (%.1fKB)' %
          (len(all_gu), sum(1 for v in sido_of.values() if v == '서울'),
           sum(1 for v in sido_of.values() if v != '서울'), OUT, os.path.getsize(OUT) / 1024.0))
    land = out['토지거래허가구역']
    print('토지거래허가구역 as_of=%s  강남구=%s  분당구=%s' %
          (land['as_of'], land['gu']['강남구']['value'], land['gu'].get('분당구', {}).get('value')))
    for k in ('조정대상지역', '투기과열지구', '분양가상한제'):
        vals = set(v['value'] for v in out[k]['gu'].values())
        on = sorted(g for g, v in out[k]['gu'].items() if v['value'] is True)
        print('%s: 값 집합=%s  true=%d구 %s' % (k, vals, len(on), ' '.join(on[:6])))
        for g in ('분당구', '수정구', '중원구'):
            print('    %s -> %s' % (g, out[k]['gu'][g]['value']))


if __name__ == '__main__':
    main()
