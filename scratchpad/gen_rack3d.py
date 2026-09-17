# -*- coding: utf-8 -*-
"""베라 루빈 NVL72 3D 분해도 — 랙에서 HBM4 다이까지 다섯 단을 눌러 들어간다.

외부 3D 모델 없이 Three.js 가 상자·판을 런타임에 만든다. 슬라이더가 조립↔분해를 오가고,
부품을 누르면 이름·개수·규격·출처가 뜨고, 안쪽 단이 있으면 그리로 들어간다.

부품 개수는 값이다(규칙 — 도해 §1). 원문에 있는 개수만 그 수대로 그리고, 셈한 개수는
「셈한 값」, 원문에 없는 배치·개수는 「도식」으로 부품마다 적는다.

    PYTHONIOENCODING=utf-8 python scratchpad/gen_rack3d.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', 'model', 'rack-vera-rubin-nvl72.html')

R = '[260226] 베라 루빈 — 익스트림 코디자인'
GTC = 'NVIDIA GTC 2025 — Built For Reasoning, Vera Rubin, Kyber (영문)'
ISS = '[260416] ISSCC 2026 총정리'
KOR = '[260901] 한국의 조 단위 주권 AI 투자'
NVB = 'NVIDIA 기술 블로그 — Vera Rubin POD (2026)'
TSV_ = 'Transurfing Volatility — Vera Rubin Decoded Pt.4'
SE = 'Schneider Electric NetShelter MGX 랙(NVL72 용) 제품 사양'

# 부품 사전. kind: src(원문 값) · calc(원문에서 셈한 값) · schema(원문에 없는 배치를 도식으로)
P = {
    # ── 홀 ──
    'rackunit': dict(name='VR NVL72 랙', count='42대 (셈한 값)', kind='calc',
                     spec='10MW 를 GPU 한 장 3.3kW(총전력)로 나누면 3,030장, 랙 하나 72장으로 나누면 42대. '
                          '3.3kW 는 InferenceX 대시보드 앱의 칩 상수, 10MW 조건은 루빈 에이전틱 글의 함대 비교다. 줄 배치는 도식',
                     cite='모델링 층 ㉔ check_agentx · 루빈 에이전틱 영문 L152', child='rack'),
    'coolant': dict(name='냉각수 공급·회수관', count='줄마다 2', kind='schema',
                    spec='랙은 100% 액체 냉각이고 트레이마다 좌측 후면 UQD 로 들어와 우측으로 나간다. 홀 배관의 위치·굵기·흐름 방향은 원문에 없어 줄 위 두 관으로만 그렸다. 띠가 움직이는 쪽이 흐름',
                    cite=R + ' L360·L458'),
    'busway': dict(name='전력 레일', count='줄마다 1', kind='schema',
                   spec='랙 전력 셸프가 3상 415~480VAC 를 받아 50VDC 로 낮춘다. 홀 전력선이 레일인지 케이블인지는 원문에 없어 줄 위 레일로만 그렸다',
                   cite=R + ' L523'),
    'aisle': dict(name='통로 바닥', count='—', kind='schema',
                  spec='랙 줄 사이 통로. 폭과 줄 수는 원문에 없어 도식으로만 그렸다', cite='—'),
    # ── 0 랙 ──
    'rackframe': dict(name='MGX 랙 프레임', count='1', kind='src',
                      spec='48U, 높이 2,236mm × 폭 600mm × 깊이 1,200mm. 랙 전체 부품 약 130만 개·칩 약 1,300개·무게 약 4,000파운드. 치수는 GB 세대 NVL72 용 MGX 랙 제품 사양이다',
                      cite=SE + ' · ' + NVB),
    'tray': dict(name='컴퓨트 트레이', count='18개', kind='src',
                 spec='GPU 72 · Vera 36 을 트레이 18개에 나눠 담는다. 조립 시간 2시간 → 5분, 케이블·호스·팬 없는 모듈 10개 구조. 트레이 높이와 랙 안 위아래 순서는 도식',
                 cite=NVB + ' · ' + R + ' L166·L220', child='tray'),
    'switchtray': dict(name='NVLink 스위치 트레이', count='9개', kind='src',
                       spec='트레이 9개에 NVLink 6 스위치 ASIC 36개. 트레이당 4개는 36 ÷ 9 로 셈한 값',
                       cite=NVB + ' · ' + R + ' L166'),
    'switch': dict(name='NVLink 6 스위치 ASIC', count='36개 (트레이당 4개, 셈한 값)', kind='src',
                   spec='랙당 칩 수 36개로 두 배, 칩 하나 대역폭 28.8T 는 NVLink 5 와 같다',
                   cite=R + ' L156·L166'),
    'spine': dict(name='NVLink 스파인 카트리지', count='4개', kind='src',
                  spec='미리 조립한 구리 케이블 카트리지 4개에 케이블 5,000가닥, 합친 길이 2마일 넘음. 랙 뒤쪽 세로 배치는 도식',
                  cite=NVB),
    'shelf': dict(name='전력 셸프', count='4개', kind='src',
                  spec='110kW 셸프 4개(N+1 이중화), 3상 415~480VAC 를 50VDC 로 낮춰 버스바에 공급. 랙 TDP 180~220kW',
                  cite=R + ' L522·L523'),
    'busbar': dict(name='후면 버스바', count='1', kind='src',
                   spec='50VDC 가 랙 후면 버스바 클립으로 트레이에 들어간다', cite=R + ' L395'),
    'manifold': dict(name='냉각수 배관', count='—', kind='schema',
                     spec='원문은 트레이마다 냉각수가 좌측 후면 UQD 로 들어와 내부 매니폴드를 거쳐 우측 후면 UQD 로 나간다고 적었다. 랙 쪽 배관 모양은 원문에 없어 좌우 기둥으로만 그렸다',
                     cite=R + ' L360·L376'),
    # ── 1 트레이 ──
    'strata': dict(name='Strata 모듈', count='트레이당 2개', kind='src',
                   spec='GB200/300 의 Bianca 보드에 해당. Rubin GPU 2개 + Vera CPU 1개, SOCAMM 소켓 8개. 후면 배치',
                   cite=R + ' L221·L240', child='strata'),
    'midplane': dict(name='미드플레인', count='1개', kind='src',
                     spec='Strata 와 전면 모듈 사이 PCIe 신호를 잇는 다리. 새로 생긴 유일한 모듈', cite=R + ' L242'),
    'orchid': dict(name='Orchid 모듈', count='트레이당 4개', kind='src',
                   spec='ConnectX-9 NIC 2개 · 800G 트랜시버 케이지 2개 · E1.S SSD 슬롯 1개. 전면 좌우에 2개씩 쌓인다',
                   cite=R + ' L241'),
    'cx9': dict(name='ConnectX-9 NIC', count='Orchid 당 2개', kind='src',
                spec='800G, PCIe6 스위치 48레인. InfiniBand 와 800G 이더넷. 미드플레인에서 PCIe6 신호를 받는다',
                cite=R + ' L157·L241'),
    'cage': dict(name='800G 트랜시버 케이지', count='Orchid 당 2개', kind='src',
                 spec='NIC 를 전면으로 옮겨 200G 이더넷 신호가 케이블 없이 케이지 바로 옆에서 끝난다', cite=R + ' L241·L313'),
    'e1s': dict(name='E1.S SSD 슬롯', count='Orchid 당 1개', kind='src',
                spec='로컬 NVMe 저장장치. Orchid 모듈의 ConnectX-9 가 관리한다', cite=R + ' L241·L277'),
    'uqd': dict(name='UQD (냉각수 입출구)', count='2개', kind='src',
                spec='냉각수가 좌측 후면 UQD 로 들어가 내부 매니폴드에서 모듈마다 나뉘고 우측 후면 UQD 로 나온다. 모듈 콜드플레이트는 MQD 로 매니폴드에 붙는다',
                cite=R + ' L360·L376'),
    'clip': dict(name='버스바 클립', count='1', kind='src',
                 spec='50VDC 가 랙 후면 버스바 클립으로 들어와 좌·우 Strata 에는 직접, 전면 전력분배보드에는 미드플레인 아래 버스바로 간다. 클립 모양은 도식',
                 cite=R + ' L395'),
    'paladin': dict(name='Paladin HD2 커넥터', count='미드플레인 앞뒤', kind='schema',
                    spec='신호는 Strata → Paladin HD2 → PCB 미드플레인 → Paladin HD2 → 딸 모듈 순서로 간다. 커넥터 수와 자리는 원문에 없어 띠로만 그렸다',
                    cite=R + ' L305·L306'),
    'chassis': dict(name='트레이 섀시', count='1', kind='schema',
                    spec='모듈마다 작은 금속 섀시가 있고 섀시가 모듈을 미드플레인·매니폴드에 맞춰 끼운다(블라인드 메이트). 바깥 트레이 판의 모양은 도식',
                    cite=R + ' L448'),
    'manifoldi': dict(name='트레이 내부 매니폴드', count='1', kind='src',
                      spec='좌측 UQD 에서 들어온 냉각수를 모듈 콜드플레이트로 나누고 우측 UQD 로 모은다. 관 모양은 도식',
                      cite=R + ' L360'),
    'bf4': dict(name='BlueField-4 모듈', count='1개', kind='src',
                spec='전면 중앙 DPU. 온보드 LPDDR5x 128GB · SSD 512GB · AST2600 BMC. KV 캐시 전용 3번째 네트워크(ICMS/CMX)의 핵심 실리콘',
                cite=R + ' L222·L243'),
    'pwr': dict(name='전력 공급 모듈', count='1개', kind='src',
                spec='50V 를 12V 로 낮춰 전면 모듈에 나눈다. 전면 가운데 BlueField-4 위쪽(평면도 기준)', cite=R + ' L244 · ' + TSV_),
    'mgmt': dict(name='시스템 관리 모듈', count='1개', kind='src',
                 spec='SMM · TPM · DC-SCM 등 보안·관리. 전면 가운데 BlueField-4 아래쪽(평면도 기준)', cite=R + ' L245 · ' + TSV_),
    # ── 2 Strata ──
    'rubin': dict(name='Rubin GPU 패키지', count='Strata 당 2개', kind='src',
                  spec='3nm, 레티클 크기 다이 2개 + HBM 8스택. FP4 35 PFLOPS, TDP 최대 2,300W(Max-P)',
                  cite=R + ' L98·L103·L105', child='rubin'),
    'vera': dict(name='Vera CPU', count='Strata 당 1개', kind='src',
                 spec='88코어·176스레드, L3 162MB, NVLink-C2C 1.8TB/s 로 Rubin 에 연결, PCIe6·CXL3.1',
                 cite=R + ' L135·L137·L142'),
    'socamm': dict(name='SOCAMM (LPDDR5X)', count='8개', kind='src',
                   spec='192GB·128GB 두 종류, Vera 하나에 1,024GB~1,536GB, 9,600MT/s. 두 줄 배치는 도식',
                   cite=R + ' L136·L240'),
    'strataboard': dict(name='Strata 보드', count='1', kind='src',
                        spec='GPU·CPU·SOCAMM 이 올라가는 판. 아래는 전부 보드-투-보드 커넥터라 케이블이 없다', cite=R + ' L240'),
    'coldplate': dict(name='Strata 콜드플레이트', count='1개', kind='src',
                      spec='GPU 2개 + CPU + SOCAMM 을 한 판으로 통째 덮는다. Rubin 쪽은 채널 간격 100마이크론 MCCP',
                      cite=R + ' L361·L369'),
    # ── 3 Rubin 패키지 ──
    'die': dict(name='GPU 연산 다이', count='패키지당 2개', kind='src',
                spec='3nm 레티클 크기 다이. Rubin 트랜지스터 3,360억 개', cite=R + ' L98·L121'),
    'hbm': dict(name='HBM4 스택', count='패키지당 8개', kind='src',
                spec='패키지 합계 288GB, 대역폭 22TB/s(초기 출하는 20TB/s 에 못 미칠 수 있다). 스택 배치는 도식',
                cite=GTC + ' L99 · ' + R + ' L104·L118', child='hbm'),
    'interposer': dict(name='인터포저', count='1', kind='schema',
                       spec='다이와 HBM 을 나란히 올리는 2.5D 판. Rubin 의 인터포저 종류는 이 원문에 없다', cite='—'),
    'substrate': dict(name='패키지 기판', count='1', kind='schema', spec='원문에 규격 없음', cite='—'),
    'lid': dict(name='히트스프레더 + 강성보강재', count='1', kind='src',
                spec='강성보강재를 더하고 액체금속 TIM2 부식을 막으려 금도금. B200·B300 은 덮개만 있었다',
                cite=R + ' L128'),
    # ── 4 HBM4 스택 ──
    'dram': dict(name='DRAM 코어 다이', count='12단', kind='src',
                 spec='12-Hi, 원문 표기로 층 밀도 24 GB(24Gb). 288GB 를 8스택 × 12층으로 나누면 층당 3GB·스택당 36GB. 버스 폭 2,048비트',
                 cite=GTC + ' L99'),
    'base': dict(name='베이스(로직) 다이', count='1', kind='src',
                 spec='HBM4 부터 로직 공정으로 따로 만든다 — SK하이닉스 N12, 삼성 SF4. 코어 다이는 삼성 1c D램',
                 cite=ISS + ' L79·L84 · ' + KOR + ' L244'),
    'tsv': dict(name='TSV 영역', count='—', kind='schema',
                spec='다이를 수직으로 잇는 관통 전극. HBM4 는 TSV 영역이 넓어져 다이가 20% 커졌다. 전극 수는 원문에 없어 띠로만 그렸다',
                cite='[250812] HBM 로드맵 L702'),
}

LEVELS = [
    ('hall', '10MW 홀', '루빈 랙 42대 — GPU 3,030장 × 3.3kW ≈ 10MW, 한 대를 누르면 랙 안으로 들어간다'),
    ('rack', '랙', 'VR NVL72 랙 — 컴퓨트 트레이 18 · NVLink 스위치 트레이 9 · 전력 셸프 4 · 스파인 카트리지 4'),
    ('tray', '컴퓨트 트레이', '후면 Strata 2 · 가운데 미드플레인 · 전면 Orchid 4 + BlueField-4·전력·관리'),
    ('strata', 'Strata', 'Rubin GPU 2 + Vera CPU 1 + SOCAMM 8, 콜드플레이트 한 판'),
    ('rubin', 'Rubin 패키지', '연산 다이 2 + HBM4 스택 8'),
    ('hbm', 'HBM4 스택', 'DRAM 코어 다이 12단 + 로직 베이스 다이'),
]

SOURCES = [
    (R, 'content/newsletter/ai_infra/compute/[260226] 베라 루빈 - 익스트림 코디자인, 그레이스 블랙웰 오베론에서의 진화.md'),
    (GTC, 'input/clippings/NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman.md'),
    (ISS, 'content/newsletter/ai_infra/memory/[260416] ISSCC 2026 총정리 - HBM4, LPDDR6, CPO, 액티브 LSI 등 차세대 메모리·인터커넥트.md'),
    (KOR, 'content/newsletter/ai_infra/business/[260901] 한국의 조 단위 주권 AI 투자 - 엔비디아는 웃고 하이닉스는 운다.md'),
    ('[250812] HBM 로드맵', 'content/newsletter/ai_infra/memory/[250812] HBM 로드맵 - 메모리 벽을 넘는 HBM의 부상과 미래.md'),
    (NVB, 'https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/'),
    (TSV_, 'https://transurfing-volatility.com/vera-rubin-decoded-pt4/'),
    (SE, 'https://www.se.com/us/en/product/SEORNVL72X3000/'),
]

PAGE = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>베라 루빈 랙 분해도</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>
:root{--bg:#f6f6f3;--card:#fff;--ink:#1d1d1b;--ink2:#55534e;--ink3:#8d8a83;--line:#dedcd5;--sel:#2a2a28;--mesh0:#e2e0da;--mesh1:#cfcdc7;--mesh2:#b7b5af;--mesh3:#9d9b95}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141416;--card:#1c1c1f;--ink:#ecebe6;--ink2:#b3b1aa;--ink3:#86847e;--line:#2d2d31;--sel:#ffffff;--mesh0:#6f6e6a;--mesh1:#8a8984;--mesh2:#a6a5a0;--mesh3:#c9c8c3}}
:root[data-theme="dark"]{--bg:#141416;--card:#1c1c1f;--ink:#ecebe6;--ink2:#b3b1aa;--ink3:#86847e;--line:#2d2d31;--sel:#ffffff;--mesh0:#6f6e6a;--mesh1:#8a8984;--mesh2:#a6a5a0;--mesh3:#c9c8c3}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:20px 16px 48px}
h1{font-size:22px;line-height:1.4;margin:6px 0 4px}
.lede{color:var(--ink2);margin:0 0 14px;max-width:760px}
.crumb{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:8px 0}
.crumb button{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:4px 12px;font:inherit;font-size:13px;cursor:pointer}
.crumb button[aria-current="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.crumb span{color:var(--ink3);font-size:12px}
.stage{position:relative;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
#view{display:block;width:100%;height:min(62vh,560px);touch-action:none}
.tip{position:absolute;pointer-events:none;background:var(--ink);color:var(--bg);font-size:12px;padding:3px 8px;border-radius:6px;display:none;white-space:nowrap}
.hint{position:absolute;left:12px;bottom:10px;font-size:12px;color:var(--ink3)}
.ctrl{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:12px 0}
.ctrl label{font-size:13px;color:var(--ink2)}
.ctrl input[type=range]{width:220px;accent-color:var(--ink)}
.ctrl button{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:8px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:760px){.grid{grid-template-columns:1fr}.ctrl input[type=range]{width:160px}}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.panel h2{font-size:15px;margin:0 0 8px}
.parts{list-style:none;margin:0;padding:0}
.parts li button{width:100%;text-align:left;border:0;border-bottom:1px solid var(--line);background:none;color:var(--ink);font:inherit;font-size:14px;padding:7px 2px;cursor:pointer;display:flex;justify-content:space-between;gap:10px}
.parts li button:hover,.parts li button[aria-pressed="true"]{font-weight:700}
.parts small{color:var(--ink3);white-space:nowrap}
.info dt{font-size:12px;color:var(--ink3);margin-top:8px}
.info dd{margin:2px 0 0}
.kind{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:999px;padding:0 8px;color:var(--ink2);margin-left:6px}
.go{margin-top:12px;border:1px solid var(--ink);background:var(--ink);color:var(--bg);border-radius:8px;padding:6px 14px;font:inherit;font-size:13px;cursor:pointer}
.src{font-size:13px;color:var(--ink2)}
.src code{font-size:12px;word-break:break-all}
.back{font-size:13px;color:var(--ink2)}
.back a{color:var(--ink)}
</style>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>
</head>
<body>
<div class="wrap">
<p class="back"><a href="../모델링 대시보드.html">← 모델링 대시보드</a></p>
<h1>베라 루빈 NVL72 — 10MW 홀에서 HBM4 다이까지 분해도</h1>
<p class="lede">10MW 홀 → 랙 → 컴퓨트 트레이 → Strata → Rubin 패키지 → HBM4 스택 여섯 단을 눌러 들어갑니다. 슬라이더로 조립과 분해를 오가고, 부품을 누르면 개수·규격·출처가 뜹니다. 개수는 원문에 적힌 수대로 그렸고, 원문에서 셈한 개수와 원문에 없는 배치는 부품마다 따로 표시했습니다. 크기 비율은 실제와 다릅니다.</p>
<div class="crumb" id="crumb"></div>
<div class="stage"><canvas id="view"></canvas><div class="tip" id="tip"></div><div class="hint">끌어서 돌리기 · 휠로 확대 · 부품 누르기</div></div>
<div class="ctrl">
  <label for="ex">분해</label><input id="ex" type="range" min="0" max="1" step="0.01" value="0.35">
  <button id="play">조립 ↔ 분해</button><button id="reset">시점 처음으로</button>
</div>
<div class="grid">
  <div class="panel"><h2 id="lvtitle"></h2><p class="src" id="lvsub"></p><ul class="parts" id="parts"></ul></div>
  <div class="panel info" id="info"><h2>부품을 누르세요</h2><p class="src">화면의 부품이나 왼쪽 목록을 누르면 여기에 설명이 뜹니다.</p></div>
</div>
<div class="panel" style="margin-top:14px"><h2>출처</h2><ul class="src" id="srcs"></ul>
<p class="src">성격 표시 — <b>원문 값</b>: 원문에 적힌 수 · <b>셈한 값</b>: 원문 값으로 셈한 수 · <b>도식</b>: 원문에 없는 배치나 모양을 그림으로만 둔 것.</p></div>
</div>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const P = __PARTS__;
const LEVELS = __LEVELS__;
const SOURCES = __SOURCES__;
const KIND = {src:'원문 값', calc:'셈한 값', schema:'도식'};

const canvas = document.getElementById('view');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, matchMedia('(max-width: 760px)').matches ? 1.5 : 2));
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 5000);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
const SMALL = matchMedia('(max-width: 760px)').matches;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.shadowMap.enabled = !SMALL; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.add(new THREE.HemisphereLight(0xffffff, 0x3a3a3a, 0.35));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.0004; scene.add(sun); scene.add(sun.target);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.ShadowMaterial({opacity: .18}));
ground.rotation.x = -Math.PI/2; ground.receiveShadow = true; scene.add(ground);
let dirty = true;
const MAT = {glass:[.05,.1], metal:[.85,.32], pcb:[.05,.72], die:[.35,.22], silicon:[.55,.28], plastic:[0,.6]};
const KINDMAT = {coolant:'metal', busway:'metal', uqd:'metal', clip:'metal', paladin:'plastic', chassis:'metal', manifoldi:'metal', rackunit:'metal', aisle:'plastic', rackframe:'glass', busbar:'metal', manifold:'metal', spine:'metal', shelf:'metal', tray:'metal',
  switchtray:'metal', switch:'die', strata:'pcb', strataboard:'pcb', midplane:'pcb', orchid:'pcb', bf4:'pcb',
  pwr:'metal', mgmt:'pcb', coldplate:'metal', rubin:'die', vera:'die', socamm:'pcb', die:'die', hbm:'die',
  interposer:'silicon', substrate:'pcb', lid:'metal', dram:'silicon', base:'silicon', tsv:'glass',
  cx9:'die', cage:'metal', e1s:'plastic'};

const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
function tone(i){ return new THREE.Color(css(['--mesh0','--mesh1','--mesh2','--mesh3'][i])); }

let group = null, items = [], level = 'rack', selected = null, explode = +document.getElementById('ex').value;

// 부품 하나 = 상자. a 는 조립 위치, e 는 분해 방향(분해 1.0 일 때 더해지는 벡터)
function box(id, size, a, e, t, opts={}){
  const r = Math.min(Math.min(...size) * 0.22, 1.2);
  const g = r > 0.05 ? new RoundedBoxGeometry(size[0], size[1], size[2], 2, r) : new THREE.BoxGeometry(...size);
  const [metal, rough] = MAT[opts.mat || KINDMAT[id] || 'plastic'];
  const m = new THREE.MeshStandardMaterial({color: tone(t), roughness: rough, metalness: metal, envMapIntensity: .9,
    transparent: !!opts.op, opacity: opts.op || 1, depthWrite: !opts.op});
  const mesh = new THREE.Mesh(g, m);
  mesh.castShadow = !opts.op; mesh.receiveShadow = true;
  if (opts.op) {
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(...size)),
      new THREE.LineBasicMaterial({color: tone(3), transparent:true, opacity:.5}));
    mesh.add(edges);
  }
  mesh.userData = {id, a:new THREE.Vector3(...a), e:new THREE.Vector3(...e), t, o: 0};
  group.add(mesh); items.push(mesh);
  return mesh;
}

// 분해 순서: 멀리 가는 부품일수록 늦게 출발한다. 0~1 로 매긴다
function order(){
  const mags = items.map(m => m.userData.e.length()), mx = Math.max(1e-6, ...mags);
  items.forEach((m, i) => { m.userData.o = mags[i] / mx; });
}

const flowTex = [];
function stripe(dark, light){
  const cv = document.createElement('canvas'); cv.width = 64; cv.height = 8;
  const g = cv.getContext('2d'); g.fillStyle = dark; g.fillRect(0, 0, 64, 8);
  g.fillStyle = light; g.fillRect(0, 0, 22, 8);
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
function pipe(id, len, radius, pos, e, dark, light, dir){
  const t = stripe(dark, light); t.repeat.set(len / 40, 1); t.userData = {dir};
  flowTex.push(t);
  const g = new THREE.CylinderGeometry(radius, radius, len, 16, 1, false);
  g.rotateZ(Math.PI / 2);
  const m = new THREE.MeshStandardMaterial({map: t, roughness: .4, metalness: .5});
  const mesh = new THREE.Mesh(g, m);
  mesh.castShadow = true;
  mesh.userData = {id, a: new THREE.Vector3(...pos), e: new THREE.Vector3(...e), t: 2, o: 0, keep: true};
  group.add(mesh); items.push(mesh);
  return mesh;
}

const RACK_SLOTS = ['shelf','shelf'].concat(Array(9).fill('tray'), Array(9).fill('switchtray'), Array(9).fill('tray'), ['shelf','shelf']);
let frontTex = null;
function rackFront(){
  if (frontTex) return frontTex;
  const cv = document.createElement('canvas'); cv.width = 256; cv.height = 954;   // 600 × 2,236 비율
  const g = cv.getContext('2d');
  g.fillStyle = '#2b2b2b'; g.fillRect(0, 0, cv.width, cv.height);
  const slotH = 5.2 / 223.6 * cv.height, top = (cv.height - RACK_SLOTS.length * slotH) / 2;
  RACK_SLOTS.forEach((k, i) => {
    const y = top + i * slotH;
    g.fillStyle = k === 'tray' ? '#5d5d5b' : (k === 'switchtray' ? '#8a8986' : '#b9b8b3');
    g.fillRect(10, y + 1.5, cv.width - 20, slotH - 3);
    if (k === 'tray') {           // 트레이 앞 좌우 Orchid 트랜시버 케이지 자리 — 개수는 Orchid 당 2(원문), 좌우 두 줄은 도식
      g.fillStyle = '#1f1f1f';
      for (const x of [22, 52, cv.width - 82, cv.width - 52]) g.fillRect(x, y + slotH * 0.28, 26, slotH * 0.44);
    }
  });
  frontTex = new THREE.CanvasTexture(cv); frontTex.colorSpace = THREE.SRGBColorSpace; frontTex.anisotropy = 8;
  return frontTex;
}

const BUILD = {
  hall(){
    // 42대 = 10MW ÷ 3.3kW ÷ 72 (셈한 값). 7대씩 6줄로 세운 배치는 도식
    const W = 60, D = 120, H = 223.6, per = 7, rows = 6, gapX = 8, aisle = 140;
    let n = 0;
    for (let r = 0; r < rows; r++) {
      const z = (r - (rows - 1) / 2) * (D + aisle / 2) + (r % 2 ? -aisle / 4 : aisle / 4);
      for (let c = 0; c < per; c++, n++) {
        const x = (c - (per - 1) / 2) * (W + gapX);
        const rk = box('rackunit', [W, H, D], [x, H / 2, z], [(c - (per - 1) / 2) * 14, 0, (r - (rows - 1) / 2) * 26], 3);
        const face = new THREE.Mesh(new THREE.PlaneGeometry(W - 2, H - 2),
          new THREE.MeshStandardMaterial({map: rackFront(), roughness: .55, metalness: .3}));
        face.position.z = (r % 2 ? 1 : -1) * (D / 2 + 0.3);
        if (!(r % 2)) face.rotation.y = Math.PI;
        rk.add(face);
      }
    }
    box('aisle', [per * (W + gapX) + 120, 2, rows * (D + aisle / 2) + 120], [0, -1, 0], [0, 0, 0], 0);
    // 줄마다 위로 공급·회수관 둘과 전력 레일 하나(도식). 공급은 +x, 회수는 -x 로 흐른다
    const len = per * (W + gapX) + 60;
    for (let r = 0; r < rows; r++) {
      const z = (r - (rows - 1) / 2) * (D + aisle / 2) + (r % 2 ? -aisle / 4 : aisle / 4);
      const up = [0, 70, (r - (rows - 1) / 2) * 26];
      pipe('coolant', len, 4.5, [0, H + 30, z - 18], up, '#6f6e6a', '#d9d8d3', 1);
      pipe('coolant', len, 4.5, [0, H + 30, z + 18], up, '#3d3c3a', '#9d9b95', -1);
      box('busway', [len, 5, 8], [0, H + 14, z], up, 3);
    }
    return {pos: [520, 420, 640], target: [0, 60, 0]};
  },
  rack(){
    // 치수 비율은 MGX 랙(600 × 2,236 × 1,200mm)을 cm 로. 장비는 트레이 18 · 스위치 트레이 9 · 셸프 4.
    // 장비 높이와 위아래 순서는 원문에 없는 도식이다 — 셸프 둘 · 트레이 9 · 스위치 9 · 트레이 9 · 셸프 둘
    const W = 60, D = 120, HR = 223.6, H = 5.2;
    const slots = [];
    for (let i=0;i<2;i++) slots.push('shelf');
    for (let i=0;i<9;i++) slots.push('tray');
    for (let i=0;i<9;i++) slots.push('switchtray');
    for (let i=0;i<9;i++) slots.push('tray');
    for (let i=0;i<2;i++) slots.push('shelf');
    const total = slots.length * H;
    let y = total/2;
    slots.forEach((id, i) => {
      const cy = y - H/2; y -= H;
      const k = slots.length/2 - i;
      box(id, [W-4, H*0.86, D-10], [0, cy, 0], [0, k*2.0, 0], id==='tray'?1:(id==='switchtray'?2:0));
      if (id === 'switchtray') for (let c=0;c<4;c++)
        box('switch', [6, 1.0, 6], [-16 + c*10.7, cy + H*0.43 + 0.5, -10], [0, k*2.0 + 1.6, 0], 3);
    });
    box('rackframe', [W, HR, D], [0, 0, 0], [0, 0, 0], 0, {op:.08});
    for (let c=0;c<4;c++) box('spine', [4, total*0.5, 3], [-18 + c*12, 0, -D/2 + 3], [0, 0, -36 - c*3], 3);
    box('busbar', [3, total, 2], [0, 0, -D/2 - 1], [0, 0, -18], 2);
    box('manifold', [2.2, total, 2.2], [-W/2 + 2, 0, -D/2 + 1], [-22, 0, -20], 2);
    box('manifold', [2.2, total, 2.2], [W/2 - 2, 0, -D/2 + 1], [22, 0, -20], 2);
    return {pos:[170, 60, 190], target:[0,0,0]};
  },
  tray(){
    box('strata', [27, 1.2, 38], [-14.5, 0, -24], [-10, 0, -40], 1);
    box('strata', [27, 1.2, 38], [14.5, 0, -24], [10, 0, -40], 1);
    box('midplane', [58, 4, 1.2], [0, 1.4, 0], [0, 12, 0], 2);
    for (const sx of [-1, 1]) for (const k of [0, 1]) {
      const ay = -0.4 + k*2.2, ex = [sx*12, k*8, 36];
      box('orchid', [16, 1.0, 30], [sx*20, ay, 19], ex, 1);
      for (const q of [-1, 1]) box('cx9', [4, 0.6, 4], [sx*20 + q*3.8, ay + 0.8, 12], ex, 3);
      for (const q of [-1, 1]) box('cage', [5.6, 1.4, 5], [sx*20 + q*3.8, ay + 1.1, 31], ex, 2);
      box('e1s', [3.2, 0.5, 11], [sx*20, ay + 0.75, 22], ex, 0);
    }
    box('pwr', [18, 1.2, 8], [0, 1.6, 7], [0, 6, 18], 0);
    box('bf4', [18, 1.2, 12], [0, 1.6, 19], [0, 12, 36], 2);
    box('mgmt', [18, 1.2, 6], [0, 1.6, 30], [0, 6, 54], 0);
    // 섀시 판(도식) — 모듈 아래로 내려간다
    box('chassis', [62, 0.6, 90], [0, -1.6, 0], [0, -14, 0], 0);
    // 미드플레인 앞뒤 커넥터 띠(도식) — 미드플레인과 같이 움직인다
    for (const z of [-1.4, 1.4]) box('paladin', [52, 1.4, 1.0], [0, 0.4, z], [0, 12, z * 3], 3);
    // 후면 UQD 2 · 버스바 클립 · 내부 매니폴드
    for (const sx of [-1, 1]) box('uqd', [3.2, 3.2, 4], [sx * 27, 0.6, -45], [sx * 6, 0, -22], 2);
    box('clip', [8, 3.4, 3], [0, 0.6, -45.5], [0, 0, -26], 3);
    box('manifoldi', [56, 1.2, 1.6], [0, 1.2, -43], [0, 6, -14], 2);
    return {pos:[70, 70, 90], target:[0,0,0]};
  },
  strata(){
    box('coldplate', [26, 1.2, 36], [0, 3.2, 0], [0, 26, 0], 0, {op:.3});
    box('rubin', [9, 1.6, 9], [-6.5, 1.2, -10], [-6, 12, -8], 3);
    box('rubin', [9, 1.6, 9], [6.5, 1.2, -10], [6, 12, -8], 3);
    box('vera', [7, 1.4, 7], [0, 1.1, 4], [0, 10, 2], 2);
    for (let i=0;i<8;i++){
      const row = i < 4 ? 0 : 1, c = i % 4;
      box('socamm', [1.6, 0.8, 10], [-7.5 + c*5 , 0.8, 12 + row*5], [(c-1.5)*3, 6 + row*2, 8 + row*4], 1);
    }
    box('strataboard', [26, 0.6, 36], [0, 0, 0], [0, -6, 0], 0);
    return {pos:[40, 38, 44], target:[0,0,0]};
  },
  rubin(){
    box('substrate', [16, 0.8, 14], [0, 0, 0], [0, -6, 0], 0);
    box('interposer', [12, 0.4, 10], [0, 0.6, 0], [0, -2, 0], 1);
    box('die', [3.2, 0.5, 4.6], [-1.9, 1.05, 0], [-2, 2, 0], 3);
    box('die', [3.2, 0.5, 4.6], [1.9, 1.05, 0], [2, 2, 0], 3);
    for (let i=0;i<8;i++){
      const side = i < 4 ? -1 : 1, k = i % 4;
      box('hbm', [1.6, 1.2, 2.0], [side*5.0, 1.4, -3.3 + k*2.2], [side*4, 3 + k*0.4, (k-1.5)*1.2], 2);
    }
    box('lid', [15, 0.5, 13], [0, 2.4, 0], [0, 10, 0], 0, {op:.45});
    for (const [w, d, x, z] of [[16, .8, 0, -6.9], [16, .8, 0, 6.9], [.8, 13, -7.6, 0], [.8, 13, 7.6, 0]])
      box('lid', [w, 1.2, d], [x, 1.5, z], [0, 8, 0], 1);
    return {pos:[18, 16, 20], target:[0,0.8,0]};
  },
  hbm(){
    box('base', [8, 0.9, 10], [0, 0, 0], [0, -3, 0], 3);
    for (let i=0;i<12;i++) box('dram', [8, 0.28, 10], [0, 0.75 + i*0.34, 0], [0, i*0.9, 0], i%2?1:0);
    box('tsv', [1.2, 5, 6], [0, 2.4, 0], [9, 0, 0], 2, {op:.5});
    return {pos:[16, 12, 18], target:[0,2.5,0]};
  },
};

function fit(dirv){
  const b = new THREE.Box3().setFromObject(group), c = b.getCenter(new THREE.Vector3()), sz = b.getSize(new THREE.Vector3());
  const r = sz.length() / 2, fov = camera.fov * Math.PI / 180;
  const aspect = Math.max(0.6, canvas.clientWidth / Math.max(1, canvas.clientHeight));
  const dist = r / Math.sin(fov / 2) / Math.min(1, aspect) * 1.05;
  const d = new THREE.Vector3(...dirv).normalize();
  camera.position.copy(c).addScaledVector(d, dist); camera.near = dist / 100; camera.far = dist * 10; camera.updateProjectionMatrix();
  controls.target.copy(c); controls.update();
  const span = Math.max(sz.x, sz.y, sz.z);
  ground.scale.set(span * 6, span * 6, 1); ground.position.set(c.x, b.min.y - span * 0.02, c.z);
  sun.position.set(c.x + span * 0.8, c.y + span * 1.6, c.z + span * 1.1); sun.target.position.copy(c);
  const sc = sun.shadow.camera; sc.left = sc.bottom = -span * 1.2; sc.right = sc.top = span * 1.2;
  sc.near = span * 0.1; sc.far = span * 5; sc.updateProjectionMatrix();
  dirty = true;
}

const SPREAD = 0.55;
function layout(){
  for (const m of items){
    const {a, e, o} = m.userData;
    let k = Math.min(1, Math.max(0, explode * (1 + SPREAD) - o * SPREAD));
    k = k * k * (3 - 2 * k);
    m.position.set(a.x + e.x*k, a.y + e.y*k, a.z + e.z*k);
  }
  dirty = true;
}

function paint(){
  for (const m of items){
    const on = selected && m.userData.id === selected;
    m.material.color = on ? new THREE.Color(css('--sel')) : tone(m.userData.t);
    m.material.emissive = new THREE.Color(on ? 0x1a1a1a : 0x000000);
  }
  dirty = true;
}

function load(lv, keepCam){
  if (group) { scene.remove(group); group.traverse(o=>{o.geometry&&o.geometry.dispose();o.material&&o.material.dispose&&o.material.dispose();}); }
  flowTex.forEach(t => t.dispose()); flowTex.length = 0;
  group = new THREE.Group(); items = []; scene.add(group);
  level = lv; selected = null;
  const cam = BUILD[lv]();
  order(); layout(); paint();
  if (!keepCam) fit(cam.pos);
  const L = LEVELS.find(x=>x[0]===lv);
  document.getElementById('lvtitle').textContent = L[1] + ' — 부품';
  document.getElementById('lvsub').textContent = L[2];
  const ids = [...new Set(items.map(m=>m.userData.id))];
  const ul = document.getElementById('parts'); ul.innerHTML = '';
  for (const id of ids){
    const li = document.createElement('li'), b = document.createElement('button');
    b.innerHTML = `<span>${P[id].name}</span><small>${P[id].count}</small>`;
    b.onclick = () => select(id); b.dataset.id = id; li.appendChild(b); ul.appendChild(li);
  }
  crumb();
  document.getElementById('info').innerHTML = '<h2>부품을 누르세요</h2><p class="src">화면의 부품이나 왼쪽 목록을 누르면 여기에 설명이 뜹니다.</p>';
  location.hash = lv;
}

function crumb(){
  const el = document.getElementById('crumb'); el.innerHTML = '';
  const idx = LEVELS.findIndex(x=>x[0]===level);
  LEVELS.slice(0, idx+1).forEach((L, i) => {
    if (i) { const s = document.createElement('span'); s.textContent = '›'; el.appendChild(s); }
    const b = document.createElement('button'); b.textContent = L[1];
    b.setAttribute('aria-current', i===idx ? 'true' : 'false');
    b.onclick = () => load(L[0]); el.appendChild(b);
  });
}

function select(id){
  selected = id; paint();
  document.querySelectorAll('#parts button').forEach(b => b.setAttribute('aria-pressed', b.dataset.id===id));
  const p = P[id];
  const child = p.child && p.child !== level ? `<button class="go" id="go">${LEVELS.find(x=>x[0]===p.child)[1]} 안으로 들어가기 →</button>` : '';
  document.getElementById('info').innerHTML =
    `<h2>${p.name}<span class="kind">${KIND[p.kind]}</span></h2>
     <dl><dt>개수</dt><dd>${p.count}</dd><dt>규격·역할</dt><dd>${p.spec}</dd><dt>출처</dt><dd class="src">${p.cite}</dd></dl>${child}`;
  const go = document.getElementById('go'); if (go) go.onclick = () => load(p.child);
}

const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(), tip = document.getElementById('tip');
function pick(ev){
  const r = canvas.getBoundingClientRect();
  ptr.set(((ev.clientX - r.left)/r.width)*2-1, -((ev.clientY - r.top)/r.height)*2+1);
  ray.setFromCamera(ptr, camera);
  const hit = ray.intersectObjects(items, false)[0];
  return {hit, x: ev.clientX - r.left, y: ev.clientY - r.top};
}
canvas.addEventListener('pointermove', ev => {
  const {hit, x, y} = pick(ev);
  if (hit){ tip.style.display='block'; tip.textContent = P[hit.object.userData.id].name; tip.style.left = (x+12)+'px'; tip.style.top = (y+12)+'px'; canvas.style.cursor='pointer'; }
  else { tip.style.display='none'; canvas.style.cursor='grab'; }
});
let down = null;
canvas.addEventListener('pointerdown', ev => { down = [ev.clientX, ev.clientY]; });
canvas.addEventListener('pointerup', ev => {
  if (!down || Math.hypot(ev.clientX-down[0], ev.clientY-down[1]) > 5) return;
  const {hit} = pick(ev);
  if (hit) select(hit.object.userData.id);
});

const ex = document.getElementById('ex');
ex.addEventListener('input', () => { explode = +ex.value; layout(); });
let anim = null;
document.getElementById('play').onclick = () => {
  const from = explode, to = explode > 0.5 ? 0 : 1, t0 = performance.now();
  anim = t => { const k = Math.min(1, (t - t0)/1200), s = k<.5 ? 4*k*k*k : 1-Math.pow(-2*k+2,3)/2;
    explode = from + (to-from)*s; ex.value = explode; layout(); if (k>=1) anim = null; };
};
document.getElementById('reset').onclick = () => load(level);

const srcs = document.getElementById('srcs');
for (const [label, path] of SOURCES){ const li = document.createElement('li'); li.innerHTML = `${label} — <code>${path}</code>`; srcs.appendChild(li); }

function resize(){
  const w = canvas.clientWidth, h = canvas.clientHeight;
  if (canvas.width !== Math.floor(w*renderer.getPixelRatio()) || canvas.height !== Math.floor(h*renderer.getPixelRatio())){
    renderer.setSize(w, h, false); camera.aspect = w/h; camera.updateProjectionMatrix(); dirty = true;
  }
}
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', paint);
controls.addEventListener('change', () => { dirty = true; });
let lastT = 0;
function loop(t){
  resize(); if (anim) anim(t); controls.update();
  const dt = Math.min(0.05, (t - lastT) / 1000); lastT = t;
  if (level === 'hall' && flowTex.length && !SMALL && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    for (const tx of flowTex) tx.offset.x -= tx.userData.dir * dt * 0.6;
    dirty = true;
  }
  if (dirty) { renderer.render(scene, camera); dirty = false; }
  requestAnimationFrame(loop);
}
const start = (location.hash || '').slice(1);
load(LEVELS.some(x=>x[0]===start) ? start : 'hall');
requestAnimationFrame(loop);
window.__rack = {load, select, setExplode: v => { explode = v; ex.value = v; layout(); }, ready: true};
</script>
</body>
</html>
'''


def main():
    html = (PAGE.replace('__PARTS__', json.dumps(P, ensure_ascii=False))
                .replace('__LEVELS__', json.dumps(LEVELS, ensure_ascii=False))
                .replace('__SOURCES__', json.dumps(SOURCES, ensure_ascii=False)))
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('썼다:', OUT, len(html), 'bytes')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
