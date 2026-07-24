import gen_insights as g

def test_slugify_strips_tags_and_symbols():
    assert g.slugify('호남 반도체 산단, 4년 <span>x</span>') == '호남-반도체-산단-4년-x'

def test_parse_front_matter_scalars_and_sources():
    raw = 'cluster_id: A\ntitle: "이란 전쟁"\nsources:\n  - "카드 하나"\n  - "카드 둘"\nupdated: 2026-07-25'
    fm = g.parse_front_matter(raw)
    assert fm['cluster_id'] == 'A'
    assert fm['title'] == '이란 전쟁'
    assert fm['sources'] == ['카드 하나', '카드 둘']

def test_md_to_html_headings_bullets_bold():
    html = g.md_to_html('## 공통 진단\n- 첫째 **강조**\n- 둘째\n')
    assert '<h4>공통 진단</h4>' in html
    assert '<li>첫째 <b>강조</b></li>' in html
