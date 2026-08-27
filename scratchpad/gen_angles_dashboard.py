# -*- coding: utf-8 -*-
"""각도 지도 — insights/angles/*.md 를 한 화면으로 낸다.

카드 대시보드가 아니다. 카드 규약(섹션 타일·render())을 따르지 않는다 — 여기 실리는
것은 카드가 아니라 원문에서 뽑은 각도이고, 카드 틀에 밀어 넣으면 값 없는 항목이
떨어진다. 그래서 조립을 따로 한다.

생성물이다. 고칠 것은 이 파일과 insights/angles/*.md 다.

  py -3.13 scratchpad/gen_angles_dashboard.py
"""
import collections
import glob
import html
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '대시보드', '각도 지도.html')

FRONT = re.compile(r'^---\n(.*?)\n---\n(.*)$', re.S)
TAG = re.compile(r'\[([^\[\]]+?)\s·\s([^\[\]]+?)\s·\s([^\[\]]+?)\s·\s([^\[\]]+?)\]')


def read_docs():
    docs = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'insights', 'angles', '*.md'))):
        base = os.path.basename(f)
        if base.startswith('_'):
            continue
        s = io.open(f, encoding='utf-8').read()
        m = FRONT.match(s)
        head, body = m.group(1), m.group(2)

        def one(k):
            g = re.search(r'^%s:\s*(.+)$' % k, head, re.M)
            return g.group(1).strip().strip('"') if g else ''

        def lst(k):
            g = re.search(r'^%s:\s*\[(.*?)\]' % k, head, re.M)
            return [x.strip() for x in g.group(1).split(',')] if g else []

        rows = []
        angle = None
        for ln in body.split('\n'):
            h = re.match(r'^##\s+(.+)$', ln)
            if h:
                angle = h.group(1).strip()
                continue
            if ln.startswith('|'):
                c = [x.strip() for x in ln.strip('|').split('|')]
                if len(c) >= 5 and c[0] not in ('대상',) and not set(c[0]) <= set('-: '):
                    rows.append({'angle': angle, '대상': c[0], '무엇': c[1],
                                 '값': c[2], '때': c[3], '성격': c[-1], 'kind': '표'})
                continue
            t = TAG.search(ln)
            if t:
                text = ln[:t.start()].strip()
                rows.append({'angle': angle, '대상': t.group(1).strip(),
                             '무엇': re.sub(r'\s{2,}', ' — ', text), '값': '',
                             '때': t.group(2).strip(), '성격': t.group(4).strip(),
                             'kind': '꼬리표'})

        docs.append({'file': base, 'title': (body.split('\n')[1] if len(body.split('\n')) > 1 else base).lstrip('# ').strip(),
                     'date': one('date'), 'kind': one('kind'),
                     'angles': lst('angles'), 'actors': lst('actors'),
                     'rows': rows, 'source': one('source')})
    return docs


def e(s):
    return html.escape(str(s))


CSS = '''
:root{--bg:#fff;--fg:#1a1a1a;--dim:#6b7280;--line:#e5e7eb;--ac:#1d4ed8;--warn:#b45309;--card:#fafafa}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1115;--fg:#e8eaed;--dim:#9aa0a6;--line:#2a2e37;--ac:#7aa2f7;--warn:#e0a458;--card:#161922}}
:root[data-theme=dark]{--bg:#0f1115;--fg:#e8eaed;--dim:#9aa0a6;--line:#2a2e37;--ac:#7aa2f7;--warn:#e0a458;--card:#161922}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.65 -apple-system,"Segoe UI","Malgun Gothic",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:28px 18px 80px}
h1{font-size:22px;margin:0 0 4px}
h2{font-size:17px;margin:34px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
.sub{color:var(--dim);font-size:13px;margin:0 0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card h3{margin:0 0 2px;font-size:15px}
.meta{color:var(--dim);font-size:12px;margin-bottom:8px}
.tags{display:flex;flex-wrap:wrap;gap:4px}
.tag{font-size:11px;padding:2px 7px;border:1px solid var(--line);border-radius:999px;color:var(--dim)}
.tag.hit{border-color:var(--ac);color:var(--ac)}
table{width:100%;border-collapse:collapse;font-size:13px}
.scroll{overflow-x:auto}
th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--dim);font-weight:600;font-size:12px}
td.n{white-space:nowrap;color:var(--dim)}
.k{font-size:11px;padding:1px 6px;border-radius:4px;border:1px solid var(--line);white-space:nowrap}
.k.사실{color:var(--ac);border-color:var(--ac)}
.k.추정,.k.가정,.k.전망{color:var(--warn);border-color:var(--warn)}
.bar{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:8px 0}
.bar i{display:block}
.legend{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--dim)}
.tl{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;white-space:pre-wrap;line-height:1.9}
details{border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:8px 0;background:var(--card)}
summary{cursor:pointer;font-weight:600;font-size:14px}
.note{color:var(--dim);font-size:13px}
'''


