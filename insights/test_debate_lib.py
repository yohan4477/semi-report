# -*- coding: utf-8 -*-
import debate_lib as dl

DOC = '''---
view: debate
question: AI 설비투자가 금리를 미나, 금리가 투자를 정하나?
as_of: 2026-08-27
closes_when: {what: "엔비디아 실적 가이던스", by: 2026-08-27}
sources:
  - {file: "content/understanding/회계사/[260820] 바이백을 두 배로 늘렸다 - 엘곰.md", note: "가"}
  - {file: "content/understanding/회계사/[260820] 삼성전자 9% 급등 - 엘곰.md", note: "나"}
---

## 물음

두 글이 인과를 반대로 놓는다.

## 발언

### 엘곰 · 2026-08-20 · 「삼성전자 9% 급등」
- 관계: 충돌 ↔ 엘곰 08-20 「바이백」
- 주장: 금리가 투자를 정한다
금리가 내리면 조달금리가 따라 내린다 ([260820] 삼성전자 9% L23).

### 엘곰 · 2026-08-20 · 「바이백」
- 관계: 단독
- 주장: 투자가 금리를 정한다
회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).

## 답하지 않은 화자

- SemiAnalysis — 같은 기간 조달비용을 다룬 글이 없다

## 갈리는 자리

금리 수준이 임계다.

## 무엇을 보면 갈리나

30년물이 5.3%를 넘긴 뒤 청약배수가 1.6배 아래로 가는지.
'''


def test_parse_reads_frontmatter_and_sources():
    d = dl.parse(DOC)
    assert d['meta']['view'] == 'debate'
    assert len(d['sources']) == 2
    assert d['sources'][0]['base'].startswith('[260820] 바이백')


def test_parse_splits_five_sections():
    d = dl.parse(DOC)
    assert set(d['sections']) == {
        '물음', '발언', '답하지 않은 화자', '갈리는 자리', '무엇을 보면 갈리나'}
    assert '두 글이 인과를' in d['sections']['물음']


def test_parse_reads_two_voices():
    d = dl.parse(DOC)
    v = d['voices']
    assert len(v) == 2
    assert v[0]['actor'] == '엘곰'
    assert v[0]['said'] == '2026-08-20'
    assert v[0]['title'] == '삼성전자 9% 급등'
    assert v[0]['stance'] == '충돌'
    assert v[0]['against'] == '엘곰 08-20 「바이백」'
    assert v[0]['claim'] == '금리가 투자를 정한다'
    assert '조달금리가 따라 내린다' in v[0]['body']


def test_solo_voice_has_no_target():
    d = dl.parse(DOC)
    assert d['voices'][1]['stance'] == '단독'
    assert d['voices'][1]['against'] == ''


def test_voice_body_excludes_label_lines():
    d = dl.parse(DOC)
    assert '관계:' not in d['voices'][0]['body']
    assert '주장:' not in d['voices'][0]['body']


def test_voice_key_matches_relation_target():
    d = dl.parse(DOC)
    assert dl.voice_key(d['voices'][1]) == '엘곰 08-20 「바이백」'
    assert d['voices'][0]['against'] == dl.voice_key(d['voices'][1])
