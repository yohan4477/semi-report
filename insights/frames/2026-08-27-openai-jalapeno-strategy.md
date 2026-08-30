---
source: content/understanding/Semi Doped/2026-08-27-openai-jalapeno.md
kind: strategy
model: Gemini (Chrome)
asked: 전략컨설턴트처럼 구조적으로 설명하라 (McKinsey/BCG 시니어 파트너 · MECE · Executive Summary)
date: 2026-08-30
named: 550W · 1.5~1.9배 (안 가져왔다고 카드에 이름만 댄 것)
used: 목적함수 대비 · 밸류체인 전후 도식 · 리스크 절
---

이 파일은 **미검증 원본**이다. 여기 있는 문장은 카드로 그대로 옮기지 않는다 —
`insights/check_frame.py` 로 원문과 대조한 뒤, 원문이 받쳐 주는 것만 옮긴다.

## 받은 답 (요지)

- 핵심 테제 — Jalapeño 는 하드웨어 내재화가 아니라 추론 비용 구조 혁신 · Nvidia 종속
  탈피 · 풀스택 수직계열화의 전환점이다.
- 전략적 배경 — 추론 비용(OPEX) 증가 대응 · 벤더 락인 완화 · SW-HW co-design 으로
  전력당 처리량(Tokens/kW) 극대화.
- 핵심 역량 표 — Broadcom(ASIC 공동 설계) + TSMC(3nm) + HBM4 / TDP 700W(실측 550W 내외)
  / GB200·GB300 대비 kW당 토큰 1.5~1.9배, 지연 1.7~3.6배 / Spatial Architecture ·
  온칩 메모리-연산 밀결합 · Gluon 프레임워크 · KV 캐시 이동 최소화.
- 밸류체인 — [모델] → [Nvidia GPU/CUDA] → [Azure] 에서 [모델] → [Jalapeño ASIC] →
  [자체·하이브리드 DC] 로.
- 파급 — 프론티어 랩의 커스텀 실리콘 가속(Google TPU · Amazon Trainium · Meta MTIA 에
  이어 OpenAI 와 Anthropic 까지) · HBM/첨단 패키징 캐파 경쟁 · 학습은 Nvidia 유지,
  추론은 ASIC 잠식.
- 리스크 — CUDA 대비 툴체인 성숙도 · 칩 개발 주기(18~24개월)와 모델 구조 변화의 괴리 ·
  차세대 GPU(Vera Rubin) 와의 격차 유지.

## 두 번째 답 (같은 각도, 서사형)

- 물음을 「Jalapeño 가 NVIDIA 를 대체하나」에서 「모델 회사가 자체 HW 를 만들면 NVIDIA 의
  가치사슬상 구조적 우위가 약해지나」로 바꾼다.
- 목적함수 대비 — NVIDIA 고객은 하이퍼스케일러라 다양한 워크로드·TCO, OpenAI 고객은 최종
  사용자라 지연·에너지. 그래서 수직 결합으로 극단적 co-design 이 가능하다.
- 층 넷 — User Experience / AI Workload(Prefill·Decode·KV·Speculative) / Jalapeño /
  System(128→2,048 · ESUN).
- HBM 은 더 빠르게가 답이 아니다 — Peak Bandwidth ≠ Effective Bandwidth, operands arrive late.
- Theoretical Performance → Delivered Performance 로 경쟁축 이동.
- Dark silicon is cheaper than idle accelerators 를 균형 설계로 설명.
- 9개월 → AI 도구가 반도체 설계 생산성을 올려 진입장벽이 낮아진다.
- Impact Map(NVIDIA 🔴 · AMD 🔴 · Google TPU 🟠 · ASIC 스타트업 🔴 · EDA 🟢 · HBM 🟠 …).
- 마지막 물음 — 1년 안에 쓸 만한 가속기를 만들 수 있다면 범용 GPU 의 해자는 무엇인가.

## 이 답이 붙인 각주 (원문 확인 필요)

- 「Semi Doped 도 대규모 생산·배포에서 reliability 와 scalability 를 증명해야 한다고 지적」
- 「Semi Doped 는 9개월을 AI tools + experienced team + blank-sheet architecture 로 해석」
- 「Semi Doped 도 이 점을 Google TPU 와 비교한다」
