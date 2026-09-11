# -*- coding: utf-8 -*-
"""전자부품 사슬 — 태양유전(TAIYO YUDEN).

Drive `value chain 분석/태양유전` 의 01~05 가 canonical 이다. 거기 있는 것만 옮긴다.
  01_태양유전 조사 추적과정            1GvZKsOg9IwZgIMWdjK4KXx03hwLldHYWOMqb7B-fFag
  02_TAIYO YUDEN 글로벌 Value Chain   1MN039e1vmXzklmAfiSFeYejzzbMCvISBZ0B8yg3q1fU
  03_태양유전 Evidence & Sources      1Yn0E4RBGoYVDTXSn_wbHbTNJGVfwjx9NNPlWG_y-xTg
  04_태양유전 Entities & Edges        1CAorm2tm51tuQd2VYQ90yF2I7dOOjinmNOxKpIkfJ-A
  05_태양유전 UIUX & Implementation Guide  1QyJAGldPsVKkEOQHluZLSsg8g2o1OkEaNb-spJWw91Q

NVIDIA·AWS 는 이미 다른 사슬(주로 nvidia 사슬)이 전역 엔티티로 갖고 있다. 그 둘은
ENTITIES 에 다시 넣지 않고 관계에서 id 만 참조한다 — 다시 넣으면 merge() 가 그 쪽
레코드를 얇은 버전으로 덮어쓴다. app-automotive 도 kr-substrate 사슬 소유라 같은
이유로 참조만 한다.

04 의 관측(O001~O011) 가운데 entity 전체 단위 절대값(O001 총매출, O009 출하량,
O010 BB 비율)은 이을 관계(edge)가 없어 관측이 아니라 CLAIMS 로 옮긴다 — 본보기
(build_substrate_vc.py)도 총매출 같은 값은 관측이 아니라 주장으로 남겼다.
O002~O008·O011 은 제품별·전방별 매출 축이라 nvidia 사슬의 SERVES_END_MARKET 관례를
그대로 써서 04 목록에 없는 매출원·전방 노드 6개(ty-rev-capacitor·ty-rev-inductor·
app-it-infra-industrial·app-communication·app-information-equipment·app-consumer)를
구조 보강으로 만든다. 값은 전부 04 표에 있는 값 그대로다 — 이 노드들은 그 값을
얹을 자리를 만들 뿐이다.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'taiyo-yuden')
TY = 'taiyo-yuden'

SOURCES = [
 ('ty_fin_2026', 'TAIYO YUDEN', 'Financial Statements', 'primary_official', '2026-03-31',
  'https://www.yuden.co.jp/en/ir/financial/financial_data.html',
  'FY2026(2026년 3월 결산) 매출 355,341백만엔·매출원가 273,412백만엔·매출총이익 81,928백만엔'),
 ('ty_product_2026', 'TAIYO YUDEN', '연차 주주 자료 — 제품별 매출', 'primary_official', '2026',
  'https://www.yuden.co.jp/en/ir/financial/summary.html',
  'FY2026 Capacitors 251,771백만엔(70.9%)·Inductors 64,319백만엔(18.1%)·'
  'Integrated Modules & Devices 14,796백만엔(4.2%)·Others 24,453백만엔(6.9%). '
  '제품·매출 축이며 고객 비중 축이 아니다'),
 ('ty_forecast_2027', 'TAIYO YUDEN', 'Forecasts', 'primary_official', '2026-08-05',
  'https://www.yuden.co.jp/en/ir/financial/achievement_forecast.html',
  'FY2027 전망 매출 424,000백만엔·영업이익 45,000백만엔'),
 ('ty_procurement', 'TAIYO YUDEN', 'CSR Procurement', 'primary_official', '2025',
  'https://www.yuden.co.jp/en/sustainability/society/procurement/initiative/',
  '공급사 약 2,600개, 2025년 관리 대상 중요 공급사 약 500개. 개별 실명·구매비중은 비공개'),
 ('ty_material_risk', 'TAIYO YUDEN', 'Business Risks', 'primary_official', None,
  'https://www.yuden.co.jp/en/ir/management/risk.html',
  '일부 원재료는 특정 공급사 의존도가 높고 장기공급계약으로 조달한다고 회사가 공시. '
  '실명·비중은 비공개(원표기: current disclosure)'),
 ('ty_internal_material', 'TAIYO YUDEN', 'Management System Certification Status',
  'primary_official', '2026-08',
  'https://www.yuden.co.jp/en/sustainability/society/QA/certification/',
  'Haruna·Yawatabara 세라믹 분말, Nakanojo 인덕터 코어·분말, '
  'TY Chemical Technology 도금 — 수직계열화의 핵심 근거'),
 ('ty_capacity', 'TAIYO YUDEN', 'Integrated Report 2025', 'primary_official', '2025',
  'https://www.yuden.co.jp/en/ir/2025ar/',
  '중국·말레이시아 신규 MLCC 공장 증설, 자동차·AI 서버향 대형·고용량 제품에 투자 초점 이동'),
 ('apple_supplier', 'Apple', 'Apple Supplier List', 'primary_company', '2024',
  'https://www.supplychainreports.apple/files/doc_downloads/2024/04/Apple-Supplier-List.pdf',
  '태양유전이 명단에 오르고 중국·일본·말레이시아·필리핀·한국 제조지역이 함께 공개된다. '
  '매출 비중과 결제 경로는 비공개'),
 ('apple_tf', 'TrendForce', 'Apple 향 MLCC 생산 보도', 'industry_research', None,
  'https://www.trendforce.com/research/download/RP240711DB',
  '태양유전 라인이 Apple·아이폰 수요향 MLCC 를 만든다고 보도. 2024-07·2025-10 두 시점 '
  '자료다(원표기: CONFIRMED industry evidence)'),
 ('ty_auto_tier1', 'TAIYO YUDEN', 'Integrated Report / CEO 자료', 'primary_official', None,
  'https://www.yuden.co.jp/en/ir/',
  '유럽·미국·중국·한국·일본 주요 1차 협력사와 폭넓게 거래한다고 공시. 개별 실명은 '
  '비공개(원표기: company disclosure)'),
 ('ty_ledger_04', u'조사 원장', u'04 Entities & Edges · 03 Evidence & Sources (Drive)',
  'research_ledger', None, None,
  u'공식 유통 파트너 목록과 FY2027 1분기 전방별 매출 비중이 원장에 E015~E017·O002~O008 로 '
  u'적혀 있다. 개별 공시 번호는 원장에만 있고 공개 주소로는 아직 못 박았다'),
 ('vw_qual', 'TAIYO YUDEN', '제품 뉴스 — VW80808 인증', 'primary_company', None,
  'https://www.yuden.co.jp/en/news/',
  '일부 자동차용 MLCC 가 VW80808 인증을 받았다. 직접고객·매출 관계의 근거는 '
  '아니다(원표기: current product release)'),
 ('ai_tf_20260728', 'TrendForce', '2026년 6월 MLCC 출하 보도', 'industry_research',
  '2026-07-28', 'https://www.trendforce.com/presscenter/news/20260728-13155.html',
  '2026년 6월 태양유전 MLCC 출하 약 400억 개, 5년래 월간 최고. AI TPU·Trainium 수요를 '
  '원인으로 든다. 출하량이지 매출 비중이 아니다(원표기: CONFIRMED industry estimate)'),
 ('ai_bb_202607', 'TrendForce', '2026년 6월 말 BB 비율 보도', 'industry_research',
  '2026-07-06', 'https://www.trendforce.com/presscenter/news/20260706-13136.html',
  '2026년 6월 말 기준 태양유전 BB 비율 1.25. 회사 분기 실적 자료의 BB 정의·기간과 '
  '다르므로 섞지 않는다(원표기: CONFIRMED industry estimate)'),
 ('ai_platform', 'TrendForce · TAIYO YUDEN', 'AI 플랫폼 수요 연결', 'industry_research',
  None, 'https://www.trendforce.com/presscenter/',
  'NVIDIA·Google·AWS 는 AI 플랫폼 수요 노출 노드일 뿐 확인된 직접고객이 아니다. 매출 '
  '배분은 비공개(원표기: INFERRED topology, 시점 2026 current)'),
 ('sakai_hist', '학계 기술 자료', 'Sakai Chemical BT04 BaTiO3 연구 사례', 'industry_research',
  None, None,
  '과거 태양유전 관련 MLCC 연구에 쓰인 사례일 뿐 현재 공급사임을 확인해 주지 않는다'
  '(원표기: HISTORICAL_CURRENT_UNKNOWN)'),
 ('ai_share_scenario', '자체 민감도 모델', 'AI 매출 노출 시나리오', 'analyst_estimate', None,
  None,
  'IT Infrastructure/Industrial 27% 가운데 AI 비중을 40/50/60%로 가정하면 회사 매출 '
  '노출은 10.8/13.5/16.2%. 시나리오일 뿐 공식치가 아니다(원표기: ESTIMATED, '
  '시점 FY2027 Q1 vicinity)'),
]

# (id, 이름, 한국어, 유형, 나라, 갈래, 메모)
ENTITIES = [
 (TY, 'TAIYO YUDEN CO., LTD.', '태양유전', 'company', '일본', ['Electronic components'],
  'MLCC 를 중심으로 소재·공정·생산기술을 안에 갖춘 전자부품 회사다(04의 TY)'),
 # 내부 소재·공정 계열사·공장
 ('taiyo-yuden-chemical-technology', 'TAIYO YUDEN CHEMICAL TECHNOLOGY CO., LTD.',
  '태양유전 케미컬 테크놀로지', 'company', '일본', ['Plating'],
  '전자부품 도금을 맡는 자회사다(04의 TY_CHEM)'),
 ('taiyo-yuden-haruna-plant', 'TAIYO YUDEN CO., LTD. Haruna Plant', '하루나 공장',
  'company', '일본', ['Ceramic powder'],
  'MLCC 용 세라믹 분말을 만든다. IATF 인증 공정을 포함한다(04의 TY_HARUNA)'),
 ('taiyo-yuden-yawatabara-plant', 'TAIYO YUDEN CO., LTD. Yawatabara Plant', '야와타바라 공장',
  'company', '일본', ['Ceramic powder'],
  'MLCC 용 세라믹 분말을 만든다. IATF 인증 공정을 포함한다(04의 TY_YAWATABARA)'),
 ('taiyo-yuden-nakanojo-plant', 'TAIYO YUDEN CO., LTD. Nakanojo Plant', '나카노조 공장',
  'company', '일본', ['Inductor material'],
  '인덕터용 코어·분말을 만든다(04의 TY_NAKANOJO)'),
 # 생산 자회사
 ('niigata-taiyo-yuden', 'NIIGATA TAIYO YUDEN CO., LTD.', '니가타 태양유전', 'company',
  '일본', ['MLCC manufacturing'], 'MLCC 를 생산하는 자회사다(04의 TY_NIIGATA)'),
 ('korea-kyongnam-taiyo-yuden', 'KOREA KYONG NAM TAIYO YUDEN CO., LTD.', '한국경남태양유전',
  'company', '한국', ['MLCC manufacturing'], 'MLCC 를 생산하는 한국 자회사다(04의 TY_KOREA)'),
 ('taiyo-yuden-guangdong', 'TAIYO YUDEN (GUANGDONG) CO., LTD.', '태양유전 광둥', 'company',
  '중국', ['MLCC manufacturing'], 'MLCC 와 파워인덕터를 함께 생산한다(04의 TY_GD)'),
 ('taiyo-yuden-changzhou', 'TAIYO YUDEN (CHANGZHOU) CO., LTD.', '태양유전 창저우', 'company',
  '중국', ['MLCC manufacturing'], '새로 늘린 MLCC 생산능력을 맡는다(04의 TY_CZ)'),
 ('taiyo-yuden-sarawak', 'TAIYO YUDEN (SARAWAK) SDN. BHD.', '태양유전 사라왁', 'company',
  '말레이시아', ['MLCC manufacturing'], '새로 늘린 MLCC 생산능력을 맡는다(04의 TY_SARAWAK)'),
 # 다운스트림 — NVIDIA·AWS 는 다른 사슬이 이미 가진 전역 엔티티라 여기서 다시 안 넣는다
 ('apple', 'Apple Inc.', '애플', 'company', '미국', ['End customer'],
  'Apple 공급사 명단에 태양유전이 올라 있다. 매출 비중은 공개되지 않았다(04의 APPLE)'),
 ('volkswagen', 'Volkswagen AG', '폭스바겐', 'company', '독일', ['Automotive'],
  'VW80808 인증을 받았을 뿐 직접고객·매출 관계의 근거는 아니다(04의 VW)'),
 ('google', 'Google LLC', '구글', 'company', '미국', ['AI platform'],
  'TPU 수요가 고사양 MLCC 를 늘린다. 태양유전과 직접 거래를 확인할 근거는 없다(04의 GOOGLE)'),
 ('arrow-electronics', 'Arrow Electronics, Inc.', '애로우 일렉트로닉스', 'company', '미국',
  ['Distributor'], '공식 인증 유통 파트너다(04의 ARROW)'),
 ('avnet', 'Avnet, Inc.', '애브넷', 'company', '미국', ['Distributor'],
  '공식 인증 유통 파트너다(04의 AVNET)'),
 ('mouser-electronics', 'Mouser Electronics, Inc.', '마우저 일렉트로닉스', 'company', '미국',
  ['Distributor'], '공식 인증 유통 파트너다(04의 MOUSER)'),
 # 구조 보강 — 04 원 목록에는 없다. O002~O008·O011 을 얹을 매출원·전방 노드
 ('ty-rev-capacitor', 'Capacitors', '커패시터 매출', 'revenue_type', None, ['Revenue type'],
  'FY2026 매출의 70.9%. MLCC 가 중심이다'),
 ('ty-rev-inductor', 'Inductors', '인덕터 매출', 'revenue_type', None, ['Revenue type'],
  'FY2026 매출의 18.1%. 페라이트·금속 파워인덕터가 중심이다'),
 ('app-it-infra-industrial', 'IT Infrastructure / Industrial', 'IT 인프라·산업용',
  'application', None, ['Application'],
  'AI 서버를 포함한 서버·통신인프라·산업용을 함께 묶은 분류다. AI 전용 매출만 '
  '떼어내지 않는다'),
 ('app-communication', 'Communication', '통신', 'application', None, ['Application'], None),
 ('app-information-equipment', 'Information Equipment', '정보기기', 'application', None,
  ['Application'], None),
 ('app-consumer', 'Consumer', '소비자가전', 'application', None, ['Application'], None),
]

REGION = {'한국': 'Korea', '일본': 'Japan', '대만': 'Taiwan', '중국': 'China',
          '미국': 'North America', '독일': 'Europe', '말레이시아': 'Southeast Asia'}

# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence_level, src_tier, tgt_tier, sources, notes)
R = [
 # ── 내부 소재·공정 계열화(04 의 lane=UPSTREAM/INTERNAL 을 한데 CORPORATE 로 묶는다)──
 ('haruna-ceramic-powder', 'taiyo-yuden-haruna-plant', TY, 'INTERNAL_MATERIAL_SUPPLY',
  'CORPORATE', 'Ceramic powder', '세라믹 분말', '내부 생산', '본사', None, None, 'ACTIVE',
  'CONFIRMED', None, None, ['ty_internal_material'], '그룹 안 공정이다(04의 E001·신뢰도 0.95)'),
 ('yawatabara-ceramic-powder', 'taiyo-yuden-yawatabara-plant', TY, 'INTERNAL_MATERIAL_SUPPLY',
  'CORPORATE', 'Ceramic powder', '세라믹 분말', '내부 생산', '본사', None, None, 'ACTIVE',
  'CONFIRMED', None, None, ['ty_internal_material'], '그룹 안 공정이다(04의 E002·신뢰도 0.95)'),
 ('tychem-plating', 'taiyo-yuden-chemical-technology', TY, 'PROCESSING', 'CORPORATE',
  'Plating', '전자부품 도금', '내부 생산', '본사', None, None, 'ACTIVE', 'CONFIRMED', None,
  None, ['ty_internal_material'], '자회사가 맡는 도금 공정이다(04의 E003·신뢰도 0.95)'),
 ('nakanojo-inductor-material', 'taiyo-yuden-nakanojo-plant', TY, 'INTERNAL_MATERIAL_SUPPLY',
  'CORPORATE', 'Inductor material', '인덕터 코어·분말', '내부 생산', '본사', None, None,
  'ACTIVE', 'CONFIRMED', None, None, ['ty_internal_material'],
  '그룹 안 소재 공정이다(04의 E004·신뢰도 0.95)'),
 ('niigata-mlcc', 'niigata-taiyo-yuden', TY, 'MANUFACTURES', 'CORPORATE',
  'MLCC manufacturing', 'MLCC', '생산 자회사', '본사', None, None, 'ACTIVE', 'CONFIRMED',
  None, None, ['ty_capacity'], '생산 자회사다(04의 E005·신뢰도 0.98)'),
 ('korea-mlcc', 'korea-kyongnam-taiyo-yuden', TY, 'MANUFACTURES', 'CORPORATE',
  'MLCC manufacturing', 'MLCC', '생산 자회사', '본사', None, None, 'ACTIVE', 'CONFIRMED',
  None, None, ['ty_capacity'], '생산 자회사다(04의 E006·신뢰도 0.98)'),
 ('guangdong-mlcc', 'taiyo-yuden-guangdong', TY, 'MANUFACTURES', 'CORPORATE',
  'MLCC manufacturing', 'MLCC·파워인덕터', '생산 자회사', '본사', None, None, 'ACTIVE',
  'CONFIRMED', None, None, ['ty_capacity'], '생산 자회사다(04의 E007·신뢰도 0.98)'),
 ('changzhou-mlcc', 'taiyo-yuden-changzhou', TY, 'MANUFACTURES', 'CORPORATE',
  'MLCC manufacturing', 'MLCC', '생산 자회사', '본사', '2023', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['ty_capacity'], '새로 늘린 생산능력이다(04의 E008·신뢰도 0.98)'),
 ('sarawak-mlcc', 'taiyo-yuden-sarawak', TY, 'MANUFACTURES', 'CORPORATE',
  'MLCC manufacturing', 'MLCC', '생산 자회사', '본사', '2023', None, 'ACTIVE', 'CONFIRMED',
  None, None, ['ty_capacity'], '새로 늘린 생산능력이다(04의 E009·신뢰도 0.98)'),
 # ── 다운스트림 ───────────────────────────────────────────────────
 ('ty-apple-supply-chain', TY, 'apple', 'END_CUSTOMER_SUPPLY_CHAIN', 'DOWNSTREAM',
  'End customer', '전자부품·MLCC 공급망', '공급망', '고객', '2024', None, 'ACTIVE',
  'CONFIRMED', None, 'CONTRACTUAL_CUSTOMER', ['apple_supplier', 'apple_tf'],
  'Apple 공급사 명단에 오른 관계다. 매출 비중은 공개되지 않았다(04의 E010·신뢰도 0.9)'),
 ('ty-vw-qualification', TY, 'volkswagen', 'QUALIFICATION', 'DOWNSTREAM', 'Automotive',
  '자동차용 MLCC·VW80808 인증', '인증', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'END_USER', ['vw_qual'], '인증일 뿐 직접고객 관계의 근거는 아니다(04의 E011·신뢰도 0.85)'),
 ('ty-nvidia-platform-exposure', TY, 'nvidia', 'PLATFORM_EXPOSURE', 'DOWNSTREAM',
  'AI platform', 'AI 서버향 MLCC 수요', '수요 노출', '플랫폼', '2026', None, 'ACTIVE',
  'INFERRED', None, 'END_USER', ['ai_platform'], '직접 구매 근거는 없다(04의 E012·신뢰도 0.55)'),
 ('ty-google-platform-exposure', TY, 'google', 'PLATFORM_EXPOSURE', 'DOWNSTREAM',
  'AI platform', 'TPU 향 고사양 MLCC 수요', '수요 노출', '플랫폼', '2026', None, 'ACTIVE',
  'INFERRED', None, 'END_USER', ['ai_platform', 'ai_tf_20260728'],
  'TrendForce 가 수요 연결고리로 짚었을 뿐 직접 구매 근거는 없다(04의 E013·신뢰도 0.6)'),
 ('ty-aws-platform-exposure', TY, 'aws', 'PLATFORM_EXPOSURE', 'DOWNSTREAM', 'AI platform',
  'Trainium 향 고사양 MLCC 수요', '수요 노출', '플랫폼', '2026', None, 'ACTIVE', 'INFERRED',
  None, 'END_USER', ['ai_platform', 'ai_tf_20260728'],
  'TrendForce 가 수요 연결고리로 짚었을 뿐 직접 구매 근거는 없다(04의 E014·신뢰도 0.6)'),
 ('ty-arrow-distribution', TY, 'arrow-electronics', 'DISTRIBUTION_PARTNERSHIP', 'DOWNSTREAM',
  'Distributor', '전자부품 유통', '유통', '유통사', None, None, 'ACTIVE', 'CONFIRMED', None,
  'INTERMEDIARY', ['ty_ledger_04'], '공식 인증 유통사다(04의 E015·신뢰도 0.95). 03 표에 개별 출처 번호가 없다'),
 ('ty-avnet-distribution', TY, 'avnet', 'DISTRIBUTION_PARTNERSHIP', 'DOWNSTREAM',
  'Distributor', '전자부품 유통', '유통', '유통사', None, None, 'ACTIVE', 'CONFIRMED', None,
  'INTERMEDIARY', ['ty_ledger_04'], '공식 인증 유통사다(04의 E016·신뢰도 0.95). 03 표에 개별 출처 번호가 없다'),
 ('ty-mouser-distribution', TY, 'mouser-electronics', 'DISTRIBUTION_PARTNERSHIP', 'DOWNSTREAM',
  'Distributor', '전자부품 유통', '유통', '유통사', None, None, 'ACTIVE', 'CONFIRMED', None,
  'INTERMEDIARY', ['ty_ledger_04'], '공식 인증 유통사다(04의 E017·신뢰도 0.95). 03 표에 개별 출처 번호가 없다'),
 # ── 구조 보강: 제품·전방 매출 축(04 원 목록에는 없다. O002~O008·O011 을 얹는 자리)──
 ('ty-rev-capacitor-edge', TY, 'ty-rev-capacitor', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '커패시터', '본사', '매출원', None, None, 'ACTIVE', 'CONFIRMED', None,
  'REVENUE_TYPE', ['ty_product_2026'], 'FY2026 제품별 매출 축이다'),
 ('ty-rev-inductor-edge', TY, 'ty-rev-inductor', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '인덕터', '본사', '매출원', None, None, 'ACTIVE', 'CONFIRMED', None,
  'REVENUE_TYPE', ['ty_product_2026'], 'FY2026 제품별 매출 축이다'),
 ('ty-app-it-infra-industrial', TY, 'app-it-infra-industrial', 'SERVES_END_MARKET',
  'DOWNSTREAM', 'Application', 'IT 인프라·산업용', '본사', '전방', None, None, 'ACTIVE',
  'CONFIRMED', None, 'END_USER', ['ty_ledger_04'],
  'FY2027 1분기 전방별 매출 비중이다. 03 표에 개별 출처 번호가 없다'),
 ('ty-app-automotive', TY, 'app-automotive', 'SERVES_END_MARKET', 'DOWNSTREAM',
  'Application', '자동차', '본사', '전방', None, None, 'ACTIVE', 'CONFIRMED', None, 'END_USER',
  ['ty_ledger_04'], 'FY2027 1분기 전방별 매출 비중이다. 03 표에 개별 출처 번호가 없다'),
 ('ty-app-communication', TY, 'app-communication', 'SERVES_END_MARKET', 'DOWNSTREAM',
  'Application', '통신', '본사', '전방', None, None, 'ACTIVE', 'CONFIRMED', None, 'END_USER',
  ['ty_ledger_04'], 'FY2027 1분기 전방별 매출 비중이다. 03 표에 개별 출처 번호가 없다'),
 ('ty-app-information-equipment', TY, 'app-information-equipment', 'SERVES_END_MARKET',
  'DOWNSTREAM', 'Application', '정보기기', '본사', '전방', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'END_USER', ['ty_ledger_04'], 'FY2027 1분기 전방별 매출 비중이다. 03 표에 개별 출처 번호가 없다'),
 ('ty-app-consumer', TY, 'app-consumer', 'SERVES_END_MARKET', 'DOWNSTREAM', 'Application',
  '소비자가전', '본사', '전방', None, None, 'ACTIVE', 'CONFIRMED', None, 'END_USER', ['ty_ledger_04'],
  'FY2027 1분기 전방별 매출 비중이다. 03 표에 개별 출처 번호가 없다'),
]

PCT = 'percent'
FY26_START, FY26_END = '2025-04-01', '2026-03-31'
Q1FY27_START, Q1FY27_END = '2026-04-01', '2026-06-30'

# (id, rel, metric, value, low, high, unit, period, p_start, p_end, as_of,
#  denominator, status, evidence_level, confidence, method_id, sources, note)
O = [
 ('o-ty-capacitor-share', 'ty-rev-capacitor-edge', 'capacitor_revenue_share', 70.9, None,
  None, PCT, 'FY2026', FY26_START, FY26_END, FY26_END, '회사 총매출', 'CURRENT',
  'CONFIRMED', None, None, ['ty_product_2026'], '251,771백만엔(04의 O002)'),
 ('o-ty-inductor-share', 'ty-rev-inductor-edge', 'inductor_revenue_share', 18.1, None,
  None, PCT, 'FY2026', FY26_START, FY26_END, FY26_END, '회사 총매출', 'CURRENT',
  'CONFIRMED', None, None, ['ty_product_2026'], '64,319백만엔(04의 O003)'),
 ('o-ty-it-infra-share', 'ty-app-it-infra-industrial', 'IT_infra_industrial_share', 27,
  None, None, PCT, 'FY2027 Q1', Q1FY27_START, Q1FY27_END, Q1FY27_END,
  '분기 회사 매출(전방별 분류)', 'CURRENT', 'CONFIRMED', None, None, [],
  'AI 서버를 포함한 서버·통신인프라·산업용 전체를 묶은 수치다. AI 전용 매출이 아니다'
  '(04의 O004)'),
 ('o-ty-automotive-share', 'ty-app-automotive', 'automotive_share', 28, None, None, PCT,
  'FY2027 Q1', Q1FY27_START, Q1FY27_END, Q1FY27_END, '분기 회사 매출(전방별 분류)',
  'CURRENT', 'CONFIRMED', None, None, [], '(04의 O005)'),
 ('o-ty-communication-share', 'ty-app-communication', 'communication_share', 20, None,
  None, PCT, 'FY2027 Q1', Q1FY27_START, Q1FY27_END, Q1FY27_END, '분기 회사 매출(전방별 분류)',
  'CURRENT', 'CONFIRMED', None, None, [], '(04의 O006)'),
 ('o-ty-info-equip-share', 'ty-app-information-equipment', 'information_equipment_share',
  18, None, None, PCT, 'FY2027 Q1', Q1FY27_START, Q1FY27_END, Q1FY27_END,
  '분기 회사 매출(전방별 분류)', 'CURRENT', 'CONFIRMED', None, None, [], '(04의 O007)'),
 ('o-ty-consumer-share', 'ty-app-consumer', 'consumer_share', 7, None, None, PCT,
  'FY2027 Q1', Q1FY27_START, Q1FY27_END, Q1FY27_END, '분기 회사 매출(전방별 분류)',
  'CURRENT', 'CONFIRMED', None, None, [], '(04의 O008)'),
 ('o-ty-ai-exposure-scenario', 'ty-app-it-infra-industrial', 'AI_revenue_exposure_scenario',
  13.5, 10.8, 16.2, PCT, 'FY2027 Q1 vicinity', Q1FY27_START, Q1FY27_END, Q1FY27_END,
  '회사 매출', 'CURRENT', 'ESTIMATED', None,
  '27% IT/industrial × AI 비중 40/50/60% 가정',
  ['ai_share_scenario'],
  '시나리오일 뿐 실제 AI 전용 매출은 공개되지 않는다(04의 O011)'),
]

CLAIMS = [
 ('clm-ty-revenue-fy2026',
  '태양유전의 FY2026(2026년 3월 결산) 매출은 355,341백만엔, 매출원가는 273,412백만엔, '
  '매출총이익은 81,928백만엔이다.', TY, None, 'FY2026', 'CONFIRMED', None, ['ty_fin_2026'],
  '매출총이익률은 약 23.1%다. FY2025(2025년 3월 결산) 매출은 341,438백만엔·'
  '매출원가는 269,867백만엔이었다(04의 O001)'),
 ('clm-ty-forecast-fy2027',
  '태양유전은 FY2027(2027년 3월 결산) 매출 424,000백만엔·영업이익 45,000백만엔을 '
  '전망한다(2026-08-05 발표).', TY, None, 'FY2027', 'CONFIRMED', None, ['ty_forecast_2027'],
  'FY2027 1분기 매출은 939억 엔이며 회사는 AI 서버 수요를 핵심 성장동인으로 꼽는다'),
 ('clm-ty-product-mix',
  'FY2026 제품별 매출은 Capacitors 251,771백만엔(70.9%)·Inductors 64,319백만엔(18.1%)·'
  'Integrated Modules & Devices 14,796백만엔(4.2%)·Others 24,453백만엔(6.9%)이다.', TY,
  None, 'FY2026', 'CONFIRMED', None, ['ty_product_2026'],
  'Integrated Modules·Others 두 갈래는 04 표에 관측 번호가 없어 관측이 아니라 이 '
  '주장으로만 남긴다'),
 ('clm-ty-vertical-integration',
  '태양유전은 Haruna·Yawatabara 공장의 세라믹 분말, Nakanojo 공장의 인덕터 코어·분말, '
  'TY Chemical Technology 의 도금까지 소재·공정을 그룹 안에 갖췄다.', TY, None, None,
  'CONFIRMED', None, ['ty_internal_material'],
  '외부 분말 공급사에서 사들여 최종 조립만 한다는 단순한 구조가 아니다'),
 ('clm-ty-supplier-undisclosed',
  '태양유전은 약 2,600개 공급사와 거래하고 2025년 중요 공급사 약 500개를 관리하지만 '
  '개별 핵심 원재료 공급사의 실명·구매비중은 공개하지 않는다.', TY, None, '2025',
  'CONFIRMED', None, ['ty_procurement', 'ty_material_risk'],
  '일부 원재료는 특정 공급사 의존도가 높아 장기공급계약으로 조달한다고만 밝힌다'),
 ('clm-ty-candidates-excluded',
  'Sumitomo Metal Mining 등 니켈·BaTiO3 계열 업체는 제품 정합성만 있는 산업 후보일 뿐 '
  '태양유전과의 직접 거래 근거가 없어 공급사 노드로 넣지 않는다.', TY, None, '2026',
  'INFERRED', None, ['ty_material_risk'],
  '근거 없는 공급사 이름을 그래프에 올리지 않는다는 원칙을 지킨 결과다'),
 ('clm-ty-sakai-historical',
  'Sakai Chemical BT04 BaTiO3 는 과거 태양유전 관련 MLCC 연구에 쓰인 사례일 뿐 현재 '
  '공급사 관계를 확인해 주지 않는다.', TY, None, None, 'HISTORICAL_CURRENT_UNKNOWN', None,
  ['sakai_hist'], None),
 ('clm-ty-shipments-202606',
  '2026년 6월 태양유전 MLCC 출하는 약 400억 개로 5년래 월간 최고치다.', TY, None,
  '2026-06', 'CONFIRMED', None, ['ai_tf_20260728'],
  'TrendForce 조사 기준 산업 추정치다. 회사 분기 실적의 수주·출하 지표와 정의가 다르다'
  '(원표기: CONFIRMED industry estimate · 04의 O009)'),
 ('clm-ty-bb-ratio-202606',
  '2026년 6월 말 기준 태양유전 BB(수주잔고) 비율은 1.25배다.', TY, None, '2026-06',
  'CONFIRMED', None, ['ai_bb_202607'],
  'TrendForce 조사 기준 산업 추정치이며 회사 분기 실적 자료의 BB 지표와는 정의·기간이 '
  '달라 섞지 않는다(원표기: CONFIRMED industry estimate · 04의 O010)'),
 # 시장 점유율(Murata 약 40%·삼성전기 23~25% 등)은 02 본문에만 있고 03 표에 출처
 # 번호가 없다. 근거 없는 숫자를 주장으로 세우지 않는다 — 03 에 출처가 붙으면 넣는다
 ('clm-ty-ai-exposure-scenario',
  'IT 인프라·산업용 27% 가운데 AI 서버 비중을 40/50/60%로 가정하면 회사 매출 노출은 '
  '10.8/13.5/16.2%로 추정된다. 실제 AI 전용 매출은 공개되지 않는다.', TY, None,
  'FY2027 Q1 vicinity', 'ESTIMATED', None, ['ai_share_scenario'],
  '시나리오일 뿐 확정치가 아니다(04의 O011)'),
]


def ent(t):
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
            'legal_name': t[1], 'display_name': t[2] or t[1],
            'region': REGION.get(t[4]) if t[4] else None, 'parent_entity_id': None,
            'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
            'country': t[4], 'categories': t[5], 'desc': t[6], 'anon': False}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-11', 'note': t[6]}


def rel(t):
    return {'id': t[0], 'source_entity': t[1], 'target_entity': t[2],
            'relationship_type': t[3], 'lane': t[4], 'subsystem': t[5], 'component': t[6],
            'source_role': t[7], 'target_role': t[8], 'valid_from': t[9], 'valid_to': t[10],
            'status': t[11], 'evidence_level': t[12],
            'source_tier': t[13], 'target_tier': t[14],
            'economic_importance': None, 'capacity_criticality': None,
            'integration_criticality': None,
            'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium'}.get(t[12], 'low'),
            'flows': [], 'source_ids': t[15], 'notes': t[16]}


SRC_DATE = dict((x[0], x[4]) for x in SOURCES)


def obs(t):
    return {'id': t[0], 'relationship_id': t[1], 'metric': t[2], 'value': t[3],
            'value_low': t[4], 'value_high': t[5], 'unit': t[6], 'period': t[7],
            'period_start': t[8], 'period_end': t[9], 'as_of_date': t[10],
            'denominator': t[11], 'status': t[12], 'evidence_level': t[13],
            'confidence': t[14], 'method_id': None, 'method_note': t[15],
            'source_ids': t[16], 'denominator_scope': 'EDGE',
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
            out.append({'id': 'ty-e%03d' % n, 'relationship_id': t[0], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if t[12] == 'CONFIRMED' else 'indirect',
                        'evidence': t[16] or '', 'hypothesis_id': None})
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'ty-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid, 'evidence_type': 'direct',
                        'evidence': t[17] or '', 'hypothesis_id': None})
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print('전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d · 주장 %d'
          % (ne, ns, len(R), len(O), len(CLAIMS)))

    # 재료를 다시 쌓았으면 v2 꼴로 바로 옮긴다 — 옮기는 일을 사람 손에 맡기면
    # 다음 build 때 공급원·매출원이 상자로 되살아난다(프레임워크 §13)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
