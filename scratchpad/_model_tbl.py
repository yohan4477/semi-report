# -*- coding: utf-8 -*-
"""보고서 「모델 총정리」 층의 표 다섯. 원문 계산기의 칸 배치를 그대로 세운다.

값을 손으로 옮겨 적지 않는다. `insights/models/` 의 모델이 계산해서 내고,
발표치는 그림에서 읽은 것을 상수로 두어 나란히 놓는다. 그래서 모델을 고치면
표가 같이 바뀌고, 어긋난 칸이 저절로 드러난다.

`rows_text()` 는 같은 값을 글자로 낸다 — scratchpad/gen_model_facts.py 가 그것을
사실표에 떨어뜨려 check_report 의 대조 재료로 쓴다. 표와 사실표가 한 함수에서
나오므로 갈릴 수 없다.
"""
import os
import sys

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'insights', 'models')
if _MODELS not in sys.path:
    sys.path.insert(0, _MODELS)

from gpu_cluster_tco import goodput_breakdown                    # noqa: E402
from inference_tco import Capex, Opex, Sku                        # noqa: E402
import check_gpu_tco as G                                         # noqa: E402
import check_inference_tco as I                                   # noqa: E402


def _m(v, unit='$'):
    """돈은 자리를 끊는다. 단가는 센트까지 봐야 하므로 천 달러 미만은 소수 둘째.

    원문 표가 kW·월 단가를 $198.6 으로 적었다. 반올림해 $199 로 내면 전기와
    코로케이션의 합이 안 맞아 보인다.
    """
    if unit == '$':
        if abs(v) < 1000:
            return '$%.2f' % v
        return '$%s' % format(int(round(v)), ',')
    if unit == '%':
        return '%.2f%%' % v
    if unit == 'x':
        return '%.2f배' % v
    return format(v, ',')


# ── 표 1. GPU 클러스터 TCO 계산기 (그림 016) ────────────────────────────
# 원문 표의 세로 칸 순서를 그대로 둔다 — 항목을 다시 묶으면 대조가 안 된다.
_TCO_ROWS = [
    ('GPU', 'GB300 NVL72 5,184장 · $4/GPU-시간', lambda t: t.gpu_cost()),
    ('저장', '핫 500TiB · 콜드 10PiB', lambda t: t.storage_cost()),
    ('네트워크', '이그레스·NAT·전송', lambda t: t.network_cost()),
    ('컨트롤 플레인', 'VM 3대', lambda t: t.ctrl_plane_cost()),
    ('지원', '% 할증', lambda t: t.support_cost()),
    ('굿풋 손실', '% 할증', lambda t: t.goodput_cost()),
    ('설치 (일시금)', '엔지니어 인월 + POC', lambda t: t.setup_cost_onetime()),
    ('설치 (36개월 상각)', '', lambda t: t.setup_cost_onetime() / 36),
    ('디버깅', '엔지니어 인월 + 클러스터 시간', lambda t: t.debugging_cost()),
]


def tco_table():
    """반환: (머리, 본문 행들, 안 맞는 칸 수). 값은 전부 모델이 낸 것이다."""
    head = ['항목', '수량·단위'] + [n for n, _t, _w in G.TIERS]
    body = []
    for label, unit, fn in _TCO_ROWS:
        body.append([label, unit] + [_m(fn(t)) for _n, t, _w in G.TIERS])
    body.append(['월 합계 (상각 포함)', '', ]
                + [_m(t.monthly_amortized()) for _n, t, _w in G.TIERS])
    body.append(['36개월 합계', '']
                + [_m(t.contract_total()) for _n, t, _w in G.TIERS])
    base = G.TIERS[0][1].contract_total()
    body.append(['Gold 대비', '']
                + [_m(t.contract_total() / base, 'x') for _n, t, _w in G.TIERS])
    return head, body


# 어긋난 줄마다 어느 항을 빼야 발표치가 나오나. 항을 하나씩·둘씩·셋씩 꺼서
# 전부 시험한 결과이고 판단이 아니다 — insights/models/ 의 대조로 나온다
_MISSING = {
    '대규모 학습 / Silver': '고장 인지 시간을 빼야',
    '소규모 학습 / Silver': '체크포인트 손실을 빼야',
    '소규모 학습 / Gold': '인지 시간이나 수리 시간을 빼야 (둘이 같은 값이라 안 갈림)',
}


