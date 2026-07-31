# 제약과 회사 — 원자가 말하는 제약 옆에 그 제약을 파는 회사와 맞는 회사를 놓는다.
# 원자(감사 대상)는 손대지 않는다. 상업적 해석은 views/actor_map.json에만 있고,
# 이 페이지는 그 해석과 원자를 잇기만 한다. 가격·타이밍은 이 체계에 없다 — 종목 추천이 아니다.
import os, io, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca
import style
from gen_atomview import DISP, NODE_NOTE, esc

ROOT = ca.ROOT
OUT = os.path.join(ROOT, '대시보드', '제약과 회사.html')
AMAP = os.path.join(ROOT, 'insights', 'views', 'actor_map.json')


def build():
    atoms = ca.load_atoms()
    amap = json.load(io.open(AMAP, encoding='utf-8'))
    comp = amap['companies']
    man = {s['id']: s for s in json.load(io.open(ca.MAN, encoding='utf-8'))['sources']}

    # (칸, 회사) -> 원자들. 한 원자에 주체가 여럿이면 그 회사 모두에 걸린다
    grid = {}
    seen = set()
    for a in atoms:
        node = a['view']['stack']
        for name in a['view'].get('actor') or []:
            grid.setdefault((node, name), []).append(a)
            seen.add(name)

    def atom_card(a):
        src = man.get(a['_source_id'], {})
        doc = os.path.basename(src.get('path', a['_path']))
        h = ['<div class="atom"><span class="aid">%s</span>' % esc(a['id'])]
        h.append('<span class="atag">%s</span>' % esc(ca.corpus_of(a['_source_id'])))
        h.append('<p class="aclaim">%s</p>' % esc(a.get('claim')))
        if a.get('value'):
            h.append('<p class="kv"><span>값</span> %s</p>' % esc(a['value']))
        h.append('<p class="kv"><span>조건</span> %s</p>' % esc(a.get('condition')))
        h.append('<p class="kv"><span>출처</span> %s %s행 · %s</p>'
                 % (esc(doc), esc(a.get('line')), esc(a['view']['time'])))
        h.append('<div class="src">%s</div></div>' % esc(a.get('line_text')))
        return ''.join(h)

    def co_card(node, name, items):
        c = comp.get(name) or {}
        tick = (('<span class="tk">%s</span>' % esc(c['ticker'])) if c.get('ticker')
                else '<span class="tk off">비상장</span>')
        unsure = ('<span class="tk warn">확인 필요</span>'
                  if c.get('confidence') != '확인' else '')
        return ('<details class="co"><summary>'
                '<span class="con">%s</span>%s%s<span class="cnt">원자 %d개</span>'
                '<p class="crole">%s</p>'
                '<p class="cmkt">%s</p></summary>%s</details>'
                % (esc(name), tick, unsure, len(items), esc(c.get('role') or ''),
                   esc(c.get('market') or ''), ''.join(atom_card(a) for a in items)))

    SIDES = ['파는 쪽', '맞는 쪽', '양쪽']
    blocks = []
    for node in DISP:
        rows = [(n, v) for (nd, n), v in grid.items() if nd == node]
        if not rows:
            continue
        rows.sort(key=lambda kv: (-len(kv[1]), kv[0]))
        cols = []
        for side in SIDES:
            mine = [(n, v) for n, v in rows if (comp.get(n) or {}).get('side') == side]
            if not mine:
                continue
            cols.append('<div class="side"><p class="sh">%s <span>%d곳</span></p>%s</div>'
                        % (esc(side), len(mine),
                           ''.join(co_card(node, n, v) for n, v in mine)))
        blocks.append('<section class="nodeblk"><h3 class="nh">%s</h3>'
                      '<p class="nn">%s · 원자 %d개</p><div class="sides">%s</div></section>'
                      % (esc(node), esc(NODE_NOTE.get(node, '')),
                         sum(len(v) for _, v in rows), ''.join(cols)))

    # 원자에 한 번도 안 나온 회사 — 사전에는 있는데 근거가 없다
    idle = sorted(set(comp) - seen)
    idle_html = ('<p class="axnote">사전에는 있지만 아직 어느 원자에도 나오지 않은 회사: %s</p>'
                 % esc(', '.join(idle))) if idle else ''

    listed = sum(1 for v in comp.values() if v.get('listed'))
    unsure = sorted(n for n, v in comp.items() if v.get('confidence') != '확인')
    unsure_html = ('<p class="axnote">티커·소속을 더 확인해야 하는 곳: <b>%s</b>. '
                   '이 표시가 붙은 줄은 그대로 쓰지 말 것.</p>' % esc(', '.join(unsure))) if unsure else ''

    html = (TMPL
            .replace('__CSS__', style.BASE)
            .replace('__BLOCKS__', ''.join(blocks))
            .replace('__IDLE__', idle_html)
            .replace('__UNSURE__', unsure_html)
            .replace('__DISC__', esc(amap['disclaimer']))
            .replace('__NOTE__', esc(amap['note']))
            .replace('__NCO__', str(len(comp)))
            .replace('__NLISTED__', str(listed))
            .replace('__NPAIR__', str(len(grid)))
            .replace('__NATOM__', str(len(atoms))))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('OK: 회사 %d곳(상장 %d) / 칸·회사 짝 %d개 -> %s' % (len(comp), listed, len(grid), OUT))


