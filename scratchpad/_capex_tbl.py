# -*- coding: utf-8 -*-
"""데이터센터 자본지출 층 넷의 표. 값은 `insights/models/` 의 모델이 낸다.

원자료는 `insights/models/raw/capex.json` 하나다. 여기서 값을 손으로 옮겨 적지
않는다 — 모델을 고치면 표가 같이 바뀌어야 어긋난 칸이 저절로 드러난다.

`_model_tbl` 이 이 파일의 TABLES 를 자기 TABLES 에 합친다. 그래서 본문 표와
`gen_model_facts.py` 가 내는 사실표가 한 함수에서 나온다.
"""
import json
import io
import os
import sys

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'insights', 'models')
if _MODELS not in sys.path:
    sys.path.insert(0, _MODELS)

import lego_capex as LG                                          # noqa: E402
import ground_capex as GC                                        # noqa: E402
import trinity_debt as TD                                        # noqa: E402
import spacex_payback as SX                                      # noqa: E402
import bridge_capex as BR                                        # noqa: E402

RAW = json.loads(io.open(os.path.join(_MODELS, 'raw', 'capex.json'),
                         encoding='utf-8').read())


def _tbl(tid):
    for t in RAW['tables']:
        if t['id'] == tid:
            return t
    raise KeyError(tid)


_C = _tbl('lego-cost')
_L = _tbl('lego-labor')
_S = _tbl('lego-schedule')
_P = _tbl('lego-power-only')
_LY = _tbl('ground-layers')
_G = _tbl('ground-assump')
_B = _tbl('trinity-backstop')
_D = _tbl('trinity-debt')
_X = _tbl('spacex-econ')
_FR = _tbl('frame-capex')
_SH = _tbl('frame-sheet')
_SC = _tbl('frame-scn')
_LV = _tbl('frame-lever')


def _v(t, k):
    return t['rows'][k][1]


# ── 레고 ────────────────────────────────────────────────────────────────
def lego_cost_table():
    """MW당 총원가와 그 차이. 절감 항목 둘의 합이 차이와 같은지 본다."""
    head = ['무엇', '현장시공', '완전 모듈러', '차이', '성격']
    delta = _v(_C, 'stick_all_in') - _v(_C, 'modular_all_in')
    pct = LG.delta_pct(_v(_C, 'stick_all_in'), _v(_C, 'modular_all_in'))
    add = _v(_C, 'svc_saving') + _v(_C, 'install_saving')
    return head, [
        ['MW당 총원가', '$%.1f백만' % _v(_C, 'stick_all_in'),
         '$%.1f백만' % _v(_C, 'modular_all_in'), '$%.1f백만' % delta, '원문 값'],
        ['비싼 쪽 대비', '—', '—', '%.1f%%' % pct, '모델이 낸 값'],
        ['원문이 적은 비율', '—', '—', '%g%%' % _v(_C, 'stated_pct'), '원문 값'],
        ['건설서비스 절감', '—', '—', '$%.1f백만' % _v(_C, 'svc_saving'), '원문 값'],
        ['설치비 절감', '—', '—', '$%.1f백만' % _v(_C, 'install_saving'), '원문 값'],
        ['그 둘의 합', '—', '—', '$%.1f백만' % add, '모델이 낸 값'],
    ]


