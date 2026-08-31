# -*- coding: utf-8 -*-
"""원문 하나에 뷰 셋을 물어 프레임 파일로 받는다.

  PYTHONIOENCODING=utf-8 python scripts/gem_views.py <원문 md 경로> <회차 링크>

프롬프트는 scripts/prompts/{strategy,tech,merged}.txt 다. 규칙은 둘뿐이다 —
회차 밖 값은 쓰지 않는다, 값마다 성격을 단다. 나머지(문체·절 제목·표·마지막 절)는
받은 뒤 우리가 세우므로 시키지 않는다.

받은 답은 재료가 아니라 프레임 후보다. insights/frames/ 에 두고 check_frame 으로
원문과 대조한 뒤에 카드로 옮긴다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gem_ask  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPTS = os.path.join(ROOT, 'scripts', 'prompts')
FRAMES = os.path.join(ROOT, 'insights', 'frames')
OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8')

HEAD = """---
source: %s
kind: %s
model: Gemini 3.1 Pro (CDP 크롬 · playwright · 복사 버튼)
asked: scripts/prompts/%s.txt
date: %s
used:
named:
---

이 파일은 **미검증 원본**이다. `insights/check_frame.py` 로 원문과 대조한 뒤,
원문이 받쳐 주는 것만 카드로 옮긴다.

"""


def run(src, url, today):
    slug = os.path.splitext(os.path.basename(src))[0]
    got = {}
    for kind in ('strategy', 'tech', 'merged'):
        tpl = io.open(os.path.join(PROMPTS, kind + '.txt'), encoding='utf-8').read()
        text = tpl.replace('{URL}', url)
        if kind == 'merged':
            text = text.replace('{STRATEGY}', got['strategy']).replace('{TECH}', got['tech'])
        tmp = os.path.join(FRAMES, '.ask-%s.txt' % kind)
        io.open(tmp, 'w', encoding='utf-8').write(text)
        dest = os.path.join(FRAMES, '%s-%s.md' % (slug, kind))
        gem_ask.ask(io.open(tmp, encoding='utf-8').read(), dest + '.raw')
        body = io.open(dest + '.raw', encoding='utf-8').read()
        got[kind] = body
        io.open(dest, 'w', encoding='utf-8').write(
            HEAD % (src, kind, kind, today) + body)
        os.remove(dest + '.raw')
        os.remove(tmp)
        print('%s -> %s (%d자)' % (kind, os.path.basename(dest), len(body)), file=OUT)


if __name__ == '__main__':
    import datetime
    run(sys.argv[1], sys.argv[2], datetime.date.today().isoformat())
