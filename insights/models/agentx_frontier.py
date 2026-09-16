"""AgentX 프런티어 모델 — 같은 사용자 속도에서 1달러당·1메가와트당 토큰과 기가와트당 매출.

원문: input/clippings/Vera Rubin NVL72 Agentic Inference 67x better Performance per Dollar.md
원자료: insights/models/raw/inferencex_dsv4_agentx.json
  rows    InferenceX 공개 API 의 DeepSeek V4 Pro 에이전틱 행(2026-09-13 스냅숏)
  tables  칩 상수·매출 가정은 대시보드 앱(SemiAnalysisAI/InferenceX-app@6f17111) 코드에서 옮겼다

원문은 값만 적고 계산은 앱에 두었다. 앱은 타입스크립트라 여기 파이썬으로 다시 세운다.
사슬은 이렇다.

  동시성 스윕 한 줄  →  위-왼쪽 파레토 프런티어(속도가 낮아질수록 처리량이 커지는 점만)
  프런티어  →  단조 3차 에르미트 보간(Steffen 1990, d3.curveMonotoneX 와 같다)
  목표 속도 s 에서 GPU 한 장의 처리량 T(s)
    1메가와트당 토큰/초  = T × 1000 ÷ 칩당 전력(kW)
    1달러당 토큰         = T × 3600 ÷ 칩당 시간당 원가
    기가와트당 매출      = T × 3600 × 섞은 단가 ÷ 1e6 × (1e6 ÷ kW × 연 시간) × 가동률
    섞은 단가            = 입력 몫 × ((1−캐시 적중) × 입력가 + 캐시 적중 × 캐시 입력가)
                           + (1−입력 몫) × 출력가

캐시 적중과 입력 비중도 같은 프런티어 위에서 같은 보간으로 낸다. 목표 속도가 측정 범위
밖이면 값을 내지 않는다(앱도 그 행을 건너뛴다).
"""

KW_PER_MW = 1000
KW_PER_GW = 1_000_000
SEC_PER_HOUR = 3600
TOK_PER_M = 1_000_000


def frontier(rows):
    """위-왼쪽 파레토 프런티어. 속도(x) 오름차순, 처리량(y)은 x 가 커질수록 줄어든다.

    같은 속도면 처리량이 큰 점만 남기고, 더 빠르면서 처리량도 크거나 같은 점이 오면
    앞의 점을 버린다. 앱의 paretoFrontUpperLeft 와 같은 순서다.
    """
    pts = sorted(rows, key=lambda e: (_x(e), -_y(e)))
    out = []
    for e in pts:
        if out and _x(out[-1]) == _x(e):
            if _y(e) > _y(out[-1]):
                out[-1] = e
            continue
        while out and _y(e) >= _y(out[-1]):
            out.pop()
        out.append(e)
    return out


def _x(e):
    return e['metrics']['p90_intvty']


def _y(e):
    return e['metrics']['tput_per_gpu']


def slopes(xs, ys):
    """Steffen 단조 기울기. 끝점은 3차 끝점 공식으로 낸다."""
    n = len(xs)
    if n < 2:
        return [0.0] * n
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    s = [(ys[i + 1] - ys[i]) / h[i] if h[i] else 0.0 for i in range(n - 1)]
    m = [0.0] * n
    sg = lambda v: -1 if v < 0 else 1
    for i in range(1, n - 1):
        p = (s[i - 1] * h[i] + s[i] * h[i - 1]) / (h[i - 1] + h[i])
        m[i] = (sg(s[i - 1]) + sg(s[i])) * min(abs(s[i - 1]), abs(s[i]), 0.5 * abs(p)) or 0.0
    m[0] = (3 * s[0] - m[1]) / 2 if h[0] else m[1]
    m[-1] = (3 * s[-1] - m[-2]) / 2 if h[-1] else m[-2]
    return m


