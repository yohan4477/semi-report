---
categories: [ai-infra/memory, ai-infra/compute]
---

# ISSCC 2026 Roundup: NVIDIA & Broadcom CPO, HBM4 & LPDDR6, TSMC Active LSI, Logic-Based SRAM, UCIe-S and More

> **출처**: [https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo](https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo)
> **저자**: Dylan Patel
> **발행일**: 2026-04-16

📑 목차
 1. [ISSCC 2026 총정리 개요](#1-isscc-2026-총정리-개요)
 2. [삼성 HBM4 (Paper 15.6)](#2-삼성-hbm4-paper-156)
 3. [삼성 LPDDR6과 SF2 PHY (Paper 15.8, 37.3)](#3-삼성-lpddr6과-sf2-phy-paper-158-373)
 4. [SK하이닉스 1c LPDDR6과 GDDR7 (Paper 15.7, 15.9)](#4-sk하이닉스-1c-lpddr6과-gddr7-paper-157-159)
 5. [삼성 4F² COP D램 (Paper 15.10)](#5-삼성-4f²-cop-d램-paper-1510)
 6. [샌디스크·키오시아 BiCS10 낸드 (Paper 15.1)](#6-샌디스크키오시아-bics10-낸드-paper-151)
 7. [미디어텍 xBIT 로직 기반 비트셀 (Paper 15.2)](#7-미디어텍-xbit-로직-기반-비트셀-paper-152)
 8. [TSMC N16 MRAM (Paper 15.4)](#8-tsmc-n16-mram-paper-154)
 9. [엔비디아 DWDM과 CPO 스케일업 (Paper 23.1)](#9-엔비디아-dwdm과-cpo-스케일업-paper-231)
10. [마벨 코히런트-라이트 트랜시버 (Paper 23.2)](#10-마벨-코히런트-라이트-트랜시버-paper-232)
11. [브로드컴 6.4T 광학 엔진 (Paper 23.4)](#11-브로드컴-64t-광학-엔진-paper-234)
12. [인텔 UCIe-S 다이간 인터커넥트 (Paper 8.1)](#12-인텔-ucie-s-다이간-인터커넥트-paper-81)
13. [TSMC 액티브 LSI (Paper 8.2)](#13-tsmc-액티브-lsi-paper-82)
14. [마이크로소프트 D2D 인터커넥트 (Paper 8.3)](#14-마이크로소프트-d2d-인터커넥트-paper-83)
15. [미디어텍 디멘시티 9500 (Paper 10.2)](#15-미디어텍-디멘시티-9500-paper-102)
16. [인텔 18A-on-인텔3 하이브리드 본딩 (Paper 10.6)](#16-인텔-18a-on-인텔3-하이브리드-본딩-paper-106)
17. [AMD MI355X (Paper 2.1)](#17-amd-mi355x-paper-21)
18. [리벨리온스 Rebel100 (Paper 2.2)](#18-리벨리온스-rebel100-paper-22)
19. [마이크로소프트 마이아 200 (Paper 17.4)](#19-마이크로소프트-마이아-200-paper-174)
20. [삼성 SF2 온도 센서 (Paper 21.5)](#20-삼성-sf2-온도-센서-paper-215)

🔑 용어 정리
- **HBM4 (5세대 고대역폭 메모리)**: DRAM을 여러 층 쌓아 GPU 옆에 붙이는 AI 전용 메모리의 최신 세대 — 이번 세대부터 맨 아래층(베이스 다이)을 DRAM 공정이 아니라 로직(연산칩) 공정으로 만드는 것이 핵심 변화
- **LPDDR6**: 스마트폰 등 모바일 기기에 쓰는 저전력 DRAM의 차세대 표준 — 속도를 크게 높이면서도 배터리 소모를 줄이는 데 초점
- **GDDR7**: 게임용 그래픽카드에 주로 쓰이는 고속 메모리 — HBM보다 저렴하지만 용량과 밀도는 더 낮음
- **CPO (Co-Packaged Optics, 광학엔진 동일패키지 통합)**: 빛(광신호)으로 데이터를 주고받는 광통신 부품을 반도체 칩과 한 패키지 안에 붙여, 전기 신호보다 더 멀리, 더 적은 전력으로 데이터를 보내는 기술
- **하이브리드 본딩 (Hybrid Bonding)**: 칩과 칩을 쌓을 때 금속 돌기(범프) 없이 구리 면끼리 직접 붙이는 차세대 적층 기술 — 더 촘촘하게 쌓을 수 있지만 수율 확보가 어려움
- **UCIe-S (Universal Chiplet Interconnect Express - Standard)**: 서로 다른 회사가 만든 칩(다이)들을 하나의 패키지 안에서 표준화된 방식으로 연결하는 업계 공통 규격
- **D2D 인터커넥트 (Die-to-Die Interconnect, 다이간 인터커넥트)**: 한 패키지 안에 여러 개로 쪼갠 칩(다이)들이 서로 데이터를 주고받는 통로 — AI 가속기가 칩 하나로 안 만들고 여러 조각으로 쪼개면서 이 통로의 성능이 전체 칩 성능을 좌우하게 됨
- **MRAM (Magnetic RAM, 자기저항 메모리)**: 전원이 꺼져도 데이터가 남아있는 비휘발성 메모리 — 자동차·산업용처럼 안정성이 최우선인 곳에 주로 사용

---

## 1. ISSCC 2026 총정리 개요

**📌 핵심:**
- 매년 열리는 3대 반도체 학회(IEDM, VLSI, ISSCC) 중 마지막인 ISSCC 2026은 회로·측정 데이터 중심 발표가 특징이며, 올해는 유독 실제 산업 트렌드와 직결된 논문이 많았음
- 메모리(HBM4·LPDDR6·GDDR7·낸드·SRAM·MRAM), 인터커넥트(광통신 CPO + 다이간 전기 연결), 프로세서(모바일·서버·AI 가속기) 세 축으로 총 20개 발표를 정리
- 결론: 이번 학회는 "칩 하나를 어떻게 더 빠르게 만드나"보다 "여러 칩·여러 층을 어떻게 더 촘촘하고 저전력으로 연결하나"에 초점이 쏠려 있었음

---

ISSCC(International Solid-State Circuits Conference)는 매년 열리는 3대 반도체 학회 중 회로·집적 설계 비중이 가장 크고, 거의 모든 발표에 회로도와 실측 데이터가 함께 제시됩니다. 예년에는 산업 영향력이 들쭉날쭉했지만, 올해는 HBM4·LPDDR6·GDDR7·낸드부터 광학엔진 동일패키지 통합(CPO), 다이간 고속 연결, 미디어텍·AMD·엔비디아·마이크로소프트의 최신 프로세서까지 시장 흐름과 직결된 논문이 대거 발표됐습니다.

```mermaid
flowchart TD
    A["ISSCC 2026 총정리<br/>(20개 발표, 4대 영역)"] --> B["메모리<br/>(HBM4·LPDDR6·GDDR7·낸드·SRAM·MRAM)"]
    A --> C["인터커넥트<br/>(광통신 CPO + 다이간 전기 연결)"]
    A --> D["프로세서<br/>(모바일·서버·AI 가속기)"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef highlight fill:#fff7ed,stroke:#ea580c,stroke-width:2px;
    class A highlight;
```

---

## 2. 삼성 HBM4 (Paper 15.6)

**📌 핵심:**
- 삼성전자는 3대 메모리 기업 중 유일하게 HBM4 기술 논문을 공개, 6세대 10나노급(1c) D램 코어 + SF4 로직 공정 베이스 다이로 **36GB, 12층 적층, 2048개 입출력 핀, 3.3TB/s 대역폭**을 시연
- 베이스 다이(HBM 스택 맨 아래 중계칩)를 D램 공정 대신 로직(연산칩) 공정으로 만든 것이 HBM3E 대비 가장 큰 구조 변화 — 전력 전압(VDDQ)이 1.1V에서 0.75V로 **32% 감소**
- 다만 1c D램 공정 자체는 2025년 한 해 수율이 **약 50%**에 그쳐 아직 불안정했고, SK하이닉스 대비 신뢰성·안정성은 여전히 뒤처짐
- 결론: 삼성 HBM4는 JEDEC 표준(핀당 6.4Gb/s, 약 2TB/s) 대비 **2배 이상의 핀 속도(13Gb/s, 3.3TB/s)**를 달성해 기술 격차를 좁히고 있으나, 수율·마진 리스크는 아직 해소되지 않음

---

HBM4에서 가장 큰 구조 변화는 코어 D램 다이와 베이스 다이의 공정을 분리한 것입니다. 이전 세대까지는 코어 다이와 베이스 다이 모두 같은 D램 공정으로 만들었지만, HBM4부터는 베이스 다이만 첨단 로직 공정(SF4)으로 제작합니다.

```mermaid
flowchart TD
    Old["HBM3E까지<br/>코어 다이 + 베이스 다이<br/>모두 D램 공정으로 제작"] --> Problem["AI 워크로드가 요구하는<br/>더 높은 대역폭·데이터 속도를<br/>D램 공정만으로는 감당 어려움"]
    Problem --> New["HBM4: 베이스 다이만<br/>SF4 로직 공정으로 전환<br/>(코어 다이는 6세대 10nm급 1c D램 유지)"]
    New --> Result["VDDQ 전압 1.1V → 0.75V<br/>(32% 감소, 속도↑ 전력↓)"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef success fill:#f0fdf4,stroke:#16a34a,stroke-width:2px;
    class Result success;
```

로직 공정 베이스 다이는 트랜지스터를 더 촘촘히 넣을 수 있고 배선층도 더 많이 쌓을 수 있어, D램 공정 베이스 다이보다 면적 효율이 좋습니다. 3대 메모리 기업의 베이스 다이 공정 선택은 서로 다릅니다.

```mermaid
flowchart TD
    Choice["HBM4 베이스 다이<br/>공정 선택"] --> Sam["삼성: 자사 SF4<br/>(첨단 공정, 성능 최고<br/>대신 비용도 최고)"]
    Choice --> SK["SK하이닉스: TSMC N12<br/>(저비용 로직 공정)"]
    Choice --> Mic["마이크론: 자체 CMOS<br/>(가장 저비용)"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef highlight fill:#fff7ed,stroke:#ea580c,stroke-width:2px;
    class Sam highlight;
```

삼성은 코어 다이 TSV(층간 관통전극) 수를 4배로 늘리고, 적층 편차를 보정하는 적응형 바디 바이어스(ABB) 제어를 더해 최대 13Gb/s의 핀 속도를 달성했습니다. 또 하나의 난제는 tCCDR(서로 다른 스택ID 간 연속 읽기 명령 사이 최소 간격)로, 층수·채널 수가 16개에서 32개로 늘수록 층간 타이밍 편차가 누적돼 이 값이 나빠집니다.

```mermaid
flowchart TD
    Issue["tCCDR 문제<br/>(채널·층수 16→32로 증가<br/>→ 층간 타이밍 편차 누적)"] --> Fix["채널별 TSV RDQS<br/>자동 보정 기술 도입<br/>(전원 인가 후 편차 측정→보정회로로 상쇄)"]
    Fix --> Gain["데이터 속도<br/>7.8Gb/s → 9.4Gb/s 향상"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef success fill:#f0fdf4,stroke:#16a34a,stroke-width:2px;
    class Gain success;
```

로직 베이스 다이 전환의 또 다른 성과는 PMBIST(프로그래머블 메모리 자체 테스트)입니다. HBM3E는 베이스 다이가 D램 공정이라 전력·면적 제약 때문에 정해진 소수의 테스트 패턴만 돌릴 수 있었지만, HBM4는 실제 시스템이 보내는 것과 동일한 JEDEC 명령 전체를 임의 시점에 풀 스피드로 실행할 수 있어 양산 수율 개선에 직접 도움이 됩니다.

**📌 용어 풀이: tCCDR과 TSV 타이밍 편차**
> - **tCCDR**: 서로 다른 스택ID(칩 내 논리적 구획)에서 연속으로 읽기 명령을 처리할 때 필요한 최소 대기시간 — 이 값이 짧을수록 병렬 접근 성능이 좋음
> - **타이밍 편차의 원인**: 여러 층을 쌓다 보면 층마다 제조 편차, TSV(관통전극)를 타고 가는 신호의 전달 속도 차이, 채널별 국소 편차가 겹쳐서 층·채널 간 신호 도착 시각이 조금씩 어긋남
> - **쉬운 비유**: 12층 건물의 각 층에서 엘리베이터가 1층에 도착하는 시간이 층마다 미묘하게 다른데, 이 편차를 자동으로 재고 보정해 모든 층이 동시에 도착한 것처럼 맞추는 것과 비슷

삼성 HBM4는 JEDEC 공식 표준(JESD270-4, 핀당 최대 6.4Gb/s, 약 2TB/s)을 2배 이상 웃도는 핀당 13Gb/s, 3.3TB/s 대역폭을 시연했습니다. VDDC/VDDQ를 1.05V/0.75V로 낮춰도 11.8Gb/s를 유지합니다. 다만 1c 전공정 자체가 까다로워 2025년 한 해 수율이 약 50%에 머물렀고(1b 노드를 건너뛰고 1a에서 바로 1c로 전환한 영향), 삼성 HBM은 역사적으로 SK하이닉스보다 마진이 낮았던 만큼 이 수율 리스크가 HBM4 마진에도 부담으로 작용할 수 있습니다.

---

## 3. 삼성 LPDDR6과 SF2 PHY (Paper 15.8, 37.3)

**📌 핵심:**
- 삼성과 SK하이닉스가 나란히 LPDDR6을 공개, 삼성은 다이 하나를 **2개 서브채널**로 나누고 안 쓰는 서브채널을 꺼서 전력을 아끼는 **효율 모드**를 채택 — 다만 이 구조 때문에 다이 면적의 약 5%를 주변회로가 추가로 차지
- 신호 방식은 GDDR7과 달리 PAM3가 아닌 **와이드 NRZ**(서브채널당 12개 핀, 버스트 길이 24)를 사용, 대역폭 계산 시 오류정정(ECC)·전력절감용 비트(DBI) 32개를 제외해야 함(예: 12.8Gb/s → 실효 34.1GB/s)
- 전력 도메인을 세분화해 **읽기 전력 27% 감소, 쓰기 전력 22% 감소**를 달성했고, SF2 공정으로 만든 별도 PHY 칩은 효율 모드에서 읽기 39%·쓰기 29% 절감, 클럭게이팅까지 더하면 최대 약 50% 절감
- 결론: 삼성 LPDDR6은 12.8~14.4Gb/s 구간에서 동작하지만 밀도(0.360Gb/mm²)가 기존 LPDDR5X 1b 공정(0.447Gb/mm²)보다 낮아, 아직 성숙하지 않은 1b 공정에서 만든 시제품으로 추정됨

---

LPDDR6은 다이 하나를 2개의 서브채널로 나누고, 각 서브채널에 16개 뱅크를 배치하는 구조입니다. 평소에는 두 서브채널을 모두 쓰는 일반 모드로 동작하지만, 절전이 필요할 때는 보조 서브채널의 전원을 끄고 주 서브채널이 32개 뱅크를 전부 제어하는 효율 모드로 전환할 수 있습니다. 다만 이 경우 보조 서브채널 접근 시 지연시간이 늘어나는 손해가 있습니다.

```mermaid
flowchart TD
    Chip["LPDDR6 다이 1개"] --> Normal["일반 모드<br/>(2개 서브채널 동시 동작<br/>각 16개 뱅크)"]
    Chip --> Eff["효율 모드<br/>(보조 서브채널 전원 차단<br/>주 서브채널이 32개 뱅크 전담)"]
    Eff --> Cost["대신 보조 채널 접근 시<br/>지연시간 증가 + 주변회로<br/>중복으로 다이 면적 약 5% 손실"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef warn fill:#fff7ed,stroke:#ea580c,stroke-width:2px;
    class Cost warn;
```

신호 방식은 GDDR7의 PAM3(한 신호에 여러 값을 실어 보내는 방식)와 달리, LPDDR6은 일반 NRZ(신호를 0/1 두 값으로만 보내는 가장 단순한 방식)로는 여유(eye margin)가 부족해 서브채널당 12개 핀, 버스트 길이 24를 쓰는 "와이드 NRZ"를 사용합니다.

```mermaid
flowchart TD
    Burst["12핀 × 버스트 24 = 288비트"] --> Extra["나머지 32비트 추가<br/>(16비트 메타데이터/ECC<br/>+ 16비트 DBI 전력절감 플래그)"]
    Extra --> Formula["실효 대역폭 = 데이터 속도 × 24 × 32 / 36"]
    Formula --> Ex["예: 12.8Gb/s → 34.1GB/s<br/>14.4Gb/s → 38.4GB/s"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef highlight fill:#fff7ed,stroke:#ea580c,stroke-width:2px;
    class Ex highlight;
```

**📌 용어 풀이: DBI (Data Bus Inversion, 데이터 버스 반전)**
> - **의미**: 한 번에 보낼 신호 중 절반 이상이 0→1 또는 1→0으로 바뀔 것 같으면, 차라리 전체 비트를 반전시켜 보내고 반전 여부만 플래그 1비트로 알려주는 절전 기법
> - **효과**: 한 번에 스위칭하는 신호 수를 버스 폭의 절반 이하로 제한해 전력 소모와 신호 잡음을 줄임
> - **쉬운 비유**: 편지에서 대부분 문장이 반대말이면, 원문 대신 "전부 반대로 읽으세요"라는 메모 한 줄만 보내는 것과 비슷

삼성은 저전력 상태(3.2Gb/s 이하로 대기 상태에 있을 때가 대부분)에 쓰는 전압 도메인을 세밀하게 나눠, 읽기 전력을 27%, 쓰기 전력을 22% 줄였습니다. 배선을 물리적으로 가깝게 재배치하는 RDL(재배선층) 기법도 함께 적용해 고주파에서 필수적인 타이밍 여유를 확보했습니다. 이 시제품은 0.97V에서 12.8Gb/s, 1.025V에서 최대 14.4Gb/s를 기록했지만, 16Gb 다이 기준 밀도가 0.360Gb/mm²로 기존 LPDDR5X 1b 공정(0.447Gb/mm²)보다 낮고 오히려 구형 1a 공정(0.341Gb/mm²)에 가까워, 아직 성숙 전인 1b 공정 시제품으로 추정됩니다.

별도로 공개된 SF2 공정 PHY(Paper 37.3)는 LPDDR6 인터페이스 전용 칩으로, 최대 14.4Gb/s를 지원하며 배선 폭 2.32mm·면적 0.695mm²에 대역폭 밀도 16.6Gb/s/mm(배선 1mm당) 및 55.3Gb/s/mm²(면적 1mm²당)를 달성했습니다.

```mermaid
flowchart TD
    PHY["SF2 LPDDR6 PHY"] --> Base["효율 모드만 적용<br/>읽기 -39% / 쓰기 -29%"]
    PHY --> Gate["효율 모드 + 클럭게이팅<br/>(안 쓰는 서브채널<br/>클럭까지 차단)"]
    Gate --> Max["읽기·쓰기 약 -50%<br/>대기전력 -41%"]

    classDef default fill:#eff6ff,stroke:#3b82f6,stroke-width:1px;
    classDef success fill:#f0fdf4,stroke:#16a34a,stroke-width:2px;
    class Max success;
```

---

*작성 진행률: 약 20% 완료 (1~3장 작성)*
*업데이트: ISSCC 2026 개요, 삼성 HBM4, 삼성 LPDDR6/SF2 PHY 섹션 작성*
