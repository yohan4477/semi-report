# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — daily.semidoped.com 전사본을 카드로 낸다.

백지에서 다시 짓는 판이다. 앞선 판은 카드를 스물일곱 장 먼저 깔고 구조를 나중에
얹었다. 그래서 각도 상자·목차·축이 카드마다 다른 때에 다른 꼴로 붙었고, 고칠 때마다
스물일곱 장을 한꺼번에 건드려야 했다. 이번에는 **한 장을 끝까지 세워 보이고 그것을
본 뒤에 나머지로 옮긴다.**

카드 한 장의 뼈대:

    앞머리      물음 하나 · 바탕(무슨 재료 몇 편) · 축(묶음 둘셋)
    각도        접혀 있다. 눌러야 펴진다 — 원문이 어떤 마디로 뽑혔는지는
                읽는 사람이 필요할 때 여는 것이지 늘 펴 놓고 볼 것이 아니다
    목차        대상의 마디 + 글의 꼴 두 열
    절          제목이 물음을 답한다. 번호는 ①②③
    한계        마지막 절. 검증 안 한 것, 진행자 추정인 것

생성물이다. 고칠 것은 이 파일이다.

  py -3.13 scratchpad/gen_semidoped_dashboard.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))

import dash_common as dc  # noqa: E402
import semidoped_figs as figs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', 'Semi Doped 대시보드.html')
SRC = 'content/understanding/Semi Doped/'
BLOB = 'https://github.com/johnn8n/semianalysis/blob/main/'


def blob(p):
    return BLOB + p.replace(' ', '%20')


def angles(items):
    """각도 상자 — 접혀 있다.

    items = [(마디, 세웠나, [(물음, 꼴, [(축, 값)…])…])].

    목차는 「이 카드가 무엇을 말하나」이고 각도는 「원문이 어떤 마디로 뽑혔나」다. 둘이
    같지 않다 — 원문이 다룬 것 중 카드가 절로 안 세운 것이 늘 있고, 그것을 감추면
    카드가 원문 전부인 것처럼 읽힌다. 다만 늘 펴 놓으면 본문보다 먼저 눈에 들어와
    카드가 목록으로 보인다. **눌러야 펴진다.**

    축 이름은 그 물음을 답하는 데 필요한 칸이다. 값만 늘어놓으면 무엇과 무엇이
    겹치는지가 안 보인다.
    """
    li = []
    on = 0
    for node, used, subs in items:
        on += 1 if used else 0
        kids = []
        for q, form, rows in subs:
            body = ''.join('<li><span class="sa-x">%s</span>'
                           '<span class="sa-v">%s</span></li>' % r for r in rows)
            kids.append('<li><span class="sa-q">%s</span>'
                        '<span class="sa-f">%s</span><ul>%s</ul></li>'
                        % (q, form, body))
        li.append('<li class="%s"><span class="sa-n">%s</span><ul>%s</ul></li>'
                  % ('sa-on' if used else 'sa-off', node, ''.join(kids)))
    return ('<details class="sa"><summary>각도 %d <span>· 이 편이 어떤 마디로 '
            '뽑혔나 (절로 세운 것 %d)</span></summary><ul class="sa-t">%s</ul>'
            '<p class="sa-note">진한 마디가 이 카드가 절로 세운 것이다. 흐린 마디는 '
            '원문에는 있는데 이 카드가 안 세운 것 — 감추면 카드가 원문 전부인 것처럼 '
            '읽힌다.</p></details>' % (len(items), on, ''.join(li)))


