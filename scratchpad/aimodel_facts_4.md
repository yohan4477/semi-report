# 사실표 4 — GLM-HBM / GLM-DRAM

두 편은 본문이 사실상 같다. 아래 항목은 각 편의 자기 줄 번호로 따로 적었다. 두 편 사이에 값이 다른 곳은 없다. 다른 점은 파일 끝에 모았다.

원문에 없는 것(찾아봤으나 두 편 어디에도 없음): 층 수, 은닉 차원, 어텐션 헤드 수 외의 GLM-5 사양(헤드 수는 H = 64 한 값만 나온다), 어휘 크기, 컨텍스트 길이, 정밀도(모델 가중치 기준), 라이선스, 출시일, 사전학습 토큰 수, 학습 컴퓨트·GPU 시간, KV 캐시 바이트/토큰 계산식과 결과, 컨텍스트 길이별 HBM 사용량 표, DRAM/NAND TAM 크기 숫자. 제목은 HBM·DRAM 용량 영향을 말하지만 본문에 용량(GB)이나 시장 규모(달러) 값은 없다.

## GLM-HBM (발행 2026-09-28)

### 모델 사양 (GLM-5 / GLM-5.x)
- L87 | GLM-5(및 GLM-5.x 모델)는 총 744B, 활성 40B 파라미터의 mixture-of-experts 모델. "744B total, 40B active-parameter mixture-of-experts model" | 성격: 불명(원문이 사실로 서술) | 언제 것: 2026-09
- L87 | 토큰마다 공유 전문가 1개를 쓰고 256개 중 8개 전문가로 라우팅. 희소도(sparsity) 32. "1 shared expert and is routed through 8 out of 256 experts, which is sparsity 32" | 성격: 불명 | 언제 것: 2026-09
- L87 | DeepSeek Sparse Attention을 쓴다 | 성격: 불명 | 언제 것: 2026-09
- L152 | GLM-5의 쿼리 헤드 수 H = 64. DeepSeek V3.2 설정(H ~= 128 로 추정)의 절반 | 성격: 저자 판단(DeepSeek 쪽 H 는 계산으로 도출) | 언제 것: 2026-09
- L145 | MLA 계산에 쓴 값 d = 512, r = 64, b = 2. DeepSeek V3.2 설정으로 제시, GLM-5 설정에도 같은 d, r, b 를 대입 ("d = 512, r = 64, b = 2, H = 64") | 성격: 불명 | 언제 것: 2026-09
- L154 | GLM-5는 QK NoPE 차원을 128에서 192로 키웠다. 이유는 iso-FLOP·iso-parameter 조건에서 이 설정이 낫다는 ablation. 결과로 SDPA 헤드 차원이 192에서 256이 된다. 헤드 수 감소까지 감안해도 FLOP 33% 감소. "which is still a 33% FLOP reduction after considering the head number reduction" | 성격: 공표(ablation 결과를 원문이 전함) | 언제 것: 2026-09
- L107 | GLM-5와 DeepSeek V3.2 의 MLA 차원 구성에서 가장 눈에 띄는 차이는 쿼리 헤드 수와 쿼리-키 헤드 차원. 비교표는 그림이고 클리핑에 값이 없다 | 성격: 저자 판단 | 언제 것: 2026-09

### DSA 구성 (아키텍처 기법)
- L89 | DeepSeek Sparse Attention(DSA)은 DeepSeek V3.2 에서 도입. 두 부품: top K 토큰을 고르는 lightning indexer, 희소 Multi-Latent Attention(MLA) | 성격: 불명 | 언제 것: 2026-09
- L16 | 희소 어텐션은 가장 관련 있는 top-k 토큰만 보아 핵심 SDPA 연산의 메모리 소비와 대역폭 요구를 줄인다. 그러나 top-k 선택 연산이 보통 전체 컨텍스트를 HBM 에 올려 두어야 하므로 메모리 용량 병목은 안 없앤다. "the top-k selection operation typically requires the full context to be in HBM" | 성격: 저자 판단 | 언제 것: 2026-09
- L26 | 희소 어텐션은 SDPA 단계의 KV 캐시 메모리·대역폭 요구를 줄이지만 전체 메모리 용량 사용은 안 줄인다. 희소 어텐션의 메모리 프로파일만으로는 시스템 KV 캐시 효율의 전체 그림을 못 그린다 | 성격: 저자 판단 | 언제 것: 2026-09
- L56 | GLM 은 기록 처리 비용을 두 방식으로 줄인다. KV 압축은 토큰당 저장하는 캐시 상태를 줄이고, 희소 어텐션은 어텐션 연산 1회가 읽는 상태를 줄인다. 그다음 서빙 엔진이 캐시를 어디 두고 어떻게 가져올지 정한다 | 성격: 불명 | 언제 것: 2026-09

### Lightning indexer 동작 (단계별)
- L93 | ① 기능은 경량 어텐션과 비슷하다. 쿼리와 키를 낮은 차원으로 하향 투영하고, 인덱서 쿼리는 멀티헤드, 인덱서 키는 단일 헤드 | 성격: 불명 | 언제 것: 2026-09
- L93 | ② 인덱서는 선택용 점수(logits)만 필요하므로 value 임베딩과 정규화용 softmax 가 필요 없다 | 성격: 불명 | 언제 것: 2026-09
- L93 | ③ 쿼리-키 내적을 계산하고 ReLU 비선형을 건다 | 성격: 불명 | 언제 것: 2026-09
- L93 | ④ 토큰의 인덱서 점수는 모든 쿼리 헤드에 걸친 logits 의 가중합. 이 점수로 top K 토큰을 고른다 | 성격: 불명 | 언제 것: 2026-09
- L93 | ⑤ 인덱서가 멀티헤드여도 토큰 선택은 여러 어텐션 헤드가 공유한다. "token selection is shared across multiple attention heads" | 성격: 불명 | 언제 것: 2026-09
- L93 | ⑥ K 개 미만의 토큰에 어텐션하는 쿼리는 dense 어텐션을 유지하고, 그 외에만 top K 를 고른다 | 성격: 불명 | 언제 것: 2026-09
- L101 | top K 는 2048. 그래서 2K 미만 길이의 어텐션은 dense. "The 2K minimum is due to top K being 2048" | 성격: 불명 | 언제 것: 2026-09

