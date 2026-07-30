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


def pick_target(argv):
    """인수가 있으면 그 파일. 없으면 미커밋 원자 파일 → mtime 최신 순."""
    if argv:
        return os.path.basename(argv[0])
    try:
        import subprocess
        r = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain',
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

    stale = find_stale(new, atoms, load_assign())
    clashes = find_clashes(new, old)

    print('대상: %s (원자 %d개)' % (target, len(new)))
    print('')
    print('STALE %d건' % len(stale))
    for s in stale:
        print('  %s  as_of %s  [%s]' % (s['file'], s['as_of'], s['scope']))
        print('    미인용 신규 원자: %s' % ', '.join(s['uncited']))
    if stale:
        print('  처리 4갈래: 뒷받침(atoms에 id 추가) / 조건 다름(조건 충돌 절) /')
        print('             뒤집음(주장 재작성, 이전 판단 보존) / 무관(dismissed + 검토 후 무관 절)')
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
