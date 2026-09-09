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
_STAGE = [['① 사는 값', '자본지출'],
          ['② 매달 나가는 값', '운영비'],
          ['③ 헛돈 시간', '굿풋 손실'],
          ['④ 시간당 단가', 'GPU-시간']]


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
_IX, _IY, _IH = 20, 62, 30
_IBAR, _IBARW = 228, 244
_IMAX = 14_929_920


def _ibar(v):
    """막대 길이. 최대값이 나머지의 서른 배라 제곱근으로 눌러 세운다."""
    return _IBARW * (v / _IMAX) ** 0.5


def _item_row(i, name, val, billed):
    y = _IY + i * _IH
    v = float(val.replace(',', ''))
    col = INK3 if billed else INK
    return ''.join([
        _lt(_IX, y + 19, name, bold=False),
        '<rect x="%d" y="%d" width="%.1f" height="18" rx="2" fill="%s"/>'
        % (_IBAR, y + 4, max(_ibar(v), 2.0), col),
        _lt(int(_IBAR + max(_ibar(v), 2.0)) + 8, y + 18, '$' + val, 't-sm', False),
    ])


FIG_STACK = _svg(W, 386, '청구서에 찍히는 다섯 줄과 안 찍히는 세 줄', ''.join(
    [_lt(_IX, 30, '월 비용 항목'), _lt(_IBAR, 30, '금액 (막대는 제곱근 눈금)')]
    + [_item_row(i, *it) for i, it in enumerate(_ITEMS)]
    + [_vline(_IX + 4, 52, 62 + 5 * _IH),
       _lt(_IX + 12, 316, '위 다섯은 청구서에 찍힌다. 아래 셋은 안 찍힌다', 't-sm', False),
       _box(_IX, 328, W - 40, 44,
            ['굿풋 손실은 GPU 비용에만 붙는다. 저장·망·컨트롤 플레인에는 안 붙는다',
             '이 규칙은 표에 안 적혀 있고 결과 값에서 거꾸로 읽어야 나온다'])]
))


# ── 절 4. 고장 한 번이 몇 장의 시간을 먹나 ──────────────────────────────
# 곱해지는 대상이 다르다는 것이 이 그림의 전부다. 셋을 가로로 세우면 176픽셀 칸에
# 수식이 안 들어가 글자가 테두리를 넘는다(2026-09-09) — 세로로 쌓아 한 줄을 넓게 쓴다.
_MODE = [('차가운 예비', '작업 크기 × (인지 + 체크포인트/2 + 초기화 + 수리)',
          '4,096장이 통째로 멎는다', 4096),
         ('뜨거운 예비', '작업 크기 × (인지 + 체크포인트/2 + 초기화) + 폭발 반경 × 수리',
          '4,096장이 멎고 수리만 64장', 4096),
         ('고장 견딤', '작업 크기 × (인지 + 전환) + 폭발 반경 × 수리',
          '64장만 수리를 기다린다', 64)]
_MY, _MSTEP, _MW = 76, 74, 600
_MBX, _MBW = 430, 190          # 막대가 놓이는 자리


def _mode_row(i):
    name, formula, note, n = _MODE[i]
    y = _MY + i * _MSTEP
    on = (i == 2)
    return ''.join([
        _lt(20, y + 14, '%s — %s' % (name, note), bold=on),
        '<rect x="%d" y="%d" width="%.1f" height="14" rx="2" fill="%s"/>'
        % (_MBX, y + 2, _MBW * (n / 4096.0) ** 0.5, INK if on else INK3),
        _box(20, y + 22, _MW, 36, [formula], INK if on else INK3, 2.0 if on else 1.5),
    ])


FIG_GOODPUT = _svg(W, 392, '같은 고장인데 곱해지는 장수가 예순네 배 다르다', ''.join(
    [_lt(20, 30, '고장 한 번 → 잃는 GPU-시간'),
     _lt(20, 52, '클러스터 5,184장 · 평균 작업 4,096장 · 폭발 반경 64장 (그림 019)',
         't-sm', False)]
    + [_mode_row(i) for i in range(3)]
    + [_legend(316, ['위 둘은 작업 전체가 멎는다 — 체크포인트 이후 계산이 날아간다',
                     '아래는 작업이 계속 돈다 — 고장 난 랙 하나만 수리를 기다린다',
                     '막대는 수리 시간에 곱해지는 장수, 제곱근 눈금이다'])]
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
    out.append(_t(x3 + w3 // 2, y3 + 20, '③ 헛돈 시간', 't-lab'))
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
# 가로 축은 H200 대비 처리량 비율 하나뿐이다. 문턱 둘을 세로선으로 세우고
# 작업 셋의 실측 구간을 그 위에 얹는다.
_TX0, _TXW = 130, 420
_TLO, _THI = 0.70, 1.05


def _tx(v):
    return _TX0 + _TXW * (v - _TLO) / (_THI - _TLO)


_WORK = [('번역·대화 1k/1k', 0.76, 0.76),
         ('추론형 1k/4k', 0.84, 0.96),
         ('요약 4k/1k', 0.84, 0.96)]


def _work_row(i):
    y = 96 + i * 46
    name, lo, hi = _WORK[i]
    x1, x2 = _tx(lo), _tx(hi)
    win = lo > 0.82
    return ''.join([
        _lt(20, y + 18, name, bold=False),
        '<rect x="%.1f" y="%d" width="%.1f" height="20" rx="3" fill="%s"/>'
        % (x1, y + 2, max(x2 - x1, 5.0), INK if win else INK3),
        _lt(int(x2) + 10, y + 18,
            '%.2f' % lo if lo == hi else '%.2f~%.2f' % (lo, hi), 't-sm', False),
    ])


FIG_THRESHOLD = _svg(W, 306, '문턱 0.82를 넘느냐로 소유의 답이 갈린다', ''.join(
    [_lt(20, 30, 'MI300X 의 H200 대비 처리량'),
     _lt(20, 52, '가로축은 H200 을 1 로 놓은 비율이다', 't-sm', False)]
    + ['<path d="M%.1f 64 V236" stroke="var(--line)" stroke-width="1"/>' % _tx(v)
       for v in (0.70, 0.80, 0.90, 1.00)]
    + ['<text x="%.1f" y="80" text-anchor="middle" class="t-sm">%.2f</text>' % (_tx(v), v)
       for v in (0.70, 0.80, 0.90, 1.00)]
    + [_work_row(i) for i in range(3)]
    # 문턱 둘 — 사는 값과 빌리는 값
    + ['<path d="M%.1f 88 V236" stroke="%s" stroke-width="2"/>' % (_tx(0.82), INK),
       _t(_tx(0.82), 250, '사서 쓸 때 문턱 0.82', 't-lab'),
       '<path d="M%.1f 88 V236" stroke="%s" stroke-width="1.5" '
       'stroke-dasharray="5 4"/>' % (_tx(1.00), INK3),
       _t(_tx(1.00), 250, '빌릴 때 문턱 1.00', 't-lab'),
       _box(20, 258, W - 40, 44,
            ['왼쪽 문턱은 우리가 자기 TCO 로 계산한 것이고 원문에는 없다',
             '가로 막대의 값은 원문이 낸 손익분기 임대료를 뒤집어 낸 비율이다'])]
))
