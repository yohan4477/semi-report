# 커버리지 diff — manifest ↔ clusters
import os, re, io, json, glob, sys

ROOT = r"C:\Users\y\semianalysis"
MAN_PATH = os.path.join(ROOT, "insights", "manifest.json")
CLUSTERS = os.path.join(ROOT, "insights", "clusters")
REPORT = os.path.join(ROOT, "insights", "coverage_report.md")

def parse_cluster(md_text):
    m = re.match(r'^---\n(.*?)\n---', md_text, re.DOTALL)
    fm = m.group(1) if m else ''
    def scal(k):
        mm = re.search(r'^%s:\s*(.*)$' % k, fm, re.M)
        return mm.group(1).strip().strip('"') if mm else ''
    def lst(k):
        mm = re.search(r'^%s:\s*\[(.*)\]\s*$' % k, fm, re.M)
        if not mm: return []
        return [x.strip().strip('"').strip("'") for x in mm.group(1).split(',') if x.strip()]
    def hashes():
        mm = re.search(r'^source_hashes:\s*(\{.*\})\s*$', fm, re.M)
        if not mm: return {}
        try: return json.loads(mm.group(1))
        except Exception: return {}
    return {'cluster_id': scal('cluster_id'), 'categories': lst('categories'),
            'sources': lst('sources'), 'source_hashes': hashes()}

def load_clusters():
    out = []
    for p in sorted(glob.glob(os.path.join(CLUSTERS, '*.md'))):
        out.append(parse_cluster(io.open(p, encoding='utf-8').read()))
    return out

def load_taxonomy():
    p = os.path.join(ROOT, "insights", "taxonomy.json")
    return json.load(io.open(p, encoding='utf-8')) if os.path.exists(p) else {}

def expand(cats, tax):
    # 카테고리 집합을 자손까지 확장(계층 매칭). tax = {parent:[children]}
    out, stack = set(), list(cats)
    while stack:
        c = stack.pop()
        if c in out: continue
        out.add(c)
        stack += tax.get(c, [])
    return out

def _cats(s):
    return s.get('categories') or ([s['category']] if s.get('category') else [])

def classify(manifest, clusters, full=False, tax=None):
    tax = tax if tax is not None else load_taxonomy()
    by_id = {s['id']: s for s in manifest['sources']}
    covered = set()
    stale = {}
    for c in clusters:
        covered |= set(c['sources'])
        routed = expand(c['categories'], tax)   # 이 클러스터가 흡수하는 카테고리(자손 포함)
        reasons = []
        for sid in c['sources']:
            if sid not in by_id: reasons.append('삭제:%s' % sid)
            elif c['source_hashes'].get(sid) != by_id[sid]['hash']: reasons.append('변경:%s' % sid)
        for s in manifest['sources']:
            if (set(_cats(s)) & routed) and s['id'] not in c['sources']:
                reasons.append('신규:%s' % s['id'])
        if reasons: stale[c['cluster_id']] = reasons
    all_routed = set()
    for c in clusters: all_routed |= expand(c['categories'], tax)
    uncovered = [s['id'] for s in manifest['sources']
                 if s['id'] not in covered and not (set(_cats(s)) & all_routed)]
    ok = [c['cluster_id'] for c in clusters if c['cluster_id'] not in stale]
    if full:
        stale = {c['cluster_id']: ['--full'] for c in clusters}
        ok = []
    return {'stale': stale, 'uncovered': sorted(uncovered), 'ok': ok}

def main():
    full = '--full' in sys.argv
    manifest = json.load(io.open(MAN_PATH, encoding='utf-8'))
    r = classify(manifest, load_clusters(), full=full)
    lines = ['# 커버리지 리포트\n']
    lines.append('## STALE (재합성 필요)')
    lines += ['- %s: %s' % (k, ', '.join(v)) for k, v in r['stale'].items()] or ['- (없음)']
    lines.append('\n## UNCOVERED (새 클러스터 후보)')
    lines += ['- %s' % s for s in r['uncovered']] or ['- (없음)']
    lines.append('\n## OK')
    lines += ['- %s' % s for s in r['ok']] or ['- (없음)']
    if len(r['uncovered']) >= 5:
        lines.insert(1, '> ⚠️ uncovered %d건 — 새 클러스터/전체 재합성 권장\n' % len(r['uncovered']))
    io.open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
    print('STALE %d · UNCOVERED %d · OK %d -> %s' % (len(r['stale']), len(r['uncovered']), len(r['ok']), REPORT))
    sys.exit(1 if (r['stale'] or r['uncovered']) else 0)

if __name__ == '__main__':
    main()
