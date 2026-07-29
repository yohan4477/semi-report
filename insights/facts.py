# 코퍼스 원문에서 사실 추출 — 대장 등재 여부와 무관하게 모든 근거 문서를 커버한다.
# semi 문서: 섹션마다 붙는 **📌 핵심:** 불릿 / und 문서: ## 주요 숫자 표
import os, re, io

ROOT = r"C:\Users\y\semianalysis"
HAS_NUM = re.compile(r'\d')
SEC_H = re.compile(r'^##\s+(?:\d+\.\s*)?(.+?)\s*$')


def _semi(text):
    """**📌 핵심:** 블록의 불릿 중 수치가 든 것만. 섹션 제목을 맥락으로."""
    rows, sec, in_blk = [], '', False
    for line in text.splitlines():
        h = SEC_H.match(line)
        if h:
            t = h.group(1)
            if not t.startswith(('📑', '🔑')):
                sec = re.sub(r'^[^:]*:\s*', '', t).strip() or t.strip()
            in_blk = False
            continue
        if line.startswith('**📌'):
            in_blk = '핵심' in line
            continue
        if in_blk:
            m = re.match(r'^-\s+(.*)$', line)
            if not m:
                if line.strip() and not line.startswith('-'):
                    in_blk = False
                continue
            f = m.group(1).strip()
            if f.startswith('결론:') or not HAS_NUM.search(f):
                continue
            rows.append((f, sec))
    return rows


def _und(text):
    """## 주요 숫자 표: | 수치 | 의미 |"""
    m = re.search(r'^## 주요 숫자\s*\n(.*?)(?=\n## |\Z)', text, re.M | re.DOTALL)
    if not m:
        return []
    rows = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith('|') or set(line) <= set('|-: '):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 2 or cells[0] in ('수치', '지표'):
            continue
        rows.append(('**%s** — %s' % (cells[0], cells[1]), ''))
    return rows


def rows(path):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        return []
    t = io.open(p, encoding='utf-8').read()
    return _und(t) if '/understanding/' in path.replace('\\', '/') else _semi(t)


if __name__ == '__main__':
    import json, glob
    man = json.load(io.open(os.path.join(ROOT, 'insights', 'manifest.json'), encoding='utf-8'))['sources']
    tot = empty = 0
    for s in man:
        r = rows(s['path'])
        tot += len(r)
        if not r:
            empty += 1
            print('EMPTY:', s['path'])
    print('문서 %d편 / 사실 %d행 / 빈 문서 %d편' % (len(man), tot, empty))
