# -*- coding: utf-8 -*-
"""AgentX 프런티어 층의 도해 셋. 색은 회색만(확정 규칙 S2).

판은 하나다 — 가로가 사용자 한 명이 받는 속도(P90 TPS), 세로가 GPU 한 장 처리량인
좌표면. 세 도해가 그 판의 서로 다른 자리를 본다. ① 곡선 셋 전체, ② 100 TPS 한 줄을
설정 일곱으로 편 순위, ③ GB300 TRT 곡선 끝 부근을 확대한 배수.

선과 점은 전부 원자료(API 행)와 우리 모델(check_agentx 와 같은 함수)이 낸 값이다.
좌표는 손으로 안 찍는다 — _px·_py 가 값에서 낸다.
"""
import _biz_fig as bf
import _agentx_tbl as T

CA, AX = T.CA, T.AX
_svg, _lt = bf._svg, bf._lt
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'
NUM = '①②③④⑤⑥⑦⑧⑨'


def _t(cx, y, s, cls='t-sm', anchor='middle'):
    return '<text x="%.1f" y="%.1f" text-anchor="%s" class="%s">%s</text>' % (cx, y, anchor, cls, s)


def _mark(x, y, n):
    """동그라미 번호. ①이 이미 동그라미라 테두리를 또 두르지 않는다."""
    return ('<circle cx="%.1f" cy="%.1f" r="10" fill="var(--paper)"/>%s'
            % (x, y, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    return ''.join(_lt(20, y + i * 21, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


# ── 판. P90 속도 × GPU 한 장 처리량 ─────────────────────────────────────
_X0, _XW, _Y0, _YH = 84, 520, 62, 210
_XMAX, _YMAX = 300.0, 240000.0
_XT = (0, 50, 100, 150, 200, 250, 300)
_YT = (0, 60000, 120000, 180000, 240000)
_SERIES = [('vr', INK, '2.6', ''), ('gb300_sgl', INK2, '2', '7 4'),
           ('gb300_trt', INK3, '2', '2 3')]


def _px(x):
    return _X0 + _XW * x / _XMAX


def _py(y):
    return _Y0 + _YH - _YH * y / _YMAX


def _axes():
    out = ['<path d="M%d %d V%d H%d" stroke="var(--line)" stroke-width="1.2" fill="none"/>'
           % (_X0, _Y0, _Y0 + _YH, _X0 + _XW)]
    out += [_t(_px(x), _Y0 + _YH + 16, '%d' % x) for x in _XT]
    out += [_t(_X0 - 8, _py(y) + 4, '%d만' % (y // 10000) if y else '0', 't-sm', 'end')
            for y in _YT]
    return ''.join(out)


def _curve(key, stroke, width, dash):
    front = CA.S[key][1]
    xs = [AX._x(e) for e in front]
    lo, hi = min(xs), max(xs)
    n = 120
    pts = []
    for i in range(n + 1):
        s = lo + (hi - lo) * i / n
        v = CA.tput(key, s)
        pts.append('%.1f %.1f' % (_px(s), _py(v)))
    out = ['<path d="M%s" fill="none" stroke="%s" stroke-width="%s"%s/>'
           % (' L'.join(pts), stroke, width,
              ' stroke-dasharray="%s"' % dash if dash else '')]
    out += ['<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (_px(AX._x(e)), _py(AX._y(e)), stroke)
            for e in front]
    return ''.join(out)


def _vline(s, n):
    x = _px(s)
    return ('<path d="M%.1f %d V%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 4"/>'
            % (x, _Y0 - 4, _Y0 + _YH, INK3) + _mark(x, _Y0 - 16, n))


def _key(y):
    out = []
    for i, (key, stroke, width, dash) in enumerate(_SERIES):
        x = 20 + i * 205
        out.append('<path d="M%d %d H%d" stroke="%s" stroke-width="%s"%s/>'
                   % (x, y, x + 30, stroke, width,
                      ' stroke-dasharray="%s"' % dash if dash else ''))
        out.append(_lt(x + 38, y + 5, CA.label(key).replace(' NVL72', ''), 't-sm', False))
    return ''.join(out)


FIG_CURVE = _svg(W, 420, '루빈과 GB300 두 엔진 — 곡선 셋을 같은 속도 선에서 읽는다', ''.join(
    [_lt(20, 26, '가로 사용자 한 명이 받는 속도(P90 TPS) · 세로 GPU 한 장 처리량(tok/s)'),
     _axes()]
    + [_curve(*s) for s in _SERIES]
    + [_vline(75, 1), _vline(100, 2), _vline(170, 3),
       _key(_Y0 + _YH + 46),
       _legend(_Y0 + _YH + 84, ['75 TPS — 기가와트당 매출을 셈한 속도',
                                '100 TPS — 메가와트당 토큰 표의 속도',
                                '170 TPS — 「67배」를 적은 속도'])]
))


# ── 100 TPS 한 줄을 일곱 설정으로 편 순위 ───────────────────────────────
_RBX, _RBW = 250, 290


def _rank():
    rows = sorted(((CA.permw(k, 100), k) for k in T._ORDER), reverse=True)
    top = rows[0][0]
    out = []
    for i, (v, k) in enumerate(rows):
        y = 50 + i * 36
        on = k == 'vr'
        out.append(_lt(20, y + 17, '%d' % (i + 1), 't-sm', on))
        out.append(_lt(40, y + 17, CA.label(k).replace(' NVL72', ''), 't-sm', on))
        w = _RBW * v / top
        out.append('<rect x="%d" y="%d" width="%.1f" height="22" rx="3" fill="%s"/>'
                   % (_RBX, y, max(w, 1.5), INK if on else INK3))
        out.append(_lt(int(_RBX + w) + 8, y + 17, '%.2f' % v if v < 10 else '%.1f' % v,
                       't-sm', on))
    return ''.join(out)


FIG_RANK = _svg(W, 310, '100 TPS 에서 1메가와트가 내는 토큰 — 일곱 설정', ''.join(
    [_lt(20, 28, '1메가와트당 초당 토큰(백만) · 막대 길이는 0 에서 시작한다'), _rank()]
))


# ── GB300 TRT 곡선 끝 부근에서 배수가 움직이는 폭 ────────────────────────
_EX0, _EXW, _EY0, _EYH = 84, 500, 58, 190
_ELO, _EHI, _EYMAX = 160.0, 172.0, 80.0


def _ex(s):
    return _EX0 + _EXW * (s - _ELO) / (_EHI - _ELO)


def _ey(v):
    return _EY0 + _EYH - _EYH * v / _EYMAX


def _edge():
    end = max(AX._x(e) for e in CA.S['gb300_trt'][1])
    out = ['<path d="M%d %d V%d H%d" stroke="var(--line)" stroke-width="1.2" fill="none"/>'
           % (_EX0, _EY0, _EY0 + _EYH, _EX0 + _EXW)]
    out += [_t(_ex(s), _EY0 + _EYH + 16, '%d' % s) for s in (160, 164, 168, 172)]
    out += [_t(_EX0 - 8, _ey(v) + 4, '%d' % v, 't-sm', 'end') for v in (0, 20, 40, 60, 80)]
    pts = []
    s = _ELO
    while s <= end:
        pts.append('%.1f %.1f' % (_ex(s), _ey(CA.own('vr', 'gb300_trt', s))))
        s += 0.1
    out.append('<path d="M%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (' L'.join(pts), INK))
    for n, s in ((1, 170.0), (2, 171.4)):
        v = CA.own('vr', 'gb300_trt', s)
        out.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (_ex(s), _ey(v), INK))
        out.append(_mark(_ex(s) - 22 * (2 - n) - 6, _ey(v) - 4 - 18 * (n - 1), n))
    out.append('<path d="M%.1f %d V%d" stroke="%s" stroke-width="1.2" stroke-dasharray="4 4"/>'
               % (_ex(end), _EY0 - 4, _EY0 + _EYH, INK3))
    out.append(_mark(_ex(end) + 14, _EY0 + _EYH - 20, 3))
    return ''.join(out)


FIG_EDGE = _svg(W, 360, '곡선 끝 앞 2 TPS 안에서 달러당 배수가 60 에서 67 로 간다', ''.join(
    [_lt(20, 26, '루빈 ÷ GB300 TRT, 사서 운영할 때 1달러당 토큰 · 가로 P90 TPS'), _edge(),
     _legend(_EY0 + _EYH + 44, ['170 TPS — 원문이 적은 속도, 모델 62.6배',
                                '171.4 TPS — 모델이 67배에 닿는 속도',
                                'GB300 TRT 가 잰 가장 빠른 점, 171.53 TPS'])]
))
