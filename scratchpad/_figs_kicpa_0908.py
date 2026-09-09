# -*- coding: utf-8 -*-
"""회계사 카드 도해 — 2026-09-08 추가분(엘곰·방구퐁 08-31~09-08 열다섯 편) 중 앞 다섯.

  ① 두 레인 타임라인  개발 순서와 탑재 순서가 뒤집혔다 (LPDDR6 편)
  ② 나란한 세로 막대  증권사가 정당하다는 배수와 시장이 매기는 배수 (08-31 시황 편)
  ③ 좌우 두 판       배수는 세 자리, PEG는 기준선의 다섯 배 (테슬라 편)
  ④ 세로 눈금        29,000 아래위로 필자가 적어 둔 자리들 (나스닥 밸류에이션 편)
  ⑤ 나란한 세로 막대  지수는 0.4%대, 반도체는 2~3%대 (09-03 시황 편)

규칙(yohan-figure · 글과 도해 확정 규칙):
  - 원문에 있는 값만 쓴다. 막대 높이와 눈금 위치는 전부 원문이 준 수치를 옮긴 것이다.
  - 색은 회색만이다(확정 규칙 S2). 짙은 상자 하나로 강조하고 점선은 아직 없는 것에만 쓴다.
  - 견줌은 나란한 세로 막대로 세운다. 성격이 다른 값(배수와 PEG)은 같은 판에 안 세운다.
  - 배치는 scratchpad/check_fig.py 가 본다.
"""

CSS = """
  .uc-fig .k8-fill { fill:rgba(127,127,127,.20); stroke:var(--ink-3); stroke-width:1.3; }
  .uc-fig .k8-open { fill:rgba(127,127,127,.06); stroke:var(--line); stroke-width:1.2; }
  .uc-fig .k8-dash { fill:none; stroke:var(--line); stroke-width:1.2; stroke-dasharray:4 4; }
  .uc-fig .k8-rule { stroke:var(--ink-3); stroke-width:1.2; }
  .uc-fig .k8-thin { stroke:var(--line); stroke-width:1; }
"""


# ── ① 두 레인 타임라인 — 개발과 탑재의 순서가 다르다 ──────────────────────
# 값은 [260831] LPDDR6 편에 있는 것만: 2025-11 삼성 개발 · 2026-03 SK 개발 ·
# 2026-01 삼성 CES 공개 · 2026-03 CXMT 시험공급 · 2026-08 CXMT 최종점검 · 20만~30만대
_LANE_X = {'2025-11': 118, '2026-01': 208, '2026-03': 298, '2026-08': 452}


def fig_lpddr6():
    h = ['<svg viewBox="0 0 560 268" role="img" aria-label="LPDDR6 개발은 삼성전자가 '
         '2025년 11월에 먼저 마쳤지만 스마트폰 탑재는 CXMT가 2026년 8월 20만에서 '
         '30만대 규모로 먼저 했다">']
    h.append('<text x="26" y="22" class="t-head">개발 레인과 탑재 레인</text>')
    # 눈금
    for lab, x in sorted(_LANE_X.items(), key=lambda kv: kv[1]):
        h.append('<line class="k8-thin" x1="%d" y1="44" x2="%d" y2="212"/>' % (x, x))
        h.append('<text x="%d" y="38" class="t-sub" text-anchor="middle">%s</text>' % (x, lab))
    # 개발 레인
    h.append('<text x="26" y="72" class="t-step">개발</text>')
    h.append('<rect class="k8-fill" x="%d" y="56" width="132" height="34" rx="6"/>'
             % (_LANE_X['2025-11'] - 8))
    h.append('<text x="%d" y="78" class="t-sub">삼성전자 세계 최초</text>' % (_LANE_X['2025-11'] + 4))
    h.append('<rect class="k8-open" x="%d" y="96" width="120" height="34" rx="6"/>'
             % (_LANE_X['2026-03'] - 8))
    h.append('<text x="%d" y="118" class="t-sub">SK하이닉스 개발 성공</text>' % (_LANE_X['2026-03'] + 4))
    # 탑재 레인
    h.append('<line class="k8-rule" x1="26" y1="146" x2="534" y2="146"/>')
    h.append('<text x="26" y="172" class="t-step">탑재</text>')
    h.append('<rect class="k8-dash" x="%d" y="156" width="118" height="32" rx="6"/>'
             % (_LANE_X['2026-01'] - 8))
    h.append('<text x="%d" y="176" class="t-sub">삼성전자 CES 공개</text>' % (_LANE_X['2026-01'] + 4))
    h.append('<text x="%d" y="204" class="t-sub">양산 시점 안 밝힘</text>' % (_LANE_X['2026-01'] + 4))
    h.append('<rect class="k8-fill" x="%d" y="156" width="102" height="32" rx="6"/>'
             % (_LANE_X['2026-08'] - 60))
    h.append('<text x="%d" y="176" class="t-sub" text-anchor="end">CXMT · 샤오미 18 폴드</text>'
             % (_LANE_X['2026-08'] + 36))
    h.append('<text x="%d" y="204" class="t-val" text-anchor="end">20만~30만대</text>'
             % (_LANE_X['2026-08'] + 36))
    h.append('<text x="26" y="240" class="t-sub">점선 상자는 시점이 아직 안 나온 것이다. '
             'SK하이닉스 탑재는 하반기 예정이라 눈금에 못 세웠다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_LPDDR6 = (
    3, '개발은 삼성전자가 먼저, 탑재는 CXMT가 먼저다',
    fig_lpddr6(),
    '위 레인이 개발, 아래 레인이 실제 스마트폰 탑재다. 삼성전자가 <b>2025년 11월</b>에 개발을 '
    '먼저 마쳤지만 아래 레인의 첫 실물은 <b>2026년 8월</b> CXMT의 샤오미 18 폴드 '
    '<b>20만~30만대</b>다. 삼성전자 칸을 점선으로 둔 것은 양산 시점이 원문에 없기 때문이고, '
    'SK하이닉스 탑재도 하반기 예정이라는 말만 있어 눈금에 세우지 않았다.')


