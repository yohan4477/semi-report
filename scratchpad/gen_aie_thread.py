# -*- coding: utf-8 -*-
"""AI Engineer 주장 흐름 — 물음 열여섯으로 세운 한 장.

처음에는 126줄을 날짜순으로만 깔았다. 「이걸로 뭘 얘기하고 싶은지가 전혀 안 보인다」는
지적을 받았다(2026-09-09). 원인은 여는 말 셋이 전부 방법 이야기(몇 줄을 어떻게 셌나,
어느 것이 옅은가)였고 판단은 둘째 문단에 한 번 나온 뒤 평평한 목록에 묻혔기 때문이다.

그래서 걸림으로 이어진 덩어리를 물음 하나로 본다. 줄 A 가 B 에 걸리고 B 가 C 에 걸리면
셋은 같은 물음을 놓고 말한 것이다 — 덩어리를 사람이 고르지 않고 lib.components() 가
자료에서 뽑고, 그 덩어리에 이름과 판단 한 줄을 붙이는 것만 사람이 한다(SECTIONS).
자료가 바뀌어 덩어리가 갈라지거나 붙으면 앵커가 안 맞아 생성이 멈춘다 — 표를 고치기
전에는 화면이 안 나온다.

아카이브 부품(dash_common)을 안 쓴다. 저기는 카드가 쌓이는 장이라 최신순 목록과
태그로 고르게 돼 있는데, 이 장은 위에서 아래로 한 줄기를 읽는 장이라 고를 것이
순서가 아니다. 규약은 아래 check_ui() 가 생성 때 검사한다 — 규약을 우회하려고 나온
장이 규약 없는 장이 되면 다음 사람이 같은 자리를 다시 판다.

산출은 대시보드/ 바로 아래다. 대시보드/ai-engineer/ 안에 두면
dash_common._write_card_pages 가 카드 슬러그가 아닌 html 을 매 생성 때 지운다.

색으로 입장을 가르지 않는다. 어느 주장이 어느 편인지는 우리가 매긴 값이고, 이 장이
내놓는 근거는 나란히 놓인 두 인용뿐이다. 관계는 기호(● ↑ ✕)와 선꼴(실선·점선)로만
가른다.

옅게 내는 자리가 둘이라 클래스를 나눈다. faint 는 아무 데도 안 걸린 주장이고 이것은
생성 때 박혀 거르개를 눌러도 안 바뀐다. off 는 조직 거르개가 지금 안 고른 줄이라 누를
때마다 붙었다 떨어진다. 한 클래스로 겸하면 조직을 한 번 누르는 순간 고립 표시가
통째로 지워진다.
"""
import io
import os
import sys
from urllib.parse import quote
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import aie_thread_lib as lib          # noqa: E402
import check_aie_thread as chk        # noqa: E402
import ui_bits                        # noqa: E402
from card_lib import slug             # noqa: E402
from gen_aie_dashboard import BOLD_RE, BOLD_TO   # noqa: E402

OUT = os.path.join(ROOT, '대시보드', 'AI Engineer 주장 흐름.html')

MARK = {'신규': '●', '동조': '↑', '엇갈림': '✕'}

CIRCLED = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮'

# 축 셋. 물음 열여섯을 어디에 세울지만 정한다 — 묶는 일을 독자에게 넘기지 않는다.
AXES = [
    ('어떻게를 누가 쥐나', '모델에 결정을 얼마나 맡길 것인가. 이 장에서 갈린 자리는 여기 하나뿐이다.'),
    ('모델에 무엇을 들려 보내나', '창·기억·도구·권한을 어떻게 마련해 주는가.'),
    ('무엇을 재나', '올려도 되는지, 나아졌는지를 무엇으로 아는가.'),
]

