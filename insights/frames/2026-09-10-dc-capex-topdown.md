---
title: 하이퍼스케일러 자본지출 하향 모델 — 다른 대화에서 받은 틀
date: 2026-09-10
kind: frame
source: scratchpad/capex_frame_xlsx.md
url: claude.ai 공유 대화 https://claude.ai/share/627424cd-9b04-49d5-a730-dbc73e710216 (2026-09-10 열람). 엑셀 세 개를 사용자가 따로 줬다
asked: 「ai dc capex modeling」 — 범위는 하이퍼스케일러 전체 자본지출 추정, 용도는 예산·자금조달 계획, 산출물은 엑셀 모델
model: claude (그 대화의 모델). 우리 저장소의 원문은 안 줬다 — 회사 공시와 웹 검색으로 세운 값이다
warn: **검증 안 된 원본이다.** 여기 숫자는 우리 코퍼스 대조를 안 거쳤다. 카드나 보고서 본문으로 옮길 때는 우리 원문이 받쳐 주는 것만 옮기고, 아닌 것은 「프레임 값」이라고 밝힌다.
named: 업계 집계치 7,250억 달러 — 2차 출처 두 곳이 받쳐 준다. 그 대화 화면에는 출처가 없었고 사용자가 뒤에 목록을 줬다.
xlsx: 엑셀 두 개를 받았다 — AI_DC_Capex_Big4.xlsx 와 AI_DC_Capex_Big4_HBM.xlsx. 시트와 값은 scratchpad/capex_frame_xlsx.md 에 옮겼다
---

## 받은 그대로 — 모델 구조

모델 구조는 Assumptions → Capacity → Capex → Funding → Sensitivity, 앞에 Summary 시트가 있어요. 노란 셀만 바꾸면 전부 재계산됩니다.

핵심 로직:

- Capex = 신규 GW × $M/MW (GW×$M/MW = $B라 환산 불필요). 시설·전력·네트워킹·AI IT·일반 IT로 분해하고, AI IT는 GPU/MW × GPU당 단가로 계산
- 시설·전력은 차년도 가동분의 50% 선지출, IT는 5년 갱신 주기로 리프레시 capex 별도 반영
- Funding은 Sources(OCF·부채·리스/JV) vs Uses(capex·주주환원·상환) → 기말 현금 → 최소 현금 대비 추가 조달 필요액 자동 산출
- Sensitivity는 GPU 단가 × 신규 용량 배수 5×5 그리드

예시 가정 기준으로는 5년 누적 capex 약 $1.17T, 2029년부터 조달 갭이 발생하는 구조라 부채·리스 비율 레버 조정을 바로 테스트해볼 수 있어요. 숫자는 전부 예시이니 실제 회사 공시치로 교체가 필요합니다.

## 받은 그대로 — 회사마다 달라야 하는 이유

맞아요. 지금 파일은 "하이퍼스케일러 한 곳" 템플릿이라 회사별 차이가 반영 안 돼 있어요. 실제로는 이런 게 다 달라요:

- AI 비중·용량: MSFT/META는 GPU 비중 높고, AMZN은 자체 칩(Trainium)·물류 capex 섞임, GOOGL은 TPU라 $/MW가 다름
- 조달 구조: META는 JV·사모채(Hyperion 등), ORCL은 순차입 의존, MSFT/GOOGL은 OCF로 대부분 소화, AMZN은 리스 비중 큼
- 회계연도·공시 단위: MSFT는 6월 결산, 금융리스 포함 여부도 제각각

그래서 회사별 시트(각자 가정 블록)를 만들고 합산 시트로 업계 총 capex를 보는 구조로 확장하는 게 맞아요.

## 받은 그대로 — 빅4 반영값 (7월 말 2분기 실적 콜 기준)

회사별 시트(동일 구조) + Consolidated 합산 + README로 구성했어요. 7월 말 2분기 실적 콜 기준 반영값:

- MSFT: CY2026 ≈ $175B — FY27부터 DC 내용연수를 15→25년으로 바꾸면서 금융리스가 운용리스로 재분류돼 capex가 줄어 보이지만, 그 외 CY2026 투자 계획은 변동 없음. 분기 capex $41B 중 약 2/3가 GPU·CPU 등 단기자산. (Microsoft)
- GOOGL: 2026 가이던스 $195~205B(종전 $180~190B), 2027년에도 큰 폭 증가 예정. 2분기 $44.9B 중 서버 60%/DC 40%, FCF 첫 마이너스. (Investing.com)
- AMZN: 2026 현금 capex 약 $220B — 메모리 가격 상승으로 $200B에서 상향, 그래도 수요를 못 맞추는 상황. 장기부채가 6개월 만에 ~2배($129B). (Yahoo Finance)
- META: 2026 capex(금융리스 원금 포함) $130~145B. 2분기 capex가 OCF의 98%를 먹어 FCF ~$0.8B, JV(BlackRock 엘패소, Hyperion)·부채 의존. (Q4cdn)

