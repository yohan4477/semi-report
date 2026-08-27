# -*- coding: utf-8 -*-
"""AI Engineer 번호글에 끼우는 도해.

열쇠는 영상 ID, 값은 `card_lib`의 figs 그대로다 — `[(anchor, 제목, svg, 캡션)]`.

지킬 것 넷.

**anchor는 그 그림이 푸는 번호 바로 앞이다.** 7~19번을 푸는 그림이면 6이다.
판을 먼저 보여 주고 그 아래에서 번호가 하나씩 풀리게 한다.

**한 편에 그림 하나로 제한하지 않는다.** 논지가 꺾이는 자리마다 판을 새로 깐다.

**항목이 셋을 넘으면 좌우가 아니라 위아래로 쌓는다.** 옆으로 늘어놓으면 칸마다
폭이 줄고 글자가 그만큼 작아진다.

**칸은 글자에 맞춰 잰다.** 폭을 손으로 정하면 글자 양옆에 빈자리가 남고 그만큼
글자를 못 키운다. `w_of()`가 가장 긴 줄에 여백 2px만 더해 폭을 낸다. 남는
자리는 칸 사이 틈으로 간다.

**글자 크기는 본문과 같다.** 판 안 글자도 그 아래 설명도 전부 `.95rem`이다.
전에는 그림을 19px로 키웠는데, `svg.epoch`가 `width:100%`라 판이 화면 폭을 따라
늘었다 줄었다 하면서 글자도 같이 스케일됐다 — 넓은 화면에서는 본문보다 크고
좁은 화면에서는 본문보다 작았다. 그래서 판을 좁게(520px) 잡고 글자를 본문과 같은 값으로 맞춘다. 화면에는
`width:100%; max-width:520px`으로 내보내므로 **옆으로 스크롤하는 일이 없다** —
자리가 520보다 넓으면 배율이 1이라 `.95rem`이 그대로 그려지고, 좁으면 판이
줄어든다. 판을 넓게 잡을수록 배율 1이 깨지는 창이 늘어난다.

배치는 `scratchpad/check_fig.py`가 본다. 그 검사기는 붓 이름(fig-b·fig-st…)으로
글자 폭을 갈라 재므로 이 장 도해도 제대로 걸린다.
"""

W = 520.0        # 내보내는 판 폭. 좁게 잡는 이유는 스크롤을 안 내려고다 —
                 # 776은 데스크톱 슬롯에 꼭 맞아서 창이 조금만 좁아도 옆으로 밀렸다
CHW = 15.6       # .95rem(15.2px) 한글 한 글자 폭. 본문 글자와 같은 값이다
PAD = 2          # 칸 좌우 여백. 글자에 자리를 다 준다
LH = 23          # 줄 간격
GAP = 16         # 칸 사이 틈


def w_of(*groups):
    """글줄들을 담는 데 필요한 칸 폭."""
    longest = max(len(t) for g in groups for t in g)
    return round(longest * CHW + 2 * PAD)


def box(x, y, w, h, lines, cls='fig-box', tcls='fig-b'):
    out = ['  <rect x="%g" y="%g" width="%g" height="%g" rx="9" class="%s"/>' % (x, y, w, h, cls)]
    cx, n = x + w / 2, len(lines)
    top = y + h / 2 - (n - 1) * LH / 2 + 6
    for i, t in enumerate(lines):
        assert len(t) * CHW <= w + 1, '칸(%g)보다 넓은 글: %r' % (w, t)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="%s">%s</text>'
                   % (cx, top + i * LH, tcls, t))
    return out


def mid(y, h, lines, cls='fig-box', tcls='fig-b'):
    """글자에 맞춰 재고 판 가운데에 앉히는 상자. 폭을 판 끝까지 늘리면
    짧은 글이 넓은 칸 한가운데 떠서 들여쓴 것처럼 보인다."""
    w = w_of(lines)
    return box((W - w) / 2, y, w, h, lines, cls, tcls)


def head(x, y, w, t):
    """칸 위 열 이름. 네모 없이 글자만."""
    assert len(t) * CHW <= w + 1, '칸(%g)보다 넓은 열 이름: %r' % (w, t)
    return ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>' % (x + w / 2, y, t)]


def arrow(x1, x2, y, t='', back=False):
    m = 'marker-start="url(#aieArwL)"' if back else 'marker-end="url(#aieArw)"'
    out = ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" %s/>' % (x1, y, x2, y, m)]
    if t:
        assert len(t) * CHW <= (x2 - x1) + 28, '화살표(%g)보다 넓은 말: %r' % (x2 - x1, t)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
                   % ((x1 + x2) / 2, y - 12, t))
    return out


def down(x, y1, y2):
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
            % (x, y1, x, y2)]


def legend(items, y):
    out, x = [], 0
    for cls, t in items:
        out.append('  <rect x="%g" y="%g" width="14" height="14" rx="3" class="fig-box %s"/>' % (x, y, cls))
        out.append('  <text x="%g" y="%g" class="fig-lg">%s</text>' % (x + 22, y + 12, t))
        x += 22 + len(t) * CHW + 30
    assert x <= W, '범례가 판보다 넓다'
    return out


