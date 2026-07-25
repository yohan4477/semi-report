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

CARD = '<div class="ucard"><h2>이란 전쟁 <span>(1부)</span></h2></div>'

def test_inject_card_ids_adds_anchor_and_map():
    out, m = g.inject_card_ids(CARD)
    assert 'id="card-이란-전쟁-1부"' in out
    assert m['이란 전쟁 (1부)'] == '#card-이란-전쟁-1부'

def test_inject_card_ids_idempotent():
    out1, _ = g.inject_card_ids(CARD)
    out2, _ = g.inject_card_ids(out1)
    assert out1 == out2

def test_resolve_sources_matches_and_warns():
    _, m = g.inject_card_ids(CARD)
    ok, miss = g.resolve_sources(['이란 전쟁 (1부)', '없는 카드'], m)
    assert ok == [('이란 전쟁 (1부)', '#card-이란-전쟁-1부')]
    assert miss == ['없는 카드']

def test_render_block_has_thesis_and_source_chip():
    fm = {'cluster_id': 'A', 'title': '이란 전쟁', 'subtitle': '부제', 'sources': ['이란 전쟁 (1부)']}
    _, m = g.inject_card_ids(CARD)
    html, miss = g.render_block(fm, '## 통합 논지\n한 줄.\n', m)
    assert '이란 전쟁' in html and '한 줄.' in html
    assert 'href="#card-이란-전쟁-1부"' in html
    assert miss == []

def test_strip_section_idempotent():
    wrapped = 'A<!-- INSIGHTS:START -->x<!-- INSIGHTS:END -->B'
    assert g.strip_section(wrapped) == 'AB'
