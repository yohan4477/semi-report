# -*- coding: utf-8 -*-
# 리소그래피 지도 재료 — 원문 코퍼스에서 이름마다 등장 횟수와 문서를 센다.
#
# 이름 사전(NAMES)과 나무(VIEWS)를 뗀다. 한 이름을 여러 뷰가 같이 쓴다 —
# 「거울·반사광학」은 부품 뷰의 잎이면서 기능 뷰에서는 EUV 아래 선다.
# 이름의 횟수는 뷰가 바뀌어도 같다. 사전에 없는 말은 만들지 않는다.
import io, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 이 공정 장의 이름표 — 생성기가 이것만 보고 페이지를 짓는다
KEY = 'litho'
LABEL = '리소그래피'
OUT_NAME = 'AI 인프라 지도 — 리소그래피.html'
SLUG = 'map-litho'

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
    'Hyper-NA': r'hyper[- ]?NA|하이퍼\s?NA',
    '멀티패터닝': r'멀티\s?패터닝|multi[- ]?patterning|SAQP|SADP|더블\s?패터닝',
    '패턴 셰이핑': r'pattern shaping|패턴\s?셰이핑',
    # DSA 약어는 딴 데서 다른 뜻으로 쓰여(희소 어텐션) 풀어 쓴 표기만 문다
    'DSA(자기조립 패터닝)': r'directed self[- ]?assembly|자기\s?조립\s?패터닝|block copolymer',
    '레일리 식': r'Rayleigh|레일리',
    '나노임프린트': r'나노임프린트|nanoimprint|\bNIL\b',
    # 기계 안 부품
    '주석 플라스마 광원': r'주석\s?플라스마|tin\s?droplet|\bLPP\b',
    '광원 출력': r'\d+\s?W source|source power|광원\s?출력',
    '거울·반사광학': r'다층\s?반사|multilayer mirror|반사경|\bmirrors?\b|거울',
    '아나모픽 광학': r'anamorphic|아나모픽',
    '진공': r'진공|vacuum',
    '트랙(코터·디벨로퍼)': r'resist track|코터|디벨로퍼|도포\s?현상',
    '포토마스크': r'포토마스크|photomask|레티클|reticle',
    '6x12 마스크': r'6\s?x\s?12[”"\s]*(?:inch)?\s*mask|6x12\s?마스크|6×12',
    '마스크 3D 효과': r'mask 3D|마스크\s?3D|\bM3D\b',
    '블랭크마스크': r'블랭크\s?마스크|blank\s?mask|\bHOYA\b|호야',
    '펠리클': r'펠리클|pellicle',
    '포토레지스트': r'포토레지스트|photoresist|감광액',
    '메탈옥사이드 레지스트': r'메탈\s?옥사이드|metal[- ]?oxide resist|Inpria|인프리아',
    '드라이 레지스트': r'dry resist|드라이\s?레지스트',
    '드라이 현상': r'dry develop|건식\s?현상',
    'CAR(화학증폭형) 레지스트': r'chemically amplified|화학\s?증폭',
    '레지스트 두께': r'resist thickness|레지스트\s?두께',
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
    '가장자리 어긋남(EPE)': r'edge placement error|\bEPE\b',
    'LER(선폭 거칠기)': r'\bLER\b|line edge roughness|line width roughness|\bLWR\b',
    '확률적 결함': r'stochastic|확률적\s?결함',
    '초점 심도': r'depth of focus|\bDOF\b|초점\s?심도',
    '수율': r'수율',
    '스루풋': r'스루풋|wafers? per hour|\bWPH\b|시간당 웨이퍼',
    '설치 대수': r'installed base|설치\s?기반|보유\s?대수',
    'EUV 레이어 수': r'EUV layers?|EUV\s?레이어|레이어\s?수',
    '패터닝 비용': r'패터닝\s?비용|cost per (?:layer|wafer)',
    '웨이퍼당 비용': r'cost per wafer|웨이퍼당\s?비용',
    '수출 통제': r'수출\s?통제|export control|엔티티\s?리스트|entity list',
}

# 뷰 = 같은 이름들을 다른 축으로 세운 나무.
# 가지 -> [이름] 또는 [(마디 이름, [자식 이름])]
VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇을 하나',
  'branches': [
    ('빛으로 새긴다', '파장이 짧을수록 가는 선을 새긴다', [
      ('EUV', ['High-NA EUV', 'Hyper-NA', 'EUV 다중 노광']),
      ('DUV', ['ArF 이머전', 'KrF']),
      '레일리 식',
    ]),
    ('해상도를 늘린다', '같은 빛으로 더 가늘게 — 여러 번 나눠 찍는다', [
      '멀티패터닝', '패턴 셰이핑', 'DSA(자기조립 패터닝)',
    ]),
    ('빛을 안 쓴다', '빛 대신 틀을 찍어 누른다', ['나노임프린트']),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '기계 안에 뭐가 드나',
  'branches': [
    ('빛을 만든다', '주석 방울에 레이저를 쏘아 플라스마로 만든다', [
      ('주석 플라스마 광원', ['광원 출력']),
    ]),
    ('빛을 모은다', '렌즈가 아니라 거울로 — 반사마다 힘이 준다', [
      ('거울·반사광학', ['High-NA EUV', '아나모픽 광학']),
      '진공',
    ]),
    ('무늬를 담는다', '새길 무늬를 담은 원판과 그 덮개', [
      ('포토마스크', ['6x12 마스크', '마스크 3D 효과', '블랭크마스크', '펠리클']),
    ]),
    ('웨이퍼에 바른다', '빛을 받아 녹거나 굳는 막을 입히고 굽는다', [
      ('포토레지스트', ['메탈옥사이드 레지스트', 'CAR(화학증폭형) 레지스트',
                    '드라이 레지스트', '레지스트 두께']),
      ('트랙(코터·디벨로퍼)', ['드라이 현상']),
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
      ('오버레이', ['가장자리 어긋남(EPE)']),
      ('수율', ['LER(선폭 거칠기)', '확률적 결함', '초점 심도']),
    ]),
    ('얼마나 빨리', '한 시간에 몇 장, 몇 대가 깔려 있나', [
      '스루풋', '설치 대수', 'EUV 레이어 수',
    ]),
    ('얼마인가', '한 층을 새기는 데 드는 값', ['패터닝 비용', '웨이퍼당 비용']),
    ('누가 못 사나', '기계를 살 수 있느냐가 기술만큼 세다', ['수출 통제']),
  ]},
]


