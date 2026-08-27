# -*- coding: utf-8 -*-
"""색인 검사 — 주소가 맞나, 그리고 색인이 낡지 않았나.

  X1  코퍼스 지문이 색인의 것과 다르다 — 조용한 실패
  X2  entities.json 이 스스로 어긋난다
  X3  색인 주소가 가리키는 파일이 없다
  X4  주소의 줄 번호가 파일 범위 밖이다
  X5  노트 actors 에 있는 이름이 사전에 없다 (WARN)
  X6  times.json 의 가리키는 때가 있을 수 없는 값이다
  X7  times.json 의 주소가 index.json 에 없다
  X8  times.json 이 index.json 보다 낡았다
  X9  색인이 읽을 줄 모르는 갈래의 파일이 코퍼스 자리에 있다 (WARN)

X1 이 첫째다. 나머지 넷은 틀린 주소를 잡지만 X1 만이 없는 자료를 잡는다.
새 원문이 들어왔는데 색인을 안 돌리면 조회가 에러 없이 그럴듯한 답을 낸다.

  py -3.13 insights/check_index.py
"""
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entities_lib as el  # noqa: E402
import gen_entities as ge  # noqa: E402
import gen_index as gi  # noqa: E402
import paths  # noqa: E402
import source_lines as sl  # noqa: E402
import times  # noqa: E402
import utterance as ut  # noqa: E402


def check(root, rows, idx, actors, tmap=None, meta=None):
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
                counts[rel] = sl.count(root, rel)
            if not num.isdigit() or int(num) < 1 or int(num) > counts[rel]:
                out.append(('FAIL', 'X4',
                            '%s 의 줄 번호가 범위 밖이다: %s (파일 %d 줄)'
                            % (name, addr, counts[rel])))

    if tmap:
        fp_idx = (idx.get('_meta') or {}).get('fingerprint', '')
        fp_tm = (tmap.get('_meta') or {}).get('index_fingerprint', '')
        if fp_idx != fp_tm:
            out.append(('FAIL', 'X8',
                        '색인이 바뀐 뒤 때를 다시 안 만들었다. '
                        'insights/gen_times.py 를 다시 돌린다'))
        known_addrs = set()
        for name, addrs in idx.items():
            if name != '_meta':
                known_addrs.update(addrs)
        meta = meta or {}
        for addr in sorted(tmap):
            if addr == '_meta':
                continue
            if addr not in known_addrs:
                out.append(('FAIL', 'X7', '색인에 없는 주소에 때가 붙어 있다: %s' % addr))
                continue
            rel = addr.rpartition('#L')[0]
            utter = ut.date_of(meta, rel)
            uy = int(utter[:4]) if utter[:4].isdigit() else 0
            t = str(tmap[addr].get('t') or '')
            if not t.isdigit():
                out.append(('FAIL', 'X6', '%s 의 t 가 숫자가 아니다: %r' % (addr, t)))
                continue
            t = int(t)
            if t < times.LOW or (uy and t > uy + times.AHEAD):
                out.append(('FAIL', 'X6',
                            '%s 의 가리키는 때가 있을 수 없다: %d (쓴 날 %s)'
                            % (addr, t, utter or '모름')))

    # X9 — 코퍼스 자리에 있는데 색인이 못 읽는 갈래. FAIL 이 아닌 까닭은
    # input/clippings 아래에 이미지나 메모가 섞여 드는 것이 정상이기 때문이다.
    # 그래도 조용히 넘기지는 않는다 — 색인이 안 보는 원문이 는다는 신호다.
    unread = set()
    for parts in gi.CORPUS:
        # 무늬의 끝(*.md)을 *로 바꿔 그 자리의 파일을 전부 본다. 확장자 무늬
        # 그대로 훑으면 못 읽는 갈래는 애초에 안 걸려 검사가 아무것도 못 잡는다
        wild = tuple(parts[:-1]) + ('*',)
        for q in glob.glob(os.path.join(root, *wild), recursive=True):
            if not os.path.isfile(q):
                continue
            rel = os.path.relpath(q, root).replace(os.sep, '/')
            if not sl.known(rel):
                unread.add(rel)
    for rel in sorted(unread):
        out.append(('WARN', 'X9', '색인이 못 읽는 갈래다: %s' % rel))

    known = set(el.alias_index(rows).values())
    for a in sorted(actors - known):
        out.append(('WARN', 'X5', '노트 actors 의 %s 가 사전에 없다' % a))
    return out


def main():
    rows = el.load()
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    actors = set(ge.actors_from_notes(paths.NOTES))
    tmap = None
    if os.path.exists(paths.TIMES):
        with io.open(paths.TIMES, encoding='utf-8') as f:
            tmap = json.load(f)
    meta = ut.load(paths.ROOT)
    out = check(paths.ROOT, rows, idx, actors, tmap, meta)
    for lvl, rule, msg in out:
        print('%s %s %s' % (lvl, rule, msg))
    fails = sum(1 for lvl, _, _ in out if lvl == 'FAIL')
    warns = len(out) - fails
    print('FAIL %d · WARN %d' % (fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
