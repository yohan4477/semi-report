# -*- coding: utf-8 -*-
"""시점 검사 — 그 인사이트가 아직 지금 이야기인가.

맞는 말이어도 옛날 이야기면 틀린 말과 다르지 않다. 값은 뛰었다 내려가고,
"막힌다"던 자리는 풀리고, 1등은 바뀐다. 그런데 지금까지 검사기 넷은 전부
"근거가 있는가"만 봤지 "그 근거가 언제 것인가"는 안 봤다.

  F1  더 새 문서가 들어왔는데 안 고쳤다 — 같은 주제 노트가 이 글의 최신 근거보다 뒤에 있다
  F2  근거가 통째로 낡았다 — 최신 근거가 기준일보다 오래됐다(주제마다 기준이 다르다)
  F3  as_of 가 근거보다 앞선다 — 언제 기준 글인지 표기가 틀렸다
  F4  교차 카드의 근거끼리 시차가 크다 — 대립인지 그사이 바뀐 것인지 안 밝혔다

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
        # 쉼표로만 나눈다. 공백으로도 쪼개면 「반도체 클러스터」가 「반도체」가 돼
        # 부동산 노트가 추론 경제 브리핑을 낡게 만드는 오탐이 난다(2026-08-16).
        # 대신 표기가 다르면 못 잡는다 — 「종부세」와 「종합부동산세」는 남남이다.
        # 노트를 쓸 때 topics 를 같은 말로 적는 편이 맞고, 동의어 사전은 두지 않는다.
        topics = [t.strip() for t in
                  str(meta.get('topics') or '').strip().strip('[]').split(',')]
        topics = [t for t in topics if t]
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
    # 읽고 "이건 안 바뀐다"고 판단한 것도 검토한 것이다. 그 판단을 frontmatter 의
    # checked: 에 이유와 함께 적어 두면 다음 회차에 같은 문서를 다시 뒤지지 않는다.
    seen = set(re.findall(r'file:\s*"([^"]+)"', meta.get('_head', '')))

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
             if n['date'] > newest and n['src'] not in used and n['src'] not in seen
             and (n['topics'] & topics)]
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

    # F4 — 교차 카드에서 두 문서가 "어긋난다"고 말하려면 같은 때를 봐야 한다.
    # 반년 떨어진 두 글이 다른 말을 하는 것은 대립이 아니라 그사이에 사실이 바뀐
    # 것일 수 있다. 시차가 주제 기준을 넘으면 본문이 그 시차를 밝혔는지 본다.
    # 브리핑은 쌓인 상태를 적는 자리라 시차가 당연하므로 뺀다.
    if str(meta.get('view') or '').strip() == 'cross':
        # checked: 에 적은 문서는 "읽고 안 쓰기로 했다"는 표시라 시차 계산에서 뺀다.
        head = meta.get('_head', '')
        cited = set(re.findall(r'file:\s*"([^"]+)"', head.split('\nchecked:')[0]))
        span = [n['date'] for n in mine if n['src'] in cited] or [n['date'] for n in mine]
        oldest, latest = min(span), max(span)
        spread = (latest - oldest).days
        if spread > limit:
            body = io.open(path, encoding='utf-8').read()
            # 「9개월 사이」 같은 표현은 본문이 다루는 사실의 기간일 때가 많아
            # 근거로 안 친다(2026-08-17에 「2026년 전분기」가 「2026년 전」으로
            # 잡히는 오탐까지 확인했다). 양쪽 발행 연월을 다 적은 경우만 인정한다.
            def ym(d):
                return ['%d년 %d월' % (d.year, d.month), '%04d-%02d' % (d.year, d.month)]
            told = (any(m in body for m in ym(oldest))
                    and any(m in body for m in ym(latest)))
            if not told:
                add('WARN', where, 'F4',
                    '근거 발행일이 %d일 벌어졌다(%s~%s) — %s 주제 기준 %d일을 넘는다. '
                    '어긋남인지 그사이 바뀐 것인지 본문에서 시차를 밝힌다'
                    % (spread, oldest, latest, section or '기본', limit))


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
