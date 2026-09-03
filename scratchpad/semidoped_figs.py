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
/* 색은 회색만 — 흰 상자·회색 선(기본), 옅은 회색 채움에 짙은 선(이 회차의 선택, 판에 하나),
   점선 회색(문제·아직 없는 것). 주황·청록은 정신 사납다는 지적(2026-09-02)으로 다 걷었다 */
.uc-fig{--ink:#1b1f27;--ink-2:#3a4150;--ink-3:#66707f;--surface:#fff;--line:#e2e5ea;
        --epoch-teal:#8a93a1;--epoch-coral:#8a93a1;--epoch-keybg:#eef1f6;
        --epoch-wrapbg:#e7ebf1;--sunk:#f1f3f6;--pick:#1b1f27}
.uc-fig{margin:6px 0 22px;border:1px solid var(--line);border-radius:12px;padding:12px 10px 10px;
        background:#fbfbfc}
.uc-fig svg{display:block;width:100%;max-width:520px;height:auto;margin:0 auto}
.uc-fig .fig-title{margin:0 0 10px;font-size:.95rem;font-weight:700;color:var(--ink-3)}
.uc-fig figcaption{margin:10px 2px 0;font-size:.88rem;line-height:1.65;color:var(--ink-3)}
.uc-fig figcaption b{color:var(--ink-2)}
.uc-fig .fig-box{fill:var(--surface);stroke:#9aa3b2;stroke-width:1.2}
.uc-fig .fig-human{fill:var(--epoch-keybg)}
.uc-fig .fig-agent{fill:var(--epoch-wrapbg);stroke:var(--pick);stroke-width:1.6}
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
    return svg(ty + 60, parts,
               'AI 도구·TPU 출신 인재·백지 설계 셋이 겹쳐 첫 RTL 에서 테이프아웃까지 아홉 달이 걸렸다. 통상은 최소 2~3년이다')


def _jal_numa4():
    """가속기를 모듈로 놓고 넷을 그린다. 두 판이 같은 꼴이다 — 위 가속기 넷, 아래 HBM, 화살표는
    아래로. 왼쪽은 넷이 HBM 한 덩어리로 모이고, 오른쪽은 각자 따로 둔 HBM 으로 내려간다. 넷은
    보기용 수다 — 실제 랙은 128칩이고 몇 개가 한 HBM 을 나눠 쓰는지는 전사에 없다."""
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, 'HBM 을 나눠 쓴다') + head(R, 22, 248, '가속기마다 전용 HBM')
    acc = [(['가속기'], 'fig-box')] * 4
    y_acc, y_hbm = 38, 150
    # 왼쪽 — 가속기 넷(위) → HBM 한 덩어리(아래)로 화살표 넷이 모인다
    row, _x, cs, hh = panel_boxes(L + 4, y_acc, acc, gap=12)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, y_acc + hh + 2, y_hbm - 2)
    parts += box(L + 4, y_hbm, 240, hh, ['HBM 한 덩어리'], 'fig-stage')
    parts += box(L + 4, y_hbm + hh + 22, 240, 44, ['데이터가 늦게 온다'], 'fig-bad')
    # 오른쪽 — 가속기 넷(위) → 각자 따로 둔 HBM(아래), 전용 버스 하나씩
    row2, _x2, cs2, hh2 = panel_boxes(R + 4, y_acc, acc, gap=12)
    parts += row2
    for cx, w in cs2:
        parts += vline(cx, y_acc + hh2 + 2, y_hbm - 2)
        parts += box(cx - w / 2, y_hbm, w, hh, ['전용', 'HBM'], 'fig-agent')
    parts += box(R + 4, y_hbm + hh + 22, 240, 44, ['실제로 전달되는 플롭'], 'fig-agent')
    y = y_hbm + hh + 22 + 44
    parts += legend([('fig-agent', '할라페뇨의 배치'), ('fig-bad', '경합이 나는 자리')], y + 16)
    return svg(y + 42, parts,
               '왼쪽은 가속기 넷이 HBM 한 덩어리로 내려가 데이터가 늦게 오고, 오른쪽은 가속기마다 따로 둔 HBM 으로 내려가 실제로 플롭을 전달한다')


def _jal_scaleup():
    parts, y_end = table(
        [[['랙 16대'], ['2,048칩'], ['ESUN', '초당 200 기가비트']],
         [['랙 1대'], ['128칩'], ['Tomahawk 6', '칩당 초당', '600 기가비트']]],
        ['fig-stage', 'fig-box', 'fig-box'], heads=['층', '칩 수', '연결'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '랙 1대 안 128칩은 Tomahawk 6 로 칩당 초당 600기가비트, 랙 16대 2,048칩은 ESUN 으로 초당 200기가비트로 잇는다')


def _rect(x, y, w, h, cls='fig-box'):
    return ['  <rect x="%g" y="%g" width="%g" height="%g" rx="4" class="%s"/>' % (x, y, w, h, cls)]


def eband(items, y, h, w=None, min_gap=20):
    """가로 사슬 — **상자는 전부 한 폭**. 폭은 가장 긴 글(또는 w), 틈은 남는 자리를 화살표 수로 고르게.
    aie_figs.band 은 글자마다 폭을 재서 상자 크기가 달라지는데, 사슬에서는 그게 중요도로 읽힌다
    (2026-09-02 사용자 지적). 두 줄을 견줄 때는 w 를 같이 준다."""
    boxes = [it for it in items if it[0] != '>']
    narw = len(items) - len(boxes)
    w = w or max(w_of(l) for l, _ in boxes)
    need = len(boxes) * w + narw * min_gap
    assert need <= W + 1, '한 폭으로 놓으면 판보다 넓다(%g) — 라벨을 줄이거나 세로 사슬로' % need
    gap = (W - len(boxes) * w) / narw if narw else 0
    out, x = [], 0.0
    for it in items:
        if it[0] == '>':
            out += arrow(x + 4, x + gap - 4, y + h / 2, it[1], len(it) > 2 and it[2])
            x += gap
        else:
            lines, cls = it
            out += box(x, y, w, h, lines, cls)
            x += w
    return out, x


def _jal_cycle():
    """주기 둘. 위는 통상(2~3년), 아래는 할라페뇨(아홉 달). 잘라낸 기능이 다음 판에 붙는 간격이
    곧 욕심의 크기다 — 간격이 길면 무리해서 넣고, 짧으면 덜 넣어도 된다."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '통상 — 다음 세대까지 2~3년')
    bw = w_of(['테이프아웃 근접'])
    r1, _ = eband([(['1세대', '잘라낸 기능'], 'fig-box'), ('>', '2~3년 뒤에나 다시'),
                   (['2세대', '그때 다시 넣음'], 'fig-box')], 32, h, w=bw)
    parts += r1
    parts += head(0, 32 + h + 34, W, '할라페뇨 — 첫 RTL 에서 테이프아웃까지 아홉 달')
    y2 = 32 + h + 44
    r2, _ = eband([(['1세대', '잘라낸 기능'], 'fig-box'), ('>', '아홉 달'),
                   (['2세대', '테이프아웃 근접'], 'fig-agent'), ('>', ''),
                   (['3세대', '구상 중'], 'fig-box')], y2, h, w=bw)
    parts += r2
    return svg(y2 + h + 16, parts,
               '통상은 다음 세대까지 2~3년이라 잘라낸 기능이 그때나 다시 들어가지만, 할라페뇨는 아홉 달 주기라 2세대가 이미 테이프아웃에 다가섰고 3세대를 구상 중이다')


def _jal_yardstick():
    """잣대가 다른 이유 — 사이에 판매자가 있나. 위는 상용 실리콘(설계팀 → 판매 → 랩·하이퍼스케일러 → 사용자),
    아래는 할라페뇨(설계팀 → 사용자). 같은 꼴, 칸 하나 차이."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '상용 실리콘 — 잣대는 TCO')
    bw = w_of(['(OpenAI)'])
    r1, _ = eband([(['칩 설계팀'], 'fig-box'), ('>', '판다'),
                   (['AI 랩 ·', '하이퍼스케일러'], 'fig-box'), ('>', '서비스'),
                   (['사용자'], 'fig-box')], 32, h, w=bw)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '할라페뇨 — 잣대는 요청당 에너지 · 마지막 토큰까지 지연')
    r2, _ = eband([(['칩 설계팀', '(OpenAI)'], 'fig-agent'), ('>', '중간 판매자 없음'),
                   (['사용자'], 'fig-box')], y2, h, w=bw)
    parts += r2
    return svg(y2 + h + 16, parts,
               '상용 실리콘은 설계팀과 사용자 사이에 판매자가 있어 TCO 를 잣대로 삼고, 할라페뇨는 설계팀이 곧 서비스 주체라 요청당 에너지와 지연을 잣대로 삼는다')


def _jal_specdec():
    """투기적 디코딩 — 초안 모델이 토큰을 여럿 뱉고 큰 모델이 검증한다. 초안이 덜 똑똑하면
    여덟 개를 뱉어 검증이 무겁고, 똑똑하면 두 개만 뱉어 가볍다(L159·L161). 8 과 2 는 전사의 수다."""
    h = 2 * LH + 22
    tw = 18

    def row(y, label, n, verify_cls):
        out = []
        lw = w_of([label, '초안 모델'])
        out += box(0, y, lw, h, [label, '초안 모델'], 'fig-box')
        x0 = lw + 26
        out += vline(lw + 4, y + h / 2, lw + 4, arrow_=False)  # 자리 맞춤용 빈 선 없음
        out.pop()
        out += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
                % (lw + 4, y + h / 2, x0 - 4, y + h / 2)]
        for k in range(n):
            out += _rect(x0 + k * (tw + 6), y + h / 2 - tw / 2, tw, tw)
        xe = x0 + 8 * (tw + 6) + 20
        vw = w_of(['큰 모델이 검증', '무겁다'])
        out += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
                % (x0 + n * (tw + 6) - 2, y + h / 2, xe - 4, y + h / 2)]
        out += box(xe, y, vw, h, ['큰 모델이 검증', '무겁다' if n == 8 else '가볍다'], verify_cls)
        return out, xe + vw

    parts = head(0, 22, W, '토큰 하나 = 네모 하나')
    r1, xe1 = row(34, '덜 똑똑한', 8, 'fig-bad')
    r2, xe2 = row(34 + h + 24, '똑똑한', 2, 'fig-agent')
    assert max(xe1, xe2) <= W + 1, '판보다 넓다: %g' % max(xe1, xe2)
    parts += r1 + r2
    y = 34 + 2 * h + 24
    return svg(y + 16, parts,
               '덜 똑똑한 초안 모델은 토큰 여덟 개를 뱉어 큰 모델의 검증이 무겁고, 똑똑한 초안 모델은 두 개만 뱉어 검증이 가볍다. 비율이 워크로드마다 움직인다')