def lego_labor_table():
    """공장으로 옮겨 아끼는 인건비가 발표된 차이의 몇 할인가."""
    s = LG.labor_saving(_v(_L, 'hours_field'), _v(_L, 'hours_after'),
                        _v(_L, 'wage_field_eff'), _v(_L, 'wage_factory'))
    share = LG.explained_share(s['saving'], _v(_C, 'stated_delta'))
    head = ['무엇', '값', '성격']
    return head, [
        ['MW당 현장 인시(옮기기 전)', '%s시간' % format(_v(_L, 'hours_field'), ','), '원문 값'],
        ['MW당 현장 인시(옮긴 뒤)', '%s시간' % format(_v(_L, 'hours_after'), ','), '원문 값'],
        ['공장으로 옮긴 시간', '%s시간' % format(s['moved_hours'], ','), '모델이 낸 값'],
        ['실질 현장 전기공 임금', '$%g/시간' % _v(_L, 'wage_field_eff'), '원문 값'],
        ['공장 임금', '$%g/시간' % _v(_L, 'wage_factory'), '원문 값'],
        ['옮기기 전 MW당 인건비', '$%s' % format(int(s['before']), ','), '모델이 낸 값'],
        ['옮긴 뒤 MW당 인건비', '$%s' % format(int(s['after']), ','), '모델이 낸 값'],
        ['아끼는 인건비', '$%s' % format(int(s['saving']), ','), '모델이 낸 값'],
        ['발표된 차이', '$%s' % format(int(_v(_C, 'stated_delta') * 1e6), ','), '원문 값'],
        ['인건비로 설명되는 몫', '%.0f%%' % share, '모델이 낸 값'],
    ]


def lego_sched_table():
    """공법마다 공사 기간과 허가까지 포함한 기간."""
    head = ['방식', '공사(하한)', '공사(상한)', '허가 포함', '현장시공 대비']
    body = []
    st_lo, st_hi = _S['rows']['stick'][1], _S['rows']['stick'][2]
    for v in _S['rows'].values():
        name, lo, hi, alo, ahi = v[0], v[1], v[2], v[3], v[4]
        span = '%g~%g개월' % (alo, ahi) if alo else '—'
        cut = LG.months_cut((st_lo + st_hi) / 2.0, (lo + hi) / 2.0)
        body.append([name, '%g개월' % lo, '%g개월' % hi, span,
                     '—' if name == '현장시공' else '%.0f%% 짧다' % cut])
    body.append(['전력 스코프만 옮길 때', '%g개월' % _v(_P, 'months_modular'),
                 '%g개월' % _v(_P, 'months_modular'), '—',
                 '%.0f%% 짧다' % LG.months_cut(_v(_P, 'months_stick'),
                                             _v(_P, 'months_modular'))])
    return head, body


def lego_vendor_table():
    """벤더 하나가 MW당 총원가에서 가져가는 몫."""
    a = LG.content_share(_v(_C, 'vertiv_discrete'), _v(_C, 'stick_all_in'))
    b = LG.content_share(_v(_C, 'vertiv_fullstack'), _v(_C, 'modular_all_in'))
    head = ['파는 방식', 'MW당 콘텐츠', '그 홀의 MW당 총원가', '총원가에서 차지하는 몫']
    return head, [
        ['낱개 장비', '$%.1f백만' % _v(_C, 'vertiv_discrete'),
         '$%.1f백만' % _v(_C, 'stick_all_in'), '%.0f%%' % a],
        ['풀스택 모듈', '$%.1f백만' % _v(_C, 'vertiv_fullstack'),
         '$%.1f백만' % _v(_C, 'modular_all_in'), '%.0f%%' % b],
        ['차이', '$%.1f백만 늘어난다' % (_v(_C, 'vertiv_fullstack')
                                  - _v(_C, 'vertiv_discrete')),
         '$%.1f백만 준다' % (_v(_C, 'stick_all_in') - _v(_C, 'modular_all_in')),
         '%.0f%%p 늘어난다' % (b - a)],
    ]


