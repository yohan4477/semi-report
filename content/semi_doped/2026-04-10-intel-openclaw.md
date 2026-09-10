---
title: 에이전트 토큰 비용이 오르자 사람은 싼 모델로 옮기고 추론 칩은 메모리를 섞어 칩을 줄인다
date: 2026-04-10
source: https://www.youtube.com/watch?v=rFf8ABolyi0
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: compute
topic: 에이전틱 AI 토큰 비용 · 추론 칩 메모리 구조 · 인텔 주가
gain: 구독형 요금이 에이전트 상시 구동에 안 맞아 쪼개지자 개인은 저가 모델·로컬 추론으로 옮기고, 추론 칩 쪽에서는 SRAM만 쓰는 그록(Groq) 구조보다 SRAM·HBM·D램을 섞는 SambaNova식 구조가 훨씬 적은 칩 수로 같은 디코드를 해낸다는 것이 이번 회차의 핵심 대비다.
---

## 한 줄
Anthropic이 구독제 요금으로 에이전트 하니스 "오픈클로(OpenClaw)"를 상시 구동하는 것을 막자, Vik가 저가 모델·로컬 추론으로 옮겨간 경험담을 계기로 두 진행자가 에이전틱 AI의 토큰 비용 구조를 짚는다. 이어 인텔의 주가 반등과 인텔-SambaNova의 새 추론 아키텍처를 다루며, 그록(Groq)의 SRAM 전용 구조가 확장에서 갖는 한계를 대비시킨다.

