# -*- coding: utf-8 -*-
"""글이 인용한 전사 줄만 뽑는다 — 대조 에이전트에 전사 전문(3~4만 토큰) 대신 이것을 보낸다.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/cited_lines.py <slug> [<출력 파일>]

insights/semidoped/<slug>-strategy.md 의 (L줄) 표기를 모두 모아, content/understanding/Semi Doped/raw/<slug>.md
의 그 줄과 앞뒤 한 줄을 줄 번호와 함께 낸다. 출력 파일을 안 주면 _workspace/cited/<slug>.md 에 쓴다.
비용 — 인용 40~60줄이면 전사의 1/5 안팎이다(2026-09-03).
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(slug, out=None):
    lane = io.open(os.path.join(ROOT, 'insights', 'semidoped', slug + '-strategy.md'), encoding='utf-8').read()
    raw = io.open(os.path.join(ROOT, 'content', 'understanding', 'Semi Doped', 'raw', slug + '.md'), encoding='utf-8').read().split('\n')
    nums = set()
    for m in re.finditer(r'\(L([^)]*)\)', lane):
        for part in re.split(r'[·,]', m.group(1)):
            part = part.strip().lstrip('L')
            if '~' in part:
                a, b = part.split('~'); nums.update(range(int(a.lstrip('L')), int(b.lstrip('L')) + 1))
            elif part.isdigit():
                nums.add(int(part))
    want = set()
    for n in nums:
        want.update((n - 1, n, n + 1))
    lines = ['# %s — 글이 인용한 줄 %d개(앞뒤 한 줄 포함 %d줄). 줄 번호는 전사 파일의 것' % (slug, len(nums), len(want))]
    for n in sorted(want):
        if 1 <= n <= len(raw) and raw[n - 1].strip():
            mark = '*' if n in nums else ' '
            lines.append('%sL%d: %s' % (mark, n, raw[n - 1].strip()))
    out = out or os.path.join(ROOT, '_workspace', 'cited', slug + '.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    text = '\n'.join(lines) + '\n'
    io.open(out, 'w', encoding='utf-8', newline='\n').write(text)
    print(out, '— 인용 줄 %d, 낸 줄 %d, %d자 (전사 %d자)' % (len(nums), len(lines) - 1, len(text), len('\n'.join(raw))))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
