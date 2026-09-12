# -*- coding: utf-8 -*-
"""반도체 기판 사슬 — 대덕전자.

Drive `value chain 분석/대덕전자` 의 01~05 가 canonical 이다. 거기 있는 것만 옮긴다.
  02_대덕전자 Value Chain        1NnKsHQAbnJoBppoUO4hYtuka3R7pi2uU-7sON_xnbQU
  03_대덕전자 Evidence & Sources  1fZjSuxpg03-Rvbwu712dkrWJ6GulhFGfkbqXhHiSA2U
  04_대덕전자 Entities & Edges    1Yb6yPbaMjhk6q8A3udUF4wztu2QzAPGRfCsWMZsdk8g

실명 고객·강한 2차근거 고객·익명 고객을 등급으로 가른다. 제품 정합성만 있는 후보
(브로드컴·마벨 등)는 노드로 만들지 않는다.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'kr-substrate')
DD = 'daeduck-electronics'

SOURCES = [
 ('dd_ar_fy2025', '대덕전자 / KRX KIND', 'FY2025 사업보고서', 'primary_official', '2026-03-18',
  'https://kind.krx.co.kr/', '매출·원재료 매입 구조·고객 집중도·생산능력'),
 ('dd_filing_1h2024', '대덕전자 / KRX KIND', '2024 반기보고서 주요 거래처', 'primary_official',
  '2024-08-14', 'https://kind.krx.co.kr/',
  '주요 거래처로 삼성전자·SK하이닉스·앰코테크놀로지코리아·스태츠칩팩코리아를 든다'),
 ('dd_ir_mix', '증권사 리서치', '메모리·비메모리·MLB 매출 구성', 'analyst_estimate',
  '2025-04-30',
  None, 'FY2024 메모리 패키지기판 비중'),
 ('dd_ir_fcbga_mix', '증권사 리서치', 'FC-BGA 전방 구성', 'analyst_estimate', '2026-01-30',
  None, '4Q2025 자동차 45 · 데이터센터 30 · 네트워크 25'),
 ('dd_ir_util', '증권사 리서치', '2026 가동률·증설', 'analyst_estimate', '2026-08-03', None,
  'FC-BGA 가동률 약 90%'),
 ('dd_product_page', '대덕전자', 'FC-BGA 제품 소개', 'primary_company', '2026',
  'https://www.daeduck.com/', 'FC-BGA 기술과 전방 산업'),
 ('dd_bk_amd', 'BusinessKorea', 'AMD AI 가속기 MLB 샘플 관계', 'reputable_media',
  '2025-04-11', None, '2024~2025 샘플 단계 보도. 03 의 SRC006'),
 ('zdnet_tesla_2026', 'ZDNet Korea', '테슬라 AI4 기판 공급망', 'reputable_media', '2026-05-06',
  None, '대덕전자가 AI4 자율주행용 FC-BGA 공급망에 포함됐다는 보도'),
 ('eugene_spacex_2026', '유진투자증권', '주간 경제·전략', 'analyst_estimate', '2026-06-15',
  None, 'MLB 안에서 스페이스X향 항공우주 물량이 는다'),
 ('dd_cisco_legacy', '업계 2차자료', '네트워크 PCB 과거 관계', 'industry_research', '2024',
  None, '시스코와의 과거 관계를 시사하나 현재 제품·비중은 확인되지 않는다'),
 ('dd_ir_800g', '증권사 리서치', '800G 스위치 MLB 신규 고객', 'analyst_estimate', '2026-03-06',
  None, '2025 2분기 신규 고객 확보와 물량 확대'),
 ('dd_ir_ssd_optical', '증권사 리서치', 'AI 데이터센터 컨트롤러·광모듈 FC-BGA',
  'analyst_estimate', '2026-03-19', None, '수요는 확인되나 고객 실명은 비공개'),
 ('dd_ir_pcie', '증권사 리서치', 'PCIe 스위치·대면적 FC-BGA 로드맵', 'analyst_estimate',
  '2026-06-10', None, '2026 하반기 이후. 고객 실명 비공개'),
 ('dd_ir_amd', '증권사 리서치', 'AMD AI 가속기 MLB 양산', 'analyst_estimate', '2025-06-10',
  None, 'AMD향 AI 가속기 MLB 양산과 Helios 연계'),
 ('dd_ir_mlb_forecast', '증권사 리서치', 'AI 가속기향 MLB 매출 전망', 'analyst_estimate',
  '2026-06-10', None, '2025E 350억 → 2026E 1,550억 → 2027E 3,300억'),
]

# (id, 이름, 한국어, 유형, 나라, 갈래, 메모)
ENTITIES = [
 (DD, 'Daeduck Electronics', '대덕전자', 'company', '한국', ['Substrate'],
  '적층·미세회로·레이저 비아·도금·빌드업·범프를 거쳐 패키지 기판을 만든다'),
 # 소재
 ('ccl-substrate', 'Copper clad laminate', '동박적층판(CCL)', 'material', None, ['Material'],
  'FY2025 원재료 매입의 62.2%'),
 ('prepreg', 'Prepreg', '프리프레그', 'material', None, ['Material'],
  'FY2025 원재료 매입의 26.0%'),
 ('abf-film', 'Ajinomoto build-up film', 'ABF 빌드업 필름', 'material', None, ['Material'],
  '매입 비중은 6.7%지만 FC-BGA 절연층의 핵심이라 전략 중요도가 가장 높다'),
 ('pgc-plating', 'Plating chemicals (PGC)', '도금 재료(PGC)', 'material', None, ['Material'],
  '부재료 매입의 42.2%. 미세회로·도금 품질과 직결된다'),
 # 소재 공급사
 ('ajinomoto-fine-techno', 'Ajinomoto Fine-Techno', '아지노모토 파인테크노', 'company', '일본',
  ['Material'], 'ABF 공급사'),
 ('lg-chem', 'LG Chem', 'LG화학', 'company', '한국', ['Material'], 'CCL·프리프레그 계열'),
 ('doosan-electronics', 'Doosan Electronics', '두산전자', 'company', '한국', ['Material'],
  'CCL·프리프레그 계열'),
 ('heesung-catalysts', 'Heesung Catalysts', '희성촉매', 'company', '한국', ['Material'],
  '도금 재료 계열'),
 # 매출원
 ('dd-rev-memory', 'Memory package substrate', '메모리 패키지기판', 'revenue_type', None,
  ['Revenue type'], 'CSP·FCBOC 계열'),
 ('dd-rev-fcbga', 'FC-BGA', 'FC-BGA', 'revenue_type', None, ['Revenue type'],
  '자동차에서 데이터센터·네트워크로 전방이 넓어지는 중'),
 ('dd-rev-mlb', 'High-layer MLB', '고다층 MLB', 'revenue_type', None, ['Revenue type'],
  'AI 가속기·스위치·항공우주'),
 ('dd-rev-unallocated', 'Unallocated / undisclosed', '배분 미상', 'revenue_type', None,
  ['Revenue type'], '공시가 고객을 익명으로만 밝힌 자리'),
 # 실명 고객
 ('samsung-electronics', 'Samsung Electronics', '삼성전자', 'company', '한국', ['Chip maker'],
  '공시가 주요 거래처로 든다. 제품별 매출은 비공개'),
 ('sk-hynix', 'SK hynix', 'SK하이닉스', 'company', '한국', ['Chip maker'],
  '주요 거래처이자 반복된 Best Partner 관계'),
 ('amkor-korea', 'Amkor Technology Korea', '앰코테크놀로지코리아', 'company', '한국', ['OSAT'],
  '2024 반기 공시 주요 거래처'),
 ('stats-chippac-korea', 'STATS ChipPAC Korea', '스태츠칩팩코리아', 'company', '한국', ['OSAT'],
  '2024 반기 공시 주요 거래처'),
 ('amd', 'AMD', 'AMD', 'company', '미국', ['Chip maker'],
  'AI 가속기향 MLB. 회사가 공시한 고객명은 아니다'),
 ('tesla', 'Tesla', '테슬라', 'company', '미국', ['Automotive'],
  'AI4 자율주행 FC-BGA 공급망 포함 보도'),
 ('spacex', 'SpaceX', '스페이스X', 'company', '미국', ['Aerospace'],
  '항공우주 MLB 물량 증가'),
 ('cisco', 'Cisco Systems', '시스코', 'company', '미국', ['Network'],
  '과거 네트워크 PCB 관계. 현재 제품·비중은 모른다'),
 # 후보 — 제품 정합성만 있고 공급 근거가 없어 엣지를 걸지 않는다 (04 의 ENT027·ENT028)
 ('broadcom', 'Broadcom', '브로드컴', 'company', '미국', ['Chip maker'],
  'PCIe 스위치·광·네트워크 제품이 겹친다. 대덕전자 공급 근거는 아직 없다'),
 ('marvell', 'Marvell', '마벨', 'company', '미국', ['Chip maker'],
  'SSD 컨트롤러·광 DSP 제품이 겹친다. 대덕전자 공급 근거는 아직 없다'),
 # 익명 고객
 ('dd-800g-cust-a', '800G Network Customer A', '800G 네트워크 고객 A', 'company', None,
  ['Network'], '2025 2분기 확보한 800G 스위치 신규 고객. 실명 비공개'),
 ('dd-ssd-cust-a', 'SSD Controller Customer A', 'SSD 컨트롤러 고객 A', 'company', None,
  ['Chip maker'], 'AI 데이터센터 컨트롤러향 FC-BGA. 실명 비공개'),
 ('dd-optical-cust-a', 'Optical Module Customer A', '광모듈 고객 A', 'company', None,
  ['Network'], '광모듈향 FC-BGA. 실명 비공개'),
 ('dd-pcie-cust-a', 'PCIe Switch Customer A', 'PCIe 스위치 고객 A', 'company', None,
  ['Chip maker'], '대면적 FC-BGA 로드맵. 실명 비공개'),
 ('dd-anon-1', 'Anonymous customer (A) FY2025', '익명 고객 (가)', 'company', None, [],
  'FY2025 총매출의 20.6%'),
 ('dd-anon-2', 'Anonymous customer (B) FY2025', '익명 고객 (나)', 'company', None, [],
  'FY2025 총매출의 16.2%'),
 ('dd-anon-3', 'Anonymous customer (C) FY2025', '익명 고객 (다)', 'company', None, [],
  'FY2025 총매출의 11.4%'),
 # 최종 전방
 ('app-ai-datacenter', 'AI data center', 'AI 데이터센터', 'application', None, ['Application'],
  None),
 ('app-automotive', 'Automotive / physical AI', '자동차·피지컬 AI', 'application', None,
  ['Application'], None),
 ('app-800g-network', '800G network', '800G 네트워크', 'application', None, ['Application'],
  None),
 ('app-aerospace', 'Satellite / defense', '위성·방산', 'application', None, ['Application'],
  None),
 ('app-server-mobile', 'Server / PC / mobile', '서버·PC·모바일', 'application', None,
  ['Application'], 'DDR5·GDDR7·LPDDR·NAND·SoCAMM 계열'),
]

# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence_level, src_tier, tgt_tier, sources, notes)
R = [
 # ── 업스트림 ─────────────────────────────────────────────────────
 ('ajinomoto-abf', 'ajinomoto-fine-techno', 'abf-film', 'MANUFACTURES', 'MANUFACTURING_BOM',
  'Material', 'ABF 빌드업 필름', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025', 'dd_product_page'],
  '공급 생태계가 좁고 인증 장벽이 높다'),
 ('lgchem-ccl', 'lg-chem', 'ccl-substrate', 'SUPPLIES', 'MANUFACTURING_BOM', 'Material',
  'CCL', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025'],
  '공급 생태계로 확인된다. 이 회사가 대덕전자 안에서 차지하는 몫은 공개되지 않았다'),
 ('lgchem-prepreg', 'lg-chem', 'prepreg', 'SUPPLIES', 'MANUFACTURING_BOM', 'Material',
  '프리프레그', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025'], None),
 ('doosan-ccl', 'doosan-electronics', 'ccl-substrate', 'SUPPLIES', 'MANUFACTURING_BOM',
  'Material', 'CCL', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025'], None),
 ('doosan-prepreg', 'doosan-electronics', 'prepreg', 'SUPPLIES', 'MANUFACTURING_BOM',
  'Material', '프리프레그', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025'], None),
 ('heesung-pgc', 'heesung-catalysts', 'pgc-plating', 'SUPPLIES', 'MANUFACTURING_BOM',
  'Material', '도금 재료', '소재 공급', '소재', None, None, 'ACTIVE', 'CONFIRMED',
  'RAW_MATERIAL', None, ['dd_ar_fy2025'], None),
 ('ccl-dd', 'ccl-substrate', DD, 'INPUT_TO', 'MANUFACTURING_BOM', 'Material', 'CCL',
  '소재', '기판 제조', None, None, 'ACTIVE', 'CONFIRMED', 'MATERIAL_PROCESSING', None,
  ['dd_ar_fy2025'], 'FY2025 원재료 매입 1,404억 원'),
 ('prepreg-dd', 'prepreg', DD, 'INPUT_TO', 'MANUFACTURING_BOM', 'Material', '프리프레그',
  '소재', '기판 제조', None, None, 'ACTIVE', 'CONFIRMED', 'MATERIAL_PROCESSING', None,
  ['dd_ar_fy2025'], 'FY2025 원재료 매입 587억 원'),
 ('abf-dd', 'abf-film', DD, 'INPUT_TO', 'MANUFACTURING_BOM', 'Material', 'ABF',
  '소재', '기판 제조', None, None, 'ACTIVE', 'CONFIRMED', 'MATERIAL_PROCESSING', None,
  ['dd_ar_fy2025'], 'FY2025 원재료 매입 151억 원. 금액은 작지만 FC-BGA 병목이다'),
 ('pgc-dd', 'pgc-plating', DD, 'INPUT_TO', 'MANUFACTURING_BOM', 'Material', '도금 재료',
  '소재', '기판 제조', None, None, 'ACTIVE', 'CONFIRMED', 'MATERIAL_PROCESSING', None,
  ['dd_ar_fy2025'], '부재료 매입의 42.2%'),
 # ── 다운스트림 1층: 매출원 ───────────────────────────────────────
 ('dd-rev-memory-edge', DD, 'dd-rev-memory', 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type',
  '메모리 패키지기판', '기판 제조', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['dd_ir_mix'], None),
 ('dd-rev-fcbga-edge', DD, 'dd-rev-fcbga', 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type',
  'FC-BGA', '기판 제조', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['dd_product_page'], None),
 ('dd-rev-mlb-edge', DD, 'dd-rev-mlb', 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type',
  '고다층 MLB', '기판 제조', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['dd_ir_mix'], None),
 ('dd-rev-unalloc-edge', DD, 'dd-rev-unallocated', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '매출원 배분이 공개되지 않은 몫', '기판 제조', '매출원', None, None,
  'ACTIVE', 'UNDISCLOSED', None, 'REVENUE_TYPE', ['dd_ar_fy2025'],
  '공시가 상위 고객을 익명으로만 밝힌다'),
 # ── 메모리 패키지기판 고객 ───────────────────────────────────────
 ('mem-samsung', 'dd-rev-memory', 'samsung-electronics', 'SELLS_TO', 'DOWNSTREAM',
  'Chip maker', '메모리 패키지기판', '매출원', '고객', '2024-06-30', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_filing_1h2024'],
  '2024 반기 공시가 이름을 든다. 매출원 안의 몫은 공개되지 않았다'),
 ('mem-hynix', 'dd-rev-memory', 'sk-hynix', 'SELLS_TO', 'DOWNSTREAM', 'Chip maker',
  '메모리 패키지기판', '매출원', '고객', '2024-06-30', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_filing_1h2024'], None),
 ('mem-amkor', 'dd-rev-memory', 'amkor-korea', 'SELLS_TO', 'DOWNSTREAM', 'OSAT',
  '패키지 기판', '매출원', '고객', '2024-06-30', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_filing_1h2024'], None),
 ('mem-stats', 'dd-rev-memory', 'stats-chippac-korea', 'SELLS_TO', 'DOWNSTREAM', 'OSAT',
  '패키지 기판', '매출원', '고객', '2024-06-30', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_filing_1h2024'], None),
 ('mem-app', 'samsung-electronics', 'app-server-mobile', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', 'DDR5·GDDR7·LPDDR·NAND·SoCAMM', '고객', '전방', None, None, 'ACTIVE',
  'ESTIMATED', None, 'END_USER', ['dd_ir_mix'], '메모리 기판이 실리는 자리'),
 # ── FC-BGA 고객 ─────────────────────────────────────────────────
 ('fcbga-tesla', 'dd-rev-fcbga', 'tesla', 'SELLS_TO', 'DOWNSTREAM', 'Automotive',
  'AI4 자율주행 FC-BGA', '매출원', '고객', '2025-10-01', None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['zdnet_tesla_2026'],
  '복수 업계 보도로 공급망 포함이 확인된다. 회사가 공시한 고객명은 아니다'),
 ('fcbga-ssd', 'dd-rev-fcbga', 'dd-ssd-cust-a', 'SELLS_TO', 'DOWNSTREAM', 'Chip maker',
  'AI 데이터센터 SSD 컨트롤러 FC-BGA', '매출원', '고객', '2025-10-01', None, 'ACTIVE',
  'CONFIRMED', None, 'CONTRACTUAL_CUSTOMER', ['dd_ir_ssd_optical'],
  'IR 가 거래와 물량 증가를 밝혔다. 비공개인 것은 상대 실명뿐이다'),
 ('fcbga-optical', 'dd-rev-fcbga', 'dd-optical-cust-a', 'SELLS_TO', 'DOWNSTREAM', 'Network',
  '광모듈 FC-BGA', '매출원', '고객', '2025-10-01', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_ir_ssd_optical'],
  'IR 가 거래를 밝혔다. 비공개인 것은 상대 실명뿐이다'),
 ('fcbga-pcie', 'dd-rev-fcbga', 'dd-pcie-cust-a', 'SELLS_TO', 'DOWNSTREAM', 'Chip maker',
  '대면적 PCIe 스위치 FC-BGA', '매출원', '고객', '2026-07-01', None, 'PLANNED', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_ir_pcie'],
  '2026 하반기 이후 로드맵. IR 가 밝힌 것은 계획이고 상대 실명은 비공개다'),
 ('fcbga-app-auto', 'tesla', 'app-automotive', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', '자율주행 프로세서', '고객', '전방', None, None, 'ACTIVE', 'ESTIMATED',
  None, 'END_USER', ['zdnet_tesla_2026'], None),
 ('fcbga-app-dc', 'dd-ssd-cust-a', 'app-ai-datacenter', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', 'AI 데이터센터 컨트롤러', '고객', '전방', None, None, 'ACTIVE', 'ESTIMATED',
  None, 'END_USER', ['dd_ir_ssd_optical'], None),
 # ── MLB 고객 ────────────────────────────────────────────────────
 ('mlb-amd', 'dd-rev-mlb', 'amd', 'SELLS_TO', 'DOWNSTREAM', 'Chip maker',
  'AI 가속기 MLB', '매출원', '고객', '2025-01-01', None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_ir_amd', 'dd_bk_amd'],
  '증권사 자료가 양산과 Helios 연계를 적는다. 회사 공시 고객명은 아니다'),
 ('mlb-spacex', 'dd-rev-mlb', 'spacex', 'SELLS_TO', 'DOWNSTREAM', 'Aerospace',
  '항공우주·위성 MLB', '매출원', '고객', '2026-01-01', None, 'ACTIVE', 'INFERRED',
  None, 'CONTRACTUAL_CUSTOMER', ['eugene_spacex_2026'], None),
 ('mlb-800g', 'dd-rev-mlb', 'dd-800g-cust-a', 'SELLS_TO', 'DOWNSTREAM', 'Network',
  '800G 스위치 MLB', '매출원', '고객', '2025-04-01', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['dd_ir_800g'],
  'IR 가 신규 고객 확보와 양산 진입을 밝혔다. 비공개인 것은 실명뿐이다'),
 ('mlb-cisco', 'dd-rev-mlb', 'cisco', 'SELLS_TO', 'DOWNSTREAM', 'Network',
  '네트워크 장비 PCB·MLB', '매출원', '고객', None, None, 'UNKNOWN',
  'HISTORICAL_CURRENT_UNKNOWN', None, 'CONTRACTUAL_CUSTOMER', ['dd_cisco_legacy'],
  '과거 관계를 시사하는 2차자료뿐이다. 800G 신규 고객과 같다는 근거는 없다'),
 ('mlb-app-ai', 'amd', 'app-ai-datacenter', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', 'AI 가속기', '고객', '전방', None, None, 'ACTIVE', 'ESTIMATED',
  None, 'END_USER', ['dd_ir_amd'], None),
 ('mlb-app-800g', 'dd-800g-cust-a', 'app-800g-network', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', '800G 스위치', '고객', '전방', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'END_USER', ['dd_ir_800g'], None),
 ('mlb-app-space', 'spacex', 'app-aerospace', 'END_USER_DEPLOYMENT', 'DOWNSTREAM',
  'Application', '위성·방산', '고객', '전방', None, None, 'ACTIVE', 'ESTIMATED',
  None, 'END_USER', ['eugene_spacex_2026'], None),
 # ── 익명 집중도 고객 ────────────────────────────────────────────
 ('unalloc-anon1', 'dd-rev-unallocated', 'dd-anon-1', 'SELLS_TO', 'DOWNSTREAM',
  'Undisclosed customer', None, '매출원', '계약상 고객', '2025-01-01', '2025-12-31',
  'UNKNOWN', 'UNDISCLOSED', None, 'CONTRACTUAL_CUSTOMER', ['dd_ar_fy2025'],
  '공시가 (가)로만 밝힌다. 삼성전자·SK하이닉스 등으로 임의 매핑하지 않는다'),
 ('unalloc-anon2', 'dd-rev-unallocated', 'dd-anon-2', 'SELLS_TO', 'DOWNSTREAM',
  'Undisclosed customer', None, '매출원', '계약상 고객', '2025-01-01', '2025-12-31',
  'UNKNOWN', 'UNDISCLOSED', None, 'CONTRACTUAL_CUSTOMER', ['dd_ar_fy2025'], None),
 ('unalloc-anon3', 'dd-rev-unallocated', 'dd-anon-3', 'SELLS_TO', 'DOWNSTREAM',
  'Undisclosed customer', None, '매출원', '계약상 고객', '2025-01-01', '2025-12-31',
  'UNKNOWN', 'UNDISCLOSED', None, 'CONTRACTUAL_CUSTOMER', ['dd_ar_fy2025'], None),
]

PCT = 'percent'
# (id, rel, metric, value, low, high, unit, period, p_start, p_end, as_of,
#  denominator, status, evidence_level, confidence, method_id, sources, note)
O = [
 ('o-dd-ccl-share', 'ccl-dd', 'purchase_share', 62.2, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 원재료 매입액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '1,404억 원'),
 ('o-dd-prepreg-share', 'prepreg-dd', 'purchase_share', 26.0, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 원재료 매입액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '587억 원'),
 ('o-dd-abf-share', 'abf-dd', 'purchase_share', 6.7, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 원재료 매입액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '151억 원. 매입 비중은 낮고 전략 중요도는 가장 높다'),
 ('o-dd-pgc-share', 'pgc-dd', 'purchase_share', 42.2, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 부재료 매입액', 'CURRENT', 'CONFIRMED',
  0.9, None, ['dd_ar_fy2025'], '852억 원. 분모가 원재료가 아니라 부재료다'),
 ('o-dd-memory-share-2024', 'dd-rev-memory-edge', 'revenue_type_share', 53.4, None, None,
  PCT, 'FY2024', '2024-01-01', '2024-12-31', '2024-12-31', '대덕전자 총매출', 'HISTORICAL',
  'ESTIMATED', 0.7, None, ['dd_ir_mix'], '약 4,764억 원. 회사 공식 분해가 아니다'),
 ('o-dd-fcbga-util', 'dd-rev-fcbga-edge', 'utilization', 90, None, None, PCT, '2026',
  '2026-01-01', '2026-12-31', '2026-08-03', 'FC-BGA 라인 가동률', 'CURRENT', 'ESTIMATED',
  0.6, None, ['dd_ir_util'], '전사 평균 가동률 76%를 FC-BGA 가동률로 읽지 않는다'),
 ('o-dd-anon1', 'unalloc-anon1', 'customer_revenue_share', 20.6, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 총매출', 'HISTORICAL', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '약 2,190억 원'),
 ('o-dd-anon2', 'unalloc-anon2', 'customer_revenue_share', 16.2, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 총매출', 'HISTORICAL', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '약 1,727억 원'),
 ('o-dd-anon3', 'unalloc-anon3', 'customer_revenue_share', 11.4, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-03-18', '대덕전자 총매출', 'HISTORICAL', 'CONFIRMED',
  1.0, None, ['dd_ar_fy2025'], '약 1,210억 원. 셋을 더하면 48.1%'),
 ('o-dd-fcbga-auto', 'fcbga-app-auto', 'application_mix', 45, None, None, PCT, '4Q2025',
  '2025-10-01', '2025-12-31', '2026-01-30', 'FC-BGA 전방 구성', 'HISTORICAL', 'ESTIMATED',
  0.6, None, ['dd_ir_fcbga_mix'], '자동차 45 · 데이터센터 30 · 네트워크 25'),
 ('o-dd-fcbga-dc', 'fcbga-app-dc', 'application_mix', 30, None, None, PCT, '4Q2025',
  '2025-10-01', '2025-12-31', '2026-01-30', 'FC-BGA 전방 구성', 'HISTORICAL', 'ESTIMATED',
  0.6, None, ['dd_ir_fcbga_mix'], None),
 ('o-dd-fcbga-net', 'dd-rev-fcbga-edge', 'application_mix', 25, None, None, PCT, '4Q2025',
  '2025-10-01', '2025-12-31', '2026-01-30', 'FC-BGA 전방 구성', 'HISTORICAL', 'ESTIMATED',
  0.6, None, ['dd_ir_fcbga_mix'],
  '네트워크 갈래. 고객별로 나눌 근거가 없어 FC-BGA 매출원에 건다. 03 의 CLM007'),
 ('o-dd-mlb-ai-2026', 'mlb-amd', 'segment_revenue_forecast', 155, None, None, 'KRW B',
  '2026E', '2026-01-01', '2026-12-31', '2026-06-10', 'AI 가속기향 MLB 매출 전망', 'CURRENT',
  'ESTIMATED', 0.5, None, ['dd_ir_mlb_forecast'],
  '2025E 35 → 2026E 155 → 2027E 330 (십억 원). 실적이 아니라 전망이다'),
]

CLAIMS = [
 ('clm-dd-rev-fy2025', '대덕전자의 FY2025 매출은 1조 650억 원이다.', DD, None, 'FY2025',
  'CONFIRMED', 1.0, ['dd_ar_fy2025'], None),
 ('clm-dd-material-mix',
  'FY2025 원재료 매입은 CCL 62.2%, 프리프레그 26.0%, ABF 6.7% 구조다.', DD, None, 'FY2025',
  'CONFIRMED', 1.0, ['dd_ar_fy2025'], 'CCL 과 프리프레그가 약 88%를 차지한다'),
 ('clm-dd-abf-critical',
  '매입액이 가장 큰 소재는 CCL 이지만 전략 중요도는 ABF 가 더 높다.', DD,
  'abf-film', '2026', 'ESTIMATED', 0.7, ['dd_ar_fy2025'],
  'FC-BGA 빌드업 절연층의 핵심이고 인증 장벽이 높다'),
 ('clm-dd-concentration',
  'FY2025 상위 익명 고객 셋이 총매출의 20.6%·16.2%·11.4%, 합계 48.1%를 차지한다.', DD,
  None, 'FY2025', 'CONFIRMED', 1.0, ['dd_ar_fy2025'],
  '이 셋을 삼성전자·SK하이닉스·AMD 등으로 임의 매핑하지 않는다'),
 ('clm-dd-named-customers',
  '공시로 이름이 확인되는 고객은 삼성전자·SK하이닉스·앰코테크놀로지코리아·스태츠칩팩코리아다.',
  DD, 'samsung-electronics', '1H2024', 'CONFIRMED', 1.0, ['dd_filing_1h2024'], None),
 ('clm-dd-amd', 'AMD 향 AI 가속기 MLB 양산이 증권사 자료에서 확인된다.', 'amd', DD,
  '2025-2026', 'INFERRED', 0.7, ['dd_ir_amd'], '회사가 공시한 고객명은 아니다'),
 ('clm-dd-tesla', '테슬라 AI4 자율주행 FC-BGA 공급망에 대덕전자가 포함됐다는 보도가 있다.',
  'tesla', DD, '2025-2026', 'INFERRED', 0.7, ['zdnet_tesla_2026'], None),
 ('clm-dd-spacex', '스페이스X 향 항공우주 MLB 물량이 늘고 있다.', 'spacex', DD, '2026',
  'INFERRED', 0.7, ['eugene_spacex_2026'], None),
 ('clm-dd-candidates',
  '브로드컴·마벨은 제품 정합성만 있고 직접 공급 근거가 없어 고객으로 넣지 않는다.', DD,
  None, '2026', 'INFERRED', 0.4, ['dd_ir_pcie'], '후보 메모로만 남긴다'),
 ('clm-dd-capacity',
  'FY2025 생산능력은 약 100.2만 제곱미터, 생산은 약 75.9만 제곱미터로 가동률 약 76%다.',
  DD, None, 'FY2025', 'CONFIRMED', 1.0, ['dd_ar_fy2025'],
  '제품별 편차가 커서 전사 평균을 FC-BGA 가동률로 읽으면 안 된다'),
]

REGION = {'한국': 'Korea', '일본': 'Japan', '대만': 'Taiwan', '중국': 'China',
          '미국': 'North America', '베트남': 'Vietnam'}


def ent(t):
    anon = t[0].startswith('dd-anon') or t[0].endswith('-cust-a')
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
            'legal_name': t[1], 'display_name': t[2] or t[1],
            'region': REGION.get(t[4]) if t[4] else None, 'parent_entity_id': None,
            'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
            'country': t[4], 'categories': t[5], 'desc': t[6], 'anon': anon}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-11', 'note': t[6]}


# 계약상 구매 주체라는 근거가 어디까지인지는 줄마다 다르다 (Drive 04 role_to).
# 공시가 이름을 든 넷만 확인이고, 보도·2차자료로 아는 쪽은 확인 전이다
CONTRACT_BY_ID = {
    'fcbga-tesla': 'UNVERIFIED', 'mlb-amd': 'UNVERIFIED', 'mlb-spacex': 'UNVERIFIED',
    'mlb-cisco': 'UNVERIFIED',
}


def rel(t):
    out = {'id': t[0], 'source_entity': t[1], 'target_entity': t[2],
           'relationship_type': t[3], 'lane': t[4], 'subsystem': t[5], 'component': t[6],
           'source_role': t[7], 'target_role': t[8], 'valid_from': t[9], 'valid_to': t[10],
           'status': t[11], 'evidence_level': t[12],
           'source_tier': t[13], 'target_tier': t[14],
           'economic_importance': None, 'capacity_criticality': None,
           'integration_criticality': None,
           'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium',
                               'INFERRED': 'high'}.get(t[12], 'low'),
           'flows': [], 'source_ids': t[15], 'notes': t[16]}
    if t[0] in CONTRACT_BY_ID:
        out['contractual_customer'] = CONTRACT_BY_ID[t[0]]
    return out


SRC_DATE = dict((x[0], x[4]) for x in SOURCES)


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': t[15], 'source_ids': t[16],
            'method_note': t[17],
            'denominator_scope': ('FOCAL_TOTAL_REVENUE'
                                  if t[2] == 'customer_revenue_share' else 'EDGE'),
            'source_date': SRC_DATE.get((t[16] or [None])[0]) or t[10]}


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


def dump(path, o):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(o, ensure_ascii=False, indent=1))
        f.write(u'\n')


def merge(name, rows, key='id'):
    """이 스크립트가 맡은 항목은 덮어쓴다. 남의 항목은 건드리지 않는다."""
    p = os.path.join(DATA, name)
    cur = json.load(io.open(p, encoding='utf-8'))
    mine = dict((r[key], r) for r in rows)
    out = [mine.pop(x[key], x) for x in cur]
    out += [mine[k] for k in mine]
    dump(p, out)
    return len(out)


def evidence():
    out, n = [], 0
    for t in R:
        for sid in t[15]:
            n += 1
            out.append({'id': 'kr-e%03d' % n, 'relationship_id': t[0], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if t[12] == 'CONFIRMED' else 'indirect',
                        'evidence': t[16] or '', 'hypothesis_id': None})
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'kr-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid, 'evidence_type': 'direct',
                        'evidence': t[17] or '', 'hypothesis_id': None})
    return out


# 04 Observations OBS001~OBS004 — 공급원별 매입 비중. 분모가 둘이다(원재료 매입액 셋,
# 부재료 매입액 하나). 띠는 분모가 같은 셋만 숫자로 적고 PGC 는 손 얹었을 때만 보인다
SS_SHARES = [
 ('ss-ccl-substrate', 62.2, u'FY2025 원재료 매입액', u'OBS001'),
 ('ss-prepreg', 26.0, u'FY2025 원재료 매입액', u'OBS002'),
 ('ss-abf-film', 6.7, u'FY2025 원재료 매입액', u'OBS003'),
 ('ss-pgc-plating', 42.2, u'FY2025 부재료 매입액', u'OBS004'),
]


def apply_supply_shares():
    u"""vc_norm 이 옮긴 분류 위에 공급원 매입 비중을 얹는다. 멱등."""
    cp = os.path.join(CHAIN, 'classifications.json')
    cls = json.load(io.open(cp, encoding='utf-8'))
    by = dict((x['id'], x) for x in cls['supply_sources'])
    for sid, v, den, obsid in SS_SHARES:
        x = by.get(sid)
        if not x:
            continue
        row = {'metric': 'purchase_share', 'value': v, 'value_low': None, 'value_high': None,
               'unit': 'percent', 'period': 'FY2025', 'period_start': '2025-01-01',
               'period_end': '2025-12-31', 'as_of_date': '2025-12-31', 'denominator': den,
               'evidence_level': 'CONFIRMED', 'confidence': None,
               'method_note': u'04 의 %s' % obsid, 'source_ids': ['dd_ar_fy2025'],
               'source_date': '2026-03-18'}
        x['shares'] = [s for s in x.get('shares') or []
                       if not (s.get('metric') == 'purchase_share'
                               and s.get('period') == 'FY2025')] + [row]
        if 'dd_ar_fy2025' not in x.get('source_ids', []):
            x.setdefault('source_ids', []).append('dd_ar_fy2025')
    dump(cp, cls)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'chain.json'),
         {'id': 'kr-substrate', 'focal_entity': DD, 'label': '반도체 기판',
          'note': '패키지 기판 제조사 한 곳을 중심으로 세운 사슬'})
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'hypotheses.json'), [])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print('전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d · 주장 %d'
          % (ne, ns, len(R), len(O), len(CLAIMS)))

    # 재료를 다시 쌓았으면 v2 꼴로 바로 옮긴다 — 옮기는 일을 사람 손에 맡기면
    # 다음 build 때 공급원·매출원이 상자로 되살아난다(프레임워크 §13)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
    apply_supply_shares()
