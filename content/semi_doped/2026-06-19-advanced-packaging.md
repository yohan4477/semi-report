---
title: 레티클 한 장을 넘기는 두 가지 방법 — CoWoS 와 EMIB
date: 2026-06-19
source: https://daily.semidoped.com/p/semi-doped-advanced-packaging
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: fab
topic: 첨단 패키징 · CoWoS · EMIB
gain: 다이를 무한정 키우지 못하는 이유(레티클 858제곱밀리미터)와 그 벽을 넘는 두 갈래. 실리콘 인터포저를 한 층 더 까는 쪽과 기판 안에 브리지만 심는 쪽이 층 수·재료비·수율에서 어떻게 갈리는지, 그리고 레티클 몇 배까지 담는지의 로드맵.
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
---

## 한 줄
TSMC의 CoWoS와 Intel의 EMIB를 축으로, 첨단 패키징(advanced packaging)이 왜 필요해졌는지부터 두 기술의 구조·트레이드오프, 그리고 구글 TPU 3백만 개가 MediaTek을 거쳐 Intel EMIB로 패키징된다는 최근 소식까지 다룬 회차. 레티클(reticle) 한계를 넘어서기 위한 실리콘 인터포저·유기 기판·브리지 세 갈래 해법을 병렬로 설명한다.

