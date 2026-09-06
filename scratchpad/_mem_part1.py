# -*- coding: utf-8 -*-
"""보고서 ⑨ — 메모리 총정리. 본문은 insights/reports/mem-2026-09-06.md 에서 읽는다.

CPO 층(_cpo_part1)·선단 패키징 층(_pkg_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고
여기서 HTML 로 바꾼다 — 대시보드 HTML 은 생성물이고 고칠 것은 그 원본이다.

원본 규약
  ## N. 제목          절. 번호는 여기서 다시 센다(목차와 본문이 같은 함수에서 나온다)
  [[fig:이름]]        도해. 아래 CAPTION 의 (제목, svg, 캡션) 을 붙인다
  | … |               표 — 첫 줄이 머리, 둘째 줄이 구분선
  (라벨 L12)          출처 표기. 화면에서는 걷는다(확정 규칙 S1)

루빈 울트라 랙 지출(RACK)과 HBM4 베이스 다이(BASE)는 CPO·패키징 층의 도해를 그대로 가져온다.
여기서 다시 그리면 한쪽만 고쳐진다.
"""
import io
import os
import re

import _rep_toc as rt

import _mem_fig as mf
import _cpo_fig as cf
import _pkg_fig as pf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'mem-2026-09-06.md')

HEAD_MEM = (
    '<div class="rep-head"><span class="rn">보고서 ⑨</span>'
    '<h2 id="rep-mem">메모리 총정리 — 40년 만에 모자란데 왜 만드는 회사가 안 웃나</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 뉴스레터 5편 · 링크드인 석 달치 · 한국어 해설 11편 · '
    '영문 클리핑 2편</b> · 원문 기간 <b>2026-02 ~ 2026-09</b><br>'
    'D램과 HBM 값이 40년 만에 가장 크게 오른 국면을 한데 놓고, 그런데 왜 삼성전자·SK하이닉스·'
    '마이크론의 손에 그만큼 안 남는지를 묻습니다. 패키징 공정과 냉각은 보고서 ⑥·⑦이, 환율과 '
    '금리는 보고서 ⑧이 맡습니다. 분량 제한 없이 썼습니다.</p></div>')

# 절 묶음 — 목차를 접는 단위. 절 번호는 원본 순서다.
GROUPS = [('모자란데 왜 안 남나', 1, 5),
          ('누가 값을 정하고 누가 반격하나', 6, 9),
          ('중국·청구서·다음 판', 10, 13)]

