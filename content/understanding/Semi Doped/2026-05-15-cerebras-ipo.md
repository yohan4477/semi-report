---
title: 웨이퍼 한 장을 통째로 칩으로 쓰는 회사가 상장한다
date: 2026-05-15
source: https://daily.semidoped.com/p/cerebras-ipo
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
section: compute
topic: 웨이퍼 스케일 · SRAM 추론 · 상장
gain: SRAM 44기가바이트를 한 장에 얹은 칩의 스펙과 전력, 그리고 웨이퍼 스케일이라는 발상이 40년 전에 한 번 회사를 무너뜨린 적이 있다는 내력.
---

## 한 줄

Cerebras가 IPO(기업공개) 가격을 주당 185달러로 확정한 2026년 5월 14일 아침 녹음된 회차. 웨이퍼 스케일 엔진(WSE)의 구조·전력·냉각 방식, 1980년대 Trilogy Systems의 웨이퍼 스케일 실패담, OpenAI와의 토큰 판매 계약을 다뤘다.

## 사실 — 절 순서대로

- 녹음 시점. 2026년 5월 14일 아침, Cerebras IPO 가격 확정 당일에 녹음했다고 Austin이 밝힘.
- 공모 방식. 이베이(eBay) 경매식 입찰 — 투자자가 원하는 주식 수와 지불 의사가 있는 최고가를 제시하는 방식을 썼다고 Vik이 설명.
- 막판 참여 시도. Bloomberg 보도에 따르면 Arm과 Softbank가 막판(11th hour)에 참여를 시도했으나 매입에는 이르지 못했다고(이베이의 "스나이핑"에 빗대) 언급.
- 가격 형성 과정. 초기엔 135달러 예상 → 150~160달러 → 최종 185달러로 확정. 애초 목표 조달액은 35~40억 달러였는데, 그보다 약 15억 달러 많은 55억 달러를 조달했다고 Austin이 언급.
- Cerebras의 제품 정의. 통상 웨이퍼를 다이 단위로 잘라 개별 패키징하는 대신, 웨이퍼 전체를 하나의 칩으로 남겨 금속 배선으로 서로 연결하는 방식이 웨이퍼 스케일 엔진(WSE)이라고 설명.
- 규모 비교. WSE 하나가 Nvidia H100 약 60개 정도 크기이고, 84개의 레티클(reticle, 노광 1회당 찍히는 단위 영역)이 그리드 형태로 이어 붙어 있다고 설명.
- 결함 대응 구조. 웨이퍼는 완벽할 수 없어 항상 결함(수율 문제)이 있다는 전제 아래, Cerebras는 웨이퍼를 GPU 대비 1/100~1/20 크기의 아주 작은 processing core 단위로 쪼갠다고 설명.
- 코어 수와 가동률. 전체 코어 수는 약 100만 개(정확히는 970K 정도로 언급), 이 중 약 90만 개가 실제 가동 중이라고 설명.
- 결함 우회 방식. 결함이 있는 코어는 웨이퍼 상의 네트워킹 패브릭을 통해 우회 라우팅해 인접한 예비 코어로 연결을 넘긴다고 설명.
- 핵심 스펙. 이렇게 완성된 웨이퍼는 44GB의 온-웨이퍼 SRAM을 21페타바이트/초(PB/s) 대역폭으로 제공한다고 확인.
- 코어 구성 비율. Vik의 질문에 Austin이 각 컴퓨트 코어가 대략 실리콘 면적의 50%는 컴퓨트, 50%는 SRAM으로 배분돼 있다고 답함.
- 전력 규모. 웨이퍼 한 장이 약 23킬로와트(kW)를 소비하며, 1볼트(V) 공급 기준 수만 암페어의 전류가 필요하다고 설명. 84개 레티클은 NVL72(72칩 구성)보다 많은 칩 수에 해당한다고 비교.
- 전력 전달 방식. 웨이퍼 한쪽에서만 전류를 흘려보낼 수 없어, 웨이퍼 표면 수백 개 지점에서 수직으로 전력을 공급하는 특수 커넥터를 자체 개발했다고 설명.
- 냉각 방식. 마이크로 유체 채널로 웨이퍼 전체를 수직으로 흘러 냉각하는 "engine block"이라는 냉각 장치를 사용한다고 설명.
- 열팽창 문제. 웨이퍼가 발열로 약 0.1mm(십분의 1밀리미터) 팽창하는데, 실리콘 웨이퍼와 PCB(인쇄회로기판)의 열팽창 계수가 달라 커넥터가 어긋나는 문제가 생긴다고 설명. Cerebras가 이를 해결하기 위한 커스텀 소재를 특허로 보유하고 있다고 언급.
- 비용 관점. 이 접근은 비용 절감이 목적이 아니라고 Vik이 명확히 함 — 레티클 스티칭(reticle stitching) 자체가 TSMC와 10년 넘게 함께 풀어온 제조 난제라고 설명.
- 44GB 한계. Cerebras가 창업할 당시(ChatGPT 이전)는 44GB가 충분해 보였겠지만, 현재 LLM(대형언어모델) 시대엔 Llama 70B 같은 중형 모델도 이미 44GB를 넘는다고 지적.
- 다중 웨이퍼 병목. 모델이 44GB를 넘으면 여러 웨이퍼로 나눠야 하는데, 파워는 웨이퍼 표면 전체로 공급되는 반면 네트워킹은 웨이퍼 한쪽 끝으로만 나가고 온-웨이퍼 대역폭보다 훨씬 느리다고 설명.
- 병렬화 방식. 파이프라인 병렬화(레이어별로 웨이퍼를 나눔), 텐서 병렬화(행렬을 나눠 여러 웨이퍼에서 실행), 전문가 병렬화(MoE 방식으로 전문가를 웨이퍼별로 배치) 세 가지 방식이 거론됨.
- 포토닉 인터커넥트 언급. Austin이 SemiAnalysis의 최근 기사에서 Cerebras가 웨이퍼 스케일 광학 인터커넥트를 실험 중이라는 내용을 봤다며, 웨이퍼 위에 광학 웨이퍼를 하나 더 얹어 Z축 방향으로 정보를 라우팅하는 방식일 수 있다고 언급(직접 다 읽지는 못했다고 밝힘).
- Trilogy Systems 창업 배경. 1980년대 Gene Amdahl이 약 2억 3000만 달러(오늘날 가치로 약 10억 달러 상당)를 모아 2.5인치 웨이퍼 스케일 칩을 만들려 했다고 소개.
- Trilogy의 재난. 1982년 폭풍으로 3300만 달러 규모의 공장이 침수됐고, 배관이 녹슬면서 클린룸에 미세먼지가 유입돼 수율이 무너졌으며, 원인 파악에만 수개월이 걸려 그사이 자금을 소진했다고 설명.
- Trilogy의 Hail Mary IPO. 1983년 제품 없이 약 6000만 달러를 조달했으나, 초기 주당 12달러였던 주가가 이후 거의 0원 수준으로 폭락했다고 설명.
- 후속 비극. Amdahl이 롤스로이스를 사고로 파손했고, 위기가 한창일 때 재무 담당자 Clifford Madden이 뇌종양으로 사망했다고 언급. 회사는 구조조정 후 웨이퍼 스케일 사업을 포기하고 남은 자금으로 미니컴퓨터 스타트업을 인수했다고 설명.
- Amdahl의 발언(Vik이 재구성). "앞으로 100년은 이걸 해낼 수 없다"고 말했다고 Vik이 전함. 1989년 Amdahl이 사임했다고 언급.
- Trilogy부터 Cerebras까지의 시간. 시도 이후 약 40년 만에 Cerebras가 실제로 작동하는 웨이퍼 스케일 엔진을 만들어냈다고 정리.
- 사업 방향의 변천. Cerebras는 애초 슈퍼컴퓨팅용으로 구상됐다가, LLM 훈련 시대에 훈련(training)용으로 피벗했으나 CUDA 생태계의 장벽 때문에 훈련 시장에서 성공하지 못했고, 현재는 추론(inference), 특히 분리형(disaggregated) 추론의 디코드 단계에서 필요한 메모리 대역폭 수요에 부합해 다시 피벗했다고 설명.
- OpenAI 딜 구조. OpenAI는 Cerebras의 하드웨어를 사는 것이 아니라 토큰(연산 결과) 사용료를 지불하는 방식이며, Cerebras가 데이터센터 구축·운영·클라우드 서비스·토큰 제공을 전부 담당한다고 설명. 계약에는 워런트(warrant) 조건이 포함돼 있다고 언급(세부 수치는 본인 Substack에 별도로 썼다고 밝힘).
- NVIDIA-Groq 비교. NVIDIA가 Groq를 인수해 저지연 추론 솔루션을 확보했으며, Vik은 그 인수 가격이 비쌌다고 평가.
- 저지연 추론의 용처. 코딩(에이전틱 코딩), 금융 트레이딩, 실시간 음성 번역 등 프리미엄 토큰 비용을 감당할 수 있는 용도로 시장이 제한적이라는 논의.
- 경쟁사 언급. SambaNova, MatX(창업자 Reiner Pope), Taalas, Sohu, Tenstorrent, Etched, Fractile(전일 2억 2000만 달러 조달), d-Matrix 등이 SRAM 기반 추론 경쟁사로 거론됨.
- 마무리. Cerebras가 55억 달러를 확보해 채용을 확대할 수 있다는 언급으로 마무리.

