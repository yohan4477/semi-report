# NVIDIA 밸류체인 분석 및 고객·공급사 비중 추정

## 1. Executive Summary

NVIDIA의 밸류체인은 단순한 반도체 공급사 → NVIDIA → Hyperscaler 구조로 보기 어렵다. NVIDIA는 fabless 기업으로서 파운드리·메모리·첨단 패키징·시스템 제조업체에 생산을 의존하는 동시에, downstream에서는 hyperscaler와 AI model maker에 직접 제품을 판매하기도 하고 Dell, Foxconn, Quanta/QCT 등 OEM·ODM·system integrator를 경유해 최종 고객에게 제품을 공급하기도 한다.

따라서 NVIDIA 밸류체인 분석에서는 회계적 거래 관계와 실제 경제적 수요 관계를 분리하는 것이 핵심이다.

회계 기준으로는 다음 구조를 사용한다.

```
Supplier → NVIDIA → Direct Customer → Indirect Customer
```

반면 실제 제품 및 최종수요 흐름은 다음과 같이 나타날 수 있다.

```
TSMC / Memory → NVIDIA → Dell·Foxconn·QCT → Hyperscaler·AI Cloud → AI Model Maker
```

두 구조를 혼합할 경우 예를 들어 Microsoft의 GPU 수요가 NVIDIA→Microsoft direct revenue로 잡힌 것인지, NVIDIA→Dell/Foxconn 매출 후 Microsoft가 최종 고객으로 존재하는 것인지 구분할 수 없게 된다.

NVIDIA의 FY27 Q2 10-Q에 따르면 FY27 상반기 매출은 $177.837B이며, 익명의 direct customer 세 곳이 각각 전체 매출의 **16%, 15%, 13%**를 차지했다. 달러 기준으로 약 $28.45B, $26.68B, $23.12B에 해당한다. NVIDIA는 해당 고객의 실명은 공개하지 않았다.

본 분석은 이 실명을 임의로 단정하지 않고, 다음 다섯 단계로 후보를 좁혔다.

① NVIDIA 공시 concentration 복원
② Q1·Q2·H1 간 수학적 continuity 분석
③ 고객 본사 지역별 매출을 이용한 제약조건 적용
④ 각 후보의 AI infrastructure 구매능력과 NVIDIA content 역산
⑤ 실제 procurement route를 통한 direct/indirect 여부 검증

분석 결과, FY27 H1 Top 3 direct customers를 Foxconn·Quanta·Wistron과 같은 대만 ODM 3개사로 설명하는 가설은 geography constraint와 충돌한다. 반면 미국 본사 hyperscaler, AI 기업 또는 대형 OEM이 Top 3 상당수를 구성했을 가능성이 높다.

현 단계에서 Microsoft, Meta, Dell 등이 우선 검증 후보지만, Microsoft=16%, Meta=15%, Dell=13%와 같은 실명 매칭은 공개 자료만으로 확정할 수 없다. 따라서 최종 데이터베이스에는 공시된 anonymous customer와 실명 후보를 별도의 필드로 저장하는 것이 적절하다.

---

## 2. NVIDIA 밸류체인의 기본 구조

### 2.1 Upstream

NVIDIA의 주요 upstream은 크게 다음으로 나눌 수 있다.

```
Foundry → Memory → Advanced Packaging → Substrate/Components → System Manufacturing
```

대표적인 구조는 다음과 같다.

```
Foundry
  TSMC
    │
    ▼
GPU / CPU Die
    │
    ├──────────────┐
    │              │
    ▼              ▼
HBM / Memory    Advanced Packaging
SK hynix        TSMC / packaging ecosystem
Micron
Samsung
    │              │
    └──────┬───────┘
           ▼
         NVIDIA
           │
           ▼
System Manufacturing
Dell / Foxconn / Wistron / QCT / etc.
```

TSMC, Foxconn, Wistron, Dell, Micron 등은 NVIDIA가 공식적으로 manufacturing partner로 명시하고 있는 기업들이다. NVIDIA는 TSMC가 Blackwell 칩을 생산하고 있으며 Foxconn과 Wistron 등이 AI server 및 AI supercomputer 생산에 참여하고 있다고 밝히고 있다.

