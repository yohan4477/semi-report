# -*- coding: utf-8 -*-
"""청약 어댑터 — 공공데이터포털의 청약홈 분양정보·경쟁률 API 에서 세 권역의 공고를 받는다.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 다섯.

1. **열쇠가 없으면 빈 손으로 돌아온다.** 예외를 던지지 않는다 — 워치 실행기가 줄
   하나 때문에 통째로 멈추면 안 되고, 「아직 못 받는다」는 것 자체가 화면에 적힐
   사실이다. 열쇠는 환경변수 DATA_GO_KR_KEY. 발급 절차는 아래 「열쇠」 절.
2. **구는 주소 부분일치로 거른다.** 이 API 의 지역 파라미터(SUBSCRPT_AREA_CODE_NM)는
   청약홈 검색 화면과 같은 시·도 단위로 보인다 — 서울까지만 좁혀진다. 구까지 내려가려면
   공급위치(HSSPLY_ADRES)를 LIKE 로 건다. 정확한 코드표를 못 봐서(2026-09-03) 시·도로
   받아 놓고 주소 문자열로 다시 거르는 두 단계를 쓴다. 놓친 공고가 있을 수 있다는
   것을 src 끝에 적어 둔다.
3. **경쟁률은 공고 하나를 열쇠로 받는다.** HOUSE_MANAGE_NO 와 PBLANC_NO 를 함께 넘겨야
   하고, 돌아오는 것은 단지 하나의 수가 아니라 주택형×순위×거주코드 조합마다 한 행이다.
   그래서 「이 권역 경쟁률」이라는 한 수는 API 에 없다 — 우리가 만들면 우리가 만든 수다.
   여기서는 1순위 해당지역 행의 경쟁률만 모아 그 공고의 최소·최대를 적어 둔다.
   2026-09-03 활용신청이 승인돼 응답이 온다(그전엔 401 이었다) — 접수가 아직 안
   끝난 공고는 CMPET_RATE 가 "-"(신청자 0)라 값이 안 잡힌다. 그래도 실패하면(게이트웨이
   장애 등) 그 공고부터는 조용히 건너뛰고 한 번만 경고한다 — 공고 목록 자체는 지킨다.
4. **시계열을 지어내지 않는다.** 공고는 달마다 나오지 않는다. 값이 한 점뿐이면
   series 를 비운다 — 도해가 두 점을 이어 없는 추세를 그리는 것을 막는 자리다.
5. **분양가상한제·투기과열지구는 그 공고 시점의 값이다.** PARCPRC_ULS_AT·
   SPECLT_RDN_EARTH_AT 는 공고마다 붙는 값이라, 서울이 전역 투기과열지구가 되기
   전(2025-10-16 이전)에 난 공고는 그 구가 지금 규제지역이어도 N 으로 온다 —
   실제로 2025-10-02 이전 공고는 강남 3구·용산·송파를 빼면 전부 N, 그 뒤로는
   전부 Y 였다(2026-09-03 확인, 표본 50건). 지어낸 규칙이 아니라 응답 그대로다.

2026-09-04 — 세 권역만 거르던 것을 서울 25구 전부로 넓혔다(지도가 25구를 그리므로
구를 못 뽑은 공고만 세지 못하고 나머지는 다 세야 한다). `pblanc_gu` 가 그 산출이다
— 구 이름마다 공고 목록을 묶고, 총 건수는 구를 뽑아낸 공고만 센다(주소에 25구
이름이 하나도 안 걸린 공고는 `n_unmatched` 로 src 에만 남기고 목록에서는 뺀다 —
값을 지어내지 않는다). 세 권역 metric(`pblanc_cnt_<권역>`·`pblanc_list_<권역>`)은
그대로 둔다 — 「청약 — 조건」 절의 표가 그 셋만 본다. 구를 뽑는 로직(`_in_gu`)과
경쟁률 호출(`_rate1_summary`, 공고당 한 번)은 공고 하나에 한 번만 돈다 — 권역별로
따로 돌리면 세 권역에 걸치지 않는 22구를 볼 방법이 없고, 겹치는 구도 없으니(세
권역이 서로소) 한 번에 다 나눠 담아도 세 권역 결과가 이전과 같다.

2026-09-04 두 번째 — 지도가 성남 3구까지 그리게 되며 지역 필터를 서울 + 경기로
넓혔다. `SUBSCRPT_AREA_CODE_NM`(청약홈 지역 파라미터)이 시·도 단위까지만 좁혀지는
건 서울 때와 같아서(위 머리 2번), 경기 전체를 한 번 더 받고 공급위치(HSSPLY_ADRES)에
"성남시"가 든 행만 남긴다 — 안양·수원 같은 다른 경기 시가 섞여 들어오지 않는다.
`_in_gu`가 구 이름을 찾을 때 ALL_GU 는 `_seoul_gu.json`(지도 정본)을 그대로 읽으므로
그 파일에 성남 3구가 들어간 순간 "성남시 분당구" 같은 주소에서 "분당구" 가 그대로
잡힌다 — 이 파일에서 새로 할 일은 경기 사도를 한 번 더 부르는 것뿐이다. 경기 호출이
실패해도(게이트웨이 장애 등) 서울 몫은 버리지 않는다 — `fetch.gg_error` 에 사유만
남기고 서울 결과로 계속 간다.

## 열쇠

공공데이터포털(data.go.kr)에서 두 서비스를 각각 활용신청한다.

  - 15098547  한국부동산원_청약홈 분양정보 조회 서비스
  - 15098905  한국부동산원_청약홈 청약접수 경쟁률 및 특별공급 신청현황 조회 서비스

    https://www.data.go.kr/data/15098547/openapi.do
    https://www.data.go.kr/data/15098905/openapi.do

개발단계는 자동승인, 운영단계는 심의승인이라고 두 페이지에 적혀 있다(2026-09-03 확인).
심의에 며칠 걸리는지는 페이지에 없다. 발급받은 일반 인증키(Decoding)를 환경변수
DATA_GO_KR_KEY 에 넣는다. 게이트웨이는 odcloud.kr 이고 구형 apis.data.go.kr 이 아니다 —
그쪽 주소로 부르면 NO_OPENAPI_SERVICE_ERROR 가 온다.

열쇠 없이 부르면 {"code":-401,"msg":"인증키는 필수 항목 입니다."} 가 온다(HTTP 401,
2026-09-03 확인). 없는 경로에도 같은 응답이 오므로 이 401 은 「경로가 맞다」는 증거가
아니다 — 오퍼레이션 이름은 두 서비스의 Swagger 문서에서 왔다.
"""
import os
import re
import json
import datetime
import urllib.parse
import urllib.request

