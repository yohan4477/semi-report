# -*- coding: utf-8 -*-
"""포트폴리오 워치 — 감시 화면. 아카이브 부품(dash_common)을 안 쓴다.

왜 따로 짰나. 아카이브는 카드가 쌓이니 접어서 고르게 만든 부품이고, 이 장은 열 줄이
안 늘고 매달 같은 것을 다시 본다. 접힘·타일·카드 세 겹이 「무엇이 바뀌었나」 앞을
막아서, 두 번 우회한 뒤(home='all' · tiles=False) 뼈대째 걷었다.

규약은 check_ui() 가 생성 때 검사한다. 규약을 우회하려고 나온 장이 규약이 없는 장이
되면 다음 사람이 같은 자리를 다시 판다.

2026-09-02 에 맨 위 띠를 「지금 걸린 것」에서 「지난 확인 이후」로 바꿨다. 한 달에 한
번 여는 독자에게 「지금 걸려 있다」는 새 정보가 아니다 — 지난달에도 걸려 있었을 수
있다. 정말 새 정보는 「지난번과 달라진 것」이라 `insights/watch/_seen.json`
(scripts/watch_mark.py 가 찍는 스냅숏)과 지금 상태를 견줘 새로 걸린·새로 근접·풀린·
그대로 걸린 네 묶음으로 가른다. 그 파일이 없으면(한 번도 확인한 적이 없으면) 비교할
기준점이 없다는 뜻이라 지금 걸린 것을 전부 「새로」로 센다.

트리거 표는 이제 여섯 열(watch_lib.py 머리 주석 참고)이고, 값 트리거에는 「걸리면」
(다음에 할 일)이, 사건 트리거에는 「걸리면」·「확인처」(사람이 확인하는 URL)가 붙는다.
줄 하나가 `## 이력` 절을 두면 「판단 이력」 표로 낸다 — 판단이 언제 왜 바뀌었는지가
「지금 판단」 문단 하나에는 안 남는다.

2026-09-02 두 번째 변경 — 화면을 두 층으로 가른다. 도해 26장·표 32개·줄 열 개가
한 장에 다 펼쳐져 있어 390px 폰에서 스크린 수십 개였다. 이 장을 여는 이유는
「지난번 이후 무엇이 바뀌었나 → 내 판단을 건드리나 → 뭘 하나」 셋뿐이라, 그 답이
되는 것(지난 확인 이후·권역 견주기·제도 요약·줄 목록)만 본 장에 남기고 줄마다의
상세(트리거 표·도해·이력·반대 근거)는 `watch/<슬러그>.html` 로 뺐다. **접지는
않는다** — 이 장의 규약이 접힘을 금지한다. 대신 페이지를 가른다. 법·고시 전체 표는
같은 이유로 `watch/제도.html` 로 옮겼다.

2026-09-02 세 번째 변경 — 화면을 「연구 노트」에서 「제품」으로 다시 세운다. 사용자가
「uiux 가 이따위면 돈 내고 쓰겠냐」로 지적한 자리다. 문제는 두 가지였다.
① 맨 위가 값이 아니라 메타데이터였다 — 열자마자 보이는 것이 「자료 기준」 날짜지
「지금 전세가 나은가」가 아니었다. ② 라벨이 10px 회색 대문자 자간(「TRIGGER」류)으로
저장소 안에서만 통하는 말(「때 자」「줄」「성격」)을 그대로 화면에 냈다.
고친 것 셋 — (a) 권역마다 지금 값이 큰 글씨로 서는 카드 셋과, 세 권역을 한 줄에
놓는 「전세가율 자」를 새로 그렸다(둘 다 없는 값은 안 그린다 — 원문 밖 값 금지는
그대로다). (b) 색을 이름과 값 둘로 나눴다 — 상태(걸림·근접)는 먹색·황토, 방향
(석 달 전 대비 오름·내림)만 --up/--down 이다. (c) 절 제목·표 열 이름에서 은어
넷(「때 자」「줄」「성격」「언제 것」)을 걷었다 — check_ui()·check_detail_ui() 가
그 넷이 화면에 남으면 FAIL 한다.
"""
import datetime
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import watch_lib as wl          # noqa: E402
import watch_fig as wf          # noqa: E402

OUT = os.path.join(ROOT, '대시보드', '포트폴리오 워치.html')
WATCH_DIR = os.path.join(ROOT, '대시보드', 'watch')
AREAS_PATH = os.path.join(ROOT, 'insights', 'watch', '_areas.json')
E = wl.esc
# 청약 공고 상태는 화면을 만드는 날 기준으로 빌드 때 박는다(JS 계산 금지 — 이 장의
# 기존 규약). 배포까지 며칠 걸려도 사용자가 보는 상태가 만든 날짜와 다르게
# 보이지 않도록 캡션에 이 날짜를 그대로 적는다.
_TODAY = datetime.date.today().strftime('%Y-%m-%d')

KIND_LABEL = {'realestate': '부동산', 'policy': '제도', 'equity': '종목'}


def _load_areas():
    """권역 → 구 목록 정본. 손으로 구 이름을 박지 않는다 — insights/watch/_areas.json
    이 바뀌면(권역 경계 수정 등) 화면이 자동으로 따라가야 한다."""
    with io.open(AREAS_PATH, encoding='utf-8') as f:
        d = json.load(f)
    return dict((k, v) for k, v in d.items() if not k.startswith('_'))


AREAS = _load_areas()


def _gu_short(target):
    """권역 이름 옆에 구 셋을 짧게 푼다(「노원·도봉·강북」류) — AREAS 정본에서만 읽는다.
    자(ruler)의 점 라벨은 대상이 아니다 — 거기는 짧게 그대로 둔다(자리가 좁다)."""
    gus = (AREAS.get(target) or {}).get('구') or []
    return '·'.join(g[:-1] if g.endswith('구') else g for g in gus)


def _area_head(target):
    """카드 머리·상세 eyebrow 에 쓰는 「권역 — 구 셋」. 구가 없으면(정책 줄 등) 그냥
    권역 이름이다."""
    gu = _gu_short(target)
    return '%s — %s' % (target, gu) if gu else target


# ── 서울 지도 (2026-09-03) ─────────────────────────────────────────────────
# southkorea/seoul-maps 의 25개 구 경계와 서울부동산정보광장·국토교통부 지정 현황을
# 읽기만 한다(손으로 안 고친다). 지도가 첫 화면이고 나머지 정보는 지도에서 나온다 —
# 사용자 지시(2026-09-03) 「계속 밑으로 내리는 것보다 지도를 통해서 모든 정보를
# 보여줄 수 있잖아」. 구를 손대면(호버·포커스) 오른쪽 패널이 그 구로 바뀌고,
# 누르면(클릭·Enter) 권역에 든 구만 그 권역 상세로 넘어간다.
SEOUL_GU_PATH = os.path.join(ROOT, 'insights', 'watch', '_seoul_gu.json')
ZONES_PATH = os.path.join(ROOT, 'insights', 'watch', '_zones.json')


def _load_json(path):
    with io.open(path, encoding='utf-8') as f:
        return json.load(f)


SEOUL_GU = _load_json(SEOUL_GU_PATH)
ZONES = _load_json(ZONES_PATH)
# 구 → 권역. 보는 것은 넷뿐이라(강남 3구·노도강·마용성·성남) 그 구 열둘만 채워진다.
# 나머지는 지도에 있지만 「보고 있지 않은 구」다.
GU_REGION = dict((g, t) for t in AREAS if isinstance(AREAS[t], dict)
                 for g in AREAS[t].get('구', []))
WATCHED_GU = sorted(GU_REGION)
# 시·도 — 첫 화면의 최상위 갈래다(2026-09-04 사용자 지시 「서울 경기 구분이 가장 상위」).
# 성남 3구만 경기, 나머지(서울 25구)는 서울. 지도·분양·달라진 것·보고 있는 것이
# 전부 이 갈래 아래 선다 — 제도·청약 조건·자료 기준은 전국 공통이라 밖에 남는다
SIDOS = (('서울', ''), ('경기', '-gg'))
_GYEONGGI_GU = set(g for t, v in AREAS.items() if isinstance(v, dict)
                   and v.get('sido') == '경기' for g in v.get('구', []))


def _sido_of(gu):
    return '경기' if gu in _GYEONGGI_GU else '서울'


def _sido_gus(sido):
    return sorted(g for g in SEOUL_GU['gu'] if _sido_of(g) == sido)


def _area_sido(target):
    gus = AREAS.get(target, {}).get('구') or []
    return _sido_of(gus[0]) if gus else '서울'


def _sido_watches(watches, sido):
    """그 시·도의 실거주·투자 줄만 — 제도 줄(전국)은 안 든다."""
    return [w for w in watches if w['kind'] == 'realestate' and _area_sido(w['target']) == sido]


def _ratio_bin(v):
    """전세가율 값 → 다섯 단 순차 램프의 몇 번째 칸인가. <45·45~50·50~55·55~60·≥60."""
    if v is None:
        return None
    for edge, b in ((45, 1), (50, 2), (55, 3), (60, 4)):
        if v < edge:
            return b
    return 5


def _lth_info(gu):
    """토지거래허가구역 (값, 상세)."""
    e = (ZONES.get('토지거래허가구역', {}).get('gu', {}) or {}).get(gu) or {}
    return e.get('value'), e.get('detail')


def _reg_info(gu):
    """조정대상지역·투기과열지구 여부(True/False/None 각각)."""
    adj = ((ZONES.get('조정대상지역', {}).get('gu', {}) or {}).get(gu) or {}).get('value')
    hot = ((ZONES.get('투기과열지구', {}).get('gu', {}) or {}).get(gu) or {}).get('value')
    return adj, hot


def _cap_info(gu):
    """민간택지 분양가상한제 (값, 상세). 규제지역과 별개 지정이라 층이 따로다 —
    서울이 전역 투기과열지구가 된 뒤에도 이 층만 넷과 스물하나로 갈린다."""
    e = (ZONES.get('분양가상한제', {}).get('gu', {}) or {}).get(gu) or {}
    return e.get('value'), e.get('detail')


def _cap_counts(gus=None):
    """적용·미적용·확인 안 됨. 손으로 안 센다 — _zones.json 이 바뀌면 화면이 따라간다."""
    vals = [_cap_info(g)[0] for g in (gus or SEOUL_GU['gu'])]
    return (vals.count(True), vals.count(False),
            sum(1 for v in vals if v is None))


def _cap_names(gus=None):
    return sorted(g for g in (gus or SEOUL_GU['gu']) if _cap_info(g)[0] is True)


def _reg_bin(adj, hot):
    """규제지역 채움 칸 — both(둘 다 지정)·one(하나만)·none(둘 다 해제)·null(모름)."""
    if adj is None or hot is None:
        return 'null'
    if adj and hot:
        return 'both'
    if adj or hot:
        return 'one'
    return 'none'


def _lth_counts(gus=None):
    gus = list(gus or SEOUL_GU['gu'])
    gu = (ZONES.get('토지거래허가구역', {}) or {}).get('gu', {}) or {}
    vals = [(gu.get(g) or {}).get('value') for g in gus]
    n_all, n_part, n_none = vals.count('전부'), vals.count('일부'), vals.count('없음')
    return n_all, n_part, n_none, len(gus) - n_all - n_part - n_none


def _reg_counts(gus=None):
    cnt = {'both': 0, 'one': 0, 'none': 0, 'null': 0}
    for name in (gus or SEOUL_GU['gu']):
        cnt[_reg_bin(*_reg_info(name))] += 1
    return cnt


def _region_raw(watches):
    """3 실거주 줄의 원자료(insights/watch/_metrics/) — target 이름으로 찾는다."""
    return dict((w['target'], wl.metrics_of(w['kind'], w['slug'])) for w in _live_areas(watches))


def _sub_gu_data(watches):
    """청약 제도 줄의 pblanc_gu.by_gu — 구 이름 → 최근 6개월 공고 목록(접수일 내림차순).

    (None, None) 은 「어댑터가 못 냈다」(열쇠 없음 등)이고, ({}, as_of) 는 「받았는데
    구가 하나도 안 걸렸다」다 — 지도 층 버튼은 앞의 경우에만 안 낸다. 값이 있는데
    전부 0건인 것과 아예 못 받은 것은 다른 상태라 dict 존재 여부로 가른다."""
    w = next((x for x in watches if x['kind'] == 'policy' and x['slug'] == '청약 제도'), None)
    if w is None:
        return None, None
    m = (w['metrics'] or {}).get('pblanc_gu')
    if m is None:
        return None, None
    return (m.get('by_gu') or {}), m.get('as_of')


# 정비사업 진행 단계 — 정비사업 정보몽땅(서울) 16종을 순서대로. 경기도 온누리(성남)는
# 대분류 넷만 준다(추진주체 구성 전·추진위원회·조합(시행자)·청산위원회) — 둘을 한 자로
# 안 섞고, 화면에는 원천이 준 낱말 그대로 낸다. 큰 묶음 다섯은 화면 요약용이다
REBUILD_STAGES = ('정비계획수립', '재정비촉진지구수립', '안전진단', '정비구역지정', '추진위원회승인',
                  '조합설립인가', '주민대표회의구성통지', '사업시행인가', '관리처분인가',
                  '철거', '착공', '분양', '준공인가', '이전고시', '조합해산', '조합청산',
                  '추진주체 구성 전', '추진위원회', '조합(시행자)', '청산위원회')
def _rebuild_bucket(stage):
    """단계 이름 → 큰 묶음 다섯. 원천의 낱말이 고정돼 있지 않아(「정비계획 수립」·
    「안전진단(1차)」·「철거 및 착공」·「사업계획승인(리모델링 허가)」·빈 값) 이름표가
    아니라 낱말 조각으로 가른다. 순서가 뜻이다 — 「철거 및 착공」은 공사, 「조합해산」은 끝"""
    st = (stage or '').replace(' ', '')
    if any(k in st for k in ('준공', '이전고시', '해산', '청산')):
        return '끝'
    if any(k in st for k in ('착공', '철거', '분양')):
        return '공사'
    if any(k in st for k in ('관리처분', '사업시행', '사업계획승인')):
        return '인가'
    if any(k in st for k in ('조합', '주민대표')):
        return '조합'
    return '구역'


REBUILD_BUCKET_ORDER = ('구역', '조합', '인가', '공사', '끝')
REBUILD_BUCKET_LABEL = {'구역': '구역 지정·추진위까지', '조합': '조합 단계', '인가': '사업시행·관리처분 인가',
                        '공사': '철거·착공·분양', '끝': '준공·청산'}
REBUILD_SLUG = '정비사업'


def _stage_rank(stage):
    """늦은 단계가 큰 수. 묶음이 먼저, 묶음 안에서는 원천 목록 순서"""
    b = REBUILD_BUCKET_ORDER.index(_rebuild_bucket(stage))
    st = (stage or '').replace(' ', '')
    inner = next((i for i, k in enumerate(REBUILD_STAGES) if k.replace(' ', '') in st), 0)
    return b * 100 + inner


def _rebuild_data(watches):
    """정비사업 줄의 rebuild_gu — (by_gu, as_of, src). 어댑터가 못 냈으면 (None, None, None)."""
    w = next((x for x in watches if x['kind'] == 'policy' and x['slug'] == REBUILD_SLUG), None)
    if w is None:
        return None, None, None
    m = (w['metrics'] or {}).get('rebuild_gu')
    if m is None:
        return None, None, None
    return (m.get('by_gu') or {}), m.get('as_of'), m.get('src')


def _rebuild_gu_summary(items):
    """구 하나의 수 — 사업구분별·큰 묶음별."""
    by_type, by_bucket = {}, {}
    for it in items:
        by_type[it.get('type') or '기타'] = by_type.get(it.get('type') or '기타', 0) + 1
        b = _rebuild_bucket(it.get('stage'))
        by_bucket[b] = by_bucket.get(b, 0) + 1
    return by_type, by_bucket


def _rebuild_item_html(it, full=False):
    nm = E(it.get('name') or '—')
    if full and it.get('url'):
        nm = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (E(it['url']), nm)
    parts = [E(it.get('type') or ''), E(it.get('stage') or '단계 미기재')]
    if full and it.get('addr'):
        parts.append(E(it['addr']))
    return ('<div class="rb-item"><p class="si-1">%s <span class="si-gu">%s</span></p>'
            '<p class="si-2 mono">%s</p></div>'
            % (nm, E(it.get('gu') or ''), ' · '.join(p for p in parts if p)))


def rebuild_section(watches, sido='서울', suffix=''):
    """시·도 상자의 「정비사업」 절 — 보고 있는 구마다 사업장 수(재건축·재개발·리모델링)와
    단계 묶음, 인가·공사 단계에 든 사업장 이름 최대 셋. 전부는 watch/정비사업 현황.html.
    어댑터가 못 냈으면 절 자체를 안 낸다(자리표시 금지)."""
    by_gu, as_of, _src = _rebuild_data(watches)
    if by_gu is None:
        return ''
    gus = [g for g in _sido_gus(sido) if g in WATCHED_GU]
    total = sum(len(by_gu.get(g) or []) for g in gus)
    tot_type = {}
    for g in gus:
        for it in by_gu.get(g) or []:
            t = it.get('type') or '기타'
            tot_type[t] = tot_type.get(t, 0) + 1
    type_txt = ' · '.join('%s %d' % (E(t), tot_type[t])
                          for t in ('재건축', '재개발', '리모델링') if tot_type.get(t))
    src_txt = ('서울시 정비사업 정보몽땅' if sido == '서울' else '경기도 정비사업 종합관리시스템')
    h = ['<div class="band" id="rebuild%s"><p class="band-t">정비사업 — 재건축·재개발·리모델링</p>'
         '<p class="cond-lead">보고 있는 %d구 사업장 %d곳%s · %s · 기준 %s</p>'
         % (suffix, len(gus), total, (' — ' + type_txt) if type_txt else '', E(src_txt),
            E(as_of or '—'))]
    for g in gus:
        items = sorted(by_gu.get(g) or [], key=lambda it: -_stage_rank(it.get('stage') or ''))
        by_type, by_bucket = _rebuild_gu_summary(items)
        t_txt = ' · '.join('%s %d' % (E(t), by_type[t]) for t in ('재건축', '재개발', '리모델링')
                           if by_type.get(t))
        b_txt = ' · '.join('%s %d' % (E(REBUILD_BUCKET_LABEL[b]), by_bucket[b])
                           for b in REBUILD_BUCKET_ORDER if by_bucket.get(b))
        late = [it for it in items if _rebuild_bucket(it.get('stage')) in ('인가', '공사')]
        late_html = ''.join(_rebuild_item_html(it) for it in late[:3])
        h.append('<div class="rb-row"><p class="rb-k"><a href="watch/정비사업 현황.html#g-%s">%s</a> '
                 '<span class="rb-n">%d곳</span></p>'
                 '<p class="rb-v">%s</p><p class="rb-v">%s</p>%s</div>'
                 % (E(g), E(g), len(items), t_txt or '사업장 없음', b_txt, late_html))
    h.append('<p class="lbl"><a href="watch/정비사업 현황.html">사업장 전부 보기 →</a></p>')
    h.append('<p class="cond-tail">단계 이름은 원천이 준 그대로입니다. 서울은 16단계, 성남은 '
             '추진주체 구성 전·추진위원회·조합·청산위원회 넷으로만 옵니다 — 성남 「조합」에는 '
             '사업시행인가·관리처분인가·착공이 다 섞여 있습니다.</p>')
    h.append('</div>')
    return ''.join(h)


def rebuild_page(watches):
    """정비사업 사업장 전부 — 대시보드/watch/정비사업 현황.html. 구마다 한 절, 절 안은
    단계 늦은 순(준공·청산이 위, 구역 지정이 아래). 표가 아니라 목록이다."""
    by_gu, as_of, src = _rebuild_data(watches)
    if by_gu is None:
        by_gu, as_of, src = {}, '—', ''
    gus = [g for g in WATCHED_GU if g in by_gu or True]
    gus = sorted(gus, key=lambda g: (_sido_of(g) != '서울', g))
    nav = ('<nav class="jump" aria-label="절 바로가기">%s<a href="#basis">자료 기준</a></nav>'
           % ''.join('<a href="#g-%s">%s %d</a>' % (E(g), E(g), len(by_gu.get(g) or []))
                     for g in gus))
    bands = []
    for g in gus:
        items = sorted(by_gu.get(g) or [], key=lambda it: (-_stage_rank(it.get('stage') or ''),
                                                          it.get('name') or ''))
        by_type, by_bucket = _rebuild_gu_summary(items)
        lead = ' · '.join('%s %d' % (E(t), by_type[t]) for t in sorted(by_type, key=lambda t: -by_type[t]))
        body = (''.join(_rebuild_item_html(it, full=True) for it in items)
                if items else '<p class="cond-lead">원천에 이 구 사업장이 없습니다</p>')
        bands.append('<div class="band" id="g-%s"><p class="band-t">%s · %s — %d곳</p>'
                     '<p class="cond-lead">%s</p><div class="sub-list">%s</div></div>'
                     % (E(g), E(_sido_of(g)), E(g), len(items), lead, body))
    total = sum(len(by_gu.get(g) or []) for g in gus)
    basis = ('<div class="band" id="basis"><p class="band-t">자료 기준</p>'
             '<p class="cond-tail">서울 — 서울시 정비사업 정보몽땅(cleanup.seoul.go.kr) 사업장 목록 · '
             '성남 — 경기도 정비사업 종합관리시스템(gg.go.kr/onnuri) · 자료 기준 %s · '
             '단계 이름은 원천이 준 그대로 · 리모델링은 서울 원천에만 갈래가 있음</p>'
             '<p><a class="back" href="../포트폴리오 워치.html#rebuild">← 포트폴리오 워치</a></p></div>'
             % E(as_of or '—'))
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>정비사업 현황 — 포트폴리오 워치</title>%s<style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#rebuild">'
            '← 포트폴리오 워치</a>'
            '<header><p class="meta mono">사업장 %d곳 · 기준 %s</p><h1>정비사업 현황</h1>'
            '<p class="lede">재건축·재개발·리모델링 사업장이 지금 어느 단계에 있나 — 보고 있는 '
            '%d곳, 단계 늦은 순.</p></header>%s<div class="dbody">%s%s</div>'
            '<footer>서울시 정비사업 정보몽땅과 경기도 정비사업 종합관리시스템에서 받습니다. '
            '매달 다시 확인합니다.</footer>'
            '<!-- 이 화면은 scratchpad/gen_watch_page.py 가 만든다 -->'
            '</div></body></html>'
            % (FONTS, CSS, total, E(as_of or '—'), len(gus), nav, ''.join(bands), basis))


def _all_sub_items(watches):
    """청약 제도 줄의 최근 6개월 공고 전부 — 서울 25구 + 성남 3구를 한 목록으로
    편다(권역 셋에 갇히지 않는다). 어댑터가 못 냈으면(열쇠 없음) (None, None) —
    「청약 공고」 화면·본 장 「청약」 절 축약 둘 다 이 자리를 그냥 비운다."""
    sub_gu, sub_asof = _sub_gu_data(watches)
    if sub_gu is None:
        return None, None
    return [it for lst in sub_gu.values() for it in lst], sub_asof


# 청약공고_스펙 §2 — 상태는 날짜 문자열 비교만으로 기계가 정한다. 종료일이 없으면
# (RCEPT_ENDDE 를 못 받으면) 끝나는 날을 추정해 만들지 않는다 — 접수 시작 당일만
# 「접수 중」으로 보고 다음 날부터 「접수 마감·발표 대기」다.
_SUB_STATUS_CLS = {'접수 중': 't-hit', '접수 예정': 't-near',
                    '접수 마감·발표 대기': 't-clear', '발표됨': 't-none',
                    '일정 미정': 't-none'}


def _sub_status(it, today):
    apply_ = it.get('apply')
    if not apply_:
        return '일정 미정'
    if today < apply_:
        return '접수 예정'
    end_ = it.get('end')
    if end_:
        if apply_ <= today <= end_:
            return '접수 중'
    elif today == apply_:
        return '접수 중'
    announce_ = it.get('announce')
    if announce_:
        return '접수 마감·발표 대기' if today < announce_ else '발표됨'
    if today > apply_:
        return '접수 마감·발표 대기'
    return '일정 미정'


def _period_txt(apply_, end_):
    """접수 기간 — 끝나는 날이 있으면 「2026-08-24~08-26」, 없으면 「2026-08-24~」로
    열어 둔다(끝을 추정하지 않는다)."""
    return '%s~%s' % (apply_, _mmdd(end_)) if end_ else '%s~' % apply_


def _sub_line2(it):
    """둘째 줄 — 접수 기간·발표일·세대수·분양가상한제·입주 예정·특별공급. 없는
    조각은 통째로 뺀다(청약공고_스펙 §6) — 「—」를 찍지 않는다."""
    parts = []
    if it.get('apply'):
        parts.append('접수 %s' % _period_txt(it['apply'], it.get('end')))
    if it.get('announce'):
        parts.append('발표 %s' % it['announce'])
    if it.get('total'):
        parts.append('%s세대' % it['total'])
    cap = it.get('cap')
    if cap is not None:
        parts.append('분양가상한제 %s' % ('적용' if cap else '미적용'))
    if it.get('movein'):
        parts.append('입주 %s' % it['movein'])
    if it.get('sp_apply'):
        parts.append('특별공급 %s' % it['sp_apply'])
    return E(' · '.join(parts))


