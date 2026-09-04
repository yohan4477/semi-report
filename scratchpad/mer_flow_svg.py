# -*- coding: utf-8 -*-
"""흐름도를 인라인 SVG로 그린다. 두 겹 모두 이 파일에서 나온다.

  inter_svg  통합 흐름도 — 가로는 날짜, 세로는 레인. lift 마디만 선다.
             편을 가로지르는 화살표는 그 편의 lift 마디로 접어서 붙인다.
  intra_svg  글 한 편의 개념도 — 사슬을 따라 층을 매기고 depth 2 세부 단계까지 편다.

**선이 겹치지 않게 배선한다.** 곡선을 아무 데나 그으면 마디 위를 지나고 선끼리 포갠다.
그래서 직교 배선으로 간다 — 가로줄은 줄 사이 복도(corridor), 세로줄은 열 사이 홈(gutter)에
넣고, 같은 복도·홈에서 구간이 겹치면 다른 채널을 준다(구간 그래프 그리디 배정). 배정이
끝나면 어떤 두 선도 같은 직선 위에서 포개지지 않는다.

색은 CSS 변수로 받는다(카드 도해와 같은 규칙). 없는 값을 그리지 않는다 — 마디는 전부
mer_flow_lib.check()를 통과한 것만 들어온다.
"""
import collections
import html as H
import re

ROLE_ORDER = ['bg', 'event', 'mech', 'risk', 'watch', 'verdict']
ROLE_KO = {'bg': '배경', 'event': '사건', 'mech': '메커니즘', 'risk': '부작용',
           'watch': '관전포인트', 'verdict': '한줄 코멘트'}

CSS = '''
  .merflow{margin:14px 0;border:1px solid var(--line);border-radius:12px;
           background:var(--fig-bg,rgba(127,127,127,.05));padding:12px 12px 8px}
  .merflow-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .merflow svg{display:block;height:auto}
  .merflow .mf-lane{fill:var(--ink-3);font-size:11px;font-weight:800}
  .merflow .mf-lane-bg{fill:var(--sunk,rgba(127,127,127,.06))}
  .merflow .mf-date{fill:var(--ink-3);font-size:10.5px;font-weight:700}
  .merflow .mf-grid{stroke:var(--line);stroke-width:1;stroke-dasharray:2 4}
  .merflow .mf-box{fill:var(--card,var(--surface,#fff));stroke:var(--line);stroke-width:1.2}
  .merflow .mf-box.ev{stroke:var(--ink-3);stroke-width:1.6}
  .merflow .mf-box.vd{fill:var(--accent-soft,rgba(127,127,127,.10));stroke:var(--ink-3)}
  .merflow .mf-box.wt{stroke-dasharray:4 3}
  .merflow .mf-box.rk{stroke:var(--risk,#c2504a)}
  .merflow .mf-box.d2{stroke-width:1;opacity:.94}
  .merflow .mf-t{fill:var(--ink-2);font-size:11.5px;font-weight:650}
  .merflow .mf-t.sm{fill:var(--ink-2);font-size:10.5px;font-weight:600}
  .merflow .mf-r{fill:var(--ink);font-size:11.5px;font-weight:850}
  .merflow .mf-r.sm{font-size:11px}
  .merflow .mf-a{fill:none;stroke:var(--ink-3);stroke-width:1.4;stroke-linejoin:round;
                 marker-end:url(#mf-ar)}
  .merflow .mf-a.up{stroke-dasharray:5 3}
  .merflow .mf-a.ct{stroke:var(--risk,#c2504a);stroke-dasharray:2 3}
  .merflow .mf-elab{fill:var(--ink-3);font-size:9.5px;font-weight:600}
  .merflow .mf-elab-bg{fill:var(--fig-bg,rgba(127,127,127,.05));stroke:none;opacity:.92}
  .merflow figcaption{margin:8px 2px 0;font-size:.78rem;line-height:1.55;color:var(--ink-3)}
  .merflow .mf-key{margin:0 0 8px;font-size:10.5px;color:var(--ink-3);display:flex;
                   gap:12px;flex-wrap:wrap;font-weight:700}
'''

ARROW_DEF = ('<defs><marker id="mf-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             'markerHeight="6" orient="auto-start-reverse">'
             '<path d="M0,0 L10,5 L0,10 z" fill="var(--ink-3)"/></marker></defs>')

BOX_CLS = {'event': 'ev', 'bg': '', 'mech': '', 'risk': 'rk', 'watch': 'wt', 'verdict': 'vd'}


def esc(s):
    return H.escape(s or '', quote=True)


def cw(ch, fs):
    """글자 하나의 폭. 한글·한자·가나는 글씨 크기만큼, 나머지는 그 55%로 본다."""
    o = ord(ch)
    wide = 0x1100 <= o <= 0x11FF or 0x3000 <= o <= 0x9FFF or 0xAC00 <= o <= 0xD7A3
    return fs * (1.0 if wide else 0.55)


def measure(s, fs):
    return sum(cw(c, fs) for c in s)


def wrap(text, fs, maxw):
    """상자 폭에 맞춰 줄을 나눈다. 글자 수가 아니라 실제 폭으로 재야 글자가 안 삐져나온다.
    띄어쓰기가 있으면 거기서 끊고, 한 낱말이 너무 길면 글자 단위로 끊는다."""
    lines, line = [], ''
    for word in re.split(r'(\s+)', text):
        if not word:
            continue
        if measure(line + word, fs) <= maxw:
            line += word
            continue
        if line.strip():
            lines.append(line.strip())
            line = ''
        while measure(word, fs) > maxw:
            k = 1
            while k < len(word) and measure(word[:k + 1], fs) <= maxw:
                k += 1
            lines.append(word[:k])
            word = word[k:]
        line = word
    if line.strip():
        lines.append(line.strip())
    return lines


# ── 채널 배정 ────────────────────────────────────────────────────────────────
class Channels(object):
    """한 복도(또는 홈)에 구간을 넣는다. 겹치는 구간은 다른 채널로 밀어낸다."""

    def __init__(self):
        self.tracks = []          # [[(a, b), …], …]

    def put(self, a, b):
        a, b = (a, b) if a <= b else (b, a)
        a, b = a - 6, b + 6       # 끝점이 스치기만 해도 갈라 놓는다
        for i, tr in enumerate(self.tracks):
            if all(b <= x or a >= y for x, y in tr):
                tr.append((a, b))
                return i
        self.tracks.append([(a, b)])
        return len(self.tracks) - 1

    def __len__(self):
        return len(self.tracks)


