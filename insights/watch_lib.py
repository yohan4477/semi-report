# -*- coding: utf-8 -*-
# 워치 줄을 읽어 카드 재료로 바꾼다. 설계는
# docs/superpowers/specs/2026-08-31-포트폴리오-워치-대시보드-design.md.
#
# 판단은 insights/watch/<kind>/<슬러그>.md 에 사람이 쓰고, 수치는
# insights/watch/_metrics/<kind>/<슬러그>.json 에 어댑터가 덮어쓴다. 두 파일을 여기서 합친다.
# 한 파일에 섞지 않는 이유 — 스크립트가 사람 글을 날리거나 사람이 수치를 손으로 고친다.
#
# 어댑터 계약 (metric 하나가 주는 것):
#   {"value": …, "as_of": "2026-07", "kind": "공표|추정", "src": …,
#    "unit": "지수(2021.6=100)", "series": [["2024-01", 98.2], …]}
# series 는 트렌드 도해가 읽는 자리다. 설계에는 없었고 「권역별 가격 트렌드」를 넣으려다
# 나왔다 — 한 시점 값만으로는 선을 못 그린다. 따로 빼지 않고 같은 파일에 둔 이유는
# 「지금 값」이 시계열의 마지막 점이라야 둘이 어긋나지 않기 때문이다.
#
# 트리거는 frontmatter 가 아니라 본문 표에 있다. notes_lib.parse_front 가 평평한
# key:value 만 읽기도 하고, 파일을 열었을 때 카드와 같은 꼴로 읽히는 편이 낫기도 하다.
import io, os, re, json, glob
import notes_lib as nl

HERE = os.path.dirname(os.path.abspath(__file__))
WATCH = os.path.join(HERE, 'watch')
METRICS = os.path.join(WATCH, '_metrics')

# 트리거 갈래 둘. 값은 어댑터가 채우고, 사건은 사람이 checked 를 갱신할 때만 움직인다.
# 설계에는 값 하나뿐이었는데 삼성전자 줄(HBM 공급 계약 공표)이 안 맞아 여기서 갈랐다.
KIND_VALUE, KIND_EVENT = '값', '사건'
KINDS = (KIND_VALUE, KIND_EVENT)

SEC_RE = re.compile(r'^##\s+(.+?)\s*$', re.M)


def sections(body):
    """본문을 ## 제목으로 가른다. {제목: 그 아래 글}."""
    hits = list(SEC_RE.finditer(body))
    out = {}
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        out[m.group(1)] = body[m.end():end].strip()
    return out


def table_rows(block):
    """마크다운 표에서 몸통 줄만. 머리와 구분선은 버린다."""
    rows = []
    for ln in block.splitlines():
        ln = ln.strip()
        if not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip('|').split('|')]
        if not cells or set(''.join(cells)) <= set('-: '):
            continue          # 구분선
        rows.append(cells)
    if not rows:
        return []
    # 첫 줄을 무조건 버리면 머리 없는 표에서 첫 트리거가 조용히 사라진다.
    # 머리로 보이는 줄일 때만 버린다.
    return rows[1:] if rows[0][:2] == ['무엇을', '갈래'] else rows


def bullets(block):
    """- 로 시작하는 줄만. 이어지는 줄은 들여썼을 때만 앞 항목에 붙인다 —
    그냥 「비지 않은 줄」로 두면 목록 뒤 마무리 문단이 마지막 불릿에 삼켜진다."""
    out, open_item = [], False
    for ln in block.splitlines():
        t = ln.strip()
        if t.startswith('- ') and not ln.startswith((' ', '	')):
            out.append(t[2:].strip()); open_item = True
        elif not t:
            open_item = False
        elif open_item and ln.startswith((' ', '	')):
            out[-1] += ' ' + t
    return out


def esc(s):
    """HTML 로 나가기 전에 막는다. 워치의 「걸리는 조건」은 본성상 부등호를 쓰고 싶은
    자리라(「< 100」) 안 막으면 그 뒤가 태그로 먹혀 칸이 통째로 깨진다."""
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def md_inline(s):
    """**굵게** 와 `코드` 만 마크업으로. 본문 전체를 마크다운으로 굴리지 않는다 —
    카드가 받는 것은 이미 HTML 이고, 여기서 바꿀 것은 이 둘뿐이다.
    탈출을 먼저 걸고 그 위에 이 둘을 푼다."""
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    return re.sub(r'`(.+?)`', r'<code>\1</code>', s)


def metrics_of(kind, slug):
    p = os.path.join(METRICS, kind, slug + '.json')
    if not os.path.exists(p):
        return {}
    with io.open(p, encoding='utf-8') as f:
        return json.load(f)