DETAIL = 'https://api.odcloud.kr/api/ApplyhomeInfoDetailSvc/v1/'
CMPET = 'https://api.odcloud.kr/api/ApplyhomeInfoCmpetRtSvc/v1/'
KEY_ENV = 'DATA_GO_KR_KEY'

# 워치가 보는 세 권역. _areas.json 과 같은 이름을 쓴다 — 여기서 새로 만들지 않는다.
AREA_GU = {
    '강남 3구': ('강남구', '서초구', '송파구'),
    '마용성': ('마포구', '용산구', '성동구'),
    '노도강': ('노원구', '도봉구', '강북구'),
}


def _all_gu():
    """서울 25구 + 성남 3구 이름 — insights/watch/_seoul_gu.json(지도 정본)에서 읽는다.
    손으로 목록을 새로 적지 않는다 — 지도가 구를 늘리거나 이름을 바꾸면 여기도
    따라가야 한다."""
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      '_seoul_gu.json')
    with open(p, encoding='utf-8') as f:
        d = json.load(f)
    return sorted(d['gu'])


ALL_GU = _all_gu()


class NoKey(Exception):
    """열쇠가 없다. 오류가 아니라 상태다 — fetch 는 이것을 잡아 빈 손으로 돌아온다."""


def _key():
    k = os.environ.get(KEY_ENV)
    if not k:
        raise NoKey('%s 가 없다 — data.go.kr 에서 15098547·15098905 를 활용신청한다' % KEY_ENV)
    return k


def _get(base, op, params, timeout=30):
    p = dict(params)
    p['serviceKey'] = _key()
    u = base + op + '?' + urllib.parse.urlencode(p)
    with urllib.request.urlopen(u, timeout=timeout) as r:
        d = json.loads(r.read().decode('utf-8', 'replace'))
    if 'data' not in d:
        # {"code":-4,"msg":"등록되지 않은 인증키 입니다."} 같은 게이트웨이 응답
        raise NoKey('게이트웨이가 거절했다: %s' % str(d)[:120])
    return d['data']


