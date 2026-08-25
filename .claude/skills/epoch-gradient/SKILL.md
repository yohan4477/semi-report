---
name: epoch-gradient
description: Epoch AI 리서치 글(Gradient Updates) 한 편을 요약본 + 대시보드 카드 + 한국어 도해까지 처리한다. epoch.ai 링크만 붙였을 때, "이 글 올려줘" / "이어서 처리해" / "다음 편도" 라고 할 때 쓴다. 원문 도해를 PNG로 싣지 않고 전부 한국어 인라인 SVG로 다시 그리는 것이 이 장의 규칙이다. SemiAnalysis 뉴스레터는 대상이 아니다(semianalysis-newsletter).
---

# Epoch AI 글 처리

한 편이 들어오면 **요약본 md → 도해 → 카드 → 검사 → 푸시**까지 간다. 사용자가 링크 하나만 던져도 이 순서를 그대로 밟는다. 단계마다 승인을 묻지 않는다.

저장소 루트 `C:\Users\y\semianalysis`. 콘솔이 cp949라 파이썬 실행에 `PYTHONIOENCODING=utf-8`을 붙인다.

| 무엇 | 어디 |
|---|---|
| 대시보드 | `대시보드/Epoch AI 대시보드.html` (공개 슬러그 `/epoch`) |
| 생성기 | `scratchpad/gen_epoch_dashboard.py` |
| 도해 | `scratchpad/epoch_fig.py` |
| 요약본 | `content/epoch/[YYMMDD] 제목.md` |

## 0. 이미 있는지 본다

```bash
ls content/epoch/
grep -c "gradient-updates/<슬러그>" scratchpad/gen_epoch_dashboard.py
```

요약본과 카드가 둘 다 있으면 멈추고 알린다.

## 1. 원문을 받는다

WebFetch는 요약만 돌려준다. 전문이 필요하니 HTML을 직접 받아 뜯는다.

```bash
curl -sL "https://epoch.ai/gradient-updates/<슬러그>" -o <슬러그>.html
```

본문은 `formatted-text content-body article-content` 부터 `About the authors` 앞까지다.
발행일은 `<span class="badge-text">May 20, 2026</span>`, 저자는 `/about/team/<slug>` 링크와
`alt="... 's avatar"`에 있다. 그림 목록은 `<img src="/assets/images/gradient-updates/...">`의
`src`와 `alt`로 뽑는다 — **alt에 그 그림이 무슨 값을 담고 있는지가 적혀 있어 도해를 다시 그릴 때
그대로 쓴다.**

그림은 눈으로도 본다. `.webp`로 줄여 Read로 열어 확인한다 — alt에 없는 각주가 그림 안에 있는 일이
잦다(트랜치 그림의 「33억 달러·연 6.6억 달러」가 그랬다).

## 2. 요약본을 쓴다

`content/epoch/[YYMMDD] 제목.md`. 절 순서는 고정이다.

```
# 제목
> 출처: Epoch AI, Gradient Updates, <저자>, <날짜>. 원문의 **요약**이며 전문 재수록이 아님.
  원문 <URL> · 도해는 원문 그림(CC-BY, Epoch AI)의 구조와 값을 그대로 두고 한국어로 다시 그렸다.
  SemiAnalysis 코퍼스와 별개의 제3자 해설로, 투자 판단 근거로 쓰지 말 것.

## 한 줄 요약
## 핵심 포인트        — 각 항목 <b>소제목.</b>으로 열고 숫자·고유명사를 남긴다
## 주요 숫자          — 표
## (원문에 표가 있으면 그 표)
## 등장하는 회사
## 원문 인용          — 영문 그대로
```

**도해에 넣을 값은 전부 이 파일에 있어야 한다.** `epoch_fig.py`의 값 대조가 이 md를 읽는다.
그림에만 있고 본문에 없는 값(각주·축 라벨)도 여기 적어 둔다. 안 적으면 대조에서 걸린다.

## 3. 도해를 다시 그린다 — 원문 그림 전부

**원문 PNG를 그대로 싣지 않는다.** 라벨이 영어라 카드 본문만 한국어가 된다. 2026-08-25에 data
URI로 구워 넣었다가 전부 걷어냈다(페이지도 500KB에서 98KB로 줄었다).

`insight-figure` 스킬과 `docs/흐름도 — 만드는 규칙.md`를 먼저 읽는다. 그 위에 이 장의 규칙이 얹힌다.

### 부품은 이미 있다 — 새로 짜지 않는다

`scratchpad/epoch_fig.py` 안에 있다.