def _jal_three_configs():
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


def _jal_ladder():
    """공급망 다섯 단. 오른쪽이 이 회차가 그 단에 본 것 — 값이 움직이는 둘만 짙은 선."""
    rows = [('CPU', '대체재가 널렸다 — Venice · 인텔', 'fig-stage'),
            ('파운드리', '대안이 없다 — TSMC N3', 'fig-stage'),
            ('메모리', '새 수요가 생긴다 — 세대 차가 비교를 뒤집는다', 'fig-agent'),
            ('스케일업 망', '새 수요가 생긴다 — 규격이 갈라져 있다', 'fig-agent'),
            ('시스템 조립', 'Celestica 로 추정', 'fig-stage')]
    lw = w_of([r[0] for r in rows] + ['밸류체인'])
    rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts = head(x0, 26, lw, '밸류체인') + head(x0 + lw + gap, 26, rw, '이 회차가 본 것')
    y, h = 36, 44
    for name, seen, cls in rows:
        parts += box(x0, y, lw, h, [name], 'fig-box')
        parts += box(x0 + lw + gap, y, rw, h, [seen], cls)
        y += h + 10
    return svg(y + 2, parts,
               'CPU 는 대체재가 널렸고 파운드리는 대안이 없어 그대로 가고, 새 수요가 생기는 곳은 메모리와 스케일업 망 둘이다. 시스템 조립은 Celestica 로 추정된다')


def _jal_domain():
    """스케일업 도메인 — 랙 16대가 한 도메인이다. 랙 하나 = 128칩, 16대 = 2,048칩. 개수 16 은 전사의 수다."""
    rw, rh, gap = 54, 40, 8
    cols, rows = 8, 2
    fw = cols * rw + (cols - 1) * gap + 24
    fx = (W - fw) / 2
    parts = box(fx, 30, fw, 2 * LH + 22, ['랙 16대 = 2,048칩 한 도메인', 'ESUN · 초당 200기가비트'], 'fig-stage')
    fy = 30 + 2 * LH + 22 + 10
    fh = rows * rh + (rows - 1) * gap + 24
    parts += _rect(fx, fy, fw, fh, 'fig-outside')
    for r in range(rows):
        for c in range(cols):
            x = fx + 12 + c * (rw + gap)
            y = fy + 12 + r * (rh + gap)
            parts += box(x, y, rw, rh, ['랙'], 'fig-agent' if (r == 0 and c == 0) else 'fig-box')
    y2 = fy + fh + 14
    parts += box(fx, y2, fw, 2 * LH + 22, ['랙 하나 = 128칩', 'Tomahawk 6 · 칩당 초당 600기가비트'], 'fig-agent')
    return svg(y2 + 2 * LH + 22 + 12, parts,
               '랙 16대가 한 스케일업 도메인이다. 랙 하나는 128칩을 Tomahawk 6 로 칩당 초당 600기가비트로, 16대 2,048칩은 ESUN 으로 초당 200기가비트로 잇는다')


def _jal_spectrum():
    """범용과 전용 사이 — 범용 GPU · TPU · 할라페뇨 · 한 모델 전용. 자리는 이 회차의 말이고 값은 없다."""
    h = 2 * LH + 22
    items = [(['범용 GPU', '어떤 모델이든'], 'fig-box'), (['구글 TPU', '한 모델 아님'], 'fig-box'),
             (['할라페뇨', 'LLM 추론용'], 'fig-agent'), (['한 모델 전용', '극단 코디자인'], 'fig-outside')]
    ws = [w_of(l) for l, _ in items]
    gap = (W - sum(ws)) / 3
    assert gap > 8
    x, parts = 0.0, []
    parts += ['  <line x1="0" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (30 + h + 22, W, 30 + h + 22)]
    for (lines, cls), w in zip(items, ws):
        parts += box(x, 30, w, h, lines, cls)
        parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x + w / 2, 30 + h + 2, x + w / 2, 30 + h + 22)]
        x += w + gap
    parts += head(0, 30 + h + 46, 120, '범용') + head(W - 120, 30 + h + 46, 120, '전용')
    return svg(30 + h + 60, parts,
               '범용 GPU 에서 한 모델 전용까지의 축 위에 구글 TPU 와 할라페뇨가 중간에 선다. 할라페뇨는 LLM 추론용이되 어떤 모델이든 돈다')


JAL = '2026-08-27-openai-jalapeno'


# ══ GPU 옆 CPU (2026-08-24) 전략 판 ═══════════════════════════════════
# 값은 전사의 것만 — 월 200달러 · 1천만 명 · 에이전트 100개 · 코어 10억 개. 자리·역할은 상태다.

def _grok_places():
    """에이전트가 사는 자리 셋. 열 셋이 같은 꼴 — 위 「에이전트 잡일」, 아래 「추론」. 다른 것은 잡일 칸의
    위치(내 노트북 / 책상 위 두 번째 기계 / 남의 데이터센터)뿐이다."""
    cols = [('노트북', ['잡일: 내 노트북', 'CPU'], 'fig-box'),
            ('Mac Mini', ['잡일: 책상 위', '두 번째 CPU'], 'fig-box'),
            ('클라우드 가상머신', ['잡일: 남의', '서버 CPU'], 'fig-agent')]
    h = 2 * LH + 22
    bot = ['추론', '클라우드 GPU']
    ws = [w_of(top, [hd], bot) for hd, top, _c in cols]
    gap = 12
    x = (W - (sum(ws) + gap * 2)) / 2
    parts = []
    for (hd, top, cls), w in zip(cols, ws):
        parts += head(x, 26, w, hd)
        parts += box(x, 36, w, h, top, cls)
        parts += vline(x + w / 2, 36 + h + 2, 36 + h + 26)
        parts += box(x, 36 + h + 28, w, h, bot, 'fig-stage')
        x += w + gap
    y = 36 + h + 28 + h
    parts += legend([('fig-agent', '쉬운 버튼이 옮기는 자리')], y + 16)
    return svg(y + 42, parts,
               '세 자리 모두 추론은 클라우드 GPU 다. 다른 것은 에이전트 잡일이 도는 CPU 가 내 노트북인가, 책상 위 두 번째 기계인가, 남의 서버인가 하나다')


def _grok_genius():
    """천재(GPU)와 조수 둘. 호스트 CPU 는 같은 방에서 천재를 먹이고, 에이전틱 CPU 랙은 넘치는 잡일을 받는다."""
    h = 2 * LH + 22
    gw = w_of(['GPU = 천재', 'HBM 종이 더미'])
    hw = w_of(['호스트 CPU', '다음 서류철 대령'])
    aw = w_of(['에이전틱 CPU 랙', '공시 긁기·컴파일'])
    gap = 40
    x0 = (W - (gw + gap + hw)) / 2
    parts = head(x0, 26, gw + gap + hw, '같은 방 — 코히어런트 연결(C2C)')
    parts += box(x0, 36, gw, h, ['GPU = 천재', 'HBM 종이 더미'], 'fig-agent')
    parts += box(x0 + gw + gap, 36, hw, h, ['호스트 CPU', '다음 서류철 대령'], 'fig-box')
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x0 + gw + 2, 36 + h / 2, x0 + gw + gap - 2, 36 + h / 2)]
    y2 = 36 + h + 40
    ax = (W - aw) / 2
    parts += box(ax, y2, aw, h, ['에이전틱 CPU 랙', '공시 긁기·컴파일'], 'fig-outside')
    parts += vline(x0 + gw / 2, 36 + h + 2, y2 - 2)
    parts += head(0, y2 + h + 22, W, '다른 랙 — 코히어런시 없음')
    return svg(y2 + h + 36, parts,
               'GPU 천재 옆에 같은 방의 호스트 CPU 가 다음 서류철을 대령하고, 천재가 뱉은 잡일은 코히어런시 없는 별도 랙의 에이전틱 CPU 가 받는다')


def _grok_layers():
    """랙 종류 넷이 아래에 나란히, 그 위에 Dynamo(천재 안쪽), 맨 위가 빈 조율 층."""
    h = 44
    racks = [(['GPU 랙'], 'fig-box'), (['Cerebras 랙'], 'fig-box'), (['P코어 랙'], 'fig-box'), (['E코어 랙'], 'fig-box')]
    ws = [w_of(l) for l, _ in racks]
    gap = 14
    x = (W - (sum(ws) + gap * 3)) / 2
    y_r = 150
    parts, cs = [], []
    for (l, c), w in zip(racks, ws):
        parts += box(x, y_r, w, h, l, c)
        cs.append(x + w / 2)
        x += w + gap
    dw = w_of(['Nvidia Dynamo — 천재를 굴리는 층'])
    parts += box(cs[0] - 20, 92, dw, h, ['Nvidia Dynamo — 천재를 굴리는 층'], 'fig-stage')
    tw = w_of(['랙을 가로질러 일감을 나누는 층 — 있는지 미확인'])
    parts += box((W - tw) / 2, 30, tw, h, ['랙을 가로질러 일감을 나누는 층 — 있는지 미확인'], 'fig-outside')
    parts += legend([('fig-outside', '비어 있는 자리'), ('fig-stage', '천재 안쪽 층')], y_r + h + 16)
    return svg(y_r + h + 42, parts,
               '아래에 성격이 다른 랙 넷이 서고, 그 위 Nvidia Dynamo 는 천재를 굴리는 층일 뿐이다. 랙을 가로질러 일감을 나누는 맨 위 층은 있는지 미확인이다')


def _grok_math():
    """코어 10억 개의 곱셈. 항 셋과 결과가 한 줄, 항마다 아래에 조건."""
    h = 2 * LH + 22
    terms = [(['사용자', '1천만 명'], ['쉬운 버튼이', '쉬워야']),
             (['사람당', '가상머신 1개'], ['제품 구조일', '뿐']),
             (['가상머신마다', '에이전트 100개'], ['기다리는 일이면', '코어를 나눠 씀']),
             (['코어', '10억 개'], ['가장 헐거운', '항은 셋째'])]
    ws = [w_of(t, c) for t, c in terms]
    gap = 22
    x = (W - (sum(ws) + gap * 3)) / 2
    parts, ops = [], ['×', '×', '=']
    for k, ((t, c), w) in enumerate(zip(terms, ws)):
        parts += box(x, 30, w, h, t, 'fig-agent' if k == 3 else 'fig-box')
        parts += vline(x + w / 2, 30 + h + 2, 30 + h + 22)
        parts += box(x, 30 + h + 24, w, h, c, 'fig-stage')
        if k < 3:
            parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-st">%s</text>' % (x + w + gap / 2, 30 + h / 2 + 6, ops[k])]
        x += w + gap
    y = 30 + h + 24 + h
    return svg(y + 14, parts,
               '사용자 1천만 명 × 사람당 가상머신 1개 × 가상머신마다 에이전트 100개 = 코어 10억 개. 항마다 조건이 붙고 셋째 항이 가장 헐겁다')