## 숫자 (원문에 나온 것만)

- IPO 공모가: 주당 185달러
- 조달액: 55억 달러(Austin 추정)
- 초기 목표 조달액: 35~40억 달러 (실제보다 약 15억 달러 적은 규모)
- 가격 변동: 135달러 → 150~160달러 → 185달러(확정)
- 상장 초기 주가 상승폭: 거의 70%(소개문 표현)
- WSE 크기: Nvidia H100 약 60개 분량, 84개 레티클
- 코어 수: 약 100만 개 중 약 90만 개(970K 수준) 가동
- 컴퓨트 코어 구성: 실리콘의 약 50%는 컴퓨트, 약 50%는 SRAM
- 온-웨이퍼 SRAM: 44GB, 대역폭 21PB/s
- 전력 소비: 웨이퍼 1장당 약 23kW
- 웨이퍼 열팽창: 약 0.1mm(십분의 1밀리미터)
- NVL72: 72칩 구성 (비교 대상)
- Trilogy Systems 조달액: 약 2억 3000만 달러(오늘날 가치로 약 10억 달러 상당)
- Trilogy 공장 규모: 3300만 달러
- Trilogy Hail Mary IPO 조달액: 약 6000만 달러, 초기 주가 12달러 → 거의 0달러로 폭락
- Trilogy 창업(1980년대) ~ Cerebras 상장까지: 약 40년
- Fractile 조달액: 2억 2000만 달러(팟캐스트 녹음 전날 발표)
- Groq LPU의 SRAM 용량: "170 megabytes or something"(대략적 수치로 언급)