# ── 지상 데이터센터 ──────────────────────────────────────────────────────
def ground_layer_table():
    """층마다 MW당 자본이 매출에서 먹는 몫."""
    head = ['층', 'MW당 자본', '연 자본비', '매출에서 먹는 몫', '무엇이 막나']
    body = []
    for v in _LY['rows'].values():
        name, lo, hi, why = v[0], v[1], v[2], v[3]
        hi_v = hi if hi is not None else lo
        alo = GC.annual_capital(lo, _v(_G, 'wacc'), _v(_G, 'life_dc'))
        ahi = GC.annual_capital(hi_v, _v(_G, 'wacc'), _v(_G, 'life_dc'))
        slo = GC.revenue_share(lo, _v(_G, 'rev_hi'), _v(_G, 'wacc'), _v(_G, 'life_dc'))
        shi = GC.revenue_share(hi_v, _v(_G, 'rev_lo'), _v(_G, 'wacc'), _v(_G, 'life_dc'))
        span = '$%g~%g백만' % (lo, hi) if hi is not None else '$%g백만 이상' % lo
        body.append([name, span, '$%.2f~%.2f백만' % (alo, ahi),
                     '%.1f~%.1f%%' % (slo, shi), why])
    return head, body


def ground_power_table():
    """같은 글에 든 전기 단가 셋을 한 줄에 세운다."""
    head = ['단가', 'MWh당', 'MW당 연 전기값', '매출에서 먹는 몫', '모델 단가 대비']
    base = GC.power_cost_per_mw_year(_v(_G, 'power_price'), _v(_G, 'pue'),
                                    _v(_G, 'util'))
    rows = [('모델이 쓴 단가', _v(_G, 'power_price') * 1000),
            ('배후 자체발전 하한', _v(_G, 'btm_lo')),
            ('배후 자체발전 상한', _v(_G, 'btm_hi')),
            ('주요 시장 계통가', _v(_G, 'grid_price'))]
    body = []
    for name, p in rows:
        c = GC.power_cost_per_mw_year(GC.price_from_mwh(p), _v(_G, 'pue'),
                                      _v(_G, 'util'))
        body.append([name, '$%g' % p, '$%.2f백만' % (c / 1e6),
                     '%.1f~%.1f%%' % (c / 1e6 / _v(_G, 'rev_hi') * 100,
                                      c / 1e6 / _v(_G, 'rev_lo') * 100),
                     '%.2f배' % (c / base)])
    return head, body


def ground_early_table():
    """여섯 달 일찍 켜는 값이 전제하는 마진."""
    rev_mid = (_v(_G, 'rev_lo') + _v(_G, 'rev_hi')) / 2
    rev = GC.pulled_forward_revenue(_v(_G, 'early_mw'), _v(_G, 'early_months'), rev_mid)
    head = ['무엇', '값', '성격']
    body = [
        ['용량', '%gMW' % _v(_G, 'early_mw'), '원문 값'],
        ['앞당긴 기간', '%g개월' % _v(_G, 'early_months'), '원문 값'],
        ['MW당 연 매출', '$%g~%g백만' % (_v(_G, 'rev_lo'), _v(_G, 'rev_hi')), '원문 값'],
        ['먼저 받는 매출', '$%.0f백만' % rev, '모델이 낸 값'],
    ]
    for npv in (_v(_G, 'npv_lo'), _v(_G, 'npv_hi')):
        m = GC.implied_margin(npv, _v(_G, 'early_mw'), _v(_G, 'early_months'), rev_mid)
        body.append(['발표된 순현재가치 $%g백만' % npv, '그 매출의 %.0f%%' % m,
                     '모델이 낸 값'])
    return head, body


