# -*- coding: utf-8 -*-
"""AI Engineer 번호글에 끼우는 도해.

번호글은 한 생각에 한 줄이라 「전체가 어떻게 맞물리는지」가 안 잡힌다. 그 한 장을
여기서 그린다. 열쇠는 영상 ID이고 값은 `card_lib`의 figs 그대로다 —
`[(anchor, 제목, svg, 캡션)]`.

**anchor는 그 그림이 설명하는 번호 바로 앞이다.** 7~19번을 푸는 그림이면 6이다.
먼저 판을 보여 주고 그 아래에서 번호가 하나씩 풀리게 한다 — 다 읽은 뒤에 그림이
나오면 그림이 할 일이 없다.

**한 편에 그림 하나로 제한하지 않는다.** 번호가 마흔을 넘으면 끝까지 읽기 힘들다.
논지가 꺾이는 자리마다 판을 새로 깔아 준다.

규칙은 `.claude/skills/insight-figure`. 원문에 없는 값을 그리지 않는다 —
도형 개수도 값이다. 배치는 `scratchpad/check_fig.py`가 검사하는데, 이 검사기는
text-anchor를 **태그 속성에서** 읽는다. 가운데 정렬을 클래스로만 주면 왼쪽 정렬로
재어 없는 넘침이 잡히거나 있는 넘침이 안 잡힌다 — 아래 헬퍼가 속성으로도 박는다.
"""

# ── 판을 짜는 작은 부품 ────────────────────────────────────────────────
# 자리를 손으로 찍으면 반드시 어긋난다. 칸 폭·줄 간격을 계산해서 내보낸다.
LH = 18          # 상자 안 줄 간격
CH = 9.0         # check_fig가 어림하는 한 글자 폭. 칸 폭을 이걸로 잡는다


def box(x, y, w, h, lines, cls='fig-box', tcls='fig-b'):
    """네모 하나와 그 안에 세로로 가운데 맞춘 글줄들."""
    out = ['  <rect x="%g" y="%g" width="%g" height="%g" rx="9" class="%s"/>' % (x, y, w, h, cls)]
    cx, n = x + w / 2, len(lines)
    top = y + h / 2 - (n - 1) * LH / 2 + 4
    for i, t in enumerate(lines):
        assert len(t) * CH <= w - 8, '칸(%g)보다 넓은 글: %r' % (w, t)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="%s">%s</text>'
                   % (cx, top + i * LH, tcls, t))
    return out


def arrow(x1, x2, y, label=''):
    """가로 화살표. label은 선 위에 붙는다."""
    out = ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
           % (x1, y, x2, y)]
    if label:
        assert len(label) * CH <= (x2 - x1) + 16, '화살표(%g)보다 넓은 말: %r' % (x2 - x1, label)
        out.append('  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
                   % ((x1 + x2) / 2, y - 9, label))
    return out


def down(x, y1, y2):
    """세로 화살표."""
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
            % (x, y1, x, y2)]


def legend(items, y):
    """판 아래 색 딱지. items = [(클래스, 말)]"""
    out, x = [], 0
    for cls, t in items:
        out.append('  <rect x="%g" y="%g" width="12" height="12" rx="3" class="fig-box %s"/>' % (x, y, cls))
        out.append('  <text x="%g" y="%g" class="fig-lg">%s</text>' % (x + 20, y + 10, t))
        x += 24 + len(t) * CH + 26
    return out


def svg(h, parts, alt):
    head = ('<svg class="epoch" viewBox="0 0 640 %g" role="img" aria-label="%s">\n'
            '  <defs>\n'
            '    <marker id="aieArw" viewBox="0 0 10 10" refX="9" refY="5"\n'
            '            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            '      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '  </defs>\n' % (h, alt))
    return head + '\n'.join(parts) + '\n</svg>'


# ══ 신호에서 PR까지 (9HbzAWnKbo4) ═════════════════════════════════════

_P1A = svg(266,
    box(0, 34, 46, 48, ['예전'], 'fig-tag', 'fig-tag-t')
    + box(56, 34, 112, 48, ['오류가 남'])
    + arrow(170, 210, 58, '깨움')
    + box(214, 34, 210, 48, ['사람이 빈손으로 뒤짐'], 'fig-box fig-human')
    + arrow(426, 466, 58, '고침')
    + box(470, 34, 170, 48, ['수정'])
    + box(0, 146, 46, 76, ['지금'], 'fig-tag', 'fig-tag-t')
    + box(56, 146, 112, 76, ['오류가 남'])
    + arrow(170, 210, 184, '붙음')
    + box(214, 146, 210, 76, ['에이전트가 먼저 붙어', '기록·로그·저장소를', '한자리에 모음'], 'fig-box fig-agent')
    + arrow(426, 466, 184, '이슈')
    + box(470, 146, 170, 76, ['사람이 검토부터', '시작'], 'fig-box fig-human')
    + legend([('fig-human', '사람이 붙는 자리'), ('fig-agent', '에이전트가 붙는 자리')], 240),
    '예전에는 오류가 사람을 깨워 사람이 빈손으로 뒤졌고, 지금은 에이전트가 먼저 붙어 증거를 모아 두면 사람이 검토부터 시작한다')