### Sparse MLA 동작: MHA 모드 대 MQA 모드
- L101 | MLA 는 두 모드로 동작한다. MHA 모드는 FLOPs 가 낮지만 메모리 비용 42x 높음. MQA 모드는 메모리 비용이 낮지만 FLOPs 가 최대 3.4x 높음. "MHA mode has lower FLOPs but 42x higher memory cost, MQA mode has lower memory cost but up to 3.4x higher FLOPs" (Kimi K3 글에서 설명했다고 원문이 밝힘) | 성격: 불명 | 언제 것: 2026-09
- L101 | DSA 는 MQA 모드를 쓴다. 희소 어텐션은 적은 토큰을 보므로 높은 FLOPs 가 완화된다 | 성격: 불명 | 언제 것: 2026-09
- L101 | 실제로는 시퀀스 길이 임계값 아래에서 MHA 모드가 MQA 모드보다 효율적이다. 짧은 길이에서는 메모리 적재 시간이 지배적이지 않아 FLOPs 가 낮은 MHA 가 유리하다는 직관 | 성격: 저자 판단 | 언제 것: 2026-09
- L101 | vLLM 은 MHA 모드를 시퀀스 길이 2K ~ 약 5K(data parallel), 2K ~ 약 77K(tensor parallel)에 설정한다. "2K to about 5K for data parallel, and 2K to about 77K for tensor parallel" | 성격: 불명(구현 설정) | 언제 것: 2026-09

### MLA 디코드 산술 강도 유도 (수식 그대로)
- L111 | 주장: MLA 의 SDPA 디코드 산술 강도는 H800 의 ridge point 근처. GLM-5 기술보고서가 DeepSeek 이 H800 roofline 에 맞춰 쿼리 헤드 수를 골랐다고 언급한다고 원문이 전하고, 저자는 이것이 위 사실을 가리킨다고 본다("This is likely referring to") | 성격: 저자 판단 | 언제 것: 2026-09
- L113-121 | 기호: L 시퀀스 길이, d 헤드 차원, r RoPE 차원, H 헤드 수, b 파라미터당 바이트 | 성격: 공표 | 언제 것: 2026-09
- L126-130 | MQA 모드 FLOPs: `2 * H * L * (d+r)` (P = Q [H, d+r] @ K.T [d+r, L]), `2 * H * L * d` (O = P [H, L] @ V [L * d]) | 성격: 저자 도출 | 언제 것: 2026-09
- L132-136 | MQA 모드 적재 메모리: `b * H * (d+r)` (Q), `b * L * (d+r)` (K and V) | 성격: 저자 도출 | 언제 것: 2026-09
- L138-143 | 산술 강도 = `(2 * H * L * (2 * d + r)) / (b * (d+r) * (L + H))`, L >> H 이면 `(2 * H * (2 * d + r)) / (b * (d + r))` | 성격: 저자 도출 | 언제 것: 2026-09
- L145-148 | DeepSeek V3.2 설정(d = 512, r = 64, b = 2) 대입: `(2 * H * (2 * 512 + 64) / (2 * (512 + 64)) ~= 2 * H` | 성격: 저자 도출 | 언제 것: 2026-09
- L150 | H800 의 실효 산술 강도 258.2 FLOP/B (실효 피크 865 TFLOP/s, 대역폭 3.35 TB/s, DeepSeek 출처). 대입하면 H ~= 128. "H800's practical arithmetic intensity is 258.2 FLOP/B" | 성격: 공표(DeepSeek 수치 인용) | 언제 것: 2026-09
- L152 | GLM-5 설정(d = 512, r = 64, b = 2, H = 64)의 산술 강도는 120.8 FLOP/B | 성격: 저자 도출 | 언제 것: 2026-09
- L152 | 저자는 GLM-5 가 약 128 FLOP/B 인 Moore Threads MTT S4000 에 맞춰 최적화됐다고 의심한다("we suspect"). 근거는 Moore Threads 와 Z.ai 의 협업(GLM-5.3-Flash day 0 지원) | 성격: 저자 판단 | 언제 것: 2026-09

### IndexShare (IndexCache)
- L158 | 컨텍스트가 길어지면 인덱서의 지연 비용이 무시할 수 없게 된다. Z.ai 는 GLM-5.2 에서 IndexShare(IndexCache)를 제안: DSA 층 4개마다 인덱서 하나를 공유 | 성격: 공표 | 언제 것: GLM-5.2 (2026-09 기준 글)
- L162 | 표준 DSA 학습은 두 단계: ① dense warm-up, 인덱서를 뺀 모든 가중치를 동결하고 어텐션은 dense ② sparse adaptation, 전체 모델을 희소 어텐션으로 학습 | 성격: 불명 | 언제 것: 2026-09
- L166 | 학습 목표: 표준에서는 인덱서를 어텐션 헤드 점수의 합에 맞추며 KL divergence 를 쓴다. IndexShare 는 이를 공유 층들의 어텐션 점수 평균 분포에 인덱서 logit 분포를 맞추는 것으로 바꾼다 | 성격: 불명 | 언제 것: 2026-09
- L168 | 추론: 보통 인덱서는 키를 캐시한다(어텐션이 KV 를 캐시하듯). 여러 층이 인덱서 하나를 공유하므로, 공유 층에서 top K 선택을 재사용하려면 full 층에서 top K 인덱스를 추가로 캐시해야 한다 | 성격: 불명 | 언제 것: 2026-09
- L170 | 효과: 인덱서 캐시 75% 감소, 인덱서 FLOPs 75% 감소, 컨텍스트 길이와 prefill/decode 에 따라 처리량 1.5x ~ 1.8x. "reduces indexer cache by 75%, reduces indexer FLOPs by 75%, and boosts throughput by 1.5x to 1.8x" | 성격: 공표(IndexCache 논문의 30B DSA 모델 그림 기준으로 보임) | 언제 것: 2026-09
- L160, L172 | 지연 비용과 베이스라인 대 GLM-5.2 설정 그림은 30B DSA 모델 기준. 값은 그림에만 있다 | 성격: 불명 | 언제 것: 2026-09

### 사후학습 파이프라인
- L178 | 사전학습·미드트레이닝 후 GLM-5 사후학습: SFT, 이어서 RL 3단계(reasoning RL, agentic RL, general RL), 마지막으로 on-policy cross-stage distillation(reasoning RL 과 general RL 을 SFT 체크포인트로 되돌려 증류) | 성격: 공표(기술보고서 기반) | 언제 것: GLM-5
- L182 | 기술보고서는 reasoning RL 모델이 entirely on-policy 로 학습됐다고 밝힌다. 저자는 동기 학습을 뜻한다고 본다. 동기 RL 은 시스템 효율이 낮고 학습 안정성은 높다 | 성격: 공표 + 저자 판단 | 언제 것: GLM-5
- L182 | on-policy cross-stage distillation 은 Multi-teacher On-Policy Distillation(MOPD, 학생 모델이 여러 교사 모델로 on-policy 증류하며 RL 학습)과 비슷하다. MOPD 의 목적은 전문가 교사를 한 모델로 합치는 것이나, GLM-5 쪽은 새 능력을 배우며 잃은 옛 능력을 회복하는 것으로 보인다 | 성격: 저자 판단 | 언제 것: GLM-5
- L182 | 저자는 reasoning RL 과 general RL 체크포인트만 교사로 쓰고 세 RL 체크포인트 전부를 안 쓰는 이유를 모르겠다고 적는다 | 성격: 저자 판단 | 언제 것: GLM-5
- L184 | 발표 블로그에 따르면 GLM-5.2 는 on-policy cross-stage distillation 을 표준 MOPD 로 대체했을 수 있다("may have"). Z.ai 는 이를 parallel OPD training 이라 부르며, 전문가 모델 10개 넘게를 약 이틀 학습으로 최종 모델에 합쳤다고 내세운다. "merged more than ten expert models into a final model by training for about two days" | 성격: 회사 주장 | 언제 것: GLM-5.2