그러나 supplier 관계가 확인된다는 것과 NVIDIA 구매액 중 해당 supplier가 몇 %를 차지한다는 것은 전혀 다른 문제다.

NVIDIA는 FY27 Q2 현재 향후 supply and capacity commitment를 $279B로 공시했으며, 이는 주로 data center infrastructure systems 생산을 위한 memory 및 manufacturing facilities 관련 commitments라고 설명한다.

다만 NVIDIA는 이 $279B를 TSMC, SK hynix, Micron 등 supplier별로 분해하지 않는다.

따라서 upstream supplier share는 반드시 추정 모델을 사용해야 한다.

---

## 3. Upstream 공급사 비중 추정 방법

### 3.1 기본 원리

NVIDIA supplier별 exposure는 다음 식으로 추정한다.

```
Supplier Spend ≈ NVIDIA Unit Volume × Component Content per Unit × Supplier Allocation
```

이를 매출 기반으로 단순화하면,

```
Supplier Exposure ≈ Relevant NVIDIA Revenue × Component BOM Ratio × Supplier Share
```

이다.

예를 들어 HBM 공급사의 NVIDIA exposure를 추정할 경우:

```
HBM Supplier Spend ≈ Accelerator Shipments × HBM Capacity per Accelerator × HBM $/GB × Supplier Allocation
```

와 같이 계산한다.

여기서 네 가지 변수를 분리해야 한다.

* NVIDIA accelerator 출하량
* 제품별 HBM 탑재량
* 당시 HBM 가격
* SK hynix/Micron/Samsung 간 allocation

이 중 NVIDIA 제품 사양은 상대적으로 확인 가능하지만 HBM ASP와 supplier allocation은 대부분 추정값이므로 결과는 point estimate보다 range로 표시하는 것이 적절하다.

### 3.2 Supply commitment를 sanity check로 사용

FY27 Q2 NVIDIA의 supply and capacity commitments는:

```
FY27 remainder      $92B
FY28                $87B
FY29                $88B
FY30                 $6B
FY31                 $5B
FY32+                $1B
-------------------------
Total               $279B
```

이다.

이 값은 supplier share를 직접 알려주는 데이터가 아니다.

대신 bottom-up으로 계산한 supplier spending의 총합이 NVIDIA의 공개된 commitments와 지나치게 동떨어지지 않는지 확인하는 sanity check로 사용한다.

따라서 다음과 같은 계산은 허용된다.

```
TSMC 추정 + HBM 추정 + Packaging 추정 + 기타 공급 추정 ≈ 공개 commitment와 방향성 비교
```

반면 다음과 같이 직접 나누는 것은 근거가 없다.

```
$279B × 40% = TSMC
```

공개 자료상 $279B의 supplier별 allocation은 알려져 있지 않기 때문이다.

---

## 4. NVIDIA Downstream: Direct와 Indirect를 먼저 분리

NVIDIA는 FY27 Q2 10-Q에서 고객을 명확하게 두 종류로 정의한다.

Direct customers: NVIDIA에서 직접 제품을 구매하는 고객으로 AIB, distributor, ODM, OEM, CSP, AI model maker, system integrator 등이 포함된다.

Indirect customers: NVIDIA의 direct customer를 통해 제품을 구매하는 CSP, AI Cloud, AI model maker, enterprise, public sector 등이 포함된다. NVIDIA는 indirect customer revenue 자체도 purchase order information, product specification, internal sales data 등 여러 자료를 이용하여 추정한다고 밝힌다.

따라서 실제 제품 흐름은 여러 형태가 가능하다.

Case A: Hyperscaler direct procurement

```
NVIDIA
   │
   ▼
Microsoft
   │
   ▼
Microsoft Data Center
```

Case B: OEM 경유

```
NVIDIA
   │
   ▼
Dell
   │
   ▼
AI Cloud / Enterprise
```

Case C: ODM 제조 경유

