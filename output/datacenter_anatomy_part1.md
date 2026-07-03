# Datacenter Anatomy Part 1: Electrical Systems

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)
> **저자**: Dylan Patel
> **발행일**: 2024-10-14

---

## 🟡 서론: AI 시대의 Datacenter 변화

### 핵심 변화: AI가 Datacenter 설계를 재정의하다

```mermaid
flowchart TD
    Start[AI 수요 증가] --> Power[전력 수요 급증]
    Start --> Density[컴퓨팅 밀도 증가]

    Power --> BlackwellReq{Blackwell GB200<br/>요구사항}
    Density --> BlackwellReq

    BlackwellReq --> DirectLiquid[Direct-to-chip<br/>액체냉각 필수]
    BlackwellReq --> HighDensity[130kW+ 랙<br/>전력밀도]

    DirectLiquid --> Bottleneck{기존 datacenter<br/>대응 가능?}
    HighDensity --> Bottleneck

    Bottleneck -->|No: 낮은 전력밀도| MetaCase[Meta 사례:<br/>건설 중 건물 철거]
    Bottleneck -->|Yes: 고밀도 지원| Competitive[경쟁력 유지]

    MetaCase --> Redesign[AI-Ready<br/>설계로 전환]

    style Start fill:#fff7ed,stroke:#ea580c
    style BlackwellReq fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Bottleneck fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style MetaCase fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Competitive fill:#f0fdf4,stroke:#16a34a
```

**📌 용어 풀이: Blackwell GB200**
> - Nvidia의 차세대 GPU 제품군
> - 랙당 130kW+ 전력 소비
> - H100 대비 추론 성능 9배, 훈련 성능 3배 향상
> - Direct-to-chip 액체냉각 필수

### Meta 사례: 전력밀도가 경쟁력을 결정한다

```mermaid
graph LR
    OldDesign[기존 Meta 'H' 설계] --> LowDensity[낮은 전력밀도<br/>~10kW/rack]
    LowDensity --> Incompatible{GB200<br/>호환?}
    Incompatible -->|No: 130kW 지원 불가| Demolish[건설 중<br/>건물 철거]
    Demolish --> NewDesign[AI-Ready 설계<br/>고밀도 지원]

    Competitor[경쟁사: Google] --> HighDensity[높은 전력밀도<br/>~40kW/rack]
    HighDensity --> Compatible[GB200<br/>즉시 배치 가능]

    style OldDesign fill:#fef2f2,stroke:#dc2626
    style Demolish fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style NewDesign fill:#f0fdf4,stroke:#16a34a
    style Compatible fill:#f0fdf4,stroke:#16a34a
```

**핵심 인사이트:**
- Meta는 건설 중인 건물을 철거하고 AI-Ready 설계로 전환
- 전력밀도: Google 40kW/rack vs Meta 10kW/rack (4배 차이)
- GB200 130kW 요구사항을 충족하지 못하면 AI 경쟁에서 뒤처짐

---

## 🟢 Datacenter 기초

### Datacenter란?
IT 장비에 안전하고 효율적으로 전력을 공급하는 특수 목적 시설. 서버, 네트워크 스위치, 스토리지 장치가 랙에 배치되어 대량의 전력을 소비하고 열을 발생시킵니다.

**📌 용어 풀이: Critical IT Power**
> - IT 장비가 소비하는 최대 전력 (단위: kW 또는 MW)
> - 실제 전력망에서 공급되는 전력 > Critical IT Power (냉각, 조명 등 포함)
> - **Power Utilization Rate**:
>   - 클라우드 컴퓨팅: 50-60%
>   - AI 훈련: 80%+
>   - 엔터프라이즈: <50%

### 규모 비교: Datacenter vs 일반 건물

```mermaid
graph TD
    Building[건물 유형별<br/>전력 밀도 비교] --> Office[일반 사무실]
    Building --> Datacenter[현대 Datacenter]

    Office --> OfficeSpec["기준치:<br/>X W/sq ft"]
    Datacenter --> DatacenterSpec["50X 이상<br/>W/sq ft"]

    DatacenterSpec --> Evolution[30년 진화]
    Evolution --> Past["과거: 사무실 +<br/>강력한 에어컨"]
    Evolution --> Now["현재: 전문 시설<br/>특수 냉각 인프라"]

    style Datacenter fill:#fae8ff,stroke:#a855f7,stroke-width:2px
    style DatacenterSpec fill:#fef3c7,stroke:#f59e0b
```

