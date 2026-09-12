---
title: GPU 잔존가치를 미리 값 매기면 뉴클라우드의 파이낸싱 비용이 낮아진다
date: 2026-02-10
source: https://www.youtube.com/watch?v=I1eKrYsgt1k
speaker: Wayne Nelms
org: Ornn 최고기술책임자(CTO)
channel: Semi Doped
host: Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) / 게스트 [[Wayne Nelms]] (Ornn 최고기술책임자(CTO))
section: news
topic: GPU 선물시장 · 잔존가치 보험 · 파이낸싱 비용
gain: 컴퓨트·메모리에 매긴 선물가격이 스팟 가격 급등을 어떻게 헤지하는지, GPU 잔존가치를 미리 값 매겨 파는 상품이 뉴클라우드의 대출 금리를 어떻게 낮추는지, 그리고 감가상각을 직선이 아니라 처음 3년에 쏠린 곡선으로 봐야 하는 이유.
---

## 한 줄
Ornn 최고기술책임자 Wayne Nelms는 GPU 컴퓨트와 메모리를 표준 상품처럼 거래하는 선물(先物)거래소를 만들었다고 설명한다. 스팟 가격이 뛸 때 상한을 씌우는 선물, GPU가 몇 년 뒤 얼마에 팔릴지 미리 값을 매기는 잔존가치 상품, 그리고 그 확실성이 뉴클라우드의 대출 금리를 낮춘다는 논리를 진행자 Vik Sekar와 나눈다.

