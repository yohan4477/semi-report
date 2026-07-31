# 원자·인사이트 검사기 — 설계: docs/superpowers/specs/2026-07-30-원자-뷰-인사이트-design.md
# C1~C21. FAIL이 하나라도 있으면 종료코드 1.
import os, io, re, json, glob, sys
import datetime
TODAY = datetime.date.today().isoformat()

ROOT = r"C:\Users\y\semianalysis"
ATOMS = os.path.join(ROOT, "insights", "atoms")
SYNTH = os.path.join(ROOT, "insights", "synth")
MAN = os.path.join(ROOT, "insights", "manifest.json")
ACTORS = os.path.join(ROOT, "insights", "views", "actors.json")
ACTOR_MAP = os.path.join(ROOT, "insights", "views", "actor_map.json")
VERIFY = os.path.join(ROOT, "insights", "verify.json")
PROCESS = os.path.join(ROOT, "insights", "views", "process.json")

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


def corpus_of(source_id):
    """source_id 접두어가 코퍼스다 — semi(SemiAnalysis) / und(언더스탠딩·제3자)."""
    return (source_id or '').split(':')[0]


def load_atoms():
    out = []
    for p in sorted(glob.glob(os.path.join(ATOMS, '*.json'))):
        d = json.load(io.open(p, encoding='utf-8'))
        for a in d['atoms']:
            a['_file'] = os.path.basename(p)
            a['_source_id'] = d['source_id']
            a['_path'] = d['path']
            a['_source_hash'] = d.get('source_hash')
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


def check_atoms(atoms, man_hashes, actor_names):
    lines_cache = {}
    seen_files = set()
    # C19 — id 중복. 순번이 문서 내 일련이라 같은 날 발행된 다른 문서가 같은 id를
    # 만들 수 있다. by_id = {a['id']: a for a in atoms}가 파일명 정렬 순서로 뒤 파일을
    # 조용히 채택하므로, 기존 인사이트가 인용하는 id가 다른 문서의 원자를 가리키게 되고도
    # FAIL 하나 없이 통과한다 — 여기서 잡는다
    id_files = {}
    for a in atoms:
        id_files.setdefault(a['id'], []).append(a['_file'])
    for aid, files in sorted(id_files.items()):
        if len(files) > 1:
            add('FAIL', aid, 'C19', 'id 중복 — 파일 %s' % ', '.join(sorted(set(files))))
    for a in atoms:
        where = '%s %s' % (a['_file'], a['id'])
        if a['_source_id'] not in man_hashes:
            add('FAIL', where, 'C1', 'manifest에 없는 source_id: %s' % a['_source_id'])
            continue
        # C16 — 원문이 바뀌면 줄 번호가 밀린다. 그 줄에 우연히 같은 숫자가 있으면 C2가 통과하므로
        # 본문 hash를 직접 대조해 원문 변경 자체를 잡는다. 파일당 한 번만 본다
        if a['_file'] not in seen_files:
            seen_files.add(a['_file'])
            fh, mh = a.get('_source_hash'), man_hashes[a['_source_id']]
            if not fh:
                add('FAIL', a['_file'], 'C16', 'source_hash 필드 없음 (manifest: %s)' % mh)
            elif fh != mh:
                add('FAIL', a['_file'], 'C16',
                    '원문이 바뀌었다 — 원자 추출 시 %s, 현재 %s. 이 문서의 원자를 재추출할 것' % (fh, mh))
        p = os.path.join(ROOT, a['_path'])
        if p not in lines_cache:
            lines_cache[p] = io.open(p, encoding='utf-8').read().splitlines() if os.path.exists(p) else []
        lines = lines_cache[p]
        n = a.get('line')
        if not isinstance(n, int) or n < 1 or n > len(lines):
            add('FAIL', where, 'C2', 'line %s이 문서 범위(1~%d) 밖' % (n, len(lines)))
        else:
            if a.get('value'):
                hay = norm(lines[n - 1])
                missing = [t for t in NUMTOK.findall(a['value']) if t not in hay]
                if missing:
                    add('FAIL', where, 'C2', '%d행에 없는 수치 %s' % (n, ','.join(missing)))
            # C17 — 그 줄의 원문을 원자 옆에 그대로 둔다. C2는 숫자의 소재지만 보므로
            # claim이 원문과 어긋나도 통과한다. 원문을 붙여 두면 대조가 눈으로 끝난다
            lt = a.get('line_text')
            if lt is None:
                add('FAIL', where, 'C17', 'line_text 없음')
            elif norm(lt) != norm(lines[n - 1]):
                add('FAIL', where, 'C17', 'line_text가 %d행 원문과 다름 (원문 변경 또는 줄 밀림)' % n)
        if not (a.get('condition') or '').strip():
            add('FAIL', where, 'C3', 'condition 비어 있음')
        if a.get('view', {}).get('stack') not in STACK:
            add('FAIL', where, 'C4', '스택 노드 아님: %s' % a.get('view', {}).get('stack'))
        for name in a.get('view', {}).get('actor', []):
            if name not in actor_names:
                add('WARN', where, 'C5', 'actors.json에 없는 주체: %s' % name)


