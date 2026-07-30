# 새 원자 대 기존 원자·인사이트 대조 — 설계: docs/superpowers/specs/2026-07-30-원자화-스킬-design.md
# 파일을 수정하지 않는다. 계산하고 출력만 한다.
import os, io, re, json, glob, sys
import check_atoms as ca

ROOT = ca.ROOT
SYNTH = ca.SYNTH


def units(value):
    """값 문자열에서 단위 토큰 집합. 판정은 check_atoms.UNIT을 그대로 쓴다 —
    복사하면 C9와 이 리포트가 어긋난다."""
    return set(ca.UNIT.findall(value or ''))


def find_clashes(new_atoms, old_atoms):
    """같은 스택 노드 · 단위 겹침 · condition 다름인 쌍. C9는 인사이트가 그 둘을
    함께 인용할 때만 FAIL을 내므로, 인사이트를 쓰기 전에 목록을 준다."""
    out = []
    for n in new_atoms:
        for o in old_atoms:
            if n['view']['stack'] != o['view']['stack']:
                continue
            if (n.get('condition') or '') == (o.get('condition') or ''):
                continue
            for u in sorted(units(n.get('value')) & units(o.get('value'))):
                out.append({'unit': u, 'new': n, 'old': o})
    return out


def load_assign():
    """프로세스 단계 배정을 한 번만 읽는다. ca.check_process는 사전 무결성 검사용이라
    findings에 부산물을 남기므로 리포트 경로에서는 부르지 않는다."""
    p = os.path.join(ROOT, 'insights', 'views', 'process.json')
    if not os.path.exists(p):
        return {}
    return json.load(io.open(p, encoding='utf-8')).get('assign') or {}


def find_stale(new_atoms, all_atoms, assign, synth_dir=None):
    """새 원자가 건드린 칸을 쓰는 인사이트 중 as_of가 그 원자보다 이른 것.
    C11은 모든 인사이트를 훑는 상시 위생 검사이고, 이쪽은 방금 들어온 원자로
    범위를 좁혀 무엇을 처리해야 하는지까지 붙여 준다."""
    synth_dir = synth_dir or SYNTH
    assign = assign or {}
    out = []
    for p in sorted(glob.glob(os.path.join(synth_dir, '*.md'))):
        meta, _ = ca.parse_synth(io.open(p, encoding='utf-8').read())
        if not meta:
            continue
        view = meta.get('view') or 'stack'
        cited = set(meta.get('atoms') or []) | set(meta.get('dismissed') or [])
        as_of = meta.get('as_of') or ''
        nodes = meta.get('nodes') or ([meta['node']] if meta.get('node') else [])
        stages = meta.get('stages') or []
        if view == 'process':
            in_scope = lambda a: assign.get(a['id']) in stages
            scope = '단계 ' + '·'.join(stages)
        else:
            in_scope = lambda a: a['view']['stack'] in nodes
            scope = '노드 ' + '·'.join(nodes)
        hit = [a['id'] for a in new_atoms
               if in_scope(a) and a['id'] not in cited and a['view']['time'] > as_of]
        if hit:
            out.append({'file': os.path.basename(p), 'as_of': as_of,
                        'scope': scope, 'uncited': sorted(hit)})
    return out


def find_lumps(all_atoms, assign, threshold=10, dominance=0.6):
    """한 칸에 원자가 몰린 곳. 좌표를 쪼갤지 판단하는 근거다.

    문서 수만 세면 거의 모든 칸이 2편을 넘어 아무것도 걸러지지 않는다. 실제 신호는
    **한 문서가 그 칸을 독점하는가**다. 최다 문서 비중이 60%를 넘으면 그 구조는 아직
    한 문서의 목차이므로 쪼개지 않는다 — 좌표는 문서를 가로질러 비교하는 자리다.
    비중이 흩어져 있으면 하위 단계 후보로 올린다. 다만 여러 문서가 같은 순서를
    말하는지는 기계가 못 본다 — 후보까지만 낸다."""
    groups = {}
    for a in all_atoms:
        for axis, key in (('노드', a['view']['stack']), ('단계', assign.get(a['id']))):
            if not key:
                continue
            g = groups.setdefault((axis, key), {'n': 0, 'docs': {}})
            g['n'] += 1
            g['docs'][a['_file']] = g['docs'].get(a['_file'], 0) + 1
    out = []
    for (axis, key), g in groups.items():
        if g['n'] < threshold:
            continue
        top_doc, top_n = max(g['docs'].items(), key=lambda kv: kv[1])
        share = top_n / float(g['n'])
        out.append({'axis': axis, 'key': key, 'n': g['n'], 'docs': len(g['docs']),
                    'top_doc': top_doc, 'top_n': top_n, 'share': share,
                    'promotable': share < dominance})
    out.sort(key=lambda x: -x['n'])
    return out