def _box(x, y, w, h, n, sub='', small=False):
    """상자 하나. 머리에 주체, 그 아래 무엇을 했나가 온다.

    「미 재무부 / 바이백 두 배」처럼 읽혀야 사슬이 「누가 무엇을 해서 누구에게 뭐가 갔나」로
    이어진다. 주체를 어깨에 작게 달면 눈이 행동만 좇아 주어가 사라진다."""
    cls = BOX_CLS.get(n.get('role'), '')
    if n.get('depth', 1) >= 2:
        cls += ' d2'
    fs = 10.5 if small else 11.5
    tcls = 'mf-t sm' if small else 'mf-t'
    hcls = 'mf-r sm' if small else 'mf-r'
    hfs = 11.0 if small else 11.5
    lh = 13 if small else 14
    pad = 9
    lines = wrap(n['label'], fs, w - pad * 2 - 2)
    head = 17 if sub else 0
    cap = max(1, int((h - head - 6) // lh))
    if len(lines) > cap:
        lines = lines[:cap]
        while lines and measure(lines[-1] + '…', fs) > w - pad * 2 - 2:
            lines[-1] = lines[-1][:-1]
        lines[-1] += '…'
    body_h = len(lines) * lh
    ty = y + head + (h - head - body_h) / 2 + lh * 0.74
    parts = ['<rect class="mf-box %s" x="%d" y="%d" width="%d" height="%d" rx="7"/>'
             % (cls, x, y, w, h)]
    if sub:
        who = sub
        while measure(who, hfs) > w - pad * 2 - 2 and len(who) > 4:
            who = who[:-1]
        parts.append('<text class="%s" x="%d" y="%d">%s</text>'
                     % (hcls, x + pad, y + 16, esc(who)))
    for i, ln in enumerate(lines):
        parts.append('<text class="%s" x="%d" y="%d">%s</text>'
                     % (tcls, x + pad, ty + i * lh, esc(ln)))
    return ''.join(parts)


def _poly(pts, kind):
    cls = {'update': ' up', 'contradict': ' ct'}.get(kind, '')
    d = 'M%d,%d ' % pts[0] + ' '.join('L%d,%d' % p for p in pts[1:])
    return '<path class="mf-a%s" d="%s"/>' % (cls, d)


def _clean(pts):
    """같은 점과 같은 방향으로 이어지는 점을 접는다.

    격자에 스냅하고 나면 한 칸 내려갔다 다시 올라오는 토막이 생긴다. 눈에는 선이 겹쳐
    보이고 검사기에도 걸린다. 세 점이 한 직선 위에 있으면 가운데를 버린다."""
    out = [pts[0]]
    for p in pts[1:]:
        if (round(p[0], 1), round(p[1], 1)) != (round(out[-1][0], 1), round(out[-1][1], 1)):
            out.append(p)
    i = 1
    while i < len(out) - 1:
        a, b, c = out[i - 1], out[i], out[i + 1]
        if (abs(a[0] - b[0]) < 1.5 and abs(b[0] - c[0]) < 1.5) or            (abs(a[1] - b[1]) < 1.5 and abs(b[1] - c[1]) < 1.5):
            del out[i]
            i = max(1, i - 1)
        else:
            i += 1
    return out


def _segs(pts):
    return list(zip(pts, pts[1:]))


def _hits_box(pts, bxs, skip, strict=False, pad=0):
    """선이 카드 속을 지나나.

    strict면 출발·도착 카드도 봐준다 — 예외를 두면 위아래로 나란한 두 카드를 잇는 선이
    두 카드 몸통을 관통해 버린다. 대신 면에 붙는 짧은 토막은 안쪽 4px을 비워 통과시킨다.

    pad를 주면 카드 둘레에 그만큼 빈 띠를 둔다 — 선이 모서리를 스치면 카드에 붙어 보인다.
    붙는 자리의 첫·마지막 토막은 제 카드에 한해 이 띠를 지키지 않아도 된다."""
    segs = _segs(pts)
    for si, (a, b) in enumerate(segs):
        edge = si in (0, len(segs) - 1)        # 붙는 자리의 꼭지
        lo_x, hi_x = sorted((a[0], b[0]))
        lo_y, hi_y = sorted((a[1], b[1]))
        # 가로·세로 선분은 한쪽 두께가 0이라 그대로 재면 어떤 상자와도 안 겹치는 것으로 나온다.
        # 얇은 띠로 부풀려서 잰다 — 이걸 빠뜨려 가로선이 카드를 뚫고 지나갔다.
        if hi_y - lo_y < 1.5:
            lo_y, hi_y = lo_y - 1.5, hi_y + 1.5
        if hi_x - lo_x < 1.5:
            lo_x, hi_x = lo_x - 1.5, hi_x + 1.5
        for k, (x0, y0, w, h) in bxs.items():
            x1, y1 = x0 + w, y0 + h
            if strict:
                m = -4 if (pad and edge and k in skip) else pad
                if (min(hi_x, x1 + m) - max(lo_x, x0 - m) > 1
                        and min(hi_y, y1 + m) - max(lo_y, y0 - m) > 1):
                    return True
                continue
            if k in skip:
                continue
            if (min(hi_x, x1 + 3) - max(lo_x, x0 - 3) > 1
                    and min(hi_y, y1 + 3) - max(lo_y, y0 - 3) > 1):
                return True
    return False


def _hits_line(pts, drawn, sep=2.5):
    """이미 그은 선과 부딪히나. sep는 나란한 선이 지켜야 할 최소 간격이다 —
    2~3px만 띄우면 눈에는 겹쳐 보인다. 격자 간격만큼 벌려야 따로 보인다."""
    for a, b in _segs(pts):
        horiz = abs(a[1] - b[1]) < 1.5
        lo, hi = sorted((a[0], b[0]) if horiz else (a[1], b[1]))
        fix = a[1] if horiz else a[0]
        for c, d in drawn:
            if (abs(c[1] - d[1]) < 1.5) != horiz:
                continue
            f2 = c[1] if horiz else c[0]
            if abs(fix - f2) >= sep:
                continue
            l2, h2 = sorted((c[0], d[0]) if horiz else (c[1], d[1]))
            if min(hi, h2) - max(lo, l2) > 2:
                return True
    return False


def _out(p, box, d=16):
    """면이 향한 쪽으로 한 발 빠져나온 점. 왼쪽 면에서 나가면서 오른쪽으로 뻗으면
    제 카드 안으로 들어가 어떤 길도 못 찾는다."""
    x, y, w, h = box
    if abs(p[0] - x) <= 4:
        return (p[0] - d, p[1])
    if abs(p[0] - (x + w)) <= 4:
        return (p[0] + d, p[1])
    if abs(p[1] - y) <= 4:
        return (p[0], p[1] - d)
    return (p[0], p[1] + d)


def _candidates(p1, p2, corr_ys, gut_xs=(), dst=None, src=None, pad=0):
    """짧은 길부터 내놓는다. 곧은 선 → 두 번 꺾기 → 복도로 돌아가기 순서다.

    dst(목표 상자)를 주면 왼쪽 면이 다 찼을 때 위·아래에서 꽂는 길도 낸다. 진입 방향이
    하나뿐이면 그 자리가 이미 찬 순간 어떤 길도 못 들어간다."""
    (x1, y1), (x2, y2) = p1, p2
    if abs(y1 - y2) < 1.5 or abs(x1 - x2) < 1.5:
        yield [(x1, y1), (x2, y2)]
    # 한 번만 꺾는 길(ㄴ자)을 먼저 낸다 — 두 번 꺾는 길보다 늘 낫다
    yield [(x1, y1), (x2, y1), (x2, y2)]
    yield [(x1, y1), (x1, y2), (x2, y2)]
    for k in range(7):                       # 나오자마자 꺾기
        gx = x1 + 14 + k * 7
        if gx < x2 - 8:
            yield [(x1, y1), (gx, y1), (gx, y2), (x2, y2)]
    for k in range(7):                       # 목표 앞에서 꺾기
        gx = x2 - 16 - k * 7
        if gx > x1 + 8:
            yield [(x1, y1), (gx, y1), (gx, y2), (x2, y2)]
    for k in range(1, 12):                   # 중간에서 한 번 더 꺾기(계단)
        for sgn in (1, -1):
            my = (y1 + y2) / 2 + sgn * k * 6
            gx, gx2 = x1 + 14, x2 - 16
            if gx < gx2:
                yield [(x1, y1), (gx, y1), (gx, my), (gx2, my), (gx2, y2), (x2, y2)]
    for gx0 in gut_xs:                       # 열 경계 홈에서 꺾기
        for k in range(6):
            gx = gx0 + k * 7
            if x1 + 8 < gx < x2 - 8:
                yield [(x1, y1), (gx, y1), (gx, y2), (x2, y2)]
    # 촘촘히 훑기 — 정해 둔 자리가 다 차면 4px 간격으로 빈틈을 찾는다
    for gx in range(int(x1) + 12, max(int(x2) - 10, int(x1) + 13), 4):
        yield [(x1, y1), (gx, y1), (gx, y2), (x2, y2)]
    lo, hi = sorted((y1, y2))
    for my in range(int(lo) - 60, int(hi) + 61, 4):
        gx, gx2 = x1 + 14, x2 - 16
        if gx < gx2:
            yield [(x1, y1), (gx, y1), (gx, my), (gx2, my), (gx2, y2), (x2, y2)]
    if src and dst:
        d = max(16, pad + 4)      # 빠져나오는 거리는 빈 띠보다 넉넉해야 제 카드에 안 걸린다
        e1, e2 = _out(p1, src, d), _out(p2, dst, d)
        for cy in sorted(corr_ys, key=lambda c: abs(c - y1)):
            yield [(x1, y1), e1, (e1[0], cy), (e2[0], cy), e2, (x2, y2)]
        for gx in sorted({e1[0], e2[0]} | set(gut_xs)):
            yield [(x1, y1), e1, (e1[0], e2[1]), e2, (x2, y2)]
            yield [(x1, y1), e1, (gx, e1[1]), (gx, e2[1]), e2, (x2, y2)]
    if dst:                                  # 왼쪽 면이 다 찼으면 위·아래로 꽂는다
        dx0, dy0, dx1, dy1 = dst[0], dst[1], dst[0] + dst[2], dst[1] + dst[3]
        for f in (0.35, 0.5, 0.65):
            xc = dx0 + (dx1 - dx0) * f
            for k in range(1, 14):
                for my, ey in ((dy0 - 8 - k * 5, dy0 - 3), (dy1 + 8 + k * 5, dy1 + 3)):
                    gx = x1 + 12
                    yield [(x1, y1), (gx, y1), (gx, my), (xc, my), (xc, ey)]
    if src and dst:                          # 나가는 자리도 위·아래로 연다
        sx0, sy0, sx1, sy1 = src[0], src[1], src[0] + src[2], src[1] + src[3]
        dx0, dy0, dx1, dy1 = dst[0], dst[1], dst[0] + dst[2], dst[1] + dst[3]
        for fs_ in (0.4, 0.6):
            xs = sx0 + (sx1 - sx0) * fs_
            for fd in (0.4, 0.6):
                xd = dx0 + (dx1 - dx0) * fd
                for k in range(1, 12):
                    yield [(xs, sy1), (xs, sy1 + 8 + k * 5), (xd, sy1 + 8 + k * 5), (xd, dy0 - 3)]
                    yield [(xs, sy0), (xs, sy0 - 8 - k * 5), (xd, sy0 - 8 - k * 5), (xd, dy1 + 3)]
    if src and dst and corr_ys:
        # 마지막 훑기 — 정해 둔 복도가 다 차면 6px 간격으로 빈 가로 통로를 찾는다.
        # 여기까지 못 찾으면 검사 안 된 예비 길이 나가 선이 겹친다.
        lo_c, hi_c = min(corr_ys) - 60, max(corr_ys) + 60
        d = max(16, pad + 4)
        e1, e2 = _out(p1, src, d), _out(p2, dst, d)
        cy = lo_c
        while cy <= hi_c:
            yield [(x1, y1), e1, (e1[0], cy), (e2[0], cy), e2, (x2, y2)]
            cy += 6
    # 목표가 왼쪽이거나 같은 열이면 앞의 길이 다 막힌다 — 복도로 나갔다 되돌아온다
    for cy in sorted(corr_ys, key=lambda c: abs(c - y1)):
        for k in range(10):
            gx = x1 + 12 + k * 7
            ax = x2 - 18 - k * 7
            yield [(x1, y1), (gx, y1), (gx, cy), (ax, cy), (ax, y2), (x2, y2)]


def route_all(items, bxs, corr_ys, gut_xs=(), sep=2.5, grid=0, strict=False, tries=2600,
              pad=0, prefer_ys=(), prefer_xs=()):
    """선을 하나씩 놓되 짧은 것부터 자리를 잡는다.

    items = [(from_key, to_key, kind, (x1,y1), (x2,y2)), …]
    통과하는 첫 후보를 쓰지 않는다 — 여러 후보를 모아 **꺾임이 적은 것**을 고르고, 같으면
    **카드 사이 한가운데 길**에 가까운 것, 그다음 짧은 것을 고른다. 꺾임 하나가 눈에는
    사슬이 한 번 끊기는 것으로 읽히고, 카드에 붙어 도는 선은 그 카드의 것처럼 보인다."""
    def bends(pts):
        n = 0
        for i in range(1, len(pts) - 1):
            a, b, c = pts[i - 1], pts[i], pts[i + 1]
            if (abs(a[0] - b[0]) < 1.5) != (abs(b[0] - c[0]) < 1.5):
                n += 1
        return n

    def length(pts):
        return sum(abs(b[0] - a[0]) + abs(b[1] - a[1]) for a, b in _segs(pts))

    def off_center(pts):
        """긴 토막이 카드 사이 한가운데 길에서 얼마나 벗어났나. 짧은 꼭지는 안 센다."""
        worst = 0
        for a, b in _segs(pts):
            dx, dy = abs(b[0] - a[0]), abs(b[1] - a[1])
            if dx + dy < 40:
                continue
            if dy < 1.5 and prefer_ys:
                worst = max(worst, min(abs(a[1] - c) for c in prefer_ys))
            elif dx < 1.5 and prefer_xs:
                worst = max(worst, min(abs(a[0] - c) for c in prefer_xs))
        return int(worst // 8)

    drawn, out = [], []
    order = sorted(range(len(items)),
                   key=lambda i: abs(items[i][3][0] - items[i][4][0])
                   + abs(items[i][3][1] - items[i][4][1]))
    for i in order:
        a, b, kind, p1, p2 = items[i]
        best, seen = None, 0
        for cand in _candidates(p1, p2, corr_ys, gut_xs, bxs.get(b), bxs.get(a), pad):
            seen += 1
            # 후보를 다 보진 않는다. 다만 아직 쓸 길을 못 찾았으면 계속 찾는다 —
            # 여기서 끊으면 검사 안 된 예비 길이 나가 선이 겹친다
            if seen > tries and best is not None:
                break
            pts = _clean(cand)
            if grid:
                pts = _clean([(round(px / grid) * grid if j not in (0, len(pts) - 1) else px,
                               round(py / grid) * grid if j not in (0, len(pts) - 1) else py)
                              for j, (px, py) in enumerate(pts)])
            if _hits_box(pts, bxs, {a, b}, strict, pad) or _hits_line(pts, drawn, sep):
                continue
            score = (bends(pts), off_center(pts), length(pts))
            if best is None or score < best[0]:
                best = (score, pts)
            if score[0] == 0 and score[1] == 0:  # 곧고 한가운데면 더 볼 것이 없다
                break
        # 하나도 못 찾으면 **덜 나쁜 것**을 고른다. 예비 경로를 그냥 쓰면 검사도 안 거친
        # 선이 나가 다른 선과 통째로 겹친다.
        if best is None:
            worst = None
            for cand in _candidates(p1, p2, corr_ys, gut_xs, bxs.get(b), bxs.get(a), pad):
                pts = _clean(cand)
                bad = (1 if _hits_box(pts, bxs, {a, b}, strict, pad) else 0) * 100
                bad += 10 if _hits_line(pts, drawn, sep) else 0
                sc = (bad, bends(pts), off_center(pts), length(pts))
                if worst is None or sc < worst[0]:
                    worst = (sc, pts)
                if bad == 0:
                    break
            best = worst
        pick = best[1] if best else _clean([(p1[0], p1[1]), (p1[0] + 14, p1[1]),
                                            (p1[0] + 14, p2[1]), (p2[0], p2[1])])
        drawn += _segs(pick)
        out.append((i, pick, kind))
    out.sort()
    return [(p, k) for _, p, k in out]


def _fan(edge_list):
    """마디마다 나가는 선·들어오는 선에 번호를 매긴다(면에 붙는 자리를 가르려고)."""
    outs, ins = collections.defaultdict(list), collections.defaultdict(list)
    for i, (a, b) in enumerate(edge_list):
        outs[a].append(i)
        ins[b].append(i)
    ok, on, ik, ino = {}, {}, {}, {}
    for a, idxs in outs.items():
        for k, i in enumerate(idxs):
            ok[i], on[i] = k, len(idxs)
    for b, idxs in ins.items():
        for k, i in enumerate(idxs):
            ik[i], ino[i] = k, len(idxs)
    return ok, on, ik, ino


# ── 통합 흐름도 ──────────────────────────────────────────────────────────────
def inter_svg(nodes, edges, lanes, caption=''):
    by_id = {n['id']: n for n in nodes}
    lift = [n for n in nodes if n.get('lift')]
    if not lift:
        return ''
    rep = {}
    for n in lift:
        rep.setdefault(n['src'], n['id'])

    def fold(nid):
        n = by_id.get(nid)
        return rep.get(n['src']) if n else None

    seen, folded = set(), []
    for e in edges:
        a, b = fold(e['from']), fold(e['to'])
        if not a or not b or a == b or (a, b) in seen:
            continue
        seen.add((a, b))
        folded.append((a, b, e['kind']))

    dates = sorted({n['date'] for n in lift})
    used = [l for l in lanes if any(n['lane'] == l[0] for n in lift)]
    row = {l[0]: i for i, l in enumerate(used)}

    L, COLW, BW, BH, VGAP = 118, 196, 150, 54, 20
    # 레인 높이는 그 레인에서 한 날짜에 겹쳐 서는 마디 수로 정한다
    stack = collections.Counter((n['lane'], n['date']) for n in lift)
    rows_of = {l[0]: max([stack[(l[0], d)] for d in dates] or [1]) for l in used}
    CORR = 26                                   # 레인 사이 복도 높이(채널이 여기 들어간다)
    rowh = {l[0]: rows_of[l[0]] * (BH + VGAP) + CORR for l in used}

    top = {}
    y = 34
    for l in used:
        top[l[0]] = y
        y += rowh[l[0]]
    Hh = y + 16
    W = L + COLW * len(dates) + 40

    pos = {}
    for n in lift:
        peers = [m for m in lift if m['date'] == n['date'] and m['lane'] == n['lane']]
        k = peers.index(n)
        x = L + COLW * dates.index(n['date']) + 8
        yy = top[n['lane']] + CORR + k * (BH + VGAP)
        pos[n['id']] = (x, yy, BW, BH)

    ok, on, ik, ino = _fan([(a, b) for a, b, _ in folded])
    items = []
    for i, (a, b, kind) in enumerate(folded):
        sa, sb = pos[a], pos[b]
        p1 = (sa[0] + sa[2], sa[1] + sa[3] * (ok[i] + 1.0) / (on[i] + 1.0))
        p2 = (sb[0] - 3, sb[1] + sb[3] * (ik[i] + 1.0) / (ino[i] + 1.0))
        items.append((a, b, kind, p1, p2))
    corr_ys = ([top[l[0]] + 6 + k * 7 for l in used for k in range(3)]
               + [top[l[0]] + rowh[l[0]] - 8 - k * 7 for l in used for k in range(3)])
    gut_xs = [L + COLW * (c + 1) - 40 + k * 8 for c in range(len(dates)) for k in range(-3, 5)]
    routes = route_all(items, pos, corr_ys, gut_xs, sep=8)

    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img">' % (W, Hh, W), ARROW_DEF]
    for i, (lid, name) in enumerate(used):
        if i % 2 == 0:
            s.append('<rect class="mf-lane-bg" x="0" y="%d" width="%d" height="%d" rx="6"/>'
                     % (top[lid], W, rowh[lid]))
        s.append('<text class="mf-lane" x="10" y="%d">%s</text>'
                 % (top[lid] + rowh[lid] / 2, esc(name)))
    for i, d in enumerate(dates):
        x = L + COLW * i
        s.append('<line class="mf-grid" x1="%d" y1="28" x2="%d" y2="%d"/>' % (x, x, Hh - 10))
        s.append('<text class="mf-date" x="%d" y="20">%s</text>'
                 % (x + 8, d[5:].replace('-', '/')))
    for pts, kind in routes:
        s.append(_poly(pts, kind))
    for n in lift:
        x, yy, w, h = pos[n['id']]
        s.append(_box(x, yy, w, h, n, n.get('actor', '')))
    s.append('</svg>')
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    key = ('<div class="mf-key"><span>─ 낳는다</span><span>--- 앞 판단을 고친다(A/S)</span>'
           '<span style="color:var(--risk,#c2504a)">··· 어긋난다</span></div>')
    return ('<figure class="merflow">%s<div class="merflow-scroll">%s</div>%s</figure>'
            % (key, ''.join(s), cap))


# ── 글 한 편의 개념도 ────────────────────────────────────────────────────────
def _rank(ids, edges):
    """사슬을 따라 층을 매긴다(가장 긴 경로). 순환이 없으니 반복으로 굳는다."""
    rank = {i: 0 for i in ids}
    for _ in range(len(ids) + 1):
        moved = False
        for e in edges:
            a, b = e['from'], e['to']
            if a in rank and b in rank and rank[b] < rank[a] + 1:
                rank[b] = rank[a] + 1
                moved = True
        if not moved:
            break
    return rank


def _order(layers, edges):
    """층 안 차례를 이웃의 평균 자리로 몇 번 흔들어 선 교차를 줄인다."""
    pos = {}
    for l, ns in layers.items():
        for i, n in enumerate(ns):
            pos[n] = i
    pred = collections.defaultdict(list)
    succ = collections.defaultdict(list)
    for e in edges:
        if e['from'] in pos and e['to'] in pos:
            pred[e['to']].append(e['from'])
            succ[e['from']].append(e['to'])
    for it in range(6):
        keys = sorted(layers) if it % 2 == 0 else sorted(layers, reverse=True)
        for l in keys:
            ref = pred if it % 2 == 0 else succ
            def bary(n):
                v = [pos[m] for m in ref[n] if m in pos]
                return sum(v) / len(v) if v else pos[n]
            layers[l].sort(key=bary)
            for i, n in enumerate(layers[l]):
                pos[n] = i
    return pos


def intra_svg(nodes, edges, src, caption=''):
    mine = [n for n in nodes if n['src'] == src]
    if not mine:
        return ''
    by_id = {n['id']: n for n in mine}
    ids = set(by_id)
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]

    rank = _rank(ids, mye)
    # 층을 매길 수 없는(화살표가 안 닿는) 마디는 역할 차례로 뒤에 세운다
    loose = [i for i in ids if rank[i] == 0 and not any(e['to'] == i for e in mye)
             and not any(e['from'] == i for e in mye)]
    for i in loose:
        rank[i] = ROLE_ORDER.index(by_id[i]['role'])
    layers = collections.defaultdict(list)
    for i in sorted(ids, key=lambda k: (rank[k], ROLE_ORDER.index(by_id[k]['role']), k)):
        layers[rank[i]].append(i)
    order = _order(layers, mye)

    BW, BH, GY, GX = 178, 60, 18, 236
    ncol = max(layers) + 1
    nrow = max(len(v) for v in layers.values())
    W = 16 + GX * ncol + 20
    Hh = 26 + nrow * (BH + GY) + 26

    pos = {}
    for l, ns in layers.items():
        x = 14 + GX * l
        for n in ns:
            pos[n] = (x, 26 + order[n] * (BH + GY), BW, BH)

    ok, on, ik, ino = _fan([(e['from'], e['to']) for e in mye])
    items = []
    for i, e in enumerate(mye):
        sa, sb = pos[e['from']], pos[e['to']]
        p1 = (sa[0] + sa[2], sa[1] + sa[3] * (ok[i] + 1.0) / (on[i] + 1.0))
        p2 = (sb[0] - 3, sb[1] + sb[3] * (ik[i] + 1.0) / (ino[i] + 1.0))
        items.append((e['from'], e['to'], e['kind'], p1, p2))
    corr_ys = ([26 + r * (BH + GY) - 8 - k * 6 for r in range(nrow) for k in range(3)]
               + [26 + nrow * (BH + GY) + 2 + k * 6 for k in range(3)])
    gut_xs = [14 + GX * (c + 1) - 50 + k * 8 for c in range(ncol) for k in range(-3, 5)]
    routes = route_all(items, pos, corr_ys, gut_xs, sep=8)

    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img">' % (W, Hh, W), ARROW_DEF]
    for pts, kind in routes:
        s.append(_poly(pts, kind))
    for i in ids:
        x, y, w, h = pos[i]
        s.append(_box(x, y, w, h, by_id[i], by_id[i].get('actor', ''), small=True))
    s.append('</svg>')
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    return ('<figure class="merflow"><div class="merflow-scroll">%s</div>%s</figure>'
            % (''.join(s), cap))


# ── ① 시간 띠 ────────────────────────────────────────────────────────────────
def time_svg(nodes, lanes, caption=''):
    """언제 무엇이 있었나만 본다. 날짜 간격에 비례해 자리를 잡고 화살표는 긋지 않는다.

    인과를 여기 얹지 않는다 — A/S는 시간상 뒤인데 앞 판단을 고치고, 메커니즘 사슬은
    하루 안에 다 일어나서 시간축 위에서는 펼 자리가 없다. 그건 cause_svg가 맡는다."""
    import datetime as _dt
    ev = [n for n in nodes if n.get('kind') == 'event']
    if not ev:
        return ''
    used = [l for l in lanes if any(n['lane'] == l[0] for n in ev)]
    row = {l[0]: i for i, l in enumerate(used)}

    def day(s):
        return _dt.date(*[int(v) for v in s.split('-')]).toordinal()

    d0 = min(day(n['date']) for n in ev)
    d1 = max(day(n['date']) for n in ev)
    L, PPD, BW, BH, VG = 132, 26, 150, 44, 8     # PPD = 하루당 가로 픽셀
    W = L + (d1 - d0) * PPD + BW + 40

    # 같은 레인에서 가로로 겹치면 아래 줄로 내린다(자리를 옮기지 지우지 않는다)
    placed = collections.defaultdict(list)
    pos = {}
    for n in sorted(ev, key=lambda n: (row[n['lane']], n['date'], n['id'])):
        x = L + (day(n['date']) - d0) * PPD
        k = 0
        while any(abs(px - x) < BW + 10 and pk == k for px, pk in placed[n['lane']]):
            k += 1
        placed[n['lane']].append((x, k))
        pos[n['id']] = (x, k)
    depth = {l[0]: max([k for _, k in placed[l[0]]] or [0]) + 1 for l in used}
    top, y = {}, 40
    for l in used:
        top[l[0]] = y
        y += depth[l[0]] * (BH + VG) + 14
    Hh = y + 8

    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img">' % (W, Hh, W)]
    for i, (lid, name) in enumerate(used):
        h = depth[lid] * (BH + VG) + 8
        if i % 2 == 0:
            s.append('<rect class="mf-lane-bg" x="0" y="%d" width="%d" height="%d" rx="6"/>'
                     % (top[lid] - 6, W, h))
        s.append('<text class="mf-lane" x="10" y="%d">%s</text>'
                 % (top[lid] + h / 2 - 6, esc(name)))
    # 날짜 눈금 — 주 단위로만 적는다(날마다 적으면 글자가 붙는다)
    for d in range(d0, d1 + 1):
        x = L + (d - d0) * PPD
        dt = _dt.date.fromordinal(d)
        if dt.weekday() == 0:
            s.append('<line class="mf-grid" x1="%d" y1="30" x2="%d" y2="%d"/>' % (x, x, Hh - 6))
            s.append('<text class="mf-date" x="%d" y="22">%d/%d</text>' % (x - 8, dt.month, dt.day))
    for n in ev:
        x, k = pos[n['id']]
        s.append(_box(x, top[n['lane']] + k * (BH + VG), BW, BH, n,
                      '%s · %s' % (n.get('actor', ''), n['date'][5:].replace('-', '/')),
                      small=True))
    s.append('</svg>')
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    return ('<figure class="merflow"><div class="mf-key"><span>가로 = 날짜(간격 비례)</span>'
            '<span>세로 = 주제 레인</span><span>화살표 없음 — 인과는 아래 인과도</span></div>'
            '<div class="merflow-scroll">%s</div>%s</figure>' % (''.join(s), cap))


# ── ② 인과도 ────────────────────────────────────────────────────────────────
def cause_svg(nodes, edges, keys=None, caption='', label_edges=True,
              box=(188, 62), gap=(30, 300)):
    """무엇이 무엇을 낳나만 본다. 가로는 시간이 아니라 사슬 깊이다.

    화살표에 근거 문장을 얹는다 — 선만 있으면 왜 그리로 가는지 못 읽는다. 날짜는 마디
    어깨에 작게 단다(시간은 time_svg가 맡는다)."""
    sel = [n for n in nodes if keys is None or n.get('thread') in keys]
    if not sel:
        return ''
    ids = {n['id'] for n in sel}
    by_id = {n['id']: n for n in sel}
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]

    rank = _rank(ids, mye)
    layers = collections.defaultdict(list)
    for i in sorted(ids, key=lambda k: (rank[k], by_id[k]['date'], k)):
        layers[rank[i]].append(i)
    order = _order(layers, mye)

    BW, BH = box
    GY, GX = gap
    ncol, nrow = max(layers) + 1, max(len(v) for v in layers.values())
    W, Hh = 16 + GX * ncol + 24, 30 + nrow * (BH + GY) + 24
    pos = {}
    for l, ns in layers.items():
        for n in ns:
            pos[n] = (14 + GX * l, 30 + order[n] * (BH + GY), BW, BH)

    ok, on, ik, ino = _fan([(e['from'], e['to']) for e in mye])
    items = []
    for i, e in enumerate(mye):
        sa, sb = pos[e['from']], pos[e['to']]
        p1 = (sa[0] + sa[2], sa[1] + sa[3] * (ok[i] + 1.0) / (on[i] + 1.0))
        p2 = (sb[0] - 3, sb[1] + sb[3] * (ik[i] + 1.0) / (ino[i] + 1.0))
        items.append((e['from'], e['to'], e['kind'], p1, p2))
    corr_ys = ([30 + r * (BH + GY) - 10 - k * 6 for r in range(nrow) for k in range(4)]
               + [30 + nrow * (BH + GY) + 2 + k * 6 for k in range(4)])
    gut_xs = [int(14 + GX * c + BW + 12 + k * 9)
              for c in range(ncol) for k in range((GX - BW - 24) // 9)]
    routes = route_all(items, pos, corr_ys, gut_xs, sep=8)

    s = ['<svg viewBox="0 0 %d %d" width="%d" role="img">' % (W, Hh, W), ARROW_DEF]
    # 글자 자리 — 마디 상자를 먼저 잡아 둔다. 라벨끼리만 견주면 상자 글씨 위에 얹힌다
    taken = [(x - 3, y - 3, x + w + 3, y + h + 3) for x, y, w, h in pos.values()]
    for (pts, kind), e in zip(routes, mye):
        s.append(_poly(pts, kind))
        if not label_edges:
            continue
        # 가장 긴 가로 구간 위에 근거 문장을 얹는다. 자리가 모자라면 생략한다
        best, blen = None, 0
        for a, b in _segs(pts):
            if abs(a[1] - b[1]) < 1.5 and abs(b[0] - a[0]) > blen:
                best, blen = (a, b), abs(b[0] - a[0])
        if not best or blen < 70:
            continue
        (ax, ay), (bx, _) = best
        fsz = 9.5
        lines = wrap(e.get('why', ''), fsz, max(blen - 12, 60))[:2]
        if not lines:
            continue
        x = min(ax, bx) + 6
        y = ay - 5 - (len(lines) - 1) * 11
        w = max(measure(t, fsz) for t in lines)
        rect = (x - 3, y - 10, x + w + 3, y + (len(lines) - 1) * 11 + 3)
        if any(min(rect[2], t[2]) - max(rect[0], t[0]) > 1
               and min(rect[3], t[3]) - max(rect[1], t[1]) > 1 for t in taken):
            continue
        taken.append(rect)
        s.append('<rect class="mf-elab-bg" x="%d" y="%d" width="%d" height="%d" rx="4"/>'
                 % (rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]))
        for i, t in enumerate(lines):
            s.append('<text class="mf-elab" x="%d" y="%d">%s</text>' % (x, y + i * 11, esc(t)))
    for i in ids:
        x, y, w, h = pos[i]
        n = by_id[i]
        s.append(_box(x, y, w, h, n, '%s · %s' % (n.get('actor', ''),
                                                  n['date'][5:].replace('-', '/')), small=True))
    s.append('</svg>')
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    key = ('<div class="mf-key"><span>가로 = 사슬 깊이(시간 아님)</span>'
           '<span>진한 테두리 = 일어난 일</span>'
           '<span style="color:var(--risk,#c2504a)">붉은 테두리 = 부작용</span>'
           '<span>점선 테두리 = 앞으로 볼 것</span><span>채운 상자 = 결론</span>'
           '<span>─ 낳는다</span><span>--- 앞 판단을 고친다</span>'
           '<span style="color:var(--risk,#c2504a)">··· 어긋난다</span></div>')
    return ('<figure class="merflow">%s<div class="merflow-scroll">%s</div>%s</figure>'
            % (key, ''.join(s), cap))


# ── ③ 사슬 글 — 그림 대신 번호 문장으로 ─────────────────────────────────────
CHAIN_CSS = '''
  .merchain{margin:14px 0;border:1px solid var(--line);border-radius:12px;padding:6px 14px 12px}
  .merchain ol{list-style:none;margin:0;padding:0;counter-reset:mc}
  .merchain li{position:relative;padding:12px 0 12px 46px;counter-increment:mc}
  .merchain li::before{content:counter(mc);position:absolute;left:0;top:12px;width:26px;
    height:26px;border-radius:50%;background:var(--sunk,rgba(127,127,127,.10));
    color:var(--ink-2);font-size:12px;font-weight:800;display:flex;align-items:center;
    justify-content:center}
  .merchain li + li::after{content:"";position:absolute;left:13px;top:-14px;height:26px;
    border-left:2px solid var(--line)}
  .merchain .mc-link{display:inline-block;font-size:11px;font-weight:800;color:var(--ink-3);
    margin:0 0 3px}
  .merchain .mc-say{font-size:14.5px;font-weight:750;color:var(--ink);line-height:1.5}
  .merchain .mc-who{font-size:11.5px;font-weight:700;color:var(--ink-3);margin-left:6px}
  .merchain .mc-why{font-size:12.5px;color:var(--ink-2);line-height:1.6;margin:4px 0 0}
  .merchain .mc-num{font-size:11.5px;color:var(--ink-3);margin:4px 0 0}
  .merchain li.side{margin-left:34px;padding-left:38px;border-left:2px dashed var(--line)}
  .merchain li.side .mc-say{font-weight:650;color:var(--ink-2);font-size:13.5px}
  .merchain li.bad .mc-link{color:var(--risk,#c2504a)}
'''

LINK_KO = {'cause': '그래서', 'update': '그 뒤 고쳤다', 'contradict': '그런데'}


def chain_html(nodes, edges, keys=None, say=None, lede=''):
    """사슬을 번호 문장으로 편다. 갈라지는 것(부작용·관전포인트)만 옆줄로 뺀다.

    도해가 안 읽히는 자리를 메우는 층이다 — 상자 사이를 눈으로 좇지 않고 위에서 아래로
    읽는다. 문장은 say로 갈아 끼울 수 있고, 없으면 마디 이름을 그대로 쓴다."""
    sel = [n for n in nodes if keys is None or n.get('thread') in keys]
    if not sel:
        return ''
    ids = {n['id'] for n in sel}
    by_id = {n['id']: n for n in sel}
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]
    rank = _rank(ids, mye)
    inbound = collections.defaultdict(list)
    for e in mye:
        inbound[e['to']].append(e)

    main = [i for i in ids if by_id[i]['role'] not in ('risk', 'watch')]
    main.sort(key=lambda i: (rank[i], by_id[i]['date'], i))
    side = collections.defaultdict(list)
    for i in ids:
        if by_id[i]['role'] in ('risk', 'watch'):
            src = [e['from'] for e in inbound[i] if e['from'] in main]
            side[src[0] if src else (main[0] if main else i)].append(i)

    say = say or {}
    out = ['<div class="merchain">']
    if lede:
        out.append('<p class="mc-why">%s</p>' % esc(lede))
    out.append('<ol>')

    def item(i, is_side=False):
        n = by_id[i]
        es = inbound[i]
        kind = es[0]['kind'] if es else None
        why = next((e.get('why') for e in es if e.get('why')), '')
        cls = 'side' if is_side else ''
        if n['role'] == 'risk':
            cls += ' bad'
        link = ''
        if is_side:
            link = '부작용' if n['role'] == 'risk' else '앞으로 볼 것'
        elif kind:
            link = LINK_KO.get(kind, '')
        out.append('<li class="%s">' % cls.strip())
        if link:
            out.append('<span class="mc-link">%s</span><br>' % esc(link))
        out.append('<span class="mc-say">%s</span><span class="mc-who">%s · %s</span>'
                   % (esc(say.get(i) or n['label']), esc(n.get('actor', '')),
                      n['date'][5:].replace('-', '/')))
        if why:
            out.append('<p class="mc-why">%s</p>' % esc(why))
        if n.get('nums'):
            out.append('<p class="mc-num">%s</p>' % esc(' · '.join(n['nums'])))
        out.append('</li>')

    for i in main:
        item(i)
        for j in side.get(i, []):
            item(j, True)
    out.append('</ol></div>')
    return ''.join(out)


# ── 주체 사슬 — 「누가 무엇을 해서 누구에게 뭐가 갔나」 한 줄로 ────────────────
def actor_chain_svg(nodes, edges, keys=None, per_row=3, caption='', say=None,
                    trunk_max=0, show_why=True, show_branch=True, show_bg=True):
    """사슬의 본줄기를 한 줄로 편다. 줄 끝에 닿으면 아래로 접어 다시 왼쪽에서 잇는다.

    상자마다 주체가 머리에 서서 「미 재무부 → 장기채 시장 → 미 재무부 → 월가」처럼
    주어가 이어진다. 갈라지는 것(부작용·앞으로 볼 것)은 본줄기 아래에 달아 둔다."""
    sel = [n for n in nodes if keys is None or n.get('thread') in keys]
    if not sel:
        return ''
    ids = {n['id'] for n in sel}
    by_id = {n['id']: n for n in sel}
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]

    # 본줄기 = 사슬에서 가장 긴 길. 부작용·관전포인트는 곁가지로 뺀다
    trunk_ids = [i for i in ids if by_id[i]['role'] not in ('risk', 'watch')
                 and (show_bg or by_id[i]['role'] != 'bg')
                 and by_id[i].get('depth', 1) < 2]
    te = [e for e in mye if e['from'] in trunk_ids and e['to'] in trunk_ids]
    rank = _rank(set(trunk_ids), te)
    trunk = sorted(trunk_ids, key=lambda i: (rank[i], by_id[i]['date'], i))
    inbound = collections.defaultdict(list)
    for e in mye:
        inbound[e['to']].append(e)
    if trunk_max and len(trunk) > trunk_max:
        # 굵은 마디부터 남긴다 — 사건과 결론이 먼저고 그다음이 메커니즘이다
        want = {'event': 0, 'verdict': 1, 'mech': 2, 'bg': 3}
        keep = sorted(trunk, key=lambda i: (want.get(by_id[i]['role'], 9),
                                            by_id[i]['date']))[:trunk_max]
        trunk = [i for i in trunk if i in set(keep)]
    branch = collections.defaultdict(list)
    for i in (ids if show_branch else set()):
        if by_id[i]['role'] in ('risk', 'watch'):
            up = [e['from'] for e in inbound[i] if e['from'] in trunk]
            branch[up[0] if up else trunk[0]].append(i)

    say = say or {}
    BW, BH, GX, BR = 214, 74, 66, 60
    rows = [trunk[i:i + per_row] for i in range(0, len(trunk), per_row)]
    W = 16 + per_row * (BW + GX) - GX + 40

    # 줄 높이는 그 줄에 달린 곁가지 수로 정한다 — 고정 높이로 두면 아래 줄과 겹친다
    rowtop, y = [], 16
    for row in rows:
        rowtop.append(y)
        nb = max([len(branch.get(i, [])) for i in row] or [0])
        y += BH + nb * (BR + 12) + 64
    Hh = y + 10

    pos = {}
    for r, row in enumerate(rows):
        rev = r % 2 == 1                      # 짝수 줄은 오른쪽에서 왼쪽으로 읽는다
        for c, i in enumerate(row):
            cc = (per_row - 1 - c) if rev else c
            pos[i] = (16 + cc * (BW + GX), rowtop[r], BW, BH)

    def nput(n, txt):
        m = dict(n)
        m['label'] = txt
        return m

    s = []
    taken = []                                 # 상자 자리 — 화살표 글자가 그 위에 얹히지 않게
    for i in trunk:
        x, yy, w, h = pos[i]
        taken.append((x - 4, yy - 4, x + w + 4, yy + h + 4))
        for j in range(len(branch.get(i, []))):
            by_ = yy + h + 14 + j * (BR + 12)
            taken.append((x + 12, by_ - 4, x + BW + 4, by_ + BR + 4))

    for k in range(len(trunk) - 1):
        a_, b_ = trunk[k], trunk[k + 1]
        (ax, ay, aw, ah), (bx, byy, bw, bh) = pos[a_], pos[b_]
        same_row = abs(ay - byy) < 2
        if same_row:
            x1, x2 = (ax + aw, bx - 3) if bx > ax else (ax - 3, bx + bw)
            s.append(_poly([(x1, ay + ah / 2), (x2, ay + ah / 2)], 'cause'))
        else:                                  # 줄을 접는 자리 — 아래로 내려 잇는다
            xm = ax + aw / 2
            s.append(_poly([(xm, ay + ah), (xm, byy - 3)], 'cause'))
        why = next((e.get('why') for e in inbound[b_] if e.get('why')), '') if show_why else ''
        if not why:
            continue
        if same_row:
            lx = (ax + aw + 8) if bx > ax else (bx + bw + 8)
            ly = ay + ah / 2 - 16
            wid = GX - 8
        else:
            lx = min(ax, bx) + aw / 2 + 12
            ly = ay + ah + 16
            wid = BW
        lines = wrap(why, 9.5, wid)[:3]
        if not lines:
            continue
        tw = max(measure(t, 9.5) for t in lines)
        rect = (lx - 3, ly - 11, lx + tw + 3, ly + (len(lines) - 1) * 11 + 3)
        if any(min(rect[2], t[2]) - max(rect[0], t[0]) > 1
               and min(rect[3], t[3]) - max(rect[1], t[1]) > 1 for t in taken):
            continue
        taken.append(rect)
        for t, ln in enumerate(lines):
            s.append('<text class="mf-elab" x="%d" y="%d">%s</text>' % (lx, ly + t * 11, esc(ln)))

    for i in trunk:
        x, yy, w, h = pos[i]
        n = by_id[i]
        s.append(_box(x, yy, w, h, nput(n, say.get(i) or n['label']), n.get('actor', '')))
        for j, bid in enumerate(branch.get(i, [])):
            bn = by_id[bid]
            bx, byy = x + 16, yy + h + 14 + j * (BR + 12)
            s.append(_poly([(x + 34 + j * 8, yy + h), (x + 34 + j * 8, byy - 3)], 'cause'))
            s.append(_box(bx, byy, BW - 16, BR, nput(bn, say.get(bid) or bn['label']),
                          bn.get('actor', ''), small=True))

    svg = '<svg viewBox="0 0 %d %d" width="%d" role="img">%s%s</svg>' % (W, Hh, W, ARROW_DEF,
                                                                        ''.join(s))
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    key = ('<div class="mf-key"><span>상자 머리 = 누가</span><span>아래 = 무엇을 했나</span>'
           + ('<span style="color:var(--risk,#c2504a)">붉은 상자 = 부작용</span>'
              if show_branch else '') + '</div>')
    return ('<figure class="merflow">%s<div class="merflow-scroll">%s</div>%s</figure>'
            % (key, svg, cap))


