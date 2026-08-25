# -*- coding: utf-8 -*-
"""AI Engineer 번호글에 끼우는 도해.

번호글은 한 생각에 한 줄이라 「전체가 어떻게 맞물리는지」가 안 잡힌다. 그 한 장을
여기서 그린다. 열쇠는 영상 ID이고 값은 `card_lib`의 figs 그대로다 —
`[(anchor, 제목, svg, 캡션)]`, anchor는 몇 번째 번호 뒤에 세울지(0이면 맨 앞).

규칙은 `.claude/skills/insight-figure`. 원문에 없는 값을 그리지 않는다 —
도형 개수도 값이다. 배치는 `scratchpad/check_fig.py`가 검사한다.
"""

# ── 신호에서 PR까지 (9HbzAWnKbo4) ─────────────────────────────────────────
# 이 발표의 뼈대는 「사람의 자리가 맨 앞에서 맨 뒤로 옮겨간다」 하나다.
# 그래서 같은 줄을 둘 그리고 사람 상자만 자리를 바꾼다. 단계 수는 발표에 나온
# 그대로이고 없는 단계를 만들어 넣지 않았다.
_SIGNAL = '''<svg class="epoch" viewBox="0 0 640 266" role="img"
     aria-label="예전에는 오류가 나면 사람이 먼저 화면을 뒤졌고, 지금은 에이전트가 먼저 증거를 모아 이슈를 만들고 사람은 뒤에서 검토한다">
  <defs>
    <marker id="aieSigArw" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>
    </marker>
  </defs>

  <!-- 예전 -->
  <rect x="0" y="34" width="46" height="48" rx="9" class="fig-tag"/>
  <text x="23" y="63" text-anchor="middle" class="fig-tag-t">예전</text>

  <rect x="56" y="34" width="112" height="48" rx="10" class="fig-box"/>
  <text x="112" y="63" text-anchor="middle" class="fig-b">오류가 남</text>

  <line x1="170" y1="58" x2="210" y2="58" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="190" y="47" text-anchor="middle" class="fig-e">깨움</text>

  <rect x="214" y="34" width="210" height="48" rx="10" class="fig-box fig-human"/>
  <text x="319" y="63" text-anchor="middle" class="fig-b">사람이 빈손으로 뒤짐</text>

  <line x1="426" y1="58" x2="466" y2="58" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="446" y="47" text-anchor="middle" class="fig-e">고침</text>

  <rect x="470" y="34" width="170" height="48" rx="10" class="fig-box"/>
  <text x="555" y="63" text-anchor="middle" class="fig-b">수정</text>

  <!-- 지금 -->
  <rect x="0" y="146" width="46" height="76" rx="9" class="fig-tag"/>
  <text x="23" y="189" text-anchor="middle" class="fig-tag-t">지금</text>

  <rect x="56" y="146" width="112" height="76" rx="10" class="fig-box"/>
  <text x="112" y="189" text-anchor="middle" class="fig-b">오류가 남</text>

  <line x1="170" y1="184" x2="210" y2="184" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="190" y="173" text-anchor="middle" class="fig-e">붙음</text>

  <rect x="214" y="146" width="210" height="76" rx="10" class="fig-box fig-agent"/>
  <text x="319" y="174" text-anchor="middle" class="fig-b">에이전트가 먼저 붙어</text>
  <text x="319" y="192" text-anchor="middle" class="fig-b">기록·로그·저장소를</text>
  <text x="319" y="210" text-anchor="middle" class="fig-b">한자리에 모음</text>

  <line x1="426" y1="184" x2="466" y2="184" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="446" y="173" text-anchor="middle" class="fig-e">이슈</text>

  <rect x="470" y="146" width="170" height="76" rx="10" class="fig-box fig-human"/>
  <text x="555" y="178" text-anchor="middle" class="fig-b">사람이 검토부터</text>
  <text x="555" y="200" text-anchor="middle" class="fig-b">시작</text>

  <!-- 범례는 판 아래 -->
  <rect x="56" y="240" width="12" height="12" rx="3" class="fig-box fig-human"/>
  <text x="76" y="250" class="fig-lg">사람이 붙는 자리</text>
  <rect x="228" y="240" width="12" height="12" rx="3" class="fig-box fig-agent"/>
  <text x="248" y="250" class="fig-lg">에이전트가 붙는 자리</text>
</svg>'''

