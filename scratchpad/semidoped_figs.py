# -*- coding: utf-8 -*-
"""Semi Doped 카드 도해.

  ① 순서 도해   곱셈이 덧셈이 되고 되돌아오는 자리   (텐서다인 편)
  ② 구조 도해   쿼터랙 하나가 담는 것                (텐서다인 편)

규칙(insight-figure):
  - 원문에 없는 값을 그리지 않는다. 도형 개수도 값이다 → ②의 칸 넷은 원문의
    "we can put four of them in a rack"에서만 온다. 칩 72개는 아이콘으로 세지 않고
    글자로만 적는다.
  - 판 위에 글자를 얹지 않는다. 판단은 판 아래 캡션이 말한다.
  - 배치는 scratchpad/check_fig.py 가 본다.
"""

# ── ① 곱셈이 덧셈이 되고, 되돌아온다 ────────────────────────────────────
# 값은 전사본에 있는 관계식뿐이다. 면적 비율을 상자 폭으로 그리지 않는다 —
# 원문에 "a lot more area"라는 말만 있고 배수가 없다.
_STEPS = [
    (10,  126, '곱셈 A × B',    '면적·전력이 크다'),
    (160, 126, '로그로 바꾼다',  'log A, log B'),
    (310, 126, '덧셈이 된다',    'log A + log B'),
    (460, 130, '선형으로 되돌린다', '여기서 잃으면 헛일'),
]


