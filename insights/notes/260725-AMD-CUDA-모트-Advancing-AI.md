---
source: "content/newsletter/ai_infra/compute/[260725] AMD는 CUDA 모트를 깰 수 있는가 - AMD Advancing AI 2026.md"
title: "Can AMD break the CUDA Moat? AMD Advancing AI 2026"
date: 2026-07-25
corpus: semi
lang: ko
actors: [AMD, 엔비디아, 메타, 마이크로소프트, 앤트로픽, 오픈AI]
topics: [GPU소프트웨어스택, 랙설계, 추론]
---

## 이 문서가 주장하는 것

SemiAnalysis는 AMD가 CUDA 소프트웨어 장벽을 깰 확률을 2023년 "0%"에서 이번 리포트 "두 리스크만 해결하면 성공 확률 높음"으로 세 번째 상향했다. Anthropic이 AMD 칩 2기가와트 배치를 공식화했고, 2023년 품질 문제로 AMD를 버렸던 Microsoft도 이번에 MI455X Helios로 복귀했다는 것이 근거다. 다만 두 리스크가 남는다 — 랙 시스템 Helios가 케이블 없는 트레이 설계를 못 써서 조립이 오래 걸리고, 신호 회로가 약해 리타이머까지 대량으로 들어가고, AMD 내부 개발·자동검증(CI)용 GPU 클러스터가 만성 부족해 개선 속도를 발목잡는다. 다만 코딩 에이전트가 사람 엔지니어의 일을 대신하면서 CUDA 소프트웨어 장벽의 상대적 중요성 자체가 낮아지고 있다는 게 저자들의 진단이다.

## 수치

- SemiAnalysis는 AMD의 CUDA 소프트웨어 장벽 돌파 확률을 2023년 "0%"→2025년 4월 "의미 있는 성공 가능성"→이번 리포트 "두 리스크만 해결하면 성공 확률 높음"으로 올렸다 (CUDA 모트 L52)
- Anthropic은 AMD 칩 2기가와트 배치를 공식 발표했고, MI300X 품질 문제로 2023년 AMD를 이탈했던 Microsoft도 MI455X Helios로 복귀했다 (CUDA 모트 L53)
- 쿠버네티스용 Pollara NIC의 자동검증(CI) 매칭률은 엔비디아 ConnectX 대비 0%다 (CUDA 모트 L87)
- AMD 경영진이 내부 용량 부족을 이유로 vLLM 팀 전용 클러스터를 재배치하며 매칭률 90% 목표가 후퇴했다 (CUDA 모트 L88)
- MI455X는 AMD가 데이터센터용 2나노 실리콘을 세계 최초로 출하하는 칩이다 (CUDA 모트 L131)
- MI455X는 HBM4(여러 층 쌓은 메모리) 12스택으로 패키지당 432GB를 담아 엔비디아·구글의 8스택 288GB보다 크지만, 대역폭은 23.3TB/s로 Rubin의 22TB/s와 거의 같다 (CUDA 모트 L133)
- Meta가 주문한 MI455X 대부분은 연산 다이 8개→4개, HBM 12스택→6스택으로 줄인 절반 사양이다 (CUDA 모트 L177)
- Helios 백플레인 최대 85%에 리타이머(신호 재증폭 칩)가 필요하고 랙당 550개가 넘는다. 랙당 백플레인 44,352달러에 플라이오버 케이블 24,576달러를 더해 68,928달러다 (CUDA 모트 L79, L241, L242)
- DeepSeek-R1(전문가 256개) 기준 광역 전문가 병렬화로 8GPU를 64GPU로 넓히면 GPU당 담당 전문가가 32개→4개로 줄어, 엔비디아 기준 처리량이 최대 2.28배 늘었다 (CUDA 모트 L458)
- MI455X 서버는 약 240kW(순수 IT 전력)를 써 GB300 NVL72의 약 142kW보다 높다 (CUDA 모트 L539)