| 쓸 자리 | 부품 |
|---|---|
| 상자 하나 | `box(x, y, w, 이름, [설명줄], key=강조)` — 글자 폭을 재서 넘치면 그 자리에서 멈춘다 |
| 직각 선 | `arrow('cash'|'svc'|'cond', [(x,y), …])` |
| 선 위 글자 | `lab(x, y, 글, cash=)` — 색은 그 선의 색을 따른다 |
| 역할 라벨 | `role(cx, y, 글)` · 범례 세 줄 `legend()` |
| 세로 스택 | `stack(rows)` · `pair()` · `down_only()` · `left_rail()` · `side()` · `wrap()` |
| 가로·세로 막대 | `barh(rows, vmax, ticks, 제목)` · `barv(...)` |
| 축 | `xaxis()` · `yaxis()` · 색 딱지 `swatch()` |
| 작은 선그래프 | `_panel(...)` — 원문에 식이 있을 때만 |

새 그림은 함수 하나로 짜고 아래 셋에 등록한다.

```python
SRC = {'<키>': '<요약본 파일명>'}      # 새 글이면 한 줄 추가
FIGS = {'<그림 이름>': fig_...}
FIG_SRC = {'<그림 이름>': '<키>'}      # 이 그림을 어느 원문과 대조할지
```

### 카드를 쪼갰으면 카드마다 도해가 서야 한다

원문 그림 수에 맞추지 않는다. 파이낸싱 편은 원문 그림이 넷인데 카드를 셋으로 갈라 카드마다
한두 장씩만 갔고, 사용자가 「도해 하나밖에 없다」로 잡아냈다. **원문에 값이 있는데 그림이 없는
자리를 찾아 채운다** — 조달 구성·성장 곡선·집행 일정·금리 비교·사업장 목록·인도 일정이 그렇게
나왔다. 카드 하나에 셋에서 다섯 장이 기준이다.

### 형태를 바꾸기 전에 그림을 열어 본다

**「원문에 값이 없다」고 판단하기 전에 반드시 이미지를 연다.** 2026-08-25에 여섯 장을 그렇게
막대로 바꿨다가 되돌렸다 — 값은 그림 안에 인쇄돼 있거나 축 눈금을 재면 읽을 수 있었다.
본문 문장에 없다는 것은 값이 없다는 뜻이 아니다.

읽는 순서는 셋이다.

1. **그림에 인쇄된 값**을 먼저 본다. 막대 옆 숫자·버블 옆 숫자·주석의 신뢰구간이 흔하다
2. 없으면 **눈금을 재서 읽는다.** `scratchpad/epoch_extract.py`가 원본 이미지에서 격자선과
   도형을 찾아 데이터 좌표로 되돌려 `data/epoch_fig_data.json`에 굽는다. 그림은 그 값만 쓴다 —
   눈으로 어림해 옮기지 않는다(규칙 2)
3. 그래도 못 읽는 것만 형태를 바꾸고 **캡션에 이유를 적는다**

읽어 낸 값은 요약본 md에 **「원문 도해에서 읽은 값」** 절로 적어 둔다. 값 대조가 그 절을 본다.

### 지키는 것 넷

1. **원문에 없는 값을 그리지 않는다.** 막대 길이·칸 개수·선의 좌표가 전부 값으로 읽힌다.
   못 그리면 형태를 바꾸고 **캡션에 왜 바꿨는지 적는다.** 실제로 두 번 바꿨다 —
   로그 선그래프는 세계 총량의 연도별 값이 원문에 없어 증가율 막대로, 세대별 스택 막대는
   세대별 수치가 없어 총량 막대로 갔다. 청크 프리필 타임라인은 단계별 시간 비율이 없어
   칸을 같은 너비로 뒀다.
2. **축 눈금과 항목 이름은 `t-axis`를 단다.** 눈금값은 자를 읽는 눈금이지 원문에서 가져온
   값이 아니라 대조에서 뺀다. 대신 **눈금 자체를 빼지는 않는다** — 뺐다가 막대를 견줄 자가
   사라졌다.
3. **격자선은 두지 않는다.** 막대 옆 값 라벨을 가로질러 「글자가 선에 깔림」으로 걸린다.
4. **`FIGS`·`FIG_SRC`에 반드시 등록한다.** 빠뜨리면 그 그림은 자기검사를 통째로 빠져나간다 —
   2026-08-25에 딕셔너리가 패치로 잘려 아홉 장이 값 대조를 안 받고 지나갔다. 두 딕셔너리의
   키가 어긋나면 `assert`가 멈춘다.
5. **캡션 끝에 출처를 단다.** 「값은 Epoch AI 원문 도해(CC-BY)를 따랐다」. 형태를 바꿨으면
   그 앞에 이유를 한 문장 적는다.

### 그림 제목은 문장이다

`figs = [(anchor, 제목, svg, 캡션)]`의 제목이 결론을 말한다. 「원문 도해 ②」 같은 라벨은 쓰지 않는다.

