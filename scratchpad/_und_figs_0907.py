# -*- coding: utf-8 -*-
"""2026-09-07 언더스탠딩 성상현 전무 편의 카드 도해.

값은 변환본 md 에 있는 것만 쓴다. 상자 개수도 값이다 — 부채 계정 넷은 화자가
「네 개로 나눈다」고 센 그대로이고, 아래 그림의 사슬 칸은 규제 완화에서 대출까지
화자가 짚은 자리만 둔다. 검증은 이 파일 아래 __main__ 에서 check_fig.hits 로 돌린다.
"""


def _box(x, y, w, h, label, sub='', sub2='', key=False, dash=False, rx=8):
    cls = 'bx-key' if key else 'bx'
    st = ' stroke-dasharray="5 4"' if dash else ''
    out = ['<rect class="%s" x="%d" y="%d" width="%d" height="%d" rx="%d"%s/>'
           % (cls, x, y, w, h, rx, st)]
    cx = x + w / 2.0
    if sub2:
        out.append('<text class="t-lab" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + 26, label))
        out.append('<text class="t-sm" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + 48, sub))
        out.append('<text class="t-sm" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + 68, sub2))
    elif sub:
        out.append('<text class="t-lab" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 - 2, label))
        out.append('<text class="t-sm" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 + 18, sub))
    else:
        out.append('<text class="t-lab" x="%.0f" y="%.0f" text-anchor="middle">%s</text>'
                   % (cx, y + h / 2.0 + 6, label))
    return ''.join(out)


# ── 1 — 긴축을 했는데 순유동성은 안 줄었다 ────────────────────────────────────
# 연준 부채 계정 넷 가운데 자산시장에 닿는 것은 지급준비금 하나뿐이고, 이번 사이클에
# 물이 빠진 자리는 역레포였다. 계정을 나란히 두고 빠져나간 자리만 아래로 뺀다.
def rrp_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 310" role="img">']
    p.append('<text class="t-role" x="8" y="18">연준 대차대조표의 부채 계정</text>')

    xs = [16, 174, 332, 490]
    p.append(_box(xs[0], 34, 134, 74, '현금통화', '시중에 도는 돈'))
    p.append(_box(xs[1], 34, 134, 74, '지급준비금', '자산시장에 닿는', '순유동성은 이것뿐', key=True))
    p.append(_box(xs[2], 34, 134, 74, '역레포', '2조 달러 넘게', '쌓여 있었다'))
    p.append(_box(xs[3], 34, 134, 74, '재무부 일반계좌', '국채를 팔아', '받은 돈'))

    # 빠져나간 물 — 역레포에서만 아래로
    p.append('<path class="flow-cash" d="M399 108 L399 176"/>')
    p.append('<text class="t-cash t-sm" x="410" y="146">재무부가 여기서 뺐다</text>')
    p.append(_box(266, 184, 266, 56, '시장으로 나간 유동성', '연준은 긴축, 재무부는 완화'))

    # 안 빠진 쪽 — 화살표를 두면 여기서도 물이 나간 것으로 읽힌다
    p.append('<text class="t-sm" x="241" y="132" text-anchor="middle">'
             '여기서는 거의 안 빠졌다</text>')
    p.append('<text class="t-sm" x="16" y="270">2023년부터 2025년까지 금리는 올랐고 '
             '양적긴축도 했지만 자산시장은 올랐다</text>')
    p.append('<text class="t-sm" x="16" y="292">2008년부터 2020년까지는 역레포가 비어 있어 '
             '긴축이 곧 순유동성 축소였다</text>')
    p.append('</svg>')
    return ''.join(p)


RRP_CAP = ('연준 대차대조표는 자산이 곧 부채이고, 화자는 그 부채 계정을 넷으로 나눈다. '
           '이 가운데 자산시장에 실제로 닿는 순유동성은 <b>지급준비금</b> 하나다. '
           '2008년부터 2020년까지는 역레포가 비어 있어서 대차대조표가 줄면 곧 지급준비금이 '
           '줄었고, 그래서 긴축이 곧 유동성 축소였다. 이번 사이클에는 역레포에 2조 달러 넘게 '
           '쌓여 있었고 재무부가 그 계좌에서 물을 뺐다. 연준 대차대조표는 줄었는데 자산시장에 '
           '닿는 물은 안 줄어든 자리가 여기다.')


# ── 2 — 물길이 연준에서 시중은행으로 넘어간다 ────────────────────────────────
# 위는 줄어드는 쪽, 아래는 늘어나는 쪽. 둘을 같은 오른쪽 상자로 모아 합이 어디로
# 가는지 보인다. 아래 사슬의 칸은 화자가 짚은 자리(규제 완화 → 풀리는 돈 → 대출)만.
def bank_svg():
    p = ['<svg class="epoch" viewBox="0 0 640 320" role="img">']

    p.append('<text class="t-role" x="8" y="18">연준 — 줄이는 쪽</text>')
    p.append(_box(16, 30, 236, 56, '대차대조표 축소', '만기 온 장기국채를 단기로', dash=True))
    # 줄이는 쪽은 오른쪽 바깥을 타고 내려가 합에서 만난다 — 은행 사슬을 가로지르면
    # 연준이 그 사슬에 물을 대는 것으로 읽힌다
    p.append('<path class="flow-cash" d="M252 58 L632 58 L632 272 L628 272" '
             'stroke-dasharray="5 4"/>')

    p.append('<text class="t-role" x="8" y="120">시중은행 — 늘리는 쪽</text>')
    p.append(_box(16, 132, 190, 84, 'LCR 규제 완화',
                  '고유동성 자산 13% 를', '6.5% 로 낮춘다', key=True))
    p.append('<path class="flow-cash" d="M206 174 L232 174"/>')
    p.append(_box(232, 132, 174, 84, '풀려 나오는 돈',
                  '5,000억 달러에서', '1조 달러', key=True))
    p.append('<path class="flow-cash" d="M406 174 L432 174"/>')
    p.append(_box(432, 132, 186, 84, '대출과 신용창출',
                  '대출이 예금이 되고', '예금이 다시 대출이 된다', key=True))

    p.append('<path class="flow-cash" d="M525 216 L525 240"/>')
    p.append(_box(216, 246, 402, 52, '전체 유동성은 커진다', '광의통화가 늘어나는지로 잰다', key=True))
    p.append('<text class="t-sm" x="16" y="264">국채를 떠안는 기관 중</text>')
    p.append('<text class="t-sm" x="16" y="284">시중은행 비중은 13% 로</text>')
    p.append('<text class="t-sm" x="16" y="304">줄어 있다</text>')
    p.append('</svg>')
    return ''.join(p)


BANK_CAP = ('점선은 줄어드는 쪽, 실선은 늘어나는 쪽이다. 연준이 만기 온 장기국채를 단기로 '
            '갈아타며 대차대조표를 줄여도, 시중은행 쪽에서 그보다 큰 물이 나온다는 것이 이 편의 '
            '그림이다. 통로는 LCR 규제 완화다 — 유동성 없는 자산을 미리 담보로 걸어 두면 그만큼을 '
            '현금으로 쳐 주기 때문에, 미국 은행이 통상 13% 들고 있던 고유동성 자산을 JP모건처럼 '
            '6.5%까지 낮출 수 있다. 화자는 이렇게 나올 돈을 5,000억 달러에서 1조 달러로 잡고, '
            '거기에 대출이 예금이 되고 예금이 다시 대출이 되는 승수가 붙는다고 본다. '
            '그래서 봐야 할 지표는 연준의 금리가 아니라 <b>광의통화가 늘고 있는지</b>다.')


if __name__ == '__main__':
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, fig in (('물이 어디서 빠졌나', rrp_svg()),
                      ('물길이 넘어간다', bank_svg())):
        print(name, check_fig.hits(fig) or 'FAIL 0건')
