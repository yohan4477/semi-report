# -*- coding: utf-8 -*-
"""AI 클라우드 사슬 — Nebius.

Drive `value chain 분석/Nebius` 의 01~05 가 canonical 이다. 거기 있는 것만 옮긴다.
  01_Nebius 조사 추적과정                17a7WI5jAsf1qSXbrc4QvVp4Ecz4xJRLnjJJKr2Ju6xI
  02_Nebius Value Chain                 1LnXHLWatbal-_0RLApOOwRw8KBXfEH6rQv-ozQ70P6k
  03_Nebius Evidence & Sources          (같은 폴더)
  04_Nebius Entities & Edges            1r53THYQ_RKAK0mZ0o-isnoYQX81dlB_pE-rdYpSaoLM
  05_Nebius UIUX & Implementation Guide 1s-6lR6oq7gw-c2HUWMP7kNxcxM7V50g4C8qlNwmILg0

NVIDIA·마이크로소프트·메타·에퀴닉스·블룸에너지는 다른 사슬이 이미 전역에 갖고 있다.
그 다섯은 ENTITIES 에 다시 넣지 않고 관계에서 id 만 참조한다 — 다시 넣으면 merge() 가
저쪽 레코드를 얇은 버전으로 덮어쓴다.

Drive 는 매출 갈래를 상자가 아니라 관계 속성으로 두라고 적는다. 이 저장소도 같은 자리에
닿는다 — 여기서는 매출원 상자로 세우고 vc_norm 이 분류로 접는다(프레임워크 §13).

익명 고객 C·D·E 는 공시가 비중만 밝힌 자리다. 01 §4 가 실명 매핑을 명시적으로 거부했으니
가설표를 만들지 않는다. 04 관측 가운데 이을 관계가 없는 전사 절대값(총매출·RPO·조달)은
관측이 아니라 주장으로 옮긴다 — 태양유전·대덕전자 사슬이 세운 관례다.
"""
import io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'valuechain')
CHAIN = os.path.join(DATA, 'chains', 'nebius')
NE = 'nebius'

# ── 출처 (03 S001~S026) ────────────────────────────────────────────
SOURCES = [
 ('ne_20f_2025', 'SEC / Nebius Group', 'Nebius Group N.V. 2025 Form 20-F',
  'primary_official', '2026-04',
  'https://www.sec.gov/Archives/edgar/data/1513845/000110465926052948/nbis-20251231x20f.htm',
  '사업 구조·공급사 의존·고객 집중도의 원천. 03 의 S001'),
 ('ne_6k_q2_ex991', 'SEC / Nebius Group', 'Q2 2026 Form 6-K Exhibit 99.1',
  'primary_official', '2026-08-12',
  'https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d1.htm',
  '2026 2분기 매출과 부문 매출. 03 의 S002'),
 ('ne_6k_q2_ex992', 'SEC / Nebius Group', 'Q2 2026 Form 6-K Exhibit 99.2',
  'primary_official', '2026-08-12',
  'https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d2.htm',
  '고객 집중도 C·D·E, 잔여 이행 의무, 공급사 수. 03 의 S003'),
 ('ne_microsoft', 'Nebius', 'Nebius announces multi-billion dollar agreement with Microsoft '
  'for AI infrastructure', 'primary_company', '2025-09-08',
  'https://nebius.com/newsroom/nebius-announces-multi-billion-dollar-agreement-with-microsoft-'
  'for-ai-infrastructure', '뉴저지 바인랜드 전용 GPU 인프라 5년 계약. 03 의 S004'),
 ('ne_meta', 'Nebius', 'Nebius signs new AI infrastructure agreement with Meta',
  'primary_company', '2026-03-16',
  'https://nebius.com/newsroom/nebius-signs-new-ai-infrastructure-agreement-with-meta',
  '5년 120억 달러와 잔여 용량 최대 150억 달러 구매 약정. 03 의 S005'),
 ('ne_nvidia', 'Nebius / NVIDIA', 'NVIDIA and Nebius partner to scale full-stack AI cloud',
  'primary_company', '2026-03-11',
  'https://nebius.com/newsroom/nvidia-and-nebius-partner-to-scale-full-stack-ai-cloud',
  '20억 달러 투자와 2030년 말까지 5GW 넘는 시스템 목표. 03 의 S006'),
 ('ne_bloom', 'Nebius / Bloom Energy',
  'Nebius and Bloom Energy partner to power AI infrastructure build-out',
  'primary_company', '2026-05-20',
  'https://nebius.com/newsroom/nebius-and-bloom-energy-partner-to-power-ai-infrastructure-'
  'build-out', '1차 프로젝트 328MW 계량기 뒤 전력. 03 의 S007'),
 ('ne_vineland', 'Nebius', 'Vineland, New Jersey AI infrastructure site', 'primary_company',
  '2026', 'https://nebius.com/vinelandnj',
  '데이터원이 소유·운영하고 네비우스가 임차한다. 시공은 노스이스트 프리캐스트. 03 의 S008'),
 ('ne_paris', 'Nebius', 'Nebius launches GPU cluster in Paris, France', 'primary_company',
  '2024', 'https://nebius.com/blog/posts/nebius-launches-gpu-cluster-in-paris-france',
  '파리 생드니 에퀴닉스 PA10 배치. 03 의 S009'),
 ('ne_weka', 'Nebius', 'WEKA partner integration', 'primary_company', '2025',
  'https://nebius.com/partner-catalog/weka', 'NeuralMesh 를 네비우스 하드웨어에 얹는다. 03 의 S010'),
 ('ne_vast', 'Nebius', 'VAST Data partner integration', 'primary_company', '2025',
  'https://nebius.com/partner-catalog/vast', 'VAST Data Platform 통합. 03 의 S011'),
 ('ne_partnership_model', 'Nebius', 'Nebius introduces business model to scale AI cloud '
  'globally through infrastructure partnerships', 'primary_company', '2026-07-15',
  'https://nebius.com/newsroom/nebius-introduces-business-model-to-scale-ai-cloud-globally-'
  'through-infrastructure-partnerships',
  '파트너가 인프라와 하드웨어를 사고 소유하는 자산 경량 모델. 03 의 S012'),
 ('ne_palantir', 'Nebius / Palantir',
  'Palantir and Nebius partner to deliver a complete sovereign AI stack',
  'primary_company', '2026-09-08',
  'https://nebius.com/newsroom/palantir-and-nebius-partner-to-deliver-a-complete-sovereign-'
  'ai-stack-to-palantir-customers', '주권 AI 우선 파트너. 03 의 S013'),
 ('ne_q2_results', 'Nebius', 'Nebius reports second quarter 2026 financial results',
  'primary_company', '2026-08-12',
  'https://nebius.com/newsroom/nebius-reports-second-quarter-2026-financial-results',
  '2026 2분기 실적 발표. 03 의 S014'),
 ('ne_finland', 'Nebius', 'Nebius to construct 310 MW AI factory in Finland',
  'primary_company', '2026-03-31',
  'https://nebius.com/newsroom/nebius-to-construct-310-mw-ai-factory-in-finland',
  '라펜란타 최대 310MW, 첫 용량은 2027년. 만찰라 75MW 확장 완료도 같은 발표. 03 의 S015'),
 ('ne_missouri', 'Nebius', 'Nebius secures approval for its first gigawatt-scale AI factory',
  'primary_company', '2026-03-03',
  'https://nebius.com/newsroom/nebius-secures-approval-for-its-first-gigawatt-scale-ai-factory',
  '미주리 인디펜던스 최대 1.2GW 잠재 용량. 03 의 S016'),
 ('ne_revolut', 'Nebius', 'Revolut on the Inference Frontier', 'primary_company', '2026',
  'https://nebius.com/customer-stories/revolut', 'H100 200기 넘는 사용. 03 의 S017'),
 ('ne_recraft', 'Nebius', "Training a 20B foundational model: Recraft's journey",
  'primary_company', '2026', 'https://nebius.com/customer-stories/recraft',
  '200억 변수 모델 학습. 03 의 S018'),
 ('ne_sword', 'Nebius', 'Building Dawn: AI-powered mental health wellbeing support',
  'primary_company', '2026', 'https://nebius.com/customer-stories/swordhealth',
  '블랙웰 전용 엔드포인트와 토큰 팩토리. 03 의 S019'),
 ('ne_prime_intellect', 'Nebius',
  'Prime Intellect: Distributed training and RL with NVIDIA GB200 NVL72', 'primary_company',
  '2026', 'https://nebius.com/customer-stories/prime-intellect',
  '분산 학습과 강화학습. 03 의 S020'),
 ('ne_lynx', 'Nebius', 'Lynx Analytics: Scaling Graph AI to solve complex business problems',
  'primary_company', '2026', 'https://nebius.com/customer-stories/lynx-analytics',
  '그래프 AI 작업. 03 의 S021'),
 ('ne_roboforce', 'Nebius', 'Building Robo-Labor: How RoboForce is turning Physical AI '
  'into work', 'primary_company', '2026', 'https://nebius.com/customer-stories/roboforce',
  '물리 AI 학습·평가. 03 의 S022'),
 ('ne_prima_mente', 'Nebius', "Scaling Pleiades: Uncovering the brain's biology with "
  'Prima Mente', 'primary_company', '2026', 'https://nebius.com/customer-stories/prima-mente',
  'H200 32기 예약 클러스터. 03 의 S023'),
 ('ne_uk', 'Nebius', 'Nebius AI Cloud arrives in UK with advanced NVIDIA AI infrastructure '
  'deployment', 'primary_company', '2025-11-06',
  'https://nebius.com/newsroom/nebius-ai-cloud-arrives-in-uk-with-one-of-the-country-s-first-'
  'advanced-nvidia-ai-infrastructure-deployments',
  '영국 첫 배치 파트너로 베이스캠프 리서치·프리마 멘테. 03 의 S024'),
 ('ne_debt_775', 'Nebius', 'Nebius raises $775 million in first secured debt financing',
  'primary_company', '2026-07-17',
  'https://nebius.com/newsroom/nebius-raises-775-million-in-first-secured-debt-financing-to-'
  'accelerate-global-buildout', 'GPU 를 담보로 잡은 선순위 담보부 7억 7,500만 달러. 03 의 S025'),
 ('ne_convertible', 'Nebius Group',
  'Nebius Group closes $5.75B convertible senior notes offering', 'primary_company',
  '2026-08-24',
  'https://nebius.com/newsroom/nebius-group-announces-closing-of-private-offering-of-'
  'convertible-senior-notes-with-aggregate-gross-proceeds-of-approximately-5-75-billion',
  '전환사채 두 갈래 합계 57억 5,000만 달러. 03 의 S026'),
]

