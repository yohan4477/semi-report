# -*- coding: utf-8 -*-
"""모델을 세울 만한 원문을 찾는다. 검사기가 아니라 재료 찾기 도구다.

모델이 서려면 셋이 있어야 한다.

  ① 규칙   수식이나 「이렇게 계산한다」는 서술
  ② 입력   그 수식에 넣을 값
  ③ 출력   맞는지 견줄 발표치

셋 다 있으면 재현이 되고, ①과 ②만 있으면 확장만 된다(지연 모델이 그 꼴이다).
가려진 칸이 많으면 ②가 없어 못 한다 — SemiAnalysis 는 자재비 표를 검게 지우고
그 모델을 따로 판다.

    PYTHONIOENCODING=utf-8 python scripts/find_models.py
    PYTHONIOENCODING=utf-8 python scripts/find_models.py --all
"""
import io
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLIP = os.path.join(ROOT, 'input', 'clippings')
TRIAGE = os.path.join(ROOT, 'input', 'clip-images-triage.json')

URL = re.compile(r'https?://\S+')
CODE = re.compile(r'`[^`]*`')
# 진짜 수식 — 왼쪽에 이름, 오른쪽에 계산. URL 질의와 코드 조각을 걷은 뒤 센다
FORMULA = re.compile(r'(?<![\w?&=])[A-Za-z_Ͱ-Ͽ][\wͰ-Ͽ]{1,}\s*='
                     r'\s*[^=\n]{6,}')
# 계산 규칙을 말로 적은 자리
RULE = re.compile(r'(we (?:model|assume|estimate|calculate|derive)|is calculated as'
                  r'|is defined as|attach (?:rate|ratio)|calculator|methodology'
                  r'|levelized|amortiz|per (?:GPU|chip|rack|server|token|watt|kW))', re.I)
# 단위가 붙은 값 — 입력이 있다는 표지
UNIT = re.compile(r'\$[\d,]+|\d+\s?(?:kW|MW|GW|kWh|W/m|TB|PB|GB/s|Gbit|tok/s|ms)\b'
                  r'|\d+(?:\.\d+)?%')
# 발표된 출력이 있다는 표지
OUTPUT = re.compile(r'(table below|the table|we (?:find|see|calculate) that|results in'
                    r'|comes out to|works out to|총|합계)', re.I)
# 가려질 위험 — 자재비·원가 분해 표를 파는 자리
REDACT = re.compile(r'(bill of material|BoM|cost breakdown|our .{0,20}model[,.]|'
                    r'semianalysis\.com/[a-z-]*model)', re.I)


def scan(path):
    raw = io.open(path, encoding='utf-8', errors='ignore').read()
    t = CODE.sub(' ', URL.sub(' ', raw))
    return {
        'formula': len(FORMULA.findall(t)),
        'rule': len(RULE.findall(t)),
        'unit': len(UNIT.findall(t)),
        'output': len(OUTPUT.findall(t)),
        'redact': len(REDACT.findall(t)),
        'chars': len(t),
        'sample': [m.group(0)[:70].replace('\n', ' ')
                   for m in list(FORMULA.finditer(t))[:2]],
    }


def score(s, tables):
    """규칙·입력·출력이 다 있나. 가려질 위험은 뺀다."""
    rule = min(s['formula'] * 3 + s['rule'], 40)
    inp = min(s['unit'] / 4.0, 30)
    out = min(s['output'] * 2 + tables * 2, 30)
    return rule + inp + out - min(s['redact'] * 2.0, 20)


def main():
    show_all = '--all' in sys.argv
    tabs = Counter()
    if os.path.exists(TRIAGE):
        for r in json.loads(io.open(TRIAGE, encoding='utf-8').read()):
            if r['kind'] == '표후보':
                tabs[r['clip']] += 1

    rows = []
    for name in sorted(os.listdir(CLIP)):
        if not name.endswith('.md'):
            continue
        stem = name[:-3]
        s = scan(os.path.join(CLIP, name))
        rows.append((score(s, tabs.get(stem, 0)), s, tabs.get(stem, 0), stem))
    rows.sort(key=lambda r: -r[0])

    print('점수 = 규칙 + 입력 + 출력 − 가려질 위험. 100 점 만점이 아니라 견주는 눈금이다.')
    print()
    print('%5s %4s %4s %4s %4s %4s  %s'
          % ('점수', '수식', '규칙', '단위', '출력', '표', '클리핑'))
    for sc, s, nt, stem in (rows if show_all else rows[:25]):
        print('%5.0f %4d %4d %4d %4d %4d  %s'
              % (sc, s['formula'], s['rule'], min(s['unit'], 999), s['output'],
                 nt, stem[:64]))
        for ex in s['sample']:
            print('%29s %s' % ('', ex))
    print()
    print('클리핑 %d편 · 표 후보가 있는 편 %d' % (len(rows), sum(1 for r in rows if r[2])))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
