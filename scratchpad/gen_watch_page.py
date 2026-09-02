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
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0F1418; --surface:#171D22;
  --ink:#E9EDF0; --ink-2:#AAB4BC; --ink-3:#7C8791;
  --line:#263038;
  --up:#E0704A; --down:#5C8CE0; --near:#D9AA4A;
  --fig-blue:#AAB4BC; --fig-good:#E0704A; --warn:#D9AA4A;
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
/* 절 바로가기 — 스크롤해도 붙어 있다. 현재 절 강조는 JS 없이는 못 하니 안 한다 */
.jump{position:sticky;top:0;z-index:5;display:flex;gap:6px;overflow-x:auto;
  white-space:nowrap;margin:16px 0 0;padding:10px 0;background:var(--paper);
  border-bottom:1px solid var(--line);scrollbar-width:none}
.jump::-webkit-scrollbar{display:none}
.jump a{flex:0 0 auto;font-size:12.5px;font-weight:500;background:var(--surface);
  border:1px solid var(--line);border-radius:999px;padding:6px 12px}
.jump a:hover{border-color:var(--ink-3)}
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
.stat-m{font-size:12.5px;color:var(--ink-3);margin:4px 0 0}
.delta{font-size:15px;font-weight:600;margin-left:6px}
.d-up{color:var(--up)}
.d-down{color:var(--down)}
/* 절 — 대문자·자간 라벨을 걷고 문장형 제목으로 */
.hero{margin:28px 0 0}
.band{margin:40px 0 0;border-top:2px solid var(--ink);padding-top:11px}
.band-t{font-size:15px;font-weight:600;margin:0}
.band-s{font-size:.9rem;color:var(--ink-2);margin:6px 0 0;max-width:66ch}
.chip-legend{margin-left:8px;font-size:12.5px;font-weight:400;color:var(--ink-3)}
/* 용어 풀이 — 그 말 옆에 둔다. 별도 절이 아니라 등장한 자리 바로 아래 잔글씨다 */
.term{font-size:12.5px;color:var(--ink-3);margin:4px 0 0;max-width:66ch}
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
  .stats{flex-wrap:nowrap;gap:8px}
  .stat{flex:1 1 0;min-width:0}
  .stat-v{font-size:26px}
  .delta{font-size:13px}
  .areas{grid-template-columns:1fr}
  .area-n{font-size:30px}
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

    def px(a):
        return X0 + (X1 - X0) * ((xs[a] - lo) / float(hi - lo) if hi > lo else .5)

    order = sorted(pts, key=lambda a: xs[a])
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
        # 한 번만 밀면 마지막 점이 판 끝에 붙어 앞 라벨과 겹친 채로 남는다
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
    o.append('<text x="%d" y="%d" class="t-sm t-axis">%s</text>' % (X0, cap_y, E('전세가 낫다')))
    o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="end">%s</text>'
             % (X1, cap_y, E('매매 문턱이 낮다')))
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
    cap = ('전세가율 = 중위 전세가 ÷ 중위 매매가. 올라가면 보증금이 집값에 가까워지고, '
           '동시에 매매로 넘어가는 자기 돈이 줄어듭니다. 기준 %s · 공표.' % E(asof))
    return '<figure>%s%s<figcaption>%s</figcaption></figure>' % (wide, narrow, cap)


