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


def main(slug, out=None, lane_path=None):
    # --lane <경로> 로 다른 판(견주기용 초안)을 읽을 수 있다
    lane = io.open(lane_path or os.path.join(ROOT, 'insights', 'semidoped', slug + '-strategy.md'), encoding='utf-8').read()
    raw = io.open(os.path.join(ROOT, 'content', 'understanding', 'Semi Doped', 'raw', slug + '.md'), encoding='utf-8').read().split('\n')
    nums = set()
    # 「(Austin 의 설명, L57)」처럼 괄호 안에 다른 말이 있어도 잡는다(2026-09-03 인터커넥트 대조에서 놓쳤다)
    for m in re.finditer(r'\(([^)]*L\d[^)]*)\)', lane):
        for part in re.findall(r'L\d+(?:~L?\d+)?', m.group(1)):
            part = part.strip().lstrip('L')
            if '~' in part:
                a, b = part.split('~'); nums.update(range(int(a.lstrip('L')), int(b.lstrip('L')) + 1))
            elif part.isdigit():
                nums.add(int(part))
    # 전사 한 줄이 문단 하나라 앞뒤 줄을 붙이면 전사의 2/3 가 된다 — 인용 줄만 낸다(--around 로 앞뒤 포함)
    want = set()
    for n in nums:
        want.update((n - 1, n, n + 1) if '--around' in sys.argv else (n,))
    lines = ['# %s — 글이 인용한 줄 %d개(앞뒤 한 줄 포함 %d줄). 줄 번호는 전사 파일의 것' % (slug, len(nums), len(want))]
    # 전사는 「Vik: …」 라벨이 한 번 붙고 뒤 문단은 라벨 없이 이어진다 — 인용 줄만 보면 화자가 안 보여
    # 귀속을 잘못 잡는다(2026-09-03). 줄마다 가장 가까운 앞 라벨을 [화자 …←L줄] 로 붙인다
    label_re = re.compile(r'^([A-Z][A-Za-z .]{0,24}?):\s')
    for n in sorted(want):
        if 1 <= n <= len(raw) and raw[n - 1].strip():
            mark = '*' if n in nums else ' '
            who = ''
            for k in range(n, 0, -1):
                mm = label_re.match(raw[k - 1])
                if mm:
                    who = '[화자 %s ←L%d] ' % (mm.group(1), k) if k != n else ''
                    break
            lines.append('%sL%d: %s%s' % (mark, n, who, raw[n - 1].strip()))
    out = out or os.path.join(ROOT, '_workspace', 'cited', slug + '.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    text = '\n'.join(lines) + '\n'
    io.open(out, 'w', encoding='utf-8', newline='\n').write(text)
    print(out, '— 인용 줄 %d, 낸 줄 %d, %d자 (전사 %d자)' % (len(nums), len(lines) - 1, len(text), len('\n'.join(raw))))


if __name__ == '__main__':
    lane_path = sys.argv[sys.argv.index('--lane') + 1] if '--lane' in sys.argv else None
    args = [x for x in sys.argv[1:] if not x.startswith('--') and x != lane_path]
    main(args[0], args[1] if len(args) > 1 else None, lane_path)
