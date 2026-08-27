# -*- coding: utf-8 -*-
"""사전 씨앗 — 노트가 이미 적어 둔 actors 와 actor_alias.json 을 합친다.

1회성 생성기다. 한 번 돌려 entities.json 을 만든 뒤에는 사람이 손으로 고친다.
다시 돌리면 손으로 고친 것을 덮으므로, 이미 파일이 있으면 --force 를 요구한다.

  py -3.13 insights/gen_entities.py
"""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entities_lib as el  # noqa: E402
import paths  # noqa: E402

ACTORS_RE = re.compile(r'^actors:\s*\[(.*?)\]\s*$', re.M)
LATIN = re.compile(r'[A-Za-z]')
ALIAS_MAP = os.path.join(paths.HERE, 'actor_alias.json')


def actors_from_notes(notes_dir):
    out = {}
    for f in sorted(glob.glob(os.path.join(notes_dir, '*.md'))):
        with io.open(f, encoding='utf-8') as fh:
            head = fh.read(4000)
        m = ACTORS_RE.search(head)
        if not m:
            continue
        for name in m.group(1).split(','):
            name = name.strip()
            if name:
                out[name] = out.get(name, 0) + 1
    return out


def load_alias_map(path=ALIAS_MAP):
    with io.open(path, encoding='utf-8') as f:
        raw = json.load(f)
    return {k: v for k, v in raw.items() if not k.startswith('_')}


def seed(actors, alias_map):
    rows = {}
    for name in actors:
        latin = bool(LATIN.search(name))
        rows[name] = {
            'canonical': name,
            'type': '미정',
            'ko': [name],
            'en': [name] if latin else [],
            'deny': [],
        }
    for alias, canonical in alias_map.items():
        r = rows.get(canonical)
        if r is None:
            continue
        bucket = 'en' if LATIN.search(alias) else 'ko'
        if el.norm(alias) not in [el.norm(x) for x in r[bucket]]:
            r[bucket].append(alias)
    return [rows[k] for k in sorted(rows)]


def main():
    if os.path.exists(paths.ENTITIES) and '--force' not in sys.argv:
        print('entities.json 이 이미 있다. 덮으려면 --force 를 준다.')
        return 1
    actors = actors_from_notes(paths.NOTES)
    rows = seed(actors, load_alias_map())
    msgs = el.validate(rows)
    if msgs:
        for m in msgs:
            print('FAIL', m)
        return 1
    el.save(rows)
    print('개체 %d 종 · 별칭 %d 개'
          % (len(rows), sum(len(el.aliases_of(r)) for r in rows)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
