# AI Engineer 주장 흐름 — 구현 계획

> **에이전트에게:** 이 계획은 `superpowers:subagent-driven-development` 또는
> `superpowers:executing-plans` 로 한 과제씩 실행한다. 단계는 체크박스로 센다.

**Goal:** AI Engineer 발표 81편에서 뽑은 주장을 시간순 한 줄기로 세우고, 뒤에 온
주장이 앞선 주장에 동조했는지 엇갈렸는지 새로 열었는지를 원문 인용 두 개로 보이는
화면 한 장을 만든다.

**Architecture:** 재료는 `insights/views/aie_thread.json` 한 파일(줄 = 주장 하나).
1판은 sonnet 서브에이전트 병렬로 `claim`·`line` 만 뽑고, 2판은 메인이 날짜순으로
`rel` 을 붙인다. 조립기 `scratchpad/gen_aie_thread.py` 가 json 을 읽어 정적 HTML 한
장을 쓰고, 같은 파일 안 `check_ui()` 가 규약을 문다. 인용 대조는 별도
`scratchpad/check_aie_thread.py`.

**Tech Stack:** Python 3 표준 라이브러리만(이 저장소 생성기 관례). 외부 의존 없음.
HTML 은 인라인 CSS/JS, 프레임워크 없음. `scripts/ui_bits.py` 의 `OPEN_AT_TOP` 재사용.

**Spec:** `docs/superpowers/specs/2026-09-08-AI-Engineer-주장-흐름-design.md`

## Global Constraints

- 콘솔은 cp949 다. 파이썬은 항상 `PYTHONIOENCODING=utf-8 python ...` 로 돈다.
  스크립트 머리에 `sys.stdout.reconfigure(encoding='utf-8')` 를 넣는다.
- 파일 읽기·쓰기는 `io.open(..., encoding='utf-8')`. 읽은 뒤 `.replace('\r\n','\n')`.
- **`대시보드/ai-engineer/` 안에 파일을 만들지 않는다.** `dash_common._write_card_pages`
  가 카드 슬러그가 아닌 html 을 매 생성 때 지운다. 산출 경로는
  `대시보드/AI Engineer 주장 흐름.html`.
- 관계 이름은 **`동조`·`엇갈림`** 둘뿐. `반박`·`보강` 을 쓰지 않는다. 관계가 없으면
  `rel: []` 이고 그것이 신규다.
- `claim` 은 `content/aie/<talk>.md` 의 그 줄에 있는 글자 그대로다. 우리 말로 다시
  쓰지 않는다. 줄 번호는 1부터, 빈 줄 포함.
- 도해·화면에 **원문에 없는 값을 그리지 않는다.** 입장을 좌표·점수·색으로 매기지
  않는다. 색은 회색 계열만 — 관계는 기호와 선꼴로 가른다.
- HTML 은 생성물이다. 손으로 고치지 않는다. 고칠 것은 json 과 생성기다.
- 의미 단위마다 커밋·푸시한다. 커밋 메시지 끝에:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
```

## 파일 구조

```
insights/views/aie_thread.json          재료. 줄 = 주장 하나. 사람이 읽고 고칠 수 있는 크기
scratchpad/aie_thread_lib.py            읽기·검증 한 곳. 생성기와 검사기가 같이 쓴다
scratchpad/gen_aie_thread.py            조립기. check_ui() 를 안에 둔다
scratchpad/check_aie_thread.py          claim 이 그 md 줄에 실제로 있나
대시보드/AI Engineer 주장 흐름.html      생성물
scratchpad/gen_aie_dashboard.py         (수정) 머리에 이 장 링크 한 줄
```

`aie_thread_lib.py` 를 따로 두는 이유 — 스키마 검증이 생성기와 검사기 둘 다에 필요한데
한쪽에만 있으면 다른 쪽이 낡는다.

---

### Task 1: 재료 스키마와 읽기 부품

**Files:**
- Create: `scratchpad/aie_thread_lib.py`
- Create: `insights/views/aie_thread.json` (씨앗 3줄)
- Test: `scratchpad/test_aie_thread_lib.py`

**Interfaces:**
- Produces:
  - `load(path=None) -> list[dict]` — json 을 읽어 날짜·id 순으로 정렬해 돌려준다
  - `validate(rows) -> list[str]` — 규약 위반 메시지 목록. 빈 목록이면 통과
  - `REL_KINDS = ('동조', '엇갈림')`
  - `JSON_PATH` — `insights/views/aie_thread.json` 절대경로
  - `AIE_DIR` — `content/aie` 절대경로

- [ ] **Step 1: 씨앗 재료 3줄을 손으로 쓴다**

먼저 실제 줄 번호를 확인한다:

```bash
PYTHONIOENCODING=utf-8 python - <<'EOF'
import io
for f, kw in [('content/aie/2025-08-26-판단은-모델에-맡긴다.md', '판단'),
              ('content/aie/2026-07-26-LLM에게-운전대를-주지-마라.md', '상태'),
              ('content/aie/2025-12-26-에이전트-말고-스킬을-만들어라.md', '스킬')]:
    for i, ln in enumerate(io.open(f, encoding='utf-8').read().replace('\r\n','\n').split('\n'), 1):
        if kw in ln and len(ln) > 30:
            print(f, i, ln[:100]); break
