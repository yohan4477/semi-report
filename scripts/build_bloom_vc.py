# -*- coding: utf-8 -*-
"""Bloom Energy 사슬을 Drive 조사(01·02·03·04)에서 정규화해 굽는다.

Drive 는 조사·근거 저장소다. 웹은 Drive 를 읽지 않는다 — 여기서 만든 Git JSON 만 읽는다.
Drive 문장을 그대로 옮기지 않고 엔티티·관계·관측·주장·출처·방법 중 어디에 속하는지 갈라 넣는다.
과거 수치를 current 로 올리지 않는다. 없는 값은 채우지 않고 UNKNOWN 으로 남긴다.

  02_Bloom Energy Value Chain  1bWf25JYMIk71UYJJIk-FtPALrOu7fjbBpp76sZWNsoM
  03_Evidence & Sources        1TmF0PFCWFWHYx1gASzKqizUBZMAhJ4MjwwmFgPwHc6M
  04_Entities & Edges          1u250_aBLn8yzhxJrSLuWBxHUQ1MuCJotVjNkhi467XY
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'bloom-energy')

# ── 출처 ────────────────────────────────────────────────────────────
SOURCES = [
 ('be_10k_fy2025', 'Bloom Energy', 'Form 10-K (FY2025)', 'primary_official', '2026-02-09',
  'https://www.sec.gov/Archives/edgar/data/1664703/000162828026006516/be-20251231.htm',
  '매출·고객 집중도·Fund JV·공급망·JV·AEP 역할. 03 의 SRC001'),
 ('be_10k_fy2024', 'Bloom Energy', 'Form 10-K (FY2024)', 'primary_official', '2025-02',
  'https://www.sec.gov/Archives/edgar/data/1664703/000162828025008747/be-20241231.htm',
  '2024 매출·원가·고객 집중도 23/16/14'),
 ('be_10q_2026q2', 'Bloom Energy', 'Form 10-Q (2026 Q2)', 'primary_official', '2026-07',
  'https://www.sec.gov/Archives/edgar/data/1664703/000162828026050325/be-20260630.htm',
  '2026 상반기 매출·고객 집중도 44/21, 비특수관계 고객 73%'),
 ('be_scandium_blog', 'Bloom Energy', 'Demystifying scandium oxide', 'primary_company', '2026',
  'https://www.bloomenergy.com/blog/demystifying-scandium-oxide-why-it-matters-in-bloom-fuel-cells/',
  '스칸듐·지르코니아, 복수국 조달, 25GW, 중국 비의존. 03 의 SRC002'),
 ('sedaily_kr_suppliers', 'Seoul Economic Daily', 'US AI data-center power crunch drives Korean suppliers',
  'reputable_media', '2026-07-29',
  'https://en.sedaily.com/finance/2026/07/29/us-ai-data-center-power-crunch-drives-korean-suppliers',
  'AMOsense·Coseus·Seojin·Bloom 증설. 03 의 SRC003'),
 ('cctc_yicai', 'Yicai', 'CCTC Bloom 공급 관계 보도', 'industry_research', '2025-2026',
  'https://www.yicai.com/brief/102939658.html',
  'CCTC 가 전해질 세라믹 주요 공급사. 점유율은 2차 조사. 03 의 SRC004'),
 ('mtar_ar_fy2425', 'MTAR Technologies', 'Annual Report FY2024-25', 'primary_company', '2025-08',
  'https://mtar.in/wp-content/uploads/2025/08/Annual-Report-FY-2024-25.pdf',
  'Bloom 핫박스 요구량의 50~60%, 전해조 유닛 단독 공급. 03 의 SRC005'),
 ('mtar_ar_fy2024', 'MTAR Technologies', 'Annual Report FY2024', 'primary_company', '2024-08-17',
  'https://mtar.in/wp-content/uploads/2025/03/Annual-Report-FY-2024-Aug-17-2024.pdf',
  'FY24 파워유닛·판금·인클로저 실행액, ASP 어셈블리'),
 ('coseus_kind', 'KRX KIND', 'Coseus 공급계약 공시', 'primary_official', '2026-07-13',
  'https://kind.krx.co.kr/external/2026/07/13/000131/20260713000113/70370.htm',
  '전극셀 코팅 자동화 장비 1억 달러. 03 의 SRC006'),
 ('seojin_kind', 'KRX KIND', '서진시스템 공급계약 공시', 'primary_official', '2026-07-15',
  'https://kind.krx.co.kr/external/2026/07/15/000165/20260715000002/70012.htm',
  'SOFC 모듈·부품 5,263.8만 달러. 03 의 SRC007'),
 ('lselectric_kind', 'KRX KIND', 'LS ELECTRIC 공급계약 공시', 'primary_official', '2026-04-29',
  'https://kind.krx.co.kr/external/2026/04/29/000110/20260428001034/91370.htm',
  '뉴멕시코 배전반·변압기 2억 1,652.6만 달러. 03 의 SRC008'),
 ('be_hitachi_japan', 'Hitachi', 'Hitachi-Bloom onsite power collaboration in Japan',
  'primary_company', '2026-09-01',
  'https://www.hitachi.com/en/press/articles/2026/09/0901b/',
  '일본 온사이트 협업의 노릇 분담, 오미카 실증, 겨냥한 데이터센터·산업 고객. 03 의 SRC048'),
 ('be_power_connect', 'Bloom Energy', 'Bloom Energy introduces Power Connect',
  'primary_company', '2026-08-19',
  'https://www.bloomenergy.com/news/bloom-energy-introduces-power-connect/',
  '전기 통합을 공장으로 옮기는 배치 방식. 회사가 밝힌 설치 시간 40% 이상 단축. 03 의 SRC049'),
 ('coseus_4gw_media', 'Hankyung', 'Coseus 7월 블룸 수주와 4GW 양산 라인 맥락',
  'reputable_media', '2026-07-16',
  'https://www.hankyung.com/article/202607168611O',
  '1억 달러 자동화 패키지가 4GW 양산 라인용이라는 2차 보도. 공시 문구가 아니다. 03 의 SRC050'),
 ('be_aep_1gw', 'Bloom Energy', 'Gigawatt fuel cell procurement agreement with AEP',
  'primary_company', '2024-11-14',
  'https://investor.bloomenergy.com/press-releases/press-release-details/2024/Bloom-Energy-Announces-Gigawatt-Fuel-Cell-Procurement-Agreement-with-AEP-to-Power-AI-Data-Centers/default.aspx',
  '최대 1GW, 초기 100MW. 03 의 SRC009'),
 ('be_sk_eternix_80mw', 'Bloom Energy', "World's largest fuel cell installation",
  'primary_company', '2024-11-07',
  'https://investor.bloomenergy.com/press-releases/press-release-details/2024/Bloom-Energy-Announces-Worlds-Largest-Fuel-Cell-Installation-in-History/default.aspx',
  '한국 80MW, KDB 주도 PF. 03 의 SRC010'),
 ('be_brookfield_25b', 'Bloom Energy', 'Brookfield and Bloom Energy expand AI infrastructure partnership',
  'primary_company', '2026-06-30',
  'https://www.bloomenergy.com/news/brookfield-and-bloom-energy-expand-ai-infrastructure-partnership/',
  '250억 달러 금융 프레임워크. 03 의 SRC011'),
 ('oracle_jupiter', 'Oracle', 'Oracle, BorderPlex and Bloom Energy to power Project Jupiter',
  'primary_company', '2026-04-27',
  'https://www.oracle.com/news/announcement/oracle-borderplex-and-bloom-energy-to-power-project-jupiter-with-fuel-cell-technology-2026-04-27/',
  '뉴멕시코 프로젝트 주피터 최대 2.45GW. 03 의 SRC012'),
 ('be_oracle_28gw', 'Bloom Energy', 'Bloom Energy and Oracle expand strategic partnership',
  'primary_company', '2026-04-13',
  'https://www.bloomenergy.com/news/bloom-energy-and-oracle-expand-strategic-partnership-to-deploy-up-to-2-8-gw-to-accelerate-ai-infrastructure-build-out/',
  '최대 2.8GW, 초기 1.2GW. 03 의 SRC013'),
 ('be_oracle_2025', 'Bloom Energy', 'Oracle and Bloom Energy collaborate', 'primary_company',
  '2025-07-24',
  'https://www.bloomenergy.com/news/oracle-and-bloom-energy-collaborate-to-deliver-power-to-data-centers-at-the-speed-of-ai/',
  '오라클 관계 최초 공식 발표'),
 ('be_equinix_100mw', 'Bloom Energy', 'Bloom expands data center power agreement with Equinix',
  'primary_company', '2025-02-20',
  'https://www.bloomenergy.com/news/bloom-energy-expands-data-center-power-agreement-with-equinix-surpassing-100mw/',
  '100MW 초과, 미국 19개 데이터센터. 03 의 SRC014'),
 ('nebius_be_328mw', 'Nebius', 'Nebius and Bloom Energy partner', 'primary_company', '2026-05-20',
  'https://nebius.com/newsroom/nebius-and-bloom-energy-partner-to-power-ai-infrastructure-build-out',
  '첫 미국 배치 328MW. 03 의 SRC015'),
 ('be_sk_500mw_2023', 'Bloom Energy', 'Bloom Energy and SK ecoplant announce 500MW sales agreement',
  'primary_company', '2023',
  'https://investor.bloomenergy.com/press-releases/press-release-details/2023/Bloom-Energy-and-SK-ecoplant-Announce-500-MW-Sales-Agreement-Strengthening-Existing-Partnership/default.aspx',
  'ASP 앵커로 쓰는 500MW / 약 15억 달러'),
 ('be_10qa_2026q2', 'Bloom Energy', 'Form 10-Q/A (2026 Q2 정정)', 'primary_official',
  '2026-07-29',
  'https://www.sec.gov/Archives/edgar/data/1664703/000162828026050325/be-20260630.htm',
  '정정 공시. 상반기 44%·21%, 2분기 73%. 오라클은 「고객의 고객」 회계처리'),
 ('be_424b7_2026', 'Bloom Energy', 'Form 424B7 (오라클 워런트)', 'primary_official',
  '2026-04-27',
  'https://www.sec.gov/Archives/edgar/data/1664703/000119312526179296/d253699d424b7.htm',
  '2025-07 오라클 공급계약과 2026-03 마스터 서비스 계약'),
 ('aep_ohio_2025', 'AEP Ohio', 'AEP 오하이오 온사이트 전력 프로젝트 발표', 'primary_company',
  '2025-06-05', 'https://www.aep.com/news/stories/view/10262/',
  'AEP 오하이오가 AWS·콜로직스 부지에 블룸 연료전지를 설치한다. 최종 고객이 비용을 댄다'),
 ('kaori_ar_fy2025', 'Kaori Heat Treatment', '2025 연차보고서', 'primary_company', '2026',
  'https://www.kaori.com.tw/tw/uploads/filelist/1000/2/1778739932_dc80eed76adc9748.pdf',
  '블룸향 매출 NT$26.496억으로 Kaori 순매출의 40.26%. 2024 년은 NT$18.735억·28.47%'),
 ('cctc_ipo_2014', 'CCTC', 'IPO 공모설명서 고객 공시', 'primary_official', '2014',
  'https://money.finance.sina.com.cn/corp/view/vISSUE_RaiseExplanationDetail.php'
  '?id=1558553&stockid=300408',
  '2014 상반기 블룸이 CCTC 1위 고객이고 매출의 9.54%'),
 ('customs_sanmina_2026', 'ImportInfo', '산미나 인도 통관 기록', 'trade_data', '2026',
  'https://www.importinfo.com/sanmina-sci-india-private-limited',
  '정지형 컨버터·CCE CORVA 직접 선적. 선적 건수는 조달 비중이 아니다'),
 ('customs_acbel_2026', 'ImportInfo', '캐벨 통관 기록', 'trade_data', '2026',
  'https://www.importinfo.com/acbel-polytech-inc',
  '캐벨의 블룸 직접 선적. 캐벨에서 산미나로 가는 계층 증거는 없다'),
 ('customs_nash_2026', 'ImportGenius', '내시 인더스트리스 통관 기록', 'trade_data', '2026',
  'https://www.importgenius.com/suppliers/nash-industries-i-pvt-ltd',
  'KPE·CM2 산타크루즈와 CCE+1 인클로저 직접 선적'),
 ('customs_texon_2026', 'Seair', '텍슨 통관 기록', 'trade_data', '2026',
  'https://www.seair.co.in/us-import/i-bloom-energy-corp/e-texon.aspx',
  '강판 전기 인클로저·KPE 도어·측면 패널 직접 선적'),
 ('texon_history', 'Texon', '회사 연혁', 'primary_company', '2026',
  'https://www.texon.co.kr/en/history/',
  '2015-12 최대주주가 서진시스템으로 바뀌었다'),
 ('seojin_ar_2025', 'KRX KIND', '서진시스템 2025 사업보고서', 'primary_official', '2026-03-23',
  'https://kind.krx.co.kr/external/2026/03/23/002251/20260323009399/11011.htm',
  '텍슨과 텍슨 반도체가 서진 연결 자회사다'),
 ('patent_stackpole', 'Google Patents', '블룸·스택폴 금속 인터커넥트 공동 특허',
  'primary_official', '2015~2018', 'https://patents.google.com/patent/US20150244004A1/en',
  '2014~2018 기술 공동개발을 확인한다. 조달 점유율 근거는 아니다'),
 ('porite_2026_note', 'Porite Taiwan', 'SOFC 공급사 공지', 'primary_company', '2026-05-11',
  'https://tw.porite.com/en-US/newsc27-the-growing-demand-for-sofc-systems-in-taiwan-and-the-role-of-powder-metallurgy-components',
  '블룸 인터커넥트 플레이트 장기 공급사임을 회사가 밝힌다'),
 ('customs_porite_2026', 'Seair', '포리테 통관 기록', 'trade_data', '2025-2026',
  'https://www.seair.co.in/us-import/i-bloom-energy-corp/e-por.aspx',
  '2026 년 8월까지 직접 선적. 관계가 살아 있다는 신호일 뿐 점유율이 아니다'),
 # ── 2026-09-11 조사분 — 03 의 SRC030~SRC047 ──────────────────────
 ('tarifflo_q1_2026', 'Tarifflo', 'Bloom 1분기 공급사 통관 스냅샷', 'trade_data', '2026 Q1',
  'https://www.tarifflo.com/trade-data/bloom-energy-15e60e',
  '공급사 수와 선적 건수다. 금액 비중이 아니다'),
 ('importinfo_bloom_list', 'ImportInfo', 'Bloom 수입자 공급사 목록', 'trade_data', '2026-09',
  'https://www.importinfo.com/bloom-energy-corporation',
  '2026 년 8~9월까지 활동. 선적 건수는 금액 비중이 아니다'),
 ('importgenius_bloom_hist', 'ImportGenius', 'Bloom 수입 이력', 'trade_data', '2026-09',
  'https://www.importgenius.cn/importers/bloom-energy-corporation',
  'MTAR·Kaori·산미나·캐벨·둥관자펑이 최근까지 나온다'),
 ('customs_jiafeng_2026', 'Seair', '둥관자펑 통관 기록', 'trade_data', '2026',
  'https://www.seair.co.in/us-import/i-bloom-energy-bldg/e-dongguan-jiafeng-mechanical-equipme.aspx',
  'CM1 빌드베이스 키트·측면 패널·워터 스키드 접합 조립품 직접 선적'),
 ('customs_cumi_2026', 'Seair', 'CUMI 엔지니어링 세라믹 통관 기록', 'trade_data', '2026',
  'https://www.seair.co.in/us-import/product-engineering/i-bloom-energy-3way-logistics-ftz.aspx',
  'Bloom 3Way Logistics FTZ 로 반복 선적'),
 ('customs_mingrui_2026', 'Mati Logistics', '융저우밍루이 통관 기록', 'trade_data', '2026',
  'https://www.matilogistics.com/supplier/yongzhou-mingrui-ceramic-technology',
  '기술 세라믹 플레이트 선적의 매입자가 Bloom 이다. 어느 계통에 쓰이는지는 안 나온다'),
 ('be_coreweave_2024', 'Bloom Energy', 'Bloom·코어위브 파트너십 발표', 'primary_company',
  '2024-07-16',
  'https://www.bloomenergy.com/news/bloom-energy-and-coreweave-partner-to-revolutionize-ai-data-center-power-solutions/',
  '치리사가 가진 일리노이 볼로 부지에서 코어위브가 쓴다'),
 ('equinix_own_2025', 'Equinix', '에퀴닉스 자체 발표', 'primary_company', '2025-08-14',
  'https://investor.equinix.com/news-events/press-releases/detail/1079/equinix-collaborates-with-leading-alternative-energy',
  '100MW 를 넘는 블룸 계약을 에퀴닉스가 직접 확인한다'),
 ('be_conflict_minerals_2025', 'Bloom Energy', '2025 분쟁광물 보고서 (Form SD 별지 1.01)',
  'primary_official', '2026-06-01',
  'https://www.sec.gov/Archives/edgar/data/1664703/000119312526251628/d61094dex101.htm',
  '2026-04-23 기준 실사 대상 공급사 136곳. 3TG 실사 분모이지 1차 협력사 총수가 아니다'),
 ('customs_cypress_2026', 'ImportKey', '사이프러스 통관 기록', 'trade_data', '2026-09',
  'https://importkey.com/i/cypress-industries-india-pvt-ltd',
  '2026 년 9월 와이어 하네스 직접 선적'),
 ('customs_unicorn_2026', 'ImportInfo·Seair', '유니콘 통관 기록', 'trade_data', '2026-09',
  'https://www.importinfo.com/unicorn-insulations-sdn-bhd',
  '미세다공 단열재 직접 선적. 관계가 살아 있다'),
 ('customs_wolfe_2026', 'Seair', '울프 엔지니어링 통관 기록', 'trade_data', '2025-2026',
  'https://www.seair.co.in/us-import/product-exhaust/e-wolfe-engineering-shanghai-co-limited.aspx',
  '발전기 배기관 직접 선적'),
 ('customs_thermocouple_2026', 'Seair', '열전대 통관 기록', 'trade_data', '2026',
  'https://www.seair.co.in/us-import/product-thermocouple/i-bloom-energy.aspx',
  '저장휘 춘후이와 오카자키의 열전대가 반복 선적된다'),
 ('thebell_hansun_2026', '더벨', '한선엔지니어링 블룸 글로벌 공급사 인증', 'reputable_media',
  '2026-06-24',
  'https://www.thebell.co.kr/front/newsview.asp?code=0104&key=202606231744045760105369',
  '배관 모듈 공급사로 인증을 받았다'),
 ('be_mitac_2026', 'Bloom Energy', 'Bloom·마이택 파트너십 확대 발표', 'primary_company',
  '2026-08-06',
  'https://investor.bloomenergy.com/press-releases/press-release-details/2026/Bloom-Energy-Continues-to-Set-the-Standard-for-AI-Onsite-Power-with-Expanded-MiTAC-Partnership/default.aspx',
  '프리몬트 AI 서버 캠퍼스에 섬형 마이크로그리드. 산호세 설치는 이미 있던 것'),
 ('customs_microsensor_2026', 'Seair', '마이크로센서 통관 기록', 'trade_data', '2026',
  'https://www.seair.co.in/us-import/i-bloom-energy-corp/e-micro-sensor-co-limited.aspx',
  '레벨 트랜스미터 직접 선적'),
 ('cw_porite_2024', 'CommonWealth Magazine', 'Taiwan supply chain 현장 취재', 'industry_research',
  '2024-10-02', 'https://english.cw.com.tw/article/article.action?id=3781',
  'Porite 와 캐나다 공급사가 당시 대략 50:50, 연 1,000만 장 근처, 650kW 당 3만 장'),
 ('kgi_kaori_2024', 'KGI', 'Kaori Heat Treatment (8996 TT)', 'analyst_estimate', '2024-06-06',
  'https://www.kgi.com.hk/en/-/media/files/kgishk/research-reports/tw-reports/2024/01/kaori-heat-treatment_8996-tt_06062024.pdf',
  'Kaori 의 Bloom 관련 매출 전망 2024F~2026F. 실적이 아니라 2024년 시점 전망'),
 ('aep_ohio_release', 'AEP Ohio', 'AEP Ohio 온사이트 연료전지 프로젝트 발표', 'primary_company',
  '2025', None, '04 에 URL 없이 이름만 적혀 있다'),
]

# ── 엔티티 ──────────────────────────────────────────────────────────
# (id, 이름, 한국어 이름, 유형, 나라, 카테고리, 메모)
ENTITIES = [
 ('bloom-energy', 'Bloom Energy', '블룸에너지', 'company', '미국', ['Integrator'],
  'SOFC·SOEC 제조와 시스템 통합. 셀/공정 IP·제어·설치·서비스를 쥔 중심 노드'),
 ('bloom-sk-fuel-cell', 'Bloom SK Fuel Cell LLC', '블룸SK퓨얼셀', 'jv', '한국', ['Assembly'],
  '2019 설립, 2020 가동, 2023 한국 시설 범위를 full assembly 로 확대'),
 ('bloom-energy-india', 'Bloom Energy India', '블룸에너지 인도', 'company', '인도',
  ['Power electronics'], '전력 조절·제어 시스템 활동 확인'),
 # 원재료
 ('scandium-oxide', 'Scandium oxide', '산화스칸듐', 'material', None, ['Raw material'],
  '복수국 복수 공급사, 업체명·물량 비공개. 산업 부산물 회수 기반'),
 ('zirconium-oxide', 'Zirconium oxide', '산화지르코늄', 'material', None, ['Raw material'],
  '초박형 세라믹 기판의 기반 물질. 벤더 비공개'),
 ('scsz-electrolyte', 'Scandia-stabilized zirconia electrolyte', '스칸디아 안정화 지르코니아',
  'material', None, ['Material processing'],
  '지르코니아에 산화스칸듐을 조금 섞은 전해질 소재. 조성과 공정은 Bloom 핵심 기술'),
 ('cr-fe-alloy', 'Cr / Fe alloy', '크롬·철 합금', 'material', None, ['Raw material'],
  '인터커넥트 플레이트의 모재. 공급사는 공개되지 않았다'),
 ('natural-gas', 'Natural gas', '천연가스', 'material', None, ['Operational input'],
  '제조 BOM 이 아니라 운영 투입'),
 ('biogas', 'Biogas', '바이오가스', 'material', None, ['Operational input'], None),
 ('hydrogen', 'Hydrogen', '수소', 'material', None, ['Operational input'],
  '혼소 수소 포함'),
 # 셀·세라믹
 ('cctc', 'Chaozhou Three-Circle Group (CCTC)', '차오저우 싼환', 'company', '중국', ['Cell'],
  '전해질 세라믹 격막 주요 공급사. 공식 점유율 비공개'),
 ('amosense', 'AMOsense', '아모센스', 'company', '한국', ['Cell'],
  '2026 신규 진입. 월 20만 → 60만 장'),
 ('yongzhou-mingrui', 'Yongzhou Mingrui Ceramic', '융저우 밍루이 세라믹', 'company', '중국',
  ['Other ceramic'], '세라믹 플레이트·심. 전해질 기판과 별개'),
 ('cumi', 'Carborundum Universal (CUMI)', 'CUMI', 'company', '인도', ['Other ceramic'],
  '고알루미나 엔지니어링·내화 세라믹. 실 공급사로 단정하지 않는다'),
 ('unicorn-insulations', 'Unicorn Insulations', '유니콘 인슐레이션', 'company', None,
  ['Thermal'], '단열재'),
 # 부품·계통 — 공급사를 중심에 바로 붙이지 않으려고 두는 층 (04 의 E027~E032)
 ('cmp-electrolyte-substrate', 'SOFC ceramic electrolyte substrate', 'SOFC 전해질 세라믹 기판',
  'component', None, ['Cell'], '셀 공급사의 관측이 붙는 자리. 블룸 셀 공정으로 들어간다'),
 ('cmp-interconnect-plate', 'SOFC metallic interconnect plate', 'SOFC 금속 인터커넥트 플레이트',
  'component', None, ['Interconnect'], '성형과 표면 처리를 거쳐 인터커넥트 계통으로 간다'),
 ('sub-cell', 'Cell / electrochemical subsystem', '셀·전기화학 계통', 'subsystem', None,
  ['Cell'], None),
 ('sub-interconnect', 'Interconnect system', '인터커넥트 계통', 'subsystem', None,
  ['Interconnect'], '원가 모델의 계통 층이다. 공급사 조달 배분과 섞지 않는다'),
 ('sub-hotbox', 'Hotbox / power unit', '핫박스·파워유닛 계통', 'subsystem', None, ['Hotbox'],
  'MTAR·가오리 점유율의 분모가 여기 있다'),
 ('sub-power-electronics', 'Power electronics / power conditioning', '전력 전자 계통',
  'subsystem', None, ['Power electronics'], '캐벨에서 산미나로 가는 계층은 근거가 없어 안 잇는다'),
 ('sub-mechanical', 'Mechanical / module BoP', '기계·모듈 계통', 'subsystem', None,
  ['Mechanical'], '서진·내시·텍슨의 상하 관계는 미확정이라 나란히 둔다'),
 # 인터커넥트
 ('porite-taiwan', 'Porite Taiwan', '포리테 대만', 'company', '대만', ['Interconnect'],
  '크롬 합금 인터커넥트 플레이트 장기 공급사'),
 ('stackpole-intl', 'Stackpole International Powder Metal', '스택폴', 'company', '캐나다',
  ['Interconnect'], 'Bloom 과의 금속 인터커넥트 공동 특허로 추정한 캐나다 공급사 후보'),
 ('plus-metal-tech', 'Plus Metal Tech', '플러스메탈텍', 'company', None, ['Interconnect'],
  '인터커넥트 표면 코팅·관련 플레이트'),
 # 핫박스
 ('mtar-technologies', 'MTAR Technologies', 'MTAR', 'company', '인도', ['Hotbox'],
  '핫박스·파워유닛·판금·인클로저·ASP 어셈블리·SOEC 부품'),
 ('kaori-heat-treatment', 'Kaori Heat Treatment', '가오리', 'company', '대만', ['Hotbox'],
  'Bloom 핫박스 주요 공급사. 현재 조달 점유율 비공개'),
 # 전력 전자
 ('acbel-polytech', 'AcBel Polytech', '캐벨', 'company', '대만', ['Power electronics'],
  '전력 변환·전원 공급'),
 ('sanmina-sci-india', 'Sanmina-SCI India', '산미나 인도', 'company', '인도',
  ['Power electronics'], '정지형 컨버터와 DC-DC 어셈블리 반복 공급'),
 ('cypress-industries', 'Cypress Industries', '사이프러스 인더스트리스', 'company', None,
  ['Power electronics'], '와이어 하네스'),
 # 기계·모듈
 ('seojin-system', 'Seojin System', '서진시스템', 'company', '한국·베트남', ['Mechanical'],
  '셀 제외 주요 부품·모듈. 베트남 공장 EXW 로 미국 공급'),
 ('nash-industries', 'Nash Industries (I) Pvt Ltd', '내시 인더스트리스', 'company', '인도',
  ['Mechanical'], 'CCE 인클로저·KPE 도어·CM 어셈블리를 블룸에 직접 보낸다'),
 ('texon', 'Texon', '텍손', 'company', None, ['Mechanical'],
  '강판 전기·기계 인클로저, 도어, KPE 인클로저'),
 ('hansun-engineering', 'Hansun Engineering', '한선엔지니어링', 'company', '한국', ['Mechanical'],
  '연료·가스 분배 배관 모듈, 피팅, 밸브'),
 ('technoflex-tf-vietnam', 'Technoflex / TF Vietnam', '테크노플렉스', 'company', '중국·베트남',
  ['Thermal'], '발전기 배기 연결'),
 # 계측
 ('zhejiang-chunhui', 'Zhejiang Chunhui Instrumentation', '저장 춘후이', 'company', '중국',
  ['Instrumentation'], '열전대'),
 ('okazaki-mfg', 'Okazaki Manufacturing', '오카자키 제작소', 'company', '일본',
  ['Instrumentation'], '열전대'),
 ('micro-sensor', 'Micro Sensor', '마이크로센서', 'company', '중국', ['Instrumentation'],
  '레벨 트랜스미터'),
 ('protechnic-wujiang', 'Protechnic Electric Wujiang', '프로테크닉', 'company', '중국',
  ['Thermal'], 'DC 팬 공급 이력. 현재 주력 여부 불확실'),
 # ── 2026-09-11 조사분 — 04 의 E044·E047·E048·E051·E052·E055~E058 ──
 ('dongguan-jiafeng', 'Dongguan Jiafeng Mechanical Equipment', '둥관자펑', 'company', '중국',
  ['Mechanical'], 'CM1 빌드베이스 키트·패널·워터 스키드 접합 조립품. 조달 몫은 모른다'),
 ('wolfe-engineering-shanghai', 'Wolfe Engineering (Shanghai) Co., Ltd.', '울프 엔지니어링',
  'company', '중국', ['Mechanical'], '발전기 배기관. 2025~2026 직접 선적'),
 ('chirisa', 'Chirisa Technology Parks', '치리사 테크놀로지 파크스', 'company', '미국',
  ['Data center'], '일리노이 볼로 데이터센터 부지를 가진 곳이다'),
 ('volo-datacenter', 'Volo, Illinois Data Center', '볼로 데이터센터', 'project_spv', '미국',
  ['Project'], '치리사가 갖고 코어위브가 쓰는 AI 데이터센터. 블룸 연료전지가 들어간다'),
 ('mitac-computing', 'MiTAC Computing Technology Corp.', '마이택 컴퓨팅', 'company', '미국',
  ['Data center'], 'AI 서버를 만든다. 블룸 온사이트 발전을 쓴다'),
 ('mitac-fremont', 'MiTAC Fremont AI Server Manufacturing Campus', '마이택 프리몬트 캠퍼스',
  'project_spv', '미국', ['Project'], '섬형 연료전지 마이크로그리드. 2026-08-06 발표'),
 ('mitac-sanjose', 'MiTAC San Jose Manufacturing Facility', '마이택 산호세 공장',
  'project_spv', '미국', ['Project'], '2026 확대 발표에 나오는 기존 설치 자리'),
 ('cmp-engineering-ceramics', 'Engineering ceramics', '엔지니어링 세라믹', 'material', None,
  ['Other ceramic'], 'CUMI 선적을 받는 자리. 어느 계통에 놓이는지는 추론이다'),
 ('cmp-ceramic-plate', 'Technical ceramic plate / shim', '기술 세라믹 플레이트·심', 'material',
  None, ['Other ceramic'], '밍루이 선적을 받는 자리. 어느 계통에 놓이는지는 추론이다'),
 # 장비·사이트 전기
 ('coseus', 'Coseus', '코세스', 'company', '한국', ['Manufacturing equipment'],
  '전극셀 코팅 자동화 장비. 제품 BOM 이 아니라 설비 투자'),
 ('ls-electric', 'LS ELECTRIC', 'LS일렉트릭', 'company', '한국', ['Site electrical BoP'],
  '배전반·배전 변압기 모회사. 블룸 프로젝트를 딴 곳은 미국 법인이다'),
 ('ls-electric-america', 'LS ELECTRIC AMERICA Inc.', 'LS일렉트릭 아메리카', 'company', '미국',
  ['Site electrical BoP'], '블룸이 발주한 북미 데이터센터 전력 설비 프로젝트를 수주했다'),
 ('texon-semiconductor-vn', 'Texon Semiconductor Technologies', '텍슨 반도체', 'company',
  '베트남', ['Mechanical'], '텍슨의 베트남 제조 법인'),
 # 매출 유형 — 회계상 매출원. 회사가 아니라 층이다 (05 §28)
 ('be-rev-product', 'Product revenue', '제품 매출', 'revenue_type', None, ['Revenue type'],
  'Energy Server·전해조 장비 판매'),
 ('be-rev-installation', 'Installation revenue', '설치 매출', 'revenue_type', None,
  ['Revenue type'], '현장 설치 역무'),
 ('be-rev-service', 'Service revenue', '서비스 매출', 'revenue_type', None, ['Revenue type'],
  '유지·보수와 성능 보증'),
 ('be-rev-electricity', 'Electricity revenue', '전력 매출', 'revenue_type', None,
  ['Revenue type'], '직접 보유·운영 설비에서 파는 전기'),
 ('be-rev-unallocated', 'Unallocated / undisclosed', '배분 미상', 'revenue_type', None,
  ['Revenue type'], '어느 매출원에서 나왔는지 공개되지 않은 고객이 앉는 자리'),
 # 다운스트림 — 금융
 ('brookfield', 'Brookfield', '브룩필드', 'company', '글로벌', ['Financing'],
  '펀드 스폰서. 250억 달러 프레임워크'),
 ('brookfield-fund-jvs', 'Brookfield-related Fund JVs', '브룩필드 계열 펀드 JV', 'fund_jv',
  '미국·글로벌', ['Financing'], '계약상 고객이자 자산 보유 주체. 스폰서와 분리해 둔다'),
 ('kdb', 'Korea Development Bank', '산업은행', 'financial_institution', '한국', ['Financing'],
  'SK 에너닉스 80MW 프로젝트 금융 주선'),
 ('southern-company', 'Southern Company', '서던컴퍼니', 'company', '미국', ['Financing'],
  '과거 제3자 금융 관계'),
 ('duke-energy', 'Duke Energy', '듀크에너지', 'company', '미국', ['Financing'],
  '과거 제3자 금융 관계'),
 ('exelon', 'Exelon', '엑셀론', 'company', '미국', ['Financing'], '과거 제3자 금융 관계'),
 # 다운스트림 — EPC·유통
 ('hitachi', 'Hitachi, Ltd.', '히타치', 'company', '일본',
  ['System integrator', 'Channel partner'],
  '일본 온사이트 연료전지의 기획·설계·제어 통합과 운영 지원을 맡는다. 계약 고객이라는 근거는 없다'),
 ('hitachi-omika-works', 'Hitachi Omika Works', '히타치 오미카 공장', 'project_spv', '일본',
  ['Project'],
  '이바라키 실증 부지. 블룸 연료전지에 히타치 제어를 붙여 원격 출력 조정과 상태 감시를 확인했다. 용량은 비공개'),
 ('sk-ecoplant', 'SK ecoplant', 'SK에코플랜트', 'company', '한국', ['EPC / Distribution'],
  '한국 우선 유통·EPC 이자 전략 파트너'),
 ('sk-ecoplant-americas', 'SK ecoplant Americas', 'SK에코플랜트 아메리카스', 'company', '미국',
  ['EPC / Distribution'], '미국 프로젝트 시공 관리·EPC·금융 서비스'),
 ('sk-eternix', 'SK Eternix', 'SK에너닉스', 'company', '한국', ['EPC / Distribution'],
  '한국 개발사·유통사. 충주 40MW + 대소원 40MW'),
 # 다운스트림 — 유틸리티
 ('aep', 'American Electric Power', 'AEP', 'utility', '미국', ['Utility'],
  '유틸리티이자 채널이자 금융 파트너. 역할은 엣지마다 다르다'),
 ('aep-ohio', 'AEP Ohio', 'AEP 오하이오', 'utility', '미국', ['Utility'],
  '중부 오하이오 온사이트 연료전지 프로젝트'),
 # 프로젝트·SPV
 ('sk-eternix-80mw', 'SK Eternix 80MW Korea project', '충주·대소원 80MW 프로젝트',
  'project_spv', '한국', ['Project'],
  '충주 40MW + 대소원 40MW. 산업은행 주도 PF'),
 ('bfjv-spv-unknown', 'Fund JV project SPV (미상)', '펀드 JV 프로젝트 법인 (미상)',
  'project_spv', None, ['Project'],
  '펀드 JV 아래에 프로젝트 법인이 선다고 원문이 말하지만 법인명은 공개되지 않았다'),
 ('project-jupiter', 'Project Jupiter', '프로젝트 주피터', 'project_spv', '미국', ['Project'],
  '뉴멕시코. Oracle·BorderPlex·Bloom 구조, 최대 2.45GW 마이크로그리드 계획'),
 ('borderplex', 'BorderPlex', '보더플렉스', 'company', '미국', ['Project'],
  '프로젝트 주피터 개발 주체'),
 # 최종 고객
 ('oracle', 'Oracle', '오라클', 'end_user', '미국', ['Data center'],
  '최대 2.8GW, 초기 1.2GW 계약·배치 중'),
 ('equinix', 'Equinix', '에퀴닉스', 'end_user', '미국·글로벌', ['Data center'],
  '약 75MW 가동 + 30MW 공사 중'),
 ('nebius', 'Nebius', '네비우스', 'end_user', '미국·글로벌', ['Data center'],
  '첫 미국 배치 328MW'),
 ('aws', 'AWS', 'AWS', 'end_user', '미국·글로벌', ['Data center'],
  'AEP 오하이오 프로젝트. 장기 계약으로 비용 부담'),
 ('cologix', 'Cologix', '콜로직스', 'end_user', '미국', ['Data center'],
  'AEP 오하이오 프로젝트'),
 ('coreweave', 'CoreWeave', '코어위브', 'end_user', '미국', ['Data center'],
  'Bloom 이 공개한 데이터센터 고객'),
 ('intel', 'Intel', '인텔', 'end_user', '미국', ['Data center'], None),
 ('att', 'AT&T', 'AT&T', 'end_user', '미국', ['Data center'], None),
 ('verizon', 'Verizon', '버라이즌', 'end_user', '미국', ['Data center'], None),
 ('quanta-computer', 'Quanta Computer', '콴타컴퓨터', 'end_user', '대만', ['C&I'],
  '2024 기존 계약 확대. AI 하드웨어 제조 시설 용량 150% 이상 증가'),
 ('walmart', 'Walmart', '월마트', 'end_user', '미국', ['C&I'], None),
 ('home-depot', 'The Home Depot', '홈디포', 'end_user', '미국', ['C&I'], None),
 ('ferrari', 'Ferrari', '페라리', 'end_user', '이탈리아', ['C&I'], None),
 ('fedex', 'FedEx', '페덱스', 'end_user', '미국', ['C&I'], None),
 # 익명
 ('be24_c2', '미상 고객 #2 (FY2024)', '미상 고객 #2 (FY2024)', 'company', None, [],
  'FY2024 매출의 16%. 공개 자료로 법인 특정 불가'),
 ('be24_c3', '미상 고객 #3 (FY2024)', '미상 고객 #3 (FY2024)', 'company', None, [],
  'FY2024 매출의 14%. 공개 자료로 법인 특정 불가'),
 ('be25_c2', '미상 고객 #2 (FY2025)', '미상 고객 #2 (FY2025)', 'company', None, [],
  'FY2025 총매출의 13%. SEC 가 법인명을 밝히지 않는다'),
 ('be25_c3', '미상 고객 #3 (FY2025)', '미상 고객 #3 (FY2025)', 'company', None, [],
  'FY2025 총매출의 12%. SEC 가 법인명을 밝히지 않는다'),
 ('be26_c1', '미상 고객 #1 (2026 H1)', '미상 고객 #1 (2026 H1)', 'company', None, [],
  '2026 상반기 매출의 73%. 비특수관계. SEC 가 법인명을 밝히지 않았다'),
 ('undisclosed-scandium-suppliers', '비공개 스칸듐 공급사', '비공개 스칸듐 공급사', 'company',
  None, ['Raw material'], '복수 국가의 복수 업체라고만 공개'),
]


# 법인 관계 — 브랜드가 같아도 법인이 다르면 다른 노드다 (§3-A)
PARENT = {
 'bloom-energy-india': 'bloom-energy',
 'ls-electric-america': 'ls-electric',
 'texon': 'seojin-system',
 'texon-semiconductor-vn': 'texon',
 'sk-ecoplant-americas': 'sk-ecoplant',
 'aep-ohio': 'aep',
 'brookfield-fund-jvs': 'brookfield',
}
REGION = {
 '미국': 'North America', '캐나다': 'North America', '한국': 'Korea', '중국': 'China',
 '대만': 'Taiwan', '일본': 'Japan', '인도': 'India', '이탈리아': 'Europe',
 '네덜란드': 'Europe', '글로벌': 'Global',
}


def region_of(country):
    if not country:
        return None
    rs = []
    for part in country.split('·'):
        r = REGION.get(part.strip())
        if r and r not in rs:
            rs.append(r)
    return '·'.join(rs) or None


def ent(t):
    e = {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
         'legal_name': t[1], 'display_name': t[2] or t[1],
         'region': region_of(t[4]), 'parent_entity_id': PARENT.get(t[0]),
         'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
         'country': t[4], 'categories': t[5], 'desc': t[6],
         'anon': t[0].startswith('be24_c') or t[0].startswith('be26_c')
                 or t[0].startswith('be25_c')
                 or t[0] in ('undisclosed-scandium-suppliers', 'bfjv-spv-unknown')}
    return e


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-11', 'note': t[6]}


def dump(path, obj):
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        os.makedirs(d)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))
        f.write(u'\n')


def normalize(e):
    """프레임워크 §8 이 요구하는 칸을 채운다. 다른 사슬이 넣은 항목도 여기서 맞춘다."""
    e.setdefault('legal_name', e.get('name') or e['id'])
    e.setdefault('display_name', e.get('name_ko') or e.get('name') or e['id'])
    if not e.get('legal_name'):
        e['legal_name'] = e.get('name') or e['id']
    if not e.get('display_name'):
        e['display_name'] = e.get('name_ko') or e.get('name') or e['id']
    e.setdefault('region', region_of(e.get('country')))
    e.setdefault('parent_entity_id', PARENT.get(e['id']))
    cats = e.get('categories') or []
    e.setdefault('primary_role', cats[0] if cats else None)
    e.setdefault('other_roles', cats[1:])
    return e


def merge_global():
    """전역 레지스트리를 갱신한다. 이 스크립트가 맡은 항목은 덮어쓴다."""
    ents = json.load(io.open(os.path.join(DATA, 'entities.json'), encoding='utf-8'))
    srcs = json.load(io.open(os.path.join(DATA, 'sources.json'), encoding='utf-8'))
    mine_e = dict((t[0], ent(t)) for t in ENTITIES)
    mine_s = dict((t[0], src(t)) for t in SOURCES)
    ents = [mine_e.pop(e['id'], e) for e in ents]
    ents += [mine_e[k] for k in mine_e]
    srcs = [mine_s.pop(x['id'], x) for x in srcs]
    srcs += [mine_s[k] for k in mine_s]
    ents = [normalize(e) for e in ents]
    dump(os.path.join(DATA, 'entities.json'), ents)
    dump(os.path.join(DATA, 'sources.json'), srcs)
    return len(ents), len(srcs)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne, ns = merge_global()
    print('전역 엔티티 %d · 출처 %d' % (ne, ns))

    # 재료를 다시 쌓았으면 v2 꼴로 바로 옮긴다 — 옮기는 일을 사람 손에 맡기면
    # 다음 build 때 공급원·매출원이 상자로 되살아난다(프레임워크 §13)
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