# (축 번호, 덩어리 앵커 id, 절 제목=물음, 판단 한 줄)
#
# 앵커는 그 덩어리에서 가장 이른 줄의 id 다. 제목과 판단은 그 덩어리의 줄을 다
# 읽고 사람이 붙인다 — 자료에 없는 말을 쓰지 않는다. 덩어리 하나가 절 하나이고,
# 표에 없는 덩어리가 생기면 build() 가 멈춘다.
SECTIONS = [
    (1, '2025-08-26-aws-판단은모델에', '어떻게까지 모델에 맡기나',
     '2025-08 AWS 가 「무엇을 할지에 집중하고 어떻게 할지는 일러 주지 않는다」고 한 자리에, '
     '1년 뒤 Microsoft 셋과 Neo4j·OpenAI 가 제어 흐름을 모델에서 빼내라고 답했다. '
     '이 장의 엇갈림 다섯은 전부 여기 붙어 있다.'),
    (1, '2025-08-26-microsoft-행동값재기', '사람은 어디에 남나',
     '권한을 올리는 자리, 머지하는 자리, 책임지는 자리는 사람 몫으로 남겨 둔다는 데는 여섯이 같은 말을 한다.'),
    (1, '2025-08-26-microsoft-거르개외부', '검사는 누가 하나',
     '거르개도 검증 에이전트도 만든 쪽 바깥에 둔다 — 자기 것을 자기가 채점하지 않게 한다.'),
    (1, '2025-08-26-cloudflare-승인대기', '오래 도는 일을 어떻게 되살리나',
     '승인을 기다리는 동안 멈춘 호출이 살아 있어야 하고, 돌아온 승인이 원래 그 에이전트를 찾아가야 한다.'),

    (2, '2025-08-26-aws-찾아오게', '창에 무엇을 넣나',
     '가장 큰 묶음이다. 목록을 밀어 넣지 말고 필요할 때 코드로 찾아오게 한다는 쪽으로 열넷이 모인다.'),
    (2, '2025-08-26-microsoft-지시문기록', '시킨 말을 어디에 남기나',
     '한 번 잘 시키려 애쓰는 대신 파일로 남긴다. 마크다운 문서가 곧 장치가 된다.'),
    (2, '2025-08-26-microsoft-구조기억', '기억을 어디에 두나',
     '파일에 던져 두는 것보다 나은 기억 장치가 필요하다는 쪽으로 셋이 이어진다.'),
    (2, '2025-08-26-braintrust-그대로안됨', '도구를 누구 눈높이로 쓰나',
     '사람이 쓰던 API 를 그대로 비추지 않고, 에이전트가 읽을 것을 전제로 다시 쓴다.'),
    (2, '2025-08-26-microsoft-읽기전용', '능력을 얼마나 주고 시작하나',
     '아무 능력도 없는 자리에서 시작해 필요한 것만 연다. 자격 증명은 모델 손에 안 쥐여 준다.'),
    (2, '2025-04-01-bloomberg-가드레일', '가드레일을 누가 만드나',
     '팀마다 따로 만들지 않고 판이 한 번 만들어 나눠 쓴다. 이 장에서 가장 오래된 줄이 여기 있다.'),
    (2, '2025-08-26-anthropic-쉬운길선택', '기본값을 누가 고르나',
     '옳은 일을 가장 쉬운 일로 만든다 — 정교한 선택지를 늘리는 일보다 기본값이 앞선다.'),
    (2, '2025-08-26-anthropic-하나로통일', '갈래를 몇 개로 두나',
     '무엇이든 하나로 정한다. 1년 뒤 GitHub 가 PR 을 하나로 못 박는 자리에서 같은 말이 나온다.'),

    (3, '2025-08-26-aws-관측필수', '재지 않고 올려도 되나',
     '관측 없이 파일럿도 하지 말라는 자리에서 시작해, 되짚어 좁힐 수 없으면 못 고친다는 데까지 간다.'),
    (3, '2026-05-26-braintrust-자취로채점', '평가를 어디서 시작하나',
     '망가지는 갈래를 먼저 찾고, 그 갈래는 내보낸 자취에서 나온다.'),
    (3, '2025-08-26-microsoft-무관한기준', '무엇에 견주나',
     '에이전트와 무관한 기준을 잡고, 켠 채로 한 번 끈 채로 한 번 돌려 견준다.'),
    (3, '2025-08-26-microsoft-평가는바퀴', '평가를 몇 번 하나',
     '한 번 하고 끝내지 않고 바퀴로 만든다 — 되돌아가는지 계속 잰다.'),
    (3, '2026-06-26-braintrust-재현으로봄', '무엇을 다시 돌리나',
     '같은 결과를 다시 만들려 하지 말고 그때 있었던 일을 되감는다.'),
]

