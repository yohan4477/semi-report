# -*- coding: utf-8 -*-
# 건강 인사이트 대시보드 생성. 채널을 가리지 않고 「몸에서 벌어지는 일」만 모으는 아카이브다.
# 통합 인사이트(insights/)와는 잇지 않는다 — 노트도 원자도 만들지 않는 독립 페이지다.
#
# 이 페이지만의 규칙 둘.
#  1) 카드 단위는 영상이 아니라 주제다. 한 영상에서 여러 주제가 나오면 주제 수만큼 카드를 쪼갠다.
#  2) 새 영상이 이미 있는 카드와 같은 이야기를 하면 카드를 늘리지 않는다. 그 카드의 포인트를
#     보강하고 meta의 출처 편수와 links에 영상을 더한다. 새 카드는 새 주제일 때만 만든다.
#
# 그림은 본문 중간중간에 들어간다 — 몸 이야기는 말로만 하면 안 박힌다. 부품은 card_lib의 figs.
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import health_assets as ha

OUT = os.path.join(dc.ROOT, '대시보드', '건강 대시보드.html')
blob = dc.blob

STAMP = '2026-08-17'
SUM = 'content/health/'

# 출처 한 벌 — 여러 카드가 같은 영상을 나눠 갖고, 한 카드가 여러 영상을 묶기도 한다.
# 카드를 새로 만들기 전에 여기 이미 있는 편으로 보강할 수 있는지부터 본다.
SPK = '이승훈 <b>서울대 신경과 교수</b>'
SPK2 = '조영민 <b>서울대 내분비대사내과 교수</b>'

SRC_EP155 = 'https://youtu.be/ZFzS1UwVgNc'
SUM_EP155 = blob(SUM + '지식인사이드/[260801] 만성 염증의 정체, 과잉 칼로리가 혈관을 '
                 '망가뜨리는 경로 - 이승훈 (1부).md')
SRC_EP156 = 'https://youtu.be/LM-cSnJbanA'
SUM_EP156 = blob(SUM + '지식인사이드/[260802] 당뇨는 포도당 병이 아니라 지방 병이다 - 이승훈 (2부).md')
SRC_EP107 = 'https://youtu.be/NSqZmrp85es'
SUM_EP107 = blob(SUM + '지식인사이드/[260309] 의사를 만나기 전에 내 단계를 안다 - 이승훈 (EP.107).md')
SRC_EP108 = 'https://youtu.be/bgrXlaImNtU'
SUM_EP108 = blob(SUM + '지식인사이드/[260310] 살은 병을 이기는 자산이다 - 이승훈 (EP.108).md')

SRC_LEGEND = 'https://youtu.be/6mmMRFwDwBc'
SUM_LEGEND = blob(SUM + '언더스탠딩/[240918] 뇌출혈·골든타임·혈압약 - 이승훈 레전드 모음집.md')

SRC_NOBEL = 'https://youtu.be/KHSuev5sXGg'
SUM_NOBEL = blob(SUM + '언더스탠딩/[251027] 몸속 배신자 조절 T세포 - 이승훈 (노벨생리의학상 해설).md')
SRC_DOPA = 'https://youtu.be/ai0Id2yBtGM'
SUM_DOPA = blob(SUM + '언더스탠딩/[260712] 도파민은 쾌락이 아니라 희망의 물질이다 - 이승훈.md')

SRC_GLP1 = 'https://youtu.be/n-oxjOCXLSE'
SUM_GLP1 = blob(SUM + '언더스탠딩/[260720] 비만약이 중독까지 줄인다 - 조영민.md')

SRC_3PART = 'https://youtu.be/qHp7iQDuvtw'
SUM_3PART = blob(SUM + '언더스탠딩/[251007] 질병·소화·신약 3부작 - 이승훈 레전드 모음집.md')

META_EP155 = [SPK, '지식인사이드 EP.155', '2026-08-01', '출처 1편']
META_EP156 = [SPK, '지식인사이드 EP.156', '2026-08-02', '출처 1편']
META_EP107 = [SPK, '지식인사이드 EP.107', '2026-03-09', '출처 1편']
META_FRUIT = [SPK, '지식인사이드 EP.156 · 108', '2026-08 · 03', '출처 2편']
META_PROTEIN = [SPK, '지식인사이드 EP.155 · 156 · 107 · 108', '2026-08 · 03', '출처 4편']
META_STAGE = [SPK, '지식인사이드 EP.107 · 155 · 언더스탠딩', '2024-09 · 2026', '출처 3편']
META_WEIGHT = [SPK, '지식인사이드 EP.108 · 107 · 156', '2026-03 · 08', '출처 3편']

META_NOBEL = [SPK, '언더스탠딩 · 노벨생리의학상 해설', '2025-10-27', '출처 1편']
META_DOPA = [SPK, '언더스탠딩 · 뇌과학', '2026-07-12', '출처 1편']

META_GLP1 = [SPK2, '언더스탠딩 · 비만약과 중독', '2026-07-20', '출처 1편']

META_DISEASE = [SPK, '언더스탠딩 3부작 · 질병이란 무엇인가', '2025-10-07', '출처 1편']
META_DRUG = [SPK, '언더스탠딩 3부작 · 소화와 약', '2025-10-07', '출처 1편']

LINKS_EP155 = [('영상 — EP.155', SRC_EP155, ''), ('요약본 전문', SUM_EP155, 'secondary')]
LINKS_EP156 = [('영상 — EP.156', SRC_EP156, ''), ('요약본 전문', SUM_EP156, 'secondary')]
LINKS_EP107 = [('영상 — EP.107', SRC_EP107, ''), ('요약본 전문', SUM_EP107, 'secondary')]
LINKS_FRUIT = [('영상 — EP.156', SRC_EP156, ''), ('영상 — EP.108', SRC_EP108, ''),
               ('요약본 — EP.156', SUM_EP156, 'secondary'), ('요약본 — EP.108', SUM_EP108, 'secondary')]
LINKS_PROTEIN = [('영상 — EP.156', SRC_EP156, ''), ('영상 — EP.108', SRC_EP108, ''),
                 ('영상 — EP.107', SRC_EP107, ''),
                 ('요약본 — EP.156', SUM_EP156, 'secondary'), ('요약본 — EP.107', SUM_EP107, 'secondary')]
LINKS_STAGE = [('영상 — EP.107', SRC_EP107, ''), ('영상 — 언더스탠딩 모음집', SRC_LEGEND, ''),
               ('요약본 — EP.107', SUM_EP107, 'secondary'), ('요약본 — 모음집', SUM_LEGEND, 'secondary')]
LINKS_WEIGHT = [('영상 — EP.108', SRC_EP108, ''), ('영상 — EP.107', SRC_EP107, ''),
                ('요약본 — EP.108', SUM_EP108, 'secondary'), ('요약본 — EP.107', SUM_EP107, 'secondary')]

META_BLEED = [SPK, '언더스탠딩 레전드 모음집', '2024-09-18', '출처 1편']
META_EMERG = [SPK, '지식인사이드 EP.107 · 언더스탠딩', '2026-03 · 2024-09', '출처 2편']
LINKS_BLEED = [('영상 — 언더스탠딩 모음집', SRC_LEGEND, ''), ('요약본 전문', SUM_LEGEND, 'secondary')]
LINKS_EMERG = [('영상 — EP.107', SRC_EP107, ''), ('영상 — 언더스탠딩 모음집', SRC_LEGEND, ''),
               ('요약본 — EP.107', SUM_EP107, 'secondary'), ('요약본 — 모음집', SUM_LEGEND, 'secondary')]


LINKS_NOBEL = [('영상 — 언더스탠딩 노벨상 해설', SRC_NOBEL, ''), ('요약본 전문', SUM_NOBEL, 'secondary')]
LINKS_DOPA = [('영상 — 언더스탠딩 도파민', SRC_DOPA, ''), ('요약본 전문', SUM_DOPA, 'secondary')]

LINKS_GLP1 = [('영상 — 언더스탠딩 비만약', SRC_GLP1, ''), ('요약본 전문', SUM_GLP1, 'secondary')]

LINKS_DISEASE = [('영상 — 언더스탠딩 3부작', SRC_3PART, ''), ('요약본 전문', SUM_3PART, 'secondary')]
LINKS_DRUG = [('영상 — 언더스탠딩 3부작', SRC_3PART, ''), ('요약본 전문', SUM_3PART, 'secondary')]

# 섹션은 몸에서 벌어지는 순서로 세운다. 염증이 먼저고, 그 위에 당뇨가 얹히고,
# 먹는 것이 원인 쪽이고, 검사가 확인 쪽이다. 체중·약과 뇌·수면은 축이 다르다.
SEC_INFLAM = ('sec-inflam', '01', '염증과 면역',
              '염증이 뭔지, 음식을 과하게 먹으면 왜 만성이 되는지, 그리고 암이 면역을 어떻게 구슬리는지')
SEC_DIABETES = ('sec-diabetes', '02', '당뇨',
                '지방산이 신호를 막아 생기는 병, 그리고 과당이 다른 당과 갈라지는 지점')
SEC_EAT = ('sec-eat', '03', '먹는 것',
           '무엇을 먹느냐보다 얼마나 먹게 되느냐, 그리고 단백질은 누가 더 먹어야 하는지')
SEC_STAGE = ('sec-stage', '04', '내 단계 알기',
             '의사를 만나기 전에 스스로 확인하는 방법, 그리고 유일한 전조증상')
SEC_WEIGHT = ('sec-weight', '05', '몸무게와 약',
              '살이 자산이 되는 경우, 그리고 영양제·스타틴·다이어트 약을 보는 눈')
SEC_GLP1 = ('sec-glp1', '06', '비만약과 중독',
            '덜 먹게 하는 약이 왜 갈망까지 줄이는지, 근거는 어디까지 왔고 무엇이 위험한지')
SEC_BRAIN = ('sec-brain', '07', '뇌 · 마음 · 수면',
             '뇌가 씻기는 시간대, 그리고 의욕과 만족을 정하는 물질')


# ── 그림 1. 급성 염증과 만성 염증 — 조직 단면 ───────────────────────────────
# 왼쪽은 한 번 다치고 끝나는 급성, 오른쪽은 같은 반응이 되풀이되는 만성.
# 두 그림에서 달라지는 것은 손상 구역(점선 타원)의 크기 하나다.
FIG_INFLAM = '''<svg viewBox="0 0 640 262" role="img" aria-label="급성 염증과 만성 염증의 조직 단면 비교">
  <rect x="18" y="34" width="286" height="184" rx="16" class="organ2 cut"/>
  <rect x="18" y="34" width="286" height="184" rx="16" class="hatch-w"/>
  <rect x="336" y="34" width="286" height="184" rx="16" class="organ2 cut"/>
  <rect x="336" y="34" width="286" height="184" rx="16" class="hatch-w"/>
  <text class="t-lab" x="18" y="24">급성 염증 — 한 번 다치고 끝난다</text>
  <text class="t-lab" x="336" y="24">만성 염증 — 같은 반응이 5~10년</text>

  <path class="vessel" d="M18 152 C 80 132, 130 168, 186 146 C 232 128, 268 138, 304 128"/>
  <ellipse cx="150" cy="150" rx="54" ry="40" fill="var(--fig-bad,#c2504a)" fill-opacity=".14"/>
  <ellipse cx="150" cy="150" rx="54" ry="40" fill="none" stroke="var(--fig-bad,#c2504a)"
           stroke-width="1.2" stroke-dasharray="4 4"/>
  <circle class="bad" cx="150" cy="146" r="6"/>
  <circle class="cell" cx="124" cy="134" r="8"/>
  <circle class="cell" cx="176" cy="140" r="8"/>
  <circle class="cell" cx="140" cy="172" r="8"/>
  <circle class="cell" cx="172" cy="170" r="7"/>
  <text class="t-sm" x="150" y="206" text-anchor="middle">손상이 침입 지점 둘레에서 멈춘다</text>
  <path class="lead-line" d="M150 146 L 214 96"/>
  <text class="t-sm" x="218" y="94">균 · 침입 물질</text>
  <path class="lead-line" d="M124 134 L 64 74"/>
  <text class="t-sm" x="26" y="68">대식 세포 · 호중구</text>

  <path class="vessel" d="M336 152 C 398 132, 448 168, 504 146 C 550 128, 586 138, 622 128"/>
  <ellipse cx="478" cy="150" rx="126" ry="52" fill="var(--fig-bad,#c2504a)" fill-opacity=".16"/>
  <ellipse cx="478" cy="150" rx="126" ry="52" fill="none" stroke="var(--fig-bad,#c2504a)"
           stroke-width="1.2" stroke-dasharray="4 4"/>
  <circle class="fat" cx="404" cy="150" r="5"/>
  <circle class="fat" cx="438" cy="140" r="5"/>
  <circle class="fat" cx="470" cy="158" r="5"/>
  <circle class="fat" cx="508" cy="144" r="5"/>
  <circle class="fat" cx="546" cy="154" r="5"/>
  <circle class="cell" cx="418" cy="126" r="8"/>
  <circle class="cell" cx="462" cy="180" r="8"/>
  <circle class="cell" cx="500" cy="122" r="8"/>
  <circle class="cell" cx="530" cy="178" r="8"/>
  <circle class="cell" cx="556" cy="128" r="7"/>
  <text class="t-sm" x="478" y="216" text-anchor="middle">손상이 쌓여 장기가 조용히 망가진다</text>
  <path class="lead-line" d="M470 158 L 420 92"/>
  <text class="t-sm" x="376" y="86">유리 지방산 — 내 몸에서 나온다</text>
</svg>'''

# ── 그림 2. 동맥 벽 세로단면 — 지방산이 쌓이는 자리 ─────────────────────────
# 몸통과 한 그림에 넣었더니 라벨 자리가 없어 둘로 쪼갰다. 벽은 세 층으로 그린다.
FIG_ARTERY = '''<svg viewBox="0 0 640 250" role="img" aria-label="동맥 벽 세로단면과 쌓인 플라크">
  <text class="t-lab" x="18" y="22">동맥 벽 세로단면</text>

  <!-- 위쪽 벽 — 바깥 막과 근육층 -->
  <rect x="26" y="44" width="392" height="26" class="organ2 cut"/>
  <rect x="26" y="44" width="392" height="26" class="hatch"/>
  <rect x="26" y="70" width="392" height="16" class="organ cut"/>
  <rect x="26" y="70" width="392" height="16" class="hatch"/>
  <!-- 혈액이 흐르는 안쪽 -->
  <rect x="26" y="86" width="392" height="78" class="body"/>
  <!-- 아래쪽 벽 -->
  <rect x="26" y="164" width="392" height="16" class="organ cut"/>
  <rect x="26" y="164" width="392" height="16" class="hatch"/>
  <rect x="26" y="180" width="392" height="26" class="organ2 cut"/>
  <rect x="26" y="180" width="392" height="26" class="hatch"/>

  <!-- 플라크 — 안쪽 막 밑에서 부풀어 혈액 길을 좁힌다 -->
  <path fill="var(--fig-bad,#c2504a)" fill-opacity=".26" stroke="var(--fig-bad,#c2504a)"
        stroke-width="1.4" d="M150 86 C 184 86, 196 130, 240 134 C 286 138, 302 98, 332 86 Z"/>
  <circle class="fat" cx="196" cy="102" r="5"/>
  <circle class="fat" cx="228" cy="112" r="5"/>
  <circle class="fat" cx="262" cy="106" r="5"/>
  <circle class="fat" cx="290" cy="98" r="5"/>
  <circle class="cell" cx="216" cy="96" r="7"/>
  <circle class="cell" cx="272" cy="120" r="7"/>

  <!-- 혈류 -->
  <path class="flow" d="M40 150 L 108 150"/>
  <path class="flow" d="M40 126 L 96 126"/>
  <text class="t-sm" x="40" y="172">혈류</text>

  <!-- 라벨 -->
  <path class="lead-line" d="M418 57 L 430 57"/>
  <text class="t-sm" x="434" y="61">바깥 막</text>
  <path class="lead-line" d="M418 78 L 430 78"/>
  <text class="t-sm" x="434" y="82">가운데 근육층</text>
  <path class="lead-line" d="M336 96 L 430 108"/>
  <text class="t-bad" x="434" y="112">쌓인 콜레스테롤</text>
  <text class="t-sm" x="434" y="130">노란 알갱이가 지방,</text>
  <text class="t-sm" x="434" y="146">파란 것이 대식 세포다</text>
  <path class="lead-line" d="M418 190 L 430 190"/>
  <text class="t-sm" x="434" y="194">반대쪽 벽도 같은 구조</text>
  <text class="t-sm" x="26" y="228">혈압이 벽을 눌러 터뜨리고, 복구가 덜 된 자리가 딱딱해진다. 그 틈으로 지방이 파고든다.</text>
</svg>'''

