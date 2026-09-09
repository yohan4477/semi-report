# -*- coding: utf-8 -*-
"""보고서 「모델 총정리」 층. 본문은 insights/reports/model-2026-09-09.md 에서 읽는다.

트럼프 층(_trump_part1)과 같은 규약이다. 산문은 마크다운 원본에 두고 여기서 HTML 로
바꾼다. 차례와 절 번호는 _rep_toc 가 붙인다 — 층마다 복사하지 않는다.

이 층만 다른 것 하나 — 재료가 남이 공개한 계산기이고 산출물이 그것을 다시 세운
코드다. 그래서 값의 출처가 셋이다. 원문 글자(줄 번호로 인용), 원문이 실은 표 그림
(그림 번호로 밝힌다), 우리 모델 출력(scratchpad/model_facts.md 가 정본). 표의 「성격」
열이 셋 중 어느 것인지를 가른다.
"""
import io
import os
import re

import _rep_toc as rt
import _model_fig as mf
import _model_tbl as mt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'insights', 'reports', 'model-2026-09-09.md')

HEAD_MODEL = (
    '<div class="rep-head"><span class="rn">보고서 ⑪</span>'
    '<h2 id="rep-model">모델 총정리 — 남이 공개한 계산기를 다시 세우면 어디가 맞고 '
    '어디가 어긋나나</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 영문 클리핑 2편</b>과 그 안의 표 그림 7장 · '
    '한국어 변환본 1편<br>'
    '값의 출처가 셋입니다. 원문 글자는 줄 번호로 인용하고, 원문이 실은 표 그림에서 읽은 값은 '
    '몇 번 그림인지 밝히고, 우리 모델이 낸 값은 표의 「성격」 열에 적었습니다. 그림에서 읽은 '
    '값은 픽셀이라 자릿수 오독 가능성이 남습니다. 모델 코드는 '
    '<code>insights/models/</code> 에 있고 검사기가 매번 발표치와 대조합니다.</p></div>')

GROUPS = [('무엇을 왜 다시 세우나', 1, 2),
          ('학습 클러스터 — 고장이 원가가 되는 길', 3, 5),
          ('추론 — 서버 값이 원가가 되는 길', 6, 8),
          ('남은 것', 9, 9)]

LEAD = ('리서치 회사가 낸 표를 옮겨 적는 대신 그 표를 만든 계산을 다시 세웠습니다. '
        '큰 층은 달러 단위까지 맞았고, 두 글 모두 안쪽 한 층에서 어긋났습니다. '
        '어긋난 방식이 서로 달랐다는 것이 이 글의 물음입니다.')

CAPTION = {
    'STACK': ('청구서에 찍히는 다섯 줄과 안 찍히는 세 줄', mf.FIG_STACK,
              '그림 016 의 Hyperscaler 열입니다. 여덟 줄이 다 0 이 아닌 유일한 열이라 '
              '사슬이 안 끊깁니다. 막대는 GPU 한 줄이 나머지의 서른 배라 제곱근 눈금으로 '
              '눌러 세웠으므로 길이 비를 그대로 읽으면 안 됩니다. 설치비는 일시금 '
              '14,996,587 달러를 36개월로 나눈 값입니다. 굿풋 손실이 GPU 비용에만 붙는다는 '
              '규칙은 표에 안 적혀 있고 결과 값에서 거꾸로 읽어 확인한 것입니다.'),
    'GOODPUT': ('같은 고장인데 곱해지는 장수가 예순네 배 다르다', mf.FIG_GOODPUT,
                '수식은 원문 L131 의 셋이고 값은 그림 019 의 대규모 학습 설정입니다. '
                '이 그림이 말하는 것은 시간이 아니라 곱해지는 대상입니다 — 체크포인트 '
                '재시작은 작업 크기 전체를 곱하고, 고장을 견디는 방식은 수리 시간에 폭발 '
                '반경만 곱합니다. 막대는 수리 시간에 곱해지는 장수이고 제곱근 눈금입니다. '
                '잃는 시간의 절대값은 설정마다 달라 안 그렸습니다.'),
    'CHAIN': ('서버 값 한 줄이 GPU 시간당 단가가 되기까지', mf.FIG_CHAIN,
              '값은 MI300X 열이고 출처는 그림 049 와 050 입니다. 점선 상자는 이 글이 안 '
              '다루는 마디입니다 — 추론 원가 글에는 굿풋 항이 없습니다. WACC 13.25% 는 '
              '표에 찍힌 13.3% 가 아니라 우리가 발표된 월 자본비에서 역산한 값입니다(7절). '
              '아래 상자의 월 시간 차이는 두 글을 섞을 때 실제로 걸리는 자리입니다.'),
    'THRESHOLD': ('문턱 0.82를 넘느냐로 소유의 답이 갈린다', mf.FIG_THRESHOLD,
                  '점과 가로 막대는 원문이 낸 손익분기 임대료(L298·L302·L306)를 H200 시세 '
                  '2.5달러로 나눈 비율입니다. 값 하나뿐인 줄은 점으로, 구간인 줄은 막대로 '
                  '냈습니다. 처리량을 직접 잰 값이 아니라 임대료를 뒤집어 '
                  '낸 값이라 원문의 계산이 옳다는 전제 위에 섭니다. 왼쪽 세로선 0.82 는 '
                  '원문에 없고 우리가 자기 TCO 로 계산한 문턱입니다. 오른쪽 점선 1.00 은 '
                  '빌릴 때의 문턱입니다.'),
}

