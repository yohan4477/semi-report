import structures as st


def _doc(sid='semi:a:b', **kw):
    d = {'source_id': sid, 'path': 'x.md', 'structures': []}
    d.update(kw)
    return d


def test_kind_of_doc_invalid_value():
    errs = st.validate({'docs': [_doc(kind_of_doc='essay')]})
    assert any('kind_of_doc' in e for e in errs)


def test_argument_requires_thesis():
    errs = st.validate({'docs': [_doc(kind_of_doc='argument')]})
    assert any('thesis' in e for e in errs)


def test_thesis_requires_line():
    errs = st.validate({'docs': [_doc(kind_of_doc='argument',
                                      thesis={'claim': '병목이 옮겨갔다', 'line_text': 'y'})]})
    assert any('line' in e for e in errs)


def test_argument_with_atoms_fails():
    # 논증 문서로 판정했으면 원자를 만들지 않는다 — thesis가 원자의 우회로가 되면 안 된다
    data = {'docs': [_doc(kind_of_doc='argument',
                          thesis={'line': 1, 'claim': 'x', 'line_text': 'y'})]}
    errs = st.validate(data, atom_counts={'semi:a:b': 13})
    assert any('원자' in e for e in errs)


def test_argument_with_atoms_passes_when_legacy():
    # 이 스펙 이전에 원자화된 문서는 소급 삭제하지 않기로 했다 — 그 하나만 열어 둔다
    data = {'docs': [_doc(kind_of_doc='argument', legacy_atoms=True,
                          thesis={'line': 1, 'claim': 'x', 'line_text': 'y'})]}
    assert st.validate(data, atom_counts={'semi:a:b': 13}) == []


def test_quantitative_with_atoms_passes():
    assert st.validate({'docs': [_doc(kind_of_doc='quantitative')]},
                       atom_counts={'semi:a:b': 13}) == []


def test_missing_kind_of_doc_defaults_to_quantitative():
    assert st.validate({'docs': [_doc()]}, atom_counts={'semi:a:b': 5}) == []


def test_structure_needs_two_items():
    d = _doc(structures=[{'kind': 'process', 'name': 'x', 'line': 3, 'steps': ['하나']}])
    assert any('2개 미만' in e for e in st.validate({'docs': [d]}))


def test_jaccard_zero_when_labels_differ():
    # 실측: 리포트마다 자기 어휘를 써서 라벨이 안 겹친다 — 그래서 의미 묶기가 따로 필요하다
    assert st.jaccard(['설계', '조립'], ['범프 피치', '레티클']) == 0.0
