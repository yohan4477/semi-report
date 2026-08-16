# -*- coding: utf-8 -*-
"""insight-dashboard.com 정적 사이트 빌드.

대시보드/ 에서 공개 대상만 골라 site/ 에 ASCII 슬러그로 복사하고,
파일 사이 상대 링크를 슬러그로, 사이트에 없는 페이지는 github.io 절대 URL로 바꾼다.

locked=True 페이지는 functions/_middleware.js 가 서버에서 비밀번호로 막는다.
잠금 목록은 이 파일이 아니라 미들웨어 쪽 PROTECTED 와 맞춰야 한다.
"""
import json
import re
import shutil
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / '대시보드'
OUT = ROOT / 'site'
GH = 'https://yohan4477.github.io/semi-report/%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C/'

# 공개 대상: 원본 파일명 -> (슬러그, 카드 제목, 이모지, 한 줄 설명, 잠금 여부)
PAGES = [
    ('통합 인사이트.html', 'unified', '통합 인사이트', '🧩',
     '노트 45장을 가로질러야 보이는 판단만 — 문서 한 편 요약은 싣지 않는다', True),
    ('SemiAnalysis 대시보드.html', 'semianalysis', 'SemiAnalysis', '📊',
     '반도체·AI 인프라 뉴스레터 변환본과 소셜 신호 아카이브', True),
    ('미국주식 사관학교 대시보드.html', 'usa-academy', '미국주식 사관학교', '🎓',
     '미국 증시 강의 정리 — 종목·거시·투자 프레임', True),
    ('언더스탠딩 대시보드.html', 'understanding', 'AI · 인프라 · 에너지', '⚡',
     '데이터센터 전력·에너지 수급·유가 — 국내 해설 아카이브', False),
    ('금융 대시보드.html', 'finance', '금융 인사이트', '💵',
     '금리·국채·환율 — 전 한국은행 국장 해설 정리', False),
    ('부동산 대시보드.html', 'realestate', '부동산 인사이트', '🏠',
     '공급·세제·전세 — 주제별 해설 아카이브', False),
    ('관리자 대시보드.html', 'admin', '관리자', '🛠️',
     '세 갈래가 데이터를 어떻게 처리하는지 — 소스·집필 룰·검사기 색인', True),
]

SLUGS = {src: slug for src, slug, *_ in PAGES}

