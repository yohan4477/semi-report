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

import os, io, tempfile

def _mkfile(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, 'w', encoding='utf-8').write(text)
    return p

def test_scan_ids_and_excludes_통합(tmp_path):
    root = str(tmp_path)
    _mkfile(root, 'content/newsletter/ai_infra/cooling/[250214] 냉각.md', 'x')
    _mkfile(root, 'content/understanding/권효재 대표/미국 데이터센터.md', 'published: 2026-07-24\n')
    _mkfile(root, 'content/understanding/통합/A-이란.md', 'insight body')  # 제외돼야
    bases = [(os.path.join(root, 'content', 'newsletter'), 'semianalysis', 'semi'),
             (os.path.join(root, 'content', 'understanding'), 'understanding', 'und')]
    out = gm.scan(bases, root)
    ids = {s['id'] for s in out}
    assert 'semi:cooling:냉각' in ids
    assert any(s['id'].startswith('und:권효재 대표:') for s in out)
    assert not any(':통합:' in s['id'] for s in out)   # 통합 폴더 제외
    cool = next(s for s in out if s['id'] == 'semi:cooling:냉각')
    assert cool['corpus'] == 'semianalysis' and cool['date'] == '2025-02-14'
    assert cool['path'] == 'content/newsletter/ai_infra/cooling/[250214] 냉각.md'
