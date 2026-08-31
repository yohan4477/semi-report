# -*- coding: utf-8 -*-
"""원문 하나에 뷰 둘(전략·기술)을 물어 프레임 파일로 받는다.

  PYTHONIOENCODING=utf-8 python scripts/gem_views.py <원문 md 경로> <회차 링크>

프롬프트는 scripts/prompts/{strategy,tech}.txt 다. 시키는 것은 셋뿐이다 —
회차 밖 값은 쓰지 않는다, 값마다 성격을 단다, 그림으로 보이면 쉬운 대목에는 도해를
넣는다. **도해를 어떻게 그리라고는 안 적는다** — 꼴을 길게 달아도 그대로 오지 않고,
받는 꼴을 맞추는 일은 frame_view 가 한다. 나머지(문체·절 제목·표·마지막 절)도 받은 뒤
우리가 세우므로 시키지 않는다.

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
model: %s (CDP 크롬 · playwright · 복사 버튼)
asked: scripts/prompts/%s.txt
date: %s
used:
named:
---

이 파일은 **미검증 원본**이다. `insights/check_frame.py` 로 원문과 대조한 뒤,
원문이 받쳐 주는 것만 카드로 옮긴다.

"""


def run(src, url, today, allow_lower=False):
    # 링크만 주면 못 읽고 배경지식으로 쓰는 일이 있다 — 2026-08-31 에 기술 뷰가
    # 「유료라 원문을 못 긁는다」고 적고 업계 동향으로 답했다. **전문을 같이 보낸다.**
    # 우리가 옮긴 요약본은 사실을 골라 담은 중간물이라 그 선택까지 넘어간다 —
    # 무엇을 고를지는 받는 쪽이 해야 뷰가 뷰다. 무료로 푸는 매체라 보낼 수 있다
    slug = os.path.splitext(os.path.basename(src))[0]
    raw = os.path.join(ROOT, os.path.dirname(src), 'raw', os.path.basename(src))
    assert os.path.exists(raw), '전문이 없다. scripts/semidoped_clip.py 로 먼저 긁는다: ' + raw
    src_text = io.open(raw, encoding='utf-8').read()
    # 뷰는 둘이다. 통합 뷰는 걷었다 — 두 뷰를 합쳐 받아 보니 혼자 가진 대목이 없었고
    # (2026-08-31 할라페뇨 대조), 카드로도 안 섰다
    got = {}
    for kind in ('strategy', 'tech'):
        tpl = io.open(os.path.join(PROMPTS, kind + '.txt'), encoding='utf-8').read()
        text = tpl.replace('{URL}', url).replace('{SOURCE}', src_text)
        tmp = os.path.join(FRAMES, '.ask-%s.txt' % kind)
        io.open(tmp, 'w', encoding='utf-8').write(text)
        dest = os.path.join(FRAMES, '%s-%s.md' % (slug, kind))
        # 실제로 걸린 모델 이름을 받아 머리말에 적는다 — 하드코딩하면 한도가 차서 낮은
        # 모델이 답한 날에도 「3.1 Pro」라고 적힌다
        model = gem_ask.ask(io.open(tmp, encoding='utf-8').read(), dest + '.raw',
                            allow_lower=allow_lower)
        body = io.open(dest + '.raw', encoding='utf-8').read()
        got[kind] = body
        io.open(dest, 'w', encoding='utf-8').write(
            HEAD % (src, kind, model, kind, today) + body)
        os.remove(dest + '.raw')
        os.remove(tmp)
        print('%s -> %s (%d자)' % (kind, os.path.basename(dest), len(body)), file=OUT)


if __name__ == '__main__':
    import datetime
    # 세 번째 인자로 --allow-lower 를 주면 한도가 찼을 때 낮은 모델로도 받는다
    run(sys.argv[1], sys.argv[2], datetime.date.today().isoformat(),
        allow_lower='--allow-lower' in sys.argv[3:])
