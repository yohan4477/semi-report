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
                out.append((sum(p[0] for p in pts) / len(pts),
                            sum(p[1] for p in pts) / len(pts), len(pts)))
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
            for bx, by, n in blobs(px, box, c):
                pts.append([name, round(fx(bx)), round(fy(by))])
        out[key] = {'grid_y': gy, 'grid_x': gx, 'points': pts}
        print('  %-6s 격자 y%s x%s / 점 %d개' % (key, gy, gx, len(pts)))
    return out


def main():
    data = {}
    data['calib'] = do_calib()
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False))
    print('->', OUT)


if __name__ == '__main__':
    main()
