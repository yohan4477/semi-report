# -*- coding: utf-8 -*-
"""서울 25구 윤곽을 SVG path로 굽는다 — insights/watch/_seoul_gu.json.

포트폴리오 워치가 구별 지정 현황(토지거래허가·조정대상·투기과열)을 지도로 보여주려면
구 하나하나가 판 위에서 어디 있는지가 있어야 한다. 좌표를 받아 오는 곳과 정책값을
받아 오는 곳(fetch_zones.py)을 나눈 건 후자가 사람 손으로 확인해야 하는 값이라서다 —
지도는 안 바뀌지만 지정 현황은 달마다 바뀐다.

원본: southkorea/seoul-maps (JUSO 2015 시군구 경계, Apache-2.0). 그 저장소 자체가
KOSTAT·JUSO(둘 다 정부 공개 자료)를 가공한 것이고 가공자가 Apache-2.0 으로 재배포한다.

투영: 등장방형(위도 cos 보정) — x = lon * cos(lat0), y = lat, lat0 = 서울 중심위도(37.55).
      서울은 남북으로 짧아(위도 폭 0.27도) 정식 도법 없이도 왜곡이 안 보인다.
단순화: Douglas-Peucker, 허용 오차 0.8px(판 좌표계, viewBox 640x560, 여백 12).
라벨점: 격자 탐색으로 「경계까지 거리가 가장 먼 안쪽 점」(pole of inaccessibility 근사).
      무게중심(centroid)은 오목한 구(종로구 등)에서 구 밖으로 나갈 수 있어 안 쓴다.

    python scripts/fetch_seoul_gu.py
"""
import io
import json
import math
import os
import urllib.request

SRC = ('https://raw.githubusercontent.com/southkorea/seoul-maps/master/'
       'juso/2015/json/seoul_municipalities_geo_simple.json')
LICENSE = ('Apache-2.0 (southkorea/seoul-maps 가공물). 원 데이터는 KOSTAT'
           '(2013 센서스용 행정구역경계)·서울시 JUSO(2015 행정구역 시군구 정보) 공개자료')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'insights', 'watch', '_seoul_gu.json')

VB_W, VB_H, MARGIN = 640.0, 560.0, 12.0
LAT0 = 37.55            # 서울 중심위도 — x축 cos 보정 기준
DP_EPS = 0.8            # Douglas-Peucker 허용 오차, 판 좌표계 px 단위


def proj_raw(lon, lat):
    """경위도를 등장방형 평면좌표로. 단위는 도(度) 그대로, 축척은 부르는 쪽에서 맞춘다."""
    return lon * math.cos(math.radians(LAT0)), lat


def douglas_peucker(pts, eps):
    """점 목록을 재귀로 줄인다. pts는 (x, y) 튜플 리스트, 첫/끝점은 남는다."""
    if len(pts) < 3:
        return pts
    x1, y1 = pts[0]
    x2, y2 = pts[-1]
    dx, dy = x2 - x1, y2 - y1
    seglen = math.hypot(dx, dy)
    dmax, idx = -1.0, -1
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        if seglen == 0:
            d = math.hypot(px - x1, py - y1)
        else:
            d = abs(dy * px - dx * py + x2 * y1 - y2 * x1) / seglen
        if d > dmax:
            dmax, idx = d, i
    if dmax > eps:
        left = douglas_peucker(pts[:idx + 1], eps)
        right = douglas_peucker(pts[idx:], eps)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def point_in_ring(x, y, ring):
    """레이캐스팅. ring은 (x, y) 리스트(마지막점=첫점이어도 무방)."""
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi):
            inside = not inside
        j = i
    return inside


def dist_to_ring(x, y, ring):
    """점에서 ring(선분들)까지 최단거리."""
    best = float('inf')
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        seglen2 = dx * dx + dy * dy
        if seglen2 == 0:
            d = math.hypot(x - x1, y - y1)
        else:
            t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / seglen2))
            d = math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))
        best = min(best, d)
    return best


def pole_of_inaccessibility(rings, bbox):
    """경계까지 거리가 가장 먼 안쪽 점을 격자 탐색으로 근사한다 (polylabel 간이판).

    거친 격자에서 최선점을 찾고, 그 둘레로 격자를 좁혀 가며 5단계 다시 찾는다.
    """
    minx, miny, maxx, maxy = bbox
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    cell = max(maxx - minx, maxy - miny)
    best_x, best_y, best_d = cx, cy, -1.0

    def score(x, y):
        if not point_in_ring(x, y, rings[0]):
            return -1.0
        for hole in rings[1:]:
            if point_in_ring(x, y, hole):
                return -1.0
        return min(dist_to_ring(x, y, r) for r in rings)

    d0 = score(cx, cy)
    if d0 > best_d:
        best_x, best_y, best_d = cx, cy, d0

    grid = 12
    for _ in range(6):
        half = cell / 2.0
        found = False
        for gy in range(grid + 1):
            y = best_y - half + (2 * half) * gy / grid
            for gx in range(grid + 1):
                x = best_x - half + (2 * half) * gx / grid
                d = score(x, y)
                if d > best_d:
                    best_x, best_y, best_d, found = x, y, d, True
        cell = half
        if not found and cell < 0.01:
            break
    return best_x, best_y


