# -*- coding: utf-8 -*-
"""용어사전 장에 서는 보고서 — 「하네스 위에 무엇이 얹히나」.

용어 카드가 말 하나를 풀면 이 글은 그 말들이 한 판에서 어떻게 맞물리는지를 잇는다.
재료가 원문(뉴스레터·유튜브)이 아니라 **이 컴퓨터에 깔린 실제 설정**이라, 숫자는
scratchpad/agent_facts.py 가 파일을 세어 낸 값을 그대로 쓴다. 손으로 적지 않는다 —
스킬을 하나 더 깔면 값이 바뀌는데 본문만 옛날 수로 남는 사고를 막는다.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'scripts'))
from card_lib import fig_html
import agent_facts as F


# ── 그림 1. 부품이 판의 어느 줄에 꽂히나 ─────────────────────────────────────
# 이 글의 요지가 이 한 장이다. 부품 다섯 중 넷이 ②(컨텍스트 조립)에 꽂힌다 —
# 「도구를 확장했다」는 말이 대개 「모델에게 읽힐 글을 늘렸다」는 뜻인 이유다.
# 세로로 쌓는다. 가로로 늘어놓으면 한글 라벨이 길어 판을 넘긴다.
_ROWS = [
    ('②', '컨텍스트 조립',
     ['스킬 · 슬래시 명령 · MCP 도구 목록', 'SessionStart 훅 · UserPromptSubmit 훅'],
     '요청마다 처음부터 다시 실린다. 모델은 사이에 기억이 없다'),
    ('③', '모델이 글자를 낸다', ['꽂을 자리가 없다'],
     '여기서 하는 일은 다음 토큰을 잇는 것뿐이다'),
    ('④', '셸에서 집행', ['PreToolUse 훅 · MCP 서버'],
     '명령을 갈아치우거나 막는다. 모델은 갈아치운 줄 모른다'),
    ('⑥', '결과를 줄여 되먹임', ['PostToolUse 훅'],
     '로그를 깎아 ②로 되돌린다. 깎는 판단은 모델 밖에 있다'),
]
_SUB = ('서브에이전트 — 위 네 줄을 통째로 한 판 더 연다',
        '그 판이 무엇을 읽었는지는 이 판에 안 남는다. 보고 한 덩어리만 ⑥으로 들어온다')


def _map_svg():
    x0, lw, rx, rw = 12, 152, 178, 370
    y0, gap, lh = 34, 10, 19
    o, y = [], y0
    rects = []
    for num, station, parts, note in _ROWS:
        h = 20 + lh * (len(parts) + 1)
        rects.append((y, h, num, station, parts, note))
        y += h + gap
    ysub = y + 4
    hsub = 20 + lh * 2
    tot = ysub + hsub + 14
    o.append('<svg viewBox="0 0 560 %d" role="img" aria-label="하네스 한 판의 줄마다 '
             '어떤 부품이 꽂히는지">' % tot)
    o.append('<text x="12" y="20" class="t-head">하네스가 도는 한 판</text>')
    o.append('<text x="178" y="20" class="t-head">그 줄에 꽂히는 부품</text>')
    for y, h, num, station, parts, note in rects:
        o.append('<rect class="body" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
                 % (x0, y, lw, h))
        o.append('<text x="%d" y="%d" class="t-no">%s</text>' % (x0 + 10, y + h // 2 + 7, num))
        o.append('<text x="%d" y="%d" class="t-lab">%s</text>'
                 % (x0 + 38, y + h // 2 + 4, station))
        o.append('<line class="lead-line" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (x0 + lw, y + h // 2, rx, y + h // 2))
        o.append('<rect class="body" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
                 % (rx, y, rw, h))
        ty = y + 22
        for i, line in enumerate(parts):
            cls = 't-bad' if line == '꽂을 자리가 없다' else 't-lab'
            o.append('<text x="%d" y="%d" class="%s">%s</text>' % (rx + 12, ty, cls, line))
            ty += lh
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (rx + 12, ty, note))
    o.append('<rect class="body" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
             % (x0, ysub, rx + rw - x0, hsub))
    o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (x0 + 14, ysub + 22, _SUB[0]))
    o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (x0 + 14, ysub + 22 + lh, _SUB[1]))
    o.append('</svg>')
    return ''.join(o)


FIG_MAP = ('부품 다섯이 판의 어느 줄에 꽂히나', _map_svg(),
           '스킬도 슬래시 명령도 MCP 도구 목록도 전부 <b>②</b> 한 줄에 꽂힙니다 — 모델에게 '
           '읽힐 글을 늘리는 일입니다. 실행을 실제로 바꾸는 부품은 훅뿐이고, ③에는 꽂을 자리가 '
           '아예 없습니다. 「도구를 확장했다」는 말이 대개 무엇을 뜻하는지가 이 배치에 있습니다.')


# ── 그림 2. 스킬이 두 단계로 열린다 ──────────────────────────────────────────
# 값은 agent_facts 가 이 저장소 .claude/skills/ 를 세어 낸 실측이다. 막대 길이가
# 곧 그 값이라 손으로 늘리지 않는다.
def _skill_svg():
    x0, xr, top, bh, gap = 14, 168, 42, 26, 34
    span = 470 - xr        # 가장 긴 막대 뒤에 값 라벨이 설 자리를 남긴다
    bars = [('평소 실리는 것', F.CH_DESC,
             '스킬 %d개의 설명 한 줄씩' % F.N_SKILL),
            ('한 장이 열릴 때', F.CH_ONE, '그 스킬 본문 하나 (평균)'),
            ('처음부터 다 실으면', F.CH_BODY, '본문 %d개 전부' % F.N_SKILL)]
    tot = top + len(bars) * (bh + gap) + 4
    o = ['<svg viewBox="0 0 560 %d" role="img" aria-label="스킬이 평소 차지하는 '
         '글자수와 전부 실었을 때의 글자수 비교">' % tot]
    o.append('<text x="14" y="22" class="t-head">요청 하나에 실리는 스킬 글자수</text>')
    for i, (lab, v, note) in enumerate(bars):
        y = top + i * (bh + gap)
        w = max(2, int(span * v / F.CH_BODY))
        o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (x0, y + 17, lab))
        o.append('<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="3"/>'
                 % ('good' if i == 0 else ('cell' if i == 1 else 'bad'), xr, y, w, bh))
        o.append('<text x="%d" y="%d" class="t-lab">%s자</text>'
                 % (xr + w + 9, y + 17, '{:,}'.format(v)))
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (x0, y + 34, note))
    o.append('</svg>')
    return ''.join(o)


FIG_SKILL = ('스킬 %d개를 깔아도 평소에는 %.1f%%만 실린다' % (F.N_SKILL, F.PCT_DESC),
             _skill_svg(),
             '이 저장소에 걸리는 스킬 <b>%d개</b>를 실측한 값입니다. 본문을 다 합치면 '
             '<b>%s자</b>인데 평소 실리는 것은 각 스킬의 설명 한 줄씩 <b>%s자</b>, 전체의 '
             '<b>%.1f%%</b>입니다. 지금 하는 일과 맞는 한 장이 열릴 때만 그 본문 '
             '<b>%s자</b>가 더해집니다. 스킬을 백 개 깔아도 평소 부담이 안 늘어나는 이유가 '
             '이 두 단계입니다.'
             % (F.N_SKILL, '{:,}'.format(F.CH_BODY), '{:,}'.format(F.CH_DESC),
                F.PCT_DESC, '{:,}'.format(F.CH_ONE)))


# ── 그림 3. 플러그인 상자 안에 무엇이 들었나 ─────────────────────────────────
# 개수는 agent_facts 가 플러그인 캐시 폴더를 세어 낸 실측이다. 두 상자를 나란히 두는
# 것이 요지다 — 「플러그인 = 스킬 묶음」이 아니라 상자마다 담긴 것이 다르다.
_SLOTS = [('스킬', 'skills'), ('슬래시 명령', 'commands'),
          ('서브에이전트', 'agents'), ('훅', 'hooks')]


def _plug_svg():
    bw, bx = 262, (14, 284)
    top, rh = 32, 24
    hd = 26
    bh = hd + len(_SLOTS) * rh + 14
    o = ['<svg viewBox="0 0 560 %d" role="img" aria-label="플러그인 두 개에 각각 '
         '스킬·명령·서브에이전트·훅이 몇 개 들었는지">' % (top + bh + 12)]
    o.append('<text x="14" y="20" class="t-head">플러그인 한 상자에 담기는 것 넷</text>')
    for x, pl, sub in ((bx[0], F.CAVEMAN, '훅으로 말투를 바꾼다'),
                       (bx[1], F.SUPERPOWERS, '스킬만으로 절차를 준다')):
        if not pl:
            continue
        o.append('<rect class="body" x="%d" y="%d" width="%d" height="%d" rx="10"/>'
                 % (x, top, bw, bh))
        o.append('<text x="%d" y="%d" class="t-lab">%s</text>'
                 % (x + 14, top + 19, pl['name']))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end">%s</text>'
                 % (x + bw - 14, top + 19, sub))
        for i, (lab, key) in enumerate(_SLOTS):
            y = top + hd + 18 + i * rh
            o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (x + 14, y, lab))
            n = pl[key]
            o.append('<text x="%d" y="%d" class="%s" text-anchor="end">%s</text>'
                     % (x + bw - 14, y, 't-lab' if n else 't-sm',
                        ('%d개' % n) if n else '없음'))
    o.append('</svg>')
    return ''.join(o)


FIG_PLUG = ('같은 플러그인이라도 담긴 것이 다르다', _plug_svg(),
            '이 컴퓨터에 깔린 두 상자를 세어 본 값입니다. <b>caveman</b>은 훅 <b>%d</b>가지 '
            '이벤트에 붙어 말투 자체를 바꾸고, <b>superpowers</b>는 훅 <b>%d</b>개와 스킬 '
            '<b>%d개</b>로 절차만 줍니다. 「플러그인을 깔았다」는 말만으로는 무엇이 달라지는지 '
            '알 수 없고, 상자를 열어 이 네 칸을 봐야 압니다 — 훅이 든 상자는 사용자가 '
            '아무것도 부르지 않아도 이미 동작을 바꾸고 있습니다.'
            % ((F.CAVEMAN or {}).get('hooks', 0), (F.SUPERPOWERS or {}).get('hooks', 0),
               (F.SUPERPOWERS or {}).get('skills', 0)))


# ── 그림 4. 훅이 명령을 갈아치우는 자리 ──────────────────────────────────────
# 이 컴퓨터의 실제 설정 하나를 그린다 — ~/.claude/settings.json 의 PreToolUse 훅.
_HOOK = [('모델이 적어 보낸 것', 'git status'),
         ('PreToolUse 훅', 'rtk hook claude'),
         ('셸에서 실제로 돈 것', 'rtk git status')]


def _hook_svg():
    w, gap, x0, top, h = 168, 13, 14, 32, 52
    o = ['<svg viewBox="0 0 560 %d" role="img" aria-label="모델이 적은 명령을 훅이 '
         '갈아치워 셸에 넘기는 세 걸음">' % (top + h + 40)]
    o.append('<text x="14" y="20" class="t-head">모델이 적은 명령이 셸에 닿기까지</text>')
    for i, (lab, cmd) in enumerate(_HOOK):
        x = x0 + i * (w + gap + 13)
        o.append('<rect class="body" x="%d" y="%d" width="%d" height="%d" rx="8"/>'
                 % (x, top, w, h))
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (x + 12, top + 19, lab))
        o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (x + 12, top + 38, cmd))
        if i < len(_HOOK) - 1:
            o.append('<line class="flow" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                     % (x + w + 3, top + h // 2, x + w + gap + 10, top + h // 2))
    o.append('<text x="14" y="%d" class="t-sm">모델은 자기가 적은 줄이 그대로 돌았다고 '
             '여긴다. 갈아치운 사실은 대화에 남지 않는다.</text>' % (top + h + 26))
    o.append('</svg>')
    return ''.join(o)


FIG_HOOK = ('훅은 모델을 거치지 않는 자리에 선다', _hook_svg(),
            '이 컴퓨터의 <code>~/.claude/settings.json</code>에 실제로 걸린 설정입니다 — '
            '<code>Bash</code> 도구를 부를 때마다 <code>rtk hook claude</code>가 먼저 돌아 '
            '명령을 갈아 끼웁니다(<code>RTK.md</code>). 프롬프트로 부탁하는 것과 다른 점은 '
            '<b>모델의 판단을 아예 안 거친다</b>는 것입니다. 스킬은 읽고 안 따를 수 있지만 '
            '훅은 따르고 말고가 없습니다.')
