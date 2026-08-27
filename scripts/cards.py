# -*- coding: utf-8 -*-
"""카드 적재 — 대시보드 생성기의 CARDS 에서 카드를 읽는다.

카드는 대시보드 HTML 이 아니라 생성기 모듈의 CARDS 리스트에서 읽는다. 생성물을
되읽으면 원본이 바뀔 때 어긋난다. 생성기는 전부 __main__ 가드를 갖고 최상위에서
파일을 안 쓰므로 import 는 안전하다 — gen_*.py 26개를 전수 확인했다.

읽기 전용이다. 아무것도 쓰지 않는다.
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
# slim_oneliner·slim_points 는 oneliner·points 대신 쓰는 카드(건강·Epoch·계보 등)의
# 본문이다. 이걸 빼면 카드 368장 중 101장이 제목만 읽히고 그 대시보드가 통째로 굶는다.
TEXT_KEYS = ('title', 'oneliner', 'slim_oneliner', 'gain', 'points', 'slim_points',
             'quote', 'note', 'clash')


def card_modules(root):
    """CARDS 를 가진 생성기만. 목록을 박으면 대시보드가 늘 때마다 낡는다."""
    out = []
    for d in GEN_DIRS:
        for path in glob.glob(os.path.join(root, d, 'gen_*.py')):
            with io.open(path, encoding='utf-8', errors='replace') as f:
                if CARDS_RE.search(f.read()):
                    out.append((os.path.splitext(os.path.basename(path))[0], path))
    return sorted(out)


def load_cards(root, module):
    """import 오류를 삼키지 않는다. 삼키면 깨진 생성기가 빈 카드 목록으로 읽힌다.

    주의: scratchpad/gen_accountant_dashboard.py 는 import 시점에
    `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, ...)` 로 stdout
    객체 자체를 새 걸로 바꿔치기한다(다른 gen_*는 reconfigure()로 제자리
    수정만 한다). pytest 처럼 매 테스트마다 stdout 을 갈아 끼우는 도구
    안에서 이 모듈을 import 하면, 그 시점의 캡처 버퍼를 물고 있는 새
    TextIOWrapper 가 sys.stdout 자리에 눌러앉는다. 이후 그 버퍼가 닫히면
    나중 테스트의 print 가 전부 'I/O operation on closed file' 로 죽는다
    (insights/test_cards.py 의 all_cards 테스트가 열두 생성기를 한꺼번에
    import 하다 이걸 밟았다). all_cards/load_cards 를 테스트나 다른 도구
    안에서 부를 때는 이 모듈을 포함해 다수를 한 프로세스에 import 하는
    상황을 피하거나, 부르기 전에 sys.stdout 을 저장해뒀다가 복원한다.
    """
    for d in GEN_DIRS:
        p = os.path.join(root, d)
        if p not in sys.path:
            sys.path.insert(0, p)
    return list(getattr(importlib.import_module(module), 'CARDS', ()))


def all_cards(root):
    """대시보드 전부의 카드를 [(모듈, 카드), …] 로."""
    out = []
    for m, _ in card_modules(root):
        for c in load_cards(root, m):
            out.append((m, c))
    return out


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


def section_id(sec):
    """section 은 (id, …, 라벨) 튜플이다. 문자열로 와도 되고 없어도 된다."""
    return sec[0] if isinstance(sec, (list, tuple)) and sec else sec
