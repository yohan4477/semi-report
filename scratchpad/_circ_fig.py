# -*- coding: utf-8 -*-
"""보고서 순환금융 층의 도해 아홉. 색은 회색만(확정 규칙 S2).

프로세스 판을 먼저 세우고 그 위에 얹는다(확정 규칙, 2026-09-09). 이 층의 판은
돈이 도는 세 마디다 — 칩 회사 · 모델 랩 · 데이터센터. 좌표는 `_B` 하나가 갖고
있고 도해마다 다시 찍지 않는다. 되돌아오는 화살표는 판 바깥 오른쪽 레일로 돈다.

값은 전부 원문에 있는 것만 그린다 — 캡션이 라벨과 줄 번호를 댄다.
"""
import _biz_fig as bf

_svg, _box, _a, _lt, _row = bf._svg, bf._box, bf._a, bf._lt, bf._row
W = 640
INK, INK2, INK3 = 'var(--ink)', 'var(--ink-2)', 'var(--ink-3)'

_DEFS = ('<defs><marker id="fig-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         '<path d="M0 0 L10 5 L0 10 z" fill="%s"/></marker></defs>' % INK3)


def _t(cx, y, s, cls='t-sm'):
    return '<text x="%d" y="%d" text-anchor="middle" class="%s">%s</text>' % (cx, y, cls, s)


def _dash(x1, y1, x2, y2):
    return _a(x1, y1, x2, y2, dash=True)


def _vline(x, y1, y2, dash=False):
    return ('<path d="M%d %d V%d" class="flow"%s/>'
            % (x, y1, y2, ' style="stroke-dasharray:5 4"' if dash else ''))


# ── 판. 돈이 도는 세 마디. 이 좌표를 도해 셋이 같이 쓴다 ──────────────
_BX, _BW, _BH, _BSTEP = 176, 260, 54, 104
_BY0 = 44
_BOARD = [(_BX, _BY0 + i * _BSTEP, _BW, _BH) for i in range(3)]
_BNAMES = [['칩 회사', '엔비디아'],
           ['모델 랩', '오픈AI'],
           ['데이터센터·클라우드', '오라클']]
_RAIL = _BX + _BW + 46            # 되돌아오는 레일이 도는 자리
_BOARD_H = _BY0 + 2 * _BSTEP + _BH


def _board(accent=-1):
    """세 마디 판. 상자 크기는 전부 같다(사슬은 한 크기)."""
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(_BOARD, _BNAMES)):
        st, sw = (INK, 2.0) if i == accent else (INK3, 1.5)
        out.append(_box(x, y, w, h, lines, st, sw))
    return ''.join(out)


NUM = '①②③④⑤⑥⑦⑧⑨'


def _mark(x, y, n):
    """화살표에 붙는 동그라미 번호. 설명은 판 위에 안 얹고 아래 범례로 내린다."""
    return ('<circle cx="%d" cy="%d" r="10" fill="var(--paper)" stroke="%s" '
            'stroke-width="1.5"/>%s' % (x, y, INK3, _t(x, y + 5, NUM[n - 1], 't-lab')))


def _legend(y, items):
    """판 아래 범례. 한 줄에 하나씩 — 번호와 그 화살표가 나르는 것."""
    return ''.join(_lt(24, y + i * 22, '%s %s' % (NUM[i], s), 't-sm', False)
                   for i, s in enumerate(items))


