---
title: 메타 광고 추천 시스템은 GPU와 다른 실리콘(MTIA)을 요구했고, 이제 LLM이 그 하드웨어별 커널을 직접 짠다
date: 2026-04-20
source: https://www.youtube.com/watch?v=5dWovJ4YHTY
speaker: Matt Steiner
org: Meta
channel: Semi Doped
host: Austin Lyons
people: 진행 [[Austin Lyons]] (Semi Doped) / 게스트 [[Matt Steiner]] (Meta 수익화 인프라·랭킹·AI 파운데이션 부문 VP)
section: compute
topic: 광고 추천 시스템 · 추론 실리콘 · LLM 커널 자동화
gain: 메타 광고 랭킹이 CPU에서 GPU 코-디자인으로, 다시 메모리 대 컴퓨트 비율이 다른 커스텀 칩(MTIA)으로 옮겨간 이유, 그리고 LLM이 하드웨어별 커널을 직접 써서 그 전환 비용을 낮추는 방식.
---

## 한 줄
메타의 광고 추천 인프라를 총괄하는 Matt Steiner가 광고 시스템의 두 단계(검색 — Andromeda, 랭킹 — Lattice)와 그 아래를 받치는 실리콘의 변천사를 설명한다. CPU에서 Nvidia와 co-design한 GPU로, 다시 추천 시스템 특유의 메모리·컴퓨트 비율 때문에 커스텀 칩 MTIA로 넘어간 과정과, LLM이 하드웨어별 커널을 직접 써 주는 최근 기법(AlphaEvolve/AlphaKernel)까지 짚는다.

