# -*- coding: utf-8 -*-
# 포트폴리오 워치 대시보드 생성. 보유 자산이 아니라 **보고 있는 대상**을 세우는 장이다.
# 설계는 docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md.
#
# 워치 줄은 insights/watch/<kind>/*.md 에 있고 여기서는 읽어서 카드로 굽기만 한다.
# 이 파일에 판단을 적지 않는다 — 적으면 같은 글이 두 벌이 되고 한쪽만 고친 날부터
# 어느 것이 맞는지 알 수 없게 된다.
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
sys.path.insert(0, os.path.join(dc.ROOT, 'insights'))
import watch_lib as wl  # noqa: E402
import watch_fig as wf  # noqa: E402
import card_lib as cl  # noqa: E402

OUT = os.path.join(dc.ROOT, '대시보드', '포트폴리오 워치.html')
# 정리일을 손으로 적으면 워치 줄을 고친 날과 어긋난다 — 실제로 하루 벌어져 있었다.
# 줄들이 마지막으로 확인된 날에서 뽑는다.
def _stamp(ws):
    return max([w['checked'] for w in ws if w.get('checked')] or ['—'])

# 부제는 한 줄에 끝나야 한다 — 길면 타일에서 말줄임표로 잘리고, 잘린 자리가 하필
# 「여기는 「무엇을…」이라 읽어도 아무 정보가 없다.
SECS = {
    'realestate': ('sec-area', '01', '권역 — 부동산', '전세냐 매매냐, 깎을 수 있는 장인가'),
    'equity': ('sec-ticker', '02', '종목 — 주식', '무엇이 깨지면 계산을 다시 하나'),
}
LABEL = {'realestate': '부동산 — 권역', 'equity': '주식 — 종목'}
# 관점을 한쪽에만 적으면 라벨 없는 쪽이 기본값처럼 보인다 — 「강남 3구」와
# 「강남 3구 — 집 구하는 사람」이 나란히 서면 앞엣것이 무슨 관점인지 열어 봐야 안다
DEFAULT_VIEW = {'realestate': '투자로 보는 사람', 'equity': '보고만 있는 사람'}

# 트리거 표의 열은 어느 자산군이든 같다 — 어댑터가 자산군마다 값만 다르게 채운다.
# 「언제 것 · 성격」은 CLAUDE.md 가 값에 요구하는 두 열이라 어댑터 계약에 박혀 있다.
TRG_HEAD = ['무엇을', '지금 값', '걸리는 조건', '상태', '언제 것', '성격']
# 사건 줄은 하는 일이 다르다 — 견주는 표가 아니라 사람이 확인할 목록이다.
# 한 표에 섞으면 표가 두 가지 일을 하고, 값 없는 줄이 값 있는 줄 사이에 끼어 읽기를 끊는다
EVT_HEAD = ['무엇을 확인하나', '언제 판단이 바뀌나']

# 상태 딱지 — 걸린 것이 표에서 눈에 띄어야 한다. 「지금 걸렸나」가 이 장의 존재 이유인데
# 지금 값과 조건을 나란히 놓기만 하면 사람이 줄마다 암산으로 부등호를 세운다.
STATE_CSS = {'걸림': 'background:var(--warn,#c2831f);color:#fff',
             '근접': 'border:1px solid var(--warn,#c2831f)'}


def state_tag(st, why):
    style = STATE_CSS.get(st, 'color:var(--ink-3)')
    return ('<span title="%s" style="%s;border-radius:9px;padding:1px 7px;'
            'font-size:.72rem;font-weight:800;white-space:nowrap">%s</span>'
            % (wl.esc(why), style, wl.esc(st)))

# 열쇠 앞머리를 도해 제목으로. 없으면 열쇠를 그대로 쓴다
TITLE = {'sale_idx': '매매가격지수', 'jeonse_idx': '전세가격지수',
         'jeonse_ratio': '전세가율 — 중위 매매가격 대비 전세가격',
         'supply_demand': '매매수급동향 — 100이 균형',
         'median': '서울 중위가격 — 매매와 전세',
         'deal_count': '아파트 매매 거래량 — 가격보다 먼저 움직인다',
         'rent_conv': '전월세 전환율 — 보증금을 월세로 바꿀 때 붙는 비율'}

