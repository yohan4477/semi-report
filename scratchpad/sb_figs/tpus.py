# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aie_figs as F  # noqa: E402

# ── TPU 칩 한 장 — HBM에서 TensorCore 안 셋으로 ────────────────────
# 데이터가 HBM에서 VMEM을 거쳐 MXU로 가는 순서가 내용이라 _chain.
_CHIP = F._chain([
    ('HBM', '칩 옆에 쌓은 주 메모리 · TensorCore가 쓰려면 먼저 VMEM으로 옮긴다'),
    ('VMEM', '온칩 저장소 · v5e 128MiB · MXU로 가는 대역폭이 HBM보다 훨씬 높다'),
    ('MXU', '시스톨릭 배열 · 8사이클마다 [8,128]×[128,128] 곱 · v5e 칩당 2e14 bf16 FLOPs/s'),
    ('VPU', 'ReLU 같은 일반 연산 · 벡터 덧셈·곱셈·합산'),
], mark=3)
_CHIP_CAP = ('TPU 한 장은 HBM에 TensorCore를 붙인 기계이고, TensorCore 안은 MXU·VPU·VMEM '
             '셋이다. <b>시간을 먹는 것은 MXU 앞까지 데이터를 옮기는 일</b>이라 저자들은 '
             'HBM→VMEM 복사를 MXU 연산과 겹쳐 돌리는 파이프라인을 먼저 설명한다.')

# ── 칩과 칩 사이 — ICI 토러스와 그 밖 ──────────────────────────────
_NETWORK = F._chain([
    ('칩 ↔ 이웃 칩 (ICI)', 'v5e·v6e는 이웃 넷과 2차원 토러스 · v4·v5p는 이웃 여섯과 3차원 토러스'),
    ('포드', 'v4 16×16×16 · v5p 16×20×28 · v5e·v6e는 16×16에서 끝'),
    ('포드 ↔ 포드 (DCN)', '데이터센터 네트워크 · ICI보다 훨씬 느리다'),
])
_NETWORK_CAP = ('칩은 호스트를 거치지 않고 ICI로 이웃 칩과 직접 이어져 토러스를 이루고, '
                '토러스가 포드 크기까지 자라면 그 밖은 DCN이 잇는다. GPU가 스위치를 겹겹이 쌓아 '
                '모든 칩을 점대점으로 잇는 것과 갈리는 자리다.')

# ── 문제 6 — 대역폭 넷을 한 번에 거치면 ─────────────────────────────
# 순서대로 거치는 경로 넷. 가장 느린 칸(ICI)만 강조한다.
_Q6 = F._chain([
    ('① PCIe', '호스트 DRAM → 각 TPU · 8GB씩 링크 16개 · 약 63ms'),
    ('② ICI', '15GB를 TPU{0,0}로 · 두 축 · 링크당 4.5e10 B/s · 약 167ms'),
    ('③ HBM → MXU', '16e9바이트 · 약 20ms'),
    ('④ 곱셈', '2.7e11 FLOPs ÷ 1.97e14 FLOPs/s · 약 1.4ms'),
], mark=2)
_Q6_CAP = ('int8 행렬 16GB를 v5e 4×4 슬라이스의 호스트에서 TPU{0,0}로 모아 곱하는 경로다. '
           '<b>넷을 겹쳐 돌리면 전체 시간은 가장 느린 ICI 복사 167ms에 가깝게 잡힌다</b>. '
           '겹침이 완벽하지 않으면 200ms에 가까워진다.')

FIGS = {
    'chip': ('TPU 칩 한 장 — 데이터가 MXU까지 가는 길', _CHIP, _CHIP_CAP),
    'network': ('칩과 칩 사이 — ICI 토러스와 그 밖', _NETWORK, _NETWORK_CAP),
    'q6': ('문제 6 — 대역폭 넷을 한 번에 거치면', _Q6, _Q6_CAP),
}
