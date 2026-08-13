# -*- coding: utf-8 -*-
"""insight-dashboard.com 정적 사이트 빌드.

대시보드/ 에서 공개 대상만 골라 site/ 에 ASCII 슬러그로 복사하고,
파일 사이 상대 링크를 슬러그로, 사이트에 없는 페이지는 github.io 절대 URL로 바꾼다.

locked=True 페이지는 functions/_middleware.js 가 서버에서 비밀번호로 막는다.
잠금 목록은 이 파일이 아니라 미들웨어 쪽 PROTECTED 와 맞춰야 한다.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '대시보드'
OUT = ROOT / 'site'
GH = 'https://yohan4477.github.io/semi-report/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/'

# 공개 대상: 원본 파일명 -> (슬러그, 카드 제목, 이모지, 한 줄 설명, 잠금 여부)
PAGES = [
    ('SemiAnalysis 대시보드.html', 'semianalysis', 'SemiAnalysis', '📊',
     '반도체·AI 인프라 뉴스레터 변환본과 소셜 신호 아카이브', True),
    ('미국주식 사관학교 대시보드.html', 'usa-academy', '미국주식 사관학교', '🎓',
     '미국 증시 강의 정리 — 종목·거시·투자 프레임', True),
    ('언더스탠딩 대시보드.html', 'understanding', '언더스탠딩', '🎧',
     '에너지·거시 해설 영상과 프리미엄 기사 요약', False),
    ('금융 대시보드.html', 'finance', '금융 인사이트', '💵',
     '금리·국채·환율 — 전 한국은행 국장 해설 정리', False),
    ('부동산 대시보드.html', 'realestate', '부동산 인사이트', '🏠',
     '공급·세제·전세 — 주제별 해설 아카이브', False),
]

SLUGS = {src: slug for src, slug, *_ in PAGES}


def rewrite_links(html: str) -> str:
    """상대 .html 링크를 슬러그(사이트 내) 또는 github.io 절대 URL(사이트 밖)로."""
    def repl(m):
        target = m.group(1)
        if target in SLUGS:
            return f'href="/{SLUGS[target]}"'
        from urllib.parse import quote
        return f'href="{GH}{quote(target)}" target="_blank" rel="noopener"'

    return re.sub(r'href="([^"/:]+\.html)"', repl, html)


def build_index() -> str:
    cards = '\n'.join(
        f'''    <a class="card" href="/{slug}">
      <span class="ico">{emoji}</span>
      <span class="tx"><strong>{title}{'<span class="lock">🔒</span>' if locked else ''}</strong><em>{desc}</em></span>
    </a>'''
        for _, slug, title, emoji, desc, locked in PAGES
    )
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Insight Dashboard</title>
<meta name="description" content="반도체·AI 인프라·금융·부동산 인사이트 대시보드 모음">
<style>
  :root {{
    --bg:#fbfbf9; --fg:#1b1b19; --sub:#6c6a63; --line:#e5e3dc; --card:#fff; --accent:#b4522b;
  }}
  :root:not([data-theme="light"]) {{ }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg:#16161a; --fg:#eceae4; --sub:#9b988f; --line:#2c2c32; --card:#1e1e23; --accent:#e08a5f;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg:#16161a; --fg:#eceae4; --sub:#9b988f; --line:#2c2c32; --card:#1e1e23; --accent:#e08a5f;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--bg); color:var(--fg);
    font-family:-apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:760px; margin:0 auto; padding:14vh 22px 12vh; }}
  h1 {{ font-size:1.9rem; letter-spacing:-.02em; margin:0 0 .5rem; }}
  .lead {{ color:var(--sub); font-size:1rem; line-height:1.7; margin:0 0 2.6rem; }}
  .grid {{ display:grid; gap:12px; }}
  .card {{
    display:flex; gap:14px; align-items:flex-start;
    padding:18px 20px; border:1px solid var(--line); border-radius:14px;
    background:var(--card); text-decoration:none; color:inherit;
    transition:border-color .15s ease, transform .15s ease;
  }}
  .card:hover {{ border-color:var(--accent); transform:translateY(-1px); }}
  .ico {{ font-size:1.5rem; line-height:1.3; flex:none; }}
  .tx {{ display:flex; flex-direction:column; gap:3px; }}
  .tx strong {{ font-size:1.02rem; font-weight:700; letter-spacing:-.01em; }}
  .lock {{ font-size:.72rem; margin-left:6px; opacity:.55; vertical-align:1px; }}
  .tx em {{ font-style:normal; color:var(--sub); font-size:.87rem; line-height:1.55; }}
  footer {{ margin-top:3rem; color:var(--sub); font-size:.8rem; line-height:1.7; }}
  footer a {{ color:var(--sub); }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Insight Dashboard</h1>
    <p class="lead">반도체·AI 인프라부터 금리·부동산까지, 원문을 읽고 정리한 인사이트 아카이브입니다.</p>
    <div class="grid">
{cards}
    </div>
    <footer>
      🔒 표시된 곳은 비밀번호가 필요합니다.<br>
      개인 학습·정리용 아카이브입니다. 투자 권유가 아닙니다.<br>
      원문 저작권은 각 발행처에 있습니다.
    </footer>
  </div>
</body>
</html>
'''


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    for src, slug, *_ in PAGES:
        html = (SRC / src).read_text(encoding='utf-8')
        (OUT / f'{slug}.html').write_text(rewrite_links(html), encoding='utf-8')
        print(f'  {src}  ->  {slug}.html')

    (OUT / 'index.html').write_text(build_index(), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    print(f'\n{len(PAGES) + 1} files -> {OUT}')


if __name__ == '__main__':
    main()
