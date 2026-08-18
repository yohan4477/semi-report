# 🧩 통합 인사이트 — 노트를 통째로 읽고 교차에서 나온 판단만 싣는다.
# 카드를 모아 두는 페이지가 아니라, 문서 여러 편을 가로질러야 보이는 것만 남긴다.
# 문장 옆 줄번호를 누르면 근거가 된 원문 그 줄로 간다.
import io, os, re, sys, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths, style
import notes_lib as nl
sys.path.insert(0, os.path.join(paths.ROOT, 'scripts'))
import ui_bits  # noqa: E402

OUT = os.path.join(paths.ROOT, '대시보드', '통합 인사이트.html')


# 주제 여섯을 한 줄로 세우면 "사업 · 재무"가 원유·환율과 같은 급으로 보인다.
# 실제로는 앞의 넷이 다 AI 이야기고(칩·전력·모델·그 돈), 뒤의 둘만 AI 밖이다.
# 그래서 큰 묶음을 한 겹 위에 둔다 — 주제 id는 그대로라 노트는 안 고친다.
GROUPS = (# 수혜 기업은 주제가 아니라 가로지르는 물음이다("그래서 누가 받나"). AI 판 안에 두면
          # 칩·전력·시장 타일과 같은 급으로 읽혀 묻힌다. 그래서 층을 따로 세우고
          # 「전체 보기」보다 위에 놓는다(sectiles 참조).
          # 묶음 이름은 섹션 제목과 달라야 한다 — 같으면 카드 머리에 같은 말이 두 번 찍힌다
          ('winner', '가로지르는 물음', '갈래를 가로질러 — 지금 나온 숫자로 누가 돈을 벌고 누가 밀리나'),
          ('ai', 'AI 판', 'AI를 만들고 파는 쪽 — 칩부터 그 돈까지'),
          ('macro', 'AI 밖', 'AI 판을 흔드는 바깥 조건 — 기름값과 돈값'),
          # 부동산은 「AI 밖」에 넣으면 원유·환율 카드와 같은 급으로 읽힌다.
          # 코퍼스가 22편으로 따로 서 있고 안에서 갈래가 셋이라 묶음을 따로 낸다.
          ('estate', '부동산', '집을 짓고 사고 파는 쪽 — 공급부터 세금까지'))

# (id, 큰 묶음, 이름, 설명)
SECTIONS = (('winner', 'winner', '수혜 기업과 위기에 빠진 기업', '지금 나온 숫자로 누가 돈을 벌고 누가 밀리나'),
            ('chip', 'ai', '반도체 · 메모리 · 가속기', '메모리 수급, GPU 경쟁, 직접 설계한 칩'),
            ('power', 'ai', '전력 · 데이터센터', '전력망 제약과 자가발전, 랙 밀도와 냉각'),
            ('model', 'ai', '모델 · 학습', '강화학습과 환경 제작, 모델 구조'),
            # 옛 이름 "사업 · 비용 · 재무"는 아래 "시장 · 자금"과 구별이 안 됐다.
            # 여기는 AI를 파는 회사들의 손익이고, 저기는 금리·환율이다.
            ('biz', 'ai', 'AI 사업 · 수익', '토큰 값과 마진, AI로 누가 얼마를 버나'),
            # 아래 둘은 제3자 코퍼스가 들어오며 생겼다. 위 넷에 억지로 밀어 넣으면
            # 원유·해협·환율 이야기가 칩 이야기와 섞여 어느 것도 안 읽힌다.
            ('energy', 'macro', '에너지 · 원자재', '유가와 해협, LNG 비축, 에너지 안보'),
            ('market', 'macro', '금리 · 환율 · 시장', '돈값과 환율, 수급과 포지션, 값이 매겨지는 방식'),
            # 부동산은 한 칸에 다 넣으니 「공급」과 「세금」과 「재건축」이 섞여
            # 어느 것도 안 읽혔다. 갈래 셋으로 나눈다 — 짓는 쪽, 멈추는 쪽, 값 매기는 쪽
            ('estate_supply', 'estate', '공급 · 공사비', '무엇을 짓고 있나, 짓는 값은 왜 올랐나'),
            ('estate_project', 'estate', '정비사업 · 심의', '재건축이 멈추는 자리, 통과 기준이 없는 자리'),
            ('estate_price', 'estate', '값 · 세금 · 땅', '숫자가 갈리는 이유, 만기 뒤 규칙, 공장이 오는 땅'))

