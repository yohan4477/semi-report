---
title: Arm이 자체 CPU 칩을 파는 이유는 전력 효율이 아니라 코어 수 4배 주장이다
date: 2026-03-27
source: https://www.youtube.com/watch?v=Npi-TLWCz3o
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: compute
topic: Arm 첫 자체 CPU 실리콘 · 에이전틱 AI 코어 수 논쟁 · TurboQuant KV 캐시 압축
gain: Arm이 "CPU 개수"가 아니라 "코어 수"로 말했다는 구분, IP 라이선스·CSS·실리콘 판매의 마진 구조(5%·10%·50%) 비교, TurboQuant 압축이 메모리 수요를 줄이기보다 컨텍스트 길이를 늘리는 쪽으로 쓰인다는 논리.
---

## 한 줄
이번 회차는 글로벌파운드리(GlobalFoundries)가 타워세미컨덕터(Tower Semiconductor)에 낸 특허소송 속보로 문을 열고, 구글 리서치가 재조명한 KV 캐시 압축 기법 TurboQuant를 짚은 뒤, Austin이 다녀온 Arm Everywhere 행사에서 나온 Arm의 첫 자체 CPU 칩 발표—에이전틱 AI(agentic AI)에는 기가와트당 코어 수가 4배 필요하다는 주장—를 놓고 두 진행자가 코어 수·전력·소프트웨어 호환성 관점에서 엇갈리는 반응을 주고받는다.

