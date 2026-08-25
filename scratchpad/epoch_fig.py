# -*- coding: utf-8 -*-
"""Epoch AI 장의 도해 — 원문 그림을 한국어 인라인 SVG로 다시 그린다.

원문(epoch.ai) 도해는 라벨이 전부 영어라 그대로 실으면 카드 본문만 한국어가 된다.
그래서 값과 구조는 원문 그대로 두고 판을 새로 짠다. 규칙은 둘이다.
  · insight-figure 스킬 — 없는 값 금지·좌표 계산·판 위 글자 금지·검사기
  · docs/흐름도 — 만드는 규칙.md — 선 세 종류·역할 도랑·강조 한 종류·숫자는 상자 안

글자 폭은 여기서 재서 상자 밖으로 나가면 그 자리에서 멈춘다. check_fig.py는 한 글자를
9px로 어림하는데 한글은 글자 크기만큼 넓어서, 검사기만 믿으면 한글 줄이 상자를 넘는다.
"""


def w(s, fs):
    """글자 폭 어림 — 한글·한자·기호는 글자 크기만큼, 라틴·숫자는 그 55%."""
    return sum(fs if ord(c) > 0x2E80 else fs * 0.55 for c in s)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ── 부품 ──────────────────────────────────────────────────────────────
def box(x, y, bw, name, lines, key=False, wrap=False):
    """상자 하나. 이름 한 줄 + 설명 여러 줄. 높이는 줄 수가 정한다.

    설명은 그 주체가 하는 동사로 쓴다(규칙 5). 숫자는 이 상자 안에만 산다."""
    h = 26 + 15 * len(lines) + 8
    cls = 'bx-wrap' if wrap else ('bx-key' if key else 'bx')
    o = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" class="%s"/>' % (x, y, bw, h, cls)]
    assert w(name, 11.5) < bw - 22, '상자 이름이 넘친다: %s' % name
    o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (x + 11, y + 20, esc(name)))
    for i, ln in enumerate(lines):
        assert w(ln, 10) < bw - 22, '설명 줄이 상자를 넘는다(%d px): %s' % (bw, ln)
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>'
                 % (x + 11, y + 38 + 15 * i, esc(ln)))
    return ''.join(o), h


def arrow(kind, pts):
    """직각으로만 꺾는 선. kind = cash | svc | cond."""
    d = 'M%d %d' % pts[0] + ''.join(' L%d %d' % p for p in pts[1:])
    return '<path d="%s" class="flow-%s"/>' % (d, kind)


def lab(x, y, s, cash=False, anchor='start', fs=10):
    """선 위 글자 — 오가는 것의 이름. 색은 그 선의 색을 따른다(규칙 6)."""
    cls = 't-cash' if cash else 't-sm'
    a = '' if anchor == 'start' else ' text-anchor="%s"' % anchor
    return ('<text x="%d" y="%d" class="%s"%s style="font-size:%spx">%s</text>'
            % (x, y, cls, a, fs, esc(s)))


def role(cx, y, s):
    """역할 도랑 라벨 — 상자 밖에 세운다(규칙 3)."""
    return '<text x="%d" y="%d" class="t-role" text-anchor="middle">%s</text>' % (cx, y, esc(s))


def head(cx, y, s):
    return '<text x="%d" y="%d" class="t-lab" text-anchor="middle">%s</text>' % (cx, y, esc(s))


def legend(y=22):
    """선 세 줄 범례 — 그림마다 똑같은 문구로 판 위쪽에 둔다(규칙 2).

    조건부 지원을 실선으로 그리면 「보증이 있다」로 읽힌다. 대시로 가른다."""
    items = [('cash', '돈이 흐른다'), ('svc', '물건·용역·리스가 간다'),
             ('cond', '부도 뒤에만 작동하는 조건부 지원')]
    o, x = [], 16
    for kind, text in items:
        o.append(arrow(kind, [(x, y - 4), (x + 20, y - 4)]))
        o.append(lab(x + 26, y, text, cash=(kind == 'cash'), fs=9.5))
        x += 26 + int(w(text, 9.5)) + 20
    assert x < 645, '범례가 판을 넘는다: %d' % x
    return ''.join(o)


def svg(h, body):
    return ('<svg viewBox="0 0 640 %d" role="img" xmlns="http://www.w3.org/2000/svg">%s</svg>'
            % (h, body))


