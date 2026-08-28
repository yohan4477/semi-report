---
title: 구리가 끝나는 거리 — 빛을 패키지 안으로 들인다
date: 2026-08-07
source: https://daily.semidoped.com/p/new-episode-globalfoundries-thomas
speaker: Thomas Barber
org: GlobalFoundries
channel: Semi Doped
host: Austin
section: link
topic: 실리콘 포토닉스 · CPO · SiGe
gain: 구리가 속도별로 몇 미터에서 끊기는지, 광 링크의 손실과 비트당 전력이 플러거블에서 CPO 로 가며 어떻게 줄어드는지를 수치로 짚는다. NRZ 로 되돌아가는 이유와 레이저 하나가 파이버 몇 가닥을 먹이는지까지.
---

## 한 줄
GlobalFoundries의 통신 인프라·데이터센터 담당 부사장 Tom Barber가 회사의 실리콘 포토닉스(Silicon Photonics, 빛으로 신호를 주고받는 반도체 기술) 사업 연혁과 300mm 웨이퍼 전환, 구리 배선의 한계, pluggable→NPO→CPO(co-packaged optics, 공동 패키지 광학) 전환 이유, OCI MSA(복수업체 합의 규격)가 PAM4 대신 NRZ 변조를 택한 배경, 자사 Scale 플랫폼과 실리콘 저메이늄(SiGe) 공정의 역할을 설명한다.

## 사실 — 절 순서대로

**GlobalFoundries의 포토닉스 역사**
- GlobalFoundries는 AMD에서 분사한 파운드리이며, 이후 Chartered Semiconductor와 IBM Microelectronics를 인수했다.
- IBM Microelectronics의 실리콘 포토닉스 작업은 2000년대 중반, CMOS 공정에 도파관(waveguide)·변조기(modulator)·포토다이오드(photodiode)를 집적하는 기초 연구로 시작했다.
- 약 10년 뒤인 2010년대 중반 25기가비트/레인(lane)급 제품이 대량 양산에 들어갔다. 당시는 장거리 점대점(point-to-point) 통신용으로만 쓰여 물량은 크지 않았다.
- 현재는 3세대 통합 실리콘 포토닉스 제품이 데이터센터에 대규모로 공급되고 있다고 밝혔다.
- Barber는 GlobalFoundries가 매출 기준 최대 순수(pure-play) 실리콘 포토닉스 파운드리라고 말했다.
- 실리콘 포토닉스를 뉴욕주 몰타(Malta) 공장의 300mm 웨이퍼 라인으로 조기에 옮긴 것이 매출 1위의 핵심 요인 중 하나라고 설명했다.
- 싱가포르의 AMF(어드밴스드 마이크로 파운드리) 팀을 합류시켜 장거리(long-range) 제품군을 보강했다. GF 자체는 원래 단거리·데이터센터용 제품에 집중해 있었다고 설명했다.

**300mm 웨이퍼로의 확장**
- 오늘날 실리콘 포토닉스 대부분은 여전히 200mm 웨이퍼에서 생산된다고 말했다.
- 300mm 웨이퍼는 반지름이 200mm 대비 50% 커지고 면적은 반지름 제곱에 비례하므로, 웨이퍼당 다이(die) 수가 2.25배가 되고 같은 웨이퍼 매수로 완제품이 두 배 넘게 나온다고 설명했다.
- 5년 전만 해도 실리콘 포토닉스는 상대적으로 작은 사업이었다. 인듐 인화물(Indium Phosphide)·EML 등 대안 기술이 50~100기가비트/초 구간에서 경쟁력이 있었고, 데이터센터 시장 자체도 아직 크지 않았다고 말했다.
- 200기가비트/초 레인 속도가 실리콘 포토닉스에 최적인 구간으로 떠오르면서 수요가 늘었다고 설명했다.