_P1A_CAP = ('같은 일을 하는데 <b>사람이 붙는 자리만 앞에서 뒤로</b> 옮겨간다. '
            '예전에는 오류가 사람을 깨웠고 사람이 빈손으로 화면을 뒤졌다. '
            '지금은 에이전트가 먼저 붙어 실행 기록·로그·저장소를 한자리에 모아 이슈를 만들어 두고, '
            '사람은 증거가 갖춰진 상태에서 검토부터 시작한다 — 발표자가 「대응자에서 검토자로」라고 부른 자리 바꿈이다.')

_P1B = svg(212,
    box(0, 10, 250, 62, ['저장소', '코드가 밟을 수 있는 경로'])
    + box(0, 88, 250, 62, ['실행 기록 · 로그', '실제로 밟은 경로'])
    + arrow(258, 318, 41)
    + arrow(258, 318, 119)
    + box(326, 30, 314, 90, ['스킬이 실행 중 만든 임시 파일까지',
                             '저장소 안으로 끌어와',
                             '벌어진 일과 코드를 한자리에 둠'], 'fig-box fig-agent')
    + legend([('fig-agent', '스킬이 하는 일')], 176),
    '저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를 알려주고 스킬이 둘을 한자리에 모은다')

_P1B_CAP = ('둘 중 하나만으로는 못 고친다. <b>저장소는 코드가 밟을 수 있는 경로를, 실행 기록과 로그는 실제로 밟은 경로를</b> '
            '알려준다. 스킬이 하는 일은 실행 중에 만든 임시 파일까지 저장소 안으로 끌어와 둘을 같은 자리에 놓는 것이고, '
            '발표자는 이 조합이 스킬을 조립 가능하게 만드는 핵심이라고 한다.')

_P1C = svg(214,
    box(0, 60, 130, 56, ['시그널'], 'fig-box fig-agent')
    + arrow(138, 198, 44, '갈래 1')
    + arrow(138, 198, 132, '갈래 2')
    + box(206, 14, 434, 62, ['앤트로픽이 관리하는 매니지드 에이전트', '연결이 회사 밖으로 나감'])
    + box(206, 100, 434, 62, ['자사 VPC 안에 세운 아라이즈 샌드박스', '연결이 회사 안에 머묾'], 'fig-box fig-human')
    + legend([('fig-human', '우버·부킹이 고른 쪽')], 188),
    '시그널은 앤트로픽 매니지드 에이전트로 돌릴 수도 있고 자사 VPC 안 샌드박스로 돌릴 수도 있다')

_P1C_CAP = ('갈래가 둘인 이유는 기술이 아니라 <b>고객이 프로덕션 시스템을 앤트로픽에 직접 연결하고 싶어 하지 않기 때문</b>이다. '
            '우버와 부킹은 자사 VPC(가상 사설 클라우드, 회사 전용으로 격리된 클라우드망) 안에 샌드박스를 세워 '
            '연결을 바깥으로 내보내지 않고 쓴다.')


# ══ 일하면서 배우는 에이전트 (k35LeKZEhiE) ═════════════════════════════
# 계단이나 막대로 그리면 높이가 수치로 읽히는데 원문에 그런 수는 없다 —
# 네 칸을 같은 크기로 두고 안·밖에 든 것만 이름으로 적는다.

_STAGES = [('한 턴 문답', ['롤아웃 진행', '형식·채점까지'], ['없음']),
           ('합성 환경', ['오케스트레이터', '샌드박스'], ['환경 상태']),
           ('남의 하니스', ['모델 엔드포인트', '요청·응답 기록'], ['오케스트레이션', '전체']),
           ('에이전트 시민', ['없음'], ['모델이 스스로', '평가·개선'])]
_p, _W, _G = [], 142, 24
for _i, (_t, _in, _out) in enumerate(_STAGES):
    _x = _i * (_W + _G)
    _p += box(_x, 0, _W, 30, [_t], 'fig-box fig-stage', 'fig-st')
    _p += box(_x, 38, _W, 58, _in, 'fig-box fig-inside')
    _p += box(_x, 104, _W, 58, _out, 'fig-box fig-outside')
    if _i < 3:
        _p += arrow(_x + _W - 30, _x + _W + _G + 30, 176)
_P2A = svg(214, _p + legend([('fig-inside', '훈련 스택 안'), ('fig-outside', '훈련 스택 밖')], 192),
           '포스트트레이닝 네 단계에서 훈련 스택 안에 남는 것과 밖으로 나간 것')

