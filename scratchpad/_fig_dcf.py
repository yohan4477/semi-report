# -*- coding: utf-8 -*-
"""DCF 대장 — 내재가치가 주가에서 얼마나 떨어져 있나, 그리고 다시 계산했을 때 어디로 갔나.

재료는 data/dcf_ledger.json 한 곳이다. 새 평가 편이 들어오면 rows에 한 줄 더하고
이 파일을 다시 돌리면 그림과 표가 같이 갱신된다.

규칙(insight-figure):
  - 점 자리는 원문에 적힌 괴리율 그대로다. 눈금도 관측 최저·최고만 세운다.
  - 세로 기준선에는 숫자를 안 쓴다 — 「주가」라고만 적는다. 0%는 원문에 없는 값이다.
  - 같은 회사를 두 번 계산한 줄만 화살표를 단다. 나머지는 점 하나다.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'dcf_ledger.json')

W, LEFT, RIGHT, TOP, ROW = 560, 152, 544, 40, 27


def load():
    return json.load(io.open(DATA, encoding='utf-8'))['rows']


def signed(r):
    return r['gap'] if r['dir'] == '위' else -r['gap']


def by_company(rows):
    """회사별로 묶고 평가일 순으로 세운다 — 줄 하나가 회사 하나다."""
    out = {}
    for r in rows:
        out.setdefault(r['company'], []).append(r)
    for v in out.values():
        v.sort(key=lambda r: r['date'])
    return sorted(out.items(), key=lambda kv: signed(kv[1][-1]))


def svg():
    rows = load()
    groups = by_company(rows)
    lo = min(signed(r) for r in rows)
    hi = max(signed(r) for r in rows)
    pad = (hi - lo) * 0.10
    dlo, dhi = lo - pad, hi + pad
    span = RIGHT - LEFT

    def x(v):
        return LEFT + (v - dlo) / (dhi - dlo) * span

    bottom = TOP + ROW * len(groups) + 30
    h = ['<svg viewBox="0 0 %d %d" role="img" aria-label="회사별 DCF 내재가치가 주가에서 '
         '얼마나 떨어져 있는지, 다시 계산한 회사는 어디로 옮겨갔는지">' % (W, bottom)]
    h.append('<defs><marker id="dcfArrow" markerWidth="8" markerHeight="8" refX="7" refY="4" '
             'orient="auto"><path d="M0,1 L7,4 L0,7 z" class="arrowhead"/></marker></defs>')

    x0 = x(0)
    h.append('<line class="zero" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>'
             % (x0, TOP - 16, x0, bottom - 26))
    h.append('<text x="%.1f" y="%d" class="t-head" text-anchor="middle">주가</text>'
             % (x0, TOP - 22))
    for v, anc in ((lo, 'start'), (hi, 'end')):
        h.append('<text x="%.1f" y="%d" class="t-sub" text-anchor="%s">%g%% %s</text>'
                 % (x(v), bottom - 8, anc, abs(v), '아래' if v < 0 else '위'))

    for i, (comp, rs) in enumerate(groups):
        y = TOP + i * ROW
        h.append('<text x="8" y="%d" class="t-step">%s</text>' % (y + 4, comp))
        last = rs[-1]
        if len(rs) > 1:
            first = rs[0]
            h.append('<circle cx="%.1f" cy="%d" r="5" class="was"/>' % (x(signed(first)), y))
            h.append('<line class="move" x1="%.1f" y1="%d" x2="%.1f" y2="%d" '
                     'marker-end="url(#dcfArrow)"/>'
                     % (x(signed(first)) + 7, y, x(signed(last)) - 9, y))
        cls = 'good' if signed(last) > 0 else 'bad'
        h.append('<circle cx="%.1f" cy="%d" r="6" class="%s"/>' % (x(signed(last)), y, cls))
        lx, anc = (x(signed(last)) + 11, 'start') if signed(last) < 60 else \
                  (x(signed(last)) - 11, 'end')
        h.append('<text x="%.1f" y="%d" class="t-sub" text-anchor="%s">%s</text>'
                 % (lx, y + 4, anc, last['value']))
    h.append('</svg>')
    return ''.join(h)


CSS = """
  .uc-fig .zero { stroke:var(--ink-3); stroke-width:1.2; stroke-dasharray:5 4; }
  .uc-fig .was  { fill:none; stroke:var(--ink-3); stroke-width:1.6; }
  .uc-fig .move { stroke:var(--ink-3); stroke-width:1.4; }
  .uc-fig .arrowhead { fill:var(--ink-3); }
"""


def table():
    rows = sorted(load(), key=lambda r: r['date'], reverse=True)
    body = [[r['date'], r['company'], r['value'], '%g%% %s' % (r['gap'], r['dir'])]
            for r in rows]
    return ('평가한 순서대로', ['평가일', '회사', '내재가치', '주가 대비'], body)


def redone():
    """두 번 계산한 회사만 — 값이 어디서 어디로 갔는지."""
    out = []
    for comp, rs in by_company(load()):
        if len(rs) > 1:
            out.append((comp, rs[0], rs[-1]))
    return out


FIG = (1, '내재가치가 주가에서 떨어진 거리',
       svg(),
       '점 하나가 평가 한 편이다. 세로 점선이 주가이고, 오른쪽으로 갈수록 계산값이 주가보다 '
       '높다는 뜻이다. 빈 동그라미에서 화살표가 나간 두 줄은 <b>같은 회사를 다시 계산한 것</b>이다 — '
       '현대모비스는 주가보다 <b>50.7% 위</b>에서 <b>4.5% 위</b>로 내려왔고, 효성중공업은 '
       '<b>64.8% 아래</b>에서 <b>30.4% 아래</b>로 올라왔다. 눈금은 이 표에 실제로 적힌 최저·최고 '
       '두 값만 세웠다.')

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check_fig
    print('배치:', check_fig.hits(FIG[2]) or 'FAIL 0건')
    for c, a, b in redone():
        print('%s: %s %g%% %s → %s %g%% %s' % (c, a['date'], a['gap'], a['dir'],
                                               b['date'], b['gap'], b['dir']))