# ── ② 나란한 세로 막대 — 정당하다는 배수와 시장이 매기는 배수 ─────────────
# 값은 [260831] 시황 편에 있는 것만: 삼성 5.5배 / 13배, 하이닉스 4.71배 / 10배
_PER = [('삼성전자', '시장', 5.5, 'k8-open'), ('삼성전자', '증권사 목표', 13.0, 'k8-fill'),
        ('SK하이닉스', '시장', 4.71, 'k8-open'), ('SK하이닉스', '증권사 목표', 10.0, 'k8-fill')]
_PH = 150.0 / 13.0   # 배당 px


def fig_per_gap():
    base = 196
    h = ['<svg viewBox="0 0 560 260" role="img" aria-label="12개월 선행 PER은 삼성전자 '
         '5.5배 SK하이닉스 4.71배인데 증권사가 제시한 목표 PER은 13배와 10배다">']
    h.append('<text x="26" y="22" class="t-head">12개월 선행 PER과 증권사 목표 PER</text>')
    h.append('<line class="k8-rule" x1="60" y1="%d" x2="534" y2="%d"/>' % (base, base))
    for i, (who, kind, v, cls) in enumerate(_PER):
        x = 84 + i * 112
        hgt = v * _PH
        h.append('<rect class="%s" x="%d" y="%.1f" width="64" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">%s배</text>'
                 % (x + 32, base - hgt - 10, ('%g' % v)))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 32, base + 18, kind))
        if i % 2 == 0:
            h.append('<text x="%d" y="%d" class="t-step" text-anchor="middle">%s</text>'
                     % (x + 88, base + 40, who))
    h.append('<text x="26" y="248" class="t-sub">막대 높이는 배수다. '
             '같은 회사 두 막대의 차이가 시장과 증권사 사이의 거리다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_PER_GAP = (
    3, '증권사가 정당하다는 배수의 절반에서 거래된다',
    fig_per_gap(),
    '같은 회사를 두 막대로 나란히 세웠다. 왼쪽 옅은 막대가 시장이 실제로 매기는 12개월 선행 '
    'PER(<b>삼성전자 5.5배 · SK하이닉스 4.71배</b>)이고, 오른쪽 짙은 막대가 한 증권사가 '
    '정당하다고 제시한 목표 PER(<b>13배 · 10배</b>)이다. 그 증권사는 이익 전망치를 최대 '
    '<b>18%</b>까지 올리면서도 이 격차를 좁히지 못했다. 2026년 물량 완판과 D램 가격 연간 '
    '<b>47%</b> 상승 전망은 이익 쪽 숫자이지 배수 쪽 숫자가 아니다.')


# ── ③ 좌우 두 판 — 배수와 PEG는 성격이 달라 판을 가른다 ────────────────────
# 값은 [260901] 테슬라 편에 있는 것만: Trailing 328.53 · Forward 181.82 ·
# PEG 5.20 · 린치 기준 1.0 · 통상 고평가 구간 2.0
def fig_tesla():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="테슬라 후행 PER 328.53배 '
         '선행 PER 181.82배이고 PEG 5.20배는 피터 린치 기준 1.0배의 다섯 배가 넘는다">']
    h.append('<text x="26" y="22" class="t-head">이익배수 판</text>')
    h.append('<text x="316" y="22" class="t-head">PEG 판</text>')
    # 왼쪽 — PER 두 개
    base = 186
    for i, (lab, v) in enumerate([('후행', 328.53), ('선행', 181.82)]):
        x = 52 + i * 108
        hgt = v * (140.0 / 328.53)
        h.append('<rect class="%s" x="%d" y="%.1f" width="62" height="%.1f" rx="5"/>'
                 % ('k8-fill' if i == 0 else 'k8-open', x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">%s배</text>'
                 % (x + 31, base - hgt - 10, ('%.2f' % v)))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s PER</text>'
                 % (x + 31, base + 18, lab))
    h.append('<line class="k8-rule" x1="34" y1="%d" x2="248" y2="%d"/>' % (base, base))
    # 오른쪽 — PEG 세 개
    for i, (lab, v, cls) in enumerate([('린치 기준', 1.0, 'k8-open'),
                                       ('고평가 구간', 2.0, 'k8-open'),
                                       ('테슬라', 5.20, 'k8-fill')]):
        x = 316 + i * 74
        hgt = v * (140.0 / 5.20)
        h.append('<rect class="%s" x="%d" y="%.1f" width="46" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">%s</text>'
                 % (x + 23, base - hgt - 10, ('%g' % v)))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 23, base + 18, lab))
    h.append('<line class="k8-rule" x1="300" y1="%d" x2="534" y2="%d"/>' % (base, base))
    h.append('<text x="26" y="222" class="t-sub">'
             '순이익률 3.67% · ROE 4.67% · 시가총액 1.40조 달러</text>')
    h.append('<text x="26" y="240" class="t-sub">'
             '두 판은 눈금이 다르다. 한 막대에 세우면 견줌이 안 된다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_TESLA = (
    4, '배수는 세 자리, PEG는 기준선의 다섯 배다',
    fig_tesla(),
    '왼쪽은 이익배수, 오른쪽은 성장까지 반영한 PEG다. 후행 PER <b>328.53배</b>가 선행 '
    '<b>181.82배</b>로 낮아지지만 여전히 세 자리이고, PEG <b>5.20배</b>는 피터 린치가 적정 '
    '기준으로 든 <b>1.0배</b>의 다섯 배가 넘는다. 두 판을 따로 세운 것은 눈금이 다르기 때문이다. '
    '아래 줄의 순이익률 <b>3.67%</b>와 ROE <b>4.67%</b>는 이 배수를 떠받치는 것이 지금 이익이 '
    '아니라는 원문의 근거다.')