### Tier 분류 체계 (Uptime Institute)

```mermaid
flowchart TD
    Start[Tier 분류 체계] --> Tier1{Tier 1}
    Start --> Tier2{Tier 2}
    Start --> Tier3{Tier 3}
    Start --> Tier4{Tier 4}

    Tier1 --> T1Spec["99.671% 가용성<br/>다운타임: 28.8시간/년<br/>단일 경로, 중복 없음"]
    Tier2 --> T2Spec["99.741% 가용성<br/>다운타임: 22시간/년<br/>단일 경로 + 일부 중복"]
    Tier3 --> T3Spec["99.982% 가용성<br/>다운타임: 1.6시간/년<br/>✅ 동시 유지보수 가능<br/>N+1 redundancy"]
    Tier4 --> T4Spec["99.995% 가용성<br/>다운타임: 0.4시간/년<br/>Fault tolerant<br/>2N redundancy"]

    T3Spec --> MostCommon[대형 시설에서<br/>가장 일반적]

    style Tier1 fill:#fef2f2,stroke:#dc2626
    style Tier2 fill:#fef3c7,stroke:#f59e0b
    style Tier3 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style Tier4 fill:#eff6ff,stroke:#3b82f6
    style MostCommon fill:#f0fdf4,stroke:#16a34a
```

**📌 용어 풀이: Redundancy (중복성)**
> - **N**: 정확히 필요한 수량만 보유
>   - 예: transformer 10개 필요 → 10개 구매
> - **N+1**: 필요한 수량 + 1개 예비
>   - 예: transformer 10개 필요 → 11개 구매 (10개 운영, 1개 대기)
> - **2N**: 필요한 수량의 2배
>   - 예: transformer 10개 필요 → 20개 구매
> - **Tier 3 일반적 구성**:
>   - Transformer/Generator: N+1
>   - UPS/PDU: 2N

**📌 용어 풀이: "Concurrently Maintainable" (동시 유지보수 가능)**
> Tier 3 시설의 핵심 특징. 시스템 중단 없이 장비를 유지보수할 수 있음을 의미합니다.

**참고: CSP의 "Three Nines" vs Datacenter Tier**
- CSP (클라우드 서비스 제공자)의 99.9%/99.999% 가용성은 SLA(서비스 수준 계약)
- 여러 Availability Zone 포함 + 서버/네트워크 가동시간 포함
- Datacenter Tier는 단일 시설의 물리적 인프라 가용성만 측정

---

## 🟡 Datacenter 종류별 비교

```mermaid
flowchart TD
    DatacenterTypes[Datacenter 분류] --> Retail[Retail<br/>Datacenter]
    DatacenterTypes --> Wholesale[Wholesale<br/>Datacenter]
    DatacenterTypes --> Hyperscale[Hyperscale<br/>Datacenter]

    Retail --> RetailSpec["⚡ 전력: 최대 수 MW<br/>📍 위치: 도심 내<br/>👥 고객: 다수의 소규모 테넌트<br/>💎 가치 제안: 네트워크 생태계<br/>(낮은 지연시간 상호연결)"]

    Wholesale --> WholesaleSpec["⚡ 전력: 10-30 MW<br/>📍 위치: 교외<br/>👥 고객: 대규모 영역 임차<br/>💎 가치 제안: 확장성<br/>(단계별 구축 phased build-out)"]

    Hyperscale --> HyperscaleSpec["⚡ 전력: 40-100 MW/건물<br/>🏢 캠퍼스: 100s MW<br/>👥 고객: 자체 구축/전용 임차<br/>💎 가치 제안: 대규모 배치<br/>(예: 300MW 캠퍼스)"]

    HyperscaleSpec --> PowerExample["🔋 전력 규모 예시:<br/>300MW 캠퍼스 ≈<br/>미국 가정 20만 가구의<br/>연간 전력 소비량"]

    HyperscaleSpec --> AIExample["🤖 AI 배치 예시:<br/>H100 20,840개 클러스터<br/>= ~25.9MW Critical IT Power"]

    style Retail fill:#dbeafe,stroke:#3b82f6
    style Wholesale fill:#e0e7ff,stroke:#6366f1
    style Hyperscale fill:#fae8ff,stroke:#a855f7,stroke-width:2px
    style PowerExample fill:#fef3c7,stroke:#f59e0b
    style AIExample fill:#fef3c7,stroke:#f59e0b
```

