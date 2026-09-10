# 사실표 — 우주영문 / 우주

파일:
- 우주영문 = `input/clippings/To Boldly Go The Case for Space Datacenters.md` (924줄, 정본)
- 우주 = `content/newsletter/ai_infra/business/[260603] 우주로 담대하게 - 우주 데이터센터의 경제성.md` (592줄, 참고)
줄 번호는 모두 우주영문(영문 원문) 기준. 우주(한글본) 인용은 별도로 [우주 L...] 표기.

## 1. 지상 데이터센터 MW당 자본지출 — 층별

- L252 | Layer 1(계통연계) infrastructure costs in the $12–15M/MW range | 성격: 공표 | 언제 것: 2026-06 (모델 기준)
- L280 | Layer 2(전환·유휴부지) 사이트는 grid-connected supply와 비슷하거나 더 낮음, around $10–15M/MW | 성격: 저자 판단 | 언제 것: 2026-06
- L292 | Layer 3(BTM) system-wide DC-addressable ceiling(2027년까지 연 수십 GW) 비용은 $15-20M/MW | 성격: 저자 추정 | 언제 것: 2026-06
- L306 | Layer 4(산업생산 확충) 진입 시 costs per MW beyond the $20M/MW range | 성격: 저자 추정 | 언제 것: 2026-06
- L492 | Facility construction is projected at $15–18M/MW by 2027 as demand outstrips build capacity | 성격: 저자 추정 | 언제 것: 2027 전망
- L506 | Elon Musk 시나리오: Earth datacenter capex costs to nearly $55M/MW vs the $12-14M/MW modeled today; 동시에 space datacenter capex per MW down to $11M/MW | 성격: 저자 시나리오 가정(상방 케이스, 공식 통일된 견해 아님이라고 저자가 직접 명시) | 언제 것: 2026-06 대비 장기 전망
- L228 | 「Peak Oil Theory」를 데이터센터 전력 공급에 빌려와 층별로 비용이 올라간다고 설명 — cost escalates as we tap into more difficult to access sources of power | 성격: 저자 판단(비유) | 언제 것: 불명
- 참고 [우주 L121-124] 한글본 mermaid 도해에 1~4층 MW당 비용이 요약(계통 $12~15M/MW · 전환 $10~15M/MW · BTM $110~170/MWh · 산업생산 $20M/MW+) — 원문(영문) 수치와 일치, 별도 신규 값 없음 | 성격: 공표/저자추정 혼합 | 언제 것: 2026-06

## 2. MW당 연 매출·계약 임대료, 가동률·계약 기간

- L280 | 「1 GW of AI capacity can support on the order of $12–13B of annual revenue」(1GW당 연 매출, MW당이 아니라 GW당 값) | 성격: 저자 추정 | 언제 것: 2026-06
- L280 | Oracle committed at least $3.65B to support 1.4 GW of capacity at Related/Oracle/DTE Electric campus, Michigan | 성격: 공표(회사 발표) | 언제 것: 2026-06 시점 기준
- L288 | 「major AI cloud contracts imply annual revenue in the range of roughly $12–13M per MW of contracted critical IT load」 | 성격: 저자 추정 | 언제 것: 2026-06
- L288 | getting 200 MW online six months early carries an NPV of roughly $400M-$500M | 성격: 저자 추정 | 언제 것: 2026-06
- L432 | 지상 B300 클러스터 가정: power utilization rate of 80% (steady training workloads 기준), PUE 1.35 | 성격: 저자 모델 가정 | 언제 것: 2026
- L890 | 30kW 클러스터 기준 전기요금 연 ~$25k/year (1.35 PUE·~80% utilization 가정) | 성격: 저자 추정 | 언제 것: 2026
- 계약 임대료·가동률에 관한 그 이상의 세부(임대차 계약기간 등)는 원문에 없음 — 없음

## 3. NPV·IRR·회수기간, 할인율·기간 가정

