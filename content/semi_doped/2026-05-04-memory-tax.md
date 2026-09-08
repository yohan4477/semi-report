---
title: 캡엑스는 이제 메모리세다
date: 2026-05-04
source: https://daily.semidoped.com/p/capex-is-just-memory-tax-now-deepseek
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: mem
topic: 설비투자 · 메모리 값 · 낸드 계약
gain: 설비투자가 늘었는데 그 상당 부분이 연산이 아니라 부품 값 상승분을 메우는 데 간다는 프레임. 한 회사가 1,900억 달러 중 250억을 부품값이라고 밝힌 대목과, 낸드 쪽에 420억 달러짜리 장기 계약이 잡힌 이야기.
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
---

## 한 줄
2026년 빅테크 캡엑스(설비투자) 상승분의 상당 부분이 컴퓨트(플롭스) 확대가 아니라 메모리·스토리지 가격 상승분을 메우는 데 쓰인다는 "메모리 택스" 프레임을 삼성·샌디스크 실적과 함께 짚고, 디렉SSD 중심 추론 흐름(DeepSeek v4)을 연결한다.

## 사실 — 절 순서대로
- Vik이 15년 반도체 업계 커리어를 접고 Substack·팟캐스트를 풀타임으로 전환했다고 밝힘. 컨설팅 사업을 "Semiexponent" 브랜드로 시작한다고 언급.
- Semi Doped Substack이 무료(페이월 없음) 일간 뉴스레터로 운영 중이라고 소개 — 3~5분 분량의 짧은 하루치 업데이트.
- 실적 시즌 개관. 4대 하이퍼스케일러(마이크로소프트·구글·메타·아마존)가 2026년 캡엑스 약 $700B에 확정, 2025년 약 $500B 대비 증가라고 언급. 이번 분기의 특징은 캡엑스 증가분 상당수가 "더 많은 플롭스"가 아니라 메모리·스토리지·광부품 등 상승한 부품 가격을 충당하는 용도라는 점이라고 규정.
- 삼성전자 실적. 메모리 매출 전년비 101% 증가, Q1 매출·영업이익 사상 최대치. HBM 매출은 2026년 전년비 3배(triple) 전망, HBM4가 Q3까지 HBM 매출의 50% 이상을 차지할 전망.
- 삼성의 HBM 시장점유율 변화. 한때(약 6분기 전 기준) 약 40%였다가 2025년 13~20%대로 하락, HBM4로 재도약을 시도 중이라고 설명.
- JEDEC 규격상 HBM4는 초당 8기가비트/핀(pin)이지만, 엔비디아·AMD 등 고객사의 성능 경쟁 압박으로 업계는 규격을 넘어선 10~12Gbps/pin을 목표로 경쟁 중이라고 설명. 한번 하이퍼스케일러가 HBM 벤더를 인증(qualify)하면 교체가 어려운 "스티키(고착적)" 관계라고 설명.
- 삼성전자 EVP 발언 인용(J. June Kim, 메모리영업총괄) — HBM4 최초 상용 출하, 생산 가능 물량 완판, 프리미엄 가격 반영을 언급. 수요 이행률(demand fulfillment rate)이 사상 최저 수준이며 고객들이 2027년 수요를 미리 당겨오고 있다고 발언.
- 샌디스크·웨스턴디지털 연혁. 웨스턴디지털이 2016년 샌디스크를 약 $20B에 인수했다가, 2023년 10월 분할 발표, 2025년 2월 샌디스크가 독립 상장사로 재분사됐다고 설명.
- 웨스턴디지털은 HAMR(열보조자기기록, Heat Assisted Magnetic Recording) 기술로 100TB 이상 용량 HDD를 2027년 양산 목표로 개발 중이라고 소개. 샌디스크의 QLC(4비트/셀) SSD는 이미 최대 256TB 용량을 제공한다고 대비.
- 샌디스크의 원래 창업자는 현 마이크론 CEO 산자이 메로트라(Sanjay Mehrotra)라는 트리비아. 공동창업자 일라이 하라리(Eli Harari)의 딸이 디스크 모양을 보고 "태양 같다"고 해 원래 사명이 "SunDisk"였다가, 선 마이크로시스템즈의 상표 이의로 창업 7년 후 "SanDisk"로 개명했다고 설명.
- 샌디스크 실적. 매출 약 $6B, 전분기(QoQ) 대비 97% 증가, 전년비(YoY) 251% 증가. 매출총이익률 78.4%(전분기 51.1%에서 급등), 다음 분기 가이던스는 80% 이상.
- CEO 데이비드 괴켈러(David Goeckeler)가 다년 공급 파트너십("New Business Models", NBM) 5건 체결을 발표. 이 중 신규 3건이 총 $42B의 RPO(잔여 이행의무, remaining performance obligations)라고 처음 공개. 고객 약정이 이미 FY27 비트 물량의 1/3을 커버하며, 최장 계약기간은 5년이라고 설명.
- 괴켈러가 실적콜에서 AI 모델의 파라미터 확장과 KV캐시(키-밸류 캐시, 추론 시 이전 계산 결과 재사용 저장소)·RAG(검색증강생성) 등 워크로드가 고성능·저지연 낸드플래시를 필요로 한다고 주장, NAND가 유일하게 경제적으로 확장 가능한 솔루션이라는 취지로 발언.
- DeepSeek v4와 SSD 중심 추론. DeepSeek v4가 전작(v3.2) 대비 KV캐시를 크게 압축했으나, 에이전틱(agentic)·멀티턴 추론에서는 다수 에이전트의 장기 컨텍스트가 HBM·DRAM에 다 담기지 않아 KV캐시를 거의 전량 SSD에 저장하는 구조로 설계됐다고 설명.
- 엔비디아가 GTC 이후 발표한 추론 컨텍스트 스토리지 시스템(현재 명칭 CTX)도 언급 — 랙 단위 SSD를 고대역폭 패브릭으로 GPU와 연결해 KV캐시를 오프로드하는 개념.
- 캐시 히트(재사용)와 캐시 미스 개념 설명. 입력 토큰 대비 출력 토큰이 대략 4~5배 비싸며(추론 과정 때문), 캐시 히트 시 추론 비용이 크게 낮아진다고 설명. DeepSeek는 에이전틱 사용에서 캐시 히트율 95%, 일부 경우 99%에 달한다고 언급. DeepSeek v4 Pro API 가격이 100만 토큰당 1센트 미만 수준까지 낮아졌다고 언급(구체 수치는 미제시, Claude Opus 대비 훨씬 낮다고만 비교).
- DeepSeek 팀의 신규 논문 "Dual Path: Breaking the Storage Bandwidth Bottleneck in LLM Inference"를 아직 안 읽었다며 소개.
- Vik은 낸드 컨트롤러 기술 차이(샌디스크의 QLC 컨트롤러 명칭 "Stargate")는 있지만 "비트는 비트"(a bit is a bit)라는 견해를 밝히며, 스토리지 전문가의 의견을 구한다고 덧붙임. TLC(9개 상태/셀)에서 QLC(16개 상태/셀)로 갈수록 셀 하나가 구분해야 할 상태 수가 늘어 컨트롤러 복잡도가 커진다고 설명(PLC는 연구 단계에서 32개 상태).
- 하이퍼스케일러 캡엑스와 부품 가격 상승 연결. 마이크로소프트는 2026년 캡엑스 $190B 공시, CFO 에이미 후드(Amy Hood)가 그중 약 $25B는 특정하게 부품 가격 상승분이라고 밝힘. 메타는 캡엑스 상승분 대부분이 부품비용(특히 메모리 가격) 상승이라고 저커버그가 언급. 구글은 순다르 피차이가 클라우드 매출이 전년비 63% 성장했으며 수요를 다 맞췄다면 더 높았을 것이라고 발언.
- 아마존 CEO 앤디 재시(Andy Jassy)가 메모리 공급 제약이 오히려 클라우드 성장을 촉진하는 역설적 효과를 낳고 있다고 발언 — 메모리 공급업체들이 최대 고객인 하이퍼스케일러를 우선 배정하면서, 온프레미스 인프라를 확보하지 못한 기업들이 클라우드로 더 빨리 이전하고 있다는 취지.
- AI 가속기 동향. 구글이 실적콜에서 TPU를 처음으로 머천트(외부 판매) 형태로, 멀티기가와트 규모로 판매한다고 공개, 10-Q 리스크 항목에 CoWoS·HBM 할당 리스크가 신규 명시됐다고 언급.
- AWS Trainium 런레이트 $20B, 3자릿수 성장률. Trainium2는 거의 매진, Trainium3는 거의 다 예약됐다고 언급. 재시는 커스텀 XPU 사용으로 매년 수백억 달러(tens of billions) 캡엑스를 절감하며, 머천트 칩 대비 영업이익률이 수백bp 개선된다고 발언.
- 메타는 브로드컴과 함께 1기가와트 규모 MTIA를 발표, 향후 2년간 4개 칩 로드맵을 공개했다고 언급. AMD·엔비디아 신제품도 대규모로 배치 중이라고 언급.
- 마무리. 유튜브 시청자들이 이전 회차(구글 TPU 편)의 "왜 16홉이 아니라 7홉인가(Boardfly)"를 다시 설명해 달라고 요청, 후속 회차에서 그림으로 설명하겠다고 예고.

