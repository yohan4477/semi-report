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
# 낱말을 찾을 필드. stats·table 은 숫자라 잡음이고 links 는 경로라 파일명이 걸린다.
# meta 는 뺀다 — 필자·업로드일이 들어 있어 이름·연도가 엉뚱하게 걸린다.
# slim_oneliner·slim_points 는 oneliner·points 대신 쓰는 카드(건강·Epoch·계보 등)의 본문이다
TEXT_KEYS = ('title', 'oneliner', 'slim_oneliner', 'gain', 'points', 'slim_points',
             'quote', 'note', 'clash')


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
    """축 정의를 정규화한다. 사람이 적은 shape 는 버리고 칸에서 계산한 값을 넣는다.

    사람이 직접 쓴 JSON 이 이 도구의 주 입력이라 내용이 어긋나면 ValueError 로
    알린다 — 트레이스백 대신 무엇이 잘못됐는지 한국어로 짚는다.
    """
    if not isinstance(obj, dict):
        raise ValueError('축 정의는 객체(object)여야 하는데 %s 다' % type(obj).__name__)
    cells = []
    for c in obj.get('cells') or ():
        if not isinstance(c, dict):
            raise ValueError('칸은 객체(object)여야 하는데 %r 다' % (c,))
        if 'id' not in c:
            raise ValueError('칸에 id 가 없다: %r' % (c,))
        cid = c['id']
        if not isinstance(cid, str):
            raise ValueError('칸 id 는 문자열이어야 하는데 %r 다' % (cid,))
        raw_words = list(c.get('words') or ())
        for w in raw_words:
            if not isinstance(w, str):
                raise ValueError('칸 %r 의 낱말은 문자열이어야 하는데 %r 다' % (cid, w))
        words = [w.lower() for w in ([cid] + raw_words)]
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


def _tally(cells, placement):
    """칸마다 카드가 몇 장인지 센다. review 와 declared_review 가 같은 셈을 쓴다."""
    counts = {cell['id']: 0 for cell in cells}
    for hits in placement.values():
        for cid in hits:
            counts[cid] += 1
    placed = [n for n in counts.values() if n]
    return counts, placed


def _summarize(cards, axis, placement):
    """review 와 declared_review 가 공유하는 집계. overlap 의 이름은 호출부가 정한다.

    여기서는 겹치는 카드를 'overlap' 에 담아 돌려준다 — review 는 그대로 쓰고
    declared_review 는 'overlap_declared' 로 옮기고 'overlap' 을 비운다.
    """
    counts, placed = _tally(axis['cells'], placement)
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


def review(cards, axis):
    """넷을 센다 — 겹침·빈칸·잔여·쏠림. 아무것도 던지지 않는다."""
    placement = place(cards, axis)
    return _summarize(cards, axis, placement)


def _sec_id(sec):
    return sec[0] if isinstance(sec, (list, tuple)) and sec else sec


def declared_axis(cards):
    """섹션이 이미 축이다. 카드에 적힌 차례가 곧 칸의 차례다."""
    ids, seen = [], set()
    for c in cards:
        for sec in [c.get('section')] + list(c.get('also') or ()):
            sid = _sec_id(sec)
            if sid is not None and sid not in seen:
                seen.add(sid)
                ids.append(sid)
    return parse_axis({'name': '섹션', 'cells': [{'id': i} for i in ids]})


def declared_place(cards):
    """선언된 배치는 낱말로 안 정한다. section 과 also 를 그대로 읽는다."""
    out = {}
    for c in cards:
        secs = [c.get('section')] + list(c.get('also') or ())
        out[card_id(c)] = sorted({_sec_id(s) for s in secs if _sec_id(s) is not None})
    return out


def declared_review(cards):
    """섹션 축의 집계. 겹침은 사람이 선언한 것이므로 이름을 달리 단다."""
    axis = declared_axis(cards)
    placement = declared_place(cards)
    res = _summarize(cards, axis, placement)
    res['overlap_declared'] = res['overlap']
    res['overlap'] = []
    return res
