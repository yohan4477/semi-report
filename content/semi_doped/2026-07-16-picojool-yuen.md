---
title: 새 공장을 안 지어도 되는 쪽 — VCSEL 로 스케일업 광통신을 채운다
date: 2026-07-16
source: https://daily.semidoped.com/p/picojools-al-yuen-the-case-for-gaas
speaker: Al Yuen
org: PicoJool 최고경영자(CEO)
channel: Semi Doped
host: Austin Lyons
people: 진행 [[Austin Lyons]] (Semi Doped) / 게스트 [[Al Yuen]] (PicoJool 최고경영자, 전사 라벨 Al)
section: link
topic: VCSEL · 스케일업 인터커넥트
gain: 광소자 경쟁을 성능이 아니라 물량이 정한다는 논지. 인듐인 계열은 기판부터 막혀 있고 갈륨비소는 이미 월 수백만 개를 찍어 왔다는 주장, 1.6테라비트를 채우는 세 조합, 12.8테라비트까지 새 기술 없이 가는 경로, 그리고 실제 리드타임과 웨이퍼 한 장에서 나오는 개수까지.
---

## 한 줄

PicoJool CEO Al Yuen 은 갈륨비소(GaAs, gallium arsenide) 기반 VCSEL(수직공동표면방출레이저, vertical-cavity surface-emitting laser)이 인듐인(InP, indium phosphide) 기반 단일모드(single-mode) 광소자보다 스케일업 인터커넥트(scale-up interconnect, 랙 간 짧은 거리 광통신)에 실용적이라고 주장한다. 근거는 25년간 월 수백만 개를 출하해 온 공급망이 이미 갖춰져 "제약 없음(unconstrained)"이라는 점이며, 회사는 200기가비트/레인 VCSEL 을 막 발표하고 8×200/16×100/32×50 세 가지 조합으로 1.6T 를 채운 뒤 2-D 배열과 양방향(bi-di) 파장으로 12.8T 까지 가는 로드맵을 제시한다.

## 사실 — 절 순서대로

**From HP Labs to the First 10 Gigabit Ethernet**
- Al Yuen 은 UC 산타바바라 대학원을 거쳐 HP Labs 에서 포토닉스(photonics, 광자공학) 연구를 했다.
- 1999년경 HP 를 나와 첫 창업사 Alvesta 를 세웠고, 여기서 "세계 최초 10기가비트 이더넷"을 만들었다고 밝힌다.
- 이후 Coherent 에서 한 사업부를 이끌었고, 태양광·클린테크 회사를 몇 곳 거쳐 마지막으로 Lumentum 에서 일했다.
- 약 2년 전(대화 시점 기준) Playground Global 의 투자를 받아 PicoJool 을 창업했다.

**Inventing the Active Optical Cable with Mellanox**
- Alvesta 시절 초기 Mellanox(현재 Nvidia 소속, InfiniBand 생태계를 만든 회사)가 접촉해, 부피가 큰 구리 케이블을 대체할 옵틱을 커넥터 안에 넣어 달라고 요청했다.
- 이 결과가 세계 최초의 능동형 광케이블(AOC, active optical cable) — 전기로 들어가 전기로 나오되 내부에서 전기-광 변환이 일어나는 케이블 — 데모였다.
- 이후 25년간 AOC 는 데이터센터의 표준 워크호스로 쓰였다.

**The Engineer's Mindset and Why Optics Must Exit the Rack**
- Al 은 자신을 연구자(R&D)가 아니라 스펙·비용·신뢰성·도달거리를 맞추는 엔지니어로 규정한다.
- 오늘날 구리선의 도달거리는 레인당 200기가비트/초 기준 약 3~4미터로 줄었다.
- 랙 안에 GPU·CPU 를 더 많이 채우면서 랙이 뜨거워지는데, 정보를 랙 밖으로 빼려면 광 솔루션이 필요하다고 설명한다.

