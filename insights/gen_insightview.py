# 🧩 통합 인사이트 — 노트를 통째로 읽고 교차에서 나온 판단만 싣는다.
# 카드를 모아 두는 페이지가 아니라, 문서 여러 편을 가로질러야 보이는 것만 남긴다.
# 문장 옆 줄번호를 누르면 근거가 된 원문 그 줄로 간다.
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths, style
import notes_lib as nl

OUT = os.path.join(paths.ROOT, '대시보드', '통합 인사이트.html')


# 종류 안에서도 주제로 묶는다 — 카드 열 장이 한 줄로 늘어서면 어디를 보는지 놓친다
SECTIONS = (('chip', '반도체 · 메모리 · 가속기'),
            ('power', '전력 · 데이터센터'),
            ('model', '모델 · 학습'),
            ('biz', '사업 · 비용 · 재무'))


# (디렉터리, 배지 이름, 탭 id) — 탭은 이 순서로 선다
KINDS = ((paths.BRIEFS, '브리핑', 'brief'),
         (paths.SYNTH, '교차 인사이트', 'cross'),
         (paths.THESES, '종합 판단', 'thesis'))


def anchor(head):
    """NEW 배지는 카드 id 기준이라(scripts/update_card_ledger.py) h2에 id가 있어야 한다"""
    key = re.sub(r'[^0-9A-Za-z가-힣]+', '-', head).strip('-')
    return 'card-' + key


def srcbox(src):
    """무엇을 읽고 썼는지 카드 안에서 바로 보이게 — 인용은 줄 단위라 문서 목록이 따로 필요하다"""
    if not src:
        return ''
    import urllib.parse
    rows = []
    for d in src:
        f = d['file'].replace(os.sep, '/')
        rows.append('<li><a href="%s%s" target="_blank" rel="noopener">%s</a></li>'
                    % (nl.BLOB, urllib.parse.quote(f), nl.esc(d['base'])))
    return ('<details class="srcs"><summary>참고한 문서 %d편</summary><ul>%s</ul></details>'
            % (len(src), ''.join(rows)))


def one(meta, body, tab, kind):
    src = nl.sources_of(meta)
    head = meta.get('headline') or ''
    return ('<details class="ins" data-kind="%s"><summary><span class="cid">%s</span>'
            '<span class="asof">as_of %s</span><h2 id="%s">%s</h2>'
            '<p class="sub">%s</p></summary><div class="body">%s</div>%s</details>'
            % (tab, nl.esc(kind), nl.esc(meta.get('as_of', '')),
               anchor(head), nl.esc(head), nl.esc(meta.get('subhead', '')),
               nl.md_body(body, src, 'h4', 'bsec'), srcbox(src)))


def cards():
    out, per, bysec = [], {}, {}
    for d, kind, tab in KINDS:
        got = {}
        for p in sorted(glob.glob(os.path.join(d, '*.md')), reverse=True):
            meta, body = nl.parse_front(io.open(p, encoding='utf-8').read())
            meta.setdefault('headline', os.path.basename(p)[:-3])
            sid = meta.get('section', 'etc')
            got.setdefault(sid, []).append(one(meta, body, tab, kind))
            per[tab] = per.get(tab, 0) + 1
            bysec[sid] = bysec.get(sid, 0) + 1
        if not got:
            continue
        blocks, num = [], 0
        for sid, title in SECTIONS + (('etc', '그 밖'),):
            if not got.get(sid):
                continue
            num += 1
            blocks.append('<section class="isec" data-kind="%s" data-sec="%s"><div class="ihead">'
                          '<span class="inum">%02d</span><h3>%s</h3>'
                          '<span class="icnt">%d</span></div>%s</section>'
                          % (tab, sid, num, nl.esc(title), len(got[sid]), ''.join(got[sid])))
        out.append('<div class="kgroup" data-kind="%s"><h2 class="ktitle">%s</h2>%s</div>'
                   % (tab, nl.esc(kind), ''.join(blocks)))
    return ''.join(out), per, bysec


GUIDE = ('<div class="guide">'
         '<div class="g-brief"><b>브리핑 %d</b>'
         '<p>한 주제의 지금 상태를 모아 둔 것. 판단하지 않고 나온 숫자와 갈리는 지점만 정리한다.</p></div>'
         '<div class="g-cross"><b>교차 인사이트 %d</b>'
         '<p>문서 여러 편을 가로질러야 보이는 것. 같은 단위가 다른 것을 재거나, 서로 어긋나거나, '
         '아무도 안 다룬 자리를 짚는다.</p></div></div>')


def guide(per):
    return GUIDE % (per.get('brief', 0), per.get('cross', 0))


