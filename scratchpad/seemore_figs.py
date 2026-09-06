# -*- coding: utf-8 -*-
"""채널 씨모어 판에 끼우는 도해.

열쇠는 (slug, lane), 값은 `[(절 제목 머리, 제목, svg, 캡션)]`. 절 제목 머리는 판
(insights/seemore/<slug>-<lane>.md)의 `## ` 제목이 그 문자열로 시작하는 절이다
(「## 3. (대비) …」면 '3.'). `gen_seemore.body_html` 이 그 제목 바로 아래, 본문보다
**앞에** 그림을 세운다.

붓과 판 폭은 Semi Doped 장과 같다(`aie_figs`). 색은 회색만 쓰고 좌표는 사람이 안
찍는다 — `table` 이 글자 폭으로 잰다. 그림 글자에 든 값이 전사에 있는지는
`missing_values` 가 보고, 배치가 겹치는지는 `check_fig.hits` 가 본다.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aie_figs import W, LH, box, head, svg, table  # noqa: E402
from semidoped_figs import CSS, fig_html, values  # noqa: F401,E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'content', 'understanding', '채널 씨모어', 'raw')


def missing_values(slug, svg_):
    """전사에 없는 값. 전사가 없으면 값 전부를 돌려준다 — 대조 못 한 것은 못 찾은 것이다."""
    path = os.path.join(RAW, slug + '.md')
    if not os.path.exists(path):
        return sorted(values(svg_))
    src = re.sub(r'[\s,]', '', io.open(path, encoding='utf-8').read())
    return sorted(n for n in values(svg_) if n.replace(',', '') not in src)


def _table(specs, clss, heads, arrows=True):
    parts, h = table(specs, clss, heads, arrows=arrows)
    return parts, h


def spans(stages, rows, bar=None, gap=6, y0=30):
    """공정을 칸으로 깔고, 그 아래에 누가 어디부터 어디까지 덮는지를 박스로 잡는다.

    stages = ['R&D', '임상', …]  칸 이름. 폭은 판을 칸 수로 나눠 고르게 준다.
    rows   = [(첫 칸, 끝 칸, 줄들)]  끝 칸은 포함이다. 한 줄에 겹치는 구간을 두지 않는다.
    bar    = 판 전체를 덮는 한 줄. 여러 칸에 걸친 주체(빅파마)를 여기에 둔다.

    좌표를 손으로 안 찍는다 — 칸 폭도 구간 폭도 판 폭에서 나온다."""
    n = len(stages)
    cw = (W - gap * (n - 1)) / n
    def x(i):
        return i * (cw + gap)
    out = []
    for i, s in enumerate(stages):
        out += head(x(i), y0 - 10, cw, '')
        out += box(x(i), y0, cw, 34, [s], 'fig-stage', 'fig-st')
    y = y0 + 34 + 14
    rh = max(len(r[2]) for r in rows) * LH + 26
    for a, b, lines in rows:
        out += box(x(a), y, x(b) + cw - x(a), rh, lines)
    y += rh
    if bar:
        y += 12
        out += box(0, y, W, len(bar) * LH + 24, bar, 'fig-agent')
        y += len(bar) * LH + 24
    return out, y


# ── 2026-08-16 밸류체인 편 ────────────────────────────────────────────

_B, _S, _P = 'fig-box', 'fig-stage', 'fig-agent'

_p, _h = spans(
    ['R&D', '임상', '허가', '생산', '판매'],
    [(0, 0, ['바이오텍', '물질을 판다']),
     (1, 2, ['CRO', '대행 수수료']),
     (3, 3, ['CDMO', '만든 양만큼']),
     (4, 4, ['도매상과', 'PBM', '통과 여부'])],
    bar=['빅파마 — 사 와서 팔고, 특허가 풀리면 밀린다'])
FIG_CHAIN = ('1.', '다섯 칸과 그 칸을 덮는 회사',
             svg(_h + 10, _p, '신약이 지나는 다섯 단계와 각 단계를 덮는 회사'),
             '한 칸을 덮는 회사는 그 칸에서만 번다. CRO 만 임상과 허가 두 칸에 걸치고, '
             '빅파마는 칸을 사서 덮는다.')

_p, _h = _table(
    [(['1상'], ['이 약이 안전한가']),
     (['2상'], ['효과가 있는가']),
     (['3상'], ['기존 약보다 우수한가'])],
    [_S, _B], ['단계', '묻는 것'])
FIG_PHASE = ('3.', '단계마다 묻는 것이 다르다',
             svg(_h + 10, _p, '임상 1상 2상 3상이 각각 무엇을 묻는지'),
             '사람 수로 나뉘는 것이 아니다. 값을 정하는 관문은 이미 팔리는 약과 겨루는 3상이다.')

_p, _h = _table(
    [(['신약'], ['원본'], ['특허로 보호']),
     (['제네릭'], ['화학의약품'], ['단가 싸움']),
     (['바이오시밀러'], ['바이오의약품'], ['기술 과점'])],
    [_S, _B, _B], ['갈래', '무엇을 복제', '겨루는 방식'], arrows=False)
FIG_COPY = ('6.', '같은 「복제」인데 싸움이 다르다',
            svg(_h + 10, _p, '신약 제네릭 바이오시밀러가 각각 무엇을 복제하고 어떻게 겨루는지'),
            '한 낱말로 묶으면 이익률의 방향을 반대로 읽는다.')


# ── 2026-09-06 병목 편 ────────────────────────────────────────────────

_p, _h = _table(
    [(['후보 물질'], ['4~5년에서 1년으로']),
     (['임상'], ['안 줄어듦']),
     (['허가'], ['안 줄어듦']),
     (['생산'], ['안 줄어듦']),
     (['유통'], ['안 줄어듦'])],
    [_S, _B], ['칸', '걸리는 시간'])
FIG_SPEED = ('1.', '빨라진 것은 첫 칸뿐이다',
             svg(_h + 10, _p, '밸류체인 다섯 칸 가운데 후보 물질 단계만 빨라지고 나머지는 그대로다'),
             '앞 칸만 빨라지면 산출물이 다음 칸 앞에 쌓인다. 값은 뒤로 밀린다.')

_p, _h = _table(
    [(['임상'], ['첫 병목'], ['보유 중']),
     (['생산'], ['판단 유보'], ['안 삼']),
     (['유통'], ['전통적 병목'], ['재매수'])],
    [_S, _B, _P], ['자리', '판단', '계좌'], arrows=False)
FIG_BOTTLE = ('2.', '세 자리를 서로 다르게 다뤘다',
              svg(_h + 10, _p, '임상 생산 유통 세 자리에 대한 판단과 실제 매매'),
              '기준은 하나다. 물량이 늘 때 새 공급자가 붙을 수 있는가.')

_p, _h = _table(
    [(['파이프라인'], ['후보 물질과 최적화']),
     (['임상 성공'], ['허가받아 출시']),
     (['블록버스터'], ['연매출 10억 달러']),
     (['특허 만료'], ['복제약이 붙음']),
     (['특허 절벽'], ['수익성 급락'])],
    [_S, _B], ['자리', '일어나는 일'])
FIG_CYCLE = ('4.', '한 바퀴가 도는 순서',
             svg(_h + 10, _p, '파이프라인에서 블록버스터를 거쳐 특허 절벽까지 도는 순서'),
             '값을 정하는 것은 지금 어디에 서 있느냐가 아니라 다음 바퀴가 준비돼 있느냐다.')


FIGS = {
    ('2026-08-16-pharma-valuechain', 'strategy'): [FIG_CHAIN, FIG_PHASE, FIG_COPY],
    ('2026-09-06-pharma-bottleneck', 'strategy'): [FIG_SPEED, FIG_BOTTLE, FIG_CYCLE],
}


def figs_for(slug, lane):
    return FIGS.get((slug, lane), [])
