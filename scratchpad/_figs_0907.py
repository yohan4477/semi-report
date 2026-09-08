# -*- coding: utf-8 -*-
"""미주사 09-06~09-07 편 도해 둘.

  ① 좌우 대비   같은 낙폭인데 확인할 것이 몇 가지인가            (HONA vs 스페이스X)
  ② 갈라짐      같은 물가를 놓고 증명 책임이 반대로 걸린다        (워시 vs 월러)

규칙(insight-figure):
  - 원문에 없는 값은 안 그린다. ①은 주가 낙폭을 막대로 안 그린다 — 두 종목의 고점·저점은
    있지만 이 그림이 말하는 것은 값이 아니라 확인할 항목의 수다.
  - ②는 인상 확률의 시간 경로를 선으로 안 그린다. 원문에 있는 것은 세 시점의 값뿐이다.
  - 판단은 캡션이 말한다. 붓과 CSS는 _figs_0825의 것을 그대로 쓴다.
"""

# ── ① 확인해야 할 것이 몇 가지인가 ───────────────────────────────────────
_ROWS = [
    ('확인할 질문',
     ('이미 받은 주문을', '정상적으로 납품할 수 있나'),
     ('여러 미래 사업 가운데', '무엇이 크게 성공할까')),
    ('값을 재는 법',
     ('대형 항공우주 회사들과 견준다', '2028년 P/FCF 16.8배', '중앙값 대비 35% 할인'),
     ('사업 범위가 넓어', '같은 방식으로 값을 못 잡는다')),
    ('앞으로의 수급',
     ('9월 21일 S&amp;P 100 제외', '날짜가 정해진 일회성')),
]

_SUPPLY_R = ('8월에 9억 1,150만 주 해제', '12월 초까지 40%가 거래 가능해진다')


def fig_verify():
    lx, rx, lw, rw = 148, 362, 200, 194
    h = ['<svg viewBox="0 0 580 312" role="img" aria-label="허니웰 에어로스페이스와 '
         '스페이스X를 저가매수로 볼 때 확인해야 하는 항목 비교">']
    h.append('<text x="24" y="22" class="t-head">저가매수로 보려면 무엇을 확인해야 하나</text>')
    h.append('<rect x="%d" y="34" width="%d" height="34" rx="8" class="good-box"/>' % (lx, lw))
    h.append('<text x="%d" y="56" class="t-step" text-anchor="middle">허니웰 에어로스페이스</text>'
             % (lx + lw // 2))
    h.append('<rect x="%d" y="34" width="%d" height="34" rx="8" class="bad-box"/>' % (rx, rw))
    h.append('<text x="%d" y="56" class="t-step" text-anchor="middle">스페이스X</text>'
             % (rx + rw // 2))
    for i, row in enumerate(_ROWS):
        y = 84 + i * 70
        label, left = row[0], row[1]
        right = row[2] if len(row) > 2 else _SUPPLY_R
        h.append('<text x="24" y="%d" class="t-head">%s</text>' % (y + 22, label))
        h.append('<rect x="%d" y="%d" width="%d" height="58" rx="8" class="mid-box"/>' % (lx, y, lw))
        h.append('<rect x="%d" y="%d" width="%d" height="58" rx="8" class="mid-box"/>' % (rx, y, rw))
        for j, line in enumerate(left):
            h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                     % (lx + lw // 2, y + 18 + j * 16, line))
        for j, line in enumerate(right):
            h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                     % (rx + rw // 2, y + 18 + j * 16, line))
    h.append('<text x="24" y="304" class="t-msg">'
             '빠진 폭은 둘 다 비슷하다 — 다른 것은 그 값이 틀렸는지 확인하는 데 드는 품이다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_VERIFY = (
    3, '확인할 것이 몇 가지인가 — 같은 낙폭, 다른 난이도',
    fig_verify(),
    '저가매수는 값이 많이 빠진 것을 사는 일이 아니라 시장이 값을 잘못 매긴 회사를 찾는 일이다. '
    '그래서 필자가 재는 것은 낙폭이 아니라 <b>그 판단을 확인하는 데 드는 품</b>이다. '
    '허니웰 에어로스페이스는 질문이 하나로 좁혀지고 견줄 동종기업이 있고 수급 이벤트도 날짜가 '
    '박혀 있다. 스페이스X는 셋 다 열려 있다.')


# ── ② 같은 물가, 반대 방향의 증명 책임 ───────────────────────────────────
_SIDES = [
    (24, '워시 의장', 'bad-box',
     ('물가가 충분히 좋아졌다는', '증거가 있나'),
     '증거가 없으면 올릴 수 있다'),
    (316, '월러 이사', 'good-box',
     ('좋아지는 흐름이 깨졌다는', '증거가 있나'),
     '증거가 없으면 동결한다'),
]


def fig_burden():
    h = ['<svg viewBox="0 0 580 286" role="img" aria-label="같은 물가 데이터를 놓고 '
         '워시 의장과 월러 이사가 서로 반대 방향으로 증거를 요구하는 구조">']
    h.append('<text x="24" y="22" class="t-head">둘이 보는 물가는 같은 숫자다</text>')
    h.append('<rect x="140" y="34" width="300" height="46" rx="9" class="mid-box"/>')
    h.append('<text x="290" y="54" class="t-step" text-anchor="middle">2% 목표보다 높고</text>')
    h.append('<text x="290" y="72" class="t-sub" text-anchor="middle">'
             '최근 몇 달 오르는 속도는 낮아졌다</text>')
    h.append('<line class="flow" x1="200" y1="84" x2="144" y2="112"/>')
    h.append('<line class="flow" x1="380" y1="84" x2="436" y2="112"/>')
    for x, who, kind, ask, out in _SIDES:
        h.append('<rect x="%d" y="118" width="240" height="72" rx="9" class="%s"/>' % (x, kind))
        h.append('<text x="%d" y="142" class="t-step" text-anchor="middle">%s</text>' % (x + 120, who))
        for j, line in enumerate(ask):
            h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                     % (x + 120, 162 + j * 16, line))
        h.append('<text x="%d" y="210" class="t-val" text-anchor="middle">%s</text>' % (x + 120, out))
    h.append('<text x="24" y="240" class="t-head">규칙</text>')
    h.append('<text x="140" y="240" class="t-msg">'
             '다음 결정을 약속하지 않는다 — 어떤 데이터에 어떻게 반응할지만 알린다</text>')
    h.append('<text x="24" y="262" class="t-head">시장이 매긴 값</text>')
    h.append('<text x="140" y="262" class="t-msg">'
             '한때 60%를 넘겼다가 월러 발언 뒤 거의 반반, 강한 고용 뒤 다시 57%</text>')
    h.append('<text x="24" y="280" class="t-msg">'
             '남은 숫자는 8월 CPI 하나다 — 고용도 유가도 이미 확인됐다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_BURDEN = (
    3, '같은 물가, 반대로 걸린 증명 책임',
    fig_burden(),
    '워시는 동결하려면 물가가 좋아졌다는 증거를 더 내라 하고, 월러는 올리려면 흐름이 깨졌다는 '
    '증거를 내라 한다. 요구하는 방향이 반대라 <b>아무 증거도 안 나온 상태의 기본값</b>이 서로 '
    '다르다. 연준이 며칠마다 말을 바꾸는 것처럼 보이는 이유는 규칙이 흔들려서가 아니라 그 규칙에 '
    '넣는 숫자가 계속 바뀌기 때문이다.')


ALL = [FIG_VERIFY, FIG_BURDEN]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