## 사실 — 절 순서대로
- 진행자 소개. Austin은 자신을 Chipstrat의 Austin Lyons로, Vik를 Vik's Newsletter의 Vik Sekar로 소개했다(자막은 "Aston Lyons"·"Vic Shaker"로 잘못 받아 적었다).
- Anthropic 정책 변경. Vik는 4월 8일 Anthropic이 이메일로 구독제(Claude Max 등) 계정을 오픈클로 같은 에이전틱 하니스에 쓰지 못하게 막고, API 크레딧을 따로 사라고 통지했다고 전했다.
- 비용 체감. Vik는 오픈클로를 API 요금으로 돌려보니 5~7달러가 5분 만에 소진됐다고 말했다.
- Austin의 재구성. Austin은 Vik의 이야기를 구독료가 실은 정해진 토큰량을 원가보다 싸게 보조해주는 구조였는데, 에이전트가 쉬지 않고 도는 쓰임에는 그 보조가 안 맞았을 것이라고 풀어 설명했다.
- Fireworks AI 대안. Vik는 Fireworks AI의 "파이어패스(Fire Pass)"라는 상품으로 주당 7달러를 내면 Kimi K2.5 Turbo 모델을 사실상 무제한 토큰으로 쓸 수 있다고 소개했다 — Sonnet보다 약간 못한 수준이라고 평가했다.
- 드리밍 모드. Vik는 오픈클로 최신 버전에 추가된 "드리밍 모드(dreaming mode)"를 켰다고 밝혔다 — 하루 동안의 지시·경험을 마크다운 파일에 기록하고, "드림 상태"에서 이를 파싱해 더 긴 기억으로 별도 마크다운 메모리 파일에 저장하는 기능이다.
- 로컬 모델 검토. Vik는 로컬 실행을 위해 Gemma 3 1B(약 30GB 램 필요)와 더 작은 Gemma 4 계열의 E4B·E2B 모델을 검토했다고 말했다 — 자원 소모에 비해 지능이 높아지는 추세라고 평가했다.
- OpenRouter 실험. Vik는 OpenRouter에서 20~25달러 크레딧을 사서 Xiaomi MiMo V2 Pro 모델을 써봤다고 밝혔다 — OpenRouter 기술 부문 사용량 1위 모델이며, Opus급 지능을 주장하는 오픈소스 모델이라고 소개했다.
- Austin의 반문. Austin은 그런 오픈소스 모델이 실제로 Opus 수준의 프런티어 지능인지 물었고, Vik는 "아니다"라고 답했다.
- 로컬 에이전트 활용례. Vik는 자신의 가상 비서가 Discord로 후속 이메일·할 일 목록을 알려주는 등의 작업을 주당 7달러 수준의 비용으로 처리해준다고 설명했다.
- 에이전트 컴퓨터 비유. Austin은 5천 달러짜리 "에이전트 컴퓨터"를 사는 것과 주당 7달러 무제한 토큰을 비교하며, 자산을 소유한다는 만족감과 중고 판매로 원금을 회수할 가능성을 짚었다.
- GPU 재판매 경험담. Austin은 크립토 붐 전 300달러에 산 그래픽카드를 1년 뒤 530달러에 되팔았던 경험을 들며, 메모리 가격이 계속 오르는 지금 "토큰 생성기"를 사두는 것도 비슷한 투자일 수 있다고 말했다.
- MatX 인터뷰 소개. Austin은 최근 Reiner Pope(MatX 공동창업자)와 진행한 인터뷰를 언급했다 — Pope와 공동창업자는 LLM에 특화된 칩을 만들겠다며 ChatGPT 출시 일주일 전 구글을 떠났다고 전했다.
- 인텔 시가총액. Austin은 인텔 시가총액이 3000억 달러를 넘었다는 소식을 전했다 — 6개월 전보다 3배, 이번 4월에만 50% 올랐고 주가는 약 30달러에서 60달러가 됐다고 말했다.
- 테라팹 추정 재확인. Austin은 지난 회차에서 자신이 예측했던 "일론 머스크의 테라팹(Terafab) 프로젝트에 인텔이 칩을 만들어줄 수 있다"는 시나리오가 다른 업계 보도로도 뒷받침되고 있다고 말했다 — 단, 인텔의 발표 자체는 세부 내용이 적었다고 밝혔다.
- 구글-인텔 제온 계약. Austin은 인텔과 구글이 제온(Xeon) CPU에 대한 다년 계약을 새로 맺었다는 소식(전날 발표)을 전했다.
- 실망 지점. Austin은 처음에는 이 계약이 AI 랙용 CPU 수요와 직결된 것으로 기대했지만, 실제로는 2년 전 발표된 구글의 C4·N4 머신(에메랄드 래피즈 기반 제온)과 같은 구세대 인텔 7 CPU에 대한 것으로 보인다고 정정했다 — 인텔이 구세대 CPU 공급 부족을 겪었던 배경이 있다고 덧붙였다.
- IPU 설명. Vik는 인텔과 공동설계 중인 IPU(인프라 처리 장치)를 스토리지·네트워킹·보안 기능을 호스트 CPU에서 떼어내는 별도 칩이라고 설명했다 — AWS Nitro나 DPU와 비슷한 개념이라고 Austin이 덧붙였다.
- ARM 대 x86. Vik는 데이터센터 CPU의 90%가 ARM으로 넘어갈 것이라는 주장에 동의하지 않는다며, 구글의 Axion 같은 전력효율형 ARM 칩과 제온 같은 고성능 x86 칩이 서로 다른 워크로드에 병행 배치될 것이라고 말했다.
- Mohamed Awad 인용. Austin은 ARM 행사에서 만난 Mohamed Awad(ARM)와의 대화를 전했다 — LLM 덕분에 ARM으로 포팅하기는 쉬워졌지만, 기업 고객이 오래된 시스템을 옮기는 일은 기술 난도와 무관하게 여전히 큰 결정이라는 지적이었다.
- 인텔-SambaNova 발표. Vik는 인텔과 SambaNova가 제온 CPU와 SambaNova RDU(재구성 가능 데이터 유닛)를 결합한 새로운 이종(heterogeneous) 추론 아키텍처를 발표했다고 전했다 — 디코드를 RDU가 맡는 구조로, "Vera CPU + Groq LPU" 조합에 비유했다.
- RDU 구조. Vik는 SambaNova RDU가 SRAM뿐 아니라 HBM·D램까지 함께 쓰며, 데이터가 각 메모리 계층에서 오는 시점을 미리 정해두는(결정론적) 데이터 경로 설계가 핵심이라고 설명했다.
- 칩 수 비교. Vik는 이 구조라면 256개 칩으로 그록(Groq) LPU 수천 개가 하는 디코드 작업을 해낼 수 있다고 말했다 — 그록은 SRAM만 쓰기 때문에 메모리를 늘리려면 칩(연산)도 함께 늘려야 한다는 이유를 들었다.
- 그록 구조의 한계. Austin은 그록의 VLIW(초장명령어, very large instruction word) 방식이 클록 단위까지 결정론적이지만, SRAM에 물리적으로 묶여 있어 HBM이나 D램을 붙이기 어렵다는 점이 확장의 걸림돌("아킬레스건")이라고 짚었다.
- 경쟁 구도 전망. Austin은 Groq·Cerebras·SambaNova·Etched·MatX·Talos 등 추론 칩 스타트업이 여럿이지만, 제조 비용이 워낙 커서 손익분기를 넘기려면 일정 물량이 필요해 결국 몇몇 조합만 남을 것이라고 전망했다.
- 니치 응용. Vik는 Talos 같은 "하드코딩된 LLM" 칩이 서버 시장에서 밀려도 어린이 장난감처럼 저비용·저지능이 허용되는 소비자 응용으로 옮겨갈 수 있다고 말했다.
- 마무리. 두 진행자는 인텔 소식과 오픈클로 경험담을 정리하며 다음 회차에서 드리밍 모드 결과를 확인하자고 말하고 방송을 마쳤다.

