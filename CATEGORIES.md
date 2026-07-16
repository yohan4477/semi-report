# SemiAnalysis 카테고리 분류 체계

이 문서는 `원본 해석/` 문서에 붙이는 카테고리 태그의 유효 목록과 정의를 관리합니다. TRANSFORMATION_RULES.md와 마찬가지로 이 저장소의 단일 소스이며, 카테고리가 추가·변경되면 이 파일을 수정하는 커밋으로 이력을 남깁니다.

## 사용 방식

- 문서 하나가 여러 카테고리에 걸칠 수 있음 (예: 냉각 시스템이 로봇 데이터센터에 미치는 영향 → `ai-infra/cooling` + `robotics`)
- 각 문서 맨 위 YAML frontmatter에 배열로 기록:
  ```yaml
  ---
  categories: [ai-infra/power]
  ---
  ```
- 카테고리는 계층형 슬래시 표기 사용 (예: `ai-infra/power`) — 대분류만 있는 카테고리는 슬래시 없이 그대로 사용 (예: `robotics`)

## 유효 카테고리 목록

### `ai-models` — AI 모델
모델 아키텍처, 학습 방법론, 추론 최적화, 벤치마크 등 AI 모델 자체에 대한 내용. 아래 하위 카테고리로 세분화 (하위 카테고리에 안 맞는 일반적인 모델 내용은 상위 `ai-models` 그대로 사용):

- **`ai-models/agents`** — AI 에이전트 (도구 사용, 멀티스텝 추론, 에이전틱 워크플로우, 오케스트레이션)
- **`ai-models/rl`** — 강화학습 (RLHF, RLVR, 보상 모델링, RL 기반 추론 능력 학습)

### `ai-infra` — AI 인프라
데이터센터·클러스터를 구성하는 물리적·시스템적 인프라. 아래 하위 카테고리로 세분화:

- **`ai-infra/power`** — 전력 시스템 (변압기, UPS, 발전기, 전력망 연계, 온사이트 발전(BTM), 전력 시장·규제)
- **`ai-infra/cooling`** — 냉각 시스템 (공랭·수랭, DLC, 냉각탑, CDU)
- **`ai-infra/compute`** — 연산 (가속기 칩, GPU/TPU/ASIC, 서버 설계)
- **`ai-infra/memory`** — 메모리 (HBM, DRAM, 메모리 대역폭·용량 트렌드)
- **`ai-infra/networking`** — 네트워킹 (NVLink·InfiniBand·이더넷 등 스케일업/스케일아웃 인터커넥트, CPO, 스위치·랙 간 연결 아키텍처) — 컴퓨트 문서에 흔히 곁들여지지만 네트워킹 자체가 문서 상당 분량을 차지하면 이 태그를 `ai-infra/compute`와 함께 이중 부여
- **`ai-infra/business`** — 인프라·컴퓨트를 둘러싼 사업 구조·재무 (조달 전략, 마진, 토큰 지출, 클라우드 파트너십 등 — 하드웨어 스펙보다 비즈니스 축이 중심인 문서)

### `robotics` — 로봇
로봇 하드웨어, 자율주행, 물리 AI 등

### `semiconductors` — 반도체 산업
반도체 설계·제조를 둘러싼 소프트웨어·비즈니스 생태계 (EDA 툴링, IP 라이선싱, 파운드리·팹리스 산업 구조 등) — `ai-infra`가 데이터센터·클러스터의 물리적 인프라를 다루는 것과 달리, 이 카테고리는 칩을 설계·양산하는 산업 자체의 소프트웨어·비즈니스 축을 다룸

## 현재 카테고리별 문서 수

<!-- 문서가 추가/변경될 때마다 이 표를 갱신 -->

| 카테고리 | 문서 수 |
|---|---|
| ai-infra/compute | 19 |
| ai-infra/memory | 9 |
| ai-infra/networking | 7 |
| ai-infra/business | 7 |
| ai-infra/power | 6 |
| ai-infra/cooling | 2 |
| ai-models/rl | 3 |
| ai-models/agents | 2 |
| ai-models | 1 |
| robotics | 1 |
| semiconductors | 1 |

