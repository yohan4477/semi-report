# -*- coding: utf-8 -*-
"""원문 하나에 뷰 둘(전략·기술)을 물어 프레임 파일로 받는다.

  PYTHONIOENCODING=utf-8 python scripts/gem_views.py <원문 md 경로> <회차 링크>

프롬프트는 조각으로 나뉜다. 앵글(`prompts/{strategy,tech}.txt`)이 페르소나와 그
앵글에만 걸리는 요구를 적고, 그 뒤에 공통 조각(`공통-값.txt` · `공통-도해.txt`)을
붙인다. 앵글은 둘로 고정이다 — 경영전략 컨설턴트와 업계 기술 전문가.

**도해는 어떻게 그리라고 적는다**(공통-도해). 예전에는 안 적었다 — 꼴을 달아도 그대로
안 온다고 봤고 받는 꼴은 frame_view 가 맞춘다고 여겼다. 2026-09-01 에 받은 판 열일곱을
경영 관점으로 훑어 보니 그게 아니었다: 분류를 화살표로 긋고, 한 판에 꼴 둘셋을 섞고,
갈래에 축이 없고, 대비 칸에 양쪽 다 있는 값을 넣었다. 배치는 frame_view 가 고쳐 주지만
**무엇을 무엇과 견줄지는 고쳐 줄 수 없다.** 그래서 규칙 여섯을 프롬프트로 옮겼다.

나머지(문체·절 제목·표·마지막 절)는 받은 뒤 우리가 세우므로 시키지 않는다.

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
# 앵글 파일 뒤에 이 차례로 붙인다. 앵글이 둘(경영전략·기술)뿐이라도 규칙은 공통이다
COMMON = ('공통-값.txt', '공통-도해.txt')
FRAMES = os.path.join(ROOT, 'insights', 'frames')
OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8')

HEAD = """---
source: %s
kind: %s
model: %s (CDP 크롬 · playwright · 복사 버튼)
asked: scripts/prompts/%s.txt + 공통-값 + 공통-도해
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
        # 앵글 파일 + 공통 조각을 조립한다. 규칙을 앵글마다 복사해 두면 한쪽만 고치게
        # 된다 — 2026-09-01 에 도해 규칙을 실험 사본에만 넣고 운영 프롬프트는 옛
        # 것으로 남겨 뒀다. 규칙이 사는 자리는 공통 파일 하나다
        parts = [io.open(os.path.join(PROMPTS, kind + '.txt'), encoding='utf-8').read()]
        for common in COMMON:
            parts.append(io.open(os.path.join(PROMPTS, common), encoding='utf-8').read())
        tpl = chr(10).join(p.strip(chr(10)) for p in parts) + chr(10)
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
