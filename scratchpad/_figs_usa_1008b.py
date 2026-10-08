# -*- coding: utf-8 -*-
"""미주사 09-28~10-07 편 도해 열한 장 (카드 여섯).

  [260928] 디스퍼션   FIG_DISP_DAYS  평소 하루와 충격 하루, 같은 네 종목 (좌우 같은 꼴)
                     FIG_DISP_CHAIN 시장 충격 → 지수 옵션 되사기 → 청산 연쇄 (되돌아가는 선)
  [260930] 구글      FIG_GOOG_LAYERS AI 시장의 세 층과 Flash 자리
                     FIG_GOOG_LOOP   싸고 빠른 Flash → 호출 증가 → 가동률 → 수익
  [261002] 10년물    FIG_RATE_PATH   회사채 만기가 늦게 오고 기업마다 닿는 길이 다르다
                     FIG_RATE_YEARS  2022년과 2026년의 금리 충격 (좌우 같은 꼴)
  [261004] 엔비디아  FIG_NVDA_BUY    실제 매입액 막대 (2026회계연도 전체 / 2027회계연도 상반기)
                     FIG_NVDA_MONEY  돈이 들어오는 곳과 쓰는 곳
  [261005] TLTW/TLTP FIG_TLT_COVER   TLTP 자산 기둥 (옵션이 덮은 29% / 노출 71%)
                     FIG_TLT_SCEN    금리 경로별 필자의 선택
  [261007] 신고가    FIG_ATH_BARS    세계 시가총액 · 미국 · 외국인 보유 미국 증권
                     FIG_ATH_WAIT    기다림의 세 걸음

규칙(yohan-figure · docs/규칙 — 도해.md):
  - 원문에 없는 값은 안 그린다. 도형 개수와 높이도 값이다. TLTW의 커버 비율은 원문에 없어 안 그렸다.
    장기채 ETF의 47.8%(보유 TLT 기준)와 29%(필자가 찾은 실제 커버)는 기준이 달라 한 기둥에 안 섞었다.
  - 색은 회색만이다. 짙은 상자는 그림당 한 종류.
  - 판 위에는 이름과 값만 두고, 설명이 붙을 자리에는 ①②③만 얹는다. 풀이는 캡션이 한 줄씩.
  - 붓은 _figs_0825.FIG_CSS(t-head·t-step·t-sub·t-msg·t-day·t-val)와 card_lib.FIG_DEFS(화살촉)를 쓴다.
    상자 색은 이 파일이 style 로 직접 정한다(good-box·bad-box 는 초록·빨강이라 안 쓴다).
"""

# ── 붓 ───────────────────────────────────────────────────────────────────
_N = 'fill:rgba(127,127,127,.07);stroke:var(--ink-3);stroke-width:1.2'
_D = 'fill:rgba(127,127,127,.30);stroke:var(--ink-2);stroke-width:1.6'
_X = 'fill:rgba(127,127,127,.07);stroke:var(--ink-3);stroke-width:1.2;stroke-dasharray:4 4'
_BAR = 'fill:var(--ink-3);fill-fill-opacity:.5'
_AX = 'stroke:var(--ink-3);stroke-width:1'


def _svg(w, h, label):
    return ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (w, h, label)]


def _t(x, y, s, cls='t-sub', anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ''
    return '<text x="%s" y="%s" class="%s"%s>%s</text>' % (x, y, cls, a, s)


def _r(x, y, w, h, style=_N, rx=8):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%d" style="%s"/>' % (x, y, w, h, rx, style)


def _bar(x, y, w, h, op):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="2" '
            'style="fill:var(--ink-3);fill-opacity:%s"/>' % (x, y, w, h, op))


def _flow(x1, y1, x2, y2):
    return '<line class="flow" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (x1, y1, x2, y2)


def _path(d):
    return '<path d="%s" class="flow"/>' % d


def _cap(*lines):
    return '<br>'.join(lines)