## 숫자 (원문에 나온 것만)
- 월 200달러 — Vik가 오픈클로에 쓰던 Claude Max 구독료
- 5~7달러/5분 — Vik가 API 요금으로 오픈클로를 돌렸을 때 소진된 금액
- 4월 8일 — Anthropic이 구독제-에이전트 하니스 겸용을 막는다고 통지한 날짜
- 주당 7달러(월 28달러) — Fireworks AI 파이어패스 요금
- 20~25달러 — Vik가 OpenRouter에서 산 크레딧
- 약 30GB — Gemma 3 1B 모델 로컬 구동에 필요한 램
- 5천~1만 달러 — Vik가 어림잡은 로컬 추론용 Mac Mini(에이전트 컴퓨터) 가격
- 5년 — Vik가 가정한 그 기기의 수명
- 300달러 → 530달러 — Austin이 크립토 붐 전에 사서 되판 그래픽카드 가격
- 3000억 달러 — 인텔 시가총액(회차 당시)
- 3배 — 6개월 전 대비 인텔 시가총액 증가율
- 50% — 4월 한 달간 인텔 주가 상승률
- 30달러 → 60달러 — 인텔 주가(몇 주 전 대비)
- 256개 — SambaNova RDU 기반 구조로 그록급 디코드를 해내는 데 필요하다고 언급된 칩 수
- 수천 개 — 같은 작업에 그록(Groq) LPU가 필요로 하는 칩 수(Vik의 발언)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "Suddenly on April 8th, they sent an email saying like, 'Hey, if you're using your subscription plan to use agentic harnesses like open claw, you can't do that anymore. You need to go and buy API credits like the rest of users or whatever.'" — Vik. "4월 8일 갑자기 이메일을 보내서, '이봐, 구독제 요금제로 오픈클로 같은 에이전틱 하니스를 쓰고 있다면 이제 그렇게 못 해. 다른 사용자들처럼 API 크레딧을 따로 사야 해'라고 하더라고요."
- "a Fireworks AI has this thing called like fire pass which allows you to use like $7 a week and it gives you basically unlimited tokens to uh use Kimiko 2.5 Turbo." — Vik. "Fireworks AI에 파이어패스라는 게 있는데, 주당 7달러를 내면 사실상 무제한 토큰으로 Kimi 2.5 Turbo를 쓸 수 있어요."
- "Like a 256 chips can do what Groq LPUs need thousands of chips to do because they just don't have memory." — Vik. "256개 칩으로 그록 LPU가 수천 개나 필요한 일을 해낼 수 있어요. 그록은 메모리가 그만큼 없으니까요."
- "it's relative inelasticity is its own Achilles' heel." — Austin. "그 구조가 상대적으로 잘 안 늘어난다는 게 그록 자신의 아킬레스건인 거죠."
- "Intel's market cap apparently crossed 300 billion, which is 3x up from about 6 months ago." — Austin. "인텔 시가총액이 3000억 달러를 넘었다는데, 6개월 전보다 3배가 된 거예요."

## 주의
- 자막 인명 오표기: "Aston Lyons"는 Austin Lyons, "Chip Strat"은 Chipstrat, "Vic Shaker"·"Vic's Newsletters"는 Vik Sekar·Vik's Newsletter의 오기로 보고 표준 표기로 통일했다.
- "Kimiko 2.5 Turbo"는 발음상 Kimi K2.5 Turbo(문샷 AI의 Kimi 계열 모델)의 오기로 보인다.
- 회차 뒤쪽에서 언급된 추론 칩 스타트업 목록 중 "Mad Max"는 같은 회차 앞부분에서 다룬 MatX(Reiner Pope 인터뷰의 그 회사)의 오기로 보인다.
- "테라팹(Terafab)" 프로젝트의 정확한 명칭·주체는 이 전사만으로는 확인되지 않는다 — 앞선 회차에서 다룬 내용을 다시 언급한 것이라 이번 전사에는 근거가 없다.
- SambaNova RDU의 정식 명칭은 통상 Reconfigurable Dataflow Unit으로 알려져 있으나, 전사에서는 "reconfigurable data units"라고만 언급했다 — 원문 표현을 그대로 남겼다.
- 전사는 유튜브 자막 기반이라 화자 태그가 없다 — 1인칭 표현·상대를 부르는 말("Vic, you...")·문맥으로 화자를 판정했다. 도입부(1번째 문단)는 이후 본편에서 그대로 반복되는 내용으로, 예고 성격의 발췌로 보인다.
