# -*- coding: utf-8 -*-
# 「드라이버 지도」 렌더러. 값과 근거는 driver_map_data.py가 갖는다 — 여기서는 손대지 않는다.
# 회계사 대시보드의 rollup 슬롯에 꽂히는 CSS+HTML+JS 한 덩어리를 render()가 만들어 낸다.
#
# 스타일 변수는 dash_common.css()가 물려받는 언더스탠딩 대시보드 CSS의 실제 토큰을 그대로 쓴다:
#   --paper --surface --sunk --ink --ink-2 --ink-3 --line
#   --accent --accent-ink --accent-soft --good --good-soft --warn --warn-soft --risk --risk-soft --shadow
# 새 색은 하드코딩하지 않는다.
#
# 구조는 상위/하위 2단계다. 수식 사슬 안의 드라이버는 이제 누르는 칩이 아니라 읽는 텍스트고,
# 축 카드 아래에 그 축이 쓰는 상위 드라이버(GROUPS)만 칩으로 놓는다. 누르면 팝업(모달)이
# 뜨고, 1단계는 갈래 화면(질문·왜·코퍼스+세부 드라이버 목록), 2단계는 세부 드라이버 화면이다.
import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import driver_map_data as dmd

sys.path.insert(0, os.path.join(dc.ROOT, 'insights'))
import notes_lib as nl  # noqa: E402

# 수식 사슬 안의 {드라이버id} 를 이제는 텍스트로 바꾼다 — 수식은 읽는 것이지 누르는 것이
# 아니다. str.format을 쓰지 않는 건 수식에 (1+...) 같은 괄호가 있어서 format의 {}와
# 충돌하기 때문이다.
_CHIP_RE = re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}')


def _chain_label(driver_id):
    d = dmd.DRIVERS[driver_id]
    return '<b class="dm-chain-driver">%s</b>' % d['label']


def _linkify(line):
    return _CHIP_RE.sub(lambda m: _chain_label(m.group(1)), line)


def _by_badge(key):
    """누가 낸 값인가 배지. 내 계산(ours)을 필자 주장으로 읽지 않게 값마다 붙인다."""
    label, desc = dmd.BY[key]
    return '<span class="dm-by dm-by--%s" title="%s">%s</span>' % (key, desc, label)


# ── 내 판정 (insights/valuation/005930-삼성전자/judgment.json) ──────
# 이 파일은 종목마다 있을 수도 없을 수도 있다. 없거나 깨졌으면 조용히 건너뛴다 —
# 예외를 던지면 이 파일이 없는 다른 종목 대시보드까지 죽는다.
_JUDGMENT_PATH = os.path.join(dc.ROOT, 'insights', 'valuation', '005930-삼성전자', 'judgment.json')
_NOTES_DIR = os.path.join(dc.ROOT, 'insights', 'notes')

_VERDICT_CLASS = {'유지': 'keep', '수정': 'fix', '보류': 'hold', '확인필요': 'check'}

# 근거 묶음 키 → 화면에 쓸 이름. cite만 「근거」로 바꾸고 나머지는 밑줄을 공백으로
# 바꿔 그대로 쓴다(높게_볼_근거 → 높게 볼 근거).
_EV_KEYS = [('cite', '근거'), ('높게_볼_근거', '높게 볼 근거'),
            ('낮게_볼_근거', '낮게 볼 근거'), ('반대_근거', '반대 근거')]
_EXTRA_KEYS = [('영향', '영향'), ('단서', '단서'), ('다음에_할_일', '다음에 할 일')]

# 인용 해석 성공/실패를 세어 보고에 쓴다. (note, cite, ok) 튜플을 쌓는다.
_RESOLVE_LOG = []
_resolve_cache = {}


def _map_driver_id(raw):
    """judgment.json의 driver 값을 DRIVERS 키로 맞춘다. d_opm_하강시점처럼
    DRIVERS에 없는 세부 키는 마지막 밑줄 뒤를 잘라 상위 드라이버로 붙인다."""
    if raw in dmd.DRIVERS:
        return raw
    if '_' in raw:
        cut = raw.rsplit('_', 1)[0]
        if cut in dmd.DRIVERS:
            return cut
    return None


def _load_judgment():
    try:
        with io.open(_JUDGMENT_PATH, encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return {}, None, []

    by_driver = {}

    def add(did, entry):
        if did is None:
            return
        by_driver.setdefault(did, []).append(entry)

    fixed = data.get('고정한_것') or {}
    if isinstance(fixed.get('discount_rate'), dict):
        v = fixed['discount_rate']
        add('d_wacc', dict(verdict=v.get('verdict'), why=v.get('why')))
    if isinstance(fixed.get('terminal_growth'), dict):
        v = fixed['terminal_growth']
        add('d_g', dict(verdict=v.get('verdict'), why=v.get('why')))

    for v in (data.get('verdicts') or []):
        did = _map_driver_id(v.get('driver', ''))
        add(did, dict(v))

    return by_driver, data.get('as_of'), data.get('아직_판정_못한_것') or []


_JUDGMENTS, _JUDGMENT_ASOF, _JUDGMENT_TODO = _load_judgment()


def _resolve_note_sources(note_name):
    if note_name in _resolve_cache:
        return _resolve_cache[note_name]
    sources = []
    try:
        path = os.path.join(_NOTES_DIR, note_name + '.md')
        with io.open(path, encoding='utf-8') as f:
            text = f.read()
        meta, _body = nl.parse_front(text)
        sources = nl.sources_of(meta)
    except Exception:
        sources = []
    _resolve_cache[note_name] = sources
    return sources


def _resolve_evidence_url(note_name, cite_str):
    """근거 {note, cite}를 원문 파일 + 줄로 풀어 blob 링크를 낸다. 못 풀면 None —
    조용히 죽지 않고 링크 없이 인용 문자열만 보인다."""
    if not note_name or not cite_str:
        return None
    sources = _resolve_note_sources(note_name)
    ok = False
    url = None
    if sources:
        try:
            refs = nl.cite_refs('(%s)' % cite_str, sources)
        except Exception:
            refs = []
        if refs and refs[0]['ok'] and refs[0]['lines']:
            url = dc.blob(refs[0]['file']) + '#L%d' % refs[0]['lines'][0]
            ok = True
    _RESOLVE_LOG.append((note_name, cite_str, ok))
    return url


def _evidence_item_data(item):
    """근거 한 줄. url은 여기서(파이썬) 미리 풀어 둔다 — JS는 텍스트만 조립한다.
    HTML은 JS 쪽에서 만든다 — JSON 데이터 안에 <div>가 그대로 박히면 </div>만
    </ 이스케이프 규칙(data_json의 replace('</','<\\/'))에 걸려 div 짝이 안 맞아 보인다."""
    note = item.get('note', '')
    cite = item.get('cite', '')
    fact = item.get('fact', '')
    return dict(note=note, cite=cite, fact=fact, url=_resolve_evidence_url(note, cite))


def _evidence_groups_data(v):
    groups = []
    for key, label in _EV_KEYS:
        items = v.get(key)
        if not items:
            continue
        groups.append(dict(label=label, items=[_evidence_item_data(it) for it in items]))
    return groups


def _extra_data(v):
    out = []
    for key, label in _EXTRA_KEYS:
        val = v.get(key)
        if val:
            out.append(dict(label=label, text=val))
    return out


def _judgment_entries_data(entries):
    """드라이버 상세(2단계)의 「내 판정」 칸에 쓸 구조화 데이터. 판정이 둘이면(d_opm)
    항목이 둘이고, 그때만 각 항목에 원래 label을 붙여 구분한다."""
    if not entries:
        return None
    show_label = len(entries) > 1
    out = []
    for v in entries:
        out.append(dict(
            label=v.get('label') if show_label else None,
            verdict=v.get('verdict'),
            why=v.get('why'),
            mine=v.get('mine'),
            evidence=_evidence_groups_data(v),
            extra=_extra_data(v),
        ))
    return out


def _judgment_todo_html(items, as_of):
    if not items:
        return ''
    lis = ''.join('<li>%s</li>' % nl.esc(x) for x in items)
    asof_html = ('<span class="dm-jgtodo-date">%s 기준</span>' % nl.esc(as_of)) if as_of else ''
    return ('<div class="dm-jgtodo"><p class="dm-jgtodo-label">아직 판정 못한 것%s</p>'
            '<ul class="dm-jgtodo-list">%s</ul></div>' % (asof_html, lis))


def _group_chips_html(ax):
    """그 축이 쓰는 갈래만, GROUPS 순서대로 칩을 낸다. 세부 개수를 같이 보이고,
    그 축의 세부 드라이버 중 근거가 빈 것(basis=='none')이 있으면 경고 표시를 단다."""
    rows = []
    for g in dmd.GROUPS:
        members = g['members'].get(ax['id'])
        if not members:
            continue
        warn = any(dmd.DRIVERS[did]['basis'] == 'none' for did in members)
        warn_html = ('<span class="dm-gchip-warn" aria-hidden="true" title="근거가 빈 값 포함">!</span>'
                     if warn else '')
        # 내 판정이 붙은 세부 드라이버 개수 — 근거 없음 경고(!)와 자리를 나눠 구분되게 둔다.
        jg_n = sum(1 for did in members if did in _JUDGMENTS)
        jg_html = ('<span class="dm-gchip-jg" aria-hidden="true" '
                   'title="내 판정이 있는 세부 드라이버 %d개">%d</span>' % (jg_n, jg_n)
                   if jg_n else '')
        rows.append(
            '<button type="button" class="dm-gchip" data-group="%s" data-members="%s" '
            'aria-haspopup="dialog">'
            '<span class="dm-gchip-name">%s</span><span class="dm-gchip-n">· %d</span>%s%s'
            '</button>' % (g['id'], ','.join(members), g['name'], len(members), warn_html, jg_html))
    if not rows:
        return ''
    return '<div class="dm-gchips">%s</div>' % ''.join(rows)


def _doc_date(key):
    return '20%s-%s-%s' % (key[:2], key[2:4], key[4:6])


def _axis_latest_html(ax):
    """이 축의 최신 글이 무엇인지 패널 맨 위에 한 줄로 적는다. 그 축이 글을
    여럿 쓰면 나머지도 작게 나열한다 — 아니면 「이 하나가 이 방법의 전부다」로 읽힌다."""
    key, date, title = ax['latest']
    url = dc.blob(dmd.SUM + dmd.DOCS[key])
    others = [d for d in ax.get('docs', []) if d != key]
    others_html = ''
    if others:
        links = ' · '.join(
            '<a href="%s" target="_blank" rel="noopener">%s</a>'
            % (dc.blob(dmd.SUM + dmd.DOCS[d]), _doc_date(d)) for d in others)
        others_html = '<p class="dm-axis-otherdocs">그 밖에: %s</p>' % links
    return ('<div class="dm-axis-latest">'
            '<span class="dm-axis-latest-date">%s</span>'
            '<span class="dm-axis-latest-title">%s</span>'
            '<a class="dm-axis-latest-link" href="%s" target="_blank" rel="noopener">요약본 ▸</a>'
            '</div>%s' % (date, title, url, others_html))


def _author_scenarios_html():
    """엘곰이 직접 만든 시나리오(02-26 역산 글의 보수 A·기준 B). 그 글에서 나온
    것이라 rev 축 패널에 속한다 — 위층 「내 계산」과 섞이면 안 된다."""
    s = dmd.SCENARIOS
    if not s.get('author_scenarios'):
        return ''
    au = s['author_scenarios']
    ah2 = ''.join('<th>%s</th>' % h for h in au['head'])
    ab2 = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in au['rows'])
    return (
        '<div class="dm-auth"><p class="dm-auth-label">%s %s</p>'
        '<p class="dm-auth-lede">%s</p>'
        '<div class="dm-auth-wrap"><table class="dm-auth-tbl">'
        '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
        '<p class="dm-auth-note">%s</p></div>'
        % (au['label'], _by_badge(au['by']), au['lede'], ah2, ab2, au['note']))