def area_cards(watches):
    """권역 카드 셋 — 지금 값이 큰 글씨로 먼저 선다. 표(area_table)를 걷어낸 자리다.
    아카이브의 「타일 금지」 규약은 접어서 고르는 카드를 말한다. 이 카드는 접히지
    않고 늘 펼쳐져 있으므로 class="area" 로 두고 그 규약을 그대로 지킨다."""
    live = _live_areas(watches)
    items = []
    for w in live:
        metrics = [m for k, m in (w.get('metrics') or {}).items() if k.startswith('jeonse_ratio_')]
        if not metrics:
            continue
        rs = [m['value'] for m in metrics]
        avg = _avg_series(w)
        cur = avg[-1][1] if avg else sum(rs) / len(rs)
        delta = (avg[-1][1] - avg[-4][1]) if len(avg) >= 4 else None
        sd = (w.get('metrics') or {}).get('supply_demand')
        n_hit = sum(1 for t in w['triggers'] if t['kind'] == wl.KIND_VALUE
                    and wl.state_now(t['cond'], t['series'])[0] == '걸림')
        n_near = sum(1 for t in w['triggers'] if t['kind'] == wl.KIND_VALUE
                     and wl.state_now(t['cond'], t['series'])[0] == '근접')
        items.append((cur, w, rs, delta, sd, n_hit, n_near))
    if not items:
        return ''
    # 오름차순 — 전세가율 자도 값이 작은 쪽이 왼쪽이다. 반대로 두면 눈이 자와
    # 카드 순서를 못 맞춘다
    items.sort(key=lambda r: r[0])
    h = ['<div class="areas">']
    for cur, w, rs, delta, sd, n_hit, n_near in items:
        if delta is None or abs(delta) < 0.05:
            arrow = ''
        elif delta > 0:
            arrow = '<span class="delta d-up">↑%s</span>' % _fmt1(delta)
        else:
            arrow = '<span class="delta d-down">↓%s</span>' % _fmt1(-delta)
        if sd and sd.get('value') is not None:
            sdv = float(sd['value'])
            sd_line = ('<b>%s</b> · %s <span class="t-sub">%s</span>'
                      % (_fmt1(sdv), '사려는 사람이 많다' if sdv >= 100 else '팔려는 사람이 많다',
                         E(sd.get('area') or '')))
        else:
            sd_line = '못 붙임'
        # 0인 쪽은 아예 안 낸다 — 「걸림 0」은 안심시키는 정보가 아니라 잡음이다
        parts = []
        if n_hit:
            parts.append('<span class="tag t-hit">걸림 %d</span>' % n_hit)
        if n_near:
            parts.append('<span class="tag t-near">근접 %d</span>' % n_near)
        chips = ' '.join(parts) if parts else '<span class="t-none">조건에 든 것 없음</span>'
        h.append(
            '<div class="area"><p class="area-k">%s · %s</p>'
            '<p class="area-v">%s</p>'
            '<p class="area-n">%s%%%s</p>'
            '<p class="area-r">구별 %s ~ %s</p>'
            '<div class="area-d">'
            '<div class="area-row"><span>매매 문턱</span><span>전세금의 %s배</span></div>'
            '<div class="area-row"><span>수급동향</span><span>%s</span></div>'
            '</div>'
            '<p class="area-c">%s</p>'
            '<a class="area-more" href="watch/%s.html">자세히 →</a></div>'
            % (E(_area_head(w['target'])), E(w.get('view') or ''),
               E(w.get('verdict') or '판단 없음'),
               _fmt1(cur), arrow, ('%.2f' % min(rs)), ('%.2f' % max(rs)),
               _fmt1(100.0 / cur) if cur else '—', sd_line, chips, w['slug']))
    h.append('</div>')
    return ''.join(h)


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
        '매매가격지수': ('그 구 아파트 값이 %s 대비 얼마나 움직였나. 값 자체보다 세 구가 같이 '
                    '가나, 어느 구가 먼저 꺾이나를 본다.' % basephrase),
        '전세가율': ('그 구 아파트의 중위 전세가 ÷ 중위 매매가. 올라가면 보증금이 집값에 '
                  '가까워지고, 동시에 매매로 넘어갈 때 더 얹을 돈이 준다.'),
        '수급동향': '100 이 균형. 위면 사려는 사람이, 아래면 팔려는 사람이 많다.',
    }


def _metric_name(what):
    """트리거 「무엇을」에서 지표 이름만(구 이름을 뗀다) — "전세가율 — 강남구" → "전세가율"."""
    return (what or '').split(' —')[0].strip()


