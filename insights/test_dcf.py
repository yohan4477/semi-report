# dcf.py 재현 테스트. 필자가 실제로 낸 밸류에이션 리포트 숫자를 그대로 넣어
# 우리 계산기가 같은 결론에 도달하는지 검증한다. 이 테스트가 깨지면 계산기가
# 틀린 것이다 — 사양(할인 규약)을 바꿔서 통과시키지 않는다.
import dcf


def approx(actual, expected, pct):
    """상대오차가 pct(0.1이면 0.1%) 이내인가."""
    if expected == 0:
        return abs(actual) < 1e-9
    return abs(actual - expected) / abs(expected) * 100 <= pct


# ── 사례 1: 삼성전자, 필자 2026-07-16 평가 ──────────────────────────
SEC_FCFS = [2337932, 3655949, 3498216, 3028735,
            2366276, 1770471, 1369360, 1100917]
SEC_R = 0.1034
SEC_G = 0.025
SEC_NET_DEBT = -1192160  # 순현금이라 음수
SEC_SHARES = 5846278608
UNIT = 100_000_000  # 억원 -> 원 (per_share 환산용, shares는 실주식수)


def _sec_value():
    return dcf.value(SEC_FCFS, SEC_R, SEC_G, SEC_NET_DEBT, SEC_SHARES)


def test_samsung_pv_explicit():
    v = _sec_value()
    assert approx(v['pv_explicit'], 13385590, 0.1)


def test_samsung_pv_tv():
    v = _sec_value()
    assert approx(v['pv_tv'], 6550866, 0.1)


def test_samsung_ev():
    v = _sec_value()
    assert approx(v['ev'], 19936456, 0.1)


def test_samsung_equity():
    v = _sec_value()
    assert approx(v['equity'], 21128616, 0.1)


def test_samsung_per_share_won():
    v = _sec_value()
    per_share_won = v['per_share'] * UNIT
    assert approx(per_share_won, 361403, 0.1)


def test_samsung_sensitivity_grid():
    # 필자가 낸 5x5 감도표 (WACC 세로, g 가로, 단위 원). 25칸 전부 0.5% 이내.
    r_list = [0.0934, 0.0984, 0.1034, 0.1084, 0.1134]
    g_list = [0.015, 0.020, 0.025, 0.030, 0.035]
    expected = {
        0.0934: [376014, 384771, 394809, 406430, 420041],
        0.0984: [361132, 368597, 377079, 386801, 398057],
        0.1034: [347758, 354171, 361403, 369620, 379038],
        0.1084: [335656, 341204, 347418, 354424, 362385],
        0.1134: [324636, 329466, 334843, 340864, 347653],
    }
    grid = dcf.sensitivity(SEC_FCFS, r_list, g_list, SEC_NET_DEBT, SEC_SHARES)
    for r in r_list:
        for i, g in enumerate(g_list):
            won = grid[(r, g)] * UNIT
            assert approx(won, expected[r][i], 0.5), (r, g, won, expected[r][i])


def test_samsung_implied_discount_rate():
    # "현재 주가 255,250원을 정당화하려면 내재 할인율이 약 16.2%여야 한다"
    target_equity = 255250 * SEC_SHARES / UNIT
    r = dcf.implied_discount_rate(SEC_FCFS, SEC_G, target_equity, SEC_NET_DEBT)
    assert r is not None
    assert abs(r - 0.162) <= 0.005  # 0.5%p 허용오차


# ── 사례 2: WACC 산출, 필자 2026-07-16 ──────────────────────────────
def test_wacc_matches_author():
    w = dcf.wacc(rf=0.0420, beta=1.18, mrp=0.0550, kd_after_tax=0.0280, debt_weight=0.0444)
    assert abs(w - 0.1034) <= 0.0005


def test_ke_matches_author():
    ke = 0.0420 + 1.18 * 0.0550
    assert abs(ke - 0.1069) <= 0.0005


# ── 사례 3: NVIDIA, 필자 2025-03-07 평가 (FCFE 2단계) ───────────────
NVDA_FCFE = [64584.58, 98643.10, 127385.67, 144661.47, 163448.00,
             193089.00, 213242.92, 230582.43, 245609.35, 258839.98]
