# -*- coding: utf-8 -*-
"""부동산 카드 도해 다섯 — 2026-08-27 추가분. 이 장 최초의 도해다.

  ① 순위 막대   같은 서울에서 용적률이 넷으로 갈린다 (63빌딩 편)
  ② 순위 막대   시행사가 제 돈을 얼마나 넣나 (선분양·가계부채 편)
  ③ 시간축      정화가 끝나야 삽을 뜬다 (용산공원 편)
  ④ 좌우 대비   사선을 5미터로 눕히면 폭이 3.5미터 넓어진다 (빌라 10평 편)
  ⑤ 하루 시간축 아침에 신고해도 순위는 다음 날 0시에 선다 (이삿날 전세사기 편)

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. 막대 길이와 건물 폭은 전부 요약본에 있는 수치를
    그대로 옮긴 것이고, 원문에 수가 없는 것은 개수로도 그리지 않았다.
  - 판 위에 글자를 얹지 않는다. 판단은 캡션이 말한다.
  - 배치는 scratchpad/check_fig.py 가 본다.

CSS는 _figs_0825.FIG_CSS(t-head·t-step·t-sub·t-val·good-box·mid-box·bad-box)와
card_lib 기본(.body·.flow·.lead-line·.bad·.good)을 쓴다.
"""

# ── ① 용적률 — 같은 서울, 넷으로 갈린 상한 ──────────────────────────────
_FAR = [
    ('CBD 지정 전', '300~400%', 400, 'mid-box'),
    ('CBD 중심상업지역 지정 후', '1,000%대', 1000, 'good-box'),
    ('강남 재건축 아파트', '250%', 250, 'bad-box'),
]
_FW = 330.0 / 1000


def fig_far():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="서울 중심업무지구 용적률이 '
         '300~400퍼센트에서 1000퍼센트대로 올라간 것과 강남 재건축 아파트 250퍼센트를 '
         '나란히 견준 막대">']
    h.append('<text x="26" y="22" class="t-head">용적률 상한</text>')
    for i, (name, val, num, cls) in enumerate(_FAR):
        y = 40 + i * 58
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 12, name))
        h.append('<rect class="%s" x="26" y="%d" width="%.1f" height="24" rx="5"/>'
                 % (cls, y + 20, num * _FW))
        h.append('<text x="%.1f" y="%d" class="t-val">%s</text>'
                 % (26 + num * _FW + 10, y + 38, val))
    h.append('<rect class="body" x="26" y="214" width="508" height="30" rx="8"/>')
    h.append('<text x="44" y="233" class="t-sub">'
             '올려받은 대가가 다르다 — 오피스는 공개공지 약 30%, 재건축은 늘어난 용적률의 절반을 임대주택으로</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_FAR = (
    3, '같은 서울인데 용적률 상한이 넷으로 갈린다',
    fig_far(),
    '막대 길이는 각 자리에 걸린 용적률 상한이다. 을지로·광화문 일대는 중심상업지역으로 '
    '지정되며 <b>300~400%대에서 1,000%대</b>로 올라갔고, 강남 재건축 아파트는 새로 지어도 '
    '<b>250%</b>에 묶여 있다. 이 편이 던지는 물음이 여기서 나온다 — 오피스에는 풀어 준 것을 '
    '주거지역에는 왜 못 푸느냐는 것이다. 다만 올려받은 대가의 성격이 달라 같은 잣대로 견주기 '
    '어렵다는 점은 아래 칸에 따로 적었다.')


# ── ② 시행사 자기자본 — 한국 3%, 미국 30%, 일본 37% ─────────────────────
_EQ = [('한국 시행사 (KDI 집계)', '3%', 3, 'bad-box'),
       ('미국 디벨로퍼', '30%', 30, 'mid-box'),
       ('일본 디벨로퍼', '37%', 37, 'good-box')]
_EW = 330.0 / 37


def fig_equity():
    h = ['<svg viewBox="0 0 560 246" role="img" aria-label="시행사 평균 자기자본 비율이 '
         '한국 3퍼센트, 미국 30퍼센트, 일본 37퍼센트로 갈리는 막대">']
    h.append('<text x="26" y="22" class="t-head">사업에 넣는 제 돈의 비중</text>')
    for i, (name, val, num, cls) in enumerate(_EQ):
        y = 40 + i * 56
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 12, name))
        w = max(num * _EW, 4)
        h.append('<rect class="%s" x="26" y="%d" width="%.1f" height="24" rx="5"/>'
                 % (cls, y + 20, w))
        h.append('<text x="%.1f" y="%d" class="t-val">%s</text>' % (26 + w + 10, y + 38, val))
    h.append('<rect class="body" x="26" y="210" width="508" height="30" rx="8"/>')
    h.append('<text x="44" y="229" class="t-sub">'
             '1천억원 사업에 30억원만 넣고 나머지는 수분양자가 미리 낸 분양대금이 채운다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_EQUITY = (
    2, '제 돈 3%로 짓는다',
    fig_equity(),
    '막대는 시행사가 사업에 직접 넣는 자기자본 비율이다. 한국이 <b>3%</b>, 미국이 '
    '<b>30%</b>, 일본이 <b>37%</b>다. 넣은 돈이 적을수록 사업성을 스스로 검증할 유인이 '
    '줄고, 나머지는 집을 짓기 전에 받은 분양대금과 세입자가 맡긴 전세보증금이 채운다. '
    '이 편이 가계부채와 주택공급을 한 사슬로 묶는 근거가 이 비율이다.')


