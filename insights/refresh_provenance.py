# 클러스터 provenance 갱신 — source_hashes·source_dates·as_of를 manifest에서 재계산(단일줄).
# sources 목록은 유지, 파생 필드만 새로고침. 소스 내용/발행일 변경 후 실행.
import os, re, io, json, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coverage as cov

ROOT = r"C:\Users\y\semianalysis"
MAN = os.path.join(ROOT, "insights", "manifest.json")
CLUSTERS = os.path.join(ROOT, "insights", "clusters")

def refresh():
    man = json.load(io.open(MAN, encoding='utf-8'))
    hsh = {s['id']: s['hash'] for s in man['sources']}
    dat = {s['id']: s['date'] for s in man['sources']}
    for p in sorted(glob.glob(os.path.join(CLUSTERS, '*.md'))):
        t = io.open(p, encoding='utf-8').read()
        c = cov.parse_cluster(t)
        srcs = c['sources']
        miss = [s for s in srcs if s not in hsh]
        sh = {s: hsh.get(s, 'MISSING') for s in srcs}
        sd = {s: dat.get(s) for s in srcs}
        dates = [d for d in sd.values() if d]
        as_of = max(dates) if dates else ''
        # 기존 파생 3줄 제거 후 sources 줄 뒤에 새로 삽입
        t = re.sub(r'^(source_hashes|source_dates|as_of):.*\n', '', t, flags=re.M)
        block = ('source_hashes: %s\n' % json.dumps(sh, ensure_ascii=False)
                 + 'source_dates: %s\n' % json.dumps(sd, ensure_ascii=False)
                 + 'as_of: %s\n' % as_of)
        t = re.sub(r'^(sources:.*\n)', r'\1' + block, t, count=1, flags=re.M)
        io.open(p, 'w', encoding='utf-8').write(t)
        print(os.path.basename(p), '| as_of', as_of, '| MISS' if miss else '', miss or '')

if __name__ == '__main__':
    refresh()
