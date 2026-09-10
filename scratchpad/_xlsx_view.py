# -*- coding: utf-8 -*-
"""받은 엑셀을 화면에 그대로 편다.

프레임 값을 본문에 옮겨 적기만 하면 독자가 「그 표가 실제로 어떻게 생겼나」를 못 본다.
이 모듈은 시트 한 조각을 읽어 표로 낸다 — 값만 옮기고 수식은 칸의 title 로 붙인다.
숫자를 고치지 않는다. 받은 그대로다.

파일은 `대시보드/model/*.xlsx` 에 두고 화면에서 내려받을 수 있게 한다. 전사본은
`scratchpad/capex_frame_xlsx.md` 와 `scratchpad/capex_frame_scn.md` 가 갖고 있다.
"""
import io
import os

import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, '대시보드', 'model')

FILES = {
    'big4': 'AI_DC_Capex_Big4.xlsx',
    'hbm': 'AI_DC_Capex_Big4_HBM.xlsx',
    'scn': 'AI_DC_Capex_Big4_HBM_Scn.xlsx',
}

_CACHE = {}


def _book(key, formulas=False):
    ck = (key, formulas)
    if ck not in _CACHE:
        p = os.path.join(XLSX, FILES[key])
        _CACHE[ck] = openpyxl.load_workbook(p, data_only=not formulas)
    return _CACHE[ck]


def _fmt(v):
    """칸 하나를 글자로. 소수는 두 자리까지만 보이고 정수는 그대로 둔다."""
    if v is None:
        return ''
    if isinstance(v, float):
        if abs(v) < 1 and v != 0:
            return '%.3f' % v
        if abs(v - round(v)) < 1e-9:
            return format(int(round(v)), ',')
        return format(round(v, 2), ',')
    if isinstance(v, int):
        return format(v, ',')
    return str(v)


def sheet_html(key, sheet, r1, r2, c1, c2, note=''):
    """시트 한 조각을 표로 낸다. 첫 행을 머리로, 첫 열을 이름 열로 세운다."""
    ws = _book(key).worksheets[[w.title for w in _book(key).worksheets].index(sheet)]
    fs = _book(key, True).worksheets[
        [w.title for w in _book(key, True).worksheets].index(sheet)]
    rows = []
    for r in range(r1, r2 + 1):
        cells = []
        empty = True
        for c in range(c1, c2 + 1):
            v = ws.cell(row=r, column=c).value
            f = fs.cell(row=r, column=c).value
            txt = _fmt(v)
            if txt:
                empty = False
            cells.append((txt, f if isinstance(f, str) and f.startswith('=') else ''))
        if not empty:
            rows.append(cells)
    if not rows:
        return ''
    out = ['<div class="xls" data-quote="1"><div class="xlt">'
           '%s · %s 시트 %s%d:%s%d</div><div class="xlw">'
           % (FILES[key], sheet, chr(64 + c1), r1, chr(64 + c2), r2),
           '<table class="xl"><thead><tr>']
    for txt, _f in rows[0]:
        out.append('<th>%s</th>' % txt)
    out.append('</tr></thead><tbody>')
    for cells in rows[1:]:
        out.append('<tr>')
        for i, (txt, f) in enumerate(cells):
            cls = ' class="num"' if i and txt and txt[0].isdigit() or (
                i and txt.startswith('-')) else ''
            title = ' title="%s"' % f.replace('"', '&quot;') if f else ''
            out.append('<td%s%s>%s</td>' % (cls, title, txt))
        out.append('</tr>')
    out.append('</tbody></table></div></div>')
    if note:
        out.append('<p class="xl-memo">%s</p>' % note)
    return ''.join(out)


def downloads():
    """내려받기 줄. 파일은 그 장의 글 페이지 폴더에 같이 선다."""
    items = []
    for key, fn in FILES.items():
        size = os.path.getsize(os.path.join(XLSX, fn)) // 1024
        items.append('<a href="%s">%s</a> (%dKB)' % (fn, fn, size))
    return ('<p class="xl-memo"><b>파일 내려받기</b><br>' + ' · '.join(items)
            + '<br>세 개가 같은 모델의 판 셋입니다 — 기본, HBM 을 더한 판, '
              '케이스 스위치를 더한 판입니다.</p>')