```
NVIDIA
   │
   ▼
Foxconn / QCT
   │
   ▼
Hyperscaler
```

중요한 것은 NVIDIA가 일부 direct customer가 자체 인력뿐 아니라 third-party system integrator를 활용하여 build를 완료할 수도 있다고 명시한다는 점이다. 따라서 Foxconn이 실제 서버를 조립했다는 사실만으로 Foxconn이 NVIDIA의 회계상 direct customer라고 결론지을 수 없다.

---

## 5. Direct Customer Concentration: 공시 기반 출발점

FY27 Q1 NVIDIA 매출은 $81.615B이었다.

NVIDIA는 Q1에 direct customer 세 곳이 전체 매출의 각각:

```
21%
17%
16%
```

를 차지했다고 공시했다.

이를 금액으로 환산하면 대략:

```
21% ≈ $17.14B
17% ≈ $13.87B
16% ≈ $13.06B
```

이다.

FY27 Q2 매출은 $96.221B이며, Q2에는 **한 direct customer만 16%**를 차지했다. 나머지 고객은 개별적으로 10% threshold를 넘지 않았다.

즉 Q2 최대 고객의 매출 기여는:

```
$96.221B × 16% ≈ $15.40B
```

이다.

FY27 H1에서는 세 고객이:

```
16%
15%
13%
```

를 차지했다.

총 H1 매출 $177.837B에 적용하면:

```
16% ≈ $28.45B
15% ≈ $26.68B
13% ≈ $23.12B
```

이다.

---

## 6. 추론 단계 1: Q1 → Q2 → H1 Continuity 분석

여기서 단순히 H1 16/15/13을 보고 실명을 추정하는 것보다 강한 방법은 Q1과 H1을 동시에 만족하는 고객 trajectory를 계산하는 것이다.

### 6.1 H1 16% 고객

Q1의 16% 고객이 H1의 16% 고객과 동일하다고 가정하면:

```
H1 16%      ≈ $28.45B
Q1 16%      ≈ $13.06B
----------------------
Implied Q2  ≈ $15.39B
```

Q2 매출 대비:

```
$15.39B / $96.221B ≈ 16.0%
```

이다.

실제 NVIDIA 공시는 Q2의 한 고객이 16%였다고 한다.

따라서:

```
Q1 16% 고객 = Q2 16% 고객 = H1 16% 고객
```

이라는 가설은 숫자상 매우 강하게 맞는다.

다만 공시 비율이 정수 단위로 반올림되기 때문에 이를 수학적 확정이라고 볼 수는 없다.

### 6.2 H1 15% 고객

Q1 21% 고객이 H1 15% 고객이라고 가정한다.

```
H1 15%      ≈ $26.68B
Q1 21%      ≈ $17.14B
----------------------
Implied Q2  ≈ $9.54B
```

Q2 비중:

```
$9.54B / $96.221B ≈ 9.9%
```

이다.

즉 Q2에는 10% threshold 아래로 내려간다.

NVIDIA가 Q2에 16% 고객 외에는 10% 이상 고객을 공개하지 않은 것과 정확하게 일치한다.

### 6.3 H1 13% 고객

Q1 17% 고객을 H1 13% 고객으로 가정하면:

```
H1 13%      ≈ $23.12B
Q1 17%      ≈ $13.87B
----------------------
Implied Q2  ≈ $9.25B
```

Q2 비중은 약:

```
9.6%
```

이다.

역시 10% 아래다.

따라서 가장 자연스러운 anonymous-customer continuity는:

```
                     Q1       Q2        H1
Customer A           16%  →   16%   →   16%
Customer B           21%  →  ~9.9%  →   15%
Customer C           17%  →  ~9.6%  →   13%
```

이다.

이 결과는 실명을 알려주지는 않지만 후보 기업을 검증할 때 매우 중요한 time-series fingerprint가 된다.

---

## 7. 추론 단계 2: Geography Constraint

NVIDIA는 customer headquarters 기준 geography를 공개한다.

FY27 Q1은:

```
United States     $63.769B
Taiwan             $12.006B
China               $4.550B
Other               $1.290B
Total              $81.615B
```