def _axis_html(ax):
    # 역산(rev)은 방향이 반대다 — 가격이 출력이 아니라 입력이다. 그래서 셋과
    # 같은 「적정가」 줄에 세우지 않고, 테두리·머리 색·결과 라벨을 다르게 그린다.
    is_rev = ax.get('kind') == 'reverse'
    axis_cls = 'dm-axis dm-axis--reverse' if is_rev else 'dm-axis'
    input_driver = dmd.INPUT_DRIVER.get(ax['id']) if is_rev else None
    latest_html = _axis_latest_html(ax)

    inputs_html = ''
    if ax.get('inputs'):
        rows = []
        for k, v in ax['inputs']:
            if input_driver and '시가총액' in k:
                rows.append(
                    '<tr><td class="dm-inputs-k">%s</td><td><button type="button" '
                    'class="dm-inputs-btn" data-driver="%s" data-noback="1">%s</button></td></tr>'
                    % (k, input_driver, v))
            else:
                rows.append('<tr><td class="dm-inputs-k">%s</td>'
                            '<td class="dm-inputs-v">%s</td></tr>' % (k, v))
        inputs_html = ('<div class="dm-inputs"><p class="dm-inputs-label">입력</p>'
                       '<div class="dm-inputs-wrap"><table class="dm-inputs-tbl">'
                       '<thead><tr><th>입력</th><th>값</th></tr></thead>'
                       '<tbody>%s</tbody></table></div></div>' % ''.join(rows))

    chain_html = ''.join('<p class="dm-chain-line">%s</p>' % _linkify(c) for c in ax['chain'])
    gchips_html = _group_chips_html(ax)

    out_tag = '이 주가를 유지하려면 필요한 것' if is_rev else '결과'
    result_driver = dmd.RESULT_OF.get(ax['id'])
    if result_driver:
        out_html = (
            '<button type="button" class="dm-axis-out dm-axis-out--btn" '
            'data-driver="%s" data-noback="1">'
            '<span class="dm-axis-out-tag">%s</span><span class="dm-axis-out-val">%s</span>'
            '</button>' % (result_driver, out_tag, ax['out']))
    else:
        out_html = ('<div class="dm-axis-out"><span class="dm-axis-out-tag">%s</span>'
                    '<span class="dm-axis-out-val">%s</span></div>' % (out_tag, ax['out']))

    # 07-16 민감도 25칸 격자는 그 글이 낸 DCF 축 자료다. 드라이버 범위·이익 경로 표와
    # 달리 다섯 축을 가로지르지 않으므로 패널 밖에 두면 어느 글 것인지 안 보인다.
    # dcf 축에만, 수식→칩→결과 다음 자리에 끼운다.
    sens_html = (_sens_html() + _earnpath_html()) if ax['id'] == 'dcf' else ''

    # 재무제표 축은 값을 내지 않는 앞단계다. 그래서 결과 줄만 두면 왜 있는 축인지
    # 안 보인다. 다섯 편이 잰 것과 그걸 8년 DCF가 어떻게 썼는지를 여기 붙인다.
    if ax['id'] == 'stmt':
        sens_html = _stmt_vs_dcf_html() + _cash_bridge_html()

    # 역산 축의 값어치는 필자를 감사하는 데 있지 않고 시장이 무엇을 깔고 있는지를
    # 읽는 데 있다. 그래서 같은 공식을 시점마다 내가 다시 돌린 표를 결과 뒤에 붙인다.
    mr_html = ''
    if ax.get('market_read'):
        mr = ax['market_read']
        head = ''.join('<th>%s</th>' % h for h in mr['head'])
        body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in mr['rows'])
        mr_html = ('<div class="dm-mr"><p class="dm-mr-label">그 주가를 유지하려면 필요한 이익 — 시점마다 다시 계산했다 %s</p>'
                   '<div class="dm-mr-wrap"><table class="dm-mr-tbl">'
                   '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                   '<p class="dm-mr-note">%s</p></div>' % (_by_badge('ours'), head, body, mr['note']))

    bench_html = ''
    if ax.get('benchmark'):
        rows = ''.join(
            '<tr><td>%s</td><td class="dm-bench-v">%s</td><td class="dm-bench-note">%s</td></tr>'
            % (k, v, note) for k, v, note in ax['benchmark'])
        bench_html = ('<div class="dm-bench"><p class="dm-bench-label">그 이익이 나올 만한가</p>'
                      '<div class="dm-bench-wrap"><table class="dm-bench-tbl">'
                      '<thead><tr><th>대조 대상</th><th>값</th><th>요구치와 견주면</th></tr></thead>'
                      '<tbody>%s</tbody></table></div></div>' % rows)

    # 엘곰이 직접 만든 시나리오(02-26 역산 글)는 rev 축에만 속한다. 대조 표
    # 다음, 판정 앞에 놓는다.
    auth_html = _author_scenarios_html() if is_rev else ''

    verdict_html = ''
    if ax['verdict']:
        vlabel, vdesc = ax['verdict']
        vcls = 'dm-verdict--risk' if '되지 않는다' in vlabel else 'dm-verdict--good'
        verdict_html = ('<div class="dm-verdict %s"><span class="dm-verdict-tag">%s</span>'
                         '<span class="dm-verdict-desc">%s</span></div>' % (vcls, vlabel, vdesc))

    return ('<article class="%s" id="dm-axis-%s">'
            '<div class="dm-axis-head"><span class="dm-axis-no">%s</span>'
            '<div class="dm-axis-headtext"><h3 class="dm-axis-name">%s</h3>'
            '<span class="dm-axis-tag">%s</span></div></div>'
            '%s'
            '<p class="dm-axis-sub">%s</p>'
            '%s'
            '<div class="dm-chain">%s</div>'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '</article>'
            % (axis_cls, ax['id'], ax['no'], ax['name'], ax['tag'], latest_html, ax['sub'],
               inputs_html, chain_html, gchips_html, out_html, sens_html, mr_html, bench_html,
               auth_html, verdict_html))


_AXIS_IDS = set(ax['id'] for ax in dmd.AXES)
_AXIS_LOOKUP = {ax['id']: (ax['no'], ax['name']) for ax in dmd.AXES}
_AXIS_LOOKUP['quote'] = ('—', '외부 인용')



def _ranges_html():
    """엘곰이 드라이버마다 얼마나 벌려 봤는지. 성장 경로 둘만 보이면 그가 시나리오를
    조금밖에 안 만든 것처럼 읽힌다."""
    a = dmd.AUTHOR_RANGES
    head = ''.join('<th>%s</th>' % h for h in a['head'])
    body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in a['rows'])
    return ('<div class="dm-rg"><p class="dm-rg-label">%s %s</p>'
            '<p class="dm-rg-lede">%s</p>'
            '<div class="dm-rg-wrap"><table class="dm-rg-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-rg-note">%s</p></div>'
            % (a['label'], _by_badge(a['by']), a['lede'], head, body, a['note']))


def _sens_html():
    """25칸 격자를 그대로 올린다. 3×3으로 줄이면 그가 얼마나 넓게 시험했는지가 안 보인다."""
    v = dmd.SENSITIVITY
    br, bc = v['base']
    head = ''.join('<th>%s</th>' % h for h in v['head'])
    body = []
    for i, r in enumerate(v['rows']):
        tds = []
        for j, c in enumerate(r):
            cls = ''
            if j == 0:
                cls = ' class="dm-sn-rowhead"'
            elif i == br and j - 1 == bc:
                cls = ' class="dm-sn-base"'
            tds.append('<td%s>%s</td>' % (cls, c))
        body.append('<tr>%s</tr>' % ''.join(tds))
    return ('<div class="dm-sn"><p class="dm-sn-label">%s %s</p>'
            '<div class="dm-sn-wrap"><table class="dm-sn-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-sn-note">%s</p></div>'
            % (v['label'], _by_badge(v['by']), head, ''.join(body), v['note']))


def _earnpath_html():
    """이익 성장 경로를 한 표에 세운다. 말로 적으면 「+25%로 3년, 그다음 10%」가
    귀에 안 들어온다. 나란히 놓아야 출발점과 착지점의 어긋남이 보인다."""
    e = dmd.EARN_PATH
    ncol = len(e['head'])
    head = ''.join('<th>%s</th>' % h for h in e['head'])
    body = []
    for label, rows in e['bands']:
        body.append('<tr class="dm-ep-band"><td colspan="%d">%s</td></tr>' % (ncol, label))
        for r in rows:
            cls = []
            if r.get('note'):
                cls.append('dm-ep-hi')
            if r.get('muted'):
                cls.append('dm-ep-muted')
            cells = ''.join('<td>%s</td>' % c for c in r['cells'])
            body.append('<tr%s>%s</tr>'
                        % (' class="%s"' % ' '.join(cls) if cls else '', cells))
            # 메모를 연도 칸 안에 넣었더니 좁은 칸을 넘쳐 옆 숫자와 겹쳤다.
            # 행을 하나 더 써서 가로로 펼친다.
            if r.get('note'):
                body.append('<tr class="dm-ep-noterow"><td colspan="%d">%s</td></tr>'
                            % (ncol, r['note']))
    body = ''.join(body)
    return ('<div class="dm-ep">'
            '<p class="dm-ep-label">%s</p>'
            '<div class="dm-ep-wrap"><table class="dm-ep-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-ep-punch">%s</p>'
            '<p class="dm-ep-foot">%s</p>'
            '</div>' % (e['lede'], head, body, e['punch'], e['foot']))


def _stmt_vs_dcf_html():
    """재무제표 본편 다섯이 잰 것과 8년 DCF가 실제로 쓴 것을 마주 세운다.
    따로 두면 다섯 편이 그냥 옛날 글로 보인다. 나란히 놓아야 빠진 자리가 보인다."""
    v = dmd.STMT_VS_DCF
    head = ''.join('<th>%s</th>' % h for h in v['head'])
    body = []
    for r in v['rows']:
        cls = ' class="dm-sv-hi"' if r.get('tone') == 'high' else ''
        body.append('<tr%s>%s</tr>'
                    % (cls, ''.join('<td>%s</td>' % c for c in r['cells'])))
    return ('<div class="dm-sv"><p class="dm-sv-label">%s %s</p>'
            '<p class="dm-sv-lede">%s</p>'
            '<div class="dm-sv-wrap"><table class="dm-sv-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-sv-note">%s</p></div>'
            % (v['label'], _by_badge(v['by']), v['lede'], head, ''.join(body), v['note']))


