# -*- coding: utf-8 -*-
"""Semi Doped 판에 끼우는 도해.

받은 글(insights/semidoped/<slug>-<lane>.md)은 문장을 안 고친다. 도해는 그 글의 것이
아니라 우리 것이라 여기 따로 둔다 — 열쇠는 (slug, lane), 값은 `[(절 제목 머리, 제목, svg, 캡션)]`.
절 제목 머리는 받은 글의 `## ` 제목이 그 문자열로 시작하는 절이다(「## 4. (프로세스)」면 '4.').
`gen_semidoped.body_html` 이 그 제목 바로 아래, 본문보다 **앞에** 그림을 세운다.

지킬 것은 `yohan-figure` 스킬 넷 — 원문에 없는 값을 안 그린다(도형 개수도 값이다) ·
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
RAW = os.path.join(ROOT, 'content', 'semi_doped', 'raw')

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
    raw = io.open(path, encoding='utf-8').read()
    # 전사는 수를 말로 적는다(forty-eight volts) — 영어 수사를 숫자로 풀어 붙여 두고 대조한다(2026-09-03)
    words = _number_words(raw)
    # 달러 억 단위 — 「$190 billion」은 글에서 「1,900억」이다. billion 은 ×10, trillion 은 ×10000 을 억으로 더한다
    eok = []
    for num, unit in re.findall(r'(\d+(?:\.\d+)?)\s*(billion|trillion)', raw, re.I):
        eok.append(str(int(round(float(num) * (10 if unit.lower() == 'billion' else 10000)))))
    for w in words:
        n = int(w)
        if n >= 10 ** 8 and n % 10 ** 8 == 0:
            eok.append(str(n // 10 ** 8))
    src = re.sub(r'[\s,]', '', raw) + '|' + '|'.join(words + eok)
    return sorted(n for n in values(svg_) if n.replace(',', '') not in src)


_ONES = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split())}
_TENS = {w: i * 10 for i, w in enumerate('_ _ twenty thirty forty fifty sixty seventy eighty ninety'.split()) if w != '_'}
_MULT = {'hundred': 100, 'thousand': 1000, 'million': 10 ** 6, 'billion': 10 ** 9}


def _number_words(text):
    """영어 수사 연쇄를 숫자로. 「forty-eight」→48, 「eight hundred」→800, 「two point five」는 안 다룬다."""
    toks = re.findall(r"[A-Za-z]+|-|[^A-Za-z\s-]", text.lower())  # 구두점은 끊는 표시
    out, cur, total = [], 0, 0
    def flush():
        nonlocal cur, total
        if cur or total:
            out.append(str(total + cur))
        cur = total = 0
    for t in toks:
        if t in _ONES:
            cur += _ONES[t]
        elif t in _TENS:
            cur += _TENS[t]
        elif t in _MULT:
            if t == 'hundred':
                cur = (cur or 1) * 100
            else:
                total += (cur or 1) * _MULT[t]; cur = 0
        elif t == '-' or t == 'and':
            continue
        else:
            flush()
    flush()
    return out


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


def _cds_pricing():
    """설비투자 값을 누가 매기나 — 돈의 출처가 바뀌자 심사하는 쪽과 주기가 바뀐다."""
    w = w_of(['영업으로 번 현금'])
    r1, _ = eband([(['영업으로 번 현금'], 'fig-box'), ('>', ''),
                   (['이사회', '분기에 한 번'], 'fig-box'), ('>', ''),
                   (['설비투자'], 'fig-stage')], 40, 2 * LH + 22, w=w, min_gap=14)
    y2 = 40 + 2 * LH + 22 + 46
    r2, _ = eband([(['부채 · 특수법인'], 'fig-box'), ('>', ''),
                   (['채권 투자자', 'CDS 스프레드'], 'fig-agent'), ('>', ''),
                   (['설비투자'], 'fig-stage')], y2, 2 * LH + 22, w=w, min_gap=14)
    y = y2 + 2 * LH + 22
    parts = (head(0, 30, 300, '여태 — 이사회가 승인') + r1
             + head(0, y2 - 10, 300, '지금 — 채권시장이 값매김') + r2
             + legend([('fig-agent', '값을 매기는 자리')], y + 16))
    return svg(y + 42, parts,
               '여태는 영업으로 번 현금으로 사서 이사회가 분기에 한 번 심사했고, 지금은 부채와 특수법인으로 사서 채권 투자자가 CDS 스프레드로 매일 값을 매긴다')


def _cds_expect():
    """좋은 숫자가 나쁜 사건이 되는 경로 — 실적에서 주가까지."""
    steps = [(['매출 257% · 영업이익 6배 넘게', '영업이익률 76%'], 'fig-box'),
             (['그런데 시장 기대에 못 미쳤다'], 'fig-bad'),
             (['레버리지 · 한 나라 한 종목 쏠림'], 'fig-bad'),
             (['하루 20% 하락'], 'fig-agent')]
    parts, y = [], 34.0
    for k, (lines, cls) in enumerate(steps):
        h = len(lines) * LH + 22
        if k:
            parts += down(W / 2, y - 20, y - 2)
        parts += mid(y, h, lines, cls)
        y += h + 20
    return svg(y + 6, parts,
               '매출 257% 증가와 영업이익률 76% 라는 숫자가 시장 기대에 못 미치자, 레버리지와 한 나라 한 종목 쏠림이 겹쳐 하루 20% 하락으로 이어졌다')


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


def _pj_order():
    """무엇이 무엇을 묶나 — 흔한 읽기와 이 회차의 읽기. 같은 항을 순서만 뒤집어 그린다."""
    w = w_of(['랙 안에 GPU 를 더 채운다'])
    h = LH + 22
    parts = head(0, 24, W, '흔히 읽는 순서')
    a, _ = band([(['랙이 뜨겁다'], 'fig-box'), ('>', '그래서'),
                 (['GPU 를 못 늘린다'], 'fig-box')], 34, h)
    parts += a
    y = 34 + h + 44
    parts += head(0, y - 10, W, '이 회차가 말하는 순서')
    steps = [(['구리 도달거리가 3~4미터'], 'fig-agent'), (['랙 밖으로 정보를 못 뺀다'], 'fig-box'),
             (['랙 안에 GPU 를 더 채운다'], 'fig-box'), (['랙이 더 뜨거워진다'], 'fig-box')]
    for k, (lines, cls) in enumerate(steps):
        parts += box((W - w) / 2, y, w, h, lines, cls)
        y += h
        if k < len(steps) - 1:
            parts += down(W / 2, y, y + 18)
            y += 20
    parts += legend([('fig-agent', '출발점')], y + 14)
    return svg(y + 40, parts,
               '흔히는 랙이 뜨거워서 GPU 를 못 늘린다고 읽는데, 이 회차는 구리 도달거리가 3~4미터로 줄어 랙 밖으로 정보를 못 빼니 랙 안에 GPU 를 더 채우게 되고 그래서 더 뜨거워진다고 본다')


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


def _al_beads():
    """실에 꿴 구슬 — 보낸 줄과 받은 줄. 받은 줄에서 흐려지고 붙고 어긋난 자리가 보인다.
    구슬 여섯은 보기용 수다. 전사에는 몇 개인지 없다."""
    y1, y2 = 74.0, 150.0
    x0, x1 = 40.0, 480.0
    xs = [70.0, 152.0, 234.0, 316.0, 398.0]
    parts = head(0, 34, W, '보낸 줄')
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x0, y1, x1, y1)]
    for x in xs:
        parts += ['  <circle cx="%g" cy="%g" r="11" class="fig-box"/>' % (x, y1)]
    parts += head(0, 122, W, '받은 줄')
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x0, y2, x1, y2)]
    parts += ['  <circle cx="%g" cy="%g" r="10" class="fig-box"/>' % (xs[0], y2)]
    parts += ['  <circle cx="%g" cy="%g" r="8" class="fig-stage"/>' % (xs[1], y2)]
    parts += ['  <ellipse cx="%g" cy="%g" rx="47" ry="8" class="fig-stage"/>' % ((xs[2] + xs[3]) / 2, y2)]
    parts += ['  <circle cx="%g" cy="%g" r="6" class="fig-stage"/>' % (xs[4] + 22, y2)]
    for cx, mark in ((xs[1], '①'), ((xs[2] + xs[3]) / 2, '④'), (xs[4] + 22, '⑤')):
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
                  % (cx, y2 + 30, mark)]
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" '
              'style="stroke-dasharray:4 3" marker-end="none"/>' % (xs[4], y2 - 26, xs[4], y2 + 26)]
    # ② 반사 — 배선 끝에서 되돌아온다
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" '
              'marker-end="url(#aieArw)"/>' % (x1 - 4, y2 - 28, x1 - 56, y2 - 28)]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">②</text>' % (x1 - 30, y2 - 36)]
    # ③ 크로스토크 — 옆 배선에서 끼어든다
    y3 = y2 + 54
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" '
              'style="stroke-dasharray:4 3"/>' % (x0, y3, x1, y3)]
    parts += ['  <text x="%g" y="%g" class="fig-e">옆 배선</text>' % (x0, y3 + 22)]
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" '
              'marker-end="url(#aieArw)"/>' % (110, y3 - 6, 110, y2 + 12)]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">③</text>' % (128, y3 - 8)]
    y = y3 + 40
    items = [(['① 감쇠'], 'fig-box'), (['② 반사'], 'fig-box'),
             (['③ 크로스토크'], 'fig-box')]
    w1 = sum(w_of(l) for l, _ in items) + 2 * 12
    row, _x, cs, hh = panel_boxes((W - w1) / 2, y, items, gap=12, h=LH + 26)
    parts += row
    items2 = [(['④ 심볼 간 간섭'], 'fig-box'), (['⑤ 지터'], 'fig-box')]
    w2 = sum(w_of(l) for l, _ in items2) + 12
    row2, _x2, cs2, hh2 = panel_boxes((W - w2) / 2, y + hh + 10, items2, gap=12, h=LH + 26)
    parts += row2
    y4 = y + hh + 10 + hh2
    return svg(y4 + 16, parts,
               '보낸 줄에서는 같은 크기의 구슬이 고른 간격으로 놓이는데 받은 줄에서는 흐려지고 둘이 붙고 하나는 읽는 시각에서 어긋나 있다')


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


# ══ 컴퓨텍스 2026 (2026-06-12) 전략 판 ═══════════════════════════════════
# 값은 전사의 것만 — 99%, OSFP 8개, 800·48·12·6볼트, 칩렛 2·3·12(=17). 배치 시간 「절반」은 담당자 말이라 캡션에.

def _cx_cpo_blocks():
    """CPO 가 랙 안으로 못 들어오는 이유 둘 — 같은 꼴 두 기둥. 위는 지금 있는 것, 아래 점선은 아직 없는 것."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '① 수율') + head(R, 22, pw, '② 검사')
    cols = [(L, ['엔지니어링 샘플', '99%'], ['수백만 개 양산', '아직 모름']),
            (R, ['웨이퍼 위·아래', '동시 정렬'], ['빠른 검사 장비', '아직 없음'])]
    w = max(w_of(a) + 0 for _, a, b in cols for a in (a, b))
    h = 2 * LH + 22
    for x0, top, bot in cols:
        x = x0 + (pw - w) / 2
        parts += box(x, 36, w, h, top, 'fig-box')
        parts += down(x + w / 2, 36 + h, 36 + h + 20)
        parts += box(x, 36 + h + 22, w, h, bot, 'fig-outside')
    y = 36 + 2 * h + 22
    parts += legend([('fig-box', '지금 있는 것'), ('fig-outside', '아직 없는 것')], y + 16)
    return svg(y + 42, parts, '수율은 엔지니어링 샘플 99% 까지만 확인됐고 양산은 아직 모른다. 검사는 웨이퍼 위아래를 동시에 맞춰야 하는데 빠른 장비가 아직 없다')


def _cx_optics_ways():
    """빛으로 가는 길 넷 — 광 엔진이 칩에서 얼마나 가까운가. 같은 폭 상자 넷, 화살표는 가까워지는 방향."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '광 엔진이 칩에 가까워지는 순서')
    row, _x = eband([(['플러그형', 'OSFP'], 'fig-box'), ('>', ''),
                     (['XPO', 'OSFP×8'], 'fig-box'), ('>', ''),
                     (['NPO', '소켓'], 'fig-box'), ('>', ''),
                     (['CPO', '패키지 위'], 'fig-agent')], 36, h)
    parts += row + legend([('fig-agent', '이 회차의 물음 — 랙 안까지 들어오나')], 36 + h + 16)
    return svg(36 + h + 42, parts, '플러그형에서 OSFP 여덟을 합친 XPO, 소켓에 꽂는 NPO, 패키지 위에 붙이는 CPO 순으로 광 엔진이 칩에 가까워진다')


def _cx_voltage():
    """전압 구간마다 소재가 정해져 있다 — 배전망 → 800볼트 → 48볼트 → 12·6볼트. 실리콘카바이드 구간만 짙게."""
    h = 3 * LH + 22
    row, _x = eband([(['배전망', '중전압'], 'fig-box'), ('>', ''),
                     (['800볼트', '실리콘', '카바이드'], 'fig-agent'), ('>', ''),
                     (['48볼트', '실리콘', '카바이드'], 'fig-agent'), ('>', ''),
                     (['12·6볼트', '실리콘'], 'fig-box')], 30, h)
    parts = row + legend([('fig-agent', '실리콘카바이드'), ('fig-box', '실리콘')], 30 + h + 16)
    return svg(30 + h + 42, parts, '중전압 배전망에서 800볼트로, 다시 48볼트로 내리는 구간은 실리콘카바이드이고 그 아래 12·6볼트로 가는 변환은 실리콘이다')


def _cx_chiplets():
    """클리어워터포레스트 칩렛 열일곱 — 아래 줄 I/O 둘·베이스 셋, 그 위에 컴퓨트 열둘. 칸 수가 값이다."""
    cw, ch, g = 78.0, 2 * LH + 22, 10.0  # 두 줄 글에 맞춘 높이 — 44 면 둘째 줄이 아래 테두리에 깔린다
    labels = [('I/O', '인텔7', 'fig-box'), ('베이스', '인텔3', 'fig-agent'), ('베이스', '인텔3', 'fig-agent'),
              ('베이스', '인텔3', 'fig-agent'), ('I/O', '인텔7', 'fig-box')]
    total = 5 * cw + 4 * g
    x0 = (W - total) / 2
    parts = head(0, 22, W, '컴퓨트 다이 열둘 (인텔18A) — 베이스 위에 쌓음')
    ty, th, tg = 36, 22, 4
    # 컴퓨트 열둘 — 베이스 셋 위에 넷씩
    for k in range(1, 4):
        bx = x0 + k * (cw + g)
        tw = (cw - 3 * tg) / 4
        for j in range(4):
            parts += _rect(bx + j * (tw + tg), ty, tw, th, 'fig-box')
    by = ty + th + 14
    for k, (n, proc, cls) in enumerate(labels):
        parts += box(x0 + k * (cw + g), by, cw, ch, [n, proc], cls)
    parts += head(0, by + ch + 24, W, 'I/O 둘 (인텔7) · 액티브 베이스 셋 (인텔3)')
    return svg(by + ch + 36, parts, '칩렛 열일곱 — 인텔7 I/O 다이 둘, 인텔3 액티브 베이스 다이 셋, 그 위에 인텔18A 컴퓨트 다이 열둘')


def _cx_prefab():
    """조립식 인프라 블록 — 전에는 현장에서 설비를 짓고 랙을 넣었고, 후에는 갖춘 컨테이너에 랙만 밀어 넣는다. 같은 폭."""
    h = 2 * LH + 22
    bw = w_of(['냉각·전원 설비', '현장에서 짓기'])
    parts = head(0, 22, W, '전 — 현장 시공')
    r1, _ = eband([(['냉각·전원 설비', '현장에서 짓기'], 'fig-box'), ('>', ''),
                   (['설비와 랙', '잇기'], 'fig-box'), ('>', ''),
                   (['랙 넣기'], 'fig-box')], 32, h, w=bw)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '후 — 조립식 블록')
    r2, _ = eband([(['갖춘 컨테이너', '들여오기'], 'fig-agent'), ('>', ''),
                   (['랙 밀어 넣기', '연결'], 'fig-box')], y2, h, w=bw)
    parts += r2
    return svg(y2 + h + 16, parts, '전에는 냉각·전원 설비를 현장에서 짓고 랙을 넣었다. 조립식 블록은 설비를 갖춘 컨테이너에 랙만 밀어 넣는다')


def _cx_marvell():
    """마벨의 세 사업 — 거리만 다르고 하는 일은 하나다."""
    items = [(['칩 안', 'ASIC'], 'fig-box'), (['칩 사이', '인터커넥트'], 'fig-agent'),
             (['데이터센터 사이', 'DSP'], 'fig-box')]
    h = 2 * LH + 22
    ws = [w_of(l) for l, _ in items]
    gap = 24.0
    x = (W - (sum(ws) + gap * 2)) / 2
    parts, centers = [], []
    for (lines, cls), w in zip(items, ws):
        parts += box(x, 36, w, h, lines, cls)
        centers.append(x + w / 2)
        x += w + gap
    y = 36 + h
    parts += mid(y + 34, LH + 22, ['셋 다 데이터를 옮기는 일이다'], 'fig-stage')
    for cx in centers:
        parts += down(cx, y + 2, y + 32)
    parts += legend([('fig-agent', '이번에 무게를 실은 자리')], y + 34 + LH + 22 + 16)
    return svg(y + 34 + LH + 22 + 52, parts,
               '마벨은 칩 안에서 ASIC, 칩 사이에서 인터커넥트, 데이터센터 사이에서 DSP 를 판다. 거리만 다르고 셋 다 데이터를 옮기는 일이며, 이번 키노트는 인터커넥트에 무게를 실었다')


CX = '2026-06-12-computex-optics-power'


# ══ 전력 벽 (2026-05-08) 전략 판 ═════════════════════════════════════════
# 값은 전사의 것만 — 600킬로와트, 48볼트·12,500암페어, 800볼트·750암페어, 수백 kV·10~30kV·400~430V·48V·12V·1V.

def _pw_current():
    """같은 600킬로와트를 48볼트로 보낼 때와 800볼트로 보낼 때 — 같은 꼴 둘, 다른 것은 전류."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '48볼트로 보내면') + head(R, 22, pw, '800볼트로 보내면')
    h = 2 * LH + 22
    w = w_of(['12,500암페어'])
    for x0, volt, amp, cls in [(L, '48볼트', '12,500암페어', 'fig-outside'), (R, '800볼트', '750암페어', 'fig-agent')]:
        x = x0 + (pw - w) / 2
        parts += box(x, 36, w, h, ['600킬로와트', volt], 'fig-box')
        parts += down(x + w / 2, 36 + h, 36 + h + 20)
        parts += box(x, 36 + h + 22, w, h, ['흐르는 전류', amp], cls)
    y = 36 + 2 * h + 22
    parts += legend([('fig-agent', '가는 길'), ('fig-outside', '안 되는 길')], y + 16)
    return svg(y + 42, parts, '같은 600킬로와트를 48볼트로 보내면 12,500암페어가 흐르고 800볼트로 보내면 750암페어가 흐른다')


def _pw_chain():
    """발전소에서 GPU 까지 — 전압이 바뀌는 자리. 위에서 아래로, 마지막 칸이 가장 많다."""
    return _chain_down([(['발전소 — 수백 킬로볼트'], 'fig-box'),
                        (['변전소 — 10~30킬로볼트'], 'fig-box'),
                        (['유틸리티룸 — 400~430볼트 삼상'], 'fig-box'),
                        (['랙 전원장치 — 48볼트 직류'], 'fig-box'),
                        (['중간 버스 컨버터 — 12볼트'], 'fig-box'),
                        (['VRM — 1볼트 안팎, 개수가 가장 많다'], 'fig-agent')],
                       '발전소에서 GPU 까지 전압이 여섯 번 바뀌고, 자리마다 다른 회사가 선다. 마지막 VRM 이 가장 많다')


def _pw_fork():
    """800볼트 다음 — 48볼트를 거쳐 내려갈지 6볼트로 바로 갈지. 같은 폭 상자, 같은 출발."""
    h = 2 * LH + 22
    bw = w_of(['800볼트'])
    parts = head(0, 22, W, '① 있던 48볼트 설비를 그대로 쓴다')
    r1, _ = eband([(['800볼트'], 'fig-box'), ('>', ''), (['48볼트'], 'fig-agent'), ('>', ''),
                   (['12볼트'], 'fig-box'), ('>', ''), (['1볼트'], 'fig-box')], 32, h, w=bw)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '② 6볼트로 바로 간다 — TI · Navitas')
    r2, _ = eband([(['800볼트'], 'fig-box'), ('>', ''), (['6볼트'], 'fig-agent')], y2, h, w=bw)
    parts += r2
    parts += legend([('fig-agent', '갈래가 갈리는 자리')], y2 + h + 16)
    return svg(y2 + h + 42, parts, '800볼트 다음은 두 갈래다. 있던 48볼트 설비를 거쳐 12볼트·1볼트로 내려가거나, 6볼트로 바로 간다')


def _pw_racks():
    """랙 하나가 먹는 전력 — 막대 높이가 킬로와트다. AI 이전 10~15킬로와트는 캡션에만 적는다."""
    bars = [(20, '20', '클라우드 시대', 'fig-box'), (120, '100~120', '지금', 'fig-box'),
            (600, '600', '카이버 세대', 'fig-agent'), (1000, '1메가와트', '다음 세대', 'fig-agent')]
    base, scale, bw, gap = 196.0, 0.17, 110.0, 20.0
    x0 = (W - (len(bars) * bw + (len(bars) - 1) * gap)) / 2
    parts = []
    for i, (v, lab, name, cls) in enumerate(bars):
        x = x0 + i * (bw + gap)
        hh = v * scale
        parts += _rect(x, base - hh, bw, hh, cls)
        parts += head(x, base - hh - 8, bw, lab)
        parts += head(x, base + 20, bw, name)
    parts += hline(10, W - 10, base)
    return svg(base + 40, parts,
               '랙 하나가 먹는 전력이 클라우드 시대 20킬로와트에서 지금 100~120킬로와트, 카이버 세대 600킬로와트, 다음 세대 1메가와트로 올라간다')


def _pw_vertical():
    """전압을 어디서 낮추나 — 멀리서 낮추는 길과 칩 가까이서 낮추는 길."""
    lw, rw, gapx = 150.0, 240.0, 44.0
    x0 = (W - (lw + gapx + rw)) / 2
    h = LH + 22
    left = [(['800볼트'], 'fig-box'), (['멀리서 48볼트로'], 'fig-outside'),
            (['긴 구리 트레이스'], 'fig-outside'), (['GPU'], 'fig-box')]
    right = [(['800볼트'], 'fig-box'), (['GPU 바로 아래에서 낮춘다'], 'fig-agent'), (['GPU'], 'fig-box')]
    parts = head(x0, 24, lw, '멀리서 낮추면') + head(x0 + lw + gapx, 24, rw, '칩 가까이서 낮추면')
    ys = []
    for x, w, col in [(x0, lw, left), (x0 + lw + gapx, rw, right)]:
        y = 36.0
        for k, (lines, cls) in enumerate(col):
            if k:
                parts += down(x + w / 2, y - 20, y - 2)
            parts += box(x, y, w, h, lines, cls)
            y += h + 20
        ys.append(y - 20)
    y = max(ys)
    parts += legend([('fig-agent', '가는 길'), ('fig-outside', '안 되는 길')], y + 14)
    return svg(y + 40, parts,
               '전압을 멀리서 낮추면 낮은 전압이 긴 구리를 지나며 손실이 붙고, 칩 가까이서 낮추면 고전압이 GPU 바로 아래까지 간다')


PW = '2026-05-08-power-wall'


# ══ 메모리세 (2026-05-04) 전략 판 ═══════════════════════════════════════
# 값은 전사의 것만 — 1,900억·250억, 40%·13~20%, 핀당 8·10·11·12기가비트, 51.1·78.4·80·75%.

def _mt_capex():
    """마이크로소프트 2026년 설비투자 1,900억 달러 중 부품값 상승분 250억 — 한 막대 안의 조각. 길이가 값이다."""
    bw = 440.0; x0 = (W - bw) / 2; y, h = 40, 34
    part = bw * 250 / 1900
    parts = head(0, 22, W, '2026년 설비투자 1,900억 달러')
    parts += _rect(x0, y, bw, h, 'fig-box')
    parts += _rect(x0, y, part, h, 'fig-agent')
    parts += ['  <text x="%g" y="%g" class="fig-e">부품값 상승분 250억</text>' % (x0 + part + 10, y + h / 2 + 6)]
    parts += down(x0 + part / 2, y + h + 4, y + h + 26)
    parts += head(0, y + h + 46, W, '← 250억 — 몇 년 전 한 분기 설비투자 전체')
    return svg(y + h + 60, parts, '마이크로소프트의 2026년 설비투자 1,900억 달러 중 250억 달러가 부품값 상승분이다. 몇 년 전에는 한 분기 설비투자 전체가 250억 달러였다')


def _mt_loop():
    """돈이 연산으로 가면 고리가 닫히고, 메모리 회사로 가면 안 닫힌다 — 같은 폭 두 줄. 끝 칸이 다르다."""
    h = 2 * LH + 22
    bw = w_of(['더 나은 도구', '매출로 돌아옴'])
    parts = head(0, 22, W, '설비투자가 연산으로 가면')
    r1, _ = eband([(['설비투자'], 'fig-box'), ('>', ''), (['가속기'], 'fig-box'), ('>', ''),
                   (['더 나은 도구'], 'fig-box'), ('>', ''), (['매출로 돌아옴'], 'fig-agent')], 32, h, w=bw)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '설비투자가 메모리 회사로 가면')
    r2, _ = eband([(['설비투자'], 'fig-box'), ('>', ''), (['메모리 회사'], 'fig-box'), ('>', ''),
                   (['돌아오는 것', '없음'], 'fig-outside')], y2, h, w=bw)
    parts += r2
    parts += legend([('fig-agent', '고리가 닫힌다'), ('fig-outside', '고리가 안 닫힌다')], y2 + h + 16)
    return svg(y2 + h + 42, parts, '설비투자가 가속기로 가면 도구가 좋아지고 매출로 돌아와 고리가 닫힌다. 메모리 회사로 가면 돌아오는 것이 없다')


