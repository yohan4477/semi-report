# -*- coding: utf-8 -*-
"""문단째 다시 쓴 본문을 글에 넣는다 — 한글패치 두 번째 판.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/rewrite_apply.py <run_id>

_workspace/<run_id>/ 의 01_input.txt(전)·final.md(후)·slug.txt 를 읽는다. 게이트는 humanize_gate 와 같되
문단 앞머리와 인용 문구는 바뀌어도 된다(문단째 다시 쓰기라서). 줄 표기·숫자·절 제목·①②③·문단 수가 하나라도
다르면 넣지 않는다. 통과하면 rekey_figs 로 도해 열쇠를 새 앞머리에 옮기고 본문을 글에 넣는다.
frontmatter 에 `rewritten:` 한 줄. 전사 대조는 따로 돈다(이 스크립트는 사실을 못 본다).
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def paras(s):
    return [' '.join(p.split()) for p in re.split(r'\n\s*\n', s.strip()) if p.strip() and not p.strip().startswith('#')]


def main(rid):
    d = os.path.join(ROOT, '_workspace', rid)
    slug = io.open(os.path.join(d, 'slug.txt'), encoding='utf-8').read().strip()
    A = io.open(os.path.join(d, '01_input.txt'), encoding='utf-8').read().strip()
    B = re.split(r'<!--\s*HUMANIZE[- ]SUMMARY', io.open(os.path.join(d, 'final.md'), encoding='utf-8').read())[0].strip()
    B = re.sub(r'^---.*?---\s*', '', B, flags=re.S)  # 에이전트가 frontmatter 를 붙였으면 걷는다
    fails = []

    def same(name, fa, fb):
        if fa != fb:
            fails.append(name)
            print('FAIL %s — 전에만 %s / 후에만 %s' % (name, sorted(set(fa) - set(fb))[:6], sorted(set(fb) - set(fa))[:6]))
        else:
            print('ok   %s (%d)' % (name, len(fa)))

    same('줄 표기 (L..)', sorted(re.findall(r'\(L[^)]*\)', A)), sorted(re.findall(r'\(L[^)]*\)', B)))
    same('숫자', sorted(re.findall(r'\d[\d,.~%]*', A)), sorted(re.findall(r'\d[\d,.~%]*', B)))
    same('절 제목', re.findall(r'^## .*$', A, re.M), re.findall(r'^## .*$', B, re.M))
    same('①②③', re.findall('[①-⑩]', A), re.findall('[①-⑩]', B))
    pa, pb = paras(A), paras(B)
    if len(pa) != len(pb):
        fails.append('문단 수'); print('FAIL 문단 수 %d → %d' % (len(pa), len(pb)))
    else:
        print('ok   문단 %d' % len(pa))
    nq_a, nq_b = len(re.findall(r'"[^"\n]+"', A)), len(re.findall(r'"[^"\n]+"', B))
    if nq_a != nq_b:
        print('WARN 따옴표 인용 수 %d → %d (문구는 바뀌어도 되지만 수는 같아야 한다)' % (nq_a, nq_b))
        fails.append('인용 수')
    n = len(re.sub(r'\(L[^)]*\)', '', B))
    print('글자 %d → %d' % (len(re.sub(r'\(L[^)]*\)', '', A)), n))
    if fails:
        print('넣지 않음 —', ', '.join(fails)); return 1
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'scratchpad', 'rekey_figs.py'), slug,
                        os.path.join(d, '01_input.txt'), os.path.join(d, 'final.md')],
                       capture_output=True, env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    print(r.stdout.decode('utf-8', 'replace').strip())
    if r.returncode != 0:
        print('넣지 않음 — 도해 열쇠'); return 1
    p = os.path.join(ROOT, 'insights', 'semidoped', slug + '-strategy.md')
    s = io.open(p, encoding='utf-8').read()
    fm = s.split('---', 2)[1]
    note = 'rewritten: 2026-09-03 문단째 한국어로 다시 씀(sonnet, 본보기 Grok 편) run %s — 문단 %d · (L) %d · 전사 대조는 따로' % (rid, len(pb), len(re.findall(r'\(L', B)))
    if not re.search(r'^rewritten:', fm, re.M):
        fm = fm.replace('\ntitle:', '\n' + note + '\ntitle:', 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write('---' + fm + '---\n\n' + B + '\n')
    print('넣음', slug)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
