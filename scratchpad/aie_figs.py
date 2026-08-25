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
  <text x="23" y="63" class="fig-tag-t">예전</text>

  <rect x="56" y="34" width="112" height="48" rx="10" class="fig-box"/>
  <text x="112" y="63" class="fig-b">오류가 남</text>

  <line x1="170" y1="58" x2="210" y2="58" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="190" y="47" class="fig-e">깨움</text>

  <rect x="214" y="34" width="210" height="48" rx="10" class="fig-box fig-human"/>
  <text x="319" y="63" class="fig-b">사람이 빈손으로 뒤짐</text>

  <line x1="426" y1="58" x2="466" y2="58" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="446" y="47" class="fig-e">고침</text>

  <rect x="470" y="34" width="170" height="48" rx="10" class="fig-box"/>
  <text x="555" y="63" class="fig-b">수정</text>

  <!-- 지금 -->
  <rect x="0" y="146" width="46" height="76" rx="9" class="fig-tag"/>
  <text x="23" y="189" class="fig-tag-t">지금</text>

  <rect x="56" y="146" width="112" height="76" rx="10" class="fig-box"/>
  <text x="112" y="189" class="fig-b">오류가 남</text>

  <line x1="170" y1="184" x2="210" y2="184" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="190" y="173" class="fig-e">붙음</text>

  <rect x="214" y="146" width="210" height="76" rx="10" class="fig-box fig-agent"/>
  <text x="319" y="174" class="fig-b">에이전트가 먼저 붙어</text>
  <text x="319" y="192" class="fig-b">기록·로그·저장소를</text>
  <text x="319" y="210" class="fig-b">한자리에 모음</text>

  <line x1="426" y1="184" x2="466" y2="184" class="fig-arw" marker-end="url(#aieSigArw)"/>
  <text x="446" y="173" class="fig-e">이슈</text>

  <rect x="470" y="146" width="170" height="76" rx="10" class="fig-box fig-human"/>
  <text x="555" y="178" class="fig-b">사람이 검토부터</text>
  <text x="555" y="200" class="fig-b">시작</text>

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
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:1.8;fill:none}
'''

FIGS = {
    '9HbzAWnKbo4': [(6, '오류가 났을 때 누가 먼저 붙나', _SIGNAL, _SIGNAL_CAP)],
}