### 규모별 특징 상세

| 특징 | Retail | Wholesale | Hyperscale |
|------|--------|-----------|------------|
| **Critical IT Power** | 수 MW | 10-30 MW | 40-100 MW/건물 |
| **위치** | 도심 내 | 교외 | 대규모 부지 |
| **임차 단위** | 수 kW (랙 몇 개) | 1-5 MW (여러 행) | >5 MW (건물 전체) |
| **고객 수** | 다수 (수십~수백) | 중간 (수~수십) | 단일 또는 소수 |
| **가치 제안** | 네트워크 상호연결 | 확장 가능성 | 대규모 + 맞춤 설계 |
| **비즈니스 모델** | 부동산 ("location³") | 용량 + 확장성 | 효율성 극대화 |

### 운영 모델 비교

```mermaid
graph TD
    OperatorType[운영 모델] --> Colocation[Colocation<br/>제3자 임차]
    OperatorType --> SelfBuild[Self-Build<br/>자체 구축]

    Colocation --> ColoFeature["💰 가격: $/kW/month<br/>📏 규모: 100kW - 100s MW<br/>✅ 장점: Capex 절감,<br/>빠른 배치<br/>👥 고객: 모든 규모"]

    SelfBuild --> Private["Private Self-Build<br/>(금융, 정부, 헬스케어)<br/>🔒 민감한 데이터 처리"]
    SelfBuild --> HyperscaleSelf["Hyperscale Self-Build<br/>(Big Tech)<br/>⚡ 최대 효율성 추구"]

    HyperscaleSelf --> Hybrid["🔄 하이브리드 전략:<br/>- Build-to-suit 임차<br/>- Warm shell 임차<br/>- 완전 자체 구축"]

    style Colocation fill:#dbeafe,stroke:#3b82f6
    style SelfBuild fill:#e0e7ff,stroke:#6366f1
    style HyperscaleSelf fill:#fae8ff,stroke:#a855f7,stroke-width:2px
```

**📌 용어 풀이: Build-to-Suit & Warm Shell**
> - **Build-to-Suit**: Colocation 업체가 hyperscaler 사양에 맞춰 건설 후 임대
>   - 장점: Capex 분산, 전문가 설계
>   - 규모: 100MW+ 임차 계약도 흔함
> - **Warm Shell**: 전력 연결은 완료, 내부 M&E(기계/전기) 인프라는 임차자가 구축
>   - 장점: 유연성 + 부분적 Capex 절감

---

## 🔴 Datacenter 전기 시스템

### 핵심 원리: 왜 고전압으로 전달하나?

```mermaid
flowchart TD
    Question[왜 고전압 전송?] --> PowerLoss[전력 손실 = I² × R]

    PowerLoss --> HighV{고전압 사용?}
    HighV -->|Yes| LowCurrent[낮은 전류<br/>낮은 손실]
    HighV -->|No| HighCurrent[높은 전류<br/>높은 손실]

    LowCurrent --> Safety{건물 근처?}
    Safety -->|Yes| StepDown[MV로 강압<br/>안전 + 효율]
    Safety -->|No| KeepHigh[HV 유지<br/>장거리 전송]

    style Question fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style PowerLoss fill:#fef3c7,stroke:#f59e0b
    style LowCurrent fill:#f0fdf4,stroke:#16a34a
    style HighCurrent fill:#fef2f2,stroke:#dc2626
```

**📌 용어 풀이: 전압 레벨**
> - **High Voltage (HV)**: >100kV
>   - 예: 138kV, 230kV, 345kV
>   - 용도: 장거리 송전선
> - **Medium Voltage (MV)**: 11kV, 25kV, 33kV
>   - 용도: 건물 간 배전
> - **Low Voltage (LV)**: 415V (미국 3상)
>   - 용도: IT 장비 근처 배전

