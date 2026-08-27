# -*- coding: utf-8 -*-
"""각도 — 등뼈가 사전과 어긋나 있지 않나 본다.

각도 파일은 나중에 서로 붙으라고 만든 것이고, 붙는 조건은 `대상` 문자열이 같은
것이다. 「OpenAI」와 「오픈AI」는 사람 눈에만 같아서, 표기가 갈리면 합칠 때
조용히 안 붙는다 — 에러도 안 난다. 그것을 여기서 막는다.

정본은 insights/entities.json 이다. 이 검사기는 판단을 더하지 않는다. 사전이
아는 것만 FAIL 로 잡고(별칭 → 정본), 사전이 모르는 이름은 WARN 으로 넘긴다 —
새 개체인지 집합명(「AI 랩」·「엔터프라이즈」)인지는 사람이 정한다.

  PYTHONIOENCODING=utf-8 python insights/check_angles.py
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import entities_lib as el  # noqa: E402
import paths  # noqa: E402

# 성격은 닫힌 목록이다. 늘리면 같은 것이 여러 이름으로 갈리고, 합칠 때 저자
# 가정이 사실로 굳는다. 목록을 고치려면 스킬 본문(레인 A)부터 고친다
KINDS = ('사실', '계획', '전망', '추정', '가정', '발언', '제안', '개념')
# 꼬리표 — 코드블록 안 항목 줄 끝에 붙는다. [대상 · 때 · §출처 · 성격]
TAG_RE = re.compile(r'\[([^\[\]\n]*?·[^\[\]\n]*?)\]')
SEP_RE = re.compile(r'^\|[\s:|-]+\|$')
# 표가 아닌 절 — 여기엔 꼬리표를 안 단다
NO_TAG_HEADS = ('## 시계열', '## 잔여', '## 다음 글이 채울 자리')


def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def rows(text):
    """표 행과 꼬리표를 한 꼴로 돌려준다 — (줄번호, 대상, 때, 성격, 원문)."""
    out = []
    skip = False
    for i, line in enumerate(text.split('\n'), 1):
        if line.startswith('## '):
            skip = any(line.startswith(h) for h in NO_TAG_HEADS)
        if skip:
            continue
        if line.startswith('|') and not SEP_RE.match(line):
            c = _cells(line)
            if len(c) == 6 and c[0] != '대상':
                out.append((i, c[0], c[3], c[5], line))
            continue
        for body in TAG_RE.findall(line):
            # 구분자는 ` · ` 다. 가운뎃점만으로 쪼개면 이름 안에 점이 든 대상
            # (「즈푸·미니맥스」)이 두 칸으로 갈려 칸 수가 안 맞는다
            f = [x.strip() for x in body.split(' · ')]
            if len(f) == 4:
                out.append((i, f[0], f[1], f[3], line))
            else:
                out.append((i, None, None, None, line))
    return out


def check(text, canon, alias):
    msgs = []
    for ln, target, when, kind, raw in rows(text):
        if target is None:
            msgs.append(('FAIL', 'A4', ln,
                         '꼬리표 칸이 넷이 아니다 — [대상 · 때 · §출처 · 성격]: %s'
                         % raw.strip()[:60]))
            continue
        if kind not in KINDS:
            msgs.append(('FAIL', 'A3', ln,
                         '성격 "%s" 는 여덟에 없다 — %s' % (kind, '·'.join(KINDS))))
        if not when:
            msgs.append(('WARN', 'A5', ln,
                         '때가 비었다 — 모르면 「—」로 둔다 (%s)' % target))
        key = el.norm(target)
        if key in alias and alias[key] != target:
            msgs.append(('FAIL', 'A1', ln,
                         '대상 "%s" 는 별칭이다 — 정본 "%s" 로 쓴다'
                         % (target, alias[key])))
        elif key not in alias and target not in canon:
            msgs.append(('WARN', 'A2', ln,
                         '대상 "%s" 가 사전에 없다 — 개체면 entities.json 에 넣고, '
                         '집합명이면 그대로 둔다' % target))
    return msgs


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ents = el.load()
    canon = set(r['canonical'] for r in ents)
    alias = el.alias_index(ents)
    files = [p for p in sorted(glob.glob(os.path.join(paths.ANGLES, '*.md')))
             if not os.path.basename(p).startswith('_')]
    fails = warns = items = 0
    for p in files:
        text = io.open(p, encoding='utf-8').read()
        items += len(rows(text))
        for level, rule, ln, msg in check(text, canon, alias):
            fails += level == 'FAIL'
            warns += level == 'WARN'
            print('%s %s:%d [%s] %s'
                  % (level, os.path.basename(p), ln, rule, msg))
    print('\n요약: 각도 %d편 / 항목 %d / FAIL %d / WARN %d'
          % (len(files), items, fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