def check_process(atoms, by_id):
    """C13 — 단계 사전 자체의 무결성. 배정은 process.json에만 있고 원자 파일에는 없다."""
    if not os.path.exists(PROCESS):
        return None
    pr = json.load(io.open(PROCESS, encoding='utf-8'))
    stages, assign = pr.get('stages') or [], pr.get('assign') or {}
    where = 'views/process.json'
    if len(set(stages)) != len(stages):
        add('FAIL', where, 'C13', '중복된 단계 이름')
    for aid, st in sorted(assign.items()):
        if aid not in by_id:
            add('FAIL', where, 'C13', '존재하지 않는 원자에 단계 배정: %s' % aid)
        if st not in stages:
            add('FAIL', where, 'C13', '%s의 단계가 사전에 없음: %s' % (aid, st))
    return pr


def check_synth(atoms, pr):
    by_id = {a['id']: a for a in atoms}
    stages = (pr or {}).get('stages') or []
    assign = (pr or {}).get('assign') or {}
    for p in sorted(glob.glob(os.path.join(SYNTH, '*.md'))):
        where = os.path.basename(p)
        meta, body = parse_synth(io.open(p, encoding='utf-8').read())
        if not meta:
            add('FAIL', where, 'C6', 'frontmatter 없음')
            continue
        view = meta.get('view') or 'stack'
        nodes = meta.get('nodes') or ([meta['node']] if meta.get('node') else [])
        used_stages = meta.get('stages') or []
        cited = meta.get('atoms') or []
        sec = sections(body)

        if view == 'process':
            # C14 — 단계를 가로질러야 프로세스 뷰다. 한 단계에 머물면 스택 뷰와 다를 게 없다
            bad = [s for s in used_stages if s not in stages]
            if bad:
                add('FAIL', where, 'C14', '사전에 없는 단계: %s' % ', '.join(bad))
            else:
                order = [stages.index(s) for s in used_stages]
                if order != sorted(order):
                    add('FAIL', where, 'C14', 'stages가 사전 순서를 역행함: %s' % ' → '.join(used_stages))
        else:
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
            if view == 'process':
                st = assign.get(aid)
                if not st:
                    add('FAIL', where, 'C14', '%s에 단계 배정이 없음 (process.json)' % aid)
                elif st not in used_stages:
                    add('FAIL', where, 'C14', '%s는 단계 "%s" 소속인데 %s에서 인용' % (aid, st, '·'.join(used_stages)))
            elif a['view']['stack'] not in nodes:
                add('FAIL', where, 'C6', '%s는 노드 %s 소속인데 %s에서 인용' % (aid, a['view']['stack'], '·'.join(nodes)))
            cited_atoms.append(a)

        if view == 'process':
            spread = {assign.get(a['id']) for a in cited_atoms} - {None}
            if len(spread) < 2:
                add('FAIL', where, 'C14', '인용 원자가 단계 %d개에만 걸림 (2개 이상 필요)' % len(spread))
            # C15 — 프로세스 뷰의 산출물은 "어디를 지나면 앞 결정을 못 고치나"다
            if not sec.get('되돌릴 수 없는 지점'):
                add('FAIL', where, 'C15', '"되돌릴 수 없는 지점" 절이 없거나 비어 있음')

        if len(cited_atoms) < 3:
            add('FAIL', where, 'C7', '원자 %d개 (3개 이상 필요)' % len(cited_atoms))
        if len({a['_source_id'] for a in cited_atoms}) < 2:
            add('FAIL', where, 'C7', '출처 문서 %d편 (2편 이상 필요)' % len({a['_source_id'] for a in cited_atoms}))

        # C18 — 제3자(und) 근거가 SemiAnalysis(semi) 판단에 섞이면 근거 무게가 뒤섞이고
        # 어느 주장이 1차 리포트에서 나왔는지 추적이 끊긴다. 인사이트 단위로 코퍼스를 가른다
        corpora = {corpus_of(a['_source_id']) for a in cited_atoms}
        if len(corpora) > 1:
            add('FAIL', where, 'C18', '한 인사이트에 코퍼스가 섞였다: %s' % ', '.join(sorted(corpora)))

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

        # C12 — 검토했으나 이 주장과 무관하다고 판정한 원자. 근거를 본문에 남겨야 도피구가 안 된다
        dismissed = meta.get('dismissed') or []
        if dismissed:
            reasons = ' '.join(sec.get('검토 후 무관') or [])
            for aid in dismissed:
                a = by_id.get(aid)
                if not a:
                    add('FAIL', where, 'C12', '존재하지 않는 원자를 무관 처리: %s' % aid)
                    continue
                scoped = (assign.get(aid) in used_stages) if view == 'process' else (a['view']['stack'] in nodes)
                if not scoped:
                    add('FAIL', where, 'C12', '%s는 이 인사이트 범위 소속이 아니라 무관 처리 대상이 아님' % aid)
                if aid not in reasons:
                    add('FAIL', where, 'C12', '%s를 무관 처리했으나 "검토 후 무관" 절에 사유가 없음' % aid)

        as_of = meta.get('as_of') or ''
        skip = set(cited) | set(dismissed)

        def in_scope(a):
            return assign.get(a['id']) in used_stages if view == 'process' else a['view']['stack'] in nodes

        newer = [a['id'] for a in atoms
                 if in_scope(a) and a['id'] not in skip and a['view']['time'] > as_of]
        if newer:
            add('WARN', where, 'C11', 'as_of(%s) 이후 원자 %d개 미반영: %s'
                % (as_of, len(newer), ', '.join(newer[:6])))


