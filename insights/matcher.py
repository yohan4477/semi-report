# -*- coding: utf-8 -*-
"""줄 하나에서 개체를 찾는다. 파일도 코퍼스도 모른다 — 문자열만 받는다.

규칙이 셋이다.
  영문 별칭  단어 경계를 요구한다. Lam 이 Lamborghini 에 걸리면 안 된다
  한글 별칭  부분 문자열로 잡는다. 조사가 붙어서 경계를 요구하면 다 놓친다
  deny      그 자리가 deny 항목의 일부면 버린다. 메타 가 메타버스 에 걸린다
"""
import re

import entities_lib as el

LATIN = re.compile(r'[A-Za-z]')


def compile_rules(rows):
    out = []
    for r in sorted(rows, key=lambda x: x['canonical']):
        deny = tuple(r.get('deny') or [])
        for a in el.aliases_of(r):
            if not a:
                continue
            if LATIN.search(a):
                pat = re.compile(r'(?<![A-Za-z0-9])%s(?![A-Za-z0-9])'
                                 % re.escape(a), re.I)
                out.append((r['canonical'], pat, None, deny))
            else:
                out.append((r['canonical'], None, a, deny))
    return out


def _denied(line, start, end, deny):
    for d in deny:
        at = line.find(d)
        while at != -1:
            if at <= start and end <= at + len(d):
                return True
            at = line.find(d, at + 1)
    return False


def find(line, rules):
    if not line:
        return []
    hit = set()
    for canonical, pat, literal, deny in rules:
        if canonical in hit:
            continue
        if pat is not None:
            for m in pat.finditer(line):
                if not _denied(line, m.start(), m.end(), deny):
                    hit.add(canonical)
                    break
        else:
            at = line.find(literal)
            while at != -1:
                if not _denied(line, at, at + len(literal), deny):
                    hit.add(canonical)
                    break
                at = line.find(literal, at + 1)
    return sorted(hit)
