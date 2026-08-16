---
name: insight-note
description: 원문 1편을 노트 1장으로 만들어 인사이트 체계에 넣는다. "이 문서 노트화해" / "노트 만들어" / 변환·클리핑을 막 끝낸 문서가 insights/notes/에 아직 없을 때 쓴다. 문서를 가로지르는 판단(교차·대조)은 하지 않는다 — 그건 insight-review가 한다.
---

# 새 문서 노트화

설계 SSOT: `docs/superpowers/specs/2026-08-09-원문-기반-노트-체계-design.md`. 원자(atom) 체계는 폐기됐다 — `insights/atoms/`·`check_atoms.py`·`views/process.json`·`insight-atomizer` 에이전트는 없다.

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 파이썬 실행에 `PYTHONIOENCODING=utf-8`을 붙인다.

## 원칙

**문서 하나에 노트 하나.** 압축을 두 번 하지 않는다. 여러 문서를 한 노트에 눌러 담으면 요약의 요약이 되고, 그게 원자 체계를 폐기한 이유다.

**노트는 문서가 말한 것만 담는다.** 티커·수혜/피해·전망은 서술(`insights/synth/`)에서 한다.

## 1. 대상 확인

```bash
PYTHONIOENCODING=utf-8 python insights/gen_manifest.py
ls insights/notes/ | grep <yymmdd>
```

이미 노트가 있으면 멈춘다 — 원문이 안 바뀌었으면 노트도 안 바뀐다. 원문이 바뀌었으면 `check_notes.py`의 N4 WARN이 그 사실을 알려 준다.

manifest에 원문이 없으면 여기서 멈추고 변환 파이프라인 쪽 문제로 보고한다.

## 2. 노트 작성

`insights/notes/<yymmdd>-<슬러그>.md`. 날짜는 원문 발행일이다.

```markdown
---
source: "content/newsletter/…/[YYMMDD] ….md"
title: "원문 제목"
date: YYYY-MM-DD
corpus: semi          # semi | und
lang: en              # en | ko
actors: [회사명, 회사명]
topics: [주제, 주제]
---

## 이 문서가 주장하는 것

(3~5문장. 요약이 아니라 논지다 — 이 문서가 무엇을 주장하려고 쓰였는지)

## 수치

- 값 · 조건 · 귀속 (라벨 L123)
  … 5~15개

## 저자가 추정이라고 밝힌 것

- … (라벨 L456)

## 이 문서가 반박하거나 뒤집는 것

- (다른 문서를 명시적으로 반박할 때만. 없으면 절을 빼도 된다)
```

**규칙**

- **조건 없는 수치는 적지 않는다.** 값만 있고 언제·어디서·누구 기준인지 없으면 나중에 서술에서 반대 결론이 나온다. N6가 FAIL로 잡는다
- **인용 라벨은 원문 파일명의 알아볼 수 있는 조각**이면 된다. `notes_lib`가 부분 일치로 푼다
- **3KB를 넘기지 않는다**(N5 WARN). 넘으면 서술 단계에서 원문을 다시 읽는 편이 낫다는 신호다
- `actors`·`topics`는 **이름만** 적는 얇은 색인이다. 해석을 담지 않는다
- 문장을 쪼개지 않는다. 논증이 살아 있어야 「왜 그렇게 말했나」가 남는다

**원문이 클 때는 위임한다.** 원문을 메인 대화로 끌어들이면 이후 교차 작업의 컨텍스트가 오염된다. 서브에이전트에 원문 경로와 위 형식을 주고 노트만 받는다. 사용자가 위임을 막았으면 직접 읽되 노트를 쓴 뒤 원문을 다시 참조하지 않는다.

## 3. 검사

```bash
PYTHONIOENCODING=utf-8 python insights/check_notes.py
PYTHONIOENCODING=utf-8 python insights/check_prose.py
```

`check_notes.py` FAIL 0이 되어야 한다.

| | 흔한 원인 | 처리 |
|---|---|---|
| N1 | `source` 경로 오타 | 경로를 고친다 |
| N2 | 라벨이 원문 파일명과 안 겹친다 | 라벨을 파일명 조각으로 바꾼다 |
| N3 | 줄 번호가 파일 범위 밖 | **손으로 맞추지 말고** 원문을 다시 열어 그 줄을 찾는다 |
| N6 | 수치에 조건이나 인용이 없다 | 조건을 채우거나 그 줄을 지운다 |

`check_prose.py` FAIL은 **용어를 지우지 말고 괄호로 푼다.** 이 저장소의 확정 규칙이다.

한 파일에 `check_prose` WARN이 5건을 넘으면 `humanize-korean` 스킬을 부를 계기다.

## 4. 커밋·보고

```bash
git add insights/notes/<파일> insights/manifest.json
git commit -F - <<'EOF'
feat(노트): <문서 제목> — 수치 N개

- corpus: semi / lang: en
- 검사기 FAIL 0

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
EOF
git push origin main
```

커밋 메시지의 수치는 검사기 출력에서 복사한다(눈으로 세지 말 것).

보고에 **다음 단계 안내**를 적는다 — 아래 중 하나면 `insight-review`를 돌려야 한다.

- 직전 리뷰 이후 새 노트가 3편 이상
- `check_fresh.py`가 F1 FAIL을 낸다(더 새 문서가 들어왔는데 서술을 안 고쳤다)
- 교차 인사이트를 새로 쓰거나 고치기 직전

## 하지 않는 것

- 서술(`insights/synth/`·`briefs/`·`tracks/`) 본문 수정
- 새 교차 인사이트 제안 — 대조는 `insight-review`가 한다
- 기존 노트 소급 수정
- 노트에 상업적 해석 넣기