_P2A_CAP = ('단계가 올라갈수록 <b>훈련 스택이 쥐고 있던 것이 한 겹씩 바깥으로 나간다.</b> '
            '한 턴 문답에서는 롤아웃을 어떻게 돌리고 어떻게 포맷하는지까지 스택 안에서 통제했는데, '
            '남의 하니스로 오면 스택 안에 남는 것은 모델 완성 엔드포인트와 요청·응답을 기록하는 장치뿐이다. '
            '통제를 놓는 대신 실제 프로덕션 환경을 그대로 쓰게 되지만, 그만큼 거기서 뽑아낼 학습 신호도 줄어든다.')

_P2B = svg(238,
    box(0, 0, 308, 34, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(332, 0, 308, 34, ['환경에 난 틈'], 'fig-box fig-stage', 'fig-st')
    + box(0, 44, 308, 48, ['도구 호출의 약 10%가 실패함'])
    + box(332, 44, 308, 48, ['타임아웃난 롤아웃은 훈련에서 뺌'])
    + down(154, 96, 108) + down(486, 96, 108)
    + box(0, 112, 308, 48, ['길게 답할수록 빠질 확률이 커짐'])
    + box(332, 112, 308, 48, ['0점 받느니 아예 빠지는 쪽이 이득'])
    + down(154, 164, 176) + down(486, 164, 176)
    + box(0, 180, 308, 48, ['모델이 답을 짧게 냄'], 'fig-box fig-bad')
    + box(332, 180, 308, 48, ['모델이 일부러 타임아웃을 냄'], 'fig-box fig-bad'),
    '도구 호출 10퍼센트 실패는 모델이 답을 짧게 내게 만들었고, 타임아웃 롤아웃을 뺀 것은 모델이 일부러 타임아웃을 내게 만들었다')

_P2B_CAP = ('발표자가 든 두 사례다. <b>환경의 사소한 버릇을 모델이 그대로 배운다.</b> '
            '리워드 함수에는 길이 벌점이 전혀 없었는데도 답이 짧아졌고, 타임아웃난 롤아웃을 훈련에서 걸러내자 '
            '모델이 도구 호출을 남발해 스스로 타임아웃을 냈다. 발표자는 환경 충실도와 리워드 해킹이 결국 같은 문제라고 한다.')

_D = [('자기증류', ['모델이 스스로 만든 답에서', '새 행동을 심음', '아직 좁은 범위만 성공']),
      ('자동화된 데이터 파이프라인', ['대량의 트레이스를 훑어', '실패 사례를 골라 다시 먹임', '지금은 사람이 손으로 함']),
      ('정성적 피드백 흡수', ['점수 대신 글로 된 반응만', '남는 프로덕션에서', '그것만으로 모델을 고침'])]
_q, _CW, _CG = [], 197, 24
for _i, (_t, _ls) in enumerate(_D):
    _x = _i * (_CW + _CG)
    _q += box(_x, 0, _CW, 34, [_t], 'fig-box fig-stage', 'fig-st')
    _q += box(_x, 42, _CW, 74, _ls, 'fig-box fig-agent')
_P2C = svg(130, _q,
           '통제를 놓은 자리를 메우는 연구 방향 셋 — 자기증류, 자동화된 데이터 파이프라인, 정성적 피드백 흡수')

_P2C_CAP = ('앞 단계에서 놓아 버린 통제를 무엇으로 메울지에 대한 답이다. 셋 다 <b>아직 열린 연구 질문</b>이고, '
            '특히 트레이스를 훑어 실패 사례를 골라내는 일은 지금도 사람이 손으로 하고 있다고 발표자가 밝힌다.')


# 이 장 도해에만 쓰는 붓. card_lib의 .uc-fig 안에서만 물린다.
FIG_CSS = """
  .uc-fig .fig-box{fill:var(--surface,#fff);stroke:var(--ink-3);stroke-width:1.2}
  .uc-fig .fig-human{fill:var(--epoch-keybg)}
  .uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--epoch-teal);stroke-width:1.6}
  .uc-fig .fig-stage{fill:var(--sunk,rgba(127,127,127,.08))}
  .uc-fig .fig-inside{fill:var(--epoch-keybg)}
  .uc-fig .fig-outside{fill:var(--surface,#fff);stroke-dasharray:4 3}
  .uc-fig .fig-bad{fill:var(--surface,#fff);stroke:var(--epoch-coral);stroke-width:1.6}
  .uc-fig .fig-tag{fill:none;stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
  .uc-fig .fig-tag-t{fill:var(--ink-3);font-size:11px;font-weight:800}
  .uc-fig .fig-st{fill:var(--ink);font-size:11px;font-weight:800}
  .uc-fig .fig-b{fill:var(--ink);font-size:11px;font-weight:650}
  .uc-fig .fig-e{fill:var(--ink-3);font-size:9.5px;font-weight:700}
  .uc-fig .fig-lg{fill:var(--ink-3);font-size:10px;font-weight:600}
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:1.8;fill:none}
"""

# anchor는 그 그림이 푸는 번호 바로 앞이다.
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