def _cash_bridge_html():
    """영업이익에서 FCF까지의 다리. 원문에 빈칸이던 두 자리(세율·앞 3년 D&A)를
    항등식으로 되돌린 것이라, 되돌아왔다는 사실 자체가 △NWC=0의 증거다."""
    v = dmd.CASH_BRIDGE
    head = ''.join('<th>%s</th>' % h for h in v['head'])
    body = []
    for r in v['rows']:
        cls = ' class="dm-cb-solved"' if r.get('solved') else ''
        body.append('<tr%s>%s</tr>'
                    % (cls, ''.join('<td>%s</td>' % c for c in r['cells'])))
    results = ''.join(
        '<tr><td class="dm-cb-rk">%s</td><td class="dm-cb-rv">%s</td></tr>' % (k, d)
        for k, d in v['results'])
    return ('<div class="dm-cb"><p class="dm-cb-label">%s %s</p>'
            '<p class="dm-cb-lede">%s</p>'
            '<div class="dm-cb-wrap"><table class="dm-cb-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-cb-note">%s</p>'
            '<div class="dm-cb-res"><p class="dm-cb-reslabel">되돌린 것</p>'
            '<table class="dm-cb-restbl"><tbody>%s</tbody></table></div>'
            '<p class="dm-cb-punch">%s</p>'
            '<p class="dm-cb-foot">%s</p></div>'
            % (v['label'], _by_badge(v['by']), v['lede'], head, ''.join(body),
               v['solved_note'], results, v['punch'], v['foot']))


def _scenario_html():
    """이 페이지의 결론 — 한 시점(최신)의 밸류에이션을 보수·기준·공격 세 갈래로
    놓는다. 시장이 실제로 깔고 있는 값은 시나리오가 아니라 참고선이라 표 안에서
    굵은 위쪽 경계선으로 확실히 구분해 마지막에 붙인다."""
    s = dmd.SCENARIOS
    # 정상화 수준을 정하려면 실제 실적을 먼저 봐야 한다. 2025년 값만 보이고 2026년
    # 확정 분기가 안 보이면 보수 시나리오가 이미 나온 실적보다 낮아지는 사고가 난다.
    act_html = ''
    if s.get('actuals'):
        a = s['actuals']
        ah = ''.join('<th>%s</th>' % h for h in a['head'])
        ab = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in a['rows'])
        # 연간·합계는 분기 줄과 기간이 달라 같은 표에 놓으면 분기로 읽힌다. 따로 세운다.
        sums = ''
        if a.get('rows2'):
            sums = '<dl class="dm-act-sums">%s</dl>' % ''.join(
                '<dt>%s</dt><dd>%s</dd>' % (k, v) for k, v in a['rows2'])
        act_html = ('<div class="dm-act"><p class="dm-act-label">%s</p>'
                    '<div class="dm-act-wrap"><table class="dm-act-tbl">'
                    '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                    '%s<p class="dm-act-note">%s</p></div>'
                    % (a['label'], ah, ab, sums, a['note']))
    head = ''.join('<th>%s</th>' % h for h in s['head'])
    body_rows = []
    for r in s['rows']:
        tone = r.get('tone')
        tone_cls = ' dm-sc-gap--%s' % tone if tone else ''
        tds = []
        for i, c in enumerate(r['cells']):
            if i == 2 and r.get('doc'):
                # 근거만 적으면 어느 글 어느 시점 값인지 알 수 없다. 출처 칩을 붙인다.
                d = r['doc']
                url = dc.blob(dmd.SUM + dmd.DOCS[d]) + '#L%d' % r.get('line', 1)
                label = '%s-%s-%s' % ('20' + d[:2], d[2:4], d[4:6])
                tds.append('<td>%s <a class="dm-sc-src" href="%s" target="_blank" '
                           'rel="noopener">%s ▸</a></td>' % (c, url, label))
            elif i == 4:
                tds.append('<td class="dm-sc-gap%s">%s</td>' % (tone_cls, c))
            else:
                tds.append('<td>%s</td>' % c)
        tds.append('<td>%s</td>' % _by_badge(r['by']))
        body_rows.append('<tr class="dm-sc-row">%s</tr>' % ''.join(tds))
    # 엘곰이 직접 만든 시나리오(02-26 역산 글)는 이 위층이 아니라 rev 축 패널에
    # 놓는다 — 여기는 「내 계산」만 남는 자리다.

    # 역산은 방향이 반대라 같은 표에 넣으면 네 번째 시나리오로 읽힌다. 블록을 따로 세운다.
    rev_html = ''
    if s.get('reverse'):
        rv = s['reverse']
        rv_rows = ['<tr class="dm-rv-row dm-rv-row--main"><td>요구 할인율</td>'
                   '<td class="dm-rv-val">%s</td><td class="dm-rv-notecell">%s</td></tr>'
                   % (rv['result'], rv['result_note'])]
        for k, v, tone in rv['compare']:
            rv_rows.append(
                '<tr class="dm-rv-row"><td>%s</td>'
                '<td class="dm-rv-val dm-rv-val--%s">%s</td><td></td></tr>' % (k, tone, v))
        hl = ''
        if rv.get('headline'):
            h = rv['headline']
            ds = ''.join(
                '<div class="dm-rv-hl-row"><span class="dm-rv-hl-if">%s</span>'
                '<span class="dm-rv-hl-d">%s</span>'
                '<span class="dm-rv-hl-n">%s</span></div>' % (a, b, c)
                for a, b, c in h['demands'])
            hl = ('<div class="dm-rv-hl"><p class="dm-rv-hl-px">%s</p>%s</div>'
                  % (h['price'], ds))
        rev_html = (
            '<div class="dm-rv">'
            '<p class="dm-rv-label">%s %s</p>'
            '<p class="dm-rv-lede">%s</p>'
            '%s'
            '<p class="dm-rv-formula">%s</p>'
            '<div class="dm-rv-wrap"><table class="dm-rv-tbl">'
            '<thead><tr><th>항목</th><th>값</th><th>비고</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            '</div>' % (rv['label'], _by_badge(rv['by']), rv['lede'], hl, rv['formula'],
                        ''.join(rv_rows)))
    return ('<div class="dm-scenario">'
            '<div class="dm-scenario-head">'
            '<p class="dm-scenario-kicker">내 계산 — 지금 시점의 결론</p>'
            '<div class="dm-scenario-meta">'
            '<span class="dm-scenario-asof">%s 기준</span>'
            '<span class="dm-scenario-price">주가 %s</span>'
            '<span class="dm-scenario-mcap">시가총액 %s</span>'
            '</div></div>'
            # 시나리오가 먼저다. 실적 추이는 그 값을 왜 그렇게 잡았는지 받쳐 주는
            # 재료라 아래에 둔다 — 위에 두면 결론 앞에 표가 하나 더 서서 가린다.
            '<p class="dm-fwd-label">이익을 가정하면 적정 주가가 나온다</p>'
            '<p class="dm-scenario-formula">%s</p>'
            '<div class="dm-scenario-wrap"><table class="dm-scenario-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '%s'
            '%s'
            '<p class="dm-scenario-note">%s</p>'
            '<div class="dm-scenario-punch">%s</div>'
            '</div>'
            % (s['asof'], s['price'], s['mcap'], s['formula'], head,
               ''.join(body_rows), rev_html, act_html, s['note'], s['punch']))


def _timeline_html():
    # kind: 'price'(적정가를 낸 평가) | 'ask'(역산 — 가격이 입력이라 값이 아니라
    # 요구 문장이다). 같은 칸의 값처럼 보이면 안 되므로 행 배경을 경고톤으로 가른다.
    # JS는 e.target.closest('.dm-tl-item')로 행을 찾으므로 클래스·data-target·
    # tabindex·role은 그대로 <tr>에 옮긴다 — 이 넷을 건드리면 클릭 이동이 죽는다.
    rows = []
    for date, axid, kind, v1, v2, tag, by in dmd.TIMELINE:
        no, name = _AXIS_LOOKUP.get(axid, ('—', axid))
        target = ' data-target="dm-axis-%s"' % axid if axid in _AXIS_IDS else ''
        badge_html = _by_badge(by)
        axis_label = '%s %s' % (no, name)
        if kind == 'ask':
            rows.append(
                '<tr class="dm-tl-item dm-tl-ask"%s tabindex="0" role="button">'
                '<td class="dm-tl-date">%s</td>'
                '<td class="dm-tl-axis">%s</td>'
                '<td class="dm-tl-val">%s <b>%s</b></td>'
                '<td class="dm-tl-tagcell"><span class="dm-tl-tag">%s</span></td>'
                '<td>%s</td>'
                '</tr>' % (target, date, axis_label, v1, v2, tag, badge_html))
            continue
        cls = ' dm-tl-quote' if axid == 'quote' else ''
        val_html = '%s %s' % (v1, v2) if v2 else v1
        tag_html = '<span class="dm-tl-tag">%s</span>' % tag if tag else ''
        rows.append(
            '<tr class="dm-tl-item%s"%s tabindex="0" role="button">'
            '<td class="dm-tl-date">%s</td>'
            '<td class="dm-tl-axis">%s</td>'
            '<td class="dm-tl-val">%s</td>'
            '<td class="dm-tl-tagcell">%s</td>'
            '<td>%s</td>'
            '</tr>' % (cls, target, date, axis_label, val_html, tag_html, badge_html))
    return ('<div class="dm-timeline-wrap"><table class="dm-timeline-tbl">'
            '<thead><tr><th>날짜</th><th>축</th><th>값</th><th>꼬리표</th><th>계산</th></tr></thead>'
            '<tbody>%s</tbody></table></div>'
            '<p class="dm-tl-hint">행을 누르면 그 축 카드로 이동한다</p>' % ''.join(rows))


def _data_json():
    """모달 JS가 쓰는 데이터. drivers는 예전 그대로, groups는 새로 추가한
    상위 드라이버(1단계 화면) 메타다 — members는 축마다 달라 칩의 data-members로 넘긴다."""
    axis_meta = {ax['id']: '%s %s' % (ax['no'], ax['name']) for ax in dmd.AXES}
    drivers = {}
    for did, d in dmd.DRIVERS.items():
        basis_label, basis_desc = dmd.BASIS[d['basis']]
        url = dc.blob(dmd.SUM + dmd.DOCS[d['doc']]) + '#L%d' % d['line']
        jentries = _JUDGMENTS.get(did)
        drivers[did] = dict(
            label=d['label'], axisMeta=axis_meta.get(d['axis'], d['axis']),
            doc=d['doc'], line=d['line'], base=d['base'],
            basisKey=d['basis'], basisLabel=basis_label, basisDesc=basis_desc,
            why=d['why'], impact=d['impact'], url=url,
            bar=list(d['bar']) if 'bar' in d else None,
            # 「내 판정」 칸 — 구조화 데이터만 넘긴다. HTML은 JS가 만든다(fmtJudgment).
            judgment=_judgment_entries_data(jentries),
            judgmentVerdicts=[e.get('verdict') for e in jentries] if jentries else None,
        )
    groups = {g['id']: dict(name=g['name'], q=g['q'], why=g['why'], corpus=g['corpus'])
              for g in dmd.GROUPS}
    return dict(drivers=drivers, groups=groups)


