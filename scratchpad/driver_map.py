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
import glob, io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_common as dc
import driver_map_data
# 기본값(삼성전자). render(data=...)가 호출되면 그 데이터 모듈로 다시 잡는다 —
# 아래 모든 헬퍼 함수는 이 전역 dmd를 통해서만 데이터에 접근한다.
dmd = driver_map_data

sys.path.insert(0, os.path.join(dc.ROOT, 'insights'))
import notes_lib as nl  # noqa: E402

# 수식 사슬 안의 {드라이버id} 를 이제는 텍스트로 바꾼다 — 수식은 읽는 것이지 누르는 것이
# 아니다. str.format을 쓰지 않는 건 수식에 (1+...) 같은 괄호가 있어서 format의 {}와
# 충돌하기 때문이다.
_CHIP_RE = re.compile(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}')


def _chain_label(driver_id, repeat=False):
    """수식 한 자리. 이름만 있으면 값을 보려고 아래 칩을 눌러야 한다 —
    수식이 무슨 계산인지는 알려 주는데 결과가 어떤 자릿수인지는 안 알려 준다.
    그래서 이름 옆에 값을 같이 박는다. base가 긴 드라이버는 short를 쓴다.

    한 줄에 같은 드라이버가 여러 번 나오면(영구가치 줄의 할인율이 세 번)
    두 번째부터는 값만 남긴다. 이름까지 세 번 적으면 수식이 안 읽힌다."""
    d = dmd.DRIVERS[driver_id]
    val = d.get('short', d['base'])
    if repeat:
        return '<b class="dm-chain-val">%s</b>' % val
    return ('<span class="dm-chain-driver">'
            '<span class="dm-chain-name">%s</span>'
            '<b class="dm-chain-val">%s</b></span> ' % (d['label'], val))


def _linkify(line):
    seen = set()

    def one(m):
        did = m.group(1)
        html = _chain_label(did, repeat=did in seen)
        seen.add(did)
        return html

    return _CHIP_RE.sub(one, line)


def _by_badge(key):
    """누가 낸 값인가 배지. 내 계산(ours)을 필자 주장으로 읽지 않게 값마다 붙인다."""
    label, desc = dmd.BY[key]
    return '<span class="dm-by dm-by--%s" title="%s">%s</span>' % (key, desc, label)


# ── 내 판정 (insights/valuation/<judgment_dir>/judgment.json) ──────
# 이 파일은 종목마다 있을 수도 없을 수도 있다. 없거나 깨졌으면 조용히 건너뛴다 —
# 예외를 던지면 이 파일이 없는 다른 종목 대시보드까지 죽는다.
# render()가 호출될 때마다 그 회사의 judgment_dir로 다시 잡는다. 기본값은 삼성전자 폴더다.
_JUDGMENT_PATH = None
_NOTES_DIR = os.path.join(dc.ROOT, 'insights', 'notes')

_VERDICT_CLASS = {'유지': 'keep', '수정': 'fix', '보류': 'hold', '확인필요': 'check'}

# 지도 뿌리 요소의 접두어. 회사별로 갈라 한 페이지에 지도 두 개가 있어도 id가 안 부딪히게 한다.
# render()가 호출될 때마다 데이터 모듈 이름에서 다시 뽑는다.
_PX = 'ss'


def _prefix_for(data):
    """데이터 모듈 이름에서 접두어를 뽑는다. driver_map_data → 'ss'(기본·삼성전자),
    driver_map_data_hynix → 'hynix'. 값을 손으로 안 붙여도 되게 모듈명에서 뽑는다."""
    name = getattr(data, '__name__', '') or ''
    tail = name.rsplit('driver_map_data', 1)[-1].strip('_')
    return tail or 'ss'

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
    if not _JUDGMENT_PATH:
        return {}, None, []
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


# render()가 호출될 때마다 그 회사의 judgment_dir로 다시 채운다. 모듈을 처음 불러온 시점에는
# 빈 상태 — render()를 거치지 않고 이 아래 함수들을 직접 부르는 코드는 없다.
_JUDGMENTS, _JUDGMENT_ASOF, _JUDGMENT_TODO = {}, None, []


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


def _judgment_inline_html(did):
    """내 판정. 모달에 있던 것을 지면으로 내린다 — 이 페이지에는 눌러서 여는 것이 없다."""
    entries = _JUDGMENTS.get(did)
    if not entries:
        return ''
    show_label = len(entries) > 1
    out = []
    for v in entries:
        vd = v.get('verdict') or ''
        cls = _VERDICT_CLASS.get(vd, 'check')
        lab = ('<span class="dm-dv-jglabel">%s</span>' % v['label']) if (show_label and v.get('label')) else ''
        why = ('<span class="dm-dv-jgwhy">%s</span>' % v['why']) if v.get('why') else ''
        mine = ('<p class="dm-dv-jgmine"><b>주인장이 대신 보는 값</b> %s</p>' % v['mine']) if v.get('mine') else ''
        out.append('<div class="dm-dv-jgitem">%s<span class="dm-dv-jgbadge dm-dv-jgbadge--%s">%s</span>%s%s</div>'
                   % (lab, cls, vd, why, mine))
    return ('<div class="dm-dv-jg"><p class="dm-dv-jgtitle">주인장 판정 %s</p>%s</div>'
            % (_by_badge('ours'), ''.join(out)))


# render()가 호출될 때마다 그 회사의 GROUPS로 다시 채운다 (아래 참조).
_GROUP_OF = {}


def _driver_cells(did):
    """드라이버 한 개를 열 하나로 낸다 — (이름, 값, 근거, 설명).

    가로가 드라이버, 세로가 항목이다. 값이 여럿일 때 「얼마」끼리 한 줄에 서야
    서로 견줘진다. 세로로 쌓으면 값 하나를 보려고 설명 문단을 건너뛰어야 한다."""
    d = dmd.DRIVERS[did]
    basis_label, basis_desc = dmd.BASIS[d['basis']]
    name = d['label']
    basis = ('<span class="dm-basis%s" title="%s">%s</span>'
             % (' dm-basis--none' if d['basis'] == 'none' else '', basis_desc, basis_label))
    why = ('%s<span class="dm-dvt-impact"><b>그래서</b> %s</span>%s'
           % (d['why'], d['impact'], _judgment_inline_html(did)))
    return name, d['base'], basis, why, d['basis'] == 'none'


def _drivers_table_html(dids):
    """열은 둘뿐이다 — 왼쪽이 항목, 오른쪽이 내용. 드라이버는 위에서 아래로 쌓인다.

    네 열로 늘어놓으면 설명 칸이 좁아 문장이 세로로 흘렀고, 가로로 뒤집으면 한 항목을
    보려고 옆으로 밀어야 했다. 두 열이면 좁은 화면에서도 가로 스크롤이 없다(2026-08-19)."""
    out, cur = [], None
    for did in dids:
        # 묶음(「이익 수준」 같은 상위 갈래)은 드라이버 이름 옆 알약이 아니라 그 묶음이
        # 시작하는 자리의 머리줄로 낸다. 알약으로 붙이면 이름과 같은 층으로 읽히는데
        # 실제로는 드라이버 여럿을 덮는 위 칸이다(2026-08-19 화면에서 지적).
        grp = _GROUP_OF.get(did, '')
        if grp and grp != cur:
            out.append('<tr class="dm-dvt-grp"><th colspan="2">%s</th></tr>' % grp)
        cur = grp
        name, val, basis, why, is_none = _driver_cells(did)
        cls = ' class="dm-dv--none"' if is_none else ''
        out.append('<tr class="dm-dvt-head"%s><th colspan="2">%s</th></tr>'
                   '<tr><th scope="row">얼마</th><td class="dm-dvt-val">%s</td></tr>'
                   '<tr><th scope="row">근거</th><td>%s</td></tr>'
                   '<tr><th scope="row">왜</th><td class="dm-dvt-why">%s</td></tr>'
                   % (cls, name, val, basis, why))
    # table-layout:fixed는 첫 행으로 열 폭을 정하는데 첫 행이 colspan=2라 폭을 못 읽고
    # 반반으로 갈랐다. colgroup으로 못 박는다(2026-08-19 화면에서 첫 열이 절반이었다).
    return ('<div class="dm-dvt-wrap"><table class="dm-dvt">'
            '<colgroup><col class="dm-dvt-c1"><col></colgroup>'
            '<tbody>%s</tbody></table></div>' % ''.join(out))


def _driver_block_html(did):
    """옛 이름 — 드라이버 하나짜리 표를 낸다. 부르는 자리가 남아 있어 이름을 지키다."""
    return _drivers_table_html([did])


def _doc_gist(key):
    """그 글이 무엇을 주장하는지 한 문장. 노트의 「이 문서가 주장하는 것」 첫 문장이다."""
    src = dmd.DOCS.get(key, '')
    for path in glob.glob(os.path.join(_NOTES_DIR, '*.md')):
        try:
            t = io.open(path, encoding='utf-8').read()
        except Exception:
            continue
        if src and src in t:
            m = re.search(r'## 이 문서가 주장하는 것\n+(.+?)(?:\n|$)', t)
            if not m:
                return ''
            first = re.match(r'^(.+?다[.])', m.group(1).strip())
            return (first.group(1) if first else m.group(1).strip())[:190]
    return ''


def _doc_title(key):
    """DOCS 파일명에서 제목만 뽑는다. 「[260716] 제목 - 삼성전자 - 엘곰.md」 꼴이다."""
    name = dmd.DOCS.get(key, '')
    name = re.sub(r'^\[\d{6}\]\s*', '', name)
    name = re.sub(r'\.md$', '', name)
    name = re.sub(r'\s*-\s*엘곰$', '', name)
    return name


