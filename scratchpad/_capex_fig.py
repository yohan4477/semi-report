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
