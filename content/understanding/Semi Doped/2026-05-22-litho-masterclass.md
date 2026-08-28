---
title: 파장이 줄어든 만큼 값이 올랐다 — 리소그래피의 경제학
date: 2026-05-22
source: https://daily.semidoped.com/p/a-masterclass-on-ic-lithography
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: fab
topic: EUV · 멀티패터닝 · 노광 장비 값
gain: 365나노미터에서 13.5나노미터까지 온 광원의 역사와, 그 대가로 장비 한 대가 2.5억에서 4억 달러가 된 셈. EUV 를 못 구하면 왜 패터닝을 서너 번 반복해야 하는지, 그리고 광원을 서비스로 팔겠다는 쪽과 X선으로 가겠다는 쪽.
---

## 한 줄
DUV에서 EUV로 넘어온 리소그래피(lithography)의 경제학과 공학을 한 시간짜리 마스터클래스로 정리한 회차. 광원 파장의 역사, 멀티패터닝(multi-patterning)의 원리, EUV 미러의 실체, 그리고 xLight·Substrate 두 스타트업이 각각 자유전자레이저와 X선으로 판을 다시 짜려는 시도까지 다룬다.

## 사실 — 절 순서대로
- 오프닝 잡담. Leopold Aschenbrenner의 13F 공시로 옵틱스·AMD·Intel 관련주가 급락했다는 시장 이야기로 시작, 왜 첨단 EUV 리소그래피 비용이 진입장벽이 되는지로 화제 전환.
- Gavin Baker 인터뷰 인용. TSMC가 DUV·EUV 장비 도입에 신중해 산업 전체 캐파(capacity)를 의도적으로 억누르고 있다는 견해를 소개(TSMC가 EUV 도입에 소극적이고 가능한 한 DUV+멀티패터닝을 고수하려 한다는 취지).
- Austin의 클린룸 경력. 일리노이대 어바나-섐페인 대학원 시절 Eric Pop 교수 연구실에서 그래핀 기반 트랜지스터를 연구하며 리소그래피(E-beam 리소그래피 포함)를 직접 수행했다고 소개. 그래핀을 스카치테이프로 기계적 박리(exfoliation)해 단층 그래핀을 찾던 경험, 이후 구리 호일 위 화학기상증착(CVD)으로 그래핀을 성장시킨 경험을 언급.
- Rock's Law. Arthur Rock(초기 Intel 투자자)의 이름을 딴 관측으로, 반도체 팹 건설 비용이 4년마다 두 배씩 늘어난다는 법칙. 무어의 법칙(트랜지스터 수 2년마다 2배)과 비교하면 팹 비용 증가 속도가 더 느리다는 점에서, 무어의 법칙은 본질적으로 "같은 비용으로 더 많은 트랜지스터를 얻는다"는 경제학적 명제라고 재해석.
- EUV 장비 가격 추이. 저(低) NA EUV 장비는 과거 약 2.5억 달러, 현재 고(高) NA는 약 4억 달러 수준("give or take")이라고 언급. 향후 소문 속 Hyper NA 장비는 6억~8억 달러, 극단적 상황("Strait of Hormuz stays closed")이면 10억 달러까지 갈 수 있다고 추정.
- 팹 하나에 필요한 EUV 대수. CNBC 보도를 인용해 Intel의 애리조나 18A 팹(Fab 52)에 EUV 장비 15대가 필요했다고 언급(Austin, 출처를 명확히 CNBC로 지칭하되 "I think I'd seen some CNBC coverage"라고 헤지). 신규 팹 하나의 총 건설비는 대략 200억~300억 달러 수준이라고 정리.
- 클린룸의 물리적 요건. 지진에도 흔들리지 않도록 공장 바닥 전체를 피스톤 위에 띄우는 TSMC의 시공 방식, 클린룸 등급(class 1, 10, 100 등 단위 부피당 먼지 입자 수 기준) 개념을 소개. 팹 하나를 짓는 데 3~5년이 걸린다고 언급.
- Intel Fab 52 방문 경험. Austin이 최근 Intel Fab 52를 견학했다고 소개하며, 지진뿐 아니라 지나가는 차량 진동까지 신경 써야 할 정도로 미세 진동에 민감하다고 설명. 장비 아래 서브팹(sub-fab) 층에 전원·광원 관련 설비가 들어간다고 부연.
- Intel의 "copy exactly" 방식. 팹마다 배관·심지어 페인트 브랜드까지 똑같이 복제하는 방식으로, 작은 변화가 수율에 영향을 줄 수 있다는 우려에서 나온 관행이라고 설명. 이 방식이 개발 속도를 늦춘 측면도 있다고 언급.
- DUV 광원과 노광 개념. 리소그래피는 빛으로 트랜지스터(또는 식각할 영역)의 형태를 "그리는" 작업이라는 기본 개념 설명. 파장이 작을수록 더 가는 선을 그릴 수 있다는 원리를 "굵은 샤피 펜 vs 가는 촉 펜" 비유로 설명.
- Rayleigh criterion(레일리 기준). 웨이퍼 위에 만들 수 있는 최소 치수는 파장에 비례하고 수치조리개(numerical aperture, NA)에 반비례한다는 관계식이라고 소개. 여기에 K1이라는 상수 인자가 있어 마스크 설계 기법으로 이 비례계수를 개선할 수 있다고 부연.
- 광원 파장의 역사. 1980년대 i-line(365nm) → KrF(크립톤 플루오라이드, 248nm) → ArF(아르곤 플루오라이드, 193nm) 순으로 발전했다고 정리. ArF 193nm는 2000년대까지 이어졌다고 언급.
- 이머전 리소그래피(immersion lithography). 웨이퍼 위에 초순수(pure water)를 얹고 그 물을 통해 빛을 쏘는 방식으로, 이 트릭으로 유효 해상도를 더 끌어올렸다고 설명.
- 광학 리소그래피의 기원 일화. TI에서 일하던 한 연구자가 현미경을 뒤집어 반대편에서 빛을 쏘면 상이 작아진다는 아이디어에서 축소 노광(reductive printing) 개념이 시작됐다는 일화를 소개(이 인물의 이름은 대화 중반에는 기억나지 않는다고 했다가, 후반부에 Jay Lathrop이라는 이름으로 다시 언급됨).
- 멀티패터닝(multi-patterning) 비유. 미식축구 경기장 라인을 10야드 간격으로만 그릴 수 있는 기계로 5야드 간격까지 그리려면, 먼저 10·20·30…을 그리고 다시 5야드씩 옮겨서 5·15·25…를 그리면 된다는 비유로 설명. 이 방식이 LELE(litho-etch-litho-etch)라고 불린다고 확인.
- 트리플·쿼드 패터닝의 문제. 패턴 단계를 3~4회로 늘리면 마스크 정렬 난이도가 커지고, 각 단계가 선형적으로 시간을 더해 처리량(throughput)이 떨어지며, 이는 곧 트랜지스터당 비용 상승으로 이어진다고 설명.
- SMIC 사례. EUV를 확보하지 못한 SMIC(중국 파운드리)가 DUV와 쿼드패터닝 같은 기법으로 7nm급, 5nm급 트랜지스터를 만들었다고 언급.
- "2나노미터" 표기의 실체. FinFET·RibbonFET 같은 3차원 트랜지스터 구조로 인해 트랜지스터 하나를 만드는 데 60~80단계가 들어가며, "2나노미터"·"1.8나노미터" 같은 노드명은 실제 최소 치수를 뜻하지 않는 마케팅 용어가 됐다고 설명 — 실제 최소 치수는 약 30나노미터 수준일 수 있다고 언급.
- EUV에서도 남는 멀티패터닝 필요성. EUV(13.5nm)로 해상도 자체는 충분해졌지만, 수율 관점에서는 여전히 일부 멀티패터닝이 필요할 수 있다고 설명 — 짧은 파장 빛을 특정 도즈(dose)로 쏠 때 광자 수가 제한적이라 스토캐스틱(확률적) 결함이 생긴다는 점을 스프레이 페인트 비유로 설명. Fred Chen의 Substack 글을 참고문헌으로 언급.
- 13.5nm EUV 광원 생성 방식. 챔버 안에서 낙하하는 주석(tin) 방울(지름 약 50마이크론)을 레이저로 두 번 때려 플라스마를 만들고, 두 번째 타격에서 13.5nm 파장 빛이 폭발적으로 방출된다고 설명(레이저 생성 플라스마, LPP 방식).
- 빛의 손실 문제. 생성된 EUV 빛이 미러 약 13개를 거쳐 웨이퍼까지 도달하는데, 미러 반사마다 파워가 손실돼 최종적으로 생성된 EUV 파워의 한 자릿수 퍼센트(single-digit percentage) 미만만 웨이퍼에 도달한다고 설명.
- 미국 기원 기술이라는 지적. EUV 기술이 원래 미국에서 개발돼 이후 ASML에 매각됐고, 당시 미국 정부가 이를 전략기술로 규제하지 않았다는 점을 짚는다. ASML은 이후 약 20년에 걸쳐 이를 완성했다고 언급.
- High NA와 미러 크기. 산업이 저NA(0.33)에서 고NA(0.55)로 이동하며 피처 크기를 약 1.5~1.7배 더 작게 만들 수 있다고 설명. 다만 미러가 커지면서 빛의 입사각이 가팔라지는 아나모픽 광학(anamorphic optics) 문제로, 고NA 장비는 저NA 대비 절반 면적("half field")만 노광할 수 있다는 트레이드오프가 있다고 지적.
- 미러의 실체. EUV 미러는 몰리브덴과 실리콘을 40~50겹 교대로 쌓은 초정밀 구조라고 설명. Chris Miller의 책 『Chip War』에서 "미러를 독일 국토 크기로 확대해도 가장 큰 요철이 0.1mm에 불과하다"는 인용을 소개.
- 스캐너 속도로 상쇄. 고NA 장비가 노광 면적은 좁지만, 스캐너·메커트로닉스 이동 속도를 훨씬 빠르게 만들어 이를 보완한다고 설명.
- xLight 소개. 캘리포니아 소재 스타트업으로, LPP(레이저 생성 플라스마) 대신 자유전자레이저(free electron laser, FEL)를 광원으로 쓰려 한다고 소개. Pat Gelsinger가 이사회에 있다고 언급(정확한 직함은 "maybe he's the chairman or something"으로 헤지). FEL은 하나의 광원으로 여러 EUV 스캐너에 빛을 나눠 공급(광원과 스캐너의 디커플링)하는 것을 목표로 한다고 설명 — 이론상 1나노미터급까지 파장을 낮출 수 있는 잠재력이 있다고 언급.
- xLight의 비즈니스 모델. "photons as a service"로 표현 — xLight가 팹 옆에 FEL 설비를 짓고 자본 지출(capex)을 부담한 뒤, 소비한 광자(빛)량만큼 팹에 과금하는 유틸리티형 모델이라고 설명. 초기에는 기존 ASML 스캐너와 호환되는 13.5nm 빛을 공급하고, 이후 더 짧은 파장(1nm급)을 프리미엄으로 판매할 수 있다는 구상.
- Substrate 소개. 샌프란시스코 소재 스타트업으로, X선 리소그래피(X-ray lithography)를 시도한다고 소개. 과거 IBM이 1980~90년대에 트럭에 실릴 만큼 작은 싱크로트론(synchrotron)을 만들어 X선 광원 가능성을 실험한 역사가 있다고 언급.
- 싱크로트론 원리. 하전 입자를 원형(또는 타원형) 궤도에서 계속 가속시키면, 방향이 꺾일 때마다 X선이 방출된다는 원리라고 Vik가 설명.
- X선 리소그래피의 난점. X선은 물질을 투과하기 때문에 EUV처럼 미러로 반사시켜 집속(focus)할 수 없다는 것이 핵심 난제라고 설명. 그 대안으로 근접 인쇄(proximity printing) 방식을 써야 하고, 이 경우 마스크를 실제 패턴과 동일한 임계 치수로 만들어야 해 마스크 제작 난도가 훨씬 높아진다고 설명.
- Substrate의 경제적 함의. X선 리소그래피가 성공하면 EUV 장비(약 10억 달러)보다 훨씬 저렴하게 미세 공정을 구현할 수 있어, 자본이 적은 업체도 팹을 운영할 수 있게 되고, 이 기술이 미국 내에 머문다면 반도체 제조가 미국으로 돌아올 잠재력이 있다는 지정학적 함의를 논의.
- 마무리 논의. GlobalFoundries나 Texas Instruments 같은 레거시 팹도 저비용 X선 리소그래피가 실현되면 더 미세한 공정에 접근할 수 있고, 팹리스 기업도 웨이퍼당 비용이 크게 낮아질 수 있다는 함의를 짚으며 마무리.

