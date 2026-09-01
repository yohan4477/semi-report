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

# 판 안 글자는 본문과 같은 크기로 둔다. 판이 width:100% 라 카드 슬롯보다 넓게 잡으면
# 화면에서 배율이 1 아래로 내려가 글자가 본문보다 작아진다 — 판을 좁게(520) 잡고
# 글자를 본문 크기(.95rem ≈ 15.2px)로 맞춘다. aie_figs 가 같은 이유로 그렇게 한다
FS = 15.2            # 판 안 글자 크기 = 본문과 같다
FS_S = 13.5          # 둘째 줄
LH = 20.0            # 줄 간격
PAD_X = 14.0         # 상자 좌우 여백
PAD_Y = 12.0         # 상자 위아래 여백
GAP_X = 28.0         # 칸 사이 가로 틈. 화살표가 지나는 자리다
GAP_Y = 26.0         # 줄 사이 세로 틈
CHECK_CH = 9.0       # `check_fig` 가 한 글자를 이만큼으로 어림한다

CSS = '''
.fl { font: 600 15.2px/1.35 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;
  fill: var(--ink-2); }
.fl-s { font-weight: 400; font-size: 13.5px; fill: var(--ink-3); }
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


def _word_w(s, fs=FS):
    """`s` 안 낱말 중 가장 넓은 것의 폭. `wrap()`이 낱말 사이에서만 자르므로,
    칸이 이 폭만 넘으면 나머지는 줄 수를 늘려서라도 접힌다."""
    words = s.split(' ') if s else ['']
    return max(text_w(w, fs) for w in words) if words else 0.0


def wrap(s, width, fs=FS_S):
    """글줄을 폭에 맞춰 나눈다. 낱말 사이에서만 자른다.

    상자 안에 설명을 넣으려면 폭이 아니라 높이로 늘려야 한다 — 폭으로 늘리면 두 칸짜리
    줄이 판을 넘어 세로 사슬로 떨어진다.
    """
    out, cur = [], ''
    for w in s.split(' '):
        cand = (cur + ' ' + w).strip()
        if cur and text_w(cand, fs) > width:
            out.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        out.append(cur)
    return out


class Box(object):
    """놓인 상자 하나. 변 위의 점을 준다 — 좌표는 여기서만 나온다."""

    def __init__(self, x, y, w, h, label, sub='', hi=False, rc=None, subout=False,
                 fs=FS, fs_s=FS_S, wrap_label=False):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label, self.sub, self.hi = label, sub, hi
        # subout 이면 부제를 상자 **안**에 여러 줄로 깐다. 폭이 아니라 높이로 늘린다 —
        # 폭으로 늘리면 두 칸짜리 줄이 판을 넘어 세로 사슬로 떨어진다. 상자 안에 두는
        # 이유는 포함 관계다: 그 설명은 그 상자가 하는 일이다
        self.subout = subout
        # wrap_label 이면 **이름 자체**(부제가 아니라 label)를 칸 폭에 맞춰 여러 줄로
        # 접는다. 이름이 길어 칸에 못 들어갈 때 이름을 자르거나 갈래를 세로로 쌓는
        # 대신 상자를 키워 접는다 — 형제 상자(같은 부모에서 갈린 것들)가 같은 행에
        # 나란히 서야 하는데, 이름 길이 때문에 열을 줄이면 그 나란함이 깨진다
        self.wrap_label = wrap_label
        self.rc = rc                # (줄, 칸). 판을 다시 놓아도 링크를 찾아온다
        # 글자 크기는 판마다 다를 수 있다(카드 본문에 낀 판은 본문 크기로 줄인다).
        # CSS 클래스(.fl · .fl-s)는 다른 장도 같이 쓰므로 고치지 않고, 여기서만
        # 인라인 font-size 로 덮어쓴다 — weight·line-height·색은 클래스 그대로 남는다
        self.fs, self.fs_s = fs, fs_s

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
        # font-size 만 인라인으로 덮는다 — .fl/.fl-s 의 weight·line-height·색은 그대로 쓴다
        fa = ' style="font-size:%gpx"' % self.fs
        fsa = ' style="font-size:%gpx"' % self.fs_s
        if self.wrap_label:
            # 이름 자체를 칸 폭에 맞춰 접는다 — `_layout()` 이 이미 이 폭·줄 수로
            # 상자 키를 정해 뒀으니(같은 self.w·self.fs 로 다시 접는다) 여기서
            # 나온 줄 수가 거기서 셈한 줄 수와 어긋나지 않는다
            lines = wrap(self.label, self.w - 2 * PAD_X, fs=self.fs) or ['']
            extra = wrap(self.sub, self.w - 2 * PAD_X, fs=self.fs_s) if self.sub else []
            n = len(lines) + len(extra)
            y0 = self.cy - (n - 1) * LH / 2.0 + 4
            for i, ln in enumerate(lines):
                o.append('<text x="%g" y="%g" class="fl" text-anchor="middle"%s>%s</text>'
                         % (self.cx, y0 + i * LH, fa, ln))
            for j, ln in enumerate(extra):
                o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                         % (self.cx, y0 + (len(lines) + j) * LH, fsa, ln))
        elif self.sub and self.subout:
            # 줄바꿈 자리는 늘 기본 폭 계산(FS_S)과 맞춘다 — _layout() 이 상자 키를
            # 그 계산으로 이미 정했다. 여기서 작은 글자 폭으로 다시 접으면 줄 수가
            # 달라져 정해 둔 키보다 글이 넘치거나 아래가 빈다
            lines = wrap(self.sub, self.w - 2 * PAD_X)
            y = self.y + (self.h - LH) / 2.0 + LH - 12
            o.append('<text x="%g" y="%g" class="fl" text-anchor="middle"%s>%s</text>'
                     % (self.cx, y, fa, self.label))
            for i, ln in enumerate(lines):
                o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                         % (self.cx, y + 18 + i * 17, fsa, ln))
        elif self.sub:
            o.append('<text x="%g" y="%g" class="fl" text-anchor="middle"%s>%s</text>'
                     % (self.cx, self.cy - 2, fa, self.label))
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                     % (self.cx, self.cy + 13, fsa, self.sub))
        else:
            o.append('<text x="%g" y="%g" class="fl" text-anchor="middle"%s>%s</text>'
                     % (self.cx, self.cy + 4, fa, self.label))
        return o


class Plate(object):
    """판 하나. 칸을 격자로 놓고, 선은 놓인 상자에서 뽑는다."""

    def __init__(self, width=520.0, top=16.0, gap_x=GAP_X, gap_y=GAP_Y, mid='',
                 stretch=True, subout=False, pad_y=PAD_Y, bottom=14.0,
                 fs=FS, fs_s=FS_S, wrap_label=False):
        self.W = float(width)
        self.top = float(top)
        self.gap_x, self.gap_y = gap_x, gap_y
        self.mid = mid              # 열 사이 도랑에 세울 역할 라벨(흐름도 규칙 3)
        self.subout = subout        # 부제를 상자 안에 여러 줄로 깐다(폭 계산에서 뺀다)
        # 이름 자체가 칸 폭보다 길면 자르거나 옆 칸을 잡아먹는 대신 상자 안에서
        # 여러 줄로 접는다 — 형제 상자(분기·합류)를 같은 행에 나란히 세워야 할 때,
        # 열을 줄여 한 줄로 쌓으면 갈래가 사슬로 보인다(2026-09-01)
        self.wrap_label = wrap_label
        # 다른 장(회계사·메르 등)은 이 판을 기본 크기(15.2/13.5)로 쓰므로 모듈 상수는
        # 그대로 두고, 카드 본문에 낀 판만 호출하는 쪽에서 작은 크기를 넘긴다
        self.fs, self.fs_s = fs, fs_s
        # 상자 안 위아래 여백과 판 아래 여백. 받은 도식을 굽는 판은 글 사이에 끼므로
        # 좁게 준다 — 손으로 그리는 판은 기본값 그대로다
        self.pad_y = float(pad_y)
        self.bottom = float(bottom)
        # 칸을 판 끝까지 늘린다. 글자에 맞춰 재기만 하면 짧은 이름이 든 줄은 가운데
        # 조금만 차지하고 양옆이 크게 빈다 — 그 빈자리 때문에 글자가 더 작아 보인다
        self.stretch = stretch
        self.rows = []
        self.labels = {}            # 줄 왼쪽에 세우는 이름(전·후 같은 것)
        self.notes = []             # 판 아래 한 줄 설명
        self.links = []
        self.heads = []             # 열 이름
        self._placed = None

    # ---- 짓기 ------------------------------------------------------------
    def head(self, *names):
        self.heads = list(names)
        self._placed = None

    def label(self, i, text):
        """줄 왼쪽 도랑에 세우는 이름. 「전·후」처럼 줄 전체를 가리키는 말이다.

        칸 안에 넣으면 상자 하나를 이름에 쓰게 되고, 판 아래로 내리면 어느 줄 이야기인지가
        사라진다. 이름이 하나라도 있으면 왼쪽에 도랑을 내고 칸은 그만큼 오른쪽에서 시작한다."""
        self.labels[i] = text
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
        # 칸 폭·틈은 늘 기본 크기(FS·FS_S)로 잰다 — fs·fs_s 는 그려지는 글자만
        # 줄이지 칸 크기는 안 줄인다. 폭 계산까지 작은 글자로 다시 재면 원래는
        # 안 들어가던 도식이 「더 좁게 잰 폭 덕에 들어간다」는 이유만으로 판이 되어
        # 아스키로 남아야 할 넷 중 하나가 판으로 넘어간다 — 2026-08-31 에 「다이어그램
        # 1: 유휴 자산」이 그렇게 넘어갔다. 칸이 넉넉해 보여도 그 여백은 원래 더 큰
        # 글자를 위해 잡아 둔 자리라 안전하다
        ncol = max(len(r) for r in self.rows)
        ws = []
        for c in range(ncol):
            cand = [0.0]
            if c < len(self.heads):
                cand.append(text_w(self.heads[c], FS_S))
            for r in self.rows:
                if c < len(r) and r[c]:
                    if self.wrap_label:
                        # 이름 전체가 아니라 가장 긴 낱말 하나만큼만 요구한다 —
                        # 낱말 사이에서 접을 수 있으니 그 밖은 칸을 늘려 줄 수를
                        # 늘리면 된다(`wrap()`과 같은 규칙). 한 낱말이 이미 칸보다
                        # 넓으면(고유명사 등) 그건 접어도 못 줄이니 그대로 요구한다
                        cand.append(_word_w(r[c][0], FS))
                        if r[c][1]:
                            cand.append(_word_w(r[c][1], FS_S))
                    else:
                        cand.append(text_w(r[c][0]))
                        if r[c][1] and not self.subout:
                            cand.append(text_w(r[c][1], FS_S))
            ws.append(round(max(cand) + 2 * PAD_X))
        gap = max(self.gap_x, self._need_gap_x())
        if self.mid:
            gap = max(gap, text_w(self.mid, FS_S) + 16)
        total = sum(ws) + gap * (ncol - 1)
        if total > self.W:
            raise AssertionError('판(%g)보다 넓다: %g' % (self.W, total))
        gut = (max(text_w(t) for t in self.labels.values()) + 12) if self.labels else 0.0
        if self.stretch and total < self.W - gut:
            extra = (self.W - gut - total) / float(ncol)
            ws = [w + extra for w in ws]
            total = self.W - gut
        xs, x = [], gut + (self.W - gut - total) / 2.0
        for w in ws:
            xs.append(x)
            x += w + gap
        y = self.top + (20.0 if self.heads else 0.0)
        gy = max(self.gap_y, self._need_gap_y())
        placed = []
        for r in self.rows:
            if self.wrap_label:
                # 이름을 접은 줄 수(+부제 한 묶음) 만큼 키를 키운다. `svg()` 가
                # 그릴 때도 같은 폭(ws[c])·글자 크기(self.fs)로 다시 접으므로
                # 여기서 셈한 줄 수와 어긋나지 않는다
                deep = 1
                for c in range(ncol):
                    cell = r[c] if c < len(r) else None
                    if not cell:
                        continue
                    n = len(wrap(cell[0], ws[c] - 2 * PAD_X, fs=self.fs)) or 1
                    if cell[1]:
                        n += len(wrap(cell[1], ws[c] - 2 * PAD_X, fs=self.fs_s)) or 1
                    deep = max(deep, n)
                h = self.pad_y * 2 + LH * deep
            else:
                two = any(c and c[1] for c in r) and not self.subout
                h = self.pad_y * 2 + LH + (LH if two else 0)
                if self.subout:
                    # 상자 안에 깐 설명 줄만큼 키를 키운다. 열 폭이 이미 정해져 있어
                    # 몇 줄이 될지 여기서 셀 수 있다
                    deep = 0
                    for c in range(ncol):
                        cell = r[c] if c < len(r) else None
                        if cell and cell[1]:
                            deep = max(deep, len(wrap(cell[1], ws[c] - 2 * PAD_X)))
                    h += 17 * deep + (6 if deep else 0)
            below = 0.0
            line = []
            # 한 칸만 든 줄은 판을 가로질러 세운다. 안 그러면 그 줄만 반쪽에 몰려
            # 오른쪽이 통째로 비고, 빈자리 때문에 글자가 더 작아 보인다
            filled = [c for c in range(ncol) if c < len(r) and r[c]]
            wide = len(filled) == 1 and ncol > 1
            for c in range(ncol):
                cell = r[c] if c < len(r) else None
                if not cell:
                    line.append(None)
                    continue
                bx, bw = (xs[0], xs[-1] + ws[-1] - xs[0]) if wide else (xs[c], ws[c])
                line.append(Box(bx, y, bw, h, cell[0], cell[1], cell[2],
                                (len(placed), c), self.subout,
                                fs=self.fs, fs_s=self.fs_s, wrap_label=self.wrap_label))
            placed.append(line)
            y += h + below + gy
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
        for (ra, _ca), (rb, _cb), label, _k, _at in self.links:
            if label and ra == rb:
                need = max(need, text_w(label, FS_S) + 10)
        return need

    def _need_gap_y(self):
        """줄과 줄 사이를 세로로 잇는 선의 이름이 앉을 띠."""
        return 30.0 if any(ra != rb and label
                           for (ra, _ca), (rb, _cb), label, _k, _at in self.links) else 0.0

    def at(self, row, col):
        placed = self._layout()
        b = placed[row][col]
        if b is None:
            raise IndexError('빈 칸 (%d,%d)' % (row, col))
        return b

    # ---- 잇기 ------------------------------------------------------------
    def connect(self, a, b, label='', kind='l', at=0.5):
        """두 상자를 잇는다. 어느 변에서 나가고 들어올지는 자리가 정한다.

        kind: 'l' 회색 실선(물건·용역) · 'a' 강조색 실선(돈) · 'd' 점선(조건부)
        at: 위아래로 잇는 선이 상자 변의 어디에 붙을지(0~1, 기본 가운데).
            한 칸으로 쌓은 판에서 한 상자를 건너뛰는 이음은 가운데로 그으면
            사이 상자를 정통으로 뚫고 지나가 다른 이음과 겹쳐 안 보인다 —
            가장자리로 붙여야 「그 상자를 지나쳐 간다」는 게 보인다
        """
        self.links.append((a.rc, b.rc, label, kind, at))
        self._placed = None         # 틈이 이름에 따라 달라진다. 다시 놓는다

    def _link_svg(self, a, b, label, kind, at=0.5):
        cls = {'l': 'fl-l', 'a': 'fl-a', 'd': 'fl-d'}[kind]
        mk = 'url(#flAa)' if kind == 'a' else 'url(#flA)'
        fsa = ' style="font-size:%gpx"' % self.fs_s
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
            p0 = a.port('b' if down else 't', at)
            p1 = b.port('t' if down else 'b', at)
            if abs(p0[0] - p1[0]) < 1.0:
                d = 'M%g %g L%g %g' % (p0[0], p0[1], p1[0], p1[1])
                my = (p0[1] + p1[1]) / 2.0
                lx, ly, anchor = p0[0] + 9, my + 4, 'start'
            else:
                # 꺾이는 자리를 가운데가 아니라 **나가는 쪽에 붙여** 잡는다. 가운데면
                # 틈이 반씩 나뉘어 받는 쪽 토막이 촉(8px)에 거의 다 먹힌다 —
                # 화살표가 촉만 남아 보인다(2026-09-01). 35% 자리면 받는 쪽이 길다
                # 35% 자리는 줄을 건너뛰는 이음에서 **사이 줄 안**에 떨어진다 —
                # 그러면 가로 토막이 남의 상자를 정통으로 지난다(2026-09-01,
                # 할라페뇨 밸류체인). 나가는 상자 바로 아래 도랑 안으로 묶는다
                span = p1[1] - p0[1]
                my = p0[1] + (span * 0.35 if abs(span) < 60 else
                              (17.0 if span > 0 else -17.0))
                d = 'M%g %g L%g %g L%g %g L%g %g' % (
                    p0[0], p0[1], p0[0], my, p1[0], my, p1[0], p1[1])
                # 꺾여 내려가는 이음은 이름을 가로로 꺾인 구간의 **한가운데**에 둔다.
                # 한쪽 끝 좌표로만 잡으면 그 끝을 나눠 쓰는 이음끼리 이름이 같은 점에
                # 포개진다 — 나가는 쪽으로 잡으면 한 상자에서 갈래가 둘 나갈 때
                # (「판다」·「안 판다」), 받는 쪽으로 잡으면 셋이 한 상자로 모일 때
                # (「결과 취합」 셋) 겹쳤다. 두 끝의 가운데는 어느 쪽을 나눠 쓰든
                # 갈린다 (2026-09-01)
                lx, ly, anchor = (p0[0] + p1[0]) / 2.0, my - 4, 'middle'
        o = ['<path d="%s" class="%s" marker-end="%s"/>' % (d, cls, mk)]
        if label:
            # 이미 이름이 앉은 점이면 한 줄씩 올려 비킨다. 계산으로 갈리지 않는 경우가
            # 남는다 — 고리가 있는 판에서 두 이음의 꺾인 구간 가운데가 같은 점이 된다
            # (2026-09-01, 「작업 분배」와 「다음 작업 투입」이 한 자리에 겹쳤다)
            pts = getattr(self, '_label_pts', None)
            if pts is not None:
                while (round(lx), round(ly)) in pts:
                    ly -= 13.0
                pts.add((round(lx), round(ly)))
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="%s"%s>%s</text>'
                     % (lx, ly, anchor, fsa, label))
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
        fa = ' style="font-size:%gpx"' % self.fs
        fsa = ' style="font-size:%gpx"' % self.fs_s
        if self.heads:
            for c, name in enumerate(self.heads):
                o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                         % (self._xs[c] + self._ws[c] / 2.0, self.top + 4, fsa, name))
        for i, line in enumerate(placed):
            for b in line:
                if b:
                    o += b.svg()
            if i in self.labels:
                first = next(b for b in line if b)
                o.append('<text x="0" y="%g" class="fl"%s>%s</text>'
                         % (first.cy + 5, fa, self.labels[i]))
        if self.mid and len(self._xs) > 1:
            gx = (self._xs[0] + self._ws[0] + self._xs[1]) / 2.0
            o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                     % (gx, self.top + (20.0 if self.heads else 0.0) - 6, fsa, self.mid))
        # 이음 이름이 앉은 자리. 꺾인 구간의 가운데로 잡아도 고리(사이클)가 있는 판에서는
        # 두 이음의 가운데가 같은 점이 되는 일이 있다 — 먼저 앉은 이름을 비켜 준다
        self._label_pts = set()
        for (ra, ca), (rb, cb), label, kind, at in self.links:
            o += self._link_svg(placed[ra][ca], placed[rb][cb], label, kind, at)
        y = self._bottom
        for n in self.notes:
            # 각주도 판 폭에 맞춰 나눈다. 한 줄로 두면 긴 한 줄 평이 판 밖으로 나가거나,
            # 잘라 담으면 뒷말이 사라진다 — 2026-08-31 에 「…이득이다!」가 그렇게 없어졌다
            for ln in wrap(n, self.W - 8):
                y += 18
                o.append('<text x="%g" y="%g" class="fl fl-s" text-anchor="middle"%s>%s</text>'
                         % (self.W / 2.0, y, fsa, ln))
        h = y + self.bottom
        return ('<svg viewBox="0 0 %g %g" width="100%%" data-fig-layout="1" role="img" '
                'aria-label="%s">%s%s</svg>' % (self.W, h, alt, self.DEFS, ''.join(o)))
