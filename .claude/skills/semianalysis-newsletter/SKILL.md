---
name: semianalysis-newsletter
description: Fetch a SemiAnalysis newsletter article past the paywall via the authenticated CDP Chrome session (the chrome-semianalysis profile is a paid subscriber), save it as an Obsidian-clipper markdown file under input/clippings/, then hand it to the semianalysis-transformer agent. Use whenever the user says something like "새 뉴스레터 나왔어 / 분석해줘 / 이 SemiAnalysis 글 변환해줘", or when a WebFetch of a newsletter.semianalysis.com article returns only the free ~30% preview ("This post is for paid subscribers").
---

# SemiAnalysis Newsletter Skill

Paywalled `newsletter.semianalysis.com/p/...` articles return only a ~30% free preview to `WebFetch` — the rest is subscriber-only. **The `chrome-semianalysis` Chrome profile is logged in as a paid SemiAnalysis subscriber**, so driving it over CDP renders the full article body. This skill clips the full text, then transforms it.

Working clipper reference implementation: `scratchpad/clip_articles.py` (CDP + `.available-content` extract + `html2text` → Obsidian-clipper markdown). Reuse its `CDP` class and `EXTRACT` JS rather than rewriting.

## 1. Connect to the authenticated CDP Chrome

Same dedicated profile as the linkedin-update skill (`C:\Users\y\.claude\chrome-semianalysis`), one Chrome logged into **both** LinkedIn and SemiAnalysis. Launch with CDP + `--remote-allow-origins=*` (recent Chrome 403s the websocket without it):

```bash
cmd //c start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir="C:\Users\y\.claude\chrome-semianalysis" --no-first-run --no-default-browser-check "https://newsletter.semianalysis.com/"
```

If a chrome-semianalysis process is already running (e.g. from a linkedin-update session), just reuse it — verify with `curl -s http://127.0.0.1:9222/json/version`. **Websocket connection MUST pass `suppress_origin=True`** (`create_connection(url, suppress_origin=True, timeout=30)`), otherwise the handshake 403s. Use `Runtime.evaluate` with `returnByValue:True, awaitPromise:True`.

## 2. Resolve the article slug

The slug is the trailing path of the URL: `https://newsletter.semianalysis.com/p/<slug>`. If the user gives a title instead of a URL, find the newest posts with `WebFetch https://newsletter.semianalysis.com/archive` (the archive/preview pages are NOT paywalled) and match the title → slug.

## 3. Extract the full body (paywall bypass check)

Navigate the CDP tab to `https://newsletter.semianalysis.com/p/<slug>`, wait ~8s, then run the `EXTRACT` JS from `clip_articles.py`. It returns `{title, subtitle, published, authors, text_len, paywalled, html}`.

**Validate before trusting it:**
- `paywalled` should be `false` and `text_len` should be **large (≫ 6000, typically 25K–60K)**. A logged-in subscriber sees the whole article.
- If `paywalled:true` or `text_len < 6000`, the **subscriber session has expired** — do NOT proceed with a partial clip (that's exactly the failure the transformer refuses on). Tell the user to re-login: suggest they type `! ` + the launch command above and sign in to SemiAnalysis in that Chrome window, then retry.

Quick single-article check (adapt `clip_articles.py`, don't reinvent):
```python
call("Page.navigate", {"url": "https://newsletter.semianalysis.com/p/" + slug})
time.sleep(8)
d = json.loads(js(EXTRACT))   # EXTRACT copied from clip_articles.py
assert not d["paywalled"] and d["text_len"] > 6000, "subscriber session expired — re-login"
```

## 4. Save the clipping

Write the Obsidian-clipper markdown to `input/clippings/<sanitized title>.md` using the same frontmatter block `clip_articles.py` builds (`title`, `source`, `author` as `[[..]]`, `published`, `created`, `description`, `tags: [clippings]`) followed by the `html2text`-converted body. This matches the 60+ existing clippings so the transformer finds it the same way. (You can just run `clip_articles.py` after adding the slug to `scratchpad/clipping_gap.md`, or call its functions directly for a one-off.)

## 5. Hand off to the transformer

Once the full clipping exists on disk, spawn the **semianalysis-transformer** agent (delegate — the transform is long and token-heavy; keep it off the main context per [[feedback_delegate_to_protect_context]]). Point it at the saved `input/clippings/<title>.md` (a raw markdown file already on disk — its preferred input) and let it run the full incremental pipeline (read current `TRANSFORMATION_RULES.md`, write to `content/newsletter/`, commit+push as it goes). Model choice per [[feedback_model_selection_delegation]].

## 6. Reflect the new document in the dashboards (optional, on request)

After transformation, the new Korean doc under `content/newsletter/` can be surfaced in `대시보드/인텔리전스 대시보드.html` section ② (뉴스레터) and the cluster summary (③), and cross-linked from related ① signals via the "관련 N" expanders. Only do this when the user asks to update the dashboard too.

## Gotchas

- **Session expiry is the #1 failure.** The symptom is a small `text_len` / `paywalled:true`. Never transform a partial preview — the transformer will (correctly) refuse and you waste a round trip. Verify `text_len` first.
- **`suppress_origin=True` is mandatory** on the websocket, same as the LinkedIn skill.
- Substack lazy-loads images and some embeds; the `.available-content` innerText is complete for text even if a few figures are `[image]` placeholders. That's fine — the transform is text-driven.
- Do not commit the raw clipping under `input/clippings/` unless the repo already tracks them (check `git status`); the transformed output under `content/newsletter/` is the tracked deliverable.