GROK = '2026-08-24-grok-bots-cpu'


# ══ 텐서다인 (2026-08-18) 전략 판 ══════════════════════════════════════
# 값은 전사의 것만 — 40바이트·9K · 13U·칩 72개·30킬로와트 · 150킬로와트. 절감률·성능 비율은 없다.

def _td_logflow():
    """곱셈을 덧셈으로 — 로그로 들어가 덧셈하고 선형으로 되돌아와 누산한다. 어려운 곳이 되돌아오는 자리.
    가로로 놓으면 「log A + log B」가 다른 칸보다 넓어져 세로 사슬로(2026-09-02)."""
    return _chain_down([(['A × B — 곱셈'], 'fig-box'),
                        (['로그로 가면 log A + log B — 덧셈'], 'fig-agent'),
                        (['선형 복귀 — 이득 안 반납'], 'fig-outside'),
                        (['누산'], 'fig-box')],
                       '곱셈을 로그 영역으로 옮기면 덧셈이 되고, 누산하려면 선형으로 되돌아와야 한다. 되돌아오는 자리에서 이득을 잃지 않는 것이 특허다')


def _td_fabric():
    """라우터를 그대로 가져온다 — 왼쪽 라우터(앞면 포트 → 뒷면 패브릭), 오른쪽 텐서다인(가속기 → 같은 패브릭). 같은 꼴."""
    L, R = 0.0, 272.0
    h = 2 * LH + 22
    parts = head(L, 22, 248, '고성능 라우터') + head(R, 22, 248, '텐서다인 쿼터랙')
    for x0, top, cls in [(L, ['앞면 포트', '아무 크기 패킷'], 'fig-box'), (R, ['가속기', '72개'], 'fig-agent')]:
        tw = w_of(top)
        parts += box(x0 + (248 - tw) / 2, 36, tw, h, top, cls)
        parts += vline(x0 + 124, 36 + h + 2, 36 + h + 26)
        bw = w_of(['뒷면 패브릭', '어느 포트에서 어느 포트로든'])
        parts += box(x0 + (248 - bw) / 2, 36 + h + 28, bw, h, ['뒷면 패브릭', '어느 포트에서 어느 포트로든'], 'fig-stage')
    y = 36 + h + 28 + h
    return svg(y + 16, parts,
               '라우터 뒷면 패브릭은 어느 포트에서 어느 포트로든 아무 크기 패킷을 처리하도록 20년 다듬어졌다. 텐서다인은 그것을 설계하지 않고 가속기 72개 아래에 그대로 가져왔다')


def _td_rack():
    """쿼터랙 대 풀랙 — 같은 꼴 두 칸. 성능이 동급인지는 값이 없어 캡션에 적는다."""
    L, R = 0.0, 272.0
    h = 3 * LH + 22
    parts = head(L, 22, 248, '텐서다인 쿼터랙') + head(R, 22, 248, 'GB300 풀랙')
    a = ['13U · 랙의 1/4', '칩 72개', '30킬로와트 · 공랭']
    b = ['풀랙', '', '150킬로와트 · 액랭']
    aw, bw = w_of(a), w_of(b)
    parts += box(L + (248 - aw) / 2, 36, aw, h, a, 'fig-agent')
    parts += box(R + (248 - bw) / 2, 36, bw, h, [x for x in b], 'fig-box')
    return svg(36 + h + 16, parts,
               '텐서다인 쿼터랙은 13U 에 칩 72개, 30킬로와트 공랭이고 견준 상대는 GB300 풀랙 150킬로와트 액랭이다. 성능이 동급인지는 이 회차에 값이 없다')


def _td_outsource():
    """스타트업이 자기 손으로 하는 것과 남에게 맡긴 것 — 밸류체인 순서대로 다섯 칸, 자기 것 둘만 짙게."""
    h = 2 * LH + 22
    items = [(['프런트엔드', '설계 · 자기'], 'fig-agent'), ('>', ''),
             (['물리 설계', '브로드컴'], 'fig-box'), ('>', ''),
             (['시스템', 'HP주니퍼'], 'fig-box'), ('>', ''),
             (['양산', 'Flex'], 'fig-box')]
    row, _x = eband(items, 30, h)
    cw = w_of(['컴파일러 — 자기 (엔지니어 60% 이상이 소프트웨어)'])
    parts = row + box((W - cw) / 2, 30 + h + 18, cw, 40, ['컴파일러 — 자기 (엔지니어 60% 이상이 소프트웨어)'], 'fig-agent')
    parts += legend([('fig-agent', '자기 손으로 한다'), ('fig-box', '남의 것을 쓴다')], 30 + h + 76)
    return svg(30 + h + 102, parts,
               '텐서다인이 자기 손으로 하는 것은 프런트엔드 설계와 컴파일러뿐이다. 물리 설계는 Broadcom, 시스템은 HP주니퍼, 양산은 페낭의 Flex 공장이 맡는다')


TD = '2026-08-18-tensordyne-rk-anand'


# ══ 중국 광트랜시버 (2026-08-11) 전략 판 ══════════════════════════════════
# 값은 전사의 것만 — 27%·34%·약 50%. 부품·갈래·조달 부품은 상태다.

def _op_module():
    """같은 트랜시버 모듈을 두 줄로. 윗줄은 미국이 만드는 부품만 짙게, 아랫줄은 중국이 맡는 부품(과 조립
    테두리)만 짙게. 나머지는 점선. 같은 꼴 둘이라 다른 곳만 보인다. 부품 이름은 전사에 나온 것(L61·L65)."""
    parts_all = [('DSP', 'us'), ('드라이버', 'us'), ('증폭기', 'cn'), ('광섬유', 'cn'),
                 ('증폭기', 'cn'), ('변환', 'cn'), ('TIA', 'us'), ('리타이머', 'us')]
    h, gap = 44, 8
    ws = [w_of([n]) for n, _ in parts_all]
    inner = sum(ws) + gap * (len(ws) - 1)
    fw = inner + 32
    fx = (W - fw) / 2
    parts, y = [], 22

    def row(y, who, label):
        out = head(fx, y, fw, label)
        fy = y + 10
        # 테두리 배경은 줄마다 같다 — 다른 것은 부품 색만이어야 견줌이 된다(2026-09-02)
        out += ['  <rect x="%g" y="%g" width="%g" height="%g" rx="10" class="fig-outside"/>'
                % (fx, fy, fw, h + 32)]
        x = fx + 16
        for (n, c), w in zip(parts_all, ws):
            out += box(x, fy + 16, w, h, [n], 'fig-agent' if c == who else 'fig-box')
            x += w + gap
        return out, fy + h + 32

    r1, y1 = row(y, 'us', '미국이 만드는 부품')
    r2, y2 = row(y1 + 26, 'cn', '중국이 맡는 부품 — 조립도 중국')
    parts += r1 + r2
    parts += legend([('fig-agent', '그 나라가 맡는 것'), ('fig-box', '아닌 것')], y2 + 16)
    return svg(y2 + 42, parts,
               '같은 트랜시버 모듈을 두 줄로 그렸다. 윗줄은 미국이 만드는 부품(DSP·드라이버·TIA·리타이머)만 짙고, 아랫줄은 중국이 맡는 부품(증폭기 둘·광섬유 접속·변환 회로)과 모듈 테두리(조립)가 짙다')


def _op_chain():
    """광트랜시버 밸류체인 끝에서 끝까지 — 부품(미국) → 광원(Lumentum·Coherent) → 조립(중국) → 구축(하이퍼스케일러).
    급소인 조립만 짙게. 두 층만 뽑으면 층 셋으로 읽혀서 전체를 그린다(2026-09-02)."""
    h = 3 * LH + 22
    # 사슬은 넷 다 그리고, 이 절이 말하는 두 단(광원·조립)만 짙게
    row, _x = eband([(['부품·미국', 'DSP', 'TIA'], 'fig-box'), ('>', ''),
                     (['광원 부품', '루멘텀', '코히런트'], 'fig-agent'), ('>', ''),
                     (['조립·중국', '약 50%', '27~34%'], 'fig-agent'), ('>', ''),
                     (['구축', 'Azure'], 'fig-box')], 30, h)
    parts = row + legend([('fig-agent', '이 절이 말하는 두 단')], 30 + h + 16)
    return svg(30 + h + 42, parts,
               '광트랜시버 밸류체인은 미국 부품에서 광원, 중국 조립을 거쳐 하이퍼스케일러 구축으로 간다. 이 절이 말하는 두 단은 광원과 조립이다')


def _op_fork():
    """규제 발표 뒤 갈림 — 증설(되돌릴 수 없음) / 규제가 뒤집힘(설비가 남음). 그래서 아무도 첫 갈래를 안 간다."""
    h = 2 * LH + 22
    tw = w_of(['금지안 발표 — 되돌릴 수 있는 결정'])
    parts = box((W - tw) / 2, 24, tw, 44, ['금지안 발표 — 되돌릴 수 있는 결정'], 'fig-stage')
    lw = rw = max(w_of(['증설한다', '건물·장비·라인']), w_of(['기다린다', '공급이 빈다']),
                  w_of(['몇 달 뒤 뒤집히면', '설비가 통째로 남는다']))  # 갈래 상자는 한 폭(2026-09-02)
    lx, rx = 60.0, W - 60.0 - rw
    y2 = 24 + 44 + 40
    parts += vline(W / 2, 68, 88, arrow_=False) + hline(lx + lw / 2, rx + rw / 2, 88)
    parts += vline(lx + lw / 2, 88, y2 - 2) + vline(rx + rw / 2, 88, y2 - 2)
    parts += box(lx, y2, lw, h, ['증설한다', '건물·장비·라인'], 'fig-outside')
    parts += box(rx, y2, rw, h, ['기다린다', '공급이 빈다'], 'fig-agent')
    nw = lw
    parts += box(lx + lw / 2 - nw / 2, y2 + h + 22, nw, h, ['몇 달 뒤 뒤집히면', '설비가 통째로 남는다'], 'fig-outside')
    parts += vline(lx + lw / 2, y2 + h + 2, y2 + h + 20)
    return svg(y2 + 2 * h + 36, parts,
               '설비를 늘리는 결정은 되돌릴 수 없고 정부의 결정은 되돌릴 수 있다. 몇 달 뒤 뒤집히면 설비가 통째로 남으니 아무도 증설 쪽을 고르지 않는다')


