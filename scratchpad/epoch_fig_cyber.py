# -*- coding: utf-8 -*-
"""Epoch AI 사이버 편 도해 둘 — 원문 그림을 한국어 인라인 SVG로 다시 그린다.

  cve_spike   Critical and high severity vulnerabilities from 21 notable organizations
  cyber_prog  Claude Mythos and GPT-5.6 Sol were large leaps in cyber capabilities

값은 눈으로 어림하지 않는다. 아래 _extract()가 원본 webp에서 격자선을 찾아 축을 세우고
색으로 도형을 찾아 데이터 좌표로 되돌린다. 그 결과를 이 파일 안에 리터럴로 박아 두어
그림을 그릴 때마다 이미지를 다시 읽지 않는다. 값을 다시 뽑으려면

  PYTHONIOENCODING=utf-8 python scratchpad/epoch_fig_cyber.py --extract

부품과 색·굵기·글자 크기는 epoch_fig.py 머리의 「이 장 도해의 한 벌」을 그대로 쓴다.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import epoch_fig as ef                                          # noqa: E402

esc, lab, svg = ef.esc, ef.lab, ef.svg

SRCDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'epoch_src')


# ══ ① 원본에서 읽어 둔 값 ═══════════════════════════════════════════════════
# cve.webp — 가로 격자 2022~2026(1년 224.0px), 세로 격자 0~900(100당 40.56px).
# 표식은 달마다 하나씩 x=95+18.667i(i=0 → 2022년 1월). 가파른 구간에서는 선이
# 열을 가로질러서 열 표본으로는 못 읽는다 — 표식 지름이 가장 넓어지는 행을 골랐다.
CVE_M0 = (2022, 1)                       # 첫 점이 가리키는 달
CVE_HIGH = [152, 85, 99, 158, 160, 137, 100, 131, 219, 145, 200, 263,
            229, 197, 229, 231, 196, 163, 165, 145, 207, 187, 157, 137,
            160, 223, 208, 255, 244, 182, 276, 242, 210, 271, 306, 244,
            288, 313, 227, 269, 233, 148, 258, 259, 371, 240, 224, 202,
            215, 261, 381, 598, 900]
CVE_CRIT = [20, 20, 1, 12, 7, 15, 9, 10, 16, 17, 21, 32,
            17, 18, 25, 25, 27, 12, 21, 12, 20, 12, 17, 14,
            18, 33, 25, 17, 30, 28, 23, 25, 20, 25, 21, 20,
            36, 16, 57, 22, 28, 23, 64, 30, 31, 27, 20, 32,
            22, 43, 55, 96, 141]
CVE_MARK = 51.19                         # 세로 점선 자리(달 단위) = 2026년 4월 초

# cyberprog.webp — 세로 격자 140~180(10당 141.17px), 가로 격자 2025/04~2026/08
# (4달당 173.38px). 점은 검은 테두리 원이라, 반지름 7.6 고리에 테두리가 몇 도나
# 걸리는지로 중심을 찾았다(가려진 점도 25/36도 이상 남는다).
CP_X0 = (2025, 4)                        # 가로 0 = 2025년 4월. 단위는 달
CP_GRAY = [(0.47, 146.25), (1.65, 144.55), (1.67, 143.98), (4.16, 146.17),
           (4.21, 149.50), (5.96, 149.72), (7.58, 154.32), (8.59, 154.82),
           (10.19, 157.79), (10.58, 154.68), (10.67, 154.04), (11.09, 157.72),
           (12.15, 163.96), (12.49, 155.74), (12.72, 164.03), (13.85, 162.26)]
CP_NAMED = [('Opus 4.5', 'pink', 7.81, 154.04),
            ('Opus 4.6', 'pink', 10.19, 159.35),
            ('Mythos Preview', 'pink', 12.17, 169.55),
            ('Mythos 5', 'pink', 14.25, 172.17),
            ('GPT-5.6 Sol', 'teal', 15.24, 171.18)]
CP_GLM = (14.66, 153.90, 159.35)         # 점이 아니라 세로 구간이다
CP_TREND = ((0.01, 143.62), (16.92, 163.98))


# ══ ② 값을 뽑는 자리 — 눈으로 어림하지 않기 위한 것 ══════════════════════════
def _extract():
    """원본 webp에서 위 리터럴을 다시 뽑는다. 그림 그릴 때는 부르지 않는다."""
    import math
    from PIL import Image

    # ── cve.webp ────────────────────────────────────────────────────────
    im = Image.open(os.path.join(SRCDIR, 'cve.webp')).convert('RGB')
    px = im.load()

    def gridlines(axis, rng, other, need):
        hit = []
        for v in rng:
            n = sum(1 for u in other
                    if (lambda c: c != (255, 255, 255) and abs(c[0] - c[2]) < 12
                        and 195 < c[0] < 250)(px[u, v] if axis == 'y' else px[v, u]))
            if n > need:
                hit.append(v)
        g, cur = [], [hit[0]]
        for v in hit[1:]:
            (cur if v - cur[-1] <= 3 else g.append(sum(cur) / len(cur)) or cur.clear() or cur
             ).append(v)
        g.append(sum(cur) / len(cur))
        return g

    gy = gridlines('y', range(90, 495), range(120, 1080, 4), 150)   # 900 … 0
    gx = gridlines('x', range(60, 1160), range(120, 490, 4), 60)    # 2023 … 2026
    y900, y0 = gy[0], gy[-1]
    per100 = (y0 - y900) / 9.0
    year = (gx[-1] - gx[0]) / 3.0                                   # 1년 픽셀
    x_2022 = gx[0] - year
    print('cve  격자 y %.1f(900) … %.1f(0)  100당 %.2fpx' % (y900, y0, per100))
    print('     격자 x 2022=%.1f  1년 %.2fpx  1달 %.3fpx' % (x_2022, year, year / 12))

    ORA, MAG = (240, 105, 62), (222, 62, 142)

    def near(c, t, tol=46):
        return all(abs(a - b) <= tol for a, b in zip(c, t))

    def marker(xc, t):
        """표식은 채워진 원이라 그 중심 행에서 가로로 가장 넓다. 선만 지나는 행은 좁다."""
        best = [(sum(1 for x in range(xc - 5, xc + 6) if near(px[x, y], t)), y)
                for y in range(108, 498)]
        mx = max(b[0] for b in best)
        ys = [y for n, y in best if n == mx]
        return (y0 - sum(ys) / len(ys)) / per100 * 100

    step = year / 12.0
    x_first = x_2022 + step * 0.55
    high = [round(marker(round(x_first + step * i), ORA)) for i in range(53)]
    crit = [round(marker(round(x_first + step * i), MAG)) for i in range(53)]
    print('     HIGH %s' % high)
    print('     CRIT %s' % crit)
    mark = None
    for x in range(1000, 1080):
        n = sum(1 for y in range(120, 490)
                if abs(px[x, y][0] - px[x, y][2]) < 14 and 120 < px[x, y][0] < 200)
        if n > 150:
            mark = (x - x_2022) / step
    print('     세로 점선 = %.2f달째(2022-01 기준)' % mark)

    # ── cyberprog.webp ──────────────────────────────────────────────────
    im = Image.open(os.path.join(SRCDIR, 'cyberprog.webp')).convert('RGB')
    px = im.load()
    ry = [v for v in range(330, 960)
          if sum(1 for x in range(180, 930, 3)
                 if abs(px[x, v][0] - px[x, v][2]) < 10 and 215 < px[x, v][0] < 238) > 150]
    rx = [v for v in range(80, 960)
          if sum(1 for y in range(360, 930, 3)
                 if abs(px[v, y][0] - px[v, y][2]) < 10 and 215 < px[v, y][0] < 238) > 110]

    def group(vs):
        g, cur = [], [vs[0]]
        for v in vs[1:]:
            if v - cur[-1] <= 3:
                cur.append(v)
            else:
                g.append(sum(cur) / len(cur))
                cur = [v]
        g.append(sum(cur) / len(cur))
        return g
    gy, gx = group(ry), group(rx)                 # 180…150 / 2025-04…2026-08
    per10 = (gy[-1] - gy[0]) / 3.0
    per4m = (gx[-1] - gx[0]) / 4.0
    print('prog 격자 y %s  10당 %.2fpx' % ([round(v, 1) for v in gy], per10))
    print('     격자 x %s  4달당 %.2fpx' % ([round(v, 1) for v in gx], per4m))

    def fy(v):
        return 180 - (v - gy[0]) / per10 * 10

    def fx(v):
        return (v - gx[0]) / (per4m / 4.0)

    def dark(x, y):
        c = px[x, y]
        return c[0] < 95 and c[1] < 95 and c[2] < 95

    def cover(cx, cy, R=7.6):
        """반지름 R 고리에 검은 테두리가 몇 도나 걸리나. 가려진 점도 살아남는다."""
        n = 0
        for a in range(36):
            t = math.radians(a * 10)
            n += any(dark(round(cx + r * math.cos(t)), round(cy + r * math.sin(t)))
                     for r in (R - 1.2, R - 0.4, R + 0.4, R + 1.2))
        return n

    def kind(cx, cy):
        """속이 채움색으로 차 있어야 표식이다. 검은 글자는 여기서 걸러진다 —
        글자 획 언저리에도 회색 안티에일리어싱이 있어서 몇 점만 보면 속는다."""
        vote, tot, ink = {}, 0, 0
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if dx * dx + dy * dy > 16:
                    continue
                tot += 1
                r, g, b = px[cx + dx, cy + dy]
                if r < 95 and g < 95 and b < 95:
                    ink += 1
                elif abs(r - g) < 12 and abs(g - b) < 12 and 195 < r < 222:
                    vote['gray'] = vote.get('gray', 0) + 1
                elif r > 190 and g < 110 and 100 < b < 190:
                    vote['pink'] = vote.get('pink', 0) + 1
                elif r < 90 and 130 < g < 205 and 130 < b < 205:
                    vote['teal'] = vote.get('teal', 0) + 1
        if not vote or ink > tot * 0.30:      # 속이 검으면 글자 획이지 표식이 아니다
            return None
        k = max(vote, key=vote.get)
        return k if vote[k] >= tot * 0.45 else None

    res = sorted(((cover(x, y), x, y) for y in range(388, 935) for x in range(158, 938)
                  if cover(x, y) >= 25), reverse=True)
    dots = []
    for c, x, y in res:
        if any(abs(a - x) < 7 and abs(b - y) < 7 for _, a, b in dots):
            continue
        k = kind(x, y)
        if k:
            dots.append((k, x, y))
    for k in ('gray', 'pink', 'teal'):
        print('     %-5s %s' % (k, sorted((round(fx(x), 2), round(fy(y), 2))
                                             for kk, x, y in dots if kk == k)))
    bx = [x for x in range(800, 850)
          if any(px[x, y][2] > 190 and px[x, y][0] < 90 for y in range(600, 760))]
    by = [y for y in range(380, 760)
          if px[bx[len(bx) // 2], y][2] > 190 and px[bx[len(bx) // 2], y][0] < 90]
    print('     GLM 구간 x %.2f  %.2f … %.2f'
             % (fx(sum(bx) / len(bx)), fy(max(by)), fy(min(by))))
    # 추세선 — 중간 회색 점선. 점 테두리와 글자에도 같은 밝기가 섞여 있어서,
    # 기울기와 절편을 표로 쌓아 가장 많은 점이 얹히는 직선 하나를 고른다.
    cand = [(x, y) for x in range(150, 960) for y in range(380, 940)
            if 60 < px[x, y][0] < 130 and abs(px[x, y][0] - px[x, y][2]) < 14
            and abs(px[x, y][0] - px[x, y][1]) < 14]
    acc = {}
    for x, y in cand:
        for si in range(-120, -39):
            s = si / 250.0
            acc.setdefault((si, round(y - s * (x - 500))), []).append((x, y))
    (si, _b), on = max(acc.items(), key=lambda kv: len(kv[1]))
    slope = si / 250.0
    x1 = sum(p[0] for p in on) / float(len(on))
    y1 = sum(p[1] for p in on) / float(len(on))
    xa, xb = min(p[0] for p in on), max(p[0] for p in on)
    print('     추세선 점 %d개 기울기 %.4f  (%.2f, %.2f) → (%.2f, %.2f)'
             % (len(on), slope, fx(xa), fy(y1 + slope * (xa - x1)),
                fx(xb), fy(y1 + slope * (xb - x1))))


# ══ ③ 그린다 ═══════════════════════════════════════════════════════════════
AMBER = 'var(--epoch-coral,#FD6438)'
BAD = 'var(--epoch-pink,#E03C8F)'
# 회사를 가르는 색으로는 --fig-bad 를 쓰지 않는다 — 이 저장소에서 빨강은 「나쁨」이라
# 앤트로픽만 나쁜 것처럼 읽힌다. 원문의 자홍에 가장 가까운 보라를 쓴다.
VIOLET = 'var(--epoch-pink,#E03C8F)'
GOOD = 'var(--fig-good,#2f8f6b)'
BLUE = 'var(--fig-blue,#2f6fd0)'
GRAY = 'rgba(127,127,127,.30)'


def _key(x, y, color, text):
    """색 범례 한 칸 — 네모와 글자. 흐름도 범례가 아니라 계열 색이다."""
    return ('<rect x="%d" y="%d" width="14" height="11" rx="2" fill="%s" '
            'stroke="var(--ink-3)" stroke-width="1"/>' % (x, y - 9, color)
            + lab(x + 20, y, text, fs=13))


def _axline(x1, y1, x2, y2):
    return ('<path d="M%.1f %.1f L%.1f %.1f" stroke="var(--ink-3)" stroke-width="1" '
            'fill="none"/>' % (x1, y1, x2, y2))


def fig_cve_spike():
    """21개 기업이 공개한 CVE 월별 집계. 마지막 석 달에 고위험이 세로로 선다."""
    X0, STEP, Y0, Y1, VMAX = 62, 9.5, 62, 300, 950.0
    X1 = X0 + STEP * 52

    def px(i):
        return X0 + STEP * i

    def py(v):
        return Y1 - (Y1 - Y0) * v / VMAX

    o = [_key(16, 22, AMBER, '고위험(High)'), _key(146, 22, BAD, '치명(Critical)')]
    o.append('<text x="16" y="44" class="t-sm" style="font-weight:800">월별 CVE 건수</text>')
    o.append(_axline(X0, 54, X0, Y1))
    o.append(_axline(X0, Y1, X1 + 14, Y1))
    for v in (0, 300, 600, 900):
        o.append(_axline(X0 - 5, py(v), X0, py(v)))
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%d</text>'
                 % (X0 - 9, py(v) + 4, v))
    for k in range(5):
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%d</text>'
                 % (px(12 * k), Y1 + 22, 2022 + k))
    # 두 계열 — 표식이 53개라 선 위 표식은 조밀한 쪽 값(3.4)을 쓴다
    for vals, col in ((CVE_CRIT, BAD), (CVE_HIGH, AMBER)):
        pts = ' '.join('%.1f,%.1f' % (px(i), py(v)) for i, v in enumerate(vals))
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3" '
                 'stroke-linejoin="round"/>' % (pts, col))
        for i, v in enumerate(vals):
            o.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (px(i), py(v), col))
    # 미토스 프리뷰가 공개된 자리 — 기준선이라 1.2 점선이다
    mx = px(CVE_MARK)
    o.append('<path d="M%.1f %d L%.1f %d" stroke="var(--ink-3)" stroke-width="1.8" '
             'stroke-dasharray="6 4" fill="none"/>' % (mx, 84, mx, Y1))
    o.append('<text x="%.1f" y="100" class="t-sm" text-anchor="end" '
             'style="font-weight:800">미토스 프리뷰 공개</text>' % (mx - 6))
    o.append('<text x="%.1f" y="118" class="t-sm t-axis" text-anchor="end">'
             '(2026년 4월)</text>' % (mx - 6))
    o.append('<text x="%.1f" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             '%d건</text>' % (X1 + 8, py(CVE_HIGH[-1]) + 4, AMBER, CVE_HIGH[-1]))
    o.append('<text x="%.1f" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             '%d건</text>' % (X1 + 8, py(CVE_CRIT[-1]) + 4, BAD, CVE_CRIT[-1]))
    ny = Y1 + 40
    for s in ('2022년 1월부터 2026년 5월까지, 21개 기업이 공개한 치명·고위험 CVE를 달마다 셌다',
              '고위험은 2026년 3월 381건에서 4월 598건, 5월 900건으로 두 달 만에 2.4배가 됐다',
              '치명도 같은 두 달에 55건 → 96건 → 141건으로 늘었다',
              '공개 절차와 등급 기준, 공개 주기가 기업마다 크게 달라 회사끼리 그대로 견주지는 못한다',
              '대상은 AWS·아파치·애플·시스코·구글·리눅스·마이크로소프트·모질라·엔비디아 등 21곳이다'):
        o.append(lab(16, ny, s, fs=13))
        ny += 16
    return svg(ny - 4, ''.join(o))


def fig_cyber_prog():
    """공개일 대 Cyber ECI. 미토스 프리뷰 이후 세 모델이 앞선 추세선 위로 벗어난다."""
    X0, X1, Y0, Y1 = 70, 560, 58, 330
    MMAX, VLO, VHI = 17.5, 139.0, 181.0

    def px(m):
        return X0 + (X1 - X0) * m / MMAX

    def py(v):
        return Y1 - (Y1 - Y0) * (v - VLO) / (VHI - VLO)

    o = [_key(16, 22, GOOD, 'OpenAI'), _key(102, 22, VIOLET, 'Anthropic'),
         _key(215, 22, BLUE, 'Zhipu AI'), _key(319, 22, GRAY, '그 밖의 모델')]
    o.append('<text x="16" y="44" class="t-sm" style="font-weight:800">'
             'Cyber ECI — 사이버 공격 능력 점수</text>')
    o.append(_axline(X0, 52, X0, Y1))
    o.append(_axline(X0, Y1, X1 + 14, Y1))
    for v in (140, 150, 160, 170, 180):
        o.append(_axline(X0 - 5, py(v), X0, py(v)))
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%d</text>'
                 % (X0 - 9, py(v) + 4, v))
    for m, t in ((0, '2025/04'), (4, '2025/08'), (8, '2025/12'), (12, '2026/04'),
                 (16, '2026/08')):
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (px(m), Y1 + 22, t))
    o.append('<text x="%.1f" y="%d" class="t-sm" text-anchor="middle" '
             'style="font-weight:800">공개일</text>' % ((X0 + X1) / 2, Y1 + 42))
    # 미토스 프리뷰 이전 모델로 그은 추세선 — 추세선이라 1.2 점선이다
    (ta, tav), (tb, tbv) = CP_TREND
    o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="var(--ink-3)" stroke-width="1.8" '
             'stroke-dasharray="6 4" fill="none"/>'
             % (px(ta), py(tav), px(tb), py(tbv)))
    o.append('<path d="M210 292 L210 264" stroke="var(--ink-3)" stroke-width="1" '
             'fill="none"/>')
    o.append(lab(180, 308, '미토스 프리뷰 이전 추세', fs=13))
    for m, v in CP_GRAY:
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="var(--ink-3)" '
                 'stroke-width="1"/>' % (px(m), py(v), GRAY))
    # GLM-5.2는 점이 아니라 구간이다 — 원문도 세로 막대로 그렸다
    gm, glo, ghi = CP_GLM
    o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="3" fill="none"/>'
             % (px(gm), py(glo), px(gm), py(ghi), BLUE))
    for v in (glo, ghi):
        o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="3" '
                 'fill="none"/>' % (px(gm) - 6, py(v), px(gm) + 6, py(v), BLUE))
    o.append('<text x="%.1f" y="250" class="t-sm" text-anchor="middle" '
             'style="font-weight:850;fill:%s">GLM-5.2</text>' % (px(gm), BLUE))
    col = {'pink': VIOLET, 'teal': GOOD}
    for name, k, m, v in CP_NAMED:
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="var(--ink-3)" '
                 'stroke-width="1"/>' % (px(m), py(v), col[k]))
    place = {'Opus 4.5': (272, 222, 'end'), 'Opus 4.6': (347, 190, 'end'),
             'Mythos Preview': (403, 137, 'end'), 'Mythos 5': (461, 104, 'end'),
             'GPT-5.6 Sol': (504, 134, 'start')}
    for name, k, m, v in CP_NAMED:
        lx, ly, an = place[name]
        shown = name + '(4월판)' if name == 'Mythos Preview' else name
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="%s" '
                 'style="font-weight:850;fill:%s">%s</text>' % (lx, ly, an, col[k], esc(shown)))
    ny = Y1 + 56
    for s in ('가로는 모델 공개일, 세로는 Cyber ECI다. 회색은 원문이 이름을 달지 않은 그 밖의 모델이다',
              '점선은 Mythos Preview 이전 모델만으로 그은 추세선이다',
              'Mythos Preview 169.6 · Mythos 5 172.2 · GPT-5.6 Sol 171.2 —',
              '셋 다 같은 시점 추세선 값보다 9점 넘게 높다',
              'GLM-5.2는 점이 아니라 구간이다. Irregular과 영국 AISI의 발언을 근거로',
              'Opus 4.5(154.0)와 Opus 4.6(159.4) 사이로 원문이 어림한 값이다'):
        o.append(lab(16, ny, s, fs=13))
        ny += 16
    return svg(ny - 4, ''.join(o))


FIGS = {'cve_spike': fig_cve_spike, 'cyber_prog': fig_cyber_prog}


if __name__ == '__main__':
    if '--extract' in sys.argv:
        _extract()
    else:
        import check_fig
        for k, fn in FIGS.items():
            print(k, check_fig.hits(fn()) or 'OK')