- 원문에 IRR·payback period(회수기간) 값은 없음 — 없음. NPV는 BTM 200MW 조기 가동 사례($400-500M, L288)만 명시
- L400 | 지상 WACC 10.3%(flat) = ~7% pre-tax cost of debt, 20% cost of equity, 75/25 debt-equity split | 성격: 저자 모델 가정 | 언제 것: 2026
- L400 | 우주 WACC 초기 15.0%, declines over time to reach parity at 10.3% within ~10 years | 성격: 저자 모델 가정 | 언제 것: 2026-2036년경까지
- L520 | 위 WACC 가정 재확인(동일 문구, Part Three 결론부) | 성격: 저자 모델 가정 | 언제 것: 2026
- L522 | SpaceX 실제 자본비용 참고치 — S-1 기준 $20B SpaceX Bridge Loan effective rate 4.58%(SOFR + 75-175 bps), equipment leases via Valor ~5.5% blended, weighted average pre-tax cost of debt ~4.86% | 성격: 공표(S-1 공시) | 언제 것: 2026-03(브리지론 체결 시점 기준)
- L535 | 참고 비교치: Hyperscaler WACC typically 8-10%, pure project finance for established infra 5-8% | 성격: 저자 판단 | 언제 것: 불명(일반론)
- L400, L420 | 감가상각/유효수명 가정: IT equipment 5-year useful life(양쪽 동일); 데이터센터 자산 — 우주 5년(2032년 이후 10년으로 개선 가정) vs 지상 15년 | 성격: 저자 모델 가정 | 언제 것: 2026, 2032 이후
- L412 | 지상 데이터센터 facility life 가정: 5-year useful life until 2032, then 10-year useful life after (이는 지상이 아니라 텍스트상 space 관련 문맥 — 재확인 필요. 원문은 "5-year useful space datacenter facility life until 2032, then... 10-year useful life after"로 공간(우주) 시설 수명을 말함) | 성격: 저자 모델 가정 | 언제 것: 2026-2032

## 4. 전력원가 — $/MWh, 기술별, 계통 대기 기간

- L252 | North Virginia's PJM interconnection timelines run to roughly seven years in practice | 성격: 저자 판단(업계 관찰) | 언제 것: 2026-06 기준
- L288 | BTM all-in costs roughly $110–170/MWh depending on technology | 성격: 저자 추정 | 언제 것: 2026-06
- L288 | grid power can already clear around $150/MWh in major US markets | 성격: 저자 판단(시장 관찰) | 언제 것: 2026-06
- L432 | 지상 datacenter 전기요금 가정 $0.087/kWh(=8.7 cents/kWh, L890과 동일 값) | 성격: 저자 모델 가정 | 언제 것: 2026
- L492 | Electricity has climbed 2–5%/year in major datacenter markets, Virginia spiking 15–20% in 2023–2024 from capacity strain | 성격: 저자 관찰/추정 | 언제 것: 2023-2024, 전망 2-5%/년
- L492 | Land and permitting timelines stretched from 12–18 months to 36–48 months in constrained markets | 성격: 저자 관찰 | 언제 것: 불명(최근 추세)
- L256-258 | 미 ISO 계통 신뢰성 여유(gross positive grid reliability headroom, ELCC 방식): 2021년 70.2 GW → 2025년 18.3 GW → 2026년 15.9 GW → 2027년 마이너스 전환 → 2030년 약 40GW 적자 | 성격: 공표(SemiAnalysis Energy Model 산출치) | 언제 것: 2021-2030
- L262 | 세계 데이터센터 전력소비 2024년 약 340 TWh(전세계 발전량 약 1.1%); AI 전용 수요 현재 약 0.3%, 2027년경 1.7%, 2030년 5% 미만(가속 시나리오도 2030년 약 7%, 연속 전력수요 약 380GW) | 성격: 저자 추정 | 언제 것: 2024-2030
- L274 | 2027년까지 글로벌 데이터센터 신규 발전 용량 추가분 ~106 GW | 성격: 저자 추정 | 언제 것: 2027까지