# ── GPU 금융 ────────────────────────────────────────────────────────────
def trinity_split_table():
    """바닥값 위 초과분을 나누는 1년차 계산을 다시 낸다."""
    s = TD.split(_v(_B, 'y1_floor'), _v(_B, 'y1_charge'), _v(_B, 'nvda_share'))
    head = ['무엇', '모델', '발표', '차이']
    rows = [('고객 청구가', _v(_B, 'y1_charge'), _v(_B, 'y1_charge')),
            ('백스톱 바닥값', _v(_B, 'y1_floor'), _v(_B, 'y1_floor')),
            ('초과분', s['excess'], _v(_B, 'y1_charge') - _v(_B, 'y1_floor')),
            ('엔비디아 몫', s['nvda'], _v(_B, 'y1_nvda')),
            ('네오클라우드 몫', s['neo'], _v(_B, 'y1_neo')),
            ('네오클라우드 실현 합계', s['neo_total'], _v(_B, 'y1_total'))]
    body = []
    for name, got, want in rows:
        body.append([name, '$%.2f' % got, '$%.2f' % want,
                     '일치' if abs(got - want) < 0.005 else '%+.2f' % (got - want)])
    body.append(['1년차 테이크레이트',
                 '%.1f%%' % TD.take_rate(s['nvda'], _v(_B, 'y1_charge')),
                 '%g%% (6년 평균)' % _v(_B, 'take_rate'), '모델이 낸 값'])
    return head, body


def trinity_gpu_table():
    """공시 총액에서 바닥값과 장수를 되짚는다."""
    floor = TD.implied_floor(_v(_B, 'sharon_total') * 1e9, _v(_B, 'sharon_gpus'),
                             _v(_B, 'sharon_years'))
    n = TD.gpus_behind(_v(_B, 'guarantee_per_100mw') * 1e9, _v(_B, 'curve_avg'),
                       _v(_B, 'backstop_years'))
    head = ['무엇', '값', '성격']
    return head, [
        ['샤론AI 백스톱 총액', '$%g십억' % _v(_B, 'sharon_total'), '회사 공시'],
        ['그 계약의 GPU 장수', '%s장' % format(_v(_B, 'sharon_gpus'), ','), '회사 공시'],
        ['역산한 평균 바닥값', '$%.3f/GPU·시간' % floor, '모델이 낸 값'],
        ['원문이 적은 값', '$%g/GPU·시간' % _v(_B, 'sharon_floor'), '원문 값'],
        ['예시 커브의 6년 평균', '$%g/GPU·시간' % _v(_B, 'curve_avg'), '원문 값'],
        ['100MW마다 늘어나는 우발채무', '$%g십억' % _v(_B, 'guarantee_per_100mw'), '원문 값'],
        ['그 뒤에 선 GPU 장수', '%s장' % format(int(n), ','), '모델이 낸 값'],
        ['GPU 한 장이 끌어가는 전력', '%.2fkW' % TD.kw_per_gpu(n, 100), '모델이 낸 값'],
    ]


def trinity_debt_table():
    """금리가 이익률을 깎는 폭에서 부채와 원가수익률을 푼다."""
    ratio = TD.implied_debt_to_revenue(_v(_D, 'rate_secured'), _v(_D, 'rate_unsecured'),
                                       _v(_D, 'pbt_unsecured'), _v(_D, 'pbt_secured'))
    head = ['무엇', '값', '성격']
    body = [
        ['담보를 붙였을 때 조달비용', '%g%%' % _v(_D, 'rate_secured'), '원문 값'],
        ['무담보로 갔을 때', '%g%%' % _v(_D, 'rate_unsecured'), '원문 값'],
        ['그때 세전이익률', '%g%% → %g%%' % (_v(_D, 'pbt_secured'),
                                       _v(_D, 'pbt_unsecured')), '원문 값'],
        ['금리 차', '%.2f%%p' % (_v(_D, 'rate_unsecured') - _v(_D, 'rate_secured')),
         '모델이 낸 값'],
        ['이익률이 깎인 폭', '%.1f%%p' % (_v(_D, 'pbt_secured') - _v(_D, 'pbt_unsecured')),
         '모델이 낸 값'],
        ['그 둘을 잇는 부채', '연 매출의 %.2f배' % ratio, '모델이 낸 값'],
    ]
    for ltv in (_v(_D, 'ltv_lo'), _v(_D, 'ltv_hi')):
        body.append(['담보인정비율 %g%% 일 때 원가수익률' % ltv,
                     '%.1f%%' % TD.implied_yield_on_cost(ratio, ltv), '모델이 낸 값'])
    body.append(['부채상환비율 문턱', '%g배' % _v(_D, 'dscr'), '원문 값'])
    return head, body