**Why VCSELs — 25 Years of Shipping in the Millions**
- VCSEL 은 1996년 첫 기가비트 이더넷부터 데이터센터 현장에 존재해 온 기술이라고 말한다(HP 와 Honeywell 이 초기 업체).
- 하이퍼스케일러에 납품하려면 용량·수요·비용을 모두 맞춰야 하며, 지금 이 체크리스트를 만족하는 것은 주로 구리라고 말한다(비용이 가장 낮기 때문).
- 데이터센터의 스케일업 구간은 보통 25~30미터(약 75피트)로, 도달거리가 짧을수록 물량이 많아진다고 설명한다.
- 월 수백만 개(millions per month) 규모로 출하하려면 커넥터·트랜시버·소켓 등 부품 전체(bill of material)가 그 규모를 받쳐야 하는데, VCSEL 은 이미 25년째 그렇게 출하해 왔다고 말한다.

**The Hyperscale Shift to Error-Free**
- 실리콘 포토닉스(silicon photonics)·EML(electro-absorption modulated laser)·마이크로LED 등 여러 기술이 200기가비트 전기 신호를 광 신호로 바꾸는 경쟁을 벌인다.
- 이더넷은 원래 패킷 손실·지연에 관대했지만, 수천 개 GPU 가 하나의 뇌처럼 동작하는 하이퍼스케일 시스템에서는 수십~수백 나노초 지연도 문제가 된다.
- 이 때문에 전형적인 이더넷 비트오류율(BER, bit error rate) 기준이 10⁻⁶에서 10⁻¹⁰ 이하("에러-프리")로, 나아가 10⁻¹²까지 낮아져야 했다고 말한다.
- 이 기준 변화가 원래 장거리용이던 고성능 단일모드 솔루션이 데이터센터 안으로 들어오게 된 계기라고 설명한다.
- PicoJool 은 VCSEL 을 200기가비트로, 또 100·50기가비트 NRZ(non-return-to-zero) 로 밀어 올려 낮은 BER 을 확보했다고 말한다.

**One Pizza Oven vs. 5,000 Pizzas — The Capacity Argument**
- 실리콘 포토닉스·EML·DFB(distributed feedback laser) 등 단일모드 소자도 약 25년 역사를 가졌지만, 원래는 파장분할다중화(WDM, wavelength division multiplexing)로 소수의 광섬유에 많은 정보를 실어 장거리를 가는 용도였다고 설명한다.
- 이런 업체들은 도시·국가 간 연결용으로 대략 10만(100K) 단위 물량에 맞춰 인프라를 키워 왔는데, 데이터센터가 요구하는 물량은 그보다 10~50배 크다고 말한다.
- 이를 "피자 오븐 하나로 시간당 20판 굽던 곳에 갑자기 한 시간 안에 5,000판을 주문받은" 상황에 비유한다.
- 반대로 VCSEL 은 25년간 이미 월 수백만 개를 출하해 왔으므로 새 공장(shovel to ground)이 필요 없고, VCSEL 자체 성능만 바꾸면 된다고 말한다.
- PicoJool 은 이런 이유로 VCSEL 공급이 "제약 없음(unconstrained)"이라고 부른다 — 리드타임은 4~12주의 자체 생산 사이클에 의해서만 결정되고, 공급망 병목에 의해 결정되지 않는다는 뜻이다.

**InP vs. GaAs and the Fabless Split**
- 실리콘 포토닉스·EML 은 대부분 인듐인(InP, indium phosphide) 기반이며, VCSEL 은 항상 갈륨비소(GaAs, gallium arsenide) 기반이었다고 설명한다.
- InP 는 처리 이전 단계, 즉 기판(substrate) 원재료 자체가 이미 제약돼 있다고 말한다. GaAs 는 제약이 없다("Gallium arsenide: unconstrained").
- PicoJool 같은 팹리스(fabless) 회사는 자체 클린룸 공장을 갖지 않고 파운드리(foundry)를 통해 VCSEL 칩을 생산한다.
- 칩을 실제 플러거블(pluggable) 광 엔진·트랜시버로 만들려면 레이저 드라이버, 보드, 그리고 단일모드 광섬유에 정밀 정렬하는 장비가 필요한데, 이 장비군까지 대량 생산 인프라로 갖춰진 것은 VCSEL 쪽뿐이라고 말한다.