## 5. 우주 데이터센터 자본지출 — 발사비용($/kg), 질량, 지상 대비 배수

### 발사비용 ($/kg)
- L118 | ~80% drop in launch costs from ~$1,400-$1,800/kg for Falcon 9 today to only ~$250/kg for Starship(미래, SpaceX 전망) | 성격: 저자 판단(SpaceX 비전 인용) | 언제 것: 2026-06(현재) → 미정(미래)
- L494 | Starship targets $250–500/kg by 2028, and long-run costs below $185/kg(저자는 base case에 더 보수적/높은 값 사용한다고 명시) | 성격: 회사 주장(SpaceX 목표) | 언제 것: 2028, 장기
- L645 | Falcon 9 (expendable/rideshare) 16,000–22,800 kg to LEO, 5.2m fairing, at $1,200-$1,700/kg (internal cost); Starship targets 100-150 tons to LEO, 9m fairing, at ~$500/kg (internal cost); Starship V2 초기 비행은 ~50 tons | 성격: 저자 추정(내부원가) | 언제 것: 2026-06
- L824 | 현재 수준 launch cost ~$1,750/kg, 2026년 30kW 위성 기준 launch costs = 40% of total program cost | 성격: 저자 모델 가정 | 언제 것: 2026
- L826 | Starship 도입 후 2032년 launch cost ~$650/kg으로 하락, program cost 비중 14.5% | 성격: 저자 모델 전망 | 언제 것: 2032
- L830 | 3개 발사비용 시나리오 — (1) 기준안: $645/kg by 2032, $309/kg by 2050 (2) Elon Musk안: $384/kg by 2032, ~$80/kg by 2039, $50/kg by 2042(이후 2050까지 flat) (3) 완만안(slow case): $744/kg by 2032, $500/kg by 2050 | 성격: 저자 모델 시나리오 | 언제 것: 2032-2050
- L516 | Elon Musk scenario launch cost $80/kg vs ~$1,700/kg today, vs $485/kg in base case(특정 연도 명시 없이 비교) — 이 문장 자체는 시점 특정 안 함(다른 문장 L830에서는 2039년 기준 $80/kg) | 성격: 저자 모델 시나리오 | 언제 것: 불명(비교 시점 혼재 — 확인 필요)
- L846-848 | Falcon 9 실제 원가: reused 1단 marginal cost ~$1.2M, 소모성 2단 ~$9M; 외부고객 가격 ~$67–70M/launch; 내부 Starlink 임무 marginal cost ~$15M; fully loaded internal cost ~$31M/launch = ~$1,350–1,400/kg to LEO(fully loaded payload 가정); FY25 Space Capex $3.8B ÷ 122 internal launches = $31M/launch | 성격: 저자 추정(공개 진술 기반 역산) | 언제 것: 2020-2023(머스크 발언), 2025(FY25 실적)
- L836, L838 | SpaceX 누적 ~7,400 metric tons to orbit(2026년 3월까지), 세계 궤도 질량의 >80%(2023년 이후); Falcon 9 2025년 165회 발사, 누적 >540회 재사용 부스터 발사·~530회 착륙(2026-03-31 기준); 부스터 설계수명 최대 40회(기록 34회), 회계상 25회 인정 | 성격: 공표 | 언제 것: 2026-03
- L858 | Starship V3: >100 tons to LEO fully reusable, up to ~200 tons expendable | 성격: 회사 주장 | 언제 것: 2026-05(V3 첫 비행)
- L878 | Starship 목표 건조비 $50-90M/척, 항공기식 반복운항 지향 | 성격: 저자 판단/회사 주장 혼재 | 언제 것: 불명
- L880 | 완전 재사용 성숙 시 sub-$500/kg per launch 가능(그림에서만 상세 수치) | 성격: 저자 추정 | 언제 것: 불명