이다. 즉 Q1 NVIDIA 매출의 약 78%가 미국 본사 고객에서 발생했다.

FY27 H1에서도 해외 본사 고객 비중은 30%였기 때문에 약 70%가 미국 본사 고객이다.

이 정보는 customer identity를 추정하는 강한 제약조건이다.

예를 들어 H1의 16%와 15% 고객을 각각 Foxconn과 Quanta라고 가정하면:

```
16% + 15% = 31%
```

가 된다.

두 회사 모두 대만 본사 기업이므로 두 고객만으로 전체 non-US revenue 30%와 거의 같거나 초과하게 된다. 여기에 다른 대만·중국·해외 고객도 존재해야 하므로 16%와 15% 고객이 모두 대만 ODM일 가능성은 극히 낮다.

따라서 초기의:

```
Foxconn + Quanta + Wistron = Top 3
```

가설은 배제하는 것이 타당하다.

반대로 Top 3 중 상당수가 Microsoft, Meta, Dell과 같은 미국계 기업일 경우 NVIDIA의 geography 공시와 자연스럽게 부합한다.

---

## 8. 추론 단계 3: 후보별 구매능력 Sanity Check

실명 후보를 평가할 때 단순히 "NVIDIA GPU를 많이 쓴다"는 사실로는 부족하다.

필요한 질문은:

```
이 회사가 한 반기 동안 NVIDIA에 $23B~$29B 수준을 지급할 경제적 규모가 존재하는가?
```

이다.

이를 검증하기 위해 각 고객의 capex 또는 AI server revenue를 NVIDIA 익명 customer value와 비교한다.

---

## 9. Microsoft 분석

Microsoft의 calendar 2026 Q1에 대응하는 FY26 Q3 capex는 $31.9B였으며, 약 2/3가 GPU와 CPU 중심의 short-lived assets였다. 다음 분기인 FY26 Q4 capex는 $41B이며 역시 약 2/3가 CPU/GPU 중심 short-lived assets였다.

두 분기를 합치면:

```
Total Capex
≈ $31.9B + $41.0B
≈ $72.9B

Short-lived asset portion
≈ $72.9B × 2/3
≈ $48.6B
```

이다.

NVIDIA H1 anonymous customers와 비교하면:

```
$28.45B / $48.6B ≈ 59%
$26.68B / $48.6B ≈ 55%
$23.12B / $48.6B ≈ 48%
```

이다.

즉 Microsoft의 GPU/CPU 및 기타 short-lived asset 투자 중 대략 절반 정도가 NVIDIA 관련 구매로 연결된다면 Top 3 규모를 설명할 수 있다.

다만 Microsoft의 short-lived assets에는 NVIDIA GPU 외에도 CPU, networking replacement, AMD accelerator 및 기타 장비가 포함될 수 있으므로 이 계산은 capacity test이지 구매액 확정 추정은 아니다.

평가:

```
Top-3 candidate probability: High
```

특히 규모 측면에서는 16% 고객을 설명할 수 있는 충분한 구매능력을 갖고 있다.

---

## 10. Meta 분석

Meta는 2026 Q2 capex를 $31.08B로 공개했고, 2026년 전체 capex guidance를 $130B~$145B로 제시했다. Meta는 인프라 투자의 확대가 AI와 핵심 사업 지원을 위한 것이라고 설명하고 있다.

Meta 역시 NVIDIA Top-3 customer 규모를 경제적으로 감당할 수 있는 기업이다.

하지만 Meta capex에는:

```
GPU
CPU
Networking
Storage
Data center construction
Power infrastructure
Other equipment
```

가 함께 들어간다.

따라서:

```
Meta Capex × 임의 NVIDIA 비중 = NVIDIA 매출
```

이라는 방식으로 실명을 확정하는 것은 위험하다.

평가:

```
Top-3 candidate probability: High
```

단, 정확히 16%, 15%, 13% 중 어디에 해당하는지는 공개자료만으로 판단하기 어렵다.

---

## 11. Dell 분석

Dell은 hyperscaler와 달리 별도의 검증 방식이 가능하다.