# ── ③ 용산공원 시간축 — 정화가 끝나야 삽을 뜬다 ─────────────────────────
def fig_yongsan():
    h = ['<svg viewBox="0 0 600 236" role="img" aria-label="인허가와 오염토 정화를 거쳐 '
         '착공 2031~2032년, 입주 2036년 전후로 이어지는 시간축">']
    h.append('<text x="26" y="22" class="t-head">법을 고친다 해도 남는 시간</text>')
    h.append('<line class="lead-line" x1="40" y1="108" x2="578" y2="108"/>')
    h.append('<rect class="mid-box" x="40" y="44" width="180" height="46" rx="8"/>')
    h.append('<text x="58" y="66" class="t-step">인허가 · 영향평가</text>')
    h.append('<text x="58" y="84" class="t-sub">2~3년</text>')
    h.append('<rect class="bad-box" x="228" y="44" width="180" height="46" rx="8"/>')
    h.append('<text x="246" y="66" class="t-step">오염토 정화</text>')
    h.append('<text x="246" y="84" class="t-sub">통상 3~5년</text>')
    for x, lab, sub in ((425, '착공', '2031~2032년'), (535, '입주', '2036년 전후')):
        h.append('<circle cx="%d" cy="108" r="6" class="good"/>' % x)
        h.append('<text x="%d" y="134" class="t-step" text-anchor="middle">%s</text>' % (x, lab))
        h.append('<text x="%d" y="152" class="t-sub" text-anchor="middle">%s</text>' % (x, sub))
    h.append('<text x="26" y="182" class="t-head">정화가 길어진 사례</text>')
    h.append('<rect class="body" x="26" y="192" width="254" height="34" rx="8"/>')
    h.append('<text x="44" y="214" class="t-sub">유엔사 부지 — 세 차례 반복, 17년</text>')
    h.append('<rect class="body" x="292" y="192" width="254" height="34" rx="8"/>')
    h.append('<text x="310" y="214" class="t-sub">캠프킴 — 6년째 진행, 완료 시점 미정</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_YONGSAN = (
    4, '법을 고쳐도 삽은 2031년에야 뜬다',
    fig_yongsan(),
    '두 상자는 착공 전에 반드시 지나야 하는 구간이고, 그 길이가 곧 시간표다. 인허가와 '
    '영향평가에 <b>2~3년</b>, 오염토 정화에 통상 <b>3~5년</b>이 걸려 착공이 빨라야 '
    '<b>2031~2032년</b>, 입주가 <b>2036년 전후</b>가 된다. 아래 두 사례는 정화가 예정대로 '
    '끝나지 않은 경우다 — 유엔사 부지는 조사와 정화를 세 차례 반복해 17년이 걸렸고 캠프킴은 '
    '문화재가 나와 6년째다. 세로 눈금은 없다. 원문이 준 것이 기간과 시점뿐이라 길이를 값으로 '
    '읽지 않는다.')


# ── ④ 사선 규제 — 17미터 건물의 후퇴 거리 ───────────────────────────────
# 값은 요약본에 있는 것만: 17m 높이 · 기존 8.5m · 완화 5m · 차이 3.5m · 3층까지 1.5m
_PPM = 8.0   # 미터당 px. 17m를 136px로 놓는다
_GY = 214.0  # 지표면


def _panel(h, bx, setback, head, sub, cls):
    """경계선에서 setback(미터)만큼 물러선 17미터 건물 한 채를 그린다."""
    x0 = bx + setback * _PPM
    x1 = bx + 220
    top = _GY - 17 * _PPM
    h.append('<text x="%d" y="34" class="t-head">%s</text>' % (bx, head))
    h.append('<line class="lead-line" x1="%d" y1="46" x2="%d" y2="%d"/>' % (bx, bx, _GY))
    h.append('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>'
             % (cls, x0, top, x1 - x0, _GY - top))
    h.append('<line class="flow" style="marker-end:none" x1="%d" y1="%d" x2="%.1f" y2="%d"/>'
             % (bx, _GY + 16, x0, _GY + 16))
    h.append('<text x="%.1f" y="%d" class="t-val">%s</text>' % (bx + 4, _GY + 34, sub))