## 사실 — 절 순서대로
- 게스트 소개. Vik는 이번 회차를 단독으로 진행하며 Ornn 최고기술책임자 Wayne Nelms를 소개했다 — Ornn은 GPU 컴퓨트를 표준 상품(commodity)으로 거래하는 금융거래소이며, 컴퓨트를 위한 선물시장이자 최근에는 메모리까지 다룬다고 밝혔다.
- 창업 배경. Wayne은 2024년 12월 MIT를 한 학기 일찍 졸업했고 수학·컴퓨터과학을 전공했으며, 졸업 후 뉴욕 Susquehanna International Group(SIG)에서 주식옵션 퀀트 트레이더로 일했다.
- 창업 계기. 그 무렵 비트코인 채굴업체들이 GPU 서비스업으로 사업모델을 바꾸며 주가가 급등하는 것을 보고 반도체·컴퓨트 시장을 조사하기 시작했다고 Wayne이 말했다. CoreWeave가 대표 사례로 언급됐다.
- 공동창업자. MIT에서 4년간 알고 지낸 친구 Kush Bubaria(현 Ornn CEO, 벤처·스타트업 배경)에게 상의했고, 두 사람은 사모펀드에서 일하던 지인으로부터 "데이터센터 딜을 검토하는데 위험을 어떻게 재야 할지 모르겠다"는 이야기를 들은 것이 창업 계기가 됐다고 Wayne이 전했다.
- 문제의식. Wayne은 이 일화에서 나온 물음 — "컴퓨트의 가치를 어떻게 매길 것인가" — 가 Ornn의 출발점이라고 정리했다. 본인의 금융 배경과 Kush의 벤처 배경을 합쳐 이 문제를 풀려 했다고 말했다.
- 시장의 현주소. Wayne은 컴퓨트의 금융화·상품화가 아직 초기 단계라며, SF Compute 같은 오프테이크(offtake) 표준화 업체나 지역·제공사·칩종별로 가격을 추적하는 Ornn 같은 업체가 있지만, 실제로 "거래"할 수 없다면 — 즉 그 숫자로 운영비를 헤지할 수 없다면 — 가치는 크지 않다고 봤다.
- Ornn의 상품 구조. Wayne은 데이터센터·콜로케이션·뉴클라우드 쪽과, 반대편의 컴퓨트 구매자(연구소·대학·병원) 양쪽 모두 Ornn 플랫폼에서 포지션을 잡아 운영비를 헤지할 수 있다고 설명했다.
- 헤지 예시(구매자). Wayne은 예시로, 장기계약은 있지만 추론 수요가 들쭉날쭉한 연구소가 스팟시장에서 대량 매수하면 가격이 오를 수 있는데, Ornn에서 현금결제형 선물(future)을 사면 실제 GPU 시간은 받지 않지만 인덱스가 오를 때 그 선물에서 이익이 나 지불액에 상한을 씌우는 효과가 난다고 설명했다.
- 헤지 예시(판매자). 반대로 데이터센터 쪽은 선물을 팔아 판매가에 하한을 둘 수 있다고 Wayne이 덧붙였다 — 석유·가스·전력 시장에서 이미 쓰이는 것과 같은 구조이며 금융에서는 이를 "칼라(collar)"라고 부른다고 설명했다.
- 스팟 가격 사례. Vik가 가격대를 묻자 Wayne은 H100 SXM 기준으로 오늘 기준 마켓플레이스 가격이 시간당 약 1.70~1.80달러, CoreWeave·Lambda·Crusoe·Nebius 같은 네오클라우드급은 3~4달러대, AWS·GCP 같은 하이퍼스케일러는 5~7달러대라고 밝혔다.
- 왜 마켓플레이스만 추적하나. Wayne은 하이퍼스케일러 가격은 분기에 한두 번만 바뀌어 일간 시장의 진짜 움직임을 반영하지 못한다고 보고, Ornn은 더 역동적인 마켓플레이스 가격만 인덱스로 삼는다고 설명했다.
- 지역별 표준화. Vik가 지역·제공사마다 가격이 다른데 어떻게 표준화하냐고 묻자, Wayne은 전력시장의 "허브" 개념을 끌어와 — 전력이 GPU 구동의 큰 원가 요소이므로 지역별 전력가 차이가 컴퓨트 가격에도 반영된다고 보고, 미국 안에서 특정 지역의 컴퓨트만 추적해 헤지를 더 구체적으로 만든다고 답했다.
- 선물의 작동 방식. Wayne은 예시로 2026년 2월물 선물을 오늘 2달러에 살 수 있다면, 2월 한 달간 인덱스가 21달러, 22달러, 최대 25달러까지 오르내리더라도(가정) 매수자는 2달러에 고정한 값으로 노출된다고 설명했다.
- 가격 결정 요인. Wayne은 순전히 수요와 공급이라며, 특정 달에 몇 명이 H100 시간을 공급하는지와 연구·훈련·추론 수요가 얼마인지가 가격을 정한다고 말했다. 그는 공급이 제약된 자원에는 역사적으로 금융시장이 뒤따랐다는 논리로 컴퓨트의 금융화가 필연적이라고 주장했다.
- 메모리로 확장. Wayne은 최근 Ornn이 DRAM·DDR5·DDR4·SRAM에 대한 메모리 선물을 출시했다고 밝혔다 — Architect Financial의 Brett Harrison과 함께 architect 플랫폼에서 내놨으며, 메모리 가격이 급등하는 상황에서 미래 수요에 대한 시각을 지금 거래할 수 있게 한다고 설명했다.
- Architect 파트너십. Wayne은 Architect 파트너십 이전 Ornn 자체 플랫폼에서는 매수자·매도자가 일대일로 맞물리는 스왑(swap)만 취급했는데, Architect의 퍼페추얼(perpetual) 거래소에서는 주식처럼 매일 가격에 노출되고, 큰 매도자 하나를 여러 소규모 매수자와 다대다로 매칭할 수 있어 시장이 더 진짜 시장처럼 작동한다고 설명했다.
- H100 감가 전망. Vik가 시간이 지나면 H100 컴퓨트가 저렴해지는 게 맞냐고 묻자, Wayne은 대체로 그렇다고 보면서도(largely agree), Ornn이 1년 반가량 추적한 A100 스팟 가격은 최근 몇 달간 오히려 안정적이거나 상승했다며 H100도 비슷한 경로를 밟을 수 있다고 말했다 — 관건은 구세대 칩에 대한 향후 추론 수요라고 덧붙였다.
- 유효수명 대 전성기 수명. Vik가 GPU 감가상각 기간(5년이냐 2년이냐)을 둘러싼 논쟁과 Michael Burry의 서브스택 글을 언급하자, Wayne은 "유효수명"과 "전성기 수명"을 구분해야 한다고 답했다 — A100 사례에서 보듯 특정 연차가 지났다고 GPU가 곧바로 고철이 되는 게 아니라 항상 잔존가치가 있다는 것이다.
- 전성기 수명 추정치. Wayne은 H100·B200·루빈(Rubin)의 전성기 수명이 통념상 5년이라 해도 자신은 2~3년에 더 가깝다고 보며, 유효수명은 5~10년까지 이어질 수 있다고 말했다.
- 감가상각 곡선. Wayne은 데이터센터 수익성 모델에서 흔히 쓰는 정액(직선)감가 가정을 "순진한" 가정이라 지적하며, 실제로는 가치 대부분이 처음 3년 사이에 빠지고 남은 5~7년은 비교적 평평하고 안정적이라고 자신의 트레이딩 배경을 근거로 설명했다.
- 잔존가치 상품. Wayne은 이 시점에 Ornn이 준비 중인 새 상품 — GPU 잔존가치 상품을 소개했다. 예시로 72랙 규모 B300 클러스터를 4년 테이크오어페이(take-or-pay) 계약으로 임대한 뉴클라우드가, 계약 만료 시 세입자가 재계약하지 않을 경우(더 나은 칩이 나왔을 때) 그 하드웨어를 되팔 수 있도록 4년 뒤 가격을 오늘 미리 매겨준다고 설명했다.
- 슈퍼카 비유. Vik가 이를 "쇼룸을 나서는 순간 값이 급락하지만 0으로 가지는 않는 슈퍼카"에 비유하자 Wayne은 대체로 맞는 비유(roughly correct)라고 동의했다.
- 가격 범위 밖의 것들. Wayne은 스위치·네트워킹은 값을 매기지 않고 GPU·HPC 하드웨어 본체만 값을 매긴다고 밝혔고, 4년 뒤 이 칩들이 지리적으로 어디로 향할지(남미·동유럽·아프리카 등 신흥시장) 자신도 관심 있게 지켜보는 영역이라고 덧붙였다.
- 전력은 값에 안 넣는다. Vik가 전력은 어떻게 값을 매기냐고 묻자, Wayne은 전력은 입지마다 달라(site-specific) 하드웨어 값을 매길 때 전력은 넣지 않는다고 답했다 — 다만 추론 중심 시장에서 토큰당 비용이 전력가격에 크게 좌우된다는 점은 인정했다.
- 투명한 가격의 수혜자. Wayne은 이 인덱스로 가장 득을 보는 쪽은 컴퓨트 구매자, 특히 병원·소규모 연구소·취미로 컴퓨트를 쓰는 사람들처럼 필요 이상의 성능에 시간당 8달러 같은 값을 과다 지불하고 있을 수 있는 소규모 사용자라고 말했다.
- 추론용 하드웨어 폐기 위험. Vik가 SRAM 기반 추론이나 Nvidia의 컨텍스트 메모리 스토리지(플래시 기반) 등장으로 구세대 훈련용 GPU가 추론에도 못 쓰이게 될 위험을 묻자, Wayne은 그런 "노후화 위험(obsolescence risk)"을 가격에 반영한다며 이는 확실히 가능성 있는 일(certainly a possibility)이라고 인정했다.
- 잔존가치 보장 범위. Wayne은 Ornn이 보통 잔존가치의 15~30% 구간을 보장한다고 밝혔다 — 예를 들어 칩 한 개를 3만 달러에 샀다면 8천~1만 달러어치의 잔존가치를 보장하는 식이며, 이는 시장의 "꼬리(tail)" 부분을 커버하는 것이라고 설명했다.
- 훈련 대 추론의 역전 가능성. Wayne은 구세대 칩이 추론에도 아예 못 쓰이고 신흥시장의 훈련용으로만 쓰일 가능성도 인정하며(I will agree with you however), 향후 수요의 상당 부분이 거기서 나올 것으로 본다고 말했다. Vik는 상시 가동되는 에이전트형 추론 수요가 늘면서 오히려 추론이 훈련보다 더 많은 최신 하드웨어를 필요로 하는 상황이 올 수 있다고 자신의 해석을 덧붙였다.
- 데이터센터 건설에 미치는 영향. Wayne은 선물시장 덕분에 여러 해 앞선 월별 H100 시간당 가격을 볼 수 있게 되면, 데이터센터 사업자가 칩종·입지 선택 이전에 몇 년 치 수익성을 미리 계산할 수 있다고 설명했다. 과거에는 사업자에게 "내년 가격은 얼마냐"고 물으면 근거 없는 숫자만 돌아왔다고 지적했다.
- 파이낸싱 비용 하락 논리. Wayne은 잔존가치 상품이 있으면 데이터센터가 대출 기관(신용펀드 등)에 "세입자가 재계약하지 않아도 4년 뒤 이 하드웨어를 다른 곳에 팔 수 있다"고 말할 수 있게 되고, 그 확실성이 위험을 낮춰 금리를 낮춘다고 설명했다 — 상위권 뉴클라우드의 이익률이 작은 이유가 바로 매년 칩당 지불하는 파이낸싱 비용이 크기 때문이라고 덧붙였다.
- 10년 뒤를 돌아보면. Wayne은 지금의 GPU·메모리 붐을 10년 뒤 돌아보면, 데이터센터들이 수요를 뒷받침할 숫자 없이 거의 직감과 희망만으로 지어졌다는 사실이 이상하게 느껴질 것이라며, Ornn이 그 수요를 계량화하는 첫걸음이 되길 바란다고 말했다.
- 마무리. Vik는 평소 이 팟캐스트에서 기술적인 이야기를 주로 다루는데 이번 회차는 금융·비즈니스 쪽이었다며, 평소 비즈니스 쪽을 잘 다루는 공동진행자 Austin이 이번 회차에는 함께하지 않았다고 언급하고 마무리했다.