TMPL = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>제약과 회사</title>
<style>__CSS__
  .disc{background:var(--soft);border-left:3px solid var(--accent);border-radius:0 var(--r) var(--r) 0;
        padding:12px 16px;margin:18px 0 0;font-size:var(--t-body);color:var(--ink);line-height:1.6}
  .disc b{color:var(--accent2)}
  .nodeblk{margin-top:26px;padding-top:18px;border-top:1px solid var(--line)}
  .nh{font-size:var(--t-h2);font-weight:850;letter-spacing:-.02em;margin:0}
  .nn{font-size:var(--t-meta);color:var(--faint);margin:3px 0 12px}
  .sides{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .side{min-width:0}
  .sh{font-size:var(--t-lbl);font-weight:800;letter-spacing:.08em;text-transform:uppercase;
      color:var(--accent);margin:0 0 7px}
  .sh span{color:var(--faint);font-weight:700;margin-left:4px}
  .co{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--accent);
      border-radius:var(--r);padding:12px 14px;margin-bottom:8px;box-shadow:var(--shadow)}
  .co>summary{list-style:none;cursor:pointer;position:relative;padding-right:22px;
              -webkit-tap-highlight-color:transparent}
  .co>summary::-webkit-details-marker{display:none}
  .co>summary::after{content:"⌄";position:absolute;right:0;top:-4px;font-size:19px;color:var(--faint);
                     transition:transform .3s cubic-bezier(.32,.72,0,1)}
  .co[open]>summary::after{transform:rotate(180deg)}
  .co>summary:active{transform:scale(.994);transition:transform 100ms ease-out}
  .con{font-size:var(--t-lead);font-weight:800;letter-spacing:-.01em}
  .tk{font-size:var(--t-lbl);font-weight:800;margin-left:6px;padding:2px 7px;border-radius:999px;
      background:var(--soft);color:var(--accent2);font-variant-numeric:tabular-nums}
  .tk.off{background:var(--sunk);color:var(--faint)}
  .tk.warn{background:#f6ecda;color:#9a5b12}
  @media (prefers-color-scheme:dark){.tk.warn{background:#2a2113;color:#d79a4e}}
  .cnt{font-size:var(--t-lbl);color:var(--faint);margin-left:6px;font-variant-numeric:tabular-nums}
  .crole{font-size:var(--t-body);color:var(--sub);margin:5px 0 0;line-height:1.55}
  .cmkt{font-size:var(--t-lbl);color:var(--faint);margin:3px 0 0}
  .co .atom{border-top:1px solid var(--line);margin-top:9px;padding-top:10px}
  .co[open]>.atom:first-of-type{animation:reveal .3s cubic-bezier(.32,.72,0,1) both}
  @keyframes reveal{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
  @media (prefers-reduced-motion:reduce){
    .co[open]>.atom:first-of-type{animation:none}
    .co>summary:active{transform:none}
  }
  .maplink{color:var(--accent);font-weight:700;text-decoration:none}
  @media (max-width:640px){
    .sides{grid-template-columns:1fr}
    .co>summary{min-height:44px}
  }
</style>
<div class="wrap">
<header>
  <p class="eyebrow">Constraints &amp; Companies</p>
  <h1>제약과 회사</h1>
  <p class="lede">원자가 말하는 제약 옆에, 그 제약을 <b>파는 회사</b>와 <b>맞는 회사</b>를 놓았습니다.
  회사 이름을 누르면 그 회사가 그 칸에서 나온 원자와 원문 줄이 나옵니다.</p>
  <p class="disc"><b>종목 추천이 아닙니다.</b> __DISC__</p>
  <div class="meta"><span>회사 __NCO__곳 · 상장 __NLISTED__</span><span>칸·회사 짝 __NPAIR__개</span>
    <span>원자 __NATOM__개</span>
    <a class="maplink" href="인사이트와 근거.html">인사이트와 근거 →</a></div>
</header>

<p class="axnote">__NOTE__</p>
__UNSURE__
__IDLE__
__BLOCKS__

<footer>insights/views/actor_map.json(해석)과 atoms(원자)에서 <code>gen_actormap.py</code>로 생성.
원자는 원문 환원 대상이라 이 해석을 원자 파일에 넣지 않습니다 — 배정이 바뀌어도 원자는 그대로여야 합니다.
어느 칸에서 나온 회사인지는 원자의 주체 표기를 그대로 따릅니다.</footer>
</div>
'''

if __name__ == '__main__':
    build()
