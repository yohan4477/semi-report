# 🧩 통합 인사이트 — 노트를 통째로 읽고 교차에서 나온 판단만 싣는다.
# 카드를 모아 두는 페이지가 아니라, 문서 여러 편을 가로질러야 보이는 것만 남긴다.
# 문장 옆 줄번호를 누르면 근거가 된 원문 그 줄로 간다.
import io, os, re, sys, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths, style
import axes
import sources_rank as sr
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


# (디렉터리, 배지 이름, 탭 id) — 탭은 이 순서로 선다.
# loop 가 맨 앞이다. 여덟 편이 다 서면 나머지 셋은 비고 탭도 사라진다
KINDS = ((paths.LOOP, '고리', 'loop'),
         (paths.BRIEFS, '브리핑', 'brief'),
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


def period(meta, src, body=''):
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
    # 링크드인은 파일명이 [2608]처럼 월 단위라 위에서 안 잡힌다.
    # 인용된 줄이 속한 게시물의 기준일을 대신 센다.
    for ref in nl.cite_refs(body, src):
        if not (ref.get('file') and ref.get('lines')):
            continue
        b = nl.li_basis(ref['file'], ref['lines'][0])
        if b:
            ds.append(b[2:4] + b[5:7] + b[8:10])
    ds = sorted(ds)
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


def copy_btn(aid, cls):
    """이 카드(또는 이 갈래)만 가리키는 주소를 집어 가는 버튼.

    페이지 전체 주소밖에 못 보내던 자리다. 카드는 uc-copy, 갈래는 sec-copy로 갈라 두고
    TAB_JS가 둘을 같이 받는다 — 받은 사람 화면에서 그 갈래를 펴 주는 일까지 거기서 한다."""
    return ('<button type="button" class="%s" data-anchor="%s">링크 복사</button>'
            % (cls, nl.esc(aid)))


def rank_dot(section):
    """근거표 각주 앞에 붙는 등급 표시. 문장 속 인용에는 안 붙인다 — 점으로 덮인다."""
    def dot(f):
        r = sr.rank_of(f, section)
        name, _bysec, _d = sr.source_of(f)
        return ('<span class="rkd rk-%s" title="%s — %s">%s</span>'
                % (sr.SLUG[r], nl.esc(name or '분류 안 된 출처'), r, sr.MARK[r]))
    return dot


RANK_LEGEND = ('<p class="rkleg">%s 관측: 직접 재거나 현장에서 본 것 · '
               '%s 해석: 1차 자료를 읽고 푸는 쪽 · %s 전달: 남의 말을 옮기는 쪽. '
               '등급은 그 주제에 대해 누가 가까이 있었나를 뜻하며 어느 쪽이 옳은지를 '
               '정하지 않습니다.</p>'
               % (sr.MARK[sr.OBS], sr.MARK[sr.INT], sr.MARK[sr.REL]))


def one(meta, body, tab, kind, cells=()):
    src = nl.sources_of(meta)
    head = meta.get('headline') or ''
    # 이 카드가 서는 축의 칸. 글이 axis:/cell: 로 스스로 밝힌다(insights/axes.py)
    cellattr = ' data-cell="%s"' % nl.esc(' '.join(cells)) if cells else ''
    # 이 글이 서는 축의 칸을 본문 맨 앞에 작게 다시 그린다 — 그 칸만 불이 켜진다.
    minimap = ''
    if meta.get('axis') and meta.get('cell'):
        minimap = ('<div class="minimap">%s</div>'
                   % axis_svg(meta['axis'], active='%s:%s' % (meta['axis'], meta['cell']),
                              mini=True))
    # 두 명단이 제목보다 위다. 이 카드를 여는 이유가 「그래서 누가 받나」라서
    # 회사 이름이 제목보다 먼저 눈에 들어와야 한다(2026-08-18에 올렸다).
    return ('<details class="ins" data-kind="%s"%s><summary><span class="cid">%s</span>'
            '%s%s<h2 id="%s">%s%s</h2>'
            '<p class="sub">%s</p></summary><div class="body">%s%s</div>%s</details>'
            % (tab, cellattr, nl.esc(kind), period(meta, src, body), roster(meta),
               anchor(head), nl.esc(head), copy_btn(anchor(head), 'uc-copy'),
               nl.esc(meta.get('subhead', '')),
               minimap,
               nl.md_body(body, src, 'h4', 'bsec', rank_dot(meta.get('section', 'etc')))
               + (RANK_LEGEND if '|' in body else ''),
               srcbox(src)))


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
            cellid = '%s:%s' % (meta.get('axis', ''), meta.get('cell', ''))
            got.setdefault(sid, []).append(
                one(meta, body, tab, kind, (cellid,) if meta.get('cell') else ()))
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
            aid = 'sec-%s-%s' % (tab, sid)
            blocks.append('<section class="isec" id="%s" data-kind="%s" data-sec="%s" '
                          'data-grp="%s"><div class="ihead"><span class="inum">%02d</span>'
                          '<h3>%s</h3><span class="igrp">%s</span>'
                          '<span class="icnt">%d</span>%s</div>%s</section>'
                          % (aid, tab, sid, grp, num, nl.esc(title), nl.esc(GRPNAME[grp]),
                             len(got[sid]), copy_btn(aid, 'sec-copy'), ''.join(got[sid])))
        if blocks:
            out.append('<div class="kgroup" data-kind="%s"><h2 class="ktitle">%s</h2>%s</div>'
                       % (tab, nl.esc(kind), ''.join(blocks)))
    tophtml = ''
    if top:
        title = next((t for s, _g, t, _sub in ALLSEC if s == TOPSEC), TOPSEC)
        sub = next((x for s, _g, _t, x in ALLSEC if s == TOPSEC), '')
        tophtml = ('<section class="topsec" id="sec-%s"><div class="ihead">'
                   '<span class="inum">★</span><h3>%s</h3><span class="igrp">%s</span>'
                   '<span class="icnt">%d</span>%s</div>%s</section>'
                   % (TOPSEC, nl.esc(title), nl.esc(sub), len(top),
                      copy_btn('sec-' + TOPSEC, 'sec-copy'), ''.join(top)))
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


# 합류도. 타일 바로 위에 접힌 채로 서고, 열면 지도가 나온다.
MRG_CSS = '''
  .mrg{margin:0 0 14px;border:1px solid var(--line);border-radius:10px;
    background:var(--card);padding:0 16px}
  .mrg>summary{list-style:none;cursor:pointer;padding:13px 0;display:flex;
    align-items:baseline;gap:10px;flex-wrap:wrap}
  .mrg>summary::-webkit-details-marker{display:none}
  .mrg>summary::after{content:"▾";margin-left:auto;color:var(--faint);font-size:12px}
  .mrg[open]>summary::after{content:"▴"}
  .mg-t{font-size:14px;font-weight:800;color:var(--ink)}
  .mg-s{font-size:12px;color:var(--faint)}
  .mg-b{padding:0 0 16px}
  .mg-one+.mg-one{margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
  .mg-h{margin:0 0 3px;font-size:13.5px;font-weight:800;color:var(--ink)}
  .mg-l{margin:0 0 10px;font-size:12.5px;line-height:1.6;color:var(--sub)}
  .mg-n{margin:14px 0 0;font-size:11.5px;line-height:1.6;color:var(--faint)}
  .mg-b svg{width:100%;height:auto;display:block}
  .m-col{font-size:11px;font-weight:850;fill:var(--faint);
    letter-spacing:.02em;text-transform:none}
  .m-lab{font-size:11.5px;font-weight:800;fill:var(--ink)}
  .mflow{stroke:var(--line);stroke-width:1.4;fill:none}
  .mdot{fill:var(--sub)}
  .mcell{cursor:pointer}
  .mcell rect{fill:var(--card);stroke:var(--sub);stroke-width:1.4;
    transition:stroke .15s,fill .15s}
  .mcell.is-merge rect{stroke:var(--accent);stroke-width:2.2}
  .mcell:hover rect,.mcell:focus rect{fill:var(--soft);stroke:var(--accent)}
  .mcell:focus{outline:none}
  .mcell[aria-pressed="true"] rect{fill:var(--soft);stroke:var(--accent);stroke-width:2.4}

  /* 출처 등급 — 근거표 각주 앞 점 하나. 문장 속 인용에는 안 붙인다 */
  .rkd{font-size:9px;margin-right:3px;vertical-align:1px;letter-spacing:0}
  .rk-obs{color:var(--accent)}
  .rk-int{color:var(--sub)}
  .rk-rel{color:var(--faint)}
  .rkleg{margin:6px 0 0;font-size:11px;line-height:1.6;color:var(--faint)}

  .axis{margin:0 0 20px;padding:16px;border:1px solid var(--line);border-radius:10px;
    background:var(--card)}
  .ax-t{margin:0 0 3px;font-size:15px;font-weight:850;color:var(--ink)}
  .ax-l{margin:0 0 12px;font-size:12.5px;line-height:1.6;color:var(--sub)}
  .loopsvg{width:100%;height:auto;display:block}
  .loopsvg.is-mini{max-width:420px;margin:0 0 14px}
  .lp-sub{font-size:9.5px;fill:var(--faint)}
  .lp-back{stroke-dasharray:none}
  .mcell.is-todo rect{stroke-dasharray:4 3;stroke:var(--faint)}
  .mcell.is-off{opacity:.35}
  .mcell.is-on rect{fill:var(--soft);stroke:var(--accent);stroke-width:2.4}
  .minimap{margin:0 0 10px}

  /* merge 축 — 인과선은 근거가 붙는다. 나머지 mflow(회색 실선)와 색으로 가른다 */
  .causesvg,.flowsvg{width:100%;height:auto;display:block}
  .ce{stroke:var(--accent);stroke-width:1.6}
  .ce-sg{font-size:11px;font-weight:850;fill:var(--accent)}
  .cz-t{margin:16px 0 6px;font-size:12px;font-weight:800;color:var(--faint);
    text-transform:uppercase;letter-spacing:.04em}
  .flow-dot{fill:var(--faint)}
  .flow-dot-on{fill:var(--accent)}
  .flow-stop{cursor:pointer}
  .flow-stop text{fill:var(--sub)}
  .flow-stop:hover text{fill:var(--accent)}

  /* 축 탭 — 축이 둘 이상일 때만 선다 */
  .axtabs{display:flex;gap:6px;margin:0 0 12px;flex-wrap:wrap}
  .axtabs button{font:inherit;font-size:12.5px;font-weight:700;padding:6px 13px;
    border:1px solid var(--line);border-radius:999px;background:transparent;
    color:var(--sub);cursor:pointer}
  .axtabs button[aria-pressed="true"]{border-color:var(--accent);color:var(--accent)}
  .ax-pane[hidden]{display:none}
'''

def written_cells():
    """이미 글이 선 칸. 아직 안 쓴 칸은 점선으로 그린다.

    고리 편만 보던 자리다. 그런데 어느 글이 어느 칸에 서는지는 글이 자기 frontmatter 의
    cell: 로 밝히는 것이고(axes.py), 거기 「고리 편만」이라는 단서는 없다. 교차 인사이트가
    칸에 서 있는데도 「아직 안 씀」으로 그려지던 것을 고친다."""
    out = {}
    for p in sorted(glob.glob(os.path.join(paths.LOOP, '*.md'))
                    + glob.glob(os.path.join(paths.SYNTH, '*.md'))
                    + glob.glob(os.path.join(paths.BRIEFS, '*.md'))):
        meta, _b = nl.parse_front(io.open(p, encoding='utf-8').read())
        if meta.get('axis') and meta.get('cell'):
            out['%s:%s' % (meta['axis'], meta['cell'])] = {
                'head': meta.get('headline', ''), 'anchor': anchor(meta.get('headline', ''))}
    return out


_BW, _BH, _GAP = 96, 46, 14        # 칸 폭·높이·사이


def loop_svg(axis_id, active=None, mini=False):
    rows = axes.cells(axis_id)
    loop = [r for r in rows if r[3] == 'loop']
    out = [r for r in rows if r[3] == 'outside']
    done = written_cells()
    n = len(loop)
    W = n * _BW + (n - 1) * _GAP
    # 축이 한 바퀴 도는지는 축이 정한다(axes.py 의 back). 순환이 아닌 축에 곡선을 그리면
    # 있지도 않은 되먹임이 있는 것처럼 읽혀서, 곡선도 그 자리도 함께 뺀다.
    back = axes.BY_ID.get(axis_id, {}).get('back')
    top = 34 if back else 12                   # 되돌아오는 곡선 자리
    H = top + _BH + (6 if mini else 58)   # 미니는 칸 밑선·풀이 글이 잘리던 자리
    h = ['<svg viewBox="0 0 %d %d" class="loopsvg%s" role="group" '
         'aria-label="%s">' % (W, H, ' is-mini' if mini else '', nl.esc(axis_id))]
    if back:
        # 되돌아오는 곡선 — 마지막 칸 위에서 첫 칸 위로
        h.append('<path class="mflow lp-back" d="M%d %d C %d 2, %d 2, %d %d"/>'
                 % (W - _BW / 2, top, W - _BW / 2, _BW / 2, _BW / 2, top))
        if not mini:
            h.append('<text x="%d" y="12" text-anchor="middle" class="m-col">'
                     '%s</text>' % (W / 2, nl.esc(back)))
    for i, (cid, name, gloss, _col) in enumerate(loop):
        x = i * (_BW + _GAP)
        key = '%s:%s' % (axis_id, cid)
        got = done.get(key)
        cls = 'mcell'
        if active is not None:
            cls += ' is-on' if key == active else ' is-off'
        if not got:
            cls += ' is-todo'
        h.append('<g class="%s" data-cell="%s" data-label="%s" %s>'
                 % (cls, nl.esc(key), nl.esc(name),
                    '' if mini else 'role="button" tabindex="0"'))
        h.append('<title>%s — %s</title>' % (nl.esc(name), nl.esc(gloss)))
        h.append('<rect x="%d" y="%d" width="%d" height="%d" rx="9"/>'
                 % (x, top, _BW, _BH))
        h.append('<text x="%d" y="%d" text-anchor="middle" class="m-lab">%s</text>'
                 % (x + _BW / 2, top + 20, nl.esc(name)))
        h.append('<text x="%d" y="%d" text-anchor="middle" class="lp-sub">%s</text>'
                 % (x + _BW / 2, top + 35, nl.esc(gloss if got else '아직 안 씀')))
        h.append('</g>')
        if i < n - 1:
            h.append('<path class="mflow" d="M%d %d L%d %d"/>'
                     % (x + _BW, top + _BH / 2, x + _BW + _GAP, top + _BH / 2))
    if out and not mini:
        h.append('<text x="0" y="%d" class="m-col">고리 밖</text>' % (top + _BH + 24))
        for j, (cid, name, gloss, _col) in enumerate(out):
            x = 58 + j * (_BW + _GAP)
            key = '%s:%s' % (axis_id, cid)
            got = done.get(key)
            cls = 'mcell is-out' + ('' if got else ' is-todo')
            h.append('<g class="%s" data-cell="%s" data-label="%s" role="button" '
                     'tabindex="0"><title>%s</title>' % (cls, nl.esc(key),
                                                         nl.esc(name), nl.esc(gloss)))
            h.append('<rect x="%d" y="%d" width="%d" height="%d" rx="9"/>'
                     % (x, top + _BH + 10, _BW, 28))
            h.append('<text x="%d" y="%d" text-anchor="middle" class="m-lab">%s</text>'
                     % (x + _BW / 2, top + _BH + 29, nl.esc(name)))
            h.append('</g>')
    h.append('</svg>')
    return ''.join(h)


_CGEO = {'outer': (8, 128, 44, 10), 'price': (258, 150, 44, 11), 'merge': (486, 158, 56, 12)}
_CCOLT = (('outer', '바깥에서 오는 것'), ('price', '값이 매겨지는 곳'), ('merge', '회사 안으로'))


def _note_url(note, line=None):
    """근거 노트로 가는 주소. edges는 줄 번호까지, flow는 노트 파일까지만 가리킨다."""
    import urllib.parse
    rel = 'insights/notes/%s' % note
    url = nl.BLOB + urllib.parse.quote(rel)
    return url + ('#L%d' % line if line else '')


def _wrap2(s, n):
    """칸 라벨을 두 줄까지만 접는다. loop_svg 쪽은 칸이 넓어 이 접기가 필요 없었다."""
    if len(s) <= n:
        return [s]
    cut = s.rfind(' ', 0, n + 1)
    if cut < n // 2:
        cut = n
    head, tail = s[:cut].rstrip(), s[cut:].lstrip()
    return [head, tail[:n + 2] + ('…' if len(tail) > n + 2 else '')]


def cause_svg(axis_id, active=None):
    """합류(merge) 축 한 장. 바깥 → 값 → 회사 안으로, 근거가 있는 짝만 선을 긋는다.

    설계 docs/superpowers/specs/2026-08-21-돈값-축-design.md 「인과선은 근거가 있는
    것만 긋는다」. axes.edges_of()에 없는 짝은 나란히 있어도 선을 안 긋는다."""
    rows = axes.cells(axis_id)
    bycol = {}
    for cid, name, gloss, col in rows:
        bycol.setdefault(col, []).append((cid, name, gloss))
    done = written_cells()
    tot = {}
    for col, _t in _CCOLT:
        _x, _w, bh, _n = _CGEO[col]
        k = len(bycol.get(col, []))
        tot[col] = k * bh + (k - 1) * 16 if k else 0
    span = max(tot.values()) if tot else 0
    cy = 40 + span / 2.0
    H = int(40 + span + 26)
    W = 660
    h = ['<svg viewBox="0 0 %d %d" class="causesvg" role="group" aria-label="%s">'
         % (W, H, nl.esc(axis_id))]
    for col, title in _CCOLT:
        x, w, _bh, _n = _CGEO[col]
        h.append('<text x="%.0f" y="16" text-anchor="middle" class="m-col">%s</text>'
                 % (x + w / 2.0, nl.esc(title)))
    tops = {}
    for col, _title in _CCOLT:
        x, w, bh, cw = _CGEO[col]
        entries = bycol.get(col, [])
        y0 = cy - tot[col] / 2.0
        for i, (cid, name, gloss) in enumerate(entries):
            y = y0 + i * (bh + 16)
            tops[cid] = (x, y, w, bh)
            key = '%s:%s' % (axis_id, cid)
            got = done.get(key)
            cls = 'mcell'
            if col == 'merge':
                cls += ' is-merge'
            if active is not None:
                cls += ' is-on' if key == active else ' is-off'
            if not got:
                cls += ' is-todo'
            h.append('<g class="%s" data-cell="%s" data-label="%s" role="button" tabindex="0">'
                     % (cls, nl.esc(key), nl.esc(name)))
            h.append('<title>%s — %s</title>'
                     % (nl.esc(name), nl.esc(gloss if got else '아직 안 씀')))
            h.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="9"/>'
                     % (x, y, w, bh))
            lines = _wrap2(name, cw)
            ty = y + bh / 2.0 - (len(lines) - 1) * 7 + 4
            for j, line in enumerate(lines):
                h.append('<text x="%.0f" y="%.0f" text-anchor="middle" class="m-lab">%s</text>'
                         % (x + w / 2.0, ty + j * 14, nl.esc(line)))
            h.append('</g>')
    for src, dst, sign, why, note, line in axes.edges_of(axis_id):
        if src not in tops or dst not in tops:
            continue    # 검사기(A5)가 잡는다 — 그림은 조용히 건너뛴다
        sx, sy, sw, sh_ = tops[src]
        dx, dy, dw, dh_ = tops[dst]
        if sx <= dx:
            x1, y1 = sx + sw, sy + sh_ / 2.0
            x2, y2 = dx, dy + dh_ / 2.0
        else:
            x1, y1 = sx, sy + sh_ / 2.0
            x2, y2 = dx + dw, dy + dh_ / 2.0
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        h.append('<a href="%s" target="_blank" rel="noopener">' % _note_url(note, line))
        h.append('<title>%s — %s L%d</title>' % (nl.esc(why), nl.esc(note), line))
        h.append('<path class="mflow ce" data-why="%s" data-src="%s#L%d" '
                 'd="M%.0f %.0f L%.0f %.0f"/>'
                 % (nl.esc(why), nl.esc(note), line, x1, y1, x2, y2))
        h.append('<text x="%.0f" y="%.0f" text-anchor="middle" class="ce-sg">%s</text>'
                 % (mx, my - 4, nl.esc(sign)))
        h.append('</a>')
    h.append('</svg>')
    return ''.join(h)