## 그대로 인용 (영어 원문 + 한국어 옮김)

- "This was an insane IPO because it was oversubscribed massively and they used an eBay bidding style approach" — "정말 미친 IPO였다. 엄청나게 초과 청약됐고, 이베이식 입찰 방식을 썼다." (Vik)
- "44 GB of on-wafer SRAM operating at 21 petabytes per second memory bandwidth. That's amazing." — "44GB의 온-웨이퍼 SRAM이 초당 21페타바이트의 메모리 대역폭으로 작동한다. 놀랍다." (Vik)
- "I don't think this whole thing is about cost at all" — "이건 애초에 비용에 관한 이야기가 전혀 아니라고 본다." (Vik)
- "We are not in a position to do this for another 100 years. We cannot make this happen for another 100 years." — "앞으로 100년은 이걸 해낼 수 있는 위치에 있지 않다. 100년 안에는 이걸 이룰 수 없다." (Vik이 전한 Gene Amdahl의 발언)
- "Open models was a gift to Groq. Groq was a gift to Cerebras." — "오픈 모델은 Groq에게 선물이었다. Groq는 Cerebras에게 선물이었다." (Austin)
- "The need for memory bandwidth during the decode phase of disaggregated inference is a gift that landed in Cerebras' lap." — "분리형 추론의 디코드 단계에서 필요한 메모리 대역폭 수요가 Cerebras의 품에 굴러떨어진 선물이다." (Vik)
- "We live in the wild west of the inference world." — "우리는 추론 세계의 무법지대에 살고 있다." (Vik)

## 주의

- 조달액(55억 달러), 초기 목표 조달액(35~40억 달러), 코어 수(970K 수준) 등은 진행자들이 "I believe"·"or something"·"roughly speaking" 같은 헤지 표현을 쓰며 구두로 언급한 값이다. 정확한 공식 수치는 회사 공시를 확인해야 한다.
- Groq LPU의 SRAM 용량("170 megabytes or something")은 Austin이 추정치로 언급한 것으로, 정확한 스펙이 아니다.
- SemiAnalysis의 포토닉 인터커넥트 관련 기사 내용은 Austin이 "다 읽지 못했다(I didn't read too much about it)"고 밝힌 상태에서 전한 것이라 세부 내용이 불확실하다.
- Trilogy Systems 관련 일화(재무 담당자 사망, Amdahl의 롤스로이스 사고 등)는 Vik이 구두로 재구성한 이야기이며, 재무 담당자 이름은 "Clifford Madden이라고 적어뒀다(I've written down his name as)"고 스스로 불확실성을 표시했다.
- 이 사이트는 팟캐스트 오디오의 텍스트 전사본이며, "lightly edited for clarity"라는 표기가 붙어 있다.
