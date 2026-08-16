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
    # 읽는 데 있다. 그래서 같은 공식을 시점마다 우리가 다시 돌린 표를 결과 뒤에 붙인다.
    mr_html = ''
    if ax.get('market_read'):
        mr = ax['market_read']
        head = ''.join('<th>%s</th>' % h for h in mr['head'])
        body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % c for c in r) for r in mr['rows'])
        mr_html = ('<div class="dm-mr"><p class="dm-mr-label">시장이 요구하는 것 — 시점마다 다시 계산했다</p>'
                   '<div class="dm-mr-wrap"><table class="dm-mr-tbl">'
                   '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                   '<p class="dm-mr-note">%s</p></div>' % (head, body, mr['note']))

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


def _conclusions_html():
    """축 넷을 다 읽어야 나오는 것을 맨 위에 먼저 놓는다. 아래로 스크롤하기 전에
    무엇이 문제인지 알고 들어가야 드라이버를 누를 이유가 생긴다."""
    cards = []
    for c in dmd.CONCLUSIONS:
        cards.append(
            '<div class="dm-cc dm-cc--%s">'
            '<div class="dm-cc-big">%s</div>'
            '<div class="dm-cc-label">%s</div>'
            '<p class="dm-cc-body">%s</p>'
            '</div>' % (c.get('tone', 'plain'), c['big'], c['label'], c['body']))
    return ('<div class="dm-concl">'
            '<p class="dm-concl-h">결론 — 열다섯 달을 가로질러 본 것</p>'
            '<div class="dm-cc-grid">%s</div>'
            '</div>' % ''.join(cards))


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


def _timeline_html():
    # kind: 'price'(적정가를 낸 평가) | 'ask'(역산 — 가격이 입력이라 값이 아니라
    # 요구 문장이다). 같은 줄의 값처럼 보이면 안 되므로 마름모·점선 상자로 따로 그린다.
    items = []
    for date, axid, kind, v1, v2, tag in dmd.TIMELINE:
        no, name = _AXIS_LOOKUP.get(axid, ('—', axid))
        target = ' data-target="dm-axis-%s"' % axid if axid in _AXIS_IDS else ''
        if kind == 'ask':
            items.append(
                '<div class="dm-tl-item dm-tl-ask"%s tabindex="0" role="button">'
                '<span class="dm-tl-dot dm-tl-ask-mark" aria-hidden="true"></span>'
                '<span class="dm-tl-date">%s</span>'
                '<div class="dm-tl-ask-body">'
                '<p class="dm-tl-ask-sent">%s <b>%s</b></p>'
                '<span class="dm-tl-tag">%s</span>'
                '</div></div>' % (target, date, v1, v2, tag))
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
            '%s'
            '</div>' % (cls, target, date, no, name, v1, v2_html, tag_html))
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

/* ── 결론 ── 축을 다 읽어야 나오는 것을 맨 위에 먼저 놓는다 */
.dm-concl{margin:20px 0 6px}
.dm-concl-h{font-size:12px;font-weight:850;letter-spacing:.06em;color:var(--ink-3);
            text-transform:uppercase;margin:0 0 10px}
.dm-cc-grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
.dm-cc{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--line);
       border-radius:10px;padding:13px 15px;box-shadow:var(--shadow)}
.dm-cc--warn{border-left-color:var(--warn);background:var(--warn-soft)}
.dm-cc--ok{border-left-color:var(--accent)}
.dm-cc-big{font-size:23px;font-weight:850;letter-spacing:-.02em;color:var(--ink);
           font-variant-numeric:tabular-nums;line-height:1.1}
.dm-cc--warn .dm-cc-big{color:var(--warn)}
.dm-cc--ok .dm-cc-big{color:var(--accent)}
.dm-cc-label{font-size:12px;font-weight:800;color:var(--ink-3);margin-top:3px}
.dm-cc-body{font-size:13px;line-height:1.6;color:var(--ink-2);margin:8px 0 0}
@media (max-width:640px){.dm-cc-grid{grid-template-columns:1fr}}

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

/* ── 이익 성장 경로 표 ── */
.dm-ep{margin:20px 0 4px;background:var(--surface);border:1px solid var(--line);
       border-radius:10px;padding:14px 16px;box-shadow:var(--shadow)}
.dm-ep-label{font-size:11px;font-weight:850;letter-spacing:.04em;color:var(--ink-3);margin:0 0 9px}
.dm-ep-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.dm-ep-tbl{width:100%;border-collapse:collapse;font-size:12.5px;font-variant-numeric:tabular-nums}
.dm-ep-tbl th{font-size:11px;font-weight:850;letter-spacing:.02em;color:var(--ink-2);
              text-align:left;padding:4px 12px 7px 0;border-bottom:1px solid var(--line);
              white-space:nowrap;vertical-align:bottom}
/* 보수·기준·직접이 무슨 뜻인지 머리에서 바로 알려 준다 */
.dm-ep-tbl th span{display:block;font-size:10px;font-weight:700;color:var(--ink-3);
                   letter-spacing:0;margin-top:3px;white-space:normal;max-width:19ch}
.dm-ep-tbl td{padding:5px 12px 5px 0;border-bottom:1px solid var(--line);
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
.dm-tl-track::before{content:"";position:absolute;left:10px;right:10px;top:19px;height:1px;background:var(--line)}
.dm-tl-item{position:relative;display:flex;flex-direction:column;gap:2px;width:150px;flex:0 0 auto;
            padding:22px 10px 8px;cursor:pointer;border-radius:8px;border:0;background:transparent;
            text-align:left;font:inherit}
.dm-tl-item:hover{background:var(--sunk)}
.dm-tl-item:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.dm-tl-dot{position:absolute;left:10px;top:14px;width:9px;height:9px;border-radius:50%;
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
.dm-tl-ask-body{margin-top:18px;padding:8px 9px;border:1px dashed var(--warn);
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
.dm-modal-backdrop{position:fixed;inset:0;z-index:200;display:flex;align-items:center;
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
    parts.append(_conclusions_html())
    parts.append(_timeline_html())
    parts.append(_earnpath_html())
    parts.append('<div class="dm-axes">%s</div>' % axes_html)
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