# 대시보드마다 CSS 변수 이름이 달라서(--ink/--paper vs --sub/--card) 버튼은 색을 자기가 들고 간다.
# 클래스는 ida- 접두어로 격리한다.
HOME_BTN = '''
<style>
  /* 나가는 길은 처음부터 보여야 한다 — 제목 위에 놓는 인라인 링크 */
  .ida-top {
    display:inline-flex; align-items:center; gap:6px; margin:0 0 14px;
    font:600 .8rem/1 -apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    letter-spacing:.012em; text-decoration:none; color:currentColor; opacity:.6;
    transition:opacity .2s ease, transform .34s cubic-bezier(.19,1,.22,1);
    -webkit-tap-highlight-color:transparent;
  }
  .ida-top:hover { opacity:1; transform:translateX(-2px); }
  .ida-top:active { opacity:.45; transition-duration:.09s; }
  .ida-top:focus-visible { outline:2px solid currentColor; outline-offset:3px; border-radius:4px; }

  /* 스크롤로 머리글이 밀려난 뒤에만 뜬다 — 헤더를 가리지 않으려고 */
  .ida-home {
    position:fixed; z-index:9999;
    left:max(16px, env(safe-area-inset-left)); top:max(14px, env(safe-area-inset-top));
    opacity:0; pointer-events:none; transform:translateY(-6px);
    display:inline-flex; align-items:center; gap:7px;
    padding:9px 14px 9px 12px; border-radius:999px;
    /* 작은 글씨는 tracking을 살짝 벌려야 읽힌다 */
    font:600 .82rem/1 -apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    letter-spacing:.012em;
    text-decoration:none; color:#33312c;
    background:rgba(255,255,255,.82); border:1px solid rgba(0,0,0,.11);
    box-shadow:0 4px 16px -4px rgba(0,0,0,.22);
    -webkit-backdrop-filter:saturate(1.5) blur(14px); backdrop-filter:saturate(1.5) blur(14px);
    /* 놓았을 때 감속하듯 — 임계감쇠 스프링에 가까운 곡선 */
    transition:transform .34s cubic-bezier(.19,1,.22,1),
               box-shadow .34s cubic-bezier(.19,1,.22,1),
               opacity .22s ease;
    -webkit-tap-highlight-color:transparent; touch-action:manipulation;
  }
  .ida-home.is-on { opacity:1; pointer-events:auto; transform:translateY(0); }
  .ida-home.is-on:hover { transform:translateY(-1px); box-shadow:0 8px 22px -6px rgba(0,0,0,.3); }
  /* 피드백은 누르는 순간에. 뗄 때까지 기다리면 죽은 느낌이 난다 */
  .ida-home.is-on:active {
    transform:translateY(0) scale(.955);
    transition-duration:.09s; transition-timing-function:ease-out;
  }
  .ida-home:focus-visible { outline:2px solid currentColor; outline-offset:3px; }
  .ida-home .ida-arrow { font-size:.95em; opacity:.62; }
  @media (prefers-color-scheme: dark) {
    .ida-home {
      color:#ecead9; background:rgba(28,28,32,.82);
      border-color:rgba(255,255,255,.15); box-shadow:0 4px 16px -4px rgba(0,0,0,.55);
    }
  }
  /* 투명도를 줄이는 사용자에겐 유리 대신 불투명 판 */
  @media (prefers-reduced-transparency: reduce) {
    .ida-home { background:#fff; -webkit-backdrop-filter:none; backdrop-filter:none; }
    @media (prefers-color-scheme: dark) { .ida-home { background:#1c1c20; } }
  }
  @media (prefers-contrast: more) {
    .ida-home {
      background:#fff; color:#000; border:1.5px solid #000;
      -webkit-backdrop-filter:none; backdrop-filter:none;
    }
    @media (prefers-color-scheme: dark) { .ida-home { background:#000; color:#fff; border-color:#fff; } }
  }
  /* 움직임을 줄여도 피드백 자체는 남긴다 — 이동 대신 명암으로 */
  @media (prefers-reduced-motion: reduce) {
    .ida-home { transition:opacity .15s ease; transform:none; }
    .ida-home.is-on { transform:none; }
    .ida-home.is-on:hover { transform:none; }
    .ida-home.is-on:active { transform:none; opacity:.65; }
    .ida-top:hover { transform:none; }
  }
  /* 좁은 화면에서는 위쪽이 sticky 섹션 선택기 자리라 겹친다 — 아래로 내린다.
     머리글 인라인 링크가 이미 처음부터 보이므로 발견성은 그쪽이 맡는다 */
  @media (max-width: 760px) {
    .ida-home {
      top:auto; bottom:max(16px, env(safe-area-inset-bottom));
      transform:translateY(6px);
    }
    .ida-home.is-on { transform:translateY(0); }
    .ida-home.is-on:hover { transform:translateY(0); }
  }
  @media print { .ida-home, .ida-top { display:none; } }

  /* NEW 배지 — 영상 업로드일이 아니라 사이트에 올라온 날 기준 */
  .ida-new {
    display:inline-block; vertical-align:.14em; margin-right:6px;
    padding:2px 6px 3px; border-radius:5px;
    font:800 .58rem/1 -apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    letter-spacing:.06em; /* 아주 작은 글씨라 tracking을 벌려야 뭉치지 않는다 */
    color:#fff; background:#d1483a; box-shadow:0 1px 3px -1px rgba(209,72,58,.6);
  }
  @media (prefers-color-scheme: dark) {
    .ida-new { background:#e0604f; color:#1a1005; box-shadow:none; }
  }
  @media (prefers-contrast: more) {
    .ida-new { background:#000; color:#fff; box-shadow:none; }
    @media (prefers-color-scheme: dark) { .ida-new { background:#fff; color:#000; } }
  }
  @media print { .ida-new { display:none; } }
</style>
<a class="ida-home" href="/" aria-label="메인 화면으로"><span class="ida-arrow" aria-hidden="true">←</span>메인</a>
<script>
/* 배지는 보는 시점 기준으로 스스로 만료된다 — 재배포를 안 해도 일주일이 지나면 사라진다 */
(function () {
  var WINDOW = 7 * 864e5, now = Date.now();
  document.querySelectorAll('.ida-new[data-since]').forEach(function (el) {
    var since = Date.parse(el.getAttribute('data-since') + 'T00:00:00');
    if (!(now - since < WINDOW)) el.remove();
  });
})();

/* 머리글의 인라인 링크가 화면에서 사라지면 고정 버튼이 그 역할을 넘겨받는다 */
(function () {
  var pill = document.querySelector('.ida-home');
  var anchor = document.querySelector('.ida-top');
  if (!pill) return;
  if (!anchor) { pill.classList.add('is-on'); return; }
  if (!('IntersectionObserver' in window)) { pill.classList.add('is-on'); return; }
  new IntersectionObserver(function (entries) {
    pill.classList.toggle('is-on', !entries[0].isIntersecting);
  }, { rootMargin: '-8px 0px 0px 0px' }).observe(anchor);
})();
</script>
'''

