# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — daily.semidoped.com 전사본을 카드로 낸다.

백지에서 다시 짓는 판이다. 앞선 판은 카드를 스물일곱 장 먼저 깔고 구조를 나중에
얹었다. 그래서 각도 상자·목차·축이 카드마다 다른 때에 다른 꼴로 붙었고, 고칠 때마다
스물일곱 장을 한꺼번에 건드려야 했다. 이번에는 **한 장을 끝까지 세워 보이고 그것을
본 뒤에 나머지로 옮긴다.**

카드 한 장의 뼈대:

    앞머리      물음 하나 · 바탕(무슨 재료 몇 편) · 축(묶음 둘셋)
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



JAL = {
    'id': 'sd-jalapeno',
    'section': ('sd-infer', '01', '추론 하드웨어',
                '칩 하나가 무엇을 기준으로 설계됐나'),
    'title': '오픈AI 할라페뇨 — 모델을 파는 회사가 칩을 만들면 기준이 어디로 가나',
    'gain': ('모델을 파는 회사가 칩을 만들자 잣대가 총소유비용에서 사용자가 겪는 시간과 '
             '전기로 옮겼다는 것. 그 잣대가 메모리·연산·연결에서 각각 어떤 설계를 낳았는지, '
             '그래서 무엇이 나왔고 무엇을 아직 못 믿는지.'),
    'meta': ['Austin · Vik Sekar <b>Semi Doped 공동 진행</b>',
             '업로드 2026-08-27', '게스트 없음', '발표 12시간 뒤 녹음'],
    'links': [('요약본', blob(SRC + '2026-08-27-openai-jalapeno.md'), ''),
              ('원문(Semi Doped)',
               'https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling',
               'ghost')],
    # 한줄 코멘트는 결론만. 접힌 카드에서 먼저 보이는 자리라 여기 있어야 하는 것은
    # 이 편을 읽고 남는 한 문장이다. 물음·바탕·축은 펼친 뒤 맨 위 앞머리 상자로 간다
    'verdict': ('모델을 파는 회사가 칩을 만들자 설계 잣대가 데이터센터 운영자가 치르는 '
                '돈에서 사용자가 겪는 시간과 전기로 옮겼고, 메모리·연산·연결 설계가 '
                '전부 그 잣대에서 나왔다.'),
    'report': [
        ('lead', [
            ('물음', '모델을 파는 회사가 칩을 만들면 설계 잣대가 어디로 옮겨 가나'),
            ('바탕', 'Semi Doped 2026-08-27 한 편. 오픈AI 가 Hot Chips 에서 할라페뇨를 '
                     '발표한 지 열두 시간이 안 돼 녹음한 전사본이고, 진행자 둘이 슬라이드를 '
                     '순서대로 읽는다'),
            ('축', '잣대가 바뀌었다 → 그래서 이렇게 지었다 → 그래서 이만큼 나왔다 → '
                   '그런데 이건 못 믿는다. 인과 사슬로 나눴다'),
        ]),
        # 뿌리를 인과 사슬로 가른다 — 잣대가 바뀌었다, 그래서 이렇게 지었다, 그래서
        # 이만큼 나왔다, 그런데 이건 못 믿는다. 노드마다 방법은 하나다
        ('toc', ('인과 사슬', [
            ('바뀐 평가지표', '대비', [
                ('①', '전 → 후', '총소유비용에서 무엇으로 바뀌었나')]),
            ('지은 설계', '부분 나눔', [
                ('①', '메모리', '대역폭을 깔고도 왜 못 쓰나'),
                ('②', '연산', '왜 한 칩에 몰았나'),
                ('③', '연결', '칩을 어떻게 묶었나')]),
            ('낸 결과', '부분 나눔', [
                ('①', '성능', '얼마나 나왔나'),
                ('②', '속도', '9개월이 어떻게 나왔나')]),
            ('못 믿을 것', '부분 나눔', [('①', '', '이 편이 밝히지 않은 것')]),
        ])),

        ('h', '<span class="h-node">바뀐 평가지표</span> ① 총소유비용에서 무엇으로 바뀌었나'),
        ('fig', ('잣대가 무엇에서 무엇으로 바뀌었나', figs.CRITERIA,
                 '왼쪽은 칩을 사서 굴리는 회사가 치르는 돈이고 오른쪽은 사람이 앉아서 겪는 '
                 '것이다. 오픈AI 는 오른쪽 둘을 골랐고, 두 값이 서로 밀어내므로 곡선으로 '
                 '낸다.')),
        ('p', '<b>전.</b> 칩을 파는 회사가 평가지표를 정했다. 엔비디아·AMD 는 총소유비용부터 '
              '본다. 칩을 사서 몇 년 굴리는 데 드는 돈이고, 그 돈을 치르는 것은 챗을 쓰는 '
              '사람이 아니라 데이터센터를 운영하는 회사다.'),
        ('fig', ('두 잣대를 같이 낮출 수 없다', figs.PARETO,
                 '지연을 줄이려면 전기를 더 쓰고, 전기를 아끼면 지연이 늘어난다. 그래서 '
                 '오픈AI 는 수치 하나를 안 내고 곡선으로 낸다. 축에 눈금이 없는 것은 '
                 '원문에 점도 눈금도 없기 때문이다 — 자리는 값이 아니고 모양만 뜻이 있다.')),
        ('p', '<b>후.</b> 오픈AI 는 지표 둘을 앞세웠다. ① <b>엔드투엔드 지연</b> — 질문을 '
              '넣고 마지막 글자가 나올 때까지 걸리는 시간 ② <b>요청당 전기에너지</b> — 한 번 '
              '답하는 데 쓰는 전기. 둘 다 사람이 앉아서 겪는 것이다. 오픈AI 는 모델을 팔아 '
              '돈을 벌므로 사용자가 기다리는 시간이 곧 제 매출이 걸린 값이 된다.'),
        ('p', '두 값은 같이 낮출 수 없다. 빨리 내려면 전기를 더 쓰고, 아끼려면 느려진다. '
              '그래서 수치 하나를 내지 않고 <b>파레토 곡선</b>(어느 한쪽을 포기하지 않고는 더 '
              '나아질 수 없는 지점들을 이은 선)으로만 보이겠다고 했다. 진행자들은 이 대목을 '
              '이 발표에서 가장 특이한 자리로 짚는다.'),
        ('p', '아래 절 셋은 그 잣대가 실리콘에서 어떻게 박혔는지다. 메모리·연산·연결이 각각 '
              '다른 답을 내놓는데, 세 답이 전부 사람이 기다리는 시간을 줄이는 쪽으로 간다.'),

        ('h', '<span class="h-node">지은 설계</span> ① 대역폭을 깔고도 왜 못 쓰나'),
        ('fig', ('메모리를 같이 쓸 때와 조각내 전담시킬 때', figs.NUMA,
                 '왼쪽은 한 덩어리를 여럿이 같이 써서 차례를 기다리는 그림이고, 오른쪽은 '
                 '조각을 하나씩 맡기고 길을 따로 낸 그림이다. 대역폭 숫자는 그리지 않았다 '
                 '— 이 그림이 말하는 것은 기다림이다.')),
        ('p', '<b>있는 것.</b> HBM4 가 초당 읽어 내는 양을 칩 128개치 합치면 약 '
              '<b>1페타바이트</b>다. 진행자 셈으로 1조 파라미터 모델을 FP4(값 하나를 4비트로 '
              '줄여 담는 방식)로 담으면 약 0.5테라바이트니, 읽어 내는 속도만 보면 초당 약 '
              '<b>2,000토큰</b>이 나와야 한다.'),
        ('p', '<b>못 쓰는 이유.</b> 실제로는 거기 못 미친다. 대역폭은 <b>한꺼번에 얼마나 '
              '많이</b> 실어 나르는지를 말하지, 그 값이 <b>언제</b> 연산기 손에 닿는지는 '
              '말하지 않는다. 연산기는 곱할 숫자가 제 앞에 와 있어야 곱한다. 없으면 그 '
              '사이 논다.'),
        ('p', '오픈AI 가 짚은 것이 둘이다. ① <b>값이 늦게 온다.</b> HBM 에서 꺼낸 숫자는 연산기 바로 앞의 작은 저장소'
              '(레지스터)까지 와야 쓰인다. 그 마지막 구간이 밀리면 대역폭이 남아돌아도 '
              '연산기는 기다린다. ② <b>차례를 기다린다.</b> HBM 한 덩어리를 이웃 가속기와 '
              '같이 쓰면 남이 읽는 동안 내 요청이 뒤로 밀린다. 초당 총량은 채워도 내 값이 '
              '오는 시각은 그만큼 늦어진다.'),
        ('p', '<b>솔루션.</b> 가속기마다 HBM 을 조각내 하나씩 전담시키고 그 조각으로 가는 전용 '
              '버스를 따로 깔았다. NUMA(비균일 메모리 접근 — 멀티코어 CPU 에서 코어마다 '
              '메모리를 전담시키던 방식)를 그대로 가져온 것이다. 대역폭 숫자를 키우는 대신 '
              '기다림을 없앴다. 잣대가 지연이니 그쪽을 잡는다.'),

        ('h', '<span class="h-node">지은 설계</span> ② 연산을 왜 한 칩에 몰았나'),
        ('p', '추론은 단계가 둘이다. ① <b>프리필</b>은 질문을 한꺼번에 읽는다 '
              '② <b>디코드</b>는 토큰을 하나씩 내놓는다. 단계마다 필요한 것이 달라서, GPU '
              '에서는 둘을 서로 다른 칩에 맡기는 방법이 있고 그 편이 유리해 보인다.'),
        ('p', '무슨 비율인지부터 말한다. 요청 하나를 처리하는 데 드는 일 가운데 <b>프리필이 '
              '가져가는 몫과 디코드가 가져가는 몫</b>이다. 질문이 길고 답이 짧으면 프리필 '
              '쪽이 크고, 질문이 짧고 답이 길면 디코드 쪽이 크다. 문서 한 장을 넣고 한 줄로 '
              '요약시키면 프리필이 여덟에 디코드가 둘쯤 되고, 한 줄 물어 긴 글을 받으면 '
              '둘에 여덟으로 뒤집힌다 — <b>비율은 예시이고 원문에 없다</b>. 요청마다 다르고, '
              '초안·검증'
              '(작은 모델이 토큰 여러 개를 미리 내고 큰 모델이 맞는 것만 고르는 방식)까지 '
              '섞이면 더 흔들린다.'),
        ('p', '갈림은 여기다. <b>그 몫이 늘 같으면</b> 전담 칩이 낫다. 프리필 칩과 디코드 '
              '칩을 그 비율대로 사 두면 된다. <b>몫이 요청마다 달라지면</b> 한쪽 칩이 논다. '
              '실제가 뒤쪽이다.'),
        ('p', '그래서 칩 하나에 둘 다 넣고 어느 쪽에도 치우치지 않게 맞췄다. 그 순간 안 쓰는 '
              '회로는 전원을 끊는다. 슬라이드 문구가 그 셈을 그대로 말한다 — '
              '<b>dark silicon is cheaper than idle accelerators</b>. 노는 회로가 노는 '
              '가속기보다 싸다는 판단인데, 이것도 요청당 전기에너지를 잣대로 놓아야 나온다. '
              '총소유비용으로 보면 안 쓰는 회로를 실리콘에 남기는 것이 낭비다.'),

        ('h', '<span class="h-node">지은 설계</span> ③ 칩을 어떻게 묶었나'),
        ('fig', ('칩을 묶는 두 단계', figs.DOMAIN,
                 '선 굵기가 속도다 — 안쪽이 바깥의 세 배다(600 ÷ 200). 칩을 셋만 그리고 '
                 '말줄임을 둔 것은 개수가 뜻이 되지 않게 하려는 것이다. 칩 128개가 한 랙이면 '
                 '2,048개는 약 열여섯 랙인데, 그 랙 수는 발표에 없고 진행자가 두 수를 나눠 '
                 '본 값이다.')),
        ('p', '칩을 묶는 단위가 두 단계다. <b>작은 묶음</b>은 칩 128개이고 그 안에서 칩 '
              '하나가 초당 600기가비트로 붙는다. <b>큰 묶음</b>은 작은 묶음을 여럿 모은 것으로 '
              '칩이 최대 2,048개까지 가고, 이 바깥 구간에서는 칩 하나가 초당 200기가비트로 '
              '붙는다. 안쪽을 세 배 빠르게 두고 바깥을 넓게 가져가는 배치다.'),
        ('p', '붙이는 장치는 브로드컴 Tomahawk 6 스위치이고, 칩끼리 말을 맞추는 규약은 '
              'ESUN(브로드컴이 미는 스케일업 연결 규격)이다. AMD 쪽 UALink 와는 다른 진영이다. '
              '칩 128개가 한 랙이면 2,048개는 약 열여섯 랙인데, 이 랙 수는 발표에 없고 '
              '진행자가 두 수를 나눠 본 값이다.'),

        ('h', '<span class="h-node">낸 결과</span> ① 성능이 얼마나 나왔나'),
        ('p', '잰 도구는 SemiAnalysis 의 <b>Inference X</b>다. 전력을 정규화해 공개 비교했고, '
              '작은 모델부터 큰 모델까지 여러 오픈 모델을 돌린다. 칩 하나의 최고 수치가 아니라 '
              '시스템 전체가 사용자에게 어떤 속도를 주는지를 보려는 것이라, 잣대를 고른 방식과 '
              '재는 방식이 같은 쪽을 본다.'),
        ('p', '재는 값이 둘이다. ① <b>처리량</b>은 그 시스템이 초당 몇 토큰을 내놓는지다 '
              '② <b>응답성</b>은 사용자 한 사람이 초당 몇 토큰을 받는지다. 여럿을 한꺼번에 '
              '받으면 처리량은 오르지만 한 사람이 체감하는 속도는 떨어진다. 둘을 같이 '
              '올리기 어려워서 잘한 지점을 이은 선, 곧 파레토 곡선으로 낸다.'),
        ('p', '나온 것은 셋이다. ① <b>DeepSeek R1</b>(중국 딥시크가 가중치를 공개한 모델, '
              '6,710억 파라미터)에서 그 곡선을 새로 그었다. 같은 응답성에서 토큰을 더 많이 '
              '내놓고, 응답성 자체도 더 높은 데까지 간다. ② <b>GPT-OSS</b>(오픈AI 가 '
              '가중치를 공개한 모델, 1,200억 파라미터)에서 사용자당 초당 1,000토큰을 '
              '넘겼다. 진행자들은 이 구간을 통상 GPU 가 못 가는 자리로 본다. ③ 700W 로 '
              '돌았다. 견준 GB200 은 약 1,200W 다.'),
        ('tbl', ('할라페뇨와 견준 상대',
                 ['무엇을 견줬나', '할라페뇨', '견준 상대', '언제 것 · 성격'],
                 [['DeepSeek R1 6,710억', '파레토 곡선을 새로 그었다',
                   '그전 곡선 — 값은 안 나왔다', '2026-08 · 발표 슬라이드'],
                  ['GPT-OSS 1,200억', '사용자당 초당 1,000토큰 이상',
                   '통상 GPU 는 이 구간에 못 간다', '2026-08 · 발표 슬라이드와 진행자 판단'],
                  ['전력', '700W', 'GB200 약 1,200W', '2026-08 · 상대 값은 진행자 어림'],
                  ['메모리 세대', 'HBM4', '블랙웰·MI355 는 HBM3E',
                   '2026-08 · 진행자가 짚은 불공평'],
                  ['입출력 길이', '8K 넣고 1K 받기', '같은 조건',
                   '2026-08 · 이 밖은 안 쟀다']])),

        ('h', '<span class="h-node">낸 결과</span> ② 9개월이 어떻게 나왔나'),
        ('p', '첫 RTL(회로를 글로 적은 설계) 작성부터 테이프아웃(설계를 공장에 넘기는 것)까지 '
              '<b>9개월</b>이다. 통상 2~3년 걸리는 일이라 진행자들이 여러 번 되돌아온다.'),
        ('p', '초기 RTL 을 GPT-3급 모델로 짰고 모델이 좋아지면서 더 나은 것으로 바꿨다는 것이 '
              '진행자 전언이다. 회사의 첫 칩은 보통 버리는 셈 치는데 오픈AI 는 1호부터 '
              '완성도가 높았다고 본다. 다만 이 9개월을 뒷받침하는 것은 발표 슬라이드 한 줄과 '
              '진행자의 전언뿐이다.'),

        ('h', '<span class="h-node">못 믿을 것</span> ① 이 편이 밝히지 않은 것'),
        ('p', '못 잰 범위가 셋이다. ① 벤치마크의 입출력이 8K·1K 로 짧아 100만 토큰급 긴 '
              '문맥에서 어떤지는 아직 안 나왔다 ② agentic 워크로드는 테스트하지 않아 별도 '
              'AgentX 로 재겠다고 했다 ③ 견준 상대의 세대가 다르다. 할라페뇨는 HBM4 를 쓰고 '
              '블랙웰·MI355 는 HBM3E 다. 진행자들이 스스로 Vera Rubin·Helios 와 견줘야 '
              '공평하다고 말한다.'),
        ('p', '스펙 상당수는 진행자 추측이다. CPU 가 x86 계열 Turin 급인지, 공정이 TSMC N3 '
              '변형인지, HBM 이 삼성 것인지는 오픈AI 가 확인한 것이 아니다. 삼성 HBM4 가 '
              'SK하이닉스보다 핀당 빠를 수 있다는 대목은 진행자 본인이 전적으로 추측이라고 '
              '못박았다. 셀레스티카가 시스템 설계 파트너라는 것도 추정이고, 테이프아웃과 초기 '
              '양산에 약 1억 달러가 든다는 말과 랙 열여섯도 확정치가 아닌 어림이다.'),
        ('p', '이 카드가 절로 세우지 않은 마디도 남는다. 발표자 셋이 누구인지, 무엇을 뺄지가 '
              '가장 어려운 결정이었다는 설계 태도, 남의 모델까지 돌려 보인 이유, 다음 세대 '
              '로드맵. 잣대가 옮긴 이야기의 사슬 밖이라 뺐다.'),
    ],
}

