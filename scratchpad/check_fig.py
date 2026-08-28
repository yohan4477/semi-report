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


LINE = re.compile('<line x1="(-?[0-9.]+)" y1="(-?[0-9.]+)" x2="(-?[0-9.]+)" y2="(-?[0-9.]+)"')
# AI Engineer 도해는 판 안 글자를 본문과 같은 .95rem으로 낸다(다른 장은 9px 어림).
# 한 벌로 재면 폭을 절반으로 어림해 겹침을 놓친다. 글자 붓 이름으로 골라 잰다.
CLASS_CH = {"fig-b": 15.6, "fig-st": 15.6, "fig-hd": 15.6, "fig-e": 15.6, "fig-lg": 15.6}


def boxes(svg):
    """글자 하나하나의 상자. (x0, x1, y0, y1, 글)"""
    out = []
    for m in TEXT.finditer(svg):
        x, y, attr, txt = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
        if not txt.strip():
            continue
        ch, asc, desc = CH, ASC, DESC
        for cls, cw in CLASS_CH.items():
            if 'class="' + cls + '"' in attr:
                ch, asc, desc = cw, cw * 0.77, cw * 0.3
                break
        w = len(txt) * ch
        x0 = x - w / 2 if 'middle' in attr else (x - w if 'end' in attr else x)
        out.append((x0, x0 + w, y - asc, y + desc, txt))
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
    # <line>도 센다. AI Engineer 도해는 화살표와 생명선을 전부 <line>으로 그려서
    # <path>만 보던 동안 선이 글자를 가로질러도 통과했다.
    for m in LINE.finditer(svg):
        x1, y1, x2, y2 = (float(v) for v in m.groups())
        if abs(y1 - y2) < 0.5 or abs(x1 - x2) < 0.5:
            out.append((min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)))
    return out


def rect_edges(svg):
    """네모의 네 변도 선으로 센다.

    segments()가 <path>만 봐서, 상자 테두리나 묶음 컨테이너 위에 얹힌 글자를 놓쳤다.
    2026-08-25에 두 칸 대조의 역할 라벨이 양쪽 칸 테두리를 물고 있었는데 검사기가
    통과시켰다. 사람이 눈으로 지키지 말고 여기서 막는다."""
    out = []
    for m in RECT.finditer(svg):
        x, y, w, h = [float(v) for v in m.groups()]
        out += [(x, x + w, y, y), (x, x + w, y + h, y + h),
                (x, x, y, y + h), (x + w, x + w, y, y + h)]
    return out


# 판 위에서 쓰면 안 되는 줄임말. 단위는 풀어 적는다 — 도해는 본문의 각주가 아니라
# 그 자체로 읽혀야 한다
SHORT = re.compile(r'\d\s*(Gb|GB|Tb|TB|Mb|MB|kW|MW|GHz|MHz|㎿|㎾)\b')
# 문장이 끊긴 줄. **격조사로 끝나면** 그 줄만으로는 아무 뜻이 없다 —
# 「기준이 운영자 / 셈에서 사용자 / 경험으로 옮겼다」가 그랬다.
# 「~고」·「~며」로 끝나는 줄은 절이 끝난 자리라 잡지 않는다
CUT = re.compile(r'(이|가|을|를|의|에|에서|으로|로|와|과|보다|부터|까지|에게|한테)$')
# 이 장은 규칙을 세우며 다시 그리는 중이라 줄임말도 FAIL 로 막는다.
# 나머지 장은 이 규칙보다 먼저 그려졌으니 세기만 한다
STRICT_FIG = ('오픈AI 할라페뇨',)


