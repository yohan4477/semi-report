# -*- coding: utf-8 -*-
"""보고서 ⑨ 메모리 층의 도해. 색은 회색만(확정 규칙 S2) — 강조는 짙은 테두리 하나.

루빈 울트라 랙 지출(_cpo_fig.FIG_RACK)과 HBM4 베이스 다이(_pkg_fig.FIG_BASE)는 여기서
다시 그리지 않고 원본 모듈에서 가져다 쓴다 — 같은 그림을 두 곳에 두면 한쪽만 고쳐진다
(insight-report 규칙).

값은 전부 원문에 있는 것만. 범위 값(3.0~3.3)은 위 끝으로 그리고 캡션에 그렇게 적는다.
자리는 _row 와 아래 눈금 함수가 계산하고 손으로 찍지 않는다(insight-figure 규칙 2).
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK3 = 'var(--ink)', 'var(--ink-3)'


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _plain(x, y, w, h, st=INK3, sw=1.5, rx=6, dash=False):
    extra = ' stroke-dasharray="5 4"' if dash else ''
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="none" '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, rx, st, sw, extra))


def _fill(x, y, w, h, st=INK, sw=1.6, rx=6):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="var(--sunk)" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, st, sw))


def _bar(x, base, h, w, lab_top, lab_bot, accent=False, dash=False):
    """세로 막대 하나. 값을 견줄 때는 나란한 세로 막대(확정 규칙 2026-09-04)."""
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    extra = ' stroke-dasharray="6 4"' if dash else ''
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" '
        'stroke-width="%s"%s/>' % (x, base - h, w, h, 'var(--sunk)' if accent else 'none',
                                   st, sw, extra),
        _t(x + w // 2, base - h - 8, lab_top, 't-sm'),
        _t(x + w // 2, base + 20, lab_bot, 't-sm'),
    ])


# ── 도해 1. 값이 오른 자리와 안 남는 자리 ────────────────────────────
# 상자는 이 글의 절 배열이고 원문이 센 수가 아니다 — 캡션에 그렇게 적는다.
_M1 = _row(1, 16, 44, 236)
_M2 = _row(3, 104, 96, 190, gap=12)
_M3 = _row(3, 232, 46, 190, gap=12)

FIG_MAP = _svg(W, 318, '값은 올랐는데 만드는 회사 손에 안 남는 세 자리', ''.join(
    [_box(_M1[0][0], _M1[0][1], _M1[0][2], _M1[0][3], ['메모리 값이 오른다'], INK, 2.0)]
    + [_a(_M1[0][0] + _M1[0][2] // 2, 60, c[0] + c[2] // 2, 104) for c in _M2]
    + [_box(c[0], c[1], c[2], c[3], lines) for c, lines in zip(_M2, [
        ['① 시차', 'HBM — 연간 계약', '범용 D램 — 그때그때 시세'],
        ['② 협상', '엔비디아', '다른 1군 고객'],
        ['③ 반격', '엔비디아 — 덜어낸다', '메타 — 다시 쓴다', '애플 — 다른 문'],
    ])]
    + [_a(c[0] + c[2] // 2, 200, c[0] + c[2] // 2, 232) for c in _M2]
    + [_box(c[0], c[1], c[2], c[3], lines, INK3, 1.5) for c, lines in zip(_M3, [
        ['4절 · 5절'], ['6절'], ['7절 · 8절 · 9절'],
    ])]
    + [_lt(18, 310, '상자는 이 글의 절 배열이고 원문이 센 수가 아니다', 't-sm', False)]
))


# ── 도해 2. 웨이퍼 한 장의 배분 ──────────────────────────────────
# 왼쪽: 웨이퍼 한 장에서 나오는 비트 비(마니아 L334). 오른쪽: 전체 D램 생산능력에서
# HBM 이 차지하는 몫(마니아 L333). 눈금은 아래 함수가 계산한다.
_WB = 196


def _wq(v):           # 왼쪽 눈금 — 비트 비 4 = 136px
    return int(136 * v / 4.0)


def _wp(v):           # 오른쪽 눈금 — 35% = 136px
    return int(136 * v / 35.0)


FIG_WAFER = _svg(W, 266, '같은 웨이퍼 한 장에서 HBM 은 비트를 훨씬 적게 낸다', ''.join([
    _lt(18, 18, '웨이퍼 한 장이 내는 비트 (HBM = 1)', 't-sm', True),
    _bar(26, _WB, _wq(3), 74, '3배', '범용(HBM3E)'),
    _bar(112, _WB, _wq(4), 74, '4배', '범용(HBM4)'),
    _bar(198, _WB, _wq(1), 74, '1', 'HBM', accent=True),
    '<line x1="306" y1="10" x2="306" y2="244" stroke="%s" stroke-width="1" '
    'stroke-dasharray="4 4"/>' % INK3,
    _lt(326, 18, 'D램 생산능력에서 HBM 의 몫', 't-sm', True),
    _bar(336, _WB, _wp(5), 74, '5% 미만', '2022년'),
    _bar(422, _WB, _wp(20), 74, '20%', '2025년 말'),
    _bar(508, _WB, _wp(35), 74, '35%', '2027년 말', accent=True),
    _lt(18, 258, '오른쪽 뒤 둘은 SemiAnalysis 전망치다 (2026-02)', 't-sm', False),
]))


# ── 도해 3. 2027년 HBM4 값 — 누가 사느냐로 갈린다 ────────────────────
# 값은 주권AI L214·L215. 범위는 위 끝으로 그린다.
_PB = 200


def _pd(v):           # 눈금 — Gb당 4.1달러 = 150px
    return int(150 * v / 4.1)


FIG_PRICE = _svg(W, 250, '같은 HBM4 를 누가 사느냐로 값이 갈린다 (2027년, Gb당 달러)', ''.join([
    _lt(18, 20, 'SK하이닉스가 파는 값', 't-sm', True),
    _bar(38, _PB, _pd(3.3), 96, '3.0~3.3', '엔비디아', accent=True),
    _bar(150, _PB, _pd(4.1), 96, '3.7~4.1', '다른 1군 고객'),
    '<line x1="272" y1="12" x2="272" y2="234" stroke="%s" stroke-width="1" '
    'stroke-dasharray="4 4"/>' % INK3,
    _lt(292, 20, '삼성전자가 파는 값', 't-sm', True),
    _bar(312, _PB, _pd(3.9), 96, '3.5~3.9', '평균'),
    '<line x1="424" y1="12" x2="424" y2="234" stroke="%s" stroke-width="1" '
    'stroke-dasharray="4 4"/>' % INK3,
    _lt(444, 20, '2026년 대비 인상률', 't-sm', True),
    _bar(452, _PB, int(150 * 70 / 98.0), 62, '70%', '엔비디아向', accent=True),
    _bar(530, _PB, int(150 * 98 / 98.0), 62, '98%', '삼성向'),
    _lt(18, 242, '막대 높이는 범위의 위 끝이고, 세 묶음은 눈금이 다르다', 't-sm', False),
]))


# ── 도해 4. CXMT 는 어디쯤 왔나 ───────────────────────────────────
# 왼쪽 값은 CXMT L268·L272-276(2026년 말 전망), 오른쪽은 CXMT L262(2025년 말 실적).
_CB = 200


def _cw(v):           # 눈금 — 720kwspm = 150px
    return int(150 * v / 720.0)


FIG_CXMT = _svg(W, 258, 'CXMT 는 웨이퍼로는 3위를 노리는데 HBM 은 거의 안 만든다', ''.join([
    _lt(18, 20, '웨이퍼 생산능력 2026년 말 전망 (kwspm)', 't-sm', True),
    _bar(24, _CB, _cw(720), 78, '720', '삼성전자'),
    _bar(114, _CB, _cw(595), 78, '595', 'SK하이닉스'),
    _bar(204, _CB, _cw(385), 78, '385', '마이크론'),
    _bar(294, _CB, _cw(350), 78, '350', 'CXMT', accent=True),
    '<line x1="396" y1="12" x2="396" y2="242" stroke="%s" stroke-width="1" '
    'stroke-dasharray="4 4"/>' % INK3,
    _lt(416, 20, 'CXMT 웨이퍼를 어디에 쓰나 (2025년 말)', 't-sm', True),
    '<rect x="470" y="50" width="60" height="150" rx="6" fill="none" stroke="%s" '
    'stroke-width="1.5"/>' % INK3,
    _t(500, 42, '100%', 't-sm'),
    '<rect x="470" y="197" width="60" height="3" rx="1" fill="var(--sunk)" stroke="%s" '
    'stroke-width="1.6"/>' % INK,
    '<path d="M530 198 H566" class="flow" fill="none"/>',
    _lt(570, 202, 'HBM 2%', 't-sm', False),
    '<path d="M530 120 H566" class="flow" fill="none"/>',
    _lt(570, 124, '범용 98%', 't-sm', False),
    _t(500, 222, '265kwspm', 't-sm'),
    _lt(18, 250, '왼쪽은 전망치이고 오른쪽은 2025년 말 실적이다', 't-sm', False),
]))


# ── 도해 5. HBM 위에 얹는 층 — 두 진영 ────────────────────────────
# 같은 꼴 둘을 나란히 두고 맨 위 층만 다르게(확정 규칙 「견줄 때는 같은 꼴」).
# 값은 메르NextHBM T65-T67·T118·T186·T188. 층 이름은 원문 그대로.
_NC = _row(2, 62, 178, 250, gap=40)
_NH = 38


def _stack(c, head, top_name, top_note, dashed, when):
    x, y, w, h = c
    cx = x + w // 2
    out = [_t(cx, y - 10, head, 't-lab')]
    rows = [(top_name, dashed), ('HBM', False), ('가속기', False)]
    for i, (name, dsh) in enumerate(rows):
        yy = y + 8 + i * (_NH + 10)
        if i == 0:
            out.append(_fill(x + 16, yy, w - 32, _NH) if not dsh
                       else _plain(x + 16, yy, w - 32, _NH, INK, 2.0, dash=True))
        else:
            out.append(_plain(x + 16, yy, w - 32, _NH))
        out.append(_t(cx, yy + 24, name, 't-lab'))
    out.append(_t(cx, y + h - 22, top_note))
    out.append(_t(cx, y + h - 4, when))
    return ''.join(out)


FIG_NEXT = _svg(W, 278, 'HBM 위에 무엇을 한 층 더 얹을 것인가 — 두 진영', ''.join([
    _lt(18, 22, '짙은 칸이 새로 얹는 층이고 점선은 상용화 시점이 아직 없는 것', 't-sm', True),
    _stack(_NC[0], 'SK하이닉스 · 샌디스크 · 구글', 'HBF', '용량과 비용',
           False, '2026년 하반기 샘플 · 2027년 양산 목표'),
    _stack(_NC[1], '삼성전자', 'zHBM', '속도와 효율', True, '개념 모델 · 시점 미정'),
    _lt(18, 270, '아래 두 층은 두 진영이 같다 — 다른 것은 맨 위 한 칸뿐이다', 't-sm', False),
]))
