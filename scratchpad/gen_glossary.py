# -*- coding: utf-8 -*-
# 용어사전 — 이 저장소 글을 읽다 막히는 말을 한 장에 모은다.
# 카드 하나가 용어 하나다. 뜻만 적지 않고 그 말이 가리키는 물건이 실제로 어떻게 도는지까지 그린다.
# 마크업과 CSS는 dash_common이 갖고 있다 — 첫 화면 규약도 그쪽 머리말에 있다.
import html as _html
import os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import _agent_report as ar
import gen_anim_page as ga
import gen_ffn_page as gf
import gen_ngram_page as gn

OUT = os.path.join(dc.ROOT, '대시보드', '용어사전.html')

STAMP = '2026-08-24'

SEC_AGENT = ('sec-agent', '01', 'AI 에이전트 · 실행 구조',
             '모델이 혼자 못 하는 일을 누가 대신 하나')

SEC_MODEL = ('sec-model', '02', '모델 안쪽 · 계산 구조',
             '모델이 글자를 이어 붙일 때 안에서 무슨 계산이 도나')


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



_FT = gf.load_trace()
_PR = _FT['params']
_DM = _FT['d_model']
_DF = format(_FT['d_ff'], ',')
_QUIET = '%.1f' % (_FT['quiet_share'] * 100)
_FP = format(_PR['ffn_per_layer'], ',')
_AP = format(_PR['attn_per_layer'], ',')
_SHARE = '%.0f' % (_PR['ffn_share'] * 100)

FIG_ATTN = (1, '1막 — 어텐션 (23초짜리 한 바퀴)',
            ga.embed(ga.load_trace(), 'attn-scene'),
            '실제로 Qwen2.5-0.5B 를 한 번 돌려 뽑은 수치다. 「그것은」 자리의 Q 가 앞선 토큰들의 '
            'K 를 왼쪽부터 훑어 점수를 내고, 그 점수가 합 1 의 비율로 다시 선 뒤, 그 비율을 '
            '가중치로 V 를 가중평균해 출력 하나가 남는다.')

FIG_FFN = (5, '2막 — FFN (21초짜리 한 바퀴)',
           gf.embed(_FT, 'ffn-scene'),
           '위 1막이 낸 출력이 이 막의 입력이다. 같은 층·같은 자리에서 잰 수치다. 문장이 떴다가 '
           '「그것은」만 남는 것은 FFN 이 옆 토큰을 안 보기 때문이다. 넓힌 줄의 칸 하나가 '
           'key·value 짝 하나이고, 칸 밝기가 지금 문맥에 그 key 가 얼마나 걸렸는지다.')


_NG = gn.load_trace()
_NF = _NG['from']

FIG_NGRAM = (2, 'FFN 과 엔그램 — 21초짜리 한 바퀴',
             gn.embed(_NG, _FT, 'ngram-scene'),
             '같은 일(표에서 꺼내 잔차 스트림에 더한다)을 하는 둘을 나란히 놓았다. 왼쪽은 표를 '
             '끝까지 훑어야 어디가 걸리는지 알고, 오른쪽은 토큰 ID 로 행 번호를 먼저 낸다. '
             'FFN 쪽 가중치 개수는 Qwen2.5-0.5B 에서 세었고, 엔그램 쪽 수치는 SemiAnalysis '
             '뉴스레터 변환본에서 가져왔다.')