# ── 표 2. 굿풋 계산기 세 시나리오 (그림 019·022·025) ────────────────────
# 여기만 발표치와 모델값을 나란히 둔다 — 이 표가 어긋나는 자리이기 때문이다.
def goodput_table():
    head = ['시나리오', '클러스터 / 작업 / 반경', '복원 방식',
            '월 중단', '발표 손실', '수식대로', '차이', '발표치가 나오려면']
    body = []
    for name, g, want in G.SCENARIOS:
        mode = {'tolerant': '고장 견딤', 'chkpt_hot': '뜨거운 예비',
                'chkpt_cold': '차가운 예비'}[g.mode]
        got = goodput_breakdown(g)
        d = got['total_pct'] - want['total_pct']
        body.append([
            name,
            '%s / %s / %s' % (format(g.cluster_size, ','), format(g.j_size, ','),
                              g.b_radius),
            mode,
            '%.1f회' % got['failures_per_month'],
            _m(want['total_pct'], '%'),
            _m(got['total_pct'], '%'),
            '일치' if abs(d) < 0.01 else '%+.2f%%p' % d,
            _MISSING.get(name, ''),
        ])
    return head, body


# ── 표 3. 굿풋 어긋남이 3년 값을 얼마나 바꾸나 ──────────────────────────
def impact_table():
    head = ['티어', '발표 굿풋', '수식대로 굿풋', '36개월 발표', '36개월 수식', '차이']
    model_pct = {n.split(' / ')[1]: goodput_breakdown(g)['total_pct']
                 for n, g, _w in G.SCENARIOS if n.startswith('대규모 학습')}
    key = {'Gold-tier': 'Gold', 'Hyperscaler': 'Hyperscaler', 'Silver-tier': 'Silver'}
    body = []
    for name, t, _want in G.TIERS:
        pub_pct = t.goodput_pct
        t.goodput_pct = model_pct[key[name]]
        modeled = t.contract_total()
        t.goodput_pct = pub_pct
        pub_total = _want['total36']
        body.append([name, _m(pub_pct, '%'), _m(model_pct[key[name]], '%'),
                     _m(pub_total), _m(modeled), _m(modeled - pub_total)])
    return head, body


# ── 표 4·5. 추론 원가 자본지출과 운영비 (그림 049·050) ──────────────────
# WACC 는 역산한 13.25% 를 쓴다. 표에 찍힌 13.3% 는 소수 한 자리 표시값이다.
def _refit():
    return [Sku(s.name, Capex(s.capex.server_cost, s.capex.other_cluster_cost,
                              wacc=0.1325), s.opex) for s in I.SKUS]


_CAPEX_ROWS = [
    ('서버 값', lambda s: s.capex.server_cost),
    ('서비스·망·저장·소프트웨어', lambda s: s.capex.other_cluster_cost),
    ('서버당 선불 자본지출', lambda s: s.capex.upfront_per_server()),
    ('논리 GPU당 선불', lambda s: s.capex.upfront_per_gpu()),
    ('월 자본비 (WACC 13.25% · 4년)', lambda s: s.capex.monthly_per_server()),
]
_OPEX_ROWS = [
    ('전기 kW·월 (가동률 80% · PUE 1.35)', lambda s: s.opex.electricity_per_kw_month()),
    ('코로케이션 kW·월', lambda s: s.opex.colocation_kw_month),
    ('호스팅 kW·월 합계', lambda s: s.opex.hosting_per_kw_month()),
    ('월 호스팅 (서버당)', lambda s: s.opex.hosting_per_server_month()),
    ('월 운영비 (서버당)', lambda s: s.opex.monthly_per_server()),
    ('월 운영비 (GPU당)', lambda s: s.opex.monthly_per_gpu()),
]


def _sku_table(rows, tail):
    skus = _refit()
    head = ['항목'] + [s.name for s in skus]
    body = [[label] + [_m(fn(s)) for s in skus] for label, fn in rows]
    for label, fn, unit in tail:
        body.append([label] + [_m(fn(s), unit) for s in skus])
    return head, body


def capex_table():
    return _sku_table(_CAPEX_ROWS,
                      [('GPU 시간당 자본비', lambda s: s.capex.hourly_per_gpu(), '$')])


def opex_table():
    return _sku_table(_OPEX_ROWS,
                      [('GPU 시간당 운영비', lambda s: s.opex.hourly_per_gpu(), '$')])


