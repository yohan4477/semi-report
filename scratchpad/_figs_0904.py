# -*- coding: utf-8 -*-
"""미주사 08-28·08-30·08-31 편 도해 셋.

  ① 공정 사슬   태양광 셀을 사 오던 자리를 공장 하나로 끌어오면 무엇이 바뀌나 (테슬라 크리스탈 선)
  ② 조건 격자   워시가 금리를 올려도 이상하지 않게 만드는 조건 넷            (잭슨홀)
  ③ 구성 기둥   콜을 얼마나 씌우나 — QQQ·QYLG·QYLD                          (커버드콜)

규칙(insight-figure):
  - 원문에 없는 값은 안 그린다. ①은 공장 규모를 칸 크기로 안 그린다(101억 달러는 글자로만).
    ③은 성과를 그리지 않는다 — 원문에 세 상품의 수익률 비교 수치가 없다.
  - 판 위에 판단을 얹지 않는다. 판단은 캡션이 말한다.
  - 붓과 CSS는 _figs_0825의 것을 그대로 쓴다.
"""

# ── ① 사 오던 셀을 직접 만들면 무엇이 달라지나 ────────────────────────────
_CHAIN = [
    (24, '폴리실리콘', ('태양광의',), 'mid-box'),
    (154, '잉곳 · 웨이퍼', ('덩어리를',), 'mid-box'),
    (284, '셀', ('빛을 전기로',), 'bad-box'),
    (414, '모듈 조립', ('패널로',), 'good-box'),
]


def fig_crystal_sun():
    h = ['<svg viewBox="0 0 580 214" role="img" aria-label="폴리실리콘부터 모듈까지의 태양광 '
         '공정에서 테슬라가 지금 어디를 하고 크리스탈 선이 어디를 덮으려는지">']
    for x, name, sub, kind in _CHAIN:
        h.append('<rect x="%d" y="46" width="112" height="58" rx="9" class="%s"/>' % (x, kind))
        h.append('<text x="%d" y="72" class="t-step" text-anchor="middle">%s</text>' % (x + 56, name))
        h.append('<text x="%d" y="90" class="t-sub" text-anchor="middle">%s</text>' % (x + 56, sub[0]))
        if x != _CHAIN[-1][0]:
            h.append('<line class="flow" x1="%d" y1="75" x2="%d" y2="75"/>' % (x + 116, x + 150))
    h.append('<text x="24" y="30" class="t-head">지금 — 셀은 사 온다</text>')
    h.append('<text x="284" y="126" class="t-msg" text-anchor="middle">중국이 가장 싸게 만든다</text>')
    h.append('<text x="414" y="126" class="t-msg">버팔로에서 조립</text>')
    h.append('<text x="24" y="158" class="t-head">크리스탈 선</text>')
    h.append('<text x="176" y="158" class="t-msg">네 칸 전부를 텍사스 한 공장에 넣겠다는 계획</text>')
    h.append('<text x="24" y="182" class="t-head">드는 돈 · 일정</text>')
    h.append('<text x="176" y="182" class="t-msg">최대 101억 달러, 2026년 착공 2028년 완공, 첫 패널 2029년</text>')
    h.append('<text x="24" y="206" class="t-head">아직 아닌 것</text>')
    h.append('<text x="176" y="206" class="t-msg">승인된 공장이 아니다. 후보지를 여러 주에서 검토 중이다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_CRYSTAL = (
    3, '사 오던 셀을 직접 만들면 어디가 달라지나',
    fig_crystal_sun(),
    '테슬라 배터리 사업은 셀을 중국과 동남아에서 사 와 조립하고 소프트웨어로 엮어 돈을 번다. '
    '태양광에서 가장 싼 셀을 만드는 곳도 중국인데, 크리스탈 선은 그 반대로 <b>폴리실리콘부터 '
    '모듈까지 미국 한 공장에 넣겠다</b>는 계획이다. 필자는 이 어긋남을 순수한 사업 논리로는 '
    '설명하기 어렵다고 보고, 연방 세액공제와 주 정부 감면 또는 자기가 쓸 부품이라는 두 가지로만 '
    '말이 된다고 정리한다.')


# ── ② 금리를 올려도 이상하지 않은 논리 ────────────────────────────────────
_COND = [
    (24, '경기', ('기업투자 강함',)),
    (164, '고용', ('완전고용에 가깝다',)),
    (304, '금융여건', ('충분히 빡빡하지 않다',)),
    (444, '물가', ('PCE 3%대 후반',)),
]


