# -*- coding: utf-8 -*-
"""Semi Doped 판에 끼우는 도해.

받은 글(insights/semidoped/<slug>-<lane>.md)은 문장을 안 고친다. 도해는 그 글의 것이
아니라 우리 것이라 여기 따로 둔다 — 열쇠는 (slug, lane), 값은 `[(절 제목 머리, 제목, svg, 캡션)]`.
절 제목 머리는 받은 글의 `## ` 제목이 그 문자열로 시작하는 절이다(「## 4. (프로세스)」면 '4.').
`gen_semidoped.body_html` 이 그 제목 바로 아래, 본문보다 **앞에** 그림을 세운다.

지킬 것은 `insight-figure` 스킬 넷 — 원문에 없는 값을 안 그린다(도형 개수도 값이다) ·
좌표는 사람이 안 찍는다(`aie_figs` 의 box·band·table 이 글자 폭으로 잰다) · 판 위에 글자를
안 얹는다 · 배치는 `check_fig.hits` 가 본다. 붓과 판 폭은 AI Engineer 도해와 같다 —
글자가 본문과 같은 .95rem 이고 판은 520 이라 옆으로 안 밀린다.

값 대조는 `check_figval` 이 아니라 여기 `values()` 가 뽑아 준다 — 그림 글자에 든 숫자를
전사(raw)에서 찾는다. `gen_semidoped` 가 생성 때 돌리고 못 찾은 값이 있으면 멈춘다.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aie_figs import (W, CHW, LH, GAP, w_of, box, mid, head, arrow, down,  # noqa: F401,E402
                      legend, svg, table, band)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'content', 'understanding', 'Semi Doped', 'raw')

# 색 변수는 이 장 페이지에 없다(dash_common 을 안 쓴다). gen_semidoped 가 이 CSS 를 그대로 싣는다
CSS = '''
.uc-fig{--ink:#1b1f27;--ink-2:#3a4150;--ink-3:#66707f;--surface:#fff;--line:#e2e5ea;
        --epoch-teal:#00A5A6;--epoch-coral:#FD6438;--epoch-keybg:#D6F2F2;
        --epoch-wrapbg:rgba(0,165,166,.10);--sunk:rgba(127,127,127,.10)}
.uc-fig{margin:6px 0 22px;border:1px solid var(--line);border-radius:12px;padding:12px 10px 10px;
        background:#fbfbfc}
.uc-fig svg{display:block;width:100%;max-width:520px;height:auto;margin:0 auto}
.uc-fig .fig-title{margin:0 0 10px;font-size:.95rem;font-weight:800;color:var(--ink-3)}
.uc-fig figcaption{margin:10px 2px 0;font-size:.88rem;line-height:1.65;color:var(--ink-3)}
.uc-fig figcaption b{color:var(--ink-2)}
.uc-fig .fig-box{fill:var(--surface);stroke:var(--ink-3);stroke-width:1.2}
.uc-fig .fig-human{fill:var(--epoch-keybg)}
.uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--epoch-teal);stroke-width:1.6}
.uc-fig .fig-stage{fill:var(--sunk)}
.uc-fig .fig-inside{fill:var(--epoch-keybg)}
.uc-fig .fig-outside{fill:var(--surface);stroke-dasharray:4 3}
.uc-fig .fig-bad{fill:var(--surface);stroke:var(--epoch-coral);stroke-width:1.6}
.uc-fig .fig-b{fill:var(--ink);font-size:.95rem;font-weight:600}
.uc-fig .fig-st{fill:var(--ink);font-size:.95rem;font-weight:800}
.uc-fig .fig-hd{fill:var(--ink-3);font-size:.95rem;font-weight:800}
.uc-fig .fig-e{fill:var(--ink-3);font-size:.95rem;font-weight:700}
.uc-fig .fig-lg{fill:var(--ink-3);font-size:.95rem;font-weight:650}
.uc-fig .fig-arw{stroke:var(--epoch-teal);stroke-width:2;fill:none}
'''


def fig_html(f):
    _key, title, svg_, cap = f
    h = ['<figure class="uc-fig">']
    if title:
        h.append('<p class="fig-title">%s</p>' % title)
    h.append(svg_)
    if cap:
        h.append('<figcaption>%s</figcaption>' % cap)
    h.append('</figure>')
    return ''.join(h)


def values(svg_):
    """그림 글자에 든 두 자리 이상 숫자."""
    nums = set()
    for s in re.findall(r'<text[^>]*>([^<]*)<', svg_):
        for n in re.findall(r'\d[\d,\.]*', s):
            if len(n.replace(',', '').rstrip('.')) >= 2:
                nums.add(n)
    return nums


def missing_values(slug, svg_):
    """전사에 없는 값. 전사가 없으면 값 전부를 돌려준다 — 대조 못 한 것은 못 찾은 것이다."""
    path = os.path.join(RAW, slug + '.md')
    if not os.path.exists(path):
        return sorted(values(svg_))
    src = re.sub(r'[\s,]', '', io.open(path, encoding='utf-8').read())
    return sorted(n for n in values(svg_) if n.replace(',', '') not in src)


# ── 붓 ───────────────────────────────────────────────────────────────

def vline(x, y1, y2, arrow_=True):
    m = ' marker-end="url(#aieArw)"' if arrow_ else ''
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"%s/>' % (x, y1, x, y2, m)]


def hline(x1, x2, y):
    return ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x1, y, x2, y)]


def panel_boxes(x0, y, items, gap=12, h=None):
    """상자 여러 개를 x0 에서부터 가로로 잇는다. [(줄들, 클래스)]. 폭은 글자로 잰다."""
    out, x, centers = [], x0, []
    hh = h or (max(len(l) for l, _ in items) * LH + 26)
    for lines, cls in items:
        w = w_of(lines)
        out += box(x, y, w, hh, lines, cls)
        centers.append((x + w / 2, w))
        x += w + gap
    return out, x - gap, centers, hh


# ══ 할라페뇨 (2026-08-27) 전략 판 ═══════════════════════════════════════
# 값은 전사에 있는 것만 — 128칩·600Gb/s·2,048칩·16랙·200Gb/s·아홉 달. 상자 개수는
# 그 자체가 뜻이 아닌 자리(가속기 「둘」)를 캡션에 밝힌다.

def _jal_numa():
    # 왼쪽 — 나눠 쓰는 HBM.  오른쪽 — 가속기마다 전용 슬라이스
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '나눠 쓰는 HBM') + head(R, 22, 248, '전용 슬라이스 (할라페뇨)')
    # 왼쪽: HBM 한 덩어리 위, 가속기 둘 아래, 둘 다 위로 올라가 한 곳에 닿는다
    hbm_w = w_of(['HBM 한 덩어리'])
    hbm_x = L + (248 - hbm_w) / 2
    parts += box(hbm_x, 40, hbm_w, 44, ['HBM 한 덩어리'], 'fig-stage')
    acc, x_end, cs, hh = panel_boxes(L + 24, 128, [(['가속기'], 'fig-box'), (['이웃 가속기'], 'fig-box')], gap=20)
    parts += acc
    for cx, _w in cs:
        parts += vline(cx, 128, 86)
    parts += box(L + 20, 200, 208, 44, ['데이터가 늦게 온다'], 'fig-bad')
    # 오른쪽: 가속기 둘, 각자 아래 자기 슬라이스
    acc2, _x, cs2, _h = panel_boxes(R + 8, 40, [(['가속기'], 'fig-box'), (['가속기'], 'fig-box')], gap=96)
    parts += acc2
    for cx, _w in cs2:
        sw = w_of(['전용 HBM', '슬라이스'])
        parts += box(cx - sw / 2, 128, sw, hh + 23, ['전용 HBM', '슬라이스'], 'fig-agent')
        parts += vline(cx, 84, 126)
    parts += box(R + 20, 200 + 23, 208, 44, ['전달되는 플롭'], 'fig-agent')
    return svg(272, parts,
               '왼쪽은 가속기 둘이 HBM 한 덩어리를 나눠 써 데이터가 늦게 오고, 오른쪽은 가속기마다 전용 HBM 슬라이스를 둬 전달되는 플롭을 확보한다')


def _jal_scaleup():
    parts, y_end = table(
        [[['랙 사이'], ['2,048칩', '16랙'], ['ESUN', '초당 200 기가비트']],
         [['랙 안'], ['128칩'], ['Tomahawk6', '칩당 초당', '600 기가비트']]],
        ['fig-stage', 'fig-box', 'fig-box'], heads=['층', '칩 수', '연결'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '랙 안 128칩은 Tomahawk6 로 칩당 600Gb/s, 랙 사이 2,048칩(16랙)은 ESUN 으로 200Gb/s 로 잇는다')


def _jal_balanced():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '분리 (GPU 방식)') + head(R, 22, 248, '균형 단일 칩 (할라페뇨)')
    sep, x_end, cs, hh = panel_boxes(L + 30, 40, [(['프리필 칩'], 'fig-box'), (['디코드 칩'], 'fig-box')], gap=16)
    parts += sep
    parts += box(L + 12, 150, 224, 44, ['비율이 바뀌면 한쪽이 논다'], 'fig-bad')
    one_w = w_of(['한 칩에', '연산·대역폭·IO', '다 넉넉히'])
    parts += box(R + (248 - one_w) / 2, 40, one_w, 3 * LH + 26, ['한 칩에', '연산·대역폭·IO', '다 넉넉히'], 'fig-agent')
    parts += box(R + 12, 150, 224, 44, ['안 쓰는 부분만 끈다'], 'fig-agent')
    return svg(210, parts,
               '왼쪽은 프리필 칩과 디코드 칩을 나눠 비율이 바뀌면 한쪽이 놀고, 오른쪽은 한 칩에 연산·대역폭·IO 를 다 넉넉히 두고 안 쓰는 부분만 끈다')


def _jal_cycle():
    # 「아홉 달」 라벨이 상자 테두리에 닿지 않게 첫 틈만 넓게 준다 — 남는 자리 192 를 96·48·48 로
    row, _x = band([(['첫 RTL'], 'fig-box'), ('>', '아홉 달'),
                    (['테이프아웃'], 'fig-agent'), ('>', ''),
                    (['Gen 2', '테이프아웃', '근접'], 'fig-box'), ('>', ''),
                    (['Gen 3', '구상'], 'fig-box')], 40, 95, gaps=[96, 48, 48])
    note = mid(140, 44, ['통상은 첫 RTL 에서 테이프아웃까지 2~3년'], 'fig-stage')
    return svg(200, row + note,
               '첫 RTL 에서 테이프아웃까지 아홉 달, 통상은 2~3년. Gen 2 는 테이프아웃에 다가섰고 Gen 3 은 구상 중이다')


def _jal_sell():
    top_w = w_of(['할라페뇨 칩을'])
    parts = box((W - top_w) / 2, 20, top_w, 44, ['할라페뇨 칩을'], 'fig-box')
    # 갈림 둘
    lw, rw = w_of(['사내 전용']), w_of(['판다'])
    lx, rx = 60.0, 354.0     # 오른쪽 가지 셋(250..493)의 한가운데가 371 이라 「판다」를 거기 맞춘다
    parts += box(lx, 110, lw, 44, ['사내 전용'], 'fig-box')
    parts += box(rx, 110, rw, 44, ['판다'], 'fig-agent')
    parts += vline(W / 2, 64, 86, arrow_=False) + hline(lx + lw / 2, rx + rw / 2, 86)
    parts += vline(lx + lw / 2, 86, 108) + vline(rx + rw / 2, 86, 108)
    # 사내 전용 아래 근거 하나
    gl = ['Anthropic·', 'Google', '상대 우위']
    gw = w_of(gl)
    parts += box(lx + lw / 2 - gw / 2, 200, gw, 3 * LH + 26, gl, 'fig-stage')
    parts += vline(lx + lw / 2, 154, 198)
    # 판다 아래 행위자 셋
    acts, x_end, cs, hh = panel_boxes(250, 200, [(['기업에', '직접'], 'fig-box'),
                                                 (['네오클라우드', '경유'], 'fig-box'),
                                                 (['추론을', '서비스로'], 'fig-box')], gap=14)
    parts += acts
    parts += vline(rx + rw / 2, 154, 176, arrow_=False) + hline(cs[0][0], cs[-1][0], 176)
    for cx, _w in cs:
        parts += vline(cx, 176, 198)
    return svg(200 + hh + 14, parts,
               '할라페뇨 칩을 사내 전용으로 두면 Anthropic·Google 상대 우위, 판다면 기업에 직접·네오클라우드 경유·추론을 서비스로 셋 중 하나다')


JAL = '2026-08-27-openai-jalapeno'

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]
FIGS = {
    (JAL, 'strategy'): [
        ('2-1', 'NUMA 슬라이스가 푼 것', _jal_numa(),
         '왼쪽이 문제다 — 이웃 가속기와 HBM 한 덩어리를 나눠 쓰면 대역폭이 있어도 필요한 순간 데이터가 없다(Chris, L129). '
         '오른쪽이 할라페뇨의 답이다 — 가속기마다 전용 HBM 슬라이스와 저지연 버스를 둔다(L131). '
         '가속기를 둘 그린 것은 「나눠 쓴다」를 보이려는 최소 수이고 실제 개수는 전사에 없다.'),
        ('2-2', '스케일업 두 층', _jal_scaleup(),
         '담는 것이 위, 담기는 것이 아래다. 랙 안 128칩은 Broadcom Tomahawk6 로 칩당 600Gb/s, '
         '랙 사이는 2,048칩(16랙)까지 ESUN 으로 200Gb/s 다(L141·L145). 스케일업의 기준이 랙 경계가 아니라 메모리를 공유하는 범위라는 것이 Austin 의 논지다(L149).'),
        ('2-3', '분리 대 균형 단일 칩', _jal_balanced(),
         '왼쪽은 GPU 쪽 관행 — 프리필 칩과 디코드 칩을 나누면 워크로드 비율이 바뀔 때 한쪽이 논다(L155). '
         '오른쪽은 할라페뇨 — 한 칩에 연산·대역폭·IO 를 다 넉넉히 두고 안 쓰는 부분만 끈다(L157). 끈 자리가 다크 실리콘이다.'),
        ('4.', '첫 RTL 에서 Gen 3 까지', _jal_cycle(),
         '순서가 뜻이다. 첫 RTL 에서 테이프아웃까지 아홉 달(L97), 통상은 2~3년. Gen 2 는 이미 테이프아웃에 다가섰고 Gen 3 은 구상 중이라고 Richard 가 말했다고 Austin 이 전했다(L95).'),
        ('6.', '사내 전용인가 파는가', _jal_sell(),
         '갈림 하나에 가지 셋. 왼쪽은 Austin 이 든 사내 전용의 논리(L77), 오른쪽 셋은 Austin 이 「thinking out loud」라 밝힌 즉흥 제안이다(L81). '
         '원문은 어느 쪽도 확정하지 않았다.'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
