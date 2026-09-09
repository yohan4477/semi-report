# -*- coding: utf-8 -*-
"""도해 설명이 본문과 갈리나 — 판 위는 번호, 캡션은 그 번호 풀이.

2026-09-09 전수 조사에서 나온 것: 도해 설명이 본문을 되풀이하는 것이 사고가 아니라
기본값이었다. 겹침률 0.17 이상 222쌍 중 217쌍이 겹쳤고, 문턱 아래 40쌍을 뽑아 봐도
27쌍이 겹쳤다. 원인은 캡션을 본문과 같은 말투의 산문으로 썼다는 데 있다 — 같은 꼴이면
같은 말을 쓰게 되고, 읽는 사람은 어디까지가 도해 설명인지 모른다.

그래서 캡션의 꼴을 바꾼다. **판 위에는 값 라벨만 남기고 설명이 붙을 자리에 ①②③ 만
얹는다. 캡션은 그 번호 풀이만 적는다.** 번호에 안 딸린 문장은 캡션에 두지 않는다.
그러면 본문이 한 말이 캡션에 들어갈 자리가 없어진다.

  PYTHONIOENCODING=utf-8 python insights/check_figdup.py
  PYTHONIOENCODING=utf-8 python insights/check_figdup.py --selftest   규칙이 결함을 무나

  G1  판에 얹은 번호를 캡션이 다 푸나                FAIL
  G2  캡션의 번호가 판에 실제로 있나                 FAIL
  G3  캡션이 번호 풀이와 출처 말고 산문을 담았나       FAIL
  G4  캡션이 이웃 본문 문단과 겹치나                 FAIL

FAIL 은 게이트에 올린 장(`STRICT`)에서만 난다. 나머지 장은 줄을 안 뱉고 **빚**으로
장별 한 줄만 센다 — `check_struct` 와 같은 꼴이다. 693종을 한꺼번에 고칠 수 없고,
안 읽히는 경고를 693줄 흘리면 규칙이 죽는다.
"""
import collections
import glob
import html as htmllib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8',
                       line_buffering=True)

# 게이트로 세운 장. 여기 없는 장은 빚으로만 센다.
# 2026-09-09 에 빈 채로 연다 — 전수 조사에서 693종 중 208종이 이미 어긋나 있어서,
# 올릴 장은 그 장의 캡션을 번호 꼴로 옮긴 뒤에 하나씩 넣는다.
STRICT = ()

# 이 장은 규칙이 아예 안 맞아 세지도 않는다.
SKIP = {}

CIRCLE = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'
FIGURE = re.compile(r'<figure\b.*?</figure>', re.S)
CAPTION = re.compile(r'<figcaption\b[^>]*>(.*?)</figcaption>', re.S)
PARA = re.compile(r'<p\b[^>]*>(.*?)</p>', re.S)
TAG = re.compile(r'<[^>]+>')
SVG = re.compile(r'<svg\b.*?</svg>', re.S)
# 출처 — 괄호 안에 원문 줄 주소가 든 것(전력-260526 L55·L561)
SOURCE = re.compile(r'\([^()]*L\d+[^()]*\)')
# 겹침을 잴 만큼 긴 캡션. 이보다 짧으면 되풀이할 것도 없다
MIN_CAP = 40
# 겹침률 문턱. 전수 조사에서 이 위는 사실상 전부 겹쳤다
COV = 0.17

rows = []
debt = collections.Counter()


def add(where, code, msg):
    """게이트에 올린 장은 FAIL, 나머지 장은 빚으로 한 줄만 센다."""
    for chapter, skip in SKIP.items():
        if where.startswith(chapter) and code in skip:
            return
    if where.startswith(STRICT):
        rows.append(('FAIL', where, code, msg))
    else:
        debt[(where.split(' · ')[0], code)] += 1


def txt(s):
    """태그를 떼고 글자만. 빈칸으로 바꾼다 — 지우면 두 줄이 붙어 한 낱말이 된다."""
    return re.sub(r'\s+', ' ', htmllib.unescape(TAG.sub(' ', s or ''))).strip()


def circles(s):
    return set(c for c in (s or '') if c in CIRCLE)


def grams(s):
    """네 글자 조각. 낱말을 안 자르고 재려면 형태소가 필요한데, 겹침은 조각으로 충분하다."""
    s = re.sub(r'[^가-힣0-9A-Za-z%]', '', s or '')
    return set(s[i:i + 4] for i in range(len(s) - 3))


def coverage(cap, para):
    """캡션 조각 중 본문이 되풀이한 몫. 본문이 길어도 값이 안 커지도록 캡션으로 나눈다."""
    a, b = grams(cap), grams(para)
    return len(a & b) / len(a) if a and b else 0.0


def lead_prose(cap):
    """번호에 안 딸린 산문. 첫 번호 앞을 보고, 출처 괄호는 뗀다."""
    head = cap
    for i, ch in enumerate(cap):
        if ch in CIRCLE:
            head = cap[:i]
            break
    return re.sub(r'[\s·,.]+', '', SOURCE.sub('', head))


