# 회계 처리 관찰 후보 — B갈래 (23편)

## 찾은 것

### 1. TCO 모델의 감가상각 내용연수 가정이 실제 업계 관행과 다르다

- **어느 회사·어느 항목**: Neocloud·하이퍼스케일러 일반 / GPU 시간당 자본비용(TCO) 계산
- **원문**: `content/newsletter/ai_infra/compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md` L738-739
- **인용**: "SemiAnalysis TCO 모델은 보수적 기준으로 4년 사용연한(내용연수)을 적용해 시간당 자본비용을 계산" / "하지만 실제 대다수 Neocloud·하이퍼스케일러는 5\~6년 감가상각을 적용 — 상각 기간에 영향받지 않는 프로젝트 IRR(내부수익률)을 더 선호하는 지표로 제시"
- **종류**: 감가상각 내용연수

### 2. 시설·전력 등 통과 비용을 오픈AI가 총액 기준으로 매출 인식

- **어느 회사·어느 항목**: 오픈AI-세레브라스 MRA(마스터 관계 계약) / 오픈AI 매출
- **원문**: `content/newsletter/ai_infra/compute/[260513] 세레브라스 - 더 빠른 토큰을 주세요.md` L506
- **인용**: "시설 임대료·전력 등 통과 비용은 오픈AI가 총액 기준으로 매출 인식되도록 상환"
- **종류**: 총액·순액 매출 인식

### 3. 고객에게 준 워런트(지분)를 매출 차감(contra-revenue)으로 처리

- **어느 회사·어느 항목**: 세레브라스 / 오픈AI에 발급한 워런트, 매출 차감분
- **원문**: `content/newsletter/ai_infra/compute/[260513] 세레브라스 - 더 빠른 토큰을 주세요.md` L508
- **인용**: "결론: 회계상 이 워런트는 2025년 말 기준 주당 82.02달러로 평가돼 최대 약 27.4억 달러(오픈AI 예상 매출의 약 10%)의 매출 차감(contra-revenue)으로 처리 — 다만 \"확정적(probable)\"으로 분류된 트랜치만 실제로 매출에서 차감되며, 2GW 확장 옵션에 연동된 부분은 옵션이 실행돼야 비로소 반영됨"
- **종류**: 지분 대가의 매출 차감 회계처리 (기타, 위 목록의 8종에 정확히 안 들어맞지만 회계 처리 선택이 공시 매출 규모를 바꾸는 사례)

### 4. 같은 컴퓨트 판매가 클라우드 매출이 아니라 하드웨어 매출로 인식될 전망

- **어느 회사·어느 항목**: 세레브라스-AWS 딜 / 매출 분류(클라우드 매출 vs 하드웨어 매출)
- **원문**: `content/newsletter/ai_infra/compute/[260513] 세레브라스 - 더 빠른 토큰을 주세요.md` L593
- **인용**: "결론: 세레브라스는 오픈AI 딜과 유사하게 AWS에도 워런트(최대 270만 주, 행사가 주당 100달러, 구매 물량 연동)를 발급 — 다만 이 딜은 클라우드 매출이 아니라 AWS 소유 데이터센터에 CS-3를 판매하는 하드웨어 매출로 인식될 전망"
- **종류**: 매출 항목 분류(같은 경제 실질이 어느 매출 항목에 잡히는지)

## 관찰이 없는 파일

