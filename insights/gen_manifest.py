# 소스 매니페스트 생성 — content/newsletter + content/understanding 스캔
import os, re, io, json, hashlib, glob

ROOT = r"C:\Users\y\semianalysis"
BASES = [(os.path.join(ROOT, "content", "newsletter"), "semianalysis", "semi"),
         (os.path.join(ROOT, "content", "understanding"), "understanding", "und")]
OUT = os.path.join(ROOT, "insights", "manifest.json")
EXCLUDE_DIRS = ("통합",)  # understanding/통합 = Layer2 인사이트, 소스 아님

def slug(filename):
    s = re.sub(r'\.md$', '', filename)
    s = re.sub(r'^\[\d{6}\]\s*', '', s)                 # [YYMMDD] 접두 제거
    s = re.sub(r'[\s]+', '-', s.strip())
    s = re.sub(r'[^0-9A-Za-z가-힣\-]', '', s)
    return re.sub(r'-+', '-', s).strip('-')[:60]

def parse_date(filename, body):
    m = re.search(r'\[(\d{2})(\d{2})(\d{2})\]', filename)
    if m: return "20%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
    m = re.search(r'^(?:published|updated):\s*(\d{4}-\d{2}-\d{2})', body, re.M)
    return m.group(1) if m else None

def body_hash(text):
    return hashlib.sha1(text.encode('utf-8')).hexdigest()[:12]

def source_id(corpus, category, filename):
    abbr = "semi" if corpus == "semianalysis" else "und"
    return "%s:%s:%s" % (abbr, category, slug(filename))

def scan(bases, root=ROOT):
    out = []
    for base, corpus, _ in bases:
        for p in glob.glob(os.path.join(base, '**', '*.md'), recursive=True):
            rel = os.path.relpath(p, base).replace('\\', '/')
            parts = rel.split('/')
            if any(d in EXCLUDE_DIRS for d in parts[:-1]):   # 통합 등 제외
                continue
            category = parts[-2] if len(parts) >= 2 else 'root'
            name = parts[-1]
            body = io.open(p, encoding='utf-8').read()
            out.append({
                'id': source_id(corpus, category, name),
                'corpus': corpus, 'category': category,
                'date': parse_date(name, body),
                'path': os.path.relpath(p, root).replace('\\', '/'),
                'hash': body_hash(body),
            })
    return sorted(out, key=lambda s: s['id'])

def main():
    import datetime
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    data = {'generated': datetime.date.today().isoformat(), 'sources': scan(BASES)}
    io.open(OUT, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=1))
    print('OK: %d sources -> %s' % (len(data['sources']), OUT))

if __name__ == '__main__':
    main()
