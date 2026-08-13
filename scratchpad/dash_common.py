# -*- coding: utf-8 -*-
# 제3자 해설 대시보드 공용 부품 — 카드 마크업·추가 CSS·페이지 조립.
# 미국주식 사관학교와 부동산 두 페이지가 같은 규칙을 쓰게 한 벌만 둔다.
# 기본 CSS는 언더스탠딩 대시보드의 <style>을 통째로 물려받는다(세 페이지가 한 벌로 보이게).
import io, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
import rollup_lib as _rl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '대시보드', '언더스탠딩 대시보드.html')
BLOB = 'https://github.com/yohan4477/semi-report/blob/main/'

EXTRA_CSS = '''
  .tbl-wrap{overflow-x:auto;margin:8px 0 4px;-webkit-overflow-scrolling:touch}
  .uc-tbl{border-collapse:collapse;width:100%;min-width:520px;font-size:.86rem}
  .uc-tbl th,.uc-tbl td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
  .uc-tbl th{font-size:.74rem;font-weight:800;color:var(--ink-3);letter-spacing:.04em;text-transform:uppercase;
             border-bottom:1px solid var(--line)}
  .uc-tbl td:first-child{font-weight:800;color:var(--ink);white-space:nowrap}
  /* 파란 글씨는 링크로 읽힌다 — 진짜 티커 열에만 쓴다 */
  .uc-tbl.tick td:nth-child(2){font-weight:800;color:var(--accent);white-space:nowrap;font-variant-numeric:tabular-nums}
  .uc-tbl td:nth-child(2){font-weight:700;color:var(--ink)}
  .uc-tbl tr:last-child td{border-bottom:0}
  /* 반론·충돌 — 한 편만 읽고 결론 내리지 않게, 같은 대시보드의 다른 편이나
     SemiAnalysis 코퍼스와 어긋나는 지점을 카드 안에 박아 둔다 */
  .clash{margin:14px 0 0;border-left:3px solid var(--warn,#c2831f);background:var(--warnbg,#fdf6e6);
         border-radius:0 10px 10px 0;padding:11px 14px}
  @media (prefers-color-scheme:dark){.clash{background:#2b2416;border-left-color:#d9a441}}
  .clash .ch{font-size:var(--t-lbl,10.5px);font-weight:800;letter-spacing:.06em;color:#9a6a12;margin:0 0 6px}
  @media (prefers-color-scheme:dark){.clash .ch{color:#e0b256}}
  .clash ul{margin:0;padding-left:17px}
  .clash li{font-size:.84rem;line-height:1.6;color:var(--ink-2);margin-bottom:5px}
  .clash li:last-child{margin-bottom:0}
  .clash li b{color:var(--ink)}
  .clash .who{display:inline-block;font-size:.68rem;font-weight:800;padding:1px 7px;border-radius:999px;
              background:rgba(154,106,18,.13);color:#9a6a12;margin-right:6px;vertical-align:1px;white-space:nowrap}
  @media (prefers-color-scheme:dark){.clash .who{background:rgba(224,178,86,.16);color:#e0b256}}
  /* 국내·해외 필터 — 카드에 data-scope가 있을 때만 생긴다.
     목차(.sec-nav)가 이미 sticky라 그 위에 한 층 더 붙이고 목차를 아래로 민다 */
  .scope-tabs{position:sticky;top:0;z-index:21;display:flex;gap:8px;flex-wrap:wrap;
              padding:10px 0 9px;margin:0;background:var(--paper)}
  /* 섹션 고르기 — 칩을 좌우로 늘어놓는 대신 눌러서 아래로 펼치는 목록 */
  .sec-pick{position:sticky;top:0;z-index:20;background:var(--paper);padding:0 0 10px;
            margin:0 0 6px;border-bottom:1px solid var(--line)}
  .scope-tabs ~ .sec-pick{top:55px}
  .sp-btn{display:flex;align-items:center;gap:8px;width:100%;font:inherit;font-size:13px;font-weight:800;
          cursor:pointer;padding:9px 14px;border-radius:12px;border:1px solid var(--line);
          background:var(--surface);color:var(--ink);text-align:left}
  .sp-btn:hover{border-color:var(--ink-3)}
  .sp-btn .sp-cnt{margin-left:auto;font-weight:700;color:var(--ink-3)}
  .sp-btn .sp-caret{color:var(--ink-3);transition:transform .15s ease}
  .sec-pick.open .sp-btn{border-color:var(--accent);color:var(--accent-ink)}
  .sec-pick.open .sp-caret{transform:rotate(180deg)}
  .sp-list{position:absolute;left:0;right:0;top:calc(100% - 4px);margin:0;padding:6px;list-style:none;
           background:var(--surface);border:1px solid var(--line);border-radius:12px;
           box-shadow:0 8px 24px rgba(26,34,51,.13);max-height:60vh;overflow-y:auto;z-index:30}
  .sp-list li{margin:0}
  .sp-list button{display:flex;align-items:center;gap:8px;width:100%;font:inherit;font-size:13px;font-weight:700;
                  cursor:pointer;padding:9px 12px;border:0;border-radius:9px;background:transparent;
                  color:var(--ink-2);text-align:left}
  .sp-list button:hover{background:var(--sunk);color:var(--ink)}
  .sp-list button .cnt{margin-left:auto;font-weight:700;color:var(--ink-3)}
  .sp-list button[aria-current="true"]{background:var(--accent-soft);color:var(--accent-ink)}
  .sp-sep{height:1px;background:var(--line);margin:5px 4px}
  .scope-tabs button{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:7px 15px;
                     border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2)}
  .scope-tabs button:hover{color:var(--ink);border-color:var(--ink-3)}
  .scope-tabs button[aria-pressed="true"]{background:var(--accent-soft);border-color:var(--accent);
                                          color:var(--accent-ink)}
  .scope-tabs .cnt{font-weight:800;opacity:.75;margin-left:5px}
  /* 목차 칩은 이동이 아니라 그 섹션만 보는 토글이다 — 한 번 더 누르면 풀린다 */
  section[hidden]{display:none}
  /* 제목 밑 한 줄 — 이 편을 열면 무엇을 알게 되는지 */
  .uc-gain{margin:5px 0 8px;font-size:13.5px;line-height:1.55;color:var(--ink-3);font-weight:500}
  /* 카드 접기 — 기본은 제목만, 머리를 누르면 펴진다 */
  .uc-head{position:relative;cursor:pointer;padding-right:28px}
  .uc-head:hover h2{color:var(--accent-ink)}
  .uc-head:focus-visible{outline:2px solid var(--accent);outline-offset:4px;border-radius:8px}
  .uc-caret{position:absolute;right:2px;top:2px;font-size:15px;color:var(--ink-3);
            transition:transform .15s ease}
  .ucard.is-open .uc-caret{transform:rotate(180deg)}
  .ucard.is-fold:not(.is-open) .uc-body{display:none}
  .ucard.is-fold:not(.is-open) .uc-meta{margin-bottom:0}
  .ucard.is-fold:not(.is-open){padding-bottom:16px}
''' + _rl.CSS + '''</style>'''


