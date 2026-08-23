---
source: "content/understanding/피지컬AI/[260721] Sunday Robotics ACT-2 프리뷰.md"
title: "Sunday Robotics ACT-2 프리뷰"
date: 2026-07-21
corpus: third
lang: ko
actors: [Sunday Robotics, Walden Robotics]
topics: [로봇 데이터 수집, 스케일링 법칙]
---

## 이 문서가 주장하는 것

「Sunday Robotics ACT-2 Preview 내용 훑어보자」 편은 Sunday Robotics가 시리즈 B를 알리며 더 이상 '데모'를 내지 않고 '솔브(정해진 범위 안에서 신뢰할 수 있는 성능)'만 공개하겠다고 선언한 것을 다룬다. 첫 사례로 처음 보는 집에서 빨래 개기를 제로샷으로 거의 다 성공했다고 밝혔고, 진행자들은 사전학습 데이터양과 검증 손실의 관계가 LLM 스케일링 법칙과 닮았다는 점을 근거로 짚었다. 데이터는 사람이 스킬 캡처 글로브를 끼고 직접 접어서 모으며, 이 작업 직함을 '데이터 콜렉터'가 아니라 '메모리 디벨로퍼'라 부른다. 이 방식은 앞선 다른 편에서 다룬 로봇 미사용 데이터 수집의 연장선이다. 후반부는 MIT 교수 Russ Tedrake가 도요타 리서치 인스티튜트(TRI) 출신들과 창업한 산업용 로봇 스타트업 Walden Robotics를 소개한다 — 시드 단계에서 이미 유니콘 밸류를 받았고 '노동 대체가 아니라 증강'을 표어로 내세운다. 진행자들은 모델 규모나 데이터 수집 비용의 지속 가능성은 회사가 밝히지 않은 자신들의 추정이라고 구분해 말했다.

## 수치

- Sunday Robotics가 처음 보는 집에서 빨래 개기 제로샷 성공률 99.1%를 냈다고 밝혔다 ([260721] Sunday Robotics ACT-2 L11)
- 품목별로는 티셔츠 약 99%, 블라우스 94%로 나뉘었다 ([260721] Sunday Robotics ACT-2 L14)
- 루브릭 채점 평균 점수는 5점 만점에 4.72였다 ([260721] Sunday Robotics ACT-2 L15)
- 사전학습 데이터를 1, 1/2, 1/4, 1/8로 줄이며 인도메인-아웃도메인 성능 갭을 비교했다 ([260721] Sunday Robotics ACT-2 L18)
- 데이터 수집 시급은 평균 30달러, 승인된 고품질 데이터는 최대 60달러다 ([260721] Sunday Robotics ACT-2 L26)
- 동시에 약 1,000명이 '메모리 디벨로퍼'로 일한다 ([260721] Sunday Robotics ACT-2 L27)
- Walden Robotics는 시드 라운드 3억 달러, 기업가치 11억 달러로 출발했다 ([260721] Sunday Robotics ACT-2 L34)

## 저자가 추정이라고 밝힌 것

- 모델 파라미터 규모는 공개되지 않았고, 엣지 추론 전환 정황만으로 20억~100억 개 사이일 것이라 추정했다 ([260721] Sunday Robotics ACT-2 L48)
- 데이터 수집에 월 100억 원 안팎이 든다는 계산은 진행자들이 시급·인원 수로 직접 추산한 것이지 회사 발표가 아니다 ([260721] Sunday Robotics ACT-2 L49)
- 원샷으로 따라 한 접기 방식이 사전학습 데이터에 이미 포함돼 있었는지는 진행자들 사이에서도 의견이 갈렸다 ([260721] Sunday Robotics ACT-2 L50)
