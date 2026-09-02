# -*- coding: utf-8 -*-
"""Semi Doped 대시보드 — 목록 한 장과 회차마다 글 한 장.

카드가 없다. 접힘도 타일도 없다. 회차 목록에서 줄을 눌러 글로 들어가고,
글 페이지에는 그 회차에 대해 선 판만 실린다.

  판   전략(⚖) 컨설턴트 출신 애널리스트의 이슈 트리   ·   기술(🔧) 주제 + 순서·층위
       판은 주제가 서는 회차에만 생긴다. 둘 다 안 서면 그 줄은 링크가 안 걸린다.

  재료 content/understanding/Semi Doped/*.md   회차 메타와 한 줄
       insights/semidoped/<slug>-{strategy,tech}.md   받은 글 원본

  이 화면   py -3.13 scratchpad/gen_semidoped.py

규약은 이 파일 check_ui() 가 검사한다 — 접는 것 없음 · 판 없는 줄은 링크가
안 걸림 · 메타에 「언제 것」 · 타일 없음.
"""
import io
import os
import re
import sys
import html as _html

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import semidoped_figs  # noqa: E402
import check_fig  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'understanding', 'Semi Doped')
LANE_DIR = os.path.join(ROOT, 'insights', 'semidoped')
OUT = os.path.join(ROOT, '대시보드', 'Semi Doped 대시보드.html')
POST_DIR = os.path.join(ROOT, '대시보드', 'semidoped')
BLOB = 'https://github.com/johnn8n/semianalysis/blob/main/'

LANES = [('strategy', '⚖', '전략', '컨설턴트 출신 애널리스트의 이슈 트리'),
         ('tech', '🔧', '기술', '주제 아래 순서와 층위')]

# 회차가 아니라 모음인 글. 목록에 줄은 서되 판을 세우지 않는다
NOT_EPISODE = {'daily-2026-04-08': '월별 회차 목록',
               'til-14': '역사 토막 모음'}


def esc(s):
    return _html.escape(s, quote=False)


def blob(p):
    return BLOB + p.replace(' ', '%20')


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
            meta[k.strip()] = v.strip()
    return meta, md[end + 4:]


def one_line(body):
    """요약본의 「## 한 줄」 절 첫 문단. 없으면 gain 으로 갈음한다."""
    m = re.search(r'^## 한 줄\s*\n+(.+?)(?:\n\s*\n|\n## )', body, re.S | re.M)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


# ── 받은 글을 화면으로 ────────────────────────────────────────────────
# 표·문단·목록·굵게만 옮긴다. 도해는 받은 글에 없다 — 우리가 그려 semidoped_figs 에
# 두고, 절 제목 바로 아래(본문보다 앞)에 세운다. 그림을 보고 그 아래 글을 읽는 순서다.

def inline(s):
    s = esc(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    return s


def table_html(rows):
    head, body = rows[0], rows[2:]
    out = ['<table><thead><tr>']
    out += ['<th>%s</th>' % inline(c) for c in head]
    out.append('</tr></thead><tbody>')
    for r in body:
        out.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in r) + '</tr>')
    out.append('</tbody></table>')
    return ''.join(out)


def cells(ln):
    return [c.strip() for c in ln.strip().strip('|').split('|')]


