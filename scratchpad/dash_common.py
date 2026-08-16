# -*- coding: utf-8 -*-
# 제3자 해설 대시보드 공용 부품 — 카드 마크업·추가 CSS·페이지 조립.
# 미국주식 사관학교와 부동산 두 페이지가 같은 규칙을 쓰게 한 벌만 둔다.
# 기본 CSS는 언더스탠딩 대시보드의 <style>을 통째로 물려받는다(세 페이지가 한 벌로 보이게).
import io, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import rollup_lib as _rl
# 카드 마크업 표준은 scripts/card_lib.py 한 벌뿐이다 — 여기서는 가져다 쓴다
from card_lib import EXTRA_CSS, FIG_CSS, FIG_DEFS, slug, card_html  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import ui_bits  # noqa: E402

SRC = os.path.join(ROOT, '대시보드', '언더스탠딩 대시보드.html')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'

def blob(path):
    return BLOB + urllib.parse.quote(path)


# 주제 고르는 화면 ↔ 카드 읽는 화면 — 물려받는 CSS에는 없는 규칙만 여기서 더한다.
# .sgrid는 display:grid라 hidden 속성만으로는 안 사라진다. 그래서 [hidden] 규칙이 꼭 있어야 한다.
PICK_CSS = '''
  .sgrid[hidden], .sec-pick[hidden]{display:none}
  .sback{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 2px}
  .sback[hidden]{display:none}
  .sb-btn{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:7px 13px;
          border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink)}
  .sb-btn:hover{border-color:var(--accent);color:var(--accent)}
  .sb-now{font-weight:800;font-size:13.5px}
  /* 데스크톱에서는 카드를 읽는 동안 「주제 다시 고르기」가 따라 내려온다.
     배경이 없으면 뒤 글자가 비쳐 겹쳐 보이니 지면 색을 깔고 카드 위에 올린다. */
  @media (min-width:820px){
    .sback{position:sticky;top:0;z-index:40;margin:0 0 8px;padding:12px 0 10px;
           background:var(--paper);border-bottom:1px solid var(--line)}
  }
</style>'''


def css():
    src = io.open(SRC, encoding='utf-8').read()
    out = src[src.find('<style'):src.find('</style>') + 8]
    # 원본에 이미 표준 CSS가 들어가 있으면(에너지 페이지 전환 이후) 두 번 붙이지 않는다
    out = out if '.uc-gain{' in out else out.replace('</style>', EXTRA_CSS)
    if '.sb-btn{' not in out:
        out = out.replace('</style>', PICK_CSS)
    # 물려받은 CSS에 표준 규칙이 이미 구워져 있으면 위에서 EXTRA_CSS가 안 붙는다 —
    # 그림 규칙은 그때도 있어야 한다. 없으면 검은 덩어리로만 그려진다.
    if '.uc-fig{' not in out:
        # FIG_CSS는 규칙만 담은 조각이라 태그를 다시 닫아 준다. 안 닫으면 문서 나머지가
        # 통째로 스타일로 먹혀 본문이 빈 페이지가 나간다.
        out = out.replace('</style>', FIG_CSS + '</style>')
    # .xlink는 언더스탠딩 대시보드 CSS에 있다 — 페이지끼리 오가는 링크가 같은 모양이어야 한다
    assert '.xlink{' in out, '언더스탠딩 대시보드 CSS에 .xlink 규칙이 없다'
    return out


def sections(cards):
    """카드를 섹션별로 묶는다 — CARDS에 적힌 순서가 곧 화면 순서다"""
    secs, order = {}, []
    for c in cards:
        sid = c['section'][0]
        if sid not in secs:
            secs[sid] = (c['section'], [])
            order.append(sid)
        secs[sid][1].append(c)
    return secs, order


SCOPE_TABS = '''<div class="scope-tabs">
    <button data-pick="kr" aria-pressed="true">🇰🇷 국내 <span class="cnt">%d</span></button>
    <button data-pick="intl" aria-pressed="false">🌍 해외 <span class="cnt">%d</span></button>
    <button data-pick="all" aria-pressed="false">전체 <span class="cnt">%d</span></button>
  </div>'''

