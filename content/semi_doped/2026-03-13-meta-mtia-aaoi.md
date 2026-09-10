---
title: 메타 MTIA는 칩렛 재사용으로 반도체를 6개월마다 낸다
date: 2026-03-13
source: https://www.youtube.com/watch?v=bsY1vNAATCE
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: compute
topic: 메타 MTIA 칩렛 전략 · Applied Optoelectronics(AAOI) 레이저 · Arista와 광서킷 스위칭(OCS)
gain: 메타가 랭킹·추천 추론에 맞춘 자체 칩(MTIA)을 칩렛 재사용으로 6개월마다 새로 내는 전략과, 레이저 회사 AAOI가 2017년과 같은 급등 뒤 폭락을 다시 겪을 위험을 함께 짚는다.
---

## 한 줄
Austin Lyons와 Vik Sekar가 Synopsys 패널 후기로 문을 연 뒤, Vik의 Arista·광서킷 스위칭(OCS) 글, Austin의 "메타는 반도체를 6개월마다 낸다" 글(MTIA 칩렛 전략), 마지막으로 레이저 회사 Applied Optoelectronics(AAOI)의 급등과 2017년 붕괴 데자뷔까지 세 갈래를 훑는다.

## 사실 — 절 순서대로
- 예고. Austin은 이번 회차에서 자신이 참석한 Synopsys Converge 패널 후기, Vik가 그 주에 쓴 글, 메타의 추론 가속기 칩, 시간이 남으면 Applied Optoelectronics(AAOI)까지 다루겠다고 예고했다. Vik는 AAOI를 다뤄달라는 독자 요청이 여러 번 있었다고 덧붙였다.
- Synopsys 패널. Austin은 Synopsys Converge의 executive forum에서 "칩 설계에서의 에이전틱(agentic) AI"를 주제로 패널을 진행했다고 소개했다. 참석자는 Nvidia의 Kari Briski(자막 표기는 "Carey Brisky"), OpenAI 하드웨어 총괄 Richard Ho, Microsoft의 Asim Datta, Synopsys의 Roger Tebbet이었다.
- 이름을 깜빡한 일화. Austin은 패널이 끝난 뒤 다음 발표자로 소개해야 했던 Synopsys 최고매출책임자(CRO) Mike Ello의 이름을 무대에서 순간 기억하지 못해 "다음은 Synopsys에서 온 분인데 이름이 기억 안 난다"고 말해버렸다는 일화를 전했다. Mike Ello는 Synopsys로 오기 전 Siemens EDA CEO였다고 덧붙였다.
- 판단력론. Austin은 패널에서 나온 논지로, 시니어 엔지니어·아키텍트가 쌓은 것은 코딩 실력이 아니라 판단력과 안목이며 에이전틱 AI가 개별 작업을 자동화해도 이 판단력까지는 못 갖춘다고 정리했다.
- 주니어 기회론. Austin은 반대로 주니어 엔지니어에게 좁은 업무를 넘어서는 책임을 맡겨 시니어로 성장하는 시간을 앞당길 수도 있다는 낙관적 해석을 제시했다. 다만 멘토링이 뒤따라야 한다고 덧붙였다.
- 현장 체감. Vik는 이런 도구를 만드는 스타트업들, 그리고 지금 시장에서 취업이 어려운 주니어 엔지니어들과도 이야기해봤다며, 회사들이 "AI가 대신할 수 있다면 채용을 줄이자"는 쪽으로 기울고 있다고 전했다.
- 코드화 아이디어. Vik는 시니어의 판단이 AI를 매개로 코드화되어 주니어에게 전달될 수 있고, 이 경우 주니어의 역량이 크게 끌어올려질 수 있다는 아이디어를 냈고 Austin이 전적으로 동의했다.
- Arista와 OCS. Austin이 Vik의 그 주 글(광서킷 스위칭이 Arista에 미칠 영향)을 물었다. Vik는 Arista가 자체 반도체 없이 Broadcom Tomahawk 스위치 실리콘을 사다 박스에 넣고, EOS라는 소프트웨어로 패킷 스위칭·혼잡 제어 의사결정을 처리해 높은 마진("블루박스")을 만든다고 설명했다.
- OCS의 한계. Vik는 광서킷 스위칭이 전기적 패킷 스위칭 없이 빛을 그대로 반사해 전달하는 방식이라 매력적이지만, 아직 Arista의 소프트웨어 정교함을 대체할 만큼 성숙하지 않았다는 결론을 자신의 글에서 냈다고 밝혔다.
- 다차원 체스 가설. Austin은 이 논지가 Vik가 지난 회차에서 낸 "Hock Tan이 구리(전기 스위칭 영역)에 계속 투자하는 것은 다차원 체스(four-dimensional chess, 여러 수 앞을 내다보는 전략)"라는 가설과 연결된다고 짚었고 Vik가 확인했다. Austin은 나아가, 전기적 패킷 스위칭이 사라지면 Arista의 소프트웨어 우위 자체가 흔들려 화이트박스처럼 될 수 있다는 이차 효과를 짚었다.
- 메타 MTIA 글 소개. Vik가 Austin이 쓴 "메타는 반도체를 6개월마다 낸다" 글을 소개해달라고 요청했다.
- 메타의 본질. Austin은 메타를 소셜미디어 회사로 여기기 쉽지만 본질은 광고 사업이며, 2011년경 피드와 알고리즘 피드 도입 이후 랭킹·추천이 핵심 기술이 됐다고 짚었다.
- 세 시스템 — Andromeda. Austin은 광고 파이프라인 첫 단계 "Andromeda"가 방대한 후보 광고군에서 사용자에게 보여줄 수 있는 수천 개 후보를 골라내는 검색(retrieval) 역할을 한다고 설명했다. 원래 Nvidia Grace Hopper와 공동 설계됐지만, 최근 실적발표에서는 이 워크로드가 Nvidia·AMD·메타 자체 MTIA 칩까지 여러 하드웨어에서 돈다고 밝혔다고 전했다.
- 세 시스템 — Lattice. Austin은 두 번째 단계 "Lattice"가 Andromeda가 골라낸 후보 중 실제로 보여줄 광고를 순위 매기는 역할이며, 피드·스토리·릴스·메신저 신호를 하나로 묶은 단일 통합 모델을 쓴다고 설명했다. 다만 이 모델이 어떤 하드웨어에서 도는지는 자신도 찾지 못했고 GPU일 것으로 추정한다고 밝혔다.
- 세 시스템 — Gem 파운데이션 모델. Austin은 세 번째로 추천용 "Gem 파운데이션 모델"을 소개했다 — 추천 시스템 중 처음으로 LLM과 같은 스케일링 법칙(컴퓨트를 더 넣으면 결과가 더 나아지는 양상)을 보였다고 설명했다. 다만 이 큰 모델 그대로는 35억 일간 활성 사용자에게 서비스하기엔 너무 비싸, 교사-학생(teacher-student) 방식으로 작은 모델들에 지식을 증류(distill)해 실서비스에 쓴다고 밝혔다.
- MTIA300 사양. Austin은 MTIA300이 800W급 가속기로 스케일아웃 대역폭이 초당 200GB로 매우 높은 반면, 연산량(flops)은 LLM 디코딩만큼 크지 않다고 정리했다 — 임베딩 테이블을 조회하는 메모리 접근·용량 중심 워크로드에 맞춘 설계라는 것이다. 현재 수십만 대가 실서비스에 배치돼 있다고 메타 블로그를 인용해 밝혔다.
- 칩 세대 구분. Vik는 MTIA 100·200은 이미 몇 년 전부터 나와 있던 세대이고, 이번에 새로 발표된 것은 300·400·450·500이라고 정리했다. MTIA300은 컴퓨트 칩 1개, 네트워크 칩 2개, 다량의 HBM(고대역폭메모리)으로 구성되며, 저지연 워크로드임에도 네 칩 모두 SRAM 언급이 없고 전부 HBM 기반이라고 짚었다.
- SRAM 미언급의 해석. Vik는 SRAM이 전략의 핵심이 아니고 처리량(throughput)이 지연시간보다 더 중요한 최적화 목표라는 뜻으로 해석했다. Austin은 메타가 Nvidia의 Groq 인수 같은 초저지연 SRAM 스타트업을 인수할 수도 있지 않겠냐면서도 "잘 모르겠다, 그럴 수도 있다"며 확신하지 못했다.
- 4개 칩을 2년 만에. Vik는 반도체 하나를 팹에서 만드는 데만 최소 2~3개월이 걸리는데, 메타가 2년 안에 네 개 칩을 낸다는 것 자체가 "말이 안 될 정도"라고 놀라움을 표했다. Austin은 이것이 가능한 이유가 칩렛(chiplet, 여러 작은 다이를 조합해 만드는 방식)화라고 설명했다 — 세대마다 컴퓨트 다이·네트워크 다이의 조합만 바꿔 새 제품을 만든다는 것이다.
- 생성형 AI 쪽 확장. Vik는 MTIA500이 최대 400~500GB의 HBM을 갖춰 랭킹·추천뿐 아니라 생성형 AI(Gen AI)도 함께 겨냥한다고 짚었다.
- 과도한 GenAI 프레이밍 비판. Austin은 투자자들이 메타를 "라마(Llama)가 OpenAI·Anthropic보다 못하다"는 생성형 AI 서사로만 평가하는 데 과도하게 치우쳐 있다고 지적했다 — 메타의 실제 핵심 사업과 칩 전략은 랭킹·추천이라는 것이다.
- 제조사 확인. 두 사람은 이 커스텀 ASIC(주문형반도체)을 누가 만드는지 논의했다 — Broadcom의 커스텀 ASIC 사업이라는 데 동의했고, Marvell도 관여하는지는 "늘 나오는 의문"이라 별도 확인이 필요하다고 밝혔다.
- Broadcom 실적발표 반응. Austin은 The Information이 "메타가 트레이닝용 칩 계획을 접었다"고 보도한 지 며칠 뒤 Broadcom 실적발표에서 Hock Tan이 "메타는 좋은 고객이고 다 잘 되고 있다"고 진화에 나섰다고 전했다. 메타의 MTIA 계약은 고객주도설계(COT, customer owned tooling)가 아니라 그대로 Broadcom 커스텀 ASIC 방식이라고 확인했다.
- 생성형 AI의 실제 쓸모. Austin은 메타가 생성형 AI를 다국어 더빙(예: 영어 대화를 만다린으로), 광고 크리에이티브 자동 생성 등 광고 참여·전환을 늘리는 데 쓴다고 설명했다. 이 때문에 400·450·500 세대는 HBM 용량과 저정밀 연산량을 늘리되, 학습용 대규모 스케일아웃 네트워크 비중은 줄이고 추론용 스케일업 도메인은 16노드에서 72노드로 늘렸다고 짚었다.
- 팀 구성 방식. Austin의 질문에 Vik는 네 세대 칩이 모두 같은 핵심 실리콘 IP를 공유하고, 세대마다 다이 간 인터페이스 위치 같은 작은 구조 변경만 들어간다고 답했다. "유사성에 의한 검증(qualifying by similarity)"이라는 방법으로 변경이 작을 때는 전체 재검증 대신 증분 테스트만 거친다고 설명했다.
- Rivos 인수. Vik는 메타가 원래 MTIA 1·2세대 설계를 도왔던 회사(자막에는 "Rivers"로 표기됐으나 애플 출신 창업자·소송 이력 등 정황상 Rivos로 추정)를 인수했다고 전했다. 창업 초기 엔지니어 100명으로 출발해 이후 애플 출신 창업자들의 인맥으로 50명을 추가 채용했으며, Lip-Bu Tan이 자신이 투자자로 있던 벤처투자사(자막에는 "Walden Investments/Capital"로 표기, Walden International로 추정)를 통해 문제 해결에 관여했다고 밝혔다.
- AAOI 소개. Vik는 Applied Optoelectronics(AAOI)를 텍사스의 작은 레이저 회사로 소개하며, 6개월 만에 주가가 약 700% 뛰어 10달러대에서 100달러대로 올랐다고 밝혔다. 인듐인화물(InP) 기판부터 레이저, 모듈레이터, 커넥터까지 전부 자체 생산하는 수직계열화가 특징이라고 설명했다.
- 정정 — 기판 생산. Austin이 기판까지 직접 재배하는지 묻자 Vik는 처음엔 그렇다고 답했지만, 독자 피드백을 받고 확인해보니 이는 다른 레이저 회사 Coherent에 대한 착각이었다고 정정했다 — Coherent는 실리콘카바이드 잉곳만 자체로 키우고 인듐인화물 웨이퍼는 사서 쓴다는 것이다. AAOI는 자체 잉곳 재배부터 전부 자체 생산한다고 재확인했다.
- 숨은 캐시카우 — 케이블TV. Vik는 AAOI가 원래 케이블TV 장비로 유명했던 회사이며, DOCSIS 4(케이블 인터넷 기술 표준) 전환 덕에 케이블TV 사업 매출이 전년 대비 3배 가까이 늘어 여전히 회사 매출의 절반을 차지한다고 밝혔다. 다만 코드커팅(cord-cutting, 유료방송 해지)이 이 사업에 영향을 줬는지는 두 사람 모두 "잘 모른다"고 인정했다.
- Amazon 워런트. Vik는 Amazon이 AAOI와 10년, 40억 달러 규모의 구매계약을 맺으며 워런트(warrant, 주식매입권)를 부여했다고 밝혔다. 발표 직후 주가는 45~50% 가까이 뛰었다고 전했다. Austin은 AI 스타트업이나 Rivian 같은 곳에도 Amazon이 비슷한 워런트를 줘 왔다며, 이런 워런트가 경고 신호가 아니라 흔한 관행이라고 설명했다.
- S&P500 편입. Vik는 이번 달 Lumentum과 Coherent가 S&P500에 편입된다는 점을 들어, 광학 부품이 이제 중요해졌다는 신호로 해석했다.
- EML 모트 의문. Vik는 AAOI가 수직계열화됐다고 해도 정작 핵심인 EML(전기흡수변조레이저, electro-absorption modulated laser) 칩의 품질이 Lumentum만큼 좋은지는 의문이라며, "아마 아닐 것"이라고 봤다 — 그렇지 않다면 다들 AAOI에서 레이저를 사갔을 것이라는 논리다.
- CPO 시대의 재평준화. Vik는 공동패키지광학(CPO, co-packaged optics) 시대가 오면 변조를 실리콘포토닉스 칩이 맡게 돼 EML 자체가 필요 없어지고, 300~400mW급 고출력 CW(연속파) 레이저만 있으면 되므로 Lumentum의 EML 우위가 사라지고 Coherent·AAOI 모두 CW 레이저를 만들 수 있어 경쟁이 평준화된다고 짚었다.
- 웨이퍼 크기 약점. Vik는 AAOI가 4인치 웨이퍼 라인에 머물러 있는 반면 경쟁사들은 6인치로 넘어가고 있어, Coherent가 6인치 CW 레이저를 완전 수율로 뽑아내면 AAOI의 원가 경쟁력이 밀릴 수 있다고 지적했다.
- 자동화 생산과 미국 내 생산. Vik는 AAOI의 10-K(미국 상장사 연차보고서)를 인용해 "상대적으로 더 자동화된 생산 공정" 덕분에 미국 내에서도 아시아 대비 10~15% 정도의 프리미엄만으로 생산할 수 있다고 설명했다. Austin은 이것이 미국 내 제조를 유지하려면 로보틱스·휴머노이드 자동화가 답이라는 더 큰 논의로 이어진다고 짚었다.
- 증설 계획과 매출. Vik는 AAOI의 2025년 매출이 4.55억 달러였고 2026년 예상 매출은 10억 달러를 넘는다며, 800기가 제품 생산능력을 2026년 말까지 9만 대에서(800기가+1.6테라 합산) 50만 대로 늘릴 계획이라고 전했다.
- 회의론도 있다. Vik는 Citrini Research(자막 표기는 "Cetrini Research")의 최근 글 "Let There Be Light"를 언급하며, 이 글이 AAOI가 이미 정점을 찍었다고 보는 회의적 시각을 담고 있다고 소개했다.
- 2017년의 데자뷔. Vik는 2017년에도 40기가에서 100기가로의 데이터센터 연결 전환 사이클을 타고 AAOI 주가가 12달러에서 105달러까지 오른 적이 있다며, 지금과 가격대까지 거의 같고 경영진도 같으며 "수직계열화" 서사도 같다고 짚었다. 당시 상위 2개 고객 집중도는 75%였는데 지금은 80%대로 오히려 더 높아졌고, 2017년의 핵심 고객도 이번처럼 Amazon이었다고 밝혔다.
- 붕괴의 기억. Vik는 그 뒤 한 분기 수요가 약해지면서 주가가 미끄러졌고 100기가 제품의 판매단가(ASP)가 무너졌으며, 수직계열화가 오히려 문제가 됐다고(자체 레이저 신뢰성 문제가 생기면 스스로 고쳐야 했다) 전했다. 정점 100달러대에서 2022년경 바닥 1.48달러까지, 거의 99% 떨어졌다고 밝혔다. 투자 조언이 아니라는 점도 못박았다.
- 이번엔 다르다는 반론. Austin은 2017년 사례는 단일 네트워킹 속도 전환 사이클에 불과했지만 지금의 AI 데이터센터 투자는 산업 전반에 걸친 여러 해짜리 구조적 붐이며, Amazon의 10년짜리 구매계약도 2017년에는 없던 안정 요인이라고 짚었다. 다만 "역사는 되풀이된다"며 과거를 살펴볼 필요는 있다고 두 사람 모두 동의했다.
- 마무리. 진행자들은 청취자에게 평점과 리뷰를 부탁하며, 유튜브 구독자가 1,000명을 넘었다고 알렸다.

