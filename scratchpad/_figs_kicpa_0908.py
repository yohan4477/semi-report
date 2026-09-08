# -*- coding: utf-8 -*-
"""회계사 카드 도해 — 2026-09-08 추가분(엘곰·방구퐁 08-31~09-08 열다섯 편) 중 앞 다섯.

  ① 두 레인 타임라인  개발 순서와 탑재 순서가 뒤집혔다 (LPDDR6 편)
  ② 나란한 세로 막대  증권사가 정당하다는 배수와 시장이 매기는 배수 (08-31 시황 편)
  ③ 좌우 두 판       배수는 세 자리, PEG는 기준선의 다섯 배 (테슬라 편)
  ④ 세로 눈금        29,000 아래위로 필자가 적어 둔 자리들 (나스닥 밸류에이션 편)
  ⑤ 나란한 세로 막대  지수는 0.4%대, 반도체는 2~3%대 (09-03 시황 편)

규칙(insight-figure · 글과 도해 확정 규칙):
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


ALL = [FIG_LPDDR6, FIG_PER_GAP, FIG_TESLA, FIG_NASDAQ, FIG_SELECTIVE]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
