# 🧩 통합 인사이트 — 노트를 통째로 읽고 교차에서 나온 판단만 싣는다.
# 카드를 모아 두는 페이지가 아니라, 문서 여러 편을 가로질러야 보이는 것만 남긴다.
# 문장 옆 줄번호를 누르면 근거가 된 원문 그 줄로 간다.
import io, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths, style
import notes_lib as nl

OUT = os.path.join(paths.ROOT, '대시보드', '통합 인사이트.html')


# (디렉터리, 배지 이름, 탭 id) — 탭은 이 순서로 선다
KINDS = ((paths.SYNTH, '교차 인사이트', 'cross'),
         (paths.DIGESTS, '정리본', 'digest'),
         (paths.THESES, '종합 판단', 'thesis'))


def cards():
    out, per = [], {}
    for d, kind, tab in KINDS:
        for p in sorted(glob.glob(os.path.join(d, '*.md')), reverse=True):
            meta, body = nl.parse_front(io.open(p, encoding='utf-8').read())
            src = nl.sources_of(meta)
            head = meta.get('headline') or os.path.basename(p)[:-3]
            sub = meta.get('subhead', '')
            out.append('<details class="ins" data-kind="%s"><summary><span class="cid">%s</span>'
                       '<span class="asof">as_of %s</span><h2>%s</h2>'
                       '<p class="sub">%s</p></summary><div class="body">%s</div></details>'
                       % (tab, nl.esc(kind), nl.esc(meta.get('as_of', '')),
                          nl.esc(head), nl.esc(sub), nl.md_body(body, src, 'h4', 'bsec')))
            per[tab] = per.get(tab, 0) + 1
    return ''.join(out), per


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
    body, per = cards()
    n = sum(per.values())
    html = (TMPL.replace('__CSS__', style.BASE + CSS)
                .replace('__TABS__', tabs(per))
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
'''

TAB_JS = '''<script>
(function(){
  var bar=document.querySelector('.itabs'); if(!bar) return;
  bar.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    var pick=b.dataset.tab;
    document.querySelectorAll('.ins[data-kind]').forEach(function(c){
      c.hidden = !(pick==='all' || c.dataset.kind===pick);
    });
    bar.querySelectorAll('button').forEach(function(x){
      x.setAttribute('aria-pressed', String(x.dataset.tab===pick));
    });
  });
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
  <p class="lede">문서 하나를 요약한 것이 아니라, 노트 전량을 한 번에 읽어야 보이는 것만
  올립니다. 문장 옆의 파란 줄번호를 누르면 그 근거가 된 원문 줄로 갑니다.</p>
  <div class="meta"><span>판단 __N__건</span>
    <a class="maplink" href="Yomianalysis.html">전체 입구 →</a></div>
</header>
__TABS__
__CARDS__
__TABJS__
<footer>근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
