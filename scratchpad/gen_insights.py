# 통합 인사이트 빌드 — content/understanding/통합/*.md → 대시보드 상단 섹션 주입
import re, io, os, glob, sys

DASH = r"C:\Users\y\semianalysis\대시보드\언더스탠딩 대시보드.html"
INS_DIR = r"C:\Users\y\semianalysis\content\understanding\통합"

def slugify(title):
    s = re.sub(r'<[^>]+>', '', title)                 # 태그 제거
    s = re.sub(r'[\s,·—…()\[\]?]+', '-', s.strip())    # 공백·기호 → 하이픈
    s = re.sub(r'[^0-9A-Za-z가-힣\-]', '', s)
    return re.sub(r'-+', '-', s).strip('-')[:60]

def parse_front_matter(raw):
    fm = {}
    key = None
    for line in raw.splitlines():
        m_item = re.match(r'^\s*-\s+(.*)$', line)
        if m_item and key:
            fm.setdefault(key, []).append(m_item.group(1).strip().strip('"'))
            continue
        m = re.match(r'^(\w+):\s*(.*)$', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"')
            fm[key] = val if val else []
    return fm

def _inline(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)

def md_to_html(body):
    out, in_ul = [], False
    for line in body.splitlines():
        h = re.match(r'^##\s+(.*)$', line)
        li = re.match(r'^-\s+(.*)$', line)
        if h:
            if in_ul: out.append('</ul>'); in_ul = False
            out.append('<h4>%s</h4>' % _inline(h.group(1).strip()))
        elif li:
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append('<li>%s</li>' % _inline(li.group(1).strip()))
        elif line.strip():
            if in_ul: out.append('</ul>'); in_ul = False
            out.append('<p>%s</p>' % _inline(line.strip()))
    if in_ul: out.append('</ul>')
    return '\n'.join(out)

def _text_of(h2_inner):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h2_inner)).strip()

def card_titles(html):
    return [_text_of(m) for m in re.findall(r'<h2>(.*?)</h2>', html, re.DOTALL)]

def inject_card_ids(html):
    id_map = {}
    seen = {}
    def repl(m):
        inner = m.group(1)
        title = _text_of(inner)
        if title in id_map:
            return m.group(0)
        base = 'card-' + slugify(title)
        sid = base
        n = seen.get(base, 0)
        if n: sid = '%s-%d' % (base, n + 1)
        seen[base] = n + 1
        id_map[title] = '#' + sid
        return '<h2 id="%s">%s</h2>' % (sid, inner)
    def keep(m):
        sid, inner = m.group(1), m.group(2)
        id_map[_text_of(inner)] = '#' + sid
        return m.group(0)
    html = re.sub(r'<h2 id="([^"]+)">(.*?)</h2>', keep, html, flags=re.DOTALL)
    html = re.sub(r'<h2>(.*?)</h2>', repl, html, flags=re.DOTALL)
    return html, id_map

def resolve_sources(titles, id_map):
    ok, miss = [], []
    for t in titles:
        key = re.sub(r'\s+', ' ', t).strip()
        if key in id_map: ok.append((t, id_map[key]))
        else: miss.append(t)
    return ok, miss
