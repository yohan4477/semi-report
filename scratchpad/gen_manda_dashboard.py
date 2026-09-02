# -*- coding: utf-8 -*-
"""M&A 대시보드 — 한주성(PwC Korea) 링크드인 글 한 편이 카드 한 장.

카드 목록을 이 파일에 적지 않는다. `content/understanding/한주성/*.md` 한 편이 카드 한 장이고,
섹션·주제칩·gain 까지 전부 그 글의 frontmatter 에 있다. 원고를 새로 넣고 이 파일을 다시
돌리면 카드가 는다. 원고 형식과 쓰는 규칙은 `docs/M&A 대시보드 — 만드는 규칙.md` 가 정본이다.

원문 대조는 `scratchpad/check_manda.py` 가 한다 — 이 생성기는 원고를 믿고 화면만 만든다.
그래서 순서는 check_manda → gen_manda_dashboard 다.

  PYTHONIOENCODING=utf-8 python scratchpad/gen_manda_dashboard.py
"""
import glob
import html as _html
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc  # noqa: E402

SRC_DIR = os.path.join(dc.ROOT, 'content', 'understanding', '한주성')
RAW_DIR = os.path.join(dc.ROOT, 'input', 'linkedin', '한주성')
OUT = os.path.join(dc.ROOT, '대시보드', 'M&A 대시보드.html')
PERMALINK = 'https://www.linkedin.com/feed/update/urn:li:activity:%s/'
AUTHOR = 'https://www.linkedin.com/in/%ED%95%9C%EC%A3%BC%EC%84%B1-jason-han-7b875a58/'

# 섹션은 「무엇에 대한 글인가」로 나눈다. 회사로 나누지 않는다 — 같은 회사가 국내 딜에도
# 실무 글에도 나온다. 번호는 dash_common 이 다시 매긴다.
SEC = {
    'deal-kr':   ('sec-deal-kr', '01', '국내 딜',
                  '한샘·피자헛·배민·컬리 — 한국 시장에서 실제로 오간 딜과 매각설을 구조로 읽는다'),
    'deal-intl': ('sec-deal-intl', '02', '해외 딜',
                  '넷플릭스·하겐다즈·레드불·레이커스 — 국경 밖 딜에서 사는 쪽과 파는 쪽이 각각 무엇을 얻었나'),
    'practice':  ('sec-practice', '03', '딜 실무',
                  '카브아웃·실사·PMI·CoC — 딜 테이블에서 실제로 걸리는 것과 숫자를 의심하는 법'),
    'pe':        ('sec-pe', '04', 'PE · 자본시장',
                  '사모펀드가 어떻게 돈을 벌고 왜 지금 한국 상장사를 사는지, 승계와 상속세가 만드는 매물'),
    'industry':  ('sec-industry', '05', '산업 해설',
                  '반도체 공정·전력 밸류체인·K뷰티 — 딜 밖에서 산업의 돈이 어디로 가는지 읽은 글'),
    'career':    ('sec-career', '06', '커리어 · 일하는 법',
                  '유학·영어·실사 현장에서 본 일 잘하는 사람 — 필자 자신의 이야기'),
}

# frontmatter 에 반드시 있어야 하는 것. 없으면 생성이 멈춘다 — 빈 칸을 채우려면 지어내야 한다
REQUIRED = ('aid', 'title', 'date', 'section', 'topic', 'gain')


def esc(s):
    return _html.escape(s, quote=False)


# 원제의 이모지·국기는 뗀다 — 화면 글꼴에서 국기가 「ITKR」 같은 글자로 나온다
EMOJI = re.compile('[🀀-🫿☀-➿🇦-🇿⭐⭕️‍⚠❗📌]+')


def de_emoji(s):
    return re.sub(r'\s{2,}', ' ', EMOJI.sub('', s)).strip()


# 글 페이지 파일 이름은 slug(제목)인데 slug 가 한자를 떨어낸다 — 「上·中·下」만 다른 연재 제목이
# 같은 파일이 된다(Red Bull 上/中, 2026-09-02). 제목에서 한글로 바꿔 둔다
HANJA = {'上': '상', '中': '중', '下': '하'}


def title_of(t):
    t = de_emoji(t)
    for a, b in HANJA.items():
        t = re.sub(r'(?<![가-힣A-Za-z])%s(?![가-힣A-Za-z])' % a, b, t)
    return t


