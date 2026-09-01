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
    return rows[1:] if rows else []      # 첫 줄은 머리


def bullets(block):
    """- 로 시작하는 줄만. 여러 줄로 접힌 항목은 이어 붙인다."""
    out = []
    for ln in block.splitlines():
        s = ln.strip()
        if s.startswith('- '):
            out.append(s[2:].strip())
        elif out and s:
            out[-1] += ' ' + s
    return out


def md_inline(s):
    """**굵게** 와 `코드` 만 마크업으로. 본문 전체를 마크다운으로 굴리지 않는다 —
    카드가 받는 것은 이미 HTML 이고, 여기서 바꿀 것은 이 둘뿐이다."""
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