# ── 그림 3. 복부 관상단면 — 남은 에너지가 도는 길 ───────────────────────────
# 번호는 해부 위에 찍고 설명은 오른쪽 열에 세운다. 화살표를 몸통 안에서 꼬면
# 어느 장기에서 어디로 가는지 읽히지 않는다.
FIG_TORSO = '''<svg viewBox="0 0 640 400" role="img" aria-label="복부 관상단면에서 간·근육·내장지방을 도는 지방 경로">
  <text class="t-lab" x="18" y="22">복부 관상단면</text>

  <path class="body cut" d="M155 56 C 147 100, 155 140, 159 170 C 163 205, 167 240, 177 272
                            C 187 306, 205 330, 230 342 C 255 330, 273 306, 283 272
                            C 293 240, 297 205, 301 170 C 305 140, 313 100, 305 56 Z"/>
  <path class="hatch-w" d="M155 56 C 147 100, 155 140, 159 170 C 163 205, 167 240, 177 272
                           C 187 306, 205 330, 230 342 C 255 330, 273 306, 283 272
                           C 293 240, 297 205, 301 170 C 305 140, 313 100, 305 56 Z"/>
  <path fill="none" stroke="var(--fig-line,#9a8078)" stroke-width="2" d="M153 62 C 187 26, 273 26, 307 62"/>
  <text class="t-sm" x="230" y="44" text-anchor="middle">횡격막</text>

  <!-- 간 — 오른쪽 엽이 크고 아래 모서리가 얇다 -->
  <path class="organ cut" d="M159 80 C 185 68, 231 68, 263 80 C 267 98, 255 118, 231 124
                             C 201 130, 167 118, 159 102 Z"/>
  <path class="hatch" d="M159 80 C 185 68, 231 68, 263 80 C 267 98, 255 118, 231 124
                         C 201 130, 167 118, 159 102 Z"/>
  <path fill="none" stroke="var(--fig-line,#9a8078)" stroke-width="1.1" d="M231 72 L 227 122"/>
  <text class="t-lab" x="188" y="100">간</text>
  <circle class="fat" cx="176" cy="96" r="4"/>
  <circle class="fat" cx="192" cy="110" r="4"/>
  <circle class="fat" cx="206" cy="96" r="4"/>

  <!-- 위 -->
  <path class="organ2 cut" d="M265 86 C 287 82, 299 98, 295 118 C 291 140, 269 148, 257 136
                              C 251 126, 255 112, 265 102 Z"/>
  <text class="t-sm" x="276" y="118" text-anchor="middle">위</text>

  <!-- 창자 -->
  <path class="organ2 cut" d="M173 198 C 205 186, 261 186, 287 200 C 295 228, 285 260, 263 274
                              C 235 286, 201 280, 183 264 C 169 248, 167 218, 173 198 Z"/>
  <path class="lead-line" d="M183 216 C 205 202, 251 202, 275 216"/>
  <path class="lead-line" d="M181 236 C 207 222, 255 222, 279 236"/>
  <path class="lead-line" d="M187 256 C 211 244, 253 244, 275 256"/>
  <text class="t-sm" x="230" y="196" text-anchor="middle">창자</text>

  <!-- 내장 지방 — 창자 사이를 메운다 -->
  <circle class="fat" cx="166" cy="202" r="10"/>
  <circle class="fat" cx="294" cy="206" r="10"/>
  <circle class="fat" cx="174" cy="268" r="11"/>
  <circle class="fat" cx="288" cy="264" r="10"/>
  <circle class="fat" cx="230" cy="294" r="12"/>
  <circle class="fat" cx="230" cy="178" r="9"/>
  <text class="t-sm" x="230" y="320" text-anchor="middle">내장 지방</text>

  <!-- 복벽 근육 -->
  <path fill="none" stroke="var(--fig-organ,#e3d3cc)" stroke-width="8" stroke-linecap="round"
        d="M161 178 C 157 212, 161 248, 173 276"/>
  <path fill="none" stroke="var(--fig-line,#9a8078)" stroke-width="1"
        d="M161 178 C 157 212, 161 248, 173 276"/>
  <text class="t-sm" x="104" y="230">복벽 근육</text>

  <!-- 대동맥과 대정맥 -->
  <path class="vessel" d="M239 64 C 243 140, 241 240, 243 336"/>
  <path class="vein" d="M221 64 C 217 140, 219 240, 217 336"/>
  <text class="t-sm" x="250" y="358">대동맥</text>
  <text class="t-sm" x="180" y="358">대정맥</text>

  <!-- 번호는 해부 위에 -->
  <circle cx="276" cy="70" r="11" fill="var(--fig-organ2,#f0e2d8)" stroke="var(--fig-line,#9a8078)"/>
  <text class="t-lab" x="276" y="74" text-anchor="middle">1</text>
  <circle cx="140" cy="256" r="11" fill="var(--fig-organ2,#f0e2d8)" stroke="var(--fig-line,#9a8078)"/>
  <text class="t-lab" x="140" y="260" text-anchor="middle">2</text>
  <circle cx="306" cy="294" r="11" fill="var(--fig-organ2,#f0e2d8)" stroke="var(--fig-line,#9a8078)"/>
  <text class="t-lab" x="306" y="298" text-anchor="middle">3</text>
  <circle cx="150" cy="112" r="11" fill="var(--fig-organ2,#f0e2d8)" stroke="var(--fig-line,#9a8078)"/>
  <text class="t-lab" x="150" y="116" text-anchor="middle">4</text>

  <!-- 설명은 오른쪽 열에 -->
  <text class="t-lab" x="370" y="86">1 · 간이 지방을 만든다</text>
  <text class="t-sm" x="370" y="104">근육과 심장이 태울 연료다</text>
  <text class="t-lab" x="370" y="146">2 · 근육이 더 안 받는다</text>
  <text class="t-sm" x="370" y="164">그날 쓸 만큼은 이미 썼다</text>
  <text class="t-lab" x="370" y="206">3 · 내장 지방도 자리가 없다</text>
  <text class="t-sm" x="370" y="224">지방 세포가 이미 빵빵하다</text>
  <text class="t-lab" x="370" y="266">4 · 간세포가 떠안는다</text>
  <text class="t-sm" x="370" y="284">이 상태가 지방간이다</text>
  <text class="t-bad" x="370" y="326">삐져나온 지방산은 혈액을 돌다</text>
  <text class="t-bad" x="370" y="344">동맥 벽에 쌓인다</text>
</svg>'''

# ── 그림 6. 소화관과 세 갈래 ────────────────────────────────────────────────
# 왼쪽 해부도는 손으로 그리지 않았다. 위키미디어 공용의 퍼블릭도메인 도해를 가져와
# 라벨을 떼고 색만 우리 붓으로 갈아끼웠다(scratchpad/health_assets.py 참고).
FIG_FUEL = '''<svg viewBox="0 0 640 344" role="img" aria-label="위와 창자를 지난 3대 영양소가 갈라지는 경로">
  <text class="t-lab" x="18" y="22">소화관 — 위에서 대장까지</text>
  <text class="t-lab" x="336" y="22">그다음 세 갈래</text>

  <g transform="translate(24,32) scale(0.42)">%s</g>

  <path class="flow" d="M286 92 L 328 88"/>
  <path class="flow" d="M286 160 L 328 158"/>
  <path class="flow" d="M286 216 L 328 226"/>

  <text class="t-lab" x="336" y="76">단백질</text>
  <text class="t-sm" x="336" y="94">몸을 이루고 기능하는 성분으로 간다.</text>
  <text class="t-sm" x="336" y="108">에너지로 바꾸는 걸 몸이 싫어한다.</text>

  <text class="t-lab" x="336" y="146">탄수화물과 지방, 그날 쓸 만큼</text>
  <text class="t-sm" x="336" y="164">근육이 태운다. 갑자기 뛸 때는 포도당,</text>
  <text class="t-sm" x="336" y="178">평상시에는 지방이 연료다.</text>

  <text class="t-bad" x="336" y="216">남은 만큼은 반드시 지방으로</text>
  <text class="t-sm" x="336" y="234">탄수화물이 남아도 지방,</text>
  <text class="t-sm" x="336" y="248">지방이 남아도 지방이다.</text>
  <circle class="fat" cx="348" cy="278" r="10"/>
  <circle class="fat" cx="372" cy="282" r="12"/>
  <circle class="fat" cx="398" cy="276" r="9"/>
  <text class="t-sm" x="416" y="284">지방 세포로 쌓인다</text>

  <text class="t-sm" x="18" y="330">왼쪽 도해는 위키미디어 공용의 퍼블릭도메인 그림을 다시 칠한 것이다.</text>
</svg>''' % ha.GUT

# ── 그림 4. 무엇을 어디서 재나 — 전신 계측 지도 ─────────────────────────────
FIG_MEASURE = '''<svg viewBox="0 0 640 320" role="img" aria-label="혈압·허리둘레·혈액검사를 재는 위치를 표시한 전신 그림">
  <text class="t-lab" x="18" y="22">집에서 둘 · 피검사에서 셋</text>

  <!-- 전신 실루엣 -->
  <circle class="body" cx="212" cy="60" r="26"/>
  <path class="body" d="M212 88 C 178 90, 162 108, 160 136 C 158 160, 164 176, 164 196
                        C 164 224, 170 246, 172 264 L 196 264 L 202 200 L 222 200 L 228 264
                        L 252 264 C 254 246, 260 224, 260 196 C 260 176, 266 160, 264 136
                        C 262 108, 246 90, 212 88 Z"/>
  <!-- 팔 -->
  <path class="body" d="M164 112 C 146 122, 138 152, 136 186 C 135 202, 140 210, 148 210
                        C 154 210, 156 200, 157 186 C 159 156, 164 134, 172 124 Z"/>
  <path class="body" d="M260 112 C 278 122, 286 152, 288 186 C 289 202, 284 210, 276 210
                        C 270 210, 268 200, 267 186 C 265 156, 260 134, 252 124 Z"/>
  <!-- 다리 -->
  <path class="body" d="M172 264 C 170 292, 174 306, 176 314 L 198 314 C 200 300, 202 284, 204 264 Z"/>
  <path class="body" d="M252 264 C 254 292, 250 306, 248 314 L 226 314 C 224 300, 222 284, 220 264 Z"/>

  <!-- ① 혈압 커프 -->
  <rect x="132" y="130" width="34" height="26" rx="6" class="organ"/>
  <path class="lead-line" d="M132 142 L 60 118"/>
  <text class="t-lab" x="18" y="112">① 혈압</text>
  <text class="t-sm" x="18" y="130">130 / 85만 돼도 혈관이</text>
  <text class="t-sm" x="18" y="144">손상되고 있다고 본다</text>

  <!-- ② 허리둘레 -->
  <ellipse cx="212" cy="196" rx="52" ry="13" fill="none" stroke="var(--fig-bad,#c2504a)"
           stroke-width="1.6" stroke-dasharray="5 4"/>
  <path class="lead-line" d="M264 196 L 344 196"/>
  <text class="t-lab" x="350" y="192">② 허리(배꼽) 둘레</text>
  <text class="t-sm" x="350" y="210">남 90cm · 여 85cm를 넘으면</text>
  <text class="t-sm" x="350" y="224">내장 지방이 많은 사람</text>

  <!-- ③ 채혈 -->
  <circle class="bad" cx="288" cy="176" r="5"/>
  <path class="lead-line" d="M292 172 L 352 96"/>
  <text class="t-lab" x="350" y="62">③ 피검사 — 셋만 본다</text>
  <text class="t-sm" x="350" y="82">HS-CRP  0.2 넘으면 만성 염증 신호</text>
  <text class="t-sm" x="350" y="98">당화혈색소  6.0% 넘으면 대사 이상</text>
  <text class="t-sm" x="350" y="114">간 효소 AST·ALT  40 이하가 정상</text>
  <text class="t-sm" x="350" y="132">— HS-CRP는 검진에 잘 없어 따로 요청</text>

  <text class="t-sm" x="18" y="292">넷 다 증상이 아니라 숫자다.</text>
  <text class="t-sm" x="18" y="308">아프기 전에 움직이는 게 목적이다.</text>
</svg>'''

# ── 그림 5. 뇌는 깊은 잠에서만 씻긴다 — 시상단면과 수면 곡선 ────────────────
FIG_SLEEP = '''<svg viewBox="0 0 640 300" role="img" aria-label="뇌 시상단면의 글림프 흐름과 수면 단계 곡선">
  <text class="t-lab" x="18" y="22">뇌 시상단면 — 청소 통로</text>
  <text class="t-lab" x="352" y="22">하룻밤 수면 단계</text>

  <path class="organ cut" d="M40 148 C 40 86, 96 44, 168 44 C 236 44, 288 78, 292 130
                         C 296 168, 276 190, 248 196 C 210 204, 150 206, 110 198
                         C 68 190, 40 178, 40 148 Z"/>
  <path class="hatch-w" d="M40 148 C 40 86, 96 44, 168 44 C 236 44, 288 78, 292 130
                         C 296 168, 276 190, 248 196 C 210 204, 150 206, 110 198
                         C 68 190, 40 178, 40 148 Z"/>
  <!-- 뇌량 — 시상면에서 좌우 반구를 잇는 활 모양 띠. 이게 있어야 시상면으로 읽힌다 -->
  <path fill="none" stroke="var(--fig-line,#9a8078)" stroke-width="2.2"
        d="M96 150 C 104 116, 140 100, 178 104 C 208 107, 226 120, 232 136"/>
  <path class="lead-line" d="M74 106 C 96 92, 120 92, 138 104"/>
  <path class="lead-line" d="M150 82 C 174 72, 202 78, 216 94"/>
  <path class="lead-line" d="M226 116 C 248 112, 264 122, 268 138"/>
  <path class="organ2" d="M126 138 C 152 126, 190 128, 210 142 C 202 158, 168 164, 142 158 Z"/>
  <text class="t-sm" x="168" y="152" text-anchor="middle">뇌실</text>
  <path class="organ2 cut" d="M236 200 C 268 194, 288 208, 284 228 C 278 246, 248 250, 230 238 Z"/>
  <path class="hatch" d="M236 200 C 268 194, 288 208, 284 228 C 278 246, 248 250, 230 238 Z"/>
  <text class="t-sm" x="292" y="222">소뇌</text>
  <path class="organ2 cut" d="M186 198 C 202 198, 208 216, 204 244 C 200 264, 188 268, 180 262
                          C 176 240, 178 214, 186 198 Z"/>
  <path class="hatch" d="M186 198 C 202 198, 208 216, 204 244 C 200 264, 188 268, 180 262
                          C 176 240, 178 214, 186 198 Z"/>
  <text class="t-sm" x="140" y="252">뇌간</text>
  <path class="flow" d="M92 168 C 118 150, 150 142, 178 140"/>
  <path class="flow" d="M214 142 C 240 140, 258 152, 268 168"/>
  <path class="flow" d="M108 118 C 140 106, 178 104, 208 112"/>
  <text class="t-sm" x="42" y="216">뇌척수액이 들어와</text>
  <text class="t-sm" x="42" y="230">부산물을 씻어 나간다</text>

  <path class="lead-line" d="M392 52 L 392 250 L 626 250"/>
  <text class="t-sm" x="376" y="66" text-anchor="end">각성</text>
  <text class="t-sm" x="376" y="96" text-anchor="end">1단계</text>
  <text class="t-sm" x="376" y="126" text-anchor="end">2단계</text>
  <text class="t-sm" x="376" y="160" text-anchor="end">3단계</text>
  <text class="t-sm" x="376" y="192" text-anchor="end">4단계</text>
  <rect x="392" y="146" width="234" height="56" fill="var(--fig-good,#2f8f6b)" fill-opacity=".14"/>
  <text class="t-sm" x="618" y="166" text-anchor="end" fill="var(--fig-good,#2f8f6b)">여기서만 씻긴다</text>
  <path fill="none" stroke="var(--fig-vein,#4a6ec2)" stroke-width="2.4" stroke-linejoin="round"
        d="M392 62 L 410 92 L 428 122 L 446 156 L 468 188 L 496 188 L 512 156 L 526 122
           L 540 92 L 552 78 L 566 108 L 580 150 L 598 186 L 616 186"/>
  <circle class="good" cx="482" cy="188" r="4"/>
  <circle class="good" cx="606" cy="186" r="4"/>
  <text class="t-sm" x="470" y="230">깊은 잠 1회</text>
  <text class="t-sm" x="616" y="230" text-anchor="end">2회</text>
  <text class="t-sm" x="616" y="252" text-anchor="end">하룻밤 4~5회 반복</text>
</svg>'''


# ── 그림 4. 인슐린 초인종 — 세포막 단면 ─────────────────────────────────────
# 왼쪽이 정상, 오른쪽이 지방산이 많을 때. 달라지는 건 수용체가 받는 신호의 세기다.
FIG_INSULIN = '''<svg viewBox="0 0 640 300" role="img" aria-label="세포막 단면에서 인슐린 신호가 지방산에 막히는 비교">
  <text class="t-lab" x="18" y="22">정상 — 초인종이 울린다</text>
  <text class="t-lab" x="336" y="22">지방산이 많을 때 — 뻑뻑해진다</text>

  <!-- 왼쪽 세포 -->
  <rect x="18" y="118" width="286" height="34" class="organ2 cut"/>
  <rect x="18" y="118" width="286" height="34" class="hatch"/>
  <rect x="18" y="152" width="286" height="96" class="body"/>
  <text class="t-sm" x="26" y="172">세포 안</text>
  <text class="t-sm" x="26" y="110">혈액 쪽</text>
  <!-- 수용체와 수송체 -->
  <rect x="122" y="110" width="26" height="50" rx="7" class="organ"/>
  <rect x="212" y="110" width="26" height="50" rx="7" class="organ"/>
  <text class="t-sm" x="96" y="98">수용체</text>
  <text class="t-sm" x="200" y="98">포도당 문</text>
  <circle class="good" cx="135" cy="96" r="7"/>
  <text class="t-sm" x="146" y="80">인슐린</text>
  <!-- 신호와 포도당 -->
  <path class="flow" d="M148 150 C 176 158, 196 156, 210 150"/>
  <text class="t-sm" x="152" y="176">열어라</text>
  <circle class="cell" cx="225" cy="88" r="7"/>
  <circle class="cell" cx="252" cy="96" r="7"/>
  <path class="flow" d="M225 106 L 225 176"/>
  <circle class="cell" cx="225" cy="196" r="7"/>
  <text class="t-sm" x="150" y="232">포도당이 들어가 쓰인다</text>

  <!-- 오른쪽 세포 -->
  <rect x="336" y="118" width="286" height="34" class="organ2 cut"/>
  <rect x="336" y="118" width="286" height="34" class="hatch"/>
  <rect x="336" y="152" width="286" height="96" class="body"/>
  <rect x="440" y="110" width="26" height="50" rx="7" class="organ"/>
  <rect x="530" y="110" width="26" height="50" rx="7" class="organ"/>
  <circle class="good" cx="424" cy="92" r="7"/>
  <circle class="good" cx="452" cy="86" r="7"/>
  <circle class="good" cx="478" cy="94" r="7"/>
  <text class="t-sm" x="366" y="76">인슐린이 더 나온다</text>
  <!-- 지방산이 막 둘레에 낀다 -->
  <circle class="fat" cx="400" cy="134" r="6"/>
  <circle class="fat" cx="424" cy="140" r="6"/>
  <circle class="fat" cx="470" cy="132" r="6"/>
  <circle class="fat" cx="496" cy="140" r="6"/>
  <circle class="fat" cx="516" cy="130" r="6"/>
  <text class="t-bad" x="366" y="170">지방산</text>
  <!-- 신호가 약하다 -->
  <path class="lead-line" d="M466 150 C 494 158, 514 156, 528 150"/>
  <text class="t-sm" x="470" y="176">신호가 안 간다</text>
  <circle class="cell" cx="546" cy="88" r="7"/>
  <circle class="cell" cx="572" cy="96" r="7"/>
  <circle class="cell" cx="596" cy="86" r="7"/>
  <text class="t-bad" x="470" y="232">포도당이 밖에 남는다</text>
  <text class="t-sm" x="18" y="268">초인종이 완전히 고장 난 게 아니라 뻑뻑해진 상태다. 인슐린을 더 세게 눌러야 겨우 울린다.</text>
</svg>'''

