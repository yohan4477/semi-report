# 주석 확인 — 알파벳 구매약정 · 엔비디아 부채·증권 태그

## 1. 알파벳 — LongTermPurchaseCommitmentAmount 7,070억 달러

- **출처**: 10-Q, FY2026 Q2(회계기간 2026-01-01~2026-06-30, 대차대조표 기준일 2026-06-30), accession 0001652044-26-000071, https://www.sec.gov/Archives/edgar/data/1652044/000165204426000071/goog-20260630.htm — 재무제표 Note 10 "Commitments and Contingencies"
- 비교용: 직전 10-Q, FY2026 Q1(2026-01-01~2026-03-31), accession 0001652044-26-000048, https://www.sec.gov/Archives/edgar/data/1652044/000165204426000048/goog-20260331.htm

**기간 값인가 잔액인가 — 문서가 안 밝힘(정확히는: "As of [기준일]"로 서술된 잔액 문장이다)**

Note 10 원문 문장은 duration(기간 누적)이 아니라 특정 시점 기준 문장으로 되어 있다. Q2 10-Q:

> "As of June 30, 2026, expected future fixed or guaranteed commitments under these agreements were $707.0 billion, the significant majority of which related to long-term supply agreements."

번역: 2026년 6월 30일 기준, 이 계약들에 따른 향후 확정 또는 보증 약정액은 7,070억 달러였고, 그 압도적 다수는 장기 공급계약과 관련되어 있다.

Q1 10-Q도 같은 형식이다:

> "As of March 31, 2026, expected future fixed or minimum guaranteed commitments under these agreements were $232.7 billion."

번역: 2026년 3월 31일 기준, 이 계약들에 따른 향후 확정 또는 최소 보증 약정액은 2,327억 달러였다.

두 문장 모두 "As of [기준일]"로 시작해 그 시점에 남아 있는 약정 총액을 말한다 — "그 분기에 새로 체결한 금액"이라는 서술은 어느 10-Q에도 없다. 다만 XBRL 상 이 태그는 `start`(2026-01-01)~`end`(기말) 컨텍스트로 잡혀 있어 회계연도 시작부터의 duration으로 모델링되어 있다. 즉 **문장은 잔액을 말하는데 XBRL 컨텍스트는 기간값 구조를 쓰고 있다** — 이 불일치 자체가 문서에 설명되어 있지 않다. "그 기간에 새로 맺은 약정"이라는 해석은 주석 문장이 뒷받침하지 않는다.

**무엇에 대한 약정인가**

> "We have contractual obligations from contracts with remaining terms greater than one year primarily consisting of certain long-term supply agreements to secure future production capacity for technical infrastructure and inventory components. In addition, we have commitments for certain energy service agreements to secure energy for data center usage, and certain content licensing agreements."

번역: 잔여 계약기간 1년 초과인 계약에서 발생하는 계약상 의무로, 주로 기술 인프라와 재고 구성요소의 미래 생산능력을 확보하기 위한 장기 공급계약으로 이루어져 있다. 이 외에 데이터센터 사용을 위한 에너지를 확보하는 에너지 서비스계약, 콘텐츠 라이선스 계약에 대한 약정도 있다.

세 항목(장기 공급계약·에너지 take-or-pay·콘텐츠 라이선스) 중 "significant majority"(압도적 다수)가 장기 공급계약(기술 인프라·재고)이라고 Q2 문장이 명시한다.

**Unrecorded…756억과의 차이 — 다른 주석, 다른 대상이다**

`UnrecordedUnconditionalPurchaseObligationBalanceSheetAmount` 756억 달러(2026-03-31)는 Note 10이 아니라 **Note 4 "Leases"**에서 나온 값이다(Q1 10-Q, 같은 accession 0001652044-26-000048). 원문:

> "As of March 31, 2026, we have entered into leases primarily related to data centers that have not yet commenced with future lease payments of $75.6 billion that are not yet recorded. These leases will commence between 2026 and 2031 with non-cancelable lease terms primarily between one and 25 years."

번역: 2026년 3월 31일 기준, 아직 개시되지 않은 데이터센터 관련 리스를 체결했으며 그 향후 리스료는 756억 달러로 아직 (재무제표에) 기록되지 않았다. 이 리스들은 2026~2031년 사이에 개시되며 비해지 리스기간은 대부분 1~25년이다.

직전 분기(2025-09-30, 10-Q accession 0001652044-25-000091)에도 같은 문구가 "$42.6 billion"으로 반복된다:

> "As of September 30, 2025, we have entered into leases primarily related to data centers that have not yet commenced with future lease payments of $42.6 billion, including a purchase option considered reasonably certain to be exercised, that are not yet recorded on our Consolidated Balance Sheet."