### RL 알고리즘
- L190-196 | 동기 RL 단계: GRPO 기반에 현대적 변형 셋. ① KL 정규화 항 제거(시스템 효율, 더 공격적인 그래디언트 갱신) ② IcePop: 학습-추론 불일치 비율에 따른 토큰 단위 마스킹 ③ Clip-Higher: importance sampling 비율의 최대 문턱을 높여 탐색 장려 | 성격: 공표 | 언제 것: GLM-5
- L201 | 비동기 RL 단계: REINFORCE 류 알고리즘에 Direct Double-Sided Importance Sampling(DIS)을 더한다. DIS 는 IcePop 과 비슷한 클리핑 메커니즘 | 성격: 공표 | 언제 것: GLM-5
- L205 | IS 비율은 현재 정책과 behavior 정책 하에서 샘플된 행동의 확률을 비교해 각 행동의 기여를 스케일한다. 동기 단계의 behavior 정책은 직전 반복의 trainer 정책, 비동기 단계는 inference 정책 | 성격: 불명 | 언제 것: GLM-5
- L205 | 비동기에서는 롤아웃 중 정책 갱신이 여러 번이라 중간 체크포인트 버전이 전부 있어야 IS 비율을 정확히 구할 수 있으나, 메모리·지연 부담으로 불가능하다. 그래서 효율과 단순함을 위해 inference 정책을 쓰고 수치 안정성 문제를 감수한다 | 성격: 저자 판단 | 언제 것: GLM-5
- L209 | advantage 계산: RL 학습은 GRPO 표준 그룹 정규화 advantage, cross-distillation 은 reverse KL divergence | 성격: 불명 | 언제 것: GLM-5
- L203, L207, L211 | 토큰 단위 목적식·IS 비율·advantage 비교는 그림이고 클리핑에 수식이 없다 | 성격: 불명 | 언제 것: 2026-09

### Single-Rollout Asynchronous Optimization (SAO)
- L215 | 문제: 장기 과제는 궤적이 아주 길고, GRPO 에서는 궤적 길이의 분산이 커서 학습 신호가 불안정하고 긴 궤적으로 쏠릴 수 있다. RL 롤아웃은 종단 지연에 민감하므로 낙오 롤아웃의 꼬리 지연이 장기 과제에서 더 나빠진다 | 성격: 저자 판단 | 언제 것: 2026-09
- L215 | Z.ai 가 GLM-5.2 에서 SAO 도입. 그룹 정규화 advantage 를 PPO 에서 착안한 변형 GAE(Generalized Advantage Estimation)로 대체. GAE 는 롤아웃 하나만으로 advantage 를 계산하므로 프롬프트당 다중 롤아웃이 필요 없다 | 성격: 공표 | 언제 것: GLM-5.2
- L219 | GAE 는 value(현재 상태의 기대 반환)로 계산하고 value 모델이 추정한다. value 모델은 롤아웃을 입력받아 토큰마다 value 를 낸다 | 성격: 불명 | 언제 것: 2026-09
- L219 | SAO 는 agentic RL 에 맞춰 관측 토큰(도구 호출 결과)을 최적화에서 뺀다. GLM-5 에서는 그 토큰을 건너뛰는 것으로 충분했고, SAO 에서는 advantage 추정식을 고쳐 관측 토큰을 우회한다. Bellman target 과 ablation 은 SAO 논문 부록 A.1 참조 | 성격: 공표 | 언제 것: GLM-5.2
- L221 | value 모델은 정책 모델과 동시에 학습되는 별도 LLM. 학습 초기에 value 모델이 약해 advantage 분산이 높다 | 성격: 불명 | 언제 것: 2026-09
- L223-227 | value 모델 학습 기법 셋. ① Two Time-scale Update Rule: value 모델을 정책 모델의 2배 빈도로 갱신(정책 학습 스텝마다 각 데이터 배치를 2번 학습) ② Attention Parameter Freezing: value 모델의 full attention 층 동결 ③ Scaling Pre-training: value 모델 사전학습 코퍼스를 키워 초기화. Z.ai 는 코퍼스 규모를 공개하지 않았다 | 성격: 공표 | 언제 것: GLM-5.2
- L234 | 대가: 연산 오버헤드와 메모리 풋프린트 2배. 그 대신 그룹 샘플링을 value 모델로 바꿔 GRPO 의 지연 문제를 완화 | 성격: 저자 판단 | 언제 것: 2026-09

### 학습 시스템
- L238 | Z.ai 는 GLM-5 전 모델의 사후학습 인프라로 slime(오픈소스 RL 학습 프레임워크)을 쓴다 | 성격: 공표 | 언제 것: 2026-09
- L240 | 서버 기반 멀티태스크 롤아웃 오케스트레이터. 각 과제가 독립 마이크로서비스 서버로 롤아웃과 보상 로직을 맡고, 오케스트레이터가 과제별 롤아웃 비율과 생성 속도를 제어해 전체 성능을 균형 잡는다. Z.ai 는 GLM-5 학습 때 동시 롤아웃 1000개를 지원한다고 주장. "supports 1000 concurrent rollouts when training GLM-5" | 성격: 회사 주장 | 언제 것: GLM-5
- L244 | GLM-5.3 발표: 호스트 메모리에 더해 로컬 스토리지를 캐시 층으로 써서 MOPD 의 교사 모델 동적 전환과 프리페치를 가능케 한다고 Z.ai 가 주장 | 성격: 회사 주장 | 언제 것: GLM-5.3
- L244 | slime PR#1538 의 구현: `TensorBackuper` 클래스가 교사 가중치를 CPU 메모리에 고정된 PyTorch 텐서로 저장한다. 롤아웃이 교사로 라우팅되면 `TensorBackuper` 가 교사 모델을 GPU 메모리로 복사해 forward 를 수행한다. 이는 CPU 기반 가중치 스와핑이고, 스토리지 기반 구현은 아직 못 봤다고 저자가 적는다 | 성격: 공표(오픈소스 코드) + 저자 판단 | 언제 것: 2026-09

