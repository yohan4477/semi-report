# -*- coding: utf-8 -*-
"""손으로 유지되는 장에 「링크 복사」를 박아 둔다.

대시보드 대부분은 생성기가 통째로 다시 만들지만, 세 장은 그렇지 않다 — 히스토리 미러는
스킬이 날짜 블록을 하나씩 끼워 넣고, 개념 지도는 손으로 쓴 페이지이며, 소스 타임라인은
ad-hoc 스크립트가 조각을 덧댄다. 그런 장에 버튼을 HTML로 박아 두면 다음에 한 줄 넣는
사람이 같이 넣어야 하는데 그 규칙은 지켜지지 않는다. 그래서 붙이는 일을 브라우저에
맡기고(ui_bits.auto_copy), 이 스크립트는 그 조각이 페이지 끝에 있는지만 본다.

    PYTHONIOENCODING=utf-8 python scripts/stamp_links.py

여러 번 돌려도 같은 결과다 — 표시(MARK)로 끊고 다시 붙인다.
"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ui_bits  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = '<!-- ui-copy: scripts/stamp_links.py 가 붙인다. 손으로 고치지 않는다 -->'

# (파일, 자리를 고르는 선택자, 그 안의 제목, id 앞머리)
PAGES = [
    ('소셜 신호 히스토리.html', '.day', 'h3', 'day-'),
    ('개념 지도 — LLM 계층·병렬화.html', '.dpanel', 'h3', 'sec-'),
    ('소스 타임라인.html', '.sec', '.cap, .ccap', 'sec-'),
]


def stamp(name, sel, head, prefix):
    path = os.path.join(ROOT, '대시보드', name)
    html = io.open(path, encoding='utf-8').read()
    at = html.find(MARK)
    if at != -1:
        html = html[:at].rstrip() + '\n'
    block = MARK + '\n' + ui_bits.COPY_JS + ui_bits.auto_copy(sel, head, prefix)
    io.open(path, 'w', encoding='utf-8').write(html + block)
    return path


if __name__ == '__main__':
    for args in PAGES:
        print('OK: %s' % os.path.basename(stamp(*args)))