_CITE = re.compile(r'\s*\(([^()]*?\b(?:[LT]\d|[a-z]\d)[^()]*)\)')


def _strip(s):
    """(라벨 L12) 를 걷고 마크다운 굵게를 <b> 로, 백틱을 <code> 로."""
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
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


TBL_NOTE = {
    'TCO': '굿풋 줄은 발표된 백분율(소수 둘째 자리)로 계산했습니다. 그 반올림 때문에 '
           '발표치와 최대 700달러 차이가 납니다. 나머지 칸은 달러까지 같습니다.',
    'GOOD': '「수식대로」는 원문 L131 의 식에 그림의 입력을 그대로 넣은 값입니다. '
            '세 줄이 어긋나고 빠진 항이 줄마다 다릅니다.',
    'IMPACT': '「36개월 발표」는 그림 016 에서 읽은 값이고 「36개월 수식」은 굿풋을 '
              '원문 식으로 다시 계산해 넣은 값입니다.',
    'CAPEX': 'WACC 는 표에 찍힌 13.3%가 아니라 역산한 13.25%입니다(7절). B200 의 '
             '서버당 선불이 발표치보다 1달러 큰 것은 발표 표의 항목별 반올림 때문입니다.',
    'OPEX': '전기는 정격이 아니라 가동률과 PUE 를 거친 값입니다. 여섯 SKU 가 같은 '
            '단가를 쓰므로 차이는 서버 전력에서만 납니다.',
    'TOTAL': '맨 아래 줄은 원문에 없습니다. H200 을 1 로 놓고 각 SKU 가 사서 쓸 때 '
             '넘어야 할 처리량 비율을 우리가 계산한 것입니다.',
}


def table_html(key):
    """원문 계산기의 칸을 그대로 세운다. 값은 _model_tbl 의 모델이 낸 것이다."""
    title, fn = mt.TABLES[key]
    head, body = fn()
    h = ['<p class="ins-lede"><b>%s</b></p>' % title,
         '<div class="biz-tw"><table class="biz-t"><thead><tr>']
    h += ['<th>%s</th>' % c for c in head]
    h.append('</tr></thead><tbody>')
    for r in body:
        h.append('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>')
    h.append('</tbody></table></div>')
    h.append('<p class="ins-lede">%s</p>' % TBL_NOTE[key])
    return ''.join(h)


def load():
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
        elif s.startswith('[[tbl:'):
            flush()
            out.append(('tbl', s[6:].rstrip(']').strip()))
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


def toc_html(titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다(2026-09-05)."""
    return rt.toc_html('model', LEAD, GROUPS, titles)


def report_model(sec, p, fig):
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig', 'tbl') and not toc_done:
            p(toc_html(titles))
            toc_done = True
        if k == 'sec':
            sec(rt.sec_title(titles.index(v) + 1, v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'tbl':
            p(table_html(v))
        elif k == 'table':
            p(_table(v))
    return titles
