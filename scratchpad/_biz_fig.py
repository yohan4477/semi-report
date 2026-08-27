# -*- coding: utf-8 -*-
"""AI 비즈니스 리포트 도해 — 레일 지도.

값을 하나도 안 그린다. 상자 개수는 우리 층 구분이고 원문이 센 수가 아니라서,
캡션에 그렇게 적는다(insight-figure 규칙 1). 자리는 아래 _row 가 계산한다 —
손으로 찍지 않는다(규칙 2)."""
import gen_sudoremove_dashboard as sudo

_svg, _box, _a, _lt = sudo._svg, sudo._box, sudo._a, sudo._lt

W = 640


def _row(n, y, h, w, gap=10, y0=None):
    """가운데 정렬한 상자 n개의 (x, y, w, h) 목록. x를 손으로 찍지 않으려고 둔 함수."""
    total = n * w + (n - 1) * gap
    x0 = (W - total) // 2
    return [(x0 + i * (w + gap), y if y0 is None else y0, w, h) for i in range(n)]


def _chain(cells, lines_list, accent=()):
    """가로로 늘어선 상자와 그 사이 화살표. accent에 든 자리만 강조색 테두리."""
    out = []
    for i, ((x, y, w, h), lines) in enumerate(zip(cells, lines_list)):
        st, sw = ('var(--accent)', 1.8) if i in accent else ('var(--ink-3)', 1.5)
        out.append(_box(x, y, w, h, lines, st, sw))
        if i:
            px = cells[i - 1][0] + cells[i - 1][2]
            out.append(_a(px, y + h // 2, x, y + h // 2))
    return ''.join(out)


def _elbow(x1, y1, x2, y2):
    """세로로 내려간 뒤 가로로 꺾는 화살표. 한 path 라 화살촉이 끝에 하나만 붙는다."""
    return '<path d="M%d %d V%d H%d" class="flow" fill="none"/>' % (x1, y1, y2, x2)


R1 = _row(5, 56, 54, 112)
R2 = _row(3, 168, 48, 140)
LAB = _row(1, 240, 44, 200)
OUT = _row(3, 306, 46, 150)

FIG_RAILS = _svg(W, 376, '모델 랩이 사는 것이 둘이라 레일도 둘이다', ''.join([
    _lt(14, 44, '레일① 컴퓨트'),
    _chain(R1, [['전력·건설'], ['칩·메모리'], ['서버·랙', '네트워킹'],
                ['클라우드'], ['추론 엔진', '추론 서빙']], accent=(4,)),
    _lt(14, 156, '레일② 데이터·환경'),
    _chain(R2, [['일하는 사람'], ['RL 환경', '데이터 파운드리'], ['평가·검증']], accent=(1,)),
    # 두 레일이 모델 랩으로 모인다. 레일①은 오른쪽으로 비켜 내려온다 —
    # 곧게 그으면 레일② 상자를 가로지른다.
    _elbow(R1[4][0] + R1[4][2] - 6, R1[4][1] + R1[4][3],
           LAB[0][0] + LAB[0][2], LAB[0][1] + LAB[0][3] // 2),
    _a(R2[2][0] + R2[2][2] // 2, R2[2][1] + R2[2][3],
       LAB[0][0] + LAB[0][2] - 40, LAB[0][1]),
    _box(LAB[0][0], LAB[0][1], LAB[0][2], LAB[0][3], ['모델 랩'], 'var(--accent)', 2.2),
    _a(LAB[0][0] + LAB[0][2] // 2, LAB[0][1] + LAB[0][3],
       OUT[0][0] + OUT[0][2] // 2, OUT[0][1]),
    _chain(OUT, [['토큰'], ['앱·에이전트'], ['기업 예산']]),
]))


# ── 절 3. 같은 단가인데 TCO가 갈린다 ────────────────────────────────
# 막대 길이는 굿풋 손실률 실측값이다(260420 §5). 손으로 어림하지 않고 _bx 가 환산한다.
_r, _t = sudo._r, sudo._t

GRADE = [('골드 네오클라우드', 6.14, '1.00배'),
         ('하이퍼스케일러', 10.53, '1.10배'),
         ('실버 네오클라우드', 20.91, '1.15배')]
_GX, _GW, _GMAX = 176, 250, 24.0     # 막대 왼쪽 끝 · 최대 길이 · 눈금 상한(%)


def _bx(v):
    """값 v(%)가 놓이는 x 좌표. 막대 끝도 눈금도 전부 이 함수만 쓴다."""
    return _GX + _GW * v / _GMAX


def _row3(i, name, v, tco):
    y = 54 + i * 46
    col = 'var(--accent)' if i == 0 else 'var(--ink-3)'
    return ''.join([
        _lt(14, y + 18, name, bold=False),
        '<rect x="%d" y="%d" width="%.1f" height="26" rx="3" fill="%s"/>'
        % (_GX, y, _bx(v) - _GX, col),
        _lt(int(_bx(v)) + 8, y + 18, '%.2f%%' % v),
        _lt(500, y + 18, tco),
    ])


FIG_GOODPUT = _svg(W, 250, '시간당 단가가 같아도 총소유비용은 갈린다', ''.join(
    ['<path d="M%.1f 44 V196" stroke="var(--line)" stroke-width="1"/>' % _bx(v)
     for v in (0, 6, 12, 18, 24)]
    + ['<text x="%.1f" y="38" text-anchor="middle" class="t-sm">%d%%</text>' % (_bx(v), v)
       for v in (0, 6, 12, 18, 24)]
    + [_lt(14, 26, '돌아갔는데 결과가 안 남은 시간'), _lt(500, 26, '3년 TCO')]
    + [_row3(i, *g) for i, g in enumerate(GRADE)]
    + [_box(14, 206, W - 28, 34,
            ['GPU 시간당 단가를 세 등급 모두 4달러로 고정하고 잰 값이다'])]
))


# ── 절 8. 엔비디아 백스톱은 어떻게 정산되나 ──────────────────────────
# 폭 = 달러 값이다(260706 §3 의 1년차 예시). 총액 6.75 를 폭 _BW 에 맞춰 환산한다.
_BX0, _BW, _BTOT = 20, 600, 6.75


def _seg(v0, v1, y, h, fill, lines):
    """v0~v1 달러 구간을 한 칸으로 그린다. x는 값에서 나온다 — 손으로 안 찍는다."""
    x, w = _BX0 + _BW * v0 / _BTOT, _BW * (v1 - v0) / _BTOT
    out = ['<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="6" fill="none" '
           'stroke="%s" stroke-width="1.6"/>' % (x, y, w, h, fill)]
    top = y + (h - (len(lines) - 1) * 16) // 2 + 5
    for i, s in enumerate(lines):
        out.append(_t(int(x + w / 2), top + i * 16, s, 't-lab' if i == 0 else 't-sm'))
    return ''.join(out)


FIG_BACKSTOP = _svg(W, 268, '보증선까지는 다 갖고, 넘긴 만큼만 나눈다', ''.join([
    _lt(20, 24, '1년차 — 고객이 시간당 GPU당 6.75달러를 낸다'),
    _seg(0, 6.75, 34, 40, 'var(--ink-3)', ['6.75달러']),
    # 화살표는 보증선(3.68달러) 자리에서 내려온다 — 자리를 값에서 뽑는다
    _a(int(_BX0 + _BW * 3.68 / _BTOT), 74, int(_BX0 + _BW * 3.68 / _BTOT), 100),
    _lt(20, 122, '보증선을 기준으로 둘로 갈린다'),
    _seg(0, 3.68, 132, 52, 'var(--accent)', ['보증선 3.68달러', '전부 네오클라우드']),
    _seg(3.68, 6.75, 132, 52, 'var(--ink-3)', ['넘긴 3.07달러', '여기만 나눈다']),
    _lt(20, 208, '넘긴 몫의 40%를 엔비디아가 가져간 결과'),
    _seg(0, 5.52, 218, 40, 'var(--accent)', ['네오클라우드 5.52달러']),
    _seg(5.52, 6.75, 218, 40, 'var(--ink)', ['엔비디아 1.23달러']),
]))


# ── 절 4-b. 분산 추론 스택 3단과 해자가 걸린 자리 ────────────────────
# 값을 하나도 안 그린다. 상자는 원문이 이름을 댄 부품이고 개수가 곧 주장이 아니다.
_S = _row(3, 92, 76, 176, gap=16)

FIG_ENGINE = _svg(W, 258, '돈이 안 드는 층이 성능을 정한다', ''.join([
    _lt(14, 34, '요청이 지나가는 순서'),
    _lt(14, 56, '세 부품 다 오픈소스다 — 쓰는 데 돈이 들지 않는다', bold=False),
    _chain(_S, [['라우터', '요청을 워커로 나눈다'],
                ['추론 엔진', 'vLLM · SGLang'],
                ['캐시·전송 엔진', 'Mooncake · NIXL']], accent=(1,)),
    _a(_S[1][0] + _S[1][2] // 2, _S[1][1] + _S[1][3], _S[1][0] + _S[1][2] // 2, 196),
    _box(_S[0][0], 196, _S[2][0] + _S[2][2] - _S[0][0], 54,
         ['해자가 걸린 자리', '컨텍스트 병렬화는 vLLM 지원 목록에서 AMD 백엔드가 빠져 있다'],
         'var(--accent)', 1.8),
]))


# ── 절 6. 임대는 만기로 세 구간이다 ─────────────────────────────────
# 위층 띠는 기간에 비례한다(260402 §5~8: 3개월 미만 · 3개월~3년 · 4~5년). 단기 구간은
# 폭이 26px 라 글자가 안 들어간다 — 띠에는 글자를 안 넣고 아래 같은 폭 칸에 적는다.
_MX0, _MW, _MMAX = 88, 520, 60.0
_TEN = [(0, 3, '단기', ['런팟 · 람다', '가동률이 값을 정한다']),
        (3, 36, '중기', ['AI 네이티브 기업 · 중소 AI 랩', '설문으로 잡은 실제 협상가']),
        (48, 60, '오프테이크', ['프론티어 AI 랩', '빌린 돈의 상환 조건'])]
_COL = _row(3, 118, 98, 196, gap=12)


def _mx(m):
    return _MX0 + _MW * m / _MMAX


def _band(m0, m1, accent=False):
    x, w = _mx(m0), max(_mx(m1) - _mx(m0), 4)
    return ('<rect x="%.1f" y="52" width="%.1f" height="20" rx="4" fill="none" stroke="%s" '
            'stroke-width="%s"/>' % (x, w, 'var(--accent)' if accent else 'var(--ink-3)',
                                     1.8 if accent else 1.5))


FIG_LEASE = _svg(W, 260, '임대는 만기로 세 구간이고 구간마다 다른 고객을 만난다', ''.join(
    [_lt(14, 34, '계약 기간 — 띠 길이가 곧 기간이다')]
    + ['<text x="%.1f" y="46" text-anchor="middle" class="t-sm">%s</text>' % (_mx(m), lab)
       for m, lab in [(0, '0'), (12, '1년'), (36, '3년'), (60, '5년')]]
    + ['<path d="M%.1f 72 V86" stroke="var(--line)" stroke-width="1"/>' % _mx(m)
       for m in (12, 36)]
    + [_band(m0, m1, i == 1) for i, (m0, m1, _t2, _l) in enumerate(_TEN)]
    # 띠 한가운데에서 아래 칸 한가운데로 내린다 — 두 자리 다 계산한 값이다
    + ['<path d="M%.1f 72 L%d 118" class="flow" fill="none"/>'
       % ((_mx(m0) + _mx(m1)) / 2, _COL[i][0] + _COL[i][2] // 2)
       for i, (m0, m1, _t2, _l) in enumerate(_TEN)]
    + [_box(_COL[i][0], _COL[i][1], _COL[i][2], _COL[i][3], [title] + lines,
            'var(--accent)' if i == 1 else 'var(--ink-3)', 1.8 if i == 1 else 1.5)
       for i, (m0, m1, title, lines) in enumerate(_TEN)]
    + [_box(14, 226, W - 28, 30,
            ['3년과 4년 사이는 원문이 경계를 안 그어 비워 뒀다'])]
))