# ── 그림 5. 과당의 외길 ─────────────────────────────────────────────────────
# 포도당은 온몸이 나눠 쓰고 과당은 간 하나만 받는다. 이 차이가 결과를 가른다.
FIG_FRUCTOSE = '''<svg viewBox="0 0 640 330" role="img" aria-label="포도당은 온몸의 세포로 가고 과당은 간으로만 가는 경로 비교">
  <text class="t-lab" x="18" y="22">포도당 — 온몸이 나눠 쓴다</text>

  <circle class="cell" cx="56" cy="86" r="16"/>
  <text class="t-sm" x="30" y="122">포도당</text>
  <!-- 뇌 -->
  <path class="organ" d="M198 60 C 198 44, 214 34, 234 34 C 254 34, 268 44, 270 58
                         C 272 72, 262 80, 248 82 C 232 85, 212 84, 204 78 Z"/>
  <text class="t-sm" x="234" y="102" text-anchor="middle">뇌</text>
  <!-- 심장 -->
  <path class="organ" d="M340 46 C 348 34, 366 34, 370 48 C 374 34, 392 34, 398 48
                         C 404 64, 380 84, 369 92 C 358 84, 334 62, 340 46 Z"/>
  <text class="t-sm" x="369" y="108" text-anchor="middle">심장</text>
  <!-- 근육 -->
  <path class="organ" d="M486 40 C 506 34, 524 44, 528 62 C 532 80, 520 92, 502 92
                         C 486 92, 476 78, 478 60 Z"/>
  <text class="t-sm" x="504" y="108" text-anchor="middle">근육</text>
  <path class="flow" d="M76 82 C 128 70, 164 62, 196 58"/>
  <path class="flow" d="M76 88 C 160 88, 260 76, 336 62"/>
  <path class="flow" d="M76 94 C 200 108, 380 94, 476 66"/>

  <text class="t-lab" x="18" y="186">과당 — 간 하나만 받는다</text>
  <circle class="fat" cx="56" cy="238" r="16"/>
  <text class="t-sm" x="30" y="274">과당</text>
  <!-- 간 -->
  <path class="organ cut" d="M196 206 C 226 194, 276 198, 306 212 C 310 232, 296 252, 268 258
                             C 234 264, 202 250, 196 230 Z"/>
  <path class="hatch" d="M196 206 C 226 194, 276 198, 306 212 C 310 232, 296 252, 268 258
                         C 234 264, 202 250, 196 230 Z"/>
  <text class="t-lab" x="230" y="234">간</text>
  <path class="flow" d="M76 238 L 192 230"/>
  <!-- 다른 장기는 안 받는다 -->
  <path class="lead-line" d="M300 208 C 340 190, 380 176, 420 150"/>
  <text class="t-bad" x="330" y="200">다른 장기는 안 받는다</text>
  <!-- 간에서 지방으로 -->
  <circle class="fat" cx="240" cy="222" r="5"/>
  <circle class="fat" cx="262" cy="234" r="5"/>
  <circle class="fat" cx="284" cy="222" r="5"/>
  <path class="flow" d="M312 232 L 452 232"/>
  <circle class="fat" cx="486" cy="222" r="12"/>
  <circle class="fat" cx="512" cy="238" r="14"/>
  <circle class="fat" cx="540" cy="220" r="11"/>
  <text class="t-bad" x="470" y="272">지방으로 간다</text>
  <text class="t-sm" x="18" y="304">운동을 많이 하면 간이 젖산으로 일부 쓴다. 그렇지 않으면 적당량을 먹어도 일부는 지방이 된다.</text>
</svg>'''

# ── 그림 7. 혈관이 밟는 네 단계 ─────────────────────────────────────────────
# 횡단면 넷을 나란히 둔다. 검사로 잡아야 하는 건 2단계이고, 3단계는 이미 사건이다.
FIG_STAGE = '''<svg viewBox="0 0 640 300" role="img" aria-label="깨끗한 혈관에서 사건까지 혈관 횡단면 네 단계">
  <text class="t-lab" x="18" y="22">혈관 횡단면 — 0단계에서 3단계까지</text>

  <circle cx="92" cy="120" r="54" class="organ2 cut"/>
  <circle cx="92" cy="120" r="54" class="hatch"/>
  <circle cx="92" cy="120" r="36" class="body"/>
  <text class="t-lab" x="92" y="206" text-anchor="middle">0단계</text>
  <text class="t-sm" x="92" y="224" text-anchor="middle">깨끗하다</text>

  <circle cx="240" cy="120" r="54" class="organ2 cut"/>
  <circle cx="240" cy="120" r="54" class="hatch"/>
  <circle cx="240" cy="120" r="36" class="body"/>
  <circle class="bad" cx="240" cy="86" r="4"/>
  <circle class="bad" cx="266" cy="104" r="4"/>
  <circle class="bad" cx="216" cy="140" r="4"/>
  <text class="t-lab" x="240" y="206" text-anchor="middle">1단계</text>
  <text class="t-sm" x="240" y="224" text-anchor="middle">위험 요인이 벽을 긁는다</text>
  <text class="t-sm" x="240" y="240" text-anchor="middle">고혈압 · 당뇨 · 고지혈증</text>
  <text class="t-sm" x="240" y="256" text-anchor="middle">술 · 담배 · 심방세동 · 비만</text>

  <circle cx="392" cy="120" r="54" class="organ2 cut"/>
  <circle cx="392" cy="120" r="54" class="hatch"/>
  <circle cx="392" cy="120" r="36" class="body"/>
  <path fill="var(--fig-bad,#c2504a)" fill-opacity=".3" stroke="var(--fig-bad,#c2504a)" stroke-width="1.2"
        d="M362 96 C 380 84, 410 84, 424 100 C 412 116, 384 122, 366 114 Z"/>
  <circle class="fat" cx="384" cy="100" r="4"/>
  <circle class="fat" cx="404" cy="98" r="4"/>
  <text class="t-lab" x="392" y="206" text-anchor="middle">2단계</text>
  <text class="t-sm" x="392" y="224" text-anchor="middle">동맥경화 — 장전됐다</text>
  <text class="t-sm" x="392" y="240" text-anchor="middle">증상으로는 모른다</text>

  <circle cx="544" cy="120" r="54" class="organ2 cut"/>
  <circle cx="544" cy="120" r="54" class="hatch"/>
  <circle cx="544" cy="120" r="36" class="body"/>
  <circle class="bad" cx="544" cy="120" r="30"/>
  <text class="t-lab" x="544" y="206" text-anchor="middle">3단계</text>
  <text class="t-sm" x="544" y="224" text-anchor="middle">혈전이 막았다 — 사건</text>

  <path class="flow" d="M152 120 L 180 120"/>
  <path class="flow" d="M300 120 L 332 120"/>
  <path class="flow" d="M452 120 L 484 120"/>
  <text class="t-sm" x="18" y="286">경동맥 초음파로 잡아야 하는 건 2단계다. 1단계에서 2단계로 넘어가지만 않으면 3단계는 오지 않는다.</text>
</svg>'''


# ── 그림 10. 동맥류는 동맥경화와 다르다 ────────────────────────────────────
# 왼쪽은 두 병의 단면 대비, 오른쪽은 터진 뒤 피가 퍼진 자리.
FIG_ANEURYSM = '''<svg viewBox="0 0 640 300" role="img" aria-label="동맥경화와 동맥류의 단면 대비, 그리고 파열 뒤 지주막하 공간">
  <text class="t-lab" x="18" y="22">같은 혈관, 다른 병</text>
  <text class="t-lab" x="352" y="22">터진 뒤 — 뇌 아랫면</text>

  <!-- 위: 동맥경화 -->
  <rect x="26" y="52" width="270" height="14" class="organ2 cut"/>
  <rect x="26" y="52" width="270" height="14" class="hatch"/>
  <rect x="26" y="66" width="270" height="42" class="body"/>
  <rect x="26" y="108" width="270" height="14" class="organ2 cut"/>
  <rect x="26" y="108" width="270" height="14" class="hatch"/>
  <path fill="var(--fig-bad,#c2504a)" fill-opacity=".28" stroke="var(--fig-bad,#c2504a)" stroke-width="1.2"
        d="M120 66 C 148 66, 160 96, 196 98 C 232 100, 244 74, 262 66 Z"/>
  <text class="t-sm" x="26" y="140">동맥경화 — 벽 안쪽에 쌓여 길이 좁아진다</text>

  <!-- 아래: 동맥류 -->
  <rect x="26" y="188" width="270" height="14" class="organ2 cut"/>
  <rect x="26" y="188" width="270" height="14" class="hatch"/>
  <rect x="26" y="202" width="270" height="42" class="body"/>
  <rect x="26" y="244" width="270" height="14" class="organ2 cut"/>
  <rect x="26" y="244" width="270" height="14" class="hatch"/>
  <path class="organ2 cut" d="M150 188 C 150 156, 176 142, 198 142 C 222 142, 244 158, 242 188 Z"/>
  <path class="hatch" d="M150 188 C 150 156, 176 142, 198 142 C 222 142, 244 158, 242 188 Z"/>
  <text class="t-sm" x="26" y="278">동맥류 — 벽이 바깥으로 부푼다. 피는 그대로 흘러 증상이 없다</text>

  <!-- 오른쪽: 뇌 아랫면과 퍼진 피 -->
  <ellipse cx="486" cy="150" rx="118" ry="84" fill="var(--fig-bad,#c2504a)" fill-opacity=".16"/>
  <path class="organ cut" d="M420 92 C 452 74, 520 74, 552 92 C 574 112, 574 176, 548 202
                             C 516 226, 456 226, 424 202 C 398 176, 398 112, 420 92 Z"/>
  <path class="hatch-w" d="M420 92 C 452 74, 520 74, 552 92 C 574 112, 574 176, 548 202
                           C 516 226, 456 226, 424 202 C 398 176, 398 112, 420 92 Z"/>
  <path class="vessel" d="M486 216 C 486 184, 464 168, 440 158"/>
  <path class="vessel" d="M486 216 C 486 184, 508 168, 532 158"/>
  <path class="vessel" d="M486 190 C 470 178, 452 176, 436 180"/>
  <circle class="bad" cx="452" cy="164" r="9"/>
  <path class="lead-line" d="M452 164 L 400 118"/>
  <text class="t-bad" x="352" y="112">여기가 터졌다</text>
  <text class="t-sm" x="352" y="256">붉은 자리로 퍼진 피는 씻어낼 방법이 없다.</text>
  <text class="t-sm" x="352" y="272">혈관 밖 피는 조직을 자극하는 독이 된다.</text>
</svg>'''


# ── 그림 11. 종양이 구슬린 세포 ─────────────────────────────────────────────
# 왼쪽은 막힌 상태, 오른쪽은 관문을 덮은 뒤. 세포는 조직 그림이 아니라 세포 단위라
# 해칭 대신 면색으로만 구분한다.
FIG_TREG = '''<svg viewBox="0 0 640 320" role="img" aria-label="종양이 구슬린 조절 T세포가 킬러 T세포를 막는 상태와 항체로 관문을 덮은 상태">
  <text class="t-lab" x="18" y="22">막힌 상태 — 종양 미세환경</text>
  <text class="t-lab" x="336" y="22">관문을 덮은 뒤</text>

  <!-- 왼쪽: 종양과 구슬려진 조절 T세포 -->
  <path class="organ2 cut" d="M96 96 C 130 74, 186 76, 214 100 C 236 128, 228 176, 196 196
                              C 160 218, 108 208, 88 178 C 70 150, 74 116, 96 96 Z"/>
  <path class="hatch" d="M96 96 C 130 74, 186 76, 214 100 C 236 128, 228 176, 196 196
                         C 160 218, 108 208, 88 178 C 70 150, 74 116, 96 96 Z"/>
  <text class="t-lab" x="150" y="146" text-anchor="middle">종양</text>
  <!-- 구슬려진 조절 T세포 셋이 둘레를 두른다 -->
  <circle class="good" cx="92" cy="72" r="14"/>
  <circle class="good" cx="220" cy="80" r="14"/>
  <circle class="good" cx="228" cy="188" r="14"/>
  <text class="t-sm" x="18" y="60">구슬려진 조절 T세포</text>
  <!-- 내밀고 있는 표지 -->
  <path class="vessel" d="M92 58 L 92 44" stroke="var(--fig-bad,#c2504a)"/>
  <path class="vessel" d="M232 70 L 244 60" stroke="var(--fig-bad,#c2504a)"/>
  <path class="vessel" d="M240 196 L 254 202" stroke="var(--fig-bad,#c2504a)"/>
  <text class="t-bad" x="252" y="52">CTLA-4 · PD-1</text>
  <!-- 킬러 T세포가 다가오다 막힌다 -->
  <circle class="cell" cx="150" cy="264" r="16"/>
  <text class="t-sm" x="150" y="298" text-anchor="middle">킬러 T세포</text>
  <path class="lead-line" d="M150 246 L 150 214"/>
  <text class="t-bad" x="196" y="240">여기서 막힌다</text>

  <!-- 오른쪽: 항체가 표지를 덮는다 -->
  <path class="organ2 cut" d="M420 104 C 448 88, 490 90, 512 110 C 528 132, 522 168, 496 184
                              C 468 200, 428 192, 412 168 C 398 146, 402 120, 420 104 Z"/>
  <path class="hatch" d="M420 104 C 448 88, 490 90, 512 110 C 528 132, 522 168, 496 184
                         C 468 200, 428 192, 412 168 C 398 146, 402 120, 420 104 Z"/>
  <text class="t-lab" x="464" y="150" text-anchor="middle">종양</text>
  <circle class="good" cx="412" cy="82" r="13"/>
  <circle class="good" cx="524" cy="92" r="13"/>
  <!-- 항체 Y 모양 -->
  <path fill="none" stroke="var(--fig-vein,#4a6ec2)" stroke-width="2.6"
        d="M412 68 L 412 54 M412 54 L 402 44 M412 54 L 422 44"/>
  <path fill="none" stroke="var(--fig-vein,#4a6ec2)" stroke-width="2.6"
        d="M524 78 L 524 64 M524 64 L 514 54 M524 64 L 534 54"/>
  <text class="t-sm" x="336" y="46">항체가 표지를 덮는다</text>
  <!-- 킬러 T세포가 들어간다 -->
  <circle class="cell" cx="464" cy="264" r="16"/>
  <path class="flow" d="M464 246 L 464 206"/>
  <text class="t-sm" x="464" y="298" text-anchor="middle">킬러 T세포가 다시 일한다</text>

  <text class="t-sm" x="18" y="316">조절 T세포를 없애면 몸 전체의 염증이 폭주한다. 그래서 세포가 아니라 표지만 덮는다.</text>
</svg>'''

# ── 그림 12. 도파민이 뿌려지는 네 곳 ────────────────────────────────────────
# 뇌 시상단면에 출발점과 도착지를 얹고 설명은 오른쪽 열에 세운다.
FIG_DOPAMINE = '''<svg viewBox="0 0 640 340" role="img" aria-label="중뇌에서 출발해 선조체·변연계·전두엽·뇌하수체로 가는 도파민 회로">
  <text class="t-lab" x="18" y="22">뇌 시상단면 — 도파민 회로</text>

  <path class="organ cut" d="M34 160 C 34 96, 92 52, 166 52 C 236 52, 288 88, 292 142
                             C 296 182, 274 204, 246 210 C 208 218, 146 220, 106 212
                             C 62 204, 34 190, 34 160 Z"/>
  <path class="hatch-w" d="M34 160 C 34 96, 92 52, 166 52 C 236 52, 288 88, 292 142
                           C 296 182, 274 204, 246 210 C 208 218, 146 220, 106 212
                           C 62 204, 34 190, 34 160 Z"/>
  <!-- 소뇌와 뇌간 -->
  <path class="organ2 cut" d="M234 214 C 266 208, 286 222, 282 242 C 276 260, 246 264, 228 252 Z"/>
  <path class="organ2 cut" d="M184 212 C 200 212, 206 230, 202 258 C 198 278, 186 282, 178 276
                              C 174 254, 176 228, 184 212 Z"/>

  <!-- 전두엽 -->
  <path class="lead-line" d="M60 96 C 84 82, 106 80, 124 88"/>
  <text class="t-sm" x="46" y="80">전두엽</text>
  <!-- 선조체 -->
  <ellipse cx="132" cy="140" rx="30" ry="18" class="organ2"/>
  <text class="t-sm" x="132" y="144" text-anchor="middle">선조체</text>
  <!-- 변연계 -->
  <ellipse cx="176" cy="180" rx="26" ry="15" class="organ2"/>
  <text class="t-sm" x="176" y="184" text-anchor="middle">변연계</text>
  <!-- 중뇌 출발점 -->
  <circle class="bad" cx="226" cy="176" r="7"/>
  <text class="t-bad" x="238" y="172">중뇌</text>
  <!-- 뇌하수체 -->
  <circle class="organ2" cx="196" cy="212" r="9"/>
  <text class="t-sm" x="206" y="228">뇌하수체</text>

  <!-- 갈래 -->
  <path class="flow" d="M220 170 C 196 150, 168 140, 158 138"/>
  <path class="flow" d="M222 178 C 212 180, 204 180, 200 180"/>
  <path class="flow" d="M220 168 C 178 120, 132 96, 116 90"/>
  <path class="flow" d="M222 184 C 210 196, 202 202, 198 204"/>

  <!-- 오른쪽 설명 -->
  <text class="t-lab" x="330" y="70">선조체로 — 몸이 외운 동작</text>
  <text class="t-sm" x="330" y="88">자전거·걷기·운전을 자동으로 돌린다.</text>
  <text class="t-bad" x="330" y="104">끊기면 파킨슨병. 걸음을 시작 못 한다.</text>

  <text class="t-lab" x="330" y="146">변연계로 — 마음</text>
  <text class="t-sm" x="330" y="164">지금 하는 일이 신나는 일이라고 알린다.</text>

  <text class="t-lab" x="330" y="206">전두엽으로 — 전략과 동기</text>
  <text class="t-sm" x="330" y="224">이 일을 계속할 이유를 만든다.</text>
  <text class="t-sm" x="330" y="240">여기가 모자라면 집중이 안 된다.</text>

  <text class="t-lab" x="330" y="282">뇌하수체로 — 성격이 다른 갈래</text>
  <text class="t-sm" x="330" y="300">젖 분비를 멈추라는 신호를 준다.</text>

  <text class="t-sm" x="18" y="326">신경 전달 물질이 옆 세포 하나를 켜고 끈다면, 도파민은 구역 전체에 뿌려 분위기를 정한다.</text>
</svg>'''


# ── 그림 13. 포만 신호가 보상 회로에도 닿는다 ───────────────────────────────
# 왼쪽은 장에서 나오는 호르몬, 오른쪽은 그 호르몬이 붙는 뇌 안의 자리.
FIG_GLP1 = '''<svg viewBox="0 0 640 300" role="img" aria-label="장에서 나온 GLP-1이 뇌의 보상 회로 수용체에 닿는 경로">
  <text class="t-lab" x="18" y="22">장 — 먹으면 나온다</text>
  <text class="t-lab" x="330" y="22">뇌 — 붙는 자리가 여기에도 있다</text>

  <!-- 장 단면 -->
  <path class="organ2 cut" d="M40 96 C 84 78, 148 82, 176 104 C 190 132, 178 168, 150 182
                              C 112 200, 60 190, 44 164 C 30 142, 30 112, 40 96 Z"/>
  <path class="hatch" d="M40 96 C 84 78, 148 82, 176 104 C 190 132, 178 168, 150 182
                         C 112 200, 60 190, 44 164 C 30 142, 30 112, 40 96 Z"/>
  <path class="lead-line" d="M52 116 C 84 104, 132 108, 158 122"/>
  <path class="lead-line" d="M50 142 C 86 130, 138 134, 164 148"/>
  <text class="t-sm" x="104" y="212" text-anchor="middle">장 내분비 세포</text>
  <circle class="good" cx="188" cy="112" r="7"/>
  <circle class="good" cx="196" cy="140" r="7"/>
  <circle class="good" cx="186" cy="166" r="7"/>
  <text class="t-lab" x="176" y="248">GLP-1</text>
  <text class="t-sm" x="176" y="266">인슐린을 늘리고</text>
  <text class="t-sm" x="176" y="282">그만 먹으라고 알린다</text>
  <path class="flow" d="M206 130 C 250 118, 286 106, 316 100"/>

  <!-- 뇌 -->
  <path class="organ cut" d="M352 96 C 352 62, 388 40, 434 40 C 480 40, 512 62, 516 96
                             C 520 122, 506 138, 486 142 C 458 148, 412 148, 388 142
                             C 362 136, 352 118, 352 96 Z"/>
  <path class="hatch-w" d="M352 96 C 352 62, 388 40, 434 40 C 480 40, 512 62, 516 96
                           C 520 122, 506 138, 486 142 C 458 148, 412 148, 388 142
                           C 362 136, 352 118, 352 96 Z"/>
  <circle class="bad" cx="470" cy="120" r="6"/>
  <text class="t-sm" x="480" y="118">VTA</text>
  <ellipse cx="404" cy="106" rx="24" ry="14" class="organ2"/>
  <text class="t-sm" x="404" y="110" text-anchor="middle">측좌핵</text>
  <path class="flow" d="M462 116 C 442 110, 424 106, 430 106"/>
  <!-- 수용체 표시 -->
  <path class="vessel" d="M392 92 L 388 80" stroke="var(--fig-good,#2f8f6b)"/>
  <path class="vessel" d="M416 92 L 420 80" stroke="var(--fig-good,#2f8f6b)"/>
  <circle class="good" cx="386" cy="72" r="6"/>
  <circle class="good" cx="422" cy="72" r="6"/>
  <text class="t-sm" x="336" y="60">여기에도 GLP-1 수용체가 있다</text>

  <text class="t-lab" x="330" y="186">그래서 줄어드는 건 식욕만이 아니다</text>
  <text class="t-sm" x="330" y="206">술·담배·마약을 향한 갈망도 함께 준다.</text>
  <text class="t-sm" x="330" y="222">중독된 뇌는 좋아함은 그대로인데</text>
  <text class="t-sm" x="330" y="238">원함만 비정상적으로 커진 상태다.</text>
  <text class="t-bad" x="330" y="266">다만 관찰 연구가 앞서 있고</text>
  <text class="t-bad" x="330" y="282">임상은 이제 시작 단계다.</text>
</svg>'''