FOLD_JS = '''<script>
(function(){
  function toggle(card){
    var open=card.classList.toggle('is-open');
    var head=card.querySelector('.uc-head');
    if(head) head.setAttribute('aria-expanded', String(open));
    if(!open){
      var top=card.getBoundingClientRect().top;
      if(top<60) card.scrollIntoView({block:'start'});   // 접을 때 화면이 위로 튀지 않게
    }
  }
  document.addEventListener('click', function(e){
    var head=e.target.closest('.uc-head');
    if(head) toggle(head.closest('.ucard'));
  });
  document.addEventListener('keydown', function(e){
    if(e.key!=='Enter' && e.key!==' ') return;
    var head=e.target.closest('.uc-head');
    if(head){ e.preventDefault(); toggle(head.closest('.ucard')); }
  });
})();
</script>'''

NAV_JS = '''<script>
(function(){
  var tabs=document.querySelector('.scope-tabs');   // 범위 탭은 국내·해외가 섞인 페이지에만 있다
  var box=document.querySelector('.sec-pick'); if(!box) return;
  var back=document.querySelector('.sback');
  var pick = tabs? 'kr' : 'all';   // 범위 탭이 없는 페이지는 늘 전체
  var modes=document.querySelector('.mode-pick');
  var layer=document.querySelector('.xlayer');
  // 화면이 셋이다. 무엇을 읽을지 고르는 화면(mode===null), 주제를 고르는 화면,
  // 그 주제의 카드를 읽는 화면. 한 화면에 다 쌓으면 무엇을 보고 있는지 흐려진다.
  // 모드 버튼이 없는 페이지(금융·회계사 등)는 예전처럼 곧장 단일 포스트로 연다.
  var mode = modes ? null : 'single';
  var only=null, picking=true;
  function opt(id){ return box.querySelector('button[data-sec="'+id+'"]'); }
  function apply(){
    var single = (mode==='single');
    if(modes) modes.hidden = (mode!==null);
    if(layer) layer.hidden = (mode!=='cross');
    if(tabs) tabs.hidden = !single;
    document.querySelectorAll('.ucard[data-scope]').forEach(function(c){
      c.hidden = !(pick==='all' || c.dataset.scope===pick);
    });
    // 롤업 리포트도 범위를 따른다 — 국내를 고르면 국내 리포트만 남는다
    document.querySelectorAll('.rlrep[data-scope]').forEach(function(r){
      r.hidden = !(pick==='all' || r.dataset.scope===pick);
    });
    document.querySelectorAll('.rlold').forEach(function(o){
      o.hidden = o.querySelectorAll('.rlrep:not([hidden])').length===0;
    });
    // 섹션을 고르면 롤업 리포트도 그 섹션 항목만 남긴다(섹션 표시가 없는 항목은 늘 보인다)
    document.querySelectorAll('.rlrep').forEach(function(rep){
      if(!rep.hasAttribute('data-scope')) rep.hidden = false;
      var tagged=rep.querySelectorAll('.rll li[data-sec]');
      tagged.forEach(function(li){ li.hidden = !!only && li.dataset.sec!==only; });
      if(only && tagged.length && !rep.querySelectorAll('.rll li:not([hidden])').length) rep.hidden = true;
    });
    var roll=document.querySelector('.rollup');
    if(roll) roll.hidden = roll.querySelectorAll('.rlrep:not([hidden])').length===0;
    var seen=0;
    document.querySelectorAll('section[id]').forEach(function(s){
      var live=s.querySelectorAll('.ucard:not([hidden])').length;
      seen+=live;
      s.hidden = !single || picking || live===0 || (only && s.id!==only);
      var o=opt(s.id);
      if(o){
        o.hidden = live===0;
        var c=o.querySelector('.cnt'); if(c) c.textContent=live;
      }
    });
    var all=opt(''); if(all){ var ac=all.querySelector('.cnt'); if(ac) ac.textContent=seen; }
    box.hidden = !(single && picking);
    var roll2=document.querySelector('.rollup');
    // 롤업은 개별 포스트를 고른 뒤 주제 고르는 화면에서만 — 통합 인사이트 쪽 글이 아니다
    if(roll2){ if(!single) roll2.hidden = true; else if(picking) roll2.hidden = false; }
    if(back){
      // 돌아갈 데가 있을 때만 — 모드 버튼이 없는 페이지는 주제를 고른 뒤에야 나온다
      back.hidden = modes ? (mode===null) : picking;
      var now=back.querySelector('.sb-now');
      if(now){
        var cur = only ? opt(only) : opt('');
        var t = cur && cur.querySelector('.st-t');
        now.textContent = !single ? '통합 인사이트'
                        : picking ? '개별 포스트' : (t ? t.textContent : '');
      }
    }
    box.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String((b.dataset.sec||null)===only));
    });
    if(tabs) tabs.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.pick===pick));
    });
  }
  if(tabs) tabs.addEventListener('click', function(e){
    var b=e.target.closest('button');
    if(!b) return;
    pick=b.dataset.pick; only=null; picking=true; apply();
    window.scrollTo({top:0});   // 목록이 통째로 바뀌므로 맨 위에서 다시 읽게 한다
  });
  box.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    only = b.dataset.sec || null;   // 전체 보기 타일이면 only=null 로 전부 편다
    picking=false;
    apply();
    var sec = only ? document.getElementById(only) : null;
    if(sec) sec.scrollIntoView({behavior:'smooth', block:'start'});
    else window.scrollTo({top:0, behavior:'smooth'});
  });
  if(modes) modes.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    mode=b.dataset.mode; picking=true; only=null; apply();
    window.scrollTo({top:0});
  });
  // 「← 이전」은 한 단계씩 거슬러 간다 — 카드 → 주제 고르기 → 무엇을 읽을지 고르기
  if(back) back.addEventListener('click', function(e){
    if(!e.target.closest('.sb-btn')) return;
    if(mode==='single' && !picking){ picking=true; }
    else if(modes){ mode=null; }
    only=null; apply();
    var to = (mode===null) ? modes : box;
    if(to) to.scrollIntoView({behavior:'smooth', block:'start'});
  });
  apply();
})();
</script>'''


