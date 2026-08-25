# -*- coding: utf-8 -*-
"""알파벳 3구간 DCF를 Bear/Base/Bull 셋으로 돌린다. 검토용 계산이라 scratchpad에 둔다.

경로는 매출 × FCF마진으로 만든다. FCF를 바로 성장시키지 않는 이유는 지금 알파벳의
FCF가 CapEx로 눌린 값이라(TTM 마진 11.9%) 그 눌린 값에 성장률을 곱하면 압축이 영구히
이어지는 모형이 되기 때문이다. 매출과 마진을 따로 움직여야 R9(정상화 FCF)를 지킨다.

마진은 구간 안에서 선형으로 옮긴다. R12가 성장률을 한 해에 안 꺾는 것과 같은 이유다.
"""
import io, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'insights'))
import dcf

B = 1e9
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(root, 'insights/valuation/GOOGL/facts.json'), encoding='utf-8'))
t = d['sec']['ttm']
REV0 = t['revenue']['val'] / B
FCF0 = (t['ocf']['val'] - t['capex']['val']) / B
MARGIN0 = FCF0 / REV0
NET_DEBT = (t['lt_debt']['val'] + t['st_debt']['val']
            - t['cash']['val'] - t['st_investments']['val']) / B
# 주식수도 10억 주 단위로 맞춘다. equity가 10억 달러 단위라 실주식수로 나누면
# 주당가치가 0에 붙는다 — 2026-08-26에 케이스 셋이 전부 $0으로 나온 원인이다.
SHARES = d['sec']['shares_outstanding']['val'] / B
SHARES_DIL = d['sec']['shares_diluted']['val'] / B
PRICE = d['market']['price']
MCAP = d['market']['market_cap'] / B

P1_YEARS = 3   # 2026~2028
P2_YEARS = 7   # 2029~2035

CASES = {
    # 이름: (P1 성장, P1 끝 마진, P2 끝 성장, P3 마진, 영구성장)
    'Bear': dict(g1=0.14, m1=0.09, g2=0.040, m3=0.15, g=0.0225,
                 why='총액 인식·순환 거래를 크게 깎고, 감가상각 수렴이 마진을 15%까지만 되돌린다'),
    'Base': dict(g1=0.175, m1=0.11, g2=0.050, m3=0.17, g=0.0275,
                 why='세미 GCP 전망을 전사 기준으로 환산하고 순환 거래분을 덜어낸 값'),
    'Bull': dict(g1=0.21, m1=0.13, g2=0.060, m3=0.19, g=0.0325,
                 why='TPU 시스템 판매가 수주 잔고대로 실현되고 CapEx 압축이 2028년에 풀린다'),
}
WACC = 0.10


def lerp(a, b, i, n):
    """구간 안에서 a에서 b로 선형 이동. i는 1부터 n까지."""
    return a + (b - a) * i / n


def path(c):
    """연도별 (매출, 마진, FCF)를 만든다."""
    rows, rev = [], REV0
    for i in range(1, P1_YEARS + 1):
        rev *= 1 + c['g1']
        m = lerp(MARGIN0, c['m1'], i, P1_YEARS)
        rows.append((2025 + i, rev, m, rev * m))
    for i in range(1, P2_YEARS + 1):
        g = lerp(c['g1'], c['g2'], i, P2_YEARS)   # H-모델 선형 감소
        rev *= 1 + g
        m = lerp(c['m1'], c['m3'], i, P2_YEARS)
        rows.append((2025 + P1_YEARS + i, rev, m, rev * m))
    return rows


print('기준 (TTM %s) 매출 %.1fB · FCF %.1fB · 마진 %.1f%% · 순현금 %.1fB'
      % (t['revenue']['end'], REV0, FCF0, MARGIN0 * 100, -NET_DEBT))
print('주가 $%.2f · 시총 %.0fB · 주식수 %.3fB · WACC %.0f%%\n' % (PRICE, MCAP, SHARES, WACC * 100))

print('%-6s %7s %7s %7s %8s %9s %8s %7s' % ('케이스', 'P1성장', 'P1마진', 'P3마진', '영구g', '주당가치', '괴리', 'TV비중'))
out = {}
for name, c in CASES.items():
    rows = path(c)
    fcfs = [r[3] for r in rows]
    v = dcf.value(fcfs, WACC, c['g'], NET_DEBT, SHARES)
    ps = v['per_share']
    tv_share = v['tv_share']
    out[name] = (v, rows)
    print('%-6s %6.1f%% %6.1f%% %6.1f%% %7.2f%% %8.0f%s %7.0f%% %6.0f%%'
          % (name, c['g1'] * 100, c['m1'] * 100, c['m3'] * 100, c['g'] * 100,
             ps, '$', (ps / PRICE - 1) * 100, tv_share * 100))