def fig_log():
    h = ['<svg viewBox="0 0 600 250" role="img" aria-label="곱셈을 로그로 바꿔 덧셈으로 '
         '만들고 다시 선형으로 되돌리는 네 단계">']
    for x, w, head, sub in _STEPS:
        cls = 'good-box' if head.startswith('선형') else 'mid-box'
        h.append('<rect x="%d" y="64" width="%d" height="56" rx="9" class="%s"/>'
                 % (x, w, cls))
        h.append('<text x="%d" y="90" class="t-step" text-anchor="middle">%s</text>'
                 % (x + w // 2, head))
        h.append('<text x="%d" y="110" class="t-sub" text-anchor="middle">%s</text>'
                 % (x + w // 2, sub))
    for x0, x1 in ((136, 160), (286, 310), (436, 460)):
        h.append('<line class="flow" x1="%d" y1="92" x2="%d" y2="92"/>' % (x0, x1))
    h.append('<line class="flow" x1="525" y1="122" x2="525" y2="170"/>')
    h.append('<rect x="110" y="170" width="380" height="52" rx="9" class="bad-box"/>')
    h.append('<text x="300" y="194" class="t-msg" text-anchor="middle">'
             '룩업 테이블·테일러 급수로 복원하면</text>')
    h.append('<text x="300" y="212" class="t-msg" text-anchor="middle">'
             '앞에서 번 면적·전력을 그대로 잃는다</text>')
    h.append('</svg>')
    return ''.join(h)


LOG_MATH = fig_log()


# ── ② 쿼터랙 하나가 담는 것 ─────────────────────────────────────────────
# 칸 넷은 "we can put four of them in a rack"에서 온다. 칩 72개는 세지 않고 적는다.
def fig_rack():
    h = ['<svg viewBox="0 0 600 320" role="img" aria-label="풀랙 하나와 쿼터랙 넷으로 '
         '나뉜 랙을 나란히 둔 그림">']
    h.append('<text x="155" y="44" class="t-head" text-anchor="middle">블랙웰 GB300</text>')
    h.append('<rect x="90" y="60" width="130" height="200" rx="8" class="mid-box"/>')
    h.append('<text x="155" y="282" class="t-val" text-anchor="middle">풀랙 150kW</text>')

    h.append('<text x="445" y="44" class="t-head" text-anchor="middle">텐서다인</text>')
    h.append('<rect x="380" y="60" width="130" height="200" rx="8" class="mid-box"/>')
    for y in (110, 160, 210):
        h.append('<line class="thin" x1="380" y1="%d" x2="510" y2="%d"/>' % (y, y))
    h.append('<rect x="380" y="210" width="130" height="50" rx="6" class="good-box"/>')
    h.append('<text x="522" y="240" class="t-sub">쿼터랙</text>')
    h.append('<text x="445" y="282" class="t-val" text-anchor="middle">'
             '13U · 72칩 · 30kW</text>')
    h.append('<text x="445" y="304" class="t-sub" text-anchor="middle">'
             '넷 쌓으면 120kW</text>')
    h.append('</svg>')
    return ''.join(h)


RACK = fig_rack()


# ── ③ 속도가 오르면 구리가 짧아진다 ────────────────────────────────────
# 막대 길이가 곧 원문의 미터 값이다(1m = 120px). 없는 값을 길이로 만들지 않는다.
_COPPER = [('100Gb/s', 2.0, '약 2m'), ('200Gb/s', 1.0, '약 1m'), ('400Gb/s', 0.5, '약 0.5m')]


def fig_copper():
    h = ['<svg viewBox="0 0 600 200" role="img" aria-label="레인 속도가 오를수록 구리 '
         '직결 케이블이 닿는 거리가 짧아진다">']
    h.append('<text x="150" y="34" class="t-head">구리 직결 케이블이 닿는 거리</text>')
    for i, (lab, m, val) in enumerate(_COPPER):
        y = 60 + i * 50
        w = int(m * 120)
        h.append('<text x="138" y="%d" class="t-step" text-anchor="end">%s</text>' % (y + 5, lab))
        h.append('<rect x="150" y="%d" width="%d" height="26" rx="5" class="mid-box"/>'
                 % (y - 13, w))
        h.append('<text x="%d" y="%d" class="t-val">%s</text>' % (150 + w + 12, y + 5, val))
    h.append('</svg>')
    return ''.join(h)


COPPER = fig_copper()


# ── ④ 꽂는 것에서 패키지 안으로 ────────────────────────────────────────
# 세 줄은 위치의 종류다. 높이나 길이로 값을 주장하지 않고 값은 글자로만 적는다.
_OPTICS = [('플러거블(꽂는 방식)', '손실 약 35dB', '20~25pJ/bit'),
           ('NPO(패키지 옆)', '손실 15~20dB', '약 10pJ/bit'),
           ('CPO(패키지 안)', '손실 약 6dB', '5pJ/bit 미만')]


def fig_optics():
    h = ['<svg viewBox="0 0 600 210" role="img" aria-label="플러거블·NPO·CPO 세 자리의 '
         '손실과 비트당 전력">']
    for i, (pos, loss, pj) in enumerate(_OPTICS):
        y = 36 + i * 56
        cls = 'good-box' if pos.startswith('CPO') else 'mid-box'
        h.append('<rect x="40" y="%d" width="520" height="44" rx="8" class="%s"/>' % (y, cls))
        h.append('<text x="58" y="%d" class="t-step">%s</text>' % (y + 28, pos))
        h.append('<text x="300" y="%d" class="t-msg" text-anchor="middle">%s</text>'
                 % (y + 28, loss))
        h.append('<text x="542" y="%d" class="t-val" text-anchor="end">%s</text>'
                 % (y + 28, pj))
    h.append('</svg>')
    return ''.join(h)


OPTICS = fig_optics()


# ── ⑤ 같은 1.6테라비트를 채우는 세 조합 ────────────────────────────────
# 칸 개수가 곧 채널 수다(8·16·32). 원문에 있는 수라 그대로 나눈다.
_LANES = [(8, '8 × 200G', 'PAM4'), (16, '16 × 100G', 'LPO'), (32, '32 × 50G', 'NRZ')]


def fig_lanes():
    h = ['<svg viewBox="0 0 600 220" role="img" aria-label="채널 수와 레인 속도를 달리해 '
         '같은 1.6테라비트를 채우는 세 조합">']
    h.append('<text x="190" y="28" class="t-head">셋 다 합치면 1.6테라비트</text>')
    for i, (n, lab, mod) in enumerate(_LANES):
        y = 60 + i * 60
        h.append('<text x="178" y="%d" class="t-step" text-anchor="end">%s</text>' % (y + 5, lab))
        seg = 340.0 / n
        for k in range(n):
            h.append('<rect x="%.1f" y="%d" width="%.1f" height="30" rx="2" class="mid-box"/>'
                     % (190 + k * seg, y - 15, seg - 2))
        h.append('<text x="540" y="%d" class="t-sub">%s</text>' % (y + 5, mod))
    h.append('</svg>')
    return ''.join(h)


LANES = fig_lanes()


# ── ⑥ 메모리 네 층 ─────────────────────────────────────────────────────
# Nvidia Dynamo 팀이 가른 G1~G4. 층 사이 낙차의 크기는 원문에 수치가 없어 그리지 않는다.
_TIERS = [('G1 · HBM', '가장 빠르다'), ('G2 · CPU DRAM', '옆 자리'),
          ('G3 · 로컬 SSD', '같은 랙'), ('G4 · 원격 스토리지', '네트워크 너머')]


def fig_tiers():
    h = ['<svg viewBox="0 0 600 260" role="img" aria-label="HBM 부터 원격 스토리지까지 '
         '네 층으로 나눈 메모리 계층">']
    for i, (lab, where) in enumerate(_TIERS):
        y = 30 + i * 56
        cls = 'good-box' if i == 0 else 'mid-box'
        h.append('<rect x="90" y="%d" width="420" height="44" rx="8" class="%s"/>' % (y, cls))
        h.append('<text x="108" y="%d" class="t-step">%s</text>' % (y + 28, lab))
        h.append('<text x="492" y="%d" class="t-sub" text-anchor="end">%s</text>'
                 % (y + 28, where))
    h.append('</svg>')
    return ''.join(h)


TIERS = fig_tiers()


# ── ⑦ 스케일업 도메인 두 겹 ────────────────────────────────────────────
def fig_domain():
    h = ['<svg viewBox="0 0 600 240" role="img" aria-label="128칩 도메인이 2,048칩 도메인 '
         '안에 드는 두 겹 구조">']
    h.append('<rect x="40" y="40" width="520" height="170" rx="10" class="mid-box"/>')
    h.append('<text x="60" y="66" class="t-head">2,048칩 · 인터커넥트 200Gb/s</text>')
    h.append('<rect x="90" y="96" width="250" height="90" rx="8" class="good-box"/>')
    h.append('<text x="215" y="134" class="t-step" text-anchor="middle">128칩</text>')
    h.append('<text x="215" y="158" class="t-sub" text-anchor="middle">'
             'Tomahawk 6 · 칩당 600Gb/s</text>')
    h.append('<text x="380" y="140" class="t-sub">약 16랙 어치</text>')
    h.append('<text x="380" y="162" class="t-sub">(진행자 어림)</text>')
    h.append('</svg>')
    return ''.join(h)


DOMAIN = fig_domain()


# ── ⑧ 천재 옆에 비서를 몇 명 두나 ──────────────────────────────────────
def fig_cpu():
    h = ['<svg viewBox="0 0 600 230" role="img" aria-label="GPU 와 호스트 노드 CPU, 그리고 '
         '따로 세우는 에이전틱 CPU 랙">']
    h.append('<rect x="40" y="50" width="200" height="60" rx="9" class="good-box"/>')
    h.append('<text x="140" y="74" class="t-step" text-anchor="middle">GPU</text>')
    h.append('<text x="140" y="96" class="t-sub" text-anchor="middle">비유로는 천재</text>')
    h.append('<rect x="40" y="140" width="200" height="60" rx="9" class="mid-box"/>')
    h.append('<text x="140" y="164" class="t-step" text-anchor="middle">호스트 노드 CPU</text>')
    h.append('<text x="140" y="186" class="t-sub" text-anchor="middle">쉬지 않게 먹인다</text>')
    h.append('<line class="flow" x1="140" y1="112" x2="140" y2="138"/>')
    h.append('<line class="flow" x1="242" y1="140" x2="328" y2="140"/>')
    h.append('<rect x="330" y="95" width="230" height="90" rx="9" class="mid-box"/>')
    h.append('<text x="445" y="124" class="t-step" text-anchor="middle">에이전틱 CPU 랙</text>')
    h.append('<text x="445" y="148" class="t-sub" text-anchor="middle">컴파일 · 검색 · 조회</text>')
    h.append('<text x="445" y="172" class="t-sub" text-anchor="middle">코어 88 에서 512 로</text>')
    h.append('</svg>')
    return ''.join(h)


CPU_ROLES = fig_cpu()


# ── ⑨ 광원 파장 ────────────────────────────────────────────────────────
# 막대 길이가 곧 나노미터 값이다(1nm = 1px). EUV 가 얼마나 뚝 떨어지는지가 요점이다.
_WAVE = [('i-line 365nm', 365), ('KrF 248nm', 248), ('ArF 193nm', 193), ('EUV 13.5nm', 13.5)]


def fig_wave():
    h = ['<svg viewBox="0 0 600 225" role="img" aria-label="i-line 부터 EUV 까지 광원 '
         '파장이 짧아진 폭">']
    h.append('<text x="150" y="32" class="t-head">광원 파장 — 짧을수록 가는 선을 그린다</text>')
    for i, (lab, nm) in enumerate(_WAVE):
        y = 64 + i * 45
        cls = 'good-box' if lab.startswith('EUV') else 'mid-box'
        h.append('<text x="138" y="%d" class="t-step" text-anchor="end">%s</text>' % (y + 5, lab))
        h.append('<rect x="150" y="%d" width="%.1f" height="26" rx="5" class="%s"/>'
                 % (y - 13, nm, cls))
    h.append('</svg>')
    return ''.join(h)


WAVE = fig_wave()


# ── ⑩ 층이 셋이냐 둘이냐 ───────────────────────────────────────────────
def fig_layers():
    h = ['<svg viewBox="0 0 600 190" role="img" aria-label="CoWoS 의 세 층과 EMIB 의 '
         '두 층을 나란히 둔 그림">']
    h.append('<text x="160" y="34" class="t-head" text-anchor="middle">CoWoS-L — 층 셋</text>')
    for y, lab in ((50, '다이 · HBM'), (94, '실리콘 인터포저'), (138, '기판')):
        h.append('<rect x="60" y="%d" width="200" height="34" rx="6" class="mid-box"/>' % y)
        h.append('<text x="160" y="%d" class="t-sub" text-anchor="middle">%s</text>' % (y + 22, lab))
    h.append('<text x="440" y="34" class="t-head" text-anchor="middle">EMIB — 층 둘</text>')
    h.append('<rect x="340" y="50" width="200" height="34" rx="6" class="mid-box"/>')
    h.append('<text x="440" y="72" class="t-sub" text-anchor="middle">다이 · HBM</text>')
    h.append('<rect x="340" y="94" width="200" height="78" rx="6" class="mid-box"/>')
    h.append('<rect x="390" y="100" width="100" height="24" rx="4" class="good-box"/>')
    h.append('<text x="440" y="116" class="t-sub" text-anchor="middle">브리지</text>')
    h.append('<text x="440" y="152" class="t-sub" text-anchor="middle">기판</text>')
    h.append('</svg>')
    return ''.join(h)


LAYERS = fig_layers()


# ── ⑪ 레티클 한 장의 몇 배까지 담나 ────────────────────────────────────
# 막대 길이가 곧 배수다(1배 = 8px). 「약 40배」는 목표치라고 원문이 밝힌 값이다.
_RETICLE = [('CoWoS 1세대', 3.3, '3.3배'), ('지금 세대', 5.5, '5.5배'),
            ('다음 세대', 9.5, '9.5배'), ('웨이퍼 한 장(목표)', 40, '약 40배'),
            ('EMIB 지금(추정)', 8, '8배'), ('EMIB 2028', 12, '12배 이상')]


def fig_reticle():
    h = ['<svg viewBox="0 0 600 235" role="img" aria-label="패키징 방식별로 레티클 한 장의 '
         '몇 배까지 담는지">']
    h.append('<text x="190" y="30" class="t-head">레티클 한 장의 몇 배까지 담나</text>')
    for i, (lab, mult, val) in enumerate(_RETICLE):
        y = 60 + i * 30
        cls = 'good-box' if lab.startswith('EMIB') else 'mid-box'
        w = mult * 8
        h.append('<text x="178" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 4, lab))
        h.append('<rect x="190" y="%d" width="%.1f" height="18" rx="4" class="%s"/>'
                 % (y - 9, w, cls))
        h.append('<text x="%.0f" y="%d" class="t-sub">%s</text>' % (190 + w + 10, y + 4, val))
    h.append('</svg>')
    return ''.join(h)


RETICLE = fig_reticle()


# ── ⑫ 광트랜시버 시장에서 중국이 쥔 몫 ─────────────────────────────────
# 띠 길이가 곧 점유율이다. 27%는 로이터 기사 값, 34%는 일부 애널리스트 상향치다.
def fig_share():
    h = ['<svg viewBox="0 0 600 185" role="img" aria-label="글로벌 광트랜시버 시장에서 '
         '중국계가 쥔 몫과 그 안에서 한 회사가 쥔 몫">']
    h.append('<text x="60" y="34" class="t-head">글로벌 광트랜시버 시장</text>')
    h.append('<rect x="60" y="52" width="480" height="44" rx="6" class="mid-box"/>')
    h.append('<rect x="60" y="52" width="240" height="44" rx="6" class="bad-box"/>')
    h.append('<rect x="60" y="52" width="130" height="44" rx="6" class="good-box"/>')
    h.append('<line class="thin" x1="60" y1="108" x2="300" y2="108"/>')
    h.append('<text x="180" y="126" class="t-sub" text-anchor="middle">중국계 합산 약 50%</text>')
    h.append('<text x="420" y="126" class="t-sub" text-anchor="middle">중국 밖</text>')
    h.append('<text x="125" y="150" class="t-sub" text-anchor="middle">이노라이트 27%</text>')
    h.append('<text x="125" y="170" class="t-sub" text-anchor="middle">(상향 추정 34%)</text>')
    h.append('</svg>')
    return ''.join(h)


SHARE = fig_share()


# ── ⑬ 같은 비트를 만드는 데 드는 웨이퍼 ────────────────────────────────
# 원 개수가 곧 값이다 — "You need three wafers of DRAM to make the equivalent
# number of bits in HBM." 진행자가 어림이라고 밝힌 값이라 캡션에 그렇게 적는다.
def fig_wafer3():
    h = ['<svg viewBox="0 0 600 200" role="img" aria-label="같은 비트를 만드는 데 드는 '
         '웨이퍼가 DRAM 한 장이면 HBM 은 세 장">']
    h.append('<text x="150" y="40" class="t-head" text-anchor="middle">DRAM</text>')
    h.append('<circle cx="150" cy="110" r="42" class="mid-box"/>')
    h.append('<text x="150" y="180" class="t-sub" text-anchor="middle">웨이퍼 1장</text>')
    h.append('<text x="420" y="40" class="t-head" text-anchor="middle">HBM · 같은 비트</text>')
    for cx in (330, 420, 510):
        h.append('<circle cx="%d" cy="110" r="42" class="good-box"/>' % cx)
    h.append('<text x="420" y="180" class="t-sub" text-anchor="middle">웨이퍼 3장</text>')
    h.append('</svg>')
    return ''.join(h)


WAFER3 = fig_wafer3()


FIG_CSS = """
  .uc-fig text.t-head { font-size:11.5px; font-weight:800; fill:var(--ink-3);
    letter-spacing:.04em; }
  .uc-fig text.t-step { font-size:13px; font-weight:700; fill:var(--ink); }
  .uc-fig text.t-msg  { font-size:12.5px; fill:var(--ink-2); }
  .uc-fig text.t-sub  { font-size:11.5px; fill:var(--ink-3); }
  .uc-fig text.t-val  { font-size:14px; font-weight:800; fill:var(--ink); }
  .uc-fig .thin { stroke:var(--line); stroke-width:1; }
  .uc-fig .good-box { fill:var(--fig-good-bg,rgba(47,143,107,.12));
    stroke:var(--fig-good,#2f8f6b); stroke-width:1.4; }
  .uc-fig .mid-box  { fill:rgba(127,127,127,.10); stroke:var(--line); stroke-width:1.2; }
  .uc-fig .bad-box  { fill:var(--fig-bad-bg,rgba(194,80,74,.12));
    stroke:var(--fig-bad,#c2504a); stroke-width:1.4; }
"""

ALL = [('곱셈을 덧셈으로 바꾸고 되돌아오는 자리', LOG_MATH),
       ('쿼터랙 하나가 무엇을 담나', RACK),
       ('속도가 오르면 구리가 짧아진다', COPPER),
       ('꽂는 것에서 패키지 안으로', OPTICS),
       ('같은 1.6테라비트를 채우는 세 조합', LANES),
       ('메모리 네 층', TIERS),
       ('스케일업 도메인 두 겹', DOMAIN),
       ('천재 옆에 비서를 몇 명 두나', CPU_ROLES),
       ('광원 파장', WAVE),
       ('층이 셋이냐 둘이냐', LAYERS),
       ('레티클 한 장의 몇 배까지 담나', RETICLE),
       ('광트랜시버 시장 몫', SHARE),
       ('같은 비트에 드는 웨이퍼', WAFER3)]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, svg in ALL:
        print(name, '->', check_fig.hits(svg) or 'FAIL 0건')
