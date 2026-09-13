# -*- coding: utf-8 -*-
u"""TSMC 그림 장 1절 전체 지도 — 받은 손 그림(tsmc_map_orig)의 상자·글자·색·굵기는 그대로 두고
선만 다시 긋는다(2026-09-13 「전체지도 개판이네」).

받은 그림은 곡선이 상자 위를 지나고(HBM 점선이 인텔·소니 글자를 덮었다) 화살촉이 선 굵기를
따라 커져 엔비디아·애플 상자를 가렸다. 여기서는 탐색기와 같은 규칙으로 긋는다 — 칸 사이 통로
에서만 세로로 움직이고(가로·세로·가로 세 토막), 화살촉 크기는 고정, 같은 통로의 선은 자리를
나눠 겹치지 않는다. 상자 좌표는 원문 SVG 그대로다.
"""

W, H = 960, 560

# 칸: (x, w). 통로는 칸 사이 빈 폭
COL = {'t2': (10, 180), 't1': (235, 190), 'tsmc': (470, 110), 'cust': (620, 150), 'fin': (800, 150)}

# 상자: id → (col, y, h, fill, stroke, dashed, [(line, muted)])
BOX = [
    ('hemlock', 't2', 40, 34, '#fff', '#C9D1DA', False, [(u'Hemlock · Wacker · OCI (폴리실리콘)', False)]),
    ('stella', 't2', 84, 34, '#F3D5DC', '#9B1C3A', False, [(u'Stella · Morita (불산)', False)]),
    ('hoya', 't2', 128, 34, '#F3D5DC', '#9B1C3A', False, [(u'Hoya · AGC (EUV 블랭크)', False)]),
    ('zeiss', 't2', 172, 34, '#fff', '#C9D1DA', False, [(u'Zeiss · Cymer · Trumpf', False)]),
    ('edwards', 't2', 216, 34, '#fff', '#C9D1DA', False, [(u'Edwards · MKS · Ichor', False)]),
    ('ajinomoto', 't2', 260, 34, '#F3D5DC', '#9B1C3A', False, [(u'Ajinomoto (ABF 필름)', False)]),

    ('wafer', 't1', 40, 34, '#fff', '#8A96A3', False, [(u'SEH · SUMCO · GlobalWafers', False), (u'웨이퍼 6사 92~96%', True)]),
    ('siltron', 't1', 84, 34, '#F6E3C8', '#B4620A', False, [(u'SK실트론 → 두산', False), (u'2026.7 SPA 2.3조', True)]),
    ('resist', 't1', 128, 34, '#F3D5DC', '#9B1C3A', False, [(u'JSR · TOK · Shin-Etsu', False), (u'EUV 레지스트 90%+', True)]),
    ('asml', 't1', 172, 34, '#fff', '#8A96A3', False, [(u'ASML (EUV 100%)', False), (u'매입 1위 ~19% 추정', True)]),
    ('equip', 't1', 216, 34, '#fff', '#8A96A3', False, [(u'AMAT · Lam · KLA · TEL', False), (u'TEL 트랙 = 일본 병목', True)]),
    ('abf', 't1', 260, 34, '#fff', '#8A96A3', False, [(u'Ibiden · Unimicron · Kinsus', False), (u'ABF 기판', True)]),
    ('specialty', 't1', 304, 34, '#F6E3C8', '#B4620A', False, [(u'SK스페셜티 → 한앤코', False), (u'NF3·WF6 1위, 2025.3', True)]),
    ('gas', 't1', 348, 34, '#fff', '#8A96A3', False, [(u'Linde LienHwa · Air Liquide', False), (u'가스 9사', True)]),
    ('dist', 't1', 392, 34, '#fff', '#8A96A3', True, [(u'Wah Lee · Topco · Kanto-PPC', False), (u'유통·합작 중개', True)]),
    ('power', 't1', 436, 34, '#fff', '#8A96A3', False, [(u'대만전력 · 용수', False), (u'원가 ~7~8%', True)]),

    ('nvidia', 'cust', 60, 40, '#D9E2EF', '#31507A', False, [(u'NVIDIA', False), (u'2위 17% → 2026 1위', True)]),
    ('apple', 'cust', 110, 40, '#D9E2EF', '#31507A', False, [(u'Apple', False), (u'1위 19% (하락 중)', True)]),
    ('amd', 'cust', 160, 34, '#fff', '#31507A', False, [(u'AMD · Broadcom · Marvell', False)]),
    ('qcom', 'cust', 204, 34, '#fff', '#31507A', False, [(u'Qualcomm · MediaTek', False)]),
    ('hyper', 'cust', 248, 34, '#fff', '#31507A', False, [(u'Google·AWS·MS 자체칩', False)]),
    ('intel', 'cust', 292, 34, '#fff', '#31507A', False, [(u'Intel (외주분)', False)]),
    ('sony', 'cust', 336, 34, '#fff', '#31507A', False, [(u'Sony·NXP·Infineon', False)]),

    ('f_hyper', 'fin', 60, 44, '#fff', '#C9D1DA', False, [(u'하이퍼스케일러 4사', False), (u'MS·Meta·Google·AWS', True)]),
    ('f_foxconn', 'fin', 114, 34, '#fff', '#C9D1DA', False, [(u'Foxconn → 소비자', False)]),
    ('f_server', 'fin', 158, 34, '#fff', '#C9D1DA', False, [(u'서버 조립 Quanta·Dell', False)]),
    ('f_phone', 'fin', 202, 34, '#fff', '#C9D1DA', False, [(u'삼성·샤오미 (폰 OEM)', False)]),
    ('f_auto', 'fin', 336, 34, '#fff', '#C9D1DA', False, [(u'자동차 OEM', False)]),
]
TSMC = (470, 150, 110, 200)   # x, y, w, h
OSAT = (445, 400, 160, 40)
HBM = (445, 470, 160, 40)   # 밑줄 글자가 상자 폭을 넘지 않게 140 → 160

