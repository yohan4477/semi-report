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




def parse_axis(obj):
    """축 정의를 정규화한다. 사람이 적은 shape 는 버리고 칸에서 계산한 값을 넣는다."""
    cells = []
    for c in obj.get('cells') or ():
        cid = c['id']
        words = [w.lower() for w in ([cid] + list(c.get('words') or ()))]
        seen, uniq = set(), []
        for w in words:
            if w not in seen:
                seen.add(w)
                uniq.append(w)
        cell = {'id': cid, 'words': uniq}
        for k in ('order', 'parent', 'feeds', 'op'):
            if c.get(k) is not None:
                cell[k] = c[k]
        cells.append(cell)
    axis = {'name': obj.get('name', ''), 'cells': cells}
    axis['shape'] = shape_of(axis)
    return axis


def shape_of(axis):
    """형은 고르는 것이 아니라 칸 사이 관계에서 읽힌다.

    고리를 사슬보다 먼저 본다 — 고리는 사슬의 특수한 꼴이라 뒤에 보면 사슬로 읽힌다.
    """
    cells = axis.get('cells') or []
    if not cells:
        return '목록'
    ids = [c['id'] for c in cells]
    feeds = {c['id']: c.get('feeds') for c in cells if c.get('feeds')}
    if feeds and feeds.get(ids[-1]) == ids[0]:
        return '고리'
    if any(c.get('op') for c in cells):
        return '수식'
    if feeds:
        return '사슬'
    if any(c.get('parent') for c in cells):
        return '나무'
    if all(c.get('order') is not None for c in cells):
        return '선'
    return '목록'


def place(cards, axis):
    """카드를 칸에 넣는다. 오직 card_text 와 축의 낱말로만 정한다.

    c['also'] 를 안 본다 — 그건 사람이 선언한 다중 배치라 계산이 만든 겹침과 다르다.
    """
    out = {}
    for c in cards:
        text = card_text(c)
        hit = sorted({cell['id'] for cell in axis['cells']
                      if any(w in text for w in cell['words'])})
        out[card_id(c)] = hit
    return out


def review(cards, axis):
    """넷을 센다 — 겹침·빈칸·잔여·쏠림. 아무것도 던지지 않는다."""
    placement = place(cards, axis)
    counts = {cell['id']: 0 for cell in axis['cells']}
    for hits in placement.values():
        for cid in hits:
            counts[cid] += 1
    placed = [n for n in counts.values() if n]
    residual = sorted(t for t, hits in placement.items() if not hits)
    total = len(cards)
    return {
        'axis': axis.get('name', ''),
        'shape': axis.get('shape') or shape_of(axis),
        'cards': total,
        'cells': [{'id': cell['id'], 'n': counts[cell['id']]}
                  for cell in axis['cells']],
        'overlap': [{'card': t, 'cells': hits}
                    for t, hits in sorted(placement.items()) if len(hits) > 1],
        'empty': [cell['id'] for cell in axis['cells'] if not counts[cell['id']]],
        'residual': residual,
        'residual_pct': round(100 * len(residual) / total) if total else 0,
        'skew': round(max(placed) / min(placed), 1) if placed else 0,
        'placement': placement,
    }
