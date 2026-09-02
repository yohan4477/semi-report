# CLAUDE.md

## 이 저장소

반도체·AI 인프라(SemiAnalysis)와 제3자 해설(언더스탠딩·미주사·부동산)을 한국어로 옮기고, 문서를 가로질러 나온 판단을 대시보드로 내보낸다. 산출물은 코드가 아니라 **글**이다.

```
① 원문   content/newsletter/**  content/understanding/**  content/epoch/**  input/clippings/**
② 노트   insights/notes/*.md              화면에 안 나온다. 교차 작업용 중간물
③ 포스트 insights/synth/cross-*.md        교차 인사이트
          insights/briefs/*-지금-상태.md   현황 브리핑
④ 화면   대시보드/*.html                   생성물. 손으로 고치지 않는다
```

설계 SSOT는 `docs/superpowers/specs/2026-08-09-원문-기반-노트-체계-design.md`. 원자(atom) 체계는 폐기됐다 — `check_atoms.py`·`crosscheck.py`·`insights/atoms/`를 부르는 지시는 낡은 것이다.

## 반드시 지킬 것

**글과 그림을 새로 쓰거나 고칠 때는 `docs/글과 도해 — 확정 규칙.md`를 따른다**(2026-09-02 확정). 독자는 뉴스를 따라가는 사람, 자세는 의뢰인 없는 애널리스트, 도구 이름(MECE·프로세스·밸류체인·대비)은 글에 안 쓰고, 5,500~6,500자, 표가 산문을 되풀이하면 표를 걷고, 어려운 대목은 그림으로(한 절에 여럿 가능, 모듈로, 견줄 때는 같은 꼴, 색은 회색만), 번역체 낱말(값이 움직인다·열린다·몫·단)은 바꾼다. 다른 규칙 문서·스킬의 옛 꼴(앞머리 물음·바탕·축, 목차 두 칸, 방법 표기, so-what, 한계 절, 성격 열)과 어긋나면 **확정 규칙이 이긴다** — 각 장의 규칙 문서는 고칠 때 이쪽으로 맞춘다. 화면은 Playwright 스크린샷으로, 라이브는 깨끗한 체크아웃 빌드로 확인한다.

**스킬을 여는 자리 — 예외 없다. 한 장만 손대도 같다.**

```
③ 포스트 본문 쓰기·고치기             insight-review   겹침·자기 사례 덮기는 이 절차로만 걸린다
② 노트 새로 만들기                   insight-note
제3자 요약을 대시보드 카드로           insight-upload
원문에서 이름 찾기                    entity-search    grep 대신. 별칭·영문 표기를 사전이 알고 영수증이 붙는다.
                                                     개념으로 묻는 물음은 못 찾는다
Epoch AI 글(epoch.ai/gradient-updates) epoch-gradient   링크 하나로 요약·도해·카드·검사·푸시까지. 도해는 PNG 아닌 한국어 SVG
통합 보고서(대시보드/통합 보고서.html) insight-report   새 층은 카드가 아니라 각도에서 세운다 — structure A 로 가르고 여러 편에
                                                     걸친 주체만 남겨, 편마다 어느 자리에 서는지를 절로. 첫 실물 sec-fund(08-28)
절이 여섯을 넘는 글                   doc-structure    비교표에는 「언제 것 · 성격」 열 — 없으면 공표치와 추정치가 같은 무게
카드에 도해 붙이기·고치기             insight-figure   「없는 값을 그렸다」로 무너진다. 배치는 scratchpad/check_fig.py
구조화(원문 각도 A · 케이스 구조 B)    structure        원문이 먼저면 A, 물음이 먼저면 B, 둘 다면 A 산출을 B 재료로.
                                                     레인 파일 둘(references/원문-각도.md·케이스-구조.md)을 같이 열지 않는다
건강 인사이트(🩺)                     health-insight   카드 단위가 주제, 본문에 해부도
```

**각도는 아직 노트를 대신하지 못한다** — 고르는 데는 빠른데 세우는 데는 줄 번호와 저자 논지가 모자란다(2026-08-28 실험, 원문을 여덟 번 열었다). 각도에 줄 번호 칸·「저자 논지」 절·도해 표시가 다 들어오기 전까지 교차 카드는 노트와 함께 쓴다. 진행은 `check_angles` A7·A8.

## 검사기

