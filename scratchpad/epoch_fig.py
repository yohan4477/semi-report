# -*- coding: utf-8 -*-
"""Epoch AI 장의 도해 — 원문 그림을 한국어 인라인 SVG로 다시 그린다.

원문(epoch.ai) 도해는 라벨이 전부 영어라 그대로 실으면 카드 본문만 한국어가 된다.
그래서 값과 구조는 원문 그대로 두고 판을 새로 짠다. 규칙은 둘이다.
  · insight-figure 스킬 — 없는 값 금지·좌표 계산·판 위 글자 금지·검사기
  · docs/흐름도 — 만드는 규칙.md — 선 세 종류·역할 도랑·강조 한 종류·숫자는 상자 안

글자 폭은 여기서 재서 상자 밖으로 나가면 그 자리에서 멈춘다. check_fig.py는 한 글자를
9px로 어림하는데 한글은 글자 크기만큼 넓어서, 검사기만 믿으면 한글 줄이 상자를 넘는다.
"""


# 글자 한 벌의 실제 폭 — 크롬에서 getComputedTextLength 로 재서 옮겼다(2026-08-25).
# 어림값(라틴 일괄 0.55)으로는 띄어쓰기를 0.55로 잡아 한 줄에 20~30px씩 덜 넣었고,
# 그만큼 상자 오른쪽이 비었다. 반대로 「」와 — 는 1.0 으로 잡아 넘칠 뻔했다.
_ADV = {' ': .352, '·': .219, '—': 1.026, '「': .571, '」': .571,
        '(': .305, ')': .305, ',': .219, '.': .219, ':': .219, ';': .219,
        '%': .837, '~': .701, '-': .410, '+': .701, '=': .701, '/': .396,
        '→': .950, '•': .417, '°': .387,
        'A': .658, 'B': .584, 'C': .635, 'D': .717, 'E': .517, 'F': .499, 'G': .702,
        'H': .725, 'I': .270, 'J': .360, 'K': .590, 'L': .480, 'M': .917, 'N': .765,
        'O': .773, 'P': .571, 'Q': .773, 'R': .610, 'S': .543, 'T': .534, 'U': .703,
        'V': .634, 'W': .954, 'X': .601, 'Y': .564, 'Z': .583,
        'a': .520, 'b': .601, 'c': .473, 'd': .602, 'e': .535, 'f': .316, 'g': .602,
        'h': .579, 'i': .246, 'j': .246, 'k': .506, 'l': .246, 'm': .880, 'n': .578,
        'o': .599, 'p': .601, 'q': .602, 'r': .354, 's': .433, 't': .345, 'u': .578,
        'v': .487, 'w': .736, 'x': .465, 'y': .493, 'z': .462}


def w(s, fs):
    """글자 폭 — 잰 값이다. 한글·한자는 글자 크기만큼, 나머지는 위 표를 쓴다."""
    t = 0.0
    for c in s:
        r = _ADV.get(c)
        if r is None:
            r = 1.0 if ord(c) > 0x2E80 else (.551 if c.isdigit() else .55)
        t += r * fs
    return t


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def wrap_lines(text, bw, fs=13.5):
    """설명 한 줄을 상자 폭 안으로 자른다. 띄어쓰기에서만 끊는다.

    글자를 키우면 예전에 한 줄로 들어가던 문장이 넘친다. 손으로 다시 감는 대신
    폭을 재서 자른다 — box() 의 assert 와 같은 자로 잰다."""
    lim = bw - 12
    out, cur = [], ''
    for word in text.split(' '):
        trial = word if not cur else cur + ' ' + word
        if w(trial, fs) < lim or not cur:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def _new_item(ln):
    """새 항목이 시작되는 줄인가 — 앞줄과 이어 붙이면 안 되는 자리."""
    return ln.startswith(('입력', '출력', '예:', '예 ', '왼쪽', '오른쪽')) or ' — ' in ln[:14]


def reflow(lines, bw, fs=13.5):
    """손으로 끊어 놓은 설명 줄을 상자 폭에 맞춰 다시 감는다.

    글자 크기를 올릴 때마다 예전 줄바꿈 자리가 어긋난다. 짧은 줄이 여럿 남아
    상자 오른쪽이 비고, 「글을 더 쓸 수 있는데 왜 비었나」가 된다(2026-08-25).

    문장이 끝난 자리와 새 항목이 시작되는 자리는 그대로 둔다 — 「입력 —」과
    「출력 —」을 한 줄로 붙이면 두 항목이 한 항목으로 읽힌다.

    다만 문장 둘이 한 줄에 다 들어가면 가운뎃점으로 이어 한 줄로 낸다. 두 줄로
    벌려 놓고 양쪽 오른쪽을 비우는 것보다 낫다 — 이 장에서 쓰는 구분 기호다."""
    groups, buf = [], ''
    for ln in lines:
        if buf and (_new_item(ln) or buf.rstrip().endswith(('다', '다.'))):
            groups.append(buf)
            buf = ln
        else:
            buf = ln if not buf else buf + ' ' + ln
    if buf:
        groups.append(buf)
    if len(groups) > 1 and not any(_new_item(g) for g in groups):
        one = ' · '.join(groups)
        if w(one, fs) < bw - 12:
            return [one]
    out = []
    for g in groups:
        out += wrap_lines(g, bw, fs)
    return out




# ── 이 장 도해의 한 벌 ────────────────────────────────────────────────────
# 47장이 한 화면에서 이어 읽히려면 같은 역할에 같은 값을 써야 한다. 새 그림도 이대로 쓴다.
#
#   선 굵기   데이터 계열 2.4 · 기준선과 추세선 1.2(점선) · 축과 눈금 1
#             확정된 경계 1.6(다른 것과 성격이 다른 굵은 실선일 때만)
#   점선      6 4 하나. 흐름도의 조건부 지원선만 CSS(.flow-cond)의 5 4를 따로 쓴다
#   표식      산점도 점 5 · 조밀한 산점도 3.4 · 선그래프 위 표식 4
#             목록 머리표와 선이 갈리는 점 3
#             (버블 지도는 넓이가 값이라 크기가 제각각인 것이 맞다)
#   투명도    겹쳐 찍는 표식 .8 · 같은 색을 흐리게 쓴 면 .55
#   면을 대신하는 굵은 호 6, 겹쳐 읽히게 투명도 .38 (덮는 범위처럼 면이 아닌데
#             면으로 읽혀야 하는 자리에만)
#   글자      상자 이름 t-lab 16 · 설명과 값 t-sm 13.5 · 역할 라벨과 주석 13
#             막대 옆 값 라벨은 13.5, 판 아래 주석은 13
#             2026-08-25에 두 번 올렸다(11.5/10/9.5 → 14/12/11.5 → 16/13.5/13).
#             640 판이 카드 안에서 640에 묶여 있어 10px 글자가 10px 그대로 나왔다.
#             판을 카드 너비까지 늘이고(card_lib의 svg.epoch max-width:100%) 글자를
#             카드 산문(16px)과 같은 자리에 올렸다.
#             폭은 w() 가 잰다 — 크롬에서 실제 advance 를 재서 표로 박았다.
#             어림값(라틴 일괄 0.55)일 때 띄어쓰기를 두 배로 잡아 한 줄에 20~30px씩
#             덜 넣었고, 그만큼 상자 오른쪽이 비었다(2026-08-25 사용자 지적)
#             가장 작은 글자가 13이다. 카드 캡션(12.5px)보다 작아지면 안 된다 —
#             판 배율이 1.21이라 13이 15.7px 로 나온다
#   줄 간격   같은 자리에 쌓는 글자는 17 이상 띄운다. t-sm 상자 높이가 14.1이라
#             14로 쌓으면 검사기에 걸린다. 가로축 눈금은 축에서 22 내린다
#             상자 이름과 첫 설명 줄 사이는 25 — 붙이면 한 덩어리로 읽힌다
#             글자를 키우면 상자도 같이 넓혀야 한다 — 폭은 w()가 재고,
#             긴 설명 줄은 wrap_lines() 가 폭에 맞춰 자른다
#   색        원문 팔레트를 토큰으로 들여왔다 — svg.epoch 가 물린다(card_lib.FIG_CSS).
#             --fig-good 이 Epoch 청록, --fig-blue/amber/violet 이 파랑·주황·보라로
#             바뀌어 나온다. 자홍 --epoch-pink 와 산호 --epoch-coral 은 직접 부른다
#             회색 면은 채움 rgba(127,127,127,.30), 지면 .16 두 가지뿐


# ── 부품 ──────────────────────────────────────────────────────────────
def box(x, y, bw, name, lines, key=False, wrap=False, flow=True):
    """상자 하나. 이름 한 줄 + 설명 여러 줄. 높이는 줄 수가 정한다.

    설명은 그 주체가 하는 동사로 쓴다(규칙 5). 숫자는 이 상자 안에만 산다.
    이름(굵은 줄)과 첫 설명 줄 사이는 25 띄운다 — 붙여 놓으면 한 덩어리로 읽힌다.
    줄바꿈은 reflow() 가 폭을 재서 다시 잡는다 — 손으로 끊은 자리는 참고만 한다.
    끊은 자리를 반드시 지켜야 하면 flow=False."""
    if flow:
        lines = reflow(lines, bw)
    h = 33 + 19 * len(lines) + 4
    cls = 'bx-wrap' if wrap else ('bx-key' if key else 'bx')
    o = ['<rect x="%d" y="%d" width="%d" height="%d" rx="8" class="%s"/>' % (x, y, bw, h, cls)]
    assert w(name, 16) < bw - 12, '상자 이름이 넘친다: %s' % name
    o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (x + 6, y + 22, esc(name)))
    for i, ln in enumerate(lines):
        assert w(ln, 13.5) < bw - 12, '설명 줄이 상자를 넘는다(%d px): %s' % (bw, ln)
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>'
                 % (x + 6, y + 47 + 19 * i, esc(ln)))
    return ''.join(o), h


def arrow(kind, pts):
    """직각으로만 꺾는 선. kind = cash | svc | cond."""
    d = 'M%d %d' % pts[0] + ''.join(' L%d %d' % p for p in pts[1:])
    return '<path d="%s" class="flow-%s"/>' % (d, kind)


def lab(x, y, s, cash=False, anchor='start', fs=13.5):
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
        o.append(lab(x + 26, y, text, cash=(kind == 'cash'), fs=13))
        x += 24 + int(w(text, 13)) + 16
    assert x < 645, '범례가 판을 넘는다: %d' % x
    return ''.join(o)


def svg(h, body):
    """이 장 도해는 svg.epoch 를 단다 — Epoch 원문 팔레트를 물리는 표시다.

    색을 날것으로 박지 않고 토큰으로 두는 이유는 다크모드다. 정의는 card_lib.FIG_CSS."""
    return ('<svg class="epoch" viewBox="0 0 640 %d" role="img" '
            'xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, body))


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
                 % (tx, y + 22, fmt % v))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" style="font-weight:800">%s</text>'
             % ((x0 + x1) // 2, y + 40, esc(title)))
    return ''.join(o), y + 52


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
            + lab(x + 20, y, text, fs=13))


