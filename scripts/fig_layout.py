# -*- coding: utf-8 -*-
"""도해 배치 — 상자를 놓고, 선은 상자에서 뽑는다.

선이 상자에 안 붙는 사고는 툴 탓이 아니라 **끝점을 사람이 찍어서** 난다.
`'<path d="M485 80 L485 92"/>'` 의 485·80·92 는 상자 기하에서 나온 값이 아니라
눈으로 맞춘 값이라, 상자 하나만 옮겨도 선이 떨어진다. 여기서는 끝점을 못 찍는다 —
`plate.connect(a, b)` 가 두 상자의 변에서 좌표를 계산한다. 구조적으로 안 떨어진다.

    p = Plate(640)
    p.head('상업 실리콘 벤더', '모델랩')
    p.row(('총소유비용', '운영자가 치르는 값'), ('종단간 지연', '마지막 토큰까지', True))
    p.connect(p.at(0, 0), p.at(0, 1), '기준이 옮겨 갔다')
    svg = p.render('설계 기준 두 갈래')

칸 폭도 글자에서 나온다(`text_w`). 폭을 손으로 정하면 글자 양옆에 빈자리가 남고
그만큼 글자를 못 키운다 — `aie_figs.w_of` 와 같은 셈이다.

내보내는 SVG 에는 `data-fig-layout="1"` 이 붙는다. `scratchpad/check_fig.py` 의 F5
(선 끝이 상자에 닿았나) 는 그 표시가 붙은 도해만 본다 — 손으로 찍은 옛 도해까지
소급해 막지는 않는다.
"""

FS = 12.0            # 판 안 글자 크기. 카드 도해의 .fg 와 같다
FS_S = 11.0          # 둘째 줄
LH = 16.0            # 줄 간격
PAD_X = 14.0         # 상자 좌우 여백
PAD_Y = 12.0         # 상자 위아래 여백
GAP_X = 28.0         # 칸 사이 가로 틈. 화살표가 지나는 자리다
GAP_Y = 26.0         # 줄 사이 세로 틈
CHECK_CH = 9.0       # `check_fig` 가 한 글자를 이만큼으로 어림한다

CSS = '''
.fl { font: 600 12px/1.35 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  fill: var(--ink-2); }
.fl-s { font-weight: 400; font-size: 11px; fill: var(--ink-3); }
.fl-b { fill: var(--surface); stroke: var(--line); stroke-width: 1.2; }
.fl-bh { fill: var(--surface); stroke: var(--accent); stroke-width: 2; }
.fl-l { stroke: var(--line); stroke-width: 1.4; fill: none; }
.fl-d { stroke: var(--ink-3); stroke-width: 1.2; fill: none; stroke-dasharray: 3 3; }
.fl-a { stroke: var(--accent); stroke-width: 1.8; fill: none; }
'''


def text_w(s, fs=FS):
    """글줄 폭. 한글은 글자 크기만큼, 라틴·숫자는 그 55%로 잰다.

    `check_fig` 는 한 글자 9px 로 어림하는데 한글 12px 는 실제로 12px 다.
    9 로 재서 칸을 잡으면 검사기는 통과하고 화면에서는 삐져나간다. 거꾸로 라틴·숫자는
    검사기가 더 넓게 보므로, 둘 중 넓은 쪽을 쓴다 — 안 그러면 화면은 멀쩡한데
    검사기가 「칸 밖으로 삐짐」을 낸다.
    """
    w = 0.0
    for ch in s:
        if ch == ' ':
            w += fs * 0.3
        elif ord(ch) > 0x2000:       # 한글·한자·전각 기호
            w += fs
        else:
            w += fs * 0.55
    return max(w, len(s) * CHECK_CH)