_SIGNAL_CAP = ('같은 일을 하는데 <b>사람이 붙는 자리만 앞에서 뒤로</b> 옮겨간다. '
               '예전에는 오류가 사람을 깨웠고 사람이 빈손으로 화면을 뒤졌다. '
               '지금은 에이전트가 먼저 붙어 실행 기록·로그·저장소를 한자리에 모아 이슈를 만들어 두고, '
               '사람은 증거가 갖춰진 상태에서 검토부터 시작한다 — 발표자가 「대응자에서 검토자로」라고 부른 것이 이 자리 바꿈이다.')

# 이 장 도해에만 쓰는 붓. card_lib의 .uc-fig 안에서만 물린다.
FIG_CSS = '''
  .uc-fig .fig-box{fill:var(--surface,#fff);stroke:var(--ink-3);stroke-width:1.2}
  .uc-fig .fig-human{fill:var(--epoch-keybg)}
  .uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--epoch-teal);stroke-width:1.6}
  .uc-fig .fig-tag{fill:none;stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
  .uc-fig .fig-tag-t{fill:var(--ink-3);font-size:11px;font-weight:800;text-anchor:middle}
  .uc-fig .fig-b{fill:var(--ink);font-size:11px;font-weight:650;text-anchor:middle}
  .uc-fig .fig-e{fill:var(--ink-3);font-size:9.5px;font-weight:700;text-anchor:middle}
  .uc-fig .fig-lg{fill:var(--ink-3);font-size:10px;font-weight:600}
  .uc-fig .fig-stage{fill:var(--sunk,rgba(127,127,127,.08))}
  .uc-fig .fig-inside{fill:var(--epoch-keybg)}
  .uc-fig .fig-outside{fill:var(--surface,#fff);stroke-dasharray:4 3}
  .uc-fig .fig-st{fill:var(--ink);font-size:11px;font-weight:800;text-anchor:middle}
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:1.8;fill:none}
'''

