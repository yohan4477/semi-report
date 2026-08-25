# -*- coding: utf-8 -*-
"""「Toward an O*NET for AI R&D」(Epoch AI, 2026-06-17) 원문 도해 여섯 장을 한국어로 다시 그린다.

원문 그림은 라벨이 전부 영어라 그대로 실으면 카드 본문만 한국어가 된다. 그래서 값과
구조는 원문 그대로 두고 판만 새로 짠다. 규약은 `scratchpad/epoch_fig.py` 머리의
「이 장 도해의 한 벌」을 그대로 따르고, 부품도 거기서 가져다 쓴다.

값을 읽은 순서는 셋이다(insight-figure 규칙 2).
  1. 그림에 인쇄된 값 — 목록 그림 넷은 글자가 곧 값이라 그대로 옮겼다
  2. 인쇄돼 있지 않으면 눈금을 재서 읽는다 — 그래프 둘은 아래 `_extract_*()` 가
     원본 이미지에서 축 눈금과 곡선 자리를 찾아 데이터 좌표로 되돌린 값이다.
     뽑은 값은 `SA_SOLID`·`SA_DASH`·`SC_ELI`·`SC_NIKOLA` 에 리터럴로 박아 두었다
  3. 그래도 못 읽는 것만 형태를 바꾸고, 함수 docstring과 `CAPS` 캡션에 이유를 적는다

원본 이미지는 `scratchpad/epoch_src/{situational_awareness,superhuman_coder_extrapolation,
onet_task_samples,o-net,aird_onet_sample,expectation_reality}.webp` 에 있다.

  PYTHONIOENCODING=utf-8 python scratchpad/epoch_fig_onet.py    # 배치 검사 + 미리보기 HTML
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import epoch_fig as ef                                          # noqa: E402

SRCDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'epoch_src')


# ══ 눈금을 재서 읽은 값 ══════════════════════════════════════════════════
# 아래 두 리스트는 _extract_situational() · _extract_superhuman() 이 원본 이미지에서
# 뽑아낸 값을 그대로 박은 것이다. 눈으로 어림해 옮긴 자리는 하나도 없다.

# ── situational_awareness.png ────────────────────────────────────────────
# 세로 자는 로그다. 격자선 16줄이 10^8 … 10^-7 이고 한 칸이 39.13px,
# 가로 자는 연도 라벨 중심이 2018년 x=230 … 2028년 x=962 로 한 해가 73.2px 다.
# (연도, log10(실효 컴퓨트 / GPT-4)) — GPT-4 를 1 로 놓은 값이라 2023년이 0 이다.
SA_SOLID = [(2018.0, -7.05), (2018.5, -6.11), (2019.0, -5.25), (2019.5, -4.43),
            (2020.0, -3.69), (2020.5, -3.00), (2021.0, -2.34), (2021.5, -1.72),
            (2022.0, -1.11), (2022.5, -0.55), (2023.0, 0.01)]
# 2023년 뒤는 원문도 점선이다. 재 보니 로그 축 위에서 곧은 선이라(한 해 1.25칸)
# 측정값 여섯 곳(2023.25·2024.75·2025.0·2025.5·2026.0·2026.5·2027.0·2027.5·2027.85)이
# 오차 0.06칸 안에 들어온다. 끝점은 x=951 · y=234 로 10^6.10 이었다.
SA_DASH = [(2023.0, 0.01), (2024.0, 1.26), (2025.0, 2.48), (2026.0, 3.78),
           (2027.0, 5.02), (2028.0, 6.15)]
# 오른쪽 부채꼴(불확실 구간)의 2028년 폭. x=950 에서 아래 7.0e3 · 위 2.0e7 이었다.
SA_CONE = (4.0, 7.0)
# 오른쪽에 붙은 능력 눈금 — 라벨 글자의 세로 자리를 되돌려 읽었다.
SA_MARKS = [(0.0, 'GPT-4 · 똑똑한 고등학생'), (-3.0, 'GPT-3 · 초등학생'),
            (-5.0, 'GPT-2 · 미취학 아동')]

# ── superhuman_coder_extrapolation.png ───────────────────────────────────
# 세로 자는 확률밀도다. 0.20 라벨이 y=124.5, 0.00 이 y=639.5 로 0.05 가 128.75px,
# 가로 자는 격자선이 2034년 x=944.5 · 2035년 1034.5 · 2036년 1124.5 로 한 해가 90px 다.
# 니콜라 곡선의 마루는 범례 상자에 가려 있는데, 상자가 반투명이라 그 아래로 곡선이
# 옅은 회색으로 비친다. 그 자리를 따로 뽑아 이었다(2026.0~2027.2 구간).
SC_ELI = [(2025.0, 0.089), (2025.25, 0.1082), (2025.5, 0.126), (2025.75, 0.1412),
          (2026.0, 0.1536), (2026.25, 0.1625), (2026.5, 0.1672), (2026.75, 0.1672),
          (2027.0, 0.1633), (2027.25, 0.1561), (2027.5, 0.1462), (2027.75, 0.1353),
          (2028.0, 0.1237), (2028.5, 0.0996), (2029.0, 0.0798), (2029.5, 0.0637),
          (2030.0, 0.0526), (2030.5, 0.0455), (2031.0, 0.0402), (2032.0, 0.0336),
          (2033.0, 0.0285), (2034.0, 0.0239), (2035.0, 0.0200), (2036.0, 0.0177)]
SC_NIKOLA = [(2025.0, 0.093), (2025.25, 0.1202), (2025.5, 0.1513), (2025.75, 0.1783),
             (2026.0, 0.2000), (2026.25, 0.2148), (2026.5, 0.2188), (2026.75, 0.2161),
             (2027.0, 0.2068), (2027.25, 0.1918), (2027.5, 0.1759), (2027.75, 0.1592),
             (2028.0, 0.1431), (2028.5, 0.1122), (2029.0, 0.0876), (2029.5, 0.0676),
             (2030.0, 0.0544), (2030.5, 0.0452), (2031.0, 0.0388), (2032.0, 0.0301),
             (2033.0, 0.0235), (2034.0, 0.0192), (2035.0, 0.0161), (2036.0, 0.0126)]
# 분위수는 그림 오른쪽에 글자로 인쇄돼 있다 — 재지 않고 그대로 옮겼다.
SC_QUANT = [('엘라이 · AI 2027 저자', '2025년 10월', '2027년 8월', '2039년 8월', 2027.62),
            ('니콜라', '2025년 10월', '2027년 4월', '2033년 12월', 2027.29)]


# ══ 원본 이미지에서 값을 뽑는 코드 ═══════════════════════════════════════
# 위의 리터럴이 어디서 왔는지 되짚을 수 있게 남겨 둔다. 그림을 그릴 때는 돌지 않는다.
def _extract_situational():
    """situational_awareness.png 의 파란 곡선을 데이터 좌표로 되돌린다."""
    from PIL import Image
    px = Image.open(os.path.join(SRCDIR, 'situational_awareness.webp')).convert('RGB').load()
    x0, step = 230.0, 73.2              # 2018년 라벨 중심, 한 해 폭
    y0, ys = 159.5, 39.133              # 10^8 격자선, 한 칸(=한 자리) 높이

    def val(y):
        return 8 - (y - y0) / ys

    def blue(c):
        return c[2] - c[0] > 55 and c[2] > 90
    out, prev = [], None
    for i in range(41):
        yr = 2018 + i * 0.25
        x = int(round(x0 + (yr - 2018) * step))
        ys_ = [y for y in range(150, 790) if blue(px[x, y])]
        if not ys_:
            out.append((yr, None))
            continue
        runs, cur = [], [ys_[0]]
        for v in ys_[1:]:
            if v - cur[-1] > 3:
                runs.append(cur)
                cur = []
            cur.append(v)
        runs.append(cur)
        cs = [sum(r) / len(r) for r in runs]
        y = cs[0] if prev is None else min(cs, key=lambda v: abs(v - prev))
        prev = y
        out.append((yr, round(val(y), 3)))
    return out


def _extract_superhuman():
    """superhuman_coder_extrapolation.png 의 두 확률밀도 곡선을 되돌린다.

    범례 상자(x 146~591 · y 61~155)가 니콜라 곡선의 마루를 덮는다. 상자가 반투명이라
    그 안에서는 곡선이 옅은 초록빛 회색으로 남아, 그 자리를 따로 골라 이어 붙인다."""
    from PIL import Image
    px = Image.open(os.path.join(SRCDIR,
                                 'superhuman_coder_extrapolation.webp')).convert('RGB').load()
    x0, step = 134.5, 90.0              # 2025년, 한 해 폭
    y0, ys = 639.5, 2575.0              # 0.00 자리, 밀도 1.0 당 픽셀
    leg = (146, 591, 61, 155)

    def red(c):
        return c[0] > 110 and c[1] < 80 and c[2] < 95 and c[0] - c[1] > 50

    def grn(c):
        return 50 < c[1] < 130 and c[0] < 100 and c[2] < 100 and c[1] - c[0] > 15

    def faint(c):
        return c[1] - c[0] >= 3 and c[1] - c[2] >= 3 and 180 < sum(c) / 3 < 240

    def pick(x, f, prev, lo, hi, skip):
        cand = [y for y in range(lo, hi) if f(px[x, y])
                and not (skip and leg[0] <= x <= leg[1] and leg[2] <= y <= leg[3])]
        if not cand:
            return None
        runs, cur = [], [cand[0]]
        for v in cand[1:]:
            if v - cur[-1] > 3:
                runs.append(cur)
                cur = []
            cur.append(v)
        runs.append(cur)
        cs = [sum(r) / len(r) for r in runs]
        return cs[0] if prev is None else min(cs, key=lambda v: abs(v - prev))
    out = {}
    for key, f in (('eli', red), ('nikola', grn)):
        got, prev = [], None
        for i in range(45):
            yr = 2025 + i * 0.25
            x = int(round(x0 + (yr - 2025) * step))
            v = pick(x, f, prev, 50, 640, True)
            if v is None and key == 'nikola':
                v = pick(x, faint, prev, 62, 155, False)      # 범례 상자 아래로 비치는 곡선
            if v:
                prev = v
            got.append((yr, round((y0 - v) / ys, 4) if v else None))
        out[key] = got
    return out


# ══ 판 부품 ══════════════════════════════════════════════════════════════
def _wrapw(s):
    """check_fig 가 재는 글자 폭 — 한 글자 9px 로 어림한다."""
    return len(s) * 9.0


def _wrap(text, maxw):
    """띄어쓰기에서 끊어 여러 줄로 만든다. 폭은 검사기와 같은 자로 잰다."""
    out, cur = [], ''
    for word in text.split(' '):
        cand = word if not cur else cur + ' ' + word
        if _wrapw(cand) > maxw and cur:
            out.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


def _axis(pts):
    return ('<path d="%s" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
            % ('M%.1f %.1f' % pts[0] + ''.join(' L%.1f %.1f' % p for p in pts[1:])))


def _series(pts, color, dash=False, wd=2.4):
    d = ' '.join('%.1f,%.1f' % p for p in pts)
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"%s/>'
            % (d, color, wd, ' stroke-dasharray="6 4"' if dash else ''))


BLUE = 'var(--fig-blue,#2f6fd0)'
GOOD = 'var(--fig-good,#2f8f6b)'
BAD = 'var(--epoch-pink,#E03C8F)'
# 사람·계열을 가르는 색으로는 --fig-bad 를 쓰지 않는다 — 이 저장소에서 빨강은
# 「나쁨」이라 한쪽 예보자만 틀린 것처럼 읽힌다. 계열은 파랑으로 가른다.
BLUE = 'var(--fig-blue,#2f6fd0)'
SUP = {0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
       5: '⁵', 6: '⁶', 7: '⁷', '-': '⁻'}


def _pow10(e):
    s = ''.join(SUP['-'] if c == '-' else SUP[int(c)] for c in str(e))
    return '10' + s


# ══ ① 실효 컴퓨트를 5년 뒤까지 늘인 선 ═══════════════════════════════════
def fig_onet_sa():
    """「Situational Awareness」가 늘인 실효 컴퓨트 선.

    남의 그림(Leopold Aschenbrenner)이지만 축과 곡선은 그대로 읽어 옮겼다.
    격자선은 두지 않는다(규칙 3) — 대신 GPT-4=1 기준선만 점선으로 남겼다."""
    X0, X1, Y0, Y1 = 86, 452, 56, 252         # 가로 2018~2028, 세로 10^7~10^-7
    LO, HI = -7.0, 7.0

    def fx(yr):
        return X0 + (X1 - X0) * (yr - 2018) / 10.0

    def fy(lg):
        return Y1 - (Y1 - Y0) * (lg - LO) / (HI - LO)
    o = [ef.lab(16, 20, '「Situational Awareness」가 늘인 선 — 세로 자는 로그다', fs=13)]
    o.append('<text x="16" y="42" class="t-sm" style="font-weight:800">'
             '실효 컴퓨트 (2023년 GPT-4 = 1)</text>')
    o.append(_axis([(X0, Y0 - 6), (X0, Y1), (X1 + 10, Y1)]))
    for e in range(-6, 7, 2):
        y = fy(e)
        o.append(_axis([(X0 - 5, y), (X0, y)]))
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%s</text>'
                 % (X0 - 9, y + 4, _pow10(e)))
    for yr in (2018, 2020, 2022, 2024, 2026, 2028):
        x = fx(yr)
        o.append(_axis([(x, Y1), (x, Y1 + 5)]))
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%d</text>'
                 % (x, Y1 + 22, yr))
    # 불확실 구간 — 2023년 갈림목에서 부채꼴로 벌어진다
    o.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f Z" fill="rgba(127,127,127,.30)" '
             'stroke="none"/>' % (fx(2023), fy(0.01), fx(2028), fy(SA_CONE[1]),
                                  fx(2028), fy(SA_CONE[0])))
    o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="var(--ink-3)" stroke-width="1.8" '
             'stroke-dasharray="6 4" fill="none"/>' % (X0, fy(0), X1, fy(0)))
    o.append(_series([(fx(a), fy(b)) for a, b in SA_SOLID], BLUE))
    o.append(_series([(fx(a), fy(b)) for a, b in SA_DASH], BLUE, dash=True))
    o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (fx(2023), fy(0.01), BLUE))
    # 오른쪽 능력 눈금 — 원문이 곡선 옆에 붙여 둔 라벨을 그대로 옮긴다
    for lg, text in SA_MARKS:
        y = fy(lg)
        o.append(_axis([(X1 + 12, y), (X1 + 24, y)]))
        o.append('<text x="%d" y="%.1f" class="t-sm">%s</text>' % (X1 + 30, y + 4, ef.esc(text)))
    y6 = fy(6.15)
    o.append('<text x="%d" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             '자동화된</text>' % (X1 + 30, y6 - 5, BLUE))
    o.append('<text x="%d" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             'AI 연구자·엔지니어?</text>' % (X1 + 30, y6 + 13, BLUE))
    o.append(ef.lab(96, 118, '2023년까지는 실측이다', fs=13))
    o.append(ef.lab(96, 134, '거기서부터 5년을 늘였다', fs=13))
    o.append(ef.lab(16, Y1 + 40, '실선은 2023년까지 실측, 점선은 거기서 늘인 5년, 회색 면은 '
                                 '2028년 폭이', fs=13))
    o.append(ef.lab(16, Y1 + 56, '10⁴배에서 10⁷배 사이라는 뜻이다. 얼마의 컴퓨트가 '
                                 '세계 최고 연구자와', fs=13))
    o.append(ef.lab(16, Y1 + 72, '맞먹는지를 대는 근거는 이 그림 어디에도 없다', fs=13))
    return ef.svg(Y1 + 84, ''.join(o))


# ══ ② 초인 코더가 언제 오나 — 예보자 둘의 확률밀도 ═══════════════════════
def fig_onet_sc():
    """AI 2027 의 시간지평 외삽으로 뽑은 초인 코더 도착 시점 분포.

    분위수(10·50·90퍼센타일)는 원문 그림에 글자로 인쇄돼 있어 그대로 옮겼고,
    곡선은 눈금을 재서 읽었다. 마루가 범례에 가린 니콜라 곡선은 반투명 상자
    아래로 비치는 자리를 따로 뽑았다."""
    X0, X1, Y0, Y1 = 76, 404, 52, 240
    VMAX = 0.22

    def fx(yr):
        return X0 + (X1 - X0) * (yr - 2025) / 11.0

    def fy(v):
        return Y1 - (Y1 - Y0) * v / VMAX
    o = [ef.lab(16, 20, '초인 코더가 언제 오나 — AI 2027 이 시간지평을 늘여 뽑은 분포', fs=13)]
    o.append('<text x="16" y="42" class="t-sm" style="font-weight:800">확률밀도</text>')
    o.append(_axis([(X0, Y0 - 6), (X0, Y1), (X1 + 10, Y1)]))
    for v in (0.00, 0.05, 0.10, 0.15, 0.20):
        y = fy(v)
        o.append(_axis([(X0 - 5, y), (X0, y)]))
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%.2f</text>'
                 % (X0 - 9, y + 4, v))
    for yr in (2025, 2027, 2029, 2031, 2033, 2035):
        x = fx(yr)
        o.append(_axis([(x, Y1), (x, Y1 + 5)]))
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%d</text>'
                 % (x, Y1 + 22, yr))
    for pts, color in ((SC_NIKOLA, GOOD), (SC_ELI, BLUE)):
        o.append(_series([(fx(a), fy(b)) for a, b in pts], color))
    # 중앙값 — 날짜는 원문에 인쇄된 값이고, 세로 자리는 그 날짜에서 곡선을 읽은 것이다
    for (name, _p10, _p50, _p90, med), pts, color in ((SC_QUANT[0], SC_ELI, BLUE),
                                                      (SC_QUANT[1], SC_NIKOLA, GOOD)):
        v = _interp(pts, med)
        o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (fx(med), fy(v), color))
    o.append('<text x="%.1f" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             '니콜라</text>' % (fx(2026.5) + 6, fy(0.2188) - 10, GOOD))
    o.append('<text x="%.1f" y="%.1f" class="t-sm" style="font-weight:850;fill:%s">'
             '엘라이</text>' % (fx(2027.9), fy(0.070) + 34, BLUE))
    # 오른쪽 — 원문 그림에 인쇄돼 있던 분위수를 그대로 옮긴 표
    ty = 60
    for name, p10, p50, p90, _m in SC_QUANT:
        o.append('<text x="436" y="%d" class="t-lab">%s</text>' % (ty, ef.esc(name)))
        for i, (k, v) in enumerate((('10%', p10), ('50%', p50), ('90%', p90))):
            o.append('<text x="440" y="%d" class="t-sm t-axis">%s</text>' % (ty + 20 + i * 16, k))
            o.append('<text x="480" y="%d" class="t-sm">%s</text>' % (ty + 20 + i * 16, v))
        ty += 96
    o.append(ef.lab(436, 250, '점은 50% 자리다', fs=13))
    o.append(ef.lab(16, Y1 + 40, '두 예보자가 「AI가 초인 코더가 되는 해」에 매긴 확률이다. '
                                 '가운데값은 2027년으로', fs=13))
    o.append(ef.lab(16, Y1 + 56, '거의 같은데 90% 자리가 2033년과 2039년으로 여섯 해 벌어진다 — '
                                 '이 폭이', fs=13))
    o.append(ef.lab(16, Y1 + 72, '벤치마크가 연구의 복잡성을 못 담는 데서 온다는 것이 이 글의 '
                                 '문제 제기다', fs=13))
    return ef.svg(Y1 + 84, ''.join(o))


def _interp(pts, x):
    for (a1, b1), (a2, b2) in zip(pts, pts[1:]):
        if a1 <= x <= a2:
            return b1 + (b2 - b1) * (x - a1) / (a2 - a1)
    return pts[-1][1]


# ══ ③ O*NET 「컴퓨터·정보 연구 과학자」 과제 15개 ═════════════════════════
# 원문 그림은 O*NET 화면 갈무리다. 목록은 목록 그대로 옮긴다 — 문장을 한국어로만 바꿨다.
TASKS15 = [
    '컴퓨터 하드웨어와 소프트웨어를 수반하는 해법을 만들기 위해 문제를 분석한다',
    '이론적 전문성과 혁신을 적용해 새 기술을 만들거나 적용한다 — 이를테면 컴퓨터를 새 '
    '용도에 쓰도록 원리를 고쳐 쓴다',
    '업무 우선순위와 목표에 맞게 과제를 배정하거나 일정을 잡는다',
    '관리자·벤더 등과 만나 협조를 구하고 문제를 푼다',
    '컴퓨터와 그 위에서 도는 소프트웨어를 설계한다',
    '사업·과학·공학 등 기술 문제를 논리적으로 분석하고, 컴퓨터가 풀 수 있도록 수학 '
    '모형으로 세운다',
    '프로젝트 계획과 제안을 평가해 실현 가능성을 따진다',
    '가상현실·인간-컴퓨터 상호작용·로보틱스 같은 다학제 프로젝트에 참여한다',
    '사용자·경영진·벤더·기술자와 상의해 컴퓨팅 수요와 시스템 요구사항을 정한다',
    '조직의 목표·정책·절차를 만들고 해석한다',
    '성과 기준을 만들고, 정해 둔 기준에 비추어 일을 평가한다',
    '네트워크 하드웨어와 소프트웨어를 유지하고, 네트워크 보안 조치를 지휘하며, '
    '사용자가 쓸 수 있게 네트워크를 감시한다',
    '부서의 일상 운영을 지휘하고 다른 부서와 프로젝트 활동을 조율한다',
    '인력 배치 결정에 참여하고 부하 직원 교육을 지휘한다',
    '운영 예산을 승인·편성·감시·조정한다',
]


def fig_onet_tasks15():
    """O*NET 이 이 직업에 적어 둔 과제 15개를 그대로 옮긴 목록.

    원문 그림이 목록이라 목록으로 둔다. 첫 줄만 붉게 두는 것은 원문의 주장 때문이다 —
    「AI 엔지니어가 하는 거의 모든 일이 여기 들어간다」."""
    o = [ef.lab(16, 20, 'O*NET 「컴퓨터·정보 연구 과학자」에 적혀 있는 과제 15개', fs=13)]
    y = 46
    for i, t in enumerate(TASKS15, 1):
        key = (i == 1)
        o.append('<circle cx="20" cy="%d" r="3" fill="%s"/>' % (y - 4, BAD if key else GOOD))
        o.append('<text x="30" y="%d" class="t-sm t-axis">%d</text>' % (y, i))
        cls = 't-bad' if key else 't-sm'
        for j, line in enumerate(ef.wrap_lines(t, 584)):
            o.append('<text x="54" y="%d" class="%s">%s</text>'
                     % (y + j * 19, cls, ef.esc(line)))
            last = j
        y += 19 * (last + 1) + 8
    y += 8
    o.append('<text x="16" y="%d" class="t-bad">'
             '첫 줄이 이 데이터셋에서 가장 잘게 쪼갠 서술이다 — AI 엔지니어가 하는 거의 '
             '모든 일이 여기 든다</text>' % y)
    o.append(ef.lab(16, y + 20, 'O*NET 은 미국 경제의 직업 약 1,000개를 담은 표준 데이터셋인데, '
                                '알갱이가 이만큼 굵다', fs=13))
    return ef.svg(y + 32, ''.join(o))


# ══ ④ AI R&D O*NET 의 6개 범주 ═══════════════════════════════════════════
# 원문 그림은 도넛 여섯 조각에 범주 이름과 예시가 붙어 있다. 이름과 예시 문장을
# 그대로 옮기고, 순서가 한 바퀴 도는 것이 보이게 고리로 세웠다.
SIX = [
    ('1. 정한다 DECIDE', ['새 어텐션 변형 MLA 를 표준 MHA 와', '견주는 실험을 하기로 정한다']),
    ('2. 설계한다 DESIGN', ['실험 계획을 쓴다 — 10B 모델·100B 토큰,',
                        'MLA 대 MHA 를 4K·32K 문맥 MMLU 로']),
    ('3. 만든다 BUILD', ['트레이너에 MLA 코드를 쓴다 — 잠재 투영을',
                      '넣고 어텐션을 고쳐 FSDP 와 붙인다']),
    ('4. 돌린다 RUN', ['100B 토큰으로 학습 둘을 띄우고',
                    '손실·그래드놈 대시보드를 지켜본다']),
    ('5. 분석한다 ANALYZE', ['시드 5개에 걸쳐 MLA 와 MHA 를 견주고',
                         'MLA 가 나은지 판정한다']),
    ('6. 알린다 COMMUNICATE', ['주요 발견과 시사점(예: 벤치마크 점수에 준',
                           '영향)을 정리한 메모를 다른 팀에 쓴다']),
]


def fig_onet_six():
    """6개 범주. 원문은 도넛인데 원 위에 글자를 눕히면 읽히지 않아 고리로 폈다.

    범주 이름·번호·예시 문장은 원문 그림에 적힌 그대로다."""
    o = [ef.lab(16, 20, 'AI R&D 전용 O*NET 의 6개 범주 — 실험 하나가 도는 한 바퀴', fs=13)]
    LX, RX, BW = 8, 332, 300
    lcx, rcx = LX + BW // 2, RX + BW // 2
    ys = [56, 154, 252]
    order = [(LX, 0, 0), (LX, 1, 1), (LX, 2, 2), (RX, 2, 3), (RX, 1, 4), (RX, 0, 5)]
    hh = 0
    for x, row, idx in order:
        name, lines = SIX[idx]
        s, hh = ef.box(x, ys[row], BW, name, lines, key=(idx in (0, 5)))
        o.append(s)
    bot = ys[2] + hh
    for i in (0, 1):
        o.append(ef.arrow('svc', [(lcx, ys[i] + hh), (lcx, ys[i + 1])]))
        o.append(ef.arrow('svc', [(rcx, ys[i + 1]), (rcx, ys[i] + hh)]))
    o.append(ef.arrow('svc', [(lcx, bot), (lcx, bot + 26), (rcx, bot + 26), (rcx, bot)]))
    o.append(ef.arrow('svc', [(rcx, ys[0]), (rcx, 34), (lcx, 34), (lcx, ys[0])]))
    o.append(ef.lab(16, bot + 46, '결정에서 시작해 알리는 데서 끝나고, 알린 결과가 다음 결정으로 '
                                  '돌아온다', fs=13))
    o.append(ef.lab(16, bot + 62, '이 여섯 아래에 하위 범주가 있고, 그 아래에 60개 넘는 과제가 '
                                  '적힌다', fs=13))
    return ef.svg(bot + 74, ''.join(o))


# ══ ⑤ 과제 목록의 한 쪽 — 4.1 실행 감시 ═════════════════════════════════
RUN_TASKS = [
    ('4', '실행을 띄운다 — 학습·RL·평가',
     '예: 정해 둔 스펙으로 다음 사전학습 실행을 띄우고 첫 수백 스텝이 정상인지 확인한다'),
    ('3', '실행이 나아가는 동안 문제를 살핀다',
     '손실 급등·조용한 정확성 버그·발산·보상 해킹을 본다'),
    ('2', '원인을 진단하고 되돌리는 수를 쓴다',
     '예: 급등을 최근에 들어온 저품질·손상 샤드까지 되짚어 마지막 성한 체크포인트로 되돌린다'),
]


def fig_onet_sample():
    """과제 목록이 실제로 어떻게 생겼나 — 4번 범주 아래 4.1 실행 감시 한 쪽.

    입력·출력 줄과 과제 문장, 그리고 과제 앞에 붙은 자동화 등급 숫자([4]·[3]·[2])까지
    원문 그림에 적힌 그대로 옮겼다."""
    o = [ef.lab(16, 20, '과제 목록 한 쪽 — 6개 범주 가운데 4번 아래 하위 범주 하나', fs=13)]
    y = 44
    s, h = ef.box(8, y, 626, '4. 돌린다 RUN',
                  ['입력 — 만들어 둔 학습 잡, 평가 묶음, 또는 돌아가는 시스템',
                   '출력 — 끝난 실행, 그리고 잡아내 고친 실패'])
    o.append(s)
    o.append(ef.arrow('svc', [(320, y + h), (320, y + h + 24)]))
    y += h + 24
    s, h = ef.box(8, y, 626, '4.1 실행 감시',
                  ['학습·강화학습·평가 실행을 돌아가는 중에 지켜보고, 문제가 나타나면 잡아',
                   '정상 궤도로 되돌린다',
                   '입력 — 돌아가는 학습·RL·평가 잡과 그 실시간 계측',
                   '출력 — 성공으로 끝난 실행, 또는 정상 상태로 되돌리는 개입'], key=True)
    o.append(s)
    y += h + 28
    o.append('<text x="34" y="%d" class="t-role" text-anchor="middle">등급</text>' % (y - 8))
    o.append(ef.lab(72, y - 8, '과제', fs=13))
    for grade, name, ex in RUN_TASKS:
        s, h = ef.box(56, y, 578, name, ef.wrap_lines(ex, 578))
        o.append('<text x="34" y="%d" class="t-lab" text-anchor="middle">%s</text>'
                 % (y + 22, grade))
        o.append(s)
        y += h + 12
    o.append(ef.lab(16, y + 10, '왼쪽 숫자는 지금 AI 가 그 과제를 얼마나 대신하는지를 매긴 0~5 '
                                '등급이다 — 4 는 이끈다,', fs=13))
    o.append(ef.lab(16, y + 26, '3 은 협업한다, 2 는 거든다. 필자들이 매긴 값이고 주관적이라고 '
                                '먼저 적어 두었다', fs=13))
    return ef.svg(y + 38, ''.join(o))


# ══ ⑥ 기대와 실제 — 사전학습 + 사후학습으로 안 갈라진다 ═════════════════
def fig_onet_expect():
    """「사전학습 + 사후학습」이라는 두 칸과, 실제 학습 과정의 얽힘.

    원문은 세로로 긴 판인데 640px 가로에 맞추느라 자리를 다시 잡았다. 상자 이름
    여덟(초기화 모델 둘·모델 X·체크포인트 #0~#3·배포 모델)과 선 위 글자, 실선·점선의
    구분은 원문 그대로다. 원문에 없는 상자나 화살표는 넣지 않았다."""
    o = [ef.lab(16, 20, '기대 — 두 칸이면 끝난다', fs=13)]
    s1, h1 = ef.box(8, 32, 150, '초기화 모델', [])
    s2, _ = ef.box(482, 32, 150, '배포 모델', [])
    o += [s1, s2]
    my = 32 + h1 // 2
    o.append(ef.arrow('svc', [(158, my), (300, my)]))
    o.append(ef.lab(186, my - 6, '사전학습', fs=13))
    o.append('<circle cx="316" cy="%d" r="3" fill="var(--ink-3)"/>' % my)
    o.append(ef.arrow('svc', [(332, my), (482, my)]))
    o.append(ef.lab(360, my - 6, '사후학습', fs=13))
    o.append(_axis([(8, 92), (632, 92)]))
    o.append(ef.lab(16, 112, '실제 — 어느 하나도 그 두 칸에 얌전히 들어가지 않는다', fs=13))

    B = 124                                   # 실제 판이 시작하는 자리
    o2 = []
    a, ha = ef.box(8, B, 108, '초기화 모델', [])
    mx, _ = ef.box(190, B, 150, '모델 X', [])
    rb, _ = ef.box(470, B, 150, '초기화 모델', [])
    o2 += [a, mx, rb]
    spine = 62
    # 모델 X → 체크포인트 #0
    o2.append(ef.arrow('svc', [(265, B + 34), (265, B + 86)]))
    o2.append(ef.lab(272, B + 56, '데이터 품질을', fs=13))
    o2.append(ef.lab(272, B + 70, '채점하도록 파인튜닝한다', fs=13))
    cp0, _ = ef.box(190, B + 86, 150, '체크포인트 #0', [])
    o2.append(cp0)
    # 체크포인트 #0 ⇢ 사전학습 데이터 거르기
    o2.append(ef.arrow('cond', [(190, B + 103), (70, B + 103), (70, B + 60), (66, B + 60)]))
    o2.append(ef.lab(70, B + 142, '사전학습 데이터를 거른다', fs=13))
    o2.append(ef.lab(68, B + 54, '사전학습', fs=13))
    # 왼쪽 등뼈 — 초기화 모델에서 내려오며 세 번 갈린다
    o2.append(ef.arrow('svc', [(spine, B + 34), (spine, B + 150)]))
    o2.append('<circle cx="%d" cy="%d" r="3" fill="var(--ink-3)"/>' % (spine, B + 150))
    o2.append(ef.arrow('svc', [(spine, B + 168), (190, B + 168)]))
    o2.append(ef.lab(96, B + 162, 'SFT + RL', fs=13))
    cp1, _ = ef.box(190, B + 151, 150, '체크포인트 #1', [])
    o2.append(cp1)
    o2.append(ef.arrow('svc', [(spine, B + 150), (spine, B + 240)]))
    o2.append(ef.lab(68, B + 200, '계속 사전학습', fs=13))
    o2.append('<circle cx="%d" cy="%d" r="3" fill="var(--ink-3)"/>' % (spine, B + 240))
    o2.append(ef.arrow('svc', [(spine, B + 258), (190, B + 258)]))
    o2.append(ef.lab(72, B + 252, 'SFT', fs=13))
    o2.append('<circle cx="126" cy="%d" r="3" fill="var(--ink-3)"/>' % (B + 258))
    o2.append(ef.lab(160, B + 252, 'RL', fs=13))
    cp3, _ = ef.box(190, B + 241, 150, '체크포인트 #3', [])
    o2.append(cp3)
    o2.append(ef.arrow('svc', [(spine, B + 240), (spine, B + 330), (190, B + 330)]))
    o2.append(ef.lab(68, B + 294, 'RL', fs=13))
    cp2, _ = ef.box(190, B + 313, 150, '체크포인트 #2', [])
    o2.append(cp2)
    # 체크포인트 #1 ⇢ RL 검증자
    o2.append(ef.arrow('cond', [(265, B + 185), (265, B + 220), (145, B + 220),
                                (145, B + 254)]))
    o2.append(ef.lab(155, B + 214, 'RL 검증자로 쓴다', fs=13))
    # 체크포인트 #2 ⇢ 합성 SFT 데이터
    o2.append(ef.arrow('cond', [(265, B + 313), (265, B + 302), (100, B + 302),
                                (100, B + 262)]))
    o2.append(ef.lab(108, B + 294, '합성 SFT 데이터를 만든다', fs=13))
    # 체크포인트 #3 ⇢ 교사
    o2.append(ef.arrow('cond', [(340, B + 258), (380, B + 258), (380, B + 80),
                                (541, B + 80)]))
    o2.append(ef.lab(430, B + 74, '교사', fs=13))
    # 오른쪽 — 증류하고 도메인별 RL 을 붙였다가 가중치를 병합한다
    o2.append(ef.arrow('svc', [(545, B + 34), (545, B + 96)]))
    o2.append(ef.lab(538, B + 52, '교사 체크포인트 #3 에서', anchor='end', fs=13))
    o2.append(ef.lab(538, B + 66, '증류한다', anchor='end', fs=13))
    o2.append('<circle cx="545" cy="%d" r="3" fill="var(--ink-3)"/>' % (B + 96))
    o2.append(ef.arrow('svc', [(545, B + 96), (482, B + 96), (482, B + 150)]))
    o2.append(ef.arrow('svc', [(545, B + 96), (608, B + 96), (608, B + 150)]))
    o2.append(ef.lab(476, B + 122, 'RL 도메인 A', anchor='end', fs=13))
    o2.append(ef.lab(604, B + 122, 'RL 도메인 B', anchor='end', fs=13))
    o2.append(ef.arrow('cond', [(482, B + 150), (608, B + 150)]))
    o2.append(ef.lab(508, B + 144, '가중치 병합', fs=13))
    o2.append(ef.arrow('svc', [(545, B + 150), (545, B + 182)]))
    dep, hd = ef.box(470, B + 182, 150, '배포 모델', [])
    o2.append(dep)
    bot = B + 347
    o.append(''.join(o2))
    o.append(ef.lab(16, bot + 22, '실선은 학습 단계, 점선은 다른 모델이 만들어 준 것을 끌어다 '
                                  '쓰는 자리다', fs=13))
    o.append(ef.lab(16, bot + 38, '「실험 코드 쓰기」 같은 과제가 이 여러 자리에 되풀이돼서, '
                                  '사전학습·사후학습으로', fs=13))
    o.append(ef.lab(16, bot + 54, '가르는 분류는 접었다', fs=13))
    return ef.svg(bot + 66, ''.join(o))


# ══ 등록 ═════════════════════════════════════════════════════════════════
FIGS = {
    'onet_sa': fig_onet_sa,
    'onet_sc': fig_onet_sc,
    'onet_tasks15': fig_onet_tasks15,
    'onet_six': fig_onet_six,
    'onet_sample': fig_onet_sample,
    'onet_expect': fig_onet_expect,
}

# 카드에 실을 때 쓰는 캡션. 형태를 바꾼 그림은 왜 바꿨는지가 여기 들어 있다.
CAPS = {
    'onet_sa': '「Situational Awareness」(Leopold Aschenbrenner)의 그림이다. 곡선과 부채꼴은 '
               '원본 이미지의 축 눈금을 재서 데이터 좌표로 되돌린 값이다 — 2018년 10⁻⁷, '
               '2023년 1, 2028년 약 10⁶이고 2028년 폭은 10⁴~10⁷이다. '
               '값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
    'onet_sc': 'AI 2027 시나리오의 시간지평 외삽이다. 분위수는 원문 그림에 인쇄된 글자를 그대로 '
               '옮겼고, 곡선은 축 눈금을 재서 읽었다. 니콜라 곡선의 마루는 원문에서 범례 상자에 '
               '가려 있어 반투명 상자 아래로 비치는 자리를 뽑아 이었다. '
               '값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
    'onet_tasks15': '원문 그림은 O*NET 화면 갈무리다. 목록이라 목록 그대로 두고 문장만 한국어로 '
                    '옮겼다. 값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
    'onet_six': '원문은 도넛 여섯 조각이다. 원 위에 한국어를 눕히면 읽히지 않아 고리로 폈고, '
                '범주 이름·번호·예시 문장은 그대로 두었다. '
                '값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
    'onet_sample': '원문 그림은 제안 문서의 한 쪽이다. 입력·출력 줄, 과제 문장, 과제 앞에 붙은 '
                   '자동화 등급 [4]·[3]·[2]까지 그대로 옮겼다. '
                   '값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
    'onet_expect': '원문은 세로로 긴 판이라 640px 가로에 맞추느라 자리를 다시 잡았다. 상자 여덟과 '
                   '선 위 글자, 실선·점선의 구분은 원문 그대로이고 없는 상자나 화살표는 넣지 '
                   '않았다. 값은 Epoch AI 원문 도해(CC-BY)를 따랐다.',
}

assert set(FIGS) == set(CAPS), '캡션이 없는 그림: %s' % (set(FIGS) ^ set(CAPS))


if __name__ == '__main__':
    import io

    sys.stdout.reconfigure(encoding='utf-8')
    HERE = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scripts'))
    import check_fig
    from card_lib import FIG_CSS, FIG_DEFS

    bad, parts = 0, []
    for k, fn in FIGS.items():
        s = fn()
        miss = check_fig.hits(s)
        print('%s %s' % ('FAIL' if miss else 'OK  ', k))
        for m in miss:
            print('       ! %s' % m)
        bad += len(miss)
        parts.append('<figure class="uc-fig"><p class="fig-title">%s</p>%s'
                     '<figcaption>%s</figcaption></figure>' % (k, s, CAPS[k]))
    print('FAIL %d건' % bad)
    out = os.path.join(HERE, '_epochfig_onet.html')
    io.open(out, 'w', encoding='utf-8').write(
        '<!doctype html><meta charset="utf-8"><style>body{background:#fff;color:#1a2233;'
        'font-family:"Pretendard","Apple SD Gothic Neo",system-ui,sans-serif;max-width:760px;'
        'margin:20px auto}:root{--ink:#1a2233;--ink-2:#3d4759;--ink-3:#8a8a8a;--line:#dde2ea}'
        + FIG_CSS + '</style>' + FIG_DEFS + ''.join(parts))
    print('->', out)
