---
name: linkedin-update
description: Fetch new SemiAnalysis LinkedIn posts via an authenticated CDP Chrome session, decode exact post timestamps from the activity URN (no OCR/guessing needed), and update 대시보드/소셜 신호 히스토리.html and 대시보드/인텔리전스 대시보드.html with new entries. Use whenever the user says something like "링크드인 글 더 올라왔다" / "링크드인 최신화해".
---

# LinkedIn Update Skill

## 1. Connect to the authenticated browser

A dedicated Chrome profile (`C:\Users\y\.claude\chrome-semianalysis`) stays logged into LinkedIn as the SemiAnalysis follower account. Launch it with CDP enabled, **including `--remote-allow-origins=*`** — recent Chrome rejects the websocket-client handshake without it (403 Forbidden):

```bash
cmd //c start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Users\y\.claude\chrome-semianalysis" --no-first-run --no-default-browser-check "https://www.linkedin.com/company/semianalysis/posts/"
```

If a chrome-semianalysis process is already running without that flag, `curl -s http://127.0.0.1:9222/json/version` will connect but `websocket.create_connection` will fail with `WebSocketBadStatusException: 403`. Find and `taskkill //PID <pid> //F` the **main** process (the one whose command line is just `chrome.exe --remote-debugging-port=9222 ... <url>`, not the `--type=renderer`/`--type=utility`/`--type=gpu-process` helper processes — killing the main one is safe, it's an isolated profile dedicated to this task, not the user's regular browser) via:
```bash
wmic process where "name='chrome.exe'" get ProcessId,CommandLine | grep -i "chrome-semianalysis"
```
then relaunch with the flag above.

Verify with `curl -s http://127.0.0.1:9222/json/version`, then find the LinkedIn tab:
```python
tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
li_tab = next(t for t in tabs if t.get('type') == 'page' and 'linkedin.com' in t.get('url', ''))
ws = websocket.create_connection(li_tab['webSocketDebuggerUrl'], timeout=20)
```
Use `Runtime.enable` then `Runtime.evaluate` (with `returnByValue: True`) as the JSON-RPC pattern for everything below — see any `scratchpad/li_*.py` from prior sessions for the full send/recv boilerplate.

## 1.5. Force the feed to "최근" (recent) sort — DO THIS BEFORE SCROLLING

The company `/posts/` page defaults to **"인기순" (Top/popularity) sort**, which interleaves old high-engagement posts and can starve the scroll of the genuinely newest items. Switch it to **"최근"** first. Verify current state via the sort toggle button (text `정렬 기준: 인기순` vs `정렬 기준: 최근`).

Gotchas learned 2026-07-19:
- The recent option's visible label is **`최근`**, NOT `최신순`. Match exact text `최근`.
- The sort control is a toggle: each click of the `정렬 기준…` button flips `aria-expanded`. Only search for options when `aria-expanded==='true'`; a blind double-click just closes it again.
- Options render as `[role=option]` buttons (`인기순`, `최근`). A generic `button`/`menuitem` scan also catches the video.js speed menu (`vjs-menu-item`, `0.5x`…) — scope to `[role=option]`.

```python
def ev(js): return send('Runtime.evaluate',{'expression':js,'returnByValue':True})['result']['result']['value']
# open dropdown iff not already open
ev("(function(){var b=[].slice.call(document.querySelectorAll('button,[role=button]')).find(x=>/정렬 기준/.test(x.innerText||'')); if(b&&b.getAttribute('aria-expanded')!=='true')b.click(); return 1;})()")
time.sleep(1.2)
ev("(function(){var o=[].slice.call(document.querySelectorAll('[role=option]')).find(x=>(x.innerText||'').trim()==='최근'); if(o)o.click(); return 1;})()")
time.sleep(2.5)
# verify -> button text should now read '정렬 기준: 최근'
```
Full working script: `scratchpad/li_sort5.py`.

## 2. Extract posts (text)

```js
document.querySelectorAll('div.feed-shared-update-v2[data-urn]').forEach(el => {
  const urn = el.getAttribute('data-urn');
  const timeEl = el.querySelector('.update-components-actor__sub-description, time, .feed-shared-actor__sub-description');
  const timeText = timeEl ? timeEl.innerText.trim() : '';
  const textEl = el.querySelector('.feed-shared-update-v2__description, .update-components-text');
  const text = textEl ? textEl.innerText.trim() : '';
  // collect {urn, timeText, text}
});
```
The feed is infinite-scroll: call this after each `window.scrollBy(0, 2600)` + ~1.3s sleep, keyed by `urn` into a dict to dedupe, and stop once the unique count stalls for ~5 rounds (see `scratchpad/li_full_scroll.py` from 2026-07-16 for the exact loop).

**CRITICAL pagination gotcha (learned 2026-07-22):** the bare `/company/semianalysis/posts/` URL under the default 인기순 (Top) sort **hard-caps at 3 posts and refuses to paginate** — no scroll technique (`scrollBy`, `scrollTo(0,bottom)`, `Input.synthesizeScrollGesture`, `Page.bringToFront`, switching to 최근 sort) loads more; docHeight stays fixed. The fix that works: **open the feed URL with `?feedView=all` appended** in a *fresh tab* (`curl -s "http://127.0.0.1:9222/json/new?<url>" -X PUT`), wait ~9s, then the infinite scroll paginates normally. This also applies to `/showcase/<name>/posts/?feedView=all` (e.g. `nvidia-ai-infra`), which paginates hundreds of posts back months. Because virtualized cards unload as you scroll, grab text **every round** (merge into a dict, keep the longest text seen per urn) rather than once at the end.

