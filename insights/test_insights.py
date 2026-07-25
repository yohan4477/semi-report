import gen_manifest as gm

def test_slug_strips_datecode_and_ext():
    assert gm.slug('[260711] 컴퓨트 통합 리포트.md') == '컴퓨트-통합-리포트'

def test_parse_date_from_datecode():
    assert gm.parse_date('[250214] 냉각.md', '') == '2025-02-14'

def test_parse_date_from_frontmatter():
    assert gm.parse_date('제목.md', 'published: 2026-01-02\n') == '2026-01-02'

def test_parse_date_none():
    assert gm.parse_date('제목.md', '내용') is None

def test_body_hash_changes_with_content():
    assert gm.body_hash('a') != gm.body_hash('b')
    assert len(gm.body_hash('a')) == 12

def test_source_id_shape():
    assert gm.source_id('semianalysis', 'cooling', '[250214] 냉각 시스템.md') == 'semi:cooling:냉각-시스템'
