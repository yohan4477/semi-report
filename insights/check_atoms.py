# 원자·인사이트 검사기 — 설계: docs/superpowers/specs/2026-07-30-원자-뷰-인사이트-design.md
# C1~C11. FAIL이 하나라도 있으면 종료코드 1.
import os, io, re, json, glob, sys

ROOT = r"C:\Users\y\semianalysis"
ATOMS = os.path.join(ROOT, "insights", "atoms")
SYNTH = os.path.join(ROOT, "insights", "synth")
MAN = os.path.join(ROOT, "insights", "manifest.json")
ACTORS = os.path.join(ROOT, "insights", "views", "actors.json")

STACK = ['전자·공정', '칩', '메모리', '열', '랙', '데이터센터', '전력망', '연료·지정학']
# 스택 의존 그래프 — 인사이트는 여기서 서로 이어진 노드들만 묶을 수 있다(아무 데나 잇는 것을 막는다)
EDGES = [('전자·공정', '칩'), ('칩', '메모리'), ('칩', '열'), ('칩', '랙'), ('열', '랙'),
         ('메모리', '랙'), ('랙', '데이터센터'), ('데이터센터', '전력망'), ('전력망', '연료·지정학')]


def connected(nodes):
    """노드 집합이 EDGES 위에서 하나로 이어져 있는가."""
    nodes = set(nodes)
    if len(nodes) <= 1:
        return True
    adj = {n: set() for n in nodes}
    for a, b in EDGES:
        if a in nodes and b in nodes:
            adj[a].add(b)
            adj[b].add(a)
    seen, stack = set(), [next(iter(nodes))]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(adj[n] - seen)
    return seen == nodes
NUMTOK = re.compile(r'\d+(?:\.\d+)?')
# 같은 단위의 수치가 조건이 다른 채로 한 인사이트에 섞이면 오독이 난다 — 단위 겹침이 C9 트리거
UNIT = re.compile(r'W/m·K|kW|MW|LPM|°C|%|W|배|단|mm|kg|시간')
TIMEWORD = re.compile(r'뒤집|바뀌|이전에는|그전까지|당시에는')

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def norm(s):
    return (s or '').replace(',', '').replace(' ', '')


def load_atoms():
    out = []
    for p in sorted(glob.glob(os.path.join(ATOMS, '*.json'))):
        d = json.load(io.open(p, encoding='utf-8'))
        for a in d['atoms']:
            a['_file'] = os.path.basename(p)
            a['_source_id'] = d['source_id']
            a['_path'] = d['path']
            out.append(a)
    return out


def parse_synth(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.DOTALL)
    if not m:
        return None, text
    meta, body = {}, m.group(2)
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w+):\s*(.*)$', line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip()
        if v.startswith('['):
            v = [x.strip() for x in v.strip('[]').split(',') if x.strip()]
        meta[k] = v
    return meta, body


def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        h = re.match(r'^##\s+(.+?)\s*$', line)
        if h:
            cur = h.group(1)
            out[cur] = []
        elif cur and line.strip():
            out[cur].append(line.strip())
    return out


def check_atoms(atoms, man_ids, actor_names):
    lines_cache = {}
    for a in atoms:
        where = '%s %s' % (a['_file'], a['id'])
        if a['_source_id'] not in man_ids:
            add('FAIL', where, 'C1', 'manifest에 없는 source_id: %s' % a['_source_id'])
            continue
        p = os.path.join(ROOT, a['_path'])
        if p not in lines_cache:
            lines_cache[p] = io.open(p, encoding='utf-8').read().splitlines() if os.path.exists(p) else []
        lines = lines_cache[p]
        n = a.get('line')
        if not isinstance(n, int) or n < 1 or n > len(lines):
            add('FAIL', where, 'C2', 'line %s이 문서 범위(1~%d) 밖' % (n, len(lines)))
        elif a.get('value'):
            hay = norm(lines[n - 1])
            missing = [t for t in NUMTOK.findall(a['value']) if t not in hay]
            if missing:
                add('FAIL', where, 'C2', '%d행에 없는 수치 %s' % (n, ','.join(missing)))
        if not (a.get('condition') or '').strip():
            add('FAIL', where, 'C3', 'condition 비어 있음')
        if a.get('view', {}).get('stack') not in STACK:
            add('FAIL', where, 'C4', '스택 노드 아님: %s' % a.get('view', {}).get('stack'))
        for name in a.get('view', {}).get('actor', []):
            if name not in actor_names:
                add('WARN', where, 'C5', 'actors.json에 없는 주체: %s' % name)


