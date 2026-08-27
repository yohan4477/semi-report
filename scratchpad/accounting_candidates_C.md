# 회계 처리 관찰 후보 — C갈래 (22편)

## 찾은 것

### 1. Meta의 "재생에너지 100%"는 회계상(PPA 정산) 수치일 뿐, 데이터센터가 실제로 밤에도 태양광 전기만 쓰는 것은 아니다

- **어느 회사·어느 항목**: Meta 데이터센터 / 재생에너지 사용률·탄소배출 감축 발표
- **원문**: `content/newsletter/ai_infra/power/[240314] AI 데이터센터 에너지 딜레마 - AI 데이터센터 공간 확보 경쟁.md` L773
- **인용**: "Meta는 재생에너지 장기구매계약(PPA)으로 2022년 배출량을 1,230만 톤 줄여, PPA가 없었다면 2,080만 톤이었을 배출량을 850만 톤으로 낮춤(약 59% 감소) → 하지만 이는 회계상의 "재생에너지 100%"일 뿐, 데이터센터가 실제로 밤에도 태양광 전기만 쓰는 것은 아님"
- **종류**: 인식 기준(계약상 재무 정산 vs 실제 물리적 전력 사용)
- **보충 인용** (같은 파일 L812, 다이어그램 결론 상자): "결과: 재무제표상으로는 '재생에너지 100%'이지만, 실제 전기는 그리드 믹스 그대로 사용"

### 2. 시놉시스 FY25 유기적 매출 성장률: Ansys 인수 연결을 빼면 발표치 15%가 실제로는 약 3%에 그친다

- **어느 회사·어느 항목**: 시놉시스(Synopsys) / 유기적(organic) 매출 성장률
- **원문**: `content/newsletter/semiconductors/[260521] EDA 시장 개관 - 시장 역학, 케이던스·시놉시스·지멘스, 중국 EDA의 부상.md` L346
- **인용**: "FY2026은 전환기 — Ansys가 가린 유기적(organic) 사업은 사실 둔화 중. FY25 Ansys 제외 유기적 매출은 15% 발표치 대비 실제 약 3%에 그쳤고, IP 매출은 4분기 중 3개 분기에서 전분기 대비 감소(13% CAGR 추세 이탈) — 인텔이 외부 파운드리 공정 기준(18A→18A-P)을 바꾸면서 시놉시스가 준비한 IP의 램프업 시점이 밀린 게 주요 원인"
- **종류**: 인수 연결로 인한 유기적 성장률 착시 (M&A 매출 편입이 본업 둔화를 가림)

## 관찰이 없는 파일

- `content/newsletter/ai_infra/power/[241014] 데이터센터 해부학 Part 1 - 전기 시스템.md` — 없음 (Capex/Opex·임대 용어 설명만 있고 공시 수치와 실제 경제의 어긋남 관찰은 없음)
- `content/newsletter/ai_infra/power/[250625] 기가와트급 AI 학습 부하 변동 - 전력망 정전을 부를 수 있는가.md` — 없음
- `content/newsletter/ai_infra/power/[251231] AI 랩들은 어떻게 전력난을 해결하는가 - 온사이트 가스 딥다이브.md` — 없음
- `content/newsletter/ai_infra/power/[260303] 데이터센터가 미국 가정의 전기요금을 올리는가.md` — 없음
- `content/newsletter/ai_infra/power/[260526] 800VDC 혁명 Part 1 - 전력 배전 아키텍처의 대전환.md` — 없음
- `content/newsletter/ai_infra/power/[260619] 2026년 미국 데이터센터 용량 절반 취소설은 틀렸다.md` — 없음
- `content/newsletter/ai_infra/power/[260626] 미국 전력망 제약 - 2028년까지 40GW+ 자가발전 데이터센터로 가는 길.md` — 없음
- `content/newsletter/ai_infra/power/[260816] PJM 모델링 오류로 날린 120억 달러 - 그리고 다시 반복하려 한다.md` — 없음 (용량시장 가격결정 구조상 「횡재(windfall)」는 있으나 회계 처리 선택 문제가 아니라 경매 설계 문제)
- `content/newsletter/ai_models/[260803] Kimi K3 아키텍처 해부 - 압축 메모리, 깊이 방향 어텐션, 잠재 전문가 라우팅.md` — 없음
- `content/newsletter/ai_models/[260821] 오픈 모델은 정말 따라잡고 있는가 - 세 시대로 본 오픈-클로즈드 격차.md` — 없음
- `content/newsletter/ai_models/agents/[260206] Claude Code, 에이전트 시대의 변곡점.md` — 없음 ("TSMC vs 엔테그리스 매출총이익률 비교 차트(인수 관련 프로포마 조정 반영)"라는 언급이 있으나 어떤 수치가 어떻게 달라 보이는지 설명이 없어 제외)
- `content/newsletter/ai_models/agents/[260425] 코딩 어시스턴트 해부 - 토큰을 더 주세요.md` — 없음
- `content/newsletter/ai_models/agents/[260528] 재미로 미스컴파일 찾기 - 오후 한나절에 1만 달러를 쓰는 법.md` — 없음
- `content/newsletter/ai_models/rl/[250609] 강화학습(RL) 스케일링 - 환경, 보상 해킹, 에이전트, 데이터 스케일링.md` — 없음
- `content/newsletter/ai_models/rl/[260107] RL 환경과 과학을 위한 RL - 데이터 파운드리와 멀티 에이전트 아키텍처.md` — 없음
- `content/newsletter/ai_models/rl/[260616] RL 시스템, 틈새를 조심하라 - 학습기와 생성기 처리량 맞추기.md` — 없음 (TCO·감가상각·WACC는 비용 산출 방법론일 뿐, 공시 수치와 실제의 어긋남 관찰이 아님)
- `content/newsletter/robotics/[260608] Unitree의 믿기 힘든 성장 궤적, 여전히 저평가됐다.md` — 없음 (마진 개선은 실제 원가 절감에 따른 것으로 서술되며 회계 처리 선택 문제가 아님)
- `content/newsletter/semiconductors/[260108] 애플-TSMC - 현대 반도체를 만든 파트너십.md` — 없음 (맥 총마진 확대도 자체 실리콘 전환에 따른 실제 원가 절감으로 서술됨)
- `content/newsletter/semiconductors/[260512] EDA 입문 - RTL에서 실리콘까지.md` — 없음
- `content/newsletter/semiconductors/process/[260614] SMIC N+3 금속 배선 간격, 인텔 18A보다 좁을까 - 화웨이 기린 9030 해부.md` — 없음

읽은 파일 22편 / 관찰 2건