# ── 회수기간 ────────────────────────────────────────────────────────────
def spacex_payback_table():
    """파는 값마다 회수가 몇 해인가. 매출 기준과 현금 기준을 나란히 둔다."""
    head = ['파는 값', 'MW당 연 매출', '매출 기준 회수', '현금 기준 회수', '매출총이익률']
    body = []
    for label, key in (('지금 오픈AI 에 임대되는 값', 'rev_ms_current'),
                       ('리드타임 프리미엄 하한', 'rev_premium_lo'),
                       ('리드타임 프리미엄 상한', 'rev_premium_hi'),
                       ('API 추론으로 팔 때', 'rev_api')):
        rev = _v(_X, key)
        pc = SX.payback_on_cash(_v(_X, 'capex_per_gw'), rev, _v(_X, 'cost_per_gw_yr'))
        body.append([label, '$%g백만' % rev,
                     '%.2f년' % SX.payback_on_revenue(_v(_X, 'capex_per_gw'), rev),
                     '못 갚는다' if pc is None else '%.2f년' % pc,
                     '%.0f%%' % SX.gross_margin(rev, _v(_X, 'cost_per_gw_yr'))])
    return head, body


def spacex_arr_table():
    """발표된 매출 목표가 전제하는 MW당 값."""
    head = ['무엇', '값', '성격']
    p_lo = SX.implied_price(_v(_X, 'arr_target'), _v(_X, 'gw_hi'), _v(_X, 'monetize_share'))
    p_hi = SX.implied_price(_v(_X, 'arr_target'), _v(_X, 'gw_lo'), _v(_X, 'monetize_share'))
    return head, [
        ['2027년 증설 목표', '%g~%gGW' % (_v(_X, 'gw_lo'), _v(_X, 'gw_hi')), '회사 발표'],
        ['기가와트당 자본지출', '$%g십억' % _v(_X, 'capex_per_gw'), '원문 값'],
        ['그 곱', '$%g~%g십억' % (_v(_X, 'gw_lo') * _v(_X, 'capex_per_gw'),
                              _v(_X, 'gw_hi') * _v(_X, 'capex_per_gw')), '모델이 낸 값'],
        ['원문이 적은 폭', '$%g~%g십억' % (_v(_X, 'capex_total_lo'),
                                   _v(_X, 'capex_total_hi')), '원문 값'],
        ['목표 연간반복매출', '$%g십억' % _v(_X, 'arr_target'), '원문 값'],
        ['수익화 비중 가정', '%g%%' % _v(_X, 'monetize_share'), '원문 값'],
        ['그 목표가 전제하는 MW당 연 매출', '$%.0f~%.0f백만' % (p_lo, p_hi), '모델이 낸 값'],
    ]


def spacex_deal_table():
    """묶인 계약이 지금 임대가로 몇 해치인가."""
    head = ['계약', '총액', '용량', 'GW당 총액', '임대가로 환산한 두께']
    body = []
    for label, vk, gk in (('마이크로소프트가 올해 묶은 것', 'ms_contract_value',
                           'ms_contract_gw'),
                          ('2025년 10월 오픈AI 계약', 'openai_deal_value',
                           'openai_deal_gw')):
        v = SX.contract_value_per_gw(_v(_X, vk), _v(_X, gk))
        body.append([label, '$%g십억' % _v(_X, vk), '%gGW' % _v(_X, gk),
                     '$%.1f십억' % v,
                     '%.1f년치' % SX.years_implied(v, _v(_X, 'rev_ms_current'))])
    return head, body



# ── 다리 — 하향 총액과 상향 단가 ─────────────────────────────────────────
_GPUS_PER_SERVER = 8
_KW_PER_GPU = 2.10


