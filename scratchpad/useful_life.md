# 유형자산 내용연수 — 여섯 회사

자료: SEC EDGAR 공개 API(data.sec.gov, www.sec.gov/Archives), 각 사 최신 10-K "Summary of Significant Accounting Policies" 중 Property and Equipment 대목.

## 요약 표

| 회사 | 회계연도 | 서버 | 네트워크 장비 | 건물 | 바꾼 이력 |
|---|---|---|---|---|---|
| 알파벳 (GOOGL) | FY2025(2025-12-31 마감) | 6년(네트워크 장비와 통합 표기) | 6년(서버와 통합 표기) | 7~40년(데이터센터·오피스) | 문서에 없음 |
| 마이크로소프트 (MSFT) | FY2026(2026-06-30 마감) | 2~6년(네트워크 장비와 통합 표기) | 2~6년(서버와 통합 표기) | 5~15년(건물·개선) | 문서에 없음 |
| 엔비디아 (NVDA) | FY2026(2026-01-25 마감) | 못 찾음(별도 항목 없음, "장비·컴퓨트 하드웨어·소프트웨어"로 통합해 2~7년) | 못 찾음(위와 동일 항목에 통합) | 30년 이하 | 문서에 없음 |
| 아마존 (AMZN) | FY2025(2025-12-31 마감) | 5~6년(네트워킹 장비와 통합 표기) | 5~6년(서버와 통합 표기) | 40년 이하(잔여 내용연수 중 짧은 쪽) | **있음** — 2024-01-01 서버 5→6년, 2025-01-01 서버·네트워킹장비 일부 6→5년(AI·기술발전 가속 사유). 2025년 변경 효과: 감가상각비 +14억달러, 순이익 −10억달러(EPS −0.10달러), AWS 부문에 주로 영향 |
| 메타 (META) | FY2025(2025-12-31 마감) | 5~5.5년(네트워크 자산과 통합 표기) | 5~5.5년(서버와 통합 표기) | 25~30년 | **있음** — 2025-01-01부터 대다수 서버·네트워크 자산 내용연수를 5.5년으로 연장. 2025년 효과: 감가상각비 −29.2억달러, 순이익 +25.9억달러(희석 EPS +1.00달러) |
| 애플 (AAPL) | FY2025(2025-09-27 마감) | 못 찾음(연수 자체를 공개하지 않음) | 못 찾음 | 못 찾음(자산군만 열거, 연수 비공개) | 문서에 없음(애초에 연수를 공개하지 않으므로 변경 이력도 없음) |

## 회사별 근거

### 알파벳 (GOOGL)

- **출처**: 10-K FY2025, accession 0001652044-26-000018, https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm
- **인용**: "We depreciate data center and office buildings over periods of seven to 40 years. We depreciate servers and network equipment generally over a period of six years. We depreciate corporate and other assets over periods of two to 25 years. We depreciate leasehold improvements over the shorter of the remaining lease term or the estimated useful lives of the assets."
- **번역**: 데이터센터·오피스 건물은 7~40년, 서버·네트워크 장비는 대체로 6년, 기업용·기타 자산은 2~25년에 걸쳐 감가상각한다. 리스개량자산은 남은 리스 기간과 추정 내용연수 중 짧은 쪽으로 상각한다.
- **바꾼 이력**: 문서에 없음. 다만 "We assess the reasonableness of the useful lives of our property and equipment periodically or when events indicate a change is necessary... Any change in the estimated useful lives is recognized on a prospective basis."(내용연수를 주기적으로 재평가하며 변경 시 전진적용한다)는 일반 정책 문장만 있고, 이번 FY2025 10-K에는 구체적인 변경 연도·손익 영향 수치가 나오지 않는다.

### 마이크로소프트 (MSFT)