# 선: (from, to, 굵기, 색). 굵기는 받은 그림의 「대략적 금액 규모」 그대로, 최대만 4 → 3 으로 눌렀다
T2_T1 = [('hemlock', 'wafer'), ('stella', 'gas'), ('hoya', 'resist'), ('zeiss', 'asml'),
         ('edwards', 'equip'), ('ajinomoto', 'abf')]
T1_TSMC = [('wafer', 2.5), ('siltron', 1.2), ('resist', 1.5), ('asml', 3), ('equip', 3),
           ('abf', 1.2), ('specialty', 1), ('gas', 1.2), ('dist', 1), ('power', 1.5)]
TSMC_CUST = [('nvidia', 3), ('apple', 3), ('amd', 2), ('qcom', 1.5), ('hyper', 2), ('intel', 1), ('sony', 1.2)]
CUST_FIN = [('nvidia', 'f_hyper'), ('apple', 'f_foxconn'), ('amd', 'f_server'), ('qcom', 'f_phone'),
            ('hyper', 'f_hyper'), ('sony', 'f_auto')]

GREY, NAVY, TEAL, ORANGE = '#8A96A3', '#31507A', '#0E6B66', '#B4620A'


def _box(bid):
    for b in BOX:
        if b[0] == bid:
            x, w = COL[b[1]]
            return x, b[2], w, b[3]
    raise KeyError(bid)


def _path(x0, y0, gx, x1, y1):
    u"""가로 → 통로에서 세로 → 가로. 높이가 같으면 곧게."""
    if abs(y0 - y1) < 0.5:
        return 'M%d %dH%d' % (x0, y0, x1)
    return 'M%d %dH%d V%d H%d' % (x0, y0, gx, y1, x1)