DM_CSS = '''<style>
.dm-wrap{margin:0 0 30px;padding:0 0 26px;border-bottom:2px solid var(--ink)}
.dm-head{margin:0 0 16px}
.dm-title{font-size:20px;font-weight:850;letter-spacing:-.02em;margin:0 0 8px;color:var(--ink)}
.dm-lede{font-size:14px;line-height:1.62;color:var(--ink-2);margin:0;max-width:68ch}
.dm-lede b{color:var(--ink)}

/* ── 주체 배지 — 값마다 누가 낸 값인지 붙인다. ours가 가장 눈에 띈다 ── */
.dm-by{display:inline-flex;align-items:center;font-size:10px;font-weight:800;letter-spacing:.02em;
      padding:2px 8px;border-radius:999px;line-height:1.5;white-space:nowrap;cursor:help}
.dm-by--author{background:var(--sunk);color:var(--ink-2);border:1px solid var(--line)}
.dm-by--ours{background:var(--accent-soft);color:var(--accent-ink);border:1px solid var(--accent);
            font-weight:850}
.dm-by--ext{background:transparent;color:var(--ink-3);border:1px dashed var(--line)}
.dm-by--market{background:var(--warn-soft);color:var(--warn);border:1px solid var(--warn)}

/* ── 최신 시점 세 시나리오 — 이 페이지의 결론 ── */
.dm-scenario{margin:0 0 22px;background:var(--surface);border:1px solid var(--line);
            border-radius:12px;padding:18px 18px 16px;box-shadow:var(--shadow)}
.dm-scenario-head{margin:0 0 10px}
.dm-scenario-kicker{font-size:11px;font-weight:850;letter-spacing:.05em;color:var(--accent-ink);
                    margin:0 0 6px}
.dm-scenario-meta{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px 16px}
.dm-scenario-asof{font-size:16px;font-weight:850;color:var(--ink)}
.dm-scenario-price,.dm-scenario-mcap{font-size:13px;font-weight:700;color:var(--ink-2)}
.dm-scenario-formula{font-size:12px;line-height:1.6;color:var(--ink-3);margin:8px 0 14px;
                     font-variant-numeric:tabular-nums}
.dm-scenario-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-scenario-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
/* 표 첫 칸 왼쪽 여백을 0으로 두면 하이라이트가 글자에 겹친다. 8px를 준다 */
.dm-scenario-tbl th{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);
                    text-align:left;padding:5px 12px 7px 8px;border-bottom:1px solid var(--line);
                    white-space:nowrap;vertical-align:top}
.dm-scenario-tbl td{padding:8px 12px 8px 8px;border-bottom:1px solid var(--line);color:var(--ink)}
.dm-scenario-tbl td:first-child{font-weight:800}
.dm-sc-gap--low{color:var(--risk);font-weight:800}
.dm-sc-gap--high{color:var(--good);font-weight:800}
/* 시장 행은 시나리오가 아니라 시장이 깔고 있는 값이다 — 굵은 위 경계선으로 가른다 */
.dm-sc-market{border-top:2px solid var(--ink);background:var(--sunk)}
.dm-sc-market td{font-weight:800;border-bottom:0}
.dm-scenario-note{font-size:11.5px;line-height:1.55;color:var(--ink-3);margin:10px 0 0;max-width:70ch}
.dm-scenario-punch{font-size:13.5px;line-height:1.62;color:var(--ink-2);margin:12px 0 0;
                   border-left:3px solid var(--warn);background:var(--warn-soft);
                   border-radius:0 8px 8px 0;padding:10px 14px}
.dm-scenario-punch b{color:var(--ink);font-weight:850}

/* ── 지난 평가 (접힘) — 시간축·이익 경로 표는 결론이 아니라 근거라 뒤로 보낸다 ── */
.dm-past{margin:0 0 24px;border:1px solid var(--line);border-radius:10px;
        background:var(--surface);box-shadow:var(--shadow)}
.dm-past-summary{cursor:pointer;list-style:none;font-size:13px;font-weight:800;color:var(--ink-2);
                 padding:14px 16px}
.dm-past-summary::-webkit-details-marker{display:none}
.dm-past-summary::before{content:"▸ ";color:var(--ink-3)}
.dm-past[open] .dm-past-summary::before{content:"▾ "}
.dm-past-summary:hover{color:var(--ink)}
.dm-past-body{padding:0 16px 16px}

/* ── 시장 읽기 (역산 축만) ── */
.dm-mr{margin:12px 0 0}
.dm-mr-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 6px}
.dm-mr-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-mr-tbl{width:100%;border-collapse:collapse;font-size:12px;font-variant-numeric:tabular-nums}
.dm-mr-tbl th{font-size:10px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);
              text-align:left;padding:4px 8px 4px 0;border-bottom:1px solid var(--line);white-space:nowrap}
.dm-mr-tbl td{padding:5px 8px 5px 0;border-bottom:1px solid var(--line);color:var(--ink-2);white-space:nowrap}
.dm-mr-tbl td:first-child{font-weight:800;color:var(--ink)}
.dm-mr-tbl td:nth-last-child(-n+2){font-weight:800;color:var(--ink)}
.dm-mr-tbl tr:last-child td{border-bottom:0}
.dm-mr-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:7px 0 0}

/* 역방향 결론 두 줄 — 가격이 얼마고, 그 가격이 무엇을 요구하는가 */
.dm-rv-hl{margin:0 0 12px;padding:11px 13px;background:var(--surface);border-radius:10px}
.dm-rv-hl-px{font-size:17px;font-weight:850;letter-spacing:-.01em;color:var(--ink);margin:0 0 8px;
             font-variant-numeric:tabular-nums}
.dm-rv-hl-row{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;
              padding:7px 0 0;border-top:1px solid var(--line)}
.dm-rv-hl-if{grid-column:1;font-size:11px;color:var(--ink-3);white-space:nowrap;align-self:center}
.dm-rv-hl-d{grid-column:2;font-size:14.5px;font-weight:850;color:var(--accent-ink);
            font-variant-numeric:tabular-nums}
.dm-rv-hl-n{grid-column:2;font-size:11px;color:var(--ink-3);line-height:1.5}
@media (max-width:560px){.dm-rv-hl-row{grid-template-columns:1fr}
  .dm-rv-hl-if,.dm-rv-hl-d,.dm-rv-hl-n{grid-column:1}}

/* 근거 옆 출처 칩 — 어느 글 어느 시점 값인지 */
.dm-sc-src{display:inline-block;margin-left:4px;font-size:10px;font-weight:800;
           color:var(--accent-ink);background:var(--accent-soft);border-radius:999px;
           padding:1px 7px;text-decoration:none;white-space:nowrap}
.dm-sc-src:hover{text-decoration:underline}

/* ── 정방향 / 역방향 ── 방향이 반대라 한 표에 세우면 네 번째 시나리오로 읽힌다 */
.dm-fwd-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:14px 0 4px}
.dm-rv{margin:16px 0 0;border-left:3px solid var(--accent);background:var(--accent-soft);
       border-radius:0 10px 10px 0;padding:12px 15px}
.dm-rv-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--accent-ink);margin:0 0 4px}
.dm-rv-lede{font-size:12px;line-height:1.6;color:var(--ink-2);margin:0 0 8px}
.dm-rv-formula{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 10px;
               font-variant-numeric:tabular-nums}
.dm-rv-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-rv-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
.dm-rv-tbl th{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--accent-ink);
             text-align:left;padding:3px 12px 6px 8px;border-bottom:1px solid var(--accent);
             white-space:nowrap;vertical-align:top}
.dm-rv-tbl td{padding:7px 12px 7px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.dm-rv-tbl tr:last-child td{border-bottom:0}
.dm-rv-tbl td:first-child{font-weight:700;color:var(--ink-2)}
.dm-rv-row--main td{font-weight:850;color:var(--ink);font-size:15px}
.dm-rv-row--main td:first-child{font-size:12.5px;font-weight:800;color:var(--ink-2)}
.dm-rv-val{font-variant-numeric:tabular-nums}
.dm-rv-val--high{color:var(--warn);font-weight:800}
.dm-rv-val--low{color:var(--good);font-weight:800}
.dm-rv-notecell{color:var(--ink-3);font-size:11px;font-weight:500;line-height:1.5;
                white-space:normal;max-width:32ch}

/* ── 엘곰이 직접 만든 시나리오 ── 시점이 달라 위 표와 같은 축에 못 놓는다 */
.dm-auth{margin:16px 0 0;border:1px dashed var(--line);border-radius:10px;padding:12px 14px}
.dm-auth-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:0 0 4px}
.dm-auth-lede{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 9px}
.dm-auth-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-auth-tbl{width:100%;border-collapse:collapse;font-size:12px;font-variant-numeric:tabular-nums}
.dm-auth-tbl th{font-size:10px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
                text-align:left;padding:3px 12px 5px 8px;border-bottom:1px solid var(--line);
                white-space:nowrap;vertical-align:top}
.dm-auth-tbl td{padding:6px 12px 6px 8px;border-bottom:1px solid var(--line);
                color:var(--ink-2);white-space:nowrap}
.dm-auth-tbl td:first-child{font-weight:850;color:var(--ink)}
.dm-auth-tbl tr:last-child td{border-bottom:0}
.dm-auth-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

/* ── 실적 표 (시나리오 맨 위) ── 정상화 수준은 실제 실적에서 출발해야 한다 */
.dm-act{margin:12px 0 14px;background:var(--sunk);border-radius:10px;padding:11px 13px}
.dm-act-label{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:0 0 8px}
.dm-act-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-act-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
.dm-act-tbl th{font-size:10px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
               text-align:left;padding:3px 14px 5px 8px;border-bottom:1px solid var(--line);
               white-space:nowrap;vertical-align:top}
.dm-act-tbl td{padding:6px 14px 4px 8px;color:var(--ink);font-weight:800;white-space:nowrap}
.dm-act-tbl td:first-child{color:var(--ink-3);font-weight:700}
.dm-act-tbl th:nth-child(n+6),.dm-act-tbl td:nth-child(n+6){color:var(--accent-ink)}
.dm-act-tbl i{font-style:normal;font-size:10px;font-weight:700;color:var(--ink-3);margin-left:3px}
/* 연간·합계 — 분기 표와 기간이 달라 따로 세운다 */
.dm-act-sums{display:grid;grid-template-columns:1fr auto;gap:4px 14px;margin:10px 0 0;
             padding:9px 10px 8px;background:var(--paper);border-radius:8px}
.dm-act-sums dt{font-size:11.5px;color:var(--ink-2);margin:0}
.dm-act-sums dd{font-size:12.5px;font-weight:850;color:var(--ink);margin:0;text-align:right;
                font-variant-numeric:tabular-nums;white-space:nowrap}
.dm-act-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

/* ── 엘곰이 벌려 본 범위 · 민감도 격자 ── */
.dm-rg,.dm-sn{margin:20px 0 0;background:var(--surface);border:1px solid var(--line);
              border-radius:10px;padding:13px 15px;box-shadow:var(--shadow)}
.dm-rg-label,.dm-sn-label{font-size:12px;font-weight:850;letter-spacing:.02em;
                          color:var(--ink-2);margin:0 0 5px}
.dm-rg-lede{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 9px}
.dm-rg-wrap,.dm-sn-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-rg-tbl,.dm-sn-tbl{width:100%;border-collapse:collapse;font-size:12px;
                      font-variant-numeric:tabular-nums}
.dm-rg-tbl th,.dm-sn-tbl th{font-size:10px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
                            text-align:left;padding:3px 12px 5px 8px;
                            border-bottom:1px solid var(--line);white-space:nowrap;vertical-align:top}
.dm-rg-tbl td,.dm-sn-tbl td{padding:6px 12px 6px 8px;border-bottom:1px solid var(--line);
                            color:var(--ink-2);white-space:nowrap}
.dm-rg-tbl td:first-child,.dm-sn-rowhead{font-weight:850;color:var(--ink)}
.dm-rg-tbl td:last-child{color:var(--ink-3);font-size:11px}
.dm-rg-tbl tr:last-child td,.dm-sn-tbl tr:last-child td{border-bottom:0}
/* 그가 실제로 쓴 조합 한 칸 */
.dm-sn-base{background:var(--accent-soft);color:var(--accent-ink);font-weight:850;
            box-shadow:inset 0 0 0 1px var(--accent)}
.dm-rg-note,.dm-sn-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

/* ── 이익 성장 경로 표 ── */
.dm-ep{margin:20px 0 4px;background:var(--surface);border:1px solid var(--line);
       border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.dm-ep-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 9px}
.dm-ep-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-ep-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
/* 설명 줄 수가 열마다 달라(2줄·3줄) 아래로 맞추면 제목 높이가 어긋난다. 위로 맞춘다 */
.dm-ep-tbl th{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);
              text-align:left;padding:4px 12px 7px 8px;border-bottom:1px solid var(--line);
              white-space:nowrap;vertical-align:top}
/* 보수·기준·직접이 무슨 뜻인지 머리에서 바로 알려 준다 */
.dm-ep-tbl th span{display:block;font-size:10px;font-weight:700;color:var(--ink-3);
                   letter-spacing:0;margin-top:3px;white-space:normal;max-width:19ch}
/* 왼쪽 8px는 하이라이트 세로 바가 앉는 자리다. 0으로 두면 바가 글자에 겹친다 */
.dm-ep-tbl td{padding:5px 12px 5px 8px;border-bottom:1px solid var(--line);
              color:var(--ink);white-space:nowrap}
.dm-ep-tbl td:first-child{font-weight:800}
.dm-ep-tbl i{font-style:normal;font-size:11px;font-weight:700;color:var(--ink-3);margin-left:3px}
/* 국면 띠 — 같은 구간을 두 필자가 다르게 부르므로 라벨에 둘 다 적는다 */
.dm-ep-band td{background:var(--sunk);font-size:10.5px;font-weight:850;letter-spacing:.03em;
               color:var(--ink-3);padding:6px 12px 6px 8px;border-bottom:1px solid var(--line);
               white-space:normal}
/* 출발과 착지 — 이 표의 요점이라 눈에 걸리게 둔다 */
.dm-ep-hi td{background:var(--warn-soft);color:var(--ink);font-weight:800;border-bottom:0}
.dm-ep-hi td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.dm-ep-hi i{color:var(--ink-2)}
.dm-ep-noterow td{background:var(--warn-soft);color:var(--warn);font-size:11px;font-weight:850;
                  letter-spacing:.02em;padding:0 12px 7px 8px;border-bottom:1px solid var(--line);
                  white-space:normal;box-shadow:inset 3px 0 0 var(--warn)}
.dm-ep-noterow td::before{content:"◆ ";font-size:9px;vertical-align:1px}
.dm-ep-muted td{color:var(--ink-3)}
.dm-ep-tbl tr:last-child td{border-bottom:0}
.dm-ep-punch{font-size:13px;line-height:1.62;color:var(--ink-2);margin:11px 0 0;
             border-left:3px solid var(--warn);background:var(--warn-soft);
             border-radius:0 8px 8px 0;padding:9px 13px}
.dm-ep-punch b{color:var(--ink);font-weight:850}
.dm-ep-foot{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

/* ── 재무제표가 잰 것 vs DCF가 쓴 것 ── 마주 세우는 표라 두 열이 대비돼야 한다 */
.dm-sv{margin:20px 0 4px;background:var(--surface);border:1px solid var(--line);
       border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.dm-sv-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 4px}
.dm-sv-lede{font-size:11.5px;line-height:1.55;color:var(--ink-3);margin:0 0 9px}
.dm-sv-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-sv-tbl{width:100%;border-collapse:collapse;font-size:12px}
.dm-sv-tbl th{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);
              text-align:left;padding:4px 12px 7px 8px;border-bottom:1px solid var(--line);
              white-space:nowrap;vertical-align:top}
.dm-sv-tbl td{padding:7px 12px 7px 8px;border-bottom:1px solid var(--line);
              color:var(--ink-2);line-height:1.5;vertical-align:top}
.dm-sv-tbl td:first-child{font-weight:800;color:var(--ink);white-space:nowrap}
.dm-sv-tbl td:nth-child(2){font-size:11px;color:var(--ink-3);white-space:nowrap}
/* 마지막 열이 「안 썼다」를 말하는 자리다. 왼쪽 경계로 갈라 놓는다 */
.dm-sv-tbl td:last-child{border-left:1px solid var(--line);color:var(--ink-3)}
.dm-sv-tbl tr:last-child td{border-bottom:0}
.dm-sv-hi td{background:var(--warn-soft);color:var(--ink)}
.dm-sv-hi td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.dm-sv-hi td:last-child{color:var(--warn);font-weight:800}
.dm-sv-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:9px 0 0}

/* ── 현금흐름 다리 ── 숫자 표라 tabular-nums로 자리를 맞춘다 */
.dm-cb{margin:16px 0 4px;background:var(--surface);border:1px solid var(--line);
       border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.dm-cb-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 4px}
.dm-cb-lede{font-size:11.5px;line-height:1.55;color:var(--ink-3);margin:0 0 9px}
.dm-cb-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-cb-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
.dm-cb-tbl th{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);
              text-align:right;padding:4px 10px 7px 8px;border-bottom:1px solid var(--line);
              white-space:nowrap}
.dm-cb-tbl th:first-child{text-align:left}
.dm-cb-tbl td{padding:5px 10px 5px 8px;border-bottom:1px solid var(--line);
              color:var(--ink);white-space:nowrap;text-align:right}
.dm-cb-tbl td:first-child{font-weight:800;text-align:left}
/* 원문 FCF는 대조용이다. 우리 계산과 같은 무게로 두면 두 번 센 것처럼 보인다 */
.dm-cb-tbl td:last-child{color:var(--ink-3);border-left:1px solid var(--line)}
.dm-cb-tbl th:last-child{border-left:1px solid var(--line)}
.dm-cb-tbl tr:last-child td{border-bottom:0}
/* 되돌린 세 해 — 원문에 없던 값이 들어간 행이라 표시해 둔다 */
.dm-cb-solved td{background:var(--warn-soft)}
.dm-cb-solved td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.dm-cb-solved b{color:var(--warn);font-weight:850}
.dm-cb-note{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}
.dm-cb-res{margin:12px 0 0;background:var(--sunk);border-radius:8px;padding:10px 12px}
.dm-cb-reslabel{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 6px}
.dm-cb-restbl{width:100%;border-collapse:collapse;font-size:11.5px}
.dm-cb-rk{font-weight:850;color:var(--ink);padding:4px 12px 4px 0;
          white-space:nowrap;vertical-align:top}
.dm-cb-rv{color:var(--ink-3);line-height:1.55;padding:4px 0}
.dm-cb-punch{font-size:13px;line-height:1.62;color:var(--ink-2);margin:11px 0 0;
             border-left:3px solid var(--warn);background:var(--warn-soft);
             border-radius:0 8px 8px 0;padding:9px 13px}
.dm-cb-punch b{color:var(--ink);font-weight:850}
.dm-cb-foot{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

@media (max-width:560px){
  /* 좁은 화면에서 다리 표가 8열이라 넘친다. 셀 여백을 줄여 스크롤 폭을 줄인다 */
  .dm-cb-tbl{font-size:11.5px}
  .dm-cb-tbl td, .dm-cb-tbl th{padding-left:6px;padding-right:7px}
  .dm-sv-tbl td:first-child{white-space:normal}
}

/* ── 시간축 ── */
.dm-timeline-wrap{margin:18px 0 4px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-timeline-tbl{width:100%;border-collapse:collapse;font-size:12px;font-variant-numeric:tabular-nums}
.dm-timeline-tbl th{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
                    text-align:left;padding:4px 12px 6px 8px;border-bottom:1px solid var(--line);
                    white-space:nowrap;vertical-align:top}
.dm-timeline-tbl td{padding:8px 12px 8px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.dm-timeline-tbl tr:last-child td{border-bottom:0}
.dm-tl-item{cursor:pointer}
.dm-tl-item:hover td{background:var(--sunk)}
.dm-tl-item:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.dm-tl-date{font-weight:800;color:var(--ink-3);white-space:nowrap}
.dm-tl-axis{color:var(--ink-2);white-space:nowrap}
.dm-tl-val{font-weight:800;color:var(--ink)}
.dm-tl-val b{color:var(--ink);font-weight:850}
.dm-tl-tagcell{white-space:nowrap}
.dm-tl-tag{display:inline-block;font-size:9.5px;font-weight:800;color:var(--ink-3);
          background:var(--sunk);border-radius:999px;padding:2px 8px}
.dm-tl-hint{margin:8px 0 22px;font-size:11px;color:var(--ink-3)}
/* 인용 행에 세로 바를 달았더니 같은 경고색이 역산(배경)과 인용(바) 두 뜻으로
   쓰여 헷갈렸다. 표가 된 뒤로는 「계산」 칸의 배지가 그 일을 하므로 바를 뗀다 */
/* 역산 행 — 값이 아니라 「이 가격이 요구하는 것」이라 배경과 세로 바로 가른다 */
.dm-tl-ask td{background:var(--warn-soft)}
.dm-tl-ask td:first-child{box-shadow:inset 3px 0 0 var(--warn)}
.dm-tl-ask:hover td{background:var(--warn-soft)}
.dm-tl-ask .dm-tl-val{color:var(--ink-2);font-weight:700}
.dm-tl-ask .dm-tl-val b{color:var(--ink);font-weight:850}

/* ── 방법 버튼 줄 + 패널 하나 ── */
.dm-axheading{font-size:14px;font-weight:850;letter-spacing:-.01em;color:var(--ink);
              margin:26px 0 10px}
.dm-axisbtns{display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;
             margin:0 0 14px;padding:2px 2px 6px}
.dm-axisbtn{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-start;gap:2px;
            font:inherit;cursor:pointer;padding:8px 14px;border-radius:10px;
            border:1px solid var(--line);background:var(--surface);color:var(--ink-2)}
.dm-axisbtn:hover{border-color:var(--accent)}
.dm-axisbtn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-axisbtn[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft);
                                 box-shadow:inset 0 0 0 1px var(--accent)}
.dm-axisbtn-no{font-size:10px;font-weight:800;letter-spacing:.02em;color:var(--ink-3)}
.dm-axisbtn[aria-pressed="true"] .dm-axisbtn-no{color:var(--accent-ink)}
.dm-axisbtn-name{font-size:13px;font-weight:850;color:var(--ink)}
.dm-axisbtn[aria-pressed="true"] .dm-axisbtn-name{color:var(--accent-ink)}
.dm-axisbtn-date{font-size:10.5px;font-weight:700;color:var(--ink-3);
                 font-variant-numeric:tabular-nums}
.dm-axispanels{margin:0 0 24px}
.dm-axispanel[hidden]{display:none}

/* ── 축 패널 맨 위 — 이 축의 최신 글 ── */
.dm-axis-latest{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;
                margin:0 0 8px;padding:8px 10px;background:var(--sunk);border-radius:8px}
.dm-axis-latest-date{font-size:11px;font-weight:850;color:var(--ink-3);
                     font-variant-numeric:tabular-nums;white-space:nowrap}
.dm-axis-latest-title{font-size:12px;font-weight:700;color:var(--ink);line-height:1.4}
.dm-axis-latest-link{margin-left:auto;font-size:11px;font-weight:800;color:var(--accent-ink);
                     text-decoration:none;white-space:nowrap}
.dm-axis-latest-link:hover{text-decoration:underline}
.dm-axis-otherdocs{font-size:10.5px;color:var(--ink-3);margin:0 0 10px}
.dm-axis-otherdocs a{color:var(--accent-ink);text-decoration:none}
.dm-axis-otherdocs a:hover{text-decoration:underline}

.dm-axis{background:var(--surface);border:1px solid var(--line);border-radius:12px;
         padding:16px 15px 15px;display:flex;flex-direction:column;box-shadow:var(--shadow)}
.dm-axis-head{display:flex;align-items:flex-start;gap:9px;margin:0 0 6px}
.dm-axis-no{font-size:10.5px;font-weight:800;color:var(--accent);background:var(--accent-soft);
            border-radius:4px;padding:2px 6px;font-variant-numeric:tabular-nums;margin-top:2px;flex:0 0 auto}
.dm-axis-name{font-size:15.5px;font-weight:800;margin:0;letter-spacing:-.01em;color:var(--ink);line-height:1.3}
.dm-axis-tag{display:block;font-size:10px;font-weight:700;color:var(--ink-3);margin-top:3px}
.dm-axis-sub{font-size:12px;color:var(--ink-3);line-height:1.5;margin:0 0 12px}
.dm-chain{display:flex;flex-direction:column;gap:7px;margin:0 0 12px}
.dm-chain-line{font-size:12.5px;line-height:1.75;color:var(--ink-2);margin:0}
.dm-chain-driver{color:var(--ink);font-weight:800}

/* ── 상위 드라이버 칩 줄 ── */
.dm-gchips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px}
.dm-gchip{display:inline-flex;align-items:center;gap:4px;font:inherit;font-size:11.5px;font-weight:700;
          cursor:pointer;padding:4px 10px;margin:0;border-radius:999px;
          border:1px solid var(--accent-soft);background:var(--accent-soft);color:var(--accent-ink);
          line-height:1.4}
.dm-gchip:hover{border-color:var(--accent)}
.dm-gchip:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-gchip-n{opacity:.75;font-weight:600}
.dm-gchip-warn{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;
               width:14px;height:14px;border-radius:50%;background:var(--warn);color:var(--surface);
               font-size:10px;font-weight:900;line-height:1}
/* 내 판정이 있는 세부 드라이버 개수 — 근거 없음 경고(!)와 자리를 나눠 색으로 구분한다 */
.dm-gchip-jg{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;
             min-width:14px;height:14px;padding:0 4px;border-radius:999px;
             background:var(--accent);color:var(--surface);
             font-size:9.5px;font-weight:900;line-height:1}

.dm-axis-out{display:flex;flex-direction:column;gap:2px;margin:0 0 10px;padding-top:10px;
             border-top:1px solid var(--line)}
.dm-axis-out-tag{font-size:10px;font-weight:800;color:var(--ink-3);letter-spacing:.04em}
.dm-axis-out-val{font-size:13px;font-weight:800;color:var(--ink)}
.dm-axis-out--btn{border:0;border-top:1px solid var(--line);background:transparent;color:inherit;
                  width:100%;text-align:left;font:inherit;cursor:pointer;padding:10px 0 0;
                  margin:0 0 10px;border-radius:4px}
.dm-axis-out--btn:hover{background:var(--sunk)}
.dm-axis-out--btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-verdict{border-radius:8px;padding:9px 11px;margin-top:auto}
.dm-verdict-tag{display:block;font-size:11.5px;font-weight:800;margin-bottom:2px}
.dm-verdict-desc{display:block;font-size:11px;line-height:1.5;color:var(--ink-2)}
.dm-verdict--good{background:var(--good-soft)}
.dm-verdict--good .dm-verdict-tag{color:var(--good)}
.dm-verdict--risk{background:var(--risk-soft)}
.dm-verdict--risk .dm-verdict-tag{color:var(--risk)}

/* ── 역산 축 — 가격이 출력이 아니라 입력이다. 방향이 반대라는 걸 테두리·라벨로 드러낸다 ── */
.dm-axis--reverse{border-left:3px solid var(--warn)}
.dm-axis--reverse .dm-axis-no{background:var(--warn-soft);color:var(--warn)}
.dm-axis--reverse .dm-axis-tag{color:var(--warn);font-weight:800}
.dm-axis--reverse .dm-axis-out-tag{color:var(--warn)}

.dm-inputs{background:var(--sunk);border-radius:8px;padding:9px 10px;margin:0 0 11px}
.dm-inputs-label{font-size:10px;font-weight:800;color:var(--ink-3);letter-spacing:.08em;
                 text-transform:uppercase;margin:0 0 6px}
.dm-inputs-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-inputs-tbl{width:100%;border-collapse:collapse;font-size:11.5px}
.dm-inputs-tbl th{font-size:10px;font-weight:800;color:var(--ink-3);text-align:left;
                  padding:2px 10px 4px 8px;border-bottom:1px solid var(--line);
                  white-space:nowrap;vertical-align:top}
.dm-inputs-tbl td{padding:4px 10px 4px 8px;border-bottom:1px solid var(--line)}
.dm-inputs-tbl tr:last-child td{border-bottom:0}
.dm-inputs-k{color:var(--ink-3)}
.dm-inputs-v{font-weight:700;color:var(--ink)}
.dm-inputs-btn{border:0;background:transparent;width:100%;text-align:left;font:inherit;
               font-weight:700;color:var(--ink);cursor:pointer;padding:2px 4px;border-radius:6px}
.dm-inputs-btn:hover{background:var(--surface)}
.dm-inputs-btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.dm-bench{margin:0 0 12px;padding:10px 10px 8px;border:1px dashed var(--line);border-radius:8px}
.dm-bench-label{font-size:10px;font-weight:800;color:var(--ink-3);letter-spacing:.06em;margin:0 0 8px}
.dm-bench-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-bench-tbl{width:100%;border-collapse:collapse;font-size:11.5px}
.dm-bench-tbl th{font-size:10px;font-weight:800;color:var(--ink-3);text-align:left;
                 padding:2px 10px 4px 8px;border-bottom:1px solid var(--line);
                 white-space:nowrap;vertical-align:top}
.dm-bench-tbl td{padding:5px 10px 5px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.dm-bench-tbl tr:last-child td{border-bottom:0}
.dm-bench-v{font-weight:800;color:var(--ink);white-space:nowrap}
.dm-bench-note{color:var(--ink-3);white-space:normal;max-width:28ch}

/* ── 모달 — 상위 드라이버 칩을 누르면 뜬다. 1단계(갈래)·2단계(세부)를 한 팝업에서 넘긴다 ── */
/* 「맨 위로」 버튼이 z-index 9998이라 200으로는 모달 위로 뚫고 올라왔다.
   그 위로 올리고, 모달이 떠 있는 동안에는 버튼 자체를 감춘다 */
.dm-modal-backdrop{position:fixed;inset:0;z-index:10000;display:flex;align-items:center;
                   justify-content:center;background:rgba(0,0,0,.5);padding:20px}
.dm-modal-backdrop[hidden]{display:none}
.dm-modal{position:relative;width:100%;max-width:520px;max-height:85vh;overflow-y:auto;
         background:var(--surface);border:1px solid var(--line);border-radius:10px;
         box-shadow:var(--shadow);padding:20px 20px 22px;outline:none}
.dm-modal-close{position:absolute;top:10px;right:10px;width:30px;height:30px;border-radius:50%;
                border:1px solid var(--line);background:var(--sunk);color:var(--ink-2);
                font-size:18px;line-height:1;cursor:pointer}
.dm-modal-close:hover{color:var(--ink);border-color:var(--accent)}
.dm-modal-close:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-modal-back{display:block;font:inherit;font-size:12.5px;font-weight:700;color:var(--accent);
               background:transparent;border:0;cursor:pointer;padding:2px 0;margin:0 0 10px}
.dm-modal-back:hover{text-decoration:underline}
.dm-modal-back[hidden]{display:none}
.dm-modal-gname{font-size:18px;font-weight:850;margin:4px 30px 6px 0;color:var(--ink)}
.dm-modal-q{font-size:13.5px;font-weight:700;color:var(--ink-2);margin:0 0 10px;line-height:1.5}
.dm-modal-why{font-size:13px;line-height:1.62;color:var(--ink-2);margin:0 0 10px}
.dm-modal-corpus{font-size:12.5px;line-height:1.6;color:var(--warn);
                 background:var(--warn-soft);border:1px dashed var(--warn);border-radius:8px;
                 padding:9px 11px;margin:0 0 14px}
.dm-modal-list{display:flex;flex-direction:column;gap:8px}
.dm-modal-row{display:flex;align-items:center;flex-wrap:wrap;gap:4px 10px;width:100%;
              text-align:left;font:inherit;padding:9px 10px;border:1px solid var(--line);
              border-radius:8px;background:var(--sunk);cursor:pointer}
.dm-modal-row:hover{border-color:var(--accent)}
.dm-modal-row:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-modal-row--none{border-color:var(--risk)}
.dm-modal-row-main{display:flex;flex-direction:column;gap:1px;flex:1 1 auto;min-width:120px}
.dm-modal-row-label{font-size:12.5px;font-weight:700;color:var(--ink)}
.dm-modal-row-base{font-size:11.5px;color:var(--ink-3)}
.dm-bar-mini{position:relative;display:inline-block;width:56px;height:4px;border-radius:999px;
            background:var(--line);flex:0 0 auto}
.dm-bar-mini-fill{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:var(--accent-soft)}
.dm-bar-mini-dot{position:absolute;top:50%;width:8px;height:8px;border-radius:50%;background:var(--accent);
                 border:2px solid var(--surface);transform:translate(-50%,-50%)}
.dm-modal-dname{font-size:18px;font-weight:850;margin:4px 30px 4px 0;color:var(--ink)}
.dm-modal-loc{display:block;font-size:11.5px;color:var(--ink-3);margin:0 0 12px;
             font-variant-numeric:tabular-nums}

/* ── 상세(2단계) — 예전 인라인 dm-detail의 부품을 모달 안에서 재활용한다 ── */
.dm-basebig{font-size:22px;font-weight:850;color:var(--ink);margin:0 0 14px}
.dm-basis{display:inline-block;font-size:11px;font-weight:800;padding:3px 9px;border-radius:999px;
          background:var(--surface);border:1px solid var(--line);color:var(--ink-2);margin:0 0 5px}
.dm-basis--none{background:var(--risk-soft);border-color:var(--risk);color:var(--risk)}
.dm-basis-desc{font-size:11.5px;color:var(--ink-3);margin:0 0 12px}
.dm-detail-sec{font-size:13px;line-height:1.62;color:var(--ink-2);margin:0 0 8px}
.dm-detail-sec b{color:var(--ink);font-weight:800;margin-right:2px}
.dm-detail-src{display:inline-block;margin-top:4px;font-size:12px;font-weight:700;color:var(--accent);
               text-decoration:none}
.dm-detail-src:hover{text-decoration:underline}

/* ── 범위 막대(2단계 본문) ── */
.dm-bar{margin:0 0 16px}
.dm-bar-track{position:relative;height:4px;border-radius:999px;background:var(--line);margin:10px 4px 6px}
.dm-bar-fill{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:var(--accent-soft)}
.dm-bar-dot{position:absolute;top:50%;width:12px;height:12px;border-radius:50%;background:var(--accent);
            border:2px solid var(--surface);transform:translate(-50%,-50%);box-shadow:var(--shadow)}
.dm-bar-row{display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:var(--ink-2);
            padding:0 2px}
.dm-bar-row--base{position:relative;height:15px;margin-top:2px}
.dm-bar-base-lbl{position:absolute;top:0;font-size:11px;font-weight:800;color:var(--accent-ink);
                  transform:translateX(-50%);white-space:nowrap}

/* ── 내 판정(2단계 맨 아래) — judgment.json에서 붙인 판정 ── */
.dm-jg{margin:16px 0 0;padding-top:14px;border-top:1px solid var(--line)}
.dm-jg-title{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 10px}
.dm-jg-entry{margin:0 0 16px}
.dm-jg-entry:last-child{margin-bottom:0}
.dm-jg-sub{font-size:12.5px;font-weight:800;color:var(--ink-2);margin:0 0 6px}
.dm-jg-badge{display:inline-block;font-size:11px;font-weight:850;padding:3px 10px;
             border-radius:999px;margin:0 0 8px}
.dm-jg-badge--keep{background:var(--good-soft);color:var(--good);border:1px solid var(--good)}
.dm-jg-badge--fix{background:var(--accent-soft);color:var(--accent-ink);border:1px solid var(--accent)}
.dm-jg-badge--hold{background:var(--sunk);color:var(--ink-3);border:1px solid var(--line)}
.dm-jg-badge--check{background:var(--warn-soft);color:var(--warn);border:1px solid var(--warn)}
.dm-jg-why{font-size:12.5px;line-height:1.6;color:var(--ink-2);margin:0 0 8px}
.dm-jg-mine{font-size:12.5px;line-height:1.6;color:var(--ink);margin:0 0 10px;
            padding:8px 10px;background:var(--accent-soft);border-radius:8px}
.dm-jg-mine b{font-weight:850;color:var(--accent-ink);margin-right:4px}
.dm-jg-ev{margin:0 0 10px}
.dm-jg-ev-label{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);margin:0 0 6px}
.dm-jg-ev-item{margin:0 0 8px;padding:8px 10px;background:var(--sunk);border-radius:8px}
.dm-jg-ev-item:last-child{margin-bottom:0}
.dm-jg-ev-fact{font-size:12px;line-height:1.55;color:var(--ink);margin:0 0 3px}
.dm-jg-ev-src{display:inline-block;font-size:10.5px;color:var(--ink-3);text-decoration:none}
.dm-jg-ev-src:hover{color:var(--accent-ink);text-decoration:underline}
.dm-jg-ev-src--nolink{cursor:default}
.dm-jg-ev-src--nolink:hover{color:var(--ink-3);text-decoration:none}
.dm-jg-extra{font-size:12px;line-height:1.55;color:var(--ink-2);margin:0 0 6px}
.dm-jg-extra b{color:var(--ink);font-weight:800;margin-right:4px}

/* ── 판정 배지(1단계 세부 드라이버 목록 줄) ── */
.dm-jg-rowbadge{display:inline-block;font-size:9.5px;font-weight:850;padding:1px 7px;
                border-radius:999px;margin-left:2px;white-space:nowrap}
.dm-jg-rowbadge--keep{background:var(--good-soft);color:var(--good)}
.dm-jg-rowbadge--fix{background:var(--accent-soft);color:var(--accent-ink)}
.dm-jg-rowbadge--hold{background:var(--sunk);color:var(--ink-3);border:1px solid var(--line)}
.dm-jg-rowbadge--check{background:var(--warn-soft);color:var(--warn)}

/* ── 「아직 판정 못한 것」 — 드라이버 범위 표 다음 ── */
.dm-jgtodo{margin:20px 0 0;background:var(--surface);border:1px dashed var(--line);
          border-radius:10px;padding:12px 15px;box-shadow:var(--shadow)}
.dm-jgtodo-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:0 0 8px}
.dm-jgtodo-date{font-weight:700;color:var(--ink-3);margin-left:6px;font-size:11px}
.dm-jgtodo-list{margin:0;padding-left:18px}
.dm-jgtodo-list li{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 4px}
.dm-jgtodo-list li:last-child{margin-bottom:0}

/* 모달 열린 동안 배경 스크롤을 막는다 */
body.dm-modal-open{overflow:hidden}
body.dm-modal-open .ui-top{opacity:0;pointer-events:none}

@media (max-width:560px){
  .dm-wrap{margin:0 0 24px;padding-bottom:20px}
  /* 좁은 화면에선 가운데 정렬 모달이 답답하다 — 아래에서 올라오는 시트로 바꾼다 */
  .dm-modal-backdrop{align-items:flex-end;padding:0}
  .dm-modal{max-width:100%;border-radius:16px 16px 0 0;max-height:88vh;padding:18px 16px 20px}
}
</style>'''


