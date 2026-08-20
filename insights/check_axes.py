# -*- coding: utf-8 -*-
"""축 검사 — 사슬이 실제 글과 맞나, 그리고 못 쓸 근거를 인용했나.

  A1  글이 밝힌 axis/cell 이 축에 없다
  A2  한 축 안에서 같은 글이 두 칸에 섰다
  A3  옛 글 41장이 여덟 편에 정확히 한 번씩 안 들어갔다 (이행 중에는 WARN)
  S1  충돌을 다루는 절이 있는데 「누가 더 가까이서 봤나」가 없다 (당분간 WARN)
  L1  배제된 링크드인 게시물의 줄을 인용했다
  L2  링크드인 인용의 기준일을 못 읽는다

  py -3.13 insights/check_axes.py
"""
import glob
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import axes
import notes_lib as nl
import paths

# 이행 전 옛 글 41장의 headline. 옛 글은 흡수되는 대로 지워지므로(설계 「41장은
# 지운다」) 살아 있는 파일에서 명단을 만들면 지운 순간 그 글이 사라져 A3 가 스스로
# 무너진다. 흡수했다고 적은 글이 전부 ghost 로 잡히고, 마지막엔 명단이 비어 「남은 옛 글
# 0장」이 아무것도 안 세고 통과한다. 그래서 41장은 여기 고정해 둔다 — 이 명단은 늘지도
# 줄지도 않는다.
ROSTER = [
    '2026년에 무엇이 먼저 막히나 — 답이 셋이다',
    'AI 값은 내려가는데 파는 쪽 마진은 오른다',
    'AI가 부른 HBM 수요가 일반 D램 생산까지 갉아먹는다',
    'AMD 칩은 싸졌는데 왜 아직 안 팔리나',
    'SK하이닉스는 사상 최대 이익에도 멀티플 5배가 안 된다',
    '「집이 왜 안 팔리나」에 정부와 학자가 정반대로 답한다',
    '값을 붙잡아 주던 쪽이 빠지고 흐름을 보는 돈만 남았다',
    '같은 1GW인데 매출이 열 배 다르다',
    '같은 날 메타는 코어위브의 고객이자 경쟁자가 됐다',
    '같은 보증 계약을 한쪽은 다리로, 한쪽은 부풀림으로 센다',
    '같은 전력 병목을 두고 한쪽은 벌어진다 하고 한쪽은 곧 풀린다 한다',
    '같은 칩을 두고 2배와 100배가 같이 나온다',
    '공사비를 올린 건 자재값이 아니라 사람과 규정이다',
    '금리와 환율을 국내 수급으로 설명하는 방식이 깨졌다',
    '기준이 몇 채 가졌나에서 그 집에 사는가로 옮겨갔다',
    '깨는 문턱이 다시 묶는 문턱보다 낮다',
    '데이터센터 전력 — 전력망을 안 기다리는 쪽으로',
    '랙 한 대가 먹는 전력이 건물 설계를 정한다',
    '만기 뒤 규칙을 안 정한 채 20년이 지났다',
    '모델을 키우는 돈이 사람 손으로 만드는 과제로 간다',
    '무엇을 고쳐야 통과인지 아무도 말해 주지 않는다',
    '비싸도 자국에서 짓는 쪽으로 각국이 방향을 틀었다',
    '빅테크는 쓴 돈만큼 장부에 담지 않는다',
    '사 오는 과제가 병목이라더니 산 GPU가 74% 놀았다',
    '서울 입주 물량이 집계하는 곳마다 4천 호에서 2만 9천 호까지 나온다',
    '서울에 모자란 집과 새로 내놓는 집이 다르다',
    '수혜 SK하이닉스·삼성·마이크론·KLA: 이익은 최대인데 PER 5배 밑',
    '수혜 마벨·코히어런트·루멘텀·AOI: 성능이 다이 바깥에서 나온다',
    '수혜 엔비디아·AMD, 위기 세레브라스·Groq: 소프트웨어가 1.9배',
    '수혜 컨스텔레이션·비스트라, 위기 탈렌 에너지: 선 설비가 먼저',
    '앤트로픽은 흑자, 오픈AI는 매출만큼 적자',
    '일반 D램을 밀어낸 쪽과 사가는 쪽이 같다',
    '전기요금은 가장 싼 발전기가 아니라 그 순간 가장 비싼 발전기가 정한다',
    '직접 만든 칩은 엔비디아 청구서를 깎는다',
    '클러스터가 땅값을 올린 건 병원과 대학이 이미 있어서다',
    '태양광 3배 계획을 한쪽은 요금으로, 한쪽은 팔 곳으로 센다',
    '토큰 값은 1,000분의 1인데 최신 모델 청구서는 2배다',
    '트랜지스터가 안 줄어드니 성능을 패키지와 메모리에서 뽑는다',
    '한 회계사가 같은 범위의 중간값이라 적고 서로 다른 프리미엄을 쓴다',
    '한 회계사가 경쟁사 두 곳의 할인율을 한쪽은 표로 깔고 한쪽은 한 줄로 놓는다',
    '해협 하나가 막히자 값이 아니라 물량이 문제가 됐다',
]

