# -*- coding: utf-8 -*-
"""보고서 「모델 총정리」 층의 표 다섯. 원문 계산기의 칸 배치를 그대로 세운다.

값을 손으로 옮겨 적지 않는다. `insights/models/` 의 모델이 계산해서 내고,
발표치는 그림에서 읽은 것을 상수로 두어 나란히 놓는다. 그래서 모델을 고치면
표가 같이 바뀌고, 어긋난 칸이 저절로 드러난다.

`rows_text()` 는 같은 값을 글자로 낸다 — scratchpad/gen_model_facts.py 가 그것을
사실표에 떨어뜨려 check_report 의 대조 재료로 쓴다. 표와 사실표가 한 함수에서
나오므로 갈릴 수 없다.
"""
import json
import os
import sys
import io

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'insights', 'models')
if _MODELS not in sys.path:
    sys.path.insert(0, _MODELS)

from gpu_cluster_tco import goodput_breakdown                    # noqa: E402
from inference_tco import Capex, Opex, Sku                        # noqa: E402
import check_gpu_tco as G                                         # noqa: E402
import check_inference_tco as I                                   # noqa: E402


RAW = json.loads(io.open(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'insights', 'models', 'raw', 'tables.json'), encoding='utf-8').read())


def _count(t):
    """표 하나에 든 값의 개수. 열 목록이 있으면 행마다 열 수만큼 센다."""
    n = 0
    for v in t.get('rows', {}).values():
        n += len(v) if isinstance(v, (list, tuple)) else 1
    n += len(t.get('shared_inputs', {}))
    return n


def raw_table():
    """이 층이 쓴 원자료. 그림에서 읽은 값이 어디서 왔고 몇 개인지, 못 읽은 칸이 몇인지."""
    head = ['원자료', '출처 글', '펴낸 날', '그림', '이미지 파일', '읽은 칸',
            '가려진 줄', '읽은 날']
    body = []
    for t in RAW['tables']:
        src = RAW['sources'][t['source']]
        img = (t['image'] or '').rsplit('/', 1)[-1] or '—'
        body.append([t['title'], src['title'], src['published'], t['figure'], img,
                     '%d개' % _count(t),
                     '%d줄' % len(t['redacted']) if t['redacted'] else '없음',
                     t['read_on']])
    for m in RAW['not_captured']:
        body.append([m['what'], m['where'], '—', '—', '—', '못 읽음', '—', '—'])
    return head, body


def source_lines():
    """원자료가 온 글의 주소. 표 아래에 한 줄씩 낸다."""
    out = []
    for key, s in RAW['sources'].items():
        ko = (' · 한국어 변환본 <code>%s</code>' % s['korean'].rsplit('/', 1)[-1]
              if s.get('korean') else '')
        out.append('%s, %s, %s 발행 — <a href="%s">%s</a>%s'
                   % (s['title'], s['publisher'], s['published'], s['url'], s['url'], ko))
    return out


def ext_table():
    """가려진 칸을 박거나 현황을 갱신할 때 가져올 자료. 뉴스레터 밖의 것이다."""
    head = ['무엇을 박나', '자료', '갈래', '어디', '지금 상태']
    body = []
    for e in RAW['external_sources']:
        body.append([e['pins'], e['source'], e['kind'],
                     e['where'], e['status']])
    return head, body


def ext_lines():
    """자료마다 어떻게 쓰는지와 주소. 표에 넣으면 열이 넘쳐 아래로 내린다."""
    out = []
    for e in RAW['external_sources']:
        link = (' — <a href="%s">%s</a>' % (e['url'], e['url'])) if e.get('url') else ''
        out.append('<b>%s</b> · %s%s' % (e['pins'], e['how'], link))
    return out


# ── 토러스 모델 표 넷 ──────────────────────────────────────────────────
_TPU = json.loads(io.open(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'insights', 'models', 'raw', 'tpuv7.json'), encoding='utf-8').read())

_TDIMS = (4, 4, 4)
_TSPOT = [('꼭짓점', 'Corner'), ('모서리', 'Edge'), ('면', 'Face'), ('안쪽', 'Interior')]
_TKIND = [('구리 케이블', 'copper', 'Copper Cables'),
          ('기판 배선', 'pcb', 'PCB Traces'),
          ('광 트랜시버', 'optical', 'Optical Transceivers')]


