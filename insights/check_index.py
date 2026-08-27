# -*- coding: utf-8 -*-
"""색인 검사 — 주소가 맞나, 그리고 색인이 낡지 않았나.

  X1  코퍼스 지문이 색인의 것과 다르다 — 조용한 실패
  X2  entities.json 이 스스로 어긋난다
  X3  색인 주소가 가리키는 파일이 없다
  X4  주소의 줄 번호가 파일 범위 밖이다
  X5  노트 actors 에 있는 이름이 사전에 없다 (WARN)

X1 이 첫째다. 나머지 넷은 틀린 주소를 잡지만 X1 만이 없는 자료를 잡는다.
새 원문이 들어왔는데 색인을 안 돌리면 조회가 에러 없이 그럴듯한 답을 낸다.

  py -3.13 insights/check_index.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entities_lib as el  # noqa: E402
import gen_entities as ge  # noqa: E402
import gen_index as gi  # noqa: E402
import paths  # noqa: E402


def _line_count(path):
    with io.open(path, encoding='utf-8', errors='replace') as f:
        return sum(1 for _ in f)


def check(root, rows, idx, actors):
    out = []
    files = gi.corpus_files(root)
    now = gi.fingerprint(root, files)
    was = (idx.get('_meta') or {}).get('fingerprint')
    if now != was:
        out.append(('FAIL', 'X1',
                    '코퍼스가 색인 이후에 바뀌었다. insights/gen_index.py 를 다시 돌린다'))
    for m in el.validate(rows):
        out.append(('FAIL', 'X2', m))

    counts = {}
    for name, addrs in sorted(idx.items()):
        if name == '_meta':
            continue
        for addr in addrs:
            rel, _, num = addr.rpartition('#L')
            full = os.path.join(root, rel.replace('/', os.sep))
            if not os.path.isfile(full):
                out.append(('FAIL', 'X3', '%s 가 없는 파일을 가리킨다: %s' % (name, addr)))
                continue
            if rel not in counts:
                counts[rel] = _line_count(full)
            if not num.isdigit() or int(num) < 1 or int(num) > counts[rel]:
                out.append(('FAIL', 'X4',
                            '%s 의 줄 번호가 범위 밖이다: %s (파일 %d 줄)'
                            % (name, addr, counts[rel])))

    known = set(el.alias_index(rows).values())
    for a in sorted(actors - known):
        out.append(('WARN', 'X5', '노트 actors 의 %s 가 사전에 없다' % a))
    return out


def main():
    rows = el.load()
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    actors = set(ge.actors_from_notes(paths.NOTES))
    out = check(paths.ROOT, rows, idx, actors)
    for lvl, rule, msg in out:
        print('%s %s %s' % (lvl, rule, msg))
    fails = sum(1 for lvl, _, _ in out if lvl == 'FAIL')
    warns = len(out) - fails
    print('FAIL %d · WARN %d' % (fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
