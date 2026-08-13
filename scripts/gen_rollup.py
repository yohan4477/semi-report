# -*- coding: utf-8 -*-
"""주간·월간 롤업 리포트를 소셜 히스토리와 SemiAnalysis 대시보드 상단에 스플라이스한다.

- 산문은 data/rollup_notes.json (사람이 씀, 판단이 들어가므로 자동 생성 금지)
- 건수·기간은 소셜 신호 히스토리의 day 그룹에서 계산
- 두 페이지 모두 <!--ROLLUP:START--> ~ <!--ROLLUP:END--> 사이만 갈아끼운다
- 클래스는 rl* 접두어 — 대시보드의 기존 .repl 등과 충돌 방지

사용: python scripts/gen_rollup.py
"""
import io, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
DASH = os.path.join(ROOT, '대시보드', 'SemiAnalysis 대시보드.html')
NOTES = os.path.join(ROOT, 'data', 'rollup_notes.json')

CSS = """
  /* rollup:start */
  .rollup{margin:0 0 18px;}
  .rlrep{background:var(--card); border:1px solid var(--line); border-radius:10px; padding:10px 14px; margin-bottom:8px;}
  .rlrep[open]{padding-bottom:14px;}
  .rlhd{display:flex; align-items:baseline; gap:8px; flex-wrap:wrap; cursor:pointer; list-style:none;}
  .rlhd::-webkit-details-marker{display:none;}
  .rlhd::after{content:"▾"; flex:none; color:var(--sub); font-size:.7rem; margin-left:auto;}
  .rlrep[open] .rlhd::after{content:"▴";}
  .rlhd:focus-visible{outline:2px solid var(--accent); outline-offset:3px; border-radius:6px;}
  .rlk{flex:none; font-size:.68rem; font-weight:800; letter-spacing:.04em; color:var(--accent);
    background:var(--accent-soft); border-radius:999px; padding:2px 9px;}
  .rlt{font-size:.92rem; font-weight:700; line-height:1.4; flex:1 1 auto; min-width:0; color:var(--ink);}
  .rlmeta{color:var(--sub); font-size:.72rem; font-variant-numeric:tabular-nums; white-space:nowrap;}
  .rll{list-style:none; margin:10px 0 0; padding:0;}
  .rll li{border-top:1px solid var(--line); padding:8px 0 0; margin-top:8px;}
  .rll li:first-child{border-top:none; padding-top:0; margin-top:0;}
  .rll .rlh{display:block; font-size:.86rem; font-weight:700; margin-bottom:3px; color:var(--ink);}
  .rll .rlb{display:block; font-size:.82rem; color:var(--sub); line-height:1.6;}
  .rll .rlb b{color:var(--ink);}
  .rlold{margin:0 0 14px;}
  .rlold > summary{cursor:pointer; color:var(--sub); font-size:.78rem; font-weight:700; padding:6px 0;}
  .rlold > summary:focus-visible{outline:2px solid var(--accent); outline-offset:2px;}
  /* rollup:end */
"""

KIND = {'week': '주간 리포트', 'month': '월간 리포트'}


def day_counts(html):
    """{날짜: {'li': n, 'yt': n, 'all': n}} — 히스토리 페이지의 day 그룹 기준"""
    out = {}
    for d, body in re.findall(r'<div class="day"><h3>(\d{4}-\d{2}-\d{2})</h3>(.*?)</div></div>', html, re.S):
        rows = re.findall(r'<a class="rowmain" href="([^"]+)"', body)
        li = sum(1 for u in rows if 'linkedin.com' in u)
        out[d] = {'li': li, 'yt': len(rows) - li, 'all': len(rows)}
    return out


def count_range(counts, a, b):
    tot = {'li': 0, 'yt': 0, 'all': 0}
    for d, c in counts.items():
        if a <= d <= b:
            for k in tot:
                tot[k] += c[k]
    return tot


def render_report(r, counts):
    c = count_range(counts, r['from'], r['to'])
    meta = '%s~%s · 신호 %d건' % (r['from'][5:], r['to'][5:], c['all'])
    if c['yt']:
        meta += ' (LinkedIn %d · 영상 %d)' % (c['li'], c['yt'])
    items = ''.join(
        '<li><span class="rlh">%s</span><span class="rlb">%s</span></li>' % (it['h'], it['b'])
        for it in r['items'])
    return ('<details class="rlrep"><summary class="rlhd"><span class="rlk">%s</span>'
            '<span class="rlt">%s</span><span class="rlmeta">%s</span></summary>'
            '<ol class="rll">%s</ol></details>') % (KIND.get(r['kind'], r['kind']), r['title'], meta, items)


def build(notes, counts):
    reps = sorted(notes['reports'], key=lambda r: (r['asof'], r['kind']), reverse=True)
    if not reps:
        return ''
    newest = reps[0]['asof']
    cur = [r for r in reps if r['asof'] == newest]
    old = [r for r in reps if r['asof'] != newest]
    cur.sort(key=lambda r: 0 if r['kind'] == 'week' else 1)
    html = '<div class="rollup">' + ''.join(render_report(r, counts) for r in cur)
    if old:
        html += ('<details class="rlold"><summary>지난 리포트 %d편 ▾</summary>'
                 % len(old)) + ''.join(render_report(r, counts) for r in old) + '</details>'
    return html + '</div>'


def splice(path, anchor, block, indent=''):
    html = io.open(path, encoding='utf-8').read()
    html = re.sub(r'\n?  /\* rollup(:start)? \*/.*?(/\* rollup:end \*/\n)?(?=</style>)', '',
                  html, flags=re.S)
    html = html.replace('</style>', CSS + '</style>', 1)
    if '<!--ROLLUP:START-->' not in html:
        assert anchor in html, 'anchor not found in %s' % path
        html = html.replace(anchor, indent + '<!--ROLLUP:START--><!--ROLLUP:END-->\n' + anchor, 1)
    html = re.sub(r'<!--ROLLUP:START-->.*?<!--ROLLUP:END-->',
                  lambda m: '<!--ROLLUP:START-->' + block + '<!--ROLLUP:END-->', html, flags=re.S)
    io.open(path, 'w', encoding='utf-8').write(html)
    print('%-28s div %d %d' % (os.path.basename(path), html.count('<div'), html.count('</div>')))


def main():
    notes = json.load(io.open(NOTES, encoding='utf-8'))
    counts = day_counts(io.open(HIST, encoding='utf-8').read())
    block = build(notes, counts)
    splice(HIST, '  <div class="tabbar">', block, '  ')
    splice(DASH, '  <section id="social-section"', block, '  ')
    print('reports: %d' % len(notes['reports']))


if __name__ == '__main__':
    main()