def _torus():
    import sys as _s
    _s.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'insights', 'models'))
    import torus_attach as ta
    return ta


def _pub_torus():
    """그림 034 의 발표치를 (자리, 갈래) → (칩당, 랙 합계) 로 편다."""
    t = _TPU['tables'][0]
    per, tot = {}, {}
    for row, vals in t['rows'].items():
        a, b = float(vals[0]), float(vals[1])
        if row.startswith('Total'):
            tot[row.split('—')[1].strip()] = (a, b)
        else:
            head, kind = [x.strip() for x in row.split('—')]
            per[(head.split()[1], kind)] = (a, b)
    return per, tot


def torus_pos_table():
    """자리마다 칩 수와 칩 한 장당 연결. 발표치를 나란히 둔다."""
    ta = _torus()
    g = {v['name']: v for v in ta.classify(_TDIMS).values()}
    pub, _ = _pub_torus()
    head = ['자리', '끝에 걸린 축', '칩'] + [k for k, _a, _b in _TKIND] + ['합']
    body = []
    for ko, en in _TSPOT:
        v = g[ko]
        cells = []
        for _ko, key, en_kind in _TKIND:
            got = v[key]
            want = pub.get((en, en_kind))
            cells.append('%d' % got if want and abs(got - want[0]) < 1e-9
                         else '%d (발표 %g)' % (got, want[0]) if want else '%d' % got)
        body.append([ko, '%d' % v['optical'], '%d' % v['chips']] + cells
                    + ['%d' % (v['copper'] + v['pcb'] + v['optical'])])
    return head, body


def torus_rack_table():
    """랙 합계. 케이블은 반으로 나누고 트랜시버는 안 나눈다."""
    ta = _torus()
    r = ta.rack(_TDIMS)
    _, pub = _pub_torus()
    head = ['갈래', '연결 끝의 수', '세는 법', '랙 합계', '발표 합계', '칩당', '발표 칩당']
    rows = [('구리 케이블', 'Copper Cable', r['copper_cables'], r['copper_per_chip'],
             '두 칩을 잇는 한 물건 — 반으로 나눈다'),
            ('기판 배선', 'PCB', r['pcb_traces'], r['pcb_per_chip'],
             '두 칩을 잇는 한 물건 — 반으로 나눈다'),
            ('광 트랜시버', 'Optical Transceivers', r['transceivers'],
             r['transceivers_per_chip'], '연결 양끝에 하나씩 — 안 나눈다')]
    body = []
    for ko, en, tot, per, how in rows:
        w = pub.get(en)
        ends = tot * 2 if '반으로' in how else tot
        body.append([ko, '%g' % ends, how, '%g' % tot,
                     '%g' % w[1] if w else '—', '%.2f' % per,
                     '%g' % w[0] if w else '—'])
    return head, body


def torus_scale_table():
    """격자를 키우면 부착률이 어떻게 움직이나. 원문에 없는 값이다."""
    ta = _torus()
    head = ['격자', '칩', '끝에 걸린 칩', '광 트랜시버', '칩당 트랜시버', '구리 케이블']
    body = []
    for dims in [(2, 2, 2), (4, 4, 4), (4, 4, 8), (8, 8, 8), (16, 16, 16)]:
        x = ta.rack(dims)
        edge = sum(v['chips'] for k, v in ta.classify(dims).items() if k)
        body.append(['×'.join(map(str, dims)), format(x['chips'], ','),
                     '%s (%.0f%%)' % (format(edge, ','), edge / x['chips'] * 100),
                     format(int(x['transceivers']), ','),
                     '%.2f' % x['transceivers_per_chip'],
                     format(int(x['copper_cables']), ',')])
    return head, body


