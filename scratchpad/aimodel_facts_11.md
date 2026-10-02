# 사실표 11 — 학습벤치 / 코딩어시

## 학습벤치 (발행 2025-08-20)

### 벤치마크 방법·범위
- L15 | 2,000개 넘는 H100 GPU 벤치마크 실행 결과로 MFU, TCO, 100만 토큰 학습당 비용을 분석. 클러스터 규모 128 H100 → 2048 H100, NVIDIA 소프트웨어 버전별로도 본다 ("benchmark runs across over 2,000 H100 GPUs") | 성격: 저자 판단 | 언제 것: 2025-08
- L57 | NVIDIA DGXC Benchmarking Team의 DGX Cloud Benchmarking Scripts를 NVIDIA 내부 H100 EOS 클러스터(8×400 Gbit/s InfiniBand)에서 실행 ("8×400 Gbit/s InfiniBand networking") | 성격: 공표 | 언제 것: 2025-08
- L61 | 벤치마크는 NeMo Megatron-LM 기반. DGXC 팀은 TorchTitan 같은 네이티브 Torch DTensor 프레임워크로 범위를 넓힐 계획 ("plans to extend coverage to native Torch DTensor frameworks such as TorchTitan") | 성격: 공표 | 언제 것: 2025-08
- L91 | 저자 제안: NeMo-MegatronLM의 성능 기능은 늦어도 한 달 안에 네이티브 PyTorch로 올려야 한다. 많은 사용자가 FSDP2와 DTensor 기반 네이티브 PyTorch를 선호한다 ("upstreamed to native PyTorch after a month’s time at most") | 성격: 저자 판단 | 언제 것: 2025-08
- L93 | NeMo AutoModel 라이브러리는 Megatron-LM 외에 네이티브 PyTorch FSDP2 백엔드를 지원. 네이티브 PyTorch 3D+ 병렬화(DTensor)가 빠져 있고 사전학습 기능이 많이 부족하며 대부분 파인튜닝용이라고 본다 | 성격: 저자 판단 | 언제 것: 2025-08

### GPT-3 175B 학습 (128 H100, 2024년 소프트웨어 개선)
- L99 | NeMo-Megatron LM 버전별로 2024-01부터 2024-12까지 128 H100에서 GPT-3 175B 학습 벤치 ("starting from January 2024 and ending in December 2024") | 성격: 공표 | 언제 것: 2024-01~2024-12
- L101 | 병렬화: 128 H100, 데이터 복제본 4개. 복제본 하나는 32 GPU, 레이어마다 NVLink 도메인 4 GPU에 텐서 병렬(TP=4) 후 파이프라인 병렬 ("4 data replicas ... 32 GPUs ... TP=4") | 성격: 공표 | 언제 것: 2024-12
- L101 | GPT-3 175B는 TP=8(H100 NVLink 도메인 8 GPU 전체)보다 TP=4가 연산 강도(arithmetic intensity)가 높아 낫다 | 성격: 저자 판단 | 언제 것: 2025-08
- L103 | GPT-3 175B 은닉 차원 12,288. TP=8이면 K 축 환원 차원이 1,536으로 작아지고, TP=4면 3,072 ("hidden dimension is 12,288 ... K reduction dim of 1,536 ... 3,072") | 성격: 공표 | 언제 것: 2025-08
- L105 | 시퀀스 길이 2,048(원 GPT-3 논문 설정), 글로벌 배치 256 샘플. 옵티마이저 스텝 한 번 전에 500k 토큰(글로벌 배치 × 시퀀스 길이)을 본다 ("global batch size of 256 samples ... 500k") | 성격: 공표 | 언제 것: 2024-12
- L109 | BF16 MFU: 12개월간 34%에서 54%로, 학습 처리량 57% 개선 ("from 34% MFU to 54% MFU over the course of 12 months, amounting to a 57% improvement") | 성격: 공표 | 언제 것: 2024-01~2024-12
- L109 | 개선 원인: NVIDIA cuDNN/cuBLAS 엔지니어의 최적화된 fused wgmma 커널, NCCL 엔지니어의 통신에 SM을 적게 쓰는 최적화 collective 등 CUDA 스택 전체 최적화 | 성격: 저자 판단 | 언제 것: 2025-08
- L111 | FP8 MFU: 같은 기간 29.5%에서 39.5%로, 처리량 34% 개선 ("29.5% MFU to 39.5% MFU ... 34% improvement in throughput") | 성격: 공표 | 언제 것: 2024-01~2024-12
- L113 | GPU당 시간당 $1.42(렌탈 마진 제외) 가정 시 GPT-3 175B FP8 학습 비용이 2024-01 100만 토큰당 72센트에서 2024-12 54.2센트로 ("72 cents per 1M tokens ... 54.2 cents") | 성격: 추정 | 언제 것: 2024-12
- L113 | 원 학습 토큰 300B 기준 비용이 $218k(2024-01)에서 $162k(2024-12)로 | 성격: 추정 | 언제 것: 2024-12
- L115 | 에너지 계산 방식: 128 H100 클러스터 전체(GPU·CPU·네트워크·스토리지 등) 전력을 추산한 뒤 일반 코로케이션 데이터센터의 PUE를 곱해 토큰당 유틸리티 Joule을 구한다 | 성격: 추정 | 언제 것: 2025-08
- L117 | 미국 가구 평균 연간 에너지 소비(2022년) 10,791kWh, 약 38,847,600,000 Joules. 8,760시간으로 나누면 평균 1,232W ("10,791kWh ... 1,232 W") | 성격: 공표 | 언제 것: 2022
- L119 | 2024-12 버전 소프트웨어 기준 토큰당 FP8 2.46 Joule, BF16 3.63 Joule ("2.46 Joules for FP8 and 3.63 Joules for BF16") | 성격: 추정 | 언제 것: 2024-12
- L119 | 미국 가구 연간 에너지만큼이면 FP8 토큰 15.8B개를 학습한다. 300B 토큰 학습은 FP8 19가구, BF16 28가구의 연간 소비 에너지 ("15.8B FP8 tokens ... 19 annual US households ... 28 households") | 성격: 추정 | 언제 것: 2024-12
- L121 | GPT-3 학습비 $162k와 19가구 에너지는 과하지 않지만, 많은 실험과 실패한 학습 실행이 쌓여 미국의 AI 학습 에너지 증가를 만든다고 본다 | 성격: 저자 판단 | 언제 것: 2025-08

