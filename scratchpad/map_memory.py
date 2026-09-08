# -*- coding: utf-8 -*-
# 메모리 지도 재료. 재는 법은 map_litho 와 한 벌이다 — 다른 것은 이름과 나무뿐.
# 이 장만 공정이 아니라 제품이 축이다. 파는 물건이 층을 가르기 때문이다.
import re

from map_litho import scan_with  # noqa: F401

KEY = 'memory'
LABEL = '메모리'

SIGNAL = re.compile(
    r'\bHBM\d?\b|\bDRAM\b|디램|낸드|\bNAND\b|메모리|memory|하이닉스|마이크론|'
    r'\bDDR\d?\b|LPDDR', re.I)
THRESHOLD = 3

NAMES = {
    # 대역폭을 판다
    'HBM': r'\bHBM\d?\b',
    'HBM3E': r'HBM3E',
    'HBM4': r'HBM4',
    'HBM4E': r'HBM4E',
    '커스텀 HBM': r'커스텀\s?HBM|custom HBM',
    # 용량을 판다
    'DRAM': r'\bDRAM\b|디램',
    'DDR5': r'\bDDR5\b',
    'LPDDR': r'LPDDR',
    'GDDR': r'\bGDDR\d?\b',
    'SOCAMM': r'SOCAMM|소캠',
    'CXL': r'\bCXL\b',
    # 저장한다
    '낸드': r'낸드|\bNAND\b',
    'QLC': r'\bQLC\b',
    'eSSD': r'eSSD|엔터프라이즈\s?SSD',
    # 어떻게 쌓나
    'TSV(실리콘 관통 전극)': r'\bTSV\b|실리콘\s?관통',
    '하이브리드 본딩': r'하이브리드\s?본딩|hybrid bond',
    'MR-MUF': r'MR[- ]?MUF',
    '베이스 다이': r'베이스\s?다이|base die|로직\s?다이',
    # 파는 곳
    'SK하이닉스': r'SK\s?하이닉스|하이닉스|SK Hynix',
    '삼성전자': r'삼성전자|Samsung',
    '마이크론': r'마이크론|Micron',
    'CXMT': r'CXMT|창신',
    'YMTC': r'YMTC|양쯔메모리',
    '키오시아': r'키오시아|Kioxia',
    'SanDisk': r'SanDisk|샌디스크',
    # 재는 것
    '대역폭': r'대역폭|bandwidth',
    '용량': r'\d+\s?GB\b|용량\s?경쟁',
    '전력 효율(pJ/bit)': r'pJ/bit|피코줄',
    '설비투자(캐펙스)': r'캐펙스|\bcapex\b|설비\s?투자',
    '공급 계약': r'장기\s?공급|공급\s?계약|\bLTA\b',
    '인증 통과(퀄)': r'퀄\s?테스트|qualification|퀄리피케이션|인증\s?통과',
}

VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇을 파나',
  'branches': [
    ('대역폭을 판다', '연산 다이 옆에 붙어 초당 얼마를 넘기나', [
      ('HBM', ['HBM3E', 'HBM4', 'HBM4E', '커스텀 HBM']),
    ]),
    ('용량을 판다', '한 서버에 얼마를 얹나', [
      ('DRAM', ['DDR5', 'LPDDR', 'GDDR', 'SOCAMM']),
      'CXL',
    ]),
    ('저장한다', '전원을 꺼도 남는 것', [('낸드', ['QLC', 'eSSD'])]),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '한 스택 안에 뭐가 드나',
  'branches': [
    ('층을 잇는다', '다이를 겹쳐 놓고 위아래를 뚫어 잇는다', [
      ('TSV(실리콘 관통 전극)', ['하이브리드 본딩', 'MR-MUF']),
    ]),
    ('밑에 깔린다', '스택 맨 아래에서 연산 다이와 말을 맞추는 층', ['베이스 다이']),
  ]},
 {'key': 'supply', 'label': '공급', 'hint': '누가 무엇을 파나',
  'branches': [
    ('디램 3사', 'HBM 자리를 두고 겨루는 셋', [
      'SK하이닉스', '삼성전자', '마이크론',
    ]),
    ('중국', '통제 밖에서 같은 물건을 만들려는 곳', ['CXMT', 'YMTC']),
    ('낸드', '저장 쪽에서 파는 곳', ['키오시아', 'SanDisk']),
  ]},
 {'key': 'metric', 'label': '지표', 'hint': '무엇으로 재나',
  'branches': [
    ('얼마나 넘기나', '초당 몇 바이트, 그 바이트에 전기를 얼마나 쓰나', [
      '대역폭', '용량', '전력 효율(pJ/bit)',
    ]),
    ('얼마를 붓나', '짓는 데 드는 돈과 팔기로 한 약속', [
      '설비투자(캐펙스)', '공급 계약', '인증 통과(퀄)',
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
                print('   %-22s n=%-5d docs=%d' % (nd['name'], nd['n'], nd['ndoc']))
                for kd in nd['kids']:
                    print('     └ %-18s n=%-5d docs=%d'
                          % (kd['name'], kd['n'], kd['ndoc']))
    print('%s 문서 %d / 전체 %d' % (LABEL, out['nlitho'], out['nall']))
