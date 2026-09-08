# -*- coding: utf-8 -*-
"""보고서 하네스·스킬 층 — 판단을 모델에서 걷어 낸 열두 달.

본문은 insights/reports/harness-2026-09-08.md 에서 읽는다. CPO·선단 패키징·전력 층과
같은 규약이다. 산문은 마크다운 원본에 두고 여기서 HTML 로 바꾼다. 차례와 절 번호는
_rep_toc 가 붙인다 — 층마다 복사하지 않는다.

이 층의 성격 하나 — 재료가 컨퍼런스 발표라 화자가 열여덟 편에 흩어져 있다. 전력 층이
한 필자라 어긋남을 같은 저자의 두 글 사이에서 찾아야 했다면, 여기서는 회사가 서로를
반박한다. 그 대신 잰 값이 거의 없어 견줄 기준선이 없다 — 14절이 그 한계를 스스로 밝힌다.
"""
import io
import os
import re

import _harness_fig as hf
import _rep_toc as rt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'harness-2026-09-08.md')

HEAD_HARNESS = (
    '<div class="rep-head"><span class="rn">보고서 ⑩</span>'
    '<h2 id="rep-harness">하네스·스킬 총정리 — 판단을 모델에서 걷어 낸 열두 달, '
    '그 값을 누가 냈나</h2>'
    '<p class="rm">바탕 <b>AI Engineer 컨퍼런스 발표 16편 · SemiAnalysis 뉴스레터 2편</b> · '
    '원문 기간 <b>2025-08 ~ 2026-08</b><br>'
    '재료를 여러 회사가 썼습니다. 그래서 어긋남을 같은 저자 안에서 찾을 필요가 없었고, '
    '같은 해에 나온 답들이 서로를 반박하는 자리를 그대로 실었습니다. 대신 잰 값이 '
    '거의 없습니다 — 열여덟 편 가운데 기준선과 견준 값을 낸 편이 하나도 없다는 것을 '
    '14절에 적었습니다. 분량 제한 없이 썼습니다.</p></div>')

GROUPS = [('무엇이 옮겨 갔나', 1, 4),
          ('값이 어디서 나나', 5, 8),
          ('어디서 무너지나', 9, 14)]

LEAD = ('이 층은 물음 하나를 세 묶음으로 따라갑니다 — 무엇이 모델 바깥으로 옮겨 갔나, '
        '그 값이 어디서 나나, 그리고 어디서 무너지나.')

CAPTION = {
    'WHERE': ('판단을 어디까지 걷어낼지에 세 곳이 다르게 답했다', hf.FIG_WHERE,
              '세 판이 같은 크기이고 줄도 같은 두 줄입니다 — 위가 모델에 남긴 것, 아래가 '
              '하네스가 가져간 것. 마이크로소프트는 단계를 넘기는 판단을 모델 바깥으로 '
              '옮겼고(운전대 L41·L53), 커서는 워크트리(같은 저장소를 여러 폴더로 갈라 각각 '
              '다른 가지를 놓고 일하는 깃 기능)를 벗어나지 못하게 막던 코드를 '
              '지우고 프롬프트로 부탁하는 쪽으로 갔으며(200줄 L31·L58), 코덱스는 '
              '운영체제 샌드박스(코드가 바깥을 건드리지 못하게 가둬 놓고 돌리는 자리) '
              '위에 위험을 심사하는 서브에이전트(부모가 따로 띄워 제 맥락에서 일을 '
              '시키는 에이전트)를 얹었습니다'
              '(코덱스 L62·L72). 세 판을 나란히 놓은 것은 이 글의 배치이고, 각 칸에 적힌 '
              '말은 그 발표의 서술입니다. 값이 아니라 서술이라 막대 높이로 그리지 '
              '않았습니다.'),
    'CTX': ('컨텍스트 창에 넣는 손 셋과 빼는 손 셋', hf.FIG_CTX,
            '가운데가 창이고 좌우가 그 창을 다루는 장치입니다. 넣는 손 셋은 앤스로픽이 '
            '나눈 것이고(클로드API L36·L38, 스킬만들 L46), 빼는 손 셋은 앤스로픽 하나와 '
            '코덱스 둘입니다(클로드API L40, 코덱스 L42·L43). 상한 2%는 코덱스가 실제로 '
            '건 값이고(코덱스 L43), 백에서 이백 토큰은 스킬 설명이 부를 때마다 무는 '
            '값입니다(스킬평가 L31). 두 값은 다른 회사가 다른 대상에 적용한 것이라 '
            '더하거나 견주지 않았습니다. 여섯을 좌우로 나눈 것은 이 글의 배치입니다.'),
    'CHAIN': ('사고 다섯과 그때 없던 경계 다섯', hf.FIG_CHAIN,
              '다섯 행이 전부 같은 꼴입니다 — 왼쪽이 무엇이 났나, 가운데가 어떻게 났나, '
              '오른쪽이 그때 없던 경계입니다. 다섯 다 발표자가 오픈클로 공개 이슈에서 '
              '뽑은 것이고 짝지음도 발표자가 한 것입니다(하니스실패 L60-66). 얼마나 '
              '자주 났고 몇 명이 겪었는지는 발표에 나오지 않아 크기로 그리지 '
              '않았습니다(하니스실패 L103).'),
    'TIME': ('열세 달 동안 판단이 어느 쪽으로 옮겼나', hf.FIG_TIME,
             '세로가 시간이고 좌우가 방향입니다. 어느 쪽에 놓을지는 이 글이 나눈 '
             '것이고, 각 줄에 적힌 말은 그 발표의 서술입니다 — 앤스로픽의 「견해를 안 '
             '갖는다」(진화 L21), 오픈AI의 「하네스가 새로운 추상화 계층이 된다」'
             '(버티는 L59), 클라우드플레어의 두 도구(코드모드 L35-41), 커서의 격리 '
             '코드 삭제(200줄 L25·L58), 마이크로소프트의 상태 머신(운전대 L35), '
             '코덱스의 오토 리뷰(코덱스 L72). 오른쪽이 넷이고 왼쪽이 둘인 것은 이 '
             '재료에서 그렇게 나온 것이지 업계 비율이 아닙니다.'),
}

_CITE = re.compile(r'\s*\([^()]*?L[\d,\-\s·]+\)')


def _strip(s):
    """(라벨 L12) 는 화면에서 걷는다 — 원본 파일에만 남는다(확정 규칙 S1)."""
    s = _CITE.sub('', s)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s).strip()


def load():
    txt = io.open(SRC, encoding='utf-8').read()
    if txt.startswith('---'):
        txt = txt.split('---', 2)[2]
    out, para = [], []

    def flush():
        if para:
            out.append(('p', ' '.join(para)))
            para.clear()

    for line in txt.split('\n'):
        s = line.rstrip()
        if s.startswith('## '):
            flush()
            out.append(('sec', re.sub(r'^\d+\.\s*', '', s[3:]).strip()))
        elif s.startswith('[[fig:'):
            flush()
            out.append(('fig', s[6:].rstrip(']').strip()))
        elif not s:
            flush()
        elif s.startswith('#'):
            continue
        else:
            para.append(s.strip())
    flush()
    return out


def toc_html(titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다."""
    return rt.toc_html('harness', LEAD, GROUPS, titles)


def report_harness(sec, p, fig):
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig') and not toc_done:
            p(toc_html(titles))
            toc_done = True
        if k == 'sec':
            sec(rt.sec_title(titles.index(v) + 1, v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