# 리소그래피를 말하는 문서인지 보는 신호. 이 신호가 THRESHOLD 회 이상 나온 문서에서만
# 센다 — 「수율」·「거울」·「진공」 같은 흔한 말이 딴 문맥에서 부풀던 것을 막는다.
SIGNAL = re.compile(
    r'EUV|\bDUV\b|리소그래피|lithograph|노광|포토마스크|레티클|reticle|'
    r'포토레지스트|photoresist|극자외선', re.I)
THRESHOLD = 3
SENT_MAX = 3       # 잎 하나가 문서 하나에서 보여 줄 문장 수
SENT_CUT = 180     # 문장을 자르는 길이
WINDOW = 2         # 리소 신호를 찾는 앞뒤 줄 수


def proc_docs(signal, threshold, files=None):
    """그 공정을 말하는 문서만 고른다. 반환: ([(경로, 본문)], 전체 문서 수)"""
    if files is None:
        files = []
        for d in DIRS:
            for root, _, fs in os.walk(d):
                for f in fs:
                    if f.endswith('.md'):
                        files.append(os.path.join(root, f))
    out = []
    for p in files:
        try:
            t = io.open(p, encoding='utf-8').read()
        except Exception:
            continue
        if len(signal.findall(t)) >= threshold:
            out.append((p, t))
    return out, len(files)


def _sentence(line, m):
    """매치가 든 문장 한 도막 — 너무 길면 매치 언저리로 자른다."""
    s = line.strip()
    if len(s) <= SENT_CUT:
        return s
    i = m.start() - line.index(line.strip()[:1]) if line.strip() else m.start()
    a = max(0, i - SENT_CUT // 2)
    return ('…' if a else '') + s[a:a + SENT_CUT] + '…'


def count(names, signal, threshold, files=None):
    """이름마다 등장 횟수·문서·영수증 문장을 센다. 반환: (hits, 그 공정 문서 수, 전체 수)

    재는 법은 공정이 달라도 한 벌이다 — 문서 신호로 한 번, 줄 창으로 한 번 좁힌다.
    """
    docs, nall = proc_docs(signal, threshold, files)
    comp = [(n, re.compile(rx, re.I)) for n, rx in names.items()]
    hits = collections.defaultdict(lambda: {'n': 0, 'docs': []})
    for p, t in docs:
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        lines = t.split('\n')
        # 문서가 그 공정을 말해도 문장은 딴 얘기일 수 있다(리소 문서 안의 패키징 수율).
        # 그래서 줄 단위로도 본다 — 그 줄이나 앞뒤 두 줄에 신호가 있어야 센다.
        near = [bool(signal.search('\n'.join(lines[max(0, i - WINDOW):
                                                   i + WINDOW + 1])))
                for i in range(len(lines))]
        for n, rx in comp:
            cnt, sents = 0, []
            for i, line in enumerate(lines):
                if not near[i]:
                    continue
                m = rx.search(line)
                if not m:
                    continue
                cnt += len(rx.findall(line))
                if len(sents) < SENT_MAX:
                    sents.append([i + 1, _sentence(line, m)])
            if cnt:
                hits[n]['n'] += cnt
                hits[n]['docs'].append([rel, cnt, sents])
    for h in hits.values():
        h['docs'].sort(key=lambda x: -x[1])
    return hits, len(docs), nall


def scan_with(names, view_defs, signal, threshold):
    """뷰마다 나무를 세워 돌려준다. 잎의 숫자는 뷰가 달라도 같은 것을 본다.

    공정 모듈이 이름 사전과 나무만 넘기면 나머지는 이 한 벌이 한다.
    """
    hits, nlitho, nall = count(names, signal, threshold)

    def node(name):
        h = hits.get(name)
        if not h:
            return {'name': name, 'n': 0, 'ndoc': 0, 'top': [], 'kids': []}
        return {'name': name, 'n': h['n'], 'ndoc': len(h['docs']),
                'top': h['docs'][:6], 'kids': []}

    views = []
    for v in view_defs:
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
    return {'views': views, 'nlitho': nlitho, 'nall': nall}


def scan():
    return scan_with(NAMES, VIEWS, SIGNAL, THRESHOLD)


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
    print('리소 문서 %d / 전체 %d' % (out['nlitho'], out['nall']))
