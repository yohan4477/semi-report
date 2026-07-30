---
name: insight-atomize
description: 변환 완료된 새 문서를 원자·뷰 체계에 넣는다 — 원자 추출(전담 에이전트), 프로세스 단계 배정, 검사기 FAIL 0, 기존 인사이트와의 대조(STALE·충돌 후보) 보고까지. "새 문서 원자화해" / "이 문서 인사이트 체계에 넣어" / 변환을 막 끝낸 문서가 insights/atoms/에 아직 없을 때 쓴다. 인사이트 본문은 고치지 않는다.
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

## 2. 원자 추출 — 에이전트 1회

`insight-atomizer` 에이전트를 **한 번** 호출한다. 프롬프트는 짧게: 소스 id, 경로, hash, 발행일, 그리고 이 문서에서 특히 놓치지 말 주제(있으면). 스키마·규칙은 에이전트 정의에 이미 있으므로 다시 적지 않는다.

문서 원문이 메인 대화에 들어오지 않게 하는 것이 이 분리의 목적이다. 직접 원문을 읽지 않는다.

## 3. 프로세스 단계 배정

에이전트가 만든 원자 파일을 읽고, 각 원자의 `claim`·`view.stack`을 보고 `insights/views/process.json`의 `assign`에 항목을 추가한다.

단계 사전(순서 고정): `웨이퍼 배정` → `칩·랙 설계 확정` → `부지·전력 계약` → `냉각 방식 확정` → `건물 착공` → `랙 발주·인수` → `가동`

- 현재 축(컴퓨트 배치 순서)에 걸리지 않는 원자는 **배정하지 않고 남긴다.** 없는 연결을 억지로 만들면 프로세스 뷰의 값이 사라진다
- 축을 새로 추가하지 않는다. 특정 도메인의 미배정이 쌓이면 스펙 개정으로 논의한다
- 배정은 원자 파일에 넣지 않는다 — 원자는 원문 환원 대상, 배정은 해석이다

## 4. 검사

```bash
PYTHONIOENCODING=utf-8 py insights/check_atoms.py
```

FAIL 0이 될 때까지. 새 문서에서 흔한 것: C2(줄에 없는 수치), C17(line_text 불일치), C16(원문 hash 불일치 — 추출 후 원문이 바뀐 경우), C5(actors.json 미등록, WARN).

C16 FAIL이면 그 문서의 원자를 재추출한다(2로 돌아간다). 줄 번호를 손으로 맞추지 않는다.

## 5. 대조

```bash
PYTHONIOENCODING=utf-8 py insights/crosscheck.py
```

두 가지가 나온다.

- **STALE 인사이트**: 새 원자가 건드린 칸을 쓰는 인사이트. 처리는 4갈래 — 뒷받침(`atoms:`에 id 추가) / 조건 다름(`## 조건 충돌` 갱신) / 뒤집음(`## 주장` 재작성, 이전 판단은 무너진 이유와 함께 보존) / 무관(`dismissed:` + `## 검토 후 무관` 절)
- **충돌 후보 쌍**: 같은 단위인데 조건이 다른 기존 원자와의 쌍. 그 둘을 한 인사이트에서 함께 인용하면 C9가 FAIL을 낸다

**여기서 인사이트 본문을 고치지 않는다.** 목록을 사람에게 넘긴다.

## 6. 커밋·보고

원자 파일과 `process.json`을 한 커밋으로. 메시지에 원자 수·노드 분포·미배정 수를 적는다.

```bash
git add insights/atoms/<파일> insights/views/process.json
git commit -F - <<'EOF'
feat(insights): <문서 제목> 원자화 — 원자 N개

- 노드별: ...
- 프로세스 단계 배정 N개 / 미배정 N개
- 검사기 FAIL 0

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: <세션 URL>
EOF
git push origin main
```

보고에 넣을 것: 원자 수, 노드 분포, 미배정 수, `조건 명시 없음` 비율, STALE 인사이트 목록, 충돌 후보 쌍 수와 그중 눈에 걸리는 것.

## 하지 않는 것

- 인사이트 본문 자동 수정
- 새 인사이트 후보 제안
- 프로세스 축 추가
- 기존 원자 파일 소급 수정
- 문서 원문을 메인 대화로 읽어들이기
