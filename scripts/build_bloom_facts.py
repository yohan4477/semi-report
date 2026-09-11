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
 ('o-amosense-share-2026q3', 'amosense-bloom-substrate', 'sourcing_volume_share', 15, None,
  None, PCT, '2026 Q3', '2026-07-01', '2026-09-30', '2026-09-11',
  'Bloom 1.2GW 가동률 기준 월 세라믹 기판 수요', 'CURRENT', 'ESTIMATED', 0.7,
  'method-amosense-share-1p2gw', ['sedaily_kr_suppliers'],
  '설비 능력에서 나온 값이다. 실제 가동률과 출하는 공개되지 않았다'),
 ('o-amosense-share-2026e', 'amosense-bloom-substrate', 'capacity_volume_share', 9, None, None,
  PCT, '2026E', '2026-01-01', '2026-12-31', '2026-09-11',
  'Bloom 2GW 최대 생산 기준 세라믹 기판 수요', 'CURRENT', 'ESTIMATED', 0.65,
  'method-amosense-share-2gw', ['sedaily_kr_suppliers'], '분모가 앞의 것과 다르다. 나란히 비교하지 않는다'),
 ('o-amosense-capa-2026q3', 'amosense-bloom-substrate', 'supplier_capacity', 600000, None, None,
  'sheets/month', '2026 Q3', '2026-07-01', '2026-09-30', '2026-07-29',
  'AMOsense 월 생산 능력', 'CURRENT', 'CONFIRMED', 0.9, None, ['sedaily_kr_suppliers'],
  '20만 장에서 60만 장으로 확대 계획'),
 ('o-amosense-share-2025', 'amosense-bloom-substrate', 'sourcing_volume_share', 0, None, None,
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
 ('o-aep-share-fy2025', 'bloom-aep', 'customer_revenue_share', 13, None, None, PCT, 'FY2025',
  '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL', 'ESTIMATED',
  0.75, 'method-aep-13', ['be_10k_fy2025', 'be_aep_1gw'],
  '2위 고객이 AEP 매입 법인이라는 가설. 확정이 아니다'),
 ('o-eternix-share-fy2025', 'bloom-eternix', 'customer_revenue_share', 12, None, None, PCT,
  'FY2025', '2025-01-01', '2025-12-31', '2026-02-09', 'Bloom FY2025 총매출', 'HISTORICAL',
  'ESTIMATED', 0.7, 'method-sk-12', ['be_10k_fy2025', 'be_sk_eternix_80mw'],
  '본사인지 프로젝트 법인인지도 확정되지 않았다'),
 ('o-be26c1-share-2026q2', 'bloom-be26c1', 'customer_revenue_share', 44, None, None, PCT,
  '2026 Q2', '2026-04-01', '2026-06-30', '2026-07-31', 'Bloom 2026 2분기 총매출', 'HISTORICAL',
  'UNDISCLOSED', None, None, ['be_10q_2026q2'], None),
 ('o-be26c1-share-2026h1', 'bloom-be26c1', 'customer_revenue_share', 73, None, None, PCT,
  '2026 H1', '2026-01-01', '2026-06-30', '2026-07-31', 'Bloom 2026 상반기 총매출', 'CURRENT',
  'UNDISCLOSED', None, None, ['be_10q_2026q2'],
  '비특수관계 고객 한 곳. SEC 가 법인명을 밝히지 않았다'),
 ('o-fundjv-share-2026q2', 'bloom-fundjv-sales', 'customer_revenue_share', 21, None, None, PCT,
  '2026 Q2', '2026-04-01', '2026-06-30', '2026-07-31', 'Bloom 2026 2분기 총매출', 'CURRENT',
  'ESTIMATED', 0.7, None, ['be_10q_2026q2'],
  '2분기 특수관계 고객이 브룩필드 계열 펀드 JV 와 맞아떨어진다'),
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
  1.0, None, ['be_equinix_100mw'], '약 75MW 가동 + 30MW 공사 중'),
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
 ('method-amosense-share-1p2gw', 'AMOsense 기판 물량 점유율 (1.2GW 가동률)',
  [('월 생산 능력', 600000, '장/월'),
   ('÷ 1.2GW 가동률 기준 월 수요 약 400만 장', 15, '%')],
  15, '%', 'Bloom 1.2GW 가동률 기준 월 세라믹 기판 수요', 'ESTIMATED',
  ['sedaily_kr_suppliers'],
  '기판 한 장을 25W 로 보는 가정에서 나온 수요다. 다른 자료는 1GW 당 3,000~3,300만 장으로 잡아 값이 달라진다'),
 ('method-amosense-share-2gw', 'AMOsense 기판 물량 점유율 (2GW 최대)',
  [('연 생산 능력', 7200000, '장/년'),
   ('÷ 2GW 최대 생산 기준 수요 약 6,670만 장', 9, '%')],
  9, '%', 'Bloom 2GW 최대 생산 기준 세라믹 기판 수요', 'ESTIMATED', ['sedaily_kr_suppliers'],
  '앞의 15% 와 분모가 다르다'),
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
 {'id': 'h-be25-2nd-aep', 'anon_company_id': 'be24_c2', 'candidate_company_id': 'aep',
  'period': 'FY2025', 'likelihood': 3.75, 'status': 'estimated',
  'method': '초기 100MW 에 MW 당 250~300만 달러를 곱하면 2.5~3.0억 달러로 13% 몫 2.63억 달러와 겹친다',
  'notes': '금액이 겹친다는 것이 법인 확인은 아니다'},
 {'id': 'h-be25-3rd-eternix', 'anon_company_id': 'be24_c3', 'candidate_company_id': 'sk-eternix',
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
  'bloom-energy', 'FY2025', 'ESTIMATED', 0.75, ['be_10k_fy2025', 'be_aep_1gw'], None),
 ('clm-eternix-12', 'FY2025 3위 고객 12% 는 SK 에너닉스 또는 그 프로젝트 법인일 수 있다.',
  'sk-eternix', 'bloom-energy', 'FY2025', 'ESTIMATED', 0.7, ['be_sk_eternix_80mw'], None),
 ('clm-cctc-share', 'CCTC 는 Bloom 전해질 세라믹의 주요 공급사이며 2026 조달 점유율은 75~80% 로 추정된다.',
  'cctc', 'bloom-energy', '2026E', 'ESTIMATED', 0.75, ['cctc_yicai'],
  '관계는 확인. 점유율은 2차 조사'),
 ('clm-amosense-15', 'AMOsense 의 세라믹 기판 물량 점유율은 Bloom 1.2GW 가동률 기준 약 15% 다.',
  'amosense', 'bloom-energy', '2026 Q3', 'ESTIMATED', 0.7, ['sedaily_kr_suppliers'],
  '월 60만 장 ÷ 추정 수요 400만 장'),
 ('clm-amosense-9', 'AMOsense 의 점유율은 Bloom 2GW 최대 생산 기준으로는 약 9% 다.',
  'amosense', 'bloom-energy', '2026E', 'ESTIMATED', 0.65, ['sedaily_kr_suppliers'],
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
]


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': t[15], 'source_ids': t[16], 'method_note': t[17]}


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
