# -*- coding: utf-8 -*-
"""세계 지도를 나라별 SVG path로 굽는다 — data/world_robinson.json.

미국 안에서 벌어진 일은 미국 지도로 그리면 되는데(scripts/make_us_map_path.py),
LNG는 바다 건너 오가는 이야기라 그것만으로는 방향이 안 잡힌다. 카타르·호주에서
미국으로 들어오던 것이 미국에서 유럽·동북아로 나가게 된 것이 이 편의 뼈대다.

투영: Robinson. 메르카토르는 고위도를 부풀려 러시아·캐나다가 화면을 먹고,
      정거원통도법은 남북이 늘어난다. 로빈슨은 둘을 절충한 세계지도 표준이다.
정리: 남극을 뺀다(화면 아래를 다 먹는데 이 이야기와 무관하다). 2px보다 촘촘한
      점을 버리고, 화면에서 3px가 안 되는 조각(작은 섬)도 버린다. 가로 596으로 맞춘다
      -- 다른 도해와 글씨 크기가 같아야 한 카드 안에서 따로 놀지 않는다

    python scripts/make_world_map_path.py

산출물은 {'size': [가로, 세로], 'c': {나라: path}, 'center': {나라: [x, y]},
'at': {'경도,위도': [x, y]}} 꼴이다. center는 경계 상자 한가운데이고, 나라가
여러 대륙에 걸치면(프랑스·러시아) 쓸모가 없으니 잰 좌표가 필요하면 at을 쓴다.
"""
import io
import json
import math
import os
import urllib.request

SRC = ('https://raw.githubusercontent.com/johan/world.geo.json/'
       'master/countries.geo.json')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'data', 'world_robinson.json')
DROP = {'Antarctica'}
W, OX, OY, EPS, MINSEG = 596.0, 10.0, 10.0, 2.0, 3.0

# 로빈슨 도법 표 (위도 0~90도, 5도 간격). 가로 늘임(X)과 세로 위치(Y)
_RX = [1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730, 0.9600, 0.9427, 0.9216,
       0.8962, 0.8679, 0.8350, 0.7986, 0.7597, 0.7186, 0.6732, 0.6213, 0.5722,
       0.5322]
_RY = [0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100, 0.3720, 0.4340, 0.4958,
       0.5571, 0.6176, 0.6769, 0.7346, 0.7903, 0.8435, 0.8936, 0.9394, 0.9761,
       1.0000]


def _interp(tbl, lat):
    a = abs(lat) / 5.0
    i = min(int(a), len(tbl) - 2)
    return tbl[i] + (tbl[i + 1] - tbl[i]) * (a - i)


def proj(lon, lat):
    """로빈슨 투영. 단위 없는 좌표로 돌려주고 크기는 부르는 쪽에서 맞춘다."""
    x = _interp(_RX, lat) * math.radians(lon)
    y = _interp(_RY, lat) * (1 if lat >= 0 else -1) * 1.3523
    return x, y


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

    out = {'size': [W + OX * 2, 0.0], 'c': {}, 'center': {}, 'at': {}}
    bottom = 0.0
    for name, rs in rings.items():
        segs, kept = [], []
        for ring in rs:
            if len(ring) < 4:
                continue
            q = [xy(p) for p in ring]
            xs0 = [c[0] for c in q]
            ys0 = [c[1] for c in q]
            if max(xs0) - min(xs0) < MINSEG and max(ys0) - min(ys0) < MINSEG:
                continue            # 화면에서 점 하나로 뭉개지는 섬은 버린다
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
        out['c'][name] = ''.join(segs)
        xs = [c[0] for c in kept]
        ys = [c[1] for c in kept]
        out['center'][name] = [round((min(xs) + max(xs)) / 2, 1),
                               round((min(ys) + max(ys)) / 2, 1)]
    # 나라 한가운데로는 못 짚는 자리들. 그림에서 화살표를 걸 곳이라 미리 재 둔다
    for lon, lat in [(-93.9, 29.7), (-95.0, 40.0), (51.5, 25.3), (134.0, -25.0),
                     (5.0, 50.0), (128.0, 36.0), (-120.0, 45.0), (56.5, 26.6),
                     (-40.0, 25.0), (-25.0, 45.0), (-160.0, 25.0), (150.0, 20.0)]:
        out['at']['%g,%g' % (lon, lat)] = [round(v, 1) for v in xy(proj(lon, lat))]
    out['size'][1] = round(bottom + OY, 1)
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    n = sum(len(v) for v in out['c'].values())
    print('%d countries / path %d chars / canvas %.0f x %.0f -> %s'
          % (len(out['c']), n, out['size'][0], out['size'][1], OUT))
    for k in ('United States of America', 'Qatar', 'Australia', 'South Korea'):
        if k in out['center']:
            print('  %-26s %s' % (k, out['center'][k]))
    for k, v in out['at'].items():
        print('  at %-14s %s' % (k, v))


if __name__ == '__main__':
    main()
