# -*- coding: utf-8 -*-
"""보고서 「모델링」 섹션의 층 둘. 본문은 insights/reports/model-*-2026-09-09.md 다.

한 섹션에 카드 둘이다. 클러스터 총소유비용과 추론 원가는 재료도 다르고 어긋난
자리도 달라 한 글로 묶으면 절이 열넷이 된다. 섹션 id 를 같이 쓰면 dash_common 이
한 <section> 으로 묶어 준다 — check_report 는 그 섹션을 통째로 잘라 숫자를 본다.

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
import _model_eq as me

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_C = os.path.join(ROOT, 'insights', 'reports', 'model-cluster-2026-09-09.md')
SRC_I = os.path.join(ROOT, 'insights', 'reports', 'model-infer-2026-09-09.md')

_NOTE = ('값의 출처가 셋입니다. 원문 글자는 줄 번호로 인용하고, 원문이 실은 표 그림에서 '
         '읽은 값은 몇 번 그림인지 밝히고, 우리 모델이 낸 값은 표의 「성격」 열이나 '
         '캡션에 적었습니다. 그림에서 읽은 값은 픽셀이라 자릿수 오독 가능성이 남습니다. '
         '모델 코드는 <code>insights/models/</code> 에 있고 검사기가 매번 발표치와 '
         '대조합니다.')


def _head(num, anchor, title, base):
    return ('<div class="rep-head"><span class="rn">보고서 %s</span>'
            '<h2 id="rep-%s">%s</h2>'
            '<p class="rm">바탕 <b>%s</b><br>%s</p></div>' % (num, anchor, title, base, _NOTE))


HEAD_CLUSTER = _head('⑪', 'model-cluster',
                     '클러스터 총소유비용 — 발표된 계산기를 다시 세우면 굿풋에서 어긋난다',
                     'SemiAnalysis 영문 클리핑 1편과 그 안의 표 그림 4장 · 한국어 변환본 1편')
HEAD_INFER = _head('⑫', 'model-infer',
                   '추론 원가 — 어긋난 여덟 칸은 반올림이었고, 빌릴 때와 살 때 답이 뒤집힌다',
                   'SemiAnalysis 영문 클리핑 1편과 그 안의 표 그림 3장')

GROUPS_CLUSTER = [('무엇을 왜 다시 세우나', 1, 2),
                  ('고장이 원가가 되는 길', 3, 5),
                  ('남은 것', 6, 6)]

GROUPS_INFER = [('서버 값에서 시간당 단가까지', 1, 2),
                ('답이 갈리는 자리', 3, 3),
                ('남은 것', 4, 4)]

LEAD_CLUSTER = ('리서치 회사가 낸 표를 옮겨 적는 대신 그 표를 만든 계산을 다시 세웠습니다. '
                '총소유비용 표는 달러 단위까지 맞았고, 그 안에 든 굿풋 표는 세 칸이 자기네 '
                '공표 수식과 어긋났습니다. 빠진 항이 시나리오마다 다릅니다.')

LEAD_INFER = ('같은 방법을 추론 칩 비교에 씁니다. 자본비가 어긋난 모양이 반올림의 지문이라 '
              '역산으로 풀렸고, 원문이 임대 시장으로만 답한 물음을 소유 기준으로 다시 풀면 '
              '작업 종류에 따라 답이 뒤집힙니다.')

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
              '표에 찍힌 13.3% 가 아니라 우리가 발표된 월 자본비에서 역산한 값입니다(2절). '
              '아래 상자의 월 시간 차이는 두 글을 섞을 때 실제로 걸리는 자리입니다.'),
    'THRESHOLD': ('문턱 둘이 축을 세 구간으로 나눈다', mf.FIG_THRESHOLD,
                  '왼쪽에서 오른쪽으로 읽습니다. 가로축은 MI300X 가 H200 대비 내는 '
                  '처리량이고, 세로선 둘이 축을 세 구간으로 나눕니다. 왼쪽 굵은 선 0.82 는 '
                  '두 SKU 의 자기 TCO 비($1.34 ÷ $1.63)이고 원문에 없습니다. 오른쪽 점선 '
                  '1.00 은 임대료 비($2.50 ÷ $2.50)입니다. 띠 안의 말이 그 구간에 떨어진 '
                  '작업의 결론이고, 가운데 짙은 구간이 사느냐 빌리느냐로 답이 갈리는 '
                  '자리입니다. 아래 세 줄은 각 작업의 처리량이며, 원문이 낸 손익분기 '
                  '임대료(L298·L302·L306)를 H200 시세로 나눠 얻었습니다 — 처리량을 직접 잰 '
                  '값이 아니라 원문의 계산이 옳다는 전제 위에 섭니다.'),
}


_CITE = re.compile(r'\s*\(([^()]*?\b(?:[LT]\d|[a-z]\d)[^()]*)\)')


EST = '<span class="tag-est">추정</span>'

# 값이 원문에서 바로 안 나오고 우리가 고른 가정 위에 서는 표. 머리 띠에 배지를 단다
TBL_EST = {'GAP'}


def _strip(s):
    """(라벨 L12) 를 걷고 마크다운 굵게를 <b> 로, 백틱을 <code> 로.

    문단이 [추정] 으로 시작하면 그 자리에 배지를 단다 — 가정 위에 선 대목은
    읽기 시작할 때 알아야 한다(2026-09-09).
    """
    est = s.startswith('[추정] ')
    if est:
        s = s[len('[추정] '):]
    s = _CITE.sub('', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return (EST if est else '') + s.strip()


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
    'WACC': '「13.3%로 계산」은 표에 찍힌 값을 그대로 넣었을 때이고, 「역산 WACC」는 '
            '발표된 월 자본비에서 거꾸로 푼 값입니다. 여섯이 0.004%포인트 안에 모입니다.',
    'VERDICT': '손익분기 임대료는 원문이 글로 밝힌 값(L298·L302·L306)이고, 실측 처리량은 '
               '그것을 H200 시세 2.5달러로 나눈 비율입니다. 문턱과 결론은 원문에 없습니다.',
    'RAW': '값을 그림에서 코드로 바로 넣지 않고 이 파일을 거칩니다. 못 읽은 것도 「없음」이 '
           '아니라 「못 읽음」으로 남깁니다 — 나중에 그 값을 말한 자료가 나오면 거기에 채워 '
           '넣으면 모델과 표와 도해가 함께 따라옵니다.',
    'EXT': '뉴스레터 밖에서 가져올 수 있는 자료입니다. 「후보」는 아직 안 가져온 것이고, '
           '한 줄만 박히면 가려진 칸의 나머지가 다 풀립니다 — 차이는 이미 고정돼 있기 '
           '때문입니다.',
    'GAP': '「MI300X 대비 차이」만 원문 값에서 바로 나옵니다. 기타 서버 비용이 SKU 마다 '
           '같다고 보면 그 차이가 곧 GPU 원가의 차이입니다. 오른쪽 세 열의 기타 값은 '
           '우리가 고른 가정이고 원문에 없습니다 — 절대값이 아니라 폭을 보는 자리입니다.',
    'CAPEX': 'WACC 는 표에 찍힌 13.3%가 아니라 역산한 13.25%입니다(7절). B200 의 '
             '서버당 선불이 발표치보다 1달러 큰 것은 발표 표의 항목별 반올림 때문입니다.',
    'OPEX': '전기는 정격이 아니라 가동률과 PUE 를 거친 값입니다. 여섯 SKU 가 같은 '
            '단가를 쓰므로 차이는 서버 전력에서만 납니다.',
    'TOTAL': '맨 아래 줄은 원문에 없습니다. H200 을 1 로 놓고 각 SKU 가 사서 쓸 때 '
             '넘어야 할 처리량 비율을 우리가 계산한 것입니다.',
}


_ONE = re.compile(r'^[$+-]?[\d,.]+(%p|%|배|회)?$')


def _is_num(txt):
    """값 칸인가. 「0.84~0.96」이나 「$2.10~$2.40」 같은 구간도 값이다.

    물결을 지우고 한 덩어리로 재면 「$2.10$2.40」이 되어 달러 표가 안 걸린다 —
    그 열이 통째로 글자 열로 잡혀 왼쪽에 붙고 흐려졌다(2026-09-09).
    """
    parts = [t.strip() for t in txt.split('~')]
    return bool(parts) and all(_ONE.match(t) for t in parts if t)
# 합계·마지막 줄로 보는 이름. 원문 표에서 굵게 찍힌 줄과 같은 자리다
_SUM = ('합계', 'Gold 대비', '문턱')


def _numeric_cols(head, body):
    """열마다 숫자 열인지 정한다. 칸 하나씩 보면 같은 열에서 정렬이 갈린다 —
    「차이」 열의 「일치」가 왼쪽에 붙고 「+27.30%p」가 오른쪽에 붙었다(2026-09-09)."""
    out = []
    for i in range(len(head)):
        vals = [r[i] for r in body if i < len(r) and r[i]]  # None 은 빠진다
        hit = sum(1 for v in vals if _is_num(v))
        # 숫자가 하나라도 있고 나머지가 「일치」 같은 짧은 말뿐이면 숫자 열이다.
        # 과반으로 정하면 일곱 줄 중 넷이 「일치」인 「차이」 열이 글자 열이 되어
        # 그 열의 숫자만 왼쪽에 붙는다(2026-09-09)
        rest_ok = all(len(v) <= 3 for v in vals if not _is_num(v))
        # 첫 열만 이름 열로 못 박는다. 둘째 열을 함께 뺐더니 SKU 표의 첫 값 열이
        # 글자 열로 잡혀 왼쪽에 붙고 흐리게 나왔다(2026-09-09)
        out.append(bool(i >= 1 and vals and hit and rest_ok))
    return out


def _cell(txt, num):
    """숫자 칸은 오른쪽으로 맞춘다. 자릿수가 세로로 서야 크기가 눈에 들어온다.

    None 은 원문이 가린 값이라 어두운 칸으로 칠한다 — 빈칸으로 두면 0 으로 읽힌다.
    0 은 「—」로 낸다. 원문 표가 그 자리에 included 라고 적었고, $0.00 을 스무 칸
    깔면 값이 있는 칸이 안 보인다."""
    if txt is None:
        return '<td class="red" title="원문이 가린 값"></td>' 
    if num and txt in ('$0.00', '$0', '0.00%'):
        txt = '—'
    return '<td%s>%s</td>' % (' class="num"' if num else '', txt)


def table_html(key):
    """원문 계산기의 칸을 그대로 세운다. 값은 _model_tbl 의 모델이 낸 것이다."""
    title, fn = mt.TABLES[key]
    head, body = fn()
    nums = _numeric_cols(head, body)
    h = ['<div class="xls"><div class="xlt">%s%s</div><div class="xlw">'
         % (EST if key in TBL_EST else '', title),
         '<table class="xl"><thead><tr>']
    h += ['<th%s>%s</th>' % (' class="num"' if nums[i] else '', c)
          for i, c in enumerate(head)]
    h.append('</tr></thead><tbody>')
    for r in body:
        # 「차이」 칸이 「일치」가 아니면 어긋난 줄이다 — 왼쪽에 굵은 선을 세운다
        off = any(c and c.endswith('%p') for c in r)
        klass = ' class="sum"' if any(k in (r[0] or '') for k in _SUM) else (
            ' class="off"' if off else '')
        h.append('<tr%s>' % klass
                 + ''.join(_cell(c, nums[i]) for i, c in enumerate(r)) + '</tr>')
    h.append('</tbody></table></div></div>')
    h.append('<p class="xl-memo">%s</p>' % TBL_NOTE[key])
    if key == 'EXT':
        h.append('<p class="xl-memo"><b>어떻게 쓰나</b><br>'
                 + '<br>'.join(mt.ext_lines()) + '</p>')
    if key == 'RAW':
        # 출처는 표 아래에 한 줄씩. 표 안에 넣으면 열이 하나 더 늘어 가로로 넘친다
        h.append('<p class="xl-memo"><b>출처</b><br>'
                 + '<br>'.join(mt.source_lines()) + '</p>')
    return ''.join(h)


def load(src):
    txt = io.open(src, encoding='utf-8').read()
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
        elif s.startswith('[[eq:'):
            flush()
            out.append(('eq', s[5:].rstrip(']').strip()))
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


def toc_html(anchor, lead, groups, titles):
    """규약과 코드는 _rep_toc 하나뿐이다 — 층마다 복사하면 갈린다(2026-09-05)."""
    return rt.toc_html(anchor, lead, groups, titles)


def _report(src, anchor, lead, groups, sec, p, fig):
    items = load(src)
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == groups[-1][2], (len(titles), groups)
    toc_done = False
    for k, v in items:
        if k in ('sec', 'fig', 'tbl', 'eq') and not toc_done:
            p(toc_html(anchor, lead, groups, titles))
            toc_done = True
        if k == 'sec':
            sec(rt.sec_title(titles.index(v) + 1, v))
        elif k == 'p':
            p(_strip(v))
        elif k == 'fig':
            fig(CAPTION[v])
        elif k == 'tbl':
            p(table_html(v))
        elif k == 'eq':
            p(me.eq_html(v))
        elif k == 'table':
            p(_table(v))
    return titles


def report_cluster(sec, p, fig):
    return _report(SRC_C, 'model-cluster', LEAD_CLUSTER, GROUPS_CLUSTER, sec, p, fig)


def report_infer(sec, p, fig):
    return _report(SRC_I, 'model-infer', LEAD_INFER, GROUPS_INFER, sec, p, fig)