EOF
```

파일 이름은 `ls content/aie` 로 확인해 정확히 맞춘다(위는 예시다). 그 출력의 줄 번호와
줄 글자를 그대로 `insights/views/aie_thread.json` 에 옮긴다:

```json
[
  {"id": "2025-08-26-aws-판단은모델에", "talk": "<정확한 파일명(.md 없이)>",
   "date": "2025-08-26", "org": "AWS", "speaker": "Antje Barth",
   "claim": "<그 줄 글자 그대로>", "line": 0, "rel": []},
  {"id": "2025-12-26-anthropic-스킬", "talk": "<파일명>",
   "date": "2025-12-26", "org": "Anthropic", "speaker": "Barry Zhang & Mahesh Murag",
   "claim": "<그 줄 글자 그대로>", "line": 0, "rel": []},
  {"id": "2026-07-26-microsoft-운전대", "talk": "<파일명>",
   "date": "2026-07-26", "org": "Microsoft", "speaker": "Ornella Bahidika & Joel Allou",
   "claim": "<그 줄 글자 그대로>", "line": 0,
   "rel": [{"to": "2025-08-26-aws-판단은모델에", "kind": "엇갈림"}]}
]
```

`line` 0 은 위 명령이 찍은 번호로 바꾼다.

- [ ] **Step 2: 실패하는 테스트를 쓴다**

`scratchpad/test_aie_thread_lib.py`:

```python
# -*- coding: utf-8 -*-
"""aie_thread_lib 규약 검사. PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib

fails = []

def eq(name, got, want):
    if got != want:
        fails.append('%s: got %r want %r' % (name, got, want))

# 1. 씨앗 재료가 규약을 통과한다
rows = lib.load()
eq('씨앗이 셋 이상', len(rows) >= 3, True)
eq('씨앗 규약 통과', lib.validate(rows), [])

# 2. 날짜순으로 온다
eq('날짜 오름차순', [r['date'] for r in rows], sorted(r['date'] for r in rows))

# 3. rel.to 가 뒤 날짜를 가리키면 잡는다
bad = [dict(rows[0], rel=[{'to': rows[-1]['id'], 'kind': '엇갈림'}])] + rows[1:]
eq('앞 날짜만 가리킨다', any('앞선 날짜' in m for m in lib.validate(bad)), True)

# 4. 없는 id 를 가리키면 잡는다
bad = [dict(rows[-1], rel=[{'to': '없는-id', 'kind': '동조'}])]
eq('없는 id', any('없는 id' in m for m in lib.validate(rows[:-1] + bad)), True)

# 5. 관계 이름이 둘 밖이면 잡는다 — 「반박」은 쓰지 않는다
bad = [dict(rows[-1], rel=[{'to': rows[0]['id'], 'kind': '반박'}])]
eq('관계 이름', any('관계 이름' in m for m in lib.validate(rows[:-1] + bad)), True)

# 6. id 가 겹치면 잡는다
eq('id 중복', any('id 중복' in m for m in lib.validate(rows + rows[:1])), True)

# 7. talk 이 실재하는 파일이어야 한다
bad = [dict(rows[0], talk='없는-발표')] + rows[1:]
eq('원문 없음', any('원문 없음' in m for m in lib.validate(bad)), True)

print('FAIL %d' % len(fails))
for f in fails:
    print(' ', f)
sys.exit(1 if fails else 0)
```

- [ ] **Step 3: 돌려서 실패를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py
```

기대: `ModuleNotFoundError: No module named 'aie_thread_lib'`

- [ ] **Step 4: 부품을 쓴다**

`scratchpad/aie_thread_lib.py`:

```python
# -*- coding: utf-8 -*-
"""주장 흐름의 재료를 읽고 규약을 문다 — 생성기와 검사기가 같이 쓴다.

한쪽에만 두면 다른 쪽이 낡는다. 규약은 설계
docs/superpowers/specs/2026-09-08-AI-Engineer-주장-흐름-design.md §3·§6 이다.

관계는 동조·엇갈림 둘뿐이다. 「반박」은 발표자들이 서로 이름을 대고 받아친 적이
거의 없는데 그 자리에 없던 의도를 붙이는 이름이라 안 쓴다.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, 'insights', 'views', 'aie_thread.json')
AIE_DIR = os.path.join(ROOT, 'content', 'aie')

REL_KINDS = ('동조', '엇갈림')
FIELDS = ('id', 'talk', 'date', 'org', 'speaker', 'claim', 'line', 'rel')


