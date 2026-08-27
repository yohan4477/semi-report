# AI Engineer 보고서 전환 — 남은 일 큐

이어서 할 때 이 파일부터 읽는다. 규격은 `scratchpad/aie_report_brief.md`(보고서 쓰는 법)와
`scratchpad/aie_factsheet_brief.md`(사실표 위임문 규격)에 있다.

## 현황 (2026-08-27)

**64 / 81 편 완료.** 섹션별로는 이렇다.

| 섹션 | 상태 |
|---|---|
| agent | 31/31 완료 · 갈래 다섯 붙임 |
| eval | 17/17 완료 · 갈래 다섯 붙임 |
| infra | 12/12 완료 · 갈래 넷 붙임 |
| code | 2/6 |
| rag | 2/6 |
| voice | 0/4 |
| train | 0/3 |
| product | 0/2 |

## 남은 17편

사실표가 이미 있는 둘은 바로 쓰면 된다.

| 섹션 | 영상 ID | 사실표 | 제목 첫머리 |
|---|---|---|---|
| rag | B9h9ovW5H9U | **있음** | 문서가 아니라 결정의 … |
| rag | c5qJHr3DnT4 | **있음** | 그래프RAG로 컨텍스트 … |
| rag | ROfHHJmumcc | 없음 | 데이터가 차이를 만든다 … |
| rag | -tgQa8Fzf80 | 없음 | 지식그래프 RAG, 언제 … |
| code | IddXPepIAS4 | 없음 | AI 인턴에게는 고삐가 … |
| code | Lue8K2jqfKk | 없음 | 모델은 지수로 크는데 … |
| code | WE_Gnowy3uw | 없음 | 1만 5천 줄짜리 워크트리 … |
| code | imFedndyXYQ | 없음 | 취약점 찾기는 쉬워졌다 … |
| voice | Bc6Ojl2XS1w | 없음 | 제미나이 오디오 스택 … |
| voice | GIRpQEfYf3U | 없음 | 무엇이든 무엇으로 … |
| voice | knH3fmGAteQ | 없음 | 밀리초 안에 답하라 … |
| voice | xOP1PM8fwnk | 없음 | 디퓨전은 결국 압축과 … |
| train | 8EQo4J2BWKw | 없음 | 병목을 풀 때마다 똑똑 … |
| train | k35LeKZEhiE | 없음 | 일하면서 배우는 에이전트 … |
| train | p1CmPZ2j6Lk | 없음 | 프롬프트로 안 풀리면 … |
| product | NKwIX3CiRgU | 없음 | 생성AI 에이전트, 데이터 … |
| product | fgkXEIbZpGc | 없음 | 프롬프트 하나로 앱을 … |

## 한 편을 처리하는 순서

1. **사실표가 없으면 먼저 위임한다.** sonnet 하위 에이전트에 한 편씩, 한 번에 셋까지.
   위임문은 `aie_factsheet_brief.md`를 읽으라고 시키고 금지 사항(판단 금지·인용 필수·
   개수 지어내기 금지·발표자가 스스로 밝힐 때만 이름)을 본문에 다시 적는다.
   결과는 `scratchpad/aie_facts/<영상ID>.md`.
2. 사실표를 읽고 **도해 둘을 먼저 고른다.** `scratchpad/aie_figs.py`의 `RFIGS`에 넣는다.
   `_pair`는 `<div class="rfig">`로 직접 감싸야 한다(안 감싸면 도해가 통째로 안 나가고
   생성기는 경고도 안 낸다 — 실제로 한 번 놓쳤다).
3. 본문을 쓴다. 프런트매터에 `format: report`를 넣고 `gain`을 새로 쓴다.
4. `PYTHONIOENCODING=utf-8 python scratchpad/gen_aie_dashboard.py` — 경고 줄(`^  !`)을 본다.
   용어 별표를 안 붙였으면 여기서 걸린다.
5. 검사기: `check_fig.py`, 그리고 `insights/`의 `check_prose`·`check_read`(FAIL 0이어야 한다).
6. 브라우저로 잰다. 아래 「재는 법」 참조.
7. `git commit -- <경로들>`로 커밋하고 푸시한다.

## 지킬 것

- **도해는 한 편에 둘까지.** 목록이면 도해가 아니라 표로 낸다.
- 도해는 SVG가 아니라 HTML. 글자는 본문과 같은 `.95rem`(15.2px)이어야 하고
  295·520·776px에서 가로 넘침이 0이어야 한다.
- 용어는 쉬운 말로 바꾸지 않는다. **별표를 단어 앞에 붙이고 맨 아래 `용어` 블록에서 푼다.**
  프런트매터에는 별표를 넣지 않는다.
- 마지막 절은 언제나 **「발표가 밝히지 않은 것」**이다. 잰 값이 없으면 없다고 쓴다.
- 발표자가 자막에서 스스로 이름을 대지 않으면 본문에 이름을 쓰지 않는다.
- 자막이 숫자·이름을 뭉갠 자리는 그대로 「원문에서 갈린다」고 적는다.
- 발표가 스스로 밝힌 실패(데모 실패, 녹화 대체, 오타, 미공개)는 빠뜨리지 않는다.

## 재는 법 (브라우저)

`file://`은 막혀 있다. 로컬 서버로 띄운다.

```bash
cd C:/Users/y/semianalysis && (python -m http.server 8731 --bind 127.0.0.1 >/dev/null 2>&1 &)
```

그다음 `http://127.0.0.1:8731/대시보드/AI%20Engineer%20대시보드.html`을 열고,
카드를 `.ucard`에서 제목으로 찾아 `.uc-rep`의 너비를 295·520·776으로 바꿔 가며
`scrollWidth - clientWidth`와 `.rfig` 안 글자 크기를 잰다.

## 섹션이 끝나면

그 섹션 카드를 갈래로 나누고 읽는 차례를 세운다. `gen_aie_dashboard.py`의 `TRACKS`에
`{섹션 열쇠말: [(갈래 이름, 한 줄, [영상 ID …]), …]}`로 넣으면 섹션 머리에 접히는
「읽는 차례」가 서고 **카드도 그 차례로 정렬된다**(날짜순이 아니다).
목록에 없는 ID를 적으면 생성이 멈춘다.

## 이 저장소를 나눠 쓰는 중

다른 세션이 같은 저장소에서 일한다. **`git add -A`를 쓰지 않는다.**
인덱스에 남의 작업이 올라와 있을 수 있으므로 `git commit -m … -- <경로>`로 경로를 찍어
커밋한다. 실제로 한 번 남의 커밋에 이쪽 파일이 섞여 들어간 적이 있다.