# ── 시퀀스 다이어그램 — 주체를 기둥으로 세우고 시간은 아래로 ─────────────────
SEQ_CSS = '''
  .merflow .sq-head{fill:var(--card,var(--surface,#fff));stroke:var(--ink-3);stroke-width:1.4}
  .merflow .sq-name{fill:var(--ink);font-size:11.5px;font-weight:850}
  .merflow .sq-life{stroke:var(--ink-3);stroke-width:2;opacity:.55}
  .merflow .sq-msg{fill:none;stroke:var(--ink-3);stroke-width:1.5;marker-end:url(#mf-ar)}
  .merflow .sq-msg.rk{stroke:var(--risk,#c2504a)}
  .merflow .sq-msg.up{stroke-dasharray:5 3}
  .merflow .sq-say{fill:var(--ink);font-size:11px;font-weight:700}
  .merflow .sq-say.rk{fill:var(--risk,#c2504a)}
  .merflow .sq-day{fill:var(--ink-3);font-size:10px;font-weight:800}
  .merflow .sq-band{fill:var(--sunk,rgba(127,127,127,.05))}
  /* 메르의 판단 — 기둥으로 세우지 않는다. 그 일이 난 자리에 쪽지로 붙인다 */
  .merflow .sq-note{fill:var(--accent-soft,rgba(127,127,127,.10));stroke:var(--ink-3);
                    stroke-width:1.2}
  .merflow .sq-note-t{fill:var(--ink);font-size:11px;font-weight:700}
  .merflow .sq-note-k{fill:var(--ink-3);font-size:9.5px;font-weight:850;letter-spacing:.04em}
  .merflow .sq-tie{stroke:var(--ink-3);stroke-width:1.2;stroke-dasharray:3 3;fill:none}
'''


