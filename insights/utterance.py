# -*- coding: utf-8 -*-
"""파일 하나에 딸린 시간 사실 — 쓴 날과 신선도 갈래. 본문은 안 읽는다.

쓴 날은 두 곳에서 온다. manifest.json 의 date 가 첫째고, 비어 있으면 파일 이름의
[YYMMDD] 나 YYYY-MM-DD 를 쓴다. 코퍼스 478편 중 매니페스트가 364편을 덮고
이름이 108편을 더 덮어 472편이 된다. 남은 6편은 쓴 날을 모르고, 그 줄은
times.json 에 안 들어간다 — 기준이 없으면 상대 표현도 시제도 못 푼다.

SECTION 은 판단이다. check_fresh 의 STALE_DAYS 는 biz·chip·model·power 넷인데
매니페스트의 categories 는 주제 폴더 이름이라 둘을 손으로 이어야 한다.
표를 여기 한 곳에 두고 코드는 표를 읽기만 한다.
"""
import glob
import io
import json
import os
import re

NAME_ISO = re.compile(r'(20\d{2})-(\d{2})-(\d{2})')
NAME_6 = re.compile(r'\[(\d{2})(\d{2})(\d{2})\]')
NAME_4 = re.compile(r'\[(\d{2})(\d{2})\]')
FM_PUBLISHED = re.compile(r'^published:\s*(\d{4}-\d{2}-\d{2})\s*$', re.M)
FM_CREATED = re.compile(r'^created:\s*(\d{4}-\d{2}-\d{2})\s*$', re.M)
JSON_DATE = re.compile(r'"date"\s*:\s*"(\d{4}-\d{2}-\d{2})"')
CLIPS = ('input/clippings/*.md', 'input/clippings/mer/*.json')

SECTION = {
    # 값과 물량 — 분기면 뒤집힌다
    'ai-infra/business': 'biz',
    '회계사': 'biz',
    '미국주식 사관학교': 'biz',
    '부동산': 'biz',
    # 칩 세대와 벤치마크
    'ai-infra/compute': 'chip',
    'ai-infra/memory': 'chip',
    'ai-infra/networking': 'chip',
    'semiconductor': 'chip',
    'semiconductors': 'chip',
    # 모델과 학습 기법
    'ai-models': 'model',
    'ai-models/agents': 'model',
    'ai-models/rl': 'model',
    'AI Engineer': 'model',
    '피지컬AI': 'model',
    'physical-ai': 'model',
    # 전력망과 건물 — 연 단위로 움직인다
    'ai-infra/power': 'power',
    'ai-infra/construction': 'power',
    'power': 'power',
    'oil-geopolitics': 'power',
    'oil-supplychain': 'power',
}


def name_date(rel):
    base = rel.rsplit('/', 1)[-1]
    m = NAME_ISO.search(base)
    if m:
        return '%s-%s-%s' % m.groups()
    m = NAME_6.search(base)
    if m:
        y, mo, d = m.groups()
        return '20%s-%s-%s' % (y, mo, d)
    m = NAME_4.search(base)
    if m:
        y, mo = m.groups()
        return '20%s-%s-01' % (y, mo)
    return ''


def clipping_date(root, rel):
    """클리핑의 쓴 날. 영문은 frontmatter, 메르는 JSON 의 date.

    JSON 을 통째로 파싱하지 않고 앞 2,000자만 정규식으로 본다. 메르 364편을
    조회 한 번마다 json.load 하면 2.8MB를 파싱하는데 date 키는 text 앞에 온다.
    """
    path = os.path.join(root, rel.replace('/', os.sep))
    if not os.path.isfile(path):
        return ''
    with io.open(path, encoding='utf-8', errors='replace') as f:
        head = f.read(2000)
    if rel.lower().endswith('.json'):
        m = JSON_DATE.search(head)
        return m.group(1) if m else ''
    m = FM_PUBLISHED.search(head) or FM_CREATED.search(head)
    return m.group(1) if m else ''


def section_for(categories):
    for c in (categories or []):
        if c in SECTION:
            return SECTION[c]
    return ''


def load(root, manifest_path=None):
    p = manifest_path or os.path.join(root, 'insights', 'manifest.json')
    with io.open(p, encoding='utf-8') as f:
        rows = json.load(f).get('sources') or []
    out = {}
    for s in rows:
        rel = str(s.get('path') or '')
        if not rel:
            continue
        out[rel] = {
            'date': str(s.get('date') or '') or name_date(rel),
            'section': section_for(s.get('categories')),
        }
    # 클리핑은 매니페스트에 없다. 갈래도 없어 기본 신선도(180일)로 떨어진다
    for pat in CLIPS:
        for q in glob.glob(os.path.join(root, pat.replace('/', os.sep))):
            rel = os.path.relpath(q, root).replace(os.sep, '/')
            if rel in out:
                continue
            out[rel] = {'date': clipping_date(root, rel), 'section': ''}
    return out


def date_of(meta, rel):
    m = meta.get(rel) or {}
    return m.get('date') or name_date(rel)


def section_of(meta, rel):
    return (meta.get(rel) or {}).get('section', '')
