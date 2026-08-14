# -*- coding: utf-8 -*-
"""인용한 줄에 그 숫자가 실제로 있는지 대조한다.

브리핑을 노트만 보고 쓰다 사고가 났다. 노트가 두 사실을 한 줄에 붙여 놓은 것을
그대로 옮겨 원인이 바뀌었고(케이블 → 리타이머), 68,928달러의 정체도 달라졌다.
노트는 찾아가는 길이지 근거가 아니다. 그래서 문장의 숫자를 인용한 원문 줄과 맞춰 본다.

기계가 잡는 것은 절반이다. 숫자가 그 줄에 있어도 뜻이 다를 수 있다.
나머지 절반은 사람이 원문 줄을 열어 확인해야 한다.

  py -3.13 insights/check_cite.py
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_lib as nl
import paths

NUM = re.compile(r'(?<![A-Za-z0-9])\d[\d,\.]*')   # L423 같은 줄 번호는 본문 숫자가 아니다
SKIP = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '100'}
NEAR = 2          # 인용 줄 위아래 이 정도는 같은 대목으로 본다
findings = []


def norm(t):
    return re.sub(r'[\s,]', '', t)


def lines_of(path):
    p = nl.abspath(path)
    if not os.path.isfile(p):
        return None
    return io.open(p, encoding='utf-8', errors='replace').read().split('\n')


def sentences(body):
    """인용이 붙은 문장 단위로 자른다 — 그 문장의 숫자를 그 인용과 맞춘다"""
    out = []
    for chunk in re.split(r'\n(?=[-|#])|(?<=[.!?])\s', body):
        if nl.CITE.search(chunk):
            out.append(chunk)
    return out


BARE = re.compile(r'\((L\d+(?:,\s*L\d+)*)\)')


def check(path, src):
    where = os.path.basename(path)
    body = nl.parse_front(io.open(path, encoding='utf-8').read())[1]
    cache, last = {}, None
    for sent in sentences(body):
        refs = [r for r in nl.cite_refs(sent, src) if r['ok'] and r['lines']]
        if refs:
            last = refs[-1]['file']
        # "(L256)"처럼 파일 없이 줄만 적은 인용은 바로 앞 문서를 가리킨다
        for m in BARE.finditer(sent):
            if last:
                refs.append({'file': last, 'lines': [int(x) for x in re.findall(r'L(\d+)', m.group(1))],
                             'ok': True, 'label': ''})
        if not refs:
            continue
        pool = ''
        for r in refs:
            if r['file'] not in cache:
                cache[r['file']] = lines_of(r['file'])
            ls = cache[r['file']]
            if ls is None:
                continue
            for n in r['lines']:
                lo, hi = max(0, n - 1 - NEAR), min(len(ls), n + NEAR)
                pool += norm(' '.join(ls[lo:hi]))
        if not pool:
            continue
        plain = nl.CITE.sub('', re.sub(r'<[^>]+>', '', sent))
        plain = re.sub(r'L\d+', '', plain)          # 줄 번호는 본문 숫자가 아니다
        plain = re.sub(r'\[\d{6}\]', '', plain)         # 출처 표기의 날짜도 아니다
        # 영문 원문은 달러를 그대로 쓰고 우리는 억·조로 환산한다. 그 자리는 기계가 못 맞춘다
        money = re.search(r'\$|billion|million', pool) is not None
        for v in set(NUM.findall(plain)):
            if v in SKIP or len(norm(v).replace('.', '')) < 2:
                continue
            if re.fullmatch(r'(19|20)\d\d', v):      # 연도는 문맥에서 온다
                continue
            after = plain[plain.find(v) + len(v):plain.find(v) + len(v) + 2]
            if money and after and after[0] in '억조':
                continue
            if norm(v) in pool or norm(v.split('.')[0]) in pool:
                continue
            findings.append(('WARN', where, 'C1',
                             '숫자 "%s" 가 인용한 줄에 없다 — 원문을 열어 확인한다: %s…'
                             % (v, plain.strip()[:52])))


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    files = sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md')) +
                   glob.glob(os.path.join(paths.SYNTH, '*.md')))
    for p in files:
        meta, _ = nl.parse_front(io.open(p, encoding='utf-8').read())
        src = nl.sources_of(meta)
        if src:
            check(p, src)
    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    print('\n요약: 글 %d편 / 확인 필요 %d건' % (len(files), len(findings)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
