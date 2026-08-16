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
        rows.append(
            '<button type="button" class="dm-gchip" data-group="%s" data-members="%s" '
            'aria-haspopup="dialog">'
            '<span class="dm-gchip-name">%s</span><span class="dm-gchip-n">· %d</span>%s'
            '</button>' % (g['id'], ','.join(members), g['name'], len(members), warn_html))
    if not rows:
        return ''
    return '<div class="dm-gchips">%s</div>' % ''.join(rows)


def _axis_html(ax):
    # 역산(rev)은 방향이 반대다 — 가격이 출력이 아니라 입력이다. 그래서 셋과
    # 같은 「적정가」 줄에 세우지 않고, 테두리·머리 색·결과 라벨을 다르게 그린다.
    is_rev = ax.get('kind') == 'reverse'
    axis_cls = 'dm-axis dm-axis--reverse' if is_rev else 'dm-axis'
    input_driver = dmd.INPUT_DRIVER.get(ax['id']) if is_rev else None

    inputs_html = ''
    if ax.get('inputs'):
        rows = []
        for k, v in ax['inputs']:
            if input_driver and '시가총액' in k:
                rows.append(
                    '<button type="button" class="dm-inputs-row dm-inputs-row--btn" '
                    'data-driver="%s" data-noback="1">'
                    '<span class="dm-inputs-k">%s</span><span class="dm-inputs-v">%s</span>'
                    '</button>' % (input_driver, k, v))
            else:
                rows.append('<div class="dm-inputs-row"><span class="dm-inputs-k">%s</span>'
                            '<span class="dm-inputs-v">%s</span></div>' % (k, v))
        inputs_html = '<div class="dm-inputs"><p class="dm-inputs-label">입력</p>%s</div>' % ''.join(rows)

    chain_html = ''.join('<p class="dm-chain-line">%s</p>' % _linkify(c) for c in ax['chain'])
    gchips_html = _group_chips_html(ax)

    out_tag = '이 가격이 요구하는 것' if is_rev else '결과'
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

    # 역산 축의 값어치는 필자를 감사하는 데 있지 않고 시장이 무엇을 깔고 있는지를
    # 읽는 데 있다. 그래서 같은 공식을 시점마다 내가 다시 돌린 표를 결과 뒤에 붙인다.
    mr_html = ''
    if ax.get('market_read'):
        mr = ax['market_read']
        head = ''.join('<th>%s</th>' % h for h in mr['head'])
        body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in mr['rows'])
        mr_html = ('<div class="dm-mr"><p class="dm-mr-label">시장이 요구하는 것 — 시점마다 다시 계산했다 %s</p>'
                   '<div class="dm-mr-wrap"><table class="dm-mr-tbl">'
                   '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                   '<p class="dm-mr-note">%s</p></div>' % (_by_badge('ours'), head, body, mr['note']))

    bench_html = ''
    if ax.get('benchmark'):
        rows = ''.join(
            '<div class="dm-bench-row"><div class="dm-bench-top">'
            '<span class="dm-bench-k">%s</span><span class="dm-bench-v">%s</span></div>'
            '<p class="dm-bench-note">%s</p></div>' % (k, v, note)
            for k, v, note in ax['benchmark'])
        bench_html = ('<div class="dm-bench"><p class="dm-bench-label">이 요구가 말이 되나</p>%s</div>'
                      % rows)

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
            '<p class="dm-axis-sub">%s</p>'
            '%s'
            '<div class="dm-chain">%s</div>'
            '%s'
            '%s'
            '%s'
            '%s'
            '%s'
            '</article>'
            % (axis_cls, ax['id'], ax['no'], ax['name'], ax['tag'], ax['sub'],
               inputs_html, chain_html, gchips_html, out_html, mr_html, bench_html, verdict_html))


