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
"""
import io
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
E = wl.esc

KIND_LABEL = {'realestate': '부동산', 'policy': '제도', 'equity': '종목'}

# 재 섞인 흰 바탕에 먹녹. 걸림은 벽돌, 근접은 황토, 평온은 짙은 청록.
# 색은 「지금 어떤가」에만 쓴다 — 값의 성격까지 색으로 가르면 화면이 알록달록해지고
# 정작 걸린 줄이 안 튄다.
CSS = """
:root{
  --paper:#F2F4F3; --ink:#17211F; --ink-2:#3C4A46; --ink-3:#6E7B77;
  --rule:#C9D2CE; --surface:#FBFCFB; --line:#C9D2CE;
  --hit:#B4451F; --near:#C08A2E; --calm:#2E6E63;
  --fig-blue:#2E6E63; --fig-good:#B4451F; --warn:#C08A2E;
}
@media (prefers-color-scheme:dark){:root{
  --paper:#101614; --ink:#E6EBE9; --ink-2:#B4C0BC; --ink-3:#7E8C87;
  --rule:#2A3633; --surface:#161E1B; --line:#2A3633;
  --hit:#E0703F; --near:#D9A64A; --calm:#5FA79A;
  --fig-blue:#5FA79A; --fig-good:#E0703F; --warn:#D9A64A;
}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
  font:400 15px/1.7 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  font-variant-numeric:tabular-nums}
.wrap{max-width:960px;margin:0 auto;padding:0 20px 80px}
header{padding:34px 0 0}
h1{font-size:1.5rem;font-weight:850;letter-spacing:-.02em;margin:0}
.eyebrow{font-size:10.5px;font-weight:850;letter-spacing:.16em;color:var(--ink-3);margin:0 0 7px}
.lede{color:var(--ink-2);font-size:.93rem;max-width:64ch;margin:14px 0 0}
.back{display:inline-block;margin:22px 0 0;font-size:.82rem;font-weight:700;
  color:var(--ink-3);border-bottom:0}
.back:hover,.back:focus-visible{color:var(--ink)}
.dbody{margin:26px 0 0}
.band{margin:40px 0 0;border-top:2px solid var(--ink);padding-top:11px}
.band-t{font-size:11px;font-weight:850;letter-spacing:.14em;margin:0}
.band-s{font-size:.85rem;color:var(--ink-3);margin:5px 0 0;max-width:64ch}
.rows{margin:14px 0 0}
.row{display:grid;grid-template-columns:auto 1fr auto;gap:2px 14px;align-items:baseline;
  padding:10px 0;border-bottom:1px solid var(--rule)}
.row:last-child{border-bottom:0}
.row-where{font-size:.8rem;color:var(--ink-3)}
.row-what{font-weight:700}
.row-num{font-size:1.05rem;font-weight:600;white-space:nowrap}
.row-why{grid-column:2/-1;font-size:.83rem;color:var(--ink-3)}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px}
.d-hit{background:var(--hit)}
.d-near{background:transparent;border:2px solid var(--near)}
.tag{font-size:10.5px;font-weight:850;letter-spacing:.06em;padding:1px 7px;
  border-radius:2px;white-space:nowrap}
