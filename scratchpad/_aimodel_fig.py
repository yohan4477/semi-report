# -*- coding: utf-8 -*-
"""보고서 AI 모델 층의 도해 여덟. 색은 회색만(확정 규칙 S2).

판에 남기는 글자는 이름과 값 라벨뿐이고, 설명이 붙을 자리에는 동그라미 번호만 얹는다.
그 번호는 판 아래 범례가 한 줄씩 푼다. 값은 전부 원문에 있는 것만 그리고, 캡션이
라벨과 줄 번호를 댄다(_aimodel_part1.CAPTION).

부품은 XPU 층과 같은 것을 쓴다 — 여기서 다시 짜면 한쪽만 고쳐진다.
"""
import _xpu_fig as xf

_svg, _box, _a, _lt, _row = xf._svg, xf._box, xf._a, xf._lt, xf._row
_t, _mark, _legend, _rank_row = xf._t, xf._mark, xf._legend, xf._rank_row
W = xf.W
INK, INK3 = xf.INK, xf.INK3
LINE = 'var(--line)'


def _rect(x, y, w, h, fill, stroke='none'):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s" stroke="%s"/>'
            % (x, y, w, h, fill, stroke))


# ── 1. 전문가 혼합 — GLM-5 의 256 중 8 + 공유 1 ─────────────────────────────
# 짙은 칸의 자리는 보기용이다. 개수(256 · 8 · 1)만 원문 값이다.
_GX, _GY, _CELL, _GAP = 232, 56, 11, 3
_HOT = {18, 53, 77, 120, 141, 186, 203, 247}


def _grid():
    out = []
    for i in range(256):
        r, c = divmod(i, 16)
        x, y = _GX + c * (_CELL + _GAP), _GY + r * (_CELL + _GAP)
        out.append(_rect(x, y, _CELL, _CELL, INK if i in _HOT else LINE))
    return ''.join(out)


_GW = 16 * (_CELL + _GAP) - _GAP          # 격자 폭 221
_GMID = _GY + _GW // 2

FIG_MOE = _svg(W, 380, '전문가 256개 중 8개와 공유 전문가 1개 — GLM-5', ''.join([
    _box(20, _GMID - 70, 150, 44, ['토큰 하나']),
    _box(20, _GMID + 26, 150, 44, ['라우터']),
    _a(95, _GMID - 26, 95, _GMID + 26),
    _a(170, _GMID + 48, _GX - 10, _GMID + 48),
    _grid(),
    _lt(_GX, _GY - 12, '라우팅 전문가 256', 't-sm', False),
    _box(_GX + _GW + 30, _GY, 120, 44, ['공유 전문가 1']),
    _box(_GX + _GW + 30, _GY + _GW - 44, 120, 44, ['가중합']),
    '<path d="M%d %d H%d V%d H%d" class="flow" fill="none"/>'
    % (_GX + _GW + 4, _GMID, _GX + _GW + 16, _GY + _GW - 22, _GX + _GW + 30),
    _a(_GX + _GW + 90, _GY + 44, _GX + _GW + 90, _GY + _GW - 44),
    _mark(_GX - 26, _GMID + 30, 1),
    _mark(_GX + _GW + 90, _GY + 70, 2),
    _mark(_GX + _GW + 90, _GY + _GW + 18, 3),
    _legend(306, ['라우터가 토큰마다 256개 중 8개를 고른다 (짙은 칸)',
                  '공유 전문가는 모든 토큰이 거친다',
                  '고른 전문가 출력과 공유 전문가 출력을 더해 다음 층으로 넘긴다']),
]))


# ── 2. 어텐션 계보 — 세 갈래 ─────────────────────────────────────────────────
_CW, _CH, _CS = 190, 46, 22
_CX = [20, 225, 430]