def term_lines(watches, names):
    """등장하는 지표 이름마다 풀이 한 줄. names 에 없는 지표는 안 낸다 — 세 줄을
    늘 다 보여주면 그중 못 보는 지표까지 설명한 꼴이 된다."""
    terms = _term_dict(watches)
    order = ('매매가격지수', '전세가율', '수급동향')
    keys = [n for n in order if n in names]
    if not keys:
        return ''
    return ''.join('<p class="term">%s — %s</p>' % (E(n), E(terms[n])) for n in keys)


CHIP_STATE = {'새로 걸린': '걸림', '그대로 걸린': '걸림', '새로 근접': '근접', '풀린': '풀림'}


def _since_buckets(watches, seen):
    """네 묶음 — 새로 걸린 · 새로 근접 · 풀린(지난번엔 걸림·근접, 지금은 아님) ·
    그대로 걸린. 값 트리거와 법 개정을 한자리에 놓는다 — 둘 다 「내가 본 뒤에 무엇이
    달라졌나」에 답한다. seen 이 None(한 번도 확인한 적이 없다)이면 모든 열쇠의
    지난 상태가 없는 것으로 쳐서, 지금 걸린·근접이 전부 「새로」 쪽으로 떨어진다.

    행마다 w['slug'] 를 같이 담는다 — 줄 이름 링크가 이제 화면 안 앵커(#w-…)가 아니라
    watch/<슬러그>.html 상세 페이지를 가리켜야 해서다."""
    prev_v = ((seen or {}).get('value')) or {}
    prev_l = ((seen or {}).get('laws')) or {}
    buckets = {'새로 걸린': [], '새로 근접': [], '풀린': [], '그대로 걸린': []}
    for w in watches:
        t9 = title_of(w)
        for t in w['triggers']:
            if t['kind'] != wl.KIND_VALUE:
                continue
            now, why = wl.state_now(t['cond'], t['series'])
            prev = prev_v.get('%s|%s' % (w['slug'], t['what']))
            row = (t9, w['slug'], t['what'], t['value'], t['cond'], now, why, t['as_of'] or '—')
            if now == '걸림':
                buckets['그대로 걸린' if prev == '걸림' else '새로 걸린'].append(row)
            elif now == '근접':
                if prev != '근접':
                    buckets['새로 근접'].append(row)
            elif prev in ('걸림', '근접'):
                buckets['풀린'].append(row)
        for _tg, name, law_seen in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            if law_seen and now and str(now) != law_seen:
                row = (t9, w['slug'], name, now, '내가 읽은 판 %s' % law_seen, '걸림',
                       '그 뒤에 개정됐다 — 읽고 갱신한다', now)
                buckets['그대로 걸린' if prev_l.get(name) == '걸림' else '새로 걸린'].append(row)
    return buckets