## 숫자 (원문에 나온 것만)
- 700% — AAOI 주가 상승률(6개월간, 10달러대 → 100달러대)
- 40억 달러 — Amazon-AAOI 10년 구매계약 규모(워런트 부여)
- 45~50% — 계약 발표 후 AAOI 주가 급등률
- 4.55억 달러 — AAOI 2025년 매출
- 10억 달러 초과 — AAOI 2026년 예상 매출
- 9만 대 — AAOI 800기가 제품 현재 생산능력
- 50만 대 — 2026년 말 목표 생산능력(800기가+1.6테라 합산)
- 12달러 → 105달러 — 2017년 AAOI 주가 범위(40기가→100기가 전환기)
- 75% — 2017년 AAOI 상위 2개 고객 집중도
- 80%대 — 현재 AAOI 상위 2개 고객 집중도
- 100달러대 → 1.48달러 — 2022년경 AAOI 바닥 주가(정점서 거의 99% 하락)
- 10~15% — AAOI 미국 내 생산 프리미엄
- 4인치 — AAOI 웨이퍼 크기(경쟁사는 6인치)
- 300~400mW — CPO용 CW 레이저 요구 출력
- 800W — MTIA300 가속기 전력
- 초당 200GB — MTIA300 스케일아웃 대역폭
- 400~500GB — MTIA500 최대 HBM 용량
- 16노드 → 72노드 — 세대 간 스케일업 도메인 확대
- 컴퓨트 칩 1개 + 네트워크 칩 2개 — MTIA300 구성
- 4개 칩(300·400·450·500) — 신규 발표 라인업
- 2년 — 4개 칩 출시 목표 기간(6개월 주기)
- 2~3개월 — 반도체 팹·패키징 최소 사이클타임
- 100명 — Rivos 창업 초기 엔지니어 수
- 50명 — 이후 애플 출신 인맥으로 추가 채용한 인원
- 1,000명 — Semi Doped 유튜브 구독자 수(이번에 처음 돌파)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "No, we understand our workload very, very well. We're running at insane scale. We want it to be as fast as possible, but also as cheap as possible." — Austin. "아니요, 우리는 우리 워크로드를 아주, 아주 잘 알아요. 우리는 엄청난 규모로 돌리고 있고, 최대한 빠르면서도 최대한 싸게 만들고 싶은 거예요."
- "It's 800W accelerator, it's optimized for this particular shape of workload. It has very high 200 GB per second scale-out bandwidth." — Austin. "800W급 가속기이고, 이 특정한 모양의 워크로드에 맞춰 최적화됐어요. 초당 200GB라는 아주 높은 스케일아웃 대역폭을 갖고 있죠."
- "Nvidia shows up with $4 billion to Lumentum and Coherent. And then Lumentum and Coherent this month are going to get into the S&P 500. ... imagine making it into the S&P 500 as like a laser company or whatever. Like it's important. That's it." — Vik. "Nvidia가 Lumentum과 Coherent에 40억 달러를 들고 나타나요. 그리고 이번 달에 Lumentum과 Coherent가 S&P500에 편입되죠. ...레이저 회사가 S&P500에 들어간다는 걸 상상해보세요. 이건 중요하다는 뜻이에요. 그게 다예요."
- "You know the stock price that it hit at the bottom after this great crash out that happened from the 40 gig to 100 gig transition? It hit a dollar 48 cents. It was over $100. It lost almost 99% of all of it." — Vik. "40기가에서 100기가로 전환하면서 있었던 그 대붕괴 뒤에 바닥을 찍은 주가 아세요? 1달러 48센트를 찍었어요. 원래는 100달러가 넘었었죠. 거의 99%를 다 잃은 거예요."
- "Our relatively more automated production process for certain optical modules also allows us more freedom in locating our manufacturing operations in customer favorite geographic locations while maintaining relatively low labor costs." — AAOI 10-K, Vik가 인용. "일부 광모듈에 대한 상대적으로 더 자동화된 생산 공정 덕분에, 상대적으로 낮은 인건비를 유지하면서도 고객이 선호하는 지역에 생산 시설을 두는 데 더 큰 자유를 갖게 됩니다."
- "Really you may be vertically integrated but are your EML chips really good, or are they lagging? ... So, can they make a good enough EML?" — Vik. "정말로 수직계열화가 됐다고 해도, 그쪽 EML 칩이 진짜 좋은가요, 아니면 뒤처지나요? ...그래서, 이 회사가 충분히 좋은 EML을 만들 수 있을까요?"