## 사실 — 절 순서대로
- 소개. 진행자는 Matt Steiner를 Meta의 수익화 인프라·랭킹·AI 파운데이션 부문 VP로 소개했다.
- 광고 시스템의 큰 그림. Matt는 광고주가 목표(사이트 방문·장바구니 담기·구매 등)를 지정하면, 메타가 각 사용자별로 「이 사람에게 보여줄 수 있는 광고」 목록을 미리 만들어 저장해 둔다고 설명했다.
- 두 단계 구조. 사용자가 로그인하면 요청이 인덱싱 시스템에 도착해 그 사용자에게 보여줄 수 있는 모든 광고를 가져오는 「검색(retrieval)」과, 그중 전환 확률이 높은 순서로 정렬하는 「랭킹(ranking)」 두 단계로 이어진다고 밝혔다.
- Andromeda. 검색 단계에서 쓰는 시스템의 이름은 Andromeda이며, Nvidia와 함께 GPU를 넣은 커스텀 하드웨어 스큐(skew, 특정 용도에 맞춘 하드웨어 구성)를 설계하고 그에 맞는 개인화 모델을 co-design했다고 Matt가 말했다.
- Lattice. 랭킹 단계에는 원래 목적별로 여러 모델이 있었는데, 이를 Lattice라는 기술로 단일 모델에 통합하는 작업을 해 왔다고 설명했다 — 사용자 관심사 정보를 여러 모델에 중복 저장하지 않아 메모리를 아끼고, 서브넷 연산을 한 번만 해 컴퓨트도 아끼며, 데이터가 다양해질수록 예측 성능도 좋아진다는 세 가지 이유를 들었다.
- GEM. Lattice보다 더 나아간 단계로, 메타의 광고 데이터를 최대한 많이 학습시킨 파운데이션 모델 GEM(generative ads recommendation model)을 만들었다고 밝혔다. 다만 GEM 자체는 너무 커서 그대로 서빙하기 어려워, 작은 모델로 지식을 증류(distillation)하는 과정을 거친다고 설명했다.
- 적응형 랭킹 모델(adaptive ranking model). 사용자마다 상호작용 이력의 길이가 다른데, 이력이 긴 「파워 유저」일수록 더 많은 컴퓨트를 써서 평가하는 모델을 새로 만들었다고 밝혔다 — 지연 예산(약 1초)이 고정된 상태에서 이력이 길수록 컴퓨트를 더 쓰는 방식이라고 설명했다.
- 규모. 메타 전체 서비스의 일간 활성 사용자(DAU)가 30억 명을 넘는다고 확인했다.
- 하드웨어 변천사. Matt는 예전에는 검색과 랭킹 모두 CPU에서 돌았으나, 이후 소형·중형·대형 CPU, 커스텀 ASIC, GPU, 더 강력한 GPU와 ASIC 순으로 컴퓨트를 늘려 온 「긴 행군」이었다고 말했다.
- Grace Hopper 코-디자인. 진행자가 Nvidia Grace Hopper와의 하드웨어·소프트웨어 co-design 과정을 묻자, Matt는 메타가 목표 컴퓨트량과 지연 예산을 제시하면 하드웨어 파트너가 가능한 구성을 제안하는 방식이라고 설명했다. 검색 문제는 컴퓨트보다 메모리(특히 고대역폭 메모리 채널)에 더 좌우돼, 그에 맞춰 메모리 비중이 높은 스큐로 설계했다고 밝혔다.
- MTIA로 이어진 이유. 진행자가 MTIA(Meta Training and Inference Accelerator, 메타 자체 학습·추론 가속기)로 넘어간 배경을 묻자, Matt는 광고 추천 시스템이 LLM과 다른 특성을 갖는다고 설명했다. LLM은 「병렬로 처리해도 되는(embarrassingly parallel)」 문제인 반면, 추천 시스템은 예제마다 사용자별 개인화 정보(취향 블롭)를 함께 실어야 해 데이터 패킷이 커지고, 그만큼 네트워크·메모리 대 컴퓨트 비율이 GPU 표준 구성과 달라진다고 밝혔다. 그래서 일부 워크로드에는 다른 컴퓨트 대 메모리 비율을 가진 커스텀 스큐가 필요하다고 말했다.
- GEM 서빙 규모. 적응형 랭킹 모델은 GEM을 증류한 변형으로, 파라미터가 약 1조 개에 이르는 LLM급 규모이면서도 서브세컨드(1초 미만) 지연으로 평가된다고 Matt가 밝혔다.
- LLM이 쓰는 커널(AlphaEvolve/AlphaKernel). Matt는 메타가 최근 발표한 논문(AlphaEvolve 혹은 AlphaKernel로 소개)에서, LLM이 특정 모델과 특정 하드웨어 조합에 맞춘 성능 최적화 커널을 직접 써 준다고 설명했다. 예전에는 전문 엔지니어가 일일이 손으로 튜닝해야 했던 「모델 × 하드웨어」 조합별 최적화를, 이제는 훨씬 낮은 비용으로 대규모로 만들어낼 수 있게 됐다고 밝혔다.
- 재배치 효과. 이 덕분에 예전에는 특정 하드웨어에 맞춰 튜닝한 바이너리를 다른 하드웨어로 옮기는 비용이 커서 잘 하지 않았지만, 이제는 LLM에게 새 커널을 만들게 해 같은 바이너리를 여러 하드웨어에 더 적극적으로 재배치할 수 있게 됐다고 설명했다.
- 생성형 AI 조직과의 교류. Matt는 추천 시스템 조직과 생성형 AI(LLM) 조직이 모델 트레이너 최적화, 데이터센터 설계, 성능 튜닝 등에서 서로 긴밀히 협력하며 양쪽 다 혜택을 본다고 말했다.
- 향후 2년 전망. 앞으로도 데이터센터·컴퓨트·메모리·스토리지에 대규모로 투자해 학습과 추론 성능을 함께 끌어올리는 「엔드투엔드 최적화」가 핵심이라고 밝혔다. 특히 소프트웨어 엔지니어링 수요가 오히려 크게 늘었다고 말했다 — 예전에는 한정된 수의 하드웨어 최적화 커널만 만들 수 있었지만, 이제는 하드웨어 하나당 최적화 커널을 100배 더 많이 원하게 됐고, 이를 LLM이 만들고 전문 엔지니어는 그 결과를 감독하는 역할로 바뀌었다고 설명했다.
- 마무리 질문. 진행자가 빠르게 변하는 분야에서 어떻게 따라가느냐고 묻자, Matt는 LLM으로 논문을 요약시키고 전문 AI 연구자 팀의 정리에 의존한다고 답했다.