def since_block(watches, seen):
    """맨 위 띠. 「지금 걸려 있다」가 아니라 「지난번과 무엇이 달라졌나」를 낸다 —
    한 달에 한 번 여는 독자에게 계속 걸려 있던 조건은 새 정보가 아니다."""
    buckets = _since_buckets(watches, seen)
    total = sum(len(v) for v in buckets.values())
    if seen is None:
        sub = ('아직 확인 표시를 한 적이 없어 전부 새로 걸린 것으로 봅니다. 확인했으면 '
               '<code>python scripts/watch_mark.py</code> 를 돌립니다.')
    else:
        n1, n2, n3 = len(buckets['새로 걸린']), len(buckets['새로 근접']), len(buckets['풀린'])
        sub = ('지난 확인 %s 이후 — 새로 걸린 <b>%d</b> · 가까이 온 <b>%d</b> · 풀린 <b>%d</b>'
               % (E(seen.get('checked') or '—'), n1, n2, n3))
    h = ['<p class="band-s">%s <span class="chip-legend">걸림 = 정한 조건에 들어옴 · '
         '근접 = 문턱 가까이</span></p>' % sub]
    # 이 절에 등장하는 지표 이름마다 풀이 한 줄 — 등장하지 않는 것은 안 낸다
    names = set(_metric_name(row[2]) for rows in buckets.values() for row in rows)
    h.append(term_lines(watches, names))
    if total == 0:
        h.append('<p class="band-s">조건에 든 값도, 내가 읽은 뒤에 바뀐 법도 없습니다. '
                 '이번 달은 볼 것이 없습니다.</p>')
        return ''.join(h)
    h.append('<div class="rows">')
    prev = None
    for name in ('새로 걸린', '새로 근접', '풀린', '그대로 걸린'):
        rows = buckets[name]
        for t9, wslug, what, val, cond, st, why, asof in rows:
            # 같은 줄이 잇달아 서면 이름을 되풀이하지 않는다 — 세 번 같은 이름이 서면
            # 눈이 그 열을 통째로 건너뛴다
            label = '' if t9 == prev else E(t9)
            prev = t9
            link = '<a href="watch/%s.html">%s</a>' % (wslug, label) if label else ''
            h.append('<div class="row"><span class="row-where">%s%s</span>'
                     '<span class="row-what">%s</span>'
                     '<span class="row-num">%s</span>'
                     '<span class="row-why">%s · %s · %s</span></div>'
                     % (tag(CHIP_STATE[name]), link, E(what), E(val), E(cond), E(why), E(asof)))
    h.append('</div>')
    return ''.join(h)


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

    그 metric 을 건 값 트리거가 있으면 그 조건이 걸렸던 달을 선 위에 빈 원으로
    찍는다(wl.fired_months) — 표의 「이력 N개월 중 k번」과 같은 판정을 그림으로도
    보게 하는 자리다.

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
        marks = []
        for _n, m, mkey in sel:
            t = trig_by_metric.get(mkey)
            s = [tuple(x) for x in m['series']]
            marks.append(wl.fired_months(t['cond'], s) if t else [])
        svg = wf.trend(ser, unit or '값', note=note, marks=marks)
        if svg:
            nsvg = wf.trend(ser, unit or '값', note=note, narrow=True, marks=marks)
            out.append((prio_val, '<figure>%s%s<figcaption>%s</figcaption></figure>'
                       % (svg.replace('<svg ', '<svg class="fig-w" ', 1),
                          nsvg.replace('<svg ', '<svg class="fig-n" ', 1),
                          E(TITLE.get(base, base)))))
    return out


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
    cells = []
    for t in vals:
        ser = t['series']
        cur = ser[-1][1]
        delta = ser[-1][1] - ser[-4][1] if len(ser) >= 4 else None
        unit = t.get('unit') or ''
        m = re.search(r'—\s*(\S+)$', t['what'] or '')
        label = m.group(1) if m else t['what']
        if delta is None or abs(delta) < 0.005:
            arrow = ''
        elif delta > 0:
            arrow = '<span class="delta d-up">↑%s</span>' % _fmt1(delta)
        else:
            arrow = '<span class="delta d-down">↓%s</span>' % _fmt1(-delta)
        cells.append(
            '<div class="stat"><p class="stat-k">%s</p>'
            '<p class="stat-v">%s%s%s</p>'
            '<p class="stat-m">기준 %s · %s</p></div>'
            % (E(label), _fmt1(cur), E(unit), arrow,
               E(t['as_of'] or '—'), E(t['nature'] or '공표')))
    names = set(_metric_name(t['what']) for t in vals)
    return '<div class="stats">%s</div>%s' % (''.join(cells), term_lines([w], names))


def hist_note(cond, series):
    """「조건」 칸 아래 작은 글씨 — 이력 몇 달 중 몇 번 걸렸나(check_watch W8 과
    같은 판정). series 가 없으면 잴 수 없으니 아무것도 안 붙인다."""
    if not series:
        return ''
    n, tot, _now = wl.backtest(cond, series)
    if n is None:
        return ''
    um = re.search(r'최근\s*(\d+)\s*(개월|달|년|분기)', cond or '')
    unit = um.group(2) if um else '점'
    return ('<br><span class="t-none" style="font-size:.78em">이력 %d%s 중 %d번</span>'
            % (tot, E(unit), n))


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


