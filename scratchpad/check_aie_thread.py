# -*- coding: utf-8 -*-
"""주장 흐름의 인용이 그 줄에 실제로 있나.

    PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py

왜 따로 있나 — scripts/check_jsoncite.py 는 메르 json 클리핑 전용이다(줄 번호가
파일에 없어서 순번을 세는 규약이 따로 있다). 마크다운은 줄 번호가 파일에 그대로
있으니 대조가 더 간단하고, 그래서 그물도 따로 친다.

이 검사기는 글자가 그 줄에 있나만 본다. 판정(동조·엇갈림)이 옳은지는 못 본다 —
그건 사람이 두 인용을 나란히 읽어야 할 일이다.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib


def cite_fails(rows):
    """claim 이 line 이 가리키는 줄에 없으면 메시지를 남긴다."""
    out = []
    for r in rows:
        lines = lib.md_lines(r.get('talk', ''))
        if lines is None:
            out.append('%s: 원문 없음' % r.get('id'))
            continue
        n = r.get('line', 0)
        if not isinstance(n, int) or n < 1 or n > len(lines):
            out.append('%s: 줄 번호가 파일 밖이다 — %r (전체 %d줄)' % (r.get('id'), n, len(lines)))
            continue
        src = lines[n - 1]
        if not src.strip():
            out.append('%s: 빈 줄을 가리킨다 — %d' % (r.get('id'), n))
        elif r.get('claim', '') not in src:
            out.append('%s: 그 줄에 없는 인용 — %d\n    원문: %s\n    인용: %s'
                       % (r.get('id'), n, src.strip()[:90], r.get('claim', '')[:90]))
    return out


def main():
    rows = lib.load()
    bad = lib.validate(rows) + cite_fails(rows)
    print('주장 %d줄 · 고립 %.0f%%' % (len(rows), lib.orphan_ratio(rows) * 100))
    for m in bad:
        print('FAIL ·', m)
    print('FAIL %d' % len(bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
