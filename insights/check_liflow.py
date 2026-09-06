# -*- coding: utf-8 -*-
"""링크드인 흐름 장 검사기 — 인용한 게시물이 실재하나, 그 안에 그 숫자가 있나.

    PYTHONIOENCODING=utf-8 python insights/check_liflow.py

왜 따로 두나: 이 장의 인용은 줄 번호가 아니라 **게시물 식별자**(L-20260822-4337)다.
content/linkedin 은 게시 시각 오름차순으로만 쌓이므로 줄 번호도 안 밀리지만, 게시물을
가리키는 데는 식별자가 더 안전하다 — 기준일이 뉴스레터 발행일로 덮어써지는 글이 있어
날짜가 게시물 식별자가 아니다(insights/li_signal.py urn_date 주석).

표기 정규화가 이 검사기의 몸통이다. 사실표 546줄을 검증하면서 걸린 여섯 줄이 전부
지어낸 값이 아니라 표기 차이였다(2026-09-06).

    𝟔.𝟏𝟒 · 𝟗𝟑𝟎        링크드인이 유니코드 굵은 숫자로 쓴다        → NFKC
    43만 2천 → 432,000  우리가 아라비아로 편다                     → 만·억 전개
    128k → 128,000      영어 원문의 k·B 접미사                     → 접미사 전개
    석 달 → 3개월        한글 수사                                 → 수사 표
    다섯 배 → 5배        본문이 한국어로 쓴다                       → 수사 표

정규화를 안 하면 멀쩡한 인용을 물고, 정규화가 과하면 진짜 지어낸 값을 놓친다.
그래서 정규화는 **양쪽에 똑같이** 걸고, 본문 숫자가 그 게시물 안에 있는지만 본다.
"""
import io
import os
import re
import sys
import glob
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOWS = os.path.join(ROOT, 'insights', 'li_flows')
CLIPS = os.path.join(ROOT, 'content', 'linkedin')

LEN_MIN, LEN_MAX = 5500, 6500
SEC_MIN, SEC_MAX = 5, 7
LAST_SEC = '말하지 않은 것'

# 한글 수사 — 본문은 「다섯 배」로 쓰고 원문은 「5배」로 적는다
SINO = {'영': '0', '일': '1', '이': '2', '삼': '3', '사': '4',
        '오': '5', '육': '6', '칠': '7', '팔': '8', '구': '9', '십': '10'}
NATIVE = {'한': '1', '두': '2', '세': '3', '네': '4', '다섯': '5', '여섯': '6',
          '일곱': '7', '여덟': '8', '아홉': '9', '열': '10', '스무': '20',
          '하나': '1', '둘': '2', '셋': '3', '넷': '4', '석': '3', '넉': '4'}


def normalize(s):
    """양쪽에 똑같이 거는 정규화. 숫자로 읽을 수 있는 것을 전부 아라비아로 편다."""
    s = unicodedata.normalize('NFKC', s)          # 𝟔.𝟏𝟒 → 6.14, ％ → %
    s = s.replace(',', '').replace(' ', '')
    # 한글 수사 + 단위. 「다섯 배」「석 달」「열흘」은 안 건드린다(단위가 붙은 것만)
    for w, d in sorted(NATIVE.items(), key=lambda kv: -len(kv[0])):
        s = re.sub(w + r'(?=(?:배|개|곳|건|번|달|년|주|가지|배가|배로|배씩))', d, s)
    # 만·억·조 전개 — 43만2천 → 432000, 4880억 → 488000000000 은 과하다.
    # 원문도 「43만 2천」으로 쓰므로 숫자+단위를 붙인 꼴로만 맞춘다
    s = re.sub(r'(\d+)만(\d+)천', lambda m: str(int(m.group(1)) * 10000 + int(m.group(2)) * 1000), s)
    s = re.sub(r'(\d+)만', lambda m: str(int(m.group(1)) * 10000), s)
    # 영어 접미사 — 128k → 128000, 1.25B/1.6T 는 배수가 커서 원 표기도 함께 남긴다
    s = re.sub(r'(\d+(?:\.\d+)?)k\b', lambda m: str(int(float(m.group(1)) * 1000)), s, flags=re.I)
    return s


NUM = re.compile(r'\d[\d.]*')
CITE = re.compile(r'\(((?:L-\d{8}-\d+)(?:\s*·\s*L-\d{8}-\d+)*)\)')
HEAD = re.compile(r'^## (L-\d{8}-\d+) ·', re.M)


