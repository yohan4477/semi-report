# 문체 게이트 — 인사이트 문장이 읽히는 한국어인지 검사한다. 윤문은 하지 않는다.
# 설계: docs/superpowers/specs/2026-07-30-스킬-분할-구조화-design.md ④
# 규칙이 이미 스펙 문체 절에 표로 있어 결정론적으로 검사할 수 있다 — 에이전트 호출 0회.
import os, io, re, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_atoms as ca

GLOSSARY = os.path.join(ca.ROOT, 'insights', 'views', 'glossary.json')

# 용어가 아니라 문장을 망가뜨리는 것들 — 어느 회사인지 모르면 문장이 성립하지 않고,
# 다른 분야 비유는 이 문서의 용어가 아니다
BANNED = ['벤더', '진영', '커스텀 실리콘', '헤지', '익스포저']

REF = re.compile(r'\(\s*A-\d{6}-\d{2}(?:\s*,\s*A-\d{6}-\d{2})*\s*\)')
FM = re.compile(r'^---\n.*?\n---\n', re.DOTALL)

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def strip_refs(text):
    """원자 id 인용과 frontmatter를 떨어낸 서술만 남긴다 — 검사 대상은 사람이 쓴 문장이다."""
    text = FM.sub('', text or '')
    return REF.sub('', text)


def sentences(text):
    parts = re.split(r'(?<=[.!?])\s+|\n+', text or '')
    return [p.strip() for p in parts if p.strip()]


def load_glossary():
    if not os.path.exists(GLOSSARY):
        return {}
    return {k: v for k, v in json.load(io.open(GLOSSARY, encoding='utf-8')).items()
            if not k.startswith('_')}


def check_banned(text, where):
    for w in BANNED:
        if w in text:
            add('FAIL', where, 'P1', '금지어 "%s" — 어느 회사인지 밝히거나 뜻을 그대로 쓴다' % w)


def check_glossary(text, where, gloss):
    """사전 용어는 첫 등장 문장에서 풀어야 한다. 둘째 등장부터는 그냥 쓴다."""
    for term, plain in sorted(gloss.items(), key=lambda kv: -len(kv[0])):
        first = None
        for s in sentences(text):
            if term in s:
                first = s
                break
        if first is None:
            continue
        glossed = re.search(re.escape(term) + r'\s*\(', first) or (plain in first)
        if not glossed:
            add('FAIL', where, 'P2',
                '"%s" 첫 등장에 설명이 없다 — %s(%s) 형태로 풀거나 "%s"를 함께 쓴다'
                % (term, term, plain, plain))
