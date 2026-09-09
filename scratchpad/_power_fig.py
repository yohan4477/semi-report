# -*- coding: utf-8 -*-
"""보고서 전력 층의 도해 넷. 색은 회색만(확정 규칙 S2).

값은 전부 원문에 있는 것만 그린다 — 캡션이 라벨과 줄 번호를 댄다.
좌표는 _row 와 아래 헬퍼가 계산하고 손으로 찍지 않는다(insight-figure 규칙 2).

라벨 길이를 먼저 잰다. 링크드인 흐름 장에서 상자 폭을 넘긴 글자가 옆 상자로 흘러
여섯 칸이 통째로 겹쳤다(2026-09-06). 상자 폭에 안 들어가면 라벨을 줄이고 뜻은 캡션이 받는다.
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'

# `.flow` 가 부르는 marker#fig-arrow 정의는 저장소에서 epoch 장에만 있다. 없으면
# 선만 그어지고 화살촉이 빠져 「인과는 화살표로」가 조용히 안 지켜진다(2026-09-06)
_DEFS = ('<defs><marker id="fig-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         '<path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker></defs>' % INK3)


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


# ── 도해 1. 발전소에서 GPU 까지 다섯 번 낮춘다 ────────────────────────
# 사슬은 한 크기(확정 규칙). 다섯 상자가 전부 같고 다른 것은 안에 적힌 전압뿐이다.
_C = _row(5, 46, 74, 112, gap=16)
_CHAIN_CELLS = [
    ['발전소', '수백 킬로볼트'],
    ['부지 변전소', '10~30킬로볼트'],
    ['유틸리티실', '400~430볼트'],
    ['랙 전원장치', '48·12·6볼트'],
    ['전압조정모듈', '1볼트 아래'],
]
FIG_CHAIN = _svg(W, 150, '발전소에서 가속기까지 전압을 다섯 번 낮춘다', _DEFS + ''.join(
    [_lt(8, 30, '들어오는 쪽', 't-sm', True), _lt(W - 84, 30, '쓰는 쪽', 't-sm', True)]
    + [_box(x, y, w, h, lines, INK3, 1.5)
       for (x, y, w, h), lines in zip(_C, _CHAIN_CELLS)]
    + [_a(_C[i - 1][0] + _C[i - 1][2], 83, _C[i][0], 83) for i in range(1, 5)]
    + [_t(W // 2, 138, '마디마다 손실이 난다 — 800볼트 직류는 이 사슬을 줄이려는 것', 't-sm')]))


# ── 도해 2. PJM 용량 요금이 정해지는 길 ──────────────────────────────
# 인과는 화살표로(확정 규칙). 왼쪽이 값을 정하는 길, 오른쪽이 같은 기간 실물 신호다.
# 둘을 나란히 둔 것은 이 글의 배치이고 값은 각각 원문에 있다.
_PL = _row(1, 0, 44, 250)[0]
_LX, _RX = 40, 350
_PSTEP = 66
_LEFT = [['PJM 내부 예측 모델'], ['청산점을 정하는 곡선'],
         ['청산가 하루 270달러'], ['관할 안 모든 소비자']]
_RIGHT = [['선물시장 2028·2030년'], ['12~20% 상승'], ['텍사스도 11~17%'], ['실물 돈을 건 쪽']]


def _col(x, cells, accent):
    out = []
    for i, lines in enumerate(cells):
        y = 40 + i * _PSTEP
        st, sw = (INK, 2.0) if i == accent else (INK3, 1.5)
        out.append(_box(x, y, 250, 44, lines, st, sw))
        if i:
            out.append(_a(x + 125, y - (_PSTEP - 44) + 3, x + 125, y))
    return ''.join(out)


FIG_PJMPRICE = _svg(W, 40 + 4 * _PSTEP - (_PSTEP - 44) + 34,
                    'PJM 용량 요금이 정해지는 길과 같은 기간 선물시장',
                    _DEFS + ''.join([
                        _lt(_LX, 26, '값을 정하는 길', 't-lab', True),
                        _lt(_RX, 26, '같은 기간 실물 신호', 't-lab', True),
                        _col(_LX, _LEFT, 2),
                        _col(_RX, _RIGHT, 1),
                    ]) + _t(W // 2, 40 + 4 * _PSTEP - 4,
                            '왼쪽은 9.3배, 오른쪽은 12~20%', 't-sm'))


# ── 도해 3. 모델을 고쳤다면 얼마였나 ─────────────────────────────────
# 값을 견줄 때는 나란한 세로 막대, 높이는 값에 비례(확정 규칙 2026-09-04).
# 같은 경매를 실제와 대안으로 짝지어 놓는다 — 견줄 때는 같은 꼴.
_GMAX, _GH, _GBASE = 340.0, 180, 224
_GBARS = [
    ('2025/26', '실제', 270, True),
    ('2025/26', '모델 고쳤다면', 135, False),
    ('2026/27', '실제', 329, True),
    ('2026/27', '모델 고쳤다면', 230, False),
]
_GW, _GG, _GPAIR = 76, 18, 46
_GX0 = (W - (4 * _GW + 2 * _GG + _GPAIR)) // 2


def _gbar(i, when, what, v, actual):
    x = _GX0 + i * (_GW + _GG) + (_GPAIR - _GG if i >= 2 else 0)
    h = int(_GH * v / _GMAX)
    y = _GBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _GW, h, 'var(--sunk)' if actual else 'none',
                                  INK if actual else INK3),
        _t(x + _GW // 2, y - 8, '%d달러' % v, 't-lab'),
        _t(x + _GW // 2, _GBASE + 18, what, 't-sm'),
        _t(x + _GW // 2, _GBASE + 34, when, 't-sm'),
    ])


FIG_GAP = _svg(W, 292, '같은 경매를 실제 청산가와 모델을 고쳤을 때로 견준다',
               ''.join([
                   '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
                   % (_GX0 - 16, _GBASE, W - _GX0 + 16, _GBASE, INK3),
                   _lt(_GX0 - 16, 20, '메가와트·하루당 청산가', 't-sm', True),
               ] + [_gbar(i, *b) for i, b in enumerate(_GBARS)]
                   + [_t(W // 2, 284,
                         '채운 막대가 실제로 낸 값, 빈 막대가 저자의 역산', 't-sm')]))


# ── 도해 4. 같은 물음에 답이 셋 ──────────────────────────────────────
# 견줄 때는 같은 꼴(확정 규칙). 세 판이 같은 크기이고 줄도 같은 세 줄이다.
#
# 처음에 _box 에 이름을 넘겼더니 이름이 상자 세로 가운데에 놓여, 따로 그린 줄과
# 겹쳤다(2026-09-07). _box 는 줄을 가운데 정렬하므로 머리와 본문을 같이 못 둔다 —
# 사각형을 직접 그리고 글자 자리를 손으로 잡는다. 행 이름도 판 안으로 파고들어
# 왼쪽에 라벨 열을 따로 뗐다.
_TLAB, _TGAP = 84, 14
_TW = (W - _TLAB - _TGAP * 2 - 10) // 3
_TH, _TY = 152, 44
# 라벨 열이 84px 이라 「값이 어떻게 정해지나」가 넘쳐 첫 판 글자와 겹쳤다(2026-09-07).
# 행 이름은 여기서 줄이고 온전한 말은 캡션이 받는다
_TROWS = ['누가 내나', '어떻게 정하나', '청구서에']
_THREE = [
    ('PJM', ['요금 납부자', '예측 모델이 정한다', '월 25~30달러']),
    ('ERCOT', ['실제 공급한 쪽', '실시간 값이 정한다', '용량 요금 없음']),
    ('한국·대만', ['국영 전력회사', '정부가 눌러 둔다', '적자로 숨는다']),
]


def _panel(i, name, rows):
    x = _TLAB + i * (_TW + _TGAP)
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
           'stroke-width="1.5"/>' % (x, _TY, _TW, _TH, INK3),
           _t(x + _TW // 2, _TY + 26, name, 't-lab')]
    for k, s in enumerate(rows):
        out.append(_t(x + _TW // 2, _TY + 64 + k * 34, s, 't-sm'))
    return ''.join(out)


FIG_THREE = _svg(W, 250, '같은 물음에 세 시장이 다르게 답한다',
                 ''.join([_lt(4, _TY + 64 + k * 34, s, 't-sm', False)
                          for k, s in enumerate(_TROWS)])
                 + ''.join(_panel(i, n, r) for i, (n, r) in enumerate(_THREE))
                 + _t(W // 2, 240, '어느 쪽에서도 전기가 공짜인 적은 없다 — '
                                   '청구서가 누구 앞으로 가는지가 다르다', 't-sm'))


# ── 도해 5. 변환 지점이 사슬 위에서 상류로 옮겨간다 ──────────────────
# 도해 1과 같은 사슬을 같은 자리에 다시 세우고(_C 를 그대로 쓴다), 단계마다 변환이
# 어느 마디에서 일어나는지만 표시한다. 마디는 Semi Doped 가 나눈 다섯이고
# (SD-260508 L49) 자리는 뉴스레터가 밝힌 것이다(전력-260526 L136·L137·L157).
# 단계마다 변환이 몇 개 남는지는 그리지 않는다 — 원문이 센 것은 1·2단계뿐이다.
_PHY, _PHSTEP, _PHH = 142, 44, 36
_PHASE_AT = [(3, '1단계', '83.7%'), (3, '2단계', '86.5%'),
             (2, '3단계', '86.9%'), (1, '4단계', '87.4%')]


def _phrow(i, col, name, eff):
    x, _, w, _ = _C[col]
    y = _PHY + i * _PHSTEP
    last = i == len(_PHASE_AT) - 1
    # 앞 단계와 같은 마디면 그 상자 밑에서 잇고, 마디가 옮겨 갔으면 사슬에서 새로 내린다.
    # 늘 사슬에서 내리면 같은 칸에 선 앞 상자를 선이 관통한다.
    same = i and _PHASE_AT[i - 1][0] == col
    return ''.join([
        '<path d="M%d %d V%d" stroke="%s" stroke-width="1" '
        'stroke-dasharray="4 4"/>' % (x + w // 2, y - (_PHSTEP - _PHH) if same else 120,
                                      y, INK3),
        _box(x, y, w, _PHH, [name + ' ' + eff], INK if last else INK3, 1.8 if last else 1.5),
    ])


FIG_PHASE = _svg(W, _PHY + 4 * _PHSTEP + 22, '변환이 일어나는 자리가 단계마다 상류로 옮겨간다',
                 _DEFS + ''.join(
                     [_lt(8, 30, '들어오는 쪽', 't-sm', True),
                      _lt(W - 84, 30, '쓰는 쪽', 't-sm', True)]
                     + [_box(x, y, w, h, lines, INK3, 1.5)
                        for (x, y, w, h), lines in zip(_C, _CHAIN_CELLS)]
                     + [_a(_C[i - 1][0] + _C[i - 1][2], 83, _C[i][0], 83) for i in range(1, 5)]
                     + [_lt(8, 134, '변환이 일어나는 자리', 't-sm', True)]
                     + [_phrow(i, *r) for i, r in enumerate(_PHASE_AT)])
                 + _t(W // 2, _PHY + 4 * _PHSTEP + 14,
                      '자리가 왼쪽으로 갈수록 사슬이 짧아지고 효율이 오른다', 't-sm'))


# ── 도해 6. 같은 글이 절감치를 두 값으로 적는다 ──────────────────────
# 견줄 때는 나란한 세로 막대, 높이는 값에 비례(확정 규칙 2026-09-04).
# 두 값 다 원문에 있고, 원문이 이 둘을 일치한다고 적은 것이 이 그림의 요점이다.
_MMAX, _MH, _MBASE, _MW_, _MGAP = 69.0, 130, 186, 120, 110
_MBARS = [(50, '50메가와트', '엔비디아가 밝힌', '최대 5%', True),
          (69, '69메가와트', '단계별 계산 4단계', '6.9%', False)]
_MX0 = (W - (2 * _MW_ + _MGAP)) // 2


def _mbar(i, v, top, l1, l2, filled):
    x = _MX0 + i * (_MW_ + _MGAP)
    h = int(_MH * v / _MMAX)
    y = _MBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _MW_, h, 'var(--sunk)' if filled else 'none',
                                  INK3 if filled else INK),
        _t(x + _MW_ // 2, y - 8, top, 't-lab'),
        _t(x + _MW_ // 2, _MBASE + 18, l1, 't-sm'),
        _t(x + _MW_ // 2, _MBASE + 34, l2, 't-sm'),
    ])


FIG_MW = _svg(W, 254, '같은 글이 절감치를 두 값으로 적는다', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_MX0 - 16, _MBASE, W - _MX0 + 16, _MBASE, INK3),
     _lt(_MX0 - 16, 20, '1기가와트 시설에서 아끼는 전력', 't-sm', True)]
    + [_mbar(i, *b) for i, b in enumerate(_MBARS)]
    + [_t(W // 2, 246, '원문은 이 둘이 일치한다고 적는다', 't-sm')]))


# ── 도해 7. 고치자는 안이 어느 마디를 겨눴고 어디서 멈췄나 ────────────
# 도해 2의 왼쪽 판(값을 정하는 길)을 같은 좌표로 다시 깔고, 규칙을 고치는 길을
# 그 옆에 세워 두 번째 마디로 잇는다. 부결됐으므로 잇는 선은 점선이다.
_FIXY = [40, 106, 172]
_FIXCELLS = [['고치자는 안', '겨울 인증치를 반영'],
             ['태스크포스 178대 54', '77% 통과'],
             ['26일 뒤 상위 위원회', '30.7% 부결']]

FIG_FIX = _svg(W, 40 + 4 * _PSTEP - (_PSTEP - 44) + 34,
               '고치자는 안이 곡선을 겨눴다가 위원회에서 멈췄다',
               _DEFS + ''.join([
                   _lt(_LX, 26, '값을 정하는 길', 't-lab', True),
                   _lt(_RX, 26, '규칙을 고치는 길', 't-lab', True),
                   _col(_LX, _LEFT, 1),
               ] + [_box(_RX, y, 250, 44, lines, INK if i == 2 else INK3,
                         1.8 if i == 2 else 1.5)
                    for i, (y, lines) in enumerate(zip(_FIXY, _FIXCELLS))]
                   + [_a(_RX + 125, _FIXY[i] + 44, _RX + 125, _FIXY[i + 1])
                      for i in range(2)]
                   + ['<path d="M%d %d H%d" stroke="%s" stroke-width="1.4" '
                      'stroke-dasharray="5 4" marker-end="url(#fig-arrow)"/>'
                      % (_RX - 6, _FIXY[1] + 22, _LX + 250 + 6, INK3)])
               + _t(W // 2, 40 + 4 * _PSTEP - 4,
                    '곡선은 그대로 남았다 — 점선은 닿지 못한 길', 't-sm'))


# ── 도해 8. 작업시간이 현장에서 공장으로 옮겨간다 ─────────────────────
# 같은 판(공장·현장 두 마디)을 줄마다 한 번씩 그린다 — 줄마다 다른 것만 그리면
# 다른 그림 둘로 읽힌다. 값은 50메가와트 수랭 홀 기준이다(건설-260729 L444·L445).
_MW2, _MGAP2, _MLAB = 250, 16, 96
_MY, _MSTEP2, _MH2 = 52, 74, 56
_MROWS = [('관행 시공', ['공장에서 하는 일 없음'], ['현장 메가와트당 12,000시간'], '30~35개월', 1),
          ('완전 모듈러', ['기계·전기 설치를 공장에서'], ['현장 메가와트당 4,500시간'], '24~30개월', 0)]


def _mrow(i, name, left, right, dur, accent):
    y = _MY + i * _MSTEP2
    xs = [_MLAB, _MLAB + _MW2 + _MGAP2]
    cells = [left, right]
    # 기간을 줄 밑에 적었더니 다음 줄 상자 테두리에 깔렸다 — 줄 이름 밑으로 옮긴다
    out = [_lt(6, y + _MH2 // 2 - 4, name, 't-sm', True),
           _lt(6, y + _MH2 // 2 + 14, dur, 't-sm', False)]
    for k, (x, lines) in enumerate(zip(xs, cells)):
        hot = k == accent
        out.append(_box(x, y, _MW2, _MH2, lines, INK if hot else INK3,
                        1.8 if hot else 1.2))
    return ''.join(out)


FIG_MODULAR = _svg(W, _MY + 2 * _MSTEP2 + 16, '작업시간이 현장에서 공장으로 옮겨간다',
                   ''.join([_lt(_MLAB, 34, '공장', 't-lab', True),
                            _lt(_MLAB + _MW2 + _MGAP2, 34, '현장', 't-lab', True)]
                           + [_mrow(i, *r) for i, r in enumerate(_MROWS)])
                   + _t(W // 2, _MY + 2 * _MSTEP2 + 8,
                        '전기공 면허가 필요한 작업시간은 약 85% 줄어든다', 't-sm'))