JAL_ANGLES = [
    ('설계 기준', True, [
        ('무엇을 재나', '부분 나눔',
         [('시간', '마지막 토큰까지의 종단간 지연'),
          ('에너지', '요청당 에너지'),
          ('내는 꼴', '수치 하나 말고 파레토 곡선')]),
        ('누가 정하나', '대비',
         [('상업 벤더', '총소유비용을 먼저 본다'),
          ('모델랩', '최종 사용자를 먼저 본다')])]),
    ('벤치마크', True, [
        ('무엇으로 쟀나', '부분 나눔',
         [('도구', 'SemiAnalysis Inference X'),
          ('조건', '파워 정규화'),
          ('고른 이유', '소형~대형 오픈 모델로 시스템 전체를 잰다')]),
        ('무엇이 나왔나', '부분 나눔',
         [('DeepSeek R1 6,710억', '파레토 프론티어를 새로 그었다'),
          ('GPT-OSS 1,200억', '사용자당 초당 1,000토큰 이상'),
          ('전력', '700W 대 GB200 약 1,200W')]),
        ('무엇이 안 재졌나', '조건 갈림',
         [('입출력 길이', '8K 입력·1K 출력 · 100만 토큰급은 미공개'),
          ('부하 종류', 'agentic 은 아직 · AgentX 로 잴 계획'),
          ('견준 상대', '할라페뇨는 HBM4 · 블랙웰은 HBM3E')])]),
    ('메모리 배치', True, [
        ('대역폭이 있는데 왜 못 쓰나', '문제와 처방',
         [('있는 것', '128칩 HBM4 합쳐 초당 약 1PB'),
          ('이론값', 'FP4 1조 파라미터 · 약 0.5TB 면 초당 약 2,000토큰'),
          ('막는 것', '연산에 쓸 값이 레지스터에 늦게 온다'),
          ('막는 것', 'HBM 을 이웃 가속기와 나눠 쓰며 다툰다')]),
        ('무엇으로 푸나', '문제와 처방',
         [('붙이는 곳', '가속기마다 전용 로컬 HBM 조각'),
          ('길', '전용 저지연 버스'),
          ('부르는 이름', 'NUMA — 원래 멀티코어 CPU 에서 온 개념')])]),
    ('스케일업 도메인', True, [
        ('칩 몇 개가 한 덩어리로 도나', '층위',
         [('안쪽 겹', '128칩 · 칩당 초당 600Gb'),
          ('바깥 겹', '최대 2,048칩 · 초당 200Gb'),
          ('규약', 'ESUN — 브로드컴 주도 · UALink 와 다른 진영'),
          ('스위치', '브로드컴 Tomahawk 6')])]),
    ('칩 분업', True, [
        ('왜 프리필·디코드 칩을 안 나눴나', '조건 갈림',
         [('비율이 고정이면', '전담 칩이 낫다'),
          ('비율이 바뀌면', '전담 칩이 논다'),
          ('실제', '워크로드마다 프리필과 초안·검증 비율이 계속 바뀐다'),
          ('그래서', '한 칩을 균형 잡고 안 쓰는 회로는 전원을 끊는다')])]),
    ('개발 주기', True, [
        ('9개월이 어떻게 나왔나', '시간 흐름',
         [('첫 RTL', 'GPT-3급 모델로 짰다'),
          ('그 뒤', '모델이 좋아지면서 더 나은 것으로 바꿨다'),
          ('테이프아웃', '거기까지 9개월 · 통상 2~3년')])]),
    ('사람', False, [
        ('누가 발표했나', '부분 나눔',
         [('Richard Ho', '전 구글 TPU 팀'),
          ('Ravi', '칩 아키텍트'),
          ('Chris', '소프트웨어 공동설계')])]),
    ('파트너', False, [
        ('누가 붙었나', '부분 나눔',
         [('브로드컴', '로드맵 슬라이드에 파트너로'),
          ('셀레스티카', '같은 슬라이드 · 시스템 설계 역할은 추정')])]),
    ('로드맵', False, [
        ('다음은 무엇인가', '시간 흐름',
         [('2세대', '테이프아웃 근접'), ('3세대', '구상 중')])]),
    ('설계 태도', False, [
        ('무엇이 가장 어려웠나', '인과 사슬',
         [('회한 요인', '한계비용과 기회비용을 같이 본다'),
          ('둘 중 큰 것', '기회비용 — 수요가 있는데 기능이 없어 놓치는 것'),
          ('가장 어려운 결정', '무엇을 뺄지')])]),
    ('범용성', False, [
        ('왜 남의 모델까지 돌렸나', '조건 갈림',
         [('보인 것', 'GPT-OSS 부터 Kimi K2.5 까지 · Doom 도 돌렸다'),
          ('한 갈래', '자사 모델에만 맞추면 더 세게 낼 수 있다는 반론'),
          ('다른 갈래', '팹을 열듯 남에게 빌려주는 길 · 진행자 제안')])]),
    ('프레이밍', False, [
        ('무엇을 뒤집나', '인과 사슬',
         [('바뀐 것', '오픈AI 가 직접 추론 칩을 만든다'),
          ('그래서', '기준이 데이터센터 운영자의 셈에서 사용자 경험으로 옮겨 간다'),
          ('아직 안 한 곳', '앤트로픽은 자체 칩이 없다')])]),
]