REGION = {'네덜란드': 'Europe', '미국': 'North America', '영국': 'Europe',
          '핀란드': 'Europe', '프랑스': 'Europe', '글로벌': 'Global'}

# ── 엔티티 (04 E001~E029 중 이 사슬이 새로 세우는 것) ───────────────
ENTITIES = [
 ('nebius', 'Nebius Group N.V.', '네비우스', 'company', '네덜란드', ['AI cloud'],
  'AI 클라우드 운영사이자 그룹 모법인. 매출의 거의 전부가 AI 클라우드 부문에서 난다'),
 ('nebius-inc', 'Nebius, Inc.', '네비우스 미국법인', 'company', '미국', ['AI cloud'],
  '미국 운영 법인. 마이크로소프트 계약의 당사자이고 바인랜드 부지의 임차인이다'),
 ('palantir', 'Palantir Technologies Inc.', '팔란티어', 'company', '미국',
  ['Channel partner'],
  '주권 AI 우선 파트너. 제 고객 울타리 안에서 네비우스 연산·추론을 쓰게 한다'),
 ('dataone', 'DataOne', '데이터원', 'company', '미국', ['Data center'],
  '바인랜드 맞춤 시설의 소유·운영자. 공시된 법인명은 없다'),
 ('weka', 'WEKA', 'WEKA', 'company', '미국', ['Storage software'],
  'NeuralMesh 스토리지 소프트웨어를 네비우스 하드웨어에 얹는다'),
 ('vast-data', 'VAST Data, Inc.', 'VAST 데이터', 'company', '미국', ['Storage software'],
  'VAST Data Platform 을 스토리지 층에 통합한다'),
 ('northeast-precast', 'Northeast Precast', '노스이스트 프리캐스트', 'company', '미국',
  ['Construction'], '바인랜드 부지 시공을 이끈다'),
 ('revolut', 'Revolut Ltd.', '레볼루트', 'end_user', '영국', ['AI cloud user'],
  'AI 클라우드와 토큰 팩토리 이용사. H100 200기 넘게 쓴다'),
 ('recraft', 'Recraft', '리크래프트', 'end_user', None, ['AI cloud user'],
  '200억 변수 기반 모델을 네비우스에서 학습했다'),
 ('sword-health', 'Sword Health', '소드 헬스', 'end_user', None, ['AI cloud user'],
  '블랙웰 전용 엔드포인트와 토큰 팩토리를 쓴다'),
 ('prime-intellect', 'Prime Intellect', '프라임 인텔렉트', 'end_user', None,
  ['AI cloud user'], '분산 학습과 강화학습에 쓰고 최신 시스템을 시험하는 자리로도 쓴다'),
 ('lynx-analytics', 'Lynx Analytics', '링크스 애널리틱스', 'end_user', None,
  ['AI cloud user'], '그래프 AI 작업을 돌린다'),
 ('roboforce', 'RoboForce', '로보포스', 'end_user', None, ['AI cloud user'],
  '물리 AI 학습과 평가에 쓴다'),
 ('basecamp-research', 'Basecamp Research', '베이스캠프 리서치', 'end_user', '영국',
  ['AI cloud user'], '영국 첫 배치의 파트너로 이름이 들어갔다'),
 ('prima-mente', 'Prima Mente', '프리마 멘테', 'end_user', '영국', ['AI cloud user'],
  'H200 32기 예약 클러스터로 대규모 사전학습을 돌린다'),
 ('ne-cust-c', 'Anonymous Customer C', '익명 고객 C', 'company', None, ['Customer'],
  '공시가 비중만 밝힌 고객. 실명은 비공개다'),
 ('ne-cust-d', 'Anonymous Customer D', '익명 고객 D', 'company', None, ['Customer'],
  '공시가 비중만 밝힌 고객. 실명은 비공개다'),
 ('ne-cust-e', 'Anonymous Customer E', '익명 고객 E', 'company', None, ['Customer'],
  '공시가 비중만 밝힌 고객. 실명은 비공개다'),
 # 부지 — 실제 자산이라 상자로 남고, 식구를 두르는 테두리는 projects.json 이 맡는다
 ('ne-mantsala', 'Mäntsälä AI data center', '만찰라 데이터센터', 'project_spv', '핀란드',
  ['Project'], '네비우스가 소유한 핵심 데이터센터. 2026년 3월에 75MW 로 확장을 마쳤다'),
 ('ne-vineland', 'Vineland AI infrastructure site', '바인랜드 부지', 'project_spv', '미국',
  ['Project'], '데이터원이 소유·운영하고 네비우스가 임차한다. 마이크로소프트 용량이 앉는 자리'),
 ('ne-pa10', 'Equinix PA10', '에퀴닉스 PA10', 'project_spv', '프랑스', ['Project'],
  '파리 생드니 코로케이션 부지'),
 ('ne-lappeenranta', 'Lappeenranta AI factory', '라펜란타 AI 팩토리', 'project_spv', '핀란드',
  ['Project'], '최대 310MW. 첫 용량은 2027년으로 예고됐다'),
 ('ne-independence', 'Independence AI factory', '인디펜던스 AI 팩토리', 'project_spv', '미국',
  ['Project'], '미주리. 잠재 용량 최대 1.2GW'),
 # 공급원 상자 — vc_norm 이 분류로 접는다
 ('ne-gpu-systems', 'NVIDIA GPU systems', 'GPU 시스템', 'component', None, ['Compute'],
  'AI 클라우드의 연산을 이루는 가속기 시스템'),
 ('ne-ai-network', 'AI networking platform', 'AI 네트워크', 'component', None, ['Network'],
  'InfiniBand·Spectrum-X 계열 네트워크 묶음'),
 ('ne-storage-sw', 'Storage software layer', '스토리지 소프트웨어', 'component', None,
  ['Storage'], '하드웨어 위에 얹는 스토리지 계층'),
 ('ne-site-power', 'Behind-the-meter site power', '계량기 뒤 부지 전력', 'subsystem', None,
  ['Site electrical BoP'], '전력망 앞이 아니라 부지 안에서 만드는 전기'),
 # 매출원 상자
 ('ne-rev-dedicated', 'Dedicated capacity revenue', '전용 용량 매출', 'revenue_type', None,
  ['Revenue type'], '하이퍼스케일러에 전용 용량을 대는 장기 계약'),
 ('ne-rev-ai-cloud', 'AI cloud revenue', 'AI 클라우드 매출', 'revenue_type', None,
  ['Revenue type'], '공개 AI 클라우드 이용'),
 ('ne-rev-token-factory', 'Token Factory revenue', '토큰 팩토리 매출', 'revenue_type', None,
  ['Revenue type'], '추론을 토큰 단위로 파는 자리'),
 ('ne-rev-managed-inference', 'Managed inference revenue', '관리형 추론 매출', 'revenue_type',
  None, ['Revenue type'], '파트너 울타리 안에서 쓰는 추론'),
 ('ne-rev-reserved', 'Reserved capacity revenue', '예약 용량 매출', 'revenue_type', None,
  ['Revenue type'], '기간을 잡아 두는 예약형 클러스터'),
 ('ne-rev-unallocated', 'Unallocated revenue', '배분 미상', 'revenue_type', None,
  ['Revenue type'], '공시가 고객별 배분을 밝히지 않은 몫'),
]

