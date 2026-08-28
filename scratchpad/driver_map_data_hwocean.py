# -*- coding: utf-8 -*-
# 드라이버 지도 데이터 — 한화오션. 형식은 driver_map_data_hdhi.py(단일 평가·단일 축)와
# driver_map_data_hanmi.py(역산 축)를 섞은 꼴이다 — 같은 편 하나가 DCF와 역산을 둘 다
# 계산했기 때문에 축이 둘(dcf·rev)이고, 둘 다 doc='260307' 한 편에서 나온다.
#
# 축을 이렇게 나눈 이유: 원문 ❶~❻은 수주잔고 → 매출 → EBIT margin → FCFF → 현재가치 →
# 주당가치로 이어지는 표준 DCF다(2026~2030년 5개년, 연도마다 숫자를 따로 깔았으므로
# 간이 DCF가 아니라 dcf 축). ❼은 방향이 반대다 — 지금 EV가 옳다면 얼마를 벌어야
# 하는지를 거꾸로 푸는 역산이다. 같은 WACC·영구성장률을 그대로 쓰지만 입력에 가격이
# 들어가므로 dcf 축의 「결과」로 두지 않고 별도 축(rev)으로 나눴다.
#
# 값은 요약본(content/understanding/회계사/[260307]...)에 있는 것만 옮겼다. line= 은
# 그 요약본 파일에서 실제로 그 숫자가 있는 줄 번호다(직접 세어 확인).
#
# 원문(요약본): content/understanding/회계사/[260307] DCF 내재가치 7만 7900원, 주가보다
# 38% 아래 - 한화오션 - 엘곰.md
# 원출처: 네이버 프리미엄 「한화오션 주식가치 적정성 평가」(엘곰), 2026-03-07. 본문 표는
# 텍스트로 실려 있어 이미지를 뜰 필요가 없었다.
#
# 이 원문은 한화시스템이나 그 지분을 한 번도 언급하지 않는다. 같은 저장소의 한화시스템
# 편([260711] DCF 내재가치 82,941원 - 한화시스템 - 엘곰)이 FVOCI로 잡은 한화오션 지분
# 약 4.6조원과 이 편의 값을 잇는 계산은 요약본에도, 이 지도에도 넣지 않았다 — 견줄 만한
# 자리라는 사실만 요약본 본문에 적었다.

SUM = 'content/understanding/회계사/'

DOCS = {
    '260307': '[260307] DCF 내재가치 7만 7900원, 주가보다 38% 아래 - 한화오션 - 엘곰.md',
}

# 이 종목은 평가가 한 편뿐이라 「옛 값」이 없다. STALE_BEFORE를 이 문서보다 이른 값으로
# 둬서 is_stale이 항상 False가 되게 한다.
STALE_BEFORE = '260101'
STALE_WHY = '한화오션을 값으로 매긴 평가는 이 한 편(2026-03-07)뿐이라 옛 값 구분이 없다.'


def is_stale(doc_key):
    return doc_key < STALE_BEFORE


AXIS_ERAS = [
    dict(id='now', label='지금 · 2026',
         sub='한화오션을 값으로 매긴 평가는 이 한 편(2026-03-07)뿐이다. 같은 편이 DCF와 '
             '역산을 둘 다 계산한다.',
         axes=['dcf', 'rev']),
]

# 다른 회사 모듈과 같은 배지 사전. 회사마다 값이 다르지 않다.
BASIS = {
    'consensus': ('컨센서스', '증권사 추정치를 그대로 받았다'),
    'research': ('산업 리서치', '외부 시장조사 성장률을 인용했다'),
    'history': ('과거 실적', '확정된 지난 실적에서 가져왔다'),
    'practice': ('시장 관행', '업계에서 통용되는 범위의 값을 골랐다'),
    'author': ('필자 판단', '필자가 이유를 밝히고 정한 값이다'),
    'quoted': ('외부 인용', '다른 기관이 낸 값을 그대로 옮겼다'),
    'none': ('근거 표시 없음', '원문에 이 값을 어디서 가져왔는지 없다'),
}

BY = {
    'author': ('엘곰', '필자가 직접 낸 값'),
    'ours': ('주인장', '주인장이 계산기로 낸 값'),
}