def hermite(xs, ys, m, t):
    """에르미트 보간. 측정 범위 밖이면 None — 앱은 거기서 값을 끝점에 묶지만 건너뛴다."""
    if not xs or t < xs[0] or t > xs[-1]:
        return None
    lo, hi = 0, len(xs) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if xs[mid] <= t:
            lo = mid
        else:
            hi = mid
    hh = xs[hi] - xs[lo]
    if hh == 0:
        return ys[lo]
    u = (t - xs[lo]) / hh
    u2, u3 = u * u, u * u * u
    return ((2 * u3 - 3 * u2 + 1) * ys[lo] + (u3 - 2 * u2 + u) * hh * m[lo]
            + (-2 * u3 + 3 * u2) * ys[hi] + (u3 - u2) * hh * m[hi])


def at(front, s, fn=_y):
    """프런티어 위 목표 속도 s 에서 한 지표를 보간한다."""
    xs = [_x(e) for e in front]
    ys = [fn(e) for e in front]
    return hermite(xs, ys, slopes(xs, ys), s)


def tok_per_s_per_mw(tput, kw):
    """GPU 한 장 처리량을 1메가와트에 몇 장 드는지로 곱한다."""
    return tput * KW_PER_MW / kw


def tok_per_dollar(tput, hourly):
    """GPU 한 시간 원가 1달러로 몇 토큰을 뽑나."""
    return tput * SEC_PER_HOUR / hourly


def input_share(m):
    """입력 토큰 비중. 입력·출력 처리량 합이 총처리량과 1% 안에서 맞을 때만 그것을 쓴다."""
    t, i, o = m['tput_per_gpu'] or 0, m['input_tput_per_gpu'] or 0, m['output_tput_per_gpu'] or 0
    if t > 0 and i + o > 0 and abs((i + o) / t - 1) <= 0.01:
        return i / (i + o)
    return m['total_prompt_tokens'] / (m['total_prompt_tokens'] + m['total_generation_tokens'])


def cache_hit(m, hw):
    """값을 매길 캐시 적중률. 서버가 잰 값이 먼저고, GB300 만 트레이스 이론값으로 메운다.

    GB300 발사 스크립트가 워커 지표 주소를 안 넘겨 서버 값이 비기 때문이다.
    """
    g, c = m.get('server_gpu_cache_hit_rate'), m.get('server_cpu_cache_hit_rate')
    if g is not None or c is not None:
        return max(0.0, min(1.0, (g or 0) + (c or 0)))
    if hw == 'gb300':
        return m.get('theoretical_cache_hit_rate')
    return None


def blended_price(share, hit, p_in, p_cached, p_out):
    """백만 토큰당 섞은 단가."""
    return share * ((1 - hit) * p_in + hit * p_cached) + (1 - share) * p_out


def gpu_hours_per_gw_year(kw, hours_per_year):
    return KW_PER_GW / kw * hours_per_year


def per_gw_year(front, hw, s, kw, hourly, price, utilization, hours_per_year):
    """목표 속도 s 에서 기가와트당 연 매출·원가·이익(달러)과 중간값."""
    t = at(front, s)
    if t is None:
        return None
    hits = [cache_hit(e['metrics'], hw) for e in front]
    hit = at(front, s, lambda e: cache_hit(e['metrics'], hw)) if None not in hits else 0.0
    share = at(front, s, lambda e: input_share(e['metrics']))
    bp = blended_price(share, hit, price['input_per_m'], price['cached_input_per_m'],
                       price['output_per_m'])
    gh = gpu_hours_per_gw_year(kw, hours_per_year)
    rev = t * SEC_PER_HOUR * bp / TOK_PER_M * gh * utilization
    tco = hourly * gh
    return {'tput': t, 'hit': hit, 'share': share, 'price': bp,
            'revenue': rev, 'tco': tco, 'profit': rev - tco}


def fleet_gpus(mw, kw):
    """전력 예산에 드는 GPU 장수. 한 장 단위로 내린다."""
    return int(mw * KW_PER_MW // kw)


def availability(mtbi_days, recovery_hours):
    """평균 고장 간격과 복구 시간에서 가용률."""
    return mtbi_days / (mtbi_days + recovery_hours / 24)
