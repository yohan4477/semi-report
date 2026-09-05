# -*- coding: utf-8 -*-
"""2026-09-05 언더스탠딩 권석준 교수 1·2부의 카드 도해.

값은 전부 변환본 md 에 있는 것만 쓴다. 상자 개수는 원문이 센 개수와 같다
(병목 셋은 화자가 「병목 1·2·3」으로 나눈 그대로다).
검증은 이 파일 아래 __main__ 에서 check_fig.hits 로 돌린다.
"""


def _box(x, y, w, h, label, sub='', key=False, rx=8):
    """상자 하나. label 은 굵게, sub 는 그 아래 작은 글씨."""
    cls = 'bx-key' if key else 'bx'
    out = ['<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="%d"/>' % (cls, x, y, w, h, rx)]
    cx = x + w / 2.0
    if sub:
        out.append('<text class="t-lab" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 - 2, label))
        out.append('<text class="t-sm" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 + 16, sub))
    else:
        out.append('<text class="t-lab" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 + 6, label))
    return ''.join(out)


# ── 1부 — 번 돈이 어디로 가나 ────────────────────────────────────────────────
# 예전에는 증산이 곧 미국 장비 구매였고, 지금은 그 돈이 중국 안에서 한 바퀴 돈다.
# 화자가 「승수 효과」라 부른 대목이라 오른쪽에만 되돌아오는 선을 둔다.
def loop_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 330" role="img">']
    p.append('<text class="t-role" x="8" y="18">예전 (5~10년 전)</text>')
    p.append('<text class="t-role" x="336" y="18">지금</text>')
    p.append('<line x1="320" y1="30" x2="320" y2="320" stroke="var(--line,#d8d8d8)" '
             'stroke-width="1" stroke-dasharray="4 4"/>')

    # 왼쪽 — 돈이 밖으로 나간다
    p.append(_box(20, 40, 280, 56, 'CXMT 가 번 돈', '메모리 값이 4배에서 5~6배로 올랐다'))
    p.append('<path class="flow-cash" d="M160 96 L160 158"/>')
    p.append('<text class="t-cash t-sm" x="170" y="132">장비를 사러 나간다</text>')
    p.append(_box(20, 166, 280, 56, '미국·일본·네덜란드 장비사',
                  'ASML · 도쿄일렉트론 · 미국 장비회사'))
    p.append('<text class="t-sm" x="160" y="252" text-anchor="middle">'
             '증산은 곧 해외 장비 구매였다</text>')

    # 오른쪽 — 돈이 중국 안에서 돈다
    p.append(_box(348, 40, 272, 50, 'CXMT 가 번 돈', key=True))
    p.append('<path class="flow-cash" d="M484 90 L484 132"/>')
    p.append(_box(348, 140, 272, 50, '중국 장비사 · 화웨이 · 중국 AI 데이터센터'))
    p.append('<path class="flow-cash" d="M484 190 L484 232"/>')
    p.append(_box(348, 240, 272, 50, '중국 안에서 장비가 만들어진다',
                  'AMEC · 나우라, R&D 급 DUV 까지 왔다'))
    # 되돌아오는 고리 — 오른쪽 바깥을 타고 위로
    p.append('<path class="flow-cash" d="M620 265 C 636 265 636 65 624 65"/>')
    p.append('<text class="t-cash t-sm" x="612" y="176" text-anchor="end">'
             'CXMT 경쟁력으로 되돌아온다</text>')
    p.append('</svg>')
    return ''.join(p)


LOOP_CAP = ('왼쪽과 오른쪽은 같은 돈이다. 예전에는 증산이 곧 해외 장비 구매여서 번 돈이 '
            'ASML·도쿄일렉트론·미국 장비회사로 빠져나갔다. 지금은 그 돈이 중국 장비사와 '
            '화웨이, 중국 AI 데이터센터로 가고 거기서 만든 장비가 다시 CXMT 로 돌아온다. '
            '권석준 교수가 <b>미국이 장비 수출을 조일수록 중국 장비사가 자리를 잡는다</b>고 '
            '말한 대목이 이 고리다. 다만 남은 격차인 리소그래피는 아직 이 고리 밖에 있다.')


# ── 2부 — 늘어나는 것과 정점을 지나는 것 ─────────────────────────────────────
# 같은 2028년을 놓고 매출은 늘고 웨이퍼당 수익률만 꺾인다. 축이 둘이라 좌우로 가른다.
def peak_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 300" role="img">']
    p.append('<text class="t-role" x="8" y="18">2028년, 중국 물량이 나온 뒤</text>')

    p.append(_box(16, 36, 296, 96, '늘어나는 것', key=True))
    p.append('<text class="t-sm" x="164" y="96" text-anchor="middle">매출액과 영업이익</text>')
    p.append('<text class="t-sm" x="164" y="116" text-anchor="middle">'
             '값은 내려가도 남는 물량이 팔린다</text>')

    p.append(_box(328, 36, 296, 96, '정점을 지나는 것'))
    p.append('<text class="t-sm" x="476" y="96" text-anchor="middle">웨이퍼 한 장당 순수익</text>')
    p.append('<text class="t-bad t-sm" x="476" y="116" text-anchor="middle">'
             '7% 에서 17% 까지 떨어진다</text>')

    # 시간 띠 — 상태 둘, 높이는 쓰지 않는다
    p.append('<text class="t-role" x="8" y="176">주가가 먼저 움직이는 자리</text>')
    p.append('<line x1="24" y1="238" x2="616" y2="238" stroke="var(--line,#d8d8d8)" '
             'stroke-width="1.2"/>')
    p.append('<rect class="bx" x="24" y="196" width="272" height="42" rx="6"/>')
    p.append('<rect class="bx-key" x="304" y="196" width="176" height="42" rx="6"/>')
    p.append('<rect class="bx" x="488" y="196" width="128" height="42" rx="6"/>')
    p.append('<text class="t-sm" x="160" y="222" text-anchor="middle">아직 확정된 것이 없다</text>')
    p.append('<text class="t-sm" x="392" y="222" text-anchor="middle">신호가 보이기 시작한다</text>')
    p.append('<text class="t-sm" x="552" y="222" text-anchor="middle">물량이 나온다</text>')
    p.append('<text class="t-sm" x="24" y="260">지금</text>')
    p.append('<text class="t-sm" x="304" y="260">신호가 보이기 시작하는 때</text>')
    p.append('<text class="t-sm" x="488" y="260">2028년</text>')
    p.append('<text class="t-sm" x="24" y="286">권석준 교수는 값 조정이 오른쪽 칸이 아니라 '
             '가운데 칸에서 시작된다고 본다</text>')
    p.append('</svg>')
    return ''.join(p)


PEAK_CAP = ('같은 2028년인데 두 값이 반대로 간다. 값이 내려가도 남는 물량은 팔리니 매출액과 '
            '영업이익은 절대 수치로 계속 늘고, 애널리스트들이 보는 웨이퍼 한 장당 순수익만 '
            '7%에서 17%까지 떨어진다. 아래 띠가 이 편의 요점이다. 물량이 실제로 나오는 때는 '
            '2028년이지만, <b>값이 조정되는 자리는 그 앞 칸</b>이다. 걱정할 만한 신호가 실제로 '
            '관측되는 때가 아니라 그 신호가 보이기 시작하는 때에 먼저 반영된다고 보기 때문이다.')


if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, fig in (('돈이 도는 고리', loop_svg()),
                      ('늘어나는 것과 정점', peak_svg())):
        print(name, check_fig.hits(fig) or 'FAIL 0건')