def _six_months_ago():
    """오늘부터 6개월 전 달의 1일(YYYY-MM-01). 최근 6개월치 공고만 본다."""
    d = datetime.date.today()
    y, m = d.year, d.month - 6
    while m <= 0:
        m += 12
        y -= 1
    return '%04d-%02d-01' % (y, m)


def _yn(v):
    """API 의 Y/N 문자열 → True/False/None. 값이 없거나 다른 것이면 None이지
    지어내지 않는다."""
    if v == 'Y':
        return True
    if v == 'N':
        return False
    return None


def _fmt_rate(v):
    """140.0 → "140", 15.71 → "15.71". 소수점 뒤 불필요한 0을 뗀다."""
    s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s or '0'


def pblancs(sido='서울', since=None, page_size=100):
    """모집공고일이 since(YYYY-MM-DD) 이후인 APT 분양 공고를 시·도 단위로 받는다.

    구 단위 필터를 여기서 안 거는 이유는 위 머리 2번에 적었다."""
    p = {'page': 1, 'perPage': page_size,
         'cond[SUBSCRPT_AREA_CODE_NM::EQ]': sido}
    if since:
        p['cond[RCRIT_PBLANC_DE::GTE]'] = since
    return _get(DETAIL, 'getAPTLttotPblancDetail', p)


def rank1_rates(house_manage_no, pblanc_no):
    """공고 하나의 1순위 해당지역 경쟁률만 [(주택형, 경쟁률), …] 로.

    RESIDE_SECD 01 이 해당지역이고 SUBSCRPT_RANK_CODE 1 이 1순위다. 둘을 안 고르면
    같은 주택형이 순위·거주지마다 여러 줄로 와서 평균이 뜻을 잃는다."""
    rows = _get(CMPET, 'getAPTLttotPblancCmpet', {
        'page': 1, 'perPage': 200,
        'cond[HOUSE_MANAGE_NO::EQ]': house_manage_no,
        'cond[PBLANC_NO::EQ]': pblanc_no})
    out = []
    for r in rows:
        if str(r.get('RESIDE_SECD')) != '01':
            continue
        if str(r.get('SUBSCRPT_RANK_CODE')) not in ('1', '01'):
            continue
        try:
            out.append((r.get('HOUSE_TY'), float(r.get('CMPET_RATE'))))
        except (TypeError, ValueError):
            # CMPET_RATE 가 "-"(그 구간 신청자 0)로 오는 행이 있다 — 값이 아니라 결측이다
            continue
    return out


def _rate1_summary(house_manage_no, pblanc_no):
    """공고 하나의 1순위 해당지역 경쟁률을 한 문자열로. 주택형이 여럿이면
    「최소~최대」, 하나면 그 값 하나. 잡힌 값이 없으면(접수 전이거나 신청자 0) None —
    빈 문자열이나 0으로 채우지 않는다."""
    rates = [v for _t, v in rank1_rates(house_manage_no, pblanc_no)]
    if not rates:
        return None
    lo, hi = min(rates), max(rates)
    return _fmt_rate(lo) if lo == hi else '%s~%s' % (_fmt_rate(lo), _fmt_rate(hi))


_HOUSE_TY_RE = re.compile(r'^(\d+(?:\.\d+)?)')


def _house_ty_ex(v):
    """HOUSE_TY("059.9442A")의 앞자리를 전용면적(㎡)으로. 2026-09-04에 실제 응답을
    찍어 확인했다 — getAPTLttotPblancMdl 에는 EXCLUSE_AR 같은 별도 필드가 없다.
    HOUSE_TY 의 정수부(예 "059")가 청약 화면이 부르는 「59형」 그 숫자와 같다."""
    m = _HOUSE_TY_RE.match(str(v or '').strip())
    if not m:
        return None
    try:
        return float(m.group(1))
    except ValueError:
        return None


