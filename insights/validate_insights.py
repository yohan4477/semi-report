# provenance 무결성 검사
import os, io, json, sys
import coverage as cov

ROOT = r"C:\Users\y\semianalysis"
MAN_PATH = os.path.join(ROOT, "insights", "manifest.json")

def validate(manifest, clusters):
    ids = {s['id'] for s in manifest['sources']}
    errs = []
    for c in clusters:
        if not c['cluster_id']:
            errs.append('cluster_id 없음(frontmatter 깨짐)')
        for sid in c['sources']:
            if sid not in ids:
                errs.append('%s: 존재하지 않는 소스 %s' % (c['cluster_id'] or '?', sid))
    return errs

def main():
    manifest = json.load(io.open(MAN_PATH, encoding='utf-8'))
    errs = validate(manifest, cov.load_clusters())
    for e in errs: print('ERROR', e)
    print('validate: %d errors' % len(errs))
    sys.exit(1 if errs else 0)

if __name__ == '__main__':
    main()
