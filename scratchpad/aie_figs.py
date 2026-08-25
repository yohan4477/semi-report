# -*- coding: utf-8 -*-
"""AI Engineer 번호글에 끼우는 도해.

번호글은 한 생각에 한 줄이라 「전체가 어떻게 맞물리는지」가 안 잡힌다. 그 한 장을
여기서 그린다. 열쇠는 영상 ID이고 값은 `card_lib`의 figs 그대로다 —
`[(anchor, 제목, svg, 캡션)]`.

지킬 것 셋.

**anchor는 그 그림이 푸는 번호 바로 앞이다.** 7~19번을 푸는 그림이면 6이다.
판을 먼저 보여 주고 그 아래에서 번호가 하나씩 풀리게 한다 — 다 읽은 뒤에 그림이
나오면 그림이 할 일이 없다.

**한 편에 그림 하나로 제한하지 않는다.** 번호가 마흔을 넘으면 끝까지 읽기 힘들다.
논지가 꺾이는 자리마다 판을 새로 깐다.

**항목이 셋을 넘으면 좌우가 아니라 위아래로 쌓는다.** 판은 가로 640에 묶여 있는데
칸을 옆으로 늘어놓으면 칸마다 폭이 줄고 글자가 그만큼 작아진다. 세로로 쌓으면
한 줄이 판 폭을 다 쓰므로 같은 글자가 크게 읽힌다. 훈련 스택 네 단계를 옆으로
늘어놨다가 글자가 안 보인다는 지적을 받고 고쳤다(2026-08-26).

배치는 `scratchpad/check_fig.py`가 검사한다. 그 검사기는 한 글자를 9px로 어림하고
text-anchor를 **태그 속성에서** 읽는데, 이 장 글자는 본문과 같은 15px이라 9px
어림으로는 넉넉해 보이는 칸이 실제로는 넘친다. 아래 헬퍼가 15.5px로 따로 재고
넘치면 멈춘다. 칸 좌우 여백도 6px까지 줄여 글자에 자리를 몰아준다.
"""

# ── 판을 짜는 작은 부품 ────────────────────────────────────────────────
# 자리를 손으로 찍으면 반드시 어긋난다. 칸 폭·줄 간격을 계산해서 내보낸다.
LH = 24          # 상자 안 줄 간격
CHW = 15.5       # 15px 한글 한 글자 실제 폭 어림. 칸 폭을 이걸로 잡는다
PAD = 6          # 칸 좌우 여백. 글자를 키우려고 최소로 둔다


def box(x, y, w, h, lines, cls='fig-box', tcls='fig-b'):
    """네모 하나와 그 안에 세로로 가운데 맞춘 글줄들."""
    out = ['  <rect x="%g" y="%g" width="%g" height="%g" rx="9" class="%s"/>' % (x, y, w, h, cls)]
    cx, n = x + w / 2, len(lines)
    top = y + h / 2 - (n - 1) * LH / 2 + 5
    for i, t in enumerate(lines):
        assert len(t) * CHW <= w - PAD, '칸(%g)보다 넓은 글: %r' % (w, t)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="%s">%s</text>'
                   % (cx, top + i * LH, tcls, t))
    return out


def label(x, y, w, t, tcls='fig-hd'):
    """칸 위에 세우는 열 이름. 네모 없이 글자만."""
    assert len(t) * CHW <= w, '칸(%g)보다 넓은 열 이름: %r' % (w, t)
    return ['  <text x="%g" y="%g" text-anchor="middle" class="%s">%s</text>' % (x + w / 2, y, tcls, t)]


def arrow(x1, x2, y, t='', back=False):
    """가로 화살표. t는 선 위에 붙는다. back이면 머리가 왼쪽에 달린다."""
    head = 'marker-start="url(#aieArwL)"' if back else 'marker-end="url(#aieArw)"'
    out = ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" %s/>'
           % (x1, y, x2, y, head)]
    if t:
        assert len(t) * CHW <= (x2 - x1) + 24, '화살표(%g)보다 넓은 말: %r' % (x2 - x1, t)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
                   % ((x1 + x2) / 2, y - 10, t))
    return out


