# -*- coding: utf-8 -*-
"""밸류체인 탐색기 선 규약 — 세로 이동이 칸 사이 통로에서 한 번만 일어나나.

FAIL 0 이어야 푸시한다. 규약은 scripts/gen_vcexplorer.py 의 route/place.
  R1 세로 구간이 상자가 선 칸 안에 들어갔나
  R2 세로 구간이 통로 한가운데에서 ±10px 밖으로 나갔나
  R3 타겟 왼쪽에서 타겟으로 가는 선이 아래로 꺾었나 (왼쪽은 위로만)
  R4 타겟 오른쪽에서 타겟에서 나가는 선이 위로 꺾었나 (오른쪽은 아래로만)
  R5 한 선에 세로 구간이 둘 이상인가 (상자를 피하려 여러 번 꺾었나)
  R6 직접 선이 둘 넘게 꺾였나 (곧은 구간이 넷 이상)
  R7 가로 구간이 중간 칸의 상자를 가로지르나 (place 가 빈 자리를 못 잡았다)
  R8 선 끝이 닿을 상자 높이 밖인가 (route 가 상자를 비키려 높이를 옮겼다)
  R9 프로젝트 테두리에 선이 닿았나 (테두리는 관계의 끝점이 아니다)

R5·R6·R7 은 프레임워크 §22-G·H 다. 상자를 피하는 일은 「더 일찍·더 길게 한 번 옮기기」로
풀고 「여러 번 꺾기」로 풀지 않는다. 통로를 하나 고르면 그 앞은 출발 높이로, 그 뒤는
닿을 높이로 곧게 간다 — 꺾임은 둘을 넘지 않는다.

타겟 칸을 가로지르는 선은 방향을 안 본다 — 왼쪽 공급사가 오른쪽 프로젝트에 바로
대는 꼴이라 한쪽 규칙으로 재면 반대쪽이 늘 어긋난다.

방향은 선이 가는 쪽으로 잰다. 타겟에서 왼쪽으로 나가는 선(합작사·법인)은 같은 자리를
거꾸로 지나므로 아래로 꺾는 것이 맞다 — 상자 차례가 같으면 두 꼴은 한 규칙이다.

브라우저로 사슬을 하나씩 열어 그려진 경로를 읽는다. 사슬 목록은 chain.json 에서 읽는다.
곧은 선(같은 높이)과 같은 칸끼리 잇는 곡선은 세로 구간이 아니라 안 본다.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, '대시보드', '밸류체인 탐색기.html')
DATA = os.path.join(ROOT, 'data', 'valuechain')
COL_W = 156.0
COL_GAP = 56.0
LANE_MAX = 10.0
TOL = 1.0
CLR = 6.0

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


def chain_labels():
    """실리는 사슬의 (타겟 id, 이름). 판은 주소의 focal= 로 바로 연다 — 첫 화면이 회사
    목록이 아니라 판이 된 뒤(2026-09-11)로는 이름을 눌러 여는 길이 없다."""
    ents = dict((e['id'], e) for e in json.load(
        io.open(os.path.join(DATA, 'entities.json'), encoding='utf-8')))
    base = os.path.join(DATA, 'chains')
    out = []
    for d in sorted(os.listdir(base)):
        cp = os.path.join(base, d, 'chain.json')
        if not os.path.exists(cp):
            continue
        meta = json.load(io.open(cp, encoding='utf-8'))
        fid = meta.get('focal_entity')
        e = ents.get(fid, {})
        out.append((fid, e.get('name_ko') or e.get('name') or meta.get('label')))
    return out


def check(page, fid, label):
    page.goto('file:///' + PAGE.replace(os.sep, '/') + '?focal=' + fid + '&mode=current')
    page.wait_for_timeout(2600)
    data = page.evaluate("""() => ({
      focal: (function(){
        var n = document.querySelector('.react-flow__node .nd.focal');
        var box = n && n.closest('.react-flow__node');
        if (!box) return null;
        var m = /translate\\((-?[\\d.]+)px, *(-?[\\d.]+)px\\)/.exec(box.style.transform || '');
        return m ? parseFloat(m[1]) : null;
      })(),
      boxes: Array.from(document.querySelectorAll('.react-flow__node'))
        .filter(function(n){ return n.querySelector('.nd'); })
        .map(function(n){
          var m = /translate\\((-?[\\d.]+)px, *(-?[\\d.]+)px\\)/.exec(n.style.transform || '');
          var r = n.getBoundingClientRect();
          return m ? { x: parseFloat(m[1]), y: parseFloat(m[2]), h: n.offsetHeight } : null;
        }).filter(function(x){ return x; }),
      projs: Array.from(document.querySelectorAll('.react-flow__node'))
        .filter(function(n){ return n.querySelector('.proj'); })
        .map(function(n){
          var m = /translate\\((-?[\\d.]+)px, *(-?[\\d.]+)px\\)/.exec(n.style.transform || '');
          var p = n.querySelector('.proj');
          return m ? { x: parseFloat(m[1]), y: parseFloat(m[2]),
                       w: p.offsetWidth, h: p.offsetHeight } : null;
        }).filter(function(x){ return x; }),
      paths: Array.from(document.querySelectorAll('.react-flow__edge-path'))
        .map(function(p){ return p.getAttribute('d'); })
    })""")
    boxes = data['boxes']
    cols = sorted(set(round(b['x'], 1) for b in boxes))
    if not cols:
        fails.append(u'FAIL %s — 상자를 하나도 못 읽었다' % label)
        return 0
    fx = data['focal']
    if fx is None:
        fails.append(u'FAIL %s — 타겟 상자를 못 읽었다' % label)
        return 0
    spines = [c + COL_W + COL_GAP / 2 for c in cols]

    def col_at(x):
        for c in cols:
            if c - TOL <= x <= c + COL_W + TOL:
                return c
        return None

    def box_hit(c, y):
        for b in boxes:
            if round(b['x'], 1) != c:
                continue
            if b['y'] - CLR < y < b['y'] + b['h'] + CLR:
                return b
        return None

    n = 0
    for d in data['paths']:
        if not d:
            continue
        segs = segments(d)
        if not segs:
            continue
        # 선이 가는 쪽 — 오른쪽으로 가면 1, 왼쪽으로 가면 -1
        dirx = 1 if segs[-1][1][0] >= segs[0][0][0] else -1
        ax, bx = segs[0][0][0], segs[-1][1][0]
        crosses = min(ax, bx) < fx and max(ax, bx) > fx + COL_W
        # R6 — 곧은 구간이 넷 이상이면 꺾임이 둘을 넘는다
        if len(segs) > 4:
            fails.append(u'FAIL %s — 직접 선이 %d 번 꺾였다 (둘까지)' % (label, len(segs) - 1))
        vert = 0
        for (x0, y0), (x1, y1) in segs:
            if abs(x1 - x0) <= 0.6 and abs(y1 - y0) > 2:
                vert += 1
                n += 1
                x = (x0 + x1) / 2
                if col_at(x) is not None:
                    fails.append(u'FAIL %s — 세로 구간이 상자 칸 안이다 (x=%.1f)' % (label, x))
                    continue
                if not any(abs(x - s) <= LANE_MAX + TOL for s in spines):
                    fails.append(u'FAIL %s — 세로 구간이 통로 밖이다 (x=%.1f)' % (label, x))
                    continue
                if crosses:
                    continue
                dy = y1 - y0
                if x < fx and dirx * dy > TOL:
                    fails.append(u'FAIL %s — 타겟 왼쪽에서 꺾는 쪽이 거꾸로다 (x=%.1f, %.1f→%.1f)'
                                 % (label, x, y0, y1))
                if x > fx + COL_W and dirx * dy < -TOL:
                    fails.append(u'FAIL %s — 타겟 오른쪽에서 꺾는 쪽이 거꾸로다 (x=%.1f, %.1f→%.1f)'
                                 % (label, x, y0, y1))
                continue
            if abs(y1 - y0) <= 0.6 and abs(x1 - x0) > COL_W:
                # R7 — 가로 구간이 지나는 중간 칸마다 그 높이에 상자가 있으면 가로지른 것이다
                lo, hi = min(x0, x1), max(x0, x1)
                for c in cols:
                    if c > lo + TOL and c + COL_W < hi - TOL:
                        b = box_hit(c, y0)
                        if b:
                            fails.append(u'FAIL %s — 가로 구간(y=%.1f)이 칸 %.0f 의 상자를 가로지른다'
                                         % (label, y0, c))
        if vert > 1:
            fails.append(u'FAIL %s — 한 선이 세로로 %d 번 꺾었다 (통로 하나에서 끝낸다)'
                         % (label, vert))
        # R8 — 선 끝이 닿을 상자 높이 안에 있나
        ex, ey = segs[-1][1]
        c = col_at(ex + (2 if dirx > 0 else -2))
        if c is not None and not box_hit(c, ey):
            fails.append(u'FAIL %s — 선 끝(%.1f, %.1f)이 상자 높이 밖이다' % (label, ex, ey))
        # R9 — 선 끝이 프로젝트 테두리 변에 붙었나 (상자에 붙어야 한다)
        for p in data['projs']:
            on_edge = (abs(ex - p['x']) <= TOL or abs(ex - (p['x'] + p['w'])) <= TOL) \
                and p['y'] - TOL <= ey <= p['y'] + p['h'] + TOL
            if on_edge and c is None:
                fails.append(u'FAIL %s — 선이 프로젝트 테두리에 닿았다 (%.1f, %.1f)' % (label, ex, ey))
    return n


def main():
    import playwright.sync_api as pw
    total = 0
    labels = chain_labels()
    with pw.sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={'width': 1500, 'height': 1100})
        for fid, label in labels:
            total += check(page, fid, label)
        b.close()
    for f in fails[:30]:
        print(f)
    print(u'요약: 사슬 %d · 세로 구간 %d개 / FAIL %d' % (len(labels), total, len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
