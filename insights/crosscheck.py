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