<!-- 2026-07-06 재집계: frontmatter 전수 스캔 기준. [260214] 보조금 전쟁 축약본은 원문이 Drive에 없어 사용자 지시로 전체 삭제(대장·리포트 파생분 포함) — 원문 확보 시 신규 변환으로 재작성 -->
<!-- 2026-07-10: ai-models 하위 카테고리 행 신설 — agents 2편([260206], [260425]), rl 2편([250609], [260107]). 상위 ai-models 행은 하위 미분류 문서용으로 유지 -->
<!-- 2026-07-12: [260205] ECTC 2026 총정리 추가 — ai-infra/memory, ai-infra/compute, ai-infra/cooling 각 +1 -->
<!-- 2026-07-12: [260205] EDA 시장 개관 최초 추가 — 당시엔 ai-infra +1(일반 상위 태그)로 임시 분류, 신규 카테고리 신설은 보류 -->
<!-- 2026-07-12: [260205] 메타 컴퓨트(모두가 네오클라우드가 되고 싶어한다) 추가 — ai-infra +1. 메타의 데이터센터·컴퓨트 조달 전략, 스페이스X식 컴퓨트 판매, 베드락형 제휴, RecSys·MSL 컴퓨트 배분을 다루는 비즈니스/인프라 경제학 문서로, AWS 마진 문서와 동일하게 하드웨어 스펙보다 사업 구조 중심이라 일반 ai-infra 상위 태그로만 분류 -->
<!-- 2026-07-13: [260205] 메타 슈퍼인텔리전스의 미래(1주년 성과 점검) 추가 — ai-infra +1, ai-models/rl +1. 메타의 데이터·인재·컴퓨트 3요소 진단, 5대 타이탄 클러스터·AI-Backbone 네트워킹은 ai-infra(메타 컴퓨트 문서와 자매 관계), RL 환경 스타트업 생태계·3,000명 규모 애플리케이션 AI 엔지니어링 조직 신설은 AI 모델 통합 리포트의 RL 환경 산업화 시계열(§1.2, 머서·서지·핸드셰이크 재등장)과 직접 연결돼 ai-models/rl로 이중 분류 -->
<!-- 2026-07-13: [260205] 토큰 버짓팅(기업들과 나눈 토큰 지출 실태) 추가 — ai-infra +1. 기업 AI 토큰 지출·예산 관리 관행(하드 캡·소프트 리밋), 퍼센타일 고객 매출 집중 구조, 코딩 vertical ARR 비중을 다루는 비즈니스/토큰 경제학 문서로, AWS 마진·메타 컴퓨트 문서와 동일하게 하드웨어 스펙보다 기업 지출·사업 구조 중심이라 일반 ai-infra 상위 태그로만 분류 -->
<!-- 2026-07-16: ai-infra/networking 신규 카테고리 신설(사용자 지시) — 그동안 ai-infra/compute 문서에 네트워킹 내용(NVLink·CPO·InfiniBand·스케일업 아키텍처)이 상당 분량 섞여 있었는데 독립 카테고리가 없었음. 네트워킹 관련어 밀도 기준으로 7편(AWS Trainium3 딥다이브, 베라 루빈, GTC 2026, AMD Advancing AI, 루빈 CPX, InferenceX v2, TPUv7)에 ai-infra/networking 이중 태그 부여, ai-infra/compute 태그는 유지. 이 문서에 ai-infra/business 정의도 함께 보강(기존에 폴더·frontmatter는 있었으나 정의 섹션 누락) -->
<!-- 2026-07-13: 카테고리 문서 수 재검산 — ai-infra 8편(신규 1편 반영). ai-models, memory, compute, cooling, agents, rl, robotics 행은 이번 문서와 무관해 변경 없음 -->
<!-- 2026-07-13: `semiconductors` 신규 대분류 카테고리 신설 (사용자 지시) — [260205] EDA 시장 개관 문서를 ai-infra에서 semiconductors로 재분류·재배치(ai-infra 8→7, semiconductors 0→1). 폴더도 `source/newsletter/ai_infra/`에서 `source/newsletter/semiconductors/`로 이동 -->
<!-- 2026-07-16: [260205] AWS Trainium3 딥다이브 10~16장 완료(9장에서 중단된 상태 재개) — ai-infra/compute 15→16. 스위치 세대 진화·구리케이블/전력/BOM·EFA스케일아웃·마이크로아키텍처·PyTorch 소프트웨어 전환·LNC/Megacore·데이터센터 램프업/TCO까지 전체 16개 섹션 완료 -->
<!-- 2026-07-16: [260205] AMD Advancing AI 13~16장 완료(12장에서 중단된 상태 재개) — ai-infra/compute 16→17. MI400 Flexible I/O·UALoE72, Helios 랙 아키텍처, MI500 UAL256, MI350X/MI355X/MI400 BOM·TCO 비교까지 전체 16개 섹션 완료 -->
<!-- 2026-07-16: [260205] InferenceMAX™(오픈소스 추론 벤치마킹) 신규 변환 완료 — ai-infra/compute 17→18. AMD·Nvidia 7종 칩 대상 처리량·TCO·MW당 토큰처리량 3차원 실측 벤치마크, DeepSeek R1 서빙 전략·CI/CD 인프라·트러블슈팅까지 전체 11개 섹션 완료 -->
<!-- 2026-07-16: [260205] InferenceX v2(엔비디아 블랙웰 vs AMD vs 호퍼, 구 InferenceMAX 후속) 신규 변환 완료 — ai-infra/compute 18→19. 거의 1,000개 GPU 대상 GB300/B300 Blackwell Ultra 최초 벤치마크, AMD 조합성(Composability) 문제 심층분석, MTP·Wide EP·분리형 서빙 원리, 세대별 TCO까지 전체 15개 섹션 완료 -->




## 버전 히스토리

- v1.0 (2026-07-04): 초기 카테고리 체계 수립 — ai-models, ai-infra(power/cooling/compute/memory), robotics
  - 기존 5개 문서를 소급 분류한 결과 전부 ai-infra/power(전력 시스템)에 해당, 냉각 시스템(Part 2)만 유일하게 ai-infra/cooling 추가 해당 — 현재 코퍼스가 전력 인프라에 편중되어 있음을 확인