def pick_target(argv):
    """인수가 있으면 그 파일. 없으면 미커밋 원자 파일 → mtime 최신 순."""
    if argv:
        return os.path.basename(argv[0])
    try:
        import subprocess
        r = subprocess.run(['git', '-c', 'core.quotepath=false', '-C', ROOT, 'status', '--porcelain',
                            'insights/atoms'], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            name = line[3:].strip().strip('"')
            if name.endswith('.json'):
                return os.path.basename(name)
    except Exception:
        pass
    files = glob.glob(os.path.join(ca.ATOMS, '*.json'))
    if not files:
        return None
    return os.path.basename(max(files, key=os.path.getmtime))


def main():
    # cp949 콘솔에서 한글·em dash 출력이 UnicodeEncodeError로 죽지 않게. 스킬은 이 스크립트를
    # `py insights/crosscheck.py [대상]`으로만 부르므로 환경변수에 의존할 수 없다
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    atoms = ca.load_atoms()
    target = pick_target(sys.argv[1:])
    if not target:
        print('대상 원자 파일을 찾지 못했다')
        return 1
    new = [a for a in atoms if a['_file'] == target]
    if not new:
        print('원자가 없다: %s' % target)
        return 1
    old = [a for a in atoms if a['_file'] != target]

    assign = load_assign()
    stale = find_stale(new, atoms, assign)
    clashes = find_clashes(new, old)
    # 문서 내부 충돌 — 이 체계를 만든 5.4배 사고 자체가 [260723] 한 문서 안에서 났다
    # (요약 46행 vs 본문 256·258행). find_clashes(new, new)는 같은 쌍을 양방향으로 두 번
    # 내고 자기 자신과의 쌍도 섞으므로 여기서 걸러낸다
    raw_internal = [c for c in find_clashes(new, new) if c['new']['id'] != c['old']['id']]
    seen_pairs = set()
    internal = []
    for c in raw_internal:
        key = (c['unit'],) + tuple(sorted((c['new']['id'], c['old']['id'])))
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        internal.append(c)

    lumps = find_lumps(atoms, assign)

    print('대상: %s (원자 %d개)' % (target, len(new)))
    print('')
    print('뭉침 %d칸  (원자 10개 이상 — 좌표를 쪼갤지 판단하는 자리)' % len(lumps))
    for l in lumps:
        mark = ('하위 단계 후보' if l['promotable']
                else '쪼개지 말 것 — %s 한 편이 %d%%' % (l['top_doc'][:22], round(l['share'] * 100)))
        print('  %s %-16s 원자 %3d · 문서 %d편 · 최다 %d%%  → %s'
              % (l['axis'], l['key'], l['n'], l['docs'], round(l['share'] * 100), mark))
    if lumps:
        print('  한 문서가 60%를 넘으면 그 구조는 그 문서의 목차다. 스킬은 사전을 늘리지 않는다')
    print('')
    print('STALE %d건' % len(stale))
    for s in stale:
        print('  %s  as_of %s  [%s]' % (s['file'], s['as_of'], s['scope']))
        print('    미인용 신규 원자: %s' % ', '.join(s['uncited']))
    if stale:
        print('  처리 4갈래: 뒷받침(atoms에 id 추가) / 조건 다름(조건 충돌 절) /')
        print('             뒤집음(주장 재작성, 이전 판단 보존) / 무관(dismissed + 검토 후 무관 절)')
    print('')
    print('문서 내부 충돌 %d쌍  (같은 단위 · 다른 조건 — 5.4배 사고와 같은 유형)' % len(internal))
    for c in internal:
        print('  %-4s %s "%s" [%s]' % (c['unit'], c['new']['id'],
                                       (c['new'].get('value') or '')[:40],
                                       (c['new'].get('condition') or '')[:40]))
        print('       %s "%s" [%s]' % (c['old']['id'],
                                       (c['old'].get('value') or '')[:40],
                                       (c['old'].get('condition') or '')[:40]))
    print('')
    print('충돌 후보 %d쌍  (같은 단위 · 다른 조건 — 함께 인용하면 C9가 FAIL)' % len(clashes))
    for c in clashes:
        print('  %-4s %s "%s" [%s]' % (c['unit'], c['new']['id'],
                                       (c['new'].get('value') or '')[:40],
                                       (c['new'].get('condition') or '')[:40]))
        print('       %s "%s" [%s]' % (c['old']['id'],
                                       (c['old'].get('value') or '')[:40],
                                       (c['old'].get('condition') or '')[:40]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
