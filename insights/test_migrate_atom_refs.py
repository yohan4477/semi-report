import migrate_atom_refs as m

INDEX = {
    'A-260807b-01': ('content/newsletter/ai_infra/business/[260807] 스페이스X.md', 41),
    'A-260807b-15': ('content/newsletter/ai_infra/business/[260807] 스페이스X.md', 137),
    'A-250214-01': ('content/newsletter/ai_infra/cooling/[250214] 냉각.md', 12),
}


def test_single_ref_becomes_line_cite():
    out, used = m.convert('목표다(A-260807b-01).', INDEX)
    assert out == '목표다([260807] 스페이스X L41).'
    assert used == ['content/newsletter/ai_infra/business/[260807] 스페이스X.md']


def test_multiple_refs_in_one_paren():
    out, _ = m.convert('둘이다(A-260807b-01, A-260807b-15).', INDEX)
    assert out == '둘이다([260807] 스페이스X L41, L137).'


def test_refs_from_two_docs_split_into_two_cites():
    # 괄호를 문서마다 따로 연다. 한 괄호에 합치면 뒤 문서의 줄번호가 앞 문서
    # 줄로 읽힌다 — 검사기가 실제로 세 건을 그렇게 잘못 잡았다
    out, used = m.convert('섞였다(A-260807b-01, A-250214-01).', INDEX)
    assert out == '섞였다([260807] 스페이스X L41) ([250214] 냉각 L12).'
    assert len(used) == 2


def test_unknown_ref_is_left_alone():
    out, used = m.convert('모른다(A-999999-99).', INDEX)
    assert out == '모른다(A-999999-99).'
    assert used == []


def test_prose_is_untouched():
    src = '전기를 더 사도 채울 칩이 없으면 소용이 없다(A-260807b-01).'
    out, _ = m.convert(src, INDEX)
    assert out.startswith('전기를 더 사도 채울 칩이 없으면 소용이 없다(')