def _amd(col, row):
    import json as _j
    import io as _io
    import os as _os
    raw = _j.loads(_io.open(_os.path.join(_MODELS, 'raw', 'tables.json'),
                            encoding='utf-8').read())
    for t in raw['tables']:
        if t['id'] == 'amd-capex':
            return t['rows'][row][t['columns'].index(col)]
    raise KeyError(row)


def _it_per_mw():
    per_gpu = BR.gpu_capex(_amd('B200', 'server_cost'),
                           _amd('B200', 'other_cluster_cost'), _GPUS_PER_SERVER)
    return per_gpu, BR.it_capex_per_mw(_KW_PER_GPU, per_gpu)


def bridge_frame_table():
    """엑셀이 낸 2026년 값. 전부 프레임 값이라 성격 열에 그렇게 적는다."""
    head = ['무엇', '값', '어느 칸', '성격']
    body = []
    for k in ('total_2025', 'total_2026', 'server_2026', 'dc_2026', 'five_year',
              'capex_to_sales', 'capex_to_ocf', 'fcf_2026', 'lease_jv_2026',
              'new_debt_2026', 'gap_2028'):
        what, val, unit, cite = _SH['rows'][k]
        body.append([what, '%s %s' % (format(val, ','), unit),
                     cite.replace('프레임 엑셀 ', ''), '프레임 값'])
    return head, body


def bridge_unit_table():
    """우리 원문이 그 틀의 빈칸에 넣는 값."""
    per_gpu, it = _it_per_mw()
    head = ['빈칸', '우리가 넣는 값', '어디서 왔나', '성격']
    return head, [
        ['GPU 한 장이 끄는 전력', '%.2fkW' % _KW_PER_GPU,
         'GPU 금융 층 — 우발채무와 바닥값에서 되짚었다', '모델이 낸 값'],
        ['메가와트당 칩 수', '%s장' % format(int(BR.gpus_per_mw(_KW_PER_GPU)), ','),
         '위 전력으로 나눴다', '모델이 낸 값'],
        ['칩 한 장의 선불 자본', '$%s' % format(int(per_gpu), ','),
         '추론 원가 모델 B200 열 — 서버 값에 망·저장·소프트웨어를 더해 여덟으로 나눴다',
         '원문 표 그림에서 읽은 값으로 계산'],
        ['메가와트당 IT 자본', '$%.1f백만' % it, '앞 둘의 곱', '모델이 낸 값'],
        ['메가와트당 시설·전력', '$10~20백만', '지상 층 — 전력을 끄는 층마다 다르다', '원문 값'],
        ['전부 포함 단가', '$%g백만' % _v(_X, 'capex_per_gw'),
         '회수 층 — 기가와트당 500억 달러', '원문 값'],
        ['자산 수명', '데이터센터 15년 · IT 5년', '지상 층 가정', '원문 값'],
        ['담보인정비율·부채상환비율', '70~80%% · 1.3배',
         'GPU 금융 층 — 은행이 요구하는 값', '원문 값'],
    ]


def bridge_gw_table():
    """용량을 세는 길 넷. 같은 해를 네 자로 잰다."""
    per_gpu, it = _it_per_mw()
    head = ['세는 길', '나누는 값', '단가', '신규 용량', '성격']
    dc = _v(_SH, 'dc_2026')
    srv = _v(_SH, 'server_2026')
    tot = _v(_SH, 'total_2026')
    return head, [
        ['시설 단가 상한으로', '데이터센터·전력 $%g십억' % dc, '$20백만/MW',
         '%.1fGW' % (dc / 20.0), '모델이 낸 값'],
        ['시설 단가 하한으로', '같은 값', '$10백만/MW', '%.1fGW' % (dc / 10.0),
         '모델이 낸 값'],
        ['우리 IT 단가로', '서버·칩 $%g십억' % srv, '$%.1f백만/MW' % it,
         '%.1fGW' % (srv / it), '모델이 낸 값'],
        ['전부 포함 단가로', '합산 $%g십억' % tot,
         '$%g백만/MW' % _v(_X, 'capex_per_gw'),
         '%.1fGW' % BR.implied_gw(tot, _v(_X, 'capex_per_gw')), '모델이 낸 값'],
        ['엑셀의 칩 수로', '가속기 %g백만 개' % _v(_SH, 'accel_units'),
         '%.2fkW/칩' % _KW_PER_GPU,
         '%.1fGW' % BR.gw_from_chips(_v(_SH, 'accel_units'), _KW_PER_GPU),
         '모델이 낸 값'],
    ]


