# -*- coding: utf-8 -*-
"""보고서 ⑩ — AI 모델 기술 문서. 본문은 insights/reports/aimodel-2026-10-02.md 에서 읽는다.

다른 층은 에세이 꼴(절 · 문단 · 표)이다. 이 층은 사용자 지시(2026-10-02, 「포맷 맞추지 말고
진짜 기술 문서처럼」)로 기술 문서 꼴을 쓴다 — 소절 · 수식 블록 · 번호 목록이 더 있다.
차례와 절 번호만은 _rep_toc 규약을 그대로 따른다(check_toc 가 문다).

원본 규약
  ## N. 제목          절. 번호는 여기서 다시 센다
  ### N.M 제목        소절. 번호는 원본에 적힌 그대로 둔다
  [[fig:이름]]        도해. _aimodel_fig 의 FIG_이름 과 아래 CAPTION
  | … |               표 — 첫 줄이 머리, 둘째 줄이 구분선
  ``` … ```           수식 · 유도 블록. 고정폭으로 낸다
  ①②③ 로 시작하는 줄   번호 목록. 한 줄에 하나
  (라벨 L12)          출처 표기. 화면에서는 걷는다(확정 규칙 S1)
"""
import html
import io
import os
import re

import _rep_toc as rt

import _aimodel_fig as af

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'aimodel-2026-10-02.md')

HEAD_AIMODEL = (
    '<div class="rep-head"><span class="rn">보고서 ⑩</span>'
    '<h2 id="rep-aimodel">AI 모델 기술 문서 — 구조 · 학습 · 추론 · 경쟁</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 영문 원문 21편</b> · 원문 기간 <b>2025-01 ~ 2026-09</b><br>'
    '전문가 혼합 · 어텐션 · KV 캐시 · 임베딩 메모리 · 사전학습 · 강화학습 시스템 · 추론 단계 · '
    '오픈 대 클로즈드 격차를 사양표와 유도식으로 정리했습니다.</p></div>')

GROUPS = [('모델 구조', 1, 6),
          ('학습', 7, 12),
          ('추론에서 드러나는 성질', 13, 15),
          ('경쟁 구도와 한계', 16, 18)]

# 이 층에만 있는 붓 — 수식 블록 · 소절 · 번호 목록. gen_report_dashboard 의 REPORT_CSS 에 붙는다
CSS = """
  .am-h4{margin:22px 0 8px;font-size:15px;font-weight:800;color:var(--ink)}
  .am-eq{margin:10px 0 16px;padding:12px 14px;border:1px solid var(--line);border-radius:10px;
         background:var(--paper-2,var(--accent-soft));font:12.5px/1.65 ui-monospace,SFMono-Regular,
         Menlo,Consolas,monospace;color:var(--ink);white-space:pre;overflow-x:auto}
  .am-ol{margin:6px 0 14px;padding:0;list-style:none}
  .am-ol li{margin:0 0 6px;padding-left:1.6em;text-indent:-1.6em;line-height:1.75}
"""