# ── ④ 세로 눈금 — 29,000 아래위로 적어 둔 자리 ─────────────────────────────
# 값은 [260902] 편에 있는 것만. 필자가 적은 지수 자리를 그대로 세운다.
_LEVELS = [(30350, '30,300~30,350', '조정 종료·신고가 시도'),
           (30000, '30,000', '심리 안정'),
           (29850, '29,800~29,900', '반등 첫 신호'),
           (29000, '29,000', '지키면 소화 과정'),
           (28550, '28,550', '이탈 시 1차 목표'),
           (28400, '28,400', '그 아래 지지력')]


def fig_nasdaq():
    top, bot = 46, 214
    lo, hi = 28400.0, 30350.0
    h = ['<svg viewBox="0 0 560 292" role="img" aria-label="나스닥100 지수의 29,000 방어선과 '
         '위아래 지지 저항 자리를 눈금으로 세운 그림">']
    h.append('<text x="26" y="24" class="t-head">필자가 적어 둔 나스닥100 자리</text>')
    for v, lab, note in _LEVELS:
        y = bot - (v - lo) / (hi - lo) * (bot - top)
        cls = 'k8-rule' if v == 29000 else 'k8-thin'
        h.append('<line class="%s" x1="150" y1="%.1f" x2="360" y2="%.1f"/>' % (cls, y, y))
        h.append('<text x="142" y="%.1f" class="%s" text-anchor="end">%s</text>'
                 % (y + 4, 't-val' if v == 29000 else 't-sub', lab))
        h.append('<text x="370" y="%.1f" class="t-sub">%s</text>' % (y + 4, note))
    h.append('<rect class="k8-open" x="26" y="232" width="508" height="46" rx="8"/>')
    h.append('<text x="44" y="252" class="t-step">셋이 동시에 나빠질 때만 배수 재조정이다</text>')
    h.append('<text x="44" y="270" class="t-sub">'
             '나스닥100 29,000 이탈 · 미국 10년물 4.8~5.0% 위 · 브렌트유 90달러 위 고착</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_NASDAQ = (
    5, '29,000 하나가 아니라 셋이 같이 깨지는지가 갈림길이다',
    fig_nasdaq(),
    '눈금은 필자가 글에 적은 지수 자리를 그대로 옮긴 것이고, 굵은 줄이 <b>29,000</b>이다. '
    '위로는 <b>29,800~29,900</b> 회복이 반등의 첫 신호, <b>30,300~30,350</b> 돌파가 조정 '
    '종료이고, 아래로는 <b>28,550</b>과 <b>28,400</b>이 차례로 나온다. 아래 상자가 요점이다 — '
    '지수 이탈만으로는 단기 베어트랩일 수 있고, 미국 10년물과 브렌트유가 같이 나빠질 때라야 '
    '성장주에 매기는 배수 자체가 다시 계산된다는 것이 필자의 갈림길이다.')


# ── ⑤ 나란한 세로 막대 — 지수와 반도체의 상승폭이 다르다 ────────────────────
# 값은 [260903] 시황 편에 있는 것만
_D0903 = [('Dow', 0.56), ('S&amp;P500', 0.46), ('Nasdaq', 0.45), ('러셀2000', 1.1),
          ('퀄컴', 2.0), ('마이크론', 2.4), ('엔비디아', 3.2)]


def fig_selective():
    base = 172
    h = ['<svg viewBox="0 0 560 258" role="img" aria-label="9월 2일 미국 지수는 0.45에서 '
         '1.1퍼센트 올랐고 반도체는 2.0에서 3.2퍼센트 올랐다">']
    h.append('<text x="26" y="22" class="t-head">9월 2일 하루 등락</text>')
    h.append('<line class="k8-rule" x1="34" y1="%d" x2="534" y2="%d"/>' % (base, base))
    for i, (lab, v) in enumerate(_D0903):
        x = 36 + i * 72
        hgt = v * (108.0 / 3.2)
        cls = 'k8-fill' if i >= 4 else 'k8-open'
        h.append('<rect class="%s" x="%d" y="%.1f" width="50" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">+%g%%</text>'
                 % (x + 25, base - hgt - 9, v))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 25, base + 18, lab))
    h.append('<text x="26" y="212" class="t-sub">'
             '짙은 막대 셋이 반도체다. 지수가 0.4%대일 때 2~3%대로 올랐다</text>')
    h.append('<text x="26" y="234" class="t-sub">'
             '전날 한국은 반대쪽이었다 — 코스피 −3.99%, 삼성전자 −4.02%, SK하이닉스 −4.73%</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_SELECTIVE = (
    3, '지수는 0.4%대, 반도체만 2~3%대로 올랐다',
    fig_selective(),
    '같은 날 등락을 한 눈금에 세웠다. 지수 넷이 <b>+0.45%~+1.1%</b>인 동안 짙은 막대의 '
    '반도체 셋은 <b>+2.0%~+3.2%</b>다. 시장 전체가 위험을 다시 받아들인 것이 아니라 '
    'AI·반도체에만 매수가 들어왔다는 필자의 읽기가 이 높이 차이다. 전날 한국은 반대쪽이라 '
    '아래 줄에 값을 적었다 — 코스피 <b>−3.99%</b>에 외국인 약 <b>1.9조원</b>, 기관 약 '
    '<b>2조원</b> 순매도였다.')