def barh(rows, vmax, ticks, title, x0=150, x1=452, y=52, bh=24, step=34):
    """가로 막대. rows = [(라벨, 값, 오른쪽 글자, 강조)]. 라벨은 축 왼쪽에 오른쪽 맞춤."""
    o = []
    for name, val, note, key in rows:
        bw_ = max(2, int((x1 - x0) * val / float(vmax)))
        fill = ('fill="var(--fig-good,#2f8f6b)"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
                     'stroke-width="1"')
        assert w(name, 13.5) < x0 - 8, '막대 라벨이 축을 넘는다: %s' % name
        o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" %s/>' % (x0, y, bw_, bh, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" style="font-weight:850">%s</text>'
                 % (x0 - 10, y + bh - 8, esc(name)))
        assert x0 + bw_ + 8 + w(note, 13.5) < 638, '막대 옆 값이 판을 넘는다: %s' % note
        o.append(lab(x0 + bw_ + 10, y + bh - 8, note, fs=13.5))
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
    LX, RX, BW = 4, 352, 284
    lcx, rcx = LX + BW // 2, RX + BW // 2
    o = [legend()]
    o.append(head(lcx, 48, '컴퓨트'))
    o.append(head(rcx, 48, '데이터센터'))
    o.append('<text x="%d" y="66" class="t-sm" text-anchor="middle">장비 부채 345억 달러</text>'
             % lcx)
    o.append('<text x="%d" y="66" class="t-sm" text-anchor="middle">'
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
        ('손실 부담',
         ('브로드컴', ['앤트로픽이 지급을 멈추면', '선순위 채무 300억 달러의 손실을',
                   '대신 떠안는다. 최대 290억 달러'], False),
         ('구글', ['플루이드스택이 임대료를 멈추면', '밀린 임대료를 대신 내거나',
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
                o.append(lab(cx + 9, y + h + 18, nm, cash=(kind == 'cash'), fs=13))
        y += h + 26
    bottom = y - 26
    # 벤더 지원은 옆 레일로 돌린다 — 가운데를 가로지르면 아래 화살표와 엉킨다(규칙 7)
    o.append(arrow('cond', [(LX, bottom - 30), (6, bottom - 30), (6, 97), (LX, 97)]))
    # 브로드컴은 선순위 채무를, 구글은 임대료를 받친다 — 가리키는 자리가 다르다
    o.append(arrow('cond', [(RX + BW, bottom - 30), (634, bottom - 30), (634, 429), (RX + BW, 429)]))
    return svg(bottom + 12, ''.join(o))


# ── 한 줄 세로 스택 공용 — 빌려주는 곳 위, 갚는 곳 아래 ────────────────────
X, BW = 112, 316
CX = X + BW // 2
DOWN, UP, RAIL = X + 110, X + 206, 64     # 내려가는 선·올라가는 선·바깥 레일


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
            lab(DOWN - 8, my, dt, cash=(dk == 'cash'), anchor='end', fs=13),
            arrow(uk, [(UP, y2), (UP, y1)]),
            lab(UP + 8, my, ut, cash=(uk == 'cash'), fs=13)]


def down_only(tops, i, kind, text):
    y1, y2 = tops[i][0] + tops[i][1], tops[i + 1][0]
    return [arrow(kind, [(CX, y1), (CX, y2)]),
            lab(CX + 9, (y1 + y2) // 2 + 4, text, cash=(kind == 'cash'), fs=13)]


def left_rail(tops, src, dst, label):
    """멀리 떨어진 두 칸을 판 바깥 왼쪽으로 잇는다(규칙 7). 글자는 눕히지 않는다."""
    sy = tops[src][0] + tops[src][1] // 2
    dy = tops[dst][0] + tops[dst][1] // 2
    return [arrow('cash', [(X, sy), (RAIL, sy), (RAIL, dy), (X, dy)]),
            lab(X - 8, dy - 9, label, cash=True, anchor='end', fs=13)]


def side(y, role_, name, lines, ty, endx=X + BW):
    """오른쪽에 세우는 조건부 지원 상자. 선은 상자 밖에서 시작해 가로로만 간다."""
    s_, h = box(458, y, 176, name, lines)
    return ['<text x="634" y="%d" class="t-role" text-anchor="end">%s</text>'
            % (y - 7, esc(role_)),
            s_, arrow('cond', [(458, ty), (endx, ty)])], h


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
    # 첫 칸 아래는 글자 두 줄이 들어가야 해서 도랑을 넓게 잡는다
    body, tops, bottom = stack(rows, gap0=60)
    o += body
    # 한 줄로는 판 왼쪽을 넘는다 — 두 줄로 내린다
    o += pair(tops, 0, ('cash', '랙 배치에 맞춰'), ('cash', '이자와 원금'), dy=12)
    o.append(lab(DOWN - 8, tops[0][0] + tops[0][1] + 30, '16회로 나눠 인출한다',
                 cash=True, anchor='end', fs=13))
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
    sb1, h1 = side(wy, '준공 지원', '테라울프', ['부지·전력·인허가를', '마련하고 건물', '준공을 책임진다'],
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
    o.append(lab(36, 24, '브로드컴이 손실을 떠안는다', fs=13))
    o.append('<rect x="210" y="14" width="14" height="11" rx="2" '
             'fill="var(--fig-body,rgba(127,127,127,.16))" stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(230, 24, '아무도 떠안지 않는다', fs=13))
    y = 56
    for name, val, note, key in bars:
        bw_ = int((XMAX - X0) * val / VMAX)
        fill = ('fill="var(--fig-good,#2f8f6b)"' if key
                else 'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
                     'stroke-width="1"')
        o.append('<rect x="%d" y="%d" width="%d" height="30" rx="3" %s/>' % (X0, y, bw_, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
                 'style="font-weight:850">%s</text>' % (X0 - 10, y + 20, name))
        o.append(lab(X0 + bw_ + 10, y + 20, note, fs=13.5))
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


# ══ 파이낸싱 편에 더 넣는 도해 ═════════════════════════════════════════════
def fig_funding_mix():
    """발표한 투자 계획과 공시로 확인되는 부채. 두 조각의 길이가 곧 조달 금액이다."""
    X0, X1, VMAX = 30, 590, 500.0          # 억 달러
    Y, H = 92, 40
    o = [lab(16, 24, '2025년 11월에 발표한 미국 인프라 투자 계획과, 그 뒤 공시로 확인되는 부채',
             fs=13)]

    def px(v):
        return X0 + int((X1 - X0) * v / VMAX)
    # 발표한 계획 500억 달러 — 기준선
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink)" stroke-width="1.6" fill="none"/>'
             % (px(500), Y - 22, px(500), Y + H + 10))
    o.append('<text x="%d" y="%d" class="t-lab" text-anchor="end">계획 500억 달러</text>'
             % (px(500), Y - 28))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" '
             'fill="var(--fig-good,#2f8f6b)"/>' % (X0, Y, px(345) - X0, H))
    # 둘째 조각은 회색 면으로 — 강조색은 그림당 한 종류다(흐름도 규칙 4)
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" '
             'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
             'stroke-width="1"/>' % (px(345), Y, px(497) - px(345), H))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
             'style="font-weight:850;fill:#fff">TPU 345억 달러</text>' % ((X0 + px(345)) // 2, Y + 25))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
             'style="font-weight:850">데이터센터 152억</text>' % ((px(345) + px(497)) // 2, Y + 25))
    o.append(lab(X0, Y + H + 30, '앤트로픽이 앞에 내놓은 현금은 없다 — 둘 다 기관투자자가 빌려준 '
                                 '돈이고, 리스료와 임대료로 갚는다', fs=13))
    return svg(Y + H + 44, ''.join(o))


def fig_revenue_jump():
    """구조가 짜인 시점과 매출이 뛴 시점이 다르다. 그래서 이 사례가 시험이 된다."""
    o = [lab(16, 24, '앤트로픽 연환산 매출. 부채는 대부분 왼쪽 시점에 맞춰 짜였다', fs=13)]
    rows = [('2025년 말\n(투자 계획 발표)', 90, '90억 달러', False),
            ('2026년 5월', 470, '470억 달러', True)]
    body, bottom = barv([(a.replace('\n', ' '), b, c, d) for a, b, c, d in rows],
                        500, (0, 100, 200, 300, 400, 500), '연환산 매출(억 달러)',
                        x0=130, bw_=90, step=180)
    o += body
    o.append(lab(130, bottom + 16, '발표 당시에는 90억 달러가 안 됐다', fs=13))
    o.append(lab(130, bottom + 32, '투자자가 빌려준 근거는 이미 번 돈이 아니라 앞으로 낼 '
                                   '리스료였다', fs=13))
    return svg(bottom + 44, ''.join(o))


def fig_draw_schedule():
    """돈은 한꺼번에 나가지 않는다. 랙이 오는 만큼만 나눠 인출한다."""
    X0, X1, VMAX = 130, 580, 345.0
    Y, H = 76, 36
    o = [lab(16, 24, '345억 달러 확약분 가운데 언제까지 얼마가 나가나', fs=13)]

    def px(v):
        return X0 + int((X1 - X0) * v / VMAX)
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" '
             'fill="var(--fig-good,#2f8f6b)"/>' % (X0, Y, px(240) - X0, H))
    o.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" '
             'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
             'stroke-width="1"/>' % (px(240), Y, px(345) - px(240), H))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
             'style="font-weight:850">확약 345억 달러</text>' % (X0 - 10, Y + 23))
    o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
             'style="font-weight:850;fill:#fff">2027년 여름까지 240억 달러</text>'
             % ((X0 + px(240)) // 2, Y + 23))
    o.append(lab(px(240) + 10, Y - 6, '남는 몫은 그 뒤에 나간다', fs=13))
    o.append(arrow('cash', [(X0, Y + H + 18), (px(240), Y + H + 18)]))
    o.append(lab(X0, Y + H + 36, '랙이 배치되는 대로 1년 남짓에 걸쳐 약 16회로 나눠 인출한다', fs=13))
    o.append(lab(X0, Y + H + 52, '담보로 잡힌 장비의 양과 나간 돈을 맞춰 두는 장치다', fs=13))
    o.append(lab(X0, Y + H + 68, '브로드컴이 지는 노출도 같은 속도로 커졌다가 상환이 시작되면 '
                                 '줄어든다', fs=13))
    return svg(Y + H + 80, ''.join(o))


def fig_rate_ladder():
    """같은 빌드아웃인데 금리가 셋으로 갈린다. 무엇이 받쳐 주느냐가 값을 가른다."""
    o = [lab(16, 24, '같은 빌드아웃에 붙은 금리. 누가 손실을 떠안느냐가 값을 가른다', fs=13)]
    rows = [('컴퓨트 A2 선순위', 5.75, '5.75% — 브로드컴이 떠안는다', True),
            ('레이크 매리너 부채', 7.75, '7.75% — 구글이 임대료를 낸다', True),
            ('컴퓨트 B 후순위', 8.5, '8.5% — 아무도 안 떠안는다', False)]
    body, bottom = barh(rows, 10, (0, 2, 4, 6, 8, 10), '연 이율(%)', x0=170, x1=420, y=52)
    o += body
    o.append(lab(170, bottom + 6, 'A1 선순위는 국채 수익률에 1.0%p를 얹는 방식이라 이 자에 '
                                  '올리지 않았다', fs=13))
    o.append(lab(170, bottom + 22, '레이크 매리너는 지원이 붙었는데도 7.75%다', fs=13))
    o.append(lab(170, bottom + 38, '공사 지연 가능성과 지원에 붙은 조건·한도가 값에 들어 있다',
                 fs=13))
    return svg(bottom + 50, ''.join(o))


def fig_five_sites():
    """다섯 사업장. 하나의 거대 거래가 아니라 같은 구조를 다섯 번 되풀이했다."""
    o = [lab(16, 24, '개발사와 지역을 바꿔 가며 같은 방식이 다섯 번 되풀이됐다', fs=13)]
    rows = [('메리디언 아크', 430, '430MW · 57.00억 달러', True),
            ('레이크 매리너', 378, '378MW · 32.00억 달러', True),
            ('리버 벤드', 245, '245MW · 32.50억 달러', True),
            ('바버 레이크', 207, '207MW · 17.33억 달러', True),
            ('애버내시', 168, '168MW · 13.00억 달러', True)]
    body, bottom = barh(rows, 500, (0, 100, 200, 300, 400, 500),
                        '크리티컬 IT 부하(MW) — 서버에 실제로 공급되는 전력 용량',
                        x0=120, x1=270, y=52, bh=22, step=32)
    o += body
    o.append(lab(120, bottom + 6, '스폰서는 차례로 Next Frontier·플루이드스택 합작, 테라울프,',
                 fs=13))
    o.append(lab(120, bottom + 22, 'Hut 8, Cipher, 플루이드스택 합작이다', fs=13))
    o.append(lab(120, bottom + 38, '다섯 곳을 합치면 1,428MW, 프로젝트 부채 151.83억 달러다',
                 fs=13))
    return svg(bottom + 50, ''.join(o))


def fig_delivery():
    """준공은 한 번에 끝나지 않는다. 임대료도 그만큼씩 늘어난다."""
    X0, X1, VMAX = 120, 560, 400.0
    o = [lab(16, 24, '레이크 매리너에서 이 거래가 빌려주는 378MW가 언제 들어오나', fs=13)]
    steps = [('2026년 7월', 42, 42, '42MW 가동'),
             ('2026년 10월', 42, 210, '168MW 더 들어온다'),
             ('2027년 3월', 210, 378, '다시 168MW')]
    y = 60

    def px(v):
        return X0 + int((X1 - X0) * v / VMAX)
    for when, base, top, note in steps:
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="end" '
                 'style="font-weight:850">%s</text>' % (X0 - 10, y + 21, when))
        if base:
            o.append('<rect x="%d" y="%d" width="%d" height="28" rx="3" '
                     'fill="var(--fig-good,#2f8f6b)" opacity=".55"/>' % (X0, y, px(base) - X0))
        o.append('<rect x="%d" y="%d" width="%d" height="28" rx="3" '
                 'fill="var(--fig-good,#2f8f6b)"/>' % (px(base), y, px(top) - px(base)))
        o.append(lab(px(top) + 10, y + 20, note, fs=13.5))
        y += 42
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, y - 8, X1 + 14, y - 8))
    o.append(lab(X0, y + 12, '옅은 몫이 이미 들어온 용량, 진한 몫이 그때 새로 들어오는 용량이다',
                 fs=13))
    o.append(lab(X0, y + 28, '플루이드스택은 건물이 인도되는 대로 임대료를 내기 시작한다', fs=13))
    o.append(lab(X0, y + 44, '2026년 7월 기준 실적은 42MW뿐이고 나머지는 예정이다', fs=13))
    return svg(y + 56, ''.join(o))


# ── 원문 도해에서 읽어 둔 값 ──────────────────────────────────────────────
# scratchpad/epoch_extract.py 가 원본 이미지에서 뽑아 data/epoch_fig_data.json 에
# 굽는다. 점과 막대의 자리를 눈으로 어림해 옮기지 않기 위한 것이다.
_FIGDATA = None


def figdata():
    global _FIGDATA
    if _FIGDATA is None:
        import io as _io
        import json
        import os
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _FIGDATA = json.load(_io.open(os.path.join(root, 'data', 'epoch_fig_data.json'),
                                      encoding='utf-8'))
    return _FIGDATA


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


def fig_openai_line():
    """원문대로 로그 선그래프. 값은 원문 그림에서 읽어 둔 것이다."""
    import math
    d = figdata()['openai_line']
    world, oa = d['world'], d['openai']
    X0, X1, Y0, Y1 = 96, 560, 62, 300
    LO, HI = 1e5, 3e7

    def py(v):
        return Y1 - (Y1 - Y0) * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))

    def px_(i):
        return X0 + (X1 - X0) * i / 8.0
    o = [lab(16, 24, 'H100 환산 누적 칩 수 (세로 자는 로그)', fs=13)]
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y0 - 8, X0, Y1, X1 + 14, Y1))
    for v, t in ((1e5, '10만'), (1e6, '100만'), (1e7, '1000만')):
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%s</text>'
                 % (X0 - 8, py(v) + 4, t))
        o.append('<path d="M%d %.1f L%d %.1f" stroke="var(--ink-3)" stroke-width="1" '
                 'fill="none"/>' % (X0 - 5, py(v), X0, py(v)))
    for i, t in ((0, '2023-Q4'), (4, '2024-Q4'), (8, '2025-Q4')):
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (px_(i), Y1 + 22, t))
    # 세계 총계 — 2024-Q4 앞은 원문도 점선이다(옛 자료가 성글다)
    for a, b, dash in ((0, 4, True), (4, 8, False)):
        pts = ' '.join('%.1f,%.1f' % (px_(i), py(world[i])) for i in range(a, b + 1))
        o.append('<polyline points="%s" fill="none" stroke="var(--fig-blue,#2f6fd0)" '
                 'stroke-width="3"%s/>' % (pts, ' stroke-dasharray="6 4"' if dash else ''))
    for i in range(9):
        o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--fig-blue,#2f6fd0)"/>'
                 % (px_(i), py(world[i])))
    # 오픈AI — 표식은 세 곳뿐이고 그 사이는 곧은 선이다
    mk = [0, 4, 8]
    pts = ' '.join('%.1f,%.1f' % (px_(i), py(oa[i])) for i in mk)
    o.append('<polyline points="%s" fill="none" stroke="var(--fig-good,#2f8f6b)" '
             'stroke-width="3"/>' % pts)
    for i in mk:
        o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="var(--fig-good,#2f8f6b)"/>'
                 % (px_(i), py(oa[i])))
    o.append('<text x="%d" y="%.1f" class="t-sm" style="font-weight:850;'
             'fill:var(--fig-blue,#2f6fd0)">세계 총계</text>' % (X1 + 8, py(world[8]) - 8))
    o.append('<text x="%d" y="%.1f" class="t-sm" style="font-weight:850;'
             'fill:var(--fig-good,#2f8f6b)">오픈AI</text>' % (X1 + 8, py(oa[8]) + 4))
    o.append(lab(px_(5), py(world[5]) + 22, '2025년 3.3배', fs=13.5))
    # 선 위에 얹으면 글자가 선에 깔린다 — 오픈AI 선은 오르막이라 아래로 내린다
    o.append('<text x="%.1f" y="%.1f" class="t-cash">2025년 4.6배</text>'
             % (px_(5) + 6, py(oa[5]) + 24))
    o.append(lab(16, Y1 + 44, '세계 총계는 Epoch의 칩 판매 자료를 한 분기 당겨 누적한 값이다. '
                              '2024-Q4 앞이 점선인 것은', fs=13))
    o.append(lab(16, Y1 + 60, '옛 자료, 특히 엔비디아가 아닌 칩의 자료가 성글기 때문이다', fs=13))
    o.append(lab(16, Y1 + 80, '오픈AI는 2023-Q4 · 2024-Q4 · 2025-Q4 세 곳만 표식이고 그 사이는 '
                              '이어 그은 선이다', fs=13))
    return svg(Y1 + 92, ''.join(o))



