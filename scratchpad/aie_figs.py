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
자리는 칸 사이 틈으로 간다. 글자는 19px — 본문 번호글(.95rem ≈ 15px)보다 크다.

판은 776으로 내보낸다. 데스크톱에서 카드 안 그림 자리가 776px이라
(.wrap 840 − .ucard 26×2 − .uc-fig 6×2) 배율이 1이 되어 19px이 19px로 그려진다.

배치는 `scratchpad/check_fig.py`가 보고, 브라우저에서 getBBox로 다시 잰다.
그 검사기는 한 글자를 9px로 어림하므로 19px 글자는 못 잡는다 — 아래 헬퍼가
19.5px로 따로 재고 넘치면 생성이 멈춘다.
"""

W = 776.0        # 내보내는 판 폭
CHW = 19.5       # 19px 한글 한 글자 폭. 브라우저에서 재어 얻었다
PAD = 2          # 칸 좌우 여백. 글자에 자리를 다 준다
LH = 28          # 줄 간격
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
        x += 22 + len(t) * 15 + 30
    assert x <= W, '범례가 판보다 넓다'
    return out


def svg(h, parts, alt):
    return ('<svg class="epoch" viewBox="0 0 776 %g" role="img" aria-label="%s">\n'
            '  <defs>\n'
            '    <marker id="aieArw" viewBox="0 0 10 10" refX="9" refY="5"\n'
            '            markerWidth="7" markerHeight="7" orient="auto-start-reverse">\n'
            '      <path d="M0 0 L10 5 L0 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '    <marker id="aieArwL" viewBox="0 0 10 10" refX="1" refY="5"\n'
            '            markerWidth="7" markerHeight="7">\n'
            '      <path d="M10 0 L0 5 L10 10 z" fill="var(--epoch-teal)"/>\n'
            '    </marker>\n'
            '  </defs>\n' % (h, alt)) + '\n'.join(parts) + '\n</svg>'


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


def band(items, y, h, gaps):
    """가로 한 줄. items = [(줄들, 클래스)] 또는 ('>', 말) 화살표."""
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
               (['수정'], 'fig-box')], 44, 62, [96, 96])
_a2, _ = band([(['오류가 남'], 'fig-box'), ('>', '붙음'),
               (['에이전트가 먼저 붙어', '기록·로그·저장소를', '한자리에 모음'], 'fig-box fig-agent'),
               ('>', '이슈'), (['사람이', '검토부터 시작'], 'fig-box fig-human')], 150, 104, [96, 96])
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
_RX = _LW + 90
_P1B = svg(232,
    box(0, 10, _LW, 76, ['저장소'] + _L1)
    + box(0, 104, _LW, 76, ['실행 기록 · 로그'] + _L2)
    + arrow(_LW + 8, _RX - 8, 48) + arrow(_LW + 8, _RX - 8, 142)
    + box(_RX, 32, w_of(['스킬이 실행 중 만든 임시 파일까지',
                         '저장소 안으로 끌어와',
                         '벌어진 일과 코드를 한자리에 둠']), 126, ['스킬이 실행 중 만든 임시 파일까지',
                                  '저장소 안으로 끌어와',
                                  '벌어진 일과 코드를 한자리에 둠'], 'fig-box fig-agent')
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


# ══ 운전대를 주지 마라 (m24UKZomm7k) ═══════════════════════════════════

_HW = w_of(['하네스'], ['모델'])
_P3A = svg(300,
    box(0, 0, _HW, 56, ['하네스'], 'fig-box fig-agent', 'fig-st')
    + box(W - _HW, 0, _HW, 56, ['모델'], 'fig-box fig-human', 'fig-st')
    + arrow(_HW + 10, W - _HW - 10, 100, '이 한 가지만 하고 결과를 줘')
    + arrow(_HW + 10, W - _HW - 10, 150, '결과', True)
    + box(0, 186, w_of(['결과를 검증하고', '다음 단계로 넘김']), 84,
          ['결과를 검증하고', '다음 단계로 넘김'], 'fig-box fig-agent')
    + box(w_of(['결과를 검증하고', '다음 단계로 넘김']) + GAP, 186,
          w_of(['인트로 → 티치 → 체크', '그레이드 → 어드밴스 → 랩']), 84,
          ['인트로 → 티치 → 체크', '그레이드 → 어드밴스 → 랩'])
    + legend([('fig-agent', '하네스가 정하는 것'), ('fig-human', '모델이 하는 것')], 282),
    '하네스가 모델에게 한 가지만 시키고 결과를 받아 검증한 뒤 다음 단계로 넘긴다')

_P3A_CAP = ('한 단계가 도는 방식이다. <b>하네스가 모델에게 한 번에 한 가지만 넘기고, 돌아온 결과를 검증한 뒤 '
            '다음 단계를 정한다.</b> 모델은 지금이 여섯 중 몇 번째인지 알 필요가 없다 — 그 기억을 아예 요구하지 않는다. '
            '레슨 하나는 인트로·티치·체크·그레이드·어드밴스·랩으로 이어지는 작은 상태 머신이다.')

_B1 = ['오퍼스 4.7이 생각부터 처리까지', '라이브 튜터에선 늘 통하지 않음']
_B2 = ['하이쿠 4.5는 대사만', '하네스가 흐름을 쥠', '비용·시간·지연을 아낌']
_BW = (W - GAP) / 2
_P3B = svg(210,
    box(0, 0, _BW, 52, ['모델 하나에 다 맡김'], 'fig-box fig-stage', 'fig-st')
    + box(_BW + GAP, 0, _BW, 52, ['단계마다 좁은 계약'], 'fig-box fig-stage', 'fig-st')
    + box(0, 66, _BW, 130, _B1)
    + box(_BW + GAP, 66, _BW, 130, _B2, 'fig-box fig-agent'),
    '무거운 모델 하나에 다 맡기는 방식과 단계마다 좁은 계약을 주는 방식의 대비')

_P3B_CAP = ('작은 모델을 쓴 것이 먼저가 아니다. <b>흐름을 하네스가 쥐고 나서야 작은 모델로 내려갈 수 있었다.</b> '
            '오퍼스 4.7이 생각부터 처리까지 다 하는 방식은 라이브 튜터처럼 신뢰성·비용·속도가 한꺼번에 필요한 자리에서는 '
            '늘 통하지 않는다고 발표자는 말한다.')

_h3, _h3b = table([[['섹션'], ['지금 무엇을 말하고 무엇을 할지 입력을 줌']],
                   [['화이트보드'], ['화이트보드에 그리는 것을 다룸']],
                   [['대기열'], ['대기열을 비우는 것을 다룸']],
                   [['마무리'], ['레슨을 끝내는 절차를 다룸']]],
                  ['fig-box fig-stage', 'fig-box'], y0=8, arrows=False)
_P3C = svg(_h3b + 10, _h3, '레슨 하나에 붙는 하네스가 넷이다 — 섹션, 화이트보드, 대기열, 마무리')

_P3C_CAP = ('하네스는 하나가 아니다. 녹화 로그에는 <b>섹션·화이트보드·대기열·마무리 네 갈래가 따로 돌고 있었다.</b> '
            '새 상황이 들어와도 레슨이 안 끊기게 하는 장치를 전부 상태 머신 안에 녹여 넣으려 했다고 밝힌다.')

_P3D = svg(300,
    mid(0, 56, ['성공할지 실패할지가 동전 던지기 수준인가'], 'fig-box fig-stage', 'fig-st')
    + down(W / 2, 60, 82)
    + mid(86, 56, ['그렇다면 모델에서 제어 흐름을 빼낸다'], 'fig-box fig-agent', 'fig-st')
    + down(W / 4, 146, 168) + down(W * 3 / 4, 146, 168)
    + box(0, 172, _BW, 76, ['결정은 모델 밖에', '미리 만들어 둔다'])
    + box(_BW + GAP, 172, _BW, 76, ['모델에겐 쉽게 답할', '입력만 넘긴다'])
    + mid(262, 44, ['음성 튜터 · 코딩 에이전트 · 옵스 런북 · 온보딩 플로우'], 'fig-box fig-human'),
    '성공과 실패가 동전 던지기 수준이면 제어 흐름을 모델에서 빼내고, 결정은 모델 밖에 미리 만들어 둔다')

_P3D_CAP = ('언제 이 방식을 쓰냐는 물음에 대한 기준이다. <b>성공할지 실패할지가 동전 던지기 수준이면 제어 흐름부터 걷어낸다.</b> '
            '음성 튜터만의 이야기가 아니라 코딩 에이전트·옵스 런북(장애 대응 같은 반복 운영 작업을 정리해둔 절차서)·'
            '온보딩 플로우에도 같은 원칙이 든다고 한다.')


# ══ 일하면서 배우는 에이전트 (k35LeKZEhiE) ═════════════════════════════

_p2, _p2b = table([[['한 턴 문답'], ['롤아웃 진행·형식·채점'], ['없음']],
                   [['합성 환경'], ['오케스트레이터·샌드박스'], ['환경 상태']],
                   [['남의 하니스'], ['모델 엔드포인트', '요청·응답 기록'], ['오케스트레이션 전체']],
                   [['에이전트 시민'], ['없음'], ['모델이 스스로 평가·개선']]],
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
  .uc-fig .fig-b{fill:var(--ink);font-size:19px;font-weight:600}
  .uc-fig .fig-st{fill:var(--ink);font-size:19px;font-weight:800}
  .uc-fig .fig-hd{fill:var(--ink-3);font-size:15px;font-weight:800;letter-spacing:.04em}
  .uc-fig .fig-e{fill:var(--ink-3);font-size:15px;font-weight:700}
  .uc-fig .fig-lg{fill:var(--ink-3);font-size:15px;font-weight:650}
  .uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:2;fill:none}
"""

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