## 숫자 (원문에 나온 것만)
- 약 $700B — 2026년 4대 하이퍼스케일러 캡엑스 확정치 (2025년 약 $500B)
- 101% — 삼성전자 메모리 매출 전년비 증가율
- 3배(triple) — 삼성 HBM 매출 2026년 전년비 전망
- 50%+ — HBM4가 Q3까지 차지할 HBM 매출 비중 전망
- 40% → 13~20% — 삼성 HBM 시장점유율 변화(한때 대비 2025년)
- 8Gbps/pin — HBM4 JEDEC 규격, 10~12Gbps/pin — 업계 경쟁 목표치
- 약 $6B — 샌디스크 분기 매출
- 97% — 샌디스크 매출 QoQ 증가율, 251% — YoY 증가율
- 78.4% — 샌디스크 매출총이익률(전분기 51.1%), 80%+ — 다음 분기 가이던스
- $42B — 샌디스크 신규 3건 공급계약의 RPO(잔여 이행의무)
- 1/3 — FY27 비트 물량 중 이미 고객 약정으로 커버된 비중
- 5년 — 샌디스크 최장 공급계약 기간
- 100TB+ — 웨스턴디지털 HAMR HDD 목표 용량(2027년 양산 목표)
- 256TB — 샌디스크 QLC SSD 최대 용량(현재)
- 95%, (일부 99%) — DeepSeek v4 에이전틱 사용 캐시 히트율
- $190B — 마이크로소프트 2026년 캡엑스, 그중 약 $25B — 부품가격 상승분
- 63% — 구글 클라우드 매출 전년비 성장률
- $20B — AWS Trainium 런레이트
- $20B — 웨스턴디지털의 2016년 샌디스크 인수 금액

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "the differentiated performance of our HBM4 led to concentration of demand and our production-ready capacity is fully booked and sold out." — "HBM4의 차별화된 성능으로 수요가 집중됐고, 생산 가능한 물량은 완전히 예약되어 매진됐다." (J. June Kim, 삼성전자 메모리영업 EVP)
- "our demand fulfillment rate is now at a record low." — "당사의 수요 이행률이 현재 사상 최저치다." (J. June Kim)
- "as AI models scale from billions to trillions of parameters and deployments advance from simple inference to deep reasoning and increasingly agentic systems, NAND has become a critical component of the underlying infrastructure." — "AI 모델이 수십억에서 수조 파라미터로 확장되고, 배포가 단순 추론에서 딥 리즈닝과 점점 더 에이전틱한 시스템으로 나아가면서, NAND는 기반 인프라의 핵심 구성요소가 됐다." (David Goeckeler, 샌디스크 CEO)
- "it is actually a further impetus pushing companies who have been on-premises infrastructure into the cloud." — "이는 온프레미스 인프라를 써 왔던 기업들을 클라우드로 더 밀어붙이는 추가 동인이 되고 있다." (Andy Jassy, 아마존 CEO)

## 주의
- 이 회차도 축어록에 가까운 라이트 에디팅 전사본이다.
- Austin이 SSD 시장 전망을 논하며 "Not advice, not advice, not advice"(투자 조언 아님)라고 명시적으로 강조한 대목이 있음 — 인용·재구성 시 이 맥락을 함께 남겨야 한다.
- "a bit is a bit"(NAND 비트 간 차별화가 크지 않다는 견해)는 Vik 본인이 "please correct me if there are any storage experts out there"라고 헤지한 잠정 의견이며, 진행자들도 후속 검증이 필요하다고 스스로 밝힘.
- DeepSeek v4 Pro API 가격이 "100만 토큰당 1센트 미만 수준"이라는 대목은 정확한 숫자를 대지 않고 "a fraction of a cent"라고만 언급됐다 — 구체 수치로 인용하지 말 것.
- 아마존 온프레미스→클라우드 전환 발언은 재시의 발언에 대한 진행자들의 해석("counterintuitive")이 섞여 있으므로 재시 원발언과 진행자 해석을 구분해서 읽을 것.
