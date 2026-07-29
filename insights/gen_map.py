# 인사이트 지도 (Esri식 스크롤리텔링) — 자기완결 SVG. clusters + cluster_geo.json → HTML
import os, re, io, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as cov

ROOT = r"C:\Users\y\semianalysis"
MOCKUP = os.path.join(ROOT, "대시보드", "데이터센터 지도 목업.html")
GEO = os.path.join(ROOT, "insights", "cluster_geo.json")
OUT = os.path.join(ROOT, "대시보드", "인사이트 지도.html")

W, H, LAT_MIN, LAT_MAX = 1000, 500, -58, 78
def project(lon, lat):
    return ((lon + 180) / 360 * W, (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H)

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

PALETTE = ['#2563eb', '#dc2626', '#16a34a', '#d97706', '#7c3aed', '#0891b2', '#db2777', '#65a30d', '#ea580c']

def world_path():
    t = io.open(MOCKUP, encoding='utf-8').read()
    m = re.search(r'WORLD_PATH\s*=\s*"([^"]+)"', t)
    return m.group(1) if m else ''

def main():
    geo = json.load(io.open(GEO, encoding='utf-8'))
    clusters = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'insights', 'clusters', '*.md'))):
        t = io.open(p, encoding='utf-8').read()
        c = cov.parse_cluster(t)
        fm = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.DOTALL)
        meta, body = fm.group(1), fm.group(2)
        def sc(k):
            mm = re.search(r'^%s:\s*(.*)$' % k, meta, re.M); return mm.group(1).strip().strip('"') if mm else ''
        thesis = ''
        bm = re.search(r'## 통합 논지\s*\n(.+)', body)
        if bm: thesis = bm.group(1).strip()
        cid = c['cluster_id']
        if cid in geo and geo[cid]:
            clusters.append({'id': cid, 'title': sc('title'), 'scope': sc('corpus_scope'),
                             'as_of': sc('as_of'), 'thesis': thesis, 'places': geo[cid]})
    clusters.sort(key=lambda x: x['as_of'], reverse=True)

    # 마커 + 라벨 + 스텝 카메라
    markers, labels, steps = [], [], []
    for i, c in enumerate(clusters):
        color = PALETTE[i % len(PALETTE)]
        xs, ys = [], []
        for pl in c['places']:
            x, y = project(pl['lon'], pl['lat']); xs.append(x); ys.append(y)
            markers.append('<circle class="mk mk-%d" cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (i, x, y, color))
            labels.append('<text class="lbl lbl-%d" x="%.1f" y="%.1f" data-y="%.1f" text-anchor="middle">%s</text>'
                          % (i, x, y - 7, y, esc(pl['place'])))
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        bw, bh = max(x1 - x0, 40), max(y1 - y0, 40)
        s = min(W / (bw * 2.2), H / (bh * 2.2)); s = max(1.4, min(s, 7))
        tx, ty = W / 2 - s * cx, H / 2 - s * cy
        place_html = ''.join(
            '<li><b>%s</b> <span>%s</span></li>' % (esc(pl['place']), esc(pl.get('note', '')))
            for pl in c['places'])
        badge = {'semi': ('코퍼스', 'b-semi'), 'und': ('제3자', 'b-und'), 'both': ('통합', 'b-both')}.get(c['scope'], (c['scope'], 'b-und'))
        steps.append(
            '  <section class="step" data-i="%d" data-cam="%.2f %.2f %.3f" style="--c:%s">\n'
            '    <div class="card">\n'
            '      <div class="chd"><span class="cid">%s</span><span class="bdg %s">%s</span>'
            '<span class="ao">최신 %s</span></div>\n'
            '      <h2>%s</h2>\n<p class="th">%s</p>\n'
            '      <ul class="pl">%s</ul>\n'
            '      <a class="more" href="%s" target="_blank" rel="noopener">통합 인사이트에서 전체 보기 ↗</a>\n'
            '    </div>\n  </section>' % (
                i, tx, ty, s, color, esc(c['id']), badge[1], badge[0], esc(c['as_of']),
                esc(c['title']), esc(c['thesis']), place_html, INS_URL))

    html = (TMPL.replace('__WORLD__', world_path())
                .replace('__MARKERS__', '\n'.join(markers))
                .replace('__LABELS__', '\n'.join(labels))
                .replace('__STEPS__', '\n'.join(steps))
                .replace('__COUNT__', str(len(clusters))))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %d clusters, %d markers -> %s' % (len(clusters), len(markers), OUT))

INS_URL = "https://claude.ai/code/artifact/6acd6d5a-9c65-4c23-8225-6885b35add31"

TMPL = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>인사이트 지도</title>
<style>
  :root{--bg:#0b0f17;--panel:#111826;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#6b7688;--line:#222c3d;--accent:#7aa5f8;--sea:#0e1622;--land:#1c2636;--landln:#2b3a52}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.6}
  .intro{max-width:820px;margin:0 auto;padding:64px 22px 20px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 12px}
  h1{font-size:clamp(28px,6vw,46px);font-weight:850;letter-spacing:-.035em;margin:0}
  .lede{color:var(--sub);font-size:15px;margin:14px 0 0;max-width:60ch}
  .hint{color:var(--faint);font-size:12.5px;margin-top:18px}
  .scrolly{position:relative;max-width:1200px;margin:0 auto;padding:0 22px}
  .mapwrap{position:sticky;top:0;height:100vh;display:flex;align-items:center;justify-content:center;z-index:1}
  svg#map{width:100%;height:78vh;background:var(--sea);border:1px solid var(--line);border-radius:14px}
  #cam{transition:transform 1.1s cubic-bezier(.65,0,.35,1)}
  .land{fill:var(--land);stroke:var(--landln);stroke-width:.4}
  .mk{opacity:.28;transition:opacity .5s, r .5s;stroke:#0b0f17;stroke-width:1.4;vector-effect:non-scaling-stroke}
  .mk.on{opacity:1}
  .lbl{fill:var(--ink);font-size:8px;font-weight:700;paint-order:stroke;stroke:#0b0f17;stroke-width:2.6px;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .5s}
  .lbl.on{opacity:1}
  .steps{position:relative;z-index:2;margin-top:-100vh;pointer-events:none}
  .step{min-height:100vh;display:flex;align-items:center;max-width:430px}
  .card{pointer-events:auto;background:rgba(17,24,38,.92);backdrop-filter:blur(8px);border:1px solid var(--line);border-left:3px solid var(--c);border-radius:14px;padding:20px 22px;box-shadow:0 8px 40px rgba(0,0,0,.5)}
  .chd{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px}
  .cid{font-size:11px;font-weight:800;letter-spacing:.1em;color:var(--c)}
  .bdg{font-size:10px;font-weight:800;padding:2px 8px;border-radius:999px}
  .b-semi{background:#15251b;color:#63c08c}.b-und{background:#1e2a44;color:#9ab8fa}.b-both{background:#2a2113;color:#d79a4e}
  .ao{margin-left:auto;font-size:11px;color:var(--faint)}
  .card h2{font-size:20px;font-weight:850;letter-spacing:-.02em;margin:2px 0 8px}
  .th{font-size:14px;color:var(--sub);margin:0 0 12px}
  .pl{list-style:none;margin:0 0 14px;padding:0;display:flex;flex-direction:column;gap:7px}
  .pl li{font-size:12.5px;padding-left:14px;position:relative}
  .pl li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--c)}
  .pl li b{color:var(--ink)}.pl li span{color:var(--faint)}
  .more{font-size:12px;font-weight:700;color:var(--accent);text-decoration:none}
  footer{max-width:820px;margin:0 auto;padding:40px 22px 80px;color:var(--faint);font-size:12px;border-top:1px solid var(--line)}
  @media(max-width:720px){.step{max-width:100%}.mapwrap{height:56vh;position:sticky}svg#map{height:52vh}.steps{margin-top:-56vh}.step{min-height:88vh}}
</style>
<div class="intro">
  <p class="eyebrow">인사이트 지도 · 스크롤리텔링</p>
  <h1>인사이트가 벌어지는 곳</h1>
  <p class="lede">통합 인사이트 __COUNT__개 클러스터의 핵심 장소를 지도 위에서 따라갑니다 — 스크롤하면 지도가 해당 지역으로 이동하고, 그 인사이트의 논지와 장소가 나타납니다.</p>
  <p class="hint">↓ 스크롤해서 시작</p>
</div>
<div class="scrolly">
  <div class="mapwrap">
    <svg id="map" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet" role="img" aria-label="인사이트 세계 지도">
      <g id="cam">
        <path class="land" d="__WORLD__"/>
        __MARKERS__
        __LABELS__
      </g>
    </svg>
  </div>
  <div class="steps">
__STEPS__
  </div>
</div>
<footer>자기완결 SVG(Natural Earth 110m) · 외부 로드 없음. 좌표·장소는 편집 주석이며 정밀 GIS 아님. insights/cluster_geo.json + gen_map.py 산출물.</footer>
<script>
(function(){
  var cam=document.getElementById('cam');
  var steps=[].slice.call(document.querySelectorAll('.step'));
  var scale=1;
  // 라벨은 카메라 그룹 안이라 확대되면 같이 커짐 → 활성 시 1/scale로 역보정
  function setCam(tx,ty,s){ scale=s; cam.setAttribute('transform','translate('+tx+','+ty+') scale('+s+')'); }
  function activate(i){
    document.querySelectorAll('.mk').forEach(function(m){ m.classList.remove('on'); m.setAttribute('r',(4/scale).toFixed(2)); });
    document.querySelectorAll('.lbl').forEach(function(l){ l.classList.remove('on'); });
    document.querySelectorAll('.mk-'+i).forEach(function(m){ m.classList.add('on'); m.setAttribute('r',(6/scale).toFixed(2)); });
    document.querySelectorAll('.lbl-'+i).forEach(function(l){
      l.classList.add('on');
      l.style.fontSize=(8.5/scale).toFixed(2)+'px';
      l.setAttribute('y',(+l.getAttribute('data-y')-7/scale).toFixed(2));
    });
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(e.isIntersecting){
        var s=e.target, cm=s.getAttribute('data-cam').split(' ');
        setCam(+cm[0],+cm[1],+cm[2]); activate(+s.getAttribute('data-i'));
      }
    });
  },{rootMargin:'-45% 0px -45% 0px', threshold:0});
  steps.forEach(function(s){ io.observe(s); });
  if(steps[0]){ var c=steps[0].getAttribute('data-cam').split(' '); setCam(+c[0],+c[1],+c[2]); activate(0); }
})();
</script>
'''

if __name__ == '__main__':
    main()