## 사실 — 절 순서대로
- 속보 소개. Austin은 방송 시작 10분 전 휴대폰에 뜬 글로벌파운드리 보도자료를 소개하며 회차를 열었다 — 글로벌파운드리가 타워세미컨덕터를 상대로 특허침해 소송을 냈다는 내용이다.
- 소송 내용. 보도자료에 따르면 소송은 미국 국제무역위원회(ITC)와 텍사스 서부지방법원에 냈고, 스마트 모바일·자동차·항공우주·통신 인프라에 쓰이는 고성능 기술 관련 특허 11건의 침해를 주장했다.
- 첫 반응. 두 진행자는 처음에는 광학(optics)이나 레이저 관련 다툼일 것이라 짐작했다가, 두 회사가 공유하는 RFSOI(RF용 실리콘온인슐레이터 공정) 기술이 쟁점일 수 있다는 쪽으로 옮겨 갔다 — 다만 정확히 왜 다투는지는 "전혀 모른다"고 인정했다.
- 모바일 메모리 가격 언급. 한 진행자는 최근 메모리 가격 때문에 휴대폰이 잘 안 팔린다는 점을 거론하며 이것이 소송 쟁점 중 하나일 수 있다고 짐작했지만, 곧바로 "그냥 모르겠다"고 덧붙였다.
- 투자자 영향 추측. 두 진행자는 타워세미컨덕터가 최근 투자자들 사이에서 주가가 계속 오르던 종목이라는 점을 짚고, 소송 결과에 따라 밸류에이션(기업가치 평가) 모델을 다시 계산해야 할 수 있다고 말했다. 결국은 회사가 우회 설계를 찾아 재무적으로는 가벼운 "손목 때리기" 정도에 그칠 것이라는 추측을 내놓으면서도 "누가 잘못했는지도 아직 모른다"고 못 박았다. 방송 중 확인한 타워세미컨덕터 주가는 그 시점 기준 약 5% 하락한 상태였다.
- 화제 마무리. 두 진행자는 글로벌파운드리 CTO의 "실제 혁신에는 지름길이 없다"는 발언을 인용하며, 언젠가 특허 전략을 다루는 IP법 전문가 초청 에피소드를 만들자고 합의하고 화제를 넘겼다.
- TurboQuant로 전환. 새 추론 가속기나 알고리즘이 나올 때마다 HBM(고대역폭 메모리) 관련주가 가장 먼저 흔들린다는 패턴을 짚으며 화제를 옮겼다.
- 정의. Vik는 TurboQuant를 KV 캐시(key-value cache, 어텐션 계산 중 이전 토큰 정보를 계속 쌓아 두는 저장소) 압축 알고리즘이라고 정의했다. KV 캐시는 토큰이 생성될 때마다 커지고 빠르게 접근해야 해서 보통 HBM 같은 고속 메모리 계층에 두어야 한다고 설명했다.
- Vik의 자기 유보. Vik는 "나는 ML 연구자가 아니다"라며 TurboQuant에 대한 자신의 이해가 "듣기에 불안정하다(sketchy)"고 밝히고, 틀린 부분이 있으면 정정해 달라고 청취자에게 요청했다. 다만 관련 논문 여러 편을 직접 찾아 읽었다고 말했다.
- 논문 시점. Vik는 TurboQuant의 근거 논문이 실제로는 2025년 4월 아카이브(arXiv)에 올라와 1년 넘게 주목받지 못하던 것이며, 구글 리서치 블로그가 그림과 쉬운 설명으로 재포장해서야 투자자들의 눈에 든 것뿐이라고 짚었다.
- 성능 수치. Vik는 TurboQuant가 FP16(16비트 부동소수점) 기준 KV 캐시 크기를 6배 압축했고, H100 GPU에서 테스트했을 때 추론 속도를 8배 끌어올렸다고 전했다.
- 속도 원인. Austin은 압축이 왜 속도까지 높이는지 물었다 — 계산에 쓰는 비트 수가 줄어서인지, 불러오는 데이터가 줄어서인지 궁금해했고, Vik는 "둘 다"라고 답했다.
- 두 기법 결합. Vik는 TurboQuant가 2024년 나온 PolarQuant(극좌표 변환 기반 압축)와 "quantized Johnson-Lindenstrauss transform"의 약자인 QJL 두 기법을 결합한 것이라고 설명했다.
- 정규화 문제. Vik는 어텐션·피드포워드 연산 전에 숫자가 지나치게 커지는 것을 막으려면 매 단계 정규화(renormalization)가 필요하고, 이 과정이 메모리 부담을 늘린다고 설명했다.
- PolarQuant 원리. Vik는 KV 캐시 벡터에 무작위 행렬을 곱하는 사전처리로 값들 사이의 상대적 관계(반지름·각도)는 보존하면서 유난히 큰 값(outlier)을 데이터 전체에 고르게 편 뒤, 직교좌표를 극좌표(반지름 r·각도 theta)로 바꾼다고 설명했다.
- QJL 비트 축소. Vik는 이후 QJL 변환을 거치면 반지름은 단 1비트(+1 또는 -1)로, 각도는 몇 개 값으로 몰려(clustering) 2~3비트로 표현할 수 있게 되어, KV 캐시 벡터 하나를 3비트 정도로 나타낼 수 있다고 설명했다.
- Vik의 자기 평정. Vik는 설명을 마치며 "이쯤이면 청취자들이 다 졸았을 것"이라고 웃으며 인정했다.
- Austin의 PM 프레임. 제품관리자(PM) 경험을 빌려, KV 캐시가 50% 줄었다는 보고를 받으면 곧바로 컨텍스트를 100만 토큰에서 200만 토큰으로 늘려 달라고 요청했을 것이며, 실제로는 정확히 200만까지는 아니고 150만 토큰 정도로 타협했을 것이라는 가정을 들었다.
- 압축 트렌드 연결. Austin은 FP32→FP16→FP8→FP6→FP4로 이어지는 정밀도 압축 흐름을 짚으며 이런 압축이 결국 더 많은 가중치·컨텍스트를 다루게 해 준다고 말했고, 이런 혁신이 계속되면 오늘날 프론티어급 생성형 AI도 언젠가 로컬 기기에서 돌아갈 수 있으리라는 낙관을 덧붙였다.
- Vik의 응답. Vik는 이런 벡터 양자화(vector quantization) 방식이 성능 손실 없이 일부 작업을 클라이언트 기기·엣지 추론으로 옮길 여지를 만든다고 동의했고, 구글 리서치 블로그가 제시한 "건초더미에서 바늘 찾기(needle in a haystack)" 벤치마크에서 양호한 점수를 기록했다고 전했다 — 통상 양자화는 정보 손실을 부르지만 이 방식은 그렇지 않다는 점을 강조했다.
- DeepSeek 비교. Vik는 이전에도 GQA(grouped query attention)나 DeepSeek의 MLA(multi-headed latent attention) 같은 KV 캐시 축소 기법이 있었다며, "DeepSeek 모멘트"가 2025년 초였다고 기억했다("내가 맞다면"이라는 유보를 붙였다) — 그런데도 이후 HBM 수요는 줄지 않고 오히려 계속 늘었다고 짚었다.
- 결론. Vik는 TurboQuant 이전에도 비슷한 방식으로 4배 정도 압축한 연구들이 있었지만 구글 블로그에 오르기 전엔 주목받지 못했을 뿐이라고 말했다. Austin은 SRAM·HBM·DRAM·SSD로 이어지는 메모리 계층 구조 자체는 앞으로도 계속 필요할 것이라고 덧붙였다.
- Arm 행사 소개. Vik가 Austin에게 참석한 행사를 묻자, Austin은 행사명이 "Arm Anywhere"가 아니라 "Arm Everywhere"였다고 정정하며 샌프란시스코에서 열렸다고 밝혔다.
- 사업모델 전환. Austin은 Arm이 이 행사에서 IP 라이선스 회사에서 벗어나 처음으로 직접 실리콘(칩)을 만들어 팔겠다고 발표했다고 전했다.
- 발표 프레이밍. Austin은 Arm이 에이전틱 AI가 CPU 오케스트레이션(도구 호출·웹 탐색 등)에 새로운 부담을 준다는 논리를 폈다고 설명했다 — 헤드노드 CPU만으로는 부족해 GPU를 계속 먹여야 하는 자리 바로 옆에 CPU가 더 필요하다는 것이다.
- 코어 수 주장. Austin은 Arm이 "에이전틱 AI 이전에는 기가와트당 CPU 코어 3천만 개가 필요했지만, 에이전틱 AI 시대에는 기가와트당 1억2천만 개가 필요하다"—즉 같은 전력 안에서 코어 수가 4배 필요하다는 계산을 발표에서 제시했다고 전했다.
- x86→Arm 전환 관찰. Austin은 호퍼(Hopper) 세대 초기에는 헤드노드 CPU로 인텔 제온이나 AMD x86이 많이 쓰였지만, 다음 세대 Grace Blackwell부터는 대부분 Arm 기반으로 넘어갔다고 짚었다 — AI 워크로드 대부분이 이미 Arm 위에서 돈다는 것이다.
- 초기 고객. Austin은 Arm이 무대에 메타(Meta)와 오픈AI(OpenAI) 엔지니어를 초기 고객으로 세웠다고 전했다 — 메타 엔지니어(성이 Saab이라고 들렸다)는 예전엔 포팅(porting, 다른 아키텍처로 소프트웨어 이식)이 큰 걱정거리였지만 LLM 덕분에 이제는 훨씬 쉬워졌다고 말했다고 전했다.
- Vik의 반박 1. Vik는 에이전틱 AI CPU 아키텍처를 웹 시대 CPU 역할과 완전히 떼어 놓고 볼 수 없다고 주장했다 — 캐드언스(Cadence) 같은 EDA 툴이 맥 실리콘(M 시리즈)에서 잘 도는지 자신도 확실치 않다고 인정하면서도, 이런 틈새 툴 호환성 때문에 x86이 Arm보다 약간 앞서 있을 수 있다고 말했다.
- Vik의 반박 2. 다만 Vik는 소프트웨어 지원 문제 자체는 시간이 갈수록 덜 중요해지고 있다고 인정했고, Arm이 강조한 전력 효율(TCO) 논리는 받아들이지 않았다 — GPU 랙이 워낙 많은 전력을 태우는 데이터센터 안에서는 CPU 하나의 전력 효율 차이가 시스템 전체에 별 영향을 못 준다는 것이다.
- 코어 대 칩 구분. Vik는 Arm이 "CPU"가 아니라 "코어" 수로 말했다는 점이 중요하다고 짚으며, 자신이 이미 Substack에 이 코어 수 지표에 대해 썼다고 언급했다 — 메모리 도메인을 공유하면 지연(latency)이 생기기 때문에 에이전트마다 별도 코어(때로는 코어 두 개)가 필요하다는 논리다.
- 랙 사양. Austin은 Arm이 액체냉각 랙과 공기냉각 랙 두 종류를 함께 내놓았다고 전했다 — 액체냉각 랙은 OCP 더블와이드 규격으로 트레이 42개에 트레이당 CPU 8개, 총 코어 4만5천 개 규모였다고 밝혔다. Vik는 이를 직접 나눠 계산해 액체냉각 랙이 CPU 330개, 공기냉각 랙이 CPU 60개에 해당한다고 정리했다(칩 하나당 코어 136개인 Neoverse V3 기준).
- 비율 확대 추정. Vik는 자신이 이전 Substack 글에서 계산한 베라 루빈(Vera Rubin) 랙의 GPU 대 CPU 비율이 이미 1대1이었다고 언급했고, Arm의 "기가와트당 코어 4배" 주장이 맞다면 이 비율이 4대1까지 갈 수 있다고 추정했다 — 정확한 계산은 청취자가 직접 해 보라며 확정 짓지 않았다.
- 매출 구조. Austin은 Arm이 "10억 달러어치 CPU가 팔릴 때 IP 라이선스만 하면 5%(5천만 달러), CSS(컴퓨트 서브시스템, 미리 구현해 둔 코어 블록)까지 포함하면 10%(1억 달러), 반면 실리콘을 직접 팔면 50%(5억 달러)를 가져간다"는 도표를 보여줬다고 전했다 — 라이선스·CSS 마진은 98~99%에 이르는 순이익에 가깝다고 덧붙였다.
- 타이밍 유보. Austin은 Arm이 35년 역사 만에 첫 자체 CPU를 내놓는 시점이 수요가 폭발하는 최적의 시기이지만, 동시에 메모리 부족 때문에 고객들이 실제로 이 칩을 늘려 쓰기 어려운 시기라는 이중적 상황이라고 짚었다. Arm 스스로도 매출이 10억 달러 규모로 커지는 시점을 2028년으로 잡았다는 점에 "지금이 기회인데 왜 2028년이냐"고 아쉬움을 표했다. 이 칩은 이미 물량이 넘치는(oversubscribed) 3나노 공정으로 만들어져 확보 자체가 쉽지 않을 것이라고도 짚었다.
- AMD 비교. 한 진행자는 AMD의 "Venice Dense" CPU가 칩당 코어 256개·스레드 512개인 반면 이번 Arm AGI 칩은 코어 136개(Neoverse V3)뿐이고 멀티스레딩 기능이 있다는 언급은 없었다며, "있었다면 발표했을 텐데 못 봤다"는 추측을 덧붙였다.
- AMD·인텔에 촉구. Austin은 AMD가 고밀도·고코어수·전력효율을 앞세워 옛 서버 랙 10개를 1개로 줄일 수 있다고 말해 온 논리가 이번 에이전틱 AI 랙 이야기와 그대로 맞아떨어진다며, AMD·인텔도 나서서 자신들의 "에이전틱 AI 랙" 이야기를 해야 한다고 촉구했다.
- 마무리. 두 진행자는 약 55분 진행된 이번 회차를 마무리하며 Arm·x86·Nvidia CPU 쪽 전문가를 초청해 더 정교한 논의를 이어가고 싶다고 밝히고, 뉴스레터 구독을 독려했다.

