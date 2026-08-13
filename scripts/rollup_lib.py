# -*- coding: utf-8 -*-
"""주간·월간 롤업 리포트 공용 렌더러.

- 기간 기준은 **매체 업로드일**(링크드인 게시 시각, 유튜브·네이버 발행일)이다.
  우리가 처리·반영한 날이 아니다.
- 산문은 data/rollup_notes*.json에 사람이 쓴다(판단이라 자동 생성 금지).
- 건수는 각 페이지의 원본 항목에서 세어 넘긴다: counts = {'YYYY-MM-DD': 개수}
  (히스토리처럼 소스 구분이 필요하면 {'all':n,'li':n,'yt':n} 형태도 받는다)
- 창에 항목이 0개인 리포트는 렌더하지 않는다(업로드가 없던 주는 카드도 없음).

클래스는 rl* 접두어 — 대시보드들이 이미 쓰는 .rep* / .repl 과 충돌 방지.
"""

CSS = """
  /* rollup:start */
  .rollup{margin:0 0 18px;}
  .rlrep{background:var(--card, var(--surface)); border:1px solid var(--line); border-radius:10px; padding:10px 14px; margin-bottom:8px;}
  .rlrep[open]{padding-bottom:14px;}
  .rlhd{display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; cursor:pointer; list-style:none;}
  .rlhd::-webkit-details-marker{display:none;}
  .rlhd::after{content:"▾"; flex:none; color:var(--sub, var(--ink-3)); font-size:.7rem; margin-left:auto;}
  .rlrep[open] .rlhd::after{content:"▴";}
  .rlhd:focus-visible{outline:2px solid var(--accent); outline-offset:3px; border-radius:6px;}
  .rlk{flex:none; font-size:.68rem; font-weight:800; letter-spacing:.04em; color:var(--accent);
    background:var(--accent-soft); border-radius:999px; padding:2px 9px;}
  .rlt{font-size:.92rem; font-weight:700; line-height:1.4; flex:1 1 auto; min-width:0; color:var(--ink);}
  .rlmeta{color:var(--sub, var(--ink-3)); font-size:.72rem; font-variant-numeric:tabular-nums; white-space:nowrap;}
  .rll{list-style:none; margin:10px 0 0; padding:0;}
  .rll li{border-top:1px solid var(--line); padding:8px 0 0; margin-top:8px;}
  .rll li:first-child{border-top:none; padding-top:0; margin-top:0;}
  .rll .rlh{display:block; font-size:.86rem; font-weight:700; margin-bottom:3px; color:var(--ink);}
  .rll .rlb{display:block; font-size:.82rem; color:var(--sub, var(--ink-3)); line-height:1.6;}
  .rll .rlb b{color:var(--ink);}
  .rlold{margin:0 0 14px;}
  .rlold > summary{cursor:pointer; color:var(--sub, var(--ink-3)); font-size:.78rem; font-weight:700; padding:6px 0;}
  .rlold > summary:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}
  /* rollup:end */
"""

KIND = {'week': '주간 리포트', 'month': '월간 리포트'}


def _norm(v):
    return v if isinstance(v, dict) else {'all': v}


def count_range(counts, a, b):
    tot = {}
    for d, v in counts.items():
        if a <= d <= b:
            for k, n in _norm(v).items():
                tot[k] = tot.get(k, 0) + n
    return tot


def render_report(r, counts, unit='건'):
    c = count_range(counts, r['from'], r['to'])
    n = c.get('all', 0)
    meta = '%s~%s · %d%s' % (r['from'][5:], r['to'][5:], n, unit)
    if c.get('yt'):
        meta += ' (LinkedIn %d · 영상 %d)' % (c.get('li', 0), c['yt'])
    items = ''.join(
        '<li><span class="rlh">%s</span><span class="rlb">%s</span></li>' % (it['h'], it['b'])
        for it in r['items'])
    return ('<details class="rlrep"><summary class="rlhd"><span class="rlk">%s</span>'
            '<span class="rlt">%s</span><span class="rlmeta">%s</span></summary>'
            '<ol class="rll">%s</ol></details>') % (KIND.get(r['kind'], r['kind']), r['title'], meta, items)


def build(notes, counts, unit='건'):
    """최신 회차는 펼쳐 보이고, 이전 회차는 <details>로 접어 누적한다."""
    reps = [r for r in notes.get('reports', []) if count_range(counts, r['from'], r['to']).get('all', 0)]
    if not reps:
        return ''
    reps.sort(key=lambda r: (r['asof'], r['kind']), reverse=True)
    newest = reps[0]['asof']
    cur = sorted([r for r in reps if r['asof'] == newest], key=lambda r: 0 if r['kind'] == 'week' else 1)
    old = [r for r in reps if r['asof'] != newest]
    html = '<div class="rollup">' + ''.join(render_report(r, counts, unit) for r in cur)
    if old:
        html += ('<details class="rlold"><summary>지난 리포트 %d편 ▾</summary>' % len(old)) \
                + ''.join(render_report(r, counts, unit) for r in old) + '</details>'
    return html + '</div>'
