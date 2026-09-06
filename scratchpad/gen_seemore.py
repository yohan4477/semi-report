# -*- coding: utf-8 -*-
"""씨모어 대시보드 — 회차 목록 한 장과 회차마다 글 한 장.

카드가 없다. 접힘도 타일도 없다. 회차 목록에서 줄을 눌러 글로 들어가고, 글
페이지에는 그 회차에 대해 선 판만 실린다. 꼴은 Semi Doped 장과 한 벌이라 마크업·
CSS·파서를 그 장에서 빌려 쓴다(`gen_semidoped`) — 파서를 두 벌 두지 않는다.

  판   전략(⚖) 전략 컨설턴트 출신 애널리스트의 해설
       판이 선 회차에만 링크가 걸린다.

  재료 content/understanding/채널 씨모어/*.md        회차 메타와 한 줄
       content/understanding/채널 씨모어/raw/*.md    전사 (줄 번호가 대조 주소)
       insights/seemore/<slug>-<lane>.md             판 원본
       scratchpad/seemore_figs.py                    도해

  이 화면   py -3.13 scratchpad/gen_seemore.py

규약은 이 파일 check_ui() 가 검사한다 — 접는 것 없음 · 판 없는 줄은 링크가 안 걸림 ·
메타에 「언제 것」 · 타일 없음.

섹션을 새로 팔 때는 SECTIONS 에 한 줄 더하고 회차 frontmatter 의 section 을 그 코드로
적는다. 글이 하나도 없는 섹션은 화면에 안 선다 — 「0편」 머리줄은 빈칸과 같다.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_semidoped as sd  # noqa: E402  마크업·CSS·파서
import seemore_figs  # noqa: E402
import check_fig  # noqa: E402

ROOT = sd.ROOT
SRC = os.path.join(ROOT, 'content', 'understanding', '채널 씨모어')
LANE_DIR = os.path.join(ROOT, 'insights', 'seemore')
OUT = os.path.join(ROOT, '대시보드', '씨모어 대시보드.html')
POST_DIR = os.path.join(ROOT, '대시보드', 'seemore')

LANES = [('strategy', '⚖', '전략', '전략 컨설턴트 출신 애널리스트의 해설')]

# 섹션 — 회차 frontmatter section 코드에 이름을 얹는다. 순서가 곧 화면 순서.
# 채널이 백 편 넘게 올려 두었지만 이 장에 서는 것은 판을 세운 회차뿐이다.
SECTIONS = [('pharma', '제약·바이오')]

STAMP = '2026-09-07'


def episodes():
    eps = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith('.md'):
            continue
        slug = name[:-3]
        meta, body = sd.front(io.open(os.path.join(SRC, name), encoding='utf-8').read())
        lanes = []
        for key, emo, label, sub in LANES:
            path = os.path.join(LANE_DIR, '%s-%s.md' % (slug, key))
            if os.path.exists(path):
                lmeta, lbody = sd.front(io.open(path, encoding='utf-8').read())
                lanes.append({'key': key, 'emo': emo, 'label': label, 'sub': sub,
                              'meta': lmeta, 'body': lbody,
                              'src': 'insights/seemore/%s-%s.md' % (slug, key)})
        eps.append({'slug': slug, 'meta': meta, 'lanes': lanes,
                    'one': sd.one_line(body), 'note': '',
                    'raw': 'content/understanding/채널 씨모어/%s.md' % slug,
                    'transcript': 'content/understanding/채널 씨모어/raw/%s.md' % slug})
    eps.sort(key=lambda e: e['meta'].get('date', ''), reverse=True)
    return eps


def row_html(ep):
    m = ep['meta']
    tags = ['<span class="tag on">%s %s</span>' % (emo, label)
            for key, emo, label, _sub in LANES if any(l['key'] == key for l in ep['lanes'])]
    inner = ('<div class="rmeta"><span>%s</span><span>%s</span></div>'
             '<div class="rtitle">%s</div>'
             % (sd.esc(m.get('date', '')), sd.esc(m.get('topic', '')),
                sd.esc(m.get('title', ep['slug']))))
    if ep['one']:
        inner += '<div class="rone">%s</div>' % sd.esc(ep['one'])
    inner += '<div class="tags">%s</div>' % ''.join(tags)
    if ep['lanes']:
        return '<a class="row" href="seemore/%s.html">%s</a>' % (ep['slug'], inner)
    inner += '<div class="why">글 없음 — 아직 판이 안 섰다</div>'
    return '<div class="row dead">%s</div>' % inner


def post_html(ep):
    m = ep['meta']
    # 진행자가 한 사람이라 이름 색은 한 갈래다. Semi Doped 파서의 전역을 이 회차 것으로 맞춘다
    people = m.get('people', '')
    sd.HOSTS[:] = [n for x in people.split(' / ')
                   if x.strip().startswith('진행') for n in sd.PN_RE.findall(x)]
    sd.NAMES[:] = [n for x in people.split(' / ')
                   if not x.strip().startswith('진행') for n in sd.PN_RE.findall(x)]
    out = [sd.HEAD % (sd.esc(m.get('title', ep['slug'])) + ' — 채널 씨모어', sd.CSS)]
    out.append('<a class="back" href="../씨모어 대시보드.html">← 회차 목록</a>')
    out.append('<h1>%s</h1>' % sd.esc(m.get('title', ep['slug'])))
    out.append('<div class="pmeta">%s · %s(%s)<br>원문 <a href="%s">%s</a> · '
               '요약본 <a href="%s">저장소</a> · 전사 <a href="%s">저장소</a></div>'
               % (sd.esc(m.get('date', '')), sd.esc(m.get('speaker', '')),
                  sd.esc(m.get('org', '')), sd.esc(m.get('source', '')),
                  sd.esc(m.get('source', '')), sd.blob(ep['raw']), sd.blob(ep['transcript'])))
    for lane in ep['lanes']:
        lm = lane['meta']
        out.append('<div class="lane">')
        out.append('<div class="lhead"><b>%s %s 판</b><span>%s</span></div>'
                   % (lane['emo'], lane['label'], sd.esc(lane['sub'])))
        if lm.get('title'):
            out.append('<div class="ltitle">%s</div>' % sd.esc(lm['title']))
        out.append(sd.lane_html(lane['body'], seemore_figs.figs_for(ep['slug'], lane['key'])))
        out.append('<div class="foot">전사를 줄 번호로 대조해 쓴 글이다. '
                   '원본 <a href="%s">%s</a></div>' % (sd.blob(lane['src']), sd.esc(lane['src'])))
        out.append('</div>')
    out.append('</div>')
    return ''.join(out)


def index_html(eps):
    live = sum(1 for e in eps if e['lanes'])
    out = [sd.HEAD % ('씨모어 대시보드', sd.CSS)]
    out.append('<h1>📈 채널 씨모어</h1>')
    out.append('<div class="sub">산업을 갈라 놓고 투자할 자리를 고르는 한국어 채널. '
               '회차마다 ⚖ 전략 판 하나가 선다 — 전사를 줄 번호로 대조해 쓴 해설이다.<br>'
               '글이 있는 회차만 싣는다 — 지금 %d편.</div>' % live)
    groups = []
    for code, name in SECTIONS:
        allc = [e for e in eps if e['meta'].get('section', '') == code]
        withl = [e for e in allc if e['lanes']]
        if withl:
            groups.append((code, name, allc, withl))
    out.append('<nav class="secnav">%s</nav>' % ''.join(
        '<a href="#sec-%s">%s <small>%d</small></a>' % (code, sd.esc(name), len(withl))
        for code, name, _a, withl in groups))
    for code, name, allc, withl in groups:
        out.append('<h2 class="sec" id="sec-%s"><span>%s</span><small>글 %d편 / 회차 %d편</small></h2>'
                   % (code, sd.esc(name), len(withl), len(allc)))
        out.append('<div class="rows">%s</div>' % ''.join(row_html(e) for e in withl))
    stray = [e for e in eps if e['lanes'] and e['meta'].get('section', '') not in dict(SECTIONS)]
    if stray:
        raise SystemExit('섹션 코드가 없는 회차: ' + ', '.join(e['slug'] for e in stray))
    out.append('<div class="foot">유튜브 자동 자막을 문장 단위로 끊어 전사로 두고, 그 줄 번호를 '
               '주소 삼아 판을 쓴다. 값이 전사에 있는지는 사람이 대조한다. '
               '정리일 <b>%s</b> · 페이지 생성은 <code>scratchpad/gen_seemore.py</code></div>' % STAMP)
    out.append('</div>')
    return ''.join(out)


def check_ui(index, posts):
    """이 장의 규약. 아카이브 부품을 안 쓰므로 여기서 직접 본다."""
    bad = []
    if '<details' in index or any('<details' in p for p in posts):
        bad.append('접는 것이 있다 — 이 장은 목록과 글뿐이다')
    if 'class="sec"' not in index:
        bad.append('목록에 섹션 머리줄이 없다')
    if 'class="secnav"' not in index:
        bad.append('목록 위에 섹션 선택 줄이 없다')
    if 'class="tile' in index:
        bad.append('타일이 있다 — 첫 화면은 회차 줄이다')
    for p in posts:
        if 'class="pmeta"' not in p:
            bad.append('글 페이지에 회차 메타(언제 것·누가)가 없다')
        if '<nav class="toc' not in p:
            bad.append('글 페이지에 차례가 없다')
        if 'uc-fig' not in p:
            bad.append('글 페이지에 도해가 없다')
        if '회차 목록' not in p:
            bad.append('글 페이지에서 목록으로 돌아갈 길이 없다')
        if '전사' not in p:
            bad.append('글 페이지에 전사로 가는 길이 없다')
    if re.search(r'<a class="row"[^>]*>(?:(?!</a>).)*글 없음', index, re.S):
        bad.append('판이 없는 줄에 링크가 걸렸다')
    return bad


def check_figs():
    """도해 규칙 둘을 생성 때 기계로 본다 — 글자에 든 값이 전사에 있나, 배치가 겹치나."""
    bad = []
    for (slug, lane), figs in seemore_figs.FIGS.items():
        for key, title, svg_, _cap in figs:
            miss = seemore_figs.missing_values(slug, svg_)
            if miss:
                bad.append('%s/%s %s — 전사에 없는 값 %s' % (slug, lane, title, miss))
            bare = re.sub(r'<defs>.*?</defs>', '', svg_, flags=re.S)
            for h in check_fig.hits(bare, strict=True):
                bad.append('%s/%s %s — %s' % (slug, lane, title, h))
    return bad


def main():
    eps = episodes()
    bad = check_figs()
    if bad:
        raise SystemExit('도해 규칙 위반\n  ' + '\n  '.join(bad))
    if not os.path.isdir(POST_DIR):
        os.makedirs(POST_DIR)
    posts = []
    for ep in eps:
        if not ep['lanes']:
            continue
        h = post_html(ep)
        posts.append(h)
        io.open(os.path.join(POST_DIR, ep['slug'] + '.html'), 'w',
                encoding='utf-8', newline='').write(h)
    idx = index_html(eps)
    bad = check_ui(idx, posts)
    if bad:
        raise SystemExit('규약 위반\n  ' + '\n  '.join(bad))
    io.open(OUT, 'w', encoding='utf-8', newline='').write(idx)
    # 모바일 폭에서 옆으로 밀리나 — 브라우저로만 잴 수 있어 Playwright 를 부른다
    import subprocess
    targets = [OUT] + [os.path.join(POST_DIR, ep['slug'] + '.html') for ep in eps if ep['lanes']]
    r = subprocess.run(['node', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_scroll.js')]
                       + targets, capture_output=True, text=True, encoding='utf-8')
    if r.returncode != 0:
        raise SystemExit('모바일 가로 스크롤\n' + (r.stdout or '') + (r.stderr or ''))
    print('씨모어 — 회차 %d줄 · 글 %d장  ->  %s'
          % (len(eps), sum(1 for e in eps if e['lanes']), os.path.basename(OUT)))


if __name__ == '__main__':
    main()
