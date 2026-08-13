---
source: "content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md"
title: "InferenceX v2: NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX"
date: 2026-02-16
corpus: semi
lang: ko
actors: [엔비디아, AMD]
topics: [GPU, 추론벤치마크, TCO]
---

## 이 문서가 주장하는 것

InferenceX v2(전 InferenceMAX)는 Nvidia 서방향 GPU 6종과 AMD 전 SKU(같은 세대의 별도 제품)를 대상으로, 프리필과 디코드를 서로 다른 GPU 풀에 배정하는 분리형 서빙과 전문가 병렬화를 여러 노드로 넓히는 Wide EP까지 포함해 벤치마크했다. FP8 단일 최적화에서는 AMD MI355X가 Nvidia B200과 경쟁할 만하지만, 프론티어 랩이 실제로 쓰는 FP4·분리형 서빙·Wide EP 세 가지를 동시에 걸면 AMD 성능이 급락한다. 2024년 GTC에서 Jensen Huang이 예고한 "H100 대비 GB200 최대 30배"는 당시 과장으로 치부됐지만 실측에서는 오히려 과소약속이었다. MTP(멀티토큰예측, 본 모델이 토큰 여러 개를 한 번에 예측·검증)는 토큰당 비용을 최대 21배까지 낮춘다.

## 수치

- 벤치마크 1회 전체 실행에 약 1,000개 프론티어 GPU 투입, Nvidia 6종·AMD 전 SKU 대상 (InferenceX v2 L50)
- GB300 NVL72는 H100 분리형+WideEP+MTP 기준선 대비 FP8 대 FP4 비교 최대 100배, FP8 대 FP8 비교 최대 65배 (InferenceX v2 L100)
- 60 tok/s/user에서 GB200 NVL72의 GPU당 토큰생성 속도가 B200 대비 거의 3배, 130 tok/s/user에서는 이 이점이 거의 사라지고 오히려 더 비싸짐 (InferenceX v2 L280)
- Crusoe가 36 tok/s/user·백만 입력토큰당 $1.35·출력토큰당 $5.40에 서빙한다면 입력토큰 총마진 최대 83%, 출력토큰 총마진 최대 45%로 추정 (InferenceX v2 L368)
- 116 tok/s/user 기준 GB200 NVL72 FP4는 H100 대비 최대 98배, GB300 NVL72 FP4는 최대 100배 — 토큰당 비용은 9.7배(40tok/s/user)~65배(116tok/s/user) 개선 (InferenceX v2 L414)
- vLLM CI에는 MI355X 테스트가 0건, B200은 다수 존재 (InferenceX v2 L460)
- FP4 Dynamo TRT-LLM 기준 DeepSeek R1 비용은 MTP를 켜면 백만 토큰당 $0.251→$0.057로(약 4.4배), 150tok/s/user·GB300 기준으로는 $2.35→$0.11(약 21배) 급감 (InferenceX v2 L506)
- Anthropic Fast Mode는 동일 품질에 약 2.5배 속도, 약 6~12배 가격 (InferenceX v2 L507)
- 컴퓨트 트레이 원가는 MI300X 약 $138K·H100 SXM 약 $170K, MI355X 약 $197K·B200 약 $264K·B300 약 $344K (InferenceX v2 L689)