def body_html(md, figs=()):
    """figs = [(절 제목 머리, 제목, svg, 캡션)]. 머리가 h2 제목의 앞부분과 같으면 그 제목
    바로 아래에 그림을 세운다. 안 걸린 그림은 오류다 — 절 번호가 바뀌면 그림이 소리 없이
    사라지는 일을 막는다."""
    lines = md.split('\n')
    out, i, para, items = [], 0, [], []
    pending = list(figs)

    def figs_under(title):
        hit = [f for f in pending if title.startswith(f[0])]
        for f in hit:
            pending.remove(f)
            out.append(semidoped_figs.fig_html(f))

    def flush():
        if para:
            out.append('<p>%s</p>' % inline(' '.join(para)))
            del para[:]
        if items:
            out.append('<ul>%s</ul>' %
                       ''.join('<li>%s</li>' % inline(x) for x in items))
            del items[:]

    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):
            # 펜스 블록 — 구조 절의 트리가 여기로 온다. 줄바꿈과 들여쓰기가 뜻이라
            # 문단으로 합치면 안 된다. 2026-09-02 에 이걸 안 잡아 트리가 인라인 코드
            # 한 문단으로 나갔다
            flush()
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(esc(lines[i]))
                i += 1
            out.append('<pre class="tree">%s</pre>' % '\n'.join(code))
            i += 1
            continue
        if ln.strip().startswith('|') and i + 1 < len(lines) and \
                set(lines[i + 1].replace('|', '').strip()) <= set('-: '):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(cells(lines[i]))
                i += 1
            out.append('<div class="tw">%s</div>' % table_html(rows))
            continue
        if ln.startswith('## '):
            flush()
            out.append('<h2>%s</h2>' % inline(ln[3:].strip()))
            figs_under(ln[3:].strip())
        elif ln.startswith('### '):
            flush()
            out.append('<h3>%s</h3>' % inline(ln[4:].strip()))
            figs_under(ln[4:].strip())
        elif re.match(r'^\s*[-*] ', ln):
            if para:
                out.append('<p>%s</p>' % inline(' '.join(para)))
                del para[:]
            items.append(re.sub(r'^\s*[-*] ', '', ln).strip())
        elif not ln.strip():
            flush()
        else:
            if items:
                out.append('<ul>%s</ul>' %
                           ''.join('<li>%s</li>' % inline(x) for x in items))
                del items[:]
            para.append(ln.strip())
        i += 1
    flush()
    if pending:
        raise SystemExit('도해가 설 절이 없다: %s' % ', '.join(f[0] for f in pending))
    return '\n'.join(out)


# ── 재료 읽기 ────────────────────────────────────────────────────────

def episodes():
    eps = []
    for name in sorted(os.listdir(SRC)):
        if not name.endswith('.md'):
            continue
        slug = name[:-3]
        meta, body = front(io.open(os.path.join(SRC, name), encoding='utf-8').read())
        lanes = []
        for key, emo, label, sub in LANES:
            path = os.path.join(LANE_DIR, '%s-%s.md' % (slug, key))
            if os.path.exists(path):
                lmeta, lbody = front(io.open(path, encoding='utf-8').read())
                lanes.append({'key': key, 'emo': emo, 'label': label, 'sub': sub,
                              'meta': lmeta, 'body': lbody,
                              'src': 'insights/semidoped/%s-%s.md' % (slug, key)})
        eps.append({'slug': slug, 'meta': meta, 'lanes': lanes,
                    'one': one_line(body),
                    'note': NOT_EPISODE.get(slug, ''),
                    'raw': 'content/understanding/Semi Doped/%s.md' % slug})
    eps.sort(key=lambda e: e['meta'].get('date', ''), reverse=True)
    return eps


