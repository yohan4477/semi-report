---
title: 구글의 네트워킹
date: 2026-04-24
source: https://daily.semidoped.com/p/googles-networking-innovations
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: link
topic: TPU · 광회선 스위칭 · 토폴로지
gain: 훈련용과 추론용으로 칩을 가르면 네트워크도 갈린다는 이야기. 훈련 쪽은 3D 토러스로 16홉, 추론 쪽은 보드를 묶어 7홉. 그리고 광회선 스위칭으로 계층을 줄여 칩 13만 4천 개를 한 덩이로 묶은 셈.
---

## 한 줄
구글이 Cloud Next 2026 키노트에서 공개한 TPU v8(훈련용 8T·추론용 8I)이 칩뿐 아니라 네트워크 토폴로지까지 워크로드별로 완전히 다르게 설계됐다는 점을 스케일아웃(Virgo, OCS 기반)과 스케일업(3D 토러스 대 Boardfly) 두 축으로 짚는다.

## 사실 — 절 순서대로
- 구글이 Cloud Next 2026 키노트에서 TPU를 훈련용(8T)과 추론용(8I) 두 개 칩으로 분리 발표. TPU 세대별 구성 이력: v1은 추론 전용, v2~v4는 훈련+서빙 겸용, v5는 효율칩과 성능칩 분리, v6는 다시 단일 칩, v7도 단일 칩(추론 위주로 마케팅)이었다가, v8에서 다시 훈련·추론 전용칩으로 분리됐다고 설명.
- 8I(추론용)는 SRAM 384MB로 8T(훈련용)의 3배. Groq LPU처럼 SRAM을 많이 넣어 저지연 추론·고처리량 디코딩을 노린 설계라고 설명.
- 8I는 HBM 288GB, 8T는 HBM 216GB — 추론칩이 훈련칩보다 HBM도 더 많다는 점을 짚음. 훈련은 GPU/TPU를 더 많이 묶어 클러스터 총 메모리를 늘릴 수 있지만, 추론은 개별 칩 단에서 모든 메모리 계층(SRAM·HBM·DRAM)을 최대치로 채우는 것이 중요하다는 논리로 설명.
- 두 시스템 모두 구글 자체 ARM 기반 Axion CPU를 헤드노드로 사용한다고 발표. 구글 발표 블로그를 인용하며 데이터 전처리 지연으로 인한 호스트 병목을 Axion으로 제거했다고 소개.
- 네트워킹이 이제 컴퓨트가 아니라 병목이라는 전제를 제시. 구글이 훈련·추론용으로 칩뿐 아니라 네트워크 아키텍처도 별도로 재설계했다는 것이 이번 발표의 핵심이라고 규정.
- OCS(광회선스위칭, optical circuit switching) 개념 설명 — 빛을 전기신호로 변환하지 않고 스위치 포트 간에 광 신호 경로를 그대로 바꿔 연결하는 방식.
- 구글의 이전 네트워크(Jupiter, 2015년) 소개. 당시 세계 최초 페타비트급 네트워크. 리프-스파인-슈퍼스파인 다층 구조의 Clos 네트워크 기반으로, 랙 간 통신 시 홉 수가 많아 인터넷·웹서비스 시대에는 적합했으나 AI 훈련의 동기적(synchronous) 트래픽 패턴에는 맞지 않는다고 설명.
- 홉이 많은 이유로 스위치 radix(포트 수)가 낮다는 점을 지적 — 저radix 스위치는 계층을 더 쌓아야 포트 수를 확보할 수 있다고 설명.
- 2022년경 구글이 데이터센터에 OCS를 도입, 파장분할다중화(WDM)까지 적용해 대역폭이 약 6페타비트/초로 늘었다가, 이후 400기가 네트워킹 적용으로 13.1페타비트/초까지 확장(2015~2023년 13배 성장)됐다고 설명.
- AI 훈련 특유의 동기적 트래픽에서는 가장 느린 노드(straggler)가 전체 지연(tail latency)을 좌우한다는 점을 짚으며, Jupiter 네트워크가 이 시대에는 맞지 않다는 문제의식으로 이어짐.
- Virgo(신규 스케일아웃 네트워크) 소개. 네트워크 스택을 스케일업(패드 내부)-스케일아웃(=백엔드 네트워크, 랙 간 동서 연결)-프런트엔드 네트워크(컴퓨트/스토리지/인터넷 연결, 기존 Jupiter/Clos 그대로 사용) 3계층으로 구분.
- Virgo는 고radix OCS 스위치를 활용해 계층을 2층으로 축소, 134,000개의 TPU를 하나의 컴퓨터처럼("campus as a computer") 연결한다고 설명. 현재 OCS 스위치(예: Lumentum)는 300x300 포트, 향후 1,000x1,000 포트까지 확장될 것이라고 언급.
- Virgo의 집계 대역폭이 47페타비트/초로, 기존 13.1페타비트/초 대비 약 4배라고 밝힘.
- 134,000개 칩을 하나로 묶으면 장애가 잦아지므로, 굿풋(goodput, 실제 작동 처리량 — 이론상 최대치인 스루풋과 대비되는 개념)을 지속 모니터링하는 대규모 텔레메트리 체계를 갖췄다고 언급.
- TPU Direct(RDMA, Remote Direct Memory Access) 소개. 기존에는 TPU 간 메모리 접근 시 양쪽 호스트 CPU가 개입해 여러 단계의 핸드셰이크를 거쳤으나, TPU Direct는 호스트 CPU를 거치지 않고 네트워크 인터페이스를 통해 직접 접근한다고 설명. 엔비디아의 GPU Direct와 같은 개념이라고 대비.
- 3D 토러스(스케일업, 훈련용) 설명 — 루빅스 큐브 비유. 인접한 면끼리는 구리 케이블로, 같은 행/열의 반대편 먼 면끼리는 광(옵틱)으로 연결한다고 설명.
- TPU v7 예시로 8x8x16 구성을 제시 — 큐브의 정중앙(가장자리가 아니라 중앙)이 가장 홉 수가 많은 위치이며, 각 축의 절반씩 이동해야 하므로 최대 16홉(4+4+8 계산 예시)이 필요하다고 설명.
- 3D 토러스는 훈련(모든 칩이 항상 서로 통신)에는 적합하지만, MoE(전문가 혼합, Mixture-of-Experts) 추론에는 적합하지 않다고 지적 — 활성화되는 전문가(칩)가 매번 달라 홉 지연이 추론 성능에 그대로 영향을 준다는 이유.
- Boardfly(스케일업, MoE 추론용) 소개. 보드 1개에 TPU 4개가 PCB(구리) 연결로 실장, 보드 8개가 랙(=그룹) 안에서 AEC(능동전기케이블)로 연결, 그룹 36개가 OCS로 연결돼 파드를 구성 — 36×8×4=1,152칩이라는 계산 제시.
- Boardfly라는 이름은 개별 칩이 아니라 "보드" 단위를 Dragonfly 토폴로지로 연결한다는 데서 유래했다고 설명. Dragonfly는 2008년 논문(저자: John Kim, William "Bill" Dally, Steve Scott, Dennis Abts)에서 유래한 슈퍼컴퓨팅 시대의 기존 개념이라고 소개 — Dennis Abts는 구글을 거쳐 Groq(2017~2022년), 이후 엔비디아로 옮겼다고 언급. Groq의 랙스케일 솔루션도 Dragonfly 구성이라고 덧붙임.
- Boardfly로 홉 수가 16에서 7로 줄고, 레이턴시가 50% 이상 감소한다고 설명.
- CAE(Collective Acceleration Engine) 소개 — TPU 8I 칩렛에 텐서코어 2개와 CAE 1개가 있으며, all-reduce·all-gather·all-to-all 같은 집합통신(collective) 연산을 오프로드하는 워크로드 특화 가속기라고 설명. 엔비디아 SHARP와 유사한 개념이라고 대비.
- 마무리. 훈련·추론이 칩·네트워크·(향후) 전력·입지까지 완전히 다른 방향으로 분화하는 "극단적 코디자인(co-design)" 흐름이라고 규정. AWS Trainium 등 다른 하이퍼스케일러도 이런 워크로드별 네트워크 특화를 따를지 궁금하다는 질문으로 마무리.

