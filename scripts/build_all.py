# -*- coding: utf-8 -*-
"""전부 다시 만들고 전부 검사한다 — 푸시 전에 이것 하나만 돌리면 된다.

  py -3.13 scripts/build_all.py            생성기 전부 + 검사기 전부
  py -3.13 scripts/build_all.py --check    검사만(생성 안 함)

검사기가 하나라도 FAIL 이면 종료 코드 1이다. 그 상태로 푸시하지 않는다.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = [sys.executable]

# (표시 이름, 명령) — 순서가 곧 의존 순서다
BUILD = [
    ('부동산 대시보드', ['scratchpad/gen_realestate_dashboard.py']),
    ('미주사 대시보드', ['scratchpad/gen_usa_dashboard.py']),
    ('금융 대시보드', ['scratchpad/gen_finance_dashboard.py']),
    ('통합 인사이트', ['insights/gen_insightview.py']),
    ('추적 · 일론 머스크', ['insights/gen_entity_board.py', 'musk']),
    ('인사이트 지도', ['insights/gen_map.py']),
    ('허브', ['scripts/gen_hub.py']),
    ('NEW 배지 대장', ['scripts/update_card_ledger.py']),
    ('사이트 빌드', ['scripts/gen_site.py']),
]

CHECK = [
    ('인용 해석·줄 해시', ['insights/check_notes.py']),
    ('문체', ['insights/check_prose.py']),
    ('읽히는가', ['insights/check_read.py']),
    ('숫자와 원문 대조', ['insights/check_cite.py']),
]


def run(label, args):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run(PY + args, cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    tail = [l for l in (r.stdout or '').strip().split('\n') if l.strip()]
    last = tail[-1] if tail else (r.stderr or '').strip().split('\n')[-1][:120]
    bad = r.returncode != 0 or 'FAIL 1' in last or ('FAIL' in last and 'FAIL 0' not in last)
    print('%s %-22s %s' % ('✗' if bad else '·', label, last[:96]))
    if bad and r.stderr:
        print('   ' + r.stderr.strip().split('\n')[-1][:160])
    return bad


def main():
    only_check = '--check' in sys.argv
    bad = 0
    if not only_check:
        print('— 다시 만들기')
        for label, args in BUILD:
            bad += run(label, args)
    print('— 검사')
    for label, args in CHECK:
        bad += run(label, args)
    print('\n%s' % ('실패 %d건 — 고치고 다시 돌린다' % bad if bad else '전부 통과. 커밋·푸시해도 된다'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
