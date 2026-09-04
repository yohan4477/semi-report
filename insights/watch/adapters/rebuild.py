# -*- coding: utf-8 -*-
"""정비사업 어댑터 — 재건축·재개발·리모델링 등 진행 현황을 두 원천에서 받는다.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 다섯.

1. **열쇠가 없다.** cleanup.seoul.go.kr(서울시 정비사업 정보몽땅)도 gg.go.kr/onnuri
   (경기도 정비사업 종합관리시스템)도 로그인·API 키가 필요 없다 — 둘 다 서버사이드
   렌더링 HTML 이고, 여기서는 requests·bs4 없이 표준 라이브러리 정규식으로만 읽는다.
2. **서울 9구는 자치구 코드로, 성남 3구는 인라인 배열로.** cleanup.seoul.go.kr 은
   `scupBsnsSttus.signguCode` 파라미터로 구를 거른다(구마다 GET 한 번). gg.go.kr/onnuri
   는 경기도 전역 사업장 배열을 페이지 인라인 `<script>` 에 한 번에 다 싣는다 —
   서버 파라미터로 성남만 거르는 길이 없어(2026-09-04 조사) 클라이언트에서
   `sigunSeNm`(예 "성남시 중원구")에 "성남시" 가 든 행만 남긴다.
3. **gg.go.kr/onnuri 는 브라우저 User-Agent 가 아니면 WAF 가 막는다.** curl 기본
   UA 로는 "보안 정책에 의해 차단되었습니다" 가 온다(2026-09-04 확인) — 두 원천 모두
   같은 UA 헤더를 붙인다.
4. **사업구분은 원문 텍스트가 표마다 다르다.** cleanup 은 "재개발(주택정비형)"처럼
   괄호가 붙고, onnuri 는 "재개발"만 온다 — `_norm_type` 이 여덟 갈래(재건축·재개발·
   리모델링·가로주택정비·소규모재건축·소규모재개발·지역주택·기타)로 좁힌다. 소규모
   재건축·소규모재개발은 "재건축"·"재개발" 부분일치보다 먼저 검사해야 한다 —
   순서를 바꾸면 소규모 사업이 일반 재건축/재개발로 잘못 잡힌다.
5. **한쪽이 죽어도 나머지는 지킨다.** 서울 9구 요청과 성남 배열 요청은 따로
   실패한다 — 하나가 죽으면 `fetch.last_error` 에 사유만 적고 남은 쪽 데이터로
   돌아온다. 둘 다 죽었을 때만 예외를 던진다. 값을 지어내지 않는다 — 못 받은
   구는 빈 목록이다.
"""
import re
import html
import datetime
import urllib.request
from collections import Counter

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36')

CLEANUP_BASE = 'https://cleanup.seoul.go.kr/cleanup/bsnssttus/lscrMainIndx.do'
# 사업장 팝업(cafeOpenPopup)이 여는 실제 GET 페이지 — /cafe/mainIndx.do?cafeUrl=<slug>.
# js function 정의(같은 페이지)에서 확인했다(2026-09-04). 지도 팝업(mapOpenPopup)은
# urban.seoul.go.kr 로 가는 별개 주소라 여기서는 안 쓴다.
CLEANUP_CAFE = 'https://cleanup.seoul.go.kr/cafe/mainIndx.do?cafeUrl=%s'
GG_URL = 'https://www.gg.go.kr/onnuri/view.do?no=109'

# 서울 9구 — 자치구 코드는 cleanup.seoul.go.kr 폼(scupBsnsSttus.signguCode)에서
# 확인(2026-09-04). 손으로 새로 찾지 않는다.
SEOUL_GU = {
    '강남구': '11680', '서초구': '11650', '송파구': '11710',
    '마포구': '11440', '용산구': '11170', '성동구': '11200',
    '노원구': '11350', '도봉구': '11320', '강북구': '11305',
}
SEONGNAM_GU = ('분당구', '수정구', '중원구')
# 경기도 온누리의 sigunSeNm → 판 이름. 2026-09-04 동탄·광교·평촌·남한산성(화성시·
# 수원 영통구·안양 동안구·광주시)을 더했다 — 시 단위 대상은 시 이름 그대로
GG_GU = {'성남시 분당구': '분당구', '성남시 수정구': '수정구', '성남시 중원구': '중원구',
         '수원시 영통구': '영통구', '안양시 동안구': '동안구',
         '화성시': '화성시', '광주시': '광주시'}