ALLSEC = SECTIONS + (('etc', 'macro', '그 밖', ''),)
GRPNAME = dict((g, t) for g, t, _s in GROUPS)

# 부동산 묶음의 글은 공개 페이지에도 그대로 나간다(export 참조). 그 사실을 여기 적어 두지 않으면
# 같은 판단을 두 번 읽거나, 저쪽에서 본 글을 여기서 새 글로 여긴다.
ALSO = {'estate': ('이 묶음의 %d장은 <a href="부동산 대시보드.html">부동산 인사이트</a>에도 '
                   '같은 내용으로 나갑니다. 저쪽에서는 첫 화면 「통합 인사이트」 타일에 들어 있습니다.')}


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


STALE_DAYS = {'biz': 120, 'chip': 180, 'model': 180, 'power': 365, 'winner': 120}


def period(meta, src):
    """근거가 언제 것인지를 카드 겉면에 박는다.

    맞는 말이어도 옛날 이야기면 지금은 틀린 말일 수 있다. 그런데 as_of 는 내가 쓴 날짜라
    글을 안 고치고 두면 그대로 남는다. 그래서 실제로 인용한 원문의 발행일 범위를 쓴다.
    검사기는 insights/check_fresh.py 가 따로 본다.
    """
    # checked: 는 "읽고 안 쓰기로 했다"는 표시다. 근거 범위에 넣으면 안 쓴 문서가
    # 카드를 더 새것으로 보이게 만든다(2026-08-17 확인). 인용한 것만 센다.
    cited = set(re.findall(r'file:\s*"([^"]+)"',
                           meta.get('_head', '').split('\nchecked:')[0]))
    used = [d for d in src if d.get('file') in cited] or src
    ds = sorted(re.findall(r'\[(\d{6})\]', ' '.join(d.get('base', '') for d in used)))
    if not ds:
        return '<span class="asof">as_of %s</span>' % nl.esc(meta.get('as_of', ''))
    fmt = lambda s: '20%s.%s' % (s[:2], s[2:4])
    span = fmt(ds[0]) if ds[0][:4] == ds[-1][:4] else '%s~%s' % (fmt(ds[0]), fmt(ds[-1]))
    newest = datetime.date(2000 + int(ds[-1][:2]), int(ds[-1][2:4]), int(ds[-1][4:6]))
    age = (datetime.date.today() - newest).days
    limit = STALE_DAYS.get(meta.get('section', ''), 180)
    old = ' stale' if age > limit else ''
    tip = '가장 새로운 근거가 %d일 전' % age
    return '<span class="asof%s" title="%s">근거 %s</span>' % (old, tip, nl.esc(span))


def roster(meta):
    """수혜 기업과 위기에 빠진 기업을 제목보다 위에 세운다 — 접힌 상태에서 이름부터 보여야
    「그래서 누가 받나」를 본문 안에서 찾아 읽지 않는다. frontmatter의
    winners·losers에 회사 이름만 적는다(근거는 본문 표가 진다)."""
    w = (meta.get('winners') or '').strip()
    l = (meta.get('losers') or '').strip()
    if not (w or l):
        return ''
    out = []
    if w:
        out.append('<span class="rk rk-w">수혜 기업</span><span class="rv">%s</span>' % nl.esc(w))
    if l:
        out.append('<span class="rk rk-l">위기에 빠진 기업</span><span class="rv">%s</span>' % nl.esc(l))
    return '<p class="rost">%s</p>' % ''.join(out)


def one(meta, body, tab, kind):
    src = nl.sources_of(meta)
    head = meta.get('headline') or ''
    # 두 명단이 제목보다 위다. 이 카드를 여는 이유가 「그래서 누가 받나」라서
    # 회사 이름이 제목보다 먼저 눈에 들어와야 한다(2026-08-18에 올렸다).
    return ('<details class="ins" data-kind="%s"><summary><span class="cid">%s</span>'
            '%s%s<h2 id="%s">%s</h2>'
            '<p class="sub">%s</p></summary><div class="body">%s</div>%s</details>'
            % (tab, nl.esc(kind), period(meta, src), roster(meta),
               anchor(head), nl.esc(head), nl.esc(meta.get('subhead', '')),
               nl.md_body(body, src, 'h4', 'bsec'), srcbox(src)))


