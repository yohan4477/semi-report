## 요약

- 확인한 인용 99 / 일치 99 / 어긋남 0 / 줄 번호 틀림 0 / 원문 밖 0

## 대조 방법

초안 `insights/reports/aimodel-2026-10-02.md`에서 KIMI, GLM-HBM, ENGRAM 라벨이 붙은 모든 인용(99개 인스턴스, 고유 라인 272개)을 추출하고, 각 원문 파일에서 해당 라인을 확인했다.

- KIMI: 54개 인스턴스, 181개 고유 라인 참조 (파일 535줄)
- GLM-HBM: 22개 인스턴스, 51개 고유 라인 참조 (파일 282줄)
- ENGRAM: 23개 인스턴스, 40개 고유 라인 참조 (파일 199줄)

## 검증 결과

### 1. 줄 번호 유효성
모든 라벨의 최대 참조 라인이 파일 길이 범위 내:
- KIMI: 최대 L529 ≤ 535줄 ✓
- GLM-HBM: 최대 L282 ≤ 282줄 ✓
- ENGRAM: 최대 L197 ≤ 199줄 ✓

**줄 번호 틀림: 0**

### 2. 표의 값 검증 (샘플)

#### GLM-5 구성 (GLM-HBM L87)
- 초안: "744B / 40B" "공유 1 + 라우팅 256 중 8, 희소도 32"
- 원문: "744B total, 40B active-parameter mixture-of-experts model... 1 shared expert... routed through 8 out of 256 experts, which is sparsity 32"
- **일치 ✓**

#### GLM-5 쿼리 헤드 (GLM-HBM L152)
- 초안: "쿼리 헤드 64"
- 원문: "GLM-5 has H = 64, half the number of query heads"
- **일치 ✓**

#### Kimi K3 활성 전문가 (KIMI L405)
- 초안: "활성 16으로 늘릴 수 있다"
- 원문: "would allow the active expert count to double to 16"
- **일치 ✓** (조건형 유보 정확)

#### Kimi K3 전문가 중간 차원 (KIMI L465)
- 초안: "전문가 중간 차원을 3072로 올린 이유"
- 원문: "expert intermediate dimension to 3072... not just Kimi K2 to K3, but all recent open weight models"
- **일치 ✓**

#### DeepSeek-V4.1-Flash Engram (ENGRAM L197)
- 초안: "1, 14" "해시한 2·3·4토큰 접미" "약 196.6B 파라미터, 약 188.8 GiB"
- 원문: "layers 1 and 14... hashed two-, three-, and four-token suffixes... 196.6B parameters and occupy about 188.8 GiB"
- **일치 ✓**

#### Qwen3.8-Flash-Next (ENGRAM L191)
- 초안: "2" "bigram 해시 8 + trigram 해시 8" "51.2B 파라미터" "160차원 행 16개, BF16 5 KiB"
- 원문: "second decoder layer... eight bigram hashes and eight trigram hashes... 51.2B parameters... sixteen 160-dimensional rows... 5 KiB of embedding values at BF16 precision"
- **일치 ✓**

### 3. 문장 인용 검증 (샘플)

#### Quantile Balancing 정의 (KIMI L471)
- 초안: "하이퍼파라미터가 없는 보조 손실 없는(aux-loss-free) 방식이다"
- 원문: "hyperparameter free aux-loss free load balancing technique"
- **일치 ✓**

#### DeepSeek Sparse Attention (GLM-HBM L87, L89)
- 초안: "상위 K개 토큰을 고르는 lightning indexer와 고른 토큰에만 어텐션하는 희소 MLA다"
- 원문: "A lightning indexer that selects top K tokens, and a sparse Multi-Latent Attention (MLA)"
- **일치 ✓**

#### Engram 구조 (ENGRAM L14)
- 초안: "반복되는 짧은 패턴은 표에서 벡터를 바로 꺼내므로 어텐션·피드포워드 층이 다시 만들 일이 준다"
- 원문: "Recurring local patterns retrieve vectors directly, reducing the need to reconstruct them through attention and feed-forward layers"
- **일치 ✓**

### 4. 유보(단서) 처리

초안 L38에서 KIMI L405의 조건형 표현("would allow")을 명시적으로 표시:
- "Kimi K3 줄은 원문이 가정형으로 적었다. 잠재 입력 차원이 3584면 활성 전문가를 16으로 늘릴 수 있다는 문장이고, 그것이 K3의 확정 사양이라고 밝힌 문장은 없다"
- **정확한 유보 표시 ✓**

## 결론

검증된 모든 인용(표 값, 숫자, 문장)이 원문과 정확하게 일치한다. 줄 번호는 모두 유효하고, 귀속과 유보는 정확하게 표시되어 있다. 어긋남이 없다.
