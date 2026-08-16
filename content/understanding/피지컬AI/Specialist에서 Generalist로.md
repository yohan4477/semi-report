# Specialist에서 Generalist로

> 출처: sudoremove.com 박종현(공개 웹 에세이 · fundamentals 시리즈 3/4), 2026-03-19. 원문의 **요약**이며 전문 재수록이 아님. 원문 https://sudoremove.com/knowledge/essays/fundamentals/specialist-to-generalist/ · SemiAnalysis 코퍼스와 별개의 제3자 해설로, 투자 판단 근거로 쓰지 말 것.

## 한 줄 요약
비전 AI가 과제별 특화 모델(VGGNet·YOLO·UNet)에서 통합 VLM으로 넘어간 경로를 로보틱스가 그대로 밟고 있다고 보고, 그 전환을 떠받치는 세 가지 조건(사전학습 VLM 백본, 교차 embodiment 데이터셋, 스케일링 법칙)을 정리한다.

## 핵심 포인트
- **비전 AI의 전례.** 분류·검출·분할마다 따로 있던 모델이 통합 VLM 하나로 수렴했다. 저자는 로보틱스에서 같은 일이 벌어지는 중이라고 본다.
- **Specialist와 Generalist의 차이.** 특화형은 통제된 조건에서 성능이 높지만 환경이 조금만 달라져도 무너진다. 범용형은 적용 범위가 넓고, 학습에 없던 상황을 zero-shot(사전 예시 없이)·few-shot(예시 몇 개만으로) 처리하며 세계 지식으로 추론한다.
- **조건 ①: 사전학습 VLM 백본.** PaliGemma·Qwen-VL·SmolVLM 같은 모델이 인터넷 규모 학습에서 얻은 상식을 이미 갖고 있어, 로봇이 기초부터 배울 필요가 없어졌다.
- **조건 ②: 교차 embodiment 데이터셋.** 서로 다른 로봇에서 모은 데이터를 함께 쓴다. 제조사마다 데이터를 처음부터 모아야 하는 부담이 줄어든다.
- **조건 ③: 스케일링 법칙.** 모델이 커지고 데이터가 다양해질수록 일반화가 좋아진다는 LLM의 경험칙이 로봇에도 적용될 것으로 본다.
- **현재 일반화 사례.** π0.5는 학습에 없던 환경에 적응하고, GR00T는 서로 다른 하드웨어를 오가며, SmolVLA는 4.5억(450M) 파라미터로 범용 수준의 성능을 낸다.
- **당분간의 절충은 파인튜닝.** 넓은 기반 모델에 과제별 미세조정을 얹어 특화형의 정밀도와 범용형의 유연성을 같이 가져가는 방식이 자리 잡고 있다. 웹 데이터·시뮬레이션·로봇 데이터를 함께 학습해 파인튜닝조차 필요 없게 만드는 것이 지향점이다.

## 주요 숫자(교차 embodiment 데이터셋)
| 데이터셋 | 로봇 종류 | 과제 수 | 에피소드 |
|---|---|---|---|
| Open X-Embodiment | 22종 이상 | 527 | 100만+ |
| DROID | 7종 | 500+ | 7만 6천 |
| BridgeData V2 | 1종 | 13 | 6만 |

- SmolVLA: 4.5억 파라미터로 범용 수준 성능
- 하드웨어 범위: 휴머노이드 설계 15종, 4족 보행(Spot·ANYmal), 다수의 로봇 팔과 다지 손

## 등장하는 회사·모델
| 구분 | 이름 |
|---|---|
| 회사 | 1X Technologies, 보스턴 다이내믹스, Covariant, Figure AI, 구글 딥마인드, HuggingFace, 엔비디아, Physical Intelligence, Skild AI, 테슬라, 유니트리 |
| 모델 | ACT, CraftNet, Diffusion Policy, Eagle, FAST, Figure Helix, Gemini Robotics, GEN-0, GR00T, LBM, Cosmos, Octo, OpenVLA, Redwood AI, RT, SmolVLA, Sunday ACT-1, π0·π0.5·π0.6 |

## 비유 · 표현
- **'비전 AI가 걸어간 길'**. 특화 모델 난립 → 통합 모델 수렴이라는 경로를 로보틱스의 미래 지도로 쓰는 논법.