v = out['Base'][0]
print('\nBase 희석주식 기준 주당 $%.0f' % (v['equity'] / SHARES_DIL))
print('\nBase 연도별 경로')
print('%6s %9s %7s %8s' % ('연도', '매출B', '마진', 'FCF B'))
for y, rev, m, f in out['Base'][1]:
    print('%6d %9.0f %6.1f%% %8.0f' % (y, rev, m * 100, f))

print('\n민감도 (Base 경로, WACC × 영구성장률) — 주당 $')
fcfs = [r[3] for r in out['Base'][1]]
rs = [0.09, 0.095, 0.10, 0.105, 0.11]
gs = [0.0175, 0.0225, 0.0275, 0.0325, 0.0375]
print('%8s' % 'WACC\g' + ''.join('%8.2f%%' % (g * 100) for g in gs))
grid = dcf.sensitivity(fcfs, rs, gs, NET_DEBT, SHARES)   # {(r, g): per_share}
for r in rs:
    print('%7.1f%%' % (r * 100) + ''.join('%9.0f' % grid[(r, g)] for g in gs))


def write_facts():
    """check_report 가 대조할 사실표를 뽑는다.

    검사기는 .md 만 읽는다. 값의 원천은 SEC 제출서류(facts.json)와 이 파일의 계산인데
    둘 다 JSON·파이썬이라 그대로는 대조가 안 된다. 그래서 쓰인 값을 글자로 떨어뜨린다 —
    사람이 손으로 옮기면 본문과 어긋나므로 계산 결과에서 바로 만든다.
    """
    def two(v):
        """10억 달러 값을 두 단위로 낸다.

        본문은 「4,459억 달러」로 쓰고 이 표는 445.9로 쓰면 검사기가 둘을 못 잇는다.
        같은 값을 두 표기로 적어 어느 쪽으로 써도 대조되게 한다.

        억 단위는 정확한 값과 반올림한 값을 함께 적는다. 본문은 억 단위로 반올림해
        쓰지만(1,490억) 실제 값은 1,489.5억이라 한 쪽만 적으면 대조가 안 된다.
        반대로 반올림만 적으면 시가총액 41,940.5억이 41,941로 올라가 「4조 1,940억」과
        어긋난다. 둘 다 같은 값이고 자릿수만 다르다."""
        e = v * 10
        return '%.1f (%s억 · %s억)' % (v, format(e, ',.1f'), format(int(round(e)), ','))

    L = ['# 알파벳 밸류에이션 사실표 — 기계 대조용',
         '',
         '자동 생성이다. `python scratchpad/googl_cases.py` 가 다시 쓴다. 손으로 고치지 않는다.',
         '', '## SEC 제출서류에서 받은 값', '']
    c, tt = d['sec']['concepts'], t
    for k, name in (('revenue', '매출'), ('ebit', '영업이익'), ('ocf', '영업현금흐름'),
                    ('capex', '설비투자'), ('dna', '감가상각비'),
                    ('pretax_income', '세전이익'), ('tax_expense', '세금비용'),
                    ('nonoperating', '영업 밖 손익'), ('equity_fv_gain', '지분 평가이익'),
                    ('cash_taxes_paid', '납부세금')):
        if k in c and '2025' in c[k]:
            L.append('- FY2025 %s %s' % (name, two(c[k]['2025']['val'] / B)))
        if k in tt:
            L.append('- TTM %s %s' % (name, two(tt[k]['val'] / B)))
    L += ['- TTM 잉여현금흐름 %s' % two(FCF0),
          '- FY2025 잉여현금흐름 %s' % two(c['ocf']['2025']['val'] / B - c['capex']['2025']['val'] / B),
          '- TTM 영업이익률 %.1f%%' % (t['ebit']['val'] / t['revenue']['val'] * 100),
          '- FY2025 영업이익률 %.1f%%' % (c['ebit']['2025']['val'] / c['revenue']['2025']['val'] * 100),
          '- TTM 설비투자 대비 감가상각 배수 %.2f' % (t['capex']['val'] / t['dna']['val']),
          '- 순현금 %s' % two(-NET_DEBT),
          '- 주가 %.2f' % PRICE,
          '- 시가총액 %s' % two(MCAP),
          '- 발행주식수 %.3f' % SHARES,
          '- 무위험수익률 %.2f%%' % (d['risk_free']['rate'] * 100),
          '- 베타 %.3f' % d['beta']['beta'],
          '- 베타 관측일수 %d' % d['beta']['n_days'],
          '- 비상장 지분 장부금액 %s' % two(124.3),
          '- 장기 투자자산 %s' % two(131.5),
          '', '## 2026년 2분기 (10-Q)', '',
          '- 매출 %s' % two(119.8), '- 영업이익 %s' % two(40.8),
          '- 순이익 %s' % two(112.2), '- 영업 밖 손익 %s' % two(98.0),
          '- 지분 평가이익 %s' % two(99.0),
          '', '## 우리가 돌린 계산', '',
          '- 할인율 %.1f%%' % (WACC * 100),
          '- 시장위험프리미엄 4.6%',
          '- 자기자본비용 9.99%',
          '- 세율 후보 16.7% / 18.4% / 20.7%',
          '- 명시적 기간 %d년 (구간 %d년 + %d년)' % (P1_YEARS + P2_YEARS, P1_YEARS, P2_YEARS),
          '- 민감도 할인율 축 9.0% 9.5% 10.0% 10.5% 11.0%',
          '- 민감도 영구성장률 축 1.75% 2.25% 2.75% 3.25% 3.75%',
          '- 매출의 94%가 순이익으로 남은 분기',
          '- 잉여현금흐름 27% 감소',
          '- 기준연도와 주가 기준일 시차 237일']
    for name, c2 in CASES.items():
        v = dcf.value([r[3] for r in path(c2)], WACC, c2['g'], NET_DEBT, SHARES)
        L.append('- %s 주당가치 %.0f · 매출성장 %.1f%% · 구간끝마진 %.1f%% · 영구마진 %.1f%% '
                 '· 영구성장 %.2f%% · 영구가치비중 %.0f%% · 현재가 대비 %.0f%%'
                 % (name, v['per_share'], c2['g1'] * 100, c2['m1'] * 100, c2['m3'] * 100,
                    c2['g'] * 100, v['tv_share'] * 100, (v['per_share'] / PRICE - 1) * 100))
    base = [r[3] for r in path(CASES['Base'])]
    g25 = dcf.sensitivity(base, [0.09, 0.095, 0.10, 0.105, 0.11],
                          [0.0175, 0.0225, 0.0275, 0.0325, 0.0375], NET_DEBT, SHARES)
    L.append('- 민감도 최고 %.0f · 최저 %.0f' % (max(g25.values()), min(g25.values())))
    L.append('- 비영업자산 반영 시 주당 가산 %.1f' % (131.5 / SHARES))
    L.append('- 실무 도구 보수적 상한 10년 성장 20%')
    eq = dcf.value(base, WACC, CASES['Base']['g'], NET_DEBT, SHARES)['equity']
    L.append('- Base 비영업자산 반영 주당 %.0f' % ((eq + 131.5) / SHARES))
    for r in (0.09, 0.095, 0.10, 0.105, 0.11):
        L.append('- 역산 요구성장률 (할인율 %.1f%%) %.2f%%'
                 % (r * 100, dcf.implied_growth(FCF0, r, 0.0275, 10, MCAP, NET_DEBT) * 100))
    for name, c2 in CASES.items():
        ir = dcf.implied_discount_rate([r[3] for r in path(c2)], c2['g'], MCAP, NET_DEBT)
        L.append('- %s 경로 내재 할인율 %.2f%% (우리 할인율 대비 %.2f%%p 낮다)'
                 % (name, ir * 100, (WACC - ir) * 100))
    g10 = dcf.implied_growth(FCF0, 0.10, 0.0275, 10, MCAP, NET_DEBT)
    f10 = FCF0 * (1 + g10) ** 10
    last = path(CASES['Base'])[-1][3]
    L += ['- 10년 뒤 요구 잉여현금흐름 %s' % two(f10),
          '- 지금의 %.1f배' % (f10 / FCF0),
          '- Base 경로 마지막 해 잉여현금흐름 %s' % two(last),
          '- 두 값의 차이 %s' % two(f10 - last),
          '- 내재 시장위험프리미엄 3.3%',
          '- 위험 대가 3.80%p']
    L += ['', '## 회계사 판 필자가 알파벳에 쓴 값 (2026-05-16 편)', '',
          '- 2026~2028 매출 성장률 20~22%',
          '- 그 구간 잉여현금흐름 마진 3~8%',
          '- 적정주가 계산 없음',
          '- TTM 실측 잉여현금흐름 마진 11.9%']
    L.append('- 근거 원문 발행일 시차 252일 · 가장 오래된 편 271일')
    p = os.path.join(root, 'scratchpad', 'googl_facts.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return p


if __name__ == '__main__':
    print('\n사실표 ->', write_facts())
