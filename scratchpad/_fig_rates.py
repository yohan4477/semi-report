# -*- coding: utf-8 -*-
"""미 장기금리 타임라인 — 값이 적힌 날만 찍는 도해와 그 카드.

재료는 data/rates_timeline.json 한 곳에 둔다. 새 원문이 들어오면 rows에 한 줄
더하고 이 파일을 다시 돌리면 그림과 표가 같이 갱신된다.

규칙(insight-figure):
  - 값은 원문에 적힌 것만 찍는다. 범위로 적힌 값은 세로 막대로 그 구간을 그대로
    보이고 가운데 값을 만들어 넣지 않는다.
  - 점을 선으로 잇지 않는다 — 사이 값이 원문에 없다.
  - 같은 날을 두 원문이 다르게 적으면 둘 다 찍고 어긋남으로 표시한다.
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'rates_timeline.json')

W, PAD_L, PAD_R = 560, 58, 26
H30, H10, GAP, TOP = 120, 92, 46, 26


def load():
    return json.load(io.open(DATA, encoding='utf-8'))


def _x(i, n):
    span = W - PAD_L - PAD_R
    return PAD_L + (span / max(n, 1)) * (i + 0.5)


def _y(v, lo, hi, y0, h):
    return y0 + h - (v - lo) / (hi - lo) * h


def observed(rows, key):
    """그 줄들에 실제로 적힌 값만 모은다 — 눈금도 원문에 있는 값으로만 세운다."""
    vs = []
    for r in rows:
        if r.get(key) is not None:
            vs.append(r[key])
        if key == 'y30':
            if r.get('y30_alt') is not None:
                vs.append(r['y30_alt'])
            vs += r.get('y30_range', [])
    return min(vs), max(vs)


def svg():
    d = load()
    rows = d['rows']
    n = len(rows)
    lo30, hi30 = observed(rows, 'y30')
    lo10, hi10 = observed(rows, 'y10')
    y30_0, y10_0 = TOP, TOP + H30 + GAP
    bottom = y10_0 + H10 + 44
    h = ['<svg viewBox="0 0 %d %d" role="img" aria-label="미 30년물과 10년물 국채금리를 '
         '값이 적힌 날만 찍은 타임라인">' % (W, bottom)]

    pads = {}
    for lab, y0, hh, lo, hi in (('30년물', y30_0, H30, lo30, hi30),
                                ('10년물', y10_0, H10, lo10, hi10)):
        m = (hi - lo) * 0.22          # 점이 판 끝에 붙지 않게 그리는 범위만 넓힌다
        pads[lab] = (lo - m, hi + m)
        dlo, dhi = pads[lab]
        h.append('<text x="10" y="%d" class="t-head">%s</text>' % (y0 - 8, lab))
        for v in (lo, hi):
            yy = _y(v, dlo, dhi, y0, hh)
            h.append('<line class="lead-line" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                     % (PAD_L - 8, yy, W - PAD_R, yy))
            h.append('<text x="%d" y="%.1f" class="t-sub" text-anchor="end">%.2f%%</text>'
                     % (PAD_L - 14, yy + 4, v))

    for i, r in enumerate(rows):
        x = _x(i, n)
        if 'y30_range' in r:
            a, b = r['y30_range']
            ya, yb = _y(a, *pads['30년물'], y30_0, H30), _y(b, *pads['30년물'], y30_0, H30)
            h.append('<line class="rng" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                     % (x, ya, x, yb))
            h.append('<text x="%.1f" y="%.1f" class="t-val" text-anchor="middle">%.2f~%.2f</text>'
                     % (x, yb - 10, a, b))
        if r.get('y30') is not None:
            y = _y(r['y30'], *pads['30년물'], y30_0, H30)
            h.append('<circle cx="%.1f" cy="%.1f" r="6" class="bad"/>' % (x, y))
            h.append('<text x="%.1f" y="%.1f" class="t-val" text-anchor="middle">%.2f</text>'
                     % (x, y - 12, r['y30']))
        if r.get('y30_alt') is not None:
            y = _y(r['y30_alt'], *pads['30년물'], y30_0, H30)
            h.append('<circle cx="%.1f" cy="%.1f" r="6" class="alt"/>' % (x, y))
            h.append('<text x="%.1f" y="%.1f" class="t-val alt-t" text-anchor="middle">%.2f</text>'
                     % (x, y - 12, r['y30_alt']))
        if r.get('y10') is not None:
            y = _y(r['y10'], *pads['10년물'], y10_0, H10)
            h.append('<circle cx="%.1f" cy="%.1f" r="6" class="cool"/>' % (x, y))
            h.append('<text x="%.1f" y="%.1f" class="t-val" text-anchor="middle">%.2f</text>'
                     % (x, y - 12, r['y10']))
        h.append('<text x="%.1f" y="%d" class="t-day" text-anchor="middle">%s</text>'
                 % (x, bottom - 22, r['date']))
        h.append('<text x="%.1f" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x, bottom - 6, r['dow']))
        if r.get('event'):
            h.append('<line class="flow" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>'
                     % (x, TOP - 18, x, TOP - 2))
    h.append('</svg>')
    return ''.join(h)


CSS = """
  .uc-fig .rng { stroke:var(--fig-bad,#c2504a); stroke-width:7; stroke-linecap:round; opacity:.55; }
  .uc-fig .alt { fill:none; stroke:var(--fig-bad,#c2504a); stroke-width:2; stroke-dasharray:3 3; }
  .uc-fig .cool { fill:var(--fig-vein,#4a6ec2); }
  .uc-fig text.alt-t { fill:var(--ink-3); }
"""


def table():
    d = load()
    head = ['날짜', '30년물', '10년물', '그날']
    body = []
    for r in d['rows']:
        if 'y30_range' in r:
            v30 = '%.2f~%.2f%%' % tuple(r['y30_range'])
        elif r.get('y30_alt'):
            v30 = '%.2f%% / %.2f%%' % (r['y30'], r['y30_alt'])
        else:
            v30 = '%.2f%%' % r['y30'] if r.get('y30') is not None else '—'
        v10 = '%.2f%%' % r['y10'] if r.get('y10') is not None else '—'
        body.append(['%s(%s)' % (r['date'], r['dow']), v30, v10,
                     r.get('event') or r.get('note') or '—'])
    return ('값이 적힌 날만', head, body)


FIG = (1, '값이 적힌 날만 찍은 타임라인', svg(),
       '위가 30년물, 아래가 10년물이다. 8월 18일 30년물에 점이 둘인 것은 같은 날을 두 원문이 '
       '<b>5.31%</b>와 <b>5.34%</b>로 다르게 적기 때문이고, 8월 19일의 굵은 막대는 그날 값이 '
       '<b>5.18~5.20%</b>라는 구간으로만 적혀 있어서다. 점을 선으로 잇지 않은 것은 하루 사이 값이 '
       '원문에 없기 때문이다. 세로선이 선 날이 되사기 확대를 발표한 날이다.')

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import check_fig
    print('배치:', check_fig.hits(FIG[2]) or 'FAIL 0건')
    for row in table()[2]:
        print(' | '.join(row))