Dell FY27 Q1 AI server revenue는 $16.1B, Q2는 $16.4B, H1 누적 $32.533B다.

NVIDIA anonymous customer value와 비교하면 Dell AI server revenue 중 NVIDIA content가 다음 수준이어야 한다.

```
H1 16% customer:
$28.45B / $32.53B ≈ 87.5%

H1 15% customer:
$26.68B / $32.53B ≈ 82.0%

H1 13% customer:
$23.12B / $32.53B ≈ 71.1%
```

AI server에는 GPU 외에도 CPU, DRAM, SSD, networking, power/cooling, chassis 및 Dell margin 등이 포함되므로 87.5%는 상당히 높은 가정이다.

반면 약 71% 수준은 상대적으로 더 plausible하다.

따라서 규모만 비교할 경우 Dell은 13% customer와 가장 잘 맞는다.

그러나 time-series 측면에서는 문제가 있다.

Dell AI server revenue는:

```
Q1 $16.1B → Q2 $16.4B
```

로 거의 변하지 않았다.

반면 NVIDIA anonymous customer trajectory 중 13% H1 고객으로 추정되는 고객은:

```
Q1 약 17% → Q2 약 9.6%
```

와 같은 매출 감소 패턴을 가져야 한다.

따라서 Dell을 H1 13% customer로 바로 매칭하는 것은 규모 fit은 좋지만 quarter-to-quarter trajectory fit은 약하다.

평가:

```
Top-3 probability: Medium to High
Specific 13% identity confidence: Medium
```

---

## 12. 후보 추정 시 반드시 피해야 할 오류

### 오류 1. Capex = NVIDIA Purchase로 보는 것

Microsoft $73B capex를 그대로 NVIDIA향 구매액으로 보면 안 된다.

Capex에는 GPU뿐 아니라 CPU, network, building, power equipment 등이 들어간다.

### 오류 2. 최종 사용자 = Direct Customer라고 보는 것

Meta가 NVIDIA GPU를 10만 장 사용한다고 해도 해당 GPU를 Foxconn 또는 Dell을 통해 구매했다면 NVIDIA 회계상 direct customer는 다른 회사일 수 있다.

### 오류 3. 제조업체 = 반드시 Direct Customer라고 보는 것

반대로 Foxconn이 서버를 조립했다고 해서 NVIDIA가 GPU를 Foxconn에 회계상 판매했다고 단정할 수도 없다.

NVIDIA는 direct customer가 third-party integrator를 이용할 수 있다고 명시한다.

### 오류 4. Geography를 최종수요 지역으로 해석

NVIDIA geography는 customer headquarters 기준이다.

따라서 Taiwan revenue가 Taiwan 내 AI demand를 의미하지 않는다.

미국 hyperscaler용 AI server를 대만 ODM이 구매하는 경우 Taiwan revenue로 잡힐 수 있다.

### 오류 5. 서로 다른 시점의 점유율 혼합

FY26 annual concentration, FY27 Q1 concentration, FY27 Q2 concentration을 한 표에서 동일 시점 share처럼 사용하면 안 된다.

모든 edge에는 반드시:

```
period
```

필드를 저장해야 한다.

---

## 13. 고객 실명 추정의 최종 Scoring Model

향후 각 후보를 정량 평가하려면 다음 scoring model을 사용하는 것이 적절하다.

A. Revenue Fit — 30%

후보가 $23B~$29B 구매액을 설명할 수 있는가.

B. Quarterly Trajectory Fit — 25%

후보의 구매 흐름이:

```
16 → 16
21 → <10
17 → <10
```

등 NVIDIA 공시 패턴과 맞는가.

C. Geography Fit — 20%

NVIDIA의 US/non-US revenue distribution과 후보 본사가 일치하는가.

D. Procurement Route Evidence — 20%

NVIDIA 직접 구매 관계가 확인되는가, 아니면 OEM/ODM 경유가 더 가능성 높은가.

E. Product Mix Fit — 5%

해당 기업의 GPU architecture, accelerator mix, 자체 ASIC 사용 등을 고려했을 때 NVIDIA dependence가 충분한가.

