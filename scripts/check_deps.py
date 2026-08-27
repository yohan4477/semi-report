# -*- coding: utf-8 -*-
"""의존 검사 — 추적된 코드가 부르는데 추적이 안 된 파일이 있나.

이 저장소는 .gitignore 1행이 scratchpad/ 를 통째로 무시하면서 그 안의 생성기
백여 개를 강제로 추적한다. 그래서 추적된 파일이 추적 안 된 파일을 import 하는 일이
조용히 생긴다 — 이 작업 폴더에서는 잘 돌고, 새 클론과 워크트리에서만 죽는다.

2026-08-27 에 실제로 그랬다. gen_report_dashboard.py 는 추적되는데 그것이 부르는
_biz_part1~4 와 _biz_fig 는 아니어서, 워크트리에서 build_all.py 가 멈췄다. git status
에도 안 뜬다(무시 대상이라). 그런 것은 사람이 알아채기 어렵다.

  py -3.13 scripts/check_deps.py
"""
import io
import os
import re
import subprocess
import sys

# 저장소 안 모듈이 사는 곳. 여기 없는 이름은 표준·외부 라이브러리로 본다
DIRS = ('scratchpad', 'scripts', 'insights')
# 줄 첫머리(들여쓰기 허용)의 import 만 본다. 주석 뒤의 것은 코드가 아니다
IMP = re.compile(r'^[ \t]*(?:import|from)[ \t]+([A-Za-z_]\w*)', re.M)


def tracked(root):
    r = subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True,
                       text=True, encoding='utf-8', errors='replace')
    return {p.replace('/', os.sep) for p in (r.stdout or '').split('\n') if p}


def imports_of(root, rel):
    try:
        with io.open(os.path.join(root, rel), encoding='utf-8', errors='replace') as f:
            return IMP.findall(f.read())
    except OSError:
        return []


def where(root, mod):
    """모듈 이름이 이 저장소 안 어느 파일인가. 아니면 None."""
    for d in DIRS:
        rel = os.path.join(d, mod + '.py')
        if os.path.isfile(os.path.join(root, rel)):
            return rel
    return None


def untracked_deps(root, tracked_set, dirs=DIRS):
    """추적된 .py 에서 출발해 import 를 따라가며 추적 안 된 파일을 모은다.

    추적된 것에서 닿지 않는 파일은 안 본다 — scratchpad 의 일회용 스크립트가
    무엇을 부르든 그것은 아무도 안 쓰는 코드라 저장소가 책임질 것이 아니다.
    """
    found, seen = {}, set()
    queue = [p for p in sorted(tracked_set)
             if p.endswith('.py') and p.split(os.sep)[0] in dirs]
    while queue:
        rel = queue.pop()
        if rel in seen:
            continue
        seen.add(rel)
        for mod in imports_of(root, rel):
            dep = where(root, mod)
            if dep is None or dep == rel or dep in tracked_set:
                continue
            found.setdefault(dep, set()).add(rel)
            queue.append(dep)
    return {dep: sorted(callers) for dep, callers in sorted(found.items())}


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tr = tracked(root)
    bad = untracked_deps(root, tr)
    n = len([p for p in tr if p.endswith('.py') and p.split(os.sep)[0] in DIRS])
    for dep in bad:
        print('FAIL D1 %s 가 추적이 안 됐는데 %s 가 부른다'
              % (dep, ', '.join(bad[dep])))
        print('        고치려면: git add -f %s' % dep.replace(os.sep, '/'))
    print('요약: 추적된 .py %d개 / FAIL %d' % (n, len(bad)))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