def sequence_svg(nodes, edges, columns, keys=None, caption='', say=None, only_trunk=True,
                 flip=False, nums=True):
    """주체를 기둥으로 세우고 시간을 아래로 흘린다.

    같은 주체가 여러 번 나와도 기둥은 하나다 — 미 재무부 상자가 여덟 번 서는 대신 기둥
    하나에 화살표 여덟 개가 붙는다. 시간은 세로 한 방향, 인과는 화살표 방향이라 둘이 안 섞인다.
    화살표에 적히는 말은 **받는 쪽에서 무슨 일이 났나**다."""
    sel = [n for n in nodes if keys is None or n.get('thread') in keys]
    if only_trunk:
        sel = [n for n in sel if n.get('depth', 1) < 2]
    if not sel:
        return ''
    by_id = {n['id']: n for n in sel}
    ids = set(by_id)
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]
    # 메르의 판단은 기둥이 아니다 — 그 대목에 쪽지로 붙는다
    NOTE = '메르'
    cols = [c for c in columns if c != NOTE and any(n.get('col') == c for n in sel)]
    if flip:                                   # 기둥 차례를 좌우로 뒤집는다
        cols = cols[::-1]
    cx = {c: 150 + i * 232 for i, c in enumerate(cols)}
    if not cx:
        return ''

    say = say or {}
    rank = _rank(ids, mye)
    mye.sort(key=lambda e: (by_id[e['to']]['date'], rank[e['to']], e['to']))

    ROWH, NOTEH, TOP, NW, MW = 78, 78, 126, 250, 196
    W = 96 + (len(cols) - 1) * 232 + 250
    inb = collections.defaultdict(list)
    for e in mye:
        inb[e['to']].append(e)
    seq = sorted(ids, key=lambda i: (by_id[i]['date'], rank[i], i))

    rows = []                                  # (종류, 마디, 들어오는 화살표들, y)
    y = TOP
    for i in seq:
        n = by_id[i]
        kind = 'note' if n.get('col') == NOTE else 'msg'
        rows.append((kind, i, inb.get(i, []), y))
        y += NOTEH if kind == 'note' else ROWH
    Hh = y + 26
    s = [ARROW_DEF]
    for c in cols:
        x = cx[c]
        s.append('<line class="sq-life" x1="%d" y1="%d" x2="%d" y2="%d"/>'
                 % (x, 66, x, Hh - 16))
        w = max(measure(c, 11.5) + 22, 96)
        s.append('<rect class="sq-head" x="%d" y="26" width="%d" height="34" rx="8"/>'
                 % (x - w / 2, w))
        s.append('<text class="sq-name" x="%d" y="48" text-anchor="middle">%s</text>'
                 % (x, esc(c)))

    ry = {i: y for _, i, _, y in rows}
    last_day = None
    for k, (kind, i, ins, y) in enumerate(rows):
        b = by_id[i]
        if k % 2 == 0:
            s.append('<rect class="sq-band" x="0" y="%d" width="%d" height="%d"/>'
                     % (y - 24, W, (NOTEH if kind == 'note' else ROWH)))
        if b['date'] != last_day:
            s.append('<text class="sq-day" x="12" y="%d">%s</text>'
                     % (y + 4, b['date'][5:].replace('-', '/')))
            last_day = b['date']
        txt = say.get(i) or b['label']
        nl = ' · '.join(b.get('nums') or []) if nums else ''
        if kind == 'note':                      # 메르의 판단 — 앞 대목 옆에 쪽지로
            x1 = cx.get(by_id[ins[0]['from']].get('col')) if ins else cx[cols[0]]
            if x1 is None:
                x1 = cx[cols[0]]
            nx = x1 + 22 if x1 + 22 + NW <= W - 12 else max(x1 - 22 - NW, 12)
            lines = wrap(txt, 11.0, NW - 20)[:2]
            nlines = wrap(nl, 9.5, NW - 20)[:1] if nl else []
            h = 26 + len(lines) * 14 + (13 if nlines else 0)
            tie_x = nx if nx > x1 else nx + NW
            s.append('<path class="sq-tie" d="M%d,%d L%d,%d"/>' % (x1, y - 6, tie_x, y - 6))
            s.append('<rect class="sq-note" x="%d" y="%d" width="%d" height="%d" rx="6"/>'
                     % (nx, y - 16, NW, h))
            s.append('<text class="sq-note-k" x="%d" y="%d">메르의 판단</text>' % (nx + 10, y - 2))
            for t, ln in enumerate(lines):
                s.append('<text class="sq-note-t" x="%d" y="%d">%s</text>'
                         % (nx + 10, y + 14 + t * 14, esc(ln)))
            for t, ln in enumerate(nlines):
                s.append('<text class="qh-n" x="%d" y="%d">%s</text>'
                         % (nx + 10, y + 14 + len(lines) * 14 + t * 12, esc(ln)))
            continue
        x2 = cx.get(b.get('col'))
        if x2 is None:
            continue
        rk = b['role'] == 'risk'
        lines = wrap(txt, 10.5, MW - 18)[:2]
        nlines = wrap(nl, 9.5, MW - 18)[:1] if nl else []
        bh = 14 + len(lines) * 14 + (13 if nlines else 0)
        bx, by_ = x2 - MW / 2, y - bh / 2
        # 들어오는 화살표를 전부 그린다 — 하나만 그리면 사슬이 끊겨 비약으로 보인다
        for t, e in enumerate(ins):
            a = by_id[e['from']]
            x1 = cx.get(a.get('col'))
            ay = ry.get(e['from'])
            if x1 is None or ay is None:
                continue
            cls = ' rk' if rk else (' up' if e['kind'] == 'update' else '')
            yy = y + (t - (len(ins) - 1) / 2.0) * 11
            if abs(x1 - x2) < 2:                # 제 기둥 안에서 일어난 일 — 고리로
                s.append('<path class="sq-msg%s" d="M%d,%d L%d,%d L%d,%d L%d,%d"/>'
                         % (cls, x1, ay + 14, x1 + MW / 2 + 22, ay + 14,
                            x1 + MW / 2 + 22, yy, bx + MW + 4, yy))
            else:
                s.append('<path class="sq-msg%s" d="M%d,%d L%d,%d L%d,%d"/>'
                         % (cls, x1, ay + 14, x1, yy,
                            (bx - 4) if x2 > x1 else (bx + MW + 4), yy))
        s.append('<rect class="qh-box%s" x="%d" y="%d" width="%d" height="%d" rx="7"/>'
                 % (' rk' if rk else '', bx, by_, MW, bh))
        for t, ln in enumerate(lines):
            s.append('<text class="qh-t" x="%d" y="%d">%s</text>'
                     % (bx + 9, by_ + 19 + t * 14, esc(ln)))
        for t, ln in enumerate(nlines):
            s.append('<text class="qh-n" x="%d" y="%d">%s</text>'
                     % (bx + 9, by_ + 19 + len(lines) * 14 + t * 12, esc(ln)))

    svg = '<svg viewBox="0 0 %d %d" width="%d" role="img">%s</svg>' % (W, Hh, W, ''.join(s))
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    key = ('<div class="mf-key"><span>위 = 누가</span><span>아래로 = 시간</span>'
           '<span>화살표 = 무슨 일이 났나</span>'
           '<span style="color:var(--risk,#c2504a)">붉은 화살표 = 부작용</span>'
           '<span>채운 쪽지 = 메르의 판단</span></div>')
    return ('<figure class="merflow">%s<div class="merflow-scroll">%s</div>%s</figure>'
            % (key, svg, cap))