# ══ 보고서 형식으로 다시 쓴 편의 그림 ═══════════════════════════════════
#
# 번호글은 번호 뒤에 그림을 끼웠지만, 보고서는 절 안에서 `[[fig:열쇠]]`로 부른다.
# 그래서 앵커가 숫자가 아니라 이름이고, 값도 목록이 아니라 사전이다.


def lifeline(x, y1, y2):
    """시퀀스 그림의 생명선. 점선 세로줄 하나."""
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-life"/>' % (x, y1, x, y2)]


# ── 한눈에 ──────────────────────────────────────────────────────────
_s_rows = [[['만든 것'], ['학생과 말을 주고받으며', '레슨 하나를 끝까지 끌고 가는 음성 튜터']],
           [['막힌 것'], ['다단계 에이전트가 실사용에서', '스스로 끝내거나 건너뛰거나 맴돔']],
           [['바꾼 것'], ['여섯 단계 상태 머신을 만들고', '단계를 넘기는 판단을 하네스가 쥠']],
           [['얻은 것'], ['오퍼스 4.7 대신 하이쿠 4.5로도', '기대한 수준으로 작동']]]
_s_body, _s_h = table(_s_rows, ['fig-box fig-stage', 'fig-box fig-agent'], y0=8, arrows=False)
_R_SUM = svg(_s_h + 10, _s_body,
             '만든 것과 막힌 것과 바꾼 것과 얻은 것을 네 줄로 정리한 표')

