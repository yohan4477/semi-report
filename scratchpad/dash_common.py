# -*- coding: utf-8 -*-
# 제3자 해설 대시보드 공용 부품 — 카드 마크업·추가 CSS·페이지 조립.
# 미국주식 사관학교와 부동산 두 페이지가 같은 규칙을 쓰게 한 벌만 둔다.
# 기본 CSS는 언더스탠딩 대시보드의 <style>을 통째로 물려받는다(세 페이지가 한 벌로 보이게).
import io, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import rollup_lib as _rl
# 카드 마크업 표준은 scripts/card_lib.py 한 벌뿐이다 — 여기서는 가져다 쓴다
from card_lib import EXTRA_CSS, slug, card_html  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '대시보드', '언더스탠딩 대시보드.html')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'

def blob(path):
    return BLOB + urllib.parse.quote(path)


def css():
    src = io.open(SRC, encoding='utf-8').read()
    out = src[src.find('<style'):src.find('</style>') + 8]
    # 원본에 이미 표준 CSS가 들어가 있으면(에너지 페이지 전환 이후) 두 번 붙이지 않는다
    out = out if '.uc-gain{' in out else out.replace('</style>', EXTRA_CSS)
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
  var btn=box && box.querySelector('.sp-btn');
  var list=box && box.querySelector('.sp-list');
  var label=box && box.querySelector('.sp-label');
  var total=box && box.querySelector('.sp-cnt');
  var pick = tabs? 'kr' : 'all';   // 범위 탭이 없는 페이지는 늘 전체
  var only=null;                   // only = 고른 섹션 하나, "전체 보기"로 되돌린다
  function opt(id){ return list && list.querySelector('button[data-sec="'+id+'"]'); }
  function close(){ if(box){ box.classList.remove('open'); list.hidden=true; btn.setAttribute('aria-expanded','false'); } }
  // 섹션을 고른 상태면 그 항목을, 전체를 보는 중이면 지금 화면에 걸린 섹션 항목을 켠다
  function spy(){
    var cur=only, line=120;
    if(!cur){
      var live=document.querySelectorAll('section[id]:not([hidden])');
      live.forEach(function(s){ if(s.getBoundingClientRect().top<=line) cur=s.id; });
      if(!cur && live.length) cur=live[0].id;
    }
    if(list) list.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-current', String(b.dataset.sec===(only||'') || (!only && b.dataset.sec===cur)));
    });
  }
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
    var roll=document.querySelector('.rollup');
    if(roll) roll.hidden = roll.querySelectorAll('.rlrep:not([hidden])').length===0;
    var seen=0;
    document.querySelectorAll('section[id]').forEach(function(s){
      var live=s.querySelectorAll('.ucard:not([hidden])').length;
      seen+=live;
      s.hidden = live===0 || (only && s.id!==only);
      var o=opt(s.id);
      if(o){
        o.parentNode.hidden = live===0;
        var c=o.querySelector('.cnt'); if(c) c.textContent=live;
      }
    });
    if(only){
      var head=document.querySelector('#'+only+' .sec-title');
      var one=document.querySelector('#'+only+' .ucard:not([hidden])');
      if(label) label.textContent = head? head.textContent : '섹션';
      if(total) total.textContent = document.querySelectorAll('#'+only+' .ucard:not([hidden])').length;
      if(!one && label) label.textContent='섹션 전체';
    }else{
      if(label) label.textContent='섹션 전체';
      if(total) total.textContent=seen;
    }
    var all=opt(''); if(all){ var ac=all.querySelector('.cnt'); if(ac) ac.textContent=seen; }
    spy();
    if(tabs) tabs.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.pick===pick));
    });
  }
  if(tabs) tabs.addEventListener('click', function(e){
    var b=e.target.closest('button');
    if(!b) return;
    pick=b.dataset.pick; only=null; close(); apply();
    window.scrollTo({top:0});   // 목록이 통째로 바뀌므로 맨 위에서 다시 읽게 한다
  });
  if(btn) btn.addEventListener('click', function(){
    var open=!box.classList.contains('open');
    box.classList.toggle('open', open);
    list.hidden=!open;
    btn.setAttribute('aria-expanded', String(open));
  });
  if(list) list.addEventListener('click', function(e){
    var b=e.target.closest('button'); if(!b) return;
    only = b.dataset.sec || null;
    close(); apply();
    window.scrollTo({top:0});
  });
  document.addEventListener('click', function(e){
    if(box && !e.target.closest('.sec-pick')) close();
  });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });
  var tick=false;
  window.addEventListener('scroll', function(){
    if(tick) return;
    tick=true;
    requestAnimationFrame(function(){ tick=false; spy(); });
  }, {passive:true});
  apply();
})();
</script>'''


def sec_picker(secs, order, total):
    """섹션 고르기 목록. 칩을 늘어놓지 않고 눌러서 아래로 펼친다"""
    items = ['<li><button data-sec="">전체 보기<span class="cnt">%d</span></button></li>'
             '<li class="sp-sep"></li>' % total]
    items += ['<li><button data-sec="%s">%s<span class="cnt">%d</span></button></li>'
              % (sid, secs[sid][0][2], len(secs[sid][1])) for sid in order]
    return ('<div class="sec-pick">'
            '<button class="sp-btn" aria-expanded="false" aria-haspopup="true">'
            '<span class="sp-label">섹션 전체</span><span class="sp-cnt">%d</span>'
            '<span class="sp-caret" aria-hidden="true">▾</span></button>'
            '<ul class="sp-list" hidden>%s</ul></div>' % (total, ''.join(items)))


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


def render(cards, title, header, footer, out, rollup=''):
    secs, order = sections(cards)
    scoped = [c for c in cards if c.get('scope')]
    kr = len([c for c in scoped if c['scope'] == 'kr'])
    nav = sec_picker(secs, order, kr if scoped else len(cards))
    tabs = ''
    if scoped:
        tabs = SCOPE_TABS % (kr, len(scoped) - kr, len(cards)) + '\n\n  '
    body = []
    for sid in order:
        (_, num, stitle, _sub), cs = secs[sid]
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2></div>%s</section>'
                    % (sid, num, stitle, ''.join(card_html(c) for c in cs)))
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n' % title + css()
            + '\n<div class="wrap">\n' + header + '\n\n  ' + rollup + '\n\n  ' + tabs + nav + '\n\n  ' + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n' + FOLD_JS + NAV_JS + '\n')
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 섹션 %d개 -> %s' % (len(cards), len(order), out))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
    return html
