---
source: content/understanding/Semi Doped/2026-08-27-openai-jalapeno.md
kind: tech
model: Gemini (Chrome)
asked: 반도체 아키텍처·시스템 엔지니어링 관점에서 딥다이브하라 (업계 기술 전문가)
date: 2026-08-30
named: 550W · 1.5~1.9배 · RoCEv2 · PCIe · SRAM 핀닝 (안 가져왔다고 카드에 이름만 댄 것)
used: 프리필=연산 바운드·디코드=메모리 바운드 (업계 상식으로 표시하고 인용)
---

이 파일은 **미검증 원본**이다. 대조 결과 사양의 대부분이 원문 밖이었고, 해법과 네트워크는
원문과 반대였다. 카드로 옮긴 것은 위 `used` 한 줄뿐이다.

## 받은 답 (요지)

- 핵심 테제 — 메모리 월과 배치 확장에 따른 지연 페널티를 온칩 통신 최소화와 Spatial
  Compute 패러다임으로 극복한 추론 특화 칩.
- 실리콘 — TSMC 3nm(N3P) + CoWoS 패키징 / HBM4 3D 스택, HBM3E 대비 I/O 핀 확장 /
  TDP 700W(연속 실측 550W 내외), GB200 1000~1200W / Broadcom PCIe Gen6 및 차세대
  이더넷(RoCEv2 · Ultra Ethernet Consortium) 스위칭을 D2D·랙 간 인터커넥트에 직결.
- 아키텍처 — 범용 GPU 는 SIMT 기반이라 큰 배치를 강제해 TTFT·ITL 이 늘어난다.
  Jalapeño 는 HBM4 → 분산 온칩 SRAM → Systolic/Spatial 연산기 꼴이고, KV 캐시를 타일
  단위로 SRAM 에 핀닝해 DRAM 왕복을 끊는다. MoE 라우팅은 하드웨어 크로스바로 처리.
- 소프트웨어 — CUDA 런타임을 안 거치고 Triton 기반 파생 컴파일러와 사내 런타임(Gluon)으로
  직접 제어. 커널 퓨전·그래프 실행으로 스필을 0 에 가깝게. 배치 1~4 에서도 MFU 60% 이상.
- 트레이드오프 — kW당 토큰 1.5~1.9배 · 지연 단축 / 범용 연산기 부재로 Diffusion·State
  Space 등 비정형 대응력 저하 / 개발-양산 주기 18~24개월 동안 모델 구조가 바뀌면 실리콘
  고정화 위험 / CUDA 수준의 디버깅·프로파일링 툴체인을 자체 인력으로 감당해야 한다.