CARDS = [JAL]

CSS = '''
/* 한줄 코멘트가 머리다. 그 아래를 한 칸 들여써서 나머지가 그 머리에 딸린 것으로
   보이게 한다 — 나란히 서면 코멘트가 여러 문단 중 하나로 읽힌다 */
.uc-body > .uc-verdict { margin-bottom:12px; }
/* 딱지 뒤에서 줄을 바꾼다 — 딱지와 글이 한 문장처럼 붙어 읽히지 않게 */
.uc-body > .uc-verdict > b:first-child { display:block; margin-bottom:5px;
  font-size:.74rem; color:var(--ink-3); letter-spacing:.02em; }
.uc-body > .uc-rep { margin-left:14px; padding-left:14px;
  border-left:2px solid var(--line); }
@media (max-width:520px) {
  .uc-body > .uc-rep { margin-left:6px; padding-left:10px; }
}
/* 앞머리 — 물음·바탕·축. 글을 여는 자리라 목차보다 먼저 선다 */
.uc-rep .uc-lead { margin:0 0 14px; padding:0 0 12px;
  border-bottom:1px solid var(--line); }
.uc-rep .uc-lead > div { display:flex; gap:10px; align-items:baseline; padding:2px 0; }
.uc-rep .uc-lead .ld-k { flex:0 0 3.2em; font-size:.74rem; font-weight:800;
  color:var(--ink-3); letter-spacing:.02em; }
.uc-rep .uc-lead .ld-v { flex:1; font-size:.86rem; line-height:1.6; color:var(--ink-2); }
@media (max-width:520px) {
  .uc-rep .uc-lead > div { display:block; }
  .uc-rep .uc-lead .ld-k { margin-bottom:2px; }
}
/* 절 제목 앞의 노드 이름 — 번호가 노드마다 다시 시작하므로 어느 노드의 몇째인지를
   제목이 스스로 말해야 한다 */
.uc-rep h3 .h-node { display:block; font-size:.72rem; font-weight:700; line-height:1.6;
  color:var(--ink-3); opacity:.8; letter-spacing:.02em; }
/* 목차 — 번호가 ①②③ 이라 불릿을 쓰지 않는다. 마커가 둘이면 어느 쪽이 항목인지
   흐려지고, 들여쓰기만 두 번 먹는다. 줄 간격도 본문만큼 벌리지 않는다 —
   목차는 읽는 글이 아니라 한눈에 훑는 표다 */
.uc-rep .uc-toc { margin:2px 0 18px; padding:10px 12px; border:1px solid var(--line);
  border-radius:8px; background:var(--surface); }
.uc-rep .uc-toc .uc-label { margin:0 0 7px; }
.uc-rep .uc-toc .tg { display:flex; gap:10px; align-items:baseline; padding:3px 0; }
.uc-rep .uc-toc .tg-k { flex:0 0 4.6em; font-size:.82rem; font-weight:800;
  line-height:1.5; color:var(--ink); }
.uc-rep .uc-toc .tg-f { flex:0 0 4.6em; font-size:.7rem; font-weight:700;
  line-height:1.75; color:var(--ink-3); opacity:.72; }
.uc-rep .uc-toc ul { flex:1; margin:0; padding:0; list-style:none; }
.uc-rep .uc-toc li { font-size:.84rem; line-height:1.5; color:var(--ink-2);
  padding:1px 0; }
.uc-rep .uc-toc li b { color:var(--ink); font-weight:700; margin-right:4px; }
@media (max-width:520px) {
  .uc-rep .uc-toc .tg { display:block; }
  .uc-rep .uc-toc .tg-f { display:inline-block; margin-left:6px; }
}
/* 목차 안의 축 — 절이 셋을 넘는 마디는 그 안에서 한 번 더 갈린다 */
.uc-rep .uc-toc li.tg-ax { padding:1px 0 2px; }
.uc-rep .uc-toc li.tg-ax > span { display:block; font-size:.72rem;
  font-weight:700; color:var(--ink-3); opacity:.85; }
.uc-rep .uc-toc li.tg-ax > ul { margin:0 0 0 10px; }
.uc-rep .uc-toc .tg-a { font-size:.74rem; font-weight:700; color:var(--ink-3);
  opacity:.85; }
/* 목차 맨 위 사슬 — 목표 → 시도 → 성과 → 한계 */
.uc-rep .uc-toc .tg-chain { margin:0 0 8px; padding:0 0 7px;
  border-bottom:1px solid var(--line); font-size:.78rem; line-height:1.6; }
.uc-rep .uc-toc .tg-chain b { font-weight:800; color:var(--ink); }
.uc-rep .uc-toc .tg-chain i { font-style:normal; color:var(--ink-3); padding:0 1px; }
'''

HEADER = '''<h1>🎙️ Semi Doped</h1>
<p class="lede">daily.semidoped.com 전사본을 카드로 옮긴다. 원문은 전부 무료라
잠그지 않는다. 카드 한 장이 원문 한 편이고, 목차가 그 편을 무슨 방법으로 나눴는지를
먼저 보인다.</p>'''

FOOTER = ('<p>생성물이다. 고칠 것은 <code>scratchpad/gen_semidoped_dashboard.py</code> 다. '
          '원문은 <a href="https://daily.semidoped.com">daily.semidoped.com</a>.</p>')


def main():
    dc.check_links(CARDS)
    dc.check_labels(CARDS)
    dc.render(CARDS, 'Semi Doped 대시보드', HEADER, FOOTER, OUT,
              extra_css=figs.FIG_CSS + CSS, newest_first=True)


if __name__ == '__main__':
    main()
