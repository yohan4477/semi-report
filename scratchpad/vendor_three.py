# -*- coding: utf-8 -*-
"""three.js 를 사이트에 같이 올린다 — 외부 CDN 이 막히거나 느린 곳에서도 3D 분해도가 뜨게.

three@0.160.0 의 빌드와, 분해도가 부르는 addons 가 다시 부르는 파일까지 따라가며 받아
대시보드/model/vendor/three/ 아래에 CDN 과 같은 경로로 둔다. 한 번 돌리면 되고, 판을 올릴 때만 다시 돌린다.

    PYTHONIOENCODING=utf-8 python scratchpad/vendor_three.py
"""
import io
import os
import re
import sys
import urllib.request

VER = '0.160.0'
CDN = 'https://cdn.jsdelivr.net/npm/three@%s/' % VER
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', 'model', 'vendor', 'three')

START = ['build/three.module.js'] + ['examples/jsm/' + p for p in (
    'controls/OrbitControls.js', 'geometries/RoundedBoxGeometry.js', 'environments/RoomEnvironment.js',
    'postprocessing/EffectComposer.js', 'postprocessing/RenderPass.js', 'postprocessing/OutlinePass.js',
    'postprocessing/OutputPass.js', 'postprocessing/GTAOPass.js', 'renderers/CSS2DRenderer.js')]

IMPORT = re.compile(r"""(?:import|export)[^'"]*?from\s*['"]([^'"]+)['"]|import\s*['"]([^'"]+)['"]""")


def fetch(rel):
    with urllib.request.urlopen(CDN + rel, timeout=60) as r:
        return r.read().decode('utf-8')


def main():
    seen, todo = set(), list(START)
    while todo:
        rel = todo.pop()
        if rel in seen:
            continue
        seen.add(rel)
        src = fetch(rel)
        path = os.path.join(OUT, *rel.split('/'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, 'w', encoding='utf-8', newline='\n').write(src)
        for m in IMPORT.finditer(src):
            spec = m.group(1) or m.group(2)
            if spec.startswith('.'):
                base = rel.rsplit('/', 1)[0]
                parts = (base + '/' + spec).split('/')
                stack = []
                for part in parts:
                    if part == '..':
                        stack.pop()
                    elif part and part != '.':
                        stack.append(part)
                todo.append('/'.join(stack))
    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
    print('받음 %d개 · %.0fKB -> %s' % (len(seen), total / 1024, OUT))
    for r in sorted(seen):
        print('  ', r)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
