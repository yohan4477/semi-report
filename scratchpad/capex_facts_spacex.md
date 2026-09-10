# 사실표 — 스페이스X영문 / 스페이스X

라벨 `스페이스X영문` = `input/clippings/SpaceX 10GW in 2027 – Why It's Real, Will Drive $300B ARR for SpaceX, and Why Microsoft Will Be the Largest Offtaker.md` (정본, Read 도구 줄번호 기준)
라벨 `스페이스X`는 대조 대상으로만 열었고, 값은 전부 영문 원문에서 뽑았다(수치 표기가 동일해 별도 줄번호는 안 붙인다).

## ① GW당 자본지출과 구성

- L14 | "At 50B per GW, that's $300-500B in capex in 2027" — GW당 자본지출 $50B, 2027년 총 capex $300-500B (6-8GW 기준, well above +10GW 가능성 포함) | 성격: 회사 주장(Elon 발표 기반 저자 추정) | 언제 것: 2026-08 (발표는 2027년 계획)
- GPU·데이터센터·전력 각각의 몫으로 나눈 구성비 수치: 없음. L42에서 "$300B of total contract value (not including the GPU cost)"라고만 밝혀 GPU 비용이 이 $300B 밖에 별도로 있다는 사실만 나온다 — 몫(%)은 안 나온다.

## ② MW당 연 매출 값

- L18 | "priced at a huge premium – up to $50B/GW/year" — 대규모·단기 컴퓨트의 가격 상한, GW당 연 $50B (= MW당 연 $50M) | 성격: 회사 주장(SemiAnalysis 분석) | 언제 것: 2026-08
- L20 | "both OpenAI and Anthropic can generate over $100B/GW/year of revenue when selling API inference on a GB300 cluster" (= MW당 연 $100M 초과) | 성격: 추정(SemiAnalysis Tokenomics Model/Inference Simulator 산출) | 언제 것: 2026-08
- L26 | "We assume around $12B/GW/year of cost per year, using a conservative rental pricing rate of $3/GPU-hr" — GW당 연 비용 $12B, GPU 시간당 임대가 $3 가정 | 성격: 추정(저자 가정) | 언제 것: 2026-08
- L36 | "much of their datacenter capacity currently goes to OpenAI at ~14M/MW/year" — 현재 마이크로소프트가 OpenAI에 임대 중인 계약가 MW당 연 ~$14M | 성격: 추정 | 언제 것: 2026-08(현재 시점)
- L40 | "Microsoft signing 3GW with SpaceX for 50B/GW/year" (= MW당 연 $50M) — 마이크로소프트·스페이스X 간 3GW 계약 가정가 | 성격: 저자 판단(가능성 시나리오, "sounds insane"이라 명시) | 언제 것: 2026-08
- L53 | "price it accordingly at 30-50M/MW/year" — 스페이스X가 3-5개월 리드타임을 무기로 매기는 판매가 MW당 연 $30-50M | 성격: 회사 주장/저자 추정 | 언제 것: 2026-08
- L62 | "We'll briefly discuss economics to get to $100M/MW/year of inference revenue" | 성격: 추정 | 언제 것: 2026-08
- L72 | "their desperate need for compute to capture a $100M/MW/Year revenue opportunity" | 성격: 추정 | 언제 것: 2026-08
- L102 | "This is Microsoft's $100M per MW opportunity." | 성격: 추정 | 언제 것: 2026-08

## ③ 회수기간(payback) 언급과 계산 근거

- L53 | "That pays back the capex in less than a year." — 근거: 3-5개월 리드타임 기반 산업 최고가 판매(30-50M/MW/year)로 인한 영업현금흐름 조달. 구체적 계산식(분자·분모)은 본문에 없음 — "$50B/GW capex ÷ $30-50M/MW/year 매출"이라는 명시적 나눗셈은 원문에 안 나온다, 결론만 서술 | 성격: 저자 판단 | 언제 것: 2026-08
- L92 | "the leaked DeepSeek investor call (which said they have a 10-month GPU payback period)" — 스페이스X가 아닌 DeepSeek 사례, 마진 추정치의 방증으로 인용된 것 | 성격: 회사 주장(DeepSeek 투자자 콜 유출, 제3자) | 언제 것: 2026-07(유출 시점, news.pedaily.cn 기사)

