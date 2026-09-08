# -*- coding: utf-8 -*-
"""링크드인 흐름 — SemiAnalysis 링크드인 537건을 줄기 하나로 꿴 층.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_li_flow.py

이 파일은 홀로 서는 장을 쓰지 않는다. SemiAnalysis 대시보드의 첫 절(①)로 끼워 넣는다
(2026-09-08). 같은 링크드인 537건이 두 주소에 서 있으면 읽는 사람이 어느 쪽이 최신인지
못 고른다 — 그 장의 ② 소셜·영상 신호가 「무엇이 새로 왔나」를 답하고 이 절이 「그래서
무엇이 막혔나」를 답한다.

끼워 넣는 자리는 주석 표시 둘 사이다(`li-flow:start` ~ `li-flow:end`). 손으로 쓴 장이라
표시가 없으면 처음 한 번 만들어 넣는다.

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
from card_lib import FIG_CSS, fig_html  # noqa: E402

SRC = os.path.join(dc.ROOT, 'insights', 'li_flows', '2026-09-06-판이-어디로-갔나.md')
DASH = os.path.join(dc.ROOT, '대시보드', 'SemiAnalysis 대시보드.html')
STAMP = '2026-09-06'

GROUPS = [('무엇이 막혔나', 1, 3),
          ('그 막힘이 어디에 드러났나', 4, 5),
          ('누가 그 사이로 들어왔나', 6, 7)]

LEAD = ('결론을 맨 앞에 놓고 병목 셋을 먼저 세운 다음, 값과 소프트웨어가 그 병목의 '
        '어느 쪽에 있는지를 봅니다.')

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
    # 1절 제목이 「병목은 칩이 아니라 그 바깥이었다」라 머리에 같은 말을 길게 쓰면
    # 타일·머리·절 셋이 겹쳐 읽힌다(확정 규칙 「중복 없음」). 머리는 기간으로 가른다
    '<h2 id="li-flow">병목은 칩이 아니었다 — 여섯 달, 2026년 2월부터 9월까지</h2>'
    '<p class="rm">바탕 <b>SemiAnalysis 링크드인 537건</b>(자체 발화 274건) · '
    '<b>뉴스레터 변환본 53편</b> · 원문 기간 <b>2026-02-06 ~ 2026-09-07</b><br>'
    '게시일순 목록은 <a href="소셜 신호 히스토리.html">소셜 신호 히스토리</a>에 있습니다. '
    '이 장은 링크드인 537건에서 뽑은 546줄과 같은 기간 뉴스레터 변환본을 함께 읽고 줄기 '
    '하나로 꿴 글입니다. 문장 끝의 작은 표시가 그 문장이 나온 원문입니다.</p></div>')

LI_CSS = """
  .li-src{font-size:10.5px;color:var(--ink-3);white-space:nowrap;
          font-variant-numeric:tabular-nums;margin-left:3px}
  .li-src::before{content:"("}
  .li-src::after{content:")"}
"""

# 손으로 쓴 장에는 dash_common 의 잉크 변수가 없다. 그 장의 변수로 다리를 놓는다.
# 그 장에 이미 사는 `.tl`(관전 목록의 윗줄)과 이름이 겹쳐 차례 머리글에 줄이 그어졌다 —
# 겹치는 자리만 되돌린다.
BRIDGE_CSS = """
  /* li-flow:vars */
  #li-flow-sec{--ink-2:var(--ink);--ink-3:var(--sub);--accent-ink:var(--accent)}
  #li-flow-sec .rep-toc .tl{border-top:none;padding-top:0;margin-top:0}
  #li-flow-sec .ins-lede{margin:0 0 12px;font-size:.92rem;line-height:1.9;color:var(--ink)}
  #li-flow-sec h3{margin:26px 0 10px;font-size:1.02rem}