# 머리글 링크는 문서 맨 앞 컨테이너 바로 안쪽에 꽂는다 (대시보드마다 header 또는 main)
TOP_LINK = '<a class="ida-top" href="/"><span aria-hidden="true">←</span>메인</a>\n'
TOP_ANCHOR = re.compile(r'(<(?:header|main)\b[^>]*>)')

LEDGER = ROOT / 'data' / 'site_card_first_seen.json'
NEW_DAYS = 7
H2_CARD = re.compile(r'(<h2 id="(card-[^"]+)"[^>]*>)')


def load_ledger() -> dict:
    if not LEDGER.exists():
        print(f'  ! 대장 없음 ({LEDGER.name}) — NEW 배지를 붙이지 않는다')
        return {}
    return json.loads(LEDGER.read_text(encoding='utf-8'))


def mark_new(html: str, book: dict) -> tuple:
    """일주일 안에 올라온 카드 제목 앞에 NEW 배지를 심는다.

    실제 표시 여부는 브라우저에서 다시 판정한다 — 여기선 후보만 남긴다.
    """
    cutoff = (date.today() - timedelta(days=NEW_DAYS)).isoformat()
    hits = []

    def repl(m):
        since = book.get(m.group(2))
        if not since or since < cutoff:
            return m.group(1)
        hits.append(m.group(2))
        return f'{m.group(1)}<span class="ida-new" data-since="{since}">NEW</span>'

    return H2_CARD.sub(repl, html), hits


def rewrite_links(html: str) -> str:
    """상대 .html 링크를 슬러그(사이트 내) 또는 github.io 절대 URL(사이트 밖)로."""
    def repl(m):
        target = m.group(1)
        if target in SLUGS:
            return f'href="/{SLUGS[target]}"'
        from urllib.parse import quote
        return f'href="{GH}{quote(target)}" target="_blank" rel="noopener"'

    return re.sub(r'href="([^"/:]+\.html)"', repl, html)


def _card(slug: str, title: str, emoji: str, desc: str, locked: bool) -> str:
    lock = '<span class="lock">🔒</span>' if locked else ''
    return f'''    <a class="card" href="/{slug}">
      <span class="ico">{emoji}</span>
      <span class="tx"><strong>{title}{lock}</strong><em>{desc}</em></span>
    </a>'''


# 잠긴 대시보드는 첫 화면에 늘어놓지 않는다. 「비공개 자료」 한 칸으로 묶고
# 비밀번호를 통과한 뒤 그 안에서 고르게 한다. /private 도 미들웨어가 막는다.
PRIVATE_SLUG = 'private'