## 숫자 (원문에 나온 것만)
- 30억 명 이상 — 메타 전체 서비스의 일간 활성 사용자 수("More than 3 billion daily active users across Meta's properties worldwide")
- 약 1초 — 광고 요청 처리에 배정된 지연 예산("Let's call it roughly 1 second")
- 서브세컨드(1초 미만) — 적응형 랭킹 모델이 실제 평가되는 지연 수준
- 약 1조 개 — 적응형 랭킹 모델(GEM 증류 변형)의 파라미터 수
- 10년 — Matt가 언급한, 메타가 성능 최적화(하드웨어·네트워크·데이터센터·칩·모델·소프트웨어)에 깊이 투자해 온 최소 기간
- 100배 — LLM 덕분에 하드웨어 한 종류당 원하게 된 소프트웨어 최적화 커널 수의 증가 폭("now we want 100 times as many software optimization kernels for each piece of hardware")

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "The adaptive ranking model is a LLM scale and complexity recommender model for meta with roughly 1 trillion parameters in this inference time model. And it gets evaluated at sub-second latencies, which is a pretty kind of fun and interesting software and hardware challenge." — Matt Steiner. "적응형 랭킹 모델은 메타 기준으로 LLM급 규모와 복잡도를 가진 추천 모델이에요, 추론 시점 파라미터가 약 1조 개고요. 그런데 이게 서브세컨드로 평가돼요, 소프트웨어와 하드웨어 양쪽에서 꽤 재미있고 흥미로운 과제죠."
- "It's kind of like context. Like I want a big model and I want to give it a ton of context, but that's expensive and that takes time." — Austin Lyons. "일종의 컨텍스트 문제인 거죠. 큰 모델을 쓰면서 컨텍스트도 잔뜩 주고 싶은데, 그게 비싸고 시간도 걸리잖아요."
- "So the optimal skew for training hardware skew for training a recommender systems may be not the same as a GPU that is optimized for training large language models." — Matt Steiner. "그러니까 추천 시스템 학습에 최적인 하드웨어 스큐가, LLM 학습에 최적화된 GPU와 같지 않을 수 있는 거예요."
- "We recently put out a paper, I believe we called it Alpha Evolve or Alpha Kernel where machine learning model, a large language model, will write a custom performance optimized kernel for a particular binary or machine learning model and a particular hardware pair." — Matt Steiner. "최근에 저희가 논문을 하나 냈는데, AlphaEvolve인가 AlphaKernel이라고 불렀던 걸로 기억하는데요, LLM이 특정 바이너리나 모델과 특정 하드웨어 조합에 맞춘 성능 최적화 커널을 직접 써 주는 방식이에요."
- "The demand for custom software that is more performant than a generic abstraction layer has gone through the roof and every team at every layer is trying to do much better optimization to produce better results per dollar, better results per watt of power used in these data centers." — Matt Steiner. "범용 추상화 계층보다 성능이 좋은 맞춤형 소프트웨어에 대한 수요가 폭발적으로 늘었고, 모든 계층의 모든 팀이 데이터센터에서 쓰는 달러당·와트당 결과를 더 끌어올리려고 훨씬 더 나은 최적화를 시도하고 있어요."

## 주의
- 전사에 화자 표시가 없어, Matt가 "great to be here with you, Austin"이라고 부른 대목과 소개 흐름을 근거로 진행자를 Austin(Semi Doped 진행자 Austin Lyons로 추정), 게스트를 Matt Steiner로 나눠 읽었다 — 원문 자체에 이름 라벨은 없다.
- 마무리 인사에서 Matt가 "Thank you for having me, Allison."이라고 말하는 대목이 있는데, 앞서 진행자를 계속 "Austin"으로 부른 것과 어긋난다. 자동 전사 오류로 보이지만 확인할 방법이 없어 원문 그대로 두고 고치지 않았다.
- MTIA와 Broadcom 파트너십·로드맵은 진행자의 질문 속에서만 언급됐고, Matt의 답변은 그 배경(추천 시스템과 LLM의 워크로드 특성 차이)을 설명하는 데 그쳐 계약 규모나 구체적 로드맵 수치는 나오지 않았다.
- AlphaEvolve/AlphaKernel의 정확한 논문명은 Matt 본인도 "I believe we called it"이라고 확신 없이 말한 것이라, 원문 그대로 두 이름을 함께 적었다.