# ── 일하면서 배우는 에이전트 (k35LeKZEhiE) ────────────────────────────
# 이 발표의 축은 「훈련 스택이 쥔 것이 단계마다 한 겹씩 줄어든다」 하나다.
# 계단이나 막대로 그리면 높이가 수치로 읽히는데 원문에 그런 수는 없다 —
# 그래서 네 칸을 같은 크기로 두고 안·밖에 든 것만 이름으로 적는다.
_POSTTRAIN = '<svg class="epoch" viewBox="0 0 640 214" role="img"\n     aria-label="포스트트레이닝 네 단계에서 훈련 스택이 쥔 것과 바깥으로 나간 것">\n  <defs>\n    <marker id="aiePtArw" viewBox="0 0 10 10" refX="9" refY="5"\n            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>\n    </marker>\n  </defs>\n  <rect x="0" y="0" width="142" height="30" rx="8" class="fig-box fig-stage"/>\n  <text x="71" y="20" text-anchor="middle" class="fig-st">한 턴 문답</text>\n  <rect x="0" y="38" width="142" height="58" rx="8" class="fig-box fig-inside"/>\n  <text x="71" y="53" text-anchor="middle" class="fig-b">롤아웃 진행</text>\n  <text x="71" y="71" text-anchor="middle" class="fig-b">형식·채점까지</text>\n  <rect x="0" y="104" width="142" height="58" rx="8" class="fig-box fig-outside"/>\n  <text x="71" y="128" text-anchor="middle" class="fig-b">없음</text>\n  <line x1="112" y1="176" x2="196" y2="176" class="fig-arw" marker-end="url(#aiePtArw)"/>\n  <rect x="166" y="0" width="142" height="30" rx="8" class="fig-box fig-stage"/>\n  <text x="237" y="20" text-anchor="middle" class="fig-st">합성 환경</text>\n  <rect x="166" y="38" width="142" height="58" rx="8" class="fig-box fig-inside"/>\n  <text x="237" y="53" text-anchor="middle" class="fig-b">오케스트레이터</text>\n  <text x="237" y="71" text-anchor="middle" class="fig-b">샌드박스</text>\n  <rect x="166" y="104" width="142" height="58" rx="8" class="fig-box fig-outside"/>\n  <text x="237" y="128" text-anchor="middle" class="fig-b">환경 상태</text>\n  <line x1="278" y1="176" x2="362" y2="176" class="fig-arw" marker-end="url(#aiePtArw)"/>\n  <rect x="332" y="0" width="142" height="30" rx="8" class="fig-box fig-stage"/>\n  <text x="403" y="20" text-anchor="middle" class="fig-st">남의 하니스</text>\n  <rect x="332" y="38" width="142" height="58" rx="8" class="fig-box fig-inside"/>\n  <text x="403" y="53" text-anchor="middle" class="fig-b">모델 엔드포인트</text>\n  <text x="403" y="71" text-anchor="middle" class="fig-b">요청·응답 기록</text>\n  <rect x="332" y="104" width="142" height="58" rx="8" class="fig-box fig-outside"/>\n  <text x="403" y="119" text-anchor="middle" class="fig-b">오케스트레이션</text>\n  <text x="403" y="137" text-anchor="middle" class="fig-b">전체</text>\n  <line x1="444" y1="176" x2="528" y2="176" class="fig-arw" marker-end="url(#aiePtArw)"/>\n  <rect x="498" y="0" width="142" height="30" rx="8" class="fig-box fig-stage"/>\n  <text x="569" y="20" text-anchor="middle" class="fig-st">에이전트 시민</text>\n  <rect x="498" y="38" width="142" height="58" rx="8" class="fig-box fig-inside"/>\n  <text x="569" y="62" text-anchor="middle" class="fig-b">없음</text>\n  <rect x="498" y="104" width="142" height="58" rx="8" class="fig-box fig-outside"/>\n  <text x="569" y="119" text-anchor="middle" class="fig-b">모델이 스스로</text>\n  <text x="569" y="137" text-anchor="middle" class="fig-b">평가·개선</text>\n  <rect x="0" y="192" width="12" height="12" rx="3" class="fig-box fig-inside"/>\n  <text x="20" y="202" class="fig-lg">훈련 스택 안</text>\n  <rect x="140" y="192" width="12" height="12" rx="3" class="fig-box fig-outside"/>\n  <text x="160" y="202" class="fig-lg">훈련 스택 밖</text>\n</svg>'

_POSTTRAIN_CAP = '단계가 올라갈수록 <b>훈련 스택이 쥐고 있던 것이 한 겹씩 바깥으로 나간다.</b> 한 턴 문답에서는 롤아웃을 어떻게 돌리고 어떻게 포맷하는지까지 스택 안에서 통제했는데, 남의 하니스로 오면 스택 안에 남는 것은 모델 완성 엔드포인트와 요청·응답을 기록하는 장치뿐이다. 통제를 놓는 대신 실제 프로덕션 환경을 그대로 쓰게 되지만, 그만큼 거기서 뽑아낼 학습 신호도 줄어든다.'

FIGS = {
    '9HbzAWnKbo4': [(6, '오류가 났을 때 누가 먼저 붙나', _SIGNAL, _SIGNAL_CAP)],
    'k35LeKZEhiE': [(12, '단계마다 훈련 스택이 무엇을 놓는가', _POSTTRAIN, _POSTTRAIN_CAP)],
}
