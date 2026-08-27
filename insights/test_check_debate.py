# -*- coding: utf-8 -*-
import datetime
import check_debate as cd

HEAD = '''---
view: debate
question: 무엇이 먼저인가?
as_of: 2026-08-27
closes_when: {what: "엔비디아 실적", by: 2026-12-31}
sources:
  - {file: "content/understanding/회계사/[260820] 바이백을 두 배로 늘렸다 - 엘곰.md", note: "가"}
---
'''

BODY_OK = '''
## 물음

두 글이 인과를 반대로 놓는다.

## 발언

### 엘곰 · 2026-08-20 · 「바이백」
- 관계: 단독
- 주장: 투자가 금리를 정한다
회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).

## 답하지 않은 화자

- SemiAnalysis — 같은 기간 조달비용을 다룬 글이 없다

## 갈리는 자리

금리 수준이 임계다.

## 무엇을 보면 갈리나

30년물이 5.3%를 넘기는지.
'''

# D8 전용 — 발언 둘인 문서. 하나는 정상 제목줄로 더 넣어 「### 줄 수 == voices
# 수」가 맞는 기준 문서로 쓰고, 이걸 망가뜨려 D8을 건다.
BODY_TWO_OK = BODY_OK.replace(
    '## 답하지 않은 화자',
    '### 이선엽 · 2026-08-21 · 「금리」\n'
    '- 관계: 단독\n'
    '- 주장: 조달비용이 실적을 정한다\n'
    '조달비용이 이미 실적에 반영됐다 ([260821] 금리 L5).\n\n'
    '## 답하지 않은 화자')

TODAY = datetime.date(2026, 8, 27)


def rules(found):
    return [r for _, r, _ in found]


def no_d7(found):
    """D7 은 저장소의 노트 파일을 읽는다 — 단위 테스트에서는 빼고 본다."""
    return [(lv, r, m) for lv, r, m in found if r != 'D7']


def test_clean_doc_has_no_findings():
    assert no_d7(cd.check('x.md', HEAD + BODY_OK, TODAY)) == []


def test_d1_flags_moderator_sentence_inside_voice():
    bad = BODY_OK.replace(
        '회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).',
        '회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).\n'
        '이 설명이 더 그럴듯하다.')
    assert 'D1' in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d1_ignores_label_lines():
    assert 'D1' not in rules(cd.check('x.md', HEAD + BODY_OK, TODAY))


def test_d2_flags_dangling_relation_target():
    bad = BODY_OK.replace('- 관계: 단독', '- 관계: 충돌 ↔ 이선엽 08-19 「없는 글」')
    assert 'D2' in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d3_flags_unknown_stance():
    bad = BODY_OK.replace('- 관계: 단독', '- 관계: 반박')
    assert 'D3' in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d4_flags_stale_as_of_after_close_date():
    bad = (HEAD.replace('by: 2026-12-31', 'by: 2026-08-20')
               .replace('as_of: 2026-08-27', 'as_of: 2026-08-19'))
    assert 'D4' in rules(cd.check('x.md', bad + BODY_OK, TODAY))


def test_d4_passes_when_as_of_moved_past_close_date():
    ok = HEAD.replace('by: 2026-12-31', 'by: 2026-08-20')
    assert 'D4' not in rules(cd.check('x.md', ok + BODY_OK, TODAY))


def test_d5_flags_verdict_word_in_moderator_section():
    bad = BODY_OK.replace('금리 수준이 임계다.', '엘곰이 맞았다.')
    assert 'D5' in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d5_ignores_verdict_word_inside_voice():
    bad = BODY_OK.replace(
        '회사채 발행이 매수 여력을 두고 경쟁한다',
        '앞선 예측이 맞았다고 적는다')
    assert 'D5' not in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d6_warns_when_single_voice_and_no_silent_list():
    bad = BODY_OK.replace(
        '- SemiAnalysis — 같은 기간 조달비용을 다룬 글이 없다', '')
    found = cd.check('x.md', HEAD + bad, TODAY)
    assert ('WARN', 'D6') in [(lv, r) for lv, r, _ in found]


def test_d8_flags_malformed_voice_heading():
    """제목줄이 두 자리 연도로 어긋나면 그 발언이 통째로 안 읽힌다 — 예외도
    경고도 없이 사라지던 것을, ### 줄 수와 voices 수를 대조해 잡는다."""
    bad = BODY_TWO_OK.replace(
        '### 이선엽 · 2026-08-21 · 「금리」',
        '### 이선엽 · 26-08-21 · 「금리」')
    assert 'D8' in rules(cd.check('x.md', HEAD + bad, TODAY))


def test_d8_silent_on_two_well_formed_voices():
    assert 'D8' not in rules(cd.check('x.md', HEAD + BODY_TWO_OK, TODAY))


def test_d1_passes_with_decimal_point():
    """소수점이 든 정상 문장에 D1이 안 뜬다."""
    decimal_body = BODY_OK.replace(
        '회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).',
        '발표 직후 30년물은 9bp 내려 5.18~5.20%대가 됐다 ([260820] 바이백을 두 배로 L21).')
    assert 'D1' not in rules(no_d7(cd.check('x.md', HEAD + decimal_body, TODAY)))


def test_d1_detects_after_decimal_sentence():
    """소수점 정상 문장 뒤에 인용 없는 문장이 있으면 D1이 뜬다."""
    bad = BODY_OK.replace(
        '회사채 발행이 매수 여력을 두고 경쟁한다 ([260820] 바이백을 두 배로 L17).',
        '발표 직후 30년물은 9bp 내려 5.18~5.20%대가 됐다 ([260820] 바이백을 두 배로 L21).\n'
        '이 설명이 더 그럴듯하다.')
    assert 'D1' in rules(no_d7(cd.check('x.md', HEAD + bad, TODAY)))
