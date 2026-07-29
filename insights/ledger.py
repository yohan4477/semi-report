# 대장(숫자·예측) 파서 — 문서 단위 섹션을 표 행으로 분해해 인사이트 산출물에서 재사용
import os, re, io

ROOT = r"C:\Users\y\semianalysis"
NUM = os.path.join(ROOT, "대장", "숫자 대장.md")
PRED = os.path.join(ROOT, "대장", "예측 대장.md")

SEC = re.compile(r'^## (\[\d{6}\] .+?)\s*$', re.M)


def _sections(path):
    """## [YYMMDD] 제목 → 그 아래 표 행들. 문서 stem을 키로 반환."""
    if not os.path.exists(path):
        return {}
    t = io.open(path, encoding='utf-8').read()
    out, ms = {}, list(SEC.finditer(t))
    for i, m in enumerate(ms):
        body = t[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(t)]
        rows = []
        for line in body.splitlines():
            line = line.strip()
            if not line.startswith('|') or set(line) <= set('|-: '):
                continue
            cells = [c.strip().replace('\\~', '~') for c in line.strip('|').split('|')]
            if cells and cells[0] in ('지표', '예측 내용'):
                continue
            rows.append(cells)
        if rows:
            out[m.group(1)] = rows
    return out


def load():
    return _sections(NUM), _sections(PRED)


def stem(path):
    """manifest의 path → 대장 섹션 키(= 파일명에서 확장자 뗀 것)."""
    return os.path.splitext(os.path.basename(path))[0]


STATUS = {'✅': ('hit', '적중'), '🔶': ('part', '부분'), '❌': ('miss', '빗나감'), '⏳': ('wait', '미도래')}


def status_of(cell):
    for k, v in STATUS.items():
        if k in cell:
            return v
    return ('wait', cell.strip() or '미도래')


if __name__ == '__main__':
    n, p = load()
    print('숫자 대장 문서 %d개 / 행 %d' % (len(n), sum(len(v) for v in n.values())))
    print('예측 대장 문서 %d개 / 행 %d' % (len(p), sum(len(v) for v in p.values())))
