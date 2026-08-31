# -*- coding: utf-8 -*-
# 워치 줄 검사기. 설계는
# docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md.
#
# 규칙을 세울 때는 결함을 일부러 넣어 무는지 먼저 본다(CLAUDE.md). --selftest 가 그 자리다 —
# 규칙마다 걸려야 할 줄과 걸리면 안 되는 줄을 하나씩 넣고 실제로 그렇게 되는지 센다.
#
# 설계에서 바뀐 것 둘.
#  W1  설계는 「actor_alias.json 정본」이라고만 했는데 그 사전은 회사 사전이라 권역이 없다.
#      종목은 actor_alias 정본, 권역은 watch/_areas.json 으로 갈랐다.
#  W6  설계는 「트리거 src 가 실재하나」였다. 트리거 표를 네 열로 줄이면서 src 를 뺐고
#      (출처는 metric JSON 이 들고 온다), 대신 절 넷이 서 있는지를 본다.
import io, os, re, sys, json, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import watch_lib as wl
import notes_lib as nl

HERE = os.path.dirname(os.path.abspath(__file__))
ALIAS = os.path.join(HERE, 'actor_alias.json')
AREAS = os.path.join(wl.WATCH, '_areas.json')
NEED_SECS = ('지금 판단', '트리거', '왜 보나', '반대 근거')
STALE_DAYS = 90
NUM_RE = re.compile(r'\d')
# metric 열쇠 꼴. 소문자로 열고 밑줄·숫자·한글만. 한글을 여는 이유는 열쇠에 구 이름이
# 들어가기 때문이다(sale_idx_강남구) — 구마다 값을 따로 받아 평균을 안 내는 설계라
# 무엇을 재는 값인지가 열쇠에 남아야 한다. 빈칸과 문장부호는 계속 막는다.
KEY_RE = re.compile(r'^[a-z][a-z0-9_가-힣]*$')


def canon():
    """종목 정본 집합과 권역 정본 집합."""
    with io.open(ALIAS, encoding='utf-8') as f:
        d = json.load(f)
    eq = set(v for k, v in d.items() if not k.startswith('_'))
    with io.open(AREAS, encoding='utf-8') as f:
        ar = set(k for k in json.load(f) if not k.startswith('_'))
    return eq, ar


def check_one(path, today, eq, ar):
    out = []
    def bad(rule, msg, sev='FAIL'):
        out.append((sev, os.path.basename(path), rule, msg))

    with io.open(path, encoding='utf-8') as f:
        raw = f.read()
    meta, body = nl.parse_front(raw)
    sec = wl.sections(body)
    w = wl.load_one(path)

    # W1 — 대상이 사전 정본인가. 이름이 글마다 달라지면 한 대상이 둘로 갈라진다.
    if w['kind'] == 'equity':
        if w['target'] not in eq:
            bad('W1', '종목 대상 "%s" 가 actor_alias 정본이 아니다' % w['target'])
        if not w['ticker']:
            bad('W1', '종목 줄에 ticker 가 없다')
    elif w['kind'] == 'realestate':
        if w['target'] not in ar:
            bad('W1', '권역 대상 "%s" 가 watch/_areas.json 에 없다' % w['target'])
    else:
        bad('W1', 'kind 가 equity·realestate 가 아니다: "%s"' % w['kind'])

    if not w['triggers']:
        bad('W2', '트리거가 하나도 없다')
    for t in w['triggers']:
        if t['kind'] not in wl.KINDS:
            bad('W2', '트리거 "%s" 의 갈래가 값·사건이 아니다: "%s"' % (t['what'], t['kind']))
            continue
        # W2 — 값 트리거의 조건에 잴 수 있는 수가 있나. 「오르면」만 있으면 언제 걸린 건지 모른다.
        #      사건 트리거는 면제다 — 공표가 났나 안 났나로 갈린다.
        if t['kind'] == wl.KIND_VALUE and not NUM_RE.search(t['cond']):
            bad('W2', '값 트리거 "%s" 의 조건에 수가 없다: "%s"' % (t['what'], t['cond']))
        # W3 — 값 트리거에 metric 키가 있나, 사건 트리거에 키가 붙지 않았나
        if t['kind'] == wl.KIND_VALUE and not KEY_RE.match(t['metric'] or ''):
            bad('W3', '값 트리거 "%s" 의 metric 키가 없거나 꼴이 아니다: "%s"'
                % (t['what'], t['metric']))
        if t['kind'] == wl.KIND_EVENT and KEY_RE.match(t['metric'] or ''):
            bad('W3', '사건 트리거 "%s" 에 metric 키가 붙어 있다 — 어댑터가 채울 자리가 아니다'
                % t['what'])
        # W4 — 값이 들어온 줄에는 「언제 것 · 성격」이 있어야 한다. 표에서 공표치와
        #      추정치가 같은 무게로 읽히는 것을 막는 자리다(CLAUDE.md).
        if t['value'] is not None and not (t['as_of'] and t['nature']):
            bad('W4', '값이 든 트리거 "%s" 에 as_of·kind 가 없다' % t['what'])

    # W5 — 오래 안 본 줄. 워치는 안 보면 그냥 옛날 판단이 된다.
    try:
        d = (today - datetime.date.fromisoformat(w['checked'])).days
        if d > STALE_DAYS:
            bad('W5', '마지막 확인이 %d일 전이다 — 다시 보거나 줄을 닫는다' % d, 'WARN')
    except ValueError:
        bad('W5', 'checked 가 YYYY-MM-DD 가 아니다: "%s"' % w['checked'])

    # W6 — 절 넷이 서 있나. 하나라도 없으면 카드에 빈 자리가 생긴다.
    for s in NEED_SECS:
        if not sec.get(s):
            bad('W6', '절 「%s」 가 없거나 비어 있다' % s)
    if not w['why']:
        bad('W6', 'frontmatter 에 why 가 없다')

    # W7 — 본문이 가리키는 경로가 실재하나
    for m in re.finditer(r'`([\w./가-힣-]+/[\w./가-힣-]*)`', body):
        p = m.group(1)
        if not os.path.exists(os.path.join(os.path.dirname(HERE), p.rstrip('/'))):
            bad('W7', '본문이 가리키는 경로가 없다: %s' % p)
    return out