def total_table():
    skus = _refit()
    head = ['항목'] + [s.name for s in skus]
    body = [
        ['GPU 시간당 자본비'] + [_m(s.capex.hourly_per_gpu()) for s in skus],
        ['GPU 시간당 운영비'] + [_m(s.opex.hourly_per_gpu()) for s in skus],
        ['GPU 시간당 합계'] + [_m(s.tco_hourly_per_gpu()) for s in skus],
        ['자본비 비중'] + [_m(s.capital_share(), '%') for s in skus],
        ['H200 대비 처리량 문턱']
        + [_m(s.tco_hourly_per_gpu() / skus[4].tco_hourly_per_gpu(), 'x')
           for s in skus],
    ]
    return head, body


def wacc_table():
    """발표된 월 자본비에서 역산한 WACC. 표에 찍힌 13.3% 는 소수 한 자리 표시값이다."""
    from inference_tco import implied_wacc, levelized_monthly
    head = ['SKU', '서버당 선불', '발표 월 자본비', '13.3%로 계산', '차이', '역산 WACC']
    body = []
    for sku in I.SKUS:
        up = sku.capex.upfront_per_server()
        want = I.PUBLISHED[sku.name][2]
        got = levelized_monthly(up, 0.133, 4)
        r = implied_wacc(up, want, 4)
        body.append([sku.name, _m(up), _m(want), _m(got),
                     '%+.4f%%' % ((want / got - 1) * 100), '%.4f%%' % (r * 100)])
    return head, body


# 원문이 글로 밝힌 손익분기 임대료(AMD영문 L298·L302·L306)와 H200 시세 2.5달러.
# 비율은 그 둘로 나온 값이라 손으로 적지 않는다
_WORKLOAD = [('번역·대화 1k/1k', 1.9, 1.9), ('추론형 1k/4k', 2.1, 2.4),
             ('요약 4k/1k', 2.1, 2.4)]


def verdict_table():
    """작업 성격마다 사서 쓸 때의 답. 문턱은 두 SKU 의 시간당 원가 비다."""
    from inference_tco import implied_throughput_ratio
    by = {s.name: s for s in _refit()}
    thr = by['MI300X'].tco_hourly_per_gpu() / by['H200 SXM'].tco_hourly_per_gpu()
    head = ['작업 성격', '손익분기 임대료', 'MI300X 실측 처리량', '사서 쓸 때 문턱', '결론']
    body = []
    for name, lo, hi in _WORKLOAD:
        r_lo = implied_throughput_ratio(I.H200_RENTAL, lo)
        r_hi = implied_throughput_ratio(I.H200_RENTAL, hi)
        verdict = ('사서 쓰면 MI300X가 싸다' if r_lo > thr
                   else ('빌려도 사도 H200이 싸다' if r_hi < thr else '문턱을 걸친다'))
        body.append([
            name,
            '$%.2f' % lo if lo == hi else '$%.2f~$%.2f' % (lo, hi),
            '%.2f' % r_lo if lo == hi else '%.2f~%.2f' % (r_lo, r_hi),
            '%.2f' % thr, verdict])
    return head, body


TABLES = {
    'TCO': ('GPU 클러스터 TCO 계산기 — 월 비용 (그림 016 재현)', tco_table),
    'GOOD': ('굿풋 계산기 세 시나리오 (그림 019·022·025 재현)', goodput_table),
    'IMPACT': ('굿풋 어긋남이 3년 값에 미치는 폭', impact_table),
    'WACC': ('표에 찍힌 13.3%에서 역산한 실제 할인율', wacc_table),
    'VERDICT': ('작업 성격마다 갈리는 소유의 답', verdict_table),
    'CAPEX': ('추론 원가 — 자본지출 (그림 049 재현)', capex_table),
    'OPEX': ('추론 원가 — 운영비 (그림 050 재현)', opex_table),
    'TOTAL': ('추론 원가 — GPU 시간당 합계 (그림 016 뒷장 재현)', total_table),
}


def rows_text():
    """같은 값을 글자로. 사실표가 이것을 받아 check_report 의 대조 재료가 된다."""
    out = []
    for key, (title, fn) in TABLES.items():
        head, body = fn()
        out.append('### 표 %s — %s' % (key, title))
        out.append(' · '.join(head))
        for r in body:
            out.append(' · '.join(r))
        out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(rows_text())
