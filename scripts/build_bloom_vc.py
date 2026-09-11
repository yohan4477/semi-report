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
 ('nash-industries', 'Nash Industries', '내시 인더스트리스', 'company', None, ['Mechanical'],
  '인클로저·섀시·기계 조립'),
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
 # 장비·사이트 전기
 ('coseus', 'Coseus', '코세스', 'company', '한국', ['Manufacturing equipment'],
  '전극셀 코팅 자동화 장비. 제품 BOM 이 아니라 설비 투자'),
 ('ls-electric', 'LS ELECTRIC', 'LS일렉트릭', 'company', '한국·미국', ['Site electrical BoP'],
  '배전반과 배전 변압기'),
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
 # 프로젝트
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
 ('be26_c1', '미상 고객 #1 (2026 H1)', '미상 고객 #1 (2026 H1)', 'company', None, [],
  '2026 상반기 매출의 73%. 비특수관계. SEC 가 법인명을 밝히지 않았다'),
 ('undisclosed-scandium-suppliers', '비공개 스칸듐 공급사', '비공개 스칸듐 공급사', 'company',
  None, ['Raw material'], '복수 국가의 복수 업체라고만 공개'),
]


def ent(t):
    e = {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
         'country': t[4], 'categories': t[5], 'desc': t[6],
         'anon': t[0].startswith('be24_c') or t[0].startswith('be26_c')
                 or t[0] == 'undisclosed-scandium-suppliers'}
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


def merge_global():
    """전역 레지스트리에 덧붙인다. 기존 사슬(NVIDIA)의 항목을 지우지 않는다."""
    ents = json.load(io.open(os.path.join(DATA, 'entities.json'), encoding='utf-8'))
    srcs = json.load(io.open(os.path.join(DATA, 'sources.json'), encoding='utf-8'))
    have_e = set(e['id'] for e in ents)
    have_s = set(s['id'] for s in srcs)
    for t in ENTITIES:
        if t[0] not in have_e:
            ents.append(ent(t))
    for t in SOURCES:
        if t[0] not in have_s:
            srcs.append(src(t))
    dump(os.path.join(DATA, 'entities.json'), ents)
    dump(os.path.join(DATA, 'sources.json'), srcs)
    return len(ents), len(srcs)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne, ns = merge_global()
    print('전역 엔티티 %d · 출처 %d' % (ne, ns))