CSS = '''<style>
  :root { --ink:#1a1a1a; --dim:#555; --pale:#999; --line:#ddd; --bg:#fbfbfa; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.7 -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
         word-break:keep-all; overflow-wrap:anywhere; }
  .wrap { max-width:860px; margin:0 auto; padding:28px 18px 80px; }
  h1 { font-size:24px; margin:0 0 6px; }
  .lede { color:var(--dim); margin:0 0 14px; }
  .lede b { color:var(--ink); font-weight:600; }
  .fig { margin:26px 0 6px; background:#fff; border:1px solid var(--line); padding:14px 12px 8px; }
  .fig svg { display:block; width:100%; height:auto; }
  .cap { color:var(--dim); font-size:13px; margin:8px 2px 26px; }
  .tw { overflow-x:auto; margin:0 0 26px; }
  table { border-collapse:collapse; font-size:14px; background:#fff; min-width:640px; }
  th, td { border:1px solid var(--line); padding:7px 9px; text-align:left; vertical-align:top; }
  td:first-child, td:last-child { white-space:nowrap; }
  th { color:var(--dim); font-weight:600; background:#f6f6f4; }
  .toc { background:#fff; border:1px solid var(--line); padding:14px 16px; margin:0 0 28px; }
  .toc .tl { display:block; color:var(--dim); font-size:13px; margin:0 0 8px; }
  .toc .tg { display:block; margin:8px 0 2px; padding-left:6px; font-weight:600; }
  .toc .tt { display:block; padding-left:16px; }
  .toc a { color:var(--ink); text-decoration:none; }
  .toc a:hover { text-decoration:underline; }
  h2 { font-size:19px; margin:34px 0 4px; scroll-margin-top:92px; }
  h3 { font-size:16px; margin:26px 0 2px; scroll-margin-top:92px; }
  .sub, .verdict { color:var(--dim); margin:0 0 10px; }
  .verdict { color:var(--ink); }
  .filters { position:sticky; top:0; background:var(--bg); padding:10px 0;
             border-bottom:1px solid var(--line); z-index:2; }
  .chip { display:inline-block; border:1px solid var(--line); background:#fff;
          border-radius:999px; padding:4px 12px; margin:0 6px 6px 0; cursor:pointer;
          font-size:13px; color:var(--dim); }
  .chip[aria-pressed="true"] { border-color:var(--ink); color:var(--ink); }
  .row { display:grid; grid-template-columns:24px minmax(0,1fr); gap:10px;
         padding:14px 0; border-bottom:1px solid var(--line);
         /* 거르개 줄이 sticky 라 앵커로 뛴 줄이 그 뒤에 숨는다. 그만큼 띄운다. */
         scroll-margin-top:92px; }
  .row[hidden] { display:none; }
  .sec[hidden] { display:none; }
  .mark { color:var(--dim); text-align:center; }
  .when { font-size:12px; color:var(--pale); }
  .who { font-size:13px; color:var(--dim); }
  .claim { margin:3px 0 0; }
  .row.faint .claim, .row.faint .who,
  .row.off .claim, .row.off .who { color:var(--pale); }
  .row.off .mark, .row.off .tie { opacity:.45; }
  .tie { margin:8px 0 0; padding:8px 12px; border-left:2px solid var(--line);
         background:#fff; font-size:14px; }
  .tie.cross { border-left-style:dashed; }
  .tie b { font-weight:600; }
  a.to { color:inherit; text-decoration:none; border-bottom:1px solid var(--line); }
  .q { display:block; color:var(--dim); margin:2px 0; }
  a.card { color:inherit; text-decoration:none; border-bottom:1px solid var(--line); }
  details.rest { margin:30px 0 0; }
  details.rest > summary { cursor:pointer; color:var(--dim); padding:10px 0;
                           border-top:1px solid var(--line); }
  .end { margin:34px 0 0; color:var(--dim); }
</style>'''