# ── 시퀀스 눕히기 — 주체는 왼쪽 행, 시간은 위쪽 가로축 ───────────────────────
SEQH_CSS = '''
  .merflow .qh-name{fill:var(--ink);font-size:11.5px;font-weight:850}
  .merflow .qh-head{fill:var(--card,var(--surface,#fff));stroke:var(--ink-3);stroke-width:1.4}
  .merflow .qh-life{stroke:var(--line);stroke-width:1.4;stroke-dasharray:3 5}
  .merflow .qh-band{fill:var(--sunk,rgba(127,127,127,.05))}
  .merflow .qh-day{fill:var(--ink-3);font-size:10.5px;font-weight:800}
  .merflow .qh-grid{stroke:var(--line);stroke-width:1;stroke-dasharray:2 4}
  .merflow .qh-msg{fill:none;stroke:var(--ink-3);stroke-width:1.5;marker-end:url(#mf-ar)}
  .merflow .qh-msg.rk{stroke:var(--risk,#c2504a)}
  .merflow .qh-msg.up{stroke-dasharray:5 3}
  .merflow .qh-box{fill:var(--card,var(--surface,#fff));stroke:var(--line);stroke-width:1.2}
  .merflow .qh-box.rk{stroke:var(--risk,#c2504a)}
  .merflow .qh-t{fill:var(--ink);font-size:10.5px;font-weight:700}
  .merflow .qh-n{fill:var(--ink-3);font-size:9.5px;font-weight:700}
  .merflow .qh-note{fill:var(--accent-soft,rgba(127,127,127,.10));stroke:var(--ink-3);
                    stroke-width:1.2}
  .merflow .qh-note-k{fill:var(--ink-3);font-size:9.5px;font-weight:850;letter-spacing:.04em}
  .merflow .qh-tie{stroke:var(--ink-3);stroke-width:1.2;stroke-dasharray:3 3;fill:none}
'''


