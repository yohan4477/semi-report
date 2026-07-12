---
categories: [ai-infra/memory, ai-infra/compute, ai-infra/cooling]
---

# EMIB-T Roadmap, Custom HBM, HBM4 Packaging Challenges, Microfluidic Cooling, Photonic Interconnects, and More

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/ectc2026)
> **저자**: Afzal Ahmad, DC, Gerald Wong, Dylan Patel
> **발행일**: 2026-02-05

---

## 📑 목차

### 전체 섹션
 1. [ECTC 2026 총정리 개요](#1-ectc-2026-총정리-개요)
 2. [인텔 EMIB-T 로드맵 - 브릿지 패키징의 다음 세대](#2-인텔-emib-t-로드맵---브릿지-패키징의-다음-세대)
 3. [마벨 커스텀 HBM - 표준을 버리고 얻는 것](#3-마벨-커스텀-hbm---표준을-버리고-얻는-것)
 4. [삼성 HBM 인터포저 - 배선 복잡도와 커패시터 배치](#4-삼성-hbm-인터포저---배선-복잡도와-커패시터-배치)
 5. [삼성 HBM 하이브리드 본딩 열특성](#5-삼성-hbm-하이브리드-본딩-열특성)
 6. [마이크로플루이딕 냉각 - TSMC와 마이크로소프트](#6-마이크로플루이딕-냉각---tsmc와-마이크로소프트)
 7. [마벨 광학 인터커넥트 - OMIB와 포토닉 패브릭](#7-마벨-광학-인터커넥트---omib와-포토닉-패브릭)
 8. [Lightmatter Passage M1000 - 멀티 레티클 포토닉 인터포저](#8-lightmatter-passage-m1000---멀티-레티클-포토닉-인터포저)
 9. [하이브리드 본딩 경쟁 - 저온·미세피치 접근법](#9-하이브리드-본딩-경쟁---저온미세피치-접근법)
10. [인터포저 대안 - 원형 웨이퍼 한계 우회](#10-인터포저-대안---원형-웨이퍼-한계-우회)
11. [열계면 소재(TIM) - 액체금속과 다이아몬드 접합](#11-열계면-소재tim---액체금속과-다이아몬드-접합)
12. [유리 기판 - SeWaRe 균열과의 싸움](#12-유리-기판---seware-균열과의-싸움)
13. [RDL 스케일링 - 서브마이크론 시대로](#13-rdl-스케일링---서브마이크론-시대로)
14. [적층 메모리 - 삼성의 TSV 없는 VCS 구조](#14-적층-메모리---삼성의-tsv-없는-vcs-구조)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **EMIB-T (Embedded Multi-die Interconnect Bridge with TSV)**: 인텔의 실리콘 브릿지 패키징 기술 — 패키지 전체를 덮는 판 대신, 필요한 자리에만 작은 실리콘 조각(브릿지)을 파묻어 옆 칩들을 초고속으로 연결
- **인터포저 (Interposer)**: 여러 칩(다이)을 패키지 안에서 이어주는 중간 배선판 — 브릿지가 필요한 부분에만 있는 국소 부품이라면, 인터포저는 패키지 전체를 덮는 배선판
- **커스텀 HBM (Custom HBM)**: 업계 표준(JEDEC) 규격 대신 메모리와 가속기 사이 연결 방식을 특정 회사에 맞춰 새로 설계한 HBM — 호환성을 포기하는 대신 전력·성능·면적을 더 아낄 수 있음
- **하이브리드 본딩 (Hybrid Bonding)**: 범프(금속 돌기) 없이 구리 면과 면을 직접 맞붙여 칩을 쌓는 차세대 적층 기술 — 더 촘촘하게 연결할 수 있지만 표면이 완벽히 평평하고 깨끗해야 함
- **마이크로플루이딕 냉각 (Microfluidic Cooling, 칩 내장형 물길 냉각)**: 냉각수를 칩 표면(또는 칩 내부에 새긴 미세 통로)에 직접 흘려보내는 냉각 방식 — 기존 냉각판보다 열원에 훨씬 가까이 접근해 더 많은 열을 뽑아냄
- **CPO (Co-Packaged Optics, 광학엔진 동일패키지 통합)와 포토닉 인터포저**: 빛으로 데이터를 주고받는 광통신 부품을 반도체 패키지 안에 함께 넣는 기술 — 전기 신호보다 멀리, 적은 전력으로 데이터 전송
- **RDL (Redistribution Layer, 재배선층)**: 칩의 원래 배선 위치를 패키지의 다른 위치로 옮겨주는 얇은 배선층 — 여러 칩을 하나의 패키지에 모을 때 배선을 다시 그려주는 역할
- **TIM (Thermal Interface Material, 열계면 소재)**: 칩과 방열판 사이의 미세한 틈을 메워 열이 잘 전달되게 하는 물질 — 틈에 남는 공기(단열재 역할)를 없애는 것이 목적

---

## 1. ECTC 2026 총정리 개요

**📌 핵심:**
- 트랜지스터 미세화 속도가 둔화되며 반도체 성능을 끌어올리는 주된 방법이 **첨단 패키징**으로 넘어갔는데, 이제는 AI 가속기가 너무 커지고 연결 속도 요구도 높아져 **패키지 자체가 한계**에 부딪히기 시작
- 원형 실리콘 인터포저는 패키지 크기·웨이퍼 활용률을 제약하고, HBM4E는 입출력 핀 수를 2배로 늘리며 속도까지 높이고, 수 킬로와트급 패키지는 기존 냉각 방식을 압도
- ECTC(반도체 패키징 최대 학회) 2026은 실제 상용 제품과 맞닿은 발표가 유독 많았음: 인텔은 EMIB-T 구조·로드맵을, 마벨은 커스텀 HBM으로 인터페이스 로직을 가속기 밖으로 빼내는 방법을, TSMC·마이크로소프트는 냉각수를 실리콘에 직접 주입하는 기술을, 마벨·Lightmatter는 광학 인터커넥트를 패키지에 통합하는 방법을 각각 공개
- 결론: 이 문서는 향후 수년간 AI 가속기 패키지를 좌우할 ECTC 2026의 핵심 기술 14개 주제를 정리함

---

```mermaid
flowchart TD
    A["반도체 성능 향상의 축<br/>트랜지스터 미세화 둔화"] --> B["첨단 패키징이<br/>주된 스케일링 수단으로 부상"]
    B --> C["AI 가속기 대형화 +<br/>초고속 연결 요구"]
    C --> D["패키지 자체가<br/>한계에 도달"]

    style B fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style D fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

```mermaid
flowchart TD
    Limit["패키지가 부딪힌 3대 한계"] --> L1["원형 실리콘 인터포저<br/>패키지 크기·웨이퍼 활용률 제약"]
    Limit --> L2["HBM4E<br/>입출력 핀 2배 + 속도 상승"]
    Limit --> L3["수 킬로와트급 패키지<br/>기존 냉각 방식 압도"]

    style Limit fill:#eff6ff,stroke:#3b82f6
    style L3 fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

```mermaid
flowchart TD
    ECTC["ECTC 2026<br/>(핵심 주제 14개)"] --> G1["패키징 브릿지·인터포저<br/>(인텔 EMIB-T·마벨 커스텀 HBM·<br/>삼성 인터포저)"]
    ECTC --> G2["냉각<br/>(TSMC·마이크로소프트<br/>마이크로플루이딕 냉각, TIM)"]
    ECTC --> G3["광학·기타<br/>(마벨·Lightmatter 광학,<br/>유리기판·RDL·적층메모리)"]

    style ECTC fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

이번 ECTC는 인텔이 최다 발표(12건)를 낸 학회였고, 삼성이 11건으로 뒤를 이었습니다. 반면 TSMC는 단 3건에 그쳤는데, 이는 발표량이 적다기보다 상용화 임박 기술 위주로 선별 공개했기 때문으로 보입니다.

---

## 2. 인텔 EMIB-T 로드맵 - 브릿지 패키징의 다음 세대

**📌 핵심:**
- 인텔은 ECTC 최다 발표 기업(12건)이었고 핵심은 **EMIB-T** — TSV(관통전극)를 더한 차세대 EMIB로, 구글 TPU v9에 쓰일 것으로 예상되며 대형 AI 가속기 패키지에서 TSMC CoWoS의 가장 유력한 대안으로 꼽힘
- 범프(연결 돌기) 간격을 기존 45µm에서 **36/35µm로 축소**(범프 밀도 +65%)했고, 240×240mm(약 67레티클) 대형 패키지 시험차량까지 검증했으나 부스 샘플에서 **심각한 휨(warpage)**이 관찰됨
- 브릿지에 TSV를 추가해 전력을 브릿지로 직접 전달하는 방식으로 **DC 전압강하를 68\~80% 감소**시켰고, MIM 커패시터로 전력분배망(PDN) AC 임피던스를 **82% 이상 개선**
- 결론: EMIB-T는 12Gb/s 이상 HBM4E 신호 품질(등화기 적용 시 아이 폭 약 72.5%)까지 확보하며 격차를 좁히고 있지만, TSMC는 이미 커패시터 내장·전압조정기 통합·액티브 LSI를 양산 중이라 인텔은 여전히 추격 중

---

### 범프 피치 축소와 대형 패키지 검증

```mermaid
flowchart TD
    P1["Granite Rapids<br/>45µm 피치"] --> P2["EMIB-T 2배 레티클 검증<br/>36/35µm (범프 밀도 +65%)"]
    P2 --> P3["4.5배 레티클로 검증 확장<br/>(2026년 말 인증 목표)"]
    P3 --> P4["다음 단계: 25µm 피치<br/>(1레티클 다이 2개 +<br/>3mm×18mm 브릿지)"]

    style P2 fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style P4 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

Granite Rapids-AP는 70mm×105mm(약 9레티클)의 대형 패키지였는데, EMIB-T는 이보다 훨씬 촘촘한 피치를 검증하고 있습니다. 다만 피치를 더 줄이면 새로운 문제가 생깁니다.

```mermaid
flowchart TD
    Below["25µm 미만 피치"] --> Solder["범프당 솔더(땜납)<br/>부피 급감"]
    Solder --> Risk["단락·단선·조립 수율 저하<br/>위험 증가"]
    Risk --> Shift["한계 요인 이동:<br/>브릿지 배선 밀도 →<br/>범프 형성·정렬·조립 수율"]

    style Risk fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

### 대형 패키지의 벽 - 쿼터패널과 휨(Warpage)

```mermaid
flowchart TD
    Size["EMIB-T 패키지 크기 로드맵"] --> GR["그래나이트 래피즈-AP<br/>70×105mm (약 9레티클)"]
    Size --> QP["쿼터패널 시험차량<br/>240×240mm (약 67레티클)<br/>부스 샘플에서 심각한 휨 관찰"]
    QP --> Constraint["기판 취급·휨·오버레이·<br/>패널 단위 패터닝이<br/>1차 제약 조건으로 부상"]

    style QP fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Constraint fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

인텔은 전체 패널 크기까지도 가능하다고 밝혔지만, 실제로는 쿼터패널을 현실적 목표로 제시했습니다. 이 정도 크기에서는 첨단 리소그래피 기법으로 오버레이(패턴 정렬 정밀도)를 유지하는 방안도 함께 검토 중입니다.

### 브릿지 내부 구조 - TSV로 전력을 직접 전달

EMIB-T는 단순한 수동 배선 브릿지가 아닙니다. TSV, 추가 금속층, 전력망(Power Mesh), MIM 커패시터층까지 더해 브릿지 하나가 고밀도 신호와 수직 전력 전달을 동시에 감당합니다. 인텔이 공개한 단면에는 10개 금속층(그중 4개가 배선 전용층)과 M1\~M2 사이 MIM 커패시터가 포함돼 있습니다.

```mermaid
flowchart TD
    Old["기존 EMIB<br/>전력을 기판 통해 수직 전달<br/>브릿지 근처는 옆으로 우회"] --> New["EMIB-T: 브릿지에<br/>TSV(관통전극) 추가<br/>전력을 브릿지로 바로 전달"]
    New --> Result["DC 전압강하<br/>68~80% 감소"]

    style New fill:#fff7ed,stroke:#ea580c,stroke-width:2px
    style Result fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

### HBM4E가 어려운 이유 - 신호와 전력의 동시 확장

HBM4E는 인터커넥트가 신호밀도와 전력전달을 동시에 확장해야 하는 난제를 안고 있습니다. HBM4는 HBM3 대비 핀 수가 2배로 늘고, PHY에는 VDDQ·VDDQL 같은 전력레일이 추가로 필요한데, 이 레일들이 배선 면적을 잠식해 남은 공간의 신호밀도를 더 끌어올립니다.

```mermaid
flowchart TD
    Problem["HBM4E 난제<br/>핀 수 2배(HBM3 대비) +<br/>VDDQ·VDDQL 전력레일 추가"] --> Squeeze["전력레일이 배선면적 차지<br/>→ 남은 공간 신호밀도 상승"]
    Squeeze --> Fix["대응: 가장 긴 신호는<br/>깨끗한 배선층에 배치<br/>(M9는 최장경로의 28%만<br/>최혼잡 구간 통과,<br/>M3는 84%지만 경로가 짧음)"]

    style Problem fill:#fef2f2,stroke:#dc2626,stroke-width:2px
    style Fix fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

### MIM 커패시터와 신호 품질 - 실측 결과

전력전달은 브릿지 안으로도 이동하고 있습니다. EMIB-M이 도입한 M1\~M2 사이 MIM 커패시터를 EMIB-T가 계승해, 커패시턴스 밀도 500 fF/µm²(인텔 18A급과 비슷한 수준)를 달성했습니다.

```mermaid
flowchart TD
    MIM["EMIB-T 브릿지 내<br/>MIM 커패시터<br/>(500fF/µm², 인텔 18A급)"] --> Impedance["PDN(전력분배망)<br/>AC 임피던스<br/>82% 이상 개선"]

    style Impedance fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

```mermaid
flowchart TD
    Signal["12Gb/s HBM4E 신호 품질<br/>(UI 아이 폭, 클수록 좋음)"] --> NoDFE["등화 없음: 약 67%"]
    Signal --> DFE["1-tap DFE 적용: 약 72.5%"]
    Signal --> High["12.8~16Gb/s 전 구간<br/>60% 이상 유지"]

    style DFE fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

**📌 용어 풀이: DFE(결정귀환등화기)와 UI 아이 폭**
> - **DFE (Decision Feedback Equalizer)**: 신호가 패키지 배선을 지나며 이전 비트의 잔상이 다음 비트를 방해하는 간섭을 수신단에서 계산해 제거하는 회로
> - **UI 아이 폭 (Unit Interval Eye Width)**: 한 비트를 정확히 읽을 수 있는 시간 여유의 비율 — 클수록 신호를 오판독할 위험이 적음

### 향후 로드맵과 TSMC 대비 격차

```mermaid
flowchart TD
    Roadmap["인텔 EMIB 향후 로드맵"] --> R1["고밀도 온브릿지 MIM +<br/>대형 고종횡비 브릿지"]
    Roadmap --> R2["서브 25µm 피치 +<br/>능동 브릿지"]
    Roadmap --> R3["브릿지 내장 전압조정기 +<br/>기판 매립 DTC"]
    R3 --> Gap["다만 TSMC는 이미<br/>DTC/eDTC·전압조정기·<br/>액티브 LSI 양산 중<br/>→ EMIB-T는 격차를 좁히는 중"]

    style Gap fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

인텔은 기판 코어에 매립하는 딥트렌치 커패시터(DTC)와 베이스 다이 아래 매립하는 2.5 µF/mm² 이상의 eMIM-T 커패시터 개념도 공개했지만, 아직 실제 출하 제품에는 적용되지 않았습니다.

---

## 3. 마벨 커스텀 HBM - 표준을 버리고 얻는 것

**📌 핵심:**
- 표준 HBM은 JEDEC 규격에 따라 메모리와 가속기 사이 인터페이스가 고정돼 어떤 메모리사 제품과도 호환되지만, 패키지가 커지고 HBM 속도가 오를수록 전력·성능·면적 최적화가 어려워짐
- 마벨 커스텀 HBM은 D램 코어는 그대로 두고 **베이스 다이만 첨단 로직 공정으로 재설계** — HBM 컨트롤러·관리기능·커스텀 로직·확장 인터페이스까지 베이스 다이로 옮겨, 가속기 칩에서 HBM 관련 회로가 차지하는 면적을 **약 60% 절감**
- 예시 설계는 1024채널×32Gb/s로 **4.1TB/s**를 구현(2048비트 JEDEC HBM4(E) 16Gb/s와 동급 대역폭)하면서도, 인터포저 배선 길이를 6.5mm에서 **1.5mm로 단축**해 배선층 9개·2/2µm 배선폭을 그대로 유지
- 결론: 엔비디아 Feynman도 커스텀 HBM을 채택할 예정(현재 루빈 GPU 다이 면적의 약 16%가 HBM 관련 회로)이며, 확장 인터페이스로 LPDDR 등 추가 메모리를 붙일 수 있어 AMD MI450·MI500의 LPDDR 지원 전략과도 맞닿아 있음

---

### JEDEC 표준의 트레이드오프

```mermaid
flowchart TD
    JEDEC["JEDEC 표준 HBM<br/>고정된 인터페이스"] --> Good["장점: 어떤 메모리사<br/>HBM이든 호환 가능"]
    JEDEC --> Bad["단점: 가속기가 표준 PHY +<br/>넓은 평행 인터페이스를<br/>그대로 구현해야 함<br/>→ 전력·성능·면적 최적화 어려움"]

    style Bad fill:#fef2f2,stroke:#dc2626,stroke-width:2px
```

마벨은 2024년 Industry Analyst Day에서 커스텀 HBM을 처음 언급했고, Hot Chips 2025에서 베이스 다이 플로어플랜을, 이번 ECTC에서야 패키지 레벨 세부 설계를 공개했습니다.

### 커스텀 HBM 구조 - 베이스 다이로의 이전

```mermaid
flowchart TD
    Custom["커스텀 HBM<br/>(D램 코어는 그대로)"] --> Base["베이스 다이만<br/>첨단 로직 공정으로 재설계"]
    Base --> Content["HBM 컨트롤러 +<br/>관리·모니터링 + 커스텀 로직 +<br/>확장 인터페이스 통합"]
    Content --> Save["가속기 다이의<br/>HBM 관련 면적 약 60% 절감"]

    style Save fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

### 성능·배선 개선 실측치

```mermaid
flowchart TD
    Perf["마벨 예시 설계"] --> BW["1024채널×32Gb/s<br/>= 4.1TB/s<br/>(2048비트 JEDEC 16Gb/s와 동급)"]
    Perf --> Route["인터포저 배선 길이<br/>6.5mm → 1.5mm<br/>(배선층 9개·2/2µm 그대로 유지)"]

    style BW fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
```

이 예시는 실리콘 대신 유기물 재배선층(RDL) 인터포저를 사용해 패키징 비용을 낮췄습니다. 유기 RDL은 CoWoS-S 실리콘 인터포저나 CoWoS-L·EMIB-T의 실리콘 브릿지보다 배선폭이 훨씬 굵어 레이아웃이 까다로운데, 마벨은 구간별 맞춤 차폐·배선 패턴으로 대역폭 밀도를 높이면서 신호 간섭을 제어했습니다.

### 확장 인터페이스와 업계 파급 효과

```mermaid
flowchart TD
    Expand["베이스 다이가<br/>2차 메모리 컨트롤러 역할"] --> More["LPDDR(대용량·저대역폭) 또는<br/>HBM 2차 레이어로 확장 가능"]
    More --> Nvidia2["엔비디아 Feynman:<br/>커스텀 HBM 채택 예정<br/>(루빈 GPU 다이 면적 약 16%가<br/>HBM 관련 회로)"]
    More --> AMD2["AMD MI450·MI500:<br/>LPDDR 지원으로<br/>메모리 용량 확장"]

    style Nvidia2 fill:#fff7ed,stroke:#ea580c,stroke-width:2px
```

이런 확장 인터페이스는 모든 메모리 트래픽을 제한된 다이 가장자리로만 몰아넣지 않고, 베이스 다이가 2차 메모리 컨트롤러 역할을 하며 외부 I/O에 쓸 다이 가장자리 공간을 아끼면서도 용량을 늘릴 길을 열어줍니다.

---

*작성 진행률: 약 21% 완료*
*업데이트: 헤더·목차·용어 정리 및 1\~3장(개요, 인텔 EMIB-T, 마벨 커스텀 HBM) 작성 완료*
