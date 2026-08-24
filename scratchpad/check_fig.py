# -*- coding: utf-8 -*-
"""도해 안에서 글자가 겹치거나 선에 깔리는지 본다.

눈으로 보고 「안 겹친다」고 보고했다가 두 번 틀렸다. 처음에는 글자끼리만 재서
✕ 줄과 범례가 같은 높이인 것을 놓쳤고, 그다음에는 글자끼리는 봤는데 선을 안 봐서
갈고리가 「왜 줬나」 줄을 가로지르는 것을 놓쳤다. 그래서 기계로 센다.

  PYTHONIOENCODING=utf-8 python scratchpad/check_fig.py            전체
  PYTHONIOENCODING=utf-8 python scratchpad/check_fig.py 세계        제목에 그 말이 든 도해만

보는 것 넷이다.

  글자끼리 겹침   같은 높이(10px 안)에서 가로 구간이 물린다
  선에 깔림      가로선·세로선이 글자 상자를 지난다
  가로 넘침      viewBox 밖으로 나간다
  세로 넘침      viewBox 아래로 나간다
  칸 밖으로 삐짐  글자가 제가 든 네모보다 넓다

글자 폭은 한 글자 9px로 어림한다. 실제 렌더링과 다르지만 겹침을 잡기에는 넉넉하다.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scratchpad'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8', line_buffering=True)

CH = 9.0            # 한 글자 폭 어림
ASC, DESC = 9.0, 3.0    # 글자 상자의 위·아래 여유. 두 줄 라벨이 14px 간격이라
                        # 이보다 키우면 정상 배치가 겹침으로 잡힌다
TEXT = re.compile(r'<text x="(-?[\d.]+)" y="(-?[\d.]+)"([^>]*)>([^<]*)<')
VIEW = re.compile(r'viewBox="0 0 ([\d.]+) ([\d.]+)"')
PATH = re.compile(r'<path d="([^"]+)"([^>]*)/>')
RECT = re.compile(r'<rect x="(-?[\d.]+)" y="(-?[\d.]+)" width="([\d.]+)" height="([\d.]+)"')
MOVE = re.compile(r'[ML](-?[\d.]+)[ ,](-?[\d.]+)')


def boxes(svg):
    """글자 하나하나의 상자. (x0, x1, y0, y1, 글)"""
    out = []
    for m in TEXT.finditer(svg):
        x, y, attr, txt = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
        if not txt.strip():
            continue
        w = len(txt) * CH
        x0 = x - w / 2 if 'middle' in attr else (x - w if 'end' in attr else x)
        out.append((x0, x0 + w, y - ASC, y + DESC, txt))
    return out


def rects(svg):
    """네모 하나하나. (x0, x1, y0, y1)"""
    out = []
    for m in RECT.finditer(svg):
        x, y, w, h = (float(m.group(i)) for i in (1, 2, 3, 4))
        out.append((x, x + w, y, y + h))
    return out


def segments(svg):
    """가로·세로 선분만 추린다. 지도 윤곽처럼 점이 많은 path는 건너뛴다."""
    out = []
    for m in PATH.finditer(svg):
        d, attr = m.group(1), m.group(2)
        pts = [(float(a), float(b)) for a, b in MOVE.findall(d)]
        if len(pts) > 12 or 'class="body"' in attr or 'class="cell"' in attr \
                or 'class="fat"' in attr:
            continue                     # 나라·주 윤곽은 대상이 아니다
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            if abs(y1 - y2) < 0.5 or abs(x1 - x2) < 0.5:
                out.append((min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)))
    return out


def hits(svg):
    bad = []
    bs = boxes(svg)
    vm = VIEW.search(svg)
    vw, vh = (float(vm.group(1)), float(vm.group(2))) if vm else (640.0, 1e9)
    for x0, x1, y0, y1, txt in bs:
        if x0 < -1 or x1 > vw + 1:
            bad.append('가로 넘침 %.0f..%.0f  %s' % (x0, x1, txt[:28]))
        if y1 > vh + 1:
            bad.append('세로 넘침 y=%.0f  %s' % (y1, txt[:28]))
    for i in range(len(bs)):
        for j in range(i + 1, len(bs)):
            a, b = bs[i], bs[j]
            if a[0] < b[1] and b[0] < a[1] and a[2] < b[3] and b[2] < a[3]:
                bad.append('글자끼리 겹침  %s | %s' % (a[4][:18], b[4][:18]))
    # 글자가 제가 든 네모보다 넓으면 옆 칸을 침범한다. 26px 짜리 칸에 「남는 용량」을
    # 넣었다가 걸렸다(2026-08-24) — 겹침 검사만으로는 이게 안 잡힌다.
    for x0, x1, y0, y1, txt in bs:
        cx = (x0 + x1) / 2
        for rx0, rx1, ry0, ry1 in rects(svg):
            if rx0 <= cx <= rx1 and ry0 <= (y0 + y1) / 2 <= ry1:
                if x0 < rx0 - 2 or x1 > rx1 + 2:
                    bad.append('칸 밖으로 삐짐 칸 %.0f..%.0f  %s' % (rx0, rx1, txt[:28]))
    for sx0, sx1, sy0, sy1 in segments(svg):
        for x0, x1, y0, y1, txt in bs:
            if sx0 < x1 and x0 < sx1 and sy0 < y1 and y0 < sy1:
                bad.append('선에 깔림 (%.0f,%.0f)-(%.0f,%.0f)  %s'
                           % (sx0, sy0, sx1, sy1, txt[:28]))
    return bad


# 도해를 가진 생성기를 여기 적는다. 빠뜨리면 그 장은 검사를 통째로 안 받는다 —
# 2026-08-23에 수도리무브 도해 서른 장이 이 목록에 없어서 한 번도 안 걸러졌다.
GENERATORS = ['gen_industry_dashboard', 'gen_sudoremove_dashboard', 'gen_glossary',
              'gen_report_dashboard']


def all_figs():
    import importlib
    out = []
    for name in GENERATORS:
        mod = importlib.import_module(name)
        out += [(c['title'], f) for c in getattr(mod, 'CARDS', ()) for f in c.get('figs', ())]
        # 카드가 아니라 보고서 층에 실린 도해. 이름을 REPORT_FIGS 로 둔 것은
        # 수도리무브 생성기가 EXTRA_FIGS 를 다른 뜻으로 이미 쓰고 있어서다.
        # 카드가 아니라 보고서 층에 실린 도해. CARDS만 걷으면 검사를 통째로 빠져나간다 —
        # 4장짜리 에이전트 보고서가 그렇게 한 번도 안 걸러질 뻔했다(2026-08-24).
        out += [(name, f) for f in getattr(mod, 'REPORT_FIGS', ())]
    return out


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    figs = all_figs()
    fails = 0
    for _card, (_anchor, title, svg, _cap) in figs:
        if want and want not in title:
            continue
        bad = hits(svg)
        print('%s %s' % ('FAIL' if bad else 'OK  ', title), file=OUT)
        for b in bad:
            print('       ! %s' % b, file=OUT)
        fails += bool(bad)
    print('\nFAIL %d건' % fails, file=OUT)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
