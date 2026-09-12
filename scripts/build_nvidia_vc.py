# -*- coding: utf-8 -*-
u"""AI 가속기 사슬 — NVIDIA. migrate_nvidia_ship.py 가 옮긴 v1 여섯 장을 이 빌더로 갈아 끼운다.

Drive `value chain 분석/NVIDIA` 의 01~05 가 canonical 이다. 거기 있는 것만 옮긴다.
  01_NVIDIA 조사 추적과정                1RdmW8_MySPfStGhBDnpFjn9slOA8CA45NQQO12XQR8o
  02_NVIDIA Value Chain                 1-t6wbc16ieSRVvs30-rXIwpMeO-jBEU9P8kpMHPsbRM
  03_NVIDIA Evidence & Sources          1oJB9uQE2f16mOKIfkZUmj128dk5Db9_hyjmLjHKpXqM
  04_NVIDIA Entities & Edges            1wsoz-O2amfculwosoZuyzhx_zuixAIqX_LYVcKVtu1k
  05_NVIDIA UIUX & Implementation Guide 1Ka4molFybAbrAIBLAZOIkMiN2UyAE9gJB_8jVnzHKrw

04 의 Entities 탭 23개(NVDA 포함) 가운데 TSMC·삼성전자·SK하이닉스·마이크론·폭스콘·위스트론·
페브리넷·AWS·코어위브·네비우스·오픈AI·마벨·아마존은 다른 사슬이 이미 전역에 갖고 있다.
그 열둘은 ENTITIES 에 다시 넣지 않고 관계에서 전역 id(samsung-electronics·sk-hynix 등)만
참조한다 — 다시 넣으면 merge() 가 저쪽 레코드를 얇은 버전으로 덮어쓴다. 새로 넣는 것은
SPIL·Kinsus·KYEC·Unimicron·Coherent·Lumentum·MediaTek·SSI·SpaceXAI 아홉뿐이다.

04 의 Edges 탭(R001~R023)이 유일한 관계 원장이다. 02·01 본문이 거론하는 Dell·HPE·Pegatron·
WEKA·DDN 등은 Edges 탭에 없어 상자로 넣지 않는다 — 「직접 확인되지 않으면 잇지 않는다」는
01 §3·§5 원칙 그대로다.

Revenue Mix/Market Platform(FY2024~26 Data Center/Gaming/ProViz/Automotive/OEM, FY2027
Hyperscale/ACIE/Edge Computing)은 04 에 상자로 없다 — Drive 05 §13 이 "analytical
classification, not entity node"라고 못박는다. 이 저장소는 매출원 상자로 세우고 vc_norm 이
분류로 접는다(프레임워크 §22·§23, build_taiyo_vc.py 와 같은 자리). RevenueCustomerMap(RCM001
~021)은 전부 UNALLOCATED_CUSTOMER 버킷이라 실명 매핑은 없다 — apply_recast() 가 분류마다
residual 만 적는다.

04 의 Observations 탭(OBS001~011)은 개별 관계가 없는 전사 절대값(직접·간접 고객 집중도,
데이터센터 세부 비중)이라 관측이 아니라 주장으로 옮긴다 — 태양유전·네비우스 사슬이 세운
관례다(build_taiyo_vc.py, build_nebius_vc.py 의 독스트링). 이 열한 줄은 03 에 개별 출처
번호가 없어(04 Observations 탭에 source_id 칸이 없다) 조사 원장 출처(nv_obs_ledger) 하나로
묶어 잇는다. Q1·H1·AR 집중도처럼 03 에 전용 claim id(NV-CUST-002/001/003)가 붙은 것은 그
출처를 쓴다.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'nvidia')
NV = 'nvidia'

REGION = {'대만': 'Asia', '미국': '미국', '한국': 'Asia'}

# ── 출처 (03 NV-* 26 줄 + 조사 원장 1줄) ─────────────────────────────
SOURCES = [
 ('nv_fin_001', 'NVIDIA Corporation', 'FY2026 Form 10-K', 'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'FY2026 총매출 2,159억 3,800만 달러, 데이터센터 1,937억 3,700만 달러(89.7%). 회사 총매출 기준'),
 ('nv_fin_002', 'NVIDIA Corporation', '2027 회계연도 2분기 Form 10-Q(2026-07-26 마감)',
  'primary_official', '2026-08-26',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  '2분기 데이터센터 890억 2,300만 달러 = 하이퍼스케일 487억 1,000만 달러 + ACIE 403억 1,300만 '
  '달러, 엣지 컴퓨팅 71억 9,800만 달러. 2분기 총매출 962억 2,100만 달러. 시장·플랫폼 구분으로 '
  '표시 방식이 바뀌었다'),
 ('nv_fin_003', 'NVIDIA Corporation', 'FY2026 Form 10-K 비교표(FY2024~FY2026)',
  'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'FY2024/FY2025/FY2026 데이터센터 매출 475억 2,500만/1,151억 8,600만/1,937억 3,700만 달러, '
  '총매출 609억 2,200만/1,304억 9,700만/2,159억 3,800만 달러. 레거시 전방시장 구분'),
 ('nv_cust_001', 'NVIDIA Corporation', '2027 회계연도 2분기 Form 10-Q', 'primary_official',
  '2026-08-26', 'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  'H1 FY2027 직접고객 집중도 16%·15%·13%(회사 총매출 기준). 실명은 비공개'),
 ('nv_cust_002', 'NVIDIA Corporation', '2027 회계연도 1분기 Form 10-Q', 'primary_official',
  '2026-05-20', 'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm',
  'Q1 FY2027 직접고객 세 곳이 총매출의 21%·17%·16%. 실명은 비공개'),
 ('nv_cust_003', 'NVIDIA Corporation', '2027 회계연도 2분기 Form 10-Q', 'primary_official',
  '2026-08-26', 'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  '2026-07-26 기준 매출채권 잔액의 22%·14%·13%·11%·10%를 직접고객 다섯 곳이 차지한다. 매출 '
  '비중과는 분모가 다르다'),
 ('nv_sup_001', 'NVIDIA Corporation', 'FY2026 Form 10-K', 'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'TSMC 와 삼성전자가 엔비디아의 반도체 웨이퍼 파운드리다. 배분 비중은 비공개'),
 ('nv_sup_002', 'NVIDIA Corporation', 'FY2026 Form 10-K', 'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'SK하이닉스·마이크론·삼성전자가 엔비디아에 메모리를 공급한다. 공급사별 정확한 비중은 비공개'),
 ('nv_sup_003', 'NVIDIA Corporation', 'FY2026 Form 10-K', 'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'CoWoS 첨단 패키징 기술을 쓴다고 밝힌다. 엔비디아 전용 용량 비중은 비공개'),
 ('nv_sup_004', 'NVIDIA Corporation', 'FY2026 Form 10-K', 'primary_official', '2026-02-25',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm',
  'Hon Hai(폭스콘)·위스트론·페브리넷이 조립·시험·패키징을 맡는 하청업체다. 개별 물량 비중은 '
  '비공개'),
 ('nv_rub_001', 'NVIDIA', 'Powering the Taiwan Ecosystem for Global AI Infrastructure',
  'primary_company', None, 'https://blogs.nvidia.com/blog/taiwan-ecosystem-ai-infrastructure/',
  'Rubin 생태계 — TSMC·SPIL·Kinsus·KYEC·Unimicron 이 웨이퍼·칩 파트너, 폭스콘·페가트론·QCT·'
  '위스트론·인벤텍이 제조·시스템 리더다. 생태계 역할일 뿐 개별 상거래선은 별도로 확인돼야 '
  '한다'),
 ('nv_rub_002', 'NVIDIA', 'NVIDIA Vera Rubin Ramps Into Full Production to Power Agentic AI '
  'Factories Worldwide', 'primary_company', None,
  'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Vera-Rubin-Ramps-Into-'
  'Full-Production-to-Power-Agentic-AI-Factories-Worldwide/default.aspx',
  'Dell·HPE·Lenovo·Supermicro 등 폭넓은 ODM·스토리지 파트너가 참여하는 생산 생태계. 개별 '
  '물량 비중은 비공개'),
 ('nv_hbm_001', 'TrendForce', 'HBM Market Bulletin 2026', 'industry_research', None, None,
  'Rubin HBM4 를 둘러싼 세 공급사 생태계 추정. 엔비디아 공시가 아니라 제3자 추정치이며 '
  '검증 일정이 바뀌면서 해가 가는 동안 수치가 달라졌다'),
 ('nv_opt_001', 'NVIDIA / Coherent', 'NVIDIA and Coherent Announce Strategic Partnership to '
  'Develop Optics Technology to Scale Next-Generation Data Center Architecture',
  'primary_company', '2026-03-02',
  'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Coherent-Announce-'
  'Strategic-Partnership-to-Develop-Optics-Technology-to-Scale-Next-Generation-Data-Center-'
  'Architecture/default.aspx',
  '다중 십억 달러 구매 약정 + 미래 용량권 + 엔비디아의 20억 달러 지분투자'),
 ('nv_opt_002', 'NVIDIA / Lumentum', 'NVIDIA Announces Strategic Partnership With Lumentum to '
  'Develop State-of-the-Art Optics Technology', 'primary_company', '2026-03-02',
  'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Strategic-'
  'Partnership-With-Lumentum-to-Develop-State-of-the-Art-Optics-Technology/default.aspx',
  '다중 십억 달러 구매 약정 + 미래 용량권 + 엔비디아의 20억 달러 지분투자'),
 ('nv_down_001', 'AWS / NVIDIA', '2026-08-26 공동 발표', 'primary_company', '2026-08-26', None,
  'AWS 가 2027~28년 엔비디아 GPU 200만 개 추가 도입을 계획. Vera CPU·NVLink Fusion·NVHBM '
  '통합. 익명 고객 집중도 수치와 매핑하지 않는다'),
 ('nv_down_002', 'NVIDIA', '2026-01-26 공식 발표', 'primary_company', '2026-01-26', None,
  '코어위브와 2030년까지 5GW 넘는 협력. 엔비디아가 20억 달러를 투자했다'),
 ('nv_down_003', 'NVIDIA', 'NVIDIA and Nebius Partner to Scale Full-Stack AI Cloud',
  'primary_company', '2026-03-11',
  'https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-and-Nebius-Partner-to-'
  'Scale-Full-Stack-AI-Cloud/',
  '네비우스와 2030년까지 5GW 넘는 협력. 엔비디아가 20억 달러를 투자했다'),
 ('nv_down_004', 'NVIDIA / OpenAI', '2025-09-22 공식 발표', 'primary_company', '2025-09-22',
  None, '오픈AI 가 최소 10GW 규모 엔비디아 시스템 구매 의향서(LOI)를 맺었다. 엔비디아는 배치가 '
  '진행됨에 따라 최대 1,000억 달러까지 투자할 의향이 있다고 밝혔다'),
 ('nv_down_005', 'NVIDIA / SSI', "Ilya Sutskever's Safe Superintelligence Inc. and NVIDIA "
  'Announce Long-Term Strategic Partnership', 'primary_company', '2026-07-27',
  'https://investor.nvidia.com/news/press-release-details/2026/Ilya-Sutskevers-Safe-'
  'Superintelligence-Inc--and-NVIDIA-Announce-Long-Term-Strategic-Partnership/default.aspx',
  '장기 전략 제휴, 엔비디아의 투자, Rubin 시스템 접근권'),
 ('nv_down_006', 'NVIDIA', 'SpaceXAI Adopts NVIDIA Vera CPU to Accelerate Agentic AI at '
  'Massive Scale', 'primary_company', '2026-08-24',
  'https://investor.nvidia.com/news/press-release-details/2026/SpaceXAI-Adopts-NVIDIA-Vera-CPU-'
  'to-Accelerate-Agentic-AI-at-Massive-Scale/default.aspx',
  'Vera CPU 도입과 Vera Rubin 기반 인프라 확장. Starmind 위성이 예로 들린다'),
 ('nv_arch_001', 'NVIDIA', 'NVLink Fusion', 'primary_company', None,
  'https://www.nvidia.com/en-us/data-center/nvlink-fusion/',
  '제3자 커스텀 XPU·CPU 를 엔비디아 랙 스케일 AI 팩토리 아키텍처에 통합하는 규격이다'),
 ('nv_stx_001', 'NVIDIA', 'BlueField-4 STX/CMX', 'primary_company', None,
  'https://www.nvidia.com/en-us/data-center/ai-storage/cmx/',
  'AI 네이티브 컨텍스트·KV 캐시 스토리지 레인이다. 채택이 곧 직접 고객을 뜻하지 않는다'),
 ('nv_dsx_001', 'NVIDIA', 'Vera Rubin DSX', 'primary_company', None, None,
  'DSX 참조 설계에 Eaton·Schneider·Siemens·Trane·Vertiv·Jacobs·Switch 등이 참여한다. 부지 '
  '인프라·참조설계 레인이지 제품 BOM 이 아니다'),
 ('nv_rev_recast_001', 'NVIDIA Corporation', '2027 회계연도 2분기 Form 10-Q',
  'primary_official', '2026-08-26',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  '2027 회계연도 1분기부터 시장·플랫폼 표시로 바뀌었고 2분기에 한 회사를 ACIE 에서 하이퍼스케일로 '
  '재분류하며 이전 기간도 다시 표시했다. 분류는 시점마다 다른 관측이지 고정된 성격이 아니다'),
 ('nv_sem_001', 'NVIDIA Corporation', 'FY2026 10-K + 2027 회계연도 2분기 10-Q',
  'primary_official', '2026-08-26',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  'FY2024~26 공시는 "전방시장별 매출", FY2027 2분기는 "시장·플랫폼별 매출"이라는 이름을 쓴다. '
  '이 구분 자체는 특정 고객 귀속의 근거가 아니다'),
 ('nv_skh_001', 'NVIDIA / SK Group', 'SK Group and NVIDIA Expand Strategic Partnership Across '
  'AI Factories and Next-Generation Memory', 'primary_company', '2026-07-24',
  'https://investor.nvidia.com/news/press-release-details/2026/SK-Group-and-NVIDIA-Expand-'
  'Strategic-Partnership-Across-AI-Factories-and-Next-Generation-Memory/default.aspx',
  '차세대 AI 메모리(HBM 포함)를 함께 확보·공동개발하는 장기 제휴다. 일반 메모리 공급 관계와는 '
  '별도로 다룬다'),
 ('nv_map_001', 'NVIDIA Corporation', 'FY2026 10-K + 2027 회계연도 2분기 10-Q + 프레임워크 규칙',
  'primary_official', '2026-08-26',
  'https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm',
  '매출 구분·시장 플랫폼별 실명 고객 귀속은 공시되지 않는다. 파트너 목록을 매출 배분으로 '
  '승격하지 않는다'),
 ('nv_obs_ledger', u'조사 원장', '04 Observations 탭 (Drive)', 'research_ledger', None, None,
  u'OBS001~011 고객 집중도·데이터센터 세부 비중이 원장에 적혀 있다. 개별 10-K/10-Q 조항 '
  u'번호는 원장에 없어 발행 문서명·마감일만 특정한다'),
]

# ── 엔티티 — 04 Entities 탭 23개 중 전역에 없는 9개만 새로 넣는다 ────
ENTITIES = [
 ('spil', 'Siliconware Precision Industries Co., Ltd.', '실리콘웨어(SPIL)', 'company', '대만',
  ['Packaging partner'], 'Rubin 생태계의 웨이퍼·칩 파트너로 이름이 오른다. 엔비디아와의 직접 '
  '상거래 몫은 공개되지 않는다'),
 ('kinsus', 'Kinsus Interconnect Technology Corp.', '킨서스', 'company', '대만',
  ['Substrate partner'], '기판(서브스트레이트) 파트너로 Rubin 생태계에 이름이 오른다. 개별 '
  '물량은 비공개'),
 ('kyec', 'King Yuan Electronics Co., Ltd.', '킹윤일렉트로닉스(KYEC)', 'company', '대만',
  ['Test partner'], '테스트 파트너로 Rubin 생태계에 이름이 오른다. 개별 물량은 비공개'),
 ('unimicron', 'Unimicron Technology Corp.', '유니마이크론', 'company', '대만',
  ['Substrate partner'], '기판(서브스트레이트) 파트너로 Rubin 생태계에 이름이 오른다. 개별 '
  '물량은 비공개'),
 ('coherent', 'Coherent Corp.', '코히런트', 'company', '미국', ['Optics supplier'],
  '광통신 부품·용량 공급사이자 엔비디아로부터 20억 달러 지분투자를 받았다'),
 ('lumentum', 'Lumentum Holdings Inc.', '루멘텀', 'company', '미국', ['Optics supplier'],
  '광통신 부품·용량 공급사이자 엔비디아로부터 20억 달러 지분투자를 받았다'),
 ('mediatek', 'MediaTek Inc.', '미디어텍', 'company', '대만', ['Custom silicon partner'],
  'NVLink Fusion 생태계의 커스텀 XPU 설계 파트너다'),
 ('ssi', 'Safe Superintelligence Inc.', '세이프 슈퍼인텔리전스(SSI)', 'company', '미국',
  ['AI model maker'], '2026년 7월 엔비디아와 장기 전략 제휴를 맺고 투자를 받았으며 Rubin '
  '시스템에 접근한다'),
 ('spacexai', 'SpaceXAI', '스페이스XAI', 'company', '미국', ['AI infrastructure operator'],
  '2026년 8월 Vera CPU 를 도입하고 Vera Rubin 기반 인프라를 확장한다고 발표했다. 회계상 '
  '직접고객 지위는 별도로 주장되지 않는다'),
 # 매출원 상자 — vc_norm 이 분류로 접는다. 04 Entities 탭에는 없다(05 §13: analytical
 # classification, not entity node). REV001~021 의 값을 얹는 자리일 뿐이다
 ('nv-rev-datacenter', 'Data Center', '데이터센터 매출', 'revenue_type', None,
  ['Revenue type'], 'FY2024~FY2026 레거시 전방시장 구분의 최대 갈래. FY2027부터는 '
  '하이퍼스케일·ACIE 로 재편됐다'),
 ('nv-rev-gaming', 'Gaming', '게이밍 매출', 'revenue_type', None, ['Revenue type'],
  'FY2024~FY2026 레거시 전방시장 구분. FY2027 표시에서는 엣지 컴퓨팅에 흡수됐다'),
 ('nv-rev-proviz', 'Professional Visualization', '프로페셔널 시각화 매출', 'revenue_type',
  None, ['Revenue type'], 'FY2024~FY2026 레거시 전방시장 구분. FY2027 표시에서는 엣지 '
  '컴퓨팅에 흡수됐다'),
 ('nv-rev-automotive', 'Automotive', '자동차 매출', 'revenue_type', None, ['Revenue type'],
  'FY2024~FY2026 레거시 전방시장 구분. FY2027 표시에서는 엣지 컴퓨팅에 흡수됐다'),
 ('nv-rev-oem-other', 'OEM and Other', 'OEM·기타 매출', 'revenue_type', None,
  ['Revenue type'], 'FY2024~FY2026 레거시 전방시장 구분. FY2027 표시에서는 엣지 컴퓨팅에 '
  '흡수됐다'),
 ('nv-rev-hyperscale', 'Hyperscale', '하이퍼스케일 매출', 'revenue_type', None,
  ['Revenue type'], 'FY2027 1분기부터 쓰는 시장·플랫폼 구분. 데이터센터 매출을 ACIE 와 '
  '둘로 가른 한쪽이다'),
 ('nv-rev-acie', 'AI Clouds, Industrial & Enterprise (ACIE)', 'AI 클라우드·산업·기업(ACIE) '
  '매출', 'revenue_type', None, ['Revenue type'], 'FY2027 1분기부터 쓰는 시장·플랫폼 구분. '
  '데이터센터 매출의 나머지 한쪽'),
 ('nv-rev-edge-computing', 'Edge Computing', '엣지 컴퓨팅 매출', 'revenue_type', None,
  ['Revenue type'], 'FY2027 표시의 데이터센터 바깥 구분. 옛 게이밍·프로페셔널 시각화·자동차·'
  'OEM 이 여기로 흡수됐고 따로 공시되지 않는다'),
]

# ── 관계 — 04 Edges 탭 R001~R023. 이미 전역에 있는 회사는 그 id 를 쓴다 ──
# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence, src_tier, tgt_tier, sources, notes)
R = [
 # ── 업스트림(R001~R009·R011·R021) — lane MANUFACTURING_BOM ─────────
 ('nv-tsmc-foundry', 'tsmc', NV, 'MANUFACTURES', 'MANUFACTURING_BOM', 'Foundry',
  '반도체 웨이퍼 파운드리', '파운드리', '엔비디아', None, None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['nv_sup_001'], '웨이퍼 배분 비중은 공개되지 않는다(04의 R001)'),
 ('nv-samsung-foundry', 'samsung-electronics', NV, 'MANUFACTURES', 'MANUFACTURING_BOM',
  'Foundry', '반도체 웨이퍼 파운드리', '파운드리', '엔비디아', None, None, 'ACTIVE',
  'CONFIRMED', 'COMPONENT_SUPPLIER', None, ['nv_sup_001'],
  '웨이퍼 배분 비중은 공개되지 않는다(04의 R002)'),
 ('nv-skhynix-memory', 'sk-hynix', NV, 'SUPPLIES', 'MANUFACTURING_BOM', 'Memory',
  '메모리·HBM', '메모리 공급사', '엔비디아', None, None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['nv_sup_002'], '정확한 공급 비중은 공개되지 않는다(04의 R003)'),
 ('nv-micron-memory', 'micron', NV, 'SUPPLIES', 'MANUFACTURING_BOM', 'Memory', '메모리·HBM',
  '메모리 공급사', '엔비디아', None, None, 'ACTIVE', 'CONFIRMED', 'COMPONENT_SUPPLIER', None,
  ['nv_sup_002'], '정확한 공급 비중은 공개되지 않는다(04의 R004)'),
 ('nv-samsung-memory', 'samsung-electronics', NV, 'SUPPLIES', 'MANUFACTURING_BOM', 'Memory',
  '메모리·HBM', '메모리 공급사', '엔비디아', None, None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['nv_sup_002'], '정확한 공급 비중은 공개되지 않는다(04의 R005)'),
 ('nv-foxconn-cm', 'foxconn', NV, 'CONTRACT_MANUFACTURES', 'MANUFACTURING_BOM',
  'Assembly & Test', '조립·시험·패키징', '위탁생산', '엔비디아', None, None, 'ACTIVE',
  'CONFIRMED', 'SUBSYSTEM_MODULE', None, ['nv_sup_004'],
  '10-K 가 이름을 적은 하청업체다. 개별 물량 비중은 비공개(04의 R006)'),
 ('nv-wistron-cm', 'wistron', NV, 'CONTRACT_MANUFACTURES', 'MANUFACTURING_BOM',
  'Assembly & Test', '조립·시험·패키징', '위탁생산', '엔비디아', None, None, 'ACTIVE',
  'CONFIRMED', 'SUBSYSTEM_MODULE', None, ['nv_sup_004'],
  '10-K 가 이름을 적은 하청업체다. 개별 물량 비중은 비공개(04의 R007)'),
 ('nv-fabrinet-cm', 'fabrinet', NV, 'CONTRACT_MANUFACTURES', 'MANUFACTURING_BOM',
  'Assembly & Test', '조립·시험·패키징', '위탁생산', '엔비디아', None, None, 'ACTIVE',
  'CONFIRMED', 'SUBSYSTEM_MODULE', None, ['nv_sup_004'],
  '10-K 가 이름을 적은 하청업체다. 개별 물량 비중은 비공개(04의 R008)'),
 ('nv-coherent-capacity', 'coherent', NV, 'SUPPLIES', 'MANUFACTURING_BOM', 'Optics',
  '고급 레이저·광네트워킹 부품', '광통신 공급사', '엔비디아', '2026-03-02', None, 'ACTIVE',
  'CONFIRMED', 'COMPONENT_SUPPLIER', None, ['nv_opt_001'],
  '다중 십억 달러 구매 약정과 미래 용량권이다. 확정 물량은 아니다(SUPPLIES_CAPACITY, 04의 '
  'R009)'),
 ('nv-lumentum-capacity', 'lumentum', NV, 'SUPPLIES', 'MANUFACTURING_BOM', 'Optics',
  '고급 레이저 부품', '광통신 공급사', '엔비디아', '2026-03-02', None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['nv_opt_002'],
  '다중 십억 달러 구매 약정과 미래 용량권이다. 확정 물량은 아니다(SUPPLIES_CAPACITY, 04의 '
  'R011)'),
 ('nv-skhynix-partner', 'sk-hynix', NV, 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Memory',
  '차세대 AI 메모리 공동개발', '전략 파트너', '엔비디아', '2026-07-24', None, 'ACTIVE',
  'CONFIRMED', None, None, ['nv_skh_001'],
  '일반 메모리 공급 관계(nv-skhynix-memory)와는 별도의 전략적 공동개발 관계다(04의 R021)'),
 # ── 다운스트림·구조 파트너십(R010·R012~R020·R022~R023) — lane CORPORATE ──
 ('nv-coherent-invest', NV, 'coherent', 'INVESTS_IN', 'CORPORATE', 'Corporate', '지분투자',
  '투자자', '피투자사', '2026-03-02', None, 'ACTIVE', 'CONFIRMED', None, None, ['nv_opt_001'],
  '20억 달러(04의 R010)'),
 ('nv-lumentum-invest', NV, 'lumentum', 'INVESTS_IN', 'CORPORATE', 'Corporate', '지분투자',
  '투자자', '피투자사', '2026-03-02', None, 'ACTIVE', 'CONFIRMED', None, None, ['nv_opt_002'],
  '20억 달러(04의 R012)'),
 ('nv-coreweave-partner', NV, 'coreweave', 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  '전략적 협력', '엔비디아', '전략 파트너', '2026-01-26', '2030-12-31', 'ACTIVE', 'CONFIRMED',
  None, None, ['nv_down_002'], '2030년까지 AI 팩토리·Rubin·CPU·스토리지에 걸쳐 5GW 넘는 '
  '협력(04의 R013)'),
 ('nv-coreweave-invest', NV, 'coreweave', 'INVESTS_IN', 'CORPORATE', 'Corporate', '지분투자',
  '투자자', '피투자사', '2026', None, 'ACTIVE', 'CONFIRMED', None, None, ['nv_down_002'],
  '20억 달러(04의 R014)'),
 ('nv-nebius-partner', NV, 'nebius', 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  '전략적 협력', '엔비디아', '전략 파트너', '2026-03-11', '2030-12-31', 'ACTIVE', 'CONFIRMED',
  None, None, ['nv_down_003'], '2030년까지 풀스택 AI 클라우드·AI 팩토리에 걸쳐 5GW 넘는 '
  '협력(04의 R015)'),
 ('nv-nebius-invest', NV, 'nebius', 'INVESTS_IN', 'CORPORATE', 'Corporate', '지분투자',
  '투자자', '피투자사', '2026', None, 'ACTIVE', 'CONFIRMED', None, None, ['nv_down_003'],
  '20억 달러(04의 R016)'),
 ('nv-aws-partner', NV, 'aws', 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  'GPU·Vera·NVLink Fusion·NVHBM', '엔비디아', '전략 파트너', '2026-08-26', '2028-12-31',
  'ACTIVE', 'CONFIRMED', None, None, ['nv_down_001'],
  '2027~2028년 GPU 200만 개 추가 계획. 익명 고객 집중도 수치와 매핑하지 않는다(04의 R017)'),
 ('nv-openai-partner', NV, 'openai', 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  'NVIDIA 시스템·Rubin', '엔비디아', '전략 파트너', '2025-09-22', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['nv_down_004'],
  '최소 10GW 규모 시스템 구매 의향서(LOI). SEC 상 직접 고객으로 표기되지 않는다(04의 R018)'),
 ('nv-ssi-partner', NV, 'ssi', 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  'Rubin 연산 접근권', '엔비디아', '전략 파트너', '2026-07-27', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['nv_down_005'], '투자가 존재하나 금액은 이 원장에 없다(04의 R019)'),
 ('nv-spacexai-adopt', NV, 'spacexai', 'PLATFORM_EXPOSURE', 'CORPORATE', 'Corporate',
  'Vera CPU·Vera Rubin', '엔비디아', '플랫폼 채택자', '2026-08-24', None, 'ACTIVE',
  'CONFIRMED', None, None, ['nv_down_006'],
  '채택 사실만 확인되고 회계상 직접 고객 지위는 주장되지 않는다(PLATFORM_ADOPTION, 04의 '
  'R020)'),
 ('nv-marvell-adopt', 'marvell', NV, 'PLATFORM_EXPOSURE', 'CORPORATE', 'Corporate',
  '커스텀 XPU·스케일업 네트워킹', '커스텀 실리콘 파트너', '엔비디아', '2026', None, 'ACTIVE',
  'CONFIRMED', None, None, ['nv_arch_001'],
  'NVLink Fusion 생태계 파트너. 엔비디아도 20억 달러를 투자했다고 원장에 적혀 있으나 별도 '
  '투자 관계 행은 04에 없다(PLATFORM_ADOPTION, 04의 R022)'),
 ('nv-mediatek-adopt', 'mediatek', NV, 'PLATFORM_EXPOSURE', 'CORPORATE', 'Corporate',
  '커스텀 XPU 설계 기반', '커스텀 실리콘 파트너', '엔비디아', '2026', None, 'ACTIVE',
  'CONFIRMED', None, None, ['nv_arch_001'],
  '랙 스케일 세미커스텀 아키텍처 파트너다(PLATFORM_ADOPTION, 04의 R023)'),
]

# ── 매출원 갈림목 — REVENUE_FROM 스캐폴드. vc_norm 이 분류로 접으며 이 관계 행은
#    사라지고 관측은 classifications.json 의 shares 로 옮겨간다(태양유전 사슬과 같은 자리) ──
REV_R = [
 ('nv-rev-datacenter-edge', 'nv-rev-datacenter', '데이터센터', ['nv_fin_001', 'nv_fin_003']),
 ('nv-rev-gaming-edge', 'nv-rev-gaming', '게이밍', ['nv_fin_003']),
 ('nv-rev-proviz-edge', 'nv-rev-proviz', '프로페셔널 시각화', ['nv_fin_003']),
 ('nv-rev-automotive-edge', 'nv-rev-automotive', '자동차', ['nv_fin_003']),
 ('nv-rev-oem-other-edge', 'nv-rev-oem-other', 'OEM·기타', ['nv_fin_003']),
 ('nv-rev-hyperscale-edge', 'nv-rev-hyperscale', '하이퍼스케일', ['nv_fin_002']),
 ('nv-rev-acie-edge', 'nv-rev-acie', 'ACIE', ['nv_fin_002']),
 ('nv-rev-edge-computing-edge', 'nv-rev-edge-computing', '엣지 컴퓨팅', ['nv_fin_002']),
]
for _rid, _tgt, _label, _srcs in REV_R:
    R.append((_rid, NV, _tgt, 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type', _label,
              '엔비디아', '매출원', None, None, 'ACTIVE', 'CONFIRMED', None, 'REVENUE_TYPE',
              _srcs, None))

# ── 관측 — REV001~021. 04 Observations 탭(OBS)과 달리 REV 는 revenue_mix_id 를 가진
#    매출원 비중이라 그대로 관측으로 옮긴다(태양유전 사슬과 같은 자리) ──
PCT, USDM = 'percent', 'USD M'
TOTAL_REV_KO = {
 'FY2024': 'NVIDIA FY2024 총매출 609억 2,200만 달러',
 'FY2025': 'NVIDIA FY2025 총매출 1,304억 9,700만 달러',
 'FY2026': 'NVIDIA FY2026 총매출 2,159억 3,800만 달러',
 'Q2 FY2027': 'NVIDIA 2027 회계연도 2분기 총매출 962억 2,100만 달러',
 'H1 FY2027': 'NVIDIA 2027 회계연도 상반기 총매출 1,778억 3,700만 달러',
}
FY24 = ('FY2024', '2023-01-30', '2024-01-28')
FY25 = ('FY2025', '2024-01-29', '2025-01-26')
FY26 = ('FY2026', '2025-01-27', '2026-01-25')
Q2FY27 = ('Q2 FY2027', '2026-04-27', '2026-07-26')
H1FY27 = ('H1 FY2027', '2026-01-26', '2026-07-26')
LEGACY_SRC = ['nv_fin_003']
FY26_SRC = ['nv_fin_001', 'nv_fin_003']
RECAST_SRC = ['nv_fin_002']

# (revtype, metric_key, period_tuple, amount_m, pct, sources, status)
REV_ROWS = [
 ('nv-rev-datacenter-edge', 'data_center_revenue_share', FY24, 47525, 78.01, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-gaming-edge', 'gaming_revenue_share', FY24, 10447, 17.15, LEGACY_SRC, 'HISTORICAL'),
 ('nv-rev-proviz-edge', 'proviz_revenue_share', FY24, 1553, 2.55, LEGACY_SRC, 'HISTORICAL'),
 ('nv-rev-automotive-edge', 'automotive_revenue_share', FY24, 1091, 1.79, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-oem-other-edge', 'oem_other_revenue_share', FY24, 306, 0.50, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-datacenter-edge', 'data_center_revenue_share', FY25, 115186, 88.27, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-gaming-edge', 'gaming_revenue_share', FY25, 11350, 8.70, LEGACY_SRC, 'HISTORICAL'),
 ('nv-rev-proviz-edge', 'proviz_revenue_share', FY25, 1878, 1.44, LEGACY_SRC, 'HISTORICAL'),
 ('nv-rev-automotive-edge', 'automotive_revenue_share', FY25, 1694, 1.30, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-oem-other-edge', 'oem_other_revenue_share', FY25, 389, 0.30, LEGACY_SRC,
  'HISTORICAL'),
 ('nv-rev-datacenter-edge', 'data_center_revenue_share', FY26, 193737, 89.72, FY26_SRC,
  'CURRENT'),
 ('nv-rev-gaming-edge', 'gaming_revenue_share', FY26, 16042, 7.43, FY26_SRC, 'CURRENT'),
 ('nv-rev-proviz-edge', 'proviz_revenue_share', FY26, 3191, 1.48, FY26_SRC, 'CURRENT'),
 ('nv-rev-automotive-edge', 'automotive_revenue_share', FY26, 2349, 1.09, FY26_SRC, 'CURRENT'),
 ('nv-rev-oem-other-edge', 'oem_other_revenue_share', FY26, 619, 0.29, FY26_SRC, 'CURRENT'),
 ('nv-rev-hyperscale-edge', 'hyperscale_revenue_share', Q2FY27, 48710, 50.62, RECAST_SRC,
  'CURRENT'),
 ('nv-rev-acie-edge', 'acie_revenue_share', Q2FY27, 40313, 41.90, RECAST_SRC, 'CURRENT'),
 ('nv-rev-edge-computing-edge', 'edge_computing_revenue_share', Q2FY27, 7198, 7.48,
  RECAST_SRC, 'CURRENT'),
 ('nv-rev-hyperscale-edge', 'hyperscale_revenue_share', H1FY27, 91761, 51.60, RECAST_SRC,
  'CURRENT'),
 ('nv-rev-acie-edge', 'acie_revenue_share', H1FY27, 72508, 40.77, RECAST_SRC, 'CURRENT'),
 ('nv-rev-edge-computing-edge', 'edge_computing_revenue_share', H1FY27, 13568, 7.63,
  RECAST_SRC, 'CURRENT'),
]

O = []
for _rel, _metric, _per, _amt, _pct, _srcs, _status in REV_ROWS:
    _period, _pstart, _pend = _per
    O.append(('o-%s-%s-pct' % (_rel, _period.replace(' ', '')), _rel, _metric, _pct, None,
               None, PCT, _period, _pstart, _pend, _pend, 'NVIDIA 총매출', _status,
               'CONFIRMED', 1.0, None, _srcs))
    O.append(('o-%s-%s-amt' % (_rel, _period.replace(' ', '')), _rel,
               _metric.replace('_share', '_amount'), _amt, None, None, USDM, _period, _pstart,
               _pend, _pend, TOTAL_REV_KO[_period], _status, 'CONFIRMED', 1.0, None, _srcs))

# ── 주장 — 04 Observations 탭(OBS001~011, 전사 절대값이라 관계가 없다) + 서술적 맥락 ──
CLAIMS = [
 ('clm-nv-cust-fy2024-direct', 'FY2024(2024년 1월 28일 마감)에는 직접고객 한 곳이 총매출의 '
  '13%를 차지했다.', NV, None, 'FY2024', 'CONFIRMED', 1.0, ['nv_obs_ledger'],
  '실명은 비공개다(04의 OBS001)'),
 ('clm-nv-cust-fy2024-indirect', '같은 기간 회사는 별도로 간접고객 한 곳의 몫을 총매출의 약 '
  '19%로 추정했다. 직접고객 수치와 합쳐서 보지 않는다.', NV, None, 'FY2024', 'ESTIMATED', 1.0,
  ['nv_obs_ledger'], '주문·채널 자료를 바탕으로 한 회사 자체 추정치다(04의 OBS002)'),
 ('clm-nv-cust-fy2025', 'FY2025(2025년 1월 26일 마감)에는 직접고객 세 곳이 각각 총매출의 '
  '12%·11%·11%를 차지했다.', NV, None, 'FY2025', 'CONFIRMED', 1.0, ['nv_obs_ledger'],
  '실명은 비공개다(04의 OBS003)'),
 ('clm-nv-cust-fy2026', 'FY2026(2026년 1월 25일 마감)에는 직접고객 두 곳이 각각 총매출의 '
  '22%·14%를 차지했다.', NV, None, 'FY2026', 'CONFIRMED', 1.0, ['nv_obs_ledger'],
  '실명은 비공개다(04의 OBS004)'),
 ('clm-nv-cust-q1fy2027', 'Q1 FY2027(2026년 4월 26일 마감)에는 직접고객 세 곳이 각각 '
  '21%·17%·16%를 차지했다.', NV, None, 'Q1 FY2027', 'CONFIRMED', 1.0, ['nv_cust_002'],
  '실명은 비공개다(04의 OBS005)'),
 ('clm-nv-cust-q2fy2027-top1', 'Q2 FY2027(2026년 7월 26일 마감)에는 직접고객 한 곳이 '
  '총매출의 16%를 넘겼다.', NV, None, 'Q2 FY2027', 'CONFIRMED', 1.0, ['nv_cust_001'],
  '실명은 비공개다(04의 OBS006)'),
 ('clm-nv-cust-h1fy2027', 'H1 FY2027 누계 기준으로는 직접고객 세 곳이 각각 16%·15%·13%를 '
  '차지했다.', NV, None, 'H1 FY2027', 'CONFIRMED', 1.0, ['nv_cust_001'],
  '실명은 비공개다(04의 OBS007)'),
 ('clm-nv-ar-concentration', '2026년 7월 26일 기준 매출채권 잔액의 22%·14%·13%·11%·10%를 '
  '직접고객 다섯 곳이 차지했다.', NV, None, '2026-07-26', 'CONFIRMED', 1.0, ['nv_cust_003'],
  '분모가 매출채권 잔액이라 매출 비중과는 다르다(04의 OBS008)'),
 ('clm-nv-dc-large-cloud', 'Q4 FY2024(2024년 1월 28일 마감) 기준 대형 클라우드 제공자가 '
  '데이터센터 매출의 50%를 웃돌았다.', NV, None, 'Q4 FY2024', 'CONFIRMED', 1.0,
  ['nv_obs_ledger'], '분모는 회사 총매출이 아니라 데이터센터 부문 매출이다(04의 OBS009)'),
 ('clm-nv-dc-inference-share', 'FY2024 데이터센터 매출 가운데 AI 추론이 차지하는 몫을 회사는 '
  '약 40%로 추정했다.', NV, None, 'FY2024', 'ESTIMATED', 1.0, ['nv_obs_ledger'],
  '분모는 데이터센터 부문 매출이다(04의 OBS010)'),
 ('clm-nv-dc-csp-share', 'Q2 FY2025(2024년 7월 28일 마감) 기준 CSP(클라우드서비스제공사)가 '
  '데이터센터 매출의 약 45%를 차지했다.', NV, None, 'Q2 FY2025', 'CONFIRMED', 1.0,
  ['nv_obs_ledger'], '옛 전방시장 구분 기준이라 지금 표시와 그대로 잇지 않는다(04의 OBS011)'),
 ('clm-nv-revenue-fy2026', 'FY2026(2026년 1월 25일 마감) 총매출은 2,159억 3,800만 달러이고 '
  '데이터센터 부문이 1,937억 3,700만 달러(89.7%)다.', NV, None, 'FY2026', 'CONFIRMED', 1.0,
  ['nv_fin_001'], None),
 ('clm-nv-revenue-history', 'FY2024 총매출 609억 2,200만 달러에서 FY2025 1,304억 9,700만 '
  '달러, FY2026 2,159억 3,800만 달러로 늘었고 그 사이 데이터센터 비중은 78.0%→88.3%→89.7%로 '
  '올라갔다.', NV, None, 'FY2024~FY2026', 'CONFIRMED', 1.0, ['nv_fin_003'], None),
 ('clm-nv-q2fy2027-mix', '2027 회계연도 2분기(2026년 7월 26일 마감) 총매출 962억 2,100만 '
  '달러 가운데 데이터센터 890억 2,300만 달러는 하이퍼스케일 487억 1,000만 달러와 ACIE 403억 '
  '1,300만 달러로 나뉘고, 엣지 컴퓨팅이 71억 9,800만 달러다.', NV, None, 'Q2 FY2027',
  'CONFIRMED', 1.0, ['nv_fin_002'],
  '2027 회계연도 1분기부터 시장·플랫폼 구분으로 표시 방식이 바뀌었다'),
 ('clm-nv-rubin-ecosystem', 'Rubin 생태계의 웨이퍼·칩 파트너로 TSMC·SPIL·Kinsus·KYEC·'
  '유니마이크론이, 제조·시스템 리더로 폭스콘·페가트론·QCT·위스트론·인벤텍이 공식적으로 '
  '이름을 올렸다.', NV, None, '2026', 'CONFIRMED', 1.0, ['nv_rub_001', 'nv_rub_002'],
  '생태계 역할일 뿐 공급사 사이의 정확한 상거래선은 별도로 확인되지 않는 한 잇지 않는다'),
 ('clm-nv-hbm4-estimate', 'Rubin 의 HBM4 는 SK하이닉스·마이크론·삼성전자 세 공급사 생태계로 '
  '거론되나 엔비디아 몫별 정확한 배분은 공개되지 않는다.', NV, None, '2026', 'ESTIMATED', 0.6,
  ['nv_hbm_001'], 'TrendForce 등 제3자 추정치이며 검증 일정이 바뀌면서 수치가 해가 가는 동안 '
  '달라졌다'),
 ('clm-nv-nvlink-fusion', 'NVLink Fusion 은 마벨·미디어텍 등 제3자 커스텀 XPU·CPU 를 엔비디아 '
  '랙 스케일 AI 팩토리 아키텍처에 붙이는 규격이다.', NV, None, '2025~2026', 'CONFIRMED', 1.0,
  ['nv_arch_001'], None),
 ('clm-nv-stx', 'BlueField-4 STX/CMX 는 AI 네이티브 컨텍스트·KV 캐시 스토리지 레인이다.', NV,
  None, '2026', 'CONFIRMED', 1.0, ['nv_stx_001'], '채택이 곧 회계상 직접 고객을 뜻하지 않는다'),
 ('clm-nv-dsx', 'DSX AI 팩토리 참조 설계에 Eaton·Schneider·Siemens·Trane·Vertiv·Jacobs·'
  'Switch 등이 참여한다.', NV, None, '2026', 'CONFIRMED', 1.0, ['nv_dsx_001'],
  '부지 인프라·참조설계 레인이지 엔비디아 제품 BOM 이 아니다'),
 ('clm-nv-taxonomy-recast', 'FY2024~FY2026 공시는 데이터센터·게이밍·프로페셔널 시각화·자동차·'
  'OEM 으로 나눈 "전방시장별 매출"을, FY2027 2분기부터는 하이퍼스케일·ACIE·엣지 컴퓨팅으로 '
  '나눈 "시장·플랫폼별 매출"을 쓴다. 2분기에 한 회사를 ACIE 에서 하이퍼스케일로 재분류하며 '
  '이전 기간도 다시 표시했다.', NV, None, 'FY2024~2027 Q2', 'CONFIRMED', 1.0,
  ['nv_rev_recast_001', 'nv_sem_001'], '구분 자체는 실명 고객 귀속의 근거가 아니다'),
 ('clm-nv-revenue-map-nomap', '매출 구분·시장 플랫폼별 실명 고객 귀속은 어느 기간도 공개되지 '
  '않는다. AWS·코어위브·네비우스·오픈AI 등 이름이 공개된 전략 파트너·투자·플랫폼 채택 관계는 '
  '그래프에 실제 관계로 남기되, 그 회사를 하이퍼스케일·ACIE 등 매출 구분으로 승격하지 '
  '않는다.', NV, None, 'FY2024~2027 Q2', 'CONFIRMED', 1.0, ['nv_map_001'],
  '01 §9 의 공시 경계와 같은 자리다'),
]


def ent(t):
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
            'legal_name': t[1], 'display_name': t[2] or t[1],
            'region': REGION.get(t[4]) if t[4] else None, 'parent_entity_id': None,
            'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
            'country': t[4], 'categories': t[5], 'desc': t[6], 'anon': False}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-12', 'note': t[6]}


def rel(t):
    return {'id': t[0], 'source_entity': t[1], 'target_entity': t[2],
            'relationship_type': t[3], 'lane': t[4], 'subsystem': t[5], 'component': t[6],
            'source_role': t[7], 'target_role': t[8], 'valid_from': t[9], 'valid_to': t[10],
            'status': t[11], 'evidence_level': t[12],
            'source_tier': t[13], 'target_tier': t[14],
            'economic_importance': None, 'capacity_criticality': None,
            'integration_criticality': None,
            'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium',
                                'INFERRED': 'high'}.get(t[12], 'low'),
            'flows': [], 'source_ids': t[15], 'notes': t[16]}


SRC_DATE = dict((x[0], x[4]) for x in SOURCES)


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': None, 'method_note': t[15],
            'source_ids': t[16], 'denominator_scope': 'FOCAL_TOTAL_REVENUE',
            'source_date': SRC_DATE.get((t[16] or [None])[0]) or t[10]}


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


def evidence():
    out, n = [], 0
    for t in R:
        for sid in t[15]:
            n += 1
            out.append({'id': 'nv-e%03d' % n, 'relationship_id': t[0], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if t[12] == 'CONFIRMED' else 'indirect',
                        'evidence': t[16] or '', 'hypothesis_id': None})
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'nv-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid, 'evidence_type': 'direct',
                        'evidence': t[15] or '', 'hypothesis_id': None})
    return out


def dump(path, o):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(o, ensure_ascii=False, indent=1))
        f.write(u'\n')


def merge(name, rows, key='id'):
    u"""이 스크립트가 맡은 항목은 덮어쓴다. 남의 항목은 건드리지 않는다."""
    p = os.path.join(DATA, name)
    cur = json.load(io.open(p, encoding='utf-8'))
    mine = dict((r[key], r) for r in rows)
    out = [mine.pop(x[key], x) for x in cur]
    out += [mine[k] for k in mine]
    dump(p, out)
    return len(out)


# RCM001~021 은 전부 UNALLOCATED_CUSTOMER 버킷이다 — 04 에 실명 매핑이 하나도 없다.
# 매출원마다 residual 만 적는다(revenue_type_map 은 없음). RCM id 는 04 RevenueCustomerMap
# 탭의 번호 그대로 옮긴다
RESIDUAL = {
 'rt-nv-rev-datacenter': (['nv_fin_001'], 'RCM001·006·011(FY2024~FY2026). 이름이 공개된 '
   '고객으로 배분된 몫은 없다'),
 'rt-nv-rev-gaming': (['nv_fin_003'], 'RCM002·007·012(FY2024~FY2026). 이름이 공개된 고객으로 '
   '배분된 몫은 없다'),
 'rt-nv-rev-proviz': (['nv_fin_003'], 'RCM003·008·013(FY2024~FY2026). 이름이 공개된 고객으로 '
   '배분된 몫은 없다'),
 'rt-nv-rev-automotive': (['nv_fin_003'], 'RCM004·009·014(FY2024~FY2026). 이름이 공개된 '
   '고객으로 배분된 몫은 없다'),
 'rt-nv-rev-oem-other': (['nv_fin_003'], 'RCM005·010·015(FY2024~FY2026). 이름이 공개된 '
   '고객으로 배분된 몫은 없다'),
 'rt-nv-rev-hyperscale': (['nv_fin_002'], 'RCM016·019(Q2·H1 FY2027). AWS·Azure·GCP·OCI 로 '
   '배분한 근거는 없다'),
 'rt-nv-rev-acie': (['nv_fin_002'], 'RCM017·020(Q2·H1 FY2027). 코어위브·네비우스·람다 등으로 '
   '배분한 근거는 없다'),
 'rt-nv-rev-edge-computing': (['nv_fin_002'], 'RCM018·021(Q2·H1 FY2027). 이름이 공개된 '
   '고객으로 배분된 몫은 없다'),
}


def apply_recast():
    u"""vc_norm 이 옮긴 v2 classifications.json 위에 04 RevenueCustomerMap 의 residual 을
    얹는다. 04 에는 실명 매핑이 하나도 없어 revenue_type_map 은 만들지 않는다. 멱등."""
    cp = os.path.join(CHAIN, 'classifications.json')
    cls = json.load(io.open(cp, encoding='utf-8'))
    # 두 분류 체계 — FY2027 부터 시장 플랫폼(하이퍼스케일·ACIE·엣지)으로 다시 갈랐다. 옛 체계
    # (데이터센터·게이밍…)와 한 줄에 서면 합이 100 을 넘는 것처럼 읽히니 무리로 가른다
    RECAST = {'rt-nv-rev-hyperscale', 'rt-nv-rev-acie', 'rt-nv-rev-edge-computing'}
    for x in cls['revenue_types']:
        if x.get('unallocated'):
            continue
        if x['id'] in RECAST:
            x['group_rank'], x['group_label'] = 0, u'FY2027 재분류 · 시장 플랫폼'
        else:
            x['group_rank'], x['group_label'] = 1, u'FY2026 이전 분류'
        r = RESIDUAL.get(x['id'])
        if not r:
            continue
        srcs, note = r
        x['residual'] = {'status': 'UNDISCLOSED', 'label': u'배분 미상 잔여',
                         'source_ids': srcs + ['nv_map_001'], 'note': note}
    dump(cp, cls)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'chain.json'),
         {'id': 'nvidia', 'focal_entity': NV, 'label': u'엔비디아',
          'note': u'AI 가속기 회사 한 곳을 중심으로 세운 사슬. FY2026 10-K 와 2026-09-11 '
                  u'Drive 조사가 앵커다'})
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'hypotheses.json'), [])
    dump(os.path.join(CHAIN, 'projects.json'), [])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print(u'전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d · 주장 %d'
          % (ne, ns, len(R), len(O), len(CLAIMS)))

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
    apply_recast()
    import migrate_vc2
    migrate_vc2.main()