### 약한 확장 vs 강한 확장
- L127 | 강한 확장(strong scaling): 모델 크기와 글로벌 배치를 고정한 채 컴퓨트를 늘림. 암달의 법칙으로 속도 향상을 정량화 | 성격: 공표 | 언제 것: 2025-08
- L129 | 약한 확장(weak scaling): 일정한 시간에 더 큰 문제를 풀도록 컴퓨트를 늘림. AI 학습은 GPU를 늘려 모델 크기와 글로벌 배치(수렴에 따라)를 키우므로 본질적으로 약한 확장 | 성격: 공표 | 언제 것: 2025-08

### Llama 3 405B 학습 (약한 확장)
- L137 | 클러스터를 576 H100에서 2,304 H100으로 늘려도 FP8 MFU 약 43%, BF16 MFU 약 54%로 유지 ("hover around 43% MFU and 54% MFU respectively") | 성격: 공표 | 언제 것: 2025-08
- L137 | Llama 3 Herd of Models 논문의 실제 학습: 16k H100, 사전학습 BF16 MFU 41%, 시퀀스 길이 8192 ("16k H100s ... BF16 MFU of 41%") | 성격: 공표 | 언제 것: 2024
- L137 | 중간학습 컨텍스트 확장은 시퀀스 길이 131,072. 16개 노드에 걸친 컨텍스트 병렬이 필요해 링 어텐션 통신으로 MFU가 38%로 떨어진다 ("context parallelism across 16 nodes ... MFU dropping to 38%") | 성격: 공표 | 언제 것: 2024
- L141 | Llama 3 405B 15T 토큰 사전학습을 2,304 H100 클러스터 BF16으로 하면 100만 토큰당 $1.95, 사전학습 단계만 $29.1M. DeepSeek은 학습 한 번에 $5M ("$1.95 per million tokens ... $29.1M ... only $5M per training run") | 성격: 추정 | 언제 것: 2025-08
- L143 | 이 비용은 최종 성공 학습 한 번의 값이며 사전 실험, 연구자 인건비 등은 빠져 있다 | 성격: 저자 판단 | 언제 것: 2025-08
- L145 | Llama 3 405B는 GPT-3 175B보다 총 파라미터 약 2.3배 크고, 토큰당 유틸리티 Joule도 약 2.3배: 8.8 Joule 대 3.6 Joule ("8.8 Joules per token vs 3.6 Joules per token") | 성격: 추정 | 언제 것: 2025-08
- L147 | 가구 연간 에너지로 Llama 3 405B BF16 4.4B 토큰 학습. 15T 토큰 수렴까지는 미국 3,400가구의 연간 소비와 같은 에너지 ("4.4B tokens ... 3,400 US households") | 성격: 추정 | 언제 것: 2025-08

### Llama 3 70B 학습 (약한 확장)
- L151 | 64 H100에서 2,048 H100으로 늘리면 FP8 MFU가 38.1%에서 35.5%로 하락(저자는 약 10% 하락으로 표현) ("from 38.1% for 64 GPUs down to 35.5% for 2,048 GPUs") | 성격: 공표 | 언제 것: 2025-08
- L151 | 복제본당 배치 크기와 병렬화 전략은 불변(TP=4, PP=2, 컨텍스트 병렬=2), 데이터 복제본만 추가 ("TP=4,PP=2, and context parallel=2") | 성격: 공표 | 언제 것: 2025-08
- L151 | BF16은 하락이 1~2%로 작다: 64 H100 54.5%에서 2,408 GPU 53.7%로. (원문은 2,048과 2,408 두 표기를 섞어 쓴다) | 성격: 공표 | 언제 것: 2025-08
- L155 | Llama 3 405B는 70B보다 5.7배 크다. 밀집 모델은 FLOPs가 파라미터에 선형이므로 비용도 5.7배여야 하나, 약 2k H100 규모 BF16 100만 토큰당 비용은 5.4배 ("5.7x larger ... 5.4x more expensive") | 성격: 추정 | 언제 것: 2025-08
- L157 | FP8 학습은 2,408 H100이 64 H100보다 토큰당 에너지가 10% 더 든다. 15T 토큰 FP8 수렴까지 64 H100은 440가구, 2,048 H100은 472가구의 연간 에너지 ("440 US households ... 472") | 성격: 추정 | 언제 것: 2025-08

### Llama 3 8B 학습 시간 추이
- L161 | Llama 3 8B는 텐서·파이프라인 병렬 없이 NVLink 도메인 내 GPU 쌍마다 8,192 시퀀스에 컨텍스트 병렬, 나머지는 데이터 병렬 | 성격: 공표 | 언제 것: 2025-08
- L161 | 2024-11부터 2025-04까지 성능은 소폭만 개선("only improved slightly"). 2025-04는 Hopper 대량 배치 후 23개월째 | 성격: 공표 | 언제 것: 2025-04