## ④ 총 용량 계획 · 연도별 배치 · 총 capex

- L14 | "aims to build & deliver an incremental 6-8GW in 2027 alone, with potential for that number to be well above +10GW" | 성격: 회사 주장(Elon 발표) | 언제 것: 2026-08 (SpaceX 첫 실적발표)
- L58 | 스페이스X 2027년 말까지 "path to $300B of ARR" — 2027년 증분 컴퓨트의 50%만 수익화한다는 가정, 나머지는 Grok·Cursor 팀 학습용(추론 매출 미반영) | 성격: 추정 | 언제 것: 2026-08 (2027년 말 시점 목표)
- L104 | "their compute capacity will "only" be 2GW by year-end 2026" | 성격: 추정 | 언제 것: 2026-08 (2026년 말 시점)
- L66 | "Microsoft has contracted over 10GW across all these surfaces, which is the equivalent of ~$300B in new binding commitments." | 성격: 공표(마이크로소프트 서명 계약 기준, SemiAnalysis Datacenter Model 집계) | 언제 것: 2026-08 (year-to-date 누적)
- L72 | "Microsoft signed in October 2025 a $250B agreement with OpenAI, which we estimate at ~7GW in total" | 성격: 공표($250B 계약) + 추정(~7GW 환산) | 언제 것: 2025-10
- L112 | "The power plant in Southaven has expanded from 27 turbines (~495MW) in February 2026, to 69 turbines (1.7GW) in July 2026." | 성격: 공표(관측 기반, SemiAnalysis Datacenter Industry Model) | 언제 것: 2026-02~2026-07
- L118 | "MiniHard,\" which upon vertical construction in March 2026, will likely reach 450-500MW in just ~5 months!" | 성격: 추정 | 언제 것: 2026-03 착공 기준
- L162 | "474k sqft building in Southaven, Mississippi. That size could provide ~1GW of capacity or more." / "863k sqft site in Olive Branch, Mississippi"(용량 수치 없음) | 성격: 추정 | 언제 것: 2026-08
- L166 | "the Pampa location – aiming to deploy 2GW of onsite generation" | 성격: 회사 주장/추정(문서에 "No documents confirm this yet"라고 명시 — 저자 판단에 가까움) | 언제 것: 2026-08

## ⑤ 오프테이크·계약 조건

- L40 | "Microsoft signing 3GW with SpaceX for 50B/GW/year" — 상대방: 마이크로소프트, 규모: 3GW, 조건: $50B/GW/year | 성격: 저자 판단(가능성 시나리오, 확정 계약 아님) | 언제 것: 2026-08
- L42 | "they've signed 10GW of contracts year-to-date, for over $300B of total contract value (not including the GPU cost)... these contracts contribute to late 2027 and 2028 capacity" — 계약 기여 시점: 2027년 말~2028년 | 성격: 공표 | 언제 것: 2026 year-to-date
- L44 | "With a 90-day cancellation policy, akin to the SpaceX deals with Anthropic and Google, there is zero balance sheet risk." — 계약 조건: 90일 해지 조항, 상대방: 앤스로픽·구글(기존 스페이스X 딜) | 성격: 회사 주장 | 언제 것: 불명(기존 딜 기준)
- L72 | 마이크로소프트-OpenAI $250B 계약, ~7GW 환산 | 성격: 공표+추정 | 언제 것: 2025-10
- L36 | "the deal reworked in April 2026 dropped the old 20% revenue share from the equation" — 마이크로소프트-OpenAI 계약 재구성, 기존 매출분배 20% 조항 삭제 | 성격: 공표 | 언제 것: 2026-04

## ⑥ 마진·비용 구조

