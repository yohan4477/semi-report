# -*- coding: utf-8 -*-
"""회계사 카드 도해 — 2026-10-06~08 일곱 편(엘곰·방구퐁).

  재건축 1+1      F_ACQ 취득가액 막대 · F_INHERIT 새 아파트가 옛집에서 이어받는 것
  선박왕 체납     F_SHIPNUM 숫자 셋 막대 · F_SERVE 송달 두 장면
  1873년 철도     F_RAIL 세 단계 · F_TIMING 현금흐름 시점
  미국 증시       F_CHAIN 유가에서 할인율까지 · F_DRAM DRAM 가격 상승률
  AI 에이전트     F_THREE 책임안 셋
  AI 속도조절론   F_WHERE 사고가 난 곳
  삼성전자 3분기  F_OI 영업이익 컨센서스와 Bear · F_PRICE 주가와 DCF 두 가지

규칙(yohan-figure · 규칙 — 도해): 원문에 있는 값만, 색은 회색만, 판 위 글자는 값 라벨과
이름뿐이고 설명이 붙을 자리는 번호만, 캡션은 번호 풀이. 배치는 scratchpad/check_fig.py.
"""

CSS = """
  .uc-fig .k10-fill { fill:rgba(127,127,127,.20); stroke:var(--ink-3); stroke-width:1.3; }
  .uc-fig .k10-open { fill:rgba(127,127,127,.06); stroke:var(--line); stroke-width:1.2; }
  .uc-fig .k10-dash { fill:none; stroke:var(--line); stroke-width:1.2; stroke-dasharray:4 4; }
  .uc-fig .k10-rule { stroke:var(--ink-3); stroke-width:1.2; }
  .uc-fig .k10-thin { stroke:var(--line); stroke-width:1; }
  .uc-fig .k10-arr  { stroke:var(--ink-3); stroke-width:1.6; fill:none; marker-end:url(#k10-arrow); }
"""

_DEFS = ('<defs><marker id="k10-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
         'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
         'fill="var(--ink-3,#8a8a8a)"/></marker></defs>')