DM_JS = '''<script>
(function(){
  var el = document.getElementById('dm-data');
  if(!el) return;
  var DATA = JSON.parse(el.textContent);
  var backdrop = document.getElementById('dm-modal-backdrop');
  var modal = document.getElementById('dm-modal');
  var closeBtn = document.getElementById('dm-modal-close');
  var backBtn = document.getElementById('dm-modal-back');
  var bodyEl = document.getElementById('dm-modal-body');
  if(!backdrop || !modal) return;

  var state = {gid:null, members:null, driver:null, noback:false, trigger:null};

  function fmtNum(v){
    var s = (Math.round(v*100)/100).toString();
    return s;
  }

  function fmtBar(bar){
    var lo=bar[0], base=bar[1], hi=bar[2], unit=bar[3];
    function f(v){ return fmtNum(v)+unit; }
    var span = hi-lo;
    var pct = span===0 ? 50 : (base-lo)/span*100;
    pct = Math.max(0, Math.min(100, pct));
    var clamped = Math.max(8, Math.min(92, pct));
    var row1, row2;
    if(lo===base && base===hi){
      row1 = '<span></span><span></span>';
      row2 = '<span class="dm-bar-base-lbl" style="left:50%">'+f(base)+' (고정)</span>';
    } else if(lo===base){
      row1 = '<span></span><span>'+f(hi)+'</span>';
      row2 = '<span class="dm-bar-base-lbl" style="left:'+clamped+'%">'+f(lo)+' = 기준</span>';
    } else if(base===hi){
      row1 = '<span>'+f(lo)+'</span><span></span>';
      row2 = '<span class="dm-bar-base-lbl" style="left:'+clamped+'%">기준 = '+f(hi)+'</span>';
    } else {
      row1 = '<span>'+f(lo)+'</span><span>'+f(hi)+'</span>';
      row2 = '<span class="dm-bar-base-lbl" style="left:'+clamped+'%">'+f(base)+' 기준</span>';
    }
    var track = '<div class="dm-bar-track"><span class="dm-bar-fill" style="width:'+pct+'%"></span>'
              + '<span class="dm-bar-dot" style="left:'+pct+'%"></span></div>';
    return '<div class="dm-bar">'+track
         + '<div class="dm-bar-row">'+row1+'</div>'
         + '<div class="dm-bar-row--base">'+row2+'</div></div>';
  }

  function fmtBarMini(bar){
    var lo=bar[0], base=bar[1], hi=bar[2];
    var span = hi-lo;
    var pct = span===0 ? 50 : (base-lo)/span*100;
    pct = Math.max(0, Math.min(100, pct));
    return '<span class="dm-bar-mini"><span class="dm-bar-mini-fill" style="width:'+pct+'%"></span>'
         + '<span class="dm-bar-mini-dot" style="left:'+pct+'%"></span></span>';
  }

  function focusModal(){
    requestAnimationFrame(function(){ modal.focus(); });
  }

  var JG_CLASS = {'유지':'keep', '수정':'fix', '보류':'hold', '확인필요':'check'};

  function fmtJgBadges(verdicts){
    if(!verdicts || !verdicts.length) return '';
    return verdicts.map(function(v){
      var cls = JG_CLASS[v] || 'hold';
      return '<span class="dm-jg-rowbadge dm-jg-rowbadge--'+cls+'">'+v+'</span>';
    }).join('');
  }

  // 「내 판정」 칸(2단계 맨 아래). 데이터는 파이썬이 구조화해 넘기고 HTML은 여기서 만든다.
  function fmtJgEvidence(groups){
    if(!groups || !groups.length) return '';
    return groups.map(function(g){
      var items = g.items.map(function(it){
        var src = it.url
          ? '<a class="dm-jg-ev-src" href="'+it.url+'" target="_blank" rel="noopener">'
            +it.note+' · '+it.cite+' ▸</a>'
          : '<span class="dm-jg-ev-src dm-jg-ev-src--nolink">'+it.note+' · '+it.cite+'</span>';
        return '<div class="dm-jg-ev-item"><p class="dm-jg-ev-fact">'+it.fact+'</p>'+src+'</div>';
      }).join('');
      return '<div class="dm-jg-ev"><p class="dm-jg-ev-label">'+g.label+'</p>'+items+'</div>';
    }).join('');
  }

  function fmtJgExtra(extra){
    if(!extra || !extra.length) return '';
    return extra.map(function(e){
      return '<p class="dm-jg-extra"><b>'+e.label+'</b>'+e.text+'</p>';
    }).join('');
  }

  function fmtJudgment(entries){
    if(!entries || !entries.length) return '';
    var body = entries.map(function(v){
      var cls = JG_CLASS[v.verdict] || 'hold';
      var sub = v.label ? '<p class="dm-jg-sub">'+v.label+'</p>' : '';
      var badge = '<span class="dm-jg-badge dm-jg-badge--'+cls+'">'+v.verdict+'</span>';
      var why = v.why ? '<p class="dm-jg-why">'+v.why+'</p>' : '';
      var mine = v.mine ? '<p class="dm-jg-mine"><b>내가 대신 보는 값</b>'+v.mine+'</p>' : '';
      return '<div class="dm-jg-entry">'+sub+badge+why+mine
           + fmtJgEvidence(v.evidence)+fmtJgExtra(v.extra)+'</div>';
    }).join('');
    return '<div class="dm-jg"><p class="dm-jg-title">내 판정</p>'+body+'</div>';
  }

  function renderStage1(){
    var g = DATA.groups[state.gid];
    if(!g) return;
    var rows = state.members.map(function(did){
      var d = DATA.drivers[did];
      if(!d) return '';
      var noneCls = d.basisKey === 'none' ? ' dm-modal-row--none' : '';
      var basisNoneCls = d.basisKey === 'none' ? ' dm-basis--none' : '';
      return '<button type="button" class="dm-modal-row'+noneCls+'" data-driver="'+did+'">'
           + '<span class="dm-modal-row-main">'
           +   '<span class="dm-modal-row-label">'+d.label+fmtJgBadges(d.judgmentVerdicts)+'</span>'
           +   '<span class="dm-modal-row-base">'+d.base+'</span>'
           + '</span>'
           + (d.bar ? fmtBarMini(d.bar) : '')
           + '<span class="dm-basis'+basisNoneCls+'">'+d.basisLabel+'</span>'
           + '</button>';
    }).join('');
    bodyEl.innerHTML =
        '<h3 id="dm-modal-title" class="dm-modal-gname" tabindex="-1">'+g.name+'</h3>'
      + '<p class="dm-modal-q">'+g.q+'</p>'
      + '<p class="dm-detail-sec">'+g.why+'</p>'
      + '<div class="dm-modal-corpus">'+g.corpus+'</div>'
      + '<div class="dm-modal-list">'+rows+'</div>';
    backBtn.hidden = true;
    focusModal();
  }

  function renderStage2(){
    var d = DATA.drivers[state.driver];
    if(!d) return;
    var barHtml = d.bar ? fmtBar(d.bar) : '<div class="dm-basebig">'+d.base+'</div>';
    var noneCls = d.basisKey === 'none' ? ' dm-basis--none' : '';
    bodyEl.innerHTML =
        '<h3 id="dm-modal-title" class="dm-modal-dname" tabindex="-1">'+d.label+'</h3>'
      + '<span class="dm-modal-loc">'+d.axisMeta+' · '+d.doc+'</span>'
      + barHtml
      + '<span class="dm-basis'+noneCls+'">'+d.basisLabel+'</span>'
      + '<p class="dm-basis-desc">'+d.basisDesc+'</p>'
      + '<p class="dm-detail-sec"><b>왜</b>'+d.why+'</p>'
      + '<p class="dm-detail-sec"><b>영향</b>'+d.impact+'</p>'
      + '<a class="dm-detail-src" href="'+d.url+'" target="_blank" rel="noopener">출처: 요약본 L'+d.line+' ▸</a>'
      + fmtJudgment(d.judgment);
    backBtn.hidden = state.noback || !state.gid;
    focusModal();
  }

  function showModal(trigger){
    state.trigger = trigger || null;
    backdrop.hidden = false;
    document.body.classList.add('dm-modal-open');
  }

  function closeModal(){
    if(backdrop.hidden) return;
    backdrop.hidden = true;
    document.body.classList.remove('dm-modal-open');
    var t = state.trigger;
    state = {gid:null, members:null, driver:null, noback:false, trigger:null};
    if(t && typeof t.focus === 'function') t.focus();
  }

  function openGroup(gid, members, trigger){
    state.gid = gid; state.members = members; state.driver = null; state.noback = false;
    showModal(trigger);
    renderStage1();
  }

  function openDriverFromGroup(did){
    state.driver = did; state.noback = false;
    renderStage2();
  }

  function openDriverDirect(did, trigger){
    state.gid = null; state.members = null; state.driver = did; state.noback = true;
    showModal(trigger);
    renderStage2();
  }

  function backToStage1(){
    if(!state.gid) return;
    state.driver = null;
    renderStage1();
  }

  document.addEventListener('click', function(e){
    var gchip = e.target.closest('.dm-gchip');
    if(gchip){ openGroup(gchip.dataset.group, gchip.dataset.members.split(','), gchip); return; }

    var mrow = e.target.closest('.dm-modal-row');
    if(mrow){ openDriverFromGroup(mrow.dataset.driver); return; }

    var direct = e.target.closest('[data-driver][data-noback]');
    if(direct){ openDriverDirect(direct.dataset.driver, direct); return; }

    if(e.target === closeBtn || e.target.closest('#dm-modal-close')){ closeModal(); return; }
    if(e.target === backBtn || e.target.closest('#dm-modal-back')){ backToStage1(); return; }
    if(e.target === backdrop){ closeModal(); return; }

    var tl = e.target.closest('.dm-tl-item');
    if(tl && tl.dataset.target){
      var t = document.getElementById(tl.dataset.target);
      if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });

  document.addEventListener('keydown', function(e){
    if(e.key==='Enter' || e.key===' '){
      var tl = e.target.closest('.dm-tl-item');
      if(tl && tl.dataset.target){
        e.preventDefault();
        var t = document.getElementById(tl.dataset.target);
        if(t) t.scrollIntoView({behavior:'smooth', block:'start'});
        return;
      }
    }
    if(backdrop.hidden) return;
    if(e.key === 'Escape'){ closeModal(); return; }
    if(e.key === 'Tab'){
      var focusables = Array.prototype.slice.call(
        modal.querySelectorAll('button, a[href], [tabindex]:not([tabindex="-1"])')
      ).filter(function(n){ return !n.disabled && n.offsetParent !== null; });
      if(!focusables.length) return;
      var first = focusables[0], last = focusables[focusables.length-1];
      if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  });
})();
</script>'''


