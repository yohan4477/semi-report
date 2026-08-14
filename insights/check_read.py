# -*- coding: utf-8 -*-
"""읽히는가 검사 — 문체가 아니라 뜻이 통하는지를 본다.

check_prose 는 금지어·문장 길이·번역투를 본다. 그런데 그걸 다 통과하고도
못 알아듣는 글이 나왔다(AMD 편: "값은 붙었고", "두 리스크"가 무엇인지 없음).
그래서 세 가지를 따로 본다.

  R1  설명 없는 약어 — 제품명이 아닌 약어를 첫 등장에 괄호로 풀지 않았다
  R2  가리키기만 한 표현 — "두 문제", "이 셋"이라 해 놓고 무엇인지 안 밝혔다
  R3  제목이 비유다 — 무엇에 관한 글인지 제목만 보고 알 수 없다

  py -3.13 insights/check_read.py
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_lib as nl
import paths

# 굳이 풀 필요 없는 것들 — 일상어에 가깝다
OK_ABBR = {'AI', 'GPU', 'CPU', 'API', 'IT', 'PC', 'TV', 'GDP', 'ETF', 'IPO', 'PER',
           'PR', 'CEO', 'CI', 'KB', 'MB', 'GB', 'TB', 'MW', 'GW', 'KW'}
# 회사·서비스 이름은 뜻을 푸는 대상이 아니라 이름이다
OK_NAME = {'AMD', 'AWS', 'IBM', 'TSMC', 'SK', 'LG', 'ASML', 'BMW', 'NVIDIA', 'ARM',
           'OpenAI', 'DeepSeek', 'SpaceX', 'PyTorch', 'GPT', 'ROCm', 'CoreWeave',
           'InferenceMAX', 'InferenceX', 'Helios', 'Rubin', 'Trainium', 'Bedrock'}
# 제품·회사 이름은 약어가 아니라 이름이다(GB200, MI455X, H100, N3, V4, TPUv7 …)
NAME = re.compile(r'^(?:[A-Z]{1,4}\d{1,4}[A-Za-z0-9]{0,4}|[A-Z][a-z]+[A-Za-z]*\d*|[A-Z]{2,4}v\d)$')
ABBR = re.compile(r'\b([A-Z][A-Za-z0-9]{1,7})\b')
LINE_REF = re.compile(r'^L\d+$')

# "두 문제"라 해 놓고 무엇인지 안 밝히면 독자는 그 자리에서 막힌다
POINTER = re.compile(r'(두 (?:리스크|문제|가지|축|요인|갈래)|세 (?:가지|요소|답|축|갈래)'
                     r'|네 (?:가지|축|층)|이 (?:둘|셋|넷)|그 (?:둘|셋)'
                     r'|경쟁 제품|해당 제품|양쪽|후자|전자)')
ENUM = re.compile(r'(하나는|첫째|둘째|①|②|—|·|:|\n-)')

# 영어를 그대로 옮겨 굳은 말들 — 우리말로 풀어 쓴다(오른쪽이 권장)
LITERAL = {'함대': 'GPU 물량 전체', '모트': '진입 장벽', '풋프린트': '설치 규모',
           '랜드스케이프': '판도', '에코시스템': '생태계', '런레이트': '연환산 매출',
           '오프테이크': '장기 구매 계약', '백스톱': '최소 매출 보증',
           '리레이팅': '값을 다시 매기는 것', '스택': '층 또는 소프트웨어 묶음'}


# 제목에 쓰면 무슨 말인지 모르는 압축 표현
VAGUE = ['붙었', '갈랐', '갈린 자리', '뒤집힌다', '남는다', '돌아온다', '옮겨간다',
         '협상력', '경쟁력', '역량', '구조적', '패러다임', '지형']

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def strip(text):
    """인용과 표 구분선을 걷어낸다 — 검사 대상은 사람이 읽는 문장이다"""
    text = nl.CITE.sub('', text)
    text = re.sub(r'\(\[\d{6}\][^()]*\)', '', text)   # 줄번호 없는 출처 표기도 문장이 아니다
    return re.sub(r'^\|[-: |]+\|$', '', text, flags=re.M)


def check_file(path):
    where = os.path.basename(path)
    raw = io.open(path, encoding='utf-8').read()
    meta, mdbody = nl.parse_front(raw)
    body = strip(mdbody)   # frontmatter 의 파일 경로에 든 약어까지 잡히면 안 된다

    seen = set()
    for m in ABBR.finditer(body):
        a = m.group(1)
        if a in OK_ABBR or a in OK_NAME or a in seen or NAME.match(a) or LINE_REF.match(a):
            continue
        seen.add(a)
        # 두 가지 다 인정한다 — "HGX(…)"처럼 뒤에 뜻을 붙인 것과
        # "강화학습(RL, …)"처럼 우리말을 앞에 두고 괄호 안에 약어를 넣은 것
        tail = body[m.end():m.end() + 60]
        inside = body[:m.start()].rstrip().endswith('(')
        if not inside and '(' not in tail.split('.')[0].split('다 ')[0]:
            add('FAIL', where, 'R1', '약어 "%s" 를 첫 등장에 안 풀었다 — %s(뜻) 형태로' % (a, a))

    for m in POINTER.finditer(body):
        if not ENUM.search(body[m.end():m.end() + 240]):
            add('FAIL', where, 'R2', '"%s" 라고만 하고 무엇인지 안 밝혔다' % m.group(1))

    for w, alt in LITERAL.items():
        if w in body:
            add('FAIL', where, 'R4', '직역 표현 "%s" — 우리말로 쓴다(예: %s)' % (w, alt))

    head = (meta.get('headline') or '')
    for v in VAGUE:
        i = head.find(v)
        if i < 0:
            continue
        # "엔비디아 상대 협상력"처럼 누구를 상대로 한 것인지 앞에 붙었으면 뜻이 통한다
        before = head[max(0, i - 14):i]
        if re.search(r'(상대|와의|과의|대비|앞에서|사이)\s*$', before):
            continue
        add('WARN', where, 'R3',
            '제목에 뜻이 흐린 표현 "%s" — 무엇에 대한 것인지 앞에 붙인다: %s' % (v, head))


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    files = sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md')) +
                   glob.glob(os.path.join(paths.SYNTH, '*.md')))
    for p in files:
        check_file(p)
    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    print('\n요약: 글 %d편 / FAIL %d / WARN %d' % (len(files), fails, len(findings) - fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
