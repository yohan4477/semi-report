# -*- coding: utf-8 -*-
"""빅테크 여섯을 같은 잣대로 재는 비교 계산.

알파벳 편(절 1~12)은 회사 하나를 깊게 판다. 이 모듈은 반대로 여섯을 **같은 산식**에
넣어 어디가 어떻게 다른지만 본다. 회사마다 3구간 가정을 새로 세우지 않는다 —
가정을 여섯 벌 만들면 그 가정 차이가 회사 차이로 둔갑한다.

대신 가정이 거의 안 드는 두 축만 쓴다.

  ① 구조    실적에서 바로 읽히는 값 — 매출·영업이익률·FCF마진·설비투자/감가상각
  ② 역산    시가총액을 정답으로 놓고 요구 성장률을 되돌린다

역산 기준을 둘로 둔다. **잉여현금흐름**은 손에 실제로 남는 현금이고, **NOPAT**은
설비투자를 빼기 전 영업 이익력이다. 둘의 차이가 곧 설비투자가 먹는 몫이라, 그
간격이 회사마다 얼마나 벌어지는지가 이 비교의 요점이다. 아마존은 잉여현금흐름이
음수라 첫 기준으로는 계산이 아예 안 선다 — 그것도 결과다.

세율은 **21%로 통일**한다. 회사마다 실제 납부세율을 쓰면 그 해의 납부 시차가 회사
차이로 읽힌다. 각자의 납부세율은 따로 낸다.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'insights'))
import dcf  # noqa: E402

B = 1e9
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TICKERS = ('GOOGL', 'MSFT', 'NVDA', 'AMZN', 'META', 'AAPL')
NAMES = {'GOOGL': '알파벳', 'MSFT': '마이크로소프트', 'NVDA': '엔비디아',
         'AMZN': '아마존', 'META': '메타', 'AAPL': '애플'}

MRP = 0.046          # 시장위험프리미엄. 여섯 공통
TAX = 0.21           # 미국 법인세 기본세율. 여섯 공통
G = 0.0275           # 영구성장률. 여섯 공통
YEARS = 10           # 명시적 기간


def _facts(t):
    return json.load(open(os.path.join(_root, 'insights/valuation/%s/facts.json' % t),
                          encoding='utf-8'))


def row(t):
    """회사 하나의 비교값. 값이 없으면 None 을 담고 표에서 빈칸으로 낸다."""
    d = _facts(t)
    tt, c = d['sec']['ttm'], d['sec']['concepts']

    def v(k):
        return tt[k]['val'] / B if k in tt else None

    rev, eb, ocf, cap, dna = v('revenue'), v('ebit'), v('ocf'), v('capex'), v('dna')
    fcf = (ocf - cap) if (ocf is not None and cap is not None) else None
    # 주식보상비용. 현금이 안 나가 영업현금흐름에 도로 더해져 있으므로 위의 잉여현금흐름
    # 안에 이미 들어 있다. 빼는 것이 옳은지는 판단이라 여기서 정하지 않고 값만 남긴다.
    sbc = v('sbc')
    fcf_sbc = (fcf - sbc) if (fcf is not None and sbc is not None) else None
    net_debt = ((tt.get('lt_debt', {}).get('val', 0) + tt.get('st_debt', {}).get('val', 0)
                 - tt.get('cash', {}).get('val', 0)
                 - tt.get('st_investments', {}).get('val', 0)) / B)
    beta = d['beta']['beta']
    rf = d['risk_free']['rate']
    ke = rf + beta * MRP
    mcap = d['market']['market_cap'] / B
    nopat = eb * (1 - TAX) if eb is not None else None

    # 각자의 실제 납부세율 — 통일 세율과 견주려고 함께 낸다
    cash_tr = None
    if 'cash_taxes_paid' in c and 'ebit' in c:
        yrs = sorted(set(c['cash_taxes_paid']) & set(c['ebit']))
        if yrs:
            y = yrs[-1]
            cash_tr = c['cash_taxes_paid'][y]['val'] / c['ebit'][y]['val']

    def req(base):
        """그 기준값이 시가총액을 정당화하려면 필요한 10년 복리 성장률."""
        if base is None or base <= 0:
            return None
        try:
            return dcf.implied_growth(base, ke, G, YEARS, mcap, net_debt)
        except Exception:
            return None

    return dict(t=t, name=NAMES[t], end=tt.get('revenue', {}).get('end', ''),
                rev=rev, ebit=eb, ebit_m=(eb / rev if (eb and rev) else None),
                fcf=fcf, fcf_m=(fcf / rev if (fcf is not None and rev) else None),
                capex=cap, dna=dna, cd=(cap / dna if (cap and dna) else None),
                nopat=nopat, beta=beta, ke=ke, mcap=mcap, net_cash=-net_debt,
                cash_tr=cash_tr, req_fcf=req(fcf), req_nopat=req(nopat),
                sbc=sbc, fcf_sbc=fcf_sbc, req_fcf_sbc=req(fcf_sbc),
                mult=(mcap / fcf if (fcf and fcf > 0) else None),
                mult_sbc=(mcap / fcf_sbc if (fcf_sbc and fcf_sbc > 0) else None),
                sbc_share=(sbc / fcf if (sbc is not None and fcf and fcf > 0) else None),
                **_levels(fcf, nopat, rev, req(fcf), req(nopat)))


def _levels(fcf, nopat, rev, rf_, rn_):
    """요구 성장률이 10년 뒤 어떤 금액을 뜻하는지. 가정을 더 넣지 않는 순수 산술이다."""
    def grow(base, g):
        return base * (1 + g) ** YEARS if (base and g and base > 0) else None
    f10, n10 = grow(fcf, rf_), grow(nopat, rn_)
    return dict(fcf10=f10, nopat10=n10,
                fcf_x=(f10 / fcf if f10 else None),
                nopat_x=(n10 / nopat if n10 else None),
                fcf10_rev=(f10 / rev if (f10 and rev) else None),
                nopat10_rev=(n10 / rev if (n10 and rev) else None))


def rows():
    return [row(t) for t in TICKERS]


def bias_rows():
    """구조적 편향을 재는 줄. 예측 채점이 아니라 배수 둘의 거리다.

    우리 잣대의 영구가치 배수는 (1+g)/(r-g) 하나로 정해진다. 그 값이 지난 3년 동안
    시장이 실제로 낸 배수 범위 안에 든 적이 있는가를 본다. 한 번도 없으면 그것은
    예측이 틀린 것이 아니라 잣대가 구조적으로 낮은 것이다.

    시장 배수는 facts.json 의 lookback 이 준다 — 그때 제출돼 있던 서류만으로 낸
    값이라 사후 정보가 안 섞인다.
    """
    out = []
    for t in TICKERS:
        d = _facts(t)
        tt = d['sec']['ttm']
        fcf = (tt['ocf']['val'] - tt['capex']['val']) / 1e9
        mcap = d['market']['market_cap'] / 1e9
        now = (mcap / fcf) if fcf > 0 else None
        lb = [r['multiple'] for r in (d.get('lookback') or []) if r.get('multiple')]
        ke = d['risk_free']['rate'] + d['beta']['beta'] * 0.046
        ours = (1 + 0.0275) / (ke - 0.0275)
        out.append(dict(t=t, name=NAMES[t], now=now, lo=min(lb) if lb else None,
                        hi=max(lb) if lb else None, n=len(lb), ours=ours,
                        beta=d['beta']['beta'], ke=ke,
                        gap=(now / ours) if now else None,
                        inside=bool(lb) and min(lb) <= ours <= max(lb)))
    return out


# 순위가 잣대를 바꾸면 얼마나 흔들리나. 절 8이 이 잣대에 남긴 유일한 쓰임이 「회사끼리
# 견주기」였으므로, 그 쓰임이 성립하는지는 **순위의 안정성**으로만 답할 수 있다.
#
# 축 넷을 쓴다 — 배수와 요구 성장률 각각에 대해 주식보상을 두고 잰 것과 빼고 잰 것.
# 넷 다에서 자리가 같은 회사는 잣대가 가를 수 있는 회사이고, 자리가 바뀌는 회사는
# 못 가르는 회사다.
_AXES = (('배수', 'mult', False), ('배수(주식보상 뺀 값)', 'mult_sbc', False),
         ('요구 성장률', 'req_fcf', False),
         ('요구 성장률(주식보상 뺀 값)', 'req_fcf_sbc', False))


def rankings():
    """축마다 「싼 순서」를 낸다. 값이 없는 회사는 그 축에서 빠진다."""
    rs = rows()
    out = []
    for label, key, rev in _AXES:
        ok = [r for r in rs if r.get(key) is not None]
        out.append(dict(label=label, key=key,
                        order=[r['name'] for r in
                               sorted(ok, key=lambda r: r[key], reverse=rev)]))
    return out


def rank_stability():
    """회사마다 축 넷에서 몇 번째였나. 자리 폭이 곧 못 가르는 정도다."""
    rk = rankings()
    out = []
    for r in rows():
        pos = [a['order'].index(r['name']) + 1 for a in rk if r['name'] in a['order']]
        out.append(dict(name=r['name'], t=r['t'], seen=len(pos),
                        best=min(pos) if pos else None,
                        worst=max(pos) if pos else None,
                        spread=(max(pos) - min(pos)) if pos else None,
                        fixed=bool(pos) and len(set(pos)) == 1))
    return out


def sbc_rows():
    """현금이 안 나가는 항목 하나가 우리 기준값을 얼마나 들어 올리나.

    우리 잉여현금흐름은 영업현금흐름에서 설비투자를 뺀 값이다. 영업현금흐름에는
    주식보상비용이 비현금 항목으로 도로 더해져 있다 — 회사가 임직원에게 새로 찍은
    주식을 주므로 현금은 안 나가지만 주주 지분은 묽어진다.

    여기서 빼야 하는지를 정하지 않는다. 두 값을 나란히 내고 **회사마다 벌어지는 폭이
    얼마나 다른지**를 보인다. 폭이 고르면 회사끼리 견줄 때 상쇄되지만, 열 배 넘게
    다르면 우리가 잣대에 남겨 둔 단 하나의 쓰임(회사 간 비교)이 그만큼 흔들린다.
    """
    out = []
    for r in rows():
        f, sb, adj, mc = r['fcf'], r['sbc'], r['fcf_sbc'], r['mcap']
        out.append(dict(t=r['t'], name=r['name'], fcf=f, sbc=sb, adj=adj,
                        share=r['sbc_share'],
                        mult=(mc / f) if (f and f > 0) else None,
                        mult_adj=(mc / adj) if (adj and adj > 0) else None))
    return out


def write_facts():
    """check_report 가 대조할 사실표. 본문이 찍는 형태 그대로 적는다."""
    L = ['# 빅테크 여섯 비교 사실표 — 기계 대조용', '',
         '자동 생성이다. `python scratchpad/_val_peers.py` 가 다시 쓴다.', '',
         '- 시장위험프리미엄 4.6%', '- 통일 세율 21%', '- 영구성장률 2.75%',
         '- 명시적 기간 10년', '']
    for r in rows():
        L.append('## %s (%s)' % (r['name'], r['t']))
        L.append('')
        def n(x, s='%.1f'):
            return (s % x) if x is not None else '없음'
        L += ['- TTM 끝 %s' % r['end'],
              '- 매출 %s' % n(r['rev'], '%.0f'),
              '- 영업이익 %s · 영업이익률 %s' % (n(r['ebit'], '%.1f'),
                                          n(r['ebit_m'] and r['ebit_m'] * 100, '%.1f%%')),
              '- 잉여현금흐름 %s · 마진 %s' % (n(r['fcf'], '%.0f'),
                                        n(r['fcf_m'] and r['fcf_m'] * 100, '%.1f%%')),
              '- 설비투자 %s · 감가상각 %s · 배수 %s'
              % (n(r['capex'], '%.0f'), n(r['dna'], '%.0f'), n(r['cd'], '%.2f')),
              '- NOPAT %s' % n(r['nopat'], '%.0f'),
              '- 베타 %.3f · 자기자본비용 %.2f%%' % (r['beta'], r['ke'] * 100),
              '- 시가총액 %s · 순현금 %s' % (n(r['mcap'], '%.0f'), n(r['net_cash'], '%.0f')),
              '- 실제 납부세율 %s' % n(r['cash_tr'] and r['cash_tr'] * 100, '%.1f%%'),
              '- 잉여현금흐름 기준 요구 성장률 %s'
              % n(r['req_fcf'] and r['req_fcf'] * 100, '%.2f%%'),
              '- NOPAT 기준 요구 성장률 %s'
              % n(r['req_nopat'] and r['req_nopat'] * 100, '%.2f%%')]
        if r['req_fcf'] and r['req_nopat']:
            L.append('- 두 기준 차이 %.1f%%포인트' % ((r['req_fcf'] - r['req_nopat']) * 100))
        L += ['- 10년 뒤 요구 잉여현금흐름 %s · 지금의 %s · 지금 매출의 %s'
              % (n(r['fcf10'], '%.0f'), n(r['fcf_x'], '%.1f배'), n(r['fcf10_rev'], '%.1f배')),
              '- 10년 뒤 요구 NOPAT %s · 지금의 %s · 지금 매출의 %s'
              % (n(r['nopat10'], '%.0f'), n(r['nopat_x'], '%.1f배'),
                 n(r['nopat10_rev'], '%.1f배'))]
        L.append('')
    L += ['## 구조적 편향 — 우리 배수와 시장 배수', '']
    for b in bias_rows():
        L.append('- %s 우리 영구가치 배수 %.1f배 · 지금 시장 배수 %s · 지난 3년 시장 범위 '
                 '%.0f~%.0f배 · 관측 %d개 · 우리 배수가 그 범위 안인가 %s'
                 % (b['name'], b['ours'],
                    ('%.0f배' % b['now']) if b['now'] else '없음(잉여현금흐름 0 이하)',
                    b['lo'], b['hi'], b['n'], '그렇다' if b['inside'] else '아니다'))
        if b['gap']:
            L.append('- %s 지금 시장 배수가 우리 배수의 %.1f배' % (b['name'], b['gap']))
    _bb = bias_rows()
    L += ['- 우리 배수 최저 %.1f배 · 최고 %.1f배'
          % (min(x['ours'] for x in _bb), max(x['ours'] for x in _bb)),
          '- 시장 범위 최저 %.0f배 · 최고 %.0f배'
          % (min(x['lo'] for x in _bb), max(x['hi'] for x in _bb)),
          '- 우리 배수가 시장 범위 안에 든 회사 %d곳' % sum(1 for x in _bb if x['inside']),
          '- 거리가 가장 작은 곳 %s %.1f배 · 가장 큰 곳 %s %.1f배'
          % (min((x for x in _bb if x['gap']), key=lambda x: x['gap'])['name'],
             min(x['gap'] for x in _bb if x['gap']),
             max((x for x in _bb if x['gap']), key=lambda x: x['gap'])['name'],
             max(x['gap'] for x in _bb if x['gap'])),
          '']
    L += ['## 현금 아닌 것에 우리 기준값이 얼마나 기대나 — 주식보상비용', '']
    _sb = sbc_rows()
    for r in _sb:
        L.append('- %s 잉여현금흐름 %.1f · 주식보상비용 %.1f · 잉여현금흐름 대비 %s · '
                 '빼고 남는 값 %.1f'
                 % (r['name'], r['fcf'], r['sbc'],
                    ('%.1f%%' % (r['share'] * 100)) if r['share'] else
                    '잴 수 없음(잉여현금흐름 0 이하)', r['adj']))
        if r['mult'] and r['mult_adj']:
            L.append('- %s 지금 시장 배수 %.0f배 · 빼고 재면 %.0f배'
                     % (r['name'], r['mult'], r['mult_adj']))
        # 본문 표는 억 달러로 찍는다. 대조가 자릿수까지 붙게 같은 단위도 함께 적는다.
        L.append('- %s 억 달러 표기 · 잉여현금흐름 %.0f억 달러 · 주식보상비용 %.0f억 달러'
                 % (r['name'], r['fcf'] * 10, r['sbc'] * 10))
    _sh = [(x['share'], x['name']) for x in _sb if x['share']]
    L += ['- 잉여현금흐름 대비 비중 최저 %s %.1f%% · 최고 %s %.1f%%'
          % (min(_sh)[1], min(_sh)[0] * 100, max(_sh)[1], max(_sh)[0] * 100),
          '- 최고가 최저의 %.1f배' % (max(_sh)[0] / min(_sh)[0]),
          '- 여섯 합계 주식보상비용 %.1f' % sum(x['sbc'] for x in _sb),
          '- 여섯 합계 주식보상비용 %.0f억 달러' % (sum(x['sbc'] for x in _sb) * 10),
          '']
    # 본문이 찍는 표기를 그대로 한 번 더 적는다. 자릿수가 다르면 check_report 가
    # 못 찾는다 — 요구 성장률은 소수 한 자리, 금액은 억 달러다.
    L += ['## 본문 표기 그대로', '']
    for r in rows():
        L.append('- %s 시가총액 %.0f억 달러 · 잉여현금흐름 %.0f억 달러'
                 % (r['name'], r['mcap'] * 10, r['fcf'] * 10))
        if r['req_fcf']:
            L.append('- %s 요구 성장률 %.1f%% · 주식보상 빼고 재면 %.1f%%'
                     % (r['name'], r['req_fcf'] * 100,
                        (r['req_fcf_sbc'] or 0) * 100))
        for k in ('purchase_unrecorded', 'guarantee_max', 'nonmarketable_equity',
                  'lt_debt', 'st_debt'):
            v = _facts(r['t'])['sec']['ttm'].get(k)
            if v:
                L.append('- %s %s %.0f억 달러' % (r['name'], k, v['val'] / B * 10))
    L += ['']

    L += ['## 잣대를 바꾸면 순위가 흔들리나', '']
    for a in rankings():
        L.append('- %s 싼 순서 %s' % (a['label'], ' > '.join(a['order'])))
    for x in rank_stability():
        if x['seen']:
            L.append('- %s 축 %d개에서 %d등~%d등 · 자리 폭 %d%s'
                     % (x['name'], x['seen'], x['best'], x['worst'], x['spread'],
                        ' (안 흔들린다)' if x['fixed'] else ''))
        else:
            L.append('- %s 어느 축에도 안 나온다(잉여현금흐름 0 이하)' % x['name'])
    _st = [x for x in rank_stability() if x['seen']]
    L += ['- 자리가 한 번도 안 바뀐 회사 %d곳' % sum(1 for x in _st if x['fixed']),
          '- 자리 폭이 가장 큰 곳 %s %d' % (max(_st, key=lambda x: x['spread'])['name'],
                                     max(x['spread'] for x in _st)),
          '']
    p2 = os.path.join(_root, 'scratchpad', 'peers_facts.md')
    io.open(p2, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p2


def report():
    rs = rows()
    print('%-8s %-11s %6s %7s %7s %7s %6s %6s %7s %8s %9s'
          % ('회사', 'TTM끝', '매출', '영업익률', 'FCF', 'FCF마진', 'C/D',
             '베타', 'Ke', 'FCF역산', 'NOPAT역산'))
    for r in rs:
        f = lambda x, s='%.1f': (s % x) if x is not None else '-'
        print('%-8s %-11s %6s %7s %7s %7s %6s %6.3f %6.2f%% %8s %9s'
              % (r['name'], r['end'], f(r['rev'], '%.0f'),
                 f(r['ebit_m'] and r['ebit_m'] * 100, '%.1f%%'),
                 f(r['fcf'], '%.0f'), f(r['fcf_m'] and r['fcf_m'] * 100, '%.1f%%'),
                 f(r['cd'], '%.2f'), r['beta'], r['ke'] * 100,
                 f(r['req_fcf'] and r['req_fcf'] * 100, '%.2f%%'),
                 f(r['req_nopat'] and r['req_nopat'] * 100, '%.2f%%')))


if __name__ == '__main__':
    report()
    print('\n사실표 ->', write_facts())