def line_block(w):
    """줄 하나의 상세 본문 — watch/<슬러그>.html 안에 실린다.

    2026-09-02 순서 — 머리 수치 띠 → 트리거 metric 도해 → 「지금 판단」 산문 →
    「판단 이력」 → 「값으로 오는 것」(무엇을·지금·조건·상태·걸리면·기준) →
    정책 줄의 법 표 → 나머지 도해 → 「왜 보나」 → 「사람이 확인하는 것」 →
    「반대 근거」. 그 줄을 여는 이유가 되는 값(트리거가 건 metric)을 산문보다
    먼저 세운다 — 나머지는 참고용 시계열이다."""
    h = ['<section class="line">']
    h.append(stat_strip(w))
    h.append(figures_trigger(w))
    h.append('<p class="line-judge">%s</p>' % w['judged'])

    if w.get('history'):
        h.append(tbl('판단 이력', ['날짜', '무엇을', '왜'],
                     [[E(d), wl.md_inline(what), wl.md_inline(why)]
                      for d, what, why in w['history']]))

    vals = [t for t in w['triggers'] if t['kind'] == wl.KIND_VALUE]
    if vals:
        rows = []
        for t in vals:
            st, why = wl.state_now(t['cond'], t['series'])
            unit = t.get('unit') or ''
            rows.append([E(t['what']),
                         ('—' if t['value'] is None else
                          '%s <span class="t-none">%s</span>' % (E(t['value']), E(unit))),
                         E(t['cond']) + hist_note(t['cond'], t['series']),
                         tag(st) + ' <span class="t-none">%s</span>' % E(why),
                         wl.md_inline(t['act']) if t['act'] else '<span class="t-none">—</span>',
                         '%s <span class="t-none">%s</span>' % (E(t['as_of'] or '—'),
                                                                E(t['nature'] or '자리표시'))])
        h.append(tbl('값으로 오는 것',
                     ['무엇을', '지금', '조건', '상태', '걸리면', '기준'], rows))
    if w.get('laws'):
        rows = []
        for _tg, name, seen in w['laws']:
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            st = '—' if not now or not seen else ('같다' if str(now) == seen else '걸림')
            rows.append([E(name), E(seen or '—'), E(now or '아직 안 받음'), tag(st)])
        h.append(tbl('내가 읽은 판과 지금 판',
                     ['법·고시', '내가 읽은 판', '지금 판', '같은가'], rows))
    h.append(figures_rest(w))
    if w['points']:
        h.append('<p class="lbl">왜 보나</p><ul class="pts">%s</ul>'
                 % ''.join('<li>%s</li>' % p for p in w['points']))
    evt = [t for t in w['triggers'] if t['kind'] == wl.KIND_EVENT]
    if evt:
        h.append(tbl('사람이 확인하는 것',
                     ['무엇을 확인하나', '언제 판단이 바뀌나', '걸리면', '어디서 확인하나'],
                     [[E(t['what']), E(t['cond']),
                       wl.md_inline(t['act']) if t['act'] else '<span class="t-none">—</span>',
                       link_out(t['where'])] for t in evt]))
    if w['clash']:
        h.append('<p class="lbl">반대 근거</p><ul class="pts">%s</ul>'
                 % ''.join('<li>%s</li>' % c for c in w['clash']))
    h.append('</section>')
    return ''.join(h)


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


