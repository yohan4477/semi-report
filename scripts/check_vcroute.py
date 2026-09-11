# -*- coding: utf-8 -*-
"""밸류체인 탐색기 선 규약 — 세로 이동이 칸 사이 통로에서만 일어나나.

FAIL 0 이어야 푸시한다. 규약은 scripts/gen_vcexplorer.py 의 gutterX.
  R1 세로 구간이 상자가 선 칸 안에 들어갔나
  R2 세로 구간이 통로 한가운데에서 ±10px 밖으로 나갔나
  R3 타겟 왼쪽에서 타겟으로 가는 선이 아래로 꺾었나 (왼쪽은 위로만)
  R4 타겟 오른쪽에서 타겟에서 나가는 선이 위로 꺾었나 (오른쪽은 아래로만)
  R5 한 선에 세로 구간이 둘 이상인가 (상자를 피하려 여러 번 꺾었나)

R5 는 프레임워크 §22-G·H 다. 상자를 피하는 일은 「더 일찍·더 길게 한 번 옮기기」로
풀고 「여러 번 꺾기」로 풀지 않는다. 통로를 하나 고르면 그 앞은 출발 높이로, 그 뒤는
닿을 높이로 곧게 간다 — 꺾임은 둘을 넘지 않는다.

타겟 칸을 가로지르는 선은 방향을 안 본다 — 왼쪽 공급사가 오른쪽 프로젝트에 바로
대는 꼴이라 한쪽 규칙으로 재면 반대쪽이 늘 어긋난다.

방향은 선이 가는 쪽으로 잰다. 타겟에서 왼쪽으로 나가는 선(합작사·법인)은 같은 자리를
거꾸로 지나므로 아래로 꺾는 것이 맞다 — 상자 차례가 같으면 두 꼴은 한 규칙이다.

브라우저로 사슬을 하나씩 열어 그려진 경로를 읽는다. 곧은 선(같은 높이)과 같은 칸끼리
잇는 곡선은 세로 구간이 아니라 안 본다. 프로젝트 테두리는 칸이 아니라 세지 않는다.
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
      focal: (function(){
        var n = document.querySelector('.react-flow__node .nd.focal');
        var box = n && n.closest('.react-flow__node');
        if (!box) return null;
        var m = /translate\((-?[\d.]+)px, *(-?[\d.]+)px\)/.exec(box.style.transform || '');
        return m ? parseFloat(m[1]) : null;
      })(),
      cols: Array.from(document.querySelectorAll('.react-flow__node'))
        .filter(function(n){ return !n.querySelector('.proj'); })
        .map(function(n){
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
    fx = data['focal']
    if fx is None:
        fails.append(u'FAIL %s — 타겟 상자를 못 읽었다' % label)
        return 0
    spines = [c + COL_W + COL_GAP / 2 for c in cols]
    n = 0
    for d in data['paths']:
        if not d:
            continue
        segs = segments(d)
        if not segs:
            continue
        # 선이 가는 쪽 — 오른쪽으로 가면 1, 왼쪽으로 가면 -1
        dirx = 1 if segs[-1][1][0] >= segs[0][0][0] else -1
        # 타겟 칸을 가로지르는 선(왼쪽 공급사가 오른쪽 프로젝트에 바로 대는 꼴)은
        # 한쪽 규칙으로 못 잰다. 어느 쪽에서 보든 반대쪽이 어긋난다
        ax, bx = segs[0][0][0], segs[-1][1][0]
        crosses = min(ax, bx) < fx and max(ax, bx) > fx + COL_W
        vert = 0
        for (x0, y0), (x1, y1) in segs:
            if abs(x1 - x0) > 0.6 or abs(y1 - y0) <= 2:
                continue
            vert += 1
            n += 1
            x = (x0 + x1) / 2
            inside = [c for c in cols if c - TOL <= x <= c + COL_W + TOL]
            if inside:
                fails.append(u'FAIL %s — 세로 구간이 상자 칸 안이다 (x=%.1f, 칸 %.1f~%.1f)'
                             % (label, x, inside[0], inside[0] + COL_W))
                continue
            if not any(abs(x - s) <= LANE_MAX + TOL for s in spines):
                fails.append(u'FAIL %s — 세로 구간이 통로 밖이다 (x=%.1f)' % (label, x))
                continue
            # 왼쪽은 타겟 쪽으로 갈 때 위로만, 오른쪽은 타겟에서 멀어질 때 아래로만
            if crosses:
                continue
            dy = y1 - y0
            if x < fx and dirx * dy > TOL:
                fails.append(u'FAIL %s — 타겟 왼쪽에서 꺾는 쪽이 거꾸로다 (x=%.1f, %.1f→%.1f)'
                             % (label, x, y0, y1))
            if x > fx + COL_W and dirx * dy < -TOL:
                fails.append(u'FAIL %s — 타겟 오른쪽에서 꺾는 쪽이 거꾸로다 (x=%.1f, %.1f→%.1f)'
                             % (label, x, y0, y1))
        if vert > 1:
            fails.append(u'FAIL %s — 한 선이 세로로 %d 번 꺾었다 (통로 하나에서 끝낸다)'
                         % (label, vert))
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