CARDS = [{
    'section': SEC_INFLAM,
    'topic': ('market', '염증 · 면역'),
    'title': '염증은 나쁜 게 아니다. 과하게 먹는 것이 만성 염증을 만든다',
    'gain': '급성과 만성이 어떻게 다른지, 그리고 살이 왜 그 자체로 염증인지.',
    'meta': META_EP155,
    'quote': '"결국엔 어떻게 보면은 다 과잉 칼로리 때문에 벌어진 사건이라고 볼 수 있겠습니다."',
    'note': ('지식인초대석 EP.155, 2부작 중 1부다. 자막을 옮긴 요약이라 표기 일부는 발언 그대로 두었다. '
             '진단이나 처방이 아니다.'),
    'links': LINKS_EP155,
    'slim_oneliner': ('염증은 몸이 침입자와 싸울 때 나는 현상이다. 감기로 붓고 열이 오르는 고통도 균이 만드는 게 '
                      '아니라 우리 편이 만든다. 이승훈 교수는 병을 만드는 쪽이 그 싸움에 딸려오는 '
                      '<b>부수적 손상</b>이라고 정리한다. 그리고 그 손상이 5년 10년 이어지게 만드는 흔한 원인이 '
                      '<b>남은 칼로리</b>다. 혈관 쪽에서는 동맥경화로, 간 쪽에서는 지방간으로 나온다.'),
    'slim_points': [
        '<b>염증은 선천 면역이 일한 결과다.</b> 처음 보는 침입자에게도 곧바로 달려드는 1차 방어를 선천 면역이라 '
        '하고, 주인공은 대식 세포와 호중구다. 이들이 싸우는 자리가 붓고 열이 난다.',

        '<b>정상 조직도 같이 죽는다.</b> 불난 집을 끄면서 옆집에도 물을 뿌리고 출입을 막는 것과 같다. 넓게 '
        '다치면 그만큼 넓게 염증이 된다.',

        '<b>면역 세포에는 브레이크가 없다.</b> 회사 자본이 1억인데 5억을 달라 하고, 회사가 망하든 말든 제 '
        '프로젝트만 끝내려 든다는 게 그의 비유다. 다리가 끝장나도 신경 쓰지 않는다.',

        '<b>급성은 한 번 다치고 끝난다.</b> 만성은 뭐가 들어왔는지도 모르는 채 같은 반응을 되풀이한다. 5년 10년 '
        '지나면 장기가 조용히 망가지고, 그 과정에서 암·동맥경화증·뇌졸중이 나온다.',

        '<b>죽은 세포도 염증을 부른다.</b> 세포가 터지면 안에 있던 물질이 쏟아지고 몸은 그걸 침입자로 읽는다. '
        '심근경색이나 뇌경색에서 죽은 부위가 처음보다 커지는 까닭이 여기 있다. 치우려는 힘이 너무 세서 옆에 '
        '있던 멀쩡한 세포까지 죽는다.',

        '<b>바깥에서 오는 만성 염증도 있다.</b> 헤르페스 바이러스, 결핵, 나병, 헬리코박터처럼 몸에 눌러앉아 계속 '
        '자극하는 것들이다. 그래도 훨씬 흔한 쪽은 몸 안에서 나오는 원인, 곧 비만이다.',

        '<b>살이 찌면 지방 세포 개수는 그대로고 부피만 커진다.</b> 세포가 빵빵해지면 지방산이 삐져나오고, 쓰이지 '
        '않은 채 혈액을 떠도는 그걸 호중구가 침입 물질로 본다. 지방산은 원래 근육과 심장이 평상시에 태우는 '
        '연료다. 갑자기 뛸 때만 포도당을 쓴다.',

        '<b>에너지는 쓰는 순서가 있다.</b> 체온과 심장 같은 기본 생존에 70%, 머리 쓰고 몸 쓰는 데 20% 남짓, '
        '그러고 남아야 면역으로 간다. 굶으면 면역부터 줄어 병에 잘 걸리고, 다음에 힘이 빠지고, 체온까지 '
        '떨어지면 죽는다.',

        '<b>1970년대부터 에너지가 남기 시작했다.</b> 값싼 고칼로리 음식이 퍼지면서 먹고사는 데 문제가 없어지자 '
        '면역에 쓸 몫이 남았다. 면역이 세지면 좋을 것 같지만, 별것 아닌 지방산에도 반응이 커진다.',

        '<b>염증을 키우는 인자는 둘인데 과잉 칼로리가 둘 다 민다.</b> 공격 대상이 늘어나는 쪽과 면역 세포가 '
        '세지는 쪽이다. 그래서 만성 염증은 굶는 사람보다 에너지가 남는 사람에게 생긴다.',

        '<b>혈관에서는 눌리고 터지고 굳는 일이 반복된다.</b> 혈압이 벽을 계속 누르다 터뜨리고, 복구가 제대로 안 '
        '되면 그 자리가 딱딱해진다. 손상된 벽으로 콜레스테롤이 파고들어 대식 세포와 싸우고, 콜레스테롤이 농축돼 '
        '쌓인 것이 동맥경화증이다.',

        '<b>간은 갈 곳 잃은 지방을 떠안는다.</b> 간이 만든 지방을 근육이 안 쓰고 내장 지방도 꽉 차면 간세포가 '
        '지방 세포처럼 지방으로 찬다. 그게 지방간이다. 지방이 터져 간세포가 죽으면 지방간염, 복구하다 굳으면 '
        '간경화, 복구하던 세포가 급발진하면 암이 된다.',

        '<b>요즘 간 질환은 원인이 달라졌다.</b> 술과 바이러스가 가장 흔하다고들 알지만, 대사 이상에서 오는 간 '
        '질환이 중요한 축이 됐다.',
    ],
    'figs': [
        (4, '그림 1 · 조직 단면',
         FIG_INFLAM,
         '급성은 침입 지점 둘레에서 멈추고, 만성은 같은 반응이 되풀이돼 손상이 조직 전체로 번진다. 두 그림에서 '
         '달라지는 것은 점선 안쪽 넓이 하나다.'),
        (11, '그림 2 · 동맥 벽 세로단면',
         FIG_ARTERY,
         '벽은 세 층이다. 혈압에 눌려 터진 자리를 복구하다 굳고, 그 틈으로 콜레스테롤이 파고들어 대식 세포와 '
         '싸운다. 그 자리에 지방이 농축돼 쌓인 것이 동맥경화다.'),
        (12, '그림 3 · 복부 관상단면',
         FIG_TORSO,
         '남은 에너지가 도는 순서를 번호로 따라간다. 간이 만들어 내보내고(1), 근육이 안 받고(2), 내장 지방도 '
         '자리가 없어(3), 결국 간세포가 떠안는다(4). 그 상태가 지방간이다.'),
    ],
    'slim_stats': [('부수적 손상', '싸움에 딸려오는 정상 조직 손상. 병은 여기서 온다'),
                   ('70% · 20%', '기본 생존과 활동이 먼저 가져가는 에너지 몫'),
                   ('5~10년', '만성 염증이 장기를 조용히 망가뜨리는 시간'),
                   ('지방', '남은 탄수화물도 남은 지방도 결국 여기로 간다')],
}, {
    'section': SEC_INFLAM,
    'topic': ('market', '면역 · 암'),
    'title': '면역을 말리는 세포가 있다. 암이 그 세포를 구슬린다',
    'gain': '2025년 노벨생리의학상이 무엇을 밝혔고, 그것이 왜 항암제의 개념을 뒤집었는지.',
    'meta': META_NOBEL,
    'quote': '"조절 티세포가 너무 관용을 해. 너무 참아. 그래서 암세포를 계속 냅둔다."',
    'note': ('2025년 노벨생리의학상(말초 면역 관용) 해설이다. 치료 선택에 관한 조언이 아니고 기전 설명이며, '
             '관문 억제제와 CAR-T는 모두 전문 진료 영역이다.'),
    'links': LINKS_NOBEL,
    'slim_oneliner': ('면역 연구는 오랫동안 달려드는 쪽만 봤다. 다 죽인 뒤에도 멈추지 않으면 몸이 남아나지 '
                      '않으니 말리는 쪽도 있어야 한다. 그게 <b>조절 T세포</b>다. 암은 이 세포를 자기 편으로 '
                      '만들어 공격을 막는다.'),
    'slim_points': [
        '<b>이 세포가 하는 일은 셋이다.</b> 균을 다 죽인 뒤에도 계속되는 선천 면역을 멈추고, 자기 몸을 공격하는 '
        '자가면역을 멈추고, 과열된 킬러 T세포를 멈춘다.',

        '<b>있을 것이라는 생각은 5~60년 전부터 있었다.</b> 억제 T세포라는 이름으로 찾았다는 발표가 나왔다가 '
        '뒤집혀, 있어야 설명이 되는데 실체가 없는 유령이 됐다.',

        '<b>그래서 진짜를 찾은 논문도 무시당했다.</b> 사카구치 시몬이 1995년에 낸 논문은 심사에서 계속 밀려 낮은 '
        '학술지까지 내려갔다. 2003년에 그 세포를 알아보는 표지 FOXP3를 정리하면서 판이 뒤집혔다.',

        '<b>암은 이 세포를 자기 편으로 만든다.</b> 종양이 내는 물질로 주변 조절 T세포를 깨워 "여기는 정상 조직" '
        '이라고 알리게 만든다. 그렇게 만들어진 구역이 종양 미세환경이다.',

        '<b>구슬려진 세포는 표지를 내민다.</b> CTLA-4와 PD-1이다. 세포를 없애면 몸 전체의 염증이 폭주하니, '
        '종양 주변에서 내밀고 있는 그 표지만 항체로 덮는다. 이것이 면역 관문 억제제다.',

        '<b>여보이·옵디보·키트루다가 그렇게 나왔다.</b> CTLA-4를 막는 것이 첫 약이었고, PD-1을 막는 계열에서 '
        '키트루다가 세계 1위 약이 됐다.',

        '<b>2018년 노벨상은 표지를 발견한 두 사람에게 갔다.</b> 정작 두 사람은 그것이 조절 T세포의 표지인 줄 '
        '몰랐다. 특이한 T세포가 있다는 것까지가 그때의 발견이었다.',

        '<b>항암제의 전제가 바뀌었다.</b> 1990년대까지는 몸이 암을 못 죽이니 독한 약으로 죽인다는 발상이었고, '
        '그래서 분열이 빠른 위장과 머리카락과 피부가 같이 망가졌다. 지금은 몸이 죽일 수 있는데 신호가 막혀 있을 '
        '뿐이라고 본다.',

        '<b>CAR-T도 같은 이유로 관문 억제제를 함께 쓴다.</b> 환자의 T세포를 꺼내 강하게 만들어 넣어도 조절 '
        'T세포가 말리면 소용이 없다.',

        '<b>10년 만에 약의 판이 바뀌었다.</b> 2010년 미국 상위권은 스타틴과 항혈전제 같은 혈관 약이었는데, '
        '2020년에는 이름이 -맙으로 끝나는 항체 치료제가 상위를 채웠다.',

        '<b>번역이 오해를 만들었다.</b> regulatory는 볼륨을 올리고 내리는 조절이 아니고 감시하다 억제한다는 '
        '뜻이다. 식약처 같은 규제 기관을 떠올리면 맞는다는 것이 그의 설명이다.',
    ],
    'figs': [
        (5, '그림 4 · 종양이 구슬린 세포',
         FIG_TREG,
         '왼쪽은 구슬려진 조절 T세포가 표지를 내밀어 킬러 T세포를 막는 상태다. 오른쪽처럼 항체로 그 표지만 덮으면 '
         '킬러 T세포가 다시 들어간다.'),
    ],
    'slim_stats': [('말리는 쪽', '조절 T세포가 면역에서 맡은 자리'),
                   ('CTLA-4 · PD-1', '구슬려진 세포가 내미는 표지. 항체가 덮는 지점'),
                   ('1995 → 2003', '무시당한 논문과 판을 뒤집은 논문 사이의 8년'),
                   ('2018 · 2025', '표지에 준 노벨상과 그 위층에 준 노벨상')],
    'clash': [
        ('본인 평가', '<b>세 수상자 중 사카구치의 기여가 가장 크다는 것은 그의 평가다.</b> 나머지 두 사람의 '
                   '업적도 훌륭하다고 함께 밝혔다.'),
        ('오해 방지', '<b>조절 T세포를 없애는 것은 방법이 아니다.</b> 그러면 몸 전체의 염증이 폭주한다. 그래서 '
                   '종양 주변의 표지만 덮는 쪽으로 갔다.'),
    ],
}, {
    'section': SEC_DIABETES,
    'topic': ('market', '당뇨 · 대사'),
    'title': '당뇨는 포도당이 넘쳐서 생기는 병이 아니다. 지방산이 신호를 막는다',
    'gain': '2형 당뇨가 시작되는 자리, 한국인이 더 위험한 이유, 그리고 되돌아오는 경우.',
    'meta': META_EP156,
    'quote': '"사실은 포도당이 많아서 생긴 병이 아니고 지방이 많아져서 생긴 병이고"',
    'note': ('지식인초대석 EP.156, EP.155의 2부다. 수치는 그가 말한 값이고 진단이나 처방이 아니다. '
             '20대 당뇨 환자 증가 수치는 자막이 손상돼 방향만 싣는다.'),
    'links': LINKS_EP156,
    'slim_oneliner': ('인슐린은 포도당이 왔다고 세포에 알리는 <b>초인종</b>이다. 지방 세포에서 새어 나온 지방산이 '
                      '그 초인종을 뻑뻑하게 만들면, 세포는 포도당을 못 쓰고 혈액에는 포도당과 인슐린이 함께 쌓인다. '
                      '그래서 높은 혈당은 원인보다 결과에 가깝다.'),
    'slim_points': [
        '<b>인슐린은 초인종이다.</b> 췌장 베타 세포가 만들어, 들어온 포도당을 각 세포로 들여보내라고 알린다. '
        '지방산이 이 신호 체계를 망가뜨리면 인슐린이 눌러도 문이 열리지 않는다.',

        '<b>완전히 고장 난 게 아니라 뻑뻑해진 상태다.</b> 그래서 인슐린이 많이 나오면 결국 누를 수는 있다. '
        '문제는 얼마나 낼 수 있느냐다.',

        '<b>한국인은 같은 비만도에서 더 위험하다.</b> 체형이 작고 췌장의 인슐린 생산 능력도 낮은 편인데, 먹는 음식은 '
        '단위 질량당 열량이 높은 쪽으로 바뀌었다. 그래서 췌장 기능 부전을 이른 나이에 겪는다. 아시아 지역의 당뇨 발생 '
        '비율이 빠르게 오르는 배경이다.',

        '<b>해로움은 노출 기간에 비례한다.</b> 고혈압과 원리가 같다. 혈압 자체는 몸이 필요해서 올리는 것이고, '
        '나쁜 이유는 오래 노출되면 혈관이 손상되기 때문이다.',

        '<b>남은 포도당은 아무 데나 가서 붙는다.</b> 혈색소에 붙은 것을 재는 게 당화혈색소이고 알부민에도 붙는다. '
        '몸은 이렇게 붙은 물질을 외부에서 온 것으로 읽고 공격한다. 그래서 있던 동맥경화가 훨씬 빠르게 자란다.',

        '<b>20대에 걸리면 40대에 여든 살의 동맥경화를 겪는다.</b> 50대에 걸린 사람과는 비교가 안 된다는 것이 '
        '그의 표현이다.',

        '<b>진단 기준은 공복 126이다.</b> 경구 당부하 검사에서는 두 시간 뒤 180이나 200, 아무 때나 재서 200을 '
        '넘으면 포도당이 높은 상태로 본다.',

        '<b>당뇨는 관해된다.</b> 완치와는 다르다. 예전 생활로 돌아가면 다시 걸리기 때문이다. 그래도 식단과 운동을 '
        '권했을 때 3~40%가 정상 수치를 만들어 온다. 당화혈색소 9점대가 6개월 만에 정상이 되어 몇 년을 유지한 '
        '사례도 있다.',

        '<b>망가진 초인종은 복구된다.</b> 다만 지방산이 계속 와서 다시 망가뜨릴 뿐이다. 그 상태가 오래가면 '
        '인슐린을 내던 베타 세포가 망가지기 시작하고, 그때부터는 약을 써도 잘 듣지 않는다.',

        '<b>진짜 합병증은 큰 혈관이다.</b> 눈·신장·신경 합병증은 모세혈관 문제다. 미국 당뇨학회는 10~20년 전부터 '
        '당뇨가 큰 혈관을 막는다는 캠페인을 해 왔고, 가장 큰 합병증은 심근경색과 뇌졸중으로 죽는 것이다.',

        '<b>동맥경화 위험 요인 순서에서 당뇨는 둘째다.</b> 고혈압 다음이고 고지혈증과 술·담배보다 앞이다. 지금은 '
        '뇌졸중과 심근경색에 미치는 영향에서 고혈압만큼 흔하다.',
    ],
    'figs': [
        (2, '그림 5 · 세포막 단면',
         FIG_INSULIN,
         '인슐린이 수용체를 눌러 포도당 문이 열리는 것이 정상이다. 지방산이 끼면 신호가 약해지고, 포도당은 밖에 '
         '남고, 몸은 인슐린을 더 낸다.'),
    ],
    'slim_stats': [('126', '공복 혈당 당뇨 진단 기준'),
                   ('20대 → 40대', '일찍 걸리면 여든 살의 동맥경화를 겪기 시작하는 나이'),
                   ('3~40%', '식단과 운동만으로 정상 수치로 돌아오는 환자 비율'),
                   ('고혈압 다음', '동맥경화 위험 요인 순서에서 당뇨의 자리')],
    'clash': [
        ('본인 유보', '<b>관해 비율 3~40%는 그의 진료 경험에서 나온 값이다.</b> 근거 통계는 영상에서 제시되지 '
                   '않았다.'),
        ('오해 방지', '<b>관해는 완치가 아니다.</b> 조절하며 살면 당뇨가 아닌 상태로 지낼 수 있다는 뜻이고, '
                   '예전 생활로 돌아가면 다시 걸린다고 본인이 못 박았다.'),
    ],
}, {
    'section': SEC_DIABETES,
    'topic': ('market', '과당 · 과일'),
    'title': '같은 열량이면 과일이 밀가루보다 나쁘다. 과당은 간만 받는다',
    'gain': '과일이 왜 멈추기 어려운지, 그리고 적당히 먹어도 일부가 지방이 되는 이유.',
    'meta': META_FRUIT,
    'quote': '"그 과당은 지방이 되기 위한 탄수화물이에요."',
    'note': ('EP.156과 EP.108 두 편에서 같은 주제를 다뤄 한 장으로 합쳤다. 과일의 당 비율은 그가 동양 과일 '
             '기준으로 말한 대략값이라 품종에 따라 다르다.'),
    'links': LINKS_FRUIT,
    'slim_oneliner': ('밀가루는 분해되면 거의 전부 포도당이 되고 포도당은 모든 세포가 나눠 쓴다. 과일은 절반이 '
                      '<b>과당</b>인데, 과당은 몸에서 간만 받는다. 그래서 운동하지 않으면 적당량을 먹어도 일부는 '
                      '곧장 지방이 된다.'),
    'slim_points': [
        '<b>맛을 느끼려면 분자가 작아져야 한다.</b> 탄수화물·지방·단백질은 분자량이 커서 혀가 맛을 못 느낀다. '
        '잘게 쪼개져 포도당과 과당이 되면 그때 단맛이 난다. 둘이 하나씩 붙은 것이 설탕이다.',

        '<b>과당은 포도당보다 1.5배 달다.</b> 밀가루는 분해되지 않은 상태라 맛이 없는데 과일은 이미 쪼개진 '
        '포도당과 과당이 들어 있어 먹자마자 달다. 귤을 하나 먹으면 한 박스를 먹게 되는 이유다.',

        '<b>포도당은 모든 세포가 쓰고 과당은 간만 쓴다.</b> 다른 장기가 받지 않으니 떠돌다 간으로 간다. 간은 '
        '과당을 젖산으로 바꿔 일부 쓰는데, 젖산은 운동을 많이 할 때 쓰인다.',

        '<b>그래서 적당량을 먹어도 일부는 지방이 된다.</b> 적당량의 백미는 대부분 포도당이라 살로 가지 않는다. '
        '과당은 심지어 부족하게 먹어도 일정 부분이 지방으로 간다. 이런 성분은 과당뿐이다.',

        '<b>과일은 원래 먹히려고 단맛을 만들었다.</b> 동물이 먹고 돌아다니며 배설해야 씨가 퍼진다. 먹는 쪽의 '
        '이득이 지방으로 잘 바뀐다는 것이었다. 곰이 동면 전에 산의 과일을 미친 듯이 먹는 이유가 여기 있다.',

        '<b>우리가 먹는 과일은 야생 과일이 아니다.</b> 사람이 맛있다고 느끼는 것만 골라 키운 재배종이라 과육이 '
        '크고 과당이 많다. 야생에 두면 대부분 죽는다.',

        '<b>액상 과당은 과당 비율이 55%다.</b> 미국에 옥수수가 남아돌자 옥수수로 만든 시럽이고 설탕보다 훨씬 '
        '싸다. 음료 회사들이 대량으로 쓰기 시작했고, 미국 비만의 주범으로 탄산음료가 지목되는 배경이다.',

        '<b>그렇다고 과일을 악마화할 일은 아니다.</b> 미네랄과 비타민 같은 미량 영양소가 많다. 다만 비만을 '
        '걱정하면서 과일을 열심히 먹거나 당뇨 환자가 과일을 열심히 먹는 것은 과학적으로 맞지 않다는 이야기다.',
    ],
    'figs': [
        (4, '그림 6 · 과당의 외길',
         FIG_FRUCTOSE,
         '포도당은 뇌와 심장과 근육이 나눠 쓴다. 과당은 간 하나만 받고, 운동으로 젖산을 쓰지 않으면 그대로 '
         '지방이 된다.'),
    ],
    'slim_stats': [('1.5배', '과당이 포도당보다 단 정도'),
                   ('50% / 50%', '과일의 포도당 대 과당 비율(그가 말한 대략값)'),
                   ('55%', '액상 과당의 과당 비율'),
                   ('간 하나', '과당을 받아 주는 장기의 수')],
}, {
    'section': SEC_EAT,
    'topic': ('market', '식사 · 탄수화물'),
    'title': '밥·빵 종류가 문제가 아니라 얼마나 많이 먹느냐가 문제다',
    'gain': '정제 탄수화물이 나쁘다는 말의 진짜 뜻, 그리고 반찬 위주 식사가 건강식이 아닌 이유.',
    'meta': META_EP155,
    'quote': '"맛있는 걸 찾아먹기 때문에 살이 찌는 거는 기정사실이다."',
    'note': '단순당이 나쁜 이유를 그는 성분보다 과식에서 찾는다. 진단이나 처방이 아니다.',
    'links': LINKS_EP155,
    'slim_oneliner': ('"밥은 괜찮고 빵이 더 나쁘다"는 구분에 그는 전혀 맞지 않다고 답한다. 흰쌀밥과 흰빵은 같은 '
                      '부류다. 둘 다 몸이 할 소화를 미리 해 둔 상태라 넘기는 데 힘이 안 들고 단맛이 바로 올라온다. '
                      '몸은 그걸 당장 쓸 에너지로 읽고 더 먹을 준비를 한다.'),
    'slim_points': [
        '<b>탄수화물은 염증 물질이 아니다.</b> 들어온다고 염증이 생기지 않는다. 너무 많이 들어와 보관하는 '
        '과정에서 생기는 일이 염증이 될 뿐이다.',

        '<b>정제 탄수화물이 맛있는 까닭이 곧 문제다.</b> 부드러운 빵과 흰쌀밥은 몸이 할 소화를 미리 해 둔 '
        '상태다. 씹고 녹이는 데 힘이 안 드니 몸이 좋아하고, 겉에 녹아 있는 포도당 맛과 부드러운 식감에 손이 '
        '계속 간다. 더 잘게 쪼개 놓으면 단맛이 되고, 설탕이 되고, 디저트가 된다.',

        '<b>단맛을 좋아하게 된 건 진화의 지시다.</b> 위가 애쓰지 않아도 바로 에너지가 되니 당장 먹으라는 '
        '신호다. 자연에서 단맛을 내는 게 과일뿐이었던 탓에 사람도 다른 포유류도 그렇게 굳었다.',

        '<b>3대 영양소 중 단백질만 다르게 쓰인다.</b> 몸을 이루고 기능하는 성분으로 가고, 에너지로 바꾸는 걸 몸이 '
        '싫어한다. 탄수화물과 지방은 연료인데, 자동차와 달리 몸은 남아도 받아서 전부 지방으로 바꾼다.',

        '<b>반찬 많이 먹기는 건강식이 아니다.</b> 나물과 야채는 야생 그대로는 맛이 없고 독성도 있어서, 먹을 만하게 '
        '만드느라 설탕과 소금과 조미료가 들어간다. 소금은 그대로 고혈압으로 가고, 입이 즐거우면 결국 더 먹는다.',

        '<b>채소를 먼저 먹는 것은 일리가 있다.</b> 식이섬유는 사람이 분해하지 못하는 탄수화물이라 위를 차지하고, '
        '뒤이어 들어온 탄수화물의 흡수 속도를 완만하게 한다. 소나 말은 위의 미생물이 이걸 지방산으로 바꿔 줘서 '
        '풀을 먹고도 고기를 먹은 효과가 나지만 사람은 그렇지 못하다.',

        '<b>공복 올리브유는 혈관을 씻지 않는다.</b> 올리브유 자체는 불포화 지방산인 올레산이 가장 많은 좋은 '
        '기름이라 대두유 대신 조리에 쓰는 건 낫다. 그러나 한 숟갈이 100~200kcal이다. 아침에 따로 더 먹는 건 '
        '"영양학적으로 이상한 행동"이라는 것이 그의 표현이다.',

        '<b>맛집은 좋은 습관이 아니다.</b> 가서 한 숟갈 먹고 만족하고 나올 수 있으면 가도 된다는 게 그의 답이다.',
    ],
    'figs': [
        (4, '그림 7 · 소화관과 세 갈래',
         FIG_FUEL,
         '위와 소장을 지나 간에서 갈린다. 단백질은 몸을 이루는 쪽으로 가고, 탄수화물과 지방은 그날 쓸 연료로 '
         '간다. 남은 만큼은 예외 없이 지방이 된다.'),
    ],
    'slim_stats': [('포도당', '곡식이 분해된 마지막 산물. 밥도 빵도 같다'),
                   ('100~200kcal', '올리브유 한 숟갈의 열량'),
                   ('식이섬유', '사람이 분해 못 하는 탄수화물. 흡수 속도를 늦춘다'),
                   ('소금', '반찬 위주 식사에서 곧장 고혈압으로 가는 성분')],
}, {
    'section': SEC_EAT,
    'topic': ('market', '단백질 · 근육'),
    'title': '단백질은 노인이 더 먹어야 하는데 우리나라는 거꾸로 간다',
    'gain': '얼마나 먹어야 하는지, 품질이 무엇으로 갈리는지, 그리고 보충제가 몸에서 무엇이 되는지.',
    'meta': META_PROTEIN,
    'quote': '"일단 한번 잃은 근육은 그 나이 때는 생기질 않아요."',
    'note': ('네 편에 흩어져 있던 단백질 이야기를 한 장으로 모았다. 신장 질환처럼 사정이 있으면 권장량이 '
             '달라지니 그대로 적용하기 전에 의료진과 확인한다.'),
    'links': LINKS_PROTEIN,
    'slim_oneliner': ('필요량은 젊을 때 체중 1kg당 하루 0.9g, 노인은 1.2g이다. 그런데 나이가 들면 이가 나빠지고 '
                      '소화가 힘들어 국밥과 칼국수 같은 탄수화물로 기운다. 근육은 한번 잃으면 그 나이에는 다시 '
                      '생기지 않아서, 목표가 만들기에서 <b>유지</b>로 바뀐다.'),
    'slim_points': [
        '<b>품질 기준은 계란 흰자다.</b> 이걸 100으로 놓고 식물성 단백질은 그보다 낮게, 닭가슴살 같은 동물성은 '
        '더 높게 매긴다.',

        '<b>필요량은 나이에 따라 다르다.</b> 젊을 때 0.9g/kg, 노인은 1.2g/kg이다. 70kg이면 하루 70g 안팎이고 '
        '계란 한 개가 6g쯤 된다.',

        '<b>미국의 새 지침은 과하다.</b> 1.2~1.6g/kg으로 올렸는데 한국은 기존 0.8g도 채우기 힘든 나라다. '
        '그는 이 변화를 특정 인물의 확증 편향이 반영된 것 아니냐고 보고, 목표로 삼을 값은 0.8g 정도라고 말한다.',

        '<b>노인이 단백질을 피하게 되는 이유가 있다.</b> 이가 나빠지고 소화력이 떨어지니 고기와 생선이 부담스럽다. '
        '그래서 부드러운 탄수화물 국물 음식으로 기울고 순 탄수화물만 먹게 된다.',

        '<b>그 끝이 근감소증이다.</b> 근육이 말라 병이 없는데도 일어서지 못하고 걷지 못한다. 그때 운동하라고 해도 '
        '단백질을 안 먹으면 근육이 생기지 않는다. 먼저 먹어야 한다는 것이 그의 순서다.',

        '<b>60대 이후의 목표는 유지다.</b> 근육 운동에 더해 단백질 섭취까지 신경 써야 한다고 그는 못 '
        '박는다.',

        '<b>단백질 보충제를 먹으면 아미노산으로 분해된다.</b> 알부민·글루타치온·콜라겐도 마찬가지다. 그 대표 '
        '성분이 글루탐산이고, 글루탐산은 MSG와 같은 성분이다. 그래서 "조미료를 퍼먹는 것과 동일한 효과"라는 '
        '말이 나온다.',

        '<b>알부민을 주사로 주는 이유가 이것이다.</b> 알부민을 먹으면 위에서 분해되기 때문이다. 저신장증 아이에게 성장호르몬을 '
        '매일 주사로 주는 것도 같은 까닭이다.',

        '<b>그럼 고기는 왜 먹나. 양이 다르다.</b> 단백질 자체는 무맛이고, 고기가 맛있는 건 마이야르 반응과 '
        '식감 덕이다. 그 덕에 맛없는 덩어리를 왕창 먹게 되고, 몸은 그걸 분해해 많은 아미노산을 흡수한다. 간이 '
        '레고 블록처럼 받아 필요한 단백질을 다시 조립한다.',

        '<b>보충제 열풍은 정작 20~30대에서 분다.</b> 질 좋은 단백질이 필요한 쪽은 노인인데, 노인이 먹을 수 있는 '
        '형태로 만드는 것이 좋은 방향이라는 것이 그의 의견이다.',
    ],
    'slim_stats': [('0.9g/kg · 1.2g/kg', '하루 단백질 필요량. 젊을 때와 노인'),
                   ('100', '단백질 품질 기준점. 계란 흰자'),
                   ('MSG', '보충제가 분해돼 나오는 글루탐산의 다른 이름'),
                   ('유지', '60대 이후 근육의 목표. 만들기가 아니다')],
}, {
    'section': SEC_STAGE,
    'topic': ('market', '검사 · 단계'),
    'title': '의사를 만나기 전에 내가 몇 단계인지 안다',
    'gain': '뇌졸중이 오기까지의 네 단계, 그리고 집과 병원에서 확인할 값들.',
    'meta': META_STAGE,
    'quote': '"장전되는 걸 2단계다. 그럼 장전되기 전에 총알을 준비하는 걸 1단계다."',
    'note': ('EP.107의 단계 모델에 EP.155의 검사 지표를 합쳤다. "90%가 안 생긴다"는 그의 표현이고 근거 논문은 '
             '영상에서 제시되지 않았다. 경동맥 초음파 비용은 지역과 기관에 따라 다르다.'),
    'links': LINKS_STAGE,
    'slim_oneliner': ('뇌졸중은 동맥경화라는 <b>장전</b>이 먼저 있고 그날의 혈전이나 파열이 방아쇠를 당기는 병이다. '
                      '그래서 할 일은 증상을 살피는 게 아니라 자기가 몇 단계인지 아는 것이다. 위험 요인만 있으면 '
                      '1단계, 동맥경화가 생기면 2단계, 사건이 3단계다.'),
    'slim_points': [
        '<b>1단계는 위험 요인이 하나라도 있는 상태다.</b> 고혈압·당뇨·고지혈증·술·담배·심방세동·비만이다. 하나만 '
        '있어도 1단계라는 인식이 중요하다.',

        '<b>위험 요인이 곧장 뇌졸중으로 점프하지 않는다.</b> 반드시 장전을 거친다. 그러니 목표는 2단계로 넘어가지 '
        '않는 것이다.',

        '<b>동맥경화는 증상으로 알 수 없다.</b> 두통이나 어지럼증으로 짐작하는 건 불가능하고 영상 장비로만 안다.',

        '<b>가장 싼 장비가 경동맥 초음파다.</b> 싼 곳은 3만 원 수준이다. 동맥경화가 전신 질환이라 목이 깨끗하면 '
        '머리부터 발끝까지 가늠할 수 있고, 뇌에는 있는데 목에는 없을 가능성은 매우 낮다. 2년에 한 번 봐서 계속 '
        '정상이면 안심해도 된다는 것이 그의 정리다.',

        '<b>혈압은 병원에서 재는 게 가장 나쁘다.</b> 병원에 왔다는 사실만으로 15 정도 올라간다. 팔뚝 혈압계로 '
        '집에서, 혈압계와 팔뚝과 심장을 같은 높이에 두고, 2분 가만히 있은 뒤 재고, 첫 값은 버리고 두 번째 값을 '
        '본다. 130에 80을 넘지 않으면 된다.',

        '<b>당뇨는 혈당 대신 당화혈색소로 본다.</b> 6.5%를 넘으면 당뇨, 7.0%를 넘으면 약을 먹어야 하는 경우가 '
        '많고, 6.0% 이하면 정상이다. 넘었으면 살 빼고 운동해서 두 달 뒤에 다시 잰다.',

        '<b>콜레스테롤은 LDL만 본다.</b> 160이면 고지혈증이고 두 달 노력해 130이 나오면 된 것이다.',

        '<b>HS-CRP는 증상이 없을 때 쓰는 초기 지표다.</b> 국내에서 1 이하를 정상이라 하지만 0.2를 넘어 0.4쯤 '
        '나오면 어딘가에서 만성 염증이 도는 신호로 읽는다. 값이 싼데 검진 항목에 잘 없어 따로 요청해야 한다.',

        '<b>허리둘레와 간 효소도 같은 자리에서 본다.</b> 배꼽 둘레가 남자 90cm, 여자 85cm를 넘으면 내장 지방이 '
        '많은 쪽이다. 간 효소 AST와 ALT는 40 이하가 정상이고, 한 번 높은 값보다 꾸준히 높은지가 중요하다.',

        '<b>혈압약은 평생 약이 아닐 수 있다.</b> 50~60세 이전에 생긴 본태성 고혈압이면 진단 직후 6개월은 약 '
        '대신 생활 교정을 먼저 한다. 살을 빼면 필요 혈류량이 줄어 혈압이 내려가고, 약을 썼더라도 나중에 끊게 '
        '되는 경우가 있다.',

        '<b>노인성 고혈압은 다르다.</b> 혈관에 굳은 변화가 이미 와서 마른 사람도 심하게 나온다. 구분 단서는 '
        '형태다. 아래 숫자가 높은 쪽이면 되돌릴 여지가 있고, 160에 70처럼 위아래 차이가 벌어진 형태는 석회화가 '
        '진행된 것이라 평생 쓸 가능성이 높다고 본다.',

        '<b>혈압은 하루 안에서도 움직인다.</b> 아침에 깨어 각성할 때 높고 활동하며 오후에 떨어진다. 오전 내내 '
        '높은데 오후에만 재고 정상이라 하면 안 된다. 한 달치를 기록해 두면 본인이 안다.',

        '<b>이렇게만 하면 90%는 생기지 않는다.</b> 뇌졸중과 심근경색 이야기이고, 얼마 들지도 않는다는 것이 그의 '
        '말이다.',
    ],
    'figs': [
        (2, '그림 8 · 혈관이 밟는 네 단계',
         FIG_STAGE,
         '검사로 잡아야 하는 것은 2단계다. 이 단계는 증상을 만들지 않아서, 재지 않으면 장전된 줄 모른 채 산다.'),
        (9, '그림 9 · 무엇을 어디서 재나',
         FIG_MEASURE,
         '집에서 둘, 피검사에서 셋이다. 검사에서 정상이라고 들어도 HS-CRP가 0.2를 넘었다면 생활에서 낮출 '
         '대상으로 본다.'),
    ],
    'slim_stats': [('0 · 1 · 2 · 3', '정상, 위험 요인, 동맥경화(장전), 사건(방아쇠)'),
                   ('3만 원 · 2년', '경동맥 초음파 비용과 다시 볼 주기'),
                   ('130 / 80', '집에서 확인할 혈압 상한'),
                   ('6.5% · 160', '당화혈색소 당뇨 기준과 LDL 고지혈증 기준')],
    'clash': [
        ('본인 유보', '<b>허리둘레 기준은 정밀하지 않다.</b> 키나 체격이 크면 90cm를 쉽게 넘는다는 한계를 그가 '
                   '인정한다.'),
        ('출처 없음', '<b>"90%가 안 생긴다"는 근거 논문이 제시되지 않았다.</b> 관리하면 대부분 막을 수 있다는 '
                   '취지로 읽는 편이 맞다.'),
    ],
}, {
    'section': SEC_STAGE,
    'topic': ('market', '전조 · 응급'),
    'title': '전조증상은 하나뿐이다. 그리고 시간이 곧 치료다',
    'gain': '무엇이 전조이고 무엇이 아닌지, 증상이 나면 집에서 무엇을 하고 무엇을 하지 말지.',
    'meta': META_EMERG,
    'quote': '"48시간 이내 50%라는 얘기는 일주일 한 달 이내 재발은 100%란 얘기예요."',
    'note': '뇌졸중 증상이 잠깐 나타났다 사라졌다면 응급 상황이다. 이 카드는 판단보다 행동 기준에 가깝다.',
    'links': LINKS_EP107,
    'slim_oneliner': ('전조증상을 지진처럼 생각하면 안 된다. 뇌졸중의 전조증상은 <b>뇌졸중 증상</b>이다. 한쪽 '
                      '팔다리가 마비되거나 말이 안 나오는 증상이 10~15분 만에 풀린 것, 그 하나뿐이다.'),
    'slim_points': [
        '<b>두통·어지럼증·입꼬리 처짐·팔다리 저림은 대부분 전조가 아니다.</b> 평상시 증상으로 전조를 알 방법은 '
        '없다.',

        '<b>유일한 전조는 일과성 허혈 발작이다.</b> 동맥경화반이 터지며 혈전이 생겨 혈액이 막혔다가, 운 좋게 '
        '혈전이 저절로 녹아 다시 흐른 경우다. 드물지 않고 30분 이내에 좋아지는 사람이 많다.',

        '<b>동맥경화는 그대로 남는다.</b> 그래서 48시간 안에 재발하는 경우가 50%이고, 일주일에서 한 달 안에는 '
        '사실상 전부 재발한다.',

        '<b>그때는 무조건 병원이다.</b> 응급 센터에서 이 전조를 모르는 곳이 없어 바로 입원시킨다. 민폐라고 생각할 '
        '일이 아니다. 그가 여러 번 강조한 대목이다.',

        '<b>뇌세포는 재생되지 않는다.</b> 간은 간세포의 70%가 죽어도 원래대로 돌아가고 폐나 신장은 남은 세포가 '
        '같은 일을 한다. 뇌는 재생도 안 되고 그 자리의 일을 다른 세포가 대신하지도 못한다. 자리마다 하는 일이 '
        '다르기 때문이다.',

        '<b>그래서 손쓸 시점이 다르다.</b> 뇌는 죽은 다음에 뭘 하는 게 의미가 없고 죽기 전에 해야 한다. 가장 '
        '뛰어난 의사는 죽기 전에 죽을지도 모른다는 것을 알아보는 사람이라는 말이 여기서 나온다.',

        '<b>일교차 큰 날 쓰러진다는 이야기는 과장이 아니다.</b> 다만 인과가 다르다. 이미 수년에서 수십 년 장전된 '
        '사람에게 그날 방아쇠가 당겨지는 것이다.',

        '<b>혈전은 탈수에서 잘 생긴다.</b> 자는 동안 예닐곱 시간 물이 들어가지 않아 조금씩 탈수가 진행되고, '
        '아침에 이미 생긴 상태로 발견되는 경우가 많다. 자기 전에 물을 마시는 것이 도움이 된다.',

        '<b>증상이 생기면 집에서 할 수 있는 것은 없다.</b> 손을 따거나 우황청심원을 먹이는 것은 도움이 되지 '
        '않는다. 119를 부르고 고개만 살짝 옆으로 돌려 둔다. 토할 때 기도로 넘어가면 흡인성 폐렴으로 죽을 수 '
        '있어서다. 자가용으로 가지 않는다.',

        '<b>골든타임은 두 갈래다.</b> 혈전 용해제를 정맥으로 주는 것이 4시간 30분, 막힌 곳까지 도구를 넣어 '
        '피떡을 꺼내는 기계적 제거술이 6시간이다. 6시간이 지나면 죽은 영역이 넓어져 치료가 해가 될 수 있다.',

        '<b>제거술 쪽이 훨씬 잘 듣는다.</b> 혈전 용해제로 효과를 보는 사람은 약 12%인데 제거술 성공률은 '
        '80~90%다. 그래서 일찍 도착해도 병원은 처음부터 둘 다 준비한다. 아스피린은 용해제가 아니고 혈전이 '
        '생기지 않게 막는 약이다.',
    ],
    'slim_stats': [('10~15분', '증상이 나타났다 풀리는 시간'),
                   ('48시간에 50%', '전조 뒤 재발 확률'),
                   ('70% · 0', '간세포와 뇌세포의 회복 가능성'),
                   ('바로 응급실', '전조를 겪었을 때 할 일')],
}, {
    'section': SEC_STAGE,
    'topic': ('market', '통증 · 질병'),
    'title': '통증은 믿을 만한 알람이 아니다',
    'gain': '병의 정의에 왜 「아프다」가 없는지, 그리고 아프지 않은 병이 왜 흔한지.',
    'meta': META_DISEASE,
    'quote': '"이 정의에는 아프다는 말이 없다."',
    'note': ('3부작 모음집의 1부에서 추렸다. 병을 여섯 갈래로 나누는 틀은 그가 진료 경험으로 정리한 개인 '
             '분류이고 학계 표준 용어가 아니다.'),
    'links': LINKS_DISEASE,
    'slim_oneliner': ('의학이 말하는 병은 아픈 상태를 뜻하지 않는다. 정상 범위를 벗어난 상태다. 손상됐는데 못 느끼는 '
                      '경우가 흔하다. 통증이라는 알람은 <b>피부와 소화관 벽</b>에서만 제대로 울리기 때문이다.'),
    'slim_points': [
        '<b>정의에 「아프다」가 없다.</b> 정상 기능이나 구조가 손상돼 건강이 제한되는 상태가 병이다. 20년 동안 '
        '혈압이 160인 줄 몰랐던 환자가 그 예다. 내 몸은 내가 안다는 말이 가장 위험하다.',

        '<b>정상이라는 것도 그어 놓은 선이다.</b> 평균 언저리 95%를 정상이라 부르는 통계적 개념이라, 어디서부터 '
        '병으로 볼지는 사람이 정한 경계다.',

        '<b>알람이 정확한 곳은 바깥과 맞닿은 데뿐이다.</b> 피부와 소화관 벽에서는 세게 울리는데 간 같은 내부 '
        '장기는 암이 꽤 커져도 조용하다. 뇌는 온몸의 감각을 총괄하면서 자기 통증은 못 느낀다. 두통은 뇌가 아닌 '
        '뇌막과 혈관에서 온다.',

        '<b>알람 자체가 고장 나기도 한다.</b> 신경병성 통증이 그렇고, 팔이 잘린 사람이 없는 손가락을 아파하는 '
        '환상통도 같은 원리다. 손가락을 느끼던 신경 말단이 잘린 단면에 살아남아 계속 신호를 보낸다.',

        '<b>구조가 망가진 병과 기능만 떨어진 병은 다르게 부른다.</b> 앞이 disease, 뒤가 disorder다. 정신과 '
        '질환 대부분이 뒤쪽이라 영상으로는 손상이 보이지 않는다.',

        '<b>뇌경색 안에도 둘이 함께 있다.</b> 혈류가 끊겨 죽은 중심부는 되돌릴 수 없고, 혈류가 모자라 기능만 '
        '멈춘 반음영 부위는 되살릴 수 있다. 응급 재개통 치료가 노리는 것이 이 구간이다.',

        '<b>병이 생기는 길을 그는 축구로 나눈다.</b> 공격진에 밀려 먹은 골이 감염·외상·독성·혈관성이고, 방어가 '
        '스스로 무너진 역습골이 노화성과 퇴행성이며, 자책골이 선천성과 결함성이다. 자가면역질환이 자책골 쪽이다.',

        '<b>2차성 질환은 따로 둔다.</b> 위험 요인이 수십 년 쌓여 생기는 병으로 뇌졸중과 심근경색이 여기 든다. '
        '30~40대부터 관리하면 애초에 안 생기게 만들 수 있다는 것이 그의 강조점이다.',

        '<b>자가면역질환은 닮은 구조 때문에 생긴다.</b> 감기 바이러스를 잡으려 만든 항체가 하필 내 몸의 단백질과 '
        '닮으면 평생 자기 몸을 공격한다. 혈관벽이 자주 표적이 된다.',

        '<b>건강수명은 원래 40대에서 끝났다.</b> 19세기까지 조선과 유럽의 평균수명이 그 언저리였다. 80까지 사는 '
        '지금은 이미 이긴 판이니 병을 평생 데리고 갈 친구로 여기자는 것이 그의 결론이다. 본인도 진단받은 병이 '
        '20개가 넘는다고 말한다.',
    ],
    'slim_stats': [('피부 · 소화관', '통증 알람이 제대로 울리는 곳'),
                   ('반음영 부위', '뇌경색에서 되살릴 수 있는 유일한 구간'),
                   ('2차성', '수십 년 쌓여 생기지만 관리하면 막히는 갈래'),
                   ('40대', '원래 인류의 건강수명이 끝나던 나이')],
    'clash': [
        ('개인 분류', '<b>여섯 갈래 분류는 학계 표준이 아니다.</b> 진료 경험으로 정리한 틀이라고 본인이 '
                   '밝혔다.'),
        ('추정', '<b>기존 연구는 변비를 대장암 위험 요인으로 보지 않는데, 그 결론을 반박한 것은 그의 추정이다.</b> 임상 설계가 '
                 '어렵고 말하기 부담스러운 결론이라 그럴 수 있다고 본 것이지 검증한 내용은 아니다.'),
    ],
}, {
    'section': SEC_WEIGHT,
    'topic': ('market', '체중 · 약'),
    'title': '이미 가진 살은 빼려 애쓰지 않는다. 영양제는 대부분 필요 없다',
    'gain': 'BMI 데이터가 뒤집힌 이야기, 이 말이 누구에게 하는 말인지, 그리고 영양제·스타틴·다이어트 약을 어떻게 볼지.',
    'meta': META_WEIGHT,
    'quote': '"찌지는 마시고 빼려고 노력은 하지 마시고 균형 있게 드시라. 그게 최고다."',
    'note': ('BMI 결과는 사망률 통계다. 특정 질환 위험이 낮다는 뜻이 아니고 살을 찌우라는 권고도 아니다. '
             '스타틴·위고비·펜터민은 모두 처방약이고, 기전과 부작용을 설명한 것이지 권한 것이 아니다.'),
    'links': LINKS_WEIGHT,
    'slim_oneliner': ('BMI 정상 구간은 1970년대 데이터로 정해졌다. 2000년대 이후 수백만 명을 모아 다시 보니 가장 '
                      '오래 사는 구간은 <b>25에서 30</b>이었다. 미국 기준으로 과체중, 한국 기준으로 비만에 해당하는 '
                      '구간이다.'),
    'slim_points': [
        '<b>한국 데이터도 같았다.</b> 대한비만학회가 낸 비만 팩트시트에서도 25~30 구간이 남녀 통틀어 가장 오래 '
        '사는 것으로 나왔다. 다만 홍보되지 못했다. 살을 빼라고 해야 하는 학회가 그 데이터를 말하면 살찌라는 '
        '이야기가 되기 때문이다.',

        '<b>60세 넘어 병을 겪었다면 빼려 애쓰지 않는다.</b> 자책하며 갑자기 열심히 재활하다 3개월 만에 사망한 '
        '환자 사례를 그는 든다. 찌우지도 말고 빼려 하지도 말고 저절로 빠지면 좋다고 여기라는 것이다.',

        '<b>운동도 선을 넘으면 해가 된다.</b> 뇌졸중 환자에게 권하는 최소선은 하루 7,000보다. 다만 그것만으로는 '
        '노인이 됐을 때 근육량을 유지하지 못해 50이 넘으면 무산소 운동도 신경 쓰는 편이 낫다.',

        '<b>선이 어디인지는 머리로 알 수 없다.</b> 넘으면 운동 중독으로 간다. 도파민이 나오기 때문이다. 마라톤이나 '
        '극단적인 무산소 운동은 성인 급사와 관련된 면이 있다.',

        '<b>사우나가 그 예다.</b> 핀란드 데이터에는 사우나가 건강에 좋다는 결과가 넘치는데, 일본에서는 한 해 '
        '목욕탕 사망자가 19,000명으로 교통사고보다 많다. 같은 행위가 어디서는 건강이고 어디서는 사망 원인이 된다.',

        '<b>영양제는 대부분 필요 없다.</b> 비타민 D는 야외 생활이 줄어 부족하기 쉬우니 먹고, 오메가3는 먹어도 '
        '괜찮다. 다만 생선과 해조류를 많이 먹는 한국인은 이미 충분한 편이다. 뇌졸중 예방에 쓰라는 영양제는 전 '
        '세계 어느 가이드라인에도 없다.',

        '<b>예외는 정상적인 식사를 못 하는 경우다.</b> 임산부는 엽산, 다이어터·만성질환자·암환자·노인은 종합 '
        '영양제가 낫다는 것이 그의 구분이다.',

        '<b>스타틴 부작용은 실제로 있다.</b> 이 약은 모든 세포의 콜레스테롤 합성을 억제하는데, 근육에서 '
        '콜레스테롤은 세포막을 보수하는 일을 한다. 보수가 안 되면 기능이 떨어지고 가장 먼저 밤에 쥐가 난다. '
        '의사가 이걸 부정하면서 신뢰가 무너졌다는 것이 그의 진단이다.',

        '<b>위고비와 마운자로는 기전이 낫다.</b> 배부를 때 나오는 포만 호르몬을 흉내 내 몸이 일주일 내내 '
        '배부르다고 착각하게 만든다. 부작용은 위장관 불편으로 인한 컨디션 저하가 가장 흔하고, 드물게 췌장염, '
        '무기력감이 온다.',

        '<b>나비약(펜터민)은 중독되기 쉽다.</b> 뇌에서 호랑이를 만난 상태를 만들어 컨디션은 좋아지고 식욕은 '
        '사라진다. 혈압과 맥박이 올라 장기 복용하면 고혈압을 만든다. BMI 30 이상에 한 달 이내 처방 조건인데 '
        '병원을 옮겨 다니며 받는 남용이 많다.',

        '<b>약으로 뺀 살은 끊으면 돌아온다.</b> 리바운드로 더 찔 수 있고, 빠르게 빠지는 만큼 근육도 많이 빠져 '
        '그 기간에는 단백질과 운동을 더 신경 써야 한다.',
    ],
    'slim_stats': [('25~30', '가장 오래 사는 BMI 구간'),
                   ('1970년대', '지금의 정상 구간을 정한 데이터의 시점'),
                   ('7,000보', '뇌졸중 환자에게 권하는 하루 걸음'),
                   ('19,000명', '일본의 연간 목욕탕 사망자. 교통사고보다 많다')],
    'clash': [
        ('오해 방지', '<b>살찌라는 이야기가 아니다.</b> 찌우지는 말라고 본인이 못 박았다. 이미 가진 살을 억지로 '
                   '빼려 하지 말라는 뜻이다.'),
        ('출처 없음', '<b>일본 목욕탕 사망자 19,000명은 그가 작년에 본 데이터라고 말한 값이다.</b> 출처는 '
                   '제시되지 않았다.'),
    ],
}, {
    'section': SEC_STAGE,
    'topic': ('market', '뇌출혈 · 동맥류'),
    'title': '뇌출혈은 뇌경색과 다른 병이다. 막을 수 있는 건 다음 출혈뿐이다',
    'gain': '동맥류가 왜 생기고 무엇이 터뜨리는지, 그리고 터진 뒤 치료가 무엇을 못 하는지.',
    'meta': META_BLEED,
    'quote': '"혈액은 뇌의 입장에서 혈관 안에선 좋지만 혈관 밖에서 독극 물질이다."',
    'note': ('언더스탠딩에 올라온 4시간짜리 모음집에서 뇌출혈 대목만 추렸다. 성공률과 비율은 그가 말한 값이고 '
             '출처 논문은 영상에서 제시되지 않았다.'),
    'links': LINKS_BLEED,
    'slim_oneliner': ('동맥경화는 벽 안쪽에 콜레스테롤이 쌓여 길이 좁아지는 병이다. <b>동맥류</b>는 다르다. 멀쩡한 '
                      '혈관 벽이 풍선처럼 바깥으로 부푼 혹이라 피는 그대로 흐르고 증상이 없다. 그러다 어느 날 '
                      '터진다.'),
    'slim_points': [
        '<b>지주막하출혈의 60~80%가 동맥류 파열이다.</b> 동맥류 없이 새는 출혈은 대개 가벼워서 크게 걱정할 일은 '
        '아니라는 것이 그의 정리다.',

        '<b>선천적으로 갖고 태어나는 경우는 5~15%다.</b> 나머지는 살면서 생긴다. 벽을 물리적으로 미는 고혈압과 '
        '화학적으로 손상시키는 담배가 약한 부분을 점점 키운다.',

        '<b>만드는 요인과 터뜨리는 요인이 다르다.</b> 고혈압과 담배가 만들고, 큰 혈압 변동이 터뜨린다. 과음, '
        '과격한 운동, 심리적 충격이 방아쇠다. 술은 마실 때 오르고 자는 동안 탈수로 떨어졌다가 다시 올라 하루 '
        '사이 폭을 키운다.',

        '<b>터지면 절반이 죽는다.</b> 그리고 30대에서 60대에 많이 생긴다. 한창 일할 나이다.',

        '<b>치료는 다음 출혈을 막는 것이다.</b> 코일 색전술로 혹 안을 금속으로 채워 피가 못 들어가게 하고, '
        '어려우면 머리를 열어 미세 클립으로 목을 집는다. 이미 퍼진 피를 어쩌지는 못한다.',

        '<b>그래서 뇌경색과 결과가 갈린다.</b> 뇌경색은 막힌 혈관을 열면 환자가 그 자리에서 좋아진다. '
        '지주막하출혈은 혼수 상태로 온 환자를 시술해도 상태가 그대로다.',

        '<b>혈관 밖으로 나온 피는 독이 된다.</b> 피에 잠긴 혈관이 자극을 받아 떨기만 하고 피를 밀어내지 못하는 '
        '연축이 온다. 출혈로 들어온 환자가 중환자실에서 뇌경색을 겹쳐 맞는 이유다.',

        '<b>손실의 대부분은 두 번째 물결이다.</b> 처음 크게 다친 세포는 손쓸 대상이 아니다. 오염된 자리를 치우려는 '
        '염증이 옆의 멀쩡한 세포까지 죽인다. 몸에는 적당히 죽이라는 명령이 없다.',

        '<b>뇌실질 출혈은 대개 내과적으로 다룬다.</b> 혈압을 낮춰 뿜어져 나오는 압력을 줄인다. 혈종을 뽑기도 '
        '하지만 음압이 걸려 출혈을 되레 조장하는 경우가 있어 심각하지 않으면 수술을 권하지 않는다.',
    ],
    'figs': [
        (1, '그림 10 · 같은 혈관, 다른 병',
         FIG_ANEURYSM,
         '왼쪽은 두 병의 단면 대비다. 동맥경화는 안쪽이 좁아지고 동맥류는 바깥으로 부푼다. 오른쪽은 터진 뒤로, '
         '붉게 퍼진 자리의 피를 씻어낼 방법이 없다는 것이 이 병의 핵심이다.'),
    ],
    'slim_stats': [('60~80%', '지주막하출혈 중 동맥류 파열이 차지하는 비율'),
                   ('5~15%', '동맥류를 선천적으로 갖고 태어나는 비율'),
                   ('절반', '터졌을 때 사망하는 비율'),
                   ('30~60대', '지주막하출혈이 많이 생기는 나이')],
    'clash': [
        ('본인 유보', '<b>고혈압과 담배로 원인을 좁힌 것은 단순화한 설명이다.</b> 강의 목적의 정리라고 본인이 '
                   '단서를 달았다.'),
        ('오해 방지', '<b>동맥류가 있다고 반드시 터지는 것은 아니다.</b> 있어도 터지지만 않으면 문제가 되지 '
                   '않는다는 것이 그의 설명이다.'),
    ],
}, {
    'section': SEC_GLP1,
    'topic': ('market', '기전 · 보상 회로'),
    'title': '덜 먹게 하는 약이 술과 담배까지 줄이는 이유',
    'gain': 'GLP-1이 붙는 자리가 장과 췌장만은 아니라는 사실, 그리고 갈망이 줄어드는 기전.',
    'meta': META_GLP1,
    'quote': '"중독된 뇌는 좋아함은 그대로인데 원함만 비정상적으로 커진다."',
    'note': ('처방이나 복용을 권하는 내용이 아니다. GLP-1 계열은 전문 진료 영역이다. 화자가 바뀌었다 — '
             '내분비대사내과 전문의이고, 앞선 카드들의 신경과 교수와 다른 사람이다.'),
    'links': LINKS_GLP1,
    'slim_oneliner': ('GLP-1은 음식이 장에 닿으면 장 내분비 세포가 내보내는 호르몬이다. 탄수화물만 그런 것이 '
                      '아니고 지방과 단백질이 소화될 때도 올라간다. 인슐린을 늘리고, 위에서 십이지장으로 넘어가는 '
                      '속도를 늦추고, 뇌에 그만 먹으라고 알린다. 그런데 이 호르몬이 붙는 수용체가 뇌에서 '
                      '<b>원함</b>을 만드는 자리에도 있다. 그래서 줄어드는 것이 식욕만으로 끝나지 않는다.'),
    'slim_points': [
        '<b>중독이라는 말부터 갈린다.</b> 식중독처럼 독이 들어온 상태와, 끊지 못하는 상태는 영어로 다른 단어다. '
        '뒤쪽을 학술 용어로 물질사용장애라 부르고, 이 섹션이 다루는 것도 그쪽이다.',

        '<b>중독된 뇌는 좋아함은 그대로인데 원함만 커진다.</b> 예전엔 조금만 해도 좋았는데 점점 더 많이, 더 '
        '세게 원해야 같은 만족이 온다. 돈을 버는 것도 같은 구조라는 것이 그의 예시다.',

        '<b>원함을 만드는 회로에 수용체가 있다.</b> 중뇌 복측피개영역에서 측좌핵으로 가는 길인데, 측좌핵에도 '
        'GLP-1 수용체가 있다는 것이 확인됐다. 고농도에서는 쾌락과 관련된 회로를 오히려 억누른다.',

        '<b>말초 신경에도 수용체가 있다.</b> 위고비 용량을 표준 2.4mg에서 7.2mg까지 올린 임상에서 체중은 더 '
        '빠졌지만 저릿한 이상 감각이 새로 나타났다. 고농도에서 말초 신경의 수용체까지 자극된 결과로 본다.',

        '<b>푸드 노이즈라는 말이 여기서 나왔다.</b> 배고프지 않은데 하루 종일 음식 생각이 떠도는 상태를 '
        '가리킨다. 주사를 맞은 환자들이 그 생각이 사라졌다고 말하면서 미국에서 퍼졌다.',

        '<b>저혈당은 생기지 않는다.</b> 이 호르몬은 혈당이 이미 높을 때만 인슐린 분비를 밀어 준다. 엔진이 돌 때 '
        '출력을 올리는 터보차저와 같아서, 꺼져 있으면 아무 일도 하지 않는다.',

        '<b>체중이 줄어서 생기는 몫도 섞여 있다.</b> 100kg에서 80kg이 되면 알코올이 퍼질 몸속 수분이 20리터쯤 '
        '줄어 같은 술에도 더 빨리 취한다. 그래서 덜 마시게 되는 부분이 따로 있다.',

        '<b>원래는 당뇨약이었다.</b> 식욕이 줄고 포만감이 커지는 것이 부작용으로 발견돼 비만약이 됐다. 위고비는 '
        '평균 15%, 마운자로는 20% 체중을 줄이고, 개발 중인 다음 세대는 25~30%를 목표로 한다.',
    ],
    'figs': [
        (3, '그림 11 · 포만 신호가 보상 회로에도 닿는다',
         FIG_GLP1,
         '장에서 나온 호르몬이 인슐린과 포만감만 건드리는 것으로 끝나지 않는다. 뇌에서 원함을 만드는 자리에도 '
         '수용체가 있어 갈망 자체가 줄어든다.'),
    ],
    'slim_stats': [('측좌핵', 'GLP-1 수용체가 발견된 보상 회로의 도착지'),
                   ('15% · 20%', '위고비와 마운자로의 평균 체중 감량'),
                   ('2.4 → 7.2mg', '용량을 올렸을 때 말초 신경 증상이 나타난 지점'),
                   ('20리터', '100kg에서 80kg이 될 때 줄어드는 체내 수분')],
}, {
    'section': SEC_GLP1,
    'topic': ('market', '근거 · 임상'),
    'title': '근거는 관찰에서 임상으로 막 넘어왔다',
    'gain': '어디까지가 확인된 숫자이고 어디부터가 아직 모르는 영역인지.',
    'meta': META_GLP1,
    'quote': '"기전이 서로 다른 다섯 가지 물질이 동시에 줄었다."',
    'note': ('숫자는 모두 영상에서 그가 인용한 값이다. 관찰 연구와 무작위 임상은 근거의 층이 다르므로 카드 안에서 '
             '구분해 적었다.'),
    'links': LINKS_GLP1,
    'slim_oneliner': ('가장 큰 자료는 미국 재향군인 <b>60만 명</b> 관찰 연구다. 기전이 서로 다른 다섯 물질이 '
                      '동시에 줄었다. 그다음 단계인 무작위 임상은 이제 <b>108명</b> 규모로 하나 나왔다.'),
    'slim_points': [
        '<b>다섯 가지가 함께 줄었다.</b> 오피오이드 25%, 코카인 20%, 니코틴 20%다. 알코올은 18%, 대마는 14% '
        '줄었다. 기전이 다른 물질이 같이 줄었다는 점을 연구자들은 공통 회로의 증거로 봤다.',

        '<b>물질 관련 사망이 50% 줄었다.</b> 기존에 물질사용장애가 있던 사람들의 응급실행도 줄었다. 다만 관찰 '
        '연구라 인과까지 단정할 수 없다.',

        '<b>그래서 무작위 임상이 뒤따랐다.</b> 비만하면서 술을 많이 마셔 온 108명을 절반씩 나눠 위고비와 위약을 '
        '줬다. 가짜 약임을 눈치채지 못하도록 주사 소리까지 관리했다.',

        '<b>과음 일수가 41%와 26%로 갈렸다.</b> 위약 쪽 감소가 큰 것은 참가자들이 애초에 끊고 싶어 자원한 '
        '사람들이었기 때문이라고 그는 본다. 한 번에 마시는 양과 한 달 음주량, 간 수치도 함께 좋아졌다.',

        '<b>기존 중독 치료제와 비교하면 반응이 낫다.</b> 기존 약이 일곱 명에 한 명 수준이라면 이쪽은 네 명에 한 '
        '명 수준이라는 것이 그의 평가다. 다만 알코올 사용장애와 비만을 함께 가진 환자군에서 나온 값이다.',

        '<b>대상이 좁다는 점을 그가 먼저 말한다.</b> 비만하고, 술을 많이 마시고, 스스로 끊고 싶어 온 유럽인이 '
        '참가자였다. 비만하지 않은 사람이나 끊을 생각이 없는 사람, 한국인에게도 같을지는 확인되지 않았다.',

        '<b>도박이나 투자 같은 행위 중독은 근거가 없다.</b> 대화에서 추정을 나눴을 뿐 임상 자료는 제시되지 '
        '않았다.',

        '<b>천연 위고비라는 말에는 선을 긋는다.</b> 메트포민을 먹으면 체내 GLP-1이 잠깐 두 배로 오르지만 식후 '
        '잠시일 뿐이라, 일주일 내내 농도를 유지하는 주사와 견줄 수 없다. 한국에서는 계란, 미국에서는 젤라틴을 '
        '그렇게 부르는데 공통점은 탄수화물이 없다는 것이다. 지방과 단백질이 소화될 때도 GLP-1이 오르기 '
        '때문인데, 그 상승은 잠깐이다.',
    ],
    'slim_stats': [('60만 명', '관찰 연구 규모. 근거의 크기는 여기서 나온다'),
                   ('50%', '같은 연구에서 줄어든 물질 관련 사망'),
                   ('41% vs 26%', '임상에서 위고비군과 위약군의 과음 일수 감소'),
                   ('108명', '그 임상의 규모. 아직 작다')],
    'clash': [
        ('층위 구분', '<b>60만 명 자료는 관찰 연구이고 108명 자료가 무작위 임상이다.</b> 앞의 숫자가 크다고 '
                   '근거가 더 센 것은 아니다.'),
        ('대상 한정', '<b>임상 결과를 일반 인구에 그대로 옮길 수 없다.</b> 참가자 조건이 좁다는 점을 그가 직접 '
                   '짚는다.'),
    ],
}, {
    'section': SEC_GLP1,
    'topic': ('market', '오남용 · 파장'),
    'title': '미국은 이미 대실험 중이고, 짝퉁 약이 같이 돈다',
    'gain': '허가 범위 밖 사용이 어디까지 갔는지, 부작용은 무엇이고 산업에는 무엇이 걸려 있는지.',
    'meta': META_GLP1,
    'quote': '"일반적으로 무해하다고 판정하기는 매우 어렵다."',
    'note': ('오프라벨 사용과 비인가 조재약은 영상에서 위험으로 지목된 내용이다. 이 카드는 소개보다 경고 '
             '쪽에 무게가 있다.'),
    'links': LINKS_GLP1,
    'slim_oneliner': ('뉴욕타임즈가 「미국인의 GLP 대실험」이라는 제목으로 다룰 만큼 허가 범위 밖 사용이 퍼졌다. '
                      '뇌손상 후유증, 롱코비드, 장수 목적의 <b>마이크로도징</b>까지 번졌고, 그 옆에서 짝퉁 약이 '
                      '함께 돈다.'),
    'slim_points': [
        '<b>짝퉁 약이 실제 위험이다.</b> 정식 시설이 아닌 곳에서 합성한 약이 돌고 수입품도 섞인다. 영국에서는 '
        'GLP-1이라며 판 약에서 인슐린이 나온 사례가 보도됐다. 순도와 성분이 통제되지 않는다는 것이 핵심이다.',

        '<b>가장 흔한 부작용은 구역과 구토다.</b> 그로 인한 탈수가 응급실을 찾는 흔한 이유이고, 심하면 급성 '
        '신손상까지 간다.',

        '<b>이미 마른 사람이 계속 맞는 경우가 문제다.</b> 스스로 뚱뚱하다고 느껴 굶으며 주사를 이어 가면 영양 '
        '결핍이 온다. 비타민 B1이 모자라 신경 증상까지 생긴 사례를 그가 봤다고 말한다. 섭식장애가 있던 사람에게는 '
        '병을 키운다.',

        '<b>췌장염 우려는 최근 데이터로 가라앉았다.</b> 임상에서 통계적으로 유의하지 않았고, 오히려 비만 자체가 '
        '급성 췌장염의 큰 위험 요인이라는 쪽이다. 이 약의 시작이 도마뱀 독에서 뽑은 성분이라 초기부터 의심을 '
        '받았던 대목이다.',

        '<b>암 전이가 줄었다는 관찰 결과가 나왔다.</b> 올해 미국임상종양학회에서 대형 병원 세 곳이 발표했고, '
        'GLP-1 수용체를 많이 만드는 암일수록 전이가 줄어드는 정도가 컸다. 연관성까지만 나왔고 기전은 가설이다.',

        '<b>당뇨약으로서의 위상도 올라갔다.</b> 먹는 약으로 조절되지 않아 주사가 필요한 시점에는 인슐린보다 이쪽을 '
        '먼저 권한다. 심혈관 질환이나 만성 콩팥병이 있으면 더 그렇다.',

        '<b>이름도 바뀌는 중이다.</b> 혈당만 낮추는 약에서 콩팥과 심혈관까지 지키는 약으로 확인되면서 부르는 말이 '
        '달라졌고, 비만약도 식욕 억제제에서 체중 감량제를 거쳐 항비만제로 옮겨 갔다.',

        '<b>경제 추산까지 나왔다.</b> 골드만삭스 수석 이코노미스트는 미국 비만 인구 6천만 명이 투약하면 노동 '
        '생산성 손실 3%가 해소돼 GDP가 1% 더 자랄 수 있다고 봤다. 약 540조 원 규모라는 계산이다.',

        '<b>국내 수요도 작지 않다.</b> 알코올 사용장애 평생 유병률이 11.6%로 아홉 명 중 한 명이다. 19~29세의 '
        '스마트폰 과사용 경험률은 19.9%이고, 알코올 관련 사망은 전체 사망의 5%(남성은 7%)를 차지한다.',
    ],
    'slim_stats': [('6천만 명 · 1%', '골드만삭스가 가정한 투약 인구와 GDP 추가 성장'),
                   ('540조 원', '그 추산의 경제 가치'),
                   ('11.6%', '국내 알코올 사용장애 평생 유병률'),
                   ('5% (남 7%)', '전체 사망 중 알코올 관련 비율')],
    'clash': [
        ('오해 방지', '<b>오프라벨 사용을 소개한 대목은 권장이 아니다.</b> 기사도 시도와 우려를 함께 다뤘다고 '
                   '그가 짚는다.'),
        ('가설', '<b>암 전이 지연은 관찰 단계다.</b> 실제 기전과 인과는 앞으로 검증해야 한다고 못 박았다.'),
        ('출처', '<b>경제 추산은 인용된 보고서의 숫자다.</b> 가정과 방법론은 영상에서 다뤄지지 않았다.'),
    ],
}, {
    'section': SEC_WEIGHT,
    'topic': ('market', '약 · 신약'),
    'title': '먹는 약은 900달톤을 넘지 못한다',
    'gain': '소화의 경계선 하나가 왜 신약 개발사 전체를 설명하는지.',
    'meta': META_DRUG,
    'quote': '"세상에 약과 독은 없다. 용량이 결정한다."',
    'note': ('3부작 모음집의 2·3부에서 추렸다. 영상 후반에 화자가 개발 주체인 임상 1상 물질 이야기가 나오지만, '
             '이해관계가 있고 승인 전 약이라 이 카드에는 싣지 않았다.'),
    'links': LINKS_DRUG,
    'slim_oneliner': ('몸은 분자량 <b>900달톤</b>을 넘는 물질을 그대로 들이지 않는다. 소화란 고분자를 그 아래로 '
                      '쪼개 장벽을 통과시키는 일이고, 먹는 약이 작아야 하는 이유도 같다. 이 경계 하나가 신약의 '
                      '역사를 갈랐다.'),
    'slim_points': [
        '<b>밥과 고기는 원래 맛이 없다.</b> 우리가 맛있다고 느끼는 것은 조리와 숙성으로 이미 쪼개져 나온 '
        '포도당과 글루탐산과 지방산이다. 요리는 고분자 음식을 저분자처럼 느끼게 만드는 과정인 셈이다.',

        '<b>알코올은 인류 최초의 약에 가깝다.</b> 작고, 물에도 기름에도 녹는 드문 물질이라 몸의 방어를 거치지 '
        '않고 그대로 통과한다. 빈속에 술을 마시면 10분 안에 뇌에 닿는다.',

        '<b>신장은 일단 다 버리고 필요한 것만 되찾는다.</b> 사구체가 5나노미터 아래를 기계적으로 걸러내고, '
        '포도당처럼 아는 물질만 되흡수한다. 몸이 모르는 약은 대개 그대로 소변으로 나간다.',

        '<b>간은 낯선 물질에 화학기를 붙여 물에 녹게 만든다.</b> 그래야 신장이 버릴 수 있다. 이 과정에서 약효도 '
        '대부분 사라진다. 처리 속도를 넘겨 혹사하면 간세포가 집단으로 죽는다. 술과 함께 먹지 말라는 약이 있는 '
        '이유다.',

        '<b>복용 간격은 그 처리 속도가 정한다.</b> 하루 세 번이냐 한 번이냐는 간과 신장이 다 치우는 데 걸리는 '
        '시간에서 나온다.',

        '<b>약과 독을 가르는 것은 용량이다.</b> 약효가 나기 시작하는 지점과 독성이 나타나는 지점 사이의 좁은 '
        '창을 찾는 학문이 약동학이다. 필로폰이 약으로 남지 못한 것도 그 창이 지나치게 좁아서다.',

        '<b>먹는 약 대다수가 900달톤 이하로 설계된 저분자다.</b> 문제는 이런 약효가 있을 것이라 설계해도 대개 '
        '안 듣는다는 점이다. 그래서 후보 물질을 1천 개쯤 만들어 걸러낸다.',

        '<b>그래서 단백질을 통째로 주사하는 쪽이 열렸다.</b> 인슐린이 첫 사례다. 인슐린을 먹으면 아미노산으로 '
        '분해되니 주사밖에 길이 없었다.',

        '<b>1990년대에 항체를 만들어 주사하기 시작했다.</b> 류마티스관절염에서 염증을 퍼뜨리는 단백질을 잡는 '
        '항체가 나왔고, 표적 하나만 잡도록 똑같이 찍어내는 이 약을 단클론항체라 부른다. 2000년대 이후 신약의 '
        '대부분이 여기 속한다.',

        '<b>다음은 RNA였다.</b> 단백질을 만들라는 전령을 방해해 공장을 끄는 방식이 RNA 간섭이고, 코로나 백신은 '
        '반대로 없던 단백질을 만들라는 전령을 넣었다. 잘 분해되는 RNA를 지질 껍질로 감싸 해결했다.',

        '<b>먹는 GLP-1은 두 갈래로 풀렸다.</b> 한쪽은 흡수를 돕는 꼬리를 붙여 1%만 흡수되게 하고 그만큼 용량을 '
        '100배 올렸고, 다른 쪽은 아예 저분자 화학물질로 같은 수용체를 자극하는 약을 만들었다.',

        '<b>못 넘는다던 벽도 예외가 나왔다.</b> 뇌혈관 관문은 포도당과 산소 정도만 통과시켜 분자량 10만이 넘는 '
        '항체는 못 들어간다고 봤는데, 알츠하이머 항체 치료제는 극미량만 새어 들어가고도 효과를 낸다. 나이 든 '
        '관문에 이미 틈이 있고 항체가 워낙 강력해서라는 것이 그의 설명이다.',
    ],
    'slim_stats': [('900달톤', '그대로 흡수되는 물질 크기의 경계선'),
                   ('5나노미터', '신장이 일단 걸러내는 크기'),
                   ('1천 개', '저분자 신약에서 걸러 보는 후보 물질 규모'),
                   ('1% · 100배', '먹는 GLP-1의 흡수율과 그만큼 올린 용량')],
    'clash': [
        ('이해관계', '<b>영상 후반의 신약 이야기는 화자가 개발 주체다.</b> 임상 1상이고 승인 전이라 이 카드에 '
                   '싣지 않았다.'),
        ('용어 주의', '<b>900달톤은 대략적인 경계다.</b> 물질의 성질에 따라 달라지는 기준선이지 딱 떨어지는 '
                   '문턱이 아니다.'),
    ],
}, {
    'section': SEC_BRAIN,
    'topic': ('market', '뇌 · 수면'),
    'title': '뇌는 깊은 잠에서만 씻긴다',
    'gain': '치매를 미리 아는 방법이 왜 없는지, 그리고 잠에서 확보해야 할 게 무엇인지.',
    'meta': META_EP155,
    'quote': '"깊은 잠에 들었구나 하고 문을 살짝 열고 들어가서 뇌를 쫙 씻고 나오는데"',
    'note': '그의 전공이 뇌졸중이다. 뇌졸중 이야기는 04 섹션의 두 카드에서 이어진다.',
    'links': LINKS_EP155,
    'slim_oneliner': ('"옆으로 누워 자면 뇌의 해로운 물질이 빠져나간다"는 말에 그는 근거가 없다고 답한다. 중요한 '
                      '것은 자세가 아니고 <b>수면 단계</b>다. 뇌를 씻는 글림프 시스템은 3·4단계에서만 돌고, 중간에 '
                      '깨서 사이클이 끊기면 그 구간이 통째로 사라진다.'),
    'slim_points': [
        '<b>뇌는 깨어 있을 때 청소하지 않는다.</b> 일하는 중에 청소를 안 하는 것과 같다. 아주 깊이 잠들면 '
        '뇌척수액이 들어와 뇌를 훑고 나가는데, 이것이 글림프 시스템이다.',

        '<b>씻어내는 것은 활동의 부산물이다.</b> 뇌가 ATP를 쓰며 남긴 물질을 쓸어낸다. 잘 자고 나면 머리가 '
        '맑아지는데, 실제로 맑아진 것이다.',

        '<b>청소부는 3·4단계에만 들어온다.</b> 잠은 1·2·3·4단계로 깊어졌다가 렘수면에서 깬 것처럼 꿈을 꾸고, 이 '
        '사이클을 하룻밤 네댓 번 돈다. 1·2단계에서는 청소가 일어나지 않는다.',

        '<b>치매 유발 물질도 그때 씻겨 나갈 것이라는 가설이 지금 많다.</b> 잠이 좋은 사람이 치매에 덜 걸릴 것이라는 '
        '예상으로 임상 연구가 시작됐고, 글림프 시스템을 활성화하려는 시도도 여러 방향으로 나오고 있다.',

        '<b>치매는 본인이 알아채기 어렵다.</b> 스스로 걱정해서 오면 대개 건망증이고, 배우자가 데려오는 쪽이 '
        '가능성이 높다. 아침을 차려줬는데 또 차려 달라고 하는 식으로 주변이 먼저 안다.',

        '<b>조기 진단 방법은 사실상 없다.</b> MRI는 뇌가 쭈그러들었는지 같은 형태와 구조를 보는 검사라 단백질 '
        '활성도는 못 본다. 명백한 것은 아밀로이드 PET 하나인데, 쌓였다고 반드시 치매 전 단계도 아니고 없다고 안 '
        '생기는 것도 아니다.',

        '<b>그가 지키는 습관은 셋이다.</b> 7시간 30분 안팎을 깨지 않고 자고(본인은 9시 반에 자서 3~4시에 '
        '일어난다), 집에서 혈압을 자주 재고, 스스로 정한 체중과 허리둘레를 지킨다.',
    ],
    'figs': [
        (4, '그림 12 · 뇌 시상단면과 수면 곡선',
         FIG_SLEEP,
         '뇌척수액이 뇌를 훑고 나가는 청소는 수면 3·4단계에서만 일어난다. 1·2단계에서는 청소부가 들어오지 않으니, '
         '하룻밤 네댓 번 도는 사이클이 중간에 깨지면 깊은 구간이 통째로 사라진다.'),
    ],
    'slim_stats': [('3 · 4단계', '뇌 청소가 도는 수면 깊이'),
                   ('4~5회', '하룻밤에 도는 수면 사이클 횟수'),
                   ('7시간 30분', '그가 말한 가장 좋은 수면. 깨지 않고 자는 것'),
                   ('아밀로이드 PET', '치매를 명백히 볼 수 있는 유일한 검사. 그래도 확정은 아니다')],
    'clash': [
        ('가설', '<b>글림프 시스템과 치매의 연결은 아직 증명되지 않았다.</b> 증명된 단계냐는 물음에 그는 지금은 '
                 '많은 연구자가 그럴 것이라 믿는 단계라고 답했다.'),
        ('근거 없음', '<b>"옆으로 누워 자면 치매에 덜 걸린다"는 말에는 근거가 없다.</b> 대본에서 처음 봤고 조사해 '
                   '봐도 쓸데없는 소리라는 것이 그의 답이다.'),
    ],
}, {
    'section': SEC_BRAIN,
    'topic': ('market', '도파민 · 마음'),
    'title': '도파민은 쾌락이 아니라 희망의 물질이다',
    'gain': '도파민이 언제 나오고 어디로 뿌려지는지, 그리고 방향을 잡아 주는 것이 무엇인지.',
    'meta': META_DOPA,
    'quote': '"추구와 희망의 물질이야. 쾌락의 물질이 아니고."',
    'note': ('낭만과 도파민을 잇는 해석은 그의 강의용 정리이고 학술 정설은 아니라고 본인이 밝혔다. 약 이야기는 '
             '모두 처방 영역이며 기전과 부작용을 설명한 것이다.'),
    'links': LINKS_DOPA,
    'slim_oneliner': ('도파민은 이미 받은 즐거움에서 나오지 않는다. <b>올 것 같은 보상</b>에서 나온다. 그래서 몇 년이 걸리는 '
                      '일도 그 방향으로 계속하게 만든다. 여행은 가기 전 준비할 때가 가장 좋은 것과 같다.'),
    'slim_points': [
        '<b>뇌의 물질은 두 갈래다.</b> 신경 전달 물질은 옆 신경 하나를 켜고 끈다. 켜는 쪽이 글루탐산, 끄는 쪽이 '
        '가바다. 신경 조절 물질은 구역 전체에 뿌려 분위기를 정한다.',

        '<b>이메일로 치면 본문과 행간이다.</b> 용건만 적힌 메일이 오해를 사듯, 켜고 끄는 신호만으로는 분위기가 '
        '전해지지 않는다. 도파민은 "이거 대박이다", 노르에피네프린은 "지금 위험하다", 세로토닌은 "흥분하지 마라"에 '
        '가깝다.',

        '<b>도파민이 나오는 순간은 둘이다.</b> 예상보다 큰 보상이 왔을 때, 그리고 목표를 세우고 될 것 같다고 '
        '느낄 때. 뒤쪽이 본체다.',

        '<b>그래서 중독이 붙는다.</b> 예상 밖의 보상이 한 번 오면 한 번 더가 따라온다. 카지노에서 처음 터뜨린 '
        '사람이 가진 돈을 다 미는 이유다.',

        '<b>뿌려지는 곳이 셋이고, 성격이 다른 갈래가 하나 더 있다.</b> 선조체는 몸이 외운 동작을 돌리고, '
        '변연계는 마음을 흥분시키고, 전두엽은 계속할 이유를 만든다. 시상하부에서 뇌하수체로 가는 갈래는 젖 분비를 '
        '멈추게 한다.',

        '<b>선조체 회로가 끊기면 파킨슨병이다.</b> 흑질의 도파민 세포가 남보다 빨리 노화해 죽는다. 자전거 타기나 '
        '걷기처럼 외워 둔 동작이 안 돌아가 걸음을 시작하지 못하고 얼어붙는다.',

        '<b>부족하면 우울증·파킨슨병·ADHD, 넘치면 조현병과 조증이다.</b> 깊은 우울증에서는 표정이 사라진다. '
        '정보는 들어오는데 의미가 붙지 않는다.',

        '<b>조증은 즐거워서 벌이는 게 아니다. 다 될 것 같아서 벌인다.</b> 하루에도 사업을 여러 개 시작한다. 필로폰 계열이 '
        '만드는 상태도 쾌락보다 과잉된 자신감에 가깝고, 쾌락 쪽은 오히려 엔돌핀 계열이다.',

        '<b>ADHD는 전두엽으로 가는 도파민이 모자란 쪽이다.</b> 일할 동기가 부족해 집중이 안 된다. 재흡수를 '
        '막는 약을 주면 빠르게 좋아지지만 국내에서 그 약을 줄 수 있는 진단은 사실상 ADHD뿐이다.',

        '<b>방향을 잡아 주는 것은 세로토닌이다.</b> 이 정도면 괜찮다고 느끼게 하는 물질이다. 도파민만 넘치면 '
        '질투와 상대적 박탈감처럼 엉뚱한 곳으로 힘을 쓰고, 세로토닌만 넘치면 도전하지 않는다.',

        '<b>우울증도 갈래가 둘이다.</b> 도파민이 떨어진 쪽과 세로토닌이 떨어진 쪽인데, 후자가 주종이라 보고 '
        '세로토닌을 올리는 약을 기본으로 쓴다.',

        '<b>약은 가볍게 볼 것이 아니다.</b> 효과가 나기까지 두 달쯤 걸리는데 부작용은 먼저 온다. 40%는 오히려 '
        '의욕이 떨어진다. 그는 호기심에 직접 먹어 보고 며칠 만에 그만뒀다고 말한다.',

        '<b>혈액 검사로는 알 수 없다.</b> 뇌 안에서만 변하기 때문에 행동으로 추정한다. 그래서 오진이 많다는 것이 '
        '그의 설명이다.',
    ],
    'figs': [
        (5, '그림 13 · 도파민이 뿌려지는 네 곳',
         FIG_DOPAMINE,
         '중뇌에서 출발해 선조체와 변연계와 전두엽으로 간다. 몸이 외운 동작, 마음, 그리고 계속할 이유가 각각 '
         '거기서 만들어진다.'),
    ],
    'slim_stats': [('두 순간', '예상보다 큰 보상, 그리고 될 것 같은 목표'),
                   ('860억 · 100조', '뇌의 신경 세포 수와 시냅스 수'),
                   ('두 달', '세로토닌 약의 효과가 나타나기까지'),
                   ('40%', '그 약을 먹고 오히려 의욕이 떨어지는 비율')],
    'clash': [
        ('강의용 정리', '<b>낭만과 도파민을 잇는 해석은 학술 정설이 아니다.</b> 본인이 개인적인 틀이라고 '
                     '밝혔다.'),
        ('경험 근거', '<b>차분한 사람이 파킨슨병에 잘 걸린다는 관찰도 진료 경험에 근거한 설명이다.</b> 통계로 '
                   '제시된 것은 아니다.'),
    ],
}]


