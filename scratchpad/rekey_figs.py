# -*- coding: utf-8 -*-
"""도해 열쇠(「절.|문단 앞머리」)를 새 본문의 문단 앞머리로 옮긴다 — 윤문이 문단 머리를 바꿨을 때.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/rekey_figs.py <slug> <옛 본문> <새 본문>

문단 수와 순서가 같아야 한다(윤문 규칙). 옛 본문에서 열쇠가 가리키는 문단의 차례를 찾고, 새 본문의
같은 차례 문단 첫 여덟 글자(겹치면 더 길게)로 semidoped_figs.py 의 열쇠를 바꿔 쓴다.
생성기는 ' '.join(para.split()) 한 문단 글이 열쇠 앞머리로 시작하는지를 본다(gen_semidoped 233줄).
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGS_PY = os.path.join(ROOT, 'scratchpad', 'semidoped_figs.py')


def paras(text):
    body = re.split(r'<!--\s*HUMANIZE[- ]SUMMARY', text)[0]
    out = []
    for p in re.split(r'\n\s*\n', body.strip()):
        t = ' '.join(p.split())
        if t and not t.startswith('#'):
            out.append(t)
    return out


def main(slug, old_path, new_path):
    old, new = paras(io.open(old_path, encoding='utf-8').read()), paras(io.open(new_path, encoding='utf-8').read())
    if len(old) != len(new):
        print('FAIL 문단 수가 다르다: %d → %d — 열쇠를 옮길 수 없다' % (len(old), len(new)))
        return 1
    src = io.open(FIGS_PY, encoding='utf-8').read()
    sys.path.insert(0, os.path.dirname(FIGS_PY))
    import semidoped_figs
    figs = semidoped_figs.FIGS.get((slug, 'strategy'), [])
    changed, n = src, 0
    for key, title, _svg, _cap in figs:
        if '|' not in key:
            continue
        sec, prefix = key.split('|', 1)
        idx = [i for i, t in enumerate(old) if t.startswith(prefix)]
        if len(idx) != 1:
            print('FAIL 옛 본문에서 열쇠 「%s」가 문단 %d개에 맞는다' % (key, len(idx)))
            return 1
        i = idx[0]
        if new[i].startswith(prefix):
            continue  # 머리가 안 바뀌었다
        L = 8
        while L <= 24:
            cand = new[i][:L]
            if sum(1 for t in new if t.startswith(cand)) == 1:
                break
            L += 2
        newkey = sec + '|' + cand
        a, b = "('%s', '%s'" % (key, title), "('%s', '%s'" % (newkey, title)
        if changed.count(a) != 1:
            print('FAIL semidoped_figs.py 에서 「%s」를 한 번 못 찾았다(%d)' % (a, changed.count(a)))
            return 1
        changed = changed.replace(a, b)
        n += 1
        print('  %s  →  %s   (「%s」)' % (key, newkey, title))
    if n:
        io.open(FIGS_PY, 'w', encoding='utf-8', newline='\n').write(changed)
    print('%s — 열쇠 %d개 옮김 / 도해 %d장' % (slug, n, len(figs)))
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:4]))
