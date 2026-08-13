import io
import os
import notes_lib as nl
import paths

FRONT = '''---
source: "input/clippings/Foo Bar.md"
date: 2026-08-07
sources:
  - {file: "input/clippings/Foo Bar.md", date: "2026-08-07", note: "가"}
  - {file: "content/newsletter/[251231] 온사이트 가스 딥다이브.md", date: "2025-12-31", note: "나"}
---

본문 첫 줄(Foo Bar L12).
두 번째 문단이다(온사이트 가스 딥다이브 L51, L60).
'''


def test_parse_front_splits_meta_and_body():
    meta, body = nl.parse_front(FRONT)
    assert meta['date'] == '2026-08-07'
    assert body.strip().startswith('본문 첫 줄')


def test_sources_of_reads_two_entries():
    meta, _ = nl.parse_front(FRONT)
    src = nl.sources_of(meta)
    assert len(src) == 2
    assert src[0]['base'] == 'Foo Bar'
    assert src[1]['file'].endswith('온사이트 가스 딥다이브.md')


def test_resolve_matches_by_prefix():
    meta, _ = nl.parse_front(FRONT)
    src = nl.sources_of(meta)
    assert nl.resolve('Foo Bar', src)['base'] == 'Foo Bar'


def test_resolve_matches_by_substring():
    # 사람은 「온사이트 가스 딥다이브」라고 줄여 쓰는데 파일명은 [251231]로 시작한다.
    # 앞머리 일치만 보면 놓친다 — 실제로 머스크 판에서 7건 놓쳤다
    meta, _ = nl.parse_front(FRONT)
    src = nl.sources_of(meta)
    assert nl.resolve('온사이트 가스 딥다이브', src) is not None


def test_resolve_returns_none_for_unknown():
    meta, _ = nl.parse_front(FRONT)
    assert nl.resolve('없는 문서', nl.sources_of(meta)) is None


def test_cite_refs_finds_both_and_multiline():
    meta, body = nl.parse_front(FRONT)
    refs = nl.cite_refs(body, nl.sources_of(meta))
    assert len(refs) == 2
    assert refs[0]['lines'] == [12]
    assert refs[1]['lines'] == [51, 60]
    assert all(r['ok'] for r in refs)


def test_cite_refs_marks_unresolved():
    meta, _ = nl.parse_front(FRONT)
    refs = nl.cite_refs('무엇(없는 문서 L3).', nl.sources_of(meta))
    assert refs[0]['ok'] is False


def test_line_hash_is_stable_and_none_past_eof():
    p = os.path.join(paths.ROOT, 'insights', 'world_path.txt')
    assert nl.line_hash(p, 1) == nl.line_hash(p, 1)
    assert len(nl.line_hash(p, 1)) == 12
    assert nl.line_hash(p, 10 ** 7) is None