# ── ⑥ 두 판 — 고용은 예상의 세 배, 임금은 오히려 내려갔다 ──────────────────
# 값은 [260905] 고용 편에 있는 것만: 예상 5.0만~5.5만 · 실제 16.2만 · 실업률 4.1% ·
# 임금 3.2%→3.1% · 2년 4.41% · 10년 4.80% · 30년 5.25% · 인상 확률 50%→60%
def fig_jobs():
    base = 150
    h = ['<svg viewBox="0 0 560 268" role="img" aria-label="8월 비농업 고용은 예상 '
         '5만에서 5만5천 명의 세 배에 가까운 16만2천 명이었고 시간당 임금 상승률은 '
         '3.2퍼센트에서 3.1퍼센트로 낮아졌다">']
    h.append('<text x="26" y="22" class="t-head">8월 비농업 고용</text>')
    h.append('<text x="316" y="22" class="t-head">같은 보고서의 임금</text>')
    for i, (lab, v, cls) in enumerate([('시장 예상', 5.5, 'k8-open'), ('실제', 16.2, 'k8-fill')]):
        x = 56 + i * 116
        hgt = v * (96.0 / 16.2)
        h.append('<rect class="%s" x="%d" y="%.1f" width="70" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">%s만 명</text>'
                 % (x + 35, base - hgt - 10, ('%g' % v)))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 35, base + 18, lab))
    h.append('<line class="k8-rule" x1="34" y1="%d" x2="256" y2="%d"/>' % (base, base))
    h.append('<text x="34" y="192" class="t-sub">실업률 4.1% 유지 · 참가율 61.4%에서 61.6%</text>')
    h.append('<text x="34" y="212" class="t-sub">7월도 2만3천 명 감소에서 2만1천 명 증가로 고침</text>')
    h.append('<rect class="k8-open" x="316" y="36" width="218" height="60" rx="8"/>')
    h.append('<text x="334" y="60" class="t-sub">시간당 평균임금 전년 대비</text>')
    h.append('<text x="334" y="84" class="t-val">3.2% → 3.1%</text>')
    h.append('<rect class="k8-fill" x="316" y="108" width="218" height="104" rx="8"/>')
    h.append('<text x="334" y="132" class="t-sub">발표 직후 움직인 값</text>')
    h.append('<text x="334" y="156" class="t-sub">9월 인상 확률 약 50% → 약 60%</text>')
    h.append('<text x="334" y="178" class="t-sub">2년물 4.41% · 10년물 4.80%</text>')
    h.append('<text x="334" y="200" class="t-sub">30년물 5.25% 위로</text>')
    h.append('<text x="26" y="244" class="t-sub">'
             '주가 낙폭은 이 크기에 비해 작았다 — 장중 다우 약 −0.5%, S&amp;P500 약 −0.3%</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_JOBS = (
    3, '고용은 예상의 세 배인데 임금은 내려갔다',
    fig_jobs(),
    '왼쪽 막대가 8월 비농업 고용이다. 시장 예상 <b>5만~5만5천 명</b>에 견줘 실제는 '
    '<b>16만2천 명</b>이었다. 오른쪽 위 상자가 같은 보고서의 임금인데 전년 대비 '
    '<b>3.2%에서 3.1%</b>로 내려갔다 — 취업자가 늘어도 임금이 안 따라 올랐다는 것이 '
    '필자가 과열로 안 읽는 근거다. 아래 상자는 발표 직후 값이 움직인 곳으로, 주식보다 '
    '국채가 먼저 그리고 크게 반응했다.')


# ── ⑦ 좌우 대비 — 같은 날 반도체와 소프트웨어가 반대로 갔다 ─────────────────
# 값은 [260905] 로테이션 편에 있는 것만: SOX 약 +3% · 소프트웨어 ETF −2.4% ·
# Sandisk 약 +12% · Micron 6% 이상
def fig_rotate2():
    mid = 268
    sc = 26.0   # 1%당 px
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="9월 4일 필라델피아 반도체지수는 '
         '약 3퍼센트 올랐고 소프트웨어 ETF는 2.4퍼센트 내렸다">']
    h.append('<text x="26" y="22" class="t-head">9월 4일, 기준선을 사이에 둔 두 진영</text>')
    h.append('<line class="k8-rule" x1="%d" y1="36" x2="%d" y2="168"/>' % (mid, mid))
    h.append('<rect class="k8-fill" x="%d" y="52" width="%.1f" height="36" rx="6"/>'
             % (mid, 3.0 * sc))
    h.append('<text x="%d" y="76" class="t-sub" text-anchor="end">반도체지수</text>' % (mid - 10))
    h.append('<text x="%.1f" y="76" class="t-val">약 +3%%</text>' % (mid + 3.0 * sc + 10))
    h.append('<rect class="k8-open" x="%.1f" y="112" width="%.1f" height="36" rx="6"/>'
             % (mid - 2.4 * sc, 2.4 * sc))
    h.append('<text x="%d" y="136" class="t-sub">소프트웨어 ETF</text>' % (mid + 10))
    h.append('<text x="%.1f" y="136" class="t-val" text-anchor="end">−2.4%%</text>'
             % (mid - 2.4 * sc - 10))
    h.append('<rect class="k8-open" x="26" y="182" width="508" height="52" rx="10"/>')
    h.append('<text x="46" y="204" class="t-step">같은 날 개별 종목</text>')
    h.append('<text x="46" y="226" class="t-sub">'
             'Sandisk 약 +12% · Micron 6% 이상 · Seagate도 함께 올랐다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_ROTATE2 = (
    3, '반도체가 3% 오른 날 소프트웨어는 2.4% 내렸다',
    fig_rotate2(),
    '가운데 선이 그날의 0%다. 필자가 이 하루를 메모리 재평가가 아니라 '
    '진영 사이의 자금 이동으로 읽는 근거가 이 반대 부호다. 아래 상자의 종목들은 원문이 값을 '
    '준 것만 옮겼다.')


