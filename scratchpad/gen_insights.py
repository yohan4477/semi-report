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