def build_index() -> str:
    cards = '\n'.join(
        _card(slug, title, emoji, desc, False)
        for _, slug, title, emoji, desc, locked in PAGES if not locked
    )
    n = sum(1 for *_, locked in PAGES if locked)
    if n:
        cards += '\n' + _card(PRIVATE_SLUG, '비공개 자료', '🔒',
                              f'구독 매체를 정리한 대시보드 {n}장 — 비밀번호가 필요합니다', True)
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
    word-break:keep-all; overflow-wrap:break-word;
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
    box-shadow:0 1px 2px rgba(0,0,0,.03);
    transition:border-color .2s ease,
               transform .34s cubic-bezier(.19,1,.22,1),
               box-shadow .34s cubic-bezier(.19,1,.22,1);
    -webkit-tap-highlight-color:transparent; touch-action:manipulation;
  }}
  .card:hover {{
    border-color:var(--accent); transform:translateY(-2px);
    box-shadow:0 10px 24px -12px rgba(0,0,0,.28);
  }}
  /* 누르는 즉시 반응 — 손끝 아래로 눌리듯 */
  .card:active {{
    transform:translateY(0) scale(.987);
    box-shadow:0 1px 2px rgba(0,0,0,.03);
    transition-duration:.09s; transition-timing-function:ease-out;
  }}
  .card:focus-visible {{ outline:2px solid var(--accent); outline-offset:3px; }}
  .ico {{ font-size:1.5rem; line-height:1.3; flex:none; }}
  .tx {{ display:flex; flex-direction:column; gap:3px; }}
  /* 큰 글씨는 조이고 작은 글씨는 그대로 — tracking은 크기마다 다르다 */
  .tx strong {{ font-size:1.02rem; font-weight:700; letter-spacing:-.011em; }}
  .lock {{ font-size:.72rem; margin-left:6px; opacity:.55; vertical-align:1px; }}
  .tx em {{ font-style:normal; color:var(--sub); font-size:.87rem; line-height:1.55; letter-spacing:.004em; }}
  footer {{ margin-top:3rem; color:var(--sub); font-size:.8rem; line-height:1.7; letter-spacing:.008em; }}
  footer a {{ color:var(--sub); }}
  @media (prefers-contrast: more) {{
    .card {{ border-width:1.5px; border-color:var(--fg); }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .card {{ transition:border-color .2s ease, opacity .15s ease; }}
    .card:hover {{ transform:none; box-shadow:0 1px 2px rgba(0,0,0,.03); }}
    .card:active {{ transform:none; opacity:.7; }}
  }}
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
      원문 저작권은 각 발행처에 있습니다.
    </footer>
  </div>
</body>
</html>
'''


def build_private() -> str:
    """비밀번호를 통과한 뒤 보이는 고르는 화면. 인덱스와 같은 셸을 쓴다."""
    cards = '\n'.join(
        _card(slug, title, emoji, desc, False)
        for _, slug, title, emoji, desc, locked in PAGES if locked
    )
    page = build_index()
    body = f'''    <a class="back" href="/">← 전체 목록</a>
    <h1>비공개 자료</h1>
    <p class="lead">구독 매체를 정리한 대시보드입니다. 원문 전문은 두지 않고 요약과 판단만 남깁니다.</p>
    <div class="grid">
{cards}
    </div>
    <footer>
      이 페이지와 아래 대시보드는 비밀번호로 보호됩니다.<br>
      원문 저작권은 각 발행처에 있습니다.
    </footer>
'''
    page = page[:page.index('    <h1>')] + body + page[page.index('  </div>\n</body>'):]
    page = page.replace('<title>Insight Dashboard</title>',
                        '<title>비공개 자료</title>\n<meta name="robots" content="noindex">')
    return page.replace('</style>', '''  .back {
    display:inline-block; margin:0 0 18px; color:var(--sub); text-decoration:none;
    font-size:.84rem; letter-spacing:.01em;
  }
  .back:hover { color:var(--accent); }
</style>''', 1)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    ledger = load_ledger()
    for src, slug, *_ in PAGES:
        html = rewrite_links((SRC / src).read_text(encoding='utf-8'))
        html, fresh = mark_new(html, ledger.get(slug, {}))
        html, hit = TOP_ANCHOR.subn(lambda m: m.group(1) + TOP_LINK, html, count=1)
        if not hit:
            print(f'  ! {src}: header/main을 못 찾아 머리글 링크를 넣지 못했다')
        (OUT / f'{slug}.html').write_text(html + HOME_BTN, encoding='utf-8')
        badge = f'  NEW {len(fresh)}' if fresh else ''
        print(f'  {src}  ->  {slug}.html{badge}')

    (OUT / 'index.html').write_text(build_index(), encoding='utf-8')
    (OUT / f'{PRIVATE_SLUG}.html').write_text(build_private(), encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')
    print(f'\n{len(PAGES) + 2} files -> {OUT}')


if __name__ == '__main__':
    main()
