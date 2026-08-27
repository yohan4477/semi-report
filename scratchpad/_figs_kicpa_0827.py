# -*- coding: utf-8 -*-
"""회계사 카드 도해 다섯 — 2026-08-27 추가분(엘곰 08-25~08-27 다섯 편).

  ① 좌우 대비   6월 22일 이후 두 진영의 시가총액이 반대로 갔다 (업종 로테이션 편)
  ② 폭 띠       옵션시장이 실적 발표에 매긴 값 ±5.4% (08-26 시황 편)
  ③ 순위 막대   해자라 부르는 대차대조표의 규모 (마진·대차대조표 편)
  ④ 시계열 선   시간외에서 네 번 방향이 바뀐 엔비디아 주가 (08-27 시황 편)
  ⑤ 세로 스택   같은 돈이 대금이자 지분투자로 한 바퀴 돈다 (AI 거품 논쟁 편)

규칙(insight-figure):
  - 원문에 있는 값만 쓴다. 막대 길이와 선의 높이는 전부 원문이 준 수치를 그대로 옮긴 것이고,
    원문에 수가 없는 것은 개수로도 그리지 않았다.
  - 판 위에 글자를 얹지 않는다. 판단은 캡션이 말한다.
  - ⑤는 흐름도 규칙의 「한 줄 세로 스택」이다. 오가는 것이 돈과 물건 둘뿐이라 범례도 두 줄이다 —
    조건부(점선) 선이 없는데 범례에 세워 두면 있는 것으로 읽힌다.
  - 배치는 scratchpad/check_fig.py 가 본다.

CSS는 _figs_0825.FIG_CSS(t-head·t-step·t-sub·t-val·good-box·mid-box·bad-box)와
card_lib의 흐름도 클래스(flow-cash·flow-svc·bx·bx-key·t-cash·t-role)를 쓴다.
"""

# ── ① 좌우 대비 — 6월 22일 이후 두 진영 ─────────────────────────────────
# 값은 [260825] 원문에 있는 것만: +24% / −24% / 1조 5천억 / 2조 6천억 / 37·45 / 59·60
_SCALE = 96.0 / 2.6   # 조 달러당 px. 긴 쪽(2조 6천억)을 96px로 놓고 나머지를 비례로 낸다


def fig_rotate():
    sw = 1.5 * _SCALE
    sc = 2.6 * _SCALE
    h = ['<svg viewBox="0 0 560 300" role="img" aria-label="6월 22일 이후 소프트웨어 '
         '진영 시가총액은 1조 5천억 달러 늘고 반도체 진영은 2조 6천억 달러 줄었다">']
    h.append('<text x="26" y="24" class="t-head">6월 22일 이후 진영별 시가총액</text>')
    h.append('<line class="lead-line" x1="280" y1="34" x2="280" y2="196"/>')
    # 소프트웨어 — 오른쪽으로 늘어난다
    h.append('<rect class="good-box" x="280" y="48" width="%.1f" height="40" rx="6"/>' % sw)
    h.append('<text x="272" y="66" class="t-step" text-anchor="end">소프트웨어</text>')
    h.append('<text x="272" y="84" class="t-sub" text-anchor="end">45개 중 37개 상승</text>')
    h.append('<text x="%.1f" y="74" class="t-val">+1조 5천억 달러</text>' % (280 + sw + 10))
    # 반도체 — 왼쪽으로 줄어든다
    h.append('<rect class="bad-box" x="%.1f" y="120" width="%.1f" height="40" rx="6"/>'
             % (280 - sc, sc))
    h.append('<text x="288" y="138" class="t-step">반도체</text>')
    h.append('<text x="288" y="156" class="t-sub">60개 중 59개 하락</text>')
    h.append('<text x="%.1f" y="146" class="t-val" text-anchor="end">−2조 6천억 달러</text>'
             % (280 - sc - 10))
    h.append('<text x="26" y="192" class="t-sub">막대 길이는 진영 전체 증감액이다. '
             '가운데 세로선이 6월 22일이다</text>')
    # 개별 종목 — 원문이 값을 준 것만
    h.append('<rect class="body" x="26" y="210" width="508" height="70" rx="10"/>')
    h.append('<text x="46" y="234" class="t-step">한 종목과 네 종목</text>')
    h.append('<text x="46" y="256" class="t-sub">'
             '마이크로소프트 한 곳이 약 9천억 달러 불어나는 동안</text>')
    h.append('<text x="46" y="272" class="t-sub">'
             '마이크론·TSMC·Arm·AMD 넷은 합쳐 약 9천5백억 달러가 증발했다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_ROTATE = (
    3, '6월 22일을 사이에 두고 두 진영이 반대로 갔다',
    fig_rotate(),
    '같은 날을 기준선으로 놓고 진영 전체의 시가총액 증감을 좌우로 폈다. 소프트웨어는 '
    '<b>약 1조 5천억 달러</b> 늘고 반도체는 <b>약 2조 6천억 달러</b> 줄어, 줄어든 쪽이 '
    '늘어난 쪽보다 크다. 종목 수를 아이콘으로 세지 않은 것은 원문이 준 것이 비율(45개 중 '
    '37개, 60개 중 59개)이기 때문이다. 아래 상자의 두 줄은 원문이 값을 준 개별 종목만 옮겼다.')


