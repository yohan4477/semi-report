# -*- coding: utf-8 -*-
"""정책 어댑터 — 국가법령정보센터에서 **시행일자만** 받는다.

조문을 옮기지 않는다. 워치가 물어야 하는 것은 「그 법이 무슨 내용인가」가 아니라
「내가 본 뒤에 바뀌었나」이고, 그건 시행일자 하나로 정확히 갈린다. 내용은 바뀐 것이
확인됐을 때 사람이 읽는다.

계약은 watch_lib 머리에 있다. 여기서 지키는 것 넷.

1. **값이 아니라 판본이다.** 시행일자는 시계열이 아니라 판 표시다. series 를 안 만든다 —
   지어내면 도해가 뜻 없는 선을 그린다.
2. **법과 행정규칙은 다른 자리에서 온다.** 세제는 법률(target=law), LTV·DSR 은
   금융위 고시(target=admrul)다. 한 꼴로 합치지 않는다.
3. **수치를 여기서 안 뽑는다.** LTV·DSR 은 감독규정 별표 안의 표다. API 가 별표를
   글로 주긴 하지만 판형이 바뀌면 파싱이 깨진다 — 수치는 사람이 읽고 카드에 적는다.
4. **OC 는 발급받은 것을 쓴다.** 환경변수 LAW_OC. 없으면 문서에 적힌 공개 시험 계정으로
   도는데, 그건 파이프라인을 짜 보는 동안만 쓸 자리다(발급에 1~2일 심의가 걸린다).
"""
import os, json, urllib.request, urllib.parse

SEARCH = 'https://www.law.go.kr/DRF/lawSearch.do'
OC_ENV = 'LAW_OC'
DEMO_OC = 'test'


class AdapterError(Exception):
    pass


def _oc():
    return os.environ.get(OC_ENV) or DEMO_OC


def _search(target, query):
    p = {'OC': _oc(), 'target': target, 'type': 'JSON', 'query': query, 'display': '20'}
    u = SEARCH + '?' + urllib.parse.urlencode(p)
    with urllib.request.urlopen(u, timeout=30) as r:
        d = json.loads(r.read().decode('utf-8', 'replace'))
    root = list(d.values())[0] if d else {}
    if not isinstance(root, dict):
        raise AdapterError('응답 모양이 다르다: %s' % str(d)[:150])
    if 'result' in root:
        raise AdapterError('법령정보센터가 거절했다: %s' % root.get('result'))
    for k, v in root.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            return v
        if isinstance(v, dict) and ('법령명한글' in v or '행정규칙명' in v):
            return [v]
    return []


def _pick(items, name, target):
    """이름이 정확히 같은 것만 고른다. 「은행업감독규정」으로 찾으면
    상호저축은행업감독규정이 먼저 오기도 한다."""
    key = '법령명한글' if target == 'law' else '행정규칙명'
    exact = [i for i in items if str(i.get(key, '')).strip() == name]
    return exact[0] if exact else None


def fetch(target_name, area=None, laws=()):
    """laws = [(target, 법령·행정규칙 이름), …]. 이름마다 지금 시행일자를 준다.

    target 은 law(법률·시행령) 또는 admrul(행정규칙·고시)다."""
    out = {}
    for tgt, name in laws:
        items = _search(tgt, name)
        hit = _pick(items, name, tgt)
        if hit is None:
            continue
        eff = str(hit.get('시행일자') or hit.get('발령일자') or '')
        if len(eff) != 8:
            continue
        pretty = '%s-%s-%s' % (eff[:4], eff[4:6], eff[6:])
        out['law_' + name.replace(' ', '')] = {
            'value': pretty,
            'as_of': pretty,
            'kind': '공표',
            'unit': '시행일',
            'src': '국가법령정보센터 %s · %s · %s' % (
                tgt, name, hit.get('제개정구분명') or hit.get('행정규칙종류') or ''),
            'area': name, 'level': 'law',
            # 판본 표시라 시계열이 아니다. 도해도 안 선다
            'series': [], 'partial': False,
            'law_target': tgt,
            'law_id': str(hit.get('법령일련번호') or hit.get('행정규칙일련번호') or ''),
        }
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.environ.get(OC_ENV):
        print('경고: %s 가 없다 — 공개 시험 계정으로 돈다. 발급에 1~2일 심의가 걸린다\n'
              % OC_ENV)
    got = fetch('시험', laws=[
        ('law', '종합부동산세법'), ('law', '소득세법'), ('law', '지방세법'),
        ('law', '주택임대차보호법'), ('law', '부동산 거래신고 등에 관한 법률'),
        ('admrul', '은행업감독규정')])
    for k, v in sorted(got.items()):
        print('  %-28s %s  %s' % (k, v['value'], v['src']))