NGRAM = {
    'section': SEC_MODEL,
    'topic': ('memory', '모델 구조'),
    'title': '엔그램(N-gram 임베딩) — 곱셈 없이 표에서 꺼내는 기억',
    'gain': '「표를 HBM 밖으로 내보낸다」는 말이 왜 FFN 에는 안 되고 엔그램에는 되는지. '
            '최근 모델들이 메모리 벽을 우회하는 방식이다.',
    'meta': ['용어 풀이', '정리 2026-09-20', '모델 구조'],
    'oneliner': '엔그램은 최근 토큰 몇 개를 해시해 큰 표에서 행을 꺼내 쓰는 층이다. FFN 과 '
                '같이 「표에서 꺼내 잔차 스트림에 더한다」인데 꺼내는 방식이 다르다 — FFN 은 '
                '입력을 key 전부와 대 봐야 어디가 걸리는지 알고, 엔그램은 토큰 ID 만으로 읽을 '
                '행이 먼저 정해진다. 그 차이가 표를 어느 메모리에 둘 수 있느냐까지 끌고 간다.',
    'points': [
        '<b>키가 벡터가 아니라 토큰 ID 다.</b> 지금 토큰과 그 앞 한두 개를 이어 붙여 해시하면 '
        '행 번호가 나온다. 모델을 돌리지 않고 산수로만 나오는 값이라, 앞 층이 계산하는 동안 그 '
        '행을 미리 당겨 올 수 있다.',
        '<b>그래서 표가 HBM 밖으로 나간다.</b> 뉴스레터가 잰 DeepSeek-V4.1-Flash 기준으로 표는 '
        + _NF['deepseek_table_params'] + '(' + str(_NF['deepseek_table_gib']) + ' GiB)인데, '
        '토큰 자리 하나가 실제로 읽는 양은 두 층에서 ' + str(_NF['deepseek_rows_per_layer'])
        + '행씩, 모두 합쳐 ' + str(_NF['deepseek_kib_per_token']) + ' KiB 다. GPU 4 장에 '
        '나누면 한 장당 ' + str(_NF['deepseek_kib_per_gpu']) + ' KiB. 크지만 가끔 조금씩 읽는 '
        '표라 DRAM 이나 NVMe 에 둬도 버틴다.',
        '<b>FFN 은 같은 일을 못 한다.</b> 어느 key 가 걸릴지는 입력을 전부와 대 봐야 알기 '
        '때문에 가중치 전체를 매번 읽어야 한다. 한 층에 ' + _FP + ' 개다. 그래서 HBM 에 있어야 '
        '하고, 이 자리를 줄이려고 나온 것이 MoE(여러 벌 중 일부만 돌린다)와 엔그램(아예 안 '
        '돌리고 읽는다)이다.',
        '<b>해시라서 충돌이 난다.</b> 토큰 조합은 표 크기보다 훨씬 많아서 다른 조합이 같은 행에 '
        '떨어진다. 그래서 꺼낸 것을 그대로 쓰지 않고, 지금 문맥과 얼마나 맞는지를 재서 게이트로 '
        '누른 뒤 더한다. 롱캣은 그 충돌을 줄이려고 표 크기를 어휘 크기의 정수배로 잡지 말라고 '
        '권한다.',
        '<b>무엇을 외우는지는 사람 직관과 다르다.</b> 게이트 점수를 훑어 보니 이름·코드 조각· '
        '관계 표현과 함께 라이선스 문구나 API 뼈대 같은 상투 문구가 많이 걸렸다. 「중요한 사실」을 '
        '고르는 것이 아니라 다음 토큰 예측을 쉽게 만드는 것이 자리를 차지한다.',
        '<b>떼어 낼 수 있는 사전이 아니다.</b> 추론에서 엔그램을 빼면 이후 층의 표현과 전문가 '
        '선택 자체가 달라진다. 원 논문의 제거 실험에서 사실지식 벤치마크가 원래의 29~44% 로 '
        '떨어졌고, 모델이 스스로 전문가를 다시 고르게 놔두는 편이 손실을 일부 메웠다.',
    ],
    'figs': [FIG_NGRAM],
    'note': '행 번호는 이 저장소에서 실제 토크나이저로 문장을 자른 뒤 원문이 적은 방식(곱셈 '
            '해싱 + XOR 섞기)으로 계산한 값이다 — 그 모델이 쓰는 해시 그대로는 아니고, 「토큰 '
            'ID 만으로 읽을 자리가 정해진다」를 보이려고 같은 꼴로 구현했다. 표 크기·읽는 양은 '
            '뉴스레터 변환본에서 가져왔다. 굽는 자리는 '
            '<code>scratchpad/ngram_trace.py</code>.',
    'links': [
        ('Engrams Embedding Entendre — SemiAnalysis (2026-09-18)',
         'https://newsletter.semianalysis.com/p/engrams-embedding-entendre-codesign', ''),
    ],
}

