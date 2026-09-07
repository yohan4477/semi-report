# -*- coding: utf-8 -*-
"""메르 흐름 사실표 검증 — 인용한 T줄이 실재하나, 그 줄에 그 값이 있나.

    PYTHONIOENCODING=utf-8 python scratchpad/merflow_verify.py

왜 있나 — 메르 글은 본문 안에 자체 번호를 붙인다(「97. 정유설비 노후화…」). 사실표를
뽑는 에이전트가 그 번호를 T줄번호로 착각하면, 있지도 않은 줄을 가리키거나 엉뚱한 줄을
가리킨다. 2026-09 를 맡은 에이전트가 스스로 걸려 되돌린 사고다(「97.」이 실제로는 T68).

세 가지를 센다.
    B  빈 줄을 가리켰다            거의 언제나 자체 번호를 T로 착각한 것이다
    R  줄 수를 넘겼다              같은 원인
    V  그 줄에 그 값이 없다        값이 인접 줄에 있으면 ±4줄을 훑어 알려 준다

V 는 WARN 이다 — 사실표 한 줄이 원문 두세 줄을 요약하면 값이 옆 줄에 있을 수 있다.
B·R 은 FAIL 이다. 지어낸 번호이거나 자체 번호를 옮긴 것이다.
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

_cache = {}


def lines_of(no):
    if no not in _cache:
        p = CLIP % no
        if not os.path.exists(p):
            _cache[no] = None
        else:
            _cache[no] = json.load(io.open(p, encoding='utf-8'))['text'].split('\n')
    return _cache[no]


def norm(s):
    """값 비교용 — 공백과 쉼표를 걷는다. 만·억은 펴지 않는다(원문 표기를 그대로 쓰라 했으므로)."""
    return re.sub(r'[\s,]', '', s)


bad, warn, ok, seen = [], [], 0, 0
for f in sorted(glob.glob(os.path.join(ROOT, 'scratchpad', 'merflow_facts_*.md'))):
    month = os.path.basename(f)[len('merflow_facts_'):-3]
    for raw in io.open(f, encoding='utf-8'):
        m = CITE.search(raw)
        if not m:
            continue
        seen += 1
        no = m.group(1)
        ns = [int(x) for x in re.findall(r'\d+', m.group(2))]
        L = lines_of(no)
        if L is None:
            bad.append((month, no, ns[0], '클리핑이 없다'))
            continue
        seen += len(ns) - 1          # 여러 줄이면 그만큼 더 센다
        n = ns[0]
        if len(ns) > 1:
            # 여러 줄을 가리키면 줄마다 빈 줄만 보고, 값은 그 줄들을 합쳐서 본다
            blank = [k for k in ns if k < 1 or k > len(L) or not L[k - 1].strip()]
            if blank:
                bad.append((month, no, blank[0], '빈 줄이다(여러 줄 인용 %s)' % ns))
                continue
            body = raw.split('|')[1] if '|' in raw else ''
            here = norm(''.join(L[k - 1] for k in ns))
            nums = [x for x in re.findall(r'\d[\d,\.]*', body)
                    if len(x.replace(',', '')) >= 2]
            miss = [x for x in nums if norm(x) not in here]
            if miss:
                warn.append((month, no, n, miss, []))
            else:
                ok += 1
            continue
        if n < 1 or n > len(L):
            bad.append((month, no, n, '줄 수 %d 를 넘겼다' % len(L)))
            continue
        if not L[n - 1].strip():
            near = [k for k in range(max(1, n - 4), min(len(L), n + 5)) if L[k - 1].strip()]
            bad.append((month, no, n, '빈 줄이다. 가까운 채워진 줄 %s' % near))
            continue
        # 그 줄에 그 값이 있나 — 사실표 본문에서 두 자리 이상 수만 본다
        body = raw.split('|')[1] if '|' in raw else ''
        nums = [x for x in re.findall(r'\d[\d,\.]*', body) if len(x.replace(',', '')) >= 2]
        here = norm(L[n - 1])
        miss = [x for x in nums if norm(x) not in here]
        if miss:
            span = norm(''.join(L[max(0, n - 5):n + 4]))
            near = [x for x in miss if norm(x) in span]
            warn.append((month, no, n, miss, near))
        else:
            ok += 1

print('사실표 인용 %d건 · 줄 일치 %d건' % (seen, ok))
for month, no, n, why in bad:
    print('  FAIL %s %s T%d — %s' % (month, no, n, why))
for month, no, n, miss, near in warn[:40]:
    tail = ' (±4줄 안에 있음: %s)' % near if near else ' (±4줄 안에도 없다)'
    print('  WARN %s %s T%d — 그 줄에 없는 값 %s%s' % (month, no, n, miss, tail))
if len(warn) > 40:
    print('  … WARN %d건 더' % (len(warn) - 40))
print('FAIL %d · WARN %d' % (len(bad), len(warn)))
raise SystemExit(1 if bad else 0)