def _mt_share():
    """삼성 HBM 점유율 — 여섯 분기 전 40% 에서 2025년 13~20% 로. 같은 폭 두 막대, 높이가 값."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '여섯 분기쯤 전') + head(R, 22, pw, '2025년')
    base, scale, bw = 150.0, 2.4, 90.0
    for x0, v, lab, cls in [(L, 40, '40%', 'fig-box'), (R, 20, '13~20%', 'fig-agent')]:
        hh = v * scale
        parts += _rect(x0 + (pw - bw) / 2, base - hh, bw, hh, cls)
        parts += head(x0, base - hh - 8, pw, lab)
    parts += hline(20, W - 20, base)
    return svg(base + 14, parts, '삼성의 HBM 점유율은 여섯 분기쯤 전 40% 수준에서 2025년 13~20% 대로 떨어졌다. 막대 높이가 값이고 2025년은 위쪽 값으로 그렸다')


def _mt_pin():
    """HBM4 핀당 속도 — JEDEC 규격 8기가비트와 공급사가 밀어 올린 10·11·12. 같은 폭 상자, 가로로."""
    h = 2 * LH + 22
    parts = head(0, 22, W, '핀 하나당 초당 기가비트')
    row, _x = eband([(['8', '규격'], 'fig-outside'), ('>', ''), (['10'], 'fig-box'), ('>', ''),
                     (['11'], 'fig-box'), ('>', ''), (['12', '공급사'], 'fig-agent')], 36, h)
    parts += row + legend([('fig-outside', 'JEDEC 규격'), ('fig-agent', '공급사가 밀어 올린 곳')], 36 + h + 16)
    return svg(36 + h + 42, parts, 'HBM4 의 JEDEC 규격은 핀당 초당 8기가비트인데 공급사들은 10·11·12까지 밀어 올리고 있다')


def _mt_margin():
    """샌디스크 매출총이익률 — 앞 분기 51.1% → 이번 분기 78.4% → 가이던스 80% 위. 견줌 엔비디아 75% 안팎."""
    cols = [('앞 분기', 51.1, '51.1%', 'fig-box'), ('이번 분기', 78.4, '78.4%', 'fig-agent'),
            ('가이던스', 80, '80% 위', 'fig-outside'), ('엔비디아', 75, '75% 안팎', 'fig-box')]
    n = len(cols); cw = W / n; bw = 70.0; base, scale = 160.0, 1.4
    parts = []
    for k, (lab, v, txt, cls) in enumerate(cols):
        x0 = k * cw; hh = v * scale
        parts += _rect(x0 + (cw - bw) / 2, base - hh, bw, hh, cls)
        parts += head(x0, base - hh - 8, cw, txt)
        parts += head(x0, base + 20, cw, lab)
    parts += hline(10, W - 10, base)
    return svg(base + 34, parts, '샌디스크 매출총이익률은 앞 분기 51.1% 에서 이번 분기 78.4% 로 뛰었고 다음 분기 가이던스는 80% 위다. 엔비디아가 75% 안팎이다')


def _mt_cycle():
    return _chain_down([(['하이퍼스케일러가 부품값 인상분을 설비투자에 얹어', '메모리·저장장치 회사로 넘긴다'], 'fig-box'),
                        (['부족 때문에 기업 고객이 온프레미스를 포기하고', '클라우드로 들어와 하이퍼스케일러 매출이 는다'], 'fig-box'),
                        (['자체 가속기로 아낀 돈을 다시 메모리 값에 쓴다'], 'fig-agent'),
                        (['처음으로 돌아간다'], 'fig-outside')],
                       '세 흐름을 이으면 설비투자가 도는 고리다. 부품값이 메모리 회사로, 부족이 기업을 클라우드로, 자체 가속기 절감이 다시 메모리 값으로')


MT = '2026-05-04-memory-tax'


# ══ WEKA (2026-07-10) 전략 판 ═══════════════════════════════════════════
# 값은 전사의 것만 — 레인 128·32, KV 캐시 50GB·5GB, 컨텍스트 10배·세션 10~100배·순 100배, G1~G4, 95%, 300~500TB.

def _wk_lanes():
    """NVLink 128레인 대 PCI 32레인 — 같은 꼴 두 줄, 가운데 통로 굵기가 레인 수다."""
    fw, h = 400.0, 44
    fx = (W - fw) / 2
    lw, rw = w_of(['GPU']), w_of(['스토리지'])
    parts, y = [], 22
    for label, left, right, lanes, cls in [('NVLink — 레인 128개쯤', 'GPU', '스토리지', 128, 'fig-agent'),
                                           ('마더보드 PCI — 레인 32개', 'CPU', 'DRAM', 32, 'fig-box')]:
        parts += head(fx, y, fw, label)
        fy = y + 10
        parts += _rect(fx, fy, fw, h + 32, 'fig-stage')
        px, py = fx + 16, fy + 16
        parts += box(px, py, lw, h, [left], 'fig-box')
        rx = fx + fw - 16 - rw
        parts += box(rx, py, rw, h, [right], 'fig-box')
        th = 6 + lanes * 0.2
        parts += _rect(px + lw + 8, py + h / 2 - th / 2, rx - (px + lw + 8) - 8, th, cls)
        y = fy + h + 32 + 26
    parts += legend([('fig-agent', '통로 굵기 = 레인 수')], y - 10)
    return svg(y + 16, parts, 'NVLink 쪽은 레인이 128개쯤이고 마더보드에서 CPU 가 DRAM 으로 가는 PCI 는 32개다. 통로 굵기가 레인 수다')


def _wk_kv():
    return _chain_down([(['10만 토큰의 KV 캐시 — 50기가바이트'], 'fig-box'),
                        (['DeepSeek V4 식 최적화 — 5기가바이트'], 'fig-agent'),
                        (['컨텍스트 10배 · 동시 세션 10~100배'], 'fig-box'),
                        (['총량은 순 100배'], 'fig-outside')],
                       '단위 소비는 50GB 에서 5GB 로 줄었는데 컨텍스트와 동시 세션이 곱해져 총량은 100배가 된다')


def _wk_tiers():
    """Nvidia Dynamo 의 메모리 네 층 — 위가 빠르다. 층 사이는 자릿수로 벌어진다."""
    rows = [('G1', 'HBM — GPU 안', 'fig-agent'), ('G2', 'DRAM — CPU 쪽', 'fig-box'),
            ('G3', '로컬 스토리지 — 서버 안', 'fig-box'), ('G4', '원격 스토리지 — NFS · S3', 'fig-outside')]
    lw = w_of([r[0] for r in rows]); rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 30, 44
    for name, note, cls in rows:
        parts += box(x0, y, lw, h, [name], cls)
        parts += box(x0 + lw + gap, y, rw, h, [note], 'fig-stage')
        y += h + 10
    return svg(y + 2, parts, 'Nvidia Dynamo 팀이 정리한 네 층 — HBM, CPU 쪽 DRAM, 서버 안 로컬 스토리지, NFS 나 S3 같은 원격 스토리지')


def _wk_hit():
    """캐시 적중률 둘 — 대시보드의 논리 적중률과 사업자가 실제로 맞히는 비율. 같은 꼴 좌우."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '① 논리 적중률') + head(R, 22, pw, '② 실제 적중률')
    h = 2 * LH + 22
    cols = [(L, ['에이전트 대시보드', '보통 95% 근처'], ['재사용될 수 있는', '비율'], 'fig-box'),
            (R, ['사업자가 맞히는 비율', '메모리 계층에 달림'], ['HBM·DRAM 은', '정해진 양뿐'], 'fig-agent')]
    w = w_of(*[l for _, a, b, _c in cols for l in (a, b)])  # 모든 줄 중 가장 긴 것에 맞춘다
    for x0, top, bot, cls in cols:
        x = x0 + (pw - w) / 2
        parts += box(x, 36, w, h, top, cls)
        parts += down(x + w / 2, 36 + h, 36 + h + 20)
        parts += box(x, 36 + h + 22, w, h, bot, 'fig-stage')
    y = 36 + 2 * h + 22
    return svg(y + 14, parts, '대시보드에 뜨는 논리 적중률은 95% 근처로 높지만, 사업자가 실제로 맞히는 비율은 가진 메모리 계층에 달렸다')


def _wk_provision():
    """1페타바이트를 사서 300~500테라바이트만 쓴다 — 한 막대 안의 조각."""
    bw = 440.0; x0 = (W - bw) / 2; y, h = 40, 34
    parts = head(0, 22, W, '산 용량 — 1페타바이트')
    parts += _rect(x0, y, bw, h, 'fig-outside')
    parts += _rect(x0, y, bw * 0.5, h, 'fig-agent')
    parts += head(0, y + h + 22, W, '짙은 조각 — 실제로 쓰는 300~500테라바이트')
    parts += legend([('fig-agent', '쓰는 용량'), ('fig-outside', '여유분으로 남기는 용량')], y + h + 40)
    return svg(y + h + 66, parts, 'SLC 없이 TLC 나 QLC 로 버티려면 1페타바이트를 사서 실제로는 300~500테라바이트만 쓴다. 짙은 조각은 위쪽 값으로 그렸다')


def _wk_cost():
    """소프트웨어 원가가 무엇으로 바뀌나 — 나눠 태울 수 있던 것과 없는 것."""
    h = LH + 22
    parts = head(0, 24, 300, '예전 — 나눠 태운다')
    a, _ = band([(['클라우드 인스턴스 · VM'], 'fig-box'), ('>', '나눠 쓴다'),
                 (['한계비용이 사라진다'], 'fig-box')], 34, h)
    parts += a
    y = 34 + h + 56
    parts += head(0, y - 18, 300, '지금 — 못 나눈다')
    b, _ = band([(['토큰'], 'fig-agent'), ('>', '사용자마다 따로'),
                 (['한계비용이 남는다'], 'fig-bad')], y, h)
    parts += b
    y2 = y + h + 52
    parts += head(0, y2 - 16, 300, '출구는 둘')
    items = [(['추론 사업자에 맡긴다'], 'fig-box'), (['뉴클라우드 · 토큰 공장과 합친다'], 'fig-box')]
    ws = [w_of(l) for l, _ in items]
    gap = 20.0
    x = (W - (sum(ws) + gap)) / 2
    for (lines, cls), w in zip(items, ws):
        parts += box(x, y2, w, h, lines, cls)
        x += w + gap
    return svg(y2 + h + 16, parts,
               '클라우드 인스턴스와 가상머신은 사용자 여럿에 나눠 태울 수 있어 한계비용이 사라졌는데 토큰은 그렇게 안 된다. 출구는 추론 사업자에 계속 맡기거나 뉴클라우드·토큰 공장과 합치는 둘이다')


WK = '2026-07-10-weka-bercovici'


# ══ 첨단 패키징 (2026-06-19) 전략 판 ═══════════════════════════════════
# 값은 전사의 것만 — 858제곱밀리미터(26×33), 3.3·5.5·9.5·40배, 8·12배, 2028, 120×180, 300, 500.

def _ap_stack(x0, pw, label, mid_lines, mid_cls, top='칩', bottom='기판'):
    """칩 / 가운데 층 / 기판 세 층 한 벌. 같은 꼴을 여러 벌 세우기 위한 부품."""
    w = pw - 24
    x = x0 + 12
    out = head(x0, 22, pw, label)
    y = 34
    out += box(x, y, w, 40, [top], 'fig-box'); y += 40 + 6
    h = len(mid_lines) * LH + 22
    out += box(x, y, w, h, mid_lines, mid_cls); y += h + 6
    out += box(x, y, w, 40, [bottom], 'fig-stage'); y += 40
    return out, y


def _ap_cowos():
    """TSMC CoWoS 세 갈래 — 같은 세 층, 가운데 층만 다르다."""
    pw = W / 3
    parts, y = [], 0
    for k, (label, mid, cls) in enumerate([('CoWoS-S', ['실리콘 인터포저', 'TSV 로 관통'], 'fig-agent'),
                                           ('CoWoS-R', ['유기 RDL', '금속 두세 층'], 'fig-box'),
                                           ('CoWoS-L', ['유기 층 안에', '실리콘 브리지'], 'fig-box')]):
        out, y = _ap_stack(k * pw, pw, label, mid, cls)
        parts += out
    parts += legend([('fig-agent', '실리콘을 다 깐다'), ('fig-box', '싸게 깔거나 필요한 데만')], y + 14)
    return svg(y + 40, parts, 'CoWoS 세 갈래는 칩과 기판 사이 가운데 층만 다르다 — S 는 실리콘 인터포저, R 은 유기 RDL, L 은 유기 층 안에 실리콘 브리지')


def _ap_emib():
    """CoWoS-L 세 층과 EMIB 두 층 — 같은 꼴 좌우, 인텔은 가운데 층을 뺐다."""
    pw = W / 2
    parts = []
    out, y1 = _ap_stack(0, pw, 'CoWoS-L — 세 층', ['유기 층 안 브리지'], 'fig-box')
    parts += out
    x = pw + 12; w = pw - 24
    parts += head(pw, 22, pw, 'EMIB — 두 층')
    parts += box(x, 34, w, 40, ['칩'], 'fig-box')
    parts += box(x, 80, w, LH + 22 + 40 + 6, ['브리지를 심은 기판'], 'fig-agent')
    parts += legend([('fig-agent', '가운데 층이 기판 안으로')], max(y1, 80 + LH + 22 + 46) + 14)
    return svg(max(y1, 80 + LH + 22 + 46) + 40, parts, 'CoWoS-L 은 칩·유기 층(브리지)·기판 세 층이고 EMIB 는 브리지를 기판 안에 심어 두 층이다')


def _ap_reticle():
    """다이는 레티클 한 장(858제곱밀리미터)을 못 넘는데 패키지는 3.3배로 커진다 — 위아래."""
    sw = 140.0; sx = (W - sw * 3.3) / 2
    parts = head(0, 22, W, '패키지 — 레티클 3.3배')
    parts += _rect(sx, 34, sw * 3.3, 56, 'fig-stage')
    parts += head(0, 112, W, '다이 상한 — 레티클 1배 = 858제곱밀리미터')
    parts += _rect((W - sw) / 2, 124, sw, 56, 'fig-agent')
    parts += legend([('fig-agent', '다이 하나의 상한'), ('fig-stage', '패키지가 커지는 만큼')], 196)
    return svg(222, parts, '다이 하나는 레티클 한 장 858제곱밀리미터를 넘지 못한다. 패키지는 레티클 3.3배까지 커진다. 그 차이를 패키징이 메운다')


def _ap_panel():
    """300밀리미터 원형 웨이퍼와 500×500 사각 패널 — 같은 자에 그렸다."""
    L, R = 0.0, 272.0
    pw = 248.0
    k = 0.32
    parts = head(L, 22, pw, '원형 웨이퍼 300') + head(R, 22, pw, '사각 패널 500×500')
    cy = 34 + 500 * k / 2
    parts += ['  <circle cx="%g" cy="%g" r="%g" class="fig-box"/>' % (L + pw / 2, cy, 300 * k / 2)]
    parts += _rect(R + (pw - 500 * k) / 2, 34, 500 * k, 500 * k, 'fig-agent')
    parts += legend([('fig-agent', '넓이가 웨이퍼의 다섯~여섯 배')], 34 + 500 * k + 16)
    return svg(34 + 500 * k + 42, parts, '원형 300밀리미터 웨이퍼에서 큰 사각형을 떼면 가장자리를 버린다. 500 × 500밀리미터 사각 패널은 넓이가 다섯~여섯 배다. 같은 자로 그렸다')


def _ap_roadmap():
    """레티클 배수 로드맵 두 줄 — CoWoS 와 EMIB. 같은 폭."""
    h = 2 * LH + 22
    bw = w_of(['블랙웰 울트라'])  # 넷을 한 폭으로 놓으려면 라벨이 일곱 자를 넘으면 안 된다
    parts = head(0, 22, W, 'TSMC CoWoS')
    r1, _ = eband([(['3.3배'], 'fig-box'), ('>', ''), (['5.5배', '블랙웰 울트라'], 'fig-box'), ('>', ''),
                   (['9.5배'], 'fig-box'), ('>', ''), (['40배', '웨이퍼 한 장'], 'fig-outside')], 32, h, w=bw)
    parts += r1
    y2 = 32 + h + 44
    parts += head(0, y2 - 10, W, '인텔 EMIB')
    r2, _ = eband([(['8배', 'EMIB-T'], 'fig-box'), ('>', ''), (['12배 넘게', '2028년'], 'fig-outside')], y2, h, w=bw)
    parts += r2
    parts += legend([('fig-outside', '아직 안 나온 것')], y2 + h + 16)
    return svg(y2 + h + 42, parts, 'CoWoS 는 3.3배에서 5.5배(Blackwell Ultra·Rubin), 9.5배, System on Wafer 40배로. EMIB 는 EMIB-T 8배에서 2028년 12배 넘게(120 × 180밀리미터)')


AP = '2026-06-19-advanced-packaging'


# ══ 리소그래피 마스터클래스 (2026-05-22) 전략 판 ═══════════════════════════
# 값은 전사의 것만 — 10·20·30·40 / 5·15·25·35 야드, 2억 5천만·4억·6~8억·10억 달러, 50마이크로미터, 거울 열세 장,
# 개구수 0.33·0.55, 피처 1.5~1.7배, 스캐너 열 대.

def _li_multipattern():
    """멀티패터닝 — 10야드 간격 기계로 5야드 선을 긋는다. 같은 판 셋: 1단계·2단계·합침."""
    pw = 400.0; x0 = (W - pw) / 2
    rows = [('1단계 — 10 · 20 · 30 · 40', [10, 20, 30, 40], 'fig-agent'),
            ('2단계 — 5야드 옮겨 5 · 15 · 25 · 35', [5, 15, 25, 35], 'fig-box'),
            ('합치면 5야드 간격', [5, 10, 15, 20, 25, 30, 35, 40], 'fig-agent')]
    parts, y = [], 22
    for label, xs, cls in rows:
        parts += head(0, y, W, label)
        fy = y + 8
        parts += _rect(x0, fy, pw, 36, 'fig-stage')
        for v in xs:
            xx = x0 + pw * v / 45.0
            parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" style="stroke-width:%s"/>'
                      % (xx, fy + 4, xx, fy + 32, '2.4' if cls == 'fig-agent' else '1.4')]
        y = fy + 36 + 24
    return svg(y - 4, parts, '10야드마다밖에 못 긋는 기계로 10·20·30·40 을 긋고, 5야드 옮겨 5·15·25·35 를 다시 그으면 5야드 간격이 된다. 단계는 두 배, 처리량은 절반')


def _li_toolcost():
    """EUV 장비 값의 계단 — 낮은 개구수 → 높은 개구수 → 하이퍼 개구수."""
    h = 2 * LH + 22
    row, _x = eband([(['낮은 개구수', '2억 5천만 달러'], 'fig-box'), ('>', ''),
                     (['높은 개구수', '4억 달러'], 'fig-agent'), ('>', ''),
                     (['하이퍼 개구수', '6억~8억 달러'], 'fig-outside')], 30, h)
    parts = row + legend([('fig-agent', '지금 넘어가는 곳'), ('fig-outside', '아직 안 나옴')], 30 + h + 16)
    return svg(30 + h + 42, parts, '낮은 개구수 EUV 장비가 2억 5천만 달러, 높은 개구수가 4억 달러, 하이퍼 개구수는 6억에서 8억 달러이고 10억 달러까지 갈 수 있다')


def _li_lightpath():
    return _chain_down([(['주석 방울 50마이크로미터가 떨어진다'], 'fig-box'),
                        (['떨어지는 방울을 레이저로 두 번 때린다'], 'fig-box'),
                        (['플라스마에서 13.5나노미터 빛이 난다'], 'fig-agent'),
                        (['거울 열세 장을 거쳐 초점을 잡는다'], 'fig-box'),
                        (['웨이퍼에 닿는 빛 — 한 자릿수 퍼센트 미만'], 'fig-outside')],
                       '주석 방울을 레이저로 두 번 때려 13.5나노미터 빛을 만들고 거울 열세 장을 거치면, 웨이퍼에 닿는 양은 한 자릿수 퍼센트에도 못 미친다')


def _li_halffield():
    """하프 필드 — 같은 꼴 두 판. 개구수를 올리면 피처는 작아지고 한 번에 찍는 면적은 반이 된다."""
    L, R = 0.0, 272.0
    pw = 248.0
    parts = head(L, 22, pw, '개구수 0.33') + head(R, 22, pw, '개구수 0.55')
    fw, fh = 180.0, 100.0
    parts += _rect(L + (pw - fw) / 2, 34, fw, fh, 'fig-stage')
    parts += _rect(L + (pw - fw) / 2, 34, fw, fh, 'fig-agent')
    parts += _rect(R + (pw - fw) / 2, 34, fw, fh, 'fig-stage')
    parts += _rect(R + (pw - fw) / 2, 34, fw, fh / 2, 'fig-agent')
    parts += head(L, 34 + fh + 22, pw, '전부 · 2억 5천만 달러') + head(R, 34 + fh + 22, pw, '절반 · 4억 달러')
    parts += legend([('fig-agent', '한 번에 찍는 면적'), ('fig-stage', '노광 필드')], 34 + fh + 40)
    return svg(34 + fh + 66, parts, '개구수를 0.33 에서 0.55 로 올리면 피처는 1.5~1.7배 작아지지만 한 번에 찍는 면적은 절반이 된다. 값은 두 배 가까이 오른다')


def _li_fel():
    """광원 하나에서 빔을 쪼개 스캐너 열 대를 먹인다 — 모듈 여럿. 스캐너 수가 값이다."""
    sw, sh, g = 40.0, 30.0, 8.0
    total = 10 * sw + 9 * g
    x0 = (W - total) / 2
    parts = head(0, 22, W, '팹 안 — 스캐너 열 대')
    parts += _rect(x0 - 12, 34, total + 24, sh + 24, 'fig-outside')
    for k in range(10):
        parts += _rect(x0 + k * (sw + g), 46, sw, sh, 'fig-box')
    lw = w_of(['자유전자레이저'])
    ly = 34 + sh + 24 + 30
    parts += box((W - lw) / 2, ly, lw, 44, ['자유전자레이저'], 'fig-agent')
    parts += vline(W / 2, ly, 34 + sh + 24 + 2, arrow_=True)
    parts += head(0, ly + 44 + 20, W, '광원은 팹 밖 — xLight 가 세우고 빛을 판다')
    return svg(ly + 44 + 34, parts, '자유전자레이저 하나의 빔을 쪼개 스캐너 열 대를 먹인다. 광원은 xLight 가 세우고 팹은 빛을 산다. 칸 수가 값이다')


def _li_xray():
    """EUV 와 X선 — 파장을 바꾸면 광학도 마스크도 같이 바뀐다."""
    parts, y = table([[['빛'], ['13.5나노 극자외선'], ['1나노미터 X선']],
                      [['광학'], ['거울로 반사시킨다'], ['통과해 버려', '반사가 안 된다']],
                      [['마스크'], ['5분의 1로 줄인다'], ['웨이퍼와', '같은 치수로 만든다']]],
                     ['fig-stage', 'fig-box', 'fig-agent'],
                     heads=['', 'EUV', 'X선 근접 인쇄'], y0=36, arrows=False)
    return svg(y + 16, parts,
               'EUV 는 13.5나노 극자외선을 거울로 반사시켜 마스크를 5분의 1로 줄여 찍는데, X선은 물체를 통과해 반사가 안 되니 축소가 사라지고 마스크를 웨이퍼와 같은 치수로 만들어야 한다')


LI = '2026-05-22-litho-masterclass'

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]   머리에 「|문단 앞머리」를 붙이면 그 문단 앞
CB = '2026-05-15-cerebras-ipo'


def _cb_dice():
    """자르는 길과 안 자르는 길. 두 줄이 같은 자리에서 갈린다 — 웨이퍼 한 장에서."""
    top, _ = band([(['웨이퍼'], 'fig-box'), ('>', '자른다'),
                   (['다이로'], 'fig-box'), ('>', '패키징'),
                   (['칩 하나씩'], 'fig-box'), ('>', '잇는다'),
                   (['네트워크 · 스위치'], 'fig-box')], 40, 48)
    bot, _ = band([(['웨이퍼'], 'fig-box'), ('>', '안 자른다'),
                   (['웨이퍼 위 배선으로 이음'], 'fig-agent'), ('>', '그대로'),
                   (['칩 하나'], 'fig-box')], 132, 48)
    return svg(212,
               head(0, 30, 140, '통상') + top + head(0, 122, 140, 'Cerebras') + bot,
               '통상은 웨이퍼를 잘라 다이로 만들고 하나씩 패키징한 뒤 네트워크와 스위치로 다시 잇는다. Cerebras 는 자르지 않고 웨이퍼 위 금속 배선으로 이어 한 장을 칩 하나로 쓴다')


def _cb_yield():
    """결함을 다루는 순서. 코어 수는 캡션에 적고 도형으로는 안 센다."""
    parts, y = table([[['전원을 켜고 코어를 전수로 검사한다']],
                      [['신호가 없는 자리를 적어 둔다 — 「10행 13열」']],
                      [['웨이퍼 위 패브릭이 그 자리를 건너뛰어', '예비 코어로 배선을 돌린다']],
                      [['소프트웨어가 그 자리에 일을 안 보낸다']]],
                     ['fig-box'], y0=26)
    return svg(y + 16, parts,
               '전원을 켜 코어를 전수 검사하고, 신호가 없는 자리를 적어 두고, 패브릭이 그 자리를 건너뛰어 예비 코어로 배선을 돌리고, 소프트웨어가 그 자리에 일을 안 보낸다')