# ── 그래프 부품 — 막대·띠 ────────────────────────────────────────────────
# 눈금값은 t-axis로 표시한다. 축의 눈금이지 원문에서 가져온 값이 아니라서
# 값 대조에서 뺀다(맨 아래 num_check). 막대 길이는 원문에 있는 값만 쓴다.
def xaxis(x0, x1, y, ticks, vmax, title, fmt='%g'):
    o = ['<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
         % (x0, y, x1 + 14, y)]
    for v in ticks:
        tx = x0 + int((x1 - x0) * v / float(vmax))
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
                 % (tx, y, tx, y + 5))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (tx, y + 18, fmt % v))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" style="font-weight:800">%s</text>'
             % ((x0 + x1) // 2, y + 34, esc(title)))
    return ''.join(o), y + 45


def yaxis(x, y0, y1, ticks, vmax, title, fmt='%g'):
    o = ['<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
         % (x, y0 - 8, x, y1)]
    for v in ticks:
        ty = y1 - int((y1 - y0) * v / float(vmax))
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
                 % (x - 5, ty, x, ty))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="end">%s</text>'
                 % (x - 9, ty + 4, fmt % v))
    o.append('<text x="%d" y="%d" class="t-sm" style="font-weight:800">%s</text>'
             % (x - 40, y0 - 16, esc(title)))
    return ''.join(o)


def swatch(x, y, text, key=True):
    fill = ('class="bx-key"' if key else
            'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" stroke-width="1"')
    return ('<rect x="%d" y="%d" width="14" height="11" rx="2" %s/>' % (x, y - 10, fill)
            + lab(x + 20, y, text, fs=9.5))


def barh(rows, vmax, ticks, title, x0=150, x1=452, y=52, bh=24, step=34):
    """가로 막대. rows = [(라벨, 값, 오른쪽 글자, 강조)]. 라벨은 축 왼쪽에 오른쪽 맞춤."""
    o = []
    for name, val, note, key in rows:
        bw_ = max(2, int((x1 - x0) * val / float(vmax)))
        fill = ('fill="var(--fig-good,#2f8f6b)"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
                     'stroke-width="1"')
        assert w(name, 10) < x0 - 16, '막대 라벨이 축을 넘는다: %s' % name
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" %s/>' % (x0, y, bw_, bh, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" style="font-weight:850">%s</text>'
                 % (x0 - 10, y + bh - 8, esc(name)))
        assert x0 + bw_ + 10 + w(note, 10) < 638, '막대 옆 값이 판을 넘는다: %s' % note
        o.append(lab(x0 + bw_ + 10, y + bh - 8, note, fs=10))
        y += step
    ax, bottom = xaxis(x0, x1, y - step + bh + 8, ticks, vmax, title)
    return o + [ax], bottom


def barv(rows, vmax, ticks, ytitle, x0=96, y0=54, y1=210, bw_=64, step=118):
    """세로 막대. rows = [(x라벨, 값, 막대 위 글자, 강조)]."""
    o = [yaxis(x0, y0, y1, ticks, vmax, ytitle)]
    x = x0 + 40
    for name, val, note, key in rows:
        h = max(2, int((y1 - y0) * val / float(vmax)))
        fill = ('fill="var(--fig-good,#2f8f6b)"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
                     'stroke-width="1"')
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" %s/>'
                 % (x, y1 - h, bw_, h, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
                 'style="font-weight:850">%s</text>' % (x + bw_ // 2, y1 - h - 8, esc(note)))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (x + bw_ // 2, y1 + 17, esc(name)))
        x += step
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (x0, y1, x - step + bw_ + 30, y1))
    return o, y1 + 28


# ── ① 두 칸 대조 — 컴퓨트와 데이터센터가 같은 구조다 ─────────────────────
def fig_two_columns():
    LX, RX, BW = 16, 344, 280
    lcx, rcx = LX + BW // 2, RX + BW // 2
    o = [legend()]
    o.append(head(lcx, 48, '컴퓨트'))
    o.append(head(rcx, 48, '데이터센터'))
    o.append('<text x="%d" y="62" class="t-sm" text-anchor="middle">장비 부채 345억 달러</text>'
             % lcx)
    o.append('<text x="%d" y="62" class="t-sm" text-anchor="middle">'
             '한 예로 든 레이크 매리너 32억 달러</text>' % rcx)
    rows = [
        ('대출',
         ('기관투자자', ['아폴로 운용 펀드가 주도하고', '블랙스톤·글로벌 은행이 참여한다',
                    '345억 달러 부채를 확약했다'], False),
         ('기관투자자', ['레이크 매리너 한 곳 기준으로', '32억 달러를 빌려준다'], False)),
        ('조달 법인',
         ('AI XPV Platform', ['거래 하나만을 위해 세운 회사다', '랙을 사서 보유한다'], True),
         ('테라울프가 세운 프로젝트 회사', ['빌린 돈으로 짓고', '완공한 건물을 소유한다'], True)),
        ('대상 자산',
         ('구글 TPU 시스템', ['1GW 이상을 브로드컴과 함께', '개발해 배치한다'], False),
         ('데이터센터', ['크리티컬 IT 부하 378MW를', '플루이드스택에 빌려준다'], False)),
        ('임차인',
         ('앤트로픽', ['5년 리스를 확약했다', '리스료가 이자와 원금을 갚는다'], False),
         ('플루이드스택', ['초기 10년 리스를 맺었다', '임대료가 이자와 원금을 갚는다'], False)),
        ('공급자 지원',
         ('브로드컴', ['앤트로픽이 지급을 멈추면', '선순위 채무 300억 달러를 받친다',
                   '보도된 최대 노출은 290억 달러'], False),
         ('구글', ['플루이드스택이 멈추면 그 임대료를 받친다', '밀린 임대료를 대신 내거나',
                 '리스를 넘겨받는다'], False)),
    ]
    edge = [('cash', '부채 인출', '부채 인출'), ('svc', '사서 보유', '짓고 보유'),
            ('svc', '빌려준다', '빌려준다')]
    y = 76
    for i, (rl, left, right) in enumerate(rows):
        lh_, rh_ = None, None
        for x, (name, lines, key) in ((LX, left), (RX, right)):
            s, hh = box(x, y, BW, name, lines, key)
            o.append(s)
            if x == LX:
                lh_ = hh
            else:
                rh_ = hh
        h = max(lh_, rh_)
        o.append(role(320, y + 22, rl))
        if i < 3:
            kind, lname, rname = edge[i]
            for cx, nm in ((lcx, lname), (rcx, rname)):
                o.append(arrow(kind, [(cx, y + h), (cx, y + h + 26)]))
                o.append(lab(cx + 9, y + h + 18, nm, cash=(kind == 'cash'), fs=9.5))
        y += h + 26
    bottom = y - 26
    # 벤더 지원은 옆 레일로 돌린다 — 가운데를 가로지르면 아래 화살표와 엉킨다(규칙 7)
    o.append(arrow('cond', [(LX, bottom - 30), (6, bottom - 30), (6, 97), (LX, 97)]))
    # 브로드컴은 선순위 채무를, 구글은 임대료를 받친다 — 가리키는 자리가 다르다
    o.append(arrow('cond', [(RX + BW, bottom - 30), (634, bottom - 30), (634, 429), (RX + BW, 429)]))
    return svg(bottom + 12, ''.join(o))


# ── 한 줄 세로 스택 공용 — 빌려주는 곳 위, 갚는 곳 아래 ────────────────────
X, BW = 120, 300
CX = X + BW // 2
DOWN, UP, RAIL = X + 105, X + 195, 70     # 내려가는 선·올라가는 선·바깥 레일


def wrap(x, y, ww, h, title):
    """묶이는 회사를 감싸는 컨테이너 — 강조색보다 옅은 같은 색(규칙 4)."""
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" class="bx-wrap"/>'
            '<text x="%d" y="%d" class="t-role">%s</text>' % (x, y, ww, h, x + 12, y + 15, title))