# 도해 캡션. 값 판단은 캡션에, 판 위에는 대상만(확정 규칙 §3).
CAPTION = {
    'MAP': ('값은 올랐는데 만드는 회사 손에 안 남는 세 자리', mf.FIG_MAP,
            '이 글이 따라가는 세 갈래입니다. ① 값이 오르는 속도와 매출에 잡히는 속도가 다르고, '
            '② 가장 큰 고객이 가장 싸게 사고, ③ 사는 회사들이 반격을 시작했습니다. 상자는 이 글의 '
            '절 배열이고 원문이 센 수가 아닙니다. 값은 그리지 않았습니다.'),
    'WAFER': ('같은 웨이퍼 한 장에서 HBM 은 비트를 훨씬 적게 낸다', mf.FIG_WAFER,
              '왼쪽은 웨이퍼 한 장이 내는 비트를 견준 것입니다. HBM3E 12단 기준으로 범용 D램 웨이퍼가 '
              'HBM 웨이퍼보다 약 3배, HBM4 로 넘어가면 약 4배 많은 비트를 냅니다(SemiAnalysis '
              '2026-02). 그래서 HBM 을 늘리면 범용에 쓸 웨이퍼 수가 줄고 같은 웨이퍼가 내는 비트도 '
              '줄어 두 번 맞습니다. 오른쪽은 전체 D램 생산능력에서 HBM 이 차지하는 몫이고 뒤 둘은 '
              '전망치입니다. 두 묶음은 눈금이 다릅니다.'),
    'PRICE': ('같은 HBM4 를 누가 사느냐로 값이 갈린다', mf.FIG_PRICE,
              'SemiAnalysis 가 추정한 2027년 HBM4 값입니다(2026-09). SK하이닉스가 엔비디아에 파는 값이 '
              'Gb당 3.0~3.3달러인데 다른 1군 고객에게는 3.7~4.1달러입니다. 인상률로 보면 엔비디아向만 '
              '전년 대비 약 70%이고 삼성向은 98%입니다. 막대 높이는 범위의 위 끝이고, 세 묶음은 '
              '눈금이 다릅니다. 전부 추정치이며 실제 협상 결과는 다를 수 있다고 원문이 밝혔습니다.'),
    'RACK': ('루빈 울트라 NVL576 랙 지출 — HBM 을 깎자 스케일업 네트워킹이 세 배', cf.FIG_RACK,
             '보고서 ⑥에서 그린 그림을 그대로 가져왔습니다. 엔비디아가 루빈 울트라의 HBM 을 깎자 랙 '
             '지출에서 메모리가 차지하는 몫이 40%에서 28%로 내려가고, 아낀 몫이 스케일업 네트워킹으로 '
             '옮겨 가 4%에서 12%로 세 배가 됐습니다(SemiAnalysis 2026-09-02). 기둥 하나가 랙 지출 '
             '100%이고 나머지 항목은 원문에 없어 비워 두었습니다.'),
    'CXMT': ('CXMT 는 웨이퍼로는 3위를 노리는데 HBM 은 거의 안 만든다', mf.FIG_CXMT,
             '왼쪽은 2026년 말 웨이퍼 생산능력 전망이고 CXMT 가 마이크론에 다가섭니다. 오른쪽은 그 '
             '회사가 실제로 웨이퍼를 어디에 쓰는지로, 2025년 말 기준 265kwspm 가운데 HBM 에 배정된 것은 '
             '5kwspm, 약 2%뿐입니다(SemiAnalysis 2026-06). 범용 D램이 마진도 좋고 웨이퍼당 비트도 '
             '3배 이상 나오기 때문입니다. 왼쪽은 전망치, 오른쪽은 실적입니다.'),
    'BASE': ('HBM4 베이스 다이 — 짙은 칸을 누구 공정으로 굽나', pf.FIG_BASE,
             '보고서 ⑦에서 그린 그림을 그대로 가져왔습니다. 줄마다 같은 HBM 을 그리고 그 회사가 고른 '
             '베이스 다이 공정만 짙게 했습니다. SK하이닉스는 자체 로직 파운드리가 없어 TSMC 에 맡기고 '
             '삼성전자는 SF4 로 자기 안에서 해결합니다(ISSCC 2026-02). 위에 그린 D램 코어 다이 넉 장은 '
             '표시용이고 실제 층수가 아닙니다.'),
    'NEXT': ('HBM 위에 무엇을 한 층 더 얹을 것인가 — 두 진영', mf.FIG_NEXT,
             '아래 두 층은 두 진영이 같고 다른 것은 맨 위 한 칸뿐이라 같은 꼴로 나란히 그렸습니다. '
             'SK하이닉스는 샌디스크·구글과 HBF 를 만들며 2026년 하반기 샘플에 2027년 양산 일정을 '
             '공개했고, 삼성전자의 zHBM 은 상용화 시점이 없는 개념 모델이라 점선으로 뒀습니다'
             '(2026년 8월 FMS). 두 진영의 성능 값은 각 회사 주장이라 판에 안 올렸습니다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\b[LT]\d[^()]*)\)')


def _strip(s):
    """(라벨 L12)·(라벨 T44) 를 걷고 마크다운 굵게를 <b> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
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


LEAD = ('이 층은 물음 하나를 세 묶음으로 따라갑니다 — 모자란데 왜 안 남나, '
        '누가 값을 정하고 누가 반격하나, 중국과 청구서와 다음 판.')


def toc_html(titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다(2026-09-05)."""
    return rt.toc_html('mem', LEAD, GROUPS, titles)


def report_mem(sec, p, fig):
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
