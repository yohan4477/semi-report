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
GROUPS = (('ai', 'AI 판', 'AI를 만들고 파는 쪽 — 칩부터 그 돈까지'),
          ('macro', 'AI 밖', 'AI 판을 흔드는 바깥 조건 — 기름값과 돈값'))

# (id, 큰 묶음, 이름, 설명)
SECTIONS = (('chip', 'ai', '반도체 · 메모리 · 가속기', '메모리 수급, GPU 경쟁, 직접 설계한 칩'),
            ('power', 'ai', '전력 · 데이터센터', '전력망 제약과 자가발전, 랙 밀도와 냉각'),
            ('model', 'ai', '모델 · 학습', '강화학습과 환경 제작, 모델 구조'),
            # 옛 이름 "사업 · 비용 · 재무"는 아래 "시장 · 자금"과 구별이 안 됐다.
            # 여기는 AI를 파는 회사들의 손익이고, 저기는 금리·환율이다.
            ('biz', 'ai', 'AI 사업 · 수익', '토큰 값과 마진, AI로 누가 얼마를 버나'),
            # 아래 둘은 제3자 코퍼스가 들어오며 생겼다. 위 넷에 억지로 밀어 넣으면
            # 원유·해협·환율 이야기가 칩 이야기와 섞여 어느 것도 안 읽힌다.
            ('energy', 'macro', '에너지 · 원자재', '유가와 해협, LNG 비축, 에너지 안보'),
            ('market', 'macro', '금리 · 환율 · 시장', '돈값과 환율, 수급과 포지션, 값이 매겨지는 방식'),
            # 부동산 코퍼스 21편이 들어오며 생겼다. 집값·세금은 금리 이야기와 붙일 수도
            # 있었지만, 재건축이 막히는 지점과 클러스터 땅값은 환율 카드 옆에서 안 읽힌다
            ('housing', 'macro', '집 · 땅 · 정비사업', '집값과 세금, 재건축이 막히는 지점, 공장이 오는 땅'))

ALLSEC = SECTIONS + (('etc', 'macro', '그 밖', ''),)
GRPNAME = dict((g, t) for g, t, _s in GROUPS)


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


STALE_DAYS = {'biz': 120, 'chip': 180, 'model': 180, 'power': 365}


def period(meta, src):
    """근거가 언제 것인지를 카드 겉면에 박는다.

    맞는 말이어도 옛날 이야기면 지금은 틀린 말일 수 있다. 그런데 as_of 는 내가 쓴 날짜라
    글을 안 고치고 두면 그대로 남는다. 그래서 실제로 인용한 원문의 발행일 범위를 쓴다.
    검사기는 insights/check_fresh.py 가 따로 본다.
    """
    ds = sorted(re.findall(r'\[(\d{6})\]', ' '.join(d.get('base', '') for d in src)))
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


def one(meta, body, tab, kind):
    src = nl.sources_of(meta)
    head = meta.get('headline') or ''
    return ('<details class="ins" data-kind="%s"><summary><span class="cid">%s</span>'
            '%s<h2 id="%s">%s</h2>'
            '<p class="sub">%s</p></summary><div class="body">%s</div>%s</details>'
            % (tab, nl.esc(kind), period(meta, src),
               anchor(head), nl.esc(head), nl.esc(meta.get('subhead', '')),
               nl.md_body(body, src, 'h4', 'bsec'), srcbox(src)))


