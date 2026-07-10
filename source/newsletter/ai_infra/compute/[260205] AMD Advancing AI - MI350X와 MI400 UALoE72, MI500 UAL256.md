---
categories: [ai-infra/compute]
---

# AMD Advancing AI: MI350X and MI400 UALoE72, MI500 UAL256

> **출처**: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256)
> **저자**: Kimbo Chen, Dylan Patel, Daniel Nishball
> **발행일**: 2026-02-05

---

## 📑 목차

### 전체 섹션
 1. [개요 - AMD Advancing AI 2025 발표 요약](#1-개요---amd-advancing-ai-2025-발표-요약)
 2. [MI350X·MI355X 스펙 - CDNA4 기반 신제품](#2-mi350x·mi355x-스펙---cdna4-기반-신제품)
 3. [MI355X vs HGX B200 - 성능당비용(TCO) 경쟁력](#3-mi355x-vs-hgx-b200---성능당비용tco-경쟁력)
 4. [엔비디아 DGX Lepton과 뉴클라우드의 반발](#4-엔비디아-dgx-lepton과-뉴클라우드의-반발)
 5. [MI355X는 랙 스케일 솔루션이 아니다 - 마케팅 과장 논란](#5-mi355x는-랙-스케일-솔루션이-아니다---마케팅-과장-논란)
 6. [하이퍼스케일러·AI 랩의 AMD 신제품 채택 현황](#6-하이퍼스케일러·ai-랩의-amd-신제품-채택-현황)
 7. [AMD 뉴클라우드 렌탈 시장의 구조적 약점](#7-amd-뉴클라우드-렌탈-시장의-구조적-약점)
 8. [AMD의 뉴클라우드 생태계 육성 전략](#8-amd의-뉴클라우드-생태계-육성-전략)
 9. [ROCm 소프트웨어 개선과 엔지니어링 우선순위 이슈](#9-rocm-소프트웨어-개선과-엔지니어링-우선순위-이슈)
10. [MI355X 제조 - 칩렛 아키텍처 리파인](#10-mi355x-제조---칩렛-아키텍처-리파인)
11. [CDNA4 마이크로아키텍처(UArch) 상세](#11-cdna4-마이크로아키텍처uarch-상세)
12. [AMD AI 엔지니어 보상 현실화 움직임](#12-amd-ai-엔지니어-보상-현실화-움직임)
13. [MI400 시리즈 Flexible I/O와 UALoE72 - 진짜 UALink는 아니다](#13-mi400-시리즈-flexible-io와-ualoe72---진짜-ualink는-아니다)
14. [MI400 Helios 랙 아키텍처 상세](#14-mi400-helios-랙-아키텍처-상세)
15. [MI500 UAL256 - 2027년 차세대 랙 컨셉](#15-mi500-ual256---2027년-차세대-랙-컨셉)
16. [MI350X·MI355X·MI400 BOM과 TCO 비교](#16-mi350x·mi355x·mi400-bom과-tco-비교)

---

## 🔑 용어 정리

본문을 순서대로 읽기 전에 알아두면 좋은 용어들입니다. 자세한 수치와 설명은 본문에서 처음 등장하는 위치에 나옵니다.

- **TCO(총소유비용, Total Cost of Ownership)**: 장비 구매 비용뿐 아니라 운영·전력·유지보수까지 합친 전체 비용 — 이 문서 전반에서 AMD와 Nvidia 제품을 비교하는 핵심 잣대
- **랙 스케일(Rack Scale) 솔루션**: 랙 안의 모든 GPU가 하나의 초고속 네트워크로 묶여 마치 GPU 1개처럼 작동하는 설계 — 몇 개의 서버를 그냥 한 랙에 모아놓은 것과는 다름
- **뉴클라우드(Neocloud)**: 하이퍼스케일러(Google·AWS 등 대형 클라우드)가 아니면서 GPU를 임대해주는 전문 GPU 클라우드 업체(예: CoreWeave, Tensorwave, Crusoe)
- **ROCm**: AMD GPU를 위한 오픈소스 소프트웨어 스택 — Nvidia의 CUDA에 대응하는 개념
- **UALink vs UALoE**: UALink는 여러 업체가 공동 개발 중인 GPU 스케일업(랙 내부 초고속 연결) 표준 규격 자체, UALoE(UALink over Ethernet)는 그 규격을 이더넷 스위치 위에 얹어 흉내만 낸 것 — 이 문서의 핵심 논쟁거리
- **BOM(부품 명세서, Bill of Materials)**: 시스템 하나를 만드는 데 들어가는 모든 부품과 그 원가를 나열한 목록
- **CU(컴퓨트 유닛, Compute Unit)**: AMD GPU 내부의 연산 처리 단위 — Nvidia의 SM(Streaming Multiprocessor)에 대응하는 개념
- **DGX Lepton**: Nvidia가 내놓은 GPU 임대 마켓플레이스 — 여러 클라우드의 GPU를 하나의 표준화된 창구로 묶어 파는 서비스

---

*작성 진행률: 약 5% 완료 (헤더·목차·용어 정리 작성)*
*업데이트: 헤더, 목차, 용어 정리 작성 완료 — 본문 섹션 작성 예정*