### DeepSeek 670B MoE: GB200 NVL72 대 H100
- L173 | 2025-05(GB200 NVL72 대량 배치 2개월 후) GB200의 TCO당 성능은 H100을 못 넘었고, 2025-07(5개월 후) 1.5배에 도달. 이 추세면 3~6개월 내 2.7배 가능으로 본다 ("reach 1.5x ... 2.7x that of the H100 within the next 3-6mths") | 성격: 저자 판단 | 언제 것: 2025-07
- L177 | 2025-05 DeepSeek 670B 학습에서 GB200의 Token/s/GPU는 H100보다 30% 높을 뿐 ("only 30% better") | 성격: 공표 | 언제 것: 2025-05
- L179 | 2025-07 GB200 NVL72의 Tokens/s/GPU는 H100의 2.5배. NVIDIA의 2025-12 소프트웨어 개선 예상치로 BF16에서 4.7배, MFU 42.0%가 될 것으로 추정 ("2.5x greater throughput ... 4.7x better performing ... MFU of 42.0%") | 성격: 추정 | 언제 것: 2025-07, 2025-12 전망
- L179 | 프런티에서 FP8이 일반적이지만 안정성을 위해 BF16으로 되돌아가는 학습이 많다고 본다. 활성 파라미터가 매우 적은 극도로 희소한 MoE를 지향하는 이유는 서빙 추론 비용이 낮기 때문 ("insanely sparse MoE models with a very small number of active parameters") | 성격: 저자 판단 | 언제 것: 2025-08
- L183 | 2025-05 100만 토큰 학습 비용 GB200 $0.684 대 H100 $0.626으로 GB200이 7% 비쌈 ("$0.684 per M tokens vs $0.626") | 성격: 추정 | 언제 것: 2025-05
- L183 | 2025-07 GB200 $0.307, H100 $0.468. GB200이 50% 넘게 하락, TCO당 성능 1.5배 ("$0.307 per M tokens ... $0.468") | 성격: 추정 | 언제 것: 2025-07
- L185 | DeepSeek 670B 사전학습 14.8T 토큰. GB200 NVL72 BF16 사전학습 $4.5M(2025-07), NVIDIA 예측으로 2025-12 $2.5M. H100 대비 TCO당 학습 성능 2.76배 ("14.8T tokens ... $4.5M ... $2.5M ... 2.76x") | 성격: 추정 | 언제 것: 2025-07, 2025-12 전망
- L187 | 72 GPU 스케일업 도메인 덕에 64 GPU alltoall(전문가 병렬의 핵심)이 H100 클러스터 64 GPU보다 GB200 NVL72에서 18배 빠르다 ("run 18x faster on 64 GPUs in a GB200 NVL72") | 성격: 저자 판단 | 언제 것: 2025-08
- L189 | H100 BF16에서 DeepSeek 670B의 MFU는 16.6%, 밀집 Llama 3 405B는 54.5%. 이유: 토큰을 전문가로 보내고(dispatch) 다시 합치는(combine) 통신이 크게 늘어서 ("16.6% vs dense models such as Llama 3 405B which can achieve an MFU of 54.5%") | 성격: 공표 | 언제 것: 2025-08
- L189 | MoE 통신량은 top_k(토큰이 라우팅되는 전문가 수)에 O(n)로 비례. 4개 전문가에 보내면 1개일 때의 4배 | 성격: 공표 | 언제 것: 2025-08
- L191 | 2025-07 학습 전력 효율은 GB200 NVL72가 H100의 2.2배. 주로 FLOPS/watt 차이이고, 직접 칩 액체냉각(DLC)이 낮은 PUE를 가능케 한 효과가 부분적 ("2.2x more power efficient") | 성격: 추정 | 언제 것: 2025-07
- L191 | NVIDIA 예측 기준 2025-12 토큰당 Joule이 H100 대비 4배 낮을 수 있다. 100MW 유틸리티 전력 데이터센터가 4배 많은 토큰을 학습 ("Joules per token will be 4x lower") | 성격: 추정 | 언제 것: 2025-12 전망

### Llama 4 Maverick 400B MoE: GB200 NVL72 대 H100
- L195 | Llama 4 400B MoE(활성 파라미터 17B). 2025-05 FP8 토큰 처리량이 GB200 NVL72가 H100의 2.4배. DeepSeek 670B BF16의 30%와 대비 ("17B active parameters ... 2.4x better") | 성격: 공표 | 언제 것: 2025-05
- L197 | TCO 기준 GB200 NVL72가 50% 유리: 100만 토큰당 $0.061 대 H100 $0.093 ("$0.061 per M tokens trained vs $0.093") | 성격: 추정 | 언제 것: 2025-05

