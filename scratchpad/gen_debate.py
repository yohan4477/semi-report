# -*- coding: utf-8 -*-
"""쟁점 → 대시보드 한 장.

  PYTHONIOENCODING=utf-8 python scratchpad/gen_debate.py
"""
import glob
import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'insights'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import dash_common as dc
import debate_lib as dl
import notes_lib as nl
import paths

SILENT_RE = re.compile(r'^[-*][ \t]*(.+?)[ \t]*—[ \t]*(.+?)[ \t]*$')

# 섹션은 카드의 meta['section'] 값을 열쇠말로 찾는다. 지금은 market 하나뿐이지만
# 새 열쇠말이 생기면 여기에 자리를 정해 준다(gen_undreport_dashboard.py의 SEC와 같은 방식).
SEC = {
    'market': ('sec-market', '01', '시장 · 매크로',
               '금리·수급처럼 같은 시장을 놓고 화자들이 인과를 반대로 놓은 자리'),
}


# 관계 종류 셋 — 선 모양으로 가른다(색으로만 가르지 않는다). 값은 빈 문자열이면 실선이다.
# 단독은 이 표에 없다 — 단독은 선이 없다(against가 없으므로 애초에 선을 안 그린다).
STANCE_DASH = {'충돌': '', '동의': '2 5', '결다름': '9 5'}
STANCE_ORDER = ('충돌', '동의', '결다름')


def _trim(t, n):
    t = t or ''
    return t if len(t) <= n else t[:n] + '…'


def rel_svg(voices):
    """화자 발언 사이 관계 하나를 그림 하나로. 노드는 화자가 아니라 발언이다 — 같은
    화자의 다른 글도 각각 딴 점으로 놓는다. 나르는 것은 관계 종류(충돌·동의·결다름·
    단독) 하나뿐이다 — 노드 사이 거리·선 굵기·노드 크기에는 뜻을 싣지 않는다.

    좌표는 손으로 안 찍는다. n개 발언을 원 위에 12시부터 시계 방향으로 고르게
    놓고(각도만 계산), 이름표는 그 각도를 따라 원 밖으로 낸다. 이름표를 원 반지름
    R보다 더 먼 반지름 Rl(>R)에서 시작하게 하면, 두 발언을 잇는 현(弦)은 언제나
    반지름 R 안쪽에만 머물러(원은 볼록) 이름표 글자를 절대 지나지 않는다 —
    좌표를 눈으로 맞추지 않고 이 성질로 겹침을 원천 차단한다.

    카드 본문(debate_html)이 이 문자열을 그대로 끼워 넣는다 — .uc-fig 붓을 못
    받으므로 색은 전부 인라인 style로 CSS 변수를 직접 문다(scripts/dash_base_css.html
    에 있는 --ink·--ink-2·--ink-3·--line·--surface·--sunk만 쓴다).
    """
    n = max(len(voices), 1)
    keys = [dl.voice_key(v) for v in voices]
    cx, cy, R, Rl, r_node = 410, 240, 130, 195, 5
    vw, vh = 820, 520
    pts = []
    for i in range(n):
        ang = math.radians(-90 + i * 360.0 / n)
        dx, dy = math.cos(ang), math.sin(ang)
        pts.append((cx + R * dx, cy + R * dy, cx + Rl * dx, cy + Rl * dy, dx, dy))

    # against가 다른 발언의 voice_key와 같으면 잇는다. 같은 짝을 두 번 안 긋는다 —
    # 08-20 두 글처럼 서로가 서로를 against로 적어도 선은 하나다.
    edges = {}
    for i, v in enumerate(voices):
        against = (v.get('against') or '').strip()
        stance = v.get('stance', '')
        if not against or stance not in STANCE_DASH or against not in keys:
            continue
        j = keys.index(against)
        if j != i:
            edges.setdefault(frozenset((i, j)), stance)

    h = ['<div style="margin:16px 0;border:1px solid var(--line);border-radius:12px;'
         'padding:14px 10px 10px;background:var(--sunk)">',
         '<svg viewBox="0 0 %d %d" style="display:block;width:100%%;height:auto;'
         'max-width:640px;margin:0 auto" xmlns="http://www.w3.org/2000/svg">' % (vw, vh)]

    for pair, stance in edges.items():
        i, j = tuple(pair)
        dash = STANCE_DASH[stance]
        h.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                 'style="stroke:var(--ink-3);stroke-width:1.8"%s/>'
                 % (pts[i][0], pts[i][1], pts[j][0], pts[j][1],
                    ' stroke-dasharray="%s"' % dash if dash else ''))

    for i, v in enumerate(voices):
        nx, ny, lx, ly, dx, dy = pts[i]
        h.append('<circle cx="%.1f" cy="%.1f" r="%d" '
                  'style="fill:var(--surface);stroke:var(--ink-3);stroke-width:2"/>'
                  % (nx, ny, r_node))
        if dx > 0.35:
            anchor = 'start'
        elif dx < -0.35:
            anchor = 'end'
        else:
            anchor = 'middle'
        # 위쪽 발언은 두 줄을 더 위로 밀어 올린다 — 그래도 항상 화자·날짜 줄이
        # 제목 줄보다 위에 온다(읽는 순서가 사분면마다 뒤집히지 않는다)
        if dy < -0.35:
            y_actor, y_title = ly - 14, ly
        else:
            y_actor, y_title = ly, ly + 14
        actor_line = '%s %s' % (_trim(v['actor'], 10), v['said'][5:])
        title_line = '「%s」' % _trim(v.get('title', ''), 12)
        h.append('<text x="%.1f" y="%.1f" text-anchor="%s" '
                  'style="fill:var(--ink);font-size:12.5px;font-weight:700">%s</text>'
                  % (lx, y_actor, anchor, actor_line))
        h.append('<text x="%.1f" y="%.1f" text-anchor="%s" '
                  'style="fill:var(--ink-3);font-size:11.5px">%s</text>'
                  % (lx, y_title, anchor, title_line))
        if v.get('stance') == '단독':
            y_tag = y_title + 14 if dy >= -0.35 else y_actor - 14
            h.append('<text x="%.1f" y="%.1f" text-anchor="%s" '
                      'style="fill:var(--ink-3);font-size:10.5px">단독</text>'
                      % (lx, y_tag, anchor))

    # 범례 — 이 그림에 실제로 쓰인 관계 종류만 낸다. 선 모양이 먼저고 색은 거들 뿐이다.
    used = [s for s in STANCE_ORDER if s in edges.values()]
    lx0, ly0 = 40, vh - 31
    for stance in used:
        dash = STANCE_DASH[stance]
        h.append('<line x1="%d" y1="%d" x2="%d" y2="%d" '
                  'style="stroke:var(--ink-3);stroke-width:1.8"%s/>'
                  % (lx0, ly0, lx0 + 30, ly0,
                     ' stroke-dasharray="%s"' % dash if dash else ''))
        tx = lx0 + 40
        h.append('<text x="%d" y="%d" style="fill:var(--ink-2);font-size:12px">%s</text>'
                  % (tx, ly0 + 4, stance))
        lx0 = tx + len(stance) * 13 + 34
    h.append('</svg></div>')
    return ''.join(h)