_AXIS_IDS = set(ax['id'] for ax in dmd.AXES)
_AXIS_LOOKUP = {ax['id']: (ax['no'], ax['name']) for ax in dmd.AXES}
_AXIS_LOOKUP['quote'] = ('—', '외부 인용')



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
            if i == 4:
                tds.append('<td class="dm-sc-gap%s">%s</td>' % (tone_cls, c))
            else:
                tds.append('<td>%s</td>' % c)
        tds.append('<td>%s</td>' % _by_badge(r['by']))
        body_rows.append('<tr class="dm-sc-row">%s</tr>' % ''.join(tds))
    # 엘곰도 시나리오를 만들었다 — 다만 02-26 역산 글에서만이다. 그걸 안 보이면
    # 내가 만든 사다리를 그의 것으로 읽는다. 시점이 달라 같은 표엔 못 넣는다.
    auth_html = ''
    if s.get('author_scenarios'):
        au = s['author_scenarios']
        ah2 = ''.join('<th>%s</th>' % h for h in au['head'])
        ab2 = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in au['rows'])
        auth_html = (
            '<div class="dm-auth"><p class="dm-auth-label">%s %s</p>'
            '<p class="dm-auth-lede">%s</p>'
            '<div class="dm-auth-wrap"><table class="dm-auth-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '<p class="dm-auth-note">%s</p></div>'
            % (au['label'], _by_badge(au['by']), au['lede'], ah2, ab2, au['note']))

    # 역산은 방향이 반대라 같은 표에 넣으면 네 번째 시나리오로 읽힌다. 블록을 따로 세운다.
    rev_html = ''
    if s.get('reverse'):
        rv = s['reverse']
        cmps = ''.join(
            '<div class="dm-rv-cmp dm-rv-cmp--%s"><span class="dm-rv-cmp-k">%s</span>'
            '<span class="dm-rv-cmp-v">%s</span></div>' % (tone, k, v)
            for k, v, tone in rv['compare'])
        rev_html = (
            '<div class="dm-rv">'
            '<p class="dm-rv-label">%s %s</p>'
            '<p class="dm-rv-lede">%s</p>'
            '<p class="dm-rv-formula">%s</p>'
            '<div class="dm-rv-result"><span class="dm-rv-val">%s</span>'
            '<span class="dm-rv-note">%s</span></div>'
            '<div class="dm-rv-cmps">%s</div>'
            '</div>' % (rv['label'], _by_badge(rv['by']), rv['lede'], rv['formula'],
                        rv['result'], rv['result_note'], cmps))
    return ('<div class="dm-scenario">'
            '<div class="dm-scenario-head">'
            '<p class="dm-scenario-kicker">이 시점의 평가 — 이 페이지의 결론</p>'
            '<div class="dm-scenario-meta">'
            '<span class="dm-scenario-asof">%s 기준</span>'
            '<span class="dm-scenario-price">주가 %s</span>'
            '<span class="dm-scenario-mcap">시가총액 %s</span>'
            '</div></div>'
            '%s'
            '<p class="dm-fwd-label">정방향 — 이익을 가정하면 적정가가 나온다</p>'
            '<p class="dm-scenario-formula">%s</p>'
            '<div class="dm-scenario-wrap"><table class="dm-scenario-tbl">'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            '%s'
            '%s'
            '<p class="dm-scenario-note">%s</p>'
            '<div class="dm-scenario-punch">%s</div>'
            '</div>'
            % (s['asof'], s['price'], s['mcap'], act_html, s['formula'], head,
               ''.join(body_rows), rev_html, auth_html, s['note'], s['punch']))


def _timeline_html():
    # kind: 'price'(적정가를 낸 평가) | 'ask'(역산 — 가격이 입력이라 값이 아니라
    # 요구 문장이다). 같은 줄의 값처럼 보이면 안 되므로 마름모·점선 상자로 따로 그린다.
    items = []
    for date, axid, kind, v1, v2, tag, by in dmd.TIMELINE:
        no, name = _AXIS_LOOKUP.get(axid, ('—', axid))
        target = ' data-target="dm-axis-%s"' % axid if axid in _AXIS_IDS else ''
        badge_html = _by_badge(by)
        if kind == 'ask':
            items.append(
                '<div class="dm-tl-item dm-tl-ask"%s tabindex="0" role="button">'
                '<span class="dm-tl-dot dm-tl-ask-mark" aria-hidden="true"></span>'
                '<span class="dm-tl-date">%s</span>'
                '<div class="dm-tl-ask-body">'
                '<p class="dm-tl-ask-sent">%s <b>%s</b></p>'
                '<span class="dm-tl-tag">%s</span> %s'
                '</div></div>' % (target, date, v1, v2, tag, badge_html))
            continue
        cls = ' dm-tl-quote' if axid == 'quote' else ''
        tag_html = '<span class="dm-tl-tag">%s</span>' % tag if tag else ''
        v2_html = '<span class="dm-tl-v2">%s</span>' % v2 if v2 else ''
        items.append(
            '<div class="dm-tl-item%s"%s tabindex="0" role="button">'
            '<span class="dm-tl-dot" aria-hidden="true"></span>'
            '<span class="dm-tl-date">%s</span>'
            '<span class="dm-tl-axis">%s %s</span>'
            '<span class="dm-tl-v1">%s</span>'
            '%s'
            '%s %s'
            '</div>' % (cls, target, date, no, name, v1, v2_html, tag_html, badge_html))
    return ('<div class="dm-timeline"><div class="dm-tl-track">%s</div></div>'
            '<p class="dm-tl-hint">점을 누르면 그 축 카드로 이동한다</p>' % ''.join(items))