# 한 판에 겹칠 것. 단위가 같아 나란히 놓을 수 있는 짝이다. 판 위의 벌어짐은 차(差)이지
# 전세가율(比)이 아니다 — 전세가율은 따로 판이 있다. 값은 그 짝이 정한 이름으로 구분한다.
GROUP = {'median_sale': ('median', '매매'), 'median_jeonse': ('median', '전세')}


def title_of(w):
    return '%s — %s' % (w['target'], w.get('view') or DEFAULT_VIEW[w['kind']])


def trg_row(t):
    """트리거 한 줄을 표 행으로. 사건 줄은 어댑터가 안 채우므로 값 자리에 갈래를 적는다 —
    비워 두면 「아직 안 받아 온 값」과 「애초에 값이 아닌 것」이 화면에서 같아 보인다."""
    e = wl.esc
    v = t['value']
    st, why = wl.state_now(t['cond'], t['series'])
    # 단위를 붙인다. 43.05·1308.56 이 맨 숫자로 서면 무엇을 재는 값인지 표에서 안 보인다
    unit = t.get('unit') or ''
    shown = '—' if v is None else e(v) + (' <span class="t-axis">%s</span>' % e(unit)
                                          if unit and unit not in ('배',) else '')
    return [e(t['what']), shown, e(t['cond']), state_tag(st, why),
            e(t['as_of'] or '—'), e(t['nature'] or '자리표시')]


def figs_of(w):
    """트렌드 도해. 어댑터가 받은 metric 중 series 가 든 것만 그린다 — 어댑터가 붙기
    전에는 아무것도 안 선다(insight-figure 규칙 1을 배선으로 지킨다).

    트리거가 아니라 metric 전부를 본다. 전세지수처럼 트리거는 아니고 맥락으로만
    같이 보는 값이 있어서다.

    같은 단위끼리만 한 판에 둔다. 매매지수와 전세지수를 겹치면 세로 자 하나에 뜻이
    다른 두 값이 서서 어느 쪽이 움직인 건지 안 보인다. 열쇠 앞머리가 묶는 열쇠다 —
    sale_idx_강남구 · sale_idx_서초구 는 한 판, jeonse_idx_* 는 다른 판."""
    groups = {}
    for key, m in sorted((w.get('metrics') or {}).items()):
        if not m.get('series'):
            continue
        # 열쇠를 밑줄로 쪼개 어림하지 않는다 — supply_demand 처럼 밑줄이 든 이름에서
        # 깨진다. 어댑터가 실어 보낸 area 를 떼어 내 묶음 열쇠를 만든다.
        area = m.get('area') or ''
        base = key[:-(len(area) + 1)] if area and key.endswith('_' + area) else key
        # 겹칠 짝이면 판 열쇠를 바꾸고 선 이름도 그 짝이 정한 것으로 쓴다
        gkey, gname = GROUP.get(base, (base, area or base))
        groups.setdefault((gkey, m.get('unit') or ''), []).append((gname, m))
    out = []
    for (base, unit), items in groups.items():
        # 한 판에 표 둘이 겹치면 출처도 둘이다. 하나만 달면 매매 선이 그려진 판에
        # 전세 통계표 번호가 붙는다 — GROUP 을 넣은 순간 「한 판 한 출처」가 깨졌다
        note = ' · '.join(dict.fromkeys(m.get('src', '') for _n, m in items if m.get('src')))
        svg = wf.trend([(n, [tuple(x) for x in m['series']]) for n, m in items[:3]],
                       unit or '값', note=note)
        if svg:
            out.append((0, TITLE.get(base, base), svg, note))
    return out