def _op_finance():
    """앤스로픽이 Nvidia GPU 를 더 확보하려고 꿴 부품 넷 — 왼쪽에서 오른쫽으로, 끝에 낮은 금리."""
    h = 2 * LH + 22
    row, _x = eband([(['Nvidia', '할당'], 'fig-box'), ('>', ''), (['전력'], 'fig-box'), ('>', ''),
                     (['운영', '비트디어'], 'fig-box'), ('>', ''), (['재무제표', 'Volta'], 'fig-agent')], 30, h)
    parts = row
    return svg(30 + h + 16, parts,
               'GPU 를 더 원하면 Nvidia 할당·전력·운영할 사람·담보가 될 재무제표 넷이 필요하다. 채굴 업체는 운영은 하되 장부에 부채를 못 얹고, Volta 가 판 것은 아직 아무것도 안 적힌 장부다')


OP = '2026-08-11-china-optical-ban'


# ══ 하이퍼스케일러 CDS (2026-07-29) 전략 판 ═══════════════════════════════
# 값은 전사의 것만 — 28나노·7나노·2나노·3배. 계층과 순위는 상태다.

def _cds_layers():
    """메모리 계층 셋 — 위아래 층. 빠른 것이 위. 각 층 옆에 제약."""
    rows = [('SRAM', ['가장 빠름 · 트랜지스터', '면적 크고 비쌈 · 용량 모자람'], 'fig-box'),
            ('HBM', ['DRAM 을 3D 로 쌓아 칩 옆에', '대역폭'], 'fig-agent'),
            ('DRAM', ['용량 크고', '대역폭 낮음'], 'fig-box')]
    lw = w_of([r[0] for r in rows]); rw = w_of(*[r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 30, 2 * LH + 22
    for name, note, cls in rows:
        parts += box(x0, y, lw, h, [name], cls)
        parts += box(x0 + lw + gap, y, rw, h, note, 'fig-stage')
        y += h + 10
    return svg(y + 2, parts,
               'SRAM 은 가장 빠르지만 면적을 많이 먹어 용량이 모자라고, HBM 은 DRAM 을 쌓아 칩 옆에 붙여 대역폭을 내며, DRAM 은 용량이 크고 대역폭이 낮다')


def _cds_rank():
    """수익성 순위와 대체 불가능성 순위가 어긋나 있다 — 같은 두 칸(DRAM·HBM)을 두 줄로, 줄마다 1위만 짙게."""
    L, R = 0.0, 272.0
    h = 2 * LH + 22
    parts = head(L, 22, 248, '지금 비싸게 팔리는 것') + head(R, 22, 248, '대체할 수 없는 자리')
    for x0, top in [(L, 'DRAM'), (R, 'HBM')]:
        items = [(['DRAM', '웨이퍼 모자람'], 'fig-agent' if top == 'DRAM' else 'fig-box'),
                 (['HBM', '웨이퍼 3장'], 'fig-agent' if top == 'HBM' else 'fig-box')]
        ws = [w_of(l) for l, _ in items]
        x = x0 + (248 - (sum(ws) + 14)) / 2
        for (l, c), w in zip(items, ws):
            parts += box(x, 36, w, h, l, c); x += w + 14
    parts += legend([('fig-agent', '그 줄의 1위')], 36 + h + 16)
    return svg(36 + h + 42, parts,
               '같은 두 칸을 두 줄로 그렸다. 지금 비싸게 팔리는 것은 웨이퍼가 모자란 DRAM 이고, 대체할 수 없는 자리는 HBM 이다 — 두 순위가 어긋나 있다')


def _cds_litho():
    """이머전 DUV 로 어디까지 가나 — 가로 흐름. 단일 노광 28나노 → 멀티패터닝 7나노(한계) → 2나노는 EUV."""
    h = 2 * LH + 22
    row, _x = eband([(['단일 노광', '28나노'], 'fig-agent'), ('>', ''),
                     (['멀티패터닝', '7나노 — 한계'], 'fig-agent'), ('>', ''),
                     (['2나노', 'EUV 가 필요'], 'fig-outside')], 30, h)
    parts = row + legend([('fig-agent', '이머전 DUV 로 닿는 곳'), ('fig-outside', '못 닿는 곳')], 30 + h + 16)
    return svg(30 + h + 42, parts,
               '이머전 DUV 는 한 번 노광으로 28나노, 멀티패터닝으로 7나노까지 가고 거기가 한계다. 2나노는 EUV 가 필요하다')


CDS = '2026-07-29-hyperscaler-cds'


# ══ PicoJool VCSEL (2026-07-16) 전략 판 ═══════════════════════════════════
# 값은 전사의 것만 — 8·16·32 레인, 200G·100G·50G, 1×4·4×16=64, 1.6T·12.8T.

def _pj_lanes():
    """같은 1.6테라비트를 채우는 세 구성 — 레인 하나가 네모 하나. 8·16·32 는 전사의 수."""
    rows = [('8레인 × 200G PAM4', 8), ('16레인 × 100G LPO', 16), ('32레인 × 50G NRZ', 32)]
    parts, y = [], 24
    tw = 11; gap = 3
    for label, n in rows:
        parts += head(0, y + 2, W, label)
        x = (W - (n * tw + (n - 1) * gap)) / 2
        for k in range(n):
            parts += _rect(x + k * (tw + gap), y + 12, tw, 16, 'fig-agent')
        y += 12 + 16 + 22
    return svg(y + 2, parts,
               '같은 1.6테라비트를 8레인 × 200G, 16레인 × 100G, 32레인 × 50G 셋으로 채운다. 네모 하나가 레인 하나다')


def _pj_constraint():
    """제약이 걸린 자리 셋 — 같은 세 칸(기판·파운드리·조립 장비)을 두 줄로, 인듐인은 셋 다 걸리고 갈륨비소는 안 걸린다."""
    h = 44
    stages = ['기판 원재료', '웨이퍼 공정', '뒷단 조립 장비']
    ws = [w_of([t]) for t in stages]; gap = 12
    inner = sum(ws) + gap * 2
    fx = (W - (inner + 32)) / 2
    parts, y = [], 22
    for label, blocked in [('인듐인(InP) — 단일모드', {0, 1, 2}), ('갈륨비소(GaAs) — VCSEL', set())]:
        parts += head(fx, y, inner + 32, label)
        fy = y + 10
        parts += _rect(fx, fy, inner + 32, h + 32, 'fig-outside')
        x = fx + 16
        for k, (t, w) in enumerate(zip(stages, ws)):
            parts += box(x, fy + 16, w, h, [t], 'fig-agent' if k in blocked else 'fig-box'); x += w + gap
        y = fy + h + 32 + 26
    parts += legend([('fig-agent', '제약이 걸린 자리'), ('fig-box', '안 걸림')], y - 10)
    return svg(y + 16, parts,
               '같은 세 자리를 두 줄로 그렸다. 인듐인은 기판 원재료부터 웨이퍼 공정, 뒷단 조립 장비까지 셋 다 걸리고, 갈륨비소는 어디도 안 걸린다')


def _pj_array():
    """엣지발광은 한 줄(1×4), 표면발광은 판(4×16 = 64채널). 칸 수가 전사의 값이다."""
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '엣지발광 — 한 줄로만') + head(R, 22, 248, '표면발광 — 판으로')
    t = 12; g = 3
    x = L + (248 - (4 * t + 3 * g)) / 2
    for k in range(4):
        parts += _rect(x + k * (t + g), 60, t, t, 'fig-box')
    parts += head(L, 36 + 4 * (t + g) + 16, 248, '1×4')
    x0 = R + (248 - (16 * t + 15 * g)) / 2
    for r in range(4):
        for c in range(16):
            parts += _rect(x0 + c * (t + g), 36 + r * (t + g), t, t, 'fig-agent')
    parts += head(R, 36 + 4 * (t + g) + 16, 248, '4×16 = 64채널')
    return svg(36 + 4 * (t + g) + 30, parts,
               '엣지에서 빛을 내는 소자는 1×4 처럼 한 줄로만 늘어서고, 표면에서 빛을 내는 소자는 4×16 = 64채널 판으로 깔린다')


def _pj_chain():
    """광소자 밸류체인 끝에서 끝까지 — PicoJool 이 맡는 설계만 짙게."""
    h = 3 * LH + 22
    row, _x = eband([(['설계'], 'fig-agent'), ('>', ''),
                     (['에피', '웨이퍼'], 'fig-box'), ('>', ''),
                     (['웨이퍼', '공정', 'WIN'], 'fig-box'), ('>', ''),
                     (['다이싱'], 'fig-box'), ('>', ''),
                     (['모듈', '통합', '파트너'], 'fig-box')], 30, h)
    parts = row + legend([('fig-agent', 'PicoJool 이 하는 것')], 30 + h + 16)
    return svg(30 + h + 42, parts,
               '설계에서 모듈까지 다섯 단 중 PicoJool 이 맡는 것은 설계(에피 층과 캐비티)뿐이다. 웨이퍼 공정은 대만 WIN, 모듈은 통합 파트너가 한다')


PJ = '2026-07-16-picojool-yuen'


# ══ 공용 — 같은 대상을 줄마다 (누가 무엇을 맡나 · 무엇이 어디까지 하나) ═══════════

def _same_rows(stages, rows, leg, cap):
    """같은 칸들을 줄마다 한 번씩 그리고 줄마다 켜진 칸만 짙게. 테두리는 줄마다 같다."""
    h, gap = 44, 12
    ws = [w_of([t]) for t in stages]
    inner = sum(ws) + gap * (len(ws) - 1)
    fx = (W - (inner + 32)) / 2
    parts, y = [], 22
    for label, on in rows:
        parts += head(fx, y, inner + 32, label)
        fy = y + 10
        parts += _rect(fx, fy, inner + 32, h + 32, 'fig-outside')
        x = fx + 16
        for k, (t, w) in enumerate(zip(stages, ws)):
            parts += box(x, fy + 16, w, h, [t], 'fig-agent' if k in on else 'fig-box')
            x += w + gap
        y = fy + h + 32 + 26
    parts += legend(leg, y - 10)
    return svg(y + 16, parts, cap)


def _opt_place(left, rows, cap):
    """플러거블·근접 패키지·공동 패키지 — 같은 보드에 같은 칩과 광 엔진을 두고 둘 사이 전기 배선 길이만 다르게."""
    fw, h = 400.0, 44
    fx = (W - fw) / 2
    pw, ow = w_of([left]), w_of(['광 엔진'])
    parts, y = [], 22
    for label, pos, note in rows:
        parts += head(fx, y, fw, label)
        fy = y + 10
        parts += _rect(fx, fy, fw, h + 32, 'fig-stage')
        px, py = fx + 16, fy + 16
        if pos == 'edge':
            ox = fx + fw - 16 - ow
        elif pos == 'board':
            ox = fx + fw / 2 + 20
        else:
            ox = px + pw + 8
        if pos == 'pkg':
            # 패키지 테두리는 칩보다 먼저 그린다 — 뒤에 그리면 흰 채움이 칩을 덮는다
            parts += ['  <rect x="%g" y="%g" width="%g" height="%g" rx="7" class="fig-outside"/>'
                      % (px - 6, py - 7, (ox + ow + 6) - (px - 6), h + 14)]
        parts += box(px, py, pw, h, [left], 'fig-box')
        if pos != 'pkg':
            parts += hline(px + pw, ox, py + h / 2)
        parts += box(ox, py, ow, h, ['광 엔진'], 'fig-agent')
        y = fy + h + 32
        if note:
            parts += head(fx, y + 18, fw, note)
            y += 24
        y += 22
    parts += legend([('fig-agent', '광 엔진'), ('fig-stage', '보드'), ('fig-outside', '패키지')], y - 8)
    return svg(y + 18, parts, cap)


# ══ GlobalFoundries (2026-08-07) 전략 판 ═══════════════════════════════════
# 값은 전사의 것만 — 100·200·400기가비트, 2·1·반 미터, 35·15~20·6dB, 20~25·10·5피코줄, 4·8·32대 1.

def _gf_reach():
    """레인 속도별 직결 구리의 도달 거리 — 막대 길이가 미터다. 점선은 랙 하나 높이(2미터)."""
    rows = [('레인당 100기가비트', 2.0, '2미터'), ('200기가비트', 1.0, '1미터'), ('400기가비트', 0.5, '반 미터')]
    lw = w_of([r[0] for r in rows])
    bx = lw + 16
    scale = (W - bx - 96) / 2.0
    parts, y, h = [], 30, 28
    for label, m, t in rows:
        parts += box(0, y, lw, h, [label], 'fig-stage')
        parts += _rect(bx, y, m * scale, h, 'fig-agent')
        parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>' % (bx + m * scale + 8, y + h / 2 + 6, t)]
        y += h + 14
    xr = bx + 2 * scale
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" stroke-dasharray="4 3"/>' % (xr, 22, xr, y - 6)]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">랙 하나 높이</text>' % (xr, 14)]
    return svg(y + 4, parts, '직결 구리는 레인당 100기가비트에서 2미터, 200기가비트에서 1미터, 400기가비트에서 반 미터를 간다. 랙 하나 높이가 2미터다')


def _gf_place():
    return _opt_place('프로세서', [
        ('플러거블 — 랙 가장자리', 'edge', '35dB · 20~25피코줄 · DSP 필요'),
        ('NPO — 같은 보드 위', 'board', '15~20dB · 10피코줄 · 리니어'),
        ('CPO — 패키지 안', 'pkg', '6dB 안팎 · 5피코줄 미만'),
    ], '같은 보드에서 광 엔진을 프로세서 쪽으로 당길수록 전기 배선이 짧아지고 손실과 비트당 에너지가 준다')


def _gf_pam():
    """PAM4 와 NRZ — 같은 높이 안에 레벨 넷과 둘. 레벨 사이 틈이 곧 수신 여유다."""
    L, R = 0.0, 272.0
    pw, top, hh = 248.0, 44.0, 84.0
    parts = head(L, 22, pw, 'PAM4 — 심볼당 2비트') + head(R, 22, pw, 'NRZ — 심볼당 1비트')
    for x0, n in [(L, 4), (R, 2)]:
        parts += _rect(x0 + 24, top - 8, pw - 48, hh + 16, 'fig-stage')
        for k in range(n):
            yy = top + k * (hh / (n - 1))
            parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x0 + 40, yy, x0 + pw - 40, yy)]
    parts += head(L, top + hh + 36, pw, '레벨 넷 — 틈이 좁다') + head(R, top + hh + 36, pw, '레벨 둘 — 틈이 넓다')
    return svg(top + hh + 48, parts, 'PAM4 는 같은 진폭 안에 레벨 넷을 두어 틈이 좁고, NRZ 는 레벨 둘이라 틈이 넓다')


