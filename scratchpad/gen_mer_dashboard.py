# -*- coding: utf-8 -*-
"""메르 대시보드 — 사슬 카드 · 고친 자리 · 주체별 보기.

카드를 손으로 쓰지 않는다. `insights/flows/mer/*.json` 하나가 카드 하나가 되고, 본문은
그 사슬의 마디·화살표에서 뽑는다. 원문 인용 대조를 통과한 값만 들어오므로 없는 값이
화면에 오를 길이 없다.

층 셋
  ① 사슬 카드   접히면 관계 지도, 펼치면 사슬이 어떻게 굴러가는지
  ② 고친 자리   메르가 제 판단을 고치거나(update) 스스로 어긋난(contradict) 대목만 모은다
  ③ 주체별      같은 주체가 6개월 동안 무엇을 했나 — 주제가 아니라 행위자로 자른 축
"""
import io, json, os, sys, glob, collections

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dash_common as dc          # noqa: E402
import mer_flow_lib as fl         # noqa: E402
import mer_flow_svg as fs         # noqa: E402
import mer_map_svg as mm          # noqa: E402
import mer_step as ms             # noqa: E402

OUT = os.path.join(dc.ROOT, '대시보드', '메르 대시보드.html')
BLOG = 'https://blog.naver.com/ranto28/%s'

# 레인마다 섹션 하나. 번호는 dash_common이 다시 매긴다
SEC = {
 'rate': ('sec-rate', '01', '미국 금리 · 재무부',
          '장기금리가 왜 안 잡히나. 재무부가 꺼낸 카드와 그 부작용을 따라간다'),
 'fx': ('sec-fx', '02', '환율 · 물가 · 중앙은행',
        '원화와 엔화를 지키려고 무엇을 했나. 개입의 재원이 어디서 나오는지가 요점이다'),
 'krx': ('sec-krx', '03', '국장 수급 · 제도',
         '누가 사고 누가 파나. 국민연금 리밸런싱과 외국인 매도가 겹치는 자리'),
 'semi': ('sec-semi', '04', '반도체',
          '증설·기술·중국 추격. 값이 아니라 만들 수 있는가로 갈리는 이야기'),
 'ai': ('sec-ai', '05', 'AI · 전력',
        '자본지출을 무엇으로 대나. 순환금융과 전력 병목이 같이 걸린다'),
 'comm': ('sec-comm', '06', '원자재 · 에너지',
          '자원을 쥔 쪽이 그것을 무기로 쓸 때 무엇이 어떻게 번지나'),
 'geo': ('sec-geo', '07', '지정학 · 통상',
         '해협·관세·전쟁이 값으로 바뀌는 경로'),
}

ROLE_KO = {'bg': '배경', 'event': '사건', 'mech': '메커니즘', 'risk': '부작용',
           'watch': '관전포인트', 'verdict': '한줄 코멘트'}
EDGE_KO = {'update': '고쳤다', 'contradict': '어긋난다'}


def threads():
    out = []
    for p in sorted(glob.glob(os.path.join(fl.FLOW, '*.json'))):
        d = json.load(io.open(p, encoding='utf-8'))
        d['_key'] = os.path.basename(p)[:-5]
        out.append(d)
    return out


_JS_DONE = []


def _first():
    """넘기는 층의 JS는 페이지에 한 벌만 나간다."""
    if _JS_DONE:
        return False
    _JS_DONE.append(1)
    return True