def stack(rows, y=50, gap0=46, gap=30):
    """상자를 세로로 세운다. rows = [(역할, 이름, [설명], 강조)].

    칸 사이를 잇는 선은 부르는 쪽이 pair()로 건다 — 한 칸 사이에 오가는 것이
    둘(주는 것과 돌아오는 것)인 자리가 많아서, 내려가는 화살표 하나로는 못 그린다."""
    o, tops = [], []
    for i, (rl, name, lines, key) in enumerate(rows):
        s_, h = box(X, y, BW, name, lines, key)
        if rl:
            o.append('<text x="%d" y="%d" class="t-role">%s</text>' % (X + 2, y - 6, esc(rl)))
        o.append(s_)
        tops.append((y, h))
        y += h + (gap0 if i == 0 else gap)
    return o, tops, y - gap


def pair(tops, i, down, up, y2=None, dy=14):
    """i번 칸과 i+1번 칸 사이 — 내려가는 것과 올라가는 것을 나란히 세운다.

    down·up = (선 종류, 글자). 글자 색은 그 선의 색을 따른다(규칙 6).
    y2를 주면 거기서 선을 끊는다 — 컨테이너로 감싼 칸은 상자가 아니라 테두리에 닿아야 한다."""
    y1 = tops[i][0] + tops[i][1]
    y2 = tops[i + 1][0] if y2 is None else y2
    my = y1 + dy
    dk, dt = down
    uk, ut = up
    return [arrow(dk, [(DOWN, y1), (DOWN, y2)]),
            lab(DOWN - 8, my, dt, cash=(dk == 'cash'), anchor='end', fs=9.5),
            arrow(uk, [(UP, y2), (UP, y1)]),
            lab(UP + 8, my, ut, cash=(uk == 'cash'), fs=9.5)]


