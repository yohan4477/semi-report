---
name: entity-search
description: 개체 이름 하나로 원문 917편을 가로질러 그 이름이 나온 줄 주소를 찾는다. "램리서치 나온 데 찾아줘" / "엔비디아 언급된 원문" / "이 회사 우리가 뭐라고 썼지" / 교차 인사이트·보고서를 쓰기 전 근거를 모을 때 쓴다. grep 대신 이것을 쓴다 — 별칭과 영문 표기를 사전이 알고, 답에 영수증이 붙는다. 개념으로 묻는 질문("식각 장비를 독점하는 데")은 못 찾는다.
---

# 개체로 원문 찾기

설계 SSOT: `docs/superpowers/specs/2026-08-27-개체-색인과-축-검토기-design.md`. 계획과 실측은 `docs/superpowers/plans/2026-08-2*-개체-색인-*.md`.

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 파이썬 실행에 `PYTHONIOENCODING=utf-8`을 붙인다.

## 언제 쓰나

**쓴다** — 이름을 아는 회사·기술·제품·지표·사람이 원문 어디에 나오는지 찾을 때. 교차 인사이트나 통합 보고서를 쓰기 전에 근거 줄을 모을 때. 「우리가 이 회사를 뭐라고 썼더라」를 확인할 때.

**안 쓴다** — 이름을 모르고 개념만 아는 물음(「식각 장비를 독점하는 데」)은 못 찾는다. 어휘 색인이라 그렇다. 그럴 때는 `insights/notes/`의 `topics`를 훑거나 사람에게 이름을 묻는다.

**grep 대신 쓴다.** 손으로 grep 하면 표기 하나만 떠올리는데 색인은 별칭 전부를 안다. 실측으로 엔비디아는 grep 743줄 대 색인 1,385줄이었다.

## 1. 찾는다

```bash
PYTHONIOENCODING=utf-8 python scripts/q.py 램리서치
PYTHONIOENCODING=utf-8 python scripts/q.py 엔비디아 --cap 5
```

답이 이렇게 나온다.

```
램리서치 · 원문 6편 · 36줄
  [1] 전망 2028  (쓴 날 2026-08-01, 명시)  content/linkedin/[2608] 링크드인 게시물.md#L659
      요지 — 2026~2028년 WFE 전망을 또 한 번 올렸다. …
  [2] 현재 2023  (쓴 날 2023-07-17, 상속) 낡음  content/newsletter/…#L16
  — 영수증 — 색인 2026-08-28 (a67df49f) · 본 줄 36 · 잘림 0 · 시제 전망 2 · 현재 30 · 회고 4
```

## 2. 답을 읽는다

**줄마다 붙는 것 넷.**

| | 뜻 |
|---|---|
| 시제 | 회고(지난 일) · 현재(지금 서술) · 전망(앞날 주장) |
| 연도 | 그 줄이 가리키는 때 |
| 확실도 | 명시(본문에 「1965년」) · 계산(「작년」을 쓴 날로 품) · 상속(표지가 없어 쓴 날을 물려받음) |
| 낡음 | 현재·전망 줄에만 붙는다. 회고는 면제다 — 1965년에 일어난 일은 지금도 그대로다 |

**영수증의 「잘림」을 반드시 본다.** 상한(`--cap`, 기본 40)에 걸려 안 본 줄의 개수다. 이것이 0이 아닌데 「전부 봤다」고 쓰면 거짓말이 된다. 다 봐야 하면 `--cap`을 올린다.

**상속 줄은 시점이 약하다.** 그 줄 자체에 때 표지가 없어 원문의 쓴 날을 물려받은 것이다. 연표나 검증에 쓸 근거로는 명시·계산 줄을 먼저 고른다.

## 3. 근거로 쓴다

주소(`경로#L123`)를 받아 **그 줄을 직접 읽고** 인용한다. 색인은 후보를 주는 것이지 근거가 아니다.

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'insights');import source_lines as sl;print(sl.line_at('.', 'content/…/x.md', 246))"
```

인용한 숫자가 그 줄에 정말 있는지는 `insights/check_cite.py`가 따로 본다.

## 4. 못 찾을 때

**개체가 사전에 없다.** `insights/entities.json`에 없는 이름은 안 잡힌다. 정말 없는지 본다.

```bash
PYTHONIOENCODING=utf-8 python -c "import io,json;rows=json.load(io.open('insights/entities.json',encoding='utf-8'));print([r['canonical'] for r in rows if '램리' in r['canonical']])"
```

없으면 사전에 더한다. 사전은 생성물이 아니라 **사람이 검토해 커밋하는 자료**다.

```bash
PYTHONIOENCODING=utf-8 python -c "
import sys; sys.path.insert(0,'insights')
import entities_lib as el
rows = el.load()
rows.append({'canonical': '새회사', 'type': '회사',
             'ko': ['새회사'], 'en': ['New Corp'], 'deny': []})
msgs = el.validate(rows); assert msgs == [], msgs
el.save(rows); print('넣었다')
"
PYTHONIOENCODING=utf-8 python insights/gen_index.py
PYTHONIOENCODING=utf-8 python insights/gen_times.py
```

`type`은 회사·기술·제품·지표·사람·미정 여섯 중 하나다. 사전이 바뀌면 색인이 **전수로** 다시 만들어진다(1분 남짓).

**표기가 달라 안 잡힌다.** 별칭을 더한다. 한글 별칭은 부분 문자열로, 영문 별칭은 단어 경계로 잡는다.

**엉뚱한 줄이 잡힌다.** `deny`에 넣는다. 개체 이름만 넣는 것이 아니라 **앞말을 붙인 구**를 넣을 수 있다.

```
「모델」          델 이 모델 에 걸리는 것을 막는다
「가 커서」「이 커서」  차이가 커서 를 Cursor 로 읽는 것을 막는다
```

## 5. 색인이 낡지 않았나

원문이 들어왔는데 색인을 안 돌리면 **조회가 에러 없이 그럴듯한 답을 낸다.** 그것을 막는 검사가 있다.

```bash
PYTHONIOENCODING=utf-8 python insights/check_index.py
```

`FAIL 0`이어야 한다. X1이 뜨면 `gen_index.py`를, X8이 뜨면 `gen_times.py`를 다시 돌린다. 평소에는 `scripts/build_all.py`가 둘 다 딸려 돌리므로 따로 칠 일이 드물다. 증분이라 글 한 편이 들어와도 1초 아래다.

## 덮는 범위

```
content/**/*.md              478편   변환본·요약본·팟캐스트·링크드인
input/clippings/*.md          75편   SemiAnalysis 영문 원본
input/clippings/mer/*.json   364편   메르 클리핑
                            ─────
                             917편 · 162,992줄
```

메르 JSON은 물리 줄이 14개뿐이고 본문이 `text` 문자열 하나에 접혀 있다. `#L88`은 **그 본문의 88번째 줄**이다. 갈래별 차이는 `insights/source_lines.py` 한 곳에만 있다.

## 안 하는 것

- **개념 검색을 안 한다.** 이름을 모르면 못 찾는다
- **순위를 안 매긴다.** 색인 순서(경로·줄 번호)대로 준다
- **본문을 안 담는다.** 색인에는 주소만 있고 본문은 조회할 때 읽는다
- **영문 원본의 연도 표기(`in 2026`)를 때로 안 읽는다.** 때 규칙이 「년」을 요구한다. 영문 원본 9,682줄 중 때가 붙은 것은 37줄뿐이다