# 드라이버. dcf 축(w_ 접두어)과 rev 축(r_ 접두어)이 WACC 7.8%·영구성장률 2.0%를
# 공유한다 — 같은 값이지만 두 축의 표에 각각 나오게 다른 키로 뒀다(원문도 ❼에서
# 두 값을 다시 한 번 적는다).
DRIVERS = {
    # ── dcf (260307) ───────────────────────────────────────────
    'w_base': dict(
        label='기준연도 매출 (2025 실제)', axis='dcf', doc='260307', line=39,
        base='12.69조원', basis='history',
        why='2025년 실제 매출 12.6884조원을 기준연도로 그대로 썼다. 가정표에는 반올림한 '
            '12.69조원으로 적는다.',
        impact='2026년 매출 14.2조원의 출발점이다.'),
    'w_rev_path': dict(
        label='매출 경로 (2026~2030)', axis='dcf', doc='260307', line=40,
        base='14.2 → 15.8 → 17.6 → 19.2 → 20.5조원', short='14.2조원→20.5조원',
        basis='author',
        why='2026~2030년 매출을 조원 단위로 직접 깔았다. backlog(수주잔고)가 풍부하고 '
            '상선 고선가·특수선 확대를 반영했다고 밝힌다.',
        impact='8개년이 아니라 5개년 FCFF 전체의 밑동이다. 2030년 매출 20.5조원은 2025년 '
               '실적(12.69조원)의 약 1.6배다.'),
    'w_opm': dict(
        label='EBIT margin (2026~2030)', axis='dcf', doc='260307', line=41,
        base='10.5% → 11.5% → 12.2% → 12.3% → 12.0%', short='10.5%→12.2%(정점)→12.0%',
        basis='author',
        why='2025년 실제 8.7%에서 개선되는 경로로 직접 놓았다. 2028년 12.2%가 정점이고 '
            '2029~2030년은 12.3%·12.0%로 소폭 내려온다.',
        impact='2030년 EBIT 2.460조원을 만든다 — 2025년 실제 영업이익 1.1091조원의 약 2.2배다.'),
    'w_tax': dict(
        label='법인세율', axis='dcf', doc='260307', line=42, base='24%', basis='author',
        why='정상화 유효세율 가정이라고만 적는다. 별도 근거는 없다.',
        impact='EBIT × (1−24%) = NOPAT. D&A·CAPEX가 같은 비율로 상쇄되고 ΔNWC를 0으로 '
               '둬 NOPAT이 그대로 FCFF가 된다.'),
    'w_dna_capex': dict(
        label='D&A·CAPEX', axis='dcf', doc='260307', line=43, base='각 매출의 2.8%',
        basis='author',
        why='D&A는 자본집약 산업 평균적 가정, CAPEX는 유지+확장 투자가 감가상각과 '
            '유사하다는 이유로 두 값을 같게 뒀다.',
        impact='두 값이 상쇄돼 FCFF 계산에서 실질적으로 사라진다 — FCFF ≈ NOPAT.'),
    'w_nwc': dict(
        label='ΔNWC(운전자본증감)', axis='dcf', doc='260307', line=45,
        base='0에 가깝게 가정', basis='author',
        why='선수금·중도금 구조상 일반 제조업보다 운전자본 변동이 완만하다는 이유로 '
            '0에 가깝게 뒀다.',
        impact='FCFF 계산식에서 이 항이 실질적으로 빠진다.'),
    'w_rf': dict(
        label='무위험수익률', axis='dcf', doc='260307', line=46, base='3.6%', basis='quoted',
        why='2026년 3월 6일 한국 10년물 국고채 금리 3.616%를 반올림해 썼다.',
        impact='Cost of equity 8.6%(=3.6%+1.0×5.0%)의 절반 가까이를 이 항이 만든다.'),
    'w_beta': dict(
        label='Beta', axis='dcf', doc='260307', line=47, base='1.0', basis='quoted',
        why='Yahoo Finance 5년 월간 베타를 그대로 썼다.',
        impact='시장위험프리미엄 5.0%를 그대로 곱해 Cost of equity에 반영된다 — 1.0이라 '
               '가산분이 시장위험프리미엄과 같다.'),
    'w_mrp': dict(
        label='시장위험프리미엄', axis='dcf', doc='260307', line=48, base='5.0%',
        basis='author',
        why='"보수적 실무가정"이라고만 적혀 있다. 왜 5.0%인지 별도 근거는 없다.',
        impact='Cost of equity 8.6%의 절반(1.0×5.0%=5.0%p)을 만든다.'),
    'w_kd': dict(
        label='세전 Cost of debt', axis='dcf', doc='260307', line=50, base='3.8%',
        basis='quoted',
        why='2026년 3월 6일 한국 AA- 3년 회사채 금리 3.815%를 반올림해 썼다.',
        impact='WACC 계산에서 타인자본비용 항목을 만든다.'),
    'w_wacc': dict(
        label='WACC', axis='dcf', doc='260307', line=51, base='7.8%', basis='none',
        why='Cost of equity 8.6%·세전 Cost of debt 3.8%·세율 24%까지는 근거가 있지만, '
            'WACC를 낼 때 쓴 자기자본·타인자본 비중은 원문에 없다. "Equity 비중 우세 구조 '
            '반영"이라고만 적는다.',
        impact='5개년 FCFF와 터미널가치를 이 비율로 할인한다 — 6.14조원과 22.60조원의 '
               '크기를 정한다.'),
    'w_g': dict(
        label='영구성장률', axis='dcf', doc='260307', line=52, base='2.0%', basis='author',
        why='장기 명목성장률 보수 가정이라고 밝힌다.',
        impact='터미널가치 현재가치 22.60조원을 만든다 — Enterprise Value 28.74조원의 78.6%다.'),
    'w_netdebt': dict(
        label='순차입금', axis='dcf', doc='260307', line=15, base='4.8577조원',
        basis='history',
        why='2025년 말 공시 순차입금이다.',
        impact='Enterprise Value 28.74조원에서 이 값을 빼 Equity Value 23.88조원을 만든다.'),
    'w_shares': dict(
        label='발행주식수', axis='dcf', doc='260307', line=25, base='약 3.064억주',
        basis='history',
        why='2026년 3월 6일 기준 발행주식수다.',
        impact='Equity Value 23.88조원을 이 주식수로 나눠 주당가치를 낸다.'),
    'w_out': dict(
        label='주당 내재가치', axis='dcf', doc='260307', line=81, base='약 77,900원',
        basis='author',
        why='명시적 기간 FCFF 현재가치 6.14조원 + 터미널가치 현재가치 22.60조원 = '
            'Enterprise Value 28.74조원. 여기서 순차입금 4.86조원을 빼고 발행주식수로 '
            '나눈 값이다.',
        impact='평가기준일 종가 126,700원보다 약 38% 낮다.'),
    # ── rev (260307, 같은 편 ❼) ─────────────────────────────────
    'r_ev': dict(
        label='현재 EV', axis='rev', doc='260307', line=29, base='약 43.7조원',
        basis='author',
        why='시가총액 약 38.82조원에 순차입금 4.8577조원을 더해 필자가 직접 계산했다.',
        impact='역산의 출발값이다 — 이 EV를 WACC·g로 설명할 FCFF를 거꾸로 푼다.'),
    'r_wacc': dict(
        label='WACC (역산에도 그대로)', axis='rev', doc='260307', line=93, base='7.8%',
        basis='none',
        why='dcf 축과 같은 값이다. 자기자본·타인자본 비중이 원문에 없다는 한계도 그대로 '
            '따라온다.',
        impact='정상화 단계 FCFF를 이 비율로 할인해 EV와 맞춘다.'),
    'r_g': dict(
        label='영구성장률 (역산에도 그대로)', axis='rev', doc='260307', line=93, base='2.0%',
        basis='author',
        why='dcf 축과 같은 값이다.',
        impact='정상화 단계 이후 가치를 한 덩어리로 묶는다.'),
    'r_margin': dict(
        label='EBIT margin 가정 (역산)', axis='rev', doc='260307', line=93, base='12%',
        basis='author',
        why='역산에서 steady-state EBIT margin을 12%로 가정한다고 밝힌다. dcf 축 표의 '
            '2028~2030년 마진(12.2%→12.0%)과 비슷한 수준이다.',
        impact='EBIT 4조원을 매출로 환산하는 데 쓰인다 — 매출 약 34조원이 나온다.'),
    'r_out_fcff': dict(
        label='요구 steady-state FCFF', axis='rev', doc='260307', line=93,
        base='약 3.1조원', basis='author',
        why='EV 43.7조원을 WACC 7.8%·g 2.0%로 설명하는 데 필요한 정상화 FCFF라고 필자가 '
            '적는다. EV에서 이 값으로 되짚는 중간 계산식은 원문에 없다.',
        impact='dcf 축 2030년 FCFF 1.870조원의 약 1.7배다.'),
    'r_out_ebit': dict(
        label='요구 EBIT', axis='rev', doc='260307', line=93, base='4조원 이상',
        basis='author',
        why='요구 steady-state FCFF를 뒷받침하는 데 필요한 EBIT 수준이라고 필자가 적는다.',
        impact='dcf 축 2030년 EBIT 2.460조원의 약 1.6배가 넘는다.'),
    'r_out_rev': dict(
        label='요구 매출', axis='rev', doc='260307', line=93,
        base='약 34조원 (2025년 매출의 약 2.7배)', short='약 34조원',
        basis='author',
        why='요구 EBIT 4조원을 EBIT margin 가정 12%로 나눈 값이라고 필자가 적는다.',
        impact='2025년 실제 매출 12.69조원의 약 2.7배, dcf 축 2030년 매출 20.5조원의 약 1.7배다.'),
}

