# -*- coding: utf-8 -*-
"""통합 보고서의 숫자가 원문에 있나 — 대시보드 산문용 대조기.

check_cite 는 insights/ 아래 글만 본다. 통합 보고서는 카드에서 뽑아 쓴 숫자가
문단에 흩어져 있어서 그 대조가 비어 있었다. 여기서 본문 글자에 든 수를 전부 뽑아
바탕이 되는 원문(content/understanding/피지컬AI/*.md)에 그 수가 있는지 센다.

  PYTHONIOENCODING=utf-8 python insights/check_report.py

숫자 하나가 여러 꼴로 적히므로(1천만·10밀리언·1,000만) 정규화해서 견준다.
못 찾은 값은 FAIL 이 아니라 **확인 필요**로 낸다 — 원문이 「열흘」처럼 한글로만
적어 둔 경우가 있어 사람이 봐야 갈린다.
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (페이지, 층 id, 재료 폴더) — 한 페이지에 성격이 다른 리포트 층이 여럿이면 층마다 재료가 다르다.
PAGES = [
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-report',
     os.path.join(ROOT, 'content', 'understanding', '피지컬AI')),
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-biz',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 알파벳 밸류에이션 층. 재료가 둘이다 — 산업 판단은 뉴스레터에서 오고 재무 숫자는
    # SEC 제출서류에서 온다. 후자는 JSON 이라 이 검사기가 못 읽으므로 googl_facts.md 로
    # 떨어뜨려 EXTRA 에 넣는다. 그 파일은 scratchpad/googl_cases.py 가 다시 쓴다.
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-val',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 모델 회사·칩 회사 정성 비교. 재무제표가 없는 회사가 대부분이라 값이 전부
    # 뉴스레터에서 온다.
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-ai',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 자금조달 층. 재료가 각도 파일이지만 각도의 값은 전부 뉴스레터 네 편에서 온 것이라
    # 대조 대상은 같다 — 각도를 거쳐 온 값이 원문에 없으면 각도가 틀린 것이다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-fund',
     os.path.join(ROOT, 'content', 'newsletter')),
    # CPO 층(2026-09-04). 재료가 뉴스레터 아홉 편 + Semi Doped 다섯 회차 + 영문 클리핑 넷 +
    # 링크드인 셋이다. 뉴스레터 밖의 것은 파일로 EXTRA 에 올린다 — 폴더째 넣으면 이 층과 무관한
    # 회차의 값이 다른 층의 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-cpo',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 선단 패키징 층(2026-09-05). 재료가 뉴스레터 아홉 편 + Semi Doped 한 회차 + 영문 클리핑 둘이다.
    # 뉴스레터 밖의 셋만 파일로 EXTRA 에 올린다 — 폴더째 넣으면 이 층과 무관한 회차의 값이
    # 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-pkg',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 금리·물가 층(2026-09-05). 재료가 회계사·미국주식 사관학교·류상철·김상훈·박소연에
    # 흩어져 있어 공통 폴더가 content/understanding 인데 그것을 통째로 넣으면 540편이
    # 알리바이가 된다. 그래서 폴더 없이 RATE_EXTRA 에 파일을 하나씩 적는다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-rate', None),
    # 메모리 층(2026-09-06). 뉴스레터 다섯 편은 폴더에서 오고, 링크드인 석 달치와 메르 다섯 편,
    # 미국주식 사관학교 여섯 편은 MEM_EXTRA 에 파일로 하나씩 적는다 — understanding 을 통째로
    # 넣으면 이 층과 무관한 편의 값이 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-mem',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 트럼프 층(2026-09-06). 재료가 메르 클리핑 마흔일곱 편뿐이라 폴더 없이 TRUMP_EXTRA 로 간다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-trump', None),
    # 하네스·스킬 층(2026-09-08). 재료가 AI Engineer 발표 열여섯 편 + 뉴스레터 두 편이다.
    # content/understanding 을 통째로 넣으면 이 층과 무관한 오백 편이 알리바이가 되므로
    # 폴더 없이 HARNESS_EXTRA 에 파일을 하나씩 적는다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-harness', None),
    # 전력 층(2026-09-07). 재료가 뉴스레터 열두 편 + 팟캐스트 한 회차 + 전략 판 한 회차다.
    # 뉴스레터는 폴더에서 오고 나머지 둘만 POWER_EXTRA 에 파일로 적는다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-power',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 순환금융 층(2026-09-09). 재료가 뉴스레터 열두 편 + 메르 클리핑 여섯 편이다.
    # 뉴스레터는 폴더에서 오고 메르는 CIRC_EXTRA 에 파일로 하나씩 적는다 — mer 폴더를
    # 통째로 넣으면 이 층과 무관한 편이 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '통합 보고서.html'), 'sec-circ',
     os.path.join(ROOT, 'content', 'newsletter')),
    # 모델 층(2026-09-09). 재료가 영문 클리핑 둘 + 그 안의 표 그림 일곱 + 한국어 변환본 하나다.
    # 표 그림의 값은 픽셀이라 클리핑 마크다운에 없다 — 읽은 값을 model_facts.md 에 남겨
    # 그 파일이 출처가 된다(googl_facts·peers_facts 와 같은 자리). 모델이 낸 파생값도 같다.
    # 폴더를 안 넣는다 — 뉴스레터 전체를 넣으면 이 층과 무관한 편이 알리바이가 된다
    (os.path.join(ROOT, '대시보드', '모델링 대시보드.html'), 'sec-cost', None),
    (os.path.join(ROOT, '대시보드', '모델링 대시보드.html'), 'sec-phys', None),
    (os.path.join(ROOT, '대시보드', '모델링 대시보드.html'), 'sec-dc', None),
    (os.path.join(ROOT, '대시보드', '모델링 대시보드.html'), 'sec-fin', None),
    (os.path.join(ROOT, '대시보드', '모델링 대시보드.html'), 'sec-meet', None),
]

_SD = os.path.join(ROOT, 'content', 'semi_doped')
_CLIP = os.path.join(ROOT, 'input', 'clippings')
_LI = os.path.join(ROOT, 'content', 'linkedin')
CPO_EXTRA = [os.path.join(_SD, f + '.md') for f in
             ('2026-06-12-computex-optics-power', '2026-07-16-picojool-yuen',
              '2026-07-25-datacenter-interconnects', '2026-08-07-globalfoundries-barber',
              '2026-08-11-china-optical-ban')] + [
    os.path.join(_CLIP, 'NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, '
                 'Jensen Math, Feynman.md'),
    os.path.join(_CLIP, 'Tariff Armageddon  GPU Loopholes, Mexico Supply Chain Shift, Wafer Fab Equipment '
                 'Vulnerabilities, Optical Module Pricing Surge, Datacenter Equipment.md'),
] + glob.glob(os.path.join(_CLIP, 'Huawei AI CloudMatrix 384*.md')) + glob.glob(
    os.path.join(_CLIP, 'Co-Packaged Optics (CPO) Book*.md')) + [
    os.path.join(_LI, '[2605] 링크드인 게시물.md'), os.path.join(_LI, '[2607] 링크드인 게시물.md'),
    os.path.join(_LI, '[2608] 링크드인 게시물.md'), os.path.join(_LI, '[2609] 링크드인 게시물.md')]

# 선단 패키징 층의 뉴스레터 밖 재료 셋
PKG_EXTRA = [os.path.join(ROOT, 'insights', 'semidoped', '2026-06-19-advanced-packaging-strategy.md'),
             os.path.join(_CLIP, 'EMIB-T Roadmap, Custom HBM, HBM4 Packaging Challenges, '
                          'Microfluidic Cooling, Photonic Interconnects, and More.md'),
             os.path.join(_CLIP, 'CPUs are Back The Datacenter CPU Landscape in 2026.md')]

# 금리·물가 층의 재료 마흔. 폴더째 넣지 않고 파일을 하나씩 적는다 — content/understanding 은
# 540편이라 통째로 넣으면 이 층과 무관한 편이 알리바이가 된다. EXTRA 는 확장자를 안 가려
# 읽으므로 메르 클리핑과 사슬(json)도 그대로 대조 대상이 된다
RATE_EXTRA = [os.path.join(ROOT, *p.split('/')) for p in (
    'input/clippings/mer/223873166379.json',
    'input/clippings/mer/223887755561.json',
    'input/clippings/mer/223931247450.json',
    'input/clippings/mer/223954627912.json',
    'input/clippings/mer/224032232941.json',
    'input/clippings/mer/224031770885.json',
    'input/clippings/mer/224095422334.json',
    'input/clippings/mer/224100335488.json',
    'input/clippings/mer/224153982515.json',
    'input/clippings/mer/224167473277.json',
    'input/clippings/mer/224179162516.json',
    'input/clippings/mer/224260820330.json',
    'input/clippings/mer/224292480472.json',
    'input/clippings/mer/224292701545.json',
    'input/clippings/mer/224356110315.json',
    'input/clippings/mer/224366267736.json',
    'input/clippings/mer/224369325535.json',
    'input/clippings/mer/224376966792.json',
    'input/clippings/mer/224380392566.json',
    'input/clippings/mer/224381241715.json',
    'input/clippings/mer/224381744094.json',
    'input/clippings/mer/224382901516.json',
    'input/clippings/mer/224384006179.json',
    'input/clippings/mer/224392077639.json',
    'content/understanding/류상철 국장/경제 교과서 틀렸다 - 물가 때문에 금리 인상해도 주가 오른다.md',
    'content/understanding/언더스탠딩 보고서/2026-08-24-물가-신호를-무시하면-10년이-녹는다.md',
    'content/understanding/미국주식 사관학교/[260115] 기준금리는 내렸는데 10년물은 그대로다 - 물타기는 TLT가 아니라 단기채로.md',
    'content/understanding/미국주식 사관학교/[260318] 인하 논쟁 - 물가가 안 죽었다 대 안 내리면 경기가 먼저 깨진다.md',
    'content/understanding/미국주식 사관학교/[260424] 채권이 주식을 지켜주던 20년은 예외였다 - 갈림길은 물가 3%.md',
    'content/understanding/미국주식 사관학교/[260608] 인상 소나기를 정통으로 맞는 건 중기채다 - 충격이 꽂히는 자리와 가격 반응은 다르다.md',
    'content/understanding/미국주식 사관학교/[260823] 국채가 밀리는 동안 지방채는 물량이 안 늘었다 - 고금리 뉴노멀에서 남는 채권 셋.md',
    'content/understanding/미국주식 사관학교/[260830] 워시는 파월과 다르다, 물가 2%가 찍혀야 움직인다 - 잭슨홀 조정을 저가매수 신호로 읽으면 안 되는 이유.md',
    'content/understanding/회계사/[260802] 채권 자경단, 동결 속에서 30년물 금리를 5.27%로 밀어올리다 - 엘곰.md',
    'content/understanding/회계사/[260819] 30년물이 19년 만의 고점을 찍은 이유 - 엘곰.md',
    'content/understanding/미국주식 사관학교/[260821] 재무부가 바이백을 두 배로 늘렸는데 하루 만에 되돌아왔다 - 30년물 금리와 매수자 교체.md',
    'content/understanding/김상훈 기자/[260806] 엔화를 지켜준 게 아니라 국채를 못 팔게 했다 - 미일 공동개입의 진짜 청구서 - 김상훈.md',
    'content/understanding/박소연 이사/[260806] 금리 방향이 바뀔 때마다 잘하던 방식이 먼저 무너졌다 - 철도채에서 LTCM까지 - 박소연.md',
    'insights/flows/mer/rate_cpi.json',
    'insights/flows/mer/rate_0818.json',
    'insights/debate/issue-2026-08-28-금리와-AI설비투자-무엇이-앞에-서나.md',
    # FRED 시계열 — 도해의 선이 이 값이다. 받은 그대로 두고 가공하지 않는다
    'data/fred/DGS10.csv',
    'data/fred/DGS30.csv',
    'data/fred/T10Y2Y.csv',
    'data/fred/DFF.csv',
    'content/understanding/회계사/[260724] 브렌트유 하루 7% 급등 100달러, 10년물 금리 4.71%로 2025년 1월來 최고 - 엘곰.md',
    'content/understanding/회계사/[260801] 美 10년물 4.71%, 실적이 가려온 금리 압박이 드러났다 - 엘곰.md',
    'content/understanding/회계사/[260818] 30년물 금리 5.31%로 19년來 최고, 브렌트유는 2주 만에 91달러 - 엘곰.md',
    'content/understanding/회계사/[260822] 바이백을 두 배로 늘렸지만 효과는 하루였다, 30년물은 5.28%로 되돌아왔다 - 미국 국채 - 엘곰.md',
)]

MEM_EXTRA = [os.path.join(ROOT, *p.split('/')) for p in (
    'content/linkedin/[2607] 링크드인 게시물.md',
    'content/linkedin/[2608] 링크드인 게시물.md',
    'content/linkedin/[2609] 링크드인 게시물.md',
    'input/clippings/mer/224372898270.json',
    'input/clippings/mer/224358943114.json',
    'input/clippings/mer/224358951791.json',
    'input/clippings/mer/224331285266.json',
    'input/clippings/mer/224399253940.json',
    'content/understanding/미국주식 사관학교/[260729] SK하이닉스 실적의 역설 - HBM 1등이라 상승분을 덜 받았다.md',
    'content/understanding/미국주식 사관학교/[260717] 가격이 논리를 만든다 - 마이크론의 「여기쯤」 선.md',
    'content/understanding/미국주식 사관학교/[260803] 엔비디아 vs AMD 메모리 치킨게임 - 누가 이겨도 HBM이 남는다.md',
    'content/understanding/미국주식 사관학교/[260826] 메타가 메모리 대란에서 혼자 웃는 이유 - 버려질 서버에서 헌 D램을 거의 공짜로 건진다.md',
    'content/understanding/미국주식 사관학교/[260816] 애플이 중국산 D램을 두드린 이유 - 이익률은 깎여도 대당 이익은 지킨다.md',
    'content/understanding/미국주식 사관학교/[260719] CXMT는 딥시크와 다르다 - 수요 충격이 아니라 공급 충격이다.md',
    "input/clippings/Korea’s Trillion-Dollar Sovereign AI Investment Nvidia Wins, Hynix Loses.md",
    'input/clippings/EMIB-T Roadmap, Custom HBM, HBM4 Packaging Challenges, Microfluidic Cooling, Photonic Interconnects, and More.md',
)]

# 회사 사실(설립·조달·밸류)은 유튜브 원문이 아니라 회사 공식 사이트에서 온다. 그 조사 파일도
# 대조 대상에 넣는다 — 여기에도 없는 값이면 어디서 왔는지 사람이 대야 한다.
# 트럼프 층(2026-09-06). 재료가 메르 클리핑 마흔일곱 편뿐인데, mer 폴더를 통째로 넣으면
# 697편이 알리바이가 된다. 금리 층과 같은 이유로 파일을 하나씩 적는다
TRUMP_EXTRA = [os.path.join(ROOT, *p.split('/')) for p in (
'input/clippings/mer/223838109591.json',
'input/clippings/mer/223936689668.json',
'input/clippings/mer/223979290690.json',
'input/clippings/mer/223984718208.json',
'input/clippings/mer/224002614977.json',
'input/clippings/mer/224037379068.json',
'input/clippings/mer/224056190379.json',
'input/clippings/mer/224058011342.json',
'input/clippings/mer/224058494349.json',
'input/clippings/mer/224057746385.json',
'input/clippings/mer/224059473094.json',
'input/clippings/mer/224070917734.json',
'input/clippings/mer/224075693844.json',
'input/clippings/mer/224076987628.json',
'input/clippings/mer/224089047026.json',
'input/clippings/mer/224096308091.json',
'input/clippings/mer/224101858436.json',
'input/clippings/mer/224101202316.json',
'input/clippings/mer/224132929462.json',
'input/clippings/mer/224133459941.json',
'input/clippings/mer/224137593241.json',
'input/clippings/mer/224138056243.json',
'input/clippings/mer/224161055072.json',
'input/clippings/mer/224161591616.json',
'input/clippings/mer/224162304086.json',
'input/clippings/mer/224166639439.json',
'input/clippings/mer/224183512547.json',
'input/clippings/mer/224187679101.json',
'input/clippings/mer/224190224535.json',
'input/clippings/mer/224191636505.json',
'input/clippings/mer/224226825696.json',
'input/clippings/mer/224231051991.json',
'input/clippings/mer/224244767604.json',
'input/clippings/mer/224260820330.json',
'input/clippings/mer/224267499277.json',
'input/clippings/mer/224285418418.json',
'input/clippings/mer/224289833145.json',
'input/clippings/mer/224293694461.json',
'input/clippings/mer/224306532703.json',
'input/clippings/mer/224313465740.json',
'input/clippings/mer/224319486464.json',
'input/clippings/mer/224322627044.json',
'input/clippings/mer/224321684736.json',
'input/clippings/mer/224345852124.json',
'input/clippings/mer/224350725486.json',
'input/clippings/mer/224356224538.json',
'input/clippings/mer/224399253940.json',
)]

# 하네스·스킬 층의 재료 열여덟 — AI Engineer 발표 열여섯 편과 뉴스레터 두 편
HARNESS_EXTRA = [os.path.join(ROOT, 'content', 'aie', f + '.md')
                 for f in (
    '2025-08-26-클로드-코드와-에이전트-코딩의-진화',
    '2025-12-26-에이전트-말고-스킬을-만들어라',
    '2025-12-26-에이전트를-위해-바뀌는-클로드-API',
    '2025-12-26-다음-모델에도-버티는-코딩-에이전트',
    '2026-04-26-코드-모드-말은-코드가-한다',
    '2026-05-26-1만2천-줄을-200줄-스킬로-바꾸기',
    '2026-05-26-개발자-한-명과-스무-개의-에이전트',
    '2026-07-26-LLM에게-운전대를-주지-마라',
    '2026-07-26-평가-없이-스킬을-내보내지-마라',
    '2026-07-26-긴-호흡의-작업을-맡길-때',
    '2026-07-26-더-똑똑한-바닥-위의-얇은-에이전트',
    '2026-07-26-코드를-쓰다가-시스템을-설계하는-일로',
    '2026-07-31-일하면서-배우는-에이전트',
    '2026-08-05-실패한-것은-에이전트가-아니라-하니스다',
    '2026-08-12-코덱스-하니스-뒤편',
    '2026-08-23-토큰을-누가-다-썼나',
)] + [
    os.path.join(ROOT, 'content', 'newsletter', 'ai_models', 'agents',
                 '[260206] Claude Code, 에이전트 시대의 변곡점.md'),
    os.path.join(ROOT, 'content', 'newsletter', 'ai_models', 'agents',
                 '[260425] 코딩 어시스턴트 해부 - 토큰을 더 주세요.md'),
]

# 전력 층의 뉴스레터 밖 재료 둘 — 팟캐스트 한 회차와 전략 판 한 회차
POWER_EXTRA = [os.path.join(ROOT, 'content', 'podcast', 'semianalysis',
                            '[260820] Ep.26 로버트 보스웰 - PJM이 요금 납부자 120억 달러를 더 쓰게 만든 모델링 오류.md'),
               os.path.join(ROOT, 'insights', 'semidoped',
                            '2026-05-08-power-wall-strategy.md')]

# 순환금융 층의 뉴스레터 밖 재료 여섯 — 메르 클리핑
CIRC_EXTRA = [os.path.join(ROOT, *p.split('/')) for p in (
    'input/clippings/mer/224088297516.json',
    'input/clippings/mer/224171369464.json',
    'input/clippings/mer/224193608780.json',
    'input/clippings/mer/224308296478.json',
    'input/clippings/mer/224359986701.json',
    'input/clippings/mer/224375780479.json',
)]

# 모델 층의 재료 셋 — 영문 클리핑 둘과 한국어 변환본 하나. 표 그림에서 읽은 값과
# 모델이 낸 값은 EXTRA 의 model_facts.md 가 맡는다
MODEL_EXTRA = [
    os.path.join(_CLIP, 'How Much Do GPU Clusters Really Cost.md'),
    os.path.join(_CLIP, 'AMD vs NVIDIA Inference Benchmark Who Wins - Performance & '
                 'Cost Per Million Tokens.md'),
    os.path.join(ROOT, 'content', 'newsletter', 'ai_infra', 'business',
                 '[260420] GPU 클러스터 진짜 비용 계산법 - 총소유비용(TCO)과 굿풋 이론.md'),
    # 토러스 층(2026-09-10)의 재료 — 표 그림 한 장이 든 영문 클리핑
    os.path.join(_CLIP, 'TPUv7 Google Takes a Swing at the King.md'),
    # 지연 층(2026-09-10)의 재료 — 대화 속도 값이 든 편
    os.path.join(_CLIP, 'InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - '
                 'Formerly InferenceMAX.md'),
    # PJM 층·루프라인 층(2026-09-10)의 재료
    os.path.join(_CLIP, "$12B of US ratepayers' money wasted on a modeling mistake and PJM wants to do it again.md"),
    os.path.join(_CLIP, 'Cerebras — Faster Tokens Please.md'),
    # 자본지출 층 넷(2026-09-10)의 재료 — 모듈러·지상 층·GPU 금융·회수기간
    os.path.join(_CLIP, 'The Wild Wild West Of LEGO Datacenters.md'),
    os.path.join(_CLIP, 'To Boldly Go The Case for Space Datacenters.md'),
    os.path.join(_CLIP, 'Nvidia GPU Debt Backstop Unleashes the AI Project Trinity '
                 'Capital, Offtake and Datacenters.md'),
    os.path.join(_CLIP, 'SpaceX 10GW in 2027 – Why It’s Real, Will Drive $300B ARR '
                 'for SpaceX, and Why Microsoft Will Be the Largest Offtaker.md'),
]

EXTRA = [os.path.join(ROOT, 'scratchpad', 'company_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'company_facts_B.md'),
         # SemiAnalysis 로봇 보고서의 재료 — 원문은 영어 클리핑이라 사실표로 대조한다
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_A.md'),
         os.path.join(ROOT, 'scratchpad', 'semi_robot_facts_B.md'),
         # 알파벳 밸류에이션의 재무 숫자와 우리 계산 결과
         os.path.join(ROOT, 'scratchpad', 'googl_facts.md'),
         # 원문 사실과 모형 입력 사이에 낀 판단 — insights/valuation/adjust.py 가 쓴다
         os.path.join(ROOT, 'scratchpad', 'adjust_facts.md'),
         # 빅테크 여섯 비교의 계산 결과
         os.path.join(ROOT, 'scratchpad', 'peers_facts.md'),
         os.path.join(ROOT, 'scratchpad', 'nvda_facts.md'),
         # 모델 층이 그림에서 읽은 발표치와 우리 모델이 낸 파생값
         os.path.join(ROOT, 'scratchpad', 'model_facts.md'),
         # 다리 층(2026-09-10)의 재료 — 밖에서 받은 하향 모델과 그 엑셀 전사
         os.path.join(ROOT, 'insights', 'frames', '2026-09-10-dc-capex-topdown.md'),
         os.path.join(ROOT, 'scratchpad', 'capex_frame_xlsx.md'),
         os.path.join(ROOT, 'scratchpad', 'capex_frame_scn.md')] + MODEL_EXTRA + CPO_EXTRA + PKG_EXTRA + RATE_EXTRA + MEM_EXTRA + TRUMP_EXTRA + HARNESS_EXTRA + POWER_EXTRA + CIRC_EXTRA

# 숫자로 읽히지만 대조할 값이 아닌 것들 — 연·월·일, 절 번호, 흔한 서수
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
        '2023', '2024', '2025', '2026', '0'}


def norm(t):
    """1,000 · 1000 · 1천 을 같은 자리에 놓기 위한 성긴 정규화."""
    return re.sub(r'[\s,]', '', t)


def corpus(d):
    """재료 글자를 한 덩어리로. d 가 None 이면 EXTRA 에 적은 파일만 본다.

    폴더를 통째로 넣으면 그 층과 무관한 편의 값이 알리바이가 된다. 재료가 여러 폴더에
    흩어진 층(금리·물가는 회계사·미주사·류상철·김상훈·박소연에 걸쳐 있다)은 폴더 대신
    파일을 하나씩 적는다. EXTRA 는 확장자를 안 가려서 json 도 글자로 읽는다.
    """
    out = []
    for base, _dirs, files in os.walk(d) if d else []:
        for f in sorted(files):
            if f.endswith('.md'):
                out.append(io.open(os.path.join(base, f), encoding='utf-8').read())
    for f in EXTRA:
        if os.path.exists(f):
            out.append(io.open(f, encoding='utf-8').read())
    return norm('\n'.join(out))


def body(html, sec):
    """그 층의 글자만 — 태그와 스크립트를 걷는다."""
    h = io.open(html, encoding='utf-8').read()
    i = h.find('id="%s"' % sec)
    if i < 0:
        return ''
    seg = h[i:h.find('</section>', i)]
    seg = re.sub(r'<script.*?</script>', ' ', seg, flags=re.S)
    # 「받은 그대로」 상자는 남의 시트를 편 자리라 우리 주장이 아니다. 엑셀이 화면에
    # 반올림해 보여 주므로 전사본의 444.875 가 여기서 444.88 로 나오는데, 그것을
    # 어긋남으로 세면 인용을 실을 수 없는 검사기가 된다(2026-09-10 모델링 부록)
    seg = re.sub(r'<div class="xls" data-quote="1">.*?</div>\s*</div>', ' ', seg,
                 flags=re.S)
    seg = re.sub(r'<[^>]+>', ' ', seg)
    # 인용 표시 (라벨 L12) 는 값이 아니다. 전력 층처럼 라벨에 날짜가 박힌 층에서는
    # 라벨의 260619 가 값으로 잡혀 전부 확인 필요로 뜬다. 괄호 안에 L숫자가 있으면
    # 인용으로 보고 걷는다 — 그 괄호에는 라벨과 줄 번호 말고 다른 값이 안 들어간다
    return re.sub(r'\([^()]*L[0-9]+[^()]*\)', ' ', seg)


def main():
    bad = 0
    for page, sec, src_dir in PAGES:
        if not os.path.exists(page):
            print('건너뜀 — 파일이 없다: %s' % page)
            continue
        text, src = body(page, sec), corpus(src_dir)
        if not text.strip():
            print('건너뜀 — 층이 아직 없다: %s' % sec)
            continue
        nums = []
        for m in re.finditer(r'\d[\d,\.]*', text):
            v = m.group(0).rstrip('.')
            if v in SKIP or len(norm(v)) < 2:
                continue
            nums.append((v, text[max(0, m.start() - 30):m.end() + 30]))
        # 한국식 단위로 옮긴 값은 원문 표기와 글자가 다르다(3억 9,700만 달러 ↔ $397M).
        # 바로 뒤에 원문 표기를 괄호로 병기했으면 출처가 붙은 것으로 본다.
        def sourced(v, c):
            if norm(v) in src:
                return True
            return bool(re.search(r'\(\$\s?[\d,\.]+\s?[MB]?\)', c))

        miss = [(v, c) for v, c in nums if not sourced(v, c)]
        name = os.path.basename(page) + ' / ' + sec
        for v, c in miss:
            print('확인 필요 %s — 원문에서 못 찾은 값 %s: …%s…'
                  % (name, v, ' '.join(c.split())))
        print('%s: 값 %d개 / 확인 필요 %d개' % (name, len(nums), len(miss)))
        bad += len(miss)
    print('요약: 확인 필요 %d건' % bad)


if __name__ == '__main__':
    main()