### GB200 NVL72 신뢰성·장애 (학습 시스템)
- L205 | GB200 NVL72 랙 구성: 컴퓨트 트레이 18개(서버), NVSwitch 트레이 9개, 구리 백플레인 카트리지 4개 ("18 servers (compute trays), 9 NVSwitch trays and 4 copper backplane cartridges") | 성격: 공표 | 언제 것: 2025-08
- L205 | 72 GPU 중 64개만 대규모 학습에 쓰고 나머지 8개(컴퓨트 트레이 2개)는 핫 스페어. 8개는 교체돼 내려가 있거나 선점 가능 워크로드를 돌린다 ("only 64 GPUs out of 72 GPUs ... 8 GPUs ... hot spares") | 성격: 저자 판단 | 언제 것: 2025-08
- L207 | Slurm 새 block/topology 기능의 --segment 플래그로 랙당 64 GPU 사용을 지정할 수 있으나, 스위치 트레이나 백플레인 카트리지 교체는 랙 전체를 비워야 해서 핫 스페어 8 GPU로는 해결이 안 된다. 스페어 랙을 따로 배치해야 한다 | 성격: 저자 판단 | 언제 것: 2025-08
- L203 | 백플레인 신호 무결성 문제로 초기 운영자가 XID 149 오류를 많이 겪는다 ("XID 149 errors") | 성격: 저자 판단 | 언제 것: 2025-08
- L211 | 백플레인 카트리지는 Paladin HD 암수 커넥터로 컴퓨트 트레이에 연결. 암 커넥터는 Bianca 보드 PCB 가장자리에 나사로 고정되며 나사 장력이 정확하지 않으면 커넥터 전체에 신호 무결성 문제가 생긴다 | 성격: 저자 판단 | 언제 것: 2025-08
- L215 | 수 커넥터는 구리 백플레인 케이블 끝에 있고 케이블이 컴퓨트 트레이와 NVLink 스위치 트레이를 잇는다. 스위치 트레이 안에서는 플라이오버 케이블이 암 커넥터에서 NVSwitch ASIC로 연결 | 성격: 공표 | 언제 것: 2025-08
- L219 | 고장 부품 식별만 몇 시간 걸릴 수 있다("upwards of a couple hours") | 성격: 저자 판단 | 언제 것: 2025-08
- L223 | 교체 순서와 시간: 컴퓨트 트레이 교체 1~4시간, 스위치 트레이 1~4시간(랙 전체 드레인 필요), 백플레인 8~24시간 ("1-4 hours ... 8 hours to 24 hours") | 성격: 저자 판단 | 언제 것: 2025-08
- L225 | 8 GPU Hopper 서버의 HGX 보드 교체는 숙련 기술자가 두어 시간 안에 서비스 복귀 ("under a couple hours") | 성격: 저자 판단 | 언제 것: 2025-08
- L227 | 백플레인 교체는 랙 보강대(stiffener) 10개를 제거하고 나사를 풀어야 접근 가능. 힘이 과하거나 부족하면 NCCL 타임아웃 | 성격: 저자 판단 | 언제 것: 2025-08
- L229 | Paladin HD 커넥터는 얇은 금 도금이며 최대 200회 결합 사이클("at most 200 mating cycles") 후 폐기 | 성격: 공표 | 언제 것: 2025-08
- L233 | 번인·진단 도구: Nvloom, multinode dcgmi diag ubergemm. 운영자는 더 정밀한 진단 기능을 원한다 | 성격: 저자 판단 | 언제 것: 2025-08
- L235 | 소규모 네오클라우드는 H100을 ssh 수작업으로 관리(512 H100, 서버 64대까지는 가능)하나, GB200 NVL72 랙 2개 144 GPU부터는 안 된다. 일상 관리를 자동화해야 하므로 GB200 학습 운영은 최상위 랩·하이퍼스케일러·CSP 몫. 네오클라우드는 GB200 NVL72 대신 HGX B200·B300을 택하는 경향 ("512 H100s (just 64 servers) ... 144 GPUs across two GB200 NVL72 racks") | 성격: 저자 판단 | 언제 것: 2025-08
- L239 | 2025-08 현재 GB200 NVL72 랙은 추론·소규모 실험·개발 작업에만 쓰인다. 일부 프런티어 랩은 GB200 NVL72의 스케일아웃 네트워크도 설치하지 않았다. MoE 추론에서 Hopper 대비 이득이 가장 크다 | 성격: 저자 판단 | 언제 것: 2025-08
- L19 | GB200 NVL72 대규모 학습 사례 아직 없음. 프런티어 규모 학습을 성공시킨 것은 H100·H200과 Google TPU뿐 ("no large-scale training runs done yet on GB200 NVL72") | 성격: 저자 판단 | 언제 것: 2025-08
- L243 | MTBI(평균 중단 간격): H100 2,000 GPU-days(미숙한 운영자)~5,000 GPU-days(가장 숙련된 운영자), GB200 NVL72 1,000~3,000 GPU-days ("2,000 GPU-days ... 5,000 GPU-days ... 1,000 GPU-days to 3,000 GPU-days") | 성격: 추정 | 언제 것: 2025-08
- L245 | GB200 NVL72는 스위치 트레이·백플레인 교체로 72 GPU가 내려가(폭발 반경), H100/H200/B200 서버의 8 GPU보다 스페어 랙이 더 필요하다 | 성격: 저자 판단 | 언제 것: 2025-08
- L249 | 2025-05 Llama 4 Maverick 400B 벤치에서 랙 내 선점 워크로드 GPU를 학습 비용으로 치면 GB200의 100만 토큰당 비용 우위가 50%에서 20%로 줄어든다 ("eroded from 50% cheaper to only 20% cheaper") | 성격: 추정 | 언제 것: 2025-05
- L251 | 선점 워크로드를 비용에 넣지 않더라도 대기용 스페어 랙 때문에 우위는 50%에서 30%로 줄어든다 ("only 30% cheaper") | 성격: 추정 | 언제 것: 2025-05
- L255 | 일반 B200이 보통 크기 모델 사전학습에서 GB200 NVL72보다 TCO당 성능이 좋아 보인다. 모델 크기가 커지거나 강화학습이 들어오면 GB200 NVL72가 다시 앞선다 ("vanilla B200 is better performance TCO than GB200 NVL72 for pretraining normal sized models") | 성격: 저자 판단 | 언제 것: 2025-08