def _gf_laser():
    """레이저 하나가 먹이는 파이버 수 — 4 · 8 · 32. 작은 네모 하나가 파이버 한 가닥이다."""
    rows = [('지금 — 4대 1', 4), ('플러거블이 가는 곳 — 8대 1', 8), ('OCI 규격 — 32대 1', 32)]
    lw = w_of(['레이저'])
    tw, g = 10, 3
    parts, y = [], 24
    for label, n in rows:
        parts += head(0, y, W, label)
        by = y + 10
        parts += box(0, by, lw, 26, ['레이저'], 'fig-agent')
        x = lw + 14
        parts += hline(lw, x, by + 13)
        for k in range(n):
            parts += _rect(x + k * (tw + g), by + 6, tw, 14, 'fig-box')
        y = by + 26 + 24
    return svg(y - 4, parts, '레이저 하나가 지금은 파이버 넷을, 플러거블은 여덟을, OCI 규격은 서른둘을 먹인다')


def _gf_stack():
    """Scale 광 엔진의 세 층과 누가 만드나 — 위에서 아래로 전자 IC · 광자 IC · 마이크로 광학과 커넥터."""
    rows = [('전자 IC', '자사 공정 또는 고객 웨이퍼', 'fig-box'),
            ('광자 IC', '자사 100%', 'fig-agent'),
            ('마이크로 광학 · 커넥터', '외부 제조 · 자사 조립·시험', 'fig-box')]
    lw = w_of([r[0] for r in rows]); rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 30, 44
    for name, note, cls in rows:
        parts += box(x0, y, lw, h, [name], cls)
        parts += box(x0 + lw + gap, y, rw, h, [note], 'fig-stage')
        y += h + 10
    return svg(y + 2, parts, '전자 IC 아래 광자 IC, 그 아래 마이크로 광학과 탈착식 파이버 커넥터. 광자 IC 만 100% 자사다')


GF = '2026-08-07-globalfoundries-barber'


# ══ Astera Labs (2026-08-04) 전략 판 ═══════════════════════════════════════
# 값은 전사의 것만 — 32·64·128기가전송, 2027. 눈 다이어그램은 값이 없는 그림이다.

def _al_eye():
    """눈 다이어그램 — 같은 네 궤적을 두 판에. 오른쪽은 지터로 흔들려 가운데 틈이 메워진다."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '눈이 열렸다') + head(R, 22, pw, '눈이 닫혔다')
    ym, amp = 96.0, 40.0

    def traces(x0, dx=0.0, dy=0.0, thin=False):
        a, b = x0 + 36 + dx, x0 + pw - 36 + dx
        xm = (a + b) / 2
        t, bt = ym - amp + dy, ym + amp + dy
        st = ' style="stroke-width:.9"' if thin else ''
        out = ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"%s/>' % (a, t, b, t, st),
               '  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"%s/>' % (a, bt, b, bt, st),
               '  <path d="M%g %g C%g %g %g %g %g %g" class="fig-arw"%s/>' % (a, t, xm, t, xm, bt, b, bt, st),
               '  <path d="M%g %g C%g %g %g %g %g %g" class="fig-arw"%s/>' % (a, bt, xm, bt, xm, t, b, t, st)]
        return out
    parts += _rect(L + 24, ym - amp - 16, pw - 48, 2 * amp + 32, 'fig-stage')
    parts += _rect(R + 24, ym - amp - 16, pw - 48, 2 * amp + 32, 'fig-stage')
    parts += traces(L)
    for dx in (-18, -9, 0, 9, 18):
        for dy in (-7, 0, 7):
            parts += traces(R, dx, dy, thin=True)
    return svg(ym + amp + 36, parts, '왼쪽은 0 과 1 사이 틈이 열려 있고, 오른쪽은 궤적이 시간과 전압에서 흔들려 틈이 메워졌다')


def _al_gen():
    """PCIe 세대 — 초당 기가전송. Gen6 가 블랙웰 세대에 들어간 것, Gen7 은 앞으로."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '초당 기가전송')
    row, _x = eband([(['Gen5', '32'], 'fig-box'), ('>', ''),
                     (['Gen6', '64 · PAM4'], 'fig-agent'), ('>', ''),
                     (['Gen7', '128'], 'fig-outside')], 36, h)
    parts += row + legend([('fig-agent', '블랙웰 세대'), ('fig-outside', '앞으로')], 36 + h + 16)
    return svg(36 + h + 42, parts, 'PCIe Gen5 는 초당 32기가전송, Gen6 는 64 에 PAM4, Gen7 은 128 이다')


def _al_two():
    return _same_rows(['송신 등화', 'CTLE', 'DFE', 'CDR'],
                      [('리드라이버 — 앞의 둘만', {0, 1}), ('리타이머 — 넷 다', {0, 1, 2, 3})],
                      [('fig-agent', '하는 것'), ('fig-box', '안 하는 것')],
                      '같은 네 손질 중 리드라이버는 송신 등화와 CTLE 둘만 하고, 리타이머는 넷을 다 한다')


def _al_three():
    """같은 신호 손질 칩이 트레이 안·케이블 안·스위치 안 세 자리에 — 제품 이름만 다르다."""
    fw, gap = 150.0, 20.0
    x0 = (W - (3 * fw + 2 * gap)) / 2
    cw = w_of(['신호 손질 칩'])
    parts, y = [], 22
    for k, (place, prod) in enumerate([('트레이 안', 'Aries'), ('케이블 안', '타우로스'), ('스위치 안', '스코피오')]):
        fx = x0 + k * (fw + gap)
        parts += head(fx, y, fw, place)
        parts += _rect(fx, y + 10, fw, 92, 'fig-stage')
        parts += box(fx + (fw - cw) / 2, y + 26, cw, 44, ['신호 손질 칩'], 'fig-agent')
        parts += head(fx, y + 96, fw, prod)
    return svg(y + 112, parts, '같은 신호 손질 칩이 트레이 안(Aries)·케이블 안(타우로스)·스위치 안(스코피오)에 들어간다')


def _al_order():
    """AMD 와 브로드컴 — 순서. 없는 것은 점선, 갈림을 정한 한 걸음만 짙게."""
    return _chain_down([(['AMD 가 개방형 UALink 스위치를 찾았다', '시장에 없었다'], 'fig-outside'),
             (['브로드컴 토마호크(이더넷)로 갔다'], 'fig-box'),
             (['브로드컴이 UALink 컨소시엄에서 나갔다'], 'fig-agent'),
             (['헬리오스는 UALOE 로 간다'], 'fig-box'),
             (['2027 — UALink 스코피오·마벨이 나온다', '그때 갈아타나'], 'fig-outside')],
                       'UALink 스위치가 없어 브로드컴 이더넷으로 갔고, 소켓을 잡은 브로드컴이 UALink 에서 나갔다. 2027 년 UALink 스위치가 나올 때 갈아타는지가 물음이다')


AL = '2026-08-04-astera-labs'


# ══ 데이터센터 인터커넥트 (2026-07-25) 전략 판 ══════════════════════════════
# 값은 전사의 것만 — 2미터, 열두 랙, 30~80킬로미터, 25·78층, 100·200·400·800기가, 1.6·2.4테라, 2023~24, 25~26.