def build_path(polys_xy, dp_eps):
    """폴리곤 목록(각 폴리곤=ring 목록, 각 ring=(x,y) 리스트)을 SVG path d로 굽는다."""
    segs = []
    kept_rings = []
    for rings in polys_xy:
        for ring in rings:
            simple = douglas_peucker(ring, dp_eps)
            if len(simple) < 4:
                simple = ring
            if simple[0] != simple[-1]:
                simple = simple + [simple[0]]
            pts = ['%.1f %.1f' % (x, y) for x, y in simple]
            # 인접 중복점 제거
            dedup = [pts[0]]
            for p in pts[1:]:
                if p != dedup[-1]:
                    dedup.append(p)
            if len(dedup) < 4:
                continue
            segs.append('M' + dedup[0] + 'L' + 'L'.join(dedup[1:]) + 'Z')
            kept_rings.append(simple)
    return ''.join(segs), kept_rings


def main():
    req = urllib.request.Request(SRC, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as f:
        data = json.loads(f.read().decode('utf-8'))

    # 1차: 모든 좌표를 raw 투영(도 단위)해 전체 bbox를 구한다
    raw_by_gu = {}
    all_pts = []
    for feat in data['features']:
        name = feat['properties']['SIG_KOR_NM']
        geom = feat['geometry']
        polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
        proj_polys = []
        for poly in polys:
            proj_rings = []
            for ring in poly:
                pr = [proj_raw(lon, lat) for lon, lat in ring]
                proj_rings.append(pr)
                all_pts.extend(pr)
            proj_polys.append(proj_rings)
        raw_by_gu[name] = proj_polys

    minx = min(p[0] for p in all_pts)
    maxx = max(p[0] for p in all_pts)
    miny = min(p[1] for p in all_pts)
    maxy = max(p[1] for p in all_pts)

    avail_w = VB_W - 2 * MARGIN
    avail_h = VB_H - 2 * MARGIN
    scale = min(avail_w / (maxx - minx), avail_h / (maxy - miny))
    used_w = (maxx - minx) * scale
    used_h = (maxy - miny) * scale
    pad_x = MARGIN + (avail_w - used_w) / 2.0
    pad_y = MARGIN + (avail_h - used_h) / 2.0

    def to_board(pt):
        x, y = pt
        sx = (x - minx) * scale + pad_x
        sy = (maxy - y) * scale + pad_y   # 북쪽이 위로 오게 y 반전
        return (sx, sy)

    out_gu = {}
    for name, proj_polys in raw_by_gu.items():
        board_polys = [[[to_board(pt) for pt in ring] for ring in rings]
                        for rings in proj_polys]
        d, kept_rings = build_path(board_polys, DP_EPS)
        bxs = [p[0] for r in kept_rings for p in r]
        bys = [p[1] for r in kept_rings for p in r]
        bbox = (min(bxs), min(bys), max(bxs), max(bys))
        # 라벨점은 (구멍 없는 구라 가정하고) 가장 큰 폴리곤 하나로 근사한다
        biggest = max(kept_rings, key=lambda r: (max(p[0] for p in r) - min(p[0] for p in r)) *
                                                 (max(p[1] for p in r) - min(p[1] for p in r)))
        cx, cy = pole_of_inaccessibility([biggest], bbox)
        out_gu[name] = {'d': d, 'cx': round(cx, 1), 'cy': round(cy, 1)}

    out = {
        'src': SRC,
        'license': LICENSE,
        'fetched': '2026-09-03',
        'viewBox': [0, 0, int(VB_W), int(VB_H)],
        'gu': out_gu,
    }
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    size_kb = os.path.getsize(OUT) / 1024.0
    print('gu=%d  size=%.1fKB -> %s' % (len(out_gu), size_kb, OUT))
    for k in ('강남구', '종로구', '중구'):
        if k in out_gu:
            print('  %-6s d_len=%d cx=%.1f cy=%.1f' %
                  (k, len(out_gu[k]['d']), out_gu[k]['cx'], out_gu[k]['cy']))


if __name__ == '__main__':
    main()