def snip(text, limit=46):
    """타일 설명은 두 줄까지만 — 말이 중간에서 잘리지 않게 띄어쓰기에서 끊고 …를 붙인다"""
    t = (text or '').strip()
    if len(t) <= limit:
        return t
    cut = t[:limit]
    sp = cut.rfind(' ')
    if sp >= limit - 14:      # 너무 앞에서 끊기면 차라리 글자 수로 자른다
        cut = cut[:sp]
    return cut.rstrip(' ,·') + '…'


BACK = ('<div class="sback" hidden><button type="button" class="sb-btn">← 이전</button>'
        '<span class="sb-now"></span></div>')


def sec_picker(secs, order, total, with_back=True):
    """섹션을 네모 타일로 세운다 — 무엇이 몇 편 들었는지 접지 않고 보여 준다.

    층이 있는 페이지는 「← 이전」을 층보다 위에 둬야 해서(with_back=False) 조립기가 따로 꽂는다.
    안 그러면 카드 아홉 장을 다 지나야 되돌아갈 버튼이 나온다."""
    tiles = ['<button class="stile is-all" data-sec="" aria-pressed="true">'
             '<span class="st-num">✦</span><span class="st-t">전체 보기</span>'
             '<span class="st-s">모든 섹션을 한 줄로</span>'
             '<span class="st-n cnt">%d</span></button>' % total]
    for sid in order:
        (_id, num, title, sub), cs = secs[sid]
        tiles.append('<button class="stile" data-sec="%s" aria-pressed="false">'
                     '<span class="st-num">%s</span><span class="st-t">%s</span>'
                     '<span class="st-s">%s</span><span class="st-n cnt">%d</span></button>'
                     % (sid, num, title, snip(sub), len(cs)))
    # 주제를 고르면 타일이 사라지고 카드만 남는다 — 돌아올 길을 같이 둔다
    return '<div class="sec-pick sgrid">%s</div>%s' % (''.join(tiles), BACK if with_back else '')


