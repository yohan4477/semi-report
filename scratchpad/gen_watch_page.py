# -*- coding: utf-8 -*-
"""포트폴리오 워치 — 감시 화면. 아카이브 부품(dash_common)을 안 쓴다.

왜 따로 짰나. 아카이브는 카드가 쌓이니 접어서 고르게 만든 부품이고, 이 장은 열 줄이
안 늘고 매달 같은 것을 다시 본다. 접힘·타일·카드 세 겹이 「무엇이 바뀌었나」 앞을
막아서, 두 번 우회한 뒤(home='all' · tiles=False) 뼈대째 걷었다.

규약은 check_ui() 가 생성 때 검사한다. 규약을 우회하려고 나온 장이 규약이 없는 장이
되면 다음 사람이 같은 자리를 다시 판다.
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
E = wl.esc

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
.tabs{display:flex;flex-wrap:wrap;gap:7px;margin:18px 0 0}
.tabs button{font:inherit;font-size:.85rem;font-weight:700;color:var(--ink-2);background:none;
  border:1px solid var(--rule);border-radius:2px;padding:5px 13px;cursor:pointer}
.tabs button[aria-pressed=true]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.tabs button:focus-visible{outline:2px solid var(--calm);outline-offset:2px}
.line{margin:34px 0 0;padding:20px 0 0;border-top:1px solid var(--rule)}
.line h2{font-size:1.08rem;font-weight:850;margin:0;letter-spacing:-.01em}
.line-why{color:var(--ink-2);font-size:.9rem;margin:6px 0 0}
.line-judge{margin:13px 0 0;font-size:.94rem;line-height:1.75;color:var(--ink-2)}
.line-judge b{color:var(--ink);font-weight:800}
ul.pts{margin:12px 0 0;padding-left:18px}
ul.pts li{margin:0 0 8px;font-size:.9rem;color:var(--ink-2)}
ul.pts li b{color:var(--ink)}
.lbl{font-size:10px;font-weight:850;letter-spacing:.1em;color:var(--ink-3);margin:22px 0 0}
figure{margin:9px 0 0}
figure svg{width:100%;height:auto;display:block}
figcaption{font-size:.78rem;color:var(--ink-3);margin:5px 0 0}
.t-sm{font-size:13px;fill:var(--ink-2)}
.t-axis{fill:var(--ink-3)}
.grid{stroke:var(--rule);stroke-width:1;fill:none}
footer{margin:60px 0 0;padding-top:16px;border-top:2px solid var(--ink);
  font-size:.8rem;color:var(--ink-3)}
code{font-size:.85em;background:var(--surface);padding:1px 5px;border-radius:2px}
@media (max-width:620px){
  .row{grid-template-columns:1fr auto}
  .row-where{grid-column:1/-1}
}
"""

TAB_JS = """
(function(){
  var tabs=document.querySelector('.tabs');
  if(!tabs) return;
  function apply(pick){
    document.querySelectorAll('.line').forEach(function(s){
      s.hidden = pick!=='all' && s.dataset.pick!==pick;
    });
    tabs.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.pick===pick));
    });
  }
  tabs.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(b) apply(b.dataset.pick);
  });
})();
"""


def slug(t):
    return 'w-' + re.sub(r'[^0-9A-Za-z가-힣]+', '-', t).strip('-')


def title_of(w):
    return '%s — %s' % (w['target'], w['view']) if w.get('view') else w['target']


def tbl(cap, head, rows):
    if not rows:
        return ''
    return ('<p class="lbl">%s</p><div class="tw"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>'
            % (E(cap), ''.join('<th>%s</th>' % E(h) for h in head),
               ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in rows)))


def tag(state):
    cls = {'걸림': 't-hit', '근접': 't-near', '같다': 't-calm'}.get(state, 't-none')
    return '<span class="tag %s">%s</span>' % (cls, E(state))


def _months(t):
    m = re.match(r'^(\d{4})-(\d{2})', str(t))
    return int(m.group(1)) * 12 + int(m.group(2)) if m else None


