# Semi Doped 대시보드 — 만드는 규칙

글·도해·화면·확인 규칙은 **`docs/글과 도해 — 확정 규칙.md`** 가 정본이다. 이 문서는 그 규칙
위에 Semi Doped 장에만 해당하는 것을 적는다.

## 섹션

회차 요약본 frontmatter `section` 코드에 이름을 얹는다. 순서가 화면 순서다.

```
compute  추론 칩            link  네트워크        power  전력
mem      메모리             fab   공정·패키징·리소      news   시황·규제·자금
```
회차마다 한 자리. 두 갈래인 회차(메모리 실적·캡엑스는 메모리 대 시황, 컴퓨텍스는 전력 대 잇는 길)는
판이 서면 그 판의 절이 오래 다루는 쪽으로 다시 판다. 글이 있는 회차가 없는 섹션은 안 보인다 —
「0편」 머리줄은 「글 없음」과 같다. 머리줄에 「글 m편 / 회차 n편」. TIL·하루치 모음은 회차가
아니라 섹션에 안 넣는다.

목록 줄 — 날짜 옆에는 진행자 말고 다른 참가자(게스트·발표자)만 이름과 짧은 소개로. 진행자
둘뿐인 회차는 날짜만. 판이 선 것만 꼬리표로.

## 장의 꼴

회차 하나에 판이 둘 선다 — ⚖ 전략과 🔧 기술. 회차 목록 한 장과 회차마다 글 한 장. 접힘·타일·
카드 없음. 판은 다른 모델에게 **전사 전문**을 읽혀 받은 글이다. 화면 조립은
`scratchpad/gen_semidoped.py`, 도해는 `scratchpad/semidoped_figs.py`, 규약은 `check_ui()` 와
`check_scroll.js`, 차례 클릭 확인은 `shot_toc.js`.

## 전략 판

전략 컨설턴트 출신 애널리스트가 회차를 읽고 업계에 무엇이 보이는지를 쓴다. 글을 받는 프롬프트와
대조 프롬프트는 `scratchpad/semidoped_prompt_strategy.md` — `<slug>` 만 바꿔 그대로 쓴다. frontmatter —
slug · lane · persona · model · source · sent · date · title(결론 한 문장) · fixed(고친 것).

## 화자 줄

팟캐스트라 누가 말하는지가 먼저다. 회차 요약본 frontmatter `people` 에 「진행 … / 발표 …」로
적고 생성기가 회차 메타 아래에 낸다. 말한 사람만 — 진행자가 인용한 기사(SemiAnalysis)는
화자가 아니다. 전사에 진행자 소개가 없으면 이름과 「Semi Doped 공동 진행」만.

## 재료와 산출물

```
회차 메타·한 줄    content/understanding/Semi Doped/<slug>.md
전사(정본)        content/understanding/Semi Doped/raw/<slug>.md
받은 글           insights/semidoped/<slug>-strategy.md      (문장은 안 고친다. 값·귀속·번역체만 고치고 fixed 에 적는다)
도해              scratchpad/semidoped_figs.py                (열쇠 「절.」 또는 「절.|문단 앞머리」)
화면              대시보드/Semi Doped 대시보드.html · 대시보드/semidoped/<slug>.html
```

## 기술 판

나중에. 규칙은 첫 실물을 받은 뒤 적는다.

## 2026-09-02 에 있었던 일

첫 실물이 저장소 문서 꼴(앞머리·목차 두 칸·방법 표기·so-what·한계·성격 열·임팩트 표)을 그대로
씌운 판이었고, 읽는 사람이 「중복 많고 첫 판이 낫다」고 했다. 하루 동안 다시 받고 줄이고 그림을
아홉 장 그리며 나온 것을 확정 규칙으로 옮겼다. 같은 날 다른 세션의 반쪽 커밋으로 라이브 배포가
세 시간 멈춘 것도 그 문서 5절에 있다.
