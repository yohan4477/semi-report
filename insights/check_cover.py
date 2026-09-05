# -*- coding: utf-8 -*-
"""보고서 층이 바탕 재료를 전수로 썼나 — insights/reports/*.md 의 라벨을 센다.

    PYTHONIOENCODING=utf-8 python insights/check_cover.py

2026-08-24 에 서른다섯 편 중 아홉 편이 한 번도 안 나온 채로 나갔다. 물어봐서 걸렸다.
그때 쓴 대조는 카드 제목에서 낱말을 뽑아 견주는 성긴 것이었고, 층마다 스크립트를 새로
짜야 했다(선단 패키징 층에서도 그때그때 짰다, 2026-09-05).

여기서는 **글이 스스로 밝힌 것**만 쓴다. 손으로 적는 목록이 없다.

    frontmatter labels:   이 글이 바탕으로 삼겠다고 밝힌 재료
    본문의 (라벨 L12)      실제로 근거로 댄 자리

둘을 맞춰 본다.

    C1 FAIL  선언했는데 한 번도 안 쓴 재료      빠뜨린 것이지 덜 중요한 것이 아니다
    C2 FAIL  안 선언했는데 인용한 라벨          오타이거나 labels 가 낡았다
    C3 WARN  인용이 한 번뿐인 재료              이름만 스치고 근거로 안 썼을 수 있다

라벨에 자리표(SD-mmdd · LI-yymm)를 쓰는 층이 있어서 그런 이름은 숫자 자리로 푼다.
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, 'insights', 'reports', '*.md')

# 본문 인용 — (라벨 L12) · (라벨 L12-14) · (라벨 L12, L15)
_CITE = re.compile(r'\(([^()]*?)\s+L\d[\d\s,\-·L]*\)')
# 라벨 이름에 든 자리표. 긴 것부터 봐야 mmdd 가 mm 둘로 안 쪼개진다
_SLOT = re.compile(r'mmdd|yymm|yyyy|yy|mm|dd')
_THIN = 1                      # 인용이 이 수 이하면 WARN


def declared(front):
    """frontmatter labels: 를 라벨 이름 목록으로. 「이름=설명」을 「·」로 이어 적는다."""
    m = re.search(r'^labels:\s*(.+)$', front, re.M)
    if not m:
        return []
    # 괄호 안 보충 설명은 라벨이 아니다 — 「(2605·2607·2608)」을 라벨 셋으로 셌다
    line = re.sub(r'\([^()]*\)', '', m.group(1))
    out = []
    for part in line.split('·'):
        name = part.split('=')[0].strip()
        if name:
            out.append(name)
    return out


def to_re(name):
    """자리표가 든 라벨 이름을 정규식으로. SD-mmdd 는 SD-0807 에 맞는다."""
    if not _SLOT.search(name):
        return re.compile(r'^%s$' % re.escape(name))
    pat, i = [], 0
    for m in _SLOT.finditer(name):
        pat.append(re.escape(name[i:m.start()]))
        pat.append(r'\d{%d}' % len(m.group(0)))
        i = m.end()
    pat.append(re.escape(name[i:]))
    return re.compile('^%s$' % ''.join(pat))


def used(body):
    """본문이 실제로 댄 라벨과 그 횟수."""
    hits = {}
    for lab in _CITE.findall(body):
        lab = lab.strip()
        if lab:
            hits[lab] = hits.get(lab, 0) + 1
    return hits


def main():
    fails = warns = 0
    files = sorted(glob.glob(REPORTS))
    for path in files:
        txt = io.open(path, encoding='utf-8').read()
        if not txt.startswith('---'):
            continue
        _, front, body = txt.split('---', 2)
        names = declared(front)
        if not names:
            print('SKIP %s — labels 가 없다' % os.path.basename(path))
            continue
        hits = used(body)
        pats = [(n, to_re(n)) for n in names]

        # C1 선언했는데 안 쓴 것 · C3 한 번만 쓴 것
        rows = []
        for name, pat in pats:
            n = sum(c for lab, c in hits.items() if pat.match(lab))
            rows.append((name, n))
        # C2 선언 밖에서 인용한 라벨
        stray = sorted(lab for lab in hits
                       if not any(pat.match(lab) for _n, pat in pats))

        print('\n%s — 재료 %d종 · 인용 %d건'
              % (os.path.basename(path), len(names), sum(n for _l, n in rows)))
        for name, n in rows:
            if n == 0:
                fails += 1
                print('  FAIL [C1] %s — 선언했는데 본문에 한 번도 안 나온다' % name)
            elif n <= _THIN:
                warns += 1
                print('  WARN [C3] %s — 인용 %d건. 이름만 스쳤는지 본다' % (name, n))
        for lab in stray:
            fails += 1
            print('  FAIL [C2] %s — labels 에 없는 라벨로 인용했다 (%d건)' % (lab, hits[lab]))
        ok = [n for n, c in rows if c > _THIN]
        print('  전수 %d/%d' % (len(ok) + sum(1 for _n, c in rows if 0 < c <= _THIN), len(rows)))

    print('\n요약: 보고서 %d편 / FAIL %d / WARN %d' % (len(files), fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
