# -*- coding: utf-8 -*-
"""윤문본을 글에 넣는다 — 게이트를 통과한 run 만.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/humanize_apply.py <run_id> [<run_id> ...]

run 폴더(_workspace/<run_id>/)의 slug.txt 로 글을 찾고, humanize_gate 가 FAIL 없이 통과하면
final.md 본문(요약 블록 걷고)을 insights/semidoped/<slug>-strategy.md 의 frontmatter 아래에 넣는다.
frontmatter 에 `humanized:` 한 줄을 남긴다(있으면 덧붙인다).
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def apply(rid):
    d = os.path.join(ROOT, '_workspace', rid)
    slug = io.open(os.path.join(d, 'slug.txt'), encoding='utf-8').read().strip()
    a, b = os.path.join(d, '01_input.txt'), os.path.join(d, 'final.md')
    if not os.path.exists(b):
        print(rid, slug, '— final.md 없음'); return False
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'scratchpad', 'humanize_gate.py'), a, b],
                       capture_output=True, env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    out = r.stdout.decode('utf-8', 'replace')
    rate = re.search(r'변경률 ([\d.]+)%', out)
    if r.returncode != 0:
        print(rid, slug, '— 게이트 FAIL\n' + out); return False
    B = re.split(r'<!--\s*HUMANIZE[- ]SUMMARY', io.open(b, encoding='utf-8').read())[0].strip()
    p = os.path.join(ROOT, 'insights', 'semidoped', slug + '-strategy.md')
    s = io.open(p, encoding='utf-8').read()
    fm = s.split('---', 2)[1]
    note = 'humanize-korean 윤문 한 콜(sonnet) run %s — 변경률 %s%%' % (rid, rate.group(1) if rate else '?')
    if re.search(r'^humanized:', fm, re.M):
        fm = re.sub(r'^(humanized:.*)$', lambda m: m.group(1) + ' · ' + note, fm, count=1, flags=re.M)
    else:
        fm = fm.replace('\ntitle:', '\nhumanized: ' + note + '\ntitle:', 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('---' + fm + '---\n\n' + B + '\n')
    freq = re.findall(r'  (것이다|대시 —|는 것)\s+([\d.]+) → ([\d.]+)', out)
    print(rid, slug, '— 넣음, 변경률 %s%%' % (rate.group(1) if rate else '?'), ' '.join('%s %s→%s' % f for f in freq))
    return True


if __name__ == '__main__':
    ok = all([apply(r) for r in sys.argv[1:]])
    sys.exit(0 if ok else 1)