def silent_of(sec):
    out = []
    for line in sec.split('\n'):
        m = SILENT_RE.match(line)
        if m:
            out.append({'actor': m.group(1), 'why': m.group(2)})
    return out


def card_of(path):
    text = io.open(path, encoding='utf-8').read()
    d = dl.parse(text)
    meta, secs, src = d['meta'], d['sections'], d['sources']
    voices = []
    for v in d['voices']:
        v = dict(v)
        v['body'] = nl.md_body(v['body'], src)
        voices.append(v)
    mod = {k: nl.md_body(secs.get(k, ''), src) for k in dl.MODERATOR}
    actors = []
    for v in d['voices']:
        if v['actor'] not in actors:
            actors.append(v['actor'])
    sec_key = meta.get('section', 'market').strip()
    assert sec_key in SEC, '없는 섹션 열쇠말: %r — %s' % (sec_key, path)
    return {
        'title': meta.get('question', '').strip().strip('"'),
        'gain': meta.get('subhead', '').strip().strip('"'),
        'section': SEC[sec_key],
        'meta': [' · '.join(actors), meta.get('as_of', '')],
        'links': [('원문 「%s」 ↗' % s['base'], dc.blob(s['file']), '')
                  for s in src],
        'debate': {'question': meta.get('question', ''),
                   'moderator': mod,
                   'voices': voices,
                   'silent': silent_of(secs.get('답하지 않은 화자', '')),
                   'figs': (rel_svg(d['voices']),)},
    }


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    cards = [card_of(p) for p in sorted(glob.glob(
        os.path.join(paths.DEBATE, '*.md')))]
    assert cards, '올릴 쟁점이 하나도 없다'
    dc.check_labels(cards)
    out = os.path.join(ROOT, '대시보드', '쟁점 대시보드.html')
    header = ('  <header>\n'
              '    <p class="eyebrow">쟁점 — 화자들이 갈린 자리</p>\n'
              '    <h1>쟁점</h1>\n'
              '    <p class="lede">같은 물음에 화자들이 갈린 자리를 나란히 놓습니다. '
              '화자 말은 원문 인용이고, 진행자 말이 판단입니다.</p>\n'
              '  </header>')
    dc.render(cards, title='쟁점',
              header=header,
              footer='화자 말은 원문 인용이고 진행자 말은 판단이다. '
                     '화자들은 서로를 읽지 않는다 — 이 자리는 그것을 나란히 놓은 것이다.',
              out=out, newest_first=True)
    html = io.open(out, encoding='utf-8').read()
    dc.check_ui(html, has_top=False)
    print('쟁점 %d장 → %s' % (len(cards), out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