HEADER = '''  <header>
    <p class="eyebrow">건강 — 제3자 해설 아카이브</p>
    <h1>건강 인사이트</h1>
    <div class="meta-row">
      <span>정리일 <b>%s</b></span>
      <span>카드 <b>%d장</b></span>
      <span>출처 <b>9편</b></span>
      <span>소스 <b>지식인사이드 · 언더스탠딩</b></span>
    </div>
  </header>''' % (STAMP, len(CARDS))

# 페이지 설명은 맨 밑이다. 첫 화면은 어느 장이든 섹션 타일이라(CLAUDE.md), 설명 여섯 줄이
# 그 위에 서면 타일이 화면 밖으로 밀린다. 읽는 순서 안내(「처음 오셨다면」)만 위에 남긴다.
LEDE = '''<p class="lede">채널을 가리지 않고 <b>몸에서 실제로 벌어지는 일</b>만 모읍니다. 카드는 주제로
       묶습니다. 한 영상에서 여러 이야기가 나오면 나눠 싣고, 다른 영상이 같은 이야기를 하면 그 카드를 보강합니다.
       말로만 지나가면 안 남는 대목에는 해부도를 함께 그렸습니다. 진단이나 처방이 아닙니다.</p>'''

FOOTER = (LEDE + '\n제3자 해설 아카이브 · 유튜브 요약은 자막 전문 기반입니다. 의학적 진단·처방이 아니며 판단은 의료진과 합니다.\n'
          '  요약은 <code>content/health/</code>, '
          '페이지 생성은 <code>scratchpad/gen_health_dashboard.py</code>(공용 부품 <code>dash_common.py</code>).')

