---
source: "content/newsletter/ai_infra/compute/[251009] InferenceMAX - 오픈소스 추론 벤치마킹.md"
title: "InferenceMAX™: Open Source Inference Benchmarking"
date: 2025-10-09
corpus: semi
lang: ko
actors: [엔비디아, AMD, 구글, AWS]
topics: [반도체, 벤치마크, 추론]
---

## 이 문서가 주장하는 것

InferenceMAX는 하드웨어는 매년 계단식으로 도약하지만 소프트웨어는 며칠 단위로 바뀌어 벤치마크가 금세 낡는 문제를 풀려고, 매일 밤 수백 개 칩에서 자동으로 재실행하는 오픈소스 벤치마크다. 워크로드와 상호작용성(사용자가 체감하는 초당 토큰 생성 속도) 구간에 따라 AMD와 엔비디아가 번갈아 우위를 차지해, 어느 한쪽 편을 들지 않는 결과가 나온다. 정말 중요한 잣대는 처리량이 아니라 100만 토큰당 총소유비용이며, TCO와 상호작용성 중 어느 축을 고정하느냐에 따라 승자가 뒤바뀐다. 멀티 토큰 예측(MTP, 한 번의 순전파로 토큰을 여러 개 동시에 예측하는 기법) 같은 소프트웨어 기법 하나가 세대 간 하드웨어 격차만큼 큰 차이를 만들기도 한다.

## 수치

- v1 벤치마크 대상은 GB200 NVL72·B200·MI355X·H200·MI325X·H100·MI300X 7종, 2개월 내 구글 TPU·AWS Trainium 추가 예정 (InferenceMAX L48)
- MTP를 켜면 상호작용성 70~140 tok/s/user 구간에서 동일 조건 처리량이 최대 2~3배 향상 (InferenceMAX L272)
- DeepSeek 670B FP8: TCO를 고정하면 B200 SGLang이 MI355X SGLang 대비 상호작용성 1.5배, 반대로 상호작용성을 35 tok/s/user로 고정하면 GB200 NVL72가 TCO/백만토큰 기준 4배 우위 (InferenceMAX L313)
- 임대료·전기요금은 TCO의 20% 미만 — MW당 토큰이 20% 적어도 TCO 영향은 4%뿐, TCO 대부분은 엔비디아·AMD 같은 칩 제조사가 매기는 총마진(50~75%)이 좌우 (InferenceMAX L363)
- 전력효율 세대 개선폭은 AMD(MI300X→MI355X)·엔비디아(H100→B200) 모두 약 3배(GPT-OSS 120B 기준) (InferenceMAX L364)
- 동세대 비교로는 B200이 MI355X보다 전력효율 약 20% 높음 — MI355X 단독 TDP(발열 한도) 1.4kW, B200 1kW가 원인 (InferenceMAX L365)
- 서버 가격은 H100 18만9,637달러 vs MI300X 14만5,017달러, B200 30만8,680달러 vs MI355X 18만9,607달러 — TCO 중 자본비용 비중은 엔비디아 60~75%, AMD 55~65% (InferenceMAX L480)
- 온페이퍼 스펙 기준 FP8 TCO/PFLOP은 MI355X 0.30달러, B200 0.43달러 (InferenceMAX L482)
