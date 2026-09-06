# -*- coding: utf-8 -*-
"""링크드인 흐름 — SemiAnalysis 링크드인 537건을 줄기 하나로 꿴 장.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_li_flow.py

왜 카드로 안 쪼개나: 섹션마다 업데이트하는 꼴로는 큰 흐름이 안 보였고, 주제를 열둘로
나눠도 목록 열둘이라 같았다(2026-09-06). 그래서 줄기를 하나 세우고 주제를 그 아래
가지로 넣었다. 본문은 insights/li_flows/ 의 마크다운 원본에 있고 여기서 HTML 로 바꾼다.

**건수 그래프는 없다.** 요지 평균 자수가 4월 42자에서 8월 304자로 일곱 배가 되어
월별 언급 건수가 주제 이동이 아니라 요약 길이를 그린다. 자세한 것은 마지막 절.

차례와 절 번호는 _rep_toc 가 붙인다 — 층마다 복사하면 갈린다.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _li_fig as lf  # noqa: E402
import _rep_toc as rt  # noqa: E402
import dash_common as dc  # noqa: E402
from card_lib import fig_html  # noqa: E402

SRC = os.path.join(dc.ROOT, 'insights', 'li_flows', '2026-09-06-판이-어디로-갔나.md')
OUT = os.path.join(dc.ROOT, '대시보드', '링크드인 흐름.html')
STAMP = '2026-09-06'

GROUPS = [('값이 어디서 오르나', 1, 2),
          ('무엇이 진짜 막혔나', 3, 5),
          ('누가 그 사이로 들어왔나', 6, 7)]

LEAD = ('이 글은 물음 하나를 세 묶음으로 따라갑니다 — 값이 어디서 오르나, '
        '무엇이 진짜 막혔나, 누가 그 사이로 들어왔나.')

CAPTION = {
    'SHIFT': ('값이 오른 자리 — 소재에서 완제품까지', lf.FIG_SHIFT,
              '상자 여섯이 전부 같은 크기입니다. 다른 것은 아래 붙인 날과 값뿐입니다. '
              '왼쪽에서 오른쪽이 공급망 순서인데 날짜는 그 순서를 안 따릅니다 — 메모리가 '
              '3월, 파운드리와 완제품이 8월입니다. 값이 한 자리에서 옮겨간 것이 아니라 '
              '여러 자리에서 따로 오르면서 아래쪽으로 번진 모양입니다. 판에 들어갈 자리가 '
              '좁아 값을 줄여 적었습니다 — 텅스텐은 중국 수출이 전년 대비 50% 줄어든 것, '
              '캐펙스는 TSMC 설비투자 가이던스 15% 인상과 그 원인으로 지목된 장비 '
              '인플레이션, 파운드리는 매출이 545억 달러로 사상 최대인데 물량은 6%만 늘어난 '
              '것, 기판은 2026년 물량이 전부 예약돼 리드타임이 12~14개월로 늘어난 것, '
              '완제품은 중국 스마트폰 평균판매단가가 전년 대비 27% 오르면서 물량은 줄어든 '
              '것입니다. 값은 모두 각 게시물에 적힌 것이고, 이 여섯을 한 줄에 세운 것은 '
              '이 글입니다.'),
    'POWER': ('전력 — 값 신호가 나온 뒤 계통이 문을 닫기까지', lf.FIG_POWER,
              '한 달에 하나씩 여섯 달을 이었습니다. 위에서 아래로 내려갈수록 막히는 자리가 '
              '값에서 사람으로, 사람에서 허가로, 허가에서 계통 자체로 옮겨갑니다. 8월 칸만 '
              '테두리가 짙은 것은 그 달에 신규 접속 승인이 실제로 멈췄기 때문입니다. '
              '이 순서를 그들이 한 편에 모아 적은 자리는 없습니다.'),
    'CLOCK': ('물리적인 것을 늘리는 데 걸리는 시간과 소프트웨어가 걸린 시간', lf.FIG_CLOCK,
              '높이는 개월 수에 비례합니다. △ 가 붙은 것은 범위의 위 끝입니다 — 인듐인은 '
              '2~3년, 기판 리드타임은 12~14개월이라 각각 36개월과 14개월로 그렸습니다. '
              '오른쪽 두 막대가 거의 안 보이는 것이 이 그림이 말하려는 것입니다. 왼쪽 셋은 '
              '채워 두고 오른쪽 둘은 비워 두었습니다. 다섯 값은 서로 다른 게시물에서 왔고 '
              '나란히 놓은 것은 이 글입니다.'),
}

_CITE = re.compile(r'\s*\((L-\d{8}-\d+(?:\s*·\s*L-\d{8}-\d+)*)\)')


def _strip(s):
    """게시물 식별자는 화면에서 걷는다 — 원본 파일에만 남는다(확정 규칙 S1 「줄 번호」와 같다).

    걷은 자리에 아무것도 안 남기면 어느 문장이 어느 게시물에서 왔는지 화면에서 사라진다.
    그래서 작은 첨자로 날짜만 남기고 링크드인 원글로 건다."""
    def one(m):
        ids = re.findall(r'L-(\d{4})(\d{2})(\d{2})-\d+', m.group(1))
        days = ' · '.join('%s-%s' % (mo, d) for _y, mo, d in ids)
        return '<span class="li-src" title="%s">%s</span>' % (m.group(1), days)
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
            h.append(rt.toc_html('li', LEAD, GROUPS, titles))
            toc_done[0] = True
        if k == 'sec':
            n[0] += 1
            h.append('<h3 id="li-%d">%s</h3>' % (n[0], rt.sec_title(n[0], v)))
        elif k == 'p':
            h.append('<p class="ins-lede">%s</p>' % _strip(v))
        elif k == 'fig':
            h.append(fig_html(CAPTION[v]))
    return ''.join(h)


HEAD = (
    '<div class="rep-head"><span class="rn">링크드인</span>'
    # ②절 제목이 「값이 오르는 자리가 칩 바깥으로 밀려났다」라 머리에 같은 말을 쓰면
    # 타일·머리·절 셋이 겹쳐 읽힌다(확정 규칙 「중복 없음」). 머리는 기간으로 가른다
    '<h2 id="li-flow">판이 어디로 갔나 — 링크드인 537건, 2026년 2월부터 9월까지</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 링크드인 537건</b>(자체 발화 274건) · '
    '원문 기간 <b>2026-02-25 ~ 2026-09-04</b><br>'
    '게시일순 목록은 <a href="소셜 신호 히스토리.html">소셜 신호 히스토리</a>에 있습니다. '
    '이 장은 그 537건에서 주장과 값을 546줄로 뽑아 날짜순으로 읽고 줄기 하나로 꿴 글입니다. '
    '문장 끝의 작은 날짜가 그 문장이 나온 게시물입니다.</p></div>')

LI_CSS = """
  .li-src{font-size:10.5px;color:var(--ink-3);white-space:nowrap;
          font-variant-numeric:tabular-nums;margin-left:3px}
  .li-src::before{content:"("}
  .li-src::after{content:")"}
