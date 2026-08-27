# -*- coding: utf-8 -*-
"""빅테크 여섯 비교 리포트 도해 — 구조적 편향 한 장.

값은 전부 계산에서 온다. 시장 배수 범위는 facts.json 의 lookback(그때 제출돼 있던
서류만으로 낸 값)이고, 우리 배수는 (1+g)/(r-g) 다. 손으로 찍은 자리가 없다.

한 장이 말하는 것 하나 — 우리 잣대의 영구가치 배수가 지난 3년 시장 범위 안에 든
회사가 하나도 없다. 예측이 틀린 것이 아니라 잣대가 구조적으로 낮다는 뜻이다.
"""
import _val_peers as pr
import gen_sudoremove_dashboard as sudo

_svg, _lt = sudo._svg, sudo._lt

W = 640
_X, _BARW = 132, 412
_ROWS = pr.bias_rows()
_MAX = max(r['hi'] for r in _ROWS) * 1.02


def _px(v):
    return int(round(v / _MAX * _BARW))


def _row(i, r):
    y = 58 + i * 32
    x0, x1 = _X + _px(r['lo']), _X + _px(r['hi'])
    out = ['<text x="%d" y="%d" text-anchor="end" class="t-lab">%s</text>'
           % (_X - 12, y + 15, r['name']),
           # 시장이 낸 배수 범위
           '<rect x="%d" y="%d" width="%d" height="18" fill="var(--ink-3)" opacity="0.34"/>'
           % (x0, y, max(2, x1 - x0)),
           # 우리 배수. 범위 왼쪽 밖에 서는 것이 이 그림의 요점이다
           '<path d="M%d %d V%d" stroke="var(--accent)" stroke-width="3" fill="none"/>'
           % (_X + _px(r['ours']), y - 4, y + 22),
           '<text x="%d" y="%d" class="t-sm">%.0f~%.0f배</text>'
           % (x1 + 8, y + 15, r['lo'], r['hi'])]
    return ''.join(out)


_BOT = 58 + 32 * len(_ROWS)

FIG_BIAS = _svg(W, _BOT + 84, '우리 배수가 시장 범위 안에 든 회사가 없다', ''.join(
    [_lt(40, 34, '잉여현금흐름 대비 시가총액 배수 — 회색은 지난 3년 시장이 낸 범위')]
    + [_row(i, r) for i, r in enumerate(_ROWS)]
    + [_lt(40, _BOT + 28, '세로선은 우리 잣대의 영구가치 배수다. 여섯 다 회색 막대 '
                          '왼쪽 밖에 선다', bold=False),
       _lt(40, _BOT + 48, '우리 배수 %.1f~%.1f배 · 시장 범위 %.0f~%.0f배'
           % (min(r['ours'] for r in _ROWS), max(r['ours'] for r in _ROWS),
              min(r['lo'] for r in _ROWS), max(r['hi'] for r in _ROWS)), bold=False),
       _lt(40, _BOT + 68, '시장 배수는 그때 제출돼 있던 서류로만 냈다. 사후 정보가 '
                          '안 섞인다', bold=False)]))