## 주의
- 화자 태그가 전사에 없어("화자 바뀜마다 한 줄" 표시만 있음) 문맥으로 발화자를 추정했다. 특히 "제조사 확인"(Broadcom/Marvell 문답) 구간처럼 짧게 주고받는 대목은 어느 쪽이 어느 문장을 말했는지 전사만으로 완전히 특정하기 어려웠다.
- "SemiWiki podcast"(전사 원문) — 채널명은 실제로 "Semi Doped"이므로 자막 오인식으로 보고 본문에서는 다루지 않았다.
- "Vik Shaker"(전사 원문) → 사용자 지정에 따라 "Vik Sekar"로 통일.
- "Carey Brisky"(전사 원문, Nvidia) → Nvidia에서 에이전틱 AI 관련 행사에 자주 등장하는 인물명과 발음이 가까운 "Kari Briski"로 표기를 통일했으나, 소속 외 직함은 전사에 없어 적지 않았다.
- "Cetrini Research" → 잘 알려진 리서치 발행자 "Citrini Research"의 오인식으로 보고 통일했다.
- "Rivers"(전사 원문, 메타가 인수한 회사) → 애플 출신 창업자, 소송 이력, MTIA 초기 설계 지원이라는 정황이 2024년 메타가 인수한 RISC-V 스타트업 Rivos와 일치해 Rivos로 추정 표기했다. 전사만으로 100% 확정할 수는 없다.
- "Walden Investments" / "Walden Capital"(전사 원문에서도 이름이 흔들림) → Lip-Bu Tan이 몸담았던 벤처투자사로 알려진 "Walden International"로 추정 표기했다.
- "440 gig to 100 gig transition"(전사 원문) → 같은 회차 다른 대목("40 gig to 100-gig connectivity upgrades")과 맞춰 "40 gig"의 오기로 보고 정정했다.
- "Maddox"(HBM+SRAM 전략을 언급했다는 업체명) — 전사만으로는 어느 회사를 가리키는지 특정할 수 없어 표기를 그대로 두고 본문 사실 목록에는 포함하지 않았다.
- Mike Ello(Synopsys CRO), Roger Tebbet(Synopsys), Asim Datta(Microsoft)는 표준 표기를 별도로 확인할 방법이 없어 전사 표기를 그대로 썼다.
- Lattice(랭킹 모델)가 도는 하드웨어, SRAM 미탑재 이유, Meta의 SRAM 스타트업 인수 가능성 등은 Austin·Vik 모두 "잘 모르겠다", "추정이다"라고 스스로 선을 그은 대목이라 사실 목록에서도 그 유보를 그대로 남겼다.
