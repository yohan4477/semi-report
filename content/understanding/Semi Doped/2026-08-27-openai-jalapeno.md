---
title: 설계를 아홉 달에 끝낸 추론 칩 — 오픈AI 할라페뇨
date: 2026-08-27
source: https://daily.semidoped.com/p/new-episode-openais-jalapeno-feeling
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 Austin Lyons · Vik Sekar (Semi Doped 공동 진행) / 발표 Richard Ho (전 구글 TPU 팀, 발표를 이끔) · Ravi (칩 아키텍트) · Chris (소프트웨어 코디자인)
section: compute
topic: 추론 칩 · HBM 활용률 · 스케일업 도메인
gain: RTL 부터 테이프아웃까지 아홉 달이라는 일정이 무엇을 뜻하는지, HBM 대역폭을 다 쓰지 못하는 구조적 이유, 스케일업 도메인을 128칩과 2,048칩으로 나눠 보는 셈.
---

## 한 줄
OpenAI가 Hot Chips에서 발표한 지 12시간도 안 돼 녹음한 회차로, 자체 추론(inference) 칩 Jalapeño의 설계 슬라이드를 처음부터 끝까지 훑는다. 진행자 두 사람(Austin, Vik)이 SemiAnalysis 벤치마크 기사를 화면에 띄워 놓고 사용자 경험·에너지 효율 중심 설계 철학, NUMA(비균일 메모리 접근) 방식 로컬 HBM, ESUN 스케일업 네트워킹, 9개월 설계 주기를 차례로 짚는다.