def bridge_chip_table():
    """칩 한 개 값이 두 배 갈리는 자리."""
    per_gpu, _it = _it_per_mw()
    asp = BR.blended_asp(_v(_SH, 'accel_capex'), _v(_SH, 'accel_units'))
    head = ['칩 한 개 값', '값', '무엇을 담나', '성격']
    return head, [
        ['엑셀의 블렌드', '$%.1f천' % asp,
         '가속기 자본지출 $%g십억을 %g백만 개로 나눈 값'
         % (_v(_SH, 'accel_capex'), _v(_SH, 'accel_units')), '프레임 값'],
        ['엑셀의 블랙웰', '$%g천' % _v(_SH, 'asp_blackwell'), '랙 시스템가를 GPU 수로 나눔',
         '프레임 값'],
        ['엑셀의 구글 TPU', '$%g천' % _v(_SH, 'asp_tpu'), '같은 방식', '프레임 값'],
        ['엑셀의 AWS 트레이니엄', '$%g천' % _v(_SH, 'asp_trainium'), '같은 방식', '프레임 값'],
        ['우리 B200', '$%.1f천' % (per_gpu / 1000),
         '서버 값에 망·저장·소프트웨어까지', '원문 표 그림'],
        ['배수', '%.1f배' % (per_gpu / (asp * 1000)), '우리 값이 블렌드보다 이만큼 크다',
         '모델이 낸 값'],
    ]


def bridge_hbm_table():
    """메가와트에 실리는 HBM."""
    _per_gpu, it = _it_per_mw()
    chips = BR.gpus_per_mw(_KW_PER_GPU)
    gb = _v(_SH, 'hbm_per_gb')
    head = ['칩', '칩당 HBM', '메가와트당 용량', '메가와트당 값', 'IT 자본에서 차지하는 몫']
    body = []
    for label, key in (('블랙웰 블렌드', 'hbm_blackwell_gb'), ('루빈', 'hbm_rubin_gb'),
                       ('구글 TPU', 'hbm_tpu_gb')):
        v = _v(_SH, key)
        cost = BR.hbm_cost_per_mw(v, chips, gb)
        body.append([label, '%gGB' % v, '%.1fTB' % BR.hbm_per_mw(v, chips),
                     '$%.2f백만' % cost, '%.0f%%' % (cost / it * 100)])
    return head, body


def bridge_scn_table():
    """케이스 셋의 자본지출과 그것을 우리 단가로 나눈 용량."""
    head = ['케이스', '2026E', '2028E', '2030E', '5년 누적', '누적을 우리 단가로']
    body = []
    for k in ('capex_bear', 'capex_base', 'capex_bull'):
        r = _SC['rows'][k]
        vals = r[1:6]
        cum = BR.cumulative(vals)
        body.append([r[0], '$%g십억' % vals[0], '$%g십억' % vals[2],
                     '$%g십억' % vals[4], '$%.1f십억' % cum,
                     '%.0fGW' % BR.implied_gw(cum, _v(_X, 'capex_per_gw'))])
    for k, name in (('gap_bear', 'Bear 추가 조달'), ('gap_base', 'Base 추가 조달'),
                    ('gap_bull', 'Bull 추가 조달')):
        r = _SC['rows'][k]
        body.append([r[0], '$%g십억' % r[1], '$%g십억' % r[3], '$%g십억' % r[5],
                     '$%.1f십억' % BR.cumulative(r[1:6]), '—'])
    return head, body


