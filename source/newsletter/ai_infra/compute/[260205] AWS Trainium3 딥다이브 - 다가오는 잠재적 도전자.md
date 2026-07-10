---
categories: [ai-infra/compute]
---

# AWS Trainium3 Deep Dive: A Potential Challenger Approaching

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential)
> **저자**: Dylan Patel, Daniel Nishball, Wega Chu
> **발행일**: 2026-02-05

---

## 📑 목차

### 전체 섹션
 1. [개요: Trainium3 발표와 AWS의 하드웨어 및 소프트웨어 전략](#1-개요-trainium3-발표와-aws의-하드웨어-및-소프트웨어-전략)
 2. [스펙 업그레이드: HBM3E, 스케일업, 스케일아웃 대역폭 확대](#2-스펙-업그레이드-hbm3e-스케일업-스케일아웃-대역폭-확대)
 3. [랙 아키텍처 2종 개관 - NL32x2 Switched vs NL72x2 Switched](#3-랙-아키텍처-2종-개관---nl32x2-switched-vs-nl72x2-switched)
 4. [실리콘과 패키징 - N3P 공정과 CoWoS-R, 이중 테이프아웃](#4-실리콘과-패키징---n3p-공정과-cowos-r-이중-테이프아웃)
 5. [Trainium4 로드맵 - UALink와 NVLink 이중 트랙](#5-trainium4-로드맵---ualink와-nvlink-이중-트랙)
 6. [레거시 토러스에서 스위치드로 - 전환 이유](#6-레거시-토러스에서-스위치드로---전환-이유)
 7. [NL32x2 Switched 상세 - 랙과 JBOG 트레이 구조](#7-nl32x2-switched-상세---랙과-jbog-트레이-구조)
 8. [NL72x2 Switched 상세 - 컴퓨트 트레이와 스케일아웃 네트워킹](#8-nl72x2-switched-상세---컴퓨트-트레이와-스케일아웃-네트워킹)
 9. [스케일업 네트워크 대역폭 구성 - 백플레인, PCB, 크로스랙](#9-스케일업-네트워크-대역폭-구성---백플레인-pcb-크로스랙)
10. [스위치 세대 진화 - Gen1에서 Gen3(UALink)까지](#10-스위치-세대-진화---gen1에서-gen3ualink까지)
11. [구리 케이블, 전력 예산, BOM과 수익화 속도 전략](#11-구리-케이블-전력-예산-bom과-수익화-속도-전략)
12. [스케일아웃 네트워킹 - EFA, ENA와 고radix 전략](#12-스케일아웃-네트워킹---efa-ena와-고radix-전략)
13. [마이크로아키텍처 - 4대 엔진과 숫자 포맷](#13-마이크로아키텍처---4대-엔진과-숫자-포맷)
14. [소프트웨어 대전환 - PyTorch 네이티브, NKI, MFU](#14-소프트웨어-대전환---pytorch-네이티브-nki-mfu)
15. [LNC(논리적 뉴런코어)와 Megacore, 성능 프로파일링 툴](#15-lnc논리적-뉴런코어와-megacore-성능-프로파일링-툴)
16. [데이터센터 램프업과 공랭 베팅, TCO 비교](#16-데이터센터-램프업과-공랭-베팅-tco-비교)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **JBOG (Just a Bunch of GPUs)**: XPU(가속기)만 여러 개 꽂아넣은 단순한 트레이 구조 — CPU 없이 가속기 전용으로 구성
- **NeuronLink(v4)**: AWS가 자체 설계한 스케일업(같은 랙 내부 칩 간) 연결 규격 — Nvidia NVLink와 달리 범용 PCIe 신호 규격 위에 구현
- **HBM3E 핀 속도 vs 스택 층수**: 메모리 대역폭은 스택을 얼마나 높이 쌓느냐(용량)와는 별개로, 신호를 얼마나 빨리 주고받느냐(핀 속도)로도 결정됨
- **N3P·CoWoS-R**: N3P는 TSMC 3나노 공정의 개선판(속도·전력 소폭 개선), CoWoS-R은 실리콘이 아닌 유기 재질 인터포저로 저비용에 칩을 묶는 패키징 방식
- **LNC(논리적 뉴런코어)·Megacore**: 칩 안의 물리적 연산 코어를 프로그래머에게 몇 개씩 묶어서 노출할지 정하는 방식 — 잘게 쪼갤수록 세밀한 제어가 가능하지만 진입장벽이 높아짐
- **EFA vs ENA**: EFA는 AI 훈련·추론용 고성능 후방(east-west) 네트워크, ENA는 일반 클라우드 서비스용 전방(north-south) 네트워크
- **Perf per TCO (총소유비용 대비 성능)**: 장비 가격만이 아니라 전력·운영까지 합친 총비용 대비 실제로 뽑아내는 성능 — AWS 설계 철학의 핵심 기준
- **스위치드 vs 토러스 토폴로지**: 칩들을 연결하는 두 가지 배선 방식 — 토러스는 이웃 칩끼리만 격자로 연결(홉 수 많음), 스위치드는 중앙 스위치를 거쳐 사실상 모든 칩이 직접 연결(홉 수 적음)

---

## 1. 개요: Trainium3 발표와 AWS의 하드웨어 및 소프트웨어 전략

**📌 핵심:**
- AWS는 re:Invent에서 **Trainium3(Trn3) 양산 출하**와 차세대 **Trainium4(Trn4) 로드맵**을 함께 발표 — 구글 TPUv7 심층분석 발표 직후라 경쟁 구도상 타이밍이 중요
- AWS 하드웨어 철학은 "**최저 총소유비용(TCO)에 최단 기간 출시**" — 특정 기술에 몰빵하지 않고 스위치 대역폭(12.8T/25.6T/51.2T)과 냉각 방식(공랭/수랭)을 상황에 맞춰 섞어 씀
- 스케일업(같은 랙 내부 칩 간) 네트워크를 기존 토러스 방식에서 **스위치 방식**(Nvidia GB200 NVL36x2와 유사)으로 전환 — 최신 MoE(전문가 혼합) 모델은 모든 칩이 서로 통신하는 all-to-all 방식이 많아 토러스보다 스위치가 유리하기 때문
- 결론: 소프트웨어도 사내 전용(Bedrock·Anthropic)에서 PyTorch 오픈소스화로 전환 — Nvidia CUDA 생태계의 장벽을 외부 개발자 저변 확대로 맞서겠다는 전략이며, Google TPUv7·AMD MI450X와 함께 Nvidia를 다각도로 압박하는 구도가 완성됨

---

```mermaid
flowchart TD
    Context["직전 발표: 구글 TPUv7<br/>1만 단어 심층분석"] --> ReInvent["AWS re:Invent에서<br/>Trainium3 양산 출하 +<br/>Trainium4 로드맵 발표"]
    ReInvent --> History["Amazon은 데이터센터<br/>커스텀 실리콘 역사가<br/>가장 길고 넓음(과거엔 AI에서 열세)"]

    style ReInvent fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style History fill:#eff6ff,stroke:#3b82f6
```

```mermaid
flowchart TD
    Goal["AWS 하드웨어 노스스타"] --> Star["목표: 최저 TCO +<br/>최단 기간 출시"]
    Star --> Flex["수단: 특정 설계에<br/>올인하지 않고<br/>운영 유연성 극대화"]
    Flex --> Ex1["예: 스위치 대역폭<br/>12.8T/25.6T/51.2T 중<br/>상황별 선택"]
    Flex --> Ex2["예: 공랭 vs 수랭도<br/>고객·데이터센터 조건에<br/>따라 혼용"]

    style Star fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Flex fill:#f0fdf4,stroke:#16a34a
```

```mermaid
flowchart TD
    Topo["스케일업 네트워크 전환"] --> Old["Trn2: 4x4x4<br/>3D 토러스 메시만 지원"]
    Topo --> New["Trainium3: 스위치 방식<br/>추가(GB200 NVL36x2와 유사)"]
    New --> Why["이유: 최신 MoE 모델은<br/>all-to-all 통신 비중이 커서<br/>토러스보다 스위치가<br/>절대 성능·TCO 모두 유리"]

    style Old fill:#eff6ff,stroke:#3b82f6
    style New fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    SwGen["스케일업 스위치<br/>3세대 로드맵"] --> G1["1세대: 160레인<br/>20포트 PCIe<br/>(시장 출시 속도 우선)"]
    SwGen --> G2["2세대: 320레인<br/>40포트 PCIe"]
    SwGen --> G3["3세대: 72+포트<br/>UALink(최고 성능)"]

    style G1 fill:#eff6ff,stroke:#3b82f6
    style G3 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

소프트웨어 쪽에서도 전략 전환이 큽니다. AWS의 "소프트웨어 노스스타"는 내부 Bedrock 워크로드(DeepSeek·Qwen 등 vLLM v1 자체 포크 사용)와 Anthropic 훈련·추론 전용 최적화를 넘어, 훨씬 더 넓은 개발자층을 겨냥합니다.

```mermaid
flowchart TD
    SWStrat["소프트웨어 전략 전환"] --> Before["기존: 내부 전용<br/>(Bedrock, Anthropic 맞춤)"]
    SWStrat --> P1["1단계: PyTorch 네이티브<br/>백엔드 + NKI 컴파일러<br/>오픈소스화"]
    SWStrat --> P2["2단계: XLA 그래프<br/>컴파일러 + JAX<br/>스택 오픈소스화"]

    style Before fill:#eff6ff,stroke:#3b82f6
    style P1 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style P2 fill:#f0fdf4,stroke:#16a34a
```

AWS는 "CUDA 해자(moat)는 Nvidia 엔지니어가 아니라 그 주위에 참호를 파는 수백만 외부 개발자가 만든다"고 보고, 똑같은 전략을 그대로 따라갑니다. 다만 Trainium3는 출시일(Day 0)에 LNC(논리적 뉴런코어, 15장 참고)=1 또는 2만 지원하며, 폭넓은 연구자 커뮤니티가 선호하는 LNC=8은 2026년 중반까지 지원 예정이 없습니다.

```mermaid
flowchart TD
    Battle["Nvidia가 맞이한<br/>3개 전선"] --> B1["Google TPUv7<br/>(강력한 Perf per TCO)"]
    Battle --> B2["AMD MI450X UALoE72<br/>(OpenAI 지분 리베이트로<br/>재기 노림)"]
    Battle --> B3["AWS Trainium3<br/>(이번 발표로 신규 전선)"]

    style Battle fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style B3 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

저자들은 Nvidia가 계속 개발 속도를 가속하는 한 "정글의 왕" 자리를 지킬 것으로 보되, 과거 인텔이 CPU 시장에서 안주하다 AMD·ARM에 추격당한 사례처럼, Nvidia가 안주하면 선두 자리를 더 빨리 잃을 것이라고 경고합니다.

이 리포트는 스위치 스케일업을 지원하는 두 랙 SKU — **공랭 Trainium3 NL32x2 Switched(코드네임 "Teton3 PDS")**와 **수랭 Trainium3 NL72x2 Switched(코드네임 "Teton3 Max")** — 를 중심으로, 실리콘 설계·랙 아키텍처·BOM·전력 예산·네트워크 아키텍처·마이크로아키텍처·소프트웨어 전략·데이터센터 램프업·TCO까지 순서대로 다룹니다.

---

## 2. 스펙 업그레이드: HBM3E, 스케일업, 스케일아웃 대역폭 확대

**📌 핵심:**
- 연산 성능: OCP MXFP8 처리량이 전세대 대비 **2배**로 늘고 신규 지원되는 MXFP4는 MXFP8과 동일한 성능 — 반면 FP16·FP32 같은 고정밀 포맷 성능은 전세대(Trn2)와 동일하게 유지(13장에서 트레이드오프 상세)
- 메모리: HBM3E를 12층으로 쌓아 칩당 용량 144GB 확보, 스택 수는 4개로 그대로인데도 핀 속도를 5.7Gbps(Trn2)에서 9.6Gbps(Trn3, 업계 최고 수준)로 올려 **대역폭 70% 증가** — 공급사를 삼성에서 SK하이닉스·마이크론으로 전환한 덕분(Trn2의 5.7Gbps는 사실상 HBM3급 속도였음)
- 네트워크: 스케일업 대역폭은 PCIe Gen6 전환(레인당 64Gbps, Gen5의 32Gbps 대비 2배)으로 칩당 1.2TB/s(단방향) 확보, 스케일아웃 대역폭도 최대 400Gb/s까지 가능(2배 확대)하나 실제 생산 물량 대다수는 Trn2와 같은 200Gb/s를 유지
- 결론: Trainium4는 HBM4 8스택 채택으로 Trainium3 대비 **대역폭 4배, 용량 2배**를 예고 — HBM 세대 전환이 이 아키텍처의 다음 성장축임을 시사

---

```mermaid
flowchart TD
    Compute["연산 포맷별<br/>세대 간 변화(Trn2 대비)"] --> F1["OCP MXFP8:<br/>처리량 2배"]
    Compute --> F2["OCP MXFP4:<br/>신규 지원, MXFP8과<br/>동일 성능"]
    Compute --> F3["FP16·FP32:<br/>Trn2와 동일(변화 없음)"]

    style F1 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style F3 fill:#eff6ff,stroke:#3b82f6
```

```mermaid
flowchart TD
    HBM["HBM3E 세대 비교"] --> Trn2h["Trn2: 핀 속도 5.7Gbps<br/>(삼성 공급, 사실상 HBM3급)"]
    HBM --> Trn3h["Trainium3: 핀 속도 9.6Gbps<br/>(SK하이닉스·마이크론,<br/>업계 최고 HBM3E 속도)"]
    Trn3h --> Result["같은 4스택인데도<br/>대역폭 70%↑,<br/>12층 적층으로 용량 144GB"]

    style Trn2h fill:#eff6ff,stroke:#3b82f6
    style Trn3h fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Result fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

**📌 용어 풀이: 핀 속도가 대역폭을 좌우하는 이유**
> - 메모리 대역폭 = 신호선 개수 × 신호선 하나당 속도(핀 속도) — 스택을 더 쌓는다고 대역폭이 느는 게 아니라, 신호선당 속도가 얼마나 빠른지가 관건
> - Trn2의 HBM3E는 공급사(삼성)의 속도 한계 탓에 이름만 HBM3E일 뿐 실제로는 HBM3급 속도(5.7Gbps)에 머물렀고, Trainium3는 공급사를 SK하이닉스·마이크론으로 바꿔 9.6Gbps까지 끌어올림

```mermaid
flowchart TD
    ScaleUp["스케일업 대역폭<br/>(칩 간 연결)"] --> Gen5["PCIe Gen5:<br/>레인당 32Gbps"]
    ScaleUp --> Gen6["PCIe Gen6:<br/>레인당 64Gbps(2배)"]
    Gen6 --> Lane["144개 활성 레인 사용<br/>→ 칩당 1.2TB/s(단방향)"]

    style Gen6 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Lane fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    ScaleOut["스케일아웃 대역폭<br/>(랙 밖 연결)"] --> Max["이론 최대: 400Gb/s<br/>(전세대 대비 2배)"]
    ScaleOut --> Actual["실제 생산 물량 대다수:<br/>200Gb/s per XPU<br/>(Trn2와 동일 유지)"]

    style Max fill:#eff6ff,stroke:#3b82f6
    style Actual fill:#fff7ed,stroke:#ea580c
```

```mermaid
flowchart TD
    Trn4["Trainium4 예고"] --> Stack["HBM4 8스택 채택<br/>(Trainium3는 HBM3E 4스택)"]
    Stack --> Gain["Trainium3 대비<br/>대역폭 4배, 용량 2배"]

    style Stack fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Gain fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

---

## 3. 랙 아키텍처 2종 개관 - NL32x2 Switched vs NL72x2 Switched

**📌 핵심:**
- Trn2·Trn3 세대를 합쳐 랙 SKU가 총 4종 존재하는데, AWS 공식 브랜드명과 ODM·공급망이 쓰는 코드네임이 서로 달라 업계에서도 혼선이 큼 — 저자들은 Nvidia·AMD처럼 "제품명 뒤에 스케일업 기술+월드사이즈"(예: NVL72)를 붙이는 명명법으로 통일할 것을 AWS에 공개 요청
- Trn2는 NL16 2D 토러스·NL32x2 3D 토러스 2종만 존재했지만, **Trainium3는 4종 SKU를 모두 지원** — 다만 2026년 생산 물량 대다수는 공랭 NL32x2 Switched에 집중될 전망
- 두 스위치드 랙의 핵심 차이는 냉각 방식과 스케일업 월드사이즈: NL32x2 Switched(공랭, 랙당 32칩·전체 64칩)와 NL72x2 Switched(수랭, 랙당 72칩 구성·전체 144칩, CPU를 컴퓨트 트레이에 통합)
- 결론: 두 SKU는 경쟁 관계가 아니라 상호 보완 — 액체 냉각 준비가 안 된 데이터센터는 공랭 SKU로 우선 배치하고, 준비된 곳은 고밀도 수랭 SKU로 확장하는 유연한 전개가 가능(자세한 랙 구조는 7·8장)

---

```mermaid
flowchart TD
    Naming["SKU 명명 혼선 문제"] --> Issue["AWS 공식 브랜드명 ≠<br/>ODM·공급망 코드네임"]
    Issue --> Ask["저자 요청: Nvidia·AMD처럼<br/>'스케일업 기술+월드사이즈'로<br/>통일된 명명법 채택"]

    style Issue fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Ask fill:#f0fdf4,stroke:#16a34a
```

```mermaid
flowchart TD
    Evo["세대별 지원 SKU 수"] --> Trn2s["Trn2: 2종만<br/>(NL16 2D 토러스,<br/>NL32x2 3D 토러스)"]
    Evo --> Trn3s["Trainium3: 4종 모두 지원<br/>(토러스 2종 + 스위치드 2종)"]
    Trn3s --> Volume["2026년 물량 대다수는<br/>공랭 NL32x2 Switched"]

    style Trn3s fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Volume fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    Compare["스위치드 랙 2종<br/>핵심 차이"] --> A["NL32x2 Switched<br/>(Teton3 PDS): 공랭,<br/>랙당 32칩, 월드사이즈 64칩"]
    Compare --> B["NL72x2 Switched<br/>(Teton3 Max): 수랭,<br/>랙당 72칩 구성,<br/>월드사이즈 144칩"]
    B --> CPU["CPU(Graviton4)를<br/>컴퓨트 트레이에 통합<br/>(NL32x2는 분리형)"]

    style A fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style B fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    Comp["두 SKU는<br/>경쟁이 아닌 보완 관계"] --> Case1["액체 냉각 미준비 DC:<br/>공랭 NL32x2 Switched로<br/>우선 배치"]
    Comp --> Case2["액체 냉각 준비된 DC:<br/>고밀도 수랭<br/>NL72x2 Switched로 확장"]

    style Comp fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

---

## 4. 실리콘과 패키징 - N3P 공정과 CoWoS-R, 이중 테이프아웃

**📌 핵심:**
- Trainium3는 Trn2의 N5 공정에서 **TSMC N3P**로 이전 — Vera Rubin, AMD MI450X의 AID(Active Interposer Die)와 함께 N3P 최초 채택 사례 중 하나이며, N3P 특유의 누설전류 이슈로 일정이 밀릴 가능성도 있음
- N3P는 N3E 대비 완전히 새로운 설계 규칙 없이 **같은 누설전류 기준 속도 5% 향상, 또는 같은 클럭 기준 전력 5\~10% 절감**, 밀집 로직·SRAM·아날로그 혼합 설계에서 밀도 4% 향상 정도의 점진적 개선("HPC 다이얼") — 거대 AI ASIC이 원하는 딱 그 수준의 저마찰 개선
- 패키징은 실리콘 인터포저 1장이 아니라 **CoWoS-R 어셈블리 2개**로 구성 — 저비용 유기 인터포저 기반이라 실리콘 인터포저 대비 기계적 유연성도 좋음
- 결론: 설계는 Annapurna(프론트엔드)+Alchip(백엔드) 분담 체제, 마스크셋도 Alchip 소유("Anita")와 Annapurna 소유("Mariana") 이중 테이프아웃으로 나뉘며 물량 대다수는 Mariana — 이 과정에서 전세대 설계사였던 Marvell은 소켓 자체를 잃음

---

```mermaid
flowchart TD
    N3P["N3P = 3나노<br/>플랫폼의 'HPC 다이얼'"] --> Opt1["같은 누설전류 기준<br/>속도 약 5% 향상"]
    N3P --> Opt2["또는 같은 클럭 기준<br/>전력 5\~10% 절감"]
    N3P --> Opt3["혼합 설계(로직+SRAM+<br/>아날로그) 밀도 약 4%↑"]
    Opt3 --> Fit["거대 AI ASIC이 원하는<br/>딱 그 수준의<br/>점진적·저마찰 개선"]

    style N3P fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style Fit fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

N3P는 단일 돌파구가 아니라 여러 DTCO(설계-공정 공동 최적화) 미세 조정이 쌓인 결과입니다. N3 세대 FinFlex 라이브러리로 블록 안에서 넓은 핀·좁은 핀을 섞어 구동력과 면적·누설전류를 미세 조정하고, 하위 금속층의 라이너·배리어 공정을 개선해 배선·비아 저항을 낮췄습니다. 이 개선분이 모여 긴 글로벌 배선에서 더 높은 클럭이나 더 낮은 최소 동작전압(Vmin)을 지원할 여유를 만들어냅니다.

```mermaid
flowchart TD
    Challenge["N3P의 대가"] --> Pitch["최소 금속 피치가<br/>20나노 초반대까지 축소,<br/>고종횡비 비아·타이트한<br/>광학 축소"]
    Pitch --> Variability["배선 하부 공정(BEOL)<br/>변동성·저항 증가 →<br/>비아 형상·언더에치·<br/>유전체 손상이 1차 문제화"]
    Variability --> Yield["결과: 결함밀도 개선이<br/>예상보다 느림 →<br/>수율 위해 재설계하거나<br/>공정 개선 대기열에서 대기"]

    style Pitch fill:#fef2f2,stroke:#dc2626
    style Yield fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    Package["Trainium3 패키지 구조"] --> NoMono["실리콘 인터포저 1장이<br/>아니라 CoWoS-R<br/>어셈블리 2개로 구성"]
    NoMono --> Sub["두 컴퓨트 다이는<br/>서로 기판(substrate)을<br/>통해 통신"]
    Package --> Organic["유기 박막 인터포저:<br/>폴리머 위 구리 RDL 6층,<br/>레티클급 면적, 실리콘<br/>인터포저 대비 저비용+<br/>기계적 유연성 우수"]
    Organic --> IPD["단, 32Gbps 이상 레인이<br/>많아지면 유기 인터포저만으론<br/>배선 공간 부족 → IPD(집적<br/>수동소자) 수천 개로 보완"]
    IPD --> Detail["IPD 덕에 서브마이크론<br/>배선 밀도, 미세 마이크로범프<br/>피치, HBM PHY 등 잡음<br/>구간의 강력한 디커플링 확보"]

    style NoMono fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style IPD fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Detail fill:#f0fdf4,stroke:#16a34a
```

칩 하단에는 20층 빌드업의 고층 ABF 기판이 자리해, 전력과 XSR 신호를 모듈 경계의 130\~150마이크로미터 C4 범프까지 팬아웃한 뒤 보드와 연결합니다.

```mermaid
flowchart TD
    Design["설계·제조 분담 체제"] --> Front["프론트엔드: Annapurna<br/>(PCIe SerDes는<br/>시높시스에서 라이선스)"]
    Design --> Back["백엔드 물리설계+<br/>패키지 설계: Alchip"]
    Design --> Tape["이중 테이프아웃"]
    Tape --> Anita["Anita(Alchip 소유<br/>마스크셋): Alchip이<br/>TSMC서 직접 부품 조달"]
    Tape --> Mariana["Mariana(Annapurna 소유<br/>마스크셋): Annapurna가<br/>직접 부품 조달,<br/>물량 대다수 차지"]

    style Front fill:#eff6ff,stroke:#3b82f6
    style Mariana fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

Amazon·Annapurna는 원가에 극도로 민감해 공급업체를 강하게 압박합니다. Broadcom의 ASIC 거래와 비교하면 Trainium 프로젝트는 설계 파트너(Alchip·Marvell)에게 돌아가는 이익 풀 자체가 훨씬 작으며, Perf per TCO 관점에서도 Annapurna는 TCO(분모)를 낮추는 쪽에 훨씬 무게를 둡니다.

```mermaid
flowchart TD
    Marvell["Marvell의 몰락"] --> Was["Trainium2는<br/>Marvell이 설계"]
    Was --> Lost["이번 세대(Trn3) 설계<br/>경쟁에서 Alchip에 패배"]
    Lost --> Why1["실행 부진: 개발 일정이<br/>지나치게 길어짐"]
    Lost --> Why2["RDL 인터포저 설계<br/>난항 → Alchip이 개입해<br/>수습해야 했음"]
    Lost --> Chiplet["Marvell 안(案)은 I/O를<br/>별도 칩렛으로 분리한<br/>설계였으나, 실제 채택된<br/>Trn3는 모놀리식 다이 유지"]

    style Marvell fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Lost fill:#fff7ed,stroke:#ea580c
```

---

## 5. Trainium4 로드맵 - UALink와 NVLink 이중 트랙

**📌 핵심:**
- Trainium4는 스케일업 프로토콜이 다른 **두 트랙**으로 복수 설계사가 참여 — 1트랙은 UALink 224G, 2트랙은 Nvidia NVLink 448G BiDi 프로토콜 채택(양쪽 모두 백엔드 설계는 Alchip이 주도)
- Nvidia의 VR NVL144와 NVLink Fusion 제품(Trainium4 포함) 사이에는 상당한 출시 시차가 예상 — NVLink Fusion 트랙은 퓨전 칩렛이 요구하는 추가 통합·검증 작업 때문에 더 밀릴 수 있고, Nvidia의 혼합신호 엔지니어 대다수가 우선 자사 VR NVL144 신제품 출시에 매달려 있기 때문
- Trainium4의 NVLink Fusion 출시가 늦더라도 AWS는 Nvidia의 통상 총마진(약 75%)보다 유리한 조건을 확보했을 가능성이 큼 — Nvidia 입장에서도 AWS와의 상호운용성 허용이 시스템 차원의 록인(lock-in) 유지에 도움이 되므로 가격을 더 매력적으로 제시할 유인이 있음
- 결론: VR NVL144가 72패키지 고정 NVLink 도메인에 묶인 것과 달리, Trainium4는 랙 간 AEC로 NVLink 스케일업을 확장해 **144개 이상**의 일관성(coherent) 도메인을 구성 가능 — NVLink 6는 400G 양방향(BiDi) SerDes로 같은 선에서 200G 송신·200G 수신을 동시에 수행하며 이미 구리 배선의 실용적 한계에 근접, 일부 벤더는 600G BiDi로의 절반 세대 도약도 시도할 전망

---

```mermaid
flowchart TD
    Trn4["Trainium4<br/>스케일업 프로토콜 2트랙"] --> T1["1트랙: UALink 224G"]
    Trn4 --> T2["2트랙: Nvidia NVLink<br/>448G BiDi"]
    T1 --> Backend["양쪽 모두 백엔드 설계는<br/>Alchip이 주도"]
    T2 --> Backend

    style Trn4 fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style Backend fill:#f0fdf4,stroke:#16a34a
```

```mermaid
flowchart TD
    Timing["출시 시차 리스크"] --> Gap["Nvidia VR NVL144 vs<br/>NVLink Fusion(Trainium4 등)<br/>사이 상당한 시차 예상"]
    Gap --> Reason1["퓨전 칩렛은 추가 통합·<br/>검증 요구사항 있음"]
    Gap --> Reason2["Nvidia 혼합신호<br/>엔지니어 대다수가<br/>VR NVL144 신제품 출시에<br/>우선 투입됨"]

    style Gap fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    Deal["상업 조건 전망"] --> Margin["Nvidia 통상 총마진<br/>약 75%보다 AWS는<br/>유리한 조건 확보 추정"]
    Margin --> Incentive["Nvidia도 AWS와의<br/>상호운용 허용이<br/>자사 시스템 록인 유지에<br/>도움되므로 가격 유인 존재"]

    style Margin fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    Scale["스케일업 도메인 크기 비교"] --> VR["Nvidia VR NVL144:<br/>72패키지 고정<br/>NVLink 도메인"]
    Scale --> T4["Trainium4: 랙 간 AEC로<br/>확장 → 144개 이상<br/>일관성 도메인 구성 가능"]
    T4 --> Signal["NVLink 6: 400G BiDi<br/>SerDes(같은 선에서<br/>200G 송신+200G 수신<br/>동시), 구리 실용 한계 근접"]

    style VR fill:#eff6ff,stroke:#3b82f6
    style T4 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

---

## 6. 레거시 토러스에서 스위치드로 - 전환 이유

**📌 핵심:**
- Trn2는 NL16 2D 토러스(반 랙, 4x4 메시로 칩 16개 스케일업 월드)와 NL32x2 3D 토러스(NL16 반 랙 4개를 AEC로 연결, 랙 2개·칩 64개 4x4x4 구조) 2종만 존재 — 스위치 방식은 아예 없었음
- Trn2 물량 대다수는 NL64 3D 토러스로 쏠렸는데, 이는 Anthropic의 Project Rainier가 최대 수요처였고 그 추론 모델이 더 큰 스케일업 토폴로지를 요구했기 때문
- Nvidia가 GB200 NVL72(Oberon 아키텍처, all-to-all 스위치·72칩 월드사이즈)를 선보이자 업계 전체가 로드맵을 이 방식으로 전환 — AMD가 Oberon 유사 설계(MI400 Helios)를 가장 먼저 "발표"했지만, 실제로 이런 all-to-all 스위치 스케일업을 Nvidia 밖에서 처음 "출하"하는 곳은 Trainium3를 앞세운 AWS(AMD MI450X UALoE72는 1년 늦게, 연말 목표; Meta도 AMD보다 먼저 스위치드 아키텍처 출하 예정)
- 결론: re:Invent에서 공개된 "Trainium3 UltraServer"는 NL72x2 Switched를 가리키며, 스위치드 SKU는 이것과 공랭·저전력밀도인 NL32x2 Switched 2종으로 나뉨(7·8장에서 각각 상세 구조를 다룸)

---

```mermaid
flowchart TD
    Trn2Topo["Trn2 토폴로지 2종<br/>(스위치 방식 없음)"] --> NL16["NL16 2D 토러스:<br/>반 랙, 4x4 메시,<br/>칩 16개 스케일업 월드"]
    Trn2Topo --> NL32["NL32x2 3D 토러스:<br/>NL16 반 랙 4개를 AEC 연결,<br/>랙 2개·칩 64개(4x4x4)"]

    style NL16 fill:#eff6ff,stroke:#3b82f6
    style NL32 fill:#fff7ed,stroke:#ea580c
```

```mermaid
flowchart TD
    Demand["Trn2 물량이<br/>NL64 3D 토러스로 쏠린 이유"] --> Anthropic["Anthropic Project Rainier가<br/>최대 수요처"]
    Anthropic --> Need["Anthropic 추론 모델은<br/>더 큰 스케일업<br/>토폴로지가 필요"]

    style Anthropic fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

```mermaid
flowchart TD
    Pivot["업계 전체의<br/>스위치 방식 전환"] --> Nvidia_["Nvidia GB200 NVL72<br/>(Oberon, all-to-all,<br/>72칩 월드사이즈) 선도"]
    Nvidia_ --> AMDann["AMD: MI400 Helios로<br/>Oberon 유사 설계<br/>가장 먼저 '발표'"]
    Nvidia_ --> AWSship["AWS: Trainium3로<br/>Nvidia 외 최초 실제<br/>'출하'(AMD보다 1년 빠름)"]
    AWSship --> AMDlate["AMD MI450X UALoE72:<br/>1년 늦게, 연말 목표<br/>(Meta도 AMD보다 먼저 출하)"]

    style AWSship fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style AMDlate fill:#fef2f2,stroke:#dc2626
```

```mermaid
flowchart TD
    Ultra["re:Invent 공개<br/>'Trainium3 UltraServer'"] --> Is["= NL72x2 Switched"]
    Is --> Other["다른 스위치드 SKU:<br/>NL32x2 Switched<br/>(공랭, 저전력밀도)"]

    style Is fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

---

*작성 진행률: 약 38% 완료*
*업데이트: 4\~6장(실리콘·패키징, Trainium4 로드맵, 레거시 토러스에서 스위치드로) 작성 완료*