def check_ui(html, rows):
    """이 장의 규약. 어기면 생성이 멈춘다."""
    bad = []
    if '반박' in html:
        bad.append('관계 이름은 동조·엇갈림 둘뿐이다 — 「반박」이 화면에 났다')
    for hexcol in ('#c00', '#d00', '#b00', '#00c', 'red', 'blue', 'green'):
        if hexcol in html:
            bad.append('입장을 색으로 가르지 않는다 — %s' % hexcol)
    if html.count('class="claim"') != len(rows):
        bad.append('주장 줄 수가 재료와 다르다')
    # 거르개는 조직만 남긴다. 「신규만」은 고립 줄이 제 절로 빠지면서 볼 것이 없어졌고,
    # 「엇갈림만」은 갈린 물음이 첫 절로 올라와 거르개보다 차례가 빠르다.
    if 'data-org=' not in html:
        bad.append('조직 거르개가 없다')
    if 'ai-engineer/' not in html:
        bad.append('줄에서 카드로 가는 주소가 없다')
    if '**' in html:
        # 본문이 통째로 원문 인용이라 마크다운 표시가 그대로 새면 인용이 오염된다.
        # 처음 나갈 때 126줄 중 35줄에 별표 148개가 실렸는데 어느 검사기도 안 물었다.
        bad.append('원문의 굵게 표시(**)가 화면에 그대로 났다 — rich() 를 거르고 왔다')
    # 판단이 안 보인다는 지적이 나온 자리다. 절마다 판단 한 줄이 서 있는지,
    # 차례가 절 수와 맞는지를 기계가 센다 — 절을 더하고 차례를 잊으면 멈춘다.
    if html.count('class="verdict"') != len(SECTIONS):
        bad.append('절 판단 줄 수가 표와 다르다 — %d개여야 한다' % len(SECTIONS))
    if html.count('class="tt"') != len(SECTIONS):
        bad.append('차례 줄 수가 절 수와 다르다')
    for _, _, title, _ in SECTIONS:
        if 'id="sec-%s"' % slug(title) not in html:
            bad.append('절 앵커가 없다 — %s' % title)
    for name, _ in AXES:
        if esc(name) not in html:
            bad.append('축 이름이 화면에 없다 — %s' % name)
    # 본문이 통째로 인용이라 이 그물이 유일한 바닥이다. 검사기를 따로 돌리기 전에
    # 여기서 먼저 멈춘다 — 재료의 claim 이 원문 줄과 다르면 생성이 안 된다.
    bad += chk.cite_fails(rows)
    for r in rows:
        for rel in r.get('rel') or ():
            if 'id="%s"' % esc(rel.get('to') or '') not in html:
                bad.append('%s: 걸린 대상 줄로 갈 앵커가 없다 — %s' % (r.get('id'), rel.get('to')))
    return bad