예시:

```
Identity Score
=
Revenue Fit × 30%
+ Trajectory Fit × 25%
+ Geography Fit × 20%
+ Procurement Evidence × 20%
+ Product Mix × 5%
```

이를 통해 단순 정성 판단을 피하고 candidate identity를 지속적으로 업데이트할 수 있다.

---

## 14. 현재 Direct Customer 추정 결과

현재 공개자료만을 이용하면 다음과 같이 보는 것이 가장 방어 가능하다.

| 후보 | Top 3 가능성 | 주요 근거 |
|---|---|---|
| Microsoft | High | 미국 HQ, 막대한 GPU/CPU capex, 규모 충족 |
| Meta | High | 미국 HQ, AI infra capex 규모 충족 |
| Dell | Medium-High | 실제 AI server revenue 규모가 Top 3와 유사 |
| Google | Medium | 규모 충분하나 TPU mix 불확실 |
| Amazon | Medium | 규모 충분하나 Trainium/Inferentia mix 불확실 |
| Foxconn | Medium | 제조 물량 충분하나 geography 제약 |
| Quanta/QCT | Medium | NVIDIA 생태계 핵심이나 geography 제약 |
| Wistron/Wiwynn | Medium-Low | 관계 확실, 개별 NVIDIA 구매 규모 검증 필요 |
| Supermicro | Lower | Top customer purchase 규모 대비 회사 매출 제약 |

현 단계의 가장 중요한 결론은:

```
Top 3를 모두 대만 ODM으로 해석하는 것은 부적절하며,
미국계 hyperscaler·AI buyer·OEM이 상당 부분 포함됐을 가능성이 높다.
```

그러나 공개자료만으로:

```
#1 Microsoft = 16%
```

와 같이 확정할 수 있는 수준은 아니다.

---

## 15. NVIDIA의 End-Market 구조

FY27 Q1 NVIDIA는 market platform을 새롭게 표시하기 시작했다.

Q1 매출 구조는:

```
Data Center                        $75.246B
 ├─ Hyperscale                    $37.869B
 └─ AI Clouds, Industrial
    & Enterprise                  $37.377B
Edge Computing                     $6.369B
-------------------------------------------
Total                             $81.615B
```

이었다.

이 분류는 direct customer concentration과 다른 축이다.

즉:

```
Direct customer = 누가 NVIDIA에게 돈을 지급했는가
Market platform = NVIDIA 매출이 어떤 수요군에서 발생했는가
```

를 나타낸다.

따라서 direct-customer share와 hyperscale share를 동일한 customer-market-share 개념으로 비교하면 안 된다.

---

## 16. 향후 AI Cloud가 Downstream에서 더 중요해지는 이유

NVIDIA는 FY27 Q2에 일부 AI cloud partner가 NVIDIA infrastructure를 더 많이 배치할 수 있도록 새로운 사업모델을 도입했다고 밝혔다.

AI cloud가 NVIDIA infrastructure를 구매하고, 반대편에서 NVIDIA는 해당 AI cloud의 cloud service 사용을 장기간 약정하는 구조다.

2026년 7월 26일 기준 관련 AI cloud agreement commitment는 $36B였다.

구조는 다음과 같다.

```
NVIDIA
   │
   │ AI infrastructure
   ▼
AI Cloud
   │
   │ Compute capacity
   ▼
NVIDIA / Third-party users
```

따라서 앞으로 NVIDIA downstream은 단순 vendor-customer 구조보다:

```
Vendor + investor + demand guarantor + cloud buyer
```

가 동시에 존재하는 복합 ecosystem으로 진화하고 있다.

이는 AI cloud 업체의 구매력과 NVIDIA revenue concentration을 분석할 때 반드시 반영해야 한다.

---

## 17. 최종 NVIDIA Value Chain

