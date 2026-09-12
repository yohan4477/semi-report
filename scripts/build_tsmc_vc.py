# -*- coding: utf-8 -*-
u"""파운드리 사슬 — TSMC. 앞단(공급)과 뒷단(고객)을 한 사슬로 세운다.

원문은 data/valuechain/reports/tsmc-밸류체인-조사-2026-09-12.md 하나다. 거기 없는 숫자·
회사·관계는 넣지 않는다. 원문의 근거 등급 A/B/C 를 evidence_level 로 옮긴다 —
A → CONFIRMED, B → ESTIMATED, C → INFERRED. 원문이 「미공개」라 적은 비중은 값을 비우고
UNDISCLOSED 잔여로 닫는다. 원문에 주소가 없어 출처 url 은 전부 None 이다.

  · 이미 전역에 선 상자(tsmc·apple·nvidia·amd·marvell·mediatek·intel·google·aws·
    microsoft·meta·oracle·coreweave·foxconn·quanta-computer·wistron·sk-hynix·
    samsung-electronics·micron·ajinomoto-fine-techno·amkor-korea)는 다시 넣지 않는다.
    merge() 가 저쪽 레코드를 얇은 버전으로 덮어쓴다. 미국 Amkor 본사는 한국 법인
    amkor-korea 와 다른 법인이라 amkor 로 새로 세운다.
  · 공급 품목은 상자가 아니라 분류다. 관계가 supply_source_ids 로 가리키고
    apply_supply_classes() 가 분류 레지스트리에 한국어 이름표와 비중을 얹는다.
  · 1위·2위 고객은 20-F 가 비중만 밝히고 실명을 적지 않아 익명 상자로 세운다.
    애플·엔비디아 실명 관계에는 비중 값을 적지 않는다 — 원문이 확정 불가라 했다.
  · HBM 3사는 TSMC 공급사가 아니라 TSMC 고객(엔비디아)의 병렬 공급사다. 타겟에 안 닿는
    상자로 앉힌다.
  · 프로젝트 테두리는 없다. projects.json 은 빈 목록이다.
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'tsmc')
TS = 'tsmc'
ACCESSED = '2026-09-12'

REGION = {u'미국': u'미국', u'일본': 'Asia', u'대만': 'Asia', u'한국': 'Asia',
          u'중국': 'Asia', u'독일': 'Europe', u'네덜란드': 'Europe', u'프랑스': 'Europe',
          u'독일·미국': 'Europe'}

# ── 레인·층·관계 종류 ────────────────────────────────────────────────
LB, LE, LO, LD, LC = ('MANUFACTURING_BOM', 'MANUFACTURING_EQUIPMENT',
                      'OPERATIONAL_INPUT', 'DOWNSTREAM', 'CORPORATE')
RAW, MP, CS, SM = ('RAW_MATERIAL', 'MATERIAL_PROCESSING', 'COMPONENT_SUPPLIER',
                   'SUBSYSTEM_MODULE')
CC, INT, EU = 'CONTRACTUAL_CUSTOMER', 'INTERMEDIARY', 'END_USER'

# ── 공급원 분류 id ──────────────────────────────────────────────────
SS_WAFER = 'ss-silicon-wafer'
SS_CHEM = 'ss-chemicals'
SS_PR = 'ss-photoresist'
SS_GAS = 'ss-specialty-gas'
SS_CMP = 'ss-cmp-materials'
SS_EQ = 'ss-equipment'
SS_BLANK = 'ss-mask-blank-pellicle'
SS_ABF = 'ss-abf-cowos'
SS_UTIL = 'ss-utility'
SS_MEM = 'ss-memory'

# ── 매출원 분류 id ──────────────────────────────────────────────────
RT_HPC = 'rt-tsmc-rev-hpc'
RT_SP = 'rt-tsmc-rev-smartphone'
RT_IOT = 'rt-tsmc-rev-iot'
RT_AUTO = 'rt-tsmc-rev-automotive'
RT_DCE = 'rt-tsmc-rev-dce'
RT_ETC = 'rt-tsmc-rev-other'

L = 'tsmc_report_2026_09_12'
F20 = 'tsmc_20f_2025'
AR25 = 'tsmc_ar_2025'
AR22 = 'tsmc_ar_2022'
F05 = 'tsmc_20f_2005'

# ── 출처 — 조사 원장 하나에 원문이 이름을 댄 공시를 곁들인다. url 은 원문에 없다 ──
# (id, publisher, title, source_type, published_date, note)
SOURCES = [
 (L, u'조사 원장', u'TSMC 밸류체인 조사 — 앞단/뒷단', 'research_ledger', '2026-09-12',
  u'저장소 data/valuechain/reports/tsmc-밸류체인-조사-2026-09-12.md. 근거 등급 A/B/C 가 '
  u'절마다 붙어 있고 이 사슬의 모든 줄이 이 원장을 가리킨다'),
 (F20, 'TSMC', u'TSMC 2025년 Form 20-F', 'primary_official', '2026-04',
  u'2026년 4월 SEC 제출. 고객 집중도(상위 10대·1위·2위)·플랫폼별·지역별 매출과 웨이퍼 '
  u'공급사 실명이 여기 있다. 고객 실명은 어느 해도 공개되지 않는다'),
 (AR25, 'TSMC', u'TSMC 2025년 대만 연차보고서(TWSE)', 'primary_official', None,
  u'지분·자회사와 5.3 Manufacturing Excellence 절의 공급사 표가 실린 자리다. 공급사 표 '
  u'최신판 대조는 아직 남았다'),
 (AR22, 'TSMC', u'TSMC 2022년 대만 연차보고서(TWSE)', 'primary_official', None,
  u'화학·리소그래피 소재·특수가스·CMP 공급사 명단을 카테고리별 실명으로 공개한 판이다. '
  u'2025년판과 대조해야 한다'),
 (F05, 'TSMC', u'TSMC 2005년 Form 20-F', 'primary_official', None,
  u'원재료비 안의 웨이퍼 42%·화학 20%·가스 9% 구성이 실린 옛 공시다. 구조 참고용'),
 ('apple_10k_fy2025', 'Apple', u'Apple 2025 회계연도 Form 10-K', 'primary_official',
  '2025-10', u'특정 부품을 단일 공급원에 의존한다고 적는다. TSMC 실명은 10-K 가 아니라 '
  u'공급업체 리스트에 오른다'),
 ('amd_10k_2025', 'AMD', u'AMD 2025 회계연도 Form 10-K', 'primary_official', None,
  u'TSMC 를 웨이퍼 주 공급원으로 실명으로 적는다. 금액·비중은 비공개'),
 ('avgo_10k_2025', 'Broadcom', u'Broadcom 2025 회계연도 Form 10-K', 'primary_official',
  None, u'파운드리 의존을 적는다. TSMC 실명 문구는 원문 조사에서 확인되지 않았다'),
 ('qcom_10k_2025', 'Qualcomm', u'Qualcomm 2025 회계연도 Form 10-K', 'primary_official',
  None, u'TSMC·삼성 이중 소싱을 실명으로 적는다'),
 ('intc_10k_2025', 'Intel', u'Intel 2025 회계연도 Form 10-K', 'primary_official', None,
  u'외부 파운드리 사용을 적는다'),
 ('amkr_10k_2025', 'Amkor Technology', u'Amkor 2025 회계연도 Form 10-K',
  'primary_official', None,
  u'contract foundries 를 고객군으로 적는다. TSMC 개별 물량은 비공개'),
 ('amat_10k_fy2025', 'Applied Materials', u'Applied Materials 2025 회계연도 Form 10-K',
  'primary_official', None,
  u'2대 고객이 매출의 19%·15%(전년 12%·11%). 실명은 적지 않는다. 10월 결산'),
 ('lrcx_10k_fy2025', 'Lam Research', u'Lam Research 2025 회계연도 Form 10-K',
  'primary_official', None, u'지역별 매출 중국 34%·한국 22%·대만 19%·일본 10%. 6월 결산'),
 ('asml_ar_2025', 'ASML', u'ASML 2025년 연차보고서', 'primary_official', None,
  u'2025년 매출 327억 유로(+15.6%), 시스템 매출의 지역 구성과 EUV·High-NA 판매 대수'),
 ('mediatek_twse_2025', 'MediaTek', u'MediaTek 대만 공시(TWSE 2454)', 'primary_official',
  None, u'선단 공정을 TSMC 에 맡긴다는 사실이 적히나 금액·비중은 비공개'),
 ('doosan_disclosure_20260731', u'㈜두산', u'타법인주식 취득 결정', 'primary_official',
  '2026-07-31', u'SK실트론 지분 70.6% 를 2.3조 원에 취득하는 SPA. 2027~34년 EBITDA 초과, '
  u'주요 고객사 품질 인증, 미국 자회사 자산 처분에 걸린 언아웃이 붙는다'),
 ('sk_inc_disposal_20250331', u'SK㈜', u'타법인주식 처분 결정', 'primary_official',
  '2025-03-31', u'SK스페셜티 지분 85% 를 약 2.6조 원에 한앤컴퍼니에 넘기고 15% 를 남겼다'),
 ('sk_siltron_dart', u'SK실트론 / DART', u'SK실트론 사업보고서·반기보고서',
  'primary_official', None,
  u'2024~2025년 매출·영업이익과 SK하이닉스가 상반기 매출의 18% 라는 고객 구성이 여기 있다'),
]

# 이미 전역에 선 공시는 그 id 를 쓴다 — 엔비디아 사슬의 FY2026 10-K, 애플 공급업체 리스트
NV10K = 'nv_fin_001'
APPLE_SUPPLIER = 'apple_supplier'

# ── 상자 — 전역에 없는 것만. (id, name, name_ko, type, country, categories, desc) ──
ANON = {'tsmc-anon-c1', 'tsmc-anon-c2'}
PARENT = {'cymer': 'asml', 'spil': 'ase', 'siltronic': 'wacker-chemie',
          'shin-etsu-handotai': 'shin-etsu-chemical',
          'nippon-sanso-taiwan': 'nippon-sanso'}

ENTITIES = [
 # ── 뒷단 Tier 1 ──
 ('broadcom', 'Broadcom Inc.', u'브로드컴', 'company', u'미국', ['Fabless chip maker'],
  u'구글 TPU·메타 MTIA 같은 커스텀 AI ASIC 과 네트워킹 스위치를 설계해 파운드리에 맡긴다'),
 ('qualcomm', 'QUALCOMM Incorporated', u'퀄컴', 'company', u'미국', ['Fabless chip maker'],
  u'스냅드래곤 AP·모뎀·자동차 칩을 TSMC 와 삼성에 이중으로 맡긴다'),
 ('sony', 'Sony Group Corporation', u'소니', 'company', u'일본', ['Image sensor maker'],
  u'이미지센서 로직을 맡기고 구마모토 JASM 에 출자한 주주이기도 하다'),
 ('nxp', 'NXP Semiconductors N.V.', 'NXP', 'company', u'네덜란드',
  ['Automotive chip maker'], u'자동차 MCU 를 설계하고 드레스덴 ESMC 주주로도 들어갔다'),
 ('infineon', 'Infineon Technologies AG', u'인피니온', 'company', u'독일',
  ['Automotive chip maker'], u'자동차·산업용 반도체를 만들고 드레스덴 ESMC 주주다'),
 ('stmicroelectronics', 'STMicroelectronics N.V.', u'ST마이크로일렉트로닉스', 'company',
  u'프랑스', ['Automotive chip maker'], u'자동차·산업용 칩 일부를 외부 파운드리에 맡긴다'),
 ('renesas', 'Renesas Electronics Corporation', u'르네사스', 'company', u'일본',
  ['Automotive chip maker'], u'자동차 MCU 를 만들고 선단 공정은 외부에 맡긴다'),
 ('tsmc-anon-c1', 'Largest customer (undisclosed)', u'1위 고객(비공개)', 'company', None,
  ['Undisclosed customer'],
  u'20-F 가 비중만 밝히고 실명을 적지 않은 1위 고객. 업계는 2025년까지 애플로 읽지만 '
  u'그 짝짓기의 근거 등급은 C 다'),
 ('tsmc-anon-c2', 'Second largest customer (undisclosed)', u'2위 고객(비공개)', 'company',
  None, ['Undisclosed customer'],
  u'20-F 가 비중만 밝히고 실명을 적지 않은 2위 고객. 업계는 엔비디아로 읽지만 그 '
  u'짝짓기의 근거 등급은 C 다'),
 # ── 중개 ──
 ('guc', 'Global Unichip Corp.', 'GUC', 'company', u'대만', ['Design service'],
  u'TSMC 가 약 35% 를 가진 디자인 서비스 회사. 하이퍼스케일러 ASIC 을 받아 TSMC 공정으로 '
  u'옮긴다'),
 ('alchip', 'Alchip Technologies, Ltd.', u'알칩', 'company', u'대만', ['Design service'],
  u'하이퍼스케일러 커스텀 ASIC 설계를 맡아 GUC 와 경쟁한다'),
 # ── 고객의 고객 ──
 ('pegatron', 'Pegatron Corporation', u'페가트론', 'company', u'대만', ['EMS'],
  u'애플 기기를 조립한다'),
 ('luxshare', 'Luxshare Precision Industry', u'럭스셰어', 'company', u'중국', ['EMS'],
  u'애플 기기를 조립한다'),
 ('xai', 'xAI Corp.', 'xAI', 'end_user', u'미국', ['AI lab'],
  u'엔비디아 가속기를 대량으로 들이는 AI 회사다'),
 ('supermicro', 'Super Micro Computer, Inc.', u'슈퍼마이크로', 'company', u'미국',
  ['Server ODM'], u'엔비디아 가속기를 얹은 서버를 조립한다'),
 ('dell', 'Dell Technologies Inc.', u'델', 'company', u'미국', ['Server·PC OEM'],
  u'엔비디아·AMD 칩을 넣은 서버와 PC 를 판다'),
 ('hp', 'HP Inc.', 'HP', 'company', u'미국', ['PC OEM'], u'AMD 칩을 넣은 PC 를 판다'),
 ('lenovo', 'Lenovo Group Limited', u'레노버', 'company', u'중국', ['PC OEM'],
  u'AMD 칩을 넣은 PC 를 판다'),
 ('xiaomi', 'Xiaomi Corporation', u'샤오미', 'company', u'중국', ['Smartphone OEM'],
  u'퀄컴·미디어텍 AP 를 쓰는 스마트폰을 만든다'),
 ('oppo', 'OPPO', u'오포', 'company', u'중국', ['Smartphone OEM'],
  u'퀄컴·미디어텍 AP 를 쓰는 스마트폰을 만든다'),
 ('vivo', 'vivo', u'비보', 'company', u'중국', ['Smartphone OEM'],
  u'퀄컴·미디어텍 AP 를 쓰는 스마트폰을 만든다'),
 # ── 옆단 OSAT·기판 ──
 ('ase', 'ASE Technology Holding Co., Ltd.', 'ASE 테크놀로지', 'company', u'대만',
  ['OSAT'], u'CoWoS 후공정을 TSMC 에서 받아 한다. SPIL 을 100% 가진 그룹이다'),
 ('spil', 'Siliconware Precision Industries Co., Ltd.', 'SPIL', 'company', u'대만',
  ['OSAT'], u'CoWoS oS 와 CoW 전공정을 TSMC 에서 받아 한다. ASE 그룹 자회사다'),
 ('amkor', 'Amkor Technology, Inc.', u'앰코테크놀로지', 'company', u'미국', ['OSAT'],
  u'10-K 에 contract foundries 를 고객군으로 적었고 애리조나에서 TSMC 와 InFO·CoWoS '
  u'협력을 밝혔다'),
 ('ibiden', 'Ibiden Co., Ltd.', u'이비덴', 'company', u'일본', ['Substrate'],
  u'CoWoS 에 들어가는 ABF 기판을 만든다'),
 ('unimicron', 'Unimicron Technology Corp.', u'유니마이크론', 'company', u'대만',
  ['Substrate'], u'CoWoS 에 들어가는 ABF 기판을 만든다'),
 ('kinsus', 'Kinsus Interconnect Technology Corp.', u'킨서스', 'company', u'대만',
  ['Substrate'], u'CoWoS 에 들어가는 ABF 기판을 만들고 EMIB 형 패키징 공동개발이 '
  u'이름에 오른다'),
 ('nanya-pcb', 'Nan Ya Printed Circuit Board Corp.', u'난야PCB', 'company', u'대만',
  ['Substrate'], u'CoWoS 에 들어가는 ABF 기판을 만든다'),
 # ── 앞단 웨이퍼 ──
 ('shin-etsu-handotai', 'Shin-Etsu Handotai Co., Ltd.', u'신에츠한도타이(SEH)', 'company',
  u'일본', ['Silicon wafer'],
  u'세계 1위 실리콘 웨이퍼 회사. 모회사 신에츠화학은 포토레지스트도 공급한다'),
 ('sumco', 'SUMCO Corporation', u'스미코', 'company', u'일본', ['Silicon wafer'],
  u'세계 2위 웨이퍼 회사로 300mm 로직 비중이 높다'),
 ('formosa-sumco', 'Formosa SUMCO Technology Corp. (FST)', u'포모사스미코', 'jv',
  u'대만', ['Silicon wafer'], u'포모사플라스틱 그룹과 스미코가 세운 웨이퍼 합작사다'),
 ('globalwafers', 'GlobalWafers Co., Ltd.', u'글로벌웨이퍼스', 'company', u'대만',
  ['Silicon wafer'], u'세계 3위권 웨이퍼 회사. 텍사스 셔먼에 새 공장을 세운다'),
 ('siltronic', 'Siltronic AG', u'실트로닉', 'company', u'독일', ['Silicon wafer'],
  u'바커케미 자회사로 폴리실리콘부터 수직으로 묶였다'),
 ('sk-siltron', 'SK siltron Co., Ltd.', 'SK실트론', 'company', u'한국', ['Silicon wafer'],
  u'국내 유일한 300mm 웨이퍼 제조사. 2026년 7월 ㈜두산이 지분 70.6% 인수 계약을 맺었다'),
 ('soitec', 'Soitec S.A.', u'소이텍', 'company', u'프랑스', ['Silicon wafer'],
  u'SOI 와 특수 웨이퍼를 만든다'),
 # ── 앞단 화학·레지스트·가스·CMP ──
 ('air-liquide', 'Air Liquide S.A.', u'에어리퀴드', 'company', u'프랑스',
  ['Chemicals', 'Specialty gas'], u'공정 화학품과 특수가스 두 갈래에 이름이 오른다'),
 ('basf', 'BASF SE', 'BASF', 'company', u'독일', ['Chemicals'], u'공정 화학품을 공급한다'),
 ('dupont', 'DuPont de Nemours, Inc.', u'듀폰', 'company', u'미국',
  ['Chemicals', 'CMP materials'], u'공정 화학품과 CMP 소재 두 갈래에 이름이 오른다'),
 ('entegris', 'Entegris, Inc.', u'엔테그리스', 'company', u'미국',
  ['Chemicals', 'Specialty gas', 'CMP materials'],
  u'화학·가스·CMP 세 갈래에 모두 이름이 오른다. 2022년 캐봇마이크로일렉트로닉스를 '
  u'합병했다'),
 ('fujifilm-electronic-materials', 'FUJIFILM Electronic Materials',
  u'후지필름 일렉트로닉 머티리얼즈', 'company', u'일본',
  ['Chemicals', 'Photoresist', 'CMP materials'],
  u'화학·포토레지스트·CMP 세 갈래에 모두 이름이 오른다'),
 ('kanto-ppc', 'Kanto-PPC, Inc.', u'간토PPC', 'jv', u'대만', ['Chemicals'],
  u'간토화학과 대만 PPC 가 세운 고순도 화학 합작사다'),
 ('kuang-ming', 'Kuang Ming Industrial', u'광밍', 'company', u'대만', ['Chemicals'],
  u'대만 현지 화학 공급사다'),
 ('merck', 'Merck KGaA', u'머크', 'company', u'독일', ['Chemicals'],
  u'공정 화학품을 공급한다'),
 ('rasa', 'RASA Industries, Ltd.', u'라사공업', 'company', u'일본', ['Chemicals'],
  u'공정 화학품을 공급한다'),
 ('shiny-chemical', 'Shiny Chemical Industrial Co., Ltd.', u'샤이니', 'company', u'대만',
  ['Chemicals'], u'대만 현지 화학 공급사다'),
 ('tokuyama', 'Tokuyama Corporation', u'도쿠야마', 'company', u'일본',
  ['Chemicals', 'Polysilicon'], u'공정 화학품을 공급하고 폴리실리콘도 만든다'),
 ('wah-lee', 'Wah Lee Industrial Corp.', u'화리공업', 'company', u'대만', ['Distributor'],
  u'엔테그리스·듀폰 제품을 비롯한 해외 화학·소재·장비를 대만 팹에 넣는 대표 유통사다'),
 ('3m', '3M Company', '3M', 'company', u'미국', ['Photoresist', 'CMP materials'],
  u'리소그래피 소재와 CMP 소재 두 갈래에 이름이 오른다'),
 ('jsr', 'JSR Corporation', 'JSR', 'company', u'일본', ['Photoresist'],
  u'EUV 레지스트 일본 3사 가운데 하나. 2024년 일본 정부계 JIC 가 인수해 비상장이 됐다'),
 ('nissan-chemical', 'Nissan Chemical Corporation', u'닛산화학', 'company', u'일본',
  ['Photoresist'], u'리소그래피 소재를 공급한다'),
 ('shin-etsu-chemical', 'Shin-Etsu Chemical Co., Ltd.', u'신에츠화학', 'company', u'일본',
  ['Photoresist'], u'EUV 레지스트 일본 3사 가운데 하나이고 SEH 의 모회사다'),
 ('sumitomo-chemical', 'Sumitomo Chemical Co., Ltd.', u'스미토모화학', 'company', u'일본',
  ['Photoresist'], u'리소그래피 소재를 공급한다'),
 ('tok', 'Tokyo Ohka Kogyo Co., Ltd.', u'도쿄오카공업(TOK)', 'company', u'일본',
  ['Photoresist'], u'EUV 레지스트 일본 3사 가운데 하나다'),
 ('air-products', 'Air Products and Chemicals, Inc.', u'에어프로덕츠', 'company', u'미국',
  ['Specialty gas'], u'특수가스를 공급한다'),
 ('central-glass', 'Central Glass Co., Ltd.', u'센트럴글래스', 'company', u'일본',
  ['Specialty gas'], u'특수가스를 공급한다'),
 ('linde', 'Linde plc', u'린데', 'company', u'독일·미국', ['Specialty gas'],
  u'특수가스를 공급한다. 프랙스에어는 린데에 합병돼 따로 서지 않는다'),
 ('linde-lienhwa', 'Linde LienHwa Industrial Gases Co., Ltd.', u'린데리엔화', 'jv',
  u'대만', ['Specialty gas'],
  u'린데와 리엔화실업의 합작사. 대만 최대 산업가스사이고 TSMC 팹 옆에 온사이트 플랜트를 '
  u'둔다'),
 ('lienhwa', 'LienHwa Industrial Holdings Corp.', u'리엔화실업', 'company', u'대만',
  ['Industrial gas'], u'린데리엔화 합작의 대만 쪽 모회사다'),
 ('sk-specialty', 'SK specialty Co., Ltd.', 'SK스페셜티', 'company', u'한국',
  ['Specialty gas'],
  u'NF3·WF6 세계 1위. 2025년 3월 한앤컴퍼니가 지분 85% 를 사들였다'),
 ('taiwan-material-technology', 'Taiwan Material Technology Co., Ltd.',
  u'대만머티리얼테크놀로지', 'company', u'대만', ['Specialty gas'],
  u'대만 현지 가스 공급사다'),
 ('nippon-sanso-taiwan', 'Nippon Sanso Taiwan Co., Ltd.', u'니혼산소 대만', 'jv',
  u'대만', ['Specialty gas'], u'일본 니혼산소의 대만 법인이다'),
 ('nippon-sanso', 'Nippon Sanso Holdings Corporation', u'니혼산소 홀딩스', 'company',
  u'일본', ['Industrial gas'], u'니혼산소 대만의 모회사다'),
 ('kanto-chemical', 'Kanto Chemical Co., Inc.', u'간토화학', 'company', u'일본',
  ['Chemicals'], u'간토PPC 합작의 일본 쪽 모회사다'),
 ('ppc-taiwan', 'PPC (Taiwan)', 'PPC', 'company', u'대만', ['Chemicals'],
  u'간토PPC 합작의 대만 쪽 모회사다'),
 ('formosa-plastics', 'Formosa Plastics Group', u'포모사플라스틱 그룹', 'company',
  u'대만', ['Petrochemical'], u'포모사스미코 합작의 대만 쪽 모회사다'),
 ('agc', 'AGC Inc.', 'AGC', 'company', u'일본', ['CMP materials', 'Mask blank'],
  u'CMP 소재를 공급하고 호야와 함께 EUV 마스크 블랭크를 지배한다'),
 ('fujibo', 'Fujibo Holdings, Inc.', u'후지보', 'company', u'일본', ['CMP materials'],
  u'CMP 패드 소재를 공급한다'),
 ('fujimi', 'Fujimi Incorporated', u'후지미', 'company', u'일본', ['CMP materials'],
  u'CMP 슬러리를 공급한다'),
 ('topco-scientific', 'Topco Scientific Co., Ltd.', u'토프코', 'company', u'대만',
  ['Distributor'], u'신에츠 웨이퍼와 포토레지스트의 대만 총판 노릇이 거론되는 유통사다'),
 # ── 앞단 장비 ──
 ('asml', 'ASML Holding N.V.', 'ASML', 'company', u'네덜란드', ['Lithography equipment'],
  u'EUV 노광기를 혼자 만든다. 2025년 매출 327억 유로'),
 ('applied-materials', 'Applied Materials, Inc.', u'어플라이드머티리얼즈', 'company',
  u'미국', ['Deposition·etch equipment'], u'증착·식각·CMP·검사 장비를 공급한다'),
 ('lam-research', 'Lam Research Corporation', u'램리서치', 'company', u'미국',
  ['Etch equipment'], u'식각·증착 장비를 공급한다'),
 ('kla', 'KLA Corporation', 'KLA', 'company', u'미국', ['Process control equipment'],
  u'공정제어·검사 장비를 공급하고 대체재가 없다'),
 ('tokyo-electron', 'Tokyo Electron Limited', u'도쿄일렉트론', 'company', u'일본',
  ['Track·etch equipment'],
  u'EUV 트랙(코터·디벨로퍼)을 사실상 혼자 공급하고 식각 장비도 만든다'),
 ('screen-holdings', 'SCREEN Holdings Co., Ltd.', u'스크린홀딩스', 'company', u'일본',
  ['Cleaning equipment'], u'세정 장비를 공급한다'),
 ('kokusai-electric', 'Kokusai Electric Corporation', u'고쿠사이일렉트릭', 'company',
  u'일본', ['ALD equipment'], u'ALD·열처리 장비를 공급한다'),
 ('asm-international', 'ASM International N.V.', 'ASM인터내셔널', 'company',
  u'네덜란드', ['ALD equipment'], u'ALD 장비를 공급한다'),
 ('advantest', 'Advantest Corporation', u'어드반테스트', 'company', u'일본',
  ['Test equipment'], u'테스트 장비를 공급한다'),
 ('teradyne', 'Teradyne, Inc.', u'테라다인', 'company', u'미국', ['Test equipment'],
  u'테스트 장비를 공급한다'),
 ('disco', 'DISCO Corporation', u'디스코', 'company', u'일본', ['Dicing equipment'],
  u'다이싱·그라인딩 장비를 공급한다'),
 ('onto-innovation', 'Onto Innovation Inc.', u'온토이노베이션', 'company', u'미국',
  ['Metrology equipment'], u'계측·검사 장비를 공급한다'),
 # ── 장비의 앞단 ──
 ('carl-zeiss-smt', 'Carl Zeiss SMT GmbH', u'칼자이스 SMT', 'company', u'독일',
  ['Optics'], u'ASML 노광기의 광학계를 만든다'),
 ('cymer', 'Cymer, LLC', u'사이머', 'company', None, ['Light source'],
  u'ASML 자회사로 노광 광원을 만든다'),
 ('trumpf', 'TRUMPF SE + Co. KG', u'트럼프', 'company', None, ['Laser'],
  u'EUV 광원에 쓰는 레이저를 만든다'),
 ('vdl', 'VDL Groep', 'VDL 그룹', 'company', None, ['Modules'],
  u'ASML 장비 모듈을 만든다'),
 ('prodrive', 'Prodrive Technologies', u'프로드라이브', 'company', None, ['Modules'],
  u'ASML 장비의 전자 모듈을 만든다'),
 ('ferrotec', 'Ferrotec Corporation', u'페로텍', 'company', None,
  ['Vacuum components'], u'장비용 진공 부품과 석영 도가니를 만든다'),
 ('mks-instruments', 'MKS Instruments, Inc.', 'MKS 인스트루먼츠', 'company', None,
  ['Vacuum components'], u'장비용 진공·계측 부품을 만든다'),
 ('edwards', 'Edwards Vacuum', u'에드워즈', 'company', None, ['Vacuum pumps'],
  u'장비용 진공 펌프를 만든다'),
 ('ichor', 'Ichor Holdings, Ltd.', u'아이코어', 'company', None, ['Gas panels'],
  u'장비용 가스 패널을 만든다'),
 ('ultra-clean-holdings', 'Ultra Clean Holdings, Inc. (UCT)', 'UCT', 'company', None,
  ['Gas panels'], u'장비용 가스 패널을 만든다'),
 # ── 소재의 앞단 ──
 ('wacker-chemie', 'Wacker Chemie AG', u'바커케미', 'company', u'독일', ['Polysilicon'],
  u'폴리실리콘을 만들고 실트로닉의 모회사다'),
 ('stella-chemifa', 'Stella Chemifa Corporation', u'스텔라케미파', 'company', u'일본',
  ['Hydrofluoric acid'], u'반도체용 불화수소를 만든다'),
 ('morita-chemical', 'Morita Chemical Industries Co., Ltd.', u'모리타화학', 'company',
  u'일본', ['Hydrofluoric acid'], u'반도체용 불화수소를 만든다'),
 ('hoya', 'HOYA Corporation', u'호야', 'company', u'일본', ['Mask blank'],
  u'AGC 와 함께 EUV 마스크 블랭크를 지배한다'),
 ('mitsui-chemicals', 'Mitsui Chemicals, Inc.', u'미쓰이화학', 'company', u'일본',
  ['Pellicle'], u'EUV 펠리클을 대부분 만든다'),
 # ── 유틸리티 ──
 ('taipower', 'Taiwan Power Company', u'대만전력', 'utility', u'대만', ['Utility'],
  u'대만의 전력과 용수를 혼자 맡는다. 산업용 요금 인상이 TSMC 원가에 바로 들어온다'),
 # ── 지분·자본 ──
 ('jasm', 'Japan Advanced Semiconductor Manufacturing, Inc. (JASM)', 'JASM', 'jv',
  u'일본', ['Fab'], u'구마모토의 TSMC 합작 팹. 소니·덴소·도요타가 주주로 들어왔다'),
 ('esmc', 'European Semiconductor Manufacturing Company (ESMC)', 'ESMC', 'jv', u'독일',
  ['Fab'], u'드레스덴의 TSMC 합작 팹. 보쉬·인피니온·NXP 가 각각 10% 가까이 가졌다'),
 ('tsmc-arizona', 'TSMC Arizona Corporation', 'TSMC 애리조나', 'company', u'미국',
  ['Fab'], u'TSMC 가 100% 가진 미국 팹. CHIPS 법 보조금 66억 달러와 세액공제가 붙었다'),
 ('vis', 'Vanguard International Semiconductor Corporation (VIS)', u'뱅가드(VIS)',
  'company', u'대만', ['Foundry'],
  u'TSMC 가 약 28% 를 가진 8인치·성숙 노드 파운드리다'),
 ('visera', 'VisEra Technologies Company Ltd.', u'비세라', 'company', u'대만',
  ['CIS process'], u'TSMC 가 70%대를 가진 CIS 컬러필터·마이크로렌즈 회사다'),
 ('xintec', 'Xintec Inc.', u'신텍', 'company', u'대만', ['WLCSP packaging'],
  u'TSMC 가 약 40% 를 가진 WLCSP 패키징 회사다'),
 ('denso', 'DENSO Corporation', u'덴소', 'company', u'일본', ['Automotive supplier'],
  u'JASM 주주로 자동차용 캐파에 출자했다'),
 ('toyota', 'Toyota Motor Corporation', u'도요타', 'company', u'일본', ['Automaker'],
  u'JASM 주주다'),
 ('bosch', 'Robert Bosch GmbH', u'보쉬', 'company', u'독일', ['Automotive supplier'],
  u'ESMC 주주다'),
 ('doosan', 'Doosan Corporation', u'㈜두산', 'company', u'한국', ['Industrial group'],
  u'2026년 7월 31일 SK실트론 지분 70.6% 를 2.3조 원에 사기로 계약했다'),
 ('sk-inc', 'SK Inc.', 'SK㈜', 'company', u'한국', ['Holding company'],
  u'SK실트론과 SK스페셜티의 종전 지배주주다'),
 ('hanandcompany', 'Hahn & Company', u'한앤컴퍼니', 'financial_institution', u'한국',
  ['Private equity'], u'2025년 3월 SK스페셜티 지분 85% 를 약 2.6조 원에 사들였다'),
 ('jic', 'Japan Investment Corporation (JIC)', u'일본투자공사(JIC)',
  'financial_institution', u'일본', ['State-backed fund'],
  u'2024년 JSR 을 인수해 비상장으로 돌린 일본 정부계 펀드다'),
 # ── 매출원 상자 — vc_norm 이 분류로 접는다 ──
 ('tsmc-rev-hpc', 'HPC', u'고성능 컴퓨팅(HPC) 매출', 'revenue_type', None,
  ['Revenue type'], u'2025년 매출의 58%(NT$2조1,929억)로 가장 큰 갈래다'),
 ('tsmc-rev-smartphone', 'Smartphone', u'스마트폰 매출', 'revenue_type', None,
  ['Revenue type'], u'2025년 매출의 29%'),
 ('tsmc-rev-iot', 'IoT', 'IoT 매출', 'revenue_type', None, ['Revenue type'],
  u'2025년 매출의 5%'),
 ('tsmc-rev-automotive', 'Automotive', u'자동차 매출', 'revenue_type', None,
  ['Revenue type'], u'2025년 매출의 5%'),
 ('tsmc-rev-dce', 'DCE', u'디지털 소비자 가전(DCE) 매출', 'revenue_type', None,
  ['Revenue type'], u'2025년 매출의 1%'),
 ('tsmc-rev-other', 'Others', u'기타 매출', 'revenue_type', None, ['Revenue type'],
  u'2025년 매출의 2%'),
]


# ── 관계 ────────────────────────────────────────────────────────────
R = []


def R_(rid, s, t, typ, lane, sub, comp, srole, trole, ev, srcs, notes,
       st=None, tt=None, vf=None, vt=None, status='ACTIVE', ss=None, rt=None,
       cap=None, cc=None):
    row = {'id': rid, 'source_entity': s, 'target_entity': t,
           'relationship_type': typ, 'lane': lane, 'subsystem': sub,
           'component': comp, 'source_role': srole, 'target_role': trole,
           'valid_from': vf, 'valid_to': vt, 'status': status,
           'evidence_level': ev, 'source_tier': st, 'target_tier': tt,
           'economic_importance': None, 'capacity_criticality': cap,
           'integration_criticality': None,
           'confidence_band': {'CONFIRMED': 'high', 'ESTIMATED': 'medium',
                               'INFERRED': 'low'}.get(ev, 'low'),
           'flows': [], 'source_ids': srcs, 'notes': notes,
           'supply_source_ids': ss or [], 'revenue_type_ids': rt or []}
    if cc:
        row['contractual_customer'] = cc
    R.append(row)
    return row


AR22_NOTE = (u'2022년판 대만 연차보고서가 카테고리별로 실명을 공개한 명단이다. '
             u'2025년판 5.3절 표와 대조해야 한다')

# ① 실리콘 웨이퍼 — 20-F 실명. 6개사가 웨이퍼 수요의 92~96%(2020~2022)
WAFERS = [
 ('shin-etsu-handotai', u'세계 1위 웨이퍼사. 모회사 신에츠화학이 포토레지스트도 함께 낸다',
  'MEDIUM'),
 ('sumco', u'세계 2위 웨이퍼사로 300mm 로직 비중이 높다', 'MEDIUM'),
 ('formosa-sumco', u'포모사플라스틱 그룹과 스미코의 합작사다', 'MEDIUM'),
 ('globalwafers', u'세계 3위권. 텍사스 셔먼 신공장을 세운다', 'MEDIUM'),
 ('siltronic', u'바커케미 자회사로 폴리실리콘부터 수직으로 묶였다', 'MEDIUM'),
 ('sk-siltron', u'국내 유일한 300mm 제조사. TSMC 비중은 비공개다', 'MEDIUM'),
 ('soitec', u'SOI·특수 웨이퍼를 낸다', None),
]
for eid, note, cap in WAFERS:
    R_('tsmc-wafer-' + eid, eid, TS, 'SUPPLIES', LB, 'Silicon wafer', u'300mm 실리콘 웨이퍼',
       u'웨이퍼 공급사', u'파운드리', 'CONFIRMED', [F20, L], note, st=MP, ss=[SS_WAFER],
       cap=cap)

# ②③④⑤ 화학품·포토레지스트·특수가스·CMP — 한 회사가 두 분류에 들면 ids 에 둘 다 넣는다
MATS = [
 ('air-liquide', [SS_CHEM, SS_GAS], u'공정 화학품과 특수가스 두 갈래에 이름이 오른다', None),
 ('basf', [SS_CHEM], None, None),
 ('dupont', [SS_CHEM, SS_CMP], u'공정 화학품과 CMP 소재 두 갈래에 이름이 오른다', None),
 ('entegris', [SS_CHEM, SS_GAS, SS_CMP],
  u'화학·가스·CMP 세 갈래에 모두 오른다. 명단의 캐봇마이크로일렉트로닉스는 이 회사로 읽는다',
  None),
 ('fujifilm-electronic-materials', [SS_CHEM, SS_PR, SS_CMP],
  u'화학·포토레지스트·CMP 세 갈래에 모두 오른다', None),
 ('kanto-ppc', [SS_CHEM], u'간토화학과 대만 PPC 의 고순도 화학 합작사다', None),
 ('kuang-ming', [SS_CHEM], None, None),
 ('merck', [SS_CHEM], None, None),
 ('rasa', [SS_CHEM], None, None),
 ('shiny-chemical', [SS_CHEM], None, None),
 ('tokuyama', [SS_CHEM], u'화학품 명단에 오르고 폴리실리콘도 만든다', None),
 ('wah-lee', [SS_CHEM], u'화학품 명단에 오른 대만 유통사다', None),
 ('3m', [SS_PR, SS_CMP], u'리소그래피 소재와 CMP 소재 두 갈래에 오른다', None),
 ('jsr', [SS_PR], u'EUV 레지스트 일본 3사 가운데 하나다', 'VERY_HIGH'),
 ('nissan-chemical', [SS_PR], None, None),
 ('shin-etsu-chemical', [SS_PR], u'EUV 레지스트 일본 3사 가운데 하나다', 'VERY_HIGH'),
 ('sumitomo-chemical', [SS_PR], None, None),
 ('tok', [SS_PR], u'EUV 레지스트 일본 3사 가운데 하나다', 'VERY_HIGH'),
 ('air-products', [SS_GAS], None, None),
 ('central-glass', [SS_GAS], None, None),
 ('linde', [SS_GAS], u'프랙스에어는 린데에 합병돼 따로 서지 않는다', None),
 ('linde-lienhwa', [SS_GAS], u'TSMC 팹 옆 온사이트 플랜트를 굴리는 합작사다', None),
 ('sk-specialty', [SS_GAS], u'NF3·WF6 세계 1위. TSMC 비중은 비공개다', None),
 ('taiwan-material-technology', [SS_GAS], None, None),
 ('nippon-sanso-taiwan', [SS_GAS], u'일본 니혼산소의 대만 법인이다', None),
 ('fujibo', [SS_CMP], None, None),
 ('fujimi', [SS_CMP], None, None),
 ('agc', [SS_CMP], u'CMP 소재 명단에 오른다. 마스크 블랭크는 따로 선다', None),
]
SUB_OF = {SS_CHEM: ('Chemicals', u'공정 화학품'), SS_PR: ('Photoresist', u'포토레지스트'),
          SS_GAS: ('Specialty gas', u'특수가스'), SS_CMP: ('CMP materials', u'CMP 소재')}
for eid, ss, note, cap in MATS:
    sub, comp = SUB_OF[ss[0]]
    R_('tsmc-mat-' + eid, eid, TS, 'SUPPLIES', LB, sub, comp, u'소재 공급사', u'파운드리',
       'CONFIRMED', [AR22, L], note or AR22_NOTE, st=MP, ss=ss, cap=cap)

# 마스크 블랭크·펠리클 — TSMC 자체 마스크샵에 들어가는 원재료
R_('tsmc-blank-hoya', 'hoya', TS, 'SUPPLIES', LB, 'Mask blank & pellicle',
   u'EUV 마스크 블랭크', u'블랭크 공급사', u'파운드리', 'CONFIRMED', [L],
   u'호야와 AGC 가 EUV 블랭크의 93% 가까이를 쥔다. 마스크는 TSMC 자체 마스크샵이 만든다',
   st=RAW, ss=[SS_BLANK], cap='VERY_HIGH')
R_('tsmc-blank-agc', 'agc', TS, 'SUPPLIES', LB, 'Mask blank & pellicle',
   u'EUV 마스크 블랭크', u'블랭크 공급사', u'파운드리', 'CONFIRMED', [L],
   u'호야와 함께 EUV 블랭크를 지배한다', st=RAW, ss=[SS_BLANK], cap='VERY_HIGH')
R_('tsmc-pellicle-mitsui', 'mitsui-chemicals', TS, 'SUPPLIES', LB,
   'Mask blank & pellicle', u'EUV 펠리클', u'펠리클 공급사', u'파운드리', 'CONFIRMED', [L],
   u'EUV 펠리클을 대부분 만든다', st=RAW, ss=[SS_BLANK], cap='HIGH')

# 유통사 — 원제조사 → 유통사 → TSMC
R_('tsmc-dist-topco', 'topco-scientific', TS, 'SUPPLIES', LB, 'Material processing',
   u'웨이퍼·포토레지스트 총판', u'유통사', u'파운드리', 'INFERRED', [L],
   u'신에츠 웨이퍼·포토레지스트의 대만 총판 노릇이 원문에 적힌다', st=MP,
   ss=[SS_WAFER, SS_PR])
for src_id, dst, ss, sub in [
        ('entegris', 'wah-lee', [SS_CHEM], 'Chemicals'),
        ('dupont', 'wah-lee', [SS_CHEM], 'Chemicals'),
        ('shin-etsu-chemical', 'topco-scientific', [SS_PR], 'Photoresist'),
        ('shin-etsu-handotai', 'topco-scientific', [SS_WAFER], 'Silicon wafer')]:
    R_('tsmc-via-%s-%s' % (src_id, dst), src_id, dst, 'SUPPLIES', LB, sub,
       u'유통사 취급 품목', u'원제조사', u'유통사', 'INFERRED', [L],
       u'유통사가 취급하는 브랜드로 원문이 이름을 적었다. 물량·마진은 비공개', st=MP, ss=ss)

# 장비 — capex 가 시차를 두고 감가상각으로 원가에 들어온다
EQUIP = [('asml', u'EUV 노광기를 혼자 만든다. 익명 최대 매입처 A 사로 읽힌다', 'VERY_HIGH'),
         ('applied-materials', u'증착·식각·CMP·검사에 걸쳐 여러 공정에 들어간다', None),
         ('lam-research', u'식각이 핵심이다', None),
         ('kla', u'공정제어·검사에 대체재가 없다', 'HIGH'),
         ('tokyo-electron', u'EUV 트랙(코터·디벨로퍼)을 사실상 혼자 낸다', 'VERY_HIGH'),
         ('screen-holdings', u'세정 장비를 낸다', None),
         ('kokusai-electric', u'ALD·열처리 장비를 낸다', None),
         ('asm-international', u'ALD 장비를 낸다', None),
         ('advantest', u'테스트 장비를 낸다', None),
         ('teradyne', u'테스트 장비를 낸다', None),
         ('disco', u'다이싱·그라인딩 장비를 낸다', None),
         ('onto-innovation', u'계측·검사 장비를 낸다', None)]
for eid, note, cap in EQUIP:
    R_('tsmc-eq-' + eid, eid, TS, 'EQUIPMENT_SUPPLY', LE, 'Equipment', u'전공정·후공정 장비',
       u'장비사', u'파운드리', 'CONFIRMED', [L], note, st=SM, ss=[SS_EQ], cap=cap)

# 장비의 앞단
for eid, comp in [('carl-zeiss-smt', u'노광 광학계'), ('cymer', u'노광 광원'),
                  ('trumpf', u'광원용 레이저'), ('vdl', u'장비 모듈'),
                  ('prodrive', u'장비 전자 모듈')]:
    R_('tsmc-eq2-%s-asml' % eid, eid, 'asml', 'SUPPLIES', LE, 'Equipment', comp,
       u'장비 부품사', u'장비사', 'INFERRED', [L],
       u'ASML 장비의 앞단으로 원문이 이름을 적었다. 물량 비중은 비공개', st=CS, ss=[SS_EQ])
for eid, comp in [('ferrotec', u'진공 부품'), ('mks-instruments', u'진공·계측 부품'),
                  ('edwards', u'진공 펌프'), ('ichor', u'가스 패널'),
                  ('ultra-clean-holdings', u'가스 패널')]:
    for dst in ('tokyo-electron', 'lam-research'):
        R_('tsmc-eq2-%s-%s' % (eid, dst), eid, dst, 'SUPPLIES', LE, 'Equipment', comp,
           u'장비 부품사', u'장비사', 'INFERRED', [L],
           u'도쿄일렉트론·램리서치의 앞단으로 원문이 이름을 적었다. 물량 비중은 비공개',
           st=CS, ss=[SS_EQ])

# 소재의 앞단 — 원문이 실명으로 짝지은 것만 세운다
R_('tsmc-poly-wacker-siltronic', 'wacker-chemie', 'siltronic', 'SUPPLIES', LB,
   'Raw material', u'폴리실리콘', u'폴리실리콘 공급사', u'웨이퍼사', 'INFERRED', [L],
   u'실트로닉은 바커케미 자회사여서 폴리실리콘부터 수직으로 묶인다. 헴록·도쿠야마·OCI 는 '
   u'원문이 웨이퍼사와 실명으로 짝짓지 않아 관계로 세우지 않았다', st=RAW, ss=[SS_WAFER])
for eid in ('stella-chemifa', 'morita-chemical'):
    for dst in ('linde-lienhwa', 'sk-specialty'):
        R_('tsmc-hf-%s-%s' % (eid, dst), eid, dst, 'SUPPLIES', LB, 'Raw material',
           u'불화수소(HF)', u'불소 화학사', u'가스사', 'INFERRED', [L],
           u'원문 5절 지도가 불화수소를 린데리엔화·SK스페셜티 쪽으로 그린다. 개별 물량은 '
           u'비공개', st=RAW, ss=[SS_GAS])

# ABF 기판·CoWoS 외주 — 매출 흐름의 옆단
for eid, note in [('ibiden', None), ('unimicron', None),
                  ('kinsus', u'EMIB 형 패키징 공동개발이 이름에 오른다'),
                  ('nanya-pcb', None)]:
    R_('tsmc-sub-' + eid, eid, TS, 'SUPPLIES', LB, 'Substrate', u'CoWoS ABF 기판',
       u'기판사', u'파운드리', 'INFERRED', [L], note or u'CoWoS 기판 공급사로 이름이 오른다',
       st=SM, ss=[SS_ABF])
    R_('tsmc-abf-ajinomoto-' + eid, 'ajinomoto-fine-techno', eid, 'SUPPLIES', LB,
       'Raw material', u'ABF 필름', u'필름 공급사', u'기판사', 'INFERRED', [L],
       u'ABF 필름의 95% 넘는 몫을 혼자 쥔다. CoWoS 기판의 기초 소재다', st=CS,
       ss=[SS_ABF], cap='VERY_HIGH')
for eid, ev, srcs, note in [
        ('ase', 'INFERRED', [L],
         u'CoWoS oS 와 CoW 전공정을 받아 한다. 2025년 말 월 2~2.5만 장 캐파가 거론된다'),
        ('spil', 'INFERRED', [L], u'2026년 6~8만 장/년 외주 물량이 거론된다. ASE 그룹이다'),
        ('amkor', 'ESTIMATED', ['amkr_10k_2025', L],
         u'10-K 에 contract foundries 를 고객군으로 적었다. 2026년 18~19만 장/년 외주 '
         u'물량이 거론되고 애리조나 협력을 발표했다')]:
    R_('tsmc-osat-' + eid, eid, TS, 'EMS_ASSEMBLY', LB, 'Assembly & Test',
       u'CoWoS 후공정 외주', u'후공정(OSAT)', u'파운드리', ev, srcs, note, st=SM,
       ss=[SS_ABF])

# 유틸리티 — 원가의 7~8%
R_('tsmc-util-taipower', 'taipower', TS, 'UTILITY_SERVES', LO, 'Utility',
   u'전력·용수', u'전력회사', u'파운드리', 'CONFIRMED', [L],
   u'대만 전력·용수를 혼자 맡아 대체가 없다. 2024~25년 산업용 요금 인상이 원가에 바로 '
   u'들어왔다', st=MP, ss=[SS_UTIL], cap='VERY_HIGH')

# HBM — TSMC 공급사가 아니라 TSMC 고객의 병렬 공급사
for eid in ('sk-hynix', 'samsung-electronics', 'micron'):
    R_('tsmc-hbm-' + eid, eid, 'nvidia', 'SUPPLIES', LB, 'Memory', 'HBM',
       u'메모리 공급사', u'칩 회사', 'CONFIRMED', [NV10K, L],
       u'TSMC 공급사가 아니라 TSMC 고객의 병렬 공급사다. CoWoS 에서 TSMC 로직 다이와 '
       u'합류한다', st=CS, ss=[SS_MEM])

# ── 뒷단 Tier 1 ─────────────────────────────────────────────────────
# (고객, 근거등급, 계약고객 근거, 매출원, 출처, 메모)
T1 = [
 ('apple', 'ESTIMATED', 'CONFIRMED', [RT_SP, RT_HPC],
  ['apple_10k_fy2025', APPLE_SUPPLIER, L],
  u'A 시리즈와 M 시리즈 로직을 전량 맡긴다. 10-K 는 단일 공급원 의존만 적고 TSMC 실명은 '
  u'공급업체 리스트에 오른다. 2025년 몫을 19~22%로 읽는 시각이 있으나 20-F 가 실명을 '
  u'밝히지 않아 확정할 수 없다'),
 ('nvidia', 'ESTIMATED', 'CONFIRMED', [RT_HPC], [NV10K, L],
  u'10-K 에 TSMC·삼성 파운드리와 CoWoS 패키징을 실명으로 적는다. 2025년 몫을 17~19%로 '
  u'읽는 시각이 있으나 20-F 가 실명을 밝히지 않아 확정할 수 없다'),
 ('amd', 'ESTIMATED', 'CONFIRMED', [RT_HPC], ['amd_10k_2025', L],
  u'10-K 가 TSMC 를 웨이퍼 주 공급원으로 적는다. 상위 10 안으로만 알려진다'),
 ('broadcom', 'ESTIMATED', 'UNVERIFIED', [RT_HPC], ['avgo_10k_2025', L],
  u'커스텀 AI ASIC 을 전량 맡긴다. 10-K 는 파운드리 의존만 적고 TSMC 실명 문구는 원문 '
  u'조사에서 확인되지 않았다'),
 ('marvell', 'ESTIMATED', 'UNVERIFIED', [RT_HPC], [L],
  u'커스텀 ASIC 과 광통신 DSP 를 맡긴다. 고객 공시의 TSMC 실명 문구는 확인되지 않았다'),
 ('qualcomm', 'ESTIMATED', 'CONFIRMED', [RT_SP, RT_AUTO], ['qcom_10k_2025', L],
  u'10-K 에 TSMC·삼성 이중 소싱을 적는다'),
 ('mediatek', 'ESTIMATED', 'UNVERIFIED', [RT_SP, RT_IOT], ['mediatek_twse_2025', L],
  u'선단 공정은 TSMC 단일이다. 대만 공시에 금액·비중은 없다'),
 ('intel', 'ESTIMATED', 'CONFIRMED', [RT_HPC], ['intc_10k_2025', L],
  u'10-K 에 외부 파운드리 사용을 적는다. 루나레이크·애로우레이크 타일과 Xe GPU 를 맡긴다'),
 ('google', 'INFERRED', 'UNVERIFIED', [RT_HPC], [L],
  u'자체 TPU 를 직접 계약으로 맡기거나 브로드컴·GUC 를 거친다. 경로별 배분은 비공개'),
 ('aws', 'INFERRED', 'UNVERIFIED', [RT_HPC], [L],
  u'자체 트레이니엄을 직접 계약으로 맡기거나 마벨·알칩을 거친다. 경로별 배분은 비공개'),
 ('microsoft', 'INFERRED', 'UNVERIFIED', [RT_HPC], [L],
  u'자체 마이아를 맡긴다. 직거래인지 중개인지는 비공개'),
 ('meta', 'INFERRED', 'UNVERIFIED', [RT_HPC], [L],
  u'자체 MTIA 를 맡긴다. 직거래인지 중개인지는 비공개'),
 ('sony', 'INFERRED', 'UNVERIFIED', [RT_AUTO, RT_IOT], [L],
  u'이미지센서 로직을 맡긴다. 자동차 5%·IoT 5% 의 주 구성이다'),
 ('nxp', 'INFERRED', 'UNVERIFIED', [RT_AUTO, RT_IOT], [L],
  u'자동차 MCU 를 맡긴다. 자동차 5%·IoT 5% 의 주 구성이다'),
 ('infineon', 'INFERRED', 'UNVERIFIED', [RT_AUTO, RT_IOT], [L],
  u'자동차·산업용 칩을 맡긴다'),
 ('stmicroelectronics', 'INFERRED', 'UNVERIFIED', [RT_AUTO, RT_IOT], [L],
  u'자동차·산업용 칩을 맡긴다'),
 ('renesas', 'INFERRED', 'UNVERIFIED', [RT_AUTO, RT_IOT], [L],
  u'자동차 MCU 를 맡긴다'),
]
for eid, ev, cc, rt, srcs, note in T1:
    R_('tsmc-cust-' + eid, TS, eid, 'SELLS_TO', LD, 'Chip maker', u'파운드리 위탁 생산',
       u'파운드리', u'직접 고객', ev, srcs, note, tt=CC, rt=rt, cc=cc)

# 익명 1·2위 고객 — 20-F 가 비중만 밝힌다
for eid, rank in (('tsmc-anon-c1', u'1위'), ('tsmc-anon-c2', u'2위')):
    R_('tsmc-cust-' + eid, TS, eid, 'SELLS_TO', LD, 'Undisclosed customer',
       u'파운드리 위탁 생산', u'파운드리', u'직접 고객', 'CONFIRMED', [F20, L],
       u'20-F 가 %s 고객의 총매출 대비 비중만 밝히고 실명은 어느 해도 적지 않는다. 업계가 '
       u'1위를 애플, 2위를 엔비디아로 읽는 것은 근거 등급 C 이고 대만 언론은 순서를 반대로 '
       u'읽기도 한다' % rank, tt=CC, cc='CONFIRMED')

# 중개 — 디자인 서비스가 하이퍼스케일러 ASIC 을 받아 TSMC 공정으로 옮긴다
for eid, note in [('guc', u'TSMC 가 약 35% 를 가진 디자인 서비스 회사다'),
                  ('alchip', u'GUC 와 경쟁하는 디자인 서비스 회사다')]:
    R_('tsmc-mid-' + eid, TS, eid, 'SELLS_TO', LD, 'Design service',
       u'디자인 서비스 경유 위탁', u'파운드리', u'중개', 'INFERRED', [L],
       note + u' 하이퍼스케일러 ASIC 이 이 경로로 들어오나 금액은 비공개다', tt=INT,
       cc='UNVERIFIED')

# HBM4 베이스 다이 — 병렬 공급사가 직접 고객으로 바뀌는 새 연결
R_('tsmc-cust-sk-hynix-hbm4', TS, 'sk-hynix', 'SELLS_TO', LD, 'Chip maker',
   u'HBM4 베이스 다이 로직 위탁', u'파운드리', u'직접 고객', 'INFERRED', [L],
   u'HBM4 부터 베이스 다이를 TSMC 로직 공정으로 만들면서 병렬 공급사가 직접 고객이 된다. '
   u'시점과 물량은 비공개다', tt=CC, vf='2027', status='PLANNED', cc='UNVERIFIED')

# ── 고객의 고객 ─────────────────────────────────────────────────────
CC2 = [
 ('apple', ['foxconn', 'pegatron', 'luxshare'], u'애플 기기 조립'),
 ('nvidia', ['microsoft', 'meta', 'google', 'aws', 'oracle', 'xai', 'coreweave'],
  u'하이퍼스케일러·네오클라우드'),
 ('nvidia', ['foxconn', 'quanta-computer', 'wistron', 'supermicro', 'dell'], u'서버 조립'),
 ('amd', ['dell', 'hp', 'lenovo'], 'PC'),
 ('amd', ['sony', 'microsoft'], u'콘솔'),
 ('broadcom', ['google', 'meta', 'aws'], u'커스텀 ASIC 최종 사용자'),
 ('marvell', ['google', 'meta', 'aws'], u'커스텀 ASIC 최종 사용자'),
 ('qualcomm', ['samsung-electronics', 'xiaomi', 'oppo', 'vivo'], u'스마트폰 OEM'),
 ('mediatek', ['samsung-electronics', 'xiaomi', 'oppo', 'vivo'], u'스마트폰 OEM'),
 ('guc', ['google', 'aws', 'meta'], u'커스텀 ASIC 최종 사용자'),
 ('alchip', ['google', 'aws', 'meta'], u'커스텀 ASIC 최종 사용자'),
]
for mid, dsts, comp in CC2:
    for d in dsts:
        R_('tsmc-cc-%s-%s' % (mid, d), mid, d, 'CUSTOMERS_CUSTOMER', LD, 'Integrator',
           comp, u'고객', u'고객의 고객', 'INFERRED', [L],
           u'원문 2-2 의 경로다. 금액·물량 배분은 비공개다', tt='END_USER')

# ── 지분·자본 ───────────────────────────────────────────────────────
for eid, note in [
        ('jasm', u'구마모토 특수공정·3nm 팹. 고객이 캐파에 출자해 물량을 묶었다'),
        ('esmc', u'드레스덴 28·16nm 자동차 팹. 유럽 자동차 IDM 3사가 고객 겸 주주다'),
        ('tsmc-arizona', u'CHIPS 법 보조금 66억 달러와 세액공제가 붙어 미 정부가 사실상 '
                         u'자본 파트너다'),
        ('guc', u'뒷단 중개를 지분으로 쥔다'),
        ('vis', u'성숙 노드 이관처다. 싱가포르 VSMC 는 NXP 와의 합작이다'),
        ('visera', u'CIS 컬러필터·마이크로렌즈. 지분은 70%대로만 적힌다'),
        ('xintec', 'WLCSP 패키징 회사다')]:
    R_('tsmc-eq-stake-' + eid, TS, eid, 'INVESTS_IN', LC, 'Corporate', u'지분',
       u'모회사', u'피투자사', 'CONFIRMED', [AR25, L], note)
for eid, dst in [('sony', 'jasm'), ('denso', 'jasm'), ('toyota', 'jasm'),
                 ('bosch', 'esmc'), ('infineon', 'esmc'), ('nxp', 'esmc')]:
    R_('tsmc-stake-%s-%s' % (eid, dst), eid, dst, 'INVESTS_IN', LC, 'Corporate',
       u'지분', u'주주', u'합작 팹', 'CONFIRMED', [AR25, L],
       u'고객이 캐파에 출자해 주주로 들어왔다')
R_('tsmc-stake-ase-spil', 'ase', 'spil', 'INVESTS_IN', LC, 'Corporate', u'지분',
   u'모회사', u'자회사', 'INFERRED', [L],
   u'2018년 합병으로 ASE 가 SPIL 을 100% 쥔다. CoWoS 외주 두 곳이 사실상 한 그룹이고 '
   u'앰코가 유일한 독립 대안이다')
R_('tsmc-stake-jic-jsr', 'jic', 'jsr', 'INVESTS_IN', LC, 'Corporate', u'지분',
   u'정부계 펀드', u'피투자사', 'INFERRED', [L],
   u'2024년 비상장화로 일본 정부가 병목 소재를 직접 쥐었다', vf='2024')
R_('tsmc-stake-doosan-sksiltron', 'doosan', 'sk-siltron', 'INVESTS_IN', LC, 'Corporate',
   u'지분 70.6%', u'인수자', u'웨이퍼사', 'CONFIRMED', ['doosan_disclosure_20260731', L],
   u'SPA 2.3조 원에 70.6%. 2027~34년 EBITDA 초과, 주요 고객사 품질 인증, 미국 자회사 자산 '
   u'처분에 걸린 언아웃이 붙는다. 100% 가치는 5조 원 중반으로 평가됐고 최태원 지분 29.4% 는 '
   u'별도 협상이다', vf='2026-07-31', status='PLANNED')
R_('tsmc-stake-skinc-sksiltron', 'sk-inc', 'sk-siltron', 'INVESTS_IN', LC, 'Corporate',
   u'지분 70.6%', u'종전 지배주주', u'웨이퍼사', 'CONFIRMED', ['sk_siltron_dart', L],
   u'SK㈜ 51.0% 와 TRS 19.6% 를 합쳐 70.6%. 매각 계약은 맺었으나 클로징 대기라 아직 '
   u'지배주주다')
R_('tsmc-stake-hahn-skspecialty', 'hanandcompany', 'sk-specialty', 'INVESTS_IN', LC,
   'Corporate', u'지분 85%', u'사모펀드', u'가스사', 'CONFIRMED',
   ['sk_inc_disposal_20250331', L],
   u'2025년 3월 31일 약 2.6조 원에 85% 를 인수해 SK㈜ 연결에서 빠졌다', vf='2025-03-31')
R_('tsmc-stake-skinc-skspecialty', 'sk-inc', 'sk-specialty', 'INVESTS_IN', LC,
   'Corporate', u'지분 15%', u'잔여 주주', u'가스사', 'CONFIRMED',
   ['sk_inc_disposal_20250331', L], u'85% 를 넘기고 15% 를 남겼다', vf='2025-03-31')

# 합작 — 모회사가 합작사를 통해 대만 현지에 공급한다
for p, jv in [('linde', 'linde-lienhwa'), ('lienhwa', 'linde-lienhwa'),
              ('kanto-chemical', 'kanto-ppc'), ('ppc-taiwan', 'kanto-ppc'),
              ('formosa-plastics', 'formosa-sumco'), ('sumco', 'formosa-sumco'),
              ('nippon-sanso', 'nippon-sanso-taiwan')]:
    R_('tsmc-jv-%s-%s' % (p, jv), p, jv, 'OPERATES_THROUGH', LC, 'Corporate',
       u'합작·현지 법인', u'모회사', u'합작사', 'CONFIRMED', [L],
       u'대만 현지 생산·유통을 이 법인으로 굴린다. 지분율은 원문에 없다')

# ── 매출원 갈림목 — vc_norm 이 분류로 접는다 ────────────────────────
REV = [('tsmc-rev-hpc', 'HPC', 58.0), ('tsmc-rev-smartphone', u'스마트폰', 29.0),
       ('tsmc-rev-iot', 'IoT', 5.0), ('tsmc-rev-automotive', u'자동차', 5.0),
       ('tsmc-rev-dce', 'DCE', 1.0), ('tsmc-rev-other', u'기타', 2.0)]
for eid, label, pct in REV:
    R_(eid + '-edge', TS, eid, 'REVENUE_FROM', LD, 'Revenue type', label,
       u'파운드리', u'매출원', 'CONFIRMED', [F20, L], None, tt='REVENUE_TYPE')


# ── 관측 — 관계에 붙는 %·금액만. 전사 절대값은 주장으로 간다 ──────────
O = []
PCT = 'percent'


def O_(oid, rid, metric, value, unit, period, ps, pe, aod, den, status, ev, srcs,
       low=None, high=None, note=None, scope='EDGE'):
    O.append({'id': oid, 'relationship_id': rid, 'metric': metric, 'value': value,
              'value_low': low, 'value_high': high, 'unit': unit, 'period': period,
              'period_start': ps, 'period_end': pe, 'as_of_date': aod,
              'denominator': den, 'status': status, 'evidence_level': ev,
              'confidence': 1.0, 'method_id': None, 'method_note': note,
              'source_ids': srcs, 'denominator_scope': scope,
              'source_date': aod})


# 고객 집중도 — 20-F Risk Factors. 실명은 어느 해도 없다
CONC = {'tsmc-anon-c1': [('2023', 25.0), ('2024', 22.0), ('2025', 19.0)],
        'tsmc-anon-c2': [('2023', 11.0), ('2024', 12.0), ('2025', 17.0)]}
for eid, rows in sorted(CONC.items()):
    for yr, v in rows:
        O_('o-%s-%s' % (eid, yr), 'tsmc-cust-' + eid, 'customer_revenue_share', v, PCT,
           yr, yr + '-01-01', yr + '-12-31', yr + '-12-31', u'TSMC 총매출',
           'CURRENT' if yr == '2025' else 'HISTORICAL', 'CONFIRMED', [F20],
           note=u'20-F 은 순위별 비중만 적는다', scope='FOCAL_TOTAL_REVENUE')

# 공급사 쪽 노출도 — 분모가 상대 회사 매출이라 선의 몫이 아니다
O_('o-asml-taiwan-share', 'tsmc-eq-asml', 'supplier_region_revenue_share', 22.0, PCT,
   '2025', '2025-01-01', '2025-12-31', '2025-12-31', u'ASML 2025 시스템 매출', 'CURRENT',
   'CONFIRMED', ['asml_ar_2025'],
   note=u'대만 지역 비중이고 TSMC 단독 비중이 아니다. 2분기에는 대만이 35% 로 지역 1위였다',
   scope='COUNTERPARTY_TOTAL_REVENUE')
O_('o-lam-taiwan-share', 'tsmc-eq-lam-research', 'supplier_region_revenue_share', 19.0,
   PCT, 'FY2025', '2024-07-01', '2025-06-30', '2025-06-30',
   u'Lam Research FY2025 총매출', 'CURRENT', 'CONFIRMED', ['lrcx_10k_fy2025'],
   note=u'대만 지역 비중이고 TSMC 단독 비중이 아니다', scope='COUNTERPARTY_TOTAL_REVENUE')
O_('o-amat-top-customer', 'tsmc-eq-applied-materials', 'top_customer_revenue_share',
   19.0, PCT, 'FY2025', '2024-11-01', '2025-10-31', '2025-10-31',
   u'Applied Materials FY2025 총매출', 'CURRENT', 'INFERRED', ['amat_10k_fy2025'],
   note=u'10-K 는 2대 고객이 19%·15% 라고만 적고 실명을 밝히지 않는다. 1위를 TSMC 로 읽는 '
        u'것은 근거 등급 C 다', scope='COUNTERPARTY_TOTAL_REVENUE')

# 지분율 — 거래 위에 소유를 겹친다
STAKE = [
 ('tsmc-eq-stake-jasm', 86.5, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-eq-stake-esmc', 70.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-eq-stake-tsmc-arizona', 100.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-eq-stake-guc', 35.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-eq-stake-vis', 28.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-eq-stake-xintec', 40.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-sony-jasm', 6.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-denso-jasm', 5.5, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-toyota-jasm', 2.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-bosch-esmc', 10.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-infineon-esmc', 10.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-nxp-esmc', 10.0, '2026-09', '2026-09-12', 'CURRENT', [AR25]),
 ('tsmc-stake-ase-spil', 100.0, '2018', '2018-12-31', 'CURRENT', [L]),
 ('tsmc-stake-doosan-sksiltron', 70.6, '2026-07-31', '2026-07-31', 'NOT_YET_ACTIVE',
  ['doosan_disclosure_20260731']),
 ('tsmc-stake-skinc-sksiltron', 70.6, '2026-09', '2026-09-12', 'CURRENT',
  ['sk_siltron_dart']),
 ('tsmc-stake-hahn-skspecialty', 85.0, '2025-03-31', '2025-03-31', 'CURRENT',
  ['sk_inc_disposal_20250331']),
 ('tsmc-stake-skinc-skspecialty', 15.0, '2025-03-31', '2025-03-31', 'CURRENT',
  ['sk_inc_disposal_20250331']),
]
for rid, v, period, aod, status, srcs in STAKE:
    O_('o-stake-' + rid, rid, 'equity_stake', v, PCT, period, None, None, aod,
       u'피투자사 지분 100%', status, 'CONFIRMED' if srcs != [L] else 'INFERRED', srcs)

# 플랫폼별 매출 — REVENUE_FROM 줄에 붙고 vc_norm 이 분류의 비중으로 옮긴다
for eid, label, pct in REV:
    O_('o-' + eid, eid + '-edge', 'platform_revenue_share', pct, PCT, '2025',
       '2025-01-01', '2025-12-31', '2025-12-31', u'TSMC 2025 총매출', 'CURRENT',
       'CONFIRMED', [F20], note=u'20-F 의 플랫폼별 매출 구분이다')


# ── 주장 ────────────────────────────────────────────────────────────
# (id, statement, subject, object, period, evidence_level, confidence, sources, note)
def C(cid, st, subj, period, ev, srcs, note=None, obj=None):
    return (cid, st, subj, obj, period, ev, 1.0, srcs, note)


A25 = [F20, L]
CLAIMS = [
 C('clm-tsmc-revenue-2025', u'2025년 매출은 NT$3조8,090억(US$1,224억)으로 전년보다 NT$ '
   u'기준 31.6%, 달러 기준 35.9% 늘었다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-netincome-2025', u'2025년 순이익은 NT$1조7,179억(US$552억)이고 순이익률은 '
   u'45.1% 다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-gm-2025', u'2025년 매출총이익률은 59.9% 로 2024년 56.1% 에서 올랐다.', TS,
   '2025', 'CONFIRMED', A25),
 C('clm-tsmc-shipments-2025', u'2025년 웨이퍼 출하는 12인치 환산 1,500만 장으로 2024년 '
   u'1,290만 장에서 늘었다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-customers-2025', u'2025년 고객은 534개, 제품은 12,682개다.', TS, '2025',
   'CONFIRMED', A25),
 C('clm-tsmc-node-mix-2025', u'2025년 웨이퍼 매출의 74% 가 7nm 이하이고 3nm 단독으로 '
   u'24% 다.', TS, '2025', 'CONFIRMED', A25,
   u'분모는 회사 총매출이 아니라 웨이퍼 매출이다'),
 C('clm-tsmc-capex-2025', u'2025년 Capex 는 NT$1조2,724억이다.', TS, '2025', 'CONFIRMED',
   A25),
 C('clm-tsmc-capex-2026', u'2026년 Capex 계획은 US$520~560억으로 제시됐고 이후 '
   u'US$600~640억으로 올려 잡는 이야기가 나왔다.', TS, '2026', 'INFERRED', [L],
   u'상향은 공시가 아니라 언론 보도 수준이다'),
 C('clm-tsmc-foundry20-2025', u'2025년 Foundry 2.0 점유율은 40% 로 2024년 34% 에서 '
   u'올랐다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-platform-2025', u'2025년 플랫폼별 매출은 HPC 58%(NT$2조1,929억)·스마트폰 '
   u'29%·IoT 5%·자동차 5%·DCE 1%·기타 2% 다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-region-2025', u'2025년 지역별 매출은 고객 본사 기준으로 북미 75%·중국·일본을 '
   u'뺀 아태 9%·중국 9%·일본 4%·EMEA 3% 다.', TS, '2025', 'CONFIRMED', A25),
 C('clm-tsmc-top10-conc', u'상위 10대 고객 비중은 2023년 70%, 2024년 76%, 2025년 78% 로 '
   u'올라갔다.', TS, '2023~2025', 'CONFIRMED', A25,
   u'분모는 회사 총매출이다. 실명은 어느 해도 공개되지 않는다'),
 C('clm-tsmc-top2-identity', u'1위 고객 비중은 25%→22%→19% 로 내려가고 2위는 '
   u'11%→12%→17% 로 올라갔는데, 업계는 2025년까지 1위를 애플·2위를 엔비디아로 읽고 2026년 '
   u'중 엔비디아의 역전을 본다.', TS, '2023~2026', 'INFERRED', A25,
   u'TSMC 공시는 순위만 밝혀 어느 쪽이 19% 인지 확정할 수 없다. 대만 보도는 순서를 반대로 '
   u'읽기도 한다'),
 C('clm-tsmc-wafer-supply-share', u'실리콘 웨이퍼 6개사가 2020~2022년 TSMC 웨이퍼 수요의 '
   u'92~96% 를 공급했다.', TS, '2020~2022', 'CONFIRMED', A25,
   u'2025년 20-F 의 최신 3개년 비중은 아직 대조하지 않았다'),
 C('clm-tsmc-cogs-2025', u'매출총이익률 59.9% 를 뒤집으면 2025년 매출원가는 NT$1조5,270억 '
   u'가까이인데 20-F 는 원가를 항목별로 나누지 않는다.', TS, '2025', 'INFERRED', [L]),
 C('clm-tsmc-cost-structure', u'업계가 읽는 2025년 매출원가 구성은 감가상각 40%대, '
   u'원재료 약 17%, 유틸리티 7~8% 이고 나머지가 인건비와 외주 패키징·테스트·마스크다.', TS,
   '2025', 'INFERRED', [L]),
 C('clm-tsmc-material-mix-2005', u'2005년 20-F 기준 원재료비 안에서 웨이퍼가 42%, 화학이 '
   u'20%, 가스가 9% 였다.', TS, '2005', 'CONFIRMED', [F05, L],
   u'오래된 수치이지만 원재료 안의 무게 순서를 보여 준다'),
 C('clm-tsmc-purchase-conc-2019', u'대만 연차보고서의 연결 순매입액 10% 이상 공급사 '
   u'항목은 2019년 기준으로 A 19%·B 17%·C 10% 를 적었다.', TS, '2019', 'CONFIRMED',
   [AR22, L], u'회사명은 A·B·C 로 익명 처리된다. 업계가 A 를 ASML 로 읽는 것은 근거 등급 '
   u'C 이고 2025년판 해당 페이지는 아직 대조하지 않았다'),
 C('clm-tsmc-rev-split', u'2025년 매출은 웨이퍼 약 87% 와 패키징·테스트·마스크 등 비웨이퍼 '
   u'약 13% 로 갈린다.', TS, '2025', 'INFERRED', [L]),
 C('clm-tsmc-asp', u'웨이퍼 매출은 출하 1,500만 장에 12인치 환산 혼합 ASP 약 US$7,100 을 '
   u'곱한 크기다.', TS, '2025', 'INFERRED', [L]),
 C('clm-tsmc-capacity', u'캐파는 1,700만 장을 넘고 가동률은 약 88% 이며 2026년 캐파 성장 '
   u'가이던스는 3% 다.', TS, '2025~2026', 'INFERRED', [L],
   u'캐파 성장 둔화가 물량 기여를 줄인다'),
 C('clm-tsmc-node-price', u'노드별 웨이퍼 매출 비중과 장당 가격은 3nm 24%·US$18~20k, '
   u'5·4nm 약 35%·US$15k, 7·6nm 약 15%·US$9k, 16nm 이상 성숙 26%·US$2~5k 로 읽힌다.', TS,
   '2025', 'INFERRED', [L]),
 C('clm-tsmc-price-hike', u'웨이퍼 가격은 해마다 3~10% 오르고 2027년에는 5~10% 인상 협의가 '
   u'거론된다. 2nm 은 2025년 4분기 양산에 들어가 2026~27년 믹스 상향을 끈다.', TS,
   '2026~2027', 'INFERRED', [L]),
 C('clm-tsmc-cowos', u'CoWoS 는 2025년 말 월 7.5~8만 장에 장당 US$3~5k 로 읽히고 2026년 '
   u'말 월 12~14만 장이 목표다.', TS, '2025~2026', 'INFERRED', [L]),
 C('clm-tsmc-cowos-outsource', u'2026년 CoWoS 외주 총량은 24~27만 장으로 읽히고 그만큼은 '
   u'OSAT 매출로 옮겨가 TSMC 에는 원가로 남는다.', TS, '2026', 'INFERRED', [L]),
 C('clm-tsmc-growth-decomp', u'2025년 달러 기준 매출 성장 약 36% 는 물량 16% 와 ASP 17% '
   u'로 갈리고, 2026년부터 무게중심이 물량에서 ASP·믹스·CoWoS 로 옮겨간다.', TS, '2025',
   'INFERRED', [L]),
 C('clm-tsmc-opincome-2025', u'2025년 영업이익은 매출 US$1,224억에서 매출원가 약 '
   u'US$491억(40.1%)과 영업비용 약 US$111억(9.1%)을 뺀 US$622억(50.8%)이다.', TS, '2025',
   'ESTIMATED', A25, u'매출원가율은 공시 매출총이익률에서 나오고 영업비용 구성은 추정이다'),
 C('clm-tsmc-unit-econ', u'장당으로 보면 원가 약 US$3,270 에 ASP 약 US$7,100 이라 장당 '
   u'매출총이익이 약 US$3,800 이고, 감가상각 1,470·원재료 560·유틸리티 250·인건비 330·'
   u'외주와 기타 660 이 그 원가를 채운다.', TS, '2025', 'INFERRED', [L]),
 C('clm-tsmc-wafer-cost-mix', u'웨이퍼 한 장 원가는 감가상각 약 45%, 원재료 약 17%, '
   u'유틸리티 7~8%, 인건비 약 10%, 외주·마스크·기타 약 20% 로 읽힌다.', TS, '2025',
   'INFERRED', [L], u'TSMC 는 원가 구성을 공개하지 않는다'),
 C('clm-tsmc-opex', u'영업비용은 R&D 약 7% 와 SG&A 약 2% 이고 2024년 SG&A 가 35.6% 늘어난 '
   u'주원인은 애리조나·구마모토·드레스덴 준비비다.', TS, '2024~2025', 'INFERRED', [L]),
 C('clm-tsmc-margin-levers', u'마진을 움직이는 지렛대는 가동률(1%p 당 GM 0.3~0.5%p), 노드 '
   u'믹스, 단가 인상, 해외팹 희석(GM 2~3%p), 환율(NT$ 1% 절상당 GM 0.4%p) 다섯이다.', TS,
   '2025~2026', 'ESTIMATED', [L], u'환율 민감도는 회사 가이던스이고 나머지는 추정이다'),
 # 10절 노출도
 C('clm-asml-exposure', u'ASML 의 2025년 시스템 매출은 중국 33%·한국 25%·대만 22% 로 '
   u'갈리고 2분기에는 대만이 35% 로 1위였으며, 2026년 중국 비중을 20% 로 줄이는 가이던스가 '
   u'대만·한국 비중을 키운다.', 'asml', '2025~2026', 'CONFIRMED', ['asml_ar_2025', L]),
 C('clm-asml-euv-monopoly', u'EUV 노광기는 ASML 단일 공급이고 TSMC 는 그 최대 매입처로 '
   u'읽혀 서로 대체가 없다.', 'asml', '2025', 'INFERRED', [L]),
 C('clm-amat-exposure', u'Applied Materials 의 2025 회계연도 10-K 는 2대 고객이 매출의 '
   u'19%·15% 라고 적었고(전년 12%·11%) 파운드리·로직이 반도체 매출의 67% 다.',
   'applied-materials', 'FY2025', 'CONFIRMED', ['amat_10k_fy2025', L],
   u'실명은 적히지 않는다'),
 C('clm-lam-exposure', u'Lam Research 의 2025 회계연도 지역별 매출은 중국 34%·한국 22%·'
   u'대만 19%·일본 10% 다.', 'lam-research', 'FY2025', 'CONFIRMED',
   ['lrcx_10k_fy2025', L]),
 C('clm-kla-exposure', u'KLA 는 대만이 최대 지역으로 30%대로 읽히고 공정제어에 대체재가 '
   u'없다.', 'kla', '2025', 'INFERRED', [L], u'10-K 지역별 표 대조가 남았다'),
 C('clm-tel-exposure', u'도쿄일렉트론은 대만 매출이 20%대로 읽히고 EUV 트랙을 사실상 '
   u'독점한다.', 'tokyo-electron', '2025', 'INFERRED', [L]),
 C('clm-seh-share', u'신에츠는 웨이퍼 세계 1위로 약 30% 를 쥐고 TSMC 가 최대 로직 '
   u'고객이다.', 'shin-etsu-handotai', '2025', 'INFERRED', [L]),
 C('clm-sumco-share', u'스미코는 웨이퍼 세계 2위로 약 17% 를 쥐고 300mm 로직 비중이 '
   u'높다.', 'sumco', '2025', 'INFERRED', [L]),
 C('clm-globalwafers-2025', u'글로벌웨이퍼스의 2025년 매출은 NT$606억(−3.2%)이고 점유율은 '
   u'약 17% 이며 TSMC 와 TI 가 주 고객이다.', 'globalwafers', '2025', 'INFERRED', [L]),
 C('clm-sksiltron-2025', u'SK실트론의 2025년 매출은 약 2조 원, 영업이익은 4,000억 원을 '
   u'넘고 상반기 매출 9,802억 원·영업이익 916억 원이며 SK하이닉스가 상반기 매출의 18% 를 '
   u'차지한다.', 'sk-siltron', '2025', 'CONFIRMED', ['sk_siltron_dart', L]),
 C('clm-sksiltron-2024', u'SK실트론의 2024년 매출은 2조1,268억 원, 영업이익은 3,155억 원, '
   u'EBITDA 는 6,171억 원이다.', 'sk-siltron', '2024', 'CONFIRMED',
   ['sk_siltron_dart', L]),
 C('clm-sksiltron-tsmc-share', u'SK실트론의 TSMC 비중은 공개되지 않고 두 자릿수에 못 미치는 '
   u'수준으로 읽히는데, 두산 SPA 의 주요 고객사 품질 인증 언아웃이 TSMC EUV 급 인증이면 '
   u'비중 상승의 방아쇠가 된다.', 'sk-siltron', '2026~2034', 'INFERRED', [L],
   u'㈜두산 공시의 추가 대금 지급 여부가 외부에서 읽을 수 있는 지표다'),
 C('clm-entegris-exposure', u'엔테그리스의 2025년 매출은 US$32.0억(−1%)이고 대만이 최대 '
   u'지역으로 20%대이며 화학·가스·CMP 세 카테고리에 모두 등재됐다.', 'entegris', '2025',
   'INFERRED', [L]),
 C('clm-skspecialty-exposure', u'SK스페셜티는 NF3·WF6 세계 1위로 약 40% 를 쥐고 2024년 '
   u'매출 6,817억 원·영업이익 1,471억 원인데 주 고객은 삼성·SK하이닉스이고 TSMC 비중은 '
   u'공개되지 않는다.', 'sk-specialty', '2024', 'ESTIMATED', [L]),
 C('clm-hyperscaler-exposure', u'하이퍼스케일러 4사는 자체 칩을 TSMC 에 맡기고 엔비디아 '
   u'경유까지 합치면 직접·간접으로 TSMC 매출의 30% 를 넘게 끌어온다.', TS, '2025~2026',
   'INFERRED', [L]),
 C('clm-exposure-symmetry', u'ASML·신에츠·엔비디아·애플은 TSMC 와 서로 대체 불가여서 '
   u'가격은 협상이고 관계는 장기인데, AMD·브로드컴·미디어텍·대만 유통사·SK실트론은 한쪽만 '
   u'묶여 TSMC 가격 인상이 그대로 전가된다.', TS, '2025~2026', 'INFERRED', [L]),
]

# 11절 병목 — 세 점수와 합계를 한 줄씩
BOTTLENECK = [
 ('euv-litho', u'EUV 노광기', 'asml', 'ASML', u'100%', 1, 1, 2, 4,
  u'네덜란드 단일, 광학은 독일 자이스. High-NA 전환기라 가장 위험하다'),
 ('euv-blank', u'EUV 마스크 블랭크', 'hoya', u'호야·AGC', u'약 93%', 1, 2, 1, 4,
  u'조용한 일본 단일 국가 위험이다'),
 ('euv-resist', u'EUV 레지스트', 'jsr', u'JSR·TOK·신에츠', u'90% 이상', 1, 2, 1, 4,
  u'2019년 한일 수출규제가 선례다'),
 ('euv-track', u'EUV 트랙', 'tokyo-electron', u'도쿄일렉트론', u'약 90%', 1, 2, 1, 4,
  u'코터·디벨로퍼가 사실상 한 곳이다'),
 ('abf-film', 'ABF 필름', 'ajinomoto-fine-techno', u'아지노모토', u'95% 이상', 1, 3, 1, 5,
  u'CoWoS 기판의 기초 소재다'),
 ('pellicle', u'펠리클', 'mitsui-chemicals', u'미쓰이화학', u'대부분', 2, 3, 1, 6, None),
 ('cowos', 'CoWoS 캐파', TS, u'TSMC 자체', None, 2, 2, 1, 5,
  u'2026년 외주 확대로 풀리는 중이다'),
 ('process-control', u'공정제어', 'kla', 'KLA', u'50% 이상', 2, 2, 3, 7, None),
 ('wafer-300mm', '300mm 웨이퍼', 'shin-etsu-handotai',
  u'신에츠·스미코·글로벌웨이퍼스·실트로닉·SK실트론', u'5사 90% 이상', 3, 2, 3, 8,
  u'두산 인수로 한국 노드가 안정된다'),
 ('specialty-gas', u'특수가스', 'linde', u'린데·에어리퀴드·SK스페셜티 등', u'분산',
  4, 3, 3, 10, None),
 ('polysilicon', u'폴리실리콘', 'wacker-chemie', u'헴록·바커·도쿠야마·OCI', u'분산',
  4, 3, 4, 11, None),
 ('taiwan-power', u'대만 전력·용수', 'taipower', u'대만전력', '100%', 1, 1, 1, 3,
  u'물리적으로 가장 낮은 점수다'),
]
for key, name, subj, holder, share, alt, lead, geo, total, note in BOTTLENECK:
    CLAIMS.append(C(
        'clm-tsmc-bottleneck-' + key,
        u'%s 병목은 %s가 %s 쥐고 대체 가능성 %d·리드타임 %d·지정학 %d 으로 합계 %d 이다.'
        % (name, holder, (u'점유 %s 를 ' % share) if share else u'캐파를 ',
           alt, lead, geo, total),
        subj, '2026-09', 'INFERRED', [L],
        u'점수는 1 이 가장 위험하고 합계가 낮을수록 위험하다. %s' % (note or u'')),
    )
CLAIMS += [
 C('clm-tsmc-bottleneck-top', u'최상위 위험은 대만 전력, EUV 생태계(ASML 과 자이스), '
   u'일본 EUV 소재 네 갈래(블랭크·레지스트·트랙·ABF)이고 세 번째가 가장 과소평가된다.',
   TS, '2026-09', 'INFERRED', [L],
   u'회사별 매출은 작지만 모두 일본 한 나라에 있고 대체재가 없다'),
 # 12·13절 한국 노드
 C('clm-skspecialty-ownership', u'SK스페셜티는 2025년 3월 31일 한앤컴퍼니가 85% 를 약 '
   u'2.6조 원에 인수하고 SK㈜ 가 15% 를 남겨 SK㈜ 연결에서 빠졌다.', 'sk-specialty',
   '2025-03-31', 'CONFIRMED', ['sk_inc_disposal_20250331', L]),
 C('clm-sksiltron-ownership', u'SK실트론은 2025년 12월 두산이 우선협상대상자로 뽑히고 '
   u'2026년 7월 31일 70.6% 지분 2.3조 원 SPA 를 맺어 클로징을 기다린다.', 'sk-siltron',
   '2026-07-31', 'CONFIRMED', ['doosan_disclosure_20260731', L],
   u'4절의 「한앤컴퍼니 유력」 서술은 구정보이고 12절 기준으로 읽는다'),
 C('clm-korea-nodes', u'TSMC 체인에 한국이 직접 걸리는 곳은 웨이퍼(SK실트론)와 '
   u'가스(SK스페셜티) 두 곳뿐이고 둘 다 2025~26년에 SK그룹에서 밖으로 소유권이 옮겼다.',
   TS, '2025~2026', 'INFERRED', [L]),
 C('clm-skhynix-parallel', u'SK하이닉스는 TSMC 공급사가 아니라 TSMC 고객인 엔비디아의 '
   u'병렬 공급사로 CoWoS 에서 합류하는데, HBM4 부터 베이스 다이를 TSMC 로직 공정으로 '
   u'만들면서 직접 거래로 바뀐다.', 'sk-hynix', '2026~2027', 'INFERRED', [L]),
 C('clm-tsmc-excluded-hanmi', u'한미반도체는 TC 본더 주 고객이 SK하이닉스이고 TSMC '
   u'CoWoS 직납이 확인되지 않아 직접 노드로 세우지 않았다.', TS, '2026-09', 'INFERRED',
   [L]),
 C('clm-tsmc-excluded-korea-chem', u'솔브레인·동진쎄미켐·이엔에프테크놀로지는 TSMC 공급사 '
   u'명단에 없고 주 고객이 삼성·SK하이닉스라 이 사슬에서 뺐다.', TS, '2026-09', 'INFERRED',
   [L]),
 C('clm-tsmc-excluded-quartz', u'석영 도가니(신에츠쿼츠·페로텍)와 고순도 석영(시벨코·쿼츠 '
   u'코프)은 원문이 어느 웨이퍼사에 들어가는지 실명으로 짝짓지 않아 관계로 세우지 않았다.',
   TS, '2026-09', 'INFERRED', [L]),
 C('clm-tsmc-excluded-poly', u'폴리실리콘 네 곳(헴록·바커·도쿠야마·OCI) 가운데 원문이 '
   u'웨이퍼사와 실명으로 짝지은 것은 바커–실트로닉 한 쌍뿐이라 나머지는 관계로 세우지 '
   u'않았다.', TS, '2026-09', 'INFERRED', [L]),
 C('clm-oci-indirect', u'OCI홀딩스는 말레이시아 OCIM 폴리실리콘이 주력이 태양광이고 '
   u'반도체용 고순도는 소량이어서 TSMC 체인 기여가 간접적이고 미미하다.', TS, '2025',
   'INFERRED', [L]),
 # 14절 마진 풀
 C('clm-gpu-cost-stack', u'Blackwell 급 AI 가속기 한 개를 따라가면 웨이퍼 소재 약 $50, '
   u'TSMC 로직 다이 두 개 약 $1,300, TSMC CoWoS-L 패키징 약 $1,000, HBM3E 여덟 스택 약 '
   u'$3,500, ABF 기판 약 $200, 후공정·테스트 약 $300, 기타 약 $300 으로 원가가 $6,650 '
   u'가까이 쌓이고 판매가는 $3만~3만5천이다.', 'nvidia', '2026', 'INFERRED', [L],
   u'전부 추정이고 크기 비교용이다'),
 C('clm-gpu-margin-pool', u'가속기 한 개 매출 $32k 의 마진 풀은 엔비디아 약 $25k(78%), '
   u'TSMC 약 $1.4k(4%), SK하이닉스 약 $1.9k(6%), 나머지 공급사 합계 약 $0.5k 로 갈린다.',
   'nvidia', '2026', 'INFERRED', [L]),
 C('clm-tsmc-cost-vs-profit', u'TSMC 는 원가 기준으로 가속기의 약 35% 를 만들지만 이익 '
   u'풀에서는 약 5% 를 가져가고, 그러면서도 매출총이익률 60% 를 지키는 힘은 웨이퍼 1,500만 '
   u'장의 물량과 고정비 흡수다.', TS, '2025~2026', 'INFERRED', [L]),
 C('clm-server-margin', u'DGX 급 8-GPU 서버는 40만~50만 달러이고 폭스콘·콴타의 조립 마진은 '
   u'3~5% 이며 하이퍼스케일러는 이를 자본재로 5년에 나눠 상각한다.', 'foxconn', '2026',
   'INFERRED', [L]),
 C('clm-bargaining-order', u'협상력은 엔비디아(가격 결정) > TSMC·SK하이닉스(캐파 배분권) > '
   u'기판·OSAT(가격 수용) > 웨이퍼·가스(장기계약 고정) 순으로 늘어선다.', TS, '2026',
   'INFERRED', [L]),
 C('clm-price-pass-through', u'TSMC 가 2027년 8% 를 올리면 가속기 원가가 $180 늘어 '
   u'엔비디아 매출총이익률이 75.0% 에서 74.5% 로 내려가는 정도라 거의 흡수된다.', 'nvidia',
   '2027', 'INFERRED', [L],
   u'반면 CoWoS 외주 확대는 외주 원가가 내부보다 커 TSMC 마진에 마이너스다'),
]

# 15절 시나리오
SCEN = [
 ('ai-demand-down', u'AI 수요가 20% 줄면 AI 가 매출의 약 35% 라 매출이 7% 빠지고 가동률이 '
  u'88% 에서 80% 로 내려가 매출 −US$86억·GM −4.5%p·영업이익 −US$65억(−10%)이 된다',
  u'뒷단은 엔비디아·브로드컴 주문이 줄고 앞단은 앰코·SPIL 외주가 먼저 회수되며 ASML EUV '
  u'발주가 미뤄진다'),
 ('power-price-up', u'대만 전기요금이 15% 오르면 유틸리티 약 US$37억 가운데 전력 80% 에 '
  u'붙어 GM −0.4%p·영업이익 −US$4.5억이 된다', u'대만전력과 린데리엔화 원가가 같이 오른다'),
 ('ntd-appreciation', u'NT$ 가 5% 절상되면 회사 가이던스(1% 당 GM −0.4%p)대로 GM −2.0%p·'
  u'영업이익 −US$24억이 된다',
  u'글로벌웨이퍼스·포모사스미코·대만 유통사가 같은 방향으로 눌린다'),
 ('price-hike-2027', u'2027년 단가를 8% 올리면 원가가 그대로라 매출 +US$98억이 마진으로 '
  u'다 들어와 GM +3.2%p·영업이익 +US$98억(+16%)이 된다',
  u'엔비디아 GM 은 0.5%p 내려가고 애플·퀄컴은 스마트폰 BOM 압박을 받는다'),
 ('overseas-fab', u'애리조나·구마모토·드레스덴 램프는 가이던스대로 GM 을 2~3%p 희석해 '
  u'영업이익 −US$30억이 된다', u'미국·일본·독일 현지 인력과 건설비가 늘고 CHIPS 법 '
  u'보조금이 일부를 상쇄한다'),
 ('cowos-up', u'2026년 CoWoS 캐파가 70% 늘면 비웨이퍼 매출 +US$60억에 외주 비중 상승으로 '
  u'GM 이 0.3%p 내려가 영업이익 +US$25억이 된다',
  u'앰코·SPIL 매출이 급증하고 아지노모토 ABF 가 병목이 된다'),
 ('japan-material-stop', u'일본 EUV 소재 수출이 석 달 막히면 7nm 이하 74% 가운데 EUV 노드 '
  u'생산이 멈춰 매출 −US$150억 이상·영업이익 −US$120억 이상이 된다',
  u'11절 병목 표의 최상위 위험이 실현되는 자리이고 재고 한두 달이 완충이다'),
]
for key, body, spread in SCEN:
    CLAIMS.append(C('clm-tsmc-scenario-' + key, body + u'.', TS, '2026~2027', 'INFERRED',
                    [L], u'전파 경로: ' + spread))
CLAIMS.append(C('clm-tsmc-scenario-net', u'단가 인상과 NT$ 절상이 같은 크기로 반대 방향이라 '
                u'2026~27년 마진의 방향은 가격 인상에서 NT$ 절상과 해외팹 희석을 뺀 순합이 '
                u'정하고, 세 항목 모두 물량과 무관하다.', TS, '2026~2027', 'INFERRED', [L]))

# 16절 시간축
TIME = [
 ('2026', u'Capex US$520~640억으로 사상 최대이고 N2 램프와 N2P·A16 하반기 양산, CoWoS 월 '
  u'12~14만 장, 캐파 +3% 가 걸린다. 앞단에는 ASML EUV·High-NA 와 TEL·AMAT·Lam 장비 발주가 '
  u'몰리고 아지노모토·이비덴 ABF 증설, 앰코·SPIL 외주 24~27만 장이 따라온다. 뒷단에는 애플 '
  u'A20(N2), 엔비디아 Rubin(N3), AMD MI400, 하이퍼스케일러 ASIC 2세대가 나온다'),
 ('2027', u'단가 5~10% 인상, 애리조나 Fab2(3nm) 하반기 양산, JASM Fab2(3nm)와 드레스덴 '
  u'ESMC(28·16nm) 가동, A16 확대가 걸린다. 앞단에는 미국·일본·독일 현지 소재·가스 공급망 '
  u'구축과 2026년 Capex 의 감가상각 유입이 오고, 뒷단에서는 3nm 미국산 칩 첫 출하와 '
  u'SK하이닉스 HBM4 베이스 다이 위탁이 시작된다'),
 ('2028', u'A14 양산, 애리조나 Fab3 와 패키징 공장, 두산–SK실트론 언아웃 2년차가 걸린다. '
  u'앞단에는 High-NA EUV 본격 도입으로 ASML·자이스·호야가 걸리고 웨이퍼 EUV 등급 인증이 '
  u'넓어진다. 뒷단에는 2nm 세대 가속기가 나온다'),
 ('2029~2030', u'2030년 재생에너지 목표 경로와 Foundry 2.0 점유 40% 유지 여부가 걸린다. '
  u'앞단에서는 대만 해상풍력 PPA 와 전력 병목 해소가 캐파 상한을 정한다'),
]
for period, body in TIME:
    CLAIMS.append(C('clm-tsmc-timeline-' + period.replace('~', '-'), body, TS, period,
                    'INFERRED', [L]))
CLAIMS.append(C('clm-tsmc-lag-rule', u'장비 발주에서 캐파 가동까지 12~18개월, 감가상각 '
                u'원가 반영까지 18~78개월이 걸려 2025~26년 사상 최대 Capex 는 2027~2031년 '
                u'원가로 남고 그 기간 가동률이 마진의 전부다.', TS, '2025~2031', 'INFERRED',
                [L]))

# 17절 지분·자본
CLAIMS += [
 C('clm-tsmc-stakes', u'TSMC 는 JASM 약 86.5%(소니 6%·덴소 5.5%·도요타 2%), ESMC 약 '
   u'70%(보쉬·인피니온·NXP 각 10%), 애리조나 100%, GUC 약 35%, VIS 약 28%, VisEra 70%대, '
   u'신텍 약 40% 를 쥔다.', TS, '2026-09', 'CONFIRMED', [AR25, L]),
 C('clm-tsmc-stake-logic', u'TSMC 는 뒷단 중개(GUC)와 앞단 성숙 캐파(VIS)를 지분으로 '
   u'통제하고 해외 팹은 고객·정부를 주주로 끌어들여 수요와 정치 위험을 나눈다.', TS,
   '2026-09', 'INFERRED', [L]),
 C('clm-geopolitics-capital', u'일본 정부(JIC→JSR)와 미국 정부(CHIPS→애리조나)가 각각 '
   u'병목 소재와 캐파의 자본 파트너여서 지정학이 지분 구조로 들어와 있다.', TS, '2026-09',
   'INFERRED', [L]),
 C('clm-ase-spil-group', u'ASE 가 SPIL 을 100% 쥐고 있어 CoWoS 외주 두 곳이 사실상 한 '
   u'그룹이고 앰코가 유일한 독립 대안이다.', 'ase', '2026-09', 'INFERRED', [L]),
 C('clm-entegris-cmc', u'공급사 명단의 캐봇마이크로일렉트로닉스는 2022년 합병으로 '
   u'엔테그리스로 읽어야 한다.', 'entegris', '2022', 'INFERRED', [L]),
 C('clm-jsr-jic', u'JSR 은 2024년 일본 정부계 JIC 가 인수해 비상장이 됐고 그 결과 일본 '
   u'정부가 EUV 레지스트 병목을 직접 쥔다.', 'jsr', '2024', 'INFERRED', [L]),
 C('clm-tsmc-open-items', u'2025년 대만 연차보고서 5.3절 공급사 표와 매입 10% 이상 공급사 '
   u'금액, 고객 10-K 역추적, 장비사 지역별 매출 표는 아직 대조하지 않은 자리다.', TS,
   '2026-09', 'INFERRED', [L]),
]


# ── 공급원 분류 — vc_norm 이 옮긴 뒤 이름표와 비중을 얹는다 ───────────
SS_DEFS = [
 (SS_WAFER, u'실리콘 웨이퍼', 'Silicon wafer', 'MATERIAL',
  u'20-F 가 실명을 공개하는 유일한 소재 갈래다'),
 (SS_CHEM, u'화학품', 'Chemicals', 'MATERIAL',
  u'2022년판 대만 연차보고서가 12개사를 실명으로 적었다'),
 (SS_PR, u'포토레지스트', 'Photoresist', 'MATERIAL',
  u'리소그래피 소재 7개사. EUV 레지스트는 일본 3사가 90% 넘게 쥔다'),
 (SS_GAS, u'특수가스', 'Specialty gas', 'MATERIAL',
  u'9개사. 프랙스에어는 린데에 합병돼 따로 서지 않는다'),
 (SS_CMP, u'CMP 소재', 'CMP materials', 'MATERIAL',
  u'7개사. 명단의 캐봇마이크로일렉트로닉스는 엔테그리스로 읽는다'),
 (SS_EQ, u'장비', 'Equipment', 'EQUIPMENT',
  u'capex 가 시차를 두고 감가상각으로 원가에 들어오는 자리다'),
 (SS_BLANK, u'마스크 블랭크·펠리클', 'Mask blank & pellicle', 'MATERIAL',
  u'마스크는 TSMC 자체 마스크샵이 만들고 블랭크와 펠리클을 밖에서 들인다'),
 (SS_ABF, u'ABF 기판·CoWoS 외주', 'ABF substrate & CoWoS outsourcing', 'SUBSYSTEM',
  u'TSMC 매출원가이자 기판사·OSAT 의 매출이다'),
 (SS_UTIL, u'유틸리티', 'Utility', 'OPERATIONAL', u'전력·용수·HVAC'),
 (SS_MEM, u'HBM·메모리(고객이 별도 조달)', 'Memory (customer-sourced)', 'COMPONENT',
  u'TSMC 가 사들이는 품목이 아니라 TSMC 고객이 따로 조달해 CoWoS 에서 합류하는 품목이다'),
]


def share(metric, value, period, ps, pe, aod, den, ev, srcs, note=None,
          low=None, high=None):
    return {'metric': metric, 'value': value, 'value_low': low, 'value_high': high,
            'unit': 'percent', 'period': period, 'period_start': ps, 'period_end': pe,
            'as_of_date': aod, 'denominator': den, 'evidence_level': ev,
            'confidence': 1.0, 'method_note': note, 'source_ids': srcs}


# 알약에 올리는 비중은 2025 매출원가 분모 둘(감가상각·유틸리티)과 웨이퍼 6사 92~96% 뿐이다.
# 2005년 원재료비 구성(웨이퍼 42·화학 20·가스 9)은 스무 해 전 값이라 알약이 아니라 주장
# (clm-tsmc-material-mix-2005)으로만 둔다. 원재료 ~17% 는 다섯 갈래를 합친 몫이라 어느 한
# 분류(웨이퍼)에 달면 그 갈래의 몫처럼 읽힌다 — 주장(9절)으로만 남긴다
SS_SHARES = {
 SS_WAFER: [
  share('supply_share', None, '2020~2022', '2020-01-01', '2022-12-31', '2022-12-31',
        u'TSMC 웨이퍼 수요', 'CONFIRMED', [F20, L],
        u'6개사 합계이고 회사별 몫은 공개되지 않는다', low=92.0, high=96.0),
 ],
 SS_EQ: [
  share('depreciation_cost_share', 45.0, '2025', '2025-01-01', '2025-12-31',
        '2025-12-31', u'TSMC 2025 매출원가', 'INFERRED', [L],
        u'20-F 는 원가를 항목별로 나누지 않는다. 40%대 최대 항목으로 읽힌다'),
 ],
 SS_UTIL: [
  share('utility_cost_share', None, '2025', '2025-01-01', '2025-12-31', '2025-12-31',
        u'TSMC 2025 매출원가', 'INFERRED', [L], u'전기·물·HVAC 합계다', low=7.0, high=8.0),
 ],
}

# ── 매출원 귀속 — 고객마다 어느 매출원에 드는지. 배분 %는 전부 비공개다 ──
RT_NOTE = u'원문 2-1 의 「TSMC에 맡기는 제품」으로 갈래를 정했다. 갈래 안 고객별 배분은 비공개다'
RT_MAP = {}
for _eid, _ev, _cc, _rt, _srcs, _note in T1:
    RT_MAP['tsmc-cust-' + _eid] = [(x, 'INFERRED', 0.6, _srcs, RT_NOTE) for x in _rt]

RT_RESIDUAL = {
 RT_HPC: u'엔비디아·AMD·브로드컴·마벨·인텔·하이퍼스케일러가 이 갈래에 들지만 고객별 배분은 '
         u'비공개라 잔여가 남는다',
 RT_SP: u'애플·퀄컴·미디어텍이 이 갈래에 들지만 고객별 배분은 비공개라 잔여가 남는다',
 RT_IOT: u'미디어텍과 자동차·IoT 칩 회사들이 이 갈래에 들지만 배분은 비공개다',
 RT_AUTO: u'퀄컴과 소니·NXP·인피니온·ST·르네사스가 이 갈래에 들지만 배분은 비공개다',
 RT_DCE: u'실명으로 배분된 고객이 없다',
 RT_ETC: u'실명으로 배분된 고객이 없다',
}


# ── 레코드 만들기 ───────────────────────────────────────────────────
def ent(t):
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
            'legal_name': t[1], 'display_name': t[2] or t[1],
            'region': REGION.get(t[4]) if t[4] else None,
            'parent_entity_id': PARENT.get(t[0]),
            'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
            'country': t[4], 'categories': t[5], 'desc': t[6],
            'anon': t[0] in ANON}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': None, 'accessed_date': ACCESSED,
            'note': t[5]}


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3],
            'period': t[4], 'evidence_level': t[5], 'confidence': t[6],
            'source_ids': t[7], 'note': t[8]}


def evidence():
    out, n = [], 0
    for r in R:
        for sid in r['source_ids']:
            n += 1
            out.append({'id': 'tsmc-e%03d' % n, 'relationship_id': r['id'],
                        'metric_id': None, 'source_id': sid,
                        'evidence_type': ('direct' if r['evidence_level'] == 'CONFIRMED'
                                          else 'indirect'),
                        'evidence': r['notes'] or '', 'hypothesis_id': None})
    for o in O:
        for sid in o['source_ids']:
            n += 1
            out.append({'id': 'tsmc-e%03d' % n, 'relationship_id': o['relationship_id'],
                        'metric_id': o['id'], 'source_id': sid,
                        'evidence_type': 'direct',
                        'evidence': o['method_note'] or '', 'hypothesis_id': None})
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


def apply_supply_classes():
    u"""vc_norm 이 옮긴 분류 레지스트리에 한국어 이름표와 비중을 얹는다. 멱등."""
    cp = os.path.join(CHAIN, 'classifications.json')
    cls = json.load(io.open(cp, encoding='utf-8'))
    by = dict((x['id'], x) for x in cls['supply_sources'])
    for sid, label, label_en, level, note in SS_DEFS:
        x = by.get(sid)
        if x is None:
            x = {'id': sid, 'kind': 'SUPPLY_SOURCE', 'unallocated': False}
            cls['supply_sources'].append(x)
            by[sid] = x
        x['label'], x['label_en'], x['level'], x['note'] = label, label_en, level, note
        x['shares'] = [dict(s) for s in SS_SHARES.get(sid, [])]
        srcs = set()
        for s in x['shares']:
            srcs |= set(s['source_ids'])
        x['source_ids'] = sorted(srcs or {L})
    cls['supply_sources'].sort(key=lambda x: x['id'])
    dump(cp, cls)


def apply_revenue_map():
    u"""귀속별 등급과 배분 미상 잔여를 얹는다. 멱등."""
    rp = os.path.join(CHAIN, 'relationships.json')
    rels = json.load(io.open(rp, encoding='utf-8'))
    for r in rels:
        m = RT_MAP.get(r['id'])
        if not m:
            continue
        r['revenue_type_ids'] = [x[0] for x in m]
        r['revenue_type_map'] = [
            {'id': x[0], 'status': x[1], 'confidence': x[2], 'allocation_value': None,
             'allocation_denominator': u'그 매출원 안 고객별 배분 비공개',
             'source_ids': x[3], 'note': x[4]} for x in m]
    dump(rp, rels)
    cp = os.path.join(CHAIN, 'classifications.json')
    cls = json.load(io.open(cp, encoding='utf-8'))
    for x in cls['revenue_types']:
        if x.get('unallocated'):
            continue
        note = RT_RESIDUAL.get(x['id'])
        if not note:
            continue
        x['residual'] = {'status': 'UNDISCLOSED', 'label': u'배분 미상 잔여',
                         'source_ids': [F20, L], 'note': note}
    dump(cp, cls)
    mp = os.path.join(CHAIN, 'chain.json')
    meta = json.load(io.open(mp, encoding='utf-8'))
    meta['revenue_axis_label'] = u'플랫폼별 매출'
    dump(mp, meta)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'chain.json'),
         {'id': 'tsmc', 'focal_entity': TS, 'label': 'TSMC',
          'note': u'파운드리 한 곳을 중심으로 앞단(소재·장비)과 뒷단(고객·고객의 고객)을 '
                  u'함께 세운 사슬. 2026-09-12 조사 원장이 앵커다'})
    dump(os.path.join(CHAIN, 'relationships.json'), R)
    dump(os.path.join(CHAIN, 'observations.json'), O)
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'hypotheses.json'), [])
    dump(os.path.join(CHAIN, 'projects.json'), [])
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print(u'전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d · 주장 %d'
          % (ne, ns, len(R), len(O), len(CLAIMS)))

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
    apply_supply_classes()
    apply_revenue_map()
    import migrate_vc2
    migrate_vc2.main()
