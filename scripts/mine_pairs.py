# -*- coding: utf-8 -*-
"""영한 이름 매핑 후보를 캔다. 사전에 넣지는 않는다 — 사람이 고른다.

이 저장소는 「용어는 남기고 첫 등장에 괄호로 푼다」를 규칙으로 쓴다. 그래서 본문에
「도쿄일렉트론(TEL)」 꼴이 쌓여 있고, 그것이 곧 영한 매핑이다. 다만 같은 괄호가
학회 이름·일반 용어·종목 기호에도 쓰여서 캐낸 것을 그대로 믿으면 안 된다.
연도가 든 풀이만 기계가 걸러 내고 나머지 판단은 사람에게 넘긴다.

  py -3.13 scripts/mine_pairs.py
"""
import collections
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import entities_lib as el  # noqa: E402
import gen_index as gi  # noqa: E402
import paths  # noqa: E402
import source_lines as sl  # noqa: E402

GLOSS = re.compile(
    r'([가-힣][가-힣A-Za-z0-9]{1,15})'
    r'\s*\(\s*([A-Za-z][A-Za-z0-9&.\- ]{1,30}?)\s*\)')
YEAR = re.compile(r'(?:19|20)\d{2}')


def pairs_in(line):
    out = []
    for ko, en in GLOSS.findall(line):
        en = en.strip()
        if not en or YEAR.search(en):
            continue
        out.append((ko, en))
    return out


def mine(root, files, need):
    got = collections.Counter()
    for rel in files:
        for line in sl.lines(root, rel):
            for ko, en in pairs_in(line):
                if ko in need:
                    got[(ko, en)] += 1
    return dict(got)


def main():
    rows = el.load()
    need = set()
    for r in rows:
        if not r.get('en'):
            need.add(r['canonical'])
    got = mine(paths.ROOT, gi.corpus_files(paths.ROOT), need)
    order = sorted(got.items(), key=lambda kv: (-kv[1], kv[0]))
    covered = set()
    for ko, _ in got:
        covered.add(ko)
    print('짝 %d종 · en 없는 개체 %d종 중 %d종을 덮는다'
          % (len(got), len(need), len(covered)))
    print()
    for (ko, en), n in order:
        print('%-16s %-30s %d' % (ko, en, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
