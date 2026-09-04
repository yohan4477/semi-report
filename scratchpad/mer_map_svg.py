# -*- coding: utf-8 -*-
"""관계 지도 — 주체 카드를 놓고 그 사이에 오가는 것을 적는다.

시퀀스와 다른 점은 **시간축이 없다**는 것이다. 시간은 화살표에 붙는 번호로 읽는다
(①②③). 축을 세우면 같은 주체가 여러 번 서는데, 지도에서는 카드 하나가 끝까지 그 자리를
지키고 그 사이를 오가는 것만 늘어난다.

  카드   주체 하나. 위에 붙는 작은 말(kicker)이 그가 어떤 자리인지 알려 준다
  화살표 무엇이 오가나. 실선(초록)은 돈, 실선(회색)은 값·물량, 점선은 안 하기로 한 것
  번호   시간. 사슬에서 일어난 차례다

자리(slots)는 사람이 정한다 — 어느 카드가 위에 서야 하는지는 기계가 모른다.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mer_flow_svg import esc, wrap, measure, route_all, _segs  # noqa: E402

CIRC = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮'

CSS = """
  /* 껍데기는 `docs/도해 유형 — 무엇을 언제 그리나.md` 3절을 따른다. 선·상자 붓은
     card_lib 표준(.flow-cash/.flow-svc/.flow-cond/.bx/.bx-key/.t-role)을 그대로 쓰고
     여기서는 판·제목·각주만 얹는다 — 색을 두 군데서 잡으면 다크모드가 갈린다. */
  .mermap{margin:18px 0;border-radius:14px;padding:24px 24px 18px;
          background:var(--fig-bg,rgba(127,127,127,.05))}
  .mermap h3{margin:0 0 6px;font-size:19px;font-weight:750;color:var(--ink);line-height:1.35}
  .mermap .mp-sub{margin:0 0 16px;font-size:13.5px;color:var(--ink-3);line-height:1.55}
  .mermap .mp-legend{display:flex;gap:20px;flex-wrap:wrap;font-size:13.5px;font-weight:500;
                     color:var(--ink-2);margin:0 0 16px;align-items:center}
  .mermap .mp-legend span{display:inline-flex;align-items:center;gap:8px}
  .mermap .mp-legend svg{width:30px;height:10px;display:block}
  .mermap .mp-note{margin:14px 2px 0;font-size:11.5px;color:var(--ink-3);line-height:1.6}
  .mermap .mp-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .mermap svg{display:block;width:100%;height:auto}
  .mermap .mp-group{fill:var(--fig-wrapbg,rgba(47,143,107,.10));stroke:none}
  .mermap .mp-gname{fill:var(--ink-2);font-size:11px;font-weight:600}
  .mermap .mp-card{fill:var(--fig-bxbg,#fff);stroke:var(--line,#d8d8d8);stroke-width:1.2}
  .mermap .mp-card.on{fill:var(--fig-keybg,#d8f0e6);stroke:var(--fig-good,#2f8f6b);
                      stroke-width:1.6}
  .mermap .mp-kickbg{fill:var(--fig-bg,#f6f7f8)}
  .mermap .mp-kick{fill:var(--ink-3);font-size:11px;font-weight:800;letter-spacing:.05em}
  .mermap .mp-rowlab{fill:var(--ink-3);font-size:11px;font-weight:800;letter-spacing:.05em}
  .mermap .mp-name{fill:var(--ink);font-size:15px;font-weight:750}
  .mermap .mp-desc{fill:var(--ink-2);font-size:13px}
  .mermap .mp-flow{fill:none;stroke:var(--ink-3);stroke-width:1.6;marker-end:url(#mp-a)}
  .mermap .mp-flow.cash{stroke:var(--fig-good,#2f8f6b);stroke-width:1.8;
                        marker-end:url(#mp-ac)}
  .mermap .mp-flow.cond{stroke-width:1.4;stroke-dasharray:5 4}
  .mermap .mp-lab{fill:var(--ink-2);font-size:13px;font-weight:500}
  .mermap .mp-lab.cash{fill:var(--fig-good,#2f8f6b);font-weight:700}
"""



DEFS = ('<defs>'
        '<marker id="mp-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"'
        ' markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="var(--ink-3)"/></marker>'
        '<marker id="mp-ac" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6"'
        ' markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="var(--fig-good,#2f8f6b)"/></marker>'
        '</defs>')


def _face(a, b):
    """가까운 면을 고른다. 'R','L','B','T' 중 하나."""
    acx, acy = a[0] + a[2] / 2.0, a[1] + a[3] / 2.0
    bcx, bcy = b[0] + b[2] / 2.0, b[1] + b[3] / 2.0
    if abs(acx - bcx) >= abs(acy - bcy):
        return ('R', 'L') if bcx > acx else ('L', 'R')
    return ('B', 'T') if bcy > acy else ('T', 'B')


GRID = 20          # 나란한 선 사이 간격이자 끝점이 서는 격자


def _point(box, face, k, n):
    """면 위의 자리. 한 면에서 여럿이 나가면 **격자 간격으로** 벌려 세운다 —
    비율로 나누면 카드마다 간격이 달라져 그림이 들쭉날쭉해진다."""
    x, y, w, h = box
    # 둘뿐이면 두 칸씩 벌린다 — 한 칸(14px)이면 선도 라벨도 붙어 보인다
    d = (k - (n - 1) / 2.0) * GRID * (2 if n <= 2 else 1)
    if face in ('R', 'L'):
        cy = round((y + h / 2.0 + d) / GRID) * GRID
        cy = min(max(cy, y + 16), y + h - 16)
        return (x + w + 2, cy) if face == 'R' else (x - 2, cy)
    cx = round((x + w / 2.0 + d) / GRID) * GRID
    cx = min(max(cx, x + 24), x + w - 24)
    return (cx, y - 2) if face == 'T' else (cx, y + h + 2)


def render(spec, caption=''):
    slots, actors, flows = spec['slots'], spec['actors'], spec['flows']
    # 칸은 격자에 맞춘다. 세로 여백은 가로보다 넓게 둔다 — 세로로 오가는 선 옆에
    # 라벨이 설 자리가 있어야 한다(가로줄 라벨은 선 위에 얹으면 되지만 세로는 옆에 선다)
    CW, CH, GX, GY, PAD = 268, 126, 132, 184, 28
    rowlab = spec.get('rowLabels') or []
    LABW = 150 if rowlab else 0                # 행 라벨이 설 왼쪽 칸
    nrow = max(r for r, _ in slots.values()) + 1
    ncol = max(c for _, c in slots.values()) + 1
    W = PAD * 2 + LABW + ncol * CW + (ncol - 1) * GX
    Hh = PAD * 2 + 24 + nrow * CH + (nrow - 1) * GY + 40

    def snap(v):
        return round(v / GRID) * GRID

    pos = {}
    for name, (r, c) in slots.items():
        pos[name] = (snap(PAD + LABW + c * (CW + GX)),
                     snap(PAD + 68 + r * (CH + GY)), CW, CH)

    # 면마다 몇 개가 붙는지 먼저 세고 자리를 나눈다
    faces = {}
    for f in flows:
        fa, fb = _face(pos[f['from']], pos[f['to']])
        fa, fb = f.get('fromFace', fa), f.get('toFace', fb)
        faces.setdefault((f['from'], fa), []).append(f)
        faces.setdefault((f['to'], fb), []).append(f)
    items = []
    for f in flows:
        fa, fb = _face(pos[f['from']], pos[f['to']])
        fa, fb = f.get('fromFace', fa), f.get('toFace', fb)
        ka = faces[(f['from'], fa)].index(f)
        kb = faces[(f['to'], fb)].index(f)
        p1 = _point(pos[f['from']], fa, ka, len(faces[(f['from'], fa)]))
        p2 = _point(pos[f['to']], fb, kb, len(faces[(f['to'], fb)]))
        # 마주 보는 면끼리면 끝점을 맞춰 곧은 선을 만든다. 다만 **두 카드가 그 축에서
        # 겹칠 때만** 맞춘다 — 안 겹치는데 맞추면 끝점이 카드 밖으로 나간다
        bx, by_, bw, bh = pos[f['to']]
        if {fa, fb} == {'L', 'R'} and by_ + 14 <= p1[1] <= by_ + bh - 14:
            p2 = (p2[0], p1[1])
        elif {fa, fb} == {'T', 'B'} and bx + 20 <= p1[0] <= bx + bw - 20:
            p2 = (p1[0], p2[1])
        p2 = (p2[0] + (-3 if fb == 'L' else 3 if fb == 'R' else 0),
              p2[1] + (-3 if fb == 'T' else 3 if fb == 'B' else 0))
        items.append((f['from'], f['to'], f.get('kind', 'svc'), p1, p2))
    # 복도·홈은 카드 사이 한가운데를 기준으로 격자 간격으로만 놓는다
    # 줄 사이 복도 + 판 바깥 레일(맨 윗줄 위·맨 아랫줄 아래). 규칙 §7 — 멀리 떨어진 두
    # 상자를 잇는 선은 가운데를 가로지르지 않고 바깥으로 돌린다
    # 복도와 레일은 카드가 실제로 선 자리에서 뽑는다 — 식으로 다시 계산하면 어긋난다
    tops = sorted({p[1] for p in pos.values()})
    bots = sorted({p[1] + p[3] for p in pos.values()})
    corr_ys = []
    for i in range(len(tops) - 1):
        mid = (bots[i] + tops[i + 1]) / 2.0
        corr_ys += [round((mid + (k - 2) * GRID) / GRID) * GRID for k in range(5)]
    corr_ys += [round((tops[0] - 34 - k * GRID) / GRID) * GRID for k in range(3)]
    corr_ys += [round((bots[-1] + 34 + k * GRID) / GRID) * GRID for k in range(3)]
    gut_xs = [round((PAD + c * (CW + GX) + CW + GX / 2.0 + (k - 2) * GRID) / GRID) * GRID
              for c in range(ncol) for k in range(5)]
    # 끝점은 이미 격자에 맞춰 잡았다. 중간 점까지 스냅하면 끝점과 어긋나 대각선이 생긴다
    # 카드 사이 한가운데 — 선이 여기로 지나가야 어느 카드에도 안 붙어 보인다
    # 카드 사이 한가운데 — 선이 여기로 지나가야 어느 카드에도 안 붙어 보인다
    mid_ys = [(bots[i] + tops[i + 1]) / 2.0 for i in range(len(tops) - 1)]
    mid_ys += [tops[0] - 34, bots[-1] + 34]
    lefts = sorted({p[0] for p in pos.values()})
    rights = sorted({p[0] + p[2] for p in pos.values()})
    mid_xs = [(rights[i] + lefts[i + 1]) / 2.0 for i in range(len(lefts) - 1)]
    mid_xs += [lefts[0] - 34, rights[-1] + 34]
    routes = route_all(items, pos, corr_ys, gut_xs, sep=GRID - 1, strict=True, pad=30,
                       prefer_ys=mid_ys, prefer_xs=mid_xs)

    s = [DEFS]
    for g in spec.get('groups', []):
        mem = [pos[m] for m in g['members'] if m in pos]
        if not mem:
            continue
        gx = min(m[0] for m in mem) - 18
        gy = min(m[1] for m in mem) - 34
        gx2 = max(m[0] + m[2] for m in mem) + 18
        gy2 = max(m[1] + m[3] for m in mem) + 18
        s.append('<rect class="mp-group" x="%d" y="%d" width="%d" height="%d" rx="14"/>'
                 % (gx, gy, gx2 - gx, gy2 - gy))
        s.append('<text class="mp-gname" x="%d" y="%d">%s</text>'
                 % (gx + 14, gy + 20, esc(g.get('label', ''))))
    # 라벨이 피해야 할 것 — 카드, 그리고 **이미 그은 선**. 선을 빼면 글자가 선 위에 얹힌다.
    taken = [(x - 8, y - 22, x + w + 8, y + h + 8) for x, y, w, h in pos.values()]
    for pts, _k in routes:
        for A, B in _segs(pts):
            taken.append((min(A[0], B[0]) - 6, min(A[1], B[1]) - 6,
                          max(A[0], B[0]) + 6, max(A[1], B[1]) + 6))
    labels = []
    for i, ((pts, kind), f) in enumerate(zip(routes, flows)):
        s.append('<path class="mp-flow %s" d="%s"/>'
                 % (kind, 'M%d,%d ' % pts[0] + ' '.join('L%d,%d' % p for p in pts[1:])))
        segs = _segs(pts)
        horiz = [(a, b) for a, b in segs if abs(a[1] - b[1]) < 1.5]
        seg = max(horiz, key=lambda ab: abs(ab[1][0] - ab[0][0])) if horiz else \
            max(segs, key=lambda ab: abs(ab[1][1] - ab[0][1]))
        is_h = bool(horiz)
        room = abs(seg[1][0] - seg[0][0]) - 16 if is_h else 150
        no = CIRC[i] if i < len(CIRC) else '%d.' % (i + 1)
        full = '%s %s' % (no, f['label'])
        if is_h:
            # 가로 구간은 자리가 넉넉하다 — 한 줄로 둔다
            lines = [full] if measure(full, 12.5) <= max(room, 190) else                 wrap(full, 12.5, max(room, 150))[:2]
        else:
            # 세로 구간 옆은 좁다. 두 줄로 접어야 카드 사이 홈에 들어간다
            lines = [full] if measure(full, 12.5) <= 150 else wrap(full, 12.5, 150)[:2]
        wgt = max(measure(t, 12.5) for t in lines)
        if is_h:
            lx = (seg[0][0] + seg[1][0]) / 2.0 - wgt / 2.0
            ly = seg[0][1] - 9 - (len(lines) - 1) * 14
        else:
            lx = seg[0][0] + 16
            ly = (seg[0][1] + seg[1][1]) / 2.0 - (len(lines) - 1) * 7
            rect = (lx - 4, ly - 12, lx + wgt + 4, ly + (len(lines) - 1) * 14 + 4)
            if any(min(rect[2], t[2]) - max(rect[0], t[0]) > 1
                   and min(rect[3], t[3]) - max(rect[1], t[1]) > 1 for t in taken):
                lx = seg[0][0] - 16 - wgt
        # 자리를 못 찾으면 **안 그린다**. 카드 글씨 위에 얹히면 둘 다 못 읽는다.
        def free(px, py):
            r = (px - 4, py - 12, px + wgt + 4, py + (len(lines) - 1) * 14 + 4)
            return not any(min(r[2], t[2]) - max(r[0], t[0]) > 1
                           and min(r[3], t[3]) - max(r[1], t[1]) > 1 for t in taken)

        spot = None
        for frac in (0.5, 0.34, 0.66, 0.2, 0.8):
            if is_h:
                cx0 = seg[0][0] + (seg[1][0] - seg[0][0]) * frac - wgt / 2.0
                for off in (-9, -25, 15, 31):
                    if free(cx0, seg[0][1] + off - (len(lines) - 1) * 14):
                        spot = (cx0, seg[0][1] + off - (len(lines) - 1) * 14)
                        break
            else:
                cy0 = seg[0][1] + (seg[1][1] - seg[0][1]) * frac
                for off in (16, -16 - wgt, 28, -28 - wgt):
                    if free(seg[0][0] + off, cy0):
                        spot = (seg[0][0] + off, cy0)
                        break
            if spot:
                break
        if not spot:
            print('라벨 자리 없음:', f['label'])
            continue
        lx, ly = spot
        taken.append((lx - 4, ly - 12, lx + wgt + 4, ly + (len(lines) - 1) * 14 + 4))
        labels.append((lx, ly, lines, kind))

    for i, lab in enumerate(rowlab):           # 행 라벨은 카드보다 먼저 깔아 둔다
        if not lab:
            continue
        yy = snap(PAD + 28 + i * (CH + GY)) + CH / 2 + 4
        s.append('<text class="mp-rowlab" x="%d" y="%d">%s</text>' % (PAD, yy, esc(lab)))
    for name, (x, y, w, h) in pos.items():
        a = actors.get(name, {})
        kick = a.get('kicker', '')
        if kick:
            kw = measure(kick, 10.0) + 10
            s.append('<rect class="mp-kickbg" x="%d" y="%d" width="%d" height="14" rx="3"/>'
                     % (x - 2, y - 21, kw))
            s.append('<text class="mp-kick" x="%d" y="%d">%s</text>' % (x + 2, y - 9, esc(kick)))
        s.append('<rect class="mp-card%s" x="%d" y="%d" width="%d" height="%d" rx="10"/>'
                 % (' on' if a.get('accent') else '', x, y, w, h))
        s.append('<text class="mp-name" x="%d" y="%d">%s</text>' % (x + 18, y + 34, esc(name)))
        dy = y + 58
        for line in a.get('desc', []):
            for ln in wrap(line, 13.0, w - 36)[:2]:
                s.append('<text class="mp-desc" x="%d" y="%d">%s</text>' % (x + 18, dy, esc(ln)))
                dy += 18

    for lx, ly, lines, kind in labels:          # 글자는 카드 위에 오도록 마지막에 그린다
        cls = ' cash' if kind == 'cash' else ''
        for i, ln in enumerate(lines):
            s.append('<text class="mp-lab%s" x="%d" y="%d">%s</text>'
                     % (cls, lx, ly + i * 14, esc(ln)))

    svg = '<svg viewBox="0 0 %d %d" role="img">%s</svg>' % (W, Hh, ''.join(s))
    def _mark(cls):
        return ('<svg viewBox="0 0 30 10">%s<path class="mp-flow %s" d="M0,5 L24,5"/></svg>'
                % (DEFS, cls))

    legend = ('<div class="mp-legend">'
              '<span>%s 돈이 흐른다</span><span>%s 물건·용역·의무가 간다</span>'
              '<span>%s 조건부 지원(부도 뒤에만)</span><span>①②③ 일어난 차례</span></div>'
              % (_mark('cash'), _mark(''), _mark('cond')))
    sub = ''.join('<div>%s</div>' % esc(t) for t in spec.get('sub', []))
    notes = list(spec.get('notes') or ([spec['note']] if spec.get('note') else []))
    if rail_notes:
        notes = ['바깥 레일로 돌아가는 선 — ' + ' · '.join(rail_notes)] + notes
    if caption:
        notes = notes + [caption]
    note = ''.join('<p class="mp-note">%s</p>' % esc(t) for t in notes)
    brand = ''      # 서명 바는 안 그린다 — 카드에 이미 출처 줄이 있다
    return ('<figure class="mermap"><h3>%s</h3><div class="mp-sub">%s</div>%s'
            '<div class="mp-scroll">%s</div>%s%s</figure>'
            % (esc(spec.get('headline', '')), sub, legend, svg, note, brand))


# ── 세로 스택 — Epoch 카드 그림에서 되읽은 배치 ──────────────────────────────
def _order_stack(actors, flows):
    """돈이 도는 순서대로 세운다. 화살표를 따라 위상 정렬하고, 못 잇는 것은 명세 순서."""
    names = list(actors)
    nxt = collections.defaultdict(list)
    indeg = {n: 0 for n in names}
    for f in flows:
        if f['from'] in indeg and f['to'] in indeg and f['from'] != f['to']:
            nxt[f['from']].append(f['to'])
            indeg[f['to']] += 1
    out, seen = [], set()
    q = [n for n in names if indeg[n] == 0] or names[:1]
    while q:
        n = q.pop(0)
        if n in seen:
            continue
        seen.add(n)
        out.append(n)
        for m in nxt[n]:
            indeg[m] -= 1
            if indeg[m] == 0:
                q.append(m)
    out += [n for n in names if n not in seen]
    return out


def stack_render(spec, caption=''):
    """세로 등뼈 + 옆가지 + 묶음. 주체가 많아도 한 줄이 흐름을 쥐고 나머지는 옆에 붙는다.

    등뼈  stackOrder에 든 주체. 위에서 아래로 돈·물건이 도는 차례다
    옆가지 actors[이름]['side'] = 'left'|'right' 와 'attach' = 붙을 등뼈 주체.
          준공 지원·신용 지원처럼 흐름에 끼어 있지 않고 옆에서 받쳐 주는 쪽이다
    묶음  spec['groups'] = [{label, members}] — 한 판 안에 있는 회사들을 둘러친다

    자유 배치를 버리면 꺾임·겹침·간격 문제가 생길 자리가 없다 —
    `docs/카드 도해 — 그림에서 되읽은 규칙.md` 1절."""
    actors, flows = spec['actors'], spec['flows']
    sides = {n: a for n, a in actors.items() if a.get('side')}
    order = [n for n in (spec.get('stackOrder') or _order_stack(actors, flows))
             if n not in sides]
    idx0 = {n: i for i, n in enumerate(order)}
    # 레일 수는 **그리는 순서**로 센다 — 명세 순서로 세면 레일이 모자라 카드 위로 올라간다
    n_rail = sum(1 for f in flows
                 if f['from'] in idx0 and f['to'] in idx0
                 and abs(idx0[f['from']] - idx0[f['to']]) > 1)
    BW, PAD, GAP, LABW = 420, 24, 66, 168
    SW, SGAP = 250, 46                     # 옆가지 상자 폭과 등뼈에서 떨어진 거리
    RAIL = max(44, 34 + n_rail * 30)
    right = [n for n, a in sides.items() if a.get('side') != 'left']
    left = [n for n, a in sides.items() if a.get('side') == 'left']
    W = (PAD * 2 + RAIL + BW + (SW + SGAP if right else LABW)
         + (SW + SGAP if left else 0))
    XOFF = (SW + SGAP) if left else 0       # 왼쪽 옆가지가 있으면 등뼈를 그만큼 민다

    # 상자 높이는 줄 수가 정한다
    boxes, y = {}, PAD + 46
    for name in order:
        a = actors.get(name, {})
        lines = []
        for d in a.get('desc', []):
            lines += wrap(d, 13.0, BW - 36)[:2]
        h = 30 + 18 * len(lines) + 10
        boxes[name] = (PAD + RAIL + XOFF, y, BW, h, lines)
        y += h + GAP
    Hh = y - GAP + PAD + 8

    idx = {n: i for i, n in enumerate(order)}
    s = [DEFS]
    grouped_top = set()
    for g in spec.get('groups', []):    # 묶음 — 선보다 먼저 깔아야 채움이 선을 안 덮는다
        mem = [boxes[m] for m in g.get('members', []) if m in boxes]
        if not mem:
            continue
        gx = min(m[0] for m in mem) - 16
        gy = min(m[1] for m in mem) - 34
        gx2 = max(m[0] + m[2] for m in mem) + 16
        gy2 = max(m[1] + m[3] for m in mem) + 16
        s.append('<rect class="mp-group" x="%d" y="%d" width="%d" height="%d" rx="12"/>'
                 % (gx, gy, gx2 - gx, gy2 - gy))
        # 이름은 오른쪽 끝에 붙인다 — 왼쪽은 위에서 내려오는 화살표가 지나는 자리다
        s.append('<text class="mp-gname" x="%d" y="%d" text-anchor="end">%s</text>'
                 % (gx2 - 14, gy + 21, esc(g.get('label', ''))))
        grouped_top |= {m for m in g.get('members', []) if m in boxes}
    rail_notes = []      # 바깥 레일로 돈 선은 이름을 그림 아래 한 줄로 모은다
    rail_k = 0                       # 레일은 선마다 다른 자리에 세운다 — 한 자리에 몰면 겹친다
    # 화살표 — 붙어 있으면 사이 여백에 곧게, 건너뛰면 왼쪽 레일로
    for f in flows:
        if f['from'] not in boxes or f['to'] not in boxes:
            continue
        i, j = idx[f['from']], idx[f['to']]
        ax, ay, aw, ah, _ = boxes[f['from']]
        bx, by, bw, bh, _ = boxes[f['to']]
        kind = f.get('kind', 'svc')
        cls = 'cash' if kind == 'cash' else ('cond' if kind == 'cond' else '')
        lab = f['label']
        if j == i + 1:                       # 바로 아래로
            x = ax + BW * 0.28
            s.append('<path class="mp-flow %s" d="M%d,%d L%d,%d"/>'
                     % (cls, x, ay + ah + 2, x, by - 5))
            s.append('<text class="mp-lab %s" x="%d" y="%d">%s</text>'
                     % (cls, x + 20, ay + ah + GAP * 0.38, esc(lab)))
        elif j == i - 1:                     # 바로 위로 되돌아간다
            x = ax + BW * 0.72
            s.append('<path class="mp-flow %s" d="M%d,%d L%d,%d"/>'
                     % (cls, x, ay - 2, x, by + bh + 5))
            s.append('<text class="mp-lab %s" x="%d" y="%d" text-anchor="end">%s</text>'
                     % (cls, x - 20, by + bh + GAP * 0.78, esc(lab)))
        else:                                # 건너뛰는 선은 판 바깥 레일로
            rx = PAD + 16 + rail_k * 30
            rail_k += 1
            y1 = ay + ah / 2 + (rail_k % 5 - 2) * 7
            y2 = by + bh / 2 + (rail_k % 5 - 2) * 7
            s.append('<path class="mp-flow %s" d="M%d,%d L%d,%d L%d,%d L%d,%d"/>'
                     % (cls, ax - 2, y1, rx, y1, rx, y2, bx - 5, y2))
            # 레일이 여럿이면 세로 라벨이 다른 레일의 가로 구간을 밟는다.
            # 하나뿐일 때만 옆에 세우고, 여럿이면 이름을 그림 아래 한 줄로 모은다.
            rail_notes.append('%s → %s: %s' % (f['from'], f['to'], lab))

    busy_right = {a.get('attach') for a in sides.values() if a.get('side') != 'left'}
    for name, a in sides.items():           # 옆가지 — 등뼈 옆에 붙는다
        at = a.get('attach')
        if at not in boxes:
            continue
        bx, by_, bw, bh, _l = boxes[at]
        lines = []
        for d in a.get('desc', []):
            lines += wrap(d, 12.5, SW - 32)[:3]
        h = 30 + 17 * len(lines) + 8
        yy = by_ + (bh - h) / 2
        xx = (bx + bw + SGAP) if a.get('side') != 'left' else (bx - SGAP - SW)
        s.append('<g class="mp-box" data-a="%s">' % esc(name))
        s.append('<text class="mp-rowlab" x="%d" y="%d">%s</text>'
                 % (xx, yy - 9, esc(a.get('kicker', ''))))
        s.append('<rect class="mp-card%s" x="%d" y="%d" width="%d" height="%d" rx="9"/>'
                 % (' on' if a.get('accent') else '', xx, yy, SW, h))
        s.append('<text class="mp-name" x="%d" y="%d">%s</text>' % (xx + 16, yy + 25, esc(name)))
        for i, ln in enumerate(lines):
            s.append('<text class="mp-desc" x="%d" y="%d">%s</text>'
                     % (xx + 16, yy + 46 + i * 17, esc(ln)))
        s.append('</g>')
        # 옆가지가 등뼈에 대는 선 — 짧게 곧게. 종류는 그 옆가지의 kind가 정한다
        kind = a.get('kind', 'cond')
        cls = 'cash' if kind == 'cash' else ('cond' if kind == 'cond' else '')
        y_mid = yy + h / 2
        if a.get('side') != 'left':
            s.append('<path class="mp-flow %s" d="M%d,%d L%d,%d"/>'
                     % (cls, xx - 4, y_mid, bx + bw + 4, y_mid))
        else:
            s.append('<path class="mp-flow %s" d="M%d,%d L%d,%d"/>'
                     % (cls, xx + SW + 4, y_mid, bx - 4, y_mid))

    for name in order:
        x, yy, w, h, lines = boxes[name]
        a = actors.get(name, {})
        s.append('<g class="mp-box" data-a="%s">' % esc(name))
        s.append('<rect class="mp-card%s" x="%d" y="%d" width="%d" height="%d" rx="9"/>'
                 % (' on' if a.get('accent') else '', x, yy, w, h))
        s.append('<text class="mp-name" x="%d" y="%d">%s</text>' % (x + 18, yy + 26, esc(name)))
        for i, ln in enumerate(lines):
            s.append('<text class="mp-desc" x="%d" y="%d">%s</text>'
                     % (x + 18, yy + 48 + i * 18, esc(ln)))
        if a.get('kicker'):
            if name in busy_right:           # 옆가지가 도랑을 쓰고 있으면 상자 위로
                s.append('<text class="mp-rowlab" x="%d" y="%d">%s</text>'
                         % (x, yy - 9, esc(a['kicker'])))
            else:                            # 아니면 오른쪽 도랑에
                s.append('<text class="mp-rowlab" x="%d" y="%d">%s</text>'
                         % (x + w + 16, yy + 26, esc(a['kicker'])))
        s.append('</g>')

    svg = '<svg viewBox="0 0 %d %d" role="img">%s</svg>' % (W, Hh, ''.join(s))
    legend = ('<div class="mp-legend">'
              '<span>%s 돈이 흐른다</span><span>%s 물건·물량·의무가 간다</span>'
              '<span>%s 조건이 맞을 때만</span></div>'
              % (_mark_cash(), _mark_svc(), _mark_cond()))
    sub = ''.join('<div>%s</div>' % esc(t) for t in spec.get('sub', []))
    notes = list(spec.get('notes') or ([spec['note']] if spec.get('note') else []))
    if rail_notes:
        notes = ['바깥 레일로 돌아가는 선 — ' + ' · '.join(rail_notes)] + notes
    if caption:
        notes = notes + [caption]
    note = ''.join('<p class="mp-note">%s</p>' % esc(t) for t in notes)
    return ('<figure class="mermap"><h3>%s</h3><div class="mp-sub">%s</div>%s'
            '<div class="mp-scroll">%s</div>%s</figure>'
            % (esc(spec.get('headline', '')), sub, legend, svg, note))


def _mark(cls):
    return ('<svg viewBox="0 0 30 10">%s<path class="mp-flow %s" d="M0,5 L24,5"/></svg>'
            % (DEFS, cls))


def _mark_cash():
    return _mark('cash')


def _mark_svc():
    return _mark('')


def _mark_cond():
    return _mark('cond')
