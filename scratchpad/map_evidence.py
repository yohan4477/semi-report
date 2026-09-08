# -*- coding: utf-8 -*-
"""지도 판단을 쓰기 위한 재료 — 이름마다 원문 문장을 줄 주소와 함께 뽑는다.

    py -3.13 scratchpad/map_evidence.py litho > scratchpad/_ev_litho.md

판단(insights/maps/takes/<공정>.json)은 사람이 쓴다. 이 스크립트는 그 앞의 재료만
모은다 — 문장을 고르지도 줄이지도 않는다.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

KEYS = ['litho', 'etch', 'packaging', 'memory', 'network']


def main(key, top_docs=4):
    mod = __import__('map_%s' % key)
    data = mod.scan()
    seen = set()
    out = ['# %s — 판단 재료' % mod.LABEL, '']
    for v in data['views']:
        for b in v['branches']:
            stack = []
            for nd in b['nodes']:
                stack.append(nd)
                stack.extend(nd.get('kids', []))
            for nd in stack:
                if nd['name'] in seen or not nd['n']:
                    continue
                seen.add(nd['name'])
                out.append('## %s — %d회 · %d편' % (nd['name'], nd['n'], nd['ndoc']))
                for rel, cnt, sents in nd['top'][:top_docs]:
                    for ln, s in sents:
                        out.append('- `%s:%d` %s' % (rel, ln, s.replace('\n', ' ')))
                out.append('')
    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    k = sys.argv[1] if len(sys.argv) > 1 else 'litho'
    if k not in KEYS:
        raise SystemExit('공정 이름: %s' % ', '.join(KEYS))
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main(k)