## 숫자 (원문에 나온 것만)
- 384MB — TPU 8I의 SRAM(8T의 3배)
- 288GB — TPU 8I의 HBM
- 216GB — TPU 8T의 HBM
- 약 6페타비트/초 — 2022년경 Jupiter+OCS+WDM 대역폭
- 13.1페타비트/초 — 이후 400기가 네트워킹 적용 후 Jupiter 대역폭(2015년 대비 13배 성장)
- 47페타비트/초 — Virgo 집계 대역폭(기존 대비 약 4배)
- 300x300 — 현재 OCS 스위치 포트 수(예: Lumentum)
- 1,000x1,000 — 향후 OCS 스위치 포트 수 전망
- 134,000 — Virgo로 연결되는 TPU 개수
- 8x8x16 — TPU v7 3D 토러스 구성 예시, 최대 16홉
- 4 — 보드당 TPU 개수
- 8 — 그룹(랙)당 보드 개수
- 36 — 파드당 그룹 개수
- 1,152 — 파드당 총 칩 수(36×8×4)
- 7 — Boardfly 최대 홉 수(3D 토러스 16홉 대비)
- 50%+ — Boardfly 적용 시 레이턴시 감소폭
- 2 — TPU 8I 칩렛당 텐서코어 개수, 1 — 칩렛당 CAE 개수

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "TPU introduces two distinct systems, TPU 8T and 8I." — "TPU는 8T와 8I라는 두 개의 별도 시스템을 도입한다." (구글 발표 블로그, Austin이 낭독)
- "by integrating ARM-based Axion CPU headers across our 8th Gen TPU system, we've removed the host bottleneck caused by data preparation latency." — "8세대 TPU 시스템 전반에 ARM 기반 Axion CPU 헤더를 통합함으로써, 데이터 준비 지연으로 인한 호스트 병목을 제거했다." (구글 발표 블로그)
- "campus as a computer." — "캠퍼스 전체가 하나의 컴퓨터다." (Vik, Virgo를 요약하며)