def clash_fig(pairs):
    """갈린 물음 하나를 시간축에 그린다. 값은 날짜와 조직뿐 — 자료에 있는 것만 그린다.

    층을 셋으로 나눈다. 위는 걸린 자리 한 줄, 가운데가 축, 아래가 그 줄에 맞선 주장들이다.
    처음에는 앞선 주장 이름표를 축 바로 아래에 뒀다가 첫 주장 줄과 겹쳤다 — 글자 상자를
    셋 다 다른 띠에 두고 shot_thread.js 가 겹침 0 인지 잰다."""
    x0, x1 = 150, 790
    top, axis, first = 26, 62, 104
    step = 30
    left = pairs[0][1]
    outs = [p[0] for p in pairs]
    h = first + step * len(outs) + 16
    lines = ['<svg viewBox="0 0 820 %d" role="img" aria-label="갈린 물음 하나의 시간축">' % h]
    lines.append('<defs><style>'
                 '.t { font:13px -apple-system,"Malgun Gothic",sans-serif; fill:#1a1a1a; }'
                 '.d { font:12px -apple-system,"Malgun Gothic",sans-serif; fill:#777; }'
                 '.b { font:13px -apple-system,"Malgun Gothic",sans-serif; fill:#1a1a1a;'
                 ' font-weight:600; }'
                 '</style></defs>')
    lines.append('<text x="8" y="%d" class="d">%s</text>' % (top, left['date'][:7]))
    lines.append('<text x="72" y="%d" class="b">%s · 무엇만 시키고 어떻게는 맡겨라</text>'
                 % (top, esc(left['org'])))
    lines.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#bbb"/>' % (x0, axis, x1, axis))
    lines.append('<circle cx="%d" cy="%d" r="4" fill="#1a1a1a"/>' % (x0, axis))
    lines.append('<text x="%d" y="%d" class="d" text-anchor="end">%s</text>'
                 % (x0 - 10, axis + 4, left['date'][:7]))
    lines.append('<text x="%d" y="%d" class="d" text-anchor="end">%s</text>'
                 % (x1, axis - 10, outs[-1]['date'][:7]))
    lines.append('<path d="M%d %d L%d %d" stroke="#999" fill="none"/>'
                 % (x0, top + 8, x0, axis - 6))
    for i, r in enumerate(outs):
        y = first + step * i
        cx = _fig_x(r, outs, x0, x1, left['date'])
        lines.append('<circle cx="%d" cy="%d" r="3.5" fill="#777"/>' % (cx, axis))
        lines.append('<path d="M%d %d L%d %d" stroke="#999" stroke-dasharray="3 3" fill="none"/>'
                     % (cx, axis + 6, cx, y - 10))
        lines.append('<text x="8" y="%d" class="d">%s</text>' % (y, r['date'][:7]))
        lines.append('<text x="72" y="%d" class="t">✕ %s · %s</text>'
                     % (y, esc(r['org']), esc(_short(r['claim']))))
    return '\n'.join(lines) + '\n</svg>'


def _months(a, b):
    """두 날짜(YYYY-MM-DD) 사이 개월 수."""
    ya, ma = int(a[:4]), int(a[5:7])
    yb, mb = int(b[:4]), int(b[5:7])
    return (yb - ya) * 12 + (mb - ma)


def _fig_x(r, outs, x0, x1, base=None):
    """시간축 위 자리. 실제 달 간격으로 놓는다.

    처음에는 줄 순서로 고르게 벌렸는데, 같은 날 나온 Microsoft 셋이 축에서 서로 다른
    때에 선 것처럼 보였다. 축이 시간이라고 말해 놓고 시간이 아닌 값을 그린 자리다."""
    base = base or outs[0]['date']
    span = max(_months(base, outs[-1]['date']), 1)
    return int(x0 + (x1 - x0) * _months(base, r['date']) / float(span))


def _short(claim, n=34):
    s = claim.replace('**', '').strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def clash_pairs(rows):
    """엇갈림 (뒤에 온 줄, 앞선 줄) 짝. 날짜순."""
    by_id = {r['id']: r for r in rows}
    out = []
    for r in rows:
        for rel in r.get('rel') or ():
            if rel['kind'] == '엇갈림':
                out.append((r, by_id[rel['to']]))
    out.sort(key=lambda p: (p[0]['date'], p[0]['id']))
    return out