ALL_GU = tuple(SEOUL_GU) + tuple(GG_GU.values())

# gg.go.kr/onnuri 인라인 배열의 필드 순서 — bizaraId, bizaraNm, addr, sigunSeNm,
# bizTypeNm, bizaraStepNm 그대로(2026-09-04 실측). 순서가 바뀌면 이 정규식이
# 통째로 못 잡는다 — 그때는 값이 하나도 안 나오므로 조용히 틀리지는 않는다.
_GG_ROW = re.compile(
    r"bizaraId:\s*'((?:[^'\\]|\\.)*)',\s*"
    r"bizaraNm:\s*'((?:[^'\\]|\\.)*)',\s*"
    r"addr:\s*'((?:[^'\\]|\\.)*)',\s*"
    r"sigunSeNm:\s*'((?:[^'\\]|\\.)*)',\s*"
    r"bizTypeNm:\s*'((?:[^'\\]|\\.)*)',\s*"
    r"bizaraStepNm:\s*'((?:[^'\\]|\\.)*)'",
    re.S)

# cleanup.seoul.go.kr 표의 한 행 — 번호·자치구·사업구분·사업장명·대표지번·진행단계
# (그 뒤 공개자료수·공개적시성·자료충실도·이동 세 열은 안 쓴다).
_CLEANUP_ROW = re.compile(
    r'<td[^>]*>\s*\d+\s*</td>\s*'
    r'<td[^>]*>([^<]*)</td>\s*'   # 자치구
    r'<td[^>]*>([^<]*)</td>\s*'   # 사업구분
    r'<td[^>]*>([^<]*)</td>\s*'   # 사업장명
    r'<td[^>]*>([^<]*)</td>\s*'   # 대표지번
    r'<td[^>]*>([^<]*)</td>',     # 진행단계
    re.S)
_CAFE_SLUG = re.compile(r"cafeOpenPopup\('([^']*)'\)")


def _strip_html(s):
    return html.unescape(re.sub(r'<[^>]*>', '', s or '')).strip()


def _strip_js(s):
    """onnuri 인라인 배열의 작은따옴표 JS 문자열 이스케이프를 푼다."""
    s = (s or '').replace("\\'", "'").replace('\\\\', '\\')
    return html.unescape(s).strip()


def _norm_type(raw):
    """사업구분 원문을 여덟 갈래로 좁힌다. 소규모재건축/소규모재개발을 먼저
    검사한다 — 부분일치라 순서를 바꾸면 재건축/재개발로 잘못 잡힌다."""
    s = (raw or '').strip()
    if '리모델링' in s:
        return '리모델링'
    if '가로주택' in s:
        return '가로주택정비'
    if '소규모재건축' in s:
        return '소규모재건축'
    if '소규모재개발' in s:
        return '소규모재개발'
    if '지역주택' in s:
        return '지역주택'
    if '재개발' in s:
        return '재개발'
    if '재건축' in s:
        return '재건축'
    return '기타' if s else '기타'


def _http_get(url, headers=None, timeout=30, retries=1):
    last = None
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:                       # noqa: BLE001 — 마지막 시도만 던진다
            last = e
    raise last


def _cleanup_gu(code, page_size=300, max_pages=20):
    """cleanup.seoul.go.kr 에서 구 하나의 사업장 목록을 받는다. pageSize 를 다
    채운 페이지가 오면(더 있을 수 있다는 뜻) 다음 페이지를 이어 받는다."""
    items = []
    for page in range(1, max_pages + 1):
        url = ('%s?cpage=%d&pageSize=%d&scupBsnsSttus.signguCode=%s'
               % (CLEANUP_BASE, page, page_size, code))
        body = _http_get(url, headers={'User-Agent': UA})
        i = body.find('<tbody>')
        j = body.find('</tbody>', i if i >= 0 else 0)
        table = body[i:j] if (i >= 0 and j > i) else ''
        trs = re.findall(r'<tr>(.*?)</tr>', table, re.S)
        page_items = []
        for tr in trs:
            m = _CLEANUP_ROW.search(tr)
            if not m:
                continue
            _gu_txt, type_txt, name_txt, addr_txt, stage_txt = m.groups()
            slug_m = _CAFE_SLUG.search(tr)
            slug = slug_m.group(1) if slug_m else ''
            name = _strip_html(name_txt)
            item = {
                'id': slug or ('%s-%s' % (code, name)),
                'name': name,
                'type': _norm_type(_strip_html(type_txt)),
                'stage': _strip_html(stage_txt),
                'addr': _strip_html(addr_txt),
                'src': 'cleanup_seoul',
                'url': (CLEANUP_CAFE % slug) if slug else '',
            }
            page_items.append(item)
        items.extend(page_items)
        if len(page_items) < page_size:
            break
    return items


