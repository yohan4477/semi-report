# 사실표 2 — DSV4 (DeepSeekV4 1.6T Day 0 to Day 43)

## DSV4 (발행 2026-06-09)

원문 파일 전체 353줄을 끝까지 읽음. 클리핑은 페이월로 잘리지 않았고(L170 "This post is public"), 마지막 대목은 L352의 비용 그래프 설명에서 끝난다. 원문에는 모델 사양표(총 파라미터·층 수·전문가 수·컨텍스트 길이·어휘 크기·라이선스)가 없다. 아래 사양은 원문에 흩어진 값만 옮겼다. 제목의 「1.6T」 외에 파라미터 수는 본문에 없다.

### 모델 사양 (원문에 나온 값만)
- L2 | 제목에 「DeepSeekV4 1.6T」 표기. 본문에는 총·활성 파라미터 수치가 따로 없다 | 성격: 불명 | 언제 것: 2026-06
- L14 | DeepSeek v4는 오픈 모델 커뮤니티의 진전이며 "unsurprisingly, it is the product of a Chinese lab" | 성격: 저자 판단 | 언제 것: 2026-06
- L56 | 변종 이름은 DeepSeek V4 Pro와 DeepSeek v4 Flash 둘이 나온다. 네이티브 체크포인트는 "mixed FP4 MoE-FP8 Attention quantized weights", 즉 MoE 가중치 FP4(MXFP4), 어텐션 가중치 FP8 | 성격: 공표 | 언제 것: 2026-04-25
- L100 | "All previous DeepSeek models and DeepSeek v4 flash have a hidden size of 4096" | 성격: 공표 | 언제 것: 2026-05
- L100 | DeepSeek v4 Pro의 은닉 차원은 7168 ("hidden_size=7168 not supported (only 4096)") | 성격: 공표 | 언제 것: 2026-05
- L126 | MoE 전문가 가중치는 FP8이 아니라 네이티브 FP4(MXFP4)로 둘 수 있다 | 성격: 공표 | 언제 것: 2026-05
- L164 | W4A4(MXFP4) MegaMoE 경로가 존재: 가중치 4비트·활성값 4비트 | 성격: 공표 | 언제 것: 2026-06-02
- L241 | MoE 라우팅 경로: "softplus + sqrt + bias-add + Top-6 + gather + norm + multiply" 순서. 라우팅 후 Top-6 전문가를 고른다 | 성격: 공표(SGLang 트래커 항목 인용) | 언제 것: 2026-05
- L241 | MoE 블록에 shared expert와 routed expert가 따로 있고 각각 FC13(Linear1) 커널이 있다 ("both shared-expert and routed-expert FC13 are single kernels") | 성격: 공표 | 언제 것: 2026-05
- L239 | CSA의 인덱서에서 "Top-1024"를 고르는 단계가 언급된다 ("potentially fused with MulSum and even Top-1024") | 성격: 공표 | 언제 것: 2026-05
- L322 | 목표 컨텍스트: 1M (소제목 "Inference Optimizations for 1M Context Length") | 성격: 공표 | 언제 것: 2026-06
- 컨텍스트 길이(최대 토큰 수 수치)·층 수·전문가 총수·어텐션 헤드 수·어휘 크기·라이선스 | 원문에 없다