def _pick(vals, trigger_keys, context):
    """이 줄이 쓸 metric 만 고른다. 트리거가 건 열쇠와 context 앞머리에 걸리는 것.

    앞머리로 받는 이유는 구마다 열쇠가 갈리기 때문이다 — context 에 jeonse_idx 하나만
    적으면 jeonse_idx_강남구·서초구·송파구가 다 딸려 온다."""
    pre = [x.strip() for x in (context or '').replace(',', ' ').split() if x.strip()]
    keys = set(k for k in trigger_keys if k)
    out = {}
    for k, v in (vals or {}).items():
        if k in keys or any(k == p or k.startswith(p + '_') for p in pre):
            out[k] = v
    return out


def load_one(path):
    with io.open(path, encoding='utf-8') as f:
        meta, body = nl.parse_front(f.read())
    slug = os.path.basename(path).rsplit('.md', 1)[0]
    kind = meta.get('kind', '')
    sec = sections(body)
    vals = metrics_of(kind, slug)

    trg = []
    for r in table_rows(sec.get('트리거', '')):
        # 무엇을 · 갈래 · metric · 걸리는 조건
        what, tk, key, cond = (r + ['', '', '', ''])[:4]
        v = vals.get(key) or {}
        # series 는 [(때, 값), …]. 트렌드 도해가 이 자리를 읽는다 — 트리거 값과 같은
        # 파일에 두면 「지금 값」이 시계열의 마지막 점이라 둘이 어긋날 일이 없다.
        ser = [tuple(x) for x in (v.get('series') or [])]
        trg.append({'what': what, 'kind': tk, 'metric': key, 'cond': cond,
                    'value': v.get('value'), 'as_of': v.get('as_of'),
                    'nature': v.get('kind'), 'src': v.get('src'),
                    'unit': v.get('unit', ''), 'series': ser})

    return {
        'slug': slug, 'path': os.path.relpath(path, os.path.dirname(HERE)),
        'kind': kind, 'target': meta.get('target', ''),
        'ticker': meta.get('ticker', ''),
        # view — 같은 대상을 다른 물음으로 보는 줄이 둘 이상일 때 제목을 가른다
        'view': meta.get('view', ''),
        'topic': meta.get('topic', ''),
        'opened': meta.get('opened', ''), 'checked': meta.get('checked', ''),
        'why': meta.get('why', ''),
        'judged': md_inline(sec.get('지금 판단', '').replace('\n', ' ')),
        'triggers': trg,
        # metrics 는 이 줄이 쓰겠다고 밝힌 것만이다. 트리거에 건 열쇠와 frontmatter 의
        # context 에 적은 앞머리가 그것이다. 어댑터가 받은 것을 통째로 내주면 같은 대상을
        # 다른 물음으로 보는 줄들이 전부 같은 그림을 그린다 — 줄을 가른 뜻이 사라진다.
        'metrics': _pick(vals, [t['metric'] for t in trg], meta.get('context', '')),
        'points': [md_inline(b) for b in bullets(sec.get('왜 보나', ''))],
        'clash': [md_inline(b) for b in bullets(sec.get('반대 근거', ''))],
    }


def load_all():
    out = []
    for p in sorted(glob.glob(os.path.join(WATCH, '*', '*.md'))):
        if os.path.basename(os.path.dirname(p)) == '_metrics':
            continue
        out.append(load_one(p))
    return out


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    for w in load_all():
        print('%-12s %-8s 트리거 %d (값 %d · 사건 %d)' % (
            w['target'], w['kind'], len(w['triggers']),
            sum(1 for t in w['triggers'] if t['kind'] == KIND_VALUE),
            sum(1 for t in w['triggers'] if t['kind'] == KIND_EVENT)))


# ── 조건을 기계가 읽는다 ──────────────────────────────────────────────────
# 「걸리는 조건」은 사람이 읽는 문장이었다. 그래서 「지금 걸렸나」가 카드 산문에 손으로
# 적혔고(「강북구에서 이미 넘었다」) 값이 바뀌어도 그 문장은 안 바뀌었다.
# 여기서 읽을 수 있는 꼴만 정해 두고, 못 읽는 것은 「사람 판정」으로 남긴다 —
# 억지로 다 읽으려 들면 조용히 틀린 판정이 화면에 뜬다.
# 창을 「몇 점」으로 읽는다. 부동산은 월, 종목은 연·분기라 단위 낱말이 다른데
# 세는 것은 어느 쪽이든 시계열의 점 개수다 — 낱말을 하나로 박으면 종목 줄이 통째로
# 「사람 판정」으로 떨어진다.
COND_FORMS = [
    (re.compile(r'최근\s*(\d+)\s*(?:개월|달|년|분기|점)?\s*최고\s*경신'), 'max_n'),
    (re.compile(r'최근\s*(\d+)\s*(?:개월|달|년|분기|점)?\s*최저\s*경신'), 'min_n'),
    (re.compile(r'직전\s*고점\s*대비\s*([\d.]+)\s*%\s*하회'), 'peak_down'),
    (re.compile(r'([\d.]+)\s*%?\s*상향\s*돌파'), 'above'),
    (re.compile(r'([\d.]+)\s*%?\s*하회'), 'below'),
    (re.compile(r'([\d.]+)\s*%?\s*초과'), 'above'),
]


