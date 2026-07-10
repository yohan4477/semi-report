---
categories: [ai-infra/compute]
---

# AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256)
> **저자**: Kimbo Chen, Dylan Patel, Daniel Nishball
> **발행일**: 2026-02-05

---

## 📑 목차

### 전체 섹션
 1. [개요 - AMD Advancing AI 2025 발표 요약](#1-개요---amd-advancing-ai-2025-발표-요약)
 2. [MI350X·MI355X 스펙 - CDNA4 기반 신제품](#2-mi350x·mi355x-스펙---cdna4-기반-신제품)
 3. [MI355X vs HGX B200 - 성능당비용(TCO) 경쟁력](#3-mi355x-vs-hgx-b200---성능당비용tco-경쟁력)
 4. [엔비디아 DGX Lepton과 뉴클라우드의 반발](#4-엔비디아-dgx-lepton과-뉴클라우드의-반발)
 5. [MI355X는 랙 스케일 솔루션이 아니다 - 마케팅 과장 논란](#5-mi355x는-랙-스케일-솔루션이-아니다---마케팅-과장-논란)
 6. [하이퍼스케일러·AI 랩의 AMD 신제품 채택 현황](#6-하이퍼스케일러·ai-랩의-amd-신제품-채택-현황)
 7. [AMD 뉴클라우드 렌탈 시장의 구조적 약점](#7-amd-뉴클라우드-렌탈-시장의-구조적-약점)
 8. [AMD의 뉴클라우드 생태계 육성 전략](#8-amd의-뉴클라우드-생태계-육성-전략)
 9. [ROCm 소프트웨어 개선과 엔지니어링 우선순위 이슈](#9-rocm-소프트웨어-개선과-엔지니어링-우선순위-이슈)
10. [MI355X 제조 - 칩렛 아키텍처 리파인](#10-mi355x-제조---칩렛-아키텍처-리파인)
11. [CDNA4 마이크로아키텍처(UArch) 상세](#11-cdna4-마이크로아키텍처uarch-상세)
12. [AMD AI 엔지니어 보상 현실화 움직임](#12-amd-ai-엔지니어-보상-현실화-움직임)
13. [MI400 시리즈 Flexible I/O와 UALoE72 - 진짜 UALink는 아니다](#13-mi400-시리즈-flexible-io와-ualoe72---진짜-ualink는-아니다)
14. [MI400 Helios 랙 아키텍처 상세](#14-mi400-helios-랙-아키텍처-상세)
15. [MI500 UAL256 - 2027년 차세대 랙 컨셉](#15-mi500-ual256---2027년-차세대-랙-컨셉)
16. [MI350X·MI355X·MI400 BOM과 TCO 비교](#16-mi350x·mi355x·mi400-bom과-tco-비교)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **TCO(총소유비용, Total Cost of Ownership)**: 장비 구매 비용뿐 아니라 운영·전력·유지보수까지 합친 전체 비용 — 이 문서 전반에서 AMD와 Nvidia 제품을 비교하는 핵심 잣대
- **랙 스케일(Rack Scale) 솔루션**: 랙 안의 모든 GPU가 하나의 초고속 네트워크로 묶여 마치 GPU 1개처럼 작동하는 설계 — 몇 개의 서버를 그냥 한 랙에 모아놓은 것과는 다름
- **뉴클라우드(Neocloud)**: 하이퍼스케일러(Google·AWS 등 대형 클라우드)가 아니면서 GPU를 임대해주는 전문 GPU 클라우드 업체(예: CoreWeave, Tensorwave, Crusoe)
- **ROCm**: AMD GPU를 위한 오픈소스 소프트웨어 스택 — Nvidia의 CUDA에 대응하는 개념
- **UALink vs UALoE**: UALink는 여러 업체가 공동 개발 중인 GPU 스케일업(랙 내부 초고속 연결) 표준 규격 자체, UALoE(UALink over Ethernet)는 그 규격을 이더넷 스위치 위에 얹어 흉내만 낸 것 — 이 문서의 핵심 논쟁거리
- **BOM(부품 명세서, Bill of Materials)**: 시스템 하나를 만드는 데 들어가는 모든 부품과 그 원가를 나열한 목록
- **CU(컴퓨트 유닛, Compute Unit)**: AMD GPU 내부의 연산 처리 단위 — Nvidia의 SM(Streaming Multiprocessor)에 대응하는 개념
- **DGX Lepton**: Nvidia가 내놓은 GPU 임대 마켓플레이스 — 여러 클라우드의 GPU를 하나의 표준화된 창구로 묶어 파는 서비스

---

## 1. 개요 - AMD Advancing AI 2025 발표 요약

**📌 핵심:**
- MI350X·MI355X는 소형\~중형 모델 추론에서 Nvidia HGX B200과 경쟁 가능하지만, **랙 스케일 솔루션이 아니며** GB200 NVL72(프런티어 모델 추론·학습)와는 급이 다름
- 진짜 랙 스케일 제품은 **MI400 시리즈** — 2026년 하반기 Nvidia VR200 NVL144와 경쟁 가능할 전망이나, 스케일업 네트워크는 진짜 UALink가 아니라 이더넷 위에 얹은 **UALoE(UALink over Ethernet)**
- Nvidia의 GPU 임대 마켓플레이스 DGX Lepton이 뉴클라우드(전문 GPU 임대업체)들의 불만을 사면서, AMD가 뉴클라우드 생태계를 파고들 기회의 창이 열림
- 결론: AWS는 신규 대형 고객으로 합류했지만 Microsoft는 여전히 소극적 — AMD의 하드웨어 경쟁력 개선이 뉴클라우드·소프트웨어 격차라는 두 숙제와 함께 진행 중

---

지난 6개월간 AMD는 전시(Wartime) 태세로 Nvidia와의 경쟁력 확보에 총력을 기울여 왔습니다. Advancing AI 2025 행사에서 MI350X/MI355X GPU를 공개했는데, 소형\~중형 LLM 추론에서 성능당비용(TCO) 기준으로 Nvidia HGX B200과 경쟁할 만한 수준입니다.
다만 MI355X는 랙 스케일 제품이 아니며, 프런티어 모델 추론·학습에서는 GB200 NVL72의 상대가 되지 못합니다.

```mermaid
flowchart TD
    Event["AMD Advancing AI 2025<br/>발표 요약"] --> P1["MI350X/MI355X:<br/>소형~중형 LLM 추론에서<br/>HGX B200과 경쟁 가능"]
    Event --> P2["MI400 시리즈:<br/>진짜 랙 스케일 솔루션,<br/>H2 2026 VR200 NVL144와 경쟁 목표"]
    Event --> P3["UALoE 마케팅 스핀:<br/>Infinity Fabric over Ethernet을<br/>'UALink over Ethernet'으로 개명"]

    style P1 fill:#eff6ff,stroke:#3b82f6
    style P2 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style P3 fill:#fef2f2,stroke:#dc2626
```

이번 리포트는 AMD 신제품의 상대적 경쟁력과 총소유비용을 분석하고, 신규 하이퍼스케일 고객 AWS와 반대로 후속 주문이 계속 실망스러운 기존 고객 Microsoft를 다룹니다.
또한 Nvidia의 DGX Lepton Marketplace 출시로 뉴클라우드 파트너들의 불만이 커지면서 AMD에게 열린 기회의 창, AMD가 뉴클라우드에 투자하는 금융공학적 기법, 내부 연구개발 클러스터 투자까지 살펴봅니다.

```mermaid
flowchart TD
    Summary["12개 핵심 요약<br/>(원문 Executive Summary)"] --> Hw["하드웨어 경쟁력"]
    Summary --> Eco["뉴클라우드·생태계"]
    Summary --> Org["조직·인력 이슈"]

    Hw --> Hw1["MI355X: HGX B200과 경쟁,<br/>GB200 NVL72엔 열세<br/>(스케일업 8 GPU vs 72 GPU)"]
    Eco --> Eco1["DGX Lepton發 뉴클라우드 불만<br/>→ AMD엔 기회"]
    Org --> Org1["AI 엔지니어 보상<br/>시장가 미달 문제 진행 중"]

    style Hw1 fill:#fff7ed,stroke:#ea580c
    style Eco1 fill:#f0fdf4,stroke:#16a34a
    style Org1 fill:#fef2f2,stroke:#dc2626
```

```mermaid
flowchart TD
    MI400sum["MI400 시리즈 핵심 요약"] --> M1["랙 스케일 솔루션,<br/>VR200 NVL144와<br/>스케일업 대역폭 대등"]
    MI400sum --> M2["UALoE72: 실제로는<br/>UALink가 아니라<br/>브로드컴 이더넷 스위치 사용"]
    MI400sum --> M3["2027년 말 MI500 UAL256:<br/>물리/논리 칩 256개<br/>(VR300 NVL576은 144개)"]

    style M1 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style M2 fill:#fef2f2,stroke:#dc2626
    style M3 fill:#fff7ed,stroke:#ea580c
```

---

## 2. MI350X·MI355X 스펙 - CDNA4 기반 신제품

**📌 핵심:**
- MI350X(1,000W, 공랭)와 MI355X(1,400W, 공랭+물 냉각 지원) 두 버전 — MI355X가 전력을 1.4배 더 쓰지만 공식 스펙상 TFLOPS는 10% 미만 향상, 다만 실제로는 전력 제약 탓에 공식 스펙 자체가 실전에서 잘 안 나오므로 격차가 더 클 것으로 예상
- FP4 포맷에서 MI355X는 OCP MX4만 지원(32개 원소 블록 단위 보정)하는 반면, Nvidia Blackwell은 MX4와 NVFP4(16개 원소 블록, 정확도 더 좋음)를 모두 지원 — 정밀도 열세는 런타임 양자화 기법으로 일부 보완 가능
- HBM 용량은 288GB로 B200(180GB)보다 많아 단일 노드 추론에 유리하지만, 스케일업 네트워크(XGMI, 76.8GB/s)는 Nvidia의 스위치형 전체연결 방식보다 1.6배 느림 — GB200/GB300 NVL72(72개 GPU 스케일업)와는 비교 자체가 무의미(MI350/355는 8개 GPU만 연결)
- 결론: MI350X/MI355X는 스펙상 HGX B200과 경쟁 가능한 수준이지만, 스케일아웃 네트워킹(400Gbit/s, AMD 800GbE NIC는 2H 2026 양산)도 Nvidia 대비 뒤처짐

---

```mermaid
flowchart TD
    Chips["MI350X vs MI355X"] --> C1["MI350X: 1,000W,<br/>공랭 전용"]
    Chips --> C2["MI355X: 1,400W(1.4배),<br/>공랭+물 냉각 지원"]
    C2 --> C3["공식 스펙 TFLOPS 차이는<br/>10% 미만이나, 실전에선<br/>전력 제약으로 격차 더 클 전망"]

    style C2 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style C3 fill:#eff6ff,stroke:#3b82f6
```

📌 용어 풀이: 왜 공식 스펙이 실전에서 안 나오나
> - 공식 스펙(피크 TFLOPS)은 "최고 클럭 속도를 계속 유지할 수 있다"고 가정하지만, 실제로는 전력·발열 제약 때문에 클럭이 계속 떨어짐
> - AMD·Nvidia 모두 겪는 문제 — 그래서 저자는 MI355X의 실제 성능이 공식 스펙상 "10% 미만 향상"보다 더 클 것으로 추정

```mermaid
flowchart TD
    FP4["4비트 부동소수점(FP4)<br/>포맷 지원 비교"] --> AMDf["MI355X: OCP MX4만 지원<br/>(32개 원소 블록 단위 보정)"]
    FP4 --> NVf["Blackwell: MX4 + NVFP4<br/>(NVFP4는 16개 원소 블록,<br/>정확도 더 우수)"]
    NVf --> Quant["결과: NVFP4가 양자화(QAT/PTQ)<br/>시 모델 품질 보존 우위,<br/>MX4는 런타임 기법으로 추격 가능"]

    style AMDf fill:#fef2f2,stroke:#dc2626
    style NVf fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    FP6["FP6 연산 회로 공유 방식"] --> B200fp6["B200: FP6이 FP8과<br/>같은 회로 공유<br/>(FP8과 동일 TFLOPS)"]
    FP6 --> AMDfp6["MI355X: FP6이 FP4와<br/>같은 회로 공유<br/>(FP4와 동일 TFLOPS)"]
    AMDfp6 --> Result["결과: MI355X FP6이<br/>B200 FP6보다 이론상 2.2배 빠름<br/>(단, 전력 제약으로 실전에선<br/>MI355 FP4 대비 최소 20% 느려짐)"]

    style Result fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

B300 HGX NVL8은 FP64·int8 텐서 코어 대부분을 제거하고 그 자리에 FP4 텐서 코어 회로를 1.4배 늘렸습니다. 이 최적화 덕에 B300의 FP4 TFLOPS는 MI355X보다 1.3배 빠르면서도 소비 전력은 200W 적습니다(MI350/355는 이 최적화를 쓰지 않음).

```mermaid
flowchart TD
    HBMcompare["HBM 용량·대역폭 비교"] --> Cap["용량: MI350/355 288GB<br/>vs B200 180GB<br/>(단일 노드 추론에 유리)"]
    HBMcompare --> Note["단, 다중 노드 고랭크<br/>전문가 병렬화·분리형<br/>프리필 환경에선 이점 축소<br/>(그래도 여전히 도움)"]

    style Cap fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

메모리 대역폭이 용량보다 훨씬 중요한 지표라, 8-Hi HBM4를 서로 다른 2개의 대형 ASIC 프로그램용으로 두 HBM 벤더가 서둘러 개발 중입니다(자세한 내용은 SemiAnalysis 가속기·HBM 모델 참고).

```mermaid
flowchart TD
    ScaleUp["스케일업 네트워크<br/>(XGMI) 비교"] --> AMDxgmi["MI350/355: XGMI를<br/>1.2배 오버클록<br/>(64→76.8GB/s, PCIe 5.0 확장모드)"]
    ScaleUp --> NVswitch["B200/B300: 스위치형<br/>전체연결 토폴로지가<br/>메시 토폴로지 대비 1.6배 빠름"]
    NVswitch --> NVL72["GB200/GB300 NVL72:<br/>72개 GPU 스케일업 도메인<br/>(MI350/355는 8개뿐, 비교 불가)"]

    style AMDxgmi fill:#fff7ed,stroke:#ea580c
    style NVL72 fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

```mermaid
flowchart TD
    ScaleOut["스케일아웃 네트워킹<br/>(GPU당 대역폭)"] --> Same["현재: MI350/355·B200·<br/>GB200 NVL72 모두<br/>400Gbit/s로 동일"]
    Same --> Next["곧 격차: B300 HGX NVL8·<br/>GB300 NVL72는 800Gbit/s로 상향"]
    Next --> Lag["AMD 지연: Nvidia 800GbE<br/>ConnectX-8은 2025년 양산,<br/>AMD 800GbE 'Vulcano' NIC는<br/>2H 2026에야 양산"]

    style Lag fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

---

## 3. MI355X vs HGX B200 - 성능당비용(TCO) 경쟁력

**📌 핵심:**
- MI355X는 소형\~중형 LLM 프로덕션 추론에서 HGX B200 대비 TCO가 33% 낮으면서 HBM 용량은 더 많고, FP8·FP4 TFLOPS는 소폭 우위, FP6 TFLOPS는 2배 — AMD 소프트웨어(ROCm) 개선이 이어지면 이 우위는 더 커질 전망
- AMD의 핵심 세일즈 포인트는 "칩에 직접 물을 공급하는 냉각 방식(DLC)이 필요 없다"는 점이지만, 정작 비교 대상은 이미 시장에 나온 지 오래된 Nvidia의 "보급형" HGX 제품군 — GB200 NVL72(플래그십)과는 애초에 체급이 다름
- MI355X는 스케일업 세계 크기가 작아(8 GPU) GB200 NVL72와 정면 승부가 불가능 → 대신 공랭형 HGX B200 NVL8·HGX B300 NVL8을 겨냥하는 포지셔닝
- 결론: 대규모 스케일업 네트워크의 이점을 못 받는 소형\~중형 모델 사용자에게는 MI355X가 매력적이지만, 대규모 분리형 서빙이나 혼합 전문가(MoE) 모델을 쓰는 추론 환경에서는 GB200 NVL72가 성능·성능당비용 모두 압도

---

```mermaid
flowchart TD
    TCOcomp["MI355X vs HGX B200<br/>(소형~중형 모델 추론)"] --> T1["TCO 33% 낮음<br/>(자가 소유 클러스터 기준)"]
    TCOcomp --> T2["HBM 용량 더 많음,<br/>FP8·FP4 TFLOPS 소폭 우위,<br/>FP6 TFLOPS는 2배"]
    T2 --> T3["ROCm 소프트웨어 개선<br/>지속 시 TCO 우위 더 확대 전망"]

    style T1 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style T3 fill:#eff6ff,stroke:#3b82f6
```

```mermaid
flowchart TD
    Position["MI355X의 실제 경쟁 상대"] --> NotThis["아니다: GB200 NVL72<br/>(플래그십, 스케일업 72 GPU)"]
    Position --> ThisOne["맞다: 공랭형 HGX B200 NVL8·<br/>HGX B300 NVL8<br/>('보급형' 제품군)"]
    NotThis --> WhyNot["이유: MI355X 스케일업<br/>세계 크기는 8 GPU뿐<br/>(GB200의 9분의 1)"]

    style NotThis fill:#fef2f2,stroke:#dc2626
    style ThisOne fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    Winner["워크로드별 승자"] --> Small["소형~중형 모델,<br/>대규모 스케일업 불필요:<br/>MI355X가 유리한 구간"]
    Winner --> Large["프런티어 추론,<br/>대규모 분리형 서빙·MoE:<br/>GB200 NVL72가<br/>성능·성능당비용 모두 압도"]

    style Small fill:#f0fdf4,stroke:#16a34a
    style Large fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

이 제품 구간은 MI355X의 소프트웨어 품질과 AMD가 책정할 가격에 따라 의미 있는 물량이 출하될 전망입니다.

---

*작성 진행률: 약 25% 완료 (1\~3장 작성)*
*업데이트: 개요, MI350X/MI355X 스펙, MI355X vs HGX B200 TCO 섹션 작성 완료*