### 비용 구조 (학습 한 번 환산 외, TCO 입력값 참고)
- L71 | GB200 NVL72의 GPU당 전체 자본비용은 H100의 약 1.6~1.7배(하이퍼스케일러·네오클라우드 자이언트·신흥 네오클라우드 세 구매자 유형 공통) ("about 1.6x to 1.7x") | 성격: 추정 | 언제 것: 2025-08
- L79 | GB200 NVL72 TCO는 H100의 약 1.6배. TCO당 성능 우위를 보려면 최소 1.6배 빨라야 한다 | 성격: 추정 | 언제 것: 2025-08
- L75 | GB200 칩 1200W 대 H100 700W | 성격: 공표 | 언제 것: 2025-08
- L89 | GCP a3-mega H100은 ClusterMAX 첫 공개에서 Llama 70B급 MFU가 평균보다 10% 낮고 8x7B MoE급은 15~20% 낮았다("10% worse than average MFU ... 15-20% worse") | 성격: 공표 | 언제 것: 2025-03

## 코딩어시 (발행 2026-04-24)

### 모델 출시·가격
- L20 | 3개월간 매주 하나 이상 주요 랩이 코딩용 체크포인트를 냈다. GLM-5.1, Qwen3.6-Plus, Kimi K2.6, Composer 2, Gemini 3.1 Pro가 "agentic coding", "long-horizon tasks"를 강조 | 성격: 공표 | 언제 것: 2026-04
- L28 | GPT-5.5는 "Spud"에 기반한 첫 공개 모델. 실패한 GPT-4.5 이후 OpenAI 첫 프리트레이닝 스케일업. NVIDIA·OpenAI가 100k GB200 NVL72 클러스터에서 "trained"라고 했지만 저자는 이 "training"이 사후학습(RL)뿐이며 그 규모에 도달한 적이 없다고 본다 ("this “training” is post-training (RL) only") | 성격: 저자 판단 | 언제 것: 2026-04
- L30 | GPT-5.5 API 가격 입력 100만 토큰당 $5, 출력 $30. GPT-5.4의 2배, Opus 4.7보다 약간 비쌈 ("$5 per million input tokens and $30 per million output tokens ... 2x more expensive than GPT-5.4") | 성격: 공표 | 언제 것: 2026-04
- L32 | GPT-5.5 priority 티어는 표준 요금의 2.5배. fast mode는 "2.5x faster for 6x the price" 식의 모호한 보장, priority는 구체적 SLA(예 > 50 tokens/sec > 99% of the time). 저자는 Opus 4.6 Fast만 실제로 쓰인다고 본다 | 성격: 공표 | 언제 것: 2026-04
- L34 | GPT-5.3-Codex-Spark는 Cerebras에서 돌리도록 만든 GPT-5.3의 증류 소형 모델. priority·fast mode(작은 배치, 추론 깊이 조정, 우선 큐)는 모델을 바꾸지 않는 방식이라 다르다 | 성격: 저자 판단 | 언제 것: 2026-04
- L38 | GPT-5.5 Pro는 ChatGPT와 API에서만. BrowseComp·FrontierMath SOTA, 가격은 GPT-5.4 Pro와 같은 $30/180 ("priced at the same $30/180 as GPT-5.4 Pro") | 성격: 공표 | 언제 것: 2026-04
- L40 | 추론 수준: xhigh, high, medium, low, non-reasoning. 높을수록 출력은 낫지만 토큰이 더 들고 응답이 느리다 | 성격: 공표 | 언제 것: 2026-04

### 토큰 효율과 작업당 비용
- L42 | OpenAI 모델 카드: GPT-5.5가 5.4보다 벤치마크 점수가 높으면서 토큰은 적게 쓴다("token efficient"). 저자는 작업당 비용이 모델 가격을 결정하는 핵심 지표라고 본다 ("cost per task, not cost per token, is the true north star metric") | 성격: 저자 판단 | 언제 것: 2026-04
- L42 | Mythos는 토큰당 Opus의 5배 비쌀 수 있으나 같은 문제를 더 적은 토큰으로 풀어 인상분이 상당 부분 상쇄된다. 응답도 더 빠를 수 있다 ("Mythos may be 5x more expensive than Opus on a per token basis") | 성격: 저자 판단 | 언제 것: 2026-04
- L366 | 하네스가 작업당 비용에 큰 영향. 프롬프트 캐싱, 입출력 비율, 도구 사용 패턴이 대부분 하네스로 결정 | 성격: 저자 판단 | 언제 것: 2026-04
- L366 | 예비 분석: Codex가 Claude Code보다 토큰 효율적. 평균 입출력 비율 80:1 대 100:1. 입출력 비율이 높으면 Mtok당 가격은 낮아지지만 Codex는 입력 토큰을 적게 써 더 싸다 ("average input/output ratio of 80:1 vs 100:1") | 성격: 추정 | 언제 것: 2026-04