# ── ⑧ 세 단계 — 이익이 그대로여도 배수가 오르면 값이 오른다 ──────────────────
# 값은 [260906] PER 편의 가정 예시다. 실제 기업 실적이 아니라는 것을 캡션에 적는다.
_STEPS = [('1단계', 'EPS 10', '15배', '150'),
          ('2단계 — 지속기간 재평가', 'EPS 10', '20배', '200'),
          ('3단계 — 이익도 증가', 'EPS 12', '20배', '240')]


def fig_per_steps():
    h = ['<svg viewBox="0 0 560 236" role="img" aria-label="같은 이익에도 배수가 15배에서 '
         '20배로 오르면 주가가 150에서 200이 되고 이익까지 20퍼센트 늘면 240이 된다">']
    h.append('<text x="26" y="22" class="t-head">필자가 든 가정 — 세 단계</text>')
    for i, (name, eps, per, px) in enumerate(_STEPS):
        x = 26 + i * 172
        cls = 'k8-fill' if i == 2 else 'k8-open'
        h.append('<rect class="%s" x="%d" y="40" width="156" height="128" rx="10"/>' % (cls, x))
        h.append('<text x="%d" y="64" class="t-sub">%s</text>' % (x + 16, name))
        h.append('<text x="%d" y="90" class="t-sub">%s</text>' % (x + 16, eps))
        h.append('<text x="%d" y="112" class="t-sub">적용 배수 %s</text>' % (x + 16, per))
        h.append('<text x="%d" y="146" class="t-val">주가 %s</text>' % (x + 16, px))
        if i < 2:
            h.append('<line class="k8-thin" x1="%d" y1="104" x2="%d" y2="104"/>'
                     % (x + 158, x + 170))
    h.append('<text x="26" y="196" class="t-sub">'
             '2단계에서 이익은 그대로다. 움직인 것은 시장이 그 이익을 몇 해로 보느냐다</text>')
    h.append('<text x="26" y="218" class="t-sub">'
             '1단계에서 3단계로 가면 이익은 20% 느는데 주가는 60% 오른다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_PER_STEPS = (
    4, '이익이 그대로여도 배수가 오르면 값이 오른다',
    fig_per_steps(),
    '필자가 개념을 보이려고 든 가정이다(실제 기업 실적이 아니다). 1단계에서 2단계로 갈 때 '
    'EPS는 <b>10</b>으로 같고 배수만 <b>15배에서 20배</b>로 올라 주가가 <b>150에서 200</b>이 '
    '된다. 3단계에서 EPS가 <b>12</b>로 20% 늘면 주가는 <b>240</b>, 곧 <b>60%</b>가 된다. '
    '반도체가 이익 정점에서 배수가 가장 낮아 보이는 이유도 같은 산수다 — 이익이 주가보다 '
    '빨리 늘면 배수는 내려간다.')


# ── ⑨ 두 줄 띠 — 같은 주가가 정상화 시점에 따라 6배도 18배도 된다 ────────────
# 값은 [260906] 마이크론 편의 가정 예시: 주가 900 · 호황 EPS 150 · 정상화 EPS 50
def fig_duration():
    h = ['<svg viewBox="0 0 560 262" role="img" aria-label="주가 900달러는 호황기 주당순이익 '
         '150달러 기준 PER 6배지만 정상화 이후 50달러 기준으로는 18배가 된다">']
    h.append('<text x="26" y="22" class="t-head">같은 주가 900, 갈리는 배수</text>')
    h.append('<rect class="k8-fill" x="26" y="38" width="240" height="86" rx="10"/>')
    h.append('<text x="46" y="62" class="t-sub">호황기 주당순이익 150</text>')
    h.append('<text x="46" y="94" class="t-val">PER 6배</text>')
    h.append('<text x="46" y="114" class="t-sub">싸 보이는 자리</text>')
    h.append('<rect class="k8-open" x="294" y="38" width="240" height="86" rx="10"/>')
    h.append('<text x="314" y="62" class="t-sub">정상화 뒤 주당순이익 50</text>')
    h.append('<text x="314" y="94" class="t-val">PER 18배</text>')
    h.append('<text x="314" y="114" class="t-sub">같은 주가, 다른 값</text>')
    h.append('<text x="26" y="152" class="t-step">그래서 관건은 150이 몇 해 가느냐다</text>')
    h.append('<rect class="k8-open" x="26" y="164" width="150" height="34" rx="6"/>')
    h.append('<text x="40" y="186" class="t-sub">2년으로 볼 때</text>')
    h.append('<rect class="k8-fill" x="196" y="164" width="338" height="34" rx="6"/>')
    h.append('<text x="212" y="186" class="t-sub">4~5년으로 볼 때 — 띠 길이가 곧 기업가치다</text>')
    h.append('<text x="26" y="224" class="t-sub">'
             '시장이 기다린 종료 신호 여섯은 하나도 뚜렷하지 않았다 — 빅테크 설비투자 둔화 ·</text>')
    h.append('<text x="26" y="244" class="t-sub">'
             'AI 서버 주문 둔화 · HBM 수요 둔화 · DRAM 가격 하락 · 재고 증가 · 신규 공급 급증</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_DURATION = (
    3, '같은 주가가 6배도 18배도 된다',
    fig_duration(),
    '필자가 든 가정이다. 주가 <b>900</b>은 호황기 주당순이익 <b>150</b> 기준으로 <b>6배</b>지만 '
    '정상화 뒤 <b>50</b> 기준으로는 <b>18배</b>다. 그래서 싸다·비싸다를 정하는 것이 배수가 '
    '아니라 <b>150이 몇 해 가느냐</b>가 된다. 아래 띠 두 개가 그 기간이고, 9월 4일에 움직인 '
    '것은 올해 이익 전망이 아니라 이 띠의 길이다. 시장이 기다린 종료 신호 여섯은 하나도 '
    '뚜렷하게 나오지 않았다.')


