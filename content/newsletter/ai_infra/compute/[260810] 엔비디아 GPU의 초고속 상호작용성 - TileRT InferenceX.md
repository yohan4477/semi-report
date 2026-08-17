---
categories: [ai-infra/compute]
---

# Ultra-High Interactivity on NVIDIA GPUs? - TileRT InferenceX

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia)
> **저자**: Bryan Shan, Daniel Nishball, Cam Quilici
> **발행일**: 2026-08-10

---

## 📑 목차

### 전체 섹션
 1. [배경 - 프리미엄 빠른 모드와 GPU 지연시간 격차](#1-배경---프리미엄-빠른-모드와-gpu-지연시간-격차)
 2. [InferenceX 벤치마크 플랫폼과 처리량 대 상호작용성](#2-inferencex-벤치마크-플랫폼과-처리량-대-상호작용성)
 3. [TileRT 벤치마크 결과 - 입출력 토큰 시나리오별 상호작용성](#3-tilert-벤치마크-결과---입출력-토큰-시나리오별-상호작용성)
 4. [TileRT 벤치마크 결과 - 처리량 트레이드오프와 지연시간 분해](#4-tilert-벤치마크-결과---처리량-트레이드오프와-지연시간-분해)
 5. [TileRT란 무엇인가 - 지속형 엔진 커널](#5-tilert란-무엇인가---지속형-엔진-커널)
 6. [TileRT란 무엇인가 - 타일과 워프와 GPU 특화](#6-tilert란-무엇인가---타일과-워프와-gpu-특화)
 7. [PD 분리형 엔진 - vLLM과 TileRT의 결합](#7-pd-분리형-엔진---vllm과-tilert의-결합)
 8. [세레브라스·Groq·SambaNova와의 비교 - 하드웨어 데이터플로우 vs 소프트웨어 데이터플로우](#8-세레브라스groqsambanova와의-비교---하드웨어-데이터플로우-vs-소프트웨어-데이터플로우)
 9. [세레브라스·Groq·SambaNova와의 비교 - PD 비율 유연성이라는 구조적 강점](#9-세레브라스groqsambanova와의-비교---pd-비율-유연성이라는-구조적-강점)
10. [TileRT 개발이 느린 이유 - 정적 컴파일의 대가](#10-tilert-개발이-느린-이유---정적-컴파일의-대가)
11. [다음 단계 - AgentX 벤치마크와 배치 크기 확장](#11-다음-단계---agentx-벤치마크와-배치-크기-확장)
12. [성능당 TCO 분석 - 백만 토큰당 비용](#12-성능당-tco-분석---백만-토큰당-비용)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **TileRT**: 엔비디아 GPU 위에서 돌아가는 오픈소스 추론 소프트웨어 — 디코드(토큰을 한 개씩 이어 만드는 단계) 전체를 하나의 지속형 커널로 미리 컴파일해 지연시간을 줄인다
- **상호작용성(Interactivity) vs 처리량(Throughput)**: 상호작용성은 사용자 한 명이 체감하는 초당 토큰 생성 속도(tok/s/user), 처리량은 GPU 한 대가 전체 사용자를 상대로 만들어내는 총 토큰 수(tok/s/GPU) — 배치를 키우면 처리량은 늘지만 사용자 체감 속도는 떨어지는 트레이드오프 관계
- **지속형 엔진 커널(Persistent Engine Kernel)**: GPU가 매번 새 작업을 받는 대신, 모델 전체를 미리 컴파일해 하나의 프로그램으로 GPU에 상주시켜 디코드가 끝날 때까지 계속 실행하는 방식
- **CUDA 그래프(CUDA Graph)**: 커널(GPU가 실행하는 작업 단위) 여러 개의 실행 순서를 미리 기록해뒀다가 한 번에 재생하는 엔비디아의 기존 최적화 기법 — 커널 자체는 여전히 개별적으로 분리돼 있어 경계마다 비용이 남는다
- **워프 특화(Warp Specialization)**: GPU 코어 안의 실행 단위(워프)마다 서로 다른 역할(데이터 이동·연산·통신)을 맡겨 병렬로 겹쳐 돌리는 기법 — 모든 워프가 똑같은 일을 반복하던 기존 방식과 대비된다
- **PD 분리(Prefill-Decode Disaggregation)**: 추론의 프리필(입력 처리, 연산 집약)과 디코드(출력 생성, 메모리 대역폭 집약) 단계를 서로 다른 GPU 풀에 나눠 맡기는 방식
- **데이터플로우 칩(Dataflow Chip)**: 세레브라스·Groq·SambaNova처럼 반도체 하드웨어 자체를 저지연 전용으로 설계해, 스케줄링·통신 비용을 소프트웨어가 아니라 칩 구조로 없앤 전용 추론 칩
- **TCO(총소유비용, Total Cost of Ownership)**: 초기 장비 구입비(설비투자)와 운영비(전력·인력 등)를 합쳐 실제로 토큰 하나를 만드는 데 드는 전체 비용

---

## 1. 배경 - 프리미엄 빠른 모드와 GPU 지연시간 격차

**📌 핵심:**
- OpenAI 등 프론티어 AI 랩이 세레브라스·엔비디아 Groq LPU(저지연 특화 추론 칩) 같은 전용 하드웨어를 검토하는 이유는 단순하다 — "빠른 모드" 요금제에 웃돈을 내는 고객이 실제로 있다는 게 확인됐기 때문. OpenAI GPT-Live처럼 듣기와 말하기를 동시에 하는 실시간 음성비서는 응답 지연이 곧바로 체감된다
- 8-GPU HGX B200 서버는 이론상 합산 초당 64테라바이트(TB/s)의 HBM(고대역폭메모리) 대역폭을 낸다. GLM-5를 NVFP4(4비트 정밀도)로 배치 크기 1(사용자 한 명 요청만 처리)에서 돌리면 토큰 하나 만드는 데 필요한 데이터 이동량이 약 21GB뿐이라, 대역폭만 놓고 보면 초당 사용자당(tok/s/user) 최대 3,047토큰까지 가능해야 한다 — 실제 GPU는 이 근처에도 못 간다
- 격차의 원인은 대역폭이 아니라 지연시간 — GPU는 커널(작업 단위) 수천 개를 하나씩 실행·동기화하는데, 그 준비·정리 비용이 사용자당 응답 간격 1000분의 1초 이하 구간에서는 무시할 수 없을 만큼 커진다. 게다가 GPU 메모리 대역폭은 세대마다 2\~3배씩 늘어도 메모리 지연시간 자체는 전혀 개선되지 않고 있다
- 결론: TileRT는 디코드 전체를 하나의 지속형 커널로 미리 컴파일해 이 문제를 소프트웨어로 우회 — GLM5 FP8 744B(파라미터 7,440억 개) 벤치마크에서 단일 B200 서버로 초당 사용자당 최대 500토큰을 검증, 전통적 엔진을 쓰는 GB300 NVL72보다 약 3배 빠르고 같은 비용(iso-cost) 기준으로는 최대 2배 빠른 상호작용성을 달성

---

```mermaid
flowchart TD
    Roofline["B200 8GPU 이론상 한계<br/>HBM 대역폭 64TB/s<br/>GLM-5 NVFP4 배치1"] --> Theory["대역폭만 보면<br/>최대 3,047 tok/s/user<br/>가능해야 함"]
    Theory --> Reality["실제 GPU:<br/>이 근처에도 못 감"]
    Reality --> Cause["원인 = 대역폭이 아니라<br/>지연시간(커널 수천 개<br/>준비·정리 비용)"]

    style Theory fill:#eff6ff,stroke:#3b82f6
    style Reality fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Cause fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    TileRTFix["TileRT 해법:<br/>디코드 전체를<br/>지속형 커널 하나로 컴파일"] --> Bench["GLM5 FP8 744B<br/>단일 B200 서버 검증"]
    Bench --> R1["최대 500 tok/s/user"]
    Bench --> R2["GB300 NVL72<br/>전통 엔진 대비 약 3배"]
    Bench --> R3["같은 비용(iso-cost) 기준<br/>최대 2배 빠른 상호작용성"]

    style R1 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style R2 fill:#f0fdf4,stroke:#16a34a
    style R3 fill:#f0fdf4,stroke:#16a34a
```

TileRT는 같은 커뮤니티가 만든 GPU 커널 언어 TileLang의 개발진이 만들었다. 디코드 엔진은 이미 샤오미 MiMo V2.5 Pro UltraSpeed와 Z.ai GLM 5.1 HighSpeed 상용 서비스 뒤편에서 실제로 돌고 있다.

---

## 2. InferenceX 벤치마크 플랫폼과 처리량 대 상호작용성

**📌 핵심:**
- InferenceX는 SemiAnalysis가 운영하는 오픈소스·벤더 중립 추론 벤치마크 플랫폼 — 구글 클라우드·마이크로소프트 애저·오라클·메타 등 주요 컴퓨트 구매자와 vLLM·LMCache·SGLang·PyTorch·Huggingface 같은 오픈소스 진영, OpenAI·MiniMax·Z.ai·Qwen·Moonshot Kimi 등 주요 랩의 검증·지지를 받는다. 엔비디아는 베라 루빈 실측치를, 구글은 곧 TPUv7 결과를, AMD는 올해 안에 MI455X UALoE72 결과를 제출하기로 약속했다
- 모든 추론 시스템은 두 축의 트레이드오프를 겪는다 — **상호작용성(tok/s/user)**은 사용자 한 명이 토큰을 받는 속도(토큰당 생성 시간(TPOT)의 역수)로 응답이 빠릿한지를 가르고, **처리량(tok/s/GPU)**은 시스템 전체가 만드는 총 토큰 수로 토큰당 비용을 좌우한다
- 배치(여러 사용자 요청을 묶어 한꺼번에 처리하는 것)를 키우면 처리량은 늘지만 사용자 한 명이 기다리는 시간은 길어진다 — InferenceX v2 데이터에서 상호작용성을 초당 사용자당 25토큰에서 260토큰으로 10배 늘리면, GPU당 처리량은 초당 5,900토큰에서 200토큰으로 30배 줄어든다
- 결론: 처리량과 상호작용성은 버스(다수를 저렴하게 태우지만 정차가 잦음)와 레이싱카(1\~2명에게 빠르지만 훨씬 비쌈)의 관계와 같다 — TileRT는 이 스펙트럼에서 레이싱카 쪽 극단, 즉 초고속 상호작용성 구간만을 정조준한다

---

```mermaid
flowchart TD
    IX["InferenceX<br/>오픈소스·벤더중립 벤치마크"] --> Buyers["검증: 구글클라우드·<br/>MS 애저·오라클·메타"]
    IX --> OSS["지지: vLLM·LMCache·<br/>SGLang·PyTorch·HF"]
    IX --> Labs["지지: OpenAI·MiniMax·<br/>Z.ai·Qwen·Kimi"]

    style IX fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
```

```mermaid
flowchart TD
    Tradeoff["처리량 vs 상호작용성"] --> Inter["상호작용성(tok/s/user)<br/>사용자 1명 체감 속도<br/>TPOT의 역수"]
    Tradeoff --> Thru["처리량(tok/s/GPU)<br/>전체 생산 토큰 수<br/>토큰당 비용 좌우"]
    Inter -.배치 확대.-> Thru

    style Inter fill:#f0fdf4,stroke:#16a34a
    style Thru fill:#fff7ed,stroke:#ea580c
```

```mermaid
flowchart TD
    Example["InferenceX v2 실측 예시"] --> Before["상호작용성 25 tok/s/user<br/>처리량 5,900 tok/s/GPU"]
    Before --> After["상호작용성 260 tok/s/user<br/>10배 증가<br/>처리량 200 tok/s/GPU<br/>30배 감소"]

    style After fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

---

## 3. TileRT 벤치마크 결과 - 입출력 토큰 시나리오별 상호작용성

**📌 핵심:**
- 8k(입력)/1k(출력) 토큰 시나리오에서 TileRT는 8-GPU B200 노드로 초당 사용자당 340토큰을 냈다 — 기존 최고 기록은 GB300 NVL72(NVFP4+MTP(멀티토큰예측)) 181.4토큰으로, TileRT가 1.9배 빠르다. 다만 이건 배치 크기 1 비교라, GB300 NVL72의 값비싼 구리 백플레인(GPU 72장을 통째로 묶는 통신망)이 상호작용성을 끌어올리는 데는 전혀 기여하지 않는 조건이다
- 같은 정밀도(FP8)로 좁혀도 TileRT가 앞선다 — 기존 최고 기록은 B300(MTP 사용) 초당 113.6토큰인데 TileRT는 3.0배 빠르다
- 1k/1k 시나리오에서는 TileRT FP8이 초당 사용자당 494.2토큰을 기록 — 최고 기존 FP4 기록(256.3토큰) 대비 1.9배, 최고 기존 FP8 기록(136.3토큰) 대비 3.6배다. TileRT는 아직 FP4를 지원하지 않는데도 FP4를 쓰는 기존 엔진을 이미 앞선다. 이 결과는 72개 GPU를 NVLink로 묶은 NVL72 스케일업 도메인이 아니라 8개 GPU짜리 단일 노드에서 나왔다는 점도 눈여겨볼 대목 — 어디까지나 사용자 1명당 속도 비교이지, 총 처리량이나 비용 비교는 아니다
- 결론: 종단 지연시간(요청부터 마지막 토큰까지)에서도 TileRT FP8이 기존 최고 GLM-5.1 기록을 1k/1k에서 4.5배, 8k/1k에서 3.0배 앞선다 — 첫 토큰까지 걸리는 시간(TTFT)은 평범하지만, 결정적 우위는 디코드 꼬리(마지막까지 토큰을 뽑아내는 구간)에서 나온다: TileRT 3.01초 vs 최고 NVFP4+MTP 경쟁작 6.54초 vs MI355X 18.18초

---

```mermaid
flowchart TD
    S8k["8k/1k 시나리오<br/>(입력 8천·출력 1천 토큰)"] --> T340["TileRT(8GPU B200):<br/>340 tok/s/user"]
    S8k --> G181["기존 최고(GB300 NVL72<br/>NVFP4+MTP): 181.4"]
    T340 -.1.9배.-> G181

    style T340 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    FP8Same["같은 정밀도(FP8) 비교"] --> T3["TileRT: 3.0배 빠름"]
    FP8Same --> B113["기존 최고(B300+MTP):<br/>113.6 tok/s/user"]

    style T3 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    S1k["1k/1k 시나리오"] --> T494["TileRT FP8(8GPU B200):<br/>494.2 tok/s/user"]
    T494 --> VsFP4["최고 기존 FP4 256.3<br/>대비 1.9배"]
    T494 --> VsFP8["최고 기존 FP8 136.3<br/>대비 3.6배"]

    style T494 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    E2E["종단 지연시간<br/>(요청~마지막 토큰)"] --> Improve["TileRT FP8: 기존 최고 대비<br/>1k/1k 4.5배·8k/1k 3.0배"]
    Improve --> Tail["우위 원천 = 디코드 꼬리<br/>TileRT 3.01초 vs<br/>NVFP4+MTP 6.54초 vs<br/>MI355X 18.18초"]

    style Tail fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

---

*작성 진행률: 약 25% 완료*
*업데이트: 1\~3장(배경·GPU 지연시간 격차, InferenceX 플랫폼·처리량 대 상호작용성, TileRT 벤치마크 시나리오별 결과) 작성 완료*