회사별로 다르게 잡은 레버: capex 정의(리스 포함 여부), 서버 vs DC 비중, 리스/JV 조달 비율, OCF 마진, 주주환원, 부채 발행. 2027E 이후 성장률·조달 가정은 전부 노란 셀이니 조정하세요.

빨간 글씨로 표시한 2025A 매출·현금·부채는 근사치라 10-K로 교체가 필요하고, 합산 capex(2026E ~$730B)는 업계 집계치 $725B와 대체로 맞습니다.

## 받은 엑셀에서 읽은 값 — 2026년 열

전사는 `scratchpad/capex_frame_xlsx.md` 가 정본이다. 셀 주소를 함께 적는다.

- 빅4 합산 자본지출 2025년 412십억 달러(4,120억), 2026년 732.5십억 달러(7,325억) (Consolidated!B6·C6)
- 그 가운데 서버·칩 444.875십억, 데이터센터·전력·네트워크 287.625십억 (Consolidated!C7·C8)
- 5년 합계(2026~2030년) 4976.6십억 달러 (Consolidated!H6)
- 자본지출이 매출에서 차지하는 몫 37.7퍼센트, 영업현금흐름 대비 1.13배 (Consolidated!C12·C13)
- 잉여현금흐름 2026년 마이너스 13.3십억, 추가 조달 필요액 2028년 29.65십억 (Consolidated!C20·E22)
- 리스와 합작 조달 71.675십억, 신규 부채 발행 150십억 (Consolidated!C17·C18)
- AI 가속기 자본지출 311.775십억 달러, 대수 14.3788백만 개 (HBM_Demand!C6·C7)
- HBM 수요 2.979엑사바이트, 금액 31.42십억, 블렌드 기가바이트당 10.55달러 (HBM_Demand!C8·C11·C12)
- HBM 이 가속기 자본지출에서 차지하는 몫 10.1퍼센트, 글로벌 HBM 시장 57.13십억 (HBM_Demand!C13·C25)
- 시스템 평균판매가격 — 블랙웰 40천 달러, 구글 TPU 12천, AWS 트레이니엄 8천 (HBM_Inputs!C6·C9·C10)
- 칩당 HBM 용량 — 블랙웰 블렌드 240GB, 루빈 288GB, TPU 216GB (HBM_Inputs!B6·B7·B9)
- 마이크로소프트 데이터센터 내용연수 15년에서 25년으로 변경 (실적 콜)
- 시설·전력은 차년도 가동분의 50퍼센트 선지출, IT 갱신 주기 5년 (첫 판 모델 가정)

## 1차 출처 — 회사 공시와 실적 콜 (사용자가 준 목록 그대로)

- 마이크로소프트 FY26 4분기 실적 콜, 2026-07-29 — https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q4
  4분기 자본지출 411억 달러(약 3분의 2가 단기자산), 금융리스 56억, CY2026 자본지출 약 1,750억(데이터센터 내용연수를 15년에서 25년으로 바꾸며 금융리스가 운용리스로 재분류, 그 외 계획 불변), FY27 자본지출 전년 대비 증가·잉여현금흐름 흑자 유지, FY26 매출 3,310억, 4분기 영업현금흐름 554억, FY26 주주환원 430억 이상, 커머셜 잔여이행의무 6,780억
- 알파벳 2026년 2분기 실적 콜, 2026-07-22 — https://abc.xyz/investor/events/event-details/2026/2026-Q2-Earnings-Call-2026-GgTAq7Is0z/default.aspx (트랜스크립트 https://www.investing.com/news/transcripts/earnings-call-transcript-alphabet-beats-q2-2026-estimates-shares-fall-on-capex-surge-93CH-4807140)
  2026년 자본지출 1,950억~2,050억(종전 1,800억~1,900억), 2027년 큰 폭 증가, 2분기 자본지출 449억(서버 약 60퍼센트·데이터센터와 네트워크 약 40퍼센트), 2분기 매출 1,198억, 클라우드 백로그 5,140억, 2분기 잉여현금흐름 마이너스 59억, 현금과 유가증권 2,425억, 장기부채 982억
- 메타 2026년 2분기 실적 콜 트랜스크립트, 2026-07-29 — https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Earnings-Call-Transcript.pdf
  2026년 자본지출 1,300억~1,450억(금융리스 원금상환 포함), 3분기 매출 가이던스 610억~640억. 보조 https://www.cnbc.com/2026/07/29/meta-q2-earnings-report-2026.html (엘패소 140억 블랙록 합작, 하이페리온 500억 초과). 2분기 자본지출 311억·영업현금흐름 319억·현금 903억·부채 837억·상반기 순부채발행 249억은 2차 정리 https://www.digitalapplied.com/blog/meta-q2-2026-earnings-ad-strength-capex-selloff
