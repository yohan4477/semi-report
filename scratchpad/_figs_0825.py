# -*- coding: utf-8 -*-
"""제3자 카드 시범 도해 셋 — 형태별로 한 장씩.

  ① 시간 흐름도   개입이 하루를 못 넘긴 나흘        (회계사 · 바이백 편)
  ② 인과 흐름도   엔 방어가 미 장기금리로 도는 고리 (회계사 · 30년물 편)
  ③ 구조 설명     정크를 층으로 쌓으면 맨 위가 AAA  (미주사 · CLO 편)

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. 막대 높이도 아이콘 개수도 값이다 →
    ①은 높이를 안 쓰고 날짜축 위 상태 둘로, ③은 층 개수를 주장하지 않으려고
    가운데를 「…」로 비운다.
  - 판 위에 글자를 얹지 않는다. 판단은 판 아래 캡션이 말한다.
  - 배치는 scratchpad/check_fig.py 가 본다.
"""

# ── ① 시간 흐름도 — 나흘 ──────────────────────────────────────────────────
# 값은 전부 [260822] 원문 표(L15, L16)에 있는 것만 쓴다. 선으로 잇지 않는다 —
# 이으면 사이 값이 있는 것처럼 읽힌다.
_DAYS = [
    (70,  '화', '5.34%', '10년물 값 없음', 0),
    (215, '수', '급락',   '개입 발표',      1),
    (360, '목', '5.25%', '10년물 4.70%',  0),
    (500, '금', '5.28%', '10년물 4.73%↑', 0),
]


def fig_days():
    h = ['<svg viewBox="0 0 560 226" role="img" aria-label="30년물 금리가 개입 다음날 '
         '되돌아온 나흘">']
    h.append('<line class="lead-line" x1="40" y1="150" x2="540" y2="150"/>')
    for x, day, v30, v10, hit in _DAYS:
        cls = 'good' if hit else 'bad'
        h.append('<circle cx="%d" cy="150" r="7" class="%s"/>' % (x, cls))
        h.append('<text x="%d" y="176" class="t-day" text-anchor="middle">%s</text>' % (x, day))
        h.append('<text x="%d" y="120" class="t-val" text-anchor="middle">%s</text>' % (x, v30))
        h.append('<text x="%d" y="196" class="t-sub" text-anchor="middle">%s</text>' % (x, v10))
    h.append('<text x="40" y="36" class="t-head">30년물</text>')
    h.append('<text x="40" y="216" class="t-head">10년물</text>')
    h.append('<rect class="body" x="150" y="46" width="260" height="30" rx="8"/>')
    h.append('<text x="280" y="66" class="t-msg" text-anchor="middle">'
             '되사기 한도 20억 → 40억 달러</text>')
    h.append('<line class="flow" x1="215" y1="78" x2="215" y2="138"/>')
    h.append('</svg>')
    return ''.join(h)


FIG_DAYS = (
    1, '개입이 하루를 못 넘긴 나흘',
    fig_days(),
    '화요일 값이 2007년 이전 이후 최고였고, 수요일 발표 직후 급락한 뒤 목요일에 '
    '<b>5.25%</b>, 금요일에 <b>5.28%</b> 근접까지 되올랐다. 점을 선으로 잇지 않은 것은 '
    '원문에 하루 사이의 값이 없기 때문이다. 초록 점 하나가 개입이 먹힌 유일한 날이다.')


# ── ② 인과 흐름도 — 엔 방어가 미 국채로 도는 고리 ────────────────────────
# [260823] 원문 L24~L27. 「무엇을 주고 무엇을 받는지」가 줄마다 남게 그린다.
_STEPS = [
    ('엔화 약세', '일본이 방어에 나선다'),
    ('엔을 사려면 달러가 든다', '달러를 어디서 구하나'),
    ('외환자산 최대 항목이 미 국채', '약 1조 1천억 달러'),
    ('그 국채를 팔아 현금화', '미 국채에 매도 압력'),
    ('미국 장기금리 추가 상승', '누르려던 바로 그 값'),
]
_ALT = ('우회로 — 유로를 팔아 엔을 산다', '2026년 8월 초')


def fig_chain():
    y0, step = 30, 44
    h = ['<svg viewBox="0 0 560 %d" role="img" aria-label="엔화 방어가 미 국채 매도를 '
         '거쳐 미국 장기금리로 도는 다섯 단계">' % (y0 + step * len(_STEPS) + 78)]
    for i, (head, sub) in enumerate(_STEPS):
        y = y0 + i * step
        h.append('<rect class="body" x="26" y="%d" width="380" height="34" rx="8"/>' % y)
        h.append('<text x="42" y="%d" class="t-step">%s</text>' % (y + 22, head))
        h.append('<text x="544" y="%d" class="t-sub" text-anchor="end">%s</text>'
                 % (y + 22, sub))
        if i < len(_STEPS) - 1:
            h.append('<line class="flow" x1="60" y1="%d" x2="60" y2="%d"/>'
                     % (y + 36, y + step - 2))
    y = y0 + step * len(_STEPS) + 12
    h.append('<rect class="body" x="26" y="%d" width="380" height="34" rx="8"/>' % y)
    h.append('<text x="42" y="%d" class="t-step">%s</text>' % (y + 22, _ALT[0]))
    h.append('<text x="544" y="%d" class="t-sub" text-anchor="end">%s</text>'
             % (y + 22, _ALT[1]))
    h.append('</svg>')
    return ''.join(h)