## 주의
- 이 회차도 축어록에 가까운 라이트 에디팅 전사본이다. 다만 진행자들이 구글 슬라이드 화면 공유로 그림을 보며 설명하는 형식이라("definitely watch it on YouTube"), 오디오/텍스트만으로는 도식적 설명(3D 토러스·Boardfly 배선도 등)이 완전히 전달되지 않을 수 있다.
- CAE(Collective Acceleration Engine)는 Vik 본인이 "I don't even know what that is. I haven't gotten around to reading about it"라고 밝혔고, 텐서코어 2개+CAE 1개 등 세부 스펙은 Austin이 별도로 조사해 온 내용이다 — 구글 공식 발표문 원문 대조가 필요하다.
- Dragonfly 논문 저자 트리비아(John Kim·William Dally·Steve Scott·Dennis Abts)는 Austin이 구글 검색으로 찾은 내용이며, 게시물 댓글(독자 "Tanj")에서 Cray의 사업장 연혁 등 일부 세부 사실에 이견이 제기됐다 — 이는 팟캐스트 본문 발언이 아니라 별도의 시청자 코멘트이므로 구분해서 다뤄야 한다.
- 같은 댓글에서 "Steve Scott는 최근까지 Azure 서버 엔지니어링을 이끌었다"는 정정이 달렸는데, 이 역시 팟캐스트 발언이 아닌 시청자 코멘트다.
