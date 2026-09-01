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
# 늘 걸려 있는 조건은 정의상 신호가 아니다 — FAIL.
# 한 번도 안 걸린 것은 다르다. 아직 안 일어난 일을 기다리는 것이 워치리스트다.
# 대신 「가장 가까웠을 때 얼마나 멀었나」를 재서, 이력 변동폭만큼 떨어진 적도 없으면
# 그건 닿을 수 없는 문턱이라 FAIL 로 올린다.
# 그 사이의 잦기는 무엇이 적당한지가 사람 판단이라 수만 적어 WARN 으로 낸다.
BUSY, RARE, FAR = 0.40, 0.05, 1.0
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

    # W8 — 이 조건이 이력에서 몇 번 걸렸나. 0회면 영영 안 켜지고 전부면 늘 켜져 있다 —
    #      둘 다 「무엇이 일어나면 판단이 바뀌나」에 답하지 못한다.
    for t in w['triggers']:
        if t['kind'] != wl.KIND_VALUE:
            continue
        n, tot, _now = wl.backtest(t['cond'], t['series'])
        # 단위 낱말은 조건에 적힌 것을 되쓴다 — 「개월」로 박으면 연·분기 시계열에서
        # 메시지가 거짓말을 한다(종목 줄에서 「5개월 이력」이 나왔다)
        _um = re.search(r'최근\s*\d+\s*(개월|달|년|분기)', t['cond'] or '')
        U = _um.group(1) if _um else '점'
        if n is None:
            if t['series']:
                bad('W8', '트리거 "%s" 의 조건을 기계가 못 읽는다: "%s" — 사람만 판정할 수 '
                    '있으면 갈래를 사건으로 두거나 읽는 꼴로 적는다' % (t['what'], t['cond']),
                    'WARN')
            continue
        if n == 0:
            d = wl.nearest(t['cond'], t['series'])
            if d is not None and d > FAR:
                bad('W8', '트리거 "%s" 가 %d%s 내내 안 걸렸고 가장 가까웠을 때도 이력 '
                    '변동폭의 %.1f배만큼 멀었다 — 닿을 수 없는 문턱이다: "%s"'
                    % (t['what'], tot, U, d, t['cond']))
            else:
                bad('W8', '트리거 "%s" 가 %d%s 이력에서 한 번도 안 걸렸다%s: "%s"'
                    % (t['what'], tot, U,
                       '' if d is None else ' (가장 가까웠을 때 변동폭의 %.2f배)' % d,
                       t['cond']), 'WARN')
        elif n == tot:
            bad('W8', '트리거 "%s" 가 %d%s 내내 걸려 있었다: "%s"'
                % (t['what'], tot, U, t['cond']))
        elif tot and not (RARE <= n / float(tot) <= BUSY):
            bad('W8', '트리거 "%s" 가 %d%s 중 %d번(%.0f%%) 걸렸다 — 잦기가 이래도 되나: "%s"'
                % (t['what'], tot, U, n, 100.0 * n / tot, t['cond']), 'WARN')

    # W9 — 값 트리거가 건 열쇠를 어댑터가 실제로 내나. 오타와 「원천이 아직 없다」가
    #      화면에서 똑같이 「자리표시」로 보여 구분이 안 됐다. metrics 파일이 있을 때만 본다
    mp = os.path.join(wl.METRICS, w['kind'], w['slug'] + '.json')
    if os.path.exists(mp):
        with io.open(mp, encoding='utf-8') as f:
            have = set(json.load(f))
        for t in w['triggers']:
            if t['kind'] == wl.KIND_VALUE and t['metric'] not in have:
                bad('W9', '값 트리거 "%s" 의 열쇠 %s 를 어댑터가 내지 않는다 — '
                    '영영 안 채워진다' % (t['what'], t['metric']))

        # W10 — 어댑터 산출물 검사. 지금까지 아무도 이 파일을 안 봤다
        with io.open(mp, encoding='utf-8') as f:
            mets = json.load(f)
        asofs = set()
        for k, m in mets.items():
            ser = m.get('series') or []
            if not ser:
                continue
            ts = [x[0] for x in ser]
            if ts != sorted(ts):
                bad('W10', '%s 의 series 가 때 순서가 아니다' % k)
            if len(set(ts)) != len(ts):
                bad('W10', '%s 의 series 에 같은 달이 두 번 있다' % k)
            # watch_lib 머리 주석이 「지금 값은 시계열의 마지막 점」을 근거로 삼는데
            # 그걸 강제하는 데가 없었다
            if [m.get('as_of'), m.get('value')] != list(ser[-1]):
                bad('W10', '%s 의 지금 값이 series 마지막 점과 다르다: %s vs %s'
                    % (k, (m.get('as_of'), m.get('value')), tuple(ser[-1])))
            if m.get('as_of'):
                asofs.add(m['as_of'])
        if len(asofs) > 2:
            bad('W10', 'metric 들의 as_of 가 %d가지로 갈렸다(%s) — 한 판에 서로 다른 달이 '
                '섞인다' % (len(asofs), ' · '.join(sorted(asofs))), 'WARN')

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
    # W11 — 제목이 겹치면 카드 앵커가 같아져 섹션 링크가 첫 카드로만 간다
    seen = {}
    for p in paths:
        w = wl.load_one(p)
        key = (w['kind'], w['target'], w.get('view', ''))
        if key in seen:
            rows.append(('FAIL', os.path.basename(p), 'W11',
                         '(갈래·대상·관점)이 %s 와 겹친다 — 카드 제목과 앵커가 같아진다'
                         % seen[key]))
        seen[key] = os.path.basename(p)
    for sev, f, rule, msg in rows:
        print('%s %s [%s] %s' % (sev, f, rule, msg))
    nf = sum(1 for r in rows if r[0] == 'FAIL')
    print('\n요약: 워치 %d줄 / FAIL %d / WARN %d' % (len(paths), nf, len(rows) - nf))
    return nf