def load(path=None):
    """재료를 읽어 날짜순(같으면 id순)으로 돌려준다."""
    rows = json.load(io.open(path or JSON_PATH, encoding='utf-8'))
    rows.sort(key=lambda r: (r.get('date', ''), r.get('id', '')))
    return rows


def md_lines(talk):
    """그 발표 변환본의 줄 목록. 없으면 None."""
    p = os.path.join(AIE_DIR, '%s.md' % talk)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n')


def validate(rows):
    """규약 위반 메시지 목록. 빈 목록이면 통과."""
    out = []
    seen = {}
    for r in rows:
        rid = r.get('id', '(id 없음)')
        for f in FIELDS:
            if f not in r:
                out.append('%s: 빠진 자리 %s' % (rid, f))
        if rid in seen:
            out.append('%s: id 중복' % rid)
        seen[rid] = r
        if md_lines(r.get('talk', '')) is None:
            out.append('%s: 원문 없음 content/aie/%s.md' % (rid, r.get('talk', '')))
    for r in rows:
        rid = r.get('id', '')
        for rel in r.get('rel') or ():
            to = rel.get('to')
            if rel.get('kind') not in REL_KINDS:
                out.append('%s: 관계 이름이 동조·엇갈림 밖이다 — %r' % (rid, rel.get('kind')))
            if to not in seen:
                out.append('%s: 없는 id 를 가리킨다 — %s' % (rid, to))
            elif seen[to].get('date', '') >= r.get('date', ''):
                out.append('%s: 앞선 날짜만 가리킬 수 있다 — %s' % (rid, to))
    return out


def orphan_ratio(rows):
    """아무 데도 안 걸린 주장의 비율. 걸림은 나가는 rel 이든 들어오는 rel 이든 센다."""
    if not rows:
        return 0.0
    tied = set()
    for r in rows:
        for rel in r.get('rel') or ():
            tied.add(r['id'])
            tied.add(rel.get('to'))
    return 1.0 - len(tied & {r['id'] for r in rows}) / float(len(rows))
```

- [ ] **Step 5: 돌려서 통과를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py
```

기대: `FAIL 0`, 종료 코드 0

- [ ] **Step 6: 커밋**

```bash
git add scratchpad/aie_thread_lib.py scratchpad/test_aie_thread_lib.py insights/views/aie_thread.json
git commit -F - <<'EOF'
feat(AI Engineer): 주장 흐름의 재료 스키마와 규약 검사를 세운다

줄 하나가 주장 하나다. 규약을 생성기·검사기 어느 한쪽에 두면 다른 쪽이 낡아서
읽기 부품 한 곳에 모은다. 관계는 동조·엇갈림 둘뿐 — 「반박」은 발표자에게 없던
의도를 붙이는 이름이라 규약이 문다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
```

---

### Task 2: 인용 대조 검사기

**Files:**
- Create: `scratchpad/check_aie_thread.py`
- Test: `scratchpad/test_aie_thread_lib.py:추가` (아래 8번)

**Interfaces:**
- Consumes: `aie_thread_lib.load`, `aie_thread_lib.md_lines`, `aie_thread_lib.validate`
- Produces: `cite_fails(rows) -> list[str]` — claim 이 그 줄에 없으면 메시지

- [ ] **Step 1: 실패하는 테스트를 더한다**

`scratchpad/test_aie_thread_lib.py` 의 `print('FAIL %d'...)` 바로 위에 붙인다:

```python
# 8. claim 이 그 줄에 없으면 잡는다
import check_aie_thread as chk
eq('씨앗 인용 통과', chk.cite_fails(rows), [])
bad = [dict(rows[0], claim='이 문장은 원문에 없다')] + rows[1:]
eq('인용 어긋남', len(chk.cite_fails(bad)), 1)
```