def svg(h, parts, alt):
    return ('<svg class="epoch" viewBox="0 0 %g %g" role="img" aria-label="%s">\n'
            '  <defs>\n'
            '    <marker id="aieArw" viewBox="0 0 10 10" refX="9" refY="5"\n'
            '            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            '      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '    <marker id="aieArwL" viewBox="0 0 10 10" refX="1" refY="5"\n'
            '            markerWidth="7" markerHeight="7">\n'
            '      <path d="M10 0 L0 5 L10 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '  </defs>\n' % (W, h, alt)) + '\n'.join(parts) + '\n</svg>'


def table(specs, clss, heads=None, y0=30, gap=GAP, arrows=True):
    """세로로 쌓는 판. 칸 폭은 열마다 가장 긴 글에 맞춘다. 남는 자리는 틈으로."""
    ncol = len(clss)
    ws = [w_of(*([r[c] for r in specs] + ([[heads[c]]] if heads else []))) for c in range(ncol)]
    assert sum(ws) + gap * (ncol - 1) <= W + 1, '표가 판보다 넓다'
    xs, x = [], 0.0
    for w in ws:
        xs.append(x)
        x += w + gap
    rh = max(len(l) for r in specs for l in r) * LH + 26
    out = []
    if heads:
        for c in range(ncol):
            out += head(xs[c], y0 - 10, ws[c], heads[c])
    for i, r in enumerate(specs):
        y = y0 + i * (rh + gap)
        for c in range(ncol):
            out += box(xs[c], y, ws[c], rh, r[c], clss[c])
        if arrows and i < len(specs) - 1:
            out += down(xs[0] + ws[0] / 2, y + rh + 2, y + rh + gap - 2)
    return out, y0 + len(specs) * (rh + gap) - gap


def band(items, y, h, gaps=None):
    """가로 한 줄. items = [(줄들, 클래스)] 또는 ('>', 말) 화살표.

    gaps를 안 주면 남는 자리를 화살표 수로 나눠 고르게 벌린다. 손으로 찍어 두면
    판 폭을 줄일 때 그대로 넘친다 — 도해 스킬 「좌표는 사람이 찍지 않는다」."""
    if gaps is None:
        used = sum(w_of(it[0]) for it in items if it[0] != '>')
        narw = sum(1 for it in items if it[0] == '>')
        assert narw and used < W, '틈을 나눌 자리가 없다'
        gaps = [(W - used) / narw] * narw
    gaps = list(gaps)
    out, x = [], 0.0
    for it in items:
        if it[0] == '>':
            g = gaps.pop(0)
            out += arrow(x + 4, x + g - 4, y + h / 2, it[1], len(it) > 2 and it[2])
            x += g
        else:
            lines, cls = it
            w = w_of(lines)
            out += box(x, y, w, h, lines, cls)
            x += w
    assert x <= W + 1, '줄이 판보다 넓다: %g' % x
    return out, x


# ══ 신호에서 PR까지 (9HbzAWnKbo4) ═════════════════════════════════════

_a1, _ = band([(['오류가 남'], 'fig-box'), ('>', '깨움'),
               (['사람이 빈손으로 뒤짐'], 'fig-box fig-human'), ('>', '고침'),
               (['수정'], 'fig-box')], 44, 62)
_a2, _ = band([(['오류가 남'], 'fig-box'), ('>', '붙음'),
               (['에이전트가 먼저 붙어', '기록·로그·저장소를', '한자리에 모음'], 'fig-box fig-agent'),
               ('>', '이슈'), (['사람이', '검토부터 시작'], 'fig-box fig-human')], 150, 104)
_P1A = svg(310,
    head(0, 30, 120, '예전') + _a1
    + head(0, 136, 120, '지금') + _a2
    + legend([('fig-human', '사람이 붙는 자리'), ('fig-agent', '에이전트가 붙는 자리')], 278),
    '예전에는 오류가 사람을 깨워 사람이 빈손으로 뒤졌고, 지금은 에이전트가 먼저 붙어 증거를 모아 두면 사람이 검토부터 시작한다')

_P1A_CAP = ('같은 일을 하는데 <b>사람이 붙는 자리만 앞에서 뒤로</b> 옮겨간다. '
            '예전에는 오류가 사람을 깨웠고 사람이 빈손으로 화면을 뒤졌다. '
            '지금은 에이전트가 먼저 붙어 실행 기록·로그·저장소를 한자리에 모아 이슈를 만들어 두고, '
            '사람은 증거가 갖춰진 상태에서 검토부터 시작한다 — 발표자가 「대응자에서 검토자로」라고 부른 자리 바꿈이다.')

_L1 = ['코드가 밟을 수 있는 경로']
_L2 = ['실제로 밟은 경로']
_LW = w_of(['저장소'] + _L1, ['실행 기록 · 로그'] + _L2)
_B1L = ['스킬이 실행 중 만든', '임시 파일까지 저장소 안으로',
        '끌어와 벌어진 일과', '코드를 한자리에 둔다']
_RX = _LW + 60
_P1B = svg(232,
    box(0, 10, _LW, 76, ['저장소'] + _L1)
    + box(0, 104, _LW, 76, ['실행 기록 · 로그'] + _L2)
    + arrow(_LW + 8, _RX - 8, 48) + arrow(_LW + 8, _RX - 8, 142)
    + box(_RX, 32, w_of(_B1L), 126, _B1L, 'fig-box fig-agent')
    + legend([('fig-agent', '스킬이 하는 일')], 198),
    '저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를 알려주고 스킬이 둘을 한자리에 모은다')

_P1B_CAP = ('둘 중 하나만으로는 못 고친다. <b>저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를</b> '
            '알려준다. 스킬이 하는 일은 실행 중에 만든 임시 파일까지 저장소 안으로 끌어와 둘을 같은 자리에 놓는 것이고, '
            '발표자는 이 조합이 스킬을 조립 가능하게 만드는 핵심이라고 한다.')

_SW = w_of(['시그널'])
_SX = _SW + 110
_P1C = svg(238,
    box(0, 72, _SW, 76, ['시그널'], 'fig-box fig-agent')
    + arrow(_SW + 8, _SX - 8, 50, '갈래 1') + arrow(_SW + 8, _SX - 8, 160, '갈래 2')
    + box(_SX, 12, w_of(['앤트로픽이 관리하는 매니지드 에이전트']), 76,
          ['앤트로픽이 관리하는 매니지드 에이전트', '연결이 회사 밖으로 나감'])
    + box(_SX, 122, w_of(['앤트로픽이 관리하는 매니지드 에이전트']), 76,
          ['자사 VPC 안에 세운 샌드박스', '연결이 회사 안에 머묾'], 'fig-box fig-human')
    + legend([('fig-human', '우버·부킹이 고른 쪽')], 212),
    '시그널은 앤트로픽 매니지드 에이전트로 돌릴 수도 있고 자사 VPC 안 샌드박스로 돌릴 수도 있다')

_P1C_CAP = ('갈래가 둘인 이유는 기술이 아니라 <b>고객이 프로덕션 시스템을 앤트로픽에 직접 연결하고 싶어 하지 않기 때문</b>이다. '
            '우버와 부킹은 자사 VPC(가상 사설 클라우드, 회사 전용으로 격리된 클라우드망) 안에 샌드박스를 세워 '
            '연결을 바깥으로 내보내지 않고 쓴다.')


# 「운전대를 주지 마라」의 번호글 도해 넷은 지웠다. 그 카드는 보고서 형식으로
# 바뀌면서 아래 RFIGS의 두 장을 쓴다 — 남겨 두면 화면에 안 나가는 판이 빌드만 붙잡는다.
_BW = (W - GAP) / 2      # 좌우 두 칸으로 가르는 판에서 한 칸 폭


# ══ 일하면서 배우는 에이전트 (k35LeKZEhiE) ═════════════════════════════

_p2, _p2b = table([[['한 턴 문답'], ['롤아웃 진행·형식·채점'], ['없음']],
                   [['합성 환경'], ['오케스트레이터·샌드박스'], ['환경 상태']],
                   [['남의 하니스'], ['모델 엔드포인트', '요청·응답 기록'], ['오케스트레이션 전체']],
                   [['에이전트 시민'], ['없음'], ['모델이 스스로', '평가·개선']]],
                  ['fig-box fig-stage', 'fig-box fig-inside', 'fig-box fig-outside'],
                  heads=['단계', '훈련 스택 안', '훈련 스택 밖'])
_P2A = svg(_p2b + 42,
    _p2 + legend([('fig-inside', '훈련 스택 안'), ('fig-outside', '훈련 스택 밖')], _p2b + 14),
    '포스트트레이닝 네 단계에서 훈련 스택 안에 남는 것과 밖으로 나간 것')

_P2A_CAP = ('아래로 내려갈수록 <b>훈련 스택이 쥐고 있던 것이 한 겹씩 바깥으로 나간다.</b> '
            '한 턴 문답에서는 롤아웃을 어떻게 돌리고 어떻게 포맷하는지까지 스택 안에서 통제했는데, '
            '남의 하니스로 오면 스택 안에 남는 것은 모델 완성 엔드포인트와 요청·응답을 기록하는 장치뿐이다. '
            '통제를 놓는 대신 실제 프로덕션 환경을 그대로 쓰게 되지만, 그만큼 거기서 뽑아낼 학습 신호도 줄어든다.')

_P2B = svg(292,
    box(0, 0, _BW, 44, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(_BW + GAP, 0, _BW, 44, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(0, 58, _BW, 56, ['도구 호출의 약 10%가 실패'])
    + box(_BW + GAP, 58, _BW, 56, ['타임아웃난 롤아웃은 뺌'])
    + down(_BW / 2, 118, 138) + down(_BW + GAP + _BW / 2, 118, 138)
    + box(0, 142, _BW, 56, ['길게 답할수록 빠질 확률↑'])
    + box(_BW + GAP, 142, _BW, 56, ['0점보다 빠지는 쪽이 이득'])
    + down(_BW / 2, 202, 222) + down(_BW + GAP + _BW / 2, 202, 222)
    + box(0, 226, _BW, 56, ['모델이 답을 짧게 냄'], 'fig-box fig-bad')
    + box(_BW + GAP, 226, _BW, 56, ['모델이 일부러 타임아웃'], 'fig-box fig-bad'),
    '도구 호출 10퍼센트 실패는 모델이 답을 짧게 내게 만들었고, 타임아웃 롤아웃을 뺀 것은 모델이 일부러 타임아웃을 내게 만들었다')

_P2B_CAP = ('발표자가 든 두 사례다. <b>환경의 사소한 버릇을 모델이 그대로 배운다.</b> '
            '리워드 함수에는 길이 벌점이 전혀 없었는데도 답이 짧아졌고, 타임아웃난 롤아웃을 훈련에서 걸러내자 '
            '모델이 도구 호출을 남발해 스스로 타임아웃을 냈다. 발표자는 환경 충실도와 리워드 해킹이 결국 같은 문제라고 한다.')

_p2c, _p2cb = table([[['자기증류'], ['스스로 만든 답에서 새 행동을 심음', '아직 좁은 범위만 성공']],
                     [['자동화된', '데이터 파이프라인'], ['트레이스를 훑어 실패 사례를 다시 먹임', '지금은 사람이 손으로 함']],
                     [['정성적', '피드백 흡수'], ['점수 대신 글로 된 반응만 남는 자리에서', '그것만으로 모델을 고침']]],
                    ['fig-box fig-stage', 'fig-box fig-agent'], y0=8, arrows=False)
_P2C = svg(_p2cb + 10, _p2c,
           '통제를 놓은 자리를 메우는 연구 방향 셋 — 자기증류, 자동화된 데이터 파이프라인, 정성적 피드백 흡수')

_P2C_CAP = ('앞 단계에서 놓아 버린 통제를 무엇으로 메울지에 대한 답이다. 셋 다 <b>아직 열린 연구 질문</b>이고, '
            '특히 트레이스를 훑어 실패 사례를 골라내는 일은 지금도 사람이 손으로 하고 있다고 발표자가 밝힌다.')


FIG_CSS = """
  .uc-fig .fig-box{fill:var(--surface,#fff);stroke:var(--ink-3);stroke-width:1.2}
  .uc-fig .fig-human{fill:var(--epoch-keybg)}
  .uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--epoch-teal);stroke-width:1.6}
  .uc-fig .fig-stage{fill:var(--sunk,rgba(127,127,127,.10))}
  .uc-fig .fig-inside{fill:var(--epoch-keybg)}
  .uc-fig .fig-outside{fill:var(--surface,#fff);stroke-dasharray:4 3}
  .uc-fig .fig-bad{fill:var(--surface,#fff);stroke:var(--epoch-coral);stroke-width:1.6}
  /* 글자는 19px. 본문 번호글(.95rem)보다 크게 둔다 — 그림이 먼저 읽혀야 한다 */
  /* 판 안 글자는 전부 본문과 같은 .95rem이다. 굵기로만 층을 가른다 —
     크기로 가르면 판이 화면 폭에 따라 스케일될 때 본문과 어긋난다 */
  .uc-fig .fig-b{fill:var(--ink);font-size:.95rem;font-weight:600}
  .uc-fig .fig-st{fill:var(--ink);font-size:.95rem;font-weight:800}
  .uc-fig .fig-hd{fill:var(--ink-3);font-size:.95rem;font-weight:800}
  .uc-fig .fig-e{fill:var(--ink-3);font-size:.95rem;font-weight:700}
  .uc-fig .fig-lg{fill:var(--ink-3);font-size:.95rem;font-weight:650}
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:2;fill:none}
"""

FIGS = {
    '9HbzAWnKbo4': [
        (6,  '오류가 났을 때 누가 먼저 붙나', _P1A, _P1A_CAP),
        (21, '무엇을 모아야 고칠 수 있나', _P1B, _P1B_CAP),
        (33, '연결을 어디로 내보내나', _P1C, _P1C_CAP),
    ],
    'k35LeKZEhiE': [
        (6,  '단계마다 훈련 스택이 무엇을 놓는가', _P2A, _P2A_CAP),
        (33, '환경에 난 틈을 모델이 배운다', _P2B, _P2B_CAP),
        (47, '통제를 놓은 자리를 무엇으로 메우나', _P2C, _P2C_CAP),
    ],
}


# ══ 보고서 형식 카드가 부르는 판 ═══════════════════════════════════════
#
# 여기만 SVG가 아니라 **HTML**이다. 이유는 글자 크기 하나다.
#
# SVG는 viewBox를 화면 폭에 맞춰 늘였다 줄였다 하므로 판이 좁아지면 판 안 글자도
# 같이 준다. 휴대폰에서 카드 안 자리가 300px쯤인데 판을 520으로 내보내면 배율이
# 0.6이 되고 글자가 9px로 앉는다 — 본문 15.2px와 나란히 놓이면 바로 티가 난다.
# 판을 300으로 좁히면 이번엔 데스크톱에서 초라해진다. SVG로는 둘 다 못 잡는다.
#
# 이 두 장은 상자와 화살표뿐이라 SVG일 이유가 없다. HTML로 짜면 글자는 본문과
# 같은 `.95rem` 하나로 고정되고, 자리가 좁아지면 칸이 옆이 아니라 아래로 쌓인다.
# 판 폭·글자 폭을 재는 일이 통째로 사라지므로 겹침·넘침 사고도 같이 사라진다.
#
# 값은 `[(제목, 마크업, 캡션)]`으로 SVG 때와 같다 — `card_lib.fig_html`이 그대로 받는다.


def _box(kind, head, lines):
    """판 안의 칸 하나. kind는 붓 이름(empty·harness·model)."""
    return ('<div class="rf-box rf-%s"><b>%s</b>%s</div>'
            % (kind, head, ''.join('<span>%s</span>' % t for t in lines)))


def _msg(who, t, back=False):
    """칸과 칸 사이에 오가는 것 하나.

    **보내는 쪽 이름을 말 안에 박는다.** 라벨만 가운데 띄워 놓으면 누가 하는 말인지가
    화살촉 방향에만 걸리고, 사용자는 둘 다 하네스가 하는 말로 읽었다. 이 발표는
    「모델이 제안하고 하네스가 결정한다」가 요점이라 그 오독이 주장을 뒤집는다.
    선은 받는 쪽에 화살촉이 붙고, 칸이 세로로 쌓이면 선을 숨기고 이름만 남긴다."""
    line = '<i class="rf-track%s" aria-hidden="true"></i>' % (' is-back' if back else '')
    lab = '<em><b>%s</b><span>%s</span></em>' % (who, t)
    return ('<div class="rf-msg%s">%s</div>'
            % (' is-back' if back else '', (line + lab) if back else (lab + line)))


def _pair(cap, left, msgs, right):
    return ('<div class="rf-row"><p class="rf-cap">%s</p><div class="rf-pair">%s'
            '<div class="rf-msgs">%s</div>%s</div></div>'
            % (cap, left, ''.join(msgs), right))


def _legend(items):
    return ('<div class="rf-legend">%s</div>'
            % ''.join('<span><i class="rf-sw rf-%s"></i>%s</span>' % (k, t) for k, t in items))


def _chain(items, mark=None, links=None):
    """무엇이 무엇을 거쳐 가나. 칸을 늘어놓고 사이마다 화살표를 둔다.

    items = [(머리, 아래 설명)]. mark를 주면 그 번째 칸(1부터)만 붓을 달리해
    「여기가 끝이다」를 표시한다. links를 주면 칸 사이 화살표에 이름을 붙인다 —
    두 칸을 잇는 것이 프로토콜처럼 이름을 가진 것일 때 쓴다.
    자리가 좁아지면 옆이 아니라 아래로 쌓인다."""
    links = list(links or [])
    out = []
    for i, (head, sub) in enumerate(items, 1):
        if i > 1:
            lab = links[i - 2] if len(links) >= i - 1 else ''
            out.append('<div class="rf-link"><em>%s</em><i class="rf-step" aria-hidden="true"></i></div>'
                       % lab if lab else '<i class="rf-step" aria-hidden="true"></i>')
        kind = 'harness' if mark == i else 'model'
        out.append('<div class="rf-box rf-%s"><b>%s</b><span>%s</span></div>' % (kind, head, sub))
    return '<div class="rfig"><div class="rf-chain">%s</div></div>' % ''.join(out)


def _fan(ins, rest):
    """여럿이 하나로 모이는 판. 왼쪽에 입구를 쌓고 화살표 하나로 모은 뒤 나머지를 잇는다.

    일렬로 그리면 「여기저기서 들어와 한 자리로 모인다」가 안 보인다. 모이는 것이
    내용일 때 쓴다 — 상자를 나열하는 대신 모양이 뜻을 말하게 하는 자리다."""
    stack = ('<div class="rf-stack">%s</div>'
             % ''.join('<div class="rf-box rf-model"><b>%s</b></div>' % t for t in ins))
    out = [stack]
    for i, (head, sub) in enumerate(rest):
        out.append('<i class="rf-step" aria-hidden="true"></i>')
        out.append('<div class="rf-box rf-%s"><b>%s</b><span>%s</span></div>'
                   % ('harness' if i < 2 else 'model', head, sub))
    return '<div class="rfig"><div class="rf-chain">%s</div></div>' % ''.join(out)


def _fanout(head, sub, outs):
    """하나가 여럿으로 갈리는 판. _fan의 반대다.

    같은 것이 두 갈래로 쓰인다는 것이 내용일 때 쓴다 — 일렬로 그리면 「갈린다」가 안 보인다."""
    stack = ('<div class="rf-stack">%s</div>'
             % ''.join('<div class="rf-box rf-model"><b>%s</b><span>%s</span></div>' % o
                       for o in outs))
    return ('<div class="rfig"><div class="rf-chain">'
            '<div class="rf-box rf-harness"><b>%s</b><span>%s</span></div>'
            '<i class="rf-step" aria-hidden="true"></i>%s</div></div>' % (head, sub, stack))


# ── 상태가 어디에 있나 ──────────────────────────────────────────────
# 발표의 주장 전부가 이 한 장이다. 같은 네 가지를 위에서는 모델이 쥐고 있고
# 아래에서는 셋이 하네스로 넘어가 있다. 위아래로 겹쳐 놓아 같은 자리를 두 번 보게 한다.
_STATE_4 = ['지금 몇 단계인가', '다음은 무엇인가', '레슨이 끝났는가']
_R_STATE = ('<div class="rfig">'
            + _pair('전부 모델에 맡길 때',
                    _box('empty', '하네스', ['아무것도 안 쥠']),
                    [_msg('하네스가 넘긴다', '전부 다 해 줘')],
                    _box('model', '모델', _STATE_4 + ['무슨 말을 할까']))
            + _pair('하네스가 흐름을 쥘 때',
                    _box('harness', '하네스', _STATE_4),
                    [_msg('하네스가 시킨다', '이 한 가지만 하고 결과를 줘'),
                     _msg('모델이 돌려준다', '결과 하나. 제안일 뿐이다', True)],
                    _box('model', '모델', ['이번 단계의 말 하나']))
            + _legend([('harness', '하네스가 쥔 것'), ('model', '모델이 쥔 것')])
            + '</div>')

_R_STATE_CAP = ('발표의 주장 전부가 이 한 장이다. <b>네 가지 중 셋이 모델에서 하네스로 넘어간다.</b> '
                '모델에 남는 것은 이번 단계에 무슨 말을 할까 하나뿐이고, 그 결과도 제안으로만 받는다. '
                '모델은 지금이 여섯 중 몇 번째인지 끝까지 모른다.')

# ── 한 단계가 도는 순서 (시퀀스) ────────────────────────────────────
# 레인 셋과 생명선과 오가는 화살표를 갖춘 시퀀스 판이다. SVG로 그리면 좁은 화면에서
# 글자가 같이 줄어드니 CSS 그리드로 짠다 — 레인은 열, 걸음은 행이다.
#
# 화살표는 보내는 레인 한가운데에서 받는 레인 한가운데까지 간다. 두 열을 걸치는
# 칸에서 양옆을 25%씩 밀면 정확히 그 자리가 된다(한 열의 절반 = 두 열 폭의 4분의 1).
# 열이 셋이고 이웃한 레인끼리만 주고받는다는 전제가 이 값에 들어 있다.

_ACTORS = [('학생', 'human'), ('하네스', 'harness'), ('모델', 'model')]

# (보내는 레인, 받는 레인, 무엇을) — 레인은 1부터. 둘이 같으면 자기 호출.
#
# **누가 누구에게인지는 안 적는다.** 레인과 화살표가 이미 말하고 있어서 「학생 → 하네스」를
# 덧붙이면 같은 말이 두 번 된다. 말은 제 화살표 바로 위에 얹어 자리로 묶는다.
_STEPS = [(1, 2, '학생이 답을 말함'),
          (2, 3, '이 단계에 필요한 입력만 넘긴다'),
          (3, 2, '행동 하나의 결과를 돌려준다'),
          (2, 2, '결과를 검증하고 상태를 다음으로 넘긴다'),
          (2, 1, '다음 말과 화이트보드')]


def _seq(actors, steps):
    out, last = [], 1 + 2 * len(steps)
    for i, (name, kind) in enumerate(actors, 1):
        out.append('<div class="rq-actor rf-%s" style="grid-column:%d;grid-row:1">%s</div>'
                   % (kind, i, name))
    for i in range(1, len(actors) + 1):
        out.append('<i class="rq-life" style="grid-column:%d;grid-row:2/%d"></i>'
                   % (i, last + 1))
    row = 2
    for frm, to, what in steps:
        if frm == to:
            # 자기 호출은 말을 칸 밖에 얹지 않는다. 빈 칸 위에 글이 떠 있으면
            # 그 칸이 무엇을 하는 자리인지가 안 보인다 — 벌어지는 일을 칸 안에 적는다.
            # 열을 다 걸치고 가운데에 세우면 가운데 레인 위에 앉는다(레인이 셋, 폭이 같다).
            assert frm * 2 == len(actors) + 1, '가운데 레인이 아닌 자기 호출은 자리를 다시 재야 한다'
            out.append('<p class="rq-self" style="grid-column:1/-1;grid-row:%d/%d">%s</p>'
                       % (row, row + 2, what))
        else:
            span = '%d/%d' % (min(frm, to), max(frm, to) + 1)
            back = ' is-back' if to < frm else ''
            out.append('<p class="rq-lab%s" style="grid-column:%s;grid-row:%d">%s</p>'
                       % (back, span, row, what))
            out.append('<i class="rq-arrow%s" style="grid-column:%s;grid-row:%d"></i>'
                       % (back, span, row + 1))
        row += 2
    return '<div class="rfig"><div class="rq">%s</div></div>' % ''.join(out)


_R_SEQ = _seq(_ACTORS, _STEPS)

_R_SEQ_CAP = ('앞 장이 무엇을 누가 쥐는지였다면 이 장은 한 번에 무엇이 오가는지다. '
              '<b>이 왕복이 단계마다 한 번씩, 레슨 하나에 여섯 번 돈다.</b> '
              '네 번째 걸음이 하네스가 저 혼자 하는 일이다 — 모델이 돌려준 결과를 받아들일지 '
              '거기서 정한다. 다만 발표는 턴 하나의 순서를 따로 밝히지 않았다. 하네스가 입력을 주고 '
              '결과를 검증해 상태를 넘긴다는 설명과 화이트보드 하네스가 따로 있다는 설명을 한 턴으로 엮은 것이다.')


# ══ 하니스가 실패한다 (BInpv7lGp1o) ═══════════════════════════════════

_H_BLUEPRINT = _fan(['사람이 친 채팅', '다른 시스템의 알림', '시간이 된 타이머', '살아 있나 신호'],
                    [('어느 대화인가', '들어온 것에 이름표를 붙인다'),
                     ('고치는 문 하나', '그 대화의 상태는 한 곳에서만 바꾼다'),
                     ('도구', '승인과 정책을 지나 실행한다'),
                     ('영수증', '무엇을 했는지 남는다')])

_H_BLUEPRINT_CAP = ('에이전트를 깨우는 신호는 한 곳에서만 오지 않는다. <b>여기저기서 들어온 것을 '
                    '같은 대화끼리 묶고, 그 대화의 상태를 고치는 문은 하나로 둔다.</b> '
                    '문을 하나로 안 두면 뒤에 나오는 「겹친 기록자」 사고가 난다. '
                    '개인 비서형이든 코딩 에이전트든 이 밑구조는 같다고 발표자는 말한다.')

_H_PROOF = _chain([('모델', '제안한다'),
                   ('정책', '허용하거나 거부한다'),
                   ('실행', '시도한다'),
                   ('사용자에게 보이는 경계', '확인되거나 안 된다')], mark=4)

_H_PROOF_CAP = ('증명은 주장이 아니라 사슬이다. <b>툴 결과는 세 번째 칸까지만 증명한다</b> — '
                '내부 경로가 요청을 받아들였다는 뜻이지 사용자가 그것을 봤다는 뜻이 아니다. '
                '웹챗과 TUI에서 메시지 툴이 성공을 보고했는데 화면에는 아무것도 안 뜬 사고가 여기서 났다. '
                '영수증은 마지막 칸에서 끝나야 한다.')


# ══ 코덱스 하니스 뒤편 (shRR1e2HXMk) ═══════════════════════════════════

_CX_PROTO = _chain([('UI', '메시지를 보낸다'),
                    ('하니스', '컨텍스트를 조립하고 도구를 부른다'),
                    ('추론', '모델이 답한다')],
                   mark=2, links=['앱 서버', '리스폰시스 API'])

_CX_PROTO_CAP = ('메시지 한 통이 지나는 길이다. <b>둘 다 남이 갈아 끼울 수 있게 열어 뒀다</b>고 발표자는 말한다. '
                 '앞쪽은 자기 UI를 코덱스 하니스 위에 올리는 자리이고, 뒤쪽은 리스폰시스 API를 따르는 다른 '
                 '모델 제공자를 꽂는 자리다. 오픈AI가 만든 것을 쓰라는 이야기이기도 하다.')

_CX_REVIEW = _seq([('코덱스', 'harness'), ('오토 리뷰', 'model'), ('사람', 'human')],
                  [(1, 2, '하려는 도구 호출과 대화 기록을 넘긴다'),
                   (2, 2, '사용자 권한과 위험 분류로 판단한다'),
                   (2, 1, '괜찮으면 자동으로 승인한다'),
                   (2, 3, '아니면 사람에게 올라간다')])

_CX_REVIEW_CAP = ('샌드박스가 막아선 행동을 사람 대신 판단하는 장치다. '
                  '<b>오토 리뷰는 따로 돌고, 읽기 권한만 갖고, 다른 서브에이전트를 못 띄운다.</b> '
                  '맥락이 판단을 가른다 — 지우라고 시킨 파일이면 괜찮고, 시키지 않은 .git 폴더면 아니다. '
                  '다만 발표는 자동 승인 쪽만 설명하고 승인이 안 났을 때를 따로 다루지 않는다.')


# ══ 내보낼 수 있는 에이전트 만들기 (HT4l0DeP69I) ═══════════════════════
#
# 판은 하나뿐이다. 이 발표에서 흐름이라 할 만한 것이 로컬 에이전트 한 판뿐이고,
# 최소 구성요소 다섯과 베드락 대응물은 항목이 나란히 서는 것이라 표로 내렸다.

_AW_LOOP = _chain([('자연어 입력', '주사위를 굴려 달라고 시킨다'),
                   ('언어모델', '무슨 뜻인지 파악한다'),
                   ('도구 목록', '무엇을 쓸 수 있는지 본다'),
                   ('주사위 굴리기', '그 도구를 실행한다'),
                   ('결과', '15가 나온다')], mark=5)

_AW_LOOP_CAP = ('발표자가 말로 짚은 로컬 에이전트 한 판이다. <b>프레임워크를 하나도 안 쓴 '
                '파이썬 파일 하나</b>이고, 도구도 주사위를 굴리는 난수 생성기 하나뿐이다. '
                '뒤에 베드락에서 다시 만든 에이전트도 같은 순서로 돌아 같은 15를 낸다.')


# ══ 블룸버그 에이전트 확장 (b2GqTDWtg6s) ═══════════════════════════════

_BB_QUERY = _chain([('질의', '지난 다섯 분기 미국 CPI를 묻는다'),
                    ('에이전트', '무슨 뜻인지 파악한다'),
                    ('도메인 판단', '어디로 보낼지 정한다'),
                    ('도구', 'NLP 앞단을 거쳐 데이터를 가져온다'),
                    ('답', '사용자는 이것만 본다')], mark=5)

_BB_QUERY_CAP = ('발표에서 든 실제 사고가 이 길 위에서 났다. 문자 하나가 빠져 <b>월간 자료가 '
                 '분기 자료 자리에 들어왔다.</b> 표를 안 펼치고 답만 내보내는 화면에서는 '
                 '그런 오류가 겹쳐 쌓여도 잡을 길이 없다고 발표자는 말한다.')

_BB_ORG = _chain([('뭉친 조직', '한 팀이 스택을 통째로 쥐고 빠르게 돈다'),
                  ('수평으로 가른 조직', '가드레일 같은 공통 기능을 따로 뺀다')],
                 mark=2, links=['에이전트가 많아지면'])

_BB_ORG_CAP = ('소프트웨어를 어떻게 자르느냐가 조직에 그대로 비친다는 이야기다. '
               '<b>제품 모양을 모를 때는 뭉치는 쪽이 빠르고, 에이전트가 여럿 생긴 뒤에는 가르는 쪽이 낫다.</b> '
               '가드레일이 대표적이다 — 50개 팀이 저마다 금융 자문성 질문을 걸러내는 법을 따로 알아내게 두지 않는다.')


# ══ 더 큰 모델보다 데이터 플라이휠 (6lTxD_oUjXQ) ═══════════════════════
#
# 값은 전부 자막에 나온 것만 쓴다. 라우터를 고치며 쌓인 수(1,224·729·495·140·32·685)는
# 자막이 서로 어떻게 이어지는지를 다 밝히지 않아 판에 안 넣고 표로 내렸다.

_NV_TRADE = ('<div class="rfig">'
             + _pair('같은 라우팅 일을 두 모델에 맡겨 보면',
                     _box('model', '70B 그대로', ['정확도 96%', '첫 토큰까지 26초']),
                     [],
                     _box('harness', '파인튜닝한 1B', ['정확도 94%', '추론 비용 98% 절감']))
             + '</div>')

_NV_TRADE_CAP = ('발표의 주장이 이 한 장이다. <b>그냥 줄이면 안 된다</b> — 손을 안 댄 8B는 같은 '
                 '라우팅에서 정확도가 14% 아래로 떨어진다. 정답 자료를 만들어 파인튜닝하고 나서야 '
                 '1B가 70B보다 2%p 낮은 자리까지 올라온다고 발표자는 말한다.')

_NV_WHEEL = _chain([('모니터링', '사용자 피드백을 모은다'),
                    ('분석·귀속', '오류와 모델 드리프트를 가른다'),
                    ('계획', '모델을 고르고 합성 데이터와 파인튜닝을 잡는다'),
                    ('실행', '주기를 돌리고 정확도와 지연을 좇는다')], mark=4)

_NV_WHEEL_CAP = ('발표자가 든 네 걸음이다. <b>둘째 걸음이 이 틀의 값어치를 정한다</b> — '
                 '무엇이 틀렸는지를 오류와 드리프트로 갈라 놓아야 셋째 걸음에서 무엇을 고칠지 정해진다. '
                 '넷째 걸음의 결과가 다시 첫째 걸음으로 들어가 바퀴가 된다.')


# ══ 에이전트로 앱을 만든다는 것 (R30col3UPUg) ═══════════════════════════
#
# 에이전시와 효능 두 축은 판으로 안 그린다. 자막에 놓인 사례가 둘뿐이라
# 네 칸을 그리면 없는 값을 그리게 된다 — 표로 내렸다.

_MS_LADDER = _chain([('단일 체인', '한 줄로 이어 붙인다'),
                     ('분기', '갈림길을 두고 모델이 고르게 한다'),
                     ('완전 에이전틱', '모델에 흐름을 넘긴다')], mark=1)

_MS_LADDER_CAP = ('발표의 주장이 이 순서에 있다. <b>한 줄로 되면 거기서 멈춘다.</b> '
                  '위로 갈수록 모델의 손에 쥐어 주는 것이 늘어나므로, 자율성을 목표로 삼지 말고 '
                  '풀려는 문제가 요구하는 만큼만 올라가라고 말한다.')

_MS_EVAL = _chain([('돌린다', '입력을 에이전트에 넣는다'),
                   ('사람이 본다', '출력을 검토한다'),
                   ('쌓는다', '평가셋에 더한다'),
                   ('다시 돌린다', '늘어난 평가셋으로'),
                   ('실패를 본다', '묶고 간추린다'),
                   ('고칠 것을 낸다', '개선안을 제시한다')], mark=6)

_MS_EVAL_CAP = ('발표자가 순서대로 든 여섯 걸음이다. <b>둘째 걸음에 사람이 들어가는 것이 요점이다</b> — '
                '검토를 거친 것만 평가셋에 쌓이고, 그 평가셋이 다음 판을 잰다. '
                '마지막 걸음의 결과가 다시 첫째로 들어가 바퀴가 된다.')


# ══ 반쯤 자율적인 멀티 에이전트의 UX 원칙 (fmZWvE7yDZo) ═══════════════
#
# 오류율 20%에서 1.5%로 내려간 것은 루프에 에이전트를 더해서가 아니라 모델을 바꿔서다.
# 게다가 앞선 다른 프로젝트 이야기라 루프 판에 그 수를 붙이지 않는다.

_UX_BUILD = _chain([('목표', '무엇을 풀지 정한다'),
                    ('베이스라인', 'AI와 무관한 것으로 잡는다'),
                    ('도구', '에이전트가 쓸 것을 만든다'),
                    ('테스트베드', '재는 자리를 먼저 세운다'),
                    ('에이전트', '마지막에 붙인다')], mark=2)

_UX_BUILD_CAP = ('발표자가 든 만드는 순서다. <b>둘째 자리가 눈에 걸린다</b> — 견줄 기준을 '
                 '에이전트와도 AI와도 무관한 것으로 먼저 잡으라고 말한다. '
                 '에이전트를 맨 마지막에 붙이는 것도 같은 뜻이다.')

_UX_LOOP = _chain([('기본 루프', '한 바퀴 도는 것부터'),
                   ('검증 에이전트', '결과가 맞는지 본다'),
                   ('계획 에이전트', '단계를 먼저 짠다')], mark=3)

_UX_LOOP_CAP = ('블렌더를 다루는 에이전트가 자란 순서다. <b>한 번에 셋을 만든 것이 아니라 '
                '단순한 루프에서 하나씩 붙였다.</b> 발표에 이 세 단계의 효과를 잰 수치는 나오지 않는다.')


# ══ 에이전트에서 정말 어려운 부분 (j_TKDweOsYE) ═══════════════════════

_CF_PARTS = _chain([('클라이언트', '사람과 만나는 자리'),
                    ('AI', '다음에 무엇을 할지 정한다'),
                    ('워크플로', '그 결정을 실제로 집행한다'),
                    ('툴', '바깥에 손을 댄다')], mark=3)

_CF_PARTS_CAP = ('발표자가 에이전트를 자르는 방식이다. <b>셋째 칸을 집행부라고 부른다</b> — '
                 'AI가 정하고 워크플로가 그것을 실행에 옮긴다는 뜻이다. '
                 '어디서 막히는지 짚으려면 이 넷 중 어디인지부터 말해야 한다는 것이 발표의 틀이다.')

_CF_APPROVAL = _seq([('사용자', 'human'), ('에이전트', 'harness'), ('승인자', 'model')],
                    [(1, 2, '채팅으로 카드 발급을 요청한다'),
                     (2, 3, '발급을 멈추고 승인을 요청한다'),
                     (3, 2, '승인이 돌아온다'),
                     (2, 2, '멈춰 둔 도구 호출을 다시 잇는다'),
                     (2, 1, '카드를 발급하고 알린다')])

_CF_APPROVAL_CAP = ('사람이 끼어드는 워크플로가 어려운 이유가 이 순서에 있다. '
                    '<b>승인을 기다리는 동안 도구 호출이 멈춘 채로 살아 있어야 한다.</b> '
                    '승인이 돌아오면 같은 에이전트를 찾아가 그 자리에서 다시 이어야 하고, '
                    '중복 승인과 중복 발급을 막을 상태 검사도 그 사이에 든다.')


# ══ 현장에서 쓰는 MCP (RkVILz06y08) ═══════════════════════════════════

_GH_STAGES = _chain([('코드 완성', '치는 동안 뒤를 이어 준다'),
                     ('채팅', '물어보고 답을 받는다'),
                     ('에이전트 모드', '일 하나를 끝까지 맡긴다')], mark=3)

_GH_STAGES_CAP = ('발표자가 짚은 세 걸음이다. <b>앞의 둘은 사람이 치는 것을 돕고 셋째는 일을 넘겨받는다.</b> '
                  '넘겨받는 쪽으로 오면서 바깥에 연결할 일이 생기고, 그 자리에 MCP가 붙는다.')

_GH_MCP = _chain([('프롬프트', '무엇을 시켰는지 읽는다'),
                  ('판단', 'MCP가 필요한지 정한다'),
                  ('허가', '개발자에게 연결해도 되는지 묻는다'),
                  ('서버 호출', '답을 받고 나서 부른다'),
                  ('질의', '데이터베이스에 묻는다')], mark=3)

_GH_MCP_CAP = ('셋째 칸이 이 흐름의 요점이다. <b>연결은 개발자가 답을 준 뒤에야 일어난다.</b> '
               '깃허브 쪽으로 브랜치를 만들고 PR을 올릴 때도 같은 자리에서 한 번 묻는다고 발표자는 설명한다.')


# ══ 클라우드 규모로 에이전트 굴리기 (WJjInLeaJjo) ═════════════════════

_CS_TOOLS = _chain([('도구 설명', '지식 베이스에 넣어 둔다'),
                    ('검색', '지금 일에 맞는 것을 찾는다'),
                    ('컨텍스트', '찾은 것만 넣는다'),
                    ('모델', '그 안에서 고른다')], mark=2)

_CS_TOOLS_CAP = ('도구가 6,000개면 한 컨텍스트 창에 다 넣고 고르라고 할 수 없다고 발표자가 먼저 인정한다. '
                 '<b>그래서 목록을 넣는 대신 찾아오게 만든다.</b> '
                 '도구 설명을 지식 베이스에 두고 의미로 검색해 관련된 것만 꺼내 온다.')

_CS_MCP = _chain([('로컬', '표준 입출력으로 붙였다'),
                  ('람다', '함수로 올린다'),
                  ('배포', '주소가 나온다'),
                  ('원격 호출', '토큰을 들고 붙어 도구를 부른다')], mark=4)

_CS_MCP_CAP = ('MCP가 한 대 안에서 붙던 것을 바깥으로 내보내는 순서다. '
               '<b>바깥으로 나가면 누구인지 확인할 자리가 생긴다</b> — 인가자와 사용자 풀과 '
               '세션 표가 그래서 함께 붙는다고 발표자는 설명한다.')


# ══ 에이전트 말고 스킬을 만들어라 (CEvIs9y1uog) ═══════════════════════

_SK_OPEN = _chain([('평소', '이름과 설명만 모델에 보인다'),
                   ('필요할 때', '스킬 본문을 읽어 들인다')],
                  mark=2, links=['쓰겠다고 정하면'])

_SK_OPEN_CAP = ('스킬을 수천 개 붙이고도 컨텍스트가 안 터지는 이유다. '
                '<b>목록 전체를 넣지 않고 이름표만 걸어 둔다.</b> '
                '에이전트가 그 스킬을 쓰겠다고 정한 다음에야 본문이 들어온다.')

_SK_STEPS = _chain([('가져온다', 'API를 불러 자료를 끌어온다'),
                    ('정리한다', '파일로 갈무리한다'),
                    ('분석한다', '파이썬으로 돌린다'),
                    ('합친다', '결과를 파일 하나로 낸다')], mark=4)

_SK_STEPS_CAP = ('발표가 든 재무 보고서 예다. <b>네 걸음이 모두 코드로 간다.</b> '
                 '스킬이 특별한 장치라기보다 모델이 코드로 할 일을 적어 둔 것에 가깝다는 뜻이다.')


# ══ 에이전트를 위해 바뀌는 클로드 API (aqW68Is_Kj4) ═══════════════════

_AP_WINDOW = _chain([('들여온다', '창 밖에 있는 도구와 자료를 끌어온다'),
                     ('밖에 둔다', '두었다가 필요할 때만 불러온다'),
                     ('지운다', '지금 안 쓰는 것을 창에서 뺀다')], mark=3)

_AP_WINDOW_CAP = ('컨텍스트 창을 자원 하나로 놓고 손 셋을 붙인 것이 이 발표의 뼈대다. '
                  '<b>창을 키우는 이야기가 아니라 창에 무엇을 넣고 뺄지의 이야기다.</b> '
                  '앞의 둘은 채우는 손이고 셋째만 비우는 손이라 붓을 달리했다.')

_AP_SPLIT = ('<div class="rfig">'
             + _pair('둘이 나눠 갖는 것',
                     _box('model', 'MCP', ['도구와 자료에', '닿게 해 준다']),
                     [],
                     _box('harness', '스킬', ['그것을 쓸 줄 아는', '요령을 준다']))
             + '</div>')

_AP_SPLIT_CAP = ('발표자가 둘을 가르는 자리다. <b>닿는 것과 쓸 줄 아는 것은 다른 문제다.</b> '
                 '도구에 닿아도 어떻게 쓰는지 모르면 소용이 없다는 뜻이라, 둘을 함께 놓아야 한다고 말한다.')


# ══ MCP는 어디로 가나 (v3Fr2JR47KA) ═══════════════════════════════════

_MF_SPLIT = _fanout('MCP 서버 하나', '앱과 도구를 함께 실어 보낸다',
                    [('사람', '앱으로 만진다'),
                     ('모델', '도구로 만진다')])

_MF_SPLIT_CAP = ('발표가 내다보는 자리다. <b>같은 서버가 사람용 화면과 모델용 도구를 함께 낸다.</b> '
                 '지금까지 도구만 내보내던 것을 앱까지 싣는 쪽으로 넓히겠다는 이야기다.')

_MF_CALL = ('<div class="rfig">'
            + _pair('도구를 부르는 두 방식',
                    _box('model', '왕복', ['하나 부르고 결과 받고', '말하고 또 부른다']),
                    [],
                    _box('harness', '묶어서', ['실행 환경 안에서 스크립트로', '여러 호출을 한 번에 엮는다']))
            + '</div>')

_MF_CALL_CAP = ('발표가 든 두 방식이다. <b>왕복은 부를 때마다 모델을 한 번씩 거친다.</b> '
                '실행 환경을 주면 모델이 스크립트를 써서 여러 호출을 한 번에 엮으므로 그 왕복이 사라진다.')


# ══ 코드 모드 (8txf05vVVl4) ═══════════════════════════════════════════

_CM_CALLS = ('<div class="rfig">'
             + _pair('같은 일을 시키는 두 방식',
                     _box('model', 'JSON 왕복', ['도구를 하나씩 부른다', '왕복 여덟 번']),
                     [],
                     _box('harness', '코드 한 벌', ['모델이 코드를 쓴다', 'API 옆에서 한 번에 돈다']))
             + '</div>')

_CM_CALLS_CAP = ('발표의 주장이 이 대비다. <b>왕복은 부를 때마다 모델을 거친다.</b> '
                 '모델에게 코드를 쓰게 하고 그것을 API 바로 옆에서 돌리면 그 왕복이 한 번으로 줄어든다고 '
                 '발표자는 말한다. 여덟 번이라는 수는 발표가 든 예의 값이다.')

_CM_SANDBOX = _chain([('아무것도 못 함', '코드를 돌리는 것 말고는 없다'),
                      ('능력을 준다', '필요한 것만 하나씩 연다'),
                      ('API로 낸다', '열어 준 것만 부를 수 있다'),
                      ('나가는 길도 본다', '바깥으로 나가는 요청을 통제한다')], mark=1)

_CM_SANDBOX_CAP = ('막는 순서가 거꾸로다. <b>다 열어 두고 위험한 것을 막는 대신, 아무것도 못 하는 데서 '
                   '시작해 필요한 것만 연다.</b> 나가는 요청과 연결까지 같은 자리에서 본다고 발표자는 설명한다.')


# ══ 스트랜즈 에이전트 SDK (Q3NreEAdKMc) ═══════════════════════════════

_ST_PIPE = _chain([('읽는다', '디스크에서 파일 하나를 연다'),
                   ('간추린다', '내용을 요약한다'),
                   ('쓴다', '요약을 파일로 남긴다'),
                   ('말한다', '결과를 소리로 낸다')], mark=4)

_ST_PIPE_CAP = ('시연 하나가 도는 순서다. <b>네 걸음이 기본으로 딸려 오는 도구 셋으로만 간다</b> — '
                '읽기와 쓰기와 말하기다. 따로 만든 것 없이 시킨 문장 하나로 이 순서가 돈다는 것이 '
                '이 시연이 보이려는 것이다.')

_ST_MCP = _chain([('클라이언트', '에이전트와 함께 만든다'),
                  ('붙는다', '이미 떠 있는 서버에 연결한다'),
                  ('받아 온다', '서버가 가진 도구 목록을 넘겨받는다'),
                  ('시킨다', '프롬프트를 주면 그 도구로 일한다')], mark=3)

_ST_MCP_CAP = ('바깥 도구가 붙는 순서다. <b>셋째 칸이 요점이다</b> — 서버에 무슨 도구가 있는지를 '
               '미리 적어 두지 않고 붙은 뒤에 목록을 받아 온다. 서버 쪽이 바뀌어도 클라이언트를 '
               '고칠 일이 줄어드는 방식이다.')


# 보고서 형식 카드가 부르는 판. 열쇠는 영상 ID, 값은 {이름: (제목, 마크업, 캡션)}.
RFIGS = {
    'Q3NreEAdKMc': {
        'pipe': ('한 판이 도는 순서', _ST_PIPE, _ST_PIPE_CAP),
        'mcp':  ('바깥 도구가 붙는 순서', _ST_MCP, _ST_MCP_CAP),
    },
    '8txf05vVVl4': {
        'calls':   ('왕복 여덟 번과 한 번', _CM_CALLS, _CM_CALLS_CAP),
        'sandbox': ('샌드박스가 능력을 얻는 순서', _CM_SANDBOX, _CM_SANDBOX_CAP),
    },
    'v3Fr2JR47KA': {
        'split': ('서버 하나가 두 갈래로 쓰인다', _MF_SPLIT, _MF_SPLIT_CAP),
        'call':  ('도구를 부르는 두 방식', _MF_CALL, _MF_CALL_CAP),
    },
    'aqW68Is_Kj4': {
        'window': ('컨텍스트 창을 다루는 손 셋', _AP_WINDOW, _AP_WINDOW_CAP),
        'split':  ('MCP와 스킬은 다른 것을 준다', _AP_SPLIT, _AP_SPLIT_CAP),
    },
    'CEvIs9y1uog': {
        'disclose': ('스킬이 열리는 두 걸음', _SK_OPEN, _SK_OPEN_CAP),
        'steps':    ('스킬이 실제로 하는 일', _SK_STEPS, _SK_STEPS_CAP),
    },
    'WJjInLeaJjo': {
        'tools': ('도구가 6,000개일 때', _CS_TOOLS, _CS_TOOLS_CAP),
        'mcp':   ('MCP를 바깥으로 내보내기', _CS_MCP, _CS_MCP_CAP),
    },
    'RkVILz06y08': {
        'stages': ('코파일럿이 지나온 세 걸음', _GH_STAGES, _GH_STAGES_CAP),
        'mcp':    ('MCP가 붙을 때 무엇이 오가나', _GH_MCP, _GH_MCP_CAP),
    },
    'j_TKDweOsYE': {
        'parts':    ('에이전트를 넷으로 자르면', _CF_PARTS, _CF_PARTS_CAP),
        'approval': ('사람 승인이 끼어드는 자리', _CF_APPROVAL, _CF_APPROVAL_CAP),
    },
    'fmZWvE7yDZo': {
        'build': ('만드는 순서 다섯', _UX_BUILD, _UX_BUILD_CAP),
        'loop':  ('루프가 자란 순서', _UX_LOOP, _UX_LOOP_CAP),
    },
    'R30col3UPUg': {
        'ladder': ('필요한 만큼만 올라가는 사다리', _MS_LADDER, _MS_LADDER_CAP),
        'eval':   ('평가를 바퀴로 만드는 여섯 걸음', _MS_EVAL, _MS_EVAL_CAP),
    },
    '6lTxD_oUjXQ': {
        'trade': ('큰 모델과 작은 모델의 맞바꿈', _NV_TRADE, _NV_TRADE_CAP),
        'wheel': ('데이터 플라이휠 네 걸음', _NV_WHEEL, _NV_WHEEL_CAP),
    },
    'b2GqTDWtg6s': {
        'query': ('질의 하나가 지나는 길', _BB_QUERY, _BB_QUERY_CAP),
        'org':   ('조직이 옮겨 가는 방향', _BB_ORG, _BB_ORG_CAP),
    },
    'HT4l0DeP69I': {
        'loop': ('로컬 에이전트 한 판이 도는 순서', _AW_LOOP, _AW_LOOP_CAP),
    },
    'shRR1e2HXMk': {
        'proto':  ('메시지 한 통이 지나는 길', _CX_PROTO, _CX_PROTO_CAP),
        'review': ('위험한 행동을 누가 판단하나', _CX_REVIEW, _CX_REVIEW_CAP),
    },
    'BInpv7lGp1o': {
        'blueprint': ('하니스 청사진', _H_BLUEPRINT, _H_BLUEPRINT_CAP),
        'proof':     ('증명의 사슬', _H_PROOF, _H_PROOF_CAP),
    },
    'm24UKZomm7k': {
        'state': ('상태가 어디에 있나', _R_STATE, _R_STATE_CAP),
        'seq':   ('한 단계가 도는 순서', _R_SEQ, _R_SEQ_CAP),
    },
}