# ── 관계 ───────────────────────────────────────────────────────────
# (id, from, to, type, lane, subsystem, component, from_role, to_role,
#  valid_from, valid_to, status, evidence, src_tier, tgt_tier, sources, notes)
R = [
 # 업스트림 — 연산·네트워크·스토리지·전력
 ('nv-gpu', 'nvidia', 'ne-gpu-systems', 'SUPPLIES', 'MANUFACTURING_BOM', 'Compute',
  'GPU 시스템', '공급사', '연산', '2024-01-01', None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['ne_20f_2025', 'ne_nvidia'],
  '공시가 집중된 공급사 셋을 밝히지만 어느 자리가 엔비디아인지는 적지 않는다'),
 ('gpu-ne', 'ne-gpu-systems', NE, 'INPUT_TO', 'MANUFACTURING_BOM', 'Compute', 'GPU 시스템',
  '연산', 'AI 클라우드', None, None, 'ACTIVE', 'CONFIRMED', 'COMPONENT_SUPPLIER', None,
  ['ne_20f_2025'], None),
 ('nv-net', 'nvidia', 'ne-ai-network', 'SUPPLIES', 'MANUFACTURING_BOM', 'Network',
  'AI 네트워크', '공급사', '네트워크', '2024-01-01', None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['ne_nvidia'], None),
 ('net-ne', 'ne-ai-network', NE, 'INPUT_TO', 'MANUFACTURING_BOM', 'Network', 'AI 네트워크',
  '네트워크', 'AI 클라우드', None, None, 'ACTIVE', 'CONFIRMED', 'COMPONENT_SUPPLIER', None,
  ['ne_nvidia'], None),
 ('weka-sw', 'weka', 'ne-storage-sw', 'SUBSYSTEM_SUPPLY', 'MANUFACTURING_BOM', 'Storage',
  'NeuralMesh', '기술 파트너', '스토리지', '2025-01-01', None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['ne_weka'], '쓰는 돈이나 용량의 몫은 공개되지 않았다'),
 ('vast-sw', 'vast-data', 'ne-storage-sw', 'SUBSYSTEM_SUPPLY', 'MANUFACTURING_BOM', 'Storage',
  'VAST Data Platform', '기술 파트너', '스토리지', '2025-01-01', None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['ne_vast'], None),
 ('sw-ne', 'ne-storage-sw', NE, 'INPUT_TO', 'MANUFACTURING_BOM', 'Storage',
  '스토리지 소프트웨어', '스토리지', 'AI 클라우드', None, None, 'ACTIVE', 'CONFIRMED',
  'COMPONENT_SUPPLIER', None, ['ne_weka', 'ne_vast'], None),
 ('bloom-power', 'bloom-energy', 'ne-site-power', 'ELECTRICAL_BOP_SUPPLY',
  'MANUFACTURING_BOM', 'Site electrical BoP', '연료전지 전력', '전력 공급사', '부지 전력',
  '2026-05-20', None, 'ACTIVE', 'CONFIRMED', 'SUBSYSTEM_MODULE', None, ['ne_bloom'],
  '1차 프로젝트가 328MW 다. 그 용량을 바인랜드 것으로 단정하지 않는다'),
 ('power-ne', 'ne-site-power', NE, 'INPUT_TO', 'MANUFACTURING_BOM', 'Site electrical BoP',
  '부지 전력', '부지 전력', 'AI 클라우드', None, None, 'ACTIVE', 'CONFIRMED',
  'SUBSYSTEM_MODULE', None, ['ne_bloom'], None),
 # 기업 구조와 금융
 ('ne-inc-sub', 'nebius-inc', NE, 'SUBSIDIARY_OF', 'CORPORATE', 'Corporate', '미국 운영 법인',
  '자회사', '모법인', None, None, 'ACTIVE', 'CONFIRMED', None, None, ['ne_microsoft'], None),
 ('nv-partner', 'nvidia', NE, 'STRATEGIC_PARTNERSHIP', 'CORPORATE', 'Corporate',
  'AI 팩토리 설계·소프트웨어 협업', '전략 파트너', 'AI 클라우드', '2026-03-11', None,
  'ACTIVE', 'CONFIRMED', None, None, ['ne_nvidia'],
  '2030년 말까지 5GW 넘는 엔비디아 시스템을 세우는 목표를 함께 적었다'),
 ('nv-invest', 'nvidia', NE, 'INVESTS_IN', 'CORPORATE', 'Corporate', '지분·선납 워런트',
  '투자자', '발행사', '2026-03-11', None, 'ACTIVE', 'CONFIRMED', None, None,
  ['ne_nvidia', 'ne_6k_q2_ex992'], '총액 20억 달러'),
 # 부지
 ('equinix-pa10', 'equinix', 'ne-pa10', 'HOLDS_PROJECT', 'DOWNSTREAM', 'Project',
  '코로케이션 시설', '시설 운영사', '부지', '2024-01-01', None, 'ACTIVE', 'CONFIRMED',
  None, 'PROJECT', ['ne_paris'], None),
 ('ne-pa10-deploy', NE, 'ne-pa10', 'DEPLOYS_AT', 'DOWNSTREAM', 'Project', 'GPU 클러스터',
  'AI 클라우드', '부지', '2024-01-01', None, 'ACTIVE', 'CONFIRMED', None, 'PROJECT',
  ['ne_paris'], None),
 ('dataone-vineland', 'dataone', 'ne-vineland', 'HOLDS_PROJECT', 'DOWNSTREAM', 'Project',
  '맞춤 시설', '시설 소유·운영', '부지', '2026-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'PROJECT', ['ne_vineland'], None),
 ('ne-inc-vineland', 'nebius-inc', 'ne-vineland', 'DEPLOYS_AT', 'DOWNSTREAM', 'Project',
  '전용 GPU 인프라', '미국 법인', '부지', '2025-09-08', None, 'ACTIVE', 'CONFIRMED', None,
  'PROJECT', ['ne_microsoft', 'ne_vineland'], None),
 ('precast-vineland', 'northeast-precast', 'ne-vineland', 'PROJECT_SUPPLY', 'DOWNSTREAM',
  'Project', '부지 시공', '시공사', '부지', '2026-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'PROJECT', ['ne_vineland'], None),
 ('ne-mantsala-deploy', NE, 'ne-mantsala', 'DEPLOYS_AT', 'DOWNSTREAM', 'Project',
  '자체 데이터센터', 'AI 클라우드', '부지', None, None, 'ACTIVE', 'CONFIRMED', None,
  'PROJECT', ['ne_finland', 'ne_20f_2025'], None),
 ('ne-lappeenranta-deploy', NE, 'ne-lappeenranta', 'DEPLOYS_AT', 'DOWNSTREAM', 'Project',
  'AI 팩토리', 'AI 클라우드', '부지', '2027-01-01', None, 'PLANNED', 'CONFIRMED', None,
  'PROJECT', ['ne_finland'], '첫 용량이 2027년이라 계획이다'),
 ('ne-independence-deploy', NE, 'ne-independence', 'DEPLOYS_AT', 'DOWNSTREAM', 'Project',
  'AI 팩토리', 'AI 클라우드', '부지', '2026-03-03', None, 'PLANNED', 'CONFIRMED', None,
  'PROJECT', ['ne_missouri'], '승인까지 났고 용량은 잠재치다'),
 # 매출원
 ('ne-rev-dedicated-edge', NE, 'ne-rev-dedicated', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '전용 용량', 'AI 클라우드', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['ne_microsoft', 'ne_meta'], None),
 ('ne-rev-ai-cloud-edge', NE, 'ne-rev-ai-cloud', 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type',
  'AI 클라우드', 'AI 클라우드', '매출원', None, None, 'ACTIVE', 'CONFIRMED', None,
  'REVENUE_TYPE', ['ne_6k_q2_ex991'], None),
 ('ne-rev-token-edge', NE, 'ne-rev-token-factory', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '토큰 팩토리', 'AI 클라우드', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['ne_revolut', 'ne_sword'], None),
 ('ne-rev-inference-edge', NE, 'ne-rev-managed-inference', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '관리형 추론', 'AI 클라우드', '매출원', None, None, 'ACTIVE', 'CONFIRMED',
  None, 'REVENUE_TYPE', ['ne_palantir'], None),
 ('ne-rev-reserved-edge', NE, 'ne-rev-reserved', 'REVENUE_FROM', 'DOWNSTREAM', 'Revenue type',
  '예약 용량', 'AI 클라우드', '매출원', None, None, 'ACTIVE', 'CONFIRMED', None,
  'REVENUE_TYPE', ['ne_prima_mente'], None),
 ('ne-rev-unalloc-edge', NE, 'ne-rev-unallocated', 'REVENUE_FROM', 'DOWNSTREAM',
  'Revenue type', '고객 배분이 공개되지 않은 몫', 'AI 클라우드', '매출원', None, None,
  'ACTIVE', 'UNDISCLOSED', None, 'REVENUE_TYPE', ['ne_6k_q2_ex992'],
  '공시가 상위 고객을 알파벳으로만 밝힌다'),
 # 전용 용량 고객
 ('ded-microsoft', 'ne-rev-dedicated', 'microsoft', 'SELLS_TO', 'DOWNSTREAM', 'Data center',
  '전용 GPU 인프라 용량', '매출원', '고객', '2025-09-08', '2031-12-31', 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['ne_microsoft'],
  '계약 당사자는 미국 법인이다. 약 174억 달러, 선택 서비스까지 더하면 약 194억 달러'),
 ('ded-meta', 'ne-rev-dedicated', 'meta', 'SELLS_TO', 'DOWNSTREAM', 'Data center',
  '전용 AI 용량', '매출원', '고객', '2026-03-16', '2032-12-31', 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['ne_meta'],
  '5년 120억 달러. 인도는 2027년 초에 시작한다'),
 # AI 클라우드 고객
 ('cloud-revolut', 'ne-rev-ai-cloud', 'revolut', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'AI 클라우드', '매출원', '고객', '2026-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_revolut'], '쓰는 것은 확인되고 거래 규모는 비공개다'),
 ('cloud-recraft', 'ne-rev-ai-cloud', 'recraft', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'AI 클라우드', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_recraft'], None),
 ('cloud-sword', 'ne-rev-ai-cloud', 'sword-health', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'AI 클라우드', '매출원', '고객', '2025-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_sword'], None),
 ('cloud-prime', 'ne-rev-ai-cloud', 'prime-intellect', 'SELLS_TO', 'DOWNSTREAM',
  'Application', 'AI 클라우드', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_prime_intellect'], None),
 ('cloud-lynx', 'ne-rev-ai-cloud', 'lynx-analytics', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'AI 클라우드', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_lynx'], None),
 ('cloud-roboforce', 'ne-rev-ai-cloud', 'roboforce', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'AI 클라우드', '매출원', '고객', '2026-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_roboforce'], None),
 ('cloud-basecamp', 'ne-rev-ai-cloud', 'basecamp-research', 'SELLS_TO', 'DOWNSTREAM',
  'Application', '영국 AI 인프라', '매출원', '고객', '2025-11-06', None, 'ACTIVE',
  'CONFIRMED', None, 'CONTRACTUAL_CUSTOMER', ['ne_uk'], None),
 # 토큰 팩토리·예약 용량
 ('token-revolut', 'ne-rev-token-factory', 'revolut', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  '토큰 팩토리', '매출원', '고객', '2026-01-01', None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_revolut'], None),
 ('token-sword', 'ne-rev-token-factory', 'sword-health', 'SELLS_TO', 'DOWNSTREAM',
  'Application', '토큰 팩토리', '매출원', '고객', '2025-01-01', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['ne_sword'], None),
 ('reserved-prima', 'ne-rev-reserved', 'prima-mente', 'SELLS_TO', 'DOWNSTREAM', 'Application',
  'H200 32기 예약 클러스터', '매출원', '고객', '2026-01-01', None, 'ACTIVE', 'CONFIRMED',
  None, 'CONTRACTUAL_CUSTOMER', ['ne_prima_mente'], None),
 # 중개 — 팔란티어
 ('inference-palantir', 'ne-rev-managed-inference', 'palantir', 'SELLS_TO', 'DOWNSTREAM',
  'Channel', '주권 AI 스택 안의 연산·추론', '매출원', '중개', '2026-09-08', None, 'ACTIVE',
  'CONFIRMED', None, 'INTERMEDIARY', ['ne_palantir'],
  '제휴는 확인된다. 계약상 구매 주체라는 근거는 없어 직접 고객으로 적지 않는다'),
 # 익명 고객 — 공시가 비중만 밝힌 자리
 ('unalloc-cust-c', 'ne-rev-unallocated', 'ne-cust-c', 'SELLS_TO', 'DOWNSTREAM', 'Customer',
  '고객 집중도', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_6k_q2_ex992'], '실명을 마이크로소프트나 메타로 잇지 않는다'),
 ('unalloc-cust-d', 'ne-rev-unallocated', 'ne-cust-d', 'SELLS_TO', 'DOWNSTREAM', 'Customer',
  '고객 집중도', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_6k_q2_ex992'], None),
 ('unalloc-cust-e', 'ne-rev-unallocated', 'ne-cust-e', 'SELLS_TO', 'DOWNSTREAM', 'Customer',
  '고객 집중도', '매출원', '고객', None, None, 'ACTIVE', 'CONFIRMED', None,
  'CONTRACTUAL_CUSTOMER', ['ne_6k_q2_ex992'], None),
]

PCT, USDM, MW = 'percent', 'USD million', 'MW'
# (id, rel, metric, value, low, high, unit, period, p_start, p_end, as_of,
#  denominator, status, evidence_level, confidence, note, sources)
O = [
 ('o-ne-cust-c-q2', 'unalloc-cust-c', 'customer_revenue_share', 24, None, None, PCT,
  'Q2 2026', '2026-04-01', '2026-06-30', '2026-06-30', '네비우스 총매출', 'CURRENT',
  'CONFIRMED', 1.0, '실명은 비공개다', ['ne_6k_q2_ex992']),
 ('o-ne-cust-c-h1', 'unalloc-cust-c', 'customer_revenue_share', 26, None, None, PCT,
  'H1 2026', '2026-01-01', '2026-06-30', '2026-06-30', '네비우스 총매출', 'CURRENT',
  'CONFIRMED', 1.0, None, ['ne_6k_q2_ex992']),
 ('o-ne-cust-d-q2', 'unalloc-cust-d', 'customer_revenue_share', 21, None, None, PCT,
  'Q2 2026', '2026-04-01', '2026-06-30', '2026-06-30', '네비우스 총매출', 'CURRENT',
  'CONFIRMED', 1.0, None, ['ne_6k_q2_ex992']),
 ('o-ne-cust-d-h1', 'unalloc-cust-d', 'customer_revenue_share', 21, None, None, PCT,
  'H1 2026', '2026-01-01', '2026-06-30', '2026-06-30', '네비우스 총매출', 'CURRENT',
  'CONFIRMED', 1.0, None, ['ne_6k_q2_ex992']),
 ('o-ne-cust-e-q2', 'unalloc-cust-e', 'customer_revenue_share', 14, None, None, PCT,
  'Q2 2026', '2026-04-01', '2026-06-30', '2026-06-30', '네비우스 총매출', 'CURRENT',
  'CONFIRMED', 1.0, None, ['ne_6k_q2_ex992']),
 ('o-ne-bloom-328mw', 'bloom-power', 'first_project_capacity', 328, None, None, MW,
  '2026', '2026-01-01', '2026-12-31', '2026-05-20', '블룸 1차 프로젝트 설치 용량', 'CURRENT',
  'CONFIRMED', 1.0, '부지를 바인랜드로 특정하는 문장은 없다', ['ne_bloom']),
 ('o-ne-mantsala-75mw', 'ne-mantsala-deploy', 'site_capacity', 75, None, None, MW,
  '2026', '2026-01-01', '2026-12-31', '2026-03-31', '만찰라 데이터센터 용량', 'CURRENT',
  'CONFIRMED', 1.0, '확장을 마쳤다고 회사가 밝혔다', ['ne_finland']),
 ('o-ne-lappeenranta-310mw', 'ne-lappeenranta-deploy', 'site_capacity', 310, None, None, MW,
  '2026 발표', '2026-01-01', '2027-12-31', '2026-03-31', '라펜란타 AI 팩토리 용량',
  'NOT_YET_ACTIVE',
  'CONFIRMED', 1.0, '첫 용량은 2027년', ['ne_finland']),
 ('o-ne-independence-1200mw', 'ne-independence-deploy', 'site_capacity', 1200, None, None, MW,
  '2026 발표', '2026-01-01', None, '2026-03-03', '인디펜던스 AI 팩토리 잠재 용량',
  'NOT_YET_ACTIVE',
  'CONFIRMED', 1.0, '잠재 용량이라 설치 용량으로 읽지 않는다', ['ne_missouri']),
 ('o-ne-microsoft-value', 'ded-microsoft', 'contract_value', 17400, None, None, USDM,
  '2025-2031', '2025-09-08', '2031-12-31', '2025-09-08', '단일 계약 금액', 'CURRENT',
  'CONFIRMED', 1.0, '선택 서비스까지 더하면 약 19,400', ['ne_microsoft']),
 ('o-ne-meta-value', 'ded-meta', 'contract_value', 12000, None, None, USDM,
  '2026-2032', '2026-03-16', '2032-12-31', '2026-03-16', '단일 계약 금액', 'CURRENT',
  'CONFIRMED', 1.0, '잔여 용량 구매 약정 최대 15,000 은 따로다', ['ne_meta']),
 ('o-ne-nvidia-invest', 'nv-invest', 'investment_value', 2000, None, None, USDM,
  '2026', '2026-03-11', '2026-03-11', '2026-03-11', '투자 총액', 'CURRENT', 'CONFIRMED',
  1.0, None, ['ne_nvidia']),
]

CLAIMS = [
 ('clm-ne-q2-revenue', '네비우스의 2026년 2분기 총매출은 5억 8,230만 달러다.', NE, None,
  'Q2 2026', 'CONFIRMED', 1.0, ['ne_6k_q2_ex991'], None),
 ('clm-ne-q2-cloud', '그 가운데 AI 클라우드 부문 매출이 5억 7,490만 달러다.', NE, None,
  'Q2 2026', 'CONFIRMED', 1.0, ['ne_6k_q2_ex991'], None),
 ('clm-ne-cloud-share', 'AI 클라우드가 총매출의 98.7%를 차지한다.', NE, None, 'Q2 2026',
  'ESTIMATED', 0.9, ['ne_6k_q2_ex991'], '574.9 를 582.3 으로 나눈 값이다'),
 ('clm-ne-h1-revenue', '2026년 상반기 총매출은 9억 8,130만 달러, AI 클라우드는 '
  '9억 6,460만 달러다.', NE, None, 'H1 2026', 'CONFIRMED', 1.0, ['ne_6k_q2_ex991'], None),
 ('clm-ne-rpo', '2026년 6월 말 잔여 이행 의무가 374억 9,060만 달러이고 전부 AI 클라우드 '
  '부문에서 나온다.', NE, None, '2026-06-30', 'CONFIRMED', 1.0, ['ne_6k_q2_ex992'],
  '공시가 고객별로 나누지 않았으니 실명에 배분하지 않는다'),
 ('clm-ne-supplier-3', '설비투자 익스포저가 공급사 세 곳에 몰려 있다.', NE, None,
  '2026-06-30', 'CONFIRMED', 1.0, ['ne_6k_q2_ex992'],
  '실명과 각 몫은 비공개다. 엔비디아를 그 셋 중 하나로 지목할 근거는 없다'),
 ('clm-ne-nvidia', '엔비디아는 GPU·네트워크 공급사이자 전략 파트너이며 투자자다.',
  'nvidia', NE, '2026-03~', 'CONFIRMED', 1.0, ['ne_nvidia', 'ne_20f_2025'],
  '2030년 말까지 5GW 넘는 시스템 목표와 20억 달러 투자가 같은 발표에 있다'),
 ('clm-ne-microsoft', '마이크로소프트와 맺은 전용 GPU 인프라 계약은 약 174억 달러 규모의 '
  '5년짜리다.', 'microsoft', 'nebius-inc', '2025-09~2031', 'CONFIRMED', 1.0,
  ['ne_microsoft'], '선택 서비스까지 더하면 약 194억 달러'),
 ('clm-ne-meta', '메타와 맺은 전용 용량 계약은 5년 120억 달러이고 인도는 2027년 초에 '
  '시작한다.', 'meta', NE, '2026-03~2032', 'CONFIRMED', 1.0, ['ne_meta'], None),
 ('clm-ne-meta-commit', '메타는 일부 신규 클러스터의 잔여 용량을 최대 150억 달러까지 '
  '사기로 약정했다.', 'meta', NE, '2026-03~2032', 'CONFIRMED', 1.0, ['ne_meta'],
  '약정이지 인식될 매출이 아니다'),
 ('clm-ne-bloom', '블룸에너지와의 전력 제휴에서 1차 프로젝트 용량이 328MW다.',
  'bloom-energy', NE, '2026-05~', 'CONFIRMED', 1.0, ['ne_bloom'],
  '이 용량을 바인랜드 부지로 잇는 문장은 원문에 없다'),
 ('clm-ne-vineland', '바인랜드 시설은 데이터원이 소유·운영하고 네비우스가 임차한다.',
  'dataone', 'nebius-inc', '2026~', 'CONFIRMED', 1.0, ['ne_vineland'],
  '시공은 노스이스트 프리캐스트가 이끈다'),
 ('clm-ne-paris', '파리 배치는 에퀴닉스 PA10 코로케이션에 있다.', 'equinix', NE,
  '2024~', 'CONFIRMED', 1.0, ['ne_paris'], '생드니'),
 ('clm-ne-storage', 'WEKA 와 VAST 데이터의 스토리지 소프트웨어가 네비우스 하드웨어에 '
  '얹힌다.', 'weka', NE, '2025~', 'CONFIRMED', 1.0, ['ne_weka', 'ne_vast'],
  '쓰는 돈과 용량의 몫은 비공개다'),
 ('clm-ne-asset-light', '파트너가 인프라와 하드웨어를 사고 소유하는 자산 경량 모델을 '
  '내놨다.', NE, None, '2026-07~', 'CONFIRMED', 1.0, ['ne_partnership_model'],
  '네비우스는 설계·공급망·플랫폼·영업을 댄다'),
 ('clm-ne-palantir', '팔란티어와 주권 AI 우선 파트너 관계를 맺었다.', 'palantir', NE,
  '2026-09~', 'CONFIRMED', 1.0, ['ne_palantir'],
  '계약 근거가 없으니 팔란티어를 직접 고객으로 적지 않는다'),
 ('clm-ne-palantir-indirect', '통합을 마친 팔란티어 상용 고객이 네비우스 연산·추론을 '
  '쓸 수 있다.', 'palantir', None, '2026-09~', 'CONFIRMED', 1.0, ['ne_palantir'],
  '개별 고객 실명은 비공개다. 자리표로 닫고 이름을 짓지 않는다'),
 ('clm-ne-lappeenranta', '라펜란타 AI 팩토리는 최대 310MW로 발표됐고 첫 용량은 '
  '2027년이다.', 'ne-lappeenranta', NE, '2026-03', 'CONFIRMED', 1.0, ['ne_finland'], None),
 ('clm-ne-independence', '미주리 인디펜던스 AI 팩토리의 잠재 용량은 최대 1.2GW다.',
  'ne-independence', NE, '2026-03', 'CONFIRMED', 1.0, ['ne_missouri'],
  '2026년 5월 12일에 착공했다'),
 ('clm-ne-mantsala', '만찰라 데이터센터는 2026년 3월 말 기준 75MW로 확장을 마쳤다.',
  'ne-mantsala', NE, '2026-03-31', 'CONFIRMED', 1.0, ['ne_finland', 'ne_20f_2025'], None),
 ('clm-ne-revolut', '레볼루트는 AI 클라우드와 토큰 팩토리를 쓰며 H100 을 200기 넘게 '
  '돌린다.', 'revolut', NE, '2026', 'CONFIRMED', 1.0, ['ne_revolut'],
  '사기 방지·고객 응대·모델 작업에 쓴다'),
 ('clm-ne-recraft', '리크래프트는 네비우스에서 200억 변수 기반 모델을 학습했다.',
  'recraft', NE, '2026', 'CONFIRMED', 1.0, ['ne_recraft'], None),
 ('clm-ne-sword', '소드 헬스는 블랙웰 전용 엔드포인트와 토큰 팩토리를 쓴다.',
  'sword-health', NE, '2026', 'CONFIRMED', 1.0, ['ne_sword'], None),
 ('clm-ne-prime', '프라임 인텔렉트는 최신 시스템을 시험하는 자리로도 네비우스를 쓴다.',
  'prime-intellect', NE, '2026', 'CONFIRMED', 1.0, ['ne_prime_intellect'], None),
 ('clm-ne-lynx', '링크스 애널리틱스는 그래프 AI 작업에 네비우스 인프라를 쓴다.',
  'lynx-analytics', NE, '2026', 'CONFIRMED', 1.0, ['ne_lynx'], None),
 ('clm-ne-roboforce', '로보포스는 물리 AI 학습과 평가에 AI 클라우드를 쓴다.',
  'roboforce', NE, '2026', 'CONFIRMED', 1.0, ['ne_roboforce'],
  '고객 사례는 준비 시간이 70% 줄었다고 적는다'),
 ('clm-ne-prima', '프리마 멘테는 H200 32기 예약 클러스터로 대규모 사전학습을 돌린다.',
  'prima-mente', NE, '2026', 'CONFIRMED', 1.0, ['ne_prima_mente'], None),
 ('clm-ne-basecamp', '베이스캠프 리서치는 영국 첫 배치의 이용사로 이름이 올랐다.',
  'basecamp-research', NE, '2025-11~', 'CONFIRMED', 1.0, ['ne_uk'], None),
 ('clm-ne-debt', 'GPU 를 담보로 잡은 선순위 담보부 차입 약 7억 7,500만 달러를 일으켰다.',
  NE, None, '2026-07', 'CONFIRMED', 1.0, ['ne_debt_775'],
  'SOFR 에 2.50%를 얹고 2030년 10월 31일에 만기가 온다'),
 ('clm-ne-convertible', '전환사채 두 갈래로 원금 합계 57억 5,000만 달러를 조달했다.',
  NE, None, '2026-08', 'CONFIRMED', 1.0, ['ne_convertible'],
  '2030년 만기 0.50% 34억 5,000만 달러와 2034년 만기 4.50% 23억 달러'),
 ('clm-ne-anon-nomap', '익명 고객 C·D·E 를 공개 실명 고객에 잇는 근거는 공시에 없다.',
  NE, None, '2026', 'CONFIRMED', 1.0, ['ne_6k_q2_ex992'],
  '01 조사도 매핑을 거부했다. 이 사슬에는 가설표가 없다'),
]

PROJECTS = [
 {'id': 'ne-proj-vineland', 'name': 'Vineland AI infrastructure site',
  'name_ko': '바인랜드 부지', 'site': 'ne-vineland', 'developer': 'dataone',
  'ultimate_end_user': 'microsoft',
  'members': ['ne-vineland', 'dataone', 'northeast-precast', 'nebius-inc'],
  'note': '블룸 1차 프로젝트가 328MW 지만 그 용량을 이 부지로 잇는 문장은 원문에 없다',
  'from_relationships': ['dataone-vineland', 'ne-inc-vineland', 'precast-vineland']},
 {'id': 'ne-proj-pa10', 'name': 'Paris AI cloud deployment', 'name_ko': '파리 배치',
  'site': 'ne-pa10', 'developer': 'equinix', 'members': ['ne-pa10', 'equinix'],
  'from_relationships': ['equinix-pa10', 'ne-pa10-deploy']},
 {'id': 'ne-proj-mantsala', 'name': 'Mäntsälä core data center', 'name_ko': '만찰라',
  'site': 'ne-mantsala', 'developer': NE, 'members': ['ne-mantsala'],
  'from_relationships': ['ne-mantsala-deploy']},
 {'id': 'ne-proj-lappeenranta', 'name': 'Lappeenranta AI factory', 'name_ko': '라펜란타',
  'site': 'ne-lappeenranta', 'developer': NE, 'members': ['ne-lappeenranta'],
  'from_relationships': ['ne-lappeenranta-deploy']},
 {'id': 'ne-proj-independence', 'name': 'Independence AI factory', 'name_ko': '인디펜던스',
  'site': 'ne-independence', 'developer': NE, 'members': ['ne-independence'],
  'from_relationships': ['ne-independence-deploy']},
]

CONTRACT_BY_ID = {
    # 고객 사례로 아는 이용사는 계약 근거까지 공개되지 않았다
    'cloud-revolut': 'UNVERIFIED', 'cloud-recraft': 'UNVERIFIED',
    'cloud-sword': 'UNVERIFIED', 'cloud-prime': 'UNVERIFIED',
    'cloud-lynx': 'UNVERIFIED', 'cloud-roboforce': 'UNVERIFIED',
    'cloud-basecamp': 'UNVERIFIED', 'token-revolut': 'UNVERIFIED',
    'token-sword': 'UNVERIFIED', 'reserved-prima': 'UNVERIFIED',
    'inference-palantir': 'UNVERIFIED',
}


def ent(t):
    return {'id': t[0], 'name': t[1], 'name_ko': t[2], 'entity_type': t[3],
            'legal_name': t[1], 'display_name': t[2] or t[1],
            'region': REGION.get(t[4]) if t[4] else None,
            'parent_entity_id': 'nebius' if t[0] == 'nebius-inc' else None,
            'primary_role': (t[5] or [None])[0], 'other_roles': (t[5] or [])[1:],
            'country': t[4], 'categories': t[5], 'desc': t[6],
            'anon': t[0].startswith('ne-cust-')}


def src(t):
    return {'id': t[0], 'publisher': t[1], 'title': t[2], 'source_type': t[3],
            'published_date': t[4], 'url': t[5], 'accessed_date': '2026-09-12', 'note': t[6]}


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
            'confidence': t[14], 'method_id': None, 'method_note': t[15],
            'source_ids': t[16],
            'denominator_scope': ('FOCAL_TOTAL_REVENUE'
                                  if t[2] == 'customer_revenue_share' else 'EDGE'),
            'source_date': SRC_DATE.get((t[16] or [None])[0]) or t[10]}


def claim(t):
    return {'id': t[0], 'statement': t[1], 'subject': t[2], 'object': t[3], 'period': t[4],
            'evidence_level': t[5], 'confidence': t[6], 'source_ids': t[7], 'note': t[8]}


def evidence():
    """관측과 관계마다 출처 연결을 근거 줄로 남긴다."""
    out, n = [], 0
    for t in O:
        for sid in t[16]:
            n += 1
            out.append({'id': 'ne-e%03d' % n, 'relationship_id': t[1], 'metric_id': t[0],
                        'source_id': sid,
                        'evidence_type': 'direct' if t[13] == 'CONFIRMED' else 'indirect',
                        'evidence': t[15] or '', 'hypothesis_id': None})
    for t in R:
        for sid in t[15]:
            n += 1
            out.append({'id': 'ne-e%03d' % n, 'relationship_id': t[0], 'metric_id': None,
                        'source_id': sid,
                        'evidence_type': 'direct' if t[12] == 'CONFIRMED' else 'indirect',
                        'evidence': t[16] or '', 'hypothesis_id': None})
    return out


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


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    ne_n = merge('entities.json', [ent(t) for t in ENTITIES])
    ns = merge('sources.json', [src(t) for t in SOURCES])
    dump(os.path.join(CHAIN, 'chain.json'),
         {'id': 'nebius', 'focal_entity': NE, 'label': '네비우스',
          'note': 'AI 클라우드 운영사 한 곳을 중심으로 세운 사슬'})
    dump(os.path.join(CHAIN, 'relationships.json'), [rel(t) for t in R])
    dump(os.path.join(CHAIN, 'observations.json'), [obs(t) for t in O])
    dump(os.path.join(CHAIN, 'claims.json'), [claim(t) for t in CLAIMS])
    dump(os.path.join(CHAIN, 'hypotheses.json'), [])
    dump(os.path.join(CHAIN, 'projects.json'), PROJECTS)
    dump(os.path.join(CHAIN, 'evidence.json'), evidence())
    print('전역 엔티티 %d · 출처 %d · 관계 %d · 관측 %d · 주장 %d'
          % (ne_n, ns, len(R), len(O), len(CLAIMS)))

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import vc_norm
    vc_norm.main()
