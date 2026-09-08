# -*- coding: utf-8 -*-
# 패키징 지도 재료 — 원문 코퍼스에서 이름마다 등장 횟수·문서·영수증 문장을 센다.
# 재는 법은 map_litho 와 한 벌이다(문서 신호 + 줄 창). 다른 것은 이름과 나무뿐.
import os

from map_litho import count as _count, scan_with, ROOT  # noqa: F401
import re

KEY = 'packaging'
LABEL = '패키징'

# 패키징을 말하는 문서인지 보는 신호
SIGNAL = re.compile(
    r'패키징|packaging|CoWoS|\bHBM\d?\b|인터포저|interposer|칩렛|chiplet|'
    r'하이브리드\s?본딩|hybrid bond|\bTSV\b|\bEMIB\b|범프|bump', re.I)
THRESHOLD = 3

# 이름 -> 정규식. 별칭과 영문 표기를 함께 문다.
NAMES = {
    # 옆으로 잇는다 — 2.5D
    'CoWoS': r'CoWoS',
    'CoWoS-S/R/L': r'CoWoS[- ]?[SRL]\b',
    'InFO': r'\bInFO\b',
    'EMIB': r'\bEMIB\b',
    '팬아웃': r'팬\s?아웃|fan[- ]?out',
    # 위로 쌓는다 — 3D
    'SoIC': r'\bSoIC\b',
    'Foveros': r'Foveros',
    '하이브리드 본딩': r'하이브리드\s?본딩|hybrid bond',
    'TSV(실리콘 관통 전극)': r'\bTSV\b|실리콘\s?관통|through[- ]silicon',
    # 붙이는 법
    '마이크로범프': r'마이크로\s?범프|micro[- ]?bump|\bµbump\b',
    'TCB(열압착 본딩)': r'\bTCB\b|thermo[- ]?compression|열압착',
    '리플로우': r'리플로우|reflow',
    '언더필': r'언더필|underfill',
    # 받침과 배선
    '인터포저': r'인터포저|interposer',
    '패키지 기판(ABF)': r'\bABF\b|패키지\s?기판|package substrate|유기\s?기판',
    '유리기판': r'유리\s?기판|glass substrate|glass core',
    '패널 레벨 패키징': r'panel[- ]?level|패널\s?레벨|\bPLP\b',
    'RDL(재배선층)': r'\bRDL\b|재배선',
    'UCIe': r'UCIe',
    '칩렛': r'칩렛|chiplet',
    # 얹히는 것
    'HBM': r'\bHBM\d?\b',
    'HBM4': r'HBM4',
    '베이스 다이': r'베이스\s?다이|base die|로직\s?다이',
    # 열과 빛
    'CPO(광학 인터커넥트)': r'co[- ]?packaged optics|\bCPO\b|광학\s?인터커넥트',
    '마이크로플루이딕 냉각': r'마이크로\s?플루이딕|microfluidic',
    # 파는 곳
    'ASE': r'ASE\s?(?:Group|그룹)|\bASE\b(?=[^A-Za-z])',
    'Amkor': r'Amkor|앰코',
    'JCET': r'\bJCET\b',
    'Besi': r'\bBesi\b',
    'ASMPT': r'ASMPT|ASM Pacific',
    'Disco': r'\bDisco\b|디스코',
    'SKC·앱솔릭': r'앱솔릭|Absolics|\bSKC\b',
    # 재는 것
    '워피지(휨)': r'워피지|warpage|휨',
    '패키징 수율': r'패키징\s?수율|assembly yield',
    'KGD·번인 검사': r'\bKGD\b|known good die|번인|burn[- ]?in',
    'CoWoS 캐파': r'CoWoS\s?(?:캐파|capacity|생산\s?능력|증설)',
}

VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇을 하나',
  'branches': [
    ('옆으로 잇는다', '다이 여럿을 한 받침 위에 나란히 놓고 잇는다', [
      ('CoWoS', ['CoWoS-S/R/L', 'InFO']),
      'EMIB', '팬아웃',
    ]),
    ('위로 쌓는다', '다이를 겹쳐 붙여 거리를 없앤다', [
      ('하이브리드 본딩', ['SoIC', 'Foveros']),
      'TSV(실리콘 관통 전극)',
    ]),
    ('붙인다', '무엇으로 이어 붙이고 어떻게 굳히나', [
      ('마이크로범프', ['TCB(열압착 본딩)', '리플로우']),
      '언더필',
    ]),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '한 덩이 안에 뭐가 드나',
  'branches': [
    ('받침', '다이를 얹는 판 — 무엇으로 만드나', [
      ('인터포저', ['유리기판']),
      ('패키지 기판(ABF)', ['패널 레벨 패키징']),
    ]),
    ('배선', '다이와 다이를 잇는 길과 그 약속', [
      ('RDL(재배선층)', ['UCIe']),
      '칩렛',
    ]),
    ('얹히는 것', '연산 다이 옆에 무엇이 올라가나', [
      ('HBM', ['HBM4', '베이스 다이']),
    ]),
    ('열과 빛', '한 덩이가 커질수록 붙는 것', [
      'CPO(광학 인터커넥트)', '마이크로플루이딕 냉각',
    ]),
  ]},
 {'key': 'supply', 'label': '공급', 'hint': '누가 무엇을 파나',
  'branches': [
    ('조립(OSAT)', '남의 다이를 받아 한 덩이로 만드는 곳', [
      'ASE', 'Amkor', 'JCET',
    ]),
    ('장비', '붙이고 자르는 기계', ['Besi', 'ASMPT', 'Disco']),
    ('기판', '받침을 만드는 곳', ['SKC·앱솔릭']),
  ]},
 {'key': 'metric', 'label': '지표', 'hint': '무엇으로 재나',
  'branches': [
    ('얼마나 붙었나', '휘면 안 붙고, 하나가 죽으면 덩이가 죽는다', [
      '워피지(휨)', '패키징 수율', 'KGD·번인 검사',
    ]),
    ('얼마나 나오나', '자리가 모자라면 칩이 아니라 자리를 판다', ['CoWoS 캐파']),
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
                print('   %-22s n=%-5d docs=%d' % (nd['name'], nd['n'], nd['ndoc']))
                for kd in nd['kids']:
                    print('     └ %-18s n=%-5d docs=%d'
                          % (kd['name'], kd['n'], kd['ndoc']))
    print('%s 문서 %d / 전체 %d' % (LABEL, out['nlitho'], out['nall']))
