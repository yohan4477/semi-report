# -*- coding: utf-8 -*-
"""쟁점 → 대시보드 한 장.

  PYTHONIOENCODING=utf-8 python scratchpad/gen_debate.py
"""
import glob
import io
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
                   'figs': ()},
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
