# -*- coding: utf-8 -*-
"""용어사전 카드 안에서 어텐션 장면이 실제로 도는지 본다.

읽는 자리는 카드 페이지(대시보드/glossary/…어텐션….html)다. 목록 장(용어사전.html)은
첫 화면이 최신순 이름 목록이고 본문은 접혀 있어서(dash_common 규약) 그 안의 SVG 는
크기 0 으로 잡힌다 — 그건 결함이 아니라 그 장의 설계다. 그래서 목록 장에서는 장면
마크업이 실려 있는지만 보고, 크기와 움직임은 카드 페이지에서 잰다.
"""
import io, os, sys
from playwright.sync_api import sync_playwright

PAGE = os.path.abspath(os.path.join('대시보드', '용어사전.html'))
CARD = os.path.abspath(os.path.join('대시보드', 'glossary'))
OUT = os.path.join('scratchpad', 'anim_shots')
MARKS = [1.0, 4.0, 6.5, 9.5, 12.5]


def run(pg, url, tag, fails):
    pg.goto(url)
    pg.wait_for_timeout(700)
    # 카드가 접혀 있으면 편다
    pg.evaluate("""() => {
        document.querySelectorAll('details').forEach(d => d.open = true);
        var s = document.getElementById('attn-scene');
        if (s) s.scrollIntoView({block:'center'});
    }""")
    pg.wait_for_timeout(500)
    box = pg.evaluate("""() => {
        var s = document.getElementById('attn-scene');
        if (!s) return null;
        var r = s.getBoundingClientRect();
        return {w: Math.round(r.width), h: Math.round(r.height)};
    }""")
    if not box:
        fails.append('%s: 장면 SVG 가 화면에 없다' % tag)
        return
    if tag.startswith('card') and (box['w'] < 200 or box['h'] < 120):
        fails.append('%s: 장면이 %dx%d 로 너무 작다' % (tag, box['w'], box['h']))
    print('%s 장면 크기 %dx%d' % (tag, box['w'], box['h']))
    prev, seen = 0.0, set()
    for t in MARKS:
        pg.wait_for_timeout(int((t - prev) * 1000))
        prev = t
        st = pg.evaluate("""() => {
            var s = document.getElementById('attn-scene');
            var caps = [].slice.call(s.querySelectorAll('.cap'));
            var bars = [].slice.call(s.querySelectorAll('.bar'));
            return {cap: caps.findIndex(e => +e.getAttribute('opacity') > 0.5),
                    on: caps.filter(e => +e.getAttribute('opacity') > 0.5).length,
                    bars: bars.filter(b => +b.getAttribute('height') > 0).length};
        }""")
        seen.add(st['cap'])
        print('  t=%4.1f초  자막 %d개(%d번) · 선 막대 %d' % (t, st['on'], st['cap'], st['bars']))
        if st['on'] != 1:
            fails.append('%s t=%.1f: 보이는 자막이 %d개다' % (tag, t, st['on']))
    if len(seen) < 3:
        fails.append('%s: 한 바퀴에서 자막이 %d개만 바뀐다 — 안 돈다' % (tag, len(seen)))
    over = pg.evaluate('document.documentElement.scrollWidth - '
                       'document.documentElement.clientWidth')
    if over > 0:
        fails.append('%s: 가로로 %dpx 넘친다' % (tag, over))
    pg.screenshot(path=os.path.join(OUT, 'glossary_%s.png' % tag))


def main():
    os.makedirs(OUT, exist_ok=True)
    fails = []
    cards = [f for f in os.listdir(CARD) if '어텐션' in f] if os.path.isdir(CARD) else []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={'width': 1280, 'height': 900})
        run(pg, 'file:///' + PAGE.replace(os.sep, '/'), 'list', fails)
        if not cards:
            fails.append('카드 페이지가 안 나왔다 — 장면을 읽을 자리가 없다')
        else:
            url = 'file:///' + os.path.join(CARD, cards[0]).replace(os.sep, '/')
            run(pg, url, 'card-pc', fails)
            pg.set_viewport_size({'width': 390, 'height': 820})
            run(pg, url, 'card-mobile', fails)
        b.close()
    for f in fails:
        print('FAIL', f)
    print('요약: 화면 %d벌 / FAIL %d' % (2 + (1 if cards else 0), len(fails)))
    return len(fails)


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.exit(1 if main() else 0)