def sectabs(bysec):
    """주제로도 골라 볼 수 있어야 한다 — 종류 탭과 겹쳐 걸린다"""
    total = sum(bysec.values())
    out = ['<button data-sec="all" aria-pressed="true">전체 주제 '
           '<span class="tn">%d</span></button>' % total]
    for sid, title in SECTIONS + (('etc', '그 밖'),):
        if bysec.get(sid):
            out.append('<button data-sec="%s" aria-pressed="false">%s <span class="tn">%d</span></button>'
                       % (sid, nl.esc(title), bysec[sid]))
    return '<div class="itabs sectabs">%s</div>' % ''.join(out)


def tabs(per):
    """교차 인사이트와 정리본은 성격이 달라 섞어 두면 무엇을 읽는지 헷갈린다"""
    total = sum(per.values())
    out = ['<button data-tab="all" aria-pressed="true">전체 <span class="tn">%d</span></button>' % total]
    for _d, kind, tab in KINDS:
        if per.get(tab):
            out.append('<button data-tab="%s" aria-pressed="false">%s <span class="tn">%d</span></button>'
                       % (tab, nl.esc(kind), per[tab]))
    return '<div class="itabs">%s</div>' % ''.join(out)


def build():
    body, per, bysec = cards()
    n = sum(per.values())
    html = (TMPL.replace('__CSS__', style.BASE + KIND_CSS + CSS)
                .replace('__GUIDE__', guide(per))
                .replace('__TABS__', tabs(per) + sectabs(bysec))
                .replace('__CARDS__', body)
                .replace('__N__', str(n))
                .replace('__TABJS__', TAB_JS))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %s -> %s' % (' · '.join('%s %d' % (k, per[t]) for _d, k, t in KINDS if per.get(t)), OUT))


CSS = r'''
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
       border-radius:var(--r);padding:var(--pad);margin-top:12px;box-shadow:var(--shadow)}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:26px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;
                      color:var(--faint);transition:transform .3s cubic-bezier(.32,.72,0,1)}
  .ins[open]>summary::after{transform:rotate(180deg)}
  .cid{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;color:var(--accent)}
  .asof{float:right;font-size:var(--t-meta);color:var(--faint);font-variant-numeric:tabular-nums}
  .ins h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;line-height:1.36;margin:8px 0 2px}
  .ins .sub{font-size:var(--t-body);color:var(--faint);margin:3px 0 0}
  .bsec{font-size:var(--t-meta);font-weight:800;color:var(--accent2);margin:14px 0 5px;
        text-transform:uppercase;letter-spacing:.04em}
  .body p,.body li{font-size:var(--t-body);color:var(--sub);line-height:1.65}
  .body b{color:var(--ink)}
  .cite{font-size:.72em;font-weight:800;color:var(--accent);text-decoration:none;
        vertical-align:.28em;margin-left:2px;padding:0 3px;border-radius:4px;background:var(--sunk)}
  .itabs{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 4px}
  .itabs button{font:inherit;font-size:var(--t-meta);font-weight:700;padding:6px 13px;
        border:1px solid var(--line);border-radius:999px;background:transparent;
        color:var(--sub);cursor:pointer}
  .itabs button[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
  .itabs .tn{margin-left:6px;font-variant-numeric:tabular-nums;opacity:.7}
  .sectabs{margin-top:6px}
  .sectabs button{font-weight:600;color:var(--faint)}
  .sectabs button[aria-pressed="true"]{border-color:var(--ink);color:var(--ink)}
  .srcs{margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
  .srcs>summary{cursor:pointer;font-size:var(--t-meta);font-weight:700;color:var(--sub);
        list-style:none}
  .srcs>summary::-webkit-details-marker{display:none}
  .srcs>summary::before{content:"📄 ";opacity:.7}
  .srcs ul{margin:8px 0 0;padding-left:18px}
  .srcs li{font-size:var(--t-meta);line-height:1.8}
  .srcs a{color:var(--sub);text-decoration:none;border-bottom:1px solid var(--line)}
  .srcs a:hover{color:var(--accent)}

  /* 종류 묶음과 그 안의 주제 섹션 */
  .kgroup{margin-top:26px}
  .ktitle{font-size:var(--t-lead);font-weight:850;letter-spacing:-.01em;margin:0 0 2px}
  .kgroup[data-kind="brief"] .ktitle{color:var(--brief)}
  .kgroup[data-kind="cross"] .ktitle{color:var(--cross)}
  .isec{margin-top:16px}
  .ihead{display:flex;align-items:baseline;gap:9px;padding-bottom:6px;
        border-bottom:1px solid var(--line)}
  .inum{font-size:var(--t-lbl);font-weight:800;letter-spacing:.09em;color:var(--faint);
        font-variant-numeric:tabular-nums}
  .ihead h3{font-size:var(--t-body);font-weight:800;letter-spacing:-.01em;margin:0;color:var(--ink)}
  .icnt{margin-left:auto;font-size:var(--t-lbl);color:var(--faint);font-variant-numeric:tabular-nums}

  /* 종류마다 색을 달리한다 — 브리핑은 현황, 교차 인사이트는 판단이라 읽는 자세가 다르다 */
  .ins[data-kind="brief"]{border-left-color:var(--brief)}
  .ins[data-kind="brief"] .cid{color:var(--brief)}
  .ins[data-kind="brief"] .bsec{color:var(--brief)}
  .ins[data-kind="brief"] .cite{color:var(--brief)}
  .ins[data-kind="cross"]{border-left-color:var(--cross)}
  .ins[data-kind="cross"] .cid{color:var(--cross)}
  .ins[data-kind="cross"] .bsec{color:var(--cross)}
  .ins[data-kind="cross"] .cite{color:var(--cross)}

  /* 절이 이어 붙으면 어디서 화제가 바뀌는지 안 보인다 — 선을 하나 긋는다 */
  .body .bsec{position:relative;border-top:1px solid var(--line);
        margin:20px 0 8px;padding-top:14px}
  .body .bsec:first-child{border-top:0;margin-top:6px;padding-top:0}
  /* 표 — 좁은 화면에서는 표만 옆으로 밀린다 */
  .tw{overflow-x:auto;margin:8px 0 2px;-webkit-overflow-scrolling:touch}
  .body table{width:100%;border-collapse:collapse;font-size:var(--t-meta);
        background:var(--card)}
  .body th{text-align:left;font-weight:800;color:var(--faint);white-space:nowrap;
        border-bottom:1px solid var(--line);padding:7px 12px 7px 0;
        text-transform:uppercase;letter-spacing:.03em;font-size:var(--t-lbl)}
  .body td{color:var(--sub);line-height:1.6;vertical-align:top;
        border-bottom:1px solid var(--line);padding:8px 12px 8px 0}
  .body tbody tr:last-child td{border-bottom:0}
  .body td:first-child{color:var(--ink);font-weight:700;white-space:nowrap}
  .body td:nth-child(2){font-variant-numeric:tabular-nums}
  .body td:last-child{color:var(--faint);font-size:var(--t-lbl);line-height:1.5}

  /* 페이지 안내 — 두 종류가 무엇인지 먼저 알려 준다 */
  .guide{display:grid;gap:8px;margin:14px 0 2px}
  .guide div{border:1px solid var(--line);border-left:3px solid var(--line);
        border-radius:var(--r);background:var(--card);padding:10px 14px}
  .guide .g-brief{border-left-color:var(--brief)}
  .guide .g-cross{border-left-color:var(--cross)}
  .guide b{font-size:var(--t-meta);letter-spacing:.02em}
  .guide .g-brief b{color:var(--brief)}
  .guide .g-cross b{color:var(--cross)}
  .guide p{margin:3px 0 0;font-size:var(--t-meta);color:var(--sub);line-height:1.6}
  @media (min-width:680px){.guide{grid-template-columns:1fr 1fr}}
'''

