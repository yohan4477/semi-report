# -*- coding: utf-8 -*-
# 증착·식각 지도 재료. 재는 법은 map_litho 와 한 벌이다 — 다른 것은 이름과 나무뿐.
import re

from map_litho import scan_with  # noqa: F401

KEY = 'etch'
LABEL = '증착·식각'

# 이 공정을 말하는 문서인지 보는 신호
SIGNAL = re.compile(
    r'증착|deposition|식각|etch|\bALD\b|\bCVD\b|\bPVD\b|\bCMP\b|전공정|'
    r'\bGAA\b|나노시트|배선|interconnect', re.I)
THRESHOLD = 3

NAMES = {
    # 쌓는다
    '증착': r'증착|deposition',
    'ALD(원자층 증착)': r'\bALD\b|원자층\s?증착|atomic layer deposit',
    'CVD(화학 기상 증착)': r'\bCVD\b|화학\s?기상\s?증착',
    'PVD(물리 기상 증착)': r'\bPVD\b|물리\s?기상\s?증착|스퍼터',
    '에피택시': r'에피택시|epitax|\bEPI\b',
    # 깎는다
    '식각': r'식각|dry etch|plasma etch',
    '고종횡비 식각': r'고종횡비|high aspect ratio|\bHAR\b',
    'CMP(화학기계 연마)': r'\bCMP\b|화학적\s?기계\s?연마|화학기계연마',
    # 다듬는다
    '세정': r'세정|웨이퍼\s?클리닝|wet clean',
    '열처리·어닐': r'어닐|anneal|급속\s?열처리|\bRTP\b',
    '이온주입': r'이온\s?주입|implant',
    # 무엇을 만드나
    'GAA(나노시트 트랜지스터)': r'\bGAA\b|게이트\s?올\s?어라운드|gate[- ]all[- ]around|나노시트',
    '백사이드 전력공급': r'백사이드|backside power|\bBSPDN\b',
    # 배선 금속
    '구리 배선(다마신)': r'구리\s?배선|copper interconnect|다마신|damascene',
    '텅스텐 배선': r'텅스텐|tungsten',
    '몰리브덴 배선': r'몰리브덴|molybdenum',
    '루테늄 배선': r'루테늄|ruthenium',
    # 소재
    '전구체': r'전구체|precursor',
    '특수가스': r'특수\s?가스|specialty gas|육불화|\bNF3\b',
    # 파는 곳
    '램리서치': r'Lam Research|램\s?리서치',
    '어플라이드머티리얼즈': r'Applied Materials|어플라이드\s?머티리얼|\bAMAT\b',
    '도쿄일렉트론': r'Tokyo Electron|도쿄\s?일렉트론',
    'ASM International': r'ASM International|\bASMI\b',
    'KLA': r'KLA[- ]?Tencor|\bKLA\b',
    'Naura': r'Naura|나우라',
    'AMEC': r'\bAMEC\b|중미반도체',
    # 재는 것
    '공정 스텝 수': r'공정\s?스텝|process steps|스텝\s?수',
    '낸드 적층 단수': r'\d+\s?단\s?낸드|낸드\s?적층|layer count|단수\s?경쟁',
    '장비 국산화': r'국산화|localiz',
    '수출 통제': r'수출\s?통제|export control|엔티티\s?리스트|entity list',
}

VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇을 하나',
  'branches': [
    ('쌓는다', '웨이퍼 위에 막을 한 겹씩 올린다', [
      ('증착', ['ALD(원자층 증착)', 'CVD(화학 기상 증착)', 'PVD(물리 기상 증착)']),
      '에피택시',
    ]),
    ('깎는다', '새긴 무늬대로 파고 다시 평평하게 만든다', [
      ('식각', ['고종횡비 식각']),
      'CMP(화학기계 연마)',
    ]),
    ('다듬는다', '씻고 굽고 불순물을 심는다', ['세정', '열처리·어닐', '이온주입']),
    ('무엇을 만드나', '이 공정들이 모여 나오는 구조', [
      'GAA(나노시트 트랜지스터)', '백사이드 전력공급',
    ]),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '무엇을 쌓고 무엇으로 하나',
  'branches': [
    ('배선 금속', '층과 층을 잇는 선을 무엇으로 만드나', [
      ('구리 배선(다마신)', ['텅스텐 배선', '몰리브덴 배선', '루테늄 배선']),
    ]),
    ('공정 소재', '기계에 넣는 것', ['전구체', '특수가스']),
  ]},
 {'key': 'supply', 'label': '공급', 'hint': '누가 무엇을 파나',
  'branches': [
    ('식각·증착 장비', '전공정 장비를 파는 곳', [
      '램리서치', '어플라이드머티리얼즈', '도쿄일렉트론', 'ASM International',
    ]),
    ('검사 장비', '깎은 결과를 보는 곳', ['KLA']),
    ('중국 장비', '통제 밖에서 같은 자리를 채우려는 곳', ['Naura', 'AMEC']),
  ]},
 {'key': 'metric', 'label': '지표', 'hint': '무엇으로 재나',
  'branches': [
    ('몇 번 도나', '층이 늘수록 같은 기계를 몇 번 더 지난다', [
      '공정 스텝 수', '낸드 적층 단수',
    ]),
    ('누가 못 사나', '기계를 살 수 있느냐가 기술만큼 세다', [
      '수출 통제', '장비 국산화',
    ]),
  ]},
]


def scan():
    return scan_with(NAMES, VIEWS, SIGNAL, THRESHOLD)


if __name__ == '__main__':
    out = scan()
    for v in out['views']:
        print('== %s (%s)' % (v['label'], v['hint']))
        for b in v['branches']:
            print(' #', b['name'])
            for nd in b['nodes']:
                print('   %-24s n=%-5d docs=%d' % (nd['name'], nd['n'], nd['ndoc']))
                for kd in nd['kids']:
                    print('     └ %-20s n=%-5d docs=%d'
                          % (kd['name'], kd['n'], kd['ndoc']))
    print('%s 문서 %d / 전체 %d' % (LABEL, out['nlitho'], out['nall']))