def _driver_table_html(ax):
    """그 방법이 쓴 값을 글마다 갈라서 지면에 편다.

    한 방법에 글이 여럿인 축이 있다. 재무제표(그때)는 여섯 편, 멀티플은 세 편이다.
    전에는 갈래(이익 수준·재투자…)로만 묶어서, 2024년 글의 값과 2026년 글의 값이
    한 줄기로 섞였다. 글이 둘 이상이면 날짜 탭으로 가른다 — 한 탭이 한 편이다.

    갈래는 값마다 작은 꼬리표로 남긴다. 묶음 축이 아니라 표시로 내린 것이다."""
    by_doc = {}
    for did, d in dmd.DRIVERS.items():
        if d['axis'] != ax['id']:
            continue
        by_doc.setdefault(d['doc'], []).append(did)
    if not by_doc:
        return ''
    # 최신이 맨 왼쪽이다. 지금 유효한 값이 무엇인지부터 보여야 하고, 오래된 편을
    # 먼저 세우면 첫 탭이 늘 옛날 숫자가 된다(2026-08-19 지적).
    keys = sorted(by_doc, reverse=True)

    def panel(k, hidden):
        gist = _doc_gist(k)
        url = dc.blob(dmd.SUM + dmd.DOCS[k])
        # id는 회사 접두어까지 넣어 두지만(HTML 중복 id 방지), 탭 전환 JS는 이제 data-axis·
        # data-doc만 본다 — id 문자열을 다시 조립할 필요가 없어 접두어를 JS에 넘길 일도 없다.
        return ('<div class="dm-dvdoc" id="dm-%s-dvdoc-%s-%s" data-axis="%s" data-doc="%s"%s>'
                '<p class="dm-dvdoc-title">%s '
                '<a class="dm-dvdoc-src" href="%s" target="_blank" rel="noopener">요약본 ▸</a></p>'
                '%s%s</div>'
                % (_PX, ax['id'], k, ax['id'], k, ' hidden' if hidden else '',
                   _doc_title(k), url,
                   ('<p class="dm-dvdoc-gist">%s</p>' % gist) if gist else '',
                   _drivers_table_html(by_doc[k])))

    if len(keys) == 1:
        body = panel(keys[0], False)
        tabs = ''
    else:
        tabs = ('<div class="dm-dvtabs" role="tablist">%s</div>' % ''.join(
            '<button type="button" class="dm-dvtab" role="tab" data-axis="%s" data-doc="%s" '
            'aria-selected="%s">%s<span class="dm-dvtab-n">%d</span></button>'
            % (ax['id'], k, 'true' if i == 0 else 'false', _doc_date(k), len(by_doc[k]))
            for i, k in enumerate(keys)))
        body = ''.join(panel(k, i > 0) for i, k in enumerate(keys))
    return ('<div class="dm-dvwrap"><p class="dm-dvwrap-label">무엇을 얼마로 놓았나 %s</p>'
            '%s%s</div>' % (_by_badge('author'), tabs, body))


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


# 방법이 무엇인지 모르면 표를 봐도 무엇을 견주는지 알 수 없다. 축마다 한 문단으로 붙인다.
# 「무엇을 가정하나 → 어떻게 값이 나오나 → 어디서 틀리나」 세 조각이다. 값이 아니라 정의라
# 회사와 무관하고, 데이터 모듈이 아니라 렌더러가 갖는다.
HOWTO = {
    'dcf': ('현금흐름할인법',
            '앞으로 회사가 벌어들일 현금을 해마다 추정하고, 그 돈을 지금 값으로 깎아 더한다. '
            '깎는 비율이 할인율(WACC)이고, 추정 기간이 끝난 뒤의 값은 영구성장률로 한 덩어리로 묶는다.',
            '틀리는 자리는 대개 앞 몇 해의 마진이다. 할인율을 1%p 흔드는 것보다 마진 가정을 '
            '10%p 낮추는 쪽이 값을 훨씬 크게 움직인다.'),
    'simple': ('간이 현금흐름할인법',
               '해마다의 매출·마진을 따로 깔지 않고, 최근 잉여현금흐름 하나에 성장률과 할인율만 '
               '얹어 값을 낸다. 계산이 짧아 가정이 몇 개 안 되는 만큼 가정 하나가 결과를 다 정한다.',
               '성장률을 몇 %로 놓느냐가 사실상 결론이다. 사이클이 있는 회사에서는 어느 해의 '
               '현금흐름을 출발점으로 쓰느냐도 같은 무게를 갖는다.'),
    'rev': ('역산',
            '값을 내는 대신 반대로 묻는다. 지금 시가총액이 옳다면 회사가 앞으로 얼마를 벌어야 '
            '하는지를 되돌려 푼다. 나온 숫자를 컨센서스나 과거 실적과 견주면 지금 가격이 무엇을 '
            '전제하고 있는지가 보인다.',
            '역산은 적정가를 내지 않는다. 「이 가격이 요구하는 이익」이 현실적인지는 사람이 판단한다.'),
    'stmt': ('재무제표 분석',
             '손익계산서·재무상태표·현금흐름표에서 마진, 자본 효율, 부채, 운전자본 같은 지표를 뽑아 '
             '회사의 지금 상태를 잰다. 값을 매기는 방법이 아니라 값을 매기기 전에 재는 자다.',
             '지표는 대개 최근 12개월이나 최근 분기 값이다. 사이클 꼭대기에서 잰 수익성은 그 자체로 '
             '미래를 말해 주지 않는다.'),
    'mult': ('멀티플',
             'PER·PBR·EV/EBITDA처럼 이익이나 자산에 몇 배를 쳐 주는지로 값을 잰다. 같은 업종의 '
             '다른 회사와 견주기 쉬워 가장 널리 쓰인다.',
             '배수가 낮다고 싼 것이 아니다. 분모(이익)가 꼭대기면 낮은 배수가 오히려 정점 신호일 수 '
             '있다. 그래서 이익이 얼마나 오래 갈지를 같이 봐야 한다.'),
}


def _howto_html(axis_id):
    """이 방법이 무엇인지 — 표를 읽기 전에 필요한 정의."""
    spec = HOWTO.get(axis_id)
    if not spec:
        return ''
    name, what, risk = spec
    return ('<details class="dm-howto"><summary>%s — 어떤 방법인가</summary>'
            '<p class="dm-howto-p">%s</p>'
            '<p class="dm-howto-p dm-howto-risk"><b>어디서 틀리나</b> %s</p>'
            '</details>' % (name, what, risk))


def _axis_html(ax):
    # 역산(rev)은 방향이 반대다 — 가격이 출력이 아니라 입력이다. 그래서 셋과
    # 같은 「적정가」 줄에 세우지 않고, 테두리·머리 색·결과 라벨을 다르게 그린다.
    is_rev = ax.get('kind') == 'reverse'
    axis_cls = 'dm-axis dm-axis--reverse' if is_rev else 'dm-axis'
    latest_html = _axis_latest_html(ax)

    inputs_html = ''
    if ax.get('inputs'):
        rows = []
        for k, v in ax['inputs']:
            rows.append('<tr><td class="dm-inputs-k">%s</td>'
                        '<td class="dm-inputs-v">%s</td></tr>' % (k, v))
        inputs_html = ('<div class="dm-inputs"><p class="dm-inputs-label">입력</p>'
                       '<div class="dm-inputs-wrap"><table class="dm-inputs-tbl">'
                       '<thead><tr><th>입력</th><th>값</th></tr></thead>'
                       '<tbody>%s</tbody></table></div></div>' % ''.join(rows))

    # 수식 사슬은 접는다. 표를 보고 값을 확인한 다음에야 「그 값이 어떤 식으로 나왔나」를
    # 묻게 되는데, 펼쳐 두면 표 바로 아래 수식 대여섯 줄이 깔려 다음 절이 화면 밖으로
    # 밀려난다(2026-08-19 화면에서 지적).
    chain_html = ''.join('<p class="dm-chain-line">%s</p>' % _linkify(c) for c in ax['chain'])
    gchips_html = _driver_table_html(ax)

    # 축 머리에 찍힌 최신 글 날짜와 그 축이 실제로 쓰는 드라이버의 날짜가 어긋나는
    # 축이 있다. 칩을 누르기 전에 알려 준다 — 누른 뒤에 알면 이미 숫자를 읽은 뒤다.
    stale_html = ''
    if _axis_is_stale(ax['id']):
        docs = _axis_driver_docs(ax['id'])
        span = (_doc_date(docs[0]) if docs[0] == docs[-1]
                else '%s ~ %s' % (_doc_date(docs[0]), _doc_date(docs[-1])))
        stale_html = ('<div class="dm-axis-stale">'
                      '<span class="dm-axis-stale-tag">옛 값</span>'
                      '<span class="dm-axis-stale-text">이 축의 드라이버는 전부 '
                      '%s 값이다. %s</span></div>' % (span, dmd.STALE_WHY))

    out_tag = '이 주가를 유지하려면 필요한 것' if is_rev else '결과'
    # 결과 값도 눌러서 여는 버튼이었다. 이 페이지에는 눌러서 나오는 것을 두지 않는다.
    out_html = ('<div class="dm-axis-out"><span class="dm-axis-out-tag">%s</span>'
                '<span class="dm-axis-out-val">%s</span></div>' % (out_tag, ax['out']))

    # 07-16 민감도 25칸 격자는 그 글이 낸 DCF 축 자료다. 드라이버 범위·이익 경로 표와
    # 달리 다섯 축을 가로지르지 않으므로 패널 밖에 두면 어느 글 것인지 안 보인다.
    # dcf 축에만, 수식→칩→결과 다음 자리에 끼운다.
    # 글마다 자기 연도별 표를 갖는다. 07-16 8년 추정은 DCF 축에, 02-26의 두
    # 성장 경로는 역산 축에. 둘 다 원문 표 그대로다.
    # 평가가 여러 편인 회사(삼성전자)만 이 표들을 갖는다. 평가가 한 편뿐인 회사는
    # DCF_PATH·SENSITIVITY·REV_PATH가 없을 수 있다 — 없으면 조용히 건너뛴다.
    # 주인장 계산은 지도 맨 위에 따로 서 있었다. 방법과 떼어 놓으면 「그가 쓴 값」과
    # 「내가 돌린 값」이 다른 층으로 읽혀 같은 DCF를 두 번 설명하는 모양이 된다.
    # DCF 축 안에 버튼으로 넣는다 — 기본은 접혀 있고 누르면 펴진다.
    owner_html = ''
    if ax['id'] == 'dcf' and getattr(dmd, 'SCENARIOS', None):
        owner_html = ('<details class="dm-owner"><summary>주인장이 본 지금 시점의 결론</summary>'
                      '%s</details>' % _scenario_html())

    # 비교·추이는 표로 낸다. 어느 축에든 걸 수 있게 축 id로 찾는다.
    # VS_TABLES = {축 id: spec} (한 축에 여럿이면 리스트로 준다)
    vs_html = ''
    for spec in (getattr(dmd, 'VS_TABLES', {}) or {}).get(ax['id'], []) or []:
        vs_html += _vs_html(spec)

    sens_html = ''
    if ax['id'] == 'dcf':
        # 연도별 추정이 이 방법의 본체다. 민감도는 그 결과를 흔들어 본 것이라 뒤에 둔다.
        dcf_path = getattr(dmd, 'DCF_PATH', None)
        if dcf_path:
            sens_html += _path_html(dcf_path)
        if getattr(dmd, 'SENSITIVITY', None):
            sens_html += _sens_html()
    elif ax['id'] == 'quote':
        qp = getattr(dmd, 'QUOTE_PATH', None)
        if qp:
            sens_html = _path_html(qp)
    elif ax['id'] == 'rev':
        rev_path = getattr(dmd, 'REV_PATH', None)
        if rev_path:
            sens_html = _path_html(rev_path)

    # 축 패널에는 엘곰이 쓴 것만 둔다. 대조표와 현금흐름 다리는 내가 계산한
    # 것이라 여기 있으면 그의 글에 있던 내용으로 읽힌다. 위층 「내 계산」 카드로
    # 옮겼다 — 이 페이지는 그 두 층을 갈라 놓는 것이 설계다.

    # 시장 읽기 표와 대조 표도 내가 계산한 것이라 축 패널에서 뺐다.
    # _mycalc_html이 위층 「내 계산」 카드에서 그린다.
    mr_html = ''
    bench_html = ''

    # 엘곰이 직접 만든 시나리오(02-26 역산 글)는 rev 축에만 속한다. 이 축에
    # 남는 유일한 표다 — 나머지 둘과 달리 그가 실제로 계산한 것이다.
    auth_html = _author_scenarios_html() if is_rev else ''

    verdict_html = ''
    if ax['verdict']:
        vlabel, vdesc = ax['verdict']
        vcls = 'dm-verdict--risk' if '되지 않는다' in vlabel else 'dm-verdict--good'
        verdict_html = ('<div class="dm-verdict %s"><span class="dm-verdict-tag">%s</span>'
                         '<span class="dm-verdict-desc">%s</span></div>' % (vcls, vlabel, vdesc))

    return ('<article class="%s" id="dm-%s-axis-%s">'
            '<div class="dm-axis-head"><span class="dm-axis-no">%s</span>'
            '<div class="dm-axis-headtext"><h3 class="dm-axis-name">%s</h3>'
            '<span class="dm-axis-tag">%s</span></div></div>'
            '%s'
            '<p class="dm-axis-sub">%s</p>'
            '%s'
            '%s'
            '<details class="dm-chainbox"><summary>수식 — 어떻게 계산했나</summary>'
            '<div class="dm-chain">%s</div></details>'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '</article>'
            # 연도별 경로 표(sens_html)가 드라이버 칩보다 먼저 온다. 방법을 눌렀을 때
            # 가장 먼저 보고 싶은 것은 「어느 해에 무엇을 얼마로 놓았나」이기 때문이다.
            % (axis_cls, _PX, ax['id'], ax['no'], ax['name'], ax['tag'], latest_html, ax['sub'],
               stale_html, _howto_html(ax['id']) + vs_html + sens_html, chain_html, inputs_html,
               gchips_html, out_html + owner_html, mr_html, bench_html, auth_html, verdict_html))