# 종류 색은 밝기 대비를 지키는 선에서 고른다(다크 모드 값은 아래에서 덮어쓴다)
KIND_CSS = '''
  :root{--brief:#0f766e;--cross:#b45309}
  @media (prefers-color-scheme:dark){:root{--brief:#5eead4;--cross:#fbbf24}}
'''

TAB_JS = '''<script>
(function(){
  var kbar=document.querySelector('.itabs:not(.sectabs)');
  var sbar=document.querySelector('.sectabs');
  if(!kbar) return;
  var kind='all', sec='all';
  function apply(){
    document.querySelectorAll('.isec').forEach(function(s){
      s.hidden = !((kind==='all' || s.dataset.kind===kind) &&
                   (sec==='all'  || s.dataset.sec===sec));
    });
    // 남은 섹션이 하나도 없는 종류 묶음은 제목만 남으므로 통째로 접는다
    document.querySelectorAll('.kgroup').forEach(function(g){
      g.hidden = g.querySelectorAll('.isec:not([hidden])').length===0;
    });
    kbar.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.tab===kind));
    });
    if(sbar) sbar.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.sec===sec));
    });
  }
  kbar.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    kind=b.dataset.tab; apply();
  });
  if(sbar) sbar.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    sec=b.dataset.sec; apply();
  });
  apply();
})();
</script>'''

TMPL = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>통합 인사이트</title>
<style>__CSS__</style>
<div class="wrap">
<header>
  <p class="eyebrow">노트 45장을 가로질러</p>
  <h1>통합 인사이트</h1>
  <p class="lede">문서 하나를 요약한 페이지가 아닙니다. 원문마다 노트 한 장을 만들어 두고,
  그 노트 전량을 한 번에 읽어야 보이는 것만 올립니다. 문장 옆 줄번호를 누르면 근거가 된
  원문 그 줄로 가고, 카드 아래 「참고한 문서」를 펼치면 무엇을 읽고 썼는지 나옵니다.</p>
  <div class="meta"><span>판단 __N__건</span>
    <a class="maplink" href="Yomianalysis.html">전체 입구 →</a></div>
</header>
__GUIDE__
__TABS__
__CARDS__
__TABJS__
<footer>근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
