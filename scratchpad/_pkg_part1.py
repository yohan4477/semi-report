# -*- coding: utf-8 -*-
"""보고서 ⑦ — 선단 패키징 총정리. 본문은 insights/reports/pkg-2026-09-05.md 에서 읽는다.

CPO 층(_cpo_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고 여기서 HTML 로 바꾼다 —
대시보드 HTML 은 생성물이고 고칠 것은 그 원본이다.

원본 규약
  ## N. 제목          절. 번호는 여기서 다시 센다(목차와 본문이 같은 함수에서 나온다)
  [[fig:이름]]        도해. _pkg_fig 의 FIG_이름 과 아래 CAPTION 의 캡션을 붙인다
  | … |               표 — 첫 줄이 머리, 둘째 줄이 구분선
  (라벨 L12)          출처 표기. 화면에서는 걷는다(확정 규칙 S1)
"""
import io
import os
import re

import _pkg_fig as pf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'pkg-2026-09-05.md')

HEAD_PKG = (
    '<div class="rep-head"><span class="rn">보고서 ⑦</span>'
    '<h2 id="rep-pkg">선단 패키징 총정리 — 다이 하나로 못 만들게 된 뒤 무엇이 그 자리를 대신했나</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 뉴스레터 9편 · Semi Doped 1회차 · 영문 클리핑 2편</b> · '
    '원문 기간 <b>2025-08 ~ 2026-07</b> · 유료 뉴스레터 원문<br>'
    '2.5D·3D 패키징을 다룬 원문을 한데 놓고, 다이를 쪼개게 된 뒤 무엇이 그 일을 대신했고 '
    '어디서 막혔는지를 묻습니다. 빛으로 잇는 이야기는 보고서 ⑥이 맡습니다. 분량 제한 없이 '
    '썼습니다.</p></div>')

# 절 묶음 — 목차를 접는 단위. 절 번호는 원본 순서다.
GROUPS = [('왜 쪼개고 어떻게 붙이나', 1, 5),
          ('누가 무엇을 내놓았나', 6, 9),
          ('어디가 막히고 누가 서 있나', 10, 13)]