```
✕ 원문 도해 ② TPU 리스의 자금 흐름
✓ 리스료가 한 바퀴 돌아 이자와 원금이 된다
```

## 4. 카드를 쓴다

`gen_epoch_dashboard.py`의 `CARDS`에 dict를 넣는다. 형식은 `insight-upload` 스킬과 같고
(`slim_oneliner`·`slim_points` 6~8개·`slim_stats` 4개·`gain`·`clash` 필수), 이 장에서 더 지키는 것은 넷이다.

- **글마다 `SRC*_URL`·`SRC*_MD`·`META*`·`LINKS*`를 따로 둔다.** 저자가 글마다 다르다.
- **`note`는 공통 `NOTE`를 쓴다** — 도해가 다시 그린 것이라는 고지가 거기 들어 있다.
- **`quote`는 영문 그대로 + 괄호에 한국어 옮김.** 원문이 영어라 다듬지 않는다.
- **`clash`에 「같은 대시보드의 다른 편과 겹쳐 읽어야 한다」를 한 줄 넣는다.** 이 장의 글들은
  서로 층이 달라서(파이낸싱↔분배↔토큰 공급) 한 편만 읽으면 결론이 어긋난다.

섹션은 채널이 아니라 **주제**로 나눈다. 새 주제면 `SECTIONS`에 한 줄 더한다. 섹션 번호는
생성기가 다시 매기니 손대지 않는다. **라벨(섹션 제목·topic 칩)에 회사 이름을 넣지 않는다** —
`dash_common.check_labels()`가 생성 때 막는다.

표는 슬림 카드에 안 나온다. 원문 표를 실으려면 `sec_bottom`으로 섹션 아래 층에 낸다.

## 5. 문체 — 이 장에서 실제로 걸린 것들

- **뭘 하는지 안 밝히는 동사를 쓰지 않는다.** 「돈을 댄다」·「손실을 받친다」가 그렇다. 둘 다 사용자가 「뭘 댄다는 거야」·「받친다가 무슨 말이야」로 잡아냈다. 빌려준다 / 낸다 / 떠안는다 / 대신 물어 준다 / 마련한다로 쓴다. 「댄다」는 `check_prose` P18이 잡고, 「받친다」는 아직 사람이 본다.
- **「~는 쪽」을 쓰지 않는다.** 「대는 쪽·갚는 쪽」은 주체를 지운다. 대출·임차인처럼 이름을 댄다.
- **은유를 주어에 세우지 않는다**(P14는 FAIL이다). 나머지는 `korean-readability` 스킬.
- 전문용어는 살리고 **첫 등장에 괄호로 푼다** — 프리필(prefill), SPV(거래 하나만을 위해 세운 회사).

## 6. 검사 — 통과 못 하면 푸시하지 않는다

```bash
PYTHONIOENCODING=utf-8 python scratchpad/epoch_fig.py     # 배치 + 값 대조, 미리보기 HTML
PYTHONIOENCODING=utf-8 python scratchpad/gen_epoch_dashboard.py
PYTHONIOENCODING=utf-8 python scratchpad/check_fig.py
PYTHONIOENCODING=utf-8 python insights/check_prose.py
PYTHONIOENCODING=utf-8 python scripts/update_card_ledger.py
PYTHONIOENCODING=utf-8 python scripts/gen_site.py
```

`epoch_fig.py`는 `scratchpad/_epochfig.html`을 남긴다. **눈으로 확인한다** — 검사기는 겹침만 보고
「읽히는가」는 못 본다. 화면 없이 볼 때는 헤드리스 크롬으로 찍는다.

```bash
cd scratchpad && python -m http.server 8931 &
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --hide-scrollbars --window-size=780,3400 --screenshot=<스크래치패드>/fig.png \
  --virtual-time-budget=4000 "http://127.0.0.1:8931/_epochfig.html"
```

`file://`은 확장이 못 읽고, 스크린샷은 저장소 안에 쓰면 권한이 막는다. 세션 스크래치패드에 쓴다.

## 마치기 전

- [ ] 원문 그림을 **하나도 빠뜨리지 않고** 옮겼나. 못 옮긴 것은 형태를 바꾸고 캡션에 이유를 적었나
- [ ] 그림 값이 전부 요약본 md에 있나 (`epoch_fig.py`가 대조한다)
- [ ] `gain`·`clash`가 들어갔나. clash에 다른 편과의 층 차이를 한 줄 넣었나
- [ ] 검사기 넷 FAIL 0인가
- [ ] `update_card_ledger.py` → `gen_site.py` 순서로 돌렸나
- [ ] 의미 단위로 커밋하고 `main`에 푸시했나