LAYER = {
    'section': SEC_MODEL,
    'topic': ('compute', '모델 구조'),
    'title': '어텐션과 FFN — 트랜스포머 한 층이 하는 두 걸음',
    'gain': '모델이 글자를 이어 붙일 때 한 층에서 무슨 일이 벌어지는지. 「그것은」이 문장 앞의 '
            '무엇을 가리키는지 정하는 걸음과, 그 결과를 다듬는 걸음을 나눠 본다.',
    'meta': ['용어 풀이', '정리 2026-09-20', '모델 구조'],
    'oneliner': '트랜스포머 한 층은 두 걸음이다. 먼저 어텐션이 지금 토큰과 앞선 토큰들을 '
                '섞고, 그다음 FFN 이 그 결과를 토큰 하나하나에 따로 먹여 다듬는다. 섞는 '
                '걸음은 토큰끼리 서로 보고, 다듬는 걸음은 옆을 안 본다. 이 두 걸음이 층마다 '
                '되풀이된다.',
    'points': [
        '<b>Q·K·V 는 같은 토큰에서 뽑은 세 벡터다.</b> 같은 임베딩에 서로 다른 가중치를 '
        '곱해 만든다. Q(쿼리 — 내가 무엇을 찾는가)는 그 스텝에서 쓰고 버리고, K(키 — 나는 '
        '무엇을 들고 있는가)와 V(밸류 — 골라졌을 때 내줄 내용)는 한 번 만들면 그 토큰이 대화에 남아 있는 한 계속 '
        '다시 쓰여 캐시에 쌓인다 — 「KV 캐시」가 커진다는 말이 이 뜻이다. 그리고 얼마나 볼지를 '
        '정하는 것은 Q 와 K 인데 그 비율로 섞이는 것은 V 라, 어디를 많이 보느냐와 결과를 많이 '
        '정하느냐가 같지 않다.',
        '<b>점수를 비율로 바꾼 뒤 가중평균한다.</b> Q 와 K 를 곱하면(내적) 그 수가 클수록 그 '
        '토큰을 많이 본다. 크기가 제각각이라 소프트맥스로 합이 1 이 되게 눌러 「어느 토큰을 몇 '
        '퍼센트 볼까」로 만들고, 비율 × V 를 토큰마다 구해 전부 더한다.',
        '<b>정보는 가중치에 들어 있다.</b> 넓히는 행렬 자체가 그 정보다. ' + str(_DM) + ' × '
        + _DF + ' 행렬은 ' + str(_DM) + ' 칸짜리 벡터를 ' + _DF + ' 개 세워 둔 것이고, 그 열 '
        '하나하나가 학습 때 익힌 패턴 하나다 — 이것을 key(키 — 이 패턴이 들어왔나를 재는 자)라 '
        '부른다. 접는 행렬의 행 하나가 그 key 에 딸린 value(밸류 — 걸렸을 때 내놓을 내용)다. '
        '게바 등이 2021 년에 보인 것이 이 짝이고, 지금 통용되는 설명이다.',
        '<b>곱셈은 넓히는 일이 아니라 대조하는 일이다.</b> 입력 벡터에 그 행렬을 곱하면 입력을 '
        + _DF + ' 개 key 각각과 내적한다. 나온 결과의 j 번째 숫자는 「입력이 j 번 key 와 얼마나 '
        '닮았나」 하나다. 그러니 칸이 ' + _DF + ' 개가 된 것은 정보가 늘어서가 아니라 ' + _DF
        + ' 번 대조한 점수표이기 때문이다.',
        '<b>사전 찾기 세 동작이라고 보면 맞는다.</b> ① 표제어 ' + _DF + ' 개짜리 사전(넓히는 '
        '행렬)에 입력을 들고 가 전부와 대조해 점수표를 만든다 ② 문턱이 낮은 점수를 0 으로 눌러 '
        '실제로 걸린 표제어만 남긴다 — 이 모델에서 ' + _QUIET + '% 가 여기서 꺼진다 ③ 표제어마다 '
        '딸린 뜻풀이(접는 행렬)를 점수만큼 가중합해 원래 ' + str(_DM) + ' 칸으로 되돌린다.',
        '<b>그 표제어는 낱말이 아니다.</b> key 하나는 ' + str(_DM) + ' 칸짜리 방향 하나이고, '
        '그 방향과 닮은 입력이 오면 켜진다. 게바 논문이 사람에게 시켜 분류해 보니 아래쪽 층의 '
        'key 는 표면에 가까운 패턴(어떤 낱말로 끝나는 문장 꼴 같은)에, 위쪽 층은 주제나 뜻에 '
        '가까운 패턴에 걸렸다. value 도 「이 토큰을 내놓아라」가 아니라 다음 토큰 확률을 어느 '
        '쪽으로 밀지 정하는 방향이다.',
        '<b>낱말 사전은 따로 있다.</b> 토큰 ID 를 받아 벡터를 내주는 임베딩 표가 모델 맨 앞에, '
        '어휘로 되돌리는 표가 맨 뒤에 있다. 그쪽은 「350 번 토큰 → 이 벡터」처럼 번지수로 '
        '정확히 찾는다. FFN 의 key 에는 번지수가 없어 입력을 전부와 대 보고 닮은 정도로 '
        '걸린다 — 그래서 어느 key 가 걸릴지 미리 못 알고, 가중치 전체를 매번 읽어야 해서 '
        'HBM 에 둬야 한다. 엔그램(N-gram 임베딩) 표가 DRAM 으로 나갈 수 있는 것은 반대로 '
        '토큰 ID 만으로 읽을 행이 정해지기 때문이다.',
        '<b>사실 지식이 여기 들어 있다.</b> 멍 등이 2022 년에 보인 causal tracing 은 「파리는 '
        '프랑스의 수도」 같은 사실을 모델이 꺼낼 때 결정적인 자리가 중간 층들의 이 FFN 이라는 '
        '것을 짚었고, 그 자리만 고쳐 사실을 바꿔 넣는 것도 됐다. 어텐션이 문맥을 옮겨 오는 '
        '길이라면 FFN 은 모델이 이미 외워 둔 것을 꺼내 오는 자리다.',
        '<b>넓힐수록 표제어가 는다.</b> key·value 짝 하나가 기억 한 칸이라 칸 수가 곧 그 층이 '
        '담을 수 있는 패턴의 수다. 아래쪽 층의 key 는 얕은 패턴(글자 꼴·어구)에, 위쪽 층은 '
        '뜻에 가까운 패턴에 걸린다고 같은 연구가 짚었다.',
        '<b>문턱이 없으면 이 조회가 성립하지 않는다.</b> 곱셈과 덧셈은 들어온 수에 늘 같은 '
        '규칙을 먹여서 「이 key 가 걸렸을 때만 그 value 를 쓴다」가 안 나온다. 들어온 수에서 '
        '5 를 뺀 뒤 음수면 0 으로 만드는 식의 문턱이 있어야 걸린 것과 안 걸린 것이 나뉜다. '
        '문턱이 없으면 층을 아무리 쌓아도 한 층으로 접힌다 — 2 를 곱하고 3 을 더한 뒤 5 를 '
        '곱하고 1 을 더하면 10 을 곱하고 16 을 더한 것과 같다.',
        '<b>접어야 다음 층이 받는다.</b> 걸린 key 들의 value 를 모아 원래 폭으로 되돌린다. '
        '층들이 같은 폭을 주고받아야 쌓을 수 있고, 잔차 연결로 들어온 벡터에 '
        '더할 수도 있다. 「넓혔다 접는다」가 한 세트인 이유다.',
        '<b>넓히는 대가가 크다.</b> 이 모델 한 층에서 FFN 이 쓰는 가중치가 ' + _FP
        + ' 개인데 어텐션은 ' + _AP + ' 개다 — 층 안 가중치의 ' + _SHARE
        + '% 가 FFN 에 있다. MoE 가 굳이 이 자리를 여러 벌로 쪼개 토큰마다 일부만 돌리는 '
        '이유가 여기다. 엔그램(N-gram 임베딩)은 아예 곱셈 없이 표에서 행을 읽어 와 이 비용을 '
        '피한다.',
        '<b>어텐션은 한 번으로 안 끝난다.</b> 이 계산이 층마다, 그리고 층 안에서도 헤드 '
        '여럿으로 동시에 돈다. 헤드마다 보는 데가 달라서 어떤 헤드는 지시대명사가 가리키는 '
        '명사를, 어떤 헤드는 바로 앞 낱말을 본다. 위 1막은 그중 「그것은」이 앞 명사를 가장 '
        '세게 되짚는 헤드 하나를 골라 그린 것이고, 그 고른 기준을 화면에 적어 뒀다.',
        '<b>두 걸음의 성격이 다르다.</b> 어텐션은 토큰이 늘수록 볼 것이 늘어 계산과 캐시가 같이 '
        '커지지만, FFN 은 토큰마다 독립이라 서로 얽히지 않는다. 긴 문맥이 비싸지는 쪽은 '
        '어텐션이다.',
    ],
    'figs': [FIG_ATTN, FIG_FFN],
    'note': 'Q·K·V 옆과 FFN 입력·출력 옆에 적힌 숫자는 벡터의 첫 성분 하나다. 넓힌 칸 64 개도 '
            + _DF + ' 칸에서 고르게 뽑아 보인 것이고 전부가 아니다. 그 수치를 굽는 자리는 '
            '<code>scratchpad/attn_trace.py</code> 와 <code>scratchpad/ffn_trace.py</code> 이고, '
            '거기서 직접 계산한 결과가 모델이 낸 것과 같은지를 굽는 단계에서 검사한다. 가중치 '
            '개수는 모델 설정에서 바로 센 것이다.',
    'links': [
        ('FFN 은 key·value 기억 장치다 (Geva et al., EMNLP 2021)',
         'https://arxiv.org/abs/2012.14913', ''),
        ('사실 지식이 중간 층 FFN 에 있다 (Meng et al., NeurIPS 2022)',
         'https://arxiv.org/abs/2202.05262', ''),
    ],
}