### 우주 위성 질량·비용 배분
- L342 | Terafab 배분: compute allocation 80% space / 20% terrestrial, 약 800 GW orbital + 100-200 GW terrestrial inference | 성격: 회사 주장(머스크 발표) | 언제 것: 2026-03
- L659, L661, L673 | 우주 프로그램 capex 구성비 변화: 2026년 launch 40% + bus/propulsion 19% + IT cluster 24%; 2032년 launch 15% + bus/propulsion 4% + IT cluster 65%; USD per all-in Critical IT power: $132/W(2026) → $65/W(2032) | 성격: 저자 모델 산출 | 언제 것: 2026, 2032
- L667-671 | Space program costs 표(달러·비중·wet spacecraft mass당 kg 단위) — 「그림에서만」(본문 텍스트에 구체 수치 없음, 이미지 표로만 제시) | 성격: 불명 | 언제 것: 2026, 2032

### 지상 대비 배수
- L76, L122 | 기준안: 우주-지상 비용 격차 2026년 more than 4x, ~2040년 parity, 2030년대 초 우주가 지상보다 ~30% 더 비쌈 | 성격: 저자 모델 산출 | 언제 것: 2026-2040
- L100, L102 | 30.5kW B300 datacenter(2026): 우주 total program capital cost $4.1M vs 지상 $1.4M; 월간 총소유비용 우주 $100,925/월 vs 지상 $27,724/월; datacenter capital cost 내 launch cost $1.6M(총 $3.1M 중); 월 평준화 datacenter capex 18x higher(우주) | 성격: 저자 모델 산출 | 언제 것: 2026
- L106, L110 | TCO $8.64/hr/GPU(우주) vs $2.37/hr/GPU(지상); LCOC $10.91/hr/GPU(우주, TCO 대비 26% gross up) vs $2.49/hr/GPU(지상, TCO 대비 5% gross up) | 성격: 저자 모델 산출 | 언제 것: 2026
- L376 | 월간 총소유비용 우주가 지상 대비 nearly four times higher; datacenter capex 8x higher(우주); 5y(우주) vs 15y(지상) 수명 반영 시 월 비용 17x higher | 성격: 저자 모델 산출 | 언제 것: 2026 (※L102의 "18x"와 L376의 "17x"는 표현이 다름 — 확인 필요, 둘 다 원문에 실재)
- L418, L420 | 2026년 datacenter capital cost(IT 제외) 우주 $3.1M vs 지상 $382K; 최대 항목 launch cost $1.6M(총 ~$3.1M 중); levelized 반영 시 datacenter capital cost of ownership 우주 $6.29/hr/GPU vs 지상 $0.36/hr/GPU(17x higher) | 성격: 저자 모델 산출 | 언제 것: 2026
- L512, L539 | Elon Musk 시나리오: 2039년 Space DC costs nearly 20% lower than Earth DC costs(기준안은 그때 겨우 parity); 2039년 launch costs는 space DC total program capex의 ~10%에 불과(2026년 40%에서 하락), 10x $/W 하락에도 total cost of ownership엔 영향 작음 | 성격: 저자 모델 산출 | 언제 것: 2039
- L452, L454 | B300 dense FP4 4,500 TFLOPS 기준 LCOC: 지상 $0.17/PFLOP-hr vs 우주 $0.73/PFLOP-hr; InferenceX 벤치마크(disagg TRT, MTP, Deepseek R1) 기준 B300 ~5,100 tok/s/GPU → 추론 LCOC $135/Billion Tokens(지상) vs $590/Billion Tokens(우주, 2026) | 성격: 저자 모델 산출 | 언제 것: 2026

## 6. GPU·서버 원가와 갱신 주기, GW당 웨이퍼 가치, 메모리 비중

