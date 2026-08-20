# 소스 매니페스트 생성 — content/newsletter + content/understanding + content/linkedin 스캔
import os, re, io, json, hashlib, glob

ROOT = r"C:\Users\y\semianalysis"
BASES = [(os.path.join(ROOT, "content", "newsletter"), "semianalysis", "semi"),
         # 팟캐스트는 뉴스레터와 코퍼스를 나눈다 — 대담이라 숫자의 무게가 다르고,
         # 대시보드 ② 「뉴스레터 발행일순」에 섞이면 카드 이름과 안이 어긋난다
         (os.path.join(ROOT, "content", "podcast"), "podcast", "pod"),
         (os.path.join(ROOT, "content", "understanding"), "understanding", "und"),
         # 링크드인은 월별 묶음 파일이다(scripts/gen_li_source.py 생성물).
         # 글마다 파일을 두면 400개가 넘고, 인용은 어차피 줄 번호로 간다
         (os.path.join(ROOT, "content", "linkedin"), "linkedin", "li")]
OUT = os.path.join(ROOT, "insights", "manifest.json")
EXCLUDE_DIRS = ("통합",)  # understanding/통합 = Layer2 인사이트, 소스 아님

def slug(filename):
    s = re.sub(r'\.md$', '', filename)
    s = re.sub(r'^\[\d{6}\]\s*', '', s)                 # [YYMMDD] 접두 제거
    s = re.sub(r'[\s]+', '-', s.strip())
    s = re.sub(r'[^0-9A-Za-z가-힣\-]', '', s)
    return re.sub(r'-+', '-', s).strip('-')[:60]

def parse_date(filename, body):
    # 원본 발행일 전용 — 정리일(변환일)·created·updated는 절대 사용 안 함.
    # 1) 명시 발행일: '발행일 … YYYY-MM-DD' 또는 YAML 'published: YYYY-MM-DD'
    m = re.search(r'(?:발행일|published)[^\n]{0,8}?(\d{4}-\d{2}-\d{2})', body)
    if m: return m.group(1)
    # 2) 파일명 [YYMMDD] (뉴스레터 = 발행일)
    m = re.search(r'\[(\d{2})(\d{2})(\d{2})\]', filename)
    if m: return "20%s-%s-%s" % (m.group(1), m.group(2), m.group(3))
    # 3) 백브리핑 출처 줄의 날짜: '출처: … , YYYY-MM-DD'
    m = re.search(r'출처[^\n]*?(\d{4}-\d{2}-\d{2})', body)
    if m: return m.group(1)
    return None

OVERLAY = os.path.join(ROOT, "insights", "source_categories.json")

def strip_fm(text):
    # 앞머리 YAML frontmatter(---...---) 제거 → 본문만(태그·메타 편집이 hash 안 건드림)
    m = re.match(r'^---\n.*?\n---\n', text, re.DOTALL)
    return text[m.end():] if m else text

def body_hash(text):
    return hashlib.sha1(strip_fm(text).encode('utf-8')).hexdigest()[:12]

ABBR = {"semianalysis": "semi", "podcast": "pod", "understanding": "und", "linkedin": "li"}


def source_id(corpus, folder, filename):
    return "%s:%s:%s" % (ABBR.get(corpus, "und"), folder, slug(filename))

def read_categories(text, folder, sid, overlay):
    # ① frontmatter categories 다값 ② 오버레이 ③ 폴더 fallback
    m = re.search(r'^categories:\s*\[(.*?)\]', text, re.M)
    if m:
        cats = [c.strip().strip('"').strip("'") for c in m.group(1).split(',') if c.strip()]
        if cats: return cats
    if sid in overlay: return list(overlay[sid])
    return [folder]

def scan(bases, root=ROOT):
    overlay = json.load(io.open(OVERLAY, encoding='utf-8')) if os.path.exists(OVERLAY) else {}
    out = []
    for base, corpus, _ in bases:
        for p in glob.glob(os.path.join(base, '**', '*.md'), recursive=True):
            rel = os.path.relpath(p, base).replace('\\', '/')
            parts = rel.split('/')
            if any(d in EXCLUDE_DIRS for d in parts[:-1]):   # 통합 등 제외
                continue
            folder = parts[-2] if len(parts) >= 2 else 'root'
            name = parts[-1]
            text = io.open(p, encoding='utf-8').read()
            sid = source_id(corpus, folder, name)
            out.append({
                'id': sid, 'corpus': corpus, 'folder': folder,
                'categories': read_categories(text, folder, sid, overlay),
                'date': parse_date(name, text),
                'path': os.path.relpath(p, root).replace('\\', '/'),
                'hash': body_hash(text),
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
