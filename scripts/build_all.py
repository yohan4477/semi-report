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
    ('산업/시장 대시보드', ['scratchpad/gen_industry_dashboard.py']),
    ('언더스탠딩 프리미엄', ['scratchpad/gen_undpremium_dashboard.py']),
    ('이선엽 시황', ['scratchpad/gen_leesunyeop_dashboard.py']),
    ('건강 대시보드', ['scratchpad/gen_health_dashboard.py']),
    ('수도리무브', ['scratchpad/gen_sudoremove_dashboard.py']),
    ('메르 인사이트', ['scratchpad/gen_mer_dashboard.py']),
    ('Epoch AI 대시보드', ['scratchpad/gen_epoch_dashboard.py']),
    ('Semi Doped 대시보드', ['scratchpad/gen_semidoped_dashboard.py']),
    # 각도 지도는 insights/angles/*.md 를 읽는다 — 각도를 새로 뽑으면 여기서 다시 깔린다.
    # 빌드 목록에 없어서 2026-08-29에 새 각도 한 편이 지도에 안 실린 채로 있었다
    ('각도 지도', ['scratchpad/gen_angles_dashboard.py']),
    ('AI Engineer 대시보드', ['scratchpad/gen_aie_dashboard.py']),
    ('통합 보고서', ['scratchpad/gen_report_dashboard.py']),
    ('회계사 대시보드', ['scratchpad/gen_accountant_dashboard.py']),
    # 링크드인은 원문 파일이 먼저 있어야 노트가 인용할 수 있다
    ('링크드인 원문', ['scripts/gen_li_source.py']),
    ('링크드인 신호 자격', ['insights/li_signal.py']),
    ('소스 매니페스트', ['insights/gen_manifest.py']),
    ('개체 색인', ['insights/gen_index.py']),
    ('가리키는 때', ['insights/gen_times.py']),
    ('통합 인사이트', ['insights/gen_insightview.py']),
    ('추적 · 일론 머스크', ['insights/gen_entity_board.py', 'musk']),
    ('인사이트 지도', ['insights/gen_map.py']),
    ('관리자 지도', ['scripts/gen_admin.py']),
    ('NEW 배지 대장', ['scripts/update_card_ledger.py']),
    ('사이트 빌드', ['scripts/gen_site.py']),
]

CHECK = [
    ('인용 해석·줄 해시', ['insights/check_notes.py']),
    ('문체', ['insights/check_prose.py']),
    ('읽히는가', ['insights/check_read.py']),
    ('숫자와 원문 대조', ['insights/check_cite.py']),
    ('시점', ['insights/check_fresh.py']),
    ('축과 근거', ['insights/check_axes.py']),
    ('개체 색인', ['insights/check_index.py']),
    # 도해 배치는 눈으로 보고 두 번 놓쳤다 — 글자끼리 겹침과 선에 깔림 둘 다
    ('도해 배치', ['scratchpad/check_fig.py']),
    # 추적된 코드가 추적 안 된 파일을 부르면 이 컴퓨터에서만 돈다
    ('의존 추적', ['scripts/check_deps.py']),
    # 앞의 것들은 전부 산문만 본다. 밸류에이션 결함 다섯이 그 사이로 새어 나갔다
    ('숫자 파이프라인', ['insights/check_val.py']),
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
