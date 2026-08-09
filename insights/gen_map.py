# 인사이트 지도 (Esri식 스크롤리텔링) — 자기완결 SVG. clusters + cluster_geo.json → HTML
import os, re, io, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as cov

ROOT = r"C:\Users\y\semianalysis"
# 세계지도 path는 데이터다 — 예전엔 목업 HTML에서 정규식으로 긁어 썼는데
# 2026-08-09에 그 목업을 지우면서 이 생성기가 조용히 깨졌다. 데이터를 산출물에
# 숨겨 두면 산출물을 지우는 순간 생성기가 죽는다
WORLD = os.path.join(ROOT, "insights", "world_path.txt")
GEO = os.path.join(ROOT, "insights", "cluster_geo.json")
OUT = os.path.join(ROOT, "대시보드", "인사이트 지도.html")

W, H, LAT_MIN, LAT_MAX = 1000, 500, -58, 78
def project(lon, lat):
    return ((lon + 180) / 360 * W, (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * H)

def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def inline(t):
    """클러스터 본문의 **굵게**·[[링크]]를 HTML로. 인사이트의 수치·고유명을 살리는 용도."""
    t = re.sub(r'\[\[([^\]]+)\]\]', r'\1', t)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', esc(t))

def section(body, name):
    """## 섹션의 불릿을 리스트로."""
    m = re.search(r'## %s\s*\n(.*?)(?=\n## |\Z)' % re.escape(name), body, re.DOTALL)
    if not m: return []
    return [inline(x.strip()) for x in re.findall(r'^- (.+)$', m.group(1), re.M)]

PALETTE = ['#2563eb', '#dc2626', '#16a34a', '#d97706', '#7c3aed', '#0891b2', '#db2777', '#65a30d', '#ea580c']
LBL_CH, LBL_H = 10.5, 14.0           # 화면 px 기준 글자폭·줄높이(라벨 폰트 11px)
LBL_DY = [-9.0, 19.0, -25.0, 35.0]   # 마커 기준 후보 오프셋(위·아래 교대)

def world_path():
    return io.open(WORLD, encoding='utf-8').read().strip()

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
                             'as_of': sc('as_of'), 'thesis': inline(thesis), 'places': geo[cid],
                             'sub': sc('subtitle'), 'n_src': len(c.get('sources') or []),
                             'dx': section(body, '공통 진단'),
                             'gap': section(body, '상충·이견'),
                             'watch': section(body, '함의·다음 확인 포인트')})
    clusters.sort(key=lambda x: x['as_of'], reverse=True)

    # 마커 + 라벨 + 스텝 카메라
    markers, labels, steps, chips = [], [], [], []
    for i, c in enumerate(clusters):
        color = PALETTE[i % len(PALETTE)]
        pts = [project(pl['lon'], pl['lat']) for pl in c['places']]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        bw, bh = max(x1 - x0, 40), max(y1 - y0, 40)
        s = min(W / (bw * 2.2), H / (bh * 2.2)); s = max(1.4, min(s, 7))
        tx, ty = W / 2 - s * cx, H / 2 - s * cy
        # 라벨 겹침 해소: 이 스텝의 확대율(s) 기준 화면 좌표에서 상/하 스태거
        placed = []
        for (x, y), pl in zip(pts, c['places']):
            markers.append('<circle class="mk mk-%d" cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (i, x, y, color))
            sx, sy = x * s, y * s
            half = len(pl['place']) * LBL_CH / 2
            dy = LBL_DY[0]
            for cand in LBL_DY:
                box = (sx - half, sy + cand - LBL_H, sx + half, sy + cand)
                if not any(box[0] < b[2] and b[0] < box[2] and box[1] < b[3] and b[1] < box[3] for b in placed):
                    dy = cand; break
            placed.append((sx - half, sy + dy - LBL_H, sx + half, sy + dy))
            labels.append('<text class="lbl lbl-%d" x="%.1f" y="%.1f" data-y="%.1f" data-dy="%d" text-anchor="middle">%s</text>'
                          % (i, x, y + dy / s, y, dy, esc(pl['place'])))
        place_html = ''.join(
            '<li><b>%s</b> <span>%s</span></li>' % (esc(pl['place']), inline(pl.get('note', '')))
            for pl in c['places'])
        def block(cls, head, items, limit):
            if not items: return ''
            return ('<div class="blk %s"><h3>%s</h3><ul>%s</ul></div>'
                    % (cls, head, ''.join('<li>%s</li>' % x for x in items[:limit])))
        detail = (block('dx', '핵심 진단', c['dx'], 3)
                  + block('gap', '이견·미검증', c['gap'], 3)
                  + block('watch', '지켜볼 것', c['watch'], 2))
        badge = {'semi': ('코퍼스', 'b-semi'), 'und': ('제3자', 'b-und'), 'both': ('통합', 'b-both')}.get(c['scope'], (c['scope'], 'b-und'))
        chips.append(
            '    <button class="chip" role="tab" id="tab-%d" aria-controls="panel-%d" aria-selected="%s"'
            ' data-i="%d" data-cam="%.2f %.2f %.3f" style="--c:%s">'
            '<span class="cid">%s</span><span class="ct">%s</span></button>' % (
                i, i, 'true' if i == 0 else 'false', i, tx, ty, s, color,
                esc(c['id']), esc(c['title'].split(' — ')[0])))
        steps.append(
            '  <section class="panel" id="panel-%d" role="tabpanel" aria-labelledby="tab-%d"%s style="--c:%s">\n'
            '    <div class="chd"><span class="bdg %s">%s</span><span class="ao">근거 %d건 · 최신 %s</span>'
            '<span class="ao">장소 %d곳</span></div>\n'
            '    <h2>%s</h2>\n    <p class="th">%s</p>\n'
            '    <h3 class="plh">지도 위 장소</h3>\n    <ul class="pl">%s</ul>\n'
            '    <div class="blks">%s</div>\n'
            '    <a class="more" href="%s" target="_blank" rel="noopener">통합 인사이트에서 전체 보기 ↗</a>\n'
            '  </section>' % (
                i, i, '' if i == 0 else ' hidden', color, badge[1], badge[0], c['n_src'], esc(c['as_of']),
                len(c['places']), esc(c['title']), c['thesis'], place_html, detail, INS_URL))

    html = (TMPL.replace('__WORLD__', world_path())
                .replace('__MARKERS__', '\n'.join(markers))
                .replace('__LABELS__', '\n'.join(labels))
                .replace('__CHIPS__', '\n'.join(chips))
                .replace('__STEPS__', '\n'.join(steps))
                .replace('__COUNT__', str(len(clusters))))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %d clusters, %d markers -> %s' % (len(clusters), len(markers), OUT))

INS_URL = "https://yohan4477.github.io/semi-report/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/%EC%9D%B8%EC%82%AC%EC%9D%B4%ED%8A%B8%EC%99%80%20%EA%B7%BC%EA%B1%B0.html"

TMPL = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>인사이트 지도</title>
<style>
  :root{--bg:#0b0f17;--panel:#111826;--ink:#e8ecf4;--sub:#9aa5b8;--faint:#6b7688;--line:#222c3d;--accent:#7aa5f8;--sea:#0e1622;--land:#1c2636;--landln:#2b3a52}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;line-height:1.6}
  .wrap{max-width:1080px;margin:0 auto;padding:0 20px 72px}
  header{padding:40px 0 18px}
  .eyebrow{font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);margin:0 0 10px}
  h1{font-size:clamp(26px,5.2vw,40px);font-weight:850;letter-spacing:-.035em;margin:0;text-wrap:balance}
  .lede{color:var(--sub);font-size:14.5px;margin:12px 0 0;max-width:62ch}
  .mapwrap{position:relative;border:1px solid var(--line);border-radius:14px;background:var(--sea);overflow:hidden}
  svg#map{display:block;width:100%;height:auto;aspect-ratio:2/1;max-height:66dvh}
  #cam{transition:transform 1s cubic-bezier(.65,0,.35,1)}
  .land{fill:var(--land);stroke:var(--landln);stroke-width:.4}
  .mk{opacity:.22;transition:opacity .5s, r .5s;stroke:#0b0f17;stroke-width:1.4;vector-effect:non-scaling-stroke}
  .mk.on{opacity:1}
  .lbl{fill:var(--ink);font-size:8px;font-weight:700;paint-order:stroke;stroke:#0b0f17;stroke-width:2.6px;vector-effect:non-scaling-stroke;opacity:0;transition:opacity .5s;pointer-events:none}
  .lbl.on{opacity:1}
  .nav{position:absolute;right:10px;bottom:10px;display:flex;gap:6px}
  .nav button{width:32px;height:32px;border-radius:8px;border:1px solid var(--line);background:rgba(11,15,23,.82);color:var(--ink);font-size:15px;cursor:pointer;line-height:1}
  .nav button:hover{border-color:var(--accent);color:var(--accent)}
  .rail{display:flex;gap:8px;overflow-x:auto;padding:14px 2px 4px;scrollbar-width:thin}
  .chip{flex:0 0 auto;display:flex;flex-direction:column;gap:2px;align-items:flex-start;text-align:left;cursor:pointer;
        background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:11px;padding:9px 13px;color:var(--sub);font:inherit}
  .chip .cid{font-size:10px;font-weight:800;letter-spacing:.1em;color:var(--c)}
  .chip .ct{font-size:13px;font-weight:750;color:var(--ink);white-space:nowrap}
  .chip[aria-selected="true"]{background:#16203200;box-shadow:inset 0 0 0 1px var(--c);border-color:var(--c)}
  .chip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .panel{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--c);border-radius:14px;padding:20px 22px;margin-top:10px}
  .chd{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px}
  .bdg{font-size:10px;font-weight:800;padding:2px 8px;border-radius:999px}
  .b-semi{background:#15251b;color:#63c08c}.b-und{background:#1e2a44;color:#9ab8fa}.b-both{background:#2a2113;color:#d79a4e}
  .ao{font-size:11px;color:var(--faint);font-variant-numeric:tabular-nums}
  .ao:nth-of-type(2){margin-left:auto}
  .panel h2{font-size:21px;font-weight:850;letter-spacing:-.02em;margin:4px 0 8px;text-wrap:balance}
  .th{font-size:14.5px;color:var(--sub);margin:0 0 14px}
  .plh{font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);margin:0 0 8px}
  .pl{list-style:none;margin:0 0 18px;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:8px 20px}
  .pl li{font-size:13px;padding-left:14px;position:relative}
  .pl li::before{content:"";position:absolute;left:0;top:8px;width:6px;height:6px;border-radius:50%;background:var(--c)}
  .pl li b{color:var(--ink)}.pl li span{color:var(--faint)}
  .blks{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:0 0 16px;padding-top:16px;border-top:1px solid var(--line)}
  .blk h3{font-size:10.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin:0 0 8px;
          display:inline-block;padding:2px 8px;border-radius:5px}
  .blk.dx h3{background:#132133;color:#7aa5f8}
  .blk.gap h3{background:#2a1b18;color:#e08a6a}
  .blk.watch h3{background:#15251b;color:#63c08c}
  .blk ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
  .blk li{font-size:12.5px;color:var(--sub);line-height:1.55;padding-left:11px;border-left:2px solid var(--line)}
  .blk li b{color:var(--ink);font-weight:750}
  .more{font-size:12.5px;font-weight:700;color:var(--accent);text-decoration:none}
  .more:hover{text-decoration:underline}
  footer{margin-top:30px;padding-top:16px;border-top:1px solid var(--line);color:var(--faint);font-size:12px}
  @media(prefers-reduced-motion:reduce){#cam{transition:none}.mk,.lbl{transition:none}}
  @media(max-width:640px){svg#map{aspect-ratio:3/2}.pl{grid-template-columns:1fr}}
</style>
<div class="wrap">
  <header>
    <p class="eyebrow">통합 인사이트 · 장소로 보기</p>
    <h1>인사이트가 벌어지는 곳</h1>
    <p class="lede">__COUNT__개 클러스터의 핵심 장소를 지도 위에 놓았습니다. 클러스터를 고르면 지도가 그 지역으로 이동하고, 논지와 장소가 아래에 펼쳐집니다.</p>
  </header>
  <div class="mapwrap">
    <svg id="map" viewBox="0 0 1000 500" preserveAspectRatio="xMidYMid meet" role="img" aria-label="인사이트 세계 지도">
      <g id="cam">
        <path class="land" d="__WORLD__"/>
        __MARKERS__
        __LABELS__
      </g>
    </svg>
    <div class="nav"><button id="prev" aria-label="이전 클러스터">‹</button><button id="next" aria-label="다음 클러스터">›</button></div>
  </div>
  <div class="rail" role="tablist" aria-label="인사이트 클러스터">
__CHIPS__
  </div>
__STEPS__
  <footer>자기완결 SVG(Natural Earth 110m) · 외부 로드 없음. 좌표·장소는 편집 주석이며 정밀 GIS 아님. insights/cluster_geo.json + gen_map.py 산출물.</footer>
</div>
<script>
(function(){
  var cam=document.getElementById('cam');
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var panels=[].slice.call(document.querySelectorAll('.panel'));
  var svg=document.getElementById('map');
  var scale=1, cur=0;
  // 화면 px → SVG 사용자 단위 환산. viewBox 1000 폭이 실제 몇 px로 그려지는지(unit)와
  // 카메라 확대율(scale)을 함께 되돌려야 라벨·마커가 어느 스텝에서나 같은 크기로 보인다.
  function k(){ var w=svg.getBoundingClientRect().width||1000; return 1/(scale*(w/1000)); }
  function paint(i){
    var u=k();
    document.querySelectorAll('.mk').forEach(function(m){ m.classList.remove('on'); m.setAttribute('r',(4*u).toFixed(2)); });
    document.querySelectorAll('.lbl').forEach(function(l){ l.classList.remove('on'); });
    document.querySelectorAll('.mk-'+i).forEach(function(m){ m.classList.add('on'); m.setAttribute('r',(6*u).toFixed(2)); });
    document.querySelectorAll('.lbl-'+i).forEach(function(l){
      l.classList.add('on');
      l.style.fontSize=(11*u).toFixed(2)+'px';
      l.setAttribute('y',(+l.getAttribute('data-y')+(+l.getAttribute('data-dy'))*u).toFixed(2));
    });
  }
  function select(i,focus){
    if(i<0) i=chips.length-1; if(i>=chips.length) i=0;
    cur=i;
    var cm=chips[i].getAttribute('data-cam').split(' ');
    scale=+cm[2];
    cam.setAttribute('transform','translate('+cm[0]+','+cm[1]+') scale('+cm[2]+')');
    chips.forEach(function(c,j){ c.setAttribute('aria-selected', j===i?'true':'false'); });
    panels.forEach(function(p,j){ p.hidden = j!==i; });
    chips[i].scrollIntoView({block:'nearest',inline:'nearest',behavior:'smooth'});
    if(focus) chips[i].focus();
    paint(i);
  }
  chips.forEach(function(c,i){
    c.addEventListener('click',function(){ select(i); });
    c.addEventListener('keydown',function(e){
      if(e.key==='ArrowRight'){e.preventDefault();select(i+1,true);}
      if(e.key==='ArrowLeft'){e.preventDefault();select(i-1,true);}
    });
  });
  document.getElementById('prev').addEventListener('click',function(){ select(cur-1); });
  document.getElementById('next').addEventListener('click',function(){ select(cur+1); });
  select(0);
  var rt; addEventListener('resize',function(){ clearTimeout(rt); rt=setTimeout(function(){ paint(cur); },150); });
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(function(){ paint(cur); });
})();
</script>
'''

if __name__ == '__main__':
    main()