def flow_svg(axis_id):
    """그 축이 언제 그렇게 봤나 — 정거장은 견해만 세운다(사실 보도는 안 세운다).

    scratchpad/gen_leesunyeop_dashboard.py의 flow_svg를 참고하되, 정거장이 노트를
    가리킨다는 점이 다르다 — 점을 누르면 그 노트로 간다."""
    stops = axes.flow_of(axis_id)
    if not stops:
        return ''
    n = len(stops)
    W, y = 640.0, 52.0
    pad = W / (2 * n)
    xs = [pad + (W - 2 * pad) * i / (n - 1) for i in range(n)] if n > 1 else [W / 2.0]
    wrap_at = max(6, int(52 / n))
    h = ['<svg viewBox="0 0 640 112" class="flowsvg" role="img" aria-label="언제 그렇게 봤나">']
    if n > 1:
        h.append('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" class="mflow"/>'
                 % (xs[0], y, xs[-1], y))
    for i, (d, label, note) in enumerate(stops):
        x = xs[i]
        last = (i == n - 1)
        h.append('<a href="%s" target="_blank" rel="noopener" class="flow-stop">'
                 % _note_url(note))
        h.append('<title>%s — %s</title>' % (nl.esc(label), nl.esc(note)))
        h.append('<circle cx="%.0f" cy="%.0f" r="%d" class="%s"/>'
                 % (x, y, 6 if last else 4, 'flow-dot-on' if last else 'flow-dot'))
        h.append('<text x="%.0f" y="34" text-anchor="middle" class="m-lab" '
                 'style="font-size:10.5px">%s</text>' % (x, nl.esc(d)))
        for j, line in enumerate(_wrap2(label, wrap_at)):
            h.append('<text x="%.0f" y="%d" text-anchor="middle" class="lp-sub" '
                     'style="font-size:10.5px">%s</text>' % (x, 74 + j * 13, nl.esc(line)))
        h.append('</a>')
    h.append('</svg>')
    return ''.join(h)


