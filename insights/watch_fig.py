# -*- coding: utf-8 -*-
"""워치 트렌드 도해 — 시계열 선 하나.

값은 어댑터가 채운 metric 의 series([(때, 값), …])만 쓴다. **이 파일은 값을 만들지
않는다** — 없는 값을 그리는 사고(insight-figure 규칙 1)를 구조적으로 막으려는 것이다.
series 가 비면 그림을 안 그리고 None 을 준다.

좌표는 손으로 안 찍는다(규칙 2). x 는 몇 번째 점인지를 받는 함수 하나, y 는 값을 받는
함수 하나에서만 나온다. 글자는 판 밖 — 축 눈금은 판 왼쪽·아래, 범례와 설명은 판 아래다(규칙 3).
"""
import re

W = 640
X0, X1 = 96, 560          # 판 좌우. 왼쪽 96 은 세로 눈금 글자 자리다
Y0, Y1 = 62, 300          # 판 위아래
COLORS = ('var(--fig-blue,#2f6fd0)', 'var(--fig-good,#2f8f6b)', 'var(--warn,#c2831f)')


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def _ticks(lo, hi, n=4):
    """세로 눈금값. 자의 눈금이지 원문에서 가져온 값이 아니다 — 값 대조에서 뺀다."""
    if hi <= lo:
        hi = lo + 1.0
    step = (hi - lo) / float(n)
    return [lo + step * i for i in range(n + 1)]


def _fmt(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def trend(lines, ylabel, note='', threshold=None):
    """시계열 선 도해.

    lines     = [(이름, [(때, 값), …]), …]  — 최대 셋. 같은 것을 여러 곳에서 견주는
                것(구 셋의 같은 지수)은 축이 하나라 한 판에 둔다. 축이 다르면 판을 나눈다
    ylabel    = 세로 자가 무엇인지. 「지수(2021.6=100)」처럼 기준까지 적는다
    threshold = (이름, 값) 이면 문턱을 점선으로 하나 긋는다. 트리거 조건을 눈으로 보게 하는 자리
    반환      = SVG 문자열. 그릴 값이 없으면 None
    """
    lines = [(n, s) for n, s in lines if s]
    if not lines:
        return None                      # 값이 없으면 안 그린다
    assert len(lines) <= 3, '선이 넷이면 그림을 나눈다 — 축이 둘이라는 뜻이다'

    xs = [t for _, s in lines for t, _ in s]
    order = sorted(set(xs))
    vals = [v for _, s in lines for _, v in s] + ([threshold[1]] if threshold else [])
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.12 or 1.0
    lo, hi = lo - pad, hi + pad

    def px(t):
        """때 하나의 x. 자리를 눈으로 어림하지 않으려고 순서에서만 낸다."""
        i = order.index(t)
        return X0 + (X1 - X0) * i / float(max(len(order) - 1, 1))

    def py(v):
        return Y1 - (Y1 - Y0) * (v - lo) / float(hi - lo)

    o = []
    # 세로 자 이름 — 판 위가 아니라 판 위쪽 바깥이다
    o.append('<text x="16" y="24" class="t-sm" style="font-weight:800">%s</text>' % esc(ylabel))
    # 격자 먼저(뒤에 깔린다)
    ys = _ticks(lo, hi)
    o.append(''.join('<path class="grid" d="M%.1f %.1f L%.1f %.1f"/>'
                     % (X0, py(v), X1 + 14, py(v)) for v in ys))
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y1, X1 + 14, Y1))
    for v in ys:
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%s</text>'
                 % (X0 - 8, py(v) + 4, _fmt(v)))
    # 가로 눈금은 처음·가운데·끝 셋만. 다 적으면 글자가 겹친다
    for i in dict.fromkeys([0, len(order) // 2, len(order) - 1]):
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (px(order[i]), Y1 + 22, esc(order[i])))
    # 문턱 — 트리거 조건을 판에서 보게 한다. 이름은 판 밖 범례가 말한다
    if threshold:
        o.append('<path d="M%d %.1f L%d %.1f" stroke="var(--warn,#c2831f)" stroke-width="1.6" '
                 'stroke-dasharray="6 4" fill="none"/>' % (X0, py(threshold[1]),
                                                           X1 + 14, py(threshold[1])))
    for i, (name, s) in enumerate(lines):
        c = COLORS[i % len(COLORS)]
        pts = ' '.join('%.1f,%.1f' % (px(t), py(v)) for t, v in s)
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="3"/>' % (pts, c))
        t, v = s[-1]
        o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s"/>' % (px(t), py(v), c))

    # 범례·설명은 전부 판 아래다(규칙 3)
    y = Y1 + 46
    for i, (name, _s) in enumerate(lines):
        o.append('<rect x="16" y="%d" width="18" height="4" rx="2" fill="%s"/>' % (y - 5, COLORS[i]))
        o.append('<text x="42" y="%d" class="t-sm">%s</text>' % (y, esc(name)))
        y += 20
    if threshold:
        o.append('<path d="M16 %d L34 %d" stroke="var(--warn,#c2831f)" stroke-width="1.6" '
                 'stroke-dasharray="6 4"/>' % (y - 5, y - 5))
        o.append('<text x="42" y="%d" class="t-sm">%s</text>' % (y, esc(threshold[0])))
        y += 20
    if note:
        o.append('<text x="16" y="%d" class="t-sm t-axis">%s</text>' % (y, esc(note)))
        y += 20
    return ('<svg viewBox="0 0 %d %d" role="img" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (W, y, ''.join(o)))


def from_triggers(triggers, ylabel, note='', which=None):
    """워치 줄의 트리거에서 바로 그린다. series 가 든 값 트리거만 쓴다 —
    비어 있으면 None 이라 어댑터가 붙기 전에는 카드에 그림이 아예 안 선다."""
    picked = [(t['what'], t['series']) for t in triggers
              if t.get('series') and (which is None or t['metric'] in which)]
    return trend(picked[:2], ylabel, note)


def nums_in(svg):
    """그림 글자에 든 수. 원문 대조에 쓴다 — 축 눈금(t-axis)은 자의 눈금이라 뺀다."""
    out = set()
    for m in re.finditer(r'<text[^>]*?class="([^"]*)"[^>]*>([^<]*)<', svg or ''):
        if 't-axis' in m.group(1):
            continue
        out |= set(re.findall(r'\d[\d,\.]*', m.group(2)))
    return out