# ── [260928] ① 평소의 하루와 충격이 온 하루 ───────────────────────────────
_DAY_OK = [('엔비디아', 5), ('금융주', -4), ('에너지', 6), ('소프트웨어', -7)]
_DAY_SHOCK = [('엔비디아', -8), ('금융주', -9), ('에너지', -7), ('소프트웨어', -10)]


def fig_disp_days():
    h = _svg(580, 236, '평소의 하루와 시장 전체를 치는 충격이 온 날, 같은 네 종목의 등락 예시')
    for px, head, rows, idx in [(20, '① 평소의 하루', _DAY_OK, 'OK'),
                                (300, '② 시장 전체를 치는 충격이 온 날', _DAY_SHOCK, 'SH')]:
        zero = px + 182
        h.append(_t(px, 30, head, 't-head'))
        h.append('<line x1="%d" y1="46" x2="%d" y2="200" style="%s"/>' % (zero, zero, _AX))
        for i, (name, v) in enumerate(rows):
            y = 58 + i * 34
            h.append(_t(px, y + 14, name, 't-msg'))
            w = abs(v) * 7
            if v > 0:
                h.append(_bar(zero, y, w, 18, '.45'))
                h.append(_t(zero + w + 5, y + 14, '+%d%%' % v, 't-sub'))
            else:
                h.append(_bar(zero - w, y, w, 18, '.7'))
                h.append(_t(zero - w - 5, y + 14, '%d%%' % v, 't-sub', 'end'))
        y = 58 + 4 * 34
        h.append(_t(px, y + 14, 'S&amp;P 500', 't-msg'))
        h.append(_t(zero + 12, y + 14,
                    '별 변화 없음' if idx == 'OK' else '크게 내린다', 't-step'))
    h.append('</svg>')
    return ''.join(h)


FIG_DISP_DAYS = (
    6, '같은 네 종목이 섞여 움직이는 날과 한꺼번에 내리는 날',
    fig_disp_days(),
    _cap('<b>①</b> 방향이 섞인 평소 하루의 예시. 지수는 별로 움직이지 않을 수 있다고 필자는 쓴다.',
         '<b>②</b> 시장 전체를 치는 충격이 온 날의 예시. 글은 소비주 -6%도 든다.',
         '막대는 오른쪽이 상승, 왼쪽이 하락이고 길이는 등락률에 비례한다. 등락률은 모두 필자의 설명용 가정이다.'))


# ── [260928] ② 청산이 청산을 부르는 길 ────────────────────────────────────
_CH = [
    (24, '시장 전체를', '치는 충격', _N),
    (170, '지수 옵션', '변동성 상승', _N),
    (316, '지수 옵션', '되사기', _D),
    (462, '다른 펀드', '위험한도 · 청산', _N),
]