def clash_table(pairs):
    """엇갈림 다섯을 한 표에 세운다.

    걸린 자리는 다섯이 다 같은 한 줄이라 표 밖 머리글로 한 번만 쓴다 — 같은 값을
    다섯 번 세로로 쌓으면 표에서 견줄 것이 사라진다.

    「언제 것 · 성격」 열은 둔다. 걸림은 공표된 사실이 아니라 우리가 두 인용을 읽고
    매긴 판정이고, 표는 값을 나란히 놓아 같은 무게로 보이게 만들기 때문이다."""
    early = pairs[0][1]
    head = ('<p class="sub">걸린 자리는 다섯이 모두 같은 한 줄이다 — '
            '<b>%s %s</b> 「%s」</p>'
            % (early['date'], esc(early['org']), rich(early['claim'])))
    body = ['<tr><th>언제 · 누가</th><th>뒤에 온 주장</th><th>언제 것 · 성격</th></tr>']
    for late, _ in pairs:
        body.append('<tr><td>%s<br>%s</td><td>%s</td><td>%s · 판정(우리)</td></tr>'
                    % (late['date'], esc(late['org']), rich(_short(late['claim'], 70)),
                       late['date'][:7]))
    return '%s<div class="tw"><table>%s</table></div>' % (head, ''.join(body))


def row_html(r, by_id, tied):
    kinds = {rel['kind'] for rel in r['rel']} or {'신규'}
    mark = MARK['엇갈림'] if '엇갈림' in kinds else (
        MARK['동조'] if '동조' in kinds else MARK['신규'])
    faint = '' if r['id'] in tied else ' faint'
    ties = []
    for rel in r['rel']:
        src = by_id[rel['to']]
        ties.append(
            '<div class="tie%s">'
            '<a class="to" href="#%s"><b>%s</b> · %s %s 에 걸린다</a>'
            '<span class="q">%s</span><span class="q">%s</span></div>'
            % (' cross' if rel['kind'] == '엇갈림' else '',
               quote(src['id']), rel['kind'],
               src['date'], esc(src['org']), rich(src['claim']), rich(r['claim'])))
    return ('<div class="row%s" id="%s" data-kinds="%s" data-org="%s">'
            '<div class="mark">%s</div><div>'
            '<div class="when">%s</div>'
            '<div class="who">%s · %s</div>'
            '<p class="claim"><a class="card" href="ai-engineer/%s.html">%s</a></p>'
            '%s</div></div>'
            % (faint, esc(r['id']), ' '.join(sorted(kinds)), esc(r['org']), mark, r['date'],
               esc(r['org']), esc(r['speaker']), slug(title_of(r)), rich(r['claim']),
               ''.join(ties)))


