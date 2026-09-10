# -*- coding: utf-8 -*-
"""NVIDIA·AMD·TSMC·ASML 밸류체인 — 여섯 층 흐름도 HTML 생성기.

층: 공급사 → 회사 → 사업부문 → 채널 → 고객 → 최종 수요처
선: 실선 = SEC 공시로 확인, 점선 = 추정·애널리스트 매핑
선은 직각으로만 꺾고, 한 칸을 건너뛰는 선은 판 아래 바깥 레일로 돌린다.
"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 판 치수 ───────────────────────────────────────────────────────────
PAD_L, PAD_R = 14, 14
TOP = 58            # 제목·범례 자리
GAP_Y = 14          # 같은 칸 상자 사이
GUT = 52            # 칸 사이 도랑
LINE_H = 13         # 설명 줄 높이
TITLE_H = 17        # 상자 제목 줄 높이
BOX_PAD = 9
CHAR_W = 6.05       # 한글 11px 기준 근사 폭
DESC_CHAR_W = 5.35  # 설명 9.5px

LAYERS = ['공급사', '회사', '사업부문', '채널', '고객', '최종 수요처']


def wrap(text, width_px, char_w):
    """낱말 사이에서 잘라 줄을 쌓는다."""
    if not text:
        return []
    limit = max(6, int(width_px / char_w))
    out, cur = [], ''
    for w in text.split(' '):
        cand = (cur + ' ' + w).strip()
        if len(cand) <= limit or not cur:
            cur = cand
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    return out


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


class Plate(object):
    """한 장의 흐름도."""

    def __init__(self, title, sub, col_w, foot=None, width=1180, layers=None):
        self.title = title
        self.sub = sub
        self.col_w = col_w              # 칸마다 폭
        self.layers = layers or LAYERS
        self.foot = foot or []
        self.width = width
        self.cols = [[] for _ in col_w]  # 칸마다 상자 목록
        self.edges = []
        self.by_id = {}
        self._x = []
        x = PAD_L
        for w in col_w:
            self._x.append(x)
            x += w + GUT
        self.width = x - GUT + PAD_R

    # 상자 하나. kind: 'plain' | 'hero' | 'group'
    def box(self, col, bid, name, desc=None, kind='plain', children=None, tone=None):
        b = dict(col=col, id=bid, name=name, desc=desc or [], kind=kind,
                 tone=col if tone is None else tone, children=children or [])
        self.cols[col].append(b)
        self.by_id[bid] = b
        return b

    def edge(self, a, b, label=None, dashed=False):
        self.edges.append(dict(a=a, b=b, label=label, dashed=dashed))

    # ── 배치 ────────────────────────────────────────────────────────
    def _measure(self, b, w):
        lines = []
        for d in b['desc']:
            lines += wrap(d, w - 2 * BOX_PAD, DESC_CHAR_W)
        b['_lines'] = lines
        name_lines = wrap(b['name'], w - 2 * BOX_PAD, CHAR_W)
        b['_name'] = name_lines
        h = BOX_PAD + TITLE_H * len(name_lines) + 2 + LINE_H * len(lines) + BOX_PAD
        if b['kind'] == 'group':
            inner_w = w - 16
            ih = 0
            for c in b['children']:
                self._measure(c, inner_w)
                ih += c['_h'] + 8
            h = BOX_PAD + TITLE_H * len(name_lines) + LINE_H * len(lines) + 6 + ih + 8
        b['_h'] = max(h, 30)
        return b['_h']

    def layout(self):
        heights = []
        for ci, col in enumerate(self.cols):
            w = self.col_w[ci]
            tot = 0
            for b in col:
                tot += self._measure(b, w) + GAP_Y
            heights.append(tot - GAP_Y if col else 0)
        self.body_h = max(heights) if heights else 0
        for ci, col in enumerate(self.cols):
            y = TOP + (self.body_h - heights[ci]) / 2.0
            w = self.col_w[ci]
            for b in col:
                b['_x'], b['_y'], b['_w'] = self._x[ci], y, w
                if b['kind'] == 'group':
                    iy = y + BOX_PAD + TITLE_H * len(b['_name']) + \
                        LINE_H * len(b['_lines']) + 6
                    for c in b['children']:
                        c['_x'] = b['_x'] + 8
                        c['_y'] = iy
                        c['_w'] = w - 16
                        c['col'] = b['col']
                        iy += c['_h'] + 8
                y += b['_h'] + GAP_Y
        # 바깥 레일 자리
        self.rail_n = 0
        for e in self.edges:
            a, b = self.by_id[e['a']], self.by_id[e['b']]
            if b['col'] - a['col'] > 1:
                self.rail_n += 1
        self.height = TOP + self.body_h + 16 + self.rail_n * 12 + \
            18 * len(self.foot) + 30

    # ── 그리기 ──────────────────────────────────────────────────────
    def _draw_box(self, b, out):
        x, y, w, h = b['_x'], b['_y'], b['_w'], b['_h']
        cls = {'plain': 'vc-b', 'hero': 'vc-b vc-hero', 'group': 'vc-b vc-grp'}[b['kind']]
        if b['kind'] == 'plain':
            cls += ' vc-L%d' % b['col']
        out.append('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4"/>'
                   % (cls, x, y, w, h))
        ty = y + BOX_PAD + 11
        for ln in b['_name']:
            out.append('<text class="vc-n%s" x="%.1f" y="%.1f">%s</text>'
                       % (' vc-nh' if b['kind'] == 'hero' else '', x + BOX_PAD, ty, esc(ln)))
            ty += TITLE_H
        ty = y + BOX_PAD + TITLE_H * len(b['_name']) + 2
        for ln in b['_lines']:
            ty += 9.5
            out.append('<text class="vc-d" x="%.1f" y="%.1f">%s</text>'
                       % (x + BOX_PAD, ty, esc(ln)))
            ty += LINE_H - 9.5
        for c in b['children']:
            self._draw_box(c, out)

    def _port(self, b, side):
        """상자의 좌우 접점. 그룹의 자식은 자기 자리에서 나간다."""
        y = b['_y'] + b['_h'] / 2.0
        return (b['_x'] + (b['_w'] if side == 'r' else 0), y)

    def render(self):
        self.layout()
        out = []
        out.append('<svg class="vc" viewBox="0 0 %.0f %.0f" width="100%%" '
                   'preserveAspectRatio="xMidYMid meet" role="img">' % (self.width, self.height))
        # 제목·범례
        out.append('<text class="vc-t" x="%d" y="20">%s</text>' % (PAD_L, esc(self.title)))
        out.append('<text class="vc-s" x="%d" y="36">%s</text>' % (PAD_L, esc(self.sub)))
        lx = self.width - PAD_R
        out.append('<g class="vc-lg" transform="translate(%.0f,0)">' % lx)
        out.append('<line class="vc-e" x1="-232" y1="17" x2="-206" y2="17"/>'
                   '<text class="vc-lgt" x="-202" y="20">SEC 공시로 확인</text>')
        out.append('<line class="vc-e vc-dash" x1="-232" y1="33" x2="-206" y2="33"/>'
                   '<text class="vc-lgt" x="-202" y="36">추정·교차 확인</text>')
        out.append('</g>')
        # 층 이름
        for ci, x in enumerate(self._x):
            if ci < len(self.layers) and self.cols[ci]:
                out.append('<text class="vc-lay" x="%.1f" y="%.1f">%s</text>'
                           % (x, TOP - 8, esc(self.layers[ci])))
        for col in self.cols:
            for b in col:
                self._draw_box(b, out)
        # 선
        lanes = {}
        rail_i = 0
        rail_y0 = TOP + self.body_h + 14
        for e in self.edges:
            a, b = self.by_id[e['a']], self.by_id[e['b']]
            x1, y1 = self._port(a, 'r')
            x2, y2 = self._port(b, 'l')
            cls = 'vc-e vc-dash' if e['dashed'] else 'vc-e'
            span = b['col'] - a['col']
            if span == 1 or (span == 0 and x2 > x1):
                key = (a['col'], round(y1), round(y2))
                gi = lanes.setdefault((a['col'], round(y2)), len(lanes) % 5)
                if abs(y1 - y2) < 1.5:
                    d = 'M%.1f %.1f H%.1f' % (x1, y1, x2 - 6)
                else:
                    mx = x1 + GUT * (0.32 + 0.11 * (gi % 4))
                    d = 'M%.1f %.1f H%.1f V%.1f H%.1f' % (x1, y1, mx, y2, x2 - 6)
            else:
                ry = rail_y0 + rail_i * 12
                rail_i += 1
                d = 'M%.1f %.1f H%.1f V%.1f H%.1f V%.1f H%.1f' % (
                    x1, y1, x1 + 14, ry, x2 - 20, y2, x2 - 6)
            out.append('<path class="%s" d="%s"/>' % (cls, d))
            if e['label']:
                mx = (x1 + x2) / 2.0
                out.append('<text class="vc-el" x="%.1f" y="%.1f">%s</text>'
                           % (mx, min(y1, y2) - 4, esc(e['label'])))
        fy = rail_y0 + self.rail_n * 12 + 20
        for f in self.foot:
            out.append('<text class="vc-f" x="%d" y="%.1f">%s</text>' % (PAD_L, fy, esc(f)))
            fy += 18
        out.append('</svg>')
        return ''.join(out)


CSS = """
:root{--paper:#fff;--ink1:#1a2233;--ink2:#39415a;--ink3:#6b7488;--ink4:#98a0b0;
--line:#d6dae2;--c-sup:#f2f4f8;--c-co:#e8eef7;--c-seg:#eef3ee;--c-ch:#f7f2ea;
--c-cus:#f4eef4;--c-end:#f1f1f4;--edge:#8b93a5}
*{box-sizing:border-box}
body{margin:0;background:#f7f8fa;color:var(--ink1);
font:15px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR",sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:28px 18px 80px}
h1{font-size:23px;margin:0 0 6px;letter-spacing:-.2px}
h2{font-size:19px;margin:44px 0 10px;letter-spacing:-.2px}
h3{font-size:15px;margin:26px 0 8px;color:var(--ink2)}
p{margin:0 0 12px;color:var(--ink2)}
.sub{color:var(--ink3);font-size:14px;margin-bottom:22px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:8px;
padding:16px 16px 10px;margin:14px 0 26px;overflow-x:auto}
.card>svg{min-width:900px}
table{border-collapse:collapse;width:100%;font-size:13.5px;margin:10px 0 18px}
th,td{border-bottom:1px solid var(--line);padding:7px 9px;text-align:left;
vertical-align:top;color:var(--ink2)}
th{color:var(--ink3);font-weight:600;font-size:12.5px;white-space:nowrap}
td.n{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.tag{display:inline-block;border:1px solid var(--line);border-radius:3px;
padding:0 5px;font-size:11.5px;color:var(--ink3);margin-right:4px}
.note{font-size:13px;color:var(--ink3)}
/* 도해 */
svg.vc{display:block}
.vc-t{font-size:14.5px;font-weight:700;fill:var(--ink1)}
.vc-s{font-size:11.5px;fill:var(--ink3)}
.vc-lay{font-size:10px;fill:var(--ink4);letter-spacing:.6px}
.vc-lgt{font-size:10px;fill:var(--ink3)}
.vc-b{fill:var(--paper);stroke:var(--line);stroke-width:1}
.vc-L0{fill:var(--c-sup)}.vc-L1{fill:var(--c-co)}.vc-L2{fill:var(--c-seg)}
.vc-L3{fill:var(--c-ch)}.vc-L4{fill:var(--c-cus)}.vc-L5{fill:var(--c-end)}
.lg{display:flex;flex-wrap:wrap;gap:14px 20px;align-items:center;margin:10px 0 0;
padding:14px 16px;background:var(--paper);border:1px solid var(--line);border-radius:8px}
.lg b{font-weight:600;font-size:12.5px;color:var(--ink3);margin-right:2px}
.lg span{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:var(--ink2)}
.sw{width:15px;height:15px;border:1px solid var(--line);border-radius:3px;display:inline-block}
.vc-hero{stroke:var(--ink2);stroke-width:1.6;fill:var(--c-co)}
.vc-grp{fill:#fbfcfe;stroke:var(--line);stroke-dasharray:none}
.vc-n{font-size:11px;font-weight:600;fill:var(--ink1)}
.vc-nh{font-size:12.5px}
.vc-d{font-size:9.5px;fill:var(--ink3)}
.vc-e{fill:none;stroke:var(--edge);stroke-width:1.1;marker-end:url(#vca)}
.vc-dash{stroke-dasharray:5 4}
.vc-el{font-size:9px;fill:var(--ink3);text-anchor:middle}
.vc-f{font-size:10.5px;fill:var(--ink3)}
@media (max-width:700px){.wrap{padding:18px 12px 60px}h1{font-size:20px}}
"""

DEFS = ('<svg width="0" height="0" style="position:absolute"><defs>'
        '<marker id="vca" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0 0 L8 4 L0 8 z" fill="#8b93a5"/></marker></defs></svg>')


def page(title, intro_html, blocks, out_path):
    parts = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width,initial-scale=1">',
             '<title>%s</title><style>%s</style></head><body>' % (esc(title), CSS),
             DEFS, '<div class="wrap">', intro_html]
    parts += blocks
    parts += ['</div></body></html>']
    io.open(out_path, 'w', encoding='utf-8').write(''.join(parts))
    return out_path
