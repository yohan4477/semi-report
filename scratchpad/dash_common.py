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
from card_lib import EXTRA_CSS, FIG_CSS, FIG_DEFS, slug, card_html  # noqa: F401

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
  .sectp-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:2px 0 12px}
  .sect-up{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:7px 13px;
           border:1px dashed var(--line);border-radius:999px;background:transparent;
           color:var(--ink-3)}
  .sect-up:hover{border-color:var(--accent);color:var(--accent)}
  .sectp-t{font-size:12.5px;font-weight:850;color:var(--ink)}
  .sback{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 2px}
  .sback[hidden]{display:none}
  .sb-btn{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:7px 13px;
          border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink)}
  .sb-btn:hover{border-color:var(--accent);color:var(--accent)}
  .sb-now{font-weight:800;font-size:13.5px}
  /* 섹션 안 두 갈래 버튼 — 회사를 고른 다음 무엇을 볼지 정한다 */
  /* 올라가는 길이 한 줄을 갖고, 내용 버튼은 그 아래 줄에 선다 — 성격이 다른 버튼이
     한 줄에 섞이면 어느 쪽이 위로 가는 길인지 눈이 먼저 못 가른다 */
  .secsw{display:block;margin:14px 0 4px}
  .secsw .sw-up{display:flex;width:fit-content;margin:0 0 9px}
  .secsw .sw-btn{display:inline-flex;margin:0 8px 0 0}
  .secsw[hidden]{display:none}
  .sw-up{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:11px 15px;
         border:1px dashed var(--line);border-radius:10px;background:transparent;color:var(--ink-3)}
  .sw-up:hover{border-color:var(--accent);color:var(--accent)}
  .sw-btn{font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;padding:11px 20px;
          border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink)}
  .sw-btn:hover{border-color:var(--accent);color:var(--accent)}
  .sw-btn[aria-pressed="true"]{border-color:var(--accent);color:var(--accent);background:var(--soft)}
  .sw-n{font-variant-numeric:tabular-nums;color:var(--ink-3);font-weight:700;margin-left:5px}
  .sv-val[hidden], .sv-posts[hidden]{display:none}
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


def _card(c, dup=False):
    """카드 마크업. 사본(다른 회사 섹션에 한 번 더 서는 것)은 앵커를 뗀다."""
    h = card_html(c)
    if dup:
        h = h.replace(' id="%s"' % slug(c['title']), '', 1)
    return h


