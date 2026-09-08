# -*- coding: utf-8 -*-
# 네트워킹 지도 재료. 재는 법은 map_litho 와 한 벌이다 — 다른 것은 이름과 나무뿐.
# 칩을 만드는 장이 아니라 칩과 칩을 잇는 장이다.
import re

from map_litho import scan_with  # noqa: F401

KEY = 'network'
LABEL = '네트워킹'

SIGNAL = re.compile(
    r'네트워[킹크]|이더넷|Ethernet|InfiniBand|인피니밴드|NVLink|스위치|switch|'
    r'트랜시버|transceiver|광\s?모듈|optics|스케일\s?[업아]|\bPCIe\b|대역폭', re.I)
THRESHOLD = 3

NAMES = {
    # 무엇으로 잇나 — 규격
    '이더넷': r'이더넷|Ethernet',
    'Ultra Ethernet': r'Ultra Ethernet|\bUEC\b',
    '인피니밴드': r'인피니밴드|InfiniBand',
    'NVLink': r'NVLink|엔브이링크',
    'NVSwitch': r'NVSwitch',
    'UALink': r'UALink',
    'PCIe': r'\bPCIe\b',
    'RDMA·RoCE': r'\bRDMA\b|\bRoCE\b',
    # 어디를 잇나
    '스케일업': r'스케일\s?업|scale[- ]?up',
    '스케일아웃': r'스케일\s?아웃|scale[- ]?out',
    '토폴로지(팻트리)': r'팻\s?트리|fat[- ]?tree|토폴로지|topology',
    # 무엇이 그 길에 놓이나
    '스위치 ASIC': r'스위치\s?ASIC|Tomahawk|Jericho|Spectrum',
    '광트랜시버': r'트랜시버|transceiver|\bOSFP\b|QSFP',
    '실리콘 포토닉스': r'실리콘\s?포토닉스|silicon photonics',
    'CPO(광학 동봉)': r'co[- ]?packaged optics|\bCPO\b',
    'LPO·LRO': r'\bLPO\b|\bLRO\b|linear pluggable',
    'DSP(리타이머)': r'리타이머|retimer',
    'AEC(액티브 구리)': r'\bAEC\b|액티브\s?구리|active copper',
    'DAC(구리 케이블)': r'\bDAC\b|다이렉트\s?어태치',
    # 파는 곳
    'Broadcom': r'Broadcom|브로드컴',
    'Marvell': r'Marvell|마벨',
    'Astera Labs': r'Astera',
    'Credo': r'Credo|크레도',
    'Arista': r'Arista|아리스타',
    'Cisco': r'Cisco|시스코',
    'Coherent': r'Coherent\b|코히어런트',
    'Innolight': r'Innolight|이노라이트',
    'Eoptolink': r'Eoptolink',
    # 재는 것
    '레인 속도(112G·224G)': r'112G|224G|\d+\s?Gbps per lane|레인당',
    '포트 수·기수': r'포트\s?수|radix|기수',
    '지연(레이턴시)': r'레이턴시|latency|지연\s?시간',
}

VIEWS = [
 {'key': 'func', 'label': '기능', 'hint': '무엇으로 어디를 잇나',
  'branches': [
    ('한 상자 안을 잇는다', '가까운 GPU 끼리 — 스케일업', [
      ('NVLink', ['NVSwitch']),
      'UALink', 'PCIe',
    ]),
    ('상자 밖을 잇는다', '랙과 랙, 홀과 홀 — 스케일아웃', [
      ('이더넷', ['Ultra Ethernet', 'RDMA·RoCE']),
      '인피니밴드',
    ]),
    ('어떻게 얽나', '몇 단으로 어떻게 엮느냐가 값과 지연을 정한다', [
      '토폴로지(팻트리)', '스케일업', '스케일아웃',
    ]),
  ]},
 {'key': 'part', 'label': '부품', 'hint': '그 길에 무엇이 놓이나',
  'branches': [
    ('어디로 보낼지 정한다', '들어온 것을 어느 포트로 내보낼지 고르는 칩', ['스위치 ASIC']),
    ('빛으로 보낸다', '전기를 빛으로 바꿔 먼 데까지', [
      ('광트랜시버', ['실리콘 포토닉스', 'CPO(광학 동봉)', 'LPO·LRO']),
    ]),
    ('구리로 보낸다', '가까운 데는 구리가 싸고 덜 먹는다', [
      ('DAC(구리 케이블)', ['AEC(액티브 구리)', 'DSP(리타이머)']),
    ]),
  ]},
 {'key': 'supply', 'label': '공급', 'hint': '누가 무엇을 파나',
  'branches': [
    ('칩', '스위치와 그 언저리 칩을 파는 곳', [
      'Broadcom', 'Marvell', 'Astera Labs', 'Credo',
    ]),
    ('장비', '상자로 파는 곳', ['Arista', 'Cisco']),
    ('광 모듈', '빛으로 바꾸는 부품을 파는 곳', [
      'Coherent', 'Innolight', 'Eoptolink',
    ]),
  ]},
 {'key': 'metric', 'label': '지표', 'hint': '무엇으로 재나',
  'branches': [
    ('얼마나 굵나', '한 가닥이 초당 얼마를 넘기고 한 상자에 몇 개가 붙나', [
      '레인 속도(112G·224G)', '포트 수·기수',
    ]),
    ('얼마나 늦나', '멀리 갈수록 기다리는 시간이 붙는다', ['지연(레이턴시)']),
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