def card_of(d, posts, nodes, edges):
    """사슬 하나를 카드 하나로. 본문은 전부 마디에서 뽑는다."""
    key = d['_key']
    mine = [n for n in nodes if n['id'].startswith(key + ':')]
    myed = [e for e in edges if e['from'].startswith(key + ':')]
    lifts = [n for n in mine if n.get('lift')]
    lifts.sort(key=lambda n: (n['date'], n['id']))
    srcs = sorted({n['src'] for n in mine}, key=lambda s: posts[s]['date'])
    m = d.get('map') or {}

    points = []
    for n in lifts[:8]:
        points.append('<b>%s.</b> %s <span class="mc-who">%s · %s</span>'
                      % (n['label'], n.get('detail', ''), n.get('actor', ''),
                         n['date'][5:].replace('-', '/')))
    stats = []
    for n in mine:
        for v in (n.get('nums') or []):
            if ' ' in v:
                head, tail = v.rsplit(' ', 1)
                stats.append((tail, head)) if tail[0].isdigit() else stats.append((v, n['label']))
            else:
                stats.append((v, n['label']))
    seen, uniq = set(), []
    for v, lab in stats:
        if v in seen:
            continue
        seen.add(v)
        uniq.append((v, lab))

    clash = []
    for e in myed:
        if e['kind'] in EDGE_KO:
            a = next((x for x in nodes if x['id'] == e['from']), None)
            b = next((x for x in nodes if x['id'] == e['to']), None)
            if a and b:
                clash.append(('%s → %s' % (a['label'], b['label']),
                              '%s. %s' % (EDGE_KO[e['kind']], e.get('why', ''))))
    q = next((n for n in mine if n['role'] == 'verdict'), mine[0])

    # 세로 스택으로 그린다 — docs/카드 도해 — 그림에서 되읽은 규칙.md 1절
    fig = mm.stack_render(m) if m else ''
    # 여러 편을 관통하는 것은 주체이고, 편마다 바뀌는 것은 그 주체가 한 일이다.
    # 세로를 주체로 가로를 시간으로 두면 한 판에 둘이 같이 보인다.
    span_mo = (int(d['span'][1][:4]) * 12 + int(d['span'][1][5:7])
               - int(d['span'][0][:4]) * 12 - int(d['span'][0][5:7])) + 1
    # 한 편씩 넘겨 보는 층 하나만 선다. 주체가 무엇을 하는 쪽인지는 지도가 쓴
    # 문장을 그대로 줄 머리에 붙인다.
    role = {a: (v.get('desc') or [''])[0] for a, v in (m.get('actors') or {}).items()}
    sts = ms.steps(key, nodes, posts, m)
    deck = ms.render('', sts, role,
                     '%d개월 · 원문 %d편. 넘기면 그 편이 무엇을 더했는지가 뜬다'
                     % (span_mo, len(sts)), 'mtd-' + key, with_js=_first())
    links = [('▶ 원문 %s' % posts[s]['title'][:22], BLOG % s, '' if i == 0 else 'secondary')
             for i, s in enumerate(srcs[:4])]

    return {
        'section': SEC.get(d.get('lane'), SEC['geo']),
        'topic': ('market', d.get('thread', '')[:26]),
        'title': m.get('headline') or d.get('thread', ''),
        'gain': ' '.join(m.get('sub') or [])[:160] or '이 사슬이 어떻게 굴러가는지',
        'meta': ['메르 <b>ranto28</b>', '원문 %d편' % len(srcs),
                 '%s ~ %s' % (d['span'][0], d['span'][1]), '네이버 블로그'],
        'oneliner': ' '.join(m.get('sub') or []) or d.get('thread', ''),
        'points': points,
        'stats': uniq[:6],
        'quote': q.get('quote', ''),
        'clash': clash[:6] or [('이 사슬', '판단을 고친 자리가 없다 — 한 방향으로만 흘렀다')],
        'note': (m.get('notes') or [''])[0],
        'links': links,
        'figs': [(0, '한 편씩 넘겨 본다', deck, '')],
        'date': d['span'][1],
    }


def _narr():
    p = os.path.join(dc.ROOT, 'insights', 'flows', 'mer_narrative.json')
    return json.load(io.open(p, encoding='utf-8'))