# 도해 캡션. 값 판단은 캡션에, 판 위에는 대상만(확정 규칙 §3).
CAPTION = {
    'RETICLE': ('레티클 한 장이 다이의 최대 크기이고, 패키지는 그보다 커야 한다', pf.FIG_RETICLE,
                '작은 사각형 하나가 노광기가 한 번에 새기는 최대 면적입니다. 26mm × 33mm, '
                '858제곱밀리미터이고 다이는 그보다 클 수 없습니다. H100 이 이미 그 한계에 닿아 있었고 '
                '그레이스 블랙웰이 둘, 루빈이 넷을 붙입니다(Semi Doped 2026-06). 다이 개수는 원문이 센 '
                '수이고, 바깥 패키지 테두리의 크기는 실제 레티클 배수에 비례하지 않습니다.'),
    'BRANCH': ('CoWoS 세 갈래와 EMIB — 가운데 층을 무엇으로 두나', pf.FIG_BRANCH,
               '넷을 같은 꼴로 그리고 가운데 층만 다르게 했습니다. CoWoS-S 는 실리콘 인터포저, '
               'CoWoS-R 은 유기 RDL(재배선층, 유기 절연막 위에 구리 배선을 여러 겹 그은 판), '
               'CoWoS-L 은 유기 가운데 실리콘 브리지를 박은 것이고, EMIB 는 '
               '가운데 층을 아예 빼고 브리지를 아래 기판 안에 심습니다. 짙은 칸이 실리콘입니다. '
               '층 구분과 이름은 Semi Doped 진행자의 설명(2026-06)이고 값은 없습니다.'),
    'PANEL': ('원형 웨이퍼에서 사각 패널로', pf.FIG_PANEL,
              '원 안에서 사각형을 잘라 내면 가장자리가 버려집니다. 패널은 그 손실이 없고 한 번에 '
              '더 큽니다. 도형은 한 변 길이에 비례해 그렸습니다. Semi Doped 진행자는 500mm × 500mm '
              '패널이 300mm 웨이퍼보다 다섯에서 여섯 배 크다고 말했는데(2026-06), 그림에 세운 것은 '
              'ECTC 2026 에 실제로 나온 판들입니다(2026-07). 웨이퍼와 패널을 면적으로 견준 값은 '
              '원문에 없어 그리지 않았습니다.'),
    'PITCH': ('접합점 간격이 좁아지면서 붙이는 방법이 바뀐다', pf.FIG_PITCH,
              '위 셋은 솔더를 녹여 붙이는 마이크로범프이고 아래 둘은 구리 면끼리 직접 붙이는 '
              '하이브리드 본딩입니다. 45µm 는 지금 출하 중인 그래나이트 래피즈, 25µm 는 EMIB-T 의 '
              '다음 목표이며 그 아래부터 솔더 부피가 모자랍니다(ECTC 2026-07). 450나노미터는 웨이퍼 '
              '대 웨이퍼 시험 결과입니다. 45µm 와 450나노미터가 백 배 차이라 위아래 간격은 순서만 '
              '보이고 값에 비례하지 않습니다.'),
    'YIELD': ('층당 99%가 쌓이면 스택 수율이 이렇게 내려간다', pf.FIG_YIELD,
              '네모 하나가 접합 한 번입니다. 8층은 일곱 번, 12층은 열한 번 붙이고, 층 하나의 수율을 '
              '99%로 잡으면 스택 전체가 약 92%와 약 87%가 됩니다. 접합 횟수와 두 백분율은 모두 원문의 '
              '값입니다(SemiAnalysis 2025-08). 원문은 실제로는 결함이 쌓여 이 계산보다 나쁘다고 '
              '덧붙였습니다.'),
    'MONEY': ('InFO 를 CoWoS 가 넘어섰다', pf.FIG_MONEY,
              'SemiAnalysis 추정입니다(2026-01). 애플이 개발비를 내 만든 InFO 가 2018년 6억 달러였을 때 '
              'CoWoS 는 1억 1,800만 달러였고, 2022년에 순서가 뒤집혀 2025년 CoWoS 가 96억 달러가 '
              '됐습니다. 2025년 InFO 는 같은 원문이 한 곳에 84억 달러, 다른 곳에 38억 달러로 적어 둘 다 '
              '그렸고 뒤엣것을 점선으로 뒀습니다. 어느 값이 맞는지는 원문만으로 정할 수 없습니다. '
              '막대 높이는 값에 비례합니다.'),
    'EMIBT': ('브리지에 구멍을 뚫자 전력이 곧장 올라간다', pf.FIG_EMIBT,
              '화살표가 전력이 가는 길입니다. 기존 EMIB 는 브리지가 있는 곳을 옆으로 비켜 올라가고, '
              'EMIB-T 는 브리지에 낸 TSV 로 곧장 올라갑니다. 인텔은 이것으로 직류 전압강하를 '
              '68~80% 줄였다고 밝혔습니다(ECTC 2026-07, 회사 발표). 화살표 개수는 경로를 보이려고 '
              '그린 것이고 실제 전력 배선 수가 아닙니다.'),
    'MULT': ('패키지가 레티클의 몇 배까지 가나', pf.FIG_MULT,
             'Semi Doped 진행자 둘이 정리한 값입니다(2026-06). 왼쪽 셋은 TSMC CoWoS 이고 오른쪽 둘은 '
             '인텔 EMIB-T 입니다. 막대 높이는 배수에 비례합니다. 그다음으로 거론되는 System on Wafer 는 '
             '40배쯤을 겨누는데 시점이 확실치 않다고 해서 막대로 안 그렸습니다.'),
    'BASE': ('HBM4 베이스 다이 — 짙은 칸을 누구 공정으로 굽나', pf.FIG_BASE,
             '줄마다 같은 HBM 을 그리고 그 회사가 고른 베이스 다이 공정만 짙게 했습니다. HBM4 부터 '
             '베이스 다이만 첨단 로직 공정으로 넘어갔는데 세 회사가 갈렸습니다(ISSCC 2026-02). 위에 '
             '그린 D램 코어 다이 넉 장은 표시용이고 실제 층수가 아닙니다. 실제 삼성 HBM4 는 12층입니다.'),
    'COOL': ('같은 시험차량에서 뽑아낸 열 (kW)', pf.FIG_COOL,
             'TSMC 가 CoWoS-R 기반 시험차량에서 낸 값입니다(ECTC 2026-07, 회사 발표). SoC 다이 넷과 '
             'HBM 스택 여덟을 얹은 같은 물건에서 냉각 방식만 바꿔 쟀습니다. 냉각판 둘은 유량을 분당 '
             '4리터 이상 올려도 더 안 늘었고 그 병목이 열계면 소재였습니다. 실리콘 표면에 미세기둥을 '
             '직접 새기면 그 소재를 건너뜁니다. 범위 값은 위 끝 높이로 그렸습니다.'),
    'CHAIN': ('HBM4 한 덩어리가 손을 네 번 바꾼다', pf.FIG_CHAIN,
              'SemiAnalysis 가 그린 분담(2025-08)을 끝에서 끝까지 그렸습니다. 상자 안 이름은 원문에 '
              '나온 회사만입니다. 짙은 칸이 마지막 조립인 것은 이 글의 판단입니다. 이 사슬 아래에 '
              '깔리는 패키지 기판을 만드는 회사는 원문 열두 편 어디에도 이름이 없어 그리지 못했습니다.'),
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
         '<caption>값은 그 회사가 발표했거나 SemiAnalysis 가 적은 것이고, 빈칸은 원문에 없는 자리입니다. '
         '「언제 것」은 원문 발행일이며 성격은 공표·추정·전언을 갈라 적었습니다.</caption>',
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


def _circ(n):
    """소단원 번호 ①②③. 대단원은 「1. 2. 3.」이고 그 아래가 동그라미다."""
    return chr(0x2460 + n - 1) if 1 <= n <= 20 else str(n)


def toc_html(titles):
    """묶음 이름은 제 줄에, 절은 한 줄에 하나씩. 「·」로 이으면 어디서 절이 갈리는지 안 보인다(2026-09-05)."""
    parts = ['<p class="rep-toc"><b class="tl">이 층은 물음 하나를 세 묶음으로 따라갑니다 — 왜 쪼개고 어떻게 붙이나, 누가 무엇을 내놓았나, 어디가 막히고 누가 서 있나.</b>']
    for name, a, b in GROUPS:
        links = '<br>'.join('<a href="#pkg-%d">%s %s</a>' % (i, _circ(i), titles[i - 1])
                           for i in range(a, b + 1))
        parts.append('<b class="tg">%d. %s</b><span class="tt">%s</span>'
                     % (GROUPS.index((name, a, b)) + 1, name, links))
    return ''.join(parts) + '</p>'


def report_pkg(sec, p, fig):
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig') and not toc_done:
            p(toc_html(titles))
            toc_done = True
        if k == 'sec':
            sec('%s %s' % (_circ(titles.index(v) + 1), v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'table':
            p(_table(v))
    return titles