def _cb_stack():
    """층 셋과 각 층의 숙제. 값은 글자로만 — 커넥터 개수는 그리지 않는다."""
    parts, y = table([[['엔진 블록'], ['미세 유로가 수직으로 흘러', '한 장을 한꺼번에 식힌다']],
                      [['웨이퍼 한 장'], ['23킬로와트 · 수만 암페어를', '수백 지점에서 수직으로 받는다']],
                      [['기판'], ['열을 받으면 웨이퍼만 늘어나', '정렬이 어긋나고 커넥터가 뜯긴다']]],
                     ['fig-stage', 'fig-box'], heads=['층', '이 층의 숙제'], y0=36, arrows=False)
    return svg(y + 16, parts,
               '엔진 블록은 미세 유로로 한 장을 한꺼번에 식히고, 웨이퍼는 23킬로와트를 수백 지점에서 수직으로 받고, 기판은 웨이퍼만 늘어나 정렬이 어긋나는 자리다')


def _cb_wall():
    """44기가바이트 안과 밖. 병렬 셋은 글이 가른 항의 수다."""
    inside = mid(36, 2 * LH + 22, ['모델이 44기가바이트 안에 들어간다',
                                   'SRAM 초당 21페타바이트로 돈다'], 'fig-agent')
    y1 = 36 + 2 * LH + 22
    outside = mid(y1 + 30, LH + 22, ['넘으면 웨이퍼 밖으로 나간다'], 'fig-bad')
    y2 = y1 + 30 + LH + 22
    items = [(['파이프라인 병렬', '층을 나눠 차례로'], 'fig-box'),
             (['텐서 병렬', '행렬을 쪼개'], 'fig-box'),
             (['전문가 병렬', '전문가마다 한 장'], 'fig-box')]
    row, x_end, _cs, hh = panel_boxes(0, y2 + 30, items, gap=12, h=2 * LH + 22)
    y3 = y2 + 30 + hh
    tail = mid(y3 + 26, LH + 22, ['셋 다 웨이퍼 사이 통신에 기댄다'], 'fig-bad')
    parts = (inside + down(W / 2, y1 + 2, y1 + 28) + outside
             + down(W / 2, y2 + 2, y2 + 28) + row + down(W / 2, y3 + 2, y3 + 24) + tail)
    return svg(y3 + 26 + LH + 22 + 16, parts,
               '모델이 44기가바이트 안에 들어가면 SRAM 속도로 돌고, 넘으면 웨이퍼 밖으로 나가 파이프라인·텐서·전문가 병렬 셋 중 하나를 쓰는데 셋 다 웨이퍼 사이 통신에 기댄다')


def _cb_forty():
    """같은 발상이 40년 뒤에 제품이 된 자리. 해는 전사에 있는 것만."""
    parts, y = table([[['1980년대'], ['트릴로지 — 2.5인치 웨이퍼에서', '결함을 우회해 한 장을 통째로']],
                      [['1982'], ['폭풍이 공장을 잠기게 하고', '먼지가 청정실로 날려 든다']],
                      [['1983'], ['제품 없이 상장해 돈을 모았지만', '아무 일도 없었다']],
                      [['1989'], ['Amdahl 이 물러난다', '100년은 안 된다고 말한다']],
                      [['오늘'], ['같은 발상이 12인치 웨이퍼에서 제품', '바뀐 것은 웨이퍼 제조 성숙 하나']]],
                     ['fig-stage', 'fig-box'], heads=['언제', '무슨 일이'], y0=36)
    return svg(y + 16, parts,
               '1980년대 트릴로지가 2.5인치 웨이퍼로 같은 발상을 시도했고, 침수와 제품 없는 상장 끝에 1989년 물러났으며, 같은 발상이 오늘 12인치 웨이퍼에서 제품이 됐다')


def _cb_chain():
    """하드웨어를 안 파는 구조 — 사슬 넷을 한 회사가 지고, 돈은 토큰에서만 들어온다."""
    labels = [['제조·공급망'], ['데이터센터'], ['클라우드 운영'], ['토큰 공급']]
    w = max(w_of(l) for l in labels)
    gap = (W - 4 * w) / 3
    items = []
    for i, l in enumerate(labels):
        if i:
            items.append(('>', ''))
        items.append((l, 'fig-agent'))
    row, _x = eband(items, 40, 52, w=w, min_gap=14)
    cx = 3 * (w + gap) + w / 2
    buyer = mid(150, LH + 22, ['OpenAI 가 연산 시간과 토큰에 돈을 낸다'], 'fig-box')
    sold = mid(216, LH + 22, ['하드웨어 판매 — 없다'], 'fig-bad')
    parts = (row + down(cx, 94, 146) + buyer + sold
             + legend([('fig-agent', 'Cerebras 가 지는 자리')], 268))
    return svg(310, parts,
               '제조와 공급망, 데이터센터 건설, 클라우드 운영, 토큰 공급까지 한 회사가 지고 하드웨어는 팔지 않는다. 돈은 OpenAI 가 내는 연산 시간과 토큰 값으로만 들어온다')


QC = '2026-06-29-qualcomm-hbc'


def _qc_mix():
    """매출 구성 셋. 기둥 높이는 발표가 말한 분수 그대로 — 2/3, 1/2, 1/3."""
    cols = [('회계연도 25', 2 / 3.0), ('2027 목표', 1 / 2.0), ('회계연도 29', 1 / 3.0)]
    bw, gap, top, bh = 130.0, 40.0, 46.0, 180.0
    x0 = (W - (3 * bw + 2 * gap)) / 2
    parts = []
    for i, (name, share) in enumerate(cols):
        x = x0 + i * (bw + gap)
        h1 = bh * share
        parts += head(x, top - 14, bw, name)
        parts += box(x, top, bw, h1, ['손전화'], 'fig-box')
        parts += box(x, top + h1, bw, bh - h1, ['그 밖'], 'fig-agent')
    parts += legend([('fig-box', '손전화'), ('fig-agent', '자동차 · IoT · 데이터센터')], top + bh + 20)
    return svg(top + bh + 56, parts,
               '손전화가 회계연도 25 에 3분의 2, 2027 목표에서 절반, 회계연도 29 에 3분의 1로 줄고 그 자리를 자동차와 IoT 와 데이터센터가 채운다')


def _qc_disagg():
    """랙 하나로 채우던 것이 일별 랙 넷으로 갈린다. 랙 수는 진행자V 가 센 것 그대로."""
    before = mid(40, 2 * LH + 22, ['Nvidia 랙으로 채운다', 'Blackwell GPU · Vera CPU'], 'fig-box')
    y1 = 40 + 2 * LH + 22
    items = [(['CPU 랙', 'CPU 만'], 'fig-box'),
             (['프리필', 'Nvidia GPU'], 'fig-box'),
             (['디코드', 'Groq LPU'], 'fig-box'),
             (['디코드', '퀄컴 추론 랙'], 'fig-agent')]
    row, _x, _cs, hh = panel_boxes(0, y1 + 40, items, gap=12, h=2 * LH + 22)
    parts = (head(0, 30, 200, '예전') + before + down(W / 2, y1 + 2, y1 + 36)
             + head(0, y1 + 32, 200, '지금') + row
             + legend([('fig-agent', '퀄컴이 겨냥하는 자리')], y1 + 40 + hh + 20))
    return svg(y1 + 40 + hh + 56, parts,
               '예전에는 Nvidia 랙으로 데이터센터를 채웠고, 지금은 CPU 랙과 프리필 GPU 랙과 저지연 디코드 랙과 퀄컴 추론 랙으로 갈린다')


def _qc_hbc():
    """옆에 붙이는 길과 위에 얹는 길. 레인 수는 발표 값, 대역폭 배수는 원리 계산이다."""
    left = [['다이 한 변에만 접점'], ['레인 2,000'], ['CoWoS 같은 고급 패키징']]
    right = [['칩 면 전체가 접점'], ['레인 수만 ~ 10만'], ['표준 피치 패키지']]
    specs = [[left[i], right[i]] for i in range(3)]
    parts, y = table(specs, ['fig-box', 'fig-agent'],
                     heads=['옆에 붙인다 (쇼어라인)', '위에 얹는다 (HBC)'], y0=36, arrows=False)
    return svg(y + 16, parts,
               '옆에 붙이면 다이 한 변의 쇼어라인에만 접점을 낼 수 있어 레인이 2,000 이고 고급 패키징이 든다. 위에 얹으면 칩 면 전체가 접점이 되어 레인이 수만에서 10만까지 늘고 표준 피치 패키지로 끝난다')


def _qc_read():
    """메모리 밑에 무엇이 앉나 — 두 읽기. 밑에 앉는 것은 세로로, 옆에 붙는 것은 옆에 그린다."""
    lw, rw, gapx = 230.0, 170.0, 60.0
    x0 = (W - (lw + gapx + rw)) / 2
    memh, boxh = LH + 22, 2 * LH + 22
    parts, y = [], 34.0
    plans = [('진행자A 의 읽기', ['로직 칩', '소프트맥스 등 원시 연산'], ['XPU', '행렬 곱']),
             ('진행자V 의 읽기', ['XPU', '행렬 곱을 다 한다'], ['SoC', '나머지 일'])]
    for name, under, side in plans:
        parts += head(x0, y, lw, name)
        top = y + 12
        parts += box(x0, top, lw, memh, ['메모리'], 'fig-stage')
        parts += box(x0, top + memh, lw, boxh, under, 'fig-agent')
        parts += box(x0 + lw + gapx, top + memh, rw, boxh, side, 'fig-box')
        parts += hline(x0 + lw + 4, x0 + lw + gapx - 4, top + memh + boxh / 2)
        y = top + memh + boxh + 46
    parts += legend([('fig-agent', '메모리 바로 밑에 앉는 것'), ('fig-box', '옆에 붙는 것')], y - 20)
    return svg(y + 18, parts,
               '진행자A 는 메모리 밑에 원시 연산만 맡는 로직 칩이 앉고 XPU 는 옆에 붙는다고 읽었고, 진행자V 는 밑에 앉는 것이 행렬 곱을 다 하는 온전한 XPU 이고 옆의 SoC 가 나머지를 맡는다고 읽었다')


def _qc_tsv():
    """층을 올리면 층당 용량이 뒤집힌다. 절반과 넷은 진행자A 가 든 수다."""
    parts, y = table([[['한 층'], ['비아를 안 뚫어 밀도가 그대로 나온다']],
                      [['두 층부터'], ['비아 둘레에 셀을 못 놓는 금지 구역이 생겨', '층당 용량이 절반쯤으로 떨어진다']],
                      [['넷'], ['쌓아야 쓸모가 생긴다 — 둘은 못 쌓는다']]],
                     ['fig-stage', 'fig-box'], heads=['쌓는 층', '층당 용량'], y0=36, arrows=False)
    return svg(y + 16, parts,
               '한 층이면 비아가 없어 밀도가 그대로 나오고, 두 층부터는 관통 비아 금지 구역 때문에 층당 용량이 절반쯤으로 떨어져 넷은 쌓아야 쓸모가 생긴다')


def _qc_road():
    """가속기 로드맵. 해는 발표가 댄 것만."""
    parts, y = table([[['AI 100'], ['오래전 물건']],
                      [['AI 200'], ['2026 샘플 · HBC 없음']],
                      [['AI 250'], ['2027 · HBC 1세대']],
                      [['AI 300'], ['회계연도 28 · HBC 2세대', 'UALink·E-sun · 광 스케일아웃']],
                      [['스케일업 CPO'], ['그 뒤 — 2029 쯤']]],
                     ['fig-stage', 'fig-box'], heads=['제품', '언제 · 무엇이 들어가나'], y0=36)
    return svg(y + 16, parts,
               'AI 200 은 2026 년 샘플이지만 HBC 가 없고, HBC 1세대는 2027 년 AI 250, 2세대는 회계연도 28 의 AI 300 이며 스케일업 CPO 는 그 뒤 2029 년쯤이다')


GN = '2026-04-24-google-networking'
HW = '2026-05-29-huawei-tau'
MC = '2026-07-03-micron-cxmt'


# ══ 구글 네트워킹 (2026-04-24) 전략 판 ═══════════════════════
# 값은 전사의 것만 — 384MB·288GB·216GB, 13.1·47페타비트, 134,000, 1,152, 8홉·16홉·7홉.

def _gn_gens():
    """TPU 세대별로 칩이 하나였다 둘이었다 하는 이력. 가로 한 줄, 나뉜 세대만 다른 색."""
    h = 2 * LH + 22
    items = [(['v1', '추론 전용'], 'fig-agent'), (['v2~v4', '훈련·서빙'], 'fig-box'),
             (['v5', '효율·성능'], 'fig-agent'), (['v6~v7', '한 칩'], 'fig-box'),
             (['v8', '8T·8I'], 'fig-agent')]
    ws = [w_of(l) for l, _ in items]
    gap = (W - sum(ws)) / (len(items) - 1)
    parts, x = [], 0.0
    for (l, c), w in zip(items, ws):
        parts += box(x, 40, w, h, l, c)
        x += w + gap
    parts += legend([('fig-agent', '칩이 나뉜 세대')], 40 + h + 16)
    return svg(40 + h + 42, parts,
               'TPU 는 v1 추론 전용에서 v2~v4 훈련·서빙 겸용, v5 효율·성능 분리, v6~v7 단일 칩을 거쳐 v8 에서 훈련용 8T 와 추론용 8I 로 다시 나뉘었다')


def _gn_mem():
    """추론칩과 훈련칩의 메모리. 같은 꼴 둘을 나란히 — SRAM 은 추론이 세 배, HBM 도 추론이 더 많다."""
    L, R = 0.0, 268.0
    pw = 252.0
    parts = head(L, 24, pw, '추론칩 8I') + head(R, 24, pw, '훈련칩 8T')
    rows = [(['SRAM', '384메가바이트'], ['SRAM', '그 3분의 1']),
            (['HBM', '288기가바이트'], ['HBM', '216기가바이트'])]
    y = 40
    hh = 2 * LH + 22
    for a, b in rows:
        parts += box(L, y, pw, hh, a, 'fig-agent')
        parts += box(R, y, pw, hh, b, 'fig-box')
        y += hh + 14
    parts += head(0, y + 14, W, '추론은 층을 다 채우고, 훈련은 칩을 더 붙인다')
    return svg(y + 30, parts,
               '추론칩 8I 는 SRAM 384메가바이트로 훈련칩 8T 의 세 배이고 HBM 도 288기가바이트로 훈련칩 216기가바이트보다 많다')


def _gn_layers():
    """망 계층이 셋에서 둘로. 같은 꼴 두 줄, 대역폭은 줄 아래에."""
    h = LH + 24
    parts = head(0, 22, W, '이전 Jupiter — 계층 셋')
    r1, _ = eband([(['리프'], 'fig-box'), ('>', ''), (['스파인'], 'fig-box'), ('>', ''),
                   (['슈퍼스파인'], 'fig-box'), ('>', ''), (['목적지'], 'fig-stage')], 32, h)
    parts += r1
    parts += head(0, 32 + h + 24, W, '초당 13.1페타비트')
    y2 = 32 + h + 76
    parts += head(0, y2 - 10, W, 'Virgo — 광회선 스위치로 계층 둘')
    r2, _ = eband([(['보내는 쪽'], 'fig-box'), ('>', ''), (['OCS 두 계층'], 'fig-agent'), ('>', ''),
                   (['목적지'], 'fig-stage')], y2, h)
    parts += r2
    parts += head(0, y2 + h + 24, W, '초당 47페타비트 · TPU 134,000개가 한 덩이')
    return svg(y2 + h + 40, parts,
               '이전 Jupiter 망은 리프·스파인·슈퍼스파인 세 계층에 초당 13.1페타비트였고, Virgo 는 광회선 스위치로 계층을 둘로 줄여 초당 47페타비트로 TPU 134,000개를 묶었다')


def _gn_hops():
    """홉 수 셋을 나란한 세로 막대로. 3D 토러스 둘과 Boardfly 하나."""
    bars = [(8, '8홉', '4x4x8 토러스', 'fig-box'), (16, '16홉', '8x8x16 토러스', 'fig-box'),
            (7, '7홉', 'Boardfly', 'fig-agent')]
    base, scale, bw = 190.0, 9.0, 96.0
    pw = W / 3
    parts = []
    for i, (v, lab, name, cls) in enumerate(bars):
        x0 = i * pw
        hh = v * scale
        parts += _rect(x0 + (pw - bw) / 2, base - hh, bw, hh, cls)
        parts += head(x0, base - hh - 8, pw, lab)
        parts += head(x0, base + 22, pw, name)
    parts += hline(10, W - 10, base)
    parts += head(0, base + 48, W, '보드 4칩 · 랙 8보드 · 파드 36그룹 = 1,152칩')
    return svg(base + 62, parts,
               '3D 토러스는 4x4x8 배치에서 8홉, 구글 블로그가 든 8x8x16 배치에서 16홉이 든다. Boardfly 는 같은 거리를 7홉으로 줄인다')


# ══ 화웨이 타우 (2026-05-29) 전략 판 ════════════════════════
# 값은 전사의 것만 — 알파 1.3·1.5·10배, 피치 1.5마이크론, 트랜지스터 두 배, 400층, BESI 중국 35%.

def _hw_alpha():
    """타우 셈법 — 다음 세대 지연은 이번 지연을 알파로 나눈 값. 알파 셋을 나란한 막대로."""
    parts = head(0, 24, W, '다음 세대 지연 = 이번 세대 지연 ÷ 알파')
    bars = [(1.3, '연 1.3배', '모바일'), (1.5, '연 1.5배', '자동차'), (10, '최대 10배', 'AI')]
    base, scale, bw = 190.0, 13.0, 92.0
    pw = W / 3
    for i, (v, lab, name) in enumerate(bars):
        x0 = i * pw
        hh = v * scale
        cls = 'fig-agent' if v == 10 else 'fig-box'
        parts += _rect(x0 + (pw - bw) / 2, base - hh, bw, hh, cls)
        parts += head(x0, base - hh - 8, pw, lab)
        parts += head(x0, base + 22, pw, name)
    parts += hline(10, W - 10, base)
    return svg(base + 40, parts,
               '타우 스케일링 법칙은 다음 세대 지연을 이번 세대 지연을 알파로 나눈 값으로 잡는다. 알파는 모바일 연 1.3배, 자동차 연 1.5배, AI 워크로드는 최대 10배로 제시됐다')


def _hw_stack():
    """로직 위에 로직. 위아래 층 셋 — 아래 로직, 접합면, 위 로직."""
    h = LH + 24
    w = w_of(['하이브리드 본딩 — 접속 피치 1.5마이크론'])
    x = (W - w) / 2
    parts = box(x, 30, w, h, ['로직 다이 — 위'], 'fig-box')
    parts += box(x, 30 + h + 10, w, h, ['하이브리드 본딩 — 접속 피치 1.5마이크론'], 'fig-agent')
    parts += box(x, 30 + 2 * (h + 10), w, h, ['로직 다이 — 아래'], 'fig-box')
    y = 30 + 3 * (h + 10) + 14
    parts += head(0, y, W, 'Kirin 2026 — 같은 면적에 트랜지스터 두 배')
    parts += head(0, y + 26, W, '로직끼리는 발열·정렬·평탄도가 함께 걸린다')
    return svg(y + 42, parts,
               '하이브리드 본딩으로 로직 다이 위에 로직 다이를 얹는다. 접속 피치는 1.5마이크론이고 Kirin 2026 은 같은 면적에 트랜지스터가 두 배다')


def _hw_control():
    """통제가 걸린 자리와 안 걸린 자리. 왼쪽 노광, 오른쪽 접합."""
    h = 2 * LH + 22
    L, R = 0.0, 268.0
    pw = 252.0
    parts = head(L, 24, pw, '노광') + head(R, 24, pw, '접합')
    parts += box(L, 40, pw, h, ['ASML EUV', '통제 대상'], 'fig-bad')
    parts += box(R, 40, pw, h, ['하이브리드 본딩', '통제 대상 아님'], 'fig-agent')
    y = 40 + h + 14
    parts += box(L, y, pw, h, ['중국은 애초에', '산 적이 없다'], 'fig-stage')
    parts += box(R, y, pw, h, ['BESI 네덜란드', '중국 매출 35%'], 'fig-box')
    y2 = y + h + 14
    parts += box(R, y2, pw, h, ['EV Group 오스트리아', '통제 축이 다르다'], 'fig-box')
    parts += legend([('fig-bad', '막힌 길'), ('fig-agent', '안 막힌 길')], y2 + h + 16)
    return svg(y2 + h + 42, parts,
               'EUV 노광 장비는 수출통제 대상이지만 하이브리드 본딩 장비는 아니다. BESI 는 네덜란드 회사로 중국 매출이 35%이고 EV Group 은 오스트리아 회사라 통제 축이 다르다')


# ══ 마이크론·CXMT (2026-07-03) 전략 판 ═════════════════════
# 값은 전사의 것만 — 45·56·75·85%, 웨이퍼 세 배, 5천억 달러, 3분의 2, 4기가바이트→2기가바이트.

def _mc_margin():
    """매출총이익률 넉 분기. 가로로 흐르는 막대, 높이가 값."""
    vals = [(45, '45%'), (56, '56%'), (75, '75%'), (85, '85%')]
    base, scale, bw = 180.0, 1.7, 84.0
    pw = W / 4
    parts = []
    for i, (v, lab) in enumerate(vals):
        x0 = i * pw
        hh = v * scale
        cls = 'fig-agent' if i == 3 else 'fig-box'
        parts += _rect(x0 + (pw - bw) / 2, base - hh, bw, hh, cls)
        parts += head(x0, base - hh - 8, pw, lab)
    parts += hline(10, W - 10, base)
    parts += head(0, base + 24, W, '넉 분기 · 다음 분기도 85~86% 전망')
    return svg(base + 40, parts,
               '마이크론 매출총이익률은 넉 분기 만에 45%에서 56%, 75%, 85%로 올랐고 다음 분기도 85~86%를 전망한다')


def _mc_wafer():
    """같은 비트 용량에 드는 웨이퍼. 일반 D램 한 장, HBM 세 장."""
    h = LH + 24
    L, R = 0.0, 268.0
    pw = 252.0
    parts = head(L, 24, pw, '일반 D램') + head(R, 24, pw, 'HBM')
    parts += box(L, 40, pw, h, ['웨이퍼 1장'], 'fig-box')
    for i in range(3):
        parts += box(R, 40 + i * (h + 8), pw, h, ['웨이퍼 1장'], 'fig-agent')
    y = 40 + 3 * (h + 8) + 8
    parts += head(0, y, W, '같은 비트 용량 · 실리콘관통전극 둘레에는 셀을 못 놓는다')
    return svg(y + 16, parts,
               '같은 비트 용량을 만드는 데 일반 D램은 웨이퍼 한 장, HBM 은 세 장이 든다. 실리콘관통전극 둘레에 셀을 넣지 못하기 때문이다')


def _mc_elastic():
    """값이 오를 때 두 수요가 하는 일. 같은 꼴 두 줄."""
    h = 2 * LH + 22
    parts = head(0, 24, W, '메모리 값이 오르면')
    r1, _ = eband([(['소비자 기기'], 'fig-box'), ('>', ''), (['4기가바이트를', '2기가바이트로'], 'fig-bad')], 40, h)
    parts += r1
    y2 = 40 + h + 20
    r2, _ = eband([(['데이터센터'], 'fig-box'), ('>', ''), (['값과 무관하게', '그대로 산다'], 'fig-agent')], y2, h)
    parts += r2
    parts += head(0, y2 + h + 26, W, 'D램 증설에 5천억 달러 · 세계 물량 3분의 2가 한국')
    return svg(y2 + h + 42, parts,
               '메모리 값이 오르면 소비자 기기는 탑재량을 4기가바이트에서 2기가바이트로 줄이고 데이터센터는 값과 무관하게 그대로 산다')


# ══ Gimlet (2026-05-12) 전략 판 ═══════════════════════════════════════
# 값은 전사에 있는 것만. 칩 이름은 전사가 그 조각에 붙인 것만 적는다.

GIM = '2026-05-12-gimlet-inference-cloud'


def _gim_pieces():
    """위는 추론을 한 덩어리로 본 구성, 아래는 조각으로 나눈 구성. 조각 셋은 이 회차가
    이름을 댄 것뿐이다 — 프리필·디코드·도구 호출."""
    parts = head(0, 22, W, '한 덩어리로 볼 때')
    parts += mid(32, 46, ['추론 한 덩어리 · 칩 한 종류'], 'fig-bad')
    parts += head(0, 118, W, '조각으로 나눌 때')
    items = [(['프리필'], 'fig-box'), (['디코드'], 'fig-box'), (['도구 호출'], 'fig-box')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 18
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 128, items, gap=18, h=LH + 26)
    parts += row
    chips = [['GPU'], ['GPU'], ['CPU']]
    y2 = 128 + hh + 40
    for (cx, w), c in zip(cs, chips):
        parts += vline(cx, 128 + hh + 2, y2 - 2)
        parts += box(cx - w / 2, y2, w, LH + 26, c, 'fig-agent')
    y = y2 + LH + 26
    parts += legend([('fig-bad', '깨진다고 본 전제'), ('fig-agent', '조각마다 다른 칩')], y + 16)
    return svg(y + 42, parts,
               '추론을 한 덩어리로 보면 칩도 한 종류지만, 프리필·디코드·도구 호출로 나누면 조각마다 맞는 칩이 다르다')


def _gim_stack():
    """이 회사가 파는 것의 동작 순서 넷. 상자를 한 폭으로 두어 어느 단계가 더 커 보이지 않게 한다."""
    row, _x = eband([(['① 추적'], 'fig-box'), ('>', ''),
                     (['② 그래프'], 'fig-box'), ('>', ''),
                     (['③ 나누기'], 'fig-agent'), ('>', ''),
                     (['④ 컴파일'], 'fig-box')], 40, LH + 26)
    parts = list(row)
    y = 40 + LH + 26
    parts += legend([('fig-agent', '이 회사의 성격이 드러나는 자리')], y + 16)
    return svg(y + 42, parts,
               'PyTorch 실행을 추적해 그래프로 옮기고 어디서 끊을지 정해 나눈 뒤 조각마다 대상 하드웨어로 컴파일한다')


