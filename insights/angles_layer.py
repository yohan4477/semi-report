# -*- coding: utf-8 -*-
"""통합 인사이트 맨 위에 얹는 각도 층 — 원문에서 뽑은 조각이 글끼리 어떻게 붙나.

이 페이지의 취지가 「문서 여러 편을 가로질러야 보이는 것만 남긴다」라, 한 편에만 있는
항목은 안 싣는다. 붙는 주체와 성격 분포만 낸다.

재료는 insights/angles/*.md 다. 없으면 아무것도 안 낸다.
"""
import collections
import glob
import io
import os
import re

FRONT = re.compile(r'^---\n(.*?)\n---\n(.*)$', re.S)
TAG = re.compile(r'\[([^\[\]]+?)\s·\s([^\[\]]+?)\s·\s([^\[\]]+?)\s·\s([^\[\]]+?)\]')

CSS = r'''
  .ang{background:var(--card);border:1px solid var(--line);border-radius:var(--r);
       padding:12px 14px;margin-top:12px}
  .ang>summary{cursor:pointer;font-weight:800;font-size:var(--t-body);list-style:none}
  .ang>summary::-webkit-details-marker{display:none}
  .ang .amt{font-size:var(--t-meta);color:var(--faint);font-weight:600;margin-left:6px}
  .ang table{width:100%;border-collapse:collapse;font-size:var(--t-meta);margin-top:8px}
  .ang th,.ang td{text-align:left;padding:4px 8px;border-bottom:1px solid var(--line)}
  .ang th{color:var(--faint);font-weight:700}
  .achip{display:inline-block;font-size:var(--t-lbl);padding:1px 7px;margin:2px 3px 2px 0;
         border:1px solid var(--line);border-radius:999px;color:var(--faint)}
  .achip.on{border-color:var(--accent);color:var(--accent)}
'''


def _list(head, key):
    g = re.search(r'^%s:\s*\[(.*?)\]' % key, head, re.M)
    return [x.strip() for x in g.group(1).split(',')] if g else []


def read(root):
    """각도 파일들을 읽어 (문서 목록, 성격 개수)."""
    docs, kinds = [], collections.Counter()
    for f in sorted(glob.glob(os.path.join(root, 'insights', 'angles', '*.md'))):
        if os.path.basename(f).startswith('_'):
            continue
        m = FRONT.match(io.open(f, encoding='utf-8').read())
        if not m:
            continue
        head, body = m.group(1), m.group(2)
        d = re.search(r'^date:\s*(\S+)', head, re.M)
        n = 0
        for ln in body.split('\n'):
            if ln.startswith('|'):
                c = [x.strip() for x in ln.strip('|').split('|')]
                if len(c) >= 5 and c[0] != '대상' and not set(c[0]) <= set('-: '):
                    kinds[c[-1]] += 1
                    n += 1
            else:
                t = TAG.search(ln)
                if t:
                    kinds[t.group(4).strip()] += 1
                    n += 1
        docs.append({'date': d.group(1) if d else '',
                     'angles': _list(head, 'angles'),
                     'actors': _list(head, 'actors'), 'n': n})
    return docs, kinds


def layer(root):
    docs, kinds = read(root)
    if not docs:
        return ''

    acnt = collections.Counter(a for x in docs for a in x['angles'])
    byactor = collections.defaultdict(set)
    for x in docs:
        for a in x['actors']:
            byactor[a].add(x['date'][2:])
    joined = sorted(((a, t) for a, t in byactor.items() if len(t) > 1),
                    key=lambda kv: (-len(kv[1]), kv[0]))
    tot = sum(kinds.values())
    fact = kinds.get('사실', 0)

    o = ['<details class="ang"><summary>원문에서 뽑은 각도'
         '<span class="amt">글 %d · 각도 %d종 · 항목 %d</span></summary>'
         % (len(docs), len(acnt), tot)]
    o.append('<p class="sub">등뼈 넷(대상·때·출처·성격)으로 글끼리 붙는다. '
             '각도 이름은 미리 정하지 않고 글에서 자라게 둔다 — 테두리가 진한 것이 '
             '둘 이상의 글에 나온 각도다.</p>')
    for x in docs:
        o.append('<div style="margin-top:6px"><b class="amt">%s</b> ' % x['date'])
        for a in x['angles']:
            o.append('<span class="achip%s">%s</span>'
                     % (' on' if acnt[a] > 1 else '', a))
        o.append('</div>')
    if joined:
        o.append('<table><tr><th>글끼리 붙는 주체</th><th>나온 글</th></tr>')
        for a, t in joined:
            o.append('<tr><td>%s</td><td>%s</td></tr>' % (a, ' · '.join(sorted(t))))
        o.append('</table>')
    o.append('<p class="sub">항목 %d개 중 사실이 %d개다. 나머지 %d개는 저자가 세운 값이라 '
             '이 구분이 없으면 합칠 때 추정이 사실로 굳는다 — %s</p>'
             % (tot, fact, tot - fact,
                ' · '.join('%s %d' % (k, v) for k, v in kinds.most_common())))
    # 여기는 가로지르는 것만 싣는다. 항목 전체는 각도 지도가 갖는다 —
    # 사이트 빌드가 상대 링크를 슬러그나 github.io 절대 주소로 바꾼다(gen_site.rewrite_links)
    o.append('<p class="sub"><a href="각도 지도.html">각도 지도에서 항목 %d개를 각도별로 본다 →</a></p>'
             % tot)
    o.append('</details>')
    return ''.join(o)
