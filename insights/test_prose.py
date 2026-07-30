import check_prose as cp


def _run(fn, text, gloss=None):
    cp.findings.clear()
    if gloss is None:
        fn(text, 'x.md')
    else:
        fn(text, 'x.md', gloss)
    return [(f[0], f[2]) for f in cp.findings]


def test_strip_refs_removes_atom_ids():
    t = '공랭은 41kW에서 막힌다(A-250214-07). 다음(A-260226-05, A-260226-08).'
    out = cp.strip_refs(t)
    assert 'A-250214-07' not in out
    assert 'A-260226-05' not in out
    assert '공랭은 41kW에서 막힌다' in out


def test_strip_refs_removes_frontmatter():
    t = '---\nview: stack\natoms: [A-1]\n---\n\n## 주장\n**x**\n'
    out = cp.strip_refs(t)
    assert 'view: stack' not in out
    assert '## 주장' in out


def test_sentences_splits_korean():
    s = cp.sentences('첫 문장이다. 둘째 문장이다! 셋째?')
    assert len(s) == 3


def test_banned_word_fails():
    out = _run(cp.check_banned, '냉각 방식이 벤더별로 갈라진다.')
    assert ('FAIL', 'P1') in out


def test_no_banned_word_passes():
    out = _run(cp.check_banned, '냉각 방식이 장비를 만드는 회사별로 갈라진다.')
    assert out == []


def test_glossary_term_without_gloss_fails():
    out = _run(cp.check_glossary, '공랭은 41kW에서 막힌다.', {'공랭': '공기로 식히는 방식'})
    assert ('FAIL', 'P2') in out


def test_glossary_term_with_paren_passes():
    out = _run(cp.check_glossary, '공랭(공기로 식히는 방식)은 41kW에서 막힌다.',
               {'공랭': '공기로 식히는 방식'})
    assert out == []


def test_glossary_term_with_plain_words_passes():
    # 괄호가 용어 뒤가 아니라 앞에 붙는 형태도 통과해야 한다 — 발열 한도(TDP)
    out = _run(cp.check_glossary, '칩 한 장의 발열 한도(TDP)가 올랐다.', {'TDP': '발열 한도'})
    assert out == []


def test_glossary_checks_first_occurrence_only():
    # 첫 등장에서 풀었으면 이후 등장은 그냥 써도 된다
    t = '공랭(공기로 식히는 방식)은 막힌다. 공랭 물량은 남아 있다.'
    out = _run(cp.check_glossary, t, {'공랭': '공기로 식히는 방식'})
    assert out == []