def card(w):
    return {
        'section': SECS[w['kind']],
        'topic': ('market', w['topic']),
        'title': '%s — %s' % (w['target'], w.get('view') or DEFAULT_VIEW[w['kind']]),
        'gain': w['why'],
        'meta': ([LABEL[w['kind']], '보기 시작 <b>%s</b>' % w['opened']]
                 + ([] if w['opened'] == w['checked']
                    else ['마지막 확인 <b>%s</b>' % w['checked']])),
        # 트리거 표가 맨 위다. 워치리스트에서 먼저 알아야 할 것은 근거가 아니라
        # 「지금 조건에 걸렸나」다(설계 §3).
        'lead_table': ('무엇이 일어나면 판단이 바뀌나 — 값으로 오는 것', TRG_HEAD,
                       [trg_row(t) for t in w['triggers']
                        if t['kind'] == wl.KIND_VALUE]),
        'oneliner': w['judged'],
        'points': w['points'],
        'figs': figs_of(w),
        # 사건은 값으로 안 온다. 사람이 확인할 때만 움직이므로 본문 아래에 목록으로 둔다
        'table': (('값으로 안 오는 것 — 사람이 확인한다', EVT_HEAD,
                   [[wl.esc(t['what']), wl.esc(t['cond'])] for t in w['triggers']
                    if t['kind'] == wl.KIND_EVENT])
                  if any(t['kind'] == wl.KIND_EVENT for t in w['triggers']) else None),
        # 반대 근거는 「무엇이 — 왜」로 적혀 있다. 앞머리를 화자 자리에 넣는다.
        'clash': [tuple(c.split(' — ', 1)) if ' — ' in c else ('', c) for c in w['clash']],
    }


# ── 견주는 층 ────────────────────────────────────────────────────────────
# 집 구하는 사람은 권역 하나를 보는 게 아니라 여럿을 견준다. 카드를 하나씩 열어야
# 견줄 수 있으면 그 일이 안 일어난다 — 타일과 같은 자리에 층으로 세운다.
def fired_block(watches):
    """지금 걸린 조건과 근접한 것만 모아 맨 위에 세운다.

    이게 없으면 매달 카드를 전부 열어 표를 눈으로 재야 한다. 실제로는 안 열게 되고
    넘은 줄을 놓친다 — 설계가 「알리는 길이 없다」로 적어 둔 자리를 화면이 메운다."""
    rows = []
    for w in watches:
        title = title_of(w)
        for t in w['triggers']:
            if t['kind'] != wl.KIND_VALUE:
                continue
            st, why = wl.state_now(t['cond'], t['series'])
            if st in ('걸림', '근접'):
                rows.append((0 if st == '걸림' else 1, title, t, st, why))
    if not rows:
        return ('<p class="xl-lede"><b>지금 걸린 조건이 없습니다.</b> 값 트리거 가운데 '
                '조건에 든 것도, 문턱 가까이 온 것도 없습니다.</p>')
    rows.sort(key=lambda r: (r[0], r[1]))
    n_hit = sum(1 for r in rows if r[0] == 0)
    h = ['<p class="xl-lede"><b>지금 걸린 조건 %d개</b>, 문턱 가까이 온 것 %d개입니다. '
         '아래 표의 이름을 누르면 그 카드로 갑니다.</p>' % (n_hit, len(rows) - n_hit)]
    h.append(cl.tbl_html((
        '지금 걸린 조건 · 가까이 온 조건',
        ['어디', '무엇을', '지금 값', '걸리는 조건', '상태', '얼마나', '언제 것'],
        [['<a href="#%s">%s</a>' % (cl.slug(title), wl.esc(title)),
          wl.esc(t['what']), wl.esc(t['value']), wl.esc(t['cond']),
          state_tag(st, why), wl.esc(why), wl.esc(t['as_of'] or '—')]
         for _o, title, t, st, why in rows])))
    return ''.join(h)