## 숫자 (원문에 나온 것만)
- 특허 11건 — 글로벌파운드리가 타워세미컨덕터를 상대로 주장한 침해 특허 수
- 약 5% 하락 — 방송 중 확인한 타워세미컨덕터 주가
- 6배 — TurboQuant의 KV 캐시 압축률(FP16 대비)
- 8배 — H100 GPU에서 측정한 추론 속도 향상
- 2024년 — PolarQuant(TurboQuant의 첫 구성 기법) 발표 연도
- 2025년 4월 — TurboQuant 근거 논문이 arXiv에 올라온 시점
- 1비트 — QJL 변환 후 반지름을 표현하는 비트 수
- 2~3비트 — QJL 변환 후 각도를 표현하는 비트 수
- 3비트 — 최종적으로 KV 캐시 벡터 하나를 표현하는 데 쓰는 비트 수
- 100만→150만 토큰 — Austin이 든 가상의 컨텍스트 확장 사례(50% KV 캐시 축소 가정)
- 3천만 → 1억2천만 코어(기가와트당) — Arm이 발표에서 제시한 에이전틱 AI 이전·이후 CPU 코어 수 비교(4배)
- 136개 — Arm AGI CPU 칩 하나에 들어간 Neoverse V3 코어 수
- 45,000개 — 액체냉각 랙의 총 코어 수(42트레이 × 트레이당 CPU 8개)
- 330개 — Vik가 환산한 액체냉각 랙의 CPU(칩) 수
- 60개 — 공기냉각 랙의 CPU(칩) 수
- 1대1 — Vik의 이전 Substack 계산에 따른 베라 루빈 랙의 GPU 대 CPU 비율
- 4대1 — Arm의 코어 4배 주장이 맞을 경우 Vik가 추정한 향후 비율(확정치 아님)
- 5% / 10% / 50% — Arm의 IP 라이선스·CSS·실리콘 직판 매출 마진 비교(10억 달러 매출 기준 각각 5천만·1억·5억 달러)
- 98~99% — Arm의 IP·CSS 라이선스 사업 순이익률
- 2028년 — Arm이 CPU 매출 10억 달러 이상 규모를 목표로 잡은 시점
- 3나노 — 이번 Arm AGI CPU의 제조 공정
- 256코어 / 512스레드 — AMD Venice Dense CPU 사양(비교 대상)
- 35년 — Arm이 첫 자체 CPU를 내놓기까지 걸린 회사 역사
- 약 55분 — 이번 회차 진행 시간

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "I'm no ML researcher, okay? So my understanding of this is sketchy, too. I might say stuff that isn't entirely accurate. Please correct me if I'm wrong." — Vik. "저는 ML 연구자가 아니에요. 그래서 이해도 좀 불안정해요. 정확하지 않은 얘기를 할 수도 있으니, 틀리면 정정해 주세요."
- "There is no shortcut to real innovation. Companies that attempt to extract value from patented process technologies without authorization or investment undermine fair competition and the integrity of the semiconductor ecosystem." — 글로벌파운드리 CTO(보도자료 인용). "진짜 혁신에는 지름길이 없습니다. 허락이나 투자 없이 특허 받은 공정 기술에서 가치를 빼내려는 회사는 공정한 경쟁과 반도체 생태계의 건전성을 해칩니다."
- "I reduced our KV cache size by 50%. Instead of 1 million token context, can I have 2 million tokens of context?" — Austin. "우리 KV 캐시를 50% 줄였어요. 그러면 100만 토큰 컨텍스트 대신 200만 토큰 컨텍스트를 가질 수 있을까요?"
- "He didn't say CPUs, he said cores. It's very important because the number of cores in a CPU is a very important metric for agentic AI CPUs." — Vik. "그는 CPU라고 안 하고 코어라고 했어요. 이게 중요한 이유는, CPU 안의 코어 수가 에이전틱 AI CPU에서 아주 중요한 지표라서예요."
- "When you are building a data center with so many GPU racks which are burning power like insane amounts, the CPU efficient or not doesn't really play a major role in the context of the system." — Vik. "GPU 랙이 워낙 많은 전력을 태우는 데이터센터를 짓는 상황에서는, CPU가 효율적인지 아닌지가 시스템 전체 맥락에서는 큰 역할을 못 해요."
- "It's a fantastic time in history to bring out your first CPU. When demand is off the charts and there's not enough supply." — Austin. "첫 CPU를 내놓기에는 역사적으로 기막힌 시점이에요. 수요는 하늘을 찌르는데 공급은 부족한 때니까요."

