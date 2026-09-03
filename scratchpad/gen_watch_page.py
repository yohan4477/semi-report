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
# 구 → 권역. 보는 것은 세 권역뿐이라(강남 3구·노도강·마용성) 그 구 아홉만 채워진다.
# 나머지 열여섯은 지도에 있지만 「보고 있지 않은 구」다.
GU_REGION = dict((g, t) for t in ('강남 3구', '노도강', '마용성')
                 for g in AREAS.get(t, {}).get('구', []))
WATCHED_GU = sorted(GU_REGION)


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


def _reg_bin(adj, hot):
    """규제지역 채움 칸 — both(둘 다 지정)·one(하나만)·none(둘 다 해제)·null(모름)."""
    if adj is None or hot is None:
        return 'null'
    if adj and hot:
        return 'both'
    if adj or hot:
        return 'one'
    return 'none'


def _lth_counts():
    gu = (ZONES.get('토지거래허가구역', {}) or {}).get('gu', {}) or {}
    vals = [(v or {}).get('value') for v in gu.values()]
    n_all, n_part, n_none = vals.count('전부'), vals.count('일부'), vals.count('없음')
    return n_all, n_part, n_none, len(SEOUL_GU['gu']) - n_all - n_part - n_none


def _reg_counts():
    cnt = {'both': 0, 'one': 0, 'none': 0, 'null': 0}
    for name in SEOUL_GU['gu']:
        cnt[_reg_bin(*_reg_info(name))] += 1
    return cnt


def _region_raw(watches):
    """3 실거주 줄의 원자료(insights/watch/_metrics/) — target 이름으로 찾는다."""
    return dict((w['target'], wl.metrics_of(w['kind'], w['slug'])) for w in _live_areas(watches))


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
.hero-t{font-size:15px;font-weight:600;margin:0}
/* 서울 지도 히어로 — 지도가 첫 화면이고 정보는 지도에서 나온다(2026-09-03) */
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
.seoul-map .gu{fill:var(--paper);stroke:var(--line);stroke-width:1px;cursor:default}
.seoul-map .gu[data-slug]{cursor:pointer}
.seoul-map .gu[data-ratio-bin]{stroke:var(--surface);stroke-width:1.5px}
.seoul-map .gu[data-ratio-bin="1"]{fill:var(--seq-1)}
.seoul-map .gu[data-ratio-bin="2"]{fill:var(--seq-2)}
.seoul-map .gu[data-ratio-bin="3"]{fill:var(--seq-3)}
.seoul-map .gu[data-ratio-bin="4"]{fill:var(--seq-4)}
.seoul-map .gu[data-ratio-bin="5"]{fill:var(--seq-5)}
.seoul-map .gu.gu-hover{stroke:var(--ink);stroke-width:2.5px}
.seoul-map .gu.gu-dim{opacity:.55}
.gu-lbl{font-size:11px;font-weight:600;fill:var(--ink);paint-order:stroke;
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
.gu-panel{display:block}
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
.gp-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin:0}
.gp-name{font-size:20px;font-weight:700}
.gp-close{flex:0 0 auto;width:32px;height:32px;min-width:44px;min-height:44px;margin:-6px -6px 0 0;
  border:0;background:transparent;color:var(--ink-3);font-size:20px;line-height:1;cursor:pointer;
  display:flex;align-items:center;justify-content:center;border-radius:999px}
.gp-close:hover{background:var(--line);color:var(--ink)}
.gp-sub{margin:2px 0 0;font-size:12.5px;color:var(--ink-3)}
/* 뜻 한 줄 — 수 세 줄보다 먼저 읽힌다 */
.gp-mean{font-size:14.5px;font-weight:600;color:var(--ink);margin:8px 0 10px;line-height:1.5}
/* 값 줄 — 라벨(왼쪽 정렬 12.5px ink-3) 바로 뒤 같은 줄에 값. 두 열로 안 가른다 —
   폰 폭에서 두 열이면 값이 잘린다(2026-09-03) */
.gp-row{margin:8px 0 0;font-size:.85rem;line-height:1.5;color:var(--ink-2)}
.gp-lbl{color:var(--ink-3);font-size:12.5px;margin-right:4px}
.gp-d{color:var(--ink-2)}
.gp-more{display:block;margin:12px 0 0;padding:10px 0 0;font-weight:600;font-size:.95rem;
  border-bottom:0;border-top:1px solid var(--line)}