- L398 | 2026년 30.5kW B300 클러스터(2대 서버×8 B300): base server cost $880,400; Service/Networking/Storage/Software 등 추가 $89,956; 우주 전용 capitalized burn-in cost $10,526; 지상 전용 capitalized server service cost $15,802; 총 IT cluster capex — 우주 $980,882, 지상 $986,158 | 성격: 저자 모델 산출 | 언제 것: 2026
- L400 | IT equipment useful life 5년(양쪽 동일); IT capital cost of ownership 우주 ~$2.00/hr/GPU vs 지상 $1.81/hr/GPU | 성격: 저자 모델 산출 | 언제 것: 2026
- L348 | Accelerator and HBM Model: 1GW of deployed compute = 354K wafer starts(logic+memory+packaging), memory over 60% of total; Wafer value per GW ~$3B; "1TW" 동시가동 해석 시 354M wafer starts/year = TSMC 전세계 생산량의 21x | 성격: 저자 모델 산출 | 언제 것: 불명(모델 기준)
- L340, L346 | Terafab: $20-25B 예산, 100K WSPM 시작 → 1M WSPM 목표(TSMC 전세계 생산량의 ~70%); 글로벌 300mm foundry capacity 4M+ WSPM(2025); Terafab 100K는 세계 wafer starts의 2.5%, 1M full scale은 세계의 24%(TSMC 단독의 68%) | 성격: 회사 주장(Terafab 발표치) + 저자 검증(비중 계산) | 언제 것: 2025-2026-03
- L314, L316 | AI 관련 수요가 TSMC N3 output의 60% 미만(2026년), ~86%(2027년) 소비; DRAM 중 AI 수요 비중 12%(2023) → ~70%(2027); HBM은 commodity DRAM 대비 bit당 wafer capacity 약 3배 소비 | 성격: 저자 모델 산출/추정 | 언제 것: 2023-2027
- GPU 갱신 주기(구체적 refresh cycle 연수)는 IT equipment useful life 5년(L400) 외에 별도 명시 없음 — 없음

## 7. 전력·열 관련 물리 값

- L178 | 잠재 solar irradiance 1,361 W/m²; LEO(고도 400-500km, 하루 ~15궤도, 태양광 ~60% 시간) 평균 실효 irradiance ~800 W/m² | 성격: 저자 계산(물리 상수+가정 결합) | 언제 것: 불명(물리)
- L180 | SSO eclipse 최대 up to 35 minutes per day | 성격: 저자 판단 | 언제 것: 불명
- L601 | Solar irradiance at orbit altitude 1,361 W/m²(solar constant) vs 1,000 W/m² Standard Test Conditions(지상 태양광 패널) | 성격: 공표(물리 상수) | 언제 것: 불명
- L603 | 지상 atmospheric attenuation 27%(clear-sky); weather discount factor 20-25%(best-case sunny) ~ 40-50%(global average) | 성격: 저자 추정 | 언제 것: 불명
- L617, L723 | GPU cold plate 운전온도 상한 ~350K(~80°C); LEO effective sink temperature ~255K → radiator rejects ~880 W/m²; radiator temp 343K/sink 255K/emissivity 0.95 double-sided → ~880 W/m², 30kW 위성은 ~42 m² radiator area 필요 | 성격: 저자 계산(Stefan-Boltzmann 적용) | 언제 것: 불명(물리)
- L710-721 | Stefan-Boltzmann 식 P_rad = εσA(T_rad⁴ − T_sink⁴) 명시(변수: 방사전력·방사율·상수·면적·방열판온도·싱크온도) | 성격: 공표(물리 법칙) | 언제 것: 불명
- L619 | 방열판 baseline 소재 Al 6061(98% Al·1% Mg·0.6% Si·0.3% Cu·0.2% Cr); 3mm 두께+heat pipe 내장 시 areal density ~8 kg/m² | 성격: 저자 모델 가정 | 언제 것: 2026 기준
- L705, L731 | 방열판 패널 areal density 8 kg/m²(2026) → 3.5 kg/m²(2032, 소재 개선); 방열판 kW당 비용 $4,500/kW(2026) → $2,000/kW(2032, 65% 절감); heat rejection per m² 880 W/m² → ~1,400 W/m²(온도·코팅 개선) | 성격: 저자 모델 산출 | 언제 것: 2026-2032
- L733, L735 | 방열판 specific power ~80 W/kg(2026) → 195 W/kg(2032, droplet radiator 등) → 300 W/kg(2050년경, 개선 둔화) | 성격: 저자 모델 산출 | 언제 것: 2026-2050
- L725 | 방열판 370K 운전 시 320K보다 2.3x more heat per m² 배출; 칩 신뢰성 한계는 ~85-90°C 초과 시 고장모드 가속 | 성격: 저자 계산+공학 판단 | 언제 것: 불명
- L727, L729 | Al 6061-T6: 열전도율 167 W/m·K(honeycomb 없이도 열 확산 가능); honeycomb 생략 시 질량 ~33% 증가(8 vs 6 kg/m²); honeycomb 가공비 $800+/m² 추가 대비, Starship 발사단가($200-600/kg)에서는 무게 페널티($16,000-84,000, 40m² 배열 80kg 추가 기준)가 honeycomb 비용($32,000-150,000)보다 작음 | 성격: 저자 계산 | 언제 것: 불명(Starship 궁극 목표 발사비용 기준)
- L683 | 태양광 셀 효율: silicon 20-22%, triple-junction GaAs 28-32%(비용은 GaAs가 10-20x/W 비쌈); 30kW-1MW 규모에서는 silicon이 유리; 셀 단가 <$0.30/W, 모듈+기판+하네스 합산 총 $2.70/W(2026) | 성격: 저자 모델 산출 | 언제 것: 2026
- L687, L691 | 태양광 총단가 $2.70/W(2026) → $2.54/W(2032); 셀 열화 ~2.5%/year, 5년 임무 종료 시 ~12% 출력 감소(BOL-EOL 오버사이징으로 대응) | 성격: 저자 모델 산출 | 언제 것: 2026-2032

