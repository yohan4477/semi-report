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