Diff against the existing dashboard by checking whether the numeric activity ID (the trailing digits of the urn) already appears anywhere in `대시보드/소셜 신호 히스토리.html` — if not, it's new.

## 3. Get the EXACT timestamp — don't trust the relative-time label

LinkedIn only shows fuzzy labels ("1개월 전", "2주 전") past the first few days, which is why older LinkedIn signal used to get excluded from date-sorted lists. **The activity URN itself is a Snowflake-style ID that encodes the exact millisecond timestamp** — no scraping of hover-tooltips or hidden attributes needed (checked: there is no `title`/`aria-label` with a precise date on these elements, the ID is the only source):

```python
import re, datetime
activity_id = int(re.search(r'(\d+)$', urn).group(1))
ts_ms = activity_id >> 22
dt_utc = datetime.datetime.utcfromtimestamp(ts_ms / 1000)
# convert to KST (UTC+9) for display: dt_utc + timedelta(hours=9)
```
Verified accurate against two independently-known dates (matched to the day) on 2026-07-16 — trust this over the visible label for any post older than ~a week.

## 4. Check the actual image before writing a summary

Text-only extraction misses meme/chart/screenshot posts entirely (a post can show as empty or near-empty text while the real content is an image). Before summarizing a post with short/no text, screenshot it:
```python
send('Page.navigate', {'url': f'https://www.linkedin.com/feed/update/urn:li:activity:{activity_id}/'})
time.sleep(4)
shot = send('Page.captureScreenshot', {'format': 'png'})
# base64-decode shot['result']['data'] to PNG, then Read the file to look at it
```
This has caught real content (a "two-buttons" meme, an official partner-deprecation notice with exact dates) that the text alone didn't capture or got slightly garbled (e.g. OCR-ish text mangling model names).

## 5. Update the dashboards

Two files need the new entries, both using the exact KST date from step 3 as the day-group header (`<h3>YYYY-MM-DD</h3>` or `<h3>MM-DD</h3>` depending on file):

- **`대시보드/소셜 신호 히스토리.html`**: full history, newest day-group first, right after the `.tabbar` div. Row pattern: `<div class="row"><a class="rowmain" href="https://www.linkedin.com/feed/update/urn:li:activity:{ID}/" target="_blank" rel="noopener"><span class="src">{LI SVG}</span><span class="sn">{한글 요약}</span></a></div>`. Update the `.stamp` line's date and LinkedIn count.
- **`대시보드/인텔리전스 대시보드.html`** section ① (`<h2>① 소셜·영상 신호 — LinkedIn·YouTube</h2>`): keeps only the 5 most recent items total (per user preference set 2026-07-16) — drop the oldest row(s) to stay at 5 when adding new ones. Row pattern: `<div class="sig" data-c="{category}"><span class="srci">{LI SVG}</span><div><div class="t"><a href="...">{제목}</a> <span class="delta new">신규</span></div><div class="d">{설명}</div></div></div>`. Update the `.stamp` date too.

Both files share the same LinkedIn `<svg>` icon markup — copy it from any existing row rather than retyping.

After editing, sanity-check tag balance (`<div>` open/close counts must match) and re-render with headless Chrome `--dump-dom` to confirm no JS console errors before committing.

## 6. Impact assessment → 대시보드/소스 타임라인.html

`대시보드/소스 타임라인.html`은 이벤트별 **임팩트 트리**를 임베드한다 (2026-07-22 재설계). 새 글마다 **메인 세션 모델이 직접** 영향 평가를 수행한다 — sonnet 등에 위임 금지 (판단 작업, [[feedback_model_selection_delegation]] 원칙).

평가 스키마 (파일 내 `const IMPACTS = {"<idx>": [branch...]}`):
```json
{"t":"영향 대상(기업/섹터)","d":"+|-|0","w":"인과 논리 한 줄(≤35자)","m":1~3,"k":[하위 가지(2차 파급)]}
```
규칙:
- `d`: 그 대상의 매출·수요·경쟁지위 방향. 확신 없으면 가지 자체를 넣지 말 것
- `k`(2차)는 1차 대상을 **경유**하는 파급만 (예: 허가 지연 → Oracle 지연 → OpenAI 용량 밀림). 3차는 추측 영역 — 금지
- `m`: 3=주요(로드맵 취소·대형 계약급), 2=보통, 1=경미. 홍보·밈·채용은 빈 배열 `[]`
- 새 이벤트가 기존 가지를 **반박/해소**하면 (예: 허가 승인으로 Bloom 악재 해소) 새 이벤트에 반대 방향 가지를 추가하고 `w`에 "기존 악재 해소" 식으로 명시
- 엔티티명은 파일 내 기존 명칭 재사용 (NVIDIA, SK하이닉스, 가스엔진 OEM, 광모듈 업체 …) — 새 이름 남발하면 집계 쪼개짐

추가 방법: `const EVENTS = [...]`에 `{idx,date,src,label,url}` (idx는 기존 최대값+1), `IMPACTS`에 같은 idx 키로 트리. 수동 이벤트(외부 뉴스)도 같은 구조로 추가 가능 (`src:'li'` 대신 적절한 소스, url은 뉴스 링크).