def timeline_layer(nodes, posts, narr):
    """① 연표 — 달마다 무슨 일이 있었나. 나열이 아니라 그달의 요지를 먼저 말한다."""
    by = collections.defaultdict(list)
    for n in nodes:
        if n.get('lift') and n['kind'] == 'event':
            by[n['date'][:7]].append(n)
    months = sorted(m for m in by if m in narr['months'])
    out = ['<p class="xl-lede">여섯 달을 가로질러 무슨 일이 있었는지 달마다 모았습니다. '
           '사슬을 따로 읽으면 안 보이는 순서가 여기서 보입니다.</p>']
    n_ev = 0
    for m in months:
        ev = sorted(by[m], key=lambda n: n['date'])[:7]
        n_ev += len(ev)
        rows = ''.join(
            '<li><span class="mt-d">%s</span><span class="mt-a">%s</span>'
            '<span class="mt-l">%s</span>'
            '<a class="mt-s" href="%s">원문</a></li>'
            % (n['date'][5:].replace('-', '/'), esc(n.get('actor', '')), esc(n['label']),
               BLOG % n['src'])
            for n in ev)
        out.append('<div class="mt"><h3 class="mt-m">%s</h3><p class="mt-say">%s</p>'
                   '<ul>%s</ul></div>'
                   % (m.replace('-', '년 ') + '월', esc(narr['months'][m]), rows))
    return ''.join(out), n_ev


def axes_layer(threads_meta, narr):
    """② 구조 — 사슬 열셋이 실제로는 축 셋이다."""
    out = ['<p class="xl-lede">사슬 열셋은 따로 노는 이야기가 아닙니다. '
           '축 셋으로 묶이고, 뒤로 갈수록 앞 축이 정한 금리와 원자재 값에 끌려갑니다.</p>']
    for ax in narr['axes']:
        chips = ''.join(
            '<span class="ax-c">%s <b>%d편</b></span>'
            % (esc(threads_meta[k][0][:22]), threads_meta[k][1])
            for k in ax['threads'] if k in threads_meta)
        out.append('<div class="ax"><h3 class="ax-t">%s</h3><p class="ax-b">%s</p>'
                   '<div class="ax-cs">%s</div></div>'
                   % (esc(ax['title']), esc(ax['body']), chips))
    return ''.join(out), len(narr['axes'])


def entity_layer(nodes, edges, threads_meta, narr):
    """개체 — 주제·기관 하나를 골라 그 흐름과 얽힘을 본다.

    같은 이름이 「중국·중국 상무부·시진핑」처럼 갈라져 있어 별칭을 묶어 센다."""
    by_id = {n['id']: n for n in nodes}
    out = ['<p class="xl-lede">주제나 기관 하나를 골라 <b>언제 무엇을 했고 누구와 얽혔는지</b> 봅니다. '
           '사슬을 가로지르는 개체일수록 이 여섯 달에서 하는 몫이 큽니다.</p>']
    for ent in narr.get('entities', []):
        aka = set(ent['aka'])
        mine = [n for n in nodes if n.get('actor') in aka]
        if not mine:
            continue
        th = sorted({n['id'].split(':')[0] for n in mine})
        # 한 사슬이 타임라인을 다 먹으면 다른 사슬에서 한 일이 안 보인다.
        # 사슬마다 굵은 것(lift) 우선으로 셋까지만 뽑고 날짜순으로 다시 세운다
        per = collections.defaultdict(list)
        for n in sorted(mine, key=lambda n: (not n.get('lift'), n['date'])):
            k = n['id'].split(':')[0]
            if len(per[k]) < 3:
                per[k].append(n)
        mine_tl = sorted([n for v in per.values() for n in v],
                         key=lambda n: (n['date'], n['id']))
        rows = ''.join(
            '<li><span class="en-d">%s</span><span class="en-t">%s</span>'
            '<span class="en-l">%s</span></li>'
            % (n['date'][2:].replace('-', '.'),
               esc(threads_meta.get(n['id'].split(':')[0], ('', 0, ''))[0].split(' — ')[0][:11]),
               esc(n['label']))
            for n in mine_tl[:15])

        ins, outs = [], []
        ids = {n['id'] for n in mine}
        for e in edges:
            a, b = by_id.get(e['from']), by_id.get(e['to'])
            if not a or not b:
                continue
            if e['to'] in ids and a.get('actor') not in aka:
                ins.append((a.get('actor', ''), e.get('why', '')))
            elif e['from'] in ids and b.get('actor') not in aka:
                outs.append((b.get('actor', ''), e.get('why', '')))

        def side(items, kind):
            seen, li = set(), []
            for who, why in items:
                if who in seen or not who:
                    continue
                seen.add(who)
                li.append('<li><b>%s</b> %s</li>' % (esc(who), esc(why[:52])))
                if len(li) >= 4:
                    break
            return ('<div class="en-side"><h4>%s</h4><ul>%s</ul></div>' % (kind, ''.join(li))
                    if li else '')

        out.append(
            '<div class="en"><h3 class="en-n">%s <span>%d사슬 · %d마디</span></h3>'
            '<p class="en-say">%s</p><ul class="en-tl">%s</ul>'
            '<div class="en-sides">%s%s</div></div>'
            % (esc(ent['name']), len(th), len(mine), esc(ent['say']), rows,
               side(ins, '받는 것'), side(outs, '낳는 것')))
    return ''.join(out), len(narr.get('entities', []))


