---
source: "content/newsletter/ai_infra/compute/[260401] Nvidia Blackwell 해부 - 텐서 코어, PTX 명령어, SASS, 플로어스위프, 수율.md"
title: "Dissecting Nvidia Blackwell - Tensor Cores, PTX Instructions, SASS, Floorsweep, Yield"
date: 2026-04-01
corpus: semi
lang: ko
actors: [엔비디아]
topics: [GPU, 텐서코어, 마이크로벤치마킹]
---

## 이 문서가 주장하는 것

SemiAnalysis는 Blackwell(SM100)을 공식 백서 없이 수개월간 직접 뜯어 명령어 단위로 실측해, 제조사가 발표하는 이론상 최대치가 아니라 실전에서 실제로 낼 수 있는 성능 상한선을 확인한다. tcgen05 명령어는 스레드 하나가 CTA(협력 스레드 블록) 전체를 대표해 실행하도록 관리 단위를 키웠고, 제조 결함이 칩 전체에 무작위로 분포해 GPC마다 비활성화된 SM 개수가 다르지만 SM100부터는 대체 클러스터 크기 지정으로 결함 SM까지 낭비 없이 쓸 수 있다. 실측 결과 B200 칩의 두 다이는 SM 39개와 35개로 비대칭하게 나뉘어 있고, 다이 간 연결 구간을 지날 때 약 300사이클의 지연이 추가로 붙는다. 텐서 코어의 5세대 MMA 명령어는 큰 행렬 모양에서 이론상 최대치에 근접하지만, 실전 커널처럼 동시 실행 명령어가 몇 개뿐인 조건에서는 이론치의 78~80%가 현실적인 상한선이다.

## 수치

- tcgen05 계열 명령어는 스레드 1개가 CTA 전체를 대표 — 이전 세대는 워프 32개 또는 워프그룹 128개 단위였음 (Blackwell 해부 L79)
- 제조 결함이 칩 전체에 무작위로 분포해 GPC마다, 같은 칩의 두 다이 사이에서도 비활성화된 SM 개수가 다름 (Blackwell 해부 L124)
- SM100(Blackwell)부터는 선호·대체 클러스터 크기를 함께 지정할 수 있어 대체 크기를 1이나 2로 두면 결함 SM까지 낭비 없이 활용 (Blackwell 해부 L125)
- SM-SM 거리 실측으로 다이 A는 SM 39개, 다이 B는 SM 35개로 추정되며, 다이 간 지연 페널티는 약 300사이클 (Blackwell 해부 L174)
- FlashInfer MHA 커널 재현 실측에서 32KiB 전송 시 8바이트 로드는 4단계가 필요하지만 16바이트 로드는 2단계로 충분 (Blackwell 해부 L221)
- LDGSTS 처리량은 32KiB 전송 시점에 약 6.6TB/s로 포화, 지연시간은 기본 약 600나노초에서 8KiB 초과 시 거의 2배로 증가 (Blackwell 해부 L222)
- UMMA는 1SM MMA에서 M=64일 때 이론치 최대 50%, M=128일 때는 거의 100%에 도달 (Blackwell 해부 L426)
- 실전처럼 동시 실행 명령어 1~4개 조건에서 가장 큰 N은 SoL(이론상 최대) 90%, 가장 작은 N은 70%에 그침 (Blackwell 해부 L490)
- 같은 조건에서 1SM MMA가 2SM MMA보다 SoL 도달률이 약 5%p 높고, 동시 실행 4개 조건에서는 SoL의 78~80%가 현실적 상한선 (Blackwell 해부 L491)