CSS = '''
*{box-sizing:border-box}
body{margin:0;background:#f6f7f9;color:#1b1f27;
 font:15px/1.75 -apple-system,"Segoe UI","Malgun Gothic",sans-serif}
a{color:inherit}
.wrap{max-width:900px;margin:0 auto;padding:36px 20px 80px}
h1{font-size:26px;margin:0 0 6px}
.sub{color:#66707f;font-size:13px;margin:0 0 28px;line-height:1.7}
.rows{border-top:1px solid #e2e5ea}
.row{display:block;padding:16px 4px;border-bottom:1px solid #e2e5ea;
 text-decoration:none;color:inherit}
a.row:hover{background:#eef1f6}
.rmeta{font-size:12px;color:#8a93a1;display:flex;gap:10px;flex-wrap:wrap}
.rtitle{font-size:16px;font-weight:600;margin:3px 0 4px;line-height:1.5}
.rone{font-size:13px;color:#5b6472;line-height:1.7}
.tags{display:flex;gap:5px;margin-top:7px;flex-wrap:wrap}
.tag{font-size:11px;padding:2px 8px;border-radius:11px;background:#e7ebf1;color:#4c5563}
.tag.on{background:#1b1f27;color:#fff}
.row.dead{opacity:.62}
.why{font-size:12px;color:#8a93a1;margin-top:6px}
.back{display:inline-block;font-size:13px;color:#66707f;margin-bottom:18px;
 text-decoration:none}
.pmeta{font-size:12px;color:#8a93a1;line-height:1.9;margin:0 0 26px;
 padding-bottom:18px;border-bottom:1px solid #e2e5ea}
.lane{margin:0 0 44px}
.lhead{display:flex;align-items:baseline;gap:9px;margin:0 0 4px}
.lhead b{font-size:19px}
.lhead span{font-size:12px;color:#8a93a1}
.ltitle{font-size:15px;font-weight:600;line-height:1.6;margin:10px 0 20px;
 padding:12px 14px;background:#fff;border-left:3px solid #1b1f27;border-radius:0 6px 6px 0}
.lane h2{font-size:17px;margin:30px 0 10px;line-height:1.5}
.lane h3{font-size:15px;margin:22px 0 8px}
.lane p{margin:0 0 14px}
.lane ul{margin:0 0 14px;padding-left:20px}
.lane li{margin:0 0 6px}
code{background:#e9edf2;padding:1px 5px;border-radius:4px;font-size:.9em}
pre.tree{margin:0 0 18px;padding:14px 16px;background:#fff;border:1px solid #dfe3e9;border-radius:8px;
 font:13px/1.65 Consolas,"D2Coding","Malgun Gothic",monospace;overflow-x:auto;white-space:pre}
.tw{overflow-x:auto;margin:0 0 18px}
table{border-collapse:collapse;font-size:13px;background:#fff;min-width:100%}
th,td{border:1px solid #dfe3e9;padding:7px 10px;text-align:left;vertical-align:top}
th{background:#eef1f6;font-weight:600;white-space:nowrap}
.foot{margin-top:40px;font-size:12px;color:#8a93a1;line-height:1.9}
''' + semidoped_figs.CSS

HEAD = ('<!doctype html><html lang="ko"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>%s</title><style>%s</style><div class="wrap">')


def row_html(ep):
    m = ep['meta']
    tags = []
    for key, emo, label, _sub in LANES:
        on = any(l['key'] == key for l in ep['lanes'])
        tags.append('<span class="tag%s">%s %s</span>'
                    % (' on' if on else '', emo, label))
    inner = ('<div class="rmeta"><span>%s</span><span>%s</span></div>'
             '<div class="rtitle">%s</div>'
             % (esc(m.get('date', '')), esc(m.get('speaker', '')),
                esc(m.get('title', ep['slug']))))
    if ep['one']:
        inner += '<div class="rone">%s</div>' % esc(ep['one'])
    inner += '<div class="tags">%s</div>' % ''.join(tags)
    if ep['lanes']:
        return '<a class="row" href="semidoped/%s.html">%s</a>' % (ep['slug'], inner)
    why = ep['note'] or '아직 판이 안 섰다'
    inner += '<div class="why">글 없음 — %s</div>' % esc(why)
    return '<div class="row dead">%s</div>' % inner


def post_html(ep):
    m = ep['meta']
    out = [HEAD % (esc(m.get('title', ep['slug'])) + ' — Semi Doped', CSS)]
    out.append('<a class="back" href="../Semi Doped 대시보드.html">← 회차 목록</a>')
    out.append('<h1>%s</h1>' % esc(m.get('title', ep['slug'])))
    out.append('<div class="pmeta">%s · %s<br>원문 <a href="%s">%s</a> · '
               '요약본 <a href="%s">저장소</a></div>'
               % (esc(m.get('date', '')), esc(m.get('speaker', '')),
                  esc(m.get('source', '')), esc(m.get('source', '')),
                  blob(ep['raw'])))
    for lane in ep['lanes']:
        lm = lane['meta']
        out.append('<div class="lane">')
        out.append('<div class="lhead"><b>%s %s 판</b><span>%s · %s 가 씀</span></div>'
                   % (lane['emo'], lane['label'], esc(lane['sub']),
                      esc(lm.get('model', ''))))
        if lm.get('title'):
            out.append('<div class="ltitle">%s</div>' % esc(lm['title']))
        out.append(body_html(lane['body'],
                             semidoped_figs.figs_for(ep['slug'], lane['key'])))
        out.append('<div class="foot">받은 글을 문장 그대로 싣는다. '
                   '원본 <a href="%s">%s</a> · 페르소나 %s</div>'
                   % (blob(lane['src']), esc(lane['src']),
                      esc(lm.get('persona', ''))))
        out.append('</div>')
    out.append('</div>')
    return ''.join(out)


