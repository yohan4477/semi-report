# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해 — 인라인 SVG.

규칙 둘.

**원문에 없는 값을 그리지 않는다.** 막대 길이도 아이콘 개수도 수치로 읽히므로,
원문에 그 수가 없으면 길이를 쓰지 않고 상태 둘로 바꾼다.

**판 위 글자는 그 자체로 읽혀야 한다.** 줄여 쓴 말(600Gb)·잘린 문장·본문을 읽어야
뜻이 통하는 말을 두지 않는다. 도해는 본문 옆에 서지만 본문의 각주가 아니다.

좌표는 손으로 찍지 않고 아래 셈에서 나온다. 배치는 `scratchpad/check_fig.py` 가 본다.
"""

FIG_CSS = '''
.fg { font: 600 12px/1.35 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  fill: var(--ink-2); }
.fg-s { font-weight: 400; font-size: 11px; fill: var(--ink-3); }
.fg-b { fill: var(--surface); stroke: var(--line); stroke-width: 1.2; }
.fg-l { stroke: var(--line); stroke-width: 1.2; fill: none; }
.fg-d { stroke: var(--ink-3); stroke-width: 1.2; fill: none; stroke-dasharray: 3 3; }
.fg-c { stroke: var(--accent); stroke-width: 1.2; fill: none; }
'''

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))

import chart  # noqa: E402
from fig_layout import CSS as PLATE_CSS, Plate  # noqa: E402

# Plate 로 그린 도해의 붓을 같이 내보낸다. 안 실으면 상자가 검게 찍힌다 —
# SVG 는 class 를 못 찾으면 채우기 기본값을 검정으로 둔다(2026-08-31)
FIG_CSS = FIG_CSS + PLATE_CSS


def _criteria():
    """잣대가 무엇에서 무엇으로 바뀌었나 — 전과 후를 열로 놓는다.

    손으로 좌표를 찍던 판을 걷고 `Plate` 로 다시 세웠다. 값은 안 그린다 — 원문에 든 것은
    「무엇을 잣대로 골랐나」뿐이라 막대도 눈금도 쓸 수 없다. 왼쪽 한 칸, 오른쪽 두 칸이
    그 자체로 「하나였던 것이 둘로 늘었다」를 말한다.
    """
    p = Plate()
    p.head('전 — 칩을 파는 회사가 정할 때', '후 — 모델을 파는 회사가 정할 때')
    p.row(('총소유비용', '칩을 사서 굴리는 데 드는 돈'),
          ('엔드투엔드 지연', '마지막 글자가 나올 때까지', True))
    p.row(None, ('요청당 전기에너지', '한 번 답하는 데 쓰는 전기', True))
    p.connect(p.at(0, 1), p.at(1, 1), '둘은 같이 못 낮춘다', 'd')
    p.note('돈을 치르는 쪽에서 시간을 겪는 쪽으로 잣대가 옮겼다')
    return p.render('잣대가 무엇에서 무엇으로 바뀌었나')


def _pareto():
    """파레토 곡선 — 두 잣대를 같이 낮출 수 없다.

    손으로 path 를 적지 않는다. 곡선을 눈으로 맞추면 모양이 식에서 나온 것이 아니게 되고,
    축·여백이 그림마다 달라진다. `scripts/chart.py` 가 matplotlib 으로 뽑는다.

    **축에 수를 달지 않는다.** 원문에 점도 눈금도 없어서 곡선의 자리는 값이 아니다.
    모양이 말하는 것은 하나다 — 한쪽을 낮추면 다른 쪽이 올라간다.

    축에는 **재는 것만** 짧게 단다. 어느 쪽이 큰지와 곡선을 어떻게 읽는지는 오른쪽 위
    상자에 적는다 — 맞바꿈 곡선은 왼쪽 위에서 오른쪽 아래로 내려가므로 그 자리가 늘
    빈다. 축 이름에 다 적으면 가로축이 판보다 넓어지고 세로축은 돌아누운 채 잘린다.
    """
    return chart.frontier(
        lambda x: 1.0 / x, 1.0, 4.0,
        '엔드투엔드 지연', '요청당 전기',
        '두 잣대를 같이 낮출 수 없다',
        box=['가로축 — 오른쪽일수록 오래 걸린다',
             '세로축 — 위일수록 많이 쓴다',
             '이 선 위의 점만 낼 수 있다',
             '왼쪽 아래로 갈수록 좋다'])


def _domain():
    """칩 하나에서 2,048칩까지 — 층이 셋이다.

    다른 모델이 준 계층 도식을 상자로 옮기되, 거기 붙어 있던 사양(13.4 PFLOPS ·
    216GiB · 15.4TB/s)은 **원문에 없어서 안 적는다**. 층과 그 사이 속도만 원문에 있다.
    """
    p = Plate()
    p.row(('칩 하나', '할라페뇨 · 700W'))
    p.row(('작은 묶음 — 칩 128개', '칩 하나가 초당 600기가비트', True))
    p.row(('큰 묶음 — 최대 2,048칩', '칩 하나가 초당 200기가비트'))
    p.connect(p.at(0, 0), p.at(1, 0), '이만큼 모으면')
    p.connect(p.at(1, 0), p.at(2, 0), '작은 묶음이 여럿 모이면')
    p.note('붙이는 장치는 브로드컴 Tomahawk 6 이고 규약은 ESUN 이다')
    p.note('128칩이 한 랙이면 2,048칩은 약 열여섯 랙 — 진행자가 두 수를 나눠 본 값이다')
    return p.render('칩 하나에서 2,048칩까지')


def _numa():
    """HBM 을 같이 쓸 때와 조각내 전담시킬 때.

    대역폭 숫자는 그리지 않는다. 이 그림이 말하는 것은 양이 아니라 **기다림이 생기는
    자리**다. 가속기 수도 안 그린다 — 원문에는 「가속기마다」라는 말만 있다.
    """
    p = Plate()
    p.head('전 — 한 덩어리를 같이 쓴다', '후 — 조각내 하나씩 맡긴다')
    p.row(('가속기 여럿', '한 곳을 같이 읽는다'),
          ('가속기마다 하나', '제 조각만 읽는다', True))
    p.row(('HBM 한 덩어리', '남이 읽는 동안 뒤로 밀린다'),
          ('HBM 조각과 전용 버스', '기다릴 일이 없다', True))
    p.connect(p.at(0, 0), p.at(1, 0), '차례를 기다린다')
    p.connect(p.at(0, 1), p.at(1, 1), '바로 닿는다')
    p.note('대역폭 총량은 둘이 같다. 달라지는 것은 값이 언제 손에 닿느냐다')
    return p.render('메모리를 같이 쓸 때와 조각내 전담시킬 때')


CRITERIA = _criteria()
PARETO = _pareto()
DOMAIN = _domain()
NUMA = _numa()


def _agent_flow():
    """일이 어디로 가나 — 요청 하나가 지나는 자리.

    좌표를 손으로 안 찍는다. `scripts/fig_layout.py` 의 Plate 가 글자에서 칸을 내고
    선은 상자의 변에서 뽑는다. 원문의 비유(천재·비서)를 상자 이름에 그대로 쓴다.
    """
    p = Plate()          # 판 폭은 기본값(520) — 카드 슬롯에 맞아 글자가 본문 크기로 선다
    p.row(('에이전트 요청', '사람이 시킨 일'))
    p.row(('클라우드 VM', '범용 CPU 위에서 돈다'))
    p.row(('GPU — 천재', '박사학위를 다 가진 쪽', True),
          ('에이전틱 CPU 랙', '컴파일·검색·조회를 맡는다'))
    p.row(('호스트 노드 CPU — 비서', '천재를 쉬지 않게 먹인다'), None)
    p.connect(p.at(0, 0), p.at(1, 0))
    # 갈래마다 이름을 달면 칸 사이 틈보다 이름이 넓어 상자 테두리를 문다(check_fig).
    # 갈래가 무엇인지는 상자 이름이 이미 말하므로 선은 비워 둔다
    p.connect(p.at(1, 0), p.at(2, 0))
    p.connect(p.at(1, 0), p.at(2, 1))
    p.connect(p.at(2, 0), p.at(3, 0))
    p.note('연산은 왼쪽으로, 컴파일·검색 같은 여분 일은 오른쪽으로 간다')
    p.note('천재와 비서는 원문의 비유를 그대로 쓴 것이다')
    return p.render('일이 어디로 가나')


def _cores():
    """코어 수 — 원문에 나온 수만 막대로 세운다.

    막대 길이가 곧 주장이라 없는 수는 못 넣는다. 다섯 다 원문에 있는 값이다.
    """
    return chart.bars(
        [('호스트 CPU 예시', 88), ('사무실 비유', 128), ('AMD', 256),
         ('인텔', 288), ('에이전틱으로 늘린다면', 512)],
        '코어 수', '코어 수 다섯 사례',
        note='다섯 다 진행자가 예로 든 수다. 제품 사양표가 아니다')


AGENT_FLOW = _agent_flow()
CORES = _cores()

def _before_after():
    """전과 후 — 에이전트가 도는 자리와 그 뒤에 붙는 랙.

    괄호로 적던 아스키 도식을 상자로 바꿨다. 열이 전과 후이고 아래로 흐른다.
    마지막 줄 오른쪽 상자가 새로 생긴 칸이라 강조색으로 둔다.
    """
    p = Plate()
    p.head('전', '후')
    p.row(('사람이 앉은 노트북', '앉아 있을 때만 돈다'),
          ('클라우드 가상머신', '꺼도 계속 돈다'))
    p.row(('에이전트 하니스', '직접 깔고 관리한다'),
          ('에이전트 여럿', '한 번 로그인해 나눠 쓴다'))
    p.row('GPU 랙', 'GPU 랙')
    p.row(None, ('에이전틱 CPU 랙', '이 칸이 새로 생긴다', True))
    for i in range(3):
        p.connect(p.at(i, 0), p.at(i + 1, 0)) if i < 2 else None
    p.connect(p.at(0, 1), p.at(1, 1))
    p.connect(p.at(1, 1), p.at(2, 1))
    p.connect(p.at(2, 1), p.at(3, 1))
    return p.render('전과 후 — 에이전트가 도는 자리')



BEFORE_AFTER = _before_after()

def _value_chain():
    """누가 무엇을 맡나 — 다른 모델이 준 밸류체인 도식을 상자로 다시 그렸다.

    그 도식은 [OpenAI] → [Broadcom] → [TSMC] → [Celestica] → [OpenAI DC] 였다.
    가운데 둘의 성격이 다르다 — 브로드컴은 로드맵 슬라이드에 파트너로 적혔고,
    공정과 시스템 조립은 진행자 추정이다. 그 차이를 상자 안에 적는다.
    """
    p = Plate()
    p.row(('오픈AI', '무엇을 재고 무엇을 뺄지 정한다'))
    p.row(('브로드컴', '함께 설계하고 스위치를 댄다 · 발표 슬라이드', True))
    p.row(('TSMC N3 변형', '공정 — 진행자 추측'))
    p.row(('셀레스티카', '시스템 설계 — 진행자 추정'))
    p.row(('오픈AI 데이터센터', '제 트래픽에 쓴다'))
    for i in range(4):
        p.connect(p.at(i, 0), p.at(i + 1, 0))
    p.note('강조한 칸만 발표에 나온다. 아래 둘은 진행자가 추측이라고 못박은 자리다')
    return p.render('누가 무엇을 맡나')


VALUE_CHAIN = _value_chain()
