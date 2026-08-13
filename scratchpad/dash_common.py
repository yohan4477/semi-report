# -*- coding: utf-8 -*-
# 제3자 해설 대시보드 공용 부품 — 카드 마크업·추가 CSS·페이지 조립.
# 미국주식 사관학교와 부동산 두 페이지가 같은 규칙을 쓰게 한 벌만 둔다.
# 기본 CSS는 언더스탠딩 대시보드의 <style>을 통째로 물려받는다(세 페이지가 한 벌로 보이게).
import io, os, re, urllib.parse

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
  .scope-tabs ~ .sec-nav{top:47px}
  .scope-tabs button{font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;padding:7px 15px;
                     border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink-2)}
  .scope-tabs button:hover{color:var(--ink);border-color:var(--ink-3)}
  .scope-tabs button[aria-pressed="true"]{background:var(--accent-soft);border-color:var(--accent);
                                          color:var(--accent-ink)}
  .scope-tabs .cnt{font-weight:800;opacity:.75;margin-left:5px}
  /* 목차 칩은 이동이 아니라 그 섹션만 보는 토글이다 — 한 번 더 누르면 풀린다 */
  .scope-tabs ~ .sec-nav a[aria-current="true"]{background:var(--accent-soft);border-color:var(--accent);
                                                color:var(--accent-ink)}
  section[hidden]{display:none}
</style>'''


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
    h = ['<div class="ucard"%s>' % (' data-scope="%s"' % c['scope'] if c.get('scope') else '')]
    h.append('<span class="uc-topic %s">%s</span>' % c['topic'])
    h.append('<h2 id="%s">%s</h2>' % (slug(c['title']), c['title']))
    h.append('<div class="uc-meta">%s</div>' % ''.join('<span>%s</span>' % m for m in c['meta']))
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
    h.append('</div>')
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

SCOPE_JS = '''<script>
(function(){
  var tabs=document.querySelector('.scope-tabs'); if(!tabs) return;
  var nav=document.querySelector('.sec-nav');
  var pick='kr', only=null;   // only = 목차에서 고른 섹션 하나, 다시 누르면 풀린다
  function link(id){ return nav && nav.querySelector('a[href="#'+id+'"]'); }
  function apply(){
    document.querySelectorAll('.ucard[data-scope]').forEach(function(c){
      c.hidden = !(pick==='all' || c.dataset.scope===pick);
    });
    document.querySelectorAll('section[id]').forEach(function(s){
      var live=s.querySelectorAll('.ucard:not([hidden])').length;
      s.hidden = live===0 || (only && s.id!==only);
      var a=link(s.id);
      if(a){
        a.style.display = live? '' : 'none';
        a.setAttribute('aria-current', String(only===s.id));
        var b=a.querySelector('b'); if(b) b.textContent=live;
      }
    });
    tabs.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.pick===pick));
    });
  }
  tabs.addEventListener('click', function(e){
    var b=e.target.closest('button');
    if(!b) return;
    pick=b.dataset.pick; only=null; apply();
    window.scrollTo({top:0});   // 목록이 통째로 바뀌므로 맨 위에서 다시 읽게 한다
  });
  if(nav) nav.addEventListener('click', function(e){
    var a=e.target.closest('a'); if(!a) return;
    e.preventDefault();
    var id=a.getAttribute('href').slice(1);
    only = (only===id) ? null : id;
    apply();
    if(only) nav.scrollIntoView({block:'start'});
  });
  apply();
})();
</script>'''


def render(cards, title, header, footer, out):
    secs, order = sections(cards)
    nav = '<nav class="sec-nav">%s</nav>' % ''.join(
        '<a href="#%s">%s <b>%d</b></a>' % (sid, secs[sid][0][2], len(secs[sid][1])) for sid in order)
    scoped = [c for c in cards if c.get('scope')]
    tabs = js = ''
    if scoped:
        kr = len([c for c in scoped if c['scope'] == 'kr'])
        tabs = SCOPE_TABS % (kr, len(scoped) - kr, len(cards)) + '\n\n  '
        js = SCOPE_JS
    body = []
    for sid in order:
        (_, num, stitle, sub), cs = secs[sid]
        body.append('<section id="%s"><div class="sec-head"><span class="sec-num">%s</span>'
                    '<h2 class="sec-title">%s</h2></div><p class="sec-sub">%s</p>%s</section>'
                    % (sid, num, stitle, sub, ''.join(card_html(c) for c in cs)))
    html = ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n' % title + css()
            + '\n<div class="wrap">\n' + header + '\n\n  ' + tabs + nav + '\n\n  ' + ''.join(body)
            + '\n\n  <footer>' + footer + '</footer>\n</div>\n' + js + '\n')
    io.open(out, 'w', encoding='utf-8').write(html)
    print('OK: 카드 %d개 / 섹션 %d개 -> %s' % (len(cards), len(order), out))
    print('div', html.count('<div'), html.count('</div>'), '| section', html.count('<section'), html.count('</section>'))
    return html