def _col(ci, y0, items, accent=None):
    out = []
    x = _CX[ci]
    for i, lines in enumerate(items):
        y = y0 + i * (_CH + _CS)
        st, sw = (INK, 2.0) if accent == i else (INK3, 1.5)
        out.append(_box(x, y, _CW, _CH, lines, st, sw))
        if i:
            out.append(_a(x + _CW // 2, y - _CS, x + _CW // 2, y))
    return ''.join(out)


_ROOT_Y, _COL_Y = 14, 112
FIG_ATTN = _svg(W, 470, 'full attention 에서 갈라진 세 갈래', ''.join([
    _box(225, _ROOT_Y, _CW, _CH, ['full attention']),
    '<path d="M320 %d V%d H115 V%d" class="flow" fill="none"/>'
    % (_ROOT_Y + _CH, _ROOT_Y + _CH + 26, _COL_Y),
    _a(320, _ROOT_Y + _CH, 320, _COL_Y),
    '<path d="M320 %d V%d H525 V%d" class="flow" fill="none"/>'
    % (_ROOT_Y + _CH, _ROOT_Y + _CH + 26, _COL_Y),
    _col(0, _COL_Y, [['MLA', 'DeepSeek V2 · 2024-05'],
                     ['DSA', 'DeepSeek V3.2 · GLM-5'],
                     ['CSA · HCA', 'DeepSeek V4']]),
    _col(1, _COL_Y, [['선형 어텐션'], ['DeltaNet'], ['Gated DeltaNet'],
                     ['KDA', 'Kimi K3']]),
    _col(2, _COL_Y, [['청크 어텐션', 'Llama 4 Behemoth']]),
    _mark(_CX[0] + _CW - 14, _COL_Y - 12, 1),
    _mark(_CX[1] + _CW - 14, _COL_Y - 12, 2),
    _mark(_CX[2] + _CW - 14, _COL_Y - 12, 3),
    _legend(398, ['토큰당 KV 를 압축하고, 읽을 토큰을 고른다',
                  '상태 크기를 고정한다 — 단계마다 잊는 법을 고쳤다',
                  '계산 범위를 블록으로 자른다']),
]))


# ── 3. Engram — 토큰 ID 로 표에서 꺼낸다 ─────────────────────────────────────
_EW, _EH, _EY, _EGAP = 104, 54, 50, 20
_E = _row(5, _EY, _EH, _EW, _EGAP)
_ENAMES = [['토큰 ID'], ['2·3·4토큰', '접미 해시'], ['표 조회'], ['게이트'], ['잔차 흐름']]


def _echain(accent=()):
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(_E, _ENAMES)):
        st, sw = (INK, 2.0) if i in accent else (INK3, 1.5)
        out.append(_box(x, y, w, h, lines, st, sw))
        if i:
            out.append(_a(_E[i - 1][0] + _EW, y + h // 2, x, y + h // 2))
    return ''.join(out)


_TX = _E[2][0] + _EW // 2
FIG_ENGRAM = _svg(W, 310, 'Engram 조회 — DeepSeek-V4.1-Flash', ''.join([
    _echain(accent=(2,)),
    _a(_TX, _EY + _EH, _TX, _EY + _EH + 34),
    _box(_TX - 170, _EY + _EH + 36, 212, 54, ['호스트 DRAM 의 표', '약 196.6B 파라미터 · 188.8 GiB']),
    _box(_TX + 58, _EY + _EH + 36, 200, 54, ['토큰 위치당 읽는 양', '24행 × 2층 · 약 12.4 KiB']),
    _mark(_E[1][0] + _EW // 2, _EY - 16, 1),
    _mark(_TX, _EY - 16, 2),
    _mark(_E[3][0] + _EW // 2, _EY - 16, 3),
    _legend(226, ['주소가 은닉 상태가 아니라 토큰 ID 로 정해져 앞 층 계산 중에 미리 가져온다',
                  '표는 HBM 밖에 둔다 — 층 1 과 14 두 곳',
                  '문맥과 어긋난 조회는 게이트가 누른다']),
]))


# ── 4. MFU — 학습 일곱 건 ────────────────────────────────────────────────────
_MFU = [('GPT-3 175B · H100 128장 · BF16', '54%', 54),
        ('Llama 3 405B · H100 2,304장 · BF16', '약 54%', 54),
        ('Llama 3 405B 실제 · H100 16k장 · BF16', '41%', 41),
        ('같은 모델 컨텍스트 131,072 · BF16', '38%', 38),
        ('Llama 3 70B · H100 2,048장 · FP8', '35.5%', 35.5),
        ('DeepSeek 670B MoE · H100 · BF16', '16.6%', 16.6),
        ('RL 학습기 · Qwen3-235B · H200 64장', '10.5%', 10.5)]

FIG_MFU = _svg(W, 300, '학습 일곱 건의 MFU', ''.join(
    [_lt(20, 32, '큰 것이 위 · 막대 길이는 값에 비례한다 · 0에서 시작한다', 't-sm', False)]
    + [_rank_row(i, n, v, k / 54, accent=(i == 5), step=33, gx=330, gw=230)
       for i, (n, v, k) in enumerate(_MFU)]))


# ── 5. RL 루프 판 ────────────────────────────────────────────────────────────
_RW, _RH, _RY, _RGAP = 118, 56, 50, 34
_R = _row(4, _RY, _RH, _RW, _RGAP)
_RNAMES = [['생성기'], ['RL 환경'], ['큐'], ['학습기']]
_RBOT = _RY + _RH


def _rboard(accent=()):
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(_R, _RNAMES)):
        st, sw = (INK, 2.0) if i in accent else (INK3, 1.5)
        out.append(_box(x, y, w, h, lines, st, sw))
        if i:
            out.append(_a(_R[i - 1][0] + _RW, y + h // 2, x, y + h // 2))
    return ''.join(out)


_RX0, _RX3 = _R[0][0] + _RW // 2, _R[3][0] + _RW // 2
FIG_RLLOOP = _svg(W, 300, 'RL 학습 한 걸음 — 생성기 · 환경 · 큐 · 학습기', ''.join([
    _rboard(),
    _mark((_R[0][0] + _RW + _R[1][0]) // 2, _RY - 16, 1),
    _mark((_R[1][0] + _RW + _R[2][0]) // 2, _RY - 16, 2),
    _mark((_R[2][0] + _RW + _R[3][0]) // 2, _RY - 16, 3),
    '<path d="M%d %d V%d H%d V%d" class="flow" fill="none"/>'
    % (_RX3, _RBOT, _RBOT + 36, _RX0, _RBOT),
    _mark((_RX0 + _RX3) // 2, _RBOT + 36, 4),
    _legend(176, ['프롬프트로 롤아웃을 만들며 환경과 주고받는다',
                  '환경이 보상을 매긴 샘플을 큐에 넣는다',
                  '학습기가 큐에서 샘플을 꺼내 한 걸음 학습한다',
                  '새 가중치를 생성기에 밀어 넣는다 — 롤아웃이 끝나기 전에도']),
]))


# ── 6. RL 실험 네 번 — 학습기가 기다린 비율 ─────────────────────────────────
_BASE, _TOP = 220, 50                      # 100% 가 _TOP, 0% 가 _BASE
_CASE = [('사례 1', 30, None), ('사례 2', 74, None), ('사례 3', 30, 60), ('사례 4', 60, None)]


def _vy(v):
    return _BASE - (_BASE - _TOP) * v / 100.0


def _vbar(i, label, lo, hi):
    x = 110 + i * 120
    out = ['<rect x="%d" y="%.1f" width="64" height="%.1f" rx="3" fill="%s"/>'
           % (x, _vy(lo), _BASE - _vy(lo), INK3)]
    txt = '%d%%' % lo
    if hi:
        out.append('<rect x="%d" y="%.1f" width="64" height="%.1f" rx="3" fill="%s"/>'
                   % (x, _vy(hi), _vy(lo) - _vy(hi), LINE))
        txt = '%d~%d%%' % (lo, hi)
    out.append(_t(x + 32, int(_vy(hi or lo)) - 8, txt, 't-lab'))
    out.append(_t(x + 32, _BASE + 20, label))
    return ''.join(out)


FIG_RLCASE = _svg(W, 270, 'RL 실험 네 번에서 학습기가 기다린 시간 비율', ''.join(
    ['<path d="M80 %d H600" stroke="var(--line)" stroke-width="1"/>' % _BASE,
     _lt(20, _TOP + 4, '100%', 't-sm', False), _lt(30, _BASE + 4, '0%', 't-sm', False),
     '<path d="M80 %d H600" stroke="var(--line)" stroke-width="1" '
     'style="stroke-dasharray:4 4"/>' % _TOP]
    + [_vbar(i, n, lo, hi) for i, (n, lo, hi) in enumerate(_CASE)]
    + [_lt(20, 262, '사례 3 은 범위 — 옅은 위 끝이 60%', 't-sm', False)]))


# ── 7. 추론 네 영역 ──────────────────────────────────────────────────────────
_QW, _QH, _QY, _QGAP = 128, 54, 50, 26
_Q = _row(4, _QY, _QH, _QW, _QGAP)
_QNAMES = [['프리필'], ['미드필'], ['디코드', '어텐션'], ['디코드', '전문가']]
_QNECK = [['연산'], ['KV 읽기 +', '전문가 트래픽'], ['KV 이동'], ['전문가', '가중치 적재']]

FIG_REGIONS = _svg(W, 300, '추론의 네 운영 영역과 각 병목', ''.join(
    [_box(x, y, w, h, n) for (x, y, w, h), n in zip(_Q, _QNAMES)]
    + [_a(_Q[i - 1][0] + _QW, _QY + _QH // 2, _Q[i][0], _QY + _QH // 2) for i in range(1, 4)]
    + [_a(x + _QW // 2, _QY + _QH, x + _QW // 2, _QY + _QH + 30) for (x, y, w, h) in _Q]
    + [_box(x, _QY + _QH + 32, w, 50, n) for (x, y, w, h), n in zip(_Q, _QNECK)]
    + [_mark(_Q[1][0] + _QW // 2, _QY - 16, 1), _mark(_Q[2][0] + _QW // 2, _QY - 16, 2)]
    + [_lt(20, 32, '위는 영역, 아래는 그 영역의 병목', 't-sm', False),
       _legend(226, ['캐시된 긴 문맥 뒤에 새 입력이 붙는다 — 연산 강도가 바이트당 수천 연산까지',
                     '쿼리마다 자기 문맥을 읽어 묶어도 연산 강도가 그대로다'])]))


# ── 8. 격차가 닫히는 데 걸린 개월 ───────────────────────────────────────────
_GBASE, _GTOP = 220, 60                    # 10개월이 _GTOP
_GAPS = [('초기 스케일링', None, ''), ('추론', 8.5, 'R1-0528'),
         ('에이전트', 4.8, 'Kimi K2.6'), ('에이전트', 6, 'GLM-5.2')]


def _gy(v):
    return _GBASE - (_GBASE - _GTOP) * v / 10.0


def _gbar(i, era, v, model):
    x = 100 + i * 124
    out = [_t(x + 32, _GBASE + 20, era), _t(x + 32, _GBASE + 38, model, 't-sm')]
    if v is None:
        out.append(_t(x + 32, _GBASE - 12, '원문에 없음', 't-sm'))
    else:
        out.append('<rect x="%d" y="%.1f" width="64" height="%.1f" rx="3" fill="%s"/>'
                   % (x, _gy(v), _GBASE - _gy(v), INK if i == 2 else INK3))
        out.append(_t(x + 32, int(_gy(v)) - 8, ('%g개월' % v), 't-lab'))
    return ''.join(out)


FIG_GAP = _svg(W, 280, '오픈 모델이 그 시대 첫 클로즈드 모델을 따라잡는 데 걸린 개월', ''.join(
    ['<path d="M80 %d H600" stroke="var(--line)" stroke-width="1"/>' % _GBASE,
     _lt(20, 32, '막대 높이는 개월 수에 비례한다 · 0에서 시작한다', 't-sm', False)]
    + [_gbar(i, e, v, m) for i, (e, v, m) in enumerate(_GAPS)]))
