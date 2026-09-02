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
# 값은 전사에 있는 것만. 상자 개수는 글이 가른 항의 수와 같다(요인 셋·구성 셋·단 둘).

def _col(x0, y0, items, gap=10):
    """상자를 위아래로 쌓는다. [(줄들, 클래스)]. 폭은 열에서 가장 긴 글에 맞춘다."""
    w = w_of(*[l for l, _ in items])
    out, y = [], y0
    for lines, cls in items:
        h = len(lines) * LH + 22
        out += box(x0, y, w, h, lines, cls)
        y += h + gap
    return out, w, y - gap


def _jal_nine_months():
    items = [(['AI 도구', 'GPT-3급 모델로', '첫 RTL 초안'], 'fig-box'),
             (['TPU 출신 인재', 'Richard Ho'], 'fig-box'),
             (['백지 설계', '레거시 부담 없음'], 'fig-box')]
    row, x_end, cs, hh = panel_boxes(0, 30, items, gap=18, h=3 * LH + 22)
    parts = list(row)
    tl = ['첫 RTL 에서 테이프아웃까지 아홉 달']
    tw = w_of(tl)
    ty = 30 + hh + 40
    parts += box((W - tw) / 2, ty, tw, 44, tl, 'fig-agent')
    for cx, _w in cs:
        parts += vline(cx, 30 + hh + 2, ty - 2)
    parts += mid(ty + 60, 44, ['통상은 최소 2~3년, 수작업이 많이 든다'], 'fig-stage')
    return svg(ty + 116, parts,
               'AI 도구·TPU 출신 인재·백지 설계 셋이 겹쳐 첫 RTL 에서 테이프아웃까지 아홉 달이 걸렸다. 통상은 최소 2~3년이다')


def _jal_three_configs():
    # 추론 워크로드를 받는 세 구성을 나란히. 열 셋, 위 = 구성, 아래 = 이 회차가 붙인 조건
    # 열 셋 합이 520 을 넘으면 안 된다 — 한 줄 10자(160px) 안으로 자른다
    cols = [(['범용 GPU', '한 종류'], 'fig-box', ['초당 1,000토큰', '못 닿음'], 'fig-bad'),
            (['프리필·디코드', '나눔', 'GPU+SRAM'], 'fig-box', ['NVL72 1대', 'Groq 9대'], 'fig-stage'),
            (['균형 잡힌', '한 칩', '안 쓰는 구획 끔'], 'fig-agent', ['할라페뇨', '랙 1~2대', '700W'], 'fig-agent')]
    gap = 16
    ws = [w_of(top, bot) for top, _c, bot, _b in cols]
    x, parts = (W - (sum(ws) + gap * 2)) / 2, []
    th = 3 * LH + 22
    bh = 3 * LH + 22
    for (top, tc, bot, bc), w in zip(cols, ws):
        parts += box(x, 30, w, th, top, tc)
        parts += vline(x + w / 2, 30 + th + 2, 30 + th + 26)
        parts += box(x, 30 + th + 28, w, bh, bot, bc)
        x += w + gap
    y = 30 + th + 28 + bh
    parts += legend([('fig-agent', '할라페뇨의 선택'), ('fig-bad', '못 닿는 자리')], y + 18)
    return svg(y + 44, parts,
               '범용 GPU 하나는 초당 1,000토큰 영역에 못 닿고, 프리필·디코드를 나누면 NVL72 랙 1대에 Groq 랙 9대가 붙고, 균형 잡힌 한 칩은 랙 1~2대 700W 로 그 자리를 밟는다')


def _jal_hbm_gap():
    # 위에서 아래로 흐른다 — 산수 셋, 실제 하나, 원인, 처방. 실측치는 전사에 없어 「그 수가 안 나온다」로만
    steps = [(['128칩 HBM4 대역폭을 다 더하면 초당 1페타바이트'], 'fig-box'),
             (['1조 파라미터 모델을 FP4 로 얹으면 0.5테라바이트'], 'fig-box'),
             (['산수로는 초당 2,000토큰'], 'fig-stage'),
             (['실제로는 그 수가 안 나온다'], 'fig-bad'),
             (['연산하려는 순간 데이터가 없다 — 이웃과 HBM 경합'], 'fig-bad'),
             (['처방: 가속기마다 자기 몫 HBM 슬라이스 + 전용 버스'], 'fig-agent')]
    w = w_of(*[l for l, _ in steps])
    x0, y, parts = (W - w) / 2, 24, []
    for k, (lines, cls) in enumerate(steps):
        parts += box(x0, y, w, 44, lines, cls)
        if k < len(steps) - 1:
            parts += vline(W / 2, y + 46, y + 66)
        y += 68
    return svg(y - 10, parts,
               '128칩의 HBM4 대역폭을 다 더하면 초당 1페타바이트, 1조 파라미터를 FP4 로 얹으면 0.5테라바이트라 산수로는 초당 2,000토큰인데 실제로는 그 수가 안 나온다. 원인은 경합, 처방은 가속기마다 자기 몫 슬라이스')


def _jal_scaleup():
    parts, y_end = table(
        [[['랙 16대'], ['2,048칩'], ['ESUN', '초당 200 기가비트']],
         [['랙 1대'], ['128칩'], ['Tomahawk 6', '칩당 초당', '600 기가비트']]],
        ['fig-stage', 'fig-box', 'fig-box'], heads=['층', '칩 수', '연결'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '랙 1대 안 128칩은 Tomahawk 6 로 칩당 초당 600기가비트, 랙 16대 2,048칩은 ESUN 으로 초당 200기가비트로 잇는다')


JAL = '2026-08-27-openai-jalapeno'

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]
FIGS = {
    (JAL, 'strategy'): [
        ('1.', '아홉 달을 만든 세 요인', _jal_nine_months(),
         '셋이 겹쳐 아홉 달이 됐다(L97). 사람과 백지는 전에도 있던 항이고 AI 도구만 새 항이라는 것이 이 절의 논지다. '
         '셋 중 무엇이 몇 할인지는 전사에 없어 상자 크기를 같게 뒀다.'),
        ('3.', '추론을 받는 세 구성', _jal_three_configs(),
         '위가 구성, 아래가 이 회차가 붙인 조건이다. 랙 수(NVL72 1대 + Groq 9대 대 할라페뇨 1~2대)는 Austin 의 어림이고(L109), '
         '700W 는 발표 값(L111), 초당 1,000토큰은 GPT-OSS 기준이다(L105).'),
        ('4.', 'HBM 대역폭이 토큰으로 안 옮겨지는 자리', _jal_hbm_gap(),
         'Vik 의 산수(L121)는 초당 2,000토큰까지 가는데 실제는 그 수가 안 나온다. 실측치는 전사에 없어 마지막 칸을 상태로만 그렸다. '
         '원인은 Chris 가 「the operands arrive late」라 부른 경합(L129), 처방은 가속기마다 로컬 HBM 슬라이스(L131).'),
        ('5.', '스케일업 두 층', _jal_scaleup(),
         '담는 것이 위, 담기는 것이 아래다(L141·L145). 스케일업의 기준이 랙 안이 아니라 메모리를 나눠 쓰는 범위라는 것이 Austin 의 지적이다(L149).'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