## 사실 — 절 순서대로
- 오프닝 잡담. 이 회차는 스페이스X IPO 당일(6월 12일 금요일 녹음분)에 녹음됐다고 언급. Elon Musk의 Terrafab이 Intel과 연결된다는 이야기로 첨단 패키징 화제로 넘어간다.
- 단순 패키징의 정의. 패키징이란 웨이퍼가 팹을 떠난 뒤 일어나는 모든 일 — 다이(die)와 외부 세계를 잇는 전력·신호 연결, 방열, 기계적 보호까지를 포함한다고 정의.
- 와이어 본딩(wire bonding). 가장 원시적인 패키징 방식으로, PCB에서 칩까지 금속선을 연결하는 방식. AI 시대에도 전력 반도체 등에는 여전히 쓰인다고 설명.
- 플립 칩(flip chip). 1990년대에 등장한 전환점으로, 칩을 뒤집어 솔더볼로 PCB에 붙이는 방식. 연결 거리가 짧아져 기생 저항·기생 커패시턴스가 줄었다고 설명.
- OSAT의 역할. 파운드리는 완성 웨이퍼만 출하하고, Amkor·ASE·SPIL·Powertech 같은 OSAT(외주 반도체 조립·테스트 업체)가 다이싱·와이어본딩/플립칩·성형·테스트를 담당한다고 정리. 팹리스가 설계, 파운드리가 제조, OSAT가 패키징이라는 3분할 구도로 요약.
- 첨단 패키징이 필요해진 이유. 레티클 한계(reticle limit) 때문에 실리콘 다이를 무한정 크게 만들 수 없고, SRAM·IO처럼 미세화 이득이 적은 요소는 칩렛(chiplet)으로 분리해야 한다는 배경 — Clearwater Forest 사례(연산 다이는 18A, IO·메모리 다이는 Intel 3·Intel 7)를 언급.
- 레티클 한계 수치. 레티클 크기는 858mm²(26mm×33mm)로 고정돼 있고, H100이 이미 이 한계에 도달했다고 설명.
- 멀티다이 GPU. Blackwell은 두 개의 레티클 크기 GPU 다이를 하나로 묶은 구성이고, Rubin은 "네 개의 GPU 다이"가 묶일 것으로 알려져 있다고 언급(Austin, "I believe... supposed to be"라는 헤지 표현 사용).
- HBM 신호 수. HBM3는 약 1,024개 신호, HBM4는 2,048개 병렬 레인으로 늘었다는 수치를 통해 미세 인터커넥트가 왜 필요한지 설명.
- 2D·2.5D·3D 정의. 2D는 다이 하나를 기판에 얹고 배선하는 것, 2.5D는 능동 다이를 수동 실리콘(인터포저) 위에 얹는 것(active-on-passive), 3D는 능동 다이를 능동 다이 위에 쌓는 것(active-on-active)이라고 구분. HBM 내부는 3D(적층)지만 GPU와 연결된 상태로는 2.5D로 분류된다고 부연.
- CoWoS(Chip on Wafer on Substrate) 구조. GPU 다이가 실리콘 인터포저(웨이퍼) 위에 얹히고, 그 인터포저가 다시 기판(substrate) 위에 얹히는 3층 구조. TSMC가 2010년대 초 FPGA용으로 처음 양산에 투입했다고 설명(Austin은 시기를 "late 2000s or early 2010s"로 헤지).
- CoWoS-S. 인터포저가 실리콘 전체로 된 방식. 미세 배선에는 유리하지만 실리콘을 라우팅 용도로 쓰는 만큼 비용이 비싸다는 점을 지적. 재료가 파운드리급 공정을 쓰기 때문에 레티클 크기의 배수 한계(3.3배 정도)를 넘기 어렵다고 언급.
- CoWoS-R. 인터포저를 유기 RDL(재배선층, redistribution layer)로 대체한 저비용 버전. 폴리이미드 유전체에 금속층 2~3개를 패턴하는 팬아웃(fan-out) 기술에서 파생. 미세 피치가 부족해 GPU 가속기에는 못 쓰고 저가 스마트폰·차량용 칩 정도에 쓰인다고 설명.
- CoWoS-L. 유기 기판을 기본으로 쓰되, 다이와 다이가 만나는 부위에만 국소적으로 작은 실리콘 브리지를 심는 절충안. "L"은 로컬 실리콘 브리지(local silicon bridge)를 뜻한다고 설명. 레티클 크기 제약 없이 실리콘급 인터커넥트 성능을 얻을 수 있다고 정리.
- EMIB의 기원. 브리지 개념은 TSMC가 아니라 Intel이 먼저 개발했고, EMIB가 CoWoS-L보다 앞선다고 확인(Vik: "TSMC가 베꼈다"는 세간의 소송 논쟁이 있었다는 일화 언급).
- EMIB(Embedded Multi-die Interconnect Bridge) 구조. 인터포저 층 자체를 없애고, 다이를 곧바로 기판에 얹은 뒤 필요한 자리에만 작은 브리지를 기판 안에 매립(embed)하는 2층 구조. CoWoS-L(3층)과 대비되는 2층 구조라는 점을 강조.
- 패널 방식의 이점. EMIB 기판은 원형 웨이퍼가 아니라 정사각형 패널(대략 500mm×500mm) 위에서 만들어져 원형 웨이퍼 대비 웨이퍼 활용률(utilization)이 훨씬 높고 낭비가 적다고 설명 — 패널이 웨이퍼보다 5~6배 크다고 언급.
- EMIB-T와 EMIB-M. EMIB-T는 브리지를 관통하는 TSV(through-silicon via)를 넣어 전력·고속 신호 접근을 가능하게 한 버전, EMIB-M은 전력 안정화를 위한 MIM(metal-insulator-metal) 커패시터를 브리지에 내장한 버전이라고 구분.
- Intel의 EMIB 사용 이력. Intel은 약 10년간 초기 FPGA부터 CPU SoC(Sapphire Rapids, Granite Rapids 포함)까지 EMIB를 써왔다고 확인.
- EMIB 장점 정리. 3층이 아닌 2층 구조라 인터포저 다이싱·재료비가 줄고, 사각 패널 덕분에 폐기율이 낮으며, 레티클 배수 확장에 유리하고(3×3, 4×4 등으로 스케일 가능), 브리지 자체가 작아 수율이 좋다고 요약.
- EMIB 단점/리스크 논쟁. TSMC CoWoS만큼 대규모 검증 이력이 없고, Nvidia 등 다른 회사의 다이로 실제 양산된 사례가 아직 없다는 점을 단점으로 제기(Vik). Austin은 Intel 자체 물량으로는 이미 대량 검증됐다고 반박.
- EMIB 수율 논쟁. 일부에서 "EMIB 수율이 90%대"라는 이야기가 돈다는 점을 언급 — Vik는 "95%라고 읽은 적도 있다"고 덧붙임(둘 다 출처 불명확). 패키징 수율은 사실상 100%에 가까워야 한다는 반론과, 이 수치가 신뢰할 만한지에 대한 의문을 나눈다.
- 구글 TPU-MediaTek-Intel EMIB 소식. 구글의 TPU 발주 물량 중 약 300만 개가 2028년경 MediaTek을 거쳐 Intel EMIB로 패키징된다는 최근 뉴스를 소개. SK하이닉스도 HBM 통합용으로 EMIB를 테스트 중이라고 언급.
- MediaTek과 Broadcom 구도. 구글 TPU 건으로 MediaTek이 Broadcom의 커스텀 ASIC 사업 모델에 위협이 되고 있다는 시장 해석을 소개, 최근 실적 발표에서 이 흐름 전환이 언급되며 Broadcom 주가 약세와 연결짓는다.
- Intel Foundry의 광학(optics) 잠재력. Intel이 광학·포토닉스 역량을 갖고 있어 EMIB와 결합해 CPO(co-packaged optics)를 만들 수 있는 잠재력이 있다고 언급(향후 별도 회차 예고).
- Intel CFO 발언 인용. David Zinsner가 "첨단 패키징만으로도 수십억 달러 규모의 수주를 받고 있다"고 말했다는 내용을 Austin이 전달.
- 레티클 배수 스케일 로드맵(CoWoS). 1세대 CoWoS는 3.3배 레티클, 현재 Blackwell Ultra·Rubin급은 5.5배 레티클, 다음 세대는 9.5배 레티클, 그 이후 System on Wafer는 약 40배를 목표로 한다고 정리.
- EMIB 사이즈 로드맵. 현재(추정) EMIB-T 기준 8배 레티클 수준이고, 2028년까지 12배 이상 레티클(120mm×180mm 직사각형, 2×4 다이 그리드)로 확장될 예정이라고 소개(Austin: "정확히 오늘 시점 수치는 모른다"고 헤지).