# ── ② 폭 띠 — 옵션시장이 매긴 발표의 몸값 ───────────────────────────────
# 값은 [260826] 원문에 있는 것만: ±5.4% · 약 2,800억 달러
def fig_priced():
    h = ['<svg viewBox="0 0 560 236" role="img" aria-label="옵션시장이 엔비디아 실적 발표 '
         '후 주가가 약 플러스마이너스 5.4퍼센트 움직일 가능성을 가격에 반영했다">']
    h.append('<text x="26" y="24" class="t-head">발표 전날, 옵션시장이 이미 매겨 둔 폭</text>')
    h.append('<rect class="mid-box" x="120" y="46" width="320" height="46" rx="8"/>')
    h.append('<line class="lead-line" x1="280" y1="38" x2="280" y2="100"/>')
    h.append('<text x="280" y="112" class="t-step" text-anchor="middle">실적 발표</text>')
    h.append('<text x="132" y="74" class="t-val">−5.4%</text>')
    h.append('<text x="428" y="74" class="t-val" text-anchor="end">+5.4%</text>')
    h.append('<text x="280" y="74" class="t-sub" text-anchor="middle">'
             '이 폭이 값에 이미 들어 있다</text>')
    h.append('<rect class="body" x="26" y="132" width="240" height="80" rx="10"/>')
    h.append('<text x="46" y="158" class="t-step">시가총액으로 바꾸면</text>')
    h.append('<text x="46" y="182" class="t-val">약 2,800억 달러</text>')
    h.append('<text x="46" y="200" class="t-sub">한 종목 실적이 아니라는 근거다</text>')
    h.append('<rect class="body" x="294" y="132" width="240" height="80" rx="10"/>')
    h.append('<text x="314" y="158" class="t-step">그래서 외국인이 할 일</text>')
    h.append('<text x="314" y="182" class="t-sub">신규 매수가 아니라</text>')
    h.append('<text x="314" y="200" class="t-sub">전날 순매도를 줄이는 쪽이다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_PRICED = (
    4, '발표 전날, 폭은 이미 값에 들어 있었다',
    fig_priced(),
    '띠의 좌우 끝은 옵션시장이 반영한 <b>±5.4%</b>이고, 그 폭을 시가총액으로 환산한 것이 '
    '<b>약 2,800억 달러</b>다. 방향이 아니라 크기만 매겨져 있다는 것이 이 그림의 요점이다 — '
    '그래서 필자는 매수 전환이 아니라 매도 진정을 보라고 적는다. 실제로 다음 날 폭은 이 '
    '범위 안이었지만 방향은 시간외 내내 뒤집혔다(④ 그림).')


# ── ③ 순위 막대 — 해자라 부르는 규모 ────────────────────────────────────
# 값은 [260826] 원문에 있는 것만. 5,000억이 둘인데 성격이 달라 라벨로 갈랐다.
_MOAT = [
    ('보유 유동성', '약 2,500억 달러', 2500, 'mid-box'),
    ('파이낸싱·전력 지원까지 포함', '약 5,000억 달러', 5000, 'good-box'),
    ('미국 6대 금융기관과 주선한 고객 자금조달', '5,000억 달러', 5000, 'mid-box'),
    ('오픈AI 오하이오 데이터센터 20년 임대 보증', '최대 1,050억 달러', 1050, 'mid-box'),
]
_MW = 250.0 / 5000   # 억 달러당 px


def fig_moat():
    h = ['<svg viewBox="0 0 560 268" role="img" aria-label="엔비디아의 유동성과 '
         '고객 파이낸싱 약정 규모를 막대로 견준 그림">']
    h.append('<text x="26" y="22" class="t-head">해자라고 부르는 쪽이 드는 값</text>')
    for i, (name, val, num, cls) in enumerate(_MOAT):
        y = 40 + i * 54
        h.append('<text x="26" y="%d" class="t-sub">%s</text>' % (y + 12, name))
        h.append('<rect class="%s" x="26" y="%d" width="%.1f" height="22" rx="5"/>'
                 % (cls, y + 20, num * _MW))
        h.append('<text x="%.1f" y="%d" class="t-val">%s</text>'
                 % (26 + num * _MW + 10, y + 37, val))
    h.append('</svg>')
    return ''.join(h)