# ── 결함을 넣어 무는지 본다 ────────────────────────────────────────────────
SEED = '''---
kind: %(kind)s
target: %(target)s
ticker: %(ticker)s
topic: 시험
opened: 2026-08-31
checked: %(checked)s
why: 시험용
---

## 지금 판단

시험. %(extra)s

## 트리거

| 무엇을 | 갈래 | metric | 걸리는 조건 |
|---|---|---|---|
%(rows)s

## 왜 보나

- 시험.

## 반대 근거

- 시험 — 시험.
'''

def _M(vals, start=1):
    """시험용 metric — 값 목록에서 series·value·as_of 를 한꺼번에 만든다."""
    ser = [['2026-%02d' % (start + i), v] for i, v in enumerate(vals)]
    return {'value': ser[-1][1], 'as_of': ser[-1][0], 'kind': '공표',
            'unit': '배', 'src': '시험', 'series': ser}


CASES = [
    # (이름, 걸려야 할 규칙 또는 None, .md 를 바꿀 것, metrics JSON)
    ('멀쩡한 줄', None, {}, None),
    ('대상이 사전에 없다', 'W1', {'target': '없는회사'}, None),
    ('ticker 가 없다', 'W1', {'ticker': ''}, None),
    ('갈래가 엉뚱하다', 'W1', {'kind': 'bogus'}, None),
    ('값 조건에 수가 없다', 'W2', {'rows': '| 배수 | 값 | fwd_pe | 오르면 |'}, None),
    ('트리거가 하나도 없다', 'W2', {'rows': ''}, None),
    ('값 트리거에 metric 이 없다', 'W3', {'rows': '| 배수 | 값 | — | 30배 초과 |'}, None),
    ('사건에 metric 이 붙었다', 'W3', {'rows': '| 공표 | 사건 | fwd_pe | 공표 발생 |'}, None),
    ('열쇠 자리에 산문', 'W3', {'rows': '| 배수 | 값 | 선행 P/E 배수 | 30배 초과 |'}, None),
    ('열쇠에 한글은 통과', None, {'rows': '| 지수 | 값 | sale_idx_강남구 | 5% 하회 |'}, None),
    ('값에 as_of 가 없다', 'W4',
     {}, {'fwd_pe': {'value': 20, 'series': [['2026-06', 19], ['2026-07', 20]]}}),
    ('오래 안 봤다', 'W5', {'checked': '2020-01-01'}, None),
    ('절이 하나 없다', 'W6', {'drop_sec': '반대 근거'}, None),
    ('없는 경로를 가리킨다', 'W7', {'extra': '`insights/없는폴더/x.md` 를 본다.'}, None),
    ('늘 걸려 있는 조건', 'W8', {'rows': '| 배수 | 값 | fwd_pe | 1 초과 |'},
     {'fwd_pe': _M([10, 11, 12, 13])}),
    ('닿을 수 없는 문턱', 'W8', {'rows': '| 배수 | 값 | fwd_pe | 9999 상향 돌파 |'},
     {'fwd_pe': _M([10, 11, 12, 13])}),
    ('아직 안 걸린 것은 통과', None, {'rows': '| 배수 | 값 | fwd_pe | 14 상향 돌파 |'},
     {'fwd_pe': _M([10, 11, 12, 13])}),
    ('어댑터가 안 내는 열쇠', 'W9', {'rows': '| 배수 | 값 | 없는열쇠 | 5 초과 |'},
     {'fwd_pe': _M([10, 11, 12, 13])}),
    ('지금 값이 마지막 점과 다르다', 'W10', {'rows': '| 배수 | 값 | fwd_pe | 5 초과 |'},
     {'fwd_pe': dict(_M([10, 11, 12, 13]), value=99)}),
    ('series 가 때 순서가 아니다', 'W10', {'rows': '| 배수 | 값 | fwd_pe | 5 초과 |'},
     {'fwd_pe': {'value': 10, 'as_of': '2026-01', 'kind': '공표',
                 'series': [['2026-04', 13], ['2026-01', 10]]}}),
]


