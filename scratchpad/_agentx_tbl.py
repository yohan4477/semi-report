# -*- coding: utf-8 -*-
"""AgentX 프런티어 층의 표. 값은 전부 insights/models/check_agentx.py 와 같은 함수에서 낸다.

검사기의 함수(permw·own·rent·gw)를 그대로 불러 쓴다 — 표와 검사기가 다른 길로 셈하면
한쪽만 고쳐지는 사고가 난다. 원자료는 insights/models/raw/inferencex_dsv4_agentx.json.
"""
import os
import sys

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'insights', 'models')
if _MODELS not in sys.path:
    sys.path.insert(0, _MODELS)
import agentx_frontier as AX                                     # noqa: E402
import check_agentx as CA                                        # noqa: E402

_ORDER = ('vr', 'gb300_sgl', 'gb300_trt', 'b200', 'b300', 'h200', 'mi355x')


def _pub(k):
    return CA.pub(k)


def _diff(got, want):
    d = (got / want - 1) * 100
    return '일치' if abs(d) <= 1 else '%+.1f%%' % d


def hw_table():
    """칩 상수 — 앱 코드에서 옮긴 값."""
    head = ['설정', '칩당 전력', '사서 운영', '3년 약정 임대', '측정 점', '속도 범위(P90 TPS)']
    body = []
    for k in _ORDER:
        h = CA.S[k][0]
        rows = [e for e in CA.RAW['rows'] if e['hardware'] == h
                and e['framework'] == CA.SER['rows'][k][1]]
        xs = [AX._x(e) for e in CA.S[k][1]]
        body.append([CA.label(k), '%.2fkW' % CA.hw(h, 'power_kw'),
                     '$%.2f/시간' % CA.hw(h, 'costh'), '$%.2f/시간' % CA.hw(h, 'costr'),
                     '%d점 중 프런티어 %d' % (len(rows), len(xs)),
                     '%.0f~%.0f' % (min(xs), max(xs))])
    return head, body


def mw_table():
    """100 TPS 에서 1메가와트당 토큰 — 일곱 설정 전부."""
    head = ['설정', 'GPU 한 장 처리량', '1MW 에 드는 장수', '모델', '발표', '차이']
    body = []
    for k in _ORDER:
        h = CA.S[k][0]
        t = CA.tput(k, 100)
        got = CA.permw(k, 100)
        want = _pub('permw100_' + k)
        body.append([CA.label(k), '%s tok/s' % format(int(round(t)), ','),
                     '%.0f장' % (1000 / CA.hw(h, 'power_kw')),
                     '%.2f백만' % got, '%g백만' % want, _diff(got, want)])
    return head, body


def gap_table():
    """어긋난 일곱 칸."""
    head = ['원문 값', '줄', '모델', '발표', '차이', '왜 갈리나']
    r = lambda key: CA.line(key)
    sgl = lambda s: CA.permw('vr', s) / CA.permw('gb300_sgl', s)
    rows = [
        ['150 TPS 루빈 ÷ GB300 SGLang (메가와트당)', r('x150_vr_sgl'), sgl(150),
         _pub('x150_vr_sgl'), '곡선은 스냅숏 넷에서 같다 — 못 풀었다'],
        ['170 TPS 같은 비교', r('x170_vr_sgl_mw'), sgl(170), _pub('x170_vr_sgl_mw'),
         '위와 같은 곡선'],
        ['200 TPS 같은 비교', r('x200_vr_sgl'), sgl(200), _pub('x200_vr_sgl'), '위와 같은 곡선'],
        ['170 TPS 루빈 ÷ GB300 TRT (사서 운영, 달러당)', r('x170_vr_trt_own'),
         CA.own('vr', 'gb300_trt', 170), _pub('x170_vr_trt_own'),
         '곡선 끝 바로 앞 — 171.4 TPS 에서 67'],
        ['80 TPS 루빈 ÷ B300 (사서 운영)', r('own80_vr_b300'), CA.own('vr', 'b300', 80),
         _pub('own80_vr_b300'), '원문이 엔진을 안 적었다 · vLLM 기준'],
        ['80 TPS 임대 토큰 더 (%)', r('rent80_more_pct'),
         (CA.rent('vr', 'gb300_sgl', 80) - 1) * 100, _pub('rent80_more_pct'),
         '엔진 미기재 · SGLang 기준, TRT 면 %.0f' % ((CA.rent('vr', 'gb300_trt', 80) - 1) * 100)],
        ['임대 최대 배수', r('rent_hi_max'),
         CA.best(lambda s: CA.rent('vr', 'gb300_sgl', s), 75, 276.2)[0], _pub('rent_hi_max'),
         'SGLang 대비 최대 6, TRT 대비 최대 %.0f — 16 은 안 나온다'
         % CA.best(lambda s: CA.rent('vr', 'gb300_trt', s), 75, 171.5)[0]],
    ]
    return head, [[a, 'L%d' % b, '%.3g' % c, '%g' % d, '%+.1f%%' % ((c / d - 1) * 100), e]
                  for a, b, c, d, e in rows]


def gw_table():
    """75 TPS · 가동률 60% 에서 기가와트당 연 매출과 그 중간값."""
    head = ['무엇', '루빈', 'GB300 SGLang', 'GB300 TRT', '성격']
    g = [CA.gw(k, 75) for k in ('vr', 'gb300_sgl', 'gb300_trt')]
    return head, [
        ['GPU 한 장 처리량 (tok/s)'] + ['%s' % format(int(round(x['tput'])), ',') for x in g]
        + ['모델이 낸 값 — 프런티어 보간'],
        ['입력 토큰 비중'] + ['%.2f%%' % (x['share'] * 100) for x in g]
        + ['모델이 낸 값 — 행의 입력·출력 처리량'],
        ['캐시 적중'] + ['%.1f%%' % (x['hit'] * 100) for x in g]
        + ['모델이 낸 값 — 루빈·SGLang 은 서버 측정, TRT 는 트레이스 이론값'],
        ['섞은 단가 (백만 토큰당)'] + ['$%.3f' % x['price'] for x in g]
        + ['모델이 낸 값 — 입력 $1.32 · 캐시 $0.044 · 출력 $3.96'],
        ['기가와트당 연 원가'] + ['$%.2f십억' % (x['tco'] / 1e9) for x in g]
        + ['모델이 낸 값 — 칩당 시간 원가 × 연 GPU 시간'],
        ['기가와트당 연 매출'] + ['$%.1f십억' % (x['revenue'] / 1e9) for x in g]
        + ['모델이 낸 값'],
        ['원문 매출', '$%g십억' % _pub('rev_vr'), '$%g십억' % _pub('rev_gb300_sgl'),
         '$%g십억' % _pub('fleet_gwyr_trt'), '원문 값 (L142·L152)'],
        ['기가와트당 연 이익'] + ['$%.1f십억' % (x['profit'] / 1e9) for x in g]
        + ['모델이 낸 값'],
        ['원문 이익', '$%g십억' % _pub('profit_vr'), '$%g십억' % _pub('profit_gb300_sgl'),
         '—', '원문 값 (L142)'],
    ]


TABLES = {
    'AXHW': ('칩 상수와 측정 곡선 — 앱 코드와 API 스냅숏', hw_table),
    'AXMW': ('100 TPS 에서 1메가와트당 토큰 — 일곱 설정', mw_table),
    'AXGW': ('75 TPS 에서 기가와트당 연 매출 — 캐시 적중이 단가를 정한다', gw_table),
    'AXGAP': ('어긋난 일곱 칸', gap_table),
}