## 8. 원문이 명시한 계산식·가정

- L400, L520 | WACC — 지상 10.3%(flat, 7% pre-tax debt cost·20% equity cost·75/25 D/E), 우주 15.0%(초기)→10.3%(수렴, ~10년) | 성격: 저자 모델 가정 | 언제 것: 2026
- L400, L420 | 유효수명 — IT equipment 5년(양쪽); 데이터센터 자산 우주 5년(2032 이전)/10년(2032 이후) vs 지상 15년 | 성격: 저자 모델 가정 | 언제 것: 2026-2032
- L432, L890 | 전력가격 가정 $0.087/kWh, PUE 1.35, utilization 80% | 성격: 저자 모델 가정 | 언제 것: 2026
- L442 | LCOC 보정 — radiation availability 95%(우주) vs 100%(지상); 99% SLA 도달용 추가 GPU: 지상 cold spare 최대 5% vs 우주 redundancy 20% | 성격: 저자 모델 가정 | 언제 것: 2026
- L126, L472 | 지상 GPU 연간 고장률(사람 손 개입 필요) 3-6%; burn-in 기간 조기 고장률 통상치의 3-4배(10-20%) | 성격: 저자 판단(업계 관찰) | 언제 것: 불명
- L900 | 우주 COTS 부품 연간 고장률 모델 가정 5%(Starlink 실적 2-3%보다 보수적) | 성격: 저자 모델 가정 | 언제 것: 불명
- L492 | 전력가격 상승률 가정 2-5%/year(주요 시장), Virginia 급등 15-20%(2023-2024) | 성격: 저자 추정 | 언제 것: 2023-2024, 전망치
- L807 | Structure and Integration: 구조 건조질량의 constant 15%, 시작단가 $1,000/kg(하락 추세) | 성격: 저자 모델 가정 | 언제 것: 불명
- L816, L818 | AI&T "10% Rule"(업계 heuristic, 하드웨어 조달비의 ~10%); 저자 모델은 초기 15%(non-GPU costs 기준) → 2032년 10%로 수렴 | 성격: 공표(업계 heuristic) + 저자 모델 가정 | 언제 것: 2032까지
- L797, L799 | 추진계 — 수명종료 deorbit(650km→200km) 약 120-150 m/s; 최소 thruster 2대; 2026년 30kW 위성 propulsion hardware cost $400,000, 2032년 $354k(6년간 cost-down) | 성격: 저자 모델 가정 | 언제 것: 2026, 2032

