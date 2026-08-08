# 추적판 — 「얘네가 지금 뭘 하고 있나」를 한 화면에.
#
# 사건 목록이 아니라 상태판이다. 그 차이가 이 파일의 설계 전부다:
#   · 주체별 카드가 맨 위다. 묶음을 뭉개면 "스페이스X는 나가는데 xAI는 조용하다"가 안 보인다
#   · 모든 카드에 「마지막 확인 + 며칠 지났나」를 박는다. 코퍼스에 없으면 없다고 쓴다
#   · 근거는 세 층(원자 / 문서 언급 / 신호)으로 갈라 배지를 단다. 섞으면 어느 주장이
#     1차 리포트에서 나왔는지 추적이 끊긴다(check_atoms C18과 같은 이유)
#
# 대상은 views/entities.json에 적힌 것만. 명단에 없으면 페이지도 없다.
import os, io, re, sys, json, glob, datetime, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca
import style

ROOT = ca.ROOT
ENT = os.path.join(ROOT, 'insights', 'views', 'entities.json')
HIST = os.path.join(ROOT, '대시보드', '소셜 신호 히스토리.html')
NEWS = os.path.join(ROOT, 'content', 'newsletter')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'
TODAY = datetime.date.today()

LANE_ORDER = ['power', 'build', 'model', 'deal']


