---
title: 엔비디아의 마벨 투자는 경쟁 칩 지원이 아니라 NVLink 표준 장악을 위한 포석이다
date: 2026-04-03
source: https://www.youtube.com/watch?v=oWQG207QPvk
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: link
topic: NVLink Fusion 투자 · 메모리 호그 사이클 · 인텔 아일랜드 팹 재매입
gain: NVLink Fusion 투자를 "XPU 키우기"가 아니라 인터커넥트 표준 장악으로 읽는 관점, HBM 전환이 표준 DRAM 웨이퍼를 갈아 먹는 구조, Apollo가 인텔 아일랜드 팹 지분 매매로 2년 만에 30억 달러를 남긴 경위.
---

## 한 줄
이번 회차는 세 화제를 다룬다. 먼저 NVIDIA가 경쟁사 마벨(Marvell)의 NVLink Fusion(NVIDIA의 개방형 랙스케일 인터커넥트 플랫폼)에 낸 투자를 두고 Austin Lyons과 Vik Sekar가 "XPU(범용 GPU 대신 특정 워크로드에 맞춘 커스텀 칩)를 키워주는 게 왜 NVIDIA에 이득인가"를 풀어내고, 이어 DRAM·NAND 가격이 폭등한 메모리 사이클을 진단하며 이번엔 AI 수요가 소비자 수요 둔화를 흡수할지를 따진다. 마지막으로 Intel이 2년 전 사모펀드 Apollo에 팔았던 아일랜드 팹(Fab 34) 지분 49%를 도로 사들인 사건을 짚는다.

