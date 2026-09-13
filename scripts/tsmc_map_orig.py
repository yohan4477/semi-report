# -*- coding: utf-8 -*-
u"""TSMC 그림 장의 원문 1절 — 손으로 그린 전체 지도(2026-09-13 사용자가 준 그대로).

탐색기 절은 이것을 대신하지 않고 뒤에 더한다 — 「보고서 꼴에 밸류체인을 추가로 보여 준다」.
gen_vcreport.py 가 읽는다.
"""

SECTION_1_ORIG = u'''  <!-- 1. 전체 지도 -->
  <section>
    <h2>1. 전체 지도<small>앞단 → TSMC → 뒷단</small></h2>
    <p class="note">굵은 선이 돈이 가장 많이 흐르는 경로. 색은 소속: 청록 TSMC, 주황 한국 노드, 진홍 일본 단일소스 병목, 남색 고객.</p>
    <svg viewBox="0 0 960 560" role="img" aria-label="TSMC value chain map">
      <defs>
        <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="#8A96A3"/></marker>
        <marker id="at" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5 0 10z" fill="#0E6B66"/></marker>
      </defs>
      <!-- column headers -->
      <g font-size="13" fill="#6B7785">
        <text x="10" y="22">Tier 2 원료·부품</text>
        <text x="235" y="22">Tier 1 소재·장비·유통</text>
        <text x="600" y="22">고객</text>
        <text x="800" y="22">최종 수요</text>
      </g>
      <!-- Tier 2 -->
      <g font-size="12" fill="#1C2733">
        <rect x="10" y="40" width="180" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="20" y="62">Hemlock · Wacker · OCI (폴리실리콘)</text>
        <rect x="10" y="84" width="180" height="34" rx="3" fill="#F3D5DC" stroke="#9B1C3A"/><text x="20" y="106">Stella · Morita (불산)</text>
        <rect x="10" y="128" width="180" height="34" rx="3" fill="#F3D5DC" stroke="#9B1C3A"/><text x="20" y="150">Hoya · AGC (EUV 블랭크)</text>
        <rect x="10" y="172" width="180" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="20" y="194">Zeiss · Cymer · Trumpf</text>
        <rect x="10" y="216" width="180" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="20" y="238">Edwards · MKS · Ichor</text>
        <rect x="10" y="260" width="180" height="34" rx="3" fill="#F3D5DC" stroke="#9B1C3A"/><text x="20" y="282">Ajinomoto (ABF 필름)</text>
      </g>
      <!-- Tier 1 -->
      <g font-size="12" fill="#1C2733">
        <rect x="235" y="40" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="55">SEH · SUMCO · GlobalWafers</text><text x="245" y="69" fill="#6B7785">웨이퍼 6사 92~96%</text>
        <rect x="235" y="84" width="190" height="34" rx="3" fill="#F6E3C8" stroke="#B4620A"/><text x="245" y="99">SK실트론 → 두산</text><text x="245" y="113" fill="#6B7785">2026.7 SPA 2.3조</text>
        <rect x="235" y="128" width="190" height="34" rx="3" fill="#F3D5DC" stroke="#9B1C3A"/><text x="245" y="143">JSR · TOK · Shin-Etsu</text><text x="245" y="157" fill="#6B7785">EUV 레지스트 90%+</text>
        <rect x="235" y="172" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="187">ASML (EUV 100%)</text><text x="245" y="201" fill="#6B7785">매입 1위 ~19% 추정</text>
        <rect x="235" y="216" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="231">AMAT · Lam · KLA · TEL</text><text x="245" y="245" fill="#6B7785">TEL 트랙 = 일본 병목</text>
        <rect x="235" y="260" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="275">Ibiden · Unimicron · Kinsus</text><text x="245" y="289" fill="#6B7785">ABF 기판</text>
        <rect x="235" y="304" width="190" height="34" rx="3" fill="#F6E3C8" stroke="#B4620A"/><text x="245" y="319">SK스페셜티 → 한앤코</text><text x="245" y="333" fill="#6B7785">NF3·WF6 1위, 2025.3</text>
        <rect x="235" y="348" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="363">Linde LienHwa · Air Liquide</text><text x="245" y="377" fill="#6B7785">가스 9사</text>
        <rect x="235" y="392" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3" stroke-dasharray="4 3"/><text x="245" y="407">Wah Lee · Topco · Kanto-PPC</text><text x="245" y="421" fill="#6B7785">유통·합작 중개</text>
        <rect x="235" y="436" width="190" height="34" rx="3" fill="#fff" stroke="#8A96A3"/><text x="245" y="451">대만전력 · 용수</text><text x="245" y="465" fill="#6B7785">원가 ~7~8%</text>
      </g>
      <!-- TSMC -->
      <rect x="470" y="150" width="110" height="200" rx="4" fill="#0E6B66"/>
      <g fill="#fff" font-size="13">
        <text x="525" y="205" text-anchor="middle" font-size="20" font-weight="600">TSMC</text>
        <text x="525" y="228" text-anchor="middle">매출 $1,224억</text>
        <text x="525" y="246" text-anchor="middle">GM 59.9%</text>
        <text x="525" y="264" text-anchor="middle">1,500만 장</text>
        <text x="525" y="290" text-anchor="middle" font-size="11" opacity=".85">원재료 ~17%</text>
        <text x="525" y="306" text-anchor="middle" font-size="11" opacity=".85">감가상각 ~45%</text>
      </g>
      <!-- OSAT below TSMC -->
      <rect x="455" y="400" width="140" height="40" rx="3" fill="#D6ECEA" stroke="#0E6B66"/>
      <text x="525" y="416" text-anchor="middle" font-size="12">ASE·SPIL · Amkor</text><text x="525" y="431" text-anchor="middle" font-size="11" fill="#6B7785">CoWoS 외주 24~27만 장</text>
      <path d="M525 350V400" stroke="#0E6B66" stroke-width="2" fill="none" marker-end="url(#at)"/>
      <!-- HBM side -->
      <rect x="455" y="470" width="140" height="40" rx="3" fill="#F6E3C8" stroke="#B4620A"/>
      <text x="525" y="486" text-anchor="middle" font-size="12">SK hynix HBM</text><text x="525" y="501" text-anchor="middle" font-size="11" fill="#6B7785">고객이 별도 조달 → CoWoS 합류</text>
      <path d="M525 470V440" stroke="#B4620A" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>
      <!-- Customers -->
      <g font-size="12" fill="#1C2733">
        <rect x="620" y="60" width="150" height="40" rx="3" fill="#D9E2EF" stroke="#31507A"/><text x="630" y="77">NVIDIA</text><text x="630" y="92" fill="#6B7785">2위 17% → 2026 1위</text>
        <rect x="620" y="110" width="150" height="40" rx="3" fill="#D9E2EF" stroke="#31507A"/><text x="630" y="127">Apple</text><text x="630" y="142" fill="#6B7785">1위 19% (하락 중)</text>
        <rect x="620" y="160" width="150" height="34" rx="3" fill="#fff" stroke="#31507A"/><text x="630" y="182">AMD · Broadcom · Marvell</text>
        <rect x="620" y="204" width="150" height="34" rx="3" fill="#fff" stroke="#31507A"/><text x="630" y="226">Qualcomm · MediaTek</text>
        <rect x="620" y="248" width="150" height="34" rx="3" fill="#fff" stroke="#31507A"/><text x="630" y="270">Google·AWS·MS 자체칩</text>
        <rect x="620" y="292" width="150" height="34" rx="3" fill="#fff" stroke="#31507A"/><text x="630" y="314">Intel (외주분)</text>
        <rect x="620" y="336" width="150" height="34" rx="3" fill="#fff" stroke="#31507A"/><text x="630" y="358">Sony·NXP·Infineon</text>
      </g>
      <!-- Final -->
      <g font-size="12" fill="#1C2733">
        <rect x="800" y="60" width="150" height="44" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="810" y="78">하이퍼스케일러 4사</text><text x="810" y="94" fill="#6B7785">MS·Meta·Google·AWS</text>
        <rect x="800" y="114" width="150" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="810" y="136">Foxconn → 소비자</text>
        <rect x="800" y="158" width="150" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="810" y="180">서버 조립 Quanta·Dell</text>
        <rect x="800" y="202" width="150" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="810" y="224">삼성·샤오미 (폰 OEM)</text>
        <rect x="800" y="336" width="150" height="34" rx="3" fill="#fff" stroke="#C9D1DA"/><text x="810" y="358">자동차 OEM</text>
      </g>
      <!-- arrows tier2->tier1 -->
      <g stroke="#8A96A3" stroke-width="1.2" fill="none" marker-end="url(#a)">
        <path d="M190 57H235"/><path d="M190 101C210 101 210 365 235 365"/><path d="M190 145H235"/><path d="M190 189H235"/><path d="M190 233H235"/><path d="M190 277H235"/>
      </g>
      <!-- arrows tier1->TSMC -->
      <g stroke="#8A96A3" fill="none" marker-end="url(#a)">
        <path d="M425 57C450 57 445 200 470 200" stroke-width="2.5"/>
        <path d="M425 101C450 101 445 210 470 210" stroke-width="1.2"/>
        <path d="M425 145C450 145 445 220 470 220" stroke-width="1.5"/>
        <path d="M425 189C450 189 445 230 470 230" stroke-width="3.5"/>
        <path d="M425 233C450 233 445 240 470 240" stroke-width="3"/>
        <path d="M425 277C450 277 445 250 470 250" stroke-width="1.2"/>
        <path d="M425 321C450 321 445 260 470 260" stroke-width="1"/>
        <path d="M425 365C450 365 445 270 470 270" stroke-width="1.2"/>
        <path d="M425 409C450 409 445 280 470 280" stroke-width="1"/>
        <path d="M425 453C450 453 445 300 470 300" stroke-width="1.5"/>
      </g>
      <!-- arrows TSMC->customers -->
      <g stroke="#31507A" fill="none" marker-end="url(#a)">
        <path d="M580 200C600 200 600 80 620 80" stroke-width="4"/>
        <path d="M580 210C600 210 600 130 620 130" stroke-width="4"/>
        <path d="M580 220C600 220 600 177 620 177" stroke-width="2"/>
        <path d="M580 230C600 230 600 221 620 221" stroke-width="1.5"/>
        <path d="M580 250C600 250 600 265 620 265" stroke-width="2"/>
        <path d="M580 270C600 270 600 309 620 309" stroke-width="1"/>
        <path d="M580 290C600 290 600 353 620 353" stroke-width="1.2"/>
      </g>
      <!-- customers->final -->
      <g stroke="#8A96A3" stroke-width="1.2" fill="none" marker-end="url(#a)">
        <path d="M770 80H800"/><path d="M770 130H800"/><path d="M770 177C785 177 785 175 800 175"/><path d="M770 221H800"/><path d="M770 265C785 265 785 82 800 82"/><path d="M770 353H800"/>
      </g>
      <!-- HBM to NVIDIA dashed -->
      <path d="M595 490C700 490 720 300 695 100" stroke="#B4620A" stroke-width="1.5" stroke-dasharray="4 3" fill="none"/>
      <text x="705" y="440" font-size="11" fill="#B4620A">HBM은 NVIDIA 원가에서</text>
      <text x="705" y="454" font-size="11" fill="#B4620A">TSMC보다 큼 (~$3.5k vs ~$2.3k)</text>
      <!-- footer note -->
      <text x="10" y="545" font-size="11" fill="#6B7785">선 굵기 = 대략적 금액 규모. 점선 박스 = 중개·유통. 한국 노드 2곳은 2025~26년 SK그룹에서 이탈.</text>
    </svg>
    <div class="legend"><span class="l-tsmc">TSMC·외주</span><span class="l-kr">한국 노드</span><span class="l-jp">일본 단일소스 병목</span><span class="l-cust">고객</span><span class="l-sup">기타 공급사</span></div>
  </section>
'''