def esc(s):
    return (str(s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def days_since(d):
    try:
        y, m, dd = (int(x) for x in d.split('-'))
        return (TODAY - datetime.date(y, m, dd)).days
    except Exception:
        return None


def stale_class(n):
    """오래될수록 죽인다 — 낡은 값을 최신인 것처럼 보이게 두지 않는다."""
    if n is None:
        return 'gone'
    return 'fresh' if n <= 14 else ('warm' if n <= 60 else 'cold')


def ago(n):
    if n is None:
        return '확인된 적 없음'
    return '오늘' if n == 0 else ('어제' if n == 1 else '%d일 전' % n)


# ── 층 1: 원자 ────────────────────────────────────────────────────────
def atom_hits(atoms, alias):
    """actor 배열에 있거나 본문에 별칭이 나오면 이 묶음의 것으로 본다.
    본문 매칭은 오탐이 섞인다 — 그래서 페이지에 그렇게 적어 둔다."""
    out = []
    for a in atoms:
        blob = (a.get('claim') or '') + (a.get('line_text') or '') + str(a.get('condition') or '')
        acts = a['view'].get('actor') or []
        if any(x in acts for x in alias) or any(x in blob for x in alias):
            out.append(a)
    return out


# ── 층 2: 문서 언급 ───────────────────────────────────────────────────
# 문서에서 걷어내야 하는 줄 — 목차 앵커, mermaid 노드, 표. 이름은 나오지만
# 읽을 문장이 아니다. 안 거르면 한 문서가 목차만으로 스무 줄을 차지한다
JUNK = re.compile(r'\]\(#|-->|--\||\["|\{\{|^\s*\||^\s*:?-{3,}')
PER_DOC = 6   # 한 문서가 판을 독점하지 못하게. 긴 줄이 대개 더 알맹이가 있다


def doc_hits(alias, atom_lines):
    """변환 문서의 문단 중 별칭이 나온 것. 이미 원자가 덮은 줄은 뺀다 —
    같은 이야기가 층을 옮겨 다니며 세 번 나오면 판이 부풀기만 한다."""
    out = []
    for p in glob.glob(os.path.join(NEWS, '**', '*.md'), recursive=True):
        rel = os.path.relpath(p, ROOT).replace('\\', '/')
        base = os.path.basename(p)
        m = re.match(r'\[(\d{6})\]', base)
        if not m:
            continue
        date = '20%s-%s-%s' % (m.group(1)[:2], m.group(1)[2:4], m.group(1)[4:])
        lines = io.open(p, encoding='utf-8').read().split('\n')
        got = []
        for i, ln in enumerate(lines, 1):
            t = ln.strip()
            if len(t) < 40 or t.startswith('#') or JUNK.search(t):
                continue
            if not any(x in t for x in alias):
                continue
            if (rel, i) in atom_lines:
                continue
            got.append({'date': date, 'text': re.sub(r'[*`>]', '', t).strip()[:300],
                        'doc': base, 'url': BLOB + urllib.parse.quote(rel) + '#L%d' % i})
        got.sort(key=lambda d: -len(d['text']))
        out += got[:PER_DOC]
    return out


# ── 층 3: 신호 ────────────────────────────────────────────────────────
def signal_hits(alias):
    """소셜 신호 히스토리에서 별칭이 나온 행. 근거로는 가장 가볍지만
    원자 층이 비어 있는 구간(xAI가 그렇다)에서 유일한 최신성이다."""
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
        for row in re.findall(r'<div class="row">.*?</div>\s*(?=<div class="row">|<div class="day">|$)',
                              chunk, re.S):
            sn = re.search(r'<span class="sn">(.*?)</span>', row, re.S)
            href = re.search(r'href="([^"]+)"', row)
            if not sn:
                continue
            txt = re.sub(r'<[^>]+>', '', sn.group(1)).strip()
            if not any(x in txt for x in alias):
                continue
            out.append({'date': date, 'text': txt, 'url': href.group(1) if href else ''})
    return out


def lane_of(text, hint):
    """갈래는 낱말로 가른다. 안 걸리면 사업·계약으로 — 버리지는 않는다."""
    best, score = 'deal', 0
    for lane in LANE_ORDER:
        n = sum(1 for w in hint.get(lane, []) if w in text)
        if n > score:
            best, score = lane, n
    return best


def build(key):
    spec = json.load(io.open(ENT, encoding='utf-8'))
    ent = spec['entities'][key]
    lane_def = spec['lane_def']
    atoms = ca.load_atoms()
    by_id = {a['id']: a for a in atoms}
    man = {s['id']: s for s in json.load(io.open(ca.MAN, encoding='utf-8'))['sources']}
    hint = ent.get('lane_hint', {})

    all_alias = [x for m in ent['members'] for x in m['alias']]
    mine = atom_hits(atoms, all_alias)
    atom_lines = {(a['_path'].replace('\\', '/'), a.get('line')) for a in mine}
    docs = doc_hits(all_alias, atom_lines)
    sigs = signal_hits(all_alias)

    # ── 주체 카드 ─────────────────────────────────────────────────
    cards = []
    for mem in ent['members']:
        hit = atom_hits(atoms, mem['alias'])
        sg = [s for s in sigs if any(x in s['text'] for x in mem['alias'])]
        # 신선도는 가장 무거운 층(원자)으로 매긴다. 신호가 최근이라고 초록으로
        # 칠하면 "검증된 게 최근"이라는 착시가 생긴다 — xAI가 정확히 그 경우다
        a_last = max((a['view']['time'] for a in hit), default=None)
        s_last = max((s['date'] for s in sg), default=None)
        n = days_since(a_last) if a_last else None
        cls = stale_class(n)
        last = ('원자 %s · %s' % (a_last, ago(n))) if a_last else '원자 없음'
        if s_last:
            last += ' / 신호 %s' % s_last

        bar = ''
        pr = mem.get('progress')
        if pr:
            pct = max(4, min(100, int(round(100.0 * pr['done'] / pr['goal']))))
            bar = ('<div class="prog"><div class="bar"><i style="width:%d%%"></i></div>'
                   '<span>%s</span></div>' % (pct, esc(pr['note'])))

        facts = ''.join(
            '<div class="ft"><span>%s</span><b>%s</b>%s</div>'
            % (esc(f['label']), esc(f['value']),
               ('<i class="aid">%s</i>' % esc(f['atom'])) if f.get('atom') in by_id else
               '<i class="aid bad">원자 없음</i>')
            for f in mem.get('facts', []))
        if not facts:
            facts = '<div class="ft none">이 묶음에 대해 코퍼스가 말한 값이 없다</div>'

        gap = ''
        if hit and sg and days_since(max(a['view']['time'] for a in hit)) > 90:
            gap = ('<p class="gapnote">⚠ 원자 층이 %s에서 멈췄다. 아래 근거는 신호 층이다</p>'
                   % max(a['view']['time'] for a in hit))

        cards.append(
            '<section class="mc %s"><div class="mch"><h3>%s</h3>'
            '<span class="last">%s</span></div>'
            '<p class="one">%s</p>%s%s%s'
            '<p class="cnt">원자 %d · 신호 %d</p></section>'
            % (cls, esc(mem['name']), esc(last),
               esc(mem['one']), bar, facts, gap, len(hit), len(sg)))

    # ── 갈래별 근거 ───────────────────────────────────────────────
    rows = []
    for a in mine:
        src = man.get(a['_source_id'], {})
        doc = os.path.basename(src.get('path', a['_path']))
        rows.append({'layer': 'atom', 'date': a['view']['time'],
                     'text': a.get('claim'), 'sub': a.get('condition'),
                     'id': a['id'], 'doc': doc,
                     'url': BLOB + urllib.parse.quote(a['_path'].replace('\\', '/')) +
                            '#L%d' % (a.get('line') or 1),
                     'lane': lane_of((a.get('claim') or '') + str(a.get('condition') or ''), hint)})
    for d in docs:
        rows.append({'layer': 'doc', 'date': d['date'], 'text': d['text'], 'sub': None,
                     'id': None, 'doc': d['doc'], 'url': d['url'],
                     'lane': lane_of(d['text'], hint)})
    for s in sigs:
        rows.append({'layer': 'sig', 'date': s['date'], 'text': s['text'], 'sub': None,
                     'id': None, 'doc': None, 'url': s['url'],
                     'lane': lane_of(s['text'], hint)})
    rank = {'atom': 0, 'doc': 1, 'sig': 2}
    rows.sort(key=lambda r: (r['date'], -rank[r['layer']]), reverse=True)

    LAB = {'atom': '원자', 'doc': '문서', 'sig': '신호'}

    def row_html(r, open_=False):
        meta = []
        if r['id']:
            meta.append('<i class="aid">%s</i>' % esc(r['id']))
        if r['doc']:
            meta.append(esc(r['doc'][:44]))
        return ('<a class="ev %s%s" href="%s" target="_blank" rel="noopener">'
                '<span class="lay">%s</span><span class="dt">%s</span>'
                '<span class="tx">%s</span>%s%s</a>'
                % (r['layer'], ' hi' if open_ else '', esc(r['url']), LAB[r['layer']],
                   esc(r['date'][5:]), esc(r['text']),
                   ('<span class="cond">%s</span>' % esc(r['sub'])) if r['sub'] else '',
                   ('<span class="mt">%s</span>' % ' · '.join(meta)) if meta else ''))

    lanes = []
    for lane in LANE_ORDER:
        rs = [r for r in rows if r['lane'] == lane]
        if not rs:
            continue
        head, rest = rs[:3], rs[3:]
        more = ('<details class="more"><summary>나머지 %d건</summary>%s</details>'
                % (len(rest), ''.join(row_html(r) for r in rest))) if rest else ''
        lanes.append('<section class="lane"><h3>%s<span>%d건</span></h3>%s%s</section>'
                     % (esc(lane_def[lane]), len(rs),
                        ''.join(row_html(r, True) for r in head), more))

    # ── 아직 확인 안 된 것 ────────────────────────────────────────
    unk = []
    for a in mine:
        c = str(a.get('condition') or '')
        if any(w in c for w in ('추정', '확정되지 않', '미확정', '가정')):
            unk.append('<li>%s <i class="aid">%s</i><br><span>%s</span></li>'
                       % (esc(a.get('claim')[:120]), esc(a['id']), esc(c[:140])))
    unk_html = ('<ul class="unk">%s</ul>' % ''.join(unk[:8])) if unk else \
               '<p class="axnote">추정으로 표시된 원자가 없다.</p>'

    html = (TMPL.replace('__CSS__', style.BASE + CSS)
                .replace('__TITLE__', esc(ent['title']))
                .replace('__EMOJI__', ent.get('emoji', '📌'))
                .replace('__LEDE__', esc(ent['lede']))
                .replace('__STAMP__', '%s 기준 · 원자 %d · 문서 언급 %d · 신호 %d'
                         % (TODAY.isoformat(), len(mine), len(docs), len(sigs)))
                .replace('__CARDS__', ''.join(cards))
                .replace('__LANES__', ''.join(lanes))
                .replace('__UNK__', unk_html))
    out = os.path.join(ROOT, '대시보드', '추적 - %s.html' % ent['title'])
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: %s — 원자 %d / 문서 %d / 신호 %d -> %s'
          % (ent['title'], len(mine), len(docs), len(sigs), out))


CSS = r'''
  .mcs{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));margin:20px 0 0}
  .mc{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
      border-radius:var(--r);padding:14px 16px;box-shadow:var(--shadow)}
  .mc.warm{border-left-color:#c98a2e}
  .mc.cold,.mc.gone{border-left-color:var(--line)}
  .mc.cold .one,.mc.gone .one{color:var(--faint)}
  .mch{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
  .mch h3{font-size:var(--t-lead);font-weight:850;letter-spacing:-.01em;margin:0}
  .last{font-size:var(--t-lbl);font-weight:800;color:var(--faint);white-space:nowrap;
        font-variant-numeric:tabular-nums}
  .mc.fresh .last{color:var(--accent)}
  .one{font-size:var(--t-body);color:var(--sub);margin:6px 0 0;line-height:1.55}
  .prog{margin:10px 0 2px}
  .bar{height:7px;border-radius:4px;background:var(--sunk);overflow:hidden}
  .bar i{display:block;height:100%;background:var(--accent);border-radius:4px}
  .prog span{display:block;font-size:var(--t-lbl);color:var(--faint);margin-top:4px}
  .ft{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;font-size:var(--t-meta);
      padding:6px 0;border-top:1px solid var(--line);margin-top:8px}
  .ft:first-of-type{margin-top:10px}
  .ft>span{color:var(--faint);flex:0 0 auto}
  .ft>b{color:var(--ink);font-weight:700}
  .ft.none{color:var(--faint);border-top:1px solid var(--line)}
  .aid{font-style:normal;font-size:var(--t-lbl);font-weight:800;color:var(--accent);
       font-variant-numeric:tabular-nums}
  .aid.bad{color:#a3372f}
  .gapnote{font-size:var(--t-lbl);color:#9a5b12;background:#f6ecda;border-radius:7px;
           padding:7px 10px;margin:9px 0 0;line-height:1.5}
  @media (prefers-color-scheme:dark){.gapnote{background:#2a2113;color:#d79a4e}}
  .cnt{font-size:var(--t-lbl);color:var(--faint);margin:9px 0 0;font-variant-numeric:tabular-nums}
  .lane{margin:26px 0 0}
  .lane h3{font-size:var(--t-body);font-weight:800;color:var(--sub);margin:0 0 8px;
           display:flex;align-items:baseline;gap:8px}
  .lane h3 span{font-size:var(--t-lbl);font-weight:800;color:var(--faint)}
  .ev{display:grid;grid-template-columns:auto auto 1fr;gap:3px 9px;align-items:baseline;
      text-decoration:none;color:inherit;padding:9px 11px;border-radius:9px;
      border:1px solid transparent}
  .ev:hover{background:var(--sunk)}
  .ev.hi{background:var(--card);border-color:var(--line);margin-bottom:6px}
  .lay{font-size:var(--t-lbl);font-weight:800;padding:2px 7px;border-radius:999px;
       background:var(--sunk);color:var(--faint)}
  .ev.atom .lay{background:var(--soft);color:var(--accent2)}
  .dt{font-size:var(--t-lbl);color:var(--faint);font-variant-numeric:tabular-nums}
  .tx{font-size:var(--t-body);color:var(--ink);line-height:1.55}
  .cond,.mt{grid-column:3;font-size:var(--t-lbl);color:var(--faint);line-height:1.5}
  .ev.sig .tx,.ev.doc .tx{color:var(--sub)}
  .more{margin:4px 0 0}
  .more>summary{cursor:pointer;font-size:var(--t-meta);color:var(--accent);
                list-style:none;padding:7px 11px}
  .more>summary::-webkit-details-marker{display:none}
  .more>summary::before{content:"▸ "}
  .more[open]>summary::before{content:"▾ "}
  .unk{margin:0;padding-left:17px}
  .unk li{font-size:var(--t-body);color:var(--ink);margin-bottom:9px;line-height:1.55}
  .unk li span{font-size:var(--t-lbl);color:var(--faint)}
  @media (max-width:640px){
    .mcs{grid-template-columns:1fr}
    .ev{grid-template-columns:auto 1fr;padding:11px}
    .tx,.cond,.mt{grid-column:1/-1}
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

<h3 class="sec">지금 어디쯤인가</h3>
<p class="axnote">「최신」은 이 코퍼스가 마지막으로 그 이름을 말한 날입니다. 그 뒤로 조용한 것이지
아무 일이 없었던 것은 아닙니다 — 리포트가 안 다뤘다는 뜻입니다.</p>
<div class="mcs">__CARDS__</div>

<h3 class="sec">근거 — 갈래별</h3>
<p class="axnote"><b>원자</b>는 조건과 원문 줄이 붙은 검증된 사실, <b>문서</b>는 변환 문서의 문단,
<b>신호</b>는 LinkedIn·YouTube 한 줄입니다. 아래로 갈수록 가볍습니다.
문서·신호 층은 이름만 스쳐 지나간 것이 섞일 수 있습니다.</p>
__LANES__

<h3 class="sec">아직 확인 안 된 것</h3>
__UNK__

<footer>추적 대상은 <code>insights/views/entities.json</code>에 적힌 것만 생깁니다.
재생성 <code>py insights/gen_entity_board.py musk</code>.
종목 추천이 아니며 가격·밸류에이션·타이밍은 이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'musk')