### 추론에서 드러나는 성질: 계층 메모리와 KV 오프로딩
- L20 | SGLang 팀의 HiSparse: KV 캐시 항목을 디바이스 HBM 에서 호스트 DRAM 으로 선제 오프로드하는 계층 메모리 시스템 | 성격: 공표 | 언제 것: 2026-04 (원문 링크 날짜 2026-04-10)
- L20 | 동작 ① LRU(Least Recently Used) 캐시처럼 동작 ② top-k 선택에서 캐시 미스가 나면 DRAM 에서 HBM 으로 토큰을 올림 ③ LRU 축출 정책으로 HBM 에서 DRAM 으로 내림 ④ 미스 지연을 줄이려 층 N 의 KV 캐시 적재를 층 N-1 의 실행과 겹침(layer-wise overlapping, 앞선 연구 HiCache 에서 도입) | 성격: 공표 | 언제 것: 2026-04
- L24 | HiSparse 로 SGLang 은 높은 동시성·긴 컨텍스트에서 처리량을 크게 올리나, top-k 캐시 미스 I/O 오버헤드가 대가. 수치는 그림에만 있다 | 성격: 공표 | 언제 것: 2026-04
- L18 | 그림 캡션: "Sparse attention throughput is bottlenecked by memory capacity" | 성격: 공표 | 언제 것: 2026-04
- L58 | B200 결과(InferenceX): 동시성이 8에서 16 요청으로 늘면 GPU 메모리에서 재사용된 프롬프트 토큰 비중이 90.3%에서 54.8%로 떨어지고, 호스트 메모리 재사용이 6.0%에서 40.3%로 오른다. 전체 캐시 히트율은 모든 동시성에서 95% 위 유지. "falls from 90.3% to 54.8%", "rose from 6.0% to 40.3%" | 성격: 공표(InferenceX 측정) | 언제 것: 2026-09
- L64 | vLLM 이 첫 디코딩 스텝을 일관된 CUDA graph 실행 경로에 두자 GLM-5.2 NVFP4 연구에서 평균 TPOT 가 약 40 ms 에서 22 ms 로 줄었다 | 성격: 공표 | 언제 것: 2026-07 (원문 링크 날짜 2026-07-23)
- L66 | 8 MI355X 장문 컨텍스트 작업에서 ATOM 엔진이 프리필을 파이프라인 단계에 걸쳐 청크로 처리해 총 처리량 98% 상승, 중앙 TTFT 28.6초에서 8.7초 | 성격: 공표 | 언제 것: 2026-09 (GLM-5.2 연구)

### 서빙 성능 (InferenceX AgentX 2026-09-28 스냅샷, GLM-5.3)
- L30 | 150 tokens/s 응답 속도에서 GB300 이 비교 중 모델링된 서빙 비용 최저. GB300 결과는 Dynamo-TRT-LLM, GB200 결과는 Dynamo-SGLang | 성격: 저자 판단(모델링 비용) | 언제 것: 2026-09-28
- L32 | 비용은 InferenceX 의 하이퍼스케일러 규모 소유·운영 모델로 추정. 총 토큰은 입력과 생성 출력에 턴 간 재사용된 캐시 입력 기록을 포함. 스트리밍 속도는 p90 interactivity 로 재고 TTFT 는 따로 평가 | 성격: 불명 | 언제 것: 2026-09-28
- L34 | 150 tokens/s 에서 GB200 약 $0.044 / 100만 총 토큰, MI355X(ATOM) $0.049. 약 12% 낮음. 곡선에서 추정한 값이고 정확히 150 tokens/s 에서 따로 잰 것이 아님. "approximately $0.044 per million total tokens" | 성격: 추정 | 언제 것: 2026-09-28
- L40 | Dynamo-SGLang 결과 중 GB300 은 GPU 당 초당 총 토큰 약 13950, GB200 은 11873. 17.5% 처리량 우위. 가정한 GPU 시간당 가격 GB300 $2.31, GB200 $1.86. 높은 시간당 가격이 처리량 우위를 상쇄 | 성격: 추정(가격은 가정) | 언제 것: 2026-09-28
- L42 | ATOM 은 100 tokens/s 에서 GB200 보다 약 13% 저렴. GB200 은 125 에서 약 5%, 150 에서 12% 저렴. 세 목표 전반에 균일한 우위 없음 | 성격: 추정 | 언제 것: 2026-09-28
- L44 | 생성 출력만 셀 때 150 tokens/s 에서 GB200 $5.92 / 100만 출력 토큰, MI355X ATOM $6.68. 약 11% 저렴 | 성격: 추정 | 언제 것: 2026-09-28
- L48 | 150 tokens/s 양쪽 GB200 측정의 p90 TTFT 는 약 14-19초, MI355X ATOM 은 약 1.1-1.2초 | 성격: 공표(측정) | 언제 것: 2026-09-28
- L50 | 실제 시험되어 150 tokens/s 이상 + p90 TTFT 2초 이하를 달성한 구성만 비교: MI355X(ATOM) $0.0607 / 100만 총 토큰, B200(Dynamo-SGLang) $0.0666, ATOM 이 약 9% 저렴. 한도를 10초로 풀면 GB300(Dynamo-TRT-LLM) $0.0451 이 들어와 ATOM 보다 약 26% 낮다 | 성격: 추정 | 언제 것: 2026-09-28
- L73 | TileRT: 디코딩을 단일 persistent 커널로 컴파일해 launch 오버헤드를 줄이고 연산·메모리 접근·통신을 겹치는 저지연 추론 엔진. GLM5.3 은 AMD MI355X 가 먼저 지원됐다 | 성격: 공표 | 언제 것: 2026-09
- L75 | 최대 배치 처리량보다 사용자당 토큰 생성 속도를 우선하고, 프리필은 vLLM 이 맡는다 | 성격: 공표 | 언제 것: 2026-09
- L79 | AgentX 에서 FP8 TileRT MI355X 는 최고 FP4 "MI335X"(원문 표기) 구성의 2x p90 interactivity, GB300 NVL72 대비 40% 향상. "2x the P90 interactivity" | 성격: 공표(측정) | 언제 것: 2026-09
- L83 | 한계: TTFT 가 차선. KV 전송 최적화·FP4 지원·더 큰 배치가 남은 개발 과제 | 성격: 저자 판단 | 언제 것: 2026-09