### 전력 전달 경로 (Outside-In)

```mermaid
flowchart TD
    Utility["⚡ 전력회사<br/>High Voltage<br/>&gt;100kV"] --> Substation{On-site<br/>Substation}

    Substation --> HVTransformer["🔌 HV Transformer<br/>230kV → 33kV<br/>(50-100 MVA)"]
    HVTransformer --> MVPower["Medium Voltage<br/>11/25/33 kV"]

    MVPower --> MVSwitchgear["📊 MV Switchgear<br/>배전 + 보호 + 계량"]
    MVSwitchgear --> DataHall["🏢 Data Hall 근처"]

    DataHall --> MVTransformer["🔌 MV Transformer<br/>33kV → 415V<br/>(2.5-3 MVA)"]
    DataHall --> Generator["🔋 Diesel Generator<br/>415V AC 출력<br/>(2-3 MW)"]

    MVTransformer --> ATS{"⚡ Auto Transfer<br/>Switch (ATS)"}
    Generator --> ATS

    ATS --> TwoPath{전력 경로 분기}

    TwoPath --> ITPath["💻 IT Equipment 경로"]
    TwoPath --> CoolingPath["❄️ Cooling Equipment 경로"]

    ITPath --> UPS["🔋 UPS System<br/>배터리 백업 5-10분<br/>응답시간 &lt;10ms"]
    UPS --> PDU["📡 Power Distribution<br/>Units (PDU)"]
    PDU --> Rack["🖥️ IT Racks"]
    Rack --> PSU["⚙️ PSU & VRM"]
    PSU --> Chip["🎯 CPU/GPU Chip"]

    style Utility fill:#dbeafe,stroke:#3b82f6
    style HVTransformer fill:#e0e7ff,stroke:#6366f1
    style MVTransformer fill:#e0e7ff,stroke:#6366f1
    style ATS fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style UPS fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style Chip fill:#f0fdf4,stroke:#16a34a
```

**핵심 포인트:**
1. **전압 변환**: HV (230kV) → MV (33kV) → LV (415V) 3단계 강압
2. **백업 시스템**: Generator (1분 내 기동) + UPS (<10ms 응답)
3. **이중 경로**: IT 장비용 + 냉각 장비용 별도 경로

---

## 🔴 High Voltage Transformers

### Transformer 작동 원리

```mermaid
flowchart TD
    Concept[Transformer 기본 개념] --> OldTech["100년 이상 된<br/>간단한 기술"]

    OldTech --> AC["AC 전류 →<br/>변화하는 자기장"]
    AC --> Induction["전자기 유도<br/>(Electromagnetic Induction)"]

    Induction --> Coils{2개 코일 배치}
    Coils --> Primary["1차 코일<br/>(Primary Coil)"]
    Coils --> Secondary["2차 코일<br/>(Secondary Coil)"]

    Secondary --> Turns{권선 수<br/>비교}
    Turns -->|감소| StepDown["Step-Down<br/>전압 감소<br/>전류 증가"]
    Turns -->|증가| StepUp["Step-Up<br/>전압 증가<br/>전류 감소"]

    style Concept fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style StepDown fill:#f0fdf4,stroke:#16a34a
    style StepUp fill:#dbeafe,stroke:#3b82f6
```

**📌 용어 풀이: MVA vs MW**
> - **MVA (Mega Volt-Ampere)**: "겉보기 전력" = 전압 × 전류
> - **MW (Mega Watt)**: "실제 전력" (유효 전력)
> - **관계**: MW = MVA × Power Factor
> - **Power Factor**: 일반적으로 ~0.95, 여유를 위해 0.9로 설계
> - **예시**: 80 MVA transformer ≈ 72 MW 실제 전력

### HV Transformer 사양 및 배치