# ── ⑩ 가로 띠 — 필자가 매긴 오늘 시나리오 셋 ─────────────────────────────
# 값은 [260907] 시황 편에 있는 것만: 50% / 30% / 20%, 등락 범위, SOX +3.37% 등
_SCEN = [('반도체 주도 상승', 50, '+1.0~+3.0%'),
         ('상승 출발 뒤 보합', 30, '0~+1%'),
         ('유가·금리 부담으로 하락', 20, '−0.5~−1.5%')]


def fig_scenario():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="필자는 반도체 주도 상승 50퍼센트 '
         '보합 30퍼센트 하락 20퍼센트로 오늘 시나리오를 매겼다">']
    h.append('<text x="26" y="22" class="t-head">9월 7일 한국 증시 시나리오</text>')
    for i, (name, p, rng) in enumerate(_SCEN):
        y = 40 + i * 52
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 14, name))
        h.append('<rect class="%s" x="222" y="%d" width="%.1f" height="24" rx="5"/>'
                 % ('k8-fill' if i == 0 else 'k8-open', y, p * 2.4))
        h.append('<text x="%.1f" y="%d" class="t-val">%d%%</text>' % (222 + p * 2.4 + 10, y + 18, p))
        h.append('<text x="222" y="%d" class="t-sub">예상 등락 %s</text>' % (y + 44, rng))
    h.append('<rect class="k8-open" x="26" y="196" width="508" height="50" rx="8"/>')
    h.append('<text x="46" y="218" class="t-sub">'
             '전날 미국 — 다우 −0.51% · S&amp;P500 −0.38%</text>')
    h.append('<text x="46" y="238" class="t-sub">'
             '그런데 SOX +3.37% · Micron +6.10%</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_SCENARIO = (
    3, '반도체가 끌어올리되 폭은 외국인이 정한다',
    fig_scenario(),
    '띠 길이가 필자가 매긴 확률이다 — 반도체 주도 상승 <b>50%</b>, 보합 <b>30%</b>, 하락 '
    '<b>20%</b>다. 아래 상자가 그 전날 미국인데, 지수는 내리고 반도체만 올랐다. 필자가 '
    'Micron이 6.1% 올랐으니 오늘 SK하이닉스도 6%라는 식의 연결을 막는 이유가 여기 있다 — '
    '같은 밤에 10년물 <b>4.78%</b>와 브렌트유 <b>96.28달러</b>도 함께 나왔기 때문이다. '
    '그래서 보는 자리를 개장가가 아니라 10시 30분 이후 외국인 매매로 잡는다.')

# ── ⑪ 두 판 — 가동률과 정상화 이익률 ────────────────────────────────────
# 값은 [260907] 2차전지 편에 있는 것만: LG에너지솔루션 가동률 47.6% · 정상 기준 70~80% ·
# CATL 2025년 약 18% · 파나소닉 약 14% · 시나리오 3~5% / 6~8% / 9~11%
def fig_battery():
    h = ['<svg viewBox="0 0 560 262" role="img" aria-label="LG에너지솔루션 가동률은 '
         '47.6퍼센트로 영업레버리지가 작동한다는 70에서 80퍼센트에 못 미치고 정상화 '
         '영업이익률 시나리오는 3에서 11퍼센트다">']
    h.append('<text x="26" y="22" class="t-head">가동률</text>')
    # 가동률 띠
    h.append('<rect class="k8-open" x="26" y="38" width="400" height="34" rx="6"/>')
    h.append('<rect class="k8-fill" x="26" y="38" width="190" height="34" rx="6"/>')
    h.append('<text x="42" y="60" class="t-val">47.6%</text>')
    h.append('<line class="k8-rule" x1="306" y1="32" x2="306" y2="78"/>')
    h.append('<line class="k8-rule" x1="346" y1="32" x2="346" y2="78"/>')
    h.append('<text x="326" y="94" class="t-sub" text-anchor="middle">70~80%</text>')
    h.append('<text x="440" y="60" class="t-sub">영업레버리지가</text>')
    h.append('<text x="440" y="76" class="t-sub">도는 자리</text>')
    h.append('<text x="26" y="116" class="t-sub">'
             '수요는 늘었다 — 2025년 전기차 판매 20% 증가, 배터리 탑재량 1.2TWh</text>')
    # 이익률 막대
    base = 218
    h.append('<text x="26" y="146" class="t-head">정상화 영업이익률</text>')
    h.append('<line class="k8-rule" x1="34" y1="%d" x2="534" y2="%d"/>' % (base, base))
    bars = [('보수', 4.0, '3~5%', 'k8-open'), ('기본', 7.0, '6~8%', 'k8-open'),
            ('낙관', 10.0, '9~11%', 'k8-open'),
            ('파나소닉 2025', 14.0, '약 14%', 'k8-fill'),
            ('CATL 2025', 18.0, '약 18%', 'k8-fill')]
    for i, (lab, v, txt, cls) in enumerate(bars):
        x = 44 + i * 98
        hgt = v * (48.0 / 18.0)
        h.append('<rect class="%s" x="%d" y="%.1f" width="60" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 30, base - hgt - 8, txt))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 30, base + 18, lab))
    h.append('<text x="26" y="256" class="t-sub">'
             '앞의 셋은 필자가 세운 시나리오, 뒤의 둘은 실제 회사 값이다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_BATTERY = (
    3, '가동률 47.6%로는 정상 이익률에 못 닿는다',
    fig_battery(),
    '위 띠가 가동률이다. LG에너지솔루션 <b>47.6%</b>는 영업레버리지가 도는 자리로 필자가 '
    '드는 <b>70~80%</b>에 한참 못 미친다. 수요가 줄어서가 아니다 — 2025년 전기차 판매는 '
    '<b>20%</b> 늘어 2,000만 대를 넘었고 배터리 탑재량도 <b>1.2TWh</b>였다. 아래 막대에서 '
    '앞의 셋은 필자가 세운 정상화 이익률 시나리오이고, 뒤의 둘은 CATL <b>약 18%</b>·파나소닉 '
    '<b>약 14%</b>라는 실제 값이다. 배터리가 본래 저마진 사업이라는 진단을 이 둘이 막는다.')


# ── ⑫ 세 줄 — 산업·설비투자·초과이익의 지속기간은 서로 다르다 ────────────────
# 값은 [260907] 엔비디아 편에 있는 것만: 시총 5.4조 달러 · S&P500의 약 8% ·
# FY2028 성장률 70%(기존 예상 45%) · PER 13배 · 주가 30%와 예상 EPS 60% 예시
def fig_duration3():
    h = ['<svg viewBox="0 0 560 258" role="img" aria-label="AI 산업의 지속기간과 설비투자 '
         '폭증의 지속기간과 엔비디아 초과이익의 지속기간은 서로 다르다">']
    h.append('<text x="26" y="22" class="t-head">시장이 의심하는 것은 셋 중 아래 둘이다</text>')
    lanes = [('AI 산업이 성장하는 기간', 470, 'k8-open'),
             ('AI 설비투자가 폭증하는 기간', 300, 'k8-open'),
             ('엔비디아 초과이익 기간', 200, 'k8-fill')]
    for i, (name, w, cls) in enumerate(lanes):
        y = 40 + i * 52
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 14, name))
        h.append('<rect class="%s" x="26" y="%d" width="%d" height="20" rx="5"/>'
                 % (cls, y + 22, w))
    h.append('<text x="26" y="212" class="t-sub">'
             '띠 길이는 원문에 값이 없어 순서만 나타낸다 — 길이를 값으로 읽으면 안 된다</text>')
    h.append('<rect class="k8-open" x="26" y="222" width="508" height="28" rx="8"/>')
    h.append('<text x="42" y="241" class="t-sub">'
             '시총 5.4조 달러 · S&amp;P500의 약 8% · FY2028 성장률 70% · 배수 13배</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_DURATION3 = (
    3, '세 가지 지속기간을 섞으면 배수가 안 읽힌다',
    fig_duration3(),
    '필자가 갈라 놓은 셋이다. AI 산업이 오래 간다는 것과, 설비투자가 지금 속도로 계속 는다는 것과, '
    '엔비디아가 지금의 초과이익을 유지한다는 것은 서로 다른 이야기다. 시장이 값을 안 주는 자리는 '
    '아래 둘이고, 그래서 <b>FY2028 성장률 70%</b> 가이던스에도 배수가 <b>13배</b>에 머문다. '
    '띠 길이에는 값이 없다 — 원문이 기간을 숫자로 준 적이 없어 순서만 그렸다.')