- L36 | 마이크로소프트는 OpenAI 모델에 "full access"가 있어 "the exact same revenue and margin per MW, while paying none of the training costs" — 학습비 부담 없음 | 성격: 저자 판단 | 언제 것: 2026-08
- L90 | "inference gross margins are north of 60%" (2026년 1월 최초 제시) | 성격: 추정 | 언제 것: 2026-01(최초 제시), 서술은 2026-08
- L90 | "Opus 4.8 in particular had 85%+ margins" (2026년 6월 딥다이브) | 성격: 추정 | 언제 것: 2026-06
- L26 | 토큰 원가 산정 근거: GPU 시간당 임대가 $3(보수적 가정), Inference Simulator로 토큰 산출량 추정, 입력·캐시읽기·캐시쓰기·출력 토큰 비용을 실제 워크로드 비율로 블렌딩 | 성격: 추정 | 언제 것: 2026-08

## ⑦ 자금 조달

- L51 | "Support from Nvidia, in the form of vendor financing to lower the upfront cash cost." — 조달 수단: 엔비디아 벤더 파이낸싱(선급 현금 부담 완화) | 성격: 저자 판단 | 언제 것: 2026-08
- L53 | "Operating cash-flow financing led by industry-high pricing, enabled by fastest timelines" — 조달 수단: 영업현금흐름(산업 최고가 판매 + 최단 리드타임에서 창출) | 성격: 저자 판단 | 언제 것: 2026-08
- 조달 "규모"(부채·주식 발행액 등 구체적 금액)는 없음 — 원문은 수단만 서술하고 액수는 안 밝힌다.
- L44 | "zero balance sheet risk" — 90일 해지 조항 덕에 마이크로소프트 쪽 재무 위험 없음(스페이스X 관점 자금조달과는 별개, 계약상 리스크 배분 서술) | 성격: 회사 주장 | 언제 것: 2026-08

## ⑧ 우주·위성 쪽 값(발사 비용·질량 등)

- 없음. 원문은 데이터센터·전력·컴퓨트 경제성만 다루고, 발사 비용·위성 질량 등 우주 사업 고유 수치는 언급하지 않는다.

## ⑨ 원문이 명시한 계산식·가정

- L14 | 계산: "6-8GW × $50B/GW = $300-500B"(원문이 명시적으로 곱셈 형태로 쓰지는 않았으나 "At 50B per GW, that's $300-500B in capex" 로 GW당 단가 × 용량 구조를 직접 서술) | 성격: 회사 주장/저자 추정
- L26 | 계산 가정: GPU 임대가 $3/GPU-hr(보수적), Inference Simulator의 토큰 산출량 추정, agentic coding 벤치마크(AgentX) 트레이스로 워크로드 비율 산정 → "$100B/GW/year 초과" 도출 | 성격: 추정
- L58 | 가정: "2027년 증분 컴퓨트의 50%만 수익화, 나머지는 Grok·Cursor 학습용(추론 매출 미반영)" → $300B ARR 도출 근거 | 성격: 추정

## ⑩ 표·그림에서만 보이는 값

- L24, L38, L60, L100 등 이미지 캡션("Source: SemiAnalysis Tokenomics Model", "Inference Simulator") — 그림 자체에 담긴 수치(예: GB200 vs GB300 매출 비교, Microsoft 계약 누적 추이)는 이미지이며 OCR·수치 추출 불가. 캡션 텍스트만 확인했고 그림 속 구체적 값은 "그림에서만"이며 이 사실표에는 못 옮겼다.
- L68-70 | 이미지("The SemiAnalysis diagram illustrates Microsoft's projected growth in energy contracts and construction activities for the years 2025 and 2026")도 마찬가지로 그림에서만 — 수치 미추출.
- L114, L126, L154, L160, L164, L168 | 지도·표 이미지(Southaven 발전소, MiniHard, Olive Branch/Pampa 부지) — 그림에서만, 본문 텍스트로 언급된 수치(L112, L118, L162, L166)는 위에 이미 옮겼고 그 외 이미지 자체의 추가 값은 추출 불가.

---
확인: 위 인용 25개 줄(L14, 18, 20, 26, 36, 40, 42, 44, 51, 53, 58, 62, 66, 72, 90, 92, 102, 104, 110, 112, 118, 124, 142, 162, 166)을 `sed -n 'NNNp' <파일>`로 다시 열어 원문과 대조했다. 전부 일치.
