# -*- coding: utf-8 -*-
"""제3자 해설 카드의 표준 마크업 — 한 벌만 둔다.

부동산 인사이트에서 자리를 잡은 형식이고, 새로 올리는 글은 대시보드를 가리지 않고
이 스키마를 따른다(SemiAnalysis 대시보드는 예외 — 카드 단위가 아니라 그대로 둔다).
자세한 절차는 .claude/skills/insight-upload/SKILL.md 를 본다.

카드 dict 필수 키
  section  (섹션id, 번호, 제목, 한 줄 설명)   섹션 번호는 생성기가 다시 매긴다
  topic    (색 클래스, 주제 칩 문구)
  title    카드 제목
  gain     이 편을 열면 무엇을 알게 되는지 — 접힌 채로 고르는 기준이라 반드시 쓴다
  meta     [화자, 업로드 날짜, 길이, 소스]
  oneliner 무슨 이야기인지 한 문단
  points   핵심 포인트. 각 항목은 <b>소제목.</b>으로 연다
  stats    [(값, 라벨)] 주요 숫자
  quote    원문에서 그대로 가져온 한 마디
  clash    [(누구, 반론)] 한 편만 읽고 결론 내리지 않게 어긋나는 지점을 박아 둔다
  note     곁다리 메모
  links    [(라벨, 주소, 클래스)]
선택 키
  scope    'kr' | 'intl'   국내·해외 탭이 있는 페이지에서만
  table    (표 제목, [머리], [[행]])
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rollup_lib as _rl

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
  /* 자세히 서랍 — 슬림 본문 아래에서 전체 포인트·표·유보를 연다 */
  .uc-more{margin:14px 0 0;border-top:1px solid var(--line);padding-top:10px}
  .uc-more>summary{cursor:pointer;list-style:none;font-size:12.5px;font-weight:800;color:var(--ink-3);
                   padding:4px 0;display:flex;align-items:center;gap:6px}
  .uc-more>summary::-webkit-details-marker{display:none}
  .uc-more>summary::after{content:'▾';font-size:12px;transition:transform .15s ease}
  .uc-more[open]>summary::after{transform:rotate(180deg)}
  .uc-more>summary:hover{color:var(--accent-ink)}
  .uc-more-body{padding-top:6px}
  .ucard.is-fold:not(.is-open) .uc-body{display:none}
  .ucard.is-fold:not(.is-open) .uc-meta{margin-bottom:0}
  .ucard.is-fold:not(.is-open){padding-bottom:16px}
''' + _rl.CSS + '''</style>'''



def slug(t):
    return 'card-' + re.sub(r'[^0-9A-Za-z가-힣]+', '-', t).strip('-')



def slim_html(c):
    """펼쳤을 때 본문을 AI · 인프라 · 에너지 카드와 같은 형태로 낸다.

    접힌 상태는 부동산 인사이트 그대로다(주제칩·제목·gain·화자와 날짜).
    펼치면 한 줄 요약 → 핵심 포인트 → 주요 숫자 → 인용까지가 저쪽 형식과 같고,
    그 뒤에 <b>반론·충돌은 원본 그대로</b> 붙인다(줄이지 않는다). 표는 내지 않는다.

    slim_* 필드를 갖춘 카드만 이 형식으로 나가고 기존 필드는 그대로 남는다.
      slim_oneliner  두세 문장
      slim_points    6~8개, 각 한두 문장
      slim_stats     4개
    """
    h = ['<div class="ucard is-fold"%s>' % (' data-scope="%s"' % c['scope'] if c.get('scope') else '')]
    # 접힌 상태는 지금까지와 같다 — 주제칩·제목·이 편에서 무엇을 알 수 있는지·화자와 날짜
    h.append('<div class="uc-head" role="button" tabindex="0" aria-expanded="false">')
    h.append('<span class="uc-topic %s">%s</span>' % c['topic'])
    h.append('<h2 id="%s">%s</h2>' % (slug(c['title']), c['title']))
    if c.get('gain'):
        h.append('<p class="uc-gain">%s</p>' % c['gain'])
    h.append('<div class="uc-meta">%s</div>' % ''.join('<span>%s</span>' % m for m in c['meta']))
    h.append('<span class="uc-caret" aria-hidden="true">▾</span></div>')
    h.append('<div class="uc-body">')
    h.append('<p class="uc-oneliner">%s</p>' % c.get('slim_oneliner', c['oneliner']))
    h.append('<p class="uc-label">핵심 포인트</p><ul class="uc-points">%s</ul>'
             % ''.join('<li>%s</li>' % p for p in c['slim_points']))
    h.append('<p class="uc-label">주요 숫자</p><div class="stat-grid">%s</div>'
             % ''.join('<div class="stat"><div class="s-val">%s</div><div class="s-label">%s</div></div>' % s
                       for s in c.get('slim_stats', c['stats'])))
    h.append('<p class="uc-quote">%s</p>' % c['quote'])
    # 반론·충돌은 줄이지 않는다 — 한 편만 읽고 결론 내리지 않게 하는 장치라 원본 그대로 쓴다
    if c.get('clash'):
        h.append('<div class="clash"><p class="ch">반론 · 충돌</p><ul>%s</ul></div>'
                 % ''.join('<li><span class="who">%s</span>%s</li>' % (w, t) for w, t in c['clash']))
    h.append('<div class="side-note">%s</div>' % c['note'])
    h.append('<div class="uc-links" style="margin-top:16px;">%s</div>'
             % ''.join('<a %shref="%s" target="_blank" rel="noopener">%s</a>'
                       % (('class="%s" ' % cls) if cls else '', url, lab) for lab, url, cls in c['links']))
    h.append('</div></div>')
    return ''.join(h)


def card_html(c):
    # 슬림 필드를 갖춘 카드는 슬림으로, 아직 없는 카드는 지금까지의 형식 그대로 나간다
    if c.get('slim_points'):
        return slim_html(c)
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


# 카드 접기 동작 — card_html 이 만든 .uc-head 를 눌러 편다
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
