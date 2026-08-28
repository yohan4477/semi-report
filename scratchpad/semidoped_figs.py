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
    """칩을 고르는 잣대가 어디로 옮겼나.

    값을 그리지 않는다. 원문에 든 것은 「무엇을 잣대로 골랐나」뿐이라 막대도 눈금도
    쓸 수 없다. 상자와 화살표로만 어느 쪽을 골랐는지 보인다.

    상자 사이 띠를 32픽셀로 벌려 글자를 그 안에 앉힌다. 앞 판은 띠가 12픽셀뿐이라
    글자가 아래 상자 테두리에 깔렸다 — check_fig 가 잡았다.
    """
    W = 640
    Y1, GAP, BH = 44, 32, 46
    y2 = Y1 + BH + GAP
    y3 = y2 + BH + 14
    H = y3 + 40 + 12
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="칩을 고르는 잣대가 어디로 옮겼나">' % (W, H)]
    o.append('<text x="20" y="24" class="fg">칩을 파는 회사는</text>')
    o.append('<text x="360" y="24" class="fg">칩을 쓰는 오픈AI 는</text>')
    o.append(_box(20, Y1, 250, BH, '총소유비용을 본다', '칩을 사서 굴리는 데 드는 돈'))
    o.append(_box(360, Y1, 250, BH, '① 엔드투엔드 지연',
                  '질문을 넣고 마지막 글자가 나올 때까지', hi=True))
    o.append(_box(360, y2, 250, BH, '② 요청당 전기에너지',
                  '한 번 답하는 데 쓰는 전기', hi=True))
    mid = Y1 + BH + GAP / 2.0
    o.append('<path d="M485 %g L485 %g" class="fg-d"/>' % (Y1 + BH + 3, mid - 9))
    o.append('<path d="M485 %g L485 %g" class="fg-d"/>' % (mid + 5, y2 - 3))
    o.append('<text x="497" y="%g" class="fg fg-s">둘은 같이 못 낮춘다</text>' % (mid + 4))
    o.append(_box(360, y3, 250, 40, '그래서 수치 하나로 못 적는다',
                  '잘한 지점을 이은 곡선으로 낸다'))
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


def _domain():
    """칩 몇 개가 한 덩어리로 도나 — 묶는 단위가 두 단계다.

    칩을 128개 그리지 않는다. 개수를 그리면 그 개수가 주장이 된다. 묶음 둘과 그 사이를
    잇는 속도만 남긴다.
    """
    W, H = 640, 226
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" '
         'aria-label="칩을 묶는 두 단계">' % (W, H)]
    o.append('<rect x="16" y="16" width="608" height="194" rx="10" class="fg-b"/>')
    o.append('<text x="32" y="38" class="fg">큰 묶음 — 칩 최대 2,048개</text>')
    o.append('<text x="32" y="56" class="fg fg-s">칩 하나가 초당 200기가비트로 붙는다</text>')
    for i in range(4):
        x = 36 + i * 146
        o.append('<rect x="%g" y="74" width="130" height="62" rx="8" class="fg-b" '
                 'style="stroke:var(--accent);stroke-width:2"/>' % x)
        o.append('<text x="%g" y="100" class="fg" text-anchor="middle">작은 묶음</text>'
                 % (x + 65))
        o.append('<text x="%g" y="117" class="fg fg-s" text-anchor="middle">'
                 '칩 128개</text>' % (x + 65))
    o.append('<text x="320" y="158" class="fg fg-s" text-anchor="middle">'
             '작은 묶음 안에서는 칩 하나가 초당 600기가비트로 붙는다</text>')
    o.append('<text x="320" y="178" class="fg fg-s" text-anchor="middle">'
             '여기 그린 상자 넷은 그림일 뿐 개수를 뜻하지 않는다</text>')
    o.append('<text x="320" y="198" class="fg fg-s" text-anchor="middle">'
             '칩 128개가 한 랙이면 2,048개는 약 16랙 — 진행자가 나눠 본 값이다</text>')
    o.append('</svg>')
    return ''.join(o)


CRITERIA = _criteria()
DOMAIN = _domain()
