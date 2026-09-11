# -*- coding: utf-8 -*-
"""밸류체인 탐색기 선 규약 — 세로 이동이 칸 사이 통로에서만 일어나나.

FAIL 0 이어야 푸시한다. 규약은 scripts/gen_vcexplorer.py 의 gutterX.
  R1 세로 구간이 상자가 선 칸 안에 들어갔나
  R2 세로 구간이 통로 한가운데에서 ±10px 밖으로 나갔나

브라우저로 사슬을 하나씩 열어 그려진 경로를 읽는다. 곧은 선(같은 높이)과 같은 칸끼리
잇는 곡선은 세로 구간이 아니라 안 본다.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')
COL_W = 128.0
COL_GAP = 48.0
LANE_MAX = 10.0
TOL = 1.0

fails = []


def segments(d):
    """경로 문자열에서 곧은 구간만 뽑는다. Q 는 모서리라 지나간다."""
    toks = re.findall(r'[MLQ]|-?\d+(?:\.\d+)?', d)
    out = []
    i, cur = 0, None
    while i < len(toks):
        t = toks[i]
        if t == 'M':
            cur = (float(toks[i + 1]), float(toks[i + 2]))
            i += 3
        elif t == 'L':
            nxt = (float(toks[i + 1]), float(toks[i + 2]))
            if cur:
                out.append((cur, nxt))
            cur = nxt
            i += 3
        elif t == 'Q':
            cur = (float(toks[i + 3]), float(toks[i + 4]))
            i += 5
        else:
            i += 1
    return out


def check(page, label):
    page.goto('file:///' + PAGE.replace(os.sep, '/'))
    page.wait_for_timeout(1200)
    page.get_by_text(label, exact=True).first.click()
    page.wait_for_timeout(2500)
    data = page.evaluate("""() => ({
      cols: Array.from(document.querySelectorAll('.react-flow__node')).map(function(n){
        var m = /translate\\((-?[\\d.]+)px, *(-?[\\d.]+)px\\)/.exec(n.style.transform || '');
        return m ? parseFloat(m[1]) : null;
      }).filter(function(x){ return x !== null; }),
      paths: Array.from(document.querySelectorAll('.react-flow__edge-path'))
        .map(function(p){ return p.getAttribute('d'); })
    })""")
    cols = sorted(set(round(x, 1) for x in data['cols']))
    if not cols:
        fails.append(u'FAIL %s — 상자를 하나도 못 읽었다' % label)
        return 0
    spines = [c + COL_W + COL_GAP / 2 for c in cols]
    n = 0
    for d in data['paths']:
        if not d:
            continue
        for (x0, y0), (x1, y1) in segments(d):
            if abs(x1 - x0) > 0.6 or abs(y1 - y0) <= 2:
                continue
            n += 1
            x = (x0 + x1) / 2
            inside = [c for c in cols if c - TOL <= x <= c + COL_W + TOL]
            if inside:
                fails.append(u'FAIL %s — 세로 구간이 상자 칸 안이다 (x=%.1f, 칸 %.1f~%.1f)'
                             % (label, x, inside[0], inside[0] + COL_W))
                continue
            if not any(abs(x - s) <= LANE_MAX + TOL for s in spines):
                fails.append(u'FAIL %s — 세로 구간이 통로 밖이다 (x=%.1f)' % (label, x))
    return n


def main():
    import playwright.sync_api as pw
    total = 0
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width': 1500, 'height': 1100})
        for label in ('태양유전', '대덕전자', '블룸에너지'):
            total += check(page, label)
        b.close()
    for f in fails[:20]:
        print(f)
    print(u'요약: 세로 구간 %d개 / FAIL %d' % (total, len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