즉 "Unrecorded…" 태그가 붙는 숫자는 Note 10의 공급·에너지·콘텐츠 약정(707.0억/232.7억)과는 별개로, **아직 개시되지 않아 리스부채로 아직 잡히지 않은 데이터센터 리스의 미래 리스료**다. 참고: 이 대응은 달러 금액이 정확히 일치하는 것으로 확인했다 — 본문 어디에도 "unconditional"이라는 단어 자체는 나오지 않는다(2026 Q1·Q2 10-Q 전체 텍스트에서 "unconditional" 0건 검색됨). XBRL 태그명은 제출사가 붙이는 것이라 화면에 보이는 라벨과 반드시 같은 단어를 쓰지는 않는다.

**급증 설명(232.7억→707.0억, 한 분기) — 문서에 없음**

Q2 10-Q Note 10, MD&A(Liquidity and Capital Resources) 어디에도 "왜 이번 분기에 늘었는지"를 설명하는 문장이 없다. "entered into new long-term supply agreement(s)" 류의 표현, 전분기 대비 증감 설명 문장 모두 검색되지 않았다(0건). MD&A는 총액($811.0 billion, 단기 $200.7 billion 포함 — 이는 Note 10 약정에 재무보증·에너지 백스톱까지 합친 상위 지표로 Note 10 단독 숫자와 다르다)만 제시할 뿐 변동 사유는 밝히지 않는다.

## 2. 엔비디아 — LongTermDebtFairValue 314억 달러

- **출처**: 10-Q, FY2027 Q2(회계기간 종료 2026-07-26), accession 0001045810-26-000075, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm — 재무제표 Note 9 "Debt"

**주의 — 태그가 "2025-01-26에 처음 나옴"이 아니라 그 시점 값이 7.2억(72억)이 아니라 72억 달러였다는 뜻**

`companyconcept` API를 직접 조회한 결과, `LongTermDebtFairValue`는 2025-01-26(FY2025 10-K) 시점부터 이미 존재했고 값은 **72억 달러**였다. 이후 분기별로 72억→74억→76억→75억(2026-01-25)으로 완만히 움직이다가, **가장 최근 분기인 2026-07-26에 314억 달러로 급증**했다. 즉 "314억 달러"는 2026-07-26 시점 값이지 태그가 처음 나온 시점의 값이 아니다.

**어떤 부채의 공정가치인가 / 장부금액과의 차이 / 신규 조달 여부**

Note 9 - Debt (표 제목: "Jul 26, 2026 / Jan 25, 2026", 단위 백만 달러) 표는 만기별 선순위무담보사채(Notes Due 2026~2060) 잔액을 나열한 뒤 다음과 같이 마무리한다.

> "Unamortized debt discount and issuance costs (134) (32) Net carrying amount $33,366 $8,468 Less short-term portion (1,000) (999) Total long-term portion $32,366 $7,469 In June 2026, we issued an aggregate of $25.0 billion of senior unsecured notes across seven tranches for general corporate purposes. As of July 26, 2026, and January 25, 2026, the estimated fair value of debt was $31.4 billion and $7.5 billion, respectively. The estimated fair values are based on Level 2 inputs."

번역: 미상각 부채할인 및 발행비용 (134) (32). 순장부금액 333.66억 달러 / 84.68억 달러. 단기 부분 차감 (10.00억) (9.99억). 장기 부분 합계 323.66억 달러 / 74.69억 달러. 2026년 6월, 우리는 일반 기업 목적으로 7개 트랜치에 걸쳐 총 250억 달러의 선순위무담보사채를 발행했다. 2026년 7월 26일과 2026년 1월 25일 기준 부채의 추정 공정가치는 각각 314억 달러와 75억 달러였다. 공정가치 추정은 레벨2 투입값에 기반한다.

- **장부금액(순장부금액)**: 333.66억 달러(2026-07-26) — 공정가치 314억 달러보다 크다.
- **새로 조달한 것인가**: 그렇다. 2026년 6월에 7개 트랜치로 총 250억 달러의 신규 선순위무담보사채를 발행했다고 명시되어 있다(표에서도 "4.25% Notes Due 2028" 35억, "4.35% Notes Due 2029" 35억, "4.50% Notes Due 2031" 40억, "4.75% Notes Due 2033" 35억, "4.95% Notes Due 2036" 40억 등 신규 트랜치가 Jan 25, 2026 열에는 없다가 Jul 26, 2026 열에만 나타난다).

## 3. 엔비디아 — DebtSecuritiesCurrent 341억 달러 / MarketableSecuritiesCurrent 단절

- **출처**: 10-Q, FY2027 Q2(2026-07-26), accession 0001045810-26-000075 — 재무제표 Note 5 "Cash Equivalents and Marketable Securities"
- 비교: 10-K FY2026(2026-01-25), accession 0001045810-26-000021, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- 비교: 10-Q FY2026 Q3(2025-10-26), accession 0001045810-25-000230, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm

