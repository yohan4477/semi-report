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

이 검사기는 **빈 줄과 없는 번호만 잡는다.** 뜻이 맞는지는 못 본다 — 그건 대조 에이전트와
사람의 표본 확인이 할 일이다. 그래도 잘못 짚은 인용의 대부분이 여기서 걸린다.
"""
import glob, io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# 라벨 → 원문 title 의 일부
LAB = {
    '메르-역전': '장단기금리 역전이 뭐고',
    '메르-역전AS': '장단기 금리 역전이 뭐고',
    '메르-SLR': 'SLR규제 완화를 실행할까',
    '메르-몰빵': '단기국채 몰빵 발행은 정말 괜찮을까?',
    '메르-몰빵AS': '단기국채 몰빵 발행은 정말 괜찮을까? A/S',
    '메르-자경단1': '채권자경단이 출몰할 수 있다는 말의 무서운 의미는? 1',
    '메르-자경단2': '채권자경단이 출몰할 수 있다는 말의 무서운 의미는? 2',
    '메르-한국CPI': '한국 물가(CPI)가 정말 이렇게 낮을까',
    '메르-CPI비밀': '한국 CPI의 비밀',
    '메르-잭슨홀': '미국 7월 소비자물가지수(CPI)와 잭슨홀',
    '메르-한은인상': '한국은행의 기준금리 연속 인상',
    '메르-양발운전': '케빈 워시의 양발운전',
    '메르-청문회': '케빈 워시 연준의장 후보는 청문회에서',
    '메르-엔화': '엔화가 다시 강해질까',
    '메르-일본인상': '일본은행이 금리를 올리면 어떤 일이',
    '메르-공동개입': '엔화환율에 공동으로 개입했나',
    '메르-덴마크': '덴마크 연기금 미국 국채 전량 매도',
    '메르-중국매각': '중국정부가 은행들에게 미국국채 매각',
    '메르-유가': '국채금리 폭등이 정말 유가 때문일까',
    '메르-끝없이': '미국국채 금리가 끝없이 오르는 이유는?',
    '메르-끝없이AS': '미국국채 금리가 끝없이 오르는 이유는?  빠른 A/S',
    '메르-조달계획': '재무부 분기조달계획이 발표되었다',
    '메르-바이백': '미국국채 구하기, 재무부의 바이백',
    '메르-AI주가': '미국국채금리가 오른다고 AI성장주',
}

docs = {}
for p in glob.glob('input/clippings/mer/*.json'):
    d = json.load(io.open(p, encoding='utf-8'))
    docs[d.get('title', '')] = d

lines = {}
for lab, key in LAB.items():
    hits = [t for t in docs if key in t]
    if not hits:
        print('원문 못 찾음:', lab, '|', key)
        continue
    # A/S 처럼 제목이 겹치면 더 긴 쪽이 A/S 다. 정확히 고른다
    hits.sort(key=len)
    t = hits[-1] if lab.endswith('AS') or lab.endswith('2') else hits[0]
    lines[lab] = docs[t]['text'].split('\n')

draft = io.open('insights/reports/rate-2026-09-05.md', encoding='utf-8').read()
bad, ok = [], 0
for m in re.finditer(r'\((메르-[^\s)]+)\s+([^)]+)\)', draft):
    lab, refs = m.group(1), m.group(2)
    if lab not in lines:
        bad.append((lab, refs, '라벨 사전에 없음'))
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

print('메르 인용 확인 %d건 · 어긋남 %d건' % (ok + len(bad), len(bad)))
for lab, r, why in bad:
    print('  %s %s — %s' % (lab, r, why))