def _gim_toolcall():
    """도구 호출이 도는 자리 둘. 왼쪽은 오늘의 코딩 에이전트, 오른쪽은 모델 옆에서 끝내는 구성."""
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '도구가 내 노트북에') + head(R, 22, 248, '도구가 모델 옆에')
    parts += box(L + 4, 38, 240, LH + 26, ['모델 — 남의 서버'], 'fig-box')
    parts += box(L + 4, 150, 240, LH + 26, ['도구 — 내 노트북'], 'fig-box')
    parts += vline(L + 158, 38 + LH + 26 + 2, 148)
    parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="url(#aieArw)"/>'
              % (L + 90, 148, L + 90, 38 + LH + 26 + 2)]
    parts += box(L + 4, 150 + LH + 26 + 22, 240, 44, ['왕복이 지연을 정한다'], 'fig-bad')
    parts += box(R + 4, 38, 240, LH * 2 + 26 + 49, ['모델과 도구가', '같은 서버 안'], 'fig-agent')
    parts += box(R + 4, 150 + LH + 26 + 22, 240, 44, ['종단 지연이 낫다'], 'fig-agent')
    y = 150 + LH + 26 + 22 + 44
    parts += legend([('fig-bad', '네트워크에 묶이는 자리'), ('fig-agent', '이 회차가 든 구성')], y + 16)
    return svg(y + 42, parts,
               '도구 실행이 노트북에 있으면 모델과 계속 오가고 모델 옆으로 옮기면 그 왕복이 사라진다')


def _gim_three():
    parts, y_end = table(
        [[['①'], ['프리필·디코드를', 'GPU 에서 나눔'], ['바탕']],
         [['②'], ['거기에 투기적 디코딩,', '전부 GPU 에서'], ['①보다 위']],
         [['③'], ['초안 1.6B 만', 'Corsair 로'], ['②의 선 위에서', '다시 4배']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['구성', '무엇을 바꿨나', '곡선에서'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               'GPT-OSS 120B 를 같은 조건에 두고 세 구성을 견줬고 초안 모델만 Corsair 로 옮긴 구성이 다시 4배로 갔다')


def _gim_amort():
    """네오클라우드 연간 비용 기둥 하나. 70% 는 전사의 값이고 나머지는 그 나머지다."""
    x0, w = 120.0, 120.0
    y0, h = 46.0, 200.0
    hw = h * 0.7
    parts = ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
             % (x0 + w / 2, 30, '연간 비용 전부')]
    parts += _rect(x0, y0, w, hw, 'fig-agent')
    parts += _rect(x0, y0 + hw, w, h - hw, 'fig-stage')
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
              % (x0 + w / 2, y0 + hw / 2 + 6, '70%')]
    parts += hline(x0 + w, x0 + w + 30, y0 + hw / 2)
    parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>' % (x0 + w + 38, y0 + hw / 2 + 5, '하드웨어 상각')]
    parts += hline(x0 + w, x0 + w + 30, y0 + hw + (h - hw) / 2)
    parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>'
              % (x0 + w + 38, y0 + hw + (h - hw) / 2 + 5, '나머지 전부')]
    return svg(y0 + h + 30, parts,
               '네오클라우드 연간 비용에서 하드웨어 상각이 70% 이고 나머지를 조여도 비용 구조가 크게 바뀌지 않는다')


# ══ 메타 광고 인프라 (2026-04-20) 전략 판 ══════════════════════════════
# 값은 전사에 있는 것만 — 하루 30억 명, 1초, 적응형 랭킹 모델 1조 파라미터, 커널 100배.

MET = '2026-04-20-meta-steiner'


def _met_serve():
    parts, y_end = table(
        [[['① 앞단이 묻는다'], ['다음에 보여줄', '가장 좋은 광고']],
         [['② 검색 — Andromeda'], ['긴 목록에서', '흥미로울 것만']],
         [['③ 랭킹'], ['전환 확률 ×', '기대 가치']],
         [['④ 노출'], ['하루 30억 명 이상']]],
        ['fig-box', 'fig-stage'], heads=['단계', '하는 일'], y0=36)
    parts += mid(y_end + 22, 44, ['검색 요청은 1초 아래'], 'fig-agent')
    return svg(y_end + 22 + 44 + 16, parts,
               '앞단의 요청을 받아 검색이 후보를 추리고 랭킹이 순서를 정해 노출까지 가는데 검색 요청은 1초 아래에서 끝나야 한다')


def _met_lattice():
    parts, y_end = table(
        [[['목적마다 따로 선', '랭킹 모델 여럿'], ['사본과 계산이', '되풀이된다']],
         [['Lattice — 하나로'], ['비용이 줄고', '성능이 오른다']],
         [['GEM — 가장 큰 모델'], ['그대로는', '못 올린다']],
         [['증류한 작은 모델'], ['올릴 수 있는 크기']]],
        ['fig-box', 'fig-stage'], heads=['모델', '그래서'], y0=36)
    return svg(y_end + 12, parts,
               '목적마다 따로 서 있던 랭킹 모델을 Lattice 로 합치고 GEM 까지 키운 뒤 증류해서 서비스에 올린다')