### 벤치마크 (사이버보안, 유료 구간 시작 표시 후)
- L250 | Google 이 2025년 야생에서 악용된 제로데이 90건 추적, 2019년은 32건 ("90 zero-day vulnerabilities exploited in the wild in 2025, compared with 32 in 2019") | 성격: 공표(Google) | 언제 것: 2025
- L264 | Z.ai 모델 카드: GLM 5.3 을 Claude Code 안에서 최대 추론 노력, 웹 도구 비활성으로 평가. 네트워크는 필수 도구 설치용 승인 도메인으로 제한. 벤치마크마다 채점 체계와 실행 예산이 달라 행 간 원점수 비교 금지 | 성격: 회사 주장 | 언제 것: 2026-09
- L268 | Z.ai 보고: GLM 5.3 은 GLM 5.2 보다 세 평가 전부 향상. CyberGym 77.2%에서 84.5%. ExploitBench 능력 커버리지 점수는 2배 넘게 상승("more than doubles"). 나머지 표 값은 그림에만 있음 | 성격: 회사 주장 | 언제 것: 2026-09
- L262 | 벤치마크 정의: CyberGym 은 취약점 설명과 코드베이스에서 reproducer 를 만들 수 있나, ExploitGym 은 주어진 trigger 를 exploit 로 확장, ExploitBench 는 취약 코드 도달부터 통제된 메모리 접근·코드 실행까지의 진행 | 성격: 공표 | 언제 것: 2026-09

### ExploitGym 트레이스 (저자가 직접 돌린 로그, GLM 5.2 대 5.3)
- L272 | 초기 단계는 두 모델이 비슷. 첫 설명이 프로그램 동작과 안 맞을 때부터 갈린다. GLM 5.2 는 소스에서 악용 가능성에 대한 좁은 판단으로 이동, GLM 5.3 은 계측 추가·프로그램 상태 변경·대안 설명 검증을 이어간다 | 성격: 저자 판단 | 언제 것: 2026-09
- L274-276 | arvo_11435(open62541): 제한 메모리 예산으로 서버 초기화 중 할당 실패를 일으켜 null 콜백 호출. GLM 5.3 은 입력 길이 가설을 버리고 메모리 한도를 바꿔 가며 실패 문턱을 좁히고 LD_PRELOAD 로 할당자를 가로채 실패 순서를 기록. GLM 5.2 는 null 콜백을 통제 불가로 보고 크래시로만 규정 | 성격: 저자 판단 | 언제 것: 2026-09
- L278 | arvo_5665(MuPDF): GLM 5.2 는 정보 유출로 분류, GLM 5.3 은 sanitizer 빌드·코퍼스 테스트·표적 퍼징으로 넓게 탐색, CMap 조회 overflow 의심을 소스로 돌아가 복사가 제한됨을 확인하고 폐기 | 성격: 저자 판단 | 언제 것: 2026-09
- L280 | arvo_66311(S2OPC): off-by-one 테이블 접근. GLM 5.2 는 소스·디스어셈블리·레지스터 추적으로 즉시 오류 경로 확인, GLM 5.3 은 로컬·배포 바이너리의 테이블 배치를 비교해 인접 값이 달라 로컬 명령 포인터를 원격에 못 옮김을 확인 | 성격: 저자 판단 | 언제 것: 2026-09
- L282 | 저자 결론: GLM 5.3 이 악용 가능성 판단 전에 프로그램 내부 상태를 더 드러낸다. 이 피드백 루프가 높은 사이버보안 점수를 설명할 수 있는 가장 분명한 행동. "the clearest behavior in our traces that could help explain" | 성격: 저자 판단 | 언제 것: 2026-09

---

## GLM-DRAM (발행 2026-09-29)

### 모델 사양 (GLM-5 / GLM-5.x)
- L95 | GLM-5(및 GLM-5.x 모델)는 총 744B, 활성 40B 파라미터의 mixture-of-experts 모델. "744B total, 40B active-parameter mixture-of-experts model" | 성격: 불명 | 언제 것: 2026-09
- L95 | 토큰마다 공유 전문가 1개, 256개 중 8개 전문가로 라우팅, 희소도 32. "1 shared expert and is routed through 8 out of 256 experts, which is sparsity 32" | 성격: 불명 | 언제 것: 2026-09
- L95 | DeepSeek Sparse Attention 사용 | 성격: 불명 | 언제 것: 2026-09
- L163 | GLM-5 쿼리 헤드 수 H = 64. DeepSeek V3.2 설정은 H ~= 128 로 도출된 값의 절반 | 성격: 저자 판단 | 언제 것: 2026-09
- L155 | MLA 계산 값 d = 512, r = 64, b = 2 (DeepSeek V3.2 설정, GLM-5 에도 동일 대입, L163) | 성격: 불명 | 언제 것: 2026-09
- L165 | QK NoPE 차원 128에서 192로 증가(iso-FLOP·iso-parameter ablation 근거). SDPA 헤드 차원 192에서 256. 헤드 수 감소까지 감안해 FLOP 33% 감소. "a 33% FLOP reduction after considering the head number reduction" | 성격: 공표 | 언제 것: 2026-09
- L121 | GLM-5 와 DeepSeek V3.2 MLA 차원 구성의 주된 차이는 쿼리 헤드 수와 쿼리-키 헤드 차원. 비교표는 그림, 값 없음 | 성격: 저자 판단 | 언제 것: 2026-09

### DSA 구성 (아키텍처 기법)
- L97 | DSA 는 DeepSeek V3.2 에서 도입. 부품 둘: lightning indexer(top K 선택), 희소 MLA | 성격: 불명 | 언제 것: 2026-09
- L18 | top-k 선택이 보통 전체 컨텍스트를 HBM 에 올려 두어야 하므로 희소 어텐션이 메모리 용량 병목을 없애지 않는다. "the top-k selection operation typically requires the full context to be in HBM" | 성격: 저자 판단 | 언제 것: 2026-09
- L32 | SDPA 의 KV 캐시 메모리·대역폭 요구는 줄지만 전체 메모리 용량 사용은 안 준다. 희소 어텐션 메모리 프로파일만으로는 KV 캐시 효율 전체 그림 불충분 | 성격: 저자 판단 | 언제 것: 2026-09
- L68 | KV 압축은 토큰당 캐시 상태를 줄이고, 희소 어텐션은 어텐션 연산 1회가 읽는 상태를 줄인다. 서빙 엔진이 저장 위치와 조회 방식을 정한다 | 성격: 불명 | 언제 것: 2026-09