**구리의 한계와 광통신의 부상**
- 100기가비트/초에서는 별도 신호증폭 없는 직결(direct attached) 구리 케이블이 약 2m까지 뻗을 수 있다. 이는 랙 높이 정도라고 말했다.
- 200기가비트/초에서는 도달 거리가 약 1m로 줄어든다. NVL72 같은 시스템에서 스위치를 랙 중간으로 옮긴 이유로 이를 들었다.
- 400기가비트/초에서는 도달 거리가 0.5m로 더 줄어, 광통신으로 넘어갈 수밖에 없다고 설명했다.
- 현재 스케일업(scale-up) 네트워크 대부분은 한 랙 안에서 이뤄진다. NVL72와 AMD가 최근 발표한 Helios도 단일 랙 구성이라고 말했다.
- 여러 랙에 걸치려면 수십~수백 미터 거리를 커버해야 하는데, 이 속도에서는 구리로 불가능하고 광통신이 필수라고 말했다.
- 구글과 화웨이는 이미 단일 랙(72~144 GPU)을 넘어 6~10개 랙, 300~1,000 GPU 규모로 스케일업 네트워크를 확장했다고 언급했다.
- 광 연결 방식은 pluggable(꽂는 방식) → NPO(near-packaged optics) → CPO 순으로 발전하는 추세이며 이유는 비용·전력·밀도라고 설명했다.
- pluggable은 랙 가장자리에서 GPU/스위치 ASIC까지 약 35dB 손실이 발생하며, 이를 DSP(디지털 신호 처리 칩)로 보상해야 해 비용과 전력 부담이 크다고 말했다.
- NPO로 가면 손실이 약 15~20dB로 줄어든다. 링크 예산이 충분하면 재타이밍(retimer) 없는 리니어(linear) 방식으로 DSP를 없앨 수 있다고 설명했다.
- CPO까지 가면 손실이 약 6dB로 더 줄어들고, SerDes(직렬-병렬 변환기) 전력도 함께 낮아진다고 말했다.
- 비트당 전력 비교: 완전 재타이밍 pluggable은 약 20~25pJ/bit, 리니어 NPO는 약 10pJ/bit, CPO는 5pJ/bit 미만까지 낮출 수 있다고 설명했다.
- 통신에 쓰는 전력은 열 제약이 있는 시스템에서 연산에 못 쓰는 전력이므로 최소화해야 한다고 말했다.

**CPO의 신뢰성과 비용 우위**
- pluggable의 손실은 광학 자체가 아니라 코어 프로세서에서 서버 가장자리까지 이어지는 PCB(인쇄회로기판) 전기 배선(수백 cm)에서 발생한다고 설명했다. 200기가비트/초 PAM4 신호는 약 55GHz 대역폭이 필요하다고 밝혔다.
- 업계가 CPO로 곧장 가지 못하는 이유로 신뢰성을 꼽았다. pluggable은 문제가 생기면 갈아 끼우면 되지만, CPO는 GPU 패키지에 영구 부착되므로 신뢰성 기준이 훨씬 높아야 한다고 말했다.
- Meta가 약 5만 개 GPU 규모 네트워크에서 CPO 신뢰성을 검증하는 연구를 여러 차례 발표했으며, 누적 테스트 시간이 (Barber 본인도 확신은 없다는 투로) 약 5천만 시간에 이른다고 언급했다. Meta는 이 테스트에서 링크 플랩(link flap, 연결 끊김·재연결이 반복되는 현상)이 전혀 없었고 신뢰성이 pluggable보다 높게 나왔다고 밝혔다고 전했다.
- pluggable에서 신뢰성 문제로 지목되는 사례 상당수는 광학 자체가 아니라 커넥터에 먼지가 들어가는 등 '꽂는' 구조 자체에서 비롯된다고 설명했다. CPO는 클린룸에서 조립돼 이런 문제가 없다고 말했다.
- CPO는 pluggable과 '동등한' 신뢰성이 아니라 '훨씬 더 높은' 신뢰성을 입증해야 영구 부착 부품으로 채택될 수 있다고 말했다.
- 비용 측면에서 CPO는 케이스·MCU·전원회로·DSP 등 pluggable을 구성하던 여러 부품이 사라지며, 특히 DSP 제거가 비용 절감의 가장 큰 부분을 차지한다고 설명했다. 전력 절감은 곧 운영비 절감으로 이어진다고 덧붙였다.

**OCI MSA와 NRZ로의 전환**
- MSA(Multi-Source Agreement)는 IEEE 같은 표준의 여러 옵션 가운데 업계가 합의해 실제로 상호운용 가능한 규격으로 좁힌 것이라고 설명했다. 대표적 사례로 Wi-Fi Alliance를 들었다.
- 기존 광 MSA(OSFP 계열)는 주로 기계적 폼팩터에 집중했고, 전기 인터페이스는 OIF가, 광 인터페이스는 IEEE가 정의해왔다고 말했다.
- OCI MSA는 광 인터페이스 자체를 새로 정의한다는 점이 다르다. 참여사는 AMD, Broadcom, Nvidia 등 데이터센터 핵심 공급사들이며, 스케일업 컴퓨팅용으로 IEEE 802.3 규격이 적합하지 않다고 판단해 별도 규격을 만들었다고 설명했다.
- IEEE는 PAM4(한 심볼에 2비트, 4레벨을 싣는 다중 레벨 변조)로 발전해왔는데, OCI는 대신 NRZ(한 심볼에 1비트를 싣는 이진 변조)로 되돌아가 속도를 50GHz로 낮추고, 대신 광섬유 한 가닥에 파장 4개를 실어 200기가비트/초 대역폭을 유지한다고 설명했다.
- NRZ 50GHz의 고유 비트 오류율(bit error rate)은 PAM4보다 약 100만 배 낮다고 밝혔다. 이는 수신단 채널 등화(equalization)와 순방향 오류정정(forward error correction) 부담을 줄여 비용·전력을 낮춘다고 설명했다.
- 스케일업 애플리케이션에서 최대 스위치 용량은 100테라비트/초이며, 200기가비트/초 파이버 기준으로 스위치 하나에 GPU 512개를 연결할 수 있다고 설명했다.
- NVL72는 스위치 18개를 병렬로 써서 GPU당 7.2테라비트/초 대역폭을 확보하며, 실제로는 구리를 쓰고 구리 쌍 하나당 200기가비트/초를 18개 스위치에 나눠 쓴다고 설명했다.
- 레이저 1개가 구동하는 파이버 수는 pluggable 기준으로 보통 4대1(레이저 2개로 파이버 8개 구동)이었으나 8대1로 이동 중이며, OCI 규격에서는 최대 32대1까지 늘어날 수 있다고 설명했다. OCI가 요구하는 8파장 광엔진 하나를 레이저 8개로 구동할 수 있다는 뜻이라고 덧붙였다.

