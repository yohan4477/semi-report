# -*- coding: utf-8 -*-
"""보고서 ⑨ — XPU 총정리. 본문은 insights/reports/xpu-2026-09-18.md 에서 읽는다.

선단 패키징 층(_pkg_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고 여기서 HTML 로
바꾼다 — 대시보드 HTML 은 생성물이고 고칠 것은 그 원본이다.

원본 규약
  ## N. 제목          절. 번호는 여기서 다시 센다(목차와 본문이 같은 함수에서 나온다)
  [[fig:이름]]        도해. _xpu_fig 의 FIG_이름 과 아래 CAPTION 의 캡션을 붙인다
  | … |               표 — 첫 줄이 머리, 둘째 줄이 구분선
  (라벨 L12)          출처 표기. 화면에서는 걷는다(확정 규칙 S1)
"""
import io
import os
import re

import _rep_toc as rt

import _xpu_fig as xf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'xpu-2026-09-18.md')

HEAD_XPU = (
    '<div class="rep-head"><span class="rn">보고서 ⑨</span>'
    '<h2 id="rep-xpu">XPU 총정리 — 워크로드가 바뀌면 칩 순위도 바뀌나</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 뉴스레터 7편 · 영문 클리핑 2편 · Semi Doped 3회차</b> · '
    '원문 기간 <b>2025-06 ~ 2026-09</b> · 유료 뉴스레터 원문<br>'
    '엔비디아·AMD·구글 TPU·AWS 트레이니움·세레브라스·화웨이·오픈AI 자체 칩을 같은 표에 놓고, '
    '워크로드 성질이 바뀔 때 무엇이 뒤집히는지를 묻습니다. 분량 제한 없이 썼습니다.</p></div>')

# 절 묶음 — 목차를 접는 단위. 절 번호는 원본 순서다.
GROUPS = [('무엇을 재고 있나', 1, 3),
          ('축이 나눈 것', 4, 8),
          ('누가 서 있고 무엇이 남았나', 9, 13)]

