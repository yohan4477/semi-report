# -*- coding: utf-8 -*-
"""원문 도해에서 값을 읽어 data/epoch_fig_data.json 으로 굽는다.

Epoch AI 원문 그림을 한국어로 다시 그릴 때, 점과 막대의 자리를 눈으로 어림해
옮기면 반드시 어긋난다(insight-figure 규칙 2). 이미지에서 색으로 도형을 찾아
데이터 좌표로 되돌린 값만 그림이 쓴다.

  py -3.13 scratchpad/epoch_extract.py

원본 이미지는 scratchpad/epoch_src/*.webp 에 둔다(다시 받으려면 SRC 참조).
"""
import io
import json
import os
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRCDIR = os.path.join(HERE, 'epoch_src')
OUT = os.path.join(ROOT, 'data', 'epoch_fig_data.json')

SRC = 'https://epoch.ai/assets/images/gradient-updates/'


def load(name):
    im = Image.open(os.path.join(SRCDIR, name + '.webp')).convert('RGB')
    return im, im.load(), im.size


def near(c, t, tol=40):
    return all(abs(a - b) <= tol for a, b in zip(c, t))


def blobs(px, box, color, tol=42, minpx=18):
    """상자 안에서 그 색 덩어리를 찾아 가운데 좌표를 돌려준다."""
    x0, y0, x1, y1 = box
    seen = set()
    out = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not near(px[x, y], color, tol):
                continue
            stack, pts = [(x, y)], []
            seen.add((x, y))
            while stack:
                a, b = stack.pop()
                pts.append((a, b))
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (a + da, b + db)
                    if (n in seen or not (x0 <= n[0] < x1 and y0 <= n[1] < y1)
                            or not near(px[n[0], n[1]], color, tol)):
                        continue
                    seen.add(n)
                    stack.append(n)
            if len(pts) >= minpx:
                bx0, bx1 = min(p[0] for p in pts), max(p[0] for p in pts)
                by0, by1 = min(p[1] for p in pts), max(p[1] for p in pts)
                out.append((sum(p[0] for p in pts) / len(pts),
                            sum(p[1] for p in pts) / len(pts), len(pts),
                            bx1 - bx0 + 1, by1 - by0 + 1))
    return out


def round_blobs(px, box, color, tol=34, rlo=7, rhi=16):
    """동그란 표식만 남긴다 — 글자와 선은 가로세로 비가 어긋나 걸러진다."""
    out = []
    for bx, by, n, w, h in blobs(px, box, color, tol=tol, minpx=int(3.14 * rlo * rlo * 0.6)):
        if not (rlo * 2 - 2 <= w <= rhi * 2 + 2 and rlo * 2 - 2 <= h <= rhi * 2 + 2):
            continue
        if abs(w - h) > 5:
            continue
        out.append((bx, by, n))
    return out


def logscale(p0, v0, p1, v1):
    """두 눈금 자리와 값으로 로그 축을 세운다."""
    import math
    lg0, lg1 = math.log10(v0), math.log10(v1)

    def f(p):
        return 10 ** (lg0 + (p - p0) * (lg1 - lg0) / (p1 - p0))
    return f