def torus_raw_table():
    """이 글이 쓴 원자료. 표 하나와 표 아닌 것 열하나."""
    src = _TPU['source']
    head = ['원자료', '출처 글', '펴낸 날', '그림', '읽은 칸', '가려진 줄', '읽은 날']
    body = []
    for t in _TPU['tables']:
        n = sum(len(v) if isinstance(v, list) else 1 for v in t['rows'].values())
        body.append([t['title'], src['title'], src['published'], t['figure'],
                     '%d개' % n,
                     '%d줄' % len(t.get('redacted', [])) if t.get('redacted') else '없음',
                     t.get('read_on', src.get('read_on', ''))])
    body.append(['표 후보였으나 표가 아니었던 그림',
                 src['title'], src['published'], '11장', '—', '—',
                 src.get('read_on', '')])
    return head, body


def torus_source_lines():
    src = _TPU['source']
    ko = (' · 한국어 변환본 <code>%s</code>' % src['korean'].rsplit('/', 1)[-1]
          if src.get('korean') else '')
    return ['%s, %s, %s 발행 — <a href="%s">%s</a>%s'
            % (src['title'], src['publisher'], src['published'], src['url'],
               src['url'], ko)]


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


# 원문이 검은 막대로 지운 세 줄. 값 자리에 None 을 두면 표가 어두운 칸으로 칠한다 —
# 「모르는 값」과 「0」은 다르므로 빈칸으로 두면 안 된다
_REDACTED = ['GPU 원가 (GPU당)', 'GPU 원가 + 보증 (서버당)', '기타 서버 비용']

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


def _sku_table(rows, tail, redacted=()):
    skus = _refit()
    head = ['항목'] + [s.name for s in skus]
    body = [[label] + [None] * len(skus) for label in redacted]
    body += [[label] + [_m(fn(s)) for s in skus] for label, fn in rows]
    for label, fn, unit in tail:
        body.append([label] + [_m(fn(s), unit) for s in skus])
    return head, body


def capex_table():
    return _sku_table(_CAPEX_ROWS,
                      [('GPU 시간당 자본비', lambda s: s.capex.hourly_per_gpu(), '$')],
                      redacted=_REDACTED)


# 가려진 줄을 어디까지 좁힐 수 있나. 「기타 서버 비용」 하나를 모르면 절대값이 안
# 나오지만, 서버 값의 차이는 원문 값에서 바로 나온다 — 기타가 SKU 마다 같다고 보면
# 그 차이가 곧 GPU 원가의 차이다. 가정 값 셋은 우리가 고른 것이고 원문에 없다
_OTHER_ASSUMED = (20_000, 30_000, 40_000)


def gap_table():
    skus = _refit()
    base = skus[0].capex.server_cost
    head = ['SKU', '서버 값', 'MI300X 대비 차이'] + [
        'GPU 원가/장 (기타 %s 가정)' % _m(v) for v in _OTHER_ASSUMED]
    body = []
    for s in skus:
        sc = s.capex.server_cost
        row = [s.name, _m(sc), _m(sc - base)]
        row += [_m((sc - other) / 8) for other in _OTHER_ASSUMED]
        body.append(row)
    return head, body


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
    'RAW': ('이 층이 쓴 원자료와 그 출처', raw_table),
    'RAWT': ('이 글이 쓴 원자료와 그 출처', torus_raw_table),
    'TPOS': ('자리가 배선을 정한다 (그림 034 재현)', torus_pos_table),
    'TRACK': ('랙 64장 합계 — 무엇을 나누고 무엇을 안 나누나', torus_rack_table),
    'TSCALE': ('격자를 키우면 부착률이 어떻게 움직이나', torus_scale_table),
    'EXT': ('가려진 칸을 박으려면 어디서 가져와야 하나', ext_table),
    'TCO': ('GPU 클러스터 TCO 계산기 — 월 비용 (그림 016 재현)', tco_table),
    'GOOD': ('굿풋 계산기 세 시나리오 (그림 019·022·025 재현)', goodput_table),
    'IMPACT': ('굿풋 어긋남이 3년 값에 미치는 폭', impact_table),
    'WACC': ('표에 찍힌 13.3%에서 역산한 실제 할인율', wacc_table),
    'VERDICT': ('작업 성격마다 갈리는 소유의 답', verdict_table),
    'CAPEX': ('추론 원가 — 자본지출 (그림 049 재현)', capex_table),
    'GAP': ('가려진 줄을 어디까지 좁힐 수 있나', gap_table),
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
            out.append(' · '.join('가려짐' if c is None else c for c in r))
        out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(rows_text())