def check_figure(where, fig, before, after):
    """도해 하나를 본다. 판(plate)은 캡션을 뺀 나머지."""
    m = CAPTION.search(fig)
    if not m:
        return
    cap = txt(m.group(1))
    plate = txt(CAPTION.sub(' ', fig))
    pn, cn = circles(plate), circles(cap)

    for c in sorted(pn - cn):
        add(where, 'G1', '판에 얹은 %s 를 캡션이 안 푼다' % c)
    for c in sorted(cn - pn):
        add(where, 'G2', '캡션이 푸는 %s 가 판에 없다' % c)

    if len(cap) >= MIN_CAP:
        head = lead_prose(cap)
        if not pn:
            add(where, 'G3', '판에 번호가 없고 캡션이 산문 %d자다 — 설명이 붙을 '
                             '자리에 번호를 얹고 캡션은 그 풀이만 적는다' % len(cap))
        elif len(head) >= 20:
            add(where, 'G3', '번호에 안 딸린 산문이 캡션 머리에 %d자 있다' % len(head))

        for para in list(before) + list(after):
            cov = coverage(cap, para)
            if cov >= COV:
                add(where, 'G4', '캡션이 이웃 본문과 겹친다(겹침률 %.2f) — "%s…"'
                    % (cov, cap[:30]))
                break


def scan(html, where):
    paras = [(a.start(), a.end(), txt(a.group(1))) for a in PARA.finditer(html)]
    for fm in FIGURE.finditer(html):
        before = [t for a, b, t in paras if b <= fm.start() and len(t) > 60][-2:]
        after = [t for a, b, t in paras if a >= fm.end() and len(t) > 60][:2]
        check_figure(where, fm.group(0), before, after)


def selftest():
    """규칙이 결함을 실제로 무나. 세우기만 하고 안 물면 규칙이 아니라 장식이다."""
    global rows, debt, STRICT
    cases = [
        ('G1', '<figure><svg><text>①</text><text>②</text></svg>'
               '<figcaption>① 왼쪽이 발표치다. 이 캡션은 두 번째 번호를 빠뜨렸고 '
               '길이는 마흔 자를 넘긴다.</figcaption></figure>'),
        ('G2', '<figure><svg><text>①</text></svg>'
               '<figcaption>① 왼쪽이 발표치다. ② 판에 없는 번호를 풀었고 길이는 '
               '마흔 자를 넘긴다.</figcaption></figure>'),
        ('G3', '<figure><svg><text>50메가와트</text></svg>'
               '<figcaption>높이는 아끼는 전력에 비례합니다. 왼쪽이 발표치이고 '
               '오른쪽이 계산입니다. 번호가 하나도 없는 산문입니다.</figcaption>'
               '</figure>'),
        ('G4', '<figure><svg><text>①</text></svg><figcaption>① 두 값이 다른데 '
               '원문은 이 둘이 일치한다고 적습니다. 어느 쪽이 맞는지 원문만으로는 '
               '알 수 없어 맞추지 않고 둘 다 그렸습니다.</figcaption></figure>'
               '<p>두 값이 다른데 원문은 이 둘이 일치한다고 적는다. 어느 쪽이 맞는지 '
               '원문만으로는 알 수 없어 둘 다 적는다. 앞부분은 약 5퍼센트라고 적는데 '
               '뒤의 계산은 6.9퍼센트로 나온다.</p>'),
    ]
    clean = ('<figure><svg><text>①</text><text>50메가와트</text></svg>'
             '<figcaption>① 엔비디아 발표치입니다(전력-260526 L55).</figcaption>'
             '</figure><p>앞부분은 1기가와트 시설에서 약 5퍼센트를 아낀다고 적는데, '
             '뒤의 단계별 계산은 4단계에서 69메가와트로 나온다. 본문은 이 둘이 '
             '일치한다고 서술한다.</p>')
    bad = 0
    for code, markup in cases:
        rows, debt = [], collections.Counter()
        STRICT = ('t.html',)
        scan(markup, 't.html')
        got = set(r[2] for r in rows)
        ok = code in got
        print('%s %s · 실제로 난 것: %s'
              % ('문다  ' if ok else '못 문다', code, sorted(got) or '없음'), file=OUT)
        bad += 0 if ok else 1
    rows, debt = [], collections.Counter()
    scan(clean, 't.html')
    got = sorted(set(r[2] for r in rows))
    print('%s 성한 도해 · 난 것: %s'
          % ('안 문다' if not got else '헛문다', got or '없음'), file=OUT)
    bad += 1 if got else 0
    print('\n요약: 규칙 %d개 중 %d개가 제 몫을 못 한다' % (len(cases) + 1, bad),
          file=OUT)
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    want = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else ''
    n = 0
    for p in sorted(glob.glob(os.path.join(paths.ROOT, '대시보드', '**', '*.html'),
                              recursive=True)):
        where = os.path.relpath(p, os.path.join(paths.ROOT, '대시보드'))
        if want and want not in where:
            continue
        html = io.open(p, encoding='utf-8').read()
        if '<figcaption' not in html:
            continue
        n += len(FIGURE.findall(html))
        scan(html, where)
    for kind, at, code, msg in rows:
        print('%s %s [%s] %s' % (kind, at, code, msg), file=OUT)
    fail = sum(1 for r in rows if r[0] == 'FAIL')
    if debt:
        print(file=OUT)
        print('빚 — 게이트에 안 올린 장. 그 장의 캡션을 번호 꼴로 옮길 때 함께 갚는다',
              file=OUT)
        by = collections.defaultdict(list)
        for (where, code), cnt in sorted(debt.items()):
            by[where].append('%s %d' % (code, cnt))
        order = sorted(by, key=lambda w: -sum(int(x.split()[1]) for x in by[w]))
        for where in order[:20]:
            print('  %-46s %s' % (where[:44], ' · '.join(by[where])), file=OUT)
        if len(by) > 20:
            print('  … 그 밖 %d장' % (len(by) - 20), file=OUT)
    print('\n요약: 도해 %d개 / FAIL %d / 빚 %d건'
          % (n, fail, sum(debt.values())), file=OUT)
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
