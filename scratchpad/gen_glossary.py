# -*- coding: utf-8 -*-
# 용어사전 — 이 저장소 글을 읽다 막히는 말을 한 장에 모은다.
# 카드 하나가 용어 하나다. 뜻만 적지 않고 그 말이 가리키는 물건이 실제로 어떻게 도는지까지 그린다.
# 마크업과 CSS는 dash_common이 갖고 있다 — 첫 화면 규약도 그쪽 머리말에 있다.
import html as _html
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc

OUT = os.path.join(dc.ROOT, '대시보드', '용어사전.html')

STAMP = '2026-08-22'

SEC_AGENT = ('sec-agent', '01', 'AI 에이전트 · 실행 구조',
             '모델이 혼자 못 하는 일을 누가 대신 하나')


# ── 하네스 시퀀스 도해 ───────────────────────────────────────────────────────
# 기둥 넷의 가로 위치. 하네스(B)가 가운데인 것이 이 그림의 요지다 — 사용자도 모델도
# 서로에게 직접 말을 걸지 않고 전부 B를 거친다.
#
# viewBox 폭은 560이다. 도해는 카드 본문 폭에 맞춰 줄어드는데, 창이 좁으면 본문이
# 460px 남짓까지 좁아진다(창 604px에서 재 봤다). 판을 좁게 그릴수록 그 축소가
# 덜해 글자가 커진다 — 번호가 안 보인다는 말이 두 번 나온 자리다.
# 번호는 라벨과 떼어 따로 세운다 — 아래 타입스크립트의 왼쪽 칸과 짝이라 눈에 먼저
# 걸려야 한다.
_A, _B, _C, _D = 48, 198, 340, 485
_MSGS = [
    (_A, _B, '①', '버그 고쳐 줘'),
    (_B, _C, '②', '프롬프트와 지금까지의 상태 전달'),
    (_C, _B, '③', 'EXEC: pytest 실행 지시'),
    (_B, _D, '④', '터미널에서 명령 실행'),
    (_D, _B, '⑤', '실행 결과 · 에러 로그'),
    (_B, _C, '⑥', '로그 줄여 에러만 전달'),
    (_C, _B, '⑦', 'EXEC: patch app.py 지시'),
    (_B, _D, '⑧', '코드 고치고 다시 테스트'),
    (_D, _B, '⑨', '테스트 통과'),
    (_B, _C, '⑩', '이걸로 끝났는지 확인'),
    (_C, _B, '⑪', '버그 수정 완료'),
    (_B, _A, '⑫', '최종 보고'),
]
_HEADS = [(_A, 96, '사용자'), (_B, 140, '하네스'), (_C, 126, 'AI 모델(LLM)'),
          (_D, 150, '실제 환경(OS·터미널)')]