.t-hit{background:var(--hit);color:#fff}
.t-near{border:1px solid var(--near);color:var(--near)}
.t-calm{color:var(--calm)}
.t-none{color:var(--ink-3)}
table{width:100%;border-collapse:collapse;margin:12px 0 0;font-size:.88rem}
th{text-align:left;font-size:10px;font-weight:850;letter-spacing:.1em;color:var(--ink-3);
  border-bottom:1.5px solid var(--ink);padding:0 12px 7px 0;white-space:nowrap}
td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule);vertical-align:baseline}
td:first-child{font-weight:700}
.tw{overflow-x:auto}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--rule)}
a:hover,a:focus-visible{border-bottom-color:var(--ink)}
/* 줄 목록 — 이름·문장·수치 세 줄. 탭·카드 대신 훑어 내려가는 목록 하나다 */
.wline{margin:14px 0 0;padding:12px 0;border-bottom:1px solid var(--rule)}
.wline:last-child{border-bottom:0}
.wline-t{display:block;font-weight:800;font-size:1rem;border-bottom:0}
.wline-s{margin:4px 0 0;font-size:.88rem;color:var(--ink-2)}
.wline-s b{color:var(--ink);font-weight:800}
.wline-n{margin:4px 0 0;font-size:.8rem;color:var(--ink-3)}
.wline-n b{color:var(--ink-2);font-weight:800}
.line{margin:34px 0 0;padding:20px 0 0;border-top:1px solid var(--rule)}
.line-why{color:var(--ink-2);font-size:.9rem;margin:6px 0 0}
.line-judge{margin:13px 0 0;font-size:.94rem;line-height:1.75;color:var(--ink-2)}
.line-judge b{color:var(--ink);font-weight:800}
ul.pts{margin:12px 0 0;padding-left:18px}
ul.pts li{margin:0 0 8px;font-size:.9rem;color:var(--ink-2)}
ul.pts li b{color:var(--ink)}
.lbl{font-size:10px;font-weight:850;letter-spacing:.1em;color:var(--ink-3);margin:22px 0 0}
figure{margin:9px 0 0}
figure svg{width:100%;height:auto;display:block}
/* 도해는 넓은 판·좁은 판 둘을 싣고 화면 폭으로 하나만 보인다. 줄여 그리면 글자가
   7px 이 되고 최소폭을 두면 오른쪽 끝(제일 최근 달)이 화면 밖으로 나간다 */
svg.fig-n{display:none}
figcaption{font-size:.78rem;color:var(--ink-3);margin:5px 0 0}
.t-sm{font-size:13px;fill:var(--ink-2)}
.t-axis{fill:var(--ink-3)}
.grid{stroke:var(--rule);stroke-width:1;fill:none}
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
  /* 설명을 오른쪽 auto 칸에 두면 그 칸이 긴 문장을 다 먹고 왼쪽 제목이 한 자씩
     세로로 떨어진다(매/매/가/격/지/수). 설명은 제 줄로 내리고 제목은 낱말로 접는다 */
  .row{grid-template-columns:minmax(0,1fr) auto;gap:3px 10px}
  .row-where,.row-why{grid-column:1/-1}
  .row-what{word-break:keep-all;overflow-wrap:anywhere}
  .tw{overflow-x:visible}
  table,thead,tbody,tr,td{display:block;width:100%}
  thead{display:none}
  tr{padding:11px 0;border-bottom:1px solid var(--rule)}
  tr:last-child{border-bottom:0}
  td{display:flex;gap:10px;align-items:baseline;border:0;padding:2px 0}
  td::before{content:attr(data-th);flex:0 0 8.5em;font-size:10px;font-weight:850;
    letter-spacing:.08em;color:var(--ink-3);line-height:1.9}
  td:first-child{font-size:1.02rem;padding-bottom:5px}
  td:first-child::before{display:none}
  svg.fig-w{display:none}
  svg.fig-n{display:block}
  .band{margin-top:32px}
  .line{margin-top:28px}
}
"""


def title_of(w):
    return '%s — %s' % (w['target'], w['view']) if w.get('view') else w['target']


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
    cls = {'걸림': 't-hit', '근접': 't-near', '같다': 't-calm'}.get(state, 't-none')
    return '<span class="tag %s">%s</span>' % (cls, E(state))


def _months(t):
    m = re.match(r'^(\d{4})-(\d{2})', str(t))
    return int(m.group(1)) * 12 + int(m.group(2)) if m else None


def time_ruler(watches, W=640):
    """시그니처 — 값의 나이를 먼저 보여 준다.

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
        o.append('<circle cx="%.1f" cy="%d" r="%.1f" fill="var(--calm)"/>' % (x, Y, r))
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
    sub = ('아직 확인한 적이 없다 — 전부 새로 걸린 것으로 센다' if seen is None else
           '지난 확인 %s 이후' % E(seen.get('checked') or '—'))
    if total == 0:
        return ('<p class="band-s">%s. 조건에 든 값도, 내가 읽은 뒤에 바뀐 법도 없습니다. '
                '이번 달은 볼 것이 없습니다.</p>' % sub)
    h = ['<p class="band-s">%s.</p>' % sub]
    for name in ('새로 걸린', '새로 근접', '풀린', '그대로 걸린'):
        rows = buckets[name]
        if not rows:
            continue        # 묶음이 비면 그 묶음 제목을 안 낸다
        h.append('<p class="lbl">%s <b>%d</b></p><div class="rows">' % (E(name), len(rows)))
        prev = None
        for t9, wslug, what, val, cond, st, why, asof in rows:
            # 같은 줄이 잇달아 서면 이름을 되풀이하지 않는다 — 세 번 같은 이름이 서면
            # 눈이 그 열을 통째로 건너뛴다
            label = '' if t9 == prev else E(t9)
            prev = t9
            h.append('<div class="row"><span class="row-where">'
                     '<span class="dot %s"></span><a href="watch/%s.html">%s</a></span>'
                     '<span class="row-what">%s</span>'
                     '<span class="row-num">%s</span>'
                     '<span class="row-why">%s · %s · %s</span></div>'
                     % ('d-hit' if st == '걸림' else 'd-near', wslug, label, E(what),
                        E(val), E(cond), E(why), E(asof)))
        h.append('</div>')
    return ''.join(h)


