---
source: "content/understanding/피지컬AI/[260722] General Intuition MIRA는 훈련장이다.md"
title: "General Intuition MIRA는 훈련장이다"
date: 2026-07-22
corpus: third
lang: ko
actors: [General Intuition, Decart]
topics: [PhysicalAI, 월드모델, 에이전트훈련, 게임데이터, 밸류에이션]
---

## 이 문서가 주장하는 것

General Intuition은 게임 클립 플랫폼 Medal에서 스핀오프해 월드모델 MIRA를 만들었고, OpenAI의 5억 달러 인수 제안을 거절한 뒤 지금은 23억 달러 밸류를 받는다. 진행자들은 ICML 현장에서 5B 파라미터 모델이 B200 GPU 한 장으로 4인 시점을 동시에 생성하는 데모를 직접 플레이했다. 이 회사가 진짜 관심 있는 것은 월드모델 자체가 아니라 그걸로 만드는 에이전트라는 것이 이 편의 핵심이다 — 게임 데이터를 훈련장으로 쓰고 현실 세계를 그다음 게임으로 취급하는 프레이밍이다. 회사가 지목한 목표는 매니퓰레이션(조작)이 아니라 의미론적 추정이 들어간 내비게이션 에이전트다. 같은 시장에서 실시간 영상 자체를 파는 Decart(밸류에이션 40억 달러, API 초당 0.02달러)와 대조하며, 두 회사 모두 컨텍스트 윈도우가 짧아 사고나 긴 기억이 필요한 순간에 장면이 깨지는 한계를 공유한다는 것도 짚는다. 학습 데이터 양이나 인퍼런스 최적화 여부는 회사가 직접 답했지만, 정확한 데이터 규모는 "유튜브 스케일"이라는 말 이상으로 공개되지 않았다.

## 수치

- OpenAI의 인수 제안 5억 달러(약 7,500억 원)를 거절했다 ([260722] General Intuition L10)
- 현재 밸류에이션은 23억 달러로 거절한 제안액의 다섯 배를 넘겼다 ([260722] General Intuition L11)
- MIRA는 5B 파라미터, B200 GPU 한 장, 20Hz, 컨텍스트 윈도우 4초로 돌아간다 ([260722] General Intuition L16)
- Decart는 밸류에이션 40억 달러(약 6조 원), API 가격은 초당 0.02달러다 ([260722] General Intuition L27)
- Decart CEO는 군복무 포함 4년 만에 테크니언을 졸업하고 23세에 박사 학위를 받았다 ([260722] General Intuition L31)

## 저자가 추정이라고 밝힌 것

- MIRA의 컨텍스트 윈도우 4초는 지형이 부서지는 등 오래 기억해야 하는 게임에는 한계가 있을 것이라고 본다 ([260722] General Intuition L35)
- Decart 데모의 데이터가 실제 주행 데이터인지 시뮬레이션인지 확인하지 못했다고 밝힌다 ([260722] General Intuition L37)
- 월드모델 파라미터가 언어모델보다 작다는 점을 의외로 여기면서도 앞으로 커질 것이라고만 전망한다 ([260722] General Intuition L38)
