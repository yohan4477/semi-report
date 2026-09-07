# -*- coding: utf-8 -*-
"""메르 흐름 장 검사기 — 구조가 서 있나, 인용한 글이 실재하나, 그 안에 그 숫자가 있나.

    PYTHONIOENCODING=utf-8 python insights/check_merflow.py

링크드인 흐름(check_liflow)과 같은 갈래인데 인용 꼴이 다르다. 링크드인은 게시물
식별자 하나로 가리키지만 메르는 글 하나가 길어서 **글번호와 줄번호 둘**로 가리킨다.

    (메르-224190224535 T73)

T숫자는 그 글 `text` 를 줄바꿈으로 쪼갠 1부터의 순번이다(빈 줄 포함).

**빈 줄을 가리키는 사고가 이 장의 고질이다.** 메르 글은 본문 안에 자체 번호를 붙이는데
(「97. 정유설비 노후화…」) 그 번호를 줄번호로 옮기면 엉뚱한 데를 가리킨다. 사실표를
뽑은 열두 에이전트 가운데 스스로 알아챈 것은 하나뿐이었다(2026-09-07). 그래서 기계가
전수로 센다.

정규화는 check_liflow 의 것을 그대로 쓴다 — 만·억 전개와 한글 수사를 양쪽에 똑같이
건다. 한쪽만 걸면 멀쩡한 인용을 물고, 과하게 걸면 지어낸 값을 놓친다.
"""
import glob
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOWS = os.path.join(ROOT, 'insights', 'mer_flows')
CLIP = os.path.join(ROOT, 'input', 'clippings', 'mer')

sys.path.insert(0, os.path.join(ROOT, 'insights'))
from check_liflow import normalize  # noqa: E402  정규화는 한 곳에만 둔다

LEN_MIN, LEN_MAX = 5500, 6500
SEC_MIN, SEC_MAX = 5, 7
LAST_SEC = '말하지 않은 것'

CITE = re.compile(r'\(메르-(\d+)\s+(T\d+(?:[-,]\s*T?\d+)*)\)')
NUM = re.compile(r'\d[\d.]*')
_clips = {}


def lines_of(no):
    if no not in _clips:
        p = os.path.join(CLIP, '%s.json' % no)
        _clips[no] = (json.load(io.open(p, encoding='utf-8'))['text'].split('\n')
                      if os.path.exists(p) else None)
    return _clips[no]


def sentences(body):
    """인용이 붙은 문장만. 인용은 마침표 앞에 오므로 「마침표+공백」으로 자른다."""
    body = re.sub(r'\[\[fig:[A-Z]+\]\]', '', body)
    for para in body.split('\n'):
        if not para.strip() or para.startswith(('#', '|', '---')):
            continue
        for s in re.split(r'(?<=[.!?])\s+', para):
            if CITE.search(s):
                yield s.strip()


def check(path):
    raw = io.open(path, encoding='utf-8').read()
    body = raw.split('---', 2)[2] if raw.startswith('---') else raw
    name = os.path.basename(path)
    bad, warn = [], []

    # ① 구조
    secs = re.findall(r'^## (?:\d+\.\s*)?(.+)$', body, re.M)
    plain = re.sub(r'\(메르-[^)]*\)|\[\[fig:[A-Z]+\]\]|[#|>*`-]', '', body)
    n = len(re.sub(r'\s', '', plain))
    if not (LEN_MIN <= n <= LEN_MAX):
        bad.append('[M1] 본문 %d자 — %d~%d자여야 한다' % (n, LEN_MIN, LEN_MAX))
    if not (SEC_MIN <= len(secs) <= SEC_MAX):
        bad.append('[M2] 절 %d개 — %d~%d개여야 한다' % (len(secs), SEC_MIN, SEC_MAX))
    if secs and LAST_SEC not in secs[-1]:
        bad.append('[M3] 마지막 절이 「%s」가 아니다 — %s' % (LAST_SEC, secs[-1]))

    # ② 인용
    seen = 0
    for s in sentences(body):
        for m in CITE.finditer(s):
            no, refs = m.group(1), m.group(2)
            L = lines_of(no)
            if L is None:
                bad.append('[M4] 클리핑이 없다 — 메르-%s' % no)
                continue
            for r in re.findall(r'(\d+)', refs):
                seen += 1
                k = int(r)
                if k < 1 or k > len(L):
                    bad.append('[M5] 메르-%s T%d — 줄 수 %d 를 넘겼다' % (no, k, len(L)))
                elif not L[k - 1].strip():
                    near = [j for j in range(max(1, k - 3), min(len(L), k + 4)) if L[j - 1].strip()]
                    bad.append('[M6] 메르-%s T%d — 빈 줄이다. 가까운 채워진 줄 %s' % (no, k, near))
        # 문장의 숫자가 그 글 안에 있나. 줄이 아니라 글 단위로 본다 —
        # 한 문장이 원문 두세 줄을 요약하는 것이 이 장의 정상 꼴이다
        posts = ''.join(normalize(''.join(lines_of(m.group(1)) or []))
                        for m in CITE.finditer(s))
        for x in NUM.findall(normalize(re.sub(r'\(메르-[^)]*\)', '', s))):
            if len(x.rstrip('.')) >= 2 and x.rstrip('.') not in posts:
                warn.append('[M7] %s — 인용한 글에 없는 값 「%s」: %s' % (name, x, s[:60]))

    print('%s — 본문 %d자 · 절 %d개 · 인용 %d건' % (name, n, len(secs), seen))
    for b in bad:
        print('  FAIL %s' % b)
    for w in warn[:20]:
        print('  WARN %s' % w)
    if len(warn) > 20:
        print('  … WARN %d건 더' % (len(warn) - 20))
    return len(bad), len(warn)


if __name__ == '__main__':
    paths = sorted(glob.glob(os.path.join(FLOWS, '*.md')))
    if not paths:
        print('건너뜀 — insights/mer_flows/ 에 글이 아직 없다')
        raise SystemExit(0)
    f = w = 0
    for p in paths:
        a, b = check(p)
        f, w = f + a, w + b
    print('요약: 글 %d편 / FAIL %d / WARN %d' % (len(paths), f, w))
    raise SystemExit(1 if f else 0)