**GlobalFoundries의 OCI 대응 Scale 플랫폼**
- GlobalFoundries가 발표한 Scale은 "첫 OCI 대응(capable) 플랫폼"이라고 밝혔다. 전기-광 변환에 필요한 요소를 정해진 폼팩터(칩렛·모듈)로 묶은 제품이라고 설명했다.
- 구성은 CPU/GPU/AI ASIC과 통신하는 전자 IC와, 전자-광 신호를 변환하는 광자(photonic) IC로 이뤄지며, 광자 IC에는 탈부착 가능한 커넥터가 달려 있다고 말했다. 서버 조립 시 파이버가 상시 매달려 있지 않도록, 전기 배선처럼 마지막에 광 배선을 연결할 수 있게 하기 위해서라고 설명했다.
- GlobalFoundries는 광자 IC를 100% 자체 제조하며, 전자 IC는 설계 복잡도에 따라 자사 FinFET·FDX 공정 또는 실리콘 저메이늄(SiGe) 공정을 쓰거나, 고객이 3nm·2nm 같은 첨단 공정 웨이퍼를 가져오면 조립·테스트만 맡는다고 설명했다. 마이크로 광학 부품은 외부에서 제조하고 조립·테스트는 GF가 담당한다고 말했다.

**마이크로 미러 기술과 O-밴드**
- TSMC는 CoWoS와 격자 결합기(grating coupler)를 쓰는데, GlobalFoundries는 다이 가장자리 결합(edge coupling)과 유사하되 웨이퍼에 심은 마이크로 미러로 빛을 수직으로 받아 수평으로 반사시키는 방식을 쓴다고 설명했다.
- 격자 결합기는 대역폭이 제한돼 O-밴드(O band, 약 1310nm 파장대의 광통신 대역) 전체를 한 솔루션으로 커버할 수 없지만, 마이크로 미러 방식은 O-밴드 전체를 쓸 수 있어 파장 확장에 유리하다고 설명했다. 현재 OCI는 방향당 파장 4개를 쓰며, 향후 대역폭 확장은 파장 수를 늘리는 방향이라고 말했다.

**시장 검증과 실리콘 저메이늄의 역할**
- 경쟁사(TSMC 등)를 "적"이 아니라 구리를 대체하는 공동 목표를 가진 상대로 표현하며, 구리가 완전히 사라지기 전까지는 시장이 충분히 크다고 말했다.
- 광엔진에 필요한 부품을 광자 IC(실리콘 포토닉스)와 이를 구동하는 고속 아날로그 전자 IC(모듈레이터 드라이버, 트랜스임피던스 증폭기) 두 갈래로 나눠 설명했다. 모듈레이터 드라이버 기능은 점차 DSP로 통합돼 시장이 줄고 있다고 언급했다.
- 200기가비트/초 PAM4 신호를 다루려면 재타이밍 시스템 기준 약 55GHz, 리니어 시스템 기준 약 70GHz 대역폭이 필요하며, 증폭기 트랜지스터 속도는 대역폭의 5배가 필요하다고 설명했다. 200기가비트/레인에는 350~400GHz, 400기가비트/레인에는 600~700GHz급 트랜지스터가 필요하다고 말했다.
- 이 속도를 대량·신뢰성 있게 낼 수 있는 기술이 몇 안 되는데, GlobalFoundries의 실리콘 저메이늄(SiGe) 공정이 그중 하나이며 이미 200기가비트/레인 요구치를 넘는 트랜지스터 속도를 갖고 있고 400기가비트/레인을 지원하는 차세대 로드맵도 있다고 밝혔다.
- 1.6T 트랜시버 물량이 늘어나는 400기가비트/레인 구간에서 GlobalFoundries가 "불균형적으로 큰" 점유율을 얻고 있다고 말했다.