def _fmt_eok(man_won):
    """만원 → 「n억 m,mmm만원」(m 이 0 이면 「n억」). 청약공고_스펙 추가 §1."""
    man_won = int(man_won)
    eok, rem = divmod(man_won, 10000)
    if eok and rem:
        return '%d억 %s만원' % (eok, format(rem, ',d'))
    if eok:
        return '%d억' % eok
    return '%s만원' % format(rem, ',d')


def _group_types(types):
    """주택형 상세를 전용면적 정수부(「형」)로 묶는다 — 059.9200A·059.9500D·
    059.9600B 는 사람 눈에 다 「59형」이다. 세대수는 더하고 최고금액은 그 형
    안에서 가장 비싼 값을 낸다. ex 는 오름차순으로 이미 정렬돼 들어온다."""
    groups = {}
    order = []
    for t in types:
        k = int(t['ex'])
        if k not in groups:
            groups[k] = {'ex': k, 'sup': 0, 'top': 0}
            order.append(k)
        groups[k]['sup'] += t['sup']
        groups[k]['top'] = max(groups[k]['top'], t['top'])
    return [groups[k] for k in order]


def _fmt_type_item(g):
    """「전용 59㎡(약 18평) 30세대 · 최고 8억 7,500만원」. 평 = ㎡ ÷ 3.3058 반올림
    (청약공고_스펙 추가 §1) — 「약」은 반드시 붙인다."""
    py = int(round(g['ex'] / 3.3058))
    return '전용 %d㎡(약 %d평) %d세대 · 최고 %s' % (g['ex'], py, g['sup'], _fmt_eok(g['top']))


def _sub_types_html(it, full):
    """「주택형」줄 — full(새 페이지)이면 최대 3형(넘으면 「+n형」), 본 장 축약
    (full=False)은 첫 형 하나만(청약공고_스펙 추가 §1). types 가 없으면(어댑터가
    못 받았거나 실패했으면) 통째로 뺀다."""
    types = it.get('types') or []
    if not types:
        return ''
    groups = _group_types(types)
    if not groups:
        return ''
    if full:
        shown = groups[:3]
        extra = len(groups) - len(shown)
        parts = [_fmt_type_item(g) for g in shown]
        if extra > 0:
            parts.append('+%d형' % extra)
    else:
        parts = [_fmt_type_item(groups[0])]
    return '<p class="si-ty mono">%s</p>' % E(' / '.join(parts))


def _watched_market(watches):
    """WATCHED_GU(전세가율·매매가격지수를 추적하는 9구)만 — 구 이름 → (jeonse
    _val3, sale _val3). 청약 항목 「그 구의 시세」 한 줄이 쓴다(청약공고_스펙
    추가 §3). 보고 있지 않은 구는 아예 키가 없다 — 값을 지어내지 않는다."""
    rows_by = _movement_rows(watches)
    jeonse = dict(rows_by.get('전세가율') or [])
    sale = dict(rows_by.get('매매가격지수') or [])
    out = {}
    for gu in WATCHED_GU:
        j = _val3(jeonse[gu]) if gu in jeonse else None
        sv = _val3(sale[gu]) if gu in sale else None
        if j or sv:
            out[gu] = (j, sv)
    return out


def _sub_gu_line(gu, market):
    """「이 구 전세가율 43.0% · 매매가격지수 100.57 (석 달 +2.40pt) · 기준
    2026-07」 — 보고 있는(WATCHED_GU) 구에만 낸다. 색·계산은 기존 헬퍼
    (_delta_num·_val3) 그대로 재사용한다."""
    e = (market or {}).get(gu)
    if not e:
        return ''
    j, sv = e
    parts = []
    asof = None
    if j:
        parts.append('전세가율 %.1f%%' % j['cur'])
        asof = j.get('asof')
    if sv:
        parts.append('매매가격지수 %.2f (석 달 %s)' % (sv['cur'], _delta_num(sv['d3'], 'pt')))
        asof = sv.get('asof') or asof
    if not parts:
        return ''
    return ('<p class="si-gu-mkt mono">이 구 %s · 기준 %s</p>'
           % (' · '.join(parts), E(asof or '—')))


def _sub_verdict(items, today):
    """물음 ① 「지금 접수 중인 게 있나」의 답 한 문장. 새 페이지 verdict·「접수 중」
    절 빈 문구·본 장 「청약」 절의 없음 대체 문구 셋이 이 한 함수를 쓴다."""
    n_open = sum(1 for it in items if _sub_status(it, today) == '접수 중')
    if n_open:
        return '지금 접수 중인 공고가 %d건 있습니다' % n_open
    upcoming = sorted((it for it in items if _sub_status(it, today) == '접수 예정'),
                      key=lambda it: it.get('apply') or '')
    if upcoming:
        nx = upcoming[0]
        return '지금 접수 중인 공고가 없습니다 · 다음 접수 %s %s' % (nx.get('apply') or '',
                                                       nx.get('name') or '')
    return '지금 접수 중인 공고가 없습니다 · 예정된 공고도 아직 없습니다'


def _sub_name_html(it, full):
    """단지명 — 청약공고_스펙 추가 §2. 페이지 안(full=True)이면 그 건 자신의
    앵커(#p-<id>)로, 본 장 축약(full=False)이면 새 페이지의 그 앵커로 건다.
    청약홈 실제 링크는 여기서 안 쓴다 — 그 건 안 「청약홈에서 보기 →」에만 쓴다."""
    name = E(it.get('name') or '')
    pid = it.get('id')
    if pid:
        href = ('#p-%s' % E(pid)) if full else ('watch/청약 공고.html#p-%s' % E(pid))
        return '<a class="si-name" href="%s">%s</a>' % (href, name)
    return '<span class="si-name">%s</span>' % name


def _sub_links_html(it):
    """셋째 줄 오른쪽 — 분양 홈페이지(있으면)·청약홈. 값이 없으면 그 링크는 안
    낸다(자리표시 금지)."""
    links = []
    if it.get('hmpg'):
        links.append('<a class="si-go" href="%s" target="_blank" rel="noopener">분양 홈페이지 →</a>'
                     % E(it['hmpg']))
    if it.get('url'):
        links.append('<a class="si-go" href="%s" target="_blank" rel="noopener">청약홈에서 보기 →</a>'
                     % E(it['url']))
    return ''.join(links)


def _sub_item_html(it, today, full=False, market=None):
    """공고 한 건. full=True(새 페이지)면 셋째 줄(경쟁률·링크)도 낸다 — 본 장 축약
    절은 이름 자체가 링크라 둘째 줄까지만 낸다. 칩 클래스는 늘 si-chip 을 덧붙인다
    — 「tag t-near」만 단독으로 나가면 옛 조건 트리거 UI 자국 검사(_COND_CHROME)와
    글자 그대로 겹친다(이 칩은 그 기능과 무관한 새 기능이다).

    id="p-<HOUSE_MANAGE_NO>" 를 건마다 붙인다(청약공고_스펙 추가 §2) — 지도
    구 패널·본 장 3건이 여기로 앵커를 건다. 「주택형」줄(추가 §1)은 둘째 줄
    다음, 「그 구의 시세」줄(추가 §3)은 셋째 줄 앞에 선다."""
    st = _sub_status(it, today)
    cls = _SUB_STATUS_CLS.get(st, 't-none')
    pid = it.get('id')
    id_attr = ' id="p-%s"' % E(pid) if pid else ''
    h = ['<div class="sub-item"%s><p class="si-1">%s <span class="si-gu">%s</span> '
         '<span class="tag %s si-chip">%s</span></p>'
         % (id_attr, _sub_name_html(it, full), E(it.get('gu') or ''), cls, E(st))]
    if it.get('builder'):
        h.append('<p class="si-b">%s</p>' % E(it['builder']))
    h.append('<p class="si-2 mono">%s</p>' % _sub_line2(it))
    h.append(_sub_types_html(it, full))
    h.append(_sub_gu_line(it.get('gu') or '', market))
    if full:
        rate = ('<span class="si-rate">1순위 경쟁률 %s:1</span>' % E(it['rate1'])
               if it.get('rate1') else '')
        links = _sub_links_html(it)
        if rate or links:
            h.append('<p class="si-3">%s%s</p>' % (rate, links))
    h.append('</div>')
    return ''.join(h)


def _sub_bin(n):
    """구별 6개월 청약 공고 건수 → 지도 층 칸. 0건은 채우지 않는다(--paper+--line
    기본값과 같다 — 값 없는 구와 시각적으로 안 겹치려면 옅은 회색 하나로 뭉치면
    안 되니 색을 아예 안 칠한다)."""
    if not n:
        return None
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n <= 4:
        return 3
    return 4


def _val3(series):
    """지금 값 · 지난달 대비 · 석 달 대비. 견준 상대의 달(a1·a3)도 같이 낸다 —
    「+0.20%p」만 적으면 그게 한 달치인지 석 달치인지 화면에 없다."""
    ser = [tuple(x) for x in series]
    return {'cur': ser[-1][1], 'd1': _delta(ser, 1), 'd3': _delta(ser, 3),
            'asof': ser[-1][0],
            'a1': ser[-2][0] if len(ser) >= 2 else None,
            'a3': ser[-4][0] if len(ser) >= 4 else None}


def _gu_map_data(watches):
    """구 25개마다 지도·패널이 쓰는 값을 한 자리에 — movement 계산(_movement_rows)을
    그대로 재사용한다. 「지난번 본 뒤 바뀐 것」 절은 없어졌지만 그 계산은 패널이
    그대로 쓴다(2026-09-03)."""
    rows_by = _movement_rows(watches)
    jeonse = dict(rows_by.get('전세가율') or [])
    sale = dict(rows_by.get('매매가격지수') or [])
    idx = _idx_rows(watches)
    region_raw = _region_raw(watches)
    region_slug = dict((w['target'], w['slug']) for w in _live_areas(watches))
    region_view = dict((w['target'], w.get('view') or '') for w in _live_areas(watches))
    sub_gu, sub_asof = _sub_gu_data(watches)
    out = {}
    for name in sorted(SEOUL_GU['gu']):
        region = GU_REGION.get(name)
        entry = {'region': region, 'slug': region_slug.get(region),
                 'region_view': region_view.get(region) or ''}
        entry['jeonse'] = _val3(jeonse[name]) if name in jeonse else None
        entry['sale'] = _val3(sale[name]) if name in sale else None
        # 전세가격지수 — 매매가격지수와 같은 단위라 나란히 놓아야 전세가율이
        # 왜 움직였는지가 갈린다(전세가 빠졌나, 매매가 올랐나)
        ji = (idx.get(name) or {}).get('jeonse')
        entry['jeonse_idx'] = _val3(ji) if ji else None
        si = (idx.get(name) or {}).get('sale')
        entry['gap'] = (_delta(si, 3) if si else None, _delta(ji, 3) if ji else None)
        sd = (region_raw.get(region) or {}).get('supply_demand') if region else None
        entry['sd'] = ({'value': sd.get('value'), 'area': sd.get('area')} if sd else None)
        entry['lth_value'], entry['lth_detail'] = _lth_info(name)
        entry['adj'], entry['hot'] = _reg_info(name)
        # 청약홈 최근 공고 — 구 25개 전부(권역 무관). 어댑터가 못 냈으면(열쇠 없음)
        # None, 받았으면 그 구가 0건이어도 {'value':0,…} — 「못 봤다」와 「0건이다」는
        # 다른 상태다
        if sub_gu is not None:
            items = sub_gu.get(name) or []
            entry['sub_cnt'] = {'value': len(items), 'as_of': sub_asof}
            entry['sub_items'] = items
        else:
            entry['sub_cnt'] = None
            entry['sub_items'] = []
        out[name] = entry
    return out


# 구글 폰트 — 본문은 IBM Plex Sans KR, 날짜·기준 표기는 IBM Plex Mono. preconnect
# 둘을 먼저 걸고 스타일시트를 문다(display=swap 은 URL 파라미터로 이미 걸려 있다).
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+KR:wght@400;500;600;700'
         '&display=swap">')

