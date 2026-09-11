# -*- coding: utf-8 -*-
"""Bloom 사슬의 관측·방법·주장·가설·BOM·재무 앵커를 굽는다.

숫자는 전부 여기 있다. 관계 파일에는 변하는 값을 넣지 않는다.
모르는 해는 값을 비우고 status 로 남긴다 — 2024 의 값을 2026 칸에 쓰지 않는다.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'bloom-energy')

PCT = 'percent'
USDM = 'USD M'
MW = 'MW'

# (id, rel, metric, value, low, high, unit, period, p_start, p_end, as_of,
#  denominator, status, evidence_level, confidence, method_id, sources, note)
O = [
 # ── 인터커넥트 ────────────────────────────────────────────────────
 ('o-porite-share-2024', 'porite-bloom-interconnect', 'sourcing_share', 50, None, None, PCT,
  '2024', '2024-01-01', '2024-12-31', '2024-10-01',
  'Bloom 인터커넥트 플레이트 조달 물량', 'HISTORICAL', 'ESTIMATED', 0.7, None,
  ['cw_porite_2024'], '2024-10 현장 취재의 「Porite 와 캐나다 공급사가 대략 50:50」. 그 시점 관측이다'),
 ('o-porite-share-2025', 'porite-bloom-interconnect', 'sourcing_share', None, None, None, PCT,
  '2025', '2025-01-01', '2025-12-31', '2025-12-31',
  'Bloom 인터커넥트 플레이트 조달 물량', 'HISTORICAL_CURRENT_UNKNOWN', 'UNDISCLOSED', None,
  None, [], '공급은 이어지지만 점유율 공개가 없다. 2024 의 50% 를 연장하지 않는다'),
 ('o-porite-share-2026', 'porite-bloom-interconnect', 'sourcing_share', None, None, None, PCT,
  '2026', '2026-01-01', '2026-12-31', '2026-09-11',
  'Bloom 인터커넥트 플레이트 조달 물량', 'HISTORICAL_CURRENT_UNKNOWN', 'UNDISCLOSED', None,
  None, [], '증설 신호는 있으나 현재 조달 점유율은 공개되지 않았다'),
 ('o-porite-content-2024', 'porite-bloom-interconnect', 'content_per_mw', 277000, None, None,
  'USD/MW', '2024', '2024-01-01', '2024-12-31', '2024-10-01',
  'Bloom 시스템 1MW 당 Porite 몫 플레이트 값', 'HISTORICAL', 'ESTIMATED', 0.55,
  'method-porite-content', ['cw_porite_2024'], None),
 ('o-stackpole-share-2026', 'stackpole-bloom-interconnect', 'sourcing_share', None, None, None,
  PCT, '2026', '2026-01-01', '2026-12-31', '2026-09-11',
  'Bloom 인터커넥트 플레이트 조달 물량', 'UNKNOWN', 'INFERRED', 0.4, None, ['cw_porite_2024'],
  '캐나다 공급사의 정체 자체가 추론이다'),
 # ── 핫박스 ────────────────────────────────────────────────────────
 ('o-mtar-share-2024', 'mtar-bloom-hotbox', 'sourcing_share', 55, 50, 60, PCT, '2024',
  '2024-01-01', '2024-12-31', '2024-08-17', 'Bloom 핫박스 요구량', 'HISTORICAL', 'CONFIRMED',
  0.95, None, ['mtar_ar_fy2024'], 'MTAR 연차보고서의 직접 공시'),
 ('o-mtar-share-2025', 'mtar-bloom-hotbox', 'sourcing_share', 55, 50, 60, PCT, '2025',
  '2025-01-01', '2025-12-31', '2025-08-01', 'Bloom 핫박스 요구량', 'HISTORICAL', 'CONFIRMED',
  0.9, None, ['mtar_ar_fy2425'], '회사가 말한 통상 요구량 기준값으로 다룬다'),
 ('o-mtar-share-2026', 'mtar-bloom-hotbox', 'sourcing_share', 55, 50, 60, PCT, '2026',
  '2026-01-01', '2026-12-31', '2026-09-11', 'Bloom 핫박스 요구량', 'CURRENT', 'CONFIRMED',
  0.85, None, ['mtar_ar_fy2425'], None),
 ('o-kaori-share-2026', 'kaori-bloom-hotbox', 'sourcing_share', 45, 40, 50, PCT, '2026',
  '2026-01-01', '2026-12-31', '2026-09-11', 'Bloom 핫박스 요구량', 'CURRENT', 'INFERRED',
  0.4, 'method-kaori-complement', ['kgi_kaori_2024'],
  'MTAR 의 나머지를 그대로 읽은 값이다. 공식 수치가 아니다'),
 # ── 셀·세라믹 ─────────────────────────────────────────────────────
 ('o-cctc-share-2024', 'cctc-bloom-electrolyte', 'sourcing_share', None, None, None, PCT,
  '2024', '2024-01-01', '2024-12-31', '2024-12-31',
  'Bloom 전해질 세라믹 기판 조달 물량', 'HISTORICAL_CURRENT_UNKNOWN', 'UNDISCLOSED', None,
  None, [], '핵심 공급사로 알려졌을 뿐 그 해 점유율 공개 자료가 없다'),
 ('o-cctc-share-2025', 'cctc-bloom-electrolyte', 'sourcing_share', None, None, None, PCT,
  '2025', '2025-01-01', '2025-12-31', '2025-12-31',
  'Bloom 전해질 세라믹 기판 조달 물량', 'HISTORICAL_CURRENT_UNKNOWN', 'UNDISCLOSED', None,
  None, [], None),
 ('o-cctc-share-2026', 'cctc-bloom-electrolyte', 'sourcing_share', 77.5, 75, 80, PCT, '2026',
  '2026-01-01', '2026-12-31', '2026-09-11', 'Bloom 전해질 세라믹 기판 조달 물량(2026 추정)',
  'CURRENT', 'ESTIMATED', 0.75, None, ['cctc_yicai'],
  '업계·증권 조사 수치를 모은 값이다. 회사 공시가 아니다'),
 ('o-amosense-share-2026q3', 'amosense-bloom-substrate', 'capacity_equivalent_share', None, 15,
  16, PCT, '2026 Q3', '2026-07-01', '2026-09-30', '2026-09-11',
  'Bloom 1.5GW 가동률 기준 연 세라믹 기판 수요', 'CURRENT', 'ESTIMATED', 0.7,
  'method-amosense-share-1p5gw', ['sedaily_kr_suppliers'],
  '설비 능력을 수요로 나눈 값이다. 실제 조달 점유율이 아니다. 03 의 CLM006'),
 ('o-amosense-share-2026e', 'amosense-bloom-substrate', 'capacity_equivalent_share', None, 11,
  12, PCT, '2026 Q3', '2026-07-01', '2026-09-30', '2026-09-11',
  'Bloom 2.0GW 가동률 기준 연 세라믹 기판 수요', 'CURRENT', 'ESTIMATED', 0.65,
  'method-amosense-share-2gw', ['sedaily_kr_suppliers'],
  '분모가 앞의 것과 다르다. 나란히 비교하지 않는다. 03 의 CLM007'),
 ('o-amosense-capa-2026q3', 'amosense-bloom-substrate', 'supplier_capacity', 600000, None, None,
  'sheets/month', '2026 Q3', '2026-07-01', '2026-09-30', '2026-07-29',
  'AMOsense 월 생산 능력', 'CURRENT', 'CONFIRMED', 0.9, None, ['sedaily_kr_suppliers'],
  '20만 장에서 60만 장으로 확대 계획'),
 ('o-amosense-share-2025', 'amosense-bloom-substrate', 'capacity_equivalent_share', 0, None, None,
  PCT, '2025', '2025-01-01', '2025-12-31', '2025-12-31',
  'Bloom 세라믹 기판 조달 물량', 'NOT_YET_ACTIVE', 'CONFIRMED', 0.8, None,
  ['sedaily_kr_suppliers'], '2026 진입 전이다'),
 # ── 계약 ─────────────────────────────────────────────────────────
 ('o-coseus-contract-2026', 'coseus-bloom-equipment', 'contract_value', 100, None, None, USDM,
  '2026', '2026-07-10', '2026-10-29', '2026-07-13', '단일 계약 금액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['coseus_kind'], '₩1,504.2억'),
 ('o-coseus-cumulative-2026', 'coseus-bloom-equipment', 'cumulative_orders', 230, None, None,
  'KRW B', '2026', '2025-11-01', '2026-09-11', '2026-09-11',
  '2025-11 이후 Bloom 관련 누적 수주', 'CURRENT', 'ESTIMATED', 0.6, None,
  ['sedaily_kr_suppliers'], '보도 기준. 공시 합산이 아니다'),
 ('o-seojin-contract-2026', 'seojin-bloom-module', 'contract_value', 52.638, None, None, USDM,
  '2026', '2026-07-15', '2027-03-22', '2026-07-15', '단일 계약 금액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['seojin_kind'], '₩785.47억, 베트남 공장 EXW'),
 ('o-seojin-content-2026', 'seojin-bloom-module', 'content_per_mw', None, 40000, 80000,
  'USD/MW', '2026', '2026-07-15', '2027-03-22', '2026-09-11',
  '8개월 생산 시나리오별 1MW 당 서진 몫', 'UNKNOWN', 'ESTIMATED', 0.4,
  'method-seojin-sensitivity', ['seojin_kind'],
  '계약에 MW 가 없다. 중앙값을 세우지 않고 시나리오 폭만 남긴다'),
 ('o-ls-contract-nm-2026', 'lselectric-bloom-bop', 'contract_value', 216.526, None, None, USDM,
  '2026', '2026-04-28', '2027-03-29', '2026-04-29', '단일 계약 금액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['lselectric_kind'], '₩3,189.6억, 뉴멕시코 하이퍼스케일 데이터센터'),
 ('o-ls-contract-wy-2026', 'lselectric-bloom-bop', 'contract_value', 34.26, None, None, USDM,
  '2026 H2', '2026-08-01', '2027-06-30', '2026-08-01', '단일 계약 금액', 'CURRENT',
  'CONFIRMED', 0.9, None, ['lselectric_kind'], '와이오밍 하이퍼스케일 데이터센터 추가 계약'),
 # ── 매출 유형 구성 (05 §28) ──────────────────────────────────────
 ('o-rev-product-fy2024', 'bloom-rev-product', 'revenue_type_share', 73.6, None, None, PCT,
  'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10k_fy2024'], '제품 10억 8,515만 달러'),
 ('o-rev-install-fy2024', 'bloom-rev-installation', 'revenue_type_share', 8.3, None, None,
  PCT, 'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출',
  'HISTORICAL', 'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10k_fy2024'], None),
 ('o-rev-service-fy2024', 'bloom-rev-service', 'revenue_type_share', 14.5, None, None, PCT,
  'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10k_fy2024'], None),
 ('o-rev-elec-fy2024', 'bloom-rev-electricity', 'revenue_type_share', 3.6, None, None, PCT,
  'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10k_fy2024'], None),
 ('o-rev-product-fy2025', 'bloom-rev-product', 'revenue_type_share', 75.7, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10k_fy2025'], '제품 15억 3,128만 달러'),
 ('o-rev-install-fy2025', 'bloom-rev-installation', 'revenue_type_share', 10.1, None, None,
  PCT, 'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출',
  'HISTORICAL', 'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10k_fy2025'],
  '설치 2억 410만 달러'),
 ('o-rev-service-fy2025', 'bloom-rev-service', 'revenue_type_share', 11.3, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10k_fy2025'], '서비스 2억 2,830만 달러'),
 ('o-rev-elec-fy2025', 'bloom-rev-electricity', 'revenue_type_share', 3.0, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10k_fy2025'], '전력 6,035만 달러'),
 ('o-rev-product-2026h1', 'bloom-rev-product', 'revenue_type_share', 87.5, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'CONFIRMED', 1.0, 'method-revenue-mix', ['be_10q_2026q2'], '제품 15억 8,876만 달러'),
 ('o-rev-install-2026h1', 'bloom-rev-installation', 'revenue_type_share', 4.2, None, None,
  PCT, '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출',
  'CURRENT', 'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10q_2026q2'], None),
 ('o-rev-service-2026h1', 'bloom-rev-service', 'revenue_type_share', 7.2, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10q_2026q2'], None),
 ('o-rev-elec-2026h1', 'bloom-rev-electricity', 'revenue_type_share', 1.1, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'CONFIRMED', 0.95, 'method-revenue-mix', ['be_10q_2026q2'], None),
 # ── 고객 집중도 ───────────────────────────────────────────────────
 ('o-skecoplant-share-fy2024', 'bloom-skecoplant', 'customer_revenue_share', 23, None, None,
  PCT, 'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'ESTIMATED', 0.9, 'method-sk-2024-match', ['be_10k_fy2024'],
  '23% 몫 약 3.39억 달러가 특수관계 매출 3.386억 달러와 사실상 같다'),
 ('o-be24c2-share-fy2024', 'bloom-be24c2', 'customer_revenue_share', 16, None, None, PCT,
  'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'UNDISCLOSED', None, None, ['be_10k_fy2024'], '약 2.36억 달러. 법인 특정 불가'),
 ('o-be24c3-share-fy2024', 'bloom-be24c3', 'customer_revenue_share', 14, None, None, PCT,
  'FY2024', '2024-01-01', '2024-12-31', '2025-02-01', 'Bloom FY2024 총매출', 'HISTORICAL',
  'UNDISCLOSED', None, None, ['be_10k_fy2024'], '약 2.06억 달러. 법인 특정 불가'),
 ('o-fundjv-share-fy2025', 'bloom-fundjv-sales', 'customer_revenue_share', 42.6, None, None,
  PCT, 'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 0.99, 'method-fundjv-share', ['be_10k_fy2025'],
  '공시 최대 고객 43% 와 맞는다'),
 ('o-be25c2-share-fy2025', 'bloom-be25c2', 'customer_revenue_share', 13, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, None, ['be_10k_fy2025'],
  '비중 자체는 공시다. 이 자리에 앉은 법인이 누구인지는 별도 가설로 관리한다'),
 ('o-be25c3-share-fy2025', 'bloom-be25c3', 'customer_revenue_share', 12, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'CONFIRMED', 1.0, None, ['be_10k_fy2025'],
  '비중 자체는 공시다. SK 계열이라는 것은 가설이다'),
 ('o-be26c1-share-2026h1', 'bloom-be26c1', 'customer_revenue_share', 44, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'UNDISCLOSED', None, None, ['be_10q_2026q2'],
  '상반기 최대 계약 고객 한 곳. SEC 가 법인명을 밝히지 않았다'),
 ('o-be26c1-share-2026q2', 'bloom-be26c1', 'customer_revenue_share', 73, None, None, PCT,
  '2026 Q2', '2026-04-01', '2026-06-30', '2026-07-31', 'Bloom 2026 2분기 총매출', 'CURRENT',
  'UNDISCLOSED', None, None, ['be_10q_2026q2'],
  '2분기 비특수관계 계약 고객 한 곳. SEC 가 법인명을 밝히지 않았다'),
 ('o-fundjv-share-2026h1', 'bloom-fundjv-sales', 'customer_revenue_share', 21, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'ESTIMATED', 0.7, None, ['be_10q_2026q2'],
  '상반기 2위 고객이 브룩필드 계열 펀드 JV 와 맞아떨어진다'),
 # ── 용량·약정 ─────────────────────────────────────────────────────
 ('o-aep-capacity-max', 'bloom-aep', 'agreement_capacity_max', 1000, None, None, MW,
  '2024-11 이후', '2024-11-14', None, '2024-11-14', '조달 계약 상한', 'CURRENT', 'CONFIRMED',
  1.0, None, ['be_aep_1gw'], None),
 ('o-aep-capacity-initial', 'bloom-aep', 'initial_order_capacity', 100, None, None, MW,
  '2024-11', '2024-11-14', None, '2024-11-14', '초기 주문', 'HISTORICAL', 'CONFIRMED', 1.0,
  None, ['be_aep_1gw'], None),
 ('o-oracle-capacity-max', 'bloom-oracle', 'agreement_capacity_max', 2800, None, None, MW,
  '2026', '2026-04-13', None, '2026-04-13', '전략 계약 상한', 'CURRENT', 'CONFIRMED', 1.0,
  None, ['be_oracle_28gw'], None),
 ('o-oracle-capacity-initial', 'bloom-oracle', 'contracted_capacity', 1200, None, None, MW,
  '2026', '2026-04-13', None, '2026-04-13', '계약·배치 중 용량', 'CURRENT', 'CONFIRMED', 1.0,
  None, ['be_oracle_28gw'], None),
 ('o-equinix-capacity-2025', 'bloom-equinix', 'relationship_capacity', 100, None, None, MW,
  '2025', '2025-02-20', None, '2025-02-20', '관계 누적 용량(초과)', 'CURRENT', 'CONFIRMED',
  1.0, None, ['be_equinix_100mw'], '약 75MW 가동 + 30MW 공사 중. 100MW 를 넘는다'),
 ('o-nebius-capacity-2026', 'bloom-nebius', 'planned_capacity', 328, None, None, MW, '2026',
  '2026-05-20', None, '2026-05-20', '첫 미국 배치 계획', 'CURRENT', 'CONFIRMED', 1.0, None,
  ['nebius_be_328mw'], None),
 ('o-eternix-capacity', 'bloom-eternix', 'project_capacity', 80, None, None, MW, '2024-2025',
  '2024-11-07', '2025-12-31', '2024-11-07', '한국 프로젝트 용량', 'HISTORICAL', 'CONFIRMED',
  1.0, None, ['be_sk_eternix_80mw'], '충주 40MW + 대소원 40MW'),
 ('o-jupiter-capacity', 'bloom-jupiter', 'planned_capacity', 2450, None, None, MW, '2026',
  '2026-04-27', None, '2026-04-27', '프로젝트 계획 상한', 'CURRENT', 'CONFIRMED', 1.0, None,
  ['oracle_jupiter'], None),
 ('o-brookfield-framework-2025', 'brookfield-fundjv', 'financing_framework', 5, None, None,
  'USD B', '2025', '2025-01-01', '2025-12-31', '2025-12-31', '금융 프레임워크 규모',
  'HISTORICAL', 'CONFIRMED', 1.0, None, ['be_brookfield_25b'], None),
 ('o-brookfield-framework-2026', 'brookfield-fundjv', 'financing_framework', 25, None, None,
  'USD B', '2026', '2026-06-30', None, '2026-06-30', '금융 프레임워크 규모', 'CURRENT',
  'CONFIRMED', 1.0, None, ['be_brookfield_25b'], None),
]

# (id, 제목, steps, 결과, 단위, 분모, 등급, 출처, 메모)
METHODS = [
 ('method-porite-content', 'Porite 몫 1MW 당 값',
  [('650kW 파워유닛 한 대당 플레이트', 30000, '장'),
   ('÷ 0.65MW', 46154, '장/MW'),
   ('× 장당 약 $6', 277000, 'USD/MW')],
  277000, 'USD/MW', 'Bloom 시스템 1MW', 'ESTIMATED', ['cw_porite_2024'],
  '장당 단가는 공급사 실적에서 역산한 값이다'),
 ('method-amosense-share-1p5gw', 'AMOsense 기판 물량 점유율 (1.5GW 가동률)',
  [('연 생산 능력', 7200000, '장/년'),
   ('÷ 1.5GW 기준 수요 4,500~4,950만 장', 15, '%')],
  15, '%', 'Bloom 1.5GW 가동률 기준 연 세라믹 기판 수요', 'ESTIMATED',
  ['sedaily_kr_suppliers'],
  '1GW 당 3,000~3,300만 장으로 잡는다. 한 장을 25W 로 보던 옛 분모는 걷었다'),
 ('method-amosense-share-2gw', 'AMOsense 기판 물량 점유율 (2.0GW 가동률)',
  [('연 생산 능력', 7200000, '장/년'),
   ('÷ 2.0GW 기준 수요 6,000~6,600만 장', 11, '%')],
  11, '%', 'Bloom 2.0GW 가동률 기준 연 세라믹 기판 수요', 'ESTIMATED', ['sedaily_kr_suppliers'],
  '앞의 15~16% 와 분모가 다르다'),
 ('method-kaori-complement', 'Kaori 잔여 몫',
  [('Bloom 핫박스 요구량', 100, '%'), ('− MTAR 50~60%', 45, '%')],
  45, '%', 'Bloom 핫박스 요구량', 'INFERRED', ['mtar_ar_fy2425'],
  '나머지를 한 회사가 다 맡는다는 보장이 없다'),
 ('method-fundjv-share', 'FY2025 최대 고객 43% 의 정체',
  [('펀드 JV 제품 매출', 809.8, 'USD M'), ('+ 설치 매출', 52.3, 'USD M'),
   ('= 합계', 862.1, 'USD M'), ('÷ 총매출 2,024.0', 42.6, '%')],
  42.6, '%', 'Bloom FY2025 총매출', 'CONFIRMED', ['be_10k_fy2025'],
  '공시 43% 와 사실상 일치한다'),
 ('method-aep-13', 'FY2025 2위 고객 13% 의 후보',
  [('초기 주문', 100, 'MW'), ('× 약 $2.5~3.0M/MW', 300, 'USD M'),
   ('vs 총매출의 13%', 263, 'USD M')],
  13, '%', 'Bloom FY2025 총매출', 'ESTIMATED', ['be_aep_1gw', 'be_10k_fy2025'],
  '금액이 맞는다는 것이 법인 확인은 아니다'),
 ('method-sk-12', 'FY2025 3위 고객 12% 의 후보',
  [('한국 프로젝트', 80, 'MW'), ('× 약 $3.0M/MW', 240, 'USD M'),
   ('vs 총매출의 12%', 243, 'USD M')],
  12, '%', 'Bloom FY2025 총매출', 'ESTIMATED', ['be_sk_eternix_80mw', 'be_10k_fy2025'],
  'SK 에너닉스 본사인지 프로젝트 법인인지 모른다'),
 ('method-sk-2024-match', 'FY2024 최대 고객 23% 의 정체',
  [('총매출 1,473.9 × 23%', 339, 'USD M'), ('vs 특수관계 매출', 338.6, 'USD M')],
  23, '%', 'Bloom FY2024 총매출', 'ESTIMATED', ['be_10k_fy2024'],
  '두 값이 사실상 같아 SK 계열로 본다'),
 ('method-rev-equiv-mw', '매출 환산 MW',
  [('제품 매출', None, 'USD M'), ('÷ ASP 앵커 $3.0M/MW', None, 'MW')],
  None, 'MW', 'SK 500MW / 약 15억 달러에서 뽑은 $3.0M/MW 앵커', 'ESTIMATED',
  ['be_sk_500mw_2023'], '출하 MW 공시가 아니다. 원가를 나눌 분모로만 쓴다'),
 ('method-cogs-per-mw', '매출 환산 MW 당 제품 원가',
  [('제품 원가', None, 'USD M'), ('÷ 매출 환산 MW', None, 'USD M/MW')],
  None, 'USD M/MW', '매출 환산 MW', 'ESTIMATED', ['be_10k_fy2025'],
  '2024 약 1.90 → 2025 약 1.95 → 2026 상반기 약 1.93 으로 거의 움직이지 않았다'),
 ('method-revenue-mix', '매출 유형 비중',
  [('그 매출원 금액', None, 'USD M'), ('÷ 같은 기간 총매출', None, '%')],
  None, '%', '같은 기간 Bloom 총매출', 'CONFIRMED', ['be_10k_fy2025'],
  '반올림 때문에 넷을 더하면 100.0% 와 조금 다를 수 있다'),
 ('method-seojin-sensitivity', '서진 몫 1MW 당 값의 시나리오 폭',
  [('계약 금액', 52.638, 'USD M'), ('÷ 8개월 667MW 시나리오', 79000, 'USD/MW'),
   ('÷ 1.0GW 시나리오', 53000, 'USD/MW'), ('÷ 1.33GW 시나리오', 40000, 'USD/MW')],
  None, 'USD/MW', '8개월 생산량 시나리오', 'ESTIMATED', ['seojin_kind'],
  '계약에 MW 가 없으므로 중앙값을 세우지 않는다'),
]

# 재무 앵커 — 관계 데이터와 섞지 않는다
FIN = [
 ('FY2024', 1473.856, 1085.153, 685.847, 36.8, 362, '2025-02-01', ['be_10k_fy2024']),
 ('FY2025', 2023.994, 1531.281, 992.841, 35.2, 510, '2026-02-09', ['be_10k_fy2025']),
 ('2026-H1', 1816.419, 1588.761, 1023.189, 35.6, 530, '2026-07-31', ['be_10q_2026q2']),
]

# BOM 작업 모델 — 공식 BOM 이 아니다
BOM = {
 'company': 'bloom-energy', 'period': '2026-current', 'as_of_date': '2026-09-11',
 'unit': 'USD M/MW', 'status': 'ESTIMATED',
 'denominator': '매출 환산 MW 당 제품 원가',
 'total': {'low': 1.8, 'high': 1.95, 'central': 1.85},
 'note': 'Bloom 이 공개한 BOM 이 아니다. 전부 추정이며 화면에도 그렇게 적는다',
 'method_id': 'method-cogs-per-mw',
 'components': [
  {'id': 'cell', 'label': '셀·전기화학', 'central': 0.22, 'low': 0.18, 'high': 0.25,
   'share_pct': 12, 'subsystem': 'Cell', 'evidence_level': 'ESTIMATED',
   'confidence': 'MEDIUM', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'interconnect', 'label': '인터커넥트', 'central': 0.45, 'low': 0.36, 'high': 0.56,
   'share_pct': 24, 'subsystem': 'Interconnect', 'evidence_level': 'ESTIMATED',
   'confidence': 'MEDIUM', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'hotbox', 'label': '핫박스·파워유닛', 'central': 0.35, 'low': 0.30, 'high': 0.38,
   'share_pct': 19, 'subsystem': 'Hotbox', 'evidence_level': 'ESTIMATED',
   'confidence': 'MEDIUM_HIGH', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'power-electronics', 'label': '전력 전자', 'central': 0.25, 'low': 0.20, 'high': 0.30,
   'share_pct': 14, 'subsystem': 'Power electronics', 'evidence_level': 'ESTIMATED',
   'confidence': 'LOW_MEDIUM', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'mechanical', 'label': '기계·모듈', 'central': 0.12, 'low': 0.08, 'high': 0.15,
   'share_pct': 6, 'subsystem': 'Mechanical', 'evidence_level': 'ESTIMATED',
   'confidence': 'LOW_MEDIUM', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'internal', 'label': 'Bloom 내부 전환', 'central': 0.20, 'low': None, 'high': None,
   'share_pct': 11, 'subsystem': None, 'evidence_level': 'INFERRED',
   'confidence': 'LOW', 'denominator': '매출 환산 MW 당 제품 원가'},
  {'id': 'residual', 'label': '잔여·중복 조정', 'central': 0.26, 'low': None, 'high': None,
   'share_pct': 14, 'subsystem': None, 'evidence_level': 'INFERRED',
   'confidence': 'LOW', 'denominator': '매출 환산 MW 당 제품 원가'},
 ],
}

# 익명 고객에 붙는 실명 후보. 확정치와 섞지 않는다
HYP = [
 {'id': 'h-be25-2nd-aep', 'anon_company_id': 'be25_c2', 'candidate_company_id': 'aep',
  'period': 'FY2025', 'likelihood': 3.75, 'status': 'estimated',
  'method': '초기 100MW 에 MW 당 250~300만 달러를 곱하면 2.5~3.0억 달러로 13% 몫 2.63억 달러와 겹친다',
  'notes': '금액이 겹친다는 것이 법인 확인은 아니다'},
 {'id': 'h-be25-3rd-eternix', 'anon_company_id': 'be25_c3', 'candidate_company_id': 'sk-eternix',
  'period': 'FY2025', 'likelihood': 3.5, 'status': 'estimated',
  'method': '80MW 에 MW 당 300만 달러를 곱하면 2.4억 달러로 12% 몫 2.43억 달러와 겹친다',
  'notes': '본사인지 프로젝트 법인인지 갈리지 않는다'},
 {'id': 'h-be26-73pct-oracle', 'anon_company_id': 'be26_c1', 'candidate_company_id': 'oracle',
  'period': '2026 H1', 'likelihood': 4.0, 'status': 'estimated',
  'method': 'SEC 가 오라클 워런트를 「고객의 고객」 대가로 회계처리하고 그 계약에 딸린 Energy Server 인도를 적시한다',
  'notes': '계약 상대방과 오라클을 한 칸에 넣지 않는다. 오라클은 최종 사용자 쪽이다'},
]


# 문장 단위 주장 — 03_Evidence & Sources 의 CLM001~CLM018
CLAIMS = [
 ('clm-be-fy2025-revenue', 'Bloom 의 FY2025 총매출은 20억 2,399만 달러다.', 'bloom-energy',
  None, 'FY2025', 'CONFIRMED', 1.0, ['be_10k_fy2025'],
  '제품 15억 3,128만 · 설치 2억 410만 · 서비스 2억 2,830만 · 전력 6,035만'),
 ('clm-fundjv-43', 'FY2025 최대 고객 43% 는 브룩필드 계열 펀드 JV 다.', 'brookfield-fund-jvs',
  'bloom-energy', 'FY2025', 'CONFIRMED', 0.99, ['be_10k_fy2025'],
  '제품 8억 980만 + 설치 5,230만 = 8억 6,210만 달러, 총매출의 42.6%'),
 ('clm-aep-13', 'FY2025 2위 고객 13% 는 AEP 매입 법인일 가능성이 크다.', 'aep',
  'bloom-energy', 'FY2025', 'INFERRED', 0.45, ['be_10k_fy2025', 'be_aep_1gw'],
  '13% 는 공시다. AEP 라는 지목은 용량과 단가를 맞춰 본 가설이다. 03 의 CLM003'),
 ('clm-eternix-12', 'FY2025 3위 고객 12% 는 SK 에너닉스 또는 그 프로젝트 법인일 수 있다.',
  'sk-eternix', 'bloom-energy', 'FY2025', 'INFERRED', 0.4, ['be_sk_eternix_80mw'],
  '12% 는 공시다. 법인 지목과 매출 인식 시점은 비공개다. 03 의 CLM004'),
 ('clm-cctc-share', 'CCTC 는 Bloom 전해질 세라믹의 주요 공급사이며 2026 조달 점유율은 75~80% 로 추정된다.',
  'cctc', 'bloom-energy', '2026E', 'ESTIMATED', 0.75, ['cctc_yicai'],
  '관계는 확인. 점유율은 2차 조사'),
 ('clm-amosense-15', 'AMOsense 의 세라믹 기판 설비 기준 점유율은 Bloom 1.5GW 가동률 기준 15~16% 다.',
  'amosense', 'bloom-energy', '2026 Q3', 'ESTIMATED', 0.7, ['sedaily_kr_suppliers'],
  '연 720만 장 ÷ 4,500~4,950만 장'),
 ('clm-amosense-9', 'AMOsense 의 점유율은 Bloom 2.0GW 가동률 기준으로는 11~12% 다.',
  'amosense', 'bloom-energy', '2026 Q3', 'ESTIMATED', 0.65, ['sedaily_kr_suppliers'],
  '앞 항목과 분모가 다르다'),
 ('clm-mtar-5060', 'MTAR 은 Bloom 핫박스 요구량의 약 50~60% 를 공급한다.', 'mtar-technologies',
  'bloom-energy', 'FY2024-FY2026', 'CONFIRMED', 0.95, ['mtar_ar_fy2425', 'mtar_ar_fy2024'],
  '회사 공시. 전해조 유닛은 단독 공급으로 설명된다'),
 ('clm-coseus-100m', 'Coseus 는 1억 달러 규모 전극셀 코팅 자동화 장비를 공급한다.', 'coseus',
  'bloom-energy', '2026-07-10~2026-10-29', 'CONFIRMED', 1.0, ['coseus_kind'],
  '제품 BOM 이 아니라 설비'),
 ('clm-seojin-52m', '서진시스템은 5,263.8만 달러 규모 SOFC 모듈·부품을 공급한다.', 'seojin-system',
  'bloom-energy', '2026-07-15~2027-03-22', 'CONFIRMED', 1.0, ['seojin_kind'],
  '베트남 EXW, 미국 공급, 대응 MW 비공개'),
 ('clm-ls-216m', 'LS일렉트릭은 뉴멕시코 데이터센터에 2억 1,652.6만 달러 규모 전기 기자재를 공급한다.',
  'ls-electric', 'bloom-energy', '2026-04-28~2027-03-29', 'CONFIRMED', 1.0, ['lselectric_kind'],
  '배전반과 배전 변압기'),
 ('clm-ls-jupiter', '그 뉴멕시코 계약은 프로젝트 주피터를 향한 것으로 보인다.', 'ls-electric',
  'project-jupiter', '2026', 'INFERRED', 0.95, ['lselectric_kind', 'oracle_jupiter'],
  '지역과 시점이 붙지만 직접 서술은 없다'),
 ('clm-brookfield-25b', '브룩필드의 AI 인프라 전력 금융 프레임워크는 250억 달러로 커졌다.',
  'brookfield', 'bloom-energy', '2026-06', 'CONFIRMED', 1.0, ['be_brookfield_25b'],
  '50억 달러에서 확대'),
 ('clm-oracle-28gw', '오라클 계약은 최대 2.8GW 이고 초기 1.2GW 가 계약·배치 중이다.', 'oracle',
  'bloom-energy', '2026', 'CONFIRMED', 1.0, ['be_oracle_28gw'], None),
 ('clm-equinix-100mw', '에퀴닉스와의 관계는 100MW 를 넘는다.', 'equinix', 'bloom-energy',
  '2025-02', 'CONFIRMED', 1.0, ['be_equinix_100mw'], '약 75MW 가동 + 30MW 공사 중'),
 ('clm-nebius-328mw', '네비우스의 첫 미국 배치 계획 용량은 328MW 다.', 'nebius', 'bloom-energy',
  '2026', 'CONFIRMED', 1.0, ['nebius_be_328mw'], None),
 ('clm-aep-1gw', 'AEP 조달 계약은 최대 1GW 이고 초기 주문은 100MW 다.', 'aep', 'bloom-energy',
  '2024-11 이후', 'CONFIRMED', 1.0, ['be_aep_1gw'], None),
 ('clm-eternix-80mw', 'SK 에너닉스의 한국 프로젝트는 80MW 이고 산업은행이 금융을 주선했다.',
  'sk-eternix', 'bloom-energy', '2024-2025', 'CONFIRMED', 1.0, ['be_sk_eternix_80mw'],
  '충주 40MW + 대소원 40MW'),
 # ── 03 Evidence & Sources CLM021~CLM052 추가분 ────────────────────
 ('clm-be26c1-same-customer', '2026년 상반기 44% 고객과 2분기 73% 고객은 같은 익명 계약 고객이다.',
  'be26_c1', 'bloom-energy', 'H1/Q2 2026', 'INFERRED', 0.8, ['be_10qa_2026q2'],
  '상반기 44%는 약 7억 9,920만 달러, 2분기 73%는 약 7억 7,770만 달러다. 2분기 금액만으로도 '
  '상반기 총액의 42.8%에 달해 별개 법인이라는 가정은 공시된 상반기 집중도와 맞지 않는다. '
  '법인명은 여전히 비공개다. 03의 CLM021'),
 ('clm-oracle-customers-customer',
  '오라클은 전략적·상업적 계약 당사자이지만 SEC는 워런트 대가를 고객의 고객에게 지급하는 것으로도 분류한다.',
  'oracle', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['be_10qa_2026q2', 'be_424b7_2026'],
  '직접적 법률상 계약 상대방 증거 없이 오라클을 2분기 73% 계약 고객과 같다고 두지 않는다. '
  '03의 CLM023'),
 ('clm-project-equity-50m',
  '블룸은 고객 프로젝트 계약과 관련한 제3의 비계열 법인에 묶인 5,000만 달러 규모 프로젝트 관련 지분투자를 기록했다.',
  'bloom-energy', None, '2026-06-30', 'CONFIRMED', 0.8, ['be_10qa_2026q2'],
  '프로젝트 법인·SPV 층의 존재 가능성을 뒷받침한다. 근거 없이 프로젝트 주피터 법인으로 특정하지 '
  '않는다. 대응 개체 id를 목록에서 찾지 못해 object는 None으로 둔다. 03의 CLM024'),
 ('clm-aepohio-aws-cologix',
  'AEP 오하이오는 AWS와 콜로직스 시설에 블룸 연료전지를 현장 설치하며, AWS와 콜로직스가 장기 계약에 '
  '따라 프로젝트 비용 전액을 부담한다.',
  'aep-ohio', 'bloom-energy', '2025-현재', 'CONFIRMED', 0.8, ['aep_ohio_2025'],
  'AEP 오하이오라는 중개·법인 층을 그대로 두는 경로가 정본이다. AWS와 콜로직스가 자동으로 블룸의 '
  '직접 계약 고객이 되는 것은 아니다. 03의 CLM025'),
 ('clm-kaori-4026pct',
  '블룸에너지는 카오리히트트리트먼트의 2025년 순매출에서 신대만달러 26억 4,959만을 차지했으며, '
  '이는 카오리 순매출의 40.26%에 해당한다.',
  'kaori-heat-treatment', 'bloom-energy', 'FY2025', 'CONFIRMED', 0.8, ['kaori_ar_fy2025'],
  '분모는 카오리의 2025 회계연도 순매출(신대만달러 65억 8,062만)이며, 블룸 핫박스 조달 점유율이 '
  '아니다. 2024 회계연도 블룸 매출은 신대만달러 18억 7,352만으로 카오리 순매출의 28.47%였다. '
  '03의 CLM026'),
 ('clm-cctc-historical-2014', 'CCTC(차오저우 쓰리서클)와 블룸의 과거 직접 공급 관계는 1차 자료로 확인된다.',
  'cctc', 'bloom-energy', '2012-2014', 'CONFIRMED', 0.8, ['cctc_ipo_2014'],
  '블룸은 2014년 상반기 CCTC 매출의 9.54%를 차지한 1위 고객이었다. 관계와 제품 범위를 확인할 뿐 '
  '2026년 75~80% 조달 점유율을 확인하지는 않는다. 03의 CLM027'),
 ('clm-sanmina-direct', '산미나-SCI 인디아는 블룸에 직접 공급하는 EMS·정지형 컨버터 조립 협력사다.',
  'sanmina-sci-india', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_sanmina_2026'],
  '2026년 CCE CORVA·정지형 컨버터 선적이 반복 확인된다. 선적 건수를 조달 점유율로 환산할 수는 '
  '없다. 03의 CLM028'),
 ('clm-acbel-direct',
  'AcBel폴리텍은 블룸에 직접 공급하는 전력전자 협력사이며, AcBel과 산미나 사이의 블룸 전용 하도급 '
  '관계는 아직 확인되지 않았다.',
  'acbel-polytech', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_acbel_2026'],
  '드라이브 원표기는 「CONFIRMED direct relationship / UNDISCLOSED tier relation」, 신뢰도는 '
  '「HIGH direct; UNKNOWN tier」다. 블룸 프로그램 단위 공급사 간 증거가 나오기 전까지 AcBel과 '
  '산미나는 독립 노드로 둔다. 03의 CLM029'),
 ('clm-nash-direct', '내시인더스트리스는 블룸에 직접 공급하는 기계·인클로저 협력사다.',
  'nash-industries', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_nash_2026'],
  'KPE/CM2 산타크루즈, CCE+1 인클로저 선적이 확인된다. 내시를 서진시스템 산하로 강제로 묶지 않는다. '
  '위계는 아직 풀리지 않았다. 03의 CLM030'),
 ('clm-texon-seojin', '텍슨은 서진시스템 계열사이며 블룸 인클로저를 직접 공급한다.',
  'texon', 'bloom-energy', '2026', 'CONFIRMED', 0.8,
  ['customs_texon_2026', 'texon_history', 'seojin_ar_2025'],
  '텍슨의 블룸 선적을 서진시스템의 5,263.8만 달러 모듈 계약과 같은 범위·발주로 가정하지 않는다. '
  '03의 CLM031'),
 ('clm-stackpole-patent', '스택폴인터내셔널파우더메탈은 과거 블룸과 금속 인터커넥트를 공동 개발한 이력이 있다.',
  'stackpole-intl', 'bloom-energy', '2014-2018', 'CONFIRMED', 0.8, ['patent_stackpole'],
  '드라이브 원표기는 「CONFIRMED historical technical relationship / INFERRED current '
  'supplier」, 신뢰도는 「HIGH historical; LOW-MEDIUM current supplier」다. 공동 특허가 2026년 '
  '상업적 조달 점유율을 뒷받침하지는 않는다. 03의 CLM032'),
 ('clm-porite-2026-active', '포라이트타이완의 현재 블룸 인터커넥트 플레이트 공급 관계는 2026년에도 이어진다.',
  'porite-taiwan', 'bloom-energy', '2026', 'CONFIRMED', 0.8,
  ['porite_2026_note', 'customs_porite_2026'],
  '선적과 공식 공급사 발언으로 관계는 확인된다. 2024년 약 50% 조달 점유율은 '
  'HISTORICAL_CURRENT_UNKNOWN 상태로 남으며, 관계가 살아 있다는 사실이 2026년 점유율을 확인해 '
  '주지는 않는다. 03의 CLM033'),
 ('clm-trade-snapshot-q1-2026',
  '2026년 1분기 무역 스냅샷은 블룸의 폭넓은 공급 기반을 보여줄 뿐, 선적 건수는 조달 비중이 아니다.',
  'bloom-energy', None, 'Q1 2026', 'CONFIRMED', 0.6, ['tarifflo_q1_2026'],
  '드라이브 원표기는 「CONFIRMED trade-data snapshot」이다. 1분기 1차 협력사 53곳이 확인되며, '
  '관계·활동 신호로만 쓰고 조달·지출 점유율로 쓰지 않는다. object는 특정 상대 법인이 없어 '
  'None으로 둔다. 03의 CLM034'),
 ('clm-jiafeng-direct', '둥관자펑기계설비는 블룸에 직접 공급하는 기계·패널 협력사다.',
  'dongguan-jiafeng', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_jiafeng_2026'],
  'CM1 빌드베이스 키트, 사이드패널, 워터스키드 인터페이스 조립품 직납이 확인된다. 조달 점유율은 '
  '공개되지 않았다. 03의 CLM035'),
 ('clm-cumi-direct', '카보런덤유니버설(CUMI)은 블룸에 직접 공급하는 엔지니어링 세라믹 협력사다.',
  'cumi', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_cumi_2026'],
  '드라이브 원표기는 「CONFIRMED product/relationship; exact SOFC function INFERRED」, 신뢰도는 '
  '「HIGH relationship; LOW-MEDIUM function」이다. 실링 부품으로 분류하지 않으며, 핫존 구조·단열 '
  '기능은 여전히 추정이다. 03의 CLM036'),
 ('clm-mingrui-direct', '융저우밍루이세라믹테크놀로지는 블룸에 직접 공급하는 기술 세라믹판 협력사다.',
  'yongzhou-mingrui', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_mingrui_2026'],
  '드라이브 원표기는 「CONFIRMED relationship / INFERRED subsystem」, 신뢰도는 「HIGH '
  'relationship; LOW-MEDIUM subsystem」이다. CCTC·AMOsense의 전해질 기판 공급과는 분리해 둔다. '
  '03의 CLM037'),
 ('clm-seojin-overseas-mfg',
  '2026년 블룸 모듈 계약은 서진시스템 해외법인을 거쳐 생산되지만, KRX 공시는 실행 자회사를 특정하지 '
  '않는다.',
  'seojin-system', 'bloom-energy', '2026-07-15~2027-03-22', 'CONFIRMED', 0.8, ['seojin_kind'],
  '드라이브 원표기는 「CONFIRMED production method / UNDISCLOSED executing subsidiary」다. '
  '프로젝트별 증거 없이 텍슨이나 다른 명명된 자회사를 발주 실행처로 단정하지 않는다. 03의 CLM038'),
 ('clm-coreweave-chirisa',
  '블룸의 배치는 코어위브를 위한 것이며, 그 데이터센터는 일리노이주 볼로에서 치리사테크놀로지파크스가 '
  '소유한다.',
  'coreweave', 'bloom-energy', '2024-2025', 'CONFIRMED', 0.8, ['be_coreweave_2024'],
  '최종 사용자·입주사인 코어위브와 부지 소유주인 치리사를 구분한다. 보도자료만으로는 블룸의 법적 '
  '매수 주체가 아직 입증되지 않는다. 03의 CLM039'),
 ('clm-3tg-136-suppliers',
  '블룸에너지는 2026년 4월 23일 기준 3TG 실사 대상 협력사 136곳을 두었고, 136곳 모두 유효한 '
  'CMRT를 제출했다.',
  'bloom-energy', None, '2026-04-23', 'CONFIRMED', 0.8, ['be_conflict_minerals_2025'],
  '분모는 분쟁광물 대상 협력사이며 전체 1차 상업 협력사 수가 아니다. 세관 관측 협력사 수와 직접 '
  '비교하지 않는다. object에 대응하는 단일 상대 법인이 없어 None으로 둔다. 03의 CLM043'),
 ('clm-3tg-downstream',
  '블룸에너지는 3TG를 하류에서 소비할 뿐 광산·제련소·정제소에서 원자재를 직접 구매하지 않는다.',
  'bloom-energy', None, 'FY2025 보고 / 2026년 제출', 'CONFIRMED', 0.8,
  ['be_conflict_minerals_2025'],
  '원자재 → 하위 협력사 → 직접 부품·소재 협력사 → 블룸으로 이어지는 위계를 뒷받침한다. object에 '
  '대응하는 단일 상대 법인이 없어 None으로 둔다. 03의 CLM044'),
 ('clm-cypress-direct', '사이프러스인더스트리스인디아는 블룸에 직접 공급하는 배선하네스 협력사다.',
  'cypress-industries', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_cypress_2026'],
  '2026년 9월 직납 선적이 확인된다. 조달 점유율은 공개되지 않았다. 03의 CLM045'),
 ('clm-unicorn-direct', '유니콘인슐레이션스는 블룸에 직접 공급하는 단열재 협력사다.',
  'unicorn-insulations', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_unicorn_2026'],
  '미세다공성·열단열재 선적이 2026년 반복 확인된다. 조달 점유율은 공개되지 않았다. 03의 CLM046'),
 ('clm-wolfe-direct', '울프엔지니어링상하이는 블룸에 배기관을 공급하는 협력사다.',
  'wolfe-engineering-shanghai', 'bloom-energy', '2025-2026', 'CONFIRMED', 0.8,
  ['customs_wolfe_2026'],
  '발전기 배기관 선적이 확인된다. 기계·열 배기 역할이며 조달 점유율은 공개되지 않았다. '
  '03의 CLM047'),
 ('clm-thermocouple-direct', '저장춘후이와 오카자키제작소는 블룸에 열전대를 공급하는 협력사다.',
  'zhejiang-chunhui', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_thermocouple_2026'],
  '오카자키제작소(okazaki-mfg)도 함께 반복 직납이 확인된다. 선적 수량은 조달 점유율이 아니다. '
  '03의 CLM048'),
 ('clm-hansun-global-cert', '한선엔지니어링은 블룸의 글로벌 배관모듈 협력사다.',
  'hansun-engineering', 'bloom-energy', '2026-06-24', 'CONFIRMED', 0.8, ['thebell_hansun_2026'],
  'SOFC 배관모듈 글로벌 공급사 인증이 확인된다. 정확한 글로벌 조달 점유율은 비공개다. '
  '03의 CLM049'),
 ('clm-mitac-expanded',
  '블룸과 미탁컴퓨팅테크놀로지의 확대된 협력은 프리몬트 AI서버 제조단지에 독립형 연료전지 마이크로그리드를 '
  '더하고 기존 새너제이 설치를 발판 삼는다.',
  'mitac-computing', 'bloom-energy', '2026-current', 'CONFIRMED', 0.8, ['be_mitac_2026'],
  '캘리포니아 두 지점에 걸친 직접 협력·배치는 확인되나, 보도자료는 미탁 전체 지점의 정확한 계약 '
  'MW를 밝히지 않는다. 03의 CLM050'),
 ('clm-ai-infra-250mw',
  '블룸에너지는 자사 AI 인프라 부문이 스무 곳 가까운 고객과 약 250MW에 걸쳐 있다고 밝혔다.',
  'bloom-energy', None, '2026-08-06', 'CONFIRMED', 0.8, ['be_mitac_2026'],
  '드라이브 원표기는 「CONFIRMED company statement」다. 분모는 블룸 AI 인프라 고객 부문이며, 블룸 '
  '전체 배치나 총 백로그가 아니다. object에 대응하는 단일 상대 법인이 없어 None으로 둔다. '
  '03의 CLM051'),
 ('clm-microsensor-direct', '마이크로센서는 블룸에 직접 공급하는 레벨트랜스미터 협력사다.',
  'micro-sensor', 'bloom-energy', '2026', 'CONFIRMED', 0.8, ['customs_microsensor_2026'],
  '2026년 반복 직납 선적이 확인된다. 조달 점유율은 공개되지 않았다. 03의 CLM052'),
]


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


SRC_DATE = None


def src_date(ids):
    global SRC_DATE
    if SRC_DATE is None:
        rows = json.load(io.open(os.path.join(DATA, 'sources.json'), encoding='utf-8'))
        SRC_DATE = dict((r['id'], r.get('published_date')) for r in rows)
    for i in ids or []:
        if SRC_DATE.get(i):
            return SRC_DATE[i]
    return None


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': t[15], 'source_ids': t[16],
            'method_note': t[17],
            # 고객 집중도는 총매출 기준이다. 그 선의 몫이 아니므로 선에 적지 않는다 (05 §28-4)
            'source_date': src_date(t[16]),
            'denominator_scope': ('FOCAL_TOTAL_REVENUE'
                                  if t[2] == 'customer_revenue_share' else 'EDGE')}


def meth(t):
    return {'id': t[0], 'title': t[1],
            'steps': [{'label': s[0], 'value': s[1], 'unit': s[2]} for s in t[2]],
            'result': t[3], 'result_unit': t[4], 'denominator': t[5], 'result_status': t[6],
            'source_ids': t[7], 'note': t[8]}


def fin(t):
    return {'company': 'bloom-energy', 'period': t[0], 'total_revenue_usd_m': t[1],
            'product_revenue_usd_m': t[2], 'product_cogs_usd_m': t[3],
            'product_gross_margin_pct': t[4],
            'revenue_equivalent_mw': {'value': t[5], 'status': 'ESTIMATED',
                                      'method_id': 'method-rev-equiv-mw'},
            'cogs_per_equivalent_mw': {'value': round(t[3] / t[5], 2),
                                       'unit': 'USD M/MW', 'status': 'ESTIMATED',
                                       'method_id': 'method-cogs-per-mw'},
            'as_of_date': t[6], 'source_ids': t[7]}


def dump(path, o):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(o, ensure_ascii=False, indent=1))
        f.write(u'\n')


def merge_methods():
    p = os.path.join(DATA, 'methods.json')
    cur = json.load(io.open(p, encoding='utf-8'))
    have = set(m['id'] for m in cur)
    for t in METHODS:
        if t[0] not in have:
            cur.append(meth(t))
    dump(p, cur)
    return len(cur)


def evidence():
    """관측마다 출처 연결을 근거 줄로 남긴다."""
    out, n = [], 0
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'be-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid,
                        'evidence_type': 'direct' if t[13] == 'CONFIRMED' else 'indirect',
                        'evidence': t[17] or '', 'hypothesis_id': None})
    for r in json.load(io.open(os.path.join(CHAIN, 'relationships.json'), encoding='utf-8')):
        for sid in r.get('source_ids') or []:
            n += 1
            out.append({'id': 'be-e%03d' % n, 'relationship_id': r['id'], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if r['evidence_level'] == 'CONFIRMED'
                                         else 'indirect',
                        'evidence': r.get('notes') or '', 'hypothesis_id': None})
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'hypotheses.json'), HYP)
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    dump(os.path.join(CHAIN, 'bom', '2026-current.json'), BOM)
    for t in FIN:
        dump(os.path.join(CHAIN, 'financials', t[0] + '.json'), fin(t))
    nm = merge_methods()
    print('관측 %d · 방법 %d · 주장 %d · 가설 %d · 재무 %d'
          % (len(O), nm, len(CLAIMS), len(HYP), len(FIN)))