## 9. 원문 표/그림에서만 보이는 값 (「그림에서만」 표시)

- L667-671 | Space program costs 표 3종(절대 달러·프로그램 비용 대비 비중·wet spacecraft mass kg당 비용) — 본문에는 구조적 설명만 있고 구체 숫자는 이미지 표에만 존재 | 「그림에서만」
- L74, L78, L84, L88 | 우주-지상 비용 곡선(연도별 4x→parity→역전) 실제 곡선값은 도해 이미지에만 있음(본문은 L76, L122 등에서 서술적으로만 인용) | 「그림에서만」
- L232 | 5개 공급층 통합 도해(SemiAnalysis Energy Model 인용) — 층별 구체 수치는 본문 문장이 아니라 그림 캡션/출처만 | 「그림에서만」
- L246 | 실리콘 용량이 AI 칩 배치를 제약하는 표(6341x3691 이미지) — 수치 본문 없음 | 「그림에서만」
- L326, L338 | 테라팹 base case 반도체 제약 완화 정도를 보여주는 차트(686x563, 687x510) — 본문은 서술만, 구체 수치는 이미지만 | 「그림에서만」
- L392 | TCO 비용 구조 반전(운영비) 도해(1452x1098) — 본문에 서술은 있으나 그림 자체의 세부 항목별 숫자는 이미지에만 | 「그림에서만」
- L505, L510, L514, L537, L541, L545 | Elon Musk 시나리오 관련 다수 차트(비용곡선·용량곡선·WACC표 등) — 본문 서술을 넘어서는 세부 수치는 이미지에만 존재 | 「그림에서만」
- L793 | PMAD 질량 스케일링 차트(1450x974) — 구체 숫자는 그림에만 | 「그림에서만」
- L801 | 추진 하드웨어 질량/비용 차트(1271x1374) — 그림에만 | 「그림에서만」
- L761, L763 | 냉각계 냄비(냉각루프) 세부 비용 차트 2개(2169x932, 2187x943) — 그림에만 | 「그림에서만」

## 확인 절차

아래 줄을 `sed -n 'NNNp' "input/clippings/To Boldly Go The Case for Space Datacenters.md"`로 재확인함(2회 배치 실행, 총 60개 이상 줄):
76, 100, 102, 106, 110, 118, 126, 178, 180, 190, 228, 252, 256, 262, 274, 280, 288, 292, 306, 314, 316, 326, 338, 340, 342, 346, 348, 376, 392, 398, 400, 412, 418, 420, 432, 442, 452, 454, 472, 492, 494, 502, 505, 506, 510, 512, 514, 516, 520, 522, 535, 537, 539, 541, 545, 555, 559, 601, 603, 617, 619, 645, 659, 661, 667-671, 673, 683, 685, 687, 691, 693, 697, 701, 703, 705, 710-721, 723, 725, 727, 729, 731, 733, 735, 745, 749, 753, 755, 761, 763, 774, 778, 780, 782, 787, 793, 797, 799, 801, 807, 816, 818, 824, 826, 828, 830, 836, 838, 846, 848, 858, 862, 864, 878, 880, 888, 890, 892, 898, 900, 908, 912, 914.

모두 실제 파일 내용과 일치함을 Bash sed 출력으로 확인했음. 우주(한글본)는 전문(1-592줄)을 Read로 통독했으며, 별도 신규 수치는 없고 영문 원문의 요약(mermaid 도해 포함)만 확인됨 — 인용 시 [우주 L...] 표기로 구분.