# 색은 이름과 값 둘로만 쓴다. 상태(걸림·근접)는 --ink·--near — 「지금 어떤가」.
# 방향(석 달 전 대비 오름·내림)만 --up·--down — 「어디로 가나」. 둘을 섞으면 걸린
# 줄과 오르는 줄이 같은 색으로 보여 화면이 알록달록해지고 정작 걸린 줄이 안 튄다.
# 한국 시세 관례대로 오름은 빨강(--up), 내림은 파랑(--down)이다 — 증시 관례와
# 반대라 헷갈리기 쉽지만 부동산 기사가 쓰는 색이 이거다.
CSS = """
:root{
  --paper:#F3F5F7; --surface:#FFFFFF;
  --ink:#101418; --ink-2:#4A5560; --ink-3:#7C8791;
  --line:#DDE2E7;
  --up:#D6412B; --down:#2B63D6; --near:#C9931A;
  --fig-blue:#4A5560; --fig-good:#D6412B; --warn:#C9931A;
  /* 지도 전세가율 층 — 순차 램프 다섯 단(<45·45~50·50~55·55~60·≥60) */
  --seq-1:#D9EFE8; --seq-2:#9FD6C5; --seq-3:#5FB59D; --seq-4:#2E8C74; --seq-5:#175E4C;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0F1418; --surface:#171D22;
  --ink:#E9EDF0; --ink-2:#AAB4BC; --ink-3:#7C8791;
  --line:#263038;
  --up:#E0704A; --down:#5C8CE0; --near:#D9AA4A;
  --fig-blue:#AAB4BC; --fig-good:#E0704A; --warn:#D9AA4A;
  /* 다크에서도 「값이 클수록 밝다」 방향을 라이트와 같게 둔다 — 뒤집으면 같은 색이
     두 화면에서 반대 뜻이 된다(스크린샷을 주고받는 순간 오독이다). 맨 아래 단도
     --surface 보다 충분히 밝게 잡아 「값 없음」과 안 헷갈리게 한다 */
  --seq-1:#2A5F4E; --seq-2:#3E8570; --seq-3:#55A98F; --seq-4:#7ECBAF; --seq-5:#ADE4CC;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 15px/1.65 "IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  font-variant-numeric:tabular-nums}
.mono{font-family:"IBM Plex Mono","IBM Plex Sans KR",monospace}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
a:hover{border-bottom-color:var(--ink)}
a:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--down);outline-offset:2px}
/* 지도 구는 테두리 상자 대신 강조 채움(gu-hover)으로 초점을 보인다 — 누른 구 둘레에
   검은 네모가 떴다(2026-09-04 성남 판에서 두드러졌다) */
.seoul-map .gu:focus,.seoul-map .gu:focus-visible{outline:none}
.wrap{max-width:960px;margin:0 auto;padding:0 20px 80px}
header{padding:34px 0 0}
.h-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:6px 16px}
h1{font-size:22px;font-weight:700;letter-spacing:-.01em;margin:0}
.meta{font-size:12.5px;font-weight:500;color:var(--ink-3);margin:0}
.lede{color:var(--ink-2);font-size:.95rem;max-width:66ch;margin:14px 0 0}
/* 절 바로가기 — 스크롤해도 붙어 있다. 지금 어느 절인지는 IntersectionObserver 가
   .is-here 로 표시한다(층 버튼의 is-on 과 같은 꼴이라 새 시각 언어를 안 만든다) */
.jump{position:sticky;top:0;z-index:5;display:flex;gap:6px;overflow-x:auto;
  white-space:nowrap;margin:16px 0 0;padding:10px 0;background:var(--paper);
  border-bottom:1px solid var(--line);scrollbar-width:none}
.jump::-webkit-scrollbar{display:none}
.band[id],.hero[id],section[id]{scroll-margin-top:64px}
.jump a{flex:0 0 auto;font-size:12.5px;font-weight:500;background:var(--surface);
  border:1px solid var(--line);border-radius:999px;padding:6px 12px}
.jump a:hover{border-color:var(--ink-3)}
.jump a.is-here{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.back{display:inline-block;margin:22px 0 0;font-size:.82rem;font-weight:600;
  color:var(--ink-3);border-bottom:0}
.back:hover,.back:focus-visible{color:var(--ink)}
.dbody{margin:26px 0 0}
/* 판정 — 카드·상세 머리에 한 마디로 서는 지금 판단 */
.verdict{font-size:17px;font-weight:600;margin:8px 0 0;color:var(--ink)}
/* 머리 수치 띠 — 부동산 줄 상세에서 산문보다 먼저 서는 지금 값 */
.stats{display:flex;flex-wrap:wrap;gap:20px;margin:16px 0 0}
.stat{flex:1 1 150px;min-width:130px}
.stat-k{font-size:12.5px;color:var(--ink-3);margin:0}
.stat-v{font-size:34px;font-weight:700;margin:4px 0 0;line-height:1.1}
.stat-d{margin:2px 0 0;font-size:15px;font-weight:600;white-space:nowrap}
.stat-m{font-size:12.5px;color:var(--ink-3);margin:8px 0 0}
.delta{font-size:15px;font-weight:600;margin-left:6px}
.d-up{color:var(--up)}
.d-down{color:var(--down)}
/* 절 — 대문자·자간 라벨을 걷고 문장형 제목으로 */
.hero{margin:28px 0 0}
/* 최상위 탭 서울|경기 — 눌린 쪽만 먹으로. 절 바로가기(.jump)보다 위, sticky 아님 */
.sido-tabs{display:flex;gap:8px;margin:18px 0 0}
.sido-tab{flex:0 0 auto;font-size:15px;font-weight:700;padding:8px 18px;border-radius:999px;
  border:1px solid var(--line);background:var(--surface);color:var(--ink-2);cursor:pointer}
.sido-tab.is-on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.sido-block{margin:0}
.seoul-map{margin:0 auto}
.hero-t{font-size:15px;font-weight:600;margin:0}
/* 서울 지도 히어로 — 지도가 첫 화면이고 정보는 지도에서 나온다(2026-09-03) */
/* 층 버튼 — 구마다 갈리는 값만 층으로 그린다. 25구가 전부 같은 범주인 것(토허·
   규제)은 지도가 아니라 아래 배너 문장이다 */
.layer-btns{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
.layer-btn{font-size:12.5px;font-weight:600;padding:7px 14px;border-radius:999px;
  border:1px solid var(--line);background:var(--surface);color:var(--ink-2);cursor:pointer}
.layer-btn.is-on{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.maprow{display:flex;gap:24px;margin:14px 0 0;align-items:flex-start}
/* 지도는 늘 손닿는 곳에 — 패널이 길어져 스크롤해도 지도는 제자리(2026-09-03,
   사용자 P0: 「스크롤 내리다 보면 다른 지역은 선택도 못 하네」). top 은 절
   바로가기 줄(.jump, sticky top:0) 의 실측 높이(~54px) + 여백 8px */
@media (min-width:621px){.map-fig{position:sticky;top:62px}}
/* 왼쪽 칸 — 지도 그림은 이 칸의 위쪽 절반만 쓴다. 남는 아래를 상태 배너와
   「달라진 것」이 채운다(빈 칸을 300px 넘게 두지 않는다) */
.mapcol{flex:0 0 58%;min-width:0}
.map-fig{margin:0;min-width:0}
.mappanel{flex:1;min-width:0}
.seoul-map{width:100%;height:auto;display:block}
/* 값 없는 구는 「칠하지 않은 칸」 — 종이색 면에 선만. 흰 면(--surface)으로 두면
   바탕과 1.06:1 이라 서북부가 통째로 무형 덩어리가 된다. 값 있는 구의 경계선은
   거꾸로 흰 실선이라야 색 면 위에서 뜬다 */
.seoul-map .gu{fill:var(--paper);stroke:var(--line);stroke-width:var(--gu-stroke,1px);cursor:default}
.seoul-map .gu[data-slug]{cursor:pointer}
/* 성남 3구 — 서울 밖이라는 것을 옅은 점선 테두리로만 표시한다. 채움 층은 다른 구와
   똑같이 값을 따른다 — 성남만 다른 색으로 묶으면 「지금 값이 다르다」는 뜻으로
   읽힌다(여기서 말하려는 건 시·도 경계일 뿐이다) */
.seoul-map .gu[data-sido="경기"]{stroke-dasharray:2.5 2}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin]{stroke:var(--surface);stroke-width:1.5px}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin="1"]{fill:var(--seq-1)}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin="2"]{fill:var(--seq-2)}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin="3"]{fill:var(--seq-3)}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin="4"]{fill:var(--seq-4)}
.seoul-map[data-layer="ratio"] .gu[data-ratio-bin="5"]{fill:var(--seq-5)}
/* 분양가상한제 층 — 넷과 스물하나로 갈린다. 적용만 색을 얹고 나머지는 빈 칸이다
   (서울 전체를 먹 단색으로 안 칠한다 — 그래서 토허·규제 층을 걷었었다) */
.seoul-map[data-layer="cap"] .gu[data-cap="yes"]{fill:var(--seq-4);
  stroke:var(--surface);stroke-width:1.5px}
.seoul-map[data-layer="cap"] .gu[data-cap="null"]{fill:url(#hatch-line)}
/* 청약 공고 층 — 구별 6개월 건수 다섯 단(0·1·2·3~4·5+). 0건은 채우지 않는다
   (--paper+--line 기본값) */
.seoul-map[data-layer="sub"] .gu[data-sub-bin]{stroke:var(--surface);stroke-width:1.5px}
.seoul-map[data-layer="sub"] .gu[data-sub-bin="1"]{fill:var(--seq-2)}
.seoul-map[data-layer="sub"] .gu[data-sub-bin="2"]{fill:var(--seq-3)}
.seoul-map[data-layer="sub"] .gu[data-sub-bin="3"]{fill:var(--seq-4)}
.seoul-map[data-layer="sub"] .gu[data-sub-bin="4"]{fill:var(--seq-5)}
.seoul-map .gu.gu-hover{stroke:var(--ink);stroke-width:2.5px}
.seoul-map .gu.gu-dim{opacity:.55}
.gu-lbl{font-weight:600;fill:var(--ink);paint-order:stroke;
  stroke:var(--paper);stroke-width:3px;pointer-events:none}
/* 값 없는 구도 이름을 단다 — 「내가 사는 데 찾기」가 지도의 첫 동작이다. 위계는
   크기·굵기·색으로 준다 */
.gu-lbl.blank{font-size:10px;font-weight:400;fill:var(--ink-3)}
@media (prefers-reduced-motion:no-preference){.seoul-map .gu{transition:fill .15s}}
/* 패널 — 기본(권역 요약 셋)과 구 25개짜리를 data-panel 로 JS 가 바꿔 낀다.
   값은 전부 생성 때 박아 둔다 — JS 는 hidden 만 만진다(계산 안 한다).
   [hidden] 을 여기서 다시 못 박는다 — 저자 스타일시트의 .gu-panel{display:block}
   이 명시도(둘 다 (0,1,0))가 같은 UA 기본 규칙([hidden]{display:none})을 저자
   출처라는 이유만으로 이긴다. 실제로 그렇게 나가 구 25개가 패널 아래 전부
   펼쳐져 보였다(2026-09-03, 스크린샷으로 잡힘) — !important 로 확실히 막는다. */
[hidden]{display:none!important}
/* flex column — 켜진 층에 맞는 덩이를 order 로 맨 위(머리 다음)에 올리려면 flex
   컨테이너라야 한다(2026-09-04, 사용자 스크린샷: 「청약 공고」 층을 켜고 구를
   눌렀는데 전세가율부터 나오고 정작 공고는 아래로 잘렸다). 순서는 아래 세 켜로 –
   머리(-3)·부제(-2)는 늘 고정, 그 아래 「이 층의 덩이」만 -1 로 올라온다. 전세가율
   층(기본)은 그 덩이에 order 를 안 줘서 지금 문서 순서 그대로 첫 자리에 남는다 */
.gu-panel{display:flex;flex-direction:column}
.mappanel[data-layer="cap"] .gp-cap{order:-1}
.mappanel[data-layer="sub"] .gp-pblanc{order:-1}
/* 구 패널은 권역 요약 셋을 덮지 않고 그 위에 얹힌다 — 요약 셋이 화면에 남아야
   「어느 권역이 나은가」를 견줄 수 있다(그게 이 절이 답하는 물음이다) */
@media (min-width:621px){
  .gu-panel:not([data-panel="default"]){background:var(--surface);
    border:1px solid var(--line);border-radius:10px;padding:16px;margin:0 0 16px;
    box-shadow:0 2px 12px rgba(16,20,24,.10)}
}
/* 권역 요약 행 — 링크라는 것이 보여야 한다. 밑줄만으로는 행 구분선과 구분이 안 된다 */
.rs{display:block;position:relative;padding:9px 26px 9px 0;
  border-bottom:1px solid var(--line)}
.rs:last-child{border-bottom:0}
.rs::after{content:"→";position:absolute;right:2px;top:14px;color:var(--ink-3);font-weight:600}
.rs:hover{background:var(--surface);margin:0 -12px;padding-left:12px;padding-right:38px;
  border-radius:8px}
.rs:hover::after{color:var(--ink)}
.rs-k{margin:0;font-size:12.5px;color:var(--ink-3)}
.rs-v{margin:4px 0 0;font-weight:600;font-size:.92rem;color:var(--ink)}
.rs-n{margin:2px 0 0;font-size:23px;font-weight:700}
.rs-line{margin:3px 0 0;font-size:12.5px;color:var(--ink-2)}
.rs-cta{display:inline-block;margin:6px 0 0;font-size:12.5px;font-weight:600;color:var(--ink-2)}
.gp-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin:0;order:-3}
.gp-name{font-size:20px;font-weight:700}
.gp-close{flex:0 0 auto;width:32px;height:32px;min-width:44px;min-height:44px;margin:-6px -6px 0 0;
  border:0;background:transparent;color:var(--ink-3);font-size:20px;line-height:1;cursor:pointer;
  display:flex;align-items:center;justify-content:center;border-radius:999px}
.gp-close:hover{background:var(--line);color:var(--ink)}
.gp-sub{margin:2px 0 0;font-size:12.5px;color:var(--ink-3);order:-2}
/* 뜻 한 줄 — 수 세 줄보다 먼저 읽힌다 */
.gp-mean{font-size:14.5px;font-weight:600;color:var(--ink);margin:8px 0 10px;line-height:1.5}
/* 값 줄 — 라벨(왼쪽 정렬 12.5px ink-3) 바로 뒤 같은 줄에 값. 두 열로 안 가른다 —
   폰 폭에서 두 열이면 값이 잘린다(2026-09-03) */
.gp-row{margin:8px 0 0;font-size:.85rem;line-height:1.5;color:var(--ink-2)}
/* 최근 공고 줄 아래 단지 목록 — 「최근 공고 n건」에 딸린 것임을 왼쪽 선으로 보인다 */
.gp-sub-item{margin:4px 0 0;padding-left:10px;border-left:2px solid var(--line);
  font-size:.8rem}
.gp-lbl{color:var(--ink-3);font-size:12.5px;margin-right:4px}
.gp-d{color:var(--ink-2)}
.gp-more{display:block;margin:12px 0 0;padding:10px 0 0;font-weight:600;font-size:.95rem;
  border-bottom:0;border-top:1px solid var(--line)}
/* 청약 공고 상태 칩 — 구 패널 단지 줄 끝. 값 줄이 좁아 칩이 커지면 안 되므로
   이 자리에서만 작게 줄인다(청약공고_스펙 §5) */
.gp-chip{font-size:11px;padding:1px 6px;margin-left:6px;vertical-align:1px}
/* 모바일 — 구를 고르면 아래에서 시트가 올라온다. 기본(권역 요약 셋)은 그대로
   지도 아래 인라인이다(:not([data-panel="default"]) 로 가른다) */
@media (max-width:620px){
  .gu-panel:not([data-panel="default"]){
    display:flex!important;flex-direction:column;position:fixed;left:0;right:0;bottom:0;
    max-height:45vh;overflow-y:auto;background:var(--surface);border-top:1px solid var(--line);
    border-radius:14px 14px 0 0;z-index:20;
    padding:14px 16px 20px;transform:translateY(100%);pointer-events:none;visibility:hidden}
  /* 그림자는 열렸을 때만. 숨은 시트에도 두면 위로 번진 그림자가 화면 밑에 검은 띠로
     남는다(2026-09-03, 사용자 스크린샷) */
  .gu-panel:not([data-panel="default"])::before{
    content:"";display:block;width:36px;height:4px;border-radius:2px;
    background:var(--line);margin:0 0 10px}
  .gu-panel:not([data-panel="default"]):not([hidden]){
    transform:translateY(0);pointer-events:auto;visibility:visible;
    box-shadow:0 -8px 24px rgba(0,0,0,.12)}
  @media (prefers-reduced-motion:no-preference){
    .gu-panel:not([data-panel="default"]){transition:transform .18s}
  }
}
/* 범례 — 전세가율 하나뿐이다(지정 현황 둘은 지도에서 내려 배너로 갔다) */
.map-legend{margin:16px 0 0;padding:14px 0 0;border-top:1px solid var(--line)}
.leg-strip{display:flex}
.leg-strip .leg-sw{flex:1;height:16px;border-radius:0;margin:0}
.leg-strip .leg-sw:first-child{border-radius:3px 0 0 3px}
.leg-strip .leg-sw:last-child{border-radius:0 3px 3px 0}
.leg-labels{display:flex;margin:4px 0 0;font-size:11px;color:var(--ink-3)}
.leg-labels span{flex:1;text-align:center}
.leg-item{margin:8px 0 0;font-size:.85rem;color:var(--ink-2)}
.leg-sw{display:inline-block;width:16px;height:16px;border-radius:3px;
  vertical-align:middle;margin-right:6px}
.leg-hatch-ink{background-image:repeating-linear-gradient(45deg,var(--ink) 0 2px,var(--surface) 2px 6px)}
.leg-hatch-line{background-image:repeating-linear-gradient(45deg,var(--line) 0 2px,var(--surface) 2px 6px)}
.leg-src{margin:10px 0 0;font-size:12.5px;color:var(--ink-3)}
/* 지정 현황 상태 배너 — 층 버튼을 대신한다. 25구가 전부 같은 값이라 지도로 그리면
   서울 전체가 먹 단색이 되고, 얻는 정보는 문장 하나다 */
.zone-banner{margin:14px 0 0;padding:12px 0 0;border-top:1px solid var(--line)}
.zb-row{display:flex;flex-wrap:wrap;gap:3px 10px;align-items:baseline;padding:5px 0;
  font-size:.88rem}
.zb-k{flex:0 0 auto;font-weight:600}
.zb-v{color:var(--ink-2)}
.zb-m{font-size:12.5px;color:var(--ink-3)}
/* 여섯 달 넘게 안 바뀐 값에는 나이를 붙인다 — 머리의 「자료 기준 2026-07」과 같은
   무게로 읽히면 안 된다 */
.t-old{display:inline-block;font-size:12px;font-weight:600;padding:1px 7px;
  border-radius:4px;border:1px solid var(--near);color:var(--near)}
/* 지난달과 달라진 것 — 이 장을 다시 여는 이유가 이것이다 */
.changed{margin:24px 0 0;padding:14px 0 0;border-top:1px solid var(--line)}
.chg-t{font-size:15px;font-weight:600;margin:0}
.chg-row{display:flex;flex-wrap:wrap;gap:2px 12px;align-items:baseline;padding:8px 0;
  border-bottom:1px solid var(--line)}
.chg-row:last-child{border-bottom:0}
.chg-k{flex:0 0 auto;font-weight:600;font-size:.9rem}
.chg-v{font-size:.9rem;color:var(--ink-2)}
.chg-say{font-size:.85rem;color:var(--ink-3)}
/* 둘째 줄 — 전세가율만 보면 전세가 빠진 건지 매매가 오른 건지 모른다 */
.chg-2{flex:0 0 100%;font-size:.85rem;color:var(--ink-2);margin:3px 0 0}
/* 절 제목 옆 잔글씨 — 열마다 되풀이되는 상수(마지막 확인 날짜)를 한 번만 적는다 */
.band-note{margin-left:8px;font-size:12.5px;font-weight:400;color:var(--ink-3)}
/* 청약 — 조건 표 셋. 표 제목은 절 제목과 같은 무게(15px 600)로, 「근거」 칸은
   잔글씨로 내린다 — 조문 번호가 조건과 같은 크기로 서면 무엇이 답인지 흐려진다 */
.cond-t{font-size:15px;font-weight:600;margin:22px 0 0}
.cond-lead{font-size:.9rem;color:var(--ink-2);margin:6px 0 0;max-width:66ch}
.cond-tail{font-size:12.5px;color:var(--ink-3);margin:8px 0 0;max-width:66ch}
.t-why{font-size:12.5px;color:var(--ink-3)}
/* 청약 공고 한 건 — 본 장 「지금 청약」 축약과 watch/청약 공고.html 이 함께 쓴다
   (청약공고_스펙 §4). 표가 아니라 목록이다 — 값 여덟을 열로 두면 모바일에서
   가로로 밀린다 */
.sub-list{margin:12px 0 0}
.sub-title{padding:8px 0;border-bottom:1px solid var(--line)}
.sub-title:last-child{border-bottom:0}
.st-1{display:flex;justify-content:space-between;align-items:baseline;gap:8px;margin:0;font-weight:600}
.st-1 a{min-width:0}
.st-r{flex:0 0 auto;white-space:nowrap;font-weight:400}
.st-2{margin:2px 0 0;font-size:12.5px}
/* 정비사업 — 구 한 줄(이름·곳수)과 그 밑 사업장 셋 */
.rb-row{padding:12px 0;border-bottom:1px solid var(--line)}
.rb-row:last-of-type{border-bottom:0}
.rb-k{margin:0;font-size:15px;font-weight:700}
.rb-k a{color:inherit;text-decoration:none}
.rb-k a:hover{text-decoration:underline}
.rb-n{font-weight:600;color:var(--ink-2);font-size:13px;margin-left:6px}
.rb-v{margin:3px 0 0;font-size:13px;color:var(--ink-2)}
.rb-item{padding:6px 0 0}
.rb-item .si-1{font-size:14px}
.sub-item{padding:12px 0;border-bottom:1px solid var(--line);scroll-margin-top:64px}
.sub-item:last-child{border-bottom:0}
/* 공고를 누르면 그 공고가 맨 위로 — :target 강조(청약공고_스펙 추가 §2).
   레이아웃을 안 밀려고 왼쪽 선은 inset box-shadow 로 그린다 */
.sub-item:target{background:var(--surface);box-shadow:inset 3px 0 0 var(--ink);padding-left:9px}
.si-1{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:0}
.si-name{font-weight:700;font-size:1rem;border-bottom:0}
.si-name:hover{border-bottom:1px solid var(--ink)}
.si-gu{font-size:12.5px;color:var(--ink-3)}
.si-chip{margin-left:auto}
.si-b{margin:2px 0 0;font-size:12.5px;color:var(--ink-3)}
.si-2{margin:4px 0 0;font-size:.85rem;color:var(--ink-2);line-height:1.5}
/* 주택형 줄(추가 §1)·그 구의 시세 줄(추가 §3) — si-2 와 같은 잔글씨 무게 */
.si-ty,.si-gu-mkt{margin:4px 0 0;font-size:.85rem;color:var(--ink-2);line-height:1.5}
.si-3{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;
  margin:4px 0 0;font-size:.85rem}
.si-rate{color:var(--ink-2);font-weight:600}
.si-go{font-weight:600;color:var(--ink-2);border-bottom:0}
.si-go:hover{color:var(--ink)}
.si-go+.si-go{margin-left:10px}
@media (max-width:620px){.si-1{gap:2px 8px}.si-gu{flex:0 0 100%}}
.band{margin:40px 0 0;border-top:2px solid var(--ink);padding-top:11px}
.band-t{font-size:15px;font-weight:600;margin:0}
.band-s{font-size:.9rem;color:var(--ink-2);margin:6px 0 0;max-width:66ch}
.chip-legend{margin-left:8px;font-size:12.5px;font-weight:400;color:var(--ink-3)}
/* 용어 풀이 — 그 말 옆에 둔다. 별도 절이 아니라 등장한 자리 바로 아래 잔글씨다 */
.term{font-size:12.5px;color:var(--ink-3);margin:4px 0 0;max-width:66ch}
/* 「지난번 본 뒤 바뀐 것」 — 지표별 소제 + 얼마나 움직였나 행. 화살표 색만 방향을
   말한다(상태 색은 안 쓴다 — 문턱을 넘었는지가 아니라 얼마나 움직였는지만 본다) */
.move-h{font-size:15px;font-weight:600;margin:22px 0 0}
.mv-row{padding:9px 0;border-bottom:1px solid var(--line)}
.mv-row:last-child{border-bottom:0}
.mv-name{margin:0;font-weight:600;font-size:.92rem}
/* flex-wrap 로 편다 — grid 로 열을 나누면 좁은 화면에서 칸이 남거나 겹친다
   (모바일 「보고 있는 것」에서 겪은 버그와 같은 종류라 처음부터 피한다) */
.mv-line{display:flex;flex-wrap:wrap;gap:4px 14px;align-items:baseline;margin:4px 0 0}
.mv-val{font-size:20px;font-weight:600}
.mv-d{font-size:13px;color:var(--ink-2);white-space:nowrap}
.mv-as{font-size:12.5px;color:var(--ink-3);white-space:nowrap}
.rows{margin:14px 0 0}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:2px 14px;align-items:baseline;
  padding:10px 0;border-bottom:1px solid var(--line)}
.row:last-child{border-bottom:0}
.row-where{font-size:.85rem;color:var(--ink-3);display:flex;align-items:baseline;gap:8px}
.row-what{font-weight:700}
.row-num{font-size:20px;font-weight:600;white-space:nowrap}
.row-why{grid-column:2/-1;font-size:13px;color:var(--ink-3)}
/* 칩 — 상태(걸림·근접·풀림·같다)만 표시한다. 걸림은 먹색 칩, 근접은 황토 테두리다 */
.tag{display:inline-block;font-size:12.5px;font-weight:600;padding:2px 8px;
  border-radius:4px;white-space:nowrap}
.t-hit{background:var(--ink);color:var(--paper)}
.t-near{border:1px solid var(--near);color:var(--near)}
.t-clear{border:1px solid var(--line);color:var(--ink-3)}
.t-calm{color:var(--ink-2);padding:0}
.t-none{color:var(--ink-3)}
table{width:100%;border-collapse:collapse;margin:12px 0 0;font-size:.88rem}
th{text-align:left;font-size:12px;font-weight:600;color:var(--ink-3);
  border-bottom:1.5px solid var(--ink);padding:0 12px 7px 0;white-space:nowrap}
td{padding:9px 12px 9px 0;border-bottom:1px solid var(--line);vertical-align:baseline}
td:first-child{font-weight:700}
.tw{overflow-x:auto}
/* 절 제목 아래 잔글씨 라벨 — 10px 자간 라벨을 걷고 12.5px ink-3 로 */
.lbl{font-size:12.5px;font-weight:600;color:var(--ink-3);margin:22px 0 0}
/* 권역 카드 셋 */
.areas{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:16px 0 0}
.area{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:18px}
.area-k{font-size:12.5px;color:var(--ink-3);margin:0}
.area-v{font-size:17px;font-weight:600;margin:6px 0 0}
.area-n{font-size:34px;font-weight:700;margin:8px 0 0;line-height:1.1}
.area-r{font-size:12.5px;color:var(--ink-3);margin:4px 0 0}
.area-d{margin:14px 0 0;padding:12px 0 0;border-top:1px solid var(--line)}
.area-row{display:flex;justify-content:space-between;gap:10px;font-size:13px;margin:0 0 6px}
.area-row span:first-child{color:var(--ink-3)}
.area-row span:last-child{font-weight:500;text-align:right}
.area-c{margin:12px 0 0}
.area-more{display:inline-block;margin:12px 0 0;font-size:.82rem;font-weight:600;border-bottom:0}
.area-more:hover,.area-more:focus-visible{color:var(--ink-2)}
.t-sub{color:var(--ink-3);font-size:.92em}
/* 보고 있는 것 목록 — 이름·판정 왼쪽, 칩·마지막 확인 오른쪽 */
.wline{display:grid;grid-template-columns:1fr auto;column-gap:12px;row-gap:3px;
  padding:12px 0;border-bottom:1px solid var(--line);align-items:start}
.wline:last-child{border-bottom:0}
.wline-t{grid-column:1;grid-row:1;font-weight:600;font-size:1rem;border-bottom:0}
.wline-chip{grid-column:2;grid-row:1;justify-self:end;white-space:nowrap}
.wline-v{grid-column:1;grid-row:2;margin:0;font-size:.88rem;color:var(--ink-2)}
.wline-d{grid-column:2;grid-row:2;justify-self:end;font-size:12.5px;color:var(--ink-3)}
figure{margin:9px 0 0}
figure svg{width:100%;height:auto;display:block}
/* 도해는 넓은 판·좁은 판 둘을 싣고 화면 폭으로 하나만 보인다. 줄여 그리면 글자가
   7px 이 되고 최소폭을 두면 오른쪽 끝(제일 최근 달)이 화면 밖으로 나간다 */
svg.fig-n{display:none}
figcaption{font-size:.8rem;color:var(--ink-3);margin:6px 0 0}
.t-sm{font-size:13px;fill:var(--ink-2)}
.t-axis{fill:var(--ink-3)}
.grid{stroke:var(--line);stroke-width:1;fill:none}
footer{margin:60px 0 0;padding-top:16px;border-top:2px solid var(--ink);
  font-size:.8rem;color:var(--ink-3)}
code{font-size:.85em;background:var(--surface);padding:1px 5px;border-radius:2px}
/* ── 좁은 화면 ────────────────────────────────────────────────────────────
   표를 가로로 밀게 두지 않는다. 열 이름을 값 앞에 세워 세로로 편다 —
   7열짜리를 손가락으로 미는 화면에서는 값을 견줄 수가 없다.
   도해는 세로로 못 편다(가로축이 시간이다). 대신 최소 폭을 두고 그 판만 민다. */
@media (max-width:620px){
  body{font-size:16px}
  .wrap{padding:0 14px 60px}
  .h-top{flex-direction:column;align-items:flex-start;gap:4px}
  /* 3열을 유지한다 — 세로로 쌓으면 「43.0% ↓0.1」한 줄을 보자고 스크롤 셋을 만든다.
     390px 에서 한 열 ~115px 이면 이 글자가 그대로 든다(수 26px·화살표 13px로 줄인다) */
  /* 좁은 화면은 열 셋이 아니라 줄 셋 — 이름 · 값 · 변화. 글자를 키운 폰에서 3열은
     변화가 옆 열로 넘쳤다 */
  .stats{display:block;margin-top:12px}
  .stat{display:grid;grid-template-columns:5.5em 1fr auto;align-items:baseline;gap:10px;
    padding:7px 0;border-bottom:1px solid var(--line)}
  .stat:last-child{border-bottom:0}
  .stat-k,.stat-v,.stat-d{margin:0}
  .stat-v{font-size:24px}
  .stat-d{font-size:14px}
  .delta{font-size:13px}
  /* 지도 히어로 — 층 버튼 줄 → 지도 → 패널 순으로 세로 편다 */
  .layer-btns{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}
  .layer-btns::-webkit-scrollbar{display:none}
  .maprow{flex-direction:column}
  .mapcol{flex:0 0 auto;width:100%}
  /* viewBox 안이라 SVG 좌표계 기준으로 올려야 화면에서 13px 안팎으로 보인다 */
  .gu-lbl{font-size:15px;stroke-width:3.5px}
  .gu-lbl.blank{font-size:13px}
  .rs-n{font-size:24px}
  /* 설명을 오른쪽 auto 칸에 두면 그 칸이 긴 문장을 다 먹고 왼쪽 제목이 한 자씩
     세로로 떨어진다(매/매/가/격/지/수). 설명은 제 줄로 내리고 제목은 낱말로 접는다 */
  .row{grid-template-columns:minmax(0,1fr) auto;gap:3px 10px}
  .row-where,.row-why{grid-column:1/-1}
  .row-what{word-break:keep-all;overflow-wrap:anywhere}
  /* grid 를 걷는다 — grid-column 만 1로 바꾸면 grid-row 가 그대로 남아 칩(행1)이
     이름(행1) 위에, 마지막 확인(행2)이 verdict(행2) 위에 겹친다. 자연스러운 문서
     흐름으로 바꿔 1행 이름+칩(같은 줄) · 2행 verdict · 3행 마지막 확인, 세 줄로 편다 */
  .wline{display:block}
  .wline-t{display:inline}
  .wline-chip{display:inline-block;margin-left:8px;vertical-align:middle}
  .wline-v{display:block;margin:4px 0 0}
  .wline-d{display:block;margin:2px 0 0;text-align:left}
  .tw{overflow-x:visible}
  table,thead,tbody,tr,td{display:block;width:100%}
  thead{display:none}
  tr{padding:11px 0;border-bottom:1px solid var(--line)}
  tr:last-child{border-bottom:0}
  td{display:flex;gap:10px;align-items:baseline;border:0;padding:2px 0}
  td::before{content:attr(data-th);flex:0 0 8.5em;font-size:12px;font-weight:600;
    color:var(--ink-3);line-height:1.9}
  td:first-child{font-size:1.02rem;padding-bottom:5px}
  td:first-child::before{display:none}
  svg.fig-w{display:none}
  svg.fig-n{display:block}
  .band{margin-top:32px}
}
"""


def title_of(w):
    return '%s — %s' % (w['target'], w['view']) if w.get('view') else w['target']


def _fmt1(v):
    return ('%.1f' % v)


def _mmdd(d):
    """"YYYY-MM-DD" → "MM-DD". 구 패널 공고 줄은 자리가 좁아 연도까지 못 싣는다 —
    6개월 안 값이라 연도는 오늘과 같거나 하나 차이라 없어도 헷갈리지 않는다."""
    if not d or len(d) < 10:
        return d or '—'
    return d[5:10]


def _extra_sentence(ratio):
    """전세가율의 여집합을 문장으로 잇는다. 43.1 과 57 을 나란히 놓으면 빠르게
    읽는 사람에게 「43인지 57인지」로 남는다 — 둘이 한 짝이라는 것을 말로 적는다."""
    if not ratio:
        return ''
    # 한 줄에 든다. 두 줄짜리로 두면 권역 카드 셋이 데스크톱 첫 화면(900px)을 넘어
    # 셋을 견줄 수가 없다 — 이 절이 답하는 물음이 그 견주기다
    return '전세금이 매매가의 %d%%. %d%%를 더 얹으면 매매입니다.' % (round(ratio),
                                                    round(100.0 - ratio))


def _delta_num(d, unit=''):
    """부호 + 색. 색만으로 방향을 말하지 않는다 — +/− 를 글자로 먼저 쓰고 색을
    겹쳐 준다. 소수는 늘 둘째 자리다(한 화면에서 자릿수가 갈리면 크기 비교가 안 된다)."""
    if d is None:
        return '<span class="t-none">—</span>'
    if abs(d) < 0.005:
        return '<span class="delta">±0.00%s</span>' % E(unit)
    cls = 'd-up' if d > 0 else 'd-down'
    return ('<span class="delta %s">%s%.2f%s</span>'
            % (cls, '+' if d > 0 else '−', abs(d), E(unit)))


_H3_RE = re.compile(r'^###\s+(.+?)\s*$', re.M)


def _md_table(block):
    """마크다운 표에서 (머리, 몸통). watch_lib.table_rows() 는 트리거·이력 표의
    머리만 알아서(그 둘의 첫 칸 이름으로 잰다) 여기서는 못 쓴다 — 조건 표는 머리
    이름이 표마다 다르다."""
    rows = []
    for ln in block.splitlines():
        ln = ln.strip()
        if not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip('|').split('|')]
        if set(''.join(cells)) <= set('-: '):
            continue
        rows.append(cells)
    return (rows[0], rows[1:]) if rows else ([], [])


def cond_blocks(w):
    """「## 조건」 절을 ### 소제목으로 다시 가른다.

    watch_lib.sections() 는 ## 로만 가르니 표 셋이 한 덩어리로 온다. 그 안을
    ### 로 다시 갈라 표마다 (제목, 머리글, 표 머리, 표 몸통, 꼬리글)로 낸다.
    절이 없는 줄은 빈 목록이라 아무것도 안 그려진다 — 정책 줄 여섯 중 청약만
    이 절을 갖는다.

    반환: (절 머리 문장, [(제목, 머리글, head, rows, 꼬리글), …])."""
    p = os.path.join(ROOT, w.get('path') or '')
    if not w.get('path') or not os.path.exists(p):
        return '', []
    with io.open(p, encoding='utf-8') as f:
        _meta, body = wl.nl.parse_front(f.read())
    block = wl.sections(body).get('조건', '')
    if not block:
        return '', []
    hits = list(_H3_RE.finditer(block))
    lead = (block[:hits[0].start()] if hits else block).strip()
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(block)
        seg = block[m.end():end]
        head, rows = _md_table(seg)
        pre, post, seen = [], [], False
        for ln in seg.splitlines():
            t = ln.strip()
            if t.startswith('|'):
                seen = True
            elif t:
                (post if seen else pre).append(t)
        out.append((m.group(1), ' '.join(pre), head, rows, ' '.join(post)))
    return lead, out


def cond_html(w, more=''):
    """조건 표 셋 — 본 장의 「청약 — 조건」 절과 그 줄의 상세가 같은 조각을 쓴다.
    같은 표를 두 자리에서 따로 그리면 한쪽만 고치고 다른 쪽을 잊는다."""
    lead, blocks = cond_blocks(w)
    if not blocks:
        return ''
    h = ['<p class="cond-lead">%s</p>' % wl.md_inline(lead)] if lead else []
    for title, pre, head, rows, post in blocks:
        if not rows:
            continue
        # 「근거」 칸은 잔글씨로 내린다 — 조문 번호가 조건과 같은 무게로 서면
        # 무엇이 답인지 흐려진다
        body = [['<span class="t-why">%s</span>' % wl.md_inline(c)
                 if (i < len(head) and head[i] == '근거') else wl.md_inline(c)
                 for i, c in enumerate(r)] for r in rows]
        h.append('<p class="cond-t">%s</p>' % E(title))
        if pre:
            h.append('<p class="cond-tail">%s</p>' % wl.md_inline(pre))
        h.append(tbl('', head, body))  # noqa: E501 — 제목은 위에서 따로 세웠다
        if post:
            h.append('<p class="cond-tail">%s</p>' % wl.md_inline(post))
    if more:
        h.append(more)
    return ''.join(h)