def time_ruler(watches):
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
    W, X0, X1, Y = 920, 24, 896, 66

    def px(a):
        return X0 + (X1 - X0) * ((xs[a] - lo) / float(hi - lo) if hi > lo else .5)

    o = ['<line x1="%d" y1="%d" x2="%d" y2="%d" class="grid"/>' % (X0, Y, X1, Y)]
    order = sorted(pts, key=lambda a: xs[a])
    for i, a in enumerate(order):
        x, n = px(a), len(pts[a])
        r = 3.5 + min(n, 12) * .5
        up = (i % 2 == 0)
        o.append('<circle cx="%.1f" cy="%d" r="%.1f" fill="var(--calm)"/>' % (x, Y, r))
        if up:
            o.append('<line x1="%.1f" y1="34" x2="%.1f" y2="%.1f" class="grid"/>'
                     % (x, x, Y - r - 3))
        else:
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="98" class="grid"/>'
                     % (x, Y + r + 3, x))
        anc = 'start' if i == 0 else ('end' if i == len(order) - 1 else 'middle')
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="%s" '
                 'style="font-size:11px">%s</text>' % (x, 28 if up else 112, anc, E(a)))
        o.append('<text x="%.1f" y="%d" class="t-sm" text-anchor="%s" '
                 'style="font-size:11px;font-weight:800">%d</text>'
                 % (x, 14 if up else 126, anc, n))
    gap = (xs[order[-1]] - xs[order[0]]) // 12
    who = ' · '.join(sorted(set(pts[order[0]]))[:2])
    note = ('가장 오래된 것이 %s(%s), 가장 새 것이 %s입니다 — %d년 넘게 벌어져 있습니다. '
            '왼쪽 끝이 오래됐다는 것은 그 자료가 그 뒤로 안 바뀌었다는 뜻입니다.'
            % (who, order[0], order[-1], gap)) if gap >= 1 else \
           ('%s부터 %s까지 들어와 있습니다.' % (order[0], order[-1]))
    return ('<figure><svg viewBox="0 0 %d 134" role="img" aria-label="값이 언제 것인가">'
            '%s</svg><figcaption>%s 점 크기는 그 때에 딸린 값의 개수입니다.</figcaption>'
            '</figure>' % (W, ''.join(o), E(note)))


