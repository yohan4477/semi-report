# -*- coding: utf-8 -*-
"""미주사 08-24·08-26 편 도해 둘.

  ① 구조 설명   폐기 서버의 헌 D램이 새 서버에 붙는 길   (메타 비스타라 편)
  ② 대비 격자   같은 분기에 두 돈이 갈린 자리와 겹친 자리 (골드만삭스 수급 편)

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. ①은 768GB·256GB를 칸 크기로 안 그린다 —
    크기가 값으로 읽히면 10배 느린 DDR4가 3분의 1만큼 느린 것처럼 보인다.
    ②는 종목 아이콘을 세지 않는다. 원문이 「12개」라고 적고 이름은 11개만 대서,
    개수를 그리면 어느 쪽이 맞는지를 그림이 정해 버린다.
  - 판 위에 글자를 얹지 않는다. 판단은 캡션이 말한다.
  - 붓과 CSS는 _figs_0825의 것을 그대로 쓴다(생성기가 그 CSS를 이미 싣는다).
"""

# ── ① 헌 D램이 새 서버에 붙는 길 ──────────────────────────────────────────
# 값은 [260826] 요약본에 있는 것만 쓴다. 칸 크기는 전부 같게 둔다.
_STEPS = [
    (24,  '폐기 서버', ('본체는 3~5년', '쓰고 버린다'), 'mid-box'),
    (168, '남는 헌 DDR4', ('메모리는', '7~10년 버틴다'), 'good-box'),
    (312, '비스타라(CXL)', ('새 서버가', '알아듣게 통역'), 'good-box'),
    (456, '새 서버', ('DDR5 768GB에', 'DDR4 256GB를 더'), 'good-box'),
]


def fig_vistara():
    h = ['<svg viewBox="0 0 580 204" role="img" aria-label="폐기 서버에서 나온 헌 DDR4가 '
         '비스타라를 거쳐 새 서버에 붙는 길">']
    for x, name, sub, kind in _STEPS:
        h.append('<rect class="%s" x="%d" y="34" width="100" height="66" rx="9"/>' % (kind, x))
        h.append('<text x="%d" y="58" class="t-step" text-anchor="middle">%s</text>' % (x + 50, name))
        for i, line in enumerate(sub):
            h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                     % (x + 50, 76 + i * 16, line))
        if x != _STEPS[-1][0]:
            h.append('<line class="flow" x1="%d" y1="67" x2="%d" y2="67"/>' % (x + 104, x + 140))
    h.append('<text x="24" y="22" class="t-head">버리는 쪽</text>')
    h.append('<text x="456" y="22" class="t-head">쓰는 쪽</text>')
    h.append('<text x="24" y="136" class="t-head">한 대에 담기는 양</text>')
    h.append('<text x="176" y="136" class="t-val">1TB</text>')
    h.append('<text x="236" y="136" class="t-msg">둘을 합쳐서</text>')
    h.append('<text x="24" y="164" class="t-head">DDR4가 느린 정도</text>')
    h.append('<text x="176" y="164" class="t-msg">대역폭 10배 낮고 반응은 60% 느리다</text>')
    h.append('<text x="24" y="192" class="t-head">그래서 나눈 것</text>')
    h.append('<text x="176" y="192" class="t-msg">자주 쓰는 데이터는 DDR5, 어쩌다 쓰는 것은 DDR4</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_VISTARA = (
    3, '버릴 서버에서 나온 D램이 새 서버에 붙는 길',
    fig_vistara(),
    '메타가 값을 이미 치른 물건은 왼쪽 끝의 헌 DDR4다. 새로 사는 것이 아니라 '
    '<b>버리는 서버에서 뽑아 되꽂는다.</b> 그래서 새 메모리 값이 오를수록 이 길의 값어치가 커진다. '
    '메타는 이 방식으로 특정 AI 작업에 필요한 서버 대수를 최대 25% 줄였고 어떤 작업에서는 처리 '
    '지연을 29% 낮췄다고 밝혔다 — 메타 측 발표이고 제3자 검증 수치는 아니다.')


# ── ② 두 돈이 갈린 자리와 겹친 자리 ──────────────────────────────────────
# 칸 안에는 방향만 쓴다. 종목 이름을 다 넣으면 판이 글자로 덮인다.
_COLS = [(150, '빅테크'), (290, '반도체·메모리'), (430, '전력·인프라 / 금융')]
_ROWS = [
    (56, '헤지펀드', [('산다', 'good-box'), ('판다', 'bad-box'), ('산다', 'good-box')]),
    (124, '뮤추얼펀드', [('제자리', 'mid-box'), ('산다', 'good-box'), ('산다', 'good-box')]),
]


def fig_flows():
    h = ['<svg viewBox="0 0 580 234" role="img" aria-label="헤지펀드와 뮤추얼펀드가 2026년 '
         '2분기에 빅테크·반도체·전력과 금융에서 각각 어느 방향으로 움직였나">']
    for x, name in _COLS:
        h.append('<text x="%d" y="34" class="t-head" text-anchor="middle">%s</text>' % (x + 55, name))
    for y, who, cells in _ROWS:
        h.append('<text x="20" y="%d" class="t-step">%s</text>' % (y + 34, who))
        for (x, _), (label, kind) in zip(_COLS, cells):
            h.append('<rect class="%s" x="%d" y="%d" width="110" height="48" rx="9"/>' % (kind, x, y))
            h.append('<text x="%d" y="%d" class="t-step" text-anchor="middle">%s</text>'
                     % (x + 55, y + 30, label))
    h.append('<text x="20" y="204" class="t-head">겹친 자리</text>')
    h.append('<text x="150" y="204" class="t-msg">전력·발전, 데이터센터·전력장비, 부품, 금융</text>')
    h.append('<text x="20" y="228" class="t-head">헤지펀드 금융 비중</text>')
    h.append('<text x="150" y="228" class="t-msg">2분기에 300bp 넘게 늘렸다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_FLOWS = (
    2, '두 돈이 갈린 자리와 겹친 자리',
    fig_flows(),
    '가운데 칸에서 방향이 정확히 반대다. <b>헤지펀드가 판 반도체·메모리를 뮤추얼펀드가 받았다.</b> '
    '오른쪽 칸은 둘 다 같은 방향이고, 골드만삭스가 따로 짚은 AI 인프라 종목 12개와 금융 넷이 여기 든다. '
    '빅테크 칸의 헤지펀드는 종목 안에서 갈아탔다 — 마이크로소프트·아마존을 사고 알파벳·메타·엔비디아·'
    '브로드컴을 줄였다. 2026년 2분기 말 기준이라 글이 나온 때보다 한 달 앞선 자리다.')


ALL = [FIG_VISTARA, FIG_FLOWS]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
