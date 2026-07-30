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


def test_sentences_splits_markdown():
    # 마크다운 형태 - **소제목.** 본문 같은 경우도 문장으로 쪼개져야 한다
    s = cp.sentences('- **칠러가 있다.** 그런데 칠러는 비싸다.')
    assert len(s) == 2
    assert '칠러가 있다' in s[0]
    assert '칠러는 비싸다' in s[1]


def test_glossary_term_with_reverse_paren_passes():
    # 역순 괄호 형태: 설명(용어) 형태도 통과해야 한다
    # 실제 코퍼스: 열교환기(RDHx) 형태는 사전의 "랙 뒤에 붙이는 열교환기"와
    # 정확히 안 맞아도 개념이 전달되면 통과
    out = _run(cp.check_glossary, '뒤에 열교환기(RDHx)를 붙여...', {'RDHx': '랙 뒤에 붙이는 열교환기'})
    assert ('FAIL', 'P2') not in out


def test_load_glossary_excludes_underscore_keys(tmp_path, monkeypatch):
    # _로 시작하는 키는 제외된다
    gloss_file = tmp_path / 'test_glossary.json'
    gloss_file.write_text('{"_note": "metadata", "공랭": "공기로"}', encoding='utf-8')
    monkeypatch.setattr(cp, 'GLOSSARY', str(gloss_file))
    g = cp.load_glossary()
    assert '_note' not in g
    assert g == {'공랭': '공기로'}


def test_load_glossary_returns_empty_when_file_missing(monkeypatch):
    # 파일이 없으면 빈 사전을 돌려준다
    monkeypatch.setattr(cp, 'GLOSSARY', '/nonexistent/glossary.json')
    g = cp.load_glossary()
    assert g == {}


def test_strip_then_glossary_pipeline():
    # 원자 인용 괄호는 제거되고, 용어 설명 괄호는 살아있어 P2 통과해야 한다
    t = '공랭(공기로 식히는 방식)은 41kW에서 막힌다(A-250214-07).'
    stripped = cp.strip_refs(t)
    out = _run(cp.check_glossary, stripped, {'공랭': '공기로 식히는 방식'})
    assert out == []
    assert 'A-250214-07' not in stripped
    assert '공랭(공기로 식히는 방식)' in stripped
