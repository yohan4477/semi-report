# -*- coding: utf-8 -*-
"""체인 도해 — 마디를 가로로 잇고, 원문이 병목이라 지목한 마디만 짙게 한다.

정본 하나가 도해 하나다. 판은 `fig_layout.Plate` 가 세운다 — 사슬 도해는 마디가 셋에서
열까지 들쭉날쭉해서 좌표를 손으로 찍으면 반드시 어긋난다(도해 규칙 2).

  마디가 다섯을 넘으면 줄을 접는다. 판 폭 520 에 일곱을 늘어놓으면 한 칸이 60px 라
  「우라늄 농축」이 안 들어간다. 접은 자리는 줄 끝에서 다음 줄 머리로 잇는다.

  회사는 마디 상자 **안**에 깔린다. 판 위에 얹지 않는다(규칙 3). 상자 안 글자는
  그 마디가 하는 일이라 포함 관계가 맞다.

  색은 회색만 쓴다(확정 규칙). 병목은 색이 아니라 **테두리 굵기와 바탕 톤**으로 낸다 —
  `.fl-bh` 를 이 장에서만 회색으로 덮는다. 무엇이 짙은지는 판 아래 범례가 말한다.

  **개수는 값이다.** 마디 수도 회사 수도 원문이 말한 것뿐이다. 빈자리를 채우려고
  상자를 더 놓지 않는다.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import fig_layout as fl  # noqa: E402

PER_ROW = 4          # 한 줄에 놓는 마디 수. 판 폭 520 에서 이보다 늘리면 이름이 잘린다
MAX_CO = 4           # 상자 안에 이름을 다 적을 회사 수. 넘으면 「외 N」으로 줄인다

CSS = '''
.uc-fig svg.chain .fl-bh{fill:var(--ink-6,#eceef2);stroke:var(--ink-2);stroke-width:2.2}
.uc-fig svg.chain .fl-note{font-size:13px;fill:var(--ink-3)}
'''


def _co_text(stage):
    """마디 상자 안에 깔 회사 이름. 원문이 댄 이름만, 넷까지 적고 나머지는 수로 남긴다."""
    names = [c.get('name', '').strip() for c in (stage.get('companies') or [])]
    names = [n for n in names if n]
    if not names:
        return ''
    if len(names) <= MAX_CO:
        return ' · '.join(names)
    return ' · '.join(names[:MAX_CO]) + ' 외 %d' % (len(names) - MAX_CO)


def chain_svg(canon, width=520.0, per_row=PER_ROW):
    """정본 하나를 사슬 판으로 굽는다. (svg, 병목 마디 수)

    한 줄에 몇을 놓을지는 이름 길이가 정한다 — 「우라늄 농축(HALEU)」처럼 긴 이름이
    섞인 사슬은 넷이 안 들어간다. 넷으로 놓아 보고 판을 넘으면 셋, 둘로 줄인다.
    사람이 사슬마다 눈으로 정하면 새 정본이 들어올 때마다 다시 손봐야 한다."""
    for n in range(per_row, 1, -1):
        try:
            return _plate(canon, width, n)
        except AssertionError:
            continue
    return _plate(canon, width, 1)


def _plate(canon, width, per_row):
    stages = canon.get('stages') or []
    p = fl.Plate(width, subout=True, keep_cols=True, wrap_label=True)
    rows = [stages[i:i + per_row] for i in range(0, len(stages), per_row)]
    # 뱀 꼴로 접는다. 둘째 줄을 다시 왼쪽부터 놓으면 줄을 잇는 선이 오른쪽 끝에서 왼쪽
    # 끝까지 가로질러 그 줄 상자를 전부 뚫는다 — check_fig 「선에 깔림」이 열 장에서
    # 났다(2026-09-09). 줄을 번갈아 뒤집으면 이음이 같은 칸에서 곧장 아래로 내려간다
    for ri, r in enumerate(rows):
        cells = [(x.get('name', ''), _co_text(x), x.get('bottleneck') == 'high') for x in r]
        if ri % 2:
            # 짧은 줄이 뒤집히면 빈 칸을 앞에 세워야 이음이 같은 칸에서 내려온다
            cells = [None] * (per_row - len(cells)) + cells[::-1]
        p.row(*cells)

    def col(ri, i):
        # 그 줄의 i번째 마디가 놓인 칸 번호. 뒤집힌 줄은 오른쪽부터 센다
        return i if ri % 2 == 0 else per_row - 1 - i

    for ri, r in enumerate(rows):
        for ci in range(len(r) - 1):
            p.connect(p.at(ri, col(ri, ci)), p.at(ri, col(ri, ci + 1)))
        if ri + 1 < len(rows):
            p.connect(p.at(ri, col(ri, len(r) - 1)), p.at(ri + 1, col(ri + 1, 0)))
    p.at(0, 0)          # 여기서 배치가 돌아 판을 넘으면 AssertionError 가 난다
    n_bn = sum(1 for s in stages if s.get('bottleneck') == 'high')
    if n_bn:
        p.note('짙은 테두리 %d곳은 원문이 진입장벽·독과점·문지기라고 지목한 마디다' % n_bn)
    svg = p.render(canon.get('chain_name', ''))
    return svg.replace('data-fig-layout="1"', 'class="chain" data-fig-layout="1"'), n_bn


def preview(paths, out):
    """정본 파일 여럿을 한 장에 굽는다 — 배치가 무너지는 자리를 눈과 검사기가 함께 본다."""
    import io
    import json
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import card_lib as cl
    body = []
    for p in paths:
        d = json.load(io.open(p, encoding='utf-8'))
        svg, _ = chain_svg(d)
        body.append('<h3>%s <small>%s</small></h3><div class="uc-fig">%s</div>'
                    % (d.get('chain_name', ''), d.get('canon_slug', ''), svg))
    # 미리보기에는 대시보드의 색 변수가 없다. 안 채우면 var(--surface) 가 무효가 되어
    # 상자가 새까맣게 칠해진다 — 도해가 아니라 미리보기의 결함이니 여기서 값을 준다
    VARS = (':root{--surface:#fff;--line:#d6dae2;--ink-1:#1a2233;--ink-2:#39415a;'
            '--ink-3:#6b7488;--ink-6:#eceef2;--accent:#39415a}')
    html = ('<!doctype html><meta charset="utf-8"><style>%s%s%s\nbody{max-width:720px;'
            'margin:24px auto;font-family:system-ui}</style>%s%s'
            % (VARS, cl.FIG_CSS + fl.CSS, CSS, cl.FIG_DEFS, ''.join(body)))
    io.open(out, 'w', encoding='utf-8').write(html)
    return out


if __name__ == '__main__':
    import glob
    sys.stdout.reconfigure(encoding='utf-8')
    ps = sorted(glob.glob(os.path.join(ROOT, 'insights', 'chains', 'canon', '*.json')))
    if not ps:
        print('정본이 아직 없다')
    else:
        print(preview(ps, os.path.join(ROOT, 'scratchpad', '_chain_fig_preview.html')),
              '— 정본 %d' % len(ps))