def index_html(eps):
    live = sum(1 for e in eps if e['lanes'])
    out = [HEAD % ('Semi Doped 대시보드', CSS)]
    out.append('<h1>🎙️ Semi Doped</h1>')
    out.append('<div class="sub">칩을 만드는 사람이 나와 앉아 설계를 말하는 팟캐스트. '
               '회차마다 두 판이 따로 읽는다 — ⚖ 전략은 컨설턴트 출신 애널리스트의 이슈 트리로, '
               '🔧 기술은 주제 아래 순서와 층위로.<br>'
               '판은 주제가 서는 회차에만 생긴다. 안 선 회차는 줄만 서고 열리지 않는다 — '
               '회차 %d편 중 %d편에 글이 있다.</div>' % (len(eps), live))
    out.append('<div class="rows">%s</div>' % ''.join(row_html(e) for e in eps))
    out.append('<div class="foot">글은 원문 전사를 통째로 읽힌 뒤 받은 것이고 '
               '문장을 고치지 않는다. 값이 원문에 있는지는 사람이 대조한다.</div>')
    out.append('</div>')
    return ''.join(out)


def check_ui(index, posts):
    """이 장의 규약. 워치 장처럼 아카이브 부품을 안 쓰므로 여기서 직접 본다."""
    bad = []
    if '<details' in index or any('<details' in p for p in posts):
        bad.append('접는 것이 있다 — 이 장은 목록과 글뿐이다')
    if 'class="tile' in index:
        bad.append('타일이 있다 — 첫 화면은 회차 줄이다')
    for p in posts:
        if 'class="pmeta"' not in p:
            bad.append('글 페이지에 회차 메타(언제 것·누가)가 없다')
        if '<code>```' in p or '├─' in re.sub(r'<pre[^>]*>.*?</pre>', '', p, flags=re.S):
            bad.append('트리가 <pre> 밖으로 나갔다 — 펜스가 문단으로 뭉개졌다')
        if '회차 목록' not in p:
            bad.append('글 페이지에서 목록으로 돌아갈 길이 없다')
    dead = re.findall(r'<div class="row dead">(.*?)</div>\s*(?=<a class="row"|'
                      r'<div class="row|</div>)', index, re.S)
    for d in dead:
        if '글 없음' not in d:
            bad.append('판이 없는 줄에 이유가 안 적혔다')
    if re.search(r'<a class="row"[^>]*>(?:(?!</a>).)*글 없음', index, re.S):
        bad.append('판이 없는 줄에 링크가 걸렸다')
    return bad


def check_figs():
    """도해 규칙 둘을 생성 때 기계로 본다 — 글자에 든 값이 전사에 있나, 배치가 겹치나.
    도형 개수가 값인지는 사람이 본다."""
    bad = []
    for (slug, lane), figs in semidoped_figs.FIGS.items():
        for key, title, svg, _cap in figs:
            miss = semidoped_figs.missing_values(slug, svg)
            if miss:
                bad.append('%s/%s %s — 전사에 없는 값 %s' % (slug, lane, title, miss))
            # 엄격 모드로 본다(줄임말·비스듬한 선까지). 화살촉 마커는 <defs> 안 path 라
            # 비스듬한 선으로 읽히므로 defs 만 걷고 잰다
            bare = re.sub(r'<defs>.*?</defs>', '', svg, flags=re.S)
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
    live = sum(1 for e in eps if e['lanes'])
    lanes = sum(len(e['lanes']) for e in eps)
    print('Semi Doped — 회차 %d줄 · 글 %d장 · 판 %d개  ->  %s'
          % (len(eps), live, lanes, os.path.basename(OUT)))


if __name__ == '__main__':
    main()
