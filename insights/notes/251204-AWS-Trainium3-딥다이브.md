---
source: "content/newsletter/ai_infra/compute/[251204] AWS Trainium3 딥다이브 - 다가오는 잠재적 도전자.md"
title: "AWS Trainium3 Deep Dive: A Potential Challenger Approaching"
date: 2025-12-04
corpus: semi
lang: ko
actors: [AWS, 엔비디아, AMD, 구글, 삼성, SK하이닉스, 마이크론]
topics: [반도체, 랙, 네트워크]
---

## 이 문서가 주장하는 것

AWS는 구글 TPUv7 심층분석 직후 re:Invent에서 Trainium3 양산 출하와 차세대 Trainium4 로드맵을 함께 발표해, 구글 TPU·AMD와 함께 엔비디아를 다각도로 압박하는 3번째 전선을 열었다. AWS의 설계 철학은 특정 기술에 몰빵하지 않고 최저 총소유비용에 최단 기간 출시를 노리는 것이다. 핵심 하드웨어 전환은 스케일업(같은 랙 내부 칩 간 연결) 네트워크를 기존 토러스 방식에서 스위치 방식으로 바꾼 것인데, 최신 MoE(여러 전문가 모듈을 섞어 쓰는 모델) 모델이 모든 칩이 서로 통신하는 방식을 많이 써서 토러스보다 유리하기 때문이다. 소프트웨어도 내부 전용에서 PyTorch 오픈소스화로 돌아서, 엔비디아 CUDA 생태계의 개발자 저변에 맞불을 놓았다.

## 수치

- OCP MXFP8 처리량이 전세대 대비 2배, MXFP4는 MXFP8과 동일 성능, FP16·FP32는 전세대(Trn2)와 동일 유지 (Trainium3 L134)
- HBM(여러 층 쌓은 메모리)3E를 12층으로 쌓아 칩당 용량 144GB, 핀 속도를 5.7Gbps에서 9.6Gbps로 올려 대역폭 70% 증가 — 공급사를 삼성에서 SK하이닉스·마이크론으로 전환한 덕분 (Trainium3 L135)
- Trainium4는 HBM4를 8스택으로 채택해 Trainium3 대비 대역폭 4배·용량 2배를 예고 (Trainium3 L137)
- 엔비디아 밖에서 all-to-all 스위치 스케일업 랙을 실제로 처음 출하한 곳은 AWS로, AMD보다 1년 빠름 (Trainium3 L402)
- 랙 중앙에 NeuronLink 스위치 트레이 4개(스페어 포함 5개) — 엔비디아 GB200/300 NVL72는 스위치 교체 전 워크로드를 전부 빼내야 함 (Trainium3 L423)
- Trn2는 토러스 2종만 지원했지만 Trainium3는 4종 SKU(같은 세대의 별도 제품) 모두 지원, 2026년 물량 대다수는 공랭(공기로 식히는 방식) NL32x2 Switched에 집중 (Trainium3 L200)
- NL32x2 Switched 랙은 랙당 32칩, 전체 스케일업 월드는 랙 2개(64칩) (Trainium3 L422)

## 저자가 추정이라고 밝힌 것

- Trainium4의 NVLink Fusion 출시가 늦더라도 AWS는 엔비디아 통상 총마진(약 75%)보다 유리한 조건을 확보했을 가능성이 크다는 추정 (Trainium3 L326)
- 엔비디아가 계속 개발 속도를 가속하는 한 선두를 지키겠지만, 안주하면 인텔이 AMD·ARM에 추격당했듯 더 빨리 뒤처질 것이라는 경고 (Trainium3 L125)
