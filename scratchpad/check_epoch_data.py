# -*- coding: utf-8 -*-
"""뽑아 둔 점 자료가 원문이 인쇄한 값과 맞는지 본다.

배치 검사기(check_fig·check_fig_strict)는 글자가 겹치는지만 본다. 자료가 통째로
어긋난 것은 못 잡는다 — 2026-08-25에 cybereci 의 세로 자가 33% 눌려 있었고 맨
왼쪽 점 하나가 빠져 있었는데, 배치 검사는 셋 다 FAIL 0 이었다.

원문 도해는 값 몇 개를 그림 안에 인쇄해 둔다. 그 값이 우리가 뽑은 자료에서
그대로 나오면 자가 맞는 것이다. 요약본의 「원문 도해에서 읽은 값」 절이 그 값을
적어 두는 자리이고, 여기서는 그것을 기대값으로 삼는다.

  PYTHONIOENCODING=utf-8 python scratchpad/check_epoch_data.py
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DATA = json.load(io.open(os.path.join(ROOT, 'data', 'epoch_fig_data.json'), encoding='utf-8'))
fails = []


def eq(got, want, tol, what):
    ok = abs(got - want) <= tol
    print('  %s %-46s 뽑은 값 %-10s 원문 %s' % ('OK  ' if ok else 'FAIL', what, got, want))
    if not ok:
        fails.append(what)


def rising(seq, what):
    bad = [i for i in range(1, len(seq)) if seq[i] is not None and seq[i - 1] is not None
           and seq[i] < seq[i - 1]]
    print('  %s %-46s %s' % ('OK  ' if not bad else 'FAIL', what,
                             '뒤로 간 자리 없음' if not bad else '뒤로 간 자리 %s' % bad))
    if bad:
        fails.append(what)


print('① by_chip — 세대별 보유량(만 장). 요약본 표와 맞는가')
b = {x['year']: x for x in DATA['by_chip']['bars']}
for yr, amp, hop, blk, tot in ((2023, 3, 6, None, 9), (2024, 3, 34, None, 37),
                               (2025, 2, 62, 107, 171)):
    seg = b[yr]['seg']
    eq(round(seg['Ampere'] / 10.0), amp, 1, '%d년 앰페어' % yr)
    eq(round(seg['Hopper'] / 10.0), hop, 1, '%d년 호퍼' % yr)
    if blk:
        eq(round(seg['Blackwell'] / 10.0), blk, 1, '%d년 블랙웰' % yr)
    eq(round(b[yr]['total'] / 10.0), tot, 1, '%d년 합계' % yr)

print('\n② openai_line — 분기별 누적(만 장). 세계는 아홉 곳 다, 오픈AI는 표식 셋')
w = [round(v / 10000.0) for v in DATA['openai_line']['world']]
for i, want in enumerate((107, 161, 242, 351, 480, 675, 925, 1229, 1591)):
    eq(w[i], want, 2, '세계 총계 %d번째 분기' % i)
oa = [round(v / 10000.0) for v in DATA['openai_line']['openai']]
for i, want in ((0, 10), (4, 38), (8, 169)):
    eq(oa[i], want, 2, '오픈AI %d번째 분기' % i)
rising(DATA['openai_line']['openai'], '오픈AI 누적치가 줄지 않는가')
rising(DATA['openai_line']['world'], '세계 총계가 줄지 않는가')

print('\n③ cyber_prog — 원문이 그림에 인쇄한 Cyber ECI 셋')
import epoch_fig  # noqa: E402,F401  (곁 모듈이 이걸 먼저 물어야 순환이 안 난다)
import epoch_fig_cyber as cy  # noqa: E402
named = {n: v for n, _c, _m, v in cy.CP_NAMED}
for name, want in (('Mythos Preview', 169.6), ('Mythos 5', 172.2), ('GPT-5.6 Sol', 171.2)):
    eq(round(named[name], 1), want, 0.15, name)

print('\n④ cve_spike — 마지막 석 달')
eq(cy.CVE_HIGH[-3], 381, 0, '고위험 3월')
eq(cy.CVE_HIGH[-2], 598, 0, '고위험 4월')
eq(cy.CVE_HIGH[-1], 900, 0, '고위험 5월')
eq(cy.CVE_CRIT[-3], 55, 0, '치명 3월')
eq(cy.CVE_CRIT[-2], 96, 0, '치명 4월')
eq(cy.CVE_CRIT[-1], 141, 0, '치명 5월')
eq(min(cy.CVE_HIGH), 85, 0, '고위험 최저')
eq(min(cy.CVE_CRIT), 1, 0, '치명 최저')
eq(len(cy.CVE_HIGH), 53, 0, 'CVE 달 수')

print('\n⑤ cyber_eci — 세로 자가 눌리지 않았나. 자가 맞으면 맨 위 점이 프런티어다')
pts = DATA['cyber_eci']['points']
eq(len(pts['teal']), 10, 0, '프런티어 점 수')
eq(max(b for _a, b in pts['teal']), 171.2, 0.3, '맨 위 프런티어 ECI')
eq(min(b for _a, b in pts['teal']), 139.9, 0.3, '맨 아래 프런티어 ECI')
lo = min(b for v in pts.values() for _a, b in v)
print('  %s %-46s %s' % ('OK  ' if lo >= 135 else 'FAIL',
                         '모든 점이 세로 자(135~175) 안에 있나', round(lo, 1)))
if lo < 135:
    fails.append('점이 축 아래로 빠짐')

print('\n⑥ calib — 겹쳐 그려져 다 갈라지지 않는다. 요약본이 적어 둔 수')
eq(len(DATA['calib']['uncal']['points']), 47, 0, '보정 전 갈라진 점')
eq(len(DATA['calib']['cal']['points']), 36, 0, '보정 후 갈라진 점')

print('\n자료 대조 FAIL %d건' % len(fails))
sys.exit(1 if fails else 0)