def line_summary_rows(watches):
    """본 장의 「보고 있는 것」 목록 — 이름·판정 왼쪽, 칩·마지막 확인 오른쪽.
    부동산 넷을 먼저, 제도 여섯을 그다음에 묶는다."""
    ordered = sorted(watches,
                     key=lambda w: (0 if w['kind'] == 'realestate' else 1, w['slug']))
    h, cur = [], None
    for w in ordered:
        g = 0 if w['kind'] == 'realestate' else 1
        if g != cur:
            h.append('<p class="lbl">%s</p>' % ('부동산' if g == 0 else '제도'))
            cur = g
        vals = [t for t in w['triggers'] if t['kind'] == wl.KIND_VALUE]
        states = [wl.state_now(t['cond'], t['series'])[0] for t in vals]
        n_hit, n_near = states.count('걸림'), states.count('근접')
        chip = (('<span class="tag t-hit">걸림 %d</span> ' % n_hit if n_hit else '') +
                ('<span class="tag t-near">근접 %d</span>' % n_near if n_near else ''))
        verdict = w.get('verdict') or _first_sentence(w['judged'])
        h.append('<div class="wline"><a class="wline-t" href="watch/%s.html">%s</a>'
                 '<span class="wline-chip">%s</span>'
                 '<p class="wline-v">%s</p>'
                 '<span class="wline-d mono">마지막 확인 %s</span></div>'
                 % (w['slug'], E(title_of(w)), chip, E(verdict), E(w['checked'] or '—')))
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
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s — 포트폴리오 워치</title>%s<style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#lines">'
            '← 포트폴리오 워치</a>'
            '<header><p class="meta mono">%s · %s · 마지막 확인 %s</p><h1>%s</h1>'
            '<p class="verdict">%s</p></header>'
            '<div class="dbody">%s</div>'
            '<footer>이 화면은 <code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
            '</div></body></html>'
            % (E(t9), FONTS, CSS, E(_area_head(w['target'])), E(view), E(w['checked'] or '—'),
               E(t9), E(verdict), line_block(w)))


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
            '<footer>이 화면은 <code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
            '</div></body></html>'
            % (FONTS, CSS, len(_laws_grouped(watches)), body))


# 은어 넷 — 저장소 안에서만 통하는 말이 화면에 그대로 나가면 안 된다. 「걸림」·「근접」은
# 칩으로 남기되(뜻을 subtitle 에 한 번 적는다), 나머지 넷은 절 제목·목록 이름·열
# 이름으로 못 쓴다.
_JARGON = ('때 자', '<th>성격</th>', '<th>언제 것</th>')


def check_ui(html, watches):
    """본 장의 규약. 아카이브 규약(check_ui)에서 나온 장이라 규약이 없어지면 안 된다.

    2026-09-02 세 번째 개정 — 값이 아니라 메타데이터가 맨 위에 서던 문제와, 저장소
    은어가 화면에 그대로 나가던 문제를 검사기로 막는다. 도해는 이제 둘(전세가율
    자·자료 기준 자)이고, 표는 상세로 다 옮겨서 본 장엔 없어도 된다(상한만 셋)."""
    assert 'is-fold' not in html and 'uc-caret' not in html, \
        '규약 위반: 접는 것을 두지 않는다 — 열면 다 보여야 한다'
    assert 'class="stile' not in html, \
        '규약 위반: 타일을 두지 않는다 — 고르는 계층은 탭 하나다'
    assert 'class="line"' not in html, \
        '규약 위반: 줄 상세는 본 장에 없다 — watch/<슬러그>.html 로 옮겼다'
    at_fired = html.find('지난번 본 뒤 바뀐 것')
    at_lines = html.find('id="lines"')
    assert 0 < at_fired < at_lines, \
        '규약 위반: 「지난번 본 뒤 바뀐 것」이 「보고 있는 것」보다 먼저 서야 한다'
    assert '값이 언제 것인가' in html, '규약 위반: 자료 기준 자가 없다 — 값의 나이를 먼저 보인다'
    n_fig = html.count('<figure')
    assert n_fig == 2, \
        '규약 위반: 본 장의 <figure 는 전세가율 자 + 자료 기준 자 둘이어야 한다 (%d개)' % n_fig
    n_tbl = html.count('<table')
    assert n_tbl <= 3, '규약 위반: 본 장의 <table 은 셋 이하여야 한다 (%d개)' % n_tbl
    for term in _JARGON:
        assert term not in html, '규약 위반: 은어 "%s" 가 화면에 남아 있다' % term
    assert '>줄</p>' not in html and '>줄</a>' not in html, \
        '규약 위반: 「줄」을 절 제목·목록 이름으로 썼다'
    # 도해 배치는 눈이 아니라 검사기가 본다. 자는 점이 몰리면 글자가 겹치는데
    # 화면을 못 볼 때는 그걸 알 길이 없다 — 실제로 다섯 쌍이 겹친 채로 나갈 뻔했다
    sys.path.insert(0, HERE)
    import check_fig
    for m in re.finditer(r'<svg[^>]*>.*?</svg>', html, re.S):
        bad = check_fig.hits(m.group(0))
        assert not bad, '규약 위반: 도해 배치 — %s' % ' · '.join(bad)


