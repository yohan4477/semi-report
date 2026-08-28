# -*- coding: utf-8 -*-
"""구조가 글에 실제로 서 있나 — 규칙을 기계가 보는 자리.

CLAUDE.md 「글은 기본이 구조다」는 지금까지 스킬(`doc-structure`)과 규칙 문장에만 있었다.
스킬은 내가 열어야 걸리고 규칙 문장은 어겨도 아무도 안 본다. 실제로 Semi Doped 카드
스물일곱 장이 목차도 축도 없이 검사기 열셋을 전부 통과했다 — 그 자리를 이 검사기가 막는다.

보는 것은 **report 꼴로 쓴 카드**(`<div class="uc-rep">`)다. 옛 꼴 카드(핵심 포인트·주요
숫자·인용)는 절 이름이 스키마로 정해진 갈래라 대상이 아니다 — CLAUDE.md 가 그 갈래를
따로 빼 두었다.

  PYTHONIOENCODING=utf-8 python insights/check_struct.py
  PYTHONIOENCODING=utf-8 python insights/check_struct.py 텐서다인   제목에 그 말이 든 카드만

  S1  앞머리에 물음·바탕·축 셋이 다 있나              FAIL
  S2  목차가 있고 그 첫 줄이 「구조.」인가              FAIL
  S3  구조 갈래가 정해진 일곱 안에 드나                FAIL
  S4  절 제목이 물음인가                            FAIL
  S5  목차의 번호와 실제 절 번호가 맞나                FAIL
  S6  견주는 표에 「언제 것 · 성격」 열이 있나           FAIL
  S7  마지막 절이 한계인가                           WARN
  S8  절이 여덟을 넘나                              WARN
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paths  # noqa: E402

OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8', line_buffering=True)

# 글의 꼴을 적는 말 — 목차 왼쪽 칸에 오면 안 된다. 그건 내가 글을 어떻게 늘어놓았는지이지
# 다루는 것이 어떤 마디로 되어 있는가가 아니다. 마디 이름은 원문 안에서 찾는다.
SHAPE_WORDS = ('시간 흐름', '대비', '층위', '인과 사슬', '부분 나눔', '조건 갈림',
               '문제와 처방')
BAD_NODE = SHAPE_WORDS + ('서론', '본론', '결론', '배경', '개요')

# 규칙을 게이트로 세운 장. 나머지 장은 같은 것을 보되 WARN 으로만 센다 —
# AI Engineer 68편은 이 규칙보다 먼저 쓰였고 그 장의 규칙 문서가 따로 있다.
# 소급은 그 문서를 고치는 일과 함께 한다.
STRICT = ('Semi Doped 대시보드.html',)

CIRCLE = '①②③④⑤⑥⑦⑧⑨⑩'
CARD = re.compile(r'<div class="ucard[^"]*"[^>]*>(.*?)(?=<div class="ucard|<footer|\Z)', re.S)
TITLE = re.compile(r'<h2 id="[^"]*">(.*?)</h2>', re.S)
VERDICT = re.compile(r'<p class="uc-verdict">(.*?)</p>', re.S)
# 본문 안에 <div> 가 겹쳐 있다(목차 상자·그림). 링크 줄이 늘 뒤에 오니 거기까지 자른다
REP = re.compile(r'<div class="uc-rep">(.*?)(?:<div class="uc-links"|\Z)', re.S)
H3 = re.compile(r'<h3>(.*?)</h3>', re.S)
FIRST_P = re.compile(r'^\s*<p>(.*?)</p>', re.S)
# 목차는 첫 절보다 앞에 있으면 된다 — 그 앞에 각도 상자가 설 수 있다
TOCBOX = re.compile(r'<div class="uc-toc">(.*?)(?=<h3>|\Z)', re.S)
ANGBOX = re.compile(r'<div class="uc-angles">(.*?)</div>', re.S)
# 나무로 그리면서 L1 이름이 <span class="ag-1"> 안으로 들어갔다. 가지는 빼고 줄기만 읽는다
ANGLI = re.compile(r'<li class="ag-(on|off)"><span class="ag-1">(.*?)</span>', re.S)
# 물음 하나와 그 아래 구성요소 묶음
AGQ = re.compile(r'<span class="ag-q">(.*?)</span>(?:<span class="ag-eq">(.*?)</span>)?'
                 r'(?:<ul class="ag-p">(.*?)</ul>)?', re.S)
# 식을 항으로 자른다. = 로 좌우를 나누고 + − × ÷ 로 항을 쪼갠다
EQCUT = re.compile(r'[=+−×÷→∝≈]|[-]')
AGROW = re.compile(r'<li>(?:<span class="ag-ax">(.*?)</span>)?<span class="ag-v">(.*?)</span></li>',
                   re.S)
TG = re.compile(r'<span class="tg-k">(.*?)</span>', re.S)
TF = re.compile(r'<span class="tg-f">(.*?)</span>', re.S)
TBL_HEAD = re.compile(r'<thead>(.*?)</thead>', re.S)
TAG = re.compile(r'<[^>]+>')

# 절 제목이 물음인가 — 물음말이 들었거나 「~나/~가」로 닫히면 물음으로 본다
ASK = re.compile(r'무엇|왜|언제|어디|어떻게|얼마|누가|몇|어느')
CLOSE = re.compile(r'(나|가|인가|는가|을까|ㄹ까)$')
# 서랍 제목 — 물음이 아니라 칸이다
DRAWER = ('여러 가지', '기타', '그 밖', '정리', '요약', '개요')
LIMIT = ('한계', '밝히지 않', '안 밝힌', '못 밝힌', '검증되지', '남는 물음')

def load_angles():
    """각도 파일의 angles 목록 — 카드가 밝힌 각도와 대조할 정본."""
    out = {}
    for p in glob.glob(os.path.join(paths.ROOT, 'insights', 'angles', '*.md')):
        t = io.open(p, encoding='utf-8').read()
        m = re.search(r'^angles:\s*\[(.*?)\]\s*$', t, re.M)
        if m:
            names = [x.strip() for x in m.group(1).split(',') if x.strip()]
            out[os.path.basename(p)] = [n for n in names if n != '저자 논지']
    return out


ANGLES = load_angles()
rows = []


def add(kind, where, code, msg):
    # 게이트로 세운 장이 아니면 FAIL 을 WARN 으로 낮춘다
    if kind == 'FAIL' and not where.startswith(STRICT):
        kind = 'WARN'
    rows.append((kind, where, code, msg))


def txt(s):
    # 태그를 빈칸으로 바꾼다. 지워 버리면 <br> 로 나눈 두 줄이 「…사슬목차.」로 붙는다
    return re.sub(r'\s+', ' ', TAG.sub(' ', s or '')).strip()


def check_card(where, body):
    mt = TITLE.search(body)
    mr = REP.search(body)
    if not mt or not mr:
        return False
    title = txt(mt.group(1))
    rep = mr.group(1)
    at = '%s · %s' % (where, title[:34])

    # S1 앞머리 — 물음·바탕·축
    mv = VERDICT.search(body)
    v = txt(mv.group(1)) if mv else ''
    missing = [w for w in ('물음.', '바탕.', '축.') if w not in v]
    if missing:
        add('FAIL', at, 'S1', '앞머리에 %s 이(가) 없다' % '·'.join(m.rstrip('.') for m in missing))

    # S2 목차 — report 첫 블록이 갈래별 목차 상자여야 한다.
    # 한 문단에 가운뎃점으로 이어 붙인 옛 꼴(<p>목차. ① … · ② …)도 여기서 걸린다.
    mbox = TOCBOX.search(rep)
    toc = txt(mbox.group(1)) if mbox else ''
    forms_used = [txt(f) for f in TG.findall(mbox.group(1))] if mbox else []
    if not mbox:
        mp = FIRST_P.search(rep)
        first = txt(mp.group(1)) if mp else ''
        add('FAIL', at, 'S2',
            '목차가 갈래별 상자가 아니다%s' % (' — 한 문단으로 이어 붙였다' if '목차' in first else ''))

    # S3 왼쪽 칸은 대상의 마디다.
    # ① 글의 꼴을 적는 말이면 걸린다. ② 본문에 한 번도 안 나오는 말이면 걸린다 —
    # 대상의 마디라면 본문에서 그 말로 이야기하고 있어야 한다.
    body_txt = txt(rep)
    for f in forms_used:
        if f == '한계':
            continue
        if f in BAD_NODE:
            add('FAIL', at, 'S3', '글의 꼴을 마디로 적었다 — 대상의 마디를 댄다: %s' % f)
            continue
        core = max(f.split(), key=len)
        if core not in body_txt:
            add('FAIL', at, 'S3', '본문에 안 나오는 마디다: %s' % f)

    # S3b 마디 옆 칸은 글의 꼴이다. 마디만 있으면 글이 어떻게 굴러가는지가 안 보인다
    shapes = [txt(x) for x in TF.findall(mbox.group(1))] if mbox else []
    if mbox and not shapes:
        add('FAIL', at, 'S3b', '목차에 글의 꼴 칸이 없다 — 마디와 꼴 둘 다 세운다')
    for sh in shapes:
        if sh not in SHAPE_WORDS:
            add('FAIL', at, 'S3b', '글의 꼴이 정해진 일곱에 없다: %s' % sh)

    # S9 각도를 목차와 따로 밝혔나. 그리고 그 목록이 각도 파일과 같은가 —
    # 카드가 각도 일부만 절로 세우는 것은 정상이지만, 어떤 각도가 있었는지는 밝혀야 한다
    mang = ANGBOX.search(rep)
    if not mang:
        add('FAIL', at, 'S9', '각도를 밝힌 자리가 없다 — 목차와 따로 세운다')
    else:
        # 하위 각도는 각도 파일 프런트매터에 없다(L1 만 적는다) — 떼고 견준다
        named = [txt(re.sub(r'<span class="ag-sub">.*?</span>', '', m[1], flags=re.S))
                 for m in ANGLI.findall(mang.group(1))]
        if not named:
            add('FAIL', at, 'S9', '각도 목록이 비어 있다')
        elif ANGLES:
            same = [a for a in ANGLES.values() if set(a) == set(named)]
            if not same:
                add('WARN', at, 'S9', '각도 목록이 어느 각도 파일과도 안 맞는다: %s'
                    % ' · '.join(named[:5]))

    # S10 한 물음 아래 구성요소가 축으로 갈렸나. 물음만 MECE 하게 쪼개고 그 아래를
    # 사실 자루로 두면 무엇과 무엇이 겹치는지가 안 보인다. 축 이름이 있어야 겹친 축도
    # 빠진 축도 눈에 걸린다. 같은 축이 한 물음에 두 번 나오면 그건 안 가른 것이다
    if mang:
        for mq in AGQ.finditer(mang.group(1)):
            q = txt(mq.group(1))
            eq = txt(mq.group(2) or '')
            rows = AGROW.findall(mq.group(3))
            if not rows:
                continue
            axes = [txt(a) for a, _ in rows if a]
            bare = len(rows) - len(axes)
            if bare:
                add('WARN', at, 'S10', '구성요소에 축 이름이 없다(%d개) — 「%s」' % (bare, q))
            dup = {a for a in axes if axes.count(a) > 1}
            if dup:
                add('FAIL', at, 'S10', '한 물음에 같은 축이 두 번 — 「%s」의 %s'
                    % (q, ' · '.join(sorted(dup))))
            if len(rows) == 1:
                add('WARN', at, 'S10', '구성요소가 하나뿐이다 — 갈린 게 아니다: 「%s」' % q)

            # S11 식을 세웠으면 그 항이 축으로 서 있어야 한다. 「a = 가 + 나 + 다」로
            # 적어 놓고 축이 딴것이면 무엇을 더해 그 값이 나왔는지가 다시 사라진다
            if eq:
                terms = [t.strip() for t in EQCUT.split(eq) if t.strip()]
                axjoin = ' '.join(axes)
                miss = [t for t in terms if len(t) > 1 and t not in axjoin]
                if miss:
                    add('WARN', at, 'S11', '식의 항이 축에 없다 — 「%s」의 %s'
                        % (q, ' · '.join(miss[:3])))
                if len(terms) < 2:
                    add('FAIL', at, 'S11', '식에 항이 하나뿐이다 — 「%s」' % q)

    # S4 절 제목이 물음인가
    heads = [txt(h) for h in H3.findall(rep)]
    for h in heads:
        bare = h.lstrip(CIRCLE).strip()
        if any(d in bare for d in DRAWER):
            add('FAIL', at, 'S4', '서랍 제목이다 — 물음으로 바꾼다: %s' % bare)
            continue
        if any(k in bare for k in LIMIT):
            continue                      # 마지막 한계 절은 물음이 아니어도 된다
        if not (ASK.search(bare) or CLOSE.search(bare)):
            add('FAIL', at, 'S4', '물음이 아니다: %s' % bare)

    # S5 목차 번호와 실제 절 번호
    if toc:
        want = [c for c in CIRCLE if c in toc]
        got = [h[0] for h in heads if h and h[0] in CIRCLE]
        if want != got:
            add('FAIL', at, 'S5', '목차 %d개 · 절 %d개로 어긋난다' % (len(want), len(got)))

    # S6 견주는 표에 성격 열
    for th in TBL_HEAD.findall(rep):
        head = txt(th)
        if '성격' not in head:
            add('FAIL', at, 'S6', '표에 「언제 것 · 성격」 열이 없다: %s' % head[:40])

    # S7 마지막 절이 한계인가
    if heads and not any(k in heads[-1] for k in LIMIT):
        add('WARN', at, 'S7', '마지막 절이 한계가 아니다: %s' % heads[-1])

    # S8 절이 여덟을 넘나
    if len(heads) > 8:
        add('WARN', at, 'S8', '절이 %d개 — 묶어서 줄인다' % len(heads))
    return True


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else ''
    n = 0
    for p in sorted(glob.glob(os.path.join(paths.ROOT, '대시보드', '*.html'))):
        html = io.open(p, encoding='utf-8').read()
        if 'uc-rep' not in html:
            continue
        where = os.path.basename(p)
        for m in CARD.finditer(html):
            body = m.group(0)
            mt = TITLE.search(body)
            if want and (not mt or want not in txt(mt.group(1))):
                continue
            n += check_card(where, body)
    for kind, at, code, msg in rows:
        print('%s %s [%s] %s' % (kind, at, code, msg), file=OUT)
    fail = sum(1 for r in rows if r[0] == 'FAIL')
    warn = len(rows) - fail
    print('\n요약: report 카드 %d장 / FAIL %d / WARN %d' % (n, fail, warn), file=OUT)
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