NVDA_R = 0.0848
NVDA_G = 0.0275
NVDA_SHARES = 24_400_000_000
NVDA_UNIT = 1_000_000  # 백만달러 -> 달러


def _nvda_value():
    return dcf.value(NVDA_FCFE, NVDA_R, NVDA_G, 0, NVDA_SHARES)


def test_nvidia_pv_explicit():
    v = _nvda_value()
    assert approx(v['pv_explicit'], 1048331.69, 0.1)


def test_nvidia_tv():
    v = _nvda_value()
    assert approx(v['tv'], 4641502.26, 0.1)


def test_nvidia_pv_tv():
    v = _nvda_value()
    assert approx(v['pv_tv'], 2056656.68, 0.1)


def test_nvidia_per_share_loose():
    # 필자 글 안에서 총 자기자본가치가 3,104,988.37과 3,103,384.91 두 값으로
    # 갈린다(원문 자체 불일치). 우리 계산은 3,105,155.93으로 어느 쪽과도
    # 정확히 안 맞는다 — 그래서 주당가치($127.19)만, 느슨한 0.5%로 검증한다.
    v = _nvda_value()
    per_share_usd = v['equity'] * NVDA_UNIT / NVDA_SHARES
    assert approx(per_share_usd, 127.19, 0.5)


# ── 사례 4: 순수 함수 단위 테스트 ───────────────────────────────────
def test_fade_single_year_uses_end():
    assert dcf.fade(0.10, 0.03, 1) == [0.03]


def test_fade_linear_interpolation():
    path = dcf.fade(0.10, 0.02, 5)
    assert len(path) == 5
    assert path[0] == 0.10
    assert abs(path[-1] - 0.02) < 1e-12
    # 균등 간격인지: 인접 차분이 전부 같아야 한다
    steps = [path[i + 1] - path[i] for i in range(len(path) - 1)]
    assert all(abs(s - steps[0]) < 1e-12 for s in steps)


def test_fade_empty_for_zero_years():
    assert dcf.fade(0.10, 0.03, 0) == []


def test_project_fcf_compounds():
    out = dcf.project_fcf(100, [0.10, 0.10])
    assert abs(out[0] - 110) < 1e-9
    assert abs(out[1] - 121) < 1e-9


def test_fcff_formula():
    assert dcf.fcff(nopat_=100, dna=20, capex=30, delta_nwc=5) == 85


def test_nopat_formula():
    assert abs(dcf.nopat(ebit=200, tax_rate=0.25) - 150) < 1e-9


def test_terminal_value_raises_when_r_le_g():
    try:
        dcf.terminal_value(100, 0.05, 0.05)
        assert False, '발산해야 하는데 ValueError가 안 났다'
    except ValueError:
        pass
    try:
        dcf.terminal_value(100, 0.03, 0.05)
        assert False, 'r<g인데도 ValueError가 안 났다'
    except ValueError:
        pass


def test_value_raises_when_r_le_g():
    try:
        dcf.value([100, 110], 0.05, 0.05)
        assert False
    except ValueError:
        pass


def test_implied_growth_round_trip():
    # g로 명시적 기간 FCF를 만들어 자기자본가치를 구한 뒤, 그 가치를 목표로
    # implied_growth를 돌리면 같은 g가 나와야 한다(왕복 검증).
    fcf0 = 1000
    r = 0.10
    g_terminal = 0.03
    years = 5
    true_g = 0.08

    fcfs = dcf.project_fcf(fcf0, [true_g] * years)
    target_equity = dcf.value(fcfs, r, g_terminal)['equity']

    recovered_g = dcf.implied_growth(fcf0, r, g_terminal, years, target_equity)
    assert recovered_g is not None
    assert abs(recovered_g - true_g) < 1e-6


def test_implied_discount_rate_round_trip():
    fcfs = [100, 110, 121, 133]
    g = 0.02
    true_r = 0.12
    target_equity = dcf.value(fcfs, true_r, g)['equity']

    recovered_r = dcf.implied_discount_rate(fcfs, g, target_equity)
    assert recovered_r is not None
    assert abs(recovered_r - true_r) < 1e-6