### Opus 4.7 (모델 변경점)
- L48 | Opus 4.7은 Opus 4.6의 drop-in 대체, 작은 개선. Fast mode가 아직 없다. 일부 엔지니어는 품질을 약간 포기하고 "2.5x faster for 6x the price"를 택한다 | 성격: 저자 판단 | 언제 것: 2026-04
- L56 | 변경 ① 고해상도 이미지 지원, 프런트엔드 스타일링에 스크린샷을 쓰는 RL 목표 증가 (headless browser 테스트 대신) | 성격: 저자 판단 | 언제 것: 2026-04
- L58 | 변경 ② "xhigh" 추론 노력 옵션이 "high"와 "max" 사이에 추가 | 성격: 공표 | 언제 것: 2026-04
- L60 | 변경 ③ 사고(thinking) 내용은 기본 생략. 토큰 비용은 그대로 청구되고 보려면 옵트인 | 성격: 공표 | 언제 것: 2026-04
- L62 | 변경 ④ 태스크 예산(beta, API 전용): 효율적으로 끝내라는 제안 값. 너무 빡빡하면 지름길이나 거부. max_tokens는 출력 길이 하드 제한이라 다르다 | 성격: 공표 | 언제 것: 2026-04
- L64 | 변경 ⑤ 새 토크나이저: 더 세밀한 토큰 분할로 성능을 얻는 대신 총 토큰 사용량 증가. Anthropic이 직접 최대 35% 증가를 인정. 저자는 이를 사실상 35% 가격 인상으로 본다 ("increases up to 35% in token usage. Implicitly, this is a 35% increase in price") | 성격: 회사 주장 | 언제 것: 2026-04
- L69 | 행동 변화: 4.7은 기본적으로 도구 호출을 덜 쓰고 추론을 더 쓴다. Anthropic은 추론 노력을 high에서 xhigh나 max로 올려 도구 사용을 늘리라고 제안. 사용자가 그렇게 하는 것은 발표가 주장한 토큰 효율 트레이드오프와 다르다고 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L73 | 2026-04-23 Anthropic 포스트모템: 3~4월에 발견된 버그 3개가 몇 주간 Claude Code 사용자 거의 전체에 영향 | 성격: 공표 | 언제 것: 2026-04-23
- L77 | 버그 기간: 3월 4일~4월 7일, 3월 26일~4월 10일, 4월 16일~4월 20일 ("March 4 to April 7, March 26 to April 10, and April 16 to April 20") | 성격: 공표 | 언제 것: 2026-04

### DeepSeek V4 사양과 구조
- L85 | DeepSeek-V4-Pro 1.6T 총 / 49B 활성, DeepSeek-V4-Flash 284B 총 / 13B 활성. V3는 671B 총 / 37B 활성 ("1.6T total / 49B active ... 284B total / 13B active ... 671B total / 37B active") | 성격: 공표 | 언제 것: 2026-04
- L85 | 두 구조 모두 클로즈드 프런티어보다 총·활성 파라미터에서 의미 있게 뒤처진다고 본다 ("meaningfully behind") | 성격: 저자 판단 | 언제 것: 2026-04
- L87 | V3 대비 핵심 진전은 컨텍스트 128k에서 1M으로. 기술 개선이 모두 롱컨텍스트 성능에 집중 | 성격: 공표 | 언제 것: 2026-04
- L89 | 신기법 이름: Compressed Sparse Attention (CSA), Heavily Compressed Attention (HCA), Manifold-Constrained Hyper-Connections (mHC). 원문은 동작 원리를 설명하지 않는다 | 성격: 공표 | 언제 것: 2026-04
- L98 | DeepSeek 주장: 1M 토큰 컨텍스트에서 DeepSeek-V4-Pro는 DeepSeek-V3.2 대비 단일 토큰 추론 FLOPs 27%, KV 캐시 10%만 필요. 저자는 KV 캐시 90% 감소로 읽는다 ("requires only 27% of single-token inference FLOPs and 10% of KV cache compared with DeepSeek-V3.2") | 성격: 회사 주장 | 언제 것: 2026-04
- L112 | DeepGEMM 안의 Mega-Kernel이 NVIDIA GPU와 Huawei Ascend NPU 지원을 주장하나 공개 코드는 SM90(Hopper)·SM100(Blackwell)뿐. 파라미터 크기가 FP4에서 8x H20 HGX 메모리 도메인에 간신히 들어간다 ("fits just inside the memory domain of an 8x H20 HGX at FP4") | 성격: 저자 판단 | 언제 것: 2026-04
- L394 | 각주: 표에는 FP8로 표시하나 MoE 전문가 파라미터는 FP4, 대부분의 다른 파라미터는 FP8 ("MoE expert parameters use FP4, while most other parameters use FP8") | 성격: 공표 | 언제 것: 2026-04
- L83 | V4가 공개한 것: 가중치, 상세 기술 보고서, DeepEP·DeepGEMM·FlashMLA 갱신 | 성격: 공표 | 언제 것: 2026-04

### DeepSeek V4 추론 처리량
- L124 | InferenceX 팀의 day-zero H200 FP8 지원: 8k in 1k out, 20 tok/sec 상호작용에서 GPU당 처리량 약 150 tok/sec. 비교로 V3는 같은 조건에서 약 1.3k~2.3k tok/sec ("~150 tok/sec throughput per GPU at 20 tok/sec interactivity on 8k in 1k out ... ~1.3k to 2.3k tok/sec") | 성격: 공표 | 언제 것: 2026-04
- L124 | 신모델이라 몇 주 안에 큰 최적화를 기대한다 | 성격: 저자 판단 | 언제 것: 2026-04