JAL = {
    'id': 'sd-jalapeno',
    'section': ('sd-infer', '01', '추론 하드웨어',
                '칩 하나가 무엇을 기준으로 설계됐나'),
    'title': '오픈AI 할라페뇨 — 모델을 파는 회사가 칩을 만들면 기준이 어디로 가나',
    'gain': ('오픈AI 첫 추론 칩의 설계 기준이 마지막 토큰까지의 '
             '지연과 요청당 에너지라는 것 — 총소유비용은 그다음이다. 대역폭을 깔고도 왜 다 못 쓰는지, '
             '프리필·디코드 칩을 왜 안 나눴는지, 9개월이 어떻게 나왔는지.'),
    'meta': ['Austin · Vik Sekar <b>Semi Doped 공동 진행</b>',
             '업로드 2026-08-27', '게스트 없음', '발표 12시간 뒤 녹음'],
    'links': [('요약본', blob(SRC + '2026-08-27-openai-jalapeno.md'), ''),
              ('원문(Semi Doped)',
               'https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling',
               'ghost')],
    'verdict': ('<b>물음.</b> 모델을 파는 회사가 칩을 만들면 설계 기준이 어디로 옮겨 가나. '
                '<b>바탕.</b> Semi Doped 2026-08-27 한 편. 오픈AI 가 Hot Chips 에서 '
                '할라페뇨를 발표한 지 열두 시간이 안 돼 녹음한 전사본이고, 진행자 둘이 '
                '슬라이드를 순서대로 읽는다. <b>축.</b> 무엇을 기준으로 잡았나 · 메모리를 '
                '어떻게 다뤘나 · 무엇이 아직 안 재졌나 셋으로 나눴다.'),
    'report': [
        ('raw', angles(JAL_ANGLES)),
        ('toc', [
            ('설계 기준', '대비', [('①', '무엇을 재기로 했나')]),
            ('칩 안', '부분 나눔', [('②', '메모리를 어떻게 붙였나'),
                                ('③', '왜 프리필·디코드 칩을 안 나눴나')]),
            ('칩 사이', '층위', [('④', '칩 몇 개가 한 덩어리로 도나')]),
            ('성능', '대비', [('⑤', '재 보니 무엇이 나왔나'),
                            ('⑥', '무엇이 아직 안 재졌나')]),
            ('개발 주기', '시간 흐름', [('⑦', '9개월이 어떻게 나왔나')]),
            ('한계', '', [('⑧', '이 편이 밝히지 않은 것')]),
        ]),

        ('h', '① 무엇을 재기로 했나'),
        ('p', '지표 둘이다. <b>마지막 토큰까지 걸리는 종단간 지연</b>과 <b>요청당 에너지</b>. '
              '둘은 서로 밀어내는 값이라 오픈AI 는 수치 하나를 내지 않고 늘 파레토 곡선으로 '
              '보이겠다고 했다. 엔비디아·AMD 가 총소유비용을 먼저 놓는 것과 다르다 — '
              '데이터센터 운영자의 셈이 아니라 챗을 쓰는 사람이 겪는 것이 기준에 앉았다.'),
        ('fig', ('설계 기준이 어디로 옮겼나', figs.CRITERIA,
                 '왼쪽은 데이터센터 운영자의 셈이고 오른쪽은 사용자 경험이다. 오픈AI 는 '
                 '오른쪽 둘을 골랐고, 두 값이 상충하므로 곡선으로 낸다.')),

        ('h', '② 메모리를 어떻게 붙였나'),
        ('p', '128칩의 HBM4 를 합치면 초당 약 1페타바이트다. 진행자 셈으로 FP4 에서 1조 '
              '파라미터 모델이 약 0.5테라바이트니, 대역폭만 보면 <b>초당 약 2,000토큰</b>이 '
              '나와야 한다. 실제로는 거기 못 미친다.'),
        ('p', '오픈AI 설명은 둘이다. 연산에 쓸 값이 필요한 때에 레지스터로 안 온다는 것, '
              '그리고 HBM 을 이웃 가속기와 나눠 쓰면서 다툰다는 것. 그래서 가속기마다 '
              '<b>전용 로컬 HBM 조각</b>과 <b>전용 저지연 버스</b>를 두는 NUMA(비균일 메모리 '
              '접근 — 원래 멀티코어 CPU 에서 코어마다 메모리를 전담시키던 방식) 꼴로 갔다.'),

        ('h', '③ 왜 프리필·디코드 칩을 안 나눴나'),
        ('p', 'GPU 에서는 프리필(질문을 한꺼번에 읽는 단계)과 디코드(토큰을 하나씩 내는 단계)를 '
              '다른 칩에 맡기는 길이 있다. 오픈AI 는 안 나눴다. 워크로드마다 프리필과 '
              '초안·검증(작은 모델이 토큰 여러 개를 미리 내고 큰 모델이 맞는 것만 고르는 방식)의 '
              '비율이 계속 바뀌기 때문이다. 비율이 바뀌면 전담 칩이 논다.'),
        ('p', '그래서 칩 하나를 균형 잡고, 그 순간 안 쓰는 회로는 전원을 끊는다. 슬라이드 문구가 '
              '그 판단을 그대로 말한다 — <b>dark silicon is cheaper than idle accelerators</b>.'),

        ('h', '④ 칩 몇 개가 한 덩어리로 도나'),
        ('p', '겹이 둘이다. 안쪽은 <b>128칩</b>이 칩당 초당 600기가비트로 붙고, 바깥은 '
              '<b>최대 2,048칩</b>이 초당 200기가비트로 붙는다. 스위치는 브로드컴 Tomahawk 6 '
              '이고 규약은 ESUN 이다 — 브로드컴이 미는 스케일업 네트워킹이고 UALink 와 다른 '
              '진영이다. 128 이 한 랙이면 2,048 은 약 열여섯 랙이라는 것이 진행자 어림이다.'),
        ('fig', ('스케일업 도메인 두 겹', figs.DOMAIN,
                 '안쪽 겹은 칩당 초당 600기가비트, 바깥 겹은 초당 200기가비트다. 랙 수는 '
                 '원문에 없고 128 과 2,048 을 나눈 진행자 어림이다.')),

        ('h', '⑤ 재 보니 무엇이 나왔나'),
        ('p', '잰 도구는 SemiAnalysis 의 <b>Inference X</b>다. 파워를 정규화해 공개 비교했고, '
              '소형부터 대형까지 여러 오픈 모델을 돌려 시스템 전체가 사용자에게 주는 것을 '
              '본다는 이유를 댔다. 나온 것은 셋이다. DeepSeek R1(6,710억 파라미터)에서 파레토 '
              '프론티어를 새로 그었고, GPT-OSS(1,200억)에서 <b>사용자당 초당 1,000토큰 이상</b>을 '
              '냈으며, 700W 로 GB200 약 1,200W 보다 훨씬 적게 먹었다.'),

        ('h', '⑥ 무엇이 아직 안 재졌나'),
        ('p', '셋 남는다. 벤치마크의 입출력이 8K·1K 로 짧아 100만 토큰급 긴 문맥은 아직 안 '
              '나왔고, agentic 워크로드는 테스트하지 않아 별도 AgentX 로 재겠다고 했다. '
              '견준 상대도 세대가 다르다 — 할라페뇨는 HBM4 를 쓰고 블랙웰·MI355 는 HBM3E 다. '
              '진행자들이 스스로 Vera Rubin·Helios 와 견줘야 공평하다고 말한다.'),
        ('tbl', ('재진 것과 안 재진 것',
                 ['재는 것', '나온 값', '언제 것 · 성격'],
                 [['DeepSeek R1 6,710억', '파레토 프론티어를 새로 그었다',
                   '2026-08 · 발표 슬라이드'],
                  ['GPT-OSS 1,200억', '사용자당 초당 1,000토큰 이상', '2026-08 · 발표 슬라이드'],
                  ['전력', '700W · GB200 은 약 1,200W', '2026-08 · GB200 값은 진행자 어림'],
                  ['긴 문맥', '100만 토큰급 미공개', '2026-08 · 안 나온 값'],
                  ['agentic 부하', 'AgentX 로 재겠다', '2026-08 · 계획'],
                  ['견준 상대', 'HBM4 대 HBM3E', '2026-08 · 진행자 지적']])),

        ('h', '⑦ 9개월이 어떻게 나왔나'),
        ('p', '첫 RTL(회로를 글로 적은 설계) 작성부터 테이프아웃까지 <b>9개월</b>이다. 통상 '
              '2~3년 걸리는 일이다. 초기 RTL 을 GPT-3급 모델로 짰고 이후 모델이 좋아지면서 '
              '더 나은 것으로 바꿨다는 것이 진행자 전언이다. 진행자들은 첫 칩을 보통 '
              '버리는 셈 치는데 오픈AI 는 1호부터 세게 나왔다고 본다.'),

        ('h', '⑧ 이 편이 밝히지 않은 것'),
        ('p', '스펙 상당수가 진행자 추측이다. CPU 가 x86 계열 Turin 급인지, 공정이 TSMC N3 '
              '변형인지, HBM 이 삼성 것인지는 오픈AI 가 확인한 것이 아니다. 삼성 HBM4 가 '
              'SK하이닉스보다 핀당 빠를 수 있다는 대목은 진행자 본인이 전적으로 추측이라고 '
              '못박았다. 셀레스티카가 시스템 설계 파트너라는 것도 추정이고, 테이프아웃과 초기 '
              '양산에 약 1억 달러가 든다는 말도 확정치가 아닌 어림이다.'),
        ('p', '이 카드가 절로 세우지 않은 마디도 남는다 — 발표자 셋이 누구인지, 무엇을 뺄지가 '
              '가장 어려운 결정이었다는 설계 태도, 남의 모델까지 돌려 보인 이유. 각도 상자를 '
              '열면 그 마디들이 흐리게 서 있다.'),
    ],
}