def inline(s):
    """원고의 굵게·코드만 옮긴다. 나머지 마크다운은 쓰지 않는다."""
    s = esc(s.strip())
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def front(md):
    """frontmatter 를 얕게 읽는다. 값에 콜론이 들어와도 첫 콜론에서만 가른다."""
    if not md.startswith('---'):
        return {}, md
    end = md.find('\n---', 3)
    if end < 0:
        return {}, md
    meta = {}
    for ln in md[3:end].splitlines():
        if ':' in ln:
            k, v = ln.split(':', 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, md[end + 4:]


def sections(body):
    """`## 제목` 으로 가른다. {제목: 본문}."""
    out, cur, buf = {}, None, []
    for ln in body.splitlines():
        m = re.match(r'^##\s+(.+?)\s*$', ln)
        if m:
            if cur is not None:
                out[cur] = '\n'.join(buf).strip()
            cur, buf = re.sub(r'\s*[·]\s*', ' · ', m.group(1)).strip(), []
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        out[cur] = '\n'.join(buf).strip()
    return out


def bullets(txt):
    """`- ` 로 시작하는 줄만. 이어지는 줄은 앞 항목에 붙인다."""
    items = []
    for ln in txt.splitlines():
        if re.match(r'^\s*[-*]\s+', ln):
            items.append(re.sub(r'^\s*[-*]\s+', '', ln).strip())
        elif ln.strip() and items:
            items[-1] += ' ' + ln.strip()
    return items


def parse_points(txt):
    pts = []
    for it in bullets(txt):
        # **소제목.** 본문  →  <b>소제목.</b> 본문
        pts.append(inline(it))
    return pts


def parse_stats(txt):
    out = []
    for it in bullets(txt):
        if '|' not in it:
            continue
        v, lab = it.split('|', 1)
        v, lab = v.strip(), lab.strip()
        if v in ('없음', '-', '—'):
            continue
        out.append((esc(v), esc(lab)))
    return out


def parse_quotes(txt):
    qs = [re.sub(r'^\s*>\s?', '', ln).strip() for ln in txt.splitlines() if ln.strip().startswith('>')]
    return ' '.join('“%s”' % esc(q) for q in qs if q)


def parse_clash(txt):
    out = []
    for it in bullets(txt):
        if '|' in it:
            who, t = it.split('|', 1)
        else:
            who, t = '', it
        who = re.sub(r'\*\*', '', who).strip()
        out.append((esc(who), inline(t)))
    return out


def raw_files():
    """{full aid: 클리핑 경로}. 파일 이름의 끝 네 자리는 365편 중 41쌍이 겹친다 — frontmatter 의
    source 에 든 활동 ID 전체로 잇는다."""
    out = {}
    for p in glob.glob(os.path.join(RAW_DIR, '2*.md')):
        head = io.open(p, encoding='utf-8').read(800)
        m = re.search(r'activity:(\d+)/', head)
        if m:
            out[m.group(1)] = p
    return out


def load_cards():
    raw_by_aid = {a: os.path.relpath(p, dc.ROOT).replace(os.sep, '/') for a, p in raw_files().items()}
    cards = []
    for p in sorted(glob.glob(os.path.join(SRC_DIR, '*.md'))):
        if os.path.basename(p).startswith('_'):
            continue
        md = io.open(p, encoding='utf-8').read()
        fm, body = front(md)
        miss = [k for k in REQUIRED if not fm.get(k)]
        if miss:
            raise SystemExit('%s: frontmatter 에 %s 가 없다' % (os.path.basename(p), ', '.join(miss)))
        if fm['section'] not in SEC:
            raise SystemExit('%s: 모르는 섹션 %s' % (os.path.basename(p), fm['section']))
        sec = sections(body)
        need = ['한 줄', '핵심 포인트', '주요 숫자', '인용', '반론 · 충돌', '메모']
        miss = [k for k in need if k not in sec]
        if miss:
            raise SystemExit('%s: 절 %s 가 없다' % (os.path.basename(p), ', '.join(miss)))
        aid = fm['aid']
        n_chars = fm.get('chars', '')
        links = [('▶ 원문 LinkedIn', PERMALINK % aid, '')]
        rel = raw_by_aid.get(aid)
        if not rel:
            raise SystemExit('%s: aid %s 의 클리핑이 없다' % (os.path.basename(p), aid))
        if rel:
            links.append(('클리핑', dc.blob(rel), 'secondary'))
        c = {
            'section': SEC[fm['section']],
            'topic': ('market', esc(de_emoji(fm['topic']))),
            'title': esc(title_of(fm['title'])),
            'gain': inline(fm['gain']),
            'meta': ['<a href="%s" target="_blank" rel="noopener">한주성</a> <b>PwC Korea</b>' % AUTHOR,
                     '게시 %s' % fm['date'], 'LinkedIn 글'],
            'oneliner': ' '.join(inline(x) for x in sec['한 줄'].split('\n') if x.strip()),
            'points': parse_points(sec['핵심 포인트']),
            'stats': parse_stats(sec['주요 숫자']),
            'quote': parse_quotes(sec['인용']),
            'clash': parse_clash(sec['반론 · 충돌']),
            'note': ' '.join(inline(x) for x in sec['메모'].split('\n') if x.strip())
                    + raw_block(os.path.join(dc.ROOT, rel)),
            'links': links,
            'date': fm['date'],
            '_file': os.path.basename(p),
        }
        if fm.get('scope') in ('kr', 'intl'):
            c['scope'] = fm['scope']
        cards.append(c)
    # dup anchors — 「우리가 몰랐던 Red Bull 이야기 - 上 / 中」처럼 slug 가 한자를 떨어내 겹치는 제목은
    # 날짜를 붙여 가른다. 겹치면 문서에 같은 id 가 둘 서고 글 페이지 한 장이 덮어써진다
    from card_lib import anchor_of
    import collections
    cnt = collections.Counter(anchor_of(c) for c in cards)
    for c in cards:
        if cnt[anchor_of(c)] > 1:
            c['anchor'] = '%s %s' % (de_emoji(c['title']), c['date'])
    return cards


def raw_block(path):
    """클리핑 전문을 접어서 카드 끝에 둔다. <!--RAW:START/END--> 로 감싸 gen_site 가 공개본에서 뗀다 —
    남의 글 전문은 이 컴퓨터에서만 읽는다."""
    md = io.open(path, encoding='utf-8').read()
    _, body = front(md)
    body = body.split('\n## 퍼온 원글')[0].strip()
    paras = [esc(x.strip()) for x in re.split(r'\n\s*\n', body) if x.strip()]
    inner = ''.join('<p>%s</p>' % x.replace('\n', '<br>') for x in paras)
    return ('<!--RAW:START--><details class="uc-raw"><summary>원문 읽기 — 이 컴퓨터에서만 보인다</summary>'
            '<div class="uc-raw-body">%s</div></details><!--RAW:END-->' % inner)


RAW_CSS = '''
  .uc-raw{margin:14px 0 0;border-top:1px dashed var(--line);padding-top:10px}
  .uc-raw summary{cursor:pointer;font-size:12.5px;font-weight:800;color:var(--ink-3)}
  .uc-raw-body{margin-top:10px;font-size:14px;line-height:1.8;color:var(--ink-2);
    max-height:70vh;overflow:auto;padding-right:6px}
  .uc-raw-body p{margin:0 0 .9em}
'''

HEADER = '''  <header>
    <p class="eyebrow">한주성(PwC Korea)의 링크드인 — 딜로 읽는 2026</p>
    <h1>M&A 인사이트</h1>
  </header>'''

if __name__ == '__main__':
    cards = load_cards()
    n_sec = len({c['section'][0] for c in cards})
    dates = sorted(c['date'] for c in cards)
    FOOTER = ('<p class="lede">회계법인 딜 자문가 한 사람이 링크드인에 쓴 글 %d편을 카드로 옮겼습니다. '
              '숫자와 인용은 원문에 있는 것만 실었고, 필자의 판단은 사실과 갈라 표시합니다. '
              '원문 이미지에만 있는 숫자는 카드에 없습니다.</p>'
              '<div class="meta-row"><span>글 <b>%d편</b></span><span>섹션 <b>%d</b></span>'
              '<span>기간 <b>%s ~ %s</b></span>'
              '<span>소스 <b>linkedin.com/in/한주성-jason-han</b></span></div>'
              '\n제3자 해설 요약 아카이브 · 원문은 싣지 않습니다. 투자 추천이 아닙니다.\n'
              '  페이지 생성은 <code>scratchpad/gen_manda_dashboard.py</code>'
              % (len(cards), len(cards), n_sec, dates[0], dates[-1]))
    dc.render(cards, 'M&A 인사이트', HEADER, FOOTER, OUT,
              page_slug='manda',
              rollup=dc.rollup_for('manda', cards, '편'),
              search_ph='회사·딜·용어로 찾기', extra_css=RAW_CSS,
              newest_first=True)
    print('카드 %d · 섹션 %d · %s ~ %s' % (len(cards), n_sec, dates[0], dates[-1]))
    print(OUT)