def _dc_layers():
    """망의 층 — 안에서 밖으로. 이 회차가 다루는 셋만 실선, 안 다루는 둘은 점선."""
    rows = [('스케일인', '트레이 안 — 오늘은 안 다룬다', 'fig-outside'),
            ('스케일업', '랙 하나 — 2미터', 'fig-agent'),
            ('스케일아웃', '랙과 랙 — 슈퍼팟이면 열두 랙', 'fig-box'),
            ('스케일어크로스', '캠퍼스 사이 — 30~80킬로미터', 'fig-box'),
            ('스케일어보브', '우주 — 위성 주파수', 'fig-outside')]
    lw = w_of([r[0] for r in rows]); rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 30, 44
    for name, note, cls in rows:
        parts += box(x0, y, lw, h, [name], cls)
        parts += box(x0 + lw + gap, y, rw, h, [note], 'fig-stage')
        y += h + 10
    return svg(y + 2, parts, '안에서 밖으로 스케일인·업·아웃·어크로스·어보브. 이 회차는 가운데 셋을 다룬다')


def _dc_gens():
    """속도 세대 — 위에서 아래로. 겹쳐 가는 순서다."""
    return _chain_down([(['2020년대 초 — 100·200기가가 대부분'], 'fig-box'),
             (['2023~2024 — 400기가가 떠오른다'], 'fig-box'),
             (['800기가가 들어온다', '400기가는 25·26년에 스러진다'], 'fig-box'),
             (['1.6테라 — 시작', '레인당 200기가 × 여덟 레인'], 'fig-agent'),
             (['2.4테라(레인당 300기가)를 거칠 가능성'], 'fig-outside')],
                       '100·200기가에서 400, 800, 1.6테라로 두 배씩 뛰고, 2.4테라를 한 번 거칠 가능성이 돈다')


def _dc_layers78():
    """PCB 층수 — 같은 폭의 판에 층을 줄로 그렸다. 줄 수가 25 와 78 이다."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '보통 PCB · 25층') + head(R, 22, pw, '다음 세대 기판 · 78층')
    sp, bw = 1.7, 150.0
    base = 40 + 78 * sp + 10
    for x0, n in [(L, 25), (R, 78)]:
        bx = x0 + (pw - bw) / 2
        hh = n * sp + 8
        parts += _rect(bx, base - hh, bw, hh, 'fig-stage')
        for k in range(n):
            yy = base - 4 - k * sp
            parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" style="stroke-width:.8"/>' % (bx + 8, yy, bx + bw - 8, yy)]
    return svg(base + 12, parts, '보통 PCB 는 25층, Nvidia 다음 세대 미드플레인은 78층으로 알려져 있다. 줄 하나가 층 하나다')


def _dc_place():
    return _opt_place('스위치 칩', [
        ('플러거블 — 스위치 앞판에 꽂는다', 'edge', '기판 위 긴 경로 — DSP 가 메운다'),
        ('근접 패키지 광학 — 같은 보드 위', 'board', ''),
        ('공동 패키지 광학 — 패키지 옆에', 'pkg', '구리는 얇은 조각만 · 에너지 3분의 1'),
    ], '광 엔진을 스위치 칩 쪽으로 당길수록 기판 위 전기 경로가 짧아져 DSP 가 빠지고, 패키지 옆이면 에너지가 3분의 1 이 된다')


DC = '2026-07-25-datacenter-interconnects'


def _chain_down(steps, cap):
    """인과·순서 사슬 — 위에서 아래로, 상자 사이는 화살표. **상자는 전부 한 크기**다 —
    폭은 가장 긴 글, 높이는 줄이 가장 많은 상자에 맞춘다. 크기가 다르면 중요도가 다른 것처럼
    읽힌다(2026-09-02 사용자 지적). 짙은 상자 하나만 색으로 다르다."""
    w = w_of(*[l for l, _ in steps])
    h = max(len(l) for l, _ in steps) * LH + 22
    parts, y = [], 26
    for k, (lines, cls) in enumerate(steps):
        parts += box((W - w) / 2, y, w, h, lines, cls)
        y += h
        if k < len(steps) - 1:
            parts += down(W / 2, y, y + 20)
            y += 22
    return svg(y + 4, parts, cap)


def _gf_wafer():
    """200mm → 300mm — 같은 꼴의 원 둘, 지름 비는 전사의 50%. 사이 화살표가 인과다."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '전 — 200mm 웨이퍼') + head(R, 22, pw, '후 — 300mm 웨이퍼')
    cy, r1, r2 = 122.0, 50.0, 75.0
    parts += ['  <circle cx="%g" cy="%g" r="%g" class="fig-box"/>' % (L + pw / 2, cy, r1)]
    parts += ['  <circle cx="%g" cy="%g" r="%g" class="fig-agent"/>' % (R + pw / 2, cy, r2)]
    parts += arrow(L + pw / 2 + r1 + 12, R + pw / 2 - r2 - 12, cy)
    parts += head(0, cy + r2 + 28, W, '지름이 50% 커지면 웨이퍼당 다이는 2.25배')
    return svg(cy + r2 + 40, parts, '200mm 에서 300mm 로 옮기면 지름이 50% 커지고 웨이퍼당 다이는 그 제곱인 2.25배가 된다')


def _gf_chain():
    return _chain_down([(['레인 속도가 두 배 오른다'], 'fig-box'),
                        (['구리가 가는 거리가 절반이 된다'], 'fig-box'),
                        (['스위치를 랙 가운데로 내린다 — 한 번만 쓰는 수'], 'fig-box'),
                        (['랙은 4분의 1로 못 줄인다', '광으로 갈 수밖에 없다'], 'fig-agent')],
                       '속도가 오르면 구리 거리가 줄고, 스위치를 가운데로 내리는 수는 한 번뿐이라 그다음은 광이다')


def _al_chain():
    return _chain_down([(['속도가 한 세대 오른다'], 'fig-box'),
                        (['눈을 열어 둘 수 있는 거리가 준다'], 'fig-box'),
                        (['보드 크기는 그대로라', '비어 있던 자리에 칩 하나가 들어간다'], 'fig-agent'),
                        (['부품 수요가 GPU 수요와 따로 는다'], 'fig-box')],
                       '속도가 오르면 눈을 열어 둘 거리가 줄고, 보드는 그대로라 칩 자리가 새로 생긴다')


def _al_nic():
    """GPU 와 NIC — 레퍼런스(멀다) · 블랙웰 계획(붙인다) · 실제 배치(다시 멀어진다). 같은 두 칩, 사이만 다르다."""
    fw, h = 400.0, 44
    fx = (W - fw) / 2
    gw, nw, rw = w_of(['GPU']), w_of(['NIC']), w_of(['리타이머'])
    rows = [('레퍼런스 설계 — 멀다', 'far', '리타이머가 든다'),
            ('블랙웰 계획 — NIC 을 GPU 에 붙인다', 'near', '리드라이버로 충분하지 않겠나 — 걱정'),
            ('실제 배치 — 커스텀으로 다시 멀어진다', 'far', '리타이머가 남는다')]
    parts, y = [], 22
    for label, pos, note in rows:
        parts += head(fx, y, fw, label)
        fy = y + 10
        parts += _rect(fx, fy, fw, h + 32, 'fig-stage')
        gx, py = fx + 16, fy + 16
        parts += box(gx, py, gw, h, ['GPU'], 'fig-box')
        if pos == 'far':
            nx = fx + fw - 16 - nw
            rx = (gx + gw + nx) / 2 - rw / 2
            parts += hline(gx + gw, rx, py + h / 2) + hline(rx + rw, nx, py + h / 2)
            parts += box(rx, py, rw, h, ['리타이머'], 'fig-agent')
        else:
            nx = gx + gw + 8
        parts += box(nx, py, nw, h, ['NIC'], 'fig-box')
        y = fy + h + 32
        parts += head(fx, y + 18, fw, note)
        y += 46
    return svg(y + 2, parts, '같은 GPU 와 NIC 을 세 번 그렸다. 멀면 사이에 리타이머가 들고, 붙이면 빠질 것 같았는데, 실제 배치가 갈라져 다시 멀어졌다')