def build():
    """재료를 읽어 HTML 한 장을 돌려준다. 파일로 쓰지는 않는다."""
    rows = lib.load()
    hard = lib.validate(rows)
    if hard:
        raise SystemExit('재료 규약 FAIL\n  ' + '\n  '.join(hard))
    by_id = {r['id']: r for r in rows}
    tied = set()
    for r in rows:
        for rel in r['rel']:
            tied.add(r['id'])
            tied.add(rel['to'])
    orgs = sorted({r['org'] for r in rows})
    comps = lib.components(rows)
    lone = lib.orphans(rows)

    # 덩어리와 표를 맞춘다. 어긋나면 화면을 안 만든다 — 자료가 바뀌면 이름부터 다시 붙인다.
    by_anchor = {c[0]['id']: c for c in comps}
    named = [s[1] for s in SECTIONS]
    miss = [a for a in named if a not in by_anchor]
    extra = [a for a in by_anchor if a not in named]
    if miss or extra:
        raise SystemExit(
            '덩어리와 절 표가 어긋난다 — SECTIONS 를 고친다\n'
            '  표에 있는데 덩어리가 없다: %s\n  덩어리인데 표에 없다: %s'
            % (', '.join(miss) or '없음', ', '.join(extra) or '없음'))

    pairs = clash_pairs(rows)

    # 차례. 대단원은 「1. 2. 3.」, 그 아래 절은 ①②③ — 한 줄에 하나씩.
    toc = ['<div class="toc"><b class="tl">이 화면은 물음 하나를 축 셋으로 따라갑니다 — %s.</b>'
           % ' · '.join(n for n, _ in AXES)]
    body = []
    for ax, (axis_name, axis_sub) in enumerate(AXES, 1):
        toc.append('<b class="tg">%d. %s</b>' % (ax, esc(axis_name)))
        body.append('<h2 id="ax-%d">%d. %s</h2><p class="sub">%s</p>'
                    % (ax, ax, esc(axis_name), esc(axis_sub)))
        n = 0
        for axis, anchor, title, verdict in SECTIONS:
            if axis != ax:
                continue
            comp = by_anchor[anchor]
            sid = 'sec-%s' % slug(title)
            toc.append('<span class="tt"><a href="#%s">%s %s</a></span>'
                       % (sid, CIRCLED[n], esc(title)))
            body.append('<div class="sec">')
            body.append('<h3 id="%s">%s %s <span class="when">%s줄 · %s ~ %s</span></h3>'
                        % (sid, CIRCLED[n], esc(title), len(comp),
                           comp[0]['date'][:7], comp[-1]['date'][:7]))
            body.append('<p class="verdict">%s</p>' % esc(verdict))
            body.extend(row_html(r, by_id, tied) for r in comp)
            body.append('</div>')
            n += 1
    toc.append('</div>')

    rest = ('<details class="rest"><summary>아직 아무 데도 안 걸린 주장 %d줄 — 판이 굳지 않은 자리</summary>'
            '<p class="sub">뒤에 온 발표가 아직 받지도 맞서지도 않은 주장이다. '
            '주장 %d줄 중 %d%%가 여기 있다.</p>%s</details>'
            % (len(lone), len(rows), round(100.0 * len(lone) / len(rows)),
               ''.join(row_html(r, by_id, tied) for r in lone)))

    end = ('<div class="end"><h2 id="end">이 화면이 말하지 않는 것</h2>'
           '<p>걸림은 발표자들이 서로 이름을 대고 주고받은 것이 아니라 두 인용을 읽고 '
           '우리가 매긴 판정이다. 그래서 관계 이름은 동조·엇갈림 둘뿐이다 — 서로 맞선 적이 '
           '없는 자리에 그보다 센 이름을 붙이면 없던 의도를 붙이는 것이 된다.</p>'
           '<p>걸림은 앞선 날짜만 가리킨다. %s 하루에 발표 %d편·주장 %d줄이 몰려 있는데 '
           '그날 줄끼리는 서로 안 걸리는 이유다 — 같은 무대에 선 발표들이 서로 답한 적이 없다.</p>'
           '<p>묶음은 걸림으로 이어진 덩어리를 그대로 쓴다. 물음 이름과 판단 한 줄은 그 덩어리의 '
           '줄을 다 읽고 붙인 것이고, 자료가 바뀌어 덩어리가 갈라지면 생성기가 멈춘다.</p></div>'
           % ('2025-08-26', len({r['talk'] for r in rows if r['date'] == '2025-08-26'}),
              len([r for r in rows if r['date'] == '2025-08-26'])))

    chips = ['<button class="chip" data-org="" aria-pressed="true">전부</button>']
    chips += ['<button class="chip" data-org="%s">%s</button>' % (esc(o), esc(o))
              for o in orgs]

    html = ('<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>AI Engineer 주장 흐름</title>\n' + CSS + '\n'
            + ui_bits.OPEN_AT_TOP + '\n<div class="wrap">\n'
            '<a class="card" href="AI Engineer 대시보드.html">← AI Engineer</a>\n'
            '<h1>주장 흐름</h1>\n'
            '<p class="lede">발표 %d편에서 주장 %d줄을 뽑아 뒤에 온 주장이 앞선 주장에 걸리는지를 '
            '따졌더니, 걸린 줄 %d개가 물음 %d개로 뭉쳤다. '
            '<b>그 가운데 갈린 물음은 하나다 — 어떻게까지 모델에 맡길 것인가.</b> '
            '나머지 %d개에서는 뒤에 온 발표가 앞선 말을 받기만 했다.</p>\n'
            '<p class="lede">재료는 %s ~ %s 다. 걸림 %d개 중 엇갈림은 %d개이고 전부 첫 절에 있다. '
            '아무 데도 안 걸린 주장 %d줄(%d%%)은 맨 아래 접어 뒀다 — 아직 판이 굳지 않은 자리다.</p>\n'
            '<div class="fig">%s</div>'
            '<p class="cap">갈린 물음 하나. 왼쪽 점이 2025-08 AWS 의 한 줄이고, 점선이 그 줄에 '
            '걸린 뒤 주장 넷이다. 날짜와 조직 말고 다른 값은 안 그렸다. 줄 앞 기호는 '
            '● 그 물음을 연 줄 · ↑ 앞선 주장에 걸린 줄 · ✕ 앞선 주장과 갈린 줄이다.</p>\n'
            '%s\n%s\n'
            '<div class="filters">%s</div>\n%s\n%s\n%s\n</div>\n%s\n'
            % (len({r['talk'] for r in rows}), len(rows), len(rows) - len(lone), len(comps),
               len(comps) - 1,
               rows[0]['date'], rows[-1]['date'],
               sum(len(r['rel']) for r in rows), len(pairs), len(lone),
               round(100.0 * len(lone) / len(rows)),
               clash_fig(pairs), clash_table(pairs), ''.join(toc),
               ''.join(chips), ''.join(body), rest, end, JS))
    return html


