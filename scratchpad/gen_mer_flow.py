# -*- coding: utf-8 -*-
"""메르 흐름 — 메르 627편을 줄기 하나로 꿴 장.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_mer_flow.py

왜 사슬(insights/flows/mer)과 따로 두나: 사슬은 연재 주제 하나에 마디와 화살표를 세우는
꼴이라 단발 글이 갈 데가 없다. 미수록이 286편까지 쌓인 것이 그 때문이다(2026-09-06).
흐름은 줄기가 단위라서 단발도 그 줄기 위의 조각으로 들어간다.

본문은 insights/mer_flows/ 의 마크다운 원본에 있고 여기서 HTML 로 바꾼다. 차례와 절
번호는 _rep_toc 가 붙인다 — 층마다 복사하면 갈린다.

인용은 화면에서 걷고 작은 날짜만 남겨 원문 글로 건다. 날짜는 클리핑에서 읽어 온다 —
본문에 적으면 두 곳이 갈린다.
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _mer_fig as mf  # noqa: E402
import _rep_toc as rt  # noqa: E402
import dash_common as dc  # noqa: E402
from card_lib import fig_html  # noqa: E402

SRC = os.path.join(dc.ROOT, 'insights', 'mer_flows', '2026-09-07-한도가-값을-따라간다.md')
OUT = os.path.join(dc.ROOT, '대시보드', '메르 흐름.html')
CLIP = os.path.join(dc.ROOT, 'input', 'clippings', 'mer', '*.json')
STAMP = '2026-09-07'

GROUPS = [('안에서 옮긴 선', 1, 4),
          ('부딪히거나 밖에서 그어진 선', 5, 6),
          ('남은 것', 7, 7)]

LEAD = ('이 글은 물음 하나를 세 묶음으로 따라갑니다 — 안에서 옮긴 선, 부딪히거나 밖에서 '
        '그어진 선, 그리고 남은 것.')

CAPTION = {
    'CAP': ('허용 상한이 실제 보유를 못 따라가자 상한을 옮겼다', mf.FIG_CAP,
            '막대 길이는 국민연금의 국내 주식 보유 비중에 비례합니다. 두 줄의 막대는 같은 값이고 '
            '옮긴 것은 한도선뿐입니다. 위는 2026년 5월로 허용 상한이 19.9%인데 실제가 29.7%였고, '
            '아래는 목표를 20.8%로 올리고 전략적 자산배분 허용폭을 6%포인트로 넓힌 뒤라 상한이 '
            '28.8%가 됩니다. 네 값은 모두 원문에 적힌 것이고, 두 줄로 나란히 세운 것은 이 글입니다.'),
    'FUEL': ('유류세 깎아 주던 폭이 여섯 번에 걸쳐 0이 됐다', mf.FIG_FUEL,
             '막대 높이는 인하율에 비례합니다. 맨 왼쪽 37%는 줄이기 전이라 날짜를 안 붙였고, '
             '오른쪽으로 가며 여섯 번 줄어 마지막에 인하가 끝납니다. 칸이 일곱인 것은 원문이 '
             '센 여섯 번의 변경에 처음 값을 더한 수입니다. 마지막 칸은 값이 0이라 막대 대신 '
             '점선으로 두었습니다.'),
    'REDEEM': ('계약은 5%인데 요청이 그 선을 넘었다', mf.FIG_REDEEM,
               '2026년 3월 사모대출 펀드에 들어온 환매 요청입니다. 막대 높이는 자산 대비 요청 '
               '비율이고, 점선이 분기당 5%라는 계약 한도입니다. 세 건은 원문이 든 펀드 수이고 '
               '더 있는지는 원문이 말하지 않습니다. 클리프워터는 7%만 돌려줬고, 블랙스톤은 한도를 '
               '7%로 늘린 뒤 모자란 0.9%를 회사 자본금과 임원 출자로 채웠습니다.'),
}

_CITE = re.compile(r'\s*\(메르-(\d+)\s+(T\d+(?:[-,]\s*T?\d+)*)\)')


def _dates():
    """글번호 -> 발행일. 본문에 날짜를 적지 않고 여기서 읽는다."""
    out = {}
    for p in glob.glob(CLIP):
        d = json.load(io.open(p, encoding='utf-8'))
        out[str(d['no'])] = d.get('date', '')
    return out


DATE = _dates()


def _strip(s):
    """인용은 화면에서 걷고 작은 날짜만 남겨 원문 글로 건다."""
    def one(m):
        no, refs = m.group(1), m.group(2)
        d = DATE.get(no, '')
        lab = d[5:] if len(d) >= 10 else no[-4:]
        return ('<a class="mer-src" target="_blank" rel="noopener" '
                'href="https://blog.naver.com/ranto28/%s" title="메르-%s %s">%s</a>'
                % (no, no, refs, lab))
    s = _CITE.sub(one, s)
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


def body_html():
    items = load()
    titles = [t for k, t in items if k == 'sec']
    assert len(titles) == GROUPS[-1][2], (len(titles), GROUPS)
    h, n, toc_done = [HEAD], [0], [False]
    for k, v in items:
        if k in ('sec', 'fig') and not toc_done[0]:
            h.append(rt.toc_html('mer', LEAD, GROUPS, titles))
            toc_done[0] = True
        if k == 'sec':
            n[0] += 1
            h.append('<h3 id="mer-%d">%s</h3>' % (n[0], rt.sec_title(n[0], v)))
        elif k == 'p':
            h.append('<p class="ins-lede">%s</p>' % _strip(v))
        elif k == 'fig':
            h.append(fig_html(CAPTION[v]))
    return ''.join(h)


HEAD = (
    '<div class="rep-head"><span class="rn">메르</span>'
    '<h2 id="mer-flow">한도가 값을 따라간다 — 메르 627편, 2025년 10월부터 2026년 9월까지</h2>'
    '<p class="rm">바탕 <b>메르 627편</b> · 원문 기간 <b>2025-10-04 ~ 2026-09-05</b> · '
    '사실 <b>1,808줄</b><br>'
    '재료가 한 사람의 블로그입니다. 다른 매체나 1차 문서로 교차 확인하지 않았으므로 이 장의 값은 '
    '「원문에 그렇게 적혀 있다」까지만 보증합니다. 문장 끝의 작은 날짜가 그 문장이 나온 글이고, '
    '눌러서 원문으로 갑니다.</p></div>')

MER_CSS = """
  .mer-src{font-size:10.5px;color:var(--ink-3);white-space:nowrap;
           font-variant-numeric:tabular-nums;margin-left:3px;text-decoration:none}
  .mer-src::before{content:"("}
  .mer-src::after{content:")"}
  .mer-src:hover{color:var(--ink)}
