# ⚛️ 인사이트와 근거 — 판단을 읽고, 문장 옆 줄번호를 누르면 원문 그 줄로 간다.
# 옛 gen_atomview.py에 있던 근거 지도(스택 10칸·프로세스 7단계)와 구조 뷰,
# 검증 대장은 뺐다. 사용자가 실제로 읽는 것은 판단 본문 하나였다.
import io, os, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths, style
import notes_lib as nl

OUT = os.path.join(paths.ROOT, '대시보드', '인사이트와 근거.html')


def cards():
    out, n = [], 0
    for d, kind in ((paths.THESES, '종합 판단'), (paths.SYNTH, '인사이트')):
        for p in sorted(glob.glob(os.path.join(d, '*.md')), reverse=True):
            meta, body = nl.parse_front(io.open(p, encoding='utf-8').read())
            src = nl.sources_of(meta)
            head = meta.get('headline') or os.path.basename(p)[:-3]
            sub = meta.get('subhead', '')
            out.append('<details class="ins"><summary><span class="cid">%s</span>'
                       '<span class="asof">as_of %s</span><h2>%s</h2>'
                       '<p class="sub">%s</p></summary><div class="body">%s</div></details>'
                       % (nl.esc(kind), nl.esc(meta.get('as_of', '')),
                          nl.esc(head), nl.esc(sub), nl.md_body(body, src, 'h4', 'bsec')))
            n += 1
    return ''.join(out), n


def build():
    body, n = cards()
    html = (TMPL.replace('__CSS__', style.BASE + CSS)
                .replace('__CARDS__', body)
                .replace('__N__', str(n)))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: 인사이트 %d건 -> %s' % (n, OUT))


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
'''

TMPL = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>인사이트와 그 근거</title>
<style>__CSS__</style>
<div class="wrap">
<header>
  <p class="eyebrow">Insights &amp; Evidence</p>
  <h1>인사이트와 그 근거</h1>
  <p class="lede">판단을 먼저 읽고, 문장 옆의 파란 줄번호를 누르면 그 문장의 근거가 된
  원문 줄로 갑니다.</p>
  <div class="meta"><span>판단 __N__건</span>
    <a class="maplink" href="Yomianalysis.html">전체 입구 →</a></div>
</header>
__CARDS__
<footer>근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