def _gg_seongnam():
    """gg.go.kr/onnuri 인라인 배열에서 성남시(분당·수정·중원) 행만 골라낸다.
    돌려주는 값은 [(구 이름, item), ...] — by_gu 에 넣기 전 형태다."""
    body = _http_get(GG_URL, headers={'User-Agent': UA}, timeout=30)
    out = []
    for bid, name, addr, sigun, btype, step in _GG_ROW.findall(body):
        sigun_kr = ' '.join(_strip_js(sigun).split())
        gu = GG_GU.get(sigun_kr)
        if gu is None:
            continue
        item = {
            'id': _strip_js(bid),
            'name': _strip_js(name),
            'type': _norm_type(_strip_js(btype)),
            'stage': _strip_js(step),
            'addr': _strip_js(addr),
            'src': 'gg_onnuri',
            'url': '',   # 상세는 AJAX(show())로만 열려 정적 주소가 없다
        }
        out.append((gu, item))
    return out


def fetch(target_name, area=None, laws=()):
    """워치 계약대로 metric 을 돌려준다. 한 키 `rebuild_gu` — 서울 9구(cleanup.seoul.go.kr)
    + 성남 3구(gg.go.kr/onnuri) 12구를 by_gu 로 담는다. 한쪽 원천이 죽어도 나머지
    구는 지킨다 — `fetch.last_error` 에 사유를 적고, 둘 다 죽었을 때만 예외를 던진다."""
    by_gu = {gu: [] for gu in ALL_GU}
    errors = []

    seoul_ok = False
    try:
        for gu_name, code in SEOUL_GU.items():
            by_gu[gu_name] = _cleanup_gu(code)
        seoul_ok = True
    except Exception as e:                            # noqa: BLE001 — 서울 몫만 빠진다
        errors.append('cleanup.seoul.go.kr: %s: %s' % (type(e).__name__, e))

    gg_ok = False
    try:
        for gu, item in _gg_seongnam():
            by_gu[gu].append(item)
        gg_ok = True
    except Exception as e:                            # noqa: BLE001 — 성남 몫만 빠진다
        errors.append('gg.go.kr/onnuri: %s: %s' % (type(e).__name__, e))

    fetch.last_error = '; '.join(errors) if errors else None
    if not seoul_ok and not gg_ok:
        raise RuntimeError(fetch.last_error or '두 원천 모두 실패')

    total = sum(len(v) for v in by_gu.values())
    return {
        'rebuild_gu': {
            'value': total,
            'unit': '건',
            'as_of': datetime.date.today().isoformat(),
            'src': '%s;%s' % (CLEANUP_BASE, GG_URL),
            'level': 'public',
            'by_gu': by_gu,
        }
    }


if __name__ == '__main__':
    try:
        got = fetch('정비사업')
    except Exception as e:
        print('실패 — %s' % e)
        raise SystemExit(1)

    err = getattr(fetch, 'last_error', None)
    if err:
        print('경고: 한쪽 원천을 못 받았다 — %s\n' % err)

    m = got['rebuild_gu']
    by_gu = m['by_gu']
    print('rebuild_gu  %d건 · %d구 (%s 기준)' % (m['value'], len(by_gu), m['as_of']))
    for gu in ALL_GU:
        print('  %-6s %d건' % (gu, len(by_gu.get(gu, []))))

    all_items = [it for items in by_gu.values() for it in items]
    print('\n사업구분:')
    for k, v in sorted(Counter(it['type'] for it in all_items).items(),
                        key=lambda x: -x[1]):
        print('  %-8s %d건' % (k, v))
    print('\n진행단계:')
    for k, v in sorted(Counter(it['stage'] for it in all_items).items(),
                        key=lambda x: -x[1]):
        print('  %-14s %d건' % (k, v))

    for gu in ('강남구', '수정구'):
        print('\n%s 표본:' % gu)
        for it in by_gu.get(gu, [])[:2]:
            print('  %s · %s · %s' % (it['name'], it['type'], it['stage']))