def _met_adaptive():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '이력이 짧은 사람') + head(R, 22, 248, '이력이 긴 사람')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['적은 연산'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['많은 연산', '예측이 더 맞는다'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += mid(y + 22, 44, ['같은 1초 예산 · 파라미터 1조'], 'fig-stage')
    y2 = y + 22 + 44
    parts += legend([('fig-agent', '연산을 더 쓰는 쪽')], y2 + 16)
    return svg(y2 + 42, parts,
               '같은 1초 예산 안에서 이력이 긴 사람에게 훨씬 많은 연산을 쓰고 추론 시점 파라미터는 대략 1조다')


def _met_example():
    parts = head(0, 22, 248, '언어 모델 훈련 예제') + head(272, 22, 248, '추천 훈련 예제')
    parts += box(4, 32, 240, 2 * LH + 26, ['예제 하나가 작다'], 'fig-box')
    parts += box(276, 32, 240, 2 * LH + 26, ['예제마다', '개인화 덩어리가 붙는다'], 'fig-agent')
    y = 32 + 2 * LH + 26
    items = [(['더 굵은', '네트워크'], 'fig-stage'), (['더 많은', '온보드 메모리'], 'fig-stage'),
             (['연산 대비', '메모리 비율 낮게'], 'fig-stage')]
    row, _x, cs, hh = panel_boxes(0, y + 76, items, gap=10, h=2 * LH + 26)
    parts += row
    parts += vline(396, y + 4, y + 40, arrow_=False)          # 추천 쪽에서만 내려온다
    parts += hline(cs[0][0], 396, y + 40)
    for cx, _w in cs:
        parts += vline(cx, y + 40, y + 74)
    y2 = y + 76 + hh
    parts += legend([('fig-agent', '추천 쪽에만 붙는 짐')], y2 + 16)
    return svg(y2 + 42, parts,
               '추천 훈련은 예제마다 개인화 덩어리가 실려서 더 굵은 네트워크와 더 많은 온보드 메모리, 낮은 연산 대비 메모리 비율을 요구한다')


def _met_kernel():
    items = [(['① 하드웨어별로', '손으로 최적화'], 'fig-box'),
             (['② 번역 계층을', '끼워 넣는다'], 'fig-box'),
             (['③ 모델이 커널을', '직접 짠다'], 'fig-agent')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 10
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 40, items, gap=10, h=2 * LH + 26)
    parts = list(row)
    notes = [['느리고 비싸다'], ['성능이 가려진다'], ['커널을 100배로']]
    y2 = 40 + hh + 40
    for (cx, w), nt in zip(cs, notes):
        parts += vline(cx, 40 + hh + 2, y2 - 2)
        parts += box(cx - w / 2, y2, w, LH + 26, nt, 'fig-stage')
    y = y2 + LH + 26
    parts += legend([('fig-agent', '최근에 생긴 갈래')], y + 16)
    return svg(y + 42, parts,
               '하드웨어별 손 최적화와 번역 계층에 더해 모델이 커널을 직접 짜는 갈래가 생겼고 그쪽은 커널을 100배 원한다')


# ══ 인텔·오픈클로 (2026-04-10) 전략 판 ═════════════════════════════════
# 값은 전사에 있는 것만 — 월 200달러, 5분에 5~7달러, 월 2만 달러, 주 7달러,
# 5천 달러·5년, 300→530달러, 칩 256개.

INT = '2026-04-10-intel-openclaw'


def _int_price():
    parts, y_end = table(
        [[['정액 구독'], ['월 200달러'], ['기계가 돌자 막혔다']],
         [['API 종량'], ['5분에 5~7달러'], ['월 2만 달러였을 수도']],
         [['정액 무제한'], ['주 7달러'], ['최전선이 아닌 모델']]],
        ['fig-stage', 'fig-box', 'fig-box'], heads=['얻는 길', '값', '그래서'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '월 200달러 정액이 막히자 API 종량으로는 5분에 5~7달러가 나갔고 주 7달러짜리 무제한으로 내려갔다')


def _int_buy():
    """빌려 쓰기와 사서 갖기. 아래 줄에만 되팔 때의 값이 붙는다."""
    parts = head(0, 22, W, '빌려 쓴다')
    parts += mid(32, 46, ['매달 나간다'], 'fig-box')
    parts += head(0, 118, W, '사서 갖는다')
    items = [(['5천 달러'], 'fig-box'), (['5년 쓴다'], 'fig-box'), (['되팔면 회수'], 'fig-agent')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 24
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 128, items, gap=24, h=LH + 26)
    parts += row
    for i in range(len(cs) - 1):
        cx, w = cs[i]
        parts += hline(cx + w / 2 + 2, cs[i + 1][0] - cs[i + 1][1] / 2 - 2, 128 + hh / 2)
    y = 128 + hh
    parts += mid(y + 22, 44, ['300달러에 사서 530달러에 팔았다'], 'fig-stage')
    y2 = y + 22 + 44
    parts += legend([('fig-agent', '빌려 쓸 때는 없는 항')], y2 + 16)
    return svg(y2 + 42, parts,
               '빌려 쓰면 매달 나가지만 사서 가지면 5천 달러를 5년에 걸쳐 거두고 되팔 때 남는 값이 하나 더 붙는다')


def _int_ipu():
    parts = mid(30, 46, ['호스트 CPU'], 'fig-box')
    items = [(['스토리지'], 'fig-stage'), (['네트워킹'], 'fig-stage'), (['보안'], 'fig-stage')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 16
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 150, items, gap=16, h=LH + 26)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, 78, 148)
    y = 150 + hh
    parts += mid(y + 22, 46, ['IPU 가 맡는다'], 'fig-agent')
    for cx, _w in cs:
        parts += vline(cx, y + 2, y + 20)
    y2 = y + 22 + 46
    parts += vline(W / 2, y2 + 2, y2 + 20)
    parts += mid(y2 + 22, 46, ['CPU 에는 코어와 연산을 더 채운다'], 'fig-box')
    y3 = y2 + 22 + 46
    parts += legend([('fig-agent', '구글과 인텔이 함께 설계한 칩')], y3 + 16)
    return svg(y3 + 42, parts,
               '스토리지와 네트워킹과 보안을 호스트 CPU 에서 떼어 IPU 가 맡으면 CPU 에는 코어와 연산을 더 채울 수 있다')


def _int_memory():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, 'Groq LPU') + head(R, 22, 248, 'SambaNova RDU')
    parts += box(L + 4, 38, 240, LH + 26, ['SRAM 뿐'], 'fig-box')
    parts += box(R + 4, 38, 240, 3 * LH + 26, ['SRAM', 'HBM', 'DRAM'], 'fig-agent')
    y = 38 + 3 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['연산과 메모리가', '물리적으로 붙는다'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['오갈 경로를', '미리 정해 둔다'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += box(L + 4, y2 + 22, 240, LH + 26, ['수천 개'], 'fig-stage')
    parts += box(R + 4, y2 + 22, 240, LH + 26, ['256개'], 'fig-stage')
    y3 = y2 + 22 + LH + 26
    parts += legend([('fig-agent', '메모리를 섞은 쪽'), ('fig-stage', '같은 일을 하는 칩 수')], y3 + 16)
    return svg(y3 + 42, parts,
               '전부 SRAM 인 쪽은 칩이 수천 개 필요하고 SRAM·HBM·DRAM 을 섞고 경로를 미리 정한 쪽은 256개로 같은 일을 한다')


def _int_winners():
    items = [(['Groq'], 'fig-box'), (['Cerebras'], 'fig-box'), (['SambaNova'], 'fig-box')]
    w1 = sum(w_of(l) for l, _ in items) + 2 * 12
    row, _x, cs, hh = panel_boxes((W - w1) / 2, 34, items, gap=12, h=LH + 26)
    parts = list(row)
    items2 = [(['Etched'], 'fig-box'), (['Mad Max'], 'fig-box'), (['Talos'], 'fig-box')]
    w2 = sum(w_of(l) for l, _ in items2) + 2 * 12
    row2, _x2, cs2, hh2 = panel_boxes((W - w2) / 2, 34 + hh + 10, items2, gap=12, h=LH + 26)
    parts += row2
    y = 34 + hh + 10 + hh2
    parts += mid(y + 26, 46, ['손익분기에 닿을 물량'], 'fig-stage')
    parts += vline(W / 2, y + 2, y + 24)
    y2 = y + 26 + 46
    parts += mid(y2 + 26, 46, ['그만한 물량을 움직일 고객 다섯 여섯'], 'fig-agent')
    parts += vline(W / 2, y2 + 2, y2 + 24)
    y3 = y2 + 26 + 46
    parts += mid(y3 + 26, 46, ['서버에서 못 뜨면 소비자용으로'], 'fig-box')
    parts += vline(W / 2, y3 + 2, y3 + 24)
    y4 = y3 + 26 + 46
    parts += legend([('fig-agent', '조합 수를 정하는 자리')], y4 + 16)
    return svg(y4 + 42, parts,
               '이름이 나온 여섯 곳이 손익분기 물량이라는 좁은 목을 지나야 하고 그만한 물량을 움직일 고객은 다섯이나 여섯이다')


# ══ Credo·더스트포토닉스 (2026-04-17) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 2030년, 1.6Tbps·12.8Tbps, 200Gbps 채널 64개, 400W.

CRD = '2026-04-17-credo-dustphotonics'


def _crd_portfolio():
    parts, y_end = table(
        [[['서데스 IP'], ['빌려주는 데서 시작']],
         [['AEC 구리 케이블'], ['손수 만든다']],
         [['광학 DSP·트랜시버'], ['갖췄다']],
         [['파일럿 소프트웨어'], ['끊길 링크를 미리 간다']],
         [['광집적회로 설계'], ['없던 칸 — 이번에 채웠다']]],
        ['fig-box', 'fig-stage'], heads=['칸', '상태'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '서데스와 구리 케이블과 광학 DSP 와 감시 소프트웨어를 갖췄는데 광집적회로 설계만 없었고 이번 인수로 그 칸이 채워졌다')


def _crd_vectors():
    row, _x = eband([(['스케일 업'], 'fig-box'), ('>', ''),
                     (['스케일 아웃'], 'fig-box'), ('>', ''),
                     (['스케일 어크로스'], 'fig-agent')], 40, LH + 26)
    parts = list(row)
    y = 40 + LH + 26
    items = [(['랙 안', '구리는 2030년까지'], 'fig-stage'),
             (['랙 사이', '여전히 구리로'], 'fig-stage'),
             (['데이터센터 사이', '코히런트 광통신'], 'fig-stage')]
    row2, _x2, cs2, hh2 = panel_boxes(0, y + 30, items, gap=12, h=2 * LH + 26)
    parts += row2
    for cx, _w in cs2:
        parts += vline(cx, y + 2, y + 28)
    y2 = y + 30 + hh2
    parts += legend([('fig-agent', '다음 성장 축으로 꼽힌 구간')], y2 + 16)
    return svg(y2 + 42, parts,
               '랙 안은 구리가 2030년까지 남고 랙 사이도 여전히 구리로 갈 수 있으며 다음 성장 축은 데이터센터 사이를 잇는 코히런트 광통신이다')


def _crd_laser():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '레이저를 칩 위에 얹는다') + head(R, 22, 248, '레이저를 칩 옆에 놓는다')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['그 레이저 회사와', '공급망에 묶인다'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['아무 연속파 레이저나', '손실 없이 결합'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, LH + 26, ['사이에 공기 틈'], 'fig-bad')
    parts += box(R + 4, y + 22, 240, LH + 26, ['공기 틈 없음'], 'fig-agent')
    y2 = y + 22 + LH + 26
    parts += mid(y2 + 24, 46, ['액체 냉각에 그대로 넣을 수 있나'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-bad', '냉각을 막는 자리'), ('fig-agent', '더스트포토닉스의 방식')], y3 + 16)
    return svg(y3 + 42, parts,
               '레이저를 칩 위에 얹으면 공급망에 묶이고 사이에 공기 틈이 남는데 옆에 놓고 결합하면 공기 틈이 없어 액체 냉각에 그대로 넣는다')


def _crd_bars():
    """커넥터 하나가 내는 대역폭. 나란한 세로 막대 둘, 높이는 값의 비율이다."""
    base, top = 250.0, 40.0
    bw = 96.0
    xs = [140.0, 290.0]
    vals = [('OSFP', '1.6Tbps', 1.6), ('XPO', '12.8Tbps', 12.8)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 12.8
        cls = 'fig-agent' if name == 'XPO' else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(110, 420, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, '200Gbps 채널 64개를 한 커넥터에')]
    parts += legend([('fig-agent', '올해 나온 규격')], base + 70)
    return svg(base + 100, parts,
               '커넥터 하나가 내는 대역폭이 OSFP 는 1.6Tbps 이고 XPO 는 200Gbps 채널 64개를 몰아 12.8Tbps 다')


def _crd_place():
    parts, y_end = table(
        [[['CPO'], ['스위치 실리콘과', '한 패키지 안'], ['못 갈아 끼운다']],
         [['XPO'], ['랙 앞면에 꽂는다'], ['빼서 갈아 끼운다']],
         [['CPX'], ['칩 옆 소켓에 꽂는다'], ['소켓째 갈아 끼운다']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['이름', '광학 엔진이 앉는 자리', '고장 나면'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               'CPO 는 광학 엔진을 스위치 칩과 한 패키지에 넣고 XPO 는 랙 앞면에 꽂으며 CPX 는 칩 옆 소켓에 꽂아 갈아 끼운다')


# ══ MatX (2026-04-09) 전략 판 ═══════════════════════════════════════════
# 값은 전사에 있는 것만 — 100기가와트, 기가와트당 150억~200억 달러, 10배·100배, 인원 100명 대 1만~2만.

MTX = '2026-04-09-matx-reiner-pope'


def _mtx_split():
    parts, y_end = table(
        [[['HBM 에'], ['엔비디아 · 구글', '· 아마존'], ['많이 담는다']],
         [['SRAM 에'], ['Cerebras', '· Groq'], ['아주 빠르다']],
         [['둘을 합친다'], ['MatX'], ['균형이 어렵다']]],
        ['fig-box', 'fig-stage', 'fig-box'], heads=['가중치 자리', '그렇게 한 곳', '그 성질'],
        y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '가중치를 HBM 에 두면 많이 담고 SRAM 에 두면 아주 빠른데 MatX 는 둘을 한 시스템에 합쳤다')


def _mtx_bandwidth():
    """HBM 이 낼 수 있는 통행량을 무엇이 쓰나. 기둥 둘, 나눠 쓰는 쪽과 통째 쓰는 쪽."""
    x0, x1, w = 110.0, 300.0, 110.0
    y0, h = 46.0, 190.0
    parts = ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
             % (x0 + w / 2, 30, '가중치가 HBM 에')]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
              % (x1 + w / 2, 30, '가중치가 SRAM 에')]
    parts += _rect(x0, y0, w, h * 0.6, 'fig-bad')
    parts += _rect(x0, y0 + h * 0.6, w, h * 0.4, 'fig-stage')
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
              % (x0 + w / 2, y0 + h * 0.3 + 6, '가중치')]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
              % (x0 + w / 2, y0 + h * 0.8 + 6, 'KV 캐시')]
    parts += _rect(x1, y0, w, h, 'fig-agent')
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
              % (x1 + w / 2, y0 + h / 2 + 6, 'KV 캐시')]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, y0 + h + 30, 'HBM 이 낼 수 있는 통행량')]
    parts += legend([('fig-bad', '토큰마다 되풀이되는 왕복')], y0 + h + 44)
    return svg(y0 + h + 74, parts,
               '가중치가 HBM 에 있으면 통행량의 대부분을 가중치 왕복이 잡아먹고 SRAM 에 올리면 그 통행이 통째로 사라진다')


def _mtx_loop():
    rows = [('① 지연이 짧아진다', ''), ('② 동시에 처리 중인 요청이 준다', ''),
            ('③ HBM 에 쌓이는 KV 캐시가 준다', ''), ('④ 그 자리를 문맥에 내준다', '')]
    w = w_of([r[0] for r in rows])
    parts, y, h = [], 34.0, 46.0
    for i, (t, _n) in enumerate(rows):
        cls = 'fig-agent' if i == len(rows) - 1 else 'fig-box'
        parts += box((W - w) / 2, y, w, h, [t], cls)
        if i < len(rows) - 1:
            parts += vline(W / 2, y + h + 2, y + h + 18)
        y += h + 20
    parts += legend([('fig-agent', '지연을 줄여 얻는 것')], y + 4)
    return svg(y + 30, parts,
               '지연이 짧아지면 동시 처리 요청이 줄고 KV 캐시가 차지하던 자리가 비어 같은 메모리로 더 긴 문맥을 담는다')


def _mtx_five():
    parts, y_end = table(
        [[['① HBM 대역폭'], ['엔비디아 수준에 맞춘다']],
         [['② HBM 용량'], ['엔비디아 수준에 맞춘다']],
         [['③ 행렬곱 처리량'], ['크게 앞선다']],
         [['④ SRAM 대역폭·용량'], ['크게 앞선다']],
         [['⑤ 인터커넥트'], ['크게 앞선다']]],
        ['fig-box', 'fig-stage'], heads=['칩을 재는 다섯 잣대', 'MatX 의 방침'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '다섯 잣대 전부에서 엔비디아 수준에 최소한 맞추고 행렬곱과 SRAM 과 인터커넥트 셋에서 크게 앞서는 것이 방침이다')


def _mtx_scale():
    parts = mid(30, 46, ['데이터센터 수요 — 수십 기가와트로'], 'fig-box')
    parts += vline(W / 2, 78, 96)
    parts += mid(98, 46, ['엔비디아 칩은 기가와트당 200억 달러 안팎'], 'fig-box')
    parts += vline(W / 2, 146, 164)
    parts += mid(166, 46, ['여기에 10배나 100배'], 'fig-agent')
    parts += mid(232, 46, ['MatX 는 100명 남짓, 상대는 1만~2만 명'], 'fig-stage')
    parts += legend([('fig-agent', '감당해야 할 규모')], 292)
    return svg(318, parts,
               '수십 기가와트 수요에 기가와트당 200억 달러 안팎을 곱하고 다시 10배나 100배를 곱한 규모를 100명 남짓이 감당해야 한다')


# ══ 인텔·일론·오픈AI (2026-04-07) 전략 판 ══════════════════════════════
# 값은 전사에 있는 것만 — 월 100만 장·10만 장, 2억 달러, 7만 명, 1억~3억 달러.

IEO = '2026-04-07-intel-elon-openai'


def _ieo_wafer():
    """웨이퍼 투입 목표 둘. 나란한 세로 막대, 높이는 값의 비율이다."""
    base, top = 250.0, 40.0
    bw = 96.0
    xs = [140.0, 290.0]
    vals = [('시제품 공장', '월 10만 장', 10.0), ('장기 목표', '월 100만 장', 100.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 100.0
        cls = 'fig-agent' if v == 10.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(110, 420, base)
    parts += legend([('fig-agent', '오스틴 기가사이트에 세운다')], base + 40)
    return svg(base + 70, parts,
               '장기 목표가 월 100만 장 웨이퍼 투입이고 오스틴에 세울 시제품 공장은 그 십분의 일인 월 10만 장이다')


def _ieo_reunite():
    parts = mid(30, 46, ['한 집에서 설계와 제조를 같이 했다'], 'fig-box')
    parts += vline(W / 2, 78, 96)
    parts += mid(98, 46, ['갈라졌다 — 고정비를 설계사 수백 곳이 나눠 낸다'], 'fig-box')
    parts += vline(W / 2, 146, 170)
    parts += head(0, 192, W, '되돌리려면 둘 중 하나가 참이어야 한다')
    items = [(['① 한 고객이', '고정비를 다 채운다'], 'fig-agent'),
             (['② 제조에서', '비용 구조가 풀린다'], 'fig-agent')]
    wsum = sum(w_of(l) for l, _ in items) + 16
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 204, items, gap=16, h=2 * LH + 26)
    parts += row
    y = 204 + hh
    parts += mid(y + 22, 46, ['②는 EUV 지출이 막고 있다'], 'fig-bad')
    y2 = y + 22 + 46
    parts += legend([('fig-bad', '이 회차가 셈이 안 맞는다고 본 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '설계와 제조가 갈라진 이유가 고정비인데 되돌리려면 한 고객이 그 고정비를 채우거나 제조 비용 구조가 풀려야 한다')


def _ieo_scope():
    row, _x = eband([(['칩'], 'fig-box'), ('>', ''),
                     (['패키징'], 'fig-box'), ('>', ''),
                     (['부품 조립'], 'fig-outside'), ('>', ''),
                     (['기판'], 'fig-outside')], 40, LH + 26)
    parts = list(row)
    y = 40 + LH + 26
    parts += mid(y + 26, 46, ['어디서 멈추는지를 안 밝혔다'], 'fig-bad')
    y2 = y + 26 + 46
    parts += legend([('fig-outside', '이 회차가 물었는데 답이 없는 구간')], y2 + 16)
    return svg(y2 + 42, parts,
               '칩과 패키징까지는 하겠다고 했는데 부품 조립과 기판을 직접 하는지는 물음만 남고 답이 없었다')


def _ieo_audience():
    parts, y_end = table(
        [[['조 로건'], ['수백만~수억 명'], ['2억 달러']],
         [['TBPN'], ['7만 명'], ['1억~3억 달러']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['누구', '청중', '치른 금액'], y0=36, arrows=False)
    parts += mid(y_end + 22, 46, ['청중은 세 자릿수 차이, 금액은 같은 자릿수'], 'fig-box')
    return svg(y_end + 22 + 46 + 16, parts,
               '청중 수는 세 자릿수가 다른데 치른 금액은 같은 자릿수다')


def _ieo_three():
    parts, y_end = table(
        [[['인텔'], ['자기 이름을 공개적으로', '불러 줄 고객']],
         [['OpenAI'], ['결정권 쥔 7만 명 앞에서', '말하는 자리']],
         [['시트리니'], ['아무도 못 본 것을', '말할 자격']]],
        ['fig-stage', 'fig-agent'], heads=['누가', '무엇을 샀나'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '셋이 큰 금액을 치르고 산 것은 정보 자체가 아니라 남이 대신 못 하는 말을 할 수 있는 자리다')


# ══ 엔비디아·마벨·메모리 (2026-04-03) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 웨이퍼 3배·4배, 3~5년, 184억·112억·142억·30억 달러.

NVM = '2026-04-03-nvidia-marvell-memory'


def _nvm_nvlink():
    """NVLink 는 프로토콜이고 그 아래 매체만 갈아 끼운다."""
    parts = mid(30, 46, ['NVLink — 프로토콜'], 'fig-agent')
    items = [(['구리 배선', '+ SerDes'], 'fig-box'), (['빛', '이론적으로'], 'fig-outside')]
    wsum = sum(w_of(l) for l, _ in items) + 24
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 130, items, gap=24, h=2 * LH + 26)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, 78, 128)
    y = 130 + hh
    parts += legend([('fig-outside', '아직 안 된 자리')], y + 16)
    return svg(y + 42, parts,
               '지금 NVLink 는 구리 위에서 SerDes 가 비트를 실어 보내는데 매체가 빛이어도 안 될 이유가 없다')


def _nvm_support():
    parts, y_end = table(
        [[['마벨'], ['NVLink', 'UALink'], ['어느 쪽을 골라도', '받는다']],
         [['브로드컴'], ['UALink', 'ESUN'], ['NVLink 가 없다']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['누가', '지원 규격', '그래서'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '마벨은 NVLink 와 UALink 를 둘 다 지원해 고객이 어느 생태계를 고르든 받고 브로드컴에는 NVLink 가 없다')


def _nvm_hbm():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '예전 DRAM 라인') + head(R, 22, 248, 'HBM 으로 바꾼 라인')
    parts += box(L + 4, 38, 240, 3 * LH + 26, ['LPDDR', 'GDDR', '표준 DDR'], 'fig-box')
    parts += box(R + 4, 38, 240, 3 * LH + 26, ['TSV 둘레 여백', '여러 장 쌓기', '검사 공정 추가'], 'fig-agent')
    y = 38 + 3 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['같은 웨이퍼 공급', '서로 바꿔 쓴다'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['같은 비트에', '웨이퍼 3배, 앞으로 4배'], 'fig-bad')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['한번 바꾸면 안 돌아온다'], 'fig-bad')
    y3 = y2 + 24 + 46
    parts += legend([('fig-bad', '되돌릴 수 없게 만드는 자리')], y3 + 16)
    return svg(y3 + 42, parts,
               '예전 라인은 폰과 GPU 와 PC 용 메모리를 서로 바꿔 쓸 수 있었는데 HBM 은 같은 비트에 웨이퍼가 3배 들고 되돌아오지 않는다')


def _nvm_contract():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '클라우드 시대') + head(R, 22, 248, '지금')
    parts += box(L + 4, 38, 240, LH + 26, ['분기나 연 단위'], 'fig-box')
    parts += box(R + 4, 38, 240, LH + 26, ['3~5년'], 'fig-agent')
    y = 38 + LH + 26
    parts += box(L + 4, y + 20, 240, 2 * LH + 26, ['누가 발을 빼면', '거기서 사이클이 끝'], 'fig-box')
    parts += box(R + 4, y + 20, 240, 2 * LH + 26, ['공급사가 하단을 못 박는', '최저가 조항'], 'fig-agent')
    y2 = y + 20 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['줄에서 밀리면 HBM 배정이 경쟁사로'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-agent', '이번 사이클이 다르다면 그 근거')], y3 + 16)
    return svg(y3 + 42, parts,
               '분기나 연 단위였던 메모리 계약이 3~5년으로 길어지고 공급사가 하단을 못 박는 최저가 조항이 들어간다')


def _nvm_fab():
    row, _x = eband([(['짓는 데', '184억 달러'], 'fig-box'), ('>', '1년 뒤'),
                     (['지분 49%', '112억 달러에'], 'fig-box'), ('>', '2년 뒤'),
                     (['되사는 데', '142억 달러'], 'fig-agent')], 40, 2 * LH + 26)
    parts = list(row)
    y = 40 + 2 * LH + 26
    parts += mid(y + 26, 46, ['아폴로가 2년에 남긴 차익 30억 달러'], 'fig-stage')
    y2 = y + 26 + 46
    parts += legend([('fig-agent', '이번에 도로 사 온 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '184억 달러를 들여 지은 팹의 지분 49%를 112억 달러에 넘겼다가 2년 뒤 142억 달러에 되사면서 차익 30억 달러를 남겨 줬다')


# ══ Arm·터보퀀트 (2026-03-27) 전략 판 ═══════════════════════════════════
# 값은 전사에 있는 것만 — 16자리→3자리, 코어 3천만·1억2천만, 트레이 42·CPU 8·코어 4만5천,
# 코어 136개·CPU 330개·60개, 5%·10%·50%, 98~99%.

ARM = '2026-03-27-arm-cpu-turboquant'


def _arm_quant():
    row, _x = eband([(['① 무작위 행렬'], 'fig-box'), ('>', ''),
                     (['② 거리와 각도'], 'fig-box'), ('>', ''),
                     (['③ QJL 변환'], 'fig-agent')], 40, LH + 26)
    parts = list(row)
    y = 40 + LH + 26
    L, R = 60.0, 300.0
    parts += box(L, y + 30, 160, 2 * LH + 26, ['원래', '16자리'], 'fig-box')
    parts += box(R, y + 30, 160, 2 * LH + 26, ['줄인 뒤', '3자리'], 'fig-agent')
    parts += hline(L + 164, R - 4, y + 30 + LH + 13)
    y2 = y + 30 + 2 * LH + 26
    parts += legend([('fig-agent', '이 논문이 새로 얹은 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '무작위 행렬로 큰 값을 펴고 좌표를 거리와 각도로 바꾼 뒤 QJL 변환을 거치면 16자리로 적던 것이 3자리가 된다')


def _arm_slack():
    parts = mid(30, 46, ['KV 캐시를 6배 줄여 생긴 여유'], 'fig-agent')
    items = [(['① 컨텍스트를', '늘린다'], 'fig-box'),
             (['② 같은 설비로', '사용자를 더'], 'fig-box'),
             (['③ 노트북·엣지로', '내린다'], 'fig-box')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 10
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 130, items, gap=10, h=2 * LH + 26)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, 78, 128)
    y = 130 + hh
    parts += mid(y + 24, 46, ['셋 다 메모리를 덜 사는 데로 안 간다'], 'fig-bad')
    y2 = y + 24 + 46
    parts += legend([('fig-bad', '절감으로 안 가는 이유')], y2 + 16)
    return svg(y2 + 42, parts,
               '캐시를 줄여 생긴 여유는 컨텍스트와 동시 사용자와 엣지로 흘러가고 메모리를 덜 사는 결과에는 닿지 않는다')


def _arm_cores():
    """기가와트당 코어 수. 나란한 세로 막대, 높이는 값의 비율이다."""
    base, top = 250.0, 40.0
    bw = 96.0
    xs = [140.0, 290.0]
    vals = [('에이전틱 AI 이전', '3천만', 30.0), ('이후', '1억2천만', 120.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 120.0
        cls = 'fig-agent' if v == 120.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(110, 420, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, '같은 전력 안에서 기가와트당 CPU 코어')]
    parts += legend([('fig-agent', 'Arm 이 든 수')], base + 70)
    return svg(base + 100, parts,
               '같은 전력 안에서 필요한 기가와트당 CPU 코어가 3천만 개에서 1억2천만 개로 네 배가 된다는 주장이다')


def _arm_rack():
    parts, y_end = table(
        [[['랙 하나'], ['트레이 42개 × CPU 8개']],
         [['코어'], ['4만5천 개쯤']],
         [['칩 하나'], ['Neoverse V3 코어 136개']],
         [['그래서 CPU'], ['액체냉각 330개 · 공기냉각 60개']]],
        ['fig-stage', 'fig-box'], heads=['무엇을', '얼마나'], y0=36)
    return svg(y_end + 12, parts,
               '트레이 42개에 CPU 를 여덟 개씩 얹어 코어가 4만5천 개쯤 되고 칩 하나가 136코어이니 CPU 는 330개다')


def _arm_take():
    """같은 매출에서 Arm 이 가져가는 금액. 나란한 세로 막대 셋."""
    base, top = 250.0, 40.0
    bw = 86.0
    xs = [80.0, 220.0, 360.0]
    vals = [('IP 만', '5%', 5.0), ('CSS 까지', '10%', 10.0), ('직접 만들어 팔면', '50%', 50.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 50.0
        cls = 'fig-agent' if v == 50.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(60, 470, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, 'CPU 가 10억 달러어치 팔릴 때')]
    parts += legend([('fig-agent', '이번에 고른 길')], base + 70)
    return svg(base + 100, parts,
               'CPU 가 10억 달러어치 팔릴 때 IP 만 빌려주면 5%, CSS 까지 얹으면 10%, 직접 만들어 팔면 50%를 가져간다')


# ══ 마이크로LED·마이크론 (2026-03-20) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 구리 1~1.5m·400G/레인·800G, 마이크로LED 10~30m,
# 채널당 200Gbps 대 2Gbps, 이미징 파이버 천 가닥, 델 서버 12만 달러·768GB.

MLD = '2026-03-20-microled-micron'


def _mld_reach():
    """거리축 하나. 구리가 멈추는 자리와 마이크로LED 진영이 주장하는 자리."""
    y = 120.0
    x0, x1 = 40.0, 480.0
    parts = ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw"/>' % (x0, y, x1, y)]
    marks = [(x0, '0'), (x0 + 44, '1m 남짓'), (x0 + 180, '10m'), (x1, '30m')]
    for x, lab in marks:
        parts += ['  <line x1="%g" y1="%g" x2="%g" y2="%g" class="fig-arw" marker-end="none"/>'
                  % (x, y - 8, x, y + 8)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>' % (x, y + 28, lab)]
    parts += box(x0, y - 92, 160, 2 * LH + 26, ['구리 400G/레인', '800G 면 끝'], 'fig-bad')
    parts += box(x0 + 180, y - 92, 300, 2 * LH + 26, ['마이크로LED 진영이', '주장하는 거리'], 'fig-agent')
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % ((x0 + 44 + x0 + 180) / 2, y + 56, '① 비어 있는 구간')]
    parts += legend([('fig-bad', '신호가 멈추는 자리'), ('fig-agent', '업체 주장')], y + 76)
    return svg(y + 106, parts,
               '레인당 400기가비트에서 구리는 1~1.5미터에서 멈추고 800기가비트면 끝인데 마이크로LED 진영은 10미터에서 30미터를 주장한다')


def _mld_wide():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '빠르고 좁게') + head(R, 22, 248, '느리고 넓게')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['인듐인화물 레이저', '채널당 200Gbps'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['마이크로LED', '채널당 2Gbps'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, LH + 26, ['채널 하나'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['이미징 파이버', '한 다발에 천 가닥쯤'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['지나가는 사람 수는 비슷해진다'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-agent', '이 회차가 살펴본 쪽')], y3 + 16)
    return svg(y3 + 42, parts,
               '채널 하나가 100배 느려도 한 다발에 천 가닥을 넣으면 지나가는 총량은 비슷해진다는 접근이다')


def _mld_cands():
    parts, y_end = table(
        [[['구리 AEC'], ['1m 남짓'], ['400G/레인까지']],
         [['마이크로LED'], ['10~30m'], ['업체 주장']],
         [['VCSEL'], ['전사에 없음'], ['라이다에 이미 수십억 개']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['후보', '닿는 거리', '지금 서 있는 자리'],
        y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '구리와 마이크로LED 와 VCSEL 이 스케일업 자리를 놓고 서 있는데 닿는 거리가 전사에 나온 것은 앞의 둘뿐이다')


def _mld_base():
    """HBM 스택 단면. 위에 D램 다이 여럿, 맨 아래 베이스 다이."""
    x0, w = 130.0, 260.0
    parts = []
    y = 40.0
    for i in range(4):
        parts += box(x0, y, w, 34, ['D램 다이'], 'fig-box')
        y += 38
    parts += box(x0, y + 6, w, 46, ['베이스 다이 — 메모리 공정'], 'fig-agent')
    y2 = y + 6 + 46
    parts += hline(x0 + w, x0 + w + 30, y2 - 23)
    parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>' % (x0 + w + 38, y2 - 18, '①')]
    parts += mid(y2 + 24, 2 * LH + 26, ['① 1알파·1베타·1감마 체계', '키 큰 커패시터를 세우는 공정'], 'fig-stage')
    y3 = y2 + 24 + 2 * LH + 26
    parts += mid(y3 + 20, 46, ['② 열 개 중 몇 개가 그 속도를 내나'], 'fig-bad')
    y4 = y3 + 20 + 46
    parts += legend([('fig-bad', '속도에서 수율로 옮겨 간 물음')], y4 + 16)
    return svg(y4 + 42, parts,
               'HBM 스택 맨 아래 베이스 다이를 메모리 공정으로 만들었다는 대목이 의심의 뿌리이고 물음은 속도에서 수율로 옮겨 간다')


def _mld_token():
    parts = mid(30, 46, ['토큰을 어떻게 얻나'], 'fig-box')
    items = [(['직원마다', '토큰을 사 준다'], 'fig-box'),
             (['기계를 산다', '델 서버 12만 달러'], 'fig-box')]
    wsum = sum(w_of(l) for l, _ in items) + 24
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 130, items, gap=24, h=2 * LH + 26)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, 78, 128)
    y = 130 + hh
    parts += mid(y + 30, 2 * LH + 26, ['어느 쪽이든 초당 토큰 수는 정해져 있다', 'EDA 라이선스처럼 나눠 쓴다'], 'fig-agent')
    for cx, _w in cs:
        parts += vline(cx, y + 2, y + 28)
    y2 = y + 30 + 2 * LH + 26
    parts += legend([('fig-agent', '이 회차가 가장 값있게 본 반론')], y2 + 16)
    return svg(y2 + 42, parts,
               '직원마다 토큰을 사 주든 기계를 사서 사내에 두든 초당 만들 수 있는 토큰 수는 정해져 있어 결국 나눠 쓰게 된다')


# ══ 엔비디아 GTC 키노트 (2026-03-17) 전략 판 ════════════════════════════
# 값은 전사에 있는 것만 — 백만 토큰당 3달러, 칩 576개·랙 12개, 88코어·176스레드,
# 512스레드, 576-GPU 도메인·144-GPU 캐니스터, 52층, 60%, 연 500만 달러.

GTC = '2026-03-17-nvidia-gtc-keynote'


def _gtc_tiers():
    parts, y_end = table(
        [[['① 무료'], ['처리량 높고', '속도 낮다'], ['Qwen 3', '짧은 컨텍스트']],
         [['② 중간'], ['조금 더 크고', '빠르다'], ['백만 토큰당', '3달러']],
         [['③ 프리미엄'], ['가장 빠르다'], ['전사에 없음']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['등급', '곡선에서', '붙은 조건'],
        y0=36, arrows=False)
    parts += mid(y_end + 22, 46, ['같은 곡선 · 같은 전력'], 'fig-box')
    return svg(y_end + 22 + 46 + 16, parts,
               '처리량과 토큰 속도를 두 축으로 놓고 전력을 같게 맞춘 곡선 하나를 세 칸으로 잘랐다')


def _gtc_split():
    row, _x = eband([(['Vera', 'Rubin', 'HBM'], 'fig-box'), ('>', ''),
                     (['Groq 랙', 'SRAM', ''], 'fig-agent'), ('>', ''),
                     (['토큰', '', ''], 'fig-box')], 44, 3 * LH + 26, w=148, min_gap=14)
    parts = list(row)
    y = 44 + 3 * LH + 26
    parts += head(0, 34, 148, '사전연산·캐시')
    parts += head(186, 34, 148, '순차 피드포워드')
    parts += mid(y + 26, 46, ['이더넷으로 붙이고 지연 절반 모드'], 'fig-stage')
    y2 = y + 26 + 46
    parts += legend([('fig-agent', '남의 칩이 들어온 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '사전연산과 KV 캐시와 어텐션은 HBM 이 많은 랙이 맡고 활성값만 넘겨 순차 피드포워드를 시킨 뒤 토큰을 뽑는다')


def _gtc_racks():
    parts, y_end = table(
        [[['GPU 랙'], ['GPU +', '헤드노드 CPU'], ['GPU 에', '데이터를 먹인다']],
         [['Vera CPU 랙'], ['CPU 만'], ['툴 호출과', '오케스트레이션']],
         [['Groq LP 랙'], ['SRAM'], ['해독 전담']],
         [['STX 랙'], ['BlueField 4'], ['저장장치']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['랙', '무엇이', '하는 일'],
        y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '데이터센터 한 벌이 GPU 랙과 CPU 전용 랙과 해독 전담 랙과 저장 랙으로 나뉜다')


def _gtc_domain():
    parts = head(0, 30, W, '같은 스케일업 도메인 — GPU 576개')
    items = [(['캐니스터', 'GPU 144'], 'fig-box')] * 4
    wsum = sum(w_of(l) for l, _ in items) + 3 * 10
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 42, items, gap=10, h=2 * LH + 26)
    parts += row
    for i in range(len(cs) - 1):
        cx, w = cs[i]
        parts += hline(cx + w / 2 + 2, cs[i + 1][0] - cs[i + 1][1] / 2 - 2, 42 + hh / 2)
    y = 42 + hh
    parts += box(60, y + 26, 180, 2 * LH + 26, ['캐니스터 안', '구리 52층 PCB'], 'fig-box')
    parts += box(280, y + 26, 180, 2 * LH + 26, ['캐니스터 사이', '빛, 방식은 모름'], 'fig-bad')
    y2 = y + 26 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['랙이 달라도 스케일아웃이 아니다'], 'fig-agent')
    y3 = y2 + 24 + 46
    parts += legend([('fig-bad', '이 회차가 답을 못 낸 자리')], y3 + 16)
    return svg(y3 + 42, parts,
               '캐니스터 넷을 빛으로 묶어 GPU 576개가 한 도메인이 되는데 캐니스터 안은 구리이고 사이가 어느 방식인지는 안 밝혀졌다')


def _gtc_customers():
    parts = mid(30, 46, ['엔비디아 고객'], 'fig-box')
    parts += box(20, 130, 240, 3 * LH + 26,
                 ['60% — CSP 와', '하이퍼스케일러', '추론 컴퓨트만큼 번다'], 'fig-agent')
    parts += box(280, 130, 220, 3 * LH + 26,
                 ['나머지 — 일반 기업', '트랙터도 커피도', '판다'], 'fig-box')
    parts += vline(140, 78, 128)
    parts += vline(390, 78, 128)
    y = 130 + 3 * LH + 26
    parts += box(280, y + 22, 220, 2 * LH + 26, ['연 500만 달러를', '어떻게 나눠 쓰나'], 'fig-bad')
    parts += vline(390, y + 2, y + 20)
    y2 = y + 22 + 2 * LH + 26
    parts += legend([('fig-bad', '답이 안 나온 쪽')], y2 + 16)
    return svg(y2 + 42, parts,
               '고객의 60%에는 추론 컴퓨트만큼 번다는 셈이 맞지만 나머지에게는 연 500만 달러를 어떻게 나눠 쓰느냐가 남는다')


# ══ 광학과 구리의 갈림길 (2026-03-06) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 20억 달러 둘, GPU 72·144·576, 구리 3~7m, 7m→5m,
# 랙 8피트, 1.6T 2028~2029, 3.2T 2030, ALC FY2028, 2032.

OPX = '2026-03-06-optics-copper-crossroads'


def _opx_week():
    row, _x = eband([(['월요일', '엔비디아'], 'fig-box'), ('>', ''),
                     (['수요일 밤', '브로드컴'], 'fig-agent'), ('>', ''),
                     (['그날 시간외'], 'fig-box')], 40, 2 * LH + 26, w=150, min_gap=20)
    parts = list(row)
    y = 40 + 2 * LH + 26
    notes = [['루멘텀·코히런트', '각각 20억 달러'], ['200기가는 구리', '400기가도 된다'],
             ['크레도 오르고', '옵틱스 둘 내림']]
    y2 = y + 34
    xs = [0.0, 185.0, 370.0]
    for x, nt in zip(xs, notes):
        parts += box(x, y2, 150, 2 * LH + 26, nt, 'fig-stage')
        parts += vline(x + 75, y + 2, y2 - 2)
    y3 = y2 + 2 * LH + 26
    parts += legend([('fig-agent', '판을 뒤집은 발언')], y3 + 16)
    return svg(y3 + 42, parts,
               '월요일에 옵틱스 쪽으로 40억 달러가 얹혔는데 수요일 밤 실적발표에서 구리로도 된다는 말이 나오자 그날 시간외에서 값이 뒤집혔다')


def _opx_reach():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '예전 랙') + head(R, 22, 248, '지금 랙')
    parts += box(L + 4, 38, 240, LH + 26, ['GPU 72개'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['GPU 144개', '어쩌면 576개'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['GPU 와 스위치가', '멀다'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['가까워진다'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['구리가 닿는 3~7미터 안으로 들어온다'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-agent', '밀집이 만든 것')], y3 + 16)
    return svg(y3 + 42, parts,
               '밀집이 구리의 사거리를 늘려 준 것이 아니라 필요한 사거리를 줄여 배치가 구리 안으로 걸어 들어왔다')


def _opx_cable():
    """속도가 오르면 케이블이 닿는 거리가 준다. 나란한 세로 막대 둘."""
    base, top = 240.0, 60.0
    bw = 96.0
    xs = [140.0, 290.0]
    vals = [('100기가', '7미터', 7.0), ('200기가', '5미터', 5.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 7.0
        cls = 'fig-agent' if v == 5.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(110, 420, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, '랙 높이는 8피트쯤 — 5미터면 덮는다')]
    parts += legend([('fig-agent', '지금 세대')], base + 70)
    return svg(base + 100, parts,
               '속도를 200기가로 올리면 케이블이 닿는 거리가 7미터에서 5미터로 주는데 랙 하나를 덮기에는 아직 넉넉하다')


def _opx_options():
    parts = mid(30, 46, ['엔비디아가 40억 달러로 산 것'], 'fig-agent')
    items = [(['CW 레이저', '3인치 · 6인치'], 'fig-box'),
             (['OCS — 거울', 'R300'], 'fig-box'),
             (['OCS — 액정', '움직이는 부품 없음'], 'fig-box')]
    wsum = sum(w_of(l) for l, _ in items) + 2 * 10
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 130, items, gap=10, h=2 * LH + 26)
    parts += row
    for cx, _w in cs:
        parts += vline(cx, 78, 128)
    y = 130 + hh
    parts += mid(y + 24, 46, ['다년 · 비독점 — 하나든 둘이든 고를 수 있다'], 'fig-stage')
    y2 = y + 24 + 46
    parts += legend([('fig-agent', '표가 아니라 선택권')], y2 + 16)
    return svg(y2 + 42, parts,
               '두 계약은 다년이고 비독점이라 어느 갈래든 나중에 고를 수 있게 자리를 잡아 둔 것이다')


def _opx_timing():
    parts = head(0, 30, W, 'CPO 가 언제 오느냐가 중간에 낀 기술의 운명을 정한다')
    L, R = 0.0, 272.0
    parts += box(L + 4, 46, 240, 2 * LH + 26, ['CPO 가 먼저 오면', 'ALC 는 설 자리가 없다'], 'fig-bad')
    parts += box(R + 4, 46, 240, 2 * LH + 26, ['ALC 가 먼저 오면', '로우 하나를 잇는다'], 'fig-agent')
    y = 46 + 2 * LH + 26
    parts += mid(y + 24, 2 * LH + 26, ['ALC 는 2028회계연도쯤', '3.2테라비트가 구리면 CPO 는 2032년까지'], 'fig-stage')
    y2 = y + 24 + 2 * LH + 26
    parts += legend([('fig-bad', '중간에 낀 기술이 죽는 쪽')], y2 + 16)
    return svg(y2 + 42, parts,
               'ALC 는 2028회계연도쯤 나올 것 같은데 그 전에 CPO 가 오면 꽂아 쓰는 자리가 없어져 존재 이유가 사라진다')


# ══ 메타 MTIA·AAOI (2026-03-13) 전략 판 ═════════════════════════════════
# 값은 전사에 있는 것만 — MTIA300 컴퓨트 1 + 네트워크 2, MTIA500 컴퓨트 4,
# HBM 400~500GB, 800W, 초당 200GB, 16노드 → 72노드, 35억 명, 상위 두 고객 75%·80%.

MTA = '2026-03-13-meta-mtia-aaoi'


def _mta_chiplet():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, 'MTIA300') + head(R, 22, 248, 'MTIA500')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['컴퓨트 칩 1', '네트워크 칩 2'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['컴퓨트 칩 4', '2 × 2 로'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['HBM'], 'fig-stage')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['HBM', '400~500기가바이트'], 'fig-stage')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 2 * LH + 26, ['같은 블록을 다시 집는다', '다이 접점은 한 곳에서 최소 세 곳으로'], 'fig-box')
    y3 = y2 + 24 + 2 * LH + 26
    parts += legend([('fig-agent', '이번에 늘어난 자리')], y3 + 16)
    return svg(y3 + 42, parts,
               '세대가 바뀔 때 새로 만드는 것이 아니라 같은 블록의 조합을 바꾸는데 다이 접점은 한 곳에서 최소 세 곳으로 는다')


def _mta_pipeline():
    row, _x = eband([(['① 검색', 'Andromeda'], 'fig-box'), ('>', ''),
                     (['② 순위', 'Lattice'], 'fig-box'), ('>', ''),
                     (['③ 추천 모델', 'Gem'], 'fig-agent')], 44, 2 * LH + 26, w=148, min_gap=14)
    parts = list(row)
    y = 44 + 2 * LH + 26
    notes = [['후보 수천 개', '여러 벤더에서'], ['어느 하드웨어인지', '못 찾았다'], ['35억 명에게는', '너무 비싸다']]
    y2 = y + 30
    xs = [0.0, 186.0, 372.0]
    for x, nt in zip(xs, notes):
        parts += box(x, y2, 148, 2 * LH + 26, nt, 'fig-stage')
        parts += vline(x + 74, y + 2, y2 - 2)
    y3 = y2 + 2 * LH + 26
    parts += mid(y3 + 22, 46, ['교사에서 작은 모델로 옮겨 담아 서비스에 올린다'], 'fig-box')
    y4 = y3 + 22 + 46
    parts += legend([('fig-agent', '컴퓨트를 넣으면 좋아지는 첫 추천 모델')], y4 + 16)
    return svg(y4 + 42, parts,
               '방대한 광고에서 후보를 골라내고 순위를 정한 뒤 추천 파운데이션 모델을 증류해 서비스에 올린다')


def _mta_spec():
    parts, y_end = table(
        [[['HBM 용량'], ['크게 늘렸다']],
         [['저정밀 연산'], ['많이 넣었다']],
         [['스케일아웃 망'], ['오히려 줄였다']],
         [['스케일업 도메인'], ['16노드 → 72노드']]],
        ['fig-box', 'fig-agent'], heads=['항목', '400·450·500 세대'], y0=36, arrows=False)
    parts += mid(y_end + 22, 46, ['추론에 맞춘 결정이 사양에 남았다'], 'fig-stage')
    return svg(y_end + 22 + 46 + 16, parts,
               'HBM 을 늘리고 스케일아웃을 줄이며 스케일업 도메인을 16노드에서 72노드로 키운 것이 추론 쪽 결정이다')


def _mta_workload():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, 'LLM 디코드') + head(R, 22, 248, '메타의 추천')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['가중치 전체를', '순서대로 훑는다'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['거대한 임베딩 테이블을', '사람마다 다르게 뒤진다'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, LH + 26, ['연산이 많이 든다'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['메모리 접근과', '용량에 매인다'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 2 * LH + 26, ['그래서 800와트급에', '스케일아웃 초당 200기가바이트'], 'fig-stage')
    y3 = y2 + 24 + 2 * LH + 26
    parts += legend([('fig-agent', 'MTIA 가 겨눈 모양')], y3 + 16)
    return svg(y3 + 42, parts,
               '가중치를 순서대로 훑는 LLM 과 달리 임베딩 테이블을 사람마다 다르게 뒤지는 일이라 메모리 접근과 용량에 매인다')


def _mta_2017():
    parts, y_end = table(
        [[['주가'], ['12달러', '→ 105달러'], ['10달러대', '→ 100달러대']],
         [['상위 두 고객'], ['75%'], ['80%대']],
         [['앵커 고객'], ['Amazon'], ['Amazon']],
         [['서사'], ['수직계열화'], ['수직계열화']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['무엇', '2017년', '지금'], y0=36, arrows=False)
    parts += mid(y_end + 22, 46, ['그때는 수요가 한 분기 꺾이자 99%를 잃었다'], 'fig-bad')
    return svg(y_end + 22 + 46 + 16, parts,
               '주가대와 고객 집중도와 앵커 고객과 수직계열화 서사가 2017년과 거의 같은데 그때는 수요가 한 분기 꺾이자 99%를 잃었다')


# ══ 광학 공급망 (2026-02-28) 전략 판 ═════════════════════════════════════
# 값은 전사에 있는 것만 — AXT 점유율 60~70%·50~60%·스미토모 25~30%, 시총 10억·500억 달러,
# Tower 9억5천만 달러·5배·70%, 북투빌 4배, 조립 25년, 유리 100년, 웨이퍼 3인치·6인치.

OSC = '2026-02-28-optical-supply-chain'


def _osc_axt():
    parts = mid(30, 46, ['AXT — 미국 회사, 시가총액 10억 달러'], 'fig-box')
    parts += vline(W / 2, 78, 96)
    parts += mid(98, 46, ['기판 생산은 전량 베이징'], 'fig-bad')
    parts += vline(W / 2, 146, 164)
    parts += mid(166, 2 * LH + 26, ['중국이 미국으로 나가는 것을 막는 규제', '미국이 중국을 막는 규제가 아니다'], 'fig-bad')
    y = 166 + 2 * LH + 26
    parts += mid(y + 22, 46, ['허가가 늦어 매출이 실제로 깎였다'], 'fig-stage')
    y2 = y + 22 + 46
    parts += legend([('fig-bad', '규제 방향이 거꾸로 걸린 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '미국 회사인데 기판 생산이 전량 베이징에 있어 중국이 미국으로 내보내는 것을 막는 규제에 걸린다')


def _osc_reach():
    parts, y_end = table(
        [[['Coherent'], ['기판 · 레이저 칩', '· 트랜시버 모듈'], ['시가총액', '500억 달러']],
         [['Lumentum'], ['기판은 사 온다'], ['EML 점유율', '50~60%']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['누가', '자기 안의 범위', '숫자'], y0=36, arrows=False)
    parts += mid(y_end + 22, 2 * LH + 26,
                 ['Coherent 도 EML 은 Lumentum 에서 사 간다', '인텔이 자사 파운드리를 키우면서 CPU 를 TSMC 에 맡긴 것과 같다'], 'fig-box')
    return svg(y_end + 22 + 2 * LH + 26 + 16, parts,
               'Coherent 는 기판까지 자기 안에 두고 Lumentum 은 사 오는데 그 Coherent 도 EML 은 Lumentum 에서 사 간다')


def _osc_moat():
    parts, y_end = table(
        [[['AXT'], ['결정 성장'], ['수십 년']],
         [['Lumentum'], ['에피택시'], ['값 없음 — 상태만']],
         [['Fabrinet'], ['조립 · 패키징'], ['25년']],
         [['Corning'], ['유리'], ['100년']]],
        ['fig-stage', 'fig-box', 'fig-agent'], heads=['회사', '쌓은 것', '걸린 시간'], y0=36, arrows=False)
    return svg(y_end + 12, parts,
               '층마다 모트를 설명하는 말이 같다. 남이 따라오기까지 걸리는 시간으로만 설명된다')


def _osc_wafer():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '레이저 쪽') + head(R, 22, 248, '파운드리 쪽')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['3인치 → 6인치', '웨이퍼당 소자 4배 넘게'], 'fig-agent')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['200밀리 본딩 대', '300밀리 모놀리식'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['2026년 말 내부', '생산능력 절반을 6인치로'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['본딩 공정이 없으면', '전기광학 성능이 낫다'], 'fig-box')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['시간으로 쌓은 모트를 한 수가 갉는다'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-agent', '지름을 키우는 한 수')], y3 + 16)
    return svg(y3 + 42, parts,
               '웨이퍼 지름을 키우는 한 수가 레이저 쪽과 파운드리 쪽에서 각각 앞서 쌓아 둔 노하우를 갉는다')


def _osc_timing():
    parts = head(0, 30, W, '스케일업이 언제 광학으로 넘어가나')
    items = [(['2027~28년', '광학 쪽 사람들의 답'], 'fig-agent'),
             (['2030~31년', '구리 쪽 사람들의 답'], 'fig-box')]
    wsum = sum(w_of(l) for l, _ in items) + 24
    row, _x, cs, hh = panel_boxes((W - wsum) / 2, 44, items, gap=24, h=2 * LH + 26)
    parts += row
    y = 44 + hh
    parts += mid(y + 26, 2 * LH + 26, ['시점을 모르면 유리섬유 수요를 셈할 수 없다', '그래서 Corning 매수에도 단서가 붙는다'], 'fig-bad')
    for cx, _w in cs:
        parts += vline(cx, y + 2, y + 24)
    y2 = y + 26 + 2 * LH + 26
    parts += legend([('fig-bad', '답을 못 낸 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '같은 물음에 구리 쪽과 광학 쪽이 다른 해를 대고 두 사람은 답을 열어 둔 채 각자 파 볼 물음이라고 했다')


# ══ 광 네트워킹 슈퍼사이클 (2026-02-20) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 랙 안 GPU 72개·랙 3톤, 스케일아웃 100미터, DSP 20와트,
# 연속파 400밀리와트, 100기가 16개 대 200기가 8개, 3인치·12인치, 백로그 4억 달러.

OSU = '2026-02-20-optical-supercycle'


def _osu_layers():
    rows = [('스케일어크로스', '데이터센터끼리'),
            ('스케일아웃', '한 건물 안 여러 랙 — 100미터까지'),
            ('스케일업', '한 랙 안 GPU 72개')]
    lw = w_of([r[0] for r in rows])
    rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 34.0, 46.0
    for name, note in rows:
        parts += box(x0, y, lw, h, [name], 'fig-box')
        parts += box(x0 + lw + gap, y, rw, h, [note], 'fig-stage')
        y += h + 12
    parts += mid(y + 14, 46, ['셋 다 구리를 놓는데 이유가 각기 다르다'], 'fig-agent')
    y2 = y + 14 + 46
    return svg(y2 + 16, parts,
               '데이터센터끼리와 건물 안 여러 랙과 한 랙 안 GPU 가 각기 다른 이유로 구리를 놓는다')


def _osu_els():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '플러그형') + head(R, 22, 248, '떼어 놓은 구조')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['레이저가 모듈 안', '변조기도 모듈 안'], 'fig-box')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['레이저는 랙 연결 자리', '변조는 칩 위로'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['DSP 하나에만', '20와트'], 'fig-bad')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['연속파 400밀리와트', '데이터가 없는 빛'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['들어오는 빛은 그냥 켜져 있는 손전등'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-bad', '연산에 못 쓰이는 전력')], y3 + 16)
    return svg(y3 + 42, parts,
               '레이저를 모듈에서 떼어 랙 연결 자리로 옮기면 들어오는 빛에 데이터가 없고 변조는 칩 위로 올라간다')


def _osu_wafer():
    """웨이퍼 지름과 한 장에서 뽑는 칩. 나란한 세로 막대 둘."""
    base, top = 250.0, 50.0
    bw = 96.0
    xs = [140.0, 290.0]
    vals = [('인듐인화물', '3인치', 3.0), ('실리콘', '12인치', 12.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 12.0
        cls = 'fig-bad' if v == 3.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(110, 420, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, '지름 4배 · 한 장에서 뽑는 칩 최대 16배')]
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 76, '월 투입량은 수천~1만 장 대 수백만 장')]
    parts += legend([('fig-bad', '병목이 앉은 자리')], base + 94)
    return svg(base + 124, parts,
               '레이저가 올라가는 웨이퍼는 3인치이고 실리콘은 12인치라 지름이 4배, 한 장에서 뽑는 칩은 최대 16배 차이다')


def _osu_ocs():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '패킷 스위치') + head(R, 22, 248, '광회로 스위치')
    parts += box(L + 4, 38, 240, 3 * LH + 26, ['빛을 전기로', '어디로 보낼지 판단', '다시 빛으로'], 'fig-box')
    parts += box(R + 4, 38, 240, 3 * LH + 26, ['반사경으로', '방향만 돌린다', ''], 'fig-agent')
    y = 38 + 3 * LH + 26
    parts += mid(y + 24, 2 * LH + 26, ['훈련 작업은 배선이 잘 안 바뀐다', '설정해 두고 잊어버리는 방식이라 맞아떨어졌다'], 'fig-stage')
    y2 = y + 24 + 2 * LH + 26
    parts += legend([('fig-agent', '변환을 생략한 쪽')], y2 + 16)
    return svg(y2 + 42, parts,
               '패킷 스위치는 빛을 전기로 바꿔 판단하고 다시 빛으로 돌리는데 광회로 스위치는 반사경으로 방향만 돌린다')


def _osu_overlap():
    row, _x = eband([(['800기가', '오르는 중'], 'fig-box'), ('>', ''),
                     (['1.6테라', '2026년 어디쯤'], 'fig-agent')], 44, 2 * LH + 26)
    parts = list(row)
    y = 44 + 2 * LH + 26
    parts += mid(y + 26, 2 * LH + 26, ['갈아타는 것이 아니라 겹쳐서 팔린다',
                                       'TSMC 가 2나노를 올리면서 5나노에서도 버는 것과 같다'], 'fig-stage')
    y2 = y + 26 + 2 * LH + 26
    parts += legend([('fig-agent', '시점이 어림인 쪽')], y2 + 16)
    return svg(y2 + 42, parts,
               '새 세대가 올라오는 동안 앞 세대가 죽지 않고 함께 팔리는데 1.6테라 시작 시점은 어림으로만 말했다')


# ══ 메모리 대혼란·자본지출 (2026-02-13) 전략 판 ═══════════════════════════
# 값은 전사에 있는 것만 — 4사 합계 6천억 달러 초과, 구글 1,200억→1,800억,
# 아마존 1,250억→2,000억, 게이밍 35%→8%, 영업이익률 65%·40%, 낸드 1,152TB·13%,
# 마진 10~20%·30%·40~50%·70%.

MEM = '2026-02-13-memory-mayhem-capex'


def _mem_flow():
    rows = [('실적발표에서 계획을 발표한다', 'fig-box'),
            ('그 자리에서 부품 주문서가 된다', 'fig-box'),
            ('몇 분기 뒤 웨이퍼·D램·낸드 수요표로 내려온다', 'fig-agent')]
    w = w_of([r[0] for r in rows])
    parts, y, h = [], 34.0, 46.0
    for i, (t, cls) in enumerate(rows):
        parts += box((W - w) / 2, y, w, h, [t], cls)
        if i < len(rows) - 1:
            parts += vline(W / 2, y + h + 2, y + h + 18)
        y += h + 20
    parts += mid(y + 4, 46, ['4사 합계 6천억 달러 초과'], 'fig-stage')
    y2 = y + 4 + 46
    parts += legend([('fig-agent', '반도체가 실제로 받는 자리')], y2 + 16)
    return svg(y2 + 42, parts,
               '실적발표에서 발표된 계획 금액이 부품 주문서가 되고 몇 분기 뒤 웨이퍼와 D램과 낸드의 수요표로 내려온다')


def _mem_split():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '게이밍 GPU') + head(R, 22, 248, 'AI 칩')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['매출 비중', '35% → 8%'], 'fig-bad')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['영업이익률', '65%'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, 2 * LH + 26, ['영업이익률', '40%'], 'fig-box')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['HBM 을 만들 수 있는', '회사가 셋뿐'], 'fig-stage')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 46, ['같은 웨이퍼 생산 능력을 어디로 돌릴 것인가'], 'fig-stage')
    y3 = y2 + 24 + 46
    parts += legend([('fig-bad', '밀려나는 쪽')], y3 + 16)
    return svg(y3 + 42, parts,
               '게이밍은 매출 비중이 35%에서 8%로 내려왔고 이익률도 낮아 같은 웨이퍼를 AI 쪽으로 돌릴 유인이 크다')


def _mem_nand():
    parts = mid(30, 2 * LH + 26, ['스토리지 랙 한 대에', '낸드 1,152테라바이트'], 'fig-box')
    parts += vline(W / 2, 78 + LH, 104 + LH)
    parts += mid(106 + LH, 2 * LH + 26, ['2027년 루빈 랙 7만 대', '랙당 1,000테라바이트'], 'fig-box')
    y = 106 + LH + 2 * LH + 26
    parts += vline(W / 2, y + 2, y + 20)
    parts += mid(y + 22, 46, ['전 세계 낸드 공급의 13%'], 'fig-agent')
    y2 = y + 22 + 46
    parts += legend([('fig-agent', '한 제품군이 가져가는 몫')], y2 + 16)
    return svg(y2 + 42, parts,
               '스토리지 랙 한 대에 낸드가 1,152테라바이트 들어가고 2027년 루빈 랙 7만 대가 전 세계 낸드의 13%를 가져간다')


def _mem_margin():
    """빌려줄 때의 마진. 나란한 세로 막대 넷."""
    base, top = 250.0, 50.0
    bw = 76.0
    xs = [70.0, 180.0, 290.0, 400.0]
    vals = [('네오클라우드', '10~20%', 15.0), ('구글·MS', '30%', 30.0),
            ('자체 TPU', '40~50%', 45.0), ('구글 광고', '70%', 70.0)]
    parts = []
    for x, (name, lab, v) in zip(xs, vals):
        h = (base - top) * v / 70.0
        cls = 'fig-agent' if v == 70.0 else 'fig-box'
        parts += _rect(x, base - h, bw, h, cls)
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
                  % (x + bw / 2, base - h - 10, lab)]
        parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
                  % (x + bw / 2, base + 22, name)]
    parts += hline(50, 490, base)
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-e">%s</text>'
              % (W / 2, base + 52, '앞의 셋은 빌려줄 때, 맨 뒤는 본업')]
    parts += legend([('fig-agent', '회수 경로가 가장 짧은 자리')], base + 70)
    return svg(base + 100, parts,
               '같은 돈을 써도 빌려줄 때의 이익률이 층마다 다르고 본업인 광고의 이익률이 그보다 훨씬 높다')


# ══ AI 인프라 금융 (2026-02-10) 전략 판 ═══════════════════════════════════
# 값은 전사에 있는 것만 — 시간당 1.70~1.80·3~4·5~7달러, 선물 예시 2달러와 21~25달러,
# 전성기 2~3년·유효수명 5~10년, 취득가 3만 달러·보장 8천~1만 달러·15~30%, 72랙·4년.

FIN = '2026-02-10-financing-ai-infra'


def _fin_tiers():
    parts, y_end = table(
        [[['하이퍼스케일러'], ['AWS', 'GCP'], ['5~7달러']],
         [['뉴클라우드'], ['CoreWeave', 'Lambda'], ['3~4달러']],
         [['마켓플레이스'], ['—'], ['1.70달러 안팎'], ]],
        ['fig-box', 'fig-stage', 'fig-agent'], heads=['어디서', '누구', '시간당'],
        y0=36, arrows=False)
    parts += mid(y_end + 22, 46, ['지수가 보는 구간은 맨 아래층뿐'], 'fig-agent')
    return svg(y_end + 22 + 46 + 16, parts,
               '같은 H100 을 빌리는데 위아래가 세 배 넘게 벌어지고 지수는 맨 아래층만 본다')


def _fin_futures():
    rows = [('① 오늘', '2월물 선물을 2달러에 산다'),
            ('② 2월', '쓸 컴퓨트는 스팟에서 따로 산다'),
            ('③ 정산', '지수가 21~25달러면 그 차액이 현금으로')]
    lw = w_of([r[0] for r in rows])
    rw = w_of([r[1] for r in rows])
    gap = 12
    x0 = (W - (lw + gap + rw)) / 2
    parts, y, h = [], 34.0, 46.0
    for i, (name, note) in enumerate(rows):
        cls = 'fig-agent' if i == 2 else 'fig-box'
        parts += box(x0, y, lw, h, [name], 'fig-stage')
        parts += box(x0 + lw + gap, y, rw, h, [note], cls)
        if i < len(rows) - 1:
            parts += vline(x0 + lw / 2, y + h + 2, y + h + 16)
        y += h + 18
    parts += mid(y + 6, 2 * LH + 26, ['선물에서 GPU 시간이 나오지는 않는다', '지불액에 상한이 씌워질 뿐'], 'fig-box')
    y2 = y + 6 + 2 * LH + 26
    parts += legend([('fig-agent', '값은 예시 — 실제 시세가 아니다')], y2 + 16)
    return svg(y2 + 42, parts,
               '선물을 사 둬도 쓸 컴퓨트는 스팟에서 따로 사고 선물은 차액만 현금으로 정산해 지불액에 상한을 씌운다')


def _fin_depr():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '정액법으로 그리면') + head(R, 22, 248, '실제로 본 모양')
    parts += box(L + 4, 38, 240, 2 * LH + 26, ['해마다 같은 폭으로', '깎인다'], 'fig-bad')
    parts += box(R + 4, 38, 240, 2 * LH + 26, ['처음 3년에', '가치 대부분이 빠진다'], 'fig-agent')
    y = 38 + 2 * LH + 26
    parts += box(L + 4, y + 22, 240, LH + 26, ['끝에서 0'], 'fig-bad')
    parts += box(R + 4, y + 22, 240, 2 * LH + 26, ['남은 5~7년은', '평평하게 간다'], 'fig-agent')
    y2 = y + 22 + 2 * LH + 26
    parts += mid(y2 + 24, 2 * LH + 26, ['전성기 수명은 2~3년', '유효수명은 5~10년'], 'fig-stage')
    y3 = y2 + 24 + 2 * LH + 26
    parts += legend([('fig-bad', '가장 큰 실수라고 본 가정')], y3 + 16)
    return svg(y3 + 42, parts,
               '정액법은 해마다 같은 폭으로 깎아 끝에서 0 으로 보내는데 실제로는 처음 3년에 대부분 빠지고 나머지는 평평하다')


def _fin_residual():
    """칩 한 개 값에서 보장 구간이 차지하는 폭. 기둥 하나."""
    x0, w = 120.0, 120.0
    y0, h = 46.0, 200.0
    hb = h * 0.25
    parts = ['  <text x="%g" y="%g" text-anchor="middle" class="fig-hd">%s</text>'
             % (x0 + w / 2, 30, '칩 한 개 취득가 3만 달러')]
    parts += _rect(x0, y0, w, h - hb, 'fig-stage')
    parts += _rect(x0, y0 + h - hb, w, hb, 'fig-agent')
    parts += ['  <text x="%g" y="%g" text-anchor="middle" class="fig-b">%s</text>'
              % (x0 + w / 2, y0 + h - hb / 2 + 6, '8천~1만')]
    parts += hline(x0 + w, x0 + w + 30, y0 + h - hb / 2)
    parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>'
              % (x0 + w + 38, y0 + h - hb / 2 + 5, '보장 구간 — 잔존가치의 15~30%')]
    parts += hline(x0 + w, x0 + w + 30, y0 + (h - hb) / 2)
    parts += ['  <text x="%g" y="%g" class="fig-e">%s</text>'
              % (x0 + w + 38, y0 + (h - hb) / 2 + 5, '여기는 안 덮는다')]
    parts += legend([('fig-agent', '꼬리만 덮는 상품')], y0 + h + 24)
    return svg(y0 + h + 54, parts,
               '칩 한 개를 3만 달러에 샀다면 8천에서 1만 달러어치만 지켜 주는 구조이고 클러스터 전체에 보험이 걸리는 그림이 아니다')


FIGS = {
    (MEM, 'strategy'): [
        ('1.|진행자A는 그 돈이', '발표된 금액이 수요표로 내려오는 순서', _mem_flow(),
         '데이터센터 부지와 전력과 연산과 메모리와 네트워킹과 스토리지로 나뉜다(L143). '
         '회차 끝에서 이 붐을 「반도체라는 배를 전부 들어 올리는 밀물」이라고 불렀다(L327).'),
        ('2.|Nvidia 쪽 유인도', '같은 웨이퍼를 어디로 돌리나', _mem_split(),
         'HBM 은 만들기가 어려워 SK하이닉스·삼성·마이크론 세 곳만 만든다(L29). '
         '게이밍 비중과 두 이익률은 전사의 값이다(L31). 웨이퍼가 실제로 얼마나 옮겨 갔는지는 전사에 숫자가 없다.'),
        ('4.|낸드 쪽 숫자가', '루빈 하나가 가져가는 낸드', _mem_nand(),
         '랙 사양은 진행자V 가 전한 것이고 랙 대수와 비율은 모건스탠리 추정이다(L85·L87). '
         '출하 시점은 2027년이다.'),
        ('5.|같은 6천억', '빌려줄 때의 이익률과 본업의 이익률', _mem_margin(),
         '네오클라우드급과 구글·마이크로소프트급과 자체 TPU 는 GPU 를 빌려줄 때의 이익률이고(L155·L157), '
         '맨 뒤는 구글 광고 사업 자체의 이익률이다(L149·L169). 막대 높이는 값의 비율이다.'),
    ],
    (FIN, 'strategy'): [
        ('1.|진행자V는 숫자부터', '같은 칩인데 요금이 세 층', _fin_tiers(),
         '맨 아래층은 전사가 「1.70 180」으로 받아 적은 자리라 1.70에서 1.80달러 사이로 읽힌다(L71). '
         'Wayne 은 층이 갈리는 이유를 서비스 수준과 품질과 가동률이 제각각이라 표준화가 어려운 대목으로 봤다(L75). '
         '하이퍼스케일러는 분기에 한두 번만 요금을 고쳐 하루 단위 시장을 못 따라간다(L79).'),
        ('2.|금융 상품은 돈이', '선물 한 장에서 돈이 오가는 순서', _fin_futures(),
         '2달러와 21~25달러는 Wayne 이 「예를 들어」로 연 가정이다(L95·L97). '
         '요금이 그렇게까지 오르는 일은 「이상적으로는 결코 일어나지 않겠지만」이라는 단서도 함께 달았다(L99).'),
        ('4.|숫자로는 이렇다', '감가상각을 직선으로 그리면', _fin_depr(),
         '전성기 수명을 두고 통념대로 5년도 그럴듯하다고 먼저 여지를 두고 자신은 2~3년에 가깝다고 봤다(L143·L145). '
         '정액법을 두고는 「정확히 맞다고 생각하는 사람은 아무도 없을 것이라고 거의 확신한다」고 했다(L145·L147).'),
        ('5.|보장 범위는 전부가', '칩 한 개에서 덮는 구간', _fin_residual(),
         'Wayne 은 이것을 시장의 꼬리를 덮는 일이라고 했다(L197). 클러스터 전체에 보험이 걸리는 그림이 아니다. '
         '기둥을 나눈 비율은 잔존가치의 15~30% 라는 값에서 잡은 것이다.'),
    ],
    (OSC, 'strategy'): [
        ('2.|그런데 미국 회사인', '규제가 거꾸로 걸린 자리', _osc_axt(),
         '미국이 중국으로 나가는 것을 막는 규제가 아니라 중국이 미국으로 나가는 것을 막는 규제다(L65). '
         '최근 실적발표에서 처음으로 허가가 늦어져 매출이 깎였다(L65). 점유율은 두 사람이 각각 60~70%와 50~60%를 댔다(L61·L69).'),
        ('3.|Coherent는 시가총액', '공급망의 어디까지 자기 안인가', _osc_reach(),
         'Coherent 는 전기차용 실리콘카바이드와 산업용 레이저도 따로 한다(L225·L227). '
         '트랜시버 방식 셋 중 VCSEL 은 Lumentum 에 없다(L233·L249). 그러면서도 EML 은 Lumentum 에서 사 간다(L197·L241).'),
        ('4.|일곱 회사의', '모트가 전부 같은 말로 설명된다', _osc_moat(),
         'Lumentum 의 에피택시 노하우가 몇 년치인지는 전사에 숫자가 없다. '
         '진행자V 는 유리 100년을 두고 「모트로서는 그보다 좋을 수가 없다」고 했다(L365).'),
        ('5.|반대쪽 힘은', '지름을 키우는 한 수', _osc_wafer(),
         '다이 원가가 얼마로 내려가는지는 60%인지 40%인지 진행자A 도 대지 못한 채 넘어갔다(L235). '
         '진행자V 는 생산능력이 좋은 레이저를 뜻하지는 않는다는 유보를 달았다(L259·L261).'),
        ('6.|스케일업이 언제', '같은 물음에 답이 둘인 자리', _osc_timing(),
         '구리 시장에 있는 사람은 아직 아니라고 하고 광학 스케일업 시장에 있는 사람은 2027~28년이라고 할 테니 각자 파 볼 물음이라며 답을 열어 뒀다(L371·L375). '
         '진행자V 도 시점을 모르면 유리섬유 수요를 셈할 방법이 없다고 했다(L373).'),
    ],
    (OSU, 'strategy'): [
        ('1.|진행자V는 회사보다', '구리가 물러나는 세 자리', _osu_layers(),
         '진행자V 는 회사보다 기술을 먼저 놓자고 했다(L51). 스케일아웃은 100미터까지 가고 한 랙에 GPU 72개가 든다(L109·L133·L135). '
         '랙 무게 3톤은 「쯤」이라고 했다(L141).'),
        ('3.|중요한 건 시점이다', '세대가 갈아타지 않고 겹친다', _osu_overlap(),
         '1.6테라 시작을 「2026년 어느 시점일 것」이라고 어림했다(L41). '
         'TSMC 가 2나노를 올리면서 5나노·3나노에서 여전히 큰돈을 번다는 것이 진행자A 가 든 그림이다(L45).'),
        ('4.|업계가 낸 답은', '레이저를 모듈에서 떼어 놓는다', _osu_els(),
         '플러그형에서는 DSP 하나에만 20와트가 들고, 그 전력이 연산으로 가지 않는다(L117·L119·L121). '
         '연속파 레이저는 400밀리와트로 그냥 켜져 있으면 된다(L165·L179).'),
        ('5.|원인은 소재다', '웨이퍼 지름이 만든 병목', _osu_wafer(),
         '막대 높이는 지름의 비율이다. 한 장에서 뽑는 칩은 최대 16배 차이다(L195·L197). '
         '월 투입량은 진행자V 의 어림이다(L201·L203). 새 팹을 세워도 가동과 품질인증까지 6~9개월이 걸린다(L201).'),
        ('6.|광회로 스위치(OCS)는', '변환을 생략하면 무엇이 달라지나', _osu_ocs(),
         '훈련 작업은 배선이 잘 안 바뀌어 「설정해 두고 잊어버리는 방식」이 맞아떨어졌다(L233·L235). '
         '구글이 초기 TPU 팟에서 사내용으로 쓴 것이 시작이고, 루멘텀의 수주잔고가 0에서 4억 달러가 됐다(L191·L193·L229).'),
    ],
    (MTA, 'strategy'): [
        ('1.|답은 칩렛', '세대가 바뀔 때 무엇이 다시 쓰이나', _mta_chiplet(),
         '진행자A 가 레고 블록에 견줬다(L251~L255). 다이 접점이 한 곳에서 최소 세 곳으로 는다는 것이 진행자V 가 붙인 살이다(L263·L265). '
         '설계가 겹쳐도 검증과 양산은 제품 수만큼 늘어난다(L265).'),
        ('2.|진행자A 는 메타를', '광고가 도는 세 단계', _mta_pipeline(),
         'Andromeda 는 원래 Grace Hopper 와 함께 설계됐는데 지금은 여러 벤더에 걸쳐 돈다(L139~L145). '
         'Lattice 가 어느 하드웨어에서 도는지는 찾지 못했다고 밝혔다(L151). Gem 은 추천 시스템 중 처음으로 컴퓨트를 더 넣으면 좋아지는 양상을 보였다(L153·L155).'),
        ('2.|MTIA300 이 800와트급', 'LLM 과 다른 모양의 일', _mta_workload(),
         '아이오와에서 온 사용자면 그와 관련된 특성을 찾아 오고 다른 사람이면 표를 다르게 훑는다(L161). '
         '그래서 대역폭이 아니라 메모리 접근과 용량에 매인다(L163). 이 칩은 이미 수십만 대 깔렸다(L163).'),
        ('3.|바뀐 항목이', '400·450·500 세대에서 바뀐 것', _mta_spec(),
         '추론에서는 하나의 워크로드를 1만 칩까지 펼칠 이유가 없고 72개나 144개면 된다(L245·L247). '
         '전문가 혼합 모델의 통신도 요즘은 스케일업 쪽이다(L247). 각 세대의 전력과 대역폭은 이 회차에 없다.'),
        ('5.|역사가 여기 겹친다', '2017년과 지금이 겹치는 자리', _mta_2017(),
         '2017년에도 40기가에서 100기가로 넘어가는 전환을 타고 주가가 12달러에서 105달러까지 갔다(L407~L415). '
         '한 분기 수요가 약해지자 판매단가가 무너지고 자체 레이저 신뢰성에도 문제가 생겨 수직계열화의 이점이 짐이 됐다(L429·L431·L441).'),
    ],
    (OPX, 'strategy'): [
        ('1.|월요일에 엔비디아', '사흘 만에 뒤집힌 한 주', _opx_week(),
         '두 회사는 실적발표마다 스케일업이 옵틱스로 넘어온다고 말해 왔고 그 말 뒤에 40억 달러가 얹혔다(L81·L83). '
         '수요일 밤 발언으로 CPO 도입 시점이 2030년 안쪽까지 더 밀릴 수 있다는 이야기가 됐다(L95·L97·L111).'),
        ('2.|코퍼가 버티는', '밀집이 줄인 것은 필요한 거리다', _opx_reach(),
         '576개는 「정확친 않지만」이라는 단서가 붙은 수다(L237). 구리가 닿는 거리는 3미터에서 7미터 사이로 말했다(L239·L243). '
         '랙마다 실제 배선 길이는 전사에 숫자가 없다.'),
        ('2.|숫자로 확인할', '속도를 올리면 닿는 거리가 준다', _opx_cable(),
         '7미터에서 5미터로 준다는 것은 실적발표에서 그렇게 말한 것 같다는 단서가 붙은 값이다(L259). '
         '랙 높이 8피트도 「모르겠는데 8피트쯤」이라고 했다(L263).'),
        ('3.|CPO 관점의', '40억 달러로 산 갈래들', _opx_options(),
         'CW 레이저는 변조가 없어 만들기는 단순한 대신 높은 출력을 내기가 어렵다(L179·L181). '
         'OCS 두 방식 중 어느 쪽이 나은지는 자신도 모른다고 했다(L183·L187). 계약은 다년이고 비독점이다(L147).'),
        ('5.|그런데 ALC 는', '시점이 정하는 중간 기술의 운명', _opx_timing(),
         'ALC 도 마이크로LED 트랜시버를 꽂아 쓰는 방식이라 광학 엔진이 스위치 실리콘 옆으로 들어가면 자리가 없어진다(L281·L289). '
         '3.2테라비트가 구리로 되면 CPO 를 부를 이유가 2032년까지 밀린다는 것이 진행자V 의 계산이다(L321·L323).'),
    ],
    (GTC, 'strategy'): [
        ('1.|이번에는 같은', '곡선 하나를 세 칸으로', _gtc_tiers(),
         '무료 등급을 주는 이유는 간단한 물음에 답해 새 고객을 들이는 것이다(L75·L77). 백만 토큰당 3달러는 중간 등급에 붙은 예시다(L79). '
         '상위·프리미엄에 붙은 금액은 전사에 없다.'),
        ('2.|붙이는 방법이', '추론 한 번을 두 랙에 나눠 앉힌다', _gtc_split(),
         '화살표를 타고 넘어가는 것은 활성값뿐이다. Dynamo 가 사전연산과 해독을 떼어 배치하는 층이고, 젠슨은 이 층이 Groq 를 해독 자리에 세울 수 있게 했다고 말했다(L171·L173·L175). '
         '두 시스템은 오늘 이더넷으로 밀결합돼 있고 지연을 절반으로 줄이는 특수 모드가 있다(L179).'),
        ('4.|Vera Rubin은 이제', '데이터센터 한 벌의 랙 넷', _gtc_racks(),
         'Vera CPU 랙이 하나인지 여럿인지는 기억이 안 난다고 했다(L125). STX 랙과 ICMS 의 관계는 두 사람의 해석이고 젠슨은 거의 말하지 않았다(L247·L249). '
         '랙마다의 대수와 금액은 전사에 없다.'),
        ('5.|경계가 옮겨지는', '랙이 달라도 한 도메인이다', _gtc_domain(),
         '캐니스터 사이가 플러거블 트랜시버인지 CPO 인지는 진행자V 도 「정말 모르겠다」고 했고, 케이블 수와 트랜시버 전력을 세어 봐야 안다고 했다(L235·L239). '
         '미드플레인 PCB 는 52층이고 둘이 들어야 한다(L215).'),
        ('6.|여기서 60%가', '같은 말이 고객 두 무리에 다르게 닿는다', _gtc_customers(),
         '고객의 60%가 CSP 와 하이퍼스케일러이고 가장 큰 워크로드는 트랜스포머 기반 LLM 추론이다(L71). '
         '나머지에게는 트랙터도 식료품도 파는 회사에 토큰 사업 모델을 얹는 셈이 안 맞는다는 것이 진행자A 의 지적이다(L349·L353·L355).'),
    ],
    (MLD, 'strategy'): [
        ('1.|거리 수치가', '구리가 멈추는 자리와 그다음', _mld_reach(),
         '구리는 레인당 400기가비트에서 「1미터나 길어야 1미터 반」이라고 했다. 브로드컴 CEO Hock Tan 이 말하는 구간이다(L269·L271). 10~30미터는 마이크로LED 진영의 주장이라고 화자가 단서를 달았다(L277). '
         '가운데 빈 구간을 무엇이 채우는지가 이 절의 물음이다.'),
        ('2.|숫자로 보면', '채널 하나를 빠르게 대 다발을 넓게', _mld_wide(),
         '전사에는 200기가비트는 물론 50기가비트도 못 밀 것 같다는 말이 나오고 거기에도 「모르겠다」가 붙는다(L251). '
         '이미징 파이버는 내시경에 쓰는 부품이고 한 다발에 천 가닥쯤이다(L253). 총 대역폭은 전사에 숫자가 없다.'),
        ('3.|후보는 둘 이상', '스케일업 자리를 놓고 선 후보 셋', _mld_cands(),
         'VCSEL 이 닿는 거리는 전사에 없다. 라이다에 이미 수십억 개가 나갔다는 것이 그 진영의 근거이고(L303), '
         'Lumentum 이 OFC 에서 스케일업용을 개발 중이라고 밝혔다(L309).'),
        ('4.|마이크론 배제론', 'HBM 스택에서 의심을 산 자리', _mld_base(),
         'D램 셀은 트랜지스터 하나에 커패시터 하나를 얹은 꼴이라 밀도에 맞춰져 있고 가장 빠른 트랜지스터를 만드는 데는 맞춰져 있지 않다(L159·L161·L163). '
         '다이 개수는 보기용이다 — 전사에 몇 장인지 없다.'),
        ('6.|반론이 이 회차', '토큰을 얻는 두 길과 같은 끝', _mld_token(),
         '델 서버는 대당 12만 달러쯤이고 메모리 768기가바이트 정도인 것 같다고 진행자A 가 스스로 단서를 달았다(L53). '
         '초당 토큰 수가 정해져 있어 EDA 라이선스처럼 나눠 쓰게 된다는 것이 반론이다(L57·L59).'),
    ],
    (ARM, 'strategy'): [
        ('2.|원리는 두 겹', '16자리를 3자리로 줄이는 손질', _arm_quant(),
         '무작위 행렬은 점들 사이 거리와 각도는 그대로 두면서 유난히 큰 값 몇 개를 고르게 편다(L139·L143). '
         'QJL 을 거치면 거리는 한 자리, 각도는 두세 자리가 된다(L145·L153). 각도가 0에서 128까지 흩어지면 일곱 자리인데 '
         '여덟 개로 몰면 세 자리다(L149).'),
        ('3.|여유가 흘러가는', '줄여서 생긴 여유가 가는 곳 셋', _arm_slack(),
         '엣지로 내리는 길은 정보 손실 없이 된다며 「건초더미에서 바늘 찾기」 벤치마크를 근거로 들었다(L175). '
         '셋 중 어느 쪽으로 가도 메모리를 덜 사는 결과에는 닿지 않는다.'),
        ('4.|행사에서 Arm이', '기가와트당 CPU 코어', _arm_cores(),
         '에이전틱 AI 가 도구 호출과 웹 탐색 같은 조율 작업을 CPU 에 얹는다는 것이 앞의 논리다(L215). '
         '막대 높이는 두 값의 비율이다(L217). 이 수를 무엇으로 셌는지는 전사에 없다.'),
        ('4.|수를 코어에서', '코어 수를 칩 수로 옮겨 보면', _arm_rack(),
         '코어 4만5천은 화자가 「그게 얼마였더라」 하며 더듬은 근사치다(L305). 칩당 136코어로 나눈 것은 진행자V 의 계산이고(L309·L311), '
         '베라 루빈 랙이 이미 1대1이라 4배 주장이 맞으면 4대1까지 간다는 데까지만 갔다(L313·L315·L321).'),
        ('6.|Arm이 보여준', '같은 매출에서 가져가는 금액', _arm_take(),
         '막대 높이는 세 값의 비율이다(L321·L323·L325). 라이선스 사업의 순이익률은 이미 98~99%에 가깝고(L325), '
         '직접 팔면 이익률은 절반으로 내려가지만 들어오는 금액은 크게 는다(L327).'),
    ],
    (NVM, 'strategy'): [
        ('2.|여기서 나온', 'NVLink 아래에서 매체만 갈린다', _nvm_nvlink(),
         '지금은 구리 위에서 SerDes 가 비트를 실어 보낸다(L43). 빛으로 가는 것은 「이론적으로」라고 단서를 달았고(L43), '
         'HBM 과 GPU 를 광 링크로 붙이는 데까지 가느냐는 물음은 답 없이 남았다(L39).'),
        ('3.|진행자V가 얹은', '누가 어느 규격을 받쳐 주나', _nvm_support(),
         'ESUN 은 자막이 「E-Sun」으로 받아 적은 것이라 이더넷 계열 스케일업 규격으로 보일 뿐 확정할 수 없다(L79). '
         '점유율이나 물량은 전사에 숫자가 없다.'),
        ('4.|가장 값진', '예전 라인과 HBM 으로 바꾼 라인', _nvm_hbm(),
         'TSV 둘레에는 트랜지스터를 못 놓는 여백이 있어 같은 면적에 담기는 용량이 떨어진다(L181·L183). '
         '웨이퍼 3배와 앞으로 4배는 전사의 값이다(L155·L181).'),
        ('5.|달라진 자리는', '메모리 계약이 길어졌다', _nvm_contract(),
         '길게 가는 이유는 양쪽 다 물량 가시성을 원해서다(L193·L195). 하이퍼스케일러가 과다하게 잡아 두고 있을 수 있다면서도 '
         '실제로 과잉 구독인지는 모르겠다고 달았다(L187·L189).'),
        ('6.|시간 순서로 보면', 'Fab 34 지분이 오간 순서', _nvm_fab(),
         '지분을 넘긴 것은 겔싱어의 스마트 캐피털 전략 아래였다(L235·L239). 유럽 안에서 인텔의 유일한 EUV 팹이다(L237).'),
    ],
    (IEO, 'strategy'): [
        ('1.|테라팹 구상 자체는', '웨이퍼 투입 목표 둘', _ieo_wafer(),
         '막대 높이는 두 값의 비율이다(L23·L25). 언제까지 그 규모에 닿겠다는 시점은 전사에 없다.'),
        ('2.|그러면 되돌리는', '갈라진 이유와 되돌릴 조건', _ieo_reunite(),
         '고정비를 설계사 수백 곳이 나눠 내는 구조가 분업의 이유다(L39·L41). ② 는 리소그래피에 비용이 몰려 있어 '
         'ASML 의 EUV 지출을 덜어낼 방법이 안 보인다고 했고, 말하다 말고 「셈이 안 맞는다」로 닫았다(L43).'),
        ('3.|진행자V는 범위를', '수직 통합이 어디서 멈추나', _ieo_scope(),
         '광트랜시버를 만들면 부품 조립도 하나, 저항과 커패시터는 어디서 구하나, 기판은 직접 만드나까지 물었다(L45·L47·L49). '
         '두 사람이 웃은 자리이고 답은 안 나왔다(L51).'),
        ('4.|진행자V가 견줄', '청중 수와 치른 금액', _ieo_audience(),
         '조 로건은 2020년 스포티파이와 여러 해에 걸쳐 2억 달러였다(L153). TBPN 금액은 진행자들이 1억에서 3억 달러로 어림한 것이다(L81). '
         '로건의 재계약 금액은 전사에 없다.'),
        ('6.|셋을 겹쳐 보면', '셋이 산 것은 같은 물건이다', _ieo_three(),
         '이 글이 세 화제를 한 물음으로 꿴 자리다. 7만 명은 TBPN 시청자 수이고(L153), 나머지 둘은 숫자가 아니라 상태다.'),
    ],
    (MTX, 'strategy'): [
        ('2.|칩 안에서 모델', '가중치를 어디에 두나', _mtx_split(),
         'SRAM 은 응답이 아주 빠른 대신 담을 수 있는 양이 적다(L89·L91). Pope 는 둘을 합치는 일을 「테이블 위에 그냥 놓여 있던 공짜 돈」이라 불렀다(L89). '
         '어느 쪽이 얼마나 빠르고 얼마나 담는지는 전사에 숫자가 없다.'),
        ('2.|디코드에서 벌', 'HBM 통행량을 무엇이 쓰나', _mtx_bandwidth(),
         '토큰 하나를 뱉을 때마다 가중치 전체를 다시 실어 와야 한다. 가중치가 SRAM 에 올라가면 그 왕복이 통째로 사라지고 통행량 전부가 KV 캐시로 간다(L171·L173). '
         '기둥을 나눈 비율은 보기용이다 — 전사에 숫자가 없다.'),
        ('3.|여기서 Pope가', '지연을 줄이면 문맥이 길어지는 사슬', _mtx_loop(),
         '대기 줄의 길이는 도착 속도에 처리 시간을 곱한 값이라는 리틀의 법칙 그대로다(L175). '
         '「저지연은 쓰기 편하다는 이점만이 아니라 처리량 자체를 올린다」는 것이 이 사슬의 결론이다(L177). 몇 배인지는 전사에 없다.'),
        ('4.|칩을 평가하는', '칩을 재는 다섯 잣대와 그 방침', _mtx_five(),
         '다섯은 Pope 가 든 것이다(L139). 크게 앞선다고 꼽은 셋 말고 큰 항목에서 뒤지는 데는 없다고 했고, '
         'LLM 과 덜 붙는 항목에서는 뒤질 수도 있다는 유보를 달았다(L141). 잣대마다의 측정치는 이 회차에 없다.'),
        ('7.|가장 큰 회의론', '감당해야 할 규모의 크기', _mtx_scale(),
         '100기가와트에 언제 닿을지는 자신도 모르겠다고 했다(L261). 기가와트당 금액은 150억에서 200억 달러 사이로 말했고 곱하는 배수도 어림이다(L263). '
         '인원은 MatX 100명 남짓 대 상대 1만~2만 명이다(L195).'),
    ],
    (CRD, 'strategy'): [
        ('1.|Credo가 원래 잘', 'Credo 포트폴리오에서 비어 있던 칸', _crd_portfolio(),
         '서데스에서 시작해 구리 케이블과 광학 DSP·트랜시버, 링크 감시 소프트웨어까지 갖췄다(L93·L99·L101). '
         '광집적회로 설계 하나가 없었고 이번 인수로 채워졌다(L103). 칸마다의 매출은 전사에 없다.'),
        ('2.|진행자V가 투자자', '연결이 자라는 구간 셋', _crd_vectors(),
         '투자자 개빈 베이커의 글을 진행자V 가 옮긴 것이다. 구리가 2030년까지 남고(L137), 랙 사이도 여전히 구리로 갈 수 있으며(L165), '
         '다음 성장 축은 데이터센터 사이다(L145·L149). 구간마다의 크기는 전사에 없다.'),
        ('3.|더스트포토닉스가 가', '레이저를 어디에 놓나', _crd_laser(),
         '위에 얹으면 그 레이저를 만드는 회사와 공급망에 묶인다(L185·L187). 옆에 놓고 결합하면 공기 틈이 남지 않아 '
         '액체 냉각에 그대로 넣을 수 있다(L185·L189). 손실이 얼마나 주는지는 전사에 없다.'),
        ('4.|수치가 차이를', '커넥터 하나가 내는 대역폭', _crd_bars(),
         '막대 높이는 두 값의 비율이다(L197·L199). XPO 는 200Gbps 채널 예순넷을 한 커넥터에 몰아넣었고, 그만큼 열이 올라 '
         '400W 를 액체 냉각으로 받는다(L201).'),
        ('6.|CPO 쪽으로 가더라도', '광학 엔진이 앉는 자리 셋', _crd_place(),
         'CPO 는 스위치 실리콘과 한 패키지에 들어가 갈아 끼울 수 없다(L221). XPO 는 랙 앞면에 꽂아 하던 대로 갈아 끼우고(L225·L227), '
         'CPX 는 칩 옆에 소켓을 남긴다(L243·L245). 어느 쪽이 얼마나 퍼졌는지는 전사에 없다.'),
    ],
    (INT, 'strategy'): [
        ('1.|토큰 요금을 대', '토큰을 얻는 세 길과 그 값', _int_price(),
         '월 200달러 정액은 사람이 손으로 쓸 때를 전제로 짜여 있었다(L37·L39). API 종량은 진행자V 가 잠깐 돌려 본 값이고(L21), '
         '월 2만 달러는 진행자A 가 그 속도로 환산한 어림이다(L47). 주 7달러는 Fireworks AI 의 fire pass 다(L25).'),
        ('2.|기계를 사서', '빌려 쓸 때와 사서 가질 때', _int_buy(),
         '기계값은 본인도 1만인지 5천인지 헷갈렸다(L67). 되판 값은 진행자V 가 실제로 겪은 그래픽 카드다(L115). '
         '메모리 값이 오르는 중이라 1년 쓰고 같은 값에 팔 수도 있다고 봤다(L107·L121).'),
        ('4.|같은 발표에', 'IPU 가 CPU 에서 떼어 가는 것 셋', _int_ipu(),
         '구글과 인텔이 함께 설계한다(L183). AWS 의 Nitro 나 DPU 와 같은 발상이라고 진행자A 가 짚었다(L187). '
         '언제 얼마나 배치되는지는 전사에 없다.'),
        ('6.|핵심 차이는', '메모리를 한 종류로 두나, 섞나', _int_memory(),
         '섞으면 데이터가 어디서 오는지 예측이 어려워지는데, 계층마다 지연을 알고 경로를 작업 전에 정해 두는 것이 이쪽의 답이다(L221·L223). '
         '256개와 수천 개는 전사의 값이고(L225), 랙으로는 열 개가 한 개가 된다(L233).'),
        ('6.|여러 업체의', '이름은 여섯인데 자리는 몇인가', _int_winners(),
         '여섯은 이 회차에 이름이 나온 곳이다(L243). 칩 하나를 만드는 비용이 커서 손익분기 물량이 필요하고, '
         '그만한 물량을 움직일 고객은 다섯이나 여섯이다(L241·L247). 누가 남는지는 이 회차도 모른다고 했다.'),
    ],
    (GIM, 'strategy'): [
        ('1.|남는 길은 워크로', '한 덩어리로 볼 때와 조각으로 나눌 때', _gim_pieces(),
         '조각은 이 회차가 이름을 댄 셋이다. 프리필 하나만 놓고도 더 나눌 수 있다고 Natalie 는 봤고(L37), '
         '칩과 칩 사이로 데이터를 보내는 비용 때문에 끝없이 나누지는 않는다(L41). 몇 조각이 맞는지는 전사에 없다.'),
        ('2.|동작 순서는 네', '받아서 나누고 내려보내기까지 넷', _gim_stack(),
         '③ 이 이 회사의 성격이 드러나는 자리다. 어디서 끊을지를 여기서 정한다(L45). 상자 크기는 같게 뒀고 단계마다 드는 시간은 전사에 없다.'),
        ('3.|CPU 이야기가 나', '도구 호출이 어디서 도나', _gim_toolcall(),
         'Natalie 가 든 오늘의 코딩 에이전트다(L65). 왼쪽은 모델이 남의 서버에 있고 도구 실행이 내 노트북에 있어 계속 오간다. '
         '오른쪽은 그 실행을 모델 옆으로 옮긴 것이다. 지연이 몇 배 낫다는 값은 전사에 없다.'),
        ('5.|같은 워크로드에', '세 구성과 그 곡선', _gim_three(),
         '모델은 GPT-OSS 120B, 입력 8K·출력 1K 다(L151). 4배는 ③ 이 ② 의 최적화된 선 위에서 다시 벌어 준 폭이다(L151). '
         '곡선의 좌표값은 전사에 없어 그리지 않았다.'),
        ('6.|Baltier가 꺼낸', '네오클라우드 연간 비용의 구성', _gim_amort(),
         '하드웨어 상각이 70% 다(L175). 나머지 30% 의 속은 전사에 없어 한 칸으로 뒀다.'),
    ],
    (MET, 'strategy'): [
        ('1.|누가 앱을 열면', '광고 하나가 뜨기까지', _met_serve(),
         '검색과 랭킹이 갈리는 자리와 그 위에 걸린 시간 제약이다(L21·L23·L31·L33·L39). 단계마다 걸리는 시간은 전사에 없다.'),
        ('2.|Meta는 목적마다', '모델을 합쳤다가 다시 줄이기까지', _met_lattice(),
         'Lattice 로 합친 이유가 둘, GEM 을 그대로 못 올리는 이유가 둘이다(L23·L25·L27·L43). 모델 크기는 전사에 없다.'),
        ('3.|Meta가 최근 올린', '같은 예산 안에서 연산을 달리 쓴다', _met_adaptive(),
         '이력이 긴 사람에게 훨씬 많은 연산을 쓴다(L33). 몇 배인지는 전사에 없다. 파라미터 1조는 추론 시점 값이다(L109).'),
        ('4.|그래서 훈련 예제마다', '예제 하나의 크기가 부품 비율을 정한다', _met_example(),
         '추천 예제에는 개인화 덩어리가 실린다(L95·L97). 아래 셋은 그래서 달라지는 것이다(L99). 비율의 값은 전사에 없다.'),
        ('5.|여러 종류의 칩을', '이종 하드웨어를 다루는 세 갈래', _met_kernel(),
         '① 과 ② 는 전부터 있던 선택지다(L113). ③ 은 최근에 생겼고, 커널 100배를 원한다는 말이 여기 붙는다(L131).'),
    ],
    (GN, 'strategy'): [
        ('1.|TPU는 원래', 'TPU 는 세대마다 칩을 나눴다 붙였다 했다', _gn_gens(),
         '색이 다른 것이 나뉜 세대다.'),
        ('2.|HBM(고대역폭', '추론칩과 훈련칩이 메모리를 다르게 채운다', _gn_mem(),
         '추론칩 8I 의 SRAM 이 384메가바이트로 훈련칩 8T 의 세 배다(L47). HBM 도 추론칩이 288기가바이트, 훈련칩이 216기가바이트로 훈련 쪽이 적다(L49·L51). '
         '훈련은 칩을 더 붙여 클러스터 전체 메모리를 늘리면 되고, 추론은 한 칩 안의 층을 모두 채워야 한다는 것이 진행자 둘의 읽기다(L53·L55). 8T 의 SRAM 절대값은 전사에 없어 「그 3분의 1」로만 뒀다.'),
        ('3.|구글의 이전 망', '계층이 셋에서 둘로 줄었다', _gn_layers(),
         'Virgo 는 포트가 많은 광회선 스위치로 계층을 둘로 눌러 초당 47페타비트를 냈고 TPU 134,000개를 한 덩이로 묶었다(L129·L137).'),
        ('5.|TPU v7 구', '같은 거리를 몇 홉에 가나', _gn_hops(),
         'Boardfly 는 보드에 TPU 넷, 랙에 보드 여덟, 파드에 그룹 서른여섯을 두고 그룹 간을 광회선 스위치로 이어 같은 거리를 일곱 홉에 '
         '간다(L229·L243·L245).'),
    ],
    (HW, 'strategy'): [
        ('1.|Austin은 ', '지연을 무엇으로 나누겠다는 셈인가', _hw_alpha(),
         '막대 높이가 그 값이다 — 어떤 공정으로 그 배수를 내는지는 논문이 대지 않았다.'),
        ('2.|원리 자체는 새', '로직 위에 로직을 얹었다', _hw_stack(),
         '실제로 만든 것은 하이브리드 본딩으로 로직 다이 위에 로직 다이를 얹은 물건이다. 접속 피치가 1.5마이크론이고 연결이 수백만 개다(L63). '
         'Kirin 2026 은 같은 면적에 트랜지스터가 두 배다(L77). 메모리는 중복성이 있어 400층까지 쌓지만 로직끼리는 발열·정렬·평탄도가 함께 걸린다(L71·L73).'),
        ('3.|Austin은 ', '통제가 걸린 자리와 안 걸린 자리', _hw_control(),
         'EV Group 은 오스트리아 회사라 통제 축이 다르다(L99).'),
    ],
    (MC, 'strategy'): [
        ('5.|월스트리트저널 ', '넉 분기 만에 45%에서 85%로', _mc_margin(),
         ''),
        ('3.|HBM만의 문제', '같은 용량에 웨이퍼가 세 배 든다', _mc_wafer(),
         '장 수가 값이다.'),
        ('3.|Vik은 여기서', '값이 오를 때 두 수요가 하는 일이 다르다', _mc_elastic(),
         '소비자 기기는 값이 오르면 탑재량을 4기가바이트에서 2기가바이트로 줄인다(L67). 데이터센터는 값과 거의 무관하게 그대로 사서 수요 곡선이 수직에 가깝다(L111). '
         '한국은 D램 증설에 5천억 달러 넘게 걸었고 세계 물량의 3분의 2가 한국에서 나온다(L85).'),
    ],

    (QC, 'strategy'): [
        ('1.', '손전화 쪽과 그 밖 쪽의 자리 바꿈', _qc_mix(),
         'CFO 자료의 도넛 셋이다. 기둥 높이는 이 분수 그대로다. 3분의 2 안에서 셋이 각각 얼마인지는 발표가 나누지 않았다.'),
        ('2.', '랙 하나로 채우던 것이 일별로 갈린다', _qc_disagg(),
         '늦게 온 회사가 디코드 하나만 겨냥하는 자리가 여기서 나온다(L109).'),
        ('3.', '옆에 붙일 것인가, 위에 얹을 것인가', _qc_hbc(),
         ''),
        ('3.|문제는 메모리 밑에', '메모리 밑에 무엇이 앉나 — 읽기 둘', _qc_read(),
         '근거는 발표 그림 하나뿐이다.'),
        ('4.', '층을 올리면 층당 용량이 뒤집힌다', _qc_tsv(),
         '한 층만 쓰면 메모리 층에 비아를 안 뚫어 밀도가 나온다. 두 층부터는 관통 실리콘 비아 둘레에 셀을 못 놓는 금지 구역이 생겨 층당 용량이 절반쯤으로 떨어지고, '
         '그래서 넷은 쌓아야 쓸모가 생긴다(L183·L185). 메모리 밑에 앉는 XPU 는 850제곱밀리미터쯤 되는 레티클급 다이라 평탄도와 열이 함께 걸린다(L161·L163).'),
        ('5.', '가속기 로드맵 — HBC 는 2027년부터', _qc_road(),
         ''),
    ],
    (CB, 'strategy'): [
        ('2.', '자를 것인가, 그대로 둘 것인가', _cb_dice(),
         '레티클 84장이 한 장에 이어 붙는다(L77).'),
        ('2.|문제는 완벽한 웨이퍼가 없다는', '죽은 코어를 건너뛰는 순서', _cb_yield(),
         '상자로는 안 세고 순서만 그렸다.'),
        ('3.', '층 셋이 저마다 다른 숙제를 진다', _cb_stack(),
         '커넥터 개수는 전사에 없어 안 그렸다.'),
        ('4.', '44기가바이트 안과 밖', _cb_wall(),
         '모델이 44기가바이트 안에 들어가면 GPU 로는 못 내는 초당 토큰이 나온다(L137). 넘으면 웨이퍼 여러 장에 쪼개야 하는데 '
         '네트워킹은 칩 한쪽 끝으로만 나가고 웨이퍼 안 데이터 이동보다 훨씬 느리다(L139). 병렬 셋은 진행자V 가 든 우회로 그대로다(L145). '
         '셋 다 웨이퍼 사이 통신에 기대니 웨이퍼 스케일의 기본 발상과 어긋난다(L147).'),
        ('5.', '같은 발상, 40년 뒤', _cb_forty(),
         '진행자V 가 센 간격이 40년이다(L187).'),
        ('6.', '하드웨어를 안 파는 하드웨어 회사', _cb_chain(),
         ''),
    ],
    (LI, 'strategy'): [
        ('6.', 'EUV 와 X선 — 파장을 바꾸면 다 바뀐다', _li_xray(),
         ''),
        ('1.|숫자를 붙이면', 'EUV 장비 값의 계단', _li_toolcost(),
         ''),
        ('2.|193나노미', '멀티패터닝 — 두 번 그어 간격을 반으로', _li_multipattern(),
         ''),
        ('3.|13.5나노', '주석 방울에서 웨이퍼까지', _li_lightpath(),
         ''),
        ('4.|파장은 20년', '하프 필드 — 같은 꼴 두 판', _li_halffield(),
         ''),
        ('5.|떼어 내면 셈이', '광원 하나로 스캐너 열 대', _li_fel(),
         '광원은 xLight 가 세우고 자본지출을 지며 팹은 빛을 산다(L258·L260). 출력·요금 값은 전사에 없고 칸 수만 값이다.'),
    ],
    (AP, 'strategy'): [
        ('2.|여기서 앞뒤가', '다이는 레티클을 못 넘는데 패키지는 3.3배', _ap_reticle(),
         '다이 하나는 레티클 한 장 858제곱밀리미터(26 × 33밀리미터)를 넘지 못한다(L135·L159). 패키지는 레티클 3.3배까지 커진다(L161). 그 사이를 메우는 것이 첨단 패키징이다.'),
        ('3.|CoWoS 는 세 층', 'CoWoS 세 갈래 — 가운데 층만 다르다', _ap_cowos(),
         '같은 세 층을 세 벌 그렸다.'),
        ('4.|EMIB(기판 안', 'CoWoS-L 세 층 대 EMIB 두 층', _ap_emib(),
         '값은 없는 그림이다 — 층의 수만 견준다.'),
        ('4.|여기서 나오는 ', '원형 웨이퍼와 사각 패널', _ap_panel(),
         '같은 자로 그렸고 버리는 비율은 전사에 없다.'),
        ('7.|Vik 이 마지막에', '레티클 배수 로드맵 — CoWoS 와 EMIB', _ap_roadmap(),
         '점선은 아직 안 나온 것이다.'),
    ],
    (WK, 'strategy'): [
        ('6.', '소프트웨어 원가가 무엇으로 바뀌나', _wk_cost(),
         ''),
        ('1.|Val 은 저장장치를', 'NVLink 레인 128 대 PCI 레인 32', _wk_lanes(),
         '같은 꼴 두 줄이다.'),
        ('3.|압축 이야기는', 'KV 캐시 — 단위는 90% 줄고 총량은 100배', _wk_kv(),
         ''),
        ('4.|먼저 메모리 계층을', 'Dynamo 의 메모리 네 층', _wk_tiers(),
         ''),
        ('4.|그러면 캐시 적중률은', '캐시 적중률 둘 — 논리와 실제', _wk_hit(),
         '같은 꼴 둘이다.'),
        ('5.|값을 내는 자리는', '여유분 — 1페타바이트 사서 300~500테라바이트', _wk_provision(),
         '짙은 조각은 그 범위의 위쪽 값이다.'),
    ],
    (MT, 'strategy'): [
        ('1.|가장 또렷한 숫자는', '설비투자 1,900억 달러 안의 250억', _mt_capex(),
         '막대 길이가 값이다.'),
        ('1.|진행자A는 연산을 더', '설비투자가 돌아오는 고리 — 닫히는 쪽과 안 닫히는 쪽', _mt_loop(),
         '같은 폭 두 줄이다.'),
        ('2.|삼성전자 실적에서', '삼성 HBM 점유율 — 전과 후', _mt_share(),
         '오른쪽 막대는 그 범위의 위쪽 값으로 그렸다.'),
        ('2.|진행자V는 그 주장이', '핀당 속도 — 규격과 실제', _mt_pin(),
         ''),
        ('3.|샌디스크의 이번 분기', '샌디스크 매출총이익률 — 전과 후', _mt_margin(),
         ''),
        ('5.|세 흐름을 나란히', '세 흐름을 이으면 고리가 된다', _mt_cycle(),
         ''),
    ],
    (PW, 'strategy'): [
        ('1.', '랙 하나가 먹는 전력', _pw_racks(),
         '막대 높이가 킬로와트고 「지금」은 범위의 위쪽 값으로 그렸다.'),
        ('4.', '전압을 어디서 낮추나', _pw_vertical(),
         '광통신에서 빛을 칩 가까이까지 끌고 가듯 전력도 고전압인 채로 칩 가까이까지 간다(L173). 멀리서 낮추면 낮은 전압이 긴 구리를 지나며 손실이 '
         '붙는데, Austin 이 든 리니어 플러거블의 긴 구리 트레이스가 같은 자리다(L177).'),
        ('2.|전력 쪽 병목은', '같은 600킬로와트를 48볼트로, 800볼트로', _pw_current(),
         '같은 꼴 둘이다. 손실은 전류의 제곱을 따르니 그 차이가 100~200배라는 것이 Vik 의 셈이다(L163).'),
        ('5.|전체 사슬을', '발전소에서 GPU 까지 전압이 바뀌는 자리', _pw_chain(),
         '자리마다 다른 회사가 서고 VRM 이 개수가 가장 많다.'),
        ('6.|정작 어느', '800볼트 다음의 두 갈래', _pw_fork(),
         '① 있던 48볼트 설비를 그대로 쓰며 48·12·1볼트로 내려가는 길과 ② 6볼트로 바로 가는 길(TI·Navitas)이 갈린다(L215). 어느 쪽이 서는지는 아직 정해지지 않았다는 것이 Vik 의 말이다.'),
    ],
    (CX, 'strategy'): [
        ('1.', '마벨이 파는 것 — 거리만 다르다', _cx_marvell(),
         '진행자V 는 마벨의 사업을 데이터 이동 하나로 묶었다 — 칩 안에서는 ASIC, 칩 사이에서는 인터커넥트, 데이터센터 사이에서는 DSP 다(L119). '
         '이번 키노트는 매출 대부분이 인터커넥트에서 나온다는 것을 보이며 연결 회사 쪽에 무게를 실었다(L113). '
         'XPU 를 만들어 주는 고객에게 인터커넥트를 얹어 파는 이야기는 하지 않았다(L115·L117).'),
        ('2.|막힌 곳은 둘이다', 'CPO 가 랙 안으로 못 들어오는 이유 둘', _cx_cpo_blocks(),
         '같은 꼴 두 기둥이다. 99% 는 Vik 이 전한 수다.'),
        ('3.|XPO 모듈은', '빛으로 가는 길 넷 — 칩에 얼마나 가까운가', _cx_optics_ways(),
         '플러그형에서 OSFP 여덟을 하나로 합친 XPO(L141), 소켓에 꽂는 NPO(L131), 패키지 위에 붙이는 CPO 순으로 광 엔진이 칩에 가까워진다. 이 회차의 물음은 CPO 가 랙 안(스케일업)까지 들어오느냐다(L125).'),
        ('4.|전압 변환 칩을', '전압 구간마다 소재가 다르다', _cx_voltage(),
         '리테온 부스의 답과 영상이 같은 구조다(L177·L183).'),
        ('5.|버티브 부스에는', '조립식 인프라 블록 — 전과 후', _cx_prefab(),
         '전에는 냉각·전원 설비를 현장에서 짓고 랙을 넣었다. 배치 시간이 절반으로 준다는 것은 델타 부스 담당자의 말이고(L199), 판 위에 시간 값은 '
         '없다.'),
        ('6.|인텔 키노트의', '클리어워터포레스트 칩렛 열일곱', _cx_chiplets(),
         '칸 수가 값이다.'),
    ],
    (GF, 'strategy'): [
        ('1.|Barber가 ', '레인 속도별 구리가 가는 거리', _gf_reach(),
         ''),
        ('1.|문제는 이 대응', '속도가 오르면 왜 광으로 가나', _gf_chain(),
         '레인 속도가 두 배 오르면 구리가 가는 거리가 절반이 되고, 스위치를 랙 가운데로 내리는 수는 랙 높이가 바닥이라 한 번뿐이다(L81). 그다음은 광이다.'),
        ('2.|수요가 이렇게 ', '200mm 에서 300mm 로 — 전과 후', _gf_wafer(),
         '같은 꼴의 웨이퍼 둘이다.'),
        ('3.|손실이 어디서 나는지가', '광 엔진을 어디까지 안으로 들이나', _gf_place(),
         '같은 보드에 같은 프로세서와 광 엔진을 세 번 그렸다. 다른 것은 둘 사이 전기 배선 길이뿐이다. 플러거블 약 35dB·20~25피코줄, NPO '
         '15~20dB·10피코줄쯤, CPO 6dB 안팎(다른 자리에서는 3dB)·5피코줄 미만(L91~L97).'),
        ('5.|바꾼 방향이 뒤로다', 'PAM4 와 NRZ — 레벨 사이 틈', _gf_pam(),
         '같은 진폭 안에 PAM4 는 레벨 넷을, NRZ 는 둘을 둔다(L139·L141). 값은 레벨 수뿐이다.'),
        ('5.|레이저 쪽 셈도', '레이저 하나가 먹이는 파이버 수', _gf_laser(),
         '작은 네모 하나가 파이버 한 가닥이다. 파장을 늘려도 레이저 수는 그만큼 늘지 않는다.'),
        ('6.|Scale 플랫폼은', 'Scale 광 엔진의 세 층과 누가 만드나', _gf_stack(),
         '위에서 아래로 전자 IC·광자 IC·마이크로 광학과 탈착식 파이버 커넥터(L165).'),
    ],
    (AL, 'strategy'): [
        ('1.|Vik은 이 신호를', '실에 꿴 구슬이 무너지는 다섯 자리', _al_beads(),
         '① 감쇠 — 가는 동안 구슬이 흐려진다. '
         '② 반사 — 배선 끝에서 되튀다. '
         '③ 크로스토크 — 옆 배선의 구슬이 끼어든다(L57). '
         '④ 심볼 간 간섭 — 구슬이 설탕처럼 서로 달라붙어 한 덩어리가 된다(L59·L61). '
         '⑤ 지터 — 읽으려고 보는 그 시각(점선)에 구슬이 없다(L63). '
         '구슬 수와 줄어드는 폭은 보기용이다 — 전사에 숫자가 없다.'),
        ('1.|얼마나 빠른지부터', 'PCIe 세대와 초당 전송 수', _al_gen(),
         '블랙웰 세대에 들어간 것은 Gen6 제품이었을 것이라고 Vik 은 봤다(L143).'),
        ('1.|이 다섯이 한 그림으로', '눈 다이어그램 — 열린 눈과 닫힌 눈', _al_eye(),
         '같은 네 궤적을 두 판에 그렸다. 왼쪽은 0 으로 읽을 아래와 1 로 읽을 위 사이에 틈이 있고(L73·L75), 오른쪽은 궤적이 시간(지터)과 전압에서 흔들려 그 틈이 메워졌다. 값은 없는 그림이다 — 파형을 천 장쯤 겹쳐 그리면 이 모양이 된다는 것이 Austin 의 설명이다(L77).'),
        ('1.|업계에 보이는 규칙은', '속도가 오르면 왜 칩 자리가 생기나', _al_chain(),
         ''),
        ('2.|리드라이버는 ①②만', '리드라이버와 리타이머 — 같은 네 손질 중 무엇을 하나', _al_two(),
         '같은 네 칸을 두 줄로 그렸다.'),
        ('4.|이 잠금이 깨질 뻔한', 'GPU 와 NIC 사이 — 계획과 실제', _al_nic(),
         '같은 GPU 와 NIC 을 세 번 그렸다.'),
        ('5.|나머지 제품군은', '한 기술을 세 자리에', _al_three(),
         ''),
        ('6.|읽을 것은 순서다', 'AMD 와 브로드컴 — 순서', _al_order(),
         '헬리오스는 UALOE 로 간다(L169).'),
    ],
    (DC, 'strategy'): [
        ('2.|데이터센터 망은 세 층이다', '망의 층 — 안에서 밖으로', _dc_layers(),
         '점선 둘은 오늘 안 다룬다고 Vik 이 선을 그은 것이다.'),
        ('4.|속도 세대는 겹쳐서', '속도 세대 — 겹쳐서 간다', _dc_gens(),
         '다음이3.2 가 아니라 레인당 300기가짜리 2.4테라일 가능성이 '
         '돈다는 것은 Vik 의 전언이다(L157).'),
        ('5.|그런데 속도가 오르면', 'PCB 층수 — 25층과 78층', _dc_layers78(),
         '줄 하나가 층 하나다.'),
        ('6.|전력을 수로 보면', '플러거블이 스케일업에서 밀리는 셈', _dc_power(),
         ''),
        ('6.|그 전력이 어디서 새는지가', '광 엔진을 스위치 칩 쪽으로 당기기', _dc_place(),
         '같은 보드에 같은 스위치 칩과 광 엔진을 세 번 그렸다. 에너지가 3분의 1 까지 떨어진다는 것이 Vik 의 말이다(L167).'),
    ],
    (CDS, 'strategy'): [
        ('1.', '설비투자 값을 누가 매기나', _cds_pricing(),
         ''),
        ('3.', '좋은 숫자가 나쁜 사건이 되는 경로', _cds_expect(),
         ''),
        ('4.|그런데 밀려나지도', '메모리 계층 셋', _cds_layers(),
         ''),
        ('4.|그래서 지금 갈라진', '수익성 순위와 대체 불가능성 순위', _cds_rank(),
         '같은 두 칸을 두 줄로 그렸다.'),
        ('5.|Austin이 기술', '이머전 DUV 로 어디까지 가나', _cds_litho(),
         ''),
    ],
    (PJ, 'strategy'): [
        ('1.', '무엇이 랙을 묶고 있나 — 순서가 뒤집힌다', _pj_order(),
         ''),
        ('3.|Yuen 이 꼽', '제약이 걸린 자리 셋', _pj_constraint(),
         '같은 세 자리를 두 줄로 그렸다.'),
        ('4.|레인당 200기', '같은 1.6테라비트를 채우는 세 구성', _pj_lanes(),
         '네모 하나가 레인 하나다. 전력·값은 전사에 없다.'),
        ('5.|더 멀리 가는', '한 줄 대 판', _pj_array(),
         '칸 수는 전사의 값이다.'),
        ('6.|분업 구조는', '광소자에도 팹리스', _pj_chain(),
         ''),
    ],
    (TD, 'strategy'): [
        ('2.|어려운 쪽은 그다음이다', '곱셈을 덧셈으로, 그리고 되돌아오기', _td_logflow(),
         '절감률은 전사에 없다.'),
        ('3.|모델이 한 칩에', '라우터 뒷면을 그대로 가져왔다', _td_fabric(),
         '가속기 수 72 는 쿼터랙 값이다(L277).'),
        ('5.|수치가 가장', '쿼터랙 대 풀랙', _td_rack(),
         '성능이 동급이라는 전제는 이 회차에 값이 없어 그리지 않았다.'),
        ('6.|이 회차에서 가장', '자기 손으로 하는 것과 맡긴 것', _td_outsource(),
         '엔지니어 60% 이상이 소프트웨어다(L343).'),
    ],
    (OP, 'strategy'): [
        ('1.|광트랜시버(빛과', '같은 트랜시버, 누가 무엇을 만드나', _op_module(),
         '같은 모듈을 두 줄로 그렸다. 부품 순서는 이 그림의 배치다.'),
        ('1.|주가가 어긋난', '광트랜시버 밸류체인 — 광원과 조립', _op_chain(),
         '끝에서 끝까지다.'),
        ('3.|금지가 곧', '되돌릴 수 있는 규제 앞의 갈림', _op_fork(),
         ''),
        ('6.|Austin은 같은', 'GPU 를 더 얻으려면 필요한 부품 넷', _op_finance(),
         '계약 금액은 판에 안 적었다.'),
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
         'Austin 의 산수다(L145).'),
    ],
    (JAL, 'strategy'): [
        ('1.|Vik의 결론은', '아홉 달을 만든 세 요인', _jal_nine_months(),
         '셋이 겹쳐 아홉 달이 됐다(L97). 사람과 백지는 전에도 있던 항이고 AI 도구만 새 항이라는 것이 이 절의 논지다. '
         '셋 중 무엇이 몇 할인지는 전사에 없어 상자 크기를 같게 뒀다.'),
        ('1.|설계 셈법도 달라진다', '주기가 짧으면 덜 욕심내도 된다', _jal_cycle(),
         '통상은 2~3년(L97)이라 무리해서 넣게 되고, 아홉 달이면 2세대가 이미 테이프아웃에 다가섰고 3세대를 구상 중이라(L95) 곧 다시 붙는다.'),
        ('2.|Austin이 본 것은', '잣대가 다른 이유 — 사이에 판매자가 있나', _jal_yardstick(),
         '위는 상용 실리콘이다 — 설계팀이 AI 랩·하이퍼스케일러에 팔고 그들이 사용자를 상대하니 잣대가 TCO 다(L45·L47). '
         '아래는 할라페뇨 — 설계팀과 사용자 사이에 판매자가 없어 요청당 에너지와 마지막 토큰까지 지연을 잣대로 삼는다(L43).'),
        ('3.|Vik은 균형을 잡아 뒀다', '투기적 디코딩 — 초안이 똑똑할수록 검증이 가볍다', _jal_specdec(),
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
         ''),
        ('6.|Jalapeño는 자사 모델만', '범용과 전용 사이 어디에 앉았나', _jal_spectrum(),
         '범용 GPU 의 논거는 모델 모양이 바뀌어도 하드웨어가 죽지 않는다는 것, 한 모델 전용은 Vik 이 말한 극단 코디자인이다(L83). 자리는 이 '
         '회차의 말이고 값은 없다.'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
