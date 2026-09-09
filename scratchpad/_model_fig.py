# -*- coding: utf-8 -*-
"""보고서 「모델 총정리」 층의 도해 넷. 색은 회색만(확정 규칙 S2).

프로세스 판을 먼저 세우고 그 위에 얹는다(확정 규칙, 2026-09-09). 이 층의 판은
값이 원가로 바뀌는 사슬 넷이다 — 사는 값 · 매달 나가는 값 · 헛돈 시간 · 시간당 단가.
좌표는 `_RAIL_Y` 와 `_CELL` 이 갖고 있고 도해마다 다시 찍지 않는다.

화살표 설명은 판 위에 안 얹고 아래 범례로 내린다. 동그라미 번호는 한 겹이다.
값은 원문 표 그림에 있는 것과 우리 모델이 낸 것만 그린다 — 캡션이 어느 쪽인지 밝힌다.
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'
NUM = '①②③④⑤⑥⑦⑧⑨'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _mark(x, y, n):
    """화살표에 붙는 동그라미 번호. 설명은 아래 범례로 내린다(확정 규칙).

    ①은 그 자체가 동그라미다. 테두리를 또 두르면 두 겹으로 보이므로,
    선을 가리는 바탕 원은 테두리 없이 종이색으로만 둔다.
    """
    return ('<circle cx="%d" cy="%d" r="10" fill="var(--paper)"/>%s'
            % (x, y, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    """판 아래 범례. 한 줄에 하나씩 — 번호와 그 화살표가 나르는 것."""
    return ''.join(_lt(20, y + i * 21, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


def _vline(x, y1, y2, dash=False):
    return ('<path d="M%d %d V%d" class="flow"%s/>'
            % (x, y1, y2, ' style="stroke-dasharray:5 4"' if dash else ''))


# ── 판. 값이 원가로 바뀌는 네 마디. FIG_STACK 과 FIG_CHAIN 이 같이 쓴다 ─────────
_CW, _CH, _CGAP = 132, 46, 14
_CY = 52
_CELL = [(20 + i * (_CW + _CGAP), _CY, _CW, _CH) for i in range(4)]
# 판 상자에는 번호를 안 단다. 동그라미 번호는 화살표 범례가 쓰는 기호라
# 상자에도 달면 같은 ①이 두 뜻이 된다(2026-09-09)
_STAGE = [['사는 값', '자본지출'],
          ['매달 나가는 값', '운영비'],
          ['헛돈 시간', '굿풋 손실'],
          ['시간당 단가', 'GPU-시간']]


def _stage_board(accent=(), skip=()):
    """네 마디 판. 상자 크기는 전부 같다 — 사슬은 한 크기로 세운다.

    skip 에 든 마디는 상자를 안 그린다. 그 자리를 덮어 쓸 도해가 자기 상자를
    따로 세우기 때문이다 — 판까지 그리면 글자가 두 벌로 겹친다.
    """
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(_CELL, _STAGE)):
        st, sw = (INK, 2.0) if i in accent else (INK3, 1.5)
        if i not in skip:
            out.append(_box(x, y, w, h, lines, st, sw))
        if i:
            px = _CELL[i - 1][0] + _CW
            out.append(_a(px, y + h // 2, x, y + h // 2))
    return ''.join(out)


# ── 절 3. 클러스터 월 총비용을 이루는 여덟 줄 ────────────────────────────
# 청구서에 찍히는 다섯과 안 찍히는 셋을 세로로 갈라 세운다. 값은 그림 016 의
# Hyperscaler 열이다 — 여덟 줄이 다 0 이 아닌 유일한 열이라 사슬이 끊기지 않는다.
_ITEMS = [('GPU', '14,929,920', True),
          ('저장', '246,835', True),
          ('네트워크', '19', True),
          ('컨트롤 플레인', '3,318', True),
          ('지원 3%', '455,403', True),
          ('굿풋 손실 10.53%', '1,571,424', False),
          ('설치(36개월 상각)', '416,572', False),
          ('디버깅', '8,333', False)]
_IX, _IH = 20, 30
_IBAR, _IBARW = 228, 244
_IMAX = 14_929_920
# 묶음 둘. 세로 구분선을 그으면 왼쪽 항목 이름을 가로지른다(2026-09-09) —
# 선 대신 묶음 머리글과 빈 줄로 가른다
_G1Y, _G2Y = 62, 232


def _ibar(v):
    """막대 길이. 최대값이 나머지의 서른 배라 제곱근으로 눌러 세운다."""
    return _IBARW * (v / _IMAX) ** 0.5


def _item_row(y, name, val, billed):
    v = float(val.replace(',', ''))
    col = INK3 if billed else INK
    return ''.join([
        _lt(_IX, y + 19, name, bold=False),
        '<rect x="%d" y="%d" width="%.1f" height="18" rx="2" fill="%s"/>'
        % (_IBAR, y + 4, max(_ibar(v), 2.0), col),
        _lt(int(_IBAR + max(_ibar(v), 2.0)) + 8, y + 18, '$' + val, 't-sm', False),
    ])


FIG_STACK = _svg(W, 420, '청구서에 찍히는 다섯 줄과 안 찍히는 세 줄', ''.join(
    [_lt(_IX, 30, '월 비용 항목'), _lt(_IBAR, 30, '금액 (막대는 제곱근 눈금)'),
     _lt(_IX, _G1Y - 8, '청구서에 찍힌다', 't-lab', False)]
    + [_item_row(_G1Y + i * _IH, *it) for i, it in enumerate(_ITEMS[:5])]
    + [_lt(_IX, _G2Y - 8, '청구서에 안 찍힌다', 't-lab', False)]
    + [_item_row(_G2Y + i * _IH, *it) for i, it in enumerate(_ITEMS[5:])]
    + [_box(_IX, 340, W - 40, 44,
            ['굿풋 손실은 GPU 비용에만 붙는다. 저장·망·컨트롤 플레인에는 안 붙는다',
             '이 규칙은 표에 안 적혀 있고 결과 값에서 거꾸로 읽어야 나온다'])]
))


# ── 절 4. 고장 한 번이 몇 장의 시간을 먹나 ──────────────────────────────
# 수식 셋을 줄로 늘어놓으면 어느 항이 다른지 눈이 못 찾는다(2026-09-10). 시간 항을
# 세로 열로 세우고 줄마다 그 항에 곱해지는 장수를 적으면, 다른 자리가 열로 맞춰진다.
_DRV = [('인지',), ('체크포인트', '÷2'), ('초기화',), ('전환',), ('수리',)]
_JOB, _RAD, _NONE = '작업 크기', '폭발 반경', '·'
# 원문 L131·L143 의 식 셋을 항별로 편 것이다. 값이 아니라 곱해지는 대상이다
_MODE = [('차가운 예비', '작업이 통째로 수리를 기다린다',
          [_JOB, _JOB, _JOB, _NONE, _JOB]),
         ('뜨거운 예비', '수리만 폭발 반경으로 줄어든다',
          [_JOB, _JOB, _JOB, _NONE, _RAD]),
         ('고장 견딤', '체크포인트 손실이 없다',
          [_JOB, _NONE, _NONE, _JOB, _RAD])]
_GX, _GLAB, _GCW = 20, 132, 94       # 왼쪽 여백 · 이름 칸 폭 · 항 한 칸 기본 폭
# 열 폭은 그 열에서 가장 넓은 글자에 맞춘다. 한 폭으로 두면 「체크포인트」가
# 다음 열의 + 를 물었다(2026-09-10)
_GWS = [_GCW, _GCW + 14, _GCW, _GCW, _GCW]
_GTX = 7                             # 칸 안 글자의 왼쪽 들여쓰기
_GHY, _GY, _GRH = 76, 104, 62         # 머리 줄 · 첫 줄 · 줄 높이


def _gcol(j):
    """항 j 번째 칸의 왼쪽 x. 손으로 안 찍는다(yohan-figure 규칙 2)."""
    return _GX + _GLAB + sum(_GWS[:j])


def _grid_row(i):
    """줄 하나. 칸은 「× 곱해지는 장수」이고 칸과 칸 사이의 ⊕ 가 항을 더한다."""
    name, note, cells = _MODE[i]
    y = _GY + i * _GRH
    on = (i == 2)
    out = [_lt(_GX, y + 22, name, bold=on),
           _lt(_GX, y + 46, note, 't-sm', False)]
    for j, v in enumerate(cells):
        x = _gcol(j)
        # 윗줄과 달라진 칸만 테두리를 두른다. 어디서 갈리는지가 이 그림의 전부다
        if i and v != _MODE[i - 1][2][j]:
            out.append('<rect x="%d" y="%d" width="%d" height="34" rx="6" fill="none" '
                       'stroke="%s" stroke-width="1.8"/>' % (x + 1, y + 8, _GWS[j] - 6, INK))
        # 칸 글자는 왼쪽에 붙인다. 가운데로 두면 줄마다 × 자리가 어긋나 세로로 안 읽힌다
        out.append(_lt(x + _GTX, y + 28,
                       '×%s' % v if v != _NONE else _NONE,
                       't-lab' if v != _NONE else 't-sm', False))
    return ''.join(out)


FIG_GOODPUT = _svg(W, 358, '식 셋을 항별로 세우면 다른 자리가 세 칸뿐이다', ''.join(
    [_lt(_GX, 30, '고장 한 번 → 잃는 GPU-시간. 열이 시간 항, 칸이 거기 곱해지는 장수'),
     _lt(_GX, 52, '클러스터 5,184장 · 평균 작업 4,096장 · 폭발 반경 64장 (그림 019)',
         't-sm', False)]
    + [_lt(_gcol(j) + _GTX, _GHY + k * 15, d, 't-lab')
       for j, lines in enumerate(_DRV) for k, d in enumerate(lines)]
    # 항끼리는 더한다. 줄마다 같은 셈이라 머리 줄에 한 번만 적는다
    + [_lt(_gcol(j) - 7, _GHY, '+', 't-sm', False) for j in range(1, len(_DRV))]
    + ['<path d="M%d %d H%d" stroke="var(--line)" stroke-width="1"/>'
       % (_GX, _GHY + 22, _gcol(len(_DRV)))]
    + [_grid_row(i) for i in range(3)]
    + [_mark(_gcol(3) + _GWS[3] - 12, _GY + 2 * _GRH - 6, 1),
       _mark(_gcol(4) + _GWS[4] - 12, _GY + _GRH - 6, 2)]
    + [_legend(294, ['전환이 수리를 대신한다 — 예비 노드로 넘어가고 작업은 계속 돈다',
                     '수리 시간에 작업 전체가 아니라 고장 난 랙만 곱해진다'])]
))


# ── 절 6. 서버 값에서 시간당 단가까지 ───────────────────────────────────
# 판을 다시 깔고 그 위에 추론 글의 사슬을 얹는다. 같은 좌표를 쓴다.
_L1, _L2 = 150, 250
_CHAIN_IN = [('서버 값', '$162,802'), ('망·저장·SW', '$41,928')]


def _chain_fig():
    out = [_stage_board(accent=(0, 1, 3), skip=(2,))]
    # ③ 굿풋 마디는 이 글이 안 다룬다. 점선으로 비워 둔다
    x3, y3, w3, h3 = _CELL[2]
    out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="var(--paper)" '
               'stroke="var(--ink-3)" stroke-width="1.5" stroke-dasharray="5 4"/>'
               % (x3, y3, w3, h3))
    out.append(_t(x3 + w3 // 2, y3 + 20, '헛돈 시간', 't-lab'))
    out.append(_t(x3 + w3 // 2, y3 + 36, '이 글은 안 다룸'))
    # 위 — 자본지출로 들어가는 둘. 상자로 세우면 ①과 값 글자가 테두리에 깔린다.
    # 더하기 한 줄이면 충분한 자리라 글자만 얹는다
    out.append(_lt(20, 22, '서버 값 $162,802 + 망·저장·소프트웨어 $41,928', bold=False))
    out.append(_lt(20, 40, '= 서버당 선불 $204,730'))
    # 아래 — 각 마디가 내는 시간당 값
    # 한 줄에 다 적으면 132픽셀 칸을 넘는다 — 근거를 둘째 줄로 내린다
    outs = [('$0.94', '4년 상각', 'WACC 13.25%'),
            ('$0.40', '가동률 80%', 'PUE 1.35'),
            ('', '', ''),
            ('$1.34', 'MI300X', '자기 TCO')]
    for i, (v, n1, n2) in enumerate(outs):
        if not v:
            continue
        x, y, w, h = _CELL[i]
        out.append(_vline(x + w // 2, y + h, 128))
        out.append(_box(x, 128, w, 54, [v + ' /GPU-시간', n1, n2], INK3, 1.2))
    out.append(_mark(_CELL[0][0] + _CW // 2, 112, 1))
    out.append(_mark(_CELL[1][0] + _CW // 2, 112, 2))
    out.append(_legend(200, [
        '선불액을 4년 원리금 균등으로 펴면 월 $5,518, GPU-시간당 $0.94 다',
        '전기는 정격이 아니라 가동률 80%와 PUE 1.35 를 거쳐 kW·월 $68.6 이 된다',
    ]))
    out.append(_box(20, 258, W - 40, 44,
                    ['이 글은 한 달을 730시간으로 센다. 클러스터 글은 720시간이다',
                     '두 글의 시간당 값을 그냥 나란히 놓으면 1.4%가 조용히 어긋난다']))
    return ''.join(out)


FIG_CHAIN = _svg(W, 316, '서버 값 한 줄이 GPU 시간당 단가가 되기까지', _chain_fig())


# ── 절 8. 빌릴 때와 살 때 문턱이 다르다 ─────────────────────────────────
# 값만 늘어놓으면 문턱을 넘는 것이 무슨 뜻인지 안 읽힌다(2026-09-09 지적).
# 문턱 둘이 축을 세 구간으로 가르고, 구간마다 결론이 다르다 — 그것이 이 그림이다.
# 구간 이름을 축 위에 적고, 문턱이 어디서 나온 값인지도 그 자리에 적는다.
_TX0, _TXW = 96, 448
# 오른쪽 끝을 1.22 까지 늘린다. 1.06 에서 끊으면 셋째 구간이 75픽셀이라
# 「MI300X가 싸다」가 띠를 넘는다(2026-09-09)
_TLO, _THI = 0.70, 1.22
_TVAL = 560


def _tx(v):
    return _TX0 + _TXW * (v - _TLO) / (_THI - _TLO)


# (이름, 낮은 값, 높은 값) — 원문이 낸 손익분기 임대료를 H200 시세로 나눈 비율
_WORK = [('번역·대화 1k/1k', 0.76, 0.76),
         ('추론형 1k/4k', 0.84, 0.96),
         ('요약 4k/1k', 0.84, 0.96)]
_OWN, _RENT = 0.82, 1.00
_ZONE = [(_TLO, _OWN, '사도 빌려도', 'H200이 싸다'),
         (_OWN, _RENT, '사면 MI300X', '빌리면 H200'),
         (_RENT, _THI, '사도 빌려도', 'MI300X가 싸다')]
_ZY, _ROWY, _ROWSTEP = 52, 126, 40


def _zone(i):
    """구간 띠와 그 구간의 결론. 가운데 구간만 짙게 — 답이 갈리는 자리다."""
    lo, hi, l1, l2 = _ZONE[i]
    x0, x1 = _tx(lo), _tx(hi)
    mid = (x0 + x1) / 2
    return ''.join([
        # 가운데 구간은 채우기를 짙게 하지 않는다 — 회색 위 회색 글자가 안 읽힌다
        # (2026-09-09). 채우기는 옅게 두고 테두리로 강조한다
        '<rect x="%.1f" y="%d" width="%.1f" height="34" rx="4" fill="%s" '
        'fill-opacity="%s" stroke="%s" stroke-width="%s"/>'
        % (x0, _ZY, x1 - x0, INK3, '.16' if i == 1 else '.07',
           INK if i == 1 else 'none', '1.8' if i == 1 else '0'),
        _t(mid, _ZY + 15, l1, 't-sm'),
        _t(mid, _ZY + 29, l2, 't-lab'),
    ])


def _work_row(i):
    name, lo, hi = _WORK[i]
    y = _ROWY + i * _ROWSTEP
    x1, x2 = _tx(lo), _tx(hi)
    col = INK if lo > _OWN else INK3
    mark = ('<circle cx="%.1f" cy="%d" r="7" fill="%s"/>' % (x1, y + 11, col)
            if lo == hi else
            '<rect x="%.1f" y="%d" width="%.1f" height="18" rx="3" fill="%s"/>'
            % (x1, y + 2, x2 - x1, col))
    return ''.join([
        _lt(20, y + 16, name, bold=False),
        mark,
        _lt(_TVAL, y + 16,
            '%.2f' % lo if lo == hi else '%.2f~%.2f' % (lo, hi), 't-sm', False),
    ])


_TICKS = (0.70, 0.80, 0.90, 1.00, 1.10)
_BOT = _ROWY + 3 * _ROWSTEP

FIG_THRESHOLD = _svg(W, 358, '문턱 둘이 축을 세 구간으로 나눈다', ''.join(
    [_lt(20, 26, 'MI300X 가 H200 대비 내는 처리량 — 오른쪽으로 갈수록 빠르다'),
     _lt(20, 44, 'H200 을 1 로 놓은 비율이다', 't-sm', False)]
    + [_zone(i) for i in range(3)]
    # 눈금은 띠 아래에서 시작해 마지막 줄까지
    + ['<path d="M%.1f %d V%d" stroke="var(--line)" stroke-width="1"/>'
       % (_tx(v), _ZY + 34, _BOT) for v in _TICKS]
    + ['<text x="%.1f" y="%d" text-anchor="middle" class="t-sm">%.2f</text>'
       % (_tx(v), _ZY + 48, v) for v in _TICKS]
    + [_work_row(i) for i in range(3)]
    # 문턱 둘. 어디서 나온 값인지를 선 아래에 바로 적는다
    + ['<path d="M%.1f %d V%d" stroke="%s" stroke-width="2.4"/>'
       % (_tx(_OWN), _ZY, _BOT, INK),
       _t(_tx(_OWN), _BOT + 18, '0.82', 't-lab'),
       _t(_tx(_OWN), _BOT + 34, '$1.34 ÷ $1.63', 't-sm'),
       _t(_tx(_OWN), _BOT + 48, '자기 TCO 비', 't-sm'),
       '<path d="M%.1f %d V%d" stroke="%s" stroke-width="1.6" '
       'stroke-dasharray="5 4"/>' % (_tx(_RENT), _ZY, _BOT, INK3),
       _t(_tx(_RENT), _BOT + 18, '1.00', 't-lab'),
       _t(_tx(_RENT), _BOT + 34, '$2.50 ÷ $2.50', 't-sm'),
       _t(_tx(_RENT), _BOT + 48, '임대료 비', 't-sm')]
))


# ── 토러스 도해 둘 ──────────────────────────────────────────────────────
# 판은 4×4 한 층인데 두 장을 나란히 둔다. 한 층만 그리면 칸의 수가 0~2 로 끝나
# 오른쪽 자리 이름(꼭짓점 3)과 안 맞물린다(2026-09-10 지적). 끝 층과 가운데 층을
# 같이 두면 0~3 이 다 나오고 자리 넷이 그대로 보인다.
_GC = 34                                   # 칸 크기
_GY = 92
_PANE = [(28, '끝 층 — z 가 격자 끝', 1), (196, '가운데 층 — z 가 안쪽', 0)]
_SPOTNAME = {3: '꼭짓점', 2: '모서리', 1: '면', 0: '안쪽'}


def _cell_k(r, c, zbump):
    """이 칸의 좌표 가운데 격자 끝에 걸린 축의 수. zbump 는 세 번째 축 몫."""
    return (r in (0, 3)) + (c in (0, 3)) + zbump


def _pane(x0, title, zbump):
    out = [_t(x0 + 2 * _GC, _GY - 12, title, 't-lab')]
    for r in range(4):
        for c in range(4):
            k = _cell_k(r, c, zbump)
            x, y = x0 + c * _GC, _GY + r * _GC
            out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" '
                       'fill="%s" fill-opacity="%s" stroke="%s" stroke-width="1.1"/>'
                       % (x, y, _GC - 5, _GC - 5, INK3, ('.03', '.10', '.20', '.34')[k],
                          INK3))
            out.append(_t(x + (_GC - 5) // 2, y + (_GC - 5) // 2 + 5, '%d' % k, 't-lab'))
    return ''.join(out)


def _spot_rows():
    out = []
    for i, k in enumerate((3, 2, 1, 0)):
        y = _GY + i * 34
        cop = 6 - 2 - k
        out.append(_lt(368, y + 12, '%d — %s' % (k, _SPOTNAME[k])))
        out.append(_lt(368, y + 28,
                       '구리 %d · 기판 2 · 광 %d' % (cop, k), 't-sm', False))
    return ''.join(out)


FIG_TPOS = _svg(W, 276, '칸에 적힌 수가 곧 그 칩의 광 연결 수다', ''.join([
    _lt(20, 30, '4×4×4 격자를 층 둘로 잘라 본 것 — 칸 안의 수는 격자 끝에 걸린 축의 수'),
    _lt(20, 48, '끝 층은 z 축이 이미 끝에 걸려 있어 수가 하나씩 크다', 't-sm', False),
    _pane(*_PANE[0]), _pane(*_PANE[1]), _spot_rows(),
    _box(20, 238, W - 40, 30,
         ['칩마다 연결은 여섯으로 같다. 무엇으로 잇느냐만 자리가 정한다']),
]))


# ── 격자를 키우면 부착률이 내려간다. 가로 순위 막대 ──────────────────────
_SC = [('2×2×2', 8, 3.00), ('4×4×4', 64, 1.50), ('4×4×8', 128, 1.25),
       ('8×8×8', 512, 0.75), ('16×16×16', 4096, 0.38)]
_SBX, _SBW, _SMAX = 190, 300, 3.0


def _sc_row(i):
    name, chips, rate = _SC[i]
    y = 66 + i * 40
    on = i == 1
    return ''.join([
        _lt(20, y + 20, name, bold=on),
        _lt(104, y + 20, format(chips, ',') + '장', 't-sm', False),
        '<rect x="%d" y="%d" width="%.1f" height="22" rx="3" fill="%s"/>'
        % (_SBX, y + 2, _SBW * rate / _SMAX, INK if on else INK3),
        _lt(int(_SBX + _SBW * rate / _SMAX) + 8, y + 20, '%.2f' % rate, 't-sm', on),
    ])


FIG_TSCALE = _svg(W, 288, '격자가 커질수록 칩 한 장에 붙는 트랜시버가 준다', ''.join(
    [_lt(20, 30, '칩 한 장당 광 트랜시버 수'),
     _lt(20, 48, '원문은 4×4×4 하나만 냈다. 나머지는 같은 규칙으로 우리가 낸 값이다',
         't-sm', False)]
    + [_sc_row(i) for i in range(5)]
    + [_box(20, 250, W - 40, 30,
            ['끝에 걸린 칩의 몫이 줄기 때문이다 — 4×4×4 는 88%, 16×16×16 은 33%'])]
))


# ── 지연 도해 둘 ────────────────────────────────────────────────────────
# 판은 요청 하나가 지나는 시간이다. 그 위에 세 값을 얹는다.
# 첫 칸은 길이를 모르는 자리다. 6% 로 그렸더니 30픽셀이라 아래 설명이 판 밖으로
# 나갔다(2026-09-10) — 칸을 넓히지 않고 설명을 판 아래 범례로 내린다
_LX0, _LXW, _LY = 24, 500, 78
_LSEG = [('?', 0.10, ''), ('토큰 1,000개를 한 톨씩', 0.90, '')]


def _lat_board():
    out, x = [], _LX0
    for i, (name, frac, note) in enumerate(_LSEG):
        w = _LXW * frac
        out.append('<rect x="%.1f" y="%d" width="%.1f" height="38" rx="5" fill="%s" '
                   'fill-opacity="%s" stroke="%s" stroke-width="1.4"/>'
                   % (x, _LY, w, INK3, '.10' if i == 0 else '.24', INK3))
        out.append(_t(x + w / 2, _LY + 24, name, 't-lab'))
        x += w
    out.append(_a(_LX0, _LY - 16, _LX0 + _LXW, _LY - 16))
    out.append(_t(_LX0 + _LXW / 2, _LY - 24, 'E2E 지연 150초', 't-lab'))
    return ''.join(out)


FIG_LAT = _svg(W, 308, '지연 하나를 쪼개면 대화 속도와 동시 요청이 나온다', ''.join([
    _lt(20, 30, '요청 하나가 지나는 시간 — 출력 1,000토큰, 지연 150초'),
    _lat_board(),
    _box(24, 150, W - 48, 50,
         ['토큰 사이 150ms → 대화 속도 초당 6.7토큰',
          '초당 1,000토큰 ÷ 요청당 1,000토큰 × 150초 → GPU 한 장이 150요청을 붙든다']),
    _legend(222, ['「?」는 첫 토큰까지 걸린 시간이다 — 원문이 안 밝혀 길이를 모른다',
                  '가로 길이는 시간이지 값의 크기가 아니다',
                  '「?」를 0 으로 놓고 계산했다 — 실제 값이 있으면 속도는 조금 빨라진다']),
]))


# ── 대화 속도 견주기. 가로 순위 막대 ────────────────────────────────────
_SPD = [('이 벤치마크의 150초 운영점', 6.7, 6.7, True),
        ('MI325X 가 낼 수 있는 범위', 13, 35, False),
        ('오픈라우터 중간 사업자', 35, 35, False),
        ('H200 이 낼 수 있는 범위', 30, 90, False)]
_SPX, _SPW, _SPMAX = 210, 320, 90.0


def _spd_row(i):
    name, lo, hi, on = _SPD[i]
    y = 66 + i * 40
    x1 = _SPX + _SPW * lo / _SPMAX
    x2 = _SPX + _SPW * hi / _SPMAX
    return ''.join([
        _lt(20, y + 20, name, bold=on),
        ('<circle cx="%.1f" cy="%d" r="8" fill="%s"/>' % (x1, y + 12, INK if on else INK3)
         if lo == hi else
         '<rect x="%.1f" y="%d" width="%.1f" height="20" rx="3" fill="%s"/>'
         % (x1, y + 2, x2 - x1, INK if on else INK3)),
        _lt(int(max(x2, x1)) + 12, y + 20,
            '%g' % lo if lo == hi else '%g~%g' % (lo, hi), 't-sm', on),
    ])


FIG_SPEED = _svg(W, 268, '벤치마크가 선 자리는 시장이 파는 속도보다 느리다', ''.join(
    [_lt(20, 30, '사용자가 받는 속도 — 초당 토큰'),
     _lt(20, 48, '위 하나만 우리가 계산했고 아래 셋은 원문이 글로 적은 값이다',
         't-sm', False)]
    + [_spd_row(i) for i in range(4)]
    + [_box(20, 230, W - 40, 30,
            ['초당 6.7토큰은 시장 중간의 다섯 분의 일이다'])]
))
