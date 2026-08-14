# -*- coding: utf-8 -*-
"""시점 검사 — 그 인사이트가 아직 지금 이야기인가.

맞는 말이어도 옛날 이야기면 틀린 말과 다르지 않다. 값은 뛰었다 내려가고,
"막힌다"던 자리는 풀리고, 1등은 바뀐다. 그런데 지금까지 검사기 넷은 전부
"근거가 있는가"만 봤지 "그 근거가 언제 것인가"는 안 봤다.

  F1  더 새 문서가 들어왔는데 안 고쳤다 — 같은 주제 노트가 이 글의 최신 근거보다 뒤에 있다
  F2  근거가 통째로 낡았다 — 최신 근거가 기준일보다 오래됐다(주제마다 기준이 다르다)
  F3  as_of 가 근거보다 앞선다 — 언제 기준 글인지 표기가 틀렸다

  py -3.13 insights/check_fresh.py
"""
import datetime
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes_lib as nl
import paths

# 주제마다 상하는 속도가 다르다. 값과 물량은 분기면 뒤집히고, 물리 한계는 오래 간다.
STALE_DAYS = {
    'biz': 120,     # 매출·마진·가격 — 분기마다 바뀐다
    'chip': 180,    # 칩 세대·벤치마크 — 반년이면 다음 세대가 나온다
    'model': 180,   # 모델·학습 기법
    'power': 365,   # 전력망·변압기·건물 — 연 단위로 움직인다
}
DEFAULT_STALE = 180

findings = []


def add(level, where, rule, msg):
    findings.append((level, where, rule, msg))


def load_notes():
    """노트 = 원문 1편의 대표. 날짜와 주제를 여기서 가져온다."""
    out = []
    for p in sorted(glob.glob(os.path.join(paths.NOTES, '*.md'))):
        meta, _ = nl.parse_front(io.open(p, encoding='utf-8').read())
        d = str(meta.get('date') or '').strip().strip('"')
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', d):
            continue
        topics = re.findall(r'[^\[\],\s]+', str(meta.get('topics') or ''))
        out.append({
            'path': os.path.basename(p),
            'src': str(meta.get('source') or '').strip().strip('"'),
            'date': datetime.date(*map(int, d.split('-'))),
            'topics': set(topics),
            'corpus': str(meta.get('corpus') or 'semi').strip(),
        })
    return out


def check(path, notes, today):
    where = os.path.basename(path)
    meta, _ = nl.parse_front(io.open(path, encoding='utf-8').read())
    section = str(meta.get('section') or '').strip()
    used = set(s['file'] for s in nl.sources_of(meta) if s.get('file'))

    mine = [n for n in notes if n['src'] in used]
    if not mine:
        add('WARN', where, 'F1', '인용한 원문에 대응하는 노트가 없다 — 시점을 잴 수 없다')
        return

    newest = max(n['date'] for n in mine)
    topics = set()
    for n in mine:
        topics |= n['topics']

    # F1 — 이 글이 선 자리보다 뒤에 나온 같은 주제 문서. 있으면 결론이 바뀌었을 수 있다.
    later = [n for n in notes
             if n['date'] > newest and n['src'] not in used and (n['topics'] & topics)]
    if later:
        later.sort(key=lambda n: n['date'], reverse=True)
        names = ', '.join('%s(%s)' % (n['path'][:24], n['date']) for n in later[:3])
        add('FAIL', where, 'F1',
            '최신 근거가 %s인데 그 뒤 같은 주제 문서가 %d편 있다 — 읽고 반영하거나 '
            '안 바뀐다고 판단했으면 그 근거를 쓴다: %s' % (newest, len(later), names))

    # F2 — 아무도 뒤엎지 않았어도 시간이 지나면 그냥 옛말이 된다
    limit = STALE_DAYS.get(section, DEFAULT_STALE)
    age = (today - newest).days
    if age > limit:
        add('FAIL' if age > limit * 2 else 'WARN', where, 'F2',
            '가장 새로운 근거가 %d일 전(%s)이다 — %s 주제 기준 %d일을 넘었다'
            % (age, newest, section or '기본', limit))

    # F3 — as_of 는 "언제 기준으로 읽으라"는 표시다. 근거보다 앞서면 거짓말이 된다.
    a = str(meta.get('as_of') or '').strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', a):
        asof = datetime.date(*map(int, a.split('-')))
        if asof < newest:
            add('FAIL', where, 'F3', 'as_of(%s)가 최신 근거(%s)보다 앞선다' % (asof, newest))


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    today = datetime.date.today()
    notes = load_notes()
    files = sorted(glob.glob(os.path.join(paths.BRIEFS, '*.md')) +
                   glob.glob(os.path.join(paths.SYNTH, '*.md')))
    for p in files:
        check(p, notes, today)
    for level, where, rule, msg in findings:
        print('%s %s [%s] %s' % (level, where, rule, msg))
    fails = sum(1 for f in findings if f[0] == 'FAIL')
    print('\n요약: 글 %d편 / 노트 %d장 / FAIL %d / WARN %d'
          % (len(files), len(notes), fails, len(findings) - fails))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
