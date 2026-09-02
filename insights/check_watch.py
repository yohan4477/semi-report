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
POLICIES = os.path.join(wl.WATCH, '_policies.json')
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
    """종목·권역·정책 정본 집합."""
    with io.open(ALIAS, encoding='utf-8') as f:
        d = json.load(f)
    eq = set(v for k, v in d.items() if not k.startswith('_'))
    with io.open(AREAS, encoding='utf-8') as f:
        ar = set(k for k in json.load(f) if not k.startswith('_'))
    with io.open(POLICIES, encoding='utf-8') as f:
        po = set(k for k in json.load(f) if not k.startswith('_'))
    return eq, ar, po


def check_one(path, today, eq, ar, po):
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
    elif w['kind'] == 'policy':
        if w['target'] not in po:
            bad('W1', '정책 대상 "%s" 가 watch/_policies.json 에 없다' % w['target'])
        # 정책은 값이 안 온다. 값 트리거를 걸면 영영 안 채워진다
        for t in w['triggers']:
            if t['kind'] == wl.KIND_VALUE:
                bad('W1', '정책 줄에 값 트리거 "%s" 가 있다 — 정책은 사건으로만 온다'
                    % t['what'])
    else:
        bad('W1', 'kind 가 equity·realestate·policy 가 아니다: "%s"' % w['kind'])

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

    # W12 — 정책 줄이 본 판과 지금 판이 같은가. 정책의 트리거는 결국 이 하나다 —
    #       조문을 견줄 필요 없이 시행일자로 정확히 갈린다.
    for tgt, name, seen in (w.get('laws') or []):
        if not seen:
            bad('W12', '%s 에 내가 본 시행일이 없다 — laws 에 =YYYY-MM-DD 로 적는다' % name)
            continue
        m = (w.get('metrics') or {}).get(wl.law_key(name))
        if not m:
            continue                       # 아직 안 받아 왔다. W9 자리가 아니다
        if str(m.get('value')) != seen:
            bad('W12', '%s 가 내가 본 판(%s) 뒤에 바뀌었다 — 지금 시행일 %s. '
                '바뀐 것을 읽고 laws 와 checked 를 갱신한다'
                % (name, seen, m.get('value')))

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

    # W14 — 「걸리면」·「확인처」가 비어 있나. 조건만 있고 행동이 없으면 워치가 아니라
    # 관측이다 — 걸렸을 때 무엇을 하는지가 줄에 적혀 있어야 독자가 그 자리에서 움직인다.
    # 2026-09-02 에 열 줄을 다 채우고 FAIL 로 올렸다(그전에는 WARN — 여섯 열로 늘어난
    # 직후라 옛 줄이 비어 있는 게 정상이었다). 값 트리거는 「걸리면」에 다음에 할 일을,
    # 사건 트리거는 「걸리면」과 「확인처」(사람이 열어 볼 URL)를 적는다.
    for t in w['triggers']:
        if t['kind'] == wl.KIND_VALUE and not (t.get('act') or '').strip():
            bad('W14', '값 트리거 "%s" 의 「걸리면」이 비어 있다 — 이 조건이 걸렸을 때 '
                '무엇을 할지(더 볼 것·손절선 등)를 적는다' % t['what'])
        if t['kind'] == wl.KIND_EVENT:
            if not (t.get('act') or '').strip():
                bad('W14', '사건 트리거 "%s" 의 「걸리면」이 비어 있다 — 이 사건이 나면 '
                    '무엇을 할지를 적는다' % t['what'])
            if not (t.get('where') or '').strip():
                bad('W14', '사건 트리거 "%s" 의 「확인처」가 비어 있다 — 사람이 열어 볼 '
                    'URL을 적는다' % t['what'])

    # W15 — 「## 이력」 표의 날짜가 YYYY-MM-DD 이고 그 순서(오래된 것 먼저)로 늘어서 있나.
    # 판단이 언제 바뀌었는지를 적어 두는 표라, 날짜가 뒤죽박죽이면 무엇이 먼저 있었던
    # 판단인지를 표 스스로 말하지 못한다.
    DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    prev_d = None
    for d, _what, _why in w.get('history') or []:
        if not DATE_RE.match(d or ''):
            bad('W15', '이력의 날짜가 YYYY-MM-DD 꼴이 아니다: "%s"' % d)
        elif prev_d is not None and d < prev_d:
            bad('W15', '이력의 날짜가 순서(오래된 것 먼저)가 아니다: "%s" 다음에 "%s"'
                % (prev_d, d))
        if DATE_RE.match(d or ''):
            prev_d = d
    return out


