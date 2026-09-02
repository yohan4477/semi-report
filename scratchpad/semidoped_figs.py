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
    parts += mid(ty + 60, 44, ['통상은 최소 2~3년, 수작업이 많이 든다'], 'fig-stage')
    return svg(ty + 116, parts,
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


def _jal_cycle():
    """주기 둘. 위는 통상(2~3년), 아래는 할라페뇨(아홉 달). 잘라낸 기능이 다음 판에 붙는 간격이
    곧 욕심의 크기다 — 간격이 길면 무리해서 넣고, 짧으면 덜 넣어도 된다."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '통상 — 다음 세대까지 2~3년')
    r1, _ = band([(['1세대', '잘라낸 기능'], 'fig-box'), ('>', '2~3년 뒤에나 다시'),
                  (['2세대', '그때 다시 넣음'], 'fig-box')], 32, h)
    parts += r1
    parts += head(0, 32 + h + 34, W, '할라페뇨 — 첫 RTL 에서 테이프아웃까지 아홉 달')
    y2 = 32 + h + 44
    r2, _ = band([(['1세대', '잘라낸 기능'], 'fig-box'), ('>', '아홉 달'),
                  (['2세대', '테이프아웃 근접'], 'fig-agent'), ('>', ''),
                  (['3세대', '구상 중'], 'fig-box')], y2, h)
    parts += r2
    parts += mid(y2 + h + 18, 40, ['간격이 짧으면 설계마다 덜 욕심내도 된다'], 'fig-stage')
    return svg(y2 + h + 72, parts,
               '통상은 다음 세대까지 2~3년이라 잘라낸 기능이 그때나 다시 들어가지만, 할라페뇨는 아홉 달 주기라 2세대가 이미 테이프아웃에 다가섰고 3세대를 구상 중이다')


def _jal_yardstick():
    """잣대가 다른 이유 — 사이에 판매자가 있나. 위는 상용 실리콘(설계팀 → 판매 → 랩·하이퍼스케일러 → 사용자),
    아래는 할라페뇨(설계팀 → 사용자). 같은 꼴, 칸 하나 차이."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '상용 실리콘 — 잣대는 TCO')
    r1, _ = band([(['칩 설계팀'], 'fig-box'), ('>', '판다'),
                  (['AI 랩 ·', '하이퍼스케일러'], 'fig-box'), ('>', '서비스'),
                  (['사용자'], 'fig-box')], 32, h)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '할라페뇨 — 잣대는 요청당 에너지 · 마지막 토큰까지 지연')
    r2, _ = band([(['칩 설계팀', '(OpenAI)'], 'fig-agent'), ('>', '중간 판매자 없음'),
                  (['사용자'], 'fig-box')], y2, h)
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
    parts += mid(y + 18, 40, ['비율이 워크로드마다 움직인다 — 고정 배분이 비효율'], 'fig-stage')
    return svg(y + 72, parts,
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

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]   머리에 「|문단 앞머리」를 붙이면 그 문단 앞
FIGS = {
    (JAL, 'strategy'): [
        ('1.', '아홉 달을 만든 세 요인', _jal_nine_months(),
         '셋이 겹쳐 아홉 달이 됐다(L97). 사람과 백지는 전에도 있던 항이고 AI 도구만 새 항이라는 것이 이 절의 논지다. '
         '셋 중 무엇이 몇 할인지는 전사에 없어 상자 크기를 같게 뒀다.'),
        ('1.|설계 셈법도 달라진다', '주기가 짧으면 덜 욕심내도 된다', _jal_cycle(),
         '잘라낸 기능이 다음 판에 붙는 간격이 곧 욕심의 크기다. 통상은 2~3년(L97)이라 무리해서 넣게 되고, '
         '아홉 달이면 2세대가 이미 테이프아웃에 다가섰고 3세대를 구상 중이라(L95) 곧 다시 붙는다.'),
        ('2.', '잣대가 다른 이유 — 사이에 판매자가 있나', _jal_yardstick(),
         '위는 상용 실리콘이다 — 설계팀이 AI 랩·하이퍼스케일러에 팔고 그들이 사용자를 상대하니 잣대가 TCO 다(L45·L47). '
         '아래는 할라페뇨 — 설계팀과 사용자 사이에 판매자가 없어 요청당 에너지와 마지막 토큰까지 지연을 잣대로 삼는다(L43).'),
        ('3.', '투기적 디코딩 — 초안이 똑똑할수록 검증이 가볍다', _jal_specdec(),
         '작은 초안 모델이 토큰을 뱉고 큰 모델이 검증한다. 덜 똑똑하면 여덟 개를 뱉어 검증이 무겁고, 똑똑하면 두 개만 뱉어 가볍다(Vik, L159·L161). '
         '여덟과 둘은 Vik 이 든 수다. 이 비율이 워크로드마다 움직이니 칩을 고정 배분하면 한쪽이 논다.'),
        ('3.|GPU 진영이 이 비대칭을 다룬 방법', '추론을 받는 세 구성', _jal_three_configs(),
         '위가 구성, 아래가 이 회차가 붙인 조건이다. 랙 수(NVL72 1대 + Groq 9대 대 할라페뇨 1~2대)는 Austin 의 어림이고(L109), '
         '700W 는 발표 값(L111), 초당 1,000토큰은 GPT-OSS 기준이다(L105).'),
        ('4.', '가속기마다 HBM 을 나눠 쓰나, 따로 두나', _jal_numa4(),
         '왼쪽이 지금까지의 구조다 — 이웃 가속기들이 HBM 한 덩어리를 나눠 쓰니 연산하려는 순간 데이터가 없다(L129). '
         '오른쪽이 할라페뇨다 — 가속기마다 HBM 을 따로 두고 전용 버스로 붙인다(L131). '
         '가속기 넷은 보기용 수다. 실제 랙은 128칩이고 몇 개가 한 HBM 을 나눠 쓰는지는 전사에 없다.'),
        ('5.', '밸류체인에서 어디에 새 수요가 생기나', _jal_ladder(),
         '모델랩이 실리콘까지 내려와도 밸류체인 아래쪽 전부에 새 수요가 생기는 게 아니다. CPU 는 대체재가 널렸고(L117) 파운드리는 대안이 없어 그대로 간다. '
         '새 수요가 생기는 곳은 메모리와 스케일업 망 둘이다. 시스템 조립은 SemiAnalysis 의 추정이다(L119).'),
        ('5.|망이 가장 구체적이다', '스케일업은 랙 안이 아니다', _jal_domain(),
         '랙 16대가 한 스케일업 도메인이다(L145). 랙 하나 128칩은 Tomahawk 6 로 칩당 초당 600기가비트, 16대 2,048칩은 ESUN 으로 초당 200기가비트다(L141). '
         '스케일업은 메모리를 나눠 쓰는 가속기들의 범위이지 랙 경계가 아니라는 것이 Austin 의 말이다(L149).'),
        ('6.', '범용과 전용 사이 어디에 앉았나', _jal_spectrum(),
         '범용 GPU 의 논거는 모델 모양이 바뀌어도 하드웨어가 죽지 않는다는 것, 한 모델 전용은 Vik 이 말한 극단 코디자인이다(L83). '
         '구글 TPU 가 중간에 있었고 할라페뇨가 그 중간에 하나 더 앉았다(L73). 자리는 이 회차의 말이고 값은 없다.'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
