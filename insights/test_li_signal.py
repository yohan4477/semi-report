# -*- coding: utf-8 -*-
import li_signal as ls

PUB = {'some-newsletter': '2026-08-01'}


def test_meme_is_excluded():
    kind, usable, _b, _l, _p = ls.classify(
        '밈: 셀카에 “Gemini, who?” 자막을 얹은 사진 한 장.', None, '2026-08-14', PUB)
    assert usable is False
    assert kind == '밈·농담'


def test_event_is_excluded():
    kind, usable, _b, _l, push = ls.classify(
        '8월 27일 목요일 저녁 뉴욕 미드타운에서 초청제 모임을 연다고 알렸다.',
        None, '2026-08-18', PUB)
    assert usable is False
    assert push is True


def test_past_recollection_is_excluded():
    _k, usable, _b, _l, _p = ls.classify(
        '젠슨 황이 90년대 Dreamcast GPU 계약으로 맺은 인연을 회고했다.',
        None, '2026-07-16', PUB)
    assert usable is False


def test_repromotion_is_excluded():
    kind, usable, basis, lag, push = ls.classify(
        '지난 리포트를 다시 소개한다.', 'some-newsletter', '2026-09-01', PUB)
    assert kind == '재홍보'
    assert usable is False
    assert basis == '2026-08-01'
    assert lag > ls.LAG_MAX
    assert push is True


def test_fresh_newsletter_link_is_not_a_citation_target():
    """원본 뉴스레터를 인용하면 되므로 링크드인은 인용 대상이 아니다."""
    kind, usable, basis, _l, _p = ls.classify(
        '새 리포트를 냈다.', 'some-newsletter', '2026-08-03', PUB)
    assert kind == '신규 발행 알림'
    assert usable is False
    assert basis == '2026-08-01'


def test_commentary_without_numbers_is_now_usable():
    """137건이 잔여물이었다 — 숫자가 없어도 명명된 주체의 검증 가능한 주장은 쓴다."""
    _k, usable, _b, _l, _p = ls.classify(
        'AMD의 최상위 AI 엔지니어 대부분이 상하이에 있다. MoRI 그룹, '
        'KV 캐시 오프로딩·풀링 팀이 여기 몰려 있다.', None, '2026-08-06', PUB)
    assert usable is True


def test_inch_units_are_usable():
    """좁은 NUM 정규식이 「2~4인치 웨이퍼」를 떨어뜨렸다."""
    _k, usable, _b, _l, _p = ls.classify(
        'III-V 업계는 아직 2~4인치 웨이퍼가 표준이라 12인치 CMOS와 비교하면 다르다.',
        None, '2026-07-31', PUB)
    assert usable is True


def test_has_video_flag_does_not_exclude():
    """라운드 2 지시사항: has_video=True를 넘겨도 배제 목록에 안 걸리면 usable이다.
    AMD MI355X InferenceX 비교(밈 영상 자막에 수치 주장)가 실제 사례 — 카드가 이미
    이 글을 인용하므로 or has_video를 되살리면 이 테스트가 바로 잡아낸다."""
    _k, usable, _b, _l, _p = ls.classify(
        'AMD의 Anush Elangovan 팀이 밈 영상을 올렸는데 영상 자막에 수치 주장이 박혀 있다 — '
        'SemiAnalysis InferenceX 측정에서 MI355X의 vLLM이 B200의 vLLM보다 낫다.',
        None, '2026-08-15', PUB, has_video=True)
    assert usable is True


def test_parody_meme_is_excluded():
    """라운드 2: 「패러디」·「유머」는 「밈」이라는 낱말 없이도 밈이다 — 만우절 가짜 보도자료
    실제 글(L-20260416-3056)이 233건 중 하나로 usable에 남아 있었다."""
    kind, usable, _b, _l, _p = ls.classify(
        '만우절 패러디 — SemiAnalysis가 브랜드를 매각하고 신발·의류 사업으로 '
        '피벗한다는 가짜 보도자료', None, '2026-04-16', PUB)
    assert usable is False
    assert kind == '밈·농담'


def test_english_event_promo_is_excluded():
    """라운드 2: 정규식이 한국어 표지만 잡아 영어 행사 홍보 원문(L-20260428-1808,
    Milipol TechX 2026)이 걸러지지 않았다. 실제 게시물 원문 그대로."""
    kind, usable, _b, _l, push = ls.classify(
        "Here's your reminder to join us at Milipol TechX 2026! "
        "We'll be hosting two fireside chats.",
        None, '2026-04-28', PUB)
    assert usable is False
    assert kind == '행사·모임'
    assert push is True