def _back_rail(n):
    """맨 아래에서 맨 위로 되돌아오는 레일. 판 바깥 오른쪽으로 돈다."""
    y1 = _BOARD[2][1] + _BH // 2
    y2 = _BOARD[0][1] + _BH // 2
    return ''.join([
        '<path d="M%d %d H%d V%d H%d" class="flow" fill="none"/>'
        % (_BX + _BW, y1, _RAIL, y2, _BX + _BW),
        _mark(_RAIL, (y1 + y2) // 2, n),
    ])


def _down(i, n, dash=False):
    """판의 i번째 상자에서 그 아래 상자로."""
    y1 = _BOARD[i][1] + _BH
    y2 = _BOARD[i + 1][1]
    return ''.join([
        _vline(_BX + _BW // 2, y1, y2, dash),
        _mark(_BX + _BW // 2 + 26, (y1 + y2) // 2, n),
    ])


# ── 도해 1. 한 바퀴가 어떻게 도나 ────────────────────────────────────
_L1 = ['엔비디아가 오픈AI 지분에 넣은 300억 달러',
       '오픈AI가 오라클과 맺은 5년 3,000억 달러 클라우드 계약',
       '오라클이 그 데이터센터를 채우려고 사는 엔비디아 GPU']
FIG_LOOP = _svg(W, _BOARD_H + 26 + 22 * len(_L1),
                '엔비디아에서 나간 돈이 엔비디아 매출로 돌아온다',
                _DEFS + ''.join([
                    _board(accent=0),
                    _down(0, 1),
                    _down(1, 2),
                    _back_rail(3),
                    _legend(_BOARD_H + 24, _L1),
                ]))


# ── 도해 2. 고리를 도는 것 넷 ────────────────────────────────────────
# 같은 판을 같은 좌표로 다시 깔고 그 위에 갈래를 얹는다. 점선은 조건부다.
_CUSTY = _BOARD_H + 34
_L2 = ['지분 — 현금이 그 자리에서 건너간다',
       '계약 — 쓰든 안 쓰든 약속한 만큼 낸다',
       '현금 — 장비값으로 되돌아온다',
       '보증 — 발동해야 비로소 낸다 (점선)',
       '토큰 요금 — 고리 밖에서 새로 들어오는 현금']
FIG_KIND = _svg(W, _CUSTY + 70 + 22 * len(_L2),
                '지분·보증·계약·현금이 저마다 다른 마디를 잇는다',
                _DEFS + ''.join([
                    _board(),
                    _down(0, 1),
                    _down(1, 2),
                    _back_rail(3),
                    # 보증은 칩 회사에서 데이터센터로 바로 간다 — 왼쪽 레일, 점선
                    '<path d="M%d %d H%d V%d H%d" class="flow" fill="none" '
                    'style="stroke-dasharray:5 4"/>'
                    % (_BX, _BOARD[0][1] + _BH // 2, _BX - 40,
                       _BOARD[2][1] + _BH // 2, _BX),
                    _mark(_BX - 40, _BOARD[2][1] - 16, 4),
                    _box(_BX, _CUSTY, _BW, 44, ['최종 고객 — 토큰 요금'], INK, 2.0),
                    # 최종 고객은 모델 랩에 낸다 — 데이터센터 상자를 뚫지 않게
                    # 판 바깥 왼쪽 레일로 돌린다(보증 레일보다 한 칸 더 바깥)
                    '<path d="M%d %d H%d V%d H%d" class="flow" fill="none"/>'
                    % (_BX, _CUSTY + 22, _BX - 76,
                       _BOARD[1][1] + _BH // 2, _BX),
                    _mark(_BX - 76, (_BOARD[1][1] + _BH // 2 + _CUSTY + 22) // 2, 5),
                    _legend(_CUSTY + 68, _L2),
                ]))


# ── 도해 3. 신용에 따라 갈리는 조달 금리 ─────────────────────────────
_RY, _RH = 46, 176                 # 막대가 서는 판
_RMAX = 16.0


def _rbar(i, v, l1, l2, filled, dashed=False):
    x = 40 + i * 116
    h = int(_RH * v / _RMAX)
    y = _RY + _RH - h
    fill = INK3 if filled else 'none'
    style = ' style="stroke-dasharray:5 4"' if dashed else ''
    return ''.join([
        '<rect x="%d" y="%d" width="70" height="%d" rx="3" fill="%s" '
        'stroke="%s" stroke-width="1.5"%s/>' % (x, y, h, fill, INK, style),
        _t(x + 35, y - 8, '%s%%' % v),
        _t(x + 35, _RY + _RH + 20, l1, 't-lab'),
        _t(x + 35, _RY + _RH + 36, l2),
    ])


FIG_CREDIT = _svg(W, _RY + _RH + 58, '같은 담보라도 누가 세입자냐에 따라 금리가 갈린다',
                  ''.join([
                      '<path d="M28 %d H612" stroke="var(--line)" stroke-width="1"/>'
                      % (_RY + _RH),
                      _rbar(0, 5.0, '메타', '자기 채권', True),
                      _rbar(1, 5.9, '코어위브', '메타가 보증', True),
                      _rbar(2, 10.0, '코어위브', '무담보 회사채', False),
                      _rbar(3, 6.0, '투자적격 세입자', '메르가 든 값', False),
                      _rbar(4, 15.0, '오픈AI', '빌릴 수 있을지', False, True),
                  ]))


# ── 도해 4. 보증 아래 1년차 정산 ─────────────────────────────────────
# 구성비는 기둥 하나에(확정 규칙). 기둥 전체가 청구가 6.75달러다.
_SX, _SY, _SW, _SH = 150, 52, 96, 210
_STOP = 6.75


def _seg(v0, v1, label, hot):
    """청구가 기둥에서 v0~v1 구간. 값은 오른쪽으로 지시선을 빼서 단다."""
    y0 = _SY + int(_SH * (_STOP - v1) / _STOP)
    y1 = _SY + int(_SH * (_STOP - v0) / _STOP)
    mid = (y0 + y1) // 2
    return ''.join([
        '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" '
        'stroke-width="1.5"/>' % (_SX, y0, _SW, y1 - y0,
                                  INK3 if hot else 'none', INK),
        '<path d="M%d %d H%d" stroke="var(--line)" stroke-width="1"/>'
        % (_SX + _SW, mid, _SX + _SW + 24),
        _lt(_SX + _SW + 30, mid + 5, label, 't-sm', False),
    ])


FIG_SETTLE = _svg(W, _SY + _SH + 52, '보증을 낀 1년차에 네오클라우드가 실제로 쥐는 값',
                  ''.join([
                      _t(_SX + _SW // 2, _SY - 12, '청구가 $6.75/시간', 't-lab'),
                      _seg(0, 3.68, '보증 하한 $3.68 — 전액 네오클라우드', False),
                      _seg(3.68, 3.68 + 3.07 * 0.6, '초과분의 60% $1.84 — 네오클라우드', False),
                      _seg(3.68 + 3.07 * 0.6, 6.75, '초과분의 40% $1.23 — 엔비디아', True),
                      _lt(28, _SY + _SH + 30, '네오클라우드가 쥐는 값 $5.52 · '
                          '보증이 없었다면 $6.75', 't-sm', False),
                  ]))


# ── 도해 5. 부외로 쌓이는 잔액과 실제로 들어오는 매출 ────────────────
_CY, _CH = 48, 168
_CMAX = 1800.0


def _cbar(i, v, l1, l2, filled):
    x = 62 + i * 136
    h = max(int(_CH * v / _CMAX), 2)
    y = _CY + _CH - h
    return ''.join([
        '<rect x="%d" y="%d" width="78" height="%d" rx="3" fill="%s" '
        'stroke="%s" stroke-width="1.5"/>'
        % (x, y, h, INK3 if filled else 'none', INK),
        _t(x + 39, y - 8, '%s억 달러' % format(v, ',')),
        _t(x + 39, _CY + _CH + 20, l1, 't-lab'),
        _t(x + 39, _CY + _CH + 36, l2),
    ])


FIG_CONTINGENT = _svg(W, _CY + _CH + 58,
                      '보증 잔액은 재무제표 밖에 쌓이고 배분 매출만 안으로 들어온다',
                      ''.join([
                          '<path d="M40 %d H600" stroke="var(--line)" stroke-width="1"/>'
                          % (_CY + _CH),
                          _cbar(0, 775, '잔액', 'F1/27', False),
                          _cbar(1, 1753, '잔액', 'F1/29', False),
                          _cbar(2, 18, '매출', 'F1/27', True),
                          _cbar(3, 139, '매출', 'F1/29', True),
                      ]))


# ── 도해 6. 담보 값을 두 화자가 다르게 잰다 ──────────────────────────
# 두 칸 대조 — 같은 행이 같은 역할이고 이름만 다르다. 역할은 가운데 도랑에.
_PW, _PH2 = 236, 150
_PLX, _PRX = 26, W - _PW - 26
_PY = 56


def _panel2(x, name, rows, accent):
    st, sw = (INK, 2.0) if accent else (INK3, 1.5)
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" '
           'stroke="%s" stroke-width="%.1f"/>' % (x, _PY, _PW, _PH2, st, sw),
           _t(x + _PW // 2, _PY + 22, name, 't-lab')]
    for i, s in enumerate(rows):
        out.append(_t(x + _PW // 2, _PY + 54 + i * 30, s))
    return ''.join(out)


FIG_RESIDUAL = _svg(W, _PY + _PH2 + 34, '같은 GPU를 팔 때와 굴릴 때가 다르다', ''.join([
    _panel2(_PLX, '메르', ['되팔 때의 값', '3년이면 절반', '중고 시장이 크지 않다'], False),
    _panel2(_PRX, 'SemiAnalysis', ['계속 빌려줄 때의 값', '1년 임대 $1.70 → $2.35',
                                   '경제적 수명이 늘어난다'], True),
    _t(W // 2, _PY + 54, '무엇을 재나'),
    _t(W // 2, _PY + 84, '값'),
    _t(W // 2, _PY + 114, '그래서'),
]))


# ── 도해 7. 고리 밖에서 들어오는 새 돈 ───────────────────────────────
_NY, _NH = 48, 160
_NMAX = 900.0


def _nbar(i, v, l1, l2, filled, dashed=False):
    x = 46 + i * 146
    h = max(int(_NH * v / _NMAX), 2) if v else 8
    y = _NY + _NH - h
    style = ' style="stroke-dasharray:5 4"' if dashed else ''
    return ''.join([
        '<rect x="%d" y="%d" width="86" height="%d" rx="3" fill="%s" '
        'stroke="%s" stroke-width="1.5"%s/>'
        % (x, y, h, INK3 if filled else 'none', INK, style),
        _t(x + 43, y - 8, '%s억 달러' % format(v, ',') if v else '금액 미제시'),
        _t(x + 43, _NY + _NH + 20, l1, 't-lab'),
        _t(x + 43, _NY + _NH + 36, l2),
    ])


FIG_NEWMONEY = _svg(W, _NY + _NH + 58, '구글·스페이스X·앤트로픽이 같은 시기에 끌어오려는 금액',
                    ''.join([
                        '<path d="M32 %d H608" stroke="var(--line)" stroke-width="1"/>'
                        % (_NY + _NH),
                        _nbar(0, 847, '구글', '유상증자 · 완료', True),
                        _nbar(1, 750, '스페이스X', '상장 · 예상', False),
                        _nbar(2, 300, '앤트로픽', '상장 · 목표', False),
                        _nbar(3, 0, '오픈AI', '상장 · 시점만', False, True),
                    ]))


# ── 도해 8. 매출로 들어오는 것과 비용에서 빠지는 것 ──────────────────
FIG_GROSS = _svg(W, _PY + _PH2 + 34, 'TPU 판매는 총액으로 들어오고 딥마인드 학습비는 사업부 밖으로 빠진다',
                 ''.join([
                     _panel2(_PLX, '매출로 들어온다',
                             ['TPU 시스템 판매', '원가를 안 뺀 총액',
                              '기가와트당 350억 달러'], True),
                     _panel2(_PRX, '비용에서 빠진다',
                             ['딥마인드 학습비', '알파벳 레벨 활동으로',
                              '30억 → 54억 달러'], False),
                     _t(W // 2, _PY + 54, '무엇이'),
                     _t(W // 2, _PY + 84, '어떻게'),
                     _t(W // 2, _PY + 114, '얼마'),
                 ]))


# ── 도해 9. 마지막 고객이 쓰는 돈 ────────────────────────────────────
# 값이 세 자릿수씩 벌어져 선형 축으로는 중위값이 안 보인다. 로그 축이다.
import math                                                       # noqa: E402

_SPY, _SPH = 52, 168
_SPLO, _SPHI = 100.0, 100000.0


def _logy(v):
    r = (math.log10(v) - math.log10(_SPLO)) / (math.log10(_SPHI) - math.log10(_SPLO))
    return _SPY + _SPH - int(_SPH * r)


def _spbar(i, v, l1, l2, filled):
    x = 96 + i * 156
    y = _logy(v)
    return ''.join([
        '<rect x="%d" y="%d" width="92" height="%d" rx="3" fill="%s" '
        'stroke="%s" stroke-width="1.5"/>'
        % (x, y, _SPY + _SPH - y, INK3 if filled else 'none', INK),
        _t(x + 46, y - 8, '$%s' % format(v, ',')),
        _t(x + 46, _SPY + _SPH + 20, l1, 't-lab'),
        _t(x + 46, _SPY + _SPH + 36, l2),
    ])


FIG_SPEND = _svg(W, _SPY + _SPH + 58, '직원 한 사람이 한 해에 쓰는 토큰 값 (로그 축)',
                 ''.join(
                     ['<path d="M60 %d H600" stroke="var(--line)" stroke-width="1"/>'
                      % _logy(v) for v in (100, 1000, 10000, 100000)]
                     + [_lt(24, _logy(v) + 4, '$%s' % format(v, ','), 't-sm', False)
                        for v in (100, 1000, 10000, 100000)]
                     + [_spbar(0, 136, '중위값', '램프 결제 데이터', False),
                        _spbar(1, 7300, '90번째 백분위', '램프 결제 데이터', False),
                        _spbar(2, 90000, '99번째 백분위', '램프 결제 데이터', True)]))


# ── 도해 10. 누가 먼저 갚기 시작했나 ─────────────────────────────────
FIG_PAY = _svg(W, _PY + _PH2 + 34, '같은 시점에 두 랩의 손익이 갈린다', ''.join([
    _panel2(_PLX, '앤트로픽', ['영업이익률 +6%', 'API 매출 75~85%',
                            '무료 사용자 부담 작다'], True),
    _panel2(_PRX, '오픈AI', ['영업이익률 -100%', '구독 매출 65% 넘음',
                           '무료 9억 명 월 $0.70'], False),
    _t(W // 2, _PY + 54, '3분기 손익'),
    _t(W // 2, _PY + 84, '매출이 어디서'),
    _t(W // 2, _PY + 114, '누가 무나'),
]))