## 사실 — 절 순서대로
- 인사·주제 예고. Austin Lyons(Chipstrat)과 Vik Sekar(Vik's Newsletter)가 진행을 맡았고, 이번 회차는 마벨 투자와 메모리, 인텔 아일랜드 팹 세 화제를 다룬다고 예고했다.
- NVIDIA-마벨 발표문 인용. Austin이 보도자료를 읽었다 — 마벨이 NVLink Fusion 호환 커스텀 XPU와 스케일업 네트워킹을 제공하고, NVIDIA는 Vera CPU·ConnectX NIC·BlueField DPU·NVLink 인터커넥트·Spectrum-X 스위치 등을 지원한다는 내용이다.
- Vik의 첫 반응. Vik는 "NVIDIA가 왜 경쟁자에 투자하나"가 첫 의문이었다고 말했다 — 커스텀 ASIC이 GPU를 대체할 위협인데 그걸 돕는 게 이상해 보였다는 것.
- 실리콘 포토닉스 언급. Austin은 보도자료에 마벨과 NVIDIA가 실리콘 포토닉스(광 신호로 칩 간 데이터를 주고받는 기술) 협력도 명시돼 있다고 짚었다.
- Celestial AI 인수 연결. Vik는 마벨이 앞서 인수한 Celestial AI의 "포토닉 패브릭"(광 인터커넥트로 다이 간을 연결하는 기술)을 언급하며, 세부는 자신도 "다시 확인해봐야 한다"고 전제를 달았다.
- NVLink 광학화 가능성. Vik는 NVLink가 현재 구리 배선(SerDes 회로로 신호를 주고받는 물리 계층) 위에서 돌지만, 프로토콜 자체는 광학 매체로도 작동할 수 있다고 말했다 — "이론적으로는 가능하다"는 수준의 추정이다.
- 이질적 실리콘 프레이밍. Austin은 GTC에서 NVIDIA가 Vera Rubin과 (NVIDIA로 편입된) Groq LPU를 함께 쓰는 "탈중앙 추론" 구상을 밝힌 점을 들며, 마벨 XPU도 NVLink로 같은 데이터센터에 묶으려는 포석일 수 있다고 풀었다.
- AWS-마벨 관계. Austin은 Amazon Trainium이 이미 마벨을 백엔드 파트너로 쓰고 있고, 2025년 12월 2일 무렵 NVLink Fusion 관련 발표에서 Trainium이 NVLink와 UALink를 함께 쓸 가능성이 언급됐던 것으로 기억한다고 전했다 — 정확한 표현은 자신도 "다시 확인해야 한다"고 밝혔다.
- Austin의 "필요 기반" 가설. Austin은 AWS가 NVLink를 요구하는데 마벨 혼자서는 구현이 안 되니 NVIDIA에 협력을 요청했고, NVIDIA는 그 대가로 인터커넥트·플랫폼 전체를 쥔다는 가설을 제시했다 — 스스로 "제 추측이고 실제로 맞는지는 모르겠다"고 못 박았다.
- 마벨의 이중 프로토콜. Vik는 마벨이 NVLink와 UALink(NVIDIA 밖의 개방형 스케일업 표준)를 둘 다 지원하게 돼 고객이 어느 쪽을 고르든 대응 가능해졌다고 짚었고, 반대로 브로드컴은 UALink만 있고 NVLink가 없다고 대비했다.
- 마벨의 스위치 실리콘. Austin은 마벨이 2025년 6월 커스텀 UALink 스케일업 스위치를 발표했고, 이름이 "XCON"으로 들리는 회사를 5억 4천만 달러에 인수했으며, "Strata S"라는 다중 레인 PCIe 6.0 스위치도 보유하고 있다고 전했다(두 이름 모두 자막 오인식 가능성 있음, 「주의」 참조).
- GPU 수요는 안 줄어든다. Vik는 최근 나온 Blackwell Ultra의 MLPerf 추론 벤치마크가 여전히 훌륭하다며, XPU가 늘어도 학습·추론 수요가 워낙 커서 GPU 판매가 줄지 않을 것이라고 말했다.
- Upscale AI 사례. Austin은 스타트업 Upscale AI가 NVLink·UALink·이더넷 계열 프로토콜(자막상 "E-Sun"으로 들림, 「주의」 참조)을 하나의 스위치 실리콘("Skyhammer")에서 다 돌리려 한다고 소개했다.
- NVIDIA의 인재 영입. Austin은 NVIDIA가 약 2개월 전 Upscale AI의 창립 멤버였던 칩 아키텍트를 NVLink Fusion 팀으로 영입했다는 기사를 봤다고 언급했다 — "음모론이 자란다"는 농담을 덧붙였다.
- 표준 단일화 가능성 토론. Vik는 NVLink가 결국 유일한 스케일업 표준이 될 수 있느냐고 물었고, Austin은 AMD가 NVIDIA에 유리한 표준을 지지할 이유가 없다며 역사적으로 인터커넥트 표준이 하나로 좁혀진 적이 없다고 반박했다(USB·XKCD 표준 만화 비유).
- 마벨 화제 마무리. Austin은 실제 제품이 나오는 걸 봐야 한다며, 지금은 추측과 음모론 수준이라고 정리했다.
- 메모리 화두 전환. Vik는 이번 주 자신이 쓴 서브스택(Substack) 글을 소개하며 "메모리가 미쳤다"는 말로 화제를 열었다.
- DRAM·NAND 가격 급등. Vik는 2026년 1분기 DRAM 계약가가 전분기 대비 95% 올랐고 NAND도 약 60% 올랐다고 밝혔고, TrendForce는 2분기 계약가가 1분기 대비 58~60% 더 오를 것으로 전망했다고 덧붙였다 — "2017~2018년 사이클 이후 이런 상승 속도는 없었다"고 말했다.
- 소비자 제품 대응. Vik는 스마트폰·PC 제조사가 RAM 원가 부담(완제품 자재비의 20~30%까지 커질 수 있다는 우려)에 저가·중가 제품을 접거나 사양(예: 8GB RAM을 4GB로)을 낮추는 방식으로 대응한다고 설명했다.
- 메모리 호그 사이클. Vik는 이 패턴을 돼지고기 값이 오르면 농가가 몰려 사육하다 한꺼번에 출하해 가격이 무너지는 "호그 사이클"(hog cycle, 돼지 사육 주기에 빗댄 표현)에 비유했다 — 소비자 수요가 꺾이면 결국 공급 과잉과 가격 붕괴로 이어진다는 것.
- 이번엔 다를까. 두 사람은 소비자 수요가 꺾여도 AI 수요(서버용 HBM·DDR)가 그 물량을 흡수할지를 핵심 질문으로 던졌다.
- 라인 전환 사례. Vik는 마이크론이 소비자용 Crucial 브랜드 DRAM 라인을 단종했고, SK하이닉스·삼성도 DRAM 생산 라인을 HBM으로 전환하고 있다고 전했다 — "이제는 마진(margin)이라는 말도 조심스럽다, ASP(평균판매가)가 높다는 게 더 정확하다"고 스스로 표현을 고쳤다.
- 웨이퍼 배분 트레이드오프. Vik는 HBM이 관통 실리콘 비아(TSV, 칩을 수직으로 쌓아 전기적으로 연결하는 구조) 둘레의 여백 공간 때문에 같은 비트를 만드는 데 표준 DRAM보다 웨이퍼를 3배(향후 4배까지) 더 써야 한다고 설명했다.
- 소비자 웨이퍼는 어디로. Austin은 스마트폰·PC용으로 안 팔린 웨이퍼가 그냥 데이터센터용으로 넘어가면 되니 문제가 아니라고 봤고, Vik는 그 웨이퍼가 HBM행이 될지 표준 DRAM행이 될지가 관전 포인트라고 맞받았다 — 표준 DRAM도 이제 ASP가 좋아졌기 때문이다.
- 과거 사이클과의 비교. Vik는 과거 클라우드 서버 사이클이나 암호화폐 채굴 붐 때는 소비자 수요 둔화를 다른 수요가 흡수하지 못해 결국 공급 과잉이 왔다고 말했다 — 이번엔 AI 수요가 "한동안은" 흡수할 수 있을 것 같다고 했지만 "추측"이라며 확신은 아니라고 덧붙였다.
- 장기계약 구조 변화. 두 사람은 메모리 계약이 과거 분기·연 단위에서 이제 3~5년 장기계약(가격 하단을 못박는 최저가 조항 포함)으로 바뀌었다고 짚었다 — 공급사·구매사 모두 물량 가시성을 얻으려는 목적이다.
- 과잉 구독 우려. Vik는 하이퍼스케일러들이 장기계약에서 물량을 과다하게 확보하고 있을 수 있다고 말했지만 "그게 실제로 과잉 구독인지는 모르겠다"고 유보했다.
- PC·모바일 전망. Vik는 2026년 PC 출하량이 12~13% 줄어들 것이라는 전망들을 인용했고, NVIDIA의 Vera CPU가 스마트폰과 같은 LPDDR(저전력 DDR)을 쓴다는 점에서 LPDDR 공급 경쟁자가 새로 생겼다고 짚었다.
- Apple 매집설. Vik는 "확인된 건 아니고 소문일 수 있다, 인용하지 말아 달라"고 전제한 뒤, Apple이 DRAM을 비싸게 사들여 경쟁사를 공급에서 밀어내고 있다는 소문을 X(트위터)와 다른 매체에서 봤다고 전했다.
- 라즈베리파이 사례. Vik는 라즈베리파이가 작년 12월 이후 3개월 동안 가격을 세 번 올렸다고 언급했다.
- 화제 전환. Austin이 남은 시간이 얼마 없다며 마지막 화제인 Intel의 아일랜드 팹 재매입으로 넘어갔다.
- Intel의 재매입 발표. Austin은 Intel이 사모펀드 Apollo가 보유한 아일랜드 팹(Fab 34, Intel 4·Intel 3 공정용이며 유럽 내 유일한 EUV 팹이라고 Vik가 부연) 지분 49%를 142억 달러(현금+신규 채무 65억 달러)에 되사들인다고 전했다 — 정확한 위치가 아일랜드인지는 "아마 그럴 것"이라며 스스로 확신 없이 말했다.
- 되사는 배경. Vik는 2년 전 Intel이 자금난 속에서 Fab 34 지분 49%를 112억 달러에 Apollo에 팔았고, 그 1년 전에는 184억 달러를 들여 이 팹을 지었다고 정리했다 — Apollo는 2년 만에 30억 달러 차익을 남겼다.
- 신호 해석 논쟁. Austin은 이 재매입이 Intel이 자사 파운드리(18A P·14A 등 향후 공정)에 대한 자신감을 보이는 신호일 수 있다고 봤고, Vik는 "그렇게까지 확대해석은 안 하겠다, 모르겠다"며 수율에 대한 결론으로 잇는 데 신중했다.
- 재매입 경제성. Austin은 Intel이 49%의 이익을 계속 Apollo에 내주는 것보다 지금 30억 달러를 더 얹어 지분 전체를 확보하는 쪽이 낫다고 판단했을 것이라는 논리를 제시했다 — 향후 이 팹에서 나올 이익이 그 이상일 것으로 본다는 뜻이다.
- 모노폴리 비유. Vik는 이를 보드게임 모노폴리에서 저당(mortgage) 잡힌 부동산을 다시 사들이는 것에 비유했다 — 힘들 때 저당 잡혔다가, 상대가 자꾸 그 칸에 걸릴 것 같으면 다시 사들이는 것과 같다는 설명이다.
- 클로징. 진행자들은 청취자에게 리뷰·공유를 부탁하며 마무리했다.

## 숫자 (원문에 나온 것만)
- 약 20억 달러 — NVIDIA가 마벨에 낸 NVLink Fusion 투자 규모(진행자들이 정확한 금액이 아니라 "20억 달러쯤인가" 식으로 어림으로 언급)
- 2025년 6월 — 마벨이 커스텀 UALink 스케일업 스위치를 발표한 시점
- 5억 4천만 달러 — 마벨이 "XCON"(표기 불확실)이라는 회사를 인수한 금액
- 2개월 전 — NVIDIA가 Upscale AI 창립 멤버(칩 아키텍트)를 NVLink Fusion 팀으로 영입한 시점
- 2025년 12월 2일 — Amazon Trainium 관련 NVLink Fusion 발표 시점(Austin이 정확한 문구는 재확인이 필요하다고 밝힘)
- 95% — 2026년 1분기 DRAM 계약가의 전분기 대비 상승률
- 약 60% — 같은 기간 NAND 가격 상승률(어림)
- 58~60% — TrendForce가 전망한 2026년 2분기 계약가의 1분기 대비 상승률
- 20~30% — RAM이 완제품 자재비(BOM)에서 차지할 것으로 우려되는 비중
- 3배(향후 4배 전망) — HBM 생산에 필요한 웨이퍼 비트 수(표준 DRAM 대비)
- 3~5년 — 최근 메모리 장기계약의 기간
- 12~13% — 2026년 PC 출하량 하락 전망
- 3회 — 라즈베리파이가 작년 12월 이후 3개월 동안 가격을 올린 횟수
- 142억 달러 — Intel이 아일랜드 팹(Fab 34) 지분 49%를 재매입한 금액
- 65억 달러 — 재매입 자금 중 신규 채무로 조달한 금액
- 49% — Apollo가 보유했던 Fab 34 지분
- 112억 달러 — 2024년 Intel이 Apollo에 그 지분을 매각한 가격
- 184억 달러 — Fab 34를 처음 지을 때 들어간 투자액
- 30억 달러 — Apollo가 2년 만에 남긴 차익(=Intel이 재매입에 더 얹어 지불한 금액)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "So, the first thing that came to mind when I heard this was why is NVIDIA investing in its competitor?" — Vik. "이걸 들었을 때 가장 먼저 떠오른 생각은, NVIDIA가 왜 경쟁자에 투자하냐는 거였어요."
- "It's my speculation, and I do feel like the customer pull of Amazon saying, 'Let's make this happen,' is an interesting angle. We'll see if it's true." — Austin. "이건 제 추측이에요. 아마존이 '이걸 성사시키자'며 끌어당긴 고객 쪽 힘이 있었다는 게 흥미로운 관점이라고 느껴지긴 하는데, 실제로 맞는지는 지켜봐야죠."
- "So, this is what is called the memory hog cycle, you know, it's like hog as in pigs because this is like when pork prices go up, all the farmers go and they start raising pigs." — Vik. "이게 바로 '메모리 호그 사이클'이라고 부르는 거예요. 돼지고기 값이 오르면 농가들이 몰려가서 돼지를 키우기 시작하는 것과 같은 거죠."
- "The rumor is that Apple is like overpaying for DRAM right now and buying up, vacuuming up all the DRAM supply so that the competitors can't get to it." — Vik(전제: "Don't quote me on it. Might be a total rumor."). "소문에 따르면 Apple이 지금 DRAM을 비싸게 사들여서 경쟁사가 못 사도록 물량을 다 빨아들이고 있다는 거예요."
- "So unless Intel believes that they don't want to give 49% of the profits and that it is better to pay today the 3 billion dollars extra to buy it back... then why would they spend the money?" — Austin. "Intel이 이익의 49%를 계속 내주기 싫고, 오늘 30억 달러를 더 얹어 되사는 게 낫다고 판단한 게 아니라면, 왜 그 돈을 쓰겠어요?"
- "You know what it reminds me of when you play Monopoly and you could mortgage your properties, like in the good times you're buying all these properties and then times get bad and then you're like, oh crap, I need to mortgage these things." — Vik. "모노폴리 게임에서 부동산을 저당 잡히는 것과 비슷해요. 좋을 때는 부동산을 계속 사들이다가, 상황이 안 좋아지면 '아, 이거 저당 잡혀야겠다'가 되는 거죠."

## 주의
- "$2 billion" 투자 규모는 두 진행자가 농담처럼("NVIDIA $2 쿠키") 반복해 부른 어림값이고, 끝에서도 "whatever, $2 billion or something"이라고만 말해 정확한 금액이 확인되지 않는다.
- "XCON"(마벨이 인수했다는 회사)과 "Strata S"(마벨의 PCIe 6.0 스위치)는 자막 음성인식이 실제 이름을 잘못 받아 적었을 가능성이 있다 — 정확한 명칭은 전사에서 확인할 수 없어 자막 표기를 그대로 남겼다.
- "E-Sun"(Upscale AI·브로드컴이 지지한다고 언급된 이더넷 계열 표준)도 자막 오인식으로 보인다 — 문맥상 다른 이더넷 기반 스케일업 표준을 가리키는 것으로 추정되나 확정할 수 없다.
- 전사 중 "A6"라는 표기가 여러 번 나오는데, 문맥(랙에 들어가는 GPU 또는 XPU를 세는 대목)상 ASIC/XPU를 자막이 잘못 받아 적은 것으로 보여 본문에는 뜻으로 풀어 옮기고 직접 인용하지 않았다.
- Amazon Trainium이 NVLink Fusion 발표에서 정확히 어떻게 언급됐는지, Celestial AI의 고객이 실제로 Trainium인지는 Austin·Vik 두 사람 모두 스스로 "다시 확인해야 한다"고 밝힌 미확정 정보다.
- 마벨-NVIDIA 투자 동기 전체("필요 기반" 가설)는 Austin이 명시적으로 "제 추측"이라고 밝힌 해석이며, 온라인 반응("Jensen이 갈락시 브레인")과 나란히 소개된 또 다른 해석일 뿐 결론이 아니다.
- Apple의 DRAM 매집설은 Vik 본인이 "인용하지 말아 달라, 소문일 수 있다"고 전제한 뒤 전한 미확인 정보다.
- Intel 아일랜드 팹의 위치는 Austin이 "아마 아일랜드 맞죠?"라고 되묻는 형태로 확인 없이 말했다 — 전사 frontmatter의 원제("Intel's Ireland Fab")를 근거로 이 노트에서도 아일랜드로 표기했다.
- 18A P·Intel 3·Intel 4 등 공정 명칭은 전사에 나온 표현 그대로만 옮겼고, 실제 로드맵 문서와 대조하지는 않았다.
- 전사는 유튜브 자막에서 자동 옮긴 것으로 화자 표시(>>)가 드문드문하며, 이 노트의 화자 귀속은 대화 맥락(질문·응답 순서, 서로를 부르는 방식)으로 추정한 것이라 일부 발언은 화자가 바뀌었을 가능성이 있다.