def parse_cond(cond):
    """조건 문장 → (꼴, 수). 못 읽으면 (None, None)."""
    for rx, kind in COND_FORMS:
        m = rx.search(cond or '')
        if m:
            return kind, float(m.group(1))
    return None, None


def fires_at(kind, num, vals, i):
    """vals[:i+1] 까지 봤을 때 i 번째 달에 조건이 걸렸나. vals 는 값만 담은 목록."""
    v = vals[i]
    if kind == 'above':
        return v > num
    if kind == 'below':
        return v < num
    if kind == 'peak_down':
        return v <= max(vals[:i + 1]) * (1 - num / 100.0)
    if kind in ('max_n', 'min_n'):
        w = vals[max(0, i - int(num) + 1):i + 1]
        if len(w) < 2:
            return False
        return v >= max(w) if kind == 'max_n' else v <= min(w)
    return False


def nearest(cond, series):
    """한 번도 안 걸렸을 때 가장 가까웠던 거리 — 그 시계열 자신의 변동폭에 견줘 잰다.

    0.0 이면 닿았던 것이고 1.0 이면 이력 변동폭만큼 떨어져 있었다는 뜻이다.
    「아직 안 일어난 일」과 「애초에 닿을 수 없는 문턱」을 가르는 자리다.
    거리로 잴 수 없는 꼴(경신류)에는 None."""
    kind, num = parse_cond(cond)
    vals = [v for _t, v in (series or [])]
    if kind not in ('above', 'below', 'peak_down') or len(vals) < 2:
        return None
    span = max(vals) - min(vals)
    if span <= 0:
        return None
    if kind == 'above':
        gap = min(num - v for v in vals)
    elif kind == 'below':
        gap = min(v - num for v in vals)
    else:
        gap = min(v - max(vals[:i + 1]) * (1 - num / 100.0) for i, v in enumerate(vals))
    return max(gap, 0.0) / span


def backtest(cond, series):
    """이 조건이 이력에서 몇 번 걸렸나. (걸린 달 수, 전체 달 수, 지금 걸렸나).

    조건을 못 읽거나 시계열이 없으면 (None, None, None). 문턱이 0회거나 전부면
    그건 신호가 아니라는 뜻이다 — check_watch W8 이 그걸 센다."""
    kind, num = parse_cond(cond)
    if kind is None or not series:
        return None, None, None
    vals = [v for _t, v in series]
    fired = [i for i in range(len(vals)) if fires_at(kind, num, vals, i)]
    return len(fired), len(vals), bool(fired and fired[-1] == len(vals) - 1)


def state_now(cond, series):
    """지금 이 조건이 어떤 상태인가. (표시, 설명).

    표시는 걸림 · 근접 · 멂 · 사람 판정 · — 다섯. 「지금 걸렸나」를 카드 산문에 손으로
    적던 것을 여기서 낸다 — 손으로 적으면 값이 바뀌어도 그 문장이 안 바뀐다.
    거리를 못 재는 꼴(경신류)은 창 안에서 몇 번째인지로 말한다."""
    if not series:
        return '—', '값이 아직 없다'
    kind, num = parse_cond(cond)
    if kind is None:
        return '사람 판정', '조건을 기계가 못 읽는다'
    vals = [v for _t, v in series]
    i = len(vals) - 1
    if fires_at(kind, num, vals, i):
        return '걸림', '지금 조건에 든다'
    v = vals[i]
    if kind in ('above', 'below'):
        gap = (num - v) if kind == 'above' else (v - num)
        span = max(vals) - min(vals)
        near = span and gap <= span * 0.25
        return ('근접' if near else '멂',
                '문턱까지 %.2f' % gap + (' (이력 변동폭의 %.0f%%)' % (100.0 * gap / span)
                                      if span else ''))
    if kind == 'peak_down':
        peak = max(vals)
        need = peak * (1 - num / 100.0)
        return ('근접' if v <= need * 1.02 else '멂',
                '고점 %.2f 대비 지금 %+.1f%%' % (peak, (v / peak - 1) * 100))
    # 경신류 — 창 안에서 몇 번째인지가 곧 얼마나 가까운지다.
    # 단위 낱말은 조건에 적힌 것을 되쓴다 — 「개월」로 박으면 연·분기 시계열에서
    # 설명이 거짓말을 한다
    w = vals[max(0, i - int(num) + 1):i + 1]
    rank = (sorted(w, reverse=True).index(v) + 1 if kind == 'max_n'
            else sorted(w).index(v) + 1)
    um = re.search(r'최근\s*\d+\s*(개월|달|년|분기)', cond or '')
    return ('근접' if rank <= 3 else '멂',
            '최근 %d%s 중 %d번째' % (len(w), um.group(1) if um else '점', rank))