TOPSEC = 'winner'   # 타일을 고르기 전에도 보이는 층 — 첫 화면에서 바로 읽힌다


def cards():
    """(필터 대상 카드, 맨 위 고정 카드, 집계들)

    이 페이지는 첫 화면이 주제 고르기라 타일을 누르기 전에는 카드가 전부 hidden이다.
    「수혜 기업」만 그 규칙에서 뺀다 — 누가 돈을 버는지는 클릭 없이 보여야 한다.
    """
    out, top, per, bysec, mix = [], [], {}, {}, {}
    for d, kind, tab in KINDS:
        got = {}
        for p in sorted(glob.glob(os.path.join(d, '*.md')), reverse=True):
            meta, body = nl.parse_front(io.open(p, encoding='utf-8').read())
            meta.setdefault('headline', os.path.basename(p)[:-3])
            sid = meta.get('section', 'etc')
            got.setdefault(sid, []).append(one(meta, body, tab, kind))
            per[tab] = per.get(tab, 0) + 1
            bysec[sid] = bysec.get(sid, 0) + 1
            mix[(tab, sid)] = mix.get((tab, sid), 0) + 1
        if not got:
            continue
        if got.get(TOPSEC):
            top.extend(got[TOPSEC])
        blocks, num = [], 0
        for sid, grp, title, _sub in ALLSEC:
            if not got.get(sid) or sid == TOPSEC:
                continue
            num += 1
            blocks.append('<section class="isec" data-kind="%s" data-sec="%s" data-grp="%s">'
                          '<div class="ihead"><span class="inum">%02d</span>'
                          '<h3>%s</h3><span class="igrp">%s</span>'
                          '<span class="icnt">%d</span></div>%s</section>'
                          % (tab, sid, grp, num, nl.esc(title), nl.esc(GRPNAME[grp]),
                             len(got[sid]), ''.join(got[sid])))
        if blocks:
            out.append('<div class="kgroup" data-kind="%s"><h2 class="ktitle">%s</h2>%s</div>'
                       % (tab, nl.esc(kind), ''.join(blocks)))
    tophtml = ''
    if top:
        title = next((t for s, _g, t, _sub in ALLSEC if s == TOPSEC), TOPSEC)
        sub = next((x for s, _g, _t, x in ALLSEC if s == TOPSEC), '')
        tophtml = ('<section class="topsec"><div class="ihead"><span class="inum">★</span>'
                   '<h3>%s</h3><span class="igrp">%s</span><span class="icnt">%d</span></div>'
                   '%s</section>' % (nl.esc(title), nl.esc(sub), len(top), ''.join(top)))
    return ''.join(out), tophtml, per, bysec, mix


def export(key, by='group'):
    """카드를 다른 대시보드가 그대로 실을 수 있게 조각으로 내준다.

    본문은 insights/synth·briefs의 .md 한 벌뿐이다. 저쪽 생성기에 글을 옮겨 적으면 두 벌이 되고,
    한쪽만 고친 날부터 어느 것이 맞는지 알 수 없게 된다. 그래서 카드 마크업까지 여기서 만든다.
    by='group'이면 큰 묶음 전체, 'section'이면 갈래 하나다.
    """
    secs = [key] if by == 'section' else [s for s, g, _t, _sub in ALLSEC if g == key]
    got = []
    for d, kind, tab in KINDS:
        for p in sorted(glob.glob(os.path.join(d, '*.md'))):
            meta, body = nl.parse_front(io.open(p, encoding='utf-8').read())
            if meta.get('section') not in secs:
                continue
            meta.setdefault('headline', os.path.basename(p)[:-3])
            got.append((meta.get('as_of', ''), one(meta, body, tab, kind)))
    got.sort(key=lambda t: t[0], reverse=True)   # 새 판단이 위로
    return [h for _a, h in got]