## 숫자 (원문에 나온 것만)
- 레티클 한계 — 858mm²(26mm×33mm)
- HBM3 신호 수 — 약 1,024개
- HBM4 병렬 레인 — 2,048개
- CoWoS 1세대 — 레티클의 3.3배
- 현재(Blackwell Ultra·Rubin급) CoWoS — 레티클의 5.5배
- 다음 세대 CoWoS — 레티클의 9.5배
- System on Wafer 목표 — 레티클의 약 40배
- EMIB(추정 현재, EMIB-T 기준) — 레티클의 8배
- EMIB 2028년 목표 — 레티클의 12배 이상, 120mm×180mm, 2×4 다이 그리드
- 구글 TPU EMIB 발주 물량 — 약 300만 개(2028년경)
- 언급된 EMIB 수율 — 90%(일부는 95%라고 언급, 출처 불명확)
- Rubin 다이 개수 — GPU 다이 4개("supposed to be", 헤지)
- EMIB 패널 크기 — 약 500mm×500mm(웨이퍼 대비 5~6배)
- SpaceX IPO 밸류에이션 — 약 750억 달러("something like that", 헤지)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "So I think now there is no chip without the packaging." — "그래서 지금은 패키징 없이는 칩이랄 게 없다고 생각해요." (Vik)
- "EMIB predates CoWoS-L." — "EMIB가 CoWoS-L보다 먼저다." (Vik)
- "I think of pushing a piece of cracker into jello — that's the feeling I have when I think about EMIB." — "크래커를 젤리 속에 밀어 넣는 느낌, EMIB를 생각하면 그런 느낌이에요." (Vik)
- "Pavement would be like silicon — the best, but expensive." — "포장도로가 실리콘 같은 거죠 — 최고지만 비싸다." (Austin)
- "The packaging yield has to be essentially 100%... You can't lose one chip out of every ten. That's just not acceptable." — "패키징 수율은 사실상 100%여야 해요... 열 개 중 하나를 잃을 순 없죠. 그건 받아들일 수 없어요." (Vik)
- "Don't forget — advanced packaging alone, these are billions of dollars worth of commitments that we're getting." — "잊지 마세요 — 첨단 패키징만으로도 우리가 받는 수주가 수십억 달러 규모입니다." (David Zinsner, Intel CFO — Austin이 인용)

## 주의
- Rubin GPU 다이 개수(4개)는 Austin이 "I believe... there are supposed to be"라고 헤지한 진술로, 확정된 사실로 단정하지 않았다.
- EMIB 수율 수치(90%·95%)는 두 진행자 모두 출처를 명확히 못 대는 상태에서 언급한 것 — Vik는 "some sell-side reports"라고만 지칭했고 신빙성에 의문을 제기했다.
- EMIB의 현재(2026년 시점) 레티클 배수(8배)는 Austin이 "I don't know exactly what it is today... maybe that's where they are today"라고 명시적으로 불확실하다고 밝힌 추정치다.
- TSMC가 첨단 패키징에 진입한 시기("late 2000s or early 2010s")는 Austin이 헤지한 표현이다.
- SpaceX 밸류에이션(750억 달러)은 Austin이 "like $75 billion or something"이라고 어림한 수치다.
- CoWoS-S·R·L 각각의 정확한 수율은 진행자들이 "공개된 적이 없는 것 같다(I don't know if that's ever been published)"고 명시한 미공개 정보다.