- 아마존 2026년 2분기 실적 콜, 2026-07-30 — https://finance.yahoo.com/quote/AMZN/earnings/AMZN-Q2-2026-earnings_call-657334.html / https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html
  2026년 현금 자본지출 약 2,200억(종전 약 2,000억, 메모리 가격 상승분), 2분기 자본지출 531억, 매출 2,006억, 최근 12개월 잉여현금흐름 마이너스 76억, 최근 12개월 자본지출 1,690억, AWS 백로그 4,960억, 장기부채 1,289억(6개월 새 약 두 배)

## 2차 출처 — 집계와 교차검증

- 빅4 2025년 자본지출 합산 약 4,100억, 2026년 7,250억 이상 — https://finance.yahoo.com/sectors/technology/article/meta-microsoft-amazon-and-alphabet-are-about-to-spend-a-shocking-amount-of-money-to-dominate-the-ai-era-115359575.html · https://www.cnbc.com/2026/07/28/hyperscalers-face-higher-capex-scrutiny-after-alphabet-report-panned.html
- 자본지출 정의 차이(마이크로소프트는 금융리스 포함, 메타는 리스 원금 포함, 구글과 아마존은 현금 유형자산만) — https://epoch.ai/data-insights/hyperscaler-capex-trend
- 2026년 하이퍼스케일러 자본지출 7,000억 초과 분석, 메타 합작 조달 약 800억 추적 — https://www.tmtfinance.com/intel/2026-hyperscaler-capex-tops-us700bn-analysis

## HBM 출처

- 카운터포인트 2026년 2분기 HBM 매출 점유율 SK하이닉스 50퍼센트·삼성 33퍼센트·마이크론 18퍼센트 — https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share · https://en.sedaily.com/finance/2026/09/03/samsung-doubles-hbm-market-share-to-33-percent-narrowing
- 트렌드포스 2026-06-02 — 2026년 ASIC 칩당 HBM 96/192GB 에서 216/288GB 로, 루빈은 전 세대와 비슷, 2027년 루빈 울트라 384GB, 2027년 HBM 계약가 「수 배」 상승 전망, 2027년 HBM 웨이퍼 비중 30퍼센트 — https://www.trendforce.com/presscenter/news/20260602-13074.html
- 스택 가격 추정(HBM3E 36GB 약 300달러, HBM4 36GB 약 550달러) — https://siliconanalysts.com/tools/hbm-analysis · HBM4 점유율 전망 https://siliconanalysts.com/analysis/hbm4-market-share-race-2026
- 칩별 HBM 용량(H100 80GB, H200 141GB, B200 192GB, 루빈 288GB HBM4) — https://introl.com/blog/ai-memory-supercycle-hbm-2026
- 트렌드포스 2026년 HBM 수요 70퍼센트 증가 전망(간접 인용) — https://dramwatch.com/

## 출처 없는 가정값 — 모델 작성자 추정, 검증 필요

- 2025년 실적 매출·영업현금흐름·현금·부채 근사치, 마이크로소프트 회계연도에서 역년으로 환산한 2025년 약 1,180억
- 2027년 이후 자본지출 성장률, 영업현금흐름 마진, 부채 발행과 상환, 주주환원, 리스와 합작 조달 비율, 최소 현금
- 서버·칩 비중(구글 60퍼센트는 공시 기반, 나머지 추정), AI 가속기 비중(마이크로소프트 70·구글 75·아마존 60·메타 80퍼센트)
- 가속기 시스템 평균판매가격(칩당 천 달러), 회사별 칩 믹스와 세대 전환 속도, 블랙웰 블렌드 240GB
- HBM 기가바이트당 가격 연도별 경로(HBM3E 10에서 13달러, HBM4 15에서 20달러, HBM4E 22에서 24달러 뒤 하락), 스택 용량 36에서 48GB
- 빅4의 세계 HBM 수요 비중 55퍼센트, 공급사 점유율 2027년 이후 경로

## 상충 사항

- 마이크로소프트 FY27 자본지출 — 일부 2차 소스(TradingKey, ValueAddVC)는 2,550억~2,600억 가이던스를 말하지만 공식 트랜스크립트에는 「전년 대비 증가」만 있다. 공식 콜을 먼저 본다
- 마이크로소프트 2025년 역년 자본지출 — 소스마다 890억에서 1,180억으로 갈린다. 회계연도 분기를 어떻게 합치느냐의 차이다. 10-Q 로 다시 확인해야 한다

## 안 가져온 것

- 업계 집계치 725십억 달러 — 출처가 안 적혀 있다
- 엑셀 파일 자체 — 시트 안 수식과 노란 셀 값은 이 대화 화면에 안 보인다
- 5년 누적 1.17조 달러 — 「전부 예시」라고 밝힌 첫 버전의 값이라 회사별 값으로 갈아 끼운 뒤에는 안 맞는다
- 회사별 매출·현금·부채 2025년 실적치 — 그 대화가 「근사치라 10-K로 교체 필요」라고 적었다
