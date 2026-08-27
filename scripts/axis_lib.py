# -*- coding: utf-8 -*-
"""축 검토의 계산부 — 카드를 읽고, 축으로 나누고, 무엇이 겹치고 비는지 센다.

표준출력을 쓰지 않는다. 자료구조만 돌려준다. 문자열로 바꾸는 일은 axis_review.py 가 한다.

카드는 대시보드 HTML 이 아니라 생성기 모듈의 CARDS 에서 읽는다. 생성물을 되읽으면
원본이 바뀔 때 어긋난다. 생성기는 전부 __main__ 가드를 갖고 최상위에서 파일을 안 쓰므로
import 는 안전하다.
"""
import glob
import importlib
import io
import os
import re
import sys

CARDS_RE = re.compile(r'^CARDS\s*=', re.M)
GEN_DIRS = ('scratchpad', 'insights', 'scripts')
# 낱말을 찾을 필드. stats·table 은 숫자라 잡음이고 links 는 경로라 파일명이 걸린다
TEXT_KEYS = ('title', 'oneliner', 'gain', 'points', 'quote', 'note', 'clash')


def card_modules(root):
    out = []
    for d in GEN_DIRS:
        for path in glob.glob(os.path.join(root, d, 'gen_*.py')):
            with io.open(path, encoding='utf-8', errors='replace') as f:
                if CARDS_RE.search(f.read()):
                    out.append((os.path.splitext(os.path.basename(path))[0], path))
    return sorted(out)


def load_cards(root, module):
    for d in GEN_DIRS:
        p = os.path.join(root, d)
        if p not in sys.path:
            sys.path.insert(0, p)
    return list(getattr(importlib.import_module(module), 'CARDS', ()))


def _flat(v):
    if v is None:
        return []
    if isinstance(v, str):
        return [v]
    if isinstance(v, (list, tuple)):
        out = []
        for x in v:
            out.extend(_flat(x))
        return out
    return []


def card_text(card):
    parts = []
    for k in TEXT_KEYS:
        parts.extend(_flat(card.get(k)))
    return ' '.join(parts).lower()


def card_id(card):
    return card.get('title', '')
