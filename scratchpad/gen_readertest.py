# -*- coding: utf-8 -*-
"""독자 시험지를 만든다 — 이 글만 읽고 답할 수 있나 재는 자리.

인용 표시를 걷고, 표와 수식과 도해는 자리만 남긴다. 원문도 코드도 못 보는
에이전트에게 이 파일 하나만 준다. 답이 틀리거나 「글에 없다」가 나오는 자리가
실제로 안 읽히는 자리다.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_readertest.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scratchpad', '_readertest')
SRC = [('cluster', 'model-cluster-2026-09-09.md'),
       ('infer', 'model-infer-2026-09-09.md'),
       ('torus', 'model-torus-2026-09-10.md')]

sys.path.insert(0, os.path.join(ROOT, 'scratchpad'))
import _model_tbl as mt          # noqa: E402
import _model_eq as me           # noqa: E402
import _model_part1 as mp        # noqa: E402

_CITE = re.compile(r'\s*\(([^()]*?\bL\d+[^()]*)\)')


def _table_text(key):
    """표는 글자로 편다 — 값을 못 보면 물음에 답할 수 없다."""
    title, fn = mt.TABLES[key]
    head, body = fn()
    lines = ['[표: %s]' % title, ' | '.join(head)]
    for r in body:
        lines.append(' | '.join('(가려짐)' if c is None else c for c in r))
    return '\n'.join(lines)


def _eq_text(key):
    title, src, rows, terms, _code = me.EQ[key]
    lines = ['[수식: %s]' % title]
    for lhs, rhs, note in rows:
        t = '%s = %s' % (lhs, rhs)
        for a, b in (('<sub>', '_'), ('</sub>', ''), ('<sup>', '^'), ('</sup>', '')):
            t = t.replace(a, b)
        lines.append(t + ('  — ' + note if note else ''))
    for sym, mean in terms:
        lines.append('  %s : %s' % (sym.replace('<sub>', '_').replace('</sub>', ''), mean))
    return '\n'.join(lines)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SRC:
        txt = io.open(os.path.join(ROOT, 'insights', 'reports', fn),
                      encoding='utf-8').read()
        body = txt.split('---', 2)[2]
        out = []
        for line in body.split('\n'):
            s = line.rstrip()
            if s.startswith('[[tbl:'):
                out.append(_table_text(s[6:].rstrip(']').strip()))
            elif s.startswith('[[eq:'):
                out.append(_eq_text(s[5:].rstrip(']').strip()))
            elif s.startswith('[[fig:'):
                key = s[6:].rstrip(']').strip()
                out.append('[도해: %s]' % mp.CAPTION[key][0])
            else:
                out.append(_CITE.sub('', s).replace('[추정] ', '(추정) '))
        path = os.path.join(OUT, name + '.md')
        io.open(path, 'w', encoding='utf-8').write('\n'.join(out).strip() + '\n')
        print('썼다:', path, len('\n'.join(out)), '자')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
