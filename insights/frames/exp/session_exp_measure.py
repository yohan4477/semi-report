# -*- coding: utf-8 -*-
"""잰다: 앵글 둘을 한 세션에서 물을 때와 세션 둘로 나눠 물을 때가 다른가.

돌리는 법은 `session_exp_run.sh` — 같은 회차·같은 프롬프트·같은 모델(Opus 5)로
조건 셋을 굽는다. 이 파일은 그 산출을 잰다.

  B    세션 둘 · 각각 앵글 하나 (gem_ask 가 임시 채팅으로 하는 지금 방식)
  A    세션 하나 · 경영 → 기술
  A2   세션 하나 · 기술 → 경영

재는 것은 여섯이다. 「표지」는 사실을 다뤘나의 **대리 지표**다 — 원문에 나온 숫자와
영문 고유명사를 집합으로 잡고, 답이 그중 무엇을 실었나로 센다. 무엇을 담았나는
세지만 제대로 다뤘나는 못 센다.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import frame_view as F  # noqa: E402

FENCE = re.compile(r'```mermaid\n(.*?)\n```', re.S)
# 「앞선다」(우선한다)·「앞선 세대」가 걸려 헛세었다 — 앞 답을 가리키는 꼴만 남긴다
SELF = re.compile(r'앞(?:서|선) (?:답|분석|절|장)|위에서 (?:말|다룬)|전략 쪽에서|기술 쪽에서')


def marks(t):
    nums = {n.strip() for n in re.findall(r'\d[\d,\.]*', t) if len(n.strip()) > 1}
    return nums | set(re.findall(r'\b[A-Z][A-Za-z0-9\-]{2,}\b', t))


def measure(path, src_marks):
    t = io.open(path, encoding='utf-8').read()
    ok = dup = wide = 0
    blocks = FENCE.findall(t)
    for b in blocks:
        g = F._mm_parse(b)
        if F._mm_to_plate(g):
            ok += 1
        cols = {}
        for nid, ti in g.title_of.items():
            if ti:
                cols.setdefault(ti, set()).add(g.names[nid])
        ks = list(cols)
        for a in range(len(ks)):
            for c in range(a + 1, len(ks)):
                if cols[ks[a]] & cols[ks[c]]:
                    dup += 1        # 대비 칸 양쪽에 다 있는 값(규칙 4)
        for lv in F._mm_topo_levels(g.order, g.edges):
            if len(lv) > 3:
                wide += 1           # 한 층 형제 넷(규칙 6)
    return dict(자=len(t), 절=len(re.findall(r'^##\s', t, re.M)), 판=len(blocks),
                굽기=ok, 배타=dup, 형제4=wide, 자기=len(SELF.findall(t)),
                표지=marks(t) & src_marks)


def main(out_dir, src_path):
    S = marks(io.open(src_path, encoding='utf-8').read())
    sets = [('B  세션 둘', ['B-strategy.md', 'B-tech.md']),
            ('A  하나 경영→기술', ['A-1-strategy.md', 'A-2-tech.md']),
            ('A2 하나 기술→경영', ['A2-1-tech.md', 'A2-2-strategy.md'])]
    print('원문 표지 %d개' % len(S))
    print('%-18s %6s %3s %3s %4s %4s %4s %4s %7s %6s'
          % ('조건', '자', '절', '판', '굽기', '배타', '형4', '자기', '커버', '겹침'))
    for nm, fs in sets:
        ms = [measure(os.path.join(out_dir, f), S) for f in fs]
        cov = ms[0]['표지'] | ms[1]['표지']
        ov = ms[0]['표지'] & ms[1]['표지']
        print('%-18s %6d %3d %3d %4d %4d %4d %4d %6.0f%% %5.0f%%'
              % (nm, sum(m['자'] for m in ms), sum(m['절'] for m in ms),
                 sum(m['판'] for m in ms), sum(m['굽기'] for m in ms),
                 sum(m['배타'] for m in ms), sum(m['형제4'] for m in ms),
                 sum(m['자기'] for m in ms),
                 100.0 * len(cov) / len(S), 100.0 * len(ov) / max(1, len(cov))))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