CARDS = [
    NGRAM,
    LAYER,
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
      <span>용어 <b>%d개</b></span>
      <span>보고서 <b>1편</b> · 절 <b>11개</b></span>
    </div>''' % (STAMP, len(CARDS))

LEDE = '''<p class="lede">이 저장소의 글에 나오는 말을 하나씩 푸는 장입니다. 뜻만 적지 않고 그 말이 가리키는 물건이 실제로 어떻게 도는지를 그림으로 같이 답니다. 맨 앞 타일에는 그 말들이 한 판에서 어떻게 맞물리는지를 이은 보고서가 한 편 서 있습니다.</p>'''

FOOTER = (LEDE + META + '\n용어 풀이 · 카드 하나가 용어 하나입니다.\n'
          '  페이지 생성은 <code>scratchpad/gen_glossary.py</code>(공용 부품 <code>dash_common.py</code>).')

# 보고서 층 도해는 카드에 안 붙어 있다. check_fig 가 걷어 가도록 여기 내놓는다.
REPORT_FIGS = [(0,) + f for f in ar.FIGS]


# 보고서 층 표지. 통합 보고서 장에서 쓰는 것과 같은 모양이다 — 한 장에 성격이 다른
# 글이 둘 서므로 어디서 끊기는지가 보여야 한다.
REP_CSS = """
  .rep-head{margin:8px 0 18px;padding:18px 20px;border:1px solid var(--line);
            border-left:5px solid var(--accent);border-radius:12px;
            background:var(--accent-soft)}
  .rep-head .rn{display:block;font-size:11px;font-weight:850;letter-spacing:.08em;
                color:var(--accent-ink)}
  .rep-head h2{margin:6px 0 8px;font-size:21px;line-height:1.35}
  .rep-head .rm{margin:0;font-size:12.5px;line-height:1.7;color:var(--ink-2)}
  .rep-head .rm b{color:var(--ink)}
"""

if __name__ == '__main__':
    dc.render(CARDS, '용어사전', HEADER, FOOTER, OUT,
              page_slug='glossary',
              top=ar.report_html(FIG_SEQ[1:], STAMP), top_id='sec-agentrep',
              top_title='보고서 — 하네스 위에 무엇이 얹히나',
              top_sub='스킬·슬래시 명령·서브에이전트·훅·MCP가 각각 어느 줄에 꽂히나', top_n=1,
              extra_css=CODE_CSS + REP_CSS)
