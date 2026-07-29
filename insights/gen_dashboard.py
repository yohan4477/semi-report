# 통합 인사이트 대시보드 생성 — insights/clusters/*.md + manifest → 자기완결 HTML
import os, re, io, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as cov
import facts as fct

ROOT = r"C:\Users\y\semianalysis"
MAN = os.path.join(ROOT, "insights", "manifest.json")
OUT = os.path.join(ROOT, "대시보드", "통합 인사이트.html")
MAP_URL = "https://claude.ai/code/artifact/a2742433-8236-4907-8a8a-96e070452455"
GH = "https://github.com/yohan4477/semi-report/blob/main/"

import urllib.parse
def gh_link(path): return GH + urllib.parse.quote(path)

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def inline(t):
    t = esc(t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)

def md_body(body):
    out, in_ul = [], False
    for line in body.splitlines():
        h = re.match(r'^##\s+(.*)$', line)
        li = re.match(r'^-\s+(.*)$', line)
        if h:
            if in_ul: out.append('</ul>'); in_ul = False
            out.append('<h4>%s</h4>' % inline(h.group(1).strip()))
        elif li:
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append('<li>%s</li>' % inline(li.group(1).strip()))
        elif line.strip() and not line.startswith('#'):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append('<p>%s</p>' % inline(line.strip()))
    if in_ul: out.append('</ul>')
    return '\n'.join(out)

def src_title(path):
    n = os.path.basename(path)
    n = re.sub(r'\.md$', '', n)
    n = re.sub(r'^\[\d{6}\]\s*', '', n)
    return n

SCOPE = {'und': ('제3자 해설', 'scope-und'), 'semi': ('SemiAnalysis 코퍼스', 'scope-semi'),
         'both': ('통합(코퍼스+제3자)', 'scope-both')}

def evidence_html(sources, man, scope):
    """근거 문서 원문에서 뽑은 사실을 문서별로. 대장은 쓰지 않는다 — 코퍼스가 기준."""
    docs = []
    for sid in sources:
        s = man.get(sid)
        if s:
            docs.append((s.get('date') or '', src_title(s['path']), s['path']))
    docs.sort(reverse=True)

    blocks, n, covered = [], 0, 0
    for date, title, path in docs:
        rs = fct.rows(path)
        if not rs:
            continue
        covered += 1
        n += len(rs)
        blocks.append(
            '<details class="doc"><summary><span class="sd">%s</span>%s <em>%d</em></summary><ul>%s</ul></details>'
            % (esc(date[2:]), esc(title), len(rs),
               ''.join('<li>%s%s</li>' % (('<span class="secx">%s</span>' % esc(sec)) if sec else '', inline(f))
                       for f, sec in rs)))

    if not blocks:
        return '<p class="lgnone">근거 문서에서 추출 가능한 정량 사실이 없습니다.</p>'
    return ('<details class="lg"><summary><b>핵심 사실 %d개</b> — 근거 문서 %d/%d편의 원문에서 추출</summary>'
            '<div class="docs">%s</div></details>' % (n, covered, len(docs), ''.join(blocks)))


def main():
    man = {s['id']: s for s in json.load(io.open(MAN, encoding='utf-8'))['sources']}
    clusters = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'insights', 'clusters', '*.md'))):
        t = io.open(p, encoding='utf-8').read()
        c = cov.parse_cluster(t)
        fm = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.DOTALL)
        meta, body = fm.group(1), fm.group(2)
        def sc(k):
            m = re.search(r'^%s:\s*(.*)$' % k, meta, re.M); return m.group(1).strip().strip('"') if m else ''
        clusters.append({'id': c['cluster_id'], 'title': sc('title'), 'subtitle': sc('subtitle'),
                         'scope': sc('corpus_scope'), 'as_of': sc('as_of'),
                         'sources': c['sources'], 'body': body})
    clusters.sort(key=lambda x: x['as_of'], reverse=True)

    blocks = []
    for c in clusters:
        # 근거 칩: 소스 → (title, date, link) 발행일 최신순
        chips = []
        for sid in c['sources']:
            s = man.get(sid)
            if not s: continue
            chips.append((src_title(s['path']), s.get('date') or '', gh_link(s['path'])))
        chips.sort(key=lambda x: x[1], reverse=True)
        chip_html = '\n'.join(
            '        <a class="src" href="%s" target="_blank" rel="noopener"><span class="sd">%s</span>%s</a>'
            % (href, d or '·', esc(t)) for t, d, href in chips)
        label, scls = SCOPE.get(c['scope'], (c['scope'], 'scope-und'))
        blocks.append(
            '    <details class="ins">\n'
            '      <summary>\n'
            '        <span class="cid">%s</span>\n'
            '        <span class="badge %s">%s</span>\n'
            '        <span class="asof">최신 근거 %s · 근거 %d건</span>\n'
            '        <h2>%s</h2>\n'
            '        <p class="sub">%s</p>\n'
            '      </summary>\n'
            '      <div class="body">\n%s\n      </div>\n'
            '      <p class="srclabel">근거 — 원문에서 뽑은 사실</p>\n'
            '      %s\n'
            '      <p class="srclabel">근거 소스 (발행일순)</p>\n'
            '      <div class="srcs">\n%s\n      </div>\n'
            '    </details>' % (esc(c['id']), scls, esc(label), esc(c['as_of']),
                               len(chips), esc(c['title']), esc(c['subtitle']),
                               md_body(c['body']),
                               evidence_html(c['sources'], man, c['scope']), chip_html))

    html = (TMPL.replace('__COUNT__', str(len(clusters)))
                .replace('__MAP_URL__', MAP_URL)
                .replace('__BLOCKS__', '\n'.join(blocks)))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %d clusters -> %s' % (len(clusters), OUT))

