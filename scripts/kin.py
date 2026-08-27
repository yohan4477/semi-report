# -*- coding: utf-8 -*-
"""닮은 카드 — 「이것과 관련된 게 또 뭐가 있나」의 후보군과 분모.

related 는 손으로 적는다. 그래서 적어 둔 만큼만 나온다. 이 도구는 그 분모를 준다 —
「후보 열둘인데 셋만 적혀 있다」가 보이면 나머지 아홉을 볼지 말지 정할 수 있다.

읽기 전용이다. related 를 고치지 않는다. 무엇이 이미 적혀 있는지 칸으로 보여줄 뿐이다.

  py -3.13 scripts/kin.py "카드 제목"
  py -3.13 scripts/kin.py "카드 제목" --top 20
  py -3.13 scripts/kin.py "카드 제목" --in gen_health_dashboard
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import axis_lib as al  # noqa: E402
import kin_lib as kl  # noqa: E402

TOP = 12


def all_cards(root, only=None):
    """모듈 하나로 좁히면 그 대시보드 안에서만 이웃을 찾는다. 기본은 전부."""
    out = []
    for m, _ in al.card_modules(root):
        if only and m != only:
            continue
        for c in al.load_cards(root, m):
            out.append((m, c))
    return out


def render(res, where):
    mark = lambda b: '○' if b else '·'  # noqa: E731
    out = ['%s · %s · %s' % (res['title'], where.get(res['title'], '?'),
                             res['section'] or '(섹션 없음)'), '']
    if not res['rows']:
        out.append('  닮은 카드가 없다. 이 글이 쓰는 말을 다른 카드가 안 쓴다')
        return '\n'.join(out)

    out.append('  닮은 카드 %d장 · related 에 적힌 것 %d장 중 %d장이 여기 있다'
               % (res['shown'], res['declared'], res['declared_in_top']))
    out.append('')
    out.append('  점수   같은섹션  related  제목')
    for r in res['rows']:
        out.append('  %.3f     %s        %s      %s'
                   % (r['score'], mark(r['same_section']), mark(r['in_related']),
                      r['title']))
    if res['declared_missing']:
        out.append('')
        out.append('  점수가 못 찾았는데 사람이 이어 둔 것 — 낱말이 아니라 논리로 이어진 글이다')
        for t in res['declared_missing']:
            out.append('    %s' % t)
    return '\n'.join(out)


def main(argv):
    if len(argv) < 2:
        print('쓰기: py -3.13 scripts/kin.py "카드 제목" [--top N] [--in 생성기]')
        return 1

    title = argv[1]
    only = None
    if '--in' in argv:
        at = argv.index('--in') + 1
        if at >= len(argv):
            print('--in 뒤에 생성기 이름이 있어야 한다')
            return 1
        only = argv[at]
        known = [m for m, _ in al.card_modules(ROOT)]
        if only not in known:
            print('그런 생성기가 없다: %s' % only)
            print('모듈:', ', '.join(known))
            return 1

    top = TOP
    if '--top' in argv:
        at = argv.index('--top') + 1
        if at >= len(argv) or not argv[at].isdigit():
            print('--top 뒤에 숫자가 있어야 한다')
            return 1
        top = int(argv[at])

    pairs = all_cards(ROOT, only)
    cards = [c for _, c in pairs]
    where = {al.card_id(c): m for m, c in pairs}

    if title not in where:
        print('그런 제목의 카드가 없다: %s' % title)
        near = sorted(t for t in where if title in t or t in title)
        if near:
            print('비슷한 제목:')
            for t in near[:8]:
                print('  %s' % t)
        return 1

    print(render(kl.neighbors(cards, title, top), where))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
