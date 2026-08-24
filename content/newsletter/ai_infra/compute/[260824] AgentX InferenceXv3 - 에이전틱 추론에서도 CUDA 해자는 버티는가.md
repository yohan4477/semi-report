---
categories: [ai-infra/compute, ai-infra/networking, ai-models/agents]
---

# AgentX - InferenceXv3: Does CUDA Moat Hold up in Agentic Inferencing?

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat)
> **저자**: Cam Quilici, Bryan Shan, Alec Ibarra
> **발행일**: 2026-08-24

---

## 📑 목차

### 전체 섹션
 1. [서론 - AgentX 1.0 공개와 에이전틱 추론의 부상](#1-서론---agentx-10-공개와-에이전틱-추론의-부상)
 2. [에이전틱 워크로드란 무엇인가](#2-에이전틱-워크로드란-무엇인가)
 3. [모델별 에이전틱 코딩 추론 성능](#3-모델별-에이전틱-코딩-추론-성능)
 4. [업계 파급력 - 분산 추론 생태계와 50개+ 상류 PR](#4-업계-파급력---분산-추론-생태계와-50개-상류-pr)
 5. [컨텍스트 병렬화와 vLLM·SGLang 최적화](#5-컨텍스트-병렬화와-vllmsglang-최적화)
 6. [TensorRT-LLM·AMD ATOM·AITER 최적화](#6-tensorrt-llmamd-atomaiter-최적화)
 7. [Dynamo·LMCache·Mooncake 최적화와 그 밖의 개선](#7-dynamolmcachemooncake-최적화와-그-밖의-개선)
 8. [AgentX 방법론 - 300만 달러 데이터셋과 트레이스 리플레이어](#8-agentx-방법론---300만-달러-데이터셋과-트레이스-리플레이어)
 9. [InferenceX/AgentX 다음 단계](#9-inferencexagentx-다음-단계)
10. [모델 수명주기 전체로 본 성능 - 적분 관점](#10-모델-수명주기-전체로-본-성능---적분-관점)
11. [단일 턴(8k1k) 성능 - 시간에 따른 개선](#11-단일-턴8k1k-성능---시간에-따른-개선)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **에이전틱 워크로드(Agentic Workload)**: 챗봇처럼 한두 번 묻고 답하는 게 아니라, 모델이 코드를 실행하고 도구를 부르고 수십\~수백 번 대화를 이어가며 작업을 끝까지 수행하는 방식 — 대화가 길어질수록 이전 맥락을 재활용하는 비중이 커진다
- **KV 캐시와 프리픽스 재사용(Prefix Reuse)**: 이전 대화 턴에서 계산해둔 결과(KV 캐시)를 다음 턴에서 다시 계산하지 않고 그대로 재사용하는 것 — 에이전틱 대화는 turn이 쌓일수록 재사용 비율이 1(=100%)에 가까워진다
- **PD 분리(Prefill-Decode Disaggregation, PDD)**: 입력을 한번에 처리하는 프리필(prefill)과 토큰을 하나씩 뽑아내는 디코드(decode)를 서로 다른 GPU 묶음에 맡겨 처리하는 방식 — 성격이 다른 두 작업을 분리해 각각 최적화한다
- **컨텍스트 병렬화(Context Parallelism, PCP/DCP)**: 하나의 긴 입력·캐시를 여러 GPU에 쪼개 나눠 처리하는 기법 — 프리필 단계에 쓰면 PCP, 디코드 단계에 쓰면 DCP라 부른다
- **TTFT·TPS(TPOT) - 상호작용성 지표**: TTFT(Time To First Token)는 질문 후 첫 글자가 나오기까지 걸리는 시간, TPS(초당 사용자당 토큰 수)는 그 이후 얼마나 빨리 이어지는지를 나타내는 지표 — 이 둘은 종종 한쪽을 올리면 다른 쪽이 나빠지는 트레이드오프 관계
- **TCO(Total Cost of Ownership, 총소유비용)**: 칩 구매비뿐 아니라 전력·운영까지 합친 실제 총비용 — SKU 간 성능을 비교할 때 가격이 아니라 이 TCO로 정규화해서 비교한다
- **8k1k 고정 시퀀스 벤치마크**: 입력 8,000토큰·출력 1,000토큰으로 고정한 옛날 방식 성능 측정 — 프리픽스 재사용이나 세션 상태를 반영하지 못해 지금의 실제 트래픽과는 다르지만, 칩·커널 자체의 기초 성능을 보는 데는 여전히 쓸모가 있다
- **DAG 트레이스 리플레이(서브에이전트 구조)**: 하나의 에이전틱 세션을 요청들이 서로 의존하는 방향성 비순환 그래프(DAG)로 표현해 재생하는 방식 — 메인 에이전트가 여러 서브에이전트를 동시에 띄우고 다시 합류하는 구조까지 그대로 재현한다

---

## 1. 서론 - AgentX 1.0 공개와 에이전틱 추론의 부상

**📌 핵심:**
- 2025년 11월 「클로드 코드 변곡점」이후 긴 맥락·멀티턴 에이전틱 워크로드가 급증해 지금은 실제 운영 추론 트래픽의 대부분을 차지한다 — 2026년 4월 OpenAI의 기업용 에이전틱 지출이 챗GPT 지출을 넘어섰다
- SemiAnalysis는 300만 달러 이상을 들여 만든 데이터셋을 통째로 공개하며, 세계 최초로 100% 오픈소스인 멀티턴 에이전틱 코딩 추론 벤치마크 "AgentX 1.0"(1백만 토큰 맥락까지, Apache 2.0 라이선스)을 발표한다
- 전체 측정은 약 2메가와트(MW) 규모 컴퓨트를 1,000개 이상의 칩(MI355X·GB300 NVL72·GB200 NVL72·B300·B200·MI325·MI300X·H200·RTX Pro 서버 등)에 걸쳐 상시 가동해 진행했고, 루빈(Rubin)은 이달 말, TPU와 MI455X UALoE72는 올해 안에 추가될 예정이다
- 결론: 공개 첫 몇 달 만에 이 벤치마크를 기준점(north star)으로 삼아 vLLM·SGLang·TensorRT-LLM·ATOM·AITER·Dynamo·LMCache·Mooncake 등에 70여 개의 상류(upstream) 코드 개선(PR)이 올라갔다는 것 자체가 초기 성능 수치보다 더 큰 성과다

---

```mermaid
flowchart TD
    Trigger["2025-11 클로드 코드 변곡점<br/>이후 멀티턴 에이전틱 트래픽 급증"] --> Now["2026-04 OpenAI 기업용<br/>에이전틱 지출이 챗GPT 지출 추월"]
    Now --> AgentX["AgentX 1.0 공개<br/>(1M 맥락, Apache 2.0, 완전 오픈소스)"]

    style AgentX fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    Scale["측정 규모"] --> Power["약 2MW 상시 가동"]
    Scale --> Chips["칩 1,000개+<br/>MI355X·GB300·GB200·B300·B200·<br/>MI325·MI300X·H200·RTX Pro"]
    Scale --> Roadmap["루빈 이달 말·<br/>TPU/MI455X UALoE72 연내 추가"]

    style Chips fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

이 벤치마크는 오픈소스치고 이례적으로 스택 대부분을 공개한다 — 프런트엔드, 여러 1티어 AI 랩의 컴퓨트 확보 계획팀이 이미 쓰고 있는 공개 REST API 데이터베이스, GitHub Actions CI 증빙, 로그, 모든 데이터 포인트에 대한 정확도 검증까지 전부 열려 있다. 벤치마크 설정은 recipes.vllm.ai와 SGLang 쿡북의 상류(upstream) 이미지를 그대로 따라가, 실제 고객이 체감하는 성능을 측정하지 벤치마크용으로 특별 튜닝된(benchmax'ed) 이미지를 측정하지 않는다. 3\~4주 안에 AMD·Nvidia 최신 결과를 담은 후속 업데이트 기사가 나올 예정이다.

이번 릴리스는 Inferact/vLLM, RedHat/llm-d, RadixArk/SGLang, LMCache/TensorMesh, Weka, Mooncake 관리팀, AMD, Nvidia, Anthropic 직원, GitHub 등 다수 오픈소스 파트너의 기여로 완성됐고, 메타·마이크로소프트·오라클·OpenAI·미니맥스·문샷 Kimi·알리바바 Qwen·즈푸 GLM도 이 오픈소스 이니셔티브를 지지한다고 공개적으로 밝혔다.

---

## 2. 에이전틱 워크로드란 무엇인가

**📌 핵심:**
- 에이전틱 워크로드는 네 가지로 정의된다: ① 멀티턴(세션 하나에 수십\~수백 번의 대화), ② 긴 맥락(시스템 프롬프트·도구 정의·turn 누적으로 맥락이 빠르게 쌓임), ③ 높은 프리픽스 재사용(turn n-1의 출력이 turn n에 이어붙으며 재사용 비율이 1에 수렴), ④ 서브에이전트 버스트(짧게 살다 사라지는 서브에이전트가 새 맥락으로 뜨며 캐시 사용량이 들쭉날쭉해짐)
- 이 네 특징 때문에 에이전틱 추론은 칩 하나의 커널 성능 문제가 아니라 "시스템 문제"가 된다 — 재사용률이 워낙 높아 KV 텐서를 노드·랭크 사이에 효율적으로 옮겨야 하고(NIXL·MORI-IO·Mooncake), 어느 노드에 필요한 프리픽스가 있는지에 맞춰 대화를 라우팅해야 하며(LLM-d·Dynamo·vLLM/SGLang 라우터), 긴 맥락이 HBM(고대역폭메모리) 용량을 압박해 DRAM·SSD로 캐시를 내려보내는(오프로드) 작업까지 효율적으로 처리해야 한다(Mooncake Store·LMCache·vLLM Simple Offloading·SGLang HiCache)
- 반대로 옛날 방식인 고정 길이·단일 턴 벤치마크는 프리픽스 재사용이 의미가 없어 순수하게 칩·커널 기초 성능만 보여준다 — 여전히 유용한 기준점이지만 지금의 실제 트래픽과는 다르다
- 결론: 이런 실전 트래픽을 재현하기 위해 SemiAnalysis 내부의 익명화된 클로드 코드 트레이스 393개를 수집해 AIPerf로 원래의 요청 스케줄대로 재생했고, 이 데이터셋을 가능하게 하려 앤트로픽과 협력해 클로드 코드 기능 2건(GitHub 이슈 #49207, #66761)을 함께 출시했다

---

```mermaid
flowchart TD
    Agentic["에이전틱 워크로드 4대 특징"] --> MT["멀티턴<br/>세션당 수십~수백 회 대화"]
    Agentic --> LC["긴 맥락<br/>턴이 쌓일수록 급증"]
    Agentic --> PR["높은 프리픽스 재사용<br/>재사용률 → 1"]
    Agentic --> SB["서브에이전트 버스트<br/>캐시 사용량 급변"]

    style PR fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    SysProblem["에이전틱 추론 = 시스템 문제"] --> Transfer["KV 텐서 노드 간 전송<br/>(NIXL·MORI-IO·Mooncake)"]
    SysProblem --> Route["프리픽스 위치 기반 라우팅<br/>(LLM-d·Dynamo·vLLM/SGLang 라우터)"]
    SysProblem --> Offload["HBM 압박 → DRAM/SSD 오프로드<br/>(Mooncake Store·LMCache·HiCache)"]

    style SysProblem fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    Dataset["실전 트레이스 확보"] --> Collect["SemiAnalysis 내부<br/>익명화 클로드 코드 트레이스 393개"]
    Collect --> Replay["AIPerf로 원래 요청<br/>스케줄대로 재생"]
    Replay --> Anthropic["앤트로픽과 협력<br/>클로드 코드 기능 2건 공동 출시"]

    style Dataset fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

---

## 3. 모델별 에이전틱 코딩 추론 성능

**📌 핵심:**
- 프론티어 랩들은 추론 코딩 성능을 볼 때 상호작용성(TPS) 대비 달러당 성능, TTFT, 종단간(e2e) 작업 완료율 세 가지를 본다 — 메가와트당 성능도 중요한데, 자금은 랩들에게 사실상 무제한이지만 전력은 물리적으로 구하기 어려운 자원이기 때문
- DeepSeek V4 Pro(1.6조 파라미터), Kimi K3(2.8조 파라미터), MiniMax M3(432B), Qwen3.5(397B), GLM 5.3(744B 기반) 다섯 개 프론티어 모델에서 엔비디아와 AMD 모두 강점을 보이는 영역이 갈렸다
- MI355X 오픈소스(vLLM)는 AMD 자체 엔진 ATOM보다 대체로 뒤처지는데, 이는 ATOM이 중국·서구 대부분의 AI 랩에서 실제 상용 서비스에 쓰이지 않기 때문에(알리바바 소규모 광고 사업부 한 곳 제외) 실질적인 비교 기준은 여전히 vLLM이라는 점이 중요하다
- 결론: 2026년 8월 21일을 기점으로 vLLM 최적화(Inferact·엔비디아)가 반영되며 B200의 달러당 성능이 MI355X를 다시 앞질렀다 — 몇 주 전까지는 MI355X SGLang이 B200 vLLM과 비슷한 수준까지 따라붙었던 접전 구도였다

---

```mermaid
flowchart TD
    Metrics["프론티어 랩이 보는<br/>추론 성능 3대 지표"] --> PerfDollar["달러당 성능<br/>(TPS 대비)"]
    Metrics --> TTFTm["TTFT<br/>(첫 토큰까지 시간)"]
    Metrics --> E2E["종단간(e2e)<br/>작업 완료율"]

    style Metrics fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

### DeepSeek V4 Pro 0813 (1.6조 파라미터, 활성 490억)

DeepSeek V4 Pro의 요청 분포는 입력 길이(ISL) 중앙값 8만 8천 토큰(p90 27만 2천, p99 67만 5천), 출력 길이(OSL) 중앙값 413토큰(p90 2,200, p99 8,600)으로, 실전 서비스에서 "적정" p90 TTFT는 보통 200\~5,000ms이며 5\~10초를 넘으면 "온라인 추론"의 경계를 벗어난다.

```mermaid
flowchart TD
    Before["2026-08-21 이전:<br/>MI355X SGLang ≈ B200 vLLM<br/>(달러당 성능 대등)"] --> After["2026-08-21 이후:<br/>vLLM 최적화(Inferact·Nvidia)<br/>반영 → B200이 재역전"]
    After --> Still["단, B300 vLLM·B200 SGLang은<br/>줄곧 MI355X보다 우위"]

    style After fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

AMD 분산추론(DI)팀은 6개월간 8k1k 시나리오를 개선했지만 아직 실전 워크로드엔 부족하다 — 1xDEP8+1xDEP8 분리형 구성은 고처리량 구간에서 소폭 개선에 그치고 저지연 구간에서는 오히려 더 나빠지며, SGLang의 `--enable-prefill-delayer`(동시 요청 64 이상에서 프리필을 최대 30 순전파까지 미뤄 배치를 더 채우는 옵션)와 청크 프리필 크기 확대(8,192→65,536)가 처리량은 올리지만 p90 TTFT를 크게 악화시킨다. 종단간 지연 기준으로는 ATOM MI355X가 B200 vLLM을 이기지만(B300·B200 SGLang은 못 이김), ATOM은 미완성 기능이 많아 알리바바 소규모 광고 사업부 한 곳 외엔 중국·서구 어느 AI 랩도 상용에 쓰지 않는다 — Qwen 본진도 ATOM을 쓰지 않는다.

엔비디아 쪽 최강 조합은 GB300 Dynamo TRTLLM과 GB200 Dynamo vLLM으로, 둘 다 PD 분리(프리필-디코드 분리)로 합리적 상호작용성에서 높은 처리량을 뽑고, GB300은 wide-EP(DEP32) 디코드 구성까지 더해 프론티어 중간 구간 처리량을 끌어올린다. GB300은 더 높은 동시성을 달성하는 만큼 서브에이전트 트래픽·콜드 프리필도 늘어 TTFT가 더 민감하게 반응한다.

```mermaid
flowchart TD
    ServerMetric["384 동시 에이전틱 트레이스<br/>서버 지표(AgentX 신규)"] --> B300m["B300 vLLM DEP8 + 3TB DRAM<br/>HBM 캐시 적중률 91% + DRAM 1.36%<br/>(HBM KV 작업셋 ≈4,300만 토큰)"]
    ServerMetric --> B200m["B200 동시성 196<br/>HBM 캐시 적중률 73% + DRAM ≈20%<br/>(HBM KV 작업셋 ≈2,200만 토큰, B300의 절반)"]

    style B300m fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

B300이 B200 대비 HBM 용량 50% 더 많아 TCO 정규화 처리량은 비슷해도 B300이 여분의 처리량을 "짜낼" 수 있는 이유가 여기 있다. DRAM KV 오프로드는 쓰기 유지(write-through) 캐시라서 DRAM 용량이 HBM KV 캐시 용량의 1.5\~3배는 돼야 효과가 크다. H200 SGLang FP8은 저동시성에서는 B200/MI355X SGLang과 맞먹는 달러당 성능을 내지만 HBM이 적어 고처리량 구간에선 신형 SKU를 못 따라가고, 동시성이 오르면 DRAM 오프로드 의존도가 커져 지연시간이 비합리적으로 치솟는다. 종합하면 MI355X는 텐서 병렬화와 기초 커널만 쓰는 저처리량·저지연 구간에서 가장 경쟁력 있고, AMD는 B200 대비 1.5배 많은 HBM을 가진 만큼 고처리량 구간에서 DEP 커널 최적화가 더 필요하다.

### Kimi K3 (2.8조 파라미터)

Kimi K3는 클로드의 Mythos/Fable5와 비슷한 파라미터 규모의 오픈 웨이트 프록시 모델로 쓰인다. 워낙 커서 B200 서버 한 대에 다 안 들어가 wide EP/TP나 파이프라인 병렬화가 필수인데, vLLM에서 추측 디코딩(DSpark)이 파이프라인 병렬화와 최근까지 전혀 호환되지 않아 B200 성능이 참담했고 MI355X에 완전히 밀렸다.

```mermaid
flowchart TD
    K3["Kimi K3 (2.8T)"] --> B200issue["B200: 추측디코딩+파이프라인병렬<br/>비호환(최근까지) → 성능 참담"]
    K3 --> MI355issue["MI355X vLLM: 짧은 맥락은 day 0<br/>작동, 긴 맥락·멀티턴은 첫 주<br/>AITER/Triton 커널 먹통"]
    K3 --> HopperIssue["Hopper(H100/H200):<br/>K3 전용 튜닝 커널 부재로<br/>서빙 자체가 버거움"]

    style B200issue fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style MI355issue fill:#fff7ed,stroke:#ea580c
```

AMD가 ATOM으로 K3 성능을 빠르게 밀어붙이는 건 고무적이지만 vLLM 상류 반영을 더 우선해야 한다는 게 저자들 견해다 — ATOM이 AMD의 현재 최고 성능 엔진이긴 해도, 상류 오픈소스 스택을 쓰는 고객에게는 vLLM 비교가 더 의미 있다. 종단간 지연 40\~60초 구간에서는 MI355X ATOM이 GB300 NVL72 vLLM의 달러당 성능마저 앞선다.

### MiniMax M3(432B), Qwen3.5(397B), GLM 5.3

```mermaid
flowchart TD
    M3["MiniMax M3 432B"] --> NvWin["엔비디아 압도적 우위<br/>(AMD 소프트웨어 특히 긴 맥락에서 부진)"]
    M3 --> B300Crown["B300 TRT-LLM TP2가<br/>M3 성능 1위"]
    M3 --> RackVsFlat["B200/B300(평판형)이<br/>GB200/GB300(랙스케일)보다<br/>TCO 정규화 처리량 우위"]

    style NvWin fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

M3에서 AMD가 부진한 건 AMD 엔지니어링 리더십이 짧은 맥락·단일 턴 튜닝에만 인센티브를 걸고 긴 맥락·멀티턴을 등한시했기 때문이라고 저자들은 지적한다. GB200 동시성 40에서 TP4/EP4/DPA 구성은 일반 TP4 대비 처리량이 0.60배에 그치면서 p90 TTFT는 3배 넘게 나빠지고, 동시성 32에서는 이론상 96.0%여야 할 캐시 적중률이 실제로는 28.8%에 그친다 — DP 랭크마다 캐시 풀의 4분의 1씩 독점하는 구조라 30만 토큰짜리 세션이 엉뚱한 랭크에 다시 배정되면 전부 다시 계산해야 하기 때문이다. B200/B300이 랙스케일 GB200/GB300보다 TCO 정규화 처리량에서 앞서는 이유는 Dynamo 라우터가 살아있는 프리픽스 수·길이에 비례해 일이 늘어나는 병목이 되고, wideEP·wide DCP·wide TP용 튜닝된 커널이 아직 없어 TCO가 더 높은 랙스케일 쪽이 성능/TCO에서 불리하게 나오기 때문이다. 엔비디아 Pareto 최적점은 모두 동시성 20 이상에서 KV 오프로드를 쓰는 반면 AMD는 전혀 안 쓰는데, AMD vLLM의 GPU-CPU 전송용 hipMemcpyBatchAsync API가 ROCm 7.14까지 빠져 있어 오프로드 자체가 비효율적이었기 때문이다.

```mermaid
flowchart TD
    Qwen["Qwen3.5 397B<br/>(GatedDeltaNet 어텐션)"] --> QwenNv["Nvidia SGLang 독주<br/>90 tok/s/user에서 20배+ 우위<br/>AMD 경쟁작 전무"]
    GLM["GLM 5.3<br/>(GLM5.2 744B 기반)"] --> GLMNv["150 tok/s/user에서<br/>Nvidia 비용효율 최대 5배<br/>(AMD 칩이 공짜여도 Nvidia가 더 쌈)"]
    GLM --> GLMAtom["단, ATOM은 특정 구간에서<br/>GB300 NVL72 SGLang·TRTLLM보다<br/>달러당 성능 우위"]

    style QwenNv fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style GLMAtom fill:#f0fdf4,stroke:#16a34a
```

Qwen3.5는 GatedDeltaNet(MIT·엔비디아 리서치가 개발, 상태 저장 요구량이 일정해 일반 어텐션의 선형 증가 구조보다 메모리를 덜 씀)을 몇 층마다 섞어 쓰는 구조로, 네이티브 최대 맥락이 26만 2천 토큰이라 25만 6천 토큰으로 자른 데이터셋을 쓴다. H100 대비 B300 FP4는 12배 나은 달러당 성능을 낸다. GLM 5.3은 GLM5.2 744B에 추가 후속 학습을 더한 프론티어급 모델로, 여기서도 엔비디아가 SGLang에서 AMD를 크게 앞서지만 ATOM 구간에서는 AMD가 반격한다. 저자들은 TTFT와 상호작용성(TPS)을 하나로 합친 실험적 지표 "E2E Normalized Interactivity"(OSL÷E2EL)를 처음 소개하는데, 아직 PD 분리 같은 세부 최적화 효과를 완전히 반영하지 못하는 초기 버전임을 명시한다.

---

## 4. 업계 파급력 - 분산 추론 생태계와 50개+ 상류 PR

**📌 핵심:**
- AgentX가 첫 몇 달 만에 만든 가장 큰 성과는 벤치마크 수치 자체가 아니라, 이를 기준점 삼아 실전 에이전틱 워크로드를 최적화한 50개 이상의 상류(upstream) 코드 개선(PR)이다 — KV 캐시 생애주기·하이브리드 어텐션 캐시 정확성·CPU 오프로드·전송 진행 상태·라우팅 적합성·토큰화·스케줄러 장부까지 전 구간을 건드렸다
- SemiAnalysis는 AMD 소프트웨어 개발팀과 수년간 협업하며 개발 원칙 현대화를 도왔는데, 이번 AgentX 작업이 AMD 오픈소스를 에이전틱 워크로드에서 "일급(first class)"에 가깝게 끌어올리는 데 결정적이었다
- 분산 추론 스택은 라우터(요청을 워커로 분배) → 추론 엔진(vLLM·SGLang 등, 실제 연산+외부 KV 캐시 매니저 연결) → KV 캐시 매니저·전송 엔진(Mooncake·NIXL 등, GPU\~CPU\~원격노드 간 실제 데이터 이동)의 3단 구조이며, Dynamo·llm-d·AMD Infera 같은 플랫폼이 이 구성요소들을 묶어 쿠버네티스 위에서 배포 가능한 하나의 시스템으로 패키징한다
- 결론: 컨텍스트 병렬화(긴 입력·캐시를 여러 GPU에 쪼개 나누는 기법)는 엔비디아 리서치가 상당 부분 발명했는데, vLLM 지원 매트릭스에서 AMD 백엔드는 전부 미지원 상태라 CUDA 해자의 일부를 이룬다 — 다만 아래 5\~7장에서 보듯 AMD 진영도 빠르게 따라붙고 있다

---

```mermaid
flowchart TD
    Stack["분산 추론 스택 3단 구조"] --> Router["① 라우터/프런트엔드<br/>(vLLM router·llm-d router·<br/>SGLang gateway·ATOM Mesh)"]
    Router --> Engine["② 추론 엔진<br/>(vLLM·SGLang·TensorRT-LLM·ATOM)"]
    Engine --> KVMgr["③ KV 캐시 매니저·전송엔진<br/>(Mooncake·NIXL·LMCache)"]

    style Stack fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

```mermaid
flowchart TD
    Package["패키징 플랫폼"] --> Dynamo["엔비디아 Dynamo"]
    Package --> LLMD["llm-d"]
    Package --> Infera["AMD Infera"]
    Dynamo --> K8s["쿠버네티스 위에서<br/>컨테이너 묶음으로 배포·조율"]

    style K8s fill:#f0fdf4,stroke:#16a34a
```

```mermaid
flowchart TD
    CP["컨텍스트 병렬화<br/>(PCP=프리필용, DCP=디코드용)"] --> Origin["대부분 엔비디아 리서치가 발명"]
    CP --> Gap["vLLM 지원매트릭스:<br/>AMD 백엔드 전부 미지원"]
    Gap --> Moat["CUDA 해자의 한 축<br/>(단, 5~7장에서 AMD 추격 확인)"]

    style Gap fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

한 예로 현재 AgentX 결과에 쓰이는 단순 배치는 vLLM과 같은 노드에서 Mooncake를 함께 돌리는 방식이다 — 각 vLLM 워커가 Mooncake Store 클라이언트를 내장해 호스트 DRAM 일부를 외부 KV 캐시 풀에 내주고, 재사용 가능한 KV 블록을 GPU 메모리로 불러오거나 새로 계산한 블록을 호스트 메모리에 저장한다. 한 배포 안에서 Mooncake Store로 재사용 블록을 DRAM에 내리는 동시에, NIXL로 프리필-디코드 GPU 사이의 요청별 KV를 직접 옮기는 식으로 여러 전송 경로가 공존할 수 있다.

---

## 5. 컨텍스트 병렬화와 vLLM·SGLang 최적화

**📌 핵심:**
- 8k처럼 짧은 고정 길이 요청은 나눌 것도 별로 없고 TTFT도 이미 짧아 컨텍스트 병렬화의 이점을 살릴 수 없다 — 긴 맥락에서만 프리필 병렬화(PCP, 연산 집약적인 프리필을 여러 랭크에 쪼개 처리)와 디코드 병렬화(DCP, 메모리 대역폭에 묶인 디코드를 KV 샤드별로 병렬 스캔)가 진가를 발휘한다
- vLLM에서 가장 큰 개선은 하이브리드 어텐션 프리픽스 캐싱이다 — 슬라이딩 윈도우(짧게 쓰고 버리는 최근 맥락 캐시)가 긴 맥락 체크포인트를 밀어내지 못하게 막는 "선택적 보존" 기법이 동시 요청 14개·맥락 100만 토큰까지 프리픽스 캐시 적중률 95% 이상을 기록했고, DeepSeek-V4 하이브리드 어텐션용 CPU 오프로드 확장은 출력 처리량 81.7% 증가·평균 종단간 지연 46.6% 감소를 냈다
- SGLang은 슬라이딩 윈도우와 프리픽스가 같은 메모리 풀을 두고 경쟁하는 문제를 세 가지 각도로 풀었고(선제적 페이지 해제·컴퓨트 락 상한·유효기간 지난 항목 제거), 맥락 길이를 컴파일 대상이 아니라 런타임 변수로 처리해 AgentX 동시성 384에서 출력 처리량 26.75% 증가·평균 TTFT 36.25% 감소를 달성했다
- 결론: SGLang의 DP 캐시 어피니티(세션을 해당 캐시를 쥔 랭크에 고정 배정)와 라우팅 정확성 개선은 실측으로 정확도 문제까지 드러냈다 — 12만 7,500토큰 공유 프리픽스 테스트에서 정답 "니들"을 128개 중 2개만 찾던 것을 128개 전부 찾도록 고쳤고, 이 수정이 GB300에서 사용자당 출력 처리량 9.6%↑, 이어진 후속 수정이 사용자당 처리량 18.0%↑·GPU당 디코드 처리량 12.7%↑까지 이끌었다

---

```mermaid
flowchart TD
    VLLMFix["vLLM 핵심 개선"] --> Retention["선택적 보존<br/>동시 14요청·맥락 1M에서<br/>프리픽스 적중률 95%+"]
    VLLMFix --> Offload["DeepSeek-V4 하이브리드<br/>CPU 오프로드 확장<br/>처리량 +81.7%·지연 -46.6%"]

    style Offload fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    SGLangFix["SGLang 핵심 개선"] --> Window["슬라이딩윈도우 vs 프리픽스<br/>메모리 경쟁 3중 해소"]
    SGLangFix --> Runtime["맥락 길이 런타임 변수화<br/>동시성 384: 처리량 +26.75%<br/>TTFT -36.25%"]
    SGLangFix --> Affinity["DP 캐시 어피니티<br/>127.5k 프리픽스 정확도<br/>2/128 → 128/128"]

    style Affinity fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Runtime fill:#f0fdf4,stroke:#16a34a
```

SGLang은 또한 HiCache(자체 오프로딩 기능)에서 전체 어텐션 캐시만 옮기고 슬라이딩 윈도우 꼬리는 되돌아올 때 재구성하는 비대칭 전략을 쓰고, FlashInfer GDN 체크포인트로 순환 상태(recurrent state)까지 프리픽스 재사용에 참여시켜 처리량을 초당 GPU당 47,771에서 53,004토큰(캐시 적중률 92.4%)으로 끌어올렸다. 스케줄러 레벨에서는 프리필 우선 결정이 반복돼 디코드가 굶주리는 문제를 프리필 이후 디코드 라운드를 강제하는 방식으로 고쳐, DeepSeek V4 Pro에서 출력 처리량 141%↑·p99 토큰 간 지연 97.3%↓를 얻은 대신 TTFT 중앙값이 36.5초에서 59초로 늘어나는 트레이드오프도 함께 드러났다.

---

## 6. TensorRT-LLM·AMD ATOM·AITER 최적화

**📌 핵심:**
- TensorRT-LLM은 매 턴마다 대화 전체를 다시 토큰화하는 낭비를 없애는 "경계 인식 증분 토큰화"를 도입해 Qwen3.5 트레이스 1,087건 전환에서 전량 정확도를 유지하며 평균 처리시간을 185.1ms에서 11.3ms로 줄였고, MiniMax-M3의 분리형 KV 전송 조각화 문제(수천 개의 작은 전송으로 쪼개지던 것)를 정리해 동시성 5에서 KV 지연 p99를 26.74초→125ms, 동시성 40에서 10.15초→288ms로 단축했다
- AMD ATOM 엔진은 원래 단일 턴 전용으로 설계돼 있었는데, 슬라이딩 윈도우 꼬리를 살려두는 희소 체크포인트 보존을 도입해 동시성 48에서 실제 프리픽스 적중률을 5.6%→96.45%로 끌어올렸다(9건 중 9건이 캐시는 있는데 윈도우 게이트에서 버려지고 있었다는 뜻) — 다만 체크포인트를 무조건 남기면 재방문 없는 트래픽에서 처리량이 17.5% 깎여, 토큰 간격을 두고 남기는 식으로 이 손실을 없앴다
- ATOM의 청크형 파이프라인 프리필은 GLM-5.2 고부하 조건에서 출력 처리량 2배, TTFT 중앙값 28.6초→8.7초, 프리필 GPU 한 대가 보유하는 KV 블록 수 3.68배 증가라는 가장 완결된 성과를 냈고, 프리필 컨텍스트 병렬화(PCP)는 입력 6만 4천 토큰에서 평균 TTFT 35\~43%↓·총처리량 최대 49%↑를 기록했다
- 결론: 저수준 커널(AITER)에서는 대형 KV 캐시 풀이 32비트 오프셋 한계(약 1억 5천만 행을 넘으면 주소가 조용히 틀어지는 문제)를 실제로 노출시켜, DeepSeek-V4 통합 캐시 경로 전체에 64비트 주소 지정을 적용해 잘못된 행을 읽고 쓰는 사고를 막았다

---

```mermaid
flowchart TD
    TRT["TensorRT-LLM 핵심 개선"] --> Token["경계인식 증분 토큰화<br/>185.1ms → 11.3ms"]
    TRT --> KVfix["M3 분리형 KV 전송 정리<br/>p99 지연 26.74초 → 125ms<br/>(동시성 5)"]

    style Token fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style KVfix fill:#f0fdf4,stroke:#16a34a
```

```mermaid
flowchart TD
    ATOM["AMD ATOM 핵심 개선"] --> Checkpoint["희소 체크포인트 보존<br/>적중률 5.6% → 96.45%<br/>(동시성 48)"]
    ATOM --> Pipeline["청크형 파이프라인 프리필<br/>GLM-5.2: 처리량 2배<br/>TTFT 28.6초 → 8.7초"]
    ATOM --> PCPgain["프리필 컨텍스트 병렬화<br/>TTFT -35~43%, 처리량 +49%<br/>(64k 입력)"]

    style Pipeline fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    AITER["AITER 저수준 커널"] --> Addr["32비트 오프셋 한계<br/>(1.5억 행 넘으면 주소 오류)"]
    Addr --> Fix64["DeepSeek-V4 통합 캐시<br/>전체 64비트 주소 지정 적용"]

    style Addr fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Fix64 fill:#f0fdf4,stroke:#16a34a
```

TensorRT-LLM은 이 외에도 커널 선택 오류를 다수 잡아냈다 — 손상된 split-K MoE 전략이 AgentX 실행 7건 중 5건을 충돌시킨 것을 제거해 이후 7건 매칭 실행에서 충돌 0건을 만들었고, MiniMax-M3의 짧은 쿼리에서 인덱스를 잘못 읽어 비유한(non-finite) 출력을 내던 버그를 고쳐 GB300에서 서빙 오류·비유한 마커 0건을 확인했다. ATOM은 이와 별개로 라우터(ATOMesh)에 KV 생애주기 이벤트·다중 노드 프리필-디코드 라우팅·세션 고정 데이터병렬 라우팅을 추가해, 대화가 그 상태를 쥔 정상 워커로 돌아가면서도 방치된 세션이 클러스터를 영구히 불균형하게 만들지 않도록 유휴 배정은 만료시키는 절충을 택했다.

---

## 7. Dynamo·LMCache·Mooncake 최적화와 그 밖의 개선

**📌 핵심:**
- Dynamo 라우터는 생성 토큰 수가 아니라 살아있는 프리픽스의 개수·길이에 비례해 일이 늘어나는 구조라, 캐시 소유권을 "공유 블록 체인"에서 "아레나 단위 소유 카운트"를 거쳐 "백엔드별 요청 리스"로 단순화하며 vLLM 백엔드 AgentX 재생 시간을 23.7%, SGLang을 22.0% 단축했고 피크 메모리도 함께 낮췄다
- 요청 경로 자체도 뜯어고쳤다 — MessagePack 요청 페이로드 전환으로 처리량 8.1%↑·평균 TTFT 9.7%↓, 정적 로깅 필터로 프런트엔드 처리량이 초당 932건에서 1,133건으로, 응답당 한 번만 지표를 반영하는 변경이 프런트엔드 CPU 시간을 약 절반으로 줄이는 등 "매 토큰마다 반복되던 작은 낭비"를 겹겹이 제거했다
- LMCache(다양한 추론 엔진 아래에서 재사용 가능한 KV 청크를 프리픽스 해시로 저장하는 오픈소스 레이어)는 청크 단위 외부 캐시 로딩으로 동시성 32에서 옛 방식이 28건 만에 멈추던 걸 120건까지 완주시켰고, Mooncake는 AMD RDMA 등록 경로(HIP dmabuf)와 ROCm 휠 배포를 새로 만들어 AMD 하드웨어에서도 상류 이미지에 바로 설치해 GPU\~패브릭 간 KV를 직접 옮길 수 있게 됐다
- 결론: MiniMax-M3의 day-0 검증에서는 순수 소프트웨어 버그 3건이 확인됐다 — 헤드 비율 검증 오류로 gsm8k 점수가 0이 나오거나, gfx942의 FP8 인코딩(e4m3fnuz)을 잘못 읽어 K·V 값이 계산 전에 손상되던 것, AMD 모델 파일에 EAGLE3 인터페이스가 빠져 추측 디코딩이 아예 초기화 단계에서 멈추던 것을 모두 고쳐 MI355X gsm8k 점수가 정상화됐다

---

```mermaid
flowchart TD
    Dynamo["Dynamo 라우터 최적화"] --> Own["소유권 표현 단순화<br/>공유블록체인 → 리스 방식"]
    Own --> Result["재생시간 vLLM -23.7%<br/>SGLang -22.0%, 피크메모리↓"]

    style Result fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    LMCache["LMCache"] --> Chunk["청크단위 외부캐시 로딩<br/>동시성32: 28건 데드락 → 120건 완주"]
    Mooncake["Mooncake"] --> ROCm["HIP dmabuf RDMA +<br/>ROCm 휠 배포 신설"]
    ROCm --> Install["AMD도 상류 이미지에<br/>바로 설치 가능해짐"]

    style Chunk fill:#f0fdf4,stroke:#16a34a
    style Install fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    M3Bugs["MiniMax-M3 day-0 버그 3건"] --> HeadRatio["헤드비율 검증오류<br/>→ gsm8k 점수 0"]
    M3Bugs --> FP8["gfx942 FP8 인코딩 오독<br/>→ K·V 값 손상"]
    M3Bugs --> Eagle["AMD모델 EAGLE3 미구현<br/>→ 추측디코딩 초기화 실패"]
    HeadRatio --> Fixed["세 건 모두 수정<br/>MI355X gsm8k 정상화"]

    style M3Bugs fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Fixed fill:#f0fdf4,stroke:#16a34a
```

이 모든 개선의 공통점은 "더 긴 어텐션"이 아니라 계속 자라나는 세션 상태를 보존·이동·라우팅·재구성·반복 처리하는 새로운 최적화 표면이 열렸다는 점이다. 옛 고정 길이 매트릭스는 프롬프트 하나를 만들어 프리필 한 번, 디코드 한 번 하고 버리는 구조라 턴 간 캐시 생존·반복 토큰화·세션 어피니티·오프로드 왕래·스케줄러 정체 같은 것을 애초에 측정하지 못했는데, AgentX가 이런 비용을 충분히 크게 드러내 vLLM·SGLang·TensorRT-LLM·ATOM·AITER·Dynamo·LMCache 전반의 상류 개선을 이끌어냈다.

---

## 8. AgentX 방법론 - 300만 달러 데이터셋과 트레이스 리플레이어

**📌 핵심:**
- SemiAnalysis는 클로드 코드·OpenAI Codex 등으로 향하는 HTTP 요청을 가로채는 프록시를 만들어 사내 직원들의 실제 사용 트래픽을 모았다 — 현재까지 세션 8,000개 이상, 요청 340만 건, 토큰 6,100억 개(총 300만 달러 이상 상당)를 수집했고, 그중 393세션 대표 부분집합을 AgentX v1.0용으로 공개했다
- 직원 프라이버시 보호를 위해 요청 내용을 64토큰 블록으로 나눠 각 블록을 세션 단위 체인 해시로 치환한다 — 원본 프롬프트·소스코드·도구 결과는 전혀 남지 않지만 일치하는 프리픽스는 그대로 일치하는 해시 프리픽스로 남아, 재생 시 실제 코딩 데이터셋의 토큰으로 채워 넣어도 원래의 맥락 성장·KV 재사용 패턴은 보존된다
- 정제된 데이터셋의 입력 길이(ISL) 중앙값은 14만 2천 토큰, 출력 길이(OSL) 중앙값은 444토큰, 턴 사이 지연(주로 도구 사용 시간) 중앙값은 3.84초이며, 세션의 약 44%(175개)에 서브에이전트가 최소 1개 있고 서브에이전트 1,697개의 중앙값 실행 시간은 2.27분이다 — 리플레이는 Nvidia의 벤더 중립 HTTP 리플레이 도구 AIPerf(SemiAnalysis 자체 포크)를 써서 각 세션을 방향성 비순환 그래프(DAG)로 표현해 서브에이전트의 동시 실행·메인 에이전트 합류까지 재현한다
- 결론: 재현성을 위해 워밍업 2단계(대화 진행률 25\~75% 지점 재구성 → 레인마다 10개 요청 추가)를 거친 뒤 1시간 동안 측정하고, 유휴 5분을 넘긴 스트림은 끊어(앤트로픽 기본 KV 캐시 TTL 5분과 동일 기준) 벤치마크가 무한정 늘어지지 않게 하며, 추측 디코딩은 합성 데이터가 왜곡을 만들지 않도록 실제 코딩 트레이스(SPEED-Bench)에서 측정한 평균 수락 길이(acceptance length)를 그대로 적용해 공정성을 맞춘다

---

```mermaid
flowchart TD
    Collect["프록시로 직원 실사용<br/>트래픽 수집"] --> Scale["세션 8,000+·요청 340만 건<br/>토큰 6,100억(300만 달러+ 상당)"]
    Scale --> Subset["대표 393세션을<br/>AgentX v1.0으로 공개"]

    style Scale fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

```mermaid
flowchart TD
    Privacy["프라이버시 보호"] --> Hash["요청을 64토큰 블록 단위<br/>세션체인 해시로 치환"]
    Hash --> Preserve["원문은 안 남지만<br/>프리픽스 일치 패턴은 보존"]
    Preserve --> Refill["재생 시 실제 코딩<br/>토큰으로 재충전"]

    style Preserve fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    DataProfile["정제 데이터셋 프로필"] --> ISL["ISL 중앙값 14.2만 토큰"]
    DataProfile --> OSL["OSL 중앙값 444토큰"]
    DataProfile --> Sub["서브에이전트 있는 세션 44%<br/>(175개, 중앙값 4개/세션)"]

    style DataProfile fill:#eff6ff,stroke:#3b82f6
```

```mermaid
flowchart TD
    Replay["측정 절차"] --> Warmup["워밍업 2단계<br/>(25~75% 지점 재구성 + 레인당 10요청)"]
    Warmup --> Profile["1시간 측정<br/>유휴 5분 초과 스트림 절단"]
    Profile --> SpecDec["추측디코딩은 SPEED-Bench<br/>실측 수락길이로 벤더중립 보정"]

    style Warmup fill:#eff6ff,stroke:#3b82f6
```

새로 만든 시각화 도구도 이번 AgentX의 성과다 — 각 데이터 포인트를 클릭하면 어떤 설정(추측 디코딩·분리형 서빙·KV 오프로드 등)이 그 점을 만들었는지, CI 증빙과 함께 볼 수 있고, KV 캐시 이용률·요청 큐 깊이·프리픽스 캐시 적중률을 대화별·워커별 타임라인과 대화 하나의 구조를 보여주는 화염그래프(flamegraph)까지 제공한다.

---

## 9. InferenceX/AgentX 다음 단계

**📌 핵심:**
- v1.0.x 소규모 버그 수정은 계속하되, v1.1 하네스에서는 SSD/NVMe KV 오프로드를 추가해 DRAM보다 더 큰 작업셋을 감당함으로써 Pareto 곡선의 고처리량 구간을 더 넓힐 계획이다
- 다음 데이터셋은 요청을 하나의 연속된 해시 ID 리스트로 뭉치지 않고 시스템 지시·사용자/어시스턴트 메시지·도구 호출·도구 결과의 경계를 그대로 보존해, 라우터가 재사용률 낮은 도구 트래픽을 전담 프리필 워커로 보내거나 긴 도구 호출 동안 프리픽스를 유지하는 등 하네스만 아는 정보를 활용하는 서빙 기법까지 평가할 수 있게 할 계획이다
- 결론: 소프트웨어·하드웨어 스택별 "지능당 줄(Joule)" 효율까지 비교할 수 있도록 세밀한 전력 원격측정 데이터도 함께 수집하고 있다

---

```mermaid
flowchart TD
    NextGen["v1.1 하네스 계획"] --> NVMe["SSD/NVMe KV 오프로드<br/>추가 → 고처리량 구간 확장"]
    NextGen --> Structure["요청 경계(시스템·사용자·<br/>도구호출·도구결과) 보존"]
    NextGen --> Power["세밀한 전력 원격측정<br/>→ 지능당 줄(Joule) 비교"]

    style NextGen fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

---

*작성 진행률: 약 78% 완료*
*업데이트: 전체 11개 섹션 중 1\~9장(서론\~다음 단계) 작성 완료*