def down_only(tops, i, kind, text):
    y1, y2 = tops[i][0] + tops[i][1], tops[i + 1][0]
    return [arrow(kind, [(CX, y1), (CX, y2)]),
            lab(CX + 9, (y1 + y2) // 2 + 4, text, cash=(kind == 'cash'), fs=9.5)]


def left_rail(tops, src, dst, label):
    """멀리 떨어진 두 칸을 판 바깥 왼쪽으로 잇는다(규칙 7). 글자는 눕히지 않는다."""
    sy = tops[src][0] + tops[src][1] // 2
    dy = tops[dst][0] + tops[dst][1] // 2
    return [arrow('cash', [(X, sy), (RAIL, sy), (RAIL, dy), (X, dy)]),
            lab(X - 8, dy - 9, label, cash=True, anchor='end', fs=9.5)]


def side(y, role_, name, lines, ty, endx=X + BW):
    """오른쪽에 세우는 조건부 지원 상자. 선은 상자 밖에서 시작해 가로로만 간다."""
    s_, h = box(470, y, 164, name, lines)
    return ['<text x="472" y="%d" class="t-role">%s</text>' % (y - 6, esc(role_)),
            s_, arrow('cond', [(470, ty), (endx, ty)])], h


# ── ② 한 줄 세로 스택 — TPU 자금 한 바퀴 ────────────────────────────────
def fig_tpu_stack():
    o = [legend()]
    rows = [
        ('대출', '기관투자자', ['아폴로 운용 펀드가 주도하고', '블랙스톤·글로벌 은행이 참여한다',
                              '345억 달러를 확약했다'], False),
        ('조달 법인', 'AI XPV Platform', ['거래 하나만을 위해 세운 회사다', '랙을 사서 보유한다'], True),
        ('대상 자산', '구글 TPU 시스템', ['1GW 이상을 브로드컴과 함께 개발해', '배치하는 중이다'], False),
        ('임차인', '앤트로픽', ['이 리스가 사업의 고정 수요다'], False),
    ]
    body, tops, bottom = stack(rows)
    o += body
    o += pair(tops, 0, ('cash', '랙 배치에 맞춰 16회로 나눠 인출한다'), ('cash', '이자와 원금'))
    o += down_only(tops, 1, 'svc', '사서 보유한다')
    o += down_only(tops, 2, 'svc', '5년 리스로 빌려준다')
    o += left_rail(tops, 3, 1, '5년 확약 리스료')
    sb, sh = side(50, '공급자 지원', '브로드컴', ['앤트로픽이 지급을', '멈추면 300억 달러',
                                          '손실을 떠안는다', '최대 노출 290억 달러'],
                  tops[0][0] + 26)
    o += sb
    return svg(max(bottom, 50 + sh) + 12, ''.join(o))


# ── ④ 세 겹 — 레이크 매리너의 임대료가 건설 자금이 된다 ──────────────────
def fig_lake_mariner():
    o = [legend()]
    rows = [
        ('대주', '기관투자자', ['32억 달러를 빌려준다',
                                 '프로젝트 자산과 임대료에 청구권을 갖는다'], False),
        ('자금 조달', 'Wulf Compute', ['빌린 32억 달러를 공사비로 내보낸다'], True),
        ('건물 소유', 'Akela', ['건물을 소유하고 플루이드스택에 빌려준다',
                             '이 거래에서 빌려주는 것은 378MW'], True),
        ('임차·운영', '플루이드스택', ['초기 10년 리스에 5년 연장 두 번',
                                '앤트로픽에 용량과 운영 서비스를 판다'], False),
        ('고객', '앤트로픽', ['용량과 배치·운영 값을 낸다'], False),
    ]
    body, tops, bottom = stack(rows, gap0=70, gap=52)
    # 컨테이너는 상자보다 먼저 깔아야 상자가 그 위에 선다
    wy = tops[1][0] - 38
    wh = tops[2][0] + tops[2][1] + 14 - wy
    o.append(wrap(X - 14, wy, BW + 28, wh, '테라울프가 세운 프로젝트 회사'))
    o += body
    o += pair(tops, 0, ('cash', '32억 달러 프로젝트 부채'), ('cash', '임대료에서 나온 이자와 원금'),
              y2=wy)
    o += down_only(tops, 1, 'cash', '공사비로 나간다')
    o += pair(tops, 2, ('svc', '완공된 만큼 빌려준다'), ('cash', '넘어온 용량의 임대료'), dy=27)
    o += pair(tops, 3, ('svc', '용량과 배치·운영 서비스'), ('cash', '용량과 서비스 값'))
    ex = X + BW + 14
    sb1, h1 = side(wy, '준공 지원', '테라울프', ['부지·전력·인허가를 마련하고', '건물 준공을 책임진다'],
                   wy + 24, ex)
    o += sb1
    sb2, h2 = side(wy + 150, '신용 지원', '구글', ['플루이드스택이', '임대료를 멈추면',
                                              '밀린 임대료를 내거나', '리스를 넘겨받거나',
                                              '해지금을 채무에 충당한다'],
                   wy + 174, ex)
    o += sb2
    return svg(max(bottom, wy + 150 + h2) + 12, ''.join(o))


# ── ③ 막대 — 트랜치별 규모와 금리 ──────────────────────────────────────
def fig_tranches():
    """막대 길이는 원문에 있는 트랜치 금액이다. 없는 값은 그리지 않는다."""
    X0, XMAX, VMAX = 108, 496, 240.0          # 억 달러
    bars = [('A1 선순위', 60, '60억 달러 · 국채 수익률 +1.0%p', True),
            ('A2 선순위', 240, '240억 달러 · 5.75%', True),
            ('B 후순위', 45, '45억 달러 · 8.5%', False)]
    o = []
    # 범례 — 흐름도가 아니라 색 두 벌이다
    o.append('<rect x="16" y="14" width="14" height="11" rx="2" class="bx-key"/>')
    o.append(lab(36, 24, '브로드컴이 받쳐 준다', fs=9.5))
    o.append('<rect x="192" y="14" width="14" height="11" rx="2" '
             'fill="var(--fig-body,rgba(127,127,127,.16))" stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(212, 24, '받쳐 주지 않는다', fs=9.5))
    y = 56
    for name, val, note, key in bars:
        bw_ = int((XMAX - X0) * val / VMAX)
        fill = ('fill="var(--fig-good,#2f8f6b)"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
                     'stroke-width="1"')
        o.append('<rect x="%d" y="%d" width="%d" height="30" rx="3" %s/>' % (X0, y, bw_, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
                 'style="font-weight:850">%s</text>' % (X0 - 10, y + 20, name))
        o.append(lab(X0 + bw_ + 10, y + 20, note, fs=10))
        y += 46
    ay = y + 4
    # 세로 격자선은 두지 않는다 — 막대 옆 값 라벨을 가로질러 글자가 선에 깔린다
    # (check_fig가 잡는다). 눈금과 축 제목만으로 축은 읽힌다.
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, ay, XMAX + 14, ay))
    # 눈금값은 축의 눈금이지 원문에서 가져온 값이 아니다 — t-axis로 표시해 값 대조에서 뺀다
    for v in (0, 80, 160, 240):
        tx = X0 + int((XMAX - X0) * v / VMAX)
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
                 % (tx, ay, tx, ay + 5))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%d</text>'
                 % (tx, ay + 18, v))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
             'style="font-weight:800">트랜치 크기(억 달러)</text>' % ((X0 + XMAX) // 2, ay + 34))
    return svg(ay + 45, ''.join(o))


# ══ 「프런티어 랩은 세계 AI 컴퓨트의 절반도 안 쓴다」(2026-05-20) ══════════
def fig_world_share():
    """세계 AI 컴퓨트에서 각자가 쥔 몫. 값은 원문 도해의 H100 환산치를 그대로 쓴다."""
    o = [swatch(16, 24, '전업 프런티어 랩'), swatch(190, 24, '소유 전체(용도가 섞여 있다)', key=False)]
    rows = [('그 밖의 전부', 700, '약 700만 · 44%', False),
            ('구글', 400, '약 400만 · 25%', False),
            ('메타', 180, '약 180만 · 11%', False),
            ('오픈AI', 170, '약 170만 · 11%', True),
            ('앤트로픽', 100, '약 100만 · 6%', True),
            ('xAI', 70, '약 70만 · 4%', True)]
    body, bottom = barh(rows, 800, (0, 200, 400, 600, 800), 'H100 환산 보유량(만 장)')
    return svg(bottom, ''.join(o + body))


def fig_growth_2025():
    """2025년 한 해 증가율. 원문 도해는 로그 선그래프인데, 세계 총량의 연도별 값이
    원문에 없어 선을 그리면 없는 좌표를 지어내게 된다. 원문에 있는 증가율로만 그린다."""
    o = []
    rows = [('세계 전체', 3.3, '3.3배', False), ('오픈AI', 4.6, '4.6배', True)]
    body, bottom = barv(rows, 5, (0, 1, 2, 3, 4, 5), '2025년 배수', x0=150, bw_=90, step=170)
    return svg(bottom, ''.join(o + body))


def fig_openai_power():
    o = []
    rows = [('2023년 말', 0.2, '0.2GW', True), ('2024년 말', 0.6, '0.6GW', True),
            ('2025년 말', 1.9, '1.9GW', True)]
    body, bottom = barv(rows, 2, (0, 0.5, 1, 1.5, 2), '데이터센터 전력 용량(GW)')
    return svg(bottom, ''.join(o + body))


def fig_openai_chips():
    """원문 도해는 엔비디아 세대별 스택 막대인데 세대별 수치가 원문에 없다.
    그래서 스택을 쌓지 않고, 원문에 있는 연도별 H100 환산 총량만 그린다."""
    o = []
    rows = [('2023년 말', 10, '10만', True), ('2024년 말', 40, '40만', True),
            ('2025년 말', 170, '170만', True)]
    body, bottom = barv(rows, 200, (0, 50, 100, 150, 200), 'H100 환산 보유량(만 장)')
    return svg(bottom, ''.join(o + body))


def fig_deepmind_share():
    """구글 ML 컴퓨트를 100%로 놓은 띠. 확정된 경계는 절반 하나뿐이라
    딥마인드 구간의 양 끝은 점선으로 둔다 — 원문도 그 자리를 톱니로 흐려 놨다."""
    X0, X1, Y, H = 40, 600, 96, 62
    half = (X0 + X1) // 2
    o = [lab(16, 24, '구글 ML 컴퓨트를 100%로 놓았다. 딥마인드 몫의 양 끝은 원문도 확정하지 않는다',
             fs=9.5)]
    o.append('<text x="%d" y="72" class="t-role" text-anchor="middle">구글 클라우드 — 절반가량</text>'
             % ((X0 + half) // 2))
    o.append('<text x="%d" y="72" class="t-role" text-anchor="middle">나머지 구글 — 절반가량</text>'
             % ((half + X1) // 2))
    # 확정된 경계는 절반 하나뿐이다
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink)" stroke-width="1.6" fill="none"/>'
             % (half, Y - 8, half, Y + H + 8))
    o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">50%%</text>'
             % (half, Y - 14))
    segs = [(X0, 168, False), (X0 + 168, half - X0 - 168, True),
            (half, 150, True), (half + 150, X1 - half - 150, False)]
    for sx, sw_, key in segs:
        fill = ('fill="var(--fig-good,#2f8f6b)" opacity=".55"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.28))"')
        o.append('<rect x="%d" y="%d" width="%d" height="%d" %s/>' % (sx, Y, sw_, H, fill))
    for bx in (X0 + 168, half + 150):
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1.4" '
                 'stroke-dasharray="4 3" fill="none"/>' % (bx, Y, bx, Y + H))
    labs = [((X0 + X0 + 168) // 2, '외부 고객용', '클라우드 컴퓨트'),
            ((X0 + 168 + half) // 2, '제미나이', '기업용 추론'),
            ((half + half + 150) // 2, '연구개발과', '그 밖의 추론'),
            ((half + 150 + X1) // 2, '추천 시스템 등', '내부 용도')]
    for cx, l1, l2 in labs:
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle">%s</text>' % (cx, Y + H + 20, l1))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle">%s</text>' % (cx, Y + H + 34, l2))
    o.append(swatch(X0, Y + H + 62, '딥마인드 관련'))
    o.append(swatch(X0 + 150, Y + H + 62, '딥마인드와 무관', key=False))
    return svg(Y + H + 78, ''.join(o))


# ══ 「컴퓨트 크런치가 오고 있나」(2026-05-25) ═══════════════════════════════
def _panel(x0, y0, pw, ph, title, ymax, xmax, lines, ylab, xlab):
    """작은 선그래프 한 판. lines = [(이름, 기울기, 절편, 강조)] — 원문 식 그대로다."""
    o = ['<text x="%d" y="%d" class="t-lab" text-anchor="middle">%s</text>'
         % (x0 + pw // 2, y0 - 26, esc(title))]
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (x0, y0, x0, y0 + ph, x0 + pw, y0 + ph))
    for name, slope, base, key in lines:
        pts = []
        for i in range(2):
            bx = xmax * i
            v = slope * bx + base
            pts.append((x0 + int(pw * bx / float(xmax)),
                        y0 + ph - int(ph * min(v, ymax) / float(ymax))))
        cls = ('stroke="var(--fig-good,#2f8f6b)" stroke-width="2.2"' if key
               else 'stroke="var(--ink-3)" stroke-width="2.2" stroke-dasharray="6 4"')
        o.append('<path d="M%d %d L%d %d" %s fill="none"/>'
                 % (pts[0][0], pts[0][1], pts[1][0], pts[1][1], cls))
        # 선 끝이 판 위쪽이면 글자를 아래로 내린다 — 안 그러면 선 위에 얹힌다
        ly = pts[1][1] + 16 if pts[1][1] < y0 + ph / 2 else pts[1][1] - 10
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" style="font-weight:850;'
                 'fill:%s">%s</text>' % (x0 + pw - 4, ly,
                                         'var(--fig-good,#2f8f6b)' if key else 'var(--ink-3)',
                                         esc(name)))
    o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
             % (x0 + pw // 2, y0 + ph + 17, esc(xlab)))
    o.append('<text x="%d" y="%d" class="t-sm t-axis">%s</text>' % (x0 - 4, y0 - 10, esc(ylab)))
    return o


def fig_prefill_decode():
    """프리필은 연산이, 디코드는 대역폭이 발목을 잡는다. 두 판의 세로 눈금이 다르다."""
    o = [lab(16, 24, 'GB200 NVL72 한 대에 8,000:1,000 요청을 올렸을 때. 두 판의 세로 자가 다르다',
             fs=9.5)]
    o += _panel(60, 74, 240, 150, '프리필', 1000, 1000,
                [('연산', 1.0, 0, True), ('데이터 이동', 0.0005, 0.9, False)],
                '밀리초(최대 1000)', '배치 크기 B (0 → 1000)')
    o += _panel(370, 74, 240, 150, '디코드', 1400, 1000,
                [('연산', 0.3, 0, False), ('데이터 이동', 0.5, 868, True)],
                '밀리초(최대 1400)', '배치 크기 B (0 → 1000)')
    o.append(lab(60, 268, '프리필 — 연산 1B, 데이터 이동 0.9 + 0.0005B', fs=9.5))
    o.append(lab(60, 284, '디코드 — 연산 0.3B, 데이터 이동 868 + 0.5B', fs=9.5))
    o.append(lab(60, 300, '초록이 그 단계를 붙잡는 쪽이다', fs=9.5))
    return svg(312, ''.join(o))


def fig_chunked_prefill():
    """노는 자원을 다음 요청의 프리필이 채운다. 칸 길이는 시간 비율이 아니다."""
    X0, SLOT, N = 116, 96, 4
    o = [lab(16, 24, '칸은 순서를 보이는 자리이고 길이는 시간 비율이 아니다', fs=9.5)]
    o.append(swatch(300, 24, '프리필'))
    o.append('<rect x="400" y="14" width="14" height="11" rx="2" '
             'fill="var(--fig-cell,#8fb0d8)" stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(420, 24, '디코드', fs=9.5))
    o.append('<rect x="480" y="14" width="14" height="11" rx="2" fill="url(#fig-hatch-wide)" '
             'stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(500, 24, '노는 자리', fs=9.5))

    def blocks(y, title, lanes):
        out = ['<text x="16" y="%d" class="t-lab">%s</text>' % (y - 10, esc(title))]
        for li, (lane, cells) in enumerate(lanes):
            ly = y + li * 40
            out.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
                       'style="font-weight:850">%s</text>' % (X0 - 10, ly + 20, esc(lane)))
            for ci, kind in enumerate(cells):
                cx = X0 + ci * SLOT
                if kind == 'p':
                    f = 'fill="var(--fig-good,#2f8f6b)"'
                elif kind == 'd':
                    f = 'fill="var(--fig-cell,#8fb0d8)"'
                else:
                    f = 'fill="url(#fig-hatch-wide)" stroke="var(--ink-3)" stroke-width="1"'
                out.append('<rect x="%d" y="%d" width="%d" height="28" rx="3" %s/>'
                           % (cx + 3, ly, SLOT - 6, f))
        return out

    o += blocks(80, '그냥 돌릴 때', [('연산', ['p', '.', '.', '.']),
                                 ('대역폭', ['.', 'd', 'd', 'd'])])
    o += blocks(210, '청크 프리필을 쓸 때', [('연산', ['p', 'p', 'p', 'p']),
                                      ('대역폭', ['.', 'd', 'd', 'd'])])
    o.append(arrow('svc', [(X0 + SLOT * 2, 190), (X0 + SLOT * 2, 214)]))
    o.append(lab(X0 + SLOT * 2 + 9, 206, '노는 연산을 다음 요청의 프리필이 채운다', fs=9.5))
    return svg(300, ''.join(o))


def fig_calibration():
    """이론값은 낙관적이라 실측으로 깎는다. 깎는 계수 셋과 그 결과."""
    o = [lab(16, 24, 'SemiAnalysis InferenceX의 Kimi K2.5 실험 111건에 맞춰 깎은 값', fs=9.5)]
    rows = [('이론값', 64, '초당 64만 토큰', False), ('보정값', 40, '초당 40만 토큰', True)]
    body, bottom = barh(rows, 70, (), 'GB200 NVL72 한 대의 출력 처리량', x0=110, x1=420, y=56,
                        bh=30, step=46)
    o += body
    y = bottom + 6
    for t in ['연산 효율 65% — 큰 행렬 곱에서도 표기 성능을 다 못 쓴다',
              '대역폭 효율 30% — 칩 사이 통신 시간까지 여기에 들어간다',
              '토큰당 지연 5밀리초 — 통신·커널 스케줄링·라우팅 불균형']:
        o.append(lab(110, y, t, fs=9.5))
        y += 16
    return svg(y + 4, ''.join(o))


def fig_supply_growth():
    """문맥 길이별 토큰 공급이 해마다 3.4배로 는다. 시작값과 증가율은 원문에 있다."""
    import math
    X0, X1, Y0, Y1 = 92, 600, 60, 226
    LO, HI = 1e8, 1e14            # 세로 자의 아래위 (로그)

    def py(v):
        return Y1 - (Y1 - Y0) * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
    o = [lab(16, 24, '세계 블랙웰 전체가 Kimi K2.6을 돌린다고 놓았을 때', fs=9.5)]
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y0 - 8, X0, Y1, X1 + 10, Y1))
    for v, t in ((1e8, '1억'), (1e10, '100억'), (1e12, '1조'), (1e14, '100조')):
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="end">%s</text>'
                 % (X0 - 8, py(v) + 4, t))
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
                 % (X0 - 5, py(v), X0, py(v)))
    o.append('<text x="%d" y="%d" class="t-sm t-axis">%s</text>'
             % (X0 - 44, Y0 - 16, '초당 출력 토큰'))
    for i, yr in enumerate((2026, 2029, 2032)):
        tx = X0 + int((X1 - X0) * i / 2.0)
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%d</text>'
                 % (tx, Y1 + 17, yr))
    series = [('입력 8,000토큰', 20e9, '2026년 초당 200억 토큰에서 시작', 'key'),
              ('입력 25,000토큰', 6e9, '2026년 초당 60억 토큰에서 시작', 'solid'),
              ('입력 128,000토큰', 0.5e9, '2026년 초당 5억 토큰에서 시작', 'dash')]
    ly = Y1 + 40
    for name, start, note, style in series:
        end = start * (3.4 ** 6)
        if style == 'key':
            cls = 'stroke="var(--fig-good,#2f8f6b)" stroke-width="2.4"'
        elif style == 'solid':
            cls = 'stroke="var(--ink-3)" stroke-width="2.4"'
        else:
            cls = 'stroke="var(--ink-3)" stroke-width="2.4" stroke-dasharray="6 4"'
        o.append('<path d="M%d %d L%d %d" %s fill="none"/>'
                 % (X0, py(start), X1, py(end), cls))
        # 범례는 판 아래로 내린다 — 판 위에 글자를 얹지 않는다(규칙 3)
        o.append('<path d="M16 %d L44 %d" %s fill="none"/>' % (ly - 4, ly - 4, cls))
        o.append(lab(52, ly, '%s — %s' % (name, note), fs=9.5))
        ly += 17
    o.append(lab(52, ly + 4, '세로 자는 로그다 — 곧은 선이 해마다 같은 배수라는 뜻이고, '
                             '이 기울기가 3.4배다', fs=9.5))
    return svg(ly + 16, ''.join(o))


SRC = {
    'fin': '[260812] 파이낸싱이 프런티어 컴퓨트의 병목이 될까.md',
    'labs': '[260520] 프런티어 랩은 세계 AI 컴퓨트의 절반도 안 쓴다.md',
    'crunch': '[260525] 컴퓨트 크런치가 오고 있나.md',
}

# 그림 이름 -> (그리는 함수, 값을 대조할 원문)
FIGS = {
    'two_columns': fig_two_columns,
    'world_share': fig_world_share,
    'growth_2025': fig_growth_2025,
    'openai_power': fig_openai_power,
    'openai_chips': fig_openai_chips,
    'deepmind_share': fig_deepmind_share,
    'prefill_decode': fig_prefill_decode,
    'chunked_prefill': fig_chunked_prefill,
    'calibration': fig_calibration,
    'supply_growth': fig_supply_growth,
}

FIG_SRC = {
    'two_columns': 'fin', 'tpu_stack': 'fin', 'tranches': 'fin', 'lake_mariner': 'fin',
    'world_share': 'labs', 'growth_2025': 'labs', 'openai_power': 'labs',
    'openai_chips': 'labs', 'deepmind_share': 'labs',
    'prefill_decode': 'crunch', 'chunked_prefill': 'crunch', 'calibration': 'crunch',
    'supply_growth': 'crunch',
    'tpu_stack': fig_tpu_stack,
    'tranches': fig_tranches,
    'lake_mariner': fig_lake_mariner,
}

if __name__ == '__main__':
    import io
    import os
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), 'scripts'))
    import check_fig
    from card_lib import FIG_CSS, FIG_DEFS
    import re
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    srcs = {k: re.sub(r'[\s,]', '',
                      io.open(os.path.join(root, 'content', 'epoch', v), encoding='utf-8').read())
            for k, v in SRC.items()}

    def num_check(svg_, key):
        """그림 글자의 숫자가 원문에 있는지 전수 대조한다(insight-figure 규칙 1).

        축 눈금·항목 이름(t-axis)은 뺀다 — 0·80·160이나 「2024년 말」은 원문에서
        가져온 값이 아니라 자를 읽는 눈금이다. 막대 길이가 주장이고, 그 길이의 근거인
        값은 막대 옆 라벨에 따로 적혀 이 대조를 받는다."""
        srcn = srcs[FIG_SRC[key]]
        nums = {n for t in re.findall(r'<text[^>]*>([^<]*)<',
                                      re.sub(r'<text[^>]*t-axis[^>]*>[^<]*</text>', '', svg_))
                for n in re.findall(r'\d[\d,\.]*', t)}
        return [n for n in nums if len(n.replace(',', '')) >= 2 and n.replace(',', '') not in srcn]

    bad = 0
    parts = []
    for k, fn in FIGS.items():
        s = fn()
        miss = num_check(s, k)
        if miss:
            bad += len(miss)
            print('FAIL %s 원문에 없는 값: %s' % (k, ', '.join(miss)))
        hits = check_fig.hits(s)
        if hits:
            bad += len(hits)
            for h in hits:
                print('FAIL %s %s' % (k, h))
        parts.append('<figure class="uc-fig"><p class="fig-title">%s</p>%s</figure>' % (k, s))
    print('FAIL %d건 (배치 + 값 대조)' % bad)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_epochfig.html')
    io.open(out, 'w', encoding='utf-8').write(
        '<!doctype html><meta charset="utf-8"><style>body{background:#fff;color:#1a2233;'
        'font-family:"Pretendard","Apple SD Gothic Neo",system-ui,sans-serif;max-width:760px;'
        'margin:20px auto}:root{--ink:#1a2233;--ink-2:#3d4759;--ink-3:#8a8a8a;--line:#dde2ea}'
        + FIG_CSS + '</style>' + FIG_DEFS + ''.join(parts))
    print('->', out)