AXBTN_JS = '''<script>
(function(){
  var wrap = document.getElementById('dm-axisbtns');
  if(!wrap) return;
  var btns = Array.prototype.slice.call(wrap.querySelectorAll('.dm-axisbtn'));

  function select(id){
    btns.forEach(function(b){
      b.setAttribute('aria-pressed', b.dataset.axis === id ? 'true' : 'false');
    });
    document.querySelectorAll('.dm-axispanel').forEach(function(p){
      p.hidden = (p.id !== 'dm-axispanel-' + id);
    });
  }

  wrap.addEventListener('click', function(e){
    var b = e.target.closest('.dm-axisbtn');
    if(!b) return;
    select(b.dataset.axis);
  });

  wrap.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var idx = btns.indexOf(document.activeElement);
    if(idx === -1) return;
    e.preventDefault();
    var next = e.key === 'ArrowRight' ? (idx + 1) % btns.length
                                       : (idx - 1 + btns.length) % btns.length;
    btns[next].focus();
  });
})();
</script>'''

# 다섯 방법을 보여줄 순서. dcf(03)가 가장 완전한 평가라 기본으로 연다.
_AXIS_BTN_ORDER = ['stmt', 'simple', 'dcf', 'rev', 'mult']
_AXIS_BTN_DEFAULT = 'dcf'