FINDINGS = []
NEAR = '누가 더 가까이서 봤나'
CLASH = re.compile(r'^##\s*(조건 충돌|어긋나는 자리|갈리는 자리)', re.M)
LI_DIR = 'content/linkedin/'


def add(level, rule, where, msg):
    FINDINGS.append((level, rule, where, msg))


def li_excluded():
    """배제된 게시물의 기준일 집합. li_signal 이 usable=False 로 표시한 것."""
    p = os.path.join(paths.HERE, 'views', 'li_signals.json')
    if not os.path.isfile(p):
        return set()
    d = json.load(io.open(p, encoding='utf-8'))
    return set((s.get('basis_date'), s.get('id')) for s in d.get('signals', [])
               if not s.get('usable'))


def li_usable_dates():
    p = os.path.join(paths.HERE, 'views', 'li_signals.json')
    if not os.path.isfile(p):
        return set()
    d = json.load(io.open(p, encoding='utf-8'))
    return set(s.get('basis_date') for s in d.get('signals', []) if s.get('usable'))


def loop_files():
    return sorted(glob.glob(os.path.join(paths.LOOP, '*.md')))


def old_files():
    return sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md')) +
                  glob.glob(os.path.join(paths.SYNTH, '*.md')))


def main():
    known = axes.all_cell_ids()
    ok_dates = li_usable_dates()
    seen_cell = {}
    merged = []

    for f in loop_files():
        where = os.path.basename(f)
        raw = io.open(f, encoding='utf-8').read()
        meta, body = nl.parse_front(raw)
        aid, cid = meta.get('axis', ''), meta.get('cell', '')
        if (aid, cid) not in known:
            add('FAIL', 'A1', where, '축에 없는 자리다: axis=%r cell=%r' % (aid, cid))
        key = (aid, cid)
        if key in seen_cell:
            add('FAIL', 'A2', where, '%s 와 같은 칸에 두 편이 섰다' % seen_cell[key])
        seen_cell[key] = where

        merged += re.findall(r'^\s*-\s*"(.+?)"\s*$',
                             meta.get('_head', '').split('merged:')[-1].split('sources:')[0], re.M)

        if CLASH.search(body) and NEAR not in body:
            add('WARN', 'S1', where, '충돌 절이 있는데 「%s」가 없다' % NEAR)

        src = nl.sources_of(meta)
        for ref in nl.cite_refs(body, src):
            f2 = (ref.get('file') or '').replace('\\', '/')
            if not f2.startswith(LI_DIR) or not ref.get('lines'):
                continue
            b = nl.li_basis(f2, ref['lines'][0])
            if not b:
                add('FAIL', 'L2', where, '링크드인 인용의 기준일을 못 읽는다: L%d'
                    % ref['lines'][0])
            elif b not in ok_dates:
                add('FAIL', 'L1', where,
                    '배제된 링크드인 게시물을 인용했다: %s L%d' % (b, ref['lines'][0]))

    # A3 — 옛 글 41장이 정확히 한 번씩 흡수됐나. 명단은 ROSTER 고정이다.
    dup = sorted(h for h in set(merged) if merged.count(h) > 1)
    ghost = sorted(h for h in merged if h not in ROSTER)
    left = sorted(h for h in ROSTER if h not in merged)
    for h in dup:
        add('FAIL', 'A3', '-', '두 편이 같은 글을 흡수했다: %r' % h)
    for h in ghost:
        add('FAIL', 'A3', '-', '흡수했다는 글이 없다: %r' % h)
    if left:
        add('WARN', 'A3', '-', '아직 안 흡수된 옛 글 %d장' % len(left))

    for level, rule, where, msg in FINDINGS:
        print('%s %s  %s  %s' % (level, rule, where, msg))
    fails = sum(1 for f in FINDINGS if f[0] == 'FAIL')
    warns = len(FINDINGS) - fails
    print('요약: 축 %d개 / 고리 글 %d편 / 남은 옛 글 %d장 / FAIL %d / WARN %d'
          % (len(axes.AXES), len(loop_files()), len(left), fails, warns))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