def export_sections(gid):
    """묶음 안을 갈래별로 나눠 준다 — (이름, 설명, 카드 HTML 목록).

    한 층에 아홉 장을 그냥 쌓으면 공급·심의·세금이 섞여 어느 것도 안 읽힌다.
    섹션 머리 마크업은 받는 쪽 페이지가 자기 것으로 그린다. 여기는 순서와 내용만 넘긴다.
    """
    out = []
    for sid, grp, title, sub in ALLSEC:
        if grp != gid:
            continue
        got = export(sid, by='section')
        if got:
            out.append((title, sub, got))
    return out


# 다른 페이지에 실을 때 같이 넘기는 CSS.
# 두 페이지는 색 이름이 다르다(--paper·--surface·--ink-2 vs --bg·--card·--sub).
# :root에서 이름을 이어 붙이면 저쪽 기존 규칙의 값까지 바뀐다(.rlrep은 var(--card, var(--surface))를
# 쓴다). 그래서 층 안에서만 잇는다. 카드 쪽 클래스 이름(.ins·.cid·.srcs·.tw)은 저쪽에 없다.
EXPORT_CSS = '''
  #sec-cross{--bg:var(--paper);--card:var(--surface);--sub:var(--ink-2);--faint:var(--ink-3);
        --accent2:var(--accent-ink);--soft:var(--accent-soft);
        --t-lbl:10.5px;--t-meta:12px;--t-body:13.5px;--t-lead:14.5px;--t-h2:19px;
        --r:12px;--pad:16px 20px}
  .xl-lede{margin:10px 0 4px;font-size:12.5px;line-height:1.7;color:var(--ink-2)}
  .xl-lede a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--line)}
  /* 섹션 안의 갈래 — 섹션 머리(.sec-head)보다 한 단 낮게 보여야 층이 안 헷갈린다 */
  .xsec{margin-top:22px}
  .xsec-t{margin:0 0 2px;font-size:12px;font-weight:800;letter-spacing:.06em;
        text-transform:uppercase;color:var(--ink-3)}
'''


GUIDE = ('<div class="guide">'
         '<div class="g-brief"><b>브리핑 %d</b>'
         '<p>한 주제의 지금 상태를 모아 둔 것. 판단하지 않고 나온 숫자와 갈리는 지점만 정리한다.</p></div>'
         '<div class="g-cross"><b>교차 인사이트 %d</b>'
         '<p>문서 여러 편을 가로질러야 보이는 것. 같은 단위가 다른 것을 재거나, 서로 어긋나거나, '
         '아무도 안 다룬 자리를 짚는다.</p></div></div>')


def guide(per):
    return GUIDE % (per.get('brief', 0), per.get('cross', 0))