def _idx_of(w):
    """줄 하나의 구별 매매·전세 가격지수 시계열. w['metrics'](픽업)가 아니라
    insights/watch/_metrics/ 원본을 읽는다 — 실거주 줄의 context 는 지수를 안 걸어서
    (트리거가 전세가율뿐이라) 픽업에는 안 남는다.

    반환: {구: {'sale': series, 'jeonse': series}}. 둘 다 기준월=100 짜리 지수라
    같은 판에 놓고 견줄 수 있다(절대 매매가는 구 단위로 안 나온다 — 서울 전체
    중위가뿐이다)."""
    out = {}
    if w['kind'] != 'realestate':
        return out
    for k, m in wl.metrics_of(w['kind'], w['slug']).items():
        ser = [tuple(x) for x in (m.get('series') or [])]
        area = m.get('area')
        if not ser or not area:
            continue
        if k.startswith('sale_idx_'):
            out.setdefault(area, {}).setdefault('sale', ser)
        elif k.startswith('jeonse_idx_'):
            out.setdefault(area, {}).setdefault('jeonse', ser)
    return out


def _idx_rows(watches):
    """구 전부의 매매·전세 가격지수 — 여러 줄에 흩어진 것을 한 자리로 모은다."""
    out = {}
    for w in watches:
        for gu, d in _idx_of(w).items():
            e = out.setdefault(gu, {})
            for k, ser in d.items():
                e.setdefault(k, ser)
    return out


def _read_gap(ds, dj):
    """매매와 전세 중 무엇이 전세가율을 움직였나.

    전세가율 = 전세 ÷ 매매라, 그 값이 내려가도 전세가 빠진 건지 매매가 오른 건지
    모른다. 두 지수의 같은 기간 변화를 견줘 그 물음에 답한다. 여기 쓰는 0.5pt 는
    문턱이 아니라 「둘이 사실상 같이 갔다」와 「한쪽이 앞섰다」를 가르는 선이다 —
    넘었다고 뭘 하라는 말은 안 한다."""
    if ds is None or dj is None:
        return ''
    d = ds - dj
    if -0.5 < d < 0.5:
        return '매매와 전세가 같이 움직입니다'
    sale_faster = d >= 0.5
    if ds >= 0 and dj >= 0:
        return ('매매가 전세보다 빨리 올라 전세가율이 내려갑니다' if sale_faster
                else '전세가 매매보다 빨리 올라 전세가율이 올라갑니다')
    if ds < 0 and dj < 0:
        return ('전세가 매매보다 빨리 내려 전세가율이 내려갑니다' if sale_faster
                else '매매가 전세보다 빨리 내려 전세가율이 올라갑니다')
    if ds >= 0:
        return '매매는 오르고 전세는 내려 전세가율이 내려갑니다'
    return '전세는 오르고 매매는 내려 전세가율이 올라갑니다'


def _idx_gap_line(pairs, note):
    """「매매 +2.40pt · 전세 +0.95pt (석 달, 지수 · 구 셋 평균)」 + 읽는 말 한 줄.

    pairs 는 (매매 Δ, 전세 Δ). 평균을 낸 경우 note 에 그렇게 적는다 — 우리가 만든
    수라는 표시다(공표치가 아니다)."""
    ds, dj = pairs
    if ds is None or dj is None:
        return ''
    return ('<p class="rs-line">매매 %s · 전세 %s <span class="t-sub">(%s)</span> — %s</p>'
            % (_delta_num(ds, 'pt'), _delta_num(dj, 'pt'), E(note), E(_read_gap(ds, dj))))


def _idx_avg_delta(idx, gus, back=3):
    """구 셋의 석 달 Δ 평균 — 값이 다 있는 구만 센다."""
    out = []
    for key in ('sale', 'jeonse'):
        ds = [_delta(idx[g][key], back) for g in gus
              if g in idx and key in idx[g] and _delta(idx[g][key], back) is not None]
        out.append(sum(ds) / len(ds) if ds else None)
    return tuple(out)


def _delta_when(span, base):
    """기간만 글자로. 값을 큰 글씨 옆에 이미 썼을 때(머리 수치 띠) 쓴다 — 같은 수를
    두 번 적지 않는다."""
    return E('%s(%s) 대비' % (span, base) if base else '%s 대비' % span)


def _delta_phrase(span, base, d, unit=''):
    """「지난달(2026-06) 대비 +0.20%p」 — 본 장 패널·권역 요약·달라진 것·상세
    머리 띠가 전부 이 한 함수를 쓴다. 같은 지표의 변화가 두 화면에서 반대로 보인
    적이 있다(본 장 ↑0.20, 상세 ↓0.1) — 계산과 기간을 한 자리로 모아 막는다."""
    if d is None:
        return ''
    when = '%s(%s) 대비' % (span, base) if base else '%s 대비' % span
    return '%s %s' % (E(when), _delta_num(d, unit))


def _delta_unit(unit):
    """값의 단위 → 변화의 단위. 비율(%)의 변화는 %p, 지수의 변화는 pt 다."""
    return '%p' if '%' in (unit or '') else 'pt'


def tbl(cap, head, rows):
    """표. 칸마다 열 이름을 data-th 로 실어 둔다 — 좁은 화면에서 가로로 미는 대신
    그 이름을 앞에 세워 세로로 편다. 7열짜리를 손가락으로 밀게 두면 값을 못 본다."""
    if not rows:
        return ''
    body = []
    for r in rows:
        cells = ''.join('<td data-th="%s">%s</td>' % (E(head[i]) if i < len(head) else '', c)
                        for i, c in enumerate(r))
        body.append('<tr>%s</tr>' % cells)
    # cap 이 비면 제목 문단을 안 낸다 — 조건 표는 제목을 절 제목 무게(cond-t)로
    # 따로 세우고 그 사이에 보충 문장이 들어간다
    head_p = '<p class="lbl">%s</p>' % E(cap) if cap else ''
    return ('%s<div class="tw"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>'
            % (head_p, ''.join('<th>%s</th>' % E(h) for h in head), ''.join(body)))


def tag(state):
    # 표시 이름만 다듬는다 — watch_lib.state_now()가 돌려주는 내부 값('멂')은
    # 검사기(check_watch)와 다른 함수들이 그대로 비교하므로 여기서는 안 건드린다.
    cls = {'걸림': 't-hit', '근접': 't-near', '같다': 't-calm', '풀림': 't-clear'}.get(state, 't-none')
    label = {'멂': '멀다'}.get(state, state)
    return '<span class="tag %s">%s</span>' % (cls, E(label))


def _months(t):
    m = re.match(r'^(\d{4})-(\d{2})', str(t))
    return int(m.group(1)) * 12 + int(m.group(2)) if m else None


def time_ruler(watches, W=640):
    """자료 기준 자 — 값의 나이를 먼저 보여 준다.

    이 장의 모든 값에 「언제 것」이 붙는다. 그 나이가 곧 내용인데 표 안에 흩어 두면
    법 하나가 2년 전에서 멈춰 있는 것이 안 보인다. 가로축 하나에 전부 찍는다.
    자리는 손으로 안 찍는다 — 날짜를 달 수로 바꾼 값에서만 낸다."""
    pts = {}
    for w in watches:
        for k, m in (w.get('metrics') or {}).items():
            a = m.get('as_of')
            if _months(a) is not None:
                pts.setdefault(a, []).append(m.get('area') or k)
    if len(pts) < 2:
        return ''
    xs = dict((a, _months(a)) for a in pts)
    lo, hi = min(xs.values()), max(xs.values())
    # 판을 좁게 잡는다. 920 으로 두면 좁은 화면에서 2.4배 줄어 11px 글자가
    # 4.5px 이 된다 — 벡터라 판을 줄이면 같은 글자가 상대적으로 커진다
    X0, X1, Y = 20, W - 20, 66

    order = sorted(pts, key=lambda a: xs[a])
    # 가로축은 날짜 선형이 아니라 순위 등간격이다. 선형으로 두면 오른쪽 넉 달이
    # 한 자리에 뭉쳐 어느 라벨이 어느 점인지 못 짚는다 — 「2년 벌어져 있다」는
    # 사실은 아래 캡션 문장이 맡고, 자는 판독만 맡는다
    rank = dict((a, i) for i, a in enumerate(order))

    def px(a):
        n = len(order)
        return X0 + (X1 - X0) * (rank[a] / float(n - 1) if n > 1 else .5)

    # 라벨을 줄인다. 연도가 앞 점과 같으면 안 되풀이한다 — 오른쪽에 넉 달이 몰려 있어
    # 전체 날짜를 다 적으면 글자가 겹친다(실제로 다섯 쌍이 겹쳤다)
    lab, prev_y = [], None
    for a_ in order:
        y4 = a_[:4]
        lab.append(a_ if y4 != prev_y else a_[5:])
        prev_y = y4
    CH = 9.0                             # check_fig 이 한 자를 이만큼으로 센다.
    # 좁게 잡으면 내 눈에는 안 겹치는데 검사기는 겹친다고 한다 — 자를 맞춘다
    o = ['<line x1="%d" y1="%d" x2="%d" y2="%d" class="grid"/>' % (X0, Y, X1, Y)]
    # 위·아래 두 줄에 번갈아 놓고, 줄 안에서 겹치면 오른쪽으로 민다. 지시선이 제 점을
    # 가리키므로 라벨이 밀려도 어느 점인지는 안 흐려진다
    place = {}
    for row in (0, 1):
        idx = [i for i in range(len(order)) if i % 2 == row]
        wid = dict((i, len(lab[i]) * CH) for i in idx)
        x0 = dict((i, px(order[i]) - wid[i] / 2) for i in idx)
        # 왼쪽에서 오른쪽으로 밀고, 끝에 몰려 못 밀린 것은 오른쪽에서 왼쪽으로 되민다.
        # 한 번만 밀면 마지막 점이 판 끝에 붙어 앞 라벨과 겹친 채로 남는다.
        # 판 왼쪽 끝 clamp 를 맨 나중에 하면 첫 라벨이 오른쪽으로 튀어나가 두 번째
        # 라벨을 덮는다 — 밀기 전에 먼저 세운다
        x0[idx[0]] = max(x0[idx[0]], 2)
        for k in range(1, len(idx)):
            i, j = idx[k - 1], idx[k]
            x0[j] = max(x0[j], x0[i] + wid[i] + 6)
        x0[idx[-1]] = min(x0[idx[-1]], W - wid[idx[-1]] - 2)
        for k in range(len(idx) - 2, -1, -1):
            i, j = idx[k], idx[k + 1]
            x0[i] = min(x0[i], x0[j] - wid[i] - 6)
        x0[idx[0]] = max(x0[idx[0]], 2)
        for i in idx:
            place[i] = (x0[i] + wid[i] / 2, wid[i])
    for i, a_ in enumerate(order):
        x, n = px(a_), len(pts[a_])
        lx, _w = place[i]
        r = 3.5 + min(n, 12) * .5
        up = (i % 2 == 0)
        o.append('<circle cx="%.1f" cy="%d" r="%.1f" fill="var(--ink-2)"/>' % (x, Y, r))
        # 지시선은 꺾어서 간다. 비스듬한 선은 다른 선과 구분이 안 된다(check_fig)
        mid = (Y - 14) if up else (Y + 14)
        o.append('<path d="M%.1f %.1f L%.1f %d L%.1f %d L%.1f %d" class="grid"/>'
                 % (x, Y - r - 3 if up else Y + r + 3, x, mid, lx, mid,
                    lx, 36 if up else 96))
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle" '
                 'style="font-size:11px">%s</text>' % (lx, 30 if up else 110, E(lab[i])))
        o.append('<text x="%.1f" y="%d" class="t-sm" text-anchor="middle" '
                 'style="font-size:11px;font-weight:800">%d</text>'
                 % (lx, 16 if up else 124, n))
    gap = (xs[order[-1]] - xs[order[0]]) // 12
    who = ' · '.join(sorted(set(pts[order[0]]))[:2])
    note = ('가장 오래된 것이 %s(%s), 가장 새 것이 %s입니다 — %d년 넘게 벌어져 있습니다. '
            '왼쪽 끝이 오래됐다는 것은 그 자료가 그 뒤로 안 바뀌었다는 뜻입니다.'
            % (who, order[0], order[-1], gap)) if gap >= 1 else \
           ('%s부터 %s까지 들어와 있습니다.' % (order[0], order[-1]))
    return ('<svg viewBox="0 0 %d 134" role="img" aria-label="값이 언제 것인가" class="%s">'
            '%s</svg>' % (W, 'fig-w' if W > 400 else 'fig-n', ''.join(o)), note)


def time_ruler_fig(watches):
    """넓은 판과 좁은 판을 한 figure 에 싣는다. 좁은 화면에서 넓은 판을 밀게 두면
    점 하나만 보이고 나머지는 스크롤 뒤에 숨는다 — 밀 수 있다는 표시도 없다."""
    wide = time_ruler(watches, 640)
    if not wide:
        return ''
    narrow = time_ruler(watches, 360)
    return ('<figure>%s%s<figcaption>%s 점 크기는 그 때에 딸린 값의 개수입니다.</figcaption>'
            '</figure>' % (wide[0], narrow[0], E(wide[1])))


# ── 전세가율 자 ──────────────────────────────────────────────────────────
def _avg_series(w):
    """구 셋의 전세가율을 달마다 평균 낸 시계열. 카드 큰 수와 화살표가 이 값에서
    나온다. 구마다 그려도 되지만, 카드가 답해야 할 물음(「이 권역은 지금 전세가
    나은가」)에는 구 하나하나보다 권역 평균이 맞는 단위다. 모든 구가 그 달 값을
    냈을 때만 평균에 넣는다 — 하나라도 비면 그 달은 건너뛴다."""
    metrics = [m for k, m in (w.get('metrics') or {}).items() if k.startswith('jeonse_ratio_')]
    if not metrics:
        return []
    acc = {}
    for m in metrics:
        for t, v in (m.get('series') or []):
            acc.setdefault(t, []).append(v)
    n = len(metrics)
    return sorted((t, sum(vs) / n) for t, vs in acc.items() if len(vs) == n)


def _live_areas(watches):
    """전세가율이 실린 실거주 줄만. 투자 줄(강남3구, view 없음)도 같은 metric 을
    가질 수 있어 view 로 가른다 — 안 그러면 「강남 3구」점이 둘 찍힌다."""
    return [w for w in watches
            if w['kind'] == 'realestate' and w.get('view')
            and any(k.startswith('jeonse_ratio_') for k in (w.get('metrics') or {}))]


def ratio_ruler(watches, W=640):
    """시그니처 — 권역마다 지금 어디 있나를 한 줄에 놓는다.

    가로축은 고정 40~70%다(원문 값이 아니라 자의 눈금이라 값 대조에서 뺀다).
    점 위치는 그 권역 구별 전세가율의 평균, 테두리 색은 석 달 전 대비 방향이다 —
    오르면 --up, 내리면 --down. 표보다 이 그림이 먼저 「지금 어디 있나」를 답한다.

    눈금 글자는 축 위, 권역 라벨은 축 아래 한 줄에 둔다 — 처음에 라벨을 위아래로
    번갈아 놓았더니, 권역 값이 눈금과 같은 자리에 있을 때 그 라벨로 가는 지시선이
    눈금 글자를 그대로 가로질렀다(check_fig 「선에 깔림」). 두 종류의 글자가 같은
    구간을 지나지 않게 아예 위·아래로 나눈다."""
    live = _live_areas(watches)
    pts = []
    for w in live:
        avg = _avg_series(w)
        if not avg:
            continue
        cur = avg[-1][1]
        delta = avg[-1][1] - avg[-4][1] if len(avg) >= 4 else None
        pts.append((w['target'], cur, delta))
    if not pts:
        return ''
    # 눈금은 40~70 이 기본이고, 70 을 넘는 권역이 있으면 80 까지 늘린다 — 광주시(남한산성)
    # 74.4% 를 70 에 눌러 놓으면 「끝에 있다」로 읽힌다(2026-09-04). 눈금이라 값 대조에서 뺀다
    LO = 40.0
    HI = 80.0 if any(v > 70 for _n, v, _d in pts) else 70.0
    X0, X1, Y = 26, W - 26, 50

    def px(v):
        v = max(LO, min(HI, v))
        return X0 + (X1 - X0) * (v - LO) / (HI - LO)

    o = ['<line x1="%d" y1="%d" x2="%d" y2="%d" class="grid"/>' % (X0, Y, X1, Y)]
    for tkv in range(40, int(HI) + 1, 5):
        x = px(tkv)
        o.append('<path d="M%.1f %d L%.1f %d" class="grid"/>' % (x, Y - 4, x, Y + 4))
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle" '
                 'style="font-size:11px">%d</text>' % (x, Y - 16, tkv))

    pts.sort(key=lambda p: p[1])
    CH = 9.0
    labels = ['%s %s' % (n, _fmt1(v)) for n, v, _d in pts]
    # 좁은 판(모바일)에 권역이 다섯이면 「이름 값」이 한 줄에 안 든다 — 그때만 값을 떼고
    # 이름만 둔다(값은 패널·권역 요약에 있다). 넓은 판은 그대로
    if sum(len(l) * CH for l in labels) + 10 * (len(labels) - 1) > W - 4:
        labels = [n for n, _v, _d in pts]
    # 한 줄에 다 놓는다(점이 셋뿐이라 위아래로 나눌 이유가 없다). 겹치면 오른쪽으로
    # 밀고, 끝에 몰려 못 밀린 것은 왼쪽으로 되민다 — time_ruler와 같은 절차다
    idx = list(range(len(pts)))
    wid = dict((i, len(labels[i]) * CH) for i in idx)
    x0 = dict((i, px(pts[i][1]) - wid[i] / 2) for i in idx)
    for k in range(1, len(idx)):
        i, j = idx[k - 1], idx[k]
        x0[j] = max(x0[j], x0[i] + wid[i] + 10)
    x0[idx[-1]] = min(x0[idx[-1]], W - wid[idx[-1]] - 2)
    for k in range(len(idx) - 2, -1, -1):
        i, j = idx[k], idx[k + 1]
        x0[i] = min(x0[i], x0[j] - wid[i] - 10)
    x0[idx[0]] = max(x0[idx[0]], 2)
    place = dict((i, x0[i] + wid[i] / 2) for i in idx)

    LY = Y + 50            # 권역 라벨 글줄
    for i, (_name, val, delta) in enumerate(pts):
        x = px(val)
        edge = ('var(--up)' if delta and delta > 0 else
                'var(--down)' if delta and delta < 0 else 'var(--ink)')
        lx = place[i]
        o.append('<path d="M%.1f %d L%.1f %d L%.1f %d L%.1f %d" class="grid"/>'
                 % (x, Y + 9, x, Y + 20, lx, Y + 20, lx, Y + 36))
        o.append('<circle cx="%.1f" cy="%d" r="6" fill="var(--ink)" stroke="%s" '
                 'stroke-width="2"/>' % (x, Y, edge))
        o.append('<text x="%.1f" y="%d" class="t-sm" text-anchor="middle" '
                 'style="font-weight:700">%s</text>' % (lx, LY, E(labels[i])))
    cap_y = LY + 24
    o.append('<text x="%d" y="%d" class="t-sm t-axis">%s</text>' % (X0, cap_y, E('낮을수록 전세가 낫다')))
    o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="end">%s</text>'
             % (X1, cap_y, E('높을수록 매매가 가깝다')))
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="권역별 전세가율" class="%s">%s</svg>'
            % (W, cap_y + 10, 'fig-w' if W > 400 else 'fig-n', ''.join(o)))


def ratio_ruler_fig(watches):
    wide = ratio_ruler(watches, 640)
    if not wide:
        return ''
    narrow = ratio_ruler(watches, 360)
    asof = max([m['as_of'] for w in _live_areas(watches)
               for k, m in (w.get('metrics') or {}).items()
               if k.startswith('jeonse_ratio_')] or ['—'])
    cap = ('전세가율 = 중위 전세가 ÷ 중위 매매가. 세입자로 있을 거면 낮은 게 좋고, 살 거면 '
           '높은 게 얹을 돈이 적습니다. 대신 높을수록 보증금이 집값에 가까워져 못 돌려받을 '
           '위험이 커집니다. 기준 %s · 공표.' % E(asof))
    return '<figure>%s%s<figcaption>%s</figcaption></figure>' % (wide, narrow, cap)




# ── 용어 풀이 — 그 말 옆에 둔다 ─────────────────────────────────────────────
# 별도 「용어」 절을 안 둔다(CLAUDE.md 규칙). 대신 지표 이름이 등장하는 두 자리
# (본 장의 「지난번 본 뒤 바뀐 것」·상세의 머리 수치 띠)에 같은 문장을 붙인다 —
# TERM 사전 하나를 두 자리가 같이 읽어서, 한쪽만 고치고 다른 쪽을 잊는 일이 없다.
def _sale_base_month(watches):
    """매매가격지수의 기준월. unit 문자열이 "지수(기준시점=100)"처럼 날짜 없이
    와서, series 에서 값이 100 인 첫 달을 찾는다. 없으면 None — 그 자리는 문장이
    스스로 「기준월 = 100」으로 채운다."""
    for w in watches:
        for k, m in (w.get('metrics') or {}).items():
            if not k.startswith('sale_idx'):
                continue
            for t, v in (m.get('series') or []):
                if abs(v - 100.0) < 0.01:
                    return t
    return None


def _term_dict(watches):
    base = _sale_base_month(watches)
    basephrase = ('기준월(%s = 100)' % base) if base else '기준월 = 100'
    return {
        '매매가격지수': ('집값이 오르는 중인가 내리는 중인가. 그 구 아파트 값이 %s 대비 얼마나 '
                    '움직였나 — 값 자체보다 세 구가 같이 가나, 어느 구가 먼저 꺾이나를 본다.'
                    % basephrase),
        '전세가율': ('그 구 아파트의 중위 전세가 ÷ 중위 매매가. 세입자로 있을 거면 낮은 게 좋고, '
                  '살 거면 높은 게 얹을 돈이 적다. 대신 높을수록 보증금이 집값에 가까워져 '
                  '못 돌려받을 위험이 커진다.'),
        '전세가격지수': ('그 구 아파트 전세가가 %s 대비 얼마나 움직였나. 매매가격지수와 같은 '
                    '단위라 나란히 놓고 견줄 수 있다 — 전세가율이 내려갔을 때 전세가 빠진 '
                    '것인지 매매가 오른 것인지는 이 둘을 같이 봐야 갈린다.' % basephrase),
        '수급동향': '100 이 균형. 위면 사려는 사람이, 아래면 팔려는 사람이 많다.',
    }


def _metric_name(what):
    """트리거 「무엇을」에서 지표 이름만(구 이름을 뗀다) — "전세가율 — 강남구" → "전세가율"."""
    return (what or '').split(' —')[0].strip()


def term_lines(watches, names):
    """등장하는 지표 이름마다 풀이 한 줄. names 에 없는 지표는 안 낸다 — 세 줄을
    늘 다 보여주면 그중 못 보는 지표까지 설명한 꼴이 된다."""
    terms = _term_dict(watches)
    order = ('매매가격지수', '전세가격지수', '전세가율', '수급동향')
    keys = [n for n in order if n in names]
    if not keys:
        return ''
    return ''.join('<p class="term">%s — %s</p>' % (E(n), E(terms[n])) for n in keys)


# ── 지난번 본 뒤 바뀐 것 — 얼마나 움직였나 ──────────────────────────────────
# 2026-09-02: 사용자 지시 「조건 다 없애 — 독자마다 다른 거니까」. 트리거 문턱
# (「최근 3개월 흐름이 뒤집히고 0.5%p」류)은 글쓴이 개인 기준이라 독자에게는 뜻이
# 없다. 걸림·근접 판정과 조건 문장을 화면에서 걷고, 그 자리에 값 자체(지난달·
# 석 달 전 대비)만 남긴다. 데이터 모델(watch_lib.state_now 등)·검사기·알림
# (scripts/watch_mark.py)은 글쓴이 도구라 그대로 둔다 — 이 장만 안 부른다.
MOVE_ORDER = ('전세가율', '매매가격지수', '수급동향')
MOVE_UNIT = {'전세가율': '%p', '매매가격지수': 'pt', '수급동향': 'pt'}
MOVE_CUR_UNIT = {'전세가율': '%', '매매가격지수': '', '수급동향': ''}