# ── ⑬ 두 판 — 이자비용이 세수에서 차지하는 몫과 매수 주체 교체 ───────────────
# 값은 [260907] 국채 편에 있는 것만: 부채 40조 달러 · 이자 약 1.25조 달러 ·
# 세수의 약 18.4% · 2036년 25% 전망 · 노르웨이 국부펀드 2.3조 달러 ·
# 빅테크 회사채 2026년 상반기 2,250억 달러
def fig_trust():
    base = 176
    h = ['<svg viewBox="0 0 560 262" role="img" aria-label="미국 연방부채 이자비용이 세수의 '
         '18.4퍼센트를 차지하고 2036년에는 25퍼센트가 될 것으로 전망된다">']
    h.append('<text x="26" y="22" class="t-head">세수에서 이자가 가져가는 몫</text>')
    h.append('<line class="k8-rule" x1="34" y1="%d" x2="250" y2="%d"/>' % (base, base))
    for i, (lab, v, cls) in enumerate([('지금', 18.4, 'k8-fill'), ('2036년 전망', 25.0, 'k8-open')]):
        x = 56 + i * 104
        hgt = v * (112.0 / 25.0)
        h.append('<rect class="%s" x="%d" y="%.1f" width="66" height="%.1f" rx="5"/>'
                 % (cls, x, base - hgt, hgt))
        h.append('<text x="%d" y="%.1f" class="t-val" text-anchor="middle">%g%%</text>'
                 % (x + 33, base - hgt - 10, v))
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + 33, base + 18, lab))
    h.append('<text x="34" y="220" class="t-sub">연방부채 40조 달러</text>')
    h.append('<text x="34" y="240" class="t-sub">연간 이자 약 1.25조 달러</text>')
    h.append('<text x="316" y="22" class="t-head">사는 쪽이 바뀐다</text>')
    h.append('<rect class="k8-open" x="294" y="36" width="240" height="66" rx="8"/>')
    h.append('<text x="312" y="60" class="t-sub">전에는 외국 중앙은행·기관</text>')
    h.append('<text x="312" y="84" class="t-sub">노르웨이 국부펀드 2.3조 달러</text>')
    h.append('<rect class="k8-fill" x="294" y="114" width="240" height="66" rx="8"/>')
    h.append('<text x="312" y="138" class="t-sub">지금은 가격에 민감한 헤지펀드</text>')
    h.append('<text x="312" y="162" class="t-sub">발행할 때마다 금리를 더 얹는다</text>')
    h.append('<text x="294" y="220" class="t-sub">같은 시장에서 빅테크도 빌린다</text>')
    h.append('<text x="294" y="240" class="t-sub">2026년 상반기 회사채 2,250억 달러</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_TRUST = (
    4, '이자가 세수의 18.4%를 가져가고, 사는 쪽이 바뀐다',
    fig_trust(),
    '왼쪽 막대가 세수에서 이자가 차지하는 몫이다. 지금 <b>약 18.4%</b>이고 미 의회예산국은 '
    '2036년까지 <b>25%</b>로 올라갈 것으로 본다. 오른쪽은 사는 쪽의 교체다 — 오래 들고 있던 '
    '외국 중앙은행과 기관이 물러나고(노르웨이 국부펀드 <b>2.3조 달러</b>는 비중 축소를 검토 '
    '중이다) 가격에 민감한 헤지펀드가 그 자리를 메우면, 재무부는 발행할 때마다 금리를 더 '
    '얹어야 물량을 소화한다. 같은 시장에서 빅테크도 상반기에만 <b>2,250억 달러</b>를 빌렸다.')


