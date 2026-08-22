---
source: "content/understanding/피지컬AI/Specialist에서 Generalist로.md"
title: "Specialist에서 Generalist로"
date: 2026-03-19
corpus: third
lang: ko
actors: [HuggingFace, 엔비디아, Physical Intelligence, 구글 딥마인드, 보스턴 다이내믹스]
topics: [범용로봇, 교차embodiment, VLM백본, 스케일링법칙, 파인튜닝]
---

## 이 문서가 주장하는 것

비전 AI가 과제별 특화 모델에서 통합 VLM으로 수렴한 경로를 로보틱스가 그대로 밟고 있다고 본다. 전환을 떠받치는 조건을 셋으로 정리한다 — 인터넷 규모 학습에서 상식을 이미 갖춘 사전학습 VLM 백본, 서로 다른 로봇의 데이터를 함께 쓰는 교차 embodiment 데이터셋, 그리고 LLM에서 확인된 스케일링 법칙이 로봇에도 적용되리라는 기대다. 현재 위치는 완전한 범용이 아니라 절충 지점이라고 본다 — 넓은 기반 모델에 과제별 미세조정을 얹어 특화형의 정밀도와 범용형의 유연성을 함께 가져가는 방식이 자리 잡았고, 파인튜닝조차 필요 없게 만드는 것이 지향점이다.

## 수치

- Open X-Embodiment는 로봇 22종 이상, 과제 527개, 에피소드 100만 개 이상을 담는다 (Specialist에서 Generalist로 L20)
- DROID는 로봇 7종·과제 500개 이상·에피소드 7만 6천 개다 (Specialist에서 Generalist로 L21)
- BridgeData V2는 로봇 1종·과제 13개·에피소드 6만 개로, 교차 embodiment 데이터셋 셋 중 가장 좁다 (Specialist에서 Generalist로 L22)
- SmolVLA는 4.5억(450M) 파라미터로 범용 수준의 성능을 낸다 (Specialist에서 Generalist로 L24)
- 하드웨어 범위는 휴머노이드 설계 15종, 4족 보행(Spot·ANYmal), 다수의 로봇 팔과 다지 손이다 (Specialist에서 Generalist로 L25)
- 사전학습 VLM 백본으로 PaliGemma·Qwen-VL·SmolVLM이 쓰이며, 이들이 이미 가진 상식 덕에 로봇이 기초부터 배울 필요가 없어졌다 (Specialist에서 Generalist로 L11)
- 현재 일반화 사례는 학습에 없던 환경에 적응하는 π0.5와 서로 다른 하드웨어를 오가는 GR00T다 (Specialist에서 Generalist로 L14)

## 저자가 추정이라고 밝힌 것

- LLM에서 확인된 스케일링 법칙이 로봇에도 똑같이 적용될 것이라는 예상은 아직 검증되지 않았다 (Specialist에서 Generalist로 L13)
- 웹 데이터·시뮬레이션·로봇 데이터를 함께 학습해 파인튜닝 없이 쓰는 상태는 지향점이지 현재가 아니다 (Specialist에서 Generalist로 L15)
