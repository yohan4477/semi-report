# -*- coding: utf-8 -*-
"""회계사 카드 도해 — 2026-10-08 추가분 여섯 편(엘곰 260928~261007) 중 열 장.

  K1 나란한 세로 막대   8월 고용은 예상의 세 배 가까이, 9월 전망은 6만~10만 명 (주간 전망)
  K2a 나란한 세로 막대  인플레이션 3.8%·3.4%와 목표 2% (근원 PCE·금리)
  K2b 모듈 두 줄        인상 한 번을 모듈 하나로 — 점도표 1회, 금리선물 3회
  K3 막대 + 점선 기둥   필요한 AI 시장 6조 달러, 예상 상단 1.8조, 빈 4.2조 (Bain)
  K4a 세로 막대 여섯    베타만 바꾸면 주당 내재가치가 52만에서 38만으로 (에이피알)
  K4b 구성 기둥 하나    기업가치 195,664억원 중 영구가치 현가 65.4%
  K5a 진행 막대 둘      자사주 계획 물량의 74.69%와 58.79%
  K5b 같은 꼴 두 줄     매수 주체가 바뀌는 길과 안 바뀌는 길
  K6a 좌우 두 판        주가 27만 대 목표 49만, 영업이익 100조 대 눈높이 105~110조
  K6b 가로 막대 열      AI 인프라 종목의 간밤 등락 — 메모리만 내렸다

규칙(yohan-figure · 확정 규칙 도해 §3·§5·§7):
  - 값은 원문에 있는 것만 옮겼다. 막대는 0에서 시작하고 높이는 값에 비례한다.
  - 색은 회색만. 짙은 채움은 판마다 한 곳이고 점선은 아직 없는 것에만 쓴다.
  - 판 위 글자는 이름과 값 라벨이다. 설명이 붙을 자리에는 ①②③ 글자만 얹고 캡션이 푼다.
  - 캡션은 번호 풀이다. 본문이 한 말을 되풀이하지 않는다.
  - 붓(k8-*)은 _figs_kicpa_0908 의 CSS 를 그대로 쓴다. 생성기가 이미 그 CSS 를 싣는다.
"""

CSS = ''   # 새 붓 없음 — figs_k0908.CSS 의 k8-fill · k8-open · k8-dash · k8-rule · k8-thin 사용


def _t(x, y, cls, s, anchor=None):
    return ('<text x="%.1f" y="%.1f" class="%s"%s>%s</text>'
            % (x, y, cls, (' text-anchor="%s"' % anchor) if anchor else '', s))


def _rect(cls, x, y, w, h, rx=5):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" class="%s"/>' % (
        x, y, w, h, rx, cls)


def _line(cls, x1, y1, x2, y2):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (x1, y1, x2, y2, cls)


def _arrow(x1, x2, y):
    """오른쪽으로 가는 가로 화살표. 선 하나와 작은 삼각형."""
    return (_line('k8-rule', x1, y, x2 - 6, y)
            + '<polygon class="k8-fill" points="%.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
            % (x2, y, x2 - 7, y - 4, x2 - 7, y + 4))