GROUPS = [
    dict(id='rev', name='매출 경로', q='얼마를 파는가',
         why='수주잔고 321.8억달러의 매출 전환을 출발점으로 놓고 5개년 매출을 조원 단위로 '
             '직접 깔았다.',
         corpus='2025년 실적 12.69조원 → 2030년 20.5조원.',
         members=dict(dcf=['w_base', 'w_rev_path'])),
    dict(id='earn', name='이익 경로', q='얼마를 남기는가',
         why='EBIT margin을 2025년 실제 8.7%에서 2028년 12.2%까지 올렸다가 2030년 12.0%로 '
             '살짝 내렸다. D&A·CAPEX를 같은 비율로 둬 FCFF가 사실상 NOPAT과 같다.',
         corpus='EBIT margin 10.5%(2026) → 12.2%(2028년 정점) → 12.0%(2030), 세율 24%.',
         members=dict(dcf=['w_opm', 'w_tax', 'w_dna_capex', 'w_nwc'])),
    dict(id='disc', name='할인율과 베타', q='미래의 돈을 얼마로 깎는가',
         why='Cost of equity·Cost of debt 구성요소는 근거가 있지만 WACC를 짤 때 쓴 '
             '자기자본·타인자본 비중은 원문에 없다.',
         corpus='Cost of equity 8.6%(=Rf 3.6%+β1.0×MRP 5.0%), 세전 Cost of debt 3.8%, '
                'WACC 7.8%.',
         members=dict(dcf=['w_rf', 'w_beta', 'w_mrp', 'w_kd', 'w_wacc'])),
    dict(id='growth', name='영구성장률', q='끝난 뒤를 얼마로 보나',
         why='터미널가치 현재가치가 Enterprise Value의 78.6%를 차지한다 — 이 값 하나가 '
             '결과의 대부분을 쥔다.',
         corpus='2.0%. 터미널가치 현재가치 22.60조원.',
         members=dict(dcf=['w_g'])),
    dict(id='net', name='순차입금·주식수', q='영업 밖에서 무엇을 빼고 나누나',
         why='둘 다 공시 실적값이다.',
         corpus='순차입금 4.8577조원, 발행주식수 약 3.064억주.',
         members=dict(dcf=['w_netdebt', 'w_shares'])),
    dict(id='req_in', name='역산의 출발값', q='무엇을 참으로 놓았나',
         why='시가총액에 순차입금을 더한 EV를 정답으로 놓고, dcf 축과 같은 WACC·영구성장률을 '
             '그대로 쓴다.',
         corpus='EV 약 43.7조원, WACC 7.8%, 영구성장률 2.0%.',
         members=dict(rev=['r_ev', 'r_wacc', 'r_g'])),
    dict(id='req_out', name='역산이 요구하는 것', q='얼마를 벌어야 지금 값이 되나',
         why='결과값 세 개(FCFF·EBIT·매출)만 원문에 있고, EV에서 여기로 이어지는 중간 '
             '계산식은 없다.',
         corpus='steady-state FCFF 약 3.1조원, EBIT 4조원 이상(margin 가정 12%), 매출 약 '
                '34조원(2025년 매출의 약 2.7배).',
         members=dict(rev=['r_margin', 'r_out_fcff', 'r_out_ebit', 'r_out_rev'])),
]