_R_SUM_CAP = ('6분 발표의 뼈대다. <b>작은 모델을 고른 것이 앞이 아니라 뒤에 온다.</b> '
              '단계를 넘기는 판단을 모델에게서 걷어낸 다음에야 하이쿠 4.5로 내려갈 수 있었다.')

# ── 실사용에서 깨지는 세 가지 ────────────────────────────────────────
_f_w = (W - 2 * GAP) / 3
_R_FAIL = svg(196,
    mid(0, 48, ['데모까지는 잘 돌다가 진짜 사용자가 붙으면'], 'fig-box fig-stage', 'fig-st')
    + down(W / 2, 52, 74)
    + box(0, 78, _f_w, 88, ['절반쯤 가서', '끝났다고 판단'], 'fig-box fig-bad')
    + box(_f_w + GAP, 78, _f_w, 88, ['단계 하나를', '건너뜀'], 'fig-box fig-bad')
    + box(2 * (_f_w + GAP), 78, _f_w, 88, ['같은 자리를', '맴돔'], 'fig-box fig-bad'),
    '실사용에서 다단계 에이전트가 깨지는 세 가지 모양')

_R_FAIL_CAP = ('오넬라가 든 세 장면이다. 셋 다 <b>모델이 흐름을 잘못 판단해서 생긴다.</b> '
               '발표는 데모 영상이 이 장면을 절대 보여주지 않는다고 짚는다.')