**둘은 범위가 다른 게 아니라 표 형식이 바뀐 것 — 회사가 그렇게 밝혔다고까지는 말하지 않았지만 표 자체가 증거다**

2025-10-26(Q3 FY2026) 10-Q, Note 5 요약표는 "Reported as" 열이 "Cash Equivalents"와 "Marketable Securities" 단 두 개뿐이고, 이 "Marketable Securities" 열은 채무증권과 지분증권을 합친 값이다:

> "Total $54,580 $373 $(1) $58,821 $9,699 $49,122" (표 열: Amortized Cost / Unrealized Gain / Unrealized Loss / Estimated Fair Value / Reported as Cash Equivalents / Reported as Marketable Securities)

이 $49,122백만 = 491.22억 달러가 채무증권(21,555+21,439+2,218+104+41=45,357\*) + 지분증권(3,869\*) 합계다(\*표에서 두 성격을 분리하지 않고 "Marketable Securities" 한 열로 합산해서 낸다).

2026-07-26(Q2 FY2027) 10-Q, 같은 Note 5 요약표는 "Reported as" 열이 4개로 늘었다 — "Cash Equivalents / Marketable Debt Securities / Marketable Equity Securities / Other Assets":

> "Total $55,541 $8 $(56) $103,233 $21,350 $34,143 $42,783 $4,957"

이 표에서 "Marketable Debt Securities" 열 합계가 **$34,143백만 = 341.43억 달러**로 XBRL `DebtSecuritiesCurrent`(2026-07-26) 값과 정확히 일치한다. 같은 표 형식이 2026-01-25(10-K FY2026) 시점에도 쓰였고 그때는 이 열 합계가 $39,065백만 = 390.65억 달러였다 — 이 값도 `DebtSecuritiesCurrent`(2026-01-25) XBRL 값과 정확히 일치한다.

즉 2025-10-26까지는 채무증권+지분증권을 "Marketable Securities" 한 열로 합쳐 냈고(→ `MarketableSecuritiesCurrent` 태그), 2026-01-25 10-K부터는 같은 표를 "Marketable Debt Securities"와 "Marketable Equity Securities" 두 열로 쪼개 냈다(→ `DebtSecuritiesCurrent` 태그 신설). 대차대조표 본문 caption 자체는 바뀌지 않았다 — 10-K FY2026 대차대조표에는 여전히 "Marketable securities $51,951"(=채무 39,065+지분 12,886 합산) 한 줄로만 나온다. 즉 **분리는 노트(Note 5)의 세부 표에서만 일어났고, 대차대조표 caption에서는 일어나지 않았다.**

**회사가 표시 방법을 바꿨다고 밝혔나 — 이 특정 변경에 대해서는 밝히지 않음**

10-K FY2026 본문에서 "reclassified"를 검색하면 다음 문장이 나오지만, 이는 비상장주식(non-marketable equity securities)을 "Other assets"에서 대차대조표 별도 항목으로 옮긴 것에 대한 설명이지 Note 5 표의 채무/지분 분리에 대한 설명이 아니다:

> "Certain prior fiscal year balances have been reclassified to conform to the current fiscal year presentation. Non-marketable equity securities, previously presented within other assets, were reclassified to be presented separately on our consolidated balance sheets and had no impact to total assets or consolidated statement of cash flows."

번역: 일부 전기 잔액은 당기 표시방법에 맞춰 재분류되었다. 이전에 기타자산 내에 표시되던 비상장 지분증권은 연결대차대조표에 별도 항목으로 재분류되었으며, 총자산과 연결현금흐름표에는 영향이 없었다.

Note 5 표를 "Marketable Securities" 한 열에서 "Marketable Debt Securities / Marketable Equity Securities" 두 열로 바꾼 것 자체를 명시적으로 설명하는 문장은 두 필사(10-K FY2026, 10-Q Q2 FY2027) 어디에도 없었다("reclassif" 검색 6건 모두 위 비상장증권 건이거나 무관한 문맥).

## 못 찾은 것

- 알파벳 Note 10 약정 707.0억 달러가 특정 카운터파티(예: 특정 클라우드·전력 공급사)별로 어떻게 구성되는지에 대한 세부 내역 — 원문에 없음(총액과 성격 서술만 있음)
- Note 5 표의 채무/지분 분리를 회사가 "표시방법 변경"이라고 명시적으로 부른 문장 — 못 찾음(표 자체의 열 구성 변화로만 확인)

읽은 문서 5건 (알파벳 10-Q FY2026 Q2·Q1, 알파벳 10-Q FY2026 Q3(2025-09-30), 엔비디아 10-Q FY2027 Q2, 엔비디아 10-K FY2026, 엔비디아 10-Q FY2026 Q3 — 총 5개 파일링 6개 조회)