"""

HEADER = '''  <header>
    <p class="eyebrow">여섯 달치 게시물을 줄기 하나로</p>
    <h1>링크드인 흐름</h1>
  </header>'''

LEDE = ('<p class="lede">SemiAnalysis 링크드인 계정에 2026년 2월 말부터 9월 초까지 올라온 '
        '537건을 한자리에 모아 읽은 글입니다. 밈·채용·행사를 걷어 낸 자체 발화 274건에서 '
        '주장과 값을 546줄로 뽑아 날짜순으로 늘어놓았습니다. <b>건수 그래프는 싣지 '
        '않았습니다</b> — 요지의 평균 길이가 4월 42자에서 8월 304자로 일곱 배가 되어, '
        '월별 언급 건수가 주제 이동이 아니라 요약 길이를 그리기 때문입니다. 본문은 '
        '<code>insights/li_flows/</code> 의 원본에서 읽어 옵니다.</p>')

META_ROW = '''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>바탕 <b>링크드인 537건 · 자체 발화 274건 · 사실 546줄</b></span>
      <span>인용 <b>게시물 41건</b></span>
    </div>''' % STAMP

FOOTER = (LEDE + META_ROW
          + '\n조각은 SemiAnalysis 가 말한 것이고, 조각을 꿰어 줄기로 세운 것은 우리입니다. '
          '투자 추천이 아닙니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_li_flow.py</code>'
          '(공용 부품 <code>dash_common.py</code>).')

FIGS = [(0, t, svg, '') for t, svg, _c in CAPTION.values()]


if __name__ == '__main__':
    dc.render([], '링크드인 흐름', HEADER, FOOTER, OUT,
              page_slug='li-flow',
              top=body_html(), top_id='sec-li-flow',
              top_title='판이 어디로 갔나',
              top_n=1,
              top_sub='링크드인 537건 — 늘어난 것은 물량이 아니라 값이고, 값이 오르는 자리가 '
                      '칩 바깥으로 밀려났다',
              extra_css=LI_CSS)

    html = io.open(OUT, encoding='utf-8').read()
    bad = rt.check_toc(html)
    if bad:
        raise SystemExit('차례 규약 위반\n  ' + '\n  '.join(bad))
    print('  차례 규약 OK')