def fig_warsh():
    h = ['<svg viewBox="0 0 580 226" role="img" aria-label="워시가 든 조건 넷과 '
         '그 조건이 모여 만드는 결론">']
    for x, name, sub in _COND:
        kind = 'bad-box' if name == '물가' else 'good-box'
        h.append('<rect x="%d" y="40" width="112" height="56" rx="9" class="%s"/>' % (x, kind))
        h.append('<text x="%d" y="64" class="t-step" text-anchor="middle">%s</text>' % (x + 56, name))
        h.append('<text x="%d" y="82" class="t-sub" text-anchor="middle">%s</text>' % (x + 56, sub[0]))
    h.append('<text x="24" y="26" class="t-head">워시가 본 것</text>')
    h.append('<line class="flow" x1="290" y1="100" x2="290" y2="128"/>')
    h.append('<rect x="24" y="132" width="532" height="42" rx="9" class="mid-box"/>')
    h.append('<text x="290" y="158" class="t-step" text-anchor="middle">'
             '내릴 이유가 없고, 올려도 이상하지 않은 조건이 갖춰졌다</text>')
    h.append('<text x="24" y="196" class="t-head">시장이 매긴 값</text>')
    h.append('<text x="176" y="196" class="t-msg">9월 금리 인상 확률 57%, 2년물 금리가 가장 크게 뛰었다</text>')
    h.append('<text x="24" y="218" class="t-head">2% 목표</text>')
    h.append('<text x="176" y="218" class="t-msg">「대충 그 근처」가 아니라 확고하고 고정된 목표라고 못박았다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_WARSH = (
    2, '금리를 올려도 이상하지 않은 조건 넷',
    fig_warsh(),
    '워시는 금리를 올리겠다고 말하지 않았다. 대신 경기·고용·금융여건이 다 멀쩡한데 '
    '물가만 목표에서 멀다는 조건을 하나씩 세웠다. 넷이 모이면 결론은 하나로 좁혀진다 — '
    '<b>내릴 이유가 없다.</b> 시장이 9월 인상 확률을 57%까지 올린 것도, 2년물 금리가 '
    '10년물·30년물보다 크게 뛴 것도 이 논리를 읽은 결과다.')


# ── ③ 콜을 얼마나 씌우나 ─────────────────────────────────────────────────
# 기둥 하나가 보유한 나스닥100 전부다. 색을 채운 만큼이 콜을 씌운 몫이고,
# 비어 있는 만큼이 상승을 그대로 가져가는 몫이다. 성과는 그리지 않는다.
_COVER = [
    (60, 'QQQ', 0, ('상승을 전부 가져간다', '옵션 프리미엄은 없다')),
    (240, 'QYLG', 50, ('절반은 프리미엄', '절반은 상승 따라감')),
    (420, 'QYLD', 100, ('프리미엄이 가장 크고', '상승에 천장이 생긴다')),
]


def fig_covered():
    h = ['<svg viewBox="0 0 580 256" role="img" aria-label="세 상품이 보유 포트폴리오의 '
         '몇 퍼센트에 콜옵션을 씌우는지">']
    top, height = 64, 108
    for x, name, pct, sub in _COVER:
        h.append('<rect x="%d" y="%d" width="100" height="%d" rx="7" class="mid-box"/>'
                 % (x, top, height))
        if pct:
            fh = int(height * pct / 100.0)
            h.append('<rect x="%d" y="%d" width="100" height="%d" rx="7" class="bad-box"/>'
                     % (x, top + height - fh, fh))
        h.append('<text x="%d" y="%d" class="t-step" text-anchor="middle">%s</text>'
                 % (x + 50, top - 20, name))
        h.append('<text x="%d" y="%d" class="t-val" text-anchor="middle">%d%%</text>'
                 % (x + 50, top + height + 24, pct))
        for i, line in enumerate(sub):
            h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                     % (x + 50, top + height + 44 + i * 16, line))
    h.append('<text x="24" y="22" class="t-head">보유한 나스닥100 가운데 콜을 씌운 몫</text>')
    h.append('<text x="24" y="248" class="t-msg">'
             '커버드콜이 지는 자리는 하락장이 아니라 급등장이다 — 받은 프리미엄보다 포기한 상승분이 커질 때다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_COVERED = (
    3, '콜을 얼마나 씌우나 — 같은 나스닥100, 다른 비중',
    fig_covered(),
    '세 상품 모두 나스닥100을 그대로 들고 있다. 다른 것은 <b>그 가운데 몇 퍼센트에 '
    '콜옵션을 파느냐</b>뿐이다. QYLG는 종목을 가려서 콜을 파는 상품이 아니라 전체에 '
    '일괄로 절반만 씌운다. 필자는 AI가 밑에서 받치고 장기금리가 위에서 누르는 지금 국면에서 '
    '이 어중간함이 오히려 맞는다고 본다.')


ALL = [FIG_CRYSTAL, FIG_WARSH, FIG_COVERED]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
