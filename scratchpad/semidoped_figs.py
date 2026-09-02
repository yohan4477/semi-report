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
/* 색은 셋 — 흰 상자·회색 선(기본), 옅은 청록(이 회차의 선택, 판에 하나), 점선 회색(문제·아직 없는 것).
   주황·강조색 여럿은 정신 사납다는 지적(2026-09-02)으로 걷었다. 화살표도 회색이다 */
.uc-fig{--ink:#1b1f27;--ink-2:#3a4150;--ink-3:#66707f;--surface:#fff;--line:#e2e5ea;
        --epoch-teal:#8a93a1;--epoch-coral:#8a93a1;--epoch-keybg:#eef1f6;
        --epoch-wrapbg:#e9f3f3;--sunk:#eef1f6;--pick:#3d8b8b}
.uc-fig{margin:6px 0 22px;border:1px solid var(--line);border-radius:12px;padding:12px 10px 10px;
        background:#fbfbfc}
.uc-fig svg{display:block;width:100%;max-width:520px;height:auto;margin:0 auto}
.uc-fig .fig-title{margin:0 0 10px;font-size:.95rem;font-weight:700;color:var(--ink-3)}
.uc-fig figcaption{margin:10px 2px 0;font-size:.88rem;line-height:1.65;color:var(--ink-3)}
.uc-fig figcaption b{color:var(--ink-2)}
.uc-fig .fig-box{fill:var(--surface);stroke:#9aa3b2;stroke-width:1.2}
.uc-fig .fig-human{fill:var(--epoch-keybg)}
.uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--pick);stroke-width:1.4}
.uc-fig .fig-stage{fill:var(--sunk);stroke:#c9ced6;stroke-width:1}
.uc-fig .fig-inside{fill:var(--epoch-keybg)}
.uc-fig .fig-outside{fill:var(--surface);stroke:#9aa3b2;stroke-dasharray:4 3}
.uc-fig .fig-bad{fill:var(--surface);stroke:#9aa3b2;stroke-width:1.2;stroke-dasharray:4 3}
.uc-fig .fig-b{fill:var(--ink);font-size:.95rem;font-weight:600}
.uc-fig .fig-st{fill:var(--ink);font-size:.95rem;font-weight:800}
.uc-fig .fig-hd{fill:var(--ink-3);font-size:.95rem;font-weight:700}
.uc-fig .fig-e{fill:var(--ink-3);font-size:.95rem;font-weight:600}
.uc-fig .fig-lg{fill:var(--ink-3);font-size:.95rem;font-weight:600}
.uc-fig .fig-arw{stroke:#8a93a1;stroke-width:1.6;fill:none}
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
    parts += legend([('fig-agent', '할라페뇨의 선택'), ('fig-bad', '한계가 있는 자리')], y + 18)
    return svg(y + 44, parts,
               '범용 GPU 하나는 초당 1,000토큰 영역에 못 닿고, 프리필·디코드를 나누면 NVL72 랙 1대에 Groq 랙 9대가 붙고, 균형 잡힌 한 칩은 랙 1~2대 700W 로 그 자리를 밟는다')


def _jal_numa4():
    """가속기를 모듈로 놓고 넷을 그린다. 두 판이 같은 꼴이다 — 위 가속기 넷, 아래 HBM, 화살표는
    아래로. 왼쪽은 넷이 HBM 한 덩어리로 모이고, 오른쪽은 각자 제 HBM 몫으로 내려간다. 넷은
    보기용 수다 — 실제 랙은 128칩이고 몇 개가 한 HBM 을 나눠 쓰는지는 전사에 없다."""
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, 'HBM 을 나눠 쓴다') + head(R, 22, 248, '가속기마다 자기 몫')
    acc = [(['가속기'], 'fig-box')] * 4
    y_acc, y_hbm = 38, 150
    # 왼쪽 — 가속기 넷(위) → HBM 한 덩어리(아래)로 화살표 넷이 모인다
    row, _x, cs, hh = panel_boxes(L + 4, y_acc, acc, gap=12)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, y_acc + hh + 2, y_hbm - 2)
    parts += box(L + 4, y_hbm, 240, hh, ['HBM 한 덩어리'], 'fig-stage')
    parts += box(L + 4, y_hbm + hh + 22, 240, 44, ['데이터가 늦게 온다'], 'fig-bad')
    # 오른쪽 — 가속기 넷(위) → 각자 제 HBM 몫(아래), 전용 버스 하나씩
    row2, _x2, cs2, hh2 = panel_boxes(R + 4, y_acc, acc, gap=12)
    parts += row2
    for cx, w in cs2:
        parts += vline(cx, y_acc + hh2 + 2, y_hbm - 2)
        parts += box(cx - w / 2, y_hbm, w, hh, ['HBM', '몫'], 'fig-agent')
    parts += box(R + 4, y_hbm + hh + 22, 240, 44, ['실제로 전달되는 플롭'], 'fig-agent')
    y = y_hbm + hh + 22 + 44
    parts += legend([('fig-agent', '할라페뇨의 배치'), ('fig-bad', '경합이 나는 자리')], y + 16)
    return svg(y + 42, parts,
               '왼쪽은 가속기 넷이 HBM 한 덩어리로 내려가 데이터가 늦게 오고, 오른쪽은 가속기마다 자기 HBM 몫으로 내려가 실제로 플롭을 전달한다')


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
        ('4.', '가속기마다 HBM 을 나눠 쓰나, 자기 몫을 갖나', _jal_numa4(),
         '왼쪽이 지금까지의 구조다 — 이웃 가속기들이 HBM 한 덩어리를 나눠 쓰니 연산하려는 순간 데이터가 없다(L129). '
         '오른쪽이 할라페뇨다 — 가속기마다 자기 HBM 몫을 전용 버스로 붙인다(L131). '
         '가속기 넷은 보기용 수다. 실제 랙은 128칩이고 몇 개가 한 HBM 을 나눠 쓰는지는 전사에 없다.'),
        # 5절 스케일업 두 층 도해는 걷었다(2026-09-02) — 절 머리에 서는데 절은 공급망 감사 문구로 열려
        # 그림이 무엇인지 모른 채 만나고, 같은 값이 절 중간 산문과 표에 다시 나와 중복이었다
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