# 한 영상이 여러 카드로 갈릴 때 「어느 순서로 읽는가」를 카드 안에서 잇는다. 이 페이지는 카드
# 단위가 영상이 아니라 주제라, 3부작 한 편이 섹션 넷 떨어진 자리에 흩어진다. 링크가 없으면
# 화면에서는 같은 영상인지 알 길이 없다.
VID = {
    SRC_EP155: ('지식인사이드 EP.155', '2026-08-01'),
    SRC_EP156: ('지식인사이드 EP.156', '2026-08-02'),
    SRC_EP107: ('지식인사이드 EP.107', '2026-03-09'),
    SRC_EP108: ('지식인사이드 EP.108', '2026-03-10'),
    SRC_LEGEND: ('언더스탠딩 레전드 모음집', '2024-09-18'),
    SRC_NOBEL: ('언더스탠딩 노벨생리의학상 해설', '2025-10-27'),
    SRC_DOPA: ('언더스탠딩 도파민', '2026-07-12'),
    SRC_GLP1: ('언더스탠딩 비만약과 중독', '2026-07-20'),
    SRC_3PART: ('언더스탠딩 3부작 (질병·소화·신약)', '2025-10-07'),
}


def attach_kin(cards):
    """카드마다 c['kin']을 채운다 — [(영상 이름, [(제목, 앵커 또는 None)])].

    앵커가 None인 항목이 그 카드 자신이다. 순서는 CARDS에 적힌 순서 그대로다(섹션이 몸에서
    벌어지는 순서라 그게 곧 읽는 순서다). 한 영상이 카드 하나만 받쳤으면 붙이지 않는다."""
    def videos(c):
        return [u for lab, u, _cls in c['links'] if lab.startswith('영상')]

    by = {}
    for c in cards:
        for u in videos(c):
            assert u in VID, '영상 이름이 VID에 없다: %s' % u
            by.setdefault(u, []).append(c)

    for c in cards:
        kin = []
        for u in videos(c):
            group = by[u]
            if len(group) < 2:
                continue
            name, date = VID[u]
            kin.append(('%s · %s' % (name, date),
                        [(g['title'], None if g is c else dc.slug(g['title'])) for g in group]))
        if kin:
            c['kin'] = kin