# ── ⑭ 가로 막대 — 시장이 값에 넣은 인상 확률 ────────────────────────────
# 값은 [260908] 편에 있는 것만: 9월 FOMC 약 58% · 10월 약 70% · 일본은행 약 75% ·
# 코스피 +4.61% · 브렌트유 약 96.45달러 · 금 약 4,426달러
_HIKE = [('미국 9월 16일 FOMC', 58), ('미국 10월', 70), ('일본은행 9월 18일', 75)]


def fig_hike():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="시장은 9월 FOMC 인상 확률을 '
         '약 58퍼센트 10월을 약 70퍼센트 일본은행 9월 인상을 약 75퍼센트로 반영하고 있다">']
    h.append('<text x="26" y="22" class="t-head">값에 이미 들어 있는 인상 확률</text>')
    for i, (name, p) in enumerate(_HIKE):
        y = 40 + i * 46
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 16, name))
        h.append('<rect class="k8-fill" x="216" y="%d" width="%.1f" height="24" rx="5"/>'
                 % (y, p * 3.0))
        h.append('<text x="%.1f" y="%d" class="t-val">%d%%</text>' % (216 + p * 3.0 + 10, y + 18, p))
    h.append('<rect class="k8-open" x="26" y="186" width="508" height="54" rx="8"/>')
    h.append('<text x="46" y="208" class="t-step">같은 날 반대쪽에 있던 값</text>')
    h.append('<text x="46" y="230" class="t-sub">'
             '코스피 +4.61% · 브렌트유 약 96.45달러 · 금 약 4,426달러</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_HIKE = (
    4, '지수는 4.61% 올랐는데 인상 확률도 같이 올라 있다',
    fig_hike(),
    '막대는 시장이 값에 넣어 둔 인상 확률이다. 미국 9월 FOMC <b>약 58%</b>, 10월 '
    '<b>약 70%</b>, 일본은행 9월 회의 <b>약 75%</b>이고 유럽중앙은행은 이번 주 2.75%로 올릴 '
    '것으로 거의 굳어져 있다. 아래 상자가 같은 날의 반대편이다 — 코스피가 <b>4.61%</b> 오른 '
    '날 브렌트유는 <b>약 96.45달러</b>였고 금은 <b>약 4,426달러</b>였다. 필자가 이 급등을 '
    '전망이 밝아진 신호로 안 읽는 이유가 이 두 줄의 공존이다.')


# ── ⑮ 세 갈래 — 열 편이 묻는 것이 요건·기간·절차로 갈린다 ──────────────────
# 값은 [260908] 세금판례 편에 있는 것만. 편 번호와 쟁점만 옮긴다.
_CASES = [('무엇에 매기나 — 요건', ['1편 포인트 결제와 에누리', '3편 증여세 완전포괄주의',
                              '4편 명의신탁 주식의 반복 과세', '5편 론스타·스타타워의 세목과 세율']),
          ('누구에게·얼마나 — 헌법', ['2편 헌법불합치로 사라진 세금', '6편 부부 합산과세',
                                '7편 종합부동산세 두 판단']),
          ('언제까지·어떻게 — 기간과 절차', ['8편 몰수·추징 뒤에 남는 세금',
                                     '9편 제척기간 5년에서 10년', '10편 위법한 세무조사'])]


def fig_taxcases():
    h = ['<svg viewBox="0 0 560 386" role="img" aria-label="세금판례 열 편이 과세 요건과 '
         '헌법 판단과 기간·절차 세 갈래로 갈린다">']
    h.append('<text x="26" y="22" class="t-head">열 편이 묻는 자리</text>')
    y = 36
    for name, items in _CASES:
        hgt = 26 + len(items) * 20
        h.append('<rect class="k8-open" x="26" y="%d" width="508" height="%d" rx="8"/>' % (y, hgt))
        h.append('<text x="44" y="%d" class="t-step">%s</text>' % (y + 20, name))
        for j, it in enumerate(items):
            h.append('<text x="230" y="%d" class="t-sub">%s</text>' % (y + 20 + j * 20, it))
        y += hgt + 12
    h.append('<text x="26" y="%d" class="t-sub">'
             '요건이 다 맞아도 절차가 어긋나면 세금이 취소된 편이 마지막이다</text>' % (y + 14))
    h.append('</svg>')
    return ''.join(h)


FIG_TAXCASES = (
    3, '열 편이 요건·헌법·절차 세 자리로 갈린다',
    fig_taxcases(),
    '예고된 열 편을 묻는 자리로 묶었다. 위 칸은 무엇에 매기느냐(요건), 가운데는 누구에게 얼마나 '
    '매기느냐를 헌법이 판단한 편, 아래는 언제까지 어떻게 매기느냐다. 마지막 편이 요점을 '
    '보여준다 — 매길 요건이 다 맞아도 같은 대상을 두 번 조사하거나 고를 이유 없이 골랐다면 '
    '법원이 그 세금을 취소했다. 개별 판결의 선고 연도와 세액은 예고편이라 아직 없다.')


ALL = [FIG_LPDDR6, FIG_PER_GAP, FIG_TESLA, FIG_NASDAQ, FIG_SELECTIVE,
       FIG_JOBS, FIG_ROTATE2, FIG_PER_STEPS, FIG_DURATION, FIG_SCENARIO,
       FIG_BATTERY, FIG_DURATION3, FIG_TRUST, FIG_HIKE, FIG_TAXCASES]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
