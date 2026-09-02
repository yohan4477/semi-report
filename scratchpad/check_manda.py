# -*- coding: utf-8 -*-
"""M&A 카드 원고 ↔ 원문 대조.

`content/understanding/한주성/*.md` 한 편마다 `input/linkedin/한주성/` 의 같은 aid 클리핑을 열어 본다.

  FAIL  frontmatter 필수 키 없음 · 모르는 섹션 · 절 없음
        인용(`> `)이 원문에 없다(공백·따옴표를 지운 뒤 유사도 0.85 미만)
        숫자가 원문에 없다(쉼표·공백을 지우고 비교. 12 이하 정수와 날짜는 안 본다)
        반론이 없다 · 「누구」가 정해진 셋 밖이다
        번역투 낱말 넷 · 「돈을 댄다」
  WARN  핵심 포인트가 5~8개 밖 · 대시(—) 넷 이상 · 「가 아니라」 셋 이상
        소제목이 자루 이름(배경·전망·시사점·결론)

  PYTHONIOENCODING=utf-8 python scratchpad/check_manda.py          전체
  PYTHONIOENCODING=utf-8 python scratchpad/check_manda.py 한샘      파일 이름에 그 말이 든 것만
"""
import difflib
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_manda_dashboard as G  # noqa: E402

NUM = re.compile(r'\d[\d,\.]*')
BANNED = ['되어진', '로 인해', '에 있어서', '라고 할 수 있다']
MONEY = re.compile(r'돈을\s*(대|댄|댔|댈)')
WHO_OK = re.compile(r'^(필자 스스로|같은 저자 · 20\d\d-\d\d-\d\d .+|이 글이 답하지 않은 것)$')
BAG = {'배경', '전망', '시사점', '결론', '의미', '한계', '개요', '요약', '문제', '해법', '현황'}


def norm(t):
    return re.sub(r'[\s,、,·"“”\'‘’「」<>\-–—…\.]', '', t)


def raw_of(aid, raw_files):
    p = raw_files.get(aid[-4:])
    if not p:
        return None
    md = io.open(p, encoding='utf-8').read()
    _, body = G.front(md)
    return body


def quote_ok(q, raw):
    nq, nr = norm(q), norm(raw)
    if not nq:
        return True, 1.0
    if nq in nr:
        return True, 1.0
    # 문장 단위로 가장 가까운 것을 찾는다
    best = 0.0
    sents = re.split(r'(?<=[\.\?\!다요\)])\s+|\n', raw)
    for s in sents:
        ns = norm(s)
        if not ns:
            continue
        r = difflib.SequenceMatcher(None, nq, ns).ratio()
        if r > best:
            best = r
    return best >= 0.85, best


def numbers(text):
    out = []
    # 날짜는 안 본다 — 「같은 저자 · 2026-02-19」「2026년 2월 19일 쓴 글」
    text = re.sub(r'20\d\d-\d\d(-\d\d)?|20\d\d년\s*\d{1,2}월(\s*\d{1,2}일)?|\d{1,2}월\s*\d{1,2}일', '', text)
    for m in NUM.finditer(text):
        tok = m.group(0).strip('.,')
        if not tok:
            continue
        if re.fullmatch(r'\d+', tok) and int(tok) <= 12:
            continue
        if re.fullmatch(r'20\d\d(-\d\d){0,2}', tok):
            continue
        out.append(tok)
    return out


