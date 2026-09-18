# -*- coding: utf-8 -*-
"""보고서 XPU 층의 도해 아홉. 색은 회색만(확정 규칙 S2).

프로세스 판을 먼저 세우고 그 위에 얹는다(확정 규칙, 2026-09-09). 이 층의 판은
에이전틱 요청 하나가 도는 다섯 마디다 — 라우터 · 미리 채우기 · 대화 기록 · 뽑아내기 ·
도구 실행. 좌표는 `_BOARD` 하나가 갖고 있고 도해마다 다시 찍지 않는다. 다음 턴으로
되돌아오는 화살표는 판 바깥 아래 레일로 돈다.

판 위에 남기는 글자는 이름과 값 라벨뿐이고, 설명이 붙을 자리에는 동그라미 번호만
얹는다. 그 번호는 판 아래 범례가 한 줄씩 푼다.

값은 전부 원문에 있는 것만 그린다 — 캡션이 라벨과 줄 번호를 댄다.
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'
NUM = '①②③④⑤⑥⑦⑧⑨⑩'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _mark(x, y, n):
    """동그라미 번호 하나. ① 자체가 동그라미라 테두리를 두르지 않는다."""
    return ('<circle cx="%d" cy="%d" r="10" fill="var(--paper)"/>%s'
            % (x, y, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    """판 아래 범례. 한 줄에 하나씩."""
    return ''.join(_lt(20, y + i * 21, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


# ── 판. 요청 하나가 도는 다섯 마디. FIG_BOARD·FIG_MEM·FIG_SPLIT 가 같이 쓴다 ─────
_BW, _BH, _BY = 112, 56, 46
_BGAP = 18
_BOARD = _row(5, _BY, _BH, _BW, _BGAP)
_BNAMES = [['라우터'], ['미리 채우기'], ['대화 기록'], ['뽑아내기'], ['도구 실행']]
_BOARD_BOT = _BY + _BH


def _board(accent=()):
    """다섯 마디 판. 상자 크기는 전부 같다."""
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(_BOARD, _BNAMES)):
        st, sw = (INK, 2.0) if i in accent else (INK3, 1.5)
        out.append(_box(x, y, w, h, lines, st, sw))
        if i:
            px = _BOARD[i - 1][0] + _BW
            out.append(_a(px, y + h // 2, x, y + h // 2))
    return ''.join(out)


def _back_rail(n, y=None):
    """마지막 마디에서 첫 마디로 되돌아오는 레일. 판 바깥 아래로 돈다."""
    yy = _BOARD_BOT + 30 if y is None else y
    x1 = _BOARD[4][0] + _BW // 2
    x0 = _BOARD[0][0] + _BW // 2
    return ''.join([
        '<path d="M%d %d V%d H%d V%d" class="flow" fill="none"/>'
        % (x1, _BOARD_BOT, yy, x0, _BOARD_BOT),
        _mark((x0 + x1) // 2, yy, n),
    ])


# ── 1. 답이 갈리는 축 다섯 ───────────────────────────────────────────────────
_AX = [('상호작용성', 'tok/s/user'), ('수 표현', 'FP8 · FP4'),
       ('묶음 크기', '8 · 72 · 9,216'), ('메모리', 'HBM · SRAM'), ('시점', '날짜')]

FIG_AXIS = _svg(W, 300, '같은 두 칩의 순위가 갈리는 다섯 자리', ''.join(
    [_box(190, 14, 260, 44, ['"A가 B보다 빠르다"'], INK, 2.0)]
    + [_a(250 + i * 0, 58, 0, 0) for i in ()]
    + [_a(320, 58, cell[0] + _BW // 2, 96) for cell in _row(5, 96, 62, _BW, _BGAP)]
    + [_box(x, y, w, h, [_AX[i][0], _AX[i][1]])
       for i, (x, y, w, h) in enumerate(_row(5, 96, 62, _BW, _BGAP))]
    + [_mark(_row(5, 96, 62, _BW, _BGAP)[i][0] + _BW - 16, 96 + 16, i + 1)
       for i in range(5)]
    + [_legend(192, ['체감 속도를 어디로 잡나 — 경계를 넘으면 앞뒤가 바뀐다',
                     '4비트 규격이 둘이고, 연산기가 아예 없는 칩도 있다',
                     '한 덩어리로 묶인 칩 수 — 큰 쪽이 유리한 구간이 따로 있다',
                     '가중치와 대화 기록이 들어갈 자리',
                     '같은 칩 값이 6주 만에 100배 움직인 해다']),
       ]))


# ── 2. 판 — 에이전틱 요청 하나가 도는 길 ────────────────────────────────────
FIG_BOARD = _svg(W, 290, '에이전틱 요청 하나가 도는 다섯 마디', ''.join([
    _board(),
    _mark(_BOARD[1][0] + _BW // 2, _BY - 16, 1),
    _mark(_BOARD[2][0] + _BW // 2, _BY - 16, 2),
    _mark(_BOARD[3][0] + _BW // 2, _BY - 16, 3),
    _back_rail(4),
    _legend(160, ['입력을 한꺼번에 계산해 넣는다 — 연산이 몰리는 마디',
                  '계산해 둔 것을 메모리에 쥔다 — 다음 턴이 여기서 그대로 꺼내 쓴다',
                  '토큰을 하나씩 뽑는다 — 메모리에서 읽어 오는 속도에 걸린다',
                  '도구가 3.84초쯤 돌고 그 결과가 붙어 다음 턴이 시작된다']),
]))


# ── 3. 상호작용성 경계 ──────────────────────────────────────────────────────
def _curve(x0, y0, x1, y1, sag, dash=False):
    return ('<path d="M%d %d Q%d %d %d %d" fill="none" class="flow" '
            'marker-end="none"%s/>'
            % (x0, y0, (x0 + x1) // 2, sag, x1, y1,
               ' style="stroke-dasharray:5 4"' if dash else ''))


FIG_CROSS = _svg(W, 300, '경계를 넘으면 앞뒤가 바뀐다', ''.join([
    '<path d="M70 40 V236 H600" stroke="var(--line)" stroke-width="1" fill="none"/>',
    _lt(20, 44, 'GPU당', 't-sm', False), _lt(20, 60, '처리량', 't-sm', False),
    _lt(520, 258, '사용자당 초당 토큰', 't-sm', False),
    _curve(80, 60, 430, 230, 130),
    _curve(80, 120, 560, 210, 150, dash=True),
    _lt(96, 52, 'GB200 NVL72'), _lt(96, 134, 'B200 여덟 장'),
    '<path d="M300 40 V236" stroke="var(--line)" stroke-width="1" '
    'style="stroke-dasharray:4 4"/>',
    '<path d="M404 40 V236" stroke="var(--line)" stroke-width="1" '
    'style="stroke-dasharray:4 4"/>',
    _t(300, 34, '60'), _t(404, 34, '130'),
    _mark(300, 150, 1), _mark(404, 150, 2),
    _legend(272, ['NVL72 가 B200 의 세 배 (2026-02)',
                  '이점이 사라지고 백만 토큰 값이 B200 보다 비싸진다 (2026-02)']),
]))


# ── 4. 한 덩어리로 묶인 칩 수 ───────────────────────────────────────────────
_DOM = [('구글 아이언우드', '9,216칩', 9216),
        ('AWS 트레이니움3 NL72x2', '144칩', 144),
        ('엔비디아 GB300 NVL72', '72장', 72),
        ('AWS 트레이니움3 NL32x2', '64칩', 64),
        ('AMD MI355X', '8장', 8)]


def _rank_row(i, name, val, frac, accent=False, y0=52, step=34, gx=250, gw=300):
    y = y0 + i * step
    col = INK if accent else INK3
    return ''.join([
        _lt(20, y + 17, '%d' % (i + 1), 't-sm', False),
        _lt(40, y + 17, name, 't-sm', False),
        '<rect x="%d" y="%d" width="%.1f" height="20" rx="3" fill="%s"/>'
        % (gx, y, max(frac * gw, 2), col),
        _lt(int(gx + max(frac * gw, 2)) + 8, y + 17, val),
    ])


import math

_DOM_MAX = math.log10(9216)
FIG_DOMAIN = _svg(W, 244, '한 덩어리로 묶인 칩 수', ''.join(
    [_lt(20, 32, '큰 것이 위 · 막대는 자릿수에 비례한다', 't-sm', False)]
    + [_rank_row(i, n, v, math.log10(k) / _DOM_MAX, accent=(i == 2))
       for i, (n, v, k) in enumerate(_DOM)]))


# ── 5. 판 위에 메모리를 얹는다 ──────────────────────────────────────────────
_MEMS = [('블랙웰 울트라 HBM3E', '288GB'), ('트레이니움3 HBM3E', '144GB'),
         ('HBM3E 12단 한 스택', '36GB'), ('세레브라스 WSE-3 SRAM', '44GB')]

FIG_MEM = _svg(W, 330, '대화 기록이 어느 마디에서 메모리를 먹나', ''.join(
    [_board(accent=(2, 3)),
     _mark(_BOARD[2][0] + _BW // 2, _BY - 16, 1),
     _mark(_BOARD[3][0] + _BW // 2, _BY - 16, 2),
     _a(_BOARD[2][0] + _BW // 2, _BOARD_BOT, _BOARD[2][0] + _BW // 2, _BOARD_BOT + 26),
     _lt(20, 26, '짙은 칸이 메모리를 먹는 마디', 't-sm', False)]
    + [_box(x, _BOARD_BOT + 28, w, 44, [_MEMS[i][0], _MEMS[i][1]])
       for i, (x, y, w, h) in enumerate(_row(4, 0, 44, 142, 12))]
    + [_legend(216, ['가중치와 대화 기록이 같은 메모리를 나눠 쓴다',
                     '메모리에서 읽어 오는 속도가 이 마디의 천장이다',
                     '아래 넷은 용량이고, 막대가 아니라 값 그대로 적었다'])]))


# ── 6. 최고점과 누적은 다른 값이다 ──────────────────────────────────────────
FIG_INTEG = _svg(W, 300, '어느 날의 최고점과 여섯 달의 합', ''.join([
    '<path d="M70 40 V220 H600" stroke="var(--line)" stroke-width="1" fill="none"/>',
    _lt(20, 44, '초당', 't-sm', False), _lt(20, 60, '토큰', 't-sm', False),
    _lt(500, 242, '2026년 2월 → 8월', 't-sm', False),
    '<path d="M80 150 L200 120 L320 112 L440 108 L560 110" fill="none" class="flow"/>',
    '<path d="M80 220 L240 216 L360 150 L470 74 L560 120" fill="none" class="flow" '
    'style="stroke-dasharray:5 4"/>',
    _lt(96, 142, 'B200'), _lt(240, 208, 'MI355X'),
    _mark(470, 62, 1), _mark(300, 96, 2), _mark(300, 186, 3),
    _t(470, 46, '4,081'),
    _legend(252, ['MI355X 최고점 — 7월, GPU당 초당 4,081토큰',
                  'B200 누적 GPU당 538억 토큰', 'MI355X 누적 GPU당 352억 토큰']),
]))


# ── 7. 메가와트당 토큰 처리량 ───────────────────────────────────────────────
_RANK = [('베라 루빈 NVL72', '5,940만', 59.4),
         ('GB300 Dynamo SGLang', '2,850만', 28.5),
         ('GB300 Dynamo TRT-LLM', '2,110만', 21.1),
         ('B200 SGLang', '695만', 6.95),
         ('B300 vLLM', '556만', 5.56),
         ('H200 Dynamo SGLang (8비트)', '226만', 2.26),
         ('MI355X SGLang', '201만', 2.01)]

FIG_RANK = _svg(W, 300, '메가와트당 초당 토큰 — 사용자당 100토큰 기준', ''.join(
    [_lt(20, 32, '큰 것이 위 · 막대 길이는 값에 비례한다 · 0에서 시작한다',
         't-sm', False)]
    + [_rank_row(i, n, v, k / 59.4, accent=(i == 0), step=33, gx=270, gw=250)
       for i, (n, v, k) in enumerate(_RANK)]))


# ── 8. 출시 당일 무엇이 돌았나 ──────────────────────────────────────────────
_D0 = [('엔비디아 CUDA', 1, '당일 정상'),
       ('화웨이 CANN', 1, '당일 정상'),
       ('엔비디아 TensorRT-LLM', 0, '9일째 반영'),
       ('AMD ROCm', 0, '한 달에 100배')]

FIG_DAY0 = _svg(W, 270, 'DeepSeek V4 출시 당일 돈 스택과 43일 뒤', ''.join(
    ['<path d="M250 36 V212" stroke="var(--line)" stroke-width="1"/>',
     '<path d="M560 36 V212" stroke="var(--line)" stroke-width="1"/>',
     _t(250, 28, '출시 당일'), _t(560, 28, '43일 뒤')]
    + [''.join([
        _lt(20, 62 + i * 40, n, 't-sm', False),
        '<rect x="250" y="%d" width="310" height="20" rx="3" fill="%s"/>'
        % (46 + i * 40, INK if ok else 'var(--line)'),
        _lt(268, 62 + i * 40, note, 't-sm', False) if ok else
        _lt(268, 62 + i * 40, note, 't-sm', False),
    ]) for i, (n, ok, note) in enumerate(_D0)]
    + [_legend(222, ['짙은 띠가 출시 당일부터 정상 동작한 스택이다',
                     '옅은 띠는 그날 못 돌았고 며칠에서 한 달 뒤 따라붙었다'])]))


# ── 9. 판을 둘로 나눠 서로 다른 칩에 맡긴다 ────────────────────────────────
FIG_SPLIT = _svg(W, 300, '미리 채우는 마디와 뽑아내는 마디를 다른 칩에 맡긴다', ''.join([
    _board(accent=(1, 3)),
    _mark(_BOARD[1][0] + _BW // 2, _BY - 16, 1),
    _mark(_BOARD[3][0] + _BW // 2, _BY - 16, 2),
    _a(_BOARD[1][0] + _BW // 2, _BOARD_BOT, _BOARD[1][0] + _BW // 2, _BOARD_BOT + 26),
    _a(_BOARD[3][0] + _BW // 2, _BOARD_BOT, _BOARD[3][0] + _BW // 2, _BOARD_BOT + 26),
    _box(_BOARD[1][0] - 26, _BOARD_BOT + 28, 164, 46,
         ['연산이 몰리는 마디', 'AWS 트레이니움 · GPU']),
    _box(_BOARD[3][0] - 26, _BOARD_BOT + 28, 164, 46,
         ['대역폭이 걸리는 마디', '세레브라스 웨이퍼']),
    _legend(206, ['입력을 한꺼번에 계산한다 — 연산 제약',
                  '토큰을 하나씩 뽑는다 — 메모리 대역폭 제약',
                  '두 마디의 자원 비율은 하드웨어를 발주하는 날 정해진다']),
]))
