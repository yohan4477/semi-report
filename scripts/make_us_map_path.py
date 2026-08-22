# -*- coding: utf-8 -*-
"""미국 본토 윤곽을 SVG path 한 줄로 굽는다 — data/us_lower48_albers_path.txt.

손으로 찍은 다각형으로 지도를 그렸더니 「너무 허접하다」는 말을 들었다(2026-08-23).
그래서 실제 경계 데이터를 받아 앨버스 정적원추도법으로 투영해 굽는다. 결과 파일만
저장소에 두고 대시보드 생성기는 그 파일을 읽는다 — 그림을 그릴 때마다 인터넷을
타지 않게 하려는 것이다.

원본: PublicaMundi/MappingAPI us-states.json (미국 주 경계, 공개 자료)
투영: Albers Equal Area Conic (표준위도 29.5°N·45.5°N, 중앙자오선 96°W) — 미국
      본토 지도의 표준이다. 위도가 높을수록 가로로 벌어지는 왜곡을 잡아 준다
정리: 알래스카·하와이·푸에르토리코를 뺀 49개 도형, 1.1px보다 촘촘한 점은 버린다

    python scripts/make_us_map_path.py

좌표계는 가로 596 · 세로 370이고 왼쪽 위 여백이 (14, 36)이다. 위도·경도를 화면
좌표로 바꾸는 식이 필요하면 이 파일의 xy()를 그대로 쓴다 — 지도와 표시가 어긋나면
십중팔구 여기 상수와 생성기 쪽 상수가 다른 것이다.
"""
import io, json, math, os, sys, urllib.request

SRC = ('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/'
       'master/data/geojson/us-states.json')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'us_lower48_albers_path.txt')
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
    rings = []
    for f in feats:
        g = f['geometry']
        polys = [g['coordinates']] if g['type'] == 'Polygon' else g['coordinates']
        for poly in polys:
            rings += [[proj(a, b) for a, b in ring] for ring in poly]
    xs = [p[0] for r in rings for p in r]
    ys = [p[1] for r in rings for p in r]
    minx, maxx, maxy = min(xs), max(xs), max(ys)
    sc = W / (maxx - minx)

    def xy(p):                      # 북쪽이 위로 오게 세로를 뒤집는다
        return (p[0] - minx) * sc + OX, (maxy - p[1]) * sc + OY

    segs = []
    for ring in rings:
        if len(ring) < 4:
            continue
        pts = [xy(p) for p in ring]
        keep = [pts[0]]
        for q in pts[1:-1]:
            if (q[0] - keep[-1][0]) ** 2 + (q[1] - keep[-1][1]) ** 2 >= EPS * EPS:
                keep.append(q)
        keep.append(pts[-1])
        s = ['%.0f %.0f' % q for q in keep]
        s = [s[0]] + [q for i, q in enumerate(s[1:], 1) if q != s[i - 1]]
        if len(s) < 4:
            continue
        segs.append('M' + s[0] + 'L' + 'L'.join(s[1:]) + 'Z')
    path = ''.join(segs)
    io.open(OUT, 'w', encoding='utf-8').write(path)
    sys.stdout.write('%d조각 / %d자 -> %s\n' % (len(segs), len(path), OUT))


if __name__ == '__main__':
    main()
