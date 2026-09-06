# -*- coding: utf-8 -*-
"""json 원문을 인용한 보고서의 T번호가 실재하는 줄을 가리키나.

    PYTHONIOENCODING=utf-8 python scripts/check_jsoncite.py

왜 있나 — 마크다운은 줄 번호가 파일에 그대로 있어서 인용을 기계가 짚을 수 있는데, json
클리핑(메르)은 그렇지 않다. 그래서 사실표를 뽑는 에이전트가 저마다 다른 기준으로 줄을
셌고(빈 줄을 세거나 안 세거나), 2026-09-05 금리·물가 층 초안에서 인용 194건 가운데
54건이 빈 줄이나 파일 끝을 가리켰다. 대조 에이전트도 같은 이유로 한 편은 전부 틀렸다고,
다른 편은 맞다고 엇갈리게 보고했다.

규약 — T숫자는 그 글 `text` 필드를 줄바꿈으로 쪼갠 **1부터의 순번**이다(빈 줄 포함).
위임문(insight-report/references/위임문.md)에 이 문장을 넣지 않으면 또 갈린다.

라벨 사전은 **각 보고서 frontmatter 의 `labels:` 에서 읽는다**(`메르-XXX=mer/제목조각`).
2026-09-06 트럼프 층을 세울 때까지는 이 파일에 층 하나와 라벨 스물다섯이 박혀 있어서,
층이 늘 때마다 검사기를 손으로 고쳐야 했다. 선언한 자리가 곧 사전이라야 낡지 않는다.

이 검사기는 **빈 줄과 없는 번호만 잡는다.** 뜻이 맞는지는 못 본다 — 그건 대조 에이전트와
사람의 표본 확인이 할 일이다. 그래도 잘못 짚은 인용의 대부분이 여기서 걸린다.
"""
import glob, io, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, 'insights', 'reports', '*.md')
CLIPS = os.path.join(ROOT, 'input', 'clippings', 'mer', '*.json')

docs = {}
for p in glob.glob(CLIPS):
    d = json.load(io.open(p, encoding='utf-8'))
    docs[d.get('title', '')] = d


def labels_of(front):
    """frontmatter labels: 에서 `메르-XXX=mer/제목조각` 만 걷어 온다."""
    m = re.search(r'^labels:\s*(.+)$', front, re.M)
    if not m:
        return {}
    out = {}
    for item in m.group(1).split('·'):
        mm = re.match(r'\s*(메르-[^\s=]+)\s*=\s*mer/(.+?)\s*$', item)
        if mm:
            out[mm.group(1)] = mm.group(2)
    return out


def lines_of(lab, key):
    """제목 조각으로 원문을 찾아 줄 목록을 돌려준다. 못 찾으면 None."""
    hits = [t for t in docs if key in t]
    if not hits:
        return None
    # A/S 처럼 제목이 겹치면 더 긴 쪽이 A/S 다. 정확히 고른다
    hits.sort(key=len)
    t = hits[-1] if lab.endswith('AS') or lab.endswith('2') else hits[0]
    return docs[t]['text'].split('\n')


total_ok, total_bad, seen = 0, 0, 0
for path in sorted(glob.glob(REPORTS)):
    raw = io.open(path, encoding='utf-8').read()
    front = raw.split('---')[1] if raw.startswith('---') else ''
    lab_map = labels_of(front)
    cites = list(re.finditer(r'\((메르-[^\s)]+)\s+([^)]+)\)', raw))
    if not cites:
        continue
    seen += 1
    lines, bad, ok = {}, [], 0
    for lab, key in lab_map.items():
        L = lines_of(lab, key)
        if L is None:
            bad.append((lab, key, '제목 조각으로 원문을 못 찾음'))
        else:
            lines[lab] = L
    for m in cites:
        lab, refs = m.group(1), m.group(2)
        if lab not in lines:
            if lab not in lab_map:
                bad.append((lab, refs, 'labels 에 없는 라벨'))
            continue
        L = lines[lab]
        for r in re.findall(r'T(\d+)', refs):
            n = int(r)
            if n < 1 or n > len(L):
                bad.append((lab, 'T%d' % n, '줄 수 %d 를 넘김' % len(L)))
            elif not L[n - 1].strip():
                near = [k for k in range(max(1, n - 3), min(len(L), n + 4)) if L[k - 1].strip()]
                bad.append((lab, 'T%d' % n, '빈 줄. 가까운 채워진 줄 %s' % near))
            else:
                ok += 1
    print('%s — 메르 인용 %d건 · 어긋남 %d건' % (os.path.basename(path), ok + len(bad), len(bad)))
    for lab, r, why in bad:
        print('  FAIL %s %s — %s' % (lab, r, why))
    total_ok += ok
    total_bad += len(bad)

print('요약: 층 %d편 · 인용 %d건 · FAIL %d' % (seen, total_ok + total_bad, total_bad))
raise SystemExit(1 if total_bad else 0)