def sequence_h_svg(nodes, edges, columns, keys=None, caption='', say=None,
                   only_trunk=True, nums=True):
    """시퀀스를 눕힌다 — 주체가 왼쪽에 행으로 서고 시간이 가로로 흐른다.

    세로로 세우면 화살표 옆에 글자를 넣을 자리가 한 줄뿐이라 숫자를 못 단다. 눕히면 단계마다
    제 상자가 생겨서 무슨 일이 났나와 숫자를 같이 넣을 수 있다."""
    sel = [n for n in nodes if keys is None or n.get('thread') in keys]
    if only_trunk:
        sel = [n for n in sel if n.get('depth', 1) < 2]
    if not sel:
        return ''
    by_id = {n['id']: n for n in sel}
    ids = set(by_id)
    mye = [e for e in edges if e['from'] in ids and e['to'] in ids]
    NOTE = '메르'
    rows_c = [c for c in columns if c != NOTE and any(n.get('col') == c for n in sel)]
    if not rows_c:
        return ''
    say = say or {}
    rank = _rank(ids, mye)
    mye.sort(key=lambda e: (by_id[e['to']]['date'], rank[e['to']], e['to']))

    L, COLW, ROWH, BW, BH, TOP = 128, 182, 96, 166, 62, 62
    steps, seen_note = [], set()
    for e in mye:
        b = by_id[e['to']]
        if b.get('col') == NOTE:
            if b['id'] in seen_note:
                continue
            seen_note.add(b['id'])
            steps.append(('note', e))
        else:
            steps.append(('msg', e))
    ry = {c: TOP + i * ROWH for i, c in enumerate(rows_c)}
    NOTEY = TOP + len(rows_c) * ROWH + 10
    W = L + len(steps) * COLW + 30
    Hh = NOTEY + (74 if seen_note else 0) + 20

    s = [ARROW_DEF]
    for i, c in enumerate(rows_c):
        y = ry[c]
        if i % 2 == 0:
            s.append('<rect class="qh-band" x="0" y="%d" width="%d" height="%d"/>'
                     % (y - ROWH / 2 + 4, W, ROWH - 8))
        s.append('<line class="qh-life" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (L - 16, y, W - 12, y))
        w = max(measure(c, 11.5) + 20, 104)
        s.append('<rect class="qh-head" x="8" y="%d" width="%d" height="32" rx="8"/>'
                 % (y - 16, w))
        s.append('<text class="qh-name" x="%d" y="%d">%s</text>' % (16, y + 5, esc(c)))

    last_day = None
    for i, (kind, e) in enumerate(steps):
        a, b = by_id[e['from']], by_id[e['to']]
        x = L + i * COLW
        if b['date'] != last_day:
            s.append('<line class="qh-grid" x1="%d" y1="30" x2="%d" y2="%d"/>'
                     % (x - 10, x - 10, Hh - 14))
            s.append('<text class="qh-day" x="%d" y="24">%s</text>'
                     % (x - 6, b['date'][5:].replace('-', '/')))
            last_day = b['date']
        txt = say.get(b['id']) or b['label']
        if kind == 'note':
            ny = NOTEY
            lines = wrap(txt, 11.0, BW + 6)[:2]
            s.append('<path class="qh-tie" d="M%d,%d L%d,%d"/>'
                     % (x + BW / 2, ry.get(a.get('col'), TOP), x + BW / 2, ny))
            s.append('<rect class="qh-note" x="%d" y="%d" width="%d" height="%d" rx="6"/>'
                     % (x, ny, BW + 16, 26 + len(lines) * 14))
            s.append('<text class="qh-note-k" x="%d" y="%d">메르의 판단</text>' % (x + 9, ny + 14))
            for t, ln in enumerate(lines):
                s.append('<text class="qh-t" x="%d" y="%d">%s</text>'
                         % (x + 9, ny + 30 + t * 14, esc(ln)))
            continue
        y1, y2 = ry.get(a.get('col')), ry.get(b.get('col'))
        if y1 is None or y2 is None:
            continue
        cls = ' rk' if b['role'] == 'risk' else (' up' if e['kind'] == 'update' else '')
        top_y = y2 - BH / 2
        if abs(y1 - y2) < 2:                   # 제 행에서 일어난 일 — 짧은 고리
            s.append('<path class="qh-msg%s" d="M%d,%d L%d,%d L%d,%d"/>'
                     % (cls, x - 14, y1 - 16, x - 14, top_y - 8, x + 6, top_y - 8))
        else:
            s.append('<path class="qh-msg%s" d="M%d,%d L%d,%d"/>'
                     % (cls, x + BW / 2, y1 + (18 if y2 > y1 else -18),
                        x + BW / 2, top_y + (-4 if y2 > y1 else BH + 4)))
        lines = wrap(txt, 10.5, BW - 18)[:2]
        nl = ' · '.join(b.get('nums') or []) if nums else ''
        nlines = wrap(nl, 9.5, BW - 18)[:1] if nl else []
        h = 14 + len(lines) * 14 + (14 if nlines else 0)
        s.append('<rect class="qh-box%s" x="%d" y="%d" width="%d" height="%d" rx="7"/>'
                 % (' rk' if b['role'] == 'risk' else '', x, top_y, BW, max(h, 40)))
        for t, ln in enumerate(lines):
            s.append('<text class="qh-t" x="%d" y="%d">%s</text>'
                     % (x + 9, top_y + 20 + t * 14, esc(ln)))
        for t, ln in enumerate(nlines):
            s.append('<text class="qh-n" x="%d" y="%d">%s</text>'
                     % (x + 9, top_y + 20 + len(lines) * 14 + t * 12, esc(ln)))

    svg = '<svg viewBox="0 0 %d %d" width="%d" role="img">%s</svg>' % (W, Hh, W, ''.join(s))
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ''
    key = ('<div class="mf-key"><span>왼쪽 = 누가</span><span>오른쪽으로 = 시간</span>'
           '<span>세로 화살표 = 누가 누구에게</span>'
           '<span style="color:var(--risk,#c2504a)">붉은 상자 = 부작용</span>'
           '<span>아래 쪽지 = 메르의 판단</span></div>')
    return ('<figure class="merflow">%s<div class="merflow-scroll">%s</div>%s</figure>'
            % (key, svg, cap))