def area_table(watches):
    live = [w for w in watches
            if w['kind'] == 'realestate'
            and any(k.startswith('jeonse_ratio_') for k in (w['metrics'] or {}))]
    rows = []
    for w in live:
        rs = [m['value'] for k, m in (w['metrics'] or {}).items()
              if k.startswith('jeonse_ratio_')]
        sd = (w['metrics'] or {}).get('supply_demand')
        n = sum(1 for t in w['triggers'] if t['kind'] == wl.KIND_VALUE
                and wl.state_now(t['cond'], t['series'])[0] in ('걸림', '근접'))
        asof = next((m['as_of'] for k, m in (w['metrics'] or {}).items()
                     if k.startswith('jeonse_ratio_')), '—')
        rows.append(['<a href="watch/%s.html">%s</a>' % (w['slug'], E(w['target'])),
                     '%.2f ~ %.2f' % (min(rs), max(rs)) if rs else '—',
                     '전세금의 %.1f배' % (100.0 / (sum(rs) / len(rs))) if rs else '—',
                     ('%s <span class="t-none">%s</span>' % (sd['value'], E(sd['area']))
                      if sd else '못 붙임'),
                     ('<b>%d</b>' % n) if n else '0', E(asof), '공표'])
    rows.sort(key=lambda r: r[1], reverse=True)
    return tbl('권역마다 지금 어떤가',
               ['권역', '전세가율(구별 범위)', '매매로 넘어가는 문턱', '수급동향',
                '걸림·근접', '언제 것', '성격'], rows)