- [ ] **Step 2: 돌려서 실패를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py
```

기대: `ModuleNotFoundError: No module named 'check_aie_thread'`

- [ ] **Step 3: 검사기를 쓴다**

`scratchpad/check_aie_thread.py`:

```python
# -*- coding: utf-8 -*-
"""주장 흐름의 인용이 그 줄에 실제로 있나.

    PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py

왜 따로 있나 — scripts/check_jsoncite.py 는 메르 json 클리핑 전용이다(줄 번호가
파일에 없어서 순번을 세는 규약이 따로 있다). 마크다운은 줄 번호가 파일에 그대로
있으니 대조가 더 간단하고, 그래서 그물도 따로 친다.

이 검사기는 글자가 그 줄에 있나만 본다. 판정(동조·엇갈림)이 옳은지는 못 본다 —
그건 사람이 두 인용을 나란히 읽어야 할 일이다.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib


def cite_fails(rows):
    """claim 이 line 이 가리키는 줄에 없으면 메시지를 남긴다."""
    out = []
    for r in rows:
        lines = lib.md_lines(r.get('talk', ''))
        if lines is None:
            out.append('%s: 원문 없음' % r.get('id'))
            continue
        n = r.get('line', 0)
        if not isinstance(n, int) or n < 1 or n > len(lines):
            out.append('%s: 줄 번호가 파일 밖이다 — %r (전체 %d줄)' % (r.get('id'), n, len(lines)))
            continue
        src = lines[n - 1]
        if not src.strip():
            out.append('%s: 빈 줄을 가리킨다 — %d' % (r.get('id'), n))
        elif r.get('claim', '') not in src:
            out.append('%s: 그 줄에 없는 인용 — %d\n    원문: %s\n    인용: %s'
                       % (r.get('id'), n, src.strip()[:90], r.get('claim', '')[:90]))
    return out


def main():
    rows = lib.load()
    bad = lib.validate(rows) + cite_fails(rows)
    print('주장 %d줄 · 고립 %.0f%%' % (len(rows), lib.orphan_ratio(rows) * 100))
    for m in bad:
        print('FAIL ·', m)
    print('FAIL %d' % len(bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 4: 돌려서 통과를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py
PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py
```

기대: 앞은 `FAIL 0`, 뒤도 `FAIL 0`

- [ ] **Step 5: 커밋**

```bash
git add scratchpad/check_aie_thread.py scratchpad/test_aie_thread_lib.py
git commit -F - <<'EOF'
feat(AI Engineer): 주장 인용이 그 줄에 있나 무는 검사기

check_jsoncite 는 메르 json 전용이라 여기 못 쓴다. 마크다운은 줄 번호가 파일에
그대로 있어 대조가 더 간단하고, 빈 줄·파일 밖·글자 어긋남 셋을 문다. 판정이
옳은지는 못 본다 — 그건 두 인용을 나란히 읽는 사람 몫이다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
```

---

### Task 3: 1판 — 발표 81편에서 주장 뽑기

**Files:**
- Modify: `insights/views/aie_thread.json` (씨앗 3줄 → 전편)
- Create: `scratchpad/aie_thread_prompt.md` (위임문. 다음에 편이 늘 때 다시 쓴다)

**Interfaces:**
- Consumes: Task 1 의 스키마
- Produces: `rel` 이 모두 `[]` 인 전체 재료

- [ ] **Step 1: 위임문을 쓴다**

`scratchpad/aie_thread_prompt.md` — 서브에이전트에게 그대로 준다:

```markdown
# 위임 — AI Engineer 발표에서 주장 뽑기

파일 하나를 읽고 그 발표가 **에이전트를 어떻게 지어야 하는가**에 대해 낸 주장을
1~2개 뽑는다. 없으면 0개다. 억지로 채우지 않는다.

## 뽑는 것

- 이 발표가 남에게 「이렇게 해라 / 이렇게 하지 마라」고 한 대목.
- 사실 보고(무엇을 만들었다·수치가 얼마다)는 주장이 아니다.
- 도구 소개·제품 소개만 있는 편은 0개다.

## 내는 꼴 (JSON 배열만, 다른 말 없이)

    [{"claim": "<파일의 그 줄에 있는 글자 그대로>", "line": <1부터 센 줄 번호>}]

## 규칙

- `claim` 은 **파일에 있는 글자 그대로**다. 줄여 쓰거나 다듬지 않는다. 문장 하나가
  한 줄 안에 있어야 한다 — 여러 줄에 걸친 문장은 뽑지 않고 다른 줄을 고른다.
- `line` 은 **1부터 센 줄 번호, 빈 줄 포함**이다. 프런트매터 `---` 도 1줄로 센다.
- 마크다운 표시(`##`, `- `, `**`)가 붙은 줄은 피한다. 본문 문장 줄을 고른다.
- 한줄 코멘트(첫 문단)는 우리가 쓴 요약이라 뽑지 않는다. 본문에서 고른다.
- 표시한 줄 번호가 맞는지 스스로 확인하고 낸다.
```

- [ ] **Step 2: 81편을 병렬로 위임한다**

`ls content/aie/*.md` 로 목록을 얻고, 한 번에 8편씩 sonnet 서브에이전트에 나눠 준다.
각 서브에이전트에게 주는 프롬프트는 `scratchpad/aie_thread_prompt.md` 전문 + 맡을
파일 경로 목록이다. 결과 JSON 을 파일명과 함께 받는다.

- [ ] **Step 3: 받은 것을 재료로 합친다**

`id` 는 여기서 만든다 — `<date>-<org 소문자 영문>-<claim 에서 뽑은 열쇠말 2~4글자>`.
`org` 에 공백이 있으면 붙여 쓴다(`Google DeepMind` → `googledeepmind`).
프런트매터에서 `date`·`org`·`speaker`·`title` 을 읽어 채운다. `rel` 은 모두 `[]`.

```bash
PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py
```

기대: `FAIL 0`. 인용이 어긋난 줄은 그 편만 다시 위임해 고친다 —
**직접 claim 을 고쳐 맞추지 않는다.** 원문 줄을 다시 읽고 그 글자로 맞춘다.

- [ ] **Step 4: 커밋**

```bash
git add insights/views/aie_thread.json scratchpad/aie_thread_prompt.md
git commit -F - <<'EOF'
feat(AI Engineer): 발표 81편에서 주장을 뽑는다 — 관계는 아직 안 붙였다

한 편이 낸 주장 1~2줄, 없으면 0줄이다. 억지로 채우면 뒤의 판정이 빈 주장끼리
이어진다. 인용은 원문 줄 글자 그대로 — check_aie_thread 가 문다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
```

---

### Task 4: 2판 — 동조·엇갈림 판정

**Files:**
- Modify: `insights/views/aie_thread.json` (`rel` 채우기)
- Create: `insights/views/aie_thread_판정.md` (판정마다 두 인용을 나란히 남긴 기록)

**Interfaces:**
- Consumes: Task 3 의 재료
- Produces: `rel` 이 채워진 재료 + 사람이 읽을 판정 기록

- [ ] **Step 1: 날짜순 목록을 뽑는다**

```bash
PYTHONIOENCODING=utf-8 python - <<'EOF'
import os, sys
sys.path.insert(0, 'scratchpad')
import aie_thread_lib as lib
for r in lib.load():
    print('%s | %s | %-16s | %s' % (r['date'], r['id'], r['org'], r['claim'][:70]))
EOF
```

- [ ] **Step 2: 메인이 위에서 아래로 판정한다**

**이 단계는 위임하지 않는다.** 판정이 산출물이다. 각 주장에 대해 앞선 주장 목록을
보고 묻는다:

```
같은 물음에 답했나?      아니면 → 신규 (rel 비움)
같은 방향으로 밀었나?    → 동조
반대로 답했나?           → 엇갈림
애매한가?                → 신규. 「보강」 같은 중간 이름을 만들지 않는다
```

한 주장이 앞선 주장 여럿에 걸릴 수 있다. `rel` 배열이 그래서 여럿이다.

- [ ] **Step 3: 판정 기록을 남긴다**

`insights/views/aie_thread_판정.md` — 판정 하나가 문단 하나, 두 인용이 나란히:

```markdown
## 2026-07-26-microsoft-운전대 → 2025-08-26-aws-판단은모델에 · 엇갈림

    AWS 2025-08-26  <앞선 주장 claim 그대로>
    MS  2026-07-26  <이 주장 claim 그대로>

무엇이 같은 물음인가 — 판단을 누가 쥐나. 앞은 모델에 맡기라고, 뒤는 하네스가
상태와 순서를 쥐라고 답한다.
```

근거 두 줄 없이 관계를 붙인 것이 있으면 그 관계를 지운다.

- [ ] **Step 4: 검사**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py
```

기대: `FAIL 0`. 출력의 `고립 %` 를 본다 — 50% 를 넘으면 2판을 다시 훑는다(설계 §5).

- [ ] **Step 5: 커밋**

```bash
git add insights/views/aie_thread.json insights/views/aie_thread_판정.md
git commit -F - <<'EOF'
feat(AI Engineer): 주장 사이 동조·엇갈림을 판정한다 — 근거는 두 인용

판정마다 앞뒤 인용을 나란히 남긴다. 근거 두 줄이 없으면 관계를 안 붙인다 —
「같은 물음에 반대로 답했다」가 보이지 않으면 그것은 엇갈림이 아니라 신규다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
```

---

### Task 5: 조립기와 화면

**Files:**
- Create: `scratchpad/gen_aie_thread.py`
- Create(생성물): `대시보드/AI Engineer 주장 흐름.html`

**Interfaces:**
- Consumes: `aie_thread_lib.load/validate/orphan_ratio`, `scripts/ui_bits.OPEN_AT_TOP`,
  `scratchpad/card_lib.slug`(카드 페이지 주소를 맞추기 위해)
- Produces: `check_ui(html, rows) -> list[str]`, `build() -> str`

- [ ] **Step 1: 화면 규약 테스트를 쓴다**

`scratchpad/test_aie_thread_ui.py`:

```python
# -*- coding: utf-8 -*-
"""주장 흐름 화면 규약. PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_ui.py"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aie_thread_lib as lib
import gen_aie_thread as gen