### 성능·벤치마크
- L100 | DeepSeek은 표준 벤치마크가 실제 능력을 못 잰다며 자체 에이전트 벤치마크(중국어 글쓰기, 검색 증강, 장기 화이트칼라 작업, 코딩)를 도입. V4 Pro는 상위 모델과 경쟁하나 어려운 중국어 글쓰기는 Opus 4.7이 앞선다 | 성격: 회사 주장 | 언제 것: 2026-04
- L102 | 랩은 이해관계 때문에 일부 벤치마크만 발표해 공개 점수는 실제 성능의 대리 지표로 신뢰하기 어렵다고 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L128 | DeepSeek V4는 프런티어 바로 뒤. 클로즈드 모델의 가장 저렴한 대안이지만 능력은 선두가 아니다 ("right behind the SOTA frontier") | 성격: 저자 판단 | 언제 것: 2026-04
- L198 | MMLU: 2020년 학술 연구진 공개, 15,908 객관식 문항, 57과목, 4지선다 ("15,908 multiple choice questions covering 57 subjects") | 성격: 공표 | 언제 것: 2020
- L204 | MMLU는 2023-03 GPT-4가 86.4%로 사실상 포화. 한 논문은 MMLU 문항의 6.49%에 오류가 있다고 추정 | 성격: 공표 | 언제 것: 2023-03
- L221 | Humanity's Last Exam(HLE): 2025-01 Scale AI 공개, 전문가 1000명 이상이 2500문항 작성. 80%는 정확 일치 단답, 20%는 객관식 | 성격: 공표 | 언제 것: 2025-01
- L225 | 한 연구에서 HLE 화학·생물 문항의 30%가 동료 심사 문헌과 답이 충돌 ("30% of HLE chemistry/biology questions") | 성격: 공표 | 언제 것: 2025
- L227 | 랩이 RL 단계에서 이런 벤치마크를 힐클라임한다. Google은 2025년에 HLE류 STEM 문항용 9자리 수 예산을 Mercor·Surge·Handshake에 썼다고 하며, Gemini 3 Pro가 이 벤치마크에서 단계적 도약 ("9 figure budget in 2025") | 성격: 저자 판단 | 언제 것: 2025
- L237 | SWE-bench(2023): 12개 Python 저장소에서 자동 수집. 약 93k 병합 PR → 약 11k(이슈 연결, 새 테스트 도입) → 2294개(새 테스트 하나 이상이 직전 커밋에서 실패) ("~93k merged PRs ... ~11k ... 2294 PRs") | 성격: 공표 | 언제 것: 2023
- L248 | SWE-bench 판정: 기존 테스트가 깨지지 않고(pass-to-pass) 새 테스트가 모두 통과(fail-to-pass). 모델은 새 테스트를 볼 수 없고 코드를 실행할 수 없다 | 성격: 공표 | 언제 것: 2023
- L250 | 작업 생성에 사람 검증이 없어 이슈가 모호하고 테스트가 구현 세부에 묶이거나 불완전해 정답을 잘못 거부하거나 일부만 한 것을 통과시킨다. 한 작업은 문제 설명에 없는 19단어 오류 메시지를 일치시키라고 요구 (L259) | 성격: 저자 판단 | 언제 것: 2026-04
- L263 | SWE-bench verified(2024-08, OpenAI): Python 개발자 93명이 수작업 검토해 2294개를 500개로 줄임. bash 도구 추가, 작업별 Docker 컨테이너화 ("93 python devs ... 500 “verified” tasks") | 성격: 공표 | 언제 것: 2024-08
- L265 | 2026-02 OpenAI가 SWE-bench verified 보고 중단 | 성격: 공표 | 언제 것: 2026-02
- L267 | 중단 이유 ① o3가 일관되게 실패한 138문제 중 절반 넘게 여전히 불공정한 평가 ("Of the 138 problems consistently failed by o3, over half still had unfair evals") | 성격: 회사 주장 | 언제 것: 2026-02
- L269 | 중단 이유 ② 오염: GPT-5.2, Opus 4.5, Gemini 3 Flash가 일부 정답을 암기한 증거 | 성격: 회사 주장 | 언제 것: 2026-02
- L274 | OpenAI는 SWE-bench Pro 보고를 권고. Scale 제작, 더 어렵고, 덜 허용적인 라이선스의 공개 저장소와 비공개 저장소 사용, 계약자가 평가와 문제 설명 작성. 저자는 두 문제를 완전히 풀지는 못한다고 본다 | 성격: 회사 주장 / 저자 판단 | 언제 것: 2026-02
- L278 | SWE-bench multilingual은 9개 언어. Terminal-bench는 크라우드소싱. NL2Repo는 104개 오픈소스 Python 저장소를 자연어 요구문서로 역설계해 AI가 저장소를 재구성 (L282) | 성격: 공표 | 언제 것: 2026-04
- L289 | GDPval: 2025-09 OpenAI 공개, 44개 직업의 실제 경제적 가치 작업. 계약자가 문제·예시 해답·채점 기준(rubric) 3가지 제공 ("44 different jobs") | 성격: 공표 | 언제 것: 2025-09
- L304 | GDPval 평가는 전문가 계약자가 AI 결과를 사람 해답과 비교. AI 채점기도 있으나 전문가만큼 신뢰할 수 없어 공식 결과는 사람 전문가 사용 | 성격: 공표 | 언제 것: 2025-09
- L308 | GDPval-aa는 공개 GDPval 작업에 LLM 심판을 붙인 것 | 성격: 공표 | 언제 것: 2026-04
- L312 | GDPval 한계: 지나치게 명확한 프롬프트, 모호성 없음, 단일 턴(피드백 반복 없음) | 성격: 저자 판단 | 언제 것: 2026-04
- L316 | 기타 에이전트 벤치마크: Apex Agents(Mercor, 은행·컨설팅·법률, LLM 심판), Finance Agent(SEC 공시, 루브릭은 GPT-4o 생성 후 사람 검토), BrowseComp, OSWorld(CS 학생 9명 제작), Tau-bench(Sierra, 상태와 정확 문자열 일치) | 성격: 공표 | 언제 것: 2026-04
- L331 | Mythos의 SWE-bench verified 10%+ 개선은 모두가 포화로 여긴 뒤라 의미가 있다 | 성격: 저자 판단 | 언제 것: 2026-04
- L333 | OpenAI가 GPT-5.4 발표에서 벤치마크를 거의 싣지 않고 Anthropic 모델과 비교하지 않았다. 저자는 한 달 전 나온 Opus 4.6에 크게 밀렸을 것이라 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L341 | GPT-5.5 발표는 SWE-bench Pro 대신 "Expert-SWE"를 썼다. 글 하단에서 이유가 드러난다고 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L347 | GPT-5.5가 해당 코딩 벤치에서 Opus 4.7에 밀렸고 Mythos는 77.8% ("Mythos which scored 77.8%"). 저자: GPT-5.5는 일부 코딩에서 Opus 4.7보다 낫지만 전면 우위는 아니고, Mythos는 둘보다 한 단계 위로 추정 | 성격: 저자 판단 | 언제 것: 2026-04
- L355 | 저자 자체 벤치 수치가 OpenAI·Anthropic보다 낮은 이유 ① 두 랩은 성능을 높이려 맞춤형 비공개 하네스 사용 ② 비용 때문에 과제 부분집합만 실행(예 MCP atlas는 36개 MCP 서버 중 21개) ("21/36 MCP servers") | 성격: 저자 판단 | 언제 것: 2026-04
- L364 | 저자는 하네스가 이미 제품의 일부이므로 Codex 대 Claude Code가 사용자의 관심사라고 본다 | 성격: 저자 판단 | 언제 것: 2026-04

