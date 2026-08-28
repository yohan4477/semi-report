# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해 — 인라인 SVG.

규칙 하나만 지키면 나머지는 따라온다. **원문에 없는 값을 그리지 않는다.** 막대 길이도
아이콘 개수도 수치로 읽히므로, 원문에 그 수가 없으면 길이를 쓰지 않고 상태 둘로 바꾼다.

좌표는 손으로 찍지 않는다 — `scripts/fig_layout.py` 의 `Plate` 가 글자에서 칸을 내고
선은 상자의 변에서 뽑는다. 전에는 `'M485 80 L485 92'` 처럼 끝점을 눈으로 맞췄고,
상자를 옮길 때마다 선이 상자에서 떨어졌다.

배치는 `scratchpad/check_fig.py` 가 본다.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))

from fig_layout import CSS as FIG_CSS, Plate  # noqa: E402


def _criteria():
    """설계 기준 — 운영자의 셈과 사용자 경험을 좌우로 놓는다.

    값을 그리지 않는다. 원문에 든 것은 「무엇을 기준으로 골랐나」뿐이라 막대도 눈금도
    쓸 수 없다. 상자와 선으로만 어느 쪽을 골랐는지를 보인다.
    """
    p = Plate(640)
    p.head('상업 실리콘 벤더', '모델랩 오픈AI')
    p.row(('총소유비용', '운영자가 치르는 값'),
          ('종단간 지연', '마지막 토큰까지 걸리는 시간', True))
    p.row(None, ('요청당 에너지', '한 번 답하는 데 드는 전력', True))
    p.row(None, '파레토 곡선으로만 낸다')
    p.connect(p.at(0, 0), p.at(0, 1), '기준이 옮겨 갔다')
    p.connect(p.at(0, 1), p.at(1, 1), '서로 밀어낸다', 'd')
    p.connect(p.at(1, 1), p.at(2, 1))
    p.note('두 값이 상충하므로 수치 하나가 아니라 곡선으로 낸다')
    return p.render('설계 기준 두 갈래')


def _domain():
    """스케일업 도메인 두 겹 — 128칩과 최대 2,048칩.

    칩을 128개 그리지 않는다. 상자를 넷 놓는 것도 「넷」이라는 값이 되므로 겹 하나에
    상자 하나만 두고, 여럿이 모인다는 것은 선 위의 말로 적는다.
    """
    p = Plate(640)
    p.row(('안쪽 겹 — 128칩', '칩당 초당 600기가비트', True))
    p.row(('바깥 겹 — 최대 2,048칩', '칩당 초당 200기가비트 · ESUN'))
    p.connect(p.at(0, 0), p.at(1, 0), '안쪽 겹이 여럿 모인다')
    p.note('스위치는 브로드컴 Tomahawk 6')
    p.note('128칩이 한 랙이면 2,048칩은 약 열여섯 랙 — 진행자 어림')
    return p.render('스케일업 도메인 두 겹')


CRITERIA = _criteria()
DOMAIN = _domain()