def compare_layer(watches):
    """구 아홉의 전세가율을 한 판에 세우고, 묶음이 실제로 붙어 다니는지를 표로 낸다.

    벌어짐은 **같은 달끼리** 잰다. 값 배열을 순번으로 맞추면 한 구가 한 달 늦게
    공표되는 순간 서로 다른 달을 견주게 되고, 그 수가 그럴듯해서 아무도 못 본다."""
    live = [w for w in watches if w['kind'] == 'realestate'
            and any(k.startswith('jeonse_ratio_') for k in (w['metrics'] or {}))]
    rows, spread, asofs, srcs = [], [], set(), []
    for w in live:
        by = {}
        for k, m in sorted((w['metrics'] or {}).items()):
            if not k.startswith('jeonse_ratio_'):
                continue
            rows.append((w['target'], m['area'], m['value'], m['as_of']))
            asofs.add(m['as_of'])
            if m['src'] not in srcs:
                srcs.append(m['src'])
            by[m['area']] = dict((t, v) for t, v in m['series'])
        if len(by) >= 2:
            # 모든 구가 다 가진 달에서만 잰다
            common = sorted(set.intersection(*[set(d) for d in by.values()]))
            if common:
                gaps = [max(d[t] for d in by.values()) - min(d[t] for d in by.values())
                        for t in common]
                spread.append((w['target'], gaps[-1], sum(gaps) / len(gaps), max(gaps),
                               len(common), common[-1]))
    if not rows:
        return '', 0
    # as_of 가 갈리면 가장 이른 것으로 말한다. 하나만 집어 아홉에 붙이면
    # 늦게 온 구의 지난달 값이 이번 달 값으로 표시된다
    asof = min(asofs)
    mixed = len(asofs) > 1
    src = ' · '.join(srcs)
    svg = wf.rank_bar([(g, n, v) for g, n, v, _a in rows],
                      '전세가율 — 중위 매매가격 대비 중위 전세가격 (%%, %s%s)'
                      % (asof, ' 기준. 구마다 갱신월이 다르다' if mixed else ''), note=src)

    h = [fired_block(watches)]
    h.append('<p class="xl-lede">전세가율은 <b>한 수가 두 방향으로</b> 읽힙니다. 올라가면 '
         '보증금이 집값에 가까워지고, 동시에 「이 돈이면 사는 게 낫다」 쪽으로도 밉니다. '
         '내려가면 매매로 갈아타는 데 드는 자기 돈이 늘었다는 뜻입니다. '
             '권역마다 그 수가 얼마나 다른지를 먼저 봅니다.</p>')
    h.append(cl.fig_html(('구 아홉의 전세가율', svg, src)))
    same = [r for r in rows if r[3] == asof]
    hi, lo = max(same, key=lambda r: r[2]), min(same, key=lambda r: r[2])
    h.append('<p class="xl-lede">%s 기준 가장 높은 <b>%s %s%%</b>와 가장 낮은 '
             '<b>%s %s%%</b>가 <b>%.2f%%포인트</b> 벌어집니다. 같은 서울입니다.</p>'
             % (asof, hi[1], hi[2], lo[1], lo[2], hi[2] - lo[2]))
    # 보는 사람이 견주고 싶은 것은 권역 × (전세가율·협상력·걸린 조건)이다.
    # 「묶음이 옳게 묶였나」는 만든 사람의 물음이라 한 줄로 내린다
    summ = []
    for w in live:
        rs = [m['value'] for k, m in (w['metrics'] or {}).items()
              if k.startswith('jeonse_ratio_')]
        sd = (w['metrics'] or {}).get('supply_demand')
        hits = sum(1 for t in w['triggers']
                   if t['kind'] == wl.KIND_VALUE
                   and wl.state_now(t['cond'], t['series'])[0] in ('걸림', '근접'))
        summ.append([
            '<a href="#%s">%s</a>' % (cl.slug(title_of(w)), wl.esc(w['target'])),
            '%.2f ~ %.2f' % (min(rs), max(rs)) if rs else '—',
            '전세금의 %.1f배' % (100.0 / (sum(rs) / len(rs))) if rs else '—',
            ('%s <span class="t-axis">%s</span>' % (sd['value'], wl.esc(sd['area']))
             if sd else '못 붙임'),
            '%d개' % hits, asof, '공표'])
    if summ:
        h.append(cl.tbl_html((
            '권역마다 지금 어떤가',
            ['권역', '전세가율(구별 범위)', '매매로 넘어가는 문턱', '수급동향',
             '걸림·근접', '언제 것', '성격'],
            sorted(summ, key=lambda r: r[1], reverse=True))))
    if spread:
        tight = min(spread, key=lambda r: r[2])
        h.append('<p class="xl-lede"><b>%s만 묶음으로 성립합니다.</b> 세 구의 벌어짐이 '
                 '평균 %.2f%%포인트인데 나머지는 %s입니다. 시장에서 한 이름으로 부른다고 '
                 '값이 같이 움직이지는 않아서, 이 장은 묶음 평균을 내지 않고 구마다 값을 '
                 '따로 둡니다.</p>'
                 % (tight[0], tight[2],
                    ' · '.join('%s %.2f' % (r[0], r[2]) for r in spread if r[0] != tight[0])))
    h.append('<p class="xl-lede t-axis">전세가율은 공표치이고, 「매매로 넘어가는 문턱」과 '
             '묶음 안 벌어짐은 그 값에서 우리가 셈한 <b>계산치</b>입니다.</p>')
    return ''.join(h), len(rows)