def cards():
    out, per, bysec, mix = [], {}, {}, {}
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
        blocks, num = [], 0
        for sid, grp, title, _sub in ALLSEC:
            if not got.get(sid):
                continue
            num += 1
            blocks.append('<section class="isec" data-kind="%s" data-sec="%s" data-grp="%s">'
                          '<div class="ihead"><span class="inum">%02d</span>'
                          '<h3>%s</h3><span class="igrp">%s</span>'
                          '<span class="icnt">%d</span></div>%s</section>'
                          % (tab, sid, grp, num, nl.esc(title), nl.esc(GRPNAME[grp]),
                             len(got[sid]), ''.join(got[sid])))
        out.append('<div class="kgroup" data-kind="%s"><h2 class="ktitle">%s</h2>%s</div>'
                   % (tab, nl.esc(kind), ''.join(blocks)))
    return ''.join(out), per, bysec, mix


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
    total = sum(bysec.values())
    tiles = ['<button class="stile is-all" data-sec="all" aria-pressed="true">'
             '<span class="st-num">✦</span><span class="st-t">전체 보기</span>'
             '<span class="st-s">모든 주제를 한 줄로</span>'
             '<span class="st-n">%d</span></button>' % total]
    num = 0
    for gid, gtitle, gsub in GROUPS:
        rows = [s for s in ALLSEC if s[1] == gid and bysec.get(s[0])]
        if not rows:
            continue
        # 큰 묶음 이름을 한 줄 띄워 준다 — 이게 없으면 여섯 장이 다 같은 급으로 보인다
        tiles.append('<div class="sgrp"><b>%s</b><span>%s</span>'
                     '<span class="sg-n">%d</span></div>'
                     % (nl.esc(gtitle), nl.esc(gsub),
                        sum(bysec[s[0]] for s in rows)))
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
    body, per, bysec, mix = cards()
    n = sum(per.values())
    html = (TMPL.replace('__CSS__', style.BASE + KIND_CSS + CSS)
                .replace('__GUIDE__', guide(per))
                .replace('__TABS__', '<div class="tabbar">%s</div>%s'
                         % (tabs(per), sectiles(bysec, mix)))
                .replace('__CARDS__', body)
                .replace('__N__', str(n))
                .replace('__TABJS__', TAB_JS + ui_bits.TOP_BTN))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: %s -> %s' % (' · '.join('%s %d' % (k, per[t]) for _d, k, t in KINDS if per.get(t)), OUT))


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
  /* 근거가 오래된 카드는 겉면에서 바로 보이게 — 옛날 이야기를 지금 이야기로 읽지 않도록 */
  .asof.stale{color:#b45309;font-weight:600}
  .asof.stale::after{content:' · 오래됨'}
  .ins h2{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;line-height:1.36;margin:8px 0 2px}
  .ins .sub{font-size:var(--t-body);color:var(--faint);margin:3px 0 0}
  .bsec{font-size:var(--t-meta);font-weight:800;color:var(--accent2);margin:14px 0 5px;
        text-transform:uppercase;letter-spacing:.04em}
  .body p,.body li{font-size:var(--t-body);color:var(--sub);line-height:1.65}
  .body b{color:var(--ink)}
  .cite{font-size:.72em;font-weight:800;color:var(--accent);text-decoration:none;
        vertical-align:.28em;margin-left:2px;padding:0 3px;border-radius:4px;background:var(--sunk)}
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
  /* 큰 묶음 줄 — 타일 격자를 가로로 끊는다 */
  .sgrp{grid-column:1/-1;display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;
        margin:8px 0 -2px;padding-bottom:5px;border-bottom:1px solid var(--line)}
  .sgrp>b{font-size:var(--t-body);font-weight:800;color:var(--ink);letter-spacing:-.01em}
  .sgrp>span{font-size:var(--t-lbl);color:var(--faint)}
  .sg-n{margin-left:auto;font-weight:800;color:var(--faint);font-variant-numeric:tabular-nums}
  .srcs{margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
  .srcs>summary{cursor:pointer;font-size:var(--t-meta);font-weight:700;color:var(--sub);
        list-style:none}
  .srcs>summary::-webkit-details-marker{display:none}
  .srcs>summary::before{content:"📄 ";opacity:.7}
  .srcs ul{margin:8px 0 0;padding-left:18px}
  .srcs li{font-size:var(--t-meta);line-height:1.8}
  .srcs a{color:var(--sub);text-decoration:none;border-bottom:1px solid var(--line)}
  .srcs a:hover{color:var(--accent)}

  /* 좁은 화면 — 글이 화면 가장자리에 붙으면 읽기 힘들다 */
  @media (max-width:640px){
    .ins{padding:15px 16px;border-radius:10px}
    .body ul{padding-left:17px;margin:6px 0}
    .body li{margin-bottom:7px}
    .body p{margin:6px 0}
    .guide{gap:6px}
    .guide div{padding:10px 13px}
    .ihead{gap:7px}
    .tabbar{margin:12px -14px 6px;padding:8px 14px 6px}
    .sgrid{grid-template-columns:1fr 1fr;gap:8px}
    .stile{padding:11px 12px 10px}
    .st-s{display:none}
    .st-mix{margin-top:4px}
    .tw{margin-left:-16px;margin-right:-16px;padding:0 16px}
    .body td:first-child{white-space:normal}
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
__TABS__
__CARDS__
__TABJS__
<footer>근거는 원문 줄 인용입니다. 종목 추천이 아니며 가격·밸류에이션·타이밍은
이 체계에 없습니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
