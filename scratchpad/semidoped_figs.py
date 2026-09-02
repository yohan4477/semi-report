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
# 값은 전사에 있는 것만 — 아홉 달·671B·120B·1,000토큰·700W·1,200W·8K/1K·HBM4/HBM3E.
# 상자 개수는 글이 가른 항의 수와 같다(요인 셋·잰 것 셋·못 잰 것 셋·공급망 세 단).

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
    # 요인 셋(위) → 아홉 달(아래). 셋이 겹쳐 그 값이 났다는 것이라 화살표 셋이 한 상자로 모인다
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


def _jal_measured():
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '잰 것') + head(R, 22, 248, '못 잰 것')
    # 열 하나는 248 이다. 한 줄 15자(234px)를 넘기면 옆 열을 침범한다
    left, lw, ly = _col(L + 12, 36, [(['중형 R1 671B', '새 파레토 프런티어'], 'fig-agent'),
                                      (['소형 GPT-OSS 120B', '초당 1,000토큰'], 'fig-agent'),
                                      (['700W TDP', 'GB200 약 1,200W'], 'fig-agent')])
    right, rw, ry = _col(R + 12, 36, [(['짧은 컨텍스트', '8K 입력 · 1K 출력'], 'fig-outside'),
                                       (['에이전틱', 'AgentX 아직 없음'], 'fig-outside'),
                                       (['세대 차', 'HBM4 대 HBM3E'], 'fig-outside')])
    parts += left + right
    parts += legend([('fig-agent', '잰 값'), ('fig-outside', '아직 없는 값')], max(ly, ry) + 18)
    return svg(max(ly, ry) + 44, parts,
               '잰 것 셋(R1 파레토·GPT-OSS 초당 1,000토큰·700W)과 못 잰 것 셋(짧은 컨텍스트·에이전틱·HBM 세대 차)을 나란히 둔다')


def _jal_rule_pair():
    # 두 기둥. 위가 잣대, 아래가 그 잣대가 낳은 칩의 꼴
    L, R = 0.0, 272.0
    parts = head(L, 22, 248, '상용 실리콘 벤더') + head(R, 22, 248, '할라페뇨')
    a = ['잣대: TCO', '사고 굴리는 비용 전부']
    b = ['잣대: 요청당 에너지', '마지막 토큰까지 지연']
    aw, bw = w_of(a), w_of(b)
    parts += box(L + (248 - aw) / 2, 36, aw, 2 * LH + 22, a, 'fig-stage')
    parts += box(R + (248 - bw) / 2, 36, bw, 2 * LH + 22, b, 'fig-stage')
    y2 = 36 + 2 * LH + 22 + 34
    c = ['프리필 칩 · 디코드 칩 분리', '비율이 바뀌면 한쪽이 논다']
    d = ['균형 단일 칩', '안 쓰는 부분만 끈다']
    cw, dw = w_of(c), w_of(d)
    parts += box(L + (248 - cw) / 2, y2, cw, 2 * LH + 22, c, 'fig-bad')
    parts += box(R + (248 - dw) / 2, y2, dw, 2 * LH + 22, d, 'fig-agent')
    parts += vline(L + 124, 36 + 2 * LH + 24, y2 - 2) + vline(R + 124, 36 + 2 * LH + 24, y2 - 2)
    return svg(y2 + 2 * LH + 36, parts,
               '왼쪽은 TCO 잣대가 프리필·디코드 분리 칩으로, 오른쪽은 요청당 에너지·마지막 토큰 지연 잣대가 균형 단일 칩으로 이어진다')


def _jal_chain():
    row, _x = band([(['HBM', 'Samsung'], 'fig-outside'), ('>', ''),
                    (['스위치', 'Broadcom'], 'fig-agent'), ('>', ''),
                    (['시스템', 'Celestica'], 'fig-outside')], 30, 72)
    parts = row + legend([('fig-agent', '사실 — 발표자가 호명'), ('fig-outside', '추정')], 126)
    return svg(150, parts,
               'HBM(Samsung) → 스위치(Broadcom) → 시스템(Celestica) 세 단 중 사실로 확인된 것은 스위치 하나다')


JAL = '2026-08-27-openai-jalapeno'

# ── 도해 ─────────────────────────────────────────────────────────────
# FIGS[(slug, lane)] = [(절 제목 머리, 제목, svg, 캡션), …]
FIGS = {
    (JAL, 'strategy'): [
        ('1.', '아홉 달을 만든 세 요인', _jal_nine_months(),
         '요인 셋이 겹쳐 첫 RTL 에서 테이프아웃까지 아홉 달이 걸렸다(L97). AI 도구는 발표자 말을 Vik 이 전한 것(L177), '
         '백지 설계는 Richard 말을 Austin 이 전한 것(L171)이다. 셋 중 무엇이 몇 할인지는 전사에 없어 상자 크기를 같게 뒀다.'),
        ('2.', '잰 것과 못 잰 것', _jal_measured(),
         '왼쪽 셋이 InferenceX 에서 나온 값이고(L103·L105·L111), 오른쪽 셋이 아직 없는 값이다(L63·L61·L103). '
         '오른쪽이 채워지기 전까지 왼쪽은 「쉬운 조건에서 이긴 결과」일 수 있다.'),
        ('3.', '잣대가 칩의 꼴을 정한다', _jal_rule_pair(),
         '두 기둥이 한 쌍이다. TCO 를 잣대로 삼으면 프리필·디코드를 나눠 한쪽을 놀리는 설계가 나오고(L45·L155), '
         '요청당 에너지를 잣대로 삼으면 한 칩에 다 넉넉히 두고 안 쓰는 부분만 끄는 균형 단일 칩이 나온다(L43·L157).'),
        ('4-2', '공급망은 어디부터 사실인가', _jal_chain(),
         '세 단 중 실선은 발표자가 감사 인사에서 직접 호명한 Broadcom 하나다(L115). Samsung HBM 우위는 Vik 이 「entirely speculative」라 못 박은 추정(L117), '
         'Celestica 는 SemiAnalysis 추정을 Austin 이 전한 것이다(L119).'),
    ],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