def apt_types(house_manage_no, pblanc_no):
    """공고 하나의 주택형별 상세 — [{ty, ex, sup, top}, …], 전용면적(ex) 오름차순.

    getAPTLttotPblancMdl 은 주택형(모델)마다 한 행을 준다. 세대수(SUPLY_HSHLDCO)나
    분양최고금액(LTTOT_TOP_AMOUNT)이 없는 행은 버린다 — 지어내지 않는다."""
    rows = _get(DETAIL, 'getAPTLttotPblancMdl', {
        'page': 1, 'perPage': 50,
        'cond[HOUSE_MANAGE_NO::EQ]': house_manage_no,
        'cond[PBLANC_NO::EQ]': pblanc_no})
    out = []
    for r in rows:
        ex = _house_ty_ex(r.get('HOUSE_TY'))
        sup = _int_str(r.get('SUPLY_HSHLDCO'))
        top = r.get('LTTOT_TOP_AMOUNT')
        if ex is None or not sup or top in (None, '', '-'):
            continue
        try:
            top_i = int(float(str(top).replace(',', '')))
        except (TypeError, ValueError):
            continue
        out.append({'ty': str(r.get('HOUSE_TY') or '').strip(), 'ex': ex,
                    'sup': int(sup), 'top': top_i})
    out.sort(key=lambda t: t['ex'])
    return out


def _in_gu(row, gu_names):
    """공급위치 문자열에 구 이름이 들었나. 주소가 비면 못 가른다 — 버린다."""
    addr = str(row.get('HSSPLY_ADRES') or '')
    return [g for g in gu_names if g in addr]


def _int_str(v):
    """세대수 같은 숫자값을 문자열로. API 가 int 로도 "468" 로도 준다 — 콤마가
    섞여 오는 경우까지 받는다. 파싱이 안 되면 None(값을 지어내지 않는다)."""
    try:
        n = int(float(str(v).replace(',', '')))
    except (TypeError, ValueError):
        return None
    return str(n)


def _ym(v):
    """"202903"(YYYYMM) → "2029-03". 꼴이 아니면 None."""
    s = str(v or '').strip()
    if len(s) != 6 or not s.isdigit():
        return None
    return '%s-%s' % (s[:4], s[4:6])


