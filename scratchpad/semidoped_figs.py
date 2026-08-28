# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해.

  ① 순서 도해   곱셈이 덧셈이 되고 되돌아오는 자리   (텐서다인 편)
  ② 구조 도해   쿼터랙 하나가 담는 것                (텐서다인 편)

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. 도형 개수도 값이다 → ②의 칸 넷은 원문의
    "we can put four of them in a rack"에서만 온다. 칩 72개는 아이콘으로 세지 않고
    글자로만 적는다.
  - 판 위에 글자를 얹지 않는다. 판단은 판 아래 캡션이 말한다.
  - 배치는 scratchpad/check_fig.py 가 본다.
"""

# ── ① 곱셈이 덧셈이 되고, 되돌아온다 ────────────────────────────────────
# 값은 전사본에 있는 관계식뿐이다. 면적 비율을 상자 폭으로 그리지 않는다 —
# 원문에 "a lot more area"라는 말만 있고 배수가 없다.
_STEPS = [
    (10,  126, '곱셈 A × B',    '면적·전력이 크다'),
    (160, 126, '로그로 바꾼다',  'log A, log B'),
    (310, 126, '덧셈이 된다',    'log A + log B'),
    (460, 130, '선형으로 되돌린다', '여기서 잃으면 헛일'),
]


def fig_log():
    h = ['<svg viewBox="0 0 600 250" role="img" aria-label="곱셈을 로그로 바꿔 덧셈으로 '
         '만들고 다시 선형으로 되돌리는 네 단계">']
    for x, w, head, sub in _STEPS:
        cls = 'good-box' if head.startswith('선형') else 'mid-box'
        h.append('<rect x="%d" y="64" width="%d" height="56" rx="9" class="%s"/>'
                 % (x, w, cls))
        h.append('<text x="%d" y="90" class="t-step" text-anchor="middle">%s</text>'
                 % (x + w // 2, head))
        h.append('<text x="%d" y="110" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + w // 2, sub))
    for x0, x1 in ((136, 160), (286, 310), (436, 460)):
        h.append('<line class="flow" x1="%d" y1="92" x2="%d" y2="92"/>' % (x0, x1))
    h.append('<line class="flow" x1="525" y1="122" x2="525" y2="170"/>')
    h.append('<rect x="110" y="170" width="380" height="52" rx="9" class="bad-box"/>')
    h.append('<text x="300" y="194" class="t-msg" text-anchor="middle">'
             '룩업 테이블·테일러 급수로 복원하면</text>')
    h.append('<text x="300" y="212" class="t-msg" text-anchor="middle">'
             '앞에서 번 면적·전력을 그대로 잃는다</text>')
    h.append('</svg>')
    return ''.join(h)


LOG_MATH = fig_log()


# ── ② 쿼터랙 하나가 담는 것 ─────────────────────────────────────────────
# 칸 넷은 "we can put four of them in a rack"에서 온다. 칩 72개는 세지 않고 적는다.
def fig_rack():
    h = ['<svg viewBox="0 0 600 320" role="img" aria-label="풀랙 하나와 쿼터랙 넷으로 '
         '나뉜 랙을 나란히 둔 그림">']
    h.append('<text x="155" y="44" class="t-head" text-anchor="middle">블랙웰 GB300</text>')
    h.append('<rect x="90" y="60" width="130" height="200" rx="8" class="mid-box"/>')
    h.append('<text x="155" y="282" class="t-val" text-anchor="middle">풀랙 150kW</text>')

    h.append('<text x="445" y="44" class="t-head" text-anchor="middle">텐서다인</text>')
    h.append('<rect x="380" y="60" width="130" height="200" rx="8" class="mid-box"/>')
    for y in (110, 160, 210):
        h.append('<line class="thin" x1="380" y1="%d" x2="510" y2="%d"/>' % (y, y))
    h.append('<rect x="380" y="210" width="130" height="50" rx="6" class="good-box"/>')
    h.append('<text x="522" y="240" class="t-sub">쿼터랙</text>')
    h.append('<text x="445" y="282" class="t-val" text-anchor="middle">'
             '13U · 72칩 · 30kW</text>')
    h.append('<text x="445" y="304" class="t-sub" text-anchor="middle">'
             '넷 쌓으면 120kW</text>')
    h.append('</svg>')
    return ''.join(h)


RACK = fig_rack()


FIG_CSS = """
  .uc-fig text.t-head { font-size:11.5px; font-weight:800; fill:var(--ink-3);
    letter-spacing:.04em; }
  .uc-fig text.t-step { font-size:13px; font-weight:700; fill:var(--ink); }
  .uc-fig text.t-msg  { font-size:12.5px; fill:var(--ink-2); }
  .uc-fig text.t-sub  { font-size:11.5px; fill:var(--ink-3); }
  .uc-fig text.t-val  { font-size:14px; font-weight:800; fill:var(--ink); }
  .uc-fig .thin { stroke:var(--line); stroke-width:1; }
  .uc-fig .good-box { fill:var(--fig-good-bg,rgba(47,143,107,.12));
    stroke:var(--fig-good,#2f8f6b); stroke-width:1.4; }
  .uc-fig .mid-box  { fill:rgba(127,127,127,.10); stroke:var(--line); stroke-width:1.2; }
  .uc-fig .bad-box  { fill:var(--fig-bad-bg,rgba(194,80,74,.12));
    stroke:var(--fig-bad,#c2504a); stroke-width:1.4; }
"""

ALL = [('곱셈을 덧셈으로 바꾸고 되돌아오는 자리', LOG_MATH),
       ('쿼터랙 하나가 무엇을 담나', RACK)]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, svg in ALL:
        print(name, '->', check_fig.hits(svg) or 'FAIL 0건')