def do_calib():
    """이론값 대 보정값 산점도 둘. 축은 둘 다 로그다."""
    _, px, (W, H) = load('calib')
    # 축 눈금 자리는 격자선으로 잡는다
    def grids(box, axis):
        x0, y0, x1, y1 = box
        hit = []
        if axis == 'y':
            for y in range(y0, y1):
                n = sum(1 for x in range(x0, x1, 3)
                        if abs(px[x, y][0] - px[x, y][1]) < 8 and 200 < px[x, y][0] < 240)
                if n > (x1 - x0) // 6:
                    hit.append(y)
        else:
            for x in range(x0, x1):
                n = sum(1 for y in range(y0, y1, 3)
                        if abs(px[x, y][0] - px[x, y][1]) < 8 and 200 < px[x, y][0] < 240)
                if n > (y1 - y0) // 6:
                    hit.append(x)
        g, cur = [], [hit[0]]
        for v in hit[1:]:
            if v - cur[-1] <= 3:
                cur.append(v)
            else:
                g.append(sum(cur) // len(cur))
                cur = [v]
        g.append(sum(cur) // len(cur))
        return g

    panels = {'uncal': (44, 230, 592, 510), 'cal': (616, 230, 1160, 510)}
    colors = {'B200': (37, 82, 224), 'B300': (150, 110, 216),
              'GB200': (26, 178, 160), 'H200': (232, 92, 60)}
    out = {}
    for key, box in panels.items():
        gy = grids(box, 'y')          # 10^4, 10^3, 10^2
        gx = grids(box, 'x')          # 10^2, 10^3, 10^4
        assert len(gy) >= 3 and len(gx) >= 3, (key, gy, gx)
        fy = logscale(gy[0], 1e4, gy[-1], 1e2)
        fx = logscale(gx[0], 1e2, gx[-1], 1e4)
        pts = []
        for name, c in colors.items():
            for bx, by, n in round_blobs(px, box, c, tol=46, rlo=4, rhi=13):
                pts.append([name, round(fx(bx)), round(fy(by))])
        out[key] = {'grid_y': gy, 'grid_x': gx, 'points': pts}
        print('  %-6s 격자 y%s x%s / 점 %d개' % (key, gy, gx, len(pts)))
    return out


def gridlines(px, box, axis, lo=200, hi=240, frac=6):
    """옅은 회색 격자선 자리를 찾는다."""
    x0, y0, x1, y1 = box
    hit = []
    rng = range(y0, y1) if axis == 'y' else range(x0, x1)
    for v in rng:
        if axis == 'y':
            n = sum(1 for x in range(x0, x1, 3)
                    if abs(px[x, v][0] - px[x, v][1]) < 8 and lo < px[x, v][0] < hi)
            tot = (x1 - x0) // 3
        else:
            n = sum(1 for y in range(y0, y1, 3)
                    if abs(px[v, y][0] - px[v, y][1]) < 8 and lo < px[v, y][0] < hi)
            tot = (y1 - y0) // 3
        if n > tot // frac * 2:
            hit.append(v)
    if not hit:
        return []
    g, cur = [], [hit[0]]
    for v in hit[1:]:
        if v - cur[-1] <= 3:
            cur.append(v)
        else:
            g.append(sum(cur) // len(cur))
            cur = [v]
    g.append(sum(cur) // len(cur))
    return g


def do_openai_line():
    """세계 총계와 오픈AI의 H100 환산 누적치. 세로 자는 로그다."""
    _, px, (W, H) = load('openai-line')
    gy = gridlines(px, (170, 400, 940, 920), 'y')
    gx = gridlines(px, (170, 320, 960, 900), 'x')
    fy = logscale(gy[0], 1e7, gy[-1], 1e5)
    blue = lambda c: (c[2] > 180 and c[0] < 80 and c[1] < 120)
    teal = lambda c: (c[0] < 90 and 140 < c[1] < 205 and 140 < c[2] < 200)

    def runs_at(x, f):
        ys = [y for y in range(300, 915) if f(px[x, y])]
        runs, cur = [], []
        for y in ys:
            if cur and y - cur[-1] > 2:
                runs.append(cur)
                cur = []
            cur.append(y)
        if cur:
            runs.append(cur)
        return [sum(r) / len(r) for r in runs if len(r) <= 16]

    def series(f):
        """선이 지나는 자리를 고른다. 오른쪽 라벨 글자가 같은 색이라, 앞 점에서
        가장 가깝게 이어지는 자리를 골라야 글자에 안 물린다."""
        out, prev = [], None
        for x in gx:
            cand = runs_at(x, f)
            if not cand:
                out.append(None)
                continue
            y = cand[0] if prev is None else min(cand, key=lambda v: abs(v - prev))
            prev = y
            out.append(round(fy(y)))
        return out
    out = {'grid_y': gy, 'grid_x': gx, 'world': series(blue), 'openai': series(teal)}
    print('  openai-line 세로격자%s / 세계%s' % (gy, out['world']))
    print('              오픈AI%s' % (out['openai'],))
    return out


def do_by_chip():
    """엔비디아 세대별 스택 막대. 구간 경계를 색으로 읽는다."""
    _, px, (W, H) = load('openai-by-chip')
    gy = gridlines(px, (120, 350, 940, 920), 'y')
    # 1750k, 1250k, 750k 순
    k = (gy[2] - gy[0]) / 1000.0            # 1k 당 픽셀
    zero = gy[2] + 750 * k

    def cls(c):
        r, g, b = c
        if r > 200 and 120 < g < 190 and b < 60:
            return 'Blackwell'
        if r < 80 and 130 < g < 190 and 140 < b < 190:
            return 'Hopper'
        if r < 80 and 90 < g < 160 and b > 190:
            return 'Ampere'
        return None
    out = {'zero_y': round(zero, 1), 'px_per_k': round(k, 4), 'bars': []}
    for cx, year, mw in ((295, 2023, 200), (561, 2024, 600), (828, 2025, 1900)):
        tops = {}
        for y in range(400, 900):
            t = cls(px[cx, y])
            if t and t not in tops:
                tops[t] = y
        cum = {t: round((zero - y) / k) for t, y in tops.items()}
        order = ['Ampere', 'Hopper', 'Blackwell']
        seg, prev = {}, 0
        for t in order:
            if t in cum:
                seg[t] = cum[t] - prev
                prev = cum[t]
        out['bars'].append({'year': year, 'mw': mw, 'cum': cum, 'seg': seg,
                            'total': max(cum.values())})
        print('  by-chip %d (%dMW) 구간%s 합계%d' % (year, mw, seg, max(cum.values())))
    return out


def do_cyber_eci(name, ylo, yhi, key, y_top=None, per_line=10.0):
    """Cyber-ECI 산점도. 세로는 ECI, 가로는 공개일이다.

    자는 격자 간격에서 뽑는다. 찾은 격자가 몇 줄이냐로 나누면 안 된다 —
    맨 아래 줄이 상자 밖으로 잘리면 자가 통째로 어긋난다. 2026-08-25에 그래서
    cybereci 의 모든 점이 33% 눌려 있었다(회색 점 하나가 축 아래로 빠져 있었다)."""
    _, px, (W, H) = load(name)
    gy = gridlines(px, (110, 330, 950, 1010), 'y')
    gx = gridlines(px, (110, 330, 950, 940), 'x')
    # 점을 훑는 상자는 격자보다 넓게 잡는다 — 첫 눈금 왼쪽에도 점이 있다.
    # 좁게 잡았다가 cybereci 의 맨 왼쪽 점 하나를 통째로 빠뜨렸다(2026-08-25)
    box = (50, 330, 1010, 1030)
    assert len(gy) >= 2, gy
    gap = (gy[-1] - gy[0]) / float(len(gy) - 1)
    top = yhi if y_top is None else y_top

    def fy(y):
        return top - (y - gy[0]) * per_line / gap
    colors = {'teal': (26, 178, 160), 'pink': (226, 62, 140), 'blue': (30, 90, 230),
              'gray': (200, 200, 200)}
    pts = {}
    for cname, c in colors.items():
        got = []
        for bx, by, n in round_blobs(px, box, c, rlo=7, rhi=14):
            got.append([round(bx), round(fy(by), 1)])
        pts[cname] = sorted(got)
    out = {'grid_y': gy, 'grid_x': gx, 'y_lo': ylo, 'y_hi': yhi, 'points': pts}
    print('  %s 격자y%s / 점 %s' % (key, gy, {k: len(v) for k, v in pts.items()}))
    return out


def do_cve():
    """월별 CVE 수. 두 줄(치명·고위험)을 색으로 갈라 읽는다."""
    _, px, (W, H) = load('cve')
    gy = gridlines(px, (60, 100, 1150, 500), 'y', lo=205, hi=245, frac=5)
    hi = lambda c: (c[0] > 210 and 90 < c[1] < 160 and c[2] < 90)
    cr = lambda c: (c[0] > 190 and c[1] < 90 and 110 < c[2] < 190)
    out = {'grid_y': gy, 'high': [], 'critical': []}
    print('  cve 격자y%s (%d개)' % (gy[:4], len(gy)))
    return out


def main():
    data = {}
    data['calib'] = do_calib()
    data['openai_line'] = do_openai_line()
    data['by_chip'] = do_by_chip()
    data['cyber_eci'] = do_cyber_eci('cybereci', 135, 175, 'cybereci')
    data['cyber_prog'] = do_cyber_eci('cyberprog', 140, 180, 'cyberprog')
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False))
    print('->', OUT)


if __name__ == '__main__':
    main()
