---
title: HBM 을 옆에 붙이지 않고 연산 위에 쌓겠다는 설계
date: 2026-06-29
source: https://daily.semidoped.com/p/semi-doped-qualcomms-hbc-memory-alphawave
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: compute
topic: HBC · 메모리 적층 · 데이터센터 진입
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
gain: 메모리를 연산 다이 옆이 아니라 위에 쌓으면 무엇이 달라지는지(레인 수와 대역폭), 그리고 그 대가로 무엇이 어려워지는지(열·평탄도·관통전극 킵아웃존). 통신 회사가 데이터센터로 들어오는 경로와 인수 둘.
---

## 한 줄
퀄컴 인베스터 데이(뉴욕) 참관기를 다룬 회차다. 통신 중심에서 데이터센터·자동차·IoT로의 사업 다각화 목표, HBM(고대역폭 메모리, High Bandwidth Memory) 대신 로직 위에 LPDDR를 쌓는 HBC(고대역폭 컴퓨트, High Bandwidth Compute) 구조, 알파웨이브(Alphawave)·모듈러(Modular) 인수, C1000 CPU를 순서대로 짚는다.

## 사실 — 꼭지별로

### Cold Open and Catching Up
- 진행자 오스틴 라이언스(Austin Lyons, Chipstrat)와 빅 세카르(Vik Sekar, Vik's Newsletter)가 공동으로 진행한다.
- 오스틴은 퀄컴 초청으로 뉴욕에서 열린 퀄컴 인베스터 데이(Investor Day) 행사에 참석했다.
- 행사 청중은 매도측(sell-side) 애널리스트와 금융권이 중심이었고, 업계 애널리스트도 초청됐다.

### Qualcomm's Diversification Bet
- 퀄컴 CEO 크리스티아노 아몬(Cristiano Amon)이 통신(스마트폰) 중심에서 벗어나는 다각화 전략을 발표했다.
- CFO 발표에 등장한 도넛형 원 그래프(오스틴 표현)에 따르면, FY(회계연도)25 기준 스마트폰이 매출의 3분의 2, 자동차·IoT가 3분의 1이다.
- 목표는 FY27에 스마트폰과 기타(데이터센터 포함)가 각각 절반씩, FY29에는 자동차·IoT·데이터센터가 3분의 2, 스마트폰이 3분의 1이 되는 것이다.
- 퀄컴 40주년 행사에서 창업자 어윈 제이컵스(Irwin Jacobs)가 사명(Qualcomm=Quality Communications)에 M을 하나만 썼어야 했다는 농담을 했다고 빅이 전했다(그랬다면 Quality Compute가 됐을 것이라는 취지).
- 빅은 2018년 퀄컴에 입사했으며, 사내 오리엔테이션에 회사 역사 박물관 투어가 있었다고 언급했다.
- 알파웨이브 인수로 퀄컴이 확보한 IP: 구리·광 SerDes(직렬화-역직렬화), PCIe Gen 6, 서버·스토리지용 CXL, 이더넷 IP(800기가·1.6테라, 스위치·라우터·DPU·NIC용), GPU용 HBM·DRAM IP, UCIe 등 칩렛 IP.

### Disaggregated Inference
- 빅은 추론(inference) 워크로드가 프리필(prefill)과 디코드(decode)로 분리(disaggregated)되는 추세가 퀄컴 같은 후발주자에게 진입 기회를 준다고 설명했다.
- 랙 단위로 CPU 전용 랙, 저지연 디코드 전용 랙(세레브라스·그록 LPU류), 퀄컴 추론 칩 랙을 섞어 쓸 수 있다는 구상이다.
- 퀄컴의 데이터센터 브랜드명은 드래곤플라이(Dragonfly)이며, 색상은 흰색과 금색이다.

### High Bandwidth Compute
- HBC(High Bandwidth Compute)는 XPU(연산 다이) 옆에 HBM을 붙이는 대신, XPU 위에 메모리(LPDDR 계열)를 쌓아 올리는 방식이다.
- 빅에 따르면 SRAM 대역폭은 초당 약 100테라바이트(TB/s) 수준이고, 현재 HBM 대역폭은 그 10분의 1 수준인 초당 약 8테라바이트다.
- 현재 HBM-GPU 연결은 CoWoS 같은 첨단 패키징으로 옆면(shoreline)을 통해 약 2,000개 레인을 쓴다.
- 메모리를 XPU 위에 올리면 다이 전체 면을 인터커넥트로 쓸 수 있어 레인 수를 수만 개에서 최대 약 10만 개까지 늘릴 수 있고, 레인 수가 100배 늘면 대역폭도 100배 늘어난다는 것이 빅의 설명이다.
- 오스틴은 실제로 메모리가 XPU 바로 위에 붙는 게 아니라, XPU와 가까운 별도 로직 칩(사실상 가속기) 위에 메모리가 얹히고, 소프트맥스(softmax) 같은 추론 연산의 일부를 그 로직 칩으로 옮기는 구조로 이해했다고 설명했다.
- 빅은 발표 슬라이드를 보고 그 로직 다이가 단순 로직이 아니라 완전한 XPU(행렬곱 연산 담당)일 가능성이 크다고 반박했다 — 근거는 퀄컴이 "첨단 패키징이 더는 필요 없다"고 말했다는 점이다.
- 두 사람은 이 구조가 디매트릭스(d-Matrix)의 접근(디지털 인-메모리 컴퓨트, digital in-memory compute)과 유사하다고 지적했다. 디매트릭스의 랩터(Raptor) 칩은 DRAM 다이 아래에 완전한 XPU를 두는 구조다.

### The Hard Part: Thermals, Stacking, and TSV Density
- 빅은 XPU 위에 로직(메모리)을 쌓는 데 걸리는 문제로 열(thermal)을 먼저 짚었다.
- 두 번째 문제는 크기 불일치다 — 레티클 크기(reticle-sized) XPU 다이는 약 800제곱밀리미터(mm²) 이상이며, 그 위에 그만한 크기의 DRAM 다이를 쌓고 평탄도(planarity)를 유지하는 것이 어렵다.
- 오스틴은 열로 인한 변형(warp) 상태에서 다이 간 물리적 연결(범프)이 떨어지지 않게 유지해야 한다고 덧붙였다.
- 빅은 퀄컴이 "첨단 CoWoS 패키징이 필요 없다"고 말했지만 실제로는 패키징 문제를 없앤 게 아니라 다른 곳(옆이 아니라 위)으로 옮긴 것이라고 지적했다.
- 발표 슬라이드는 LPDDR 스택을 여러 층으로 그렸지만, 랩터 1세대도 실제로는 한 개 다이 층 정도일 것이라고 빅은 예상했다 — 로직 위에 메모리 한 층을 쌓는 것도 쉽지 않기 때문이다.
- HBM4(또는 HBM4E)는 이미 커스텀 로직 다이 위에 메모리를 쌓는 구조를 쓰고 있지만, 그 로직 다이·HBM 다이 크기는 GPU 다이보다 작고 연산량도 행렬곱을 계속 수행하는 XPU보다 훨씬 적다고 오스틴은 설명했다.
- TSV(실리콘관통전극, through-silicon via) 문제: 비아 주위에는 메모리 셀을 배치할 수 없는 킵아웃존(keep-out zone)이 생겨, 메모리 층을 쌓을수록(비아를 뚫을수록) 층당 용량이 줄어든다(빅 표현으로 절반가량). 그래서 유의미한 용량을 얻으려면 최소 4개 층은 쌓아야 하며, 2개 층으로는 밀도 손실 때문에 의미가 없다고 빅은 설명했다.

### The Roadmap: Accelerators, Alphawave, and the C1000 CPU
- 첫 HBC 기반 칩은 2027년 출시 예정이라고 밝혔다.
- 가속기 로드맵: AI 100(과거, 사실상 카운트하지 않음) → AI 200(2026년 샘플링, HBC 미적용) → AI 250(2027년, HBC 1세대 적용) → AI 300(FY28, HBC 2세대 적용, UALink 또는 E-sun 스케일업 패브릭 추가, 구리·광 스케일아웃 추가).
- 스케일업 CPO(공유 패키지 광학, co-packaged optics)는 청중 질의응답에서 AI 300 이후, 즉 2029년경으로 언급됐다.
- 빅이 검색(구글 AI 개요)한 바로는 퀄컴 회계연도가 9월 마지막 일요일에 시작한다 — 즉 FY27은 실제로 2026 역년(calendar year)에 걸쳐 있다.
- 알파웨이브 인수는 커스텀 실리콘 고객 관계·로드맵도 함께 가져왔다 — 발표에서 이름을 밝히지 않은 하이퍼스케일러 2곳을 언급했다. 별도로 사티아 나델라(마이크로소프트)와 마크 저커버그(메타)가 행사 영상에 등장했다.
- CFO는 2028년 알파웨이브 관련 매출로 10억 달러(각 하이퍼스케일러 고객사당 10억 달러씩 총 20억 달러)를 예상했고, 여기에 별도로 알파웨이브 기존 사업분이 추가로 더해져 총매출이 50억 달러 규모가 될 것으로 언급했다고 오스틴이 전했다(오스틴은 "I think"로 기억에 대한 유보를 달았다).
- 모듈러(Modular) 인수: 모조(Mojo, CUDA에 대응하는 프로그래밍 레이어), 맥스(MAX, Triton·TensorRT-LLM에 대응하는 모델 서빙 레이어), KV 캐시 오프로딩·데이터 이동을 처리하는 클라우드 제품(엔비디아 다이나모(Dynamo)에 대응)을 보유하고 있다. 이를 묶어 "멀티 실리콘 토큰 팩토리(multi-silicon token factory)"라 부른다.
- 모듈러 공동창업자 크리스 래트너(Chris Lattner)는 박사 과정 중 클랭(Clang) 컴파일러와 LLVM을 만들었고, 애플에서 스위프트(Swift) 언어를 만들었으며, MLIR(다층 중간 표현, multi-level intermediate representation) 작업 이력이 있다.
- 오스틴은 래트너가 과거에 모듈러 툴체인으로 엔비디아 자체보다 엔비디아 칩에서 더 높은 성능을 뽑아낼 수 있다고 말한 적이 있다고 언급했다.
- C1000 CPU 사양(퀄컴 발표 기준): 코어당 5GHz, 코어 수 250개 이상, PCIe Gen 7 지원, LPDDR 사용. 에이전틱(agentic) 전용, 범용, AI 헤드노드용 3가지 버전이 있다.
- 마크 저커버그가 영상 클립으로 등장해 메타가 C1000을 데이터센터에 배치할 계획이며, 다세대(multi-generational)에 걸친 공급 계약을 맺었다고 밝혔다.
- 청중 질의응답에서 C1000이 2028년 출시인데 2028년에도 경쟁력이 있겠냐는 질문이 나왔고, 알파웨이브 CEO 토니 피알리스(Tony Pialis)가 퀄컴 엔지니어가 처음부터 설계하면 출시 시점과 무관하게 최고 수준일 것이라고 답했다.

### Edge AI and Robotics
- 퀄컴은 소프트웨어 정의 차량(software-defined vehicle) 대신 AI 정의 차량(AI-defined vehicle)이라는 표현을 쓴다.
- 예시로 든 사례: 차량이 주차장에 진입해 QR코드를 인식하고 주차 요금을 자동 결제하며, 시간이 다 되면 자동 연장하거나 알림을 보낸다 — 이미 배치돼 있다고 밝혔다.
- 퀄컴은 비전(vision)을 엣지 추론의 핵심 입력으로 삼겠다는 방향을 밝혔다.
- 퀄컴은 최근 아두이노(Arduino)를 인수했고, 드래곤윙(Dragonwing) 플랫폼을 올여름(2026년) 출시할 예정이다.
- 빅에 따르면 아마존에서 파는 AI 카드로 클로드 코드(Claude Code)를 로컬 실행할 수 있다고 퀄컴이 인베스터 데이 발표에서 밝혔다.
- 퀄컴은 로봇공학을 2040년 기준 1조 달러 규모 기회로 제시했다.

### MOAR Memory
- 오스틴은 인베스터 데이 현장에서 CEO 크리스티아노 아몬에게 직접 질문을 던졌다 — HBC가 HBM 수요를 줄이고 DDR 수요를 늘릴 수 있는데, 동시에 엣지에서 메모리 수요가 늘어나는 상황에서 2028~2030년 메모리 시장을 어떻게 봐야 하냐는 질문이었다.
- 아몬은 HBM이 사라지지 않는다고 답했고, 대신 워크스테이션·노트북·자동차 등 온프레미스(on-premise) 인프라에서 LPDDR·메모리 수요가 늘어날 것이라고 답했다고 오스틴이 전했다.

## 숫자 (원문에 나온 것만)
- FY25 매출 구성: 스마트폰 3분의 2, 자동차·IoT 3분의 1
- FY27 목표: 스마트폰과 기타(데이터센터 포함)가 각각 절반
- FY29 목표: 자동차·IoT·데이터센터 3분의 2, 스마트폰 3분의 1
- SRAM 대역폭: 약 100TB/s (빅의 설명)
- HBM 대역폭: 약 8TB/s, SRAM의 약 10분의 1 (빅의 설명)
- 현행 HBM-GPU 인터커넥트 레인 수: 약 2,000개 (빅의 설명)
- HBC 인터커넥트 레인 수: 수만 개에서 최대 약 10만 개 (빅의 설명, 레인 100배→대역폭 100배)
- 레티클 크기 XPU 다이 면적: 약 800mm² 이상 (빅의 설명)
- 첫 HBC 칩(AI 250) 출시: 2027년
- AI 200 샘플링: 2026년
- AI 300: FY28
- 스케일업 CPO: AI 300 이후, 약 2029년 (청중 질의응답 기준)
- 퀄컴 회계연도 시작: 9월 마지막 일요일
- 알파웨이브 관련 2028년 예상 매출: 10억 달러(하이퍼스케일러 고객당) × 2곳 = 20억 달러, 총매출 50억 달러 (오스틴 "I think" 유보)
- C1000: 코어당 5GHz, 코어 250개 이상, PCIe Gen 7
- 로봇공학 기회: 1조 달러, 2040년 기준

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "Qualcomm being a communications player could just be the start of their story." — 퀄컴이 통신 기업이었다는 건 그저 이야기의 시작일 뿐일 수 있다. (Austin)
- "So the question is, what is Qualcomm's Mellanox?" — 그럼 질문은, 퀄컴에게 멜라녹스(Mellanox)에 해당하는 것은 무엇이냐다. (Vik)
- "This is d-Matrix's approach, what they call in-memory compute." — 이게 디매트릭스의 접근법이다, 그들이 인-메모리 컴퓨트라고 부르는 것. (Vik)
- "There has to be technological differentiation that really impacts TCO for a particular workload." — 특정 워크로드의 TCO(총소유비용)에 실제로 영향을 주는 기술적 차별화가 있어야 한다. (Austin)
- "They moved it to a different place." — (패키징 문제를) 없앤 게 아니라 다른 자리로 옮긴 것이다. (Vik, HBC의 패키징 문제에 대해)
- "Don't let anyone DeepSeek you and tell you, oh, HBM's dead because near-memory compute. No, MOAR, more memory." — 누가 딥시크식으로 "HBM은 죽었다, 니어메모리 컴퓨트 때문에"라고 말하게 두지 마라. 아니다, 모어, 메모리는 더 필요하다. (Austin)

## 주의
- 알파웨이브 2028년 매출 추정치(10억 달러×2, 총매출 50억 달러)는 오스틴이 "I think"라고 유보를 단 회상이며, 슬라이드 원문 인용이 아니다.
- 레인 수(2,000개 → 수만~10만 개), SRAM/HBM 대역폭(약 100TB/s, 약 8TB/s), XPU 다이 면적(약 800mm² 이상)은 모두 진행자들의 어림값이며 퀄컴 발표 슬라이드의 정확한 수치로 확인된 것은 아니다.
- 스케일업 패브릭 이름 "E-sun"은 청취 전사 표기로, 업계에서 통용되는 정식 명칭(예: Ultra Ethernet 계열)의 오기(誤記)일 가능성이 있다.
- 퀄컴 회계연도 시작일("9월 마지막 일요일")은 빅이 방송 중 실시간 검색(구글 AI 개요)으로 확인한 값이며, 원문 자체의 재확인은 아니다.
- 로봇공학 "1조 달러, 2040년" 전망은 퀄컴이 제시한 장기 전망치로, 진행자들도 "늘 2040년"이라며 회의적 뉘앙스를 붙였다.
- HBC 다이 구조(로직 칩이 완전한 XPU인지 단순 가속기인지)는 진행자 두 사람의 추정이며, 퀄컴이 명시적으로 확인한 사실이 아니다.