def check_actor_map(actor_names):
    """C20 — 주체 사전에 있는 회사는 actor_map.json에도 있어야 한다.
    빠지면 「제약 → 회사」 지도에서 그 회사만 조용히 사라진다."""
    if not os.path.exists(ACTOR_MAP):
        return
    m = json.load(io.open(ACTOR_MAP, encoding='utf-8')).get('companies') or {}
    for name in sorted(actor_names - set(m)):
        findings.append(('WARN', 'actor_map.json', 'C20', '회사 해석이 없는 주체: %s' % name))
    for name in sorted(set(m) - actor_names):
        findings.append(('WARN', 'actor_map.json', 'C20', 'actors.json에 없는 회사: %s' % name))
    for name, v in sorted(m.items()):
        if v.get('side') not in ('파는 쪽', '맞는 쪽', '양쪽'):
            findings.append(('FAIL', 'actor_map.json', 'C20', '%s: side 값이 사전에 없다(%s)' % (name, v.get('side'))))
        if v.get('listed') and not v.get('ticker'):
            findings.append(('FAIL', 'actor_map.json', 'C20', '%s: 상장인데 티커가 없다' % name))


def check_verify(atoms):
    """C21 — 검증 대장. 이 체계에서 판정은 원자로만 하고, 질문은 근거보다 먼저 있어야 한다.
    결과를 보고 나서 만든 질문은 검증이 아니므로 근거 원자의 문서 날짜가
    질문을 연 날짜보다 나중인지 본다(사후 편입 금지)."""
    if not os.path.exists(VERIFY):
        return None
    v = json.load(io.open(VERIFY, encoding='utf-8'))
    ok_status = set(v.get('status_def') or {})
    by_id = {a['id']: a for a in atoms}
    synth = {os.path.basename(p) for p in glob.glob(os.path.join(SYNTH, '*.md'))}
    seen = set()
    for c in v.get('checks') or []:
        where = 'verify.json %s' % c.get('id')
        if c.get('id') in seen:
            findings.append(('FAIL', where, 'C21', '검증 id 중복: %s' % c.get('id')))
        seen.add(c.get('id'))
        if c.get('insight') not in synth:
            findings.append(('FAIL', where, 'C21', '없는 인사이트 파일: %s' % c.get('insight')))
        if c.get('status') not in ok_status:
            findings.append(('FAIL', where, 'C21', 'status 값이 사전에 없다: %s' % c.get('status')))
        for k in ('question', 'settles', 'watch', 'opened_on', 'due'):
            if not c.get(k):
                findings.append(('FAIL', where, 'C21', '%s가 비었다' % k))
        if c.get('status') in ('적중', '빗나감'):
            if not c.get('resolved_on'):
                findings.append(('FAIL', where, 'C21', '판정했는데 resolved_on이 없다'))
            if not c.get('evidence'):
                findings.append(('FAIL', where, 'C21', '판정했는데 근거 원자가 없다 — 원자 없이 판정하지 않는다'))
        for aid in c.get('evidence') or []:
            a = by_id.get(aid)
            if not a:
                findings.append(('FAIL', where, 'C21', '없는 원자를 근거로 든다: %s' % aid))
                continue
            if str(a['view']['time']) < str(c.get('opened_on') or ''):
                findings.append(('FAIL', where, 'C21',
                                 '%s는 질문(%s)보다 이전 문서(%s)다 — 사후 편입'
                                 % (aid, c.get('opened_on'), a['view']['time'])))
        if c.get('status') == '열림' and str(c.get('due') or '') < TODAY:
            findings.append(('WARN', where, 'C21', '기한(%s)이 지났는데 열려 있다 — 판정하라' % c.get('due')))
    return v


