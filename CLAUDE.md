# CLAUDE.md

## 이 저장소

반도체·AI 인프라(SemiAnalysis)와 제3자 해설(언더스탠딩·미주사·부동산)을 한국어로 옮기고, 문서를 가로질러 나온 판단을 대시보드로 내보낸다. 코드가 아니라 **글**이 산출물이다.

```
① 원문   content/newsletter/**  content/understanding/**  input/clippings/**
② 노트   insights/notes/*.md              화면에 안 나온다. 교차 작업용 중간물
③ 포스트 insights/synth/cross-*.md        교차 인사이트
          insights/briefs/*-지금-상태.md   현황 브리핑
④ 화면   대시보드/*.html                   생성물. 손으로 고치지 않는다
```

설계 SSOT는 `docs/superpowers/specs/2026-08-09-원문-기반-노트-체계-design.md`. 원자(atom) 체계는 폐기됐다 — `check_atoms.py`·`crosscheck.py`·`insights/atoms/`를 부르는 지시가 있으면 그게 낡은 것이다.

## 반드시 지킬 것

**③ 포스트 본문을 쓰거나 고치기 전에 `insight-review` 스킬을 연다.** 예외 없다. 한 장만 손대는 경우도 마찬가지다 — 그 한 장이 다른 카드와 겹치는지, 주장이 자기 사례를 덮는지는 스킬의 절차로만 걸린다.

② 노트를 새로 만들 때는 `insight-note`, 제3자 요약을 대시보드 카드로 올릴 때는 `insight-upload`.

## 검사기는 다섯이다

```bash
PYTHONIOENCODING=utf-8 python insights/check_notes.py   # 노트·인용 무결성
PYTHONIOENCODING=utf-8 python insights/check_prose.py   # 문체·용어·절 순서 (대시보드 HTML 포함)
PYTHONIOENCODING=utf-8 python insights/check_read.py    # 읽히는가
PYTHONIOENCODING=utf-8 python insights/check_cite.py    # 인용한 줄에 그 숫자가 있나
PYTHONIOENCODING=utf-8 python insights/check_fresh.py   # 아직 지금 이야기인가
```

FAIL 0이어야 푸시한다. **앞의 셋만 돌리지 않는다** — 2026-08-15에 그렇게 푸시해서 `check_fresh` FAIL 3건과 `check_cite` 확인필요 6건이 그대로 나갔다.

콘솔이 cp949라 파이썬 실행에 `PYTHONIOENCODING=utf-8`을 붙인다.

## 글 규칙

- **용어는 남기고 첫 등장에 괄호로 푼다.** 쉬운 말로 치환하지 않는다. 지웠다가 되돌린 이력이 있다
- **대시보드 산문도 같은 규칙이다.** `check_prose`가 `대시보드/*.html`까지 본다. 금지어 목록은 2026-08-17에 걷어냈다. 대신 밀도를 본다 — 대시 개수(P8), 「A가 아니라 B」 대구(P9), 볼드 밀도(P10), 한 문장 속 절 개수(P11). 전부 WARN이니 숫자를 줄이는 건 사람 몫이다
- **일반론 금지.** 숫자·명명된 주체·비직관적인 것으로 쓴다
- **회계·금융은 돈이 움직이는 순서로.** 조문 번호와 용어를 늘어놓지 않는다. 언제 장부에 잡히고 언제 정산되는지, 어긋나면 어느 숫자가 움직이는지를 문장으로 쓴다 — `korean-readability` 「1-B」
- 문체·이해도 규칙은 `korean-readability` 스킬
- **「번역투 고쳐」에 재작성으로 답하지 않는다.** 먼저 표지를 재고(스킬 §6-1), 걸린 표지가 든 문장만 고친다. 문단 통째 재작성은 빈 수사를 없던 주장으로 바꾼다 — 논리구조가 망가지는 원인이 이것이다

## 작업 관례

- 의미 단위마다 바로 커밋·푸시한다. 몰아서 하지 않는다
- 단계마다 승인을 묻지 않는다. 판단해서 진행하고 의미 단위 끝에 한 번 보고한다
- 대시보드 HTML은 생성물이다. 고칠 것은 `insights/` 아래 원본과 `insights/gen_*.py`
- **대시보드 첫 화면은 어느 장이든 섹션 타일이다.** 그 앞에 관문 버튼을 두지 않는다 — 성격이 다른 글도 타일 하나로 넣는다. 조립은 `scratchpad/dash_common.py`의 `render()`만 거치고, 규약은 같은 파일 `check_ui()`가 검사한다