FIG_CHAIN = (
    2, '엔을 지키는 값이 미 국채로 돌아온다',
    fig_chain(),
    '일본은 미 국채를 가장 많이 들고 있는 해외 보유국이라, 엔을 사들이는 데 쓸 달러를 '
    '마련하는 경로가 그대로 미 국채 매도가 된다. 맨 아래 줄은 그 경로를 피하려고 고른 '
    '우회로다 — 유로를 팔아 엔을 샀다. 미국 재무장관이 금리와 환율을 같이 봐야 하는 이유가 '
    '이 경로다.')


# ── ③ 구조 설명 — 층 ─────────────────────────────────────────────────────
# 층 개수는 원문에 없다. 세 칸만 두고 가운데를 「…」로 비워 개수를 주장하지 않는다.
_TRANCHES = [
    ('AAA', '먼저 채워진다', 'good'),
    ('…',   '그 사이 등급들', 'mid'),
    ('에쿼티', '먼저 잃는다', 'bad'),
]


def fig_tranche():
    h = ['<svg viewBox="0 0 560 240" role="img" aria-label="정크 등급 대출을 담은 바구니와 '
         '위부터 채워지는 층 구조">']
    h.append('<rect class="body" x="26" y="14" width="180" height="52" rx="10"/>')
    h.append('<text x="116" y="38" class="t-step" text-anchor="middle">레버리지드론</text>')
    h.append('<text x="116" y="56" class="t-sub" text-anchor="middle">BB+ 아래 기업 대출</text>')
    h.append('<line class="flow" x1="210" y1="40" x2="286" y2="40"/>')
    h.append('<text x="248" y="30" class="t-sub" text-anchor="middle">이자·원금</text>')
    for i, (name, desc, kind) in enumerate(_TRANCHES):
        y = 14 + i * 62
        h.append('<rect class="%s-box" x="292" y="%d" width="120" height="46" rx="8"/>'
                 % (kind, y))
        h.append('<text x="352" y="%d" class="t-step" text-anchor="middle">%s</text>'
                 % (y + 29, name))
        h.append('<text x="424" y="%d" class="t-sub">%s</text>' % (y + 29, desc))
        if i < len(_TRANCHES) - 1:
            h.append('<line class="flow" x1="352" y1="%d" x2="352" y2="%d"/>'
                     % (y + 48, y + 60))
    h.append('<text x="26" y="206" class="t-head">채우는 순서</text>')
    h.append('<text x="140" y="206" class="t-msg">위 → 아래</text>')
    h.append('<text x="26" y="228" class="t-head">마르는 순서</text>')
    h.append('<text x="140" y="228" class="t-msg">아래 → 위</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_TRANCHE = (
    2, '정크를 쌓으면 맨 위가 AAA가 되는 자리',
    fig_tranche(),
    '들어온 돈은 반드시 맨 위층부터 채우고, 위가 가득 차 넘쳐야 아래로 간다. 기업들이 '
    '못 갚으면 아래부터 마른다. 재료가 전부 정크여도 아래층이 완충재라 맨 위층이 최고 등급을 '
    '받는 구조다. 가운데를 비워 둔 것은 층이 몇 개인지가 원문에 없기 때문이다.')


FIG_CSS = """
  .uc-fig text.t-head { font-size:11.5px; font-weight:800; fill:var(--ink-3);
    letter-spacing:.04em; }
  .uc-fig text.t-step { font-size:13px; font-weight:700; fill:var(--ink); }
  .uc-fig text.t-msg  { font-size:12.5px; fill:var(--ink-2); }
  .uc-fig text.t-sub  { font-size:11.5px; fill:var(--ink-3); }
  .uc-fig text.t-day  { font-size:13px; font-weight:800; fill:var(--ink-2); }
  .uc-fig text.t-val  { font-size:15px; font-weight:800; fill:var(--ink); }
  .uc-fig .good-box { fill:var(--fig-good-bg,rgba(47,143,107,.12));
    stroke:var(--fig-good,#2f8f6b); stroke-width:1.4; }
  .uc-fig .mid-box  { fill:rgba(127,127,127,.10); stroke:var(--line); stroke-width:1.2;
    stroke-dasharray:4 4; }
  .uc-fig .bad-box  { fill:var(--fig-bad-bg,rgba(194,80,74,.12));
    stroke:var(--fig-bad,#c2504a); stroke-width:1.4; }
"""

ALL = [FIG_DAYS, FIG_CHAIN, FIG_TRANCHE]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
