# 추적판 — 「얘네가 지금 뭘 하고 있나」를 한 번에 읽히게.
#
# 2026-08-09에 한 번 갈아엎었다. 처음엔 원자를 모아 목록으로 쌓았는데 읽히지 않았다.
# 원자는 「이 주장의 근거가 뭐냐」를 되짚는 단위지, 「지금 무슨 일이 벌어지나」를
# 서술하는 단위가 아니다. 조건이 붙은 문장 스물일곱 개를 쌓아도 이야기가 안 된다.
# 게다가 원자 층은 코퍼스의 일부만 덮는다 — 그때 xAI가 「221일째 조용」으로 나왔는데,
# 사실은 xAI 콜로서스 2 전용 클리핑(언급 107회)이 원자화 안 된 채 있었을 뿐이었다.
#
# 그래서 지금은 반대로 간다. 원문을 통째로 읽고 쓴 서술(insights/tracks/<key>.md)이
# 본문이고, 이 파일은 그것을 렌더한다. 문장 뒤의 (파일이름 L123)은 원문 그 줄로 링크된다.
import os, io, re, sys, json, datetime, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths
import style

ROOT = paths.ROOT
ENT = os.path.join(ROOT, 'insights', 'views', 'entities.json')
TRACKS = os.path.join(ROOT, 'insights', 'tracks')
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
WORLD = os.path.join(ROOT, 'insights', 'world_path.txt')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'
TODAY = datetime.date.today()

MW, MH, LAT_MIN, LAT_MAX = 1000.0, 500.0, -58.0, 78.0


