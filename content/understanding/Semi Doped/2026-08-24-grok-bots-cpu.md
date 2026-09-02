---
title: GPU 옆에 CPU 를 몇 개나 두어야 하나
date: 2026-08-24
source: https://daily.semidoped.com/p/new-episode-grok-bots-and-how-cpus
speaker: Austin Lyons · Vik Sekar
org: Semi Doped 공동 진행
channel: Semi Doped
host: Austin Lyons · Vik Sekar
people: 진행 Austin Lyons (Chipstrat) · Vik Sekar (Vik's Newsletter) — Semi Doped 공동 진행. 게스트 없음
section: compute
topic: 에이전틱 AI · 호스트 CPU · 코어 수
gain: 에이전트를 돌리는 일이 GPU 가 아니라 CPU 쪽 수요로 번지는 경로. 호스트 노드에 남아 돌던 코어를 다시 쓰는 방식과, 코어 수가 88 에서 512 로 가는 사례.
---

## 한 줄
그 주 출시된 xAI의 에이전트형(agentic) AI 플랫폼 "Grok bot"을 계기로, 진행자 두 사람이 "GPU=천재(genius), CPU=비서(assistant)" 비유를 세워 호스트 노드 CPU와 새로 떠오르는 "에이전틱 CPU(agentic CPU)"의 차이를 정리한다. Mac Mini 열풍의 원인부터 코어 수·랙 구성·오케스트레이션 소프트웨어 부재까지 짚는다.

## 사실 — 절 순서대로
- Grok bot 소개. Vik는 그 주 출시된 Grok bot을 "오픈클로(Open Claw, 오픈소스 에이전트 하니스)"에 비유하면서도 훨씬 쓰기 쉽고, 컴퓨터를 꺼둬도 에이전트가 계속 돌아간다는 점을 강조했다.
- 녹음 장소. Austin은 Chipstrat, Vik는 Vik's Newsletter를 각각 운영하며 공동 진행한다. Vik는 이번 회차를 베이 에어리어에서 녹음했는데, Hot Chips 참석을 위해 한 주 일찍 도착했고 그 전에는 대만 타이베이의 Open Compute Project APAC에 참석했다고 밝혔다.
- 설치 방식. Grok bot은 웹사이트에서 다운로드·설치하면 대화형으로 "chief agent"를 지정하고 그 아래 하위 에이전트(비서 에이전트, 뉴스 모니터링 에이전트 등)를 구성한다 — 커맨드라인이나 API 키를 따로 설정할 필요가 없다.
- 클라우드 VM 구조. Grok bot은 로컬이 아니라 클라우드의 전용 가상머신(VM)에서 동작한다. 도구·로그인 정보가 모두 그 VM 안에 있어 MCP 연결이나 플러그인을 따로 붙일 필요가 없고, 한 도구에 로그인하면 모든 에이전트가 공유해서 쓸 수 있다.
- 로컬 관리와 대비. Austin은 이를 로컬에서 여러 클로드(Claude) 에이전트를 직접 관리하는 방식과 비교했다. 로컬 관리는 OpenRouter 등으로 모델별 라우팅을 세밀하게 설정할 수 있는 대신 손이 많이 간다고 Vik가 대비했다.
- Mac Mini 열풍의 시작. 에이전트가 처음 등장한 건 작년(2025년) 12월이었고, 인텔은 올해 2월 실적발표에서 "CPU 수요가 이렇게 몰릴 줄 몰랐다"고 말했다고 Vik가 전했다.
- Mac Mini를 산 이유. Vik는 오픈클로 같은 에이전트 하니스를 기존 노트북에 깔면 컴퓨터 전체(민감정보 포함)에 접근권을 주게 되는 게 꺼려져서, 사람들이 에이전트 전용 샌드박스로 별도 기기(Mac Mini)를 마련했다고 설명했다.
- 자가 운영의 문제점. Vik는 정전·PSU 고장 시 다운, 인터넷 장애 시 원격 접속 불가, Tailscale 같은 VPN 네트워크 구성 필요 등 가정용 서버 운영의 번거로움을 지적했다(자신이 10년간 홈서버를 운영한 경험을 언급).
- VPS 대안. Vik는 당시에도 VPS(가상사설서버)를 빌려 오픈클로를 설치하는 방법이 있었다고 언급했다.
- Austin의 로컬 사용례. Austin은 자신도 로컬 "에이전트 컴퓨터"를 두고 오디오 전사·음성-텍스트 변환 같은 비프론티어(non-frontier) 소규모 작업을 돌리며, 이 팟캐스트를 뉴스레터에 올릴 때 그 로컬 박스에서 트랜스크립션을 처리한다고 밝혔다.
- 가격과 무관함 고지. Grok bot 가격은 월 200달러이며, Vik는 비싸서 대부분은 안 살 것 같다고 말했고 스폰서 관계가 아님을 명시했다.
- 통합 도구. Grok bot은 구글 캘린더·구글 드라이브·Canva·Figma 등의 통합을 설치 시 선택만 하면 자동으로 연결해준다고 Vik가 설명했다.
- 천재-비서 비유의 시작. Austin은 GPU를 "모든 것에 박사학위를 가진 천재"로, CPU를 그 지시를 받아 실제 작업을 수행하는 "비서"로 비유했다.
- 호스트 노드 CPU. Vik는 GPU 바로 옆에서 다음 작업을 끊임없이 준비해 GPU가 쉬지 않게 만드는 역할을 "호스트 노드 CPU"라 불렀고, 코어 수보다 코어당 속도(빠른 응답성)가 중요하다고 설명했다.
- 코히어런트 호스트. Austin은 코히어런트(coherent) 호스트의 예로 Grace Blackwell(칩투칩 C2C 프로토콜)을 들었다 — 메모리 코히런시가 있으면 비서(CPU)가 천재(GPU)의 "메모"를 직접 볼 수 있다고 비유했다.
- HBM 비유. Vik는 HBM을 "천재 책상 옆에 쌓인 서류더미"에 비유했다 — 자리에서 일어나지 않고 바로 쓸 수 있는 데이터이며, 코히런시가 있으면 비서(CPU)도 같은 서류더미에 접근할 수 있다고 설명했다.
- 에이전틱 CPU 개념. 호스트 노드 CPU가 GPU를 먹이는 데만 집중해야 하므로, 코드 컴파일·웹 검색·SEC 파일링 조회 같은 "여분의(spillover)" 작업은 별도의 CPU 랙이 전담해야 한다는 논의가 이어졌다 — 이를 "에이전틱 CPU"라 부른다고 Vik가 정리했다.
- AMD와의 대화. Austin은 최근 AMD와 진행한 팟캐스트에서도 비슷한 프레이밍(에이전틱 CPU)에 공감했다고 언급했다.
- 사무실 비유. Vik는 128코어 CPU를 "사무실 층별 배치도"에 비유했다 — 예를 들어 4코어씩 재무팀·리서치팀·시설팀으로 나눠 각 "부서"가 병렬로 작업을 수행하는 그림이다.
- 코어 수 사례. AMD 256코어, 인텔 288코어 CPU가 언급됐다 — 코어 수가 많을수록 "부서"를 더 크게 꾸릴 수 있지만, 코어별 성능(싱글코어 성능)도 여전히 중요하다고 Vik가 짚었다.
- 호스트 CPU 재활용. Austin은 호스트 CPU가 (예시로) 88코어급이지만 매우 빠른 코어로 GPU를 먹이는 데 특화돼 있고, 이를 에이전틱 용도로 재활용할 때는 코어 수를 128·256·288·512로 늘리는 게 나을 수도 있다고 언급했다.
- 코어당 비용. Vik는 이제 문제는 "직원 한 명당 비용"이라며, 코어를 얼마나 확보할 수 있고 그 "직원"이 얼마나 비싼지가 중요하다고 정리했다.
- 인텔 P-랙·E-랙. 인텔이 지난여름 에이전틱 AI용으로 P-랙과 E-랙을 각각 출시했다고 Austin이 언급했다 — 워크로드에 따라 성능 특화형·효율(코어 수) 특화형 랙을 나눈 사례다.
- Cerebras 랙 스케일 발표. Vik는 녹음 전날 Cerebras가 새로운 랙 스케일 솔루션을 발표했다고 언급했다 — 기존에 웨이퍼 스케일 칩으로 알려졌던 Cerebras가 랙 단위를 새로운 연산 단위로 제시했다는 것이다.
- 천재의 성격 구분. Vik는 Cerebras급을 아주 빠르지만 컨텍스트(기억)가 짧은 천재, 대형 HBM 기반 가속기를 좀 더 범용적이고 컨텍스트가 큰 천재, 그리고 답이 늦어도 되는 과학·의료 문제용으로 느리게 오래 생각하는 천재로 나눠 설명했다.
- 오케스트레이션 부재. Austin은 CPU·GPU를 아우르는 상위 오케스트레이션 소프트웨어가 아직 부족하다고 문제를 제기했고, Nvidia Dynamo는 GPU("천재") 성능을 끌어올리는 데 집중할 뿐 그 오케스트레이션 계층은 아니라고 지적했다.
- Modular 언급. Vik는 Modular를 예로 들며 Mojo 언어로 CPU·GPU 모두에서 실행 가능한 코드를 쓸 수 있다고 언급했지만, 오케스트레이션 세부 기능은 아직 잘 모른다고 밝혔다.
- Gimlet Labs 사례. Austin은 5월경 진행한 팟캐스트에서 Gimlet Labs가 뉴클라우드로서 다양한 하드웨어에 걸쳐 작업을 스케줄링해 비용을 낮추는 방향을 연구 중이라고 들었다고 전했다.
- Grok bot VM의 위치. 결론적으로 Grok bot의 VM은 "범용 CPU" 위에서 동작한다 — VM 자체는 운영체제 역할만 하고, 거기서 파생된 에이전트들이 GPU("천재")와 호스트 노드 CPU("비서")에 접근한다는 그림이다.
- 수요 규모 사고실험. Austin은 1천만 명이 이런 도구를 쓰고 VM당 100개 에이전트를 돌린다고 가정하면, 단순 계산으로 10억(1 billion) 코어 수요까지 상상할 수 있다고 말했다.
- 마무리 요청. Austin은 Anthropic·OpenAI가 실제로 에이전틱 CPU와 범용 CPU에 작업을 얼마나 나눠 쓰는지 공유해줬으면 좋겠다고 청취자에게 요청하며 마무리했다.

## 숫자 (원문에 나온 것만)
- 월 200달러 — Grok bot 가격
- 2025년 12월 — 에이전트(오픈클로 등)가 처음 등장한 시점
- 2026년 2월 — 인텔이 실적발표에서 CPU 수요 급증을 언급한 시점
- 10년 — Vik의 홈서버 운영 경력
- 88코어 — Austin이 예로 든 호스트 CPU 코어 수
- 128코어 — Vik의 "사무실 배치도" 비유에 쓰인 CPU 코어 수
- 256코어 — AMD CPU 예시
- 288코어 — 인텔 CPU 예시
- 512코어 — Austin이 언급한 에이전틱 CPU 확장 예시
- 1,000만 명 — Austin이 가정한 Grok bot류 도구 사용자 수(사고실험)
- VM당 100개 에이전트 — Austin이 가정한 값(사고실험)
- 10억 코어 — 위 두 가정을 곱한 Austin의 어림 수요 추정치(사고실험, 실측 아님)

## 그대로 인용 (영어 원문 + 한국어 옮김)
- "You think about it like an open claw, but extremely easy to use so that everybody can run agents all the time right now, even if your computer is closed." — Vik. "오픈클로 같은 거라고 생각하시면 되는데, 훨씬 쓰기 쉬워서 컴퓨터를 꺼놔도 지금 당장 누구나 에이전트를 항상 돌릴 수 있어요."
- "The GPU is the genius." — Austin. "GPU가 바로 그 천재예요."
- "the CPU as the assistants that once told what to do, they can go carry out all the work that the genius told them to do." — Austin. "CPU는 비서들이에요. 뭘 하라고 지시받으면, 천재가 시킨 그 모든 일을 나가서 처리하는 거죠."
- "HBM will be the stack of papers on the desk, and the genius can just take it and keep working on it." — Vik. "HBM은 책상 위에 쌓인 서류더미인 셈이에요. 천재는 그걸 그냥 집어서 계속 작업하면 되고요."
- "I think 10 million people doing this is not crazy. And that could be 10 million VMs running on 10 million cores in the cloud." — Austin. "1천만 명이 이걸 한다는 게 말이 안 되는 얘기는 아니라고 봐요. 그러면 클라우드에서 1천만 개 코어로 돌아가는 1천만 개 VM이 있을 수 있는 거죠."
- "It's about the cost per employee now. How many cores can you get and how expensive is each employee in that floor plan?" — Vik. "이제는 직원 한 명당 비용의 문제예요. 그 사무실 배치도에서 코어를 얼마나 확보할 수 있고, 직원 한 명이 얼마나 비싼지가 관건이죠."

## 주의
- "10억 코어" 수요는 Austin이 1천만 사용자·VM당 100 에이전트를 임의로 가정해 곱한 사고실험이며, 실측치나 업계 전망치가 아니다.
- Grok bot의 세부 기술 사양(어떤 CPU·리전에서 VM이 도는지 등)은 두 진행자도 직접 확인한 것이 아니라 사용 경험을 바탕으로 추정한 내용이다.
- 전사 텍스트는 Substack 페이지에서 자동 추출한 것으로 화자 태그("Vik:", "Austin:")는 원문 그대로이며, 문장부호 오인식은 없었다.
