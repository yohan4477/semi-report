# 시스템별 메모리 규격 표 — 원문 인용 포함

대상 7종: H200(HGX8) · B200(HGX8) · B300(HGX8, Blackwell Ultra) · GB200 NVL72 · GB300 NVL72 · Vera Rubin NVL72(vr200) · AMD MI355X(HGX8)

표기: **값** | 인용(파일#L줄) | 성격(원문 값 / 원문에서 셈한 값 / 원문에 없음)

---

## 1) H200 (HGX 8장)

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | HBM3E, **144GB** | `input/clippings/AMD vs NVIDIA Inference Benchmark Who Wins - Performance & Cost Per Million Tokens.md#L66` — "NVIDIA addressed the capacity shortcoming in Q3 2024 when they started mass production of H200, which has 144GB of memory compared to just 80GB of HBM Capacity in H100" | 원문 값 (통상 알려진 141GB와 다름 — 원문 표기 그대로 144GB 기재) |
| | 세대(HBM3E) 근거 | `input/clippings/TPUv7 Google Takes a Swing at the King.md#L163` — "it fell far short of the H100/H200 on memory capacity and bandwidth, with only 2 stacks of HBM3 vs 5 and 6 stacks of HBM3 and HBM3E respectively" (H100=HBM3 5스택, H200=HBM3E 6스택) | 원문 값 |
| ② HBM 대역폭 | 단일 HGX H200 서버(8장) 합산 **38.4TB/s** → GPU 1장당 **4.8TB/s** | `input/clippings/Ultra-High Interactivity on NVIDIA GPUs - TileRT InferenceX.md#L111` — "for just an single HGX H200 server (38.4TB/s of aggregate HBM memory bandwidth)" | 원문에서 셈한 값(38.4÷8) |
| ③ CPU 종류·호스트 메모리 | 원문에 없음 | — | 원문에 없음 |
| ④ CPU-GPU 연결 | PCIe 5.0, **128GB/s**(HGX 공통 수치로 언급) | `input/clippings/InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590` — "…compared to 128GB/s / 256GB/s on HGX with PCIe 5.0 and 6.0, respectively" | 원문 값(HGX 세대 공통 서술, H200 단독 수치는 아님) |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | 원문에 없음(H200 단독 수치 없음. H100 SXM 노드 기준 "8x400G InfiniBand"는 있으나 H200 고유 서술 아니어서 미채택) | `input/clippings/The GPU Cloud ClusterMAX™ Rating System  How to Rent GPUs.md#L380` (H100 기준, 참고용) | 원문에 없음 |
| ⑥ 스케일업 크기·NVLink 대역폭 | 8장. GPU당 NVLink(4세대) 대역폭 수치는 원문에 없음 | — | 원문에 없음 |
| ⑦ 설계 전력(TDP) | 원문에 없음(H100=700W는 확인되나 H200 고유 수치 없음) | `content/newsletter/ai_infra/compute/[250820] H100 vs GB200 NVL72 학습 벤치마크 - 전력, TCO, 신뢰성 분석.md#L107` (H100 참고용) | 원문에 없음 |

---

## 2) B200 (HGX 8장)

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | HBM3E, **192GB** | `input/clippings/InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590` — "MI355X has 288GB HBM3e versus B200s 192GB" | 원문 값 |
| | ※ 다른 발행일 원문은 180GB로 기재(어긋남, 날짜별 병기) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65`(2025-06-13 발행) — "…288GB vs 180GB for the B200" | 원문 값(2025-06-13 발행, 2026-02-16 발행 자료의 192GB와 어긋남) |
| ② HBM 대역폭 | **8TB/s** | `input/clippings/InferenceMAX™ Open Source Inference Benchmarking.md#L528` — "The MI355X has the same on-paper memory bandwidth as the B200 at 8TB/s." | 원문 값 |
| ③ CPU 종류·호스트 메모리 | 원문에 없음 | — | 원문에 없음 |
| ④ CPU-GPU 연결 | PCIe 5.0, **128GB/s** | `input/clippings/InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590` | 원문 값 |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | 스케일아웃 NIC **ConnectX-7 계열, GPU당 400Gbit/s** | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L71` — "the MI350/MI355 supports speeds of 400 Gbit/s per GPU – the same as B200 and GB200 NVL72" | 원문 값(AMD 기사 속 비교 서술에서 확인) |
| ⑥ 스케일업 크기·NVLink 대역폭 | 8장(스위치드 all-to-all). NVLink5, GPU당 **900GB/s(단방향, 7,200Gbit/s)** = 양방향 1.8TB/s | `content/newsletter/ai_infra/networking/[260101] 코패키지드 옵틱스(CPO) - 빛으로 확장하는 차세대 인터커넥트.md#L233` — "블랙웰의 NVLink 5는 GPU당 7,200Gbit/s(단방향)" | 원문 값(한국어 변환본, 영문 클리핑 `Co-Packaged Optics (CPO) Book...md`은 같은 수치가 이미지/긴 줄로 생략되어 한국어 변환본 인용) |
| ⑦ 설계 전력(TDP) | **1,000W(1kW)** | `input/clippings/AMD 2.0 - New Sense of Urgency  MI450X Chance to Beat Nvidia  Nvidia's New Moat.md#L585` — "…to stay competitive with the B200 1000W and B300A NVL16" | 원문 값 |

---

## 3) B300 (HGX 8장, Blackwell Ultra)

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | HBM3E(12-Hi), **288GB** | `input/clippings/Long Live the Short King Why 4-hi HBM Wins.md#L30` — "…compared to 192GB from 288GB per GPU compared to standard Rubin and B300" (Rubin Ultra가 다운그레이드하는 기준점이 Rubin/B300=288GB) | 원문 값 |
| ② HBM 대역폭 | **8TB/s**(MI355X와 동일 대역폭·용량이라는 원문 서술로부터 도출) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65` — "the MI350/MI355 has the same memory bandwidth and capacity as B300" + `input/clippings/InferenceMAX™ Open Source Inference Benchmarking.md#L528`(MI355X=8TB/s) | 원문에서 셈한 값(두 인용 결합) |
| ③ CPU 종류·호스트 메모리 | 원문에 없음 | — | 원문에 없음 |
| ④ CPU-GPU 연결 | PCIe 6.0, **256GB/s** | `input/clippings/InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md#L590` — "…128GB/s / 256GB/s on HGX with PCIe 5.0 and 6.0, respectively"(B300이 PCIe6.0 세대) | 원문 값(문맥상 B300 배정, "respectively" 절 해석) |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | 스케일아웃 NIC **ConnectX-8, GPU당 800Gbit/s** | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L71` — "…it will be surpassed soon by B300 HGX NVL8 and the GB300 NVL72 which both offer 800 Gbit/s per GPU networking…their 800GbE ConnectX-8 NIC" | 원문 값 |
| ⑥ 스케일업 크기·NVLink 대역폭 | 8장(스위치드 all-to-all, NVLink5 세대 계승) | 위 InferenceX v2 590 및 AMD Advancing AI 67(스위치드 all-to-all이 B200/B300 공통) | 원문 값 |
| ⑦ 설계 전력(TDP) | **1,200W**(MI355X 1,400W 대비 "200W 적음"에서 역산) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L63` — "the B300's FP4 TFLOP/s is 1.3x faster than that of the MI355X while consuming 200 W less power" | 원문에서 셈한 값(1,400−200) — 참고로 GB300(랙) GPU는 별도 원문에서 1,400W로 직접 확인됨(아래 GB300 항 참조), HGX 공랭형 B300과 다를 수 있음 |

---

## 4) GB200 NVL72

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | HBM3E, **192GB** | `content/newsletter/ai_infra/memory/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md#L448` — "H100의 80GB/3TB/s → GB200의 192GB/8TB/s로 늘어나도" | 원문 값(한국어 변환본) |
| ② HBM 대역폭 | **8TB/s** | 위와 동일 줄(#L448) | 원문 값 |
| ③ CPU 종류·호스트 메모리 | **Grace CPU**(ARM Neoverse V2, 6×7 메시, 76코어 중 72개 활성, L3 117MB), **LPDDR5X 최대 480GB**, 512비트 버스 500GB/s | `input/clippings/CPUs are Back The Datacenter CPU Landscape in 2026.md#L314` — "Grace also adopts mobile-class LPDDR5X memory to keep non-GPU power down while maintaining high bandwidths of 500GB/s on a 512-bit wide memory bus… up to 480GB memory per Grace CPU"; `#L316`(코어 구성) | 원문 값 |
| ④ CPU-GPU 연결 | **NVLink-C2C 900GB/s(양방향)**, 칩 간 직결 — 단, GPU→NIC 경로는 Grace를 거쳐 PCIe5로 ConnectX-7과 통신(간접) | `input/clippings/CPUs are Back The Datacenter CPU Landscape in 2026.md#L314` — "This 900GB/s (bi-directional) high speed link…"; `content/newsletter/ai_infra/compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md#L273` — "GB200: GPU가 Grace CPU와 C2C로 연결되고, Grace가 다시 PCIe5로 ConnectX-7과 통신(간접 연결)" | 원문 값 |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | ConnectX-7(간접, Grace 경유), 로컬 NVMe는 BlueField-3가 관리(Rubin과의 대조 서술에서 확인) | `content/newsletter/ai_infra/compute/[260226]...md#L266` — "로컬 NVMe 저장장치 BlueField-3 관리에서 Orchid 모듈의 CX-9 관리로"(GB300/VR과 대조하며 GB200/300은 BlueField-3 관리였음을 시사) | 원문 값(대조 서술에서 역추출) |
| ⑥ 스케일업 크기·NVLink 대역폭 | **72장**, NVLink5 GPU당 **900GB/s 단방향**(1.8TB/s 양방향) | `content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md#L43` — "랙 내부 GPU끼리는 NVLink로 GPU당 900GB/s(단방향)까지 연결" | 원문 값(한국어 변환본) |
| ⑦ 설계 전력(TDP) | **1,200W**(GPU 1개 기준) | `input/clippings/AWS Trainium3 Deep Dive  A Potential Challenger Approaching.md#L826` — "Trn2 runs at ~500W per chip while Trainium3 operates at ~1,000W versus ~1,200 GB200 and 1,400W for GB300."; 국문 동일 수치: `content/newsletter/ai_infra/compute/[250820] H100 vs GB200 NVL72 학습 벤치마크 - 전력, TCO, 신뢰성 분석.md#L107`("GB200 GPU 1개가 1,200W") | 원문 값 |

---

## 5) GB300 NVL72

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | **HBM3E 12-Hi, 288GB** | `content/newsletter/ai_infra/compute/[251128] TPUv7 - 구글, AI 반도체 왕좌에 도전장을 내밀다.md#L195` — "HBM3E 12-Hi 288GB를 쓰는 GB300" | 원문 값(한국어 변환본) |
| ② HBM 대역폭 | **8TB/s**(MI355X·B300과 동일 대역폭이라는 원문 서술로부터 도출) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65` + `InferenceMAX™...md#L528` | 원문에서 셈한 값 |
| ③ CPU 종류·호스트 메모리 | **Grace CPU**(GB200과 동일 스펙, 원문에서 GB300 전용 차이는 확인 안 됨) — LPDDR5X 최대 480GB | `input/clippings/CPUs are Back The Datacenter CPU Landscape in 2026.md#L314,316` | 원문 값(GB200과 공용 서술, GB300 고유 수치는 원문에 없음) |
| ④ CPU-GPU 연결 | **NVLink-C2C 900GB/s**(양방향, 세대 계승) + **GPU-ConnectX-8 직접 연결 경로 추가**(2-host NIC, 지연시간 개선) | `content/newsletter/ai_infra/compute/[260226]...md#L274` — "GB300: B300 GPU가 ConnectX-8과 직접 연결되는 경로 추가(2-host NIC, 지연시간 개선)" | 원문 값 |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | **ConnectX-8, GPU당 800Gbit/s** | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L71` — "B300 HGX NVL8 and the GB300 NVL72 which both offer 800 Gbit/s per GPU networking" | 원문 값 |
| ⑥ 스케일업 크기·NVLink 대역폭 | **72장**, NVLink GPU당 **900GB/s**, B300(8장 한계)의 InfiniBand 대비 9배 이상 | `content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md#L416` — "GB300 NVL72는 72 GPU를 NVLink(GPU당 900GB/s)로 묶어 대역폭이 9배 이상 높음" | 원문 값 |
| ⑦ 설계 전력(TDP) | **1,400W** | `input/clippings/AWS Trainium3 Deep Dive  A Potential Challenger Approaching.md#L826` — "1,400W for GB300"; `content/newsletter/ai_infra/business/[260501] AI 가치 포착 - 모델 랩으로의 이동.md#L314,323` — "GB300→VR NVL72는 칩 TDP가 거의 2배(1,400W→2,300W)" | 원문 값(복수 원문 일치) |

---

## 6) Vera Rubin NVL72 (vr200)

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | **HBM4, 288GB**(GB300과 동일 용량) | `content/newsletter/ai_infra/compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md#L104` — "HBM4 대역폭 8→22TB/s(2.75배), 용량은 288GB로 GB300과 동일"; 교차확인 `input/clippings/Long Live the Short King Why 4-hi HBM Wins.md#L30` — "conventional Rubin and even Blackwell Ultra"(둘 다 288GB) | 원문 값 |
| ② HBM 대역폭 | **22TB/s**(스택당 버스폭 2배, 10.8GT/s) — 초기 출하는 공급망 문제로 **20TB/s에 다소 못 미칠 가능성** | `content/newsletter/ai_infra/compute/[260226]...md#L91,118` — "HBM4 대역폭은 2.75배(8→22TB/s, 실제 초기 출하는 20TB/s 근접 예상)"; "…초기 출하는 20TB/s에 조금 못 미칠 가능성이 있습니다" | 원문 값(한국어 변환본) |
| ③ CPU 종류·호스트 메모리 | **Vera CPU**(자체 커스텀 "Olympus" 코어, SMT 지원 88코어/176스레드, L3 162MB), **LPDDR5X, SOCAMM 8개 소켓**(192GB·128GB 두 종류), Vera 1개당 최대 **1,536GB(1.5TB)**~최소 1,024GB, 메모리 속도 9,600MT/s | `content/newsletter/ai_infra/compute/[260209] CPU가 돌아왔다 - 2026년 데이터센터 CPU 판도.md#L474,503,504` — "8년 만에 엔비디아 자체 커스텀 코어("Olympus", SMT 지원 88코어/176스레드)"; "메모리 1.5TB(SOCAMM 8개, 1.2TB/s)"; `content/newsletter/ai_infra/compute/[260226]...md#L93,130,136,240,142` — "Vera CPU는 Grace 대비 성능 2배, 코어 72→88개…최대 용량 3배(1.5TB)"; "9,600MT/s로 대역폭 2.5배 / SOCAMM 8개로 최대 용량 3배(1.5TB)"; "SOCAMM 소켓 8개(192GB·128GB 두 종류, Vera 1개당 최대 1,536GB~최소 1,024GB)"; "L3 캐시도 40% 늘어난 162MB" | 원문 값 |
| ④ CPU-GPU 연결 | **NVLink-C2C 1.8TB/s**(양방향, Grace-Blackwell 900GB/s의 2배), 칩 간 직결(Strata 모듈: Rubin GPU 2개+Vera CPU 1개) — 단 GPU-NIC 경로는 다시 간접화: Rubin이 ConnectX-9 2개분 PCIe 대역폭을 못 감당해 Vera를 거쳐 **PCIe6**로 연결 | `content/newsletter/ai_infra/compute/[260226]...md#L137` — "Rubin 연결 NVLink-C2C 대역폭 1.8TB/s로 2배"; `#L240` — "Strata: …Rubin GPU 2개, Vera CPU 1개 탑재"; `#L275` — "VR NVL72: 다시 GB200 방식으로 회귀 — Rubin이 ConnectX-9 2개를 감당할 PCIe 대역폭이 부족해, Vera를 거쳐 PCIe6로 연결" | 원문 값 |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | **ConnectX-9**(Orchid 모듈, 전면 배치, PCIe6 스위치 48레인, 800G 대역폭·CX-8과 동일), 로컬 NVMe는 Orchid 모듈에서 ConnectX-9가 관리, **BlueField-4**가 ConnectX-9 백엔드 NIC **8개**를 통합 관리(Astra 아키텍처) | `content/newsletter/ai_infra/compute/[260226]...md#L157` — "ConnectX-9: CX-8과 대역폭(800G)·PCIe6 스위치 용량(48레인)은 같지만…GPU당 NIC 개수를 2배로"; `#L277` — "로컬 NVMe…Orchid 모듈에 위치해 ConnectX-9가 관리"; `#L279` — "BlueField-4는 ConnectX-9 백엔드 NIC 8개를 통합 관리(Astra 아키텍처)" | 원문 값 |
| ⑥ 스케일업 크기·NVLink 대역폭 | **72장**(Rubin GPU 패키지 72개, Vera CPU 36개, NVLink6 스위치 ASIC 36개). NVLink6 스위치 칩당 대역폭은 NVLink5와 동일 **28.8T**(칩 수만 2배)이나 GPU당 대역폭은 400G 양방향 SerDes로 2배 상승해 **14.4Tbit/s 단방향**(=1.8TB/s) | `content/newsletter/ai_infra/compute/[260226]...md#L166` — "Rubin GPU 패키지 72개, Vera CPU 36개, NVLink 6 스위치 ASIC 36개로 구성"; `#L156` — "NVLink 6 스위치: 랙당 칩 수가 36개로 2배 늘었지만 칩 하나의 대역폭(28.8T)은 NVLink 5와 동일…'400G' 양방향 SerDes로 속도를 2배"; `content/newsletter/ai_infra/networking/[260101] 코패키지드 옵틱스(CPO)...md#L71` — "차세대 루빈에서 14.4Tbit/s" | 원문 값 |
| ⑦ 설계 전력(TDP) | **Max-P 2,300W** / 절전형 **Max-Q 1,800W** — 양산 SKU는 트레이당 TDP 2,300W 채택 | `content/newsletter/ai_infra/compute/[260226]...md#L92,105` — "칩 발열(TDP)은 최대 2,300W(Max-P 옵션)로…절전형 Max-Q(1,800W)"; `content/newsletter/ai_infra/compute/[260914] 베라 루빈 NVL72 에이전틱 추론 - 달러당 성능 67배.md#L99` — "루빈 랙은 트레이당 TDP…2,300W…양산 SKU를 쓴다"; 교차확인 `content/newsletter/ai_infra/business/[260501] AI 가치 포착 - 모델 랩으로의 이동.md#L314` — "GB300→VR NVL72는 칩 TDP가 거의 2배(1,400W→2,300W)" | 원문 값 |

---

## 7) AMD MI355X (8장)

| 항목 | 값 | 인용 | 성격 |
|---|---|---|---|
| ① HBM 세대·용량 | **HBM3E, 288GB** | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L65` — "…much more HBM at 288GB vs 180GB for the B200"; 세대(HBM3E) 근거 `#L215`(원문 지문 214 부근, "the memory controllers can now handle faster HBM3E") | 원문 값 |
| ② HBM 대역폭 | **8TB/s** | `input/clippings/InferenceMAX™ Open Source Inference Benchmarking.md#L528` — "The MI355X has the same on-paper memory bandwidth as the B200 at 8TB/s." | 원문 값 |
| ③ CPU 종류·호스트 메모리 | 원문에 없음(별도 x86 호스트 CPU 브랜드·모델 확인 안 됨) | — | 원문에 없음 |
| ④ CPU-GPU 연결 | 원문에 없음(스케일업 XGMI/PCIe5 PHY 서술은 GPU 간 연결이며 CPU-GPU 경로 수치는 확인 안 됨) | 참고: `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L67`(XGMI가 PCIe5.0 PHY Serdes 사용, GPU 간 스케일업용) | 원문에 없음 |
| ⑤ 트레이 PCIe 스위치·NIC·NVMe | 스케일아웃 NIC **GPU당 400Gbit/s**(B200·GB200과 동일) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L71` — "the MI350/MI355 supports speeds of 400 Gbit/s per GPU – the same as B200 and GB200 NVL72" | 원문 값 |
| ⑥ 스케일업 크기·NVLink 대역폭 | **8장**(메시 토폴로지, NVLink 아님). XGMI(PCIe5.0 PHY 기반) "오버클럭"으로 링크당 **64GB/s→76.8GB/s**(1.2배) | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L67` — "AMD was able to "overclock" their XGMI protocol…by 1.2x from 64GByte/s to 76.8GByte/s"; 스위치드 all-to-all 대비 1.6배 느림, GB200/300 대비는 비교 불가 수준(같은 줄) | 원문 값 |
| ⑦ 설계 전력(TDP) | **1,400W**(MI355X, 공랭+DLC 겸용); MI350X는 1,000W 공랭 전용 | `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md#L53` — "the MI350X is the 1,000W version that is air cooled while the MI355X is a 1,400W version that supports both air cooling and DLC liquid cooling" | 원문 값 |

---

## 못 찾은 칸 목록

- H200: ③ CPU 종류·호스트 메모리, ⑤ 트레이 PCIe 스위치·NIC·NVMe 수, ⑥ GPU당 NVLink(4세대) 대역폭 수치, ⑦ TDP(H200 고유 수치)
- B200 / B300: ③ CPU 종류·호스트 메모리(둘 다)
- GB300: ③ Grace CPU가 GB200과 스펙 차이가 있는지(원문은 GB200·GB300 공용으로만 서술)
- Vera Rubin NVL72: 없음(7개 항목 모두 인용 확보)
- MI355X: ③ CPU 종류·호스트 메모리, ④ CPU-GPU 연결(PCIe 세대·대역폭)

## 사용한 검색어

- `scripts/q.py`: "Vera Rubin", "HBM4", "Rubin" → 색인(회사·기관 개체명 전용)이라 원문 0편으로 반환, 이후 Grep으로 전환
- Grep 키워드: `HBM3e|HBM3E`, `H200`, `MI355X`, `B200.*192GB|180GB`, `TDP`, `700W|1000W|1,000W|1200W|1,200W|1400W|1,400W`, `NVLink.*GPU당|TB/s`, `Grace.*LPDDR`, `C2C`, `ConnectX-7|ConnectX-8|ConnectX-9|BlueField`, `141GB`, `192GB`, `288GB`
- 확인한 원문(영문 클리핑 우선, 없으면 한국어 변환본):
  - `input/clippings/AMD Advancing AI MI350X and MI400 UALoE72, MI500 UAL256.md`
  - `input/clippings/InferenceX v2 NVIDIA Blackwell Vs AMD vs Hopper - Formerly InferenceMAX.md`
  - `input/clippings/InferenceMAX™ Open Source Inference Benchmarking.md`
  - `input/clippings/AMD vs NVIDIA Inference Benchmark Who Wins - Performance & Cost Per Million Tokens.md`
  - `input/clippings/Ultra-High Interactivity on NVIDIA GPUs - TileRT InferenceX.md`
  - `input/clippings/TPUv7 Google Takes a Swing at the King.md`
  - `input/clippings/CPUs are Back The Datacenter CPU Landscape in 2026.md`
  - `input/clippings/AWS Trainium3 Deep Dive  A Potential Challenger Approaching.md`
  - `input/clippings/Long Live the Short King Why 4-hi HBM Wins.md`
  - `input/clippings/AMD 2.0 - New Sense of Urgency  MI450X Chance to Beat Nvidia  Nvidia's New Moat.md`
  - `content/newsletter/ai_infra/compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md`(영문 클리핑 미확보, 한국어 변환본만 존재)
  - `content/newsletter/ai_infra/compute/[260209] CPU가 돌아왔다 - 2026년 데이터센터 CPU 판도.md`
  - `content/newsletter/ai_infra/compute/[260216] InferenceX v2 - Nvidia Blackwell vs AMD vs Hopper.md`
  - `content/newsletter/ai_infra/compute/[251128] TPUv7 - 구글, AI 반도체 왕좌에 도전장을 내밀다.md`
  - `content/newsletter/ai_infra/memory/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md`
  - `content/newsletter/ai_infra/networking/[260101] 코패키지드 옵틱스(CPO) - 빛으로 확장하는 차세대 인터커넥트.md`
  - `content/newsletter/ai_infra/business/[260501] AI 가치 포착 - 모델 랩으로의 이동.md`
  - `content/newsletter/ai_infra/compute/[260914] 베라 루빈 NVL72 에이전틱 추론 - 달러당 성능 67배.md`
  - `content/newsletter/ai_infra/compute/[251204] AWS Trainium3 딥다이브 - 다가오는 잠재적 도전자.md`
  - `content/newsletter/ai_infra/compute/[250820] H100 vs GB200 NVL72 학습 벤치마크 - 전력, TCO, 신뢰성 분석.md`