"""

HEADER = '''  <header>
    <p class="eyebrow">열두 달치 글을 줄기 하나로</p>
    <h1>메르 흐름</h1>
  </header>'''

LEDE = ('<p class="lede">블로거 메르가 2025년 10월부터 2026년 9월까지 쓴 627편을 한자리에 모아 '
        '읽은 글입니다. 주장과 값을 1,808줄로 뽑아 날짜순으로 늘어놓고, 되풀이되는 장면 하나를 '
        '줄기로 세웠습니다. <b>주제별 목록이 아닙니다</b> — 주제로 자르면 열두 달이 네 토막으로 '
        '흩어지는데, 그 토막을 가로질러 같은 일이 벌어지는 것이 이 글이 다루는 것입니다. '
        '주제 단위로 엮은 사슬은 <a href="메르 대시보드.html">메르 대시보드</a>에 있습니다. '
        '본문은 <code>insights/mer_flows/</code> 의 원본에서 읽어 옵니다.</p>')

META_ROW = '''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>바탕 <b>메르 627편 · 사실 1,808줄</b></span>
      <span>인용 <b>글 40여 편</b></span>
    </div>''' % STAMP

FOOTER = (LEDE + META_ROW
          + '\n조각은 메르가 적은 것이고, 조각을 이어 줄기로 세운 것은 우리입니다. '
          '투자 추천이 아닙니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_mer_flow.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

FIGS = [(0, t, svg, '') for t, svg, _c in CAPTION.values()]


if __name__ == '__main__':
    dc.render([], '메르 흐름', HEADER, FOOTER, OUT,
              page_slug='mer-flow',
              top=body_html(), top_id='sec-mer-flow',
              top_title='한도가 값을 따라간다',
              top_n=1,
              top_sub='메르 627편 — 값이 선을 넘으면 선이 옮겨진다. 국민연금은 상한 19.9%를 '
                      '넘긴 뒤 상한을 28.8%로 넓혔다',
              extra_css=MER_CSS)

    html = io.open(OUT, encoding='utf-8').read()
    bad = rt.check_toc(html)
    if bad:
        raise SystemExit('차례 규약 위반\n  ' + '\n  '.join(bad))
    print('  차례 규약 OK')