```bash
PYTHONIOENCODING=utf-8 python insights/check_notes.py   # 노트·인용 무결성
PYTHONIOENCODING=utf-8 python insights/check_prose.py   # 문체·용어·절 순서 (대시보드 HTML 포함)
PYTHONIOENCODING=utf-8 python insights/check_read.py    # 읽히는가
PYTHONIOENCODING=utf-8 python insights/check_cite.py    # 인용한 줄에 그 숫자가 있나
PYTHONIOENCODING=utf-8 python insights/check_fresh.py   # 아직 지금 이야기인가
PYTHONIOENCODING=utf-8 python insights/check_report.py  # 보고서 숫자가 원문에 있나
PYTHONIOENCODING=utf-8 python insights/check_index.py   # 색인 주소가 맞나, 색인이 낡지 않았나
PYTHONIOENCODING=utf-8 python scripts/check_deps.py    # 추적된 코드가 부르는 파일이 추적되나
PYTHONIOENCODING=utf-8 python insights/check_val.py     # 숫자 파이프라인 — 조정 표·기간 정합·박아 둔 상수
PYTHONIOENCODING=utf-8 python insights/check_debate.py   # 쟁점 — 화자 말과 진행자 말이 섞였나
PYTHONIOENCODING=utf-8 python insights/check_angles.py  # 각도 — 대상이 사전 정본인가, 성격이 여덟에 드나
PYTHONIOENCODING=utf-8 python insights/check_figval.py # 도해에 든 값이 원문에 있나 (확인 필요만 센다)
PYTHONIOENCODING=utf-8 python insights/check_struct.py # 구조 — 앞머리·목차·물음 절·성격 열이 서 있나
PYTHONIOENCODING=utf-8 python insights/check_frame.py # 프레임 — 남의 모델이 준 틀에서 원문 밖 주장이 카드로 샜나
PYTHONIOENCODING=utf-8 python insights/check_watch.py # 워치 — 문턱이 신호인가, 어댑터가 내는 열쇠인가
PYTHONIOENCODING=utf-8 python insights/check_watch.py --selftest # 그 규칙들이 결함을 실제로 무는가
```

FAIL 0이어야 푸시한다. **전부 돌린다 — 일부만 돌리지 않는다.** 앞의 셋만 돌리고 푸시한 날(2026-08-15) `check_fresh` FAIL 3건·`check_cite` 확인필요 6건이 그대로 나갔다. 콘솔이 cp949라 `PYTHONIOENCODING=utf-8`을 붙인다.

- `check_struct`는 구조 규칙(S9~S13·F1~F3, 표는 `docs/CLAUDE.md 에서 옮긴 규칙 — 2026-09-02.md`)을 기계가 보는 자리다. 게이트는 `STRICT`에 적은 장뿐, 나머지 장은 장별 빚 한 줄로 센다(AI Engineer 68편은 소급 보류). 그 장의 꼴에 아예 안 맞는 규칙은 `SKIP`. 안 읽히는 경고는 소음이라 WARN 층은 걷었다(2026-08-30, 529건 중 513건이 한 장).
- `check_watch`는 문턱이 신호인지를 이력으로 잰다(W8~W11, 같은 문서). **문턱은 사람이 정한다** — 구마다 변동폭이 달라 한 꼴을 다 걸면 어디선 0회, 어디선 매달 걸린다. 검사기는 몇 번 걸렸는지만 말한다.
- **규칙을 세울 때는 결함을 넣어 무는지 먼저 본다.** S12는 「번호가 하나라도 있으면 통과」로 ①만 남긴 문단을 지나쳤고, S3은 목차 상자를 본문으로 세어 「물총새」를 통과시켰다.
- 산문 검사기는 산문만 본다. 밸류에이션 결함(기저 오지정·날짜 혼합·박아 둔 할인율·부호 뒤집힘·주식보상 가산)은 `check_val`이 막는다 — 판단은 `insights/valuation/adjust.py` 표에 줄로 세우고 검사기는 그 표만 읽는다.

## 글 규칙

