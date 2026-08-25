# -*- coding: utf-8 -*-
"""글자가 무엇에든 깔렸는지 본다 — check_fig 가 못 보는 자리까지.

check_fig 는 <path> 의 가로·세로 선분과 <rect> 테두리만 센다. 그래서
  · 사선 (로그 그래프의 추세선·계보 화살표)
  · <polyline> (선그래프 계열)
  · <circle> (산점도 표식·지도 버블)
이 세 가지에 깔린 글자를 놓친다. 2026-08-25에 사용자가 눈으로 잡아냈다.

글자 폭은 epoch_fig.w() 로 잰다 — 한글은 글자 크기만큼 넓어서 9px 어림으로는 모자란다.

  PYTHONIOENCODING=utf-8 python scratchpad/check_fig_strict.py
  PYTHONIOENCODING=utf-8 python scratchpad/check_fig_strict.py <그림이름>
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'scripts'))

import epoch_fig as ef  # noqa: E402

TEXT = re.compile(r'<text ([^>]*)>([^<]*)</text>')
NUM = re.compile(r'(-?[\d.]+)')
PATH = re.compile(r'<path d="([^"]+)"([^>]*)/>')
POLY = re.compile(r'<polyline points="([^"]+)"')
CIRC = re.compile(r'<circle ([^>]*)/>')
MOVE = re.compile(r'[ML](-?[\d.]+)[ ,](-?[\d.]+)')
PAD = 1.5           # 이만큼 떨어져 있으면 붙었다고 보지 않는다


def attr(s, name, dflt=None):
    m = re.search(r'%s="([^"]*)"' % name, s)
    return m.group(1) if m else dflt


def fontsize(at):
    m = re.search(r'font-size:([\d.]+)px', at)
    if m:
        return float(m.group(1))
    cls = attr(at, 'class', '') or ''
    if 't-lab' in cls:
        return 16.0
    if 't-role' in cls:
        return 13.0
    return 13.5


def textboxes(svg):
    out = []
    for at, body in TEXT.findall(svg):
        if not body.strip():
            continue
        x, y = float(attr(at, 'x', 0)), float(attr(at, 'y', 0))
        fs = fontsize(at)
        wd = ef.w(body, fs)
        anc = attr(at, 'text-anchor', 'start')
        x0 = x - wd if anc == 'end' else (x - wd / 2 if anc == 'middle' else x)
        out.append((x0, x0 + wd, y - fs * 0.82, y + fs * 0.22, body))
    return out


def segments(svg):
    """사선까지 포함한 모든 선분. 나라 윤곽처럼 점이 아주 많은 것은 뺀다."""
    segs = []
    for d, at in PATH.findall(svg):
        if 'class="body"' in at or 'bx-wrap' in at or 'class="grid"' in at:
            continue
        pts = [(float(a), float(b)) for a, b in MOVE.findall(d)]
        if len(pts) > 40:
            continue                       # 지도 윤곽
        segs += list(zip(pts, pts[1:]))
    for p in POLY.findall(svg):
        v = NUM.findall(p)
        pts = [(float(v[i]), float(v[i + 1])) for i in range(0, len(v) - 1, 2)]
        segs += list(zip(pts, pts[1:]))
    return segs


def circles(svg):
    out = []
    for at in CIRC.findall(svg):
        cx, cy, r = (float(attr(at, k, 0)) for k in ('cx', 'cy', 'r'))
        out.append((cx, cy, r))
    return out



RECT = re.compile(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)"([^>]*)/>')


def panels(svg):
    """글자를 담는 네모 — 상자와 색 딱지. 판을 덮는 큰 면은 뺀다."""
    out = []
    for m in RECT.finditer(svg):
        x, y, wd, ht = (float(m.group(i)) for i in (1, 2, 3, 4))
        if wd < 20 or ht < 20:
            continue
        out.append((x, x + wd, y, y + ht))
    return out


def under_panel(svg):
    """제 상자 밖 글자가 남의 상자에 걸쳤나.

    상자가 글자보다 늦게 그려지면 글자가 그 아래로 숨는다. 상자가 높아졌는데
    아래 주석 자리를 고정해 뒀을 때 이렇게 된다(2026-08-25). 제 상자 안에
    통째로 든 글자는 정상이다 — 걸친 것만 잡는다."""
    bad = []
    ps = panels(svg)
    for x0, x1, y0, y1, txt in textboxes(svg):
        for rx0, rx1, ry0, ry1 in ps:
            if x1 <= rx0 or rx1 <= x0 or y1 <= ry0 or ry1 <= y0:
                continue
            if rx0 - 1 <= x0 and x1 <= rx1 + 1 and ry0 - 1 <= y0 and y1 <= ry1 + 1:
                continue
            bad.append('상자에 걸침 (%.0f..%.0f, %.0f..%.0f)  %s'
                       % (rx0, rx1, ry0, ry1, txt[:30]))
    return bad



def overflow(svg):
    """판 밖으로 나간 글자. check_fig 는 한 글자 9px 로 어림해 13.5px 한글을 못 잡는다."""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    vw, vh = (float(m.group(1)), float(m.group(2))) if m else (640.0, 1e9)
    bad = []
    for x0, x1, y0, y1, txt in textboxes(svg):
        if x0 < -1 or x1 > vw + 1:
            bad.append('판을 넘음 %.0f..%.0f  %s' % (x0, x1, txt[:30]))
        if y1 > vh + 1:
            bad.append('판 아래로 넘음 y=%.0f  %s' % (y1, txt[:30]))
    return bad


def seg_hits_box(p0, p1, box):
    """선분이 글자 상자를 지나는가. 선분을 잘게 끊어 점으로 본다."""
    x0, x1, y0, y1 = box[:4]
    (ax, ay), (bx, by) = p0, p1
    n = max(2, int(max(abs(bx - ax), abs(by - ay)) / 2) + 1)
    for i in range(n + 1):
        t = i / float(n)
        x, y = ax + (bx - ax) * t, ay + (by - ay) * t
        if x0 - PAD < x < x1 + PAD and y0 - PAD < y < y1 + PAD:
            return True
    return False


def hits(svg):
    bad = []
    boxes = textboxes(svg)
    for p0, p1 in segments(svg):
        for b in boxes:
            if seg_hits_box(p0, p1, b):
                bad.append('선에 깔림 (%.0f,%.0f)-(%.0f,%.0f)  %s'
                           % (p0[0], p0[1], p1[0], p1[1], b[4][:30]))
    for cx, cy, r in circles(svg):
        for b in boxes:
            x0, x1, y0, y1 = b[:4]
            nx = min(max(cx, x0), x1)
            ny = min(max(cy, y0), y1)
            if (nx - cx) ** 2 + (ny - cy) ** 2 >= (r + PAD) ** 2:
                continue
            # 동그라미 안에 글자가 통째로 들어 있으면 그 동그라미의 이름표다
            # (지구·행성, 도넛 칸 번호처럼 판 노릇을 하는 자리). 깔린 것이 아니다
            if r >= 12 and x0 >= cx - r and x1 <= cx + r and y0 >= cy - r and y1 <= cy + r:
                continue
            bad.append('동그라미에 깔림 (%.0f,%.0f,r%.1f)  %s' % (cx, cy, r, b[4][:30]))
    bad += under_panel(svg)
    bad += overflow(svg)
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i], boxes[j]
            if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]:
                bad.append('글자끼리 겹침  %s | %s' % (a[4][:20], b[4][:20]))
    return sorted(set(bad))


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    n = 0
    for k, fn in ef.FIGS.items():
        if want and want not in k:
            continue
        h = hits(fn())
        if h:
            n += len(h)
            print('FAIL %s' % k)
            for x in h[:8]:
                print('       ! %s' % x)
            if len(h) > 8:
                print('       ! … 그 밖 %d건' % (len(h) - 8))
    print('\n엄한 검사 FAIL %d건' % n)
    return 1 if n else 0


if __name__ == '__main__':
    sys.exit(main())
