---
title: Credo가 더스트포토닉스를 인수해 실리콘 포토닉스까지 갖춘 이유
date: 2026-04-17
source: https://www.youtube.com/watch?v=aIX5Sku2URI
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 [[Austin Lyons]] (Chipstrat) · [[Vik Sekar]] (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: link
topic: Credo-더스트포토닉스 인수, XPO·CPX 소켓형 커넥터, 코히런트 광통신(scale-across)
gain: Credo가 서데스와 실리콘 포토닉스 설계를 함께 갖추려 인수에 나선 이유(공급망 통제·마진 확보)와, 공동 패키지 광학(CPO)이 몰고 올 스위치 실리콘 종속에 맞서 업계가 XPO·CPX 같은 소켓형 커넥터로 기존 탈착형 생태계를 지키려는 구조.
---

## 한 줄
Austin Lyons와 Vik Sekar가 이번 주 반도체 뉴스 중 포토닉스(광학)만 골라 짚었다. Credo가 7억5천만 달러 이상을 들여 이스라엘 실리콘 포토닉스 업체 더스트포토닉스(Dust Photonics)를 인수한 배경과, 공동 패키지 광학(CPO)이 몰고 올 스위치 실리콘 종속에 맞서 아리스타네트웍스가 내세운 소켓형 커넥터 XPO·CPX까지 정리했다. 앞부분에는 퀄컴에 NuVia를 매각한 창업자들이 다시 세운 CPU 회사 Nuvacore와 에이전틱 AI 시대의 CPU 품귀 이야기도 짧게 나온다.

## 사실 — 절 순서대로
- 진행 소개. Austin은 자신을 Chipstrat 소속으로, Vik를 Vik's Newsletter 소속으로 소개하며 녹음을 시작했다.
- 화두 고르기. 그 주 Credo의 더스트포토닉스 인수, 브로드컴-메타 칩 거래 등 다룰 소재가 많다며, Vik가 범위를 포토닉스로 좁히자고 제안했다.
- Nuvacore 소개. Vik가 새 CPU 회사 Nuvacore(자막에는 "NuVia Core"로 표기) 소식을 물었고, Austin이 이 회사를 창업한 사람들이 2021년 퀄컴에 인수된 CPU 회사 NuVia의 창업자들이라고 설명했다.
- NuVia 배경. Austin은 NuVia 창업자 제라드 윌리엄스(Gerard Williams)가 애플 출신으로 M 시리즈 프로세서 개발에 참여했고, NuVia 매각 후에는 ARM과의 아키텍처 라이선스 소송의 쟁점 인물이었다고 설명했다.
- CPU 품귀. Austin은 에이전틱 AI 시대에 x86·ARM 구분보다 "구할 수 있는 CPU가 곧 최선의 CPU"라며, AI 수요가 CPU 공급을 다 가져가 일반 클라우드 사업자도 CPU를 못 구하는 상황이라고 말했다.
- 워크로드 물음. Austin은 GPU 오케스트레이션이 헤드 노드에 얼마나 가까이 있어야 하는지, 에이전트의 툴 호출·코드 실행이 CPU와 GPU 사이를 계속 오가며 생기는 지연(latency) 문제를 더 파고들고 싶다고 밝혔다.
- 젠슨 황 인터뷰. Vik는 젠슨 황의 드워케시(Dwarkesh) 팟캐스트 인터뷰를 언급하며, 에이전트가 EDA 도구를 대량으로 돌리게 되면 케이던스·시놉시스의 라이선스 판매가 늘 것이라는 황의 전망을 전했다.
- Credo 인수 발표. Vik가 발표 세부를 정리했다 — Credo는 더스트포토닉스를 현금 7억5천만 달러 선지급에 거의 100만 주, 여기에 추가 언아웃(earnout, 성과 조건 충족 시 지급하는 추가 대가)까지 더해 총합이 10억 달러를 살짝 넘는 규모로 인수했다.
- 더스트포토닉스 배경. Vik는 이 회사가 2017년 창업된 이스라엘 팹리스(fabless, 자체 공장 없이 설계만 하는) 업체로, 투자자 중 개빈 베이커(Gavin Baker)와 자막상 "Actuaries Management"가 있으며 위탁생산은 타워세미컨덕터(Tower Semiconductor)일 가능성이 크다고 말했다.
- 더스트포토닉스 규모. Vik는 직원이 약 70명이고, 400G·800G·1.6T급 광집적회로(PIC, 빛으로 신호를 처리하는 칩) 포트폴리오와 3.2T까지의 로드맵을 갖췄다고 설명했다.
- Credo의 기존 사업. Austin은 Credo가 서데스(serdes, 직렬화·역직렬화 회로) IP 라이선스에서 시작해 능동형 전기 케이블(AEC)·광학 DSP·트랜시버까지 갖춘 회사라고 정리하며 더스트포토닉스가 어디에 들어맞는지 물었다.
- Credo 대 마벨. Vik는 마벨이 DSP만 만들고 케이블 자체는 만들지 않는 것과 달리, Credo는 케이블까지 직접 만드는 종단간 업체이며, 링크 상태를 모니터링하는 소프트웨어 "파일럿(Pilot)"을 마벨의 "라이언트(Reliant)"에 대응해 운영한다고 설명했다.
- 인수 의미. Vik는 이번 인수로 Credo가 처음으로 자체 실리콘 포토닉스 칩 설계 능력을 갖춰, 근접 패키지 광학(NPO)·선형 탈착형 광학(LPO)·CPO 어디든 대응할 수 있게 됐다고 말했다. 발표 후 Credo 주가는 한 주간 약 50% 올랐다.
- 수직 통합 이유. Austin이 왜 실리콘 포토닉스를 자체 소유해야 하는지 묻자, Vik는 서데스와 칩 설계를 함께 최적화할 수 있고, 공급망을 남에게 의존하지 않을 수 있다는 두 가지 이유를 들었다.
- 마진과 원스톱. Austin은 이를 마진을 더 많이 가져가는 효과와, 하이퍼스케일러가 문제가 생겼을 때 연락할 곳이 하나뿐인("one throat to choke") 이점으로 연결해, Credo가 AEC 때부터 써온 종단간 전략을 이어가는 것이라고 정리했다.
- 마이크로 LED. Austin이 Credo의 하이퍼룸(Hyperloom) 인수(활성 LED 케이블, ALC)까지 언급하며 레이저와 마이크로 LED의 차이를 묻자, Vik는 개빈 베이커의 트윗을 근거로 하이퍼스케일러들이 마이크로 LED에 관심을 보인다고 답했다.
- 레이저 대 마이크로 LED. Vik는 레이저가 PAM4(4레벨 펄스 진폭 변조) 방식으로 레인당 최대 200Gbps를 내는 반면, 마이크로 LED는 레인당 2~10Gbps에 그쳐 여러 가닥을 나란히 묶어 1.6T급 속도를 낸다고 설명했다.
- 구리는 2030년까지. Vik는 개빈 베이커의 트윗을 빌려, 엔비디아의 루빈 울트라(Rubin Ultra, 자막은 "Ruben Ultra")가 미드플레인 PCB로 구리 상호연결 경로를 아예 짧게 줄인 사례를 들며 구리가 2030년까지는 사라지지 않을 것이라고 말했다.
- 스케일 어크로스. Vik는 개빈 베이커가 꼽은 다음 성장 축이 스케일 업이 아니라 "스케일 어크로스(scale-across, 데이터센터 사이를 잇는 연결)"라는 점에 놀랐다며, 초대형 모델을 여러 데이터센터에 나눠 훈련하려면 진폭과 위상을 함께 쓰는 코히런트(coherent) 광통신이 필요하다고 설명했다.
- 트레이니엄 모델. 두 진행자는 최근 화제가 된 10조 파라미터급 모델(자막에는 "myth house"로 표기)이 엔비디아 블랙웰이 아니라 AWS 트레이니엄 칩으로 훈련됐다는 이야기가 있었다며, AWS의 맷 가먼(Matt Garman) 또는 앤디 재시(Andy Jassy)가 이를 확인했다고 언급했다.
- 코히런트 사업자. Vik는 장거리 코히런트 광통신을 하는 회사로 시에나(Ciena)·시스코를 들고, 노키아가 인피네라(Infinera)를 인수해 이 분야의 주요 사업자가 됐다고 덧붙였다.
- 더스트포토닉스의 L3C. Vik는 더스트포토닉스가 가진 저손실 레이저 결합 기술(L3C, low-loss laser coupling)을 소개했다 — 마벨처럼 레이저를 광집적회로 위에 접합하는 대신, 어떤 연속파(CW) 레이저든 공기층 없이 옆에서 결합할 수 있다는 점이 핵심이라고 설명했다.
- 액체 냉각과의 연결. Vik는 공기층이 없으면 액체 냉각액이 결합부의 굴절률을 어지럽히지 않아, 이 결합 방식 전체를 액체 냉각 환경에 넣을 수 있다고 말했다.
- XPO 등장. Vik는 아리스타네트웍스(Arista Networks)가 올해 OFC 학회에서 발표한 새 커넥터 XPO(초고밀도 탈착형 광학, extra-dense pluggable optics)를 소개했다 — 2016년에 나온 OSFP 모듈의 후속으로, 커넥터 하나에서 OSFP의 8배인 12.8Tbps를 내고 400W까지 액체 냉각으로 감당한다고 설명했다.
- XPO 생태계. Vik는 100개가 넘는 회사가 XPO의 다중공급사협약(MSA)에 참여했다고 밝혔다.
- XPO 대 CPO 긴장. Austin이 에너지 효율이 더 좋은 CPO 대신 왜 전력을 더 많이 쓰는 XPO로 가느냐고 묻자, Vik는 CPO가 엔비디아·브로드컴 같은 스위치 실리콘 업체에 생태계 전체를 종속시킨다는 점을 짚었다.
- 아리스타의 이해관계. Austin은 아리스타가 스위치 실리콘을 브로드컴에서 사 와 그 위에 EOS 소프트웨어로 가치를 더하는 구조인데, 광학 엔진까지 브로드컴 칩 안으로 들어가면(CPO) 아리스타가 더할 수 있는 부분이 줄어든다며, 그래서 아리스타가 XPO 생태계 확산에 이해관계를 갖는다고 설명했다.
- CPX 소개. Vik는 마지막으로 CPX(엔비디아의 루빈 CPX와는 다른 개념)를 소개했다 — CPO처럼 광학 엔진을 스위치 실리콘 옆에 두지만, 그 광학 엔진 자체를 소켓에 꽂아 갈아 끼울 수 있게 만든 방식이며, 셈텍(Semtech)과 몰렉스(Molex)가 이를 이끌고 있다고 말했다.
- 모듈화 전략. Austin은 기존 탈착형 트랜시버 생태계 참여자들이 로드맵을 이어가려면 XPO를, CPO 쪽으로 가더라도 소켓형인 CPX를 선호할 것이라며, 어느 쪽이든 생태계를 더 모듈화해 경쟁을 유지하려는 움직임이라고 정리했다.
- 광섬유 배선 문제. Vik는 소켓형 CPO(CPX)에서도 랙 안으로 광섬유를 끌어들이는 배선 문제가 여전히 남는다며, 광섬유는 구부림 각도에 민감해 손실·단선 위험이 있어 업계는 랙 내부 배선을 구리로, 광학은 랙 바깥에 두는 XPO식 접근을 선호한다고 말했다.
- 마무리. 두 사람은 이 분야에 아직 정해진 승자가 없다며, 각자 서브스택(Substack)에 더 자세한 도해와 글을 올리기로 하고 방송을 마쳤다.

## 숫자 (원문에 나온 것만)
- 7억5천만 달러 — Credo가 더스트포토닉스 인수에 선지급한 현금
- 거의 100만 주 — 현금과 함께 지급하는 Credo 주식(언아웃 별도)
- 10억 달러 남짓 — 언아웃까지 포함한 인수 총 잠재 금액
- 2017년 — 더스트포토닉스 창업 연도
- 약 70명 — 더스트포토닉스 직원 수
- 400G·800G·1.6T — 더스트포토닉스 현재 광집적회로(PIC) 포트폴리오 속도
- 3.2T — 더스트포토닉스 로드맵상 목표 속도
- 약 50% — 인수 발표 후 한 주간 Credo 주가 상승률
- 200Gbps — 레이저 기반 PAM4 변조의 레인당 최대 데이터 전송률
- 2~10Gbps — 마이크로 LED 레인당 데이터 전송률
- 1.6T — 마이크로 LED를 다수 레인으로 병렬 연결해 낼 수 있는 총 속도
- 2016년 — OSFP 모듈 도입 시점
- 12.8Tbps — XPO 커넥터 하나가 내는 총 대역폭(OSFP의 8배)
- 1.6Tbps — OSFP 커넥터 하나의 대역폭
- 64채널 × 200Gbps — XPO 대역폭 산출 근거
- 400W — XPO 커넥터가 액체 냉각으로 감당할 수 있는 전력 손실
- 100개사 이상 — XPO 다중공급사협약(MSA)에 참여한 기업 수
- 2030년 — 개빈 베이커가 말한, 구리 상호연결이 유지될 것으로 보는 시점
- 2021년 — 퀄컴이 NuVia를 인수한 연도
- 10조 파라미터 — Vik가 예로 든 미래 초대형 모델의 파라미터 수(가상 예시, 실측 아님)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "So, CPX is the socketed CPO where you can put anybody's optical engine and socket it and close it down." — Vik. "그러니까 CPX는 소켓형 CPO예요. 누구의 광학 엔진이든 꽂아서 소켓에 끼우고 닫아버릴 수 있는 거죠."
- "The force of AI has taken over all CPU chips now and like nobody gets anything for anything else." — Austin. "지금은 AI의 힘이 모든 CPU 칩을 다 가져가버려서, 다른 용도로는 아무도 아무것도 못 구해요."
- "If there is no air gap, you can put this entire thing into a liquid cooling environment." — Vik. "공기층이 없으면, 이 전체를 액체 냉각 환경에 그대로 넣을 수 있어요."
- "You can get 12.8 terabits per second out of single connector... For an OSFP, you would only get like 1.6." — Vik. "커넥터 하나에서 12.8테라비트/초를 뽑아낼 수 있어요... OSFP라면 1.6밖에 안 나오죠."
- "CPO is a complexity that you don't need... XPO is what you need to run traditional pluggable interconnection in a data center for a massive number of chips for AI applications." — Vik. "CPO는 필요 없는 복잡함이에요... AI 용도로 엄청난 수의 칩이 들어간 데이터센터에서 기존 탈착형 방식의 연결을 계속 쓰려면 필요한 게 바로 XPO죠."
- "Sometimes I think for these hyperscalers when time is of the essence, like one throat to choke, the idea of one throat to choke, just one vendor that I'm working with is actually pretty nice." — Austin. "하이퍼스케일러 입장에서 시간이 급할 때는 '목 조를 곳 하나(one throat to choke)'라는 개념이 있잖아요. 그냥 협력하는 벤더가 하나뿐이라는 게 꽤 괜찮게 느껴질 때가 있죠."

## 주의
- 이 전사는 화자 태그가 없어("Vik:" "Austin:" 같은 표시가 없다) 위 「사실」 절의 화자 배정은 두 사람의 역할(Austin은 CPU·사업 전략 쪽 질문, Vik는 포토닉스 기술 설명)을 근거로 추정한 것이며, 대화가 빠르게 오간 구간 일부는 확실하지 않다.
- "Nuvacore"는 영상 제목 메타데이터의 표기이고, 전사 자막은 이를 "NuVia Core"로 잘못 갈라 받아 적었다 — 앞서 퀄컴에 팔린 회사 NuVia와 혼동하기 쉬운 표기다.
- 투자자명 "Actuaries Management"는 자막이 잘못 받아 적었을 가능성이 있으나 정확한 표기를 확인하지 못했다.
- "myth house"(트레이니엄 훈련 모델 이름으로 언급)는 자막이 잘못 받아 적은 것으로 보이나 원래 명칭을 확인하지 못했다.
- Credo의 광 인터커넥트 포트폴리오 명칭이 "zero flat optics" / "ZF optics"로 나오는데, 업계에서 흔히 쓰는 장거리 코히런트 규격명 "ZR"의 오인식일 가능성이 있으나 확인하지 못했다.
- "use CPC inside the switch rack"이라는 대목은 앞뒤 문맥(광섬유 대신 구리를 쓴다는 논지)상 "구리(copper)"의 오인식으로 보인다.
