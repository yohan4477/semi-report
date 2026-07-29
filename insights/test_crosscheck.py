import check_atoms as ca
import io as _io


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