### 어텐션 구조 — CSA / HCA (Compressed Sparse Attention · Heavily Compressed Attention)
- L322 | DeepSeek v4는 CSA와 HCA를 쓰며 Multi-head Latent Attention(MLA)에서 벗어난다: "walking away from Multi-head Latent Attention (MLA)". 설계는 KV 캐시 크기 축소가 동기: "heavily motivated by KV cache size reduction" | 성격: 공표 | 언제 것: 2026-06
- L324 | HCA의 KV 캐시는 두 부분으로 이뤄진다. ① KV 임베딩의 슬라이딩 윈도우 ② 압축된 KV 엔트리 집합 | 성격: 공표 | 언제 것: 2026-06
- L324 | HCA의 압축 단위: 엔트리 하나가 m′개 토큰에 걸친 key/value를 하나로 압축한다 ("each entry compresses key / value into one and across m′ tokens") | 성격: 공표 | 언제 것: 2026-06
- L324 | HCA 압축률 m′ = 128 (DeepSeek V4 Pro 기준) | 성격: 공표 | 언제 것: 2026-06
- L328 | CSA는 HCA와 같은 KV 압축 기법을 쓰되 압축률이 낮다: m = 4 | 성격: 공표 | 언제 것: 2026-06
- L328 | CSA는 압축된 KV 엔트리 위에 희소 어텐션을 더 얹는다. 어떤 토큰에 어텐션할지 lightning indexer로 고른다 ("using a lightning indexer to select tokens to attend to") | 성격: 공표 | 언제 것: 2026-06
- L328 | CSA의 희소 어텐션은 DeepSeek v3.2의 DeepSeek Sparse Attention을 이어받은 것: "inherits DeepSeek Sparse Attention in DeepSeek v3.2" | 성격: 공표 | 언제 것: 2026-06
- L332 | CSA와 HCA를 교대로 쌓아("By interleaving CSA and HCA") KV 캐시를 크게 줄였다. 1M 컨텍스트에서 "50x KV cache reduction" | 성격: 공표 | 언제 것: 2026-06
- L332 | 50x가 어느 기준 모델 대비인지, 토큰당 KV 바이트 값은 원문에 없다 | 성격: 불명 | 언제 것: 2026-06
- L130 | 윈도 어텐션(SWA)을 돌리기 전에 각 쿼리의 윈도가 덮는 KV 캐시 슬롯을 먼저 알아야 한다. 이 준비 단계가 SWA-prepare이고, 이것을 Triton으로 구현한 것도 성능 향상에 기여 | 성격: 공표 | 언제 것: 2026-05
- L237 | HCA 블록 구성: Compressor가 붙어 있고, fc_qa + fc_kv 투영, q-norm/k-norm, RMSNorm + RoPE, InvRoPE가 있다. 희소 인덱스(topk_idx)를 쓰지 않는 "non-sparse MQA path"가 있고, MQA는 압축 KV 캐시와 SWA KV 캐시를 함께 읽는다 | 성격: 공표(SGLang 트래커 인용) | 언제 것: 2026-05
- L237 | HCA Compressor의 상태 갱신은 "kv-update + ape-Add + score-update" 세 부분으로 되어 있다 (ape = 원문 표기, 풀이 없음) | 성격: 공표 | 언제 것: 2026-05
- L239 | CSA 블록 구성: Indexer + Compressor. 압축기가 둘이다(fc_compressor와 fc_idx_compressor). 쿼리 투영도 둘이다(fc_qb와 fc_idx_qb) | 성격: 공표 | 언제 것: 2026-05
- L239 | CSA 인덱서 경로: "(RoPE +) Hadamard + MXFP4-quant fusion", "MXFP4 BMM+ReLU kernel". 인덱서가 MXFP4로 양자화된 키 위에서 BMM과 ReLU를 거쳐 Top-1024를 고른다 | 성격: 공표 | 언제 것: 2026-05
- L210 | vLLM에는 "FP4 Indexer"가 이미 구현되어 있다 | 성격: 공표 | 언제 것: 2026-05
- L294 | Ascend 쪽 오버랩 목록에 Prolog, Compressor, LightningIndexer가 나온다. "C4A Compressor can be completely hidden" (C4A = 원문 표기, 풀이 없음) | 성격: 공표 | 언제 것: 2026-06
- L302 | Ascend 구현에서 희소 어텐션 스케줄러와 LightningIndexer의 메타데이터는 런타임 시퀀스 길이·마스크·paged-KV 정보로부터 코어별 분할 텐서를 만든다. `SparseAttnSharedkv`와 `QuantLightningIndexer`가 그것을 받아 각 cube core가 맡을 Batch/Head/Q-block/K-block 작업을 정한다 | 성격: 공표 | 언제 것: 2026-06

