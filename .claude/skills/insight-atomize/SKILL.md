---
name: insight-atomize
description: 변환 완료된 새 문서 1편을 원자·뷰 체계에 넣는다 — 문서 유형 판별(정량/논증), 원자·구조 추출(전담 에이전트 1회), 프로세스 단계 배정, 검사기 FAIL 0, 커밋까지. "새 문서 원자화해" / "이 문서 인사이트 체계에 넣어" / 변환을 막 끝낸 문서가 insights/atoms/에 아직 없을 때 쓴다. 문서를 가로지르는 판단(대조·좌표 승격)은 하지 않는다 — 그건 insight-review가 한다.
---

# 새 문서 원자화

선행 설계: `docs/superpowers/specs/2026-07-30-원자-뷰-인사이트-design.md`(체계), `docs/superpowers/specs/2026-07-30-원자화-스킬-design.md`(이 절차).

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 한글이 깨지므로 파이썬 실행에는 `PYTHONIOENCODING=utf-8`을 붙인다.

## 1. manifest 갱신

```bash
PYTHONIOENCODING=utf-8 py insights/gen_manifest.py
```

대상 문서의 `id`·`path`·`hash`를 확인한다. manifest에 없으면 여기서 멈추고 변환 파이프라인 쪽 문제로 보고한다.

이미 원자가 있는 문서면 중단한다 — 원문이 안 바뀌었으면 원자도 안 바뀐다:

```bash
PYTHONIOENCODING=utf-8 py -c "import io,json,glob;print([json.load(io.open(f,encoding='utf-8'))['source_id'] for f in glob.glob('insights/atoms/*.json')])"
```

## 2. 원자·구조 추출 — 에이전트 1회

`insight-atomizer` 에이전트를 **한 번** 호출한다. 프롬프트는 짧게: 소스 id, 경로, hash, 발행일, 그리고 이 문서에서 특히 놓치지 말 주제(있으면). 스키마·규칙은 에이전트 정의에 이미 있으므로 다시 적지 않는다.

에이전트는 세 가지를 낸다 — 문서 유형 판정(`quantitative`/`argument`), 원자 파일(정량 문서일 때), `views/structures.json`의 문서 항목. **논증 문서로 판정하면 원자 파일이 없다.** 그 경우 3단계(단계 배정)를 건너뛴다.

문서 원문이 메인 대화에 들어오지 않게 하는 것이 이 분리의 목적이다. 직접 원문을 읽지 않는다.

## 3. 프로세스 단계 배정

에이전트가 만든 원자 파일을 읽고, 각 원자의 `claim`·`view.stack`을 보고 `insights/views/process.json`의 `assign`에 항목을 추가한다.

단계 사전(순서 고정): `웨이퍼 배정` → `칩·랙 설계 확정` → `부지·전력 계약` → `냉각 방식 확정` → `건물 착공` → `랙 발주·인수` → `가동`

- 현재 축(컴퓨트 배치 순서)에 걸리지 않는 원자는 **배정하지 않고 남긴다.** 없는 연결을 억지로 만들면 프로세스 뷰의 값이 사라진다
- **축도 하위 단계도 새로 만들지 않는다.** 문서가 자기 계층·자기 프로세스를 갖고 와도(레고 문서의 3층 구조·모듈화 사이클 5단계처럼) 기존 사전에만 배정한다. 한 칸에 뭉치는 것은 "아직 한 문서만 이 구조를 말한다"는 정확한 표시다
- 좌표 승격은 5단계 `crosscheck.py`의 뭉침 리포트를 보고 **사람이 스펙 개정으로** 한다. 한 문서가 그 칸의 60%를 넘으면 쪼개지 않는다
- 배정은 원자 파일에 넣지 않는다 — 원자는 원문 환원 대상, 배정은 해석이다

## 4. 검사

```bash
PYTHONIOENCODING=utf-8 py insights/check_atoms.py
```

FAIL 0이 될 때까지. 새 문서에서 흔한 것: C2(줄에 없는 수치), C17(line_text 불일치), C16(원문 hash 불일치 — 추출 후 원문이 바뀐 경우), C5(actors.json 미등록, WARN).

C16 FAIL이면 그 문서의 원자를 재추출한다(2로 돌아간다). 줄 번호를 손으로 맞추지 않는다.

구조를 기록했으면 `structures.py`도 오류 0건이어야 한다:

```bash
PYTHONIOENCODING=utf-8 py insights/structures.py
PYTHONIOENCODING=utf-8 py insights/check_prose.py
```

문체 게이트(`check_prose.py`)는 인사이트를 손대지 않았어도 한 번 돌려 회귀가 없는지 본다. 여기서 FAIL이 나면 이번 회차와 무관한 기존 인사이트 문제이므로 보고에 적고 넘어간다.

## 5. 커밋·보고

원자 파일·`views/structures.json`·`views/process.json`·`views/actors.json`·`manifest.json`을 한 커밋으로. 메시지의 수치는 `check_atoms.py` 출력에서 그대로 복사한다(눈으로 세지 말 것).

```bash
git add insights/atoms/<파일> insights/views/structures.json insights/views/process.json insights/views/actors.json insights/manifest.json
git commit -F - <<'EOF'
feat(insights): <문서 제목> 원자화 — 원자 N개

- 문서 유형: quantitative
- 노드별: ...
- 프로세스 단계 배정 N개 / 미배정 N개
- 구조 N개(계층 N·프로세스 N)
- 검사기 FAIL 0

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: <세션 URL>
EOF
git push origin main
```

보고: 문서 유형 판정과 근거, 원자 수·노드 분포·미배정 수, `조건 명시 없음` 비율, 기록한 구조, 그리고 **다음 단계 안내** — 아래 조건 중 하나면 `insight-review`를 돌려야 한다고 적는다.

- 직전 리뷰 이후 원자화된 문서가 3편 이상
- `check_atoms.py`의 STALE(C11) WARN이 1건 이상
- 인사이트를 새로 쓰거나 고치기 직전

**대조(STALE·충돌 후보·문서 내부 충돌·뭉침)와 좌표 승격 판단은 이 스킬의 일이 아니다.** `insight-review`가 한다.

## 하지 않는 것

- 인사이트 본문 자동 수정
- 새 인사이트 후보 제안
- 프로세스 축 추가
- 기존 원자 파일 소급 수정
- 문서 원문을 메인 대화로 읽어들이기