## 숫자 (원문에 나온 것만)
- 25기가비트/레인 — 2010년대 중반 첫 대량 양산 제품 속도
- 200mm → 300mm 웨이퍼 전환, 다이 수 2.25배 (반지름 1.5배의 제곱)
- 50~100기가비트/초 — 인듐 인화물·EML이 경쟁력 있었던 구간
- 200기가비트/초 — 실리콘 포토닉스 최적 레인 속도로 언급된 구간
- 구리 도달 거리: 100기가비트/초에서 약 2m, 200기가비트/초에서 약 1m, 400기가비트/초에서 약 0.5m
- 손실: pluggable 약 35dB, NPO 약 15~20dB, CPO 약 6dB
- 비트당 전력: 재타이밍 pluggable 약 20~25pJ/bit, 리니어 NPO 약 10pJ/bit, CPO 5pJ/bit 미만
- PAM4 200기가비트/초 신호 대역폭 약 55GHz(재타이밍), 약 70GHz(리니어)
- Meta 테스트: GPU 약 5만 개 네트워크, 누적 약 5천만 시간(Barber도 "something like that"이라 확언은 아님)
- NRZ 50GHz 비트 오류율은 PAM4보다 약 100만 배 낮음
- 스위치 최대 용량 100테라비트/초 → 200기가비트/초 파이버 기준 스위치당 GPU 512개
- NVL72: 스위치 18개, GPU당 7.2테라비트/초
- 구글·화웨이 스케일업 규모: 6~10랙, GPU 300~1,000개(화자가 예시로 든 대략치)
- 레이저당 구동 파이버 수: 기존 4:1 → 8:1 이동 중, OCI 최대 32:1
- O-밴드 파장 약 1310nm
- 증폭기 필요 트랜지스터 속도: 200기가비트/레인 350~400GHz, 400기가비트/레인 600~700GHz(대역폭의 5배 규칙)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- Tom: "The enemy to me right now is copper. I'm trying to beat copper, right?" — "지금 나의 적은 구리다. 나는 구리를 이기려는 것이다."
- Tom: "So every picojoule of power that goes into the communications is one you can't use for compute." — "통신에 들어가는 전력 1피코줄은 곧 연산에 쓸 수 없는 1피코줄이다."
- Tom: "CPO has to be way more reliable than pluggables." — "CPO는 pluggable보다 훨씬 더 신뢰성이 높아야 한다."
- Tom: "The native bit error rate for NRZ 50 gigahertz is about a million times less than what it is for PAM4." — "NRZ 50기가헤르츠의 고유 비트 오류율은 PAM4보다 약 100만 배 낮다."
- Tom: "When you go to a 300 mm wafer, it's the radius squared, right? So you go up by 50% in radius, you square that, you get 2.25 times as many die per wafer." — "300mm 웨이퍼로 가면 반지름의 제곱이 문제다. 반지름이 50% 늘면 제곱해서 다이가 2.25배가 된다."
- Tom: "So it all comes down to the fundamental limitation of copper, which is range, right?" — "결국 다 구리의 근본적 한계, 즉 도달거리 문제로 귀결된다."
- Tom: "What they found is the reliability is actually higher than it is with pluggables, and they found no link flap." — "Meta가 확인한 것은 신뢰성이 실제로 pluggable보다 높다는 것이었고, 링크 플랩은 전혀 발견되지 않았다."
- Tom: "The market doesn't lie, right? So the market will choose the best solution." — "시장은 거짓말하지 않는다. 시장이 최선의 솔루션을 고를 것이다."

## 주의
- 원문에 "OFSP"로 표기된 곳(1곳)이 있으나 문맥상 pluggable 폼팩터 표준인 OSFP(Octal Small Formfactor Pluggable)의 오기·전사 오인식으로 보인다.
- 원문에 "IEEE 803 802.3"으로 표기된 대목이 있다. 말을 고쳐 하는 중 겹친 것으로 보이며 정식 표기는 IEEE 802.3이다.
- 구글·화웨이 스케일업 규모("300, 500, 1,000 GPUs")와 Meta 테스트 누적 시간("up to 50 million hours or something like that")은 화자 본인이 헤지 표현을 쓴 대략치이며, 정확한 공식 수치로 인용하지 않도록 주의.
- "Silicon Photonics"·"O band"·"OCI"·"NRZ"·"PAM4" 등은 팟캐스트 내내 영어 약어 그대로 쓰였고, 한국어 대응어를 화자가 별도로 제시하지 않았다.