# ── K1 비농업 고용 — 8월 예상과 발표, 9월 두 전망 ─────────────────────────
# 값은 [260928] 편에 있는 것만: 8월 예상 5만 3천 명 · 발표 16만 2천 명 · 9월 평균 예상 10만 명
# · 뱅크오브아메리카 6만 명. 막대 높이는 만 명 단위 값에 비례한다.
def fig_jobs():
    base, ph = 184, 120.0 / 16.2
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="8월 비농업 고용은 예상 5만 3천 명에 '
         '발표 16만 2천 명이었고 9월은 평균 예상 10만 명, 뱅크오브아메리카 6만 명이다">']
    h.append(_t(26, 22, 't-head', '비농업 고용 증가 (만 명)'))
    h.append(_line('k8-rule', 40, base, 534, base))
    bars = [(78, '예상', 5.3, '5.3', 'k8-open'), (160, '발표', 16.2, '16.2', 'k8-fill'),
            (312, '평균 예상', 10.0, '10', 'k8-open'), (394, 'BofA 예상', 6.0, '6', 'k8-open')]
    for x, name, v, lab, cls in bars:
        hg = v * ph
        h.append(_rect(cls, x, base - hg, 64, hg))
        h.append(_t(x + 32, base - hg - 9, 't-val', lab, 'middle'))
        h.append(_t(x + 32, base + 17, 't-sub', name, 'middle'))
    h.append(_t(174, base + 42, 't-step', '① 8월', 'middle'))
    h.append(_t(386, base + 42, 't-step', '② 9월', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_JOBS = (
    1, '8월 고용은 예상의 세 배 가까이였고 9월 전망은 그 아래다',
    fig_jobs(),
    '① 8월 비농업 고용. 왼쪽이 사전 예상치, 짙은 막대가 발표치다.<br>'
    '② 9월 비농업 고용 전망. 시장 평균과 뱅크오브아메리카 예상이며 아직 발표 전이다.')


# ── K2a 인플레이션 두 줄과 목표 ──────────────────────────────────────────
# 값은 [260930] 편에 있는 것만: 헤드라인 약 3.8% · 근원 약 3.4% (8월까지 12개월) · 목표 2%
def fig_infl():
    base, ph = 178, 118.0 / 3.8
    h = ['<svg viewBox="0 0 560 236" role="img" aria-label="8월까지 12개월 헤드라인 인플레이션은 '
         '약 3.8퍼센트 근원은 약 3.4퍼센트로 연준 목표 2퍼센트를 웃돈다">']
    h.append(_t(26, 22, 't-head', '8월까지 12개월 인플레이션 (%)'))
    h.append(_line('k8-rule', 60, base, 534, base))
    bars = [(104, '연준 목표', 2.0, '2', 'k8-open', '②'), (254, '근원', 3.4, '약 3.4', 'k8-fill', '①'),
            (404, '헤드라인', 3.8, '약 3.8', 'k8-fill', '①')]
    for x, name, v, lab, cls, mark in bars:
        hg = v * ph
        h.append(_rect(cls, x, base - hg, 72, hg))
        h.append(_t(x + 36, base - hg - 9, 't-val', lab, 'middle'))
        h.append(_t(x + 36, base + 17, 't-sub', name, 'middle'))
        h.append(_t(x + 36, base + 38, 't-step', mark, 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_INFL = (
    2, '헤드라인 물가는 연준 목표의 두 배 가까이다',
    fig_infl(),
    '① 8월까지 12개월 기준. 두 막대 모두 원문이 약 3.8%와 약 3.4%로 적은 근사치다.<br>'
    '② 연준의 물가 목표 수준이다.')


# ── K2b 인상 횟수 — 같은 모듈 줄 ─────────────────────────────────────────
# 값은 [260930] 편에 있는 것만: 점도표 중간값 연내 1회 추가 인상(워시 의장 제외) ·
# 금리선물 추가 3회 인상 반영. 모듈 하나가 인상 한 번이다.
def fig_hikes():
    h = ['<svg viewBox="0 0 560 190" role="img" aria-label="연준 위원 중간값은 연내 1회 추가 인상, '
         '금리선물은 추가 3회 인상을 반영한다">']
    h.append(_t(26, 22, 't-head', '추가 금리 인상 횟수 (모듈 하나가 인상 한 번)'))
    rows = [(60, '연준 위원 중간값', '①', 1, '1회'), (122, '금리선물 시장', '②', 3, '3회')]
    for y, name, mark, n, lab in rows:
        h.append(_t(26, y + 20, 't-step', name))
        h.append(_t(26, y + 38, 't-step', mark))
        for i in range(n):
            h.append(_rect('k8-fill', 196 + i * 86, y, 70, 40, 6))
        h.append(_t(196 + n * 86 + 6, y + 26, 't-val', lab))
    h.append('</svg>')
    return ''.join(h)


FIG_HIKES = (
    3, '연준은 한 번, 금리선물은 세 번을 본다',
    fig_hikes(),
    '① 점도표(위원들의 금리 전망 분포)의 중간값. 워시 의장을 뺀 위원회 기준이다.<br>'
    '② 연방기금금리 선물에 실제로 돈을 건 투자자들의 베팅이다. 월가 이코노미스트의 전망치가 아니다.')


# ── K3 Bain — 필요한 시장과 예상 시장 ────────────────────────────────────
# 값은 [261001] 편에 있는 것만: 필요 시장 약 6조 달러 · 소비자·기업용 AI 시장 1.2조~1.8조 달러
# (위 끝 1.8조로 그렸다) · 격차 4.2조 달러. 빈 칸은 점선으로 둔다.
def fig_bain():
    base, ph = 196, 140.0 / 6.0
    h = ['<svg viewBox="0 0 560 262" role="img" aria-label="Bain 계산: 지금 수준의 AI 투자를 이으려면 '
         '연 6조 달러 시장이 필요한데 예상 시장은 1.2조에서 1.8조 달러라 4.2조 달러가 빈다">']
    h.append(_t(26, 22, 't-head', '연간 AI 시장 규모 (조 달러)'))
    h.append(_line('k8-rule', 60, base, 534, base))
    # 필요 시장
    h.append(_rect('k8-fill', 120, base - 6 * ph, 110, 6 * ph))
    h.append(_t(175, base - 6 * ph - 9, 't-val', '약 6', 'middle'))
    h.append(_t(175, base + 18, 't-sub', '필요한 시장', 'middle'))
    h.append(_t(175, base + 38, 't-step', '①', 'middle'))
    # 예상 시장 + 빈 칸
    h.append(_rect('k8-dash', 330, base - 6 * ph, 110, 6 * ph - 1.8 * ph))
    h.append(_rect('k8-open', 330, base - 1.8 * ph, 110, 1.8 * ph))
    h.append(_t(385, base - 1.8 * ph + 22, 't-val', '1.2~1.8', 'middle'))
    h.append(_t(385, base - 3.9 * ph + 6, 't-val', '격차 4.2', 'middle'))
    h.append(_t(385, base + 18, 't-sub', '예상 시장', 'middle'))
    h.append(_t(385, base + 38, 't-step', '②', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_BAIN = (
    3, '필요한 시장과 예상 시장 사이에 4.2조 달러가 빈다',
    fig_bain(),
    '① 설비투자가 산업 매출의 약 25%라는 Bain의 가정 아래, 지금 수준의 투자를 이으려면 필요한 시장.<br>'
    '② 소비자·기업용 AI 시장 예상 범위. 막대 높이는 위 끝(1.8조)이고, 점선 칸이 아직 채울 곳이 없는 부분이다.')


# ── K4a 에이피알 — 베타 출처별 주당 내재가치 ─────────────────────────────
# 값은 [261001] 에이피알 평가 요약표에 있는 것만. 현재가 367,000원은 10월 1일 10:49 기준.
_APR = [('0.65', '코스콤', 523883, 'k8-fill'), ('0.74', '미국 시가', 475224, 'k8-open'),
        ('0.77', '글로벌 시가', 461400, 'k8-open'), ('0.82', '미국 장부', 440057, 'k8-open'),
        ('0.86', '글로벌 장부', 426839, 'k8-open'), ('1.00', '시장 평균', 378146, 'k8-open')]


def fig_apr_beta():
    base, ph = 192, 122.0 / 523883.0
    h = ['<svg viewBox="0 0 560 254" role="img" aria-label="에이피알 주당 내재가치는 베타 0.65에서 '
         '523,883원이고 베타 1.00이면 378,146원으로 현재가 367,000원에 가까워진다">']
    h.append(_t(26, 22, 't-head', '베타 가정별 주당 내재가치 (원)'))
    h.append(_line('k8-rule', 60, base, 534, base))
    for i, (b, src, v, cls) in enumerate(_APR):
        x = 84 + i * 74
        hg = v * ph
        h.append(_rect(cls, x, base - hg, 56, hg))
        h.append(_t(x + 28, base - hg - 9, 't-sub', '{:,}'.format(v), 'middle'))
        h.append(_t(x + 28, base + 17, 't-val', b, 'middle'))
        h.append(_t(x + 28, base + 34, 't-sub', src, 'middle'))
    y = base - 367000 * ph
    h.append(_line('k8-dash', 60, y, 534, y).replace('class="k8-dash"', 'class="k8-dash" style="stroke:var(--ink-3)"'))
    h.append(_t(536, y - 6, 't-step', '①', 'end'))
    h.append('</svg>')
    return ''.join(h)


FIG_APR_BETA = (
    2, '베타를 0.65에서 1.00으로 올리면 주당 내재가치가 현재가 근처까지 내려온다',
    fig_apr_beta(),
    '① 점선은 2026년 10월 1일 10시 49분 현재가 367,000원이다. 짙은 막대는 필자가 쓴 코스콤 2년 조정베타 기준이고, '
    '나머지는 업종 평균 베타(시가·장부 부채비율)와 시장 평균 베타로 바꾼 같은 모형의 결과다.')


# ── K4b 에이피알 — 기업가치 구성 ─────────────────────────────────────────
# 값은 [261001] 에이피알 편에 있는 것만(억원): 명시적 추정기간 FCF 현가 67,701 ·
# TV 현가 127,963 · EV 195,664 · TV 비중 65.4%
def fig_apr_ev():
    top, bot = 54, 214
    tv_h = (bot - top) * 0.654
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="에이피알 기업가치 195,664억원 가운데 '
         '영구가치 현가가 127,963억원으로 65.4퍼센트다">']
    h.append(_t(26, 22, 't-head', '기업가치(EV)를 이루는 두 부분'))
    h.append(_t(150, 44, 't-val', '100%', 'middle'))
    h.append(_rect('k8-fill', 100, top, 100, tv_h, 4))
    h.append(_rect('k8-open', 100, top + tv_h, 100, (bot - top) - tv_h, 4))
    # 지시선은 기둥 오른쪽 바깥으로 뺀다
    ym1 = top + tv_h / 2
    ym2 = top + tv_h + ((bot - top) - tv_h) / 2
    h.append(_line('k8-thin', 200, ym1, 244, ym1))
    h.append(_line('k8-thin', 200, ym2, 244, ym2))
    h.append(_t(252, ym1 - 2, 't-val', '65.4%'))
    h.append(_t(252, ym1 + 16, 't-sub', '영구가치(TV) 현가 127,963억원'))
    h.append(_t(252, ym1 + 32, 't-step', '①'))
    h.append(_t(252, ym2 - 2, 't-val', '34.6%'))
    h.append(_t(252, ym2 + 16, 't-sub', '2026~2035년 FCF 현가 67,701억원'))
    h.append(_t(252, ym2 + 32, 't-step', '②'))
    h.append(_t(150, bot + 22, 't-sub', 'EV 195,664억원', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_APR_EV = (
    4, '기업가치의 3분의 2가 추정기간 밖의 현금흐름이다',
    fig_apr_ev(),
    '① 2036년 이후 현금흐름을 영구성장률 2.5%로 이어 붙인 터미널밸류(TV)를 현재가치로 되돌린 것.<br>'
    '② 명시적 추정기간 10년의 FCF를 하나씩 할인해 더한 것. 34.6%는 원문 두 금액에서 구한 나머지 비율이다.')


# ── K5a 자사주 — 계획 물량 대비 취득 ─────────────────────────────────────
# 값은 [261002] 편에 있는 것만: 9월 20일 기준 삼성전자 74.69% · SK하이닉스 58.79% · 두 회사 투입 약 34.7조원
def fig_buyback():
    x0, wfull = 150, 360.0
    h = ['<svg viewBox="0 0 560 214" role="img" aria-label="9월 20일 기준 삼성전자는 계획 물량의 '
         '74.69퍼센트 SK하이닉스는 58.79퍼센트를 이미 샀다">']
    h.append(_t(26, 22, 't-head', '자사주 계획 물량 대비 취득 (9월 20일 기준)'))
    for i, (name, pct) in enumerate([('삼성전자', 74.69), ('SK하이닉스', 58.79)]):
        y = 66 + i * 56
        h.append(_t(26, y + 24, 't-step', name))
        h.append(_rect('k8-open', x0, y, wfull, 34, 5))
        h.append(_rect('k8-fill', x0, y, wfull * pct / 100.0, 34, 5))
        h.append(_t(x0 + wfull * pct / 100.0 - 8, y + 23, 't-val', '%.2f%%' % pct, 'end'))
    h.append(_t(x0 + wfull, 56, 't-step', '①', 'end'))
    h.append(_t(26, 192, 't-sub', '두 회사가 투입한 금액 합계 약 34.7조원'))
    h.append('</svg>')
    return ''.join(h)


FIG_BUYBACK = (
    2, '두 회사 모두 계획 물량의 절반을 넘게 샀다',
    fig_buyback(),
    '① 막대 오른쪽 끝이 이사회가 정한 계획 물량 전체(100%)다. 짙은 부분이 9월 20일까지 취득한 비율이다.')


# ── K5b 매수 주체 — 같은 꼴 두 줄 ────────────────────────────────────────
# 값은 [261002] 편 표에 있는 것만. 수급 흐름 세 마디가 두 길 모두 같은 순서다.
def fig_baton():
    h = ['<svg viewBox="0 0 560 226" role="img" aria-label="자사주 매입이 줄 때 외국인 순매수가 늘면 '
         '이상적인 길이고 외국인 매도가 이어지면 경계할 길이다">']
    h.append(_t(26, 22, 't-head', '자사주 매입이 줄어든 뒤의 수급 두 갈래'))
    xs = [150, 300, 430]
    heads = ['자사주', '기타법인', '외국인']
    for x, hd in zip(xs, heads):
        h.append(_t(x + 50, 52, 't-sub', hd, 'middle'))
    rows = [(66, '이상적', '①', ['매입 감소', '순매수 감소', '순매수 증가'], 'k8-fill'),
            (136, '경계', '②', ['매입 종료', '매수 급감', '매도 지속'], 'k8-dash')]
    for y, name, mark, cells, lastcls in rows:
        h.append(_t(26, y + 22, 't-step', name))
        h.append(_t(26, y + 40, 't-step', mark))
        for i, (x, c) in enumerate(zip(xs, cells)):
            cls = lastcls if i == 2 else 'k8-open'
            h.append(_rect(cls, x, y, 100, 44, 6))
            h.append(_t(x + 50, y + 27, 't-step', c, 'middle'))
        h.append(_arrow(xs[0] + 100, xs[1], y + 22))
        h.append(_arrow(xs[1] + 100, xs[2], y + 22))
    h.append('</svg>')
    return ''.join(h)


FIG_BATON = (
    5, '자사주가 줄 때 외국인이 받아 주는지가 갈림길이다',
    fig_baton(),
    '① 짙은 칸은 원문이 이상적 시나리오로 적은 끝이다. 실적을 보고 글로벌 투자자가 한국 반도체 비중을 늘리는 과정이다.<br>'
    '② 점선 칸은 경계 시나리오의 끝이다. 펀더멘털이 변하지 않았어도 수급 공백만으로 주가 조정이 가능하다.')


# ── K6a 삼성전자 — 주가와 목표주가, 영업이익과 눈높이 ────────────────────
# 값은 [261007] 편에 있는 것만: 주가 약 27만원 · 증권사 목표주가 평균 49만원 안팎 ·
# 3분기 영업이익 약 100조원 이상(이미 알려짐) · 시장 눈높이 105조~110조원 또는 그 이상(위 끝 110조)
def fig_gap():
    base = 186
    h = ['<svg viewBox="0 0 560 262" role="img" aria-label="삼성전자 주가 약 27만원과 증권사 목표주가 '
         '평균 49만원 안팎, 3분기 영업이익 약 100조원과 시장 눈높이 105조에서 110조원">']
    h.append(_t(26, 22, 't-head', '주가와 목표주가 (만원)'))
    h.append(_t(316, 22, 't-head', '3분기 영업이익 (조원)'))
    # 왼쪽
    ph = 130.0 / 49.0
    for i, (lab, v, vl, cls) in enumerate([('현재 주가', 27, '약 27', 'k8-open'),
                                           ('목표주가 평균', 49, '49 안팎', 'k8-fill')]):
        x = 56 + i * 104
        h.append(_rect(cls, x, base - v * ph, 70, v * ph))
        h.append(_t(x + 35, base - v * ph - 9, 't-val', vl, 'middle'))
        h.append(_t(x + 35, base + 17, 't-sub', lab, 'middle'))
    h.append(_t(150, base + 40, 't-step', '①', 'middle'))
    h.append(_line('k8-rule', 36, base, 262, base))
    # 오른쪽
    ph2 = 130.0 / 110.0
    for i, (lab, v, vl, cls) in enumerate([('이미 알려진', 100, '약 100 이상', 'k8-open'),
                                           ('시장 눈높이', 110, '105~110', 'k8-fill')]):
        x = 336 + i * 104
        h.append(_rect(cls, x, base - v * ph2, 70, v * ph2))
        h.append(_t(x + 35, base - v * ph2 - 9, 't-val', vl, 'middle'))
        h.append(_t(x + 35, base + 17, 't-sub', lab, 'middle'))
    h.append(_t(440, base + 40, 't-step', '②', 'middle'))
    h.append(_line('k8-rule', 316, base, 534, base))
    h.append('</svg>')
    return ''.join(h)


FIG_GAP = (
    2, '주가는 목표주가의 절반을 조금 넘고 영업이익은 이미 눈높이 근처다',
    fig_gap(),
    '① 목표주가는 증권사 평균이고, 원문이 49만원 안팎이라고 적었다.<br>'
    '② 눈높이는 원문이 105조~110조 또는 그 이상이라고 적었다. 막대 높이는 위 끝(110조)이다.')


# ── K6b 간밤 미국 AI 인프라 종목 ─────────────────────────────────────────
# 값은 [261007] 편에 있는 것만(%): Marvell 5.81 · Broadcom 3.67 · Amazon 1.95 · Oracle 1.61 ·
# Microsoft 0.78 · Apple 0.22 · Alphabet 0.22 · Nvidia 0.14 · ASML -1.39 · Micron -1.73
_US = [('Marvell', 5.81), ('Broadcom', 3.67), ('Amazon', 1.95), ('Oracle', 1.61),
       ('Microsoft', 0.78), ('Apple', 0.22), ('Alphabet', 0.22), ('Nvidia', 0.14),
       ('ASML', -1.39), ('Micron', -1.73)]


def fig_us():
    zx, k, top, rh = 232, 38.0, 44, 21
    h = ['<svg viewBox="0 0 560 292" role="img" aria-label="간밤 미국 AI 인프라 종목 등락률: '
         'Marvell 5.81퍼센트에서 Micron 마이너스 1.73퍼센트까지">']
    h.append(_t(26, 22, 't-head', '간밤 종목별 등락률 (%)'))
    for i, (name, v) in enumerate(_US):
        y = top + i * rh
        h.append(_t(104, y + 14, 't-sub', name, 'end'))
        w = abs(v) * k
        cls = 'k8-fill' if name == 'Micron' else 'k8-open'
        if v >= 0:
            h.append(_rect(cls, zx, y + 2, w, 15, 3))
            h.append(_t(zx + w + 6, y + 14, 't-sub', '+%.2f' % v))
        else:
            h.append(_rect(cls, zx - w, y + 2, w, 15, 3))
            h.append(_t(zx - w - 6, y + 14, 't-sub', '%.2f' % v, 'end'))
        if name == 'Micron':
            h.append(_t(zx + 14, y + 14, 't-step', '①'))
    ybot = top + len(_US) * rh + 6
    h.append(_line('k8-rule', zx, top - 2, zx, ybot))
    for v in (-2, 0, 2, 4, 6):
        x = zx + v * k
        h.append(_t(x, ybot + 18, 't-sub', '%d' % v, 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_US = (
    6, '간밤 미국에서 내린 종목은 Micron과 ASML 둘뿐이었다',
    fig_us(),
    '① 메모리 업체다. 열 종목 가운데 삼성전자·SK하이닉스와 같은 업종은 이 종목뿐이다.')