## 사실 — 절 순서대로
- 녹음 시점. Vik는 OpenAI가 Hot Chips에서 Jalapeño를 발표한 지 12시간도 안 돼 이 회차를 녹음한다고 밝혔고, 녹음 뒤 4시간 안에 해외 출장 비행기를 타야 한다고 말했다.
- 이름 우연. 두 사람은 콘퍼런스 자원봉사자·주최측이 빨간 할라피뇨가 그려진 노란 셔츠를 입고 있었다며, 칩 이름 Jalapeño와 콘퍼런스 이름 Hot Chips의 연결이 우연인지 의도인지 궁금해했다.
- 발표팀. 슬라이드를 발표한 OpenAI 팀은 Richard Ho(전 구글 TPU팀 출신), Ravi(칩 아키텍트), Chris(소프트웨어 공동설계 담당) 세 명이다.
- 설계 기준 둘. OpenAI 팀은 설계 시 우선하는 지표로 (1) 사용자 경험 — 첫 토큰까지 걸리는 시간이 아니라 마지막 토큰까지 걸리는 종단간(end-to-end) 지연 — 과 (2) 요청당 에너지(energy per request) 둘을 꼽았다.
- 파레토 곡선. 두 지표는 상충관계이므로 단일 수치 대신 항상 파레토 프론티어 곡선으로 보여주겠다고 밝혔다.
- 설계 주체 차이. Austin은 상업 실리콘 벤더는 통상 TCO(총소유비용)를 우선 내세우는데, 모델랩인 OpenAI는 최종 AI 사용자를 위해 설계한다는 점이 특이하다고 지적했다.
- 젠슨 황 인용. Vik는 엔비디아 CEO 젠슨 황이 예전에 "칩을 더 싸게 만들려고 아키텍처를 고르는 건 나쁜 설계 결정"이라는 취지로 말한 적이 있다고 전했다.
- tokens per joule. Vik는 tokens per joule(=초당·와트당 토큰 수)을 궁극적인 소유비용 지표로 제시했다.
- 벤치마크 파트너. OpenAI는 SemiAnalysis의 "Inference X" 벤치마크로 Jalapeño를 테스트했다고 슬라이드에서 밝혔고, 파워 정규화된 공개 비교라고 강조했다.
- Inference X를 고른 이유. 여러 오픈소스 모델(소형~대형)로 테스트할 수 있고, 시스템 전체의 최종 사용자 경험을 반영한다는 점을 꼽았다.
- 컨텍스트 길이 지적. Austin은 벤치마크의 입출력 컨텍스트 길이가 비교적 작았다는(예: 8K 입력/1K 출력) 이후 피드백이 있었다고 언급했다. 100만 토큰급 긴 컨텍스트에서의 성능은 아직 공개되지 않았다.
- Agentic 워크로드 미검증. Vik는 SemiAnalysis 기사에 따르면 OpenAI가 아직 Jalapeño로 agentic 워크로드는 테스트하지 않았고, 별도의 "AgentX" 플랫폼으로 벤치마크할 예정이라고 전했다.
- 범용성 시연. OpenAI는 Jalapeño가 자사 모델 전용이 아니라 GPT-OSS(소형 모델)부터 Kimi K2.5(다른 형태의 모델)까지 구동한다고 보여줬다. SemiAnalysis는 이 칩에서 Doom을 실행했다고도 언급했다.
- 판매 가능성 논쟁. Vik는 다른 회사 모델까지 도는 범용성을 굳이 보여준 이유가 궁금하다며, 자사 모델에만 초co-design하면 Cerebras급 성능까지 낼 수 있다는 반론을 폈다. Austin은 파운드리·IDM 비유(인텔이 초기엔 자사 전용으로 팹을 쓰다가 비용 분담을 위해 개방한 사례), 뉴클라우드를 통한 엔터프라이즈 임대, AWS Trainium처럼 자사 모델을 서비스로 싸게 제공하는 방식 등 여러 시나리오를 제시했다.
- 회한 요인(regret factor). Ravi는 설계 시 한계비용(기능 하나 더 넣는 비용)과 기회비용(수요가 있는데 기능이 없어 놓치는 비용)을 함께 고려하며, 기회비용이 대체로 더 크다고 말했다.
- 가장 어려운 결정. 청중 질문에 Ravi는 "무엇을 뺄지" 정하는 게 가장 어려운 결정이었다고 답했다.
- 로드맵. Richard는 이미 2세대(Gen 2) 칩이 테이프아웃에 근접했고 3세대(Gen 3)도 구상 중이라고 밝혔다.
- 설계 주기. 첫 RTL 작성부터 테이프아웃까지 약 9개월 걸렸다 — 통상 2~3년 걸리는 일을 크게 단축했다고 두 사람은 짚었다.
- 첫 칩치고 이례적. Austin은 회사의 첫 칩은 보통 버리는 셈치는(proof of concept) 경우가 많은데, OpenAI는 1호 칩부터 강하게 나왔다고 평했다.
- DeepSeek R1 비교. SemiAnalysis 슬라이드에서 Jalapeño(보라색 선)는 DeepSeek R1(6710억 파라미터)을 구동할 때 새로운 파레토 프론티어를 형성했다 — 동일 interactivity에서 처리량이 더 높고 interactivity 한계도 더 멀리 뻗었다.
- 세대 차이 지적. 다만 Jalapeño는 HBM4를, 비교 대상인 Blackwell·MI355는 HBM3E를 쓰기 때문에, 공정한 비교는 Vera Rubin·Helios와 되어야 한다는 반박이 있었다.
- SRAM 영역 진입. GPT-OSS(1200억 파라미터) 같은 소형 모델을 구동할 때 Jalapeño는 사용자당 초당 1,000토큰 이상 — 통상 GPU가 못 가는 "SRAM 영역"에 도달했다고 설명했다.
- 전력 효율. Jalapeño는 700W TDP 칩으로, Blackwell GB200(약 1,200W)보다 소비전력이 훨씬 낮다.
- 파트너 공개. 로드맵 슬라이드 하단에 Broadcom과 Celestica가 파트너로 언급됐다. SemiAnalysis는 Celestica가 시스템 레벨(OEM 격) 설계 파트너로 추정된다고 봤다고 Austin이 전했다.
- 스펙 추정. CPU는 x86 계열로 (AMD) Turin급으로 추정되고, 공정노드는 TSMC N3(N3P 또는 N3E 변형)로, HBM은 삼성 HBM4로 추정된다 — 다만 삼성 HBM4가 SK하이닉스 대비 핀당 속도가 더 빠를 수 있다는 부분은 전적으로 추측이라고 Vik가 못박았다.
- 스케일업 규모. 128개의 Jalapeño 칩이 하나의 대규모 스케일업 도메인을 이루며 Broadcom Tomahawk 6 스위치로 칩당 초당 600기가비트로 통신한다. 더 넓은 도메인은 최대 2,048개 칩까지 확장되며 초당 200기가비트 인터커넥트를 쓴다 — 이는 ESUN(Broadcom이 주도한 스케일업 네트워킹 규격, UALink와는 다른 진영)이다.
- 랙 규모 추정. Austin은 128개는 한 랙, 2,048개는 약 16개 랙에 해당하는 2단계(two-tier) 스케일업 구조로 추정했다.
- 토폴로지 이름. Vik는 이 구조를 "half flattened two-level Clos topology"라 부른다고 언급하며 정확한 의미는 아직 소화 중이라고 말했다.
- HBM 활용률 문제. Vik는 128개 칩의 HBM4 총 대역폭을 합치면 초당 약 1페타바이트에 달하며, FP4에서 1조 파라미터 모델(약 0.5테라바이트 데이터)이라면 이론상 HBM만으로 초당 약 2,000토큰이 나와야 하는데 실제로는 그만큼 나오지 않는다고 계산했다 — 이 때문에 Cerebras·Groq 같은 SRAM 기반 칩이 필요하다고 설명했다.
- 핀 전송률. Nvidia는 핀당 전송률을 초당 10기가비트에서 16기가비트로 올리고 있고, Hot Chips 메모리 세션 차트에서 HBM5는 초당 약 23~24기가비트에 이를 것으로 나왔다고 Vik가 전했다.
- 지연 원인. Chris는 연산에 필요한 데이터가 필요한 시점에 레지스터에 도착하지 않는("operands arrive late") 문제와, HBM을 이웃 가속기들과 공유하며 생기는 컨텐션(contention) 문제를 지적했다.
- NUMA 해법. 해법으로 가속기마다 전용 로컬 HBM 슬라이스와 전용 저지연 버스를 두는 NUMA(비균일 메모리 접근) 스타일 아키텍처를 채택했다. Vik는 NUMA가 원래 멀티코어 CPU에서 코어별로 메모리 일부를 전담시켜 컨텐션을 줄이는 개념이라고 설명했다.
- 균형 설계 원칙. OpenAI는 워크로드별로 prefill과 draft/verify(추측 디코딩) 비율이 계속 바뀌기 때문에 GPU처럼 prefill 전담·decode 전담 칩으로 나누면 유휴 가속기가 생긴다고 지적하고, 대신 모든 칩을 균형 잡힌 단일 칩으로 만들어 필요 없는 부분은 전원을 끄는(게이팅) 방식을 택했다고 밝혔다.
- 추측 디코딩 설명. Vik는 작은 draft 모델이 한 번에 여러 토큰(예: 8개)을 생성하면 검증(verify) 단계가 그중 맞는 토큰을 골라내는 방식이라고 설명했다.
- AI 도구로 초기 RTL. 발표 중 한 연사가 초기 RTL은 GPT-3급 모델로 작성됐고, 이후 모델이 좋아지면서 더 나은 모델을 썼다고 밝혔다고 Vik가 전했다.
- 비교 대상 스타트업. Austin은 d-Matrix, Reiner Pope 같은 구글 출신 팀을 가진 AI ASIC 스타트업과 대비했다 — 이들은 인력·노하우는 있었지만 AI 도구는 처음부터 갖추지 못했다고 언급했다.
- Anthropic 칩 부재. Vik는 Anthropic은 아직 자체 칩이 없다는 점을 지적하며 궁금하다고 말했다.