def bridge_lever_table():
    """시나리오를 흔드는 레버 일곱과, 우리 원문이 그 자리를 받쳐 주나."""
    back = {
        '자본지출 증감률 조정(2027년 이후)': '없다 — 우리 원문에 연도별 성장률이 없다',
        'AI 가속기 비중 조정': '간접 — 서버 몫 53~69%가 우리 단가에서 나온다',
        'HBM 기가바이트당 단가 배수': '없다 — HBM 값은 프레임 재료에만 있다',
        '칩당 HBM 용량 배수': '없다 — 칩 세대 로드맵은 이 층 재료 밖이다',
        '가속기 평균판매가격 배수': '있다 — 우리 칩당 자본 $47,413 이 이 칸의 값이다',
        '빅4 글로벌 비중 조정': '없다',
        '삼성 점유율 조정(SK하이닉스에서 이전)': '없다',
    }
    head = ['레버', 'Bear', 'Base', 'Bull', '단위', '우리 원문이 받쳐 주나']
    body = []
    for v in _LV['rows'].values():
        name, bear, base, bull, unit = v[0], v[1], v[2], v[3], v[4]
        body.append([name, '%g' % bear, '%g' % base, '%g' % bull, unit,
                     back.get(name, '없다')])
    return head, body


TABLES = {
    'LEGOCOST': ('발표된 8퍼센트를 다시 낸다', lego_cost_table),
    'LEGOLAB': ('그 차이 가운데 인건비는 얼마인가', lego_labor_table),
    'LEGOSCH': ('공법마다 걸리는 기간', lego_sched_table),
    'LEGOVEND': ('총원가는 주는데 한 벤더의 몫은 는다', lego_vendor_table),
    'GRDLAYER': ('층마다 자본이 매출을 얼마나 먹나', ground_layer_table),
    'GRDPWR': ('같은 글에 든 전기 단가 넷', ground_power_table),
    'GRDEARLY': ('여섯 달 일찍 켜는 값이 전제하는 마진', ground_early_table),
    'TRSPLIT': ('바닥값 위 초과분을 나누는 1년차 계산', trinity_split_table),
    'TRGPU': ('공시 총액에서 바닥값과 장수를 되짚는다', trinity_gpu_table),
    'TRDEBT': ('금리 차가 이익률을 깎는 폭에서 부채를 푼다', trinity_debt_table),
    'SXPAY': ('파는 값마다 회수가 몇 해인가', spacex_payback_table),
    'SXARR': ('발표된 매출 목표가 전제하는 값', spacex_arr_table),
    'SXDEAL': ('묶인 계약은 지금 임대가로 몇 해치인가', spacex_deal_table),
    'BRFRAME': ('받은 엑셀이 낸 2026년 값', bridge_frame_table),
    'BRUNIT': ('그 틀의 빈칸에 우리 원문이 넣는 값', bridge_unit_table),
    'BRGW': ('같은 해를 네 자로 재면', bridge_gw_table),
    'BRCHIP': ('칩 한 개 값이 두 배 갈린다', bridge_chip_table),
    'BRHBM': ('메가와트에 실리는 HBM', bridge_hbm_table),
    'BRSCN': ('케이스 셋을 우리 단가로 재면', bridge_scn_table),
    'BRLEVER': ('시나리오를 흔드는 레버 일곱', bridge_lever_table),
}


def source_lines():
    """이 층 넷이 쓴 원문의 주소."""
    out = []
    for key in ('lego', 'ground', 'trinity', 'spacex'):
        s = RAW['sources'][key]
        out.append('%s, %s, %s 발행 — <a href="%s">%s</a>'
                   % (s['title'], s['publisher'], s['published'], s['url'], s['url']))
    return out