fails = []
rows = lib.load()
html = gen.build()

def ck(name, cond):
    if not cond:
        fails.append(name)

ck('규약 통과', gen.check_ui(html, rows) == [])
ck('줄이 다 났다', html.count('class="claim"') == len(rows))
ck('거르개 둘', '신규만' in html and '엇갈림만' in html)
ck('색을 안 쓴다', gen.check_ui(html.replace('#555', '#c00'), rows) != [])
ck('반박이라는 말이 없다', '반박' not in html)
ck('카드로 가는 주소', 'ai-engineer/' in html)

print('FAIL %d' % len(fails))
for f in fails:
    print(' ', f)
sys.exit(1 if fails else 0)
```

- [ ] **Step 2: 돌려서 실패를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_ui.py
```

기대: `ModuleNotFoundError: No module named 'gen_aie_thread'`

- [ ] **Step 3: 조립기를 쓴다**

`scratchpad/gen_aie_thread.py` 의 뼈대. 머리 주석에 **왜 dash_common 을 안 쓰는지**를
적는다(워치 장 선례).

```python
# -*- coding: utf-8 -*-
"""AI Engineer 주장 흐름 — 시간순 한 줄기.

아카이브 부품(dash_common)을 안 쓴다. 저기는 카드가 쌓이는 장이라 최신순 목록과
태그로 고르게 돼 있는데, 이 장은 위에서 아래로 한 줄기를 읽는 장이라 고를 것이
순서가 아니다. 규약은 아래 check_ui() 가 생성 때 검사한다 — 규약을 우회하려고 나온
장이 규약 없는 장이 되면 다음 사람이 같은 자리를 다시 판다.

산출은 대시보드/ 바로 아래다. 대시보드/ai-engineer/ 안에 두면
dash_common._write_card_pages 가 카드 슬러그가 아닌 html 을 매 생성 때 지운다.

색으로 입장을 가르지 않는다. 어느 주장이 어느 편인지는 우리가 매긴 값이고, 이 장이
내놓는 근거는 나란히 놓인 두 인용뿐이다. 관계는 기호(● ↑ ✕)와 선꼴(실선·점선)로만
가른다.
"""
import io
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import aie_thread_lib as lib          # noqa: E402
import ui_bits                        # noqa: E402
from card_lib import slug             # noqa: E402

OUT = os.path.join(ROOT, '대시보드', 'AI Engineer 주장 흐름.html')

MARK = {'신규': '●', '동조': '↑', '엇갈림': '✕'}

CSS = '''<style>
  :root { --ink:#1a1a1a; --dim:#555; --pale:#999; --line:#ddd; --bg:#fbfbfa; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.7 -apple-system, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif; }
  .wrap { max-width:860px; margin:0 auto; padding:28px 18px 80px; }
  h1 { font-size:24px; margin:0 0 6px; }
  .lede { color:var(--dim); margin:0 0 22px; }
  .filters { position:sticky; top:0; background:var(--bg); padding:10px 0;
             border-bottom:1px solid var(--line); z-index:2; }
  .chip { display:inline-block; border:1px solid var(--line); background:#fff;
          border-radius:999px; padding:4px 12px; margin:0 6px 6px 0; cursor:pointer;
          font-size:13px; color:var(--dim); }
  .chip[aria-pressed="true"] { border-color:var(--ink); color:var(--ink); }
  .row { display:grid; grid-template-columns:24px 1fr; gap:10px;
         padding:14px 0; border-bottom:1px solid var(--line); }
  .row[hidden] { display:none; }
  .mark { color:var(--dim); text-align:center; }
  .when { font-size:12px; color:var(--pale); }
  .who { font-size:13px; color:var(--dim); }
  .claim { margin:3px 0 0; }
  .row.faint .claim, .row.faint .who { color:var(--pale); }
  .tie { margin:8px 0 0; padding:8px 12px; border-left:2px solid var(--line);
         background:#fff; font-size:14px; }
  .tie.cross { border-left-style:dashed; }
  .tie b { font-weight:600; }
  .q { display:block; color:var(--dim); margin:2px 0; }
  a.card { color:inherit; text-decoration:none; border-bottom:1px solid var(--line); }
</style>'''


def check_ui(html, rows):
    """이 장의 규약. 어기면 생성이 멈춘다."""
    bad = []
    if '반박' in html:
        bad.append('관계 이름은 동조·엇갈림 둘뿐이다 — 「반박」이 화면에 났다')
    for hexcol in ('#c00', '#d00', '#b00', '#00c', 'red', 'blue', 'green'):
        if hexcol in html:
            bad.append('입장을 색으로 가르지 않는다 — %s' % hexcol)
    if html.count('class="claim"') != len(rows):
        bad.append('주장 줄 수가 재료와 다르다')
    if '신규만' not in html or '엇갈림만' not in html:
        bad.append('거르개 둘(신규만·엇갈림만)이 없다')
    if 'ai-engineer/' not in html:
        bad.append('줄에서 카드로 가는 주소가 없다')
    return bad


def build():
    """재료를 읽어 HTML 한 장을 돌려준다. 파일로 쓰지는 않는다."""
    rows = lib.load()
    hard = lib.validate(rows)
    if hard:
        raise SystemExit('재료 규약 FAIL\n  ' + '\n  '.join(hard))
    by_id = {r['id']: r for r in rows}
    tied = set()
    for r in rows:
        for rel in r['rel']:
            tied.add(r['id'])
            tied.add(rel['to'])
    orgs = sorted({r['org'] for r in rows})

    out = []
    for r in rows:
        kinds = {rel['kind'] for rel in r['rel']} or {'신규'}
        mark = MARK['엇갈림'] if '엇갈림' in kinds else (
            MARK['동조'] if '동조' in kinds else MARK['신규'])
        faint = '' if r['id'] in tied else ' faint'
        ties = []
        for rel in r['rel']:
            src = by_id[rel['to']]
            ties.append(
                '<div class="tie%s"><b>%s</b> · %s %s 에 걸린다'
                '<span class="q">%s</span><span class="q">%s</span></div>'
                % (' cross' if rel['kind'] == '엇갈림' else '', rel['kind'],
                   src['date'], esc(src['org']), esc(src['claim']), esc(r['claim'])))
        out.append(
            '<div class="row%s" data-kinds="%s" data-org="%s">'
            '<div class="mark">%s</div><div>'
            '<div class="when">%s</div>'
            '<div class="who">%s · %s</div>'
            '<p class="claim"><a class="card" href="ai-engineer/%s.html">%s</a></p>'
            '%s</div></div>'
            % (faint, ' '.join(sorted(kinds)), esc(r['org']), mark, r['date'],
               esc(r['org']), esc(r['speaker']), slug(title_of(r)), esc(r['claim']),
               ''.join(ties)))

    chips = ['<button class="chip" data-f="all" aria-pressed="true">전부</button>',
             '<button class="chip" data-f="신규">신규만</button>',
             '<button class="chip" data-f="엇갈림">엇갈림만</button>',
             '<button class="chip" data-f="동조">동조만</button>']
    chips += ['<button class="chip" data-org="%s">%s</button>' % (esc(o), esc(o))
              for o in orgs]

    html = ('<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>AI Engineer 주장 흐름</title>\n' + CSS + '\n'
            + ui_bits.OPEN_AT_TOP + '\n<div class="wrap">\n'
            '<a class="card" href="AI Engineer 대시보드.html">← AI Engineer</a>\n'
            '<h1>주장 흐름</h1>\n'
            '<p class="lede">발표 %d편에서 뽑은 주장 %d줄. 위가 오래된 것이다. '
            '뒤에 온 주장이 앞선 주장에 걸리면 그 자리에 두 인용을 나란히 둔다.</p>\n'
            '<div class="filters">%s</div>\n%s\n</div>\n%s\n'
            % (len({r['talk'] for r in rows}), len(rows), ''.join(chips),
               '\n'.join(out), JS))
    return html


JS = '''<script>
(function () {
  var rows = [].slice.call(document.querySelectorAll('.row'));
  var kind = 'all', org = '';
  function paint() {
    rows.forEach(function (el) {
      var okK = kind === 'all' || el.dataset.kinds.split(' ').indexOf(kind) >= 0;
      var okO = !org || el.dataset.org === org;
      el.hidden = !okK;
      el.classList.toggle('faint', okK && !okO && !!org);
    });
  }
  document.querySelectorAll('.chip').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.dataset.f) { kind = b.dataset.f === kind ? 'all' : b.dataset.f; }
      else { org = b.dataset.org === org ? '' : b.dataset.org; }
      document.querySelectorAll('.chip').forEach(function (o) {
        var on = (o.dataset.f && o.dataset.f === kind) || (o.dataset.org && o.dataset.org === org)
                 || (o.dataset.f === 'all' && kind === 'all' && !org);
        o.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      paint();
    });
  });
  paint();
})();
</script>'''


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def title_of(r):
    """카드 페이지 주소는 카드 제목의 슬러그다 — 변환본 프런트매터에서 읽는다."""
    lines = lib.md_lines(r['talk'])
    for ln in lines[:20]:
        if ln.startswith('title: '):
            return ln[7:].strip()
    return r['talk']


def main():
    rows = lib.load()
    html = build()
    bad = check_ui(html, rows)
    for m in bad:
        print('FAIL ·', m)
    if bad:
        return 1
    io.open(OUT, 'w', encoding='utf-8').write(html)
    print('주장 %d줄 · 고립 %.0f%% -> %s'
          % (len(rows), lib.orphan_ratio(rows) * 100, os.path.basename(OUT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

- [ ] **Step 4: 돌려서 통과를 본다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/gen_aie_thread.py
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_ui.py
```

