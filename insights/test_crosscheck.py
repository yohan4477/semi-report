import check_atoms as ca
import io as _io
import crosscheck as cc


def _atom(aid, stack, value, cond, time='2026-01-01', sid='semi:compute:x'):
    return {'id': aid, '_source_id': sid, '_file': 'f.json',
            'value': value, 'condition': cond,
            'view': {'stack': stack, 'actor': [], 'time': time}}


def test_corpus_of_semi():
    assert ca.corpus_of('semi:compute:베라-루빈') == 'semi'


def test_corpus_of_und():
    assert ca.corpus_of('und:권효재:이란-전쟁') == 'und'


def test_corpus_of_no_colon():
    # 접두어가 없으면 통째로 코퍼스로 본다 — 조용히 semi로 넘어가면 C18이 무력해진다
    assert ca.corpus_of('semi') == 'semi'


def _atom_min(aid, sid, stack='랙', time='2026-01-01'):
    return {'id': aid, '_source_id': sid, '_file': sid.split(':')[-1] + '.json',
            '_path': 'x.md', '_source_hash': 'h',
            'value': None, 'condition': 'c', 'line': 1, 'line_text': 't',
            'view': {'stack': stack, 'actor': [], 'time': time}}


def test_c18_mixed_corpora_fails(tmp_path, monkeypatch):
    p = tmp_path / 'mixed.md'
    _io.open(str(p), 'w', encoding='utf-8').write(
        '---\nview: stack\nnodes: [랙]\natoms: [A-1, A-2, A-3]\nas_of: 2026-01-03\n---\n\n'
        '## 주장\n**x**\n## 근거\n- x\n## 조건 충돌\n- 없음\n'
        '## 그래서 무엇이 달라지나\n- x\n## 아직 모르는 것\n- x\n')
    monkeypatch.setattr(ca, 'SYNTH', str(tmp_path))
    ca.findings.clear()
    atoms = [_atom_min('A-1', 'semi:compute:x'),
             _atom_min('A-2', 'und:권효재:y'),
             _atom_min('A-3', 'semi:compute:z')]
    ca.check_synth(atoms, None)
    assert 'C18' in [f[2] for f in ca.findings]


def test_c18_single_corpus_passes(tmp_path, monkeypatch):
    p = tmp_path / 'single.md'
    _io.open(str(p), 'w', encoding='utf-8').write(
        '---\nview: stack\nnodes: [랙]\natoms: [A-1, A-2, A-3]\nas_of: 2026-01-03\n---\n\n'
        '## 주장\n**x**\n## 근거\n- x\n## 조건 충돌\n- 없음\n'
        '## 그래서 무엇이 달라지나\n- x\n## 아직 모르는 것\n- x\n')
    monkeypatch.setattr(ca, 'SYNTH', str(tmp_path))
    ca.findings.clear()
    atoms = [_atom_min('A-1', 'semi:compute:x'),
             _atom_min('A-2', 'semi:memory:y'),
             _atom_min('A-3', 'semi:compute:z')]
    ca.check_synth(atoms, None)
    assert 'C18' not in [f[2] for f in ca.findings]


def test_units_extracts_kw_and_mw():
    assert cc.units('공랭 랙 한계 41kW, GB200 120kW') == {'kW'}
    assert cc.units('CDU 2MW급 → 3~6MW급') == {'MW'}


def test_units_none_when_value_missing():
    assert cc.units(None) == set()


def test_clash_same_unit_different_condition():
    new = [_atom('A-260725-01', '랙', '랙당 132kW', 'Max-P 구성')]
    old = [_atom('A-250214-07', '랙', '공랭 랙 한계 41kW', '2025-02 H100 설계')]
    out = cc.find_clashes(new, old)
    assert len(out) == 1
    assert out[0]['unit'] == 'kW'
    assert out[0]['new']['id'] == 'A-260725-01'
    assert out[0]['old']['id'] == 'A-250214-07'