# 읽는 순서는 섹션 순서와 다르다. 섹션은 염증부터 시작하지만 처음 읽는 사람에게는 오늘
# 저녁 식탁 이야기가 먼저다. 조립과 검사는 dash_common.course()가 한다.
COURSE_LEDE = ('카드 %d장을 어디서부터 읽을지 정해 두었습니다. 앞 두 단계는 오늘 저녁 식탁에서 바로 쓰는 '
               '이야기고, 뒤로 갈수록 몸속에서 벌어지는 일로 들어갑니다. 제목을 누르면 그 카드가 열립니다.')

COURSE = [
    ('오늘 저녁부터',
     '무엇을 뺄지 고르기 전에 얼마나 먹는지부터 본다. 밥과 과일과 단백질 순으로 읽는다.',
     ['밥·빵 종류가 문제가 아니라 얼마나 많이 먹느냐가 문제다',
      '같은 열량이면 과일이 밀가루보다 나쁘다. 과당은 간만 받는다',
      '단백질은 노인이 더 먹어야 하는데 우리나라는 거꾸로 간다']),
    ('몸무게와 잠',
     '둘 다 병이 생기기 전에 손댈 수 있는 자리다. 체중은 쌓아 두는 쪽이고 잠은 씻어 내는 쪽이다.',
     ['이미 가진 살은 빼려 애쓰지 않는다. 영양제는 대부분 필요 없다',
      '뇌는 깊은 잠에서만 씻긴다']),
    ('왜 그렇게 되는가',
     '앞 다섯 장의 이유가 여기 있다. 과잉 칼로리에서 만성 염증으로, 지방산에서 당뇨로 이어지는 경로다.',
     ['염증은 나쁜 게 아니다. 과하게 먹는 것이 만성 염증을 만든다',
      '당뇨는 포도당이 넘쳐서 생기는 병이 아니다. 지방산이 신호를 막는다']),
    ('내가 몇 단계인지 알기',
     '검사 숫자로 자기 위치를 읽는 법이다. 손상됐는데 못 느끼는 경우가 흔해서 신호를 가리는 법을 같이 둔다.',
     ['의사를 만나기 전에 내가 몇 단계인지 안다',
      '통증은 믿을 만한 알람이 아니다',
      '전조증상은 하나뿐이다. 그리고 시간이 곧 치료다',
      '뇌출혈은 뇌경색과 다른 병이다. 막을 수 있는 건 다음 출혈뿐이다']),
    ('약은 어디까지 왔나',
     '먹는 약이 왜 작아야 하는지에서 시작해, 비만약이 술과 담배까지 줄인다는 임상까지 간다.',
     ['먹는 약은 900달톤을 넘지 못한다',
      '덜 먹게 하는 약이 술과 담배까지 줄이는 이유',
      '근거는 관찰에서 임상으로 막 넘어왔다',
      '미국은 이미 대실험 중이고, 짝퉁 약이 같이 돈다']),
    ('더 깊이',
     '2025년 노벨생리의학상 해설과 뇌 이야기다. 앞을 읽고 오면 훨씬 잘 붙는다.',
     ['면역을 말리는 세포가 있다. 암이 그 세포를 구슬린다',
      '도파민은 쾌락이 아니라 희망의 물질이다']),
]

if __name__ == '__main__':
    attach_kin(CARDS)
    dc.render(CARDS, '건강 인사이트', HEADER, FOOTER, OUT,
              rollup=dc.rollup_for('health', CARDS, '편'),
              intro=dc.course(CARDS, COURSE, COURSE_LEDE), extra_css=dc.COURSE_CSS)
