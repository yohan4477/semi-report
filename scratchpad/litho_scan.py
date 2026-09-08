# -*- coding: utf-8 -*-
# 리소그래피 마인드맵 재료 — 원문 코퍼스에서 후보어 빈도·등장 문서를 센다.
# 사전에 없는 말은 만들지 않는다. 결과는 scratchpad/litho_hits.json.
import io, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = [os.path.join(ROOT, 'content'), os.path.join(ROOT, 'input', 'clippings')]

# 가지 -> [(표시명, 정규식)] 또는 [(표시명, 정규식, [(자식, 정규식), …])]
# 마디도 자기 정규식으로 센다 — 자식 합이 아니다. EUV 342회 안에 High-NA 101회가
# 이미 들어 있어 합쳐 세면 거짓 숫자가 된다.
TREE = [
 ('빛으로 새긴다', [
   ('EUV', r'EUV|극자외선', [
     ('High-NA EUV', r'High[- ]?NA|하이\s?NA'),
     ('EUV 다중 노광', r'EUV\s?더블|double\s?patterning'),
   ]),
   ('DUV', r'\bDUV\b|심자외선', [
     ('ArF 이머전', r'이머전|immersion|ArFi'),
     ('KrF', r'\bKrF\b'),
   ]),
 ]),
 ('해상도를 늘린다', [
   ('멀티패터닝', r'멀티\s?패터닝|multi[- ]?patterning|SAQP|SADP|더블\s?패터닝'),
 ]),
 ('빛을 안 쓴다', [
   ('나노임프린트', r'나노임프린트|nanoimprint|\bNIL\b'),
 ]),
 # 장비를 파는 곳이 마디, 그 기계 안에 든 것이 잎이다. 원문에 없는 이름은 안 세운다 —
 # Cymer·Trumpf 는 코퍼스에 0회라 이 가지에서 뺐다.
 ('장비', [
   ('ASML', r'ASML|에이에스엠엘', [
     ('주석 플라스마 광원', r'주석\s?플라스마|tin\s?droplet|\bLPP\b'),
     ('거울·반사광학', r'다층\s?반사|multilayer mirror|반사경|\bmirrors?\b|거울'),
     ('진공', r'진공|vacuum'),
     ('Zeiss', r'\bZeiss\b|자이스'),
   ]),
   ('Canon', r'\bCanon\b|캐논'),
   ('Nikon', r'\bNikon\b|니콘'),
   ('SMEE', r'\bSMEE\b|상하이\s?마이크로'),
   ('도쿄일렉트론', r'Tokyo Electron|도쿄\s?일렉트론', [
     ('트랙(코터·디벨로퍼)', r'resist track|코터|디벨로퍼|도포\s?현상'),
   ]),
   ('KLA', r'KLA[- ]?Tencor|\bKLA\b'),
   ('Ushio', r'\bUshio\b|우시오'),
 ]),
 ('소재', [
   ('포토레지스트', r'포토레지스트|photoresist|감광액'),
   ('메탈옥사이드 레지스트', r'메탈\s?옥사이드|metal[- ]?oxide resist|Inpria|인프리아'),
   ('JSR', r'\bJSR\b'),
   ('도쿄오카(TOK)', r'Tokyo Ohka|도쿄\s?오카'),
   ('신에쓰', r'신에쓰|Shin[- ]?Etsu'),
   ('SUMCO', r'\bSUMCO\b|섬코'),
 ]),
 ('마스크·펠리클', [
   ('포토마스크', r'포토마스크|photomask|레티클|reticle'),
   ('블랭크마스크', r'블랭크\s?마스크|blank\s?mask|\bHOYA\b|호야'),
   ('펠리클', r'펠리클|pellicle'),
 ]),
 ('계측·수율·통제', [
   ('오버레이', r'오버레이|overlay'),
   ('수율', r'수율'),
   ('스루풋', r'스루풋|wafers? per hour|\bWPH\b|시간당 웨이퍼'),
   ('패터닝 비용', r'패터닝\s?비용|cost per (?:layer|wafer)'),
   ('수출 통제', r'수출\s?통제|export control|엔티티\s?리스트|entity list'),
 ]),
]