def test_no_clash_when_condition_same():
    new = [_atom('A-260725-01', '랙', '랙당 132kW', '같은 조건')]
    old = [_atom('A-250214-07', '랙', '공랭 41kW', '같은 조건')]
    assert cc.find_clashes(new, old) == []


def test_no_clash_across_different_nodes():
    # 노드가 다르면 쌍을 보지 않는다 — kW·%가 흔해서 안 좁히면 수십 쌍이 쏟아진다
    new = [_atom('A-260725-01', '열', '유량 4LPM에서 4kW', 'TSMC 시험차량')]
    old = [_atom('A-250214-07', '랙', '공랭 41kW', '2025-02 H100 설계')]
    assert cc.find_clashes(new, old) == []


def _write_synth(tmp_path, name, view, coord_line, atoms_line, as_of):
    p = tmp_path / name
    body = ('---\n'
            'view: %s\n'
            '%s\n'
            'atoms: %s\n'
            'as_of: %s\n'
            '---\n\n## 주장\n**x**\n' % (view, coord_line, atoms_line, as_of))
    _io.open(str(p), 'w', encoding='utf-8').write(body)
    return str(tmp_path)


def test_stale_when_new_atom_in_same_node_and_newer(tmp_path):
    d = _write_synth(tmp_path, 's1.md', 'stack', 'nodes: [랙]',
                     '[A-250214-07]', '2025-02-14')
    new = [_atom('A-260725-01', '랙', '132kW', 'Max-P', time='2026-07-25')]
    allx = new + [_atom('A-250214-07', '랙', '41kW', '2025-02', time='2025-02-14')]
    out = cc.find_stale(new, allx, {}, d)
    assert len(out) == 1
    assert out[0]['file'] == 's1.md'
    assert out[0]['uncited'] == ['A-260725-01']
    assert out[0]['scope'] == '노드 랙'


def test_stale_for_process_view_uses_injected_assign(tmp_path):
    d = _write_synth(tmp_path, 's4.md', 'process', 'stages: [냉각 방식 확정]',
                     '[A-250214-07]', '2025-02-14')
    new = [_atom('A-260725-01', '랙', '132kW', 'Max-P', time='2026-07-25')]
    allx = new + [_atom('A-250214-07', '랙', '41kW', '2025-02', time='2025-02-14')]
    assign = {'A-260725-01': '냉각 방식 확정'}
    out = cc.find_stale(new, allx, assign, d)
    assert len(out) == 1
    assert out[0]['scope'] == '단계 냉각 방식 확정'
    assert out[0]['uncited'] == ['A-260725-01']


def test_not_stale_when_already_cited(tmp_path):
    d = _write_synth(tmp_path, 's2.md', 'stack', 'nodes: [랙]',
                     '[A-250214-07, A-260725-01]', '2025-02-14')
    new = [_atom('A-260725-01', '랙', '132kW', 'Max-P', time='2026-07-25')]
    allx = new + [_atom('A-250214-07', '랙', '41kW', '2025-02', time='2025-02-14')]
    assert cc.find_stale(new, allx, {}, d) == []


def test_not_stale_when_new_atom_older_than_as_of(tmp_path):
    d = _write_synth(tmp_path, 's3.md', 'stack', 'nodes: [랙]',
                     '[A-250214-07]', '2026-12-31')
    new = [_atom('A-260725-01', '랙', '132kW', 'Max-P', time='2026-07-25')]
    allx = new + [_atom('A-250214-07', '랙', '41kW', '2025-02', time='2025-02-14')]
    assert cc.find_stale(new, allx, {}, d) == []


def test_pick_target_from_path():
    assert cc.pick_target(['insights/atoms/251128-TPUv7.json']) == '251128-TPUv7.json'


def test_pick_target_from_basename():
    assert cc.pick_target(['251128-TPUv7.json']) == '251128-TPUv7.json'


def test_pick_target_none_returns_none_when_no_files(tmp_path, monkeypatch):
    monkeypatch.setattr(cc.ca, 'ATOMS', str(tmp_path))
    assert cc.pick_target([]) is None