def sectiles(bysec, bykindsec):
    """주제를 네모 카드로 세운다 — 누르면 그 주제의 글만 펼쳐진다"""
    # 「수혜 기업」은 타일이 아니라 페이지 맨 위 고정 층이다(cards의 TOPSEC 참조).
    # 여기서 세면 타일을 눌러야 나오는 카드 수와 안 맞는다.
    total = sum(n for s, n in bysec.items() if s != TOPSEC)
    tiles = []
    tiles.append('<button class="stile is-all" data-sec="all" aria-pressed="true">'
                 '<span class="st-num">✦</span><span class="st-t">전체 보기</span>'
                 '<span class="st-s">모든 주제를 한 줄로</span>'
                 '<span class="st-n">%d</span></button>' % total)
    num = 0
    for gid, gtitle, gsub in GROUPS:
        if gid == 'winner':      # 위에서 이미 한 층으로 냈다
            continue
        rows = [s for s in ALLSEC if s[1] == gid and bysec.get(s[0])]
        if not rows:
            continue
        # 큰 묶음 이름을 한 줄 띄워 준다 — 이게 없으면 여섯 장이 다 같은 급으로 보인다
        gn = sum(bysec[s[0]] for s in rows)
        tiles.append('<div class="sgrp"><b>%s</b><span>%s</span>'
                     '<span class="sg-n">%d</span></div>'
                     % (nl.esc(gtitle), nl.esc(gsub), gn))
        if gid in ALSO:
            tiles.append('<p class="sg-also">%s</p>' % (ALSO[gid] % gn))
        for sid, _g, title, sub in rows:
            num += 1
            mix = ' · '.join('%s %d' % (k, bykindsec.get((t, sid), 0))
                             for _d, k, t in KINDS if bykindsec.get((t, sid)))
            tiles.append('<button class="stile" data-sec="%s" aria-pressed="false">'
                         '<span class="st-num">%02d</span><span class="st-t">%s</span>'
                         '<span class="st-s">%s</span><span class="st-n">%d</span>'
                         '<span class="st-mix">%s</span></button>'
                         % (sid, num, nl.esc(title), nl.esc(sub), bysec[sid], nl.esc(mix)))
    # 주제를 고르면 타일은 사라지고 카드만 남는다. 돌아올 길이 필요하다.
    back = ('<div class="sback" hidden><button type="button" class="sb-btn">← 주제 다시 고르기</button>'
            '<span class="sb-now"></span></div>')
    return '<div class="sgrid">%s</div>%s' % (''.join(tiles), back)


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
    body, top, per, bysec, mix = cards()
    n = sum(per.values())
    html = (TMPL.replace('__CSS__', style.BASE + KIND_CSS + CARD_CSS + CSS)
                .replace('__GUIDE__', guide(per))
                .replace('__TOP__', top)
                .replace('__TABS__', '<div class="tabbar">%s</div>%s'
                         % (tabs(per), sectiles(bysec, mix)))
                .replace('__CARDS__', body)
                .replace('__N__', str(n))
                .replace('__TABJS__', TAB_JS + ui_bits.TOP_BTN))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %s -> %s' % (' · '.join('%s %d' % (k, per[t]) for _d, k, t in KINDS if per.get(t)), OUT))


# 카드 한 장을 그리는 규칙만 따로 세운다. 부동산 대시보드가 같은 카드를 그대로 싣기 때문이다
# (export 참조). 아래 CSS 쪽 규칙까지 넘기면 .stile·.sgrid 이름이 겹쳐 그쪽 주제 타일을 덮어쓴다.
CARD_CSS = r'''
  .ins{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
       border-radius:var(--r);padding:var(--pad);margin-top:12px;box-shadow:var(--shadow)}
  .ins>summary{list-style:none;cursor:pointer;position:relative;padding-right:26px}
  .ins>summary::-webkit-details-marker{display:none}
  .ins>summary::after{content:"⌄";position:absolute;right:2px;top:-2px;font-size:22px;
                      color:var(--faint);transition:transform .3s cubic-bezier(.32,.72,0,1)}
  .ins[open]>summary::after{transform:rotate(180deg)}
  .cid{font-size:var(--t-lbl);font-weight:800;letter-spacing:.1em;color:var(--accent)}
  .asof{float:right;font-size:var(--t-meta);color:var(--faint);font-variant-numeric:tabular-nums}
  /* 근거가 오래된 카드는 겉면에서 바로 보이게 — 옛날 이야기를 지금 이야기로 읽지 않도록 */
  .asof.stale{color:#b45309;font-weight:600}
  .asof.stale::after{content:' · 오래됨'}
  .ins h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;line-height:1.36;margin:6px 0 2px}
  .ins .sub{font-size:var(--t-body);color:var(--faint);margin:3px 0 0}
  /* 받는 쪽·밀리는 쪽 명단 — 카드를 펴기 전에 회사 이름부터 읽힌다 */
  /* 맨 위 고정 층 — 타일을 고르기 전에도 보인다 */
  .topsec{margin:18px 0 6px;padding:14px 0 4px;border-top:2px solid var(--accent);
        border-bottom:1px solid var(--line)}
  .topsec .ihead .inum{color:var(--accent)}
  .rost{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:8px 0 0;clear:right}
  .rk{flex:none;font-size:var(--t-lbl);font-weight:800;letter-spacing:.04em;
      border-radius:999px;padding:2px 8px}
  .rk-w{color:var(--accent);background:var(--soft)}
  .rk-l{color:var(--faint);background:var(--sunk)}
  .rv{font-size:var(--t-meta);font-weight:700;color:var(--ink);margin-right:6px}
  .bsec{font-size:var(--t-meta);font-weight:800;color:var(--accent2);margin:14px 0 5px;
        text-transform:uppercase;letter-spacing:.04em}
  .body p,.body li{font-size:var(--t-body);color:var(--sub);line-height:1.65}
  .body b{color:var(--ink)}
  .cite{font-size:.72em;font-weight:800;color:var(--accent);text-decoration:none;
        vertical-align:.28em;margin-left:2px;padding:0 3px;border-radius:4px;background:var(--sunk)}
  .srcs{margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
  .srcs>summary{cursor:pointer;font-size:var(--t-meta);font-weight:700;color:var(--sub);
        list-style:none}
  .srcs>summary::-webkit-details-marker{display:none}
  .srcs>summary::before{content:"📄 ";opacity:.7}
  .srcs ul{margin:8px 0 0;padding-left:18px}
  .srcs li{font-size:var(--t-meta);line-height:1.8}
  .srcs a{color:var(--sub);text-decoration:none;border-bottom:1px solid var(--line)}
  .srcs a:hover{color:var(--accent)}

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

  /* 좁은 화면 — 글이 화면 가장자리에 붙으면 읽기 힘들다 */
  @media (max-width:640px){
    .ins{padding:15px 16px;border-radius:10px}
    .body ul{padding-left:17px;margin:6px 0}
    .body li{margin-bottom:7px}
    .body p{margin:6px 0}
    .tw{margin-left:-16px;margin-right:-16px;padding:0 16px}
    .body td:first-child{white-space:normal}
  }
'''