def _t(x, y, cls, s, anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ''
    return '<text x="%s" y="%s" class="%s"%s>%s</text>' % (x, y, cls, a, s)


def _svg(w, h, aria, body, defs=False):
    return ('<svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s</svg>'
            % (w, h, aria, _DEFS if defs else '', ''.join(body)))


# ── 재건축 ① 취득가액 막대 ─────────────────────────────────────────────────
# 값은 [261006] 재건축 편에 있는 것만: 큰 집 분양가 5억5천만원·취득가액 약 1억9,298만원,
# 작은 집 분양가 5억원·취득가액 약 4억8,702만원. 높이는 억 단위 수치에 비례한다.
def fig_acq():
    base, ph = 214, 150.0 / 5.5
    h = [_t(26, 22, 't-head', '계약서의 분양가와 세법이 보는 취득가액')]
    h.append('<line class="k10-rule" x1="26" y1="%d" x2="534" y2="%d"/>' % (base, base))
    bars = [(80, '분양가', 5.5, 'k10-open', '5억5천만원'),
            (205, '취득가액 ①', 1.9298, 'k10-fill', '약 1억9,298만원'),
            (355, '분양가', 5.0, 'k10-open', '5억원'),
            (480, '취득가액 ②', 4.8702, 'k10-fill', '약 4억8,702만원')]
    for cx, name, v, cls, lab in bars:
        hh = v * ph
        h.append('<rect class="%s" x="%d" y="%.1f" width="64" height="%.1f" rx="5"/>'
                 % (cls, cx - 32, base - hh, hh))
        h.append(_t(cx, '%.1f' % (base - hh - 9), 't-step', lab, 'middle'))
        h.append(_t(cx, base + 18, 't-sub', name, 'middle'))
    h.append(_t(142, base + 42, 't-step', '큰 집', 'middle'))
    h.append(_t(417, base + 42, 't-step', '작은 집', 'middle'))
    return _svg(560, 270, '재건축 1+1으로 받은 큰 집은 분양가 5억5천만원인데 취득가액은 약 1억9,298만원이고 '
                '작은 집은 분양가 5억원에 취득가액 약 4억8,702만원이다', h)


F_ACQ = (
    2, '큰 집의 취득가액은 계약서 분양가보다 약 3억5,702만원 적다',
    fig_acq(),
    '막대 높이는 금액에 비례한다. 왼쪽 옅은 막대가 계약서의 분양가, 짙은 막대가 세법이 보는 취득가액이다. '
    '<br>① 옛집 원가를 옛집 평가액 가운데 큰 집에 들어간 금액의 비율로 나눈 금액'
    '<br>② 옛집 원가에서 나눈 작은 금액에 현금으로 더 낸 금액을 더한 금액'
    '<br>(기획재정부 재산세제과-627, 2023.5.2. 회신의 재개발 사례)')


# ── 재건축 ② 새 아파트가 옛집에서 이어받는 것 ──────────────────────────────
def fig_inherit():
    h = [_t(26, 22, 't-head', '새 아파트가 옛집에서 이어받는 것')]
    h.append('<rect class="k10-open" x="26" y="42" width="130" height="150" rx="8"/>')
    h.append(_t(91, 112, 't-step', '옛집', 'middle'))
    h.append(_t(91, 134, 't-sub', '헐린 집', 'middle'))
    rows = [(46, '① 취득가액', 'k10-fill', True), (100, '② 보유기간', 'k10-fill', True),
            (154, '③ 한 채라는 신분', 'k10-dash', False)]
    for y, name, cls, solid in rows:
        cy = y + 16
        h.append('<rect class="%s" x="300" y="%d" width="234" height="32" rx="6"/>' % (cls, y))
        h.append(_t(316, cy + 5, 't-step', name))
        if solid:
            h.append('<line class="k10-arr" x1="156" y1="%d" x2="298" y2="%d"/>' % (cy, cy))
        else:
            h.append('<line class="k10-thin" x1="156" y1="%d" x2="298" y2="%d" stroke-dasharray="4 4"/>'
                     % (cy, cy))
    return _svg(560, 212, '새 아파트는 옛집에서 취득가액과 보유기간을 이어받지만 한 채라는 신분은 '
                '이어받지 못한다', h, defs=True)


F_INHERIT = (
    7, '취득가액과 보유기간은 이어지고 한 채라는 신분은 파는 날마다 따로 확인한다',
    fig_inherit(),
    '실선은 이어받는 것, 점선은 이어받지 못하는 것이다.'
    '<br>① 옛집 원가를 두 집에 나눠 받는다'
    '<br>② 옛집에서 이어진 부분은 옛집 취득일부터, 청산금 부분은 관리처분계획 인가일부터 센다'
    '<br>③ 양도일 현재 그 세대가 가진 주택 수로 따로 판정한다(소득세법 시행령 제154조)')


# ── 선박왕 ① 숫자 셋 ────────────────────────────────────────────────────
# 값은 [261007] 선박왕 편에 있는 것만: 1,000억 · 3,938억 · 7,902억원
def fig_shipnum():
    base, ph = 218, 150.0 / 7902
    h = [_t(26, 22, 't-head', '체납 발표에 나온 세 금액')]
    h.append('<line class="k10-rule" x1="26" y1="%d" x2="534" y2="%d"/>' % (base, base))
    bars = [(100, 1000, 'k10-fill', '1,000억원', '실제 들어온 현금 ①'),
            (280, 3938, 'k10-open', '3,938억원', '개인 체납액 ②'),
            (460, 7902, 'k10-open', '7,902억원', '법인 지정액을 더한 합계 ③')]
    for cx, v, cls, lab, name in bars:
        hh = v * ph
        h.append('<rect class="%s" x="%d" y="%.1f" width="84" height="%.1f" rx="5"/>'
                 % (cls, cx - 42, base - hh, hh))
        h.append(_t(cx, '%.1f' % (base - hh - 9), 't-val', lab, 'middle'))
    h.append(_t(100, base + 20, 't-sub', '실제 들어온 현금 ①', 'middle'))
    h.append(_t(280, base + 20, 't-sub', '개인 체납액 ②', 'middle'))
    h.append(_t(460, base + 20, 't-sub', '법인 지정액을 더한', 'middle'))
    h.append(_t(460, base + 36, 't-sub', '합계 ③', 'middle'))
    return _svg(560, 262, '선박왕 체납 발표의 세 금액은 실제 들어온 현금 1,000억원, 개인 체납액 3,938억원, '
                '관련 법인 지정액을 더한 합계 7,902억원이다', h)


F_SHIPNUM = (
    2, '세 금액은 같은 세금을 다른 방식으로 센 것이다',
    fig_shipnum(),
    '막대 높이는 금액에 비례한다.'
    '<br>① 7월 말 실제로 국고에 들어온 돈'
    '<br>② 1,000억원을 포함하고, 나머지는 납부계획과 담보 단계에 있다'
    '<br>③ ②에 관련 법인들의 제2차 납세의무 지정액을 더한 체납 명부상 합계. 어느 법인에 얼마가 지정됐는지는 공개 자료에 없다')


# ── 선박왕 ② 송달 두 장면 ───────────────────────────────────────────────
def fig_serve():
    h = [_t(26, 22, 't-head', '고지서 송달을 두고 법원이 본 두 장면')]
    h.append('<rect class="k10-dash" x="26" y="42" width="244" height="124" rx="8"/>')
    h.append(_t(42, 68, 't-step', '① 2012년 12월 21일'))
    h.append(_t(42, 92, 't-sub', '출입이 통제되는 건물'))
    h.append(_t(42, 110, 't-sub', '안내데스크 근무자에게 맡김'))
    h.append(_t(42, 144, 't-step', '법원 판단: 송달 무효'))
    h.append('<rect class="k10-fill" x="290" y="42" width="244" height="124" rx="8"/>')
    h.append(_t(306, 68, 't-step', '② 2013년 2월'))
    h.append(_t(306, 92, 't-sub', '서울구치소장에게 교부'))
    h.append(_t(306, 110, 't-sub', '다음 날 본인은 수령 거부'))
    h.append(_t(306, 144, 't-step', '법원 판단: 송달 적법'))
    return _svg(560, 188, '같은 납세자에게 보낸 고지서가 안내데스크에서는 송달 무효, 서울구치소장에게 교부한 '
                '때는 송달 적법으로 판단됐다', h)


F_SERVE = (
    3, '고지서가 건물 안까지 들어가도 법적으로는 도착하지 않을 수 있다',
    fig_serve(),
    '점선 상자는 무효로 본 장면, 짙은 상자는 적법으로 본 장면이다.'
    '<br>① 안내데스크 근무자가 납세자를 대신해 서류를 받을 권한을 위임받았다는 증거가 없다는 이유'
    '<br>② 수감 중인 사람에게는 구치소가 서류를 받는 장소가 될 수 있다는 판단'
    '<br>(참고자료에 오른 서울고등법원 2022. 6. 21. 선고 2021누21 판결문의 사실관계)')


# ── 1873년 철도 ① 세 단계 ────────────────────────────────────────────────
def fig_rail():
    h = [_t(26, 22, 't-head', 'AI 산업혁명의 세 단계')]
    xs = [26, 202, 378]
    heads = [('① 인프라 투자', 'k10-fill'), ('② 본격 활용', 'k10-open'), ('③ 널리 보급', 'k10-open')]
    subs = [('GPU · HBM · 데이터센터', '전력설비'),
            ('반복 업무 자동화', 'AI Agent 도입'),
            ('안정적인 현금흐름', '')]
    for x, (hd, cls), (s1, s2) in zip(xs, heads, subs):
        h.append('<rect class="%s" x="%d" y="46" width="156" height="92" rx="8"/>' % (cls, x))
        h.append(_t(x + 14, 76, 't-step', hd))
        h.append(_t(x + 14, 102, 't-sub', s1))
        if s2:
            h.append(_t(x + 14, 120, 't-sub', s2))
    for x in (182, 358):
        h.append('<line class="k10-arr" x1="%d" y1="92" x2="%d" y2="92"/>' % (x, x + 18))
    h.append('<line class="k10-thin" x1="104" y1="166" x2="456" y2="166" stroke-dasharray="4 4"/>')
    h.append(_t(280, 186, 't-sub', '시간차', 'middle'))
    return _svg(560, 204, 'AI 산업혁명은 인프라 투자, 본격 활용, 널리 보급의 세 단계로 오고 단계 사이에 '
                '시간차가 있다', h, defs=True)


F_RAIL = (
    7, '투자가 먼저 오고 안정적인 현금흐름은 마지막에 온다',
    fig_rail(),
    '짙은 상자는 필자가 지금 시장이 있을 가능성이 있다고 본 구간이다.'
    '<br>① 첫 단계에서는 기술에 대한 기대가 실제 수익보다 앞설 수 있다'
    '<br>② 생산성 개선이 실제로 나타나는 단계'
    '<br>③ 산업 전반에 보급된 뒤 안정적인 현금흐름이 나온다')


# ── 1873년 철도 ② 현금흐름 시점 ───────────────────────────────────────────
# 값은 [261007] 철도 편에 있는 것만: 3년 뒤로 예상 → 6년이나 8년 뒤
def fig_timing():
    x0, unit = 70, 54.0
    h = [_t(26, 22, 't-head', '같은 현금흐름이 나오는 시점')]
    for yrs in (3, 6, 8):
        x = x0 + yrs * unit
        h.append('<line class="k10-thin" x1="%.0f" y1="44" x2="%.0f" y2="150"/>' % (x, x))
        h.append(_t('%.0f' % x, 170, 't-sub', '%d년 뒤' % yrs, 'middle'))
    h.append('<line class="k10-rule" x1="%d" y1="86" x2="534" y2="86"/>' % x0)
    h.append('<line class="k10-rule" x1="%d" y1="126" x2="534" y2="126"/>' % x0)
    h.append(_t(26, 60, 't-step', '① 시장이 예상한 시점'))
    h.append(_t(26, 106, 't-step', '② 늦어진 시점'))
    x3 = x0 + 3 * unit
    h.append('<circle class="k10-fill" cx="%.0f" cy="86" r="9"/>' % x3)
    for yrs in (6, 8):
        h.append('<circle class="k10-open" cx="%.0f" cy="126" r="9"/>' % (x0 + yrs * unit))
    return _svg(560, 190, '현금흐름이 3년 뒤로 예상됐는데 6년 뒤나 8년 뒤로 늦어지는 경우를 견준 시간축', h)


F_TIMING = (
    4, '3년 뒤로 예상한 현금흐름이 6년이나 8년 뒤로 늦어진다',
    fig_timing(),
    '① 시장이 기대한 시점. 원문이 든 예시다'
    '<br>② 같은 현금흐름이 늦어진 두 경우. 원문은 6년 뒤 또는 8년 뒤를 든다'
    '<br>눈금은 연 단위이고 크기는 그리지 않았다')


# ── 미국 증시 ① 유가에서 할인율까지 ────────────────────────────────────────
def fig_chain():
    h = [_t(26, 22, 't-head', '유가가 주가 평가에 닿는 경로')]
    labels = ['① 브렌트유 배럴당 100달러 넘음', '② 물가가 쉽게 안 내려옴', '③ 연준이 금리를 내리기 어려움',
              '④ 10년물 5.3% 안팎 · 30년물 5.7% 접근', '⑤ 미래 현금흐름의 할인율 상승']
    for i, lab in enumerate(labels):
        y = 40 + i * 54
        cls = 'k10-fill' if i in (0, 3) else 'k10-open'
        h.append('<rect class="%s" x="110" y="%d" width="340" height="36" rx="6"/>' % (cls, y))
        h.append(_t(126, y + 23, 't-step', lab))
        if i < 4:
            h.append('<line class="k10-arr" x1="280" y1="%d" x2="280" y2="%d"/>' % (y + 36, y + 54))
    return _svg(560, 296, '브렌트유 100달러 돌파가 물가와 연준 금리 경로를 거쳐 장기금리와 할인율 상승으로 '
                '이어진다', h, defs=True)


F_CHAIN = (
    4, '유가는 비용을 올리면서 금리도 높게 묶는다',
    fig_chain(),
    '짙은 상자는 원문이 수치를 적은 곳이다.'
    '<br>① 중동 지정학 불안과 에너지 공급 차질 우려'
    '<br>② 운송비와 제조원가가 오르고 소비자의 실질구매력이 약해진다'
    '<br>③ 시장이 추가 긴축 가능성까지 다시 따져야 한다'
    '<br>④ 장기금리가 5%를 훨씬 넘는 환경'
    '<br>⑤ 이익 전망이 올라도 주가 상승으로 그대로 이어지지 않을 수 있다')


# ── 미국 증시 ② 일반 DRAM 가격 상승률 ─────────────────────────────────────
# 값은 [261007] 미 증시 편에 있는 것만: 2분기 약 60%, 3분기 10~15%(Reuters 전망 인용)
def fig_dram():
    base, ph = 200, 150.0 / 60
    h = [_t(26, 22, 't-head', '일반 DRAM 가격 상승률')]
    h.append('<line class="k10-rule" x1="60" y1="%d" x2="500" y2="%d"/>' % (base, base))
    h.append('<rect class="k10-fill" x="130" y="%.1f" width="90" height="%.1f" rx="5"/>'
             % (base - 60 * ph, 60 * ph))
    h.append(_t(175, '%.1f' % (base - 60 * ph - 9), 't-val', '약 60%', 'middle'))
    h.append(_t(175, base + 18, 't-sub', '2분기', 'middle'))
    h.append('<rect class="k10-fill" x="330" y="%.1f" width="90" height="%.1f" rx="5"/>'
             % (base - 10 * ph, 10 * ph))
    h.append('<rect class="k10-dash" x="330" y="%.1f" width="90" height="%.1f" rx="5"/>'
             % (base - 15 * ph, 5 * ph))
    h.append(_t(375, '%.1f' % (base - 15 * ph - 9), 't-val', '10~15%', 'middle'))
    h.append(_t(375, base + 18, 't-sub', '3분기 전망 ①', 'middle'))
    return _svg(560, 232, '일반 DRAM 가격 상승률이 2분기 약 60%에서 3분기 10~15%로 둔화될 것이라는 전망', h)


F_DRAM = (
    8, '일반 DRAM 가격 상승률이 2분기 약 60%에서 3분기 10~15%로 둔화될 것으로 본다',
    fig_dram(),
    '막대 높이는 상승률에 비례한다.'
    '<br>① 필자가 인용한 Reuters 전망. 점선 구간은 10%에서 15% 사이의 범위다')


# ── AI 에이전트 책임 ① 규제안 셋 ──────────────────────────────────────────
def fig_three():
    h = [_t(26, 22, 't-head', '일부 의원과 활동가가 내놓은 규제안')]
    xs = [26, 205, 384]
    names = [('① 보고 의무', 'k10-open'), ('② 독립 감사', 'k10-open'), ('③ 범죄 기준의 책임', 'k10-fill')]
    for x, (nm, cls) in zip(xs, names):
        h.append('<rect class="%s" x="%d" y="46" width="150" height="70" rx="8"/>' % (cls, x))
        h.append(_t(x + 75, 87, 't-step', nm, 'middle'))
    return _svg(560, 132, 'AI 에이전트 사고의 책임을 두고 보고 의무, 독립 감사, 범죄 기준의 책임 세 규제안이 '
                '나온다', h)


F_THREE = (
    7, '세 규제안 가운데 범죄 기준의 책임이 가장 세다',
    fig_three(),
    '짙은 상자가 원문이 셋 중 가장 세다고 쓴 안이다.'
    '<br>① AI 모델이 사람의 감독을 피하거나 시스템을 뚫으면 회사가 신고한다. 지금은 공시가 회사 재량이다'
    '<br>② 회사가 스스로 안전하다고 말하게 두지 않고 외부 제3자가 점검한다'
    '<br>③ 사람이 했다면 범죄가 될 행동을 AI 모델이 하면 그 회사가 책임진다')


# ── AI 속도조절론 ① 사고가 난 곳 ───────────────────────────────────────────
def fig_where():
    h = [_t(26, 22, 't-head', '국내 금융권 개인정보 유출이 난 곳')]
    h.append('<rect class="k10-open" x="26" y="46" width="190" height="170" rx="8"/>')
    h.append(_t(121, 118, 't-step', '① 핵심 시스템', 'middle'))
    h.append(_t(121, 140, 't-sub', '인터넷뱅킹 같은 곳', 'middle'))
    h.append(_t(300, 56, 't-sub', '② 관리가 상대적으로 느슨한 주변부'))
    for i, nm in enumerate(['대출모집인 조회 서비스', '직원 업무지원시스템', '영업지원시스템', '외주 개발 영역']):
        y = 68 + i * 40
        h.append('<rect class="k10-fill" x="300" y="%d" width="234" height="32" rx="6"/>' % y)
        h.append(_t(316, y + 21, 't-step', nm))
    return _svg(560, 236, '국내 금융권 개인정보 유출은 인터넷뱅킹 같은 핵심 시스템보다 대출모집인 조회 서비스, '
                '직원 업무지원시스템, 영업지원시스템, 외주 개발 영역 같은 주변부에서 났다', h)


F_WHERE = (
    1, '유출이 난 곳은 핵심 시스템보다 주변부였다',
    fig_where(),
    '① 원문이 사고 지점으로 꼽지 않은 쪽이다'
    '<br>② 원문이 든 네 영역. 뒤에 「등」이 붙어 이 밖에도 있다는 뜻이다'
    '<br>피해 규모와 회사 이름은 원문에 없어 그리지 않았다')


# ── 삼성전자 3분기 ① 영업이익 컨센서스와 Bear ────────────────────────────────
# 값은 [261008] 삼성전자 편에 있는 것만: 컨센서스 381·547·587조, Bear 2027 480조·2028 450조
def fig_oi():
    base, ph = 212, 150.0 / 587
    h = [_t(26, 22, 't-head', '영업이익 컨센서스와 Bear Case 가정')]
    h.append('<line class="k10-rule" x1="26" y1="%d" x2="534" y2="%d"/>' % (base, base))
    bars = [(100, 381, 'k10-fill', '컨센서스'),
            (232, 547, 'k10-fill', '컨센서스'), (306, 480, 'k10-open', 'Bear'),
            (424, 587, 'k10-fill', '컨센서스'), (498, 450, 'k10-open', 'Bear')]
    for cx, v, cls, nm in bars:
        hh = v * ph
        h.append('<rect class="%s" x="%d" y="%.1f" width="54" height="%.1f" rx="5"/>'
                 % (cls, cx - 27, base - hh, hh))
        h.append(_t(cx, '%.1f' % (base - hh - 8), 't-sub', '%d조원' % v, 'middle'))
        h.append(_t(cx, base + 17, 't-sub', nm, 'middle'))
    for cx, yr in ((100, '2026년'), (269, '2027년'), (461, '2028년')):
        h.append(_t(cx, base + 40, 't-step', yr, 'middle'))
    return _svg(560, 262, 'Bear Case는 2027년 영업이익 컨센서스 547조원을 480조원으로, 2028년 587조원을 '
                '450조원으로 낮췄다', h)


F_OI = (
    3, 'Bear Case는 2027년 547조원을 480조원으로, 2028년 587조원을 450조원으로 낮췄다',
    fig_oi(),
    '막대 높이는 영업이익에 비례한다. 짙은 막대는 FnGuide 계열 컨센서스이고 Base Case가 그대로 쓴다.'
    '<br>옅은 막대는 Bear Case가 낮춘 가정이다. 2026년 Bear 가정은 원문에 없어 그리지 않았다')


# ── 삼성전자 3분기 ② 주가와 DCF 두 가지 ──────────────────────────────────────
# 값은 [261008] 삼성전자 편에 있는 것만: 종가 26만8,500원 · Bear 약 31만원 · Base 약 49만~50만원
def fig_price():
    base, ph = 210, 150.0 / 50.0
    h = [_t(26, 22, 't-head', '주당 가치와 10월 7일 종가 (단위 만원)')]
    h.append('<line class="k10-rule" x1="60" y1="%d" x2="520" y2="%d"/>' % (base, base))
    cols = [(130, 26.85, 'k10-fill', '26만8,500원', '10월 7일 종가'),
            (280, 31.0, 'k10-open', '약 31만원', 'Bear Case ①'),
            (430, 49.0, 'k10-open', '약 49만~50만원', 'Base Case ②')]
    for cx, v, cls, lab, nm in cols:
        hh = v * ph
        h.append('<rect class="%s" x="%d" y="%.1f" width="84" height="%.1f" rx="5"/>'
                 % (cls, cx - 42, base - hh, hh))
        if cx == 430:
            h.append('<rect class="k10-dash" x="%d" y="%.1f" width="84" height="%.1f" rx="5"/>'
                     % (cx - 42, base - 50 * ph, 1 * ph))
            top = base - 50 * ph
        else:
            top = base - hh
        h.append(_t(cx, '%.1f' % (top - 9), 't-step', lab, 'middle'))
        h.append(_t(cx, base + 18, 't-sub', nm, 'middle'))
    return _svg(560, 240, '삼성전자 10월 7일 종가 26만8,500원은 필자 DCF의 Bear Case 약 31만원과 '
                'Base Case 약 49만~50만원보다 낮다', h)


F_PRICE = (
    5, '종가 26만8,500원은 Bear Case 31만원에도 못 미친다',
    fig_price(),
    '막대 높이는 주당 금액에 비례한다. Base Case 점선 구간은 49만원에서 50만원 사이의 범위다.'
    '<br>① 2027년 480조원, 2028년 450조원, 장기 영업이익률 20%, WACC 10.5%, 영구성장률 2.0%'
    '<br>② 2026~2028년 컨센서스 그대로, 장기 영업이익률 26%, WACC 9.5%, 영구성장률 2.5%')


ALL = [F_ACQ, F_INHERIT, F_SHIPNUM, F_SERVE, F_RAIL, F_TIMING, F_CHAIN, F_DRAM, F_THREE, F_WHERE,
       F_OI, F_PRICE]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