AXES = [
    dict(id='dcf', no='01', name='DCF', tag='이익을 가정해 값을 낸다 · 한화오션 유일 평가',
         kind='forward',
         latest=('260307', '2026-03-07', 'DCF 내재가치 7만 7900원, 주가보다 38% 아래'),
         sub='명시적 추정기간은 5년(2026~2030)이다. 수주잔고 321.8억달러의 매출 전환을 '
             '출발점으로 놓고, D&A와 CAPEX를 매출의 2.8%로 같게 둬 FCFF를 사실상 정상화 '
             'NOPAT과 같게 만들었다.',
         docs=['260307'],
         chain=['{w_base}에서 시작해 {w_rev_path}로 2026~2030년 매출을 깐다',
                '매출 × {w_opm} = EBIT, EBIT × (1 − {w_tax}) = NOPAT',
                '{w_dna_capex}·{w_nwc}가 상쇄되어 FCFF = NOPAT',
                'Σ FCFFₜ ÷ (1+{w_wacc})ᵗ, t=1…5 = 6.14조원 '
                '({w_rf}·{w_beta}·{w_mrp}가 Cost of equity 8.6%를 만든다)',
                'FCFF₅ × (1+{w_g}) ÷ ({w_wacc} − {w_g})를 현재가치로 당기면 22.60조원',
                '(6.14 + 22.60) − {w_netdebt} = Equity Value, ÷ {w_shares} = {w_out}'],
         out='주당 내재가치 약 77,900원 (평가기준일 종가 126,700원 대비 약 −38%)',
         verdict=None),
    dict(id='rev', no='02', name='역산', tag='가격에서 거꾸로 푼다 · 같은 편의 ❼',
         kind='reverse',
         latest=('260307', '2026-03-07', '시총이 요구하는 steady-state FCFF는 약 3.1조원'),
         sub='dcf 축과 같은 글, 같은 WACC 7.8%·영구성장률 2.0%를 그대로 쓴다. 다만 이번에는 '
             'EV 43.7조원을 정답으로 놓고 거꾸로 푼다 — 중간 계산식은 원문에 없고 결과값만 '
             '제시된다.',
         docs=['260307'],
         chain=['{r_ev}를 정답으로 놓는다',
                '{r_wacc}·{r_g}로 정상화 단계의 FCFF를 거꾸로 풀면 → {r_out_fcff}',
                '이를 뒷받침하려면 → {r_out_ebit}',
                '{r_margin}로 나누면 → {r_out_rev}'],
         out='steady-state FCFF 약 3.1조원 · EBIT 4조원 이상 · 매출 약 34조원 필요 '
             '(2025년 매출의 약 2.7배)',
         verdict=('현재가는 조선업 본업만으로 정당화되지 않는다',
                   'dcf 축 5개년 추정의 마지막 해(2030년) FCFF는 1.870조원인데, 역산이 '
                   '요구하는 정상화 FCFF는 약 3.1조원이다. 그 차이를 필자는 미국 해군 협력·'
                   '캐나다 잠수함·필리조선소 같은 방산·북미 전략자산 옵션으로 돌린다.')),
]

