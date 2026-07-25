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

import coverage as cov
import validate_insights as vi

MAN = {'sources': [
    {'id': 'und:oil:밥엘만데브', 'category': 'oil', 'hash': 'h1'},
    {'id': 'und:oil:하르그섬', 'category': 'oil', 'hash': 'h2'},
    {'id': 'semi:robotics:unitree', 'category': 'robotics', 'hash': 'h3'},
]}

def test_parse_cluster_frontmatter():
    md = '---\ncluster_id: A\ncategories: [oil]\nsources: ["und:oil:밥엘만데브"]\nsource_hashes: {"und:oil:밥엘만데브":"h1"}\n---\n본문'
    c = cov.parse_cluster(md)
    assert c['cluster_id'] == 'A' and c['categories'] == ['oil']
    assert c['sources'] == ['und:oil:밥엘만데브']
    assert c['source_hashes']['und:oil:밥엘만데브'] == 'h1'

def test_classify_stale_new_category_source():
    A = {'cluster_id': 'A', 'categories': ['oil'], 'sources': ['und:oil:밥엘만데브'],
         'source_hashes': {'und:oil:밥엘만데브': 'h1'}}
    r = cov.classify(MAN, [A])
    assert 'A' in r['stale']
    assert 'semi:robotics:unitree' in r['uncovered']

def test_classify_stale_changed_hash():
    A = {'cluster_id': 'A', 'categories': ['oil'],
         'sources': ['und:oil:밥엘만데브', 'und:oil:하르그섬'],
         'source_hashes': {'und:oil:밥엘만데브': 'OLD', 'und:oil:하르그섬': 'h2'}}
    r = cov.classify(MAN, [A])
    assert 'A' in r['stale']

def test_classify_ok():
    A = {'cluster_id': 'A', 'categories': ['oil'],
         'sources': ['und:oil:밥엘만데브', 'und:oil:하르그섬'],
         'source_hashes': {'und:oil:밥엘만데브': 'h1', 'und:oil:하르그섬': 'h2'}}
    r = cov.classify(MAN, [A])
    assert r['stale'] == {} and 'A' in r['ok']

def test_validate_flags_missing_source():
    A = {'cluster_id': 'A', 'categories': ['oil'], 'sources': ['und:oil:없는것'],
         'source_hashes': {}}
    errs = vi.validate(MAN, [A])
    assert any('없는것' in e for e in errs)

def test_parse_date_발행일_not_정리일():
    body = '> **정리일** 2026-07-24 · 자막 기반 요약\n> **발행일**: 2026-05-01\n'
    assert gm.parse_date('제목.md', body) == '2026-05-01'   # 발행일, 정리일 아님

def test_parse_date_정리일만있으면_None():
    assert gm.parse_date('제목.md', '> **정리일** 2026-07-24 · 자막 기반 요약\n') is None

def test_parse_date_출처줄_날짜():
    assert gm.parse_date('제목.md', '> 출처: 언더스탠딩 김상훈 기자(…), 2026-07-22. 요약임\n') == '2026-07-22'

def test_body_hash_ignores_frontmatter():
    a = gm.body_hash('---\ncategories: [x]\n---\n본문')
    b = gm.body_hash('---\ncategories: [x, y]\n---\n본문')   # 태그만 다름
    assert a == b   # 본문 같으면 hash 같다

def test_read_categories_priority():
    ov = {'sid1': ['oil']}
    assert gm.read_categories('categories: [compute, memory]\n', 'compute', 'sid1', ov) == ['compute', 'memory']  # frontmatter 우선
    assert gm.read_categories('본문', 'folderX', 'sid1', ov) == ['oil']   # 오버레이
    assert gm.read_categories('본문', 'folderX', 'sid2', ov) == ['folderX']  # 폴더 fallback

def test_expand_taxonomy_descendants():
    import coverage as cov
    tax = {'oil': ['oil-geopolitics', 'oil-supplychain']}
    assert cov.expand(['oil'], tax) == {'oil', 'oil-geopolitics', 'oil-supplychain'}
    assert cov.expand(['oil-geopolitics'], tax) == {'oil-geopolitics'}   # 자식은 부모로 안 올라감

def test_classify_hierarchy_routing():
    import coverage as cov
    man = {'sources': [{'id': 'semi:compute:new', 'categories': ['oil-geopolitics'], 'hash': 'h'}]}
    A = {'cluster_id': 'A', 'categories': ['oil'], 'sources': [], 'source_hashes': {}}
    r = cov.classify(man, [A], tax={'oil': ['oil-geopolitics']})
    assert 'A' in r['stale']            # oil 클러스터가 oil-geopolitics 소스를 흡수(계층)
    assert r['uncovered'] == []
