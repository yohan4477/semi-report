# -*- coding: utf-8 -*-
"""신호 흐름 지도 — SemiAnalysis 대시보드에 붙이는 네 겹 지도.

    사슬 단계 → 시기(월) → 신호 → 그 신호가 무엇을 어디로 밀었나

회계사 대시보드의 드라이버 지도와 같은 구조다(`docs/회계사 대시보드 — 만드는 규칙.md` §2).
거기가 회사·연도·방법·값이면 여기는 단계·월·신호·영향이다.

값은 새로 만들지 않는다. 이벤트와 영향 트리는 `대시보드/소스 타임라인.html`이 갖고
있고(EVENTS·IMPACTS·GROUPS), 이 스크립트는 그것을 읽어 정적 HTML로 편다. 그래서
타임라인에 이벤트를 더하면 여기를 다시 돌리는 것으로 지도가 따라온다.

    PYTHONIOENCODING=utf-8 python scripts/gen_sigmap.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '대시보드', '소스 타임라인.html')
DST = os.path.join(ROOT, '대시보드', 'SemiAnalysis 대시보드.html')
TL_URL = ('https://yohan4477.github.io/semi-report/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/'
          '%EC%86%8C%EC%8A%A4%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8.html')

# 사슬 순서와 짧은 이름은 타임라인 쪽 CHAIN·CHAIN_SHORT를 그대로 따른다
CHAIN = ['파운드리·장비·소재', '메모리', '칩·컴퓨트', '네트워킹·서버·부품', '클라우드·DC', 'AI 랩·모델']
SHORT = {'파운드리·장비·소재': '제조', '메모리': '메모리', '칩·컴퓨트': '가속기',
         '네트워킹·서버·부품': '서버', '클라우드·DC': '인프라', 'AI 랩·모델': '수요',
         '전력': '전력', '기타': '기타'}
GLOSS = {'파운드리·장비·소재': '웨이퍼에 새기는 쪽', '메모리': 'HBM과 D램',
         '칩·컴퓨트': '가속기와 그 소프트웨어', '네트워킹·서버·부품': '칩 밖에서 잇는 부품',
         '클라우드·DC': '짓고 굴리는 쪽', 'AI 랩·모델': '토큰을 파는 쪽',
         '전력': '꽂을 자리와 그 값', '기타': '사슬에 못 붙인 신호'}
ETC = '기타'
STEPS = CHAIN + ['전력', ETC]
SYM = {'+': '▲', '-': '▼', '0': '—'}
CLS = {'+': 'smup', '-': 'smdn', '0': 'smfl'}
MONTHS = 6          # 지도에 펴는 시기 — 최근 여섯 달


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def read_source():
    h = io.open(SRC, encoding='utf-8').read()
    ev = json.loads(re.search(r'const EVENTS = (\[.*?\]);', h, re.S).group(1))
    im = json.loads(re.search(r'const IMPACTS = (\{.*?\});', h, re.S).group(1))
    # GROUPS는 여러 줄짜리 JS 리터럴이라 홑따옴표와 끝쉼표를 걷어내야 json이 읽는다
    raw = re.search(r'const GROUPS=(\[.*?\n\]);', h, re.S).group(1).replace("'", '"')
    groups = json.loads(re.sub(r',(\s*[\]\}])', r'\1', raw))
    of = {}
    for g, names in groups:
        for n in names:
            of[n] = g
    return ev, im, of


def flat(branches):
    out = []

    def walk(bs):
        for b in bs or []:
            out.append(b)
            walk(b.get('k'))
    walk(branches)
    return out


def step_of(e, im, group_of):
    """그 신호가 선 단계 = 영향 대상이 가장 무겁게 몰린 밸류체인 그룹.

    별도 라벨을 손으로 달지 않는다 — 영향 트리가 이미 「누구에게」를 갖고 있어서,
    라벨을 따로 두면 트리와 어긋난 자리가 생긴다."""
    score = {}
    for b in flat(im.get(str(e['idx']))):
        g = group_of.get(b['t'])
        if not g:
            continue
        score[g] = score.get(g, 0) + (3 if b['m'] >= 3 else 2 if b['m'] >= 2 else 1)
    if not score:
        return ETC
    return sorted(score.items(), key=lambda kv: (-kv[1], STEPS.index(kv[0])))[0][0]


def node_html(b):
    kids = ''.join(node_html(c) for c in b.get('k') or [])
    return ('<div class="smnode %s"><span class="smt">%s %s</span>'
            '<span class="smw">%s</span>%s</div>%s'
            % (CLS[b['d']], SYM[b['d']], esc(b['t']), esc(b['w']),
               '<span class="smmj">주요</span>' if b['m'] >= 3 else '',
               '<div class="smkids">%s</div>' % kids if kids else ''))


def row_html(e, im):
    bs = im.get(str(e['idx'])) or []
    gly = ''.join('<span class="%s">%s</span>' % (CLS[b['d']], SYM[b['d']]) for b in bs[:4])
    tags = ''.join('<span class="smtag %s">%s</span>' % (CLS[b['d']], esc(b['t']))
                   for b in flat(bs)[:3])
    return ('<details class="smev"><summary><span class="smd">%s</span>'
            '<span class="smlbl">%s</span><span class="smgly">%s</span></summary>'
            '<div class="smtags">%s</div><div class="smtree">%s</div>'
            '<a class="smorig" href="%s" target="_blank" rel="noopener">원문 ↗</a>'
            '</details>'
            % (e['date'][5:10].replace('-', '.'), esc(e['label']), gly, tags,
               ''.join(node_html(b) for b in bs), esc(e['url'])))


def build():
    ev, im, group_of = read_source()
    live = [e for e in ev if (im.get(str(e['idx'])) or [])]
    months = sorted({e['date'][:7] for e in live}, reverse=True)[:MONTHS]
    bucket = {}
    for e in live:
        bucket.setdefault(step_of(e, im, group_of), []).append(e)
    for a in bucket.values():
        a.sort(key=lambda x: x['date'], reverse=True)

    newest = max(e['date'] for e in live)[:10]
    tiles, panels = [], []
    for i, s in enumerate(STEPS):
        lst = bucket.get(s) or []
        if not lst:
            continue
        net = sum(1 if b['d'] == '+' else -1 if b['d'] == '-' else 0
                  for e in lst[:20] for b in flat(im.get(str(e['idx']))))
        d = '+' if net > 0 else '-' if net < 0 else '0'
        recent = sum(1 for e in lst if e['date'][:7] == months[0])
        tiles.append(
            '<button type="button" class="smtile" data-step="%s"><span class="smtn">'
            '<span class="smnum">%02d</span>%s</span><span class="smg">%s</span>'
            '<span class="smm"><span class="smc">%d건</span>%s<span class="%s">%s %d</span>'
            '</span></button>'
            % (esc(s), i + 1, esc(SHORT[s]), esc(GLOSS[s]), len(lst),
               '<span class="smr">이번 달 %d</span>' % recent if recent else '',
               CLS[d], SYM[d], abs(net)))

        strip = ''.join(
            ('<span class="smarr">→</span>' if j and c in CHAIN else '')
            + '<button type="button" class="smnodebtn%s" data-step="%s">%s</button>'
            % (' on' if c == s else '', esc(c), esc(SHORT[c]))
            for j, c in enumerate(STEPS) if bucket.get(c))
        tabs, boxes = [], []
        for m in months:
            rows = [e for e in lst if e['date'][:7] == m]
            on = ' on' if m == months[0] else ''
            tabs.append('<button type="button" class="smtab%s" data-m="%s">%s</button>'
                        % (on, m, m[2:].replace('-', '.')))
            body = ''.join(row_html(e, im) for e in rows) or \
                '<p class="smempty">이 달에는 이 단계로 잡힌 신호가 없습니다.</p>'
            boxes.append('<div class="smmonth%s" data-m="%s"><p class="smcnt">%d건 · 신호를 '
                         '누르면 무엇을 어디로 밀었는지 펼쳐집니다</p>%s</div>'
                         % (on, m, len(rows), body))
        panels.append(
            '<div class="smpanel" data-step="%s"><div class="smhead"><span class="smttl">%s '
            '— %s</span><button type="button" class="smback">← 단계 고르기</button></div>'
            '<div class="smstrip">%s</div><div class="smtabs">%s</div>%s</div>'
            % (esc(s), esc(SHORT[s]), esc(GLOSS[s]), strip, ''.join(tabs), ''.join(boxes)))

    return SECTION % {
        'stamp': newest, 'n': len(live), 'url': TL_URL,
        'tiles': ''.join(tiles), 'panels': ''.join(panels),
    }


SECTION = '''<section id="sigmap-section" data-c="all compute memory power model robot">
    <div class="sec-head">
      <h2>신호 흐름 지도 — 사슬 단계별로 무엇이 어디로 밀렸나</h2>
      <span style="margin-left:auto; display:flex; gap:14px;">
      <a class="more" href="%(url)s" target="_blank" rel="noopener">영향 타임라인 ↗</a>
      </span>
    </div>
    <p class="note" style="margin-top:2px;">신호 %(n)d건을 영향 대상이 몰린 밸류체인
      단계로 갈랐습니다(%(stamp)s 기준). 단계를 고르면 그 단계의 시기별 신호가 서고,
      신호를 누르면 영향 트리가 펼쳐집니다. 방향은 매출·수요·경쟁지위 기준이며 가격
      전망이 아닙니다.</p>
    <div class="sigmap">
      <div class="smtiles">%(tiles)s</div>
      <div class="smstage">%(panels)s</div>
    </div>
  </section>'''


CSS = '''
  /* sigmap:start — 신호 흐름 지도(scripts/gen_sigmap.py가 만든다) */
  .sigmap{margin-top:12px}
  .smtiles{display:grid; grid-template-columns:repeat(auto-fill,minmax(158px,1fr)); gap:8px;}
  .smtile{display:block; text-align:left; font-family:inherit; cursor:pointer;
    border:1px solid var(--line); border-radius:12px; background:var(--card); padding:12px 13px;}
  .smtile:hover{border-color:var(--accent);}
  .smtn{display:flex; align-items:baseline; gap:7px; font-size:.95rem; font-weight:800; color:var(--ink);}
  .smnum{font-size:.7rem; font-weight:800; color:var(--sub); letter-spacing:.04em;}
  .smg{display:block; margin-top:3px; font-size:.74rem; color:var(--sub); line-height:1.5;}
  .smm{display:flex; align-items:center; gap:6px; margin-top:9px; font-size:.72rem; font-weight:700;}
  .smc{color:var(--sub);} .smr{color:var(--accent);}
  .smstage{display:none;} .sigmap.open .smstage{display:block;} .sigmap.open .smtiles{display:none;}
  .smpanel{display:none;} .smpanel.on{display:block;}
  .smhead{display:flex; align-items:center; gap:10px; margin-bottom:10px;}
  .smttl{font-size:.95rem; font-weight:800; color:var(--ink);}
  .smback{margin-left:auto; font-family:inherit; font-size:.75rem; font-weight:700; cursor:pointer;
    color:var(--sub); background:var(--card); border:1px solid var(--line); border-radius:999px; padding:5px 11px;}
  .smstrip{display:flex; align-items:center; flex-wrap:wrap; gap:5px; margin-bottom:10px;}
  .smnodebtn{font-family:inherit; font-size:.74rem; font-weight:750; cursor:pointer; color:var(--sub);
    background:var(--card); border:1px solid var(--line); border-radius:999px; padding:4px 10px;}
  .smnodebtn.on{background:var(--ink); border-color:var(--ink); color:#fff;}
  .smarr{color:var(--line); font-size:.7rem;}
  .smtabs{display:flex; flex-wrap:wrap; gap:6px; margin-bottom:6px;}
  .smtab{font-family:inherit; font-size:.74rem; font-weight:750; cursor:pointer; color:var(--sub);
    background:var(--card); border:1px solid var(--line); border-radius:999px; padding:4px 10px;}
  .smtab.on{border-color:var(--accent); color:var(--accent); background:var(--accent-soft);}
  .smmonth{display:none;} .smmonth.on{display:block;}
  .smcnt{margin:6px 0 2px; font-size:.72rem; color:var(--sub);}
  .smempty{margin:10px 0; font-size:.8rem; color:var(--sub);}
  .smev{border-top:1px solid var(--line); padding:10px 0;}
  .smev>summary{list-style:none; cursor:pointer; display:flex; align-items:flex-start; gap:8px;}
  .smev>summary::-webkit-details-marker{display:none;}
  .smd{flex:none; font-size:.72rem; font-weight:800; color:var(--sub); padding-top:2px;
    font-variant-numeric:tabular-nums;}
  .smlbl{flex:1; font-size:.83rem; line-height:1.55; font-weight:600; color:var(--ink);}
  .smgly{flex:none; font-size:.7rem; letter-spacing:1px;}
  .smtags{display:flex; flex-wrap:wrap; gap:5px; margin:7px 0 0 34px;}
  .smtag{font-size:.7rem; font-weight:750; padding:2px 7px; border-radius:999px; border:1px solid var(--line);}
  .smtree{margin:9px 0 0 34px;}
  .smnode{font-size:.78rem; line-height:1.6; padding:2px 0;}
  .smnode .smt{font-weight:800;}
  .smnode .smw{color:var(--sub); margin-left:6px;}
  .smmj{margin-left:6px; font-size:.65rem; font-weight:800; color:var(--warn);
    background:var(--warn-bg); border-radius:999px; padding:1px 6px;}
  .smkids{margin-left:14px; padding-left:10px; border-left:1px solid var(--line);}
  .smorig{display:inline-block; margin:8px 0 0 34px; font-size:.72rem; font-weight:700; color:var(--accent);}
  .smup{color:var(--risk);} .smdn{color:var(--accent);} .smfl{color:var(--sub);}
  /* sigmap:end */
'''

JS = '''
<script>
/* 신호 흐름 지도 — 타일에서 단계를 고르고, 그 안에서 시기를 고른다 */
(function(){
  var wrap=document.querySelector('.sigmap'); if(!wrap) return;
  function openStep(s){
    wrap.classList.add('open');
    wrap.querySelectorAll('.smpanel').forEach(function(p){p.classList.toggle('on',p.dataset.step===s);});
    wrap.scrollIntoView({block:'start'});
  }
  wrap.querySelectorAll('.smtile,.smnodebtn').forEach(function(b){
    b.onclick=function(){openStep(b.dataset.step);};});
  wrap.querySelectorAll('.smback').forEach(function(b){
    b.onclick=function(){wrap.classList.remove('open');
      wrap.querySelectorAll('.smpanel').forEach(function(p){p.classList.remove('on');});
      wrap.scrollIntoView({block:'start'});};});
  wrap.querySelectorAll('.smtab').forEach(function(t){
    t.onclick=function(){var p=t.closest('.smpanel');
      p.querySelectorAll('.smtab').forEach(function(x){x.classList.toggle('on',x===t);});
      p.querySelectorAll('.smmonth').forEach(function(m){m.classList.toggle('on',m.dataset.m===t.dataset.m);});};});
})();
</script>
'''


def splice():
    sec = build()
    h = io.open(DST, encoding='utf-8').read()
    # 스크립트는 섹션 바로 뒤에 둔다 — 이 페이지에는 </body>가 없어서
    # 문서 끝에 붙일 자리가 따로 없다(2026-08-21에 여기서 한 번 걸렸다)
    block = '<!--SIGMAP:START-->' + sec + JS + '<!--SIGMAP:END-->'
    if '<!--SIGMAP:START-->' in h:
        h = re.sub(r'<!--SIGMAP:START-->.*?<!--SIGMAP:END-->', lambda _m: block, h, flags=re.S)
    else:
        anchor = '<section id="social-section"'
        assert anchor in h, '① 소셜 신호 섹션을 못 찾았다'
        h = h.replace(anchor, block + '\n\n  ' + anchor, 1)
    if 'sigmap:start' not in h:
        h = h.replace('</style>', CSS + '</style>', 1)
    else:
        h = re.sub(r'\n  /\* sigmap:start.*?/\* sigmap:end \*/\n', lambda _m: CSS, h, flags=re.S)
    io.open(DST, 'w', encoding='utf-8').write(h)
    o, c = h.count('<div'), h.count('</div>')
    print('sigmap: 타일 %d · div %d %d'
          % (h.count('class="smtile"'), o, c))
    if o != c:
        print('WARN: div 짝이 안 맞는다', file=sys.stderr)


if __name__ == '__main__':
    splice()