def fig_setback():
    h = ['<svg viewBox="0 0 560 268" role="img" aria-label="17미터 건물이 대지 경계선에서 '
         '기존 8.5미터에서 완화 후 5미터만 물러서게 되어 폭이 3.5미터 넓어지는 대비">']
    _panel(h, 26, 8.5, '기존', '8.5m 물러남', 'mid-box')
    _panel(h, 300, 5.0, '완화 뒤', '5m 물러남', 'good-box')
    h.append('<line class="lead-line" x1="26" y1="%d" x2="534" y2="%d"/>' % (_GY, _GY))
    h.append('<text x="534" y="%d" class="t-val" text-anchor="end">폭 3.5m 늘어남</text>'
             % (_GY + 34))
    h.append('</svg>')
    return ''.join(h)


FIG_SETBACK = (
    2, '사선을 눕히면 한 층 바닥이 3.5미터 넓어진다',
    fig_setback(),
    '왼쪽이 지금까지, 오른쪽이 이번 대책 뒤다. 두 건물의 높이는 <b>17미터</b>로 같고 대지 '
    '경계선(왼쪽 점선)에서 물러서는 거리만 다르다. 높이의 절반인 <b>8.5미터</b>를 물러서야 '
    '했던 것이 <b>5미터</b>로 바뀌면서 한 층 바닥이 <b>3.5미터</b>만큼 넓어진다. 그만큼 옆 '
    '건물이 받는 햇빛은 줄어든다는 점은 원문도 인정한다. 3층까지는 예전에도 1.5미터만 '
    '띄우면 됐고, 이번에 바뀐 것은 그 위 구간이다.')


# ── ⑤ 이삿날 하루 — 순위가 갈리는 자리 ──────────────────────────────────
def fig_day():
    h = ['<svg viewBox="0 0 600 244" role="img" aria-label="7월 1일 오후 1시 전입신고를 해도 '
         '대항력은 7월 2일 0시에 생기고 그 사이 오후 4시에 설정된 근저당이 앞서는 하루">']
    h.append('<text x="26" y="22" class="t-head">이사한 날 하루 안에서</text>')
    # 세입자가 아직 순위를 못 잡은 구간
    h.append('<rect class="bad-box" x="150" y="96" width="330" height="26" rx="5"/>')
    h.append('<line class="lead-line" x1="60" y1="109" x2="560" y2="109"/>')
    for x, t, who, sub in ((150, '7/1 오후 1시', '세입자', '전입신고 · 확정일자'),
                           (280, '7/1 오후 4시', '은행', '근저당 설정 — 즉시 효력'),
                           (480, '7/2 0시', '세입자', '대항력 발생')):
        cls = 'bad' if who == '은행' else 'good'
        h.append('<circle cx="%d" cy="109" r="6" class="%s"/>' % (x, cls))
        h.append('<text x="%d" y="76" class="t-step" text-anchor="middle">%s</text>' % (x, who))
        h.append('<text x="%d" y="58" class="t-sub" text-anchor="middle">%s</text>' % (x, t))
        h.append('<text x="%d" y="146" class="t-sub" text-anchor="middle">%s</text>' % (x, sub))
    h.append('<rect class="body" x="26" y="172" width="508" height="52" rx="8"/>')
    h.append('<text x="44" y="196" class="t-step">붉은 구간에서 순위가 갈린다</text>')
    h.append('<text x="44" y="216" class="t-sub">'
             '아침에 신고를 마쳐도 대항력이 없어, 그사이 잡힌 근저당이 앞선다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_DAY = (
    1, '아침에 신고해도 순위는 다음 날 0시에 선다',
    fig_day(),
    '가로축은 이사한 날 하루다. 세입자가 <b>7월 1일 오후 1시</b>에 전입신고와 확정일자를 '
    '마쳐도 대항력은 <b>7월 2일 0시</b>에야 생긴다. 그사이 <b>오후 4시</b>에 집주인이 받은 '
    '대출의 근저당은 등기 접수와 동시에 효력이 생겨, 붉게 칠한 구간 동안 세입자는 순위를 '
    '못 잡은 상태로 남는다. 잔금 전에 등기부를 확인하고 들어왔더라도 다음 날 보면 은행보다 '
    '뒤에 서 있게 되는 이유가 이 하루다.')


ALL = [FIG_FAR, FIG_EQUITY, FIG_YONGSAN, FIG_SETBACK, FIG_DAY]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