# 도해 캡션. 값 판단은 캡션에, 판 위에는 대상과 값 라벨만(확정 규칙 §3).
CAPTION = {
    'AXIS': ('"A가 B보다 빠르다"가 성립하는 자리 다섯', xf.FIG_AXIS,
             '축 다섯으로 나눈 것은 이 글의 구분이고 원문이 그렇게 이름 붙인 것이 아닙니다. '
             '아래 상자의 값은 각 축에서 실제로 갈리는 범위를 보이려고 적은 것이며 서로 견줄 '
             '수 있는 값이 아닙니다.'),
    'BOARD': ('요청 하나가 도는 다섯 마디 — 이 판 위에 뒤의 도해를 얹습니다', xf.FIG_BOARD,
              '입력 중앙값 14만 2천 토큰, 출력 중앙값 444토큰, 턴 사이 3.84초는 SemiAnalysis가 '
              '사내 트래픽 393세션을 정제한 값입니다(2026-08). 상자 다섯은 이 글이 나눈 마디이고 '
              '원문이 센 단계 수가 아닙니다.'),
    'CROSS': ('사용자당 초당 토큰을 60에서 130으로 올리면 앞뒤가 바뀐다', xf.FIG_CROSS,
              '경계 두 값(60·130)은 2026년 2월 측정에서 나온 값이고, 곡선의 모양은 처리량과 '
              '체감 속도가 서로 반대로 움직인다는 것만 보이려고 그렸습니다 — 곡선 위 점의 높이는 '
              '실측치가 아닙니다.'),
    'DOMAIN': ('한 덩어리로 묶인 칩 수', xf.FIG_DOMAIN,
               '막대 길이는 값이 아니라 자릿수에 비례합니다 — 8과 9,216을 한 그림에 놓으면 값에 '
               '비례한 막대는 아래쪽이 안 보입니다. 짙은 줄은 지금 가장 많이 배치된 구성입니다. '
               '트레이니움 두 SKU는 랙 한 대(32칩)가 아니라 스케일업 한 덩어리 기준입니다.'),
    'MEM': ('대화 기록이 어느 마디에서 메모리를 먹나', xf.FIG_MEM,
            '위는 앞의 판을 그대로 다시 깔고 메모리를 먹는 두 마디만 짙게 한 것입니다. 아래 넷은 '
            '용량 값이며 막대가 아니라 숫자 그대로 적었습니다 — 세레브라스의 44GB는 SRAM이고 '
            '나머지 셋은 고대역폭 메모리라 같은 잣대로 견줄 수 없습니다.'),
    'INTEG': ('최고점을 찍은 쪽과 합이 큰 쪽이 다르다', xf.FIG_INTEG,
              'Kimi K2.5를 2026년 2월부터 8월까지 따라간 결과입니다. 최고점 4,081과 누적 538억·352억은 '
              '원문의 값이고, 두 선의 모양은 먼저 출발해 꾸준히 유지한 쪽과 나중에 최고점을 찍은 쪽을 '
              '갈라 보이려고 그린 것입니다 — 선 위 중간 점들은 실측치가 아닙니다.'),
    'RANK': ('메가와트당 초당 토큰 — 사용자당 100토큰 기준', xf.FIG_RANK,
             'DeepSeek V4 프로 에이전틱 작업을 2026년 9월에 잰 값입니다. 막대는 0에서 시작하고 값에 '
             '비례합니다. 맨 아래 H200만 8비트로 쟀고 나머지는 4비트라, 이 줄은 다른 조건의 값입니다.'),
    'DAY0': ('출시 당일 돈 스택은 둘이었다', xf.FIG_DAY0,
             'DeepSeek V4가 나온 2026년 4월 말부터 43일간의 기록입니다. 띠의 길이는 기간을 보이려고 '
             '그린 것이고 성능 값이 아닙니다.'),
    'SPLIT': ('판을 둘로 잘라 서로 다른 칩에 맡긴다', xf.FIG_SPLIT,
              '앞의 판을 다시 깔고 두 마디만 짙게 했습니다. 아래 상자의 회사 이름은 2026년 3월 아마존·'
              '세레브라스 협력에서 실제로 그렇게 나눈 구성이며, 이 그림이 제안하는 배치가 아닙니다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\bL\d[^()]*)\)')


def _strip(s):
    """(라벨 L12) 를 걷고 마크다운 굵게를 <b> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
         '<caption>값은 원문에 적힌 것만 옮겼고 빈칸은 그 원문에 없는 자리입니다. '
         '「언제 것」은 원문 발행일이며 성격은 공표·추정·화자 말을 갈라 적었습니다.</caption>',
         '<thead><tr>' + ''.join('<th>%s</th>' % _strip(c) for c in head) + '</tr></thead><tbody>']
    for r in body:
        h.append('<tr>' + ''.join('<td>%s</td>' % _strip(c) for c in r) + '</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def load():
    """원본을 (kind, payload) 목록으로. kind ∈ sec·p·fig·table."""
    txt = io.open(SRC, encoding='utf-8').read()
    if txt.startswith('---'):
        txt = txt.split('---', 2)[2]
    out, para, tbl = [], [], []

    def flush():
        if para:
            out.append(('p', ' '.join(para)))
            para.clear()
        if tbl:
            out.append(('table', list(tbl)))
            tbl.clear()

    for line in txt.split('\n'):
        s = line.rstrip()
        if s.startswith('## '):
            flush()
            out.append(('sec', re.sub(r'^\d+\.\s*', '', s[3:]).strip()))
        elif s.startswith('[[fig:'):
            flush()
            out.append(('fig', s[6:].rstrip(']').strip()))
        elif s.startswith('|'):
            if para:
                flush()
            tbl.append(s)
        elif not s:
            flush()
        elif s.startswith('#'):
            continue
        else:
            para.append(s.strip())
    flush()
    return out


LEAD = ('이 층은 물음 하나를 세 묶음으로 따라갑니다 — 무엇을 재고 있나, 축이 무엇을 나눴나, '
        '누가 어디 서 있고 무엇이 안 풀렸나.')


def toc_html(titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다(2026-09-05)."""
    return rt.toc_html('xpu', LEAD, GROUPS, titles)


def report_xpu(sec, p, fig):
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
        elif k == 'table':
            p(_table(v))
    return titles