def _axis_buttons_html():
    axes_by_id = {ax['id']: ax for ax in dmd.AXES}
    btns = []
    for aid in _AXIS_BTN_ORDER:
        ax = axes_by_id[aid]
        pressed = 'true' if aid == _AXIS_BTN_DEFAULT else 'false'
        btns.append(
            '<button type="button" class="dm-axisbtn" id="dm-axisbtn-%s" data-axis="%s" '
            'aria-pressed="%s" aria-controls="dm-axispanel-%s">'
            '<span class="dm-axisbtn-no">%s</span>'
            '<span class="dm-axisbtn-name">%s</span>'
            '<span class="dm-axisbtn-date">%s</span>'
            '</button>' % (aid, aid, pressed, aid, ax['no'], ax['name'], ax['latest'][1]))
    return '<div class="dm-axisbtns" id="dm-axisbtns">%s</div>' % ''.join(btns)


def _axis_panels_html():
    axes_by_id = {ax['id']: ax for ax in dmd.AXES}
    parts = []
    for aid in _AXIS_BTN_ORDER:
        ax = axes_by_id[aid]
        hidden = '' if aid == _AXIS_BTN_DEFAULT else ' hidden'
        parts.append(
            '<div class="dm-axispanel" id="dm-axispanel-%s" role="tabpanel" '
            'aria-labelledby="dm-axisbtn-%s"%s>%s</div>'
            % (aid, aid, hidden, _axis_html(ax)))
    return '<div class="dm-axispanels">%s</div>' % ''.join(parts)


