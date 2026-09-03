# 위임 — How To Scale Your Model 한 장을 한국어 보고서 카드로

당신은 이 저장소(C:\Users\y\semianalysis)에서 JAX 스케일링 북(How To Scale Your Model, jax-ml.github.io/scaling-book) 한 장을 한국어 **보고서 형식 마크다운** 한 편과 **도해 파이썬 파일** 하나로 옮긴다. 커밋하지 않는다. 담당 장은 이 파일 맨 끝 「담당」에 있다.

## 먼저 읽을 것 (순서대로, 전부)
1. `docs/글과 도해 — 확정 규칙.md` — 글·그림 규칙. 이것이 최우선.
2. `.claude/skills/insight-figure/SKILL.md` — 도해 규칙.
3. `content/understanding/언더스탠딩 보고서/2026-08-24-물가-신호를-무시하면-10년이-녹는다.md` 앞 60줄 — 보고서 형식 본보기 (프런트매터 · 한줄 코멘트 · `## N.` 절 · `표:` 표 · `[[fig:열쇠]]`).
4. `scratchpad/und_figs.py` 전체 — 도해 파일 본보기. `aie_figs`의 `_chain / _fan / _fanout / table / band / box / mid / head / arrow / svg` 부품을 쓴다. 필요하면 `scratchpad/aie_figs.py`에서 함수 본문을 본다.
5. 원문: `content/scaling-book/원문/NN-slug.md` (담당 참조). 수식은 LaTeX 그대로 들어 있다.

## 산출 1 — `content/scaling-book/NN-slug.md`
프런트매터 (키 전부 필수):
```
---
title: <한국어 제목 — 결론이 보이는 문장형, 40자 안팎>
date: 2025-02-04
source: <원문 url>
part: <N>
slug: <slug>
section: <아래 표의 값>
topic: <이 장의 주제 칩 2~3개, 「 · 」로 잇는다>
format: report
gain: <이 장을 읽고 무엇을 알게 되나 — 4~6문장, 숫자·이름을 넣어서. 이것이 카드 접힌 상태의 요약이다>
---
```
section 값: index·roofline·tpus·gpus → `basics` / sharding·transformers → `parallel` / training·applied-training → `train` / inference·applied-inference → `infer` / profiling·jax-stuff·conclusion → `tools`.

본문:
- 첫 문단은 반드시 `한줄 코멘트. ` 로 시작. 결론만, 별표(볼드) 금지. 3~4문장.
- 절은 `## 1. 제목` `## 2. 제목` … (번호 손으로 붙인다, 이 형식이 파서 규칙). 절 다섯~아홉.
- 절 안 나열은 ①②③. 「첫째·둘째」 금지.
- 표는 산문과 겹치지 않을 때만. 형식: 한 문단으로 `표: 제목` 줄 + 바로 다음 줄부터 마크다운 표. 표에는 「언제 것 · 성격」이 드러나게(예: 「TPU v5e 공표치」).
- 도해는 그 절의 산문보다 **앞에**, 한 줄에 `[[fig:열쇠]]` 만. 열쇠는 `[a-z0-9_-]+`. 장마다 1~3개.
- 분량 **5,500~6,500자** (공백 포함, 프런트매터 제외). index·conclusion 장만 3,000~5,000자.
- 원문에 있는 값만. 원문이 안 한 말(반례·일반화·인과) 안 한다. 수식은 말로 풀고 필요하면 `T_math = FLOPs / (FLOPs/s)` 처럼 백틱 안 한 줄로.
- 용어는 남기고 첫 등장에 괄호로 푼다. 예: HBM(고대역폭 메모리 — 칩 옆에 쌓은 주 메모리). 「용어」 절 따로 만들지 않는다.
- 문체: 독자는 뉴스 따라가는 사람, 자세는 의뢰인 없는 애널리스트. 도구 이름(MECE·프로세스·밸류체인·대비) 안 쓴다. 번역체 낱말(값이 움직인다·열린다·몫·단·「돈을 댄다」) 금지. 대시(—) 1천자당 2개 이하, 「A가 아니라 B」 대구 1천자당 1개 이하, 볼드 거의 안 쓴다. 은유를 주어 자리에 두지 않는다. 검사기를 피하려고 금지어를 변형하지 않는다 — 문장을 다시 쓴다.
- 저자 이름은 「저자들은」 또는 「제이컵 오스틴 등 저자들은」. 코드는 짧은 것만 백틱.

## 산출 2 — `scratchpad/sb_figs/<slug_with_underscores>.py`
```python
# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aie_figs as F
_X = F._chain([...])          # 또는 F.svg(h, [F.box(...), ...], alt)
_X_CAP = '캡션 — 그림이 무엇을 보여 주는지 한두 문장'
FIGS = {'열쇠': ('제목', _X, _X_CAP), ...}
```
- 본문 `[[fig:열쇠]]` 와 열쇠가 정확히 맞아야 한다. 안 부르는 도해·없는 도해 둘 다 생성이 멈춘다.
- 원문에 없는 값은 안 그린다. 색은 회색만(부품이 이미 그렇다). 항목 넷 이상은 세로로 쌓는다. 한국어 라벨.
- 쓰고 나서 반드시 실행해 검증: `PYTHONIOENCODING=utf-8 python -c "import sys; sys.path.insert(0,'scratchpad'); import sb_figs.<모듈> as m; print(list(m.FIGS))"`

## 다 쓰고 나서
원문을 절마다 다시 열어 ① 값이 그 줄에 있나 ② 원문이 안 한 말을 했나 ③ 낱말을 바꿔 뜻이 좁아졌나 대조하고 고친다. 글자 수를 `python -c` 로 재서 범위에 넣는다.

## 보고 (10줄 이내)
산출 파일 두 경로, 글자 수, 도해 열쇠, 원문에 없어서 못 쓴 것, 확신 없는 대목.