**The VCSEL Tree of Knowledge and the Handoff to WIN**
- VCSEL 업계의 "지식 계보(tree of knowledge)"로 세 갈래를 든다: ① Honeywell → Finisar → II-VI → Coherent, ② HP → Avago → Broadcom, ③ Picolight/E2O → JDSU → (JDSU 분사) Lumentum·Viavi.
- PicoJool 팀은 Lumentum 계열 출신이며, 세 계보의 설계 노하우를 함께 흡수했다고 말한다.
- PicoJool 은 VCSEL 의 에피(epi) 층 — 내부 캐비티(cavity) 설계와 도핑(doping) 공정 — 을 설계하고, 대만의 WIN Semiconductors 에 넘겨 미가공 에피 웨이퍼를 성장시킨다.
- WIN 이 클린룸 공정을 거쳐 최종 VCSEL 소자를 만든다. VCSEL 은 엣지-이미팅(edge-emitting) 소자와 달리 웨이퍼 단계에서 개별 소자를 100% 테스트("known good die")할 수 있다는 이점이 있다고 설명한다.
- WIN 은 웨이퍼 처리까지만 담당하고, 다이싱(dicing) 이후 모듈 통합 파트너들이 능동형 광케이블이나 트랜시버로 조립한다.
- TSMC 등이 실리콘 웨이퍼 위에 광소자를 직접 패키징하는 코패키지드 옵틱스(CPO, co-packaged optics) 분야를 언급한다.

**200G/Lane and the Three Flavors of 1.6T**
- PicoJool 은 200기가비트/레인 VCSEL 을 막 발표했고 다음 분기부터 샘플링을 시작한다.
- 8채널×200기가비트를 합치면 1600기가비트(1.6테라비트)가 된다.
- 현재 출하 중인 800기가비트 트랜시버는 8×100 구성이다.
- 1.6T 를 채우는 세 가지 조합을 설명한다: ① 8×200(PAM4, 4단계 신호, 고성능·고비용, "빠르고 좁음"), ② 16×100 LPO(linear-drive pluggable optics, DSP 없이 저전력), ③ 32×50 NRZ(마이크로-VCSEL, 0/1 두 단계 신호로 신호대잡음비를 늘려 BER 을 더 낮춤).
- PicoJool 은 마케팅에서 "느리다(slow)"는 표현을 피하고 "빠르고 넓음(fast and wide)"·"더 빠르고 좁음(faster and narrow)"으로 부른다고 말한다.

**The Roadmap to 3.2T and 12.8T**
- Andy Bechtolsheim 이 만든 XPO 제품이 이미 하나의 플러거블에서 12.8T 를 낸다는 사례를 언급한다.
- 로드맵 경로 하나는 양방향(bi-di) — 기존 파장에 또 다른 파장을 하나 더해 양방향으로 신호를 보내는 방식 — 으로, 1.6T 를 3.2T 로 배로 늘릴 수 있다고 말한다.
- 다른 경로는 속도를 두 배로 늘리는 것으로, 현재 50G NRZ 를 100G NRZ 로 개발 중이며 이는 기존 200기가비트 VCSEL 을 100G NRZ 모드로 돌리는 방식이다.
- VCSEL 은 표면발광(surface-emitting) 특성상 2차원 배열(2-D array)이 가능해, 4×16 커넥터(손가락 크기라고 묘사) 안에 64채널을 넣을 수 있고, 이를 200기가비트로 구동하면 12.8T 에 도달한다.
- 400G/레인으로 가는 신기술 없이도 12.8T 로드맵이 확실하다고 주장한다.

