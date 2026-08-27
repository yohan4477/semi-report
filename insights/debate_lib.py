# -*- coding: utf-8 -*-
"""쟁점 파일 한 장을 구조로 바꾼다.

파싱만 한다. 규칙에 맞는지는 check_debate.py 가 본다 — 붙여 두면 생성기가
검사기를 끌고 들어온다.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_lib as nl

STANCES = ('충돌', '동의', '결다름', '단독')
MODERATOR = ('물음', '갈리는 자리', '무엇을 보면 갈리나')

SEC_RE = re.compile(r'^##[ \t]+(.+?)[ \t]*$', re.M)
# 제목줄 — 화자 · 날짜 · 「글 제목」. 가운뎃점을 구분자로 쓴다
VOICE_RE = re.compile(
    r'^###[ \t]+(.+?)[ \t]*·[ \t]*(\d{4}-\d{2}-\d{2})[ \t]*·[ \t]*「(.+?)」[ \t]*$', re.M)
REL_RE = re.compile(r'^[-*][ \t]*관계:[ \t]*(\S+)(?:[ \t]*↔[ \t]*(.+?))?[ \t]*$')
CLAIM_RE = re.compile(r'^[-*][ \t]*주장:[ \t]*(.+?)[ \t]*$')


def split_sections(body):
    """h2 제목 → 그 절의 본문."""
    out = {}
    hits = list(SEC_RE.finditer(body))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        out[m.group(1)] = body[m.end():end].strip()
    return out


def parse_voices(sec):
    """「발언」 절을 발언 목록으로."""
    out = []
    hits = list(VOICE_RE.finditer(sec))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(sec)
        stance, against, claim, lines = '', '', '', []
        for line in sec[m.end():end].split('\n'):
            r = REL_RE.match(line)
            c = CLAIM_RE.match(line)
            if r:
                stance = r.group(1)
                against = (r.group(2) or '').strip()
            elif c:
                claim = c.group(1)
            else:
                lines.append(line)
        out.append({'actor': m.group(1).strip(),
                    'said': m.group(2),
                    'title': m.group(3).strip(),
                    'stance': stance,
                    'against': against,
                    'claim': claim,
                    'body': '\n'.join(lines).strip()})
    return out


def voice_key(v):
    """관계 대상과 짝을 맞추는 열쇠 — 화자 MM-DD 「제목」."""
    return '%s %s 「%s」' % (v['actor'], v['said'][5:], v['title'])


def parse(text):
    meta, body = nl.parse_front(text)
    sections = split_sections(body)
    return {'meta': meta,
            'sources': nl.sources_of(meta),
            'sections': sections,
            'voices': parse_voices(sections.get('발언', ''))}
