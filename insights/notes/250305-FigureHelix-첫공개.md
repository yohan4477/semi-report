---
source: "content/understanding/피지컬AI/[250305] Figure Helix 첫 공개.md"
title: "Figure Helix 첫 공개"
date: 2025-03-05
corpus: third
lang: ko
actors: [Figure AI, 오픈AI, Physical Intelligence, 엔비디아, 보스턴 다이내믹스]
topics: [PhysicalAI, VLA, System1System2, 휴머노이드, 텔레오퍼레이션]
---

## 이 문서가 주장하는 것

Figure AI가 처음 공개한 VLA(Vision-Language-Action) 모델 Helix는 그리퍼 위치만 다루던 이전 VLA를 손가락·손목·머리·몸통까지 아우르는 고자유도 제어로 확장한 첫 사례다. 로봇 정책을 고전 제어 최적화 없이 신경망 하나로 구동하는 첫 사례이기도 하며, 진행자들은 레이턴시 우려로 피해 왔던 접근이 실제로 돌아간 데 놀란다. 판단을 맡는 느린 System 2(VLM)와 반사를 맡는 빠른 System 1(비전 모터 트랜스포머)로 나눈 이원 구조를 이 편에서 처음 밝히며, 두 신경망이 비동기로 돌아가는 탓에 학습 때 시간적 오프셋을 넣었다고 설명한다. Figure AI는 오픈AI와 결별한 직후 이 모델을 공개했는데, 그 전 화제였던 사과 집기 데모가 오픈AI 모델을 가져다 붙인 수준이었다는 비판을 이번엔 자체 하드웨어·자체 모델로 정면 돌파했다고 진행자들은 평가한다. 학습 데이터는 텔레오퍼레이션으로 모은 것을 VLM이 스스로 라벨링했을 것으로 추정한다. Physical Intelligence의 π0와 비교하면 π0는 여러 로봇 몸체에 두루 통하는 범용성을, Helix는 자기 하드웨어 하나에 최적화한 고자유도를 각각 택했다는 대비를 세운다. 문서는 GPU 종류·시간적 오프셋의 이유·데이터 수량을 모두 진행자 추정으로 못박고, 근미래 시장성에는 회의적인 평가로 마무리한다.

## 수치

- Helix는 손가락·손목·머리·몸통까지 35 자유도를 신경망 하나로 구동하며, 이전 VLA는 그리퍼 위치 7 자유도(XYZ 3 + 피치·롤·요 3 + 그리퍼 1)만 다뤘다 ([250305] Figure Helix L11)
- System 2는 7B급 VLM(진행자는 처음 8B로도 언급)으로 7~9Hz로 판단하고, System 1은 200Hz로 액션을 낸다 ([250305] Figure Helix L18)
- π0가 겨냥하는 로봇 몸체는 7~18 자유도인데 Helix는 35 자유도다 ([250305] Figure Helix L39)
- 학습 데이터는 텔레오퍼레이션으로 모은 약 500시간이다 ([250305] Figure Helix L32)
- π0의 VLM은 3B, Helix의 VLM은 7B급(진행자는 처음 8B로도 언급)이다 ([250305] Figure Helix L40)

## 저자가 추정이라고 밝힌 것

- 어떤 GPU에서 도는지 공식 공개가 없어 엔비디아 오린 계열이라는 것은 진행자의 추정이다 ([250305] Figure Helix L45)
- System 2·System 1 사이 시간적 오프셋을 왜 넣었는지 회사가 공개하지 않아 정확한 이유를 모른다고 밝힌다 ([250305] Figure Helix L46)
- 학습 데이터 500시간, GPU 두 개 분리 구동, System 1 파라미터 규모는 모두 추정이며 회사가 수치를 공개한 것이 아니다 ([250305] Figure Helix L47)
