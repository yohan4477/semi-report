# -*- coding: utf-8 -*-
"""회계사 카드 도해 둘 — 2026-08-25 추가분.

  ① 시간 흐름도  회의록이 적힌 날과 공개된 날 사이 3주 (FOMC 편)
  ② 좌우 대비    같은 재료를 한국이 하루 먼저 반영했다 (시황 편)

규칙(insight-figure):
  - 원문에 있는 값만 쓴다. ①의 가운데 세 칸은 원문이 이름을 댄 지표 셋(CPI·PPI·고용)이고
    개수를 지어내지 않았다. ②의 종목도 원문이 값을 준 것만이다.
  - 판 위에 글자를 얹지 않는다. 판단은 캡션이 말한다.
  - 배치는 scratchpad/check_fig.py 가 본다.
"""

# ── ① 시간 흐름도 — 회의록의 시차 ────────────────────────────────────────
# 값은 [260824] 원문에 있는 것만: 3.50~3.75% 동결 · 8월 19일 공개 · 3주 · 0.72% · 98.93
_GAP = [
    (26,  '7월 CPI', '헤드라인·근원 둔화'),
    (198, '7월 PPI', '예상보다 약했다'),
    (370, '7월 고용', '부진 + 전월 하향'),
]


def fig_lag():
    h = ['<svg viewBox="0 0 560 286" role="img" aria-label="7월 FOMC 회의와 8월 19일 '
         '회의록 공개 사이 3주 동안 물가와 고용 지표가 약해진 흐름">']
    h.append('<rect class="body" x="26" y="14" width="230" height="54" rx="10"/>')
    h.append('<text x="42" y="38" class="t-step">7월 28~29일 FOMC</text>')
    h.append('<text x="42" y="58" class="t-sub">동결 3.50~3.75% · 다수 위원 긴축론</text>')
    h.append('<line class="flow" x1="262" y1="41" x2="298" y2="41"/>')
    h.append('<rect class="body" x="304" y="14" width="230" height="54" rx="10"/>')
    h.append('<text x="320" y="38" class="t-step">8월 19일 회의록 공개</text>')
    h.append('<text x="320" y="58" class="t-sub">회의로부터 3주 뒤</text>')
    h.append('<text x="26" y="98" class="t-head">그 3주 사이에 나온 것</text>')
    for x, name, sub in _GAP:
        h.append('<rect class="mid-box" x="%d" y="110" width="164" height="52" rx="8"/>' % x)
        h.append('<text x="%d" y="134" class="t-step">%s</text>' % (x + 16, name))
        h.append('<text x="%d" y="152" class="t-sub">%s</text>' % (x + 16, sub))
        h.append('<line class="flow" x1="%d" y1="164" x2="%d" y2="206"/>' % (x + 82, 280))
    h.append('<rect class="bad-box" x="140" y="212" width="280" height="56" rx="10"/>')
    h.append('<text x="280" y="238" class="t-val" text-anchor="middle">'
             '달러 인덱스 −0.72%</text>')
    h.append('<text x="280" y="258" class="t-sub" text-anchor="middle">'
             '98.93 — 매파 회의록이 나온 날</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_LAG = (
    2, '회의록이 적힌 날과 읽힌 날 사이 3주',
    fig_lag(),
    '위 두 상자는 같은 문서의 두 시점이다 — 왼쪽은 위원들이 그렇게 말한 날, 오른쪽은 그 말이 '
    '공개된 날이다. 가운데 세 칸은 그 사이에 새로 나온 지표이고, 셋 다 회의록의 근거를 약하게 '
    '만드는 방향이었다. 그래서 문구는 매파인데 달러는 <b>0.72%</b> 내렸다. 세 칸은 원문이 '
    '이름을 댄 지표만 세운 것이고, 각 지표의 수치는 원문에 없어 방향만 적었다.')


# ── ② 좌우 대비 — 한국이 하루 먼저 ──────────────────────────────────────
# 값은 [260825] 원문에 있는 것만. 왼쪽이 먼저 일어난 일이다.
_KR = [('코스피', '−3.12%'), ('삼성전자', '−8.70%'), ('SK하이닉스', '−3.41%')]
_US = [('엔비디아', '−2.9%'), ('브로드컴', '−2.6%'), ('마이크론', '−5.8%')]


def _panel(h, x, head, sub, rows, kind):
    h.append('<text x="%d" y="26" class="t-head">%s</text>' % (x, head))
    h.append('<rect class="%s-box" x="%d" y="36" width="240" height="112" rx="10"/>'
             % (kind, x))
    for i, (name, val) in enumerate(rows):
        y = 62 + i * 32
        h.append('<text x="%d" y="%d" class="t-step">%s</text>' % (x + 18, y, name))
        h.append('<text x="%d" y="%d" class="t-val" text-anchor="end">%s</text>'
                 % (x + 222, y, val))
    h.append('<text x="%d" y="168" class="t-sub">%s</text>' % (x, sub))


def fig_oneday():
    h = ['<svg viewBox="0 0 560 268" role="img" aria-label="전날 한국 증시 하락과 '
         '그날 밤 미국 반도체 하락을 나란히 놓은 대비">']
    _panel(h, 26, '① 전날 한국 정규장', '삼성전자 하락엔 주주환원 실망이 섞였다',
           _KR, 'bad')
    h.append('<line class="flow" x1="272" y1="92" x2="288" y2="92"/>')
    _panel(h, 294, '② 그날 밤 미국', '금리·유가는 내렸다 — 매크로는 우호적',
           _US, 'bad')
    h.append('<rect class="body" x="26" y="196" width="508" height="56" rx="10"/>')
    h.append('<text x="46" y="220" class="t-step">오늘 국내 반도체를 보는 자리</text>')
    h.append('<text x="46" y="240" class="t-sub">'
             '필자는 추가 폭락이 아니라 시초가 뒤 낙폭을 줄이는지를 본다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_ONEDAY = (
    2, '같은 재료를 한국이 하루 먼저 반영했다',
    fig_oneday(),
    '왼쪽이 먼저 일어난 일이다. 그날 밤 미국은 10년물이 <b>4.698%</b>로 내리고 WTI도 '
    '<b>2.37%</b> 빠졌는데도 반도체만 밀렸다. 밀어낸 것은 금리도 유가도 아니라 <b>8월 26일</b> '
    '엔비디아 실적을 앞둔 경계인데, 그 경계는 전날 한국 장에도 이미 있었다. 여기에 삼성전자는 '
    '<b>90조~110조원</b> 주주환원의 구체성 부족이라는 자기 악재가 겹쳐 하락폭이 가장 컸다. '
    '두 판을 같은 색으로 둔 것은 한쪽이 다른 쪽의 원인이 아니기 때문이다.')


ALL = [FIG_LAG, FIG_ONEDAY]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
