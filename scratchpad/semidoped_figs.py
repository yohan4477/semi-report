# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해 — 인라인 SVG.

규칙 둘.

**원문에 없는 값을 그리지 않는다.** 막대 길이도 아이콘 개수도 수치로 읽히므로,
원문에 그 수가 없으면 길이를 쓰지 않고 상태 둘로 바꾼다.

**판 위 글자는 그 자체로 읽혀야 한다.** 줄여 쓴 말(600Gb)·잘린 문장·본문을 읽어야
뜻이 통하는 말을 두지 않는다. 도해는 본문 옆에 서지만 본문의 각주가 아니다.

좌표는 손으로 찍지 않고 아래 셈에서 나온다. 배치는 `scratchpad/check_fig.py` 가 본다.
"""

FIG_CSS = '''
.fg { font: 600 12px/1.35 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  fill: var(--ink-2); }
.fg-s { font-weight: 400; font-size: 11px; fill: var(--ink-3); }
.fg-b { fill: var(--surface); stroke: var(--line); stroke-width: 1.2; }
.fg-l { stroke: var(--line); stroke-width: 1.2; fill: none; }
.fg-d { stroke: var(--ink-3); stroke-width: 1.2; fill: none; stroke-dasharray: 3 3; }
.fg-c { stroke: var(--accent); stroke-width: 1.2; fill: none; }
'''

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))

import chart  # noqa: E402


def _box(x, y, w, h, label, sub='', hi=False):
    """상자 하나. 글자는 상자 안 가운데 두 줄로 앉힌다."""
    cx = x + w / 2.0
    o = ['<rect x="%g" y="%g" width="%g" height="%g" rx="6" class="fg-b"%s/>'
         % (x, y, w, h, ' style="stroke:var(--accent);stroke-width:2"' if hi else '')]
    ty = y + h / 2.0 + (0 if not sub else -5)
    o.append('<text x="%g" y="%g" class="fg" text-anchor="middle">%s</text>'
             % (cx, ty + 4, label))
    if sub:
        o.append('<text x="%g" y="%g" class="fg fg-s" text-anchor="middle">%s</text>'
                 % (cx, ty + 19, sub))
    return ''.join(o)


def _criteria():
    """잣대가 무엇에서 무엇으로 바뀌었나.

    값을 그리지 않는다. 원문에 든 것은 「무엇을 잣대로 골랐나」뿐이라 막대도 눈금도
    쓸 수 없다. 상자와 화살표로만 어느 쪽을 골랐는지 보인다.

    곡선은 이 판에 안 그린다. 파레토 곡선은 그림 한 장을 따로 받는다(`_pareto`) —
    한 그림은 하나만 말한다.

    상자 사이 띠를 32픽셀로 벌려 글자를 그 안에 앉힌다. 앞 판은 띠가 12픽셀뿐이라
    글자가 아래 상자 테두리에 깔렸다 — check_fig 가 잡았다.
    """
    W = 640
    Y1, GAP, BH = 44, 32, 46
    y2 = Y1 + BH + GAP
    y3 = y2 + BH + 14
    H = y3 + 12
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="잣대가 무엇에서 무엇으로 바뀌었나">' % (W, H)]
    o.append('<text x="20" y="24" class="fg">전 — 칩을 파는 회사가 정할 때</text>')
    o.append('<text x="360" y="24" class="fg">후 — 모델을 파는 회사가 정할 때</text>')
    o.append(_box(20, Y1, 250, BH, '총소유비용을 본다', '칩을 사서 굴리는 데 드는 돈'))
    o.append(_box(360, Y1, 250, BH, '① 엔드투엔드 지연',
                  '질문을 넣고 마지막 글자가 나올 때까지', hi=True))
    o.append(_box(360, y2, 250, BH, '② 요청당 전기에너지',
                  '한 번 답하는 데 쓰는 전기', hi=True))
    mid = Y1 + BH + GAP / 2.0
    o.append('<path d="M485 %g L485 %g" class="fg-d"/>' % (Y1 + BH + 3, mid - 9))
    o.append('<path d="M485 %g L485 %g" class="fg-d"/>' % (mid + 5, y2 - 3))
    o.append('<text x="497" y="%g" class="fg fg-s">둘은 같이 못 낮춘다</text>' % (mid + 4))
    o.append('<path d="M270 %g L352 %g" class="fg-l" marker-end="url(#fgA)"/>'
             % (Y1 + BH / 2.0, Y1 + BH / 2.0))
    o.append('<defs><marker id="fgA" markerWidth="8" markerHeight="8" refX="7" refY="4" '
             'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--ink-3)"/></marker></defs>')
    # 한 줄에 한 뜻. 앞 판은 이 말을 세 줄로 잘라 「잣대가 돈에서 / 사람이 겪는 것으로 /
    # 옮겼다」로 세웠고, 한 줄씩은 아무 뜻이 없었다 — check_fig 가 잡았다
    o.append('<text x="20" y="%g" class="fg fg-s">잣대가 바뀌었다</text>' % (y2 + 10))
    o.append('<text x="20" y="%g" class="fg fg-s">돈에서 사람 경험으로</text>' % (y2 + 28))
    o.append('</svg>')
    return ''.join(o)


def _pareto():
    """파레토 곡선 — 두 잣대를 같이 낮출 수 없다.

    손으로 path 를 적지 않는다. 곡선을 눈으로 맞추면 모양이 식에서 나온 것이 아니게 되고,
    축·여백이 그림마다 달라진다. `scripts/chart.py` 가 matplotlib 으로 뽑는다.

    **축에 수를 달지 않는다.** 원문에 점도 눈금도 없어서 곡선의 자리는 값이 아니다.
    모양이 말하는 것은 하나다 — 한쪽을 낮추면 다른 쪽이 올라간다.

    축에는 **재는 것만** 짧게 단다. 어느 쪽이 큰지와 곡선을 어떻게 읽는지는 오른쪽 위
    상자에 적는다 — 맞바꿈 곡선은 왼쪽 위에서 오른쪽 아래로 내려가므로 그 자리가 늘
    빈다. 축 이름에 다 적으면 가로축이 판보다 넓어지고 세로축은 돌아누운 채 잘린다.
    """
    return chart.frontier(
        lambda x: 1.0 / x, 1.0, 4.0,
        '엔드투엔드 지연', '요청당 전기',
        '두 잣대를 같이 낮출 수 없다',
        box=['가로축 — 오른쪽일수록 오래 걸린다',
             '세로축 — 위일수록 많이 쓴다',
             '이 선 위의 점만 낼 수 있다',
             '왼쪽 아래로 갈수록 좋다'])


def _domain():
    """칩을 묶는 두 단계 — 겹이 겹을 품는다.

    안쪽과 바깥을 **색으로** 가른다(강조색은 묶음 안, 회색은 묶음끼리). 한때 굵기 3 대 1
    로 속도 차이를 보였는데, 그 그림만 선이 다른 도해보다 굵어져 한 장에서 다음 장으로
    넘어갈 때 굵기가 뜻을 갖는 것처럼 읽혔다. 선 굵기는 어느 도해에서나 1.2 로 같고,
    600 과 200 이라는 수는 판 아래 범례에 글자로 남는다.

    칩을 128개 그리지 않는다. 세 개와 말줄임으로 두어 개수가 뜻이 되지 않게 한다 —
    앞 판은 상자를 넷 그려 놓고 「개수가 아니다」라는 변명을 판 위에 적었다.
    """
    W, H = 640, 262
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="칩을 묶는 두 단계">' % (W, H)]
    # 바깥 겹
    o.append('<rect x="16" y="34" width="608" height="176" rx="10" class="fg-b"/>')
    o.append('<text x="30" y="24" class="fg">큰 묶음 — 칩 최대 2,048개</text>')
    # 안쪽 겹 둘 + 말줄임
    for k, x0 in enumerate((34, 330)):
        o.append('<rect x="%g" y="52" width="240" height="118" rx="8" class="fg-b" '
                 'style="stroke:var(--accent);stroke-width:2"/>' % x0)
        o.append('<text x="%g" y="70" class="fg fg-s">작은 묶음 — 칩 128개</text>' % (x0 + 12))
        for i in range(3):
            cx = x0 + 26 + i * 68        # 칩 가운데 = cx + 26 → x0+52 · x0+120 · x0+188
            o.append('<rect x="%g" y="80" width="52" height="24" rx="4" class="fg-b"/>' % cx)
            o.append('<text x="%g" y="96" class="fg fg-s" text-anchor="middle">칩</text>'
                     % (cx + 26))
            # 선은 x·y 축에 평행하게만 간다. 곧장 못 가면 꺾어서 간다 —
            # 칩에서 수직으로 내려 공통 가로 버스에 붙는다(check_fig F6)
            o.append('<path d="M%g 104 L%g 120" stroke="var(--accent)" stroke-width="1.2" stroke-linecap="round" '
                     'fill="none"/>' % (cx + 26, cx + 26))
        # 가로 버스와 스위치로 내려가는 한 줄
        o.append('<path d="M%g 120 L%g 120" stroke="var(--accent)" stroke-width="1.2" stroke-linecap="round" '
                 'fill="none"/>' % (x0 + 52, x0 + 188))
        o.append('<path d="M%g 120 L%g 132" stroke="var(--accent)" stroke-width="1.2" stroke-linecap="round" '
                 'fill="none"/>' % (x0 + 120, x0 + 120))
        o.append('<rect x="%g" y="132" width="176" height="28" rx="5" class="fg-b"/>' % (x0 + 32))
        o.append('<text x="%g" y="150" class="fg fg-s" text-anchor="middle">'
                 'Tomahawk 6 스위치</text>' % (x0 + 120))
    # 작은 묶음끼리는 스위치를 거쳐 붙는다. 앞 판은 이 선을 상자 아래 허공에 그어
    # 어디에도 안 닿았다 — 스위치와 스위치를 잇는다
    o.append('<path d="M242 146 L362 146" stroke="var(--ink-3)" stroke-width="1.2" '
             'fill="none"/>')
    o.append('<text x="302" y="140" class="fg fg-s" text-anchor="middle">ESUN</text>')
    o.append('<text x="302" y="100" class="fg fg-s" text-anchor="middle">⋯</text>')
    # 굵기 범례 — 판 위가 아니라 판 아래
    o.append('<path d="M40 232 L92 232" stroke="var(--accent)" stroke-width="1.2" stroke-linecap="round" '
             'fill="none"/>')
    o.append('<text x="102" y="236" class="fg fg-s">작은 묶음 안 — 칩 하나가 초당 '
             '600기가비트</text>')
    o.append('<path d="M348 232 L400 232" stroke="var(--ink-3)" stroke-width="1.2" '
             'fill="none"/>')
    o.append('<text x="410" y="236" class="fg fg-s">묶음끼리 — 칩 하나가 초당 '
             '200기가비트</text>')
    o.append('</svg>')
    return ''.join(o)


def _numa():
    """HBM 을 같이 쓸 때와 조각내 전담시킬 때.

    가속기를 셋 그리지만 그 수는 원문에 없다 — 「가속기마다」라는 말만 있다. 그래서
    개수가 뜻이 되지 않게 판 아래에 적어 둔다. 대역폭 숫자도 안 쓴다. 이 그림이
    말하는 것은 양이 아니라 **기다림이 생기는 자리**다.
    """
    W, H = 640, 260
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="메모리를 같이 쓸 때와 조각내 전담시킬 때">' % (W, H)]
    o.append('<defs><marker id="fgN" markerWidth="8" markerHeight="8" refX="7" refY="4" '
             'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--ink-3)"/></marker></defs>')
    for k, (x0, head) in enumerate(((16, '전 — 한 덩어리를 같이 쓴다'),
                                    (336, '후 — 조각내 하나씩 맡긴다'))):
        o.append('<text x="%g" y="24" class="fg">%s</text>' % (x0 + 8, head))
        o.append('<rect x="%g" y="34" width="288" height="176" rx="10" class="fg-b"/>' % x0)
        for i in range(3):
            y = 48 + i * 46
            o.append('<rect x="%g" y="%g" width="86" height="34" rx="6" class="fg-b"/>'
                     % (x0 + 12, y))
            o.append('<text x="%g" y="%g" class="fg fg-s" text-anchor="middle">가속기</text>'
                     % (x0 + 55, y + 21))
            if k == 0:
                # 가로로 나가 공통 세로 줄에 붙고, 거기서 메모리로 한 번 꺾어 든다
                o.append('<path d="M%g %g L%g %g L%g 116 L%g 116" class="fg-l" '
                         'marker-end="url(#fgN)"/>'
                         % (x0 + 98, y + 17, x0 + 140, y + 17, x0 + 140, x0 + 176))
            else:
                o.append('<rect x="%g" y="%g" width="88" height="34" rx="6" class="fg-b" '
                         'style="stroke:var(--accent);stroke-width:2"/>' % (x0 + 176, y))
                o.append('<text x="%g" y="%g" class="fg fg-s" text-anchor="middle">'
                         '메모리 조각</text>' % (x0 + 220, y + 21))
                o.append('<path d="M%g %g L%g %g" class="fg-l" marker-end="url(#fgN)"/>'
                         % (x0 + 98, y + 17, x0 + 172, y + 17))
        if k == 0:
            o.append('<rect x="%g" y="82" width="88" height="68" rx="6" class="fg-b"/>'
                     % (x0 + 176))
            o.append('<text x="%g" y="112" class="fg fg-s" text-anchor="middle">메모리</text>'
                     % (x0 + 220))
            o.append('<text x="%g" y="128" class="fg fg-s" text-anchor="middle">한 덩어리</text>'
                     % (x0 + 220))
            o.append('<text x="%g" y="188" class="fg fg-s" text-anchor="middle">'
                     '남이 읽는 동안 내 차례가 밀린다</text>' % (x0 + 144))
        else:
            o.append('<text x="%g" y="188" class="fg fg-s" text-anchor="middle">'
                     '길이 따로라 기다릴 일이 없다</text>' % (x0 + 144))
    o.append('<text x="320" y="238" class="fg fg-s" text-anchor="middle">'
             '가속기를 셋 그렸지만 그 수는 발표에 없다. 「가속기마다」라는 말만 있다</text>')
    o.append('</svg>')
    return ''.join(o)


CRITERIA = _criteria()
PARETO = _pareto()
DOMAIN = _domain()
NUMA = _numa()
