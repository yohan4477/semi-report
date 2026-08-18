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
  /* 제목 + 흐린 한 줄이 한 덩어리로 움직인다 */
  .rlttl{flex:1 1 auto; min-width:0; display:flex; flex-direction:column; gap:3px;}
  .rlt{font-size:.92rem; font-weight:700; line-height:1.4; color:var(--ink);}
  .rld{font-size:.78rem; line-height:1.55; color:var(--sub, var(--ink-3)); opacity:.85; font-weight:400;}
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
SCOPE = {'kr': '국내', 'intl': '해외'}


def _norm(v):
    return v if isinstance(v, dict) else {'all': v}


def _scoped(counts, scope):
    """counts가 {'*':{날짜:n}, 'kr':{...}} 꼴이면 해당 범위만, 아니면 통째로 쓴다"""
    if counts and '*' in counts:
        return counts.get(scope or '*', {})
    return counts


def count_range(counts, a, b, scope=None):
    tot = {}
    for d, v in _scoped(counts, scope).items():
        if a <= d <= b:
            for k, n in _norm(v).items():
                tot[k] = tot.get(k, 0) + n
    return tot


def render_report(r, counts, unit='건', open_=False, show_desc=True):
    c = count_range(counts, r['from'], r['to'], r.get('scope'))
    n = c.get('all', 0)
    meta = '%s~%s · %d%s' % (r['from'][5:], r['to'][5:], n, unit)
    if c.get('yt'):
        meta += ' (LinkedIn %d · 영상 %d)' % (c.get('li', 0), c['yt'])
    # 항목에 sec(섹션 id)을 달면 그 대시보드에서 섹션을 골랐을 때 해당 항목만 남는다
    items = ''.join(
        '<li%s><span class="rlh">%s</span><span class="rlb">%s</span></li>'
        % (' data-sec="%s"' % it['sec'] if it.get('sec') else '', it['h'], it['b'])
        for it in r['items'])
    label = KIND.get(r['kind'], r['kind'])
    if r.get('scope'):
        label += ' · ' + SCOPE.get(r['scope'], r['scope'])
    # 접힌 상태에서 무슨 내용인지 한 줄로 알려준다. 없으면 제목만 나온다.
    # show_desc=False면 이 줄을 통째로 뺀다 — 항목을 처음부터 펼쳐 두는 페이지에서는
    # 같은 이야기를 요약과 본문으로 두 번 읽게 된다(2026-08-18 SemiAnalysis 쪽 요청).
    desc = '<span class="rld">%s</span>' % r['desc'] if (show_desc and r.get('desc')) else ''
    # data-scope는 대시보드의 국내·해외 탭이 골라 보여주는 표시다(범위 없는 리포트는 늘 보인다)
    return ('<details class="rlrep"%s%s><summary class="rlhd"><span class="rlk">%s</span>'
            '<span class="rlttl"><span class="rlt">%s</span>%s</span>'
            '<span class="rlmeta">%s</span></summary>'
            '<ol class="rll">%s</ol></details>') % (
        ' open' if open_ else '',
        ' data-scope="%s"' % r['scope'] if r.get('scope') else '',
        label, r['title'], desc, meta, items)


def build(notes, counts, unit='건', open_current=False, show_desc=True):
    """최신 회차는 위에, 이전 회차는 <details>로 접어 누적한다.

    open_current=True면 최신 회차를 열린 상태로 낸다 — 클릭하지 않아도 항목이 보인다.
    지난 회차는 그대로 접어 둔다(다 펼치면 페이지가 리포트로 뒤덮인다).
    """
    reps = [r for r in notes.get('reports', [])
            if count_range(counts, r['from'], r['to'], r.get('scope')).get('all', 0)]
    if not reps:
        return ''
    reps.sort(key=lambda r: (r['asof'], r['kind']), reverse=True)
    newest = reps[0]['asof']
    cur = sorted([r for r in reps if r['asof'] == newest],
                 key=lambda r: (0 if r['kind'] == 'week' else 1,
                                {'kr': 0, 'intl': 1}.get(r.get('scope'), 0)))
    old = [r for r in reps if r['asof'] != newest]
    html = '<div class="rollup">' + ''.join(
        render_report(r, counts, unit, open_=open_current, show_desc=show_desc) for r in cur)
    if old:
        html += ('<details class="rlold"><summary>지난 리포트 %d편 ▾</summary>' % len(old)) \
                + ''.join(render_report(r, counts, unit, show_desc=show_desc)
                          for r in old) + '</details>'
    return html + '</div>'