def _data_json():
    """모달 JS가 쓰는 데이터. drivers는 예전 그대로, groups는 새로 추가한
    상위 드라이버(1단계 화면) 메타다 — members는 축마다 달라 칩의 data-members로 넘긴다."""
    axis_meta = {ax['id']: '%s %s' % (ax['no'], ax['name']) for ax in dmd.AXES}
    drivers = {}
    for did, d in dmd.DRIVERS.items():
        basis_label, basis_desc = dmd.BASIS[d['basis']]
        url = dc.blob(dmd.SUM + dmd.DOCS[d['doc']]) + '#L%d' % d['line']
        drivers[did] = dict(
            label=d['label'], axisMeta=axis_meta.get(d['axis'], d['axis']),
            doc=d['doc'], line=d['line'], base=d['base'],
            basisKey=d['basis'], basisLabel=basis_label, basisDesc=basis_desc,
            why=d['why'], impact=d['impact'], url=url,
            bar=list(d['bar']) if 'bar' in d else None,
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

/* ── 정방향 / 역방향 ── 방향이 반대라 한 표에 세우면 네 번째 시나리오로 읽힌다 */
.dm-fwd-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);margin:14px 0 4px}
.dm-rv{margin:16px 0 0;border-left:3px solid var(--accent);background:var(--accent-soft);
       border-radius:0 10px 10px 0;padding:12px 15px}
.dm-rv-label{font-size:12px;font-weight:850;letter-spacing:.02em;color:var(--accent-ink);margin:0 0 4px}
.dm-rv-lede{font-size:12px;line-height:1.6;color:var(--ink-2);margin:0 0 8px}
.dm-rv-formula{font-size:11.5px;line-height:1.6;color:var(--ink-3);margin:0 0 10px;
               font-variant-numeric:tabular-nums}
.dm-rv-result{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin:0 0 10px}
.dm-rv-val{font-size:24px;font-weight:850;letter-spacing:-.02em;color:var(--ink);
           font-variant-numeric:tabular-nums;line-height:1.1}