- **출처**: 10-K FY2026(회계연도 2026-06-30 마감), accession 0001193125-26-323660, https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm
- **인용**: "The estimated useful lives of our property and equipment are generally as follows: software developed or acquired for internal use, three years; servers and network equipment, two to six years; buildings and improvements, five to 15 years; leasehold improvements, three to 15 years; and furniture and equipment, one to 10 years. Land is not depreciated."
- **번역**: 유형자산 추정 내용연수는 대략 다음과 같다 — 사내 개발·취득 소프트웨어 3년, 서버·네트워크 장비 2~6년, 건물·개량 5~15년, 리스개량자산 3~15년, 가구·비품 1~10년. 토지는 상각하지 않는다.
- **바꾼 이력**: 문서에 없음. 이번 FY2026 10-K 본문에서 "change in accounting estimate", "shorten" 등 서버·네트워크 장비 내용연수 변경을 다루는 문장은 찾지 못했다(마이크로소프트가 과거 다른 회계연도 10-K에서 이 항목을 바꾼 적이 있다는 외부 보도가 있으나, 이번에 받은 FY2026 10-K 본문 자체에는 그 이력이 없다).

### 엔비디아 (NVDA)

- **출처**: 10-K FY2026(회계연도 2026-01-25 마감), accession 0001045810-26-000021, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm
- **인용**: "Depreciation of property and equipment is computed using the straight-line method based on the estimated useful lives of the assets of two to seven years... The estimated useful lives of our buildings are up to thirty years." 유형자산 세부 표에서는 "Equipment, compute hardware, and software" 한 줄에 "2 - 7"(년)만 표기되어 있다.
- **번역**: 유형자산 감가상각은 정액법으로 2~7년의 추정 내용연수에 걸쳐 계산한다. 건물 추정 내용연수는 최대 30년이다.
- **바꾼 이력**: 문서에 없음.
- **비고**: 엔비디아는 구글·아마존·메타·마이크로소프트와 달리 대규모 서버 함대를 직접 운영하는 하이퍼스케일러가 아니라 반도체 설계·판매 기업이어서, 10-K에 "servers"를 별도 자산군으로 구분해 내용연수를 공시하지 않는다. "장비·컴퓨트 하드웨어·소프트웨어"로 뭉뚱그려 2~7년만 밝힌다.

### 아마존 (AMZN)

- **출처**: 10-K FY2025, accession 0001018724-26-000004, https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm
- **인용(내용연수 표)**: "The estimated useful lives as of December 31, 2025, are as follows: Property and equipment Estimated useful life Buildings Lesser of forty years or the remaining life of the underlying building Servers and networking equipment Five to six years (1) Heavy equipment Ten to thirteen years (2) Other equipment Three to ten years. (1) Effective January 1, 2024, we changed our estimate of the useful lives for our servers from five to six years, and effective January 1, 2025, we changed our estimate of the useful lives of a subset of our servers and networking equipment from six to five years. (2) Ten years prior to January 1, 2025."
- **인용(손익 영향)**: "Effective January 1, 2025 we changed our estimate of the useful lives of a subset of our servers and networking equipment from six years to five years. The shorter useful lives are due to the increased pace of technology development, particularly in the area of artificial intelligence and machine learning. The effect of this change in estimate for the year ended December 31, 2025... was an increase in depreciation and amortization expense of $1.4 billion and a reduction in net income of $1.0 billion, or $0.10 per basic share and $0.10 per diluted share, which primarily impacted our AWS segment."
- **번역**: 2025년 12월 31일 기준 추정 내용연수는 건물은 40년 또는 잔여 건물수명 중 짧은 쪽, 서버·네트워킹 장비는 5~6년, 중장비는 10~13년, 기타 장비는 3~10년이다. 2024년 1월 1일부로 서버 내용연수를 5년에서 6년으로 늘렸고, 2025년 1월 1일부로는 서버·네트워킹장비 일부의 내용연수를 다시 6년에서 5년으로 줄였다. 인공지능·머신러닝 분야를 중심으로 기술 발전 속도가 빨라진 것이 내용연수를 줄인 이유다. 2025년 변경의 효과로 감가상각·상각비가 14억달러 늘고 순이익이 10억달러(기본·희석 주당 0.10달러) 줄었으며, 주로 AWS 부문에 영향을 미쳤다.
- **바꾼 이력**: 있음(위 참조) — 2024년 연장(5→6년), 2025년 재단축(6→5년, 일부 자산). 방향이 한 번은 늘리고 한 번은 줄인 특이 사례다.