def posts():
    """게시물 식별자 -> 그 게시물 덩어리 전문(정규화 전)."""
    out = {}
    for path in sorted(glob.glob(os.path.join(CLIPS, '*.md'))):
        txt = io.open(path, encoding='utf-8').read()
        heads = list(HEAD.finditer(txt))
        for i, m in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(txt)
            out[m.group(1)] = txt[m.start():end]
    return out


def sentences(body):
    """인용이 붙은 문장만.

    **자르는 자리가 이 함수의 전부다.** 인용은 마침표 앞에 온다(「…낸다 (L-…).」)
    이라 「다.」로만 자르면 문장이 안 잘리고, 한 문단이 통째로 한 문장이 되어 옆
    문장의 숫자를 끌어와 멀쩡한 인용을 문다(2026-09-06, FAIL 24건 중 22건이 이것).
    소수점(2.5배)에는 뒤에 공백이 없으므로 「마침표+공백」으로 자르면 안 깨진다.
    """
    body = re.sub(r'\[\[fig:[A-Z]+\]\]', '', body)
    for para in body.split('\n'):
        para = para.strip()
        if not para or para.startswith('#'):
            continue
        for sent in re.split(r'\.\s+|\.$', para):
            if CITE.search(sent):
                yield sent


def check(path):
    fails, warns = [], []
    txt = io.open(path, encoding='utf-8').read()
    body = txt.split('---', 2)[2] if txt.startswith('---') else txt
    name = os.path.basename(path)
    P = posts()

    # F1 길이
    plain = re.sub(r'\(L-[\d-]+(?:\s*·\s*L-[\d-]+)*\)', '', re.sub(r'\[\[fig:[A-Z]+\]\]', '', body))
    n = len(plain.strip())
    if not LEN_MIN <= n <= LEN_MAX:
        fails.append('F1 길이 %d자 — %d~%d자여야 한다' % (n, LEN_MIN, LEN_MAX))

    # F2 절 수와 마지막 절
    secs = re.findall(r'^## (.+)$', body, re.M)
    if not SEC_MIN <= len(secs) <= SEC_MAX:
        fails.append('F2 절 %d개 — %d~%d개여야 한다' % (len(secs), SEC_MIN, SEC_MAX))
    if secs and LAST_SEC not in secs[-1]:
        fails.append('F2 마지막 절이 「%s」이 아니다 — %s' % (LAST_SEC, secs[-1]))

    # F3 인용한 게시물이 실재하나
    cited = set()
    for m in CITE.finditer(body):
        for pid in re.findall(r'L-\d{8}-\d+', m.group(1)):
            cited.add(pid)
            if pid not in P:
                fails.append('F3 없는 게시물을 인용했다 — %s' % pid)

    # F4 그 문장의 숫자가 그 게시물 안에 있나
    checked = 0
    for sent in sentences(body):
        # 한 문장에 인용이 둘일 수 있다(「…됐고 (L-A), 8월 21일 … (L-B)」). 앞의 것만
        # 보면 뒤 인용이 받치는 숫자를 앞 게시물에서 찾다가 헛물을 켠다(2026-09-06)
        ids = re.findall(r'L-\d{8}-\d+', ' '.join(m.group(1) for m in CITE.finditer(sent)))
        blob = normalize(' '.join(P.get(i, '') for i in ids))
        text = normalize(CITE.sub('', sent))
        for tok in set(NUM.findall(text)):
            if len(tok) < 2 and tok in '0123456789':   # 한 자리 숫자는 우연 일치가 많다
                continue
            checked += 1
            if tok.rstrip('.') not in blob:
                fails.append('F4 %s — 「%s」가 게시물에 없다  · %s'
                             % (','.join(ids), tok, text[:52]))

    # F5 도해 열쇠가 하나 이상
    figs = re.findall(r'\[\[fig:([A-Z]+)\]\]', body)
    if not figs:
        fails.append('F5 도해가 없다')

    print('== %s' % name)
    print('   %d자 · 절 %d · 도해 %d · 인용 게시물 %d · 숫자 대조 %d건'
          % (n, len(secs), len(figs), len(cited), checked))
    for f in fails:
        print('   FAIL ' + f)
    for w in warns:
        print('   WARN ' + w)
    return len(fails)


def main():
    paths = sorted(glob.glob(os.path.join(FLOWS, '*.md')))
    if not paths:
        print('링크드인 흐름 글이 없다: %s' % FLOWS)
        return 0
    bad = sum(check(p) for p in paths)
    print('\nFAIL %d' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
