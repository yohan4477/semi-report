# -*- coding: utf-8 -*-
"""NVIDIA·AMD·TSMC·ASML 밸류체인 HTML 을 만든다.

값의 출처는 각 회사의 최신 SEC 공시 하나뿐이다.
  NVIDIA  FY2026 10-K (2026-01-25 종료)   accession 0001045810-26-000021
  AMD     FY2025 10-K (2025-12-27 종료)   accession 0000002488-26-000018
  TSMC    FY2025 20-F (2025-12-31 종료)   accession 0001628280-26-025362
  ASML    FY2025 20-F (2025-12-31 종료)   accession 0001628280-26-011378
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_valuechain import Plate, page, esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', '밸류체인 — NVIDIA·AMD·TSMC·ASML.html')

L6 = ['공급사', '회사', '사업부문', '채널', '고객', '최종 수요처']


# ══════════════════════════════════════════════════════════════════
def nvidia():
    p = Plate(
        'NVIDIA — 파운드리 둘과 메모리 셋에서 받아, 매출 2,159억 달러의 89.6%를 컴퓨트·네트워킹에서 낸다',
        '10-K는 공급사에만 실명을 적었다. 고객은 「직접고객 한 곳이 22%」처럼 익명으로만 나온다.',
        [162, 138, 150, 152, 156, 150], layers=L6,
        foot=[
            '① 「직접고객」은 최종 사용자가 아니라 유통 경로다. 10-K가 ODM·OEM·시스템 인테그레이터·디스트리뷰터를 이 말로 부른다.',
            '② 지역 매출은 청구지 기준이다. 대만 청구분 423억 달러(19.6%) 가운데 76%는 미국·유럽 최종고객 것이라고 10-K가 따로 적었다.',
            '③ 출처: NVIDIA FY2026 Form 10-K — Item 1 Business, Segment Information 주석(R18·R25·R82·R84·R85).',
        ])
    b = p.box
    b(0, 'nv_tsmc', 'TSMC', ['웨이퍼 파운드리', 'CoWoS 패키징 공정'])
    b(0, 'nv_ss', '삼성전자', ['웨이퍼 파운드리', '메모리'])
    b(0, 'nv_sk', 'SK하이닉스', ['메모리'])
    b(0, 'nv_mu', '마이크론', ['메모리'])
    b(0, 'nv_odm', '홍하이·위스트론·파브리넷', ['완제품 조립·시험·패키징 외주'])
    b(0, 'nv_sub', '기판·광부품 공급사', ['10-K에 이름이 없다'])

    b(1, 'nv', 'NVIDIA', ['FY2026 매출 2,159.38억 달러', '전년 1,304.97억에서 +65%'], kind='hero')

    b(2, 'nv_cn', 'Compute & Networking', ['1,934.79억 달러 · 89.6%', '가속 컴퓨팅·네트워킹·자동차'])
    b(2, 'nv_gx', 'Graphics', ['224.59억 달러 · 10.4%', 'GeForce · RTX'])

    b(3, 'nv_ch_dir', 'ODM·OEM·시스템 인테그레이터', ['10-K가 「직접고객」으로 부르는 경로', '경로별 비중은 공시 없음'])
    b(3, 'nv_ch_csp', 'CSP 직접 판매', ['CSP가 직접·간접 양쪽에 다 나온다'])
    b(3, 'nv_ch_aib', 'AIB·디스트리뷰터', ['그래픽카드 유통'])
    b(3, 'nv_ch_auto', '자동차 1차 협력사', ['자동차 매출 23.49억 달러'])

    b(4, 'nv_c1', '직접고객 갑 (익명)', ['총매출의 22%', '매출채권 잔액의 25%'])
    b(4, 'nv_c2', '직접고객 을 (익명)', ['총매출의 14%', '매출채권 잔액의 18%'])
    b(4, 'nv_c3', '직접고객 병 (익명)', ['매출채권 잔액의 13%', '총매출 비중은 10% 미만'])
    b(4, 'nv_c4', '간접고객군', ['CSP·네오클라우드·AI 모델 회사', '기업·공공기관'])

    b(5, 'nv_e1', '데이터센터', ['1,937.37억 달러', '컴퓨트 1,623.61 + 네트워킹 313.76'])
    b(5, 'nv_e2', '게이밍', ['160.42억 달러'])
    b(5, 'nv_e3', '프로 비주얼라이제이션', ['31.91억 달러'])
    b(5, 'nv_e4', '자동차·로보틱스', ['23.49억 달러'])

    for s in ['nv_tsmc', 'nv_ss', 'nv_sk', 'nv_mu', 'nv_odm']:
        p.edge(s, 'nv')
    p.edge('nv_sub', 'nv', dashed=True)
    p.edge('nv', 'nv_cn')
    p.edge('nv', 'nv_gx')
    p.edge('nv_cn', 'nv_ch_dir')
    p.edge('nv_cn', 'nv_ch_csp', dashed=True)
    p.edge('nv_cn', 'nv_ch_auto')
    p.edge('nv_gx', 'nv_ch_aib', dashed=True)
    p.edge('nv_ch_dir', 'nv_c1')
    p.edge('nv_ch_dir', 'nv_c2')
    p.edge('nv_ch_dir', 'nv_c3')
    p.edge('nv_ch_csp', 'nv_c4')
    p.edge('nv_c1', 'nv_e1', dashed=True)
    p.edge('nv_c2', 'nv_e1', dashed=True)
    p.edge('nv_c4', 'nv_e1')
    p.edge('nv_ch_aib', 'nv_e2', dashed=True)
    p.edge('nv_ch_auto', 'nv_e4')
    return p


# ══════════════════════════════════════════════════════════════════
def amd():
    p = Plate(
        'AMD — 7nm 이하를 TSMC에 전량 맡기고, 매출 346억 달러의 48%를 데이터센터에서 낸다',
        'FY2025·FY2024에는 매출 10%를 넘긴 고객이 하나도 없다. 랙 단위 설계는 사들이고 제조는 되팔았다.',
        [168, 140, 152, 150, 152, 146], layers=L6,
        foot=[
            '① GlobalFoundries 웨이퍼 공급계약은 연간 최소 물량과 2026년까지의 가격을 정해 뒀다. 최소 구매 금액은 10-K에 없다.',
            '② ZT Systems는 2025년 3월 현금 32억 달러와 주식 830만 주로 샀고, 그해 10월 제조 부문만 현금 24억 달러와 Sanmina 주식 120만 주로 넘겼다.',
            '③ 출처: AMD FY2025 Form 10-K — Item 1 Business, Item 1A, Note 4 Segment Reporting, Note 11, Note 12.',
        ])
    b = p.box
    b(0, 'am_tsmc', 'TSMC', ['7nm 이하 CPU·GPU 전량', 'FPGA 계열 일부'])
    b(0, 'am_gf', 'GlobalFoundries', ['12nm·14nm HPC 제품', '웨이퍼 공급계약으로 최소 물량 약정'])
    b(0, 'am_umc', 'UMC·삼성전자', ['프로그래머블 로직 IC'])
    b(0, 'am_atmp', '퉁푸 합작 2사·SPIL·KYEC', ['조립·시험·패키징'])
    b(0, 'am_mem', '메모리·기판·PCB·인터포저', ['「한정된 수의 공급사」로만 적혀 있다', '이름 없음'])
    b(0, 'am_sm', 'Sanmina', ['AI 랙 제조 우선 파트너', '2025년 10월 ZT 제조사업 인수'])

    b(1, 'am', 'AMD', ['FY2025 매출 346.39억 달러', '영업이익 36.94억 달러'], kind='hero')

    b(2, 'am_dc', 'Data Center', ['166.35억 달러 · 48.0%', '영업이익 36.03억 · 전년 +32%'])
    b(2, 'am_cg', 'Client and Gaming', ['145.50억 달러 · 42.0%', '클라이언트 106.40 + 게이밍 39.10'])
    b(2, 'am_em', 'Embedded', ['34.54억 달러 · 10.0%', '영업이익 12.43억 · 전년 -3%'])

    b(3, 'am_ch_hs', '하이퍼스케일러', ['직접·간접 양쪽으로 산다', '서버는 ODM이 만든다'])
    b(3, 'am_ch_oem', 'OEM·ODM·시스템 인테그레이터', ['서버·PC 완제품'])
    b(3, 'am_ch_dist', '공인 디스트리뷰터', ['재판매·재고 가격보호 조항'])
    b(3, 'am_ch_aib', 'AIB·게임 콘솔 제조사', ['Radeon 보드 · 콘솔 SoC'])
    b(3, 'am_ch_var', 'VAR·ISV', ['임베디드 Alveo 경로'])

    b(4, 'am_c0', '10% 넘는 고객 없음', ['FY2025·FY2024 모두', 'FY2023엔 한 곳이 18%'])
    b(4, 'am_c1', '매출채권 집중 고객 (익명)', ['2025년말 잔액의 11%'])
    b(4, 'am_c2', 'OpenAI', ['GPU 6기가와트 공급 계약', 'MI450 시리즈부터 배치'])

    b(5, 'am_e1', 'AI 학습·추론 데이터센터', ['EPYC 5세대 · Instinct MI350X'])
    b(5, 'am_e2', 'PC', ['Ryzen'])
    b(5, 'am_e3', '게임 콘솔', ['콘솔용 SoC'])
    b(5, 'am_e4', '산업·통신·자동차', ['임베디드 34.54억 달러'])

    for s in ['am_tsmc', 'am_gf', 'am_umc', 'am_atmp', 'am_sm']:
        p.edge(s, 'am')
    p.edge('am_mem', 'am', dashed=True)
    p.edge('am', 'am_dc')
    p.edge('am', 'am_cg')
    p.edge('am', 'am_em')
    p.edge('am_dc', 'am_ch_hs')
    p.edge('am_dc', 'am_ch_oem')
    p.edge('am_cg', 'am_ch_oem')
    p.edge('am_cg', 'am_ch_dist')
    p.edge('am_cg', 'am_ch_aib')
    p.edge('am_em', 'am_ch_var')
    p.edge('am_ch_oem', 'am_c0')
    p.edge('am_ch_dist', 'am_c1', dashed=True)
    p.edge('am_ch_hs', 'am_c2')
    p.edge('am_c2', 'am_e1')
    p.edge('am_c0', 'am_e2', dashed=True)
    p.edge('am_ch_aib', 'am_e3', dashed=True)
    p.edge('am_ch_var', 'am_e4')
    return p


# ══════════════════════════════════════════════════════════════════
def tsmc():
    p = Plate(
        'TSMC — 장비 공급사 이름을 하나도 적지 않은 채, 상위 10사가 매출 3조 8,090억 대만달러의 78%를 가져간다',
        '고객은 A·B·C 세 글자로만 나온다. 2023년 25%였던 B가 17%로 내려오고, A가 12%에서 19%로 올라섰다.',
        [166, 146, 158, 140, 156, 146], layers=L6,
        foot=[
            '① 20-F는 장비·소재 공급사를 「한정된 수의 공급사」로만 적는다. ASML·어플라이드머티리얼즈 같은 이름은 공급사로 등장하지 않는다.',
            '② 지역 매출은 고객 본사 소재지 기준이다. 실제 출하지와 다를 수 있다고 20-F가 직접 적었다. 북미 75% · 중국 9% · 아시아태평양 9%.',
            '③ 출처: TSMC FY2025 Form 20-F — Item 3 Risk Factors, Item 4, Item 5, 재무제표 주석(10% 이상 고객).',
        ])
    b = p.box
    b(0, 'ts_eq', '반도체 장비 공급사', ['「한정된 수의 공급사」', '20-F에 이름 없음'])
    b(0, 'ts_wf', '원판 웨이퍼 공급사', ['대만·일본·독일·싱가포르 소수', '이름 없음'])
    b(0, 'ts_pw', '전력·용수', ['대만 내 확보를 위험으로 적었다'])

    b(1, 'ts', 'TSMC', ['FY2025 매출 3조 8,090억 대만달러', '설비투자 1조 2,724억 (409억 달러)'], kind='hero')

    b(2, 'ts_adv', '첨단 노드 7nm 이하', ['웨이퍼 매출의 74% (전년 69%)', '3nm 24% · 5nm 36% · 7nm 14%'])
    b(2, 'ts_mat', '성숙 노드·특수 공정', ['웨이퍼 매출의 26%'])
    b(2, 'ts_pkg', '첨단 패키징 3DFabric', ['CoWoS · SoIC · InFO', 'Fab 23·24 증설 중'])

    b(3, 'ts_ch', '팹리스·IDM 직접 거래', ['웨이퍼 제조가 순매출의 약 86%'])

    b(4, 'ts_a', '고객 A (익명)', ['매출의 19% · 7,270억 대만달러', '2024년 12%에서 올라섰다'])
    b(4, 'ts_b', '고객 B (익명)', ['매출의 17% · 6,452억 대만달러', '2023년 25%에서 내려왔다'])
    b(4, 'ts_r', '상위 10사 합계 78%', ['매출채권 잔액의 84%'])
    b(4, 'ts_o', '그 밖의 고객 22%', [])

    b(5, 'ts_e1', 'HPC', ['2조 1,929억 대만달러 · 58%', '전년 대비 +48%'])
    b(5, 'ts_e2', '스마트폰', ['1조 1,108억 대만달러 · 29%'])
    b(5, 'ts_e3', 'IoT · 자동차', ['각 5% (1,910억 · 1,867억)'])
    b(5, 'ts_e4', '가전·기타', ['3%'])

    p.edge('ts_eq', 'ts', dashed=True)
    p.edge('ts_wf', 'ts')
    p.edge('ts_pw', 'ts')
    p.edge('ts', 'ts_adv')
    p.edge('ts', 'ts_mat')
    p.edge('ts', 'ts_pkg')
    p.edge('ts_adv', 'ts_ch')
    p.edge('ts_mat', 'ts_ch')
    p.edge('ts_pkg', 'ts_ch')
    p.edge('ts_ch', 'ts_a')
    p.edge('ts_ch', 'ts_b')
    p.edge('ts_ch', 'ts_r')
    p.edge('ts_ch', 'ts_o')
    p.edge('ts_a', 'ts_e1', dashed=True)
    p.edge('ts_b', 'ts_e2', dashed=True)
    p.edge('ts_r', 'ts_e1', dashed=True)
    p.edge('ts_o', 'ts_e3', dashed=True)
    return p


# ══════════════════════════════════════════════════════════════════
def asml():
    p = Plate(
        'ASML — 렌즈를 한 회사에서만 받고, 매출 326억 유로 가운데 10%를 넘긴 고객 넷이 61.2%를 가져간다',
        '자재의 80%가 외부 공급망이고 상당수가 단일 조달이다. 최대 고객 한 곳이 매출의 23.9%다.',
        [164, 146, 162, 146, 156, 146], layers=L6,
        foot=[
            '① 「10% 넘는 고객 넷 합계 61.2%」와 「최대 고객 23.9%」는 서로 다른 공시다. 전자는 감사 주석, 후자는 연차보고서 서술이다.',
            '② 수주잔고도 둘이다. 회계기준 잔여 이행의무는 465억 유로, 경영진이 서한에서 말한 잔고는 388억 유로다. EUV 비중 분해는 공시가 없다.',
            '③ 출처: ASML FY2025 Form 20-F — 재무제표 주석(R13·R65~R71) 및 같은 회계연도 연차보고서 Strategic report.',
        ])
    b = p.box
    b(0, 'as_z', 'Carl Zeiss SMT', ['렌즈·거울·조명계 유일 공급사', '독점 계약, 끊기면 사업이 멈춘다'])
    b(0, 'as_v', '외부 부품 공급망', ['자재의 약 80%', '단일 조달이 많다'])
    b(0, 'as_rd', '자체 연구개발', ['46.99억 유로 · 매출의 14.4%'])

    b(1, 'as', 'ASML', ['FY2025 매출 326.67억 유로', '장비 535대 출하'], kind='hero')

    b(2, 'as_exe', 'EUV High-NA (EXE)', ['4대 · 11.57억 유로'])
    b(2, 'as_nxe', 'EUV Low-NA (NXE)', ['44대 · 104.46억 유로'])
    b(2, 'as_arfi', 'ArF 이머전', ['131대 · 103.11억 유로'])
    b(2, 'as_dry', 'ArF 건식·KrF·i-line', ['148대 · 17.36억 유로'])
    b(2, 'as_mi', '계측·검사', ['208대 · 8.25억 유로'])
    b(2, 'as_svc', '설치기반 관리(서비스)', ['81.93억 유로 · 매출의 25.1%'])

    b(3, 'as_ch', '팹 직접 판매·서비스 계약', ['시스템 244.74억 유로 · 74.9%'])

    b(4, 'as_c1', '최대 고객 (익명)', ['매출의 23.9% · 77.97억 유로', '2024년 16.6%에서 올라섰다'])
    b(4, 'as_c2', '2위 고객 (익명)', ['상위 2사 합계 38.0%'])
    b(4, 'as_c4', '10% 넘는 고객 넷 합계', ['200.00억 유로 · 61.2%', '매출채권은 상위 3사가 35.4%'])

    b(5, 'as_e1', '로직 팹', ['160.54억 유로 · 364대'])
    b(5, 'as_e2', '메모리 팹', ['84.20억 유로 · 171대'])
    b(5, 'as_e3', '중국 소재 고객', ['95.20억 유로 · 29.1%', '2024년 36.1%에서 내려왔다'])

    p.edge('as_z', 'as')
    p.edge('as_v', 'as')
    p.edge('as_rd', 'as')
    for t in ['as_exe', 'as_nxe', 'as_arfi', 'as_dry', 'as_mi', 'as_svc']:
        p.edge('as', t)
        p.edge(t, 'as_ch')
    p.edge('as_ch', 'as_c1')
    p.edge('as_ch', 'as_c2')
    p.edge('as_ch', 'as_c4')
    p.edge('as_c1', 'as_e1', dashed=True)
    p.edge('as_c2', 'as_e1', dashed=True)
    p.edge('as_c4', 'as_e2', dashed=True)
    p.edge('as_c4', 'as_e3', dashed=True)
    return p


# ══════════════════════════════════════════════════════════════════
def summary():
    p = Plate(
        '요약 — 렌즈 한 회사에서 시작한 사슬이 TSMC 한 곳을 지나 NVIDIA와 AMD로 갈라진다',
        'ASML과 TSMC는 서로를 공시에서 지명하지 않는다. 반면 NVIDIA와 AMD는 TSMC를 10-K에 실명으로 적는다.',
        [150, 132, 156, 148, 156, 150],
        layers=['광학·부품', '노광 장비', '파운드리·후공정', '칩 설계사', '고객', '최종 수요처'],
        foot=[
            '① ASML과 TSMC를 잇는 선만 점선이다. 두 회사 모두 상대를 공시에 적지 않고 고객·공급사를 익명으로 처리한다.',
            '② 최종 수요처의 금액은 회사마다 회계연도가 다르다. NVIDIA는 2026-01-25, 나머지 셋은 2025년 말 종료 기준이다.',
            '③ 통화가 섞여 있다. NVIDIA·AMD는 달러, TSMC는 대만달러, ASML은 유로로 적었다.',
        ])
    b = p.box
    b(0, 'sm_z', 'Carl Zeiss SMT', ['렌즈·거울 유일 공급사', '독점 계약'])
    b(0, 'sm_v', '외부 부품 공급망', ['ASML 자재의 약 80%'])

    b(1, 'sm_as', 'ASML', ['매출 326.67억 유로', '장비 535대 · EUV 48대'], kind='hero')

    b(2, 'sm_ts', 'TSMC', ['매출 3조 8,090억 대만달러', '상위 10사가 78% · 고객명 비공개'], kind='hero')
    b(2, 'sm_mem', 'SK하이닉스·마이크론·삼성전자', ['메모리'])
    b(2, 'sm_osat', '홍하이·위스트론·파브리넷', ['퉁푸·SPIL·KYEC', '조립·시험·패키징'])

    b(3, 'sm_nv', 'NVIDIA', ['매출 2,159.38억 달러', '컴퓨트·네트워킹이 89.6%'], kind='hero')
    b(3, 'sm_am', 'AMD', ['매출 346.39억 달러', '데이터센터가 48.0%'], kind='hero')

    b(4, 'sm_c1', 'NVIDIA 직접고객 갑·을', ['총매출의 22%와 14%', '이름 비공개'])
    b(4, 'sm_c2', '간접고객군', ['CSP·네오클라우드·AI 모델 회사'])
    b(4, 'sm_c3', 'OpenAI', ['AMD GPU 6기가와트 계약'])
    b(4, 'sm_c4', 'PC·콘솔 OEM', ['AMD는 10% 넘는 고객이 없다'])

    b(5, 'sm_e1', 'AI 데이터센터', ['NVIDIA 1,937.37억 달러', 'TSMC의 HPC 매출 비중 58%'])
    b(5, 'sm_e2', '스마트폰', ['TSMC 매출의 29%'])
    b(5, 'sm_e3', 'PC·게이밍', ['NVIDIA 160.42억 · AMD 145.50억 달러'])
    b(5, 'sm_e4', '자동차·임베디드', ['AMD 34.54억 달러 · TSMC 5%'])

    p.edge('sm_z', 'sm_as')
    p.edge('sm_v', 'sm_as')
    p.edge('sm_as', 'sm_ts', dashed=True)
    p.edge('sm_ts', 'sm_nv')
    p.edge('sm_ts', 'sm_am')
    p.edge('sm_mem', 'sm_nv')
    p.edge('sm_mem', 'sm_am', dashed=True)
    p.edge('sm_osat', 'sm_nv')
    p.edge('sm_osat', 'sm_am')
    p.edge('sm_nv', 'sm_c1')
    p.edge('sm_nv', 'sm_c2')
    p.edge('sm_am', 'sm_c3')
    p.edge('sm_am', 'sm_c4')
    p.edge('sm_c1', 'sm_e1', dashed=True)
    p.edge('sm_c2', 'sm_e1')
    p.edge('sm_c3', 'sm_e1')
    p.edge('sm_c4', 'sm_e3', dashed=True)
    return p


PLATES = [('NVIDIA', nvidia), ('AMD', amd), ('TSMC', tsmc), ('ASML', asml),
          ('네 회사를 한 장으로', summary)]

LEGEND = ('<div class="lg"><b>계층</b>'
          '<span><i class="sw" style="background:#f2f4f8"></i>공급사</span>'
          '<span><i class="sw" style="background:#e8eef7;border-color:#39415a"></i>회사</span>'
          '<span><i class="sw" style="background:#eef3ee"></i>사업부문</span>'
          '<span><i class="sw" style="background:#f7f2ea"></i>채널</span>'
          '<span><i class="sw" style="background:#f4eef4"></i>고객</span>'
          '<span><i class="sw" style="background:#f1f1f4"></i>최종 수요처</span>'
          '<b style="margin-left:10px">선</b>'
          '<span><svg width="30" height="10"><line x1="0" y1="5" x2="28" y2="5" '
          'stroke="#8b93a5" stroke-width="1.4"/></svg>SEC 공시가 직접 잇는 관계</span>'
          '<span><svg width="30" height="10"><line x1="0" y1="5" x2="28" y2="5" '
          'stroke="#8b93a5" stroke-width="1.4" stroke-dasharray="5 4"/></svg>'
          '공시에 없어 반대편 공시·업계 자료로 이은 것</span></div>')


def build():
    blocks = []
    for name, fn in PLATES:
        blocks.append('<h2>%s</h2><div class="card">%s</div>' % (esc(name), fn().render()))
    blocks.append('<h2>범례</h2>' + LEGEND)
    intro = INTRO
    return page('네 회사의 밸류체인', intro, blocks, OUT)


INTRO = """<h1>네 회사의 밸류체인 — NVIDIA · AMD · TSMC · ASML</h1>
<p class="sub">최신 SEC 공시 넷을 읽고 공급사부터 최종 수요처까지 한 줄로 세웠다.
NVIDIA는 FY2026 10-K(2026-01-25 종료), AMD는 FY2025 10-K(2025-12-27 종료),
TSMC와 ASML은 FY2025 20-F(2025-12-31 종료)다.</p>
<h2>조사에서 나온 것</h2>
<p><b>공급사는 이름이 나오고 고객은 안 나온다.</b> NVIDIA는 TSMC·삼성전자·SK하이닉스·마이크론과
홍하이·위스트론·파브리넷을 10-K 본문에 실명으로 적는다. AMD도 TSMC·GlobalFoundries·UMC·삼성전자와
조립 협력사 셋을 적는다. 반대로 고객은 넷 다 익명이다. NVIDIA는 「직접고객 한 곳이 22%」,
TSMC는 「고객 A가 19%」, ASML은 「최대 고객이 23.9%」로만 적는다.</p>
<p><b>TSMC는 장비 공급사를 한 곳도 적지 않는다.</b> 20-F 전문에 ASML·어플라이드머티리얼즈·램리서치·KLA·
도쿄일렉트론이 공급사로 등장하지 않는다. 「한정된 수의 공급사」라는 표현이 전부다. 그래서 이 문서에서
ASML과 TSMC를 잇는 선은 점선이다. 사슬에서 가장 중요한 고리인데 두 회사 공시 어디에도 그것이 없다.</p>
<p><b>집중도의 방향이 회사마다 다르다.</b> NVIDIA는 상위 두 고객 비중이 FY2025 12%·11%에서
FY2026 22%·14%로 뛰었다. TSMC는 1위 고객이 25%(2023)에서 17%(2025)로 내려온 대신 다른 한 곳이
12%에서 19%로 올라섰다. ASML은 최대 고객이 16.6%에서 23.9%로 올라섰다. AMD만 반대다 —
FY2025·FY2024에는 매출 10%를 넘긴 고객이 아예 없다.</p>
<p><b>사업부문 비중.</b> NVIDIA는 두 부문뿐이고 컴퓨트·네트워킹이 89.6%다. AMD는 셋으로 갈리는데
데이터센터 48.0%·클라이언트와 게이밍 42.0%·임베디드 10.0%다. TSMC는 공정 노드로 갈리며
7nm 이하 첨단 노드가 웨이퍼 매출의 74%, 그중 5nm 하나가 36%다. ASML은 시스템 74.9%·서비스 25.1%이고
시스템 안에서 EUV 48대가 116.03억 유로, ArF 이머전 131대가 103.11억 유로다.</p>
<p><b>제조를 어디까지 들고 있나가 갈린다.</b> AMD는 2025년 3월 ZT Systems를 32억 달러에 사서 랙 단위
설계 역량을 안으로 들이고, 그해 10월 제조 부문만 Sanmina에 24억 달러로 넘겼다. 설계는 안에 두고 제조는
밖에 맡기기로 정리한 것이다. NVIDIA는 애초에 조립을 홍하이·위스트론·파브리넷에 맡긴다.</p>
"""


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(build())