def _seq_svg():
    y0, step = 92, 46
    bottom = y0 + (len(_MSGS) - 1) * step + 24
    h = ['<svg viewBox="0 0 560 %d" role="img" aria-label="하네스가 사용자·모델·터미널 '
         '사이에서 열두 번 주고받는 순서">' % (bottom + 10)]
    for cx, w, lab in _HEADS:
        h.append('<rect class="body" x="%d" y="6" width="%d" height="36" rx="8"/>'
                 % (cx - w // 2, w))
        h.append('<text x="%d" y="30" class="t-head" text-anchor="middle">%s</text>' % (cx, lab))
        h.append('<line class="lead-line" x1="%d" y1="46" x2="%d" y2="%d"/>' % (cx, cx, bottom))
    for i, (x1, x2, num, lab) in enumerate(_MSGS):
        y = y0 + i * step
        x = min(x1, x2) + 8
        h.append('<line class="flow" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (x1 + (7 if x2 > x1 else -7), y, x2 + (-7 if x2 > x1 else 7), y))
        h.append('<text x="%d" y="%d" class="t-no">%s</text>' % (x, y - 8, num))
        h.append('<text x="%d" y="%d" class="t-msg">%s</text>' % (x + 26, y - 8, lab))
    h.append('</svg>')
    return ''.join(h)


FIG_SEQ = (2, '하네스가 도는 한 판',
           _seq_svg(),
           '요청 하나가 도는 순서다. 사용자와 모델은 서로 직접 말하지 않고, 모델과 터미널도 '
           '직접 닿지 않는다. 열두 줄이 전부 가운데 기둥을 거친다. 줄 앞의 번호는 아래 '
           '타입스크립트의 왼쪽 칸에 그대로 다시 나온다 — 그 화살표를 내는 코드가 어느 줄인지다.')

# ── 코드 블록 ────────────────────────────────────────────────────────────────
# 도해가 「누가 누구에게」를 보여 준다면 코드는 「그래서 무엇을 되풀이하나」를 보여 준다.
# 둘을 잇는 것이 번호다. 코드 왼쪽 칸에 도해의 화살표 번호를 세워 두고, 도해 쪽에도
# 같은 줄의 글자를 그대로 옮겨 적는다 — 한쪽을 고치면 다른 쪽도 같이 고쳐야 한다.
#
# 각 줄은 `번호|코드` 꼴로 적는다. 번호가 없는 줄은 `|`만 남긴다. 코드 안에도 `|`가
# 나오므로(유니언 타입) 맨 앞 하나에서만 자른다.
def _code(src):
    """코드 한 덩어리를 <pre>로. 왼쪽에 도해 번호 칸을 세우고 주석은 흐리게 갈라 둔다."""
    out = []
    for line in src.strip('\n').split('\n'):
        num, _, body = line.partition('|')
        i = body.find('//')
        if i < 0:
            code = _html.escape(body, quote=False)
        else:
            code = (_html.escape(body[:i], quote=False)
                    + '<span class="cd-c">%s</span>' % _html.escape(body[i:], quote=False))
        out.append('<span class="cd-n">%s</span>%s' % (num.strip(), code))
    return '<pre class="uc-code">%s</pre>' % '\n'.join(out)


# 왼쪽 칸의 번호는 위 도해의 화살표다. ⑦~⑩은 새 줄이 아니라 ②~⑥을 한 바퀴 더 도는
# 것이라 칸에 적지 않는다 — 도해에서 그 자리에 ↻를 달아 둔 이유다.
_TS = r"""
 |type Msg = { role: "user" | "assistant" | "tool"; text: string };
 |
 |async function harness(ask: string) {
 |  // 상태는 하네스가 들고 있다. 모델은 요청과 요청 사이에 아무것도 기억하지 않는다
①|  const state: Msg[] = [{ role: "user", text: RULES + "\n" + ask }];
 |
 |  while (true) {
②|    const reply = await model.complete(state, TOOLS);   // 상태를 통째로 보낸다
 |    state.push({ role: "assistant", text: reply.text });
 |
 |    // 모델이 낸 것은 글자뿐이다. 도구 호출도 실행이 아니라 JSON 한 조각이다
⑪⑫|    if (reply.toolCalls.length === 0) return reply.text;
 |
③|    for (const call of reply.toolCalls) {          // 모델이 적어 보낸 명령
 |      if (risky(call)) await askUser(call);        // 지우는 명령 앞에서 멈춘다
④⑤|      const log = await runInShell(call);          // 셸에 실제로 던진다
⑥|      state.push({ role: "tool", text: shrink(log) });  // 실패한 줄만 남긴다
 |    }
 |    if (stuckOnSameError(state)) return "같은 실패가 되풀이돼 멈춥니다";
 |  }
 |}
"""

FIG_TS = (6, 'Loop (Typescript)',
          _code(_TS),
          '실제 하네스의 뼈대다. 왼쪽 칸의 번호가 위 도해의 화살표 번호다 — ①에서 요청을 '
          '상태에 담고, ②에서 모델을 부르고, ③~⑥에서 도구 호출을 하나씩 돌린 뒤, 부를 것이 '
          '없으면 ⑪⑫에서 빠져나온다. ⑦~⑩은 ②~⑥을 한 바퀴 더 도는 자리라 새로 나오는 줄이 없다. '
          '로그를 깎는 것도(shrink) 권한을 묻는 것도(askUser) 모델이 아니라 이 함수 안에 있다.')


CODE_CSS = """
  .uc-code { margin:0; padding:13px 15px; background:var(--sunk);
    border:1px solid var(--line); border-radius:8px; overflow-x:auto;
    font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    font-size:12.5px; line-height:1.85; color:var(--ink); white-space:pre; }
  .uc-code .cd-c { color:var(--ink-3); }
  /* 번호 칸. 동그라미 숫자는 고정폭 글꼴에서 대체 글리프로 떨어져 잘게 나온다 —
     본문 글꼴로 되돌리고 키운다. 칸 폭은 px로 고정해야 코드 들여쓰기가 안 밀린다. */
  .uc-code .cd-n { display:inline-block; width:42px; font-size:18px; line-height:1;
    font-family:"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;
    font-weight:800; color:var(--accent-ink);
    letter-spacing:-.02em; vertical-align:baseline; }
  .uc-fig text.t-head { font-size:13px; font-weight:800; fill:var(--ink); }
  .uc-fig text.t-no { font-size:19px; font-weight:800; fill:var(--accent-ink); }
  .uc-fig text.t-msg { font-size:13.5px; fill:var(--ink-2); }
  @media (max-width:640px) { .uc-code { padding:11px 10px; } }
"""


CARDS = [
    {'section': SEC_AGENT,
     'topic': ('market', 'AI 에이전트'),
     'title': '하네스(harness) — 모델과 컴퓨터 사이에 서는 실행 프로그램',
     'gain': '「클로드 코드가 파일을 고쳤다」고 할 때 실제로 파일을 고친 것이 무엇인지. 모델이 낸 글자가 터미널 명령이 되어 돌아오기까지 열두 번을 오간다.',
     'meta': ['용어 풀이', '정리 2026-08-22', 'AI 에이전트'],
     'oneliner': '하네스는 AI 모델과 실제 컴퓨터 사이에 서서 모델이 뱉은 글자를 실행으로 바꾸는 프로그램이다. 모델은 다음에 올 토큰(한 번에 내놓는 글자 조각)을 이어 붙일 뿐 파일을 열지도 명령을 돌리지도 못한다. 그 글자를 셸에 던지고, 돌아온 로그를 모델이 읽을 크기로 줄여 다시 넣어 준다. 이 일을 맡은 프로그램이 하네스다.',
     'points': [
         '<b>모델은 글자만 낸다.</b> <code>pytest</code>라고 써 놓아도 그 자체로는 아무 일도 안 벌어진다. 답이 옳은지 그른지와 무관하게, 모델의 출력은 문서 한 조각이다.',
         '<b>하네스가 그 글자를 명령으로 집행한다.</b> 미리 약속한 표시(<code>EXEC:</code> 같은 접두어나 도구 호출 JSON)를 찾아내 셸과 파일 시스템에 실제로 던진다. 클로드 코드·커서·오픈 인터프리터가 전부 하네스다.',
         '<b>한 번 오가고 끝나지 않는다.</b> 위 그림에서 ③~⑨가 실행 고리다. 테스트가 깨지면 로그가 모델로 돌아가고, 모델이 다음 명령을 내고, 하네스가 또 돌린다. 통과가 나올 때까지 이 고리를 반복하는 것이 에이전트라고 부르는 동작의 전부다.',
         '<b>결과를 그대로 넣지 않는다.</b> 컨텍스트 창(모델이 한 번에 볼 수 있는 글자 총량)이 정해져 있어 로그 수천 줄을 통째로 넘기면 앞서 넣어 둔 지시가 밀려 나간다. ⑥에서 하네스가 실패한 줄만 남기고 줄이는 이유다.',
         '<b>지금까지의 상태는 하네스가 들고 있다.</b> 모델은 요청과 요청 사이에 기억이 없다. 어느 디렉터리에 있는지, 무엇을 이미 고쳤는지, 쓸 수 있는 도구가 무엇인지를 요청마다 ②에서 다시 붙여 넣는다.',
         '<b>권한과 정지도 하네스가 쥔다.</b> 파일을 지우는 명령 앞에서 사용자에게 물어보고, 같은 실패가 되풀이되면 고리를 끊는다. 모델이 같아도 이 판단이 다르면 같은 과제의 완주율이 달라진다.',
         '<b>실무에서 「에이전트」라고 부르는 물건은 모델과 하네스를 합친 것이다.</b> GPT-5나 클로드 같은 모델 이름은 그중 한쪽만 가리킨다. 도구 성능을 견줄 때 모델 점수만 보면 나머지 절반을 빼고 세는 셈이다.',
     ],
     'figs': [FIG_SEQ, FIG_TS],
     'note': '<code>EXEC:</code>는 설명을 위해 쓴 표시다. 실제 제품은 도구 호출(tool use) 규격에 맞춘 JSON을 주고받는 쪽이 많다. 순서와 역할 분담은 같다. 코드도 뼈대만 남긴 것이다 — 실제 하네스에는 답을 한 글자씩 받아 보여 주는 처리, 끊긴 요청을 다시 부르는 처리, 오래된 대화를 요약해 넣는 처리가 더 붙는다.',
     'links': [],
    },
]


HEADER = '''  <header>
    <p class="eyebrow">용어사전 — 읽다 막히는 말</p>
    <h1>용어사전</h1>
  </header>'''

META = '''    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>수록 <b>%d개</b></span>
    </div>''' % (STAMP, len(CARDS))

LEDE = '''<p class="lede">이 저장소의 글에 나오는 말을 하나씩 푸는 장입니다. 뜻만 적지 않고 그 말이 가리키는 물건이 실제로 어떻게 도는지를 그림으로 같이 답니다.</p>'''

FOOTER = (LEDE + META + '\n용어 풀이 · 카드 하나가 용어 하나입니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_glossary.py</code>(공용 부품 <code>dash_common.py</code>).')

if __name__ == '__main__':
    dc.render(CARDS, '용어사전', HEADER, FOOTER, OUT, extra_css=CODE_CSS)