class Box(object):
    """놓인 상자 하나. 변 위의 점을 준다 — 좌표는 여기서만 나온다."""

    def __init__(self, x, y, w, h, label, sub='', hi=False, rc=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label, self.sub, self.hi = label, sub, hi
        self.rc = rc                # (줄, 칸). 판을 다시 놓아도 링크를 찾아온다

    @property
    def cx(self):
        return self.x + self.w / 2.0

    @property
    def cy(self):
        return self.y + self.h / 2.0

    @property
    def x1(self):
        return self.x + self.w

    @property
    def y1(self):
        return self.y + self.h

    def port(self, side, at=0.5):
        """변 위의 점. at 은 그 변에서의 자리(0~1)."""
        if side == 'l':
            return (self.x, self.y + self.h * at)
        if side == 'r':
            return (self.x1, self.y + self.h * at)
        if side == 't':
            return (self.x + self.w * at, self.y)
        if side == 'b':
            return (self.x + self.w * at, self.y1)
        raise ValueError(side)

    def svg(self):
        cls = 'fl-bh' if self.hi else 'fl-b'
        o = ['<rect x="%g" y="%g" width="%g" height="%g" rx="6" class="%s"/>'
             % (self.x, self.y, self.w, self.h, cls)]
        if self.sub:
            o.append('<text x="%g" y="%g" class="fl" text-anchor="middle">%s</text>'
                     % (self.cx, self.cy - 2, self.label))
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle">%s</text>'
                     % (self.cx, self.cy + 13, self.sub))
        else:
            o.append('<text x="%g" y="%g" class="fl" text-anchor="middle">%s</text>'
                     % (self.cx, self.cy + 4, self.label))
        return o