def esc(s):
    return (str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def project(lon, lat):
    return ((lon + 180) / 360 * MW, (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * MH)


# ── 서술 본문 ─────────────────────────────────────────────────────────
def load_track(key):
    p = os.path.join(TRACKS, key + '.md')
    t = io.open(p, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
    head, body = m.group(1), m.group(2)
    src = []
    for line in re.findall(r'^\s*-\s*\{(.+)\}\s*$', head, re.M):
        d = dict(re.findall(r'(\w+):\s*"([^"]*)"', line))
        if d.get('file'):
            d['base'] = os.path.basename(d['file']).rsplit('.md', 1)[0]
            src.append(d)
    meta = dict(re.findall(r'^(\w+):\s*(.+)$', head, re.M))
    return meta, src, body


CITE = re.compile(r'\(([^()]{3,80}?)\s*(L\d[\d,\sL–-]*)\)')


def link_cites(text, src):
    """(파일이름 L123) → 원문 그 줄로 가는 각주. 서술과 근거를 한 클릭 거리에 둔다."""
    def one(m):
        label, lines = m.group(1).strip().rstrip(','), m.group(2)
        # 라벨은 사람이 줄여 쓴 것이라 파일명 앞머리와 안 맞을 수 있다
        # (예: 「온사이트 가스 딥다이브」 vs 「[251231] AI 랩들은 …」). 부분 일치로 찾는다
        key = label[:18]
        hit = next((s for s in src if s['base'].startswith(key) or key in s['base']), None)
        nums = re.findall(r'L(\d+)', lines)
        if not hit or not nums:
            return m.group(0)
        url = BLOB + urllib.parse.quote(hit['file'].replace('\\', '/')) + '#L' + nums[0]
        return ('<a class="cite" href="%s" target="_blank" rel="noopener" title="%s">%s</a>'
                % (url, esc(hit['base']), esc(lines.replace(' ', ''))))
    return CITE.sub(one, text)


def md_body(body, src):
    """작은 마크다운만 쓴다 — ##, 문단, **굵게**. 그 이상은 이 판에 필요 없다."""
    out = []
    for block in re.split(r'\n\s*\n', body.strip()):
        b = block.strip()
        if not b:
            continue
        h = re.match(r'^##\s+(.+)$', b)
        if h:
            out.append('<h2 class="tsec">%s</h2>' % esc(h.group(1)))
            continue
        p = esc(b).replace('\n', ' ')
        p = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', p)
        out.append('<p>%s</p>' % link_cites(p, src))
    return ''.join(out)


# ── 신호 (최신성만 담당) ──────────────────────────────────────────────
def signal_hits(alias, cap=6):
    if not os.path.exists(HIST):
        return []
    h = io.open(HIST, encoding='utf-8').read()
    out, date = [], None
    for chunk in re.split(r'(<h3>\d{4}-\d{2}-\d{2}</h3>)', h):
        m = re.match(r'<h3>(\d{4}-\d{2}-\d{2})</h3>', chunk)
        if m:
            date = m.group(1)
            continue
        if not date:
            continue
        for row in re.findall(r'<div class="row">.*?(?=<div class="row">|<div class="day">|$)',
                              chunk, re.S):
            sn = re.search(r'<span class="sn">(.*?)</span>', row, re.S)
            href = re.search(r'href="([^"]+)"', row)
            if not sn:
                continue
            txt = re.sub(r'<[^>]+>', '', sn.group(1)).strip()
            if any(x in txt for x in alias):
                out.append({'date': date, 'text': txt, 'url': href.group(1) if href else ''})
    out.sort(key=lambda r: r['date'], reverse=True)
    return out[:cap]


# ── 지도 ──────────────────────────────────────────────────────────────
def site_map(ent):
    sites = ent.get('sites') or []
    if not sites:
        return ''
    times = sorted({p['t'] for s in sites for p in s['timeline']},
                   key=lambda t: (t == '계획', t))
    pts = [project(s['lon'], s['lat']) for s in sites]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    pad = max(28.0, (x1 - x0) * .55, (y1 - y0) * .55)
    vb = (x0 - pad, y0 - pad, (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad)
    k = vb[2] / 520.0

    marks = []
    for s in sites:
        x, y = project(s['lon'], s['lat'])
        base = 'planned' if s.get('planned') else ('cand' if s.get('candidate') else 'live')
        for t in times:
            # 뒤 데이터가 없다고 부지가 사라진 게 아니다 — 마지막 확인값을 흐리게 이월한다
            if s.get('planned'):
                seen = [p for p in s['timeline'] if p['t'] == t]
            elif t == '계획':
                seen = [p for p in s['timeline'] if p['t'] != '계획']
            else:
                seen = [p for p in s['timeline'] if p['t'] <= t]
            if not seen:
                continue
            p = seen[-1]
            carried = p['t'] != t
            r = max(3.0, (p['mw'] ** .5) / 9.0) * k
            lab = '%s · %s' % (s['name'], p['label'])
            if carried:
                lab += ' (%s 확인)' % p['t']
            marks.append(
                '<g class="mk %s%s" data-t="%s"><circle cx="%.1f" cy="%.1f" r="%.2f"/>'
                '<text x="%.1f" y="%.1f" font-size="%.1f">%s</text></g>'
                % (base, ' carried' if carried else '', esc(t), x, y, r,
                   x + 5 * k, y - 5 * k, 11 * k, esc(lab)))

    tabs = ''.join('<button class="tb%s" data-t="%s">%s</button>'
                   % (' on' if t == times[-1] else '', esc(t), esc(t)) for t in times)
    lst = ''.join('<li><b>%s</b> <span>%s</span><br>%s</li>'
                  % (esc(s['name']), esc(s['place']), esc(s['note'])) for s in sites)
    for u in ent.get('sites_unplaced') or []:
        lst += ('<li class="np"><b>%s</b> <span>위치 미상</span><br>%s</li>'
                % (esc(u['name']), esc(u['note'])))

    return ('<h2 class="tsec">부지 — 언제 어디서 늘었나</h2>'
            '<p class="axnote">%s</p><div class="tabs">%s</div>'
            '<div class="mapwrap"><svg viewBox="%.1f %.1f %.1f %.1f" role="img" '
            'aria-label="부지와 시점별 발전 용량"><path class="land" d="%s"/>%s</svg></div>'
            '<ul class="sites">%s</ul>'
            '<script>(function(){var w=document.currentScript.parentNode;'
            'function set(t){w.querySelectorAll(".mk").forEach(function(g){'
            'g.classList.toggle("off",g.dataset.t!==t)});'
            'w.querySelectorAll(".tb").forEach(function(b){'
            'b.classList.toggle("on",b.dataset.t===t)})}'
            'w.querySelectorAll(".tb").forEach(function(b){'
            'b.addEventListener("click",function(){set(b.dataset.t)})});set(%s)})();</script>'
            % (esc(ent.get('site_note', '')), tabs, vb[0], vb[1], vb[2], vb[3],
               io.open(WORLD, encoding='utf-8').read().strip(), ''.join(marks), lst,
               json.dumps(times[-1], ensure_ascii=False)))


def build(key):
    spec = json.load(io.open(ENT, encoding='utf-8'))
    ent = spec['entities'][key]
    meta, src, body = load_track(key)
    alias = [x for m in ent.get('members', []) for x in m['alias']]
    sigs = signal_hits(alias)

    # 서술과 지도를 갈라 끼운다 — 지도는 「부지」 절이 나올 자리에 들어간다
    html_body = md_body(body, src)
    mp = site_map(ent)
    if mp:
        anchor = '<h2 class="tsec">무엇이 아직 안 정해졌나</h2>'
        html_body = (html_body.replace(anchor, mp + anchor, 1)
                     if anchor in html_body else html_body + mp)

    sig_html = ''
    if sigs:
        sig_html = ('<h2 class="tsec">그 뒤로 들어온 신호</h2>'
                    '<p class="axnote">위 서술은 리포트 원문에서 왔습니다. 아래는 그보다 뒤에 올라온 '
                    'LinkedIn·YouTube 한 줄로, 아직 리포트로 정리되지 않은 것입니다.</p>'
                    '<ul class="sigs">%s</ul>'
                    % ''.join('<li><span>%s</span><a href="%s" target="_blank" rel="noopener">%s</a></li>'
                              % (esc(s['date'][5:]), esc(s['url']), esc(s['text'])) for s in sigs))

    srcs = ''.join('<li><a href="%s" target="_blank" rel="noopener">%s</a>'
                   '<span>%s · %s</span></li>'
                   % (BLOB + urllib.parse.quote(s['file'].replace('\\', '/')),
                      esc(s['base'][:70]), esc(s.get('date', '')), esc(s.get('note', '')))
                   for s in src)

    html = (TMPL.replace('__CSS__', style.BASE + CSS)
                .replace('__TITLE__', esc(ent['title']))
                .replace('__EMOJI__', ent.get('emoji', '📌'))
                .replace('__LEDE__', esc(ent['lede']))
                .replace('__STAMP__', '%s 기준 · 원문 %d편에서 직접 서술'
                         % (esc(meta.get('as_of', TODAY.isoformat())), len(src)))
                .replace('__BODY__', html_body)
                .replace('__SIGS__', sig_html)
                .replace('__SRCS__', srcs))
    out = os.path.join(ROOT, '대시보드', '추적 - %s.html' % ent['title'])
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: %s — 원문 %d편 / 출처 표기 %d / 신호 %d -> %s'
          % (ent['title'], len(src), html.count('class="cite"'), len(sigs), out))


CSS = r'''
  .tsec{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:40px 0 10px;
        padding-top:22px;border-top:1px solid var(--line)}
  .tsec:first-of-type{border-top:0;padding-top:0}
  .body p{font-size:var(--t-lead);line-height:1.78;color:var(--ink);margin:0 0 15px;max-width:70ch}
  .body p b{font-weight:750}
  /* 첫 절은 이것만 읽어도 되게 — 나머지는 그 근거다 */
  .body .tsec:first-of-type + p{background:var(--soft);border-left:3px solid var(--accent);
        border-radius:0 var(--r) var(--r) 0;padding:16px 20px;font-size:var(--t-lead);max-width:none}
  .cite{font-size:.72em;font-weight:800;color:var(--accent);text-decoration:none;
        vertical-align:.28em;margin-left:2px;padding:0 3px;border-radius:4px;background:var(--sunk)}
  .cite:hover{background:var(--soft)}
  .tabs{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
  .tb{font:inherit;font-size:var(--t-meta);font-weight:800;cursor:pointer;padding:7px 14px;
      min-height:36px;border-radius:999px;border:1px solid var(--line);background:var(--card);
      color:var(--sub);-webkit-tap-highlight-color:transparent}
  .tb:hover{border-color:var(--accent);color:var(--accent)}
  .tb.on{background:var(--accent);border-color:var(--accent);color:#fff}
  .mapwrap{border:1px solid var(--line);border-radius:var(--r);overflow:hidden;background:var(--sunk)}
  .mapwrap svg{display:block;width:100%;height:auto}
  .land{fill:var(--card);stroke:var(--line);stroke-width:.4}
  .mk circle{fill:var(--accent);fill-opacity:.35;stroke:var(--accent);stroke-width:1.2}
  .mk text{fill:var(--ink);font-weight:700;paint-order:stroke;stroke:var(--bg);
           stroke-width:2.4px;stroke-linejoin:round}
  .mk.cand circle{fill-opacity:.10;stroke-dasharray:3 2}
  .mk.planned circle{fill:#c98a2e;stroke:#c98a2e;fill-opacity:.18;stroke-dasharray:4 3}
  .mk.carried circle{fill-opacity:.12;stroke-dasharray:2 3}
  .mk.carried text{opacity:.6}
  .mk.off{display:none}
  .sites{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:9px;
         grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
  .sites li{font-size:var(--t-meta);color:var(--sub);line-height:1.55;background:var(--card);
            border:1px solid var(--line);border-radius:10px;padding:10px 13px}
  .sites li b{color:var(--ink);font-size:var(--t-body)}
  .sites li span{color:var(--faint);font-size:var(--t-lbl)}
  .sites li.np{border-style:dashed}
  .sigs,.srcs{list-style:none;margin:0;padding:0}
  .sigs li{display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:baseline;
           padding:9px 0;border-top:1px solid var(--line)}
  .sigs li span{font-size:var(--t-lbl);color:var(--faint);font-variant-numeric:tabular-nums}
  .sigs li a{font-size:var(--t-body);color:var(--ink);text-decoration:none;line-height:1.55}
  .sigs li a:hover{color:var(--accent)}
  .srcs li{padding:9px 0;border-top:1px solid var(--line)}
  .srcs li a{font-size:var(--t-body);color:var(--accent);font-weight:700;text-decoration:none}
  .srcs li span{display:block;font-size:var(--t-lbl);color:var(--faint);margin-top:2px}
  @media (max-width:640px){
    .sites{grid-template-columns:1fr}
    .body p{font-size:var(--t-body);line-height:1.75}
  }
'''

TMPL = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>추적 — __TITLE__</title>
<style>__CSS__</style>
<div class="wrap">
<header>
  <p class="eyebrow">__EMOJI__ 추적</p>
  <h1>__TITLE__</h1>
  <p class="lede">__LEDE__</p>
  <div class="meta"><span>__STAMP__</span>
    <a class="maplink" href="Yomianalysis.html">전체 입구 →</a></div>
</header>
<div class="body">__BODY__</div>
__SIGS__
<h2 class="tsec">읽은 원문</h2>
<p class="axnote">본문은 아래 문서를 통째로 읽고 쓴 것입니다. 문장 뒤의 파란 줄번호를 누르면
그 문장의 근거가 된 원문 줄로 갑니다.</p>
<ul class="srcs">__SRCS__</ul>
<footer>추적 대상은 <code>insights/views/entities.json</code>, 본문은
<code>insights/tracks/&lt;키&gt;.md</code>입니다.
재생성 <code>py insights/gen_entity_board.py musk</code>.
종목 추천이 아니며 가격·밸류에이션·타이밍은 이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'musk')
