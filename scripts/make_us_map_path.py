# -*- coding: utf-8 -*-
"""미국 본토를 주별 SVG path로 굽는다 — data/us_lower48_albers.json.

손으로 서른세 점 찍어 그린 윤곽을 지도라고 내놨더니 「너무 허접하다」는 말을 들었고,
그다음에는 표시를 위도·경도로 점 찍어 올렸더니 라벨 자리를 손으로 잡게 되어 그림과
어긋났다(둘 다 2026-08-23). 그래서 주 단위로 굽는다 — 주를 통째로 칠하면 어긋날 수가
없다. 칠하는 면이 곧 경계 자료 그 자체다. 지시선을 걸 자리도 손으로 찍지 않게 주마다
경계 상자 한가운데를 같이 내보낸다.

원본: PublicaMundi/MappingAPI us-states.json (미국 주 경계, 공개 자료)
투영: Albers Equal Area Conic (표준위도 29.5°N·45.5°N, 중앙자오선 96°W) — 미국
      본토 지도의 표준이다. 위도가 높을수록 가로로 벌어지는 왜곡을 잡아 준다
정리: 알래스카·하와이·푸에르토리코를 뺀 49개, 1.1px보다 촘촘한 점은 버린다

    python scripts/make_us_map_path.py

산출물은 {'size': [가로, 세로], 'states': {주 이름: path}, 'center': {주 이름: [x, y]}}
꼴이다. 좌표계는 가로 596 · 세로는 투영 결과대로이고 왼쪽 위 여백이 (14, 36)이다.
"""
import io
import json
import math
import os
import sys
import urllib.request

SRC = ('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/'
       'master/data/geojson/us-states.json')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'us_lower48_albers.json')
DROP = {'Alaska', 'Hawaii', 'Puerto Rico'}
LAT0, LON0, LAT1, LAT2 = 37.5, -96.0, 29.5, 45.5
W, OX, OY, EPS = 596.0, 14.0, 36.0, 1.1

_r = math.radians
_n = (math.sin(_r(LAT1)) + math.sin(_r(LAT2))) / 2
_C = math.cos(_r(LAT1)) ** 2 + 2 * _n * math.sin(_r(LAT1))
_rho0 = math.sqrt(_C - 2 * _n * math.sin(_r(LAT0))) / _n


def proj(lon, lat):
    rho = math.sqrt(_C - 2 * _n * math.sin(_r(lat))) / _n
    th = _n * _r(lon - LON0)
    return rho * math.sin(th), _rho0 - rho * math.cos(th)


def main():
    with urllib.request.urlopen(SRC) as f:
        d = json.loads(f.read().decode('utf-8'))
    feats = [f for f in d['features'] if f['properties']['name'] not in DROP]
    rings = {}
    for f in feats:
        g = f['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        rings[f['properties']['name']] = [[proj(a, b) for a, b in ring]
                                          for poly in polys for ring in poly]
    pts = [p for rs in rings.values() for r in rs for p in r]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    maxy = max(p[1] for p in pts)
    sc = W / (maxx - minx)

    def xy(p):                      # 북쪽이 위로 오게 세로를 뒤집는다
        return (p[0] - minx) * sc + OX, (maxy - p[1]) * sc + OY

    out = {'size': [W + OX * 2, 0.0], 'states': {}, 'center': {}}
    bottom = 0.0
    for name, rs in rings.items():
        segs, kept = [], []
        for ring in rs:
            if len(ring) < 4:
                continue
            q = [xy(p) for p in ring]
            keep = [q[0]]
            for c in q[1:-1]:
                if (c[0] - keep[-1][0]) ** 2 + (c[1] - keep[-1][1]) ** 2 >= EPS * EPS:
                    keep.append(c)
            keep.append(q[-1])
            s = ['%.0f %.0f' % c for c in keep]
            s = [s[0]] + [v for i, v in enumerate(s[1:], 1) if v != s[i - 1]]
            if len(s) < 4:
                continue
            segs.append('M' + s[0] + 'L' + 'L'.join(s[1:]) + 'Z')
            kept += keep
            bottom = max(bottom, max(c[1] for c in keep))
        if not segs:
            continue
        out['states'][name] = ''.join(segs)
        # 점 평균이 아니라 경계 상자 한가운데를 쓴다. 섬이 딸린 주(루이지애나·플로리다)에서
        # 평균은 섬 쪽으로 끌려간다 — 지시선을 걸 자리로는 상자 한가운데가 낫다
        xs = [c[0] for c in kept]
        ys = [c[1] for c in kept]
        out['center'][name] = [round((min(xs) + max(xs)) / 2, 1),
                               round((min(ys) + max(ys)) / 2, 1)]
    out['size'][1] = round(bottom + OY, 1)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    n = sum(len(v) for v in out['states'].values())
    print('%d states / path %d chars / canvas %.0f x %.0f -> %s'
          % (len(out['states']), n, out['size'][0], out['size'][1], OUT))
    for k in ('Pennsylvania', 'West Virginia', 'Ohio', 'New York',
              'Texas', 'Louisiana'):
        if k in out['center']:
            print('  %-14s %s' % (k, out['center'][k]))


if __name__ == '__main__':
    main()