CSS = r'''
  /* 탭은 스크롤해도 따라온다 — 긴 카드 안에서 종류·주제를 다시 고르려고 위로 올라가지 않게 */
  .tabbar{position:sticky;top:0;z-index:5;margin:16px 0 6px;padding:8px 0 6px;
        background:var(--bg);border-bottom:1px solid var(--line)}
  .itabs{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:6px;margin:0;
        padding-bottom:2px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .itabs::-webkit-scrollbar{display:none}
  .itabs button{flex:none}
  .itabs button{font:inherit;font-size:var(--t-meta);font-weight:700;padding:6px 13px;
        border:1px solid var(--line);border-radius:999px;background:transparent;
        color:var(--sub);cursor:pointer}
  .itabs button[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
  .itabs .tn{margin-left:6px;font-variant-numeric:tabular-nums;opacity:.7}
  /* 주제 타일 — 누르면 그 주제의 글만 펼쳐진다 */
  /* 카드 화면에서 주제 고르는 화면으로 돌아가는 줄 — 지금 어느 주제를 보는지도 여기 적는다 */
  .sback{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 2px}
  .sback[hidden]{display:none}
  .sb-btn{font:inherit;font-size:var(--t-meta);cursor:pointer;padding:7px 13px;
          border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink)}
  .sb-btn:hover{border-color:var(--accent);color:var(--accent)}
  .sb-now{font-weight:700}
  .sgrid[hidden]{display:none}
  .sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
        gap:10px;margin:14px 0 4px}
  .stile{position:relative;display:flex;flex-direction:column;gap:2px;text-align:left;
        font:inherit;cursor:pointer;padding:13px 15px 12px;border-radius:var(--r);
        border:1px solid var(--line);background:var(--card);box-shadow:var(--shadow);
        transition:border-color .15s ease,transform .15s ease}
  .stile:hover{border-color:var(--faint);transform:translateY(-1px)}
  .stile[aria-pressed="true"]{border-color:var(--ink);box-shadow:0 0 0 1px var(--ink) inset}
  .st-num{font-size:var(--t-lbl);font-weight:800;letter-spacing:.09em;color:var(--faint);
        font-variant-numeric:tabular-nums}
  .st-t{font-size:var(--t-body);font-weight:800;color:var(--ink);letter-spacing:-.01em}
  .st-s{font-size:var(--t-lbl);color:var(--faint);line-height:1.5}
  .st-n{position:absolute;top:12px;right:14px;font-size:var(--t-meta);font-weight:800;
        color:var(--ink);font-variant-numeric:tabular-nums}
  .st-mix{margin-top:5px;font-size:var(--t-lbl);color:var(--sub)}
  .stile.is-all .st-t{color:var(--accent)}
  /* 가로지르는 층 — 격자 한 줄을 통째로 쓰고 위아래로 선을 그어 주제 타일과 급을 가른다 */
  .stile.is-top{grid-column:1/-1;border-color:var(--accent);border-left-width:3px;
        background:var(--soft, var(--card))}
  .stile.is-top .st-num{color:var(--accent)}
  .stile.is-top .st-t{font-size:var(--t-lead);color:var(--accent)}
  /* 큰 묶음 줄 — 타일 격자를 가로로 끊는다 */
  .sgrp{grid-column:1/-1;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;
        margin:8px 0 -2px;padding-bottom:5px;border-bottom:1px solid var(--line)}
  .sgrp>b{font-size:var(--t-body);font-weight:800;color:var(--ink);letter-spacing:-.01em}
  .sgrp>span{font-size:var(--t-lbl);color:var(--faint)}
  .sg-n{margin-left:auto;font-weight:800;color:var(--faint);font-variant-numeric:tabular-nums}

  /* 좁은 화면 — 페이지 부품 쪽만. 카드 쪽 규칙은 CARD_CSS 안에 같이 있다 */
  @media (max-width:640px){
    .guide{gap:6px}
    .guide div{padding:10px 13px}
    .ihead{gap:7px}
    .tabbar{margin:12px -14px 6px;padding:8px 14px 6px}
    .sgrid{grid-template-columns:1fr 1fr;gap:8px}
    .stile{padding:11px 12px 10px}
    .st-s{display:none}
    .st-mix{margin-top:4px}
  }

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
  /* 주제 이름 옆에 "AI 판 / AI 밖"을 달아 둔다 — 스크롤 도중에도 어느 쪽인지 안다 */
  .igrp{font-size:var(--t-lbl);font-weight:700;color:var(--faint);
        border:1px solid var(--line);border-radius:999px;padding:1px 7px}

  /* 같은 글이 다른 페이지에도 실린다는 표시 — 타일 화면에서 먼저 보이게 묶음 줄에 붙인다 */
  .sg-also{grid-column:1/-1;margin:2px 0 0;font-size:var(--t-lbl);color:var(--faint);
        line-height:1.6}
  .sg-also a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--line)}
  .sg-also a:hover{border-bottom-color:var(--accent)}

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
  var kbar=document.querySelector('.itabs');
  var sbar=document.querySelector('.sgrid');
  var back=document.querySelector('.sback');
  if(!kbar) return;
  // 화면이 둘이다. 주제를 고르는 화면(sec===null)과 그 주제의 카드를 읽는 화면.
  // 한 화면에 타일과 카드를 같이 두면 무엇을 보고 있는지 흐려진다.
  var kind='all', sec=null;
  var names={};
  if(sbar) sbar.querySelectorAll('button').forEach(function(b){
    var t=b.querySelector('.st-t');
    names[b.dataset.sec] = t ? t.textContent : b.dataset.sec;
  });
  function apply(){
    var picking = (sec===null);
    document.querySelectorAll('.isec').forEach(function(s2){
      s2.hidden = picking || !((kind==='all' || s2.dataset.kind===kind) &&
                               (sec==='all'  || s2.dataset.sec===sec));
    });
    document.querySelectorAll('.kgroup').forEach(function(g){
      g.hidden = g.querySelectorAll('.isec:not([hidden])').length===0;
    });
    if(sbar) sbar.hidden = !picking;
    if(back){
      back.hidden = picking;
      var now=back.querySelector('.sb-now');
      if(now) now.textContent = picking ? '' : (names[sec]||'');
    }
    kbar.hidden = picking;
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
    var first=document.querySelector('.isec:not([hidden])');
    if(first) first.scrollIntoView({behavior:'smooth', block:'start'});
  });
  if(back) back.addEventListener('click', function(e){
    if(!e.target.closest('.sb-btn')) return;
    sec=null; kind='all'; apply();
    if(sbar) sbar.scrollIntoView({behavior:'smooth', block:'start'});
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
__TOP__
__TABS__
__CARDS__
__TABJS__
<footer>근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
