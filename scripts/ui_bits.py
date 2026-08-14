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