def _laws_grouped(watches):
    """법·고시 이름 → {지금 판·내가 읽은 판들·이 법을 보는 줄(제목, 슬러그)}.

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
    것이 본 장의 「제도」 요약(law_summary)이고, 전체는 여기 있다. prefix 는 보는 줄
    링크가 상대 경로로 어디를 가리켜야 하는지다. watch/ 폴더 안에서 부르므로 같은
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
               ['법·고시', '지금 판', '내가 읽은 판', '같은가', '보는 줄', '성격'], rows)


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
            h.append('<div class="row"><span class="row-where">'
                     '<span class="dot d-hit"></span>%s</span>'
                     '<span class="row-what">%s → %s</span>'
                     '<span class="row-why">보는 줄 %s</span></div>'
                     % (E(name), E(' · '.join(sorted(e['seen']))), E(e['now']), who))
        h.append('</div>')
    h.append('<p class="lbl"><a href="watch/제도.html">전체 표 →</a></p>')
    return ''.join(h)


def figures(w):
    """도해. series 가 든 metric 만 그린다 — 어댑터가 안 채운 자리에는 아무것도 안 선다.

    그 metric 을 건 값 트리거가 있으면 그 조건이 걸렸던 달을 선 위에 빈 원으로
    찍는다(wl.fired_months) — 표의 「이력 N개월 중 k번」과 같은 판정을 그림으로도
    보게 하는 자리다.

    2026-09-02 — 값 트리거가 건 metric 의 도해를 앞에 세운다. 상세 페이지를 여는
    이유가 그 값(실거주 줄이면 전세가율, 강남3구 매매 줄이면 매매가격지수)이지
    나머지 참고용 시계열이 아니다. sorted() 가 안정 정렬이라 우선순위가 같은 것들
    끼리는 원래 순서(열쇠 이름 알파벳)가 그대로 유지된다."""
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
    for (base, unit), items in sorted(groups.items(), key=_prio):
        sel = items[:3]
        note = ' · '.join(dict.fromkeys(m.get('src', '') for _n, m, _k in sel if m.get('src')))
        ser = [(n, [tuple(x) for x in m['series']]) for n, m, _k in sel]
        marks = []
        for _n, m, key in sel:
            t = trig_by_metric.get(key)
            s = [tuple(x) for x in m['series']]
            marks.append(wl.fired_months(t['cond'], s) if t else [])
        svg = wf.trend(ser, unit or '값', note=note, marks=marks)
        if svg:
            nsvg = wf.trend(ser, unit or '값', note=note, narrow=True, marks=marks)
            out.append('<figure>%s%s<figcaption>%s</figcaption></figure>'
                       % (svg.replace('<svg ', '<svg class="fig-w" ', 1),
                          nsvg.replace('<svg ', '<svg class="fig-n" ', 1),
                          E(TITLE.get(base, base))))
    return ''.join(out)


def hist_note(cond, series):
    """「걸리는 조건」 칸 아래 작은 글씨 — 이력 몇 달 중 몇 번 걸렸나(check_watch W8 과
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

    2026-09-02 이전에는 이 함수가 본 장 안에 h2 를 단 <section> 을 쭉 늘어놓아 화면을
    만들었다. 지금은 줄마다 제 파일을 가지므로 제목은 그 페이지의 h1 이 이미 말하고
    있다 — 여기서 다시 h2 로 되풀이하지 않는다."""
    h = ['<section class="line">']
    h.append('<p class="line-why">%s</p>' % E(w['why']))
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
                         E(t['as_of'] or '—'), E(t['nature'] or '자리표시')])
        h.append(tbl('무엇이 일어나면 판단이 바뀌나 — 값으로 오는 것',
                     ['무엇을', '지금', '걸리는 조건', '상태', '걸리면', '언제 것', '성격'],
                     rows))
    if w.get('laws'):
        rows = []
        for _tg, name, seen in w['laws']:
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            st = '—' if not now or not seen else ('같다' if str(now) == seen else '걸림')
            rows.append([E(name), E(seen or '—'), E(now or '아직 안 받음'), tag(st)])
        h.append(tbl('내가 읽은 판과 지금 판',
                     ['법·고시', '내가 읽은 판', '지금 판', '같은가'], rows))
    # 도해를 「왜 보나」보다 앞에 둔다 — 그 절의 글보다 그림이 먼저 서야 한다는 이
    # 저장소의 도해 규칙(CLAUDE.md)이 줄 하나짜리 상세 페이지에도 그대로 적용된다.
    fig = figures(w)
    if fig:
        h.append(fig)
    if w['points']:
        h.append('<p class="lbl">왜 보나</p><ul class="pts">%s</ul>'
                 % ''.join('<li>%s</li>' % p for p in w['points']))
    evt = [t for t in w['triggers'] if t['kind'] == wl.KIND_EVENT]
    if evt:
        h.append(tbl('값으로 안 오는 것 — 사람이 확인한다',
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
    """줄 목록의 「지금 판단」 요약 한 줄 — 첫 볼드 문장, 없으면 첫 문장.

    judged 는 이미 **굵게**가 <b> 로 풀린 HTML 이다(watch_lib.md_inline). 판단
    문단 전체를 목록에 실으면 세 줄 예산을 넘으니, 그 문단에서 가장 힘줘 쓴 자리
    (볼드)나 그것도 없으면 첫 문장만 뽑는다."""
    m = re.search(r'<b>(.*?)</b>', judged, re.S)
    if m:
        return m.group(1)
    text = re.sub(r'<[^>]+>', '', judged).strip()
    idx = text.find('.')
    return text[:idx + 1] if idx >= 0 else text


def line_summary_rows(watches):
    """본 장의 「줄」 목록 — 이름·문장·수치 세 줄짜리 행. 탭 대신 훑어 내려가는
    목록 하나로 둔다. 부동산 넷을 먼저, 제도 여섯을 그다음에 묶는다."""
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
        n_hit = states.count('걸림')
        n_near = states.count('근접')
        h.append('<div class="wline"><a class="wline-t" href="watch/%s.html">%s</a>'
                 '<p class="wline-s">%s</p>'
                 '<p class="wline-n">걸림 <b>%d</b> · 근접 <b>%d</b> · 마지막 확인 %s</p></div>'
                 % (w['slug'], E(title_of(w)), _first_sentence(w['judged']),
                    n_hit, n_near, E(w['checked'] or '—')))
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
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>%s — 포트폴리오 워치</title><style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#lines">'
            '← 포트폴리오 워치</a>'
            '<header><p class="eyebrow">%s · %s · 마지막 확인 %s</p><h1>%s</h1></header>'
            '<div class="dbody">%s</div>'
            '<footer>이 화면은 <code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
            '</div></body></html>'
            % (E(t9), CSS, E(w['target']), E(view), E(w['checked'] or '—'), E(t9),
               line_block(w)))


def law_page(watches):
    """법·고시 전체 표 페이지 — 대시보드/watch/제도.html.

    본 장 「제도」 요약이 「전체 표 →」로 여기를 가리킨다. 표 아래에 정책 줄로 가는
    링크도 둔다 — 표의 「보는 줄」 칸에 이미 있지만, 여섯 줄을 한눈에 훑을 목록이
    따로 있는 편이 낫다."""
    policy_ws = sorted((w for w in watches if w['kind'] == 'policy'),
                       key=lambda w: w['slug'])
    links = ''.join('<div class="wline"><a class="wline-t" href="%s.html">%s</a></div>'
                    % (w['slug'], E(title_of(w))) for w in policy_ws)
    body = law_table_full(watches, prefix='') + '<p class="lbl">이 법·고시를 보는 줄</p>' + links
    # 앵커(#policy)가 필요한 이유는 detail_page()와 같다 — rewrite_links()가
    # 「../<파일명>.html#<앵커>」꼴만 /watch#policy로 바꾼다.
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>제도 — 포트폴리오 워치</title><style>%s</style></head><body>'
            '<div class="wrap"><a class="back" href="../포트폴리오 워치.html#policy">'
            '← 포트폴리오 워치</a>'
            '<header><p class="eyebrow">법·고시 %d개</p><h1>제도</h1></header>'
            '<div class="dbody">%s</div>'
            '<footer>이 화면은 <code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
            '</div></body></html>'
            % (CSS, len(_laws_grouped(watches)), body))


def check_ui(html, watches):
    """본 장의 규약. 아카이브 규약(check_ui)에서 나온 장이라 규약이 없어지면 안 된다.

    2026-09-02 에 규약을 다시 세웠다 — 줄 상세를 watch/ 로 옮기면서 본 장에 남는
    것은 요약뿐이라, 도해는 때 자 하나, 표는 권역 견주기 하나뿐이어야 한다.
    「언제 것」 열 단언은 이제 상세 파일 쪽 몫이다(check_detail_ui)."""
    assert 'is-fold' not in html and 'uc-caret' not in html, \
        '규약 위반: 접는 것을 두지 않는다 — 열면 다 보여야 한다'
    assert 'class="stile' not in html, \
        '규약 위반: 타일을 두지 않는다 — 고르는 계층은 탭 하나다'
    assert 'class="line"' not in html, \
        '규약 위반: 줄 상세는 본 장에 없다 — watch/<슬러그>.html 로 옮겼다'
    at_fired = html.find('지난 확인 이후')
    at_lines = html.find('id="lines"')
    assert 0 < at_fired < at_lines, \
        '규약 위반: 「지난 확인 이후」가 줄 목록보다 먼저 서야 한다'
    assert '값이 언제 것인가' in html, '규약 위반: 때 자가 없다 — 값의 나이를 먼저 보인다'
    n_fig = html.count('<figure')
    assert n_fig == 1, '규약 위반: 본 장의 <figure 는 때 자 하나여야 한다 (%d개)' % n_fig
    n_tbl = html.count('<table')
    assert n_tbl <= 3, '규약 위반: 본 장의 <table 은 셋 이하여야 한다 (%d개)' % n_tbl
    # 도해 배치는 눈이 아니라 검사기가 본다. 때 자는 점이 몰리면 글자가 겹치는데
    # 화면을 못 볼 때는 그걸 알 길이 없다 — 실제로 다섯 쌍이 겹친 채로 나갈 뻔했다
    sys.path.insert(0, HERE)
    import check_fig
    for m in re.finditer(r'<svg[^>]*>.*?</svg>', html, re.S):
        bad = check_fig.hits(m.group(0))
        assert not bad, '규약 위반: 도해 배치 — %s' % ' · '.join(bad)


def check_detail_ui(watches):
    """줄 상세 페이지의 규약. 본 장에서 걷어낸 검사(도해 배치·「언제 것」 열)를
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
        assert html.count('<th>언제 것</th>') >= 1 or n == 0, \
            '규약 위반(%s): 값을 내면서 「언제 것」 열이 없다' % w['slug']
    law_path = os.path.join(WATCH_DIR, '제도.html')
    assert os.path.exists(law_path), '규약 위반: watch/제도.html 이 없다'


def build():
    ws = wl.load_all()
    snap = wl.load_seen()      # 지난 확인 스냅숏. 아래 tab 라벨 목록(seen)과 이름이 겹쳐 갈랐다
    # 통계 기준월과 법 시행일은 성격이 다르다. max 로 뭉치면 「자료 기준」에 법 시행일이
    # 올라와 통계가 실제보다 새 것처럼 읽힌다 — 이 장이 값에 「언제 것 · 성격」을 붙이는
    # 이유를 머리에서 어기는 자리였다
    stat = [m.get('as_of', '') for w in ws for m in (w['metrics'] or {}).values()
            if m.get('level') != 'law']
    laws = [m.get('as_of', '') for w in ws for m in (w['metrics'] or {}).values()
            if m.get('level') == 'law']
    asof = max(stat or ['—'])
    lawof = max(laws or ['—'])
    checked = max([w['checked'] for w in ws if w.get('checked')] or ['—'])

    h = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width, initial-scale=1">',
         '<title>포트폴리오 워치</title><style>%s</style></head><body><div class="wrap">' % CSS]
    h.append('<header><p class="eyebrow">보고 있는 것 %d · 통계 %s · 제도 %s</p>'
             '<h1>포트폴리오 워치</h1>'
             '<p class="lede">서울 세 권역을 보고 있습니다. 집값이 오를지가 아니라 '
             '<b>지금 들어가는 조건</b>을 봅니다 — 전세와 매매 중 어느 쪽이 나은지, 값을 '
             '깎을 수 있는 장인지, 제도가 그 셈을 바꿨는지. 보유 자산이 아니라 관찰이라 '
             '손익과 비중은 다루지 않습니다.</p>'
             % (len(ws), E(asof), E(lawof)))
    h.append(time_ruler_fig(ws))
    h.append('</header>')

    h.append('<div class="band"><p class="band-t">지난 확인 이후</p>%s</div>' % since_block(ws, snap))
    h.append('<div class="band"><p class="band-t">권역 견주기</p>'
             '<p class="band-s">전세가율은 한 수가 두 방향으로 읽힙니다. 올라가면 보증금이 '
             '집값에 가까워지고, 동시에 매매로 넘어가는 데 드는 자기 돈이 줄어듭니다.</p>'
             '%s</div>' % area_table(ws))
    h.append('<div class="band" id="policy"><p class="band-t">제도</p>'
             '<p class="band-s">제도는 값으로 안 옵니다. 지금 어느 판인가만 기계가 알고, '
             '바뀐 내용은 사람이 조문을 열어 읽습니다.</p>%s</div>' % law_summary(ws))

    h.append('<div class="band" id="lines"><p class="band-t">줄</p>%s</div>'
             % line_summary_rows(ws))

    h.append('<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
             '마지막 확인 %s · 통계 기준 %s. 줄 상세는 <code>watch/</code> 아래에 있습니다. '
             '줄은 <code>insights/watch/</code>, 수치는 '
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
