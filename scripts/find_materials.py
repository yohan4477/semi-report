# -*- coding: utf-8 -*-
"""주제 낱말로 코퍼스에서 보고서 재료 후보를 찾는다.

    PYTHONIOENCODING=utf-8 python scripts/find_materials.py 전력 메가와트 기가와트 전력망
    PYTHONIOENCODING=utf-8 python scripts/find_materials.py 패키징 인터포저 CoWoS EMIB --top 20
    PYTHONIOENCODING=utf-8 python scripts/find_materials.py 전력 --not 배선 --min 0.3

왜 있나 — **제목으로 훑으면 재료를 놓친다.** 2026-09-05 에 「전력」으로 재 봤더니 본문
신호가 짙은 상위 스무 편 가운데 다섯 편만 제목에 그 말이 있었다. 「데이터센터 해부학
Part 1 — 전기 시스템」도 「PJM 모델링 오류로 날린 120억 달러」도 제목으로는 안 걸린다.

`check_cover` 는 이 구멍을 못 막는다. 선언한 재료를 다 썼나만 묻지, 찾아야 할 것을 다
찾았나는 안 묻기 때문이다. 그래서 고르는 단계를 기계로 넓힌다.

**이 도구는 후보를 낼 뿐 재료를 정하지 않는다.** 넘치는 쪽으로 틀리게 만들어 두고 사람이
자른다 — 넘치는 것은 자르면 되고 놓친 것은 아무도 모른다. 총정리 편(ECTC·ISSCC)처럼
주제가 섞인 원문이 위로 올라오는 것은 정상이다. 그 편은 해당 대목만 쓰면 된다.

한 번 재 봤다 (2026-09-05)
    「전력」    상위 18편 중 13편이 제목에 그 말이 없다. 제목 훑기로는 못 찾았을 편이다
    「패키징」  사람이 손으로 고른 재료 열둘을 **12/12 되찾았고 전부 상위 18위 안**에 들었다.
               게다가 그 목록에 없던 둘을 위로 올렸다 — IEDM 2024 클리핑(차세대 SoIC·EMIB-T)과
               퀄컴 HBC 회차(연산 다이 위에 메모리를 쌓는 설계). 둘 다 주제 한복판이었다

세는 법
    신호   주제 낱말이 본문에 몇 번 나오나
    밀도   1,000자당 몇 번. 긴 글이 스쳐 지나가며 여러 번 말한 것과, 짧은 글이 그것만
           말한 것을 가른다. 순위는 밀도가 정한다
    제목   제목에도 그 말이 있나. 없는데 위에 있으면 제목 훑기로는 못 찾았을 편이다
"""
import argparse
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 보고서 층이 재료로 삼는 자리. content/understanding 은 제3자 해설이라 기본에서 뺀다
SETS = {
    '뉴스레터': ['content/newsletter/**/*.md'],
    'SemiDoped': ['insights/semidoped/*.md'],
    '클리핑': ['input/clippings/*.md'],
    '팟캐스트': ['content/podcast/**/*.md'],
    '해설': ['content/understanding/**/*.md'],
}
DEFAULT = ['뉴스레터', 'SemiDoped', '클리핑', '팟캐스트']

_DATE = re.compile(r'\[(\d{6})\]')
_FRONT = re.compile(r'^---.*?^---', re.S | re.M)


def files(sets):
    out = []
    for name in sets:
        for pat in SETS[name]:
            for p in glob.glob(os.path.join(ROOT, pat), recursive=True):
                out.append((name, p))
    return sorted(set(out))


def body(path):
    """frontmatter 를 걷은 본문. 앞머리의 태그 목록이 신호를 부풀린다."""
    t = io.open(path, encoding='utf-8', errors='ignore').read()
    return _FRONT.sub('', t, count=1)


def when(name):
    m = _DATE.search(name)
    if not m:
        m2 = re.search(r'(20\d\d)-(\d\d)-\d\d', name)
        return '%s-%s' % (m2.group(1)[2:], m2.group(2)) if m2 else '  ·  '
    return '%s-%s' % (m.group(1)[:2], m.group(1)[2:4])


def main():
    ap = argparse.ArgumentParser(description='주제 낱말로 보고서 재료 후보를 찾는다')
    ap.add_argument('words', nargs='+', help='주제 낱말. 영문 클리핑까지 보려면 영문도 같이')
    ap.add_argument('--not', dest='drop', nargs='*', default=[],
                    help='이 말이 그 편의 신호 대부분이면 후보에서 뺀다')
    ap.add_argument('--top', type=int, default=25, help='몇 편까지 보일까 (기본 25)')
    ap.add_argument('--min', type=float, default=0.15, help='이 밀도 아래는 안 보인다 (기본 0.15)')
    ap.add_argument('--set', nargs='*', default=DEFAULT, choices=list(SETS), help='어디를 볼까')
    a = ap.parse_args()

    pats = [(w, re.compile(re.escape(w), re.I)) for w in a.words]
    drops = [re.compile(re.escape(w), re.I) for w in a.drop]

    rows = []
    for kind, path in files(a.set):
        name = os.path.basename(path)
        txt = body(path)
        if not txt.strip():
            continue
        hits = {w: len(p.findall(txt)) for w, p in pats}
        n = sum(hits.values())
        if not n:
            continue
        if drops and sum(len(p.findall(txt)) for p in drops) >= n:
            continue                       # 제외어가 신호를 다 설명하면 딴 이야기다
        dens = n * 1000.0 / len(txt)
        if dens < a.min:
            continue
        in_title = any(p.search(name) for _w, p in pats)
        got = [w for w, c in hits.items() if c]
        rows.append((dens, n, kind, when(name), in_title, name, got, path))

    rows.sort(reverse=True)
    shown = rows[:a.top]
    print('주제 낱말 %s · 후보 %d편 (밀도 %.2f 이상, 상위 %d편)\n'
          % (' · '.join(a.words), len(rows), a.min, len(shown)))
    print('  밀도   신호  때      제목걸림  갈래       제목')
    for dens, n, kind, dt, in_title, name, got, _p in shown:
        print('  %5.2f  %4d  %-6s  %-8s  %-9s %s'
              % (dens, n, dt, '' if in_title else '←  못 찾음', kind, name[:58]))

    miss = [r for r in shown if not r[4]]
    print('\n제목으로 훑었으면 못 찾았을 편 %d/%d' % (len(miss), len(shown)))

    # 맞은 낱말이 하나뿐인 편은 그 낱말이 딴 뜻일 수 있다
    thin = [r for r in shown if len(r[6]) == 1]
    if thin:
        print('낱말 하나에만 걸린 편 %d — 그 말이 딴 뜻인지 본다: %s'
              % (len(thin), ' · '.join('%s(%s)' % (r[5][:22], r[6][0]) for r in thin[:5])))

    print('\n경로 (위임문에 붙일 것):')
    for _d, _n, _k, _t, _i, _name, _g, p in shown:
        print('  ' + os.path.relpath(p, ROOT).replace('\\', '/'))
    print('\n이 목록은 후보다. 재료는 사람이 자른다 — 넘치는 것은 자르면 되고 놓친 것은 안 보인다.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