기대: 앞은 `주장 N줄 · 고립 M% -> AI Engineer 주장 흐름.html`, 뒤는 `FAIL 0`

- [ ] **Step 5: 실물을 눈으로 본다**

Chrome 으로 `대시보드/AI Engineer 주장 흐름.html` 을 열어 390px 폭에서 확인한다.
확인할 것 넷 — ① 줄이 날짜순으로 위에서 아래인가 ② 「엇갈림만」을 누르면 그 줄만
남는가 ③ 조직을 누르면 나머지가 옅어지는가 ④ 줄을 누르면 그 카드 페이지가 열리는가.

- [ ] **Step 6: 커밋**

```bash
git add scratchpad/gen_aie_thread.py scratchpad/test_aie_thread_ui.py "대시보드/AI Engineer 주장 흐름.html"
git commit -F - <<'EOF'
feat(AI Engineer): 주장 흐름 화면을 세운다 — 위가 오래된 것, 걸리면 두 인용

dash_common 을 안 쓴다. 저기는 카드가 쌓이는 장이고 여기는 한 줄기를 읽는 장이라
고를 것이 순서가 아니다. 규약은 생성기 안 check_ui() 가 문다 — 색으로 입장을
가르면, 「반박」이 화면에 나면, 줄 수가 재료와 다르면 생성이 멈춘다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
```