**Lead Times, Yields, and WIN's Capacity**
- 100만 개 VCSEL 주문 시 통상 8~10주 리드타임을 준다고 말한다.
- 트랜시버까지 필요하면 VCSEL 생산 뒤 모듈 패키징에 추가로 4~6주가 붙어, 에피 성장부터 완제 모듈까지 총 12~16주가 걸린다.
- 수율(yield) — 웨이퍼당 얻는 정상(known-good) 다이 개수 — 이 높을수록 필요한 웨이퍼 수와 공장 캐파(capacity) 부담이 줄어든다고 설명한다.
- WIN 은 2016년 한 소비자 가전 응용을 위해 이 공정을 이전받은 이래 약 10년째 VCSEL 을 생산해 왔다.
- WIN 의 캐파는 주당 최대 1,000장의 웨이퍼이고, 웨이퍼 한 장에 VCSEL 약 24만 개가 들어가, 웨이퍼 약 10장이면 약 100만 개 규모가 나온다고 말한다.

**The Fabless Model — Stay Small, Leverage the Supply Chain**
- 실리콘 업계에서 팹리스 모델은 수십 년째 흔한 방식이며, AMD 도 자체 파운드리 없이 TSMC 를 쓴다고 예로 든다.
- PicoJool 은 작은 스타트업이지만 WIN Semiconductors 를 통해 월 수백만 개 규모로 출하하며 큰 광소자 업체들과 경쟁할 수 있다고 말한다.
- 회사 모토는 "작게 유지한다(stay small)"이며, 사명 PicoJool 자체가 초저전력을 뜻한다고 설명한다.

**Ramp Timing — Sampling Now, HVM in Early 2027**
- 보도자료대로 50G NRZ·100G LPO·200G 세 라인 모두 다음 분기부터 샘플링을 시작한다.
- 샘플링 이후 신뢰성 검증(qualification, 가속 노화 시험으로 10년 수명을 예측)을 거치는데, 이 기간이 소규모(티어2) 고객은 3개월, 대형(티어1) 고객은 6개월 이상 걸린다고 말한다.
- WIN 쪽 생산 램프(ramp)는 이미 준비돼 있지만, 고객과의 신뢰성 검증을 거친 뒤에야 발주가 나온다.
- 대량 생산(HVM, high-volume manufacturing) 램프 목표 시점은 2027년 초라고 밝힌다.

**Mentoring the Next Generation of Photonics Engineers**
- 지난 25년간(닷컴 시대 이후) 젊은 인력이 하드웨어·포토닉스보다 소프트웨어·응용 쪽으로 몰려, 숙련된 하드웨어 엔지니어층이 고령화됐다고 말한다.
- 로보틱스·자율주행 등으로 대역폭 수요가 계속 늘 것이라 보고, 경험 없는 젊은 엔지니어를 VCSEL·트랜시버 설계자로 키우는 일을 자신의 관심사로 꼽는다.
- 실리콘밸리에서 포토닉스·하드웨어에 대한 시장·투자 커뮤니티의 관심이 다시 커지고 있다고 말한다.

## 숫자 (원문에 나온 것만)

