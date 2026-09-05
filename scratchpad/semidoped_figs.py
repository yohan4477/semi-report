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


FIGS = {
    (QC, 'strategy'): [
        ('1.', '손전화 쪽과 그 밖 쪽의 자리 바꿈', _qc_mix(),
         'CFO 자료의 도넛 셋이다. 회계연도 25 는 손전화가 3분의 2, 자동차와 IoT 가 3분의 1이었고, 2027 목표가 반반, 회계연도 29 목표는 자동차·IoT·데이터센터가 3분의 2다(L75·L77). '
         '기둥 높이는 이 분수 그대로다. 3분의 2 안에서 셋이 각각 얼마인지는 발표가 나누지 않았다.'),
        ('2.', '랙 하나로 채우던 것이 일별로 갈린다', _qc_disagg(),
         '예전에는 Blackwell GPU 와 Vera CPU 가 든 Nvidia 랙으로 채워야 했다. 지금은 CPU 랙을 따로 세우고, 저지연 디코드는 Cerebras 나 Groq LPU 랙에, '
         '메모리 대역폭이 넓은 퀄컴 추론 랙에 디코드만 맡기면서 프리필은 Nvidia GPU 에 남길 수 있다(L107). 늦게 온 회사가 디코드 하나만 겨냥하는 자리가 여기서 나온다(L109).'),
        ('3.', '옆에 붙일 것인가, 위에 얹을 것인가', _qc_hbc(),
         '옆에 붙이면 다이 한 변의 쇼어라인에 낼 수 있는 레인 수가 정해져 있어 2,000 레인이고 CoWoS 같은 고급 패키징 기판이 든다(L117·L119). '
         '위에 얹으면 칩 면 전체가 접점이 되어 레인이 수만에서 10만까지 늘고, 레인이 100배면 대역폭도 100배라는 것이 퀄컴의 계산이다(L119) — 제품 수치는 이 회차에 없다.'),
        ('3.|문제는 메모리 밑에', '메모리 밑에 무엇이 앉나 — 읽기 둘', _qc_read(),
         '진행자A 는 메모리 아래에 별도 로직 칩을 두고 소프트맥스 같은 원시 연산만 맡겨 뜨거운 XPU 위에 메모리를 안 얹는 구조로 읽었다(L135). '
         '진행자V 는 고급 패키징이 필요 없다고 한 말을 근거로 아래가 행렬 곱을 다 하는 온전한 XPU 여야 한다고 읽었고, d-Matrix Raptor 를 예로 들었다(L141·L149). '
         '근거는 발표 그림 하나뿐이다.'),
        ('4.', '층을 올리면 층당 용량이 뒤집힌다', _qc_tsv(),
         '한 층만 쓰면 메모리 층에 비아를 안 뚫어 밀도가 나온다. 두 층부터는 관통 실리콘 비아 둘레에 셀을 못 놓는 금지 구역이 생겨 층당 용량이 절반쯤으로 떨어지고, '
         '그래서 넷은 쌓아야 쓸모가 생긴다(L183·L185). 메모리 밑에 앉는 XPU 는 850제곱밀리미터쯤 되는 레티클급 다이라 평탄도와 열이 함께 걸린다(L161·L163).'),
        ('5.', '가속기 로드맵 — HBC 는 2027년부터', _qc_road(),
         'AI 100 은 오래전 물건이고 AI 200 은 2026년 샘플이지만 HBC 가 없다. HBC 1세대가 들어가는 것은 2027년 AI 250, 2세대는 회계연도 28 의 AI 300 이다(L193). '
         'AI 300 에 UALink 나 E-sun 같은 스케일업 패브릭과 구리·광 스케일아웃이 붙고 스케일업 CPO 는 그 뒤라 2029년쯤이 된다(L191·L205).'),
    ],
    (CB, 'strategy'): [
        ('2.', '자를 것인가, 그대로 둘 것인가', _cb_dice(),
         '통상은 웨이퍼 위 칩들을 잘라 내 하나씩 패키징하고 다시 통신을 붙인다 — 운이 좋으면 이어 붙이고 아니면 네트워크와 스위치까지 들어간다(L67·L73). '
         'Cerebras 는 자르지 않고 웨이퍼 위 금속 배선으로 이어 한 장을 칩 하나로 쓴다(L69). 레티클 84장이 한 장에 이어 붙는다(L77).'),
        ('2.|문제는 완벽한 웨이퍼가 없다는', '죽은 코어를 건너뛰는 순서', _cb_yield(),
         '코어 하나는 GPU 의 20분의 1에서 100분의 1 크기라 코어 단위 표면적이 작고, 그만큼 코어 단위 수율이 좋다(L81·L89). '
         '한 장에 코어가 97만쯤 들어가 그중 90만이 돌아간다(L83) — 상자로는 안 세고 순서만 그렸다. 결과가 SRAM 44기가바이트, 초당 21페타바이트다(L87).'),
        ('3.', '층 셋이 저마다 다른 숙제를 진다', _cb_stack(),
         '웨이퍼 하나가 23킬로와트를 먹어 1볼트면 수만 암페어가 흐르는데 한쪽 커넥터로는 12인치 건너까지 못 보낸다(L109). '
         '그래서 수백 지점에 위에서 수직으로 꽂고(L111), 엔진 블록의 미세 유로가 전면을 한꺼번에 식힌다(L113). '
         '열을 받으면 웨이퍼는 10분의 1밀리미터 늘어나는데 기판은 안 늘어나 정렬이 어긋난다(L119) — 커넥터 개수는 전사에 없어 안 그렸다.'),
        ('4.', '44기가바이트 안과 밖', _cb_wall(),
         '모델이 44기가바이트 안에 들어가면 GPU 로는 못 내는 초당 토큰이 나온다(L137). 넘으면 웨이퍼 여러 장에 쪼개야 하는데 '
         '네트워킹은 칩 한쪽 끝으로만 나가고 웨이퍼 안 데이터 이동보다 훨씬 느리다(L139). 병렬 셋은 진행자V 가 든 우회로 그대로다(L145). '
         '셋 다 웨이퍼 사이 통신에 기대니 웨이퍼 스케일의 기본 발상과 어긋난다(L147).'),
        ('5.', '같은 발상, 40년 뒤', _cb_forty(),
         'Gene Amdahl 이 1980년대에 2억 3천만 달러를 모아 2.5인치 웨이퍼로 같은 일을 하려 했고 결함 우회라는 해법까지 같았다(L175·L177). '
         '막은 것은 그 시절 수율이다. 1982년 폭풍이 공장을 잠기게 했고 1983년 제품 없이 상장했으며 1989년 Amdahl 이 물러났다(L179·L181·L185). '
         '진행자V 가 센 간격이 40년이다(L187).'),
        ('6.', '하드웨어를 안 파는 하드웨어 회사', _cb_chain(),
         'OpenAI 는 웨이퍼 스케일 엔진을 사지 않고 연산 시간과 토큰에 돈을 낸다(L251). 그러면 제조와 공급망은 물론 데이터센터 건설과 클라우드 운영과 토큰 공급까지 전부 Cerebras 몫이다(L253). '
         '진행자V 가 물은 자리가 여기다 — 왜 복잡한 칩을 만들면서 신생 클라우드까지 해야 하나(L257).'),
    ],
    (LI, 'strategy'): [
        ('1.|숫자를 붙이면', 'EUV 장비 값의 계단', _li_toolcost(),
         '낮은 개구수 장비 2억 5천만 달러, 높은 개구수 4억 달러, 하이퍼 개구수는 6억에서 8억 달러이고 10억 달러까지 갈 수 있다(L78·L80). 팹 하나에 이런 장비 열다섯 대쯤이 들어가고 새 팹 한 채는 200억에서 300억 달러다(L80).'),
        ('2.|193나노미', '멀티패터닝 — 두 번 그어 간격을 반으로', _li_multipattern(),
         '10야드마다밖에 못 긋는 기계로 5야드 선을 그리려면 10·20·30·40 을 긋고 기계를 5야드 옮겨 5·15·25·35 를 다시 긋는다(L138~L142). 새 기계를 사지 않는 대신 단계가 두 배, 처리량이 절반이다(L144).'),
        ('3.|13.5나노', '주석 방울에서 웨이퍼까지', _li_lightpath(),
         '50마이크로미터 주석 방울이 떨어지는 것을 레이저로 두 번 때려 13.5나노미터 빛을 만들고(L184), 거울 열세 장을 거쳐 초점을 잡는다(L186). 웨이퍼에 닿는 빛은 한 자릿수 퍼센트에도 못 미치고, 피할 길은 없다는 것이 진행자V 의 지금까지 생각이다(L188).'),
        ('4.|파장은 20년', '하프 필드 — 같은 꼴 두 판', _li_halffield(),
         '개구수 0.33 에서 0.55 로 올리면 피처는 1.5~1.7배 작아지지만 한 번에 찍는 면적은 절반이 된다(L212). 2억 5천만 달러 장비가 찍던 면적을 4억 달러 장비가 절반만 찍는다(L214). ASML 의 답은 스캐너를 더 빨리 움직이는 것이었다(L216).'),
        ('5.|떼어 내면 셈이', '광원 하나로 스캐너 열 대', _li_fel(),
         '자유전자레이저는 총출력이 높아 빔을 쪼개면 스캐너 열 대를 광원 하나로 먹일 수 있다(L240). 광원은 xLight 가 세우고 자본지출을 지며 팹은 빛을 산다(L258·L260). 출력·요금 값은 전사에 없고 칸 수만 값이다.'),
    ],
    (AP, 'strategy'): [
        ('2.|여기서 앞뒤가', '다이는 레티클을 못 넘는데 패키지는 3.3배', _ap_reticle(),
         '다이 하나는 레티클 한 장 858제곱밀리미터(26 × 33밀리미터)를 넘지 못한다(L135·L159). 패키지는 레티클 3.3배까지 커진다(L161). 그 사이를 메우는 것이 첨단 패키징이다.'),
        ('3.|CoWoS 는 세 층', 'CoWoS 세 갈래 — 가운데 층만 다르다', _ap_cowos(),
         '같은 세 층을 세 벌 그렸다. CoWoS-S 는 실리콘 인터포저를 TSV 로 관통시켜 다 깔고(L205), R 은 금속 두세 층의 유기 RDL 로 싸게 깔고(L211), L 은 유기 층 안에 실리콘 브리지를 필요한 데만 심는다(L217). S 의 크기 상한이 레티클 3.3배다(L227·L229).'),
        ('4.|EMIB(기판 안', 'CoWoS-L 세 층 대 EMIB 두 층', _ap_emib(),
         '인텔 EMIB 는 브리지를 기판 안에 심어 가운데 층을 없앴다(L267). 값은 없는 그림이다 — 층의 수만 견준다.'),
        ('4.|여기서 나오는 ', '원형 웨이퍼와 사각 패널', _ap_panel(),
         '300밀리미터 원형 웨이퍼에서 큰 사각형을 떼면 가장자리를 버리는데, 500 × 500밀리미터 사각 패널은 넓이가 웨이퍼의 다섯~여섯 배다(L257·L261). 같은 자로 그렸고 버리는 비율은 전사에 없다.'),
        ('7.|Vik 이 마지막에', '레티클 배수 로드맵 — CoWoS 와 EMIB', _ap_roadmap(),
         'CoWoS 는 3.3배에서 5.5배(Blackwell Ultra·Rubin), 9.5배, System on Wafer 40배로 간다(L347). EMIB 는 EMIB-T 8배에서 2028년 12배 넘게, 120 × 180밀리미터다(L357). 점선은 아직 안 나온 것이다.'),
    ],
    (WK, 'strategy'): [
        ('1.|Val 은 저장장치를', 'NVLink 레인 128 대 PCI 레인 32', _wk_lanes(),
         '같은 꼴 두 줄이다. Nvidia 서버의 스케일업 구간은 NVLink 레인이 128개쯤(Val 의 기억), 마더보드에서 CPU 가 DRAM 으로 가는 PCI 는 32개다(L47). 그래서 망을 최대 속도로 쓰면 DRAM 보다 빨라진다는 것이 Val 의 산수다(L45).'),
        ('3.|압축 이야기는', 'KV 캐시 — 단위는 90% 줄고 총량은 100배', _wk_kv(),
         '10만 토큰에 50GB 들던 KV 캐시가 DeepSeek V4 식 최적화로 5GB 가 됐다(L77). 그런데 컨텍스트가 10배, 동시 세션이 10~100배가 되어 총량은 순 100배다(L77). 제번스 역설이 다시 걸린다는 것이 Val 의 말이다(L85).'),
        ('4.|먼저 메모리 계층을', 'Dynamo 의 메모리 네 층', _wk_tiers(),
         'Nvidia Dynamo 팀이 정리한 네 층이다(L69). 층 사이의 지연과 대역폭이 자릿수로 벌어져 그랜드캐니언처럼 끊긴다(L71). 사람 눈은 초당 35~50토큰을 요구하고 에이전트 스웜은 초당 수천 토큰을 뽑아 간다.'),
        ('4.|그러면 캐시 적중률은', '캐시 적중률 둘 — 논리와 실제', _wk_hit(),
         '같은 꼴 둘이다. 대시보드의 논리 적중률은 내 토큰이 재사용될 수 있는 비율이라 95% 근처로 높다(L107). 사업자가 실제로 맞히는 비율은 가진 메모리 계층에 달렸고, 스토리지 계층을 붙이면 응답 목표가 무너져 인기 모델에는 잘 안 쓴다(L109).'),
        ('5.|값을 치르는 자리는', '여유분 — 1페타바이트 사서 300~500테라바이트', _wk_provision(),
         'SLC 를 못 쓰고 TLC 나 QLC 로 버티면 드라이브가 망가지지 않게 여유 용량을 크게 잡아야 한다. 1페타바이트를 사서 전기까지 넣고도 실제로 쓰는 것은 300~500테라바이트다(L137). 짙은 조각은 그 범위의 위쪽 값이다.'),
    ],
    (MT, 'strategy'): [
        ('1.|가장 또렷한 숫자는', '설비투자 1,900억 달러 안의 250억', _mt_capex(),
         '마이크로소프트의 2026년 설비투자 1,900억 달러 중 250억 달러가 부품값 상승분이라고 최고재무책임자가 밝혔다(L221). 몇 년 전에는 한 분기 설비투자 전체가 250억 달러였다(L223). 막대 길이가 값이다.'),
        ('1.|진행자A는 연산을 더', '설비투자가 돌아오는 고리 — 닫히는 쪽과 안 닫히는 쪽', _mt_loop(),
         '같은 폭 두 줄이다. 설비투자가 가속기로 가면 사용자가 더 나은 도구를 쓰고 매출로 돌아와 고리가 닫힌다. 메모리 회사로 흘러 나가면 돌아오는 것이 없다는 것이 진행자V 의 걱정이다(L105). 그래서 「메모리세」다(L111).'),
        ('2.|삼성전자 실적에서', '삼성 HBM 점유율 — 전과 후', _mt_share(),
         '여섯 분기쯤 전 40% 수준이던 삼성의 HBM 점유율이 2025년 13~20% 대로 떨어졌다(L81). 오른쪽 막대는 그 범위의 위쪽 값으로 그렸다. 새 규격 HBM4 가 잃은 자리를 되찾을 기회다.'),
        ('2.|진행자V는 그 주장이', '핀당 속도 — 규격과 실제', _mt_pin(),
         'HBM4 의 JEDEC 규격은 핀당 초당 8기가비트인데, 추론 성능과 와트당·달러당 토큰을 두고 다투는 통에 공급사들이 10·11·12까지 밀어 올리고 있다(L89). 규격을 넘어선 이 경쟁이 판매와 고착을 만든다는 것이 진행자V 의 말이다.'),
        ('3.|샌디스크의 이번 분기', '샌디스크 매출총이익률 — 전과 후', _mt_margin(),
         '앞 분기 51.1%(L157)에서 이번 분기 78.4%(L155)로, 다음 분기 가이던스는 80% 위(L161). 엔비디아가 75% 안팎(L165). 비트를 더 실어 보낸 것이 아니라 가격 인상이라는 것이 진행자V 의 말이다(L157).'),
        ('5.|세 흐름을 나란히', '세 흐름을 이으면 고리가 된다', _mt_cycle(),
         '① 부품값 인상분이 설비투자에 얹혀 메모리·저장장치 회사로 ② 부족 탓에 기업 고객이 클라우드로 들어와 하이퍼스케일러 매출이 늘고 ③ 자체 가속기로 아낀 돈이 다시 메모리 값으로(L227·L229·L251·L255). 진행자V 는 이 고리를 우스운 순환이라 불렀다.'),
    ],
    (PW, 'strategy'): [
        ('1.', '랙 하나가 먹는 전력', _pw_racks(),
         '클라우드 시대 랙은 20킬로와트, 지금 AI 가속기 랙은 100~120킬로와트, 카이버 세대 루빈 울트라는 600킬로와트, 다음은 1메가와트다(L107·L109). '
         'AI 이전 랙이 10~15킬로와트였으니 백 배다(L109). 막대 높이가 킬로와트고 「지금」은 범위의 위쪽 값으로 그렸다.'),
        ('4.', '전압을 어디서 낮추나', _pw_vertical(),
         '광통신에서 빛을 칩 가까이까지 끌고 가듯 전력도 고전압인 채로 칩 가까이까지 간다(L173). 멀리서 낮추면 낮은 전압이 긴 구리를 지나며 손실이 붙는데, '
         'Austin 이 든 리니어 플러거블의 긴 구리 트레이스가 같은 자리다(L177). 800볼트를 그 자리에서 바로 1볼트로 바꾸는 것은 아니고 사이에 여러 단계가 남는다(L175).'),
        ('2.|전력 쪽 병목은', '같은 600킬로와트를 48볼트로, 800볼트로', _pw_current(),
         '같은 꼴 둘이다. 전력은 전압 곱하기 전류라 600킬로와트를 48볼트로 보내면 12,500암페어, 800볼트로 보내면 750암페어가 흐른다(L137·L153). 손실은 전류의 제곱을 따르니 그 차이가 100~200배라는 것이 Vik 의 셈이다(L163).'),
        ('5.|전체 사슬을', '발전소에서 GPU 까지 전압이 바뀌는 자리', _pw_chain(),
         '발전소의 수백 킬로볼트가 변전소에서 10~30킬로볼트, 유틸리티룸에서 400~430볼트 삼상, 랙 전원장치에서 48볼트 직류, 중간 버스 컨버터에서 12볼트, VRM 에서 1볼트 안팎으로 내려온다(L191·L193·L195). 자리마다 다른 회사가 서고 VRM 이 개수가 가장 많다.'),
        ('6.|정작 어느', '800볼트 다음의 두 갈래', _pw_fork(),
         '① 있던 48볼트 설비를 그대로 쓰며 48·12·1볼트로 내려가는 길과 ② 6볼트로 바로 가는 길(TI·Navitas)이 갈린다(L215). 어느 쪽이 서는지는 아직 정해지지 않았다는 것이 Vik 의 말이다.'),
    ],
    (CX, 'strategy'): [
        ('1.', '마벨이 파는 것 — 거리만 다르다', _cx_marvell(),
         '진행자V 는 마벨의 사업을 데이터 이동 하나로 묶었다 — 칩 안에서는 ASIC, 칩 사이에서는 인터커넥트, 데이터센터 사이에서는 DSP 다(L119). '
         '이번 키노트는 매출 대부분이 인터커넥트에서 나온다는 것을 보이며 연결 회사 쪽에 무게를 실었다(L113). '
         'XPU 를 만들어 주는 고객에게 인터커넥트를 얹어 파는 이야기는 하지 않았다(L115·L117).'),
        ('2.|막힌 곳은 둘이다', 'CPO 가 랙 안으로 못 들어오는 이유 둘', _cx_cpo_blocks(),
         '같은 꼴 두 기둥이다. 수율은 엔지니어링 샘플 99% 까지만 확인됐고(L127) 수백만 개 양산에서도 그런지는 아직 모른다. 검사는 웨이퍼 위아래를 동시에 맞춰야 하는데 빠른 장비가 아직 없다(L129). 99% 는 Vik 이 전한 수다.'),
        ('3.|XPO 모듈은', '빛으로 가는 길 넷 — 칩에 얼마나 가까운가', _cx_optics_ways(),
         '플러그형에서 OSFP 여덟을 하나로 합친 XPO(L141), 소켓에 꽂는 NPO(L131), 패키지 위에 붙이는 CPO 순으로 광 엔진이 칩에 가까워진다. 이 회차의 물음은 CPO 가 랙 안(스케일업)까지 들어오느냐다(L125).'),
        ('4.|전압 변환 칩을', '전압 구간마다 소재가 다르다', _cx_voltage(),
         '리테온 부스의 답과 영상이 같은 구조다(L177·L183). 중전압 배전망에서 800볼트로 내리는 칩은 실리콘카바이드, 변압기로 48볼트까지도 실리콘카바이드, 그 아래 12볼트나 6볼트로 가는 변환은 전부 실리콘이다. GaN 은 「아직 이르다」.'),
        ('5.|버티브 부스에는', '조립식 인프라 블록 — 전과 후', _cx_prefab(),
         '전에는 냉각·전원 설비를 현장에서 짓고 랙을 넣었다. 조립식 블록은 설비를 갖춘 컨테이너에 랙만 밀어 넣고 연결하면 끝난다(L193·L197). 배치 시간이 절반으로 준다는 것은 델타 부스 담당자의 말이고(L199), 판 위에 시간 값은 없다.'),
        ('6.|인텔 키노트의', '클리어워터포레스트 칩렛 열일곱', _cx_chiplets(),
         '아래 줄이 인텔7 I/O 다이 둘과 인텔3 액티브 베이스 다이 셋, 그 위에 인텔18A 컴퓨트 다이 열둘이 포베로스 다이렉트 3D 로 쌓인다(L219·L221). I/O 는 이전 세대 것을 재사용했고 최신 공정은 연산 코어에만 썼다(L227). 칸 수가 값이다.'),
    ],
    (GF, 'strategy'): [
        ('1.|Barber가 ', '레인 속도별 구리가 가는 거리', _gf_reach(),
         '막대 길이가 미터다. 레인당 100기가비트에서 2미터, 200기가비트에서 1미터, 400기가비트에서 반 미터(L81). 점선이 랙 하나 높이라, 200기가비트부터 스위치를 랙 가운데로 내려야 하고 400기가비트에서는 그 수도 안 먹힌다.'),
        ('1.|문제는 이 대응', '속도가 오르면 왜 광으로 가나', _gf_chain(),
         '레인 속도가 두 배 오르면 구리가 가는 거리가 절반이 되고, 스위치를 랙 가운데로 내리는 수는 랙 높이가 바닥이라 한 번뿐이다(L81). 그다음은 광이다.'),
        ('2.|수요가 이렇게 ', '200mm 에서 300mm 로 — 전과 후', _gf_wafer(),
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
         '같은 네 궤적을 두 판에 그렸다. 왼쪽은 0 으로 읽을 아래와 1 로 읽을 위 사이에 틈이 있고(L73·L75), 오른쪽은 궤적이 시간(지터)과 전압에서 흔들려 그 틈이 메워졌다. 값은 없는 그림이다 — 파형을 천 장쯤 겹쳐 그리면 이 모양이 된다는 것이 Austin 의 설명이다(L77).'),
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
        ('1.', '설비투자 값을 누가 매기나', _cds_pricing(),
         '여태 하이퍼스케일러는 영업으로 번 현금으로 랙을 샀고 설비투자의 타당성은 이사회가 판단했다(L31·L33). '
         '잉여현금흐름이 바닥나면서 부채와 부외 특수법인으로 옮겨 가자(L33) 그 판단을 채권 투자자가 대신하고, CDS 프리미엄과 스프레드로 매일 찍힌다(L37·L39·L41). '
         '프리미엄이 오르면 빌리는 값도 비싸진다(L37).'),
        ('3.', '좋은 숫자가 나쁜 사건이 되는 경로', _cds_expect(),
         'SK하이닉스는 매출이 전년 대비 257% 늘고 영업이익은 6배 넘게, 영업이익률은 76%까지 올랐는데 시장 기대에는 못 미쳤다(L57·L59). '
         '서울 상장 주식이 하루에 20% 빠졌고 코스피 전체를 끌어내렸다(L59). Vik 은 원인을 수요가 아니라 보유 구조에서 찾았다 — 한 나라에서 한 종목에 몰리고 레버리지를 쓴 자리다(L71).'),
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
        ('1.', '무엇이 랙을 묶고 있나 — 순서가 뒤집힌다', _pj_order(),
         'Yuen 은 레인당 초당 200기가비트에서 구리 도달거리가 3~4미터쯤으로 줄었다고 말한다(L53). 랙 밖으로 정보를 못 빼니 GPU 를 랙 안에 더 채우게 되고 그래서 랙이 더 뜨거워진다는 순서다(L53). '
         '흔히 읽는 순서는 그 반대다 — 랙이 뜨거워서 못 늘린다. 어느 쪽을 출발점으로 두느냐에 따라 광소자가 선택 품목인지 필수 부품인지가 갈린다.'),
        ('3.|Yuen 이 꼽', '제약이 걸린 자리 셋', _pj_constraint(),
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
        ('1.|Vik의 결론은', '아홉 달을 만든 세 요인', _jal_nine_months(),
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