TMPL = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>통합 인사이트</title>
<style>
  :root{--bg:#f7f8fa;--card:#fff;--ink:#1a2233;--sub:#5b6577;--faint:#8892a3;--line:#e3e7ee;--accent:#2563eb;--accent2:#1e40af;--soft:#eaf1fe;--sunk:#eef1f5;--shadow:0 1px 2px rgba(26,34,51,.05)}
  @media (prefers-color-scheme:dark){:root{--bg:#12151c;--card:#1a1f2a;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#7e8798;--line:#2a3140;--accent:#7aa5f8;--accent2:#9ab8fa;--soft:#1e2a44;--sunk:#242b38;--shadow:none}}
  *{box-sizing:border-box}
  body{background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.64;margin:0;padding:0 20px 80px}
  .wrap{max-width:860px;margin:0 auto}
  header{padding:52px 0 6px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
  h1{font-size:clamp(28px,6vw,44px);font-weight:850;letter-spacing:-.035em;margin:0}
  h1::after{content:"";display:block;width:52px;height:3px;background:var(--accent);margin-top:14px;border-radius:2px}
  .lede{color:var(--sub);font-size:15px;margin:16px 0 0;max-width:62ch}
  .meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding-top:14px;border-top:1px solid var(--line);font-size:12.5px;color:var(--faint)}
  .maplink{color:var(--accent);font-weight:700;text-decoration:none}
  .maplink:hover{text-decoration:underline}
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:12px;padding:18px 22px;margin-top:14px;box-shadow:var(--shadow)}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:28px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;color:var(--faint);transition:transform .2s}
  .ins[open]>summary::after{transform:rotate(180deg)}
  .ins[open]>summary{border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:8px}
  .cid{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--accent)}
  .badge{font-size:10px;font-weight:800;letter-spacing:.04em;padding:2px 8px;border-radius:999px;margin-left:8px}
  .scope-und{background:var(--soft);color:var(--accent2)}
  .scope-semi{background:#e8f6ec;color:#1d6e45}
  .scope-both{background:#f6ecda;color:#9a5b12}
  @media (prefers-color-scheme:dark){.scope-semi{background:#173323;color:#63c08c}.scope-both{background:#2a2113;color:#d79a4e}}
  .asof{float:right;font-size:11px;color:var(--faint);font-variant-numeric:tabular-nums;margin-top:2px}
  .ins h2{font-size:21px;font-weight:850;letter-spacing:-.02em;margin:6px 0 2px}
  .ins .sub{font-size:13.5px;color:var(--faint);margin:0}
  .body h4{font-size:12.5px;font-weight:800;color:var(--accent2);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.04em}
  .body p{font-size:14.5px;line-height:1.62;margin:0 0 8px}
  .body ul{margin:0 0 8px;padding-left:18px}
  .body li{font-size:13.5px;color:var(--sub);line-height:1.58;margin-bottom:4px}
  .body b{color:var(--ink)}
  .lg{border:1px solid var(--line);border-radius:10px;background:var(--sunk);margin-bottom:8px}
  .lg>summary{cursor:pointer;padding:9px 13px;font-size:12.5px;color:var(--sub);list-style:none}
  .lg>summary::-webkit-details-marker{display:none}
  .lg>summary::before{content:"▸ ";color:var(--faint)}
  .lg[open]>summary::before{content:"▾ "}
  .lg>summary b{color:var(--ink)}
  .docs{border-top:1px solid var(--line);padding:6px 10px 10px}
  .doc{border-bottom:1px solid var(--line)}
  .doc:last-child{border-bottom:0}
  .doc>summary{cursor:pointer;padding:8px 2px;font-size:12.5px;color:var(--ink);list-style:none;display:flex;gap:8px;align-items:baseline}
  .doc>summary::-webkit-details-marker{display:none}
  .doc>summary .sd{font-size:10px;font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums;flex:0 0 auto}
  .doc>summary em{margin-left:auto;font-style:normal;font-size:10.5px;color:var(--faint);font-variant-numeric:tabular-nums}
  .doc ul{margin:0 0 10px;padding:0 0 0 2px;list-style:none;display:flex;flex-direction:column;gap:8px}
  .doc li{font-size:12.5px;color:var(--sub);line-height:1.55;padding-left:11px;border-left:2px solid var(--line)}
  .doc li b{color:var(--ink);font-weight:750}
  .secx{display:block;font-size:10px;font-weight:800;letter-spacing:.05em;color:var(--faint);margin-bottom:2px}
  .tw{overflow-x:auto;border-top:1px solid var(--line)}
  .nt{width:100%;border-collapse:collapse;font-size:12px}
  .nt thead th{position:sticky;top:0;background:var(--sunk);text-align:left;font-size:10px;font-weight:800;
               letter-spacing:.06em;text-transform:uppercase;color:var(--faint);padding:7px 10px;white-space:nowrap}
  .nt tbody th{text-align:left;font-weight:750;color:var(--ink);padding:7px 10px;vertical-align:top;min-width:150px}
  .nt td{padding:7px 10px;color:var(--sub);vertical-align:top}
  .nt tbody tr+tr{border-top:1px solid var(--line)}
  .nt .v{color:var(--ink);font-weight:750;font-variant-numeric:tabular-nums;white-space:nowrap}
  .nt .w,.nt .d{color:var(--faint);white-space:nowrap;font-variant-numeric:tabular-nums}
  .st{font-size:10px;font-weight:800;padding:2px 7px;border-radius:999px;white-space:nowrap}
  .st.wait{background:var(--soft);color:var(--accent2)}
  .st.hit{background:#e8f6ec;color:#1d6e45}
  .st.part{background:#f6ecda;color:#9a5b12}
  .st.miss{background:#fbe9e9;color:#a32626}
  @media (prefers-color-scheme:dark){.st.hit{background:#173323;color:#63c08c}.st.part{background:#2a2113;color:#d79a4e}.st.miss{background:#2e1a1a;color:#e08a8a}}
  .lgnone{font-size:12px;color:var(--faint);margin:0 0 8px}
  .srclabel{font-size:10.5px;font-weight:800;color:var(--faint);letter-spacing:.08em;text-transform:uppercase;margin:16px 0 7px}
  .srcs{display:flex;flex-wrap:wrap;gap:6px}
  .src{display:inline-flex;align-items:center;gap:7px;font-size:11.5px;padding:5px 11px;border-radius:999px;background:var(--sunk);border:1px solid var(--line);color:var(--sub);text-decoration:none;max-width:100%}
  .src:hover{border-color:var(--accent);color:var(--accent)}
  .src .sd{font-size:10px;font-weight:800;color:var(--accent);font-variant-numeric:tabular-nums}
  footer{margin-top:44px;padding-top:16px;border-top:2px solid var(--ink);font-size:12px;color:var(--faint);line-height:1.7}
</style>
<div class="wrap">
  <header>
    <p class="eyebrow">크로스-문서 합성 · 발행일 기준</p>
    <h1>통합 인사이트</h1>
    <p class="lede">여러 문서가 합쳐서 말하는 것 — 주제 클러스터별로 통합 논지·공통 진단·연결·인과·상충·이견·함의를 합성하고, 근거 소스를 발행일순으로 연결합니다. 제목을 클릭해 펼치세요.</p>
    <div class="meta"><span>클러스터 <b>__COUNT__</b></span><span>소스 = 근거 provenance</span><span>as_of = 최신 근거 발행일</span><span><a class="maplink" href="__MAP_URL__" target="_blank" rel="noopener">인사이트 지도에서 장소로 보기 ↗</a></span></div>
  </header>
__BLOCKS__
  <footer>인사이트 아키텍처(insights/) 산출물 — manifest(소스·발행일)+clusters(provenance)에서 생성. 클러스터 확신도·시계열은 근거 소스로 검증하세요.</footer>
</div>
'''

if __name__ == '__main__':
    main()
