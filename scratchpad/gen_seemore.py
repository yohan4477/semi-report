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
SECTIONS = [('news', '기사 읽기'), ('basics', '투자 원칙'), ('edu', '제도와 개념'),
            ('aiinfra', 'AI 인프라'), ('power', '전력·전력반도체'), ('gold', '금'),
            ('hotel', '호텔'),
            ('pharma', '제약·바이오'), ('dist', '제약유통'), ('space', '우주테크'),
            ('physicalai', '피지컬 AI'), ('nuclear', '원전·SMR')]

STAMP = '2026-09-07'

# 채널이 한 주제를 연달아 올린 묶음은 목록에서 한 덩어리로 세운다. 잣대는 「연달아」다 —
# 날짜 내림차순으로 늘어놓았을 때 같은 섹션이 끊기지 않고 이어지는 구간이 곧 시리즈다.
# 사이에 다른 주제가 끼면 거기서 끊긴다(원전은 06-08 한 편과 06-29부터 넉 편이 따로 선다).
# 기사 읽기는 매주 돌아오는 꼴이라 이어져도 시리즈가 아니다 — 여기서만 뺀다.
NO_SERIES = {'news'}

# 목록은 최신 순서 하나다. 섹션은 줄에 붙는 태그이고, 위 선택 줄은 그 태그로 줄을 고르는
# 장치다 — 화면 순서를 바꾸지 않는다. 접는 것이 아니라 거르는 것이라 규약에 안 걸린다.
SECJS_CSS = """
.secnav a.on{background:#1b1f27;color:#fff;border-color:#1b1f27}
.secnav a.on small{color:#c8cdd6}
.grp{border:1px solid #d5dae2;border-radius:10px;background:#f7f9fc;padding:10px 10px 4px;margin:0 0 10px}
.grp .ghead{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;margin:0 4px 8px}
.grp .ghead b{font-size:15px;color:#1b1f27}
.grp .ghead span{font-size:12px;color:#7b8492}
.grp .row{background:#fff}
"""
SECJS = """<script>
(function(){
  var nav=document.querySelector('.secnav'),
      rows=[].slice.call(document.querySelectorAll('.rows > [data-sec]'));
  if(!nav) return;
  nav.addEventListener('click', function(e){
    var a=e.target.closest('a[data-sec]'); if(!a) return;
    e.preventDefault();
    [].forEach.call(nav.querySelectorAll('a'), function(x){ x.classList.remove('on'); });
    a.classList.add('on');
    var sec=a.getAttribute('data-sec');
    rows.forEach(function(r){ r.hidden = !!sec && r.getAttribute('data-sec')!==sec; });
  });
})();
</script>""" 


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


SEC_NAME = dict(SECTIONS)