def check_detail_ui(watches):
    """줄 상세 페이지의 규약. 본 장에서 걷어낸 검사(도해 배치·「기준」 열·은어)를
    상세 파일 전부로 돌린다 — 옮겼다고 검사까지 놓치면 안 된다."""
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
        assert html.count('<th>기준</th>') >= 1 or n == 0, \
            '규약 위반(%s): 값을 내면서 「기준」 열이 없다' % w['slug']
        for term in _JARGON:
            assert term not in html, '규약 위반(%s): 은어 "%s" 가 남아 있다' % (w['slug'], term)
    law_path = os.path.join(WATCH_DIR, '제도.html')
    assert os.path.exists(law_path), '규약 위반: watch/제도.html 이 없다'
    law_html = io.open(law_path, encoding='utf-8').read()
    for term in _JARGON:
        assert term not in law_html, '규약 위반(제도): 은어 "%s" 가 남아 있다' % term


def build():
    ws = wl.load_all()
    snap = wl.load_seen()      # 지난 확인 스냅숏. 아래 tab 라벨 목록(seen)과 이름이 겹쳐 갈랐다
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
             '<p class="lede">서울 세 권역, 지금 들어가는 조건을 봅니다 — 전세냐 매매냐, '
             '깎을 수 있는 장이냐, 제도가 셈을 바꿨냐.</p>' % (E(checked), E(asof)))
    # 절 바로가기 — 앵커다. 저장소 규칙(관문 버튼 금지)은 내용을 가리는 버튼을
    # 말한다(스킨 첫 화면에서 카드를 숨기고 그 앞을 막는 것). 이 줄은 아래 다섯
    # 절을 전부 그대로 펼쳐 두고 그 자리로 뛰는 것만 돕는다 — 걸러 내지 않는다.
    h.append('<nav class="jump" aria-label="절 바로가기">'
             '<a href="#areas">권역</a><a href="#since">바뀐 것</a>'
             '<a href="#policy">제도</a><a href="#lines">보고 있는 것</a>'
             '<a href="#basis">자료 기준</a></nav>')
    h.append('</header>')

    h.append('<section class="hero" id="areas">%s%s</section>'
             % (ratio_ruler_fig(ws), area_cards(ws)))

    h.append('<div class="band" id="since"><p class="band-t">지난번 본 뒤 바뀐 것</p>%s</div>'
             % since_block(ws, snap))
    h.append('<div class="band" id="policy"><p class="band-t">제도</p>'
             '<p class="band-s">제도는 값으로 안 옵니다. 지금 어느 판인가만 기계가 알고, '
             '바뀐 내용은 사람이 조문을 열어 읽습니다.</p>%s</div>' % law_summary(ws))

    h.append('<div class="band" id="lines"><p class="band-t">보고 있는 것 %d</p>%s</div>'
             % (len(ws), line_summary_rows(ws)))

    h.append('<div class="band" id="basis"><p class="band-t">값이 언제 것인가</p>%s</div>'
             % time_ruler_fig(ws))

    h.append('<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
             '마지막 확인 %s · 통계 기준 %s. 줄 상세는 <code>watch/</code> 아래에 있습니다. '
             '판단은 <code>insights/watch/</code>, 수치는 '
             '<code>insights/watch/_metrics/</code>, 이 화면은 '
             '<code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
             % (E(checked), E(asof)))
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