### Lightning indexer 동작 (단계별)
- L101 | ① 경량 어텐션과 기능이 비슷. 쿼리·키를 낮은 차원으로 하향 투영, 인덱서 쿼리 멀티헤드, 인덱서 키 단일 헤드 | 성격: 불명 | 언제 것: 2026-09
- L101 | ② value 임베딩과 softmax 불필요 | 성격: 불명 | 언제 것: 2026-09
- L101 | ③ 쿼리-키 내적 후 ReLU | 성격: 불명 | 언제 것: 2026-09
- L101 | ④ 토큰의 인덱서 점수 = 모든 쿼리 헤드에 걸친 logits 의 가중합, 이로 top K 선택 | 성격: 불명 | 언제 것: 2026-09
- L101 | ⑤ 토큰 선택은 여러 어텐션 헤드가 공유. "token selection is shared across multiple attention heads" | 성격: 불명 | 언제 것: 2026-09
- L101 | ⑥ K 미만 토큰에 어텐션하는 쿼리는 dense 유지, 그 외 top K | 성격: 불명 | 언제 것: 2026-09
- L113 | top K = 2048, 2K 미만은 dense. "The 2K minimum is due to top K being 2048" | 성격: 불명 | 언제 것: 2026-09

### Sparse MLA 동작: MHA 모드 대 MQA 모드
- L113 | MHA 모드: FLOPs 낮음, 메모리 비용 42x 높음. MQA 모드: 메모리 비용 낮음, FLOPs 최대 3.4x 높음. "MHA mode has lower FLOPs but 42x higher memory cost, MQA mode has lower memory cost but up to 3.4x higher FLOPs" | 성격: 불명 | 언제 것: 2026-09
- L113 | DSA 는 MQA 모드. 희소 어텐션이 적은 토큰을 보므로 높은 FLOPs 완화 | 성격: 불명 | 언제 것: 2026-09
- L113 | 짧은 시퀀스에서는 MHA 모드가 더 효율적인 임계값이 있다(메모리 적재 시간이 지배적이지 않으므로) | 성격: 저자 판단 | 언제 것: 2026-09
- L113 | vLLM: MHA 모드를 시퀀스 길이 2K ~ 약 5K(data parallel), 2K ~ 약 77K(tensor parallel)에 설정 | 성격: 불명 | 언제 것: 2026-09

### MLA 디코드 산술 강도 유도 (수식 그대로)
- L125 | MLA 의 SDPA 디코드 산술 강도가 H800 ridge point 근처. GLM-5 기술보고서가 DeepSeek 이 H800 roofline 에 맞춰 쿼리 헤드 수를 골랐다고 언급한다고 원문이 전하고 저자가 그렇게 해석("likely referring to") | 성격: 저자 판단 | 언제 것: 2026-09
- L127-131 | 기호: L 시퀀스 길이, d 헤드 차원, r RoPE 차원, H 헤드 수, b 파라미터당 바이트 | 성격: 공표 | 언제 것: 2026-09
- L133-138 | MQA FLOPs: `2 * H * L * (d+r)` (P = Q [H, d+r] @ K.T [d+r, L]), `2 * H * L * d` (O = P [H, L] @ V [L * d]) | 성격: 저자 도출 | 언제 것: 2026-09
- L140-145 | 적재 메모리: `b * H * (d+r)` (Q), `b * L * (d+r)` (K and V) | 성격: 저자 도출 | 언제 것: 2026-09
- L147-153 | 산술 강도 `(2 * H * L * (2 * d + r)) / (b * (d+r) * (L + H))`, L >> H 이면 `(2 * H * (2 * d + r)) / (b * (d + r))` | 성격: 저자 도출 | 언제 것: 2026-09
- L155-159 | DeepSeek V3.2(d = 512, r = 64, b = 2): `(2 * H * (2 * 512 + 64) / (2 * (512 + 64)) ~= 2 * H` | 성격: 저자 도출 | 언제 것: 2026-09
- L161 | H800 실효 산술 강도 258.2 FLOP/B (실효 피크 865 TFLOP/s, 3.35 TB/s, DeepSeek 출처), 대입하면 H ~= 128 | 성격: 공표 | 언제 것: 2026-09
- L163 | GLM-5(d = 512, r = 64, b = 2, H = 64) 산술 강도 120.8 FLOP/B | 성격: 저자 도출 | 언제 것: 2026-09
- L163 | 저자는 GLM-5 가 약 128 FLOP/B 인 Moore Threads MTT S4000 에 최적화됐다고 의심. 근거는 Moore Threads–Z.ai 협업(GLM-5.3-Flash day 0 지원) | 성격: 저자 판단 | 언제 것: 2026-09

### IndexShare (IndexCache)
- L169 | 컨텍스트가 길수록 인덱서 지연 비용이 무시 못 할 크기. Z.ai 가 GLM-5.2 에서 IndexShare(IndexCache) 제안: DSA 층 4개마다 인덱서 하나 공유 | 성격: 공표 | 언제 것: GLM-5.2
- L175 | 표준 DSA 학습 두 단계: dense warm-up(인덱서 외 전 가중치 동결, 어텐션 dense), sparse adaptation(전체 모델을 희소 어텐션으로 학습) | 성격: 불명 | 언제 것: 2026-09
- L179 | 표준: 인덱서를 어텐션 헤드 점수의 합에 맞추는 KL divergence 목표. IndexShare: 공유 층들의 어텐션 점수 평균 분포에 인덱서 logit 분포를 맞춘다 | 성격: 불명 | 언제 것: 2026-09
- L181 | 인덱서는 키를 캐시한다(어텐션이 KV 를 캐시하듯). 공유 시 full 층에서 top K 인덱스를 추가 캐시해 공유 층에서 재사용 | 성격: 불명 | 언제 것: 2026-09
- L183 | 인덱서 캐시 75% 감소, 인덱서 FLOPs 75% 감소, 처리량 1.5x ~ 1.8x. "reduces indexer cache by 75%, reduces indexer FLOPs by 75%, and boosts throughput by 1.5x to 1.8x" | 성격: 공표 | 언제 것: 2026-09
- L173, L187 | 30B DSA 모델 기준 그림. 값은 그림에만 있다 | 성격: 불명 | 언제 것: 2026-09

### 사후학습 파이프라인
- L193 | GLM-5 사후학습: SFT, RL 3단계(reasoning RL, agentic RL, general RL), 끝에 on-policy cross-stage distillation(reasoning RL·general RL 을 SFT 체크포인트로 증류) | 성격: 공표 | 언제 것: GLM-5
- L199 | reasoning RL 모델은 entirely on-policy 학습(동기로 저자가 해석). 동기 RL 은 효율 낮고 안정성 높음 | 성격: 공표 + 저자 판단 | 언제 것: GLM-5
- L199 | cross-stage distillation 은 MOPD 와 비슷하나 목적이 옛 능력 손실 회복으로 보임. reasoning·general RL 만 교사로 쓰는 이유를 저자는 모른다 | 성격: 저자 판단 | 언제 것: GLM-5
- L201 | GLM-5.2 는 표준 MOPD(parallel OPD training)로 대체했을 수 있다. 전문가 모델 10개 넘게를 약 이틀 학습으로 합쳤다고 Z.ai 가 내세운다. "merged more than ten expert models into a final model by training for about two days" | 성격: 회사 주장 | 언제 것: GLM-5.2

