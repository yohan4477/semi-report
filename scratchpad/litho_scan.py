# -*- coding: utf-8 -*-
# 리소그래피 지도 재료 — 원문 코퍼스에서 이름마다 등장 횟수와 문서를 센다.
#
# 이름 사전(NAMES)과 나무(VIEWS)를 뗀다. 한 이름을 여러 뷰가 같이 쓴다 —
# 「거울·반사광학」은 부품 뷰의 잎이면서 기능 뷰에서는 EUV 아래 선다.
# 이름의 횟수는 뷰가 바뀌어도 같다. 사전에 없는 말은 만들지 않는다.
import io, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = [os.path.join(ROOT, 'content'), os.path.join(ROOT, 'input', 'clippings')]

# 이름 -> 정규식. 별칭과 영문 표기를 함께 문다.
NAMES = {
    # 노광 방식
    'EUV': r'EUV|극자외선',
    'High-NA EUV': r'High[- ]?NA|하이\s?NA',
    'EUV 다중 노광': r'EUV\s?더블|double\s?patterning',
    'DUV': r'\bDUV\b|심자외선',
    'ArF 이머전': r'이머전|immersion|ArFi',
    'KrF': r'\bKrF\b',
    '멀티패터닝': r'멀티\s?패터닝|multi[- ]?patterning|SAQP|SADP|더블\s?패터닝',
    '패턴 셰이핑': r'pattern shaping|패턴\s?셰이핑',
    '나노임프린트': r'나노임프린트|nanoimprint|\bNIL\b',
    # 기계 안 부품
    '주석 플라스마 광원': r'주석\s?플라스마|tin\s?droplet|\bLPP\b',
    '거울·반사광학': r'다층\s?반사|multilayer mirror|반사경|\bmirrors?\b|거울',
    '진공': r'진공|vacuum',
    '트랙(코터·디벨로퍼)': r'resist track|코터|디벨로퍼|도포\s?현상',
    '포토마스크': r'포토마스크|photomask|레티클|reticle',
    '블랭크마스크': r'블랭크\s?마스크|blank\s?mask|\bHOYA\b|호야',
    '펠리클': r'펠리클|pellicle',
    '포토레지스트': r'포토레지스트|photoresist|감광액',
    '메탈옥사이드 레지스트': r'메탈\s?옥사이드|metal[- ]?oxide resist|Inpria|인프리아',
    '드라이 레지스트': r'dry resist|드라이\s?레지스트',
    # 파는 곳
    'ASML': r'ASML|에이에스엠엘',
    'Canon': r'\bCanon\b|캐논',
    'Nikon': r'\bNikon\b|니콘',
    'SMEE': r'\bSMEE\b|상하이\s?마이크로',
    '도쿄일렉트론': r'Tokyo Electron|도쿄\s?일렉트론',
    'KLA': r'KLA[- ]?Tencor|\bKLA\b',
    'Zeiss': r'\bZeiss\b|자이스',
    'Ushio': r'\bUshio\b|우시오',
    'JSR': r'\bJSR\b',
    '도쿄오카(TOK)': r'Tokyo Ohka|도쿄\s?오카',
    '신에쓰': r'신에쓰|Shin[- ]?Etsu',
    'SUMCO': r'\bSUMCO\b|섬코',
    # 재는 것
    '오버레이': r'오버레이|overlay',
    '수율': r'수율',
    '스루풋': r'스루풋|wafers? per hour|\bWPH\b|시간당 웨이퍼',
    '패터닝 비용': r'패터닝\s?비용|cost per (?:layer|wafer)',
    '수출 통제': r'수출\s?통제|export control|엔티티\s?리스트|entity list',
}