def check_file(p, raw_files):
    fails, warns = [], []
    name = os.path.basename(p)
    md = io.open(p, encoding='utf-8').read()
    fm, body = G.front(md)
    for k in G.REQUIRED:
        if not fm.get(k):
            fails.append('frontmatter %s 없음' % k)
    if fm.get('section') and fm['section'] not in G.SEC:
        fails.append('모르는 섹션 %s' % fm['section'])
    sec = G.sections(body)
    for k in ['한 줄', '핵심 포인트', '주요 숫자', '인용', '반론 · 충돌', '메모']:
        if k not in sec:
            fails.append('절 「%s」 없음' % k)
    raw = raw_of(fm.get('aid', ''), raw_files) if fm.get('aid') else None
    if raw is None:
        fails.append('원문 클리핑을 못 찾음 (aid %s)' % fm.get('aid'))
        return fails, warns

    # 인용
    for ln in sec.get('인용', '').splitlines():
        if ln.strip().startswith('>'):
            q = re.sub(r'^\s*>\s?', '', ln).strip()
            ok, r = quote_ok(q, raw)
            if not ok:
                fails.append('인용이 원문에 없다 (유사도 %.2f): %s' % (r, q[:60]))

    # 숫자 — 본문(frontmatter 제외) 전체
    text_for_num = '\n'.join(v for k, v in sec.items() if k != '반론 · 충돌') + '\n' + fm.get('gain', '')
    text_for_num = re.sub(r'같은 저자 · 20\d\d-\d\d-\d\d', '', text_for_num)
    nraw = norm(raw)
    for tok in numbers(text_for_num):
        if norm(tok) not in nraw:
            fails.append('숫자 %s 가 원문에 없다' % tok)
    # 반론 절의 숫자는 「같은 저자」 인용일 수 있어 WARN 으로만
    for tok in numbers(re.sub(r'같은 저자 · 20\d\d-\d\d-\d\d', '', sec.get('반론 · 충돌', ''))):
        if norm(tok) not in nraw:
            warns.append('반론 절 숫자 %s 가 이 편 원문에 없다(다른 글 인용이면 정상)' % tok)

    # 반론
    clash = G.bullets(sec.get('반론 · 충돌', ''))
    if not clash:
        fails.append('반론이 없다')
    for it in clash:
        who = re.sub(r'\*\*', '', it.split('|', 1)[0]).strip() if '|' in it else ''
        if not WHO_OK.match(who):
            fails.append('반론 「누구」가 정해진 셋 밖: %s' % (who or it[:40]))

    # 포인트
    pts = G.bullets(sec.get('핵심 포인트', ''))
    if not 5 <= len(pts) <= 8:
        warns.append('핵심 포인트 %d개' % len(pts))
    for it in pts:
        m = re.match(r'^\*\*(.+?)\.?\*\*', it)
        if not m:
            fails.append('포인트가 **소제목.** 으로 안 열림: %s' % it[:40])
        elif m.group(1).strip().rstrip('.') in BAG:
            warns.append('소제목이 자루 이름: %s' % m.group(1))

    # 문체
    for w in BANNED:
        if w in body:
            fails.append('번역투 「%s」' % w)
    if MONEY.search(body):
        fails.append('「돈을 댄다」')
    if body.count('—') > 3:
        warns.append('대시 %d개' % body.count('—'))
    if len(re.findall(r'가 아니라|이 아니라', body)) > 2:
        warns.append('「가 아니라」 %d회' % len(re.findall(r'가 아니라|이 아니라', body)))
    return fails, warns


def main():
    key = sys.argv[1] if len(sys.argv) > 1 else ''
    raw_files = {}
    for p in glob.glob(os.path.join(G.RAW_DIR, '*.md')):
        m = re.search(r'\[(\d{4})\]\.md$', p)
        if m:
            raw_files[m.group(1)] = p
    files = [p for p in sorted(glob.glob(os.path.join(G.SRC_DIR, '*.md')))
             if not os.path.basename(p).startswith('_') and key in os.path.basename(p)]
    nf = nw = 0
    for p in files:
        fails, warns = check_file(p, raw_files)
        nf += len(fails)
        nw += len(warns)
        for f in fails:
            print('FAIL %s | %s' % (os.path.basename(p)[:44], f))
        for w in warns:
            print('WARN %s | %s' % (os.path.basename(p)[:44], w))
    print('파일 %d · FAIL %d · WARN %d' % (len(files), nf, nw))
    return 1 if nf else 0


if __name__ == '__main__':
    sys.exit(main())
