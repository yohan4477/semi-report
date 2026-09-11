# -*- coding: utf-8 -*-
"""Bloom 사슬의 관계·관측·방법·주장·BOM·재무 앵커를 굽는다.

관계는 지속적인 것만 담는다. 변하는 숫자는 전부 관측으로 가고 분모·기준일·근거등급을 단다.
2024 의 값을 2026 으로 끌어 쓰지 않는다 — 모르는 해는 값을 비우고 UNKNOWN 으로 남긴다.
scripts/build_bloom_vc.py 가 엔티티·출처를 전역에 넣은 뒤에 돌린다.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'bloom-energy')
BE = 'bloom-energy'

# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence_level, econ, capa, sources, notes)
R = [
 # ── 원재료 ────────────────────────────────────────────────────────
 ('scandium-undisclosed-bloom', 'undisclosed-scandium-suppliers', BE, 'SUPPLIES',
  'MANUFACTURING_BOM', 'Raw material', '산화스칸듐', '원재료 공급사', '제조사',
  None, None, 'ACTIVE', 'UNDISCLOSED', 'LOW', 'HIGH', ['be_scandium_blog'],
  '복수국 복수 업체라고만 공개. 업체명·물량·조달 전략 비공개'),
 ('zirconia-bloom', 'zirconium-oxide', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Raw material',
  '산화지르코늄', '원재료', '제조사', None, None, 'ACTIVE', 'UNDISCLOSED', 'LOW', 'HIGH',
  ['be_scandium_blog'], '초박형 세라믹 기판의 기반 물질. 벤더 비공개'),
 # ── 운영 투입 (제조 BOM 아님) ─────────────────────────────────────
 ('natgas-bloom-fleet', 'natural-gas', BE, 'FUELS', 'OPERATIONAL_INPUT', 'Operational input',
  '설치된 Energy Server 연료', '연료', '운영자', None, None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_10k_fy2025'], '제조 원가가 아니라 가동 중인 설비의 투입'),
 ('biogas-bloom-fleet', 'biogas', BE, 'FUELS', 'OPERATIONAL_INPUT', 'Operational input',
  '설치된 Energy Server 연료', '연료', '운영자', None, None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_10k_fy2025'], None),
 ('hydrogen-bloom-fleet', 'hydrogen', BE, 'FUELS', 'OPERATIONAL_INPUT', 'Operational input',
  '혼소 수소', '연료', '운영자', None, None, 'ACTIVE', 'CONFIRMED', None, None,
  ['be_10k_fy2025'], None),
 # ── 셀·세라믹 ─────────────────────────────────────────────────────
 ('cctc-bloom-electrolyte', 'cctc', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Cell',
  'SOFC 전해질 세라믹 격막·기판', '세라믹 공급사', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'MEDIUM', 'VERY_HIGH', ['cctc_yicai'],
  '관계는 확인. 조달 점유율은 공식 비공개이고 2차 조사 추정만 있다'),
 ('amosense-bloom-substrate', 'amosense', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Cell',
  'SOFC 세라믹 기판', '세라믹 공급사', '제조사', '2026-01-01', None, 'ACTIVE', 'CONFIRMED',
  'LOW', 'MEDIUM', ['sedaily_kr_suppliers'], '2026 신규 진입. 세라믹 공급망 다변화 신호'),
 ('yongzhou-bloom-ceramic', 'yongzhou-mingrui', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Other ceramic', '세라믹 플레이트·심', '세라믹 공급사', '제조사', None, None, 'ACTIVE',
  'INFERRED', 'LOW', None, ['be_10k_fy2025'],
  '전해질 기판과 분리한다. 어느 하위 계통에 쓰이는지는 추론'),
 ('cumi-bloom-alumina', 'cumi', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Other ceramic',
  '고알루미나 엔지니어링·내화 세라믹', '세라믹 공급사', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'],
  '제품은 확인. 핫존 구조·단열 용도는 추론이며 실(seal) 공급사로 단정하지 않는다'),
 ('unicorn-bloom-insulation', 'unicorn-insulations', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Thermal', '단열재', '부품 공급사', '제조사', None, None, 'ACTIVE', 'ESTIMATED',
  'LOW', None, ['be_10k_fy2025'], None),
 # ── 인터커넥트 ────────────────────────────────────────────────────
 ('porite-bloom-interconnect', 'porite-taiwan', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Interconnect', '크롬 합금 인터커넥트 플레이트', '부품 공급사', '제조사', '2024-01-01',
  None, 'ACTIVE', 'CONFIRMED', 'HIGH', 'HIGH', ['cw_porite_2024'],
  '장기 공급사. 2024 의 50% 는 그 시점 관측일 뿐 현재 점유율이 아니다'),
 ('stackpole-bloom-interconnect', 'stackpole-intl', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Interconnect', '금속 인터커넥트', '부품 공급사', '제조사', None, None, 'UNKNOWN',
  'INFERRED', None, None, ['cw_porite_2024'],
  '2024 취재의 「캐나다 공급사」 후보. 공동 특허가 근거이며 현재 점유율은 모른다'),
 ('plusmetal-bloom-coating', 'plus-metal-tech', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Interconnect', '인터커넥트 표면 코팅·관련 플레이트', '부품 공급사', '제조사', None, None,
  'ACTIVE', 'CONFIRMED', 'MEDIUM', None, ['be_10k_fy2025'], None),
 # ── 핫박스 ────────────────────────────────────────────────────────
 ('mtar-bloom-hotbox', 'mtar-technologies', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Hotbox',
  '핫박스·파워유닛·판금 어셈블리·인클로저·ASP 어셈블리', '전략 제조 파트너', '제조사',
  '2024-01-01', None, 'ACTIVE', 'CONFIRMED', 'HIGH', 'HIGH', ['mtar_ar_fy2425', 'mtar_ar_fy2024'],
  '전해조 유닛은 단독 공급으로 설명된다. 인클로저·하네스가 섞여 기계 계통과 겹칠 수 있다'),
 ('kaori-bloom-hotbox', 'kaori-heat-treatment', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Hotbox',
  '핫박스·반응박스', '부품 공급사', '제조사', None, None, 'ACTIVE', 'CONFIRMED',
  'HIGH', 'HIGH', ['kgi_kaori_2024'],
  'MTAR 50~60% 의 나머지를 그대로 Kaori 몫으로 읽는 것은 보수적 추론일 뿐이다'),
 # ── 전력 전자 ─────────────────────────────────────────────────────
 ('acbel-bloom-power', 'acbel-polytech', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Power electronics', '전력 변환·전원 공급', '부품 공급사', '제조사', '2024-01-01', None,
  'ACTIVE', 'CONFIRMED', 'MEDIUM', None, ['be_10k_fy2025'], None),
 ('sanmina-bloom-converter', 'sanmina-sci-india', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Power electronics', '정지형 컨버터·DC-DC 어셈블리', 'EMS', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'MEDIUM', None, ['be_10k_fy2025'],
  'AcBel·Sanmina·Bloom 인도를 단순히 더하면 부품과 조립과 통합이 겹쳐 이중계산된다'),
 ('cypress-bloom-harness', 'cypress-industries', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Power electronics', '와이어 하네스', '부품 공급사', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'], None),
 ('bloomindia-bloom-power', 'bloom-energy-india', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Power electronics', '전력 조절·제어 시스템', '자회사 생산', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'MEDIUM', None, ['be_10k_fy2025'], None),
 # ── 기계·모듈 ─────────────────────────────────────────────────────
 ('seojin-bloom-module', 'seojin-system', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Mechanical',
  'SOFC 모듈과 셀 제외 주요 부품', '모듈 제조 파트너', '제조사', '2026-07-15', '2027-03-22',
  'ACTIVE', 'CONFIRMED', 'MEDIUM', 'MEDIUM', ['seojin_kind', 'sedaily_kr_suppliers'],
  '계약에 MW·수량이 없다. 통합 경계는 추론이며 조달 점유율은 모른다'),
 ('nash-bloom-enclosure', 'nash-industries', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Mechanical',
  '인클로저·섀시·기계 조립', '부품 공급사', '제조사', None, None, 'ACTIVE', 'CONFIRMED',
  'LOW', None, ['be_10k_fy2025'], None),
 ('texon-bloom-enclosure', 'texon', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Mechanical',
  '강판 인클로저·도어·KPE 인클로저', '부품 공급사', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'], None),
 ('hansun-bloom-plumbing', 'hansun-engineering', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Mechanical', '연료·가스 분배 배관 모듈', '부품 공급사', '제조사', None, None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'], '조달 점유율은 공개되지 않았다'),
 ('technoflex-bloom-exhaust', 'technoflex-tf-vietnam', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Thermal', '발전기 배기 연결', '부품 공급사', '제조사', None, None, 'ACTIVE', 'CONFIRMED',
  'LOW', None, ['be_10k_fy2025'], None),
 # ── 계측 ─────────────────────────────────────────────────────────
 ('chunhui-bloom-thermocouple', 'zhejiang-chunhui', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Instrumentation', '열전대', '부품 공급사', '제조사', None, None, 'ACTIVE', 'CONFIRMED',
  'LOW', None, ['be_10k_fy2025'], '통관 자료에서 반복 선적 확인'),
 ('okazaki-bloom-thermocouple', 'okazaki-mfg', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Instrumentation', '열전대', '부품 공급사', '제조사', '2025-01-01', None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'], None),
 ('microsensor-bloom-level', 'micro-sensor', BE, 'SUPPLIES', 'MANUFACTURING_BOM',
  'Instrumentation', '레벨 트랜스미터', '부품 공급사', '제조사', '2026-01-01', None, 'ACTIVE',
  'CONFIRMED', 'LOW', None, ['be_10k_fy2025'], None),
 ('protechnic-bloom-fan', 'protechnic-wujiang', BE, 'SUPPLIES', 'MANUFACTURING_BOM', 'Thermal',
  'DC 팬', '부품 공급사', '제조사', None, None, 'UNKNOWN', 'HISTORICAL_CURRENT_UNKNOWN',
  'LOW', None, ['be_10k_fy2025'], '공급 이력은 있으나 현재 주력 여부가 불확실하다'),
 # ── 제조 장비·사이트 전기 (BOM 과 섞지 않는다) ─────────────────────
 ('coseus-bloom-equipment', 'coseus', BE, 'EQUIPMENT_SUPPLY', 'MANUFACTURING_EQUIPMENT',
  'Manufacturing equipment', '전극셀 코팅 자동화 장비', '설비 공급사', '제조사', '2026-07-10',
  '2026-10-29', 'ACTIVE', 'CONFIRMED', 'LOW', 'VERY_HIGH', ['coseus_kind', 'sedaily_kr_suppliers'],
  '제품 BOM 이 아니라 설비 투자. 원가 비중은 낮고 증설 병목으로서 중요도는 높다'),
 ('lselectric-bloom-bop', 'ls-electric', BE, 'ELECTRICAL_BOP_SUPPLY', 'SITE_ELECTRICAL_BOP',
  'Site electrical BoP', '배전반·배전 변압기', '전기 기자재 공급사', '제조사', '2026-04-28',
  '2027-03-29', 'ACTIVE', 'CONFIRMED', None, None, ['lselectric_kind'],
  '제품 BOM 이 아니라 부지 전기 인프라 층'),
 ('lselectric-jupiter', 'ls-electric', 'project-jupiter', 'PROJECT_SUPPLY',
  'SITE_ELECTRICAL_BOP', 'Site electrical BoP', '프로젝트 전기 BoP', '전기 기자재 공급사',
  '프로젝트', '2026-04-28', '2027-03-29', 'ACTIVE', 'INFERRED', None, None,
  ['lselectric_kind', 'oracle_jupiter'],
  '지역과 시점이 붙지만 LS 와 오라클을 직접 잇는 문장은 찾지 못했다'),
 # ── 기업 구조 ─────────────────────────────────────────────────────
 ('bloom-sk-jv', BE, 'bloom-sk-fuel-cell', 'JV_ASSEMBLY', 'CORPORATE', 'Assembly',
  '한국 완제품 조립', '기술·지분', 'JV', '2019-01-01', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_10k_fy2025'], '2020 가동, 2023 범위를 full assembly 로 확대'),
 ('aepohio-aep', 'aep-ohio', 'aep', 'SUBSIDIARY_OF', 'CORPORATE', 'Utility', None,
  '자회사', '모회사', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['aep_ohio_release'], None),
 ('borderplex-jupiter', 'borderplex', 'project-jupiter', 'DEVELOPS', 'DOWNSTREAM', 'Project',
  '부지·개발', '개발사', '프로젝트', '2026-04-27', None, 'ACTIVE', 'CONFIRMED', None, None,
  ['oracle_jupiter'], None),
 # ── 다운스트림: 금융 ──────────────────────────────────────────────
 ('brookfield-fundjv', 'brookfield', 'brookfield-fund-jvs', 'FINANCES', 'DOWNSTREAM',
  'Financing', 'AI 인프라 전력 프로젝트 금융', '펀드 스폰서', '펀드 JV', '2025-01-01', None,
  'ACTIVE', 'CONFIRMED', None, None, ['be_brookfield_25b'], '2025 50억 → 2026-06 250억 달러'),
 ('bloom-fundjv-sales', BE, 'brookfield-fund-jvs', 'SELLS_TO', 'DOWNSTREAM', 'Financing',
  'Energy Server·설치', '제조사', '계약상 고객·자산 보유', '2025-01-01', None, 'ACTIVE',
  'CONFIRMED', None, None, ['be_10k_fy2025'],
  '계약상 고객이다. 스폰서(Brookfield)와도, 최종 사용자와도 다른 주체다'),
 ('kdb-eternix-pf', 'kdb', 'sk-eternix', 'PROJECT_FINANCE', 'DOWNSTREAM', 'Financing',
  '80MW 프로젝트 금융', '주선 금융기관', '개발사', '2024-01-01', '2025-12-31', 'ACTIVE',
  'CONFIRMED', None, None, ['be_sk_eternix_80mw'], None),
 ('southern-bloom-legacy', 'southern-company', BE, 'FINANCES', 'DOWNSTREAM', 'Financing',
  '제3자 금융', '금융 제공', '제조사', None, None, 'ENDED', 'HISTORICAL_CURRENT_UNKNOWN',
  None, None, ['be_10k_fy2024'], '과거 제3자 금융 구조. 현재 핵심 구조와 구분한다'),
 ('duke-bloom-legacy', 'duke-energy', BE, 'FINANCES', 'DOWNSTREAM', 'Financing', '제3자 금융',
  '금융 제공', '제조사', None, None, 'ENDED', 'HISTORICAL_CURRENT_UNKNOWN', None, None,
  ['be_10k_fy2024'], None),
 ('exelon-bloom-legacy', 'exelon', BE, 'FINANCES', 'DOWNSTREAM', 'Financing', '제3자 금융',
  '금융 제공', '제조사', None, None, 'ENDED', 'HISTORICAL_CURRENT_UNKNOWN', None, None,
  ['be_10k_fy2024'], None),
 # ── 다운스트림: EPC·유통 ──────────────────────────────────────────
 ('bloom-skecoplant', BE, 'sk-ecoplant', 'DISTRIBUTION_PARTNERSHIP', 'DOWNSTREAM',
  'EPC / Distribution', 'Energy Server 유통·EPC', '제조사', '유통·EPC', '2019-01-01', None,
  'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025', 'be_sk_500mw_2023'],
  '과거 500MW take-or-pay 와 후속 물량 약정. 2025-07-10 까지 특수관계였다'),
 ('bloom-skamericas', BE, 'sk-ecoplant-americas', 'DISTRIBUTION_PARTNERSHIP', 'DOWNSTREAM',
  'EPC / Distribution', '미국 시공 관리·EPC·금융 서비스', '제조사', 'EPC', None, None,
  'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-eternix', BE, 'sk-eternix', 'SELLS_TO', 'DOWNSTREAM', 'EPC / Distribution',
  'Energy Server', '제조사', '개발·유통', '2024-03-01', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_sk_eternix_80mw'], '충주 40MW + 대소원 40MW'),
 # ── 다운스트림: 유틸리티 ──────────────────────────────────────────
 ('bloom-aep', BE, 'aep', 'SELLS_TO', 'DOWNSTREAM', 'Utility', 'Energy Server 조달 계약',
  '제조사', '유틸리티·채널·금융', '2024-11-14', None, 'ACTIVE', 'CONFIRMED', None, None,
  ['be_aep_1gw', 'be_10k_fy2025'],
  '한 회사가 유틸리티이자 채널이자 금융이다. 역할은 엔티티가 아니라 이 엣지에 붙는다'),
 ('aepohio-aws', 'aep-ohio', 'aws', 'UTILITY_SERVES', 'DOWNSTREAM', 'Utility',
  '온사이트 연료전지 전력', '유틸리티', '데이터센터', '2025-01-01', None, 'ACTIVE',
  'CONFIRMED', None, None, ['aep_ohio_release'], '고객이 장기 계약으로 프로젝트 비용을 부담'),
 ('aepohio-cologix', 'aep-ohio', 'cologix', 'UTILITY_SERVES', 'DOWNSTREAM', 'Utility',
  '온사이트 연료전지 전력', '유틸리티', '데이터센터', '2025-01-01', None, 'ACTIVE',
  'CONFIRMED', None, None, ['aep_ohio_release'], None),
 # ── 다운스트림: 직접 고객 ─────────────────────────────────────────
 ('bloom-oracle', BE, 'oracle', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center',
  'AI 데이터센터용 Energy Server', '제조사', '최종 사용자', '2025-07-24', None, 'ACTIVE',
  'CONFIRMED', None, None, ['be_oracle_28gw', 'be_oracle_2025'], None),
 ('bloom-jupiter', BE, 'project-jupiter', 'SUPPLIES', 'DOWNSTREAM', 'Project',
  '연료전지 마이크로그리드', '제조사', '프로젝트', '2026-04-27', None, 'PLANNED', 'CONFIRMED',
  None, None, ['oracle_jupiter'], '최대 2.45GW 계획'),
 ('bloom-equinix', BE, 'equinix', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center',
  'Energy Server', '제조사', '최종 사용자', '2025-02-20', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_equinix_100mw'], None),
 ('bloom-nebius', BE, 'nebius', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center',
  'AI 인프라용 Energy Server', '제조사', '최종 사용자', '2026-05-20', None, 'ACTIVE',
  'CONFIRMED', None, None, ['nebius_be_328mw'], None),
 ('bloom-coreweave', BE, 'coreweave', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center',
  'Energy Server', '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None,
  ['be_10k_fy2025'], None),
 ('bloom-intel', BE, 'intel', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-att', BE, 'att', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-verizon', BE, 'verizon', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'Data center',
  'Energy Server', '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None,
  ['be_10k_fy2025'], None),
 ('bloom-quanta', BE, 'quanta-computer', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'C&I',
  'Energy Server', '제조사', '최종 사용자', '2024-01-01', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['be_10k_fy2025'], 'AI 하드웨어 제조 시설 용량을 150% 이상 늘렸다'),
 ('bloom-walmart', BE, 'walmart', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'C&I', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-homedepot', BE, 'home-depot', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'C&I', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-ferrari', BE, 'ferrari', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'C&I', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 ('bloom-fedex', BE, 'fedex', 'DIRECT_CUSTOMER', 'DOWNSTREAM', 'C&I', 'Energy Server',
  '제조사', '최종 사용자', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['be_10k_fy2025'], None),
 # ── 익명 고객 ─────────────────────────────────────────────────────
 ('bloom-be24c2', BE, 'be24_c2', 'SELLS_TO', 'DOWNSTREAM', 'Undisclosed customer', None,
  '제조사', '계약상 고객', '2024-01-01', '2024-12-31', 'UNKNOWN', 'UNDISCLOSED', None, None,
  ['be_10k_fy2024'], 'FY2024 16%. 법인 특정 불가'),
 ('bloom-be24c3', BE, 'be24_c3', 'SELLS_TO', 'DOWNSTREAM', 'Undisclosed customer', None,
  '제조사', '계약상 고객', '2024-01-01', '2024-12-31', 'UNKNOWN', 'UNDISCLOSED', None, None,
  ['be_10k_fy2024'], 'FY2024 14%. 법인 특정 불가'),
 ('bloom-be26c1', BE, 'be26_c1', 'SELLS_TO', 'DOWNSTREAM', 'Undisclosed customer', None,
  '제조사', '계약상 고객', '2026-01-01', None, 'UNKNOWN', 'UNDISCLOSED', None, None,
  ['be_10q_2026q2'], '2026 상반기 73%, 비특수관계. SEC 가 법인명을 밝히지 않았다'),
]


def rel(t):
    return {'id': t[0], 'source_entity': t[1], 'target_entity': t[2],
            'relationship_type': t[3], 'lane': t[4], 'subsystem': t[5], 'component': t[6],
            'source_role': t[7], 'target_role': t[8], 'valid_from': t[9], 'valid_to': t[10],
            'status': t[11], 'evidence_level': t[12],
            'economic_importance': t[13], 'capacity_criticality': t[14],
            'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium'}.get(t[12], 'low'),
            'flows': [], 'source_ids': t[15], 'notes': t[16]}


def dump(path, obj):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))
        f.write(u'\n')


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    print('관계 %d' % len(R))