## 숫자 (원문에 나온 것만)
- 9개월 — 첫 RTL 작성부터 테이프아웃까지 걸린 기간
- DeepSeek R1: 671,000,000,000(6710억) 파라미터
- GPT-OSS: 120,000,000,000(1200억) 파라미터
- 1,000토큰/초/사용자 이상 — GPT-OSS 120B 구동 시 Jalapeño의 처리량
- 700W — Jalapeño TDP
- 약 1,200W — Blackwell GB200 TDP(비교치)
- 128개 — 하나의 대규모 스케일업 도메인을 이루는 Jalapeño 칩 수
- 초당 600기가비트 — Broadcom Tomahawk 6 스위치의 칩당 통신 속도
- 2,048개 — 더 넓은 스케일업 도메인의 최대 Jalapeño 칩 수
- 초당 200기가비트 — 2,048개 도메인의 인터커넥트 속도
- 약 16개 랙 — Austin의 추정치(2,048÷128)
- 초당 약 1페타바이트 — 128개 칩 HBM4 총 대역폭(Vik 계산)
- 약 0.5테라바이트 — FP4에서 1조 파라미터 모델의 데이터 크기(Vik의 예시 계산)
- 초당 약 2,000토큰 — 위 조건에서 이론상 HBM만으로 낼 수 있는 처리량(실제로는 못 미침, Vik 계산)
- 초당 약 4,000토큰 — Cerebras가 SRAM으로 낼 수 있다고 언급된 수치(Vik, 별도 논의라고 못박음)
- 초당 10~16기가비트 — 현재 HBM 핀당 전송률(Nvidia가 끌어올리는 중)
- 초당 약 23~24기가비트 — HBM5 예상 핀당 전송률(Hot Chips 메모리 세션 차트, Vik 전언)
- 약 1억 달러 — 테이프아웃·초기 램프업 비용에 대한 Austin의 어림 발언("talking $100 million or whatever", 확정치 아님)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "We're recording this less than 12 hours since OpenAI actually announced Jalapeño at Hot Chips." — Vik. "OpenAI가 Hot Chips에서 실제로 Jalapeño를 발표한 지 12시간도 안 돼 이걸 녹음하고 있어요."
- "there's a market for tokens, it wants them fast, it wants them cheap, and making things go fast gives us joy." — Austin이 전한 Ravi의 발언. "토큰 시장이 있고, 그 시장은 빠른 걸 원하고 싼 걸 원하죠. 그리고 빠르게 만드는 일은 우리에게 기쁨을 줍니다."
- "because ultimately the show flops don't matter. It's how many flops you actually deliver." — Austin이 전한 Chris의 발언. "결국 겉으로 보여주는 플롭스는 중요하지 않습니다. 실제로 전달하는 플롭스가 몇인지가 중요하죠."
- "dark silicon is cheaper than idle accelerators" — OpenAI 발표 슬라이드 문구. "쓰지 않는(dark) 실리콘이 놀고 있는 가속기보다 싸다."
- "So Jalapeño's benefit really seems to be the token throughput per watt. It is actually very energy efficient in generating this kind of performance." — Vik. "그러니까 Jalapeño의 강점은 결국 와트당 토큰 처리량인 것 같아요. 이 정도 성능을 내는데 실제로 에너지 효율이 아주 좋습니다."
- "It is about nine months from first RTL to tape out, which is an incredibly short period of time." — Vik. "첫 RTL부터 테이프아웃까지 약 9개월인데, 이건 정말 말도 안 되게 짧은 기간이에요."

## 주의
- Jalapeño의 정확한 스펙(CPU 종류, 공정 노드, HBM 공급사)은 진행자들이 반복해서 "추측(speculative)"이라고 명시한 부분이다 — OpenAI가 공식 확인한 수치가 아니다.
- "약 1억 달러" 테이프아웃 비용, "10억 코어 수요"(2편이 아니라 이 편의 논의 범위 밖) 등 host 발언 중 명시적으로 어림값·사고실험으로 표현된 숫자는 확정 수치와 구분해 표기했다.
- 전사 텍스트는 Substack 페이지에서 자동 추출한 것으로 화자 태그("Vik:", "Austin:")는 원문 그대로이며, 문장부호 오인식은 없었다.
