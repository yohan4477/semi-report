# SemiAnalysis 로봇 사실표 A
> 원문 2편 · 추출일 2026-08-24

원문
- **[자율] 2025-07-30** — Robotics Levels of Autonomy (Reyk Knuhtsen·Dylan Patel·Niko Ciminelli)
- **[사족] 2025-10-20** — Quadruped State of The Market: Unitree, Boston Dynamics, ANYbotics, DEEP Robotics, and The Rising Application Ecosystem (같은 저자)

두 원문은 **석 달 차이**다. 값·생산량·TAM·「지금 어디까지 왔나」는 같은 시점의 말이 아니므로, 항목마다 `(발행일 · 소제목)`을 달았다. 두 원문이 같은 대상을 다르게 말하는 자리는 맨 아래 **F**에 따로 모았다.

---

## A. 자율 레벨

SemiAnalysis가 「업계 최초」라고 내세운 분류로, 로보틱스를 5개 Level로 나눈다. 축은 둘 — **Agency**(스스로 계획·추론)와 **Dexterity**(손발의 정교함). 레벨 구분선은 「가능한가」가 아니라 **상업적 성립 여부**에 그어져 있다. 신뢰성이 증명된 뒤에도 비용을 정당화할 만큼의 처리량(throughput)을 내야 그 레벨로 친다. (2025-07-30 · 도입부, Describing Autonomy)

### L0 — Scripted Motion (스크립트 동작)
- **정의**: 로봇이 전부 사전 프로그래밍되어 있고, 정적인 환경과 정적인 작업에서만 작동한다. (2025-07-30 · Executive Summary)
- **해금(Unlock)**: 높은 정확도, 높은 반복성 / **능력**: 24/7 자동화, 높은 처리량 (2025-07-30 · Executive Summary)
- **2025년 배치처**: 자동차·전자 공장의 업계 표준 (2025-07-30 · Executive Summary)
- **대표 사례 — 「셀(cell)」**: 로봇이 우리(cage) 안에 갇혀 있는 구조. 이유 셋 — ① 주변 사람의 안전(컴퓨터 비전과 자율성이 없어 사람이 들어와도 동작을 계속한다. 대신 Estop 버튼·라이트 커튼·control barrier function을 쓴다) ② 외부 간섭·교란 차단 ③ 셀마다 로봇과 장소에 맞춰 재단해 설치·프로그래밍을 단순화 (2025-07-30 · Deployments and Considerations: Locked Away)
- **대표 사례 — 「다크 팩토리(Dark Factory)」**: 조명 없이 로봇만으로 돌아가는 시설. FANUC 관계자에 따르면 일본의 한 공장에서 자사 로봇들이 **80초에 로봇 1대**를 만들고 있다. 이것도 여전히 L0다 — 전부 사전 프로그래밍이고 환경·작업이 완벽히 통제돼 있다. (2025-07-30 · Implications: Efficiency and Dark Factories)
- **실제 배치 규모**: 자동차 공장은 통상 **공장당 산업용 로봇 400~1000대**, 많게는 **1650대** 보고 사례. 전자 제조는 더 적어 **시설당 50~200대**(AMR 운반, 회로기판에 부품을 정적으로 얹는 SCARA, 하드웨어를 깎는 CNC, 기계 관리용 협동로봇 등). Amazon은 수십만 대(hundreds of thousands). (2025-07-30 · Implications: Efficiency and Dark Factories) ※ Amazon 로봇 대수는 석 달 뒤 원문에서 갱신됐다 — F-1 참조
- **한계**: 로봇이 스스로 문제를 진단하거나 풀지 못한다. 사람 기술자가 항상 현장에 있어야 하고(다크 팩토리 제외), **로봇:사람 비율 20:1**, 까다로운 산업 현장은 **12~15:1**까지 내려간다. 사람이 점심을 먹거나 교대하면 로봇도 대개 세워야 한다. (2025-07-30 · Current Challenges: The Issue of Rigidity)

### L1 — Intelligent Pick and Place (지능형 집기·놓기)
- **정의**: 로봇이 다양한 자세로 놓인 물건을 식별하고 집어 분류할 수 있다. (2025-07-30 · Executive Summary)
- **해금**: 일반화 가능한 지각(perception), 일반화 가능한 파지(grasping) / **능력**: 고정형 pick and place (2025-07-30 · Executive Summary)
- **2025년 배치처**: 소포(parcel) 물류센터의 pick and place 분류 작업에 도입, 역량과 통합이 개선되며 추가 창고 시장으로 침투 확대 중 (2025-07-30 · Executive Summary)
- **시기**: 2015년경 로보틱스에 지능이 처음 주입됐고, 2018년경 상업화를 시도했다. 원문이 다루는 구간은 **파운데이션 모델 이전인 2015~2022년**. (2025-07-30 · Level 1: Intelligent Pick and Place)
- **대표 사례 — 「arm farm」**: 몇몇 회사가 수개월간 파지를 반복해 학습 데이터를 모은 시설. 집기 성공률은 결국 99%까지 올랐지만 99.99%로 가는 「마지막 1mm(last millimeter)」가 거의 같은 난이도였고, 그마저도 ROI를 증명하기엔 부족한 경우가 있었다. (2025-07-30 · Level 1: Intelligent Pick and Place / A Look at The Past - 2015-2022)
- **연구 이정표**: Pinto & Gupta (2015) — **700시간**의 파지 시도로 **파지 정확도 80%** 도달. Levine et al. (2016) — 약 **3000시간**의 파지 데이터, 파인튜닝 후 **파지 예측 정확도 94.6%**. 지각 쪽 계보는 ImageNet(2009) → AlexNet(2012) → YOLOv1(2015, 실시간 객체·바운딩박스 검출) → Mask R-CNN(2017, 마스크로 형상 추정) → PoseCNN(2018, 스테레오 카메라만으로 6D 자세 추정). (2025-07-30 · Beginning Sparks)
- **대표 배치처**: 창고·물류의 pick and place 자리. 두 수평 컨베이어 사이의 집기·놓기 스테이션처럼 이상적이고 값싼 위치가 선택됐고, 세로형 putwall 같은 어려운 위치는 건너뛰었다(대부분의 로봇이 수평 작업으로 학습했고 라인을 수평으로 재구성하는 비용이 컸다). 적절한 위치를 걸러내면 설치는 **최대 4주**. (2025-07-30 · Deployments and Considerations: The Wild West)
- **어디서 됐고 어디서 안 됐나**: 전자상거래 이행(high-mix·low-throughput)에서는 **로봇 11대가 사람 9명의 일**을 하는 데 그쳤고 픽당 비용이 사람 밑으로 내려가는 데 **3.5년**이 걸렸다. 반면 소포(parcel)에서는 **로봇 10대가 사람 23명의 일**을 했고 픽당 비용이 **1년 남짓** 만에 사람 밑으로 내려갔다. (2025-07-30 · Implications: A Narrow Market of Profitability)

