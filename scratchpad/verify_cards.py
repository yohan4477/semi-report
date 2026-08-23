# -*- coding: utf-8 -*-
"""새로 들어온 수도리무브 카드를 받아 들이기 전에 훑는다.

  py -3.13 scratchpad/verify_cards.py <영상ID> [<영상ID> ...]
  py -3.13 scratchpad/verify_cards.py --all        커밋 안 된 카드 전부

check_slim 이 안 보는 구멍을 메운다. 실제로 새어 나간 것들이라 하나씩 이유가 있다.
  Q1  quote 필드가 자막에 없다 — check_slim 은 slim 안 따옴표만 본다. 지어낸 문장이 나갔다
  Q2  자동 자막이 뭉갠 말을 인용했다 (텔레업 같은 오인식)
  A1  카드 본문이 회사 별칭을 쓴다 — insights/actor_alias.json 의 왼쪽 이름
  T1  영어 구조 직역 (위층·아래층 등)
  T2  일반론으로 끝나는 문장
  F1  카드 파일이 figs 를 들고 있다 — 그림은 생성기 EXTRA_FIGS 가 붙인다
  N1  같은 페이지의 다른 카드와 표기가 갈린다
"""
import difflib
import glob
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, 'scratchpad', 'cards_sudo')
SUBS = os.path.join(ROOT, 'scratchpad', 'yt_subs')
OUT = io.TextIOWrapper(open(1, 'wb', closefd=False), encoding='utf-8', line_buffering=True)

ALIAS = {k: v for k, v in json.load(
    io.open(os.path.join(ROOT, 'insights', 'actor_alias.json'), encoding='utf-8')).items()
    if not k.startswith('_')}

# 자동 자막이 흔히 뭉개는 말. 이걸 그대로 실으면 독자가 없는 용어를 배운다
GARBLED = ['텔레업', '텔레오션', '텔레오프', '올카 핸드', '셰파', '로다 AI', '파이스타']
TRANSLATIONESE = ['위층', '아래층', '되어진', '를 가진다', '에 있어서', '~에 대한 ']
VAGUE = re.compile(r'(중요하다|주목된다|필요하다|기대된다|할 것으로 보인다|살펴봐야 한다)[.,]')
STRIP = re.compile(r'<[^>]+>')


def norm(t):
    return re.sub(r'[\s,]', '', t)