def render():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="TSMC value chain map">' % (W, H),
         '<defs>',
         # 화살촉은 선 굵기를 따라 커지지 않는다 — 받은 그림에서 4px 선의 촉이 상자를 가렸다
         '<marker id="ma" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5 0 10z" fill="%s"/></marker>' % GREY,
         '<marker id="mn" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5 0 10z" fill="%s"/></marker>' % NAVY,
         '<marker id="mt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5 0 10z" fill="%s"/></marker>' % TEAL,
         '<marker id="mo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5 0 10z" fill="%s"/></marker>' % ORANGE,
         '</defs>']
    # 칸 머리글
    o.append('<g font-size="13" fill="#6B7785"><text x="10" y="22">Tier 2 원료·부품</text>'
             '<text x="235" y="22">Tier 1 소재·장비·유통</text><text x="600" y="22">고객</text>'
             '<text x="800" y="22">최종 수요</text></g>')
    # 상자
    o.append('<g font-size="12" fill="#1C2733">')
    for bid, col, y, h, fill, stroke, dashed, lines in BOX:
        x, w = COL[col]
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s"%s/>'
                 % (x, y, w, h, fill, stroke, ' stroke-dasharray="4 3"' if dashed else ''))
        # 긴 이름은 글자를 조금 줄여 상자 안에 둔다(받은 그림은 상자 밖으로 삐져나갔다)
        fs = lambda t: ' font-size="11"' if len(t) > 24 else ''
        if len(lines) == 1:
            o.append('<text x="%d" y="%d"%s>%s</text>' % (x + 10, y + 22, fs(lines[0][0]), lines[0][0]))
        else:
            o.append('<text x="%d" y="%d"%s>%s</text>' % (x + 10, y + 15, fs(lines[0][0]), lines[0][0]))
            o.append('<text x="%d" y="%d" fill="#6B7785">%s</text>' % (x + 10, y + 29, lines[1][0]))
    o.append('</g>')
    # TSMC
    tx, ty, tw, th = TSMC
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s"/>' % (tx, ty, tw, th, TEAL))
    o.append('<g fill="#fff" font-size="13" text-anchor="middle">'
             '<text x="525" y="205" font-size="20" font-weight="600">TSMC</text>'
             '<text x="525" y="228">매출 $1,224억</text><text x="525" y="246">GM 59.9%</text>'
             '<text x="525" y="264">1,500만 장</text>'
             '<text x="525" y="290" font-size="11" opacity=".85">원재료 ~17%</text>'
             '<text x="525" y="306" font-size="11" opacity=".85">감가상각 ~45%</text></g>')
    # OSAT · HBM
    ox, oy, ow, oh = OSAT
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="#D6ECEA" stroke="%s"/>' % (ox, oy, ow, oh, TEAL))
    o.append('<text x="525" y="416" text-anchor="middle" font-size="12">ASE·SPIL · Amkor</text>'
             '<text x="525" y="431" text-anchor="middle" font-size="11" fill="#6B7785">CoWoS 외주 24~27만 장</text>')
    o.append('<path d="M525 350V%d" stroke="%s" stroke-width="2" fill="none" marker-end="url(#mt)"/>' % (oy, TEAL))
    hx, hy, hw, hh = HBM
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="#F6E3C8" stroke="%s"/>' % (hx, hy, hw, hh, ORANGE))
    o.append('<text x="525" y="486" text-anchor="middle" font-size="12">SK hynix HBM</text>'
             '<text x="525" y="501" text-anchor="middle" font-size="11" fill="#6B7785">고객이 별도 조달 → CoWoS 합류</text>')
    o.append('<path d="M525 %d V%d" stroke="%s" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>' % (hy, oy + oh, ORANGE))

    # ── 선 ──
    # Tier 2 → Tier 1: 통로 190~235. 세로로 가는 선은 통로 안에서 자리를 나눈다
    o.append('<g stroke="%s" fill="none" marker-end="url(#ma)">' % GREY)
    gx0, gx1 = 190, 235
    verticals = [e for e in T2_T1 if _box(e[0])[1] != _box(e[1])[1]]
    for i, (a, b) in enumerate(T2_T1):
        ax, ay, aw, ah = _box(a); bx, by, bw, bh = _box(b)
        gx = gx0 + 8 + (verticals.index((a, b)) + 1) * (gx1 - gx0 - 16) / (len(verticals) + 1) if (a, b) in verticals else gx0
        o.append('<path d="%s" stroke-width="1.2"/>' % _path(ax + aw, ay + ah / 2, gx, bx, by + bh / 2))
    o.append('</g>')

    # Tier 1 → TSMC: 통로 425~470. 닿는 높이는 TSMC 왼쪽 변에 위에서 아래로 나눠 준다.
    # 위 상자는 위 자리, 아래 상자는 아래 자리 — 선이 서로 안 엇갈린다
    o.append('<g stroke="%s" fill="none" marker-end="url(#ma)">' % GREY)
    n = len(T1_TSMC)
    ys = [ty + 16 + i * (th - 32) / (n - 1) for i in range(n)]
    gx0, gx1 = 425, 470
    for i, (a, wd) in enumerate(T1_TSMC):
        ax, ay, aw, ah = _box(a)
        # 통로 자리: 멀리 가는 선(위·아래 끝)이 바깥쪽, 가까운 선이 안쪽 — 세로 토막이 서로 안 겹친다
        gx = gx0 + 6 + (n - 1 - i) * (gx1 - gx0 - 12) / (n - 1) if ay + ah / 2 < ys[i] else gx0 + 6 + i * (gx1 - gx0 - 12) / (n - 1)
        o.append('<path d="%s" stroke-width="%s"/>' % (_path(ax + aw, ay + ah / 2, gx, tx, ys[i]), wd))
    o.append('</g>')

    # TSMC → 고객: 통로 580~620
    o.append('<g stroke="%s" fill="none" marker-end="url(#mn)">' % NAVY)
    n = len(TSMC_CUST)
    ys = [ty + 20 + i * (th - 40) / (n - 1) for i in range(n)]
    gx0, gx1 = 580, 620
    for i, (b, wd) in enumerate(TSMC_CUST):
        bx, by, bw, bh = _box(b)
        gx = gx0 + 6 + i * (gx1 - gx0 - 12) / (n - 1) if by + bh / 2 < ys[i] else gx0 + 6 + (n - 1 - i) * (gx1 - gx0 - 12) / (n - 1)
        o.append('<path d="%s" stroke-width="%s"/>' % (_path(tx + tw, ys[i], gx, bx, by + bh / 2), wd))
    o.append('</g>')

    # 고객 → 최종 수요: 통로 770~800
    o.append('<g stroke="%s" fill="none" marker-end="url(#ma)" stroke-width="1.2">' % GREY)
    gx0, gx1 = 770, 800
    for i, (a, b) in enumerate(CUST_FIN):
        ax, ay, aw, ah = _box(a); bx, by, bw, bh = _box(b)
        ty0, ty1 = ay + ah / 2, by + bh / 2
        # 같은 상자(하이퍼스케일러)로 드는 둘째 선은 닿는 높이를 아래로 비켜 준다
        if b == 'f_hyper' and a == 'hyper':
            ty1 = by + bh - 10
        gx = gx0 + 8 + (i % 3) * 7
        o.append('<path d="%s"/>' % _path(ax + aw, ty0, gx, bx, ty1))
    o.append('</g>')

    # HBM → NVIDIA(점선): 상자 위를 지나지 않게 TSMC·고객 통로(x=612)로 올라가 엔비디아 왼쪽 변 아래쪽에 닿는다
    nx, ny, nw, nh = _box('nvidia')
    o.append('<path d="M%d %d H617 V%d H%d" stroke="%s" stroke-width="1.5" stroke-dasharray="4 3" fill="none" marker-end="url(#mo)"/>'
             % (hx + hw, hy + hh / 2, ny + nh - 8, nx, ORANGE))
    o.append('<text x="705" y="440" font-size="11" fill="%s">HBM은 NVIDIA 원가에서</text>'
             '<text x="705" y="454" font-size="11" fill="%s">TSMC보다 큼 (~$3.5k vs ~$2.3k)</text>' % (ORANGE, ORANGE))
    o.append('<text x="10" y="545" font-size="11" fill="#6B7785">선 굵기 = 대략적 금액 규모. 점선 박스 = 중개·유통. 한국 노드 2곳은 2025~26년 SK그룹에서 이탈.</text>')
    o.append('</svg>')
    return '\n      '.join(o)


SECTION_1 = u'''  <!-- 1. 전체 지도 -->
  <section>
    <h2>1. 전체 지도<small>앞단 → TSMC → 뒷단</small></h2>
    <p class="note">굵은 선이 돈이 가장 많이 흐르는 경로. 색은 소속: 청록 TSMC, 주황 한국 노드, 진홍 일본 단일소스 병목, 남색 고객.</p>
    %s
    <div class="legend"><span class="l-tsmc">TSMC·외주</span><span class="l-kr">한국 노드</span><span class="l-jp">일본 단일소스 병목</span><span class="l-cust">고객</span><span class="l-sup">기타 공급사</span></div>
  </section>
'''


def section():
    return SECTION_1 % render()
