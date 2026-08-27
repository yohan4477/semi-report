# -*- coding: utf-8 -*-
"""가지에 근거를 붙인다 — 날 것으로 세지 않고 낱말 특이도로 무게를 준다.

날 것으로 세면 거짓말한다. 원문 478편에서 실제로 쟀다.

  자금 조달 253편 = 「리스」178(37%) + 「부채」99(21%) + 「금리」97(20%)
                    「SPV」는 4편(1%)
  시간당 단가 14편 = 낱말 넷이 전부 0~2%

흔한 낱말이 만든 합집합이고, 그 위에 더 나쁜 것이 있었다 — 「리스」 178편에는
「애널리스트」와 「리스크」가 섞여 있다. 리스 계약과 무관한 글이 근거로 들어온다.

그래서 둘을 한다.
  낱말 특이도   log(N/df). 「리스」 0.99, 「SPV」 4.78. 흔한 말은 무게가 없다
  걸러낼 말     한국어는 조사 때문에 부분 문자열로 잡아야 하는데 그러면 짧은 말이
               긴 말 안에 걸린다. 개체마다 걸러낼 말을 적어 그 자리를 안 센다

그리고 낱말별 문서 수를 따로 낸다. 253 이 「리스」 하나로 부푼 것을 그 줄이 드러낸다 —
가지 하나가 흔한 낱말 한 개에 업혀 있는지는 합계만 봐서는 안 보인다.

읽기 전용이다. 아무것도 쓰지 않는다.
"""
import glob
import io
import math
import os
import re

LATIN = re.compile(r'[A-Za-z]')


def corpus(root, pattern='content/**/*.md'):
    """(상대경로, 본문) 목록. 정렬돼 있다."""
    out = []
    for p in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
        rel = os.path.relpath(p, root).replace('\\', '/')
        with io.open(p, encoding='utf-8', errors='replace') as f:
            out.append((rel, f.read()))
    return out


def _spans(line, term):
    """낱말이 놓인 자리들. 라틴 문자가 든 말은 단어 경계를 요구한다."""
    if LATIN.search(term):
        pat = re.compile(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])' % re.escape(term), re.I)
        return [(m.start(), m.end()) for m in pat.finditer(line)]
    out, at = [], line.find(term)
    while at != -1:
        out.append((at, at + len(term)))
        at = line.find(term, at + 1)
    return out


def _denied(line, start, end, deny):
    for d in deny or ():
        at = line.find(d)
        while at != -1:
            if at <= start and end <= at + len(d):
                return True
            at = line.find(d, at + 1)
    return False


def line_hits(line, term, deny=()):
    """그 줄에서 낱말이 실제로 그 뜻으로 쓰인 자리들. 걸러낼 말 안이면 안 센다."""
    if not line or not term:
        return []
    return [(s, e) for s, e in _spans(line, term) if not _denied(line, s, e, deny)]


def doc_freq(docs, term, deny=()):
    """줄이 아니라 문서를 센다. 한 글에서 열 번 나와도 한 편이다."""
    n = 0
    for _, text in docs:
        if any(line_hits(ln, term, deny) for ln in text.split('\n')):
            n += 1
    return n


def idf(total, df):
    """흔할수록 0 에 가깝다. 아무 데도 없거나 모든 데 있으면 0 이다."""
    if not df or not total or df >= total:
        return 0.0
    return math.log(float(total) / df)


def weigh(docs, branch):
    """가지 하나에 근거를 붙인다. 합계와 낱말별 내역을 같이 낸다."""
    terms = list(branch.get('terms') or ())
    deny = tuple(branch.get('deny') or ())
    total = len(docs)

    per, hit_docs, hits = [], set(), set()
    for t in sorted(terms):
        seen = set()
        for rel, text in docs:
            for i, ln in enumerate(text.split('\n'), 1):
                if line_hits(ln, t, deny):
                    seen.add(rel)
                    hits.add('%s#L%d' % (rel, i))
        per.append({'term': t, 'docs': len(seen), 'idf': round(idf(total, len(seen)), 3)})
        hit_docs |= seen

    by_term = {p['term']: p for p in per}
    weight = 0.0
    for rel, text in docs:
        for t in terms:
            if any(line_hits(ln, t, deny) for ln in text.split('\n')):
                weight += by_term[t]['idf']

    widest = max(per, key=lambda p: (p['docs'], p['term']))['term'] if per else None
    if widest and by_term[widest]['docs'] == 0:
        widest = None

    return {
        'label': branch.get('label', ''),
        'docs': len(hit_docs),
        'weight': round(weight, 3),
        'widest': widest,
        'terms': per,
        'hits': sorted(hits),
    }