## 숫자 (원문에 나온 것만)
- 2024년 12월 — Wayne이 MIT를 한 학기 일찍 졸업한 시점
- 4년 — Wayne과 Kush Bubaria가 MIT에서 알고 지낸 기간
- $1.70~$1.80/시간 — H100 SXM 마켓플레이스 스팟 가격(발언 시점 기준)
- $3~$4/시간 — CoreWeave·Lambda·Crusoe·Nebius 등 네오클라우드급 H100 가격대
- $5~$7/시간 — AWS·GCP 등 하이퍼스케일러 H100 가격대
- $2 — 2026년 2월물 컴퓨트 선물을 지금 사는 예시 가격
- $21~$25 — 2월 한 달간 인덱스가 오르내렸다고 가정한 예시 값(실제 시세 아님)
- 1년 반 — Ornn이 H100·A100 스팟 가격을 인덱스로 추적해 온 기간
- 5년 — GPU "전성기 수명"에 대한 통념
- 2~3년 — Wayne이 보는 실제 전성기 수명
- 5~10년 — Wayne이 보는 GPU 유효수명 범위
- 3년 — 가치 대부분이 소진된다고 본 초기 구간
- 5~7년 — 그 이후 가치가 비교적 안정적으로 유지된다고 본 구간
- 72랙 — 잔존가치 상품 설명에 쓰인 B300 클러스터 예시 규모
- 4년 — 그 예시에서 든 테이크오어페이 계약 기간
- 15~30% — Ornn이 잔존가치 상품에서 보장하는 잔존가치 비율
- $30,000 — 예시로 든 칩 한 개의 구입가
- $8,000~$10,000 — 그 칩 잔존가치 중 Ornn이 보장하는 금액
- $8/GPU시간 — 소규모·취미 사용자가 과다 지불할 수 있다고 언급된 예시 가격

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "Financing costs are super expensive — it's what's keeping a lot of the top Neoclouds' profit margins very small, because they're paying these huge costs per chip every year. So by saying that there's a person willing to buy this hardware in four years, it's certainty — and with certainty there's less risk, and with less risk you get charged less." — Wayne Nelms. "파이낸싱 비용은 정말 비싸요. 그게 상위권 뉴클라우드들의 이익률을 작게 만드는 이유죠, 해마다 칩 한 개당 이런 어마어마한 비용을 치르고 있으니까요. 그러니까 4년 뒤에 이 하드웨어를 사줄 사람이 있다고 말할 수 있다는 건 확실성이에요. 확실성이 있으면 위험이 줄고, 위험이 줄면 금리를 덜 물게 되죠."
- "What we're doing is effectively putting a price cap on any compute that you would be buying in the future." — Wayne Nelms. "저희가 하는 일은 사실상, 앞으로 사게 될 컴퓨트에 가격 상한을 씌우는 거예요."
- "There's a difference between useful life of a GPU and the prime life of a GPU... I think the prime life of an H100, or a B200, or a Rubin — I think five years could be reasonable, [but] I think it's probably closer to two or three years." — Wayne Nelms. "GPU의 '유효수명'과 '전성기 수명'은 달라요… H100이나 B200, 루빈의 전성기 수명은 5년도 그럴듯하다고들 하는데, 저는 2~3년에 더 가깝다고 봐요."
- "What is reality is that a lot of the value is lost across the first three years and then the remaining five, six, seven years are fairly flat or fairly stable." — Wayne Nelms. "실제로는 가치의 대부분이 처음 3년 사이에 빠지고, 남은 5~7년은 꽤 평평하게, 안정적으로 유지된다고 봐요."
- "We're usually covering between 15 to 30% of the residual value — if you bought, let's say, one chip for $30,000, we're protecting around 8 to 10 thousand dollars of the residual value." — Wayne Nelms. "저희는 보통 잔존가치의 15~30% 정도를 보장해요. 예를 들어 칩 한 개를 3만 달러에 샀다면, 그중 8천~1만 달러어치의 잔존가치를 지켜드리는 거죠."
- "We'll realize how insane it was for these data centers to be built almost based on intuition or hope — right, like, oh, I just hope that there will be more compute demand." — Wayne Nelms. "이 데이터센터들이 거의 직감이나 희망에 기대서 지어졌다는 게 얼마나 말이 안 되는 일이었는지 깨닫게 될 거예요 — '컴퓨트 수요가 더 늘어나길 바랄 뿐'이라는 식으로요."