### 모델 간 체감 비교 (저자 테스트)
- L16 | GPT-5.5는 일부 작업에서 다른 모든 모델보다 "materially better", 프런티어에 도달했다고 본다. 11월 Opus 4.5 출시 때부터 6개월간 OpenAI 코딩 모델은 대부분 지표에서 세계 최고가 아니었다 | 성격: 저자 판단 | 언제 것: 2026-04
- L52 | 모델이 좋아져 일상 작업 대부분이 성공하고 비판은 스타일·접근·아키텍처·토큰 효율(속도)에 모인다 | 성격: 저자 판단 | 언제 것: 2026-04
- L136 | 엔지니어 평가: Codex는 변경 전에 인터넷과 코드베이스에서 훨씬 많은 세부 맥락을 끌어오고, 4.7은 빠른 탐색 뒤 바로 수정하는 느낌 | 성격: 저자 판단 | 언제 것: 2026-04
- L140 | Codex는 사용자의 진짜 의도를 추론하는 데 Claude Code보다 약하고 지시를 너무 문자 그대로 듣는다 | 성격: 저자 판단 | 언제 것: 2026-04
- L142 | GPT-5.5는 코드 변경에 너무 보수적. 토큰 효율은 좋아지나 정확도를 잃는다. 4.6에서 4.7로 올 때도 비슷한 트레이드오프. 출력에 "narrow fix"가 보이면 재확인 신호 | 성격: 저자 판단 | 언제 것: 2026-04
- L154 | 대시보드 과제: Codex의 데이터가 Claude보다 훨씬 정확(둘 다 첫 시도는 불완전). Claude 수치 다수는 환각이고 TPU 차트에 NVIDIA GPU를 넣었다. Codex는 복잡하고 좁은 과제, Claude는 열린 신규 과제에 더 낫다고 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L156 | 워크플로: ① Claude로 계획·골격·첫 구현 ② Codex로 문제 해결·버그 수정 | 성격: 저자 판단 | 언제 것: 2026-04

### 경쟁·시장·가격 전략
- L372 | 두 마리 경주: OpenAI와 Anthropic. 오픈과 클로즈드 격차가 다시 벌어지기 시작. SpaceXAI가 Cursor 의사 인수 후 3위 가능성, Google은 RL을 정비하면 놀랄 수 있고 Meta Muse Spark는 뒤처짐 | 성격: 저자 판단 | 언제 것: 2026-04
- L374 | 바이브 코딩 스타트업의 ARR 합계는 한 자릿수 중반 억 달러대. 저자 추정으로 Anthropic ARR이 $9B에서 $40B로 폭증했고 대부분이 Claude Code 에이전트 코딩 덕 ("from $9B to $40B (our current estimate)") | 성격: 추정 | 언제 것: 2026-04
- L376 | Anthropic이 동일 기준 ARR에서 OpenAI를 넘었다고 본다 | 성격: 저자 판단 | 언제 것: 2026-04
- L380 | Anthropic 매출의 약 70%가 API 사용 ("~70% of revenue coming from API usage") | 성격: 추정 | 언제 것: 2026-04
- L384 | Anthropic은 고객 서비스에 컴퓨트 플릿의 50% 넘게 쓰지 않을 것으로 본다. 쿠르노 경쟁 틀에서 Evian 물. 수단: Opus 4.6 fast, 피크 시간 낮은 속도 제한, $20/월 구독에서 Claude Code 제거 시험, OpenClaw 같은 제3자 하네스 금지 | 성격: 저자 판단 | 언제 것: 2026-04
- L382 | OpenAI는 점유율을 되찾으려 하고 Codex 5.5는 Opus 4.7과 같은 급. 컴퓨트 제약이 OpenAI를 구한다고 본다. H100 렌탈 가격 계속 상승 | 성격: 저자 판단 | 언제 것: 2026-04

### 원문 한계
- 코딩어시 L370 에 "Behind the paywall, we’ll give our predictions" 문구가 있으나 L372 이후 예측 본문이 이어지고 각주(L394)로 끝난다. 유료 전용 문구로 끝나지 않는다.
- 학습벤치 클리핑 L255에서 끝나며 마지막 문장 이후 잘림 표시는 없다.
- 도해·표는 이미지로만 실려 있어 값을 뽑지 못한 것이 많다(코딩어시 L22, L36, L44, L108, L110, L353, L378, L388 등. 학습벤치 L107, L139, L153, L163, L181, L199, L253). 본문에 값이 풀려 있는 것만 적었다.

확인한 줄: L109, L189, L223, L183, L243 (학습벤치) / L98, L366, L64, L384, L112 (코딩어시)
