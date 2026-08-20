---
name: semianalysis-podcast
description: SemiAnalysis 유튜브 팟캐스트(SemiAnalysis Weekly 회차·단발 영상) 한 편을 자막 전문 기반으로 content/podcast/ 변환본 + insights/notes/ 노트 + 대시보드 ① 카드까지 처리한다. "이 팟캐스트 처리해줘" / SemiAnalysis 유튜브 링크만 붙였을 때 / 대시보드에 카드는 있는데 content/podcast/ 에 변환본이 없을 때 쓴다. 언더스탠딩 등 제3자 한국어 영상은 대상이 아니다(insight-upload).
---

# SemiAnalysis 팟캐스트 처리

뉴스레터가 `semianalysis-newsletter` → `semianalysis-transformer` 로 가는 것과 같은 자리를 영상이 차지한다. 다른 점은 셋이다 — 원문이 자막이고, 코퍼스가 `podcast`(pod)이며, 숫자가 글보다 헐겁다(대담이라 조건 없이 튀어나온다).

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 파이썬 실행에 `PYTHONIOENCODING=utf-8`을 붙인다.

## 0. 이미 처리했는지 본다

```bash
py -3.13 -c "import json,io;d=json.load(io.open('raw/youtube/youtube_summaries.json',encoding='utf-8'));print([x['video_id'] for x in d[:8]])"
ls content/podcast/semianalysis/ | grep <yymmdd>
```

`youtube_summaries.json` 에만 있고 `content/podcast/` 에 없으면 **2번부터** 하면 된다 — 대시보드 카드는 이미 서 있고 변환본·노트만 빠진 상태다. 둘 다 있으면 멈춘다.

## 1. 자막을 받는다

```bash
py -3.13 scratchpad/ytsub.py <영상ID> en
```

`scratchpad/yt_subs/<ID>.txt` 에 중복을 걷어낸 전문이 떨어지고, 마지막 줄에 `업로드일|길이(초)|제목` 이 찍힌다. 영어 회차는 `en`, 한국어 영상이면 인자를 생략한다(기본 ko).

- `NO_SUB` + `HTTP Error 429` 는 yt-dlp 쪽 레이트리밋이다. 잠시 뒤 다시 부른다
- `scratchpad/` 는 gitignore다. 자막은 커밋되지 않는다 — 커밋되는 산출물은 변환본과 노트다

## 2. 변환본을 쓴다

`content/podcast/semianalysis/[YYMMDD] <회차> <출연자> - <제목>.md`. 날짜는 영상 공개일이다.

frontmatter는 `categories:` 한 줄만 둔다(`insights/taxonomy.json` 값). 폴더 이름이 fallback이라 안 적으면 카테고리가 `semianalysis` 로 잡힌다.

절 구성:

```markdown
---
categories: [ai-infra/business, ai-models/agents]
---

# <영상 원제>

> **출처**: [SemiAnalysis Weekly (YouTube)](https://www.youtube.com/watch?v=<ID>)
> **출연**: 이름(소속), 이름(소속)
> **공개일**: YYYY-MM-DD
> **길이**: N분 (N초)
> **처리**: 영어 자동자막 전문(N자) 기반 요약

## 📑 목차
## 🔑 용어 정리
## 1. <절 제목>
**📌 핵심:** (불릿 3~5개)
(불릿 뒤에 산문 1~2문단 — 단서·반론·비유가 여기 들어간다)
…
## 자막 한계
```

**대담이라 따로 지키는 것**

- **말한 사람을 붙인다.** 「딜런의 진단은」·「조던의 반론은」. 대담에서는 두 사람이 반대로 말하는 대목이 판단 재료다. 합의된 결론처럼 뭉치면 그게 사라진다
- **자동자막이 뭉갠 고유명사는 옮기지 않는다.** 모델 버전 숫자, 사람 이름 음차가 특히 위험하다. 빼고 마지막 「자막 한계」 절에 무엇을 왜 뺐는지 적는다
- 잡담·사내 농담은 통째로 버린다. 38분 회차에서 판단 재료는 대개 뒤쪽 2/3다
- 나머지 문체 규칙은 `korean-readability` 와 CLAUDE.md 「글 규칙」 그대로다

## 3. 매니페스트에 올린다

```bash
PYTHONIOENCODING=utf-8 py -3.13 insights/gen_manifest.py
```

`content/podcast` 는 `gen_manifest.py` 의 `BASES` 에 이미 등록돼 있다(corpus `podcast`, 약칭 `pod`). 새 소스가 안 잡히면 파일명 `[YYMMDD]` 접두를 확인한다 — 발행일을 거기서 읽는다.

## 4. 노트를 만든다

`insight-note` 스킬을 연다. 형식은 그 스킬이 정본이고, 팟캐스트에서만 다른 것은 둘이다.

- frontmatter `corpus: pod`
- 「수치」의 조건이 대담에서는 자주 비어 있다. **조건이 없으면 그 줄을 적지 않는다** — 「월 1,000만 달러」가 아니라 「2026년 2분기 기준 월 1,000만 달러 언저리」다. 조건을 못 채우면 버린다

노트는 3KB를 넘기지 않는다(N5). 절이 아홉인 회차라도 노트는 한 장이다.

## 5. 대시보드 ① 카드

`raw/youtube/youtube_summaries.json` 맨 앞에 항목을 넣는다(`video_id`·`title`·`channel`·`published`·`url`·`summary_ko`). `summary_ko` 는 `[대괄호 소제목]` 문단을 이어 붙인 긴 요약이고, 대시보드에 실리는 건 이걸 줄인 판이다.

그다음 `대시보드/소셜 신호 히스토리.html` 의 해당 날짜 묶음에 카드를 넣고(`linkedin-update` 스킬의 절차와 같은 자리), ①을 재생성한다.

```bash
py -3.13 scripts/gen_bmirror.py
```

## 6. 검사·커밋

```bash
PYTHONIOENCODING=utf-8 py -3.13 insights/check_notes.py
PYTHONIOENCODING=utf-8 py -3.13 insights/check_prose.py
PYTHONIOENCODING=utf-8 py -3.13 insights/check_read.py
PYTHONIOENCODING=utf-8 py -3.13 insights/check_cite.py
PYTHONIOENCODING=utf-8 py -3.13 insights/check_fresh.py
```

다섯 전부 FAIL 0이어야 푸시한다. 커밋은 의미 단위로 나눈다 — 변환본+노트가 한 단위, 대시보드 반영이 다음 단위다.

## 하지 않는 것

- 자막 전문을 저장소에 커밋 — `scratchpad/` 밖으로 내보내지 않는다
- 뉴스레터 절 번호 체계(② 「뉴스레터 발행일순」) 에 얹기 — 코퍼스를 나눈 이유가 그것이다
- 교차 인사이트 집필 — 노트가 쌓인 뒤 `insight-review` 가 한다
