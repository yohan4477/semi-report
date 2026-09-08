# -*- coding: utf-8 -*-
"""부동산 카드 도해 둘 — 2026-09-07 추가분(훨훨 「1억 5천으로 아파트를 산다」 편).

  ① 흐름 차단   잔금을 메우던 두 길이 다 막혔다 (청약)
  ② 가격대 띠   많이 오른 구간과 아직 안 오른 구간이 갈린다

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. 띠의 양 끝(3억 8천·4억·5억·6억·7~8억·10억)은
    전부 자막에 나온 값이고, 자막이 말하지 않은 6~7억·8~10억 구간은 비워 뒀다.
    비운 자리가 곧 「원문이 말하지 않았다」는 뜻이다.
  - 가격대 좌표는 손으로 찍지 않는다. 억 단위 값을 받는 x() 하나만 쓴다.
  - 판단은 캡션이 말한다.

CSS는 _figs_0825.FIG_CSS(t-head·t-step·t-sub·t-val·good-box·mid-box·bad-box)와
card_lib 기본(.body·.flow·.lead-line·.bad·.good)을 쓴다.
"""

# ── ① 청약 — 잔금을 메우던 두 길이 막혔다 ────────────────────────────────


def fig_balance():
    h = ['<svg viewBox="0 0 560 300" role="img" aria-label="분양가 15억 아파트의 잔금 13억을 '
         '메우던 두 길인 잔금 대출과 전세보증금이 각각 대출 한도와 실거주 의무로 막힌 그림">']
    h.append('<text x="26" y="22" class="t-head">분양가 15억 · 남는 잔금 13억</text>')
    # 위 상자 — 메워야 할 것
    h.append('<rect class="body" x="150" y="34" width="260" height="40" rx="8"/>')
    h.append('<text x="280" y="59" class="t-step" text-anchor="middle">잔금 13억을 무엇으로 메우나</text>')
    # 두 갈래
    for x0, x1 in ((280, 150), (280, 410)):
        h.append('<path class="flow" d="M%d 76 L%d 94 L%d 112"/>' % (x0, x1, x1))
    box = ((30, '잔금 대출', '집값의 40%까지', '분양가가 15억을 넘으면 4억까지'),
           (290, '전세보증금으로 잔금', '토지거래허가구역 실거주 2년', '세입자 돈으로 맞추면 조건부 대출'))
    for x, name, l1, l2 in box:
        h.append('<rect class="bad-box" x="%d" y="118" width="240" height="76" rx="8"/>' % x)
        h.append('<text x="%d" y="140" class="t-step">%s</text>' % (x + 16, name))
        h.append('<text x="%d" y="162" class="t-sub">%s</text>' % (x + 16, l1))
        h.append('<text x="%d" y="182" class="t-sub">%s</text>' % (x + 16, l2))
    # 아래 — 예전 방식
    h.append('<rect class="body" x="30" y="212" width="500" height="70" rx="8"/>')
    h.append('<text x="46" y="236" class="t-step">예전에는 이렇게 갔다</text>')
    h.append('<text x="46" y="258" class="t-sub">'
             '계약금 10%만 있으면 중도금 60%는 대출로 3년을 버텼고,</text>')
    h.append('<text x="46" y="276" class="t-sub">'
             '잔금은 감정가의 70%까지 대출을 받거나 전세를 놓아 그 보증금으로 냈다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_BALANCE = (
    1, '청약은 잔금에서 막힌다',
    fig_balance(),
    '분양가 <b>15억</b>짜리에 당첨되면 잔금 <b>13억</b>이 남는다. 그것을 메우던 두 길이 '
    '동시에 막혔다는 것이 이 편의 출발점이다. 잔금 대출은 집값의 <b>40%</b>까지이고 분양가가 '
    '15억을 넘으면 <b>4억</b>까지다. 전세보증금으로 내는 길은 실거주 2년 의무와 조건부 대출에 '
    '걸린다. 아래 칸이 예전 방식이다 — 계약금 <b>10%</b>와 중도금 대출 <b>60%</b>로 3년을 '
    '버티고 잔금은 감정가의 <b>70%</b>까지 받던 구조가 지금은 서지 않는다.')