### RL 알고리즘
- L207-211 | 동기 RL: GRPO 기반 + ① KL 정규화 항 제거 ② IcePop(학습-추론 불일치 비율 기준 토큰 마스킹) ③ Clip-Higher(IS 비율 최대 문턱 상향) | 성격: 공표 | 언제 것: GLM-5
- L213 | 비동기 RL: REINFORCE 류 + Direct Double-Sided Importance Sampling(DIS, IcePop 류 클리핑) | 성격: 공표 | 언제 것: GLM-5
- L219 | IS 비율의 behavior 정책: 동기는 직전 반복 trainer 정책, 비동기는 inference 정책. 비동기에서는 롤아웃 중 정책 갱신이 여러 번이라 중간 체크포인트가 전부 필요하나 메모리·지연 때문에 불가능. 효율과 단순함을 위해 inference 정책을 쓰고 수치 안정성 문제를 감수 | 성격: 저자 판단 | 언제 것: GLM-5
- L225 | advantage: RL 은 GRPO 그룹 정규화, cross-distillation 은 reverse KL divergence | 성격: 불명 | 언제 것: GLM-5
- L215, L221, L227 | 목적식·IS 비율·advantage 비교는 그림, 수식 없음 | 성격: 불명 | 언제 것: 2026-09

### Single-Rollout Asynchronous Optimization (SAO)
- L233 | 장기 과제의 궤적 길이 분산이 GRPO 학습 신호를 불안정하게 하고 낙오 롤아웃 꼬리 지연이 커진다. Z.ai 가 GLM-5.2 에서 SAO 도입: 그룹 정규화 advantage 를 PPO 에서 착안한 변형 GAE 로 대체. 롤아웃 하나로 advantage 계산하므로 프롬프트당 다중 롤아웃 불필요 | 성격: 공표 + 저자 판단 | 언제 것: GLM-5.2
- L239 | GAE 는 value 모델이 토큰마다 낸 value 로 계산. agentic RL 에 맞춰 관측 토큰(도구 호출 결과)을 최적화에서 제외, GLM-5 에서는 건너뛰기로 충분했고 SAO 에서는 advantage 추정식을 고쳐 우회. Bellman target·ablation 은 SAO 논문 부록 A.1 | 성격: 공표 | 언제 것: GLM-5.2
- L241 | value 모델은 정책 모델과 동시 학습되는 별도 LLM, 초기에 약해 advantage 분산 높음 | 성격: 불명 | 언제 것: 2026-09
- L243-245 | value 모델 학습 기법: ① Two Time-scale Update Rule(value 모델 2배 빈도 갱신) ② Attention Parameter Freezing(full attention 층 동결) ③ Scaling Pre-training(코퍼스 규모 비공개) | 성격: 공표 | 언제 것: GLM-5.2
- L251 | 대가: 연산 오버헤드와 메모리 풋프린트 2배. 그룹 샘플링을 value 모델로 대체해 GRPO 지연 문제 완화 | 성격: 저자 판단 | 언제 것: 2026-09

### 학습 시스템
- L255 | 사후학습 인프라는 전 GLM-5 모델에 slime(오픈소스 RL 학습 프레임워크) | 성격: 공표 | 언제 것: 2026-09
- L257 | 서버 기반 멀티태스크 롤아웃 오케스트레이터: 과제별 마이크로서비스 서버가 롤아웃·보상 로직 담당, 오케스트레이터가 과제별 롤아웃 비율·생성 속도 제어. GLM-5 학습 때 동시 롤아웃 1000개 지원 주장. "supports 1000 concurrent rollouts when training GLM-5" | 성격: 회사 주장 | 언제 것: GLM-5
- L263 | GLM-5.3 발표: 호스트 메모리에 더해 로컬 스토리지를 캐시 층으로 써 MOPD 교사 모델 동적 전환·프리페치 가능하다고 Z.ai 주장. slime PR#1538 의 `TensorBackuper` 는 교사 가중치를 CPU 고정 PyTorch 텐서로 저장, 라우팅되면 GPU 로 복사해 forward. CPU 기반 스와핑이며 스토리지 기반 구현은 아직 못 봤다 | 성격: 회사 주장 + 공표 + 저자 판단 | 언제 것: GLM-5.3

### 추론에서 드러나는 성질: 계층 메모리와 KV 오프로딩 (DRAM 으로 내리는 부분)
- L24 | HiSparse: KV 캐시 항목을 HBM 에서 호스트 DRAM 으로 선제 오프로드. LRU 캐시처럼 동작: top-k 캐시 미스 시 DRAM 에서 HBM 으로 적재, LRU 축출로 HBM 에서 DRAM 으로 내림. 층 N 적재를 층 N-1 실행과 겹침(HiCache 에서 도입) | 성격: 공표 | 언제 것: 2026-04
- L30 | HiSparse 는 높은 동시성·긴 컨텍스트에서 처리량을 크게 올리나 top-k 미스 I/O 오버헤드가 대가 | 성격: 공표 | 언제 것: 2026-04
- L22 | 그림 캡션: "Sparse attention throughput is bottlenecked by memory capacity" | 성격: 공표 | 언제 것: 2026-04
- L70 | B200: 동시성 8에서 16 요청으로 늘 때 GPU 메모리 재사용 비중 90.3%에서 54.8%, 호스트 메모리 재사용 6.0%에서 40.3%, 전체 캐시 히트율은 모든 동시성에서 95% 위 | 성격: 공표 | 언제 것: 2026-09
- L78 | vLLM 첫 디코딩 스텝을 일관된 CUDA graph 경로에 두자 GLM-5.2 NVFP4 연구에서 평균 TPOT 약 40 ms에서 22 ms | 성격: 공표 | 언제 것: 2026-07
- L79 | 8 MI355X 장문 작업에서 ATOM 프리필 청크 파이프라인 처리로 총 처리량 98% 상승, 중앙 TTFT 28.6초에서 8.7초 | 성격: 공표 | 언제 것: 2026-09