# render()가 호출될 때마다 그 회사의 AXES로 다시 채운다.
_AXIS_IDS = set()
_AXIS_LOOKUP = {}



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


def _vs_html(spec):
    """두 회사 지표 대조표. 원문 표를 그대로 옮긴 것이라 계산이 한 칸도 없다.

    드라이버 칩으로 흩어 놓으면 「ROE 61.17%」가 누구 값인지, 상대가 얼마인지가
    각 칩 안에 묻힌다. 같은 줄에 나란히 놓아야 어디서 갈리는지 한눈에 보인다."""
    ncol = len(spec['head'])
    head = ''.join('<th>%s</th>' % h for h in spec['head'])
    body = []
    for label, rows in spec['bands']:
        body.append('<tr class="dm-ep-band"><td colspan="%d">%s</td></tr>' % (ncol, label))
        for r in rows:
            cells = ''.join('<td%s>%s</td>' % (' class="dm-vs-win"' if j and j == r.get('win') else '', c)
                            for j, c in enumerate(r['cells']))
            body.append('<tr>%s</tr>' % cells)
    url = dc.blob(dmd.SUM + dmd.DOCS[spec['doc']]) + '#L%d' % spec['line']
    return ('<div class="dm-ep">'
            '<p class="dm-ep-label">%s %s '
            '<a class="dm-ep-src" href="%s" target="_blank" rel="noopener">요약본 ▸</a></p>'
            '<div class="dm-ep-wrap"><table class="dm-ep-tbl dm-vs-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-ep-foot">%s</p></div>'
            % (spec['lede'], _by_badge('author'), url, head, ''.join(body), spec['foot']))


def _path_html(spec):
    """한 글의 연도별 추정 표. 원문 표를 그대로 옮긴 것이라 계산이 한 칸도 없다.

    **연도가 가로축이다.** 세로로 세우면 한 지표가 어떻게 움직이는지 보려고 눈이
    아래로 훑어야 하는데, 재무 모형은 왼쪽에서 오른쪽으로 읽는 물건이다(2026-08-18).
    원문 표는 연도가 행이므로 여기서 뒤집는다 — 첫 열이 지표 이름, 나머지가 연도다.

    구간(컨센서스·필자·정상화)은 연도 위에 띠로 얹는다. 어느 해까지가 남의 숫자이고
    어디서부터 필자가 깐 것인지가 표 안에서 보여야 한다.

    메모는 표 안에 끼우지 않는다. 줄 사이에 문장이 들어가면 숫자가 끊긴다. 표 아래에
    연도를 앞세워 모아 둔다."""
    metrics = spec['head'][1:]          # 첫 열은 연도라 행 머리로 간다
    cols, notes, bands, ccls = [], [], [], []
    for bi, (label, rows) in enumerate(spec['bands']):
        bands.append((label, len(rows), bi))
        for ri, r in enumerate(rows):
            cols.append(r)
            # 구간은 열 전체를 따라 내려가야 보인다. 띠 한 줄로만 칠하면 숫자 줄에서
            # 경계가 사라져 어디까지가 남의 숫자인지 다시 위를 봐야 한다(2026-08-19).
            cls = ['dm-ep-b%d' % (bi % 3)]
            if ri == 0 and bi:
                cls.append('dm-ep-bcut')      # 구간이 바뀌는 자리에 세로선
            if r.get('muted'):
                cls.append('dm-ep-muted')
            ccls.append(' class="%s"' % ' '.join(cls))

    # 구간은 머리에 colspan 띠로 얹지 않는다. 띠는 칸보다 길어 잘리고, 그 줄 하나 때문에
    # 표 위가 벌어졌다. 지표처럼 한 행으로 내려 열마다 짧은 이름을 적는다(2026-08-19).
    short = []
    for lab, n, _bi in bands:
        nm = lab.split('·')[0].split('—')[0].strip()
        short += [nm] * n
    band_row = ''.join('<td%s>%s</td>' % (ccls[i], short[i]) for i in range(len(cols)))
    year_row = ''.join('<th%s>%s</th>' % (ccls[i], c['cells'][0])
                       for i, c in enumerate(cols))
    body = []
    for i, name in enumerate(metrics, 1):
        cells = ''.join('<td%s>%s</td>'
                        % (ccls[j], c['cells'][i] if i < len(c['cells']) else '')
                        for j, c in enumerate(cols))
        body.append('<tr><th scope="row">%s</th>%s</tr>' % (name, cells))

    url = dc.blob(dmd.SUM + dmd.DOCS[spec['doc']]) + '#L%d' % spec['line']
    return ('<div class="dm-ep">'
            '<p class="dm-ep-label">%s %s '
            '<a class="dm-ep-src" href="%s" target="_blank" rel="noopener">요약본 ▸</a></p>'
            '<div class="dm-ep-wrap"><table class="dm-ep-tbl dm-ep-wide">'
            '%s'
            '<thead><tr><th class="dm-ep-corner">%s</th>%s</tr></thead>'
            '<tbody><tr class="dm-ep-bandrow"><th scope="row">구간</th>%s</tr>%s</tbody>'
            '</table></div>'
            '%s'
            '<p class="dm-ep-foot">%s</p>'
            '</div>' % (spec['lede'], _by_badge('author'), url,
                        '<colgroup><col class="dm-ep-mt">%s</colgroup>' % ('<col class="dm-ep-yr">' * len(cols)),
                        spec['head'][0], year_row, band_row, ''.join(body),
                        ('<ul class="dm-ep-notes">%s</ul>' % ''.join(notes)) if notes else '',
                        spec['foot']))