# ── 여섯 단계 상태 머신 ─────────────────────────────────────────────
_sm_names = ['인트로', '티치', '체크', '그레이드', '어드밴스', '랩']
_sm_ws = [w_of([n]) for n in _sm_names]
_sm_gap = (W - sum(_sm_ws)) / 5.0
_sm = []
_x = 0.0
for _i, _n in enumerate(_sm_names):
    _sm += box(_x, 46, _sm_ws[_i], 58, [_n], 'fig-box fig-human', 'fig-st')
    if _i < 5:
        _sm += arrow(_x + _sm_ws[_i] + 6, _x + _sm_ws[_i] + _sm_gap - 6, 75)
    _x += _sm_ws[_i] + _sm_gap
_R_SM = svg(200,
    mid(0, 32, ['레슨 하나'], 'fig-box fig-stage', 'fig-st') + _sm
    + down(W / 2, 108, 128)
    + mid(132, 56, ['단계를 넘기는 판단은 전부 하네스가 한다'], 'fig-box fig-agent', 'fig-st'),
    '레슨 하나는 인트로 티치 체크 그레이드 어드밴스 랩 여섯 단계를 오가는 상태 머신이다')

_R_SM_CAP = ('단계 이름이 곧 그 단계에서 할 수 있는 일의 목록이다. <b>쪼갠 것보다 중요한 것은 '
             '단계를 오가는 판단을 모델 바깥에 뒀다는 것이다.</b> 모델은 자기가 여섯 중 몇 번째인지 모른 채 돈다.')

# ── 한 단계가 도는 순서 (시퀀스) ─────────────────────────────────────
_L1X, _L2X, _L3X = 100.0, 388.0, 676.0
_lw = w_of(['학생'], ['하네스'], ['모델'])
_R_SEQ = svg(430,
    box(_L1X - _lw / 2, 0, _lw, 46, ['학생'], 'fig-box fig-human', 'fig-st')
    + box(_L2X - _lw / 2, 0, _lw, 46, ['하네스'], 'fig-box fig-agent', 'fig-st')
    + box(_L3X - _lw / 2, 0, _lw, 46, ['모델'], 'fig-box fig-stage', 'fig-st')
    + lifeline(_L1X, 50, 396) + lifeline(_L3X, 50, 396)
    # 하네스 생명선은 자기 호출 상자 자리에서 끊는다. 상자 뒤로 지나가게 두면
    # 점선이 글자를 가로지르는 것으로 잡힌다
    + lifeline(_L2X, 50, 248) + lifeline(_L2X, 304, 396)
    + arrow(_L1X + 8, _L2X - 8, 96, '학생이 답을 말함')
    + arrow(_L2X + 8, _L3X - 8, 156, '이 단계에 필요한 입력만')
    + arrow(_L2X + 8, _L3X - 8, 214, '행동 하나의 결과', True)
    + box(_L2X - w_of(['검증하고 상태를 다음으로 넘김']) / 2, 250,
          w_of(['검증하고 상태를 다음으로 넘김']), 52,
          ['검증하고 상태를 다음으로 넘김'], 'fig-box fig-agent')
    + arrow(_L1X + 8, _L2X - 8, 356, '다음 말과 화이트보드', True)
    + legend([('fig-agent', '하네스가 정하는 것'), ('fig-stage', '모델이 하는 것')], 402),
    '학생과 하네스와 모델 사이에 오가는 한 단계의 순서. 하네스가 입력을 만들어 모델에 넘기고 결과를 검증한 뒤 상태를 넘긴다')

_R_SEQ_CAP = ('한 단계가 도는 순서다. 모델에게 가는 것은 <b>그 순간에 필요한 입력 하나</b>뿐이고, '
              '돌아온 결과를 검증해 상태를 옮기는 일은 하네스가 한다. 조엘의 표현으로는 '
              '모델이 제안하고 하네스가 결정한다.')

