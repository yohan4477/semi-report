# -*- coding: utf-8 -*-
"""2026-09-05 언더스탠딩 장순원 기자 편(광명 철산·하안)의 카드 도해 둘.

값은 변환본 md 에 있는 것만 쓴다.
  ① 용적률 계단 — 기둥 하나에 220 · 250 · 280 · 330% 를 쌓고 글자는 오른쪽 지시선으로 뺀다
     (구성비는 기둥 하나, 글자는 조각 위에 쌓지 않는다 — 「글과 도해 — 확정 규칙」 §3)
  ② 고시라는 선 — 같은 지구단위계획인데 진도가 갈린 자리. 시간축 하나에 상태 둘
검증은 이 파일 아래 __main__ 에서 check_fig.hits 로 돌린다.
"""

# ── ① 용적률이 올라간 계단 ───────────────────────────────────────────────────
# 높이는 값에 비례한다. 조각 경계는 원문에 있는 네 값(220·250·280·330)이고
# 사이 증분(30·30·50)은 그 값에서 나온다. 다툼이 붙은 맨 위 조각만 짙게.
_BOT, _TOP, _MAXV = 310.0, 30.0, 330.0
_BX, _BW = 210, 104


def _y(v):
    return _BOT - (_BOT - _TOP) * v / _MAXV


def volume_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 340" role="img">']
    segs = [(0, 220, False), (220, 250, False), (250, 280, False), (280, 330, True)]
    for lo, hi, key in segs:
        y0, y1 = _y(hi), _y(lo)
        p.append('<rect class="%s" x="%d" y="%.1f" width="%d" height="%.1f" rx="3"/>'
                 % ('bx-key' if key else 'bx', _BX, y0, _BW, y1 - y0))
    p.append('<text class="t-lab" x="%d" y="%.0f" text-anchor="middle">330%%</text>'
             % (_BX + _BW / 2, _TOP - 8))

    # 오른쪽 지시선 — 조각마다 한 줄
    labels = [(110, '220% — 기준 용적률, 아무것도 안 해도 준다'),
              (235, '250% — 친환경·전기차 주차장 요건'),
              (263, '280% — 기부채납 6.8% + 종상향 8%'),
              (305, '330% — 중첩용적률로 얹은 50%포인트')]
    ys = {110: _y(110), 235: _y(235), 263: _y(265), 305: _y(305)}
    for k, txt in labels:
        y = ys[k]
        p.append('<line x1="%d" y1="%.1f" x2="358" y2="%.1f" stroke="var(--line,#d8d8d8)" '
                 'stroke-width="1"/>' % (_BX + _BW, y, y))
        cls = 't-cash t-sm' if k == 305 else 't-sm'
        p.append('<text class="%s" x="366" y="%.1f">%s</text>' % (cls, y + 4, txt))

    # 왼쪽 — 견줄 두 선
    for v, txt in ((170, '현황 용적률 170%'), (250, '2종이면 250%가 한계')):
        y = _y(v)
        p.append('<line x1="190" y1="%.1f" x2="%d" y2="%.1f" stroke="var(--line,#d8d8d8)" '
                 'stroke-width="1" stroke-dasharray="4 3"/>' % (y, _BX, y))
        p.append('<text class="t-sm" x="182" y="%.1f" text-anchor="end">%s</text>' % (y + 4, txt))
    p.append('</svg>')
    return ''.join(p)


VOLUME_CAP = ('광명시가 2024년 지구단위계획에서 쌓아 준 계단이다. 2종에서 3종으로 종상향하고 '
              '기준 220%에서 시작해, 친환경·전기차 주차장 요건으로 250%, 기반시설 기부채납 6.8%와 '
              '종상향에 따른 8%로 280%까지 간다. 그 위에 다른 법의 인센티브를 얹어 쓰는 '
              '<b>중첩용적률</b>로 330%가 됐다. 다툼이 붙은 곳은 맨 위 50%포인트다 — 시가 이 구간을 '
              '임대주택으로 채우든 친환경 인증으로 채우든 고르게 했고, 조합은 전부 친환경을 골랐다. '
              '현황 용적률이 170%이고 2종 그대로면 250%가 한계였다는 것이 이만큼 얹어 준 이유다.')


