# -*- coding: utf-8 -*-
"""소스별 미처리 신규 목록 페이지를 만든다.

카톡 말풍선에는 편수만 넣고, 누르면 이 장으로 온다.
scripts/count_new.py 가 세어 넘긴 것을 받아 쓴다 — 스스로 세지 않는다.
"""
import html
import urllib.parse
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '대시보드' / '소스 신규.html'
PUBLIC = ('https://yohan4477.github.io/semi-report/'
          '%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/' + urllib.parse.quote('소스 신규.html'))

CSS = """
:root { --bg:#fbfbfa; --fg:#1d1d1b; --dim:#6b6b66; --line:#e2e2dd; --card:#ffffff; }
:root:not([data-theme=light]) { }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme=light]) { --bg:#161614; --fg:#eceae5; --dim:#9a9891; --line:#2e2c28; --card:#1e1c1a; }
}
:root[data-theme=dark] { --bg:#161614; --fg:#eceae5; --dim:#9a9891; --line:#2e2c28; --card:#1e1c1a; }
body { background:var(--bg); color:var(--fg); margin:0;
       font:15px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI','Malgun Gothic',sans-serif; }
.wrap { max-width:760px; margin:0 auto; padding:28px 18px 64px; }
h1 { font-size:21px; margin:0 0 4px; }
.stamp { color:var(--dim); font-size:13px; margin-bottom:22px; }
.tally { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }
.tally span { background:var(--card); border:1px solid var(--line); border-radius:999px;
              padding:5px 12px; font-size:13px; }
.tally b { font-weight:600; }
h2 { font-size:16px; margin:26px 0 10px; padding-bottom:6px; border-bottom:1px solid var(--line); }
ul { list-style:none; margin:0; padding:0; }
li { padding:7px 0; border-bottom:1px solid var(--line); display:flex; gap:10px; }
.d { color:var(--dim); font-variant-numeric:tabular-nums; white-space:nowrap; font-size:13px; padding-top:1px; }
a { color:inherit; text-decoration:none; }
a:hover { text-decoration:underline; }
.none { color:var(--dim); font-size:14px; padding:6px 0; }
"""


def build(sources, total):
    """sources: [(이름, [(날짜, 영상ID, 제목), ...] 또는 오류 문자열)]"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    tally = ''.join(
        f'<span>{html.escape(name)} <b>{len(items) if isinstance(items, list) else "?"}</b></span>'
        for name, items in sources)
    blocks = []
    for name, items in sources:
        if not isinstance(items, list):
            blocks.append(f'<h2>{html.escape(name)}</h2><p class="none">{html.escape(items)}</p>')
            continue
        if not items:
            blocks.append(f'<h2>{html.escape(name)}</h2><p class="none">새로 올라온 것 없음</p>')
            continue
        rows = ''.join(
            f'<li><span class="d">{d}</span>'
            f'<a href="https://youtu.be/{vid}" target="_blank" rel="noopener">{html.escape(t)}</a></li>'
            for d, vid, t in items)
        blocks.append(f'<h2>{html.escape(name)} {len(items)}편</h2><ul>{rows}</ul>')
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>소스 신규</title><style>{CSS}</style></head>
<body><div class="wrap">
<h1>아직 처리하지 않은 것 {total}편</h1>
<p class="stamp">{now} 기준 · 채널마다 최근 15편만 본다</p>
<div class="tally">{tally}</div>
{''.join(blocks)}
</div></body></html>
"""


def write(sources, total):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(sources, total), encoding='utf-8')
    return OUT