def selftest():
    """결함을 일부러 넣어 무는지 본다. 규칙을 세울 때 이것부터 한다 —
    안 물면 규칙이 아니라 장식이다."""
    import tempfile, shutil
    eq, ar = canon()
    today = datetime.date(2026, 8, 31)
    base = {'target': '엔비디아', 'ticker': 'TST', 'checked': '2026-08-31',
            'rows': '| 배수 | 값 | fwd_pe | 30배 하회 |', 'kind': 'equity',
            'extra': '', 'drop_sec': ''}
    real_metrics = wl.METRICS
    ok = True
    for name, want, patch, mets in CASES:
        d = dict(base, **patch)
        root = tempfile.mkdtemp()
        tmp = os.path.join(root, 'TST.md')
        text = SEED % d
        if d['drop_sec']:
            i = text.index('## ' + d['drop_sec'])
            j = text.find('\n## ', i + 1)
            text = text[:i] + (text[j:] if j > 0 else '')
        io.open(tmp, 'w', encoding='utf-8', newline='\n').write(text)
        if mets is not None:
            md = os.path.join(root, '_m', d['kind'])
            os.makedirs(md)
            io.open(os.path.join(md, 'TST.json'), 'w', encoding='utf-8',
                    newline='\n').write(json.dumps(mets, ensure_ascii=False))
            wl.METRICS = os.path.join(root, '_m')
        else:
            wl.METRICS = os.path.join(root, '_none')
        try:
            rows = check_one(tmp, today, eq, ar)
            hits = {r[2] for r in rows}
            fails = {r[2] for r in rows if r[0] == 'FAIL'}
        finally:
            wl.METRICS = real_metrics
            shutil.rmtree(root, ignore_errors=True)
        # 걸려야 할 규칙은 등급을 안 가리고 본다(W5·W8 은 WARN 으로 나는 것이 있다).
        # 「걸리면 안 되는 줄」은 FAIL 만 본다 — 잦기 WARN 까지 막으면 시험이 못 돈다
        got = (want in hits) if want else (not fails)
        print('%s %-24s 기대 %-5s 잡힌 것 %s'
              % ('OK  ' if got else 'MISS', name, want or '없음', sorted(hits) or '없음'))
        ok &= got

    # W11 은 파일 하나로는 못 본다 — 두 줄을 놓고 main() 을 돌린다
    root = tempfile.mkdtemp()
    for nm in ('A.md', 'B.md'):
        io.open(os.path.join(root, nm), 'w', encoding='utf-8',
                newline='\n').write(SEED % base)
    wl.METRICS = os.path.join(root, '_none')
    try:
        rows = []
        for nm in ('A.md', 'B.md'):
            rows += check_one(os.path.join(root, nm), today, eq, ar)
        seen, dup = {}, False
        for nm in ('A.md', 'B.md'):
            w = wl.load_one(os.path.join(root, nm))
            k = (w['kind'], w['target'], w.get('view', ''))
            if k in seen:
                dup = True
            seen[k] = nm
    finally:
        wl.METRICS = real_metrics
        shutil.rmtree(root, ignore_errors=True)
    print('%s %-24s 기대 W11   잡힌 것 %s'
          % ('OK  ' if dup else 'MISS', '대상·관점이 겹친다', 'W11' if dup else '없음'))
    ok &= dup

    print('\n자체검사: %s' % ('통과' if ok else '실패'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--selftest' in sys.argv else (1 if main() else 0))