CARDS = [JAL]

CSS = '''
/* 각도 상자 — 접혀 있다. 눌러야 펴진다 */
.uc-rep details.sa { margin:2px 0 16px; padding:0; border:1px solid var(--line);
  border-radius:8px; background:var(--surface); }
.uc-rep details.sa > summary { cursor:pointer; padding:9px 12px; font-size:.8rem;
  font-weight:800; color:var(--ink-2); list-style:none; }
.uc-rep details.sa > summary::-webkit-details-marker { display:none; }
.uc-rep details.sa > summary::before { content:"▸ "; color:var(--ink-3); }
.uc-rep details.sa[open] > summary::before { content:"▾ "; }
.uc-rep details.sa > summary span { font-weight:400; color:var(--ink-3); font-size:.74rem; }
.uc-rep details.sa ul { margin:0; padding:0; list-style:none; }
.uc-rep ul.sa-t { padding:2px 12px 10px; }
.uc-rep ul.sa-t > li { position:relative; padding:0 0 9px 15px;
  border-left:2px solid var(--line); }
.uc-rep ul.sa-t > li:last-child { border-left-color:transparent; }
.uc-rep ul.sa-t > li::before { content:""; position:absolute; left:-2px; top:.62em;
  width:11px; height:2px; background:var(--line); }
.uc-rep .sa-n { display:block; font-size:.82rem; font-weight:800; line-height:1.5;
  color:var(--ink-3); }
.uc-rep li.sa-on > .sa-n { color:var(--ink); }
.uc-rep ul.sa-t > li > ul { margin:3px 0 0 4px; }
.uc-rep ul.sa-t > li > ul > li { position:relative; padding:2px 0 2px 13px; }
.uc-rep ul.sa-t > li > ul > li::before { content:"└"; position:absolute; left:0; top:1px;
  font-size:.7rem; color:var(--ink-3); opacity:.6; }
.uc-rep .sa-q { font-size:.76rem; font-weight:700; color:var(--ink-2); }
.uc-rep .sa-f { display:inline-block; margin-left:6px; padding:0 5px; border:1px solid
  var(--line); border-radius:3px; font-size:.62rem; font-weight:700; line-height:1.7;
  color:var(--ink-3); vertical-align:1px; }
.uc-rep ul.sa-t > li > ul > li > ul { margin:2px 0 0; }
.uc-rep ul.sa-t > li > ul > li > ul > li { display:flex; gap:8px; align-items:baseline;
  font-size:.72rem; line-height:1.65; }
.uc-rep .sa-x { flex:0 0 6.4em; font-weight:700; color:var(--ink-3); opacity:.85; }
.uc-rep .sa-v { flex:1; color:var(--ink-3); }
.uc-rep .sa-note { margin:0; padding:0 12px 10px; font-size:.72rem; color:var(--ink-3); }
@media (max-width:520px) {
  .uc-rep ul.sa-t > li > ul > li > ul > li { display:block; }
  .uc-rep .sa-x { margin-right:6px; }
}
'''

HEADER = '''<h1>🎙️ Semi Doped</h1>
<p class="lede">daily.semidoped.com 전사본을 카드로 옮긴다. 원문은 전부 무료라
잠그지 않는다. 카드 한 장이 원문 한 편이고, 각도 상자를 열면 그 편이 어떤 마디로
뽑혔는지와 그중 무엇을 절로 세웠는지가 함께 보인다.</p>'''

FOOTER = ('<p>생성물이다. 고칠 것은 <code>scratchpad/gen_semidoped_dashboard.py</code> 다. '
          '원문은 <a href="https://daily.semidoped.com">daily.semidoped.com</a>.</p>')


def main():
    dc.check_links(CARDS)
    dc.check_labels(CARDS)
    dc.render(CARDS, 'Semi Doped 대시보드', HEADER, FOOTER, OUT,
              extra_css=figs.FIG_CSS + CSS, newest_first=True)


if __name__ == '__main__':
    main()