"""

# 이 절이 끝나는 자리. 홀로 서던 때는 장 바닥글이 하던 말인데, 절로 들어오면서 절 안에
# 남긴다 — 건수 그래프를 왜 안 싣는지는 이 절에서만 하는 이야기라 바닥글로 보내면 사라진다
TAIL = ('<p class="rep-note"><b>정리일 %s</b> · 바탕 <b>링크드인 537건 · 자체 발화 274건 · '
        '사실 546줄</b> · 인용 <b>게시물 28건 · 뉴스레터 11편</b><br>'
        '<b>건수 그래프는 싣지 않았습니다</b> — 요지의 평균 길이가 4월 42자에서 8월 304자로 '
        '일곱 배가 되어, 월별 언급 건수가 주제 이동이 아니라 요약 길이를 그리기 때문입니다.<br>'
        '조각은 SemiAnalysis 가 말한 것이고, 조각을 꿰어 줄기로 세운 것은 우리입니다. '
        '투자 추천이 아닙니다. 본문은 <code>insights/li_flows/</code> 의 원본에서 읽어 오고 '
        '<code>scratchpad/gen_li_flow.py</code> 가 이 절을 끼워 넣습니다.</p>') % STAMP

FIGS = [(0, t, svg, '') for t, svg, _c in CAPTION.values()]


# 이 절은 접힌 채로 선다 — 5,600자짜리 글이 펴진 채로 맨 위에 서면 그 아래 「무엇이 새로
# 왔나」가 화면 밖으로 밀린다. 제목만 보이고 눌러야 펴진다(2026-09-08).
SEC_HEAD = ('  <section id="li-flow-sec" data-c="all compute memory power model robot">\n'
            '    <details class="liflow"><summary>'
            '<span class="lfh"><h2>① 여섯 달을 줄기 하나로 — 링크드인 537건</h2>'
            '<span class="lfs">병목은 칩이 아니었다 — 절 일곱 · 도해 셋 · 5,600자</span>'
            '</span></summary>\n')

SEC_FOOT = '    </details>\n  </section>\n\n'

# 앵커로 들어오면 펴 준다. ② 절 안내문이 이 절을 가리키는데, 접힌 채로 데려다 놓으면
# 누른 사람은 제목 한 줄만 보고 아무 일도 안 일어난 줄 안다
OPEN_JS = """  <script>
  (function(){
    var d = document.querySelector('#li-flow-sec details.liflow');
    if(!d) return;
    var open = function(){
      var h = location.hash;
      if(h === '#li-flow-sec' || (h.length > 1 && d.querySelector(h))) {
        d.open = true;
        var t = document.querySelector(h);
        if(t) t.scrollIntoView();
      }
    };
    window.addEventListener('hashchange', open);
    open();
  })();
  </script>
"""

FOLD_CSS = """
  /* 접힌 절 — 제목만 서고 눌러야 펴진다 */
  #li-flow-sec details.liflow > summary{list-style:none; cursor:pointer;
    display:flex; align-items:baseline; gap:10px; padding:4px 0;}
  #li-flow-sec details.liflow > summary::-webkit-details-marker{display:none}
  #li-flow-sec details.liflow > summary::before{content:"▸"; flex:none; color:var(--sub);
    font-size:.8rem; line-height:1.6;}
  #li-flow-sec details.liflow[open] > summary::before{content:"▾"}
  #li-flow-sec details.liflow > summary:hover h2{color:var(--accent)}
  #li-flow-sec .lfh{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;}
  #li-flow-sec .lfh h2{margin:0}
  #li-flow-sec .lfs{color:var(--sub); font-size:.78rem; font-weight:400;}
  #li-flow-sec details.liflow[open] > summary{border-bottom:1px solid var(--line);
    padding-bottom:10px; margin-bottom:14px;}
"""

S0, S1 = '  <!-- li-flow:start -->\n', '  <!-- li-flow:end -->\n'
C0, C1 = '  /* li-flow:start */\n', '  /* li-flow:end */\n'


def _splice(txt, a, b, new, where):
    """표시 둘 사이를 갈아 끼운다. 표시가 없으면 where 앞에 처음으로 만들어 넣는다."""
    i = txt.find(a)
    if i == -1:
        j = txt.index(where)
        return txt[:j] + a + new + b + txt[j:]
    k = txt.index(b, i) + len(b)
    return txt[:i] + a + new + b + txt[k:]


if __name__ == '__main__':
    body = SEC_HEAD + body_html() + TAIL + '\n' + SEC_FOOT + OPEN_JS
    css = rt.CSS + FIG_CSS + LI_CSS + BRIDGE_CSS + FOLD_CSS

    ds = io.open(DASH, encoding='utf-8').read()
    ds = _splice(ds, C0, C1, css, '</style>\n<main>')
    ds = _splice(ds, S0, S1, body, '  <section id="social-section"')
    io.open(DASH, 'w', encoding='utf-8').write(ds)

    bad = rt.check_toc(ds)
    if bad:
        raise SystemExit('차례 규약 위반\n  ' + '\n  '.join(bad))
    print('  차례 규약 OK')
    print('  절 %d · 도해 %d -> %s'
          % (body.count('<h3 id="li-'), body.count('<figure'), DASH))