## 숫자 (원문에 나온 것만)
- Rock's Law — 팹 건설 비용, 4년마다 2배
- Moore's Law — 트랜지스터 수, 2년마다 2배
- 저NA EUV 장비 가격 — 약 2.5억 달러(과거)
- 고NA EUV 장비 가격 — 약 4억 달러("give or take")
- Hyper NA 장비 추정가 — 6억~8억 달러, 극단적 시나리오면 10억 달러("if the Strait of Hormuz stays closed")
- Intel Fab 52(애리조나 18A)에 필요한 EUV 대수 — 15대(CNBC 보도 인용, 헤지)
- 신규 팹 건설비 — 약 200억~300억 달러
- 팹 하나에 필요한 EUV/DUV 총 대수 — 10~20대
- EUV 10대 도입 시 장비 비용만 — 약 50억 달러
- i-line 파장 — 365nm(1980년대)
- KrF 파장 — 248nm
- ArF 파장 — 193nm
- EUV 파장 — 13.5nm
- 저NA — 0.33, 고NA — 0.55
- 고NA로 얻는 피처 축소율 — 약 1.5~1.7배
- 고NA의 half field — 저NA 대비 절반 면적만 노광
- "2나노미터" 노드의 실제 최소 치수 — 약 30나노미터("may still be on the order of")
- 트랜지스터 제조 단계 수 — 약 60~80단계
- 주석(tin) 방울 크기 — 약 50마이크론
- 웨이퍼까지 도달하는 EUV 파워 비율 — 한 자릿수 퍼센트 미만
- 빛이 거치는 미러 개수 — 약 13개("like 13", 어림)
- ASML의 EUV 개발 기간 — 약 20년
- Chip War 인용 수치 — 미러를 독일 국토 크기로 확대 시 최대 요철 0.1mm

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "if the mirrors in the EUV system were scaled to the size of Germany, their biggest irregularities would be a tenth of a millimeter." — "EUV 시스템의 미러를 독일 크기로 확대해도, 가장 큰 요철은 0.1mm에 불과하다." (Vik, 『Chip War』 인용)
- "real men will have fabs again." — "진짜 사나이는 다시 팹을 갖게 될 것이다." (Vik, Jerry Sanders 발언 인용)
- "if you're writing with a Sharpie, you're going to draw fat lines." — "샤피 펜으로 쓰면 굵은 선이 그려진다." (Austin)
- "photons as a service." — "서비스형 광자." (Austin, xLight의 비즈니스 모델 설명)
- "it's very difficult to actually focus X-rays... You can't reflect them. That's a big problem." — "X선은 실제로 집속하기가 매우 어렵다... 반사시킬 수가 없다. 그게 큰 문제다." (Vik)
- "something that's called two nanometers, the smallest dimension may still be on the order of 30 nanometers." — "'2나노미터'라 불리는 것도, 실제 최소 치수는 여전히 30나노미터 수준일 수 있다." (Austin)