### 메타 플랫폼스 (META)

- **출처**: 10-K FY2025, accession 0001628280-26-003942, https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm
- **인용(내용연수 표)**: "The estimated useful lives of property and equipment and amortization periods of finance lease right-of-use (ROU) assets as of December 31, 2025 are described below: Property and Equipment Useful Life/Amortization period Servers and network assets Five to 5.5 years Buildings 25 to 30 years Equipment and other One to 25 years Finance lease right-of-use assets Five to 20 years Leasehold improvements Lesser of estimated useful life or remaining lease term."
- **인용(변경 및 손익 영향)**: "In January 2025, we completed an assessment of the useful lives of property and equipment, which resulted in an increase in the estimated useful lives of most servers and network assets to 5.5 years, effective January 1, 2025. Based on the servers and network assets placed in service as of December 31, 2024, the financial impact of this change in estimate included a reduction in depreciation expense of $2.92 billion and an increase in net income of $2.59 billion, or $1.00 per diluted share, for the year ended December 31, 2025."
- **번역**: 2025년 12월 31일 기준 서버·네트워크 자산의 추정 내용연수는 5~5.5년, 건물은 25~30년, 장비·기타는 1~25년, 금융리스 사용권자산은 5~20년이다. 2025년 1월 내용연수 재평가를 마치고 대다수 서버·네트워크 자산의 추정 내용연수를 2025년 1월 1일부로 5.5년으로 늘렸다. 2024년 말 기준 가동 중이던 서버·네트워크 자산을 기준으로 이 변경의 2025 회계연도 재무 영향은 감가상각비 29.2억달러 감소, 순이익 25.9억달러 증가(희석 주당 1.00달러)다.
- **바꾼 이력**: 있음(위 참조) — 2025년 1월 1일부로 서버·네트워크 자산 내용연수를 5.5년으로 연장, 이익 증가 25.9억달러(주당 1.00달러)를 문서에 명시.

### 애플 (AAPL)

- **출처**: 10-K FY2025(회계연도 2025-09-27 마감), accession 0000320193-25-000079, https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm
- **인용**: "Property, Plant and Equipment. Property, plant and equipment are stated at cost. Depreciation on property, plant and equipment is recognized on a straight-line basis." Note 5의 자산 구성 표는 "Land and buildings", "Machinery, equipment and internal-use software", "Leasehold improvements"의 총액·감가상각누계액만 제시하고, 자산군별 추정 내용연수(연수)는 어디에도 표기하지 않는다.
- **번역**: 유형자산은 취득원가로 계상하며 정액법으로 감가상각한다. (내용연수 연수 자체는 공시하지 않음)
- **바꾼 이력**: 문서에 없음(애초에 자산군별 내용연수 연수를 공개하지 않으므로, 변경 이력도 나올 수 없다).

## 못 찾은 것

- **애플**: 서버·네트워크 장비·건물 모두 구체적 내용연수(연수)를 10-K에서 찾지 못했다. Note 5(Property, Plant and Equipment)는 자산군별 총액·누계상각액·전체 감가상각비만 공시하고 연수는 밝히지 않는다.
- **엔비디아**: "서버"를 별도 자산군으로 구분한 내용연수 공시가 없다. "장비·컴퓨트 하드웨어·소프트웨어" 통합 항목의 2~7년만 확인된다.
- **구글·마이크로소프트**: 서버와 네트워크 장비가 하나의 문장/항목으로 묶여 있어 두 자산을 분리한 연수는 원문에 없다(둘 다 "6년" 또는 "2~6년"으로 통합 표기).
- **구글·마이크로소프트·애플**: 최근 내용연수 변경 이력(연도, 손익 영향 금액)이 이번에 받은 10-K 본문에는 없다.

읽은 회사 6곳 / 서버 내용연수를 찾은 곳 4곳(구글·마이크로소프트·아마존·메타, 단 구글·마이크로소프트는 네트워크 장비와 통합 표기) / 내용연수 변경 이력과 손익 영향을 구체 수치로 공시한 곳 2곳(아마존·메타)
