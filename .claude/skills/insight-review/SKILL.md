---
name: insight-review
description: 문서가 쌓인 뒤 인사이트 체계를 점검한다 — 검사기·문체 게이트, 대조(STALE·충돌 후보·문서 내부 충돌·뭉침), 구조 의미 중복제거, 좌표 승격 후보 보고까지. "인사이트 리뷰해" / "쌓인 문서 점검해" / 인사이트를 새로 쓰거나 고치기 직전에 쓴다. 원자를 만들지 않고 인사이트 본문도 고치지 않는다.
---

# 인사이트 리뷰

선행 설계: `docs/superpowers/specs/2026-07-30-원자-뷰-인사이트-design.md`(체계), `2026-07-30-스킬-분할-구조화-design.md`(이 절차).

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 파이썬 실행에는 `PYTHONIOENCODING=utf-8`을 붙인다.

## 언제 도나 (셋 중 하나)

- 직전 리뷰 이후 원자화된 문서가 **3편 이상**
- `check_atoms.py`의 **STALE(C11) WARN이 1건 이상**
- **인사이트를 새로 쓰거나 고치기 직전** — 문서 수와 무관하게 돈다. 충돌 후보를 모르고 쓰면 C9가 나중에 FAIL을 낸다

## 1. 검사

```bash
PYTHONIOENCODING=utf-8 py insights/check_atoms.py
PYTHONIOENCODING=utf-8 py insights/check_prose.py
```

둘 다 FAIL 0이어야 한다.

- `check_atoms.py` FAIL이면 여기서 멈추고 원자화 쪽 문제로 보고한다. 줄 번호를 손으로 맞추지 말고 그 문서를 재추출한다(C16이 원문 변경을 잡는다)
- `check_prose.py` FAIL이면 **용어를 지우지 말고 괄호로 풀어** 고친다. 이 저장소의 확정 규칙이다 — 용어를 없앴다가 되돌린 이력이 있다
- 절 순서를 바꾸면 **첫 등장 위치가 이동해 P2가 새로 뜬다.** 실측된 현상이니 놀라지 말고 새 첫 등장에서 풀면 된다

## 2. 대조

```bash
PYTHONIOENCODING=utf-8 py insights/crosscheck.py
```

네 가지가 나온다.

- **뭉침** — 원자 10개 이상인 칸. 한 문서가 60%를 넘으면 쪼개지 않는다(그 문서의 목차다). 비중이 흩어진 칸만 하위 단계 후보
- **STALE 인사이트** — 처리 4갈래: 뒷받침(`atoms:`에 id 추가) / 조건 다름(`## 조건 충돌` 갱신) / 뒤집음(`## 주장` 재작성, 이전 판단은 무너진 이유와 함께 보존) / 무관(`dismissed:` + `## 검토 후 무관` 절)
- **문서 내부 충돌** — 같은 문서 안에서 같은 단위·다른 조건인 쌍. 이 체계를 만든 5.4배 사고가 이 유형이다
- **충돌 후보** — 다른 문서와의 쌍. 한 인사이트에서 함께 인용하면 C9가 FAIL

## 3. 구조 의미 중복제거

```bash
PYTHONIOENCODING=utf-8 py insights/structures.py
```

기록 검증(오류 0건)과 1차 겹침(라벨 Jaccard)을 본다. **라벨 겹침은 거의 0으로 나온다** — 실측에서 구조 38개 중 0쌍이었고 문턱 0.15까지 낮춰도 0이었다. 리포트마다 자기 어휘로 틀을 만들기 때문이다. 버그가 아니다.

그래서 의미 묶기는 직접 한다. `insights/views/structures.json`을 **전수 읽고**(라벨만 담아 짧다) 같은 것을 말하는 구조를 묶어 `insights/views/structure_groups.json`에 쓴다. 형식은 그 파일의 기존 항목을 그대로 따른다 — `name`·`kind`·`members`·`shared_order`·`note`·`docs`·`promote`·`promote_note`.

**규칙**
- **멱등**: 기존 묶음은 유지하고 새 구조만 배치한다. 묶음 이름을 바꾸는 것은 스펙 개정으로 본다
- `members`가 **2편 이상**이어야 승격 후보다. 단독 구조는 그 문서의 목차이므로 묶음을 만들지 않는다
- 순서가 없는 `hierarchy` 묶음은 단계로 승격하지 않는다. 분류는 서술로 쓴다
- `promote: true`는 **표시만** 한다. 실제 좌표 변경(하위 단계 추가 등)은 사람이 스펙 개정으로 한다

## 4. 산출물 재생성

```bash
PYTHONIOENCODING=utf-8 py insights/gen_atomview.py
```

인사이트·원자·구조 묶음이 바뀌었으면 페이지를 다시 만든다. 대시보드 파일은 `대시보드/인사이트와 근거.html`이다.

## 5. 보고

- `check_atoms.py`·`check_prose.py` 요약 줄. `check_prose.py`가 한 파일에 WARN 5건을 넘겼으면 그 파일은 `humanize-korean` 스킬을 부를 계기다
- STALE 인사이트 목록과 각각 4갈래 중 어느 쪽으로 보이는지
- 충돌 후보·문서 내부 충돌 중 눈에 걸리는 쌍
- 뭉침 중 승격 후보(한 문서 독점 60% 미만)
- 구조 묶음 중 `members` 2편 이상인 것과 `promote` 판정
- 원자 인용률 — 과잉 추출 지표다

```bash
PYTHONIOENCODING=utf-8 py -c "import io,json,glob,re;cited=set();[cited.update(re.findall(r'A-\d{6}-\d{2}',io.open(p,encoding='utf-8').read())) for p in glob.glob('insights/synth/*.md')];ids=[a['id'] for f in glob.glob('insights/atoms/*.json') for a in json.load(io.open(f,encoding='utf-8'))['atoms']];print('인용 %d/%d (%.0f%%)'%(len(cited&set(ids)),len(ids),100*len(cited&set(ids))/len(ids)))"
```

## 6. 커밋

`structure_groups.json`과 재생성된 페이지를 커밋한다.

**고치지 않는 것**: 인사이트 본문(문체 게이트 FAIL 수정은 예외), 원자 파일, `process.json`, 좌표 사전. 이 스킬은 판단 재료를 만들어 사람에게 넘긴다.
