# -*- coding: utf-8 -*-
# 제3자 해설 대시보드 공용 부품 — 카드 마크업·추가 CSS·페이지 조립.
# 부동산·미주사·금융·회계사·건강이 같은 규칙을 쓰게 한 벌만 둔다.
# 기본 CSS는 언더스탠딩 대시보드의 <style>을 통째로 물려받는다(모든 페이지가 한 벌로 보이게).
#
# ── UI 규약 (새 대시보드·새 섹션을 만들 때도 그대로) ──────────────────────────
# 1. 페이지를 열면 **첫 화면은 섹션 타일**이다. 그 앞에 무엇을 읽을지 고르는 관문 버튼을
#    두지 않는다. 2026-08-17에 부동산만 관문을 하나 더 뒀다가 대시보드마다 첫 화면이
#    달라졌다. 성격이 다른 글(통합 인사이트)도 관문이 아니라 **타일 하나**로 넣는다.
# 2. 화면은 둘뿐이다 — 주제를 고르는 화면, 그 주제의 카드를 읽는 화면.
# 3. 되돌아가는 길은 「← 이전」 하나. 주제를 고른 뒤에만 나온다.
# 4. 카드가 없는 섹션은 <section data-fixed="1">로 표시한다. NAV_JS가 .ucard 대신
#    .ins로 세고, 국내·해외 범위 필터를 타지 않는다.
# 5. 조립은 반드시 render()를 거친다. render()가 check_ui()로 위 규약을 검사하고
#    어기면 파일을 쓰지 않는다. 페이지마다 손으로 조립하지 않는다.
# 새 대시보드는 gen_realestate_dashboard.py를 본떠 CARDS와 HEADER만 갈아 끼운다.
import io, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import rollup_lib as _rl
# 카드 마크업 표준은 scripts/card_lib.py 한 벌뿐이다 — 여기서는 가져다 쓴다
from card_lib import EXTRA_CSS, FIG_CSS, FIG_DEFS, slug, card_html, anchor_of  # noqa: F401,E501

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import ui_bits  # noqa: E402

# 기본 CSS 원천. 예전에는 「언더스탠딩 대시보드.html」의 <style>을 통째로 읽었는데,
# 그 페이지도 생성기로 만들게 되면 자기가 만들 파일을 읽는 순환이 된다. 파일로 떼어 둔다.
# 내용은 떼어낸 그대로다 — <style>로 시작해 </style>로 끝나서 아래 슬라이스가 그대로 먹는다.
SRC = os.path.join(ROOT, 'scripts', 'dash_base_css.html')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'

def blob(path):
    return BLOB + urllib.parse.quote(path)