# 잎의 갈래 — 기술(무엇을 하는가) · 회사(누가 만드나) · 지표(얼마나 맞았나, 누가 못 사나).
# 지도 위 칩 줄이 이 갈래로 잎을 거른다.
KIND = {
    'EUV': 'tech', 'High-NA EUV': 'tech', 'DUV': 'tech', 'ArF 이머전': 'tech',
    'KrF': 'tech', '멀티패터닝': 'tech', '나노임프린트': 'tech',
    'EUV 다중 노광': 'tech',
    'ASML': 'co', 'Canon': 'co', 'Nikon': 'co', 'SMEE': 'co',
    '도쿄일렉트론': 'co', 'KLA': 'co',
    'Zeiss': 'co', 'Ushio': 'co',
    '주석 플라스마 광원': 'tech', '거울·반사광학': 'tech', '진공': 'tech',
    '트랙(코터·디벨로퍼)': 'tech',
    '포토레지스트': 'tech', '메탈옥사이드 레지스트': 'tech',
    'JSR': 'co', '도쿄오카(TOK)': 'co', '신에쓰': 'co', 'SUMCO': 'co',
    '포토마스크': 'tech', '블랭크마스크': 'tech', '펠리클': 'tech',
    '오버레이': 'idx', '수율': 'idx', '스루풋': 'idx', '패터닝 비용': 'idx',
    '수출 통제': 'idx',
}
KIND_LABEL = {'tech': '기술', 'co': '회사', 'idx': '지표·제도'}


def scan():
    files = []
    for d in DIRS:
        for root, _, fs in os.walk(d):
            for f in fs:
                if f.endswith('.md'):
                    files.append(os.path.join(root, f))
    # 마디와 그 자식을 한 벌로 편다 — 세는 자리에서는 층이 없다
    flat = []
    for _br, ns in TREE:
        for item in ns:
            flat.append((item[0], re.compile(item[1], re.I)))
            for kid in (item[2] if len(item) > 2 else []):
                flat.append((kid[0], re.compile(kid[1], re.I)))
    hits = collections.defaultdict(lambda: {'n': 0, 'docs': []})
    for p in files:
        try:
            t = io.open(p, encoding='utf-8').read()
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        for n, rx in flat:
            m = rx.findall(t)
            if m:
                hits[n]['n'] += len(m)
                hits[n]['docs'].append((rel, len(m)))

    def node_of(name):
        h = hits.get(name)
        k = KIND.get(name, 'tech')
        if not h:
            return {'name': name, 'n': 0, 'ndoc': 0, 'top': [], 'kind': k, 'kids': []}
        h['docs'].sort(key=lambda x: -x[1])
        return {'name': name, 'n': h['n'], 'ndoc': len(h['docs']),
                'top': h['docs'][:6], 'kind': k, 'kids': []}

    out = {'branches': [], 'nfile': len(files)}
    for br, ns in TREE:
        nodes = []
        for item in ns:
            nd = node_of(item[0])
            nd['kids'] = [node_of(kid[0]) for kid in (item[2] if len(item) > 2 else [])]
            nodes.append(nd)
        out['branches'].append({'name': br, 'nodes': nodes})
    return out


if __name__ == '__main__':
    out = scan()
    io.open(os.path.join(ROOT, 'scratchpad', 'litho_hits.json'), 'w',
            encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
    for b in out['branches']:
        print('#', b['name'])
        for nd in b['nodes']:
            print('  %-20s %-4s n=%-5d docs=%d'
                  % (nd['name'], KIND_LABEL[nd['kind']], nd['n'], nd['ndoc']))
            for kid in nd['kids']:
                print('    └ %-16s %-4s n=%-5d docs=%d'
                      % (kid['name'], KIND_LABEL[kid['kind']], kid['n'], kid['ndoc']))
    print('files', out['nfile'])