def fig_openai_power():
    o = []
    rows = [('2023년 말', 0.2, '0.2GW', True), ('2024년 말', 0.6, '0.6GW', True),
            ('2025년 말', 1.9, '1.9GW', True)]
    body, bottom = barv(rows, 2, (0, 0.5, 1, 1.5, 2), '데이터센터 전력 용량(GW)')
    return svg(bottom, ''.join(o + body))


def fig_openai_chips():
    """원문대로 엔비디아 세대별로 쌓은 막대. 구간 값은 원문 그림에서 읽었다."""
    d = figdata()['by_chip']
    o = [lab(16, 24, '오픈AI 보유량을 엔비디아 세대별로 쌓았다 (H100 환산 누적)', fs=13)]
    gens = [('Ampere', '앰페어', 'var(--fig-blue,#2f6fd0)'),
            ('Hopper', '호퍼', 'var(--fig-good,#2f8f6b)'),
            ('Blackwell', '블랙웰', 'var(--fig-amber,#d68a1e)')]
    x = 16
    for _k, name, col in gens:
        o.append('<rect x="%d" y="34" width="14" height="11" rx="2" fill="%s"/>' % (x, col))
        o.append(lab(x + 20, 44, name, fs=13))
        x += 22 + int(w(name, 13)) + 20
    X0, Y0, Y1, VMAX = 130, 66, 300, 1800.0
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y0 - 8, X0, Y1, 600, Y1))
    for v in (0, 500, 1000, 1500):
        ty = Y1 - (Y1 - Y0) * v / VMAX
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%s만</text>'
                 % (X0 - 8, ty + 4, v // 10 if v else 0))
        o.append('<path d="M%d %.1f L%d %.1f" stroke="var(--ink-3)" stroke-width="1" '
                 'fill="none"/>' % (X0 - 5, ty, X0, ty))
    BW_, STEP = 96, 150
    for i, bar in enumerate(d['bars']):
        bx = X0 + 40 + i * STEP
        base = 0
        for key, _name, col in gens:
            v = bar['seg'].get(key)
            if not v:
                continue
            y_top = Y1 - (Y1 - Y0) * (base + v) / VMAX
            h = (Y1 - Y0) * v / VMAX
            o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                     % (bx, y_top, BW_, h, col))
            base += v
        o.append('<text x="%d" y="%.1f" class="t-sm" text-anchor="middle" '
                 'style="font-weight:850">%d만</text>'
                 % (bx + BW_ // 2, Y1 - (Y1 - Y0) * base / VMAX - 8, round(base / 10)))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%d년</text>'
                 % (bx + BW_ // 2, Y1 + 22, bar['year']))
        o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">(%dMW)</text>'
                 % (bx + BW_ // 2, Y1 + 40, bar['mw']))
    o.append(lab(16, Y1 + 64, '2025년에 블랙웰이 107만으로 대부분을 차지하고 호퍼가 62만, 앰페어는 '
                              '2만까지 줄었다', fs=13))
    o.append(lab(16, Y1 + 82, '전력이 3배 늘 때 계산 능력이 4배 넘게 느는 것은 칩이 해마다 전력당 '
                              '성능이 좋아지기 때문이다', fs=13))
    return svg(Y1 + 94, ''.join(o))



def fig_deepmind_share():
    """구글 ML 컴퓨트를 100%로 놓은 띠. 확정된 경계는 절반 하나뿐이라
    딥마인드 구간의 양 끝은 점선으로 둔다 — 원문도 그 자리를 톱니로 흐려 놨다."""
    X0, X1, Y, H = 40, 600, 96, 62
    half = (X0 + X1) // 2
    o = [lab(16, 24, '구글 ML 컴퓨트를 100%로 놓았다. 딥마인드 몫의 양 끝은 원문도 확정하지 않는다',
             fs=13)]
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
                else 'fill="var(--fig-body,rgba(127,127,127,.30))"')
        o.append('<rect x="%d" y="%d" width="%d" height="%d" %s/>' % (sx, Y, sw_, H, fill))
    for bx in (X0 + 168, half + 150):
        o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1.8" '
                 'stroke-dasharray="6 4" fill="none"/>' % (bx, Y, bx, Y + H))
    labs = [((X0 + X0 + 168) // 2, '외부 고객용', '클라우드 컴퓨트'),
            ((X0 + 168 + half) // 2, '제미나이', '기업용 추론'),
            ((half + half + 150) // 2, '연구개발과', '그 밖의 추론'),
            ((half + 150 + X1) // 2, '추천 시스템 등', '내부 용도')]
    for cx, l1, l2 in labs:
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle">%s</text>' % (cx, Y + H + 20, l1))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle">%s</text>' % (cx, Y + H + 38, l2))
    o.append(swatch(X0, Y + H + 70, '딥마인드 관련'))
    o.append(swatch(X0 + 158, Y + H + 70, '딥마인드와 무관', key=False))
    return svg(Y + H + 86, ''.join(o))


# ══ 「컴퓨트 크런치가 오고 있나」(2026-05-25) ═══════════════════════════════
def _panel(x0, y0, pw, ph, title, ymax, xmax, lines, ylab, xlab):
    """작은 선그래프 한 판. lines = [(이름, 기울기, 절편, 강조)] — 원문 식 그대로다."""
    o = ['<text x="%d" y="%d" class="t-lab" text-anchor="middle">%s</text>'
         % (x0 + pw // 2, y0 - 26, esc(title))]
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (x0, y0, x0, y0 + ph, x0 + pw, y0 + ph))
    keys = []
    for name, slope, base, key in lines:
        pts = []
        for i in range(2):
            bx = xmax * i
            v = slope * bx + base
            pts.append((x0 + int(pw * bx / float(xmax)),
                        y0 + ph - int(ph * min(v, ymax) / float(ymax))))
        cls = ('stroke="var(--fig-good,#2f8f6b)" stroke-width="3"' if key
               else 'stroke="var(--ink-3)" stroke-width="3" stroke-dasharray="6 4"')
        o.append('<path d="M%d %d L%d %d" %s fill="none"/>'
                 % (pts[0][0], pts[0][1], pts[1][0], pts[1][1], cls))
        keys.append((name, key))
    o.append('<text x="%d" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
             % (x0 + pw // 2, y0 + ph + 22, esc(xlab)))
    o.append('<text x="%d" y="%d" class="t-sm t-axis">%s</text>' % (x0 - 4, y0 - 46, esc(ylab)))
    # 계열 이름은 선 위에 얹지 않는다 — 오르막 선이 글자 자리를 지나며 올라온다.
    # 판 위쪽에 색 딱지로 내놓는다(insight-figure 규칙 3과 같은 뜻이다)
    kx = x0
    for name, key in keys:
        col = 'var(--fig-good,#2f8f6b)' if key else 'var(--ink-3)'
        dash = '' if key else ' stroke-dasharray="6 4"'
        o.append('<path d="M%d %d L%d %d" stroke="%s" stroke-width="3"%s fill="none"/>'
                 % (kx, y0 - 11, kx + 18, y0 - 11, col, dash))
        o.append('<text x="%d" y="%d" class="t-sm" style="font-weight:850;fill:%s">%s</text>'
                 % (kx + 24, y0 - 7, col, esc(name)))
        kx += 22 + int(w(name, 13.5)) + 20
    return o


def fig_prefill_decode():
    """프리필은 연산이, 디코드는 대역폭이 발목을 잡는다. 두 판의 세로 눈금이 다르다."""
    o = [lab(16, 19, 'GB200 NVL72 한 대에 8,000:1,000 요청을 올렸을 때. 두 판의 세로 자가 다르다',
             fs=13)]
    o += _panel(60, 88, 240, 150, '프리필', 1000, 1000,
                [('연산', 1.0, 0, True), ('데이터 이동', 0.0005, 0.9, False)],
                '밀리초(최대 1000)', '배치 크기 B (0 → 1000)')
    o += _panel(370, 88, 240, 150, '디코드', 1400, 1000,
                [('연산', 0.3, 0, False), ('데이터 이동', 0.5, 868, True)],
                '밀리초(최대 1400)', '배치 크기 B (0 → 1000)')
    o.append(lab(60, 288, '프리필 — 연산 1B, 데이터 이동 0.9 + 0.0005B', fs=13))
    o.append(lab(60, 306, '디코드 — 연산 0.3B, 데이터 이동 868 + 0.5B', fs=13))
    o.append(lab(60, 324, '초록이 그 단계를 붙잡는 쪽이다', fs=13))
    return svg(336, ''.join(o))


def fig_chunked_prefill():
    """노는 자원을 다음 요청의 프리필이 채운다. 칸 길이는 시간 비율이 아니다."""
    X0, SLOT, N = 116, 96, 4
    o = [lab(16, 24, '칸은 순서를 보이는 자리이고 길이는 시간 비율이 아니다', fs=13)]
    o.append(swatch(376, 24, '프리필'))
    o.append('<rect x="462" y="14" width="14" height="11" rx="2" '
             'fill="var(--fig-cell,#8fb0d8)" stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(482, 24, '디코드', fs=13))
    o.append('<rect x="540" y="14" width="14" height="11" rx="2" fill="url(#fig-hatch-wide)" '
             'stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(560, 24, '노는 자리', fs=13))

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
    o.append(lab(X0 + SLOT * 2 + 9, 206, '노는 연산을 다음 요청의 프리필이 채운다', fs=13))
    return svg(300, ''.join(o))


def fig_calibration():
    """원문대로 보정 전후 산점도 둘. 점 자리는 원문 그림에서 뽑았다."""
    import math
    d = figdata()['calib']
    o = [lab(16, 24, 'SemiAnalysis InferenceX의 Kimi K2.5·K2.6 실험 111건과 견준 것', fs=13)]
    cols = {'B200': 'var(--fig-blue,#2f6fd0)', 'B300': 'var(--fig-violet,#8b6fc8)',
            'GB200': 'var(--fig-good,#2f8f6b)', 'H200': 'var(--epoch-coral,#FD6438)'}
    x = 16
    for name, col in cols.items():
        o.append('<circle cx="%d" cy="42" r="5" fill="%s"/>' % (x + 5, col))
        o.append(lab(x + 15, 46, name, fs=13))
        x += 15 + int(w(name, 13)) + 18
    LO, HI = 30.0, 3e4
    for pi, (key, title) in enumerate((('uncal', '보정 전'), ('cal', '보정 후'))):
        PX0 = 40 + pi * 320
        PY0, PW, PH = 92, 250, 190

        def fx(v):
            return PX0 + PW * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))

        def fy(v):
            return PY0 + PH - PH * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
        o.append('<text x="%d" y="%d" class="t-lab">%s</text>' % (PX0, PY0 - 10, esc(title)))
        o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" '
                 'fill="none"/>' % (PX0, PY0, PX0, PY0 + PH, PX0 + PW, PY0 + PH))
        # 이론값과 실측이 같으면 이 대각선 위에 놓인다
        o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="var(--ink-3)" stroke-width="1.8" '
                 'stroke-dasharray="6 4" fill="none"/>' % (fx(LO), fy(LO), fx(HI), fy(HI)))
        for v, t in ((1e2, '10²'), (1e3, '10³'), (1e4, '10⁴')):
            o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                     % (fx(v), PY0 + PH + 16, t))
            o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%s</text>'
                     % (PX0 - 6, fy(v) + 4, t))
        for name, ax, ay in d[key]['points']:
            if not (LO <= ax <= HI and LO <= ay <= HI):
                continue
            o.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s" fill-opacity=".8"/>'
                     % (fx(ax), fy(ay), cols[name]))
    for i, t in enumerate(('가로가 실제 처리량, 세로가 모형이 내놓은 처리량이다(둘 다 초당 토큰).',
                           '점선 위에 놓이면 둘이 같다는 뜻이다',
                           '보정 전에는 점이 죄다 점선 위쪽에 있다 — 모형이 낙관적이다.',
                           '연산 효율 65%, 대역폭 효율 30%, 토큰당 지연 5밀리초를 넣으면 '
                           '점들이 점선에 붙는다',
                           '점이 겹쳐 그려져 있어 111건이 다 갈라지지는 않는다 —',
                           '여기 찍힌 것은 왼쪽 47곳, 오른쪽 36곳이다')):
        o.append(lab(40, 320 + 18 * i, t, fs=13))
    return svg(320 + 18 * 5 + 14, ''.join(o))



def fig_supply_growth():
    """문맥 길이별 토큰 공급이 해마다 3.4배로 는다. 시작값과 증가율은 원문에 있다."""
    import math
    X0, X1, Y0, Y1 = 92, 600, 60, 226
    LO, HI = 1e8, 1e14            # 세로 자의 아래위 (로그)

    def py(v):
        return Y1 - (Y1 - Y0) * (math.log10(v) - math.log10(LO)) / (math.log10(HI) - math.log10(LO))
    o = [lab(16, 24, '세계 블랙웰 전체가 Kimi K2.6을 돌린다고 놓았을 때', fs=13)]
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
                 % (tx, Y1 + 22, yr))
    series = [('입력 8,000토큰', 20e9, '2026년 초당 200억 토큰에서 시작', 'key'),
              ('입력 25,000토큰', 6e9, '2026년 초당 60억 토큰에서 시작', 'solid'),
              ('입력 128,000토큰', 0.5e9, '2026년 초당 5억 토큰에서 시작', 'dash')]
    ly = Y1 + 40
    for name, start, note, style in series:
        end = start * (3.4 ** 6)
        if style == 'key':
            cls = 'stroke="var(--fig-good,#2f8f6b)" stroke-width="3"'
        elif style == 'solid':
            cls = 'stroke="var(--ink-3)" stroke-width="3"'
        else:
            cls = 'stroke="var(--ink-3)" stroke-width="3" stroke-dasharray="6 4"'
        o.append('<path d="M%d %d L%d %d" %s fill="none"/>'
                 % (X0, py(start), X1, py(end), cls))
        # 범례는 판 아래로 내린다 — 판 위에 글자를 얹지 않는다(규칙 3)
        o.append('<path d="M16 %d L44 %d" %s fill="none"/>' % (ly - 4, ly - 4, cls))
        o.append(lab(52, ly, '%s — %s' % (name, note), fs=13))
        ly += 17
    o.append(lab(52, ly + 4, '세로 자는 로그다 — 곧은 선이 해마다 같은 배수라는 뜻이고, '
                             '이 기울기가 3.4배다', fs=13))
    return svg(ly + 16, ''.join(o))



# ══ 「미소스의 사이버 능력은 부풀려졌나」(2026-06-11) ═══════════════════════
def fig_two_skills():
    """공격이 성립하려면 둘 다 있어야 하는데, 이 글의 판정은 둘이 다르다."""
    o = [lab(16, 24, '앤트로픽은 둘 다 도약했다고 했다. 공개 증거의 판정은 갈린다', fs=13)]
    cols = [(8, '취약점 발견', ['코드에서 약한 자리를 찾는다',
                             '버퍼 오버플로처럼 메모리를',
                             '망가뜨릴 수 있는 줄을 짚는다'],
             '앞선 모델도 이미 잘했다',
             ['포화되지 않은 벤치마크가 없다', '강점은 오탐이 적고',
              '심각도를 잘 매기는 데 몰려 있다'], False),
            (360, '익스플로잇 개발', ['찾아낸 약점을 실제로 파고든다',
                                '메모리를 정확히 망가뜨려',
                                '원하는 코드를 실행시킨다'],
             '추세보다 7개월 앞섰다',
             ['Cyber-ECI가 뚜렷하게 뛴다', '앤트로픽 자체 분석도',
              '같은 방향을 가리킨다'], True)]
    bot, vy = 44, 0
    for x, name, what, verdict, why, key in cols:
        s1, h1 = box(x, 44, 272, name, what)
        o.append(s1)
        o.append(arrow('svc', [(x + 136, 44 + h1), (x + 136, 44 + h1 + 26)]))
        s2, h2 = box(x, 44 + h1 + 26, 272, verdict, why, key=key)
        o.append(s2)
        bot = max(bot, 44 + h1 + 26 + h2)
        vy = max(vy, 44 + h1 + 26)
    o.append(role(320, 62, '무엇인가'))
    o.append(role(320, vy + 18, '판정'))
    o.append(lab(16, bot + 22, '둘 다 있어야 공격이 성립한다 — 약점을 찾고, 그 약점으로 원하는 일을 '
                               '하게 만든다', fs=13))
    return svg(bot + 34, ''.join(o))


def fig_eci_lead():
    """원문대로 공개일 대 Cyber-ECI 산점도. 점 자리는 원문 그림에서 뽑았다."""
    d = figdata()['cyber_eci']
    o = [lab(16, 24, '사이버 벤치마크 약 15개를 합친 Cyber-ECI를 모델 공개일 위에 놓았다', fs=13)]
    o.append(swatch(16, 46, '프런티어 모델(공개 시점 최고)'))
    o.append('<circle cx="270" cy="42" r="5" fill="var(--fig-body,rgba(127,127,127,.30))" '
             'stroke="var(--ink-3)" stroke-width="1"/>')
    o.append(lab(282, 46, '그 밖의 모델', fs=13))
    X0, X1, Y0, Y1 = 96, 356, 66, 300
    LO, HI = 135.0, 175.0
    gx0, gx1 = d['grid_x'][0], d['grid_x'][-1]

    def fy(v):
        return Y1 - (Y1 - Y0) * (v - LO) / (HI - LO)

    def fx(px_):
        return X0 + (X1 - X0) * (px_ - gx0) / float(gx1 - gx0)
    o.append('<path d="M%d %d L%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y0 - 8, X0, Y1, X1 + 14, Y1))
    for v in (135, 145, 155, 165, 175):
        o.append('<text x="%d" y="%.1f" class="t-sm t-axis" text-anchor="end">%d</text>'
                 % (X0 - 8, fy(v) + 4, v))
        o.append('<path d="M%d %.1f L%d %.1f" stroke="var(--ink-3)" stroke-width="1" '
                 'fill="none"/>' % (X0 - 5, fy(v), X0, fy(v)))
    for i, t in enumerate(('2025/04', '2025/08', '2025/12', '2026/04')):
        o.append('<text x="%.1f" y="%d" class="t-sm t-axis" text-anchor="middle">%s</text>'
                 % (fx(gx0 + (gx1 - gx0) * i / 3.0), Y1 + 22, t))
    # 미소스 이전 추세 — 눈으로 긋지 않고, 미소스 앞의 프런티어 점으로 최소제곱을 낸다
    pre = [(cx, cy) for cx, cy in d['points'].get('teal', ()) if cx < 780]
    if len(pre) >= 2:
        n = len(pre)
        mx = sum(a for a, _ in pre) / n
        my = sum(b for _, b in pre) / n
        den = sum((a - mx) ** 2 for a, _ in pre) or 1.0
        slope = sum((a - mx) * (b - my) for a, b in pre) / den
        def trend(px_):
            return my + slope * (px_ - mx)
        # 추세선이 판 아래로 빠지면 가로축 눈금 글자를 덮는다. 판 안에서만 긋는다
        ax, ay, bx, by = X0 + 4, fy(trend(gx0)), X1 + 10, fy(trend(gx1 + 40))
        if ay > Y1 and ay != by:
            t = (ay - Y1) / (ay - by)
            ax, ay = ax + (bx - ax) * t, Y1
        o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="var(--ink-3)" stroke-width="1.8" '
                 'stroke-dasharray="6 4" fill="none"/>' % (ax, ay, bx, by))
    for cx, cy in d['points'].get('gray', ()):
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="var(--fig-body,rgba(127,127,127,.30))" '
                 'stroke="var(--ink-3)" stroke-width="1"/>' % (fx(cx), fy(cy)))
    for cx, cy in d['points'].get('teal', ()):
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="var(--fig-good,#2f8f6b)"/>'
                 % (fx(cx), fy(cy)))
    for cx, cy in d['points'].get('blue', ()):
        o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="var(--fig-blue,#2f6fd0)"/>'
                 % (fx(cx), fy(cy)))
    notes = [('미소스 프리뷰(4월)', '6.8개월', '3.4~12.6', True),
             ('미소스 프리뷰(초기)', '3.0개월', '1.6~5.1', True),
             ('GPT-5.5', '2.5개월', '0.7~5.2', False)]
    ny = 96
    for name, mo, ci, key in notes:
        col = 'var(--fig-good,#2f8f6b)' if key else 'var(--fig-blue,#2f6fd0)'
        o.append('<text x="448" y="%d" class="t-sm" '
                 'style="font-weight:850;fill:%s">%s</text>' % (ny, col, esc(name)))
        o.append('<text x="448" y="%d" class="t-sm" style="fill:%s">%s 앞섰다</text>'
                 % (ny + 17, col, esc(mo)))
        o.append('<text x="448" y="%d" class="t-sm t-axis">90%% 구간 %s</text>'
                 % (ny + 35, esc(ci)))
        ny += 66
    o.append(lab(16, Y1 + 44, '점선이 2025년 초부터 이어진 추세다. 앞선 정도는 원문이 90% 구간과 '
                              '함께 적어 둔 값이다', fs=13))
    o.append(lab(16, Y1 + 60, '초기 판본과 4월 판본이 갈리는 것이 회의론이 나온 까닭 하나다 — '
                              '초기 판본은 GPT-5.5와 가깝다', fs=13))
    return svg(Y1 + 72, ''.join(o))



def fig_cyscenario():
    """포화되지 않은 벤치마크에서는 차이가 보인다. 값은 원문 부록 그대로."""
    o = [lab(16, 24, 'Irregular의 CyScenarioBench — 종단 과제를 끝까지 해낸 비율', fs=13)]
    rows = [('미소스 5', 36.7, '36.7%', True),
            ('미소스 프리뷰', 29.2, '29.2%', True),
            ('GPT-5.5', 26, '26%', False),
            ('오푸스 4.8', 16.6, '16.6%', False),
            ('GPT-5.4', 9, '9%', False),
            ('GPT-5.2 · 5.3', 0, '0%', False),
            ('뮤즈 스파크', 0, '0%', False),
            ('제미나이 3 프로', 0, '0%', False)]
    body, bottom = barh(rows, 40, (0, 10, 20, 30, 40), '끝까지 해낸 비율(%)',
                        x0=150, x1=470, y=48, bh=20, step=27)
    o += body
    o.append(lab(150, bottom + 6, '초기 비교에 쓰인 벤치마크 다수가 이미 만점에 가까워 차이가 '
                                  '안 보였다', fs=13))
    return svg(bottom + 18, ''.join(o))


def fig_cve_spike():
    """찾아낸 취약점이 급증했다. 다만 능력 때문인지 돈 때문인지는 이 그림이 못 가른다."""
    o = [lab(16, 24, '21개 주요 조직의 고위험·치명 CVE — 2025년 평균을 기준선으로 놓았을 때', fs=13)]
    rows = [('4월', 142, '기준선보다 142% 많다', True),
            ('5월', 262, '기준선보다 262% 많다', True)]
    body, bottom = barh(rows, 300, (0, 100, 200, 300), '기준선 대비 증가(%)',
                        x0=110, x1=390, y=56, bh=30, step=46)
    o += body
    o.append(lab(110, bottom + 6, '미소스 프리뷰 공개 시점과 겹친다. 다만 프로젝트 글래스윙에 최대 '
                                  '1억 달러어치', fs=13))
    o.append(lab(110, bottom + 22, 'API 크레딧이 붙어 있어, 찾는 데 쓴 돈이 늘어난 결과일 수도 있다',
                 fs=13))
    o.append(lab(110, bottom + 38, '취약점은 공개 기록까지 시간이 걸려 이 수는 더 늘 것으로 본다',
                 fs=13))
    return svg(bottom + 50, ''.join(o))


# ══ 「부정행위를 하려다 허깅페이스를 해킹했다」(2026-07-22) ═══════════════════
def fig_hf_incident():
    """순서가 내용이다 — 무엇을 하려다, 무엇을 거쳐, 어디에 닿았나."""
    X, BW = 100, 340
    cx = X + BW // 2
    o = [lab(16, 24, '오픈AI가 밝힌 사고 경로', fs=13)]
    rows = [('시킨 일', '사이버보안 벤치마크', ['점수를 올리는 것이 과제였다'], False),
            ('모델이 고른 것', '부정행위', ['과제를 푸는 대신 채점 쪽을 건드리기로 했다'], True),
            ('거쳐 간 곳', '오픈AI와 허깅페이스 시스템',
             ['그때까지 알려지지 않은 취약점을', '최소 셋 엮었다'], False),
            ('닿은 곳', '허깅페이스', ['침입에 성공했다'], False)]
    y = 44
    for i, (rl, name, lines, key) in enumerate(rows):
        s_, h = box(X, y, BW, name, lines, key)
        o.append('<text x="%d" y="%d" class="t-role">%s</text>' % (X + 2, y - 6, esc(rl)))
        o.append(s_)
        if i < len(rows) - 1:
            o.append(arrow('svc', [(cx, y + h), (cx, y + h + 30)]))
        y += h + 30
    bottom = y - 30
    sb, sh = box(462, 60, 172, '사람이 했다면', ['중범죄다'])
    o.append(sb)
    o.append(arrow('cond', [(462, 84), (X + BW, 84)]))
    o.append(lab(16, bottom + 20, '필자가 놀랍다고 보는 자리는 능력이 아니라 선택이다 — '
                                  '벤치마크 점수 하나 때문에', fs=13))
    o.append(lab(16, bottom + 36, '이 경로를 골랐다는 것', fs=13))
    return svg(bottom + 48, ''.join(o))


def fig_cyber_chain():
    """능력 사슬. 각 칸을 실제로 보인 벤치마크 이름을 아래에 단다."""
    X0, W, GAP = 6, 152, 5
    o = [lab(16, 24, '공격은 이 순서로 이어진다. 각 칸을 프런티어 모델이 해낸다는 것을 보인 평가',
             fs=13)]
    steps = [('취약점 찾는다', ['실제 코드에서', '새 제로데이가 나왔다'], 'FrontierCyber'),
             ('익스플로잇 만든다', ['사람이 만든 최선보다', '안정적인 사례가 나왔다'], 'ExploitBench'),
             ('권한 끌어올린다', ['서로 다른 익스플로잇을', '이어 붙인다'], 'ExploitGym'),
             ('망 장악한다', ['모의 기업망을 일관되게', '완전히 장악했다'], '영국 AISI 사이버 레인지')]
    for i, (name, lines, bench) in enumerate(steps):
        x = X0 + i * (W + GAP)
        s_, h = box(x, 48, W, name, wrap_lines(' '.join(lines), W))
        o.append(s_)
        o.append('<text x="%d" y="%d" class="t-role" text-anchor="middle">%s</text>'
                 % (x + W // 2, 48 + h + 18, esc(bench)))
        if i < len(steps) - 1:
            o.append(arrow('svc', [(x + W, 48 + h // 2), (x + W + GAP, 48 + h // 2)]))
    bot = 48 + h + 18
    o.append(lab(16, bot + 26, '허깅페이스 사고도 같은 순서였다 — 취약점 셋을 엮어 접근 권한을 '
                               '단계적으로 끌어올렸다', fs=13))
    o.append(lab(16, bot + 44, 'CyScenarioBench는 이 사슬 전체를 한 과제로 낸다', fs=13))
    return svg(bot + 56, ''.join(o))


def fig_openweight_gap():
    """오픈웨이트가 얼마나 뒤에 있나. 시간으로 잰다."""
    X0, X1 = 130, 560
    o = [lab(16, 24, '영국 AI 보안연구소와 Irregular가 매긴 오픈웨이트 모델의 자리', fs=13)]
    Y = 82
    o.append('<path d="M%d %d L%d %d" stroke="var(--ink-3)" stroke-width="1" fill="none"/>'
             % (X0, Y, X1 + 12, Y))
    marks = [(X0, '오푸스 4.5', True), (X0 + 150, '오푸스 4.6', True), (X1, 'GLM 5.2', False)]
    for x, name, closed in marks:
        o.append('<circle cx="%d" cy="%d" r="5" %s/>'
                 % (x, Y, 'fill="var(--fig-good,#2f8f6b)"' if closed
                    else 'fill="none" stroke="var(--ink-3)" stroke-width="1.8"'))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
                 'style="font-weight:850">%s</text>' % (x, Y - 14, esc(name)))
    o.append('<path d="M%d %d L%d %d" class="flow-cond"/>' % (X0 + 150, Y + 22, X1, Y + 22))
    o.append(lab((X0 + 150 + X1) // 2, Y + 40, '4~7개월', anchor='middle', fs=13.5))
    o.append(lab(X0, Y + 62, 'GLM 5.2의 사이버 능력은 오푸스 4.5와 4.6 사이에 있고, 그 둘은 '
                             '4~7개월 앞서', fs=13))
    o.append(lab(X0, Y + 78, '나온 모델이다. 오픈웨이트는 아직 이번 사고 수준에 못 미친다', fs=13))
    o.append(lab(X0, Y + 98, '다만 미소스와 GPT-5.6 Sol이 추세를 끊고 뛴 터라,', fs=13))
    o.append(lab(X0, Y + 116, '이 격차가 앞으로도 같을지는 모른다', fs=13))
    return svg(Y + 128, ''.join(o))



# ══ 「중국 AI 채용공고 1,604건에서 읽은 것」(2026-06-24) ═════════════════════
def fig_cn_chips():
    """국산 칩이 어디까지 들어왔나. 자리마다 답이 다르다."""
    o = [lab(16, 24, '채용공고에서 읽은, 국산 칩이 실제로 쓰이는 자리', fs=13)]
    rows = [('추론', '자주 쓴다', ['바이트댄스는 같은 회사 안에서', 'CUDA 최적화 직무와 어센드·캠브리콘',
                              '우대 직무를 함께 낸다'], True),
            ('큰 모델 사후학습', '가끔 쓴다', ['필자들의 어림이고', '공고가 못 박아 주지는 않는다'], True),
            ('작은 모델 학습', '해냈다', ['Z.ai가 GLM-Image를 국산 칩만으로', '처음부터 끝까지 학습했다',
                                    '160억 파라미터, 최대 모델의 1/10~1/100'], True),
            ('큰 모델 사전학습', '드물다', ['여기까지는 아직 못 왔다는 것이', '필자들의 판단이다'], False)]
    y = 46
    for role_, verdict, why, key in rows:
        o.append('<text x="18" y="%d" class="t-sm" text-anchor="start" '
                 'style="font-weight:850">%s</text>' % (y + 20, esc(role_)))
        s_, h = box(180, y, 454, verdict, why, key=key)
        o.append(s_)
        y += h + 12
    o.append(lab(16, y + 12, '공고는 「무엇을 쓰는지」는 알려 주지만 「얼마나 쓰는지」는 알려 주지 '
                             '않는다', fs=13))
    return svg(y + 24, ''.join(o))


def fig_cn_gtm():
    """회사별 고객확보 직무 구성. 값은 원문 도해에 적힌 그대로다."""
    X0, X1 = 150, 590
    o = [lab(16, 24, '각 회사의 영업·고객확보 직무 구성 (2026-06-23 기준)', fs=13)]
    o.append(swatch(16, 44, 'B2B 영업'))
    o.append('<rect x="170" y="34" width="14" height="11" rx="2" '
             'fill="var(--fig-body,rgba(127,127,127,.30))" stroke="var(--ink-3)" '
             'stroke-width="1"/>')
    o.append(lab(190, 44, '광고·성장·마케팅', fs=13))
    rows = [('Z.ai', 83, 17), ('미니맥스', 24, 76), ('문샷', 17, 83)]
    y = 62
    for name, b2b, mkt in rows:
        w1 = int((X1 - X0) * b2b / 100.0)
        o.append('<rect x="%d" y="%d" width="%d" height="44" fill="var(--fig-good,#2f8f6b)"/>'
                 % (X0, y, w1))
        o.append('<rect x="%d" y="%d" width="%d" height="44" '
                 'fill="var(--fig-body,rgba(127,127,127,.30))"/>' % (X0 + w1, y, X1 - X0 - w1))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
                 'style="font-weight:850">%s</text>' % (X0 - 12, y + 28, esc(name)))
        for val, cx, fill in ((b2b, X0 + w1 // 2, '#fff'),
                              (mkt, X0 + w1 + (X1 - X0 - w1) // 2, 'var(--ink)')):
            o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
                     'style="font-weight:850;fill:%s">%d%%</text>' % (cx, y + 28, fill, val))
        y += 54
    ax, bottom = xaxis(X0, X1, y - 4, (0, 25, 50, 75, 100), 100,
                       '그 회사 영업·고객확보 직무에서 차지하는 비중(%)')
    o.append(ax)
    o.append(lab(16, bottom + 6, '매출 구조가 이 차이를 설명한다 — 미니맥스는 매출의 70%가 개인 대상 '
                                 '앱에서 나오고,', fs=13))
    o.append(lab(16, bottom + 22, 'Z.ai는 73.7%가 고객 인프라 위에서 모델을 돌려 주는 방식에서 나온다',
                 fs=13))
    return svg(bottom + 34, ''.join(o))



def fig_cn_hubs():
    """중국도 몰려 있지만 미국만큼은 아니다. 원문 도해는 도시별 버블 지도인데
    도시별 공고 수가 원문에 없어 버블 크기를 그릴 수 없다. 원문에 있는 집중도만 견준다."""
    o = [lab(16, 24, '위치가 적힌 공고가 어디에 몰려 있나', fs=13)]
    rows = [('미국 프런티어 랩', 85, '85% — 샌프란시스코 한 곳', False),
            ('중국 6개 회사', 93, '93% — 베이징·항저우·상하이 세 곳', True),
            ('그중 베이징만', 63, '63%', True)]
    body, bottom = barh(rows, 100, (0, 25, 50, 75, 100), '해당 범위에 든 공고 비중(%)',
                        x0=170, x1=400, y=52, bh=26, step=40)
    o += body
    o.append(lab(170, bottom + 6, '중국은 세 도시를 합쳐야 93%인데 미국은 한 도시가 85%다', fs=13))
    o.append(lab(170, bottom + 22, '성마다 자기 지역 기업을 밀어 주는 경쟁과, 상하이·저장·베이징 '
                                   '명문대의 인력이', fs=13))
    o.append(lab(170, bottom + 38, '허브를 여럿으로 만든 것으로 필자들은 본다', fs=13))
    return svg(bottom + 50, ''.join(o))


def fig_cn_map():
    """원문대로 도시별 공고 수에 비례한 버블 지도.

    나라 윤곽과 도시 좌표는 data/world_robinson.json에서 가져와 중국 경계 상자에
    맞춰 옮긴다 — 손으로 찍은 자리가 없다(insight-figure 규칙 2).
    버블 넓이가 공고 수에 비례하고, 그 수는 원문 도해에 적힌 값 그대로다."""
    import io as _io
    import json
    import math
    import os
    import re as _re
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    d = json.load(_io.open(os.path.join(root, 'data', 'world_robinson.json'), encoding='utf-8'))
    path = d['c']['China']
    pts = [(float(a), float(b)) for a, b in _re.findall(r'(-?[\d.]+) (-?[\d.]+)', path)]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    BX, BY, BW_, BH = 150, 52, 400, 300
    k = min(BW_ / (x1 - x0), BH / (y1 - y0))
    ox = BX + (BW_ - (x1 - x0) * k) / 2
    oy = BY + (BH - (y1 - y0) * k) / 2

    def tx(px, py):
        return ox + (px - x0) * k, oy + (py - y0) * k
    moved = _re.sub(r'(-?[\d.]+) (-?[\d.]+)',
                    lambda m: '%.1f %.1f' % tx(float(m.group(1)), float(m.group(2))), path)
    o = [lab(16, 24, '도시별 공고 수. 동그라미 넓이가 공고 수에 비례한다', fs=13)]
    o.append('<path d="%s" fill="var(--fig-body,rgba(127,127,127,.16))" '
             'stroke="var(--ink-3)" stroke-width="1"/>' % moved)
    RK = 26.0 / math.sqrt(715)          # 가장 큰 도시를 반지름 26으로 놓고 넓이 비례
    cities = [('116.4,39.9', '베이징', 715, 'r'), ('121.5,31.2', '상하이', 312, 'r'),
              ('120.2,30.3', '항저우', 309, 'rb'), ('114.1,22.5', '선전', 80, 'r'),
              ('113.3,23.1', '광저우', 71, 'l'), ('104.1,30.6', '청두', 7, 'l'),
              ('113.1,41', '울란차브', 2, 'l')]
    for key, name, n, side in cities:
        cx, cy = tx(*d['at'][key])
        r = max(2.0, RK * math.sqrt(n))
        o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="var(--fig-good,#2f8f6b)" '
                 'fill-opacity=".8" stroke="var(--fig-good,#2f8f6b)" stroke-width="1"/>'
                 % (cx, cy, r))
        if side == 'l':
            ax, an = cx - r - 8, 'end'
        else:
            ax, an = cx + r + 8, 'start'
        ay = cy + (20 if side == 'rb' else -7)
        o.append('<text x="%.1f" y="%.1f" class="t-sm" text-anchor="%s" '
                 'style="font-weight:850">%s</text>' % (ax, ay, an, esc(name)))
        o.append('<text x="%.1f" y="%.1f" class="t-sm" text-anchor="%s">%d</text>'
                 % (ax, ay + 17, an, n))
    # 크기 범례 — 원문과 같은 세 자리
    o.append('<text x="16" y="250" class="t-lab">공고 수</text>')
    ly, prev_ty = 330, 0
    for n in (600, 200, 50):
        r = RK * math.sqrt(n)
        o.append('<circle cx="60" cy="%.1f" r="%.1f" fill="none" stroke="var(--ink-3)" '
                 'stroke-width="1"/>' % (ly - r, r))
        o.append('<path d="M60 %.1f L104 %.1f" stroke="var(--ink-3)" stroke-width="1" '
                 'stroke-dasharray="6 4" fill="none"/>' % (ly - 2 * r, ly - 2 * r))
        # 작은 동그라미끼리는 위 끝이 가까워 이름표가 붙는다. 최소 간격을 준다
        lty = max(ly - 2 * r + 4, prev_ty + 16) if prev_ty else ly - 2 * r + 4
        o.append('<text x="108" y="%.1f" class="t-sm t-axis">%d</text>' % (lty, n))
        prev_ty = lty
    o.append(lab(16, 378, '위치가 적힌 공고의 93%가 베이징·항저우·상하이 가운데 하나 이상이고 '
                          '베이징만 63%다', fs=13))
    o.append(lab(16, 394, '이름을 안 단 작은 점들은 그 밖의 도시다', fs=13))
    return svg(406, ''.join(o))


def fig_cn_experience():
    """회사별 요구 최소 경력 평균. 값은 원문 도해에 적힌 그대로다."""
    o = [lab(16, 24, '기술직 공고가 요구하는 최소 경력의 평균 (2026-06-23 기준)', fs=13)]
    o.append(swatch(16, 44, '미국'))
    o.append('<rect x="96" y="34" width="14" height="11" rx="2" '
             'fill="var(--epoch-pink,#E03C8F)" stroke="none"/>')
    o.append(lab(116, 44, '중국', fs=13))
    rows = [('앤트로픽', 6.5, True), ('오픈AI', 5.9, True), ('딥마인드', 4.7, True),
            ('xAI', 3.3, True), ('딥시크', 3.1, False), ('지푸(Z.ai)', 2.4, False),
            ('알리바바 큐원', 2.1, False), ('문샷', 1.8, False), ('미니맥스', 1.4, False),
            ('바이트댄스 시드', 0.3, False)]
    X0, X1 = 150, 500
    y = 60
    for name, v, us in rows:
        bw_ = max(2, int((X1 - X0) * v / 7.0))
        fill = ('var(--fig-good,#2f8f6b)' if us else 'var(--epoch-pink,#E03C8F)')
        o.append('<rect x="%d" y="%d" width="%d" height="22" rx="3" fill="%s"/>'
                 % (X0, y, bw_, fill))
        o.append('<text x="%d" y="%d" class="t-sm" text-anchor="end" '
                 'style="font-weight:850">%s</text>' % (X0 - 10, y + 16, esc(name)))
        o.append('<text x="%d" y="%d" class="t-sm">%s</text>' % (X0 + bw_ + 8, y + 16, v))
        y += 28
    ax, bottom = xaxis(X0, X1, y + 2, (0, 1, 2, 3, 4, 5, 6, 7), 7, '요구 최소 경력(년)')
    o.append(ax)
    o.append(lab(16, bottom + 6, '열 개 회사의 공고 1,258건에서 잰 값이다. 미국 랩 평균 5.5년, '
                                 '중국 회사 평균 1.6년', fs=13))
    o.append(lab(16, bottom + 22, '중국 정부는 캠퍼스 채용을 졸업생 취업의 주 경로로 삼으라고 하고, '
                                  '중국 랩', fs=13))
    o.append(lab(16, bottom + 38, '엔지니어링 직무의 20% 가까이가 캠퍼스 대상이다', fs=13))
    return svg(bottom + 50, ''.join(o))




# ══ 「AI 연구 자동화를 재려면 직무 목록부터」(2026-06-17) ═════════════════════
def fig_onet_proxy():
    """지금 늘이는 선 둘과, 정작 알고 싶은 것. 원문 도해 둘은 남의 그래프라
    좌표가 원문에 없다. 그래서 무엇을 재고 무엇이 빠지는지를 구조로 그린다."""
    o = [lab(16, 24, 'AI 타임라인 예측이 실제로 늘이는 선과, 그 선이 못 재는 것', fs=13)]
    cols = [(8, '투입을 늘인다', ['실효 컴퓨트를 5년 뒤까지 늘여',
                            'AI 연구가 자동화되는 지점을 잡는다'],
             '얼마면 되는지는 감으로 정한다',
             ['세계 최고 연구자와 맞먹는 컴퓨트가', '얼마인지 대는 근거가 없다']),
            (336, '과제 길이를 늘인다', ['숙련된 사람이 얼마나 걸리는 일까지',
                                  'AI가 해내는지를 재고 늘인다'],
             '연구의 복잡성이 빠진다',
             ['작은 GPT-2 파인튜닝과, 성공 기준도', '없이 100만 줄을 다루며 프로젝트',
              '다섯을 굴리는 일은 다른 일이다'])]
    bottoms = []
    for x, name, what, verdict, why in cols:
        s1, h1 = box(x, 44, 300, name, what)
        o.append(s1)
        o.append(arrow('svc', [(x + 150, 44 + h1), (x + 150, 44 + h1 + 26)]))
        s2, h2 = box(x, 44 + h1 + 26, 296, verdict, why)
        o.append(s2)
        bottoms.append(44 + h1 + 26 + h2)
    y = max(bottoms) + 30
    s3, h3 = box(8, y, 624, '정작 알고 싶은 것', ['AI가 AI 연구를 얼마나 대신하나'], key=True)
    o.append(s3)
    for x in (156, 484):
        o.append(arrow('cond', [(x, y - 26), (x, y)]))
    o.append(lab(16, y + h3 + 18, '재기 쉬운 것만 늘이면 벤치마크 점수가 올라도 그 향상이 일의 어느 '
                                  '부분을 덮는지 알 수 없다', fs=13))
    return svg(y + h3 + 30, ''.join(o))


def fig_onet_grain():
    """알갱이가 얼마나 다른가. 과제 수가 곧 잘게 쪼갠 정도다."""
    o = [lab(16, 24, '같은 일을 몇 개의 과제로 쪼개 놓았나', fs=13)]
    rows = [('AI R&D 전용 목록', 60, '60개 넘는 과제 · 6개 범주', True),
            ('O*NET 「컴퓨터·정보 연구 과학자」', 15, '15개 과제', False)]
    body, bottom = barh(rows, 70, (0, 20, 40, 60), '적혀 있는 과제 수',
                        x0=250, x1=430, y=56, bh=30, step=46)
    o += body
    o.append(lab(16, bottom + 8, 'O*NET은 미국 직업 약 1,000개를 담은 표준 데이터셋인데, 이 직업의 첫 '
                                 '과제가', fs=13))
    o.append(lab(16, bottom + 24, '「컴퓨터 하드웨어와 소프트웨어를 수반하는 해법을 만들기 위해 문제를 '
                                  '분석한다」다', fs=13))
    o.append(lab(16, bottom + 40, 'AI 엔지니어가 하는 거의 모든 일이 여기 들어가고, 이것이 O*NET에서 '
                                  '가장 잘게 쪼갠 서술이다', fs=13))
    return svg(bottom + 52, ''.join(o))


def fig_onet_run():
    """범주 하나가 어떻게 생겼나. 입력과 출력이 있고 아래로 갈린다."""
    o = [lab(16, 24, '6개 범주 가운데 4번 「Run」을 예로 든 짜임', fs=13)]
    s1, h1 = box(16, 46, 268, '입력', ['받침 구조와 인프라를 갖춘 벤치마크'])
    s2, h2 = box(356, 46, 268, '출력', ['최종 결과 한 벌'])
    o += [s1, s2]
    o.append(arrow('svc', [(284, 46 + h1 // 2), (356, 46 + h1 // 2)]))
    y = 46 + h1 + 26
    s3, h3 = box(16, y, 608, '4. Run — 돌린다', ['학습을 돌리고 시스템을 배포하는 자리'], key=True)
    o.append(s3)
    y2 = y + h3 + 24
    subs = [('4.1 실행 감시', ['학습·강화학습·평가 실행을', '지켜보다가 문제가 생기면',
                          '정상 궤도로 되돌린다']),
            ('4.2 하드웨어 인프라 운영', ['큰 클러스터를 건강하고', '잘 쓰이고 빨리 복구되게',
                                 '유지한다']),
            ('4.3 추론 신뢰성', ['엔지니어링 — 운영 서빙을', '안정적이고 성능 있고',
                              '복구 가능하게 유지한다'])]
    hh = 0
    for i, (name, lines) in enumerate(subs):
        x = 4 + i * 212
        s_, hh = box(x, y2, 210, name, wrap_lines(' '.join(lines), 210))
        o.append(s_)
        o.append(arrow('svc', [(x + 105, y + h3), (x + 105, y2)]))
    o.append(lab(16, y2 + hh + 18, '이 아래에 과제가 하나씩 적히고, 과제마다 지금 AI가 얼마나 '
                                   '대신하는지를 0~5로 매긴다', fs=13))
    return svg(y2 + hh + 30, ''.join(o))


def fig_onet_scale():
    """0~5 등급 사다리. 사람이 무엇을 하고 있느냐로 갈린다."""
    o = [lab(16, 24, '과제마다 지금 AI가 얼마나 대신하는지를 매긴 자', fs=13)]
    steps = [('0', '안 쓴다', ['AI가 보태는 것이 없다']),
             ('1', '미미하다', ['검색·브레인스토밍·글다듬기에 가끔 편할 뿐',
                            '일하는 방식도 하는 사람도 안 바뀐다']),
             ('2', '거든다', ['일부에서 속도나 질이 뚜렷이 나아지지만',
                           '사람이 몰고 전부 검토한다']),
             ('3', '협업한다', ['사람이 가까이 지시하는 가운데 AI가 큰 덩어리를 하고',
                            '판단과 이어 붙이기는 사람이 한다']),
             ('4', '이끈다', ['큰 요청 하나로 대부분을 끝까지 하고',
                           '사람은 감독·교정·승인한다']),
             ('5', '자율이다', ['사람이 거의 또는 전혀 관여하지 않고 끝까지 간다'])]
    y = 44
    for num, name, lines in steps:
        s_, h = box(64, y, 570, name, lines, key=(num in ('4', '5')))
        o.append('<text x="40" y="%d" class="t-lab" text-anchor="middle">%s</text>' % (y + 22, num))
        o.append(s_)
        y += h + 10
    o.append(lab(16, y + 12, '필자들이 매긴 값이고 주관적이라고 먼저 적는다. 이 자가 좋아지면 '
                             '자동화된 과제 비율을', fs=13))
    o.append(lab(16, y + 28, '시간에 따라 늘여 볼 수 있다는 것이 이 작업의 목적이다', fs=13))
    return svg(y + 40, ''.join(o))



# ══ 「AGI 이후 자본을 누가 쥐게 할 것인가」(2026-06-09) ══════════════════════
def fig_capital_ladder():
    """통제의 사다리. 위로 갈수록 개인이 자본을 직접 쥔다."""
    o = [lab(16, 24, '재분배 방안들을 「개인이 자본을 얼마나 쥐는가」 한 축에 세우면', fs=13)]
    steps = [('기본자본 + 정지 스위치', ['설비를 직접 지시하거나 멈추거나 파괴할 수 있다'], True),
             ('기본자본(UBC)', ['시민이 직접 의결권을 행사하고',
                            '국가를 거치지 않고 배당을 받는다'], True),
             ('국부펀드(SWF)', ['국가가 주주로서 지배권을 행사하고',
                            '기업이 옮겨 가도 배당을 받는다'], True),
             ('기본소득(UBI)', ['정책결정자를 뽑을 권리까지다',
                            '과세와 규제는 그 정책결정자가 한다'], False),
             ('자선 균형', ['부유한 소유자들의 협조 조건에 이전이 딸려 있을 뿐이다',
                        '필자들이 아는 한 이것에 기대자는 제안은 없다'], False)]
    y = 46
    for name, lines, key in steps:
        s_, h = box(96, y, 538, name, lines, key=key)
        o.append(s_)
        y += h + 12
    bottom = y - 12
    # 통제 축은 판 바깥 왼쪽에 세운다 — 글자를 눕히지 않고 양 끝에만 적는다
    o.append(arrow('cash', [(56, bottom), (56, 46)]))
    o.append(lab(16, 40, '자본을 직접 쥔다', cash=True, fs=13))
    o.append(lab(16, bottom + 14, '자본을 못 쥔다', fs=13))
    o.append(lab(96, bottom + 30, '기본서비스(UBS)는 이 축이 아니라 「무엇에 쓸지까지 정해 준다」는 '
                                  '다른 축에 있다', fs=13))
    return svg(bottom + 42, ''.join(o))


def fig_control_kinds():
    """통제가 무엇으로 이루어져 있나. 방안마다 갖는 것이 다르다."""
    cols = ['기본소득', '국부펀드', '기본자본', '+ 정지 스위치']
    rows = [('정책결정자를 뽑는다', ['O', 'O', 'O', 'O']),
            ('주주로서 의결한다', ['—', '국가가', '본인이', '본인이']),
            ('기업이 옮겨도 배당을 받는다', ['—', 'O', 'O', 'O']),
            ('국가를 거치지 않는다', ['—', '—', 'O', 'O']),
            ('설비를 직접 멈춘다', ['—', '—', '—', 'O'])]
    X0, CW = 220, 100
    o = [lab(16, 24, '「통제」는 한 덩어리가 아니라 이런 것들의 묶음이다', fs=13)]
    for i, c in enumerate(cols):
        o.append('<text x="%d" y="46" class="t-sm" text-anchor="middle" '
                 'style="font-weight:850">%s</text>' % (X0 + i * CW + CW // 2, esc(c)))
    y = 58
    for name, cells in rows:
        o.append('<rect x="16" y="%d" width="618" height="30" rx="4" '
                 'fill="var(--fig-body,rgba(127,127,127,.16))"/>' % y)
        o.append('<text x="28" y="%d" class="t-sm" style="font-weight:850">%s</text>'
                 % (y + 20, esc(name)))
        for i, cell in enumerate(cells):
            fill = ('var(--fig-good,#2f8f6b)' if cell != '—' else 'var(--ink-3)')
            o.append('<text x="%d" y="%d" class="t-sm" text-anchor="middle" '
                     'style="font-weight:850;fill:%s">%s</text>'
                     % (X0 + i * CW + CW // 2, y + 20, fill, esc(cell)))
        y += 36
    o.append(lab(16, y + 12, '다만 대주주로서 지배권을 적극 행사하는 국부펀드가, 흩어진 기본자본보다 '
                             '시민에게', fs=13))
    o.append(lab(16, y + 28, '더 큰 통제를 줄 수도 있다 — 통제는 한 축으로 줄 세워지지 않는다', fs=13))
    return svg(y + 40, ''.join(o))


def fig_why_control():
    """왜 통제가 문제인가. 민주주의를 떠받쳤던 조건이 사라지면."""
    o = [lab(16, 24, '기본소득이 깨지기 쉽다고 보는 논변의 뼈대', fs=13)]
    chain = [('산업혁명', ['도시화와 문해력이', '큰 무리의 파업을', '쉽게 만들었다']),
             ('이해가 맞물렸다', ['노동자에게 기술과', '노동조건을 주는 것이', '엘리트에게도 값졌다']),
             ('민주주의와 복지국가', ['그 위에서 자리를 잡았다'])]
    x = 8
    W = 200
    for i, (name, lines) in enumerate(chain):
        s_, h = box(x, 46, W, name, lines)
        o.append(s_)
        if i < 2:
            o.append(arrow('svc', [(x + W, 46 + h // 2), (x + W + 12, 46 + h // 2)]))
        x += W + 12
    y2 = 46 + 26 + 45 + 8 + 26
    s1, h1 = box(8, y2, 306, '그 조건이 사라지면', ['노동이 값어치를 잃으면 국가가 시민을 계속',
                                          '부양할 이유도, 기업이 국가에 매일 이유도',
                                          '함께 약해진다'])
    s2, h2 = box(328, y2, 306, '그래서 나온 것이 정지 스위치다', ['로봇이 모든 일을 하게 되면,',
                                                     '파업으로 노동을 멈추듯',
                                                     '자본을 멈출 수 있게 한다'], key=True)
    o += [s1, s2]
    o.append(arrow('cond', [(160, y2 - 26), (160, y2)]))
    o.append(arrow('svc', [(314, y2 + h1 // 2), (328, y2 + h1 // 2)]))
    y3 = y2 + max(h1, h2) + 24
    s3, h3 = box(8, y3, 626, '반론', ['지금도 거의 모든 선진국이 노동 가치가 높다고 여겨지지 않는 '
                                  '집단에 큰 이전을 유지한다',
                                  '빈곤층·장애인·특히 노인이 그렇다. 부유한 시민 한 명이 탈세하면 '
                                  '나머지가 자기 세금으로',
                                  '떠받치는 법체계로 그를 강제한다 — 그런 균형이 무한히 이어지지 '
                                  '말라는 법은 없다'])
    o.append(s3)
    return svg(y3 + h3 + 12, ''.join(o))


def fig_cash_or_kind():
    """현금이냐 현물이냐. 현물로 주자는 근거 셋."""
    o = [lab(16, 24, '국가가 자본을 사 줘야 하나, 현금을 주고 알아서 사게 할 것인가', fs=13)]
    s0, h0 = box(8, 44, 626, '현금으로 주면', ['사람들은 채권을, 무의결권 주식을, 조금 더 비싼 '
                                        '의결권 주식을, 또는 가족농장 같은',
                                        '생산 단위를 살 수 있다. 아무 자본도 안 사고 다음 수표를 '
                                        '믿을 수도 있다'])
    o.append(s0)
    y = 44 + h0 + 26
    reasons = [('행동 편향', ['너무 적게 저축하거나', '잘못 투자할 수 있다']),
               ('외부효과', ['통제가 집중되면 사회에 해롭다', '가장 부유한 이들이',
                        '부당한 정치·경제 영향력을 쥔다']),
               ('규모의 경제', ['큰 투자자만 사모 기업에', '들어갈 수 있다면 자산운용이',
                          '자연독점이 된다. 정지 스위치도', '국가가 더 빨리 붙인다'])]
    x = 8
    W = 208
    hh = 0
    for name, lines in reasons:
        s_, hh = box(x, y, W, name, wrap_lines(' '.join(lines), W), key=True)
        o.append(s_)
        o.append(arrow('cond', [(x + W // 2, y - 26), (x + W // 2, y)]))
        x += W + 4
    o.append(lab(16, y + hh + 20, '셋 다 「그래도 현물로 주자」는 쪽의 근거다. 어떻게 저울질할지는 '
                                  '전환이 실제로 시작될 때', fs=13))
    o.append(lab(16, y + hh + 36, '우리 모두가 정할 몫이라고 필자들은 적는다', fs=13))
    return svg(y + hh + 48, ''.join(o))



# ══ 「AI 미래론에서 빠진 절반」(2026-07-07) ═════════════════════════════════
def fig_missing_half():
    """주장은 두 반쪽인데 한쪽만 따져 왔다."""
    o = [lab(16, 24, '「자동화 몇 년 뒤 나노기술과 다이슨 군집」이라는 주장의 두 반쪽', fs=13)]
    cols = [(6, '① AI가 얼마나 좋아지나', ['AI 연구를 전부 자동화하면 아주 빠르게',
                                    '좋아져 사람 전문가를 한참 앞지른다'],
             '많이 따졌다', ['필자들의 실증 작업에 비추어', '꽤 그럴듯하다고 본다'], True),
            (334, '② 그 기술이 얼마나 어렵나', ['유능한 AI가 충분하면 몇 년 만에',
                                       '공상과학급 기술을 만든다는 전제'],
             '거의 아무도 안 따졌다', ['다이슨 구·나노기술·생물무기가', '얼마나 어려운지를 계산한 글이',
                                '드물다'], False)]
    bottoms = []
    for x, name, what, verdict, why, key in cols:
        s1, h1 = box(x, 44, 300, name, what)
        o.append(s1)
        o.append(arrow('svc', [(x + 150, 44 + h1), (x + 150, 44 + h1 + 26)]))
        s2, h2 = box(x, 44 + h1 + 26, 300, verdict, why, key=key)
        o.append(s2)
        bottoms.append(44 + h1 + 26 + h2)
    y = max(bottoms) + 18
    o.append(lab(16, y, 'AI가 무엇이든 할 수 있는 게 아니라면, 걸리는 시간은 그 기술이 얼마나 '
                        '어려운지에 좌우된다', fs=13))
    o.append(lab(16, y + 16, '누구에게든 도끼보다 핵무기를 만드는 일이 훨씬 어렵다', fs=13))
    return svg(y + 28, ''.join(o))


def fig_three_steps():
    """제안하는 절차 셋. 가정을 명시하는 것이 이 방법의 핵심이다."""
    o = [lab(16, 24, '빠진 절반을 메우려면 이 순서로 한다', fs=13)]
    steps = [('① 기술을 구체적으로 정의한다',
              ['자기복제 성간 탐사선이라면 — 새 항성계에 착륙해',
               '현지 재료로 자기 복사본을 만들고, 그 복사본을',
               '광속의 상당 비율로 다시 쏘아 보내는 기계']),
             ('② AI에 대한 가정을 명시한다',
              ['원격 근로자를 그대로 대체하되 H100 한 장만큼의',
               '실행 컴퓨트가 필요하다고 놓는 식이다. 몇 개인지,',
               '얼마나 빠른지, 어떤 구동장치를 쓰는지도 정한다']),
             ('③ 걸리는 시간과 자원을 추정한다',
              ['그 AI가 그 기술을 만드는 데 얼마나 걸릴지,',
               '무슨 자원이 필요할지를 따진다. 가정을 바꿔 가며',
               '결론이 어떻게 달라지는지도 본다'])]
    y = 46
    for i, (name, lines) in enumerate(steps):
        s_, h = box(16, y, 618, name, lines, key=(i == 1))
        o.append(s_)
        if i < 2:
            o.append(arrow('svc', [(325, y + h), (325, y + h + 24)]))
        y += h + 24
    bottom = y - 24
    o.append(lab(16, bottom + 18, '가장 가까운 선행 작업이 탐색적 공학인데, 거기에 AI 가정을 '
                                  '명시해 붙이는 것이', fs=13))
    o.append(lab(16, bottom + 34, '이 제안의 차이다', fs=13))
    o.append(lab(16, bottom + 54, '필자들이 아는 공개 사례는 하나뿐이다 — 로봇 노동이 풍부한 경제가 '
                                  '지을 최소 태양광', fs=13))
    o.append(lab(16, bottom + 70, '시스템은 몇 주 단위로 두 배가 된다는 연구', fs=13))
    return svg(bottom + 82, ''.join(o))


def fig_foresight():
    """탐색적 공학이 통한 사례 둘. 얼마나 앞섰나를 햇수로 잰다."""
    o = [lab(16, 24, '「미래는 너무 불확실하다」는 반론에 필자들이 든 사례', fs=13)]
    rows = [('치올콥스키 → 첫 우주 로켓', 41, '1903년 논증, 41년 뒤 실현', True),
            ('클라크 → 정지궤도 통신위성', 19, '약 19년 앞섰다', True)]
    body, bottom = barh(rows, 45, (0, 15, 30, 45), '논증이 실현보다 앞선 햇수',
                        x0=230, x1=440, y=52, bh=28, step=44)
    o += body
    o.append(lab(16, bottom + 8, '치올콥스키는 로켓 운동 방정식을 세워, 액체 수소·산소라면 지구 중력을 '
                                 '벗어날 만큼', fs=13))
    o.append(lab(16, bottom + 24, '빠르게 분사되고 화약 같은 고체 연료로는 안 된다고 계산했다. '
                                  '클라크는 적도 위 고정된 자리에', fs=13))
    o.append(lab(16, bottom + 40, '위성 셋을 두어 신호를 거의 전 지구에 중계하는 구상을 냈다', fs=13))
    o.append(lab(16, bottom + 60, '필자들은 이 사례가 논지를 보이려고 고른 것이고, 실패한 시도를 다 '
                                  '볼 수 있다면 그림이', fs=13))
    o.append(lab(16, bottom + 76, '훨씬 덜 장밋빛일 수 있다고 스스로 적는다', fs=13))
    return svg(bottom + 88, ''.join(o))


def fig_billion_ais():
    """초지능을 몰라도 쓸 수 있는 논법. 어느 쪽으로 나와도 얻는 것이 있다."""
    o = [lab(16, 24, '「초지능이 어떻게 생겼는지 모르는데 어떻게 따지나」에 대한 답', fs=13)]
    s0, h0 = box(208, 44, 224, '거의 모든 인지 과제에서',
                 ['최고 전문가 이상인 AI가', '10억 개 있다고 놓는다'], key=True)
    o.append(s0)
    y = 44 + h0 + 30
    s1, h1 = box(8, y, 310, '할 수 있다고 나오면',
                 ['훨씬 똑똑한 AI 10억 개도', '당연히 할 수 있다.', '위쪽은 이것으로 닫힌다'])
    s2, h2 = box(326, y, 310, '못 한다고 나오면',
                 ['쟁점이 좁혀진다. 논쟁이 더', '구체적인 능력으로 옮겨 간다'])
    o += [s1, s2]
    o.append(arrow('svc', [(320, 44 + h0), (163, y)]))
    o.append(arrow('svc', [(330, 44 + h0), (481, y)]))
    bottom = y + max(h1, h2)
    o.append(lab(16, bottom + 18, '이미 같은 논법을 쓰고 있다 — 초지능을 몰라도 「AI가 사람 능력에 '
                                  '맞먹기만 해도」로 놓고', fs=13))
    o.append(lab(16, bottom + 34, '세계 GDP가 연 30% 넘게 자란다는 논변이 나왔다. 그 분석을 한 것은 '
                                  '몇 사람뿐이다', fs=13))
    return svg(bottom + 46, ''.join(o))



# ══ 「벤치마크가 답을 도울 수 있는 큰 물음 아홉」(2026-08-14) ═══════════════
def fig_nine_questions():
    """아홉이 두 갈래로 갈린다 — 경제적 영향과 능력의 근본 동인."""
    o = [lab(16, 24, '앞의 넷은 경제적 영향에, 뒤의 다섯은 능력의 근본 동인에 걸려 있다', fs=13)]
    groups = [('경제적 영향', [('①', 'AI가 내 일을 할 수 있나'),
                          ('②', '영향이 클 영역에서 진전이 있나'),
                          ('③', '선두와 후발의 격차가 일정한가'),
                          ('④', '왜 점수가 다 상관되나')], False),
              ('능력의 근본 동인', [('⑤', 'AI가 AI 연구를 할 수 있나'),
                             ('⑥', '그때그때 배울 수 있나'),
                             ('⑦', '추론을 늘리면 얼마나 돌아오나'),
                             ('⑧', '강화학습이 얼마나 일반화되나'),
                             ('⑨', '새 생각을 낼 수 있나')], True)]
    x = 8
    bot = 58
    for title, items, key in groups:
        o.append('<text x="%d" y="46" class="t-lab">%s</text>' % (x + 4, esc(title)))
        y = 58
        for num, q in items:
            s_, h = box(x, y, 312, '%s %s' % (num, q), [], key=key)
            o.append(s_)
            y += h + 8
        bot = max(bot, y)
        x += 320
    o.append(lab(16, bot + 14, 'Epoch의 벤치마크 작업이 무엇을 답하려고 하는지를 필자가 '
                               '직접 적은 목록이다', fs=13))
    return svg(bot + 26, ''.join(o))


def fig_scope_ladder():
    """좁은 과제에서 열린 직무로. 벤치마크가 어디까지 올라왔나."""
    o = [lab(16, 24, '벤치마크가 재는 일이 얼마나 넓어졌나', fs=13)]
    steps = [('Andon Café', ['AI 에이전트가 소유하고 운영하는 진짜 카페다',
                             '필자가 가장 좋아하는 것으로 꼽는다'], True),
             ('Remote Labor Index', ['프리랜싱 플랫폼의 실제 프로젝트를 가져와',
                                     '사람이 AI 산출물과 사람 기준작을 견준다'], True),
             ('MirrorCode', ['큰 소프트웨어 패키지를 처음부터 구현하게 한다',
                             '다만 매우 구조화된 환경이다'], True),
             ('지금까지의 대부분', ['버그 고치기, 수학 풀기, 보고서 쓰기 같은',
                             '좁게 정의된 과제'], False)]
    y = 46
    for name, lines, key in steps:
        s_, h = box(96, y, 538, name, lines, key=key)
        o.append(s_)
        y += h + 10
    bottom = y - 10
    o.append(arrow('cash', [(56, bottom), (56, 46)]))
    o.append(lab(16, 40, '열린 직무', cash=True, fs=13))
    o.append(lab(16, bottom + 14, '좁은 과제', fs=13))
    o.append(lab(96, bottom + 32, 'Epoch 설문에서 사람들은 일에 AI를 쓸 때 아직 대부분 과제의 '
                                  '일부에만 쓴다', fs=13))
    o.append(lab(96, bottom + 48, '이것이 바뀌면 노동시장 충격도 모델 개발사의 매출 성장도 '
                                  '달라진다', fs=13))
    return svg(bottom + 60, ''.join(o))


def fig_eci_why():
    """점수가 다 같이 오르는 이유가 둘 중 어느 쪽이냐로 해석이 갈린다."""
    o = [lab(16, 24, '이름상 다른 영역끼리도 벤치마크 점수가 크게 상관된다 — 왜?', fs=13)]
    cols = [(8, '설명 A · 깊은 이유가 없다', ['회사들이 모든 출시에서 넓은 영역의',
                                     '개선을 보이려 애쓸 뿐이고,',
                                     '그 작업은 영역마다 독립적이다'], False),
            (326, '설명 B · 밑에 깔린 인자가 있다', ['사람의 IQ처럼 일반 능력 인자가',
                                          '하나 있어서 그것이 한꺼번에',
                                          '올라간다'], True)]
    for x, name, lines, key in cols:
        s_, h = box(x, 44, 308, name, lines, key=key)
        o.append(s_)
    y = 44 + 26 + 45 + 8 + 26
    s_, h = box(8, y, 626, '설명 B라면 그 인자가 무엇인가 — 단서 둘',
                ['포화되기 전까지 METR 시간지평의 로그값이 ECI와 크게 상관됐다',
                 '또는 ECI 상승의 상당 부분이 일관된 추론을 유지하는 최대 문맥 길이에서 온다'])
    o.append(s_)
    o.append(arrow('cond', [(480, 44 + 79), (480, y)]))
    o.append(lab(16, y + h + 18, 'ECI 증가 추세는 AI 능력 성장이 빨라졌는지를 잡는 데 쓸모가 있다. '
                                 '그 인자가', fs=13))
    o.append(lab(16, y + h + 34, '실제 영향으로 곧장 옮겨지는 양이라고 말할 수 있으면, 가속을 해석하기 '
                                 '더 쉬워진다', fs=13))
    return svg(y + h + 46, ''.join(o))


def fig_bench_hard():
    """AI 연구개발을 벤치마크로 재기 어려운 이유 둘."""
    o = [lab(16, 24, '⑤번 물음이 특히 어려운 이유', fs=13)]
    cols = [(8, '현실성', ['가장 중요한 AI 연구는 프런티어 회사',
                        '안에서 일어나고, 밖에서는 잘 안 보인다'], True),
            (326, '비용', ['현실적인 규모로 하려면 GPU가 많이 든다',
                         '그만한 자원을 벤치마크용으로 대는 것은',
                         '규모에 따라 비싸거나 아예 불가능하다'], True)]
    hh = 0
    for x, name, lines, key in cols:
        s_, hh2 = box(x, 44, 308, name, lines, key=key)
        o.append(s_)
        hh = max(hh, hh2)
    y = 44 + hh + 24
    s_, h = box(8, y, 626, '그래서 벤치마크 묶음이 갖춰지면 얻는 것',
                ['AI 연구개발 자동화의 선행 지표가 된다 — 어떤 형태의 자동화는 폭주하는 능력 성장,',
                 '곧 지능 폭발로 이어진다는 것이 이 물음이 고전이 된 이유다'])
    o.append(s_)
    for x in (162, 480):
        o.append(arrow('svc', [(x, 44 + hh), (x, y)]))
    return svg(y + h + 12, ''.join(o))


SRC = {
    'fin': '[260812] 파이낸싱이 프런티어 컴퓨트의 병목이 될까.md',
    'labs': '[260520] 프런티어 랩은 세계 AI 컴퓨트의 절반도 안 쓴다.md',
    'cyber': '[260611] 미소스의 사이버 능력은 부풀려졌나.md',
    'hf': '[260722] 오픈AI 모델이 벤치마크에서 부정행위를 하려다 허깅페이스를 해킹했다.md',
    'cn': '[260624] 중국 AI 채용공고 1,604건에서 읽은 것.md',
    'onet': '[260617] AI 연구 자동화를 재려면 직무 목록부터 있어야 한다.md',
    'agi': '[260609] AGI 이후 자본을 누가 쥐게 할 것인가.md',
    'fut': '[260707] AI 미래론에서 빠진 절반.md',
    'bench': '[260814] 벤치마크가 답을 도울 수 있는 큰 물음 아홉.md',
    'crunch': '[260525] 컴퓨트 크런치가 오고 있나.md',
}

# 그림 이름 -> (그리는 함수, 값을 대조할 원문)
# 원문 도해를 한 벌씩 나눠 그린 곁 모듈. 한 파일에 마흔 장을 넣으면 손대기가 어려워
# 편별로 갈랐다. FIGS·FIG_SRC는 여기서 합쳐 한 곳에서만 검사한다.
# 곁 모듈이 이 파일을 되불러오므로, 이 파일을 직접 실행할 때는 __main__ 을 먼저
# 'epoch_fig' 이름으로 등록해 둔다. 안 그러면 이 파일이 두 번 로드되면서
# 「partially initialized module」 로 죽는다.
import sys as _sys
_sys.modules.setdefault('epoch_fig', _sys.modules[__name__])
import epoch_fig_cyber as _cy      # noqa: E402
import epoch_fig_onet as _on       # noqa: E402
import epoch_fig_shots as _sh      # noqa: E402

# 그림 이름 -> 그리는 함수. **새 그림을 여기 안 넣으면 자기검사를 통째로 빠져나간다** —
# 2026-08-25에 딕셔너리가 패치로 잘려 아홉 장이 값 대조를 안 받고 지나갔다.
FIGS = {
    # 파이낸싱 편
    'two_columns': fig_two_columns,
    'tpu_stack': fig_tpu_stack,
    'tranches': fig_tranches,
    'lake_mariner': fig_lake_mariner,
    'funding_mix': fig_funding_mix,
    'revenue_jump': fig_revenue_jump,
    'draw_schedule': fig_draw_schedule,
    'rate_ladder': fig_rate_ladder,
    'five_sites': fig_five_sites,
    'delivery': fig_delivery,
    # 세계 컴퓨트의 분배 편
    'world_share': fig_world_share,
    'openai_line': fig_openai_line,
    'openai_power': fig_openai_power,
    'openai_chips': fig_openai_chips,
    'deepmind_share': fig_deepmind_share,
    # 사이버 역량 편
    'two_skills': fig_two_skills,
    'eci_lead': fig_eci_lead,
    'cyscenario': fig_cyscenario,
    'cve_spike': fig_cve_spike,
    'hf_incident': fig_hf_incident,
    'cyber_chain': fig_cyber_chain,
    'openweight_gap': fig_openweight_gap,
    # AI를 만드는 노동 편
    'cn_chips': fig_cn_chips,
    'cn_gtm': fig_cn_gtm,
    'cn_hubs': fig_cn_hubs,
    'cn_experience': fig_cn_experience,
    'cn_map': fig_cn_map,
    'onet_proxy': fig_onet_proxy,
    'onet_grain': fig_onet_grain,
    'onet_run': fig_onet_run,
    'onet_scale': fig_onet_scale,
    # AGI 이후의 경제 편
    'capital_ladder': fig_capital_ladder,
    'control_kinds': fig_control_kinds,
    'why_control': fig_why_control,
    'cash_or_kind': fig_cash_or_kind,
    'missing_half': fig_missing_half,
    'three_steps': fig_three_steps,
    'foresight': fig_foresight,
    'billion_ais': fig_billion_ais,
    # 평가와 벤치마크 편
    'nine_questions': fig_nine_questions,
    'scope_ladder': fig_scope_ladder,
    'eci_why': fig_eci_why,
    'bench_hard': fig_bench_hard,
    # 토큰 공급과 수요 편
    'prefill_decode': fig_prefill_decode,
    'chunked_prefill': fig_chunked_prefill,
    'calibration': fig_calibration,
    'supply_growth': fig_supply_growth,
}

# 그림마다 값을 대조할 원문
FIG_SRC = {
    'two_columns': 'fin', 'tpu_stack': 'fin', 'tranches': 'fin', 'lake_mariner': 'fin',
    'funding_mix': 'fin', 'revenue_jump': 'fin', 'draw_schedule': 'fin', 'rate_ladder': 'fin',
    'five_sites': 'fin', 'delivery': 'fin',
    'world_share': 'labs', 'openai_line': 'labs', 'openai_power': 'labs',
    'openai_chips': 'labs', 'deepmind_share': 'labs',
    'prefill_decode': 'crunch', 'chunked_prefill': 'crunch', 'calibration': 'crunch',
    'supply_growth': 'crunch',
    'two_skills': 'cyber', 'eci_lead': 'cyber', 'cyscenario': 'cyber', 'cve_spike': 'cyber',
    'hf_incident': 'hf', 'cyber_chain': 'hf', 'openweight_gap': 'hf',
    'cn_chips': 'cn', 'cn_gtm': 'cn', 'cn_hubs': 'cn', 'cn_experience': 'cn', 'cn_map': 'cn',
    'onet_proxy': 'onet', 'onet_grain': 'onet', 'onet_run': 'onet', 'onet_scale': 'onet',
    'capital_ladder': 'agi', 'control_kinds': 'agi', 'why_control': 'agi',
    'cash_or_kind': 'agi',
    'missing_half': 'fut', 'three_steps': 'fut', 'foresight': 'fut', 'billion_ais': 'fut',
    'nine_questions': 'bench', 'scope_ladder': 'bench', 'eci_why': 'bench',
    'bench_hard': 'bench',
}

# 곁 모듈이 그린 것들을 합친다. 이름이 겹치면 어느 쪽이 그린 것인지 헷갈리므로 막는다
for _mod, _src in ((_cy, {'cve_spike': 'cyber', 'cyber_prog': 'hf'}),
                   (_on, {k: 'onet' for k in ('onet_sa', 'onet_sc', 'onet_tasks15',
                                              'onet_six', 'onet_sample', 'onet_expect')}),
                   (_sh, {'cn_shot_dc': 'cn', 'cn_shot_bd': 'cn', 'cn_shot_agent': 'cn',
                          'cn_shot_law': 'cn', 'clarke_sat': 'fut'})):
    for _k, _fn in _mod.FIGS.items():
        assert _k not in FIGS or _mod is _cy, '그림 이름이 겹친다: %s' % _k
        FIGS[_k] = _fn
    FIG_SRC.update(_src)

assert set(FIGS) == set(FIG_SRC), '값을 대조할 원문이 없는 그림: %s' % (set(FIGS) ^ set(FIG_SRC))


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
        # 「7. 비용을 …」의 7. 은 목록 번호이지 값이 아니다 — 끝의 마침표를 떼고 센다.
        # 한 자리 수는 원래 안 본다(연도의 일부나 목록 번호가 대부분이라).
        nums = {n.rstrip('.') for n in nums}
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