FIG_MOAT = (
    4, '해자가 CUDA에서 이 숫자들로 옮겨갔다는 주장',
    fig_moat(),
    '둘째 칸(<b>약 5,000억 달러</b>)은 첫째 칸의 유동성에 고객사 파이낸싱과 전력 생산 지원을 '
    '더한 값이라 첫째 칸을 포함한다 — 넷을 더하면 안 된다. 셋째 칸은 6대 금융기관과 함께 '
    '주선한 것이라 엔비디아 혼자 대는 돈이 아니고, 넷째 칸은 임대 계약에 대한 보증이라 '
    '부도가 나야 실제로 나가는 돈이다. 같은 분기의 다른 축인 총마진 75%는 성격이 달라 여기 '
    '섞지 않았다.')


# ── ④ 시계열 선 — 시간외에서 네 번 방향이 바뀌었다 ──────────────────────
# 값은 [260827] 원문에 있는 것만: −1.59% · +5.19% · +1.45% · +2.73%
_PTS = [('정규장 마감', -1.59), ('발표 직후', 5.19), ('오후 8시경', 1.45), ('글 작성 시점', 2.73)]
_X0, _DX, _Y0, _YS = 76.0, 140.0, 128.0, 15.0   # y = _Y0 − 값 × _YS


def _py(v):
    return _Y0 - v * _YS


def fig_after():
    h = ['<svg viewBox="0 0 560 250" role="img" aria-label="엔비디아 주가가 정규장 마감 '
         '마이너스 1.59퍼센트에서 시간외 플러스 5.19퍼센트로 뛰었다가 1.45퍼센트로 꺼지고 '
         '다시 2.73퍼센트로 올라온 흐름">']
    h.append('<line class="lead-line" x1="40" y1="%.1f" x2="534" y2="%.1f"/>'
             % (_Y0, _Y0))
    h.append('<text x="34" y="%.1f" class="t-sub" text-anchor="end">0%%</text>' % (_Y0 + 5))
    pts = ' '.join('%.1f,%.1f' % (_X0 + i * _DX, _py(v)) for i, (_, v) in enumerate(_PTS))
    h.append('<polyline class="flow" style="marker-end:none" points="%s"/>' % pts)
    for i, (name, v) in enumerate(_PTS):
        x = _X0 + i * _DX
        y = _py(v)
        h.append('<circle cx="%.1f" cy="%.1f" r="5" class="%s"/>'
                 % (x, y, 'bad' if v < 0 else 'good'))
        lab = ('%+.2f%%' % v).replace('-', '−')
        h.append('<text x="%.1f" y="%.1f" class="t-val" text-anchor="middle">%s</text>'
                 % (x, y - 14 if v >= 0 else y + 26, lab))
        h.append('<text x="%.1f" y="228" class="t-sub" text-anchor="middle">%s</text>'
                 % (x, name))
    h.append('<line class="lead-line" x1="%.1f" y1="40" x2="%.1f" y2="196"/>'
             % (_X0 + _DX / 2, _X0 + _DX / 2))
    h.append('<text x="%.1f" y="210" class="t-head" text-anchor="middle">'
             '실적 발표</text>' % (_X0 + _DX / 2))
    h.append('</svg>')
    return ''.join(h)


FIG_AFTER = (
    2, '컨센서스를 다 넘겼는데 방향이 세 번 바뀌었다',
    fig_after(),
    '세로 눈금은 원문이 시각과 함께 적은 네 값뿐이고 그 사이는 잇는 선이다 — 시간 간격은 '
    '같게 두었으니 기울기를 속도로 읽지 않는다. 실망이나 확신 한쪽으로 판단이 섰다면 시간이 '
    '갈수록 한 방향으로 수렴하는 것이 자연스러운데 그러지 않았다는 것이 필자가 잡는 대목이다. '
    '시간외는 거래량이 얇아 정규장보다 변동이 크다는 단서가 원문에 함께 붙어 있다.')