def _movement_rows(watches):
    """전세가율·매매가격지수·수급동향의 원자료 — w['metrics'](픽업)가 아니라
    insights/watch/_metrics/ 원본을 그대로 읽는다. 실거주 줄의 context 는 매매가격
    지수를 안 걸어서(트리거가 전세가율뿐이라) 픽업에는 안 남는다 — 강남 3구는
    투자 줄(강남3구.md) 원본도 같이 보고, 나머지 둘은 실거주 줄 원본만으로 채운다.
    거래량(deal_count)은 뺀다 — 달마다 요동해 「석 달 대비」가 뜻이 없다.

    반환: {지표 이름: [(구·권역 이름, series), …]}."""
    by_slug = dict((w['slug'], w) for w in watches)
    groups = dict((n, {}) for n in MOVE_ORDER)   # 이름 -> {구/권역: series} — 중복 방지
    for w in _live_areas(watches):
        raw = wl.metrics_of(w['kind'], w['slug'])
        for k, m in raw.items():
            ser = m.get('series') or []
            if not ser:
                continue
            if k.startswith('jeonse_ratio_'):
                groups['전세가율'].setdefault(m.get('area') or k, ser)
            elif k.startswith('sale_idx_'):
                groups['매매가격지수'].setdefault(m.get('area') or k, ser)
            elif k == 'supply_demand':
                groups['수급동향'].setdefault(m.get('area') or w['target'], ser)
    inv = by_slug.get('강남3구')
    if inv:
        for k, m in wl.metrics_of(inv['kind'], inv['slug']).items():
            if k.startswith('sale_idx_') and (m.get('series') or []):
                groups['매매가격지수'].setdefault(m.get('area') or k, m['series'])
    return dict((n, sorted(g.items())) for n, g in groups.items())


def _delta(series, back):
    """series[-1] 과 series[-1-back] 의 차. 그 칸이 없으면 None."""
    if len(series) <= back:
        return None
    return series[-1][1] - series[-1 - back][1]


def _laws_grouped(watches):
    """법·고시 이름 → {지금 판·내가 읽은 판들·이 법을 보는 화면(제목, 슬러그)}.

    본 장의 요약과 watch/제도.html 의 전체 표가 같은 값을 봐야 한다 — 따로 세면
    「N개를 봅니다」의 N과 표의 행 수가 어긋날 수 있다."""
    by = {}
    for w in watches:
        if w['kind'] != 'policy':
            continue
        for _tg, name, seen in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            e = by.setdefault(name, {'now': m.get('value'), 'seen': set(), 'who': []})
            if seen:
                e['seen'].add(seen)
            e['who'].append((title_of(w), w['slug']))
    return by


def _law_state(e):
    return ('—' if not e['now'] or not e['seen']
            else ('같다' if e['seen'] == set([e['now']]) else '걸림'))


def law_table_full(watches, prefix=''):
    """법·고시 전체 표. watch/제도.html 전용이다 — 32개짜리 표를 한 문장으로 줄인
    것이 본 장의 「제도」 요약(law_summary)이고, 전체는 여기 있다. prefix 는 관련
    화면 링크가 어디를 가리켜야 하는지다. watch/ 폴더 안에서 부르므로 같은
    폴더의 파일명만 적으면 된다('') — gen_site.rewrite_links()가 own_slug='watch'로
    이 폴더를 처리할 때 그 형태(디렉터리 없는 파일명)만 /watch/<이름>으로 바꾼다."""
    by = _laws_grouped(watches)
    rows = []
    for name in sorted(by, key=lambda n: (by[n]['now'] or ''), reverse=True):
        e = by[name]
        st = _law_state(e)
        rows.append([E(name), E(e['now'] or '아직 안 받음'),
                     E(' · '.join(sorted(e['seen'])) or '—'), tag(st),
                     ' · '.join('<a href="%s%s.html">%s</a>' % (prefix, s, E(t))
                                for t, s in dict.fromkeys(e['who'])), '공표'])
    return tbl('법·고시가 지금 어느 판인가',
               ['법·고시', '지금 판', '내가 읽은 판', '같은가', '관련 화면', '기준'], rows)


def law_summary(watches):
    """본 장의 「제도」 섹션 — 표 대신 한 문장 + 바뀐 것만.

    법·고시는 32개인데 대부분 내가 읽은 판과 지금 판이 같다. 매달 그 32줄을 다시
    읽게 하는 대신 「몇 개를 보고 몇 개가 바뀌었나」만 밝히고, 바뀐 것만 이름을 댄다.
    전체는 watch/제도.html 에 그대로 있다."""
    by = _laws_grouped(watches)
    changed = sorted(name for name, e in by.items() if _law_state(e) == '걸림')
    h = ['<p class="band-s">법·고시 %d개를 봅니다. 내가 읽은 뒤 바뀐 것 %d개.</p>'
         % (len(by), len(changed))]
    if changed:
        h.append('<div class="rows">')
        for name in changed:
            e = by[name]
            who = ' · '.join('<a href="watch/%s.html">%s</a>' % (s, E(t))
                              for t, s in dict.fromkeys(e['who']))
            h.append('<div class="row"><span class="row-where">%s%s</span>'
                     '<span class="row-what">%s → %s</span>'
                     '<span class="row-why">관련 화면 %s</span></div>'
                     % (tag('걸림'), E(name), E(' · '.join(sorted(e['seen']))), E(e['now']), who))
        h.append('</div>')
    h.append('<p class="lbl"><a href="watch/제도.html">전체 표 →</a></p>')
    return ''.join(h)


def subscription_now(watches, sido='서울'):
    """「분양」 절의 「지금 청약」 축약 — 그 시·도의 최근 3개월 공고를 공고일 늦은 순으로
    다섯 건, 제목 줄(단지명·구·상태)만(2026-09-04 사용자 지시 「제목만 최근 3개월 다섯」).
    평수·분양가·시세 줄은 watch/청약 공고.html 에 있다. 어댑터가 못 냈으면 빈 문자열."""
    items, as_of = _all_sub_items(watches)
    if items is None:
        return ''
    today = _TODAY
    cut = _months_before(today, 3)
    items = [it for it in items if _sido_of(it.get('gu') or '') == sido
             and (it.get('pblanc_de') or it.get('apply') or '') >= cut]
    items.sort(key=lambda it: (it.get('pblanc_de') or it.get('apply') or ''), reverse=True)
    n_open = sum(1 for it in items if _sub_status(it, today) == '접수 중')
    n_soon = sum(1 for it in items if _sub_status(it, today) == '접수 예정')
    where = '서울' if sido == '서울' else '경기 (보고 있는 %d곳)' % len(_sido_gus('경기'))
    h = ['<p class="cond-t">지금 청약</p>',
         '<p class="cond-lead">최근 3개월 %s 공고 %d건 · 지금 접수 중 %d건 · '
         '접수 예정 %d건</p>' % (E(where), len(items), n_open, n_soon)]
    if items:
        # 접수 중·접수 예정은 전부(접수 시작 가까운 순), 나머지(발표 대기·발표됨)는 공고일
        # 늦은 순으로 다섯을 채울 만큼만(2026-09-04 사용자 지시 「접수중, 접수예정은 다」)
        live = sorted((it for it in items if _sub_status(it, today) in ('접수 중', '접수 예정')),
                      key=lambda it: it.get('apply') or '')
        rest = [it for it in items if _sub_status(it, today) not in ('접수 중', '접수 예정')]
        shown = live + rest[:max(0, 5 - len(live))]
        rows = []
        for it in shown:
            st = _sub_status(it, today)
            cls = _SUB_STATUS_CLS.get(st, 't-none')
            # 이름 옆에 마감일·평수(2026-09-04 사용자 지시). 마감(RCEPT_ENDDE)이 없으면
            # 접수 시작일을, 주택형이 없으면 평수 자리를 비운다 — 지어내지 않는다
            end = it.get('end')
            when = ('마감 %s' % end[5:]) if end else (('접수 %s' % it['apply'][5:]) if it.get('apply') else '')
            gs = _group_types(it.get('types') or [])
            if gs:
                lo, hi = gs[0]['ex'], gs[-1]['ex']
                py = lambda ex: int(round(ex / 3.3058))
                area = ('%d㎡(약 %d평)' % (lo, py(lo)) if lo == hi
                        else '%d~%d㎡(약 %d~%d평)' % (lo, hi, py(lo), py(hi)))
            else:
                area = ''
            # 최고분양가 — 주택형 가운데 가장 비싼 값(LTTOT_TOP_AMOUNT). 평당가는 안 낸다 —
            # 어댑터가 받는 면적이 전용(HOUSE_TY 정수부)뿐이라 관례(공급면적 기준)와 어긋난다
            top = max((g['top'] for g in gs), default=0)
            top_txt = ('최고 %s' % _fmt_eok(top)) if top else ''
            meta = ' · '.join(x for x in (E(it.get('gu') or ''), E(when), E(area), E(top_txt)) if x)
            # 첫 줄 왼쪽 단지명, 오른쪽 상태·공고일. 둘째 줄 구·마감·평수 — 모바일에서
            # 칩이 셋째 줄로 떨어지던 것을 고친 자리(2026-09-04 사용자 스크린샷)
            rows.append('<div class="sub-title"><p class="st-1"><a href="watch/청약 공고.html#p-%s">%s</a>'
                        '<span class="st-r"><span class="tag %s si-chip">%s</span>'
                        '<span class="t-sub"> · 공고 %s</span></span></p>'
                        '<p class="st-2 t-sub">%s</p></div>'
                        % (E(it.get('id') or ''), E(it.get('name') or '—'),
                           cls, E(st), E(it.get('pblanc_de') or it.get('apply') or '—'), meta))
        h.append('<div class="sub-list">%s</div>' % ''.join(rows))
    else:
        h.append('<p class="cond-lead">최근 3개월에 공고가 없습니다</p>')
    h.append('<p class="lbl"><a href="watch/청약 공고.html">공고 전부 보기 →</a> · '
             '<a href="#subscription-cond">청약 조건 →</a></p>')
    h.append('<p class="cond-tail">청약홈(공공데이터포털) · 기준 %s · 상태는 화면 만든 날 %s '
             '기준 · 공급위치 주소로 구를 골라 놓친 공고가 있을 수 있음</p>'
             % (E(as_of or '—'), E(today)))
    return ''.join(h)


def _months_before(ymd, n):
    """YYYY-MM-DD 에서 n 달 앞 날짜(같은 일, 없으면 그 달 말일)."""
    y, m, d = int(ymd[:4]), int(ymd[5:7]), int(ymd[8:10])
    m -= n
    while m <= 0:
        m += 12
        y -= 1
    import calendar
    d = min(d, calendar.monthrange(y, m)[1])
    return '%04d-%02d-%02d' % (y, m, d)


def subscription_section(watches, sido='서울', suffix=''):
    """시·도 상자 맨 위의 「분양」 절 — 그 시·도의 지금 청약(공고)만. 조건 표 셋은
    전국 공통이라 subscription_cond_section() 으로 한 번만 낸다(2026-09-04, 「분양이
    가장 빨리 오게」 + 「서울 경기 구분이 가장 상위」)."""
    body = subscription_now(watches, sido)
    if not body:
        return ''
    return ('<div class="band" id="subscription%s"><p class="band-t">분양 — 지금 청약</p>%s</div>'
            % (suffix, body))


def subscription_cond_section(watches):
    """「청약 — 조건」 절(전국 공통, 탭 밖). 조건 표를 가진 정책 줄(지금은 청약 제도
    하나)의 표를 그대로 낸다.

    이 절만 본 장에 표를 둔다. 나머지 표는 전부 상세(watch/)로 옮겼는데, 청약
    조건은 「지금 신청할 수 있나」에 바로 답하는 값이라 한 번 더 열게 하지 않는다."""
    for w in sorted(watches, key=lambda x: x['slug']):
        if not cond_blocks(w)[1]:
            continue
        more = ('<p class="lbl"><a href="watch/%s.html">%s 자세히 →</a></p>'
                % (w['slug'], E(w['target'])))
        return ('<div class="band" id="subscription-cond"><p class="band-t">청약 — 조건</p>%s%s</div>'
                % (cond_html(w, ''), more))
    return ''


def figures_lists(w):
    """도해 목록 — (우선순위, HTML) 짝. series 가 든 metric 만 그린다 — 어댑터가
    안 채운 자리에는 아무것도 안 선다.

    「조건이 걸렸던 달」 빈 원(marks)은 안 넘긴다(2026-09-02, 「조건 다 없애」) —
    watch_fig.trend() 는 안 건드리고, marks 인자를 그냥 안 준다. trend() 의
    marks 기본값이 None → `marks or []` → `any([])` 라 그 범례 줄도 저절로 안 나온다.

    우선순위 0(값 트리거가 건 metric)은 상세 페이지 머리 쪽(판단 산문보다 먼저)에,
    1(나머지 참고용 시계열)은 법 표 아래쪽에 선다 — 상세 페이지를 여는 이유가 그
    값이지 참고용 시계열이 아니다."""
    TITLE = {'sale_idx': '매매가격지수', 'jeonse_idx': '전세가격지수',
             'jeonse_ratio': '전세가율 — 중위 매매가 대비 중위 전세가',
             'supply_demand': '매매수급동향 — 100이 균형',
             'median': '서울 중위가격 — 매매와 전세',
             'deal_count': '아파트 매매 거래량', 'rent_conv': '전월세 전환율',
             # 실거래가격지수 — 반복매매라 표본 구성에 안 흔들린다. 월간은 권역까지만
             # 내려오고 구 단위는 분기뿐이라 둘을 따로 그린다
             'rtp': '실거래가격지수 — 매매와 전세 (2017.11=100, 권역 단위)',
             'rtp_sale_idx_gu': '실거래가격지수 — 매매, 구별 (분기)'}
    GROUP = {'median_sale': ('median', '매매'), 'median_jeonse': ('median', '전세'),
             'rtp_sale_idx': ('rtp', '매매'), 'rtp_jeonse_idx': ('rtp', '전세')}
    trig_by_metric = dict((t['metric'], t) for t in w['triggers']
                          if t['kind'] == wl.KIND_VALUE and t['metric'])
    groups = {}
    for key, m in sorted((w.get('metrics') or {}).items()):
        if not m.get('series'):
            continue
        # 매매·전세 가격지수는 따로 안 그린다 — 구마다 두 선을 한 판에 놓은
        # idx_figs() 로 대체했다(같은 정보가 세 번 나오지 않게)
        if key.startswith('sale_idx_') or key.startswith('jeonse_idx_'):
            continue
        area = m.get('area') or ''
        base = key[:-(len(area) + 1)] if area and key.endswith('_' + area) else key
        gk, gn = GROUP.get(base, (base, area or base))
        groups.setdefault((gk, m.get('unit') or ''), []).append((gn, m, key))

    def _prio(item):
        _gk, entries = item
        return 0 if any(k in trig_by_metric for _n, _m, k in entries) else 1

    out = []
    for key, items in sorted(groups.items(), key=_prio):
        base, unit = key
        prio_val = _prio((key, items))
        sel = items[:3]
        note = ' · '.join(dict.fromkeys(m.get('src', '') for _n, m, _k in sel if m.get('src')))
        ser = [(n, [tuple(x) for x in m['series']]) for n, m, _k in sel]
        svg = wf.trend(ser, unit or '값', note=note)
        if svg:
            nsvg = wf.trend(ser, unit or '값', note=note, narrow=True)
            out.append((prio_val, '<figure>%s%s<figcaption>%s</figcaption></figure>'
                       % (svg.replace('<svg ', '<svg class="fig-w" ', 1),
                          nsvg.replace('<svg ', '<svg class="fig-n" ', 1),
                          E(TITLE.get(base, base)))))
    return out


def idx_figs(w):
    """구마다 매매·전세 가격지수 두 선을 한 판에.

    전세가율 = 전세 ÷ 매매라, 그 값이 내려가도 전세가 빠진 건지 매매가 오른 건지
    한 선으로는 모른다. 둘 다 기준월=100 짜리 지수라 같은 축에 놓을 수 있다.
    구별 절대 매매가는 안 나온다(서울 전체 중위가뿐) — 그래서 지수로 견준다."""
    idx = _idx_of(w)
    out = []
    for gu in sorted(idx):
        d = idx[gu]
        if 'sale' not in d or 'jeonse' not in d:
            continue
        ser = [('매매', d['sale']), ('전세', d['jeonse'])]
        svg = wf.trend(ser, '지수(기준시점=100)')
        if not svg:
            continue
        nsvg = wf.trend(ser, '지수(기준시점=100)', narrow=True)
        out.append('<figure>%s%s<figcaption>%s</figcaption></figure>'
                   % (svg.replace('<svg ', '<svg class="fig-w" ', 1),
                      nsvg.replace('<svg ', '<svg class="fig-n" ', 1),
                      E('%s — 매매·전세 가격지수 (기준월=100)' % gu)))
    return ''.join(out)


def figures_trigger(w):
    return ''.join(html for p, html in figures_lists(w) if p == 0)


def figures_rest(w):
    return ''.join(html for p, html in figures_lists(w) if p == 1)


def stat_strip(w):
    """머리 수치 띠 — 부동산 줄 상세에서 그 줄이 건 값을, 산문보다 먼저 큰 글씨로
    보여준다. 값이 없으면(트리거에 series 가 없으면) 아무것도 안 낸다."""
    if w['kind'] != 'realestate':
        return ''
    vals = [t for t in w['triggers'] if t['kind'] == wl.KIND_VALUE and t['series']]
    if not vals:
        return ''
    cells, notes = [], []
    for t in vals:
        ser = [tuple(x) for x in t['series']]
        cur = ser[-1][1]
        # 본 장 패널과 같은 계산·같은 기간이다. 예전에는 여기만 석 달치를 화살표로
        # 냈고 본 장은 지난달치를 냈다 — 같은 값에 빨강 오름과 파랑 내림이 동시에
        # 붙어 나갔다(P1-5). 기간을 글자로 박아 그 자리를 막는다
        d1 = ser[-1][1] - ser[-2][1] if len(ser) >= 2 else None
        base1 = ser[-2][0] if len(ser) >= 2 else None
        unit = t.get('unit') or ''
        du = _delta_unit(unit)
        m = re.search(r'—\s*(\S+)$', t['what'] or '')
        label = m.group(1) if m else t['what']
        # 값과 변화를 딴 요소에 둔다. 한 요소에 이어 붙이면 글자를 키운 폰에서 변화가
        # 옆 열의 큰 수 위로 넘쳤다(2026-09-03, 사용자 스크린샷). 좁은 화면은 CSS 가
        # 이 셋을 한 줄(이름 · 값 · 변화)로 눕힌다
        cells.append(
            '<div class="stat"><p class="stat-k">%s</p>'
            '<p class="stat-v">%s%s</p><p class="stat-d">%s</p></div>'
            % (E(label), _fmt1(cur), E(unit), _delta_num(d1, du)))
        notes.append('%s · 기준 %s · %s'
                     % (_delta_when('지난달', base1) if d1 is not None else '지난달 값이 없습니다',
                        E(t['as_of'] or '—'), E(t['nature'] or '공표')))
    # 「지난달(2026-06) 대비 · 기준 2026-07 · 공표」가 구 셋에 같으면 한 번만 적는다 —
    # 칸마다 두 줄씩 되풀이하면 좁은 화면에서 그 줄이 접혀 띠가 세 배로 길어진다
    if len(set(notes)) == 1:
        foot = '<p class="stat-m">%s</p>' % notes[0]
    else:
        foot = ''.join('<p class="stat-m">%s — %s</p>' % (c.split('stat-k">')[1].split('<')[0], n)
                       for c, n in zip(cells, notes))
    names = set(_metric_name(t['what']) for t in vals)
    return '<div class="stats">%s</div>%s%s' % (''.join(cells), foot, term_lines([w], names))


def link_out(url):
    """확인처 칸. URL 이면 도메인만 글자로 보이는 링크로, 아니면(빈 칸·「어댑터」)
    그대로 글자로 낸다 — 없는 것을 링크인 척 안 한다."""
    url = (url or '').strip()
    if not url:
        return '<span class="t-none">—</span>'
    m = re.match(r'https?://([^/]+)', url)
    if not m:
        return wl.md_inline(url)
    return '<a href="%s">%s</a>' % (E(url), E(m.group(1)))


def _lth_detail_block(w):
    """토지거래허가구역 「지정 내역」 — 지도 패널에서 뺀 긴 detail 문장이 가는
    자리(2026-09-03). 그 권역 구 셋만, 값·detail·기준·출처를 표로 낸다.
    권역이 없는 줄(정책 줄 등)은 아무것도 안 낸다."""
    gus = AREAS.get(w['target'], {}).get('구') or []
    if not gus:
        return ''
    z = ZONES.get('토지거래허가구역', {})
    rows = []
    for g in gus:
        v, d = _lth_info(g)
        if v is None:
            continue
        rows.append([E(g), E(v), wl.md_inline(d) if d else '<span class="t-none">—</span>',
                     E(z.get('as_of') or '—'), _src_link(z.get('src'))])
    if not rows:
        return ''
    return tbl('토지거래허가구역 지정 내역', ['구', '지정', '내용', '기준', '출처'], rows)


def line_block(w):
    """줄 하나의 상세 본문 — watch/<슬러그>.html 안에 실린다.

    2026-09-02 순서 — 머리 수치 띠 → 트리거 metric 도해 → 「지금 판단」 산문 →
    「판단 이력」 → 정책 줄의 법 표 → 나머지 도해 → 「왜 보나」 →
    「사람이 확인하는 것」 → 「반대 근거」. 그 줄을 여는 이유가 되는 값(트리거가
    건 metric)을 산문보다 먼저 세운다 — 나머지는 참고용 시계열이다.

    2026-09-02 두 번째 개정(「조건 다 없애」) — 「값으로 오는 것」 표(무엇을·지금·
    조건·상태·걸리면·기준)를 통째로 걷었다. 그 표가 보여주던 트리거 문턱은
    글쓴이 개인 기준이라 독자에게는 뜻이 없다. 머리 수치 띠(stat_strip)가 이미
    같은 값(지금·석 달 Δ·기준)을 문턱 없이 보여준다."""
    trig = [html for p, html in figures_lists(w) if p == 0]
    # 「값 더」 맨 앞이 구별 매매·전세 두 선 판이다 — 전세가율을 무엇이 움직였는지가
    # 그 판에서만 갈린다
    pair = idx_figs(w)
    rest = ([pair] if pair else []) + trig[1:] + \
        [html for p, html in figures_lists(w) if p == 1]
    h = ['<section class="line">']
    strip = stat_strip(w)
    if strip:
        h.append('<div id="now">%s</div>' % strip)
    # 문단마다 <p> — md 의 빈 줄을 살린다. 한 덩어리로 붙이면 굵은 첫 문장들이 줄줄이
    # 이어져 어디서 생각이 바뀌는지 안 보인다
    paras = w.get('judged_paras') or [w['judged']]
    h.append('<div id="judge">%s%s</div>'
             % (''.join('<p class="line-judge">%s</p>' % x for x in paras),
                trig[0] if trig else ''))
    # 「조건」 — 판단 바로 다음이다. 이 줄을 여는 이유가 「지금 신청할 수 있나」라
    # 판단 한 마디 다음에 곧장 그 표가 서야 한다
    cond = cond_html(w)
    if cond:
        h.append('<div id="cond"><p class="lbl">조건</p>%s</div>' % cond)
    if w['clash']:
        h.append('<div id="clash"><p class="lbl">반대 근거</p><ul class="pts">%s</ul></div>'
                 % ''.join('<li>%s</li>' % c for c in w['clash']))

    hist = ''
    if w.get('history'):
        hist = tbl('판단 이력', ['날짜', '무엇을', '왜'],
                   [[E(d), wl.md_inline(what), wl.md_inline(why)]
                    for d, what, why in w['history']])
    if w.get('laws'):
        rows = []
        for _tg, name, seen in w['laws']:
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            st = '—' if not now or not seen else ('같다' if str(now) == seen else '걸림')
            rows.append([E(name), E(seen or '—'), E(now or '아직 안 받음'), tag(st)])
        hist += tbl('내가 읽은 판과 지금 판',
                    ['법·고시', '내가 읽은 판', '지금 판', '같은가'], rows)
    if hist:
        h.append('<div id="hist">%s</div>' % hist)
    if rest:
        h.append('<div id="more">%s</div>' % ''.join(rest))
    if w['points']:
        h.append('<div id="why"><p class="lbl">왜 보나</p><ul class="pts">%s</ul></div>'
                 % ''.join('<li>%s</li>' % p for p in w['points']))
    # 사건 트리거도 「걸리면」(다음에 할 일) 없이 「무엇을 확인하나 · 어디서」 둘로
    # — 「언제 판단이 바뀌나」 열도 조건 문장이라 함께 걷는다(2026-09-02)
    evt = [t for t in w['triggers'] if t['kind'] == wl.KIND_EVENT]
    where = ''
    if evt:
        where = tbl('사람이 확인하는 것', ['무엇을 확인하나', '어디서'],
                    [[E(t['what']), link_out(t['where'])] for t in evt])
    where += _lth_detail_block(w)
    if where:
        h.append('<div id="where">%s</div>' % where)
    h.append('</section>')
    return ''.join(h)


def _detail_jump(w):
    """상세의 절 바로가기 — 있는 절만. 6,300px 짜리 페이지에서 「반대 근거만 보고
    싶다」가 스크롤 노동이 되면 안 된다."""
    body = line_block(w)
    items = [('now', '지금 값'), ('judge', '판단'), ('cond', '조건'),
             ('clash', '반대 근거'), ('hist', '이력'), ('more', '값 더'),
             ('where', '확인처')]
    got = [(i, t) for i, t in items if ('id="%s"' % i) in body]
    if len(got) < 2:
        return body, ''
    nav = ('<nav class="jump" aria-label="절 바로가기">%s</nav>'
           % ''.join('<a href="#%s">%s</a>' % (i, E(t)) for i, t in got))
    return body, nav