def text_hits(svg, strict=True):
    """글자 자체를 본다 — 줄임말과 잘린 줄."""
    bad = []
    items = [(float(m.group(1)), float(m.group(2)), m.group(3).strip())
             for m in re.finditer(r'<text[^>]*x="([-\d.]+)"[^>]*y="([-\d.]+)"[^>]*>([^<]*)<',
                                  svg)]
    if strict:
        for _x, _y, t in items:
            if SHORT.search(t):
                bad.append('줄임말을 판 위에 썼다 — 풀어 적는다: %s' % t[:32])
    # 같은 x 에 16~24픽셀 간격으로 이어 선 줄들이 조사로 끝나면 문장을 자른 것이다
    by_x = {}
    for x, y, t in items:
        by_x.setdefault(round(x), []).append((y, t))
    # 두 줄짜리 라벨은 정상이다 — 주어를 위에 술어를 아래에 두는 것은 흔한 배치다.
    # 잘린 것은 **세 줄 이상이 격조사로 이어지는** 경우다. 「기준이 운영자 / 셈에서
    # 사용자 / 경험으로 옮겼다」가 그랬고, 그때 한 줄씩은 아무 뜻이 없었다
    if strict:
        for _x, rows in by_x.items():
            rows.sort()
            for i in range(len(rows) - 2):
                (y0, t0), (y1, t1), (y2, t2) = rows[i], rows[i + 1], rows[i + 2]
                if not (12 <= y1 - y0 <= 24 and 12 <= y2 - y1 <= 24):
                    continue
                if CUT.search(t0) and CUT.search(t1):
                    bad.append('한 문장을 세 줄로 잘랐다 — 한 줄에 한 뜻: %s / %s / %s'
                               % (t0[:16], t1[:16], t2[:16]))
    return bad


def hits(svg, strict=True):
    bad = text_hits(svg, strict)
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
    for sx0, sx1, sy0, sy1 in rect_edges(svg):
        for x0, x1, y0, y1, txt in bs:
            # 글자가 제가 든 상자 안에 있는 것은 정상이다 — 테두리를 물었을 때만 잡는다
            if sx0 - 1 < x1 and x0 < sx1 + 1 and sy0 - 1 < y1 and y0 < sy1 + 1:
                bad.append('네모 테두리에 깔림 (%.0f,%.0f)-(%.0f,%.0f)  %s'
                           % (sx0, sy0, sx1, sy1, txt[:28]))
    return bad


# 도해를 가진 생성기를 여기 적는다. 빠뜨리면 그 장은 검사를 통째로 안 받는다 —
# 2026-08-23에 수도리무브 도해 서른 장이 이 목록에 없어서 한 번도 안 걸러졌다.
GENERATORS = ['gen_industry_dashboard', 'gen_sudoremove_dashboard', 'gen_glossary',
              'gen_report_dashboard', 'gen_epoch_dashboard', 'gen_semidoped_dashboard']


def all_figs():
    import importlib
    out = []
    for name in GENERATORS:
        mod = importlib.import_module(name)
        out += [(c['title'], f) for c in getattr(mod, 'CARDS', ()) for f in c.get('figs', ())]
        # 보고서 꼴 카드는 그림을 figs 키가 아니라 report 블록 안에 둔다. 여기를 안 걷어서
        # 상자 테두리에 깔린 글자가 그대로 나갔다(2026-08-29 할라페뇨). anchor 자리는
        # 보고서 꼴에 없으므로 0 을 채운다
        for c in getattr(mod, 'CARDS', ()):
            for kind, val in c.get('report', ()):
                if kind == 'fig':
                    out.append((c['title'], (0,) + tuple(val)))
        # 카드가 아니라 보고서 층에 실린 도해. 이름을 REPORT_FIGS 로 둔 것은
        # 수도리무브 생성기가 EXTRA_FIGS 를 다른 뜻으로 이미 쓰고 있어서다.
        # 카드가 아니라 보고서 층에 실린 도해. CARDS만 걷으면 검사를 통째로 빠져나간다 —
        # 4장짜리 에이전트 보고서가 그렇게 한 번도 안 걸러질 뻔했다(2026-08-24).
        out += [(name, f) for f in getattr(mod, 'REPORT_FIGS', ())]
    # AI Engineer 도해는 생성기가 아니라 aie_figs가 들고 있고, 카드가 아니라
    # 글의 프런트매터가 어느 그림을 부를지 정한다. GENERATORS로는 안 걸린다.
    aie = importlib.import_module('aie_figs')
    for vid, items in getattr(aie, 'FIGS', {}).items():
        out += [(vid, f) for f in items]
    for vid, named in getattr(aie, 'RFIGS', {}).items():
        out += [(vid, (0,) + f) for f in named.values()]
    return out


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    figs = all_figs()
    fails = 0
    for _card, (_anchor, title, svg, _cap) in figs:
        if want and want not in title:
            continue
        bad = hits(svg, any(k in _card for k in STRICT_FIG))
        print('%s %s' % ('FAIL' if bad else 'OK  ', title), file=OUT)
        for b in bad:
            print('       ! %s' % b, file=OUT)
        fails += bool(bad)
    print('\nFAIL %d건' % fails, file=OUT)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
