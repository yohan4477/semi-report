---
source: "content/understanding/피지컬AI/[260205] Whole-Body Control 시대의 시작.md"
title: "Whole-Body Control 시대의 시작"
date: 2026-02-05
corpus: third
lang: ko
actors: [Figure AI, Fauna Robotics, 보스턴 다이내믹스, 유니트리]
topics: [PhysicalAI, WholeBodyControl, 로코매니퓰레이션, 휴머노이드, 텔레오퍼레이션]
---

## 이 문서가 주장하는 것

Figure AI의 Helix 02는 상체만 쓰던 Helix 01과 달리 골반·다리까지 함께 움직이는 온몸 제어(whole-body control)를 자율로 시연했다. 균형을 담당하는 System 0을 기존 판단(System 2)·반사(System 1) 계층 아래 새로 넣었는데, 강화학습이 아니라 이미테이션 러닝으로 학습했다는 점이 특이하다. 학습 데이터는 사람이 온몸을 텔레오퍼레이션하되 로봇이 스스로 균형을 잡아주는 방식으로 모았다. 같은 시기에 공개된 Fauna Robotics의 소형 연구용 로봇 Sprout도 온몸 29자유도로 유사한 방향을 보여준다. 다만 Sprout는 정교한 손 대신 1자유도 집게를 택했고, 로코모션은 자세별 강화학습을 상태 머신으로 이어 붙인 구조로 진행자들은 추정한다. 문서는 팔만 쓰던 조작과 달리 온몸 제어는 균형·접촉·자유도 수가 함께 늘어나는 다른 문제라는 점을 먼저 세운 뒤, 최종 배포 모델에서도 별도의 균형 모듈이 계속 필요할지를 열린 질문으로 남긴다.

## 수치

- Helix 01은 상체만 32자유도로 움직였고 하체는 고정했다 ([260205] Whole-Body L11)
- Helix 02의 System 2는 7B, System 1은 80M, 새로 넣은 System 0은 10M 파라미터다 ([260205] Whole-Body L18, L19)
- System 0은 1000Hz(1kHz)로 돈다 ([260205] Whole-Body L19)
- Fauna Sprout는 키 107cm, 무게 22.7kg, 온몸 29자유도이며 손은 1자유도 집게다 ([260205] Whole-Body L38, L39)
- Fauna Robotics는 2년 전(재작년 2월) 설립돼 2026년 1월 28일 스텔스를 풀고 처음 공개됐다 ([260205] Whole-Body L41)
- Fauna Robotics의 투자 규모는 500억원 안팎으로 언급된다 ([260205] Whole-Body L42)

## 저자가 추정이라고 밝힌 것

- Helix 02의 데모가 테스트 셋에 오버피팅됐을 가능성을 진행자 한 명이 직접 제기한다 ([260205] Whole-Body L55)
- 촉각 센서 외에 손바닥 카메라도 쓰였을 것이라고 추정하지만 확인된 사실은 아니라고 밝힌다 ([260205] Whole-Body L34)
- Fauna Robotics 창업자 이력과 투자 단계·판매가는 진행자들도 정확히 알지 못한다고 밝힌다 ([260205] Whole-Body L56, L57)
- 로코모션이 자세별로 강화학습을 따로 학습시킨 구조라는 것은 진행자의 추정이다 ([260205] Whole-Body L46)
- 최종 배포 모델에도 RL 기반 균형 모듈이나 MPC가 남을지, 신경망에 흡수될지는 결론 내리지 않고 질문으로 남긴다 ([260205] Whole-Body L58)