- `content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md` — 없음 (총마진·원가 논의는 있으나 회계 처리 선택 이야기는 아님)
- `content/newsletter/ai_infra/compute/[260313] AI 실리콘 대란 - TSMC N3부터 메모리까지.md` — 없음
- `content/newsletter/ai_infra/compute/[260324] GTC 2026 - 추론 왕국의 확장.md` — 없음
- `content/newsletter/ai_infra/compute/[260401] Nvidia Blackwell 해부 - 텐서 코어, PTX 명령어, SASS, 플로어스위프, 수율.md` — 없음
- `content/newsletter/ai_infra/compute/[260609] DeepSeek V4 1.6T Day 0부터 Day 43까지 성능 변화 - Huawei, GB300 NVL72, MI355X, B200.md` — 없음 ("상각"이 나오지만 GPU 랭크 간 가중치 로딩 비용 분산을 뜻하는 비유적 용법, 재무 회계가 아님)
- `content/newsletter/ai_infra/compute/[260723] 베라 루빈 NVL72 vs GB200 NVL72 - 추론 TCO·아키텍처 분석.md` — 없음
- `content/newsletter/ai_infra/compute/[260725] AMD는 CUDA 모트를 깰 수 있는가 - AMD Advancing AI 2026.md` — 없음 (지분 리베이트·리스보증 확대는 딜 구조 설명일 뿐, 공시 숫자가 회계 처리 때문에 실제 경제와 어긋난다는 문장은 없음)
- `content/newsletter/ai_infra/compute/[260810] 엔비디아 GPU의 초고속 상호작용성 - TileRT InferenceX.md` — 없음
- `content/newsletter/ai_infra/compute/[260819] 세레브라스 차세대 CS-4 - 빠른 게 더 빨라졌다.md` — 없음
- `content/newsletter/ai_infra/compute/[260824] AgentX InferenceXv3 - 에이전틱 추론에서도 CUDA 해자는 버티는가.md` — 없음 ("회계"가 여러 번 나오지만 전부 KV 캐시 소유권 소프트웨어 버그를 뜻하는 용법, 재무 회계가 아님)
- `content/newsletter/ai_infra/compute/[260825] 오픈AI 할라페뇨 - 엔비디아 블랙웰보다 낫다.md` — 없음
- `content/newsletter/ai_infra/construction/[260729] 레고 데이터센터의 무법지대 - 모듈러 건설 벤더 지형도와 경제성 분석.md` — 없음 (모듈러 벤더별 단축률 주장이 서로 다른 범위를 측정한 수치라는 지적은 있으나, 이는 마케팅 수치 비교이지 회계 처리 선택 이야기가 아님)
- `content/newsletter/ai_infra/cooling/[250214] 데이터센터 해부학 Part 2 - 냉각 시스템.md` — 없음
- `content/newsletter/ai_infra/cooling/[260115] 토큰 대 햄버거 - 데이터센터 물 발자국 대결.md` — 없음 (취수·소비 구분, 하드웨어 수명 상각은 SemiAnalysis 자체 물 발자국 추정 방법론이며 공시 재무 숫자 이야기가 아님)
- `content/newsletter/ai_infra/memory/[230717] 낸드플래시 독점 균열 - 도쿄일렉트론 vs 램리서치.md` — 없음
- `content/newsletter/ai_infra/memory/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md` — 없음
- `content/newsletter/ai_infra/memory/[260207] 메모리 마니아 - 40년 만의 공급 부족이 부르는 메모리 붐.md` — 없음
- `content/newsletter/ai_infra/memory/[260416] ISSCC 2026 총정리 - HBM4, LPDDR6, CPO, 액티브 LSI 등 차세대 메모리·인터커넥트.md` — 없음
- `content/newsletter/ai_infra/memory/[260623] 중국 CXMT, DRAM 강자들에 도전장을 내밀다.md` — 없음 (마진 개선이 "가격 상승 때문"이라는 지적은 있으나 회계 처리 선택 이야기는 아님)
- `content/newsletter/ai_infra/memory/[260702] ECTC 2026 총정리 - EMIB-T 로드맵, 커스텀 HBM, 마이크로플루이딕 냉각, 광학 인터커넥트.md` — 없음
- `content/newsletter/ai_infra/networking/[260101] 코패키지드 옵틱스(CPO) - 빛으로 확장하는 차세대 인터커넥트.md` — 없음 (스위치 벤더 마진이 원가 비교를 뒤집는다는 지적은 있으나 이는 가격 구조 이야기이지 회계 처리 선택 이야기가 아님)

읽은 파일 23편 / 관찰 4건
