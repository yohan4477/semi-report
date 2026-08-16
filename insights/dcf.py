# DCF(현금흐름할인) 계산기. 순수 함수만 둔다 — 파일 입출력도, 전역 상태도 없다.
# 존재 이유: 필자들이 리포트에 낸 밸류에이션 숫자를 재현해서, 우리가 인용하는
# "적정주가" 같은 숫자가 실제로 그 필자의 가정에서 나오는지 검증하기 위함이다.
#
# 할인 규약(중요 — 임의로 바꾸면 재현 테스트가 깨진다):
#   - 기말 할인. 1차연도 FCF를 (1+r)^1로 나눈다. mid-year 보정 없음
#   - Terminal Value는 Gordon growth: TV = FCF_마지막해 * (1+g) / (r-g)
#   - TV의 현재가치는 명시적 기간 마지막 연도와 같은 지수로 할인한다


def pv_explicit(fcfs, r):
    """명시적 기간 FCF 리스트의 현재가치 합. fcfs[0]이 1차연도(할인지수 1)."""
    return sum(fcf / (1 + r) ** (i + 1) for i, fcf in enumerate(fcfs))


def terminal_value(fcf_last, r, g):
    """Gordon growth 영구가치. 할인 전, 명시적 기간 말 시점 값."""
    if r <= g:
        raise ValueError(f'r({r})가 g({g})보다 커야 Gordon growth가 수렴한다')
    return fcf_last * (1 + g) / (r - g)


def pv_terminal(fcf_last, r, g, n):
    """영구가치의 현재가치. n = 명시적 기간 연수(TV와 같은 지수로 할인)."""
    tv = terminal_value(fcf_last, r, g)
    return tv / (1 + r) ** n


def value(fcfs, r, g, net_debt=0.0, shares=None):
    """전체 평가.

    net_debt: 순부채. 순현금이면 음수로 넣는다(자기자본가치가 EV보다 커짐).
    shares가 None이면 per_share도 None.

    단위는 함수가 모른다. fcfs와 net_debt이 억원인데 shares가 주수면
    per_share는 억원/주로 나온다 — 삼성전자 사례에서 0.0036이 그것이다.
    원 단위 주가로 보려면 호출자가 1e8을 곱한다. 이 자리를 틀리면 자릿수가
    통째로 어긋나므로 평가 JSON을 쓰는 쪽에서 배율을 명시한다.
    """
    n = len(fcfs)
    pv_exp = pv_explicit(fcfs, r)
    tv = terminal_value(fcfs[-1], r, g)
    pv_tv = pv_terminal(fcfs[-1], r, g, n)
    ev = pv_exp + pv_tv
    equity = ev - net_debt
    # shares=0을 None으로 삼키면 자릿수 실수가 조용히 지나간다. 0이면 터뜨린다.
    per_share = None if shares is None else equity / shares
    tv_share = pv_tv / ev if ev else None
    return {
        'pv_explicit': pv_exp,
        'tv': tv,
        'pv_tv': pv_tv,
        'ev': ev,
        'equity': equity,
        'per_share': per_share,
        'tv_share': tv_share,
    }


def sensitivity(fcfs, r_list, g_list, net_debt=0.0, shares=None):
    """WACC x 영구성장률 격자. {(r, g): per_share}."""
    grid = {}
    for r in r_list:
        for g in g_list:
            grid[(r, g)] = value(fcfs, r, g, net_debt, shares)['per_share']
    return grid


def wacc(rf, beta, mrp, kd_after_tax, debt_weight):
    """CAPM 기반 WACC. ke = rf + beta*mrp; wacc = ke*(1-debt_weight) + kd_after_tax*debt_weight"""
    ke = rf + beta * mrp
    return ke * (1 - debt_weight) + kd_after_tax * debt_weight


def fade(g_start, g_end, years):
    """선형 fade 성장률 경로. years개 값, 첫 값이 g_start, 마지막이 g_end로 균등 분할.

    years==1이면 [g_end] — 첫 해에서 바로 종착 성장률로 넘어간다는 뜻.
    """
    if years <= 0:
        return []
    if years == 1:
        return [g_end]
    step = (g_end - g_start) / (years - 1)
    return [g_start + step * i for i in range(years)]


def project_fcf(fcf0, growths):
    """기준 FCF에 성장률 경로를 곱해 연도별 FCF를 만든다."""
    out = []
    prev = fcf0
    for g in growths:
        prev = prev * (1 + g)
        out.append(prev)
    return out


def fcff(nopat_, dna, capex, delta_nwc):
    """FCFF = NOPAT + D&A - CAPEX - 운전자본증가(순운전자본증감)"""
    return nopat_ + dna - capex - delta_nwc


def nopat(ebit, tax_rate):
    """EBIT * (1 - t)"""
    return ebit * (1 - tax_rate)


def implied_discount_rate(fcfs, g, target_equity, net_debt=0.0, tol=1e-9):
    """역산①: 목표 자기자본가치가 나오려면 할인율이 얼마여야 하나. 이분법.

    범위 0.001~1.0. 해가 없으면(구간 내에서 부호가 안 바뀌면) None.
    자기자본가치는 r이 커질수록 단조 감소하므로 이분법이 안전하다.
    """
    lo, hi = 0.001, 1.0 - 1e-9

    def eq_at(r):
        # r <= g면 발산하므로, g보다 살짝 큰 지점부터 유효 구간으로 본다.
        if r <= g:
            return None
        return value(fcfs, r, g, net_debt)['equity']

    # 유효 구간 하한을 g보다 크게 밀어올린다.
    lo = max(lo, g + 1e-6)
    f_lo = eq_at(lo)
    f_hi = eq_at(hi)
    if f_lo is None or f_hi is None:
        return None
    # 단조감소: f_lo >= target >= f_hi 이어야 해가 구간 안에 있다.
    if not (f_hi <= target_equity <= f_lo):
        return None
    while hi - lo > tol:
        mid = (lo + hi) / 2
        f_mid = eq_at(mid)
        if f_mid is None:
            lo = mid
            continue
        if f_mid > target_equity:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def implied_growth(fcf0, r, g_terminal, years, target_equity, net_debt=0.0, tol=1e-9):
    """역산②: 목표 자기자본가치가 나오려면 명시적 기간 성장률 g가 얼마여야 하나.

    fcf0에 균일 성장률 g를 years년 적용해 명시적 기간 FCF를 만들고,
    이후 g_terminal 영구성장(Gordon growth)으로 이어붙인다.
    범위 -0.5~2.0. 자기자본가치는 g가 커질수록 단조 증가하므로 이분법이 안전하다.
    """
    lo, hi = -0.5, 2.0

    def eq_at(g):
        fcfs = project_fcf(fcf0, [g] * years)
        return value(fcfs, r, g_terminal, net_debt)['equity']

    f_lo = eq_at(lo)
    f_hi = eq_at(hi)
    if not (f_lo <= target_equity <= f_hi):
        return None
    while hi - lo > tol:
        mid = (lo + hi) / 2
        f_mid = eq_at(mid)
        if f_mid < target_equity:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