- 1996 — 첫 VCSEL 기반 기가비트 이더넷 등장 연도
- 1999 — Al Yuen 이 HP 를 나와 Alvesta 창업한 시기
- 25년 — VCSEL·AOC·단일모드 소자(EML·실리콘 포토닉스·DFB) 모두의 대략적 업력
- 3~4미터 — 레인당 200기가비트/초에서 구리선의 현재 도달거리
- 25~30미터(75피트) — 데이터센터 스케일업 구간의 통상 거리
- 10⁻⁶ → 10⁻¹⁰(이하), 10⁻¹² — 전형적 이더넷 BER 에서 "에러-프리" 기준으로의 변화
- 약 100,000(100K) — 기존 장거리 단일모드 소자 업체들이 익숙했던 물량 규모
- 10~50배 — 데이터센터가 요구하는 물량이 기존 장거리 인프라 대비 큰 배수
- 200기가비트/레인 — PicoJool 이 새로 발표한 VCSEL 스펙
- 8×200 = 1600기가비트(1.6테라비트) — 첫 번째 1.6T 조합
- 8×100 = 800기가비트 — 현재 출하 중인 트랜시버 구성
- 16×100 — LPO 방식의 1.6T 조합
- 32×50 NRZ — 마이크로-VCSEL 방식의 1.6T 조합
- 3.2T — bi-di(파장 하나 추가)로 얻는 다음 단계 대역폭
- 100G NRZ — 개발 중인 차기 스펙(현재는 50G NRZ)
- 4×16 커넥터 = 64채널 — 2-D 배열 커넥터 구성
- 64채널 × 200기가비트 = 12.8T — 2-D 배열 로드맵의 도달점
- 8~10주 — VCSEL 100만 개 주문 시 통상 리드타임
- 4~6주 — VCSEL 이후 모듈 패키징에 추가되는 기간
- 12~16주 — 에피 성장부터 완제 모듈까지 총 소요 기간
- 2016년 — WIN Semiconductors 가 소비자 가전용으로 VCSEL 공정을 이전받은 연도(약 10년째 생산 중)
- 주당 최대 1,000장 — WIN 의 웨이퍼 생산 캐파
- 웨이퍼 1장당 약 240,000개 — VCSEL 다이 수
- 약 10장 → 약 100만 개 — 웨이퍼 수와 VCSEL 수량의 환산 예시
- 3개월 — 티어2(소규모) 고객 신뢰성 검증 기간
- 6개월 이상 — 티어1(대형) 고객 신뢰성 검증 기간
- 2027년 초 — HVM(대량 생산) 램프 목표 시점
- 약 2년 전(대화 시점 기준) — PicoJool 창업 시점

## 그대로 인용 (영어 원문 + 한국어 옮김)

- "VCSELs, for one thing, have been around since '96 — a technology that's been in product, in the field, in data centers since 1996, starting with the first gigabit Ethernet." — Al
  VCSEL 은 우선 96년부터 있었다 — 최초의 기가비트 이더넷부터 시작해 1996년 이래 제품과 현장, 데이터센터에 있었던 기술이다.

- "the typical Ethernet bit error rate needs to drop from 10⁻⁶ to below 10⁻¹⁰, what we call error-free" — Al
  전형적인 이더넷 비트오류율은 10⁻⁶에서 우리가 "에러-프리"라 부르는 10⁻¹⁰ 이하로 떨어져야 한다.

- "Gallium arsenide: unconstrained." — Al
  갈륨비소는 제약이 없다.

- "we're not building, we're not putting shovel to ground — we're just changing the actual VCSEL." — Al
  우리는 (새 공장을) 짓지 않는다, 삽을 땅에 꽂지 않는다 — 우리는 그저 VCSEL 자체를 바꿀 뿐이다.

- "So that roadmap to 12.8T, we believe, is very solid and very clear — without even having to invent any new technology." — Al
  그래서 12.8T 로드맵은, 우리 생각엔, 새 기술을 발명할 필요조차 없이 매우 탄탄하고 명확하다.

- "Our motto is 'stay small,' and that has to do with many things — our name is PicoJool, right?" — Al
  우리 모토는 "작게 유지한다"이고, 여기엔 여러 이유가 있다 — 우리 이름이 PicoJool 이지 않나.

- "we typically give them an eight- to ten-week lead time." — Al
  우리는 통상 8~10주의 리드타임을 준다.

## 주의

- "Picolight and E2O" (계보 설명 부분) — 실제 업계에 알려진 회사명은 "E20 Communications"다. 전사에서 "E2O"로 표기된 것은 청취/전사 과정의 오기일 가능성이 있다.
- "we created the world's first 10 gigabit Ethernet"(1999년, Alvesta) — 이는 Al Yuen 본인의 발언이며, 이 노트는 원문을 옮길 뿐 사실 검증을 하지 않는다.
- 숫자 환산("웨이퍼 약 10장 → 약 100만 개")은 원문에서도 "maybe"·근사치로 언급된 것으로, 정확한 산술값(10장×24만개=240만개)과 어긋난다 — 원문 화자의 어림을 그대로 옮긴 것이며 이 노트가 재계산·보정하지 않았다.