def _first_sentence(judged):
    """카드·목록에 쓸 「지금 판단」 요약 한 줄 — verdict 가 없을 때만 쓰는 대체
    경로다. 첫 볼드 문장, 없으면 첫 문장.

    judged 는 이미 **굵게**가 <b> 로 풀린 HTML 이다(watch_lib.md_inline)."""
    m = re.search(r'<b>(.*?)</b>', judged, re.S)
    if m:
        return m.group(1)
    text = re.sub(r'<[^>]+>', '', judged).strip()
    idx = text.find('.')
    return text[:idx + 1] if idx >= 0 else text


def _line_group(w):
    """목록을 관점으로 가른다. 「강남 3구」와 「강남 3구 — 집 구하는 사람」이 아무
    말 없이 나란히 서 있으면 뒤엣것이 앞엣것의 부분처럼 읽힌다 — 실은 같은 권역을
    다른 눈으로 본 두 줄이다. 관점을 묶음 이름으로 올리고 줄 이름에서는 뗀다."""
    if w['kind'] != 'realestate':
        return 2
    return 0 if w.get('view') else 1


GROUP_NAME = {0: '집 구하는 사람', 1: '투자로 보는 사람', 2: '제도'}
GROUP_NOTE = {1: '강남 3구만 봅니다 — 나머지 두 권역은 아직 안 봅니다.'}


def _checked_note(watches):
    """마지막 확인 날짜를 절 제목 옆에 한 번만 적는다. 열 줄 중 아홉이 같은 날짜면
    그 열은 되풀이되는 상수라 스캔만 방해한다 — 다른 것만 이름을 댄다."""
    dates = [w['checked'] for w in watches if w.get('checked')]
    if not dates:
        return ''
    common = max(set(dates), key=dates.count)
    odd = ['%s(%s)만 %s' % (w['target'], GROUP_NAME[_line_group(w)], w['checked'])
           for w in sorted(watches, key=lambda x: x['slug'])
           if w.get('checked') and w['checked'] != common]
    txt = '전부 %s 확인' % common
    if odd:
        txt += ' · ' + ' · '.join(odd)
    return '<span class="band-note">%s</span>' % E(txt)


def line_summary_rows(watches, sido=None):
    """본 장의 「보고 있는 것」 목록 — 이름·verdict 만. 마지막 확인 날짜는 절 제목
    옆으로 올렸다(_checked_note). 칩(걸림·근접)은 없다 — 문턱은 독자마다 달라 뜻이
    없다."""
    # sido 가 있으면 그 시·도의 실거주·투자 줄만, 없으면 제도 줄(전국)만
    if sido:
        watches = _sido_watches(watches, sido)
    else:
        watches = [w for w in watches if w['kind'] != 'realestate']
    ordered = sorted(watches, key=lambda w: (_line_group(w), w['slug']))
    h, cur = [], None
    for w in ordered:
        g = _line_group(w)
        if g != cur:
            h.append('<p class="lbl">%s</p>' % E(GROUP_NAME[g]))
            if GROUP_NOTE.get(g):
                h.append('<p class="wline-v">%s</p>' % E(GROUP_NOTE[g]))
            cur = g
        verdict = w.get('verdict') or _first_sentence(w['judged'])
        h.append('<div class="wline"><a class="wline-t" href="watch/%s.html">%s</a>'
                 '<p class="wline-v">%s</p></div>'
                 % (w['slug'], E(w['target']), E(verdict)))
    return ''.join(h)


def detail_page(w):
    """줄 하나의 상세 페이지 — 대시보드/watch/<슬러그>.html.

    돌아가는 링크에 앵커(#lines)를 붙인다. scripts/gen_site.py의 rewrite_links()가
    「../<대시보드 파일명>.html#<앵커>」꼴만 절대경로(/watch#lines)로 바꾼다 — 앵커가
    없는 「../포트폴리오 워치.html」은 그 정규식이 안 잡아서 배포판에서
    site/watch/<슬러그>.html 기준으로 상대경로가 풀려 엉뚱한 자리(/포트폴리오 워치.html)로
    간다. 로컬 파일 경로로도, 배포 경로로도 맞는 꼴은 이 형태뿐이다."""
    t9 = title_of(w)
    view = w.get('view') or KIND_LABEL.get(w['kind'], w['kind'])
    verdict = w.get('verdict') or _first_sentence(w['judged'])
    body, nav = _detail_jump(w)
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s — 포트폴리오 워치</title>%s<style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#map">'
            '← 서울 지도로</a>'
            '<header><p class="meta mono">%s · %s · 마지막 확인 %s</p><h1>%s</h1>'
            '<p class="verdict">%s</p></header>%s'
            '<div class="dbody">%s</div>'
            '<p><a class="back" href="../포트폴리오 워치.html#lines">'
            '← 보고 있는 것 목록</a></p>'
            '<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
            '마지막 확인 %s. 통계가 갱신되면 다음 달에 다시 확인합니다.</footer>'
            '<!-- 이 화면은 scratchpad/gen_watch_page.py 가 만든다. 판단은'
            ' insights/watch/, 수치는 insights/watch/_metrics/ -->%s'
            '</div></body></html>'
            % (E(t9), FONTS, CSS, E(_area_head(w['target'])), E(view), E(w['checked'] or '—'),
               E(t9), E(verdict), nav, body, E(w['checked'] or '—'), _JUMP_JS))


def law_page(watches):
    """법·고시 전체 표 페이지 — 대시보드/watch/제도.html.

    본 장 「제도」 요약이 「전체 표 →」로 여기를 가리킨다. 표 아래에 정책 줄로 가는
    링크도 둔다 — 표의 「관련 화면」 칸에 이미 있지만, 여섯 줄을 한눈에 훑을 목록이
    따로 있는 편이 낫다."""
    policy_ws = sorted((w for w in watches if w['kind'] == 'policy'),
                       key=lambda w: w['slug'])
    links = ''.join('<div class="wline"><a class="wline-t" href="%s.html">%s</a></div>'
                    % (w['slug'], E(title_of(w))) for w in policy_ws)
    body = law_table_full(watches, prefix='') + '<p class="lbl">이 법·고시를 보는 화면</p>' + links
    # 앵커(#policy)가 필요한 이유는 detail_page()와 같다 — rewrite_links()가
    # 「../<파일명>.html#<앵커>」꼴만 /watch#policy로 바꾼다.
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>제도 — 포트폴리오 워치</title>%s<style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#policy">'
            '← 포트폴리오 워치</a>'
            '<header><p class="meta mono">법·고시 %d개</p><h1>제도</h1></header>'
            '<div class="dbody">%s</div>'
            '<footer>제도는 국가법령정보센터에서 받습니다. 통계가 갱신되면 다음 달에 '
            '다시 확인합니다.</footer>'
            '<!-- 이 화면은 scratchpad/gen_watch_page.py 가 만든다 -->'
            '</div></body></html>'
            % (FONTS, CSS, len(_laws_grouped(watches)), body))


_SUB_EMPTY = {'soon': '예정된 공고가 아직 없습니다',
              'wait': '발표를 기다리는 공고가 없습니다',
              'done': '최근 6개월에 발표된 공고가 없습니다'}


def _sub_band(id_, title, items, empty_txt, market):
    if items:
        body = ('<div class="sub-list">%s</div>'
                % ''.join(_sub_item_html(it, _TODAY, full=True, market=market) for it in items))
    else:
        body = '<p class="cond-lead">%s</p>' % E(empty_txt)
    return '<div class="band" id="%s"><p class="band-t">%s</p>%s</div>' % (id_, E(title), body)


def subscription_page(watches):
    """청약 공고 전부 — 대시보드/watch/청약 공고.html(청약공고_스펙 §4).

    구별 필터는 없다 — 지도의 「청약 공고」 층이 이미 구로 고르는 자리라, 이
    페이지는 상태(접수 중·예정·발표 대기·발표됨) 넷으로만 가른다. 표가 아니라
    목록이다 — 한 건에 값이 여덟이라 열이 여덟이면 모바일에서 가로로 밀린다."""
    today = _TODAY
    items, as_of = _all_sub_items(watches)
    if items is None:
        items, as_of = [], '—'
    groups = {'open': [], 'soon': [], 'wait': [], 'done': []}
    key_of = {'접수 중': 'open', '접수 예정': 'soon',
             '접수 마감·발표 대기': 'wait', '발표됨': 'done'}
    for it in items:
        st = _sub_status(it, today)
        groups[key_of.get(st, 'done')].append(it)
    groups['open'].sort(key=lambda it: it.get('apply') or '')
    groups['soon'].sort(key=lambda it: it.get('apply') or '')
    groups['wait'].sort(key=lambda it: it.get('announce') or '', reverse=True)
    groups['done'].sort(key=lambda it: it.get('announce') or '', reverse=True)

    verdict = _sub_verdict(items, today)
    nav_items = [('open', '접수 중', len(groups['open'])),
                ('soon', '접수 예정', len(groups['soon'])),
                ('wait', '발표 대기', len(groups['wait'])),
                ('done', '발표됨', len(groups['done']))]
    nav = ('<nav class="jump" aria-label="절 바로가기">%s'
          '<a href="#basis">자료 기준</a></nav>'
          % ''.join('<a href="#%s">%s %d</a>' % (i, E(t), n) for i, t, n in nav_items))

    market = _watched_market(watches)
    bands = (_sub_band('open', '접수 중', groups['open'], verdict, market)
            + _sub_band('soon', '접수 예정 · 접수 시작 가까운 순', groups['soon'], _SUB_EMPTY['soon'], market)
            + _sub_band('wait', '발표 대기 · 발표 최근 순', groups['wait'], _SUB_EMPTY['wait'], market)
            + _sub_band('done', '발표됨 · 발표 최근 순', groups['done'], _SUB_EMPTY['done'], market))
    basis = ('<div class="band" id="basis"><p class="band-t">자료 기준</p>'
            '<p class="cond-tail">청약홈(공공데이터포털 15098547·15098905) · 자료 기준 %s · '
            '상태는 화면 만든 날 %s 기준 · 최근 6개월 모집공고 · 공급위치 주소로 구를 골라 '
            '놓친 공고가 있을 수 있음</p>'
            '<p><a class="back" href="../포트폴리오 워치.html#subscription">'
            '← 포트폴리오 워치</a></p></div>'
            % (E(as_of or '—'), E(today)))
    # back 링크에 앵커(#subscription)를 반드시 붙인다 — gen_site.rewrite_links()가
    # 「../<파일명>.html#<앵커>」꼴만 /watch#subscription 으로 바꾼다.
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           '<title>청약 공고 — 포트폴리오 워치</title>%s<style>%s</style></head><body>'
           '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#subscription">'
           '← 포트폴리오 워치</a>'
           '<header><p class="meta mono">서울 25구 + 성남 3구 · 최근 6개월 %d건 · 청약홈 기준 %s</p>'
           '<h1>청약 공고</h1><p class="verdict">%s</p></header>%s'
           '<div class="dbody">%s%s</div>'
           '<!-- 이 화면은 scratchpad/gen_watch_page.py 가 만든다 -->%s'
           '</div></body></html>'
           % (FONTS, CSS, len(items), E(as_of or '—'), E(verdict), nav, bands, basis, _JUMP_JS))


def _src_link(src):
    """법·고시 표의 messy 다중 URL 문자열(예: "https://a ; https://b")에서 첫
    URL만 뽑아 도메인 링크로 낸다. link_out() 은 URL 이 문자열 전체일 때만
    맞는 짝이라(끝의 부가설명까지 href 에 실린다) 지도 범례는 따로 쓴다."""
    m = re.search(r'https?://[^\s;]+', src or '')
    if not m:
        return E(src or '—')
    url = m.group(0)
    dm = re.match(r'https?://([^/]+)', url)
    return '<a href="%s">%s</a>' % (E(url), E(dm.group(1)))


def _ratio_legend_html(watches, gus=None):
    """전세가율 범례 — 다섯 단 색 띠 + 방향 한 줄 + 값 없는 구 이름 + 전세가율 자.

    값 없는 구는 수만 적으면(「값 없음 — 16구」) 어느 구인지 알 길이 없다. 지도에서
    자기 동네를 못 찾은 사람이 여기서 이름을 확인한다."""
    blanks = sorted(set(gus or SEOUL_GU['gu']) - set(WATCHED_GU))
    names = '·'.join(g[:-1] if g.endswith('구') else g for g in blanks)
    strip = ''.join('<span class="leg-sw" style="background:var(--seq-%d)"></span>' % i
                    for i in range(1, 6))
    labels = ''.join('<span>%s</span>' % E(t) for t in ('<45', '45~50', '50~55', '55~60', '≥60'))
    return ('<div class="leg-strip">%s</div><p class="leg-labels">%s</p>'
            '<p class="leg-src">→ 오른쪽일수록 매매가에 가깝습니다.</p>'
            '<p class="leg-item"><span class="leg-sw" style="background:var(--paper);'
            'border:1px solid var(--line)"></span> 값 없음 — %d구: %s</p>%s'
            % (strip, labels, len(blanks), E(names), ratio_ruler_fig(watches)))


def _cap_legend_html(gus=None):
    """분양가상한제 층의 범례 — 적용 구 이름을 다 적는다(넷뿐이라 든다). 수가 0인
    줄은 안 낸다 — 자리만 먹는 「0구」 줄이 범례를 늘린다."""
    n_cap, n_no, n_null = _cap_counts(gus)
    z = ZONES.get('분양가상한제', {})
    names = '·'.join(g[:-1] if g.endswith('구') else g for g in _cap_names(gus))
    rows = []
    if n_cap:
        rows.append('<p class="leg-item"><span class="leg-sw" '
                    'style="background:var(--seq-4)"></span> 적용 — %d구: %s</p>'
                    % (n_cap, E(names)))
    if n_no:
        rows.append('<p class="leg-item"><span class="leg-sw" style="background:var(--paper);'
                    'border:1px solid var(--line)"></span> 미적용 — %d구</p>' % n_no)
    if n_null:
        rows.append('<p class="leg-item"><span class="leg-sw leg-hatch-line"></span> '
                    '확인 안 됨 — %d구</p>' % n_null)
    return (''.join(rows) + '<p class="leg-src">민간택지 기준입니다. 공공택지는 지역 지정과 '
            '상관없이 적용됩니다. 기준 %s · %s</p>'
            % (E(z.get('as_of') or '—'), _src_link(z.get('src'))))


_SUB_BIN_LABEL = ((0, '0건'), (1, '1건'), (2, '2건'), (3, '3~4건'), (4, '5건 이상'))


def _sub_legend_html(watches, gus=None):
    """청약 공고 층의 범례 — 구별 6개월 건수를 다섯 단으로 세어 한 줄에.
    카테고리 수가 0이면 그 칸은 안 낸다(적용 구가 없는 분양가상한제 범례와 같은
    규칙). 열쇠가 없으면(sub_gu 자체가 없으면) 빈 문자열 — 층 버튼도 같이 안 낸다."""
    sub_gu, sub_asof = _sub_gu_data(watches)
    if sub_gu is None:
        return ''
    counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for name in (gus or SEOUL_GU['gu']):
        n = len(sub_gu.get(name) or [])
        counts[_sub_bin(n) or 0] += 1
    parts = ['%s %d구' % (lbl, counts[b]) for b, lbl in _SUB_BIN_LABEL if counts[b]]
    line = '최근 6개월 공고 — ' + ' · '.join(parts)
    return ('<p class="leg-item">%s</p>'
            '<p class="leg-src">기준 %s · 청약홈(공공데이터포털) · '
            '주소로 구를 골라 놓친 공고가 있을 수 있음</p>'
            % (E(line), E(sub_asof or '—')))


def _zone_age_chip(as_of, today):
    """여섯 달 넘게 안 바뀐 기준일에는 나이를 붙인다. 머리의 「자료 기준 2026-07」과
    같은 무게로 읽히면 값의 나이가 열 배 차이 나는 것이 안 보인다."""
    a, b = _months(as_of), _months(today)
    if a is None or b is None or b - a < 6:
        return ''
    return ' <span class="t-old">%d개월 전 값</span>' % (b - a)


def _zone_banner(today, gus=None):
    """지정 현황 상태 배너 — 층 버튼 둘을 대신한다.

    25구가 전부 같은 범주라 지도로 그리면 서울 전체가 먹 단색이 되고, 클릭 한 번을
    내고 얻는 정보는 「전부 지정」 문장 하나였다. 수와 날짜는 손으로 안 적는다 —
    insights/watch/_zones.json 에서 센다. 구마다 갈리는 날 층을 되살린다(그때 색은
    --seq-4 / hatch / --surface 3단)."""
    gus = list(gus or SEOUL_GU['gu'])
    total = len(gus)
    n_all, n_part, n_none, n_null = _lth_counts(gus)
    lth_txt = ('%d구 전부 지정' % total if n_all == total
               else '전부 지정 %d구 · 일부 지정 %d구 · 미지정 %d구 · 확인 안 됨 %d구'
               % (n_all, n_part, n_none, n_null))
    cnt = _reg_counts(gus)
    reg_txt = ('%d구 둘 다 지정' % total if cnt['both'] == total
               else '둘 다 지정 %d구 · 하나만 %d구 · 둘 다 해제 %d구 · 확인 안 됨 %d구'
               % (cnt['both'], cnt['one'], cnt['none'], cnt['null']))
    # 분양가상한제는 층으로도 그리지만(구마다 갈린다) 「몇 구인가」는 배너가 낸다
    n_cap, _n_no, n_cnull = _cap_counts(gus)
    cap_txt = ('%d구 적용 (%s)'
               % (n_cap, '·'.join(g[:-1] if g.endswith('구') else g for g in _cap_names(gus)))
               if n_cap else '적용되는 구 없음')
    if n_cnull:
        cap_txt += ' · 확인 안 됨 %d구' % n_cnull
    rows = []
    for label, txt, z in (('토지거래허가구역', lth_txt, ZONES.get('토지거래허가구역', {})),
                          ('규제지역', reg_txt, ZONES.get('조정대상지역', {})),
                          ('분양가상한제', cap_txt, ZONES.get('분양가상한제', {}))):
        as_of = z.get('as_of') or '—'
        rows.append('<p class="zb-row"><span class="zb-k">%s</span>'
                    '<span class="zb-v">%s</span>'
                    '<span class="zb-m">기준 %s%s · %s</span></p>'
                    % (E(label), E(txt), E(as_of), _zone_age_chip(as_of, today),
                       _src_link(z.get('src'))))
    return ('<div class="zone-banner">%s<p class="leg-src">규제지역은 조정대상지역과 '
            '투기과열지구 둘을 함께 부르는 말입니다.</p></div>' % ''.join(rows))


# 이름을 안 다는 구. 도형이 작아 가운데 좌표(cx·cy)에 글자를 놓으면 이웃 라벨과
# 겹친다(check_fig 가 잡는다). 좌표는 cx·cy 만 쓰기로 했으므로 — 지시선을 새로
# 그리지 않는다 — 이 구들만 뺀다. 값이 있는 구는 여기 못 든다(그 이름은 반드시
# 보여야 한다).
LABEL_SKIP = ()


def _path_bbox(d):
    nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', d)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def _shift_d(d, dx, dy):
    """path d 의 좌표를 (dx, dy) 만큼 옮긴다 — 시·도 판의 viewBox 를 0,0 에서 시작하게
    한다(check_fig 가 원점 0 을 전제로 넘침을 잰다). d 는 M/L 절대 좌표 쌍뿐이다"""
    idx = [0]
    def _one(m):
        v = float(m.group(0)); i = idx[0]; idx[0] += 1
        return '%.1f' % (v + (dx if i % 2 == 0 else dy))
    return re.sub(r'-?\d+(?:\.\d+)?', _one, d)


def _gu_svg(gu_data, gus=None, suffix=''):
    """서울 25개 구 지도. 채움은 CSS 가 data-ratio-bin 으로 고른다 — 값 자체는
    여기서 속성으로 다 박아 두고 JS 는 아무 계산도 안 한다.

    2026-09-03 — 층(토허·규제) 두 개를 걷었다. 25구가 전부 같은 범주라 서울 전체가
    먹 단색으로 칠해졌고, 얻는 정보는 문장 하나였다. 지도 아래 상태 배너
    (_zone_banner)가 그 문장을 대신한다. 구마다 갈리는 날 층을 되살린다 — 그때
    색은 --seq-4 / hatch / --surface 3단으로 하고, 서울 전체를 먹으로 안 칠한다."""
    gus = list(gus or sorted(SEOUL_GU['gu']))
    # viewBox 는 그 시·도 구들의 경계 상자 — 서울과 성남을 한 판에 두면 성남이
    # 오른쪽 아래 귀퉁이에 작게 붙어 세 구를 손으로 못 고른다(2026-09-04). 좌표계
    # 자체는 원본(640×688.4) 그대로라 서울 판과 성남 판의 축척이 다르다 — 성남 판은
    # 글자·선을 축척만큼 줄여 서울 판과 같은 굵기로 보인다
    bx = [_path_bbox(SEOUL_GU['gu'][g]['d']) for g in gus]
    # 여백은 라벨 반폭(네 글자 11px ≈ 44px 의 절반)보다 커야 한다 — 가장자리 구(강동·중랑)
    # 이름이 판 밖으로 나가면 check_fig 가 「가로 넘침」으로 문다(2026-09-04)
    pad = 32
    x0, y0 = min(b[0] for b in bx) - pad, min(b[1] for b in bx) - pad
    x1, y1 = max(b[2] for b in bx) + pad, max(b[3] for b in bx) + pad
    vb = (0.0, 0.0, x1 - x0, y1 - y0)   # 좌표를 -x0,-y0 옮겨 원점 0 에서 시작
    # 기준은 서울 판의 폭이다 — 「서울 25구가 칸을 꽉 채울 때의 글자 11px·선 1px」이
    # 모든 판의 기준 축척이다. 판 원본(viewBox)이 화성~광주까지 넓어져도 서울 판은 이
    # 기준으로 그대로고, 그보다 넓은 판(경기)은 글자를 그만큼 키워 화면 크기를 맞춘다
    sb = [_path_bbox(SEOUL_GU['gu'][g]['d']) for g in SEOUL_GU['gu']
          if SEOUL_GU['gu'][g].get('sido', '서울') == '서울']
    seoul_w = (max(b[2] for b in sb) - min(b[0] for b in sb)) + 2 * pad
    # 좁은 판(성남만일 때)은 축척을 2.2배까지만 키운다 — 그 이상은 화면을 빈 종이로 채운다
    zoom = min(2.2, seoul_w / vb[2]) if vb[2] < seoul_w else 1.0
    width_pct = min(100.0, 100.0 * vb[2] / seoul_w * zoom)
    scale = (width_pct / 100.0) * seoul_w / vb[2]   # 기준 축척 대비 이 판의 배율
    lbl_px = 11.0 / scale
    stroke_px = 1.0 / scale
    # 「확인 안 됨」 칸의 옅은 빗금. 지금은 0구지만 지정 공고가 PDF 로만 나와
    # 못 받는 날이 있다 — 그때 빈 칸과 구분이 되어야 한다
    defs = ('<defs><pattern id="hatch-line" width="6" height="6" '
            'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="6" height="6" fill="var(--paper)"/>'
            '<path d="M0 0L0 6" stroke="var(--line)" stroke-width="2"/></pattern></defs>')
    paths, labels = [], []
    for name in gus:
        g = SEOUL_GU['gu'][name]
        e = gu_data[name]
        watched = bool(e['jeonse'])
        label = ('전세가율 %.1f%%' % e['jeonse']['cur']) if watched else '보고 있지 않은 구'
        cap_v = _cap_info(name)[0]
        attrs = ['class="gu"', 'data-gu="%s"' % E(name),
                 'data-sido="%s"' % E(g.get('sido', '서울')),
                 'data-cap="%s"' % ('yes' if cap_v is True
                                    else 'no' if cap_v is False else 'null')]
        sub_bin = _sub_bin((e.get('sub_cnt') or {}).get('value'))
        if sub_bin:
            attrs.append('data-sub-bin="%d"' % sub_bin)
        if watched:
            attrs += ['tabindex="0"', 'role="button"',
                      'data-ratio-bin="%d"' % _ratio_bin(e['jeonse']['cur'])]
        else:
            # 값 없는 구는 탭 순서에서 뺀다 — 키보드로 열여섯 번 지나가는 죽은
            # 정거장이 된다. 마우스·터치로는 그대로 패널이 뜬다
            attrs.append('tabindex="-1"')
        if e['slug']:
            attrs.append('data-slug="%s"' % E(e['slug']))
        attrs.append('aria-label="%s"' % E('%s · %s' % (name, label)))
        attrs.append('d="%s"' % _shift_d(g['d'], -x0, -y0))
        paths.append('<path %s/>' % ' '.join(attrs))
        if name in LABEL_SKIP and not watched:
            continue
        cls = 'gu-lbl' if watched else 'gu-lbl blank'
        labels.append('<text x="%.1f" y="%.1f" class="%s" text-anchor="middle" '
                      'font-size="%.1f">%s</text>'
                      % (g['cx'] - x0, g['cy'] - y0, cls, lbl_px, E(name)))
    return ('<svg class="seoul-map%s" data-layer="ratio" viewBox="%d %d %.1f %.1f" '
            'style="width:%.0f%%;--gu-stroke:%.2fpx">%s%s'
            '<g class="gu-labels">%s</g></svg>'
            % (suffix and ' map%s' % suffix, vb[0], vb[1], vb[2], vb[3], width_pct,
               stroke_px, defs, ''.join(paths), ''.join(labels)))


