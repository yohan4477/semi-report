# -*- coding: utf-8 -*-
"""데이터센터 자본지출 층 넷의 도해. 색은 회색만(확정 규칙 S2).

판을 먼저 세우고 그 위에 얹는다. 이 층의 판은 「MW당 자본이 매출로 회수되는
사슬」 하나다 — 짓는 값 · 빌린 값 · 파는 값 · 남는 값. 네 글이 그 사슬의 서로
다른 마디를 판다. 좌표는 `_RAIL` 이 갖고 있고 도해마다 다시 찍지 않는다.

화살표 설명은 판 위에 안 얹고 아래 범례로 내린다. 동그라미 번호는 한 겹이다.
값은 원문에 글로 있는 것과 우리 모델이 낸 것만 그린다 — 캡션이 어느 쪽인지 밝힌다.
"""
import _biz_fig as bf
from _mathtree import _node, tree_svg

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'
NUM = '①②③④⑤⑥⑦⑧⑨'
_W4 = [118, 126, 130, 116]


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _mark(x, y, n):
    """판 위 동그라미 번호. ①이 이미 동그라미라 테두리를 또 두르지 않는다."""
    return ('<circle cx="%d" cy="%d" r="10" fill="var(--paper)"/>%s'
            % (x, y, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    """판 아래 범례. 한 줄에 하나씩."""
    return ''.join(_lt(20, y + i * 21, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


def _hbar(x, y, w, h, filled=True):
    """가로 막대 하나. 짙은 칸과 옅은 칸 둘뿐이라 색은 안 늘린다."""
    return ('<rect x="%d" y="%d" width="%.1f" height="%d" fill="%s" '
            'stroke="var(--ink-3)" stroke-width="1"/>'
            % (x, y, max(w, 0.5), h, 'var(--ink-2)' if filled else 'var(--paper)'))


# ── 판. 짓는 값이 매출로 돌아오는 네 마디 ────────────────────────────────
_RAIL = _row(4, 44, 48, 138, gap=12)
_RAIL_NAME = [['짓는 값', 'MW당 자본지출'], ['빌린 값', '금리·담보'],
              ['파는 값', 'MW당 연 매출'], ['남는 값', '회수 기간']]


def _board(accent=()):
    out = []
    for i, (x, y, w, h) in enumerate(_RAIL):
        st, sw = ((INK, 1.8) if i in accent else (INK3, 1.4))
        out.append(_box(x, y, w, h, _RAIL_NAME[i], st, sw))
        if i:
            px = _RAIL[i - 1][0] + _RAIL[i - 1][2]
            out.append(_a(px, y + h // 2, x, y + h // 2))
    return ''.join(out)


# ── ① 레고. 발표된 차이 110만 달러를 항으로 가른다 ────────────────────────
def _lego_split():
    x0, top, bh, gap = 150, 128, 30, 22
    full = 340.0                       # 110만 달러가 이 길이다
    rows = [('발표된 차이', 1.10, '$1,100,000', 0),
            ('인건비로 설명', 0.225, '$225,000', 1),
            ('설명 안 되는 몫', 0.875, '$875,000', 2)]
    out = [_board(accent=(0,)),
           _lt(20, 112, 'MW당 총원가 차이를 무엇이 만드나', 't-lab', False)]
    for i, (name, v, lab, mark) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 20, name, 't-sm', False))
        out.append(_hbar(x0, y, full * v / 1.10, bh, filled=(i != 2)))
        out.append(_lt(x0 + full * v / 1.10 + 8, y + 20, lab, 't-sm', False))
        if mark:
            out.append(_mark(x0 + 22, y + bh // 2, mark))
    out.append(_legend(top + 3 * (bh + gap) + 4, [
        '현장 인시가 12,000에서 4,500시간으로 줄어 아끼는 몫',
        '공기가 짧아져 에스컬레이션·컨틴전시·현장관리비가 주는 몫',
    ]))
    return ''.join(out)


FIG_LEGOSPLIT = _svg(W, 330, '아끼는 110만 달러 가운데 인건비는 5분의 1이다',
                     _lego_split())


# ── ② 지상. 층이 올라갈수록 MW당 자본이 매출을 먹는다 ─────────────────────
def _ground_layers():
    x0, top, bh, gap = 172, 128, 26, 16
    full, top_v = 300.0, 22.3
    rows = [('산업 생산 확충', 22.3, '$20백만 이상'),
            ('배후 자체발전', 22.3, '$15~20백만'),
            ('계통 연결', 16.7, '$12~15백만'),
            ('전환·유휴 부지', 16.7, '$10~15백만')]
    out = [_board(accent=(0, 2)),
           _lt(20, 112, '연 자본비가 MW당 연 매출에서 먹는 몫 (상한 기준)',
               't-lab', False)]
    for i, (name, pct, cap) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 18, '%s %s' % (NUM[i], name), 't-sm', False))
        out.append(_hbar(x0, y, full * pct / top_v, bh, filled=(i < 2)))
        out.append(_lt(x0 + full * pct / top_v + 8, y + 18,
                       '%.1f%%   %s' % (pct, cap), 't-sm', False))
    y = top + 4 * (bh + gap) + 10
    out.append(_lt(20, y, '순위는 먹는 몫이 큰 것부터다. 매출은 MW당 연 1,200만 달러로 세웠다.',
                   't-sm', False))
    out.append(_lt(20, y + 21, '나머지로 GPU 값과 전기값과 사람 값을 다 대야 한다.',
                   't-sm', False))
    return ''.join(out)


FIG_GRDLAYER = _svg(W, 352, '전력을 어렵게 끌어올수록 자본이 매출을 더 먹는다',
                    _ground_layers())


# ── ③ 트리니티. 청구가 한 줄이 셋으로 갈린다 ──────────────────────────────
def _trinity_split():
    x0, top, bh = 130, 130, 40
    full = 380.0
    charge, floor, nvda, neo = 6.75, 3.68, 1.23, 1.84
    out = [_board(accent=(1,)),
           _lt(20, 114, 'GPU 한 장·한 시간에 붙는 값 (1년차)', 't-lab', False)]
    out.append(_lt(20, top + 26, '청구가', 't-sm', False))
    w1 = full * floor / charge
    w2 = full * nvda / charge
    w3 = full * neo / charge
    out.append(_hbar(x0, top, w1, bh, True))
    out.append(_hbar(x0 + w1, top, w2, bh, False))
    out.append(_hbar(x0 + w1 + w2, top, w3, bh, True))
    out.append(_t(x0 + w1 / 2, top + 25, '$3.68'))
    out.append(_t(x0 + w1 + w2 / 2, top + 25, '$1.23'))
    out.append(_t(x0 + w1 + w2 + w3 / 2, top + 25, '$1.84'))
    out.append(_lt(x0 + full + 8, top + 26, '$6.75', 't-sm', False))
    out.append(_mark(x0 + w1, top + bh + 16, 1))
    out.append(_mark(x0 + w1 + w2, top + bh + 16, 2))
    y2 = top + bh + 42
    out.append(_lt(20, y2, '네오클라우드가 실현하는 값 $5.52 = $3.68 + $1.84',
                  't-sm', False))
    out.append(_lt(20, y2 + 21, '엔비디아가 가져가는 몫 $1.23 은 청구가의 18.2%다',
                  't-sm', False))
    out.append(_legend(y2 + 48, [
        '바닥값. 임대가 이 아래로 떨어져도 엔비디아가 여기까지 채워 준다',
        '바닥값 위 초과분 $3.07 을 40대 60으로 나눈 자리',
    ]))
    return ''.join(out)


FIG_TRSPLIT = _svg(W, 330, '바닥값을 깔아 준 대가로 초과분의 40퍼센트를 가져간다',
                   _trinity_split())


# ── ④ 스페이스X. 파는 값마다 회수가 몇 해인가 ─────────────────────────────
def _payback():
    x0, top, bh, gap = 190, 126, 22, 26
    full, top_v = 300.0, 3.57
    rows = [('지금 임대되는 값 $14M', 3.57, 25.00),
            ('프리미엄 하한 $30M', 1.67, 2.78),
            ('프리미엄 상한 $50M', 1.00, 1.32),
            ('API 추론 $100M', 0.50, 0.57)]
    out = [_board(accent=(2, 3)),
           _lt(20, 110, '자본 $50백만/MW 를 갚는 데 걸리는 햇수', 't-lab', False)]
    for i, (name, rev_y, cash_y) in enumerate(rows):
        y = top + i * (bh * 2 + gap)
        out.append(_lt(20, y + 16, name, 't-sm', False))
        out.append(_hbar(x0, y, full * min(rev_y, top_v) / top_v, bh - 4, True))
        out.append(_lt(x0 + full * min(rev_y, top_v) / top_v + 8, y + 16,
                       '매출 기준 %.2f년' % rev_y, 't-sm', False))
        w = full * min(cash_y, top_v) / top_v
        out.append(_hbar(x0, y + bh, w, bh - 4, False))
        out.append(_lt(x0 + w + 8, y + bh + 16,
                       '현금 기준 %s' % ('%.2f년' % cash_y if cash_y < 10
                                     else '%.0f년 (축 밖)' % cash_y),
                       't-sm', False))
    y = top + 4 * (bh * 2 + gap) + 4
    out.append(_mark(x0 - 26, top + 2 * (bh * 2 + gap) + 18, 1))
    out.append(_legend(y, [
        '원문이 「1년 안에 회수한다」고 적은 자리. 매출 기준으로 딱 1.00년이고 현금 기준은 1.32년이다',
    ]))
    return ''.join(out)


FIG_SXPAY = _svg(W, 430, '회수 1년은 비용을 빼기 전의 값이다', _payback())


# ── math tree 넷 ─────────────────────────────────────────────────────────
FIG_EQ_LEGO = tree_svg(
    'MW당 총원가 차이는 어떤 항으로 쪼개지나', _W4,
    _node(['MW당 총원가', '차이'], '+', [
        _node(['인건비 차이'], '−', [
            _node(['현장 인시', '× 현장 임금']),
            _node(['남은 인시', '× 현장 임금']),
            _node(['옮긴 인시', '× 공장 임금']),
        ]),
        _node(['공기가 주는 몫'], '←', [
            _node(['에스컬레이션']),
            _node(['컨틴전시']),
            _node(['현장관리비']),
        ]),
    ]),
    marks=(('옮긴 인시', 1),))

FIG_EQ_GRD = tree_svg(
    '연 자본비는 어떤 항으로 쪼개지나', _W4,
    _node(['MW당 연 자본비'], '×', [
        _node(['MW당 자본지출'], '←', [
            _node(['전력을 끄는 층']),
        ]),
        _node(['자본회수계수'], '←', [
            _node(['가중평균', '자본비용']),
            _node(['자산 수명']),
        ]),
    ]),
    marks=(('전력을 끄는 층', 1), ('자본회수계수', 2)))

FIG_EQ_TRN = tree_svg(
    '네오클라우드가 실현하는 값은 어떤 항으로 쪼개지나', _W4,
    _node(['실현 단가'], '+', [
        _node(['백스톱 바닥값']),
        _node(['초과분의 몫'], '×', [
            _node(['청구가', '− 바닥값']),
            _node(['1 − 엔비디아', '배분율']),
        ]),
    ]),
    marks=(('백스톱 바닥값', 1), ('1 − 엔비디아', 2)))

FIG_EQ_SX = tree_svg(
    '회수 기간은 어떤 항으로 쪼개지나', _W4,
    _node(['회수 기간'], '÷', [
        _node(['MW당 자본지출'], '←', [
            _node(['GW당 자본지출']),
        ]),
        _node(['한 해에 갚는 돈'], '−', [
            _node(['MW당 연 매출']),
            _node(['MW당 연 비용']),
        ]),
    ]),
    marks=(('MW당 연 비용', 1),))

# ── ⑤ 다리. 같은 해를 네 자로 재면 ────────────────────────────────────────
def _gw_ways():
    x0, top, bh, gap = 210, 126, 26, 18
    full, top_v = 300.0, 30.2
    rows = [('엑셀의 칩 수로', 30.2, False, 1),
            ('시설 단가 하한으로', 28.8, True, 0),
            ('우리 IT 단가로', 19.7, True, 0),
            ('전부 포함 단가로', 14.7, True, 0),
            ('시설 단가 상한으로', 14.4, True, 0)]
    out = [_board(accent=(0, 3)),
           _lt(20, 112, '2026년 빅4 자본지출 7,325억 달러가 몇 기가와트인가',
               't-lab', False)]
    for i, (name, v, filled, mark) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 18, name, 't-sm', False))
        out.append(_hbar(x0, y, full * v / top_v, bh, filled))
        out.append(_lt(x0 + full * v / top_v + 8, y + 18, '%.1fGW' % v, 't-sm', False))
        if mark:
            out.append(_mark(x0 + 24, y + bh // 2, mark))
    y = top + 5 * (bh + gap) + 6
    out.append(_legend(y, [
        '이 줄만 칩 수를 세어 나왔다. 자체 칩이 섞여 칩당 값이 절반이라 대수가 두 배다',
    ]))
    return ''.join(out)


FIG_BRGW = _svg(W, 356, '같은 해를 네 자로 재면 14에서 30기가와트로 갈린다', _gw_ways())


FIG_EQ_BR = tree_svg(
    '총액에서 용량으로 가는 길은 어떤 항으로 쪼개지나', _W4,
    _node(['신규 용량'], '÷', [
        _node(['자본지출 총액'], '←', [
            _node(['회사별 가이던스']),
        ]),
        _node(['MW당 자본'], '+', [
            _node(['시설·전력'], '←', [
                _node(['전력을 끄는 층']),
            ]),
            _node(['IT'], '×', [
                _node(['MW당 칩 수']),
                _node(['칩 한 개 값']),
            ]),
        ]),
    ]),
    marks=(('자본지출 총액', 1), ('칩 한 개 값', 2)))

# ── ⑥ 레고. 공법마다 착공에서 준비까지 ────────────────────────────────────
def _sched():
    x0, top, bh, gap = 150, 122, 24, 20
    full, top_v = 250.0, 35.0
    rows = [('현장시공', 18, 24, 30, 35, 0),
            ('MEP 스킷만', 17, 17, None, None, 0),
            ('완전 모듈러', 12, 18, 24, 30, 1),
            ('올인원 프리팹', 12, 12, None, None, 0)]
    out = [_board(accent=(0,)),
           _lt(20, 108, '착공에서 IT 준비까지 걸리는 달 (짙은 칸)과 허가까지 더한 폭',
               't-lab', False)]
    for i, (name, lo, hi, alo, ahi, mark) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 16, name, 't-sm', False))
        if alo:
            out.append(_hbar(x0 + full * lo / top_v, y,
                             full * (ahi - lo) / top_v, bh, False))
        out.append(_hbar(x0 + full * lo / top_v, y,
                         max(full * (hi - lo) / top_v, 3), bh, True))
        lab = '%g~%g' % (lo, hi) if lo != hi else '%g' % lo
        if alo:
            lab += ' · 허가까지 %g~%g' % (alo, ahi)
        out.append(_lt(x0 + full * (ahi or hi) / top_v + 6, y + 16, lab, 't-sm', False))
        if mark:
            out.append(_mark(x0 + full * lo / top_v - 14, y + bh // 2, mark))
    y = top + 4 * (bh + gap) + 2
    out.append(_lt(20, y, '가로축은 달이다. 왼쪽 끝이 착공이고 0에서 시작한다.',
                   't-sm', False))
    out.append(_legend(y + 20, [
        '원문이 36퍼센트 짧다고 적은 자리. 우리가 개월 수로 세면 25~33퍼센트다',
    ]))
    return ''.join(out)


FIG_LEGOSCH = _svg(W, 348, '공장에서 만들어 오면 착공에서 준비까지 여섯 달이 준다',
                   _sched())


# ── ⑦ 지상. 매출에서 자본과 전기가 먹는 몫 ────────────────────────────────
def _grd_cost():
    x0, top, bh, gap = 150, 126, 30, 26
    full = 300.0                      # 매출 1,200만 달러가 이 길이다
    rows = [('계통 연결', 2.01, 1.42, 1),
            ('배후 자체발전', 2.67, 1.42, 0),
            ('산업 생산 확충', 2.67, 1.42, 0)]
    out = [_board(accent=(0, 2)),
           _lt(20, 112, '메가와트당 연 매출 1,200만 달러를 무엇이 먹나', 't-lab', False)]
    for i, (name, cap, pw, mark) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 20, name, 't-sm', False))
        w1 = full * cap / 12.0
        w2 = full * pw / 12.0
        out.append(_hbar(x0, y, w1, bh, True))
        out.append(_hbar(x0 + w1, y, w2, bh, False))
        out.append('<path d="M%d %d V%d" stroke="var(--ink-3)" stroke-width="1" '
                   'stroke-dasharray="4 3" fill="none"/>' % (x0 + full, y - 4, y + bh + 4))
        out.append(_lt(x0 + full + 8, y + 20, '합 %.2f' % (cap + pw), 't-sm', False))
        out.append(_t(x0 + w1 / 2, y + 20, '%.2f' % cap))
        out.append(_t(x0 + w1 + w2 / 2, y + 20, '%.2f' % pw))
        if mark:
            out.append(_mark(x0 + w1 + w2 + 22, y + bh // 2, mark))
    y = top + 3 * (bh + gap) + 4
    out.append(_lt(20, y, '점선이 매출 1,200만 달러다. 남는 칸으로 GPU 값과 사람 값을 댄다.',
                   't-sm', False))
    out.append(_legend(y + 20, [
        '짙은 칸이 연 자본비, 옅은 칸이 전기값. 전기는 계통 시장가로 셌다',
    ]))
    return ''.join(out)


FIG_GRDCOST = _svg(W, 348, '자본과 전기만으로 매출의 3분의 1이 나간다', _grd_cost())


# ── ⑧ 트리니티. 금리가 이익률을 깎는다 ────────────────────────────────────
def _debt():
    x0, top, bh, gap = 200, 124, 26, 26
    full = 260.0
    out = [_board(accent=(1,)),
           _lt(20, 110, '담보를 붙일 때와 안 붙일 때 (GPU 임대 사업)', 't-lab', False)]
    rows = [('조달 금리', 5.62, 10.0, '%', 10.0, 1),
            ('세전이익률', 14.8, 5.4, '%', 14.8, 2)]
    for i, (name, a, b, unit, top_v, mark) in enumerate(rows):
        y = top + i * (bh * 2 + gap)
        out.append(_lt(20, y + 16, name + ' 담보', 't-sm', False))
        out.append(_hbar(x0, y, full * a / top_v, bh - 4, True))
        out.append(_lt(x0 + full * a / top_v + 8, y + 16, '%g%s' % (a, unit), 't-sm', False))
        out.append(_lt(20, y + bh + 16, name + ' 무담보', 't-sm', False))
        out.append(_hbar(x0, y + bh, full * b / top_v, bh - 4, False))
        out.append(_lt(x0 + full * b / top_v + 8, y + bh + 16, '%g%s' % (b, unit),
                       't-sm', False))
        out.append(_mark(x0 - 24, y + bh, mark))
    y = top + 2 * (bh * 2 + gap) + 2
    out.append(_legend(y, [
        '담보가 빠지면 금리가 4.38퍼센트포인트 오른다',
        '같은 사업의 이익률이 9.4퍼센트포인트 깎인다 — 그 둘을 잇는 부채가 연 매출의 2.15배다',
    ]))
    return ''.join(out)


FIG_TRDEBT = _svg(W, 340, '담보가 빠지면 금리 4.4퍼센트포인트가 이익률 9.4퍼센트포인트가 된다',
                  _debt())


# ── ⑨ 스페이스X. 파는 층마다 값이 다르다 ──────────────────────────────────
def _ladder():
    x0, top, bh, gap = 190, 124, 28, 22
    full, top_v = 300.0, 100.0
    rows = [('토큰을 판다 (API 추론)', 100, 1),
            ('클러스터를 짧게 빌려준다', 50, 0),
            ('같은 것을 낮은 값에', 30, 0),
            ('상면과 전력을 빌려준다', 14, 0)]
    out = [_board(accent=(2,)),
           _lt(20, 110, '같은 1메가와트를 무엇으로 파나 (연 매출, 백만 달러)',
               't-lab', False)]
    for i, (name, v, mark) in enumerate(rows):
        y = top + i * (bh + gap)
        out.append(_lt(20, y + 18, name, 't-sm', False))
        out.append(_hbar(x0, y, full * v / top_v, bh, i != 3))
        out.append(_lt(x0 + full * v / top_v + 8, y + 18, '$%g백만' % v, 't-sm', False))
        if mark:
            out.append(_mark(x0 + 22, y + bh // 2, mark))
    y = top + 4 * (bh + gap) + 4
    out.append(_lt(20, y, '맨 아래가 지금 오픈AI 에 임대되는 값이고 맨 위가 7.1배다.',
                   't-sm', False))
    out.append(_legend(y + 20, [
        '자본 5,000만 달러를 매출로 갚는 데 0.50년, 비용을 빼면 0.57년이 걸리는 자리',
    ]))
    return ''.join(out)


FIG_SXLADDER = _svg(W, 372, '같은 전력을 파는 층이 올라갈수록 매출이 일곱 배가 된다',
                    _ladder())


# ── ⑩ 다리. 케이스 셋이 벌어지는 길 ───────────────────────────────────────
def _scn():
    x0, y0, w, h = 96, 118, 420, 170
    top_v = 1600.0
    years = ['2026E', '2027E', '2028E', '2029E', '2030E']
    series = [('Bull', [732.5, 981, 1212.31, 1419.18, 1561.1], True, 1),
              ('Base', [732.5, 907.75, 1031.04, 1124.54, 1180.76], True, 0),
              ('Bear', [732.5, 834.5, 864.43, 873.69, 873.69], False, 2)]
    out = [_board(accent=(0,)),
           _lt(20, 108, '빅4 자본지출 (십억 달러)', 't-lab', False)]
    # 축
    out.append('<path d="M%d %d V%d H%d" stroke="var(--ink-3)" stroke-width="1" '
               'fill="none"/>' % (x0, y0, y0 + h, x0 + w))
    for v in (500, 1000, 1500):
        yy = y0 + h - h * v / top_v
        out.append('<path d="M%d %d H%d" stroke="var(--ink-3)" stroke-width="0.6" '
                   'stroke-dasharray="3 4" fill="none"/>' % (x0, yy, x0 + w))
        out.append(_lt(28, yy + 4, '%g' % v, 't-sm', False))
    for i, yr in enumerate(years):
        xx = x0 + w * i / (len(years) - 1.0)
        out.append(_t(xx, y0 + h + 18, yr))
    for name, vals, solid, mark in series:
        pts = []
        for i, v in enumerate(vals):
            xx = x0 + w * i / (len(vals) - 1.0)
            yy = y0 + h - h * v / top_v
            pts.append('%d %d' % (xx, yy))
        dash = '' if solid else ' stroke-dasharray="6 4"'
        out.append('<path d="M%s" stroke="var(--ink)" stroke-width="%s" fill="none"%s/>'
                   % (' L'.join(pts), '2' if name == 'Base' else '1.4', dash))
        lx = x0 + w + 6
        ly = y0 + h - h * vals[-1] / top_v
        out.append(_lt(lx, ly + 4, '%s %g' % (name, vals[-1]), 't-sm', False))
        if mark:
            out.append(_mark(x0 + w * 3 / 4.0,
                             y0 + h - h * vals[3] / top_v - 16, mark))
    out.append(_legend(y0 + h + 38, [
        '위아래 폭이 기준 케이스의 35퍼센트다 — 다섯 해 누적으로 84~118기가와트',
        '2026년은 셋이 같다. 그 해는 회사가 이미 가이던스를 냈다',
    ]))
    return ''.join(out)


FIG_BRSCN = _svg(W, 386, '케이스가 갈리는 것은 2027년부터다', _scn())