/* 모바일 — 구를 고르면 아래에서 시트가 올라온다. 기본(권역 요약 셋)은 그대로
   지도 아래 인라인이다(:not([data-panel="default"]) 로 가른다) */
@media (max-width:620px){
  .gu-panel:not([data-panel="default"]){
    display:block!important;position:fixed;left:0;right:0;bottom:0;max-height:45vh;
    overflow-y:auto;background:var(--surface);border-top:1px solid var(--line);
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
  /* 지도 히어로 — 지도 → 패널 순으로 세로 편다 */
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
    return ('<p class="lbl">%s</p><div class="tw"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>'
            % (E(cap), ''.join('<th>%s</th>' % E(h) for h in head), ''.join(body)))


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
    LO, HI = 40.0, 70.0
    X0, X1, Y = 26, W - 26, 50

    def px(v):
        v = max(LO, min(HI, v))
        return X0 + (X1 - X0) * (v - LO) / (HI - LO)

    o = ['<line x1="%d" y1="%d" x2="%d" y2="%d" class="grid"/>' % (X0, Y, X1, Y)]
    for tkv in range(40, 71, 5):
        x = px(tkv)
        o.append('<path d="M%.1f %d L%.1f %d" class="grid"/>' % (x, Y - 4, x, Y + 4))
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle" '
                 'style="font-size:11px">%d</text>' % (x, Y - 16, tkv))

    pts.sort(key=lambda p: p[1])
    CH = 9.0
    labels = ['%s %s' % (n, _fmt1(v)) for n, v, _d in pts]
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
    h.append('<div id="judge"><p class="line-judge">%s</p>%s</div>'
             % (w['judged'], trig[0] if trig else ''))
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
    items = [('now', '지금 값'), ('judge', '판단'), ('clash', '반대 근거'),
             ('hist', '이력'), ('more', '값 더'), ('where', '확인처')]
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


def line_summary_rows(watches):
    """본 장의 「보고 있는 것」 목록 — 이름·verdict 만. 마지막 확인 날짜는 절 제목
    옆으로 올렸다(_checked_note). 칩(걸림·근접)은 없다 — 문턱은 독자마다 달라 뜻이
    없다."""
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


def _ratio_legend_html(watches):
    """전세가율 범례 — 다섯 단 색 띠 + 방향 한 줄 + 값 없는 구 이름 + 전세가율 자.

    값 없는 구는 수만 적으면(「값 없음 — 16구」) 어느 구인지 알 길이 없다. 지도에서
    자기 동네를 못 찾은 사람이 여기서 이름을 확인한다."""
    blanks = sorted(set(SEOUL_GU['gu']) - set(WATCHED_GU))
    names = '·'.join(g[:-1] if g.endswith('구') else g for g in blanks)
    strip = ''.join('<span class="leg-sw" style="background:var(--seq-%d)"></span>' % i
                    for i in range(1, 6))
    labels = ''.join('<span>%s</span>' % E(t) for t in ('<45', '45~50', '50~55', '55~60', '≥60'))
    return ('<div class="leg-strip">%s</div><p class="leg-labels">%s</p>'
            '<p class="leg-src">→ 오른쪽일수록 매매가에 가깝습니다.</p>'
            '<p class="leg-item"><span class="leg-sw" style="background:var(--paper);'
            'border:1px solid var(--line)"></span> 값 없음 — %d구: %s</p>%s'
            % (strip, labels, len(blanks), E(names), ratio_ruler_fig(watches)))


def _zone_age_chip(as_of, today):
    """여섯 달 넘게 안 바뀐 기준일에는 나이를 붙인다. 머리의 「자료 기준 2026-07」과
    같은 무게로 읽히면 값의 나이가 열 배 차이 나는 것이 안 보인다."""
    a, b = _months(as_of), _months(today)
    if a is None or b is None or b - a < 6:
        return ''
    return ' <span class="t-old">%d개월 전 값</span>' % (b - a)


def _zone_banner(today):
    """지정 현황 상태 배너 — 층 버튼 둘을 대신한다.

    25구가 전부 같은 범주라 지도로 그리면 서울 전체가 먹 단색이 되고, 클릭 한 번을
    내고 얻는 정보는 「전부 지정」 문장 하나였다. 수와 날짜는 손으로 안 적는다 —
    insights/watch/_zones.json 에서 센다. 구마다 갈리는 날 층을 되살린다(그때 색은
    --seq-4 / hatch / --surface 3단)."""
    total = len(SEOUL_GU['gu'])
    n_all, n_part, n_none, n_null = _lth_counts()
    lth_txt = ('%d구 전부 지정' % total if n_all == total
               else '전부 지정 %d구 · 일부 지정 %d구 · 미지정 %d구 · 확인 안 됨 %d구'
               % (n_all, n_part, n_none, n_null))
    cnt = _reg_counts()
    reg_txt = ('%d구 둘 다 지정' % total if cnt['both'] == total
               else '둘 다 지정 %d구 · 하나만 %d구 · 둘 다 해제 %d구 · 확인 안 됨 %d구'
               % (cnt['both'], cnt['one'], cnt['none'], cnt['null']))
    rows = []
    for label, txt, z in (('토지거래허가구역', lth_txt, ZONES.get('토지거래허가구역', {})),
                          ('규제지역', reg_txt, ZONES.get('조정대상지역', {}))):
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


def _gu_svg(gu_data):
    """서울 25개 구 지도. 채움은 CSS 가 data-ratio-bin 으로 고른다 — 값 자체는
    여기서 속성으로 다 박아 두고 JS 는 아무 계산도 안 한다.

    2026-09-03 — 층(토허·규제) 두 개를 걷었다. 25구가 전부 같은 범주라 서울 전체가
    먹 단색으로 칠해졌고, 얻는 정보는 문장 하나였다. 지도 아래 상태 배너
    (_zone_banner)가 그 문장을 대신한다. 구마다 갈리는 날 층을 되살린다 — 그때
    색은 --seq-4 / hatch / --surface 3단으로 하고, 서울 전체를 먹으로 안 칠한다."""
    vb = SEOUL_GU['viewBox']
    paths, labels = [], []
    for name in sorted(SEOUL_GU['gu']):
        g = SEOUL_GU['gu'][name]
        e = gu_data[name]
        watched = bool(e['jeonse'])
        label = ('전세가율 %.1f%%' % e['jeonse']['cur']) if watched else '보고 있지 않은 구'
        attrs = ['class="gu"', 'data-gu="%s"' % E(name)]
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
        attrs.append('d="%s"' % g['d'])
        paths.append('<path %s/>' % ' '.join(attrs))
        if name in LABEL_SKIP and not watched:
            continue
        cls = 'gu-lbl' if watched else 'gu-lbl blank'
        labels.append('<text x="%.1f" y="%.1f" class="%s" text-anchor="middle">%s</text>'
                      % (g['cx'], g['cy'], cls, E(name)))
    return ('<svg class="seoul-map" viewBox="%d %d %d %d">%s'
            '<g class="gu-labels">%s</g></svg>'
            % (vb[0], vb[1], vb[2], vb[3], ''.join(paths), ''.join(labels)))


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


def changed_section(watches):
    """지난달과 달라진 것 — 이 장을 매달 다시 여는 이유가 이것 하나다.

    지도 왼쪽 아래 빈 칸에 선다(지도 그림이 그 칸의 위쪽 절반만 쓴다). 값이 없으면
    빈 절을 그대로 낸다 — 빈 절이 델타를 감추는 것보다 낫다."""
    rows, base = [], None
    idx = _idx_rows(watches)
    for w in sorted(_live_areas(watches), key=lambda w: w['target']):
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
    return ('<div class="changed" id="changed"><p class="chg-t">%s</p>%s</div>'
            % (E(title), ''.join(rows)))


# 바닐라 JS — 지도 호버=미리보기/누르기=고정(선택 모델
# 하나로, 2026-09-03) · 권역 요약 호버(지도 강조만). 상세 이동은 패널 안
# 「자세히 →」 링크로만 한다 — path 클릭은 더는 페이지를 안 옮긴다(모바일에서
# 탭=이동이면 값을 볼 길이 없다는 사용자 지적). 값은 전부 생성 때 HTML 에
# 이미 있다 — 여기서는 hidden·class 토글만 한다(계산 없음).
_MAP_JS = """<script>
(function(){
var svg=document.querySelector('.seoul-map');
if(!svg)return;
var gus=Array.from(svg.querySelectorAll('.gu'));
var panels=Array.from(document.querySelectorAll('.gu-panel'));
var rss=Array.from(document.querySelectorAll('.rs'));
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
Array.from(document.querySelectorAll('.gp-close')).forEach(function(b){
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
})();
</script>"""

# 절 바로가기의 현재 위치 표시. 본 장과 상세가 같은 조각을 쓴다 — 나브 꼴이 같은데
# 한쪽만 지금 절을 알려 주면 그것대로 헷갈린다.
_JUMP_JS = """<script>
(function(){
var links=Array.from(document.querySelectorAll('.jump a'));
if(!links.length||!window.IntersectionObserver)return;
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


def seoul_map_section(watches, asof, checked):
    """지도 히어로 — 왼쪽 지도(58%, 데스크톱은 sticky) · 오른쪽 패널(42%, 기본은
    권역 셋 요약). 구를 손대면(호버) 미리보기, 누르면(클릭·Enter) 그 구로
    고정된다. 상세 이동은 패널 안 「자세히 →」로만 한다. 값은 전부
    insights/watch/_seoul_gu.json·_zones.json·metrics 에서 — 지정 현황이 셋 다
    「전부」라도 범례 수는 그 데이터에서 센다.

    풀이 셋(전세가율·매매가격지수·수급동향)은 패널이 아니라 지도 캡션 줄로
    내렸다(2026-09-03) — 권역 요약+범례+자+풀이가 패널 안에 다 있으면 데스크톱
    800px 를 넘는다."""
    gu_data = _gu_map_data(watches)
    svg = _gu_svg(gu_data)
    # 구 패널이 기본 패널보다 앞에 선다 — 골랐을 때 위에 얹히고 권역 셋은 그 아래
    # 그대로 남는다(덮으면 견줄 수가 없다)
    panels = ''.join(_gu_panel_html(name, gu_data[name])
                     for name in sorted(SEOUL_GU['gu'])) + \
             ('<div class="gu-panel" data-panel="default">%s</div>'
              % _region_summary_html(watches))
    cap = '<p>지도 원본 southkorea/seoul-maps · 값 기준 %s</p>' % E(asof)
    return (
        '<p class="hero-t">서울 25구 — 지금 전세가율이 어디쯤인가</p>'
        '<div class="maprow">'
        '<div class="mapcol">'
        '<figure class="map-fig">%s<figcaption>%s</figcaption></figure>%s%s</div>'
        '<div class="mappanel" aria-live="polite" aria-atomic="true">%s'
        '<div class="map-legend">%s</div>'
        '</div></div>%s'
        % (svg, cap, _zone_banner(checked), changed_section(watches),
           panels, _ratio_legend_html(watches), _MAP_JS))


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
_COND_CHROME = ('class="chip-legend"', '<th>걸리면</th>', '<th>조건</th>',
                'class="tag t-near"', 'class="tag t-clear"')
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
    at_map = html.find('id="map"')
    at_changed = html.find('id="changed"')
    at_policy = html.find('id="policy"')
    assert 0 < at_map < at_policy, \
        '규약 위반: 지도 히어로(#map)가 첫 화면(제도보다 먼저)이어야 한다'
    assert 0 < at_changed < at_policy, \
        '규약 위반: 「달라진 것」(#changed)이 제도보다 먼저 서야 한다 — 매달 다시 여는 이유다'
    # 층 버튼은 걷었다. 25구가 전부 같은 범주인 층을 지도로 그리면 서울 전체가 먹
    # 단색이 되고 얻는 정보는 문장 하나다 — 그 문장을 상태 배너가 낸다
    assert 'layer-btn' not in html and 'data-layer' not in html, \
        '규약 위반: 층 버튼을 두지 않는다 — 구마다 갈리는 값만 지도로 그린다'
    assert 'class="zone-banner"' in html, \
        '규약 위반: 지정 현황 상태 배너가 없다 — 층을 걷었으면 그 값이 문장으로 서야 한다'
    assert '값이 언제 것인가' in html, '규약 위반: 자료 기준 자가 없다 — 값의 나이를 먼저 보인다'
    n_fig = html.count('<figure')
    assert n_fig == 3, \
        '규약 위반: 본 장의 <figure 는 지도 + 전세가율 자 + 자료 기준 자 셋이어야 한다 (%d개)' % n_fig
    n_tbl = html.count('<table')
    assert n_tbl == 0, \
        '규약 위반: 본 장에 표를 두지 않는다 — 표는 상세(watch/)로 옮겼다 (%d개)' % n_tbl
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
            if m.get('level') != 'law' and re.match(r'^\d{4}-\d{2}$', m.get('as_of') or '')]
    asof = max(stat or ['—'])
    checked = max([w['checked'] for w in ws if w.get('checked')] or ['—'])

    h = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>포트폴리오 워치</title>%s<style>%s</style></head><body><div class="wrap">'
         % (FONTS, CSS)]
    h.append('<header><div class="h-top"><h1>포트폴리오 워치</h1>'
             '<p class="meta mono">마지막 확인 %s · 자료 기준 %s</p></div>'
             '<p class="lede">서울 세 권역, 지금 전세로 갈지 매매로 갈지 — 값을 깎을 수 있는 '
             '장인지, 제도가 셈을 바꿨는지.</p></header>' % (E(checked), E(asof)))
    # 절 바로가기 — header 밖에 둔다. sticky 는 제 부모 상자 안에서만 붙어서, header 안에
    # 넣으면 header 가 화면 위로 지나가는 순간 같이 사라진다(실제로 그렇게 나갔다). — 앵커다. 저장소 규칙(관문 버튼 금지)은 내용을 가리는 버튼을
    # 말한다(스킨 첫 화면에서 카드를 숨기고 그 앞을 막는 것). 이 줄은 아래 절을
    # 전부 그대로 펼쳐 두고 그 자리로 뛰는 것만 돕는다 — 걸러 내지 않는다.
    # 2026-09-03 — 「권역」·「바뀐 것」 두 앵커는 없앴다(지도 히어로가 그 둘을
    # 흡수했다). 「지도」 하나로 판단한다.
    h.append('<nav class="jump" aria-label="절 바로가기">'
             '<a href="#map">지도</a><a href="#changed">달라진 것</a>'
             '<a href="#policy">제도</a><a href="#lines">보고 있는 것</a>'
             '<a href="#basis">자료 기준</a></nav>')

    # 지도가 첫 화면이고 정보는 지도에서 나온다(사용자 지시 2026-09-03) — 전세가율
    # 자·권역 카드를 여기 한자리로 접었다(ratio_ruler_fig 는 전세가율 층 범례 안으로,
    # area_cards 는 패널 기본 상태로 흡수됐다).
    h.append('<section class="hero" id="map">%s</section>'
             % seoul_map_section(ws, asof, checked))

    h.append('<div class="band" id="policy"><p class="band-t">제도</p>'
             '<p class="band-s">제도는 값으로 안 옵니다. 지금 어느 판인가만 기계가 알고, '
             '바뀐 내용은 사람이 조문을 열어 읽습니다.</p>%s</div>' % law_summary(ws))

    h.append('<div class="band" id="lines"><p class="band-t">보고 있는 것 %d%s</p>%s</div>'
             % (len(ws), _checked_note(ws), line_summary_rows(ws)))

    h.append('<div class="band" id="basis"><p class="band-t">값이 언제 것인가</p>%s</div>'
             % time_ruler_fig(ws))

    # 푸터에는 출처와 갱신 약속만. 파일 경로는 주석으로 내린다 — 「scratchpad」라는
    # 낱말이 화면에 있는 것만으로 임시로 만든 것처럼 읽힌다(2026-09-03)
    h.append('<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
             '마지막 확인 %s · 통계 기준 %s. 통계가 갱신되면 다음 달에 다시 '
             '확인합니다.</footer>' % (E(checked), E(asof)))
    h.append('<!-- 판단은 insights/watch/, 수치는 insights/watch/_metrics/, 줄 상세는'
             ' 대시보드/watch/ 아래. 이 화면은 scratchpad/gen_watch_page.py 가 만든다 -->')
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
    expected = set(w['slug'] + '.html' for w in ws) | {'제도.html'}
    for f in os.listdir(WATCH_DIR):
        if f.endswith('.html') and f not in expected:
            os.remove(os.path.join(WATCH_DIR, f))
    for w in ws:
        with io.open(os.path.join(WATCH_DIR, w['slug'] + '.html'), 'w',
                     encoding='utf-8', newline='\n') as f:
            f.write(detail_page(w))
    with io.open(os.path.join(WATCH_DIR, '제도.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(law_page(ws))
    check_detail_ui(ws)

    print('OK: 줄 %d개 -> %s' % (len(ws), OUT))
    print('OK: 상세 %d장 -> %s' % (len(ws) + 1, WATCH_DIR))
    return html


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