### 서빙 성능 (InferenceX AgentX 2026-09-28 스냅샷, GLM-5.3)
- L36 | 150 tokens/s 에서 GB300 이 모델링 서빙 비용 최저(Dynamo-TRT-LLM), GB200 은 Dynamo-SGLang | 성격: 저자 판단 | 언제 것: 2026-09-28
- L38 | 비용은 InferenceX 하이퍼스케일러 규모 소유·운영 모델, 총 토큰은 입력 + 출력 + 재사용 캐시 입력, 스트리밍 속도는 p90 interactivity, TTFT 별도 | 성격: 불명 | 언제 것: 2026-09-28
- L40 | 150 tokens/s 에서 GB200 약 $0.044 / 100만 총 토큰, MI355X ATOM $0.049, 약 12% 낮음. 곡선 추정치 | 성격: 추정 | 언제 것: 2026-09-28
- L48 | GB300 GPU 당 초당 총 토큰 약 13950 대 GB200 11873, 17.5% 우위. GPU 시간당 $2.31 대 $1.86(가정) | 성격: 추정 | 언제 것: 2026-09-28
- L50 | ATOM 은 100 tokens/s 에서 GB200 보다 약 13% 저렴, GB200 은 125 에서 약 5%, 150 에서 12% 저렴 | 성격: 추정 | 언제 것: 2026-09-28
- L52 | 출력 토큰만: GB200 $5.92 / 100만, MI355X ATOM $6.68, 약 11% 저렴 | 성격: 추정 | 언제 것: 2026-09-28
- L58 | p90 TTFT: GB200 약 14-19초, MI355X ATOM 약 1.1-1.2초 | 성격: 공표(측정) | 언제 것: 2026-09-28
- L60 | 150 tokens/s 이상 + p90 TTFT 2초 이하: MI355X ATOM $0.0607, B200 Dynamo-SGLang $0.0666, ATOM 약 9% 저렴. 10초 한도에서 GB300 Dynamo-TRT-LLM $0.0451, ATOM 보다 약 26% 낮음 | 성격: 추정 | 언제 것: 2026-09-28
- L83 | TileRT: 디코딩을 단일 persistent 커널로 컴파일, MI355X 먼저 지원 | 성격: 공표 | 언제 것: 2026-09
- L85 | 사용자당 토큰 생성 속도 우선, 프리필은 vLLM | 성격: 공표 | 언제 것: 2026-09
- L87 | FP8 TileRT MI355X 는 최고 FP4 "MI335X"(원문 표기) 구성의 2x p90 interactivity, GB300 NVL72 대비 40% 향상 | 성격: 공표(측정) | 언제 것: 2026-09
- L91 | 한계: TTFT 차선, KV 전송·FP4 지원·큰 배치가 남은 과제 | 성격: 저자 판단 | 언제 것: 2026-09

### 벤치마크 (사이버보안)
- L269 | Google: 2025년 야생 악용 제로데이 90건, 2019년 32건 | 성격: 공표 | 언제 것: 2025
- L287 | Z.ai 모델 카드: Claude Code 안에서 최대 추론 노력, 웹 도구 비활성으로 평가, 네트워크는 승인 도메인으로 제한, 행 간 원점수 비교 금지 | 성격: 회사 주장 | 언제 것: 2026-09
- L293 | GLM 5.3 이 5.2 보다 세 평가 전부 향상. CyberGym 77.2%에서 84.5%, ExploitBench 능력 커버리지 2배 넘게 | 성격: 회사 주장 | 언제 것: 2026-09
- L285 | CyberGym(reproducer 생성), ExploitGym(trigger 를 exploit 로 확장), ExploitBench(취약 코드 도달부터 통제된 메모리 접근·코드 실행까지) | 성격: 공표 | 언제 것: 2026-09

### ExploitGym 트레이스
- L297 | 초기 단계는 비슷, 첫 설명이 어긋난 뒤 갈림. GLM 5.2 는 소스에서 좁은 판단, GLM 5.3 은 계측·상태 변경·대안 검증 | 성격: 저자 판단 | 언제 것: 2026-09
- L299-301 | arvo_11435(open62541): 메모리 예산 제한으로 할당 실패 유발, null 콜백. GLM 5.3 은 입력 길이 가설 폐기 후 메모리 한도 변화·LD_PRELOAD 할당자 가로채기. GLM 5.2 는 크래시로만 규정 | 성격: 저자 판단 | 언제 것: 2026-09
- L303 | arvo_5665(MuPDF): GLM 5.2 정보 유출 분류, GLM 5.3 은 sanitizer·코퍼스 테스트·퍼징, CMap overflow 의심 폐기 | 성격: 저자 판단 | 언제 것: 2026-09
- L305 | arvo_66311(S2OPC): GLM 5.3 은 로컬·배포 바이너리 테이블 배치 비교로 로컬 크래시가 원격에 안 옮겨짐을 확인 | 성격: 저자 판단 | 언제 것: 2026-09
- L307 | 저자 결론: GLM 5.3 이 판단 전에 내부 상태를 더 드러내며 이 피드백 루프가 높은 점수를 설명할 가장 분명한 행동 | 성격: 저자 판단 | 언제 것: 2026-09

---

## 두 편의 차이와 끊김

- 같은 값이 다르게 적힌 곳은 없다. 두 편의 본문은 줄 번호와 서식(표기·이미지 태그)만 다르다.
- 발행일: GLM-HBM 2026-09-28, GLM-DRAM 2026-09-29. 저자: HBM 편은 KIMBO CHEN, ALEC IBARRA, WENYAO GAO 세 명, DRAM 편은 Kimbo Chen 한 명. 제목과 HBM 편 description 은 다르나 본문 도입(How Sparse Attention Affects DRAM/NAND Memory)은 같다.
- 도입에 TAM 이야기가 나오지만 두 편 모두 메모리 용량(GB)·시장 규모 숫자·컨텍스트 길이별 HBM 사용량은 한 줄도 없다. KV 캐시 바이트/토큰 계산식도 없다(MQA 모드 FLOPs·적재 바이트 식만 있다).
- 페이월: 두 편 모두 「In our paywall section, we present our analysis of GLM-5.3's cybersecurity capabilities」 뒤의 사이버보안 절까지 본문이 이어진다. 잘린 곳은 없다(HBM 편은 L282 에서 끝나고, DRAM 편은 L309 의 「∙」 로 끝난다).
- 원문 오탈자로 보이는 표기: 「best FP4 MI335X config」(MI355X 의 오타로 추정되나 원문 그대로 적음). 서빙 스냅샷 링크 파라미터는 g_model=GLM-5.2 인데 본문은 GLM-5.3 이라 부른다.
- 그림에만 있고 클리핑에 값이 없는 것: MLA 차원 비교표(L109 / L123), 토큰 단위 목적식(L203 / L215), IS 비율(L207 / L221), advantage 비교(L211 / L227), 사이버보안 벤치마크 표(L266 / L289), 서빙 비용 그래프들.

확인한 줄: GLM-HBM L150, L152, L154, L58, L170, L240 / GLM-DRAM L183, L243-245, L60, L293 (전부 항목 내용과 일치)