def sections(cards):
    """카드를 섹션별로 묶는다 — CARDS에 적힌 순서가 곧 화면 순서다.

    c['also'] = [섹션, …]이면 그 섹션에도 같은 카드가 선다. 마이크론과 SK하이닉스를 같이
    다룬 글은 두 회사 어느 쪽을 눌러도 나와야 한다. 두 번째 자리부터는 앵커(id)를 떼고
    낸다 — 같은 id가 문서에 둘이면 링크가 어디로 갈지 정해지지 않는다."""
    secs, order = {}, []
    for c in cards:
        for i, sec in enumerate([c['section']] + list(c.get('also') or ())):
            sid = sec[0]
            if sid not in secs:
                secs[sid] = (sec, [])
                order.append(sid)
            secs[sid][1].append((c, i > 0))
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
    if(sec && sec.hidden){
      var all=document.querySelector('.stile.is-all');
      if(all) all.click();   // 섹션 필터를 푼다. NAV_JS가 화면을 맨 위로 올린다
    }
    setTimeout(function(){
      if(card && !card.classList.contains('is-open')){
        var head=card.querySelector('.uc-head');
        if(head) head.click();   // FOLD_JS가 문서 단위로 받아서 편다
      }
      if(card) card.scrollIntoView({behavior: smooth ? 'smooth' : 'auto', block:'start'});
    }, 140);
  }
  function fromHash(smooth){
    var id=(location.hash||'').slice(1);
    if(id) jump(decodeURIComponent(id), smooth);
  }
  document.addEventListener('click', function(e){
    var a=e.target.closest('a.kin-link');
    if(a){
      e.preventDefault();
      jump(a.getAttribute('href').slice(1), true);
      return;
    }
    var b=e.target.closest('.uc-copy'); if(!b) return;
    var url=location.origin + location.pathname + '#' + encodeURIComponent(b.dataset.anchor);
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

SW_JS = '<script>\n(function(){\n  function show(sid, view){\n    var sw=document.querySelector(\'.secsw[data-sec="\'+sid+\'"]\');\n    if(sw) sw.querySelectorAll(\'.sw-btn\').forEach(function(b){\n      b.setAttribute(\'aria-pressed\', String(b.dataset.view===view));\n    });\n    var val=document.querySelector(\'.sv-val[data-sec="\'+sid+\'"]\');\n    var posts=document.querySelector(\'.sv-posts[data-sec="\'+sid+\'"]\');\n    if(val) val.hidden = view!==\'val\';\n    if(posts) posts.hidden = view!==\'posts\';\n  }\n  document.addEventListener(\'click\', function(e){\n    if(e.target.closest(\'.sw-up\')){\n      var back=document.querySelector(\'.sback .sb-btn\');\n      if(back) back.click();\n      return;\n    }\n    var b=e.target.closest(\'.sw-btn\'); if(!b) return;\n    show(b.closest(\'.secsw\').dataset.sec, b.dataset.view);\n  });\n  // 카드를 지목한 주소로 들어오면 그 카드가 든 갈래를 펴 준다\n  function fromHash(){\n    var id=(location.hash||\'\').slice(1); if(!id) return;\n    var h=document.getElementById(decodeURIComponent(id)); if(!h) return;\n    var box=h.closest(\'.sv-posts\'); if(box) show(box.dataset.sec, \'posts\');\n  }\n  window.addEventListener(\'hashchange\', fromHash);\n  if(document.readyState===\'loading\'){\n    document.addEventListener(\'DOMContentLoaded\', fromHash);\n  } else { fromHash(); }\n})();\n</script>'


NAV_JS = '''<script>
(function(){
  var tabs=document.querySelector('.scope-tabs');   // 범위 탭은 국내·해외가 섞인 페이지에만 있다
  var box=document.querySelector('.sec-pick'); if(!box) return;
  var back=document.querySelector('.sback');
  var pick = tabs? 'kr' : 'all';   // 범위 탭이 없는 페이지는 늘 전체
  // 화면이 둘이다. 주제를 고르는 화면과 그 주제의 카드를 읽는 화면.
  // 한 화면에 타일과 카드를 같이 두면 무엇을 보고 있는지 흐려진다.
  var only=null, picking=true, sect=null;
  function opt(id){ return box.querySelector('button[data-sec="'+id+'"]'); }
  function apply(){
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
      // 카드가 없는 섹션(통합 인사이트)은 교차 카드로 센다. 범위 탭은 타지 않는다
      var live = s.hasAttribute('data-fixed')
                   ? (s.dataset.n ? parseInt(s.dataset.n, 10) : s.querySelectorAll('.ins').length)
                   : s.querySelectorAll('.ucard:not([hidden])').length;
      seen+=live;
      s.hidden = picking || live===0 || (only && s.id!==only);
      var o=opt(s.id);
      if(o){
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
    document.querySelectorAll('.sec-lead, .sv-posts').forEach(function(l){
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
    var all=opt(''); if(all){ var ac=all.querySelector('.cnt'); if(ac) ac.textContent=seen; }
    box.hidden = !picking;
    // 읽는 순서 안내는 첫 화면에만 둔다 — 섹션을 고르고 나면 그 섹션을 읽을 차례다
    var intro=document.querySelector('.intro');
    if(intro) intro.hidden = !picking;
    var roll2=document.querySelector('.rollup');
    if(roll2 && picking) roll2.hidden = false;   // 주제 고르는 화면에서는 롤업을 그대로 둔다
    if(back){
      back.hidden = picking;
      var now=back.querySelector('.sb-now');
      if(now){
        var cur = only ? opt(only) : opt('');
        var t = cur && cur.querySelector('.st-t');
        now.textContent = picking ? '' : (t ? t.textContent : '');
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
    if(b.classList.contains('sect-up')){ sect=null; apply(); window.scrollTo({top:0}); return; }
    if(b.dataset.sect){ sect=b.dataset.sect; apply(); window.scrollTo({top:0}); return; }
    only = b.dataset.sec || null;   // 전체 보기 타일이면 only=null 로 전부 편다
    if(!only) sect=null;            // 전체 보기에서 돌아오면 섹터 고르는 화면부터
    picking=false;
    apply();
    var sec = only ? document.getElementById(only) : null;
    if(sec) sec.scrollIntoView({behavior:'smooth', block:'start'});
    else window.scrollTo({top:0, behavior:'smooth'});
  });
  if(back) back.addEventListener('click', function(e){
    if(!e.target.closest('.sb-btn')) return;
    picking=true; only=null; apply();
    box.scrollIntoView({behavior:'smooth', block:'start'});
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


def sec_picker(secs, order, total, extra=None, groups=None):
    """섹션을 네모 타일로 세운다 — 무엇이 몇 편 들었는지 접지 않고 보여 준다.

    extra는 카드가 아닌 섹션(통합 인사이트 등)을 맨 앞 타일로 세운다: (sid, 이름, 설명, 편수).
    별도 관문 버튼을 만들지 않는 것이 규약이다 — 페이지를 열면 어느 대시보드든 이 타일이 첫 화면이다."""
    tiles = ['<button class="stile is-all" data-sec="" aria-pressed="true">'
             '<span class="st-num">✦</span><span class="st-t">전체 보기</span>'
             '<span class="st-s">모든 섹션을 한 줄로</span>'
             '<span class="st-n cnt">%d</span></button>' % total]
    if extra:
        xid, xtitle, xsub, xn = extra
        tiles.append('<button class="stile" data-sec="%s" aria-pressed="false">'
                     '<span class="st-num">00</span><span class="st-t">%s</span>'
                     '<span class="st-s">%s</span><span class="st-n cnt">%d</span></button>'
                     % (xid, xtitle, snip(xsub), xn))
    def _tile(sid):
        (_id, num, title, sub), cs = secs[sid]
        return ('<button class="stile" data-sec="%s" aria-pressed="false">'
                '<span class="st-num">%s</span><span class="st-t">%s</span>'
                '<span class="st-s">%s</span><span class="st-n cnt">%d</span></button>'
                % (sid, num, title, snip(sub), len(cs)))

    # 주제를 고르면 타일이 사라지고 카드만 남는다 — 돌아올 길을 같이 둔다
    if not groups:
        tiles.extend(_tile(sid) for sid in order)
        return '<div class="sec-pick sgrid">%s</div>%s' % (''.join(tiles), BACK)

    # 묶음이 있으면 「전체 보기」만 위에 두고 그 아래를 묶음별로 가른다. 묶음 안이
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
        return '<div class="sec-pick">%s</div>%s' % (''.join(body), BACK)

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
                          '<button type="button" class="sect-up">◂ 섹터 다시 고르기</button>'
                          '<span class="sectp-t">%s</span></div>'
                          '<div class="sgrid">%s</div></div>' % (sect_id, name, inner))
        body.append('<div class="sgrp"><p class="sgrp-t">%s</p>'
                    '<div class="sgrid">%s</div></div>' % (label, ''.join(cells)))
    return ('<div class="sec-pick"><div class="sectpick">%s</div>%s</div>%s'
            % (''.join(body), ''.join(panels), BACK))


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


XSEC = 'sec-cross'      # 통합 인사이트 섹션 id — 카드가 없는 섹션이라 NAV_JS가 따로 센다


def render(cards, title, header, footer, out, rollup='', top='', extra_css='',
           top_n=0, top_sub='', top_title='통합 인사이트', top_id='', intro='', sec_top=None,
           sec_bottom=None, sec_groups=None):
    """대시보드 한 장을 조립한다. **첫 화면은 어느 페이지든 섹션 타일이다** — 그 앞에 관문
    버튼을 두지 않는다. top(통합 인사이트)이 있으면 타일 하나가 더 서고, 나머지 주제와 똑같이
    눌러서 열고 「← 이전」으로 돌아온다. 새 대시보드를 만들 때도 이 함수를 통해서만 조립한다.

    intro는 타일 그리드 위에 서는 안내다(읽는 순서 등). 관문이 아니다 — 아무것도 막지 않고
    접을 수 있으며 바로 아래에 타일이 그대로 있다. 섹션을 고르고 나면 스스로 접힌다.

    sec_top = {섹션 id: HTML}. 그 섹션 머리 바로 아래, 카드 앞에 들어간다. 한 회사를 여러 편으로
    평가한 것을 견주는 지도처럼 **그 섹션에만 해당하는** 층을 둘 자리다. 페이지 맨 위 롤업으로
    두면 회사 하나 이야기가 전체 보기 맨 앞에 서서 같은 내용이 두 군데 있는 것처럼 읽힌다."""
    secs, order = sections(cards)
    scoped = [c for c in cards if c.get('scope')]
    kr = len([c for c in scoped if c['scope'] == 'kr'])
    # 카드가 없는 층(통합 인사이트·밸류에이션 지도)도 타일 하나로 선다. id를 바꿀 수 있게 둔다 —
    # 한 저장소에 성격이 다른 고정 층이 여럿이라 sec-cross 하나로는 안 된다.
    tid = top_id or XSEC
    extra = (tid, top_title, top_sub, top_n) if top else None
    nav = sec_picker(secs, order, (kr if scoped else len(cards)) + top_n, extra,
                     groups=sec_groups)
    tabs = ''
    if scoped:
        tabs = SCOPE_TABS % (kr, len(scoped) - kr, len(cards)) + '\n\n  '
    body = []
    if top:
        # 카드가 없는 섹션이라 data-fixed로 표시한다 — 국내·해외 범위 필터도 타지 않는다
        # data-n은 이 층이 몇 편을 담고 있는지다. 카드가 없으니 세어 볼 수가 없다.
        body.append('<section id="%s" data-fixed="1" data-n="%d"><div class="sec-head">'
                    '<span class="sec-num">00</span><h2 class="sec-title">%s</h2></div>%s</section>'
                    % (tid, top_n, top_title, top))
    sec_top, sec_bottom = sec_top or {}, sec_bottom or {}
    unknown = [k for k in list(sec_top) + list(sec_bottom) if k not in secs]
    assert not unknown, 'sec_top·sec_bottom에 없는 섹션 id가 있다: %s' % unknown
    for sid in order:
        (_, num, stitle, _sub), cs = secs[sid]
        # 카드가 먼저다. 지도처럼 여러 편을 견주는 층은 sec_bottom으로 카드 뒤에 둔다 —
        # 앞에 두면 「전체 보기」를 열었을 때 글 대신 도구가 먼저 나온다.
        lead = sec_top.get(sid, '')
        cards_html = ''.join(_card(c, dup) for c, dup in cs)
        if lead:
            # 섹션 안이 두 갈래다. 회사를 고르면 버튼 둘만 보이고, 누른 쪽만 펴진다.
            # 지도와 카드를 한 화면에 같이 쌓으면 회사 하나가 스크롤 여러 판이 된다.
            lead = ('<div class="secsw" data-sec="%s" hidden>'
                    # 맨 앞은 올라가는 길이다. 내용 버튼과 생김새를 갈라 놓는다 —
                    # 같은 모양이면 어느 쪽이 위로 가는 길인지 눌러 봐야 안다.
                    '<button type="button" class="sw-up">◂ 회사 다시 고르기</button>'
                    '<button type="button" class="sw-btn" data-view="val">밸류에이션</button>'
                    '<button type="button" class="sw-btn" data-view="posts">개별 포스트'
                    ' <span class="sw-n">%d</span></button></div>'
                    '<div class="sec-lead sv-val" data-sec="%s" hidden>%s</div>'
                    % (sid, len(cs), sid, lead))
            cards_html = '<div class="sv-posts" data-sec="%s" hidden>%s</div>' % (sid, cards_html)
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2></div>%s%s%s</section>'
                    % (sid, num, stitle, lead, cards_html, sec_bottom.get(sid, '')))
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
            + '\n\n  ' + intro + '\n\n  ' + tabs + nav + '\n\n  ' + rollup + '\n\n  ' + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n'
            + FOLD_JS + NAV_JS + LINK_JS + SW_JS + ui_bits.TOP_BTN + '\n')
    check_labels(cards)
    check_links(cards)
    check_ui(html, bool(top))
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 섹션 %d개 -> %s' % (len(cards), len(order) + bool(top), out))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
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
        body_src = src + ' ' + (c.get('oneliner') or '') + ' ' + ' '.join(c.get('points') or ())
        title = c.get('title', '')
        named = [n for n in ACTORS if n in label]
        alien = [n for n in named if n not in body_src and n not in title]
        assert not alien, ('라벨 규칙 위반: 원문에 없는 회사를 라벨에 달았다 — %s / 라벨 %s / 없는 이름 %s'
                           % (title, label.strip(), ', '.join(alien)))
        # 여러 회사 섹션에 같이 서는 카드(c['also'])는 좁힌 것이 아니다 — 양쪽에 다 있다
        if named and not c.get('also'):
            narrowed = [n for n in ACTORS if n in src and n not in label and n not in title]
            assert not narrowed, (
                '라벨 규칙 위반: 여러 회사를 다룬 원문을 한 회사 라벨 아래 뒀다 — %s / 라벨 %s / '
                '원문에도 있는 이름 %s. 라벨을 넓히거나(예: 「반도체 3사」) 주제 라벨로 바꾼다'
                % (title, label.strip(), ', '.join(narrowed)))


# 이 규약이 깨진 채로 페이지가 나가면 대시보드마다 첫 화면이 달라진다. 2026-08-17에 부동산만
# 관문 버튼이 하나 더 생겨 그렇게 됐다. 사람이 눈으로 지키지 말고 여기서 막는다.
def check_ui(html, has_top):
    must = [('sec-pick', '섹션 타일'), ('class="sback"', '「← 이전」 버튼'),
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
