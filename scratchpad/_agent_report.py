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


# 보고서 층에 실리는 도해 전부. check_fig 가 이 목록으로 배치를 검사한다.
FIGS = [FIG_MAP, FIG_SKILL, FIG_PLUG, FIG_HOOK]


HEAD = ('<div class="rep-head"><span class="rn">보고서</span>'
        '<h2 id="rep-agent">하네스 위에 무엇이 얹히나 — 스킬·명령·서브에이전트·훅·MCP</h2>'
        '<p class="rm">바탕 <b>이 컴퓨터의 실제 설정</b> · 실측일 <b>%s</b> · '
        '스킬 %d개 · 플러그인 %d개<br>'
        '용어 카드가 말 하나를 푼다면 이 글은 그 말들이 한 판에서 어떻게 맞물리는지를 잇습니다.'
        '</p></div>')


def report_html(fig_seq, stamp):
    """보고서 본문. fig_seq는 용어사전 카드가 이미 갖고 있는 하네스 시퀀스 도해다 —
    여기서 다시 그리면 한쪽만 고쳐지는 사고가 난다."""
    h = [HEAD % (stamp, F.N_SKILL, len(F.ENABLED))]
    sec = lambda t: h.append('<h3>%s</h3>' % t)
    p = lambda t: h.append('<p class="ins-lede">%s</p>' % t)
    fig = lambda *items: h.append(''.join(fig_html(f) for f in items))

    # ── 1 ──────────────────────────────────────────────────────────────────
    sec('1. 「스킬을 깔았다」고 할 때 무엇이 어디에 깔리나')
    p('클로드 코드에 무언가를 더하는 방법이 다섯 가지 있습니다. 스킬·슬래시 명령·'
      '서브에이전트·훅·MCP 서버입니다. 이름만 보면 다섯이 비슷한 층에 있는 것 같지만 '
      '꽂히는 자리가 다릅니다. 어디에 꽂히느냐가 그 부품으로 무엇을 할 수 있고 무엇을 '
      '못 하는지를 정합니다.')
    p('앞선 용어 카드에서 하네스(harness)를 열두 걸음으로 풀었습니다. 그 열두 걸음 가운데 '
      '부품이 실제로 꽂히는 줄은 셋뿐입니다.')
    fig(FIG_MAP)
    p('이 배치에서 읽을 것이 하나 있습니다. 다섯 중 넷이 <b>②</b>에 꽂힙니다. '
      '②는 모델을 부르기 직전에 지금까지의 상태를 글로 조립하는 자리입니다. 즉 '
      '「도구를 확장했다」는 말은 대개 <b>모델에게 읽힐 글을 늘렸다</b>는 뜻입니다. '
      '실행을 실제로 바꾸는 부품은 훅 하나뿐이고, 나머지는 모델이 읽고 판단하기를 '
      '기대하는 것입니다.')

    # ── 2 ──────────────────────────────────────────────────────────────────
    sec('2. 다섯 이름부터 가른다')
    p('부르는 주체와 꽂히는 자리로 가르면 섞이지 않습니다.')
    p('<b>스킬(skill)</b>은 폴더 하나에 담은 절차서입니다. 모델이 「지금 이 일에 필요하다」고 '
      '판단해 스스로 엽니다. <b>슬래시 명령(slash command)</b>도 글을 넣는 것은 같은데, '
      '사람이 <code>/이름</code>을 쳐야 열립니다. <b>서브에이전트(subagent)</b>는 판을 '
      '통째로 하나 더 여는 것입니다. 그 판에서 무엇을 읽었든 이 판에는 마지막 보고 '
      '한 덩어리만 돌아옵니다.')
    p('<b>훅(hook)</b>은 정해진 시점에 무조건 도는 프로그램입니다. 모델의 판단을 '
      '거치지 않습니다. <b>MCP 서버(Model Context Protocol server)</b>는 도구 목록을 '
      '하네스 밖에서 꽂는 규격입니다. 이 컴퓨터에는 %s 셋이 붙어 있습니다. '
      '<b>플러그인(plugin)</b>은 이 다섯을 한 상자에 담아 남에게 넘기는 포장입니다.'
      % ' · '.join('<code>%s</code>' % m for m in F.MCP))

    # ── 3 ──────────────────────────────────────────────────────────────────
    sec('3. 부품이 꽂히는 판은 어떻게 도나')
    p('앞 절의 배치를 읽으려면 판 자체를 먼저 봐야 합니다. 아래 그림은 용어 카드에 실린 '
      '것과 같은 그림입니다.')
    fig(fig_seq)
    p('요점은 <b>②가 요청마다 되풀이된다</b>는 것입니다. 모델은 요청과 요청 사이에 아무것도 '
      '기억하지 않습니다. 지금 어느 디렉터리에 있는지, 무엇을 이미 고쳤는지, 쓸 수 있는 '
      '도구가 무엇인지를 매번 처음부터 다시 적어 보냅니다. 열두 걸음짜리 한 판이면 ②가 '
      '대여섯 번 되풀이됩니다.')
    p('그래서 ②에 무엇을 얹느냐가 값을 정합니다. 얹은 글은 한 번 읽히고 끝나지 '
      '않습니다. 판이 도는 내내 매 요청에 다시 실립니다.')

    # ── 4 ──────────────────────────────────────────────────────────────────
    sec('4. 스킬은 왜 두 단계로 열리나')
    p('절차서를 통째로 ②에 얹으면 그 값을 매 요청 물게 됩니다. 스킬은 이것을 두 단계로 '
      '나눠 피합니다. 평소에는 각 스킬의 <code>description</code> 한 줄만 실리고, 지금 하는 '
      '일과 맞는 한 장이 나타났을 때만 그 본문이 더해집니다.')
    fig(FIG_SKILL)
    p('이 저장소에서 실제로 재 본 값입니다. 스킬 %d개의 본문을 다 합치면 %s자인데 평소 '
      '실리는 것은 %s자, 전체의 %.1f%%입니다. 스킬을 스무 개 더 깔아도 평소 부담은 '
      '설명 한 줄씩만 늘어납니다.'
      % (F.N_SKILL, '{:,}'.format(F.CH_BODY), '{:,}'.format(F.CH_DESC), F.PCT_DESC))
    p('대가가 있습니다. 열리는 판단이 <code>description</code> 한 줄에 걸립니다. 그 줄이 '
      '지금 하는 일을 못 가리키면 본문은 영영 안 읽힙니다. 스킬을 쓸 만하게 만드는 일의 '
      '절반은 본문이 아닙니다. 그 한 줄을 다듬는 일입니다.')

    # ── 5 ──────────────────────────────────────────────────────────────────
    sec('5. 슬래시 명령은 스킬과 무엇이 다른가')
    p('둘 다 ②에 글을 얹습니다. 다른 것은 <b>누가 여느냐</b> 하나입니다. 스킬은 모델이 '
      '설명 한 줄을 보고 스스로 열고, 슬래시 명령은 사람이 <code>/이름</code>을 쳐야 '
      '열립니다.')
    p('이 차이가 쓰임을 가릅니다. 「이 작업을 할 때는 반드시 이 절차를 따라라」처럼 '
      '모델이 알아서 집어야 하는 것은 스킬이어야 합니다. 「지금 이걸 해라」처럼 사람이 '
      '시점을 정하는 것은 명령이어야 합니다. 커밋 메시지를 만드는 일을 스킬로 두면 '
      '모델이 안 부를 때가 생기고, 문체 규칙을 명령으로 두면 사람이 매번 쳐야 합니다.')
    p('이 저장소에는 슬래시 명령이 %d개, 스킬이 %d개 있습니다. 규칙이 「글을 쓰기 전에 '
      '반드시 연다」는 성격이라 전부 스킬 쪽에 있습니다.' % (F.N_CMD_REPO, F.N_SKILL))

    # ── 6 ──────────────────────────────────────────────────────────────────
    sec('6. 서브에이전트는 왜 컨텍스트를 아끼나')
    p('서브에이전트는 판을 하나 더 여는 것입니다. 새 판에는 새 컨텍스트 창이 붙습니다. '
      '거기서 파일 마흔 개를 읽든 로그 만 줄을 훑든, 이 판에 돌아오는 것은 마지막 보고 '
      '한 덩어리뿐입니다.')
    p('이 저장소가 서브에이전트를 두는 이유가 그것입니다. <code>semianalysis-transformer</code>는 '
      '영어 뉴스레터 원문 한 편을 통째로 읽어 한국어 변환본을 씁니다. 원문이 수만 자라 '
      '메인 판에서 읽으면 그 뒤 작업 내내 그 글자가 매 요청에 다시 실립니다. 따로 연 '
      '판에서 읽고 결과 파일만 남기면 메인 판은 그 원문을 한 번도 안 봅니다.')
    p('대가는 두 가지입니다. 새 판은 이 판이 지금까지 알아낸 것을 모릅니다. 무엇을 하라는 '
      '지시를 처음부터 다 적어 보내야 합니다. 그리고 그 판이 무엇을 잘못 읽었는지도 이 판에 '
      '안 남습니다. 돌아온 보고를 그대로 믿게 되는 구조라, 틀린 값이 조용히 들어오는 사고가 '
      '여기서 납니다. 이 컴퓨터에는 서브에이전트가 저장소에 %d개, 사용자 설정에 %d개 '
      '있습니다.' % (F.N_AGENT_REPO, F.N_AGENT_USER))

    # ── 7 ──────────────────────────────────────────────────────────────────
    sec('7. 훅은 무엇을 할 수 있고 스킬은 왜 못 하나')
    p('앞의 셋은 전부 모델에게 글을 읽히는 일입니다. 읽고 안 따를 수 있습니다. 훅은 '
      '다릅니다. 정해진 시점에 프로그램이 무조건 돌고, 모델은 그 프로그램을 막을 수단이 '
      '없습니다.')
    fig(FIG_HOOK)
    p('이 컴퓨터의 <code>~/.claude/settings.json</code>에 걸린 훅이 %s입니다. '
      '<code>Bash</code> 도구를 부를 때마다 먼저 돌아 명령을 갈아 끼웁니다. 같은 일을 '
      '「앞에 rtk를 붙여라」라고 규칙 문서에 적어 둘 수도 있습니다. 그러면 모델이 잊는 '
      '날이 생깁니다. 훅에는 잊는 날이 없습니다.'
      % ' · '.join('<code>%s</code>' % e for e in F.HOOK_EVENTS))
    p('훅이 붙을 수 있는 시점은 판의 여러 자리입니다. 세션이 열릴 때(<code>SessionStart</code>), '
      '사람이 무언가를 칠 때(<code>UserPromptSubmit</code>), 도구를 부르기 직전'
      '(<code>PreToolUse</code>), 도구가 끝난 뒤(<code>PostToolUse</code>). 앞의 둘은 ②에 '
      '글을 얹는 일이고 뒤의 둘은 집행을 가로채는 일입니다. 같은 훅이라도 어느 시점에 '
      '거느냐로 성격이 완전히 갈립니다.')

    # ── 8 ──────────────────────────────────────────────────────────────────
    sec('8. MCP 서버는 도구를 어디에 꽂나')
    p('MCP(Model Context Protocol)는 도구 목록을 하네스 밖에서 꽂는 규격입니다. 하네스가 '
      '기본으로 주는 도구는 파일 읽기·쓰기·셸 실행 정도입니다. 지메일을 읽거나 브라우저를 '
      '몰거나 사내 데이터베이스를 뒤지는 일은 하네스 안에 없습니다. MCP 서버를 붙이면 그 '
      '서버가 「내가 할 수 있는 일은 이것들이다」를 하네스에 알리고, 하네스가 그 목록을 ②에 '
      '얹습니다.')
    p('이 컴퓨터에는 %s 셋이 붙어 있습니다. 꽂히는 자리가 둘이라는 것이 중요합니다. '
      '도구 목록은 ②에 실리고 실제 집행은 ④에서 일어나는데, 그 일을 하는 것은 셸이 '
      '아닙니다. 하네스가 따로 띄운 그 서버 프로세스입니다.'
      % ' · '.join('<code>%s</code>' % m for m in F.MCP))
    p('여기에 스킬과 똑같은 문제가 생깁니다. 도구가 백 개면 그 설명 백 개가 매 요청 ②에 '
      '실립니다. 그래서 요즘 하네스는 도구 정의도 두 단계로 나눕니다. 평소에는 이름만 '
      '싣고, 필요할 때 검색해서 그 도구의 규격만 불러옵니다. 스킬이 설명 한 줄과 본문을 '
      '나눈 것과 같은 처방입니다.')
    return ''.join(h)