# ── ⑤ 세로 스택 — 같은 돈이 한 바퀴 돈다 ────────────────────────────────
# 값은 [260827] AI 거품 논쟁 편 원문에 있는 것만:
#   300억(1,100억 중) · 130억 이상 · 6,000억 RPO 중 약 45% · 3,000억 Stargate · 2029/2030
def fig_loop():
    h = ['<svg viewBox="0 0 660 392" role="img" aria-label="엔비디아와 마이크로소프트가 '
         '오픈AI에 돈을 대고 그 돈이 GPU 구매와 클라우드 사용료로 되돌아오는 순환 구조">']
    # 범례 — 이 그림에 실제로 쓰인 두 종류만 세운다
    h.append('<line class="flow-cash" x1="26" y1="18" x2="58" y2="18"/>')
    h.append('<text x="66" y="23" class="t-sub">돈이 흐른다</text>')
    h.append('<line class="flow-svc" x1="176" y1="18" x2="208" y2="18"/>')
    h.append('<text x="216" y="23" class="t-sub">물건·용역이 간다</text>')
    # 1행 — 대는 쪽
    h.append('<text x="26" y="52" class="t-role">대는 쪽</text>')
    h.append('<rect class="bx" x="26" y="62" width="238" height="76" rx="8"/>')
    h.append('<text x="44" y="86" class="t-step">엔비디아</text>')
    h.append('<text x="44" y="106" class="t-sub">오픈AI 자금조달 1,100억 달러 중</text>')
    h.append('<text x="44" y="124" class="t-sub">300억 달러를 출자한다</text>')
    h.append('<rect class="bx" x="288" y="62" width="238" height="76" rx="8"/>')
    h.append('<text x="306" y="86" class="t-step">마이크로소프트</text>')
    h.append('<text x="306" y="106" class="t-sub">130억 달러 이상을 투자하고</text>')
    h.append('<text x="306" y="124" class="t-sub">주 클라우드 공급자를 겸한다</text>')
    h.append('<path class="flow-cash" d="M145,138 V166"/>')
    h.append('<path class="flow-cash" d="M407,138 V166"/>')
    # 2행 — 받는 쪽(이 그림이 뜯어보는 대상이라 강조색)
    h.append('<text x="26" y="186" class="t-role">받는 쪽</text>')
    h.append('<rect class="bx-key" x="26" y="196" width="500" height="72" rx="8"/>')
    h.append('<text x="44" y="220" class="t-step">오픈AI</text>')
    h.append('<text x="44" y="240" class="t-sub">'
             '컴퓨트 비용이 매출을 크게 웃돈다 — 2029년까지 적자,</text>')
    h.append('<text x="44" y="258" class="t-sub">'
             '2030년에야 현금흐름 흑자 전환이 예상된다</text>')
    h.append('<path class="flow-cash" d="M276,268 V300"/>')
    h.append('<text x="286" y="290" class="t-cash">같은 돈이 대금으로 나간다</text>')
    # 3행 — 되돌아가는 자리
    h.append('<text x="26" y="320" class="t-role">되돌아가는 자리</text>')
    h.append('<rect class="bx" x="26" y="330" width="500" height="52" rx="8"/>')
    h.append('<text x="44" y="352" class="t-sub">'
             '엔비디아 GPU 구매 · Azure 클라우드 사용료</text>')
    h.append('<text x="44" y="372" class="t-sub">'
             '오라클과는 3,000억 달러 규모 Stargate 계약을 맺고 있다</text>')
    # 바깥 레일 — 매출로 잡혀 위로 돌아간다
    h.append('<path class="flow-cash" d="M526,356 H600 V100 H530"/>')
    h.append('<text x="620" y="230" class="t-cash" text-anchor="middle" '
             'transform="rotate(-90 620 230)">매출로 잡힌다</text>')
    h.append('</svg>')
    return ''.join(h)


FIG_LOOP = (
    3, '댄 돈이 대금으로 나가 댄 쪽 매출로 돌아온다',
    fig_loop(),
    '위에서 아래로 한 바퀴다. 돈을 댄 두 곳이 동시에 물건과 클라우드를 파는 쪽이라, 오른쪽 '
    '레일을 타고 돌아온 금액이 다시 매출로 잡힌다. 원문이 매출 조작이라고 말하지 않는다는 '
    '점은 그대로 둔다 — 문제 삼는 것은 그 성장률을 외부 수요의 증거로 읽는 일이다. '
    '마이크로소프트 쪽 고리 크기는 공시로 가늠할 수 있다. AI 관련 이행의무잔액 '
    '<b>6,000억 달러</b> 이상 중 약 <b>45%</b>가 오픈AI 관련이다. CoreWeave는 엔비디아가 '
    '지분을 갖고 오라클에 인프라를 대는 자리에 있는데, 선을 더 넣으면 한 바퀴가 안 읽혀 '
    '캡션으로 내렸다.')


ALL = [FIG_ROTATE, FIG_PRICED, FIG_MOAT, FIG_AFTER, FIG_LOOP]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for f in ALL:
        print(f[1], '->', check_fig.hits(f[2]) or 'FAIL 0건')