# W13 — _seen.json 의 열쇠가 지금 줄에 있나. 트리거 이름을 바꾸거나 지웠는데 스냅숏이
# 그 옛 이름을 그대로 들고 있으면, watch_mark.py 가 다음에 다시 찍기 전까지 「지난 확인
# 이후」 화면이 그 옛 이름을 향해 조용히 비교를 계속한다. main() 밖으로 뺀 것은
# --selftest 가 snap 을 직접 지어 넣어 볼 수 있어야 해서다 — main() 안에 있으면
# wl.load_seen() 을 몽키패치해야만 시험할 수 있다.
def stale_seen_rows(paths, snap):
    if not snap:
        return []
    cur_v, cur_l = set(), set()
    for p in paths:
        w = wl.load_one(p)
        for t in w['triggers']:
            if t['kind'] == wl.KIND_VALUE:
                cur_v.add('%s|%s' % (w['slug'], t['what']))
        for _tg, name, _s in (w.get('laws') or []):
            cur_l.add(name)
    out = []
    for k in (snap.get('value') or {}):
        if k not in cur_v:
            out.append(('WARN', '_seen.json', 'W13',
                        '값 열쇠 "%s" 가 지금 어느 줄에도 없다 — 트리거 이름을 바꿨거나 '
                        '지웠는데 스냅숏이 낡았다' % k))
    for k in (snap.get('laws') or {}):
        if k not in cur_l:
            out.append(('WARN', '_seen.json', 'W13',
                        '법 이름 "%s" 가 지금 어느 줄의 laws 에도 없다 — 스냅숏이 낡았다'
                        % k))
    return out


def main(paths=None, today=None):
    today = today or datetime.date.today()
    eq, ar, po = canon()
    paths = paths or [p for p in sorted(glob.glob(os.path.join(wl.WATCH, '*', '*.md')))
                      if os.path.basename(os.path.dirname(p)) != '_metrics']
    rows = []
    for p in paths:
        rows += check_one(p, today, eq, ar, po)
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

    rows += stale_seen_rows(paths, wl.load_seen())

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
laws: %(laws)s
why: 시험용
---

## 지금 판단

시험. %(extra)s

## 트리거

| 무엇을 | 갈래 | metric | 걸리는 조건 | 걸리면 | 확인처 |
|---|---|---|---|---|---|
%(rows)s

## 왜 보나

- 시험.

## 반대 근거