def esc(s):
    import html as _h
    return _h.escape(s or '', quote=True)


CSS = '''
  .mt{border-top:1px solid var(--line);padding:14px 0}
  .mt-m{margin:0 0 4px;font-size:13px;font-weight:850;color:var(--ink-3)}
  .mt-say{margin:0 0 8px;font-size:14.5px;font-weight:700;color:var(--ink);line-height:1.55}
  .mt ul{list-style:none;margin:0;padding:0}
  .mt li{display:flex;gap:10px;align-items:baseline;padding:3px 0;font-size:12.5px;
         color:var(--ink-2);line-height:1.55}
  .mt-d{flex:0 0 44px;color:var(--ink-3);font-weight:700;font-variant-numeric:tabular-nums}
  .mt-a{flex:0 0 116px;color:var(--ink-3);font-weight:700}
  .mt-l{flex:1}
  .mt-s{flex:0 0 auto;font-size:11px;color:var(--ink-3);text-decoration:none}
  .ax{border-top:1px solid var(--line);padding:16px 0}
  .ax-t{margin:0 0 6px;font-size:16px;font-weight:800;color:var(--ink);line-height:1.4}
  .ax-b{margin:0 0 10px;font-size:14px;line-height:1.75;color:var(--ink-2)}
  .ax-cs{display:flex;gap:8px;flex-wrap:wrap}
  .ax-c{font-size:11.5px;color:var(--ink-3);border:1px solid var(--line);border-radius:999px;
        padding:3px 10px}
  .ax-c b{color:var(--ink-2);font-weight:800}
        line-height:1.55}
        font-variant-numeric:tabular-nums}
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .en{border-top:1px solid var(--line);padding:16px 0}
  .en-n{margin:0 0 4px;font-size:15.5px;font-weight:850;color:var(--ink)}
  .en-n span{font-size:11.5px;font-weight:700;color:var(--ink-3);margin-left:8px}
  .en-say{margin:0 0 10px;font-size:14px;line-height:1.7;color:var(--ink-2)}
  .en-tl{list-style:none;margin:0 0 10px;padding:0}
  .en-tl li{display:flex;gap:10px;align-items:baseline;padding:2px 0;font-size:12.5px;
            color:var(--ink-2);line-height:1.55}
  .en-d{flex:0 0 52px;color:var(--ink-3);font-weight:700;font-variant-numeric:tabular-nums}
  .en-t{flex:0 0 96px;color:var(--ink-3);white-space:nowrap;overflow:hidden;
        text-overflow:ellipsis}
  .en-l{flex:1}
  .en-sides{display:flex;gap:22px;flex-wrap:wrap}
  .en-side{flex:1 1 260px}
  .en-side h4{margin:0 0 4px;font-size:11.5px;font-weight:850;color:var(--ink-3)}
  .en-side ul{list-style:none;margin:0;padding:0}
  .en-side li{font-size:12.5px;line-height:1.6;color:var(--ink-2);padding:2px 0}
  .en-side b{color:var(--ink)}
  .mfix{display:flex;gap:14px;padding:12px 0;border-top:1px solid var(--line)}
  .mfix-d{flex:0 0 74px;font-size:12px;font-weight:800;color:var(--ink-3);
          font-variant-numeric:tabular-nums;padding-top:2px}
  .mfix-k{display:inline-block;font-size:10.5px;font-weight:850;color:var(--ink-3);
          border:1px solid var(--line);border-radius:999px;padding:1px 8px;margin-right:6px}
  .mfix-ar{color:var(--ink-3);margin:0 4px}
  .mfix-w{margin:5px 0 0;font-size:13px;line-height:1.6;color:var(--ink-2)}
  .mfix-s{margin:4px 0 0;font-size:11.5px;color:var(--ink-3)}
  .mact{border-top:1px solid var(--line);padding:12px 0}
  .mact-t{margin:0 0 6px;font-size:13.5px;font-weight:850;color:var(--ink)}
  .mact-t span{font-size:11px;font-weight:700;color:var(--ink-3);margin-left:6px}
  .mact ul{list-style:none;margin:0;padding:0}
  .mact li{display:flex;gap:10px;align-items:baseline;padding:3px 0;font-size:12.5px;
           color:var(--ink-2);line-height:1.5}
  .mact-d{flex:0 0 58px;color:var(--ink-3);font-weight:700;font-variant-numeric:tabular-nums}
  .mact-r{margin-left:auto;font-size:10.5px;font-weight:800;color:var(--ink-3)}
  .uc-fig .mermap{border:0;padding:0;background:transparent}
  .mc-who{font-size:11.5px;font-weight:700;color:var(--ink-3);margin-left:4px}
'''