### KV 캐시 관리의 어려움 (구조가 새로워서 생긴 것)
- L334 | CSA·HCA는 새로워서 서빙 프레임워크의 KV 캐시 관리가 어려워진다: "the novelty of CSA and HCA creates KV cache management challenges" | 성격: 저자 판단 | 언제 것: 2026-06
- L334 | vLLM의 KV 캐시 메모리 할당기는 prefix caching 같은 기능을 지원하면서 효율적인 메모리 로딩 패턴을 유지해야 한다 | 성격: 공표 | 언제 것: 2026-06
- L334 | 조치 ①: 논리 블록 크기를 CSA와 HCA의 KV 압축률 둘을 모두 나누는 값으로 정한다 ("a logical block size that divides the KV compression rates of both CSA and HCA") | 성격: 공표 | 언제 것: 2026-06
- L334 | 조치 ②: 페이지 크기 버킷팅으로 메모리 단편화를 피한다. 이유: KV 캐시, compressor 상태, indexer KV가 각각 엔트리당 크기가 다르다 ("storing the KV cache, compressor states, indexer KV, each having a different size per entry") | 성격: 공표 | 언제 것: 2026-06
- L218 | vLLM 로드맵의 KV 캐시 항목: PD + CPU 오프로딩(PR #39654)과 분산 KV 오프로딩 | 성격: 공표 | 언제 것: 2026-05
- L94 | 초기 ATOM 구현은 `kv_cache[:1,...]`을 하드코딩해 KV 캐시를 시퀀스 슬롯 하나에 고정했다. 두 번째 동시 요청은 KV 상태를 둘 곳이 없었고 배치 크기 1만 돌릴 수 있었다 | 성격: 공표(저자 관찰) | 언제 것: 2026-04
- L136 | 이후 sparse-attention OOM이 해소되어 eager 모드와 단일 시퀀스 상한을 없앴고, 배치 지원이 들어가 스윕이 conc=1에서 conc 1–512로 늘었다 | 성격: 공표 | 언제 것: 2026-05

### mHC (원문은 풀이 없이 "mHC"로만 적음)
- L96 | mHC pre-projection 커널이 층마다 쓰이는 연산으로 언급된다 (ATOM에서 AITER 커널이 크래시해 Torch로 대체) | 성격: 공표 | 언제 것: 2026-04
- L128 | "AITER mHC kernels, which are used at every layer" — mHC는 모든 층에서 쓰인다 | 성격: 공표 | 언제 것: 2026-05
- L100 | TensorRT-LLM의 `mhcFusedHcKernel.cu`는 `FHC_HIDDEN = 4096` 상수 하나가 박혀 있었고, SHAPE_K, residual/x TMA descriptor, MMA 커널 템플릿 인스턴스가 모두 이 은닉 크기에 묶여 있었다 | 성격: 공표 | 언제 것: 2026-05
- L235 | mHC 블록 최적화 목록: `fc_hc_fn` GEMM은 N 차원이 작아서 TF32/BF16과 특수 커널이 필요할 수 있다, 1/RMS + 곱 융합, 단일 커널 `hc_split_sinkhorn`과 `hc_post`, 어텐션과 MoE 블록 안에서 MulSum + RMSNorm(+ FP8/MXFP8 양자화) 융합 | 성격: 공표 | 언제 것: 2026-05
- 원문은 mHC의 수식·동작 원리를 설명하지 않는다. sinkhorn 단계가 있다는 이름(`hc_split_sinkhorn`)만 나온다 | 성격: 불명 | 언제 것: 2026-05

### MTP (Multi-Token Prediction)
- L82 | DeepSeek v4의 MTP 지원은 Day 3에 SGLang이 처음 냈다. MTP는 높은 interactivity에서 처리량을 크게 높였다 | 성격: 공표 | 언제 것: 2026-04 (Day 3)
- L140 | MTP가 하는 일: 메모리 바운드인 디코드의 컴퓨트 여유를 쓴다 ("exploits the compute slack in memory-bound decode") | 성격: 저자 판단 | 언제 것: 2026-06
- L140 | 대가: 컴퓨트 바운드인 큰 배치 디코드에서는 MTP 비용이 초안 토큰의 이득을 넘어서 처리량이 더 나쁘다 ("MTP tends to deliver worse results at higher throughput") | 성격: 저자 판단 | 언제 것: 2026-06
- L140 | AMD에서는 4주차에 모든 프레임워크에서 MTP가 동작했다 | 성격: 공표 | 언제 것: 2026-05
- L262 | MTP 벤치마크의 AR(acceptance rate)/AL(acceptance length)은 사용처마다 다르다. 예: 벤치마크에서는 평균 3개 중 2개 초안 토큰이 받아들여져도 실제 배치에서는 3개 중 1.5개만 받아들여질 수 있다 ("accept two draft token out of three ... only accepting 1.5 tokens out of three") | 성격: 저자 판단 | 언제 것: 2026-06
- L266 | Huawei CANN의 방식: 마지막 MTP 모듈에 맞춰 디코드 스텝 전체 시간을 재고 토큰당 시간이 아니라 디코드 스텝당 시간을 기록한다. 사용자가 자기 사용처의 MTP AL을 곱해 환산한다 | 성격: 공표 | 언제 것: 2026-04-24

### 결정론적 연산 (Determinism)
- L338 | 목적: RL 학습 안정성. DeepSeek은 연산을 결정론적으로 만드는 데 전력을 다했다 ("went all in on making computation deterministic"). GPU 커널과 롤아웃 인프라 양쪽에서 드러난다 | 성격: 저자 판단 | 언제 것: 2026-06
- L338 | 방법 ①: 모든 연산에 맞춤 커널을 직접 써서 배치 불변성(batch invariance)을 확보한다. 배치 크기와 무관하게 특정 reduction 순서를 강제한다 | 성격: 공표 | 언제 것: 2026-06
- L338 | 배치 불변 커널의 범위: split KV attention forward, GEMM, MoE backward 커널 | 성격: 공표 | 언제 것: 2026-06
- L338 | 대가: reduction 순서가 결정적이지 않은 인기 알고리즘 기법을 못 쓰게 되어 성능이 떨어진다 ("come at a performance loss") | 성격: 저자 판단 | 언제 것: 2026-06
- L338 | 완화책: 워크로드에 맞춘 커널, 예를 들어 행렬 모양별로 특화한 커널 | 성격: 공표 | 언제 것: 2026-06
- L338 | 롤아웃 인프라: 모든 롤아웃을 재현 가능하게 하려고 장애 허용에 집중했다 | 성격: 공표 | 언제 것: 2026-06
- L338 | 롤아웃 인프라 구현: 생성 요청마다 토큰 단위 write-ahead log를 둔다. 프리필이든 디코드든 중간에 선점된 요청은 재계산 없이 재개할 수 있다 | 성격: 공표 | 언제 것: 2026-06

### MegaMoE 동작 원리
- L342 | 배경 ①: 전문가 병렬(EP)을 쓰는 MoE는 먼저 토큰 dispatch all-to-all, 그다음 Linear1, Activation, Linear2, 마지막으로 토큰 combine all-to-all 순서다 | 성격: 공표 | 언제 것: 2026-06
- L342 | 배경 ②: Linear1과 Linear2는 grouped GEMM이다. 한 rank의 각 전문가가 자기 가중치를 자기에게 라우팅된 토큰에 적용한다 | 성격: 공표 | 언제 것: 2026-06
- L342 | 기존 구현(DeepSeek V4 논문이 언급): dispatch를 Linear1과, combine을 Linear2와 겹치거나 인터리브한다. 그래도 Linear1 - Activation - Linear2 경계에서 모든 전문가에 걸친 동기화(sync)가 남는다 | 성격: 공표 | 언제 것: 2026-06
- L342 | MegaMoE의 방법: 전문가를 wave(묶음)로 나누고 wave마다 따로 스케줄한다. 그러면 각 연산이 더 잘게 겹쳐서 통신 지연이 더 많이 가려진다 ("splits experts into waves and schedules each wave separately") | 성격: 공표 | 언제 것: 2026-06
- L342 | 저자의 비유: 분산 GEMM처럼 컴퓨트 커널과 그에 의존하는 통신 커널을 작은 조각으로 쪼개 파이프라인으로 겹치는 방식 ("distributed GEMM") | 성격: 저자 판단 | 언제 것: 2026-06
- L344 | 논문이 주장하는 이론적 속도 향상: DeepSeek v4 Flash 구성에서 naive 커널 대비 1.92x ("a theoretical speedup of 1.92x over the naive kernel in the DeepSeek v4 Flash configuration") | 성격: 회사 주장 | 언제 것: 2026-06
- L344 | 저자의 추론: 1.92x가 맞다면 naive 커널은 시간의 거의 50%를 dispatch·combine 통신에 쓴다 ("must spend close to 50% of its time on Dispatch and Combine communication") | 성격: 저자 판단 | 언제 것: 2026-06
- L342 | MegaMoE는 DeepSeek V4 릴리스에 포함되어 나온 새 fused MoE 커널이다 | 성격: 공표 | 언제 것: 2026-04
- L150 | DeepGEMM MegaMoE(SGLang, B300)의 설명: "a grouped FP4 MoE GEMM that keeps experts resident and does one mega-dispatch instead of per-expert kernels" | 성격: 공표 | 언제 것: 2026-04~05
- L150 | 같은 대목: B300에서 MegaMoE와 EP8 대신 EP4로 튜닝해 일주일 안에 3x 향상 ("a 3x improvement over less than a week") | 성격: 공표 | 언제 것: 2026-05
- L212 | vLLM: MegaMoE 지속 작업(PR #40833)과 NVFP4 지원이 Core model support 항목 | 성격: 공표 | 언제 것: 2026-05
- L210 | vLLM은 초기 MegaMoE 지원을 이미 구현했다 | 성격: 공표 | 언제 것: 2026-05

### Day 0 → Day 43 사이 소프트웨어 변경 중 모델 구조 때문에 생긴 것
- L100~L104 | TensorRT-LLM: Pro의 은닉 7168이 FHC_HIDDEN=4096 하드코딩과 충돌. NVIDIA가 가드를 지웠고, 그 뒤 일주일 넘게 기본 설정(fused HC on)에서 7,168 텐서가 4,096용 커널로 들어가 "corrupting hidden states and producing invalid generations". 회피책은 env var `TRTLLM_MHC_ENABLE_FUSED_HC=0`. SemiAnalysis가 PR #13710으로 고쳤고 NVIDIA가 PR #13771로 재베이스·머지 | 성격: 공표 | 언제 것: 2026-05
- L106 | 이 문제를 진단해 은닉 크기 불일치까지 좁히는 사이 Day 9가 됐다 | 성격: 공표 | 언제 것: 2026-05
- L124 | MI355X: Day 0는 FP8 빌드(4월 25일), 5월 27일에는 FP4 빌드. 이득은 거의 전부 PyTorch 네이티브 폴백 경로를 AITER, Triton, TileLang, FlyDSL 커널로 교체한 데서 나왔다 | 성격: 공표 | 언제 것: 2026-05-27
- L126 | 첫 커밋 뒤 가장 큰 개선: FP4 가중치 MoE가 동작해 MoE 전문가를 FP8에서 네이티브 FP4(MXFP4)로 바꿔 expert-weight 대역폭 개선. 같은 시기 FlashMLA와 sparse-attention indexer를 torch 폴백에서 TileLang 커널로 옮기고 HIP graph를 켰다 | 성격: 공표 | 언제 것: 2026-05
- L128 | AITER mHC 커널 도입(모든 층에서 쓰임) 후 MI355X가 낮은 interactivity에서 처음으로 H200을 넘었다 | 성격: 공표 | 언제 것: 2026-05
- L130 | SWA-prepare의 Triton 구현이 윈도 어텐션 쪽 개선에 기여 | 성격: 공표 | 언제 것: 2026-05
- L132 | 5월 19일 폴백 제거: FlashMLA를 TileLang에서 Triton으로, AITER FlyDSL FP4 MoE 커널 도입. 켠 것: fused hash-topk, DSv4 radix attention, fused store-cache, fused WQA/WKV projection, fused paged-compress. 동시성 스윕을 1024까지 늘려 이전에 없던 고처리량 구간이 생김 | 성격: 공표 | 언제 것: 2026-05-19
- L136 | ATOM: AITER 수정 #2916이 mHC 크래시의 원인인 device-allocation 버그를 바로잡아 해당 AITER 커널을 되살렸다. 이어 FP4 전문가가 AITER fused MoE 커널로 옮겨갔다(Triton override 제거) | 성격: 공표 | 언제 것: 2026-05
- L96 | 초기 ATOM의 폴백: FP4 MoE는 AITER `fused_moe`가 GFX950에서 깨져 Triton으로 강제, mHC pre-projection은 AITER 커널 크래시로 Torch로 패치, 그 결과 eager 실행 | 성격: 공표 | 언제 것: 2026-04
- L164 | GB300 SGLang MTP는 6월 2일 W4A4(MXFP4) MegaMoE 구현에서 가장 크게 개선. 이 날짜 버전의 개선은 커널·정밀도가 아니라 디코드 토폴로지 재작성에서 나왔다고 원문이 적는다 | 성격: 공표 | 언제 것: 2026-06-02
- L164 | Day 0 레시피는 EP=8(prefill 워커 1~2개 공급), 동시성 상한 16,384. 5월 20일 실행은 decode를 EP=16으로 넓히고 decode 워커당 prefill 4~12개, 동시성 21,504 | 성격: 공표 | 언제 것: 2026-05-20
- L166 | Wide EP가 핵심 지렛대: 더 많은 GPU에 걸친 가중치 로딩 분할 상환(amortized weight loading) | 성격: 저자 판단 | 언제 것: 2026-06
- L196 | 구조상 이유: DeepSeek V4의 MoE dispatch/combine all-to-all을 NVLink 안에 두려면 EP를 충분히 넓혀야 한다. NVL72는 72 GPU가 한 NVLink 도메인이라 가능 | 성격: 저자 판단 | 언제 것: 2026-06
- L74 | GB200 Day 0 레시피: prefill은 eager, KV 캐시 전송은 NIXL, disaggregated + WideEP. 독자 재현에서 B200 대비 낮은 interactivity 구간 최대 5x | 성격: 공표 | 언제 것: 2026-04-27
- L233 | SGLang 트래커의 세 목표: 디코드용 CUDA graph, 프리필용 piecewise CUDA graph, 런타임 가중치 처리 없음(weight prep은 스텝마다가 아니라 한 번). V4의 네트워크 다이어그램 블록별로 항목을 정리함 | 성격: 공표 | 언제 것: 2026-05
- L246 | SGLang의 초점: 작은 연산 사슬을 단일 융합 커널로 바꾸고, 새 어텐션 변종이 캐시를 제자리에서 읽게 하고, 디코드 경로를 CUDA graph로 완전히 끌어들이는 것 | 성격: 저자 판단 | 언제 것: 2026-06
- L241 | MoE 라우터 GEMM은 TF32/BF16 확인, 라우팅 경로 커널 수 최소화, 블록별 FP8·MXFP8 활성 양자화 융합, routed 전문가 앞 작은 정렬 커널 점검 | 성격: 공표 | 언제 것: 2026-05
- L214~L216 | vLLM 런타임·커널 로드맵: Model Runner V2, MTP 최적화, PD 최적화, 파이프라인 병렬, paged prefill 커널, fast top-k 커널, 수평 융합, DeepEP V2, DeepSeek 자체 TileKernels 통합. 하드웨어 쪽: Hopper 지원 완료, SM120과 AMD 남음 | 성격: 공표 | 언제 것: 2026-05
- L216 | DeepSeek의 자체 커널 라이브러리 이름: TileKernels | 성격: 공표 | 언제 것: 2026-05

### Ascend 쪽에서 드러난 모델 구조 (모델 연관만)
- L292 | DeepSeek flash v4를 Ascend 950DT에서 16-rank DP/EP 구성으로 돌린 3단계 프로파일(원문 표기 "DeepSeek flash v4"; 소제목은 "Pro 950DT Profile"로 되어 있어 L288과 L292가 서로 다르다) | 성격: 공표 | 언제 것: 2026-06
- L294 | 디코드 스텝에서 Prolog, Compressor, LightningIndexer를 겹칠 수 있고, shared expert 계산을 routed expert 실행 밑에 숨겨도 routed expert 성능이 떨어지지 않는다 | 성격: 공표 | 언제 것: 2026-06
- L298 | shared expert 계산이 routed expert 계산과 100% 겹치는 예 | 성격: 공표 | 언제 것: 2026-06
- L300 | 스트림 145-148은 메타데이터 스트림으로 디코드 패스마다 한 번 값 의존 스케줄러·타일링 메타데이터를 미리 계산한다. AI CPU 연산은 이것뿐이고 총 시간의 극소 부분이다. 긴 컨텍스트 벤치마크에서 영향이 더 클 것으로 본다 | 성격: 저자 판단 | 언제 것: 2026-06
- L308 | 디코드의 MC²(merged compute-communication) EP 연산: `MoeDistributeDispatchV2`와 `MoeDistributeCombineV2` | 성격: 공표 | 언제 것: 2026-06
- L310 | DeepSeek v4는 Day 0 지원이 있는 스택이 둘(CANN, CUDA). 작년 v3/R1 때는 CUDA 하나뿐 | 성격: 저자 판단 | 언제 것: 2026-06
- L250 | DeepSeek 공식 API 일부는 Day 0부터 Huawei에서 서빙 | 성격: 공표 | 언제 것: 2026-06

### 성능·비용 (모델 쪽에서 쓸 값만)
- L26 | AMD SGLang이 Day 26까지 100x 넘는 성능 향상(MI355X, DeepSeek v4 Pro) | 성격: 공표 | 언제 것: 2026-05
- L86 | MI355X Day 0 interactivity 1-2 tokens/user/s (FP8만 가능) | 성격: 공표 | 언제 것: 2026-04-25
- L176 | B200 vLLM, 50 tok/s/user에서 Day 0 300,000 tok/s/MW, 6월 5일 약 500,000 tok/s/MW | 성격: 공표 | 언제 것: 2026-06-05
- L180 | B200 all-in 전력 약 2.17 kW/GPU 고정이라 ~1.7x 증가는 순수 소프트웨어 이득 | 성격: 저자 판단 | 언제 것: 2026-06
- L182 | 처리량 프런티어를 민 최적화(MegaMoE grouped-FP4 GEMM, wider EP, FP4 weight path, 스케줄러 튜닝)가 전력 효율로 그대로 이어진다 | 성격: 저자 판단 | 언제 것: 2026-06
- L192 | GB300 + MTP, 50 tok/s/user, 입력 8k·출력 1k 토큰 가정에서 출력 100만 토큰당 $0.156 | 성격: 공표 | 언제 것: 2026-06-08
- L350 | 40-60 tok/s/user 구간에서 GB200 NVL72가 H200 대비 100만 토큰당 비용 10배 넘게 저렴. NVL 백플레인이 B200 InfiniBand의 18x 속도라 wide EP가 가능하다고 원문이 설명 | 성격: 공표 | 언제 것: 2026-06
- L158 | B200: TRT가 낮은 interactivity에서 우세하나 out of the box로 안 돈다 | 성격: 공표 | 언제 것: 2026-06
- L108 | TRT-LLM은 큰 배치에서 우세하고 높은 interactivity에서 뒤처진다 | 성격: 공표 | 언제 것: 2026-05

### 경쟁과 랩
- L24 | 중국이 오픈 모델 지형을 지배하고 있다. "Kimi K2.6 still beating ... Nemotron 3 Ultra on coding" | 성격: 저자 판단 | 언제 것: 2026-06
- L22 | vLLM과 SGLang 팀이 각각 회사(Inferact, RadixArk)를 세웠고 각각 수억 달러를 조달 | 성격: 공표 | 언제 것: 2026-06

### 원문에 없는 것
- 사전학습 토큰 수, 학습 컴퓨트, 데이터, 사후학습·RL 알고리즘·보상 설계, MFU, 병렬화(학습), 벤치마크 점수, 토큰 가격(API) | 원문에 없다 (결정론적 연산 대목이 RL 안정성 목적이라고만 언급)

확인한 줄: L100, L124, L164, L237, L241, L294, L324, L338, L342, L344
