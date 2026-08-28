# -*- coding: utf-8 -*-
"""그래프는 손으로 path 를 적지 않고 matplotlib 으로 뽑는다.

곡선을 `M386 196 Q386 274 566 274` 처럼 손으로 적으면 두 가지가 무너진다. 곡선의
모양이 식에서 나온 것이 아니라 눈으로 맞춘 것이 되고, 축·눈금·여백이 그림마다 달라진다.
여기서는 식과 축 이름만 주고 판은 matplotlib 이 잡는다.

내보낸 SVG 를 그대로 쓰지는 않는다. matplotlib 은 색을 값으로 박아 넣어서 다크모드에서
검은 선이 검은 배경에 깔린다. `to_inline()` 이 그 색을 CSS 변수로 바꿔 끼우고, 글자는
`svg.fonttype='none'` 으로 두어 `<text>` 로 남긴다 — 화면 붓을 그대로 타고,
`check_fig` 도 좌표를 읽을 수 있다.

    svg = line_chart(...)      # 인라인 SVG 문자열 하나

축에 수를 달지 않는 그림도 있다. 원문에 점도 눈금도 없으면 눈금을 지운다 —
모양만 뜻이 있고 자리는 값이 아니라는 것을 그림이 스스로 말해야 한다.
"""
import io
import re

import matplotlib
matplotlib.use('Agg')
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt      # noqa: E402

# 글자를 path 로 굽지 않는다. `<text>` 로 남아야 화면 붓을 타고 `check_fig` 가 좌표를 읽는다
matplotlib.rcParams['svg.fonttype'] = 'none'
# 한글 글꼴을 안 걸면 글자 폭을 DejaVu 로 재서 자리가 어긋나고 경고가 쏟아진다
for _p in ('C:/Windows/Fonts/malgun.ttf',):
    try:
        fm.fontManager.addfont(_p)
        matplotlib.rcParams['font.family'] = fm.FontProperties(fname=_p).get_name()
        break
    except Exception:
        pass
matplotlib.rcParams['axes.unicode_minus'] = False

# 색을 값으로 박고 나중에 변수로 바꿔 끼운다. 여기 쓴 값은 화면에 안 나간다
INK = '#111111'      # 글자
LINE = '#888888'     # 축
ACCENT = '#2563eb'   # 곡선
SUB = '#555555'      # 곁글

SWAP = [(INK, 'var(--ink-2)'), (LINE, 'var(--line)'),
        (ACCENT, 'var(--accent)'), (SUB, 'var(--ink-3)')]


def to_inline(fig, alt, cls='fg-plot'):
    """matplotlib figure 를 카드에 넣을 인라인 SVG 로."""
    buf = io.StringIO()
    fig.savefig(buf, format='svg', bbox_inches='tight', pad_inches=0.02,
                transparent=True)
    plt.close(fig)
    s = buf.getvalue()
    s = s[s.index('<svg'):]
    s = re.sub(r'<metadata>.*?</metadata>', '', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    # 판 크기는 카드가 정한다. width/height 를 떼고 viewBox 만 남긴다
    s = re.sub(r'<svg([^>]*?)\swidth="[^"]*"', r'<svg\1', s, count=1)
    s = re.sub(r'<svg([^>]*?)\sheight="[^"]*"', r'<svg\1', s, count=1)
    for a, b in SWAP:
        s = s.replace(a, b).replace(a.upper(), b)
    s = re.sub(r"'Malgun Gothic'",
               "-apple-system,'Segoe UI','Malgun Gothic',sans-serif", s)  # style 이
    # 큰따옴표로 묶이므로 글꼴 이름은 작은따옴표로 둔다
    s = s.replace('<svg ', '<svg class="%s" width="100%%" role="img" '
                           'aria-label="%s" ' % (cls, alt), 1)
    return re.sub(r'\s+', ' ', s).replace('> <', '><')


def frontier(f, x0, x1, xlabel, ylabel, alt, notes=(), box=(), n=200, size=(6.4, 2.6)):
    """맞바꿈 곡선 하나. f(x) 로 모양을 주고 눈금은 달지 않는다.

    축 이름은 **재는 것만** 짧게 단다(「엔드투엔드 지연」). 어느 쪽이 큰지와 곡선을
    어떻게 읽는지는 `box` 로 준다 — 오른쪽 위 빈 자리에 상자로 앉는다. 축 이름에
    다 적으면 이름이 길어져 가로축이 판보다 넓어지고 세로축은 돌아누운 채 잘린다.

    맞바꿈 곡선은 왼쪽 위에서 오른쪽 아래로 내려가므로 오른쪽 위가 늘 빈다.

    notes = [(x비율, y비율, 글, 굵게)] — 판 안에 따로 앉히는 곁글.
    """
    xs = [x0 + (x1 - x0) * i / float(n - 1) for i in range(n)]
    ys = [f(x) for x in xs]
    fig, ax = plt.subplots(figsize=size)
    ax.plot(xs, ys, color=ACCENT, lw=1.6, solid_capstyle='round')
    ax.set_xlim(x0 - (x1 - x0) * 0.04, x1 + (x1 - x0) * 0.08)
    lo, hi = min(ys), max(ys)
    ax.set_ylim(lo - (hi - lo) * 0.12, hi + (hi - lo) * 0.12)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(LINE)
        ax.spines[side].set_linewidth(1.0)
    ax.set_xlabel(xlabel, color=INK, fontsize=11, labelpad=5)
    ax.set_ylabel(ylabel, color=INK, fontsize=11, labelpad=5)
    if box:
        ax.text(0.985, 0.95, chr(10).join(box), transform=ax.transAxes, color=SUB,
                fontsize=10.5, ha='right', va='top', linespacing=1.5,
                bbox=dict(boxstyle='square,pad=0.55', facecolor='none',
                          edgecolor=LINE, linewidth=1.0))
    for fx, fy, text, bold in notes:
        ax.text(fx, fy, text, transform=ax.transAxes, color=INK if bold else SUB,
                fontsize=10.5, fontweight='bold' if bold else 'normal',
                ha='left', va='center')
    return to_inline(fig, alt)
