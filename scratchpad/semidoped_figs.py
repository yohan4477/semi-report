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
# Nvidia Dynamo 팀이 나눈 G1~G4. 층 사이 낙차의 크기는 원문에 수치가 없어 그리지 않는다.
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


# ── ⑭ 레티클 84장이 한 칩이 된다 ───────────────────────────────────────
# 칸 개수가 곧 값이다 — 원문의 "84 reticles". 12×7 로 정확히 84칸을 그린다.
def fig_wse():
    h = ['<svg viewBox="0 0 600 270" role="img" aria-label="레티클 84장을 이어 붙여 '
         '한 칩으로 쓰는 웨이퍼 스케일 엔진">']
    h.append('<text x="300" y="28" class="t-head" text-anchor="middle">웨이퍼 스케일 엔진</text>')
    for r in range(7):
        for c in range(12):
            h.append('<rect x="%d" y="%d" width="36" height="26" rx="3" class="good-box"/>'
                     % (72 + c * 38, 40 + r * 28))
    h.append('<text x="300" y="258" class="t-sub" text-anchor="middle">레티클 84장 = 한 칩</text>')
    h.append('</svg>')
    return ''.join(h)


WSE = fig_wse()


# ── ⑮ 나란히 놓느냐 위아래로 쌓느냐 ────────────────────────────────────
# 값은 접속 피치(약 1.5마이크론)와 「트랜지스터 두 배」뿐이다. 층수를 더 그리지 않는다 —
# 몇 단까지 쌓을 수 있는지는 진행자가 모른다고 밝혔다.
def fig_fold():
    h = ['<svg viewBox="0 0 600 230" role="img" aria-label="로직 칩 둘을 나란히 놓는 것과 '
         '위아래로 쌓는 것을 견준 그림">']
    h.append('<text x="165" y="60" class="t-head" text-anchor="middle">나란히 놓으면</text>')
    h.append('<rect x="60" y="90" width="100" height="50" rx="6" class="mid-box"/>')
    h.append('<rect x="170" y="90" width="100" height="50" rx="6" class="mid-box"/>')
    h.append('<text x="165" y="170" class="t-sub" text-anchor="middle">면적이 두 배</text>')
    h.append('<text x="450" y="40" class="t-head" text-anchor="middle">위아래로 쌓으면</text>')
    h.append('<rect x="380" y="64" width="140" height="44" rx="6" class="good-box"/>')
    h.append('<rect x="380" y="112" width="140" height="44" rx="6" class="good-box"/>')
    h.append('<text x="450" y="180" class="t-sub" text-anchor="middle">같은 면적에 두 배</text>')
    h.append('<text x="450" y="202" class="t-sub" text-anchor="middle">접속 피치 약 1.5μm</text>')
    h.append('</svg>')
    return ''.join(h)


FOLD = fig_fold()


# ── ⑯ PCIe 세대별 전송 속도 ────────────────────────────────────────────
# 막대 길이가 곧 GT/s 값이다(1GT/s = 2.5px).
_PCIE = [('Gen5 · NRZ', 32, '32 GT/s'), ('Gen6 · PAM4', 64, '64 GT/s'),
         ('Gen7 · PAM4', 128, '128 GT/s')]