def _region_summary_html(watches):
    """패널 기본 상태 — 권역 셋 요약(area_cards 가 하던 계산을 그대로 쓴다). 각
    요약은 그 권역 상세로 가는 링크이고, data-gus 로 그 권역 구 셋을 실어 둔다 —
    요약에 마우스를 올리면 지도에서 그 셋이 강조된다."""
    items = []
    idx = _idx_rows(watches)
    for w in _live_areas(watches):
        metrics = [m for k, m in (w.get('metrics') or {}).items() if k.startswith('jeonse_ratio_')]
        if not metrics:
            continue
        avg = _avg_series(w)
        cur = avg[-1][1] if avg else sum(m['value'] for m in metrics) / len(metrics)
        d3 = (avg[-1][1] - avg[-4][1]) if len(avg) >= 4 else None
        sd = (w.get('metrics') or {}).get('supply_demand')
        if sd and sd.get('value') is not None:
            sdv = float(sd['value'])
            sd_txt = '수급 %s · %s' % (_fmt1(sdv),
                                      '사려는 사람이 더 많습니다' if sdv >= 100
                                      else '팔려는 사람이 더 많습니다')
        else:
            sd_txt = '수급 못 붙임'
        gu_list = AREAS.get(w['target'], {}).get('구', [])
        gus = ' '.join(gu_list)
        d1 = (avg[-1][1] - avg[-2][1]) if len(avg) >= 2 else None
        base1 = avg[-2][0] if len(avg) >= 2 else None
        gap = _idx_gap_line(_idx_avg_delta(idx, gu_list),
                            '석 달, 지수 · 구 %d곳 평균' % len(gu_list))
        items.append((cur, w, d1, base1, gus, sd_txt, gap))
    items.sort(key=lambda r: r[0])
    rows = ''.join(
        '<a class="rs" href="watch/%s.html" data-gus="%s">'
        '<p class="rs-k">%s · 전세가율 <span class="t-sub">(%s)</span></p>'
        '<p class="rs-n">%s%%</p>'
        '<p class="rs-line">%s</p>'
        '<p class="rs-v">%s</p>'
        '<p class="rs-line">%s</p>'
        '<p class="rs-line">%s</p>%s'
        '<span class="rs-cta">이 권역 자세히 보기</span></a>'
        % (w['slug'], E(gus), E(w['target']), E(_gu_short(w['target'])),
           _fmt1(cur),
           _delta_phrase('지난달', base1, d1, '%p') or '지난달 값이 없습니다',
           E(w.get('verdict') or '판단 없음'), E(_extra_sentence(cur)), E(sd_txt), gap)
        for cur, w, d1, base1, gus, sd_txt, gap in items)
    # 용어 풀이는 그 수가 처음 나오는 자리 바로 밑에 붙인다(별도 「용어」 절을 안 둔다).
    # 전세가율은 자(ratio_ruler_fig) 캡션이 이미 맡는다 — 여기서 또 적으면 같은
    # 문장이 한 화면에 두 번 나온다
    return rows + term_lines(watches, {'수급동향', '매매가격지수', '전세가격지수'})


LTH_LABEL = {'전부': '전부 지정', '일부': '일부 지정', '없음': '미지정'}


def _reg_row_text(e):
    """규제지역 한 줄 — 「조정대상지역·투기과열지구」 각각 지정/해제를 되풀이하지
    않고, 그 구에 지금 걸려 있는 이름만 나열한다(둘 다면 둘 다, 하나면 하나,
    아무 것도 안 걸리면 「해당 없음」). 어느 한쪽이라도 모르면 「확인 안 됨」."""
    if e['adj'] is None or e['hot'] is None:
        return '확인 안 됨'
    names = []
    if e['adj']:
        names.append('조정대상지역')
    if e['hot']:
        names.append('투기과열지구')
    return ' · '.join(names) if names else '해당 없음'


def _gu_meaning(cur, ds, dj):
    """구 하나의 뜻 한 줄. 앞은 전세가율이 어디쯤인가(지금 전세가 낫나, 매매가 가깝나),
    뒤는 석 달 매매·전세 지수 속도 차가 그 자리를 어디로 옮기고 있나. 둘 다 규칙이다 —
    「그래서 이게 무슨 의미냐」에 수가 아니라 문장으로 답하는 자리다(2026-09-03)."""
    if cur is None:
        return ''
    more = int(round(100 - cur))
    if cur < 50:
        base = '지금은 전세가 낫습니다 — 사려면 매매가의 %d%%를 더 얹어야 합니다' % more
        up, down = '전세의 이점이 줄고 있습니다', '전세의 이점이 커지고 있습니다'
    elif cur < 55:
        base = '전세와 매매가 비슷한 자리입니다 — 사려면 매매가의 %d%%를 더 얹습니다' % more
        up, down = '매매 쪽으로 기울고 있습니다', '전세 쪽으로 기울고 있습니다'
    else:
        base = '매매가 가깝습니다 — 매매가의 %d%%만 더 얹으면 됩니다' % more
        up, down = '매매가 더 가까워지고 있습니다', '매매 문턱이 다시 높아지고 있습니다'
    if ds is None or dj is None:
        return base + '.'
    g = dj - ds
    if g >= 0.5:
        how = '전세가 매매보다 빨리 올라' if dj > 0 else '매매가 전세보다 빨리 내려'
        return '%s. %s %s.' % (base, how, up)
    if g <= -0.5:
        how = '매매가 전세보다 빨리 올라' if ds > 0 else '전세가 매매보다 빨리 내려'
        return '%s. %s %s.' % (base, how, down)
    return base + '. 매매와 전세가 같이 움직여 자리는 그대로입니다.'


def _gu_panel_html(name, e):
    """구 하나의 패널 — 손을 대면(미리보기) 또는 누르면(고정) 이걸로 바뀐다.
    최대 9줄 — 데스크톱·모바일(시트) 어디서든 한 화면에 다 들어와야 한다
    (2026-09-03, 사용자 P0: 「내용이 한 화면에 다 들어오는 것도 아니고」).
    토허 detail 긴 문장은 여기 안 낸다 — 상세 페이지 「지정 내역」으로 옮겼다."""
    watched = bool(e['jeonse'] or e['sale'])
    h = ['<div class="gu-panel" data-panel="%s" hidden>'
         '<p class="gp-head"><span class="gp-name">%s</span>'
         '<button type="button" class="gp-close" aria-label="닫기">×</button></p>'
         % (E(name), E(name))]
    if watched and e['region']:
        h.append('<p class="gp-sub">%s · %s</p>' % (E(e['region']), E(e['region_view'])))
    else:
        h.append('<p class="gp-sub">보고 있지 않은 구</p>')
    if watched and e['jeonse']:
        ds, dj = e.get('gap', (None, None))
        mean = _gu_meaning(e['jeonse']['cur'], ds, dj)
        if mean:
            h.append('<p class="gp-mean">%s</p>' % E(mean))
    if watched:
        if e['jeonse']:
            j = e['jeonse']
            h.append('<p class="gp-row"><span class="gp-lbl">전세가율</span><b>%.1f%%</b> '
                     '<span class="gp-d">%s · %s</span></p>'
                     % (j['cur'], _delta_phrase('지난달', j['a1'], j['d1'], '%p'),
                        _delta_phrase('석 달', j['a3'], j['d3'], '%p')))
        if e['sale']:
            sv = e['sale']
            h.append('<p class="gp-row"><span class="gp-lbl">매매가격지수</span><b>%.2f</b> '
                     '<span class="gp-d">%s · %s</span></p>'
                     % (sv['cur'], _delta_phrase('지난달', sv['a1'], sv['d1'], 'pt'),
                        _delta_phrase('석 달', sv['a3'], sv['d3'], 'pt')))
        if e.get('jeonse_idx'):
            jv = e['jeonse_idx']
            h.append('<p class="gp-row"><span class="gp-lbl">전세가격지수</span><b>%.2f</b> '
                     '<span class="gp-d">%s · %s</span></p>'
                     % (jv['cur'], _delta_phrase('지난달', jv['a1'], jv['d1'], 'pt'),
                        _delta_phrase('석 달', jv['a3'], jv['d3'], 'pt')))
        say = _read_gap(*e.get('gap', (None, None)))
        if say:
            h.append('<p class="gp-row"><span class="gp-d">%s</span></p>' % E(say))
        if e['sd'] and e['sd'].get('value') is not None:
            sdv = float(e['sd']['value'])
            h.append('<p class="gp-row"><span class="gp-lbl">수급동향</span><b>%s</b> · %s '
                     '<span class="t-sub">(%s)</span></p>'
                     % (_fmt1(sdv), '사려는 사람이 많다' if sdv >= 100 else '팔려는 사람이 많다',
                        E(e['sd'].get('area') or '')))
    if e['lth_value'] is not None:
        lth_as_of = ZONES.get('토지거래허가구역', {}).get('as_of') or '—'
        h.append('<p class="gp-row"><span class="gp-lbl">토지거래허가구역</span>%s · %s 기준</p>'
                 % (E(LTH_LABEL.get(e['lth_value'], e['lth_value'])), E(lth_as_of)))
    reg_as_of = ZONES.get('조정대상지역', {}).get('as_of') or '—'
    h.append('<p class="gp-row"><span class="gp-lbl">규제지역</span>%s · %s 기준</p>'
             % (E(_reg_row_text(e)), E(reg_as_of)))
    # 분양가상한제 — 규제지역과 별개 지정이라 같은 구에서 답이 갈린다. 적용 주택은
    # 재당첨 제한이 10년으로 가장 길다(청약 제도 줄의 「당첨 뒤 제한」 표). gp-cap
    # 로 한 덩이를 묶는다 — 분양가상한제 층을 켰을 때 이 덩이가 CSS order:-1 로
    # 맨 위(머리 다음)로 올라간다(2026-09-04, 「누른 층과 다른 게 먼저 보인다」).
    cap_v, cap_d = _cap_info(name)
    cap_as_of = ZONES.get('분양가상한제', {}).get('as_of') or '—'
    cap_txt = ('적용 · %s 기준' % cap_as_of if cap_v is True
               else '미적용' if cap_v is False else '확인 안 됨')
    cap_h = ['<p class="gp-row"><span class="gp-lbl">분양가상한제</span>%s</p>' % E(cap_txt)]
    # 원 지정이 동 단위였는데 그 목록을 못 열었다 — 구 전역으로 읽으면 안 된다.
    # 상세 문장을 40자에서 자르던 것을 걷었다(2026-09-04, 「분양가상한제 층을 켜고
    # 구를 누르면 잘린 문장이 먼저 나온다」) — 뜻이 서는 한 문장으로 적는다
    if cap_d and '확인 못 함' in cap_d:
        cap_h.append('<p class="gp-row"><span class="gp-d" style="font-size:12.5px">'
                     '원 지정이 동 단위라 구 전체인지 일부 동인지는 확인 안 됨</span></p>')
    h.append('<div class="gp-cap">%s</div>' % ''.join(cap_h))
    # 청약홈 최근 공고 — 이 구 것(권역이 아니라). 열쇠가 없어 어댑터가 못 냈으면
    # (sub_cnt 없음) 덩이 자체를 안 낸다. 값이 있으면 0건이어도 낸다 — 「못 봤다」와
    # 「0건이다」는 다른 상태다. gp-pblanc 로 한 덩이를 묶는다 — 청약 공고 층을
    # 켰을 때 이 덩이가 CSS order:-1 로 맨 위로 올라간다(위 gp-cap 과 같은 이유).
    sc = e.get('sub_cnt')
    if sc is not None:
        items = e.get('sub_items') or []
        if sc['value'] == 0:
            # 값 없음 문구지 자리표시가 아니다 — 청약 공고 층을 켠 사람이 이 구를
            # 골랐을 때 물은 것(공고가 있나)에 대한 답이 이 한 줄이다
            pb_h = ['<p class="gp-row">이 구엔 최근 6개월 공고가 없습니다 '
                    '<span class="t-sub">· %s 기준</span></p>' % E(sc['as_of'])]
        else:
            n_open = sum(1 for it in items if _sub_status(it, _TODAY) == '접수 중')
            open_txt = (' <span class="t-sub">· 지금 접수 중 %d건</span>' % n_open) if n_open else ''
            pb_h = ['<p class="gp-row"><span class="gp-lbl">최근 공고</span>%d건 '
                    '<span class="t-sub">· 6개월 · %s 기준</span>%s</p>'
                    % (sc['value'], E(sc['as_of']), open_txt)]
            for it in items[:3]:
                nm = E(it.get('name') or '—')
                # 단지명은 그 건 자신의 앵커로 건다(청약공고_스펙 추가 §2) — 청약홈
                # 실제 링크는 여기서 안 쓴다(그 건 안 「청약홈에서 보기 →」에만 쓴다)
                if it.get('id'):
                    nm = ('<a href="watch/청약 공고.html#p-%s">%s</a>' % (E(it['id']), nm))
                rate_txt = (' · 1순위 %s:1' % E(it['rate1'])) if it.get('rate1') else ''
                st = _sub_status(it, _TODAY)
                chip = ('<span class="tag %s gp-chip">%s</span>'
                        % (_SUB_STATUS_CLS.get(st, 't-none'), E(st)))
                pb_h.append('<p class="gp-row gp-sub-item">%s · 접수 %s%s %s</p>'
                            % (nm, E(_mmdd(it.get('apply'))), rate_txt, chip))
            if len(items) > 3:
                pb_h.append('<p class="gp-row gp-sub-item t-sub">+%d건</p>' % (len(items) - 3))
        # 페이지에 구 필터가 없으므로 이 구 이름으로 걸러 보내지 않는다 — 전체
        # 목록으로 돌린다(청약공고_스펙 §5)
        pb_h.append('<a class="gp-more" href="watch/청약 공고.html">이 구 공고 전부 보기 →</a>')
        h.append('<div class="gp-pblanc">%s</div>' % ''.join(pb_h))
    if watched and e['slug']:
        h.append('<a class="gp-more" href="watch/%s.html">자세히 →</a>' % e['slug'])
    h.append('</div>')
    return ''.join(h)


def _read_move(d):
    """변화를 읽는 말. 규칙만 쓴다 — 0.10%p 를 넘게 움직였으면 방향을 말하고,
    그 안이면 「사실상 제자리」다. 문턱이 아니라 반올림 잡음과 뜻 있는 움직임을
    가르는 선이다(그 선을 넘었다고 뭘 하라는 말은 안 한다)."""
    if d is None:
        return '지난달 값이 없습니다'
    if d >= 0.10:
        return '매매에 가까워졌습니다'
    if d <= -0.10:
        return '전세 쪽으로 기울었습니다'
    return '사실상 제자리입니다'


def changed_section(watches, sido='서울', suffix=''):
    """지난달과 달라진 것 — 이 장을 매달 다시 여는 이유가 이것 하나다.

    지도 왼쪽 아래 빈 칸에 선다(지도 그림이 그 칸의 위쪽 절반만 쓴다). 값이 없으면
    빈 절을 그대로 낸다 — 빈 절이 델타를 감추는 것보다 낫다."""
    rows, base = [], None
    idx = _idx_rows(watches)
    for w in sorted(_live_areas(watches), key=lambda w: w['target']):
        if _area_sido(w['target']) != sido:
            continue
        avg = _avg_series(w)
        if len(avg) < 2:
            continue
        prev, cur = avg[-2][1], avg[-1][1]
        base = max(base or avg[-2][0], avg[-2][0])
        # 둘째 줄 — 전세가율만 보면 전세가 빠진 건지 매매가 오른 건지 모른다.
        # 이 절은 지난달 기준이라 지수 Δ 도 지난달치를 쓴다 — 여기만 석 달치를
        # 쓰면 윗줄과 아랫줄이 다른 기간을 말해 서로 어긋나 보인다
        ds, dj = _idx_avg_delta(idx, AREAS.get(w['target'], {}).get('구', []), back=1)
        second = ('<span class="chg-2">매매 %s · 전세 %s — %s</span>'
                  % (_delta_num(ds, 'pt'), _delta_num(dj, 'pt'), E(_read_gap(ds, dj)))
                  if _read_gap(ds, dj) else '')
        rows.append('<p class="chg-row"><span class="chg-k">%s 전세가율</span>'
                    '<span class="chg-v">%s → %s %s</span>'
                    '<span class="chg-say">%s</span>%s</p>'
                    % (E(w['target']), _fmt1(prev), _fmt1(cur),
                       _delta_num(cur - prev, '%p'), E(_read_move(cur - prev)), second))
    by = _laws_grouped(watches)
    changed = [n for n, e in by.items() if _law_state(e) == '걸림']
    law_txt = ('바뀐 법·고시 없음 (%d개 중 0개)' % len(by) if not changed
               else '바뀐 법·고시 %d개 (%d개 중) — %s'
               % (len(changed), len(by), ' · '.join(sorted(changed))))
    rows.append('<p class="chg-row"><span class="chg-k">제도</span>'
                '<span class="chg-v">%s</span></p>' % E(law_txt))
    title = '지난달(%s)과 달라진 것' % base if base else '지난달과 달라진 것'
    return ('<div class="changed" id="changed%s"><p class="chg-t">%s</p>%s</div>'
            % (suffix, E(title), ''.join(rows)))


# 바닐라 JS — 지도 호버=미리보기/누르기=고정(선택 모델
# 하나로, 2026-09-03) · 권역 요약 호버(지도 강조만). 상세 이동은 패널 안
# 「자세히 →」 링크로만 한다 — path 클릭은 더는 페이지를 안 옮긴다(모바일에서
# 탭=이동이면 값을 볼 길이 없다는 사용자 지적). 값은 전부 생성 때 HTML 에
# 이미 있다 — 여기서는 hidden·class 토글만 한다(계산 없음).
_MAP_JS = """<script>
/* 지도가 시·도마다 하나라(서울·경기) 상자(.hero)마다 따로 묶는다 — 한 상자의
   구 선택이 다른 상자 패널을 건드리면 안 된다(2026-09-04) */
Array.from(document.querySelectorAll('.hero')).forEach(function(root){
var svg=root.querySelector('.seoul-map');
if(!svg)return;
var gus=Array.from(svg.querySelectorAll('.gu'));
var panels=Array.from(root.querySelectorAll('.gu-panel'));
var rss=Array.from(root.querySelectorAll('.rs'));
var locked=null;
/* 기본 패널(권역 셋)은 절대 안 감춘다 — 구 패널은 그 위에 얹힌다. 견주는 것이
   화면에서 서로를 밀어내면 「어느 권역이 나은가」에 답할 수가 없다 */
var showPanel=function(n){panels.forEach(function(p){
  if(p.dataset.panel==='default')return;p.hidden=p.dataset.panel!==n;});};
var clearHi=function(){gus.forEach(function(g){g.classList.remove('gu-hover','gu-dim');});};
var highlight=function(names){gus.forEach(function(g){
  var on=names.indexOf(g.dataset.gu)>-1;
  g.classList.toggle('gu-hover',on);g.classList.toggle('gu-dim',!on);});};
var apply=function(n){if(n){highlight([n]);}else{clearHi();}showPanel(n||'default');};
gus.forEach(function(g){
  var n=g.dataset.gu;
  g.addEventListener('mouseenter',function(){apply(n);});
  g.addEventListener('focus',function(){apply(n);});
  g.addEventListener('mouseleave',function(){apply(locked);});
  g.addEventListener('blur',function(){apply(locked);});
  g.addEventListener('click',function(){locked=(locked===n)?null:n;apply(locked);});
  /* ARIA 버튼은 Enter 와 Space 둘 다 받아야 한다. Space 를 안 막으면 한 화면
     내려가면서 포커스가 지도 밖으로 나간다 */
  g.addEventListener('keydown',function(ev){
    if(ev.key==='Enter'||ev.key===' '||ev.key==='Spacebar'){
      ev.preventDefault();locked=(locked===n)?null:n;apply(locked);}});
});
rss.forEach(function(a){
  var names=a.dataset.gus.split(' ');
  a.addEventListener('mouseenter',function(){highlight(names);});
  a.addEventListener('focus',function(){highlight(names);});
  a.addEventListener('mouseleave',clearHi);
  a.addEventListener('blur',clearHi);
});
Array.from(root.querySelectorAll('.gp-close')).forEach(function(b){
  b.addEventListener('click',function(){locked=null;apply(null);});
});
document.addEventListener('click',function(e){
  if(!locked)return;
  if(e.target.closest('.gu,.gu-panel,.rs'))return;
  locked=null;apply(null);
});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&locked){locked=null;apply(null);}
});
/* 층 전환 — <svg> 와 .mappanel 양쪽에 data-layer 를 박고 채움·순서는 CSS 가 고른다.
   패널 안 값 자체는 안 건드린다: 「강남구가 지금 어떤가」는 층과 무관하게 같은 답이다.
   .mappanel 쪽 data-layer 는 그 층에 맞는 덩이(gp-cap·gp-pblanc)를 CSS order 로
   맨 위에 올리는 데만 쓴다(2026-09-04) — 「청약 공고」층을 켜고 구를 골랐는데
   전세가율부터 나오던 것을 고친 자리다 */
var mappanel=root.querySelector('.mappanel');
Array.from(root.querySelectorAll('.layer-btn')).forEach(function(b){
  b.addEventListener('click',function(){
    svg.setAttribute('data-layer',b.dataset.layer);
    if(mappanel)mappanel.setAttribute('data-layer',b.dataset.layer);
    Array.from(root.querySelectorAll('.layer-btn')).forEach(function(x){
      var on=(x===b);x.classList.toggle('is-on',on);
      x.setAttribute('aria-pressed',on?'true':'false');});
    Array.from(root.querySelectorAll('.map-legend')).forEach(function(x){
      x.hidden=x.dataset.legend!==b.dataset.layer;});
  });
});
});
</script>"""

# 최상위 탭 — 서울|경기. 한 번에 한 시·도만 보인다(고르는 계층은 이것 하나다).
# 둘 다 DOM 에 있고 hidden 만 토글한다 — 계산 없음. 주소에 #경기 가 있으면 그 탭으로
_SIDO_JS = """<script>
(function(){
var tabs=Array.from(document.querySelectorAll('.sido-tab'));
var blocks=Array.from(document.querySelectorAll('.sido-block'));
if(!tabs.length)return;
var pick=function(sido){
  tabs.forEach(function(t){var on=t.dataset.sido===sido;
    t.classList.toggle('is-on',on);t.setAttribute('aria-selected',on?'true':'false');});
  blocks.forEach(function(b){b.hidden=b.dataset.sido!==sido;});
};
tabs.forEach(function(t){t.addEventListener('click',function(){pick(t.dataset.sido);});});
var h=decodeURIComponent(location.hash||'').slice(1);
pick(tabs.some(function(t){return t.dataset.sido===h;})?h:tabs[0].dataset.sido);
})();
</script>"""

# 절 바로가기의 현재 위치 표시. 본 장과 상세가 같은 조각을 쓴다 — 나브 꼴이 같은데
# 한쪽만 지금 절을 알려 주면 그것대로 헷갈린다.
_JUMP_JS = """<script>
(function(){
var links=Array.from(document.querySelectorAll('.jump a'));
if(!links.length)return;
// 누르면 스크롤만 하고 주소에 #앵커를 안 남긴다 — 남기면 새로고침이 그 절로 뛴다.
// #p-<id> 는 예외다(청약공고_스펙 추가 §2) — 그 공고를 가리키는 공유용 주소라
// 지우면 :target 강조가 사라지고 새로고침·다시 열기에서 그 건으로 못 돌아간다
var strip=function(){if(location.hash&&location.hash.indexOf('#p-')!==0&&history.replaceState){
  history.replaceState(null,'',location.pathname+location.search);}};
var smooth=!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
links.forEach(function(a){a.addEventListener('click',function(ev){
  var t=document.getElementById(a.getAttribute('href').slice(1));
  if(!t)return; ev.preventDefault();
  t.scrollIntoView({behavior:smooth?'smooth':'auto',block:'start'}); strip();});});
window.addEventListener('load',function(){setTimeout(strip,50);});
if(!window.IntersectionObserver)return;
var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a;});
var secs=Object.keys(map).map(function(id){return document.getElementById(id);})
  .filter(Boolean);
var seen={};
var io=new IntersectionObserver(function(es){
  es.forEach(function(e){seen[e.target.id]=e.isIntersecting;});
  var here=null;
  secs.forEach(function(s){if(seen[s.id]&&!here)here=s.id;});
  links.forEach(function(a){
    a.classList.toggle('is-here',here!==null&&a.getAttribute('href')==='#'+here);});
},{rootMargin:'-60px 0px -55% 0px'});
secs.forEach(function(s){io.observe(s);});
})();
</script>"""


