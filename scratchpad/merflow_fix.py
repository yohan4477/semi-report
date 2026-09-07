# -*- coding: utf-8 -*-
"""메르 흐름 사실표의 T번호를 원문에서 다시 매긴다.

    PYTHONIOENCODING=utf-8 python scratchpad/merflow_fix.py          # 보기만
    PYTHONIOENCODING=utf-8 python scratchpad/merflow_fix.py --write  # 고쳐 쓴다

왜 있나 — 메르 글은 본문 안에 자체 번호를 붙인다(「97. 정유설비 노후화…」). 사실표를
뽑는 에이전트가 그 번호를 T줄번호로 옮기면 빈 줄이나 엉뚱한 줄을 가리킨다. 열두 달을
손으로 고치면 같은 사고가 다시 나므로 기계가 다시 맞춘다.

어떻게 고르나 — 사실 문장에서 두 자리 이상 수와 길이 두 자 이상 한글 낱말을 뽑아
원문 줄마다 점수를 낸다. 수는 3점, 낱말은 1점이다(값이 더 무겁다). 으뜸이 유일하고
2점 이상이며 버금보다 2점 넘게 앞설 때만 바꾼다. **애매하면 안 바꾸고 사람에게 넘긴다** —
잘못 당긴 번호는 안 고친 번호보다 나쁘다.
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIP = os.path.join(ROOT, 'input', 'clippings', 'mer', '%s.json')
CITE = re.compile(r'\(메르-(\d+)\s+(T\d+(?:\s*,\s*T\d+)*)\)')
WRITE = '--write' in sys.argv

_cache = {}


def lines_of(no):
    if no not in _cache:
        p = CLIP % no
        _cache[no] = (json.load(io.open(p, encoding='utf-8'))['text'].split('\n')
                      if os.path.exists(p) else None)
    return _cache[no]


def norm(s):
    return re.sub(r'[\s,]', '', s)


def score(line, nums, words):
    h = norm(line)
    return 3 * sum(1 for x in nums if norm(x) in h) + sum(1 for w in words if w in line)


def best(L, body):
    nums = [x for x in re.findall(r'\d[\d,\.]*', body) if len(x.replace(',', '')) >= 2]
    words = [w for w in re.findall(r'[가-힣]{2,}', body)][:12]
    if not nums and not words:
        return None, 0, 0
    ranked = sorted(((score(s, nums, words), i + 1) for i, s in enumerate(L) if s.strip()),
                    reverse=True)
    if not ranked:
        return None, 0, 0
    top, second = ranked[0], (ranked[1] if len(ranked) > 1 else (0, 0))
    return top[1], top[0], second[0]


changed, kept, skipped = 0, 0, []
for f in sorted(glob.glob(os.path.join(ROOT, 'scratchpad', 'merflow_facts_*.md'))):
    month = os.path.basename(f)[len('merflow_facts_'):-3]
    out, dirty = [], False
    for raw in io.open(f, encoding='utf-8'):
        m = CITE.search(raw)
        if not m:
            out.append(raw)
            continue
        no = m.group(1)
        ns = [int(x) for x in re.findall(r'\d+', m.group(2))]
        L = lines_of(no)
        body = raw.split('|')[1] if '|' in raw else ''

        # 두 줄 이상을 가리키는데 그중 빈 줄이 섞였으면 빈 줄만 걷는다.
        # 메르 글은 내용 줄과 빈 줄이 갈마들어서 짝을 이어 적다 보면 한쪽이 빈 줄이 된다
        if L is not None and len(ns) > 1:
            live = [k for k in ns if 1 <= k <= len(L) and L[k - 1].strip()]
            if live and len(live) != len(ns):
                new_ref = ', '.join('T%d' % k for k in live)
                out.append(raw.replace(m.group(0), '(메르-%s %s)' % (no, new_ref)))
                print('  %s %s %s → %s  (빈 줄 걷음)' % (month, no, m.group(2), new_ref))
                changed += 1
                dirty = True
                continue
            if live:
                out.append(raw)
                kept += 1
                continue
            # 가리킨 줄이 죄다 빈 줄이다. 그 글은 내용이 통째로 한 칸 밀린 것이니
            # 아래 점수 매기기로 내려보내 다시 찾는다
            cand, s1, s2 = best(L, body)
            if cand and s1 >= 2 and s1 - s2 > 2:
                out.append(raw.replace(m.group(0), '(메르-%s T%d)' % (no, cand)))
                print('  %s %s %s → T%d  (전부 빈 줄, 다시 찾음 %d점)'
                      % (month, no, m.group(2), cand, s1))
                changed += 1
                dirty = True
            else:
                out.append(raw)
                skipped.append((month, no, ns[0], '전부 빈 줄인데 으뜸 T%s %d점 · 버금 %d점'
                                % (cand, s1, s2)))
            continue

        n = ns[0]
        ok_now = L is not None and 1 <= n <= len(L) and L[n - 1].strip()
        if ok_now:
            # 값이 그 줄에 있으면 그대로 둔다
            nums = [x for x in re.findall(r'\d[\d,\.]*', body)
                    if len(x.replace(',', '')) >= 2]
            if not nums or all(norm(x) in norm(L[n - 1]) for x in nums):
                out.append(raw)
                kept += 1
                continue
        if L is None:
            out.append(raw)
            skipped.append((month, no, n, '클리핑 없음'))
            continue
        cand, s1, s2 = best(L, body)
        if cand == n:
            # 이미 그 줄이 으뜸이다. 값 일부가 옆 줄에 있는 요약이라 여기 왔을 뿐이다
            out.append(raw)
            kept += 1
        elif cand and s1 >= 2 and s1 - s2 > 2:
            out.append(raw.replace('(메르-%s T%d)' % (no, n), '(메르-%s T%d)' % (no, cand)))
            print('  %s %s T%d → T%d  (점수 %d, 버금 %d)' % (month, no, n, cand, s1, s2))
            changed += 1
            dirty = True
        else:
            out.append(raw)
            skipped.append((month, no, n, '으뜸 T%s %d점 · 버금 %d점 — 애매해서 안 바꿈'
                            % (cand, s1, s2)))
    if WRITE and dirty:
        io.open(f, 'w', encoding='utf-8').write(''.join(out))

print('다시 매김 %d · 그대로 %d · 사람이 볼 것 %d' % (changed, kept, len(skipped)))
for month, no, n, why in skipped[:30]:
    print('  SKIP %s %s T%d — %s' % (month, no, n, why))
if len(skipped) > 30:
    print('  … %d건 더' % (len(skipped) - 30))
if not WRITE:
    print('\n(보기만 했다. 고쳐 쓰려면 --write)')