# 도해 캡션 — 읽는 법과 출처만. 판단은 본문이 맡는다(확정 규칙 §5·§7).
CAPTION = {
    'MOE': ('전문가 혼합 한 층 — GLM-5', af.FIG_MOE,
            '개수(256 · 8 · 1)는 GLM-5.x 사양이다(2026-09). 짙은 칸의 자리는 보기용이고, '
            '실제로는 토큰마다 다른 8개가 고른다.'),
    'ATTN': ('어텐션의 세 갈래', af.FIG_ATTN,
             '갈래 구분은 이 문서의 것이다. 상자 아래 모델은 원문이 그 방식을 쓴다고 밝힌 모델이다.'),
    'ENGRAM': ('Engram 조회 경로', af.FIG_ENGRAM,
               '표 크기와 읽는 양은 SemiAnalysis가 DeepSeek-V4.1-Flash를 서빙하며 잰 값이다(2026-09).'),
    'MFU': ('학습 일곱 건의 MFU', af.FIG_MFU,
            '정밀도와 장비가 줄마다 달라 같은 조건의 순위가 아니다. 짙은 줄이 MoE 학습이다. '
            '2025-08 학습 벤치마크 글과 2026-06 RL 시스템 글의 값이다.'),
    'RLLOOP': ('RL 학습 한 걸음', af.FIG_RLLOOP,
               '상자 넷은 RL 시스템 글(2026-06)이 나눈 행위자와 큐다.'),
    'RLCASE': ('학습기가 기다린 시간 비율', af.FIG_RLCASE,
               '2026-06 RL 시스템 글의 실험 넷이다. 모델·장비·배치가 사례마다 달라 서로 견줄 조건은 아니다.'),
    'REGIONS': ('추론의 네 운영 영역', af.FIG_REGIONS,
                '영역 구분과 병목은 2026-09 추론 연산 글의 것이다. 수치는 그리지 않았다.'),
    'GAP': ('격차가 닫히는 데 걸린 개월', af.FIG_GAP,
            '2026-08 오픈 대 클로즈드 글의 수치다. 초기 스케일링 시대는 원문이 개월 수를 적지 않았다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\bL\d[^()]*)\)')
_CIRC = re.compile(r'^[①-⑳]')


def _strip(s):
    """(라벨 L12) 를 걷고 마크다운 굵게·코드를 태그로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s.strip()


def _table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]
    h = ['<div class="biz-tw"><table class="biz-t">',
         '<caption>수치는 원문 글자에 있는 것만 옮겼고 「—」는 원문에 없는 자리입니다. '
         '「언제 것」은 값이 가리키는 시점, 「성격」은 공표 · 추정 · 판단 · 회사 주장 · 측정입니다.</caption>',
         '<thead><tr>' + ''.join('<th>%s</th>' % _strip(c) for c in head) + '</tr></thead><tbody>']
    for r in body:
        h.append('<tr>' + ''.join('<td>%s</td>' % _strip(c) for c in r) + '</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)


def load():
    """원본을 (kind, payload) 목록으로. kind ∈ sec·h4·p·ol·eq·fig·table."""
    txt = io.open(SRC, encoding='utf-8').read()
    if txt.startswith('---'):
        txt = txt.split('---', 2)[2]
    out, para, tbl, ol, eq = [], [], [], [], None

    def flush():
        if para:
            out.append(('p', ' '.join(para)))
            para.clear()
        if tbl:
            out.append(('table', list(tbl)))
            tbl.clear()
        if ol:
            out.append(('ol', list(ol)))
            ol.clear()

    for line in txt.split('\n'):
        s = line.rstrip()
        if eq is not None:
            if s.startswith('```'):
                out.append(('eq', '\n'.join(eq)))
                eq = None
            else:
                eq.append(s)
            continue
        if s.startswith('```'):
            flush()
            eq = []
        elif s.startswith('## '):
            flush()
            out.append(('sec', re.sub(r'^\d+\.\s*', '', s[3:]).strip()))
        elif s.startswith('### '):
            flush()
            out.append(('h4', s[4:].strip()))
        elif s.startswith('[[fig:'):
            flush()
            out.append(('fig', s[6:].rstrip(']').strip()))
        elif s.startswith('|'):
            if para or ol:
                flush()
            tbl.append(s)
        elif _CIRC.match(s.strip()):
            if para or tbl:
                flush()
            ol.append(s.strip())
        elif not s:
            flush()
        elif s.startswith('#'):
            continue
        else:
            if ol:
                flush()
            para.append(s.strip())
    flush()
    return out


LEAD = ('이 문서는 네 부로 나뉩니다 — 모델이 어떻게 생겼나, 어떻게 학습되나, '
        '서빙에서 어떤 성질로 드러나나, 누가 어느 모델로 앞서 있나.')


def toc_html(titles):
    return rt.toc_html('aimodel', LEAD, GROUPS, titles)


def report_aimodel(sec, p, fig):
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
        elif k == 'h4':
            p('<h4 class="am-h4">%s</h4>' % html.escape(v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'ol':
            p('<ul class="am-ol">' + ''.join('<li>%s</li>' % _strip(x) for x in v) + '</ul>')
        elif k == 'eq':
            p('<pre class="am-eq">%s</pre>' % html.escape(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'table':
            p(_table(v))
    return titles