def seoul_map_section(watches, asof, checked, sido='서울', suffix=''):
    """지도 히어로 — 왼쪽 지도(58%, 데스크톱은 sticky) · 오른쪽 패널(42%, 기본은
    권역 셋 요약). 구를 손대면(호버) 미리보기, 누르면(클릭·Enter) 그 구로
    고정된다. 상세 이동은 패널 안 「자세히 →」로만 한다. 값은 전부
    insights/watch/_seoul_gu.json·_zones.json·metrics 에서 — 지정 현황이 셋 다
    「전부」라도 범례 수는 그 데이터에서 센다.

    풀이 셋(전세가율·매매가격지수·수급동향)은 패널이 아니라 지도 캡션 줄로
    내렸다(2026-09-03) — 권역 요약+범례+자+풀이가 패널 안에 다 있으면 데스크톱
    800px 를 넘는다."""
    gus = _sido_gus(sido)
    gu_data = _gu_map_data(watches)
    svg = _gu_svg(gu_data, gus, suffix)
    # 구 패널이 기본 패널보다 앞에 선다 — 골랐을 때 위에 얹히고 권역 요약은 그 아래
    # 그대로 남는다(덮으면 견줄 수가 없다). 권역 요약은 그 시·도 것만
    sido_ws = _sido_watches(watches, sido)
    panels = ''.join(_gu_panel_html(name, gu_data[name]) for name in gus) + \
             ('<div class="gu-panel" data-panel="default">%s</div>'
              % _region_summary_html(sido_ws))
    cap = ('<p>지도 원본 southkorea/seoul-maps(서울)·southkorea/southkorea-maps(경기) · '
           '값 기준 %s</p>' % E(asof))
    # 층 — 구마다 갈리는 값만 층이다. 토허·규제는 25구가 전부 같은 범주라 층에서
    # 내려 배너 문장으로 갔고, 분양가상한제는 넷과 스물하나로 갈려 층이 된다.
    # 청약 공고는 열쇠가 있을 때만(sub_gu is not None) 셋째 층으로 더한다 —
    # 값이 없으면 버튼 자체를 안 낸다
    sub_gu, _sub_asof = _sub_gu_data(watches)
    # 청약 공고 층이 첫 버튼이자 기본 층이다(2026-09-04 사용자 지시 「지도에서는 청약
    # 공고가 가장 앞에」) — 값이 없으면(sub_gu None) 전세가율이 기본으로 돌아간다
    first = 'sub' if sub_gu is not None else 'ratio'
    def _btn(layer, label):
        on = layer == first
        return ('<button type="button" class="layer-btn%s" data-layer="%s" aria-pressed="%s">%s</button>'
                % (' is-on' if on else '', layer, 'true' if on else 'false', label))
    def _leg(layer, body):
        return '<div class="map-legend" data-legend="%s"%s>%s</div>' % (layer, '' if layer == first else ' hidden', body)
    btn_list, legend_list = [], []
    if sub_gu is not None:
        btn_list.append(_btn('sub', '청약 공고'))
        legend_list.append(_leg('sub', _sub_legend_html(watches, gus)))
    btn_list += [_btn('ratio', '전세가율'), _btn('cap', '분양가상한제')]
    legend_list += [_leg('ratio', _ratio_legend_html(sido_ws, gus)), _leg('cap', _cap_legend_html(gus))]
    btns = '<div class="layer-btns" role="group" aria-label="지도 층">%s</div>' % ''.join(btn_list)
    head = ('서울 25구 — 어디에 청약 공고가 있나, 전세가율은 어디쯤인가' if sido == '서울'
            else '경기 — 성남·동탄·광교·평촌·남한산성, 어디에 청약 공고가 있나, 전세가율은 어디쯤인가')
    return (
        '<p class="hero-t">%s</p>%s'
        '<div class="maprow">'
        '<div class="mapcol">'
        '<figure class="map-fig">%s<figcaption>%s</figcaption></figure>%s%s</div>'
        '<div class="mappanel" data-layer="%s" aria-live="polite" aria-atomic="true">%s%s'
        '</div></div>'
        % (E(head), btns, svg.replace('data-layer="ratio"', 'data-layer="%s"' % first, 1),
           cap, _zone_banner(checked, gus), changed_section(watches, sido, suffix), first,
           panels, ''.join(legend_list)))


# 은어 넷 — 저장소 안에서만 통하는 말이 화면에 그대로 나가면 안 된다. 「걸림」·「근접」은
# 칩으로 남기되(뜻을 subtitle 에 한 번 적는다), 나머지 넷은 절 제목·목록 이름·열
# 이름으로 못 쓴다.
_JARGON = ('때 자', '<th>성격</th>', '<th>언제 것</th>')

# 2026-09-02 「조건 다 없애」 이후의 규약 — 트리거 문턱 UI(걸림·근접 칩, 조건
# 문장, 「걸리면」 열)가 화면에서 완전히 걷혔는지 검사한다. 「걸림」「근접」「조건」
# 「걸리면」 낱말 자체를 통째로 금지하지는 않는다 — md 산문·verdict 에 정당하게
# 나온다(예: 임대차 제도 줄의 verdict 「전세 계약의 조건」, 법 표의 「같은가」
# 열은 법 개정 여부를 걸림/같다로 말한다 — 이건 다른 개념이라 남긴다). 대신 옛
# 트리거 UI 만 만들던 자국(칩 클래스·범례·표 열 머리·백테스트 문구)의 부재로 잰다.
# 표 열 이름(<th>조건</th>·<th>걸리면</th>)으로 재던 것은 걷었다 — 청약 줄의
# 「1순위 요건」·「당첨 뒤 제한」 표가 「조건」을 정당한 열 이름으로 쓴다. 옛 트리거
# UI 는 클래스 자국(칩·범례)으로만 잰다. 절 제목 「조건」도 허용이다.
_COND_CHROME = ('class="chip-legend"', 'class="tag t-near"', 'class="tag t-clear"')
_HIST_RE = re.compile(r'이력\s*\d+(개월|달|년|분기|점)\s*중\s*\d+번')


def _assert_no_condition_chrome(html, where):
    for term in _COND_CHROME:
        assert term not in html, '규약 위반(%s): 옛 조건 UI 자국 "%s" 가 남아 있다' % (where, term)
    assert not _HIST_RE.search(html), \
        '규약 위반(%s): 「이력 N개월 중 k번」 백테스트 문구가 남아 있다' % where


def check_ui(html, watches):
    """본 장의 규약. 아카이브 규약(check_ui)에서 나온 장이라 규약이 없어지면 안 된다.

    2026-09-02 네 번째 개정 — 트리거 조건(문턱)은 글쓴이 개인 기준이라 독자에게는
    뜻이 없다(「조건 다 없애」). 걸림·근접 칩과 조건 문장의 부재를 잰다.

    2026-09-03 다섯 번째 개정 — 지도가 첫 화면이다. 「권역」·「바뀐 것」 앵커와
    그 절은 없어졌고(지도 히어로가 흡수), figure 예산이 셋(지도·전세가율 자·
    자료 기준 자)으로 늘었다."""
    assert 'is-fold' not in html and 'uc-caret' not in html, \
        '규약 위반: 접는 것을 두지 않는다 — 열면 다 보여야 한다'
    assert 'class="stile' not in html, \
        '규약 위반: 타일을 두지 않는다 — 고르는 계층은 탭 하나다'
    assert 'class="line"' not in html, \
        '규약 위반: 줄 상세는 본 장에 없다 — watch/<슬러그>.html 로 옮겼다'
    # 2026-09-04 여섯 번째 개정 — 최상위가 서울|경기 탭이다. 시·도 상자마다
    # 분양 → 지도 → 달라진 것 → 보고 있는 것 순서, 제도는 그 둘보다 뒤(탭 밖).
    assert html.count('class="sido-block"') == 2, '규약 위반: 시·도 상자는 서울·경기 둘이다'
    assert 'class="sido-tabs"' in html and html.count('<button type="button" class="sido-tab') == 2, \
        '규약 위반: 최상위 탭(서울|경기)이 없다 — 고르는 계층은 이것 하나다'
    at_policy = html.find('id="policy"')
    for _sido, sfx in SIDOS:
        at_sub = html.find('id="subscription%s"' % sfx)
        at_map = html.find('id="map%s"' % sfx)
        at_changed = html.find('id="changed%s"' % sfx)
        at_lines = html.find('id="lines%s"' % sfx)
        assert 0 < at_sub < at_map < at_changed < at_lines < at_policy, \
            ('규약 위반(%s): 분양 → 지도 → 달라진 것 → 보고 있는 것 → 제도 순서여야 한다'
             % _sido)
        # 정비사업 절은 어댑터가 값을 냈을 때만 선다 — 서면 달라진 것과 보고 있는 것 사이
        at_rb = html.find('id="rebuild%s"' % sfx)
        if _rebuild_data(watches)[0] is not None:
            assert at_changed < at_rb < at_lines, \
                '규약 위반(%s): 정비사업 절은 달라진 것 다음, 보고 있는 것 앞이다' % _sido
        else:
            assert at_rb < 0, '규약 위반(%s): 값 없는 정비사업 절을 냈다' % _sido
    # 층은 구마다 갈리는 값만 그린다. 25구가 전부 같은 범주인 것(토허·규제)은 지도가
    # 아니라 배너 문장이고, 갈리는 것(전세가율·분양가상한제·청약 공고)만 버튼이 된다.
    # 청약 공고는 청약홈 열쇠가 있을 때만 셋째 버튼으로 더한다 — 값이 없으면(sub
    # 데이터 없음) 버튼 자체를 안 낸다(2026-09-04, 「값이 없으면 버튼 자체를 안
    # 낸다」). 「둘」로 고정했던 단언을 「데이터가 있으면 셋, 없으면 둘」로 고쳤다.
    assert 'class="layer-btn' in html and 'aria-pressed' in html, \
        '규약 위반: 층 버튼에 aria-pressed 가 없다 — 어느 층이 켜졌는지가 안 전해진다'
    # <button ...class="layer-btn 으로만 센다 — 감싼 상자 class="layer-btns"(복수)도
    # "layer-btn" 을 부분 문자열로 품어 그냥 세면 하나 더 잡힌다
    n_btn = html.count('<button type="button" class="layer-btn') // 2   # 지도가 둘
    assert html.count('class="layer-btns" role="group" aria-label="지도 층"><button type="button" class="layer-btn is-on" data-layer="sub"') == 2         or 'data-legend="sub"' not in html,         '규약 위반: 청약 공고 데이터가 있으면 그 층이 첫 버튼이자 기본 층이어야 한다 (2026-09-04)'
    # 청약 공고 층의 존재는 svg 안 data-sub-bin 이 아니라 범례 상자(data-legend="sub")
    # 로 잰다 — CSS 규칙(.seoul-map[data-layer="sub"] …)은 값과 무관하게 항상
    # <style> 안에 있어 data-layer="sub" 라는 문자열 자체는 늘 참이다
    if 'data-legend="sub"' in html:
        assert n_btn == 3, \
            ('규약 위반: 청약 공고 데이터가 있으면 지도 층 버튼은 셋(전세가율·'
             '분양가상한제·청약 공고)이어야 한다 (%d개)' % n_btn)
    else:
        assert n_btn == 2, \
            ('규약 위반: 청약 공고 데이터가 없으면 지도 층 버튼은 둘(전세가율·'
             '분양가상한제)이어야 한다 — 값 없는 버튼을 냈다 (%d개)' % n_btn)
    assert html.count('class="zone-banner"') == 2, \
        '규약 위반: 지정 현황 상태 배너가 없다 — 층에서 내린 값이 문장으로 서야 한다'
    assert '값이 언제 것인가' in html, '규약 위반: 자료 기준 자가 없다 — 값의 나이를 먼저 보인다'
    n_fig = html.count('<figure')
    assert n_fig == 5, \
        ('규약 위반: 본 장의 <figure 는 (지도 + 전세가율 자)×시·도 둘 + 자료 기준 자 '
         '다섯이어야 한다 (%d개)' % n_fig)
    # 본 장의 표는 「청약 — 조건」 절 안에만 둔다. 나머지는 전부 상세(watch/)로
    # 옮겼는데, 청약 조건은 「지금 신청할 수 있나」에 바로 답하는 값이라 한 번 더
    # 열게 하지 않는다 — 그 예외가 다른 절로 새지 않게 자리까지 잰다
    n_tbl = html.count('<table')
    at_sub = html.find('id="subscription-cond"')
    inside = html[at_sub:html.find('id="lines-policy"')] if at_sub > 0 else ''
    # 조건 표 셋 + 청약홈 공고 표 하나 — 넷까지. 전부 #subscription 안이어야 한다
    assert n_tbl <= 4, '규약 위반: 본 장의 표는 넷 이하여야 한다 (%d개)' % n_tbl
    assert n_tbl == inside.count('<table'), \
        '규약 위반: 본 장의 표는 「청약 — 조건」 절 안에만 둔다'
    assert 'scratchpad/' not in html.split('<footer>')[-1].split('</footer>')[0], \
        '규약 위반: 푸터에 내부 파일 경로를 내지 않는다 — 주석으로 내린다'
    for term in _JARGON:
        assert term not in html, '규약 위반: 은어 "%s" 가 화면에 남아 있다' % term
    assert '>줄</p>' not in html and '>줄</a>' not in html, \
        '규약 위반: 「줄」을 절 제목·목록 이름으로 썼다'
    _assert_no_condition_chrome(html, '본 장')
    # 도해 배치는 눈이 아니라 검사기가 본다. 자는 점이 몰리면 글자가 겹치는데
    # 화면을 못 볼 때는 그걸 알 길이 없다 — 실제로 다섯 쌍이 겹친 채로 나갈 뻔했다
    sys.path.insert(0, HERE)
    import check_fig
    for m in re.finditer(r'<svg[^>]*>.*?</svg>', html, re.S):
        bad = check_fig.hits(m.group(0))
        assert not bad, '규약 위반: 도해 배치 — %s' % ' · '.join(bad)


def check_detail_ui(watches):
    """줄 상세 페이지의 규약. 본 장에서 걷어낸 검사(도해 배치·은어·조건 UI 자국)를
    상세 파일 전부로 돌린다 — 옮겼다고 검사까지 놓치면 안 된다.

    「기준」 표기 단언은 이제 표(<th>기준</th>, 「값으로 오는 것」과 함께 삭제)가
    아니라 머리 수치 띠(stat_strip 의 class="stat-m")에 있는지로 잰다."""
    sys.path.insert(0, HERE)
    import check_fig
    for w in watches:
        path = os.path.join(WATCH_DIR, w['slug'] + '.html')
        assert os.path.exists(path), '규약 위반: 줄 상세 파일이 없다 — %s' % w['slug']
        html = io.open(path, encoding='utf-8').read()
        for m in re.finditer(r'<svg[^>]*>.*?</svg>', html, re.S):
            bad = check_fig.hits(m.group(0))
            assert not bad, '규약 위반(%s): 도해 배치 — %s' % (w['slug'], ' · '.join(bad))
        n = sum(1 for t in w['triggers']
                if t['kind'] == wl.KIND_VALUE and t['value'] is not None)
        assert re.search(r'class="stat-m">[^<]*기준 ', html) or n == 0, \
            '규약 위반(%s): 값을 내면서 머리 수치 띠에 「기준」이 없다' % w['slug']
        for term in _JARGON:
            assert term not in html, '규약 위반(%s): 은어 "%s" 가 남아 있다' % (w['slug'], term)
        _assert_no_condition_chrome(html, w['slug'])
    law_path = os.path.join(WATCH_DIR, '제도.html')
    assert os.path.exists(law_path), '규약 위반: watch/제도.html 이 없다'
    law_html = io.open(law_path, encoding='utf-8').read()
    for term in _JARGON:
        assert term not in law_html, '규약 위반(제도): 은어 "%s" 가 남아 있다' % term
    _assert_no_condition_chrome(law_html, '제도')
    # check_detail_ui 는 watches 의 슬러그만 도니 청약 공고.html 은 여기서 명시로
    # 더한다(청약공고_스펙 §4 구현 주의).
    sub_path = os.path.join(WATCH_DIR, '청약 공고.html')
    assert os.path.exists(sub_path), '규약 위반: watch/청약 공고.html 이 없다'
    sub_html = io.open(sub_path, encoding='utf-8').read()
    for m in re.finditer(r'<svg[^>]*>.*?</svg>', sub_html, re.S):
        bad = check_fig.hits(m.group(0))
        assert not bad, '규약 위반(청약 공고): 도해 배치 — %s' % ' · '.join(bad)
    for term in _JARGON:
        assert term not in sub_html, '규약 위반(청약 공고): 은어 "%s" 가 남아 있다' % term
    rb_path = os.path.join(WATCH_DIR, '정비사업 현황.html')
    assert os.path.exists(rb_path), '규약 위반: watch/정비사업 현황.html 이 없다'
    rb_html = io.open(rb_path, encoding='utf-8').read()
    assert '<table' not in rb_html, '규약 위반(정비사업 현황): 표가 아니라 목록이다'
    for term in _JARGON:
        assert term not in rb_html, '규약 위반(정비사업 현황): 은어 "%s" 가 남아 있다' % term
    _assert_no_condition_chrome(rb_html, '정비사업 현황')
    assert '<table' not in sub_html, \
        '규약 위반(청약 공고): 표가 아니라 목록이다(청약공고_스펙 §4) — <table 이 있다'
    _assert_no_condition_chrome(sub_html, '청약 공고')


def build():
    ws = wl.load_all()
    # 지난번 「지금 걸려 있다」 스냅숏(_seen.json) 비교는 안 쓴다 — watch_mark.py·
    # _seen.json 은 글쓴이 도구로 그대로 둔다(2026-09-02). 「지난번 본 뒤 바뀐 것」
    # 절 자체도 이제 없다 — 그 값(지난달·석 달 Δ)은 지도 패널이 구마다 낸다
    # (2026-09-03, movement 계산 함수는 _gu_map_data 가 그대로 재사용한다).
    # 통계 기준월과 법 시행일은 성격이 다르다. max 로 뭉치면 「자료 기준」에 법 시행일이
    # 올라와 통계가 실제보다 새 것처럼 읽힌다 — 이 장이 값에 「기준」을 붙이는
    # 이유를 머리에서 어기는 자리였다. 분기 표기(YYYY-nQ)도 같은 이유로 뺀다 —
    # 문자열 max 는 "2026-2Q" > "2026-07" 로 읽어(다섯째 글자 '2' > '0') 분기가
    # 월간 통계를 이긴다. 「YYYY-MM」꼴만 자료 기준 후보로 남긴다
    stat = [m.get('as_of', '') for w in ws for m in (w['metrics'] or {}).values()
            if w['kind'] == 'realestate' and m.get('level') != 'law'
            and re.match(r'^\d{4}-\d{2}$', m.get('as_of') or '')]
    # 부동산원 통계만 센다 — 청약홈 공고월(2026-08)이 섞이면 통계가 실제보다 새 것처럼 읽힌다
    asof = max(stat or ['—'])
    checked = max([w['checked'] for w in ws if w.get('checked')] or ['—'])

    h = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>포트폴리오 워치</title>%s<style>%s</style></head><body><div class="wrap">'
         % (FONTS, CSS)]
    h.append('<header><div class="h-top"><h1>포트폴리오 워치</h1>'
             '<p class="meta mono">마지막 확인 %s · 자료 기준 %s</p></div>'
             '<p class="lede">서울 세 권역과 경기 다섯 곳, 지금 전세로 갈지 매매로 갈지 — 값을 깎을 수 '
             '있는 장인지, 제도가 셈을 바꿨는지.</p></header>' % (E(checked), E(asof)))
    # 절 바로가기 — header 밖에 둔다. sticky 는 제 부모 상자 안에서만 붙어서, header 안에
    # 넣으면 header 가 화면 위로 지나가는 순간 같이 사라진다(실제로 그렇게 나갔다). — 앵커다. 저장소 규칙(관문 버튼 금지)은 내용을 가리는 버튼을
    # 말한다(스킨 첫 화면에서 카드를 숨기고 그 앞을 막는 것). 이 줄은 아래 절을
    # 전부 그대로 펼쳐 두고 그 자리로 뛰는 것만 돕는다 — 걸러 내지 않는다.
    # 2026-09-03 — 「권역」·「바뀐 것」 두 앵커는 없앴다(지도 히어로가 그 둘을
    # 흡수했다). 「지도」 하나로 판단한다.
    # 최상위는 서울|경기 탭(2026-09-04 사용자 지시 「서울 경기 구분이 가장 상위」).
    # 시·도 상자 안 순서 — 분양(지금 청약) → 지도 → 달라진 것 → 보고 있는 것.
    # 「분양이 가장 빨리 오게」 — 지금 신청할 수 있는 것이 이 장을 여는 첫 이유다.
    # 제도·청약 조건·자료 기준은 전국 공통이라 탭 밖 아래에 한 번만 선다.
    h.append('<div class="sido-tabs" role="tablist" aria-label="시·도">%s</div>'
             % ''.join('<button type="button" class="sido-tab%s" role="tab" data-sido="%s" '
                       'aria-selected="%s">%s</button>'
                       % (' is-on' if not sfx else '', sido, 'true' if not sfx else 'false',
                          sido) for sido, sfx in SIDOS))
    for sido, sfx in SIDOS:
        sido_ws = _sido_watches(ws, sido)
        blk = ['<div class="sido-block" data-sido="%s"%s>' % (sido, '' if not sfx else ' hidden')]
        blk.append('<nav class="jump" aria-label="절 바로가기 — %s">'
                   '<a href="#subscription%s">분양</a><a href="#map%s">지도</a>'
                   '<a href="#changed%s">달라진 것</a>%s<a href="#lines%s">보고 있는 것</a>'
                   '<a href="#policy">제도</a><a href="#basis">자료 기준</a></nav>'
                   % (sido, sfx, sfx, sfx,
                      ('<a href="#rebuild%s">정비사업</a>' % sfx) if _rebuild_data(ws)[0] is not None else '',
                      sfx))
        blk.append(subscription_section(ws, sido, sfx))
        blk.append('<section class="hero" id="map%s">%s</section>'
                   % (sfx, seoul_map_section(ws, asof, checked, sido, sfx)))
        blk.append(rebuild_section(ws, sido, sfx))
        blk.append('<div class="band" id="lines%s"><p class="band-t">보고 있는 것 — %s %d</p>%s</div>'
                   % (sfx, sido, len(sido_ws), line_summary_rows(ws, sido)))
        blk.append('</div>')
        h.append(''.join(blk))

    h.append('<div class="band" id="policy"><p class="band-t">제도</p>'
             '<p class="band-s">제도는 값으로 안 옵니다. 지금 어느 판인가만 기계가 알고, '
             '바뀐 내용은 사람이 조문을 열어 읽습니다.</p>%s</div>' % law_summary(ws))

    h.append(subscription_cond_section(ws))

    n_pol = sum(1 for w in ws if w['kind'] != 'realestate')
    h.append('<div class="band" id="lines-policy"><p class="band-t">보고 있는 것 — 제도 %d%s</p>%s</div>'
             % (n_pol, _checked_note(ws), line_summary_rows(ws)))

    h.append('<div class="band" id="basis"><p class="band-t">값이 언제 것인가</p>%s</div>'
             % time_ruler_fig(ws))

    # 푸터에는 출처와 갱신 약속만. 파일 경로는 주석으로 내린다 — 「scratchpad」라는
    # 낱말이 화면에 있는 것만으로 임시로 만든 것처럼 읽힌다(2026-09-03)
    h.append('<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
             '마지막 확인 %s · 통계 기준 %s. 통계가 갱신되면 다음 달에 다시 '
             '확인합니다.</footer>' % (E(checked), E(asof)))
    h.append('<!-- 판단은 insights/watch/, 수치는 insights/watch/_metrics/, 줄 상세는'
             ' 대시보드/watch/ 아래. 이 화면은 scratchpad/gen_watch_page.py 가 만든다 -->')
    h.append(_MAP_JS)
    h.append(_SIDO_JS)
    h.append(_JUMP_JS)
    h.append('</div></body></html>')
    html = ''.join(h)
    check_ui(html, ws)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)

    # 줄 상세 페이지 + 제도 전체 표 페이지. 옛 파일이 남아 있으면 먼저 지운다 —
    # 줄 이름을 바꾸거나 지운 뒤에도 옛 슬러그 파일이 그대로 남으면 아무도 안 가리키는
    # 페이지가 site/ 로도 같이 나간다.
    os.makedirs(WATCH_DIR, exist_ok=True)
    expected = (set(w['slug'] + '.html' for w in ws)
               | {'제도.html', '청약 공고.html', '정비사업 현황.html'})
    for f in os.listdir(WATCH_DIR):
        if f.endswith('.html') and f not in expected:
            os.remove(os.path.join(WATCH_DIR, f))
    for w in ws:
        with io.open(os.path.join(WATCH_DIR, w['slug'] + '.html'), 'w',
                     encoding='utf-8', newline='\n') as f:
            f.write(detail_page(w))
    with io.open(os.path.join(WATCH_DIR, '제도.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(law_page(ws))
    with io.open(os.path.join(WATCH_DIR, '청약 공고.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(subscription_page(ws))
    with io.open(os.path.join(WATCH_DIR, '정비사업 현황.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(rebuild_page(ws))
    check_detail_ui(ws)

    print('OK: 줄 %d개 -> %s' % (len(ws), OUT))
    print('OK: 상세 %d장 -> %s' % (len(ws) + 2, WATCH_DIR))
    return html


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
