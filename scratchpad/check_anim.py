# -*- coding: utf-8 -*-
"""어텐션 애니메이션 — 흐르는 동안 화면을 찍어 본다.

눈으로 보고 「안 겹친다」고 보고하지 않는다(CLAUDE.md). 한 바퀴를 도는 동안 여러 시점을
찍고, 그때마다 자막이 하나만 떠 있는지·막대가 자라는지·가로로 안 넘치는지를 센다.
"""
import io, os, sys
sys.path.insert(0, 'scratchpad')
import check_fig
from playwright.sync_api import sync_playwright

PAGE = os.path.abspath(os.path.join('대시보드', '애니메이션 — 어텐션.html'))
OUT = os.path.join('scratchpad', 'anim_shots')
MARKS = [1.2, 3.6, 5.6, 8.0, 11.0, 14.0, 17.0, 20.5]

# 줄마다 위아래 끝을 잰다. 한 줄 안에서 가장 높이 선 것과 가장 낮게 선 것을 본다.
ROWS_JS = '''() => {
  var s = document.getElementById('stage');
  function span(sel){
    var a = [];
    s.querySelectorAll(sel).forEach(function(e){
      var b = e.getBBox ? e.getBBox() : null;
      if (b && b.height > 0) a.push([b.y, b.y + b.height]);
    });
    if (!a.length) return null;
    return [Math.round(Math.min.apply(null, a.map(function(r){return r[0]}))),
            Math.round(Math.max.apply(null, a.map(function(r){return r[1]})))];
  }
  return {tok: span('.tok'), k: span('.kc'), bar: span('.bar'),
          bv: span('.bv'), v: span('.vc'), cap: span('.cap')};
}'''


def main():
    os.makedirs(OUT, exist_ok=True)
    fails = []
    url = 'file:///' + PAGE.replace(os.sep, '/')
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 760})
        pg.goto(url)
        prev = 0.0
        seen_caps = set()
        for t in MARKS:
            pg.wait_for_timeout(int((t - prev) * 1000))
            prev = t
            pg.screenshot(path=os.path.join(OUT, 't%04d.png' % int(t * 100)))
            caps = pg.eval_on_selector_all(
                '.cap', 'els=>els.map(e=>+e.getAttribute("opacity")).filter(v=>v>0.5).length')
            bars = pg.eval_on_selector_all(
                '.bar', 'els=>els.filter(x=>+x.getAttribute("height")>0).length')
            which = pg.eval_on_selector_all(
                '.cap', 'els=>els.findIndex(e=>+e.getAttribute("opacity")>0.5)')
            seen_caps.add(which)
            print('t=%4.1f초  자막 %d개(%d번) · 선 막대 %d' % (t, caps, which, bars))
            if caps != 1:
                fails.append('t=%.1f: 보이는 자막이 %d개다' % (t, caps))
        if len(seen_caps) < 5:
            fails.append('한 바퀴에서 자막이 %d개만 바뀐다 — 장면이 안 넘어간다' % len(seen_caps))
        # 줄끼리 겹치나 — 정적 SVG 만 보는 check_fig 는 이걸 못 잡는다. 막대는 처음에
        # 높이 0 이라 다 자란 뒤에 재야 한다(실제로 막대가 K 칸을 8px 파고든 적이 있다).
        spans = pg.evaluate(ROWS_JS)
        order = ['tok', 'k', 'bar', 'bv', 'v', 'cap']
        for up, dn in zip(order, order[1:]):
            su, sd = spans.get(up), spans.get(dn)
            if not su or not sd:
                fails.append('줄 %s 또는 %s 가 화면에 없다' % (up, dn))
                continue
            gap = sd[0] - su[1]
            print('  %s(%d~%d) → %s(%d~%d) 사이 %dpx'
                  % (up, su[0], su[1], dn, sd[0], sd[1], gap))
            if gap < 6:
                fails.append('줄 %s 와 %s 가 %dpx 로 붙거나 겹친다' % (up, dn, gap))
        over = pg.evaluate('document.documentElement.scrollWidth - '
                           'document.documentElement.clientWidth')
        if over > 0:
            fails.append('폭 1200: 가로로 %dpx 넘친다' % over)
        pg.set_viewport_size({'width': 390, 'height': 780})
        pg.wait_for_timeout(600)
        over_m = pg.evaluate('document.documentElement.scrollWidth - '
                             'document.documentElement.clientWidth')
        pg.screenshot(path=os.path.join(OUT, 'mobile.png'))
        if over_m > 0:
            fails.append('폭 390: 가로로 %dpx 넘친다' % over_m)
        print('가로 넘침 — 1200: %d · 390: %d' % (over, over_m))
        b.close()
    page = io.open(PAGE, encoding='utf-8').read()
    scene = page[page.find('<svg'):page.find('</svg>') + 6]
    for h in (check_fig.hits(scene) or []):
        fails.append('배치: ' + h)
    for f in fails:
        print('FAIL', f)
    print('요약: 시점 %d개 / FAIL %d' % (len(MARKS), len(fails)))
    return len(fails)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.exit(1 if main() else 0)