## 주의
- Hyper NA 장비 가격(6억~8억 달러, 극단적으로 10억 달러)은 "rumored"라고 명시된 소문 수준 추정치이며, "Strait of Hormuz stays closed"라는 가정이 붙은 헤지 발언이다.
- Intel Fab 52의 EUV 15대라는 수치는 Austin이 "I think I'd seen some CNBC coverage"라고만 밝힌 2차 출처 인용이다.
- EUV 미러를 거치는 개수("13개")는 Vik가 "it goes through like 13 different mirrors"라고 어림한 수치다.
- "2나노미터" 노드의 실제 최소 치수(약 30nm)는 Austin이 "may still be on the order of"라고 헤지한 추정치다.
- xLight 이사회에서 Pat Gelsinger의 직함은 "maybe he's the chairman of the board or something"이라고 불확실하게 언급됐다.
- 리소그래피 축소 노광 개념을 고안한 인물의 이름은 대화 중반 "I forget the name of this guy"로 넘어갔다가, 후반부에 Jay Lathrop으로 다시 언급되는데 — 전사 상 정정된 것인지 확인이 필요한 대목이다.
- EUV 장비 가격(저NA 2.5억 달러, 고NA 4억 달러)은 "These numbers change over time, and it probably depends per customer"라고 명시적으로 유동적이라 밝힌 수치다.