def half(one):
    """목록의 한 줄 설명은 요약본 「한 줄」 절의 앞 절반만 싣는다.

    요약본의 한 줄은 네댓 문장짜리 문단이라 목록에서는 길다. 문장 경계로 끊어
    앞 절반만 남긴다 — 줄이는 자리가 문장 가운데면 뜻이 잘린다."""
    sents = [s for s in re.split(r'(?<=다\.)\s+', one.strip()) if s]
    if len(sents) < 2:
        return one
    return ' '.join(sents[:(len(sents) + 1) // 2])


def row_html(ep, in_series=False):
    m = ep['meta']
    code = m.get('section', '')
    # 묶음 안에서는 섹션을 다시 안 적는다 — 머리줄이 이미 말한다
    tags = [] if in_series else ['<span class="tag">%s</span>' % sd.esc(SEC_NAME.get(code, code))]
    tags += ['<span class="tag on">%s %s</span>' % (emo, label)
             for key, emo, label, _sub in LANES if any(l['key'] == key for l in ep['lanes'])]
    inner = ('<div class="rmeta"><span>%s</span><span>%s</span></div>'
             '<div class="rtitle">%s</div>'
             % (sd.esc(m.get('date', '')), sd.esc(m.get('topic', '')),
                sd.esc(m.get('title', ep['slug']))))
    if ep['one']:
        inner += '<div class="rone">%s</div>' % sd.esc(half(ep['one']))
    inner += '<div class="tags">%s</div>' % ''.join(tags)
    if ep['lanes']:
        return ('<a class="row" data-sec="%s" href="seemore/%s.html">%s</a>'
                % (code, ep['slug'], inner))
    inner += '<div class="why">글 없음 — 아직 판이 안 섰다</div>'
    return '<div class="row dead" data-sec="%s">%s</div>' % (code, inner)


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


def runs(live):
    """날짜 내림차순 목록을 「연달아 올린 같은 섹션」 구간으로 끊는다.

    돌려주는 것은 [(섹션 코드, [회차…])] 이고 순서는 받은 그대로다. 길이 1인 구간과
    NO_SERIES 섹션은 묶음이 아니라 낱줄로 선다."""
    out = []
    for e in live:
        code = e['meta'].get('section', '')
        if out and out[-1][0] == code:
            out[-1][1].append(e)
        else:
            out.append((code, [e]))
    return out


def series_html(code, group):
    dates = [e['meta'].get('date', '') for e in group]
    return ('<div class="grp" data-sec="%s"><div class="ghead"><b>%s</b>'
            '<span>연달아 %d편 · %s ~ %s</span></div>%s</div>'
            % (code, sd.esc(SEC_NAME.get(code, code)), len(group), dates[-1], dates[0],
               ''.join(row_html(e, in_series=True) for e in group)))


def index_html(eps):
    live = [e for e in eps if e['lanes']]
    out = [sd.HEAD % ('씨모어 대시보드', sd.CSS + SECJS_CSS)]
    out.append('<h1>📈 채널 씨모어</h1>')
    out.append('<div class="sub">산업을 갈라 놓고 투자할 자리를 고르는 한국어 채널. '
               '회차마다 ⚖ 전략 판 하나가 선다 — 전사를 줄 번호로 대조해 쓴 해설이다.<br>'
               '글이 있는 회차만 싣는다 — 지금 %d편. 최신 회차가 맨 위이고, '
               '한 주제를 연달아 올린 구간은 한 덩어리로 묶인다.</div>' % len(live))
    stray = [e for e in live if e['meta'].get('section', '') not in dict(SECTIONS)]
    if stray:
        raise SystemExit('섹션 코드가 없는 회차: ' + ', '.join(e['slug'] for e in stray))
    counts = [(code, name, sum(1 for e in live if e['meta'].get('section', '') == code))
              for code, name in SECTIONS]
    out.append('<nav class="secnav"><a href="#" class="on" data-sec="">전체 '
               '<small>%d</small></a>%s</nav>'
               % (len(live), ''.join(
                   '<a href="#" data-sec="%s">%s <small>%d</small></a>' % (code, sd.esc(name), n)
                   for code, name, n in counts if n)))
    body = []
    for code, group in runs(live):
        if len(group) > 1 and code not in NO_SERIES:
            body.append(series_html(code, group))
        else:
            body.extend(row_html(e) for e in group)
    out.append('<div class="rows">%s</div>' % ''.join(body))
    out.append('<div class="foot">유튜브 자동 자막을 문장 단위로 끊어 전사로 두고, 그 줄 번호를 '
               '주소 삼아 판을 쓴다. 값이 전사에 있는지는 사람이 대조한다. '
               '정리일 <b>%s</b> · 페이지 생성은 <code>scratchpad/gen_seemore.py</code></div>' % STAMP)
    out.append('</div>')
    out.append(SECJS)
    return ''.join(out)


def check_ui(index, posts):
    """이 장의 규약. 아카이브 부품을 안 쓰므로 여기서 직접 본다."""
    bad = []
    if '<details' in index or any('<details' in p for p in posts):
        bad.append('접는 것이 있다 — 이 장은 목록과 글뿐이다')
    if re.search(r'<a class="row"(?![^>]*data-sec=)', index):
        bad.append('회차 줄에 섹션 표시가 없다 — 목록은 최신 순서 하나이고 섹션은 태그다')
    if 'class="sec"' in index:
        bad.append('섹션 머리줄이 있다 — 이 장의 목록은 섹션으로 안 나눈다')
    if 'class="grp"' not in index:
        bad.append('연달아 올린 구간이 안 묶였다 — 시리즈는 한 덩어리로 선다')
    if re.search(r'<div class="grp"(?:(?!</div>).)*<div class="grp"', index, re.S):
        bad.append('묶음 안에 묶음이 있다')
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