```mermaid
graph TD
    Campus["Hyperscale Campus<br/>150 MW 필요"] --> Calculate{Transformer<br/>규모 계산}

    Calculate --> Option1["옵션 1: 80 MVA × 2개<br/>(N 구성, 중복 없음)"]
    Calculate --> Option2["옵션 2: 80 MVA × 3개<br/>(N+1 구성, 권장)"]

    Option2 --> Operation["운영 방식:<br/>3개가 부하 분담<br/>각각 2/3 용량으로 운영"]

    Operation --> Why{왜 2/3 용량?}
    Why --> Reason1["1. Infant Mortality 감지<br/>(초기 고장 발견)"]
    Why --> Reason2["2. 완전 미사용 시<br/>열화 방지"]

    style Campus fill:#fae8ff,stroke:#a855f7,stroke-width:2px
    style Option2 fill:#f0fdf4,stroke:#16a34a
    style Operation fill:#fef3c7,stroke:#f59e0b
```

**주요 구성 요소:**
- **Copper Coils**: 1차/2차 권선
- **Transformer Core**: GOES (Grain Oriented Electrical Steel)
  - **병목**: GOES 제조사가 제한적 → transformer 공급 부족의 주요 원인

**📌 Lead Time 주의**
> HV Transformer는 맞춤 제작 (각 송전선마다 특성이 다름)
> - 일반적 Lead Time: **>12개월**
> - 해결책: Datacenter 계획 단계에서 사전 주문

---

## 🟡 Data Halls and Pods

### 모듈화 구조: Microsoft Datacenter 예시

```mermaid
flowchart TD
    Campus["Campus<br/>(여러 건물)"] --> Building["Building<br/>~250k sq ft<br/>48 MW"]

    Building --> Hall1["Data Hall 1<br/>9.6 MW"]
    Building --> Hall2["Data Hall 2<br/>9.6 MW"]
    Building --> Hall3["Data Hall 3-5<br/>각 9.6 MW"]

    Hall1 --> Pod1["Pod 1<br/>2.4 MW"]
    Hall1 --> Pod2["Pod 2<br/>2.4 MW"]
    Hall1 --> Pod3["Pod 3<br/>2.4 MW"]
    Hall1 --> Pod4["Pod 4<br/>2.4 MW"]

    Pod1 --> Equipment["전용 장비:<br/>- Generator 1개<br/>- Transformer 1개<br/>- UPS 2개 (2N)<br/>- Switchgear 1개"]

    style Campus fill:#dbeafe,stroke:#3b82f6
    style Building fill:#e0e7ff,stroke:#6366f1
    style Hall1 fill:#fae8ff,stroke:#a855f7
    style Pod1 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
```

**구조 계층:**
1. **Campus**: 여러 건물 (100s MW)
2. **Building**: 단일 건물 (~50 MW)
3. **Data Hall**: 건물 내 방 (~10 MW)
4. **Pod**: Data Hall 내 모듈 (~2-3 MW)

### Pod 시스템의 장점

```mermaid
graph TD
    PodConcept[Pod 모듈화 시스템] --> Modularity[모듈성<br/>Modularity]
    PodConcept --> Standardization[표준화<br/>Standardization]

    Modularity --> ModBenefit["✅ 단계적 확장<br/>✅ 빠른 배치<br/>✅ 부하 증가 대응"]

    Standardization --> StdBenefit["✅ 범용 장비 사용<br/>✅ 조달 용이<br/>✅ 비용 절감"]

    StdBenefit --> CommonSizes["일반적 Pod 크기:<br/>- 1,600 kW<br/>- 2,000 kW (2 MW)<br/>- 2,500 kW (2.5 MW)"]

    CommonSizes --> WhyCommon["이 크기들은<br/>다양한 산업에서<br/>사용 → 저렴하고<br/>재고 풍부"]

    style PodConcept fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style ModBenefit fill:#f0fdf4,stroke:#16a34a
    style StdBenefit fill:#f0fdf4,stroke:#16a34a
    style CommonSizes fill:#fef3c7,stroke:#f59e0b
```

---

**[섹션 1-4 완료]**

다음 섹션 미리보기:
- 🔴 Generators, MV Transformers, Power Distribution
- 🔴 UPS Systems
- 🟡 OCP Racks and BBUs
- 🔴 AI Impact: Power Density 증가
- 🟡 Winners & Losers
- 🟡 CapEx Forecast

---

*작성 진행률: 약 40% 완료*
