---
kind: brief
headline: AMD와 엔비디아 — 값은 붙었고 소프트웨어가 갈랐다
subhead: 스펙·총소유비용·실측이 어디서 뒤집히는지, 그리고 고객이 실제로 무엇을 샀는지
section: chip
as_of: 2026-08-14
sources:
  - {file: "content/newsletter/ai_infra/compute/[260725] AMD는 CUDA 모트를 깰 수 있는가 - AMD Advancing AI 2026.md", note: ""}
  - {file: "content/newsletter/ai_infra/compute/[250613] AMD Advancing AI - MI350X와 MI400 UALoE72, MI500 UAL256.md", note: ""}
  - {file: "content/newsletter/ai_infra/compute/[251009] InferenceMAX - 오픈소스 추론 벤치마킹.md", note: ""}
  - {file: "content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md", note: ""}
  - {file: "content/newsletter/ai_infra/compute/[260609] DeepSeek V4 1.6T Day 0부터 Day 43까지 성능 변화 - Huawei, GB300 NVL72, MI355X, B200.md", note: ""}
---

## 한 줄

칩 스펙과 총소유비용은 이미 붙었고, 갈리는 곳은 소프트웨어와 랙이다. 판단이 아니라
지금까지 나온 실측을 한자리에 모은 브리핑이다.

## 지금 상태

- **평가가 세 번 올라갔다.** AMD가 CUDA 소프트웨어 장벽을 넘을 확률을 2023년 0%에서 2025년 4월 의미 있는 가능성으로, 다시 2026년 7월 두 리스크만 해결하면 높음으로 올렸다([260725] AMD는 CUDA 모트를 깰 수 있는가 L52).
- **근거는 스펙이 아니라 고객이다.** 앤트로픽이 AMD 칩 2기가와트 배치를 공식화했고, 품질 문제로 2023년에 떠났던 마이크로소프트가 돌아왔다([260725] AMD는 CUDA 모트를 깰 수 있는가 L53).
- **칩은 앞선 구석도 있다.** MI455X는 데이터센터용 2나노 실리콘을 세계 최초로 출하하는 칩이고, HBM(여러 층 쌓은 메모리) 12스택으로 패키지당 432GB를 담아 경쟁 제품의 288GB보다 크다([260725] AMD는 CUDA 모트를 깰 수 있는가 L131, L133).
- **랙에서 값이 붙는다.** 메타 배포분 기준 Helios 랙 스케일업 링크의 약 85%에 신호 재증폭 칩이 필요해 랙당 배선 비용만 68,928달러다([260725] AMD는 CUDA 모트를 깰 수 있는가 L241, L242).
- **소프트웨어가 여전히 늦다.** DeepSeek V4 출시 당일 AMD 스택은 사실상 작동 불능이었고 사용자당 초당 1~2토큰에 그쳤다([260609] DeepSeek V4 1.6T Day 0부터 Day 43까지 성능 변화 L146). 다만 43일 만에 처리량을 100배 이상 끌어올렸다(L51).

## 숫자

| 항목 | 값 | 출처 |
|---|---|---|
| 추론 총소유비용 | MI355X가 HGX B200 대비 33% 낮음 | ([250613] AMD Advancing AI L184) |
| 시간당 GPU당 총소유비용 | 1.38달러 vs 1.97달러(약 30% 낮음) | ([250613] AMD Advancing AI L841) |
| 전력 역전 | MI400 240kW vs VR200 187kW, 운영비 0.85달러 vs 0.67달러 | ([250613] AMD Advancing AI L842) |
| 집단 통신 | all-to-all에서 MI355X가 GB200 NVL72보다 18배 느림 | ([250613] AMD Advancing AI L271) |
| 전력효율 | 동세대 B200이 MI355X보다 약 20% 높음(TDP(발열 한도) 1.4kW 대 1kW) | ([251009] InferenceMAX L365) |
| 서버 가격 | H100 18만9,637달러 vs MI300X 14만5,017달러, B200 30만8,680달러 vs MI355X 18만9,607달러 | ([251009] InferenceMAX L480) |
| 종이 스펙 기준 | FP8 총소유비용/PFLOP은 MI355X 0.30달러, B200 0.43달러 | ([251009] InferenceMAX L482) |
| 자동검증 | vLLM CI에 MI355X 테스트 0건, Pollara NIC 매칭률 0% | ([260216] InferenceX v2 L460) · ([260725] AMD는 CUDA 모트를 깰 수 있는가 L87) |

## 어디서 갈리나

- **조건을 몇 개 거느냐로 결과가 뒤집힌다.** FP8 단일 최적화에서는 MI355X가 B200과 겨룰 만하지만, 프론티어 랩이 실제로 쓰는 FP4·분리형 서빙·광역 전문가 병렬화를 동시에 걸면 성능이 급락한다([260216] InferenceX v2, 주장).
- **구간을 어디로 잡느냐도 다르다.** 총소유비용을 고정하면 B200이 앞서고, 상호작용성을 초당 35토큰으로 고정하면 GB200 NVL72가 백만 토큰당 비용에서 4배 앞선다([251009] InferenceMAX L313).
- **고객이 받은 물건이 표준과 다르다.** 메타가 주문한 MI455X 대부분은 연산 다이를 8개에서 4개로, HBM을 12스택에서 6스택으로 줄인 절반 사양이다([260725] AMD는 CUDA 모트를 깰 수 있는가 L177).
- **내부 자원이 개선 속도를 잡는다.** AMD 경영진이 용량 부족을 이유로 vLLM 팀 전용 클러스터를 재배치하면서 매칭률 90% 목표가 후퇴했다([260725] AMD는 CUDA 모트를 깰 수 있는가 L88).

## 안 나온 것

- 절반 사양으로 받은 칩의 실측 성능은 어디에도 없다. 표준 사양 벤치마크로 그 물량을 대신 읽고 있다.
- 소프트웨어가 따라잡는 데 걸리는 기간을 미리 재는 방법이 없다. 43일은 사후 관측이다.