def axis_svg(axis_id, active=None, mini=False):
    """모양별로 알맞은 렌더러로 넘긴다 — loop|line은 loop_svg, merge는 cause_svg."""
    if axes.shape_of(axis_id) == 'merge':
        return cause_svg(axis_id, active=active)
    return loop_svg(axis_id, active=active, mini=mini)


def axis_layer():
    """페이지 맨 위 한 장. 「지금 무슨 일이 벌어지는 중인가」를 말하는 자리다.

    JS(TAB_JS)는 칸 클릭을 각 `.mg-b` 컨테이너에서 위임받는다(옛 합류도 프로토타입 이후
    그대로다) — svg를 `.mg-b`로 감싸지 않으면 칸을 눌러도 아무 일도 안 일어난다.
    축이 둘 이상이면 축 탭으로 고른다. 기본은 첫 축이다.
    """
    panes = []
    tabs = []
    for i, a in enumerate(axes.AXES):
        aid = a['id']
        tabs.append('<button type="button" data-axis="%s" aria-pressed="%s">%s</button>'
                    % (nl.esc(aid), 'true' if i == 0 else 'false', nl.esc(a['title'])))
        extra = ''
        if axes.shape_of(aid) == 'merge':
            fw = flow_svg(aid)
            if fw:
                extra = '<p class="cz-t">언제 그렇게 봤나</p>%s' % fw
        panes.append('<div class="ax-pane" data-axis="%s"%s><p class="ax-t">%s</p>'
                     '<p class="ax-l">%s</p><div class="mg-b">%s</div>%s'
                     '<p class="mg-n">칸을 누르면 그 편으로 갑니다.</p></div>'
                     % (nl.esc(aid), '' if i == 0 else ' hidden',
                        nl.esc(a['title']), nl.esc(a['lede']), axis_svg(aid), extra))
    tabbar = '<div class="axtabs">%s</div>' % ''.join(tabs) if len(axes.AXES) > 1 else ''
    return '<section class="axis">%s%s</section>' % (tabbar, ''.join(panes))


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
    html = (TMPL.replace('__CSS__', style.BASE + KIND_CSS + CARD_CSS + CSS + MRG_CSS)
                # 축 층이 맨 처음이다 — 지금 무슨 일이 벌어지는 중인지가 무엇이 있는지보다
                # 먼저 와야 한다. 카드 더미가 입구라는 지적에 답하는 자리다. 어디서부터
                # 읽을지는 이 합류도가 말해 준다 — 따로 두던 「처음 오셨다면」 목록은 걷어냈다.
                .replace('__GUIDE__', axis_layer() + guide(per))
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
  /* 카드 하나·갈래 하나를 지목하는 주소를 집어 가는 버튼 */
  .uc-copy,.sec-copy{font-family:inherit;font-size:var(--t-lbl);font-weight:750;cursor:pointer;
        color:var(--sub);background:transparent;border:1px dashed var(--line);
        border-radius:6px;padding:4px 10px}
  .uc-copy:hover,.sec-copy:hover{color:var(--accent);border-color:var(--accent)}
  .uc-copy{margin-left:8px;vertical-align:2px}
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
  // 합류도 칸을 고른 상태(cell)는 세 번째 화면이다. 타일은 주제로 나누고,
  // 칸은 주제를 가로질러 고른다 — 둘이 동시에 걸리면 나중 것이 앞의 것을 푼다.
  // 축이 둘 이상이면 축마다 .mg-b가 하나씩이다(안 보이는 축도 DOM에는 있다) — 전부에서
  // 칸 클릭을 받는다.
  var mbars=document.querySelectorAll('.mg-b');
  var kind='all', sec=null, cell=null;
  var names={};
  if(sbar) sbar.querySelectorAll('button').forEach(function(b){
    var t=b.querySelector('.st-t');
    names[b.dataset.sec] = t ? t.textContent : b.dataset.sec;
  });
  mbars.forEach(function(mbar){
    mbar.querySelectorAll('.mcell').forEach(function(g){
      names[g.dataset.cell] = g.dataset.label || g.dataset.cell;
    });
  });
  function apply(){
    var incell = (cell!==null);
    var picking = (sec===null && !incell);
    // 주제를 바꿔도 고른 종류는 남는다. 새 주제에 그 종류가 없으면 조건이 하나도 안 맞아
    // 빈 화면이 되므로, 그런 경우에만 「전체」로 되돌린다.
    if(!picking && !incell && kind!=='all'){
      var alive=false;
      document.querySelectorAll('.isec').forEach(function(s2){
        if(s2.dataset.kind===kind && (sec==='all' || s2.dataset.sec===sec)) alive=true;
      });
      if(!alive) kind='all';
    }
    document.querySelectorAll('details.ins').forEach(function(d){
      d.hidden = incell && (' '+(d.dataset.cell||'')+' ').indexOf(' '+cell+' ')<0;
    });
    document.querySelectorAll('.isec').forEach(function(s2){
      s2.hidden = incell
        ? s2.querySelectorAll('details.ins:not([hidden])').length===0
        : (picking || !((kind==='all' || s2.dataset.kind===kind) &&
                        (sec==='all'  || s2.dataset.sec===sec)));
    });
    var tops=document.querySelector('.topsec');
    if(tops) tops.hidden = incell &&
      tops.querySelectorAll('details.ins:not([hidden])').length===0;
    document.querySelectorAll('.kgroup').forEach(function(g){
      g.hidden = g.querySelectorAll('.isec:not([hidden])').length===0;
    });
    mbars.forEach(function(mbar){
      mbar.querySelectorAll('.mcell').forEach(function(g){
        g.setAttribute('aria-pressed', String(g.dataset.cell===cell));
      });
    });
    if(sbar) sbar.hidden = !picking;
    if(back){
      back.hidden = picking;
      var now=back.querySelector('.sb-now');
      now && (now.textContent = picking ? '' : (names[incell ? cell : sec]||''));
    }
    // 탭 숫자는 지금 보고 있는 주제 안에서 다시 센다. 전역 집계를 걸어 두면 그 주제에
    // 없는 종류에도 숫자가 찍히고, 눌렀을 때 조건이 하나도 안 맞아 빈 화면이 된다.
    // 탭 막대는 주제를 고른 뒤에만 보이므로 전역 집계가 맞는 화면은 애초에 없다.
    kbar.hidden = picking || incell;
    if(!kbar.hidden){
      var cnt={}, kinds=0, tot=0;
      document.querySelectorAll('.isec').forEach(function(s2){
        if(sec!=='all' && s2.dataset.sec!==sec) return;
        var k=s2.dataset.kind, n=s2.querySelectorAll('details.ins').length;
        cnt[k]=(cnt[k]||0)+n; tot+=n;
      });
      for(var k2 in cnt){ if(cnt[k2]) kinds++; }
      kbar.querySelectorAll('button').forEach(function(b){
        var t=b.dataset.tab, n=(t==='all') ? tot : (cnt[t]||0);
        b.hidden = (t!=='all' && !n);      // 없는 종류는 누를 수 없게 감춘다
        var tn=b.querySelector('.tn'); if(tn) tn.textContent=n;
      });
      // 종류가 하나뿐인 주제에서는 고를 것이 없다 — 「전체」와 결과가 같은 탭만 남는다
      kbar.hidden = kinds<2;
    }
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
    cell=null; sec=b.dataset.sec; apply(); mark();
    var first=document.querySelector('.isec:not([hidden])');
    if(first) first.scrollIntoView({behavior:'smooth', block:'start'});
  });
  function pickCell(g){
    // 같은 칸을 다시 누르면 푼다 — 지도를 열어 둔 채로 되돌릴 길이 있어야 한다
    cell = (g.dataset.cell===cell) ? null : g.dataset.cell;
    sec=null; kind='all'; apply(); mark();
    var first=document.querySelector('.topsec:not([hidden]), .isec:not([hidden])');
    if(cell && first) first.scrollIntoView({behavior:'smooth', block:'start'});
  }
  mbars.forEach(function(mbar){
    mbar.addEventListener('click', function(e){
      var g=e.target.closest('.mcell'); if(!g) return;
      pickCell(g);
    });
    mbar.addEventListener('keydown', function(e){
      if(e.key!=='Enter' && e.key!==' ') return;
      var g=e.target.closest('.mcell'); if(!g) return;
      e.preventDefault(); pickCell(g);
    });
  });
  // 축 탭 — 축이 둘 이상일 때만 선다. 칸 고르기(cell)와 달리 히스토리에 안 쌓는다,
  // 같은 층 안의 전환이라 관문이 아니다(UI 규약).
  var axbar=document.querySelector('.axtabs');
  if(axbar) axbar.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    var want=b.dataset.axis;
    axbar.querySelectorAll('button').forEach(function(b2){
      b2.setAttribute('aria-pressed', String(b2.dataset.axis===want));
    });
    document.querySelectorAll('.ax-pane').forEach(function(p){
      p.hidden = (p.dataset.axis!==want);
    });
  });
  // 화면이 바뀌면 히스토리에도 한 칸 쌓는다. 안 쌓으면 브라우저 뒤로가기가 「주제 고르기」로
  // 돌아가지 않고 페이지째 나간다 — 잠긴 장에서는 「비공개 자료」로 튕겨 나간다.
  var quiet=false;                       // 뒤로가기로 되돌리는 중에는 다시 쌓지 않는다
  function mark(){
    if(quiet) return;
    var base=location.pathname + location.search;
    var want = base;
    if(cell!==null) want = base + '#cell-' + encodeURIComponent(cell);
    else if(sec!==null) want = base + '#view-' + encodeURIComponent(sec);
    if(want !== base + location.hash)
      history.pushState({sec:sec, kind:kind, cell:cell}, '', want);
  }
  if(back) back.addEventListener('click', function(e){
    if(!e.target.closest('.sb-btn')) return;
    // 「← 이전」과 브라우저 뒤로가기가 같은 곳으로 가야 한다. 쌓아 둔 칸이 있으면 그걸 쓴다.
    if(history.state && (history.state.sec || history.state.cell)){ history.back(); return; }
    sec=null; cell=null; kind='all'; apply();
    if(sbar) sbar.scrollIntoView({behavior:'smooth', block:'start'});
  });
  window.addEventListener('popstate', function(e){
    quiet=true;
    var st=e.state, h=(location.hash||'').slice(1);
    if(st && typeof st.sec !== 'undefined'){
      sec=st.sec; kind=st.kind || 'all'; cell=(typeof st.cell==='undefined') ? null : st.cell;
    } else if(!h){
      sec=null; cell=null; kind='all';
    } else if(h.indexOf('cell-')===0){
      cell=decodeURIComponent(h.slice(5)); sec=null; kind='all';
    } else if(h.indexOf('view-')===0){
      sec=decodeURIComponent(h.slice(5)); cell=null;
    } else {
      var el=document.getElementById(decodeURIComponent(h));
      var s2=el && el.closest ? el.closest('.isec') : null;
      sec = s2 ? s2.dataset.sec : null;
    }
    apply();
    // 주제 고르기로 돌아왔으면 주소의 #도 지운다. 남겨 두면 뒤이어 뜨는 hashchange가
    // 그 카드를 다시 열어 뒤로가기가 제자리로 튕긴다.
    if(sec===null && cell===null && location.hash){
      history.replaceState({sec:null, kind:'all', cell:null}, '',
                           location.pathname + location.search);
    }
    quiet=false;
  });
  // 카드 하나·갈래 하나를 지목한 주소로 들어온 사람. 첫 화면이 주제 고르기라 그냥 두면
  // 링크를 받은 사람이 타일 화면에 떨어진다 — 그 갈래를 펴고 카드를 열어 거기로 보낸다.
  function jump(el, smooth){
    var isec=el.closest('.isec'), det=el.closest('details.ins');
    if(isec){ cell=null; sec=isec.dataset.sec; kind='all'; apply(); mark(); }
    if(det && !det.open) det.open=true;
    setTimeout(function(){
      (det||el).scrollIntoView({behavior: smooth ? 'smooth' : 'auto', block:'start'});
    }, 60);
  }
  function fromHash(smooth){
    var id=(location.hash||'').slice(1); if(!id) return;
    // 합류도 칸을 지목한 주소로 들어온 사람. 칸은 DOM 요소가 아니라 상태다
    if(id.indexOf('cell-')===0){
      cell=decodeURIComponent(id.slice(5)); sec=null; kind='all'; apply();
      var mg=document.querySelector('.mrg'); if(mg) mg.open=true;
      return;
    }
    var el=document.getElementById(decodeURIComponent(id));
    if(el) jump(el, smooth);
  }
  document.addEventListener('click', function(e){
    var a=e.target.closest('.body a[href^="#card-"]');
    if(a){
      var t=document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
      if(t){ e.preventDefault(); jump(t, true); return; }
    }
    var b=e.target.closest('.uc-copy, .sec-copy'); if(!b) return;
    e.preventDefault();        // 카드 머리 안에 있는 버튼이라 그냥 두면 카드가 접힌다
    e.stopPropagation();
    var url=location.origin + location.pathname + '#' + encodeURIComponent(b.dataset.anchor);
    var done=function(ok){
      b.textContent = ok ? '복사됨' : '주소창에 있습니다';
      setTimeout(function(){ b.textContent='링크 복사'; }, 1600);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(function(){ done(true); }, function(){ done(false); });
    } else {
      history.replaceState(null, '', url);
      done(false);
    }
  });
  window.addEventListener('hashchange', function(){ fromHash(true); });
  apply();
  fromHash(false);
  // 링크를 받고 들어온 사람의 첫 칸. 뒤로가기가 여기로 돌아온다
  if(!history.state) history.replaceState({sec:null, kind:'all', cell:null}, '');
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
  <div class="meta"><a class="maplink" href="Yomianalysis.html">전체 입구 →</a></div>
</header>
__GUIDE__
__TOP__
__TABS__
__CARDS__
__TABJS__
<footer>
<p class="lede">문서 하나를 요약한 페이지가 아닙니다. 원문마다 노트 한 장을 만들어 두고,
  그 노트 전량을 한 번에 읽어야 보이는 것만 올립니다. 문장 옆 줄번호를 누르면 근거가 된
  원문 그 줄로 가고, 카드 아래 「참고한 문서」를 펼치면 무엇을 읽고 썼는지 나옵니다.</p>
<div class="meta"><span>판단 __N__건</span></div>
근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
