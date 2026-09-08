# -*- coding: utf-8 -*-
"""지도 판단 — 이름마다 붙인 한 줄이 원문에 서 있나.

AI 인프라 지도는 원래 색인이었다. 이름을 세고 가지를 쳤을 뿐이라, 읽는 사람이 얻는 게
「무엇이 몇 번 나왔나」뿐이었다(2026-09-09). 이름마다 판단 한 줄을 붙여 색인을 지도로
올리는데, 그 한 줄은 손으로 쓰는 것이라 값을 지어낼 수 있다 — 도해와 같은 자리다.

판단은 insights/maps/takes/<공정>.json 에 이름별로 적는다:

    {"EUV": {"take": "…한 줄", "cite": ["content/…md:34"], "asof": "2026-08"}}

  M1 이름이 그 공정의 NAMES 사전에 있나 (사전에 없는 말은 만들지 않는다)
  M2 한 줄인가 — 70자 이하, 줄바꿈 없음
  M3 cite 가 가리키는 파일과 줄이 실재하나
  M4 판단에 든 수가 cite 한 줄에 있나 (check_cite 와 같은 대조)
  M5 원문이 없는 이름(0회)에는 판단을 달지 않는다

빚은 공정별로 센다 — 판단이 아직 없는 이름 수. FAIL 이 아니다.

  PYTHONIOENCODING=utf-8 python insights/check_maptake.py
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scratchpad'))
TAKES = os.path.join(ROOT, 'insights', 'maps', 'takes')
PROCS = ['litho', 'etch', 'packaging', 'memory', 'network']
MAXLEN = 70


def digits(s):
    """값으로 볼 수 있는 수만 — 쉼표를 걷고, 연도 네 자리와 한 자리는 뺀다"""
    out = []
    for m in re.finditer(r'\d[\d,]*\.?\d*', s.replace(',', '')):
        t = m.group(0)
        if len(t.rstrip('.')) < 2:
            continue
        if re.match(r'^(19|20)\d\d$', t):
            continue
        out.append(t.rstrip('.'))
    return out


def load_proc(key):
    mod = __import__('map_%s' % key)
    data = mod.scan()
    counts = {}

    def walk(nodes):
        for nd in nodes:
            counts[nd['name']] = nd['n']
            walk(nd.get('kids', []))
    for v in data['views']:
        for b in v['branches']:
            walk(b['nodes'])
    return mod, counts


def line_of(rel, no):
    path = os.path.join(ROOT, rel.replace('/', os.sep))
    if not os.path.isfile(path):
        return None
    lines = io.open(path, encoding='utf-8', errors='replace').read().split('\n')
    if not (1 <= no <= len(lines)):
        return ''
    return lines[no - 1]


def main():
    fails, debt, n_take = [], [], 0
    for key in PROCS:
        mod, counts = load_proc(key)
        path = os.path.join(TAKES, '%s.json' % key)
        takes = {}
        if os.path.isfile(path):
            takes = json.loads(io.open(path, encoding='utf-8').read())
        for name, t in takes.items():
            take = (t.get('take') or '').strip()
            cites = t.get('cite') or []
            if name not in mod.NAMES:
                fails.append('M1 %s 「%s」가 NAMES 사전에 없다' % (key, name))
                continue
            if not take:
                fails.append('M2 %s 「%s」의 판단이 비었다' % (key, name))
                continue
            n_take += 1
            if '\n' in take or len(take) > MAXLEN:
                fails.append('M2 %s 「%s」 %d자 — %d자 넘거나 여러 줄이다'
                             % (key, name, len(take), MAXLEN))
            if counts.get(name, 0) == 0:
                fails.append('M5 %s 「%s」는 원문에 0회인데 판단이 붙었다' % (key, name))
            hay = ''
            for c in cites:
                rel, _, no = c.rpartition(':')
                if not no.isdigit():
                    fails.append('M3 %s 「%s」 인용 꼴이 아니다: %s' % (key, name, c))
                    continue
                got = line_of(rel, int(no))
                if got is None:
                    fails.append('M3 %s 「%s」 파일이 없다: %s' % (key, name, rel))
                    continue
                if got == '':
                    fails.append('M3 %s 「%s」 줄이 파일 밖이다: %s' % (key, name, c))
                    continue
                hay += ' ' + got
            miss = [d for d in digits(take) if d not in digits(hay)]
            if miss:
                fails.append('M4 %s 「%s」 인용 줄에 없는 수 %s'
                             % (key, name, ', '.join(miss)))
        live = [n for n, c in counts.items() if c > 0]
        todo = [n for n in live if n not in takes]
        if todo:
            debt.append('%-10s 판단 %3d / 이름 %3d — 남은 %d'
                        % (key, len(live) - len(todo), len(live), len(todo)))
    for f in fails:
        print('FAIL ' + f)
    for d in debt:
        print('빚   ' + d)
    print('요약: 판단 %d줄 / FAIL %d / 빚 %d공정' % (n_take, len(fails), len(debt)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