---

### Task 6: 대시보드에서 잇고 전체 검사

**Files:**
- Modify: `scratchpad/gen_aie_dashboard.py` (`INTRO` 또는 `HEADER` 에 링크 한 줄)

**Interfaces:**
- Consumes: Task 5 의 산출 경로

- [ ] **Step 1: 링크 자리를 찾는다**

```bash
PYTHONIOENCODING=utf-8 python -c "import io;t=io.open('scratchpad/gen_aie_dashboard.py',encoding='utf-8').read();i=t.find('INTRO');print(t[i-200:i+900])"
```

- [ ] **Step 2: 링크 한 줄을 더한다**

`INTRO` 안에 이 장으로 가는 줄 하나를 넣는다. 문장은 이 장이 무엇을 답하는지로 쓴다:

```html
<a href="AI Engineer 주장 흐름.html">주장 흐름 — 누가 앞사람 말을 밀고 누가 엇갈렸나</a>
```

- [ ] **Step 3: 다시 생성한다**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/gen_aie_dashboard.py
```

기대: 오류 없이 카드 수가 찍힌다. `대시보드/ai-engineer/` 에서 「걷음」이
`AI Engineer 주장 흐름.html` 을 지우지 않는지 확인한다(그 폴더 밖이므로 안 지운다).

- [ ] **Step 4: 검사기를 전부 돌린다**

**일부만 돌리지 않는다**(CLAUDE.md). FAIL 0 이어야 푸시한다.

```bash
PYTHONIOENCODING=utf-8 python insights/check_notes.py
PYTHONIOENCODING=utf-8 python insights/check_prose.py
PYTHONIOENCODING=utf-8 python insights/check_read.py
PYTHONIOENCODING=utf-8 python insights/check_cite.py
PYTHONIOENCODING=utf-8 python insights/check_fresh.py
PYTHONIOENCODING=utf-8 python insights/check_report.py
PYTHONIOENCODING=utf-8 python insights/check_index.py
PYTHONIOENCODING=utf-8 python scripts/check_deps.py
PYTHONIOENCODING=utf-8 python insights/check_val.py
PYTHONIOENCODING=utf-8 python insights/check_debate.py
PYTHONIOENCODING=utf-8 python insights/check_cover.py
PYTHONIOENCODING=utf-8 python scripts/check_jsoncite.py
PYTHONIOENCODING=utf-8 python insights/check_figval.py
PYTHONIOENCODING=utf-8 python insights/check_struct.py
PYTHONIOENCODING=utf-8 python insights/check_frame.py
PYTHONIOENCODING=utf-8 python insights/check_watch.py
PYTHONIOENCODING=utf-8 python scratchpad/check_aie_thread.py
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_lib.py
PYTHONIOENCODING=utf-8 python scratchpad/test_aie_thread_ui.py
```

`check_prose` 가 새 HTML 의 산문을 문다. 걸리면 **HTML 이 아니라 생성기의 문장**을
고친다.

- [ ] **Step 5: 커밋하고 푸시한다**

```bash
git add scratchpad/gen_aie_dashboard.py "대시보드/AI Engineer 대시보드.html" 대시보드/ai-engineer/
git commit -F - <<'EOF'
feat(AI Engineer): 대시보드에서 주장 흐름 장으로 잇는다

카드는 한 편을 읽게 하고, 이 장은 카드 사이를 읽게 한다. 들머리에서 갈라진다.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01KPGwUaGTLkb2Apt2s82nPv
EOF
git push origin main
```

---

## 자기 검토

- 설계 §1(쟁점 서랍 안 세움) → Task 3·4 의 위임문과 판정 규칙에 그대로 있다.
- 설계 §2(관계 셋) → Task 1 `REL_KINDS`, Task 5 `check_ui` 의 「반박」 그물.
- 설계 §3(재료 스키마) → Task 1 `validate`.
- 설계 §4(두 판) → Task 3(병렬 위임)·Task 4(메인 판정).
- 설계 §5(화면) → Task 5. 색 금지·고립 옅게·균등 간격이 CSS 와 `check_ui` 에 있다.
- 설계 §6(조립·검사) → Task 2·5·6.
- 설계 §7(안 하는 것) → Task 3 「없으면 0개」, Task 5 색 금지 그물.