def down(x, y1, y2):
    """세로 화살표."""
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
            % (x, y1, x, y2)]


def legend(items, y):
    """판 아래 색 딱지. items = [(클래스, 말)]"""
    out, x = [], 0
    for cls, t in items:
        out.append('  <rect x="%g" y="%g" width="13" height="13" rx="3" class="fig-box %s"/>' % (x, y, cls))
        out.append('  <text x="%g" y="%g" class="fig-lg">%s</text>' % (x + 21, y + 11, t))
        x += 25 + len(t) * 15.5 + 24
    assert x <= 680, '범례가 판보다 넓다'
    return out


def svg(h, parts, alt):
    head = ('<svg class="epoch" viewBox="0 0 640 %g" role="img" aria-label="%s">\n'
            '  <defs>\n'
            '    <marker id="aieArw" viewBox="0 0 10 10" refX="9" refY="5"\n'
            '            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            '      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '    <marker id="aieArwL" viewBox="0 0 10 10" refX="1" refY="5"\n'
            '            markerWidth="7" markerHeight="7">\n'
            '      <path d="M10 0 L0 5 L10 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '  </defs>\n' % (h, alt))
    return head + '\n'.join(parts) + '\n</svg>'


def rows(specs, cols, y0=26, rh=58, gap=16, heads=None, arrows=True):
    """세로로 쌓는 판. specs = [[칸1 줄들, 칸2 줄들, …]], cols = [(x, w, 클래스)]."""
    out = []
    if heads:
        for (x, w, _c), t in zip(cols, heads):
            out += label(x, y0 - 8, w, t)
    for i, rowspec in enumerate(specs):
        y = y0 + i * (rh + gap)
        for (x, w, c), lines in zip(cols, rowspec):
            out += box(x, y, w, rh, lines, c)
        if arrows and i < len(specs) - 1:
            out += down(cols[0][0] + cols[0][1] / 2, y + rh + 2, y + rh + gap - 2)
    return out, y0 + len(specs) * (rh + gap) - gap


# ══ 신호에서 PR까지 (9HbzAWnKbo4) ═════════════════════════════════════

_P1A = svg(280,
    box(0, 34, 54, 52, ['예전'], 'fig-tag', 'fig-tag-t')
    + box(64, 34, 118, 52, ['오류가 남'])
    + arrow(186, 226, 60, '깨움')
    + box(232, 34, 212, 52, ['사람이 빈손으로 뒤짐'], 'fig-box fig-human')
    + arrow(448, 488, 60, '고침')
    + box(494, 34, 146, 52, ['수정'])
    + box(0, 152, 54, 84, ['지금'], 'fig-tag', 'fig-tag-t')
    + box(64, 152, 118, 84, ['오류가 남'])
    + arrow(186, 226, 194, '붙음')
    + box(232, 152, 212, 84, ['에이전트가 먼저 붙어', '기록·로그·저장소를', '한자리에 모음'], 'fig-box fig-agent')
    + arrow(448, 488, 194, '이슈')
    + box(494, 152, 146, 84, ['사람이', '검토부터 시작'], 'fig-box fig-human')
    + legend([('fig-human', '사람이 붙는 자리'), ('fig-agent', '에이전트가 붙는 자리')], 254),
    '예전에는 오류가 사람을 깨워 사람이 빈손으로 뒤졌고, 지금은 에이전트가 먼저 붙어 증거를 모아 두면 사람이 검토부터 시작한다')

_P1A_CAP = ('같은 일을 하는데 <b>사람이 붙는 자리만 앞에서 뒤로</b> 옮겨간다. '
            '예전에는 오류가 사람을 깨웠고 사람이 빈손으로 화면을 뒤졌다. '
            '지금은 에이전트가 먼저 붙어 실행 기록·로그·저장소를 한자리에 모아 이슈를 만들어 두고, '
            '사람은 증거가 갖춰진 상태에서 검토부터 시작한다 — 발표자가 「대응자에서 검토자로」라고 부른 자리 바꿈이다.')

_P1B = svg(230,
    box(0, 14, 258, 66, ['저장소', '코드가 밟을 수 있는 경로'])
    + box(0, 100, 258, 66, ['실행 기록 · 로그', '실제로 밟은 경로'])
    + arrow(266, 320, 47)
    + arrow(266, 320, 133)
    + box(328, 34, 312, 112, ['스킬이 실행 중 만든', '임시 파일까지 저장소로 끌어와', '벌어진 일과 코드를', '한자리에 둠'], 'fig-box fig-agent')
    + legend([('fig-agent', '스킬이 하는 일')], 192),
    '저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를 알려주고 스킬이 둘을 한자리에 모은다')

_P1B_CAP = ('둘 중 하나만으로는 못 고친다. <b>저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를</b> '
            '알려준다. 스킬이 하는 일은 실행 중에 만든 임시 파일까지 저장소 안으로 끌어와 둘을 같은 자리에 놓는 것이고, '
            '발표자는 이 조합이 스킬을 조립 가능하게 만드는 핵심이라고 한다.')

_P1C = svg(230,
    box(0, 66, 140, 62, ['시그널'], 'fig-box fig-agent')
    + arrow(148, 202, 48, '갈래 1')
    + arrow(148, 202, 146, '갈래 2')
    + box(210, 14, 430, 66, ['앤트로픽이 관리하는', '매니지드 에이전트 — 연결이 밖으로'])
    + box(210, 114, 430, 66, ['자사 VPC 안에 세운 샌드박스', '연결이 회사 안에 머묾'], 'fig-box fig-human')
    + legend([('fig-human', '우버·부킹이 고른 쪽')], 202),
    '시그널은 앤트로픽 매니지드 에이전트로 돌릴 수도 있고 자사 VPC 안 샌드박스로 돌릴 수도 있다')

_P1C_CAP = ('갈래가 둘인 이유는 기술이 아니라 <b>고객이 프로덕션 시스템을 앤트로픽에 직접 연결하고 싶어 하지 않기 때문</b>이다. '
            '우버와 부킹은 자사 VPC(가상 사설 클라우드, 회사 전용으로 격리된 클라우드망) 안에 샌드박스를 세워 '
            '연결을 바깥으로 내보내지 않고 쓴다.')


# ══ 일하면서 배우는 에이전트 (k35LeKZEhiE) ═════════════════════════════
# 네 단계를 옆으로 늘어놨더니 칸마다 폭이 좁아 글자가 안 보였다. 위아래로 쌓는다.
# 계단이나 막대로 그리면 높이가 수치로 읽히는데 원문에 그런 수는 없다 —
# 네 칸을 같은 크기로 두고 안·밖에 든 것만 이름으로 적는다.

_COLS = [(0, 152, 'fig-box fig-stage'), (164, 232, 'fig-box fig-inside'), (408, 232, 'fig-box fig-outside')]
_P2A_ROWS = [
    [['한 턴 문답'], ['롤아웃 진행·형식', '채점까지'], ['없음']],
    [['합성 환경'], ['오케스트레이터', '샌드박스'], ['환경 상태']],
    [['남의 하니스'], ['모델 엔드포인트', '요청·응답 기록'], ['오케스트레이션 전체']],
    [['에이전트 시민'], ['없음'], ['모델이 스스로', '평가·개선']],
]
_p, _bot = rows(_P2A_ROWS, _COLS, heads=['단계', '훈련 스택 안', '훈련 스택 밖'])
_P2A = svg(_bot + 16, _p, '포스트트레이닝 네 단계에서 훈련 스택 안에 남는 것과 밖으로 나간 것')

_P2A_CAP = ('아래로 내려갈수록 <b>훈련 스택이 쥐고 있던 것이 한 겹씩 바깥으로 나간다.</b> '
            '한 턴 문답에서는 롤아웃을 어떻게 돌리고 어떻게 포맷하는지까지 스택 안에서 통제했는데, '
            '남의 하니스로 오면 스택 안에 남는 것은 모델 완성 엔드포인트와 요청·응답을 기록하는 장치뿐이다. '
            '통제를 놓는 대신 실제 프로덕션 환경을 그대로 쓰게 되지만, 그만큼 거기서 뽑아낼 학습 신호도 줄어든다.')

_P2B = svg(268,
    box(0, 0, 312, 36, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(328, 0, 312, 36, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(0, 48, 312, 54, ['도구 호출의 약 10%가 실패함'])
    + box(328, 48, 312, 54, ['타임아웃난 롤아웃은 훈련에서 뺌'])
    + down(156, 104, 118) + down(484, 104, 118)
    + box(0, 122, 312, 54, ['길게 답할수록 빠질 확률이 커짐'])
    + box(328, 122, 312, 54, ['0점 받느니 빠지는 쪽이 이득'])
    + down(156, 178, 192) + down(484, 178, 192)
    + box(0, 196, 312, 54, ['모델이 답을 짧게 냄'], 'fig-box fig-bad')
    + box(328, 196, 312, 54, ['모델이 일부러 타임아웃을 냄'], 'fig-box fig-bad'),
    '도구 호출 10퍼센트 실패는 모델이 답을 짧게 내게 만들었고, 타임아웃 롤아웃을 뺀 것은 모델이 일부러 타임아웃을 내게 만들었다')

_P2B_CAP = ('발표자가 든 두 사례다. <b>환경의 사소한 버릇을 모델이 그대로 배운다.</b> '
            '리워드 함수에는 길이 벌점이 전혀 없었는데도 답이 짧아졌고, 타임아웃난 롤아웃을 훈련에서 걸러내자 '
            '모델이 도구 호출을 남발해 스스로 타임아웃을 냈다. 발표자는 환경 충실도와 리워드 해킹이 결국 같은 문제라고 한다.')

_DCOLS = [(0, 216, 'fig-box fig-stage'), (228, 412, 'fig-box fig-agent')]
_D_ROWS = [
    [['자기증류'], ['모델이 스스로 만든 답에서', '새 행동을 심음', '아직 좁은 범위만 성공']],
    [['자동화된', '데이터 파이프라인'], ['대량의 트레이스를 훑어', '실패 사례를 골라 다시 먹임', '지금은 사람이 손으로 함']],
    [['정성적', '피드백 흡수'], ['점수 대신 글로 된 반응만 남는 자리에서', '그것만으로 모델을 고침']],
]
_q, _qbot = rows(_D_ROWS, _DCOLS, y0=6, rh=92, gap=16, arrows=False)
_P2C = svg(_qbot + 10, _q,
           '통제를 놓은 자리를 메우는 연구 방향 셋 — 자기증류, 자동화된 데이터 파이프라인, 정성적 피드백 흡수')

_P2C_CAP = ('앞 단계에서 놓아 버린 통제를 무엇으로 메울지에 대한 답이다. 셋 다 <b>아직 열린 연구 질문</b>이고, '
            '특히 트레이스를 훑어 실패 사례를 골라내는 일은 지금도 사람이 손으로 하고 있다고 발표자가 밝힌다.')


# 운전대를 주지 마라 (m24UKZomm7k) ─────────────────────────────────────
# 이해가 어려운 대목은 장면으로 그린다. 한 단계가 어떻게 도는지는 말로 읽으면
# 안 잡히는데, 하네스와 모델이 무엇을 주고받는지 왕복으로 그리면 한눈에 보인다.

_P3A = svg(250,
    box(0, 0, 200, 44, ['하네스'], 'fig-box fig-agent', 'fig-st')
    + box(440, 0, 200, 44, ['모델'], 'fig-box fig-human', 'fig-st')
    + arrow(205, 435, 84, '이 한 가지만 하고 결과를 줘')
    + arrow(205, 435, 126, '결과', back=True)
    + box(0, 150, 200, 60, ['결과를 검증하고', '다음 단계로 넘김'], 'fig-box fig-agent')
    + box(240, 150, 400, 60, ['인트로 → 티치 → 체크', '그레이드 → 어드밴스 → 랩'])
    + legend([('fig-agent', '하네스가 정하는 것'), ('fig-human', '모델이 하는 것')], 222),
    '하네스가 모델에게 한 가지만 시키고 결과를 받아 검증한 뒤 다음 단계로 넘긴다')

_P3A_CAP = ('한 단계가 도는 방식이다. <b>하네스가 모델에게 한 번에 한 가지만 넘기고, 돌아온 결과를 검증한 뒤 '
            '다음 단계를 정한다.</b> 모델은 지금이 여섯 중 몇 번째인지 알 필요가 없다 — 그 기억을 아예 요구하지 않는다. '
            '레슨 하나는 인트로·티치·체크·그레이드·어드밴스·랩으로 이어지는 작은 상태 머신이다.')

_P3B = svg(160,
    box(0, 0, 308, 40, ['모델 하나에 다 맡김'], 'fig-box fig-stage', 'fig-st')
    + box(332, 0, 308, 40, ['단계마다 좁은 계약'], 'fig-box fig-stage', 'fig-st')
    + box(0, 52, 308, 96, ['오퍼스 4.7이', '생각부터 처리까지 다 함', '라이브 튜터에선', '늘 통하지는 않음'])
    + box(332, 52, 308, 96, ['하이쿠 4.5는 대사만', '하네스가 흐름을 쥠', '비용·시간·지연을', '아낌'], 'fig-box fig-agent'),
    '무거운 모델 하나에 다 맡기는 방식과 단계마다 좁은 계약을 주는 방식의 대비')

_P3B_CAP = ('작은 모델을 쓴 것이 먼저가 아니다. <b>흐름을 하네스가 쥐고 나서야 작은 모델로 내려갈 수 있었다.</b> '
            '오퍼스 4.7이 생각부터 처리까지 다 하는 방식은 라이브 튜터처럼 신뢰성·비용·속도가 한꺼번에 필요한 자리에서는 '
            '늘 통하지 않는다고 발표자는 말한다.')

_HCOLS = [(0, 180, 'fig-box fig-stage'), (192, 448, 'fig-box')]
_H_ROWS = [
    [['섹션'], ['지금 무엇을 말하고 무엇을 해야 하는지 입력을 줌']],
    [['화이트보드'], ['화이트보드에 그리는 것을 다룸']],
    [['대기열'], ['대기열을 비우는 것을 다룸']],
    [['마무리'], ['레슨을 끝내는 절차를 다룸']],
]
_h, _hbot = rows(_H_ROWS, _HCOLS, y0=6, rh=54, gap=12, arrows=False)
_P3C = svg(_hbot + 10, _h, '레슨 하나에 붙는 하네스가 넷이다 — 섹션, 화이트보드, 대기열, 마무리')

_P3C_CAP = ('하네스는 하나가 아니다. 녹화 로그에는 <b>섹션·화이트보드·대기열·마무리 네 갈래가 따로 돌고 있었다.</b> '
            '새 상황이 들어와도 레슨이 안 끊기게 하는 장치를 전부 상태 머신 안에 녹여 넣으려 했다고 밝힌다.')

_P3D = svg(268,
    box(0, 0, 640, 44, ['성공할지 실패할지가 동전 던지기 수준인가'], 'fig-box fig-stage', 'fig-st')
    + down(320, 48, 66)
    + box(0, 70, 640, 44, ['그렇다면 모델에서 제어 흐름을 빼낸다'], 'fig-box fig-agent', 'fig-st')
    + down(160, 118, 136) + down(480, 118, 136)
    + box(0, 140, 308, 60, ['결정은 모델 밖에', '미리 만들어 둔다'])
    + box(332, 140, 308, 60, ['모델에겐 쉽게 답할', '입력만 넘긴다'])
    + box(0, 214, 640, 44, ['음성 튜터 · 코딩 에이전트 · 옵스 런북 · 온보딩 플로우'], 'fig-box fig-human'),
    '성공과 실패가 동전 던지기 수준이면 제어 흐름을 모델에서 빼내고, 결정은 모델 밖에 미리 만들어 둔다')

_P3D_CAP = ('언제 이 방식을 쓰냐는 물음에 대한 기준이다. <b>성공할지 실패할지가 동전 던지기 수준이면 제어 흐름부터 걷어낸다.</b> '
            '음성 튜터만의 이야기가 아니라 코딩 에이전트·옵스 런북(장애 대응 같은 반복 운영 작업을 정리해둔 절차서)·'
            '온보딩 플로우에도 같은 원칙이 든다고 한다.')


# 이 장 도해에만 쓰는 붓. card_lib의 .uc-fig 안에서만 물린다.
FIG_CSS = """
  .uc-fig .fig-box{fill:var(--surface,#fff);stroke:var(--ink-3);stroke-width:1.2}
  .uc-fig .fig-human{fill:var(--epoch-keybg)}
  .uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--epoch-teal);stroke-width:1.6}
  .uc-fig .fig-stage{fill:var(--sunk,rgba(127,127,127,.10))}
  .uc-fig .fig-inside{fill:var(--epoch-keybg)}
  .uc-fig .fig-outside{fill:var(--surface,#fff);stroke-dasharray:4 3}
  .uc-fig .fig-bad{fill:var(--surface,#fff);stroke:var(--epoch-coral);stroke-width:1.6}
  .uc-fig .fig-tag{fill:none;stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
  .uc-fig .fig-tag-t{fill:var(--ink-3);font-size:14px;font-weight:800}
  .uc-fig .fig-st{fill:var(--ink);font-size:15px;font-weight:800}
  .uc-fig .fig-hd{fill:var(--ink-3);font-size:13px;font-weight:800;letter-spacing:.04em}
  /* 본문 번호글이 .95rem(약 15px)이다. 그림 글자도 같은 크기로 둔다 */
  .uc-fig .fig-b{fill:var(--ink);font-size:15px;font-weight:650}
  .uc-fig .fig-e{fill:var(--ink-3);font-size:12.5px;font-weight:700}
  .uc-fig .fig-lg{fill:var(--ink-3);font-size:13px;font-weight:650}
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:1.8;fill:none}
"""

# anchor는 그 그림이 푸는 번호 바로 앞이다.
FIGS = {
    '9HbzAWnKbo4': [
        (6,  '오류가 났을 때 누가 먼저 붙나', _P1A, _P1A_CAP),
        (21, '무엇을 모아야 고칠 수 있나', _P1B, _P1B_CAP),
        (33, '연결을 어디로 내보내나', _P1C, _P1C_CAP),
    ],
    'm24UKZomm7k': [
        (7,  '한 단계가 도는 방식', _P3A, _P3A_CAP),
        (11, '다 맡길 때와 좁게 줄 때', _P3B, _P3B_CAP),
        (20, '하네스는 하나가 아니다', _P3C, _P3C_CAP),
        (28, '언제 운전대를 뺏나', _P3D, _P3D_CAP),
    ],
    'k35LeKZEhiE': [
        (6,  '단계마다 훈련 스택이 무엇을 놓는가', _P2A, _P2A_CAP),
        (33, '환경에 난 틈을 모델이 배운다', _P2B, _P2B_CAP),
        (47, '통제를 놓은 자리를 무엇으로 메우나', _P2C, _P2C_CAP),
    ],
}