def build():
    docs = read_docs()
    rows = [r for d in docs for r in d['rows']]

    byactor = collections.defaultdict(set)
    for d in docs:
        for a in d['actors']:
            byactor[a].add(d['date'][2:])
    joined = sorted(((a, t) for a, t in byactor.items() if len(t) > 1),
                    key=lambda kv: (-len(kv[1]), kv[0]))

    angcnt = collections.Counter(a for d in docs for a in d['angles'])
    kinds = collections.Counter(r['성격'] for r in rows)
    total = sum(kinds.values())

    o = ['<title>각도 지도</title>', '<style>%s</style>' % CSS, '<div class="wrap">']
    o.append('<h1>각도 지도</h1>')
    o.append('<p class="sub">원문 %d편에서 뽑은 각도 %d종 · 항목 %d개. '
             '등뼈 넷(대상·때·출처·성격)으로 글끼리 붙는다.</p>'
             % (len(docs), len(angcnt), len(rows)))

    o.append('<h2>글</h2><div class="grid">')
    for d in docs:
        o.append('<div class="card"><h3>%s</h3>' % e(d['title']))
        o.append('<div class="meta">%s · %s · 각도 %d · 항목 %d</div>'
                 % (e(d['date']), e(d['kind']), len(d['angles']),
                    len(d['rows'])))
        o.append('<div class="tags">')
        for a in d['angles']:
            cls = 'tag hit' if angcnt[a] > 1 else 'tag'
            o.append('<span class="%s">%s</span>' % (cls, e(a)))
        o.append('</div></div>')
    o.append('</div>')
    o.append('<p class="note">테두리가 진한 각도는 둘 이상의 글에 나온 것이다. '
             '각도 이름은 미리 정하지 않고 글에서 자라게 둔다.</p>')

    o.append('<h2>글끼리 붙는 주체</h2>')
    o.append('<p class="note">각도 이름이 달라도 등뼈의 대상이 같으면 걸린다. '
             '주체 %d 중 %d 이 둘 이상의 글에 나온다.</p>'
             % (len(byactor), len(joined)))
    o.append('<div class="scroll"><table><tr><th>주체</th><th>나온 글</th></tr>')
    for a, t in joined:
        o.append('<tr><td>%s</td><td class="n">%s</td></tr>'
                 % (e(a), ' · '.join(sorted(t))))
    o.append('</table></div>')

    o.append('<h2>무엇이 사실이고 무엇이 저자가 만든 값인가</h2>')
    color = {'사실': 'var(--ac)', '추정': 'var(--warn)', '가정': '#dc2626',
             '전망': '#a855f7', '계획': '#16a34a', '제안': '#6b7280',
             '개념': '#0891b2', '발언': '#ca8a04'}
    o.append('<div class="bar">')
    for k, n in kinds.most_common():
        o.append('<i style="width:%.1f%%;background:%s"></i>'
                 % (100.0 * n / total, color.get(k, 'var(--dim)')))
    o.append('</div><div class="legend">')
    for k, n in kinds.most_common():
        o.append('<span><b style="color:%s">■</b> %s %d</span>'
                 % (color.get(k, 'var(--dim)'), e(k), n))
    o.append('</div>')
    fact = kinds.get('사실', 0)
    o.append('<p class="note">항목 %d개 중 사실은 %d개다. 나머지 %d개는 저자가 세운 값이라 '
             '이 구분이 없으면 합칠 때 추정이 사실로 굳는다.</p>'
             % (total, fact, total - fact))

    o.append('<h2>각도별 항목</h2>')
    for d in docs:
        o.append('<details><summary>%s <span class="meta">%s</span></summary>'
                 % (e(d['title']), e(d['date'])))
        byang = collections.OrderedDict()
        for r in d['rows']:
            byang.setdefault(r['angle'], []).append(r)
        for ang, rs in byang.items():
            o.append('<h3 style="font-size:13px;margin:12px 0 4px">%s</h3>' % e(ang))
            o.append('<div class="scroll"><table>')
            o.append('<tr><th>대상</th><th>무엇</th><th>값</th><th>때</th><th>성격</th></tr>')
            for r in rs:
                o.append('<tr><td class="n">%s</td><td>%s</td><td>%s</td>'
                         '<td class="n">%s</td><td><span class="k %s">%s</span></td></tr>'
                         % (e(r['대상']), e(r['무엇']), e(r['값']), e(r['때']),
                            e(r['성격']), e(r['성격'])))
            o.append('</table></div>')
        o.append('</details>')

    o.append('<p class="note">생성물이다. 고칠 것은 <code>scratchpad/gen_angles_dashboard.py</code> 와 '
             '<code>insights/angles/*.md</code> 다. 카드 대시보드가 아니라 카드 규약을 따르지 않는다.</p>')
    o.append('</div>')

    io.open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(o))
    print('%s · 글 %d · 각도 %d · 항목 %d · 붙는 주체 %d'
          % (os.path.basename(OUT), len(docs), len(angcnt), len(rows), len(joined)))


if __name__ == '__main__':
    build()