# 주제 고르는 화면 ↔ 카드 읽는 화면 — 물려받는 CSS에는 없는 규칙만 여기서 더한다.
# .sgrid는 display:grid라 hidden 속성만으로는 안 사라진다. 그래서 [hidden] 규칙이 꼭 있어야 한다.
PICK_CSS = '''
  .sgrid[hidden], .sec-pick[hidden]{display:none}
  .sgrp[hidden]{display:none}
  .sgrp-t{font-size:11px;font-weight:850;letter-spacing:.05em;color:var(--ink-3);
          margin:16px 0 8px}
  .sgrp:first-of-type .sgrp-t{margin-top:12px}
  .sectpick[hidden], .sectp[hidden]{display:none}
  /* .stile는 display:flex라 [hidden] 속성만으로는 안 사라진다(같은 우선순위에서
     저자 스타일이 브라우저 기본 [hidden] 규칙을 이긴다) — .sgrid처럼 여기서 명시한다.
     검색 필터·빈 회사 타일 숨기기 둘 다 이 규칙이 있어야 실제로 화면에서 사라진다. */
  .stile[hidden]{display:none}
  .sectp-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:2px 0 12px}
  .sectp-t{font-size:12.5px;font-weight:850;color:var(--ink)}
  .sback{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 2px}
  .sback[hidden]{display:none}
  .sb-now{font-weight:800;font-size:13.5px}
  /* 섹션 안 두 갈래 버튼 — 회사를 고른 다음 무엇을 볼지 정한다 */
  .secsw{display:block;margin:14px 0 4px}
  .secsw .sw-btn{display:inline-flex;margin:0 8px 0 0}
  .secsw[hidden]{display:none}
  /* 색은 섹션 타일(.stile)과 같은 토큰을 쓴다 — 타일을 누르면 나오는 자리라 지면이
     같은 색이어야 한다. --card·--soft는 대시보드 절반에만 있는 토큰이라(부동산·통합
     인사이트) 없는 페이지에서는 배경이 통째로 비어 회색 지면이 그대로 비쳤다.
     그래서 --surface·--accent-soft로 되짚는 사슬을 건다 */
  .sw-btn{font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;padding:11px 20px;
          border:1px solid var(--line);border-radius:12px;
          background:var(--card,var(--surface,#fff));color:var(--ink)}
  .sw-btn:hover{border-color:var(--ink-3)}
  /* 고른 것에 색을 쓰지 않는다 — 섹션 타일(.stile)과 같은 규칙이다 */
  .sw-btn[aria-pressed="true"]{border-color:var(--ink-3);background:var(--sunk)}
  .sw-n{font-variant-numeric:tabular-nums;color:var(--ink-3);font-weight:700;margin-left:5px}
  /* 타일에 붙는 괴리 배지 — 그 회사의 가장 최근 평가가 주가보다 몇 % 위/아래인가.
     한국 시장 관행대로 위는 빨강, 아래는 파랑이다. 값이 없는 편(역산처럼 값을 안 내는
     방법)은 회색으로 방법 이름만 적는다 — 없는 숫자를 만들지 않는다 */
  .stile .st-gap{display:inline-block;margin-top:auto;padding-top:8px;font-size:12px;font-weight:850;
    font-variant-numeric:tabular-nums;letter-spacing:-.01em}
  .stile .st-gap.up{color:var(--risk)}
  .stile .st-gap.down{color:var(--accent)}
  .stile .st-gap.flat{color:var(--ink-3);font-weight:800}
  /* 숫자 앞의 말표 — 무엇과 견준 값인지 밝힌다. 값보다 작고 회색이라 숫자를 안 먹는다.
     「주가 대비 밸류에이션」으로 적는다. 「밸류에이션 대비 현재가」로 적으면 기준이 뒤집혀 부호가
     전부 반대가 된다 — 이 숫자는 필자가 낸 괴리율(내재가치가 주가보다 몇 % 위/아래)이다 */
  .stile .st-gap-l{display:inline;margin-right:5px;font-size:10.5px;font-weight:700;
    color:var(--ink-3);letter-spacing:0}
  .sv-val[hidden], .sv-posts[hidden]{display:none}
  /* 회사 검색창 — 타일 격자 바로 위. .sec-pick.sgrid(묶음 없는 페이지)에서는 검색창도
     그리드 항목이 되므로 grid-column으로 한 줄 전체를 차지하게 편다. 묶음이 있는 페이지는
     .sec-pick이 그리드가 아니라 그냥 컨테이너라 이 규칙이 없어도 한 줄로 선다. */
  .ssearch{grid-column:1/-1;display:flex;align-items:center;gap:10px;margin:0 0 14px}
  .ssearch .sq{flex:1;min-width:0;font:inherit;font-size:13.5px;padding:10px 14px;
    border:1px solid var(--line);border-radius:10px;
    background:var(--card,var(--surface,#fff));color:var(--ink)}
  .ssearch .sq::placeholder{color:var(--ink-3)}
  .ssearch .sq:focus{outline:none;border-color:var(--accent)}
  .ssearch .sq-n{font-size:12px;font-weight:700;color:var(--ink-3);white-space:nowrap;
    min-width:30px;text-align:right}
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
    if '.sback{' not in out:
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


def _card(c, dup=False, page_slug=''):
    """카드 마크업. 사본(다른 회사 섹션에 한 번 더 서는 것)은 앵커를 뗀다.

    page_slug가 있으면(카드마다 파일이 따로 있는 장) 머리가 그 파일로 가는 링크가 된다."""
    h = card_html(c, page_slug=page_slug)
    if dup:
        h = h.replace(' id="%s"' % anchor_of(c), '', 1)
    return h


def sections(cards, newest_first=False):
    """카드를 섹션별로 묶는다 — CARDS에 적힌 순서가 곧 화면 순서다.

    c['also'] = [섹션, …]이면 그 섹션에도 같은 카드가 선다. 마이크론과 SK하이닉스를 같이
    다룬 글은 두 회사 어느 쪽을 눌러도 나와야 한다. 두 번째 자리부터는 앵커(id)를 떼고
    낸다 — 같은 id가 문서에 둘이면 링크가 어디로 갈지 정해지지 않는다.

    newest_first=True면 **섹션 안에서만** 원문이 매체에 올라간 날의 역순으로 다시 세운다.
    글이 쌓이는 아카이브에서는 맨 위가 가장 최근 글이어야 한다. 섹션 차례는 건드리지 않는다 —
    섹션은 주제를 나눈 것이라 날짜와 무관하고, 여기까지 날짜로 흔들면 주제 배치가 매주 바뀐다.
    meta에 날짜가 없는 카드(연재 기간만 적은 것 등)는 그 섹션 맨 뒤로 가되 서로의 차례는 지킨다."""
    secs, order = {}, []
    for c in cards:
        for i, sec in enumerate([c['section']] + list(c.get('also') or ())):
            sid = sec[0]
            if sid not in secs:
                secs[sid] = (sec, [])
                order.append(sid)
            secs[sid][1].append((c, i > 0))
    if newest_first:
        for sid in order:
            sec, cs = secs[sid]
            # 날짜가 없으면 빈 문자열 — 내림차순에서 저절로 맨 뒤에 선다. 파이썬 sort는
            # 안정 정렬이라 날짜가 같거나 둘 다 없는 카드는 CARDS에 적힌 차례를 지킨다.
            secs[sid] = (sec, sorted(cs, key=lambda t: upload_date(t[0]) or '', reverse=True))
    return secs, order


def pick_tabs_html(items, cards):
    """위에 서는 갈래 탭. 카드의 scope 값으로 거른다 — 거르는 JS 는 국내·해외 탭과
    같은 것을 쓴다(c.dataset.scope). 이름과 갈래만 장마다 다르다.

    items = [(scope 값, 보일 이름), …]. 「전체」는 여기서 붙인다.
    비교는 한 화면에 병렬로 두고 탭은 고르는 데만 쓴다 — 견주는 층이 그 자리다."""
    b = []
    for key, label in items:
        n = len([c for c in cards if c.get('scope') == key])
        b.append('<button data-pick="%s" aria-pressed="false">%s <span class="cnt">%d</span>'
                 '</button>' % (key, label, n))
    b.append('<button data-pick="all" aria-pressed="true">전체 <span class="cnt">%d</span>'
             '</button>' % len(cards))
    return '<div class="scope-tabs">\n    ' + '\n    '.join(b) + '\n  </div>'


SCOPE_TABS = '''<div class="scope-tabs">
    <button data-pick="kr" aria-pressed="false">🇰🇷 국내 <span class="cnt">%d</span></button>
    <button data-pick="intl" aria-pressed="false">🌍 해외 <span class="cnt">%d</span></button>
    <button data-pick="all" aria-pressed="true">전체 <span class="cnt">%d</span></button>
  </div>'''

FOLD_JS = '''<script>
(function(){
  function toggle(card){
    var open=card.classList.toggle('is-open');
    var head=card.querySelector('.uc-head');
    if(head && head.getAttribute('role')==='button') head.setAttribute('aria-expanded', String(open));
    var caret=card.querySelector('.uc-caret');
    if(caret && caret.getAttribute('role')==='button') caret.setAttribute('aria-expanded', String(open));
    if(!open){
      var top=card.getBoundingClientRect().top;
      if(top<60) card.scrollIntoView({block:'start'});   // 접을 때 화면이 위로 튀지 않게
    }
  }
  // 카드마다 파일이 따로 있는 장에서는 머리가 그 글 페이지로 가는 링크다(data-href).
  // 캐럿만 그 자리에서 접고 편다 — 캐럿 클릭이 머리까지 올라가 페이지를 이동시키면 안 된다.
  document.addEventListener('click', function(e){
    var caret=e.target.closest('.uc-caret');
    if(caret){ e.stopPropagation(); toggle(caret.closest('.ucard')); return; }
    var head=e.target.closest('.uc-head');
    if(!head) return;
    if(head.dataset.href){ location.href = head.dataset.href; return; }
    toggle(head.closest('.ucard'));
  });
  document.addEventListener('keydown', function(e){
    if(e.key!=='Enter' && e.key!==' ') return;
    var caret=e.target.closest('.uc-caret');
    if(caret){ e.preventDefault(); e.stopPropagation(); toggle(caret.closest('.ucard')); return; }
    var head=e.target.closest('.uc-head');
    if(!head) return;
    e.preventDefault();
    if(head.dataset.href){ location.href = head.dataset.href; return; }
    toggle(head.closest('.ucard'));
  });
})();
</script>'''

# 카드 하나를 지목하는 링크를 성립시킨다. 앵커(id="card-…")는 처음부터 있었지만 페이지가
# 주소의 #을 보지 않았다 — 첫 화면이 타일 고르기라 모든 섹션이 hidden이고, 링크를 받은 사람은
# 타일 화면에 떨어졌다. 카드 안의 「같은 영상에서 나온 카드」도 같은 이유로 두 번 막혔다.
# 그래서 한 자리에서 처리한다: 섹션을 되살리고(「전체 보기」 타일을 눌러서) 카드를 펴고 그리로
# 간다. 「링크 복사」 버튼은 그 주소를 집어 준다.
LINK_JS = """<script>
(function(){
  function jump(id, smooth){
    var h=document.getElementById(id); if(!h) return;
    var card=h.closest('.ucard'), sec=h.closest('section');
    // 범위 탭이 국내에 놓여 있으면 해외 카드는 숨어 있다. 지목받은 카드부터 되살린다
    var tabs=document.querySelector('.scope-tabs');
    if(tabs && card && card.hidden){
      var allp=tabs.querySelector('button[data-pick="all"]');
      if(allp) allp.click();
    }
    if(sec && sec.hidden){
      // 섹션 타일을 눌러 그 섹션만 편다. 카드를 지목한 주소도 제 섹션 안에서 열린다.
      // 타일이 없는 섹션(묶음 밖)만 「전체 보기」로 푼다.
      var tile=document.querySelector('.sec-pick button[data-sec="'+sec.id+'"]');
      if(tile) tile.click();
      else {
        var all=document.querySelector('.stile.is-all');
        if(all) all.click();   // NAV_JS가 화면을 맨 위로 올린다
      }
    }
    setTimeout(function(){
      if(card && !card.classList.contains('is-open')){
        // head.click()으로 미루지 않는다 — 카드마다 파일이 따로 있는 장에서는 머리가
        // data-href를 달고 있어 클릭이 그 페이지로 이동해 버린다(FOLD_JS). 여기서는
        // 목록 페이지 안에서 그 자리 펼침만 하면 된다 — 직접 편다.
        card.classList.add('is-open');
        var head=card.querySelector('.uc-head');
        if(head && head.getAttribute('role')==='button') head.setAttribute('aria-expanded', 'true');
        var caret=card.querySelector('.uc-caret');
        if(caret && caret.getAttribute('role')==='button') caret.setAttribute('aria-expanded', 'true');
      }
      // 카드를 지목했으면 카드로, 섹션을 지목했으면 섹션 머리로 간다
      (card || h).scrollIntoView({behavior: smooth ? 'smooth' : 'auto', block:'start'});
    }, 140);
  }
  function fromHash(smooth){
    var id=(location.hash||'').slice(1);
    if(id) jump(decodeURIComponent(id), smooth);
  }
  document.addEventListener('click', function(e){
    var a=e.target.closest('a.kin-link');
    if(a){
      var href=a.getAttribute('href') || '';
      // 카드마다 파일이 따로 있는 장에서는 이 링크가 진짜 다른 문서를 가리킨다 —
      // 그때는 기본 이동에 맡긴다. #으로 시작하는 옛 앵커 링크만 여기서 대신 연다.
      if(href.charAt(0) === '#'){
        e.preventDefault();
        jump(href.slice(1), true);
      }
      return;
    }
    var b=e.target.closest('.uc-copy, .sec-copy'); if(!b) return;
    // 세 갈래다 — data-href(카드 단독 페이지를 가리키는 상대 주소) > data-anchor(같은 문서 안
    // 앵커) > 아무 표도 없으면(카드 단독 페이지 자신의 「링크 복사」) 지금 이 주소 그대로.
    var url;
    if(b.dataset.href){
      url = new URL(b.dataset.href, location.href).href;
    } else if(b.dataset.anchor){
      url = location.origin + location.pathname + '#' + encodeURIComponent(b.dataset.anchor);
    } else {
      url = location.origin + location.pathname;
    }
    var done=function(ok){
      b.textContent = ok ? '복사됨' : '주소창에 있습니다';
      setTimeout(function(){ b.textContent='링크 복사'; }, 1600);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(function(){ done(true); }, function(){ done(false); });
    } else {
      // 클립보드를 못 쓰는 환경(비보안 문맥)에서는 주소창에 띄워 손으로 집게 한다
      history.replaceState(null, '', url);
      done(false);
    }
  });
  // 링크를 받고 들어온 사람. 카드가 그려진 뒤라야 앵커를 찾는다
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', function(){ fromHash(false); });
  } else {
    fromHash(false);
  }
  window.addEventListener('hashchange', function(){ fromHash(true); });
})();
</script>"""

SW_JS = '<script>\n(function(){\n  function show(sid, view){\n    var sw=document.querySelector(\'.secsw[data-sec="\'+sid+\'"]\');\n    if(sw) sw.querySelectorAll(\'.sw-btn\').forEach(function(b){\n      b.setAttribute(\'aria-pressed\', String(b.dataset.view===view));\n    });\n    var val=document.querySelector(\'.sv-val[data-sec="\'+sid+\'"]\');\n    var posts=document.querySelector(\'.sv-posts[data-sec="\'+sid+\'"]\');\n    if(val) val.hidden = view!==\'val\';\n    if(posts) posts.hidden = view!==\'posts\';\n  }\n  document.addEventListener(\'click\', function(e){\n    var b=e.target.closest(\'.sw-btn\'); if(!b) return;\n    show(b.closest(\'.secsw\').dataset.sec, b.dataset.view);\n  });\n  // 카드를 지목한 주소로 들어오면 그 카드가 든 갈래를 펴 준다\n  function fromHash(){\n    var id=(location.hash||\'\').slice(1); if(!id) return;\n    var h=document.getElementById(decodeURIComponent(id)); if(!h) return;\n    var box=h.closest(\'.sv-posts\'); if(box) show(box.dataset.sec, \'posts\');\n  }\n  window.addEventListener(\'hashchange\', fromHash);\n  if(document.readyState===\'loading\'){\n    document.addEventListener(\'DOMContentLoaded\', fromHash);\n  } else { fromHash(); }\n})();\n</script>'


NAV_JS = '''<script>
(function(){
  var tabs=document.querySelector('.scope-tabs');   // 범위 탭은 국내·해외가 섞인 페이지에만 있다
  var box=document.querySelector('.sec-pick'); if(!box) return;
  var back=document.querySelector('.sback');
  var pick = 'all';   // 범위 탭이 있든 없든 처음 화면은 전체다
  // 화면이 둘이다. 주제를 고르는 화면과 그 주제의 카드를 읽는 화면.
  // 한 화면에 타일과 카드를 같이 두면 무엇을 보고 있는지 흐려진다.
  // 합류도 칸을 고른 상태(cell)는 세 번째 화면이다. 타일은 카드를 주제별로 나누고,
  // 칸은 주제를 가로질러 고른다 — 둘이 동시에 걸리면 나중 것이 앞의 것을 푼다.
  var only=null, picking=true, sect=null, q='', cell=null;
  var mbar=document.querySelector('.mg-b');
  var sq=document.querySelector('.ssearch .sq'), sqn=document.querySelector('.ssearch .sq-n');
  function norm(s){ return (s||'').replace(/\s+/g,' ').trim().toLowerCase(); }
  function opt(id){ return box.querySelector('button[data-sec="'+id+'"]'); }
  function apply(){
    // 카드를 숨기는 조건이 둘이다 — 범위 탭(국내·해외)과 합류도 칸.
    // 칸을 고르면 섹션을 가로질러 그 칸에 선 카드만 남는다.
    document.querySelectorAll('.ucard').forEach(function(c){
      var okScope = !c.dataset.scope || pick==='all' || c.dataset.scope===pick;
      var okCell = !cell || (' '+(c.dataset.cells||'')+' ').indexOf(' '+cell+' ')!==-1;
      c.hidden = !(okScope && okCell);
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
      // 카드가 없는 섹션(통합 인사이트)은 교차 카드로 센다. 범위 탭은 타지 않는다
      var live = s.hasAttribute('data-fixed')
                   ? (s.dataset.n ? parseInt(s.dataset.n, 10) : s.querySelectorAll('.ins').length)
                   : s.querySelectorAll('.ucard:not([hidden])').length;
      seen+=live;
      // 칸을 고른 화면에서는 카드가 남은 섹션만 선다. 섹션 하나를 고른 상태가 아니다.
      s.hidden = cell ? live===0 : (picking || live===0 || (only && s.id!==only));
      var o=opt(s.id);
      if(o){
        // 카드가 0편이라 원래 숨어 있던 타일은 검색해도 나오면 안 된다. 아래 검색 분기가
        // 이 표시를 보고 판단하므로, 검색 분기가 o.hidden을 다시 덮어써도 이 값은 남는다.
        o.dataset.empty = live===0 ? '1' : '';
        o.hidden = live===0;
        var c=o.querySelector('.cnt'); if(c) c.textContent=live;
      }
    });
    // 섹션 전용 층은 그 섹션을 고른 동안만 보인다. 갈래가 둘인 섹션은 버튼 줄만 먼저 펴고
    // 안쪽(지도·카드)은 사람이 고른 뒤에 편다.
    document.querySelectorAll('.secsw').forEach(function(w){
      w.hidden = !only || w.dataset.sec!==only;
      if(w.hidden) w.querySelectorAll('.sw-btn').forEach(function(b){
        b.setAttribute('aria-pressed','false');
      });
    });
    // 「전체 보기」는 회사를 안 고른 채 전부 읽는 화면이다(picking=false, only=null).
    // 갈래 버튼은 회사 하나를 고른 뒤에만 뜻이 있으므로 여기서는 글(.sv-posts)만 펴고
    // 지도(.sv-val)는 접어 둔다 — 회사 스물둘의 지도를 한꺼번에 펴면 첫 카드에 닿기까지
    // 스크롤이 수십 판이 된다. 이 갈래가 없던 동안 전체 보기에 제목만 나오고 카드가
    // 통째로 안 나왔다.
    var allView = !picking && !only;
    document.querySelectorAll('.sec-lead, .sv-posts').forEach(function(l){
      if(allView){ l.hidden = !l.classList.contains('sv-posts'); return; }
      var sw = document.querySelector('.secsw[data-sec="'+l.dataset.sec+'"]');
      if(!sw){ l.hidden = !only || l.dataset.sec!==only; return; }
      // 갈래가 있는 섹션은 버튼이 정한다. 섹션을 떠나면 둘 다 접는다.
      if(!only || l.dataset.sec!==only) l.hidden = true;
    });
    // 섹터 타일의 수는 그 안에 든 회사 수다. 카드 수를 합치면 한 회사를 여러 편으로 평가한
    // 섹터가 회사 많은 섹터처럼 보인다. 범위 탭에 걸려 숨은 회사는 빼고 세고, 하나도 안 남으면
    // 섹터째 숨긴다.
    box.querySelectorAll('.stile[data-secs]').forEach(function(t){
      var n=0;
      t.dataset.secs.split(',').forEach(function(id){
        var o=box.querySelector('.sectp .stile[data-sec="'+id+'"]');
        if(o && !o.hidden) n += 1;
      });
      t.hidden = n===0;
      var c2=t.querySelector('.cnt'); if(c2) c2.textContent=n;
    });
    // 범위 탭이나 빈 섹션 때문에 타일이 다 숨은 묶음은 이름만 남지 않게 같이 숨긴다
    box.querySelectorAll('.sgrp').forEach(function(g){
      g.hidden = g.querySelectorAll('.stile:not([hidden])').length===0;
    });
    // 화면은 셋이다 — 섹터 고르기, 그 섹터의 회사 고르기, 고른 회사 읽기.
    var pickBox=box.querySelector('.sectpick');
    if(pickBox){
      pickBox.hidden = !!sect;
      box.querySelectorAll('.sectp').forEach(function(pn){
        pn.hidden = !sect || pn.dataset.sect!==sect;
      });
    }
    // 검색어가 있으면 섹터 층을 건너뛴다. 회사 타일 글자(.st-t)로만 맞추고, 카드 0편이라
    // 이미 숨어 있던 타일(dataset.empty)은 글자가 맞아도 그대로 숨긴다.
    if(q){
      if(pickBox) pickBox.hidden = true;
      box.querySelectorAll('.sectp').forEach(function(pn){ pn.hidden = false; });
      var qn=0;
      box.querySelectorAll('.stile[data-sec]').forEach(function(t){
        if(!t.dataset.sec) return;   // 「전체 보기」 타일은 검색 대상이 아니다
        var tt=t.querySelector('.st-t');
        var match = t.dataset.empty!=='1' && norm(tt?tt.textContent:t.textContent).indexOf(q)!==-1;
        t.hidden = !match;
        if(match) qn++;
      });
      box.querySelectorAll('.sectp').forEach(function(pn){
        pn.hidden = pn.querySelectorAll('.stile[data-sec]:not([hidden])').length===0;
      });
      if(sqn) sqn.textContent = qn + '곳';
    } else if(sqn){
      sqn.textContent = '';
    }
    var all=opt(''); if(all){ var ac=all.querySelector('.cnt'); if(ac) ac.textContent=seen; }
    box.hidden = !picking;
    // 읽는 순서 안내는 첫 화면에만 둔다 — 섹션을 고르고 나면 그 섹션을 읽을 차례다
    var intro=document.querySelector('.intro');
    if(intro) intro.hidden = !picking;
    var roll2=document.querySelector('.rollup');
    if(roll2 && picking) roll2.hidden = false;   // 주제 고르는 화면에서는 롤업을 그대로 둔다
    if(mbar) mbar.querySelectorAll('.mcell').forEach(function(g){
      g.setAttribute('aria-pressed', String(g.dataset.cell===cell));
    });
    if(back){
      back.hidden = picking;
      var now=back.querySelector('.sb-now');
      if(now){
        var cur = only ? opt(only) : opt('');
        var t = cur && cur.querySelector('.st-t');
        var mg = cell && mbar ? mbar.querySelector('.mcell[data-cell="'+cell+'"]') : null;
        now.textContent = picking ? ''
          : (mg ? (mg.dataset.label || cell) : (t ? t.textContent : ''));
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
  // 화면이 바뀌면 히스토리에도 한 칸 쌓는다. 안 쌓으면 브라우저 뒤로가기가 「타일 고르기」로
  // 돌아가지 않고 대시보드 밖으로 나간다 — 섹션을 하나 열었을 뿐인데 페이지를 떠난다.
  // 주소는 그 섹션을 지목한 주소와 같은 것을 쓴다(#섹션id). 「링크 복사」와 한 몸이다.
  var quiet=false;                       // 뒤로가기로 되돌리는 중에는 다시 쌓지 않는다
  function mark(){
    if(quiet) return;
    var base = location.pathname + location.search;
    // 타일 고르기 화면은 주소에 #이 없다. 섹션을 고르면 그 섹션 주소, 「전체 보기」는 #all.
    var want = picking ? base : base + '#' + encodeURIComponent(only || 'all');
    // 카드를 지목한 주소로 들어온 사람의 주소는 덮지 않는다. LINK_JS가 그 카드를 열려고
    // 타일을 대신 눌러 주는데, 그때 여기가 #card-… 를 #섹션id 로 갈아치웠다. 그래서 새로
    // 고침하면 읽던 카드가 아니라 섹션 목록이 떴다(2026-08-23). 지금 주소가 이미 이 섹션
    // 안을 가리키고 있으면 그대로 둔다 -- 주소가 안 바뀌니 히스토리도 안 쌓인다.
    if(!picking && only && location.hash){
      var cur=document.getElementById(decodeURIComponent(location.hash.slice(1)));
      var host=cur && cur.closest('section');
      if(host && host.id===only) want = base + location.hash;
    }
    if(want !== base + location.hash) history.pushState({sec: only, picking: picking}, '', want);
  }
  // 섹터를 펴는 것도 화면 하나다. 주소에는 안 실리지만 상태로 한 칸 쌓아 두어야
  // 기기 뒤로가기가 섹터 고르기로 돌아온다 — 안 쌓으면 페이지째 나간다.
  function markSect(){
    if(quiet) return;
    history.pushState({sec: null, picking: true, sect: sect}, '',
                      location.pathname + location.search);
  }
  function restore(st){
    quiet = true;
    cell = null;        // 히스토리에는 섹션만 쌓는다 — 되돌아오면 칸 선택은 풀린다
    var stSect = (st && st.sect) || null;
    var id = (location.hash || '').slice(1);
    if(st && typeof st.picking === 'boolean'){
      picking = st.picking; only = st.sec || null;
    } else if(!id){
      // 처음 들어온 화면. 기본은 타일 고르기 — 카드가 쌓이는 아카이브에서는 고르는
      // 일이 먼저다. 감시 성격의 장(포트폴리오 워치)은 고르러 오는 게 아니라 바뀐
      // 것을 보러 오므로 전체 보기로 연다. render(home='all') 이 이 표시를 심는다.
      if(document.getElementById('home-all')){ picking = false; only = null; }
      else { picking = true; only = null; sect = null; }
    } else if(id === 'all'){
      picking = false; only = null;
    } else {
      var el = document.getElementById(decodeURIComponent(id));
      var sc = el && el.closest ? el.closest('section[id]') : null;
      picking = false; only = sc ? sc.id : null;
    }
    if(!only) sect = stSect;
    apply();
    // 타일 고르기로 돌아왔으면 주소의 #도 지운다. 남겨 두면 뒤이어 뜨는 hashchange를 받은
    // LINK_JS가 그 카드를 다시 열어 버려 뒤로가기가 제자리로 튕긴다.
    if(picking && location.hash){
      history.replaceState({sec: null, picking: true}, '', location.pathname + location.search);
    }
    quiet = false;
  }
  if(sq) sq.addEventListener('input', function(){
    q = norm(sq.value);
    sect = null;      // 검색어를 넣거나 지우면 섹터 고르기부터 다시 시작한다
    apply();
  });
  // 합류도 칸을 누르면 그 칸에 선 카드만 남는다. 같은 칸을 다시 누르면 푼다 —
  // 지도를 열어 둔 채로 되돌릴 길이 있어야 한다.
  function pickCell(g){
    cell = (g.dataset.cell===cell) ? null : g.dataset.cell;
    only=null; sect=null;
    picking = !cell;
    apply();
    if(cell){
      var first=document.querySelector('section[id]:not([hidden])');
      if(first) first.scrollIntoView({behavior:'smooth', block:'start'});
    }
  }
  if(mbar){
    mbar.addEventListener('click', function(e){
      var g=e.target.closest('.mcell'); if(g) pickCell(g);
    });
    mbar.addEventListener('keydown', function(e){
      if(e.key!=='Enter' && e.key!==' ') return;
      var g=e.target.closest('.mcell'); if(!g) return;
      e.preventDefault(); pickCell(g);
    });
  }
  box.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    cell=null;                      // 타일과 칸은 같은 자리를 쓴다 — 나중 것이 앞의 것을 푼다
    if(b.dataset.sect){ sect=b.dataset.sect; apply(); markSect(); window.scrollTo({top:0}); return; }
    only = b.dataset.sec || null;   // 전체 보기 타일이면 only=null 로 전부 편다
    if(!only) sect=null;            // 전체 보기에서 돌아오면 섹터 고르는 화면부터
    picking=false;
    apply();
    mark();
    var sec = only ? document.getElementById(only) : null;
    if(sec) sec.scrollIntoView({behavior:'smooth', block:'start'});
    else window.scrollTo({top:0, behavior:'smooth'});
  });
  window.addEventListener('popstate', function(e){
    restore(e.state);
    var id=(location.hash||'').slice(1);
    var el=id ? document.getElementById(decodeURIComponent(id)) : null;
    if(el) el.scrollIntoView({block:'start'});
    else box.scrollIntoView({block:'start'});
  });
  apply();
  // 링크를 받고 들어온 사람의 첫 화면은 LINK_JS가 연다. 여기서는 히스토리 첫 칸만 표시해 둔다
  history.replaceState({sec: null, picking: true}, '');
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


# 되돌아가는 길은 기기 뒤로가기 하나다 — 화면 안에 「← 이전」을 두지 않는다.
# 남는 것은 지금 어느 자리인지 알리는 이름표뿐이다.
BACK = '<div class="sback" hidden><span class="sb-now"></span></div>'

# 회사 검색창 — 타일 격자 바로 위, 같은 .sec-pick 컨테이너 안에 둔다. box.hidden = !picking를
# 같이 타게 하려는 것이다(타일 고르는 화면에만 있으면 된다). 관문이 아니다 — 아무것도 막지
# 않고 바로 아래에 타일이 그대로 있다. NAV_JS가 입력을 받아 섹터 층을 건너뛰고 회사 타일만
# 글자로 거른다.
def search_html(ph='회사 이름이나 종목코드로 찾기'):
    """검색창. 무엇을 찾는 장인지에 따라 안내 문구가 달라진다 — 회사 목록이 아닌 장에서
    「종목코드로 찾기」가 서 있으면 그 장이 무엇을 담았는지 잘못 알린다."""
    return ('<div class="ssearch"><input type="search" class="sq" '
            'placeholder="%s" aria-label="찾기">'
            '<span class="sq-n"></span></div>' % ph)


SEARCH_HTML = search_html()


def _as_tops(x):
    """고정 층 인자를 목록으로 편다. 튜플 하나로 준 예전 호출도 그대로 받는다."""
    if not x:
        return []
    if isinstance(x, tuple):
        return [x]
    return list(x)


def sec_picker(secs, order, total, extra=None, groups=None, badges=None, pick_top='',
               search_ph=''):
    """섹션을 네모 타일로 세운다 — 무엇이 몇 편 들었는지 접지 않고 보여 준다.

    extra는 카드가 아닌 섹션(통합 인사이트 등)을 맨 앞 타일로 세운다: (sid, 이름, 설명, 편수).
    별도 관문 버튼을 만들지 않는 것이 규약이다 — 페이지를 열면 어느 대시보드든 이 타일이 첫 화면이다.

    pick_top은 검색창 다음·타일 격자 앞에 서는 조각이다(회계사 장의 괴리 상위 5 보드 등).
    타일과 같은 .sec-pick 컨테이너 안에 두는 이유는 box.hidden = !picking을 같이 타게
    하려는 것이다 — 회사를 고르면 검색창·이 조각·타일이 함께 접힌다."""
    tiles = ['<button class="stile is-all" data-sec="" aria-pressed="true">'
             '<span class="st-num">✦</span><span class="st-t">전체 보기</span>'
             '<span class="st-s">모든 섹션을 한 줄로</span>'
             '<span class="st-n cnt">%d</span></button>' % total]
    # extra 는 (sid, 이름, 설명, 편수) 하나이거나 그런 튜플의 목록이다. 성격이 다른 고정 층이
    # 둘 이상이면 타일도 그만큼 선다 — 하나로 합치면 타일 이름이 안에 든 글과 어긋난다.
    for i, x in enumerate(_as_tops(extra)):
        xid, xtitle, xsub, xn = x[:4]
        tiles.append('<button class="stile" data-sec="%s" aria-pressed="false">'
                     '<span class="st-num">%02d</span><span class="st-t">%s</span>'
                     '<span class="st-s">%s</span><span class="st-n cnt">%d</span></button>'
                     % (xid, i, xtitle, snip(xsub), xn))
    def _gap(sid):
        # badges = {섹션 id: (표시할 값, up|down|flat, 마우스를 올리면 뜨는 기준)}
        b = (badges or {}).get(sid)
        if not b:
            return ''
        text, tone, tip = b
        # 값이 없는 편(flat)에는 말표를 안 단다 — 「주가 대비 역산」은 뜻이 안 닿는다
        lab = '' if tone == 'flat' else '<span class="st-gap-l">주가 대비 밸류에이션</span>'
        return ('<span class="st-gap %s" title="%s">%s%s</span>'
                % (tone, tip.replace('"', '&quot;'), lab, text))

    def _tile(sid):
        (_id, num, title, sub), cs = secs[sid]
        return ('<button class="stile" data-sec="%s" aria-pressed="false">'
                '<span class="st-num">%s</span><span class="st-t">%s</span>'
                '<span class="st-s">%s</span>%s<span class="st-n cnt">%d</span></button>'
                % (sid, num, title, snip(sub), _gap(sid), len(cs)))

    # 주제를 고르면 타일이 사라지고 카드만 남는다 — 돌아올 길을 같이 둔다
    if not groups:
        tiles.extend(_tile(sid) for sid in order)
        return ('<div class="sec-pick sgrid">%s%s%s</div>%s'
                % (search_html(search_ph) if search_ph else SEARCH_HTML, pick_top, ''.join(tiles), BACK))

    # 묶음이 있으면 「전체 보기」만 위에 두고 그 아래를 묶음별로 나눈다. 묶음 안이
    # (섹터, 설명, [sid…]) 꼴이면 섹터 타일이 한 겹 더 선다. 묶음·섹터에 안 들어간
    # 섹션이 있으면 화면에서 조용히 사라지므로 여기서 잡는다.
    sectored = any(sids and not isinstance(sids[0], str) for _lab, sids in groups)
    if sectored:
        sectors = [(lab, sec) for lab, sids in groups for sec in sids]
        placed = [sid for _lab, sec in sectors for sid in sec[2]]
    else:
        placed = [sid for _lab, sids in groups for sid in sids]
    missing = [sid for sid in order if sid not in placed]
    assert not missing, '섹션 묶음에 빠진 섹션: %s' % ', '.join(missing)
    unknown = [sid for sid in placed if sid not in secs]
    assert not unknown, '없는 섹션을 묶음에 넣었다: %s' % ', '.join(unknown)

    body = ['<div class="sgrid">%s</div>' % ''.join(tiles)]
    if not sectored:
        for label, sids in groups:
            inner = ''.join(_tile(sid) for sid in order if sid in sids)
            body.append('<div class="sgrp"><p class="sgrp-t">%s</p>'
                        '<div class="sgrid">%s</div></div>' % (label, inner))
        return ('<div class="sec-pick">%s%s%s</div>%s'
                % (search_html(search_ph) if search_ph else SEARCH_HTML, pick_top, ''.join(body), BACK))

    # 섹터 타일은 그 섹터에 든 섹션 id를 달고 다닌다 — 회사 수를 세는 것도, 눌렀을 때
    # 어느 회사를 펼지도 이 목록 하나로 정해진다.
    panels, no = [], 0
    for label, sids in groups:
        cells = []
        for name, sub, members in sids:
            no += 1
            sect_id = 'sect-%d' % no
            # 섹터에 든 회사 수다. 카드 수를 합치면 한 회사를 여섯 편으로 평가한 섹터가
            # 회사 여섯 곳인 섹터처럼 보인다. 카드가 하나도 없는 회사는 타일이 안 서므로 뺀다.
            n = sum(1 for sid in members if sid in secs)
            cells.append('<button class="stile" data-sect="%s" data-secs="%s" '
                         'aria-pressed="false">'
                         '<span class="st-num">%02d</span><span class="st-t">%s</span>'
                         '<span class="st-s">%s</span><span class="st-n cnt">%d</span></button>'
                         % (sect_id, ','.join(members), no, name, snip(sub), n))
            inner = ''.join(_tile(sid) for sid in order if sid in members)
            panels.append('<div class="sectp" data-sect="%s" hidden>'
                          '<div class="sectp-head">'
                          '<span class="sectp-t">%s</span></div>'
                          '<div class="sgrid">%s</div></div>' % (sect_id, name, inner))
        body.append('<div class="sgrp"><p class="sgrp-t">%s</p>'
                    '<div class="sgrid">%s</div></div>' % (label, ''.join(cells)))
    return ('<div class="sec-pick">%s%s<div class="sectpick">%s</div>%s</div>%s'
            % (search_html(search_ph) if search_ph else SEARCH_HTML, pick_top, ''.join(body), ''.join(panels), BACK))


# ── 합류도 ────────────────────────────────────────────────────────────────
# 섹션 타일은 카드를 주제별로 **나누는** 도구다. 합류도는 반대로, 주제를 **가로질러**
# 카드 여럿이 한 곳으로 모인다는 것을 그림 한 장으로 보인다. 설계는
# docs/superpowers/specs/2026-08-20-합류도-design.md, 원형은 insights/gen_insightview.py.
#
# 읽는 층이다 — 카드 본문은 한 글자도 안 고친다. 배정은 카드 제목 문자열로만 가리키고
# 그 제목이 없으면 생성이 멈춘다. 열은 셋으로 고정한다(넷째 열을 열면 지도가 조직도가 된다).
MERGE_COLS = (('outer', '바깥에서 오는 것'),
              ('price', '값을 정하는 곳'),
              ('merge', '합류하는 곳'))

# 열 셋의 자리(x, 폭, 칸 높이, 한 줄에 담을 글자 수). 좌표를 손으로 적지 않는다 —
# 주제를 더할 때 칸 개수만 달라지고 자리는 여기서 다시 계산된다.
_MGEO = {'outer': (8, 118, 40, 9), 'price': (248, 144, 40, 11), 'merge': (470, 162, 48, 12)}
_MJX = 210.0   # 바깥 칸들이 한 번 모이는 자리. 어느 바깥이 어느 값으로 가는지는
               # 주장한 적이 없다 — 짝을 그리면 없는 인과를 그리는 것이 된다.


def _mesc(s):
    return ((s or '').replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def _mwrap(s, n):
    """칸 라벨을 두 줄까지만 접는다. 세 줄이 되면 칸 높이를 넘는다."""
    if len(s) <= n:
        return [s]
    cut = s.rfind(' ', 0, n + 1)
    if cut < n // 2:
        cut = n
    head, tail = s[:cut].rstrip(), s[cut:].lstrip()
    return [head, tail[:n + 2] + ('…' if len(tail) > n + 2 else '')]


def merge_cells(m):
    """지도 한 장의 칸 목록 — [(칸 id, 열, 라벨, [카드 제목…])]."""
    out = []
    for col, _title in MERGE_COLS:
        if col == 'merge':
            label, titles = m['merge']
            out.append(('%s-merge' % m['id'], col, label, titles))
            continue
        for i, (label, titles) in enumerate(m.get(col) or ()):
            out.append(('%s-%s%d' % (m['id'], col, i), col, label, titles))
    return out


def merge_svg(m):
    """지도 한 장. 칸은 누를 수 있고, 누르면 그 칸에 선 카드만 남는다."""
    bycol = {}
    for cid, col, label, titles in merge_cells(m):
        bycol.setdefault(col, []).append((cid, label, titles))
    tot = {}
    for col, _t in MERGE_COLS:
        _x, _w, bh, _n = _MGEO[col]
        k = len(bycol.get(col, []))
        tot[col] = k * bh + (k - 1) * 14 if k else 0
    span = max(tot.values())
    cy = 44 + span / 2.0
    H = int(44 + span + 20)
    h = ['<svg viewBox="0 0 640 %d" role="group" aria-label="%s 합류도">'
         % (H, _mesc(m['title']))]
    for col, title in MERGE_COLS:
        x, w, _bh, _n = _MGEO[col]
        h.append('<text x="%.0f" y="22" text-anchor="middle" class="m-col">%s</text>'
                 % (x + w / 2.0, _mesc(title)))
    tops = {}
    for col, _title in MERGE_COLS:
        x, w, bh, cw = _MGEO[col]
        y0 = cy - tot[col] / 2.0
        for i, (cid, label, titles) in enumerate(bycol.get(col, [])):
            y = y0 + i * (bh + 14)
            tops[cid] = (x, y, w, bh)
            lines = _mwrap(label, cw)
            ty = y + bh / 2.0 - (len(lines) - 1) * 7 + 4
            h.append('<g class="mcell%s" data-cell="%s" data-label="%s" role="button" '
                     'tabindex="0" aria-pressed="false" aria-label="%s — 카드 %d장">'
                     % (' is-merge' if col == 'merge' else '', _mesc(cid),
                        _mesc(label), _mesc(label), len(titles)))
            h.append('<title>%s — 카드 %d장</title>' % (_mesc(label), len(titles)))
            h.append('<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="9"/>' % (x, y, w, bh))
            for j, line in enumerate(lines):
                h.append('<text x="%.0f" y="%.0f" text-anchor="middle" class="m-lab">%s</text>'
                         % (x + w / 2.0, ty + j * 14, _mesc(line)))
            h.append('</g>')
    ox, ow, _obh, _n = _MGEO['outer']
    px, pw, _pbh, _n2 = _MGEO['price']
    mx, _mw, _mbh, _n3 = _MGEO['merge']
    for cid, _l, _t in bycol.get('outer', []):
        _x, y, _w, bh = tops[cid]
        h.append('<path class="mflow" d="M%.0f %.0f L%.0f %.0f"/>'
                 % (ox + ow, y + bh / 2.0, _MJX, cy))
    for cid, _l, _t in bycol.get('price', []):
        _x, y, _w, bh = tops[cid]
        h.append('<path class="mflow" d="M%.0f %.0f L%.0f %.0f"/>'
                 % (_MJX, cy, px, y + bh / 2.0))
        h.append('<path class="mflow" d="M%.0f %.0f L%.0f %.0f"/>'
                 % (px + pw, y + bh / 2.0, mx, cy))
    h.append('<circle class="mdot" cx="%.0f" cy="%.0f" r="3.5"/>' % (_MJX, cy))
    h.append('</svg>')
    return ''.join(h)


def merge_layer(maps, cards):
    """합류도 층을 만들고 카드에 c['cells']를 채운다.

    접힌 채로 선다 — 첫 화면은 어느 장이든 섹션 타일이다(UI 규약 1). intro와 함께
    타일 위에 두고, extra_css에 MERGE_CSS를 같이 넘긴다.

    가리킨 제목이 카드에 없으면 여기서 멈춘다. 한 지도 안에서 같은 카드가 두 칸에 서는 것도
    막는다 — 카드 하나가 바깥이면서 합류점일 수는 없다. 지도가 여럿이면 겹쳐 서도 된다."""
    if not maps:
        return ''
    known = {c['title']: c for c in cards}
    for c in cards:
        c['cells'] = []
    for m in maps:
        seen = {}
        assert m.get('merge') and m['merge'][1], '합류 칸이 비었다: %s' % m['id']
        assert m.get('outer') or m.get('price'), '바깥·값 칸이 하나도 없다: %s' % m['id']
        for cid, _col, label, titles in merge_cells(m):
            assert titles, '빈 칸이 있다: %s / %s' % (m['id'], label)
            for t in titles:
                assert t in known, '합류도가 없는 카드를 가리킨다: %s' % t
                assert t not in seen, ('한 지도에서 같은 카드가 두 칸에 섰다: %s (%s · %s)'
                                       % (t, seen.get(t), label))
                seen[t] = label
                known[t]['cells'].append(cid)
    h = ['<details class="mrg"><summary><span class="mg-t">합류도</span>'
         '<span class="mg-s">주제 %d개 — 카드가 어디로 모이는지 먼저 보고 들어갑니다</span>'
         '</summary><div class="mg-b">' % len(maps)]
    for m in maps:
        h.append('<div class="mg-one"><p class="mg-h">%s</p><p class="mg-l">%s</p>%s</div>'
                 % (_mesc(m['title']), _mesc(m['lede']), merge_svg(m)))
    h.append('<p class="mg-n">칸을 누르면 그 칸에 선 카드만 남습니다. 가운데 점은 바깥 조건이 '
             '한 번 모이는 자리입니다 — 어느 바깥이 어느 값으로 가는지는 이 그림이 정하지 '
             '않습니다.</p></div></details>')
    return ''.join(h)


MERGE_CSS = '''
  .mrg{margin:0 0 14px;border:1px solid var(--line);border-radius:10px;
    background:var(--surface);padding:0 16px}
  .mrg>summary{list-style:none;cursor:pointer;padding:13px 0;display:flex;
    align-items:baseline;gap:10px;flex-wrap:wrap}
  .mrg>summary::-webkit-details-marker{display:none}
  .mrg>summary::after{content:"\\25be";margin-left:auto;color:var(--ink-3);font-size:12px}
  .mrg[open]>summary::after{content:"\\25b4"}
  .mg-t{font-size:14px;font-weight:800;color:var(--ink)}
  .mg-s{font-size:12px;color:var(--ink-3)}
  .mg-b{padding:0 0 16px}
  .mg-one+.mg-one{margin-top:22px;padding-top:18px;border-top:1px solid var(--line)}
  .mg-h{margin:0 0 3px;font-size:13.5px;font-weight:800;color:var(--ink)}
  .mg-l{margin:0 0 10px;font-size:12.5px;line-height:1.6;color:var(--ink-2)}
  .mg-n{margin:14px 0 0;font-size:11.5px;line-height:1.6;color:var(--ink-3)}
  .mg-b svg{width:100%;height:auto;display:block}
  .m-col{font-size:11px;font-weight:850;fill:var(--ink-3);letter-spacing:.02em}
  .m-lab{font-size:11.5px;font-weight:800;fill:var(--ink)}
  .mflow{stroke:var(--line);stroke-width:1.4;fill:none}
  .mdot{fill:var(--ink-2)}
  .mcell{cursor:pointer}
  .mcell rect{fill:var(--surface);stroke:var(--ink-2);stroke-width:1.4;
    transition:stroke .15s,fill .15s}
  .mcell.is-merge rect{stroke:var(--accent);stroke-width:2.2}
  .mcell:hover rect,.mcell:focus rect{fill:var(--accent-soft);stroke:var(--accent)}
  .mcell:focus{outline:none}
  .mcell[aria-pressed="true"] rect{fill:var(--accent-soft);stroke:var(--accent);stroke-width:2.4}
'''


def layer(secs, lede):
    """교차 인사이트를 섹션 하나로 만든다 — 다른 대시보드와 첫 화면이 같아야 하므로
    따로 서는 층이 아니라 주제 타일 중 하나로 들어간다. 안의 갈래는 소제목으로만 나눈다."""
    n = sum(len(cs) for _t, _s, cs in secs)
    body = []
    for title, _sub, cs in secs:
        body.append('<div class="xsec"><h3 class="xsec-t">%s</h3>%s</div>'
                    % (title, ''.join(cs)))
    return ('<p class="xl-lede">%s</p>%s'
            % ((lede % n) if '%d' in lede else lede, ''.join(body))), n


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


# ── 읽는 순서(「처음 오셨다면」) ──────────────────────────────────────────────
# 처음 온 사람이 어디서부터 읽을지 정해 두는 층. 섹션 순서와 읽는 순서는 다르다 — 섹션은
# 주제를 나눈 것이고, 읽는 순서는 아무것도 모르는 사람이 밟아야 덜 걸리는 계단이다.
#
# 자리는 섹션 타일 그리드 바깥, 그 위다. 타일 하나로 들어가면 「전체 보기」와 같은 줄에 서서
# 주제 중 하나로 읽힌다. 이건 주제가 아니라 길잡이라 타일 위에 따로 선다. 관문은 아니다 —
# 접을 수 있고 바로 아래에 타일이 그대로 있다.
#
# steps는 [(단계 이름, 왜 이 자리인가, [카드 제목…])]. 카드 제목이 CARDS와 한 글자라도
# 어긋나면 assert로 걸리고, 빠뜨린 카드도 같이 걸린다 — 카드를 새로 만들면 여기에도 자리를
# 정해 줘야 한다.
_STEP_KO = {2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟'}

COURSE_CSS = '''
  .intro { margin:0 0 22px; border:1px solid var(--line); border-radius:10px;
    background:var(--sunk); padding:0 16px; }
  .intro > summary { list-style:none; cursor:pointer; padding:13px 0; display:flex;
    align-items:baseline; gap:10px; flex-wrap:wrap; }
  .intro > summary::-webkit-details-marker { display:none; }
  .intro > summary::after { content:"▾"; margin-left:auto; color:var(--ink-3); font-size:12px; }
  .intro[open] > summary::after { content:"▴"; }
  .in-t { font-size:14px; font-weight:800; color:var(--ink); }
  .in-s { font-size:12px; color:var(--ink-3); }
  .in-b { padding:0 0 16px; }
  .in-lede { margin:0 0 16px; font-size:13px; line-height:1.7; color:var(--ink-2); }
  .csteps { display:grid; grid-template-columns:1fr 1fr; gap:18px 26px; }
  @media (max-width:720px) { .csteps { grid-template-columns:1fr; } }
  .cs-h { margin:0 0 4px; font-size:14px; font-weight:800; color:var(--ink); }
  .cs-h .cs-n { display:inline-block; min-width:20px; color:var(--accent-ink); }
  .cs-why { margin:0 0 8px 20px; font-size:12.5px; line-height:1.6; color:var(--ink-2); }
  .course { margin-left:20px; }
  .course ol { margin:0; padding-left:17px; }
  .course li { font-size:12.5px; line-height:1.65; margin-bottom:3px; }
  .course li:last-child { margin-bottom:0; }
  .course a.kin-link { color:var(--ink); text-decoration:none;
    border-bottom:1px solid var(--line); }
  .course a.kin-link:hover { border-bottom-color:var(--accent); }
'''


def by_frag(cards, frags):
    """짧은 조각으로 카드 제목을 찾아 돌려준다.

    읽는 순서(course)는 제목을 그대로 적어야 하는데, 카드 제목에는 연작 표시 같은 태그가
    섞여 있어 손으로 옮기면 어긋난다. 조각 하나가 카드 둘을 가리키거나 하나도 못 가리키면
    여기서 멈춘다 — 조용히 엉뚱한 카드가 걸리는 것보다 낫다."""
    out = []
    for f in frags:
        hits = [c['title'] for c in cards if f in c['title']]
        assert len(hits) == 1, ('읽는 순서의 조각이 카드 하나를 못 가리킨다: %r — %d건 %s'
                                % (f, len(hits), [h[:30] for h in hits]))
        out.append(hits[0])
    return out


def course(cards, steps, lede):
    """읽는 순서를 render(intro=…)에 넣을 한 덩어리로 만든다. lede에 %d 하나(카드 수)."""
    have = {c['title'] for c in cards}
    listed = [t for _h, _w, ts in steps for t in ts]
    missing = have - set(listed)
    unknown = [t for t in listed if t not in have]
    assert not unknown, '읽는 순서에 없는 카드 제목이 있다: %s' % unknown
    assert not missing, '읽는 순서에서 빠진 카드가 있다: %s' % sorted(missing)
    assert len(listed) == len(set(listed)), '읽는 순서에 같은 카드가 두 번 들어갔다'

    h = ['<details class="intro" open><summary><span class="in-t">처음 오셨다면</span>'
         '<span class="in-s">카드 %d장을 %s 단계로</span></summary><div class="in-b">'
         % (len(cards), _STEP_KO[len(steps)])]
    h.append('<p class="in-lede">%s</p><div class="csteps">' % (lede % len(cards)))
    for i, (head, why, titles) in enumerate(steps, 1):
        h.append('<div class="cstep"><p class="cs-h"><span class="cs-n">%d</span>%s</p>' % (i, head))
        h.append('<p class="cs-why">%s</p>' % why)
        # 제목은 카드에 있는 글을 그대로 옮긴 것이라 산문 검사에서 빼는 자리다(class="course")
        h.append('<div class="course"><ol>%s</ol></div></div>'
                 % ''.join('<li><a class="kin-link" href="#%s">%s</a></li>' % (slug(t), t)
                           for t in titles))
    h.append('</div></div></details>')
    return ''.join(h)


def sec_copy(sid):
    """섹션 하나를 지목하는 주소를 집어 가는 버튼. 카드가 아닌 층(지도·밸류에이션)도 링크로
    보낼 수 있어야 한다 — 카드 링크는 uc-copy, 섹션 링크는 이것이다. LINK_JS가 둘을 같이 받는다."""
    return '<button type="button" class="sec-copy" data-anchor="%s">링크 복사</button>' % sid


XSEC = 'sec-cross'      # 통합 인사이트 섹션 id — 카드가 없는 섹션이라 NAV_JS가 따로 센다


def _has_figs(c):
    """카드에 그림이 있는지 — 있으면 카드 단독 페이지에 FIG_DEFS(화살촉·해칭 defs)를 싣는다.

    보통은 c['figs']에 있지만, 번호글(post)·보고서(report) 카드는 그림이 항목 사이에
    직접 낀다 — report 블록 안 ('fig', …) 항목까지 본다."""
    if c.get('figs'):
        return True
    for block in c.get('report') or ():
        if block and block[0] == 'fig':
            return True
    d = c.get('debate')
    if d and d.get('figs'):
        return True
    return False


def _write_card_pages(cards, title, footer, out, page_slug, page_css):
    """카드마다 그 글만 있는 페이지를 하나씩 쓴다 — 대시보드/<page_slug>/<카드슬러그>.html.

    껍데기는 대시보드와 같은 page_css(css() + extra_css)다. 몸은 그 카드 하나를 펼친 채로
    (card_html(c, standalone=True)) 내고, 머리에 대시보드로 돌아가는 「← 장」 링크를 단다.
    FOLD_JS·NAV_JS·SW_JS는 안 싣는다 — 접을 것도 고를 것도 없는 페이지다. LINK_JS만 실어
    「링크 복사」가 이 페이지 자신의 주소를 집게 한다.

    page_slug가 비어 있으면(호환) 아무것도 안 쓰고 0을 돌려준다."""
    if not page_slug:
        return 0
    dash_name = os.path.basename(out)
    out_dir = os.path.join(os.path.dirname(out), page_slug)
    os.makedirs(out_dir, exist_ok=True)
    seen, n = set(), 0
    for c in cards:
        t = c['title']
        if t in seen:      # 'also'로 다른 섹션에도 서는 카드는 원본 목록에서 한 번만 온다
            continue
        seen.add(t)
        sid = c['section'][0]
        body = card_html(c, standalone=True)
        fig_defs = FIG_DEFS if _has_figs(c) else ''
        page = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                '<title>%s · %s</title>\n' % (t, title) + page_css
                + '\n' + fig_defs
                + '\n<div class="wrap">\n'
                + '<a class="pback" href="../%s#%s">← %s</a>\n' % (dash_name, sid, title)
                + body
                + '\n\n  <footer>' + footer + '</footer>\n</div>\n'
                + LINK_JS + '\n')
        io.open(os.path.join(out_dir, '%s.html' % slug(t)), 'w', encoding='utf-8').write(page)
        n += 1
    # 없어진 카드의 글 페이지를 걷는다. 새로 쓰기만 하면 지운 카드의 주소가 계속 살아
    # 있어서, 대시보드에 없는 글이 링크로만 열린다(2026-08-31 Semi Doped 에서 그랬다)
    keep = {'%s.html' % slug(t) for t in seen}
    for f in os.listdir(out_dir):
        if f.endswith('.html') and f not in keep:
            os.remove(os.path.join(out_dir, f))
            print('  걷음 · %s' % f)
    print('  글 페이지 %d장 -> 대시보드/%s/' % (n, page_slug))
    return n


def render(cards, title, header, footer, out, rollup='', top='', extra_css='', tops=None,
           search_ph='',
           top_n=0, top_sub='', top_title='통합 인사이트', top_id='', intro='', sec_top=None,
           sec_bottom=None, sec_groups=None, sec_badges=None, pick_top='',
           sec_fig=None, newest_first=False,
           sw_labels=('밸류에이션', '개별 포스트'), page_slug='', home='pick',
           pick_tabs=None, tiles=True):
    """대시보드 한 장을 조립한다. **첫 화면은 어느 페이지든 섹션 타일이다** — 그 앞에 관문
    버튼을 두지 않는다. top(통합 인사이트)이 있으면 타일 하나가 더 서고, 나머지 주제와 똑같이
    눌러서 열고 「← 이전」으로 돌아온다. 새 대시보드를 만들 때도 이 함수를 통해서만 조립한다.

    tops = [(sid, 제목, 설명, 편수, html), …]. 카드 없는 고정 층이 둘 이상인 장에서 쓴다.
    top= 하나로는 성격이 다른 글 둘을 한 타일에 밀어 넣게 되어 타일 이름이 안과 어긋난다.
    top= 와 같이 주면 top 이 맨 앞에 선다.

    intro는 타일 그리드 위에 서는 안내다(읽는 순서 등). 관문이 아니다 — 아무것도 막지 않고
    접을 수 있으며 바로 아래에 타일이 그대로 있다. 섹션을 고르고 나면 스스로 접힌다.

    sec_fig = {섹션 id: HTML}. 스위치 없이 섹션 머리 바로 아래 늘 서 있는 층이다 —
    그림처럼 고르는 대상이 아니라 그 섹션을 읽는 순서를 먼저 보여 주는 것에 쓴다.
    sec_top 과 달리 「밸류에이션·개별 포스트」 버튼을 만들지 않는다.
    sec_top = {섹션 id: HTML}. 그 섹션 머리 바로 아래, 카드 앞에 들어간다. 한 회사를 여러 편으로
    평가한 것을 견주는 지도처럼 **그 섹션에만 해당하는** 층을 둘 자리다. 페이지 맨 위 롤업으로
    두면 회사 하나 이야기가 전체 보기 맨 앞에 서서 같은 내용이 두 군데 있는 것처럼 읽힌다.

    pick_top은 검색창 다음·타일 격자 앞에 서는 조각이다(sec_picker에 그대로 넘긴다). rollup과
    달리 타일과 한 컨테이너(.sec-pick) 안에 있어 회사를 고르면 같이 접힌다.

    newest_first는 글이 쌓이는 아카이브 장에서 켠다 — 섹션 안 카드를 원문 업로드일 역순으로
    세운다. 교재처럼 읽는 차례가 정해진 장(모델 가이드·알고리즘 계보·수도리무브)에서는 끈다.

    tiles=False면 섹션 타일 층을 아예 안 낸다. pick_tabs 와 같은 축을 고르는 장에서
    둘을 다 두면 같은 일을 두 번 시키는 계층이 된다 — 하나만 남긴다. 카드를 거르는 일은
    타일보다 먼저 일어나므로(apply 앞머리) 탭은 그대로 돈다.

    pick_tabs=[(scope값, 이름), …]이면 위에 그 갈래로 탭을 세운다. 국내·해외 범위 탭
    자리를 장이 가져다 쓰는 것이고, 거르는 것은 같은 JS(카드의 scope)다. 권역처럼
    **고르는** 축에만 쓴다 — 견주는 것은 탭이 아니라 한 화면 병렬이다(견주기 층).

    home='all'이면 처음 들어온 사람에게 타일 고르기 대신 **전체 보기**를 낸다. 타일은
    그대로 위에 서서 필터 노릇을 한다 — 규약(첫 화면에 섹션 타일이 선다)은 지켜진다.
    카드가 쌓이는 아카이브는 고르는 일이 먼저라 기본은 'pick'이다. 감시 성격의 장은
    고르러 오는 게 아니라 바뀐 것을 보러 오므로 'all'을 쓴다.

    page_slug가 있으면 카드마다 따로 파일을 쓴다(대시보드/<page_slug>/<카드슬러그>.html) —
    누르면 그 글만 있는 페이지로 간다. 비면(기본값) 지금까지처럼 목록 페이지 안에서만 접혔다
    편다. 값은 scripts/gen_site.py의 PAGES와 같은 슬러그를 쓴다."""
    secs, order = sections(cards, newest_first)
    scoped = [c for c in cards if c.get('scope')]
    kr = len([c for c in scoped if c['scope'] == 'kr'])
    # 카드가 없는 층(통합 인사이트·밸류에이션 지도)도 타일 하나로 선다. id를 바꿀 수 있게 둔다 —
    # 한 저장소에 성격이 다른 고정 층이 여럿이라 sec-cross 하나로는 안 된다.
    tid = top_id or XSEC
    # tops = [(sid, 제목, 설명, 편수, html), …]. 성격이 다른 고정 층이 둘 이상인 장에서 쓴다 —
    # 로봇 보고서와 AI 비즈니스 리포트를 한 타일에 넣으면 타일 이름이 안과 어긋난다.
    layers = list(tops or [])
    if top:
        layers.insert(0, (tid, top_title, top_sub, top_n, top))
    extra = [l[:4] for l in layers] or None
    # 처음 화면이 「전체」라 타일에 적히는 수도 전체다(JS가 범위를 바꿀 때 다시 센다)
    nav = sec_picker(secs, order, len(cards) + sum(l[3] for l in layers), extra,
                     groups=sec_groups, badges=sec_badges, pick_top=pick_top,
                     search_ph=search_ph) if tiles else ''
    tabs = ''
    if pick_tabs:
        # 장이 스스로 갈래를 정한 경우. 국내·해외 대신 그 갈래로 탭을 세운다
        tabs = pick_tabs_html(pick_tabs, cards) + '\n\n  '
    elif scoped:
        tabs = SCOPE_TABS % (kr, len(scoped) - kr, len(cards)) + '\n\n  '
    body = []
    for i, (lid, ltitle, _lsub, ln, lhtml) in enumerate(layers):
        # 카드가 없는 섹션이라 data-fixed로 표시한다 — 국내·해외 범위 필터도 타지 않는다
        # data-n은 이 층이 몇 편을 담고 있는지다. 카드가 없으니 세어 볼 수가 없다.
        body.append('<section id="%s" data-fixed="1" data-n="%d"><div class="sec-head">'
                    '<span class="sec-num">%02d</span><h2 class="sec-title">%s</h2>%s</div>%s</section>'
                    % (lid, ln, i, ltitle, sec_copy(lid), lhtml))
    sec_top, sec_bottom = sec_top or {}, sec_bottom or {}
    sec_fig = sec_fig or {}
    unknown = [k for k in list(sec_top) + list(sec_bottom) + list(sec_fig)
               if k not in secs]
    assert not unknown, 'sec_top·sec_bottom에 없는 섹션 id가 있다: %s' % unknown
    for sid in order:
        (_, num, stitle, _sub), cs = secs[sid]
        # 카드가 먼저다. 지도처럼 여러 편을 견주는 층은 sec_bottom으로 카드 뒤에 둔다 —
        # 앞에 두면 「전체 보기」를 열었을 때 글 대신 도구가 먼저 나온다.
        lead = sec_top.get(sid, '')
        cards_html = ''.join(_card(c, dup, page_slug) for c, dup in cs)
        if lead:
            # 섹션 안이 두 갈래다. 회사를 고르면 버튼 둘만 보이고, 누른 쪽만 펴진다.
            # 지도와 카드를 한 화면에 같이 쌓으면 회사 하나가 스크롤 여러 판이 된다.
            lead = ('<div class="secsw" data-sec="' + sid + '" hidden>'
                    '<button type="button" class="sw-btn" data-view="val">%s</button>'
                    '<button type="button" class="sw-btn" data-view="posts">%s'
                    ' <span class="sw-n">%d</span></button></div>'
                    '<div class="sec-lead sv-val" data-sec="%s" hidden>%s</div>'
                    % (sw_labels[0], sw_labels[1], len(cs), sid, lead))
            cards_html = '<div class="sv-posts" data-sec="%s" hidden>%s</div>' % (sid, cards_html)
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2>%s</div>%s%s%s%s</section>'
                    % (sid, num, stitle, sec_copy(sid), sec_fig.get(sid, ''), lead,
                       cards_html, sec_bottom.get(sid, '')))
    # 카드끼리 잇는 링크가 하나도 없는 페이지에는 스크립트를 싣지 않는다
    page_css = css()
    if extra_css:
        page_css = page_css.replace('</style>', extra_css + '</style>')
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n' % title + page_css
            # 그림 화살촉 defs는 페이지에 한 번만 — 카드마다 되풀이하지 않는다
            + '\n' + (FIG_DEFS if any(c.get('figs') for c in cards) else '')
            + '\n<div class="wrap">\n' + header
            # 타일이 롤업보다 먼저다. 회계사 장은 롤업 자리에 드라이버 지도가 들어 있어
            # 타일이 화면 한참 아래로 밀렸다(2026-08-18). 첫 화면은 어느 장이든 타일이다.
            # home='all' 표시. NAV_JS 가 처음 들어온 화면을 정할 때 이걸 본다
            + ('\n<div id="home-all" hidden></div>' if home == 'all' else '')
            + '\n\n  ' + intro + '\n\n  ' + tabs + nav + '\n\n  ' + rollup + '\n\n  ' + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n'
            + FOLD_JS + NAV_JS + LINK_JS + SW_JS + ui_bits.TOP_BTN + '\n')
    check_labels(cards)
    check_links(cards)
    check_ui(html, bool(layers), tiles)
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 섹션 %d개 -> %s' % (len(cards), len(order) + len(layers), out))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
    _write_card_pages(cards, title, footer, out, page_slug, page_css)
    return html


# 카드 라벨(섹션 제목·topic)에 회사 이름을 달 때 지키는 규칙. 2026-08-18에 삼성전자·SK하이닉스
# 공동 원문과 반도체 3사 원문을 「SK하이닉스」 섹션에 밀어 넣어 카드 제목과 안이 어긋났다.
# 섹션을 먼저 세우고 카드를 거기 맞추면 이렇게 된다. 사람이 눈으로 지키지 말고 여기서 막는다.
#
# 두 가지를 본다.
#   ① 라벨에 있는 회사가 원문에도 카드 제목에도 없다        — 남의 회사 이름을 달았다
#   ② 원문이 여러 회사를 다루는데 라벨은 그중 하나만 달았다  — 남의 글을 한 회사 것으로 좁혔다
# ②는 라벨이 회사 이름을 하나라도 달았을 때만 본다. 주제어로만 된 라벨(공급·세금·염증)은 대상이 아니다.
ACTORS = ('삼성전자', 'SK하이닉스', '마이크론', '엔비디아', 'TSMC', '애플', '테슬라',
          '마이크로소프트', '알파벳', '구글', '아마존', '메타', '오픈AI', '앤트로픽',
          'AMD', '인텔', '컨스텔레이션', '비스트라', '탈렌', 'GE버노바', 'CXMT',
          'KLA', '브로드컴', '퀄컴', '코어위브', '오라클')


# 이름은 한국어 정본으로 적었지만 본문에는 영문으로 서는 일이 잦다(받은 글은 「OpenAI」로
# 쓴다). 별칭 사전을 읽어 한 이름의 여러 표기를 다 본다 — 없으면 한국어 표기만 본다.
def _alias_map():
    out = {n: {n} for n in ACTORS}
    try:
        raw = json.load(io.open(os.path.join(ROOT, 'insights', 'actor_alias.json'),
                                encoding='utf-8'))
    except Exception:
        return out
    for k, v in raw.items():
        # 「_설명」처럼 값이 목록인 줄이 섞여 있다 — 문자열만 본다
        if isinstance(v, str) and v in out:
            out[v].add(k)
    return out


ALIASES = _alias_map()


def _has_actor(name, text):
    return any(a in text for a in ALIASES.get(name, {name}))


def attach_related(cards, by_title=None, by_keyword=()):
    """카드끼리 잇는 「연관 포스트」를 붙인다.

    섹션이 회사별로 갈리면 그 방법을 설명한 포스트가 다른 타일에 있어 카드 안에서 길이 끊긴다.
    by_title  = {카드 제목: [연결할 카드 제목, …]}          — 한 장씩 지목
    by_keyword = [(키워드, [연결할 카드 제목, …]), …]        — 제목이나 topic에 그 말이 든 카드 전부

    제목이 CARDS에 없으면 assert로 걸린다. 자기 자신은 빼고, 같은 대상이 두 번 붙지 않는다."""
    have = {c['title'] for c in cards}

    def links(c, titles):
        out = []
        for t in titles:
            assert t in have, '연관 포스트로 지목한 카드가 없다: %s' % t
            if t != c['title']:
                out.append(t)
        return out

    for c in cards:
        picked = list(links(c, (by_title or {}).get(c['title'], [])))
        label = c['title'] + ' ' + (c.get('topic', ('', ''))[1] if isinstance(c.get('topic'), tuple) else '')
        for kw, titles in by_keyword:
            if kw in label:
                picked += [t for t in links(c, titles) if t not in picked]
        if picked:
            c['related'] = [(t, slug(t)) for t in picked]


def check_links(cards):
    """카드가 가리키는 저장소 파일이 실제로 있는지 본다.

    blob 링크는 파일명을 손으로 적는 자리라 요약본 제목을 한 글자만 고쳐도 404가 된다.
    2026-08-18에 「주당 361,000원」을 「주가」로 적은 링크 둘이 그렇게 죽어 있었다."""
    import urllib.parse as _up
    for c in cards:
        for l in c.get('links', ()):
            if len(l) < 2 or 'content/' not in l[1]:
                continue
            rel = _up.unquote(l[1].split('/main/')[-1])
            assert os.path.exists(os.path.join(ROOT, rel)),                 '죽은 링크: %s — %s' % (c.get('title', ''), rel)


def check_labels(cards):
    """카드 라벨이 원문보다 좁거나 원문에 없는 회사를 달고 있으면 여기서 멈춘다."""
    import urllib.parse as _up
    for c in cards:
        sec, top = c.get('section'), c.get('topic')
        label = ' '.join([sec[2] if isinstance(sec, tuple) and len(sec) > 2 else '',
                          top[1] if isinstance(top, tuple) and len(top) > 1 else ''])
        src = ' '.join(_up.unquote(l[1]) for l in c.get('links', ())
                       if len(l) > 1 and 'content/' in l[1])
        if not src:
            continue                      # 원문 링크가 없는 카드(영상 등)는 대상이 아니다
        # 「라벨에만 있는 회사」는 카드 본문까지 보고 판단한다. 파일명만 보면 「DS 영업이익률」처럼
        # 회사 이름이 제목에 안 든 글이 걸린다. 반대로 「좁혔다」 판정은 파일명만 본다 —
        # 본문은 비교 대상으로 다른 회사를 스칠 뿐인데 그것까지 세면 전부 걸린다.
        body_src = (src + ' ' + (c.get('oneliner') or '') + ' '
                    + ' '.join(c.get('points') or ())
                    # 번호글 카드는 points가 없다 — 본문이 post에 들어 있다
                    + ' ' + ' '.join(c.get('post') or ())
                    # 받은 글을 그대로 싣는 카드(Semi Doped)는 본문이 report 에 있다.
                    # 안 보면 「제목에 회사 이름이 없다」는 이유만으로 걸린다
                    + ' ' + ' '.join(str(b[1]) for b in (c.get('report') or ())
                                     if len(b) > 1))
        title = c.get('title', '')
        named = [n for n in ACTORS if n in label]
        alien = [n for n in named
                 if not _has_actor(n, body_src) and not _has_actor(n, title)]
        assert not alien, ('라벨 규칙 위반: 원문에 없는 회사를 라벨에 달았다 — %s / 라벨 %s / 없는 이름 %s'
                           % (title, label.strip(), ', '.join(alien)))
        # 여러 회사 섹션에 같이 서는 카드(c['also'])는 좁힌 것이 아니다 — 양쪽에 다 있다
        if named and not c.get('also'):
            narrowed = [n for n in ACTORS if n in src
                        and n not in label and not _has_actor(n, title)]
            assert not narrowed, (
                '라벨 규칙 위반: 여러 회사를 다룬 원문을 한 회사 라벨 아래 뒀다 — %s / 라벨 %s / '
                '원문에도 있는 이름 %s. 라벨을 넓히거나(예: 「반도체 3사」) 주제 라벨로 바꾼다'
                % (title, label.strip(), ', '.join(narrowed)))


# 이 규약이 깨진 채로 페이지가 나가면 대시보드마다 첫 화면이 달라진다. 2026-08-17에 부동산만
# 관문 버튼이 하나 더 생겨 그렇게 됐다. 사람이 눈으로 지키지 말고 여기서 막는다.
def check_ui(html, has_top, tiles=True):
    assert 'mode-pick' not in html,         'UI 규약 위반: 섹션 타일 앞에 관문 버튼을 두지 않는다 — 타일 하나로 넣는다'
    if not tiles:
        # 타일을 안 내는 장. 갈래를 고르는 층이 탭 하나뿐이라 규약이 막던 것(관문·타일
        # 순서)이 애초에 생기지 않는다. 대신 고를 길이 하나는 있어야 한다
        assert 'scope-tabs' in html, 'UI 규약 위반: 타일도 탭도 없으면 고를 길이 없다'
        return
    must = [('sec-pick', '섹션 타일'), ('class="sback"', '현재 자리 이름표'),
            ('class="stile is-all"', '전체 보기 타일')]
    for key, name in must:
        assert key in html, 'UI 규약 위반: %s이 없다' % name
    assert 'mode-pick' not in html, \
        'UI 규약 위반: 섹션 타일 앞에 관문 버튼을 두지 않는다 — 타일 하나로 넣는다'
    if has_top:
        assert 'data-fixed="1"' in html and 'class="stile" data-sec=' in html,             'UI 규약 위반: 카드 없는 고정 층이 타일로 안 섰다'
    # 클래스가 'sec-pick sgrid'라 닫는 따옴표까지 찾으면 -1이 나와 문서 전체를 앞부분으로 본다
    at = html.find('class="sec-pick')
    assert at > 0, 'UI 규약 위반: 섹션 타일을 못 찾았다'
    assert '<section id=' not in html[:at], \
        'UI 규약 위반: 섹션 타일보다 먼저 나오는 본문 섹션이 있다'


def josa(word, pair='은는'):
    """받침에 맞는 조사를 골라 붙인다.

    회사 이름을 계산에서 뽑아 문장에 끼우면 「알파벳는·애플는」이 나온다. 이름이
    상수일 때는 손으로 맞췄지만 순위표에서 뽑아 쓰면 그럴 수가 없다.

    pair 는 받침 있을 때·없을 때 순서다. 「으로/로」는 글자 수가 달라 짝을 표로 둔다 —
    한 글자씩 자르면 「알파벳으」가 나온다.
    """
    forms = {'은는': ('은', '는'), '이가': ('이', '가'), '을를': ('을', '를'),
             '과와': ('과', '와'), '으로로': ('으로', '로'), '아야': ('아', '야')}
    has, no = forms.get(pair, (pair[0], pair[-1]))
    if not word:
        return word
    ch = word[-1]
    if not ('가' <= ch <= '힣'):
        return word + no
    jong = (ord(ch) - 0xAC00) % 28
    # 「으로」는 ㄹ 받침이 예외다 — 「서울로」지 「서울으로」가 아니다
    if pair == '으로로' and jong == 8:
        return word + '로'
    return word + (has if jong else no)
