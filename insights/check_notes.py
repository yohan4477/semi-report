# 노트와 서술의 인용을 검사한다. 원자 검사기(C1~C21)를 대신하되 실제로
# 인용한 줄만 본다 — 모든 문장을 미리 분해해 두지 않아서 훨씬 싸다.
import io, os, re, sys, json, glob
import paths
import notes_lib as nl

MAXKB = 3.0
NUM = re.compile(r'\d')
ROW = re.compile(r'^\s*-\s+(.+)$', re.M)


def check_file(path, text, lock):
    out = []
    meta, body = nl.parse_front(text)
    src = nl.sources_of(meta)
    if not src:
        out.append(('FAIL', path, 'N1', 'frontmatter에 source/sources가 없다'))
        return out
    for s in src:
        if not os.path.isfile(nl.abspath(s['file'])):
            out.append(('FAIL', path, 'N1', '원문이 없다: %s' % s['file']))

    for r in nl.cite_refs(body, src):
        if not r['ok']:
            out.append(('FAIL', path, 'N2', '라벨을 못 푼다: %s' % r['label']))
            continue
        ap = nl.abspath(r['file'])
        for n in r['lines']:
            h = nl.line_hash(ap, n)
            if h is None:
                out.append(('FAIL', path, 'N3',
                            '%s에 %d번 줄이 없다' % (r['file'], n)))
                continue
            key = '%s#L%d' % (r['file'], n)
            old = (lock.get(key) or {}).get('sha1')
            if old and old != h:
                out.append(('WARN', path, 'N4',
                            '원문이 바뀌었다 — 다시 볼 것: %s' % key))
            lock[key] = {'sha1': h}

    # 3KB 상한은 노트에만 건다. 추적·인사이트 서술은 원래 길다
    if '/notes/' in path and len(text.encode('utf-8')) > MAXKB * 1024:
        out.append(('WARN', path, 'N5',
                    '노트가 %.1fKB — %.0fKB를 넘으면 원문을 다시 읽는 편이 낫다'
                    % (len(text.encode('utf-8')) / 1024.0, MAXKB)))

    m = re.search(r'^## 수치\s*\n(.*?)(?=\n## |\Z)', body, re.S | re.M)
    if m:
        for row in ROW.findall(m.group(1)):
            if not nl.CITE.search(row):
                out.append(('FAIL', path, 'N6', '수치에 인용이 없다: %s' % row[:40]))

    for para in re.split(r'\n\s*\n', body):
        p = para.strip()
        if p.startswith('#') or p.startswith('-') or len(p) < 40:
            continue
        if NUM.search(p) and not nl.CITE.search(p):
            out.append(('WARN', path, 'N7', '숫자가 있는데 인용이 없다: %s' % p[:40]))
    return out


def main(write_lock=True):
    lock = {}
    if os.path.isfile(paths.CITES):
        lock = json.load(io.open(paths.CITES, encoding='utf-8'))
    findings, n = [], 0
    # synth·theses는 Task 5(참조 치환)가 끝난 뒤에 넣는다. 지금 넣으면
    # sources: frontmatter가 없어 전부 N1 FAIL이 난다
    for d in (paths.NOTES, paths.TRACKS):
        for p in sorted(glob.glob(os.path.join(d, '*.md'))):
            n += 1
            rel = os.path.relpath(p, paths.ROOT).replace(os.sep, '/')
            findings += check_file(rel, io.open(p, encoding='utf-8').read(), lock)
    for lv, where, rule, msg in findings:
        print('%s %s [%s] %s' % (lv, os.path.basename(where), rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    warns = len(findings) - fails
    print('요약: 문서 %d편 / FAIL %d / WARN %d' % (n, fails, warns))
    if write_lock:
        json.dump(lock, io.open(paths.CITES, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1, sort_keys=True)
    return fails


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