# ── ② 고시라는 선 ────────────────────────────────────────────────────────────
# 같은 지구단위계획에 묶였는데 진도가 갈렸다. 공문은 한 장인데 한쪽에는 고시 뒤에,
# 다른 쪽에는 고시 전에 닿는다. 그 차이가 이 편의 전부다.
def notice_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 280" role="img">']

    p.append('<rect class="bx-key" x="150" y="16" width="300" height="44" rx="8"/>')
    p.append('<text class="t-lab" x="300" y="36" text-anchor="middle">광명시 협조 공문</text>')
    p.append('<text class="t-sm" x="300" y="52" text-anchor="middle">'
             '임대주택 공급 계획을 반영해 주세요</text>')

    p.append('<text class="t-role" x="8" y="96">철산 12·13단지</text>')
    p.append('<rect class="bx" x="108" y="106" width="150" height="52" rx="8"/>')
    p.append('<text class="t-sm" x="183" y="130" text-anchor="middle">정비계획 수립</text>')
    p.append('<text class="t-sm" x="183" y="148" text-anchor="middle">협의</text>')
    p.append('<line x1="276" y1="100" x2="276" y2="164" stroke="var(--line,#d8d8d8)" '
             'stroke-width="1.6"/>')
    p.append('<text class="t-sm" x="276" y="94" text-anchor="middle">고시</text>')
    p.append('<rect class="bx" x="294" y="106" width="206" height="52" rx="8"/>')
    p.append('<text class="t-sm" x="397" y="130" text-anchor="middle">설계와 사업성 분석이 끝났다</text>')
    p.append('<text class="t-sm" x="397" y="148" text-anchor="middle">재산권 결정도 내렸다</text>')
    p.append('<path class="flow-cash" d="M300 60 L300 100"/>')

    p.append('<text class="t-role" x="8" y="196">하안지구 단지들</text>')
    p.append('<rect class="bx" x="108" y="206" width="150" height="52" rx="8"/>')
    p.append('<text class="t-sm" x="183" y="236" text-anchor="middle">아직 협의 중</text>')
    p.append('<line x1="276" y1="200" x2="276" y2="264" stroke="var(--line,#d8d8d8)" '
             'stroke-width="1.6" stroke-dasharray="5 4"/>')
    p.append('<text class="t-sm" x="276" y="194" text-anchor="middle">고시 전</text>')
    p.append('<rect class="bx" x="294" y="206" width="206" height="52" rx="8" '
             'stroke-dasharray="5 4"/>')
    p.append('<text class="t-sm" x="397" y="236" text-anchor="middle">아직 정해진 것이 없다</text>')
    p.append('<path class="flow-cash" d="M450 38 L560 38 L560 232 L506 232"/>')

    p.append('</svg>')
    return ''.join(p)


NOTICE_CAP = ('공문은 한 장인데 닿는 자리가 다르다. 14개 단지가 같은 지구단위계획에 묶여 있지만 '
              '철산 12·13단지는 정비계획 고시가 끝나 설계와 사업성 분석을 마쳤고 그 조건 위에서 '
              '집을 팔거나 안 판 사람들이 있다. 하안지구는 아직 고시 전이라 협의 단계다. '
              '진행자가 긋는 선이 여기다 — <b>고시 전이라면 시가 방침을 바꿔 요구해도 어쩔 수 없고, '
              '고시 뒤라면 소급이다.</b> 광명 건이 성수지구와 다른 점은 상위계획이나 조례가 바뀐 것이 '
              '아니라 시의 방침만 바뀌었다는 것이다.')


if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, fig in (('용적률 계단', volume_svg()), ('고시라는 선', notice_svg())):
        print(name, check_fig.hits(fig) or 'FAIL 0건')