JS = '''<script>
(function () {
  var rows = [].slice.call(document.querySelectorAll('.row'));
  var org = '';
  function paint() {
    rows.forEach(function (el) {
      el.classList.toggle('off', !!org && el.dataset.org !== org);
    });
    [].forEach.call(document.querySelectorAll('.sec'), function (s) {
      var any = [].slice.call(s.querySelectorAll('.row')).some(function (el) {
        return !org || el.dataset.org === org;
      });
      s.hidden = !any;
    });
  }
  [].forEach.call(document.querySelectorAll('.chip'), function (b) {
    b.addEventListener('click', function () {
      org = b.dataset.org === org ? '' : b.dataset.org;
      [].forEach.call(document.querySelectorAll('.chip'), function (o) {
        o.setAttribute('aria-pressed', o.dataset.org === org ? 'true' : 'false');
      });
      paint();
    });
  });
  paint();
})();
</script>'''


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def rich(s):
    """주장 인용 한 줄. 원문의 굵게 표시(**…**)를 태그로 바꾼다.

    이 장의 본문은 통째로 원문 인용이라 마크다운 표시가 그대로 나오면 넷 중 하나가
    별표에 오염된다(126줄 중 35줄). 치환은 자매 조립기 gen_aie_dashboard 의
    BOLD_RE/BOLD_TO 를 그대로 쓴다 — 꼴이 갈라지면 한쪽만 낡는다.

    순서가 뒤집히면 안 된다. esc 가 먼저고 굵게가 나중이다. 반대로 하면 방금 넣은
    <b> 가 &lt;b&gt; 로 이스케이프돼 태그 대신 글자로 난다."""
    return BOLD_RE.sub(BOLD_TO, esc(s))


_TITLES = {}


def title_of(r):
    """카드 페이지 주소는 카드 제목의 슬러그다 — 변환본 프런트매터에서 읽는다."""
    talk = r['talk']
    if talk in _TITLES:
        return _TITLES[talk]
    got = talk
    for ln in (lib.md_lines(talk) or ())[:20]:
        if ln.startswith('title: '):
            got = ln[7:].strip()
            break
    _TITLES[talk] = got
    return got


def main():
    rows = lib.load()
    html = build()
    bad = check_ui(html, rows)
    for m in bad:
        print('FAIL ·', m)
    if bad:
        return 1
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('주장 %d줄 · 물음 %d개 · 고립 %.0f%% -> %s'
          % (len(rows), len(lib.components(rows)), lib.orphan_ratio(rows) * 100,
             os.path.basename(OUT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
