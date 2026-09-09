# -*- coding: utf-8 -*-
"""보고서 전력 층의 도해 넷. 색은 회색만(확정 규칙 S2).

값은 전부 원문에 있는 것만 그린다 — 캡션이 라벨과 줄 번호를 댄다.
좌표는 _row 와 아래 헬퍼가 계산하고 손으로 찍지 않는다(yohan-figure 규칙 2).

라벨 길이를 먼저 잰다. 링크드인 흐름 장에서 상자 폭을 넘긴 글자가 옆 상자로 흘러
여섯 칸이 통째로 겹쳤다(2026-09-06). 상자 폭에 안 들어가면 라벨을 줄이고 뜻은 캡션이 받는다.
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
_elbow = bf._elbow
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
FIG_CHAIN = _svg(W, 128, '발전소에서 가속기까지 전압을 다섯 번 낮춘다', _DEFS + ''.join(
    [_lt(8, 30, '들어오는 쪽', 't-sm', True), _lt(W - 84, 30, '쓰는 쪽', 't-sm', True)]
    + [_box(x, y, w, h, lines, INK3, 1.5)
       for (x, y, w, h), lines in zip(_C, _CHAIN_CELLS)]
    + [_a(_C[i - 1][0] + _C[i - 1][2], 83, _C[i][0], 83) for i in range(1, 5)]))


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


FIG_PJMPRICE = _svg(W, 40 + 4 * _PSTEP - (_PSTEP - 44) + 12,
                    'PJM 용량 요금이 정해지는 길과 같은 기간 선물시장',
                    _DEFS + ''.join([
                        _lt(_LX, 26, '값을 정하는 길', 't-lab', True),
                        _lt(_RX, 26, '같은 기간 실물 신호', 't-lab', True),
                        _col(_LX, _LEFT, 2),
                        _col(_RX, _RIGHT, 1),
                    ]))


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


FIG_GAP = _svg(W, 270, '같은 경매를 실제 청산가와 모델을 고쳤을 때로 견준다',
               ''.join([
                   '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
                   % (_GX0 - 16, _GBASE, W - _GX0 + 16, _GBASE, INK3),
                   _lt(_GX0 - 16, 20, '메가와트·하루당 청산가', 't-sm', True),
               ] + [_gbar(i, *b) for i, b in enumerate(_GBARS)]))


# ── 도해 4. 같은 물음에 답이 셋 ──────────────────────────────────────
# 견줄 때는 같은 꼴(확정 규칙). 세 판이 같은 크기이고 줄도 같은 세 줄이다.
#
# 처음에 _box 에 이름을 넘겼더니 이름이 상자 세로 가운데에 놓여, 따로 그린 줄과
# 겹쳤다(2026-09-07). _box 는 줄을 가운데 정렬하므로 머리와 본문을 같이 못 둔다 —
# 사각형을 직접 그리고 글자 자리를 손으로 잡는다. 행 이름도 판 안으로 파고들어
# 왼쪽에 라벨 열을 따로 뗐다.
_TLAB, _TGAP = 100, 14
_TW = (W - _TLAB - _TGAP * 2 - 10) // 3
_TH, _TY = 152, 44
# 라벨 열이 84px 이라 「값이 어떻게 정해지나」가 넘쳐 첫 판 글자와 겹쳤다(2026-09-07).
# 행 이름은 여기서 줄이고 온전한 말은 캡션이 받는다. 그때 줄인 이름도 여전히 넘쳤는데
# 검사기가 한글을 9px 로 어림해 못 잡았다 — 13px 로 고친 뒤 라벨 열을 100px 로 넓혔다
# (2026-09-09). 이 장의 라벨 열 넷이 같은 이유로 함께 넓어졌다
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


FIG_THREE = _svg(W, 214, '같은 물음에 세 시장이 다르게 답한다',
                 ''.join([_lt(4, _TY + 64 + k * 34, s, 't-sm', False)
                          for k, s in enumerate(_TROWS)])
                 + ''.join(_panel(i, n, r) for i, (n, r) in enumerate(_THREE)))


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


FIG_PHASE = _svg(W, _PHY + 4 * _PHSTEP - 2, '800볼트 직류 네 단계 · 단계마다 변환이 어느 마디에서 일어나나',
                 _DEFS + ''.join(
                     [_lt(8, 30, '들어오는 쪽', 't-sm', True),
                      _lt(W - 84, 30, '쓰는 쪽', 't-sm', True)]
                     + [_box(x, y, w, h, lines, INK3, 1.5)
                        for (x, y, w, h), lines in zip(_C, _CHAIN_CELLS)]
                     + [_a(_C[i - 1][0] + _C[i - 1][2], 83, _C[i][0], 83) for i in range(1, 5)]
                     + [_lt(8, 134, '변환이 일어나는 자리', 't-sm', True)]
                     + [_phrow(i, *r) for i, r in enumerate(_PHASE_AT)]))


# ── 도해 6. 같은 글이 절감치를 두 값으로 적는다 ──────────────────────
# 견줄 때는 나란한 세로 막대, 높이는 값에 비례(확정 규칙 2026-09-04).
# 두 값 다 원문에 있고, 원문이 이 둘을 일치한다고 적은 것이 이 그림의 요점이다.
_MMAX, _MH, _MBASE, _MW_, _MGAP = 69.0, 130, 186, 120, 110
_MBARS = [(50, '50메가와트', '엔비디아 발표', '최대 5%', True),
          (69, '69메가와트', '단계별 계산', '6.9%', False)]
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


FIG_MW = _svg(W, 232, '같은 글이 절감치를 두 값으로 적는다', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_MX0 - 16, _MBASE, W - _MX0 + 16, _MBASE, INK3),
     _lt(_MX0 - 16, 20, '1기가와트에서 아끼는 전력', 't-sm', True)]
    + [_mbar(i, *b) for i, b in enumerate(_MBARS)]))


# ── 도해 7. 고치자는 안이 어느 마디를 겨눴고 어디서 멈췄나 ────────────
# 도해 2의 왼쪽 판(값을 정하는 길)을 같은 좌표로 다시 깔고, 규칙을 고치는 길을
# 그 옆에 세워 두 번째 마디로 잇는다. 부결됐으므로 잇는 선은 점선이다.
_FIXY = [40, 106, 172]
_FIXCELLS = [['겨울 인증치 반영안'],
             ['태스크포스 178대 54'],
             ['26일 뒤 30.7% 부결']]

FIG_FIX = _svg(W, 40 + 4 * _PSTEP - (_PSTEP - 44) + 12,
               '요금이 정해지는 길과 그것을 고치려던 절차',
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
                      % (_RX - 6, _FIXY[1] + 22, _LX + 250 + 6, INK3)]))


# ── 도해 8. 작업시간이 현장에서 공장으로 옮겨간다 ─────────────────────
# 같은 판(공장·현장 두 마디)을 줄마다 한 번씩 그린다 — 줄마다 다른 것만 그리면
# 다른 그림 둘로 읽힌다. 값은 50메가와트 수랭 홀 기준이다(건설-260729 L444·L445).
_MW2, _MGAP2, _MLAB = 250, 16, 96
_MY, _MSTEP2, _MH2 = 52, 74, 56
_MROWS = [('관행 시공', ['없음'], ['12,000시간', '메가와트당'], '30~35개월', 1),
          ('완전 모듈러', ['기계·전기 설치'], ['4,500시간', '메가와트당'], '24~30개월', 0)]


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


FIG_MODULAR = _svg(W, _MY + 2 * _MSTEP2 - 8, '작업시간이 현장에서 공장으로 옮겨간다',
                   ''.join([_lt(_MLAB, 34, '공장', 't-lab', True),
                            _lt(_MLAB + _MW2 + _MGAP2, 34, '현장', 't-lab', True)]
                           + [_mrow(i, *r) for i, r in enumerate(_MROWS)]))


# ── 도해 9. 랙 하나가 짊어지는 전력 ──────────────────────────────────
# 값을 견줄 때는 나란한 세로 막대, 높이는 값에 비례(확정 규칙 2026-09-04).
# 범위로 적힌 세대는 위 끝으로 그린다 — 캡션이 「위 끝」이라 밝힌다.
_DMAX, _DH, _DBASE = 1000.0, 160, 214
_DBARS = [(15, '10~15', 'AI 이전'), (20, '20', '클라우드'), (120, '100~120', '지금'),
          (600, '600', '루빈 울트라'), (1000, '1,000', '다음 세대')]
_DW, _DG = 92, 20
_DX0 = (W - (5 * _DW + 4 * _DG)) // 2


def _dbar(i, v, lab, when):
    x = _DX0 + i * (_DW + _DG)
    h = max(int(_DH * v / _DMAX), 3)
    y = _DBASE - h
    last = i == len(_DBARS) - 1
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _DW, h, 'var(--sunk)' if last else 'none',
                                  INK if last else INK3),
        _t(x + _DW // 2, y - 8, lab, 't-lab'),
        _t(x + _DW // 2, _DBASE + 18, when, 't-sm'),
    ])


FIG_DENSITY = _svg(W, 240, '랙 하나가 짊어지는 전력이 세대마다 뛴다', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_DX0 - 16, _DBASE, W - _DX0 + 16, _DBASE, INK3),
     _lt(_DX0 - 16, 22, '랙 하나의 전력 (킬로와트)', 't-sm', True)]
    + [_dbar(i, *b) for i, b in enumerate(_DBARS)]))


# ── 도해 10. 일정이 어느 마디에서 늘어났나 ───────────────────────────
# 네비우스 뉴저지 한 부지의 첫 50메가와트. 같은 일을 계획과 실제로 견준다.
_LMAX, _LH2, _LBASE = 11.0, 150, 208
_LBARS = [(4, '4개월', '발표', False), (6, '6개월', '장비 지연', False),
          (11, '10~11개월', '실제', True)]
_LW, _LG2 = 120, 40
_LX0 = (W - (3 * _LW + 2 * _LG2)) // 2


def _lbar(i, v, lab, when, hot):
    x = _LX0 + i * (_LW + _LG2)
    h = int(_LH2 * v / _LMAX)
    y = _LBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _LW, h, 'var(--sunk)' if hot else 'none',
                                  INK if hot else INK3),
        _t(x + _LW // 2, y - 8, lab, 't-lab'),
        _t(x + _LW // 2, _LBASE + 18, when, 't-sm'),
    ])


FIG_DELAY = _svg(W, 234, '첫 50메가와트를 켜기까지 걸린 개월 수', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_LX0 - 16, _LBASE, W - _LX0 + 16, _LBASE, INK3),
     _lt(_LX0 - 16, 22, '첫 50메가와트까지 (개월)', 't-sm', True)]
    + [_lbar(i, *b) for i, b in enumerate(_LBARS)]))


# ── 도해 11. 두 길 ──────────────────────────────────────────────────
# 견줄 때는 같은 꼴(확정 규칙). 두 판이 같은 크기이고 줄도 같은 세 줄이다.
_2W, _2LAB, _2GAP = 244, 108, 20
_2H, _2Y = 148, 44
_2ROWS = ['무엇을 기다리나', '언제 켜나', '값']
_2PANES = [('계통에 연결한다', ['접속 대기열·허가', '2030년', '계통 요금']),
           ('계통 뒤편에 짓는다', ['장비·인력', '2027~2028년', '더 비싸다'])]


def _2panel(i, name, rows):
    x = _2LAB + i * (_2W + _2GAP)
    hot = i == 1
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
           'stroke-width="%.1f"/>' % (x, _2Y, _2W, _2H, INK if hot else INK3,
                                      1.8 if hot else 1.5),
           _t(x + _2W // 2, _2Y + 26, name, 't-lab')]
    for k, s in enumerate(rows):
        out.append(_t(x + _2W // 2, _2Y + 62 + k * 30, s, 't-sm'))
    return ''.join(out)


FIG_TWOPATH = _svg(W, 210, '전력을 어디서 받을지 두 길이 갈린다',
                   ''.join([_lt(4, _2Y + 62 + k * 30, s, 't-sm', False)
                            for k, s in enumerate(_2ROWS)])
                   + ''.join(_2panel(i, n, r) for i, (n, r) in enumerate(_2PANES)))


# ── 도해 12. 사슬 한 마디를 건너뛴다 ─────────────────────────────────
# 도해 1의 판을 같은 좌표로 다시 깔고, 건너뛴 마디만 점선으로 바꾼다
# (점선 = 문제·없는 것, 확정 규칙 S2). 스페이스X·xAI 가 한 일이다.
_SKIP = 1
_SKIP_CELLS = [['부지 변전소'] if i == _SKIP else c
               for i, c in enumerate(_CHAIN_CELLS)]


def _skipbox(i, cell):
    x, y, w, h = _C[i]
    if i != _SKIP:
        return _box(x, y, w, h, cell, INK3, 1.5)
    return (_box(x, y, w, h, cell, INK3, 1.5)
            .replace('stroke-width="1.5"', 'stroke-width="1.5" stroke-dasharray="5 4"'))


FIG_SKIP = _svg(W, 128, '전압 사슬에서 대형 변압기 마디를 건너뛴 자리', _DEFS + ''.join(
    [_lt(8, 30, '들어오는 쪽', 't-sm', True), _lt(W - 84, 30, '쓰는 쪽', 't-sm', True)]
    + [_skipbox(i, c) for i, c in enumerate(_SKIP_CELLS)]
    + [_a(_C[i - 1][0] + _C[i - 1][2], 83, _C[i][0], 83) for i in (1, 3, 4)]
    + ['<path d="M%d %d Q%d %d %d %d" stroke="%s" stroke-width="1.6" fill="none" '
       'marker-end="url(#fig-arrow)"/>'
       % (_C[0][0] + _C[0][2], 68, W // 2 - 66, 24, _C[2][0], 68, INK)]
))


# ── 도해 13. 발전 설비 단가 ──────────────────────────────────────────
# 값을 견줄 때는 나란한 세로 막대, 범위는 위 끝(확정 규칙 2026-09-04).
# 리드타임은 축이 달라 여기 안 넣는다 — 축이 둘이면 그림을 둘로 나눈다.
_KMAX, _KH, _KBASE = 4000.0, 150, 206
_KBARS = [(1800, '1,500~1,800', '산업용', '가스터빈', False),
          (2000, '1,700~2,000', '항공유도', '가스터빈', False),
          (2000, '1,700~2,000', '왕복엔진', '', False),
          (4000, '3,000~4,000', '연료전지', '', True)]
_KW2, _KG = 110, 26
_KX0 = (W - (4 * _KW2 + 3 * _KG)) // 2


def _kbar(i, v, lab, n1, n2, hot):
    x = _KX0 + i * (_KW2 + _KG)
    h = int(_KH * v / _KMAX)
    y = _KBASE - h
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
           'stroke-width="1.6"/>' % (x, y, _KW2, h, 'var(--sunk)' if hot else 'none',
                                     INK if hot else INK3),
           _t(x + _KW2 // 2, y - 8, lab, 't-lab'),
           _t(x + _KW2 // 2, _KBASE + 18, n1, 't-sm')]
    if n2:
        out.append(_t(x + _KW2 // 2, _KBASE + 34, n2, 't-sm'))
    return ''.join(out)


FIG_KW = _svg(W, 250, '자가발전 설비 단가', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_KX0 - 16, _KBASE, W - _KX0 + 16, _KBASE, INK3),
     _lt(_KX0 - 16, 22, '킬로와트당 달러 (위 끝)', 't-sm', True)]
    + [_kbar(i, *b) for i, b in enumerate(_KBARS)]))


# ── 도해 14. 벤더가 말한 단축폭과 저자가 잰 값 ───────────────────────
_VMAX, _VH, _VBASE = 85.0, 140, 196
_VBARS = [(85, '85%', '버티브', '일부 제품군', False),
          (60, '60%', '슈나이더', '전력·냉각 모듈', False),
          (50, '50%', '버티브', '모듈 배포 단계', False),
          (36, '36%', '저자 실측', '홀 하나 전체', True)]
_VW, _VG = 116, 22
_VX0 = (W - (4 * _VW + 3 * _VG)) // 2


def _vbar(i, v, lab, who, scope, hot):
    x = _VX0 + i * (_VW + _VG)
    h = int(_VH * v / _VMAX)
    y = _VBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _VW, h, 'var(--sunk)' if hot else 'none',
                                  INK if hot else INK3),
        _t(x + _VW // 2, y - 8, lab, 't-lab'),
        _t(x + _VW // 2, _VBASE + 18, who, 't-sm'),
        _t(x + _VW // 2, _VBASE + 34, scope, 't-sm'),
    ])


FIG_VENDOR = _svg(W, 240, '벤더가 말한 단축폭과 저자가 잰 값', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_VX0 - 16, _VBASE, W - _VX0 + 16, _VBASE, INK3),
     _lt(_VX0 - 16, 22, '기간 단축폭', 't-sm', True)]
    + [_vbar(i, *b) for i, b in enumerate(_VBARS)]))


# ── 도해 15. 가속기 한 장을 한 시간 돌리는 값 ────────────────────────
# 같은 축(시간당 달러)만 담는다. 자본비용과 월 총소유비용은 축이 달라 산문에 남긴다.
_OMAX, _OH, _OBASE = 10.91, 150, 200
_OBARS = [(2.37, '2.37달러', '지상', '', True), (2.49, '2.49달러', '지상', '할증 뒤', True),
          (8.64, '8.64달러', '우주', '', False), (10.91, '10.91달러', '우주', '할증 뒤', False)]
_OW, _OG, _OPAIR = 104, 20, 56
_OX0 = (W - (4 * _OW + 2 * _OG + _OPAIR)) // 2


def _obar(i, v, lab, who, note, ground):
    x = _OX0 + i * (_OW + _OG) + (_OPAIR - _OG if i >= 2 else 0)
    h = int(_OH * v / _OMAX)
    y = _OBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _OW, h, 'var(--sunk)' if ground else 'none',
                                  INK3 if ground else INK),
        _t(x + _OW // 2, y - 8, lab, 't-lab'),
        _t(x + _OW // 2, _OBASE + 18, who, 't-sm'),
        _t(x + _OW // 2, _OBASE + 34, note, 't-sm'),
    ])


FIG_ORBIT = _svg(W, 244, '가속기 한 장을 한 시간 돌리는 값', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_OX0 - 16, _OBASE, W - _OX0 + 16, _OBASE, INK3),
     _lt(_OX0 - 16, 22, '시간당 달러', 't-sm', True)]
    + [_obar(i, *b) for i, b in enumerate(_OBARS)]))


# ── 도해 16. 한 회사 안에서 갈리는 두 말 ─────────────────────────────
# 견줄 때는 같은 꼴. 두 판이 같은 크기이고 줄도 같은 세 줄이다.
_NW, _NLAB, _NGAP = 244, 120, 20
_NH, _NY = 152, 44
_NROWS = ['언제 말했나', '어디에 짓나', '무엇을 최우선으로']
_NPANES = [('래리 코벤', ['2026년 2월 24일', 'PJM 밖에 5.4기가와트', '계통 밖 자체 발전']),
           ('롭 고데트', ['2026년 5월 6일', '계통에 연결해서', '계통 연결형이 옳다'])]


def _npanel(i, name, rows):
    x = _NLAB + i * (_NW + _NGAP)
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
           'stroke-width="1.5"/>' % (x, _NY, _NW, _NH, INK3),
           _t(x + _NW // 2, _NY + 26, name, 't-lab')]
    for k, s in enumerate(rows):
        out.append(_t(x + _NW // 2, _NY + 62 + k * 32, s, 't-sm'))
    return ''.join(out)


FIG_NRG = _svg(W, 216, '한 회사 임원 둘이 반대로 말한 자리',
               ''.join([_lt(4, _NY + 62 + k * 32, s, 't-sm', False)
                        for k, s in enumerate(_NROWS)])
               + ''.join(_npanel(i, n, r) for i, (n, r) in enumerate(_NPANES)))


# ── 도해 17. 텍사스에서 전력을 받는 길 ───────────────────────────────
# 축이 둘이다 — 전력을 어디서 가져오나(둘)와 계통에 어떻게 붙나(셋). 앞뒤 관계가
# 아니라 나란한 두 갈래라 위아래로 잇지 않는다. 개수는 원문이 센 수다.
_EL, _EY_A, _EY_B = 104, 44, 128
# 줄 이름 자리(_EL)를 비우고 그 오른쪽부터 상자를 놓는다 — 가운데 정렬하면 이름과 겹친다
_EROWA = [(_EL + i * (248 + 24), _EY_A, 248, 46) for i in range(2)]
_EROWB = [(_EL + i * (164 + 14), _EY_B, 164, 46) for i in range(3)]
_EA = [['순계량'], ['자체 발전 설비']]
_EB = [['계량점을 하나로'], ['인출 상한까지'], ['혼잡할 때 줄인다']]

FIG_ERCOTWAY = _svg(W, 194, '텍사스에서 전력을 받는 길', ''.join(
    [_lt(4, _EY_A + 28, '전력을 어디서', 't-sm', True),
     _lt(4, _EY_B + 28, '계통에 어떻게', 't-sm', True)]
    + [_box(x, y, w, h, c, INK3, 1.5) for (x, y, w, h), c in zip(_EROWA, _EA)]
    + [_box(x, y, w, h, c, INK3, 1.5) for (x, y, w, h), c in zip(_EROWB, _EB)]))


# ── 도해 18. 자체 발전소가 다섯 달 만에 커진 폭 ──────────────────────
_SMAX, _SH, _SBASE = 1700.0, 150, 200
_SBARS = [(495, '495메가와트', '2026년 2월', '터빈 27대', False),
          (1700, '1.7기가와트', '2026년 7월', '터빈 69대', True)]
_SW, _SG2 = 150, 90
_SX0 = (W - (2 * _SW + _SG2)) // 2


def _sbar(i, v, lab, when, what, hot):
    x = _SX0 + i * (_SW + _SG2)
    h = int(_SH * v / _SMAX)
    y = _SBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _SW, h, 'var(--sunk)' if hot else 'none',
                                  INK if hot else INK3),
        _t(x + _SW // 2, y - 8, lab, 't-lab'),
        _t(x + _SW // 2, _SBASE + 18, when, 't-sm'),
        _t(x + _SW // 2, _SBASE + 34, what, 't-sm'),
    ])


FIG_SOUTH = _svg(W, 244, '허가 밖에 세운 발전소가 다섯 달 만에 커진 폭', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_SX0 - 16, _SBASE, W - _SX0 + 16, _SBASE, INK3),
     _lt(_SX0 - 16, 22, '사우스헤이븐 발전소', 't-sm', True)]
    + [_sbar(i, *b) for i, b in enumerate(_SBARS)]))


# ── 도해 19. 궤도 자리 셋 ────────────────────────────────────────────
_OW2, _OLAB2, _OGAP2 = 160, 88, 16
_OH2, _OY2 = 148, 44
_OROWS = ['어디에', '햇빛', '걸리는 것']
_OPANES = [('저궤도', ['400~500킬로미터', '하루의 60%', '하루 열다섯 바퀴']),
           ('밤낮 경계선', ['같은 저궤도', '하루 35분만 그늘', '전력전자가 복잡']),
           ('라그랑주 L1', ['훨씬 멀리', '24시간', '빛이 왕복 10초'])]


def _opanel(i, name, rows):
    x = _OLAB2 + i * (_OW2 + _OGAP2)
    hot = i == 2
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
           'stroke-width="%.1f"/>' % (x, _OY2, _OW2, _OH2, INK if hot else INK3,
                                      1.8 if hot else 1.5),
           _t(x + _OW2 // 2, _OY2 + 26, name, 't-lab')]
    for k, s in enumerate(rows):
        out.append(_t(x + _OW2 // 2, _OY2 + 62 + k * 32, s, 't-sm'))
    return ''.join(out)


FIG_ORBITSITE = _svg(W, 212, '궤도 자리 셋 — 햇빛과 걸림돌',
                     ''.join([_lt(4, _OY2 + 62 + k * 32, s, 't-sm', False)
                              for k, s in enumerate(_OROWS)])
                     + ''.join(_opanel(i, n, r) for i, (n, r) in enumerate(_OPANES)))


# ── 도해 20. 데이터센터를 빼고 경매를 다시 돌리면 ────────────────────
# 축 하나(용량대금이 줄어드는 액수)만 담는다. 피크부하 감소는 축이 달라 산문에 남긴다.
_IMAX, _IH, _IBASE = 9.33, 140, 190
_IBARS = [(9.33, '93억 3,000만 달러', '모든 데이터센터를', '빼면 64% 감소', True),
          (7.74, '77억 4,000만 달러', '이미 가동 중인 것만', '넣으면 53% 감소', False)]
_IW, _IG = 180, 90
_IX0 = (W - (2 * _IW + _IG)) // 2


def _ibar(i, v, lab, l1, l2, hot):
    x = _IX0 + i * (_IW + _IG)
    h = int(_IH * v / _IMAX)
    y = _IBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _IW, h, 'var(--sunk)' if hot else 'none',
                                  INK if hot else INK3),
        _t(x + _IW // 2, y - 8, lab, 't-lab'),
        _t(x + _IW // 2, _IBASE + 18, l1, 't-sm'),
        _t(x + _IW // 2, _IBASE + 34, l2, 't-sm'),
    ])


FIG_IMM = _svg(W, 234, '데이터센터를 빼고 같은 경매를 다시 돌리면', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_IX0 - 16, _IBASE, W - _IX0 + 16, _IBASE, INK3),
     _lt(_IX0 - 16, 22, '용량대금이 줄어드는 액수', 't-sm', True)]
    + [_ibar(i, *b) for i, b in enumerate(_IBARS)]))


# ── 도해 21. 완화 설비 값 ────────────────────────────────────────────
_CMAX, _CH2, _CBASE = 157.0, 140, 196
_CBARS = [(80, '3,800만~8,000만', '배터리 100메가와트', '2시간'),
          (157, '7,600만~1억 5,700만', '같은 배터리', '4시간'),
          (20, '1,000만~2,000만', '동기조상기', '1기가와트 기준')]
_CW, _CG2 = 168, 24
_CX0 = (W - (3 * _CW + 2 * _CG2)) // 2


def _cbar(i, v, lab, l1, l2):
    x = _CX0 + i * (_CW + _CG2)
    h = int(_CH2 * v / _CMAX)
    y = _CBASE - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="none" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _CW, h, INK3),
        _t(x + _CW // 2, y - 8, lab, 't-lab'),
        _t(x + _CW // 2, _CBASE + 18, l1, 't-sm'),
        _t(x + _CW // 2, _CBASE + 34, l2, 't-sm'),
    ])


FIG_MITIGATE = _svg(W, 240, '계통 흔들림을 잡는 설비 값', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_CX0 - 16, _CBASE, W - _CX0 + 16, _CBASE, INK3),
     _lt(_CX0 - 16, 22, '설치비 달러 (위 끝)', 't-sm', True)]
    + [_cbar(i, *b) for i, b in enumerate(_CBARS)]))


# ── 도해 22. 나라별 전기요금 ─────────────────────────────────────────
# 범위는 위 끝. 보조가 섞인 값은 그 사실을 라벨에 적고 값은 원문 표기 그대로 둔다.
_TMAX, _TH2, _TBASE2 = 23.0, 150, 206
_TBARS = [(8.3, '8.3', '미국', ''), (12, '10~12', '한국·대만', '보조 섞인 값'),
          (15.2, '15.2', '일본', ''), (18, '18', '유럽 산업용', ''),
          (23, '23', '싱가포르', '')]
_TW2, _TG2 = 96, 20
_TX02 = (W - (5 * _TW2 + 4 * _TG2)) // 2


def _tbar(i, v, lab, who, note):
    x = _TX02 + i * (_TW2 + _TG2)
    h = int(_TH2 * v / _TMAX)
    y = _TBASE2 - h
    hot = who == '한국·대만'
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
           'stroke-width="1.6"/>' % (x, y, _TW2, h, 'var(--sunk)' if hot else 'none',
                                     INK if hot else INK3),
           _t(x + _TW2 // 2, y - 8, lab, 't-lab'),
           _t(x + _TW2 // 2, _TBASE2 + 18, who, 't-sm')]
    if note:
        out.append(_t(x + _TW2 // 2, _TBASE2 + 34, note, 't-sm'))
    return ''.join(out)


FIG_TARIFF = _svg(W, 250, '나라별 전기요금', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_TX02 - 16, _TBASE2, W - _TX02 + 16, _TBASE2, INK3),
     _lt(_TX02 - 16, 22, '킬로와트시당 센트 (위 끝)', 't-sm', True)]
    + [_tbar(i, *b) for i, b in enumerate(_TBARS)]))


# ── 도해 23. 긴급경매 대금이 흘러가는 길 ─────────────────────────────
# 돈이 도는 길을 판으로 세운다. 아직 안 일어난 자리는 점선(확정 규칙 S2).
_QY, _QSTEP, _QH = 14, 62, 44
_QCELLS = [(['신규 발전과 2043년까지 장기계약'], False),
           (['비용을 지역별로 나눈다 · 15년 고정 · 사후 정산 없음'], False),
           (['주가 비용배분 정책을 통과시킨다'], True),
           (['새 대형 부하가 서명한다'], True),
           (['서명이 없으면 요금청구서로 간다'], False)]


def _qbox(i, lines, pending):
    y = _QY + i * _QSTEP
    b = _box(14, y, W - 28, _QH, lines, INK if i == 4 else INK3,
             1.8 if i == 4 else 1.5)
    return b.replace('stroke-width="1.5"', 'stroke-width="1.5" stroke-dasharray="5 4"') \
        if pending else b


FIG_EMERGENCY = _svg(W, _QY + 5 * _QSTEP - 4, '긴급경매 대금이 흘러가는 길', _DEFS + ''.join(
    [_qbox(i, c, p) for i, (c, p) in enumerate(_QCELLS)]
    + [_a(W // 2, _QY + i * _QSTEP + _QH, W // 2, _QY + (i + 1) * _QSTEP)
       for i in range(4)]))


# ── 도해 24. 용량 청산가가 뛴 폭 ─────────────────────────────────────
# 같은 축(메가와트·하루당 달러) 하나. 상한은 가로 점선으로 얹는다 — 막대가 아니라 선이다.
_PMAX, _PH2, _PBASE = 450.0, 150, 210
_PBARS = [(29, '29달러', '2024/25년', '', True), (270, '270달러', '2025/26년', '', True),
          (450, '450달러', '2025/26년', '일부 지역', False)]
_PW2, _PG3 = 130, 40
_PX0 = (W - (3 * _PW2 + 2 * _PG3)) // 2
_PCAP = _PBASE - int(_PH2 * 329 / _PMAX)


def _pbar(i, v, lab, when, note, solid):
    x = _PX0 + i * (_PW2 + _PG3)
    h = int(_PH2 * v / _PMAX)
    y = _PBASE - h
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
           'stroke-width="1.6"/>' % (x, y, _PW2, h, 'var(--sunk)' if solid else 'none',
                                     INK if i == 1 else INK3),
           _t(x + _PW2 // 2, y - 8, lab, 't-lab'),
           _t(x + _PW2 // 2, _PBASE + 18, when, 't-sm')]
    if note:
        out.append(_t(x + _PW2 // 2, _PBASE + 34, note, 't-sm'))
    return ''.join(out)


FIG_CLEAR = _svg(W, 250, '용량 청산가가 뛴 폭', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_PX0 - 16, _PBASE, W - _PX0 + 16, _PBASE, INK3),
     _lt(_PX0 - 16, 22, '메가와트·하루당 달러', 't-sm', True),
     '<path d="M%d %d H%d" stroke="%s" stroke-width="1.2" stroke-dasharray="6 4"/>'
     % (_PX0 - 16, _PCAP, W - _PX0 + 16, INK3),
     _lt(W - _PX0 + 22, _PCAP + 4, '상한 329', 't-sm', False)]
    + [_pbar(i, *b) for i, b in enumerate(_PBARS)]))


# ── 도해 25. 낙찰가가 가구 청구서가 되는 계산 ────────────────────────
# 저자가 밝힌 환산 순서를 그대로 사슬로 세운다. 사슬 상자는 한 크기.
_BSTEP, _BH, _BY = 58, 44, 14
_BCELLS = [['청산가 하루 329달러'], ['용량대금 160억 달러 · 메가와트당 12만 달러'],
           ['부하율 40%를 적용 · 메가와트시당 34달러'], ['킬로와트시당 3.4센트'],
           ['월 880킬로와트시를 곱하면 월 29.9달러']]

FIG_BILL = _svg(W, _BY + 5 * _BSTEP - 4, '낙찰가가 가구 청구서가 되기까지', _DEFS + ''.join(
    [_box(60, _BY + i * _BSTEP, W - 120, _BH, c, INK if i == 4 else INK3,
          1.8 if i == 4 else 1.5) for i, c in enumerate(_BCELLS)]
    + [_a(W // 2, _BY + i * _BSTEP + _BH, W // 2, _BY + (i + 1) * _BSTEP)
       for i in range(4)]))


# ── 도해 26. 텍사스 공동입지 규모 ────────────────────────────────────
_LMAX2, _LH3, _LBASE2 = 2885.0, 140, 196
_LBARS2 = [(2885, '2,885', '알려진 전체', '2026년 6월', True),
           (1200, '1,200', 'AWS 코만치피크', '순계량', False),
           (525.5, '525.5', '크루소 굿나이트', '순계량', False)]
_LW2, _LG3 = 168, 30
_LX02 = (W - (3 * _LW2 + 2 * _LG3)) // 2


def _lbar2(i, v, lab, who, note, hot):
    x = _LX02 + i * (_LW2 + _LG3)
    h = int(_LH3 * v / _LMAX2)
    y = _LBASE2 - h
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
        'stroke-width="1.6"/>' % (x, y, _LW2, h, 'var(--sunk)' if hot else 'none',
                                  INK if hot else INK3),
        _t(x + _LW2 // 2, y - 8, lab, 't-lab'),
        _t(x + _LW2 // 2, _LBASE2 + 18, who, 't-sm'),
        _t(x + _LW2 // 2, _LBASE2 + 34, note, 't-sm'),
    ])


FIG_COLO = _svg(W, 240, '텍사스 공동입지 규모', ''.join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
     % (_LX02 - 16, _LBASE2, W - _LX02 + 16, _LBASE2, INK3),
     _lt(_LX02 - 16, 22, '메가와트', 't-sm', True)]
    + [_lbar2(i, *b) for i, b in enumerate(_LBARS2)]))


# ── 도해 27. 규칙을 고치려면 몇이 찬성해야 하나 ──────────────────────
# 부문 이름은 원문에 없다 — 개수만 원문이 센 수다(다섯). 그래서 이름을 짓지 않고
# 번호로 둔다. 짙은 둘이 「어느 두 부문만 뭉쳐도 막는다」를 보이는 자리다.
_GVY, _GVH = 66, 52
_GVC = _row(5, _GVY, _GVH, 108, gap=14)

FIG_GOVERN = _svg(W, 134, '규칙을 고치려면 다섯 부문 가운데 셋이 넘게 찬성해야 한다', ''.join(
    [_lt(8, 30, '회원 부문 다섯 · 가중치가 모두 같다', 't-sm', True)]
    + [_box(x, y, w, h, ['부문 %d' % (i + 1)], INK if i >= 3 else INK3,
            1.8 if i >= 3 else 1.5)
       for i, (x, y, w, h) in enumerate(_GVC)]))


# ── 도해 28. 기준안과 머스크안 ───────────────────────────────────────
# 견줄 때는 같은 꼴. 두 판이 같은 크기이고 줄도 같은 네 줄이다.
_SPW, _SPLAB, _SPGAP = 236, 116, 24
_SPH, _SPY = 184, 44
_SPROWS = ['역전 시점', '지상 자본비용', '발사 비용', '2035년 지상 용량']
_SPPANES = [('기준안', ['2040년쯤', '메가와트당 1,200만~1,400만 달러',
                      '기준으로 둔 값', '1,150기가와트']),
            ('머스크안', ['2034년', '메가와트당 약 5,500만 달러',
                        '기준안보다 85% 낮게', '576기가와트'])]


def _sppanel(i, name, rows):
    x = _SPLAB + i * (_SPW + _SPGAP)
    hot = i == 1
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
           'stroke-width="%.1f"/>' % (x, _SPY, _SPW, _SPH, INK if hot else INK3,
                                      1.8 if hot else 1.5),
           _t(x + _SPW // 2, _SPY + 26, name, 't-lab')]
    for k, s in enumerate(rows):
        out.append(_t(x + _SPW // 2, _SPY + 62 + k * 34, s, 't-sm'))
    return ''.join(out)


FIG_SPACECASE = _svg(W, 248, '우주가 지상을 따라잡는 시점을 두 가정으로 잡는다',
                     ''.join([_lt(4, _SPY + 62 + k * 34, s, 't-sm', False)
                              for k, s in enumerate(_SPROWS)])
                     + ''.join(_sppanel(i, n, r) for i, (n, r) in enumerate(_SPPANES)))
