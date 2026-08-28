# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해 — 인라인 SVG.

규칙 하나만 지키면 나머지는 따라온다. **원문에 없는 값을 그리지 않는다.** 막대 길이도
아이콘 개수도 수치로 읽히므로, 원문에 그 수가 없으면 길이를 쓰지 않고 상태 둘로 바꾼다.
좌표는 손으로 찍지 않고 아래 셈에서 나온다.

배치는 `scratchpad/check_fig.py` 가 본다.
"""

FIG_CSS = '''
.fg { font: 600 12px/1.35 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  fill: var(--ink-2); }
.fg-s { font-weight: 400; font-size: 11px; fill: var(--ink-3); }
.fg-b { fill: var(--surface); stroke: var(--line); stroke-width: 1.2; }
.fg-hi { fill: none; stroke: var(--accent); stroke-width: 2; }
.fg-l { stroke: var(--line); stroke-width: 1.2; fill: none; }
.fg-d { stroke: var(--ink-3); stroke-width: 1.2; fill: none; stroke-dasharray: 3 3; }
'''


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
    """설계 기준 — 운영자의 셈과 사용자 경험을 좌우로 놓는다.

    값을 그리지 않는다. 원문에 든 것은 「무엇을 기준으로 골랐나」뿐이라 막대도 눈금도
    쓸 수 없다. 상자와 화살표로만 어느 쪽을 골랐는지를 보인다.
    """
    W, H = 640, 200
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="설계 기준 두 갈래">' % (W, H)]
    o.append('<text x="20" y="22" class="fg">상업 실리콘 벤더</text>')
    o.append('<text x="360" y="22" class="fg">모델랩 오픈AI</text>')
    o.append(_box(20, 36, 250, 44, '총소유비용', '운영자가 치르는 값'))
    o.append(_box(360, 36, 250, 44, '종단간 지연', '마지막 토큰까지 걸리는 시간', hi=True))
    o.append(_box(360, 92, 250, 44, '요청당 에너지', '한 번 답하는 데 드는 전력', hi=True))
    # 두 축이 서로 밀어낸다 → 점 하나가 아니라 곡선
    o.append('<path d="M485 80 L485 92" class="fg-d"/>')
    o.append('<text x="497" y="90" class="fg fg-s">서로 밀어낸다</text>')
    o.append(_box(360, 148, 250, 36, '파레토 곡선으로만 낸다'))
    o.append('<path d="M270 58 L352 58" class="fg-l" marker-end="url(#fgA)"/>')
    o.append('<defs><marker id="fgA" markerWidth="8" markerHeight="8" refX="7" refY="4" '
             'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--ink-3)"/></marker></defs>')
    o.append('<text x="20" y="106" class="fg fg-s">기준이 운영자</text>')
    o.append('<text x="20" y="122" class="fg fg-s">셈에서 사용자</text>')
    o.append('<text x="20" y="138" class="fg fg-s">경험으로 옮겼다</text>')
    o.append('</svg>')
    return ''.join(o)


def _domain():
    """스케일업 도메인 두 겹 — 128칩과 최대 2,048칩.

    칩을 128개 그리지 않는다. 개수를 그리면 그 개수가 주장이 된다. 겹 둘과 그 사이를
    잇는 속도만 남긴다.
    """
    W, H = 640, 210
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="스케일업 도메인 두 겹">' % (W, H)]
    # 바깥 겹
    o.append('<rect x="16" y="16" width="608" height="178" rx="10" class="fg-b"/>')
    o.append('<text x="32" y="38" class="fg">바깥 겹 — 최대 2,048칩</text>')
    o.append('<text x="32" y="55" class="fg fg-s">칩당 초당 200Gb · ESUN</text>')
    # 안쪽 겹 넷 — 개수가 아니라 「여럿이 모인다」를 뜻한다
    for i in range(4):
        x = 36 + i * 146
        o.append('<rect x="%g" y="72" width="130" height="60" rx="8" class="fg-b" '
                 'style="stroke:var(--accent);stroke-width:2"/>' % x)
        o.append('<text x="%g" y="98" class="fg" text-anchor="middle">128칩</text>'
                 % (x + 65))
        o.append('<text x="%g" y="115" class="fg fg-s" text-anchor="middle">'
                 '칩당 초당 600Gb</text>' % (x + 65))
    o.append('<text x="320" y="152" class="fg fg-s" text-anchor="middle">'
             '안쪽 겹이 여럿 모여 바깥 겹이 된다 — 그림의 상자 넷은 개수가 아니다</text>')
    o.append('<text x="320" y="174" class="fg fg-s" text-anchor="middle">'
             '스위치는 브로드컴 Tomahawk 6 · 128칩이 한 랙이면 2,048칩은 약 열여섯 랙'
             '(진행자 어림)</text>')
    o.append('</svg>')
    return ''.join(o)


CRITERIA = _criteria()
DOMAIN = _domain()