def fired(watches):
    """지금 걸린 것과 가까이 온 것. 값 트리거와 법 개정을 한자리에 놓는다 —
    둘 다 「내가 본 뒤에 무엇이 달라졌나」에 답한다."""
    rows = []
    for w in watches:
        t9 = title_of(w)
        for t in w['triggers']:
            if t['kind'] != wl.KIND_VALUE:
                continue
            st, why = wl.state_now(t['cond'], t['series'])
            if st in ('걸림', '근접'):
                rows.append((0 if st == '걸림' else 1, t9, t['what'], t['value'],
                             t['cond'], st, why, t['as_of'] or '—'))
        for _tg, name, seen in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            if seen and now and str(now) != seen:
                rows.append((0, t9, name, now, '내가 읽은 판 %s' % seen, '걸림',
                             '그 뒤에 개정됐다 — 읽고 갱신한다', now))
    if not rows:
        return ('<p class="band-s">조건에 든 값도, 내가 읽은 뒤에 바뀐 법도 없습니다. '
                '이번 달은 볼 것이 없습니다.</p>')
    rows.sort(key=lambda r: (r[0], r[1]))
    hit = sum(1 for r in rows if r[0] == 0)
    h = ['<p class="band-s">걸린 것 <b>%d</b>, 문턱 가까이 온 것 <b>%d</b>.</p><div class="rows">'
         % (hit, len(rows) - hit)]
    prev = None
    for o, t9, what, val, cond, st, why, asof in rows:
        # 같은 줄이 잇달아 서면 이름을 되풀이하지 않는다 — 세 번 같은 이름이 서면
        # 눈이 그 열을 통째로 건너뛴다
        label = '' if t9 == prev else E(t9)
        prev = t9
        h.append('<div class="row"><span class="row-where">'
                 '<span class="dot %s"></span><a href="#%s">%s</a></span>'
                 '<span class="row-what">%s</span>'
                 '<span class="row-num">%s</span>'
                 '<span class="row-why">%s · %s · %s</span></div>'
                 % ('d-hit' if o == 0 else 'd-near', slug(t9), label, E(what),
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
        rows.append(['<a href="#%s">%s</a>' % (slug(title_of(w)), E(w['target'])),
                     '%.2f ~ %.2f' % (min(rs), max(rs)) if rs else '—',
                     '전세금의 %.1f배' % (100.0 / (sum(rs) / len(rs))) if rs else '—',
                     ('%s <span class="t-none">%s</span>' % (sd['value'], E(sd['area']))
                      if sd else '못 붙임'),
                     ('<b>%d</b>' % n) if n else '0', E(asof), '공표'])
    rows.sort(key=lambda r: r[1], reverse=True)
    return tbl('권역마다 지금 어떤가',
               ['권역', '전세가율(구별 범위)', '매매로 넘어가는 문턱', '수급동향',
                '걸림·근접', '언제 것', '성격'], rows)


def law_table(watches):
    by = {}
    for w in watches:
        if w['kind'] != 'policy':
            continue
        for _tg, name, seen in (w.get('laws') or []):
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            e = by.setdefault(name, {'now': m.get('value'), 'seen': set(), 'who': []})
            if seen:
                e['seen'].add(seen)
            e['who'].append(title_of(w))
    rows = []
    for name in sorted(by, key=lambda n: (by[n]['now'] or ''), reverse=True):
        e = by[name]
        st = ('—' if not e['now'] or not e['seen']
              else ('같다' if e['seen'] == set([e['now']]) else '걸림'))
        rows.append([E(name), E(e['now'] or '아직 안 받음'),
                     E(' · '.join(sorted(e['seen'])) or '—'), tag(st),
                     ' · '.join('<a href="#%s">%s</a>' % (slug(t), E(t))
                                for t in dict.fromkeys(e['who'])), '공표'])
    return tbl('법·고시가 지금 어느 판인가',
               ['법·고시', '지금 판', '내가 읽은 판', '같은가', '보는 줄', '성격'], rows)


def figures(w):
    """도해. series 가 든 metric 만 그린다 — 어댑터가 안 채운 자리에는 아무것도 안 선다."""
    TITLE = {'sale_idx': '매매가격지수', 'jeonse_idx': '전세가격지수',
             'jeonse_ratio': '전세가율 — 중위 매매가 대비 중위 전세가',
             'supply_demand': '매매수급동향 — 100이 균형',
             'median': '서울 중위가격 — 매매와 전세',
             'deal_count': '아파트 매매 거래량', 'rent_conv': '전월세 전환율'}
    GROUP = {'median_sale': ('median', '매매'), 'median_jeonse': ('median', '전세')}
    groups = {}
    for key, m in sorted((w.get('metrics') or {}).items()):
        if not m.get('series'):
            continue
        area = m.get('area') or ''
        base = key[:-(len(area) + 1)] if area and key.endswith('_' + area) else key
        gk, gn = GROUP.get(base, (base, area or base))
        groups.setdefault((gk, m.get('unit') or ''), []).append((gn, m))
    out = []
    for (base, unit), items in groups.items():
        note = ' · '.join(dict.fromkeys(m.get('src', '') for _n, m in items if m.get('src')))
        svg = wf.trend([(n, [tuple(x) for x in m['series']]) for n, m in items[:3]],
                       unit or '값', note=note)
        if svg:
            out.append('<figure>%s<figcaption>%s</figcaption></figure>'
                       % (svg, E(TITLE.get(base, base))))
    return ''.join(out)


def line_block(w):
    t9 = title_of(w)
    pick = (w['target'] if w['kind'] == 'realestate' else '제도')
    h = ['<section class="line" id="%s" data-pick="%s">' % (slug(t9), E(pick))]
    h.append('<h2>%s</h2><p class="line-why">%s</p>' % (E(t9), E(w['why'])))
    h.append('<p class="line-judge">%s</p>' % w['judged'])

    vals = [t for t in w['triggers'] if t['kind'] == wl.KIND_VALUE]
    if vals:
        rows = []
        for t in vals:
            st, why = wl.state_now(t['cond'], t['series'])
            unit = t.get('unit') or ''
            rows.append([E(t['what']),
                         ('—' if t['value'] is None else
                          '%s <span class="t-none">%s</span>' % (E(t['value']), E(unit))),
                         E(t['cond']), tag(st) + ' <span class="t-none">%s</span>' % E(why),
                         E(t['as_of'] or '—'), E(t['nature'] or '자리표시')])
        h.append(tbl('무엇이 일어나면 판단이 바뀌나 — 값으로 오는 것',
                     ['무엇을', '지금', '걸리는 조건', '상태', '언제 것', '성격'], rows))
    if w.get('laws'):
        rows = []
        for _tg, name, seen in w['laws']:
            m = (w.get('metrics') or {}).get(wl.law_key(name)) or {}
            now = m.get('value')
            st = '—' if not now or not seen else ('같다' if str(now) == seen else '걸림')
            rows.append([E(name), E(seen or '—'), E(now or '아직 안 받음'), tag(st)])
        h.append(tbl('내가 읽은 판과 지금 판',
                     ['법·고시', '내가 읽은 판', '지금 판', '같은가'], rows))
    if w['points']:
        h.append('<p class="lbl">왜 보나</p><ul class="pts">%s</ul>'
                 % ''.join('<li>%s</li>' % p for p in w['points']))
    fig = figures(w)
    if fig:
        h.append(fig)
    evt = [t for t in w['triggers'] if t['kind'] == wl.KIND_EVENT]
    if evt:
        h.append(tbl('값으로 안 오는 것 — 사람이 확인한다',
                     ['무엇을 확인하나', '언제 판단이 바뀌나'],
                     [[E(t['what']), E(t['cond'])] for t in evt]))
    if w['clash']:
        h.append('<p class="lbl">반대 근거</p><ul class="pts">%s</ul>'
                 % ''.join('<li>%s</li>' % c for c in w['clash']))
    h.append('</section>')
    return ''.join(h)


def check_ui(html, watches):
    """이 장의 규약. 아카이브 규약(check_ui)에서 나온 장이라 규약이 없어지면 안 된다."""
    assert 'is-fold' not in html and 'uc-caret' not in html, \
        '규약 위반: 접는 것을 두지 않는다 — 열면 다 보여야 한다'
    assert 'class="stile' not in html, \
        '규약 위반: 타일을 두지 않는다 — 고르는 계층은 탭 하나다'
    at_fired = html.find('지금 걸린 것')
    at_line = html.find('class="line"')
    assert 0 < at_fired < at_line, \
        '규약 위반: 「지금 걸린 것」이 줄 상세보다 먼저 서야 한다'
    assert '값이 언제 것인가' in html, '규약 위반: 때 자가 없다 — 값의 나이를 먼저 보인다'
    n = sum(1 for w in watches for t in w['triggers'] if t['kind'] == wl.KIND_VALUE
            and t['value'] is not None)
    assert html.count('<th>언제 것</th>') >= 1 or n == 0, \
        '규약 위반: 값을 내면서 「언제 것」 열이 없다'


def build():
    ws = wl.load_all()
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
    seen = []
    for w in sorted(ws, key=lambda x: (0 if x['kind'] == 'realestate' else 1,
                                       x['opened'], x['slug'])):
        k = w['target'] if w['kind'] == 'realestate' else '제도'
        if k not in seen:
            seen.append(k)

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
    h.append(time_ruler(ws))
    h.append('</header>')

    h.append('<div class="band"><p class="band-t">지금 걸린 것</p>%s</div>' % fired(ws))
    h.append('<div class="band"><p class="band-t">권역 견주기</p>'
             '<p class="band-s">전세가율은 한 수가 두 방향으로 읽힙니다. 올라가면 보증금이 '
             '집값에 가까워지고, 동시에 매매로 넘어가는 데 드는 자기 돈이 줄어듭니다.</p>'
             '%s</div>' % area_table(ws))
    h.append('<div class="band"><p class="band-t">제도</p>'
             '<p class="band-s">제도는 값으로 안 옵니다. 지금 어느 판인가만 기계가 알고, '
             '바뀐 내용은 사람이 조문을 열어 읽습니다.</p>%s</div>' % law_table(ws))

    h.append('<div class="band"><p class="band-t">줄</p>'
             '<div class="tabs"><button data-pick="all" aria-pressed="true">전체</button>%s</div>'
             '</div>' % ''.join('<button data-pick="%s" aria-pressed="false">%s</button>'
                                % (E(k), E(k)) for k in seen))
    for w in sorted(ws, key=lambda x: (0 if x['kind'] == 'realestate' else 1, x['slug'])):
        h.append(line_block(w))

    h.append('<footer>값은 한국부동산원 공표 통계, 제도는 국가법령정보센터에서 받습니다. '
             '마지막 확인 %s · 통계 기준 %s. 줄은 <code>insights/watch/</code>, 수치는 '
             '<code>insights/watch/_metrics/</code>, 이 화면은 '
             '<code>scratchpad/gen_watch_page.py</code>가 만듭니다.</footer>'
             % (E(checked), E(asof)))
    h.append('</div><script>%s</script></body></html>' % TAB_JS)
    html = ''.join(h)
    check_ui(html, ws)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('OK: 줄 %d개 -> %s' % (len(ws), OUT))
    return html


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    build()
