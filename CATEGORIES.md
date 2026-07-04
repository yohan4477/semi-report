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

### `robotics` — 로봇
로봇 하드웨어, 자율주행, 물리 AI 등

## 현재 카테고리별 문서 수

<!-- 문서가 추가/변경될 때마다 이 표를 갱신 -->

| 카테고리 | 문서 수 |
|---|---|
| ai-infra/power | 5 |
| ai-infra/cooling | 1 |
| ai-infra/compute | 1 |
| ai-infra/memory | 0 |
| ai-models | 0 |
| robotics | 0 |

## 버전 히스토리

- v1.0 (2026-07-04): 초기 카테고리 체계 수립 — ai-models, ai-infra(power/cooling/compute/memory), robotics
  - 기존 5개 문서를 소급 분류한 결과 전부 ai-infra/power(전력 시스템)에 해당, 냉각 시스템(Part 2)만 유일하게 ai-infra/cooling 추가 해당 — 현재 코퍼스가 전력 인프라에 편중되어 있음을 확인