def check_synth(atoms):
    by_id = {a['id']: a for a in atoms}
    for p in sorted(glob.glob(os.path.join(SYNTH, '*.md'))):
        where = os.path.basename(p)
        meta, body = parse_synth(io.open(p, encoding='utf-8').read())
        if not meta:
            add('FAIL', where, 'C6', 'frontmatter 없음')
            continue
        nodes = meta.get('nodes') or ([meta['node']] if meta.get('node') else [])
        cited = meta.get('atoms') or []
        sec = sections(body)

        bad = [n for n in nodes if n not in STACK]
        if bad:
            add('FAIL', where, 'C4', '스택 노드 아님: %s' % ', '.join(bad))
        elif not connected(nodes):
            add('FAIL', where, 'C6', '서로 이어지지 않은 노드를 묶음: %s' % ', '.join(nodes))

        cited_atoms = []
        for aid in cited:
            a = by_id.get(aid)
            if not a:
                add('FAIL', where, 'C6', '존재하지 않는 원자: %s' % aid)
                continue
            if a['view']['stack'] not in nodes:
                add('FAIL', where, 'C6', '%s는 노드 %s 소속인데 %s에서 인용' % (aid, a['view']['stack'], '·'.join(nodes)))
            cited_atoms.append(a)

        if len(cited_atoms) < 3:
            add('FAIL', where, 'C7', '원자 %d개 (3개 이상 필요)' % len(cited_atoms))
        if len({a['_source_id'] for a in cited_atoms}) < 2:
            add('FAIL', where, 'C7', '출처 문서 %d편 (2편 이상 필요)' % len({a['_source_id'] for a in cited_atoms}))

        for name in ('그래서 무엇이 달라지나', '아직 모르는 것'):
            if not sec.get(name):
                add('FAIL', where, 'C8', '"%s" 절이 없거나 비어 있음' % name)

        # C9 — 같은 단위의 수치를 조건이 다른 원자에서 끌어다 썼으면 비교 가능성을 밝혀야 한다
        shared = set()
        for i, a in enumerate(cited_atoms):
            for b in cited_atoms[i + 1:]:
                if a.get('condition') == b.get('condition'):
                    continue
                common = set(UNIT.findall(a.get('value') or '')) & set(UNIT.findall(b.get('value') or ''))
                shared |= common
        clash = [x for x in (sec.get('조건 충돌') or []) if x.strip('- ').strip() not in ('없음', '')]
        if shared and not clash:
            add('FAIL', where, 'C9',
                '조건이 다른 원자들이 같은 단위(%s)의 수치를 함께 쓰는데 "조건 충돌"이 비어 있음'
                % ', '.join(sorted(shared)))

        if TIMEWORD.search(body) and len({a['view']['time'] for a in cited_atoms}) < 2:
            add('WARN', where, 'C10', '판단 변화 표현이 있으나 인용 원자의 시점이 1종뿐')

        as_of = meta.get('as_of') or ''
        newer = [a['id'] for a in atoms
                 if a['view']['stack'] in nodes and a['id'] not in cited and a['view']['time'] > as_of]
        if newer:
            add('WARN', where, 'C11', 'as_of(%s) 이후 원자 %d개 미반영: %s'
                % (as_of, len(newer), ', '.join(newer[:6])))


def main():
    man_ids = {s['id'] for s in json.load(io.open(MAN, encoding='utf-8'))['sources']}
    actor_names = set(json.load(io.open(ACTORS, encoding='utf-8')))
    atoms = load_atoms()
    check_atoms(atoms, man_ids, actor_names)
    check_synth(atoms)

    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    warns = len(findings) - fails
    nodes = {}
    for a in atoms:
        nodes[a['view']['stack']] = nodes.get(a['view']['stack'], 0) + 1
    print('요약: 원자 %d개 / 문서 %d편 / FAIL %d / WARN %d'
          % (len(atoms), len({a['_source_id'] for a in atoms}), fails, warns))
    print('노드별: ' + ', '.join('%s %d' % kv for kv in sorted(nodes.items(), key=lambda x: -x[1])))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