- 시험 — 시험.
%(hist)s'''

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
    ('정책 대상이 사전에 없다', 'W1', {'kind': 'policy', 'target': '없는정책'}, None),
    ('정책에 값 트리거', 'W1',
     {'kind': 'policy', 'target': '대출 규제', 'ticker': '',
      'rows': '| 배수 | 값 | fwd_pe | 5 초과 |'}, None),
    ('본 판과 지금 판이 다르다', 'W12',
     {'kind': 'policy', 'target': '대출 규제', 'ticker': '', 'rows': '',
      'laws': 'admrul:은행업감독규정=1999-01-01'},
     {'law_은행업감독규정': {'value': '2026-04-01', 'as_of': '2026-04-01',
                       'kind': '공표', 'unit': '시행일', 'series': []}}),
    ('본 판을 안 적었다', 'W12',
     {'kind': 'policy', 'target': '대출 규제', 'ticker': '', 'rows': '',
      'laws': 'admrul:은행업감독규정'}, None),
    # 반전·속도 — 「경신」이 추세를 타서 절반이 걸리던 것을 대신한 꼴이다.
    # 늘 걸리는 값(내내 오르내림)과 한 번도 안 걸리는 값(내내 한 방향)을 넣어 본다
    ('반전이 내내 걸린다', 'W8',
     {'rows': '| 배수 | 값 | fwd_pe | 최근 1개월 흐름이 뒤집히고 0.1%p 이상 |'},
     {'fwd_pe': _M([10, 11, 10, 11, 10, 11, 10, 11])}),
    ('속도가 한 번도 안 걸린다', None,
     {'rows': '| 배수 | 값 | fwd_pe | 최근 3개월 변화가 그 앞의 9배 이상 |'},
     {'fwd_pe': _M([10, 11, 12, 13, 14, 15, 16, 17])}),
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
    # 이력 표 — 날짜 꼴과 순서(W15). 정상 표는 안 걸리고, 꼴이 틀리거나
    # 거꾸로 서면 걸린다
    ('이력 날짜가 정상', None,
     {'hist': '\n## 이력\n\n| 날짜 | 무엇을 | 왜 |\n|---|---|---|\n'
              '| 2026-01-01 | 처음 판단 | 시험 |\n| 2026-06-01 | 판단을 바꿈 | 시험 |\n'}, None),
    ('이력 날짜 꼴이 아니다', 'W15',
     {'hist': '\n## 이력\n\n| 날짜 | 무엇을 | 왜 |\n|---|---|---|\n'
              '| 2026/01/01 | 처음 판단 | 시험 |\n'}, None),
    ('이력 날짜가 거꾸로 섰다', 'W15',
     {'hist': '\n## 이력\n\n| 날짜 | 무엇을 | 왜 |\n|---|---|---|\n'
              '| 2026-06-01 | 나중 판단 | 시험 |\n| 2026-01-01 | 처음 판단 | 시험 |\n'}, None),
]


def _seed(d):
    """시험 줄을 만든다. CASES 의 줄은 옛 네 열로 적혀 있다 — 표가 여섯 열이 된 뒤에도
    케이스를 전부 고쳐 쓰지 않으려고 여기서 「걸리면」·「확인처」를 채운다. W14 를
    시험하는 자리는 여섯 열을 직접 적으므로 그 줄은 손대지 않는다."""
    out = []
    for ln in d['rows'].splitlines():
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if len(cells) == 4:
            act, where = ('시험한다', 'https://www.law.go.kr' if cells[1] == '사건' else '')
            ln = '| %s | %s | %s |' % (' | '.join(cells), act, where)
        out.append(ln)
    return SEED % dict(d, rows=chr(10).join(out))


def selftest():
    """결함을 일부러 넣어 무는지 본다. 규칙을 세울 때 이것부터 한다 —
    안 물면 규칙이 아니라 장식이다."""
    import tempfile, shutil
    eq, ar, po = canon()
    today = datetime.date(2026, 8, 31)
    base = {'target': '엔비디아', 'ticker': 'TST', 'checked': '2026-08-31',
            'rows': '| 배수 | 값 | fwd_pe | 30배 하회 |', 'kind': 'equity',
            'extra': '', 'drop_sec': '', 'laws': '', 'hist': ''}
    real_metrics = wl.METRICS
    ok = True
    for name, want, patch, mets in CASES:
        d = dict(base, **patch)
        root = tempfile.mkdtemp()
        tmp = os.path.join(root, 'TST.md')
        text = _seed(d)
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
            rows = check_one(tmp, today, eq, ar, po)
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
                newline='\n').write(_seed(base))
    wl.METRICS = os.path.join(root, '_none')
    try:
        rows = []
        for nm in ('A.md', 'B.md'):
            rows += check_one(os.path.join(root, nm), today, eq, ar, po)
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

    # W13 — main() 에서 뺀 stale_seen_rows() 를 직접 부른다. snap 을 몽키패치 없이
    # 지어 넣을 수 있어야 「값 열쇠가 지금 줄에 없다」와 「있다」 둘 다 확실히 잰다.
    root = tempfile.mkdtemp()
    tmp = os.path.join(root, 'TST.md')
    io.open(tmp, 'w', encoding='utf-8', newline='\n').write(_seed(base))
    live_key = 'TST|배수'          # SEED 의 기본 rows 가 거는 트리거 이름
    stale = stale_seen_rows([tmp], {'value': {'없는열쇠|없음': '걸림'}, 'laws': {}})
    fresh = stale_seen_rows([tmp], {'value': {live_key: '걸림'}, 'laws': {}})
    none_ = stale_seen_rows([tmp], None)
    shutil.rmtree(root, ignore_errors=True)
    ok13 = (any(r[2] == 'W13' for r in stale) and not any(r[2] == 'W13' for r in fresh)
            and not none_)
    print('%s %-24s 기대 W13   잡힌 것 stale=%s · fresh=%s · seen없음=%s'
          % ('OK  ' if ok13 else 'MISS', '_seen.json 낡은 열쇠',
             sorted(r[2] for r in stale), sorted(r[2] for r in fresh), none_))
    ok &= ok13

    # W14 — 「걸리면」·「확인처」를 채우면 사라지고 비면 걸리는지 두 파일로 견준다.
    # CASES 는 전부 옛 네 열 표를 쓰므로(빈 걸리면) W14 가 늘 걸린다 — 그것만으로는
    # 「채우면 사라진다」쪽을 못 본다
    root = tempfile.mkdtemp()
    filled = dict(base, rows='| 배수 | 값 | fwd_pe | 30배 하회 | 재평가한다 |  |')
    empty6 = dict(base, rows='| 배수 | 값 | fwd_pe | 30배 하회 |  |  |')
    evt_empty = dict(base, rows='| 공표 | 사건 | — | 공표되면 |  |  |')
    for nm, d in (('filled.md', filled), ('empty6.md', empty6), ('evt.md', evt_empty)):
        io.open(os.path.join(root, nm), 'w', encoding='utf-8', newline='\n').write(_seed(d))
    wl.METRICS = os.path.join(root, '_none')
    try:
        f_hits = {r[2] for r in check_one(os.path.join(root, 'filled.md'), today, eq, ar, po)}
        e_hits = {r[2] for r in check_one(os.path.join(root, 'empty6.md'), today, eq, ar, po)}
        v_hits = {r[2] for r in check_one(os.path.join(root, 'evt.md'), today, eq, ar, po)}
    finally:
        wl.METRICS = real_metrics
        shutil.rmtree(root, ignore_errors=True)
    ok14 = 'W14' not in f_hits and 'W14' in e_hits and 'W14' in v_hits
    print('%s %-24s 기대 W14  채우면=%s · 값 빈칸=%s · 사건 빈칸=%s'
          % ('OK  ' if ok14 else 'MISS', '걸리면·확인처',
             sorted(f_hits), sorted(e_hits), sorted(v_hits)))
    ok &= ok14

    print('\n자체검사: %s' % ('통과' if ok else '실패'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(selftest() if '--selftest' in sys.argv else (1 if main() else 0))