def fig_disp_chain():
    h = _svg(580, 178, '시장 충격이 지수 옵션 변동성을 올리고 지수 옵션 되사기가 다른 펀드의 청산으로 이어지는 연쇄')
    for i, (x, a, b, st) in enumerate(_CH):
        h.append(_t(x + 59, 38, '①②③④'[i], 't-day', 'middle'))
        h.append(_r(x, 48, 118, 58, st, 9))
        h.append(_t(x + 59, 74, a, 't-step', 'middle'))
        h.append(_t(x + 59, 92, b, 't-sub', 'middle'))
        if i < len(_CH) - 1:
            h.append(_flow(x + 121, 77, x + 143, 77))
    h.append(_path('M521 108 V140 H375 V110'))
    h.append(_t(448, 134, '⑤', 't-day', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_DISP_CHAIN = (
    7, '지수 옵션을 되사려는 펀드가 몰리면 다음 펀드가 걸린다',
    fig_disp_chain(),
    _cap('<b>①</b> 금융불안·지정학 충격·경기침체 신호처럼 거의 모든 종목을 같은 쪽으로 움직이는 일',
         '<b>②</b> 종목 간 상관관계와 S&amp;P 500 하락이 지수 옵션의 변동성을 올린다',
         '<b>③</b> 팔아 둔 지수 옵션을 되사고 가진 개별 옵션을 판다. 짙은 상자가 여러 펀드가 한꺼번에 몰리는 자리다',
         '<b>④</b> 지수 옵션 가격이 더 올라 손실이 커진 펀드가 위험한도에 걸린다',
         '<b>⑤</b> 그 펀드도 포지션을 줄이며 지수 옵션을 되사서 ③으로 돌아간다'))


# ── [260930] ① AI 시장의 세 층 ────────────────────────────────────────────
_LAY = [
    (40, '①', 'frontier intelligence', 'GPT-6 Astra · Fable 5.1', _N),
    (112, '②', 'workhorse', 'Gemini Flash', _D),
    (184, '③', 'commodity inference', 'GLM · Qwen', _N),
]


def fig_goog_layers():
    h = _svg(580, 244, 'AI 시장의 세 층과 각 층에 앉은 모델, 아래에서 올라오는 중국 모델')
    h.append(_t(24, 26, '시장의 층', 't-head'))
    h.append(_t(306, 26, '그 자리의 모델', 't-head'))
    for y, n, layer, model, st in _LAY:
        h.append(_r(24, y, 250, 48, st, 9))
        h.append(_t(38, y + 30, n, 't-day'))
        h.append(_t(62, y + 30, layer, 't-step'))
        h.append(_r(306, y, 250, 48, st, 9))
        h.append(_t(431, y + 30, model, 't-step', 'middle'))
    h.append(_flow(431, 182, 431, 162))
    h.append(_t(446, 176, '④', 't-day'))
    h.append('</svg>')
    return ''.join(h)


FIG_GOOG_LAYERS = (
    7, '구글은 가운데 층을 노리고 아래에서 중국 모델이 올라온다',
    fig_goog_layers(),
    _cap('<b>①</b> 가장 어려운 코딩·연구·장기 에이전트 작업. 비싸도 제일 똑똑한 모델의 자리',
         '<b>②</b> 회사 문서 읽기·코딩·에이전트·검색·데이터 처리 대부분. 짙은 상자가 구글이 Flash를 넣으려는 자리다',
         '<b>③</b> 분류·요약·번역을 수없이 부르는 자리. 지능 2점보다 토큰 가격 50% 차이가 더 중요하다',
         '<b>④</b> 중국 모델이 아래에서 올라온다. 글은 5~7배 싸다고 하지만 대화체 대목의 수치이고 출처가 없다'))


# ── [260930] ② 호출이 늘면 가동률이 오른다 ────────────────────────────────
_LOOP = [
    ('Flash를', '싸고 빠르게', _N),
    ('AI를 붙일', '업무 증가', _N),
    ('호출 횟수', '증가', _N),
    ('데이터센터', '가동률 상승', _D),
    ('TPU · 클라우드', 'API 수익', _N),
]


def fig_goog_loop():
    h = _svg(580, 200, 'Flash가 싸지고 빨라지면 호출이 늘고 데이터센터 가동률과 구글의 수익원이 늘어나는 순서')
    for i, (a, b, st) in enumerate(_LOOP):
        x = 14 + 114 * i
        h.append(_t(x + 48, 34, '①②③④⑤'[i], 't-day', 'middle'))
        h.append(_r(x, 44, 96, 62, st, 9))
        h.append(_t(x + 48, 72, a, 't-step', 'middle'))
        h.append(_t(x + 48, 92, b, 't-sub', 'middle'))
        if i < len(_LOOP) - 1:
            h.append(_flow(x + 99, 75, x + 111, 75))
    h.append(_flow(518, 108, 518, 140))
    h.append(_r(300, 144, 256, 44, _N, 9))
    h.append(_t(314, 171, '⑥', 't-day'))
    h.append(_t(436, 171, '앤트로픽 약정 최소 1,111억 달러', 't-step', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_GOOG_LOOP = (
    8, 'Flash의 호출이 늘수록 구글의 데이터센터가 바빠진다',
    fig_goog_loop(),
    _cap('<b>①</b> Flash를 더 싸고 빠르게 만든다',
         '<b>②</b> 호출 한 번의 단가가 내려 AI를 안 붙이던 업무에도 붙는다(제번스 역설)',
         '<b>③</b> 검색·지메일·워크스페이스·기업 고객·개발자 API에서 호출이 는다',
         '<b>④</b> 지은 컴퓨팅 자원을 더 오래 돌린다. 짙은 상자가 필자가 CAPEX 회수의 핵심으로 보는 자리다',
         '<b>⑤</b> 같은 인프라를 TPU 판매·클라우드·API로 돈을 번다',
         '<b>⑥</b> 2026년 9월 공개 자료에 나온 장기 약정액'))


# ── [261002] ① 높은 금리가 기업에 닿는 길 ─────────────────────────────────
def fig_rate_path():
    h = _svg(580, 264, '미국 비금융기업 회사채의 만기와 기업 유형별로 달라지는 재조달 부담')
    h.append(_r(40, 34, 500, 52, _N, 9))
    h.append(_t(52, 56, '①', 't-day'))
    h.append(_t(290, 56, '미국 비금융기업 회사채, 2027~2031년 만기 약 4조3,000억 달러', 't-step', 'middle'))
    h.append(_t(290, 75, '2027년 약 5,720억 달러 → 2030년 약 1조300억 달러', 't-sub', 'middle'))
    h.append(_path('M290 88 V140 H167 V188'))
    h.append(_path('M290 140 H413 V188'))
    h.append(_r(52, 192, 230, 58, _N, 9))
    h.append(_t(60, 187, '②', 't-day'))
    h.append(_t(167, 216, '현금 많고 신용등급 높은 대기업', 't-step', 'middle'))
    h.append(_t(167, 235, '다시 빌릴 필요 없거나 비슷한 조건', 't-sub', 'middle'))
    h.append(_r(298, 192, 230, 58, _D, 9))
    h.append(_t(306, 187, '③', 't-day'))
    h.append(_t(413, 216, '부채 많고 신용등급 낮은 기업', 't-step', 'middle'))
    h.append(_t(413, 235, '2027~2028년 3% → 6%', 't-sub', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_RATE_PATH = (
    5, '회사채 만기가 나뉘어 오니 금리 충격도 기업마다 다르게 닿는다',
    fig_rate_path(),
    _cap('<b>①</b> 로이터가 LSEG 자료로 분석한 값을 필자가 옮겼다',
         '<b>②</b> 필자가 짚은 대기업의 재조달 조건',
         '<b>③</b> 3%에서 6%로 두 배 가까이 오른다는 것은 필자의 예상이다'))


# ── [261002] ② 2022년과 2026년의 금리 충격 ───────────────────────────────
_YR_ROWS = [
    ('출발점', ('제로금리에서', '빠르게 인상'), ('금리가 이미 높은 상태', '시장이 알고 있다')),
    ('시장이 본 것', ('인플레이션 급등',), ('기준금리 4%대에서도', '빅테크 · 반도체가 큰 이익')),
    ('금리 충격', ('저금리를 전제한 성장주', '밸류에이션이 한꺼번에 재계산'),
     ('버티는 기업과', '못 버티는 기업을 나눈다')),
]


def fig_rate_years():
    lx, lw, rx, rw = 128, 210, 358, 198
    h = _svg(580, 296, '2022년과 2026년의 금리 충격을 같은 세 항목으로 견준 것')
    h.append(_r(lx, 34, lw, 34, _N, 8))
    h.append(_t(lx + lw // 2, 56, '① 2022년', 't-step', 'middle'))
    h.append(_r(rx, 34, rw, 34, _D, 8))
    h.append(_t(rx + rw // 2, 56, '② 2026년', 't-step', 'middle'))
    for i, (lab, left, right) in enumerate(_YR_ROWS):
        y = 84 + i * 70
        h.append(_t(24, y + 32, lab, 't-head'))
        h.append(_r(lx, y, lw, 58, _N, 8))
        h.append(_r(rx, y, rw, 58, _N, 8))
        for j, line in enumerate(left):
            h.append(_t(lx + lw // 2, y + (24 if len(left) == 1 else 22) + j * 16, line, 't-sub', 'middle'))
        for j, line in enumerate(right):
            h.append(_t(rx + rw // 2, y + 22 + j * 16, line, 't-sub', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_RATE_YEARS = (
    8, '2022년에는 모든 성장주가 흔들렸고 2026년에는 기업이 나뉜다',
    fig_rate_years(),
    _cap('<b>①</b> 필자가 든 2022년의 모습',
         '<b>②</b> 필자가 든 2026년의 모습. 시장이 2023~2025년 실적을 본 뒤라는 전제다',
         '두 해를 이렇게 견주는 것은 필자의 해석이다.'))


# ── [261004] ① 실제 매입액 ────────────────────────────────────────────────
def fig_nvda_buy():
    base, sc = 232, .37
    h = _svg(580, 270, '엔비디아의 2026회계연도 전체와 2027회계연도 상반기 실제 자사주 매입액')
    h.append(_t(24, 28, '자사주 실제 매입액 (억 달러)', 't-head'))
    h.append('<line x1="60" y1="%d" x2="520" y2="%d" style="%s"/>' % (base, base, _AX))
    h1 = 404 * sc
    h.append(_bar(110, round(base - h1, 1), 110, round(h1, 1), '.55'))
    h.append(_t(165, round(base - h1 - 7, 1), '404', 't-val', 'middle'))
    q1, q2 = 202 * sc, 197 * sc
    h.append(_bar(310, round(base - q1, 1), 110, round(q1, 1), '.55'))
    h.append(_bar(310, round(base - q1 - q2 - 1, 1), 110, round(q2, 1), '.3'))
    h.append(_t(365, round(base - q1 - q2 - 8, 1), '398', 't-val', 'middle'))
    h.append(_t(432, round(base - q1 / 2 + 4, 1), '1분기 202', 't-sub'))
    h.append(_t(432, round(base - q1 - q2 / 2 + 3, 1), '2분기 197', 't-sub'))
    h.append(_t(165, 254, '① 2026회계연도 전체', 't-msg', 'middle'))
    h.append(_t(365, 254, '② 2027회계연도 상반기', 't-msg', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_NVDA_BUY = (
    2, '반년 만에 지난해 전체와 비슷한 금액을 샀다',
    fig_nvda_buy(),
    _cap('<b>①</b> 2026회계연도 전체 매입액',
         '<b>②</b> 2027회계연도 상반기 매입액. 1분기와 2분기를 쌓았다',
         '막대 높이는 금액에 비례한다. 출처는 엔비디아 SEC 공시를 필자가 옮긴 것이다.'))


# ── [261004] ② 돈이 들어오는 곳과 쓰는 곳 ─────────────────────────────────
def fig_nvda_money():
    h = _svg(580, 176, '빅테크의 투자 예산이 엔비디아 매출이 되고 번 돈이 연구개발과 자사주 매입으로 가는 순서')
    h.append(_r(24, 60, 170, 70, _N, 9))
    h.append(_t(109, 82, '마이크로소프트 · 메타', 't-step', 'middle'))
    h.append(_t(109, 100, '아마존 · 구글', 't-step', 'middle'))
    h.append(_t(109, 119, '데이터센터 투자 예산', 't-sub', 'middle'))
    h.append(_flow(198, 95, 240, 95))
    h.append(_t(219, 86, '①', 't-day', 'middle'))
    h.append(_r(244, 60, 130, 70, _N, 9))
    h.append(_t(309, 91, '엔비디아', 't-step', 'middle'))
    h.append(_t(309, 111, '매출 · 이익', 't-sub', 'middle'))
    h.append(_path('M378 95 H400 V54 H430'))
    h.append(_path('M400 95 V136 H430'))
    h.append(_t(394, 86, '②', 't-day', 'end'))
    h.append(_r(434, 30, 132, 48, _N, 9))
    h.append(_t(500, 59, '연구개발 · 설비투자', 't-step', 'middle'))
    h.append(_r(434, 112, 132, 48, _D, 9))
    h.append(_t(500, 141, '자사주 매입', 't-step', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_NVDA_MONEY = (
    7, '자사주 매입은 번 돈이 가는 곳만 바꾼다',
    fig_nvda_money(),
    _cap('<b>①</b> 매출이 나오는 곳. 필자가 든 고객은 마이크로소프트·메타·아마존·구글이다',
         '<b>②</b> 번 돈이 가는 곳. 짙은 상자가 이번 발표의 대상이다'))


# ── [261005] ① TLTP 자산 기둥 ─────────────────────────────────────────────
def fig_tlt_cover():
    top, H = 58, 180
    h1 = round(H * .29, 1)
    h = _svg(580, 272, 'TLTP 자산 중 콜옵션이 덮은 약 29%와 덮이지 않은 약 71%')
    h.append(_t(24, 28, 'TLTP 자산 (필자가 찾은 실제 커버)', 't-head'))
    h.append(_t(240, 50, '100%', 't-val', 'middle'))
    h.append(_r(200, top, 80, h1, _D, 3))
    h.append(_r(200, round(top + h1, 1), 80, round(H - h1, 1), _N, 3))
    h.append(_t(298, round(top + h1 / 2 + 5, 1), '① 옵션을 판 부분 29%', 't-step'))
    h.append(_t(298, round(top + h1 + (H - h1) / 2 + 5, 1), '② 노출된 부분 71%', 't-step'))
    h.append(_t(240, 262, 'TLTP', 't-msg', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_TLT_COVER = (
    6, 'TLTP는 자산의 약 29%에만 옵션을 걸어 놓았다',
    fig_tlt_cover(),
    _cap('<b>①</b> 콜옵션을 팔아 상승 수익을 포기한 부분. 필자가 「찾아보니」라고만 적은 값이고 계산 근거는 원문에 없다',
         '<b>②</b> 제한 없이 채권 가격 상승에 참여하는 부분',
         '기둥 높이는 100%이다. TLTW의 비율은 원문에 없어 그리지 않았다.'))


# ── [261005] ② 금리 경로별 선택 ───────────────────────────────────────────
_SC = [
    ('계속 오른다', 'TLTW', _N),
    ('횡보', 'TLTW', _D),
    ('천천히 하락', '애매', _X),
    ('빠르게 하락', 'TLTP', _N),
    ('폭락 확신', 'TLT', _N),
]


def fig_tlt_scen():
    h = _svg(580, 190, '금리가 어떻게 움직이느냐에 따라 필자가 고른 TLT·TLTW·TLTP')
    h.append(_t(16, 22, '금리가', 't-head'))
    for i, (sc, pick, st) in enumerate(_SC):
        x = 16 + 112 * i
        if i == 1:
            h.append(_t(x + 50, 38, '①', 't-day', 'middle'))
        h.append(_r(x, 46, 100, 44, _N, 9))
        h.append(_t(x + 50, 73, sc, 't-step', 'middle'))
        h.append(_flow(x + 50, 92, x + 50, 124))
        h.append(_r(x, 128, 100, 44, st, 9))
        h.append(_t(x + 50, 155, pick, 't-step', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_TLT_SCEN = (
    7, '금리가 횡보하면 TLTW, 빠르게 내리면 TLTP',
    fig_tlt_scen(),
    _cap('<b>①</b> 필자가 가장 유력하게 보는 경로. 점선 상자는 필자가 애매하다고 한 자리다',
         '위 칸은 금리가 밟는 경로, 아래 칸은 그 경로에서 필자가 고른 상품이다.'))


# ── [261007] ① 세계 시가총액과 미국 ───────────────────────────────────────
_ATH = [
    ('세계 주식시장', '시가총액', 157.8, '157.8조', '①', '.3'),
    ('미국 주식시장', '시가총액', 68.9, '68.9조 (43.7%)', '②', '.55'),
    ('외국인 보유', '미국 증권', 35.3, '35.3조', '③', '.55'),
    ('그중', '미국주식', 19.9, '19.9조', '④', '.3'),
    ('그중', '장기채', 13.8, '13.8조', '⑤', '.3'),
]


def fig_ath_bars():
    base, sc = 214, 1.0
    h = _svg(580, 270, '세계 주식시장 시가총액, 미국 비중, 외국인이 보유한 미국 증권의 크기')
    h.append(_t(24, 24, '조 달러', 't-head'))
    h.append('<line x1="20" y1="%d" x2="560" y2="%d" style="%s"/>' % (base, base, _AX))
    for i, (a, b, v, lab, n, op) in enumerate(_ATH):
        cx = 76 + 107 * i
        hh = round(v * sc, 1)
        h.append(_bar(cx - 32, round(base - hh, 1), 64, hh, op))
        h.append(_t(cx, round(base - hh - 8, 1), lab, 't-val' if i < 3 else 't-msg', 'middle'))
        h.append(_t(cx, 233, n + ' ' + a, 't-msg', 'middle'))
        h.append(_t(cx, 251, b, 't-sub', 'middle'))
    h.append('</svg>')
    return ''.join(h)


FIG_ATH_BARS = (
    6, '미국 시장은 세계 주식시장의 43.7%이고 외국인도 이만큼 들고 있다',
    fig_ath_bars(),
    _cap('<b>①</b> SIFMA 집계, 2025년',
         '<b>②</b> 같은 자료. 괄호는 세계 시가총액에서 미국의 비중',
         '<b>③</b> 미국 재무부 자료, 2025년 6월 말',
         '<b>④⑤</b> ③의 두 구성. 둘을 합쳐도 ③에 못 미치고 나머지는 원문에 없다',
         '막대 높이는 금액에 비례한다.'))


# ── [261007] ② 기다림의 세 걸음 ───────────────────────────────────────────
_WAIT = [
    ('신고가', '20,000 → 22,000'),
    ('10% 조정', '20,000 → 18,000'),
    ('반등', '또 놓친다'),
]


def fig_ath_wait():
    h = _svg(580, 138, '신고가와 조정과 반등에서 매수를 계속 미루게 되는 세 걸음')
    for i, (a, b) in enumerate(_WAIT):
        x = 24 + 190 * i
        h.append(_t(x + 75, 30, '①②③'[i], 't-day', 'middle'))
        h.append(_r(x, 42, 150, 62, _D if i == 1 else _N, 9))
        h.append(_t(x + 75, 70, a, 't-step', 'middle'))
        h.append(_t(x + 75, 90, b, 't-sub', 'middle'))
        if i < 2:
            h.append(_flow(x + 154, 73, x + 186, 73))
    h.append('</svg>')
    return ''.join(h)


FIG_ATH_WAIT = (
    8, '조정을 기다려도 살 이유는 다시 사라진다',
    fig_ath_wait(),
    _cap('<b>①</b> 신고가라서 너무 비싸다고 느껴 사지 않는다',
         '<b>②</b> 이유가 있는 하락이라 더 떨어질까 봐 또 사지 않는다. 짙은 상자가 필자가 짚은 함정이다',
         '<b>③</b> 시장이 반등하면 또 놓친다',
         '나스닥 수치는 필자가 든 가정의 예시이다.'))


ALL = [FIG_DISP_DAYS, FIG_DISP_CHAIN, FIG_GOOG_LAYERS, FIG_GOOG_LOOP,
       FIG_RATE_PATH, FIG_RATE_YEARS, FIG_NVDA_BUY, FIG_NVDA_MONEY,
       FIG_TLT_COVER, FIG_TLT_SCEN, FIG_ATH_BARS, FIG_ATH_WAIT]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
