# -*- coding: utf-8 -*-
"""조회 — 색인에서 주소를 받고 그 줄만 읽는다. 아무것도 쓰지 않는다.

답에 영수증을 붙인다. 색인을 언제 어느 지문으로 만들었는지, 몇 줄을 봤는지,
그리고 상한에 걸려 몇 줄을 안 봤는지. 마지막 것이 없으면 잘린 답과 다 본 답이
화면에서 똑같아 보인다.

  py -3.13 scripts/q.py 램리서치
  py -3.13 scripts/q.py 램리서치 --cap 100
"""
import datetime
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'insights'))
import check_fresh  # noqa: E402  신선도 표를 복제하지 않고 그대로 쓴다
import paths  # noqa: E402
import source_lines as sl  # noqa: E402
import times  # noqa: E402,F401  때 판정 규칙의 소유자를 밝힌다
import utterance as ut  # noqa: E402

CAP = 40


def stale_limit(section):
    return check_fresh.STALE_DAYS.get(section, check_fresh.DEFAULT_STALE)


def _days_between(a, b):
    """'YYYY-MM-DD' 둘 사이의 날수. 꼴이 어긋나면 0."""
    try:
        x = datetime.date(*map(int, a.split('-')))
        y = datetime.date(*map(int, b.split('-')))
    except (ValueError, TypeError):
        return 0
    return (y - x).days


def _time_of(addr, tmap, meta, today):
    """그 줄의 때·확실도·시제·낡음. tmap 에 없으면 쓴 날을 상속한다."""
    rel = addr.rpartition('#L')[0]
    utter = ut.date_of(meta, rel)
    got = (tmap or {}).get(addr)
    if got:
        t, how, tense = got.get('t', ''), got.get('how', ''), got.get('tense', '')
    elif utter[:4].isdigit():
        t, how, tense = utter[:4], '상속', '현재'
    else:
        t, how, tense = '', '상속', '현재'
    stale = False
    if tense in ('현재', '전망') and utter and today:
        age = _days_between(utter, today)
        stale = age > stale_limit(ut.section_of(meta, rel))
    return {'t': t, 'how': how, 'tense': tense, 'utter': utter, 'stale': stale}


def read_line(root, rel, num):
    return sl.line_at(root, rel, num)


def lookup(root, idx, name, cap=CAP, tmap=None, meta=None, today=None):
    addrs = idx.get(name) or []
    imeta = idx.get('_meta') or {}
    meta = meta or {}
    shown = addrs[:cap]
    rows = []
    counts = {}
    for addr in shown:
        rel, _, num = addr.rpartition('#L')
        row = {'addr': addr,
               'text': read_line(root, rel, int(num)) if num.isdigit() else ''}
        row.update(_time_of(addr, tmap, meta, today))
        counts[row['tense']] = counts.get(row['tense'], 0) + 1
        rows.append(row)
    return {
        'name': name,
        'total': len(addrs),
        'shown': len(shown),
        'cut': len(addrs) - len(shown),
        'files': len({a.rpartition('#L')[0] for a in addrs}),
        'built': imeta.get('built', ''),
        'fingerprint': imeta.get('fingerprint', ''),
        'tense_counts': counts,
        'rows': rows,
    }


def render(r):
    out = ['%s · 원문 %d편 · %d줄' % (r['name'], r['files'], r['total'])]
    for i, row in enumerate(r['rows'], 1):
        mark = ' 낡음' if row.get('stale') else ''
        out.append('  [%d] %s %s  (쓴 날 %s, %s)%s  %s'
                   % (i, row.get('tense', ''), row.get('t', '') or '—',
                      row.get('utter', '') or '모름', row.get('how', ''),
                      mark, row['addr']))
        if row['text']:
            out.append('      %s' % row['text'][:120])
    counts = r.get('tense_counts') or {}
    tense = ' · '.join('%s %d' % (k, counts[k]) for k in sorted(counts)) or '—'
    out.append('  — 영수증 — 색인 %s (%s) · 본 줄 %d · 잘림 %d · 시제 %s'
               % (r['built'], r['fingerprint'][:8], r['shown'], r['cut'], tense))
    return '\n'.join(out)


def main(argv):
    if len(argv) < 2:
        print('쓰기: py -3.13 scripts/q.py <개체 이름> [--cap N]')
        return 1
    name = argv[1]
    cap = CAP
    if '--cap' in argv:
        cap = int(argv[argv.index('--cap') + 1])
    with io.open(paths.INDEX, encoding='utf-8') as f:
        idx = json.load(f)
    tmap = None
    if os.path.exists(paths.TIMES):
        with io.open(paths.TIMES, encoding='utf-8') as f:
            tmap = json.load(f)
    meta = ut.load(ROOT)
    print(render(lookup(ROOT, idx, name, cap, tmap, meta,
                        datetime.date.today().isoformat())))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