LEDE = ('한화오션을 값으로 매긴 평가는 이 한 편(2026-03-07)뿐이고, 같은 편이 DCF와 역산을 '
        '둘 다 계산한다. DCF 축은 5개년(2026~2030) 추정으로 주당 내재가치 약 77,900원을 '
        '내고, 평가기준일 종가 126,700원보다 <b>약 38% 낮다</b>. 같은 WACC 7.8%·영구성장률 '
        '2.0%로 거꾸로 풀면, 현재 EV 약 43.7조원을 설명하려면 정상화 단계 FCFF가 <b>약 '
        '3.1조원</b>까지, 매출로는 2025년 실적의 약 2.7배인 <b>34조원 안팎</b>까지 올라가야 '
        '한다. 필자는 이 간극을 조선업 본업이 아니라 미국 해군 협력·캐나다 잠수함·필리조선소 '
        '같은 방산·북미 전략자산 옵션이 메운다고 해석한다.')

# rev 축이 'reverse'이므로 _author_scenarios_html이 dmd.SCENARIOS를 무조건 읽는다.
# 앞 두 행은 엘곰이 원문(dcf 축 결과·rev 축 ❼ 결과)에 직접 적은 값이고, 뒤 두 행은
# 주인장이 그 값으로 되돌린 산수다(새 가정 없음 — 나누는 것까지만).
SCENARIOS = dict(
    asof='2026-03-06',
    price='126,700원 (KRX 종가)',
    mcap='약 38.82조원',
    formula='엘곰이 낸 DCF 기준값(dcf 축)과, 그가 같은 편 ❼에서 직접 적은 역산 결과(rev 축)를'
            ' 나란히 놓았다. 성장·마진·WACC 7.8%·영구성장률 2.0% 가정은 두 계산에서 같다 — '
            '다른 것은 EV를 결과로 내느냐, EV를 정답으로 두고 거꾸로 푸느냐다.',
    head=['시나리오', 'WACC · g', '근거 · 출처', '값', '기준값 대비', '계산'],
    rows=[
        dict(cells=['기준 DCF (엘곰이 쓴 값)', 'WACC 7.8% · g 2.0%',
                    '5개년 FCFF·터미널가치로 직접 계산', '약 77,900원', '−38%'],
             by='author', doc='260307', line=81, tone='low'),
        dict(cells=['역산 필요 수준 (같은 편 ❼)', 'WACC 7.8% · g 2.0%',
                    'EV 43.7조원을 설명하는 데 필요한 steady-state FCFF',
                    '약 3.1조원', '—'],
             by='author', doc='260307', line=93, tone='high'),
        dict(cells=['검산 — Equity Value ÷ 발행주식수', '가정 그대로',
                    '23.88조원 ÷ 3.064억주. 그가 적은 "약 77,900원"과 맞는다',
                    '77,939원', '−38.5%'],
             by='ours', doc='260307', line=83, tone='low'),
        dict(cells=['검산 — 요구 FCFF ÷ dcf 축 2030년 FCFF', '가정 그대로',
                    '3.1조원 ÷ 1.870조원. 정상화 단계에서 지금 5개년 추정 마지막 해보다 '
                    '얼마나 더 벌어야 하는지', '약 1.7배', '—'],
             by='ours', doc='260307', line=93, tone='mid'),
    ],
    note='앞 두 행은 엘곰이 원문에 직접 적은 값이고, 뒤 두 행은 주인장이 그 값으로 되돌린 '
         '산수다(새 가정 없음).',
    punch='이 평가는 두 방향에서 같은 결론에 닿는다. DCF로 값을 내면 주가보다 <b>약 38% '
          '낮고</b>, 거꾸로 지금 EV를 설명하려면 정상화 FCFF가 dcf 축 5개년 추정 마지막 '
          '해의 <b>약 1.7배</b>까지 올라가야 한다. 필자는 이 간극을 조선업 본업이 아니라 '
          '<b>미국 해군 협력·캐나다 잠수함·필리조선소 같은 방산·북미 전략자산 옵션</b>이 '
          '메운다고 본다.',
)

TIMELINE_LABEL = '지금까지 나온 값 — DCF·역산 한 편'

TIMELINE = [
    ('2026-03-07', 'dcf', 'price', '내재가치 77,900원', '', '필자 표기 그대로', 'author'),
    ('2026-03-07', 'rev', 'ask', '그때 EV 43.7조원이',
     'steady-state FCFF 약 3.1조원(EBIT 4조원 이상·매출 약 34조원)을 요구', '역산', 'author'),
]
