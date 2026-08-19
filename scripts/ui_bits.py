# -*- coding: utf-8 -*-
"""대시보드 공용 UI 조각.

페이지마다 CSS 변수 이름이 달라서(--ink/--paper vs --sub/--card) 여기 있는 것들은
색을 스스로 들고 간다. 클래스는 ui- 접두어로 격리한다.
"""

# 맨 위로 — 카드가 길어 스크롤이 깊어지면 되돌아갈 길이 필요하다
TOP_BTN = '''
<style>
  .ui-top{
    position:fixed; z-index:9998;
    right:max(16px, env(safe-area-inset-right));
    bottom:max(18px, env(safe-area-inset-bottom));
    width:42px; height:42px; border-radius:999px; border:1px solid rgba(0,0,0,.12);
    display:flex; align-items:center; justify-content:center;
    font:700 17px/1 -apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo",sans-serif;
    color:#33312c; background:rgba(255,255,255,.86); cursor:pointer;
    box-shadow:0 4px 16px -4px rgba(0,0,0,.25);
    -webkit-backdrop-filter:saturate(1.5) blur(12px); backdrop-filter:saturate(1.5) blur(12px);
    opacity:0; pointer-events:none; transform:translateY(6px);
    transition:opacity .2s ease, transform .3s cubic-bezier(.19,1,.22,1);
    -webkit-tap-highlight-color:transparent; touch-action:manipulation;
  }
  .ui-top.is-on{ opacity:1; pointer-events:auto; transform:translateY(0); }
  .ui-top:hover{ transform:translateY(-2px); }
  .ui-top:active{ transform:translateY(0) scale(.94); transition-duration:.09s; }
  .ui-top:focus-visible{ outline:2px solid currentColor; outline-offset:3px; }
  @media (prefers-color-scheme: dark){
    .ui-top{ color:#ecead9; background:rgba(28,28,32,.86); border-color:rgba(255,255,255,.16);
             box-shadow:0 4px 16px -4px rgba(0,0,0,.6); }
  }
  @media (prefers-contrast: more){
    .ui-top{ background:#fff; color:#000; border:1.5px solid #000;
             -webkit-backdrop-filter:none; backdrop-filter:none; }
  }
  @media (prefers-reduced-motion: reduce){
    .ui-top{ transition:opacity .15s ease; transform:none; }
    .ui-top.is-on:hover{ transform:none; }
  }
  @media print{ .ui-top{ display:none; } }
</style>
<button class="ui-top" type="button" aria-label="맨 위로">↑</button>
<script>
(function(){
  var b=document.querySelector('.ui-top'); if(!b) return;
  var show=function(){ b.classList.toggle('is-on', window.scrollY>420); };
  window.addEventListener('scroll', show, {passive:true});
  b.addEventListener('click', function(){
    window.scrollTo({top:0, behavior:'smooth'});
  });
  show();
})();
</script>
'''


# 갈래(섹션) 하나·글 하나를 지목하는 주소를 집어 가는 버튼.
#
# 대시보드 주소를 통째로 보내면 받은 사람이 무엇을 보라는 것인지 모른다. 카드 체계를 쓰는
# 장(dash_common)은 자기 것(.uc-copy/.sec-copy)이 있고, 여기 있는 것은 그 밖의 장 — 관리자·
# 허브·지도·타임라인처럼 만드는 방식이 저마다 다른 페이지가 같은 부품을 쓰라고 둔 것이다.
# 색을 스스로 들고 간다(페이지마다 CSS 변수 이름이 다르다).
def copy_btn(aid, label='링크 복사'):
    return '<button type="button" class="ui-copy" data-anchor="%s">%s</button>' % (aid, label)


COPY_JS = """
<style>
  .ui-copy{
    font:750 11.5px/1 inherit; letter-spacing:.01em; cursor:pointer;
    color:currentColor; opacity:.62; background:transparent;
    border:1px dashed currentColor; border-radius:6px; padding:4px 9px;
    -webkit-tap-highlight-color:transparent;
  }
  .ui-copy:hover{ opacity:1; }
  @media print{ .ui-copy{ display:none; } }
</style>
<script>
(function(){
  function reveal(el){
    // 접혀 있는 자리(details)와 숨겨 둔 자리(hidden)를 위로 훑어 올라가며 편다
    for(var n=el; n && n!==document.body; n=n.parentElement){
      if(n.tagName==='DETAILS') n.open=true;
      if(n.hasAttribute && n.hasAttribute('hidden')) n.hidden=false;
    }
  }
  function jump(id, smooth){
    var el=document.getElementById(id); if(!el) return;
    reveal(el);
    setTimeout(function(){
      el.scrollIntoView({behavior: smooth ? 'smooth' : 'auto', block:'start'});
    }, 40);
  }
  function fromHash(smooth){
    var id=(location.hash||'').slice(1);
    if(id) jump(decodeURIComponent(id), smooth);
  }
  document.addEventListener('click', function(e){
    var b=e.target.closest('.ui-copy'); if(!b) return;
    e.preventDefault(); e.stopPropagation();
    var url=location.origin + location.pathname + '#' + encodeURIComponent(b.dataset.anchor);
    var txt=b.textContent;
    var done=function(ok){
      b.textContent = ok ? '복사됨' : '주소창에 있습니다';
      setTimeout(function(){ b.textContent=txt; }, 1600);
    };
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(function(){ done(true); }, function(){ done(false); });
    } else {
      // 클립보드를 못 쓰는 환경(비보안 문맥)에서는 주소창에 띄워 손으로 집게 한다
      history.replaceState(null, '', url);
      done(false);
    }
  });
  window.addEventListener('hashchange', function(){ fromHash(true); });
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', function(){ fromHash(false); });
  } else { fromHash(false); }
})();
</script>
"""