def main(paths=None, today=None):
    today = today or datetime.date.today()
    eq, ar = canon()
    paths = paths or [p for p in sorted(glob.glob(os.path.join(wl.WATCH, '*', '*.md')))
                      if os.path.basename(os.path.dirname(p)) != '_metrics']
    rows = []
    for p in paths:
        rows += check_one(p, today, eq, ar)
    for sev, f, rule, msg in rows:
        print('%s %s [%s] %s' % (sev, f, rule, msg))
    nf = sum(1 for r in rows if r[0] == 'FAIL')
    print('\n요약: 워치 %d줄 / FAIL %d / WARN %d' % (len(paths), nf, len(rows) - nf))
    return nf


# ── 결함을 넣어 무는지 본다 ────────────────────────────────────────────────
SEED = '''---
kind: equity
target: %(target)s
ticker: TST
topic: 시험
opened: 2026-08-31
checked: %(checked)s
why: 시험용
---

## 지금 판단

시험.

## 트리거

| 무엇을 | 갈래 | metric | 걸리는 조건 |
|---|---|---|---|
%(rows)s

## 왜 보나

- 시험.

## 반대 근거

- 시험 — 시험.
'''

CASES = [
    # (이름, 걸려야 할 규칙 또는 None, 바꿀 것)
    ('멀쩡한 줄', None, {}),
    ('대상이 사전에 없다', 'W1', {'target': '없는회사'}),
    ('값 조건에 수가 없다', 'W2', {'rows': '| 배수 | 값 | fwd_pe | 오르면 |'}),
    ('값 트리거에 metric 이 없다', 'W3', {'rows': '| 배수 | 값 | — | 30배 초과 |'}),
    ('사건에 metric 이 붙었다', 'W3', {'rows': '| 공표 | 사건 | fwd_pe | 공표 발생 |'}),
    ('열쇠 자리에 산문', 'W3', {'rows': '| 배수 | 값 | 선행 P/E 배수 | 30배 초과 |'}),
    ('열쇠에 한글은 통과', None, {'rows': '| 지수 | 값 | sale_idx_강남구 | 5% 하회 |'}),
    ('오래 안 봤다', 'W5', {'checked': '2020-01-01'}),
]


def selftest():
    import tempfile
    eq, ar = canon()
    today = datetime.date(2026, 8, 31)
    base = {'target': '엔비디아', 'checked': '2026-08-31',
            'rows': '| 배수 | 값 | fwd_pe | 30배 하회 |'}
    ok = True
    for name, want, patch in CASES:
        d = dict(base, **patch)
        tmp = os.path.join(tempfile.mkdtemp(), 'TST.md')
        io.open(tmp, 'w', encoding='utf-8', newline='\n').write(SEED % d)
        hits = {r[2] for r in check_one(tmp, today, eq, ar)}
        got = (want in hits) if want else (not hits)
        print('%s %-22s 기대 %-5s 잡힌 것 %s'
              % ('OK  ' if got else 'MISS', name, want or '없음', sorted(hits) or '없음'))
        ok &= got
    print('\n자체검사: %s' % ('통과' if ok else '실패'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--selftest' in sys.argv else (1 if main() else 0))