def fetch(target_name, area=None, laws=()):
    """워치 계약대로 metric 을 돌려준다. 열쇠가 없으면 빈 dict 와 함께 사유를 알린다.

    target_name 은 정책 줄 이름(「청약 제도」)이고, 서울 25구 + 성남 3구를 한 줄이
    함께 본다. `pblanc_gu` 는 구마다 공고 목록을 묶은 지도용 산출(by_gu)이고,
    `pblanc_cnt_<권역>`·`pblanc_list_<권역>`(세 권역만)은 「청약 — 조건」 절의
    표가 그대로 쓰던 것이라 남긴다. 공고 하나당 경쟁률 호출(_rate1_summary)과
    구 판정(_in_gu)은 한 번만 돈다 — 세 권역이 서로소라 나중에 권역별로 다시
    나눠 담아도 세 권역 몫은 이전과 같다."""
    try:
        rows = pblancs('서울', since=_six_months_ago(), page_size=200)
    except NoKey as e:
        # 값을 못 받았다는 것을 지어낸 값으로 덮지 않는다. 빈 손이 정확한 답이다.
        fetch.last_error = str(e)
        fetch.rate_error = None
        fetch.gg_error = None
        return {}
    except Exception as e:                      # 게이트웨이 장애·응답 꼴 변경
        fetch.last_error = '%s: %s' % (type(e).__name__, e)
        fetch.rate_error = None
        fetch.gg_error = None
        return {}

    # 경기(성남) — 서울 몫은 이미 손에 있으니 이 호출이 죽어도 통째로 안 비운다.
    # 경기는 서울보다 공고가 많을 수 있어 perPage 를 넉넉히 잡는다(500) — 그래도
    # 다음 페이지를 못 받으면 놓친 공고가 있을 수 있다는 것을 src 에 적는다.
    fetch.gg_error = None
    try:
        gg_rows = pblancs('경기', since=_six_months_ago(), page_size=500)
        # 보고 있는 경기 시군구만 남긴다 — 2026-09-04 동탄(화성시)·광교(수원 영통구)·
        # 평촌(안양 동안구)·남한산성(광주시)을 더했다. 경기 sido 로 받은 행이라 「광주시」는
        # 경기 광주다(광주광역시는 sido 가 다르다)
        gg_keep = ('성남시', '화성시', '영통구', '동안구', '광주시')
        rows = rows + [r for r in gg_rows
                       if any(k in str(r.get('HSSPLY_ADRES') or '') for k in gg_keep)]
    except Exception as e:                       # noqa: BLE001 — 경기 몫만 빠진다
        fetch.gg_error = '%s: %s' % (type(e).__name__, e)

    fetch.last_error = None
    fetch.rate_error = None
    fetch.types_error = None
    rate_ok = True    # 경쟁률 서비스가 도중에 죽으면 남은 공고는 조용히 건너뛴다
    types_ok = True   # getAPTLttotPblancMdl 이 도중에 죽으면 남은 공고는 조용히 건너뛴다
    matched = []       # [(구, row, item), …] — 구를 뽑은 공고만
    n_unmatched = 0     # 공급위치 주소에 28구 이름이 하나도 안 걸린 공고
    for r in rows:
        gu_hit = _in_gu(r, ALL_GU)
        if not gu_hit:
            n_unmatched += 1
            continue
        gu = gu_hit[0]
        it = {
            'id': str(r.get('HOUSE_MANAGE_NO') or ''),
            'name': r.get('HOUSE_NM') or '',
            'gu': gu,
            'apply': r.get('RCEPT_BGNDE') or None,
            'announce': r.get('PRZWNER_PRESNATN_DE') or None,
            # 공고 시점의 값이다 — 위 머리 5번 참고
            'cap': _yn(r.get('PARCPRC_ULS_AT')),
            'hot': _yn(r.get('SPECLT_RDN_EARTH_AT')),
        }
        # 2026-09-04 — 청약 공고 화면(watch/청약 공고.html)이 쓰는 필드 여섯.
        # 없으면 키 자체를 안 둔다 — 「값은 원문에 있는 것만」(화면은 「—」를 안 찍는다).
        url = r.get('PBLANC_URL')
        if url:
            it['url'] = url
        end = r.get('RCEPT_ENDDE') or None
        if end:
            it['end'] = end
        total = _int_str(r.get('TOT_SUPLY_HSHLDCO'))
        if total:
            it['total'] = total
        movein = _ym(r.get('MVN_PREARNGE_YM'))
        if movein:
            it['movein'] = movein
        sp_apply = r.get('SPSPLY_RCEPT_BGNDE') or None
        if sp_apply:
            it['sp_apply'] = sp_apply
        pblanc_de = r.get('RCRIT_PBLANC_DE') or None
        if pblanc_de:
            it['pblanc_de'] = pblanc_de
        builder = r.get('CNSTRCT_ENTRPS_NM') or None
        if builder:
            it['builder'] = builder
        hmpg = r.get('HMPG_ADRES') or None
        if hmpg:
            it['hmpg'] = hmpg
        hmn, pno = r.get('HOUSE_MANAGE_NO'), r.get('PBLANC_NO')
        if rate_ok and hmn and pno:
            try:
                rate1 = _rate1_summary(hmn, pno)
            except NoKey as e:
                rate_ok = False
                fetch.rate_error = str(e)
                rate1 = None
            except Exception as e:            # 게이트웨이 장애 등 — 15098905 미승인 포함
                rate_ok = False
                fetch.rate_error = '%s: %s' % (type(e).__name__, e)
                rate1 = None
            if rate1:
                it['rate1'] = rate1
        # 평수·분양가 — 주택형별 상세(청약공고_스펙 추가 §1). 공고당 1회만 부른다
        if types_ok and hmn and pno:
            try:
                types = apt_types(hmn, pno)
            except NoKey as e:
                types_ok = False
                fetch.types_error = str(e)
                types = []
            except Exception as e:            # 게이트웨이 장애 등
                types_ok = False
                fetch.types_error = '%s: %s' % (type(e).__name__, e)
                types = []
            if types:
                it['types'] = types
        matched.append((gu, r, it))

    by_gu = {}
    for gu, r, it in matched:
        by_gu.setdefault(gu, []).append((str(r.get('RCEPT_BGNDE') or ''), it))
    for gu in by_gu:
        by_gu[gu] = [it for _k, it in
                     sorted(by_gu[gu], key=lambda t: t[0], reverse=True)]

    latest_all = max((str(r.get('RCRIT_PBLANC_DE') or '') for _g, r, _it in matched),
                      default='')
    out = {
        'pblanc_gu': {
            'value': len(matched),
            'by_gu': by_gu,
            'as_of': (latest_all[:7] or '확인 못 함'),
            'kind': '공표',
            'unit': '건(모집공고)',
            'src': ('공공데이터포털 15098547 한국부동산원_청약홈 분양정보 조회 · '
                    'getAPTLttotPblancDetail · 최근 6개월 서울+경기(성남시만) 공고 %d건 중 '
                    '공급위치에서 28구 이름을 찾은 것 %d건(못 찾은 것 %d건) · 주소 문자열 '
                    '매칭이라 구를 잘못 골랐거나 놓친 공고가 있을 수 있다%s'
                    % (len(rows), len(matched), n_unmatched,
                       ' · 경기 몫을 못 받았다: %s' % fetch.gg_error if fetch.gg_error else '')),
            # 공고는 달마다 나오지 않는다. 한 점을 선으로 만들지 않는다
            'series': [],
            'partial': False,
        }
    }
    for area_name, gus in AREA_GU.items():
        area_key = area_name.replace(' ', '')
        area_hit = sorted(((r, it) for gu, r, it in matched if gu in gus),
                          key=lambda t: str(t[0].get('RCEPT_BGNDE') or ''), reverse=True)
        latest = max((str(r.get('RCRIT_PBLANC_DE') or '') for r, _it in area_hit),
                     default='')
        note = ('공공데이터포털 15098547 한국부동산원_청약홈 분양정보 조회 · '
                'getAPTLttotPblancDetail · 최근 6개월 서울 공고 %d건 중 공급위치에 %s 가 든 것 '
                '· 주소 문자열 매칭이라 놓친 공고가 있을 수 있다'
                % (len(rows), '·'.join(gus)))
        items = [it for _r, it in area_hit]
        out['pblanc_cnt_' + area_key] = {
            'value': len(items),
            'as_of': (latest[:7] or '확인 못 함'),
            'kind': '공표',
            'unit': '건(모집공고)',
            'src': note,
            'area': area_name,
            'series': [],
            'partial': False,
        }
        out['pblanc_list_' + area_key] = {
            'value': len(items),
            'items': items,
            'as_of': (latest[:7] or '확인 못 함'),
            'kind': '공표',
            'unit': '건(모집공고)',
            'src': note,
            'area': area_name,
            'series': [],
            'partial': False,
        }
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    got = fetch('청약 제도')
    if not got:
        print('값 없음 — %s' % (getattr(fetch, 'last_error', None) or '사유 불명'))
        print('열쇠 발급: https://www.data.go.kr/data/15098547/openapi.do '
              '(분양정보) · https://www.data.go.kr/data/15098905/openapi.do (경쟁률)')
        print('발급 뒤 환경변수 %s 에 넣는다.' % KEY_ENV)
    else:
        gg_err = getattr(fetch, 'gg_error', None)
        if gg_err:
            print('경고: 경기(성남) 몫을 못 받았다 — %s\n' % gg_err)
        rate_err = getattr(fetch, 'rate_error', None)
        if rate_err:
            print('경고: 경쟁률(15098905)을 못 받았다 — %s\n' % rate_err)
        types_err = getattr(fetch, 'types_error', None)
        if types_err:
            print('경고: 주택형 상세(getAPTLttotPblancMdl)를 못 받았다 — %s\n' % types_err)
        for k, v in sorted(got.items()):
            if k == 'pblanc_gu':
                by_gu = v['by_gu']
                n_items = sum(len(x) for x in by_gu.values())
                print('  %-24s %d건 · %d구 (%s 기준, 항목 수 검산 %d)'
                      % (k, v['value'], len(by_gu), v['as_of'], n_items))
                for gu in sorted(by_gu, key=lambda g: -len(by_gu[g])):
                    print('      %-6s %d건' % (gu, len(by_gu[gu])))
            elif k.startswith('pblanc_list_'):
                n_rate = sum(1 for it in v['items'] if it.get('rate1'))
                print('  %-24s %d건 (%s 기준, 경쟁률 %d건)' % (k, v['value'], v['as_of'], n_rate))
            else:
                print('  %-24s %s %s  (%s)' % (k, v['value'], v['unit'], v['as_of']))