# ── 제안과 결정을 가르는 자리 ────────────────────────────────────────
_bw = (W - GAP) / 2
_R_BRANCH = svg(230,
    box(0, 0, _bw, 52, ['출력이 곧 다음 행동'], 'fig-box fig-stage', 'fig-st')
    + box(_bw + GAP, 0, _bw, 52, ['출력은 제안일 뿐'], 'fig-box fig-stage', 'fig-st')
    + box(0, 66, _bw, 68, ['모델이 다음 단계를 정함'])
    + box(_bw + GAP, 66, _bw, 68, ['하네스가 검증한 뒤 옮김'], 'fig-box fig-agent')
    + down(_bw / 2, 138, 158) + down(_bw + GAP + _bw / 2, 138, 158)
    + box(0, 162, _bw, 68, ['한 번 헛디디면', '흐름이 어긋남'], 'fig-box fig-bad')
    + box(_bw + GAP, 162, _bw, 68, ['헛디딘 출력은', '상태를 못 바꿈'], 'fig-box fig-agent'),
    '모델 출력이 곧 행동이 되는 구조와 출력을 제안으로만 받는 구조의 대비')

_R_BRANCH_CAP = ('통제 문제라고 부른 대목이 이 갈림이다. <b>같은 모델이라도 출력을 제안으로 받느냐 '
                 '행동으로 받느냐에 따라 한 번의 실수가 남기는 자국이 달라진다.</b>')

# ── 모델 밖에 미리 만들어 둔 판단 셋 ─────────────────────────────────
_t_w = (W - 2 * GAP) / 3
_R_THREE = svg(200,
    box(0, 0, _t_w, 80, ['레슨이', '언제 끝났나'], 'fig-box fig-stage', 'fig-st')
    + box(_t_w + GAP, 0, _t_w, 80, ['학생이 정말', '이해했나'], 'fig-box fig-stage', 'fig-st')
    + box(2 * (_t_w + GAP), 0, _t_w, 80, ['다음에', '무엇을 하나'], 'fig-box fig-stage', 'fig-st')
    + down(_t_w / 2, 84, 106) + down(_t_w + GAP + _t_w / 2, 84, 106)
    + down(2 * (_t_w + GAP) + _t_w / 2, 84, 106)
    + mid(110, 76, ['이 셋에 딸린 질문과 행동을', '전부 모델 바깥에 설계해 뒀다'], 'fig-box fig-agent'),
    '레슨이 언제 끝났는지 학생이 이해했는지 다음에 무엇을 할지 세 판단을 모델 바깥에 두었다')

_R_THREE_CAP = ('에이스에서 특히 공들인 판단 셋이다. <b>세 물음의 답을 모델에게 묻지 않는다.</b> '
                '모델이 하는 일은 입력을 받아 그 순간의 행동 하나를 내놓는 것으로 끝난다.')


FIG_CSS += """
  .uc-fig .fig-life{stroke:var(--ink-3);stroke-width:1.2;stroke-dasharray:5 5;opacity:.6}
"""

# 보고서 형식 카드가 부르는 그림. 열쇠는 영상 ID, 값은 {이름: (제목, svg, 캡션)}.
RFIGS = {
    'm24UKZomm7k': {
        'sum':     ('한눈에 — 무엇을 바꿔 무엇을 얻었나', _R_SUM, _R_SUM_CAP),
        'fail':    ('실사용에서 깨지는 세 가지', _R_FAIL, _R_FAIL_CAP),
        'sm':      ('레슨 하나가 여섯 단계 상태 머신이다', _R_SM, _R_SM_CAP),
        'seq':     ('한 단계가 도는 순서', _R_SEQ, _R_SEQ_CAP),
        'branch':  ('제안으로 받느냐 행동으로 받느냐', _R_BRANCH, _R_BRANCH_CAP),
        'harness': ('하네스는 하나가 아니다', _P3C, _P3C_CAP),
        'three':   ('모델 밖에 미리 만들어 둔 판단 셋', _R_THREE, _R_THREE_CAP),
        'model':   ('다 맡길 때와 좁게 줄 때', _P3B, _P3B_CAP),
        'when':    ('언제 운전대를 뺏나', _P3D, _P3D_CAP),
    },
}