def layer(secs, lede):
    """교차 인사이트 층. 카드 마크업은 gen_insightview가 만들고, 갈래 머리만 여기서 그린다 —
    단일 포스트 쪽 섹션과 같은 모양이어야 두 화면이 한 페이지로 읽힌다."""
    n = sum(len(cs) for _t, _s, cs in secs)
    body = []
    for i, (title, sub, cs) in enumerate(secs, 1):
        body.append('<section class="xsec"><div class="sec-head"><span class="sec-num">%02d</span>'
                    '<h2 class="sec-title">%s</h2></div>%s</section>'
                    % (i, title, ''.join(cs)))
    return ('<div class="xlayer" hidden><p class="xl-lede">%s</p>%s</div>'
            % ((lede % n) if '%d' in lede else lede, ''.join(body))), n


MODE_PICK = '''<div class="mode-pick sgrid">
    <button class="stile" data-mode="cross" aria-pressed="false">
      <span class="st-num">✦</span><span class="st-t">통합 인사이트</span>
      <span class="st-s">%s</span><span class="st-n">%d</span></button>
    <button class="stile" data-mode="single" aria-pressed="false">
      <span class="st-num">📄</span><span class="st-t">개별 포스트</span>
      <span class="st-s">%s</span><span class="st-n">%d</span></button>
  </div>'''


def upload_date(card):
    """카드 meta의 '업로드 YYYY-MM-DD' / '발행 YYYY-MM-DD' — 매체에 올라간 날이 기준이다"""
    for m in card.get('meta', []):
        d = re.search(r'(20\d\d-\d\d-\d\d)', m)
        if d:
            return d.group(1)
    return None


def rollup_for(key, cards, unit='편'):
    """data/rollup_notes_<key>.json의 산문 + 카드 업로드일로 센 건수 → 롤업 블록"""
    path = os.path.join(ROOT, 'data', 'rollup_notes_%s.json' % key)
    if not os.path.exists(path):
        return ''
    notes = json.load(io.open(path, encoding='utf-8'))
    # '*'는 전체, 그 밖은 카드 scope(kr·intl)별 — 리포트가 scope를 달면 그 범위만 센다
    counts = {'*': {}}
    for c in cards:
        d = upload_date(c)
        if not d:
            continue
        counts['*'][d] = counts['*'].get(d, 0) + 1
        sc = c.get('scope')
        if sc:
            counts.setdefault(sc, {})
            counts[sc][d] = counts[sc].get(d, 0) + 1
    return _rl.build(notes, counts, unit)


def render(cards, title, header, footer, out, rollup='', top='', top_css='',
           top_n=0, top_sub='', main_sub=''):
    """top이 있으면 첫 화면이 「교차 인사이트 / 단일 포스트」 두 버튼이 된다. 성격이 다른 두 글을
    한 화면에 쌓으면 어느 것을 읽는지 흐려진다. 되돌아갈 길은 「← 이전」 하나로 단계를 거슬러 간다."""
    secs, order = sections(cards)
    scoped = [c for c in cards if c.get('scope')]
    kr = len([c for c in scoped if c['scope'] == 'kr'])
    nav = sec_picker(secs, order, kr if scoped else len(cards), with_back=not top)
    tabs = ''
    if scoped:
        tabs = SCOPE_TABS % (kr, len(scoped) - kr, len(cards)) + '\n\n  '
    body = []
    for sid in order:
        (_, num, stitle, _sub), cs = secs[sid]
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2></div>%s</section>'
                    % (sid, num, stitle, ''.join(card_html(c) for c in cs)))
    page_css = css()
    if top_css:
        page_css = page_css.replace('</style>', top_css + '</style>')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n' % title + page_css
            # 그림 화살촉 defs는 페이지에 한 번만 — 카드마다 되풀이하지 않는다
            + '\n' + (FIG_DEFS if any(c.get('figs') for c in cards) else '')
            # 층이 없는 페이지는 예전 그대로 — 빈 줄만 새로 끼면 생성물 차이가 매번 남는다
            + '\n<div class="wrap">\n' + header
            + (('\n\n  ' + MODE_PICK % (top_sub, top_n, main_sub, len(cards))
                + '\n\n  ' + BACK + '\n\n  ' + top) if top else '')
            + '\n\n  ' + rollup + '\n\n  ' + tabs + nav + '\n\n  ' + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n'
            + FOLD_JS + NAV_JS + ui_bits.TOP_BTN + '\n')
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 섹션 %d개 -> %s' % (len(cards), len(order), out))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
    return html