WATCHES = wl.load_all()
CARDS = [card(w) for w in sorted(WATCHES, key=lambda w: SECS[w['kind']][1])]

HEADER = '''  <header>
    <p class="eyebrow">포트폴리오 — 무엇을 왜 보고 있나</p>
    <h1>포트폴리오 워치</h1>
  </header>'''

INTRO_T = ('<p class="lede"><b>보고 있는 곳 %d군데.</b> 권역마다 「왜 보나」와 '
           '「무엇이 일어나면 판단이 바뀌나」를 세웁니다. 값은 한국부동산원 공표 통계이고 '
           '자료 기준은 <b>%s</b>입니다. 손익·비중은 다루지 않습니다.</p>')

LEDE = ('<p class="lede"><b>보유 자산이 아닙니다.</b> 손익·비중·현금흐름은 이 장이 다루지 않습니다. '
        '보고 있는 대상마다 「왜 보나」와 「무엇이 일어나면 판단이 바뀌나」만 세웁니다. '
        '부동산은 <b>권역</b>, 주식은 <b>종목</b>이 한 줄입니다.</p>'
        '<p class="lede">트리거는 갈래가 둘입니다. <b>값</b>은 스크립트가 받아 채우고, '
        '<b>사건</b>은 공표가 날 때 사람이 갱신합니다. 성격이 <b>자리표시</b>인 줄은 '
        '아직 원천이 없어 판단 근거가 아닙니다.</p>')

ASOF = max([m.get('as_of', '') for w in WATCHES for m in (w['metrics'] or {}).values()]
           or ['—'])
INTRO = INTRO_T % (len(CARDS), ASOF)

META = ('''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>보고 있는 것 <b>%d</b></span>
      <span>지켜보는 조건 <b>%d</b></span>
    </div>''' % (_stamp(WATCHES), len(CARDS), sum(len(w['triggers']) for w in WATCHES)))

FOOTER = (LEDE + META + '\n워치 줄은 <code>insights/watch/</code>, 수치는 '
          '<code>insights/watch/_metrics/</code>, 설계는 '
          '<code>docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md</code>, '
          '페이지 생성은 <code>scratchpad/gen_watch_dashboard.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

if __name__ == '__main__':
    top, n = compare_layer(WATCHES)
    dc.render(CARDS, '포트폴리오 워치', HEADER, FOOTER, OUT, page_slug='watch',
              top=top, top_n=0, top_id='sec-compare',
              top_title='권역 견주기', top_sub='구 아홉을 한 판에 놓고 본다',
              intro=INTRO,
              # 이 장은 고르러 오는 곳이 아니라 바뀐 것을 보러 오는 곳이다.
              # 타일은 위에 남아 필터 노릇을 하고, 열면 바로 전체가 보인다
              home='all')