# 뷰 = 같은 이름들을 다른 축으로 세운 나무.
# 가지 -> [이름] 또는 [(마디 이름, [자식 이름])]
VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇을 하나',
  'branches': [
    ('빛으로 새긴다', '파장이 짧을수록 가는 선을 새긴다', [
      ('EUV', ['High-NA EUV', 'EUV 다중 노광']),
      ('DUV', ['ArF 이머전', 'KrF']),
    ]),
    ('해상도를 늘린다', '같은 빛으로 더 가늘게 — 여러 번 나눠 찍는다', [
      '멀티패터닝', '패턴 셰이핑',
    ]),
    ('빛을 안 쓴다', '빛 대신 틀을 찍어 누른다', ['나노임프린트']),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '기계 안에 뭐가 드나',
  'branches': [
    ('빛을 만든다', '주석 방울에 레이저를 쏘아 플라스마로 만든다', [
      '주석 플라스마 광원',
    ]),
    ('빛을 모은다', '렌즈가 아니라 거울로 — 반사마다 힘이 준다', [
      ('거울·반사광학', ['High-NA EUV']),
      '진공',
    ]),
    ('무늬를 담는다', '새길 무늬를 담은 원판과 그 덮개', [
      ('포토마스크', ['블랭크마스크', '펠리클']),
    ]),
    ('웨이퍼에 바른다', '빛을 받아 녹거나 굳는 막을 입히고 굽는다', [
      ('포토레지스트', ['메탈옥사이드 레지스트', '드라이 레지스트']),
      '트랙(코터·디벨로퍼)',
    ]),
  ]},
 {'key': 'supply', 'label': '공급', 'hint': '누가 무엇을 파나',
  'branches': [
    ('노광기', '기계를 통째로 파는 넷', [
      ('ASML', ['Zeiss']),
      'Canon', 'Nikon', 'SMEE',
    ]),
    ('주변 장비', '노광 앞뒤에 붙는 기계', [
      ('도쿄일렉트론', ['트랙(코터·디벨로퍼)']),
      'KLA', 'Ushio',
    ]),
    ('소재', '웨이퍼와 그 위에 바르는 것', [
      'JSR', '도쿄오카(TOK)', '신에쓰', 'SUMCO',
    ]),
  ]},
 {'key': 'metric', 'label': '지표', 'hint': '무엇으로 재나',
  'branches': [
    ('얼마나 맞았나', '층과 층이 어긋난 정도, 살아남은 칩의 몫', [
      '오버레이', '수율',
    ]),
    ('얼마나 빨리', '한 시간에 몇 장', ['스루풋']),
    ('얼마인가', '한 층을 새기는 데 드는 값', ['패터닝 비용']),
    ('누가 못 사나', '기계를 살 수 있느냐가 기술만큼 세다', ['수출 통제']),
  ]},
]


def count(files=None):
    """이름마다 등장 횟수와 문서를 센다. 반환: (hits, 파일 수)"""
    if files is None:
        files = []
        for d in DIRS:
            for root, _, fs in os.walk(d):
                for f in fs:
                    if f.endswith('.md'):
                        files.append(os.path.join(root, f))
    comp = [(n, re.compile(rx, re.I)) for n, rx in NAMES.items()]
    hits = collections.defaultdict(lambda: {'n': 0, 'docs': []})
    for p in files:
        try:
            t = io.open(p, encoding='utf-8').read()
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        for n, rx in comp:
            m = rx.findall(t)
            if m:
                hits[n]['n'] += len(m)
                hits[n]['docs'].append((rel, len(m)))
    for h in hits.values():
        h['docs'].sort(key=lambda x: -x[1])
    return hits, len(files)


def scan():
    """뷰마다 나무를 세워 돌려준다. 잎의 숫자는 뷰가 달라도 같은 것을 본다."""
    hits, nfile = count()

    def node(name):
        h = hits.get(name)
        if not h:
            return {'name': name, 'n': 0, 'ndoc': 0, 'top': [], 'kids': []}
        return {'name': name, 'n': h['n'], 'ndoc': len(h['docs']),
                'top': h['docs'][:6], 'kids': []}

    views = []
    for v in VIEWS:
        branches = []
        for bname, bnote, items in v['branches']:
            nodes = []
            for it in items:
                if isinstance(it, tuple):
                    nd = node(it[0])
                    nd['kids'] = [node(k) for k in it[1]]
                else:
                    nd = node(it)
                nodes.append(nd)
            branches.append({'name': bname, 'note': bnote, 'nodes': nodes})
        views.append({'key': v['key'], 'label': v['label'], 'hint': v['hint'],
                      'branches': branches})
    return {'views': views, 'nfile': nfile}


if __name__ == '__main__':
    out = scan()
    io.open(os.path.join(ROOT, 'scratchpad', 'litho_hits.json'), 'w',
            encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    for v in out['views']:
        print('== %s (%s)' % (v['label'], v['hint']))
        for b in v['branches']:
            print(' #', b['name'])
            for nd in b['nodes']:
                print('   %-20s n=%-5d docs=%d' % (nd['name'], nd['n'], nd['ndoc']))
                for kd in nd['kids']:
                    print('     └ %-16s n=%-5d docs=%d'
                          % (kd['name'], kd['n'], kd['ndoc']))
    print('files', out['nfile'])