def main():
    # cp949 콘솔에서 C16 등의 em dash·한글 메시지가 UnicodeEncodeError로 죽으면 그 뒤에 남은
    # FAIL 목록과 요약이 통째로 사라진다 — crosscheck.py와 같은 방식으로 막는다
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    man_hashes = {s['id']: s['hash'] for s in json.load(io.open(MAN, encoding='utf-8'))['sources']}
    actor_names = set(json.load(io.open(ACTORS, encoding='utf-8')))
    atoms = load_atoms()
    check_atoms(atoms, man_hashes, actor_names)
    check_actor_map(actor_names)
    vr = check_verify(atoms)
    pr = check_process(atoms, {a['id']: a for a in atoms})
    check_synth(atoms, pr)

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
    if vr:
        st = {}
        for c in vr.get('checks') or []:
            st[c.get('status')] = st.get(c.get('status'), 0) + 1
        done = st.get('적중', 0) + st.get('빗나감', 0)
        print('검증: %d건 (%s) / 판정 %d건%s'
              % (sum(st.values()), ', '.join('%s %d' % kv for kv in sorted(st.items())), done,
                 (' · 적중률 %.0f%%' % (100.0 * st.get('적중', 0) / done)) if done else ' — 적중률 계산 불가'))
    if pr:
        assign = pr.get('assign') or {}
        cnt = {s: 0 for s in pr['stages']}
        for aid in assign:
            if assign[aid] in cnt:
                cnt[assign[aid]] += 1
        print('단계별: ' + ' → '.join('%s %d' % (s, cnt[s]) for s in pr['stages'])
              + ' / 미배정 %d' % len([a for a in atoms if a['id'] not in assign]))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