## 주의
- 화자 표시가 전사에 거의 없어(원문 frontmatter는 화자 바뀜마다 줄이 나뉜다고 되어 있으나 이 렌더링에는 그 구분이 남아 있지 않다), 특히 글로벌파운드리·타워세미컨덕터 소송을 다루는 초반부는 발화 경계가 불분명하다. 이 절의 화자 배정(Austin/Vik 구분)은 문맥(자기소개·직접 호칭 등)으로 추정한 것이며 100% 확정은 아니다.
- 자막이 진행자 이름을 잘못 받아 적었다 — "Austin Lines" → Austin Lyons, "Vic Shayker" → Vik Sekar, "Chip Strat" → Chipstrat 로 통일했다.
- 행사 이름도 전사에는 "Arm Anywhere"로 여러 번 나오지만, Austin이 발화 중 스스로 "Arm Everywhere"로 정정했다 — 정정된 이름을 썼다.
- 메타 엔지니어의 이름은 전사에서도 "Nick Saab maybe... Paul Saab maybe"로 화자 자신이 확실치 않다고 밝혔다 — 성(Saab)만 확인되고 이름은 불확실해 지어내지 않았다.
- "The Rubin Meta signed a $27 million billion dollar deal with Nebius" 구절은 "million billion"이 겹쳐 있어 자막 오인식으로 보인다. 정확한 금액을 확정할 수 없어 본문에는 넣지 않았다.
- Arm의 코어 수 주장 부분에서 "40 million yeah it's like 30 million to 120 million. 30 million to 100."처럼 숫자가 겹쳐 나오는 구간이 있다 — 앞뒤 맥락(4배, 기가와트당)과 일관되는 "3천만 → 1억2천만"을 대표값으로 썼고, "30 million to 100" 부분은 자막 오인식으로 보고 제외했다.
- RFSOI(RF용 실리콘온인슐레이터)라는 풀이는 본문 판단을 돕기 위해 붙인 통상적 업계 용어 설명이며, 전사에는 약어("RFSOI technology")만 나온다.