# ── ② 가격대 — 오른 구간과 안 오른 구간 ──────────────────────────────────
# 좌표는 억 단위 값 하나를 받는 함수만 쓴다(손으로 찍지 않는다)
_X0, _X1, _V0, _V1 = 60.0, 520.0, 3.0, 11.0


def x(v):
    return _X0 + (v - _V0) * (_X1 - _X0) / (_V1 - _V0)


# 색은 오른 정도의 세기다 — 못 오른 구간을 나쁘다고 칠하지 않는다
_BANDS = [(3.0, 6.0, 'body', '전고점을 아직 못 찍은 구간', '6억 이하'),
          (7.0, 8.0, 'mid-box', '전고점을 뚫기 시작한 구간', '7~8억'),
          (10.0, 11.0, 'good-box', '많이 오른 구간', '10억 초과')]
_TICKS = [(4.0, '4억'), (5.0, '5억'), (6.0, '6억'), (7.0, '7억'),
          (8.0, '8억'), (10.0, '10억')]


def fig_band():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="매매가 구간별로 전고점 회복 상태가 '
         '갈리는 띠. 6억 이하는 전고점을 못 찍었고 7~8억은 뚫기 시작했으며 10억 초과는 많이 올랐다">']
    h.append('<text x="26" y="22" class="t-head">값이 올랐다는 이야기는 어느 구간의 것인가</text>')
    # 띠
    for v0, v1, cls, name, val in _BANDS:
        h.append('<rect class="%s" x="%.1f" y="40" width="%.1f" height="34" rx="5"/>'
                 % (cls, x(v0), x(v1) - x(v0)))
    # 축
    h.append('<line class="grid" x1="%.1f" y1="84" x2="%.1f" y2="84"/>' % (_X0, _X1))
    for v, lab in _TICKS:
        h.append('<line class="grid" x1="%.1f" y1="84" x2="%.1f" y2="90"/>' % (x(v), x(v)))
        h.append('<text x="%.1f" y="104" class="t-sub" text-anchor="middle">%s</text>'
                 % (x(v), lab))
    # 범례 — 판 위에 얹지 않고 아래로 내린다
    for i, (v0, v1, cls, name, val) in enumerate(_BANDS):
        y = 126 + i * 24
        h.append('<rect class="%s" x="30" y="%d" width="18" height="14" rx="3"/>' % (cls, y - 11))
        h.append('<text x="56" y="%d" class="t-sub">%s — %s</text>' % (y, val, name))
    # 1억 5천이 닿는 자리
    h.append('<rect class="body" x="30" y="200" width="500" height="40" rx="8"/>')
    h.append('<text x="46" y="216" class="t-sub">'
             '1억 5천이 닿는 자리 — 비규제 갭은 매매가 3억 8천~4억,</text>')
    h.append('<text x="46" y="234" class="t-sub">'
             '생애최초 대출로 집값의 70%를 일으키면 5억대. 둘 다 왼쪽 구간 안이다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_BAND = (
    3, '오른 것은 10억 초과였다',
    fig_band(),
    '띠의 위치는 매매가 구간이다. <b>10억을 넘는 구간</b>이 많이 올랐고 <b>7~8억</b>대가 '
    '2021년 전고점을 뚫기 시작한 단계이며 <b>6억 이하</b>는 대부분 전고점을 아직 못 찍었다는 '
    '것이 훨훨의 관찰이다. 1억 5천이 닿는 <b>3억 8천~4억</b>(비규제 갭)과 <b>5억대</b>'
    '(생애최초 대출)가 모두 그 왼쪽 칸에 들어간다. 6~7억과 8~10억 구간을 비워 둔 것은 '
    '원문이 그 자리를 말하지 않아서다. 「그래서 곧 번져 나간다」는 다음 문장에는 이 편에 '
    '통계가 붙지 않는다 — 그림은 거기까지 그리지 않는다.')