def render():
    data_json = json.dumps(_data_json(), ensure_ascii=False).replace('</', '<\\/')
    parts = [DM_CSS]
    parts.append('<div class="dm-wrap">')
    parts.append('<div class="dm-head"><h2 class="dm-title">드라이버 지도 — 무엇을 얼마로 가정했나</h2>'
                  '<p class="dm-lede">%s</p></div>' % dmd.LEDE)
    parts.append(_scenario_html())
    # 드라이버 범위 표(_ranges_html)는 걷어냈다. 같은 내용이 각 드라이버 상세의
    # 「영향」 칸에 들어 있어 두 번 말하는 셈이었다.
    # 연도별 이익 경로 표는 DCF 축 패널 안으로 옮겼다 — 연도별 추정이 그 방법의
    # 본체라서다. 07-16 민감도 격자도 같은 이유로 그 패널 안에 있다.
    parts.append('<h2 class="dm-axheading">엘곰이 한 것 — 방법을 고르면 그 방법의 최신 글이 열린다</h2>')
    parts.append(_axis_buttons_html())
    parts.append(_axis_panels_html())
    parts.append(_judgment_todo_html(_JUDGMENT_TODO, _JUDGMENT_ASOF))
    parts.append(
        '<details class="dm-past">'
        '<summary class="dm-past-summary">지난 평가 — 열다섯 달 동안 여섯 번, 값이 어떻게 움직였나</summary>'
        '<div class="dm-past-body">%s</div>'
        '</details>' % _timeline_html())
    parts.append(
        '<div class="dm-modal-backdrop" id="dm-modal-backdrop" hidden>'
        '<div class="dm-modal" id="dm-modal" role="dialog" aria-modal="true" '
        'aria-labelledby="dm-modal-title" tabindex="-1">'
        '<button type="button" class="dm-modal-close" id="dm-modal-close" aria-label="닫기">×</button>'
        '<button type="button" class="dm-modal-back" id="dm-modal-back" hidden>← 뒤로</button>'
        '<div id="dm-modal-body"></div>'
        '</div></div>')
    parts.append('</div>')
    parts.append('<script type="application/json" id="dm-data">%s</script>' % data_json)
    parts.append(DM_JS)
    parts.append(AXBTN_JS)
    return '\n'.join(parts)


if __name__ == '__main__':
    out = render()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print('OK: 렌더 길이 %d자 / 축 %d개 / 상위칩 %d개 / 드라이버 %d개'
          % (len(out), len(dmd.AXES), out.count('class="dm-gchip"'), len(dmd.DRIVERS)))
    n_ok = sum(1 for _n, _c, ok in _RESOLVE_LOG if ok)
    n_fail = len(_RESOLVE_LOG) - n_ok
    print('판정 붙은 드라이버 %d개 / 인용 링크 해석 %d건 성공, %d건 실패'
          % (len(_JUDGMENTS), n_ok, n_fail))
    if n_fail:
        for _n, _c, ok in _RESOLVE_LOG:
            if not ok:
                print('  실패: %s / %s' % (_n, _c))
    print('아직 판정 못한 것 %d건 (dm-sn 위치: dcf 패널 안)' % len(_JUDGMENT_TODO))