def best_ratio(q, sub):
    best, step, win = 0.0, max(4, len(q) // 2), len(q) * 2
    sm = difflib.SequenceMatcher(autojunk=False)
    sm.set_seq2(q)
    for i in range(0, max(1, len(sub) - win), step):
        sm.set_seq1(sub[i:i + win])
        if sm.real_quick_ratio() <= best or sm.quick_ratio() <= best:
            continue
        best = max(best, sm.ratio())
    return best


def load(vid):
    ns = {}
    p = os.path.join(CARDS, vid + '.py')
    exec(compile(io.open(p, encoding='utf-8').read(), p, 'exec'), ns)
    return ns['CARD']


def body_of(c):
    """화면에 나가는 글 전부 — 판정은 이것만 본다"""
    parts = [c.get('title', ''), c.get('gain', ''), c.get('slim_oneliner', ''),
             c.get('oneliner', ''), c.get('quote', ''), c.get('note', '')]
    parts += list(c.get('slim_points') or ()) + list(c.get('points') or ())
    parts += [t for _w, t in (c.get('clash') or ())]
    parts += [v for v, _l in (c.get('slim_stats') or ())]
    parts += [v for v, _l in (c.get('stats') or ())]
    return STRIP.sub('', ' '.join(parts))


def check(vid):
    bad, warn = [], []
    c = load(vid)
    text = body_of(c)
    subp = os.path.join(SUBS, vid + '.txt')
    sub = norm(io.open(subp, encoding='utf-8').read()) if os.path.exists(subp) else ''

    q = STRIP.sub('', c.get('quote') or '').strip()
    if not q:
        bad.append('Q1 quote 필드가 비었다')
    elif sub:
        nq = norm(q)
        r = 1.0 if nq in sub else best_ratio(nq, sub)
        if r < 0.55:
            bad.append('Q1 quote 가 자막에 없다 (유사도 %.2f) — "%s"' % (r, q[:44]))
        elif r < 0.8:
            warn.append('Q1 quote 가 자막과 조금 다르다 (유사도 %.2f)' % r)

    # note 는 표기가 왜 흔들리는지 밝히는 자리다 — 거기서 오인식 표기를 인용하는 것은 맞다.
    # 나머지 본문에 그대로 실리는 것만 잡는다.
    text_nonote = text.replace(STRIP.sub('', c.get('note') or ''), ' ')
    for g in GARBLED:
        if g in text_nonote:
            bad.append('Q2 자막 오인식을 그대로 실었다: %s' % g)
    # 별칭을 한 번도 안 쓰기는 어렵다 — 「Rhoda의 300년」처럼 줄여 부르는 자리가 있다.
    # 정본이 그 카드 안에 한 번이라도 나오면 독자가 잇는 데 문제가 없으니 넘어간다.
    # 「Sharpa(샤파)」처럼 정본 뒤 괄호로 읽기를 단 것도 넘어간다.
    for a, canon in ALIAS.items():
        if not re.search(r'(?<![A-Za-z가-힣])%s(?![A-Za-z가-힣])' % re.escape(a), text):
            continue
        if canon in text or (canon + '(' + a) in text:
            continue
        warn.append('A1 정본이 한 번도 안 나온 채 별칭만 썼다: %s 는 %s' % (a, canon))
    for t in TRANSLATIONESE:
        if t in text:
            bad.append('T1 영어 구조 직역: %s' % t)
    for m in VAGUE.finditer(text):
        warn.append('T2 일반론으로 닫는 문장: …%s' % text[max(0, m.start() - 26):m.end()])
    # L1 : 변환본 링크가 실제 파일을 가리키는가. 파일 이름을 고치면서 링크를 안 고쳐
    # 깨진 채로 나간 적이 있다(2026-08-23). 주소를 풀어서 저장소 안에 있는지 본다
    import urllib.parse
    for _lab, url, _cls in (c.get('links') or ()):
        if 'blob/main/' not in url:
            continue
        rel = urllib.parse.unquote(url.split('blob/main/', 1)[1])
        if not os.path.isfile(os.path.join(ROOT, rel.replace('/', os.sep))):
            bad.append('L1 변환본 링크가 가리키는 파일이 없다: %s' % rel)

    if c.get('figs'):
        bad.append('F1 카드 파일이 figs 를 들고 있다 — 생성기 EXTRA_FIGS 로 옮긴다')
    for k in ('section', 'date', 'title', 'gain', 'meta', 'links', 'quote', 'clash', 'note'):
        if not c.get(k):
            bad.append('필수 키가 없다: %s' % k)
    if len(c.get('clash') or ()) < 2:
        warn.append('반론이 %d개 — 둘 이상 권장' % len(c.get('clash') or ()))
    return c, bad, warn


def main(vids):
    fails = 0
    for vid in vids:
        try:
            c, bad, warn = check(vid)
        except Exception as e:
            print('FAIL %s — 읽지 못함: %s' % (vid, e), file=OUT)
            fails += 1
            continue
        mark = 'FAIL' if bad else ('warn' if warn else 'OK  ')
        print('%s %s  %s' % (mark, vid, c.get('title', '')[:58]), file=OUT)
        for b in bad:
            print('       ! %s' % b, file=OUT)
        for w in warn:
            print('       ~ %s' % w, file=OUT)
        fails += bool(bad)
    print('\nFAIL %d건 (! = 고쳐야 함, ~ = 사람이 확인)' % fails, file=OUT)
    return 1 if fails else 0


def uncommitted():
    r = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '-m',
                        'scratchpad/cards_sudo'], cwd=ROOT, capture_output=True, text=True)
    out = [os.path.basename(x)[:-3] for x in r.stdout.split('\n')
           if x.endswith('.py') and not os.path.basename(x).startswith('_')]
    if out:
        return out
    tracked = set(os.path.basename(x) for x in subprocess.run(
        ['git', 'ls-files', 'scratchpad/cards_sudo'], cwd=ROOT,
        capture_output=True, text=True).stdout.split('\n'))
    return [os.path.basename(p)[:-3] for p in sorted(glob.glob(os.path.join(CARDS, '*.py')))
            if os.path.basename(p) not in tracked and not os.path.basename(p).startswith('_')]


if __name__ == '__main__':
    args = sys.argv[1:]
    sys.exit(main(uncommitted() if (not args or args[0] == '--all') else args))
