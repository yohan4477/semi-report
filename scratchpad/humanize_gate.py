# -*- coding: utf-8 -*-
"""윤문 전후 견주기 — humanize-korean 의 verify_gates 가 이 환경에 없어 그 자리를 채운다.

    PYTHONIOENCODING=utf-8 py -3.13 scratchpad/humanize_gate.py <전 파일> <후 파일>

변경률(문자 단위 difflib) · 보존 항목(줄 표기·숫자·절 제목·①②③·문단 첫 여덟 글자·따옴표 인용) ·
표지 빈도(「것이다」·「아니라」·대시·「~라는 것이」·쉼표) 전후. 보존 항목이 하나라도 다르면 FAIL.
"""
import difflib
import io
import re
import sys


def strip_summary(s):
    import re as _re
    # 요약 블록 마커의 띄어쓰기가 달라도 걷는다 — 못 걷으면 변경률과 숫자가 다 부풀어 오른다
    return _re.split(r'<!--\s*HUMANIZE[- ]SUMMARY', s)[0].strip()


def paras(s):
    return [p.strip() for p in re.split(r'\n\s*\n', s) if p.strip() and not p.strip().startswith('#')]


def main(a, b):
    A = io.open(a, encoding='utf-8').read().strip()
    B = strip_summary(io.open(b, encoding='utf-8').read())
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    changed = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal')
    rate = changed / max(len(A), 1)
    print('변경률 %.1f%%  (전 %d자 → 후 %d자)' % (rate * 100, len(A), len(B)))
    fails = []

    def same(name, fa, fb, show=6):
        if fa != fb:
            fails.append(name)
            da, db = sorted(set(fa) - set(fb)), sorted(set(fb) - set(fa))
            print('FAIL %s — 전에만 %s / 후에만 %s' % (name, da[:show], db[:show]))
        else:
            print('ok   %s (%d)' % (name, len(fa)))

    same('줄 표기 (L..)', sorted(re.findall(r'\(L[^)]*\)', A)), sorted(re.findall(r'\(L[^)]*\)', B)))
    same('숫자', sorted(re.findall(r'\d[\d,.~%]*', A)), sorted(re.findall(r'\d[\d,.~%]*', B)))
    same('절 제목', re.findall(r'^## .*$', A, re.M), re.findall(r'^## .*$', B, re.M))
    same('①②③', re.findall('[①-⑩]', A), re.findall('[①-⑩]', B))
    same('따옴표 인용', sorted(re.findall(r'"[^"\n]+"', A)), sorted(re.findall(r'"[^"\n]+"', B)))
    pa, pb = paras(A), paras(B)
    print('문단 %d → %d' % (len(pa), len(pb)))
    heads_a = [p[:8] for p in pa]
    heads_b = set(p[:8] for p in pb)
    lost = [h for h in heads_a if h not in heads_b]
    if lost:
        fails.append('문단 앞머리')
        print('FAIL 문단 첫 여덟 글자가 사라졌다:', lost)
    else:
        print('ok   문단 첫 여덟 글자 %d개 모두 남음' % len(heads_a))
    print('표지 빈도 (전 → 후, 1천자당)')
    for name, pat in [('것이다', r'것이다'), ('라는 것이', r'라는 것이'), ('아니라', r'아니라'), ('대시 —', r'—'),
                      ('쉼표', r','), ('~것은', r'것은'), ('는 것', r'는 것')]:
        na, nb = len(re.findall(pat, A)), len(re.findall(pat, B))
        print('  %-8s %5.2f → %5.2f   (%d → %d)' % (name, na / len(A) * 1000, nb / len(B) * 1000, na, nb))
    grade = 'FAIL' if fails else ('경고 30%+' if rate > .3 else ('중단 50%+' if rate > .5 else 'ok'))
    print('판정', grade, ('— ' + ', '.join(fails)) if fails else '')
    return 1 if fails or rate > .5 else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