def _stmt_vs_dcf_html():
    """재무제표 본편 다섯이 잰 것과 8년 DCF가 실제로 쓴 것을 마주 세운다.
    따로 두면 다섯 편이 그냥 옛날 글로 보인다. 나란히 놓아야 빠진 자리가 보인다.

    평가가 한 편뿐인 회사는 「본편이 잰 것 vs 평가가 쓴 것」을 마주 세울 다른 글이 없다 —
    STMT_VS_DCF가 없으면 조용히 빈 문자열을 낸다."""
    v = getattr(dmd, 'STMT_VS_DCF', None)
    if not v:
        return ''
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
    항등식으로 되돌린 것이라, 되돌아왔다는 사실 자체가 △NWC=0의 증거다.

    되돌릴 빈칸이 없는(원문 표가 없는) 회사는 CASH_BRIDGE가 없을 수 있다."""
    v = getattr(dmd, 'CASH_BRIDGE', None)
    if not v:
        return ''
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
            # 「→」로 시작하는 항목은 확정 실적이 아니라 컨센서스를 채우려면
            # 필요한 값이다. 나머지와 같은 색으로 두면 이미 번 돈으로 읽힌다.
            sums = '<dl class="dm-act-sums">%s</dl>' % ''.join(
                '<dt%s>%s</dt><dd%s>%s</dd>'
                % ((' class="dm-act-sums-calc"' if k.startswith('→') else ''), k,
                   (' class="dm-act-sums-calc"' if k.startswith('→') else ''), v)
                for k, v in a['rows2'])
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
            # 제목은 버튼(summary)이 갖는다 — 안에서 또 적으면 같은 말이 두 번 선다
            '<div class="dm-scenario-head">'
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
            '%s'
            '<p class="dm-scenario-note">%s</p>'
            '<div class="dm-scenario-punch">%s</div>'
            '</div>'
            % (s['asof'], s['price'], s['mcap'], s['formula'], head,
               ''.join(body_rows), rev_html, act_html, _mycalc_html(),
               s['note'], s['punch']))


def _market_read_html():
    """같은 역산 공식을 시점마다 내가 다시 돌린 표. 02-26 글에 있던 표가 아니다."""
    ax = next((a for a in dmd.AXES if a.get('market_read')), None)
    if not ax:
        return ''
    mr = ax['market_read']
    head = ''.join('<th>%s</th>' % h for h in mr['head'])
    body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in mr['rows'])
    return ('<div class="dm-mr"><p class="dm-mr-label">그 주가를 유지하려면 필요한 이익 '
            '(시점마다 다시 계산했다) %s</p>'
            '<div class="dm-mr-wrap"><table class="dm-mr-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-mr-note">%s</p></div>'
            % (_by_badge('ours'), head, body, mr['note']))


def _benchmark_html():
    """요구 이익이 나올 만한 값인지 실적·컨센서스에 대 본 것. 내가 모은 대조다."""
    ax = next((a for a in dmd.AXES if a.get('benchmark')), None)
    if not ax:
        return ''
    rows = ''.join(
        '<tr><td>%s</td><td class="dm-bench-v">%s</td><td class="dm-bench-note">%s</td></tr>'
        % (k, v, note) for k, v, note in ax['benchmark'])
    return ('<div class="dm-bench"><p class="dm-bench-label">그 이익이 나올 만한가 %s</p>'
            '<div class="dm-bench-wrap"><table class="dm-bench-tbl">'
            '<thead><tr><th>대조 대상</th><th>값</th><th>요구치와 견주면</th></tr></thead>'
            '<tbody>%s</tbody></table></div></div>' % (_by_badge('ours'), rows))


def _mycalc_html():
    """내가 계산한 네 표. 원래 축 패널에 흩어져 있었는데, 그 자리는 엘곰이 쓴
    것만 두는 자리다 — 거기 있으면 그의 글에 있던 내용으로 읽힌다. 이 카드가
    「내 계산」 층이라 여기가 맞다. 결론을 아래로 밀지 않게 접어 둔다.

    네 표 전부 평가가 여러 편이라야 나오는 대조·역산 자료다. 한 편도 안 나오면
    (평가가 한 편뿐인 회사) 빈 details를 띄우지 않고 통째로 건너뛴다."""
    body = _cash_bridge_html() + _stmt_vs_dcf_html() + _market_read_html() + _benchmark_html()
    if not body:
        return ''
    return ('<details class="dm-mycalc">'
            '<summary class="dm-mycalc-summary">'
            '이 값을 어떻게 냈나 (원문에 없던 자리를 되돌리고 시점마다 다시 돌린 것) %s'
            '</summary>'
            '<div class="dm-mycalc-body">%s</div>'
            '</details>' % (_by_badge('ours'), body))


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
            # 목록에서 옛 값을 갈라 놓으려면 날짜가 데이터로 있어야 한다.
            # 지금까지는 '250816' 여섯 자리만 넘겨서 읽히지 않았다.
            date=_doc_date(d['doc']), stale=dmd.is_stale(d['doc']),
            basisKey=d['basis'], basisLabel=basis_label, basisDesc=basis_desc,
            why=d['why'], impact=d['impact'], url=url,
            bar=list(d['bar']) if 'bar' in d else None,
            # 「내 판정」 칸 — 구조화 데이터만 넘긴다. HTML은 JS가 만든다(fmtJudgment).
            judgment=_judgment_entries_data(jentries),
            judgmentVerdicts=[e.get('verdict') for e in jentries] if jentries else None,
        )
    groups = {g['id']: dict(name=g['name'], q=g['q'], why=g['why'], corpus=g['corpus'])
              for g in dmd.GROUPS}
    return dict(drivers=drivers, groups=groups, staleWhy=dmd.STALE_WHY)


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

/* ── 내 계산 과정 (접힘) ── 결론 카드 안이라 열기 전에는 자리를 거의 안 먹어야
   한다. 안에 든 두 표는 자기 테두리를 갖고 있어 여기선 테두리를 겹치지 않는다 */
.dm-mycalc{margin:14px 0 0;border:1px dashed var(--line);border-radius:10px;
           background:var(--sunk)}
.dm-mycalc-summary{cursor:pointer;list-style:none;font-size:12px;font-weight:850;
                   color:var(--ink-2);padding:10px 13px;display:flex;align-items:center;
                   gap:8px;flex-wrap:wrap}
.dm-mycalc-summary::-webkit-details-marker{display:none}
.dm-mycalc-summary::before{content:"▸";color:var(--ink-3);font-size:11px}
.dm-mycalc[open] .dm-mycalc-summary::before{content:"▾"}
.dm-mycalc-summary:hover{color:var(--ink)}
.dm-mycalc-body{padding:0 13px 13px}
/* 안쪽 표의 첫 위 여백은 summary가 이미 만들어 준다 */
.dm-mycalc-body > .dm-cb{margin-top:0}

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
/* 배경은 같은 카드 안의 실적 표(.dm-act)와 맞춘다. 강조색을 혼자 쓰면
   블록 하나만 다른 화면에서 온 것처럼 보인다. 방향이 반대라는 것은 색이
   아니라 제목과 머리말이 말한다 */
.dm-rv{margin:16px 0 0;background:var(--sunk);border-radius:10px;padding:11px 13px}
.dm-rv-label{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:0 0 4px}
.dm-rv-lede{font-size:12px;line-height:1.6;color:var(--ink-2);margin:0 0 8px}
.dm-rv-formula{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 10px;
               font-variant-numeric:tabular-nums}
.dm-rv-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-rv-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
.dm-rv-tbl th{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
             text-align:left;padding:3px 12px 6px 8px;border-bottom:1px solid var(--line);
             white-space:nowrap;vertical-align:top}
.dm-rv-tbl td{padding:7px 12px 7px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.dm-rv-tbl tr:last-child td{border-bottom:0}
.dm-rv-tbl td:first-child{font-weight:700;color:var(--ink-2)}
.dm-rv-row--main td{font-weight:850;color:var(--ink);font-size:15px}
.dm-rv-row--main td:first-child{font-size:12.5px;font-weight:800;color:var(--ink-2)}
.dm-rv-val{font-variant-numeric:tabular-nums}
.dm-rv-val--high{color:var(--warn);font-weight:800}
.dm-rv-val--low{color:var(--good);font-weight:800}
/* 결과 행 규칙(.dm-rv-row--main td, 15px)이 명시도에서 이겨 비고 칸까지 크게
   나왔다. 값만 커야 하고 설명은 다른 설명글과 같은 크기라야 한다 */
.dm-rv-row--main td.dm-rv-notecell,
.dm-rv-notecell{color:var(--ink-3);font-size:11.5px;font-weight:500;line-height:1.55;
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
/* 확정 실적과 「그러려면 필요한 값」을 같은 회색으로 두면 이미 번 돈으로 읽힌다.
   이 줄만 갈라 놓는다 — 아직 벌지 않은 숫자다. 숫자는 파랑(--accent-ink)이다.
   이 저장소는 호재를 빨강, 부담을 파랑으로 쓴다 */
.dm-act-sums dt.dm-act-sums-calc{border-top:1px dashed var(--line);padding-top:6px}
.dm-act-sums dd.dm-act-sums-calc{border-top:1px dashed var(--line);padding-top:6px;
                                 color:var(--accent-ink);font-weight:850}
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
.dm-ep{margin:20px 0 22px;background:var(--surface);border:1px solid var(--line);
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
/* 메모가 붙은 줄. 주황으로 칠했더니 표 절반이 주황이 돼 어느 줄이 중요한지 안 보였다.
   바탕은 지면과 같은 톤으로 낮추고 왼쪽 선 하나로만 표시한다. */
.dm-ep-hi td{background:var(--sunk);color:var(--ink);font-weight:800;border-bottom:0}
.dm-ep-hi td:first-child{box-shadow:inset 3px 0 0 var(--line)}
.dm-ep-hi i{color:var(--ink-2)}
/* 연도를 가로로 세운 표. 열이 열 개를 넘어가므로 첫 열(지표 이름)을 붙박이로 둔다 */
/* 두 회사 대조표. 한 화면에 들어와야 나란히 놓은 뜻이 산다 — 줄 높이를 조인다.
   앞선 쪽 칸만 진하게. 화살표나 색 배지를 붙이면 표가 시끄럽다. */
.dm-vs-tbl td{text-align:right;font-variant-numeric:tabular-nums;padding:3px 12px 3px 8px}
.dm-vs-tbl th{padding:3px 12px 5px 8px}
.dm-vs-tbl .dm-ep-band td{padding:3px 8px}
.dm-vs-tbl td:first-child{text-align:left;font-weight:800;color:var(--ink-2)}
.dm-vs-tbl th{text-align:right}
.dm-vs-tbl th:first-child{text-align:left}
.dm-vs-win{color:var(--ink);font-weight:850}
/* 구간은 선으로만 가른다. 한 구간만 칠하면 그 구간이 다른 성격의 값처럼 읽힌다 —
   컨센서스든 필자가 깐 것이든 같은 표의 같은 줄이다. 경계만 또렷하면 된다. */
.dm-ep-bcut{border-left:2px solid var(--ink-3) !important}
/* 연도 열은 폭을 같게 잡는다. 값 길이에 따라 칸이 들쭉날쭉하면 경사가 안 읽힌다 */
/* 폭은 <col>이 갖는다. th에 width를 또 주면 fixed 레이아웃에서 첫 열이 다음 열과
   겹쳐 글자가 포개졌다(2026-08-19 화면 확인). 표는 내용만큼 넓히고 감싼 상자가 스크롤한다. */
.dm-ep-wide{table-layout:fixed;width:max-content;min-width:100%}
.dm-ep-wide col.dm-ep-mt{width:104px}
.dm-ep-wide col.dm-ep-yr{width:98px}
/* 구간은 선으로만 가른다. 한 구간만 칠하면 그 구간이 다른 성격의 값처럼 읽힌다 —
   컨센서스든 필자가 깐 것이든 같은 표의 같은 줄이다. 경계만 또렷하면 된다. */
.dm-ep-bcut{border-left:2px solid var(--ink-3) !important}
.dm-ep-wide th[scope="row"]{position:sticky;left:0;z-index:2;background:var(--surface);
     text-align:left;font-size:11px;font-weight:800;color:var(--ink-2);white-space:nowrap;
     overflow:hidden;text-overflow:ellipsis;
     padding:6px 6px 6px 8px;border-bottom:1px solid var(--line);
     box-shadow:1px 0 0 var(--line)}
.dm-ep-wide td{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;
     padding:4px 12px 4px 8px}
.dm-ep-wide thead th{padding:4px 12px 6px 8px}
/* 구간 행 — 숫자가 아니라 이름이라 작게, 위아래 선으로 묶는다 */
.dm-ep-bandrow td{font-size:10px;font-weight:850;letter-spacing:.02em;color:var(--ink-3);
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dm-ep-bandrow th[scope="row"]{font-size:10px;color:var(--ink-3)}
.dm-ep-wide thead th{text-align:right;white-space:nowrap}
.dm-ep-corner{position:sticky;left:0;z-index:3;background:var(--surface);text-align:left !important;box-shadow:1px 0 0 var(--line)}
.dm-ep-bandh{font-size:10px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
     background:var(--sunk);text-align:left !important;padding:4px 8px;
     border-bottom:1px solid var(--line);
     white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
/* 메모는 표 밖, 표 바로 아래에 모은다. 연도를 앞세워 어느 줄 이야기인지 잇는다 */
/* 주인장 계산 — 축 안에서 버튼 하나로 연다 */
/* 주인장 계산은 내용 한 겹일 뿐이라 강조색을 쓰지 않는다 — 주황은 올라가는 길과
   판정 배지에만 남긴다 */
.dm-owner{margin:14px 0 0;border:1px solid var(--line);border-radius:10px;background:var(--surface)}
.dm-owner>summary{cursor:pointer;list-style:none;padding:11px 14px;font-size:12.5px;font-weight:800;
                  color:var(--ink-2)}
.dm-owner>summary::-webkit-details-marker{display:none}
.dm-owner>summary::after{content:"▾";float:right;font-size:11px}
.dm-owner[open]>summary::after{content:"▴"}
.dm-owner .dm-scenario{margin:0;border:0;background:transparent}
/* 드라이버 표 — 값 하나에 문단 둘을 붙이던 블록을 한 줄로 바꿨다 */
.dm-dvt-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 10px}
.dm-dvt{width:100%;border-collapse:collapse;font-size:12px}
/* 두 열짜리 표. 왼쪽이 항목, 오른쪽이 내용. 드라이버마다 이름 줄이 앞에 선다 */
.dm-dvt{width:100%;border-collapse:collapse;font-size:12px;table-layout:fixed}
.dm-dvt-head th{text-align:left;font-size:12.5px;font-weight:850;color:var(--ink);
     padding:12px 0 5px;border-top:1px solid var(--line)}
.dm-dvt tr:first-child .dm-dvt-head th, .dm-dvt-head:first-child th{border-top:0;padding-top:2px}
.dm-dvt col.dm-dvt-c1{width:34px}
.dm-dvt th[scope="row"]{text-align:left;font-size:10px;font-weight:800;
     color:var(--ink-3);letter-spacing:0;padding:3px 6px 3px 0;vertical-align:top;
     white-space:nowrap}
.dm-dvt td{padding:3px 0;vertical-align:top;color:var(--ink-3);line-height:1.6;
     overflow-wrap:anywhere}
.dm-dvt-val{font-size:13px;font-weight:850;color:var(--ink);font-variant-numeric:tabular-nums}
.dm-dvt-why{font-size:11.5px}
.dm-dvt tr.dm-dv--none th{box-shadow:inset 3px 0 0 var(--risk);padding-left:7px}
.dm-dvt-impact{display:block;margin-top:4px;color:var(--ink-2)}
.dm-dvt-impact b{color:var(--ink);font-weight:850;margin-right:4px}
.dm-dvt-grp th{text-align:left;font-size:9.5px;font-weight:850;letter-spacing:.06em;
     color:var(--ink-3);padding:12px 0 4px;border-bottom:1px solid var(--line)}
.dm-dvt tr:first-child.dm-dvt-grp th{padding-top:2px}
.dm-dvt tr.dm-dv--none th[scope="row"]{box-shadow:inset 3px 0 0 var(--risk)}
@media (max-width:560px){
  .dm-dvt{font-size:11.5px}
  .dm-dvt col.dm-dvt-c1{width:28px}
  .dm-dvt th[scope="row"]{font-size:9.5px;padding-right:5px}
}
/* 방법 설명. 아는 사람에게는 군더더기라 접어 둔다 */
.dm-howto{margin:0 0 14px;border:1px solid var(--line);border-radius:8px;background:var(--surface)}
.dm-howto>summary{cursor:pointer;list-style:none;padding:9px 12px;font-size:12px;font-weight:800;
                  color:var(--ink-2)}
.dm-howto>summary::-webkit-details-marker{display:none}
.dm-howto>summary::after{content:"▾";float:right;color:var(--ink-3);font-size:10px}
.dm-howto[open]>summary::after{content:"▴"}
.dm-howto-p{font-size:11.5px;line-height:1.65;color:var(--ink-3);margin:0 12px 10px}
.dm-howto-risk b{color:var(--ink-2);font-weight:800;margin-right:4px}
.dm-ep-notes{list-style:none;margin:9px 0 0;padding:0}
.dm-ep-notes li{font-size:11px;line-height:1.6;color:var(--ink-3);margin:0 0 4px;padding-left:11px;
                position:relative}
.dm-ep-notes li::before{content:"";position:absolute;left:0;top:8px;width:5px;height:1px;
                        background:var(--line)}
.dm-ep-notes b{color:var(--ink-2);font-weight:800;margin-right:5px;
               font-variant-numeric:tabular-nums}
.dm-ep-muted td{color:var(--ink-3)}
.dm-ep-tbl tr:last-child td{border-bottom:0}
.dm-ep-punch{font-size:13px;line-height:1.62;color:var(--ink-2);margin:11px 0 0;
             border-left:3px solid var(--warn);background:var(--warn-soft);
             border-radius:0 8px 8px 0;padding:9px 13px}
.dm-ep-punch b{color:var(--ink);font-weight:850}
.dm-ep-foot{font-size:11px;line-height:1.55;color:var(--ink-3);margin:8px 0 0}

/* ── 옛 값 표시 ── 사이클 전환(2026-01) 앞쪽 값에 붙는다.
   회색으로만 죽이면 「덜 중요한 것」으로 읽힌다. 옛것은 덜 중요한 게 아니라
   다른 국면의 값이다. 그래서 점선 테두리로 「따로 놓은 것」임을 보인다 */
.dm-axisbtn--stale .dm-axisbtn-date{color:var(--ink-3)}
.dm-axisbtn-stale{display:block;font-size:9.5px;font-weight:850;letter-spacing:.02em;
                  color:var(--warn);margin-top:3px;white-space:nowrap}
.dm-axis-stale{display:flex;gap:9px;align-items:flex-start;margin:0 0 12px;
               border:1px dashed var(--warn);border-radius:8px;background:var(--warn-soft);
               padding:9px 12px}
.dm-axis-stale-tag{flex:none;font-size:10px;font-weight:850;letter-spacing:.03em;
                   color:var(--warn);border:1px solid var(--warn);border-radius:999px;
                   padding:1px 8px;line-height:1.6;white-space:nowrap}
.dm-axis-stale-text{font-size:11.5px;line-height:1.55;color:var(--ink-2)}
/* 모달 목록 — 옛것은 구분선 아래로 내려간다 */
                   font-variant-numeric:tabular-nums;white-space:nowrap}
                    background:var(--warn-soft);border-radius:0 0 8px 8px}
/* 그 갈래가 통째로 옛것이면 구분선 위에 아무것도 없다 — 선만 떠 보인다 */
                                                 border-radius:8px}
                        color:var(--warn);margin-right:7px}
/* 상세 — 숫자보다 위에 둔다. 아래 두면 이미 읽은 뒤가 된다 */
                border-radius:8px;background:var(--warn-soft);
                font-size:11.5px;line-height:1.55;color:var(--ink-2)}
                  margin-bottom:3px}

/* ── 드라이버 표 ── 값을 숨기지 않고 편다. 행을 누르면 상세가 열린다 */
.dm-dt{margin:0 0 14px}
.dm-dt-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 7px}
.dm-dt-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-dt-tbl{width:100%;border-collapse:collapse;font-size:12px}
.dm-dt-tbl th{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--ink-3);
              text-align:left;padding:3px 12px 6px 8px;border-bottom:1px solid var(--line);
              white-space:nowrap}
.dm-dt-tbl td{padding:7px 12px 7px 8px;border-bottom:1px solid var(--line);
              color:var(--ink-2);line-height:1.5;vertical-align:top}
/* 갈래 띠 — 갈래마다 묻는 질문이 다르고 그 질문이 표를 읽는 실마리다 */
.dm-dt-band td{background:var(--sunk);padding:6px 12px 6px 8px;border-bottom:1px solid var(--line)}
.dm-dt-bandname{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--ink-2)}
.dm-dt-bandq{font-size:10.5px;color:var(--ink-3);margin-left:8px}
.dm-dt-row{cursor:pointer}
.dm-dt-row:hover td{background:var(--accent-soft)}
.dm-dt-row:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.dm-dt-name{font-weight:800;color:var(--ink);white-space:nowrap}
.dm-dt-val{font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums;
           min-width:14ch;max-width:26ch}
.dm-dt-basis{white-space:nowrap}
.dm-dt-why{color:var(--ink-3);min-width:24ch;max-width:44ch}
/* 근거가 빈 값은 왼쪽에 표시를 남긴다 — 비어 있다는 사실 자체가 감사 대상이다 */
.dm-dt-row--none .dm-dt-name{box-shadow:inset 3px 0 0 var(--warn)}
.dm-dt-jg{display:inline-block;font-size:9.5px;font-weight:850;color:var(--accent-ink);
          background:var(--accent-soft);border-radius:999px;padding:1px 6px;margin-left:6px}
.dm-dt-hint{font-size:10.5px;color:var(--ink-3);margin:7px 0 0}

/* ── 드라이버 지면 ── 눌러서 여는 것을 없애고 값·근거·왜·영향을 다 편다 */
.dm-dvwrap{margin:0 0 14px}
.dm-dvwrap-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 8px}
/* 글 고르는 탭 — 한 방법에 글이 여럿일 때만 선다 */
.dm-dvtabs{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.dm-dvtab{font:inherit;cursor:pointer;font-size:11.5px;font-weight:800;color:var(--ink-3);
          background:var(--surface);border:1px solid var(--line);border-radius:999px;
          padding:4px 11px;display:inline-flex;align-items:baseline;gap:5px}
.dm-dvtab:hover{border-color:var(--accent);color:var(--accent-ink)}
.dm-dvtab:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-dvtab[aria-selected="true"]{background:var(--accent-soft);border-color:var(--accent);
                                color:var(--accent-ink)}
.dm-dvtab-n{font-size:9.5px;font-weight:850;opacity:.7}
.dm-dvdoc-title{font-size:12.5px;font-weight:850;color:var(--ink);margin:0 0 4px;line-height:1.5}
.dm-dvdoc-src{font-size:10.5px;font-weight:700;color:var(--accent-ink);text-decoration:none;
              margin-left:6px;white-space:nowrap}
.dm-dvdoc-src:hover{text-decoration:underline}
.dm-dvdoc-gist{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 10px;max-width:74ch}
/* 값 한 덩이 */
.dm-dv{margin:0 0 9px;background:var(--surface);border:1px solid var(--line);
       border-radius:9px;padding:10px 12px;box-shadow:var(--shadow)}
.dm-dv--none{border-left:3px solid var(--warn)}
.dm-dv-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 9px;margin:0 0 6px}
.dm-dv-name{font-size:12px;font-weight:850;color:var(--ink-2)}
.dm-dv-val{font-size:14px;font-weight:850;color:var(--ink);font-variant-numeric:tabular-nums}
.dm-dv-grp{margin-left:auto;font-size:10px;font-weight:700;color:var(--ink-3);
           border:1px solid var(--line);border-radius:999px;padding:1px 7px;white-space:nowrap}
.dm-dv-why{font-size:11.5px;line-height:1.62;color:var(--ink-2);margin:0 0 5px;max-width:78ch}
.dm-dv-impact{font-size:11.5px;line-height:1.62;color:var(--ink-3);margin:0;max-width:78ch}
.dm-dv-impact b{color:var(--ink-2);font-weight:850;margin-right:4px}
/* 내 판정 — 필자 값 아래에 붙지만 주체가 다르다 */
.dm-dv-jg{margin:8px 0 0;padding:8px 10px;background:var(--accent-soft);border-radius:7px}
.dm-dv-jgtitle{font-size:10.5px;font-weight:850;letter-spacing:.03em;color:var(--accent-ink);margin:0 0 5px}
.dm-dv-jgitem{margin:0 0 6px}
.dm-dv-jgitem:last-child{margin-bottom:0}
.dm-dv-jglabel{display:block;font-size:10.5px;font-weight:800;color:var(--ink-3);margin:0 0 2px}
.dm-dv-jgbadge{display:inline-block;font-size:10px;font-weight:850;border-radius:999px;
               padding:1px 8px;margin-right:6px}
.dm-dv-jgbadge--keep{background:var(--good-soft);color:var(--good)}
.dm-dv-jgbadge--fix{background:var(--warn-soft);color:var(--warn)}
.dm-dv-jgbadge--hold{background:var(--sunk);color:var(--ink-3)}
.dm-dv-jgbadge--check{background:var(--risk-soft);color:var(--risk)}
.dm-dv-jgwhy{font-size:11px;line-height:1.6;color:var(--ink-2)}
.dm-dv-jgmine{font-size:11px;line-height:1.6;color:var(--ink-2);margin:5px 0 0}
.dm-dv-jgmine b{color:var(--accent-ink);font-weight:850;margin-right:4px}

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
/* 값과 뜻은 문장이라 좁으면 세로로 길어진다. 각각 폭을 잡아 준다 */
.dm-sv-tbl td:nth-child(3){min-width:20ch;max-width:30ch}
.dm-sv-tbl td:nth-child(4){min-width:22ch;max-width:34ch;color:var(--ink-3)}
/* 마지막 열이 「안 썼다」를 말하는 자리다. 왼쪽 경계로 갈라 놓는다 */
.dm-sv-tbl td:last-child{border-left:1px solid var(--line);color:var(--ink-3);
                         min-width:20ch;max-width:30ch}
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
/* ── 시기 머리말 ── 방법보다 위층이다. 한 시기 안에서만 값이 서로 비교된다 */
.dm-axisera{margin:0 0 14px}
.dm-axisera-head{margin:0 0 7px}
.dm-axisera-label{display:block;font-size:12px;font-weight:850;letter-spacing:.03em;
                  color:var(--ink)}
.dm-axisera-sub{display:block;font-size:11px;line-height:1.55;color:var(--ink-3);
                margin-top:2px;max-width:64ch}
/* 다운사이클 묶음은 들여쓰고 왼쪽 선을 둔다 — 같은 줄에 세우면 안 되는 값들이다 */
.dm-axisera--stale{padding-left:11px;border-left:2px dashed var(--line)}
.dm-axisera--stale .dm-axisera-label{color:var(--ink-3)}
.dm-axisera-btns{display:flex;gap:8px;overflow-x:auto;-webkit-overflow-scrolling:touch;
                 padding:2px 2px 6px}
.dm-axisbtns{margin:0 0 8px}
.dm-axisbtn{flex:0 0 auto;display:flex;flex-direction:column;align-items:flex-start;gap:2px;
            font:inherit;cursor:pointer;padding:8px 14px;border-radius:10px;
            border:1px solid var(--line);background:var(--surface);color:var(--ink-2)}
.dm-axisbtn:hover{border-color:var(--accent);background:var(--accent-soft)}
.dm-axisbtn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
/* ── 목록으로 돌아가는 버튼 ── 상세 맨 위, 내용보다 먼저 눈에 걸려야 한다 */
.dm-axisback{display:inline-flex;align-items:baseline;gap:7px;font:inherit;cursor:pointer;
             margin:0 0 12px;padding:6px 13px 6px 10px;border-radius:999px;
             border:1px solid var(--line);background:var(--sunk);color:var(--ink-2)}
.dm-axisback:hover{border-color:var(--accent);color:var(--accent-ink);
                   background:var(--accent-soft)}
.dm-axisback:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dm-axisback-arrow{font-size:12px;line-height:1}
.dm-axisback-text{font-size:12px;font-weight:850}
.dm-axisback-era{font-size:10.5px;font-weight:700;color:var(--ink-3)}
.dm-axisback:hover .dm-axisback-era{color:var(--accent-ink)}
.dm-axisbtn-no{font-size:10px;font-weight:800;letter-spacing:.02em;color:var(--ink-3)}
.dm-axisbtn-name{font-size:13px;font-weight:850;color:var(--ink)}
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
.dm-chainbox{margin:18px 0 14px;border:1px solid var(--line);border-radius:8px;
     background:var(--surface)}
.dm-chainbox>summary{cursor:pointer;list-style:none;padding:9px 12px;font-size:12px;
     font-weight:800;color:var(--ink-2)}
.dm-chainbox>summary::-webkit-details-marker{display:none}
.dm-chainbox>summary::after{content:"▾";float:right;color:var(--ink-3);font-size:10px}
.dm-chainbox[open]>summary::after{content:"▴"}
.dm-chain{display:flex;flex-direction:column;gap:7px;margin:0;padding:2px 12px 12px}
.dm-chain-line{font-size:12.5px;line-height:2;color:var(--ink-2);margin:0}
/* 수식 한 자리 = 이름 + 값. 줄바꿈으로 둘이 갈라지면 어느 값이 어느 이름의
   것인지 안 보이므로 통째로 묶어 둔다 */
/* 값이 길면 inline-flex 상자를 뚫고 글자가 배경 밖으로 나갔다(2026-08-19 모바일).
   글처럼 흐르게 display:inline으로 두고, 줄이 바뀌어도 배경이 각 줄에 다시 칠해지도록
   box-decoration-break:clone을 준다. 이름과 값은 사이 여백으로 묶는다. */
.dm-chain-driver{display:inline;white-space:normal;overflow-wrap:anywhere;
                 padding:1px 7px;border-radius:6px;background:var(--sunk);
                 border:1px solid var(--line);
                 -webkit-box-decoration-break:clone;box-decoration-break:clone}
.dm-chain-driver + .dm-chain-driver{margin-left:3px}
.dm-chain-name{font-size:11px;font-weight:700;color:var(--ink-3);margin-right:4px}
.dm-chain-val{color:var(--ink);font-weight:850;font-variant-numeric:tabular-nums}

/* ── 상위 드라이버 칩 줄 ── */
          cursor:pointer;padding:4px 10px;margin:0;border-radius:999px;
          border:1px solid var(--accent-soft);background:var(--accent-soft);color:var(--accent-ink);
          line-height:1.4}
               width:14px;height:14px;border-radius:50%;background:var(--warn);color:var(--surface);
               font-size:10px;font-weight:900;line-height:1}
/* 내 판정이 있는 세부 드라이버 개수 — 근거 없음 경고(!)와 자리를 나눠 색으로 구분한다 */
             min-width:14px;height:14px;padding:0 4px;border-radius:999px;
             background:var(--accent);color:var(--surface);
             font-size:9.5px;font-weight:900;line-height:1}

/* 「결과」 꼬리표와 값이 붙어 「결과주당 내재가치…」로 읽혔다(2026-08-19).
   같은 줄에 두되 사이를 벌리고, 좁으면 값이 아래로 내려간다. */
.dm-axis-out{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 9px;margin:0 0 10px;
             padding-top:10px;border-top:1px solid var(--line)}
.dm-axis-out-tag{font-size:10px;font-weight:800;color:var(--ink-3);letter-spacing:.04em}
.dm-axis-out-val{font-size:13px;font-weight:800;color:var(--ink)}
                  width:100%;text-align:left;font:inherit;cursor:pointer;padding:10px 0 0;
                  margin:0 0 10px;border-radius:4px}
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
               font-weight:700;color:var(--ink);cursor:pointer;padding:2px 4px;border-radius:6px}

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
                   justify-content:center;background:rgba(0,0,0,.5);padding:20px}
         background:var(--surface);border:1px solid var(--line);border-radius:10px;
         box-shadow:var(--shadow);padding:20px 20px 22px;outline:none}
                border:1px solid var(--line);background:var(--sunk);color:var(--ink-2);
                font-size:18px;line-height:1;cursor:pointer}
               background:transparent;border:0;cursor:pointer;padding:2px 0;margin:0 0 10px}
                 background:var(--warn-soft);border:1px dashed var(--warn);border-radius:8px;
                 padding:9px 11px;margin:0 0 14px}
              text-align:left;font:inherit;padding:9px 10px;border:1px solid var(--line);
              border-radius:8px;background:var(--sunk);cursor:pointer}
.dm-bar-mini{position:relative;display:inline-block;width:56px;height:4px;border-radius:999px;
            background:var(--line);flex:0 0 auto}
.dm-bar-mini-fill{position:absolute;left:0;top:0;bottom:0;border-radius:999px;background:var(--accent-soft)}
.dm-bar-mini-dot{position:absolute;top:50%;width:8px;height:8px;border-radius:50%;background:var(--accent);
                 border:2px solid var(--surface);transform:translate(-50%,-50%)}
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

@media (max-width:560px){
  .dm-wrap{margin:0 0 24px;padding-bottom:20px}
  /* 좁은 화면에선 가운데 정렬 모달이 답답하다 — 아래에서 올라오는 시트로 바꾼다 */

  /* 계산 사슬 칩이 화면 밖으로 튀어나왔다(2026-08-19 하이닉스 멀티플). 이름과 값이
     갈라지지 않게 nowrap을 걸어 둔 것이 원인이다. 좁은 화면에서는 칩 안에서 줄을
     바꾸게 풀고, 이름과 값은 위아래로 쌓아 짝을 유지한다. */
  .dm-chain-line{overflow-wrap:anywhere;line-height:1.9}
  /* 지표 이름 열이 넓으면 첫 칸과 경계선 사이가 텅 빈다 */
  .dm-ep-wide col.dm-ep-mt{width:88px}
  .dm-ep-wide th[scope="row"]{font-size:10.5px;padding-right:4px}
  .dm-axis, .dm-axispanel, .dm-dv, .dm-scenario{min-width:0}
  .dm-axis{padding:14px 12px 13px}
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
      var mine = v.mine ? '<p class="dm-jg-mine"><b>주인장이 대신 보는 값</b>'+v.mine+'</p>' : '';
      return '<div class="dm-jg-entry">'+sub+badge+why+mine
           + fmtJgEvidence(v.evidence)+fmtJgExtra(v.extra)+'</div>';
    }).join('');
    return '<div class="dm-jg"><p class="dm-jg-title">주인장 판정</p>'+body+'</div>';
  }

  function fmtRow(did){
    var d = DATA.drivers[did];
    if(!d) return '';
    var noneCls = d.basisKey === 'none' ? ' dm-modal-row--none' : '';
    var basisNoneCls = d.basisKey === 'none' ? ' dm-basis--none' : '';
    var staleCls = d.stale ? ' dm-modal-row--stale' : '';
    return '<button type="button" class="dm-modal-row'+noneCls+staleCls+'" data-driver="'+did+'">'
         + '<span class="dm-modal-row-main">'
         +   '<span class="dm-modal-row-label">'+d.label+fmtJgBadges(d.judgmentVerdicts)+'</span>'
         +   '<span class="dm-modal-row-base">'+d.base+'</span>'
         + '</span>'
         + '<span class="dm-modal-row-date">'+d.date+'</span>'
         + (d.bar ? fmtBarMini(d.bar) : '')
         + '<span class="dm-basis'+basisNoneCls+'">'+d.basisLabel+'</span>'
         + '</button>';
  }

  function renderStage1(){
    var g = DATA.groups[state.gid];
    if(!g) return;
    // 사이클 전환 앞뒤를 한 줄기로 늘어놓으면 2024년 값이 지금 값으로 읽힌다.
    // 지금 것을 위에, 옛것을 구분선 아래에 둔다. 순서는 각 묶음 안에서 보존한다.
    var now = [], old = [];
    state.members.forEach(function(did){
      var d = DATA.drivers[did];
      if(!d) return;
      (d.stale ? old : now).push(did);
    });
    var rows = now.map(fmtRow).join('');
    if(old.length){
      rows += '<div class="dm-modal-staleline">'
            +   '<span class="dm-modal-staleline-tag">옛 값 · '+old.length+'</span>'
            +   '<span class="dm-modal-staleline-why">'+DATA.staleWhy+'</span>'
            + '</div>'
            + old.map(fmtRow).join('');
    }
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
    // 옛 값은 열자마자 알아야 한다. 숫자를 먼저 보고 나면 이미 늦다.
    var staleHtml = d.stale
      ? '<div class="dm-modal-stale"><b>'+d.date+' 값이다</b>'+DATA.staleWhy+'</div>'
      : '';
    bodyEl.innerHTML =
        '<h3 id="dm-modal-title" class="dm-modal-dname" tabindex="-1">'+d.label+'</h3>'
      + '<span class="dm-modal-loc">'+d.axisMeta+' · '+d.date+'</span>'
      + staleHtml
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

  // 드라이버 표의 행은 tr이라 Enter·Space가 저절로 먹지 않는다. 직접 붙인다.
  document.addEventListener('keydown', function(e){
    if(e.key !== 'Enter' && e.key !== ' ') return;
    var row = e.target.closest && e.target.closest('.dm-dt-row');
    if(!row) return;
    e.preventDefault();
    openDriverDirect(row.dataset.driver, row);
  });

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


DVTAB_JS = '''<script>
(function(){
  // 방법 안에서 글을 고르는 탭. 한 방법에 글이 여럿인 축(재무제표 여섯 편,
  // 멀티플 세 편)에서 값이 어느 글 것인지 섞이지 않게 가른다.
  document.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('.dm-dvtab');
    if(!t) return;
    var ax = t.dataset.axis, doc = t.dataset.doc;
    var wrap = t.closest('.dm-dvwrap');
    if(!wrap) return;
    wrap.querySelectorAll('.dm-dvtab').forEach(function(b){
      b.setAttribute('aria-selected', b.dataset.doc === doc ? 'true' : 'false');
    });
    wrap.querySelectorAll('.dm-dvdoc').forEach(function(d){
      d.hidden = !(d.dataset.axis === ax && d.dataset.doc === doc);
    });
  });
})();
</script>'''


# 회사 접두어(px)를 문자열에 구워 넣는 함수다 — 페이지에 지도가 둘 있으면 이 스크립트도
# 두 벌 실리는데, 각자 자기 접두어가 붙은 뿌리(#dm-<px>-root) 안에서만 찾고 움직여야
# 서로 안 부딪힌다. document 전체를 뒤지던 자리(getElementById('dm-axisbtns') 등)를
# 전부 그 뿌리 기준 조회로 바꿨다.
def _axbtn_js(px):
    return ('''<script>
(function(){
  var root = document.getElementById('dm-%(px)s-root');
  if(!root) return;
  var wrap = root.querySelector('.dm-axisbtns');
  if(!wrap) return;
  var btns = Array.prototype.slice.call(wrap.querySelectorAll('.dm-axisbtn'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('.dm-axispanel'));
  var heading = root.querySelector('.dm-axheading');

  function panelOf(id){ return root.querySelector('#dm-%(px)s-axispanel-' + id); }

  // 고르면 목록이 통째로 사라지고 그 방법만 남는다. 다섯을 늘 띄워 두면
  // 어느 것을 보고 있는지가 버튼 색 하나에만 걸린다.
  function open(id){
    var p = panelOf(id);
    if(!p) return;
    panels.forEach(function(x){ x.hidden = (x !== p); });
    btns.forEach(function(b){
      b.setAttribute('aria-expanded', b.dataset.axis === id ? 'true' : 'false');
    });
    wrap.hidden = true;
    if(heading) heading.hidden = true;
    var back = p.querySelector('.dm-axisback');
    if(back) back.focus();
  }

  function close(id){
    panels.forEach(function(x){ x.hidden = true; });
    btns.forEach(function(b){ b.setAttribute('aria-expanded', 'false'); });
    wrap.hidden = false;
    if(heading) heading.hidden = false;
    // 돌아왔을 때 방금 누른 버튼에 초점을 돌려준다 — 아니면 페이지 맨 위로 튄다.
    var b = root.querySelector('#dm-%(px)s-axisbtn-' + id);
    if(b) b.focus();
  }

  wrap.addEventListener('click', function(e){
    var b = e.target.closest('.dm-axisbtn');
    if(!b) return;
    open(b.dataset.axis);
  });

  // 뒤로가기 버튼은 이 뿌리 안에서만 듣는다 — document에 달면 옆 지도의 뒤로가기를
  // 눌러도 이 지도의 close()가 같이 실행돼 낭비다(결과적으로 잘못 움직이진 않지만).
  root.addEventListener('click', function(e){
    var back = e.target.closest('.dm-axisback');
    if(!back) return;
    close(back.dataset.axisback);
  });

  // 상세를 열어 둔 채 Esc를 누르면 목록으로 돌아온다. 단 모달이 떠 있으면
  // 그쪽만 닫혀야 한다.
  //
  // 캡처 단계에 단다. 버블 단계에 달면 모달의 Esc 핸들러가 먼저 돌아
  // dm-modal-open을 지운 뒤에 이 핸들러가 실행돼, 모달이 방금 닫힌 것을
  // 「모달 없음」으로 읽고 패널까지 같이 닫는다. Esc 한 번에 두 겹이 닫혔다.
  document.addEventListener('keydown', function(e){
    if(e.key !== 'Escape' || wrap.hidden !== true) return;
    if(document.body.classList.contains('dm-modal-open')) return;
    var openPanel = panels.filter(function(x){ return !x.hidden; })[0];
    if(!openPanel) return;
    var back = openPanel.querySelector('.dm-axisback');
    if(back) close(back.dataset.axisback);
  }, true);

  wrap.addEventListener('keydown', function(e){
    if(e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    var idx = btns.indexOf(document.activeElement);
    if(idx === -1) return;
    e.preventDefault();
    var next = e.key === 'ArrowRight' ? (idx + 1) %% btns.length
                                       : (idx - 1 + btns.length) %% btns.length;
    btns[next].focus();
  });
})();
</script>''' % {'px': px})

# 다섯 방법을 보여줄 순서. dcf(03)가 가장 완전한 평가라 기본으로 연다.
_AXIS_BTN_ORDER = ['stmt', 'simple', 'dcf', 'rev', 'mult']
_AXIS_BTN_DEFAULT = 'dcf'


def _axis_driver_docs(aid):
    """그 축의 드라이버가 어느 글에서 왔나. 축의 latest와 다를 수 있다 —
    stmt는 최신 글이 2026-04-17인데 드라이버는 전부 2024~2025년이다."""
    return sorted(d['doc'] for d in dmd.DRIVERS.values() if d['axis'] == aid)


def _axis_is_stale(aid):
    """드라이버가 하나도 남김없이 사이클 전환 앞쪽이면 그 축은 옛 값만 담고 있다."""
    docs = _axis_driver_docs(aid)
    return bool(docs) and all(dmd.is_stale(k) for k in docs)


def _axis_button_html(ax, stale):
    aid = ax['id']
    # 버튼의 큰 날짜는 그 축의 최신 글이었다. 그런데 01은 최신 글이 2026-04-17
    # (판매장려금 편)인데 드라이버는 하나도 그 글에서 오지 않는다. 다운사이클
    # 묶음에 2026년 날짜가 걸려 있으면 묶음과 버튼이 서로 어긋나 보인다.
    # 옛 묶음에서는 값이 실제로 어느 시점 것인지를 앞세우고, 최신 글은 작게 뒤로 뺀다.
    date_html = '<span class="dm-axisbtn-date">%s</span>' % ax['latest'][1]
    sub_html = ''
    if stale:
        # 값이 표로 옮겨 간 축은 드라이버가 하나도 없을 수 있다. 그때는 축이 선언한
        # docs로 기간을 잡는다 — 표만으로 서는 축도 버튼에 날짜가 있어야 한다.
        docs = _axis_driver_docs(aid) or sorted(ax.get('docs') or [])
    if stale and docs:
        # 한 글에서만 온 축은 「2025-12-10 ~ 2025-12-10」이 된다. 한 번만 적는다.
        span = (_doc_date(docs[0]) if docs[0] == docs[-1]
                else '%s ~ %s' % (_doc_date(docs[0]), _doc_date(docs[-1])))
        date_html = '<span class="dm-axisbtn-date">%s</span>' % span
        if ax['latest'][0] not in docs:
            sub_html = ('<span class="dm-axisbtn-stale" title="이 축의 최신 글에서는 '
                        '드라이버가 나오지 않았다">최신 글은 %s</span>' % ax['latest'][1])
    # 탭이 아니라 드릴다운이다 — 누르면 목록이 사라지고 그 방법만 남는다.
    # 그래서 aria-pressed(눌린 상태 유지)가 아니라 aria-expanded를 쓴다.
    return ('<button type="button" class="dm-axisbtn%s" id="dm-%s-axisbtn-%s" data-axis="%s" '
            'aria-expanded="false" aria-controls="dm-%s-axispanel-%s">'
            '<span class="dm-axisbtn-no">%s</span>'
            '<span class="dm-axisbtn-name">%s</span>'
            '%s%s</button>'
            % (' dm-axisbtn--stale' if stale else '', _PX, aid, aid, _PX, aid,
               ax['no'], ax['name'], date_html, sub_html))


def _axis_buttons_html():
    """시기를 위층, 방법을 아래층으로 놓는다. 방법을 먼저 고르게 두면 「재무제표
    분석」을 눌렀을 때 2024년 값이 나온다 — 눌러 본 뒤에야 알게 된다."""
    axes_by_id = {ax['id']: ax for ax in dmd.AXES}
    groups = []
    for era in dmd.AXIS_ERAS:
        stale = era['id'] != 'now'
        # 최신이 왼쪽이다. 옛 묶음은 드라이버가 나온 글의 마지막 날짜로, 지금 묶음은
        # 그 축의 최신 글 날짜로 잰다 — 버튼에 찍히는 날짜와 같은 기준이어야 한다.
        def _when(aid):
            ax = axes_by_id[aid]
            docs = _axis_driver_docs(aid) or sorted(ax.get('docs') or ())
            return _doc_date(docs[-1]) if (stale and docs) else ax['latest'][1]
        btns = ''.join(_axis_button_html(axes_by_id[aid], stale)
                       for aid in sorted(era['axes'], key=_when, reverse=True))
        groups.append(
            '<div class="dm-axisera%s">'
            '<div class="dm-axisera-head">'
            '<span class="dm-axisera-label">%s</span>'
            '<span class="dm-axisera-sub">%s</span></div>'
            '<div class="dm-axisera-btns">%s</div></div>'
            % (' dm-axisera--stale' if stale else '', era['label'], era['sub'], btns))
    return '<div class="dm-axisbtns" id="dm-%s-axisbtns">%s</div>' % (_PX, ''.join(groups))


def _era_axis_order():
    """시기 머리말 순서대로 축을 편다. 축을 새로 만들고 AXIS_ERAS에 안 넣으면
    화면에서 조용히 사라지므로 여기서 잡는다."""
    order = [aid for era in dmd.AXIS_ERAS for aid in era['axes']]
    missing = [ax['id'] for ax in dmd.AXES if ax['id'] not in order]
    if missing:
        raise ValueError('AXIS_ERAS에 빠진 축: %s' % ', '.join(missing))
    return order


def _axis_panels_html():
    """처음엔 하나도 열지 않는다. 방법 목록이 먼저 보이고, 고른 뒤에 그 방법만 남는다.
    다섯을 늘 띄워 두면 어느 것을 보고 있는지가 버튼 색 하나에만 걸린다."""
    axes_by_id = {ax['id']: ax for ax in dmd.AXES}
    parts = []
    for aid in _era_axis_order():
        ax = axes_by_id[aid]
        era = next(e for e in dmd.AXIS_ERAS if aid in e['axes'])
        back = ('<button type="button" class="dm-axisback" data-axisback="%s">'
                '<span class="dm-axisback-arrow" aria-hidden="true">◂</span>'
                '<span class="dm-axisback-text">방법 다시 고르기</span>'
                '<span class="dm-axisback-era">%s</span></button>' % (aid, era['label']))
        parts.append(
            '<div class="dm-axispanel" id="dm-%s-axispanel-%s" role="region" '
            'aria-labelledby="dm-%s-axisbtn-%s" hidden>%s%s</div>'
            % (_PX, aid, _PX, aid, back, _axis_html(ax)))
    return '<div class="dm-axispanels">%s</div>' % ''.join(parts)


def render(data=None, judgment_dir='005930-삼성전자'):
    """드라이버 지도 한 장. data는 driver_map_data 꼴 모듈(기본은 삼성전자),
    judgment_dir는 insights/valuation/ 아래 그 회사 판정 폴더 이름이다. 없으면(None)
    「내 판정」 층 전체를 건너뛴다 — 판정 파일이 없는 회사도 지도는 그려야 한다.

    한 페이지에 지도가 둘 있어도(회사별로) id·JS가 안 부딪히게, 데이터 모듈 이름에서
    뽑은 접두어(_PX)를 뿌리 요소와 그 안의 id마다 붙인다."""
    global dmd, _JUDGMENT_PATH, _JUDGMENTS, _JUDGMENT_ASOF, _JUDGMENT_TODO
    global _GROUP_OF, _AXIS_IDS, _AXIS_LOOKUP, _RESOLVE_LOG, _resolve_cache, _PX

    dmd = data or driver_map_data
    _PX = _prefix_for(dmd)
    _JUDGMENT_PATH = (os.path.join(dc.ROOT, 'insights', 'valuation', judgment_dir, 'judgment.json')
                       if judgment_dir else None)
    _RESOLVE_LOG = []
    _resolve_cache = {}
    _JUDGMENTS, _JUDGMENT_ASOF, _JUDGMENT_TODO = _load_judgment()

    _GROUP_OF = {}
    for _g in dmd.GROUPS:
        for _ms in _g['members'].values():
            for _m in _ms:
                _GROUP_OF[_m] = _g['name']

    _AXIS_IDS = set(ax['id'] for ax in dmd.AXES)
    _AXIS_LOOKUP = {ax['id']: (ax['no'], ax['name']) for ax in dmd.AXES}
    _AXIS_LOOKUP['quote'] = ('—', '외부 인용')

    # data_json은 아무 데도 안 붙는다(모달을 걷어낸 뒤로 죽은 계산이다) — 그래도 그대로
    # 둔다. _RESOLVE_LOG(인용 링크 해석 성공/실패 집계)가 이 호출의 부작용으로 채워지고,
    # __main__ 진단 출력이 그 집계를 쓴다. 계산을 지우면 진단 출력만 조용히 달라진다.
    data_json = json.dumps(_data_json(), ensure_ascii=False).replace('</', '<\\/')  # noqa: F841

    parts = [DM_CSS]
    parts.append('<div class="dm-wrap" id="dm-%s-root">' % _PX)
    parts.append('<div class="dm-head"><h2 class="dm-title">무엇을 얼마로 가정했나</h2>'
                  '<p class="dm-lede">%s</p></div>' % dmd.LEDE)
    # 주인장 계산은 DCF 축 패널 안으로 옮겼다(_axis_html). 여기서 또 그리면 두 벌이 된다.
    # 드라이버 범위 표(_ranges_html)는 걷어냈다. 같은 내용이 각 드라이버 상세의
    # 「영향」 칸에 들어 있어 두 번 말하는 셈이었다.
    # 연도별 이익 경로 표는 DCF 축 패널 안으로 옮겼다 — 연도별 추정이 그 방법의
    # 본체라서다. 07-16 민감도 격자도 같은 이유로 그 패널 안에 있다.
    # 상세를 열면 이 머리말도 목록과 함께 접힌다 — 고르라고 해 놓고 이미 고른
    # 뒤에도 남아 있으면 아직 목록이 있는 줄 안다.
    parts.append(('<h2 class="dm-axheading" id="dm-%s-axheading">'
                 '엘곰이 한 것. 시기를 고르면 그 안에서 방법이 나온다</h2>') % _PX)
    parts.append(_axis_buttons_html())
    parts.append(_axis_panels_html())
    parts.append(_judgment_todo_html(_JUDGMENT_TODO, _JUDGMENT_ASOF))
    parts.append(
        '<details class="dm-past">'
        '<summary class="dm-past-summary">%s</summary>'
        '<div class="dm-past-body">%s</div>'
        '</details>' % (dmd.TIMELINE_LABEL, _timeline_html()))
    parts.append('</div>')
    # 모달과 그 데이터(dm-data)·JS는 걷어냈다. 값·근거·왜·영향·판정을 전부 지면에
    # 펼쳐 두었으므로 눌러서 열 것이 남지 않았다. 축 고르기 JS만 남는다.
    parts.append(_axbtn_js(_PX))
    parts.append(DVTAB_JS)
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
