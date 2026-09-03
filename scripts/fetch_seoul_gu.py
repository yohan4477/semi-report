# -*- coding: utf-8 -*-
"""서울 25구 + 성남 3구 윤곽을 SVG path로 굽는다 — insights/watch/_seoul_gu.json.

포트폴리오 워치가 구별 지정 현황(토지거래허가·조정대상·투기과열)을 지도로 보여주려면
구 하나하나가 판 위에서 어디 있는지가 있어야 한다. 좌표를 받아 오는 곳과 정책값을
받아 오는 곳(fetch_zones.py)을 나눈 건 후자가 사람 손으로 확인해야 하는 값이라서다 —
지도는 안 바뀌지만 지정 현황은 달마다 바뀐다.

2026-09 — 성남 3구(분당·중원·수정)를 같은 판에 더했다. 서울 25구는 그대로
southkorea/seoul-maps(JUSO 2015)에서 오고, 성남 3구는 그 저장소에 없어(서울시계 밖)
southkorea/southkorea-maps 의 전국 시군구 파일(KOSTAT 2013)에서 code 접두어
31021(수정)·31022(중원)·31023(분당)으로 골라낸다. 두 저장소 다 좌표계가 WGS84
경위도라(강남구로 대조: 두 파일 bbox 가 소수점 둘째 자리까지 같다) 사영 하나로
같이 굽는다.

원본 : southkorea/seoul-maps (JUSO 2015 시군구 경계, Apache-2.0) — 서울 25구.
       southkorea/southkorea-maps (KOSTAT 2013 센서스용 행정구역경계, "Free to
       share or remix", README 확인) — 성남 3구.
       둘 다 KOSTAT·JUSO(정부 공개 자료)를 가공한 것이고 가공자가 각각의 조건으로
       재배포한다.

투영: 등장방형(위도 cos 보정) — x = lon * cos(lat0), y = lat, lat0 = 서울 중심위도(37.55).
      서울·성남을 합쳐도 위도 폭이 0.6도 안팎이라 정식 도법 없이도 왜곡이 안 보인다.
단순화: Douglas-Peucker, 허용 오차 0.8px(판 좌표계, viewBox 너비 640, 여백 12).
라벨점: 격자 탐색으로 「경계까지 거리가 가장 먼 안쪽 점」(pole of inaccessibility 근사).
      무게중심(centroid)은 오목한 구(종로구 등)에서 구 밖으로 나갈 수 있어 안 쓴다.
높이: 폭(640)과 여백(12)만 고정하고 세로는 데이터에서 낸다 — 성남이 서울 남동쪽에
      붙어 판이 아래로 길어지는데, 세로를 고정하면 스케일이 줄어 서울 구가 작아진다.

    python scripts/fetch_seoul_gu.py
"""
import io
import json
import math
import os
import urllib.request

SRC = ('https://raw.githubusercontent.com/southkorea/seoul-maps/master/'
       'juso/2015/json/seoul_municipalities_geo_simple.json')
SRC_SEONGNAM = ('https://raw.githubusercontent.com/southkorea/southkorea-maps/master/'
                'kostat/2013/json/skorea_municipalities_geo_simple.json')
LICENSE = ('Apache-2.0 (southkorea/seoul-maps 가공물, 서울 25구). 원 데이터는 KOSTAT'
           '(2013 센서스용 행정구역경계)·서울시 JUSO(2015 행정구역 시군구 정보) 공개자료. '
           '성남 3구는 southkorea/southkorea-maps(KOSTAT 2013, README: "Free to share '
           'or remix") 의 code 31021·31022·31023 피처')
# 전국 파일의 code → (판에 쓸 이름, si). 성남시분당구 같은 원 이름을 그대로 쓰면
# 서울 구(단독 두 글자+구)와 라벨 길이가 안 맞는다 — 다른 실거주 줄·_areas.json 이
# 쓰는 "분당구" 로 맞춘다.
SEONGNAM_CODES = {'31021': '수정구', '31022': '중원구', '31023': '분당구'}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'insights', 'watch', '_seoul_gu.json')

VB_W, MARGIN = 640.0, 12.0
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


def _fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as f:
        return json.loads(f.read().decode('utf-8'))


def main():
    data = _fetch_json(SRC)
    seongnam = _fetch_json(SRC_SEONGNAM)

    # 1차: 모든 좌표를 raw 투영(도 단위)해 전체 bbox를 구한다. sido_of 는 gu 마다
    # 서울/경기를 붙이는 데 쓴다 — 어댑터(realestate.py)가 codes_of prefix 를 고를 때
    # 이 값을 그대로 읽는다.
    raw_by_gu = {}
    sido_of = {}
    si_of = {}
    all_pts = []

    def _add(name, geom, sido, si=None):
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
        sido_of[name] = sido
        if si:
            si_of[name] = si

    for feat in data['features']:
        _add(feat['properties']['SIG_KOR_NM'], feat['geometry'], '서울')

    n_seongnam = 0
    for feat in seongnam['features']:
        code = feat['properties'].get('code')
        if code in SEONGNAM_CODES:
            _add(SEONGNAM_CODES[code], feat['geometry'], '경기', '성남시')
            n_seongnam += 1
    if n_seongnam != len(SEONGNAM_CODES):
        raise SystemExit('성남 3구를 다 못 찾았다 — code %d개만 걸림 (기대 %d)'
                          % (n_seongnam, len(SEONGNAM_CODES)))

    minx = min(p[0] for p in all_pts)
    maxx = max(p[0] for p in all_pts)
    miny = min(p[1] for p in all_pts)
    maxy = max(p[1] for p in all_pts)

    # 폭(640)·여백(12)만 고정하고 세로는 데이터에서 낸다 — 성남이 남동쪽에 붙어
    # 판이 서울만 그릴 때보다 아래로 길어진다. 가로를 꽉 채우는 스케일 하나로
    # 재기 때문에 서울 25구의 픽셀 크기는 성남을 더하기 전과 같다.
    avail_w = VB_W - 2 * MARGIN
    scale = avail_w / (maxx - minx)
    used_h = (maxy - miny) * scale
    vb_h = used_h + 2 * MARGIN
    pad_x = MARGIN
    pad_y = MARGIN

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
        entry = {'d': d, 'cx': round(cx, 1), 'cy': round(cy, 1), 'sido': sido_of[name]}
        if name in si_of:
            entry['si'] = si_of[name]
        out_gu[name] = entry

    out = {
        'src': SRC + ' ; ' + SRC_SEONGNAM,
        'license': LICENSE,
        'fetched': '2026-09-04',
        'viewBox': [0, 0, int(VB_W), round(vb_h, 1)],
        'gu': out_gu,
    }
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False))
    size_kb = os.path.getsize(OUT) / 1024.0
    print('gu=%d (서울 %d · 성남 %d)  size=%.1fKB  viewBox=%s -> %s' %
          (len(out_gu), sum(1 for v in sido_of.values() if v == '서울'),
           sum(1 for v in sido_of.values() if v == '경기'), size_kb, out['viewBox'], OUT))
    for k in ('강남구', '종로구', '중구', '분당구', '수정구', '중원구'):
        if k in out_gu:
            print('  %-6s d_len=%d cx=%.1f cy=%.1f sido=%s'
                  % (k, len(out_gu[k]['d']), out_gu[k]['cx'], out_gu[k]['cy'], out_gu[k]['sido']))


if __name__ == '__main__':
    main()