- **글은 구조다, 나열이 아니다.** 절 이름이 정해진 갈래가 먼저다 — 교차 인사이트는 `check_prose`의 `SECTION_ORDER` 일곱 절, 대시보드 카드는 `card_lib` 스키마(points·clash·figs). 거기서는 절 이름을 물음으로 바꾸지 않는다. 앞머리·각도·목차·절·대비·값·도해·끝의 상세는 `doc-structure` 스킬과 `docs/CLAUDE.md 에서 옮긴 규칙 — 2026-09-02.md` §1 (확정 규칙과 어긋나면 확정 규칙).
- **한줄 코멘트는 결론만.** 물음·바탕·축은 본문 맨 위 앞머리 상자(`('lead', …)`)에.
- **번호는 층마다 다르다.** 단원은 「1. 2. 3.」(`card_lib.toc_html`이 붙인다, 손으로 안 적는다), 그 아래 절과 나열은 ①②③. 「첫째·둘째」는 안 쓴다.
- **도해는 그 절의 글보다 앞에.** 원문에 없는 값은 안 그린다.
- **용어는 남기고 첫 등장에 괄호로 푼다.** 쉬운 말로 치환하지 않는다(지웠다가 되돌린 이력 있음). 별도 「용어」 절로 몰지 않는다 — 예: HBC(고대역폭 컴퓨트 — 연산 다이 위에 메모리를 쌓는 방식).
- **대시보드 산문도 같은 규칙.** `check_prose`가 `대시보드/*.html`까지 본다. 금지어 목록 대신 밀도를 본다 — 대시(P8)·「A가 아니라 B」 대구(P9)·볼드(P10), **1천자당**으로 잰다. 뜻이 안 닿는 자리(P12 무엇을 먹는지 안 밝힌 조건절·P13 숫자 없이 정도만 말하는 주장)는 WARN.
- **「돈을 댄다」로 뭉개지 않는다.** 빌려준다·낸다·건다·마련한다로. P18 FAIL. 번역투 낱말 넷(P4)도 같다. **인용 안은 안 본다** — 고칠 수 없는 자리다.
- **은유를 주어 자리에 두지 않는다.** 매출인지 주문인지 이익인지, 누구 것인지를 이름으로 댄다. 은유를 다른 은유로 바꾸는 것은 수정이 아니다. P14 FAIL.
- **다 쓰고 나면 원문과 대조한다.** 쓰는 동안에는 못 본다. 절마다 원문 줄을 다시 열어 ① 값이 그 줄에 있나 ② 원문이 안 한 말(반례·일반화·인과)을 했나 ③ 낱말을 바꿔 뜻이 좁아졌나. `check_cite`는 ①만 본다.
- **일반론 금지.** 숫자·명명된 주체·비직관적인 것으로 쓴다.
- **회계·금융은 돈이 움직이는 순서로.** 조문·용어 나열 대신 언제 장부에 잡히고 언제 정산되는지 — `korean-readability` 「1-B」. 문체·이해도 규칙도 그 스킬.
- **「번역투 고쳐」에 재작성으로 답하지 않는다.** 표지를 재고(스킬 §6-1) 걸린 문장만 고친다. 통째 재작성은 빈 수사를 없던 주장으로 바꾼다 — 논리구조가 망가지는 원인.
- **다른 모델의 답은 재료가 아니라 프레임 후보다.** `insights/frames/*.md`에 원본 그대로, 카드로는 원문이 받쳐 주는 것만, 안 가져온 것은 `named:`에 이름만. `check_frame` F2. 물을 때는 유료든 무료든 **원문 전문**을 보내고(2026-08-31, 요약본은 우리 선택을 되풀이한다) 무엇을 보냈는지 frontmatter `source`에 남긴다.

## 작업 관례

- 의미 단위마다 바로 커밋·푸시한다. 단계마다 승인을 묻지 않는다 — 의미 단위 끝에 한 번 보고.
- **퀄리티가 유지되는 일은 하위 모델에 위임한다** — 메인 컨텍스트를 원문 덩어리로 안 채우는 것이 큰 이유다. 기계적 편집은 haiku, 원문을 읽어 요약·변환은 sonnet, 판단이 산출물인 일(본문·검사 규칙·설계·리뷰)은 메인. 위임문에 지킬 규칙(금지어 변형 금지 등)을 명시하고 결과는 검사기로 확인.
- 대시보드 HTML은 생성물. 고칠 것은 `insights/` 원본과 `insights/gen_*.py`.
- **대시보드 첫 화면은 어느 장이든 섹션 타일.** 관문 버튼 없음, 타일은 롤업보다 위. 조립은 `scratchpad/dash_common.py`의 `render()`만, 규약은 같은 파일 `check_ui()`.
- **워치(감시 장)는 아카이브 부품을 안 쓴다.** 접힘·타일·카드 없음, 「지금 걸린 것」이 맨 위, 값에 「언제 것」. 조립은 `scratchpad/gen_watch_page.py`, 규약은 같은 파일 `check_ui()`. 본 장은 매달 보는 것만(도해 하나·표 셋 예산), 줄마다 상세는 `대시보드/watch/<줄>.html`. 규약을 우회하려고 나온 장이 규약 없는 장이 되면 다음 사람이 같은 자리를 다시 판다.
- **카드를 다른 회사 이름 아래 두지 않는다.** 여러 주체면 라벨을 넓히거나(「반도체 3사」) 주제 라벨로. `dash_common.check_labels()`가 막는다 — 섹션을 먼저 세우고 카드를 맞추는 순서가 사고의 원인.
- **분석도 보고서도 하는 일은 쪼개기 하나다.** 방법·MECE·깊이·뷰 고르기는 `docs/쪼개기 — 원문 분석과 보고서 작성.md`. 한 노드는 한 방법으로만, 쪼개는 법에 정해진 목록은 없다.
- 장별 규칙 문서를 그 장을 고치기 전에 읽는다 — AI Engineer `docs/AI Engineer 대시보드 — 만드는 규칙.md`, 회계사 `docs/회계사 대시보드 — 만드는 규칙.md`.