### L2 — Autonomous Mobility (자율 이동)
- **정의**: 로봇이 열린 세계(open world)를 이해하고, 길을 찾고, 여러 지형을 통과할 수 있다. (2025-07-30 · Executive Summary)
- **해금**: 상위 수준 계획(high-level planning), 공간 추론, 견고한 보행 / **능력**: 열린 세계에서의 내비게이션과 주파 (2025-07-30 · Executive Summary)
- **2025년 배치처**: 점검·데이터 수집 역할의 **초기 양산 단계(early production phases)** — 건설 현장, 정유·가스 정제소, 핵심 인프라 등 (2025-07-30 · Executive Summary)
- **무엇이 열었나**: Agency는 파운데이션 모델과 VLM(Vision-Language Model)에서, Dexterity(보행)는 **시뮬레이션 안의 대규모 강화학습**에서 왔다. 둘 다 각 상황마다 데이터를 모으는 대신 방대한 디지털 데이터셋을 쓴다. (2025-07-30 · Level 2 - Autonomous Mobility)
- **대표 사례**: 「go to the stairs past the ladder」라는 명령을 VLM이 객체와 관계로 풀고, 파운데이션 모델이 "사다리 왼쪽으로 이동한 뒤 계단 쪽으로 우회전"이라는 계획으로 옮긴다. (2025-07-30 · The Breakthrough: Foundation Models)
- **하드웨어**: Nvidia Jetson 같은 온보드 컴퓨트, 다중 센서·카메라·LiDAR, 고효율 액추에이터와 개선된 배터리. (2025-07-30 · Hardware Boosts)
- **핵심 폼팩터**: **사족보행(quadruped)이 해금됐다.** 대규모 시뮬레이션 플랫폼이 네 다리의 견고한 제어를 가능케 했고, Agency가 장면 파악과 계획을 맡는다. L2에서 사족보행 보행 능력이 **개선 변곡점**에 닿았다. (2025-07-30 · Agile Movement - Dexterity / Deployment and Considerations: Agents In The Open World)
- **배치 실무**: 수백만 달러의 시설 엔지니어링이 더는 필요 없고, 새 환경에 **1~3주** 만에 투입해 도메인을 익히고 작업을 수행한다. 다만 배터리 지속시간이 로봇·충전기 대수를 결정한다 — **사족보행은 평균 90분 배터리**라 로봇이나 충전 스테이션을 더 사야 할 수 있다. (2025-07-30 · Deployment and Considerations: Agents In The Open World) ※ 배터리 수치는 석 달 뒤 원문에서 넓혀졌다 — F-2 참조
- **안전**: 넘어지거나 불이 나도 코드를 뽑을 방법이 없다. 미끄러운 바닥에서 **70lb 사족보행 로봇**이 누군가의 발 위로 넘어지거나 계단을 굴러 사람을 덮치는 위험이 대상이다. 대책은 충돌 회피, 속도·이격 감시(speed and separation monitoring), 로봇의 존재·의도를 알리는 소리·시각 신호. (2025-07-30 · Deployment and Considerations: Agents In The Open World)
- **실제 배치처(사례)**: 건설 현장 캡처, 정유·가스(방폭 사족보행이 여러 현장을 순찰), 핵심 인프라(풍력발전기·전기 야드·해상 리그). 그리고 반도체 팹, 제철소, 철도 인프라, 라스트마일 배송으로 확대 중. (2025-07-30 · Implications: Unlocking Inspections and Data Collection Roles)
- **남은 문제**: 위치 오차가 누적되는 compound error 탓에 여전히 **AprilTag**(QR코드 같은 재정위 스티커)를 관심 지점에 붙인다. 깊은 진흙·얼음·투명 유리는 여전히 어렵거나 아예 피한다. (2025-07-30 · Snapshot of Today's Autonomy Challenges for Level 2)

### L3 — Low-skill Manipulation (저숙련 조작)
- **정의**: 로봇이 기본적이고 비핵심적인 저숙련 작업을 수행할 수 있다. (2025-07-30 · Executive Summary)
- **해금**: 일반화 가능한 조작(generalizable manipulation) / **능력**: 고급 pick and place, 이동형 조작(mobile manipulation) (2025-07-30 · Executive Summary)
- **2025년 배치처**: 주방, 세탁소, 제조, 물류에서의 **초기 파일럿 단계(early pilot stages)** (2025-07-30 · Executive Summary)
- **조작의 정의**: 목적을 갖고 맥락에 맞게 환경과 상호작용해 그 상태를 바꾸는 것 — 문을 밀어 열기, 손잡이를 잡기, 상자를 모서리로 들기 등. (2025-07-30 · Level 3 - Low-Skill Manipulation)
- **무엇이 열었나**: **VLA(Vision-Language-Action) 모델** — VLM에 행동(action) 양식을 붙인 것. 이미지/텍스트/행동 쌍으로 학습해 장면을 읽고 과제를 해석하고 **행동 계획을 출력**한다. 두 형태 — task-specific(계획용 VLM + 개별 과제 모델)과 singular(단일 모델이 추론·계획·행동 전부). L1의 「성배」였던 옷 개기가 여기서 **가능해진다** — 주름을 하나하나 세는 대신 「소매」·「깃」 같은 추상 개념을 인터넷 데이터에서 이해한다. (2025-07-30 · Vision-Language-Action Models)
- **데이터**: GELLO(2023) 같은 저가 원격조작 하드웨어가 나오면서 전 세계 사용자가 로봇 행동 데이터를 모아 오픈소스로 공개하기 시작했다. (2025-07-30 · Open-Source and The Data Increase)
- **현재 과제가 갖춰야 할 4조건**: ① 성공 판정 폭이 넓을 것(정밀도 제약이 없을 것) ② 처리량 요구가 거의 없거나 비동기일 것(예: 야간) ③ 재시도 가능할 것 ④ 힘·무게 감각이 필요 없을 것 — 이 로봇들은 촉각이 없고 관절 수준의 초보적 힘 피드백만 있다. (2025-07-30 · Level 3 - Low-Skill Manipulation)
- **실제 파일럿 영역**: 식당·급식 조리(재료는 미리 계량돼 나온다), 산업용 세탁(수건·시트·베갯잇·냅킨 같은 반복 품목 개기), 물류(선반 보충, 토트 회전, 시설 내 물품·통 운반 등 「just-to-stock」), 제조(라인사이드 이송, 부품 시퀀싱과 다음날 조립용 자재 정리). 그 밖에 생울타리 손질·조경 등도 조건에 맞을 수 있으나 **아직 판단하기 이르다**. (2025-07-30 · Implications: Low-Skill Labor Replacement)
- **배치 방식**: 사람 직원처럼 투입된다. 현장에 놓고, 원격조작자가 태블릿을 보며 워크플로를 수행해 데이터를 모으고 모델을 가르친다. 원격조작 비용은 낮고 대개 신흥국에 외주로 나가며 투자자 보조를 받는 경우가 많다. 경제 논리가 **다년 ROI에서 시간당 임금 과금(Robot-as-a-Service)** 으로 바뀌어 며칠 만에 매출 플러스가 될 수 있다. (2025-07-30 · Deployments and Considerations: Robot Coworkers)
- **한계**: 원격조작 감시(teleoperation oversight)가 현재는 필수다. 조작(Action)을 VLM에 붙이면 컨텍스트 창을 크게 잡아먹어 L2에서 가졌던 시간 지평이 줄고, 현재 과제 길이는 **길어야 몇 분**이다. 초기 배치는 **펜스로 막은 구역**에 머물 가능성이 크다. (2025-07-30 · Vision-Language-Action Models / Deployments and Considerations: Robot Coworkers)

### L4 — Force-dependent Tasks (힘 의존 작업)
- **정의**: 힘과 무게에 대한 이해가 필요한 섬세한 작업을 수행할 수 있다 — 주머니 속 휴대폰 찾기, 나사를 올바른 나사산에 박기 등. (2025-07-30 · Executive Summary)
- **해금**: **연구 중(In Research)** / **능력**: 섬세한 힘 의존 작업, 미세 조작 (2025-07-30 · Executive Summary)
- **2025년 배치처**: **연구 중(In Research)** — 배치 사례 없음 (2025-07-30 · Executive Summary)
- **접근 후보**: 지문 끝 촉각 센서(advanced sensors), 대규모 시뮬레이터, 촉각·힘 데이터로 VLA 학습, 과제별 모델(task-specific models), 순응 제어(compliant control). (2025-07-30 · Potentially Useful Avenues)
- **함의(예측)**: 숙련 기술직(배관·전기·정밀 조립), 서비스업 잔여 직군, 제조·물류의 나머지 작업. 나아가 재난 구조팀, 자율 우주 탐사. (2025-07-30 · Level 4 Implications: Mass Labor Replacement)

---

## B. 값

### 통합(integration) 비용 배수 — 핵심 숫자
- **L0의 통합 총액은 로봇 자체 값의 약 4~6배.** 중형 자동차 공장을 완전히 새로운 body-in-white(용접 차체 프레임) 조립 라인으로 리트로핏하는 시나리오 기준. 셀 시공과 배치, PLC·컨베이어/라인 트랙·MES 등 관련 시스템 구성, 설치와 시험이 값을 밀어올린다. (2025-07-30 · Integration: 4x to 6x The Cost of The Robots Themselves)
- 단, **표준화된 자동차 솔루션이라면 로봇 CapEx의 ~70% 정도**로 떨어질 수 있다. (2025-07-30 · Integration: 4x to 6x The Cost of The Robots Themselves)
- 신규 대규모 자동차 조립 라인 자체는 **$10M~$60M**, 구축에 수년이 걸린다. 업계 관계자는 이런 프로젝트에 「생일이 있다」고 농담했다. (2025-07-30 · Deployments and Considerations: Locked Away)
- 통상 **같은 시스템 통합업체와 같은 로봇 브랜드+소프트웨어**를 써야 한다 — 새 시스템이 공장 흐름을 깨뜨릴 위험을 없애기 위해서다. (2025-07-30 · Integration: 4x to 6x The Cost of The Robots Themselves)

### L1 배치 비용
- 팔과 셀을 창고 라인에 통합하는 데 **$90K~$180K**. (2025-07-30 · Deployments and Considerations: The Wild West)
- 로봇의 커스텀 API가 창고관리시스템(WMS)과 「악수(handshake)」해야 하는데, 로봇 API가 애초에 WMS를 염두에 두고 만들어지지 않은 경우가 잦았다. WMS 업데이트가 실패하면 **수천만 달러(tens of millions of dollars)** 손실. 우회로로 제3자 통합업체를 쓰면 배치에 **수십만 달러(up to hundreds of thousands)** 를 청구한다. 대개는 GUI 자동화 에이전트(사람이 버튼 누르는 걸 흉내내는 프로그램) 같은 미봉책으로 때웠다. (2025-07-30 · Deployments and Considerations: The Wild West)
- 설치 자체는 위치를 잘 고르면 **최대 4주**. 다만 창고의 도입 의사결정 주기가 **수개월** 걸릴 수 있다. (2025-07-30 · Deployments and Considerations: The Wild West)

### L2·L3 배치 비용
- L2: 새 환경 투입에 **1~3주**, 수백만 달러의 시설 엔지니어링 불필요. (2025-07-30 · Deployment and Considerations: Agents In The Open World)
- L3: 「사람 직원처럼」 드롭인 배치, **시간당 임금(RaaS)** 과금. 금액은 이 원문에 없음. (2025-07-30 · Deployments and Considerations: Robot Coworkers)
- 서구 사족보행 로봇의 RaaS 요금은 **월 ~$10K**. (2025-10-20 · State of The Hardware Market - Unitree's Pricing Advantage)

### 다운타임 비용(무엇을 막으려고 로봇을 넣는가)
| 대상 | 값 | 발행일 · 소제목 |
|---|---|---|
| 자동차 공장 | 시간당 **$2M** | 2025-07-30 · Current Challenges: The Issue of Rigidity |
| 반도체 팹 | 하루 **$50M** | 2025-07-30 · Current Challenges: The Issue of Rigidity |
| 중형 정유소 | 계획 외 다운타임 1시간에 최대 **$500,000** | 2025-07-30 · Oil & Gas |
| 하이퍼스케일 데이터센터 | 하루 **~$1M** | 2025-10-20 · Potential Market Opportunities |

### L0 자동화의 경제성
- 자동차 라인은 **2년 안에** 투자를 회수하고, 이후 운영비는 **약 75% 저렴**해진다. 업계 관계자 표현으로 「돈을 찍어낸다」. (2025-07-30 · Implications: Efficiency and Dark Factories)
- 일부 시설은 **하루 2,000대**의 차를 만든다. 창고 팔 하나가 피로 없이 **사람 ~10명 몫**을 한다. **로봇 50대가 노동자 200명의 대형 조립·조작 작업을 직무당 ~73% 낮은 비용**으로 수행하는 식이다. (2025-07-30 · Implications: Efficiency and Dark Factories)

### L1의 노동 대체 산수
- Amazon의 이직률은 **주당 2~4%** — 바닥 인원 100명이면 연말까지 **104명**이 그만둘 수 있다는 뜻. 상시 채용·온보딩·교육·생산성 램프업 탓에 임금이 이직 없는 경우보다 **56% 높아진다**. (2025-07-30 · Implications: A Narrow Market of Profitability)
- 전자상거래 케이스: 픽당 비용이 사람 밑으로 내려가는 데 **3.5년**, **로봇 11대 = 사람 9명**. (2025-07-30 · Implications: A Narrow Market of Profitability)
- 소포 케이스: 목표 **시간당 550픽**, 정확도 **95%** 면 실효 픽레이트 **520**. **로봇 10대 = 사람 23명**, 픽당 비용이 **1년 남짓** 만에 사람 밑으로. (2025-07-30 · Implications: A Narrow Market of Profitability)
- 창고 환경 자체는 배송의 **98~99%가 정시**인 최적화된 곳이다. (2025-07-30 · Deployments and Considerations: The Wild West)
- Plus One Robotics는 소포 단일 팔 솔루션에서 **최대 1,600픽**. (2025-07-30 · What To Expect)

### L1의 실패 비용
- 파지 실패의 **40%** 는 사람 개입이 필요했고, 산업용 팔이라 창고 라인 전체를 멈추고 조치한 뒤 재개해야 해 **평균 복구시간(MTTR) ~6분**. (2025-07-30 · Beginning Sparks)
- **99% → 99.99%는 81배 개선**이고, 이는 처음 1%→80%로 가는 것보다 큰 폭이다. (2025-07-30 · A Look at The Past - 2015-2022)
- Amazon 품목 카탈로그의 **25%** 가 「제외 목록(exclusion list)」에 올라 있다 — 실패 위험 탓에 로봇이 집지 않기로 한 물건들. 새 품목은 시험해서 **5~10회** 실패하면 같은 목록으로 간다. (2025-07-30 · Challenges: The Limits of Brittle Intelligence)

### L2의 절감 사례
- **건설**: 공사 재작업의 **40%** 가 부실한 문서화에서 비롯되고, 이것이 청구액의 **최대 20%** 를 잡아먹는다. 전면 캡처는 가장 선임인 현장감독의 **8시간 근무 하루**를 통째로 묶는다. **200실 규모 호텔** 공사는 주(州) 규정상 토목기사나 면허 측량사가 캡처를 해야 할 만큼 클 수 있고, 이는 **격주로** 이뤄지며 **$1M을 넘길** 수 있다. (2025-07-30 · Construction)
- **정유·가스**: 중형 정유소가 누출·진동·열을 추적하도록 기계를 완전히 센서화하는 데 **수백만 달러를 수년에 걸쳐** 투입한다. 대신 알맞은 센서를 단 방폭 사족보행 로봇이 **그 비용의 일부(fraction)** 로 여러 현장을 순찰할 수 있다. (2025-07-30 · Oil & Gas)
- **핵심 인프라**: 노후 데이터센터가 폭우 때 셧다운하고 변전 설비 점검을 요구하는 자리에, 사족보행 로봇이 셧다운 없이 점검을 자동화해 **1년에 약 $350K**를 아꼈다고 들었다. (2025-07-30 · Critical Infrastructure)

### L3 노동 대체
- 샌프란시스코 식당의 연간 이직률은 **최대 170%**. (2025-07-30 · Implications: Low-Skill Labor Replacement)
- 식당은 가장 노동집약적인 업종으로, 같은 **매출 $1m**을 만드는 데 병원의 **약 3배** 인원이 필요하다. (2025-07-30 · Implications: Low-Skill Labor Replacement)
- 원격조작 감시 비율은 초기 **1:1**에서 **10:1** 정도로 늘어날 것으로 본다. (2025-07-30 · Looking Forward: Deployments)

### 사족보행 응용 시장의 값
- **라스트마일 배송**: 시급 **$18**의 사람 배달원은 배송 1건당 **최대 $9**가 드는 반면, 로봇은 같은 일을 **건당 ~$2.50**에 한다. (2025-10-20 · Potential Market Opportunities)
- **보안 순찰**: 비무장 경비원의 24/7 순찰은 임금·교육에 따라 **연 $250K~$450K**. 사족보행 RaaS는 **월 $10K**. (2025-10-20 · Potential Market Opportunities)
- **반도체 팹**: 배관 하나가 터지면 교체에 **$30,000**이지만, Spot이 조기에 감지해 수리하면 **$3,000** 수준으로 끝난다. 저입자(low-particle) 규격 인증에는 **수개월**이 걸린다. (2025-10-20 · Boston Dynamics' Aim: Fabs)
- **방폭(ATEX) 인증**: 배터리 화학 변경, 질소 충전, 스파크 제거 안전장치가 필요하고 **최대 2년**이 걸리며 그동안 하드웨어 설계가 동결된다. (2025-10-20 · ANYBotics Aim: Dirty and Dangerous Environments)

---

## C. 사족보행 시장

이 절의 항목은 별도 표기가 없으면 전부 **2025-10-20** 원문이다.

### 왜 지금 네 발인가
- **사족보행은 오늘날 가장 앞선 범용 로봇이다.** 휴머노이드만큼 헤드라인을 잡지는 못하지만, L2 자율성이 켜지면서 이전에 로보틱스가 접근하지 못한 시장이 열렸다. (2025-10-20 · 도입부)
- 강점 셋: ① 동적 보행으로 무릎을 굽혀 좁고 어수선한 곳을 지난다(화학 플랜트·건설 현장) ② 시스템 통합업체가 LiDAR·음향 센서·영상 등 온갖 센서를 얹을 수 있다 ③ 네 다리의 힘과 큼직한 배터리 덕에 장시간 점검이 가능하다. (2025-10-20 · Why Quadrupeds Dominate Navigation Tasks)
- 논리는 「범용 플랫폼으로서 초기 기능성이 가장 크다 → 더 널리 쓰인다 → 비용이 내려간다 → 내비게이션 과제에서 가장 확장 가능한 폼팩터가 된다」. (2025-10-20 · Why Quadrupeds Dominate Navigation Tasks)

**드론과의 대비** (전부 2025-10-20 · Drones - Small And Delicate Navigation)
- 드론이 속도는 훨씬 빠르고 값도 훨씬 싸지만 규제가 목을 죈다. 대부분의 경우 진짜 자율로는 못 돌고, 특히 건설 같은 옥외에서는 운용자가 계속 감시해야 한다.
- **prop wash**: 벽·천장·바닥에 가까이 가면 난류가 생겨 추락한다. **로터 지름의 약 1.5배** 거리에서 드론이 벽에 「끌려간다」.
- 드론 배터리는 이미 **~30~45분**으로 짧다. 반면 사족보행은 **수 시간(up to hours)** 을 버티고 충돌에도 견딘다.

**바퀴형·궤도형과의 대비** (전부 2025-10-20 · Wheeled Robots and Tracked Robots - Robust, But With Tradeoffs)
| 항목 | 값 |
|---|---|
| 바퀴형 속도 | **~2 m/s** |
| 사족보행 속도 | **0.75~1 m/s** |
| 궤도형 속도 | **~0.4 m/s** |
| Argus(바퀴형)의 회전 반경 | **2.5 m** |
| 대부분의 사족보행 길이 | **~1 m** |
| 궤도형 지상고(clearance) | **4~6 cm** |
| 바퀴형 지상고 | **최대 12 cm** |
| 궤도형이 오를 수 있는 계단 | **20 cm+**, 경사 **최대 45도** (넘어질 위험 있음) |
| 사족보행이 건널 수 있는 틈 | **~30 cm** |
- 바퀴를 키우면 지상고는 오르지만 안정성을 잃고 차체가 커져 회전 반경 문제가 생긴다. 다만 램프 꼭대기의 「breakover angle」을 넘으려면 큰 바퀴가 필요할 수 있다.

**사족보행을 가능하게 한 하드웨어 변화** (전부 2025-10-20 · Key Enablers of the Rise of Quadrupeds)
- 리튬이온 배터리: 2010년 **~12kg**이던 배터리가 에너지 밀도 향상으로 지금 **~6kg**.
- 액추에이터: 무겁고 새고 비싼(수천 달러대) 유압에서 값싼 전기식으로 전환.
- 센서: LiDAR 가격이 **자릿수 단위(orders of magnitude)** 로 하락, 카메라 화소는 배수로 증가, ToF(깊이) 센서 측정 거리는 두 배.
- 컴퓨트: Nvidia **Jetson TX1(2015) 1 TFLOP** → 오늘의 **Jetson Thor 2070 TFLOPS(FP4)**.

### Unitree — 가격과 BOM
- 2023년 **전 세계 판매 대수 기준 점유율 약 70%**(추정). 연매출은 **10억 RMB(~$140M)** 를 넘어섰다. (2025-10-20 · Setting The Stage)
- **2023년 한 해만으로 Unitree의 총 출하량이 차순위 경쟁사의 약 10배.** 이후 숫자는 훨씬 커졌지만 이것이 마지막 공개 발언이다. (2025-10-20 · State of The Hardware Market - Unitree's Pricing Advantage)
- 성수기에 **하루 약 200대의 Go2**를 생산한다. (2025-10-20 · State of The Hardware Market - Unitree's Pricing Advantage)
- **Go2 BoM**: 제조원가(COGS) **$3,272**. 개발용으로 잠금 해제된 **EDU 버전 가격 $8,000** 기준 **매출총이익률 59%**. (2025-10-20 · Unitree Go2 and B2 BoM and Margins)
- **B2**: 가격 **$55,000**에서 **매출총이익률 77%**. (2025-10-20 · Unitree Go2 and B2 BoM and Margins)
- 즉 **Unitree는 손해 보고 파는 것(loss leading)이 아니다.** 저비용 대량생산을 풀었다는 것이 원문의 주장. (2025-10-20 · 도입부)
- 제품군: **Go2**(저가, 고가 라인의 약 1/10 가격, 데이터 수집 용도) / **B1**(산업용 방수, 보행 시 적재 **20kg**) / **B2**(비방수, B1 위에 배터리 수명과 관절 강도를 더해 보행 적재 **40kg**, 바퀴 옵션) / **A2 'Stellar Hunter'**(최신, 스펙은 덜 알려짐, 바퀴 옵션). (2025-10-20 · Setting The Stage)
- 고급형 사족보행이 서구 모델보다 **최대 50% 저렴**하고 **IP68 완전 방수**지만 서구 산업 시장에서는 아직 흔치 않다. 중국 국가전력망·화학 플랜트·제철소에 배치되며 **완전 자율이 아니라 원격조작** 형태가 많다. (2025-10-20 · Unitree: From Industrial Use-cases In China to Research)

**왜 싼가 — 액추에이터** (전부 2025-10-20 · Actuator Design Is Pivotal / Unitree's Actuators: MIT Cheetah 3 and The Quasi-Direct-Drive)
- 액추에이터가 BoM에서 가장 큰 몫으로 **통상 50~70%**.
- Unitree는 **MIT Cheetah 3(2018)** 계열의 **Quasi-Direct-Drive(QDD)** 를 쓴다. QDD의 감속비는 **5:1~25:1**로, 흔한 고감속 기어박스의 **최대 200:1**보다 훨씬 낮다. **Unitree의 QDD는 자주 10:1 미만**이라 마찰과 비용이 더 내려간다.
- 고감속의 단점: 「투명성(transparency)」이 나빠 발끝에서 오는 힘이 뭉개지고, 마찰이 커서 충격 시 관절이 부드럽게 역회전하지 못해 손상 위험이 커진다.
- QDD의 장점: 마찰이 낮아 **backdrivability**(반대 힘에 순응하는 능력)가 생긴다. 울퉁불퉁한 지형에서 사람 무릎처럼 다리가 자연스럽게 굽는다.
- QDD의 단점: QDD에 흔히 쓰는 유성기어(planetary gear)는 다른 해법보다 빨리 닳아 잦은 수리를 부른다. **backlash**(기어를 되돌릴 때 생기는 작은 오차)가 생기는데, 발을 바닥에 쿵 찍어 위치를 되잡아 보정할 수 있으나 기어가 닳을수록 커진다.
- 감속비가 낮으니 토크 밀도가 높은 모터가 필요하고, 그래서 큰 로봇은 훨씬 무거워진다. **산업용 B2의 모터는 Go2 모터의 3배+ 무게**. 낮은 감속비로 덩치를 키우면 정확도와 견고성이 떨어져 **B1/B2가 「흔들린다(wobbliness)」**.

**왜 싼가 — 센서와 배터리**
- 센서(사방 카메라 + 중앙 360° LiDAR + 흔히 ToF)가 사족보행 비용의 **최대 20%**. (2025-10-20 · Sensors: A Chinese Cost Advantage)
- Unitree는 Robosense·LIVOX 같은 중국 제조사에서 **수백 달러(a few hundred dollar)** 짜리 LiDAR를 사거나 직접 싸게 만든다. **서구 LiDAR는 $2,000에 가깝다.** Boston Dynamics는 **BoM 전체를 비중국산으로 요구**한다고 전해져 이 절감에서 배제된다. (2025-10-20 · Sensors: A Chinese Cost Advantage)
- 배터리 지속시간은 **90분~5시간** 범위. Unitree **A2 'Stellar Hunter'는 5시간 초과**, **25kg 적재 시 3시간+**. 단 이 수치는 온보드 감지·추론 부하를 제외한 것이다. 전형적인 서구 배치는 **Nvidia Jetson Orin 1~3개(각 ~50W)** 에 음향·열화상·사진측량 센서를 더한다. 그런 부하를 얹고도 **Unitree의 배터리 수명은 서구 경쟁사의 약 두 배**. (2025-10-20 · Battery Life - Chinese Hardware Prowess)

### 다른 회사들이 노리는 자리
| 회사 | 노리는 자리 | 숫자·근거 | 발행일 · 소제목 |
|---|---|---|---|
| **Boston Dynamics** | **반도체 팹**. 저입자 규격 인증에 수개월. 서브팹·클린룸은 더 어렵고, 어떤 팹은 「한 번 들어온 로봇은 다시 나가지 않는다」를 요구해 완전 자율과 흔들림 없는 신뢰성을 강제한다. 밀봉 관절, 특수 소재, 심지어 「강아지 옷(doggy-suit)」 커버링이 필요할 수 있다 | 제품군(창고용 팔 Stretch 포함) 연매출 **$100M~$200M**(여러 보도 기준). 퇴로로 Spot의 「ruggedize」 계획 | 2025-10-20 · Boston Dynamics' Aim: Fabs / Setting The Stage / ANYBotics Aim |
| **ANYbotics** | **더럽고 위험한 환경**. IP67(방진·침수 가능) — 부식성 칼륨 광산, 해상 리그. **서구에서 유일한 IP67 등급 사족보행**. 나아가 **유일하게 방폭 모델 ANYmal X를 개발 중, 2026년 상반기(1H26) 예정**. ATEX 등급을 받으면 폭발성 가스가 있는 **Zone 1** 구역에 들어갈 수 있다 | 2016년 **ETH Zurich** 스핀오프, 연매출 **$27M 미만**. 시스템 통합업체들은 부식성·위험·(곧) 폭발성 환경의 선호 선택지로 ANYbotics를 꼽는다 | 2025-10-20 · ANYBotics Aim: Dirty and Dangerous Environments / Setting The Stage |
| **DEEP Robotics** | **전력 인프라 점검 → 라스트마일 물류**. 국내외 산업 점검에서 강한 성과, 견고한 바퀴형 로봇과 해외 네트워크로 배송 진출이 가능해 보인다 — **단 Unitree의 더 싼 바퀴형 사족보행이 들어오지 않는다면** | 산업용 Unitree와 비슷한 **IP67**·배터리·적재 능력을 **30%+ 비용**으로. **40개국+ 약 600건 배치** | 2025-10-20 · DEEP Robotics: Electrical Infrastructure to Logistics / Setting The Stage |
| **Unitree** | **중국 내 산업 용도 + 연구 커뮤니티**. 연구에서는 압도적 — Spot과 ANYmal은 대부분의 연구실에 너무 비싸고, 특히 제어 정책을 시험하다 하드웨어를 부술 위험이 있다. 연구자는 저가 Go2를 골라 Unitree SDK 위에서 대규모 R&D를 한다. **바퀴형 사족보행**이라는 별도 강점도 있어 넓은 경계 순찰처럼 속도가 필요한 용도에서 서구 제품을 이길 수 있다 | Unitree는 **직접 모터 제어를 개방**한다. Spot도 이 접근을 주지만 **연간 반복 요금**을 받는다. Unitree 로봇을 쓴 첫 주요 논문 **Rapid Motor Adaptation(2020)** 이 이 개방성 덕에 가능했고, 이후 시각에서 모터 제어까지의 첫 end-to-end 보행 시스템들이 나왔다 | 2025-10-20 · Unitree: From Industrial Use-cases / Research - Unitree's Forte / "RL Robots?" Software Architectures |

**Unitree의 보안 문제** (전부 2025-10-20 · Security Issues?)
- **Andreas Makris**가 백도어를 발견했다. Unitree는 명확한 온프레미스 데이터 솔루션이 없어 **NERC** 규정상 미국 유틸리티 접근이 제한될 수 있다. 정유·가스 회사 일부가 통합업체에 Unitree를 배치하지 않겠다고 통보했고, 반도체 팹 같은 데이터 민감 영역도 반대한다.
- 반면 많은 구매자는 덜 신경 쓴다. 건설·핵심 인프라·보안 순찰에 이미 쓰이고 있고, **미국·EU 경고 이후에도 배치가 이어진다**.

---

## D. 시장 구조

이 절의 항목은 전부 **2025-10-20** 원문이다.

### 두 갈래 전략
- **수직통합(Verticalization)**: 서구 기업들의 길. 소프트웨어·시스템 통합·자율성 대부분을 내재화해 **~2018년부터** 이른 응용을 가능케 했다. 다만 이것도 완전하지는 않다. (2025-10-20 · How Is The Quadruped Market Evolving?)
- **생태계 기반(Ecosystem-based)**: Unitree의 길. 하드웨어 스케일링에 집중하고 소프트웨어와 배치는 연구 커뮤니티·제3자 생태계에 맡긴다. (2025-10-20 · How Is The Quadruped Market Evolving?)
- 원문의 전망: **사족보행 제조사가 완결형 올인원을 만들 것으로 보지 않는다.** 로봇은 하드웨어 플랫폼 역할을 하고 그 위에 외부 솔루션이 계속 얹힌다. 그 결과 **OEM·모델 벤더·시스템 통합업체·소프트웨어 벤더로 갈라진 파편화 시장**이 된다. **응용층 회사가 배치의 대부분을 소유하는 경우가 잦다.** (2025-10-20 · How Is The Quadruped Market Evolving?)

### 세 층이 각각 하는 일
**① 모델 벤더 — 「자율성을 판다」** (전부 2025-10-20 · Model Vendors - Autonomy For Sale)
- L2 자율성의 등장이 열어 준 자리. 자율 스택을 통째로 공급한다.
- **FieldAI** — 사족보행 등 L2 시스템용 「위험 인지(risk-aware)」 파운데이션 모델. 드롭인만으로 여러 환경을 안전하게 주행. 건설 현장, 산업·에너지 플랜트, 보안 순찰 등에서 실동 배치. 두 라운드에 걸쳐 **$400M 초과** 조달.
- **Skild AI** — 보행과 조작을 여러 embodiment에 걸쳐 지휘하는 독자 「brain」. 건설과 보안 순찰에서 배치. 기업가치 **$4.5B**.
- Boston Dynamics와 ANYbotics도 AI 모델을 탐색 중이지만 **현재는 이 전문업체들보다 뒤처져 있다**.

**② 시스템 통합 — 센서와 인프라를 붙인다** (전부 2025-10-20 · System Integration - New Sensors and Infrastructure)
- 고객이 원하는 워크플로에 맞게 사족보행을 구성한다 — 센서·도구 선정, 기존 인프라와의 설치·설정. 고객과 OEM에게서 그 부담을 걷어 간다.
- Boston Dynamics와 ANYbotics는 **성숙한 API/SDK**를 갖춰 통합이 매끄럽지만 **Unitree의 것은 수준이 낮다(subpar)** 고 전해진다.
- 사례: **Chironix**(PilotOS 소프트웨어로 센서를 붙이고 기존 인프라에 연결), **IntuitiveRobots**(Spot에 음향 센서 등 페이로드를 통합하고 데이터를 영상으로 변환), **SUPCON**(중국 통합업체, 사우디아라비아 정유 플랜트 인프라에 사족보행을 성공적으로 통합).
- **아직 통합업체는 「정리(consolidate)」되지 않았다.** **SLB** 같은 대형 플레이어가 이제서야 사족보행 통합을 시작하는 단계다.

**③ 응용층 — 운영을 완성한다** (전부 2025-10-20 · Application Layer - APIs Are Nice, Not Vital)
- 임무 자율성 확정, 로봇(들) 오케스트레이션, 고객용 대시보드를 맡아 장기 운영 효율을 만든다.
- **Lattice**(Anduril) — 로봇 편대(fleet)를 위한 오케스트레이션·계획 층.
- **Formant** — 편대 관리와 텔레메트리. Spot·ANYmal·**Unitree**와 함께 배치되는 사례가 많다.
- ANYbotics와 Boston Dynamics가 API·데이터 수집 플랫폼을 미리 갖춘 초기 우위를 갖지만, Unitree의 인기가 커지면서 **회사들이 Unitree의 열등한 통합 플랫폼에 맞춰 일하는 법을 배우고 있다**.

### 자율성 격차 — 하드웨어 회사가 채우지 못한 것 (전부 2025-10-20 · Autonomy - Not The Full Picture)
자율성에 필요한 셋 — **Planning**(주변을 파악하고 어떤 계획을 따를지), **Navigating**(환경 안에서 적절히 기동), **Positioning**(점검을 안전·정확하게 하도록 자세를 잡기).
- 서구 사족보행의 자체 자율성은 사람·장애물·위험을 피해 경로를 짜고 시설을 안정적으로 이동할 수 **있다**. 그러나 **Positioning은 늘 정밀하지 않아** AprilTag나 과제별 모델이 필요하고, **Planning은 새로운 상황(움직이는 사람 등)에서 멈춰 서거나 나쁜 선택을 하며**, **Navigation은 어수선한 환경에서 취약하다**. 학습된 도메인에서는 잘하지만 새로움에는 약할 수 있다.
- **Unitree의 자체 자율성은 덜 알려져 있으나, 조사에 비춰 보면 지금으로선 사전 프로그래밍된 동작과 원격조작을 크게 넘지 않을 가능성이 크다.**

### 파편화와 하이퍼스케일러 (2025-10-20 · Fragmentation Ensues Without a Hyperscaler)
- 로보틱스에도 「하이퍼스케일러 고객」이 등장하고 있다 — **Amazon의 로봇 100만 대**가 예. 하이퍼스케일러가 들어오면 시장은 대개 소수로 정리된다.
- **사족보행에는 아직 그런 플레이어가 없어 판이 파편화돼 있다.** 등장한다면 Tesla의 Optimus(사내 사용)보다 **AWS처럼 서비스로 파는 형태**일 공산이 크다. 그때까지 Unitree의 하드웨어 우선 전략은 배치의 몫을 계속 떼어 가는 생태계 플레이어들 덕을 본다.
- 하드웨어가 상품화되면 **제3자 벤더가 서구 사족보행 판에서 가장 영향력 있는 세력이 될 수 있다.** (2025-10-20 · Ecosystem Boosts All But Changes The Landscape)

### TAM 수치 — 전부 2025-10-20 기준
| 시장 | TAM | 산출 가정 | 발행일 · 소제목 |
|---|---|---|---|
| **정유·가스**(ATEX 등급 기준) | 도표로만 제시, **본문에 금액 없음** | 전 세계 정유·가스 시설 **~13,168곳**을 용량·부지 기준으로 소형 **60%**·중형 **30%**·대형 **10%** 로 분류. Zone 1 구역은 소형 **약 5개**, 중형 **~10개**, 대형 **약 20개**. 사족보행 1대의 보행 반경 **1.5km** | 2025-10-20 · Oil and Gas TAM |
| **반도체 팹** | **연 매출 약 $397 million** | 배치 **3,312대**, 적격 사이트당 평균 **4~6대**, RaaS **월 $10,000** | 2025-10-20 · Semiconductor Fab TAM |
| **데이터센터** | **연 매출 $247 million** | 북미의 비교적 새로운 하이퍼스케일 시설 **~1,031곳**만 얼리어답터로 가정, 각 **2대**(전기 야드·냉각 인프라 점검), RaaS **월 $10,000** | 2025-10-20 · Datacenter TAM |

- 정유·가스에서는 **대형 정유·가스 회사 한 곳이 Unitree를 선택지에서 제외**했다고 들었고, **Boston Dynamics와 DEEP Robotics는 ATEX 등급을 추진하지 않는다**. 따라서 **ANYbotics가 이 TAM의 주 사업자가 될 수 있다.** (2025-10-20 · Oil and Gas TAM)
- 반도체 팹에서는 **현재 모터가 선단 팹의 엄격한 입자 기준을 맞추지 못할 가능성이 크고**, 하위 팹은 다운타임 비용이 너무 낮아 도입을 정당화하지 못한다. (2025-10-20 · Semiconductor Fab TAM)
- 데이터센터에서는 **ANYbotics·DEEP Robotics·Unitree의 ruggedized 사족보행이 유력 후보**다. (2025-10-20 · Datacenter TAM)

### 참고 — 시장 규모·매출 정리 (전부 2025-10-20 · Setting The Stage / Model Vendors)
| 회사 | 값 |
|---|---|
| Unitree 연매출 | **10억 RMB(~$140M)** 초과 |
| Unitree 2023년 점유율(대수 기준) | **약 70%**(추정) |
| Boston Dynamics 제품군 연매출 | **$100M~$200M** |
| ANYbotics 연매출 | **$27M 미만** |
| DEEP Robotics 배치 | **40개국+ 약 600건** |
| Skild AI 기업가치 | **$4.5B** |
| FieldAI 누적 조달 | **$400M 초과** |

---

## E. 원문이 유보한 것

### 명시적으로 「연구 중」·「모른다」고 밝힌 대목
- **L4는 통째로 「In Research」다.** Unlock도 「In Research」, 2025년 배치·용례도 「In Research」. 본문도 "이는 여전히 연구 영역이므로, 유망한 진전 경로와 예상 함의는 다루되 **망라적 목록은 아니다**"라고 못 박는다. (2025-07-30 · Executive Summary / Level 4: Force-Dependent Tasks 「Looking Forward」)
- **L4의 해법이 데이터 문제인지도 합의가 없다.** "일부는 데이터를 더 넣으면 풀린다고 믿지만, 일부는 이것이 데이터 문제 이상이며 다른 접근이 필요하다고 믿는다." 저자들의 결론은 "힘·토크 센싱과 촉각 센서가 앞으로 해법의 유용한 구성요소일 수 있다고 보지만, **어느 한 접근을 '옳다'고 선언하기엔 매우 이르다**". (2025-07-30 · Open Debates)
- **L3의 다른 직군은 아직 모른다.** 생울타리 손질·조경·가사 같은 역할이 4조건을 채우는 듯 보여도 "**어떻게 될지 말하기에 아직 너무 이르다**". (2025-07-30 · Implications: Low-Skill Labor Replacement)
- **L3의 향방은 「좀 흐릿하다(a bit hazy)」.** 컨퍼런스에서 원격조작→자율 인수를 약속하면서 정작 그 계획은 못 보여 준 회사들을 봤다며, **제3세계 원격조작 노동을 팔면서 자율성 전환 계획이 약할 가능성**을 두고 강하게 검증하라고 쓴다. 또 "**이 과제들에 이족보행 플랫폼이 얼마나 필요한지 우리는 모른다**" — 공장 바닥은 대개 평평하고 어수선하지 않으니 바퀴형이 똑같이 잘할 수 있다. (2025-07-30 · What To Expect)
- **sim2real 격차는 아직 안 풀렸다.** 2015~2022년에는 훨씬 심했고 "**오늘날에도 풀리지 않았다**". (2025-07-30 · Problem 2: Learning to Grasp)
- **VLA가 완전한 해법은 아닐 수 있다.** "정밀한 저수준 제어에는 과제별 모듈/정책이, 반대 힘에 순응하려면 compliant control이 쓰일 수 있고, 다른 방법도 많다". (2025-07-30 · Vision-Language-Action Models)

### 추정치임을 밝힌 값
- **원문의 상당수 도표가 「Source: SemiAnalysis Estimates」다.** L0 통합비 배수 도표, L0 노동 대체 도표, L1 MTTR 도표, L1 전자상거래·소포 경제성 도표 4장, L3 직군 표 (2025-07-30). 사족보행 출하량 추정(GGII Report 병기), 가격 비교 도표, 액추에이터 비교 도표, Go2·B2 BoM 도표 (2025-10-20).
- 표준화된 자동차 솔루션의 통합비를 두고 "**우리는 이것이 로봇 CapEx의 ~70% 정도로 갈 수 있다고 본다(We remark)**". (2025-07-30 · Integration: 4x to 6x The Cost of The Robots Themselves)
- **핵심 인프라 절감액 $350K는 전해 들은 값**이다 — "we've heard quadrupeds have been able to … saving an estimated $350K". (2025-07-30 · Critical Infrastructure)
- **Amazon의 주당 2~4% 이직률도 전해 들은 값** — "we've heard Amazon sees a turnover rate of…". (2025-07-30 · Implications: A Narrow Market of Profitability)
- **Boston Dynamics 매출 $100M~$200M은 「여러 보도 기준(based on various reports)」**, ANYbotics의 $27M 미만은 ZoomInfo 인용, Unitree의 70% 점유율은 「estimated」. (2025-10-20 · Setting The Stage)
- **사족보행 출하량 데이터는 2023년이 마지막 공개 발언**이다 — "The numbers are significantly higher now, but this is the last public statements." 즉 **2025-10-20 시점 글이지만 출하량 수치는 2023년 것**이다. (2025-10-20 · State of The Hardware Market - Unitree's Pricing Advantage)
- **Unitree A2는 「스펙이 덜 알려짐(less specs known)」.** (2025-10-20 · Setting The Stage)
- **Unitree의 자체 자율성은 「덜 알려져 있다(less-known)」** — "judging from our research, it's **likely** not much beyond the pre-programmed actions and teleoperation for now". (2025-10-20 · Autonomy - Not The Full Picture)
- **Unitree의 통합 플랫폼 수준은 「apparently subpar」** — 전언 형태. (2025-10-20 · System Integration - New Sensors and Infrastructure)
- **Boston Dynamics의 비중국산 BoM 요구는 「reportedly」.** (2025-10-20 · Sensors: A Chinese Cost Advantage)
- **A2의 배터리 5시간+ 수치는 온보드 감지·추론 부하를 제외한 값**이라고 원문이 명시한다. (2025-10-20 · Battery Life - Chinese Hardware Prowess)
- **정유·가스 TAM은 대형 정유·가스 회사 한 곳이 Unitree를 뺐다는 「we heard recently」** 에 기대어 ANYbotics를 주 사업자로 지목한다. (2025-10-20 · Oil and Gas TAM)
- **액추에이터 설계는 「향후 별도 글에서 더 깊이 다루겠다」** 고 미뤄 둔다. (2025-10-20 · Actuator Design Is Pivotal)
- **보안 문제의 향방은 미정** — "Security will likely shape which segments Unitree can enter, but **many seem undecided at the moment**". (2025-10-20 · Security Issues?)

### 예측·전망으로 제시된 것(사실이 아님)
- LiDAR가 로봇 Agency 향상에 따라 **흔적기관(vestigial)** 이 될 것이라는 전망, AprilTag 사용이 줄어들 것이라는 전망. (2025-07-30 · What To Expect / Level 2 「Looking Forward」) ※ 석 달 뒤 원문에서는 둘 다 여전히 쓰인다 — F-3 참조
- Boston Dynamics와 Anybotics가 지금 쓰는 **HarmonicDrive**가 더 싸고 backdrivable한 QDD로 바뀔 것이라는 전망. (2025-07-30 · What To Expect)
- 원격조작 감시가 **1:1 → 10:1**로 늘고 결국 자율성이 넘겨받을 것이라는 전망. (2025-07-30 · Looking Forward: Deployments)
- 사족보행 하이퍼스케일러가 등장한다면 **AWS 형태**일 것이라는 전망. (2025-10-20 · Fragmentation Ensues Without a Hyperscaler)
- ANYmal X의 **2026년 상반기(1H26)** 는 예정(slated)이다. (2025-10-20 · ANYBotics Aim: Dirty and Dangerous Environments)

---

## F. 두 원문이 같은 대상을 다르게 말하는 자리

석 달 사이에 값이 갱신되거나 논조가 달라진 대목이다. **나중 = 2025-10-20**.

**F-1. Amazon의 로봇 대수 — 수십만 대 → 100만 대**
- 앞(2025-07-30 · Implications: Efficiency and Dark Factories): Amazon의 **"hundreds of thousands"** 로봇.
- 뒤(2025-10-20 · Fragmentation Ensues Without a Hyperscaler): Amazon의 **"one million robots"**, 로보틱스의 첫 「하이퍼스케일러 고객」 사례로 인용.
- → **나중 값을 쓴다: 100만 대.** 인용 링크는 두 글 모두 Amazon 자사 발표다.

**F-2. 사족보행 배터리 수명 — 평균 90분 → 90분~5시간**
- 앞(2025-07-30 · Deployment and Considerations: Agents In The Open World): "사족보행은 **평균 90분** 배터리라 로봇이나 충전 스테이션을 더 사야 할 수 있다."
- 뒤(2025-10-20 · Battery Life / Drones): 배터리 수명은 **90분~5시간** 범위, Unitree A2는 **5시간 초과**(25kg 적재 시 3시간+). 드론과 비교할 때도 사족보행은 "**수 시간(up to hours)**" 을 버틴다고 쓴다.
- → **90분은 하한이지 평균이 아니다.** 나중 글의 범위를 쓰되, A2 수치는 온보드 추론 부하 제외임을 병기한다.

**F-3. LiDAR와 AprilTag — 「곧 사라진다」 → 「여전히 표준」**
- 앞(2025-07-30 · What To Expect / Level 2 Looking Forward): 로봇 Agency가 오르면 LiDAR는 **흔적기관(vestigial)** 이 되고 AprilTag도 덜 쓰일 것이라는 전망. 단 "당분간은 사족보행에 필수"라고 단서를 단다.
- 뒤(2025-10-20 · Sensors / Autonomy - Not The Full Picture): LiDAR는 여전히 표준 센서 구성(사방 카메라 + 중앙 360° LiDAR + ToF)이고 **Unitree는 오히려 측면 카메라를 빼고 LiDAR에 더 기댄다**. AprilTag도 서구 사족보행의 Positioning이 정밀하지 않아 **여전히 필요**하다.
- → **전망은 아직 실현되지 않았다.** 사라진다는 서술을 현재형으로 쓰지 않는다.

**F-4. L2 사족보행의 자율성 성숙도 — 「초기 양산」 → 「하드웨어 업체는 못 채웠다」**
- 앞(2025-07-30 · Executive Summary / Level 2): 사족보행이 **초기 양산 단계(early production phases)** 에서 점검·데이터 수집을 하고 있고, L2에서 보행이 개선 변곡점에 닿았다.
- 뒤(2025-10-20 · Autonomy - Not The Full Picture): 사족보행 **하드웨어 회사들이 그 잠재력을 온전히 채우지 못한다**. Positioning은 늘 정밀하지 않고, Planning은 새로운 상황에서 흔들리고, Navigation은 어수선한 환경에서 취약하다. Unitree의 자체 자율성은 사전 프로그래밍과 원격조작을 크게 넘지 않을 가능성이 크다.
- → 나중 글은 **자율성의 빈자리를 제3자 모델 벤더(FieldAI·Skild AI)가 메운다**는 구조로 다시 짠다. 「L2가 켜졌다」와 「하드웨어 업체가 L2를 다 못 한다」는 모순이 아니라 층이 다른 이야기다.

**F-5. Nvidia 온보드 컴퓨트 — 「Jetson」 → Thor 2070 TFLOPS**
- 앞(2025-07-30 · Hardware Boosts): 「Nvidia Jetson」이 데이터 처리량을 키웠다는 정도.
- 뒤(2025-10-20 · Key Enablers / "RL Robots?"): **Jetson TX1(2015) 1 TFLOP → Jetson Thor 2070 TFLOPS(FP4)**, Thor는 「최근 출시(recently released)」. 전형적 서구 배치는 **Jetson Orin 1~3개(각 ~50W)**.
- → 컴퓨트 수치는 나중 글에서만 나온다.

**F-6. RaaS 요금 — 앞 글엔 금액이 없다**
- 앞(2025-07-30 · Deployments and Considerations: Robot Coworkers): L3 로봇이 **시간당 임금(RaaS)** 으로 과금한다는 모델만 제시하고 금액은 없다.
- 뒤(2025-10-20): 서구 사족보행 RaaS **월 ~$10K**가 반복 등장하고, 팹·데이터센터 TAM 계산의 단가로 쓰인다.
- → 「$10K/월」은 **L3 조작 로봇이 아니라 L2 사족보행 점검 로봇의 값**이다. 레벨을 섞지 않는다.