def _dc_power():
    return _chain_down([(['플러거블 모듈 하나 30와트쯤', '양 끝 둘 × 케이블 5,000개'], 'fig-box'),
                        (['랙은 이미 100~200킬로와트, Kyber 는 600', '거기에 10~20% 를 더 얹는 셈'], 'fig-box'),
                        (['Nvidia — 스케일업에 플러거블을 안 쓴다'], 'fig-agent')],
                       '모듈 30와트가 양 끝 둘씩 5,000개면 이미 전력에 눌린 랙에 10~20% 를 더 얹는 셈이라 Nvidia 는 스케일업에 플러거블을 안 쓴다')

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]   머리에 「|문단 앞머리」를 붙이면 그 문단 앞
FIGS = {
    (GF, 'strategy'): [
        ('1.|Barber가 이 회차에서', '레인 속도별 구리가 가는 거리', _gf_reach(),
         '막대 길이가 미터다. 레인당 100기가비트에서 2미터, 200기가비트에서 1미터, 400기가비트에서 반 미터(L81). 점선이 랙 하나 높이라, 200기가비트부터 스위치를 랙 가운데로 내려야 하고 400기가비트에서는 그 수도 안 먹힌다.'),
        ('1.|문제는 이 대응이', '속도가 오르면 왜 광으로 가나', _gf_chain(),
         '레인 속도가 두 배 오르면 구리가 가는 거리가 절반이 되고, 스위치를 랙 가운데로 내리는 수는 랙 높이가 바닥이라 한 번뿐이다(L81). 그다음은 광이다.'),
        ('2.|수요가 저렇게 서면', '200mm 에서 300mm 로 — 전과 후', _gf_wafer(),
         '같은 꼴의 웨이퍼 둘이다. 지름이 50% 커지면 면적은 그 제곱이라 웨이퍼당 다이가 2.25배 나오고, 같은 장수를 돌려도 물량이 두 배 넘게 나온다(L73). 경쟁사 대부분은 아직 200mm 에 있다.'),
        ('3.|손실이 어디서 나는지가', '광 엔진을 어디까지 안으로 들이나', _gf_place(),
         '같은 보드에 같은 프로세서와 광 엔진을 세 번 그렸다. 다른 것은 둘 사이 전기 배선 길이뿐이다. 플러거블 약 35dB·20~25피코줄, NPO 15~20dB·10피코줄쯤, CPO 6dB 안팎(다른 자리에서는 3dB)·5피코줄 미만(L91~L97). 손실이 줄면 그것을 메우던 DSP 가 빠진다.'),
        ('5.|바꾼 방향이 뒤로다', 'PAM4 와 NRZ — 레벨 사이 틈', _gf_pam(),
         '같은 진폭 안에 PAM4 는 레벨 넷을, NRZ 는 둘을 둔다(L139·L141). 틈이 좁으면 수신에 전력을 많이 쓰거나 잡음을 극도로 낮춰야 한다. OCI 가 NRZ 로 돌아간 대신 속도를 50기가헤르츠로 낮추고 파장 넷으로 200기가비트를 맞춘다. 값은 레벨 수뿐이다.'),
        ('5.|레이저 쪽 셈도', '레이저 하나가 먹이는 파이버 수', _gf_laser(),
         '작은 네모 하나가 파이버 한 가닥이다. 지금 4대 1, 플러거블은 8대 1로 가는 중, OCI 규격은 32대 1까지(L155). 파장을 늘려도 레이저 수는 그만큼 늘지 않는다.'),
        ('6.|Scale 플랫폼은', 'Scale 광 엔진의 세 층과 누가 만드나', _gf_stack(),
         '위에서 아래로 전자 IC·광자 IC·마이크로 광학과 탈착식 파이버 커넥터(L165). 광자 IC 만 100% 자사이고, 전자 IC 는 자사 공정이거나 고객이 3나노·2나노 웨이퍼를 들고 오면 조립·시험만, 마이크로 광학은 외부 제조에 조립·시험만 자사다(L169).'),
    ],
    (AL, 'strategy'): [
        ('1.|얼마나 빠른지가', 'PCIe 세대와 초당 전송 수', _al_gen(),
         'Gen5 는 초당 32기가전송, Gen6 는 64기가전송에 PAM4, Gen7 은 128기가전송이다(L53·L81). 블랙웰 세대에 들어간 것은 Gen6 제품이었을 것이라고 Vik 은 봤다(L143).'),
        ('1.|이 다섯이 한 그림으로', '눈 다이어그램 — 열린 눈과 닫힌 눈', _al_eye(),
         '같은 네 궤적을 두 판에 그렸다. 왼쪽은 0 으로 읽을 아래와 1 로 읽을 위 사이에 틈이 있고(L73·L75), 오른쪽은 궤적이 시간(지터)과 전압에서 흔들려 그 틈이 메워졌다. 값은 없는 그림이다 — 파형을 수천 장 겹쳐 그리면 이 모양이 된다는 것이 Austin 의 설명이다(L77).'),
        ('1.|업계에 보이는 규칙은', '속도가 오르면 왜 칩 자리가 생기나', _al_chain(),
         '속도가 한 세대 오르면 눈을 열어 둘 수 있는 거리가 줄고(L85), 보드 크기는 그대로라 원래 비어 있던 자리에 칩 하나가 들어간다. 부품 수요가 GPU 수요와 따로 늘어나는 구조다.'),
        ('2.|리드라이버는 ①②만', '리드라이버와 리타이머 — 같은 네 손질 중 무엇을 하나', _al_two(),
         '같은 네 칸을 두 줄로 그렸다. 리드라이버는 송신 등화와 CTLE 둘만, 리타이머는 DFE 와 CDR 까지 넷을 다 한다(L115·L119). 뒤의 둘이 있어야 뭉개진 비트를 제자리에 다시 끼운다.'),
        ('4.|이 잠금이 깨질 뻔한', 'GPU 와 NIC 사이 — 계획과 실제', _al_nic(),
         '같은 GPU 와 NIC 을 세 번 그렸다. 레퍼런스 설계에서는 멀어서 리타이머가 들고, 블랙웰에서 붙이겠다고 하자 리드라이버로 충분하지 않겟느냐는 걱정이 돌았는데(L143), 레퍼런스 그대로 쓴 곳이 적고 커스텀 배치가 많아 거리가 다시 늘었다(L147).'),
        ('5.|나머지 제품군은', '한 기술을 세 자리에', _al_three(),
         '같은 신호 손질 칩이 트레이 안(Aries)·케이블 안(타우로스)·스위치 안(스코피오)에 들어간다(L157·L173). 값을 제대로 받는 곳은 경로 배정을 얹어야 하는 스위치 하나라는 것이 이 글의 읽기다(L161).'),
        ('6.|읽을 것은 순서다', 'AMD 와 브로드컴 — 순서', _al_order(),
         'UALink 스위치가 시장에 없어 AMD 가 브로드컴 토마호크로 갔고, 소켓을 잡은 브로드컴이 UALink 컨소시엄에서 나갔다(L167). 헬리오스는 UALOE 로 간다(L169). 2027 년쯤 UALink 스코피오와 마벨 제품이 나올 때 이미 이더넷으로 들어간 회사들이 갈아타는지가 Vik 의 물음이다(L167).'),
    ],
    (DC, 'strategy'): [
        ('2.|데이터센터 망은 세 층이다', '망의 층 — 안에서 밖으로', _dc_layers(),
         '트레이 안의 스케일인, 랙 하나(2미터)의 스케일업, 슈퍼팟이면 열두 랙을 가로지르는 스케일아웃, 30~80킬로미터의 스케일어크로스, 위성으로 잇는 스케일어보브(L43~L59). 점선 둘은 오늘 안 다룬다고 Vik 이 선을 그은 것이다.'),
        ('4.|속도 세대는 겹쳐서', '속도 세대 — 겹쳐서 간다', _dc_gens(),
         'Vik 이 그래프를 읽어 준 순서다(L153). 1.6테라는 합산 대역폭이라 레인당 200기가 여덟 레인일 수 있고(L155), 다음이 3.2 가 아니라 레인당 300기가짜리 2.4테라일 가능성이 돈다는 것은 Vik 의 전언이다(L157).'),
        ('5.|그런데 속도가 오르면', 'PCB 층수 — 25층과 78층', _dc_layers78(),
         '줄 하나가 층 하나다. 보통의 데이터센터 PCB 는 25층쯤, Nvidia 다음 세대 미드플레인은 78층으로 알려져 있다(L121). 구리를 지키는 값이 이 층수로 나온다는 것이 이 글의 읽기다.'),
        ('6.|전력을 수로 보면', '플러거블이 스케일업에서 밀리는 셈', _dc_power(),
         '모듈 하나 30와트쯤(Vik 의 어림)이 양 끝 둘씩 케이블 5,000개면, 이미 100~200킬로와트를 쓰고 Kyber 세대는 600킬로와트로 이야기되는 랙에 10~20% 를 더 얹는 셈이다(L145). 그래서 Nvidia 는 스케일업에 플러거블을 안 쓰겠다고 말해 왔다는 것이 Vik 의 전언이다.'),
        ('6.|그 전력이 어디서 새는지가', '광 엔진을 스위치 칩 쪽으로 당기기', _dc_place(),
         '같은 보드에 같은 스위치 칩과 광 엔진을 세 번 그렸다. 플러거블은 앞판에서 스위치 실리콘까지 기판 위를 길게 지나 DSP 가 메워야 하고(L159), 같은 보드 위가 근접 패키지 광학, CoWoS·EMIB 로 옆에 붙이면 공동 패키지 광학이다(L163). 에너지가 3분의 1 까지 떨어진다는 것이 Vik 의 말이다(L167).'),
    ],
    (CDS, 'strategy'): [
        ('4.|그런데 밀려나지도', '메모리 계층 셋', _cds_layers(),
         'Vik 이 정리한 계층이다(L69). SRAM 은 가장 빠르지만 트랜지스터라 면적을 많이 먹어 비싸고 용량이 모자란다. HBM 은 DRAM 을 3D 로 쌓아 칩 가까이 붙여 대역폭을 낸다. '
         '대안(KV 캐시 내리기·TurboQuant·델타 어텐션)도 결국 초당 토큰 처리량을 HBM 에 기댄다는 것이 Austin 의 말이다(L67).'),
        ('4.|그래서 지금 갈라진', '수익성 순위와 대체 불가능성 순위', _cds_rank(),
         '같은 두 칸을 두 줄로 그렸다. 지금 비싸게 팔리는 것은 웨이퍼가 모자란 일반 DRAM 이고(HBM 은 같은 비트에 DRAM 웨이퍼가 세 배 든다, L65), 대체할 수 없는 자리는 HBM 이다(L67). '
         '두 순위가 어긋나 있고, 이번 실적 충격이 그 어긋남을 분기 숫자로 드러냈다는 것이 이 글의 읽기다.'),
        ('5.|Austin이 기술', '이머전 DUV 로 어디까지 가나', _cds_litho(),
         '한 번 노광으로 28나노, 멀티패터닝으로 7나노까지 가고 거기가 한계다. 2나노로는 못 간다(L83). 7나노로 오늘 쓸 물건을 만들려면 로직 폴딩과 3D 적층이 붙어야 한다(L85).'),
    ],
    (PJ, 'strategy'): [
        ('3.|Yuen 이 물량', '제약이 걸린 자리 셋', _pj_constraint(),
         '같은 세 자리를 두 줄로 그렸다. 인듐인은 기판 원재료부터 걸리고 파운드리도 출발 재료를 못 받으며 단일모드 정렬 장비도 월 수백만 개 규모로 깔려 있지 않다(L85). 갈륨비소는 제약이 없다는 것이 Yuen 의 말이다(L85).'),
        ('4.|레인당 200기', '같은 1.6테라비트를 채우는 세 구성', _pj_lanes(),
         '네모 하나가 레인 하나다. 8레인 × 200G PAM4, 16레인 × 100G LPO, 32레인 × 50G NRZ 가 같은 1.6테라비트를 낸다(L103~L111). 셋이 같은 200G 소자를 다르게 돌린 것이라는 것이 Yuen 의 논거다(L131). 전력·값은 전사에 없다.'),
        ('5.|더 멀리 가는', '한 줄 대 판', _pj_array(),
         '엣지발광 소자는 1×4 처럼 한 줄로만 늘어서고, 표면발광 소자는 2×4·2×12·2×16 처럼 판으로 깔린다(L125). 오른쪽에 그린 4×16 은 손가락 굵기 커넥터 하나에 든 64채널이고, 200G 로 돌리면 12.8테라비트다(L127). 칸 수는 전사의 값이다.'),
        ('6.|분업 구조는', '광소자에도 팹리스', _pj_chain(),
         '설계에서 모듈까지 다섯 단 중 PicoJool 이 맡는 것은 에피 층과 캐비티 설계뿐이다. 웨이퍼 공정은 대만 WIN Semiconductors, 자른 뒤 모듈 통합은 파트너가 한다(L93·L95). WIN 의 캐파는 주당 웨이퍼 1,000장, 웨이퍼당 VCSEL 24만 개다(L141).'),
    ],
    (TD, 'strategy'): [
        ('2.|어려운 쪽은 그다음이다', '곱셈을 덧셈으로, 그리고 되돌아오기', _td_logflow(),
         '밑이 2인 로그에서 A×B 는 log A + log B 라 곱셈기가 덧셈기가 된다(L127). 어려운 곳은 누산을 위해 선형으로 되돌아오는 자리다 — '
         '룩업 테이블이나 테일러 급수로 가면 번 것을 반납하고(L131), 그 이득을 잃지 않는 방법이 특허다(L133). 절감률은 전사에 없다.'),
        ('3.|모델이 한 칩에', '라우터 뒷면을 그대로 가져왔다', _td_fabric(),
         '고성능 라우터 뒷면은 어느 포트에서 어느 포트로든 40바이트부터 9K 점보 프레임까지 처리하도록 설계돼 있다(L189). '
         '텐서다인은 스케일업 패브릭을 설계하지 않고 그것을 가속기 아래에 가져왔다(L191·L193). 가속기 수 72 는 쿼터랙 값이다(L277).'),
        ('5.|수치가 가장', '쿼터랙 대 풀랙', _td_rack(),
         '13U 에 칩 72개, 랙의 4분의 1, 30킬로와트 공랭(L277·L279) 대 GB300 풀랙 150킬로와트 액랭(L277). '
         '성능이 동급이라는 전제는 이 회차에 값이 없어 그리지 않았다. 19인치 텔코 랙이라 기존 시설에 그대로 들어간다는 것이 겨냥이다(L293).'),
        ('6.|이 회차에서 가장', '자기 손으로 하는 것과 맡긴 것', _td_outsource(),
         '프런트엔드 설계와 컴파일러만 자기 것이고 물리 설계는 Broadcom(L317), 시스템은 HP주니퍼(L329), 양산은 페낭의 Flex(L233·L311)다. '
         '엔지니어 60% 이상이 소프트웨어다(L343). 스타트업이 시스템 인증까지 지면 출시가 밀린다는 것이 이유다(L231).'),
    ],
    (OP, 'strategy'): [
        ('1.|광트랜시버(빛과', '같은 트랜시버, 누가 무엇을 만드나', _op_module(),
         '같은 모듈을 두 줄로 그렸다. 윗줄은 미국이 만드는 부품(DSP·리타이머·드라이버·TIA — Broadcom·Marvell 등, L61)만 짙고, '
         '아랫줄은 중국이 맡는 부품(증폭기 둘·변환 회로·광섬유 접속)만 짙다. 조립도 중국이 한다(L61·L65). 부품 순서는 이 그림의 배치다.'),
        ('1.|주가가 어긋난', '광트랜시버 밸류체인 — 광원과 조립', _op_chain(),
         '끝에서 끝까지다. 부품(DSP·리타이머·드라이버·TIA)은 미국(L61), 고부가 광원(200기가 EML·초고출력 레이저)은 Lumentum·Coherent(L81), 조립은 중국 공급망이 세계의 약 50% 이고 Innolight 한 곳이 27~34% 다(L79), '
         '구축은 Azure·OCI 같은 주체다(L91). 조립이 빠지면 광원 매출도 줄어들지 않겠느냐는 것이 Vik 의 말인데 주가는 광원 쪽이 올랐다(L81·L83).'),
        ('3.|금지가 곧', '되돌릴 수 있는 규제 앞의 갈림', _op_fork(),
         '건물·장비·라인은 되돌릴 수 없고 정부 결정은 되돌릴 수 있다는 Austin 의 「한 방향 문」(L95). 몇 달 뒤 뒤집히면 설비가 남는다는 Vik 의 말(L93)이 왼쪽 갈래 아래에 있다. '
         '그래서 당장 벌어지는 일은 보안 우려를 얻고 구축 능력을 잃는 것 하나다(L87).'),
        ('6.|Austin은 같은', 'GPU 를 더 얻으려면 필요한 부품 넷', _op_finance(),
         'Austin 이 세운 넷이다(L129) — Nvidia 할당 · 전력 · 운영할 사람(Bitdeer 같은 채굴 업체) · 담보가 될 재무제표. 채굴 업체는 부채를 장부에 못 얹고 낮은 금리도 못 받는다. '
         'Vik 이 찾은 Volta 의 논리는 기관급 인프라 자산으로 놓아 낮은 금리로 빌리고 그 위의 컴퓨트를 싸게 파는 것이다(L123·L125). 계약 금액은 판에 안 적었다.'),
    ],
    (GROK, 'strategy'): [
        ('2.|Austin 이 대화', '에이전트가 사는 자리 셋', _grok_places(),
         'Austin 이 나란히 세운 세 경우다(L73). 셋 모두 추론은 클라우드 GPU 이고, 갈리는 것은 에이전트 잡일이 도는 CPU 가 어디 있느냐다. '
         '쉬운 버튼은 그 잡일까지 남의 서버로 옮긴다(L147). 자리는 상태고 값은 없다.'),
        ('3.|Austin 이 세운', '천재 하나, 조수 둘', _grok_genius(),
         'GPU 가 천재, CPU 가 조수라는 Austin 의 비유(L77)를 Vik 이 둘로 쪼갠 것이다(L81·L91·L101). 호스트 CPU 는 같은 방에서 천재를 먹이고, '
         '에이전틱 CPU 랙은 천재가 뱉은 잡일을 받아 다녀온다. 천재와 계속 말하지 않으니 코히어런시가 없어도 된다.'),
        ('5.|Vik 이 곁가지로', '랙은 넷인데 지휘하는 층이 비었다', _grok_layers(),
         '아래는 이 회차에 이름이 나온 랙 넷(L115·L121). Nvidia Dynamo 는 천재를 잘 굴리는 층이지 그 위층이 아니라고 Vik 이 선을 그었다(L125). '
         '맨 위 층은 있는지 없는지 둘 다 모른다고 밝혔고(L133), 후보로 Modular 와 Gimlet Labs 가 나왔다(L129·L135).'),
        ('6.|산수의 항은', '코어 10억 개의 곱셈', _grok_math(),
         'Austin 의 산수다(L145). 항마다 조건이 붙는다 — 사용자 수는 월 200달러가 막고(L63), 사람당 가상머신 하나는 제품 구조일 뿐이고, '
         '에이전트 100개가 코어 100개가 되려면 코어를 붙들고 있어야 하는데 기다리는 일이면 나눠 쓴다(L105). 셋째 항이 가장 헐겁다.'),
    ],
    (JAL, 'strategy'): [
        ('1.|Vik의 결론은 산업을', '아홉 달을 만든 세 요인', _jal_nine_months(),
         '셋이 겹쳐 아홉 달이 됐다(L97). 사람과 백지는 전에도 있던 항이고 AI 도구만 새 항이라는 것이 이 절의 논지다. '
         '셋 중 무엇이 몇 할인지는 전사에 없어 상자 크기를 같게 뒀다.'),
        ('1.|설계 셈법도 달라진다', '주기가 짧으면 덜 욕심내도 된다', _jal_cycle(),
         '잘라낸 기능이 다음 판에 붙는 간격이 곧 욕심의 크기다. 통상은 2~3년(L97)이라 무리해서 넣게 되고, '
         '아홉 달이면 2세대가 이미 테이프아웃에 다가섰고 3세대를 구상 중이라(L95) 곧 다시 붙는다.'),
        ('2.|Austin이 본 것은', '잣대가 다른 이유 — 사이에 판매자가 있나', _jal_yardstick(),
         '위는 상용 실리콘이다 — 설계팀이 AI 랩·하이퍼스케일러에 팔고 그들이 사용자를 상대하니 잣대가 TCO 다(L45·L47). '
         '아래는 할라페뇨 — 설계팀과 사용자 사이에 판매자가 없어 요청당 에너지와 마지막 토큰까지 지연을 잣대로 삼는다(L43).'),
        ('3.|Vik은 균형을 잡아 뒀다', '투기적 디코딩 — 초안이 똑똑할수록 검증이 가볍다', _jal_specdec(),
         '작은 초안 모델이 토큰을 뱉고 큰 모델이 검증한다. 덜 똑똑하면 여덟 개를 뱉어 검증이 무겁고, 똑똑하면 두 개만 뱉어 가볍다(Vik, L159·L161). '
         '여덟과 둘은 Vik 이 든 수다. 이 비율이 워크로드마다 움직이니 칩을 고정 배분하면 한쪽이 논다.'),
        ('3.|GPU 진영이 이 비대칭을 다룬 방법', '추론을 받는 세 구성', _jal_three_configs(),
         '위가 구성, 아래가 이 회차가 붙인 조건이다. 랙 수(NVL72 1대 + Groq 9대 대 할라페뇨 1~2대)는 Austin 의 어림이고(L109), '
         '700W 는 발표 값(L111), 초당 1,000토큰은 GPT-OSS 기준이다(L105).'),
        ('4.|답은 코디자인을 맡은', '가속기마다 HBM 을 나눠 쓰나, 따로 두나', _jal_numa4(),
         '왼쪽이 지금까지의 구조다 — 이웃 가속기들이 HBM 한 덩어리를 나눠 쓰니 연산하려는 순간 데이터가 없다(L129). '
         '오른쪽이 할라페뇨다 — 가속기마다 HBM 을 따로 두고 전용 버스로 붙인다(L131). '
         '가속기 넷은 보기용 수다. 실제 랙은 128칩이고 몇 개가 한 HBM 을 나눠 쓰는지는 전사에 없다.'),
        ('5.|Austin은 발표 슬라이드의', '밸류체인에서 어디에 새 수요가 생기나', _jal_ladder(),
         '모델랩이 실리콘까지 내려와도 밸류체인 아래쪽 전부에 새 수요가 생기는 게 아니다. CPU 는 대체재가 널렸고(L117) 파운드리는 대안이 없어 그대로 간다. '
         '새 수요가 생기는 곳은 메모리와 스케일업 망 둘이다. 시스템 조립은 SemiAnalysis 의 추정이다(L119).'),
        ('5.|망이 가장 구체적이다', '스케일업은 랙 안이 아니다', _jal_domain(),
         '랙 16대가 한 스케일업 도메인이다(L145). 랙 하나 128칩은 Tomahawk 6 로 칩당 초당 600기가비트, 16대 2,048칩은 ESUN 으로 초당 200기가비트다(L141). '
         '스케일업은 메모리를 나눠 쓰는 가속기들의 범위이지 랙 경계가 아니라는 것이 Austin 의 말이다(L149).'),
        ('6.|Jalapeño는 자사 모델만', '범용과 전용 사이 어디에 앉았나', _jal_spectrum(),
         '범용 GPU 의 논거는 모델 모양이 바뀌어도 하드웨어가 죽지 않는다는 것, 한 모델 전용은 Vik 이 말한 극단 코디자인이다(L83). '
         '구글 TPU 가 중간에 있었고 할라페뇨가 그 중간에 하나 더 앉았다(L73). 자리는 이 회차의 말이고 값은 없다.'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
