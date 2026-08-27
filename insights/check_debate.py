# -*- coding: utf-8 -*-
"""쟁점 — 화자 말과 진행자 말이 섞였는지 본다.

이 장은 만들어진 구성물이다. 화자들은 서로를 안 읽는다. 그래서 지어낸 대사가
들어가는 것을 기계가 막는다 — 화자 절의 문장은 전부 인용 마커를 달아야 하고,
진행자는 누가 맞았는지 적지 못한다.

  PYTHONIOENCODING=utf-8 python insights/check_debate.py
"""
import datetime
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import debate_lib as dl
import notes_lib as nl
import paths

# 진행자가 못 쓰는 말. 승패를 적는 순간 이 장은 검증 대장이 되고, 거기 규칙은
# 판정을 사후에 끼워 넣지 말라는 것이다
VERDICT = ('맞았', '틀렸', '옳다', '옳았', '승자', '패자',
           '이겼', '졌다', '정답', '적중')
DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')
BY_RE = re.compile(r'by:\s*(\d{4}-\d{2}-\d{2})')
# 문장 끝 기호로 자른다. 인용 마커가 문장 안에 있는지 보려면 문장 단위여야 한다
# 숫자 사이의 마침표는 문장 끝이 아니다 — `5.18~5.20%` 가 문장을 셋으로 쪼개
# 앞 조각이 인용 없는 문장으로 잡혔다
SENT_RE = re.compile(r'(?:[^.!?\n]|(?<=\d)[.](?=\d))+[.!?]?')
# D8 — 제목줄 형식이 맞든 안 맞든 「### 」로 시작하는 줄은 무조건 센다. 형식이
# 틀려 VOICE_RE 가 못 읽은 발언은 voices 개수에서 그냥 빠져 버린다
VOICE_HEAD_RE = re.compile(r'^###[ \t]', re.M)
_notes_cache = []


def _date(s):
    m = DATE_RE.search(s or '')
    return datetime.date(*[int(x) for x in m.group(1).split('-')]) if m else None


def _notes_heads():
    """노트 앞머리를 한 번만 읽어 둔다 — 쟁점마다 349장을 다시 열면 느리다."""
    if not _notes_cache:
        for p in sorted(glob.glob(os.path.join(paths.NOTES, '*.md'))):
            _notes_cache.append(io.open(p, encoding='utf-8',
                                        errors='replace').read(1200))
    return _notes_cache


def _note_exists(src_file):
    """이 원문을 source: 로 가리키는 노트가 있나."""
    base = os.path.basename(src_file)
    return any(base in head for head in _notes_heads())


def check(path, text, today):
    out = []
    d = dl.parse(text)
    meta, secs, voices = d['meta'], d['sections'], d['voices']
    keys = {dl.voice_key(v) for v in voices}

    for v in voices:
        who = '%s %s' % (v['actor'], v['said'])
        # D1 — 화자 절 문장은 전부 인용을 달아야 한다
        for sent in SENT_RE.findall(v['body']):
            if len(sent.strip()) < 10:
                continue
            if not nl.CITE.search(sent):
                out.append(('FAIL', 'D1',
                            '%s 발언에 인용 없는 문장이 있다: %s…'
                            % (who, sent.strip()[:40])))
        # D3 — 관계 값
        if v['stance'] not in dl.STANCES:
            out.append(('FAIL', 'D3',
                        '%s 의 관계 「%s」는 %s 밖이다'
                        % (who, v['stance'], ' · '.join(dl.STANCES))))
        # D2 — 관계 대상
        elif v['stance'] != '단독' and v['against'] not in keys:
            out.append(('FAIL', 'D2',
                        '%s 가 가리킨 「%s」가 이 쟁점에 없다'
                        % (who, v['against'])))

    # D8 — 「발언」 절의 ### 줄 수와 실제로 읽힌 voices 수가 다르면, 제목줄
    # 형식이 틀려 발언이 예외도 경고도 없이 통째로 사라진 것이다
    voice_sec = secs.get('발언', '')
    n_heads = len(VOICE_HEAD_RE.findall(voice_sec))
    if n_heads != len(voices):
        out.append(('FAIL', 'D8',
                    '「발언」 절에 ### 줄이 %d개인데 읽힌 발언은 %d개다 — '
                    '제목줄은 「### 화자 · YYYY-MM-DD · 「제목」」 형식이어야 한다'
                    % (n_heads, len(voices))))

    # D4 — 닫힐 날짜가 지났는데 as_of 를 안 옮겼다
    m = BY_RE.search(meta.get('closes_when', ''))
    by = _date(m.group(1)) if m else None
    as_of = _date(meta.get('as_of', ''))
    if by and by < today and as_of and as_of <= by:
        out.append(('FAIL', 'D4',
                    '닫힐 날짜 %s 가 지났다 — 답이 나왔는지 확인하고 as_of 를 옮긴다'
                    % by))

    # D5 — 진행자 절 판정어
    for name in dl.MODERATOR:
        body = secs.get(name, '')
        for w in VERDICT:
            if w in body:
                out.append(('FAIL', 'D5',
                            '진행자 절 「%s」에 판정어 「%s」가 있다 — 진행자는 심판이 아니다'
                            % (name, w)))
                break

    # D6 — 한 명만 답했는데 답 안 한 화자를 안 적었다
    if len(voices) <= 1 and not secs.get('답하지 않은 화자', '').strip():
        out.append(('WARN', 'D6',
                    '발언이 하나인데 답하지 않은 화자가 비었다 — 한 명만 답한 것도 결과다'))

    # D7 — 원문을 가리키는 노트
    for s in d['sources']:
        if not _note_exists(s['file']):
            out.append(('FAIL', 'D7',
                        '%s 를 가리키는 노트가 insights/notes/ 에 없다'
                        % os.path.basename(s['file'])))
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    today = datetime.date.today()
    files = sorted(glob.glob(os.path.join(paths.DEBATE, '*.md')))
    fails = 0
    for p in files:
        text = io.open(p, encoding='utf-8').read()
        for level, rule, msg in check(p, text, today):
            fails += level == 'FAIL'
            print('%s %s [%s] %s' % (level, os.path.basename(p), rule, msg))
    print('\n요약: 쟁점 %d장 / FAIL %d' % (len(files), fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