def fig_pcie():
    h = ['<svg viewBox="0 0 600 200" role="img" aria-label="PCIe 세대별 초당 전송 속도">']
    h.append('<text x="190" y="36" class="t-head">PCIe 세대별 전송 속도</text>')
    for i, (lab, gt, val) in enumerate(_PCIE):
        y = 70 + i * 50
        cls = 'good-box' if lab.startswith('Gen6') else 'mid-box'
        w = gt * 2.5
        h.append('<text x="178" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 5, lab))
        h.append('<rect x="190" y="%d" width="%.1f" height="26" rx="5" class="%s"/>'
                 % (y - 13, w, cls))
        h.append('<text x="%.0f" y="%d" class="t-val">%s</text>' % (190 + w + 10, y + 5, val))
    h.append('</svg>')
    return ''.join(h)


PCIE = fig_pcie()


# ── ⑰ 네트워킹 세 층 ───────────────────────────────────────────────────
# 띠 길이를 거리로 읽히지 않게 셋을 같은 폭으로 둔다 — 랙 높이와 20~50마일을
# 같은 자로 그릴 수는 없다. 거리는 글자로만 적는다.
_NET = [('스케일업', '랙 하나 안(높이 6~7피트)'), ('스케일아웃', '랙 여럿에 걸쳐'),
        ('스케일어크로스', '캠퍼스 사이 20~50마일')]


def fig_net():
    h = ['<svg viewBox="0 0 600 230" role="img" aria-label="스케일업·스케일아웃·'
         '스케일어크로스 세 층이 각각 어디까지를 가리키나">']
    for i, (lab, where) in enumerate(_NET):
        y = 50 + i * 60
        cls = 'good-box' if i == 0 else 'mid-box'
        h.append('<rect x="140" y="%d" width="320" height="44" rx="8" class="%s"/>' % (y, cls))
        h.append('<text x="158" y="%d" class="t-step">%s</text>' % (y + 28, lab))
        h.append('<text x="442" y="%d" class="t-sub" text-anchor="end">%s</text>'
                 % (y + 28, where))
    h.append('</svg>')
    return ''.join(h)


NET = fig_net()


# ── ⑱ 사고가 무엇으로 남았나 ───────────────────────────────────────────
_ACC = [('금 간 실리콘 조각', '도핑과 p-n 접합'),
        ('주머니 속 녹은 초콜릿', '전자레인지'),
        ('금과 알루미늄이 섞임', '고온 강제 시험'),
        ('상온에서 멈춘 레이저', '빨간 LED')]


def fig_accident():
    h = ['<svg viewBox="0 0 600 260" role="img" aria-label="사고나 불량으로 시작한 것이 '
         '무엇으로 남았는지 넷을 짝지은 그림">']
    for i, (before, after) in enumerate(_ACC):
        y = 40 + i * 55
        h.append('<rect x="40" y="%d" width="230" height="44" rx="8" class="mid-box"/>' % y)
        h.append('<text x="155" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (y + 28, before))
        h.append('<line class="flow" x1="272" y1="%d" x2="328" y2="%d"/>' % (y + 22, y + 22))
        h.append('<rect x="330" y="%d" width="230" height="44" rx="8" class="good-box"/>' % y)
        h.append('<text x="445" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (y + 28, after))
    h.append('</svg>')
    return ''.join(h)


ACCIDENT = fig_accident()


# ── ⑲ 먼저 한 사람의 자취 ──────────────────────────────────────────────
# x 좌표는 연도에서 계산한다. 손으로 찍지 않는다.
_YEARS = [(1922, '1922 결정에서 빛', 1), (1925, '1925 특허', 0),
          (1947, '1947 트랜지스터', 1), (1995, '1995 복제 성공', 0),
          (2007, '2007 학계 인정', 1)]


def _yx(year):
    return 60 + (year - 1920) * (500.0 / 90)


def fig_timeline():
    h = ['<svg viewBox="0 0 600 170" role="img" aria-label="1922년 결정 발광부터 2007년 '
         '학계 인정까지의 연표">']
    h.append('<text x="60" y="40" class="t-head">먼저 한 사람의 자취</text>')
    h.append('<line class="thin" x1="55" y1="110" x2="570" y2="110"/>')
    for year, lab, above in _YEARS:
        x = _yx(year)
        h.append('<circle cx="%.0f" cy="110" r="6" class="good-box"/>' % x)
        h.append('<text x="%.0f" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x, 88 if above else 140, lab))
    h.append('</svg>')
    return ''.join(h)


TIMELINE = fig_timeline()


# ── ⑳ 값을 내려 죽이고, 산 쪽이 되갚는다 ───────────────────────────────
_WAR = ['칩을 팔던 회사가 완제품을 원가 아래로 낸다',
        '칩을 사다 붙이던 조립업체가 무너진다',
        '살아남은 쪽이 칩 회사를 사들인다',
        '다음 판에서 값으로 되갚는다']


def fig_pricewar():
    h = ['<svg viewBox="0 0 600 250" role="img" aria-label="칩 회사가 값을 내려 조립업체를 '
         '무너뜨리고, 살아남은 쪽이 칩 회사를 사들여 되갚는 네 단계">']
    for i, step in enumerate(_WAR):
        y = 30 + i * 55
        cls = 'bad-box' if i == 1 else 'mid-box'
        h.append('<rect x="60" y="%d" width="480" height="44" rx="8" class="%s"/>' % (y, cls))
        h.append('<text x="78" y="%d" class="t-step">%s</text>' % (y + 28, step))
        if i < len(_WAR) - 1:
            h.append('<line class="flow" x1="100" y1="%d" x2="100" y2="%d"/>' % (y + 46, y + 53))
    h.append('</svg>')
    return ''.join(h)


PRICEWAR = fig_pricewar()


# ── ㉑ 세계 희토류에서 중국이 차지하는 몫 ───────────────────────────────
# 막대 길이가 곧 퍼센트다(1% = 3.6px).
_RARE = [('채굴', 70, '약 70%'), ('정제', 90, '약 90%')]


def fig_rare():
    h = ['<svg viewBox="0 0 600 170" role="img" aria-label="세계 희토류 채굴과 정제에서 '
         '중국이 차지하는 몫">']
    h.append('<text x="180" y="36" class="t-head">세계 희토류에서 중국이 차지하는 몫</text>')
    for i, (lab, pct, val) in enumerate(_RARE):
        y = 70 + i * 60
        w = pct * 3.6
        h.append('<text x="168" y="%d" class="t-step" text-anchor="end">%s</text>' % (y + 5, lab))
        h.append('<rect x="180" y="%d" width="%.1f" height="28" rx="5" class="bad-box"/>'
                 % (y - 14, w))
        h.append('<text x="%.0f" y="%d" class="t-val">%s</text>' % (180 + w + 10, y + 5, val))
    h.append('</svg>')
    return ''.join(h)


RARE = fig_rare()


# ── ㉒ 메모리가 굵어진 넉 달 ────────────────────────────────────────────
# x 좌표는 달에서 계산한다. 점을 선으로 잇지 않는다 — 사이의 값이 없다.
_MEM = [(4, '4월 · 삼성 HBM4 완판', 1), (5, '5월 · 낸드 값 오름', 0),
        (6, '6월 · HBM4E 샘플', 1), (7, '7월 · 이익 250배', 0),
        (8, '8월 · 낸드 310억 달러', 1)]


def _mx(month):
    return 80 + (month - 4) * 108


def fig_memtime():
    h = ['<svg viewBox="0 0 600 170" role="img" aria-label="4월부터 8월까지 메모리 쪽에서 '
         '나온 발표를 달마다 하나씩 짚은 연표">']
    h.append('<line class="thin" x1="60" y1="110" x2="570" y2="110"/>')
    for m, lab, above in _MEM:
        x = _mx(m)
        h.append('<circle cx="%d" cy="110" r="6" class="good-box"/>' % x)
        h.append('<text x="%d" y="%d" class="t-sub" text-anchor="middle">%s</text>'
                 % (x, 88 if above else 140, lab))
    h.append('</svg>')
    return ''.join(h)


MEMTIME = fig_memtime()


# ── ㉓ 넉 달 사이에 발표된 금액 ─────────────────────────────────────────
# 막대 길이가 곧 억 달러 값이다. 성격이 다른 돈이라 라벨에 무엇인지 함께 적는다.
_MONEY = [(105, '1,050억 달러 · 보증'), (104, '1,040억 달러 · 수주잔고'),
          (25, '250억 달러 · 조달'), (20, '200억 달러 · 증자'),
          (19, '190억 달러 · 임차'), (12.9, '129억 달러 · 인수'),
          (10, '100억 달러 · 약정')]


def fig_money():
    h = ['<svg viewBox="0 0 600 260" role="img" aria-label="넉 달 사이에 발표된 금액을 '
         '성격과 함께 늘어놓은 막대">']
    h.append('<text x="200" y="30" class="t-head">넉 달 사이에 발표된 금액</text>')
    for i, (val, lab) in enumerate(_MONEY):
        y = 50 + i * 30
        h.append('<text x="188" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 4, lab))
        h.append('<rect x="200" y="%d" width="%.1f" height="18" rx="4" class="mid-box"/>'
                 % (y - 9, val * 3.5))
    h.append('</svg>')
    return ''.join(h)


MONEY = fig_money()


# ── ㉔ 중국이 스스로 대게 된 것 ─────────────────────────────────────────
_CN = [('DRAM', 'DDR5 수율 90%'), ('NAND', '점유율 14%'),
       ('파운드리', '분기 30억 달러 첫 돌파'), ('노광 장비', '이머전 DUV 양산 발표')]


def fig_cn():
    h = ['<svg viewBox="0 0 600 265" role="img" aria-label="중국이 자체 공급을 발표한 '
         '네 갈래와 각각의 수치">']
    for i, (lab, state) in enumerate(_CN):
        y = 40 + i * 55
        h.append('<rect x="120" y="%d" width="360" height="44" rx="8" class="mid-box"/>' % y)
        h.append('<text x="138" y="%d" class="t-step">%s</text>' % (y + 28, lab))
        h.append('<text x="462" y="%d" class="t-sub" text-anchor="end">%s</text>'
                 % (y + 28, state))
    h.append('</svg>')
    return ''.join(h)


CN = fig_cn()


# ── ㉕ 옆에 붙이느냐 위에 쌓느냐 ────────────────────────────────────────
# 레인 수(약 2,000 → 최대 약 10만)는 진행자 어림값이다. 캡션에 그렇게 적는다.
def fig_hbc():
    h = ['<svg viewBox="0 0 600 230" role="img" aria-label="메모리를 연산 다이 옆에 붙이는 '
         '지금 방식과 위에 쌓는 방식을 견준 그림">']
    h.append('<text x="160" y="70" class="t-head" text-anchor="middle">지금 — 옆에 붙인다</text>')
    h.append('<rect x="60" y="110" width="120" height="60" rx="7" class="mid-box"/>')
    h.append('<text x="120" y="145" class="t-sub" text-anchor="middle">XPU</text>')
    h.append('<rect x="190" y="110" width="70" height="60" rx="7" class="mid-box"/>')
    h.append('<text x="225" y="145" class="t-sub" text-anchor="middle">HBM</text>')
    h.append('<text x="160" y="200" class="t-sub" text-anchor="middle">옆면으로 약 2,000레인</text>')

    h.append('<text x="445" y="64" class="t-head" text-anchor="middle">쌓으면 — 면 전체</text>')
    h.append('<rect x="360" y="84" width="170" height="50" rx="7" class="good-box"/>')
    h.append('<text x="445" y="114" class="t-sub" text-anchor="middle">메모리</text>')
    h.append('<rect x="360" y="140" width="170" height="50" rx="7" class="good-box"/>')
    h.append('<text x="445" y="170" class="t-sub" text-anchor="middle">XPU</text>')
    h.append('<text x="445" y="215" class="t-sub" text-anchor="middle">최대 약 10만 레인</text>')
    h.append('</svg>')
    return ''.join(h)


HBC = fig_hbc()


# ── ㉖ 매출총이익률 넉 분기 ─────────────────────────────────────────────
# 막대 길이가 곧 퍼센트다(1% = 4px).
_MARGIN = [('4분기 전', 45), ('3분기 전', 56), ('2분기 전', 75), ('직전 분기', 85)]


def fig_margin():
    h = ['<svg viewBox="0 0 600 195" role="img" aria-label="메모리 회사 매출총이익률이 넉 '
         '분기 만에 45%에서 85%로 오른 막대">']
    h.append('<text x="200" y="34" class="t-head">매출총이익률 넉 분기</text>')
    for i, (lab, pct) in enumerate(_MARGIN):
        y = 60 + i * 35
        cls = 'good-box' if i == len(_MARGIN) - 1 else 'mid-box'
        h.append('<text x="188" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 4, lab))
        h.append('<rect x="200" y="%d" width="%d" height="22" rx="4" class="%s"/>'
                 % (y - 11, pct * 4, cls))
        h.append('<text x="%d" y="%d" class="t-val">%d%%</text>' % (200 + pct * 4 + 10, y + 4, pct))
    h.append('</svg>')
    return ''.join(h)


MARGIN = fig_margin()


# ── ㉗ 전기가 랙에 닿기까지 ─────────────────────────────────────────────
# 소재가 어디서 갈리는지만 그린다. 변환 효율이나 손실은 원문에 수치가 없다.
def fig_power():
    h = ['<svg viewBox="0 0 600 170" role="img" aria-label="중전압 그리드에서 800볼트를 '
         '거쳐 48볼트·12볼트로 내려오는 전력 변환 사슬">']
    h.append('<text x="205" y="64" class="t-sub" text-anchor="middle">실리콘카바이드</text>')
    h.append('<text x="395" y="64" class="t-sub" text-anchor="middle">실리콘</text>')
    for x, w, lab, cls in ((40, 140, '중전압 그리드', 'mid-box'),
                           (230, 140, '800V', 'good-box'),
                           (420, 140, '48V · 12V', 'mid-box')):
        h.append('<rect x="%d" y="80" width="%d" height="56" rx="8" class="%s"/>' % (x, w, cls))
        h.append('<text x="%d" y="114" class="t-step" text-anchor="middle">%s</text>'
                 % (x + w // 2, lab))
    h.append('<line class="flow" x1="182" y1="108" x2="228" y2="108"/>')
    h.append('<line class="flow" x1="372" y1="108" x2="418" y2="108"/>')
    h.append('</svg>')
    return ''.join(h)


POWER = fig_power()


# ── ㉘ 같은 600킬로와트를 보낼 때 전류 ──────────────────────────────────
# 막대 길이가 곧 암페어 값이다. 750A 가 눈에 안 띄게 작은 것이 이 그림의 요점이다.
_CURRENT = [('48V 로 600kW', 12500, '12,500A'), ('800V 로 600kW', 750, '750A')]


def fig_current():
    h = ['<svg viewBox="0 0 600 190" role="img" aria-label="같은 600킬로와트를 48볼트로 '
         '보낼 때와 800볼트로 보낼 때의 전류">']
    h.append('<text x="190" y="36" class="t-head">같은 600킬로와트를 보낼 때 전류</text>')
    for i, (lab, amp, val) in enumerate(_CURRENT):
        y = 70 + i * 60
        cls = 'bad-box' if i == 0 else 'good-box'
        w = amp * (330.0 / 12500)
        h.append('<text x="178" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 5, lab))
        h.append('<rect x="190" y="%d" width="%.1f" height="28" rx="5" class="%s"/>'
                 % (y - 14, w, cls))
        h.append('<text x="%.0f" y="%d" class="t-val">%s</text>' % (190 + w + 10, y + 5, val))
    h.append('</svg>')
    return ''.join(h)


CURRENT = fig_current()


# ── ㉙ 캡엑스가 늘어난 이유 하나 ────────────────────────────────────────
# 띠 길이가 곧 억 달러 값이다(1,900억 = 420px). 250억은 그중 부품값 상승분이다.
def fig_capex():
    h = ['<svg viewBox="0 0 600 175" role="img" aria-label="한 회사의 2026년 설비투자 '
         '1,900억 달러 가운데 부품값 상승분 250억 달러">']
    h.append('<text x="120" y="44" class="t-head">캡엑스가 늘어난 이유 하나</text>')
    h.append('<rect x="120" y="70" width="420" height="44" rx="8" class="mid-box"/>')
    h.append('<rect x="485" y="70" width="55" height="44" rx="8" class="bad-box"/>')
    h.append('<text x="300" y="128" class="t-sub" text-anchor="middle">'
             '2026년 설비투자 1,900억 달러</text>')
    h.append('<text x="470" y="152" class="t-sub" text-anchor="middle">'
             '그중 부품값 250억</text>')
    h.append('</svg>')
    return ''.join(h)


CAPEX = fig_capex()


# ── ㉚ 가장 먼 두 칩 사이 홉 수 ─────────────────────────────────────────
# 막대 길이가 곧 홉 수다(1홉 = 20px).
_HOPS = [('3D 토러스', 16, '16홉'), ('Boardfly', 7, '7홉')]


def fig_hops():
    h = ['<svg viewBox="0 0 600 165" role="img" aria-label="3D 토러스와 Boardfly 에서 가장 '
         '먼 두 칩 사이의 홉 수">']
    h.append('<text x="200" y="36" class="t-head">가장 먼 두 칩 사이 홉 수</text>')
    for i, (lab, hop, val) in enumerate(_HOPS):
        y = 70 + i * 55
        cls = 'mid-box' if i == 0 else 'good-box'
        w = hop * 20
        h.append('<text x="188" y="%d" class="t-sub" text-anchor="end">%s</text>' % (y + 4, lab))
        h.append('<rect x="200" y="%d" width="%d" height="26" rx="5" class="%s"/>'
                 % (y - 13, w, cls))
        h.append('<text x="%d" y="%d" class="t-val">%s</text>' % (200 + w + 10, y + 4, val))
    h.append('</svg>')
    return ''.join(h)


HOPS = fig_hops()


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
       ('같은 비트에 드는 웨이퍼', WAFER3),
       ('레티클 84장', WSE),
       ('나란히냐 쌓기냐', FOLD),
       ('PCIe 세대별 속도', PCIE),
       ('네트워킹 세 층', NET)]

if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'scratchpad')
    import check_fig
    for name, svg in ALL:
        print(name, '->', check_fig.hits(svg) or 'FAIL 0건')