## 주의
- 게스트 회사명은 자막에 "ORD"·"OR"·"Orin"·"orange"·"onai.com" 등으로 제각각 받아적혔다 — 이 노트는 영상 제목에 적힌 회사명 "Ornn"만 확정 표기로 쓰고 본문 어디에도 다른 표기를 쓰지 않았다.
- 진행자는 도입부에서 자신을 "Vicram from Vick's newsletter"라고 소개하는 것으로 자막에 남아 있다(자막 오인식으로 보인다) — 이 노트는 지시받은 표기 그대로 Vik Sekar로 통일했다.
- Ornn CEO로 언급된 인물명은 자막에 "Kush Bubaria"로 남아 있으나 정확한 철자는 확인되지 않았다. 이 인물은 진행자도 게스트도 아니라서 사실 절에 자막 표기 그대로만 적었다.
- Wayne의 X(트위터) 계정은 자막에 "Wayne_nelms with a Z"로만 언급되고 실제 계정명 표기는 확인할 수 없어 본문에 옮기지 않았다.
- 이 회차는 Vik Sekar 단독 진행이며 공동진행자 Austin Lyons는 참여하지 않았다(마무리에서 Vik가 "my other co-host Austin handles the business side really well"이라고 직접 언급) — 다만 frontmatter people 표기는 지시받은 고정 꼴("진행 Austin Lyons · Vik Sekar")을 그대로 따랐다.
- Wayne이 든 "2달러"·"21~25달러" 등 선물가·인덱스 값은 실제 시세가 아니라 "let's say(예를 들어)"로 시작한 가상의 설명용 예시다.
- 비트코인 채굴에서 GPU 서비스로 전환한 회사로 자막에 남은 "iron and terolf"는 정확히 어느 회사(추정: IREN·TeraWulf)를 가리키는지 자막만으로 확정할 수 없어 본문에서는 회사명을 특정하지 않았다.