HEADER = '''  <header>
    <p class="eyebrow">메르의 블로그 — 사슬로 읽는 6개월</p>
    <h1>메르 인사이트</h1>
  </header>'''

if __name__ == '__main__':
    posts = fl.load_posts()
    nodes, edges = fl.load_flow()
    bad = fl.check(nodes, edges, posts)
    if bad:
        for w, x in bad[:10]:
            print('FAIL', w, '|', x)
        raise SystemExit('검사 실패 — 고치고 다시 돌린다')

    ts = threads()
    cards = [card_of(d, posts, nodes, edges) for d in ts]
    narr = _narr()
    meta = {d['_key']: (d['thread'], len({n['src'] for n in nodes
                                          if n['id'].startswith(d['_key'] + ':')}), d['span'])
            for d in ts}
    tl_html, n_ev = timeline_layer(nodes, posts, narr)
    ax_html, n_ax = axes_layer(meta, narr)
    en_html, n_en = entity_layer(nodes, edges, meta, narr)

    used = {n['src'] for n in nodes}
    FOOTER = ('<p class="lede">메르의 블로그 글 %d편에서 사슬 %d개를 뽑았습니다. '
              '마디마다 원문 구절을 달아 대조했고, 대조를 통과한 값만 화면에 올렸습니다. '
              '판단은 메르의 것이고 여기서는 그것을 사실과 갈라 표시합니다.</p>'
              '<div class="meta-row"><span>수집 <b>%d편</b></span>'
              '<span>사슬 <b>%d개</b></span><span>마디 <b>%d</b> · 화살표 <b>%d</b></span>'
              '<span>소스 <b>blog.naver.com/ranto28</b></span></div>'
              '\n제3자 해설 요약 아카이브 · 원문은 싣지 않습니다. 투자 추천이 아닙니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_mer_dashboard.py</code>'
              % (len(used), len(ts), len(posts), len(ts), len(nodes), len(edges)))

    dc.render(cards, '메르 인사이트', HEADER, FOOTER, OUT,
              page_slug='mer',
              tops=[('sec-axes', '이 여섯 달의 구조',
                     '사슬 열셋이 실제로는 축 셋이다', n_ax, ax_html),
                    ('sec-time', '연표',
                     '달마다 무슨 일이 있었나 — 사슬을 가로질러', n_ev, tl_html),
                    ('sec-entity', '개체로 보기',
                     '중국·미 재무부·국민연금 — 하나를 골라 그 흐름과 얽힘', n_en, en_html)],
              search_ph='주체나 사슬 이름으로 찾기',
              extra_css=CSS + mm.CSS + fs.CSS + ms.CSS, newest_first=True)
    print('카드 %d · 축 %d · 연표 %d · 개체 %d' % (len(cards), n_ax, n_ev, n_en))
    print(OUT)
