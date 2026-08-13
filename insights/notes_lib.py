# 인용 한 가지만 다룬다 — (라벨 L123)을 파싱하고, 라벨을 원문 파일로 풀고,
# 그 줄의 해시를 낸다. 검사기·렌더러·마이그레이션이 이 파일만 공유한다.
import io, os, re, hashlib
import paths

FRONT_RE = re.compile(r'^---\n(.*?)\n---\n(.*)$', re.S)
SRC_RE = re.compile(r'^\s*-\s*\{(.+)\}\s*$', re.M)
KV_RE = re.compile(r'(\w+):\s*"([^"]*)"')
META_RE = re.compile(r'^(\w+):\s*(.+)$', re.M)

# 라벨은 사람이 줄여 쓴 이름, 뒤는 L12 또는 L51, L60 형태.
# 상한이 80자였을 때 마이그레이션이 만든 긴 파일명 인용(「[260416] ISSCC 2026
# 총정리 - HBM4, LPDDR6, CPO, 액티브 LSI 등…」)을 통째로 놓쳤다
CITE = re.compile(r'\(([^()]{2,160}?)\s*(L\d[\d,\sL–-]*)\)')


def parse_front(text):
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    head, body = m.group(1), m.group(2)
    meta = {k: v.strip() for k, v in META_RE.findall(head)}
    meta['_head'] = head
    return meta, body


def sources_of(meta):
    out = []
    head = meta.get('_head', '')
    for line in SRC_RE.findall(head):
        d = dict(KV_RE.findall(line))
        if d.get('file'):
            d['base'] = os.path.basename(d['file']).rsplit('.md', 1)[0]
            out.append(d)
    single = meta.get('source', '').strip().strip('"')
    if single and not out:
        out.append({'file': single,
                    'base': os.path.basename(single).rsplit('.md', 1)[0],
                    'date': meta.get('date', ''), 'note': ''})
    return out


def resolve(label, sources):
    """앞머리 일치를 먼저 보고, 없으면 부분 일치. 사람이 줄여 쓴 라벨은
    파일명 앞머리와 안 맞는 경우가 흔하다(예: [251231]로 시작하는 파일)."""
    key = label.strip().rstrip(',')[:18]
    if not key:
        return None
    for s in sources:
        if s['base'].startswith(key):
            return s
    for s in sources:
        if key in s['base']:
            return s
    return None


def cite_refs(body, sources):
    out = []
    for m in CITE.finditer(body):
        label, lines = m.group(1), m.group(2)
        hit = resolve(label, sources)
        out.append({'label': label.strip(),
                    'file': hit['file'] if hit else None,
                    'lines': [int(x) for x in re.findall(r'L(\d+)', lines)],
                    'ok': hit is not None})
    return out


def line_hash(abs_path, n):
    if not os.path.isfile(abs_path):
        return None
    with io.open(abs_path, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            if i == n:
                return hashlib.sha1(line.strip().encode('utf-8')).hexdigest()[:12]
    return None


def abspath(rel):
    return os.path.join(paths.ROOT, rel.replace('/', os.sep))
