# -*- coding: utf-8 -*-
# 리소그래피 마인드맵 재료 — 원문 코퍼스에서 후보어 빈도·등장 문서를 센다.
# 사전에 없는 말은 만들지 않는다. 결과는 scratchpad/litho_hits.json.
import io, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = [os.path.join(ROOT, 'content'), os.path.join(ROOT, 'input', 'clippings')]

# 가지 -> [(표시명, 정규식)]
TREE = [
 ('노광 방식', [
   ('EUV', r'EUV|극자외선'),
   ('High-NA EUV', r'High[- ]?NA|하이\s?NA'),
   ('DUV', r'\bDUV\b|심자외선'),
   ('ArF 이머전', r'이머전|immersion|ArFi'),
   ('KrF', r'\bKrF\b'),
   ('멀티패터닝', r'멀티\s?패터닝|multi[- ]?patterning|SAQP|SADP|더블\s?패터닝'),
   ('나노임프린트', r'나노임프린트|nanoimprint|\bNIL\b'),
 ]),
 ('장비사', [
   ('ASML', r'ASML|에이에스엠엘'),
   ('Canon', r'\bCanon\b|캐논'),
   ('Nikon', r'\bNikon\b|니콘'),
   ('SMEE', r'\bSMEE\b|상하이\s?마이크로'),
   ('도쿄일렉트론', r'Tokyo Electron|도쿄\s?일렉트론'),
   ('KLA', r'KLA[- ]?Tencor|\bKLA\b'),
 ]),
 ('광원·광학', [
   ('Cymer', r'\bCymer\b|사이머'),
   ('Trumpf', r'\bTrumpf\b|트룸프|트럼프사'),
   ('Zeiss', r'\bZeiss\b|자이스'),
   ('Ushio', r'\bUshio\b|우시오'),
   ('주석 플라스마 광원', r'주석\s?플라스마|tin\s?droplet|\bLPP\b'),
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
    'ASML': 'co', 'Canon': 'co', 'Nikon': 'co', 'SMEE': 'co',
    '도쿄일렉트론': 'co', 'KLA': 'co',
    'Cymer': 'co', 'Trumpf': 'co', 'Zeiss': 'co', 'Ushio': 'co',
    '주석 플라스마 광원': 'tech',
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
    comp = [(br, [(n, re.compile(rx, re.I)) for n, rx in ns]) for br, ns in TREE]
    hits = collections.defaultdict(lambda: {'n': 0, 'docs': []})
    for p in files:
        try:
            t = io.open(p, encoding='utf-8').read()
        except Exception:
            continue
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        for _br, ns in comp:
            for n, rx in ns:
                m = rx.findall(t)
                if m:
                    hits[n]['n'] += len(m)
                    hits[n]['docs'].append((rel, len(m)))
    out = {'branches': [], 'nfile': len(files)}
    for br, ns in TREE:
        nodes = []
        for n, _rx in ns:
            h = hits.get(n)
            k = KIND.get(n, 'tech')
            if not h:
                nodes.append({'name': n, 'n': 0, 'ndoc': 0, 'top': [], 'kind': k})
                continue
            h['docs'].sort(key=lambda x: -x[1])
            nodes.append({'name': n, 'n': h['n'], 'ndoc': len(h['docs']),
                          'top': h['docs'][:6], 'kind': k})
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
    print('files', out['nfile'])