```
                    [UPSTREAM]

Foundry
TSMC
   │
   ▼
HBM / Memory
SK hynix / Micron / Samsung
   │
   ▼
Advanced Packaging
TSMC + packaging ecosystem
   │
   ▼
System Components / Networking / Substrates
   │
   ▼

                    [NVIDIA]
          NVIDIA AI Infrastructure
   GPU + CPU + Networking + Software
                   │
                   │
        ┌──────────┼───────────┐
        ▼          ▼           ▼
   Direct CSP     OEM/SI       ODM
 Microsoft?      Dell        Foxconn
 Meta?           HPE         QCT
 Google?       Supermicro    Wistron
 AWS?                       Wiwynn
        │          │           │
        └──────────┼───────────┘
                   ▼
                 AI Cloud
        CoreWeave / Lambda / Nebius
                   │
                   ▼
              AI Model Maker
          OpenAI / Anthropic / etc.
                   │
                   ▼
              Enterprise/User
```

여기에서 ?는 관계 자체가 없다는 뜻이 아니라 NVIDIA 회계상 direct customer identity가 확인되지 않았다는 의미다.

---

## 18. 데이터베이스 설계 원칙

각 회사 간 edge에 하나의 share만 넣어서는 안 된다.

최소 다음 필드가 필요하다.

```
source_company
target_company
relationship_type
  - direct_sale
  - indirect_demand
  - manufacturing
  - component_supply
  - cloud_service
  - strategic_investment
metric_type
  - revenue_share
  - estimated_spend_share
  - shipment_share
  - capacity_share
value
unit
period_start
period_end
denominator
evidence_type
  - company_filing
  - official_announcement
  - third_party
  - model_estimate
confidence
  - confirmed
  - high
  - medium
  - low
source_url
assumptions
estimation_method
```

예를 들어 anonymous customer는:

```
source: NVIDIA
target: Direct Customer #1
relationship:
direct_sale
period:
FY27 H1
revenue_share:
16%
estimated_value:
$28.45B
identity_candidate:
Microsoft
identity_status:
estimated
identity_confidence:
medium-high
reported_share_status:
confirmed
```

로 저장한다.

별도로:

```
NVIDIA → Microsoft
relationship:
platform adoption / potential direct procurement
relationship_confidence:
confirmed/high
revenue_share:
unknown
```

를 저장한다.

이렇게 해야 확정 관계와 추정 identity가 데이터베이스에서 서로 오염되지 않는다.

---

## 19. 결론

NVIDIA 밸류체인 분석의 핵심은 단순히 supplier와 customer 이름을 나열하는 것이 아니다.

가장 중요한 것은 돈의 흐름, 제품의 흐름, 최종수요의 흐름을 서로 분리하는 것이다.

NVIDIA 공시로 확정 가능한 것은:

* FY27 H1 매출 $177.837B
* Direct customer Top 3 concentration 16% / 15% / 13%
* Q2 단일 direct customer concentration 16%
* Customer headquarters 기준 US/non-US 매출
* Direct/indirect customer 정의
* Hyperscale / ACIE / Edge market platform
* $279B supply and capacity commitments

등이다.

반면 공개되지 않는 것은:

* 16/15/13% 고객의 실명
* 각 hyperscaler의 정확한 NVIDIA 구매액
* Foxconn/Quanta/Dell을 경유하는 물량 비중
* TSMC/HBM supplier별 NVIDIA procurement share
* anonymous indirect customer별 정확한 경제적 최종수요

다.

따라서 추정은 반드시 다음 순서로 수행해야 한다.

```
공시 숫자 확보
→ 기간별 concentration 연결
→ geography constraint 적용
→ 후보 기업 구매능력 비교
→ product/BOM 분석
→ procurement route 검증
→ range 및 confidence 부여
→ 새 공시가 나올 때 update
```

이 방법의 장점은 특정 기업명을 맞히는 것 자체보다 왜 해당 기업이 후보인지, 어떤 가정을 사용했는지, 무엇이 틀리면 결론이 바뀌는지까지 설명할 수 있다는 점이다.

최종적으로 NVIDIA의 밸류체인은 하나의 정적인 그림보다, 각 node와 edge가 period + metric + source + confidence + estimation logic을 보유하는 time-dependent value-chain database로 관리하는 것이 가장 적합하다.