def blob(path):
    return BLOB + urllib.parse.quote(path)


def slug(t):
    return 'card-' + re.sub(r'[^0-9A-Za-z가-힣]+', '-', t).strip('-')


def css():
    src = io.open(SRC, encoding='utf-8').read()
    out = src[src.find('<style'):src.find('</style>') + 8].replace('</style>', EXTRA_CSS)
    # .xlink는 언더스탠딩 대시보드 CSS에 있다 — 페이지끼리 오가는 링크가 같은 모양이어야 한다
    assert '.xlink{' in out, '언더스탠딩 대시보드 CSS에 .xlink 규칙이 없다'
    return out


def card_html(c):
    # scope는 국내(kr)·국외(intl) 필터용이다. 안 적은 카드는 필터와 무관하게 늘 보인다
    h = ['<div class="ucard is-fold"%s>' % (' data-scope="%s"' % c['scope'] if c.get('scope') else '')]
    # 접힌 상태에서는 머리(주제칩·제목·화자/날짜)만 남고 uc-body는 감춘다
    h.append('<div class="uc-head" role="button" tabindex="0" aria-expanded="false">')
    h.append('<span class="uc-topic %s">%s</span>' % c['topic'])
    h.append('<h2 id="%s">%s</h2>' % (slug(c['title']), c['title']))
    # gain = 이 편을 열면 무엇을 알게 되는지. 접힌 상태에서 고를 수 있게 제목 바로 밑에 둔다
    if c.get('gain'):
        h.append('<p class="uc-gain">%s</p>' % c['gain'])
    h.append('<div class="uc-meta">%s</div>' % ''.join('<span>%s</span>' % m for m in c['meta']))
    h.append('<span class="uc-caret" aria-hidden="true">▾</span></div>')
    h.append('<div class="uc-body">')
    h.append('<p class="uc-oneliner">%s</p>' % c['oneliner'])
    h.append('<p class="uc-label">핵심 포인트</p><ul class="uc-points">%s</ul>'
             % ''.join('<li>%s</li>' % p for p in c['points']))
    if c.get('table'):
        cap, head, rows = c['table']
        h.append('<p class="uc-label">%s</p>' % cap)
        h.append('<div class="tbl-wrap"><table class="uc-tbl%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                 % (' tick' if '티커' in head else '',
                    ''.join('<th>%s</th>' % x for x in head),
                    ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % x for x in r) for r in rows)))
    h.append('<p class="uc-label">주요 숫자</p><div class="stat-grid">%s</div>'
             % ''.join('<div class="stat"><div class="s-val">%s</div><div class="s-label">%s</div></div>' % s
                       for s in c['stats']))
    h.append('<p class="uc-quote">%s</p>' % c['quote'])
    if c.get('clash'):
        h.append('<div class="clash"><p class="ch">반론 · 충돌</p><ul>%s</ul></div>'
                 % ''.join('<li><span class="who">%s</span>%s</li>' % (w, t) for w, t in c['clash']))
    h.append('<div class="side-note">%s</div>' % c['note'])
    h.append('<div class="uc-links" style="margin-top:16px;">%s</div>'
             % ''.join('<a %shref="%s" target="_blank" rel="noopener">%s</a>'
                       % (('class="%s" ' % cls) if cls else '', url, lab) for lab, url, cls in c['links']))
    h.append('</div></div>')
    return ''.join(h)


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
  var tabs=document.querySelector('.scope-tabs');   // 범위 탭은 부동산에만 있다
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