.dm-rv-note{font-size:12px;line-height:1.55;color:var(--ink-2);flex:1 1 16ch;min-width:16ch}
.dm-rv-cmps{display:grid;gap:6px;grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
.dm-rv-cmp{display:flex;align-items:baseline;justify-content:space-between;gap:8px;
           background:var(--surface);border-radius:8px;padding:6px 10px}
.dm-rv-cmp-k{font-size:11px;color:var(--ink-3)}
.dm-rv-cmp-v{font-size:13px;font-weight:850;font-variant-numeric:tabular-nums}
.dm-rv-cmp--high .dm-rv-cmp-v{color:var(--warn)}
.dm-rv-cmp--low .dm-rv-cmp-v{color:var(--good)}

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

/* ── 시간축 ── */
.dm-timeline{margin:18px 0 4px;overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-tl-track{display:flex;gap:0;position:relative;min-width:max-content;padding:8px 2px 2px}
/* 선은 점 한가운데를 지나야 한다. 점 위를 스치면 어긋나 보인다 */
.dm-tl-track::before{content:"";position:absolute;left:14px;right:14px;top:24px;height:1px;background:var(--line)}
/* 위 여백이 22px이면 점(12~21px)과 날짜가 맞붙어 1px 겹쳤다. 32px로 벌린다 */
.dm-tl-item{position:relative;display:flex;flex-direction:column;gap:2px;width:150px;flex:0 0 auto;
            padding:32px 10px 8px;cursor:pointer;border-radius:8px;border:0;background:transparent;
            text-align:left;font:inherit}
.dm-tl-item:hover{background:var(--sunk)}
.dm-tl-item:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.dm-tl-dot{position:absolute;left:10px;top:12px;width:9px;height:9px;border-radius:50%;
           background:var(--accent);border:2px solid var(--surface)}
.dm-tl-quote .dm-tl-dot{background:var(--warn)}
.dm-tl-date{font-size:10.5px;font-weight:800;color:var(--ink-3);font-variant-numeric:tabular-nums}
.dm-tl-axis{font-size:10.5px;color:var(--ink-3)}
.dm-tl-v1{font-size:13px;font-weight:800;color:var(--ink);margin-top:2px}
.dm-tl-v2{font-size:11.5px;color:var(--ink-2)}
.dm-tl-tag{align-self:flex-start;font-size:9.5px;font-weight:800;color:var(--ink-3);
           background:var(--sunk);border-radius:999px;padding:1px 7px;margin-top:3px}
.dm-tl-hint{margin:2px 0 22px;font-size:11px;color:var(--ink-3)}
/* 역산 항목 — 값이 아니라 「이 가격이 요구하는 것」이라 같은 줄의 점으로 보이면 안 된다 */
.dm-tl-item.dm-tl-ask{width:190px}
.dm-tl-ask-mark{border-radius:2px;background:var(--warn);transform:rotate(45deg)}
.dm-tl-ask-body{margin-top:8px;padding:8px 9px;border:1px dashed var(--warn);
                border-radius:8px;background:var(--warn-soft)}
.dm-tl-ask-sent{margin:0 0 5px;font-size:11.5px;line-height:1.55;color:var(--ink-2)}
.dm-tl-ask-sent b{color:var(--ink);font-weight:800}

/* ── 축 4개 ── */
/* 넷을 한 줄에 세우면 1280px에서 칸이 300px도 안 돼 수식이 잘게 접힌다.
   아주 넓을 때만 4열로 간다 */
.dm-axes{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:0 0 24px;
         align-items:start}
@media (max-width:560px){.dm-axes{grid-template-columns:1fr}}
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
.dm-inputs-row{display:flex;justify-content:space-between;gap:8px;font-size:11.5px;padding:2px 0}
.dm-inputs-k{color:var(--ink-3)}
.dm-inputs-v{font-weight:700;color:var(--ink);text-align:right}
.dm-inputs-row--btn{border:0;background:transparent;width:100%;text-align:left;font:inherit;
                    cursor:pointer;border-radius:6px;padding:3px 4px}
.dm-inputs-row--btn:hover{background:var(--surface)}
.dm-inputs-row--btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.dm-bench{margin:0 0 12px;padding:10px 10px 1px;border:1px dashed var(--line);border-radius:8px}
.dm-bench-label{font-size:10px;font-weight:800;color:var(--ink-3);letter-spacing:.06em;margin:0 0 8px}
.dm-bench-row{margin:0 0 9px}
.dm-bench-top{display:flex;justify-content:space-between;gap:6px;font-size:11.5px}
.dm-bench-k{color:var(--ink-2)}
.dm-bench-v{font-weight:800;color:var(--ink);white-space:nowrap}
.dm-bench-note{margin:2px 0 0;font-size:10.5px;color:var(--ink-3)}

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
           +   '<span class="dm-modal-row-label">'+d.label+'</span>'
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
      + '<a class="dm-detail-src" href="'+d.url+'" target="_blank" rel="noopener">출처: 요약본 L'+d.line+' ▸</a>';
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


def render():
    axes_html = ''.join(_axis_html(ax) for ax in dmd.AXES)
    data_json = json.dumps(_data_json(), ensure_ascii=False).replace('</', '<\\/')
    parts = [DM_CSS]
    parts.append('<div class="dm-wrap">')
    parts.append('<div class="dm-head"><h2 class="dm-title">드라이버 지도 — 무엇을 얼마로 가정했나</h2>'
                  '<p class="dm-lede">%s</p></div>' % dmd.LEDE)
    parts.append(_scenario_html())
    parts.append('<div class="dm-axes">%s</div>' % axes_html)
    # 연도별 이익 경로 표는 옛 평가가 아니다 — 07-16 가정의 상세다(그 열이 표 안에 있다).
    # 접어 두면 못 찾는다. 축 바로 뒤에 펼쳐 둔다.
    parts.append(_earnpath_html())
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
    return '\n'.join(parts)


if __name__ == '__main__':
    out = render()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print('OK: 렌더 길이 %d자 / 축 %d개 / 상위칩 %d개 / 드라이버 %d개'
          % (len(out), len(dmd.AXES), out.count('class="dm-gchip"'), len(dmd.DRIVERS)))