class Plate(object):
    """판 하나. 칸을 격자로 놓고, 선은 놓인 상자에서 뽑는다."""

    def __init__(self, width=640.0, top=16.0, gap_x=GAP_X, gap_y=GAP_Y, mid=''):
        self.W = float(width)
        self.top = float(top)
        self.gap_x, self.gap_y = gap_x, gap_y
        self.mid = mid              # 열 사이 도랑에 세울 역할 라벨(흐름도 규칙 3)
        self.rows = []
        self.notes = []             # 판 아래 한 줄 설명
        self.links = []
        self.heads = []             # 열 이름
        self._placed = None

    # ---- 짓기 ------------------------------------------------------------
    def head(self, *names):
        self.heads = list(names)
        self._placed = None

    def row(self, *cells):
        """줄 하나. 칸은 '제목' 또는 ('제목', '부제') 또는 ('제목', '부제', True)."""
        norm = []
        for c in cells:
            if c is None:
                norm.append(None)
            elif isinstance(c, str):
                norm.append((c, '', False))
            else:
                norm.append((c[0], c[1] if len(c) > 1 else '',
                             bool(c[2]) if len(c) > 2 else False))
        self.rows.append(norm)
        self._placed = None
        return len(self.rows) - 1

    def note(self, text):
        self.notes.append(text)

    # ---- 놓기 ------------------------------------------------------------
    def _layout(self):
        """열 폭·줄 높이를 글자에서 낸다. 좌표는 여기서만 만들어진다."""
        if self._placed is not None:
            return self._placed
        if not self.rows:
            raise AssertionError('줄이 없다')
        ncol = max(len(r) for r in self.rows)
        ws = []
        for c in range(ncol):
            cand = [0.0]
            if c < len(self.heads):
                cand.append(text_w(self.heads[c], FS_S))
            for r in self.rows:
                if c < len(r) and r[c]:
                    cand.append(text_w(r[c][0]))
                    if r[c][1]:
                        cand.append(text_w(r[c][1], FS_S))
            ws.append(round(max(cand) + 2 * PAD_X))
        gap = max(self.gap_x, self._need_gap_x())
        if self.mid:
            gap = max(gap, text_w(self.mid, FS_S) + 16)
        total = sum(ws) + gap * (ncol - 1)
        if total > self.W:
            raise AssertionError('판(%g)보다 넓다: %g' % (self.W, total))
        xs, x = [], (self.W - total) / 2.0
        for w in ws:
            xs.append(x)
            x += w + gap
        y = self.top + (20.0 if self.heads else 0.0)
        gy = max(self.gap_y, self._need_gap_y())
        placed = []
        for r in self.rows:
            two = any(c and c[1] for c in r)
            h = PAD_Y * 2 + LH + (LH if two else 0)
            line = []
            for c in range(ncol):
                cell = r[c] if c < len(r) else None
                line.append(Box(xs[c], y, ws[c], h, cell[0], cell[1], cell[2],
                                (len(placed), c)) if cell else None)
            placed.append(line)
            y += h + gy
        self._placed = placed
        self._xs, self._ws, self._gap = xs, ws, gap
        self._bottom = y - gy
        return placed

    def _need_gap_x(self):
        """같은 줄을 가로로 잇는 선의 이름이 들어갈 틈.

        이름이 틈보다 넓으면 양옆 상자 테두리를 물고 앉는다 — `check_fig` 의
        「네모 테두리에 깔림」이 그것이다. 틈을 이름에 맞춰 벌린다.
        """
        need = 0.0
        for (ra, _ca), (rb, _cb), label, _k in self.links:
            if label and ra == rb:
                need = max(need, text_w(label, FS_S) + 10)
        return need

    def _need_gap_y(self):
        """줄과 줄 사이를 세로로 잇는 선의 이름이 앉을 띠."""
        return 30.0 if any(ra != rb and label
                           for (ra, _ca), (rb, _cb), label, _k in self.links) else 0.0

    def at(self, row, col):
        placed = self._layout()
        b = placed[row][col]
        if b is None:
            raise IndexError('빈 칸 (%d,%d)' % (row, col))
        return b

    # ---- 잇기 ------------------------------------------------------------
    def connect(self, a, b, label='', kind='l'):
        """두 상자를 잇는다. 어느 변에서 나가고 들어올지는 자리가 정한다.

        kind: 'l' 회색 실선(물건·용역) · 'a' 강조색 실선(돈) · 'd' 점선(조건부)
        """
        self.links.append((a.rc, b.rc, label, kind))
        self._placed = None         # 틈이 이름에 따라 달라진다. 다시 놓는다

    def _link_svg(self, a, b, label, kind):
        cls = {'l': 'fl-l', 'a': 'fl-a', 'd': 'fl-d'}[kind]
        mk = 'url(#flAa)' if kind == 'a' else 'url(#flA)'
        if a.x1 <= b.x - 4 or b.x1 <= a.x - 4:          # 좌우로 떨어져 있다
            fwd = a.x1 <= b.x - 4
            p0 = a.port('r' if fwd else 'l')
            p1 = b.port('l' if fwd else 'r')
            if abs(p0[1] - p1[1]) < 1.0:
                d = 'M%g %g L%g %g' % (p0[0], p0[1], p1[0], p1[1])
                lx, ly, anchor = (p0[0] + p1[0]) / 2.0, p0[1] - 6, 'middle'
            else:
                mx = (p0[0] + p1[0]) / 2.0
                d = 'M%g %g L%g %g L%g %g L%g %g' % (
                    p0[0], p0[1], mx, p0[1], mx, p1[1], p1[0], p1[1])
                lx, ly, anchor = mx, min(p0[1], p1[1]) - 6, 'middle'
        else:                                            # 위아래로 떨어져 있다
            down = a.y1 <= b.y - 4
            p0 = a.port('b' if down else 't')
            p1 = b.port('t' if down else 'b')
            if abs(p0[0] - p1[0]) < 1.0:
                d = 'M%g %g L%g %g' % (p0[0], p0[1], p1[0], p1[1])
            else:
                my = (p0[1] + p1[1]) / 2.0
                d = 'M%g %g L%g %g L%g %g L%g %g' % (
                    p0[0], p0[1], p0[0], my, p1[0], my, p1[0], p1[1])
            lx, ly, anchor = p0[0] + 9, (p0[1] + p1[1]) / 2.0 + 4, 'start'
        o = ['<path d="%s" class="%s" marker-end="%s"/>' % (d, cls, mk)]
        if label:
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="%s">%s</text>'
                     % (lx, ly, anchor, label))
        return o

    # ---- 내보내기 --------------------------------------------------------
    DEFS = ('<defs>'
            '<marker id="flA" markerWidth="8" markerHeight="8" refX="7" refY="4" '
            'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--ink-3)"/></marker>'
            '<marker id="flAa" markerWidth="8" markerHeight="8" refX="7" refY="4" '
            'orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--accent)"/></marker>'
            '</defs>')

    def render(self, alt):
        placed = self._layout()
        o = []
        if self.heads:
            for c, name in enumerate(self.heads):
                o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle">%s</text>'
                         % (self._xs[c] + self._ws[c] / 2.0, self.top + 4, name))
        for line in placed:
            for b in line:
                if b:
                    o += b.svg()
        if self.mid and len(self._xs) > 1:
            gx = (self._xs[0] + self._ws[0] + self._xs[1]) / 2.0
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle">%s</text>'
                     % (gx, self.top + (20.0 if self.heads else 0.0) - 6, self.mid))
        for (ra, ca), (rb, cb), label, kind in self.links:
            o += self._link_svg(placed[ra][ca], placed[rb][cb], label, kind)
        y = self._bottom
        for n in self.notes:
            y += 18
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle">%s</text>'
                     % (self.W / 2.0, y, n))
        h = y + 14
        return ('<svg viewBox="0 0 %g %g" width="100%%" data-fig-layout="1" role="img" '
                'aria-label="%s">%s%s</svg>' % (self.W, h, alt, self.DEFS, ''.join(o)))
